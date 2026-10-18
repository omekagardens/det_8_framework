"""Finite root administrative preflight review; no candidate or subjects run."""
import hashlib,importlib.util,json,os,stat
from pathlib import Path
D=Path(__file__).parent;B=D.parent;S=B/'ri163-native-qualification-preflight-fqexul5v'
H=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=H.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
observed={}
def pin(row):
 p=row['path'];r=m.verify(p,row);assert r['resolved_path']==p and r['symlink_chain']==[];observed[p]=r;return r
pin({'path':str(S/'HANDOFF.json'),'bytes':13272,'sha256':'ea9df2610f7969b626608866e10f78e597ea00d75e74f539148d86b970e18347'})
h=m.load(S/'HANDOFF.json');assert sorted(p.name for p in S.iterdir())==sorted(h['namespace'])
assert sorted(Path(r['path']).name for r in h['payloads'])==sorted(set(h['namespace'])-{'HANDOFF.json'})
for row in h['payloads']:pin(row)
deps=m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files'];assert len(deps)==307 and len(set(r['path'] for r in deps))==307
for row in deps:pin(row['identity'])
assert sum(r['identity']['bytes'] for r in deps)==33312952
old=m.load(B/'ri161-grid-qualification-source-679wwadg/SOURCE_DEPENDENCIES.json')['protected_files'];by={r['path']:r for r in deps}
for row in old:assert {k:v for k,v in row.items() if k!='role'}=={k:v for k,v in by[row['path']].items() if k!='role'}
for row in h['accepted_sources_unchanged'].values():pin(row)
req=m.load(S/'REQUEST_PROPOSAL.json');cmd=m.load(S/'DISPATCH_PROPOSAL.json')
raw=req['exact_proposed_request_utf8'].encode();assert m.pin(raw)==m.pure(h['exact_request_proposal']) and json.loads(raw)==req['proposed_request']
assert set(req['proposed_request'])=={'schema','nonce','interpreter','sources','output_directory','trust_basis'}
assert req['proposed_request']['sources']==h['accepted_sources_unchanged']
assert m.pin(cmd['command_utf8'].encode())==cmd['command_pin']==h['command_proposal_pin']
assert m.pin(json.dumps(cmd['environment'],separators=(',',':')).encode())==cmd['environment_pin']==h['environment_proposal_pin']
absences={k:not os.path.lexists(v) for k,v in cmd['evidence_paths_proposed'].items() if k!='nonce'};assert len(absences)==6 and all(absences.values())
assert not os.path.lexists('/opt/homebrew/bin/gtimeout')
policy=m.load(S/'OBSERVATION_POLICY.json');facts=m.load(S/'HOST_RUNTIME_FACTS.json');ext=policy['supplier_extensions'][0]
expected={r['path']:r['expected_kind'] for r in ext['entries']};expected[ext['root_path']]='directory'
allrows=[r for batch in facts['vendor_batches'] for r in batch['outcome']['observations']]
extra=[r for r in allrows if r['path'] not in expected]
assert [r['path'] for r in extra]==[ext['root_path']+'/lib/python39.zip','/Library/Python/3.9/site-packages']
assert not os.path.lexists(extra[0]['path']) and not os.path.lexists('/Library/Python')
rows=[r for r in allrows if r['path'] in expected]
assert len(rows)==len(expected)==2005 and len(set(r['path'] for r in rows))==2005
statekeys=('dev','ino','mode','nlink','size','mtimeNs','ctimeNs')
st=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
counts={'file':0,'directory':0,'symlink':0};regularbytes=0;namespace=[]
for row in rows:
 p=Path(row['path']);kind=expected[str(p)];assert row['kind']==kind;before=p.lstat();assert st(before)==[int(row['state'][k]) for k in statekeys]
 if kind=='file':
  fresh=pin(row);assert fresh['state']==st(before);regularbytes+=fresh['bytes']
 elif kind=='directory':
  assert stat.S_ISDIR(before.st_mode)
  wanted=sorted(Path(k).name for k in expected if Path(k).parent==p)
  got=sorted(x.name for x in p.iterdir());assert got==wanted and len(got)==row['entries']
  namespace.append({'path':str(p),'kind':kind,'entries':got,'state':st(before)})
 elif kind=='symlink':
  assert stat.S_ISLNK(before.st_mode)
  target=os.readlink(p);assert target==row['target']
  namespace.append({'path':str(p),'kind':kind,'target':target,'state':st(before)})
 else:raise ValueError(kind)
 assert st(p.lstat())==st(before);counts[kind]+=1
assert counts=={'file':1810,'directory':185,'symlink':10} and regularbytes==48024515
for row in facts['historical_support']:pin(row)
for row in facts['phase1']['outcome']['observations']:
 if 'identity' in row:assert pin(row['identity'])['state']==[int(row['state'][k]) for k in statekeys]
for p,row in observed.items():assert m.identity(p)==row
assert sorted(p.name for p in S.iterdir())==sorted(h['namespace'])
print(m.save('NATIVE_METADATA_CHECK.json',dict(schema='ri163-root-finite-preflight-check-v1',status='EXACT_PREPARATION_AND_CURRENT_FIXED_FACTS_CONFIRMED_NOT_ADMITTED',subject=m.ref(S/'HANDOFF.json'),dependencies=len(deps),selected_source_bytes=33312952,inherited_rows=len(old),source_files=11,payloads=10,vendor_counts=counts,vendor_regular_bytes=regularbytes,namespace=namespace,fresh_identities=list(observed.values()),request_bytes=m.pin(raw),command_pin=cmd['command_pin'],environment_pin=cmd['environment_pin'],proposed_path_absences=absences,selected_gtimeout_absent=True,scientific_or_vendor_execution=False,native_dependency_graph_established=False,historical_reference_counts='Author assertions authenticated; this root check did not expand all2721 historical references.',system_trust_admitted=False)))
R=B/'ri162-independent-preflight-review-i6j707uw';a=m.load(D/'METADATA_CHECK.json');b=m.load(R/'METADATA_CHECK.json')
excluded={'schema','observed_at_utc'};assert {k:v for k,v in a.items() if k not in excluded}=={k:v for k,v in b.items() if k not in excluded}
for row in a['identities']:assert m.identity(row['path'])==row
print(m.save('MEASUREMENT_METADATA_REPLAY.json',dict(schema='ri162-root-exact-preflight-replay-v1',status='FINITE_METADATA_AND_COMMAND_BINDINGS_CONFIRMED_NOT_ADMISSION',root_full=m.ref(D/'METADATA_CHECK.json'),review_full=m.ref(R/'METADATA_CHECK.json'),replay_chunk='cf71b8',exit_code=0,predicates=a['predicate_count'],source_objects=a['source_evidence_count'],source_dependencies=a['source_dependency_count'],fresh_identities=a['unique_observed_identities'],inherited_spans=len(a['inherited_spans']),all_report_fields_equal_except=sorted(excluded),controls_executed=0)))
