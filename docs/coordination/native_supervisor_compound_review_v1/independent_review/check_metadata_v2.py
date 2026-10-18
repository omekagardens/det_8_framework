"""RI180 metadata and literal-source checks only; no subject imports or evaluations."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import os
import re
import stat

D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri180-supervisor-independent-review-4xwmvctt')
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo')
OLD=Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-supervisor-qualification-source-zksymhs1')
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-independent-supervisor-source-review-fw3b83xu')
A=Path('/Volumes/AI_DATA/development/det-review-evidence/ri179-root-upper-review-lf_39rs0/RI180_REVIEW_ASSIGNMENT.json')
checks=[];seen={}
def need(label,condition):
    if condition is not True:raise ValueError(label)
    checks.append(label)
def state(st):return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
def identity(p):
    p=Path(p);before=p.lstat()
    need('absolute regular nonsymlink '+str(p),p.is_absolute() and stat.S_ISREG(before.st_mode) and not any(x.is_symlink() for x in [p,*p.parents]))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();size=0
    try:
        need('opened same file '+str(p),state(os.fstat(fd))==state(before))
        while True:
            b=os.read(fd,1048576)
            if not b:break
            size+=len(b);h.update(b)
        need('stable descriptor '+str(p),state(os.fstat(fd))==state(before))
    finally:os.close(fd)
    need('stable final pathname '+str(p),state(p.lstat())==state(before) and size==before.st_size)
    row=dict(path=str(p),bytes=size,sha256=h.hexdigest(),state=state(before))
    if str(p) in seen:need('stable repeated identity '+str(p),seen[str(p)]==row)
    seen[str(p)]=row;return row
def pure(r):return {k:r[k] for k in ['path','bytes','sha256']}
def pin(r):
    need('typed pin '+r['path'],type(r['bytes']) is int and type(r['sha256']) is str)
    need('exact pin '+r['path'],pure(identity(r['path']))=={k:r[k] for k in ['path','bytes','sha256']})
def pairs(items):
    v={}
    for k,x in items:
        need('unique administrative key '+k,k not in v);v[k]=x
    return v
def load(p):
    need('administrative name only '+str(p),Path(p).name in ALLOW)
    row=identity(p);b=Path(p).read_bytes()
    need('decoded administrative byte pin '+str(p),len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
    return json.loads(b,object_pairs_hook=pairs)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
ALLOW={'HANDOFF.json','RI180_REVIEW_ASSIGNMENT.json','DEPENDENCY_BINDINGS.json','SOURCE_PINS.json','CASE_MANIFEST.json','CASE_OBLIGATIONS.json','ADMIN_CHECK.json','FINAL_CHECK.json','AUTHENTICATION.json','FOCUSED_VARIANTS.json','WRITE_READ_VARIANTS.json'}
pin(dict(path=str(A),bytes=1542,sha256='771e2a9c09769e05118388218dda11cb60e75f5a5c564c7022824ed7759a5568'))
pin(dict(path=str(S/'HANDOFF.json'),bytes=14679,sha256='572fe0bfc79489dc3b9c4a6df9bc4d7bbb0ff455de1c68eb2fbb00e6d870421e'))
a=load(A);h=load(S/'HANDOFF.json')
need('exact33 namespace',sorted(p.name for p in S.iterdir())==h['namespace'] and len(h['namespace'])==33)
need('32 unique complete payloads',len(h['payloads'])==32 and {Path(v['path']).name for v in h['payloads']}==set(h['namespace'])-{'HANDOFF.json'})
for row in h['payloads']:
    need('current payload path parent',Path(row['path']).parent==S);pin(row)
deps=load(S/'DEPENDENCY_BINDINGS.json');au=load(S/'ADMIN_CHECK.json');roles=load(S/'SOURCE_PINS.json')['roles'];manifest=load(S/'CASE_MANIFEST.json');ob=load(S/'CASE_OBLIGATIONS.json');final=load(S/'FINAL_CHECK.json')
need('64 unique original rows',len(deps['fresh_originals'])==len({v['path'] for v in deps['fresh_originals']})==64)
for row in deps['fresh_originals']:pin(row)
for directory in [OLD,R]:
    old=load(directory/'HANDOFF.json')
    need('exact predecessor namespace '+str(directory),sorted(p.name for p in directory.iterdir())==sorted(old['namespace']))
    for row in old['payloads']:pin(row)
need('complete source role equality',canon(roles)==canon(h['source_roles'])==canon(au['source_roles']))
for row in roles.values():pin(row)
need('complete external author result equality',canon(deps['fresh_originals'])==canon(au['fresh_external_identities']))
need('all266 administrative author records true',len(au['checks'])==au['checks_count']==266 and all(v['passed'] is True for v in au['checks']))
need('71 final declared references',len(final['identities'])==final['checked_references']==71)
for row in final['identities']:pin(row)
texts={n:(S/n).read_text() for n in ['protocol.py','qualify_supervisor.py','case_worker.py','inert_payload.py','check_saved.py','CASE_MANIFEST.json']}
oldtexts={n:(OLD/n).read_text() for n in texts}
for n in ['qualify_supervisor.py','CASE_MANIFEST.json']:need('unchanged complete '+n,texts[n]==oldtexts[n])
need('only protocol directory relocation',texts['protocol.py']==oldtexts['protocol.py'].replace("SOURCE_DIRECTORY = BASE + '/ri171-supervisor-qualification-source-zksymhs1'","SOURCE_DIRECTORY = BASE + '/ri176-supervisor-qualification-repair-3ausb2jo'"))
need('92 unique unexecuted',len(manifest['cases'])==len({c['id'] for c in manifest['cases']})==92 and all(c['executed'] is False for c in manifest['cases']))
need('13 groups',len({c['group'] for c in manifest['cases']})==13)
need('69/16/7 entry split',dict(collections.Counter(c['kind'] for c in manifest['cases']))=={'whole':69,'observer':16,'direct':7})
need('34 retained full recipe objects',sum('inherited_recipe' in c for c in manifest['cases'])==34)
need('92 ordered obligations',len(ob['rows'])==92 and [x['id'] for x in ob['rows']]==[x['id'] for x in manifest['cases']])
for row,case in zip(ob['rows'],manifest['cases']):
    need('closed obligation '+row['id'],set(row)=={'id','kind','fault','terminal','input_tag','healthy','subject_reap'})
    need('case obligation association '+row['id'],row['kind']==case['kind'] and row['fault']==case['fault'])
    body={k:v for k,v in row.items() if k!='id'}
    literal='    '+json.dumps(row['id'])+': '+json.dumps(body,separators=(',',':'))+','
    need('literal unexecuted policy '+row['id'],texts['check_saved.py'].count(literal)==1)
# Plain line-delimited text comparison, not tokenization, AST or Python evaluation.
def spans(t):
    lines=t.splitlines(keepends=True);starts=[i for i,l in enumerate(lines) if re.match(r'^(?:    )?def [A-Za-z_]',l)]
    return [(lines[v].strip(),''.join(lines[v:starts[i+1] if i+1<len(starts) else len(lines)])) for i,v in enumerate(starts)]
computed=[]
for n in texts:
    if not n.endswith('.py'):continue
    before=spans(oldtexts[n]);after=spans(texts[n])
    for heading,t in before:
        match=next((z for title,z in after if title==heading),None)
        if t==match:computed.append(dict(file=n,heading=heading,bytes=len(t.encode()),sha256=hashlib.sha256(t.encode()).hexdigest()))
need('all47 exact unchanged text spans',len(computed)==47 and canon(computed)==canon(au['unchanged_function_text_spans']))
# Apply declared unified hunks as literal text; no source execution/tokenization.
patch=(S/'SOURCE_DIFF.patch').read_text().splitlines(keepends=True)
pos=0;changed=[]
while pos<len(patch):
    need('old diff header',patch[pos].startswith('--- '))
    oldpath=patch[pos][4:].split('\t')[0].rstrip('\n');pos+=1
    need('new diff header',patch[pos].startswith('+++ '))
    newpath=patch[pos][4:].split('\t')[0].rstrip('\n');pos+=1
    name=Path(oldpath).name
    need('exact diff paths',name in texts and oldpath==str(OLD/name) and newpath==str(S/name) and name not in changed)
    changed.append(name);oldlines=oldtexts[name].splitlines(keepends=True);newlines=[];consumed=0
    while pos<len(patch) and patch[pos].startswith('@@ '):
        match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',patch[pos])
        need('literal hunk header',match is not None)
        old_start=int(match[1]);old_count=int(match[2] or '1');new_start=int(match[3]);new_count=int(match[4] or '1')
        at=old_start-1 if old_count else old_start
        need('ordered diff old span',at>=consumed)
        newlines+=oldlines[consumed:at];consumed=at
        need('new hunk position',(new_start-1 if new_count else new_start)==len(newlines))
        pos+=1;oc=0;nc=0
        while pos<len(patch) and not patch[pos].startswith(('@@ ','--- ')):
            line=patch[pos];prefix=line[0];need('literal hunk operation',prefix in ' +-')
            if prefix in ' -':
                need('exact consumed old line',consumed<len(oldlines) and oldlines[consumed]==line[1:]);consumed+=1;oc+=1
            if prefix in ' +':newlines.append(line[1:]);nc+=1
            pos+=1
        need('exact hunk lengths',oc==old_count and nc==new_count)
    newlines+=oldlines[consumed:]
    need('complete reconstructed successor '+name,''.join(newlines)==texts[name])
need('complete all changed files in delta',set(changed)=={n for n in texts if texts[n]!=oldtexts[n]})
plan=(S/'ORACLE_REJECTION_PLAN.md').read_text()
ids=re.findall(r'^\| (O\d{2}) \|',plan,re.M)
need('exact26 prospective mutation families',ids==['O'+str(i).zfill(2) for i in range(1,27)])
need('five source line inventories',{n:texts[n].count('\n') for n in texts if n.endswith('.py')}==h['source_lines'])
need('325 inherited provenance only',deps['inherited_closure']['reference_count']==325 and deps['inherited_closure']['recursively_reobserved'] is False)
for row in list(seen.values()):need('final stable reread '+row['path'],identity(row['path'])==row)
result=dict(schema='ri180-independent-administrative-source-check-v1',status='EXACT_SOURCE_METADATA_MATCH_NOT_QUALIFICATION',check_count=len(checks),checks=checks,observed_identities=list(seen.values()),observed_count=len(seen),subject_namespace=h['namespace'],cases=92,recipes=34,mutation_families=26,unchanged_text_spans=computed,executed_cases=0,subject_import_compile_AST_probe=False,subject_helper_vendor_executed=False,scientific_decode=False,current_runtime_observed=False,historical325_recursively_observed=False)
b=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
with (D/'ADMIN_CHECK.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],checks=len(checks),identities=len(seen),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),executed_cases=0),sort_keys=True))
