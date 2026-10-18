"""Root metadata preflight/card issuance only. Never executes the target."""
from pathlib import Path
import hashlib,importlib.util,os,stat,sys,time
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri249-root-premode-operation-hcybjv4k';P=B/'ri247-root-hook-branch-review-6fgw5qd9';D=B/'ri244-current-normal-premode-2kfsmiea';E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri156-operation-ri244-premode-2kfsmiea'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7';s=importlib.util.spec_from_file_location('ri249_admin',hp);m=importlib.util.module_from_spec(s);exec(compile(raw,str(hp),'exec'),m.__dict__);m.D=R
phase=sys.argv[1];assert phase in ['preflight','issue','dispatch','postflight']
def st(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
seen={}
def verify(row):
 v=m.identity(row['path']);assert all(v[k]==val for k,val in row.items()),row['path']
 if row['path'] in seen:assert seen[row['path']]==v
 seen[row['path']]=v;return v
def loadpin(row):verify(row);return m.load(row['path'])
adref=dict(path=str(P/'RI244_PREPARATION_ADJUDICATION.json'),bytes=3323,sha256='673689def36a4720a9f14d647147048fc150fc4a19fdfdc56a8816fdd87ee274');ad=loadpin(adref);assert ad['status']=='ACCEPT_UNISSUED_PREPARATION_ONLY' and not ad['operational_authorization'];root=loadpin(ad['root_check']);ih=loadpin(ad['independent_handoff'])
for row in ih['files']:verify(row)
for key in ['source_acceptance','independent_review','independent_check','genuine_tools','invocation_context','next_recipe','recipe_sequence_correction']:verify(ad[key])
for row in root['outputs']:verify(row)
assert all(r['state'][3]==1 and not r['symlink_chain'] and r['resolved_path']==r['path'] for r in root['outputs'])
custody=m.load(D/'CUSTODY_BEFORE.json');assert len(custody['identities'])==2854
for row in custody['identities']:verify(row)
for row in root['directories']:
 p=Path(row['path']);assert not p.is_symlink() and p.resolve()==p and stat.S_ISDIR(st(p)[2])
 if phase!='postflight' or p.name=='tmp':assert st(p)==row['state'] and list(p.iterdir())==[]
wrapper=m.load(D/'ADMISSION_CANDIDATE.json');card=wrapper['candidate'];assert wrapper['status']=='UNISSUED_NOT_OPERATIONAL_AUTHORITY' and wrapper['operational_authorization'] is False
assert set(card)=={'schema','status','action','source_manifest','source_review','qualification','request','output','environment','bootstrap_preflight','bounds','genuine_outer_required'} and card['action']=='pre_mode' and card['output']==str(O)
manifest=loadpin(card['source_manifest']);assert len(manifest['modules'])==11 and len(manifest['dependencies'])==567
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:verify(row)
verify(manifest['bootstrap_binding']);verify(manifest['bootstrap_provenance']);verify(card['source_review']);verify(card['bootstrap_preflight'])
qual=loadpin(card['qualification']);assert qual['source_manifest']==card['source_manifest'] and qual['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS' and qual['all_passed'] is True and qual['scientific_execution'] is False and len(qual['controls'])==106
for key in ['report','genuine_outer','independent_review']:verify(qual[key])
request=loadpin(card['request']);assert sorted(Path(card['request']['path']).parent.iterdir())==sorted([Path(card['request']['path']),Path(request['actual_runtime']['path'])]);assert len(request)==5
runtime=loadpin(request['actual_runtime']);assert len(runtime)==13 and runtime['environment']['TMPDIR']==str(E/'tmp') and card['environment']['TMPDIR']==str(D/'tmp')
assert card['bounds']==dict(file_bytes=67108864,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,rss_kib=524288,target_poll_seconds=.025,wall_seconds=180) and card['genuine_outer_required'] is True
v=m.load(D/'SUPPLIER_BEFORE.json')
for row in v['vendor']+v['tools']:verify(row)
for row in v['namespace']:
 p=Path(row['path']);assert st(p)==row['state']
 if row['kind']=='directory':assert stat.S_ISDIR(st(p)[2]) and sorted(x.name for x in p.iterdir())==row['entries']
 else:assert row['kind']=='symlink' and p.is_symlink() and os.readlink(p)==row['target']
 assert st(p)==row['state']
for p in v['absent']:assert not os.path.lexists(p)
assert [len(v['vendor']),sum(r['bytes'] for r in v['vendor']),len(v['tools']),len(v['namespace']),len(v['absent'])]==[1810,48024515,4,195,2]
hostpath=R/('GENUINE_POST_HOST.json' if phase=='postflight' else 'GENUINE_PRE_HOST.json');host=m.load(hostpath);verify(m.ref(hostpath));prior=m.load(P/'RI244_GENUINE_PREPARATION_HOST.json');assert host['arguments']==prior['arguments'] and host['result']['exit_code']==0 and not host['result'].get('session_id') and host['result']['chunk_id']!=prior['result']['chunk_id'];import json
assert json.loads(host['result']['output'])==host['observation']==prior['observation'];assert host['observation']['uname']==list(os.uname());assert v['host']==dict(argv=host['observation']['command'],exit_code=host['observation']['returncode'],stdout=host['observation']['stdout'],stderr=host['observation']['stderr'],uname=host['observation']['uname'])
et=m.load(D/'E_BEFORE.json');assert len(et)==58 and sum(x['kind']=='file' for x in et)==49
for row in et:
 p=E/row['relative'];assert not p.is_symlink() and st(p)==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:verify(row['identity'])
 assert st(p)==row['state']
for p in [E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized']:assert list(p.iterdir())==[]
monitor=B/'ri141-white-bootstrap-source-h58ls076/prepare.py';verify(dict(path=str(monitor),bytes=45721,sha256='8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe'))
verify(wrapper['bootstrap_proposal']);assert (D/'PRE_MODE_BOOTSTRAP.proposal.py').read_bytes()==Path('/private/tmp/ri244-preparation-proposal-3udz0imk/PRE_MODE_BOOTSTRAP.proposal.txt').read_bytes()
base={Path(r['path']).name for r in root['outputs']}|{'tmp','monitor'};extra={'ADMIT_PRE_MODE.json','DISPATCH.json'}
assert set(x.name for x in D.iterdir())==base|(extra if phase in ['dispatch','postflight'] else set())
if phase!='postflight':assert not os.path.lexists(O)
if phase=='issue':
 review=loadpin(m.ref(R/'PREDISPATCH_SOURCE_REVIEW.json'));assert review['status']=='ACCEPT_BOUNDED_ROOT_METADATA_PREFLIGHT_SOURCE'
 body=m.canonical(card)
 with (D/'ADMIT_PRE_MODE.json').open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
 assert (D/'ADMIT_PRE_MODE.json').read_bytes()==body
 dispatch=dict(schema='ri249-one-premode-dispatch-v1',admission=m.ref(D/'ADMIT_PRE_MODE.json'),bootstrap=wrapper['bootstrap_proposal'],preparation_acceptance=adref,environment=card['environment'],outer_cwd=str(D),child_cwd=str(D/'monitor'),label='PRE_MODE',outer_alarm_seconds=960,one_attempt=True,scientific_execution=False)
 with (D/'DISPATCH.json').open('xb') as f:f.write(m.canonical(dispatch));f.flush();os.fsync(f.fileno())
 assert (D/'DISPATCH.json').read_bytes()==m.canonical(dispatch)
if phase in ['issue','dispatch','postflight']:
 assert (D/'ADMIT_PRE_MODE.json').read_bytes()==m.canonical(card);verify(m.ref(D/'ADMIT_PRE_MODE.json'));verify(m.ref(D/'DISPATCH.json'));dispatch=m.load(D/'DISPATCH.json');assert dispatch['admission']==m.ref(D/'ADMIT_PRE_MODE.json') and dispatch['bootstrap']==wrapper['bootstrap_proposal'] and dispatch['environment']==card['environment'] and dispatch['outer_cwd']==str(D) and dispatch['child_cwd']==str(D/'monitor') and dispatch['outer_alarm_seconds']==960 and dispatch['one_attempt'] is True
 if phase in ['dispatch','postflight']:
  issued=m.load(R/'ISSUE.json')
  for name in ['ADMIT_PRE_MODE.json','DISPATCH.json']:assert m.identity(D/name)==issued['controls'][name]
for row in list(seen.values()):assert m.identity(row['path'])==row
controls={name:m.identity(D/name) for name in extra} if phase in ['issue','dispatch','postflight'] else {}
result=dict(schema='ri249-whole-premode-custody-v1',phase=phase,status='PASS_METADATA_CUSTODY',observed_at_unix_ns=time.time_ns(),prepared_outputs=root['outputs'],input_identities=list(seen.values()),immutable_preparation_input_rows=2854,supplier_reference=m.ref(D/'SUPPLIER_BEFORE.json'),E_reference=m.ref(D/'E_BEFORE.json'),host=m.ref(hostpath),controls=controls,D_namespace=sorted(x.name for x in D.iterdir()),E_files=49,E_directories=9,E_unchanged=True,subject_executed_by_this_script=False,original_preparation_preserved=True)
print(m.save(phase.upper()+'.json',result))
