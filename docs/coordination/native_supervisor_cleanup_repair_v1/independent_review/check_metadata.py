"""RI184 read-only whole-file and literal-source administrative reconciliation."""
from pathlib import Path
import collections,hashlib,json,os,re,stat
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri184-compound-independent-review-yju68l4m')
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri182-compound-cleanup-oracle-repair-6835ytb8')
OLD=Path('/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo')
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri180-supervisor-independent-review-4xwmvctt')
A=Path('/Volumes/AI_DATA/development/det-review-evidence/ri183-root-parent-capture-review-2mnanskj/RI184_REVIEW_ASSIGNMENT.json')
checks=[];seen={}
def need(label,condition):
    if condition is not True:raise ValueError(label)
    checks.append(label)
def state(st):return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
def identity(p):
    p=Path(p);before=p.lstat()
    need('absolute regular nonsymlink '+str(p),p.is_absolute() and stat.S_ISREG(before.st_mode) and not any(x.is_symlink() for x in [p,*p.parents]))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);digest=hashlib.sha256();size=0
    try:
        need('opened stable '+str(p),state(os.fstat(fd))==state(before))
        while True:
            b=os.read(fd,1048576)
            if not b:break
            digest.update(b);size+=len(b)
        need('descriptor stable '+str(p),state(os.fstat(fd))==state(before))
    finally:os.close(fd)
    need('path stable '+str(p),state(p.lstat())==state(before) and size==before.st_size)
    row=dict(path=str(p),bytes=size,sha256=digest.hexdigest(),state=state(before))
    if str(p) in seen:need('repeat stable '+str(p),row==seen[str(p)])
    seen[str(p)]=row;return row
def pure(r):return {k:r[k] for k in ('path','bytes','sha256')}
def pin(r):
    need('typed pin '+r['path'],type(r['bytes']) is int and type(r['sha256']) is str)
    need('exact opaque pin '+r['path'],pure(identity(r['path']))==pure(r))
def pairs(items):
    v={}
    for k,x in items:need('unique admin key '+k,k not in v);v[k]=x
    return v
def load(p):
    need('administrative basename allowlist '+str(p),Path(p).name in ALLOW)
    got=identity(p);b=Path(p).read_bytes();need('whole admin decode pin '+str(p),len(b)==got['bytes'] and hashlib.sha256(b).hexdigest()==got['sha256'])
    return json.loads(b,object_pairs_hook=pairs)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
ALLOW={'HANDOFF.json','RI184_REVIEW_ASSIGNMENT.json','DEPENDENCY_BINDINGS.json','SOURCE_PINS.json','CASE_MANIFEST.json','CASE_OBLIGATIONS.json','ADMIN_CHECK.json','FINAL_IDENTITY_CHECK.json','SOURCE_CORRESPONDENCE.json'}
pin(dict(path=str(A),bytes=1980,sha256='327cc285b708d2b290a7c5c889418854b87360a17ce87b05a2e2da559f270728'))
a=load(A);pin(a['subject']);pin(a['predecessor']);pin(a['root_decision']);h=load(S/'HANDOFF.json')
need('exact28 namespace',len(h['namespace'])==28 and sorted(p.name for p in S.iterdir())==h['namespace'])
need('exact27 payload membership',len(h['payloads'])==27 and {Path(v['path']).name for v in h['payloads']}==set(h['namespace'])-{'HANDOFF.json'})
for row in h['payloads']:need('payload parent',Path(row['path']).parent==S);pin(row)
d=load(S/'DEPENDENCY_BINDINGS.json');au=load(S/'ADMIN_CHECK.json');roles=load(S/'SOURCE_PINS.json')['roles'];c=load(S/'SOURCE_CORRESPONDENCE.json');m=load(S/'CASE_MANIFEST.json');o=load(S/'CASE_OBLIGATIONS.json');fin=load(S/'FINAL_IDENTITY_CHECK.json')
need('110 distinct external originals',len(d['fresh_originals'])==len({r['path'] for r in d['fresh_originals']})==d['fresh_unique_files']==110)
for row in d['fresh_originals']:pin(row)
for directory in [OLD,R]:
    prior=load(directory/'HANDOFF.json');need('exact predecessor namespace '+str(directory),sorted(p.name for p in directory.iterdir())==sorted(prior['namespace']))
    for row in prior['payloads']:pin(row)
need('all278 author admin checks true',len(au['checks'])==au['checks_count']==278 and all(v['passed'] is True for v in au['checks']))
need('same full110 author dependency records',canon(d['fresh_originals'])==canon(au['files']))
need('same complete7 role pins',canon(roles)==canon(h['source_roles'])==canon(au['source_roles']))
for row in roles.values():pin(row)
need('117 final references116 distinct',len(fin['files'])==fin['reference_count']==117 and len({r['path'] for r in fin['files']})==fin['unique_files']==116)
for row in fin['files']:pin(row)
names=['protocol.py','qualify_supervisor.py','case_worker.py','inert_payload.py','check_saved.py','CASE_MANIFEST.json','CASE_OBLIGATIONS.json','SCHEMAS.md']
old={n:(OLD/n).read_text() for n in names};new={n:(S/n).read_text() for n in names}
for n in names:
    if n not in ['protocol.py','check_saved.py']:need('whole unchanged copy '+n,old[n]==new[n])
need('only fixed protocol relocation',new['protocol.py']==old['protocol.py'].replace("SOURCE_DIRECTORY = BASE + '/ri176-supervisor-qualification-repair-3ausb2jo'","SOURCE_DIRECTORY = BASE + '/ri182-compound-cleanup-oracle-repair-6835ytb8'"))
need('6 whole correspondence rows',len(c['unchanged_files'])==6)
for r in c['unchanged_files']:pin(r['old']);pin(r['current']);need('correspondence same bytes',r['old']['bytes']==r['current']['bytes'] and r['old']['sha256']==r['current']['sha256'])
need('3 exact added spans',len(c['exact_added_checker_spans'])==3)
projected=new['check_saved.py']
for r in c['exact_added_checker_spans']:
    t=r['source_text'];need('span exact bytes hash',len(t.encode())==r['bytes'] and hashlib.sha256(t.encode()).hexdigest()==r['sha256'])
    need('span unique occurrence',projected.count(t)==1);projected=projected.replace(t,'',1)
need('entire checker reverse projection',projected==old['check_saved.py'])
need('definition plus exactly2 scoped calls',new['check_saved.py'].count('compound_cleanup_lifetime(')==3)
# Independently reconstruct the full successor from the declared literal patch.
patch=(S/'SOURCE_DIFF.patch').read_text().splitlines(keepends=True);pos=0;changed=[]
while pos<len(patch):
    need('old patch header',patch[pos].startswith('--- '));op=patch[pos][4:].split('\t')[0].rstrip('\n');pos+=1
    need('new patch header',patch[pos].startswith('+++ '));np=patch[pos][4:].split('\t')[0].rstrip('\n');pos+=1
    name=Path(op).name;need('exact patch pathname',name in names and op==str(OLD/name) and np==str(S/name) and name not in changed);changed.append(name)
    original=old[name].splitlines(keepends=True);out=[];used=0
    while pos<len(patch) and patch[pos].startswith('@@ '):
        match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',patch[pos]);need('hunk header',match is not None)
        os_,oc_,ns_,nc_=int(match[1]),int(match[2] or '1'),int(match[3]),int(match[4] or '1');at=os_-1 if oc_ else os_
        need('ordered old hunk',at>=used);out+=original[used:at];used=at;need('new hunk location',(ns_-1 if nc_ else ns_)==len(out));pos+=1;oc=nc=0
        while pos<len(patch) and not patch[pos].startswith(('@@ ','--- ')):
            line=patch[pos];prefix=line[0];need('hunk operation',prefix in ' +-')
            if prefix in ' -':need('exact old hunk line',used<len(original) and original[used]==line[1:]);used+=1;oc+=1
            if prefix in ' +':out.append(line[1:]);nc+=1
            pos+=1
        need('hunk lengths',oc==oc_ and nc==nc_)
    out+=original[used:];need('whole patched source '+name,''.join(out)==new[name])
need('only2 declared changed files',changed==['protocol.py','check_saved.py'])
need('92 unique unexecuted',len(m['cases'])==len({r['id'] for r in m['cases']})==92 and all(r['executed'] is False for r in m['cases']))
need('34 recipes13 groups',sum('inherited_recipe' in r for r in m['cases'])==34 and len({r['group'] for r in m['cases']})==13)
need('69whole16observer7direct',dict(collections.Counter(r['kind'] for r in m['cases']))=={'whole':69,'observer':16,'direct':7})
compound=[r['id'] for r in m['cases'] if r['fault'].endswith('.unregister_close')]
need('exact4 compound IDs',compound==['S10.caller.stdout.unregister_close','S10.caller.stderr.unregister_close','S10.ps.stdout.unregister_close','S10.ps.stderr.unregister_close'])
need('92 unchanged ordered policies',len(o['rows'])==92 and [r['id'] for r in o['rows']]==[r['id'] for r in m['cases']])
plan=(S/'ORACLE_REJECTION_PLAN.md').read_text();prior=(OLD/'ORACLE_REJECTION_PLAN.md').read_text();need('old26 exact plan prefix',plan.startswith(prior))
need('exact35 mutation families',re.findall(r'^\| (O\d{2}) \|',plan,re.M)==['O'+str(i).zfill(2) for i in range(1,36)])
need('all source line counts',{n:new[n].count('\n') for n in names if n.endswith('.py')}==h['source_lines'])
need('325 provenance remains opaque',d['inherited_closure']['reference_count']==325 and d['inherited_closure']['recursively_reobserved'] is False)
for row in list(seen.values()):need('final stable complete identity '+row['path'],identity(row['path'])==row)
v=dict(schema='ri184-independent-administrative-check-v1',status='EXACT_SOURCE_CORRESPONDENCE_NOT_RUNTIME_QUALIFICATION',checks=checks,check_count=len(checks),observed_identities=list(seen.values()),observed_count=len(seen),subject_namespace=h['namespace'],cases=92,recipes=34,groups=13,compound_cases=compound,mutation_families=35,source_reverse_projection=True,complete_patch_reconstruction=True,subject_cases_executed=0,oracle_mutations_executed=0,subject_import_compile_AST_probe_run=False,current_runtime_observed=False,historical325_recursively_observed=False)
b=(json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
with (D/'ADMIN_CHECK.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=v['status'],checks=len(checks),identities=len(seen),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),cases_executed=0),sort_keys=True))
