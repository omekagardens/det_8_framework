"""Finite identity checks and read-only saved-metadata review preparation."""
from pathlib import Path
import hashlib,importlib.util,json
D=Path(__file__).resolve().parent
H=D.parent/'ri122-root-execution-review-6whn_vky/metadata.py'
b=H.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
S=m.B/'ri166-native-contrast-gap-2j9ykuoq';R=m.B/'ri162-independent-outcome-review-s6xrt59o'
h=m.verify(S/'HANDOFF.json',dict(bytes=7884,sha256='418f9577fb0adb0e5f775c20b5e68903c76255154dc036f5fd979bf7fe392048'))
a=m.load(S/'HANDOFF.json');assert sorted(a['namespace'])==sorted(p.name for p in S.iterdir());current=[h]+[m.verify(x['path'],x) for x in a['payloads']];assert len(current)==8
rows=m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files'];assert len(rows)==252 and len({r['path'] for r in rows})==252
fresh=[]
for r in rows:
 z=m.verify(r['path'],r['identity']);assert z['resolved_path']==r['identity']['resolved_path'];assert z['symlink_chain']==r['identity'].get('symlinks',r['identity'].get('symlink_chain',[]));fresh.append(z)
old=m.load(m.B/'ri157-correlated-capacity-proof-tusjyk77/SOURCE_DEPENDENCIES.json')['protected_files'];assert len(old)==223
by={r['path']:r for r in rows}
for r in old:assert {k:v for k,v in r.items() if k!='role'}=={k:v for k,v in by[r['path']].items() if k!='role'}
review=m.verify(R/'INDEPENDENT_OUTCOME_REVIEW.json',dict(bytes=16134,sha256='5482ba4ea3113c53a23486ad4f0d5d8f14acd3bced3cf52119bea796e701685b'))
rv=m.load(review['path']);refs=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','bytes','sha256'}<=set(x) and str(x['path']).startswith('/'):refs.append(m.verify(x['path'],x))
  else:
   for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(rv)
replay=D/'measurement_replay';replay.mkdir()
for name,key in [('check_saved.py','finite_checker'),('check_saved_supplement.py','positive_relation_supplement_checker')]:
 r=rv['review_method'][key];m.verify(r['path'],r);(replay/name).write_bytes(Path(r['path']).read_bytes());m.verify(replay/name,r)
print(m.save('ROOT_METADATA_RECHECK.json',dict(status='PASS',native_historical=fresh,native_current=current,inherited_rows_unchanged_except_role=223,historical_source_bytes=sum(r['bytes'] for r in fresh),native_reference_expansion='Author 1977-reference expansion attributed, not independently repeated; root fresh whole identities for every selected dependency and exact inherited rows.',measurement_review=review,measurement_direct_references=refs,measurement_replay_sources=[m.ref(replay/n) for n in ('check_saved.py','check_saved_supplement.py')],scientific_body_decoded=False,scientific_execution=False,actual_vector_read=False)))
