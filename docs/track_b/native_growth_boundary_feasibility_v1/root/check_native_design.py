"""Root text/opaque identity check only; never execute subject code."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);D=Path(__file__).resolve().parent;m.D=D;B=D.parent
S=B/'ri143-native-boundary-feasibility-0i0dbnge';OLD=B/'ri140-native-failure-repair-source-l_a4mna0'
h=m.load(S/'HANDOFF.json');assert h['payload_count']==13 and h['namespace_count']==14
assert sorted(x.name for x in S.iterdir())==sorted(h['namespace'])
pool={}
for r in h['payloads']:
 m.verify(r['path'],r);pool[r['path']]=r
pool[str(S/'HANDOFF.json')]=m.ref(S/'HANDOFF.json')
deps=m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files'];old=m.load(OLD/'SOURCE_DEPENDENCIES.json')['protected_files']
assert len(deps)==450 and len(old)==423
by={x['path']:x for x in deps};assert len(by)==450
for row in deps:
 r=row['identity'];found=m.verify(r['path'],r)
 assert found['resolved_path']==r['resolved_path'] and found['symlink_chain']==r['symlinks']
 pool[r['path']]=r
for row in old:
 assert {k:v for k,v in row.items() if k!='role'}=={k:v for k,v in by[row['path']].items() if k!='role'}
ids=m.load(S/'SOURCE_IDENTITIES.json');previous=m.load(OLD/'SOURCE_IDENTITIES.json')
assert ids['unchanged_policy_subjects']==previous['subjects']
policy_count=sum(len(x['ordered_cases']) for x in ids['unchanged_policy_subjects'].values());assert policy_count==139
def refs(v):
 if isinstance(v,dict):
  if {'path','bytes','sha256'}<=v.keys():yield v
  for a in v.values():yield from refs(a)
 elif isinstance(v,list):
  for a in v:yield from refs(a)
counts={}
for p in sorted(S.glob('*.json')):
 rows=list(refs(m.load(p)))
 for r in rows:
  assert r['path'] in pool, r['path']
  assert m.pure(r)==m.pure(pool[r['path']]),r['path']
 counts[p.name]=len(rows)
a=m.load(S/'F01_BOUNDARIES.json');b=m.load(S/'F02_BOUNDARIES.json')
expected=[]
for n in range(1,16):
 expected.extend(['F01-'+str(n)+'-'+s for s in ['SIGTERM','SIGINT','SIGHUP']] if n in [1,2,10,14] else ['F01-'+str(n)])
assert [r['id'] for r in a['rows']]==expected
assert [r['id'] for r in b['cases']]==['F02-1-UNREGISTER','F02-1-CLOSE']+['F02-'+str(i) for i in range(2,8)]
ranges=[]
for rows,sources,field in [(a['rows'],a['sources'],'subject_locations'),(b['cases'],b['sources'],'source_locations')]:
 for row in rows:
  assert row['executed'] is False and row['entry_preconditions'] and row['first_reachable_refusal']
  for loc in row[field]:
   path=loc['path'] if 'path' in loc else sources[loc['source']]['path']
   assert path in pool and Path(path).suffix in ('.py','.md')
   lines=Path(path).read_bytes().splitlines(keepends=True);lo=loc['start_line'];hi=loc['end_line']
   assert 1<=lo<=hi<=len(lines)
   ranges.append(dict(case=row['id'],path=path,start=lo,end=hi,**m.pin(b''.join(lines[lo-1:hi]))))
assert len(ranges)==104
app=m.load(S/'SOURCE_APPLICABILITY.json');assert app['source_diffs']==[] and app['new_controller_implemented'] is False
assert app['disposition']['platform_wide_impossibility_claimed'] is False
print(m.save('ROOT_NATIVE_DESIGN_CHECK.json',dict(schema='ri143-root-text-identity-check-v1',status='PASS',source_handoff=m.ref(S/'HANDOFF.json'),dependencies=450,dependency_bytes=sum(r['identity']['bytes'] for r in deps),inherited_unchanged_except_role=423,additions=27,policy_objects_unchanged=policy_count,typed_reference_counts=counts,typed_reference_total=sum(counts.values()),case_ids=expected+[r['id'] for r in b['cases']],source_ranges=ranges,subject_executed=False,scientific_body_decoded=False,current_runtime_observed=False)))
