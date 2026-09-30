"""Independent bounded RI172 identity check; no subject import or scientific decode."""
import collections
import hashlib
import json
import os
from pathlib import Path
import stat

OUT = Path('/Volumes/AI_DATA/development/det-review-evidence/ri172-independent-proof-review-shli6tby')
SUB = Path('/Volumes/AI_DATA/development/det-review-evidence/ri172-full-layer-implication-6n1jflgq')
PRE = Path('/Volumes/AI_DATA/development/det-review-evidence/ri168-terminal-row-coupling-f50p8xyj')
ASSIGN = Path('/Volumes/AI_DATA/development/det-review-evidence/ri172-root-review-fkjv3v0z/INDEPENDENT_REVIEW_ASSIGNMENT.json')
checked = 0
observed = {}

def demand(condition, label):
    global checked
    checked += 1
    if not condition:
        raise ValueError(label)

def state(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def opaque(path):
    p = Path(path)
    demand(p.is_absolute(), 'absolute identity path')
    for part in [*reversed(p.parents), p]:
        demand(not part.is_symlink(), 'unexpected symlink: '+str(part))
    before = p.lstat()
    demand(stat.S_ISREG(before.st_mode), 'regular file: '+str(p))
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        demand(state(before)==state(os.fstat(fd)), 'open state: '+str(p))
        h = hashlib.sha256(); count = 0
        while True:
            data = os.read(fd, 1048576)
            if not data:
                break
            count += len(data); h.update(data)
        demand(state(before)==state(os.fstat(fd)), 'read state: '+str(p))
    finally:
        os.close(fd)
    demand(state(before)==state(p.lstat()), 'path state: '+str(p))
    demand(count==before.st_size, 'size consistency: '+str(p))
    row = dict(path=str(p),resolved_path=str(p.resolve(strict=True)),bytes=count,
               sha256=h.hexdigest(),symlinks=[],fresh_read_state=state(before))
    old = observed.get(str(p))
    if old is not None:
        demand(row==old, 'repeated read consistency: '+str(p))
    observed[str(p)] = row
    return row

def pure(r):
    return dict(bytes=r['bytes'], sha256=r['sha256'])

def pin(path, expected):
    got = opaque(path)
    demand(type(expected['bytes']) is int and type(expected['sha256']) is str, 'typed pin')
    demand(pure(got)==pure(expected), 'whole bytes/pin: '+str(path))
    for key in ('path','resolved_path'):
        if key in expected:
            demand(got[key]==expected[key], 'literal '+key+': '+str(path))
    for key in ('symlinks','symlink_chain'):
        if key in expected:
            demand(expected[key]==[], 'empty declared links: '+str(path))
    return got

def admin(path):
    # Called only for this exact finite allowlist of administrative documents.
    demand(str(path) in ADMIN, 'administrative allowlist')
    raw = Path(path).read_bytes()
    demand(pure(opaque(path))==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()), 'admin read pin')
    def pairs(items):
        result={}
        for k,v in items:
            demand(k not in result, 'duplicate administrative key')
            result[k]=v
        return result
    return json.loads(raw, object_pairs_hook=pairs)

ADMIN={str(p) for p in (ASSIGN,SUB/'HANDOFF.json',SUB/'SOURCE_DEPENDENCIES.json',SUB/'SOURCE_IDENTITIES.json',PRE/'HANDOFF.json',PRE/'SOURCE_DEPENDENCIES.json')}
pin(ASSIGN,dict(bytes=1787,sha256='3f0d98bbd556a1be64e2a0533dcbecf9248ebed689f623da7d07f62b051ffbd1'))
pin(SUB/'HANDOFF.json',dict(bytes=6736,sha256='552d173833a735c2778c02a3c561e0a9c4c204cb214f4f5db3e3e8910479079d'))
a=admin(ASSIGN); h=admin(SUB/'HANDOFF.json')
demand(sorted(p.name for p in SUB.iterdir())==sorted(h['namespace']), 'exact subject namespace')
demand(len(h['namespace'])==8 and len(set(h['namespace']))==8 and len(h['payloads'])==7, 'subject 8/7')
demand({Path(r['path']).name for r in h['payloads']}==set(h['namespace'])-{'HANDOFF.json'}, 'payload coverage')
for row in h['payloads']:
    demand(Path(row['path']).parent==SUB, 'payload parent')
    pin(row['path'],row)
d=admin(SUB/'SOURCE_DEPENDENCIES.json'); s=admin(SUB/'SOURCE_IDENTITIES.json')
rows=d['protected_files']; demand(len(rows)==276, '276 dependencies')
by={r['path']:r for r in rows}; demand(len(by)==276, 'unique dependencies')
for row in rows:
    demand(row['path']==row['identity']['path'],'declared literal path')
    pin(row['path'],row['identity'])
ph=admin(PRE/'HANDOFF.json'); pd=admin(PRE/'SOURCE_DEPENDENCIES.json')
demand(sorted(p.name for p in PRE.iterdir())==sorted(ph['namespace']), 'exact predecessor namespace')
demand(len(pd['protected_files'])==264, '264 inherited rows')
for old in pd['protected_files']:
    newer=by[old['path']]
    demand({k:v for k,v in old.items() if k!='role'}=={k:v for k,v in newer.items() if k!='role'}, 'inherited row preserved '+old['path'])
new_paths=set(by)-{r['path'] for r in pd['protected_files']}
expected_new={str(PRE/n) for n in ph['namespace']}|{
 '/Volumes/AI_DATA/development/det-review-evidence/ri168-root-coupling-review-jihb5l4y/'+n for n in
 ('RI172_NATIVE_ASSIGNMENT.json','RI168_ROOT_ADJUDICATION.json','RI168_ROOT_PROOF_REVIEW.md','RI168_ROOT_METADATA_CHECK.json')}
demand(new_paths==expected_new, 'exact eight predecessor plus four root additions')
refs=[]
def traverse(obj, location):
    if isinstance(obj,dict):
        if {'path','bytes','sha256'}<=obj.keys():
            refs.append(dict(location=location,path=obj['path'],bytes=obj['bytes'],sha256=obj['sha256']))
            demand(obj['path'] in by, 'current source reference selected: '+location)
            pin(obj['path'],obj)
        for k,v in obj.items(): traverse(v,location+'/'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): traverse(v,location+'/'+str(i))
traverse(s,'SOURCE_IDENTITIES')
demand(len(refs)==123,'123 typed current source references')
pairs=[]
for key,pub in s['source_text_counterparts']['published'].items():
    ext=s['premise_texts'][key]
    demand(ext['path']!=pub['path'],'distinct counterpart paths')
    demand(pure(ext)==pure(pub),'equal whole source text counterpart '+key)
    pairs.append(dict(role=key,external=ext,published=pub))
demand(len(pairs)==4,'four source text counterparts')
for name in ('governance_stopping_boundary','historical_phase_record_boundary','predecessor_author_support_boundary'):
    boundary=d[name]
    demand(boundary['path'] in by and boundary['typed_reference_expansion'] is False, 'opaque boundary '+name)
demand(s['scope']['actual_fixed_vector_unchanged'] is True,'actual vector preserved')
# No historical JSON references are traversed. Their complete pinned bytes remain opaque.
for path,old in list(observed.items()):
    demand(opaque(path)==old,'final independent identity pass '+path)
result=dict(schema='ri172-independent-bounded-metadata-review-v1',status='PASS_BOUNDED_ADMINISTRATIVE_CHECKS_ONLY',
    predicate_count=checked,subject_namespace=h['namespace'],subject_payload_count=7,
    dependency_count=276,inherited_row_count=264,new_dependency_count=12,
    dependency_bytes=sum(r['identity']['bytes'] for r in rows),
    classifications=dict(collections.Counter(r['classification'] for r in rows)),
    current_typed_reference_count=len(refs),current_typed_references=refs,
    counterpart_pairs=pairs,observed_identity_count=len(observed),observed_identities=list(observed.values()),
    historical_administrative_reference_traversal_rerun=False,
    historical_extended_state_compared_to_current=False,
    scientific_body_decoded=False,subject_or_helper_imported_or_executed=False,
    mathematical_theorem_tested_by_script=False,operational_or_continuous_custody_claim=False)
body=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
with (OUT/'METADATA_CHECK.json').open('xb') as f:
    f.write(body);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],predicates=checked,identities=len(observed),dependencies=276,
    current_references=len(refs),bytes=len(body),sha256=hashlib.sha256(body).hexdigest()),sort_keys=True))
