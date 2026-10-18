"""Reviewer-owned opaque/text checker. Never load, parse as Python, or run subjects."""
from pathlib import Path
import hashlib
import json
import os
import re
import stat

ROOT = Path('/Volumes/AI_DATA/development/det-review-evidence')
Q = ROOT/'ri140-native-failure-repair-source-l_a4mna0'
OLD = ROOT/'ri138-native-external-launch-source-92pbd52w'
OUT = ROOT/'ri140-independent-source-review-i57s4u4b'
EXCLUDED = {str(ROOT/'ri138-launch-independent-review-6xGu5oak'/n) for n in ('check_metadata.py', 'check_metadata_v2.py', 'OPAQUE_TEXT_CHECK.json', 'OPAQUE_TEXT_CHECK_V2.json')}
CAP = 67108864
checks, errors, observations = [], [], []

def require(c, m):
    if not c:
        raise ValueError(m)

def sig(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def opaque(path, expected=None, retain=False):
    path=Path(path)
    require(str(path) not in EXCLUDED, 'excluded diagnostic body')
    require(path.is_absolute() and os.path.normpath(str(path)) == str(path), 'noncanonical path')
    for p in list(reversed(path.parents))+[path]:
        require(not p.is_symlink(), 'symlink at '+str(p))
    before=path.lstat(); require(stat.S_ISREG(before.st_mode) and before.st_size <= CAP, 'regular/cap')
    chunks=[]; h=hashlib.sha256(); n=0
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        opened=os.fstat(fd)
        while True:
            b=os.read(fd,min(1048576,CAP+1-n))
            if not b: break
            n+=len(b); require(n<=CAP,'growth/cap'); h.update(b)
            if retain: chunks.append(b)
        after=os.fstat(fd)
    finally:
        os.close(fd)
    require(sig(before)==sig(opened)==sig(after)==sig(path.lstat()) and n==after.st_size,'unstable input')
    found={'path':str(path),'bytes':n,'sha256':h.hexdigest()}
    if expected is not None:
        require({k:expected[k] for k in found}==found,'identity mismatch '+str(path))
        if 'resolved_path' in expected:
            require(expected['resolved_path']==str(path) and expected['symlinks']==[], 'unexpected alias')
    observations.append(found)
    return b''.join(chunks) if retain else found

def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate metadata key'); d[k]=v
    return d

def readmeta(path, expected=None):
    return json.loads(opaque(path,expected,True), object_pairs_hook=pairs)

def checkpoint(label, f):
    try:
        detail=f(); checks.append({'label':label,'passed':True,'detail':detail})
    except Exception as e:
        errors.append({'label':label,'type':type(e).__name__,'message':str(e)})
        checks.append({'label':label,'passed':False})

h=readmeta(Q/'HANDOFF.json',{'path':str(Q/'HANDOFF.json'),'bytes':6044,'sha256':'8726a3d8be2d62b2326a6ad45d5e1f497fda521d4a1e4a9c92e04101c16f2141'})
require(sorted(p.name for p in Q.iterdir())==sorted([Path(i['path']).name for i in h['files']]+['HANDOFF.json']),'namespace')
for i in h['files']: opaque(i['path'],i)
checks.append({'label':'exact_current_namespace_payloads','passed':True,'names':17,'payloads':16})
d=readmeta(Q/'SOURCE_DEPENDENCIES.json'); old=readmeta(OLD/'SOURCE_DEPENDENCIES.json')
by={e['path']:e for e in d['protected_files']}; inherited={e['path']:e for e in old['protected_files']}
require(len(by)==423 and len(inherited)==396 and list(by)==sorted(by),'423/396/order')
for ix,e in enumerate(d['protected_files'],1):
    require(e['role']=='dep_'+str(ix).zfill(4) and e['identity']['path']==e['path'],'role/path')
    checkpoint('dependency:'+e['role'],lambda e=e:opaque(e['path'],e['identity']))
for path,e in inherited.items():
    require({k:v for k,v in e.items() if k!='role'}=={k:v for k,v in by[path].items() if k!='role'},'inherited row differs')
added=[e for p,e in by.items() if p not in inherited]
require(len(added)==27 and not EXCLUDED.intersection(by),'additions/exclusions')
checks.append({'label':'inherited_rows_and_additions','passed':True,'inherited':396,'added':27,'added_paths':[e['path'] for e in added],'excluded_paths_not_opened':sorted(EXCLUDED)})
ids=readmeta(Q/'SOURCE_IDENTITIES.json'); oldids=readmeta(OLD/'SOURCE_IDENTITIES.json')
require({k:v for k,v in ids.items() if k not in ('dependency_manifest','repair_ancestry')}=={k:v for k,v in oldids.items() if k!='dependency_manifest'},'subject semantics changed')
require(len(ids['subjects']['native']['ordered_cases'])==77 and len(ids['subjects']['audit']['ordered_cases'])==62,'case counts')
checks.append({'label':'subject_protocol_unchanged','passed':True,'native':77,'audit':62})
refcounts={}

def refs(x):
    if isinstance(x,dict):
        if set(('path','bytes','sha256')) <= set(x): yield x
        for v in x.values(): yield from refs(v)
    elif isinstance(x,list):
        for v in x: yield from refs(v)

for e in added:
    if e['access_policy']=='metadata-identities-only-no-scientific-body-decoding':
        v=readmeta(e['path'],e['identity']); count=0
        for i in refs(v):
            require(i['path'] in by,'new administrative reference outside selected closure '+i['path'])
            pin=by[i['path']]['identity']
            require(all(pin[k]==i[k] for k in ('path','bytes','sha256')),'new reference mismatch')
            for k in ('resolved_path','symlinks'):
                if k in i: require(i[k]==pin[k], 'full identity mismatch')
            count+=1
        refcounts[e['path']]=count
for i in refs(ids):
    pin=ids['dependency_manifest'] if i['path']==str(Q/'SOURCE_DEPENDENCIES.json') else by[i['path']]['identity']
    require(all(pin[k]==i[k] for k in ('path','bytes','sha256')),'subject reference mismatch')
checks.append({'label':'new_metadata_full_reference_traversal','passed':True,'body_counts':refcounts,'occurrences':sum(refcounts.values()),'subject_occurrences':len(list(refs(ids)))})
c=readmeta(Q/'SOURCE_CORRESPONDENCE.json')
unchanged=[]; ranges=[]
for m in c['modules']:
    prev=opaque(m['old']['path'],m['old'],True); now=opaque(m['current']['path'],m['current'],True)
    p=prev.splitlines(keepends=True); n=now.splitlines(keepends=True)
    require(len(p)==m['old_lines'] and len(n)==m['current_lines'],'line count')
    require((prev==now)==m['whole_file_identical'],'whole match claim')
    for r in m['unchanged_definitions']:
        a=b''.join(p[r['old_start']-1:r['old_end']]); b=b''.join(n[r['current_start']-1:r['current_end']])
        require(a==b and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'unchanged slice '+r['name'])
        unchanged.append({'module':m['name'],'name':r['name'],'old':[r['old_start'],r['old_end']],'current':[r['current_start'],r['current_end']]})
    for r in m['changed_definitions']:
        for side,lines in [('old',p),('current',n)]:
            z=r[side]; b=b''.join(lines[z['start']-1:z['end']]); require(len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'],'changed slice')
    for key,lines in [('added_definitions',n),('removed_definitions',p)]:
        for r in m[key]:
            b=b''.join(lines[r['start']-1:r['end']]); require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'added/removed slice')
require(len(unchanged)==96,'96 count')
checks.append({'label':'all_literal_correspondence_slices','passed':True,'unchanged_count':96,'overlapping_not_disjoint':True,'unchanged':unchanged})

def reconstruct(delta):
    ls=opaque(Q/delta,None,True).decode().splitlines(keepends=True); at=0; outcomes=[]
    while at<len(ls):
        require(ls[at].startswith('--- RI138/'),'old diff header')
        name=ls[at].strip().split('/',1)[1]; at+=1
        require(ls[at]=='+++ RI140/'+name+'\n','new diff header'); at+=1
        src=opaque(OLD/name,None,True).decode().splitlines(keepends=True); result=[]; cursor=0; hn=0
        while at<len(ls) and not ls[at].startswith('--- RI138/'):
            match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',ls[at]); require(match,'hunk header')
            oldstart,oldcount,newstart,newcount=match.groups(); oldstart=int(oldstart); oldcount=int(oldcount or 1); newcount=int(newcount or 1)
            result.extend(src[cursor:oldstart-1]); cursor=oldstart-1; at+=1; oc=nc=0
            while at<len(ls) and not ls[at].startswith(('@@ ','--- RI138/')):
                line=ls[at]; at+=1; kind=line[0]; body=line[1:]
                if kind in ' -': require(cursor<len(src) and src[cursor]==body,'diff context'); cursor+=1; oc+=1
                if kind in ' +': result.append(body); nc+=1
                require(kind in ' +-','diff line type')
            require((oc,nc)==(oldcount,newcount),'hunk counts'); hn+=1
        result.extend(src[cursor:]); found=''.join(result).encode(); expected=opaque(Q/name,None,True)
        require(found==expected,'complete reconstructed bytes '+name); outcomes.append({'name':name,'hunks':hn,'bytes':len(found)})
    return outcomes
for delta in ['SOURCE_CODE.diff','METADATA_CONTRACT.diff']:
    checkpoint('complete_diff:'+delta, lambda delta=delta:reconstruct(delta))
require(opaque(OLD/'custody.py',None,True)==opaque(Q/'custody.py',None,True),'unchanged custody')
author=readmeta(Q/'AUTHOR_STATIC_CHECKS.json')
for pin in author['payloads_observed_before_this_report']: opaque(pin['path'],pin)
# Never recursively open body references in opaque ancestry, runtime or scientific files.
report={'schema':'ri140-independent-opaque-source-check-v1','status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'dependency_count':len(by),'dependency_bytes':sum(e['identity']['bytes'] for e in by.values()),'subject_source_executed':False,'current_runtime_observed':False,'scientific_body_decoded':False,'four_excluded_bodies_opened':False,'all_current_metadata_loaded_completely':True,'observation_count_including_repeated_pins':len(observations),'observation_list_sha256':hashlib.sha256(json.dumps(observations,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
raw=(json.dumps(report,indent=2,sort_keys=True)+'\n').encode()
with (OUT/'OPAQUE_TEXT_CHECK.json').open('xb') as f: f.write(raw)
print(json.dumps({'status':report['status'],'dependencies':len(by),'dependency_bytes':report['dependency_bytes'],'checks':len(checks),'errors':errors,'report_bytes':len(raw),'report_sha256':hashlib.sha256(raw).hexdigest()}))
raise SystemExit(1 if errors else 0)
