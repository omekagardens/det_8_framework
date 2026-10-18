"""Root administrative reconstruction; never imports the subject writer/adapter."""
from pathlib import Path
import importlib.util, hashlib, json, os, stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri255-root-compensation-review-m__fsupr'
D=B/'ri249-normal-mode-card-preparation-y170alnf'
O=B/'ri156-operation-ri249-mode-card-y170alnf'
E=B/'ri154-white-execution-proposed-42_uvw15'
W=Path('/private/tmp/ri249-mode-card-preparation-proposal-y170alnf')
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=R
def state(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def load(p):return m.load(p)
def pin(p):return m.ref(p)
expected={}
def add(row):
 r={k:row[k] for k in ('path','bytes','sha256')}
 if r['path'] in expected:assert expected[r['path']]==r
 expected[r['path']]=r
def read(row):add(row);m.verify(row['path'],row);return load(row['path'])
def keep(v):
 if isinstance(v,dict):
  if {'path','bytes','sha256'}<=v.keys():add(v)
  elif set(v)=={'path','pin'} and isinstance(v['pin'],dict):add(dict(path=v['path'],**v['pin']))
  else:
   for x in v.values():keep(x)
 elif isinstance(v,list):
  for x in v:keep(x)
dec=load(R/'PREPARATION_DECISION.json');add(pin(hp));add(pin(R/'PREPARATION_DECISION.json'))
h=read(dec['proposal_handoff'])
assert sorted(x.name for x in W.iterdir())==h['namespace']
for row in h['files']:add(row)
refs=read(pin(W/'REFERENCES.json'))
for row in refs.values():add(row)
manifest=read(refs['source_manifest']);assert len(manifest['modules'])==11 and len(manifest['dependencies'])==567
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies'],manifest['bootstrap_binding']]:add(row)
qual=read(refs['qualification'])
assert qual['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS' and qual['all_passed'] and len(qual['controls'])==106
for key in ('report','genuine_outer','independent_review'):add(qual[key])
accepted=read(refs['input_review']);keep(accepted)
request=read(refs['request']);runtime=read(refs['runtime']);keep(request);keep(runtime)
assert len(runtime)==13 and len(request)==5
assert read(runtime['snapshot'])==read(runtime['baseline'])
assert read(runtime['vendor_before'])==read(runtime['vendor_after'])
assert read(runtime['observed_dyld_routes'])==read(runtime['snapshot'])['preobserved_dyld_routes']
ra=read(runtime['runtime_acceptance']);keep(ra);profiles=read(ra['profile_review']);keep(profiles)
normal=read(profiles['completions']['profile_normal']);keep(normal)
collection=read(refs['collection']);keep(collection);capture=read(refs['capture_review']);keep(capture)
preaccept=read(refs['pre_mode_acceptance']);keep(preaccept);preresult=read(refs['pre_result']);keep(preresult)
previous=read(refs['pre_mode_postflight']);keep(previous)
for row in previous['input_identities']:add(row)
priorcheck=read(refs['pre_mode_root_check']);keep(priorcheck)
for row in priorcheck['output_identities']+priorcheck['monitor_identities']:add(row)
oldroles=read(refs['old_roles'])
for row in oldroles['observed_identities']:add(row)
frozen=read(refs['copy_observation']);assert frozen['source_states']==oldroles['source_states']
oldvendor=read(refs['old_supplier']);oldE=read(refs['old_E']);oldhost=read(refs['old_host']);host=read(dec['host_transcript'])
oldpre=read(refs['old_preflight']);keep(oldpre)
oldadmit=read(pin(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'))
static=read(oldpre['static_native_adjudication'])
for row in oldvendor['vendor']+oldvendor['tools']:add(row)
for row in oldE:
 if row['kind']=='file':add(row['identity'])
cust=load(D/'CUSTODY_BEFORE.json');identities=cust['identities'];by_path={r['path']:r for r in identities}
assert len(identities)==len(by_path)==len(expected)==2920
assert set(by_path)==set(expected)
for path,r in expected.items():assert m.pure(r)==m.pure(by_path[path])
for row in identities:assert m.identity(row['path'])==row
assert cust==dict(schema='ri249-complete-mode-card-preparation-custody-v1',identities=identities,source_states=frozen['source_states'],historical_roles=refs['old_roles'],source_manifest=refs['source_manifest'],root_decision=pin(R/'PREPARATION_DECISION.json'),host_transcript=dec['host_transcript'])
assert host['arguments']==oldhost['arguments'] and json.loads(host['result']['output'])==host['observation']==oldhost['observation']
assert host['observation']['uname']==list(os.uname()) and host['result']['exit_code']==0
assert host['result']['chunk_id']!=oldhost['result']['chunk_id'] and 'session_id' not in host['result']
recipes=load(W/'ROOT_RECIPES.json');env=recipes['operation_environment'];bounds=recipes['operation_bounds']
vendor=load(D/'SUPPLIER_BEFORE.json');stable=lambda v:{k:x for k,x in v.items() if k not in ('environment','observed_at_unix_ns')}
assert stable(vendor)==stable(oldvendor) and vendor['environment']==env
assert [len(vendor['vendor']),sum(x['bytes'] for x in vendor['vendor']),len(vendor['tools']),len(vendor['namespace']),len(vendor['absent'])]==[1810,48024515,4,195,2]
for row in vendor['namespace']:
 p=Path(row['path']);assert state(p)==row['state']
 if row['kind']=='directory':assert stat.S_ISDIR(state(p)[2]) and sorted(x.name for x in p.iterdir())==row['entries']
 else:assert p.is_symlink() and os.readlink(p)==row['target']
 assert state(p)==row['state']
for p in vendor['absent']:assert not os.path.lexists(p)
ebefore=load(D/'E_BEFORE.json');assert ebefore==oldE
for row in ebefore:
 p=E/row['relative'];assert not p.is_symlink() and state(p)==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert m.identity(p)==row['identity']
 assert state(p)==row['state']
mode_request=dict(freeze=request['freeze'],mode='normal',pre=refs['pre_result'],normal_acceptance=None)
assert (D/'MODE_CARD_REQUEST.json').read_bytes()==(W/'MODE_CARD_REQUEST.proposal.json').read_bytes()==m.canonical(mode_request)
binding=m.identity(manifest['bootstrap_binding']['path'])
pre=dict(schema='ri249-root-unissued-mode-card-preflight-v1',status='PREPARED_UNISSUED_PENDING_INDEPENDENT_ROOT_REVIEW',selected_interpreter_binding=binding,source_observation=pin(D/'CUSTODY_BEFORE.json'),runtime_observation=pin(D/'SUPPLIER_BEFORE.json'),E_observation=pin(D/'E_BEFORE.json'),genuine_host=dec['host_transcript'],source_acceptance=refs['source_review'],input_acceptance=refs['pre_mode_acceptance'],static_native_adjudication=oldpre['static_native_adjudication'],platform_premises=static['platform_premises_accepted'],operation_premises=oldpre['operation_premises'],environment=env,scientific_execution_authorized=False,operational_authorization=False)
assert load(D/'BOOTSTRAP_PREFLIGHT.json')==pre
assert (D/'MODE_CARD_BOOTSTRAP.proposal.py').read_bytes()==(W/'MODE_CARD_BOOTSTRAP.proposal.txt').read_bytes()
candidate=dict(schema='ri156-root-adapter-admission-v1',status='AUTHORIZE_ONE_BOUNDED_METADATA_ACTION',action='mode_card',source_manifest=refs['source_manifest'],source_review=refs['source_review'],qualification=refs['qualification'],request=pin(D/'MODE_CARD_REQUEST.json'),output=str(O),environment=env,bootstrap_preflight=pin(D/'BOOTSTRAP_PREFLIGHT.json'),bounds=bounds,genuine_outer_required=True)
wrapper=dict(schema='ri249-wrapped-unissued-mode-card-admission-v1',status='UNISSUED_NOT_OPERATIONAL_AUTHORITY',candidate=candidate,bootstrap_proposal=pin(D/'MODE_CARD_BOOTSTRAP.proposal.py'),root_input_acceptance=refs['pre_mode_acceptance'],future_admission_path=str(D/'ADMIT_MODE_CARD.json'),operational_authorization=False)
assert len(candidate)==12 and len(wrapper)==7 and load(D/'ADMISSION_CANDIDATE.json')==wrapper
attempt=dict(schema='ri249-unissued-mode-card-preparation-attempt-v1',decision=pin(R/'PREPARATION_DECISION.json'),proposal=dec['proposal_handoff'],no_retry=True,operational_authorization=False)
assert load(D/'PREPARATION_ATTEMPT.json')==attempt
names=sorted(['PREPARATION_ATTEMPT.json','CUSTODY_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','MODE_CARD_REQUEST.json','BOOTSTRAP_PREFLIGHT.json','MODE_CARD_BOOTSTRAP.proposal.py','ADMISSION_CANDIDATE.json'])
artifacts={name:pin(D/name) for name in names};comp=load(D/'PREPARATION_COMPLETE.json');obs=comp['tail_observations'];tails=comp['independent_tails']
assert obs['inputs']==dict(values=identities,errors=[]) and obs['outputs']==dict(values=artifacts,errors=[])
assert {k:v for k,v in obs['supplier'].items() if k!='observed_at_unix_ns'}=={k:v for k,v in vendor.items() if k!='observed_at_unix_ns'}
assert type(obs['supplier']['observed_at_unix_ns']) is int and obs['supplier']['observed_at_unix_ns']>=vendor['observed_at_unix_ns']
assert obs['namespace']==sorted(names+['tmp','monitor'])
expectedtails={k:dict(value=v,error=None) for k,v in dict(inputs=2920,supplier=dict(vendor=1810,namespace=195,tools=4,absent=2),E=ebefore,authority_absences=None,outputs=artifacts,namespace=obs['namespace']).items()}
assert tails==expectedtails
assert comp==dict(schema='ri249-unissued-mode-card-preparation-completion-v1',status='UNISSUED_PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW',first_error=None,independent_tails=expectedtails,tail_observations=obs,artifacts=artifacts,input_count=2920,root_decision=pin(R/'PREPARATION_DECISION.json'),operational_authorization=False,subject_executed=False,installed_freeze_decoded=False,E_written=False,RET_paused=True)
assert sorted(x.name for x in D.iterdir())==sorted(names+['PREPARATION_COMPLETE.json','tmp','monitor'])
for name in ('tmp','monitor'):assert (D/name).is_dir() and not (D/name).is_symlink() and list((D/name).iterdir())==[]
for p in [O,D/'ADMIT_MODE_CARD.json',D/'DISPATCH.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized']:assert list(p.iterdir())==[]
priorD=B/'ri244-current-normal-premode-2kfsmiea';assert sorted(x.name for x in priorD.iterdir())==previous['D_namespace'] and not list((priorD/'tmp').iterdir())
assert sorted(x.name for x in Path(refs['request']['path']).parent.iterdir())==['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json']
priorO=Path(refs['pre_result']['path']).parent;assert sorted(x.name for x in priorO.iterdir())==['ATTEMPT.json','COMPLETE.json','RESULT.json']
priorMonitor=Path(priorcheck['monitor_identities'][0]['path']).parent;assert sorted(x.name for x in priorMonitor.iterdir())==['PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stderr','PRE_MODE.stdout']
outputs=[m.identity(D/name) for name in names+['PREPARATION_COMPLETE.json']]
for row in outputs:assert row['resolved_path']==row['path'] and not row['symlink_chain'] and stat.S_ISREG(row['state'][2]) and m.identity(row['path'])==row
g=load(R/'GENUINE_PREPARATION_TOOLS.json');assert g['initial']['result']['session_id']==49699 and g['terminal']['exit_code']==0 and g['terminal']['output']==''
out=dict(schema='ri255-root-mode-preparation-check-v1',status='PASS_COMPLETE_UNISSUED_PREPARATION_RECONSTRUCTION',source_execution_receipts=['ba403e/session49699','8b2cd4'],source_decision=pin(B/'ri253-root-sigma-review-oij6zgup/MODE_CARD_SOURCE_ADJUDICATION.json'),decision=pin(R/'PREPARATION_DECISION.json'),input_count=len(identities),exact_input_domain=True,output_identities=outputs,full_request=mode_request,full_preflight=pre,full_wrapper=wrapper,all_six_tails_reconstructed=True,supplier_files=1810,supplier_bytes=48024515,supplier_tools=4,supplier_namespaces=195,supplier_absences=2,E_files=49,E_directories=9,E_unchanged=True,prior_pre_mode_preserved=True,operational_authorization=False,scientific_execution=False,qualification_credit=0,RET_paused=True,diagnostics=['13570c overly broad COMPLETE display clipped','f90802 structural display clipped then TypeError on len(None); no target action; corrected bounded0dfe6d'])
print(m.save('ROOT_PREPARATION_CHECK.json',out))
