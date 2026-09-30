"""Root opaque identity and bounded administrative-reference check only."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
Q=m.B/'ri151-canonical-q-equalities-_546ie2h';P=m.B/'ri149-singleton-hook-incidence-yfjac93v'
H=m.load(Q/'HANDOFF.json');before=m.load(m.D/'AUTHOR_SEAL_CHECK.json')
assert m.identity(Q/'HANDOFF.json')==before['handoff']
assert [m.identity(r['path']) for r in before['files']]==before['files']
assert sorted(p.name for p in Q.iterdir())==sorted(H['namespace'])
D=m.load(Q/'SOURCE_DEPENDENCIES.json');rows=D['protected_files'];assert len(rows)==150
M={r['path']:r for r in rows};assert len(M)==150
fresh=[]
for i,r in enumerate(rows,1):
 assert r['role']=='dep_'+str(i).zfill(4) and r['path']==r['identity']['path']
 z=m.verify(r['path'],r['identity']);assert z['resolved_path']==r['identity']['resolved_path'] and z['symlink_chain']==r['identity']['symlinks'];fresh.append(z)
assert list(M)==sorted(M)
old=m.load(P/'SOURCE_DEPENDENCIES.json')['protected_files'];assert len(old)==129
for r in old:assert {k:v for k,v in r.items() if k!='role'}=={k:v for k,v in M[r['path']].items() if k!='role'}
def walk(v):
 refs=[]
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and type(v.get('bytes')) is int and isinstance(v.get('sha256'),str):
   assert v['path'] in M or v['path']==str(Q/'SOURCE_DEPENDENCIES.json');m.verify(v['path'],v);refs.append(v)
  for x in v.values():refs+=walk(x)
 elif isinstance(v,list):
  for x in v:refs+=walk(x)
 return refs
admin=[r for r in rows if r['classification']=='selected-administrative-proof-provenance'];assert len(admin)==45
refs=[x for r in admin for x in walk(m.load(r['path']))];assert len(refs)==734
S=m.load(Q/'SOURCE_IDENTITIES.json');current=walk(S);assert len(current)==66
pairs=[]
for k,r in S['source_text_counterparts']['published'].items():
 p=S['premise_texts'][k];assert Path(r['path']).read_bytes()==Path(p['path']).read_bytes();pairs.append([p,r])
assert len(pairs)==4
for row in fresh:assert m.identity(row['path'])==row
print(m.save('ROOT_NATIVE_CHECK.json',dict(schema='ri151-root-analytic-custody-check-v1',status='MATCH_NOT_MATHEMATICAL_ACCEPTANCE',author_seal=m.ref(Q/'HANDOFF.json'),dependencies=150,dependency_bytes=sum(r['bytes'] for r in fresh),identities=fresh,inherited_rows_preserved=129,administrative_bodies=45,historical_typed_refs=734,current_typed_refs=66,literal_counterparts=pairs,actual_coefficients_or_scientific_bodies_decoded=False,subject_execution=False)))
