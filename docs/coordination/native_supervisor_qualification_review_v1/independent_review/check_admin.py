"""Read-only RI171 source/metadata checker; never loads subject or control modules."""
import collections
import hashlib
import json
import os
from pathlib import Path
import stat

OUT=Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-independent-supervisor-source-review-fw3b83xu')
SUB=Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-supervisor-qualification-source-zksymhs1')
OLD=Path('/Volumes/AI_DATA/development/det-review-evidence/ri169-write-would-block-repair-7_868hay')
ASSIGN=Path('/Volumes/AI_DATA/development/det-review-evidence/ri174-root-preparation-review-wm18ymsq/RI171_INDEPENDENT_REVIEW_ASSIGNMENT.json')
seen={}; checks=[]
def need(label,test):
    if not test:raise ValueError(label)
    checks.append(label)
def signature(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(p):
    p=Path(p)
    need('absolute '+str(p),p.is_absolute())
    need('no path symlink '+str(p),not any(a.is_symlink() for a in [p,*p.parents]))
    first=p.lstat();need('regular '+str(p),stat.S_ISREG(first.st_mode))
    h=hashlib.sha256();n=0
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        need('opened identity '+str(p),signature(os.fstat(fd))==signature(first))
        while True:
            block=os.read(fd,1048576)
            if not block:break
            h.update(block);n+=len(block)
        need('stable descriptor '+str(p),signature(os.fstat(fd))==signature(first))
    finally:os.close(fd)
    need('stable path '+str(p),signature(p.lstat())==signature(first) and n==first.st_size)
    row={'path':str(p),'bytes':n,'sha256':h.hexdigest(),'fresh_state':signature(first)}
    if str(p) in seen:need('repeat identity '+str(p),row==seen[str(p)])
    seen[str(p)]=row
    return row
def pin(row):
    got=identity(row['path'])
    need('typed pin '+row['path'],type(row['bytes']) is int and type(row['sha256']) is str)
    need('whole exact pin '+row['path'],all(got[k]==row[k] for k in ('path','bytes','sha256')))
    return got
def pure(row):return {k:row[k] for k in ('path','bytes','sha256')}
def administrative(p):
    need('fixed administrative allowlist '+str(p),str(p) in ALLOW)
    raw=Path(p).read_bytes();got=identity(p)
    need('complete admin bytes '+str(p),len(raw)==got['bytes'] and hashlib.sha256(raw).hexdigest()==got['sha256'])
    def pairs(items):
        out={}
        for k,v in items:
            need('unique admin key '+k,k not in out);out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs)
def same(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)
ALLOW={str(ASSIGN)}|{str(SUB/n) for n in ('HANDOFF.json','DEPENDENCY_BINDINGS.json','SOURCE_PINS.json','CASE_MANIFEST.json','COVERAGE.json','AUTHOR_METADATA_CHECK.json','AUTHENTICATION.json')}|{str(OLD/n) for n in ('HANDOFF.json','FOCUSED_VARIANTS.json','WRITE_READ_VARIANTS.json','DEPENDENCY_BINDINGS.json')}
pin(dict(path=str(ASSIGN),bytes=1613,sha256='2c7073f137f40628b19faad42cfff085b6b8d3e1ce44c1e8dbca3fd13e274a0d'))
pin(dict(path=str(SUB/'HANDOFF.json'),bytes=14569,sha256='b83a4588d780d552cbf665263a599e514e8c6944d41d3237bce1bd1180b01078'))
a=administrative(ASSIGN);h=administrative(SUB/'HANDOFF.json')
need('exact30 namespace',sorted(p.name for p in SUB.iterdir())==sorted(h['namespace']) and len(h['namespace'])==30)
need('29 payload coverage',len(h['payloads'])==29 and {Path(v['path']).name for v in h['payloads']}==set(h['namespace'])-{'HANDOFF.json'})
for v in h['payloads']:
    need('fixed payload parent',Path(v['path']).parent==SUB);pin(v)
d=administrative(SUB/'DEPENDENCY_BINDINGS.json');p=administrative(SUB/'SOURCE_PINS.json');m=administrative(SUB/'CASE_MANIFEST.json');c=administrative(SUB/'COVERAGE.json');au=administrative(SUB/'AUTHOR_METADATA_CHECK.json');auth=administrative(SUB/'AUTHENTICATION.json')
need('24 unique originals',len(d['fresh_originals'])==len({v['path'] for v in d['fresh_originals']})==24)
for v in d['fresh_originals']:pin(v)
need('four authoritative role maps exact',same(h['source_roles'],p['roles']) and same(p['roles'],d['own_executable_and_manifest_roles']))
for k,v in p['roles'].items():pin(v)
need('manifest fixed subject',same(m['subject'],p['roles']['subject']) and same(c['bound_subject'],m['subject']))
oh=administrative(OLD/'HANDOFF.json')
need('exact predecessor namespace',sorted(v.name for v in OLD.iterdir())==sorted(oh['namespace']))
for v in oh['payloads']:pin(v)
f=administrative(OLD/'FOCUSED_VARIANTS.json');w=administrative(OLD/'WRITE_READ_VARIANTS.json');hist=administrative(OLD/'DEPENDENCY_BINDINGS.json')
need('historical325 declared only',d['inherited_reference_count']==hist['inherited_RI165_reference_entries']==325)
need('exact inherited dependency record pin',same(d['inherited_external_closure'],pure(seen[str(OLD/'DEPENDENCY_BINDINGS.json')])) )
need('same34 recipe objects in original order',same([v['inherited_recipe'] for v in m['cases'] if 'inherited_recipe' in v],f['variants']+w['variants']))
need('literal92 unique unexecuted cases',len(m['cases'])==len({v['id'] for v in m['cases']})==92 and all(v['executed'] is False for v in m['cases']))
need('58base34inherited',sum('inherited_recipe' not in v for v in m['cases'])==58 and len(f['variants'])==28 and len(w['variants'])==6)
groups=['S'+str(i).zfill(2) for i in range(1,14)]
need('exact13 groups',m['groups']==groups and sorted({v['group'] for v in m['cases']})==groups)
counts=dict(collections.Counter(v['kind'] for v in m['cases']))
need('entry69/16/7',counts=={'whole':69,'observer':16,'direct':7} and c['entry_counts']==counts)
for group in c['groups']:
    need('whole ordered group '+group['group'],group['cases']==[v['id'] for v in m['cases'] if v['group']==group['group']] and group['actual_outcomes']==0)
need('real clock inventory',m['real_clock_cases']==['S09.real_cutoffs','S09.real_expiry'])
line_counts={}
for role in ('protocol','driver','worker','payload','checker','subject'):
    v=p['roles'][role];raw=Path(v['path']).read_bytes();pin(v)
    line_counts[role]=raw.count(b'\n')
    need('literal source line inventory '+role,line_counts[role]==au['source_stats'][role]['lines'])
    need('author source identity '+role,all(au['source_stats'][role][k]==v[k] for k in ('path','bytes','sha256')))
need('five1310 subject588',sum(line_counts[k] for k in line_counts if k!='subject')==1310 and line_counts['subject']==588)
for v in list(seen.values()):need('final read window '+v['path'],identity(v['path'])==v)
result=dict(schema='ri171-independent-administrative-review-v1',status='IDENTITIES_AND_LITERAL_INVENTORIES_MATCH_NOT_QUALIFICATION',subject_namespace=h['namespace'],payloads=29,originals=24,observed_identity_count=len(seen),observed_identities=list(seen.values()),case_count=92,groups=13,base_cases=58,inherited_recipes=34,entry_counts=counts,source_line_counts=line_counts,checks=checks,check_count=len(checks),historical325_reference_entries_freshly_walked=False,current_runtime_or_supplier_observed=False,subject_control_helper_vendor_executed=False,subject_import_compile_AST_probe=False,scientific_body_decoded=False,fixtures_created=False,actual_control_outcomes=0)
b=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
with (OUT/'ADMIN_CHECK.json').open('xb') as fd:fd.write(b);fd.flush();os.fsync(fd.fileno())
print(json.dumps({'status':result['status'],'checks':len(checks),'identities':len(seen),'cases':92,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},sort_keys=True))
