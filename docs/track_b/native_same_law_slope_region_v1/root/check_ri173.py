"""Root independent finite provenance check; no science/formula execution."""
import hashlib,importlib.util
from pathlib import Path
D=Path(__file__).parent;B=D.parent
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
S=B/'ri173-same-law-endpoint-slope-ckec5j02';old=B/'ri172-full-layer-implication-6n1jflgq';review=B/'ri172-independent-proof-review-shli6tby'
m.verify(S/'HANDOFF.json',dict(bytes=5840,sha256='8eae3401a62721a0e9d569e6b9ec10e0bb6961e7522a839693e1da7bf6dfa504'))
h=m.load(S/'HANDOFF.json');assert sorted(p.name for p in S.iterdir())==sorted(h['namespace'])==sorted(['HANDOFF.json']+[Path(r['path']).name for r in h['payloads']]) and len(h['payloads'])==7
identities=[m.identity(S/'HANDOFF.json')]+[m.verify(r['path'],r) for r in h['payloads']]
d=m.load(S/'SOURCE_DEPENDENCIES.json');s=m.load(S/'SOURCE_IDENTITIES.json');by={r['path']:r for r in d['protected_files']}
assert len(by)==300 and list(by)==sorted(by)
for i,r in enumerate(by.values(),1):
 assert r['role']=='dep_'+str(i).zfill(4) and r['path']==r['identity']['path'];identities.append(m.verify(r['path'],r['identity']))
assert sum(r['identity']['bytes'] for r in by.values())==18387887
omit=lambda r:{k:v for k,v in r.items() if k!='role'}
previous=m.load(old/'SOURCE_DEPENDENCIES.json');assert len(previous['protected_files'])==276
for r in previous['protected_files']:assert omit(r)==omit(by[r['path']])
for key in ('governance_stopping_boundary','historical_phase_record_boundary','predecessor_author_support_boundary'):assert d[key]==previous[key]
for directory,count in ((old,8),(review,10)):
 seal=m.load(directory/'HANDOFF.json');assert sorted(p.name for p in directory.iterdir())==sorted(seal['namespace']) and len(seal['namespace'])==count
 for r in seal['payloads']:m.verify(r['path'],r)
refs=states=0
def scan(x,current=False):
 global refs,states
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and type(x.get('bytes')) is int and isinstance(x.get('sha256'),str):
   assert x['path'] in by or (current and x['path']==str(S/'SOURCE_DEPENDENCIES.json'))
   m.verify(x['path'],x);refs+=1;states+=int('state' in x)
  for value in x.values():scan(value,current)
 elif isinstance(x,list):
  for value in x:scan(value,current)
classes={}
for r in by.values():
 cl=r['classification'];classes[cl]=classes.get(cl,0)+1
 if cl=='selected-administrative-proof-provenance':scan(m.load(r['path']))
assert refs==3175 and states==17
historical_refs=refs;refs=states=0;scan(s,True);assert refs==142
assert classes=={'analytic-source-text-or-review':107,'opaque-historical-acceptance-or-source-support':85,'opaque-scientific-historical-premise':1,'selected-administrative-proof-provenance':106,'selected-administrative-governance-boundary':1}
for key,row in s['source_text_counterparts']['published'].items():assert Path(row['path']).read_bytes()==Path(s['premise_texts'][key]['path']).read_bytes()
assert len(s['source_text_counterparts']['published'])==4
for r in identities:assert m.identity(r['path'])==r
assert len(identities)==308 and sorted(p.name for p in S.iterdir())==sorted(h['namespace'])
print(m.save('RI173_ROOT_METADATA_CHECK.json',dict(status='PASS_FINITE_PROVENANCE_ONLY',identities=identities,selected_dependencies=300,selected_dependency_bytes=18387887,inherited_rows=276,historical_typed_references=historical_refs,current_typed_references=refs,historical_extended_state_noncomparisons=17,current_whole_state_rechecks=308,scientific_body_decode=False,scientific_formula_execution=False,author_final_reported_receipt='de8338')))
