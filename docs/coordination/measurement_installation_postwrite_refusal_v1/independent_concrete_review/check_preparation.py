"""RI224 independent administrative-only reconstruction. No subject imports/runs.
Opaque file hashing, fixed namespace checks and saved administrative JSON only.
"""
from pathlib import Path
import json,hashlib,os,stat,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri222-freeze-cwd-repair-ypiy2jqw';W=D/'worker_proposal';R=Path(__file__).resolve().parent;OLD=B/'ri206-root-freeze-5e_n5lj_';E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri222-freeze-install-operation-ypiy2jqw'
checks=0;identities={}
def c(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def require(ok,msg):
 global checks
 checks+=1
 if not ok:raise ValueError(msg)
def equal(a,b,msg):require(c(a)==c(b),msg)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(path):
 p=Path(path);s=p.lstat();require(p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode),'regular literal '+str(p));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  equal(state(os.fstat(f.fileno())),state(s),'open selection')
  for block in iter(lambda:f.read(1048576),b''):h.update(block);n+=len(block)
  equal(state(os.fstat(f.fileno())),state(s),'descriptor stable')
 equal(state(p.lstat()),state(s),'closed selection stable');require(n==s.st_size,'whole hash length')
 v=dict(path=str(p),resolved_path=str(p),symlink_chain=[],bytes=n,sha256=h.hexdigest(),state=state(s))
 if str(p) in identities:equal(v,identities[str(p)],'repeat complete identity stable')
 identities[str(p)]=v;return v

def pin(v):return {k:v[k] for k in ('path','bytes','sha256')}
def ref(path):return pin(identity(path))
def verify(row):
 z=identity(row['path']);equal(pin(z),pin(row),'declared pin '+row['path']);return z

def load(path):
 # Caller-selected administrative records only.
 def pairs(rows):
  d={}
  for k,v in rows:require(k not in d,'duplicate admin key');d[k]=v
  return d
 def bad(value):raise ValueError('nonfinite admin JSON')
 return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)
def readref(row):verify(row);return load(row['path'])

expected_namespace=['E_BEFORE.json','HOST_BEFORE.json','HOST_GENUINE_TOOL.json','INSTALLATION_PROPOSAL.json','INSTALL_BOOTSTRAP.py','INSTALL_PREFLIGHT.json','PREPARATION_CUSTODY.json','ROOT_SOURCE_REVIEW.json','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','monitor','tmp','worker_proposal']
equal(sorted(x.name for x in D.iterdir()),expected_namespace,'complete preparation namespace')
for name in ('tmp','monitor'):require((D/name).is_dir() and not (D/name).is_symlink(),'control directory');equal(list((D/name).iterdir()),[],'empty control dir')
for p in (O,D/'ADMIT_INSTALL.json',D/'DISPATCH.json',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json'):require(not os.path.lexists(p),'unissued/uninstalled '+str(p))
for name,size,sha in [('ROOT_SOURCE_REVIEW.json',2307,'ae31240d4d29b7ccefd28cf8b75d908be318eb1bd3b94fd46aa698dc7398f5bd'),('INSTALLATION_PROPOSAL.json',4509,'ca1dd21438eaff45880fae5699177f2ef29a0d5e0b2103648ee4de8704e6361b'),('PREPARATION_CUSTODY.json',16080,'b165ed2229cf07c61b138fdca0fdde53ddd25ccecdfb8273c6155fc9f552be52'),('INSTALL_BOOTSTRAP.py',2413,'8fbc916c29a874d93f2a1b0543e86870f26a6dc2ce01c57104dcd725c092d853')]:verify(dict(path=str(D/name),bytes=size,sha256=sha))
review=load(D/'ROOT_SOURCE_REVIEW.json');proposal=load(D/'INSTALLATION_PROPOSAL.json');custody=load(D/'PREPARATION_CUSTODY.json');pre=load(D/'INSTALL_PREFLIGHT.json');manifest=load(W/'SOURCE_PINS.json');hand=load(W/'HANDOFF.json')
equal(review['subject'],ref(W/'HANDOFF.json'),'accepted entire source seal');equal(review['source_manifest'],ref(W/'SOURCE_PINS.json'),'source manifest acceptance');equal(review['status'],'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY','compatible source status');require(review['installation_admitted'] is False and review['scientific_execution'] is False and review['qualification_credit']==0,'source authority boundary')
equal(sorted(x.name for x in W.iterdir()),sorted(hand['namespace']),'source seal namespace')
packet=[verify(x) for x in hand['files']]+[identity(W/'HANDOFF.json')]
support=[verify(review[k]) for k in ('independent_review','root_metadata')]
# Keep every prior independent source-review payload immutable, not merely its handoff.
review_hand=readref(review['independent_review']);equal(sorted(x.name for x in Path(review['independent_review']['path']).parent.iterdir()),review_hand['namespace'],'old review namespace')
for row in review_hand['files']:verify(row)
inputs=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');graph=readref(inputs['roles']['graph']);history=readref(inputs['roles']['historical_supplier']);oldE=readref(inputs['roles']['historical_E'])
equal([len(inputs['files']),len(repair['files']),inputs['prior_role_count'],len(inputs['prior_role_rows']),len(graph['copied_files']),len(graph['history_originals']),len(graph['sources'])],[806,90,810,810,48,124,30],'full retained domains')
source_refs={}
for row in inputs['files']+repair['files']+manifest['files']+[ref(W/'SOURCE_PINS.json'),ref(D/'ROOT_SOURCE_REVIEW.json'),ref(D/'INSTALL_BOOTSTRAP.py')]:
 z=pin(row)
 if z['path'] in source_refs:equal(source_refs[z['path']],z,'nonconflicting source alias')
 source_refs[z['path']]=z
equal(len(source_refs),904,'closed current source union')
sources=load(D/'SOURCES_BEFORE.json');equal([r['path'] for r in sources],sorted(source_refs),'every sorted source path');equal(len(sources),904,'all904')
for row in sources:equal(pin(row),source_refs[row['path']],'source role pin');equal(identity(row['path']),row,'full saved/current source selection')
# Complete selected supplier inventory, fixed named namespace and absence checks.
supplier=load(D/'SUPPLIER_BEFORE.json');equal(sorted(supplier),sorted(history),'supplier closed fields')
env=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
limits=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864)
equal(supplier['environment'],env,'ten exact environment fields');equal({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in history.items() if k not in ('environment','observed_at_unix_ns')},'entire unchanged historical supplier')
require(type(supplier['observed_at_unix_ns']) is int and supplier['observed_at_unix_ns']>history['observed_at_unix_ns'],'new supplier observation time')
equal([len(supplier['vendor']),sum(r['bytes'] for r in supplier['vendor']),len(supplier['tools']),len(supplier['namespace']),len(supplier['absent'])],[1810,48024515,4,195,2],'supplier complete retained sizes')
for row in supplier['vendor']+supplier['tools']:equal(identity(row['path']),row,'every current vendor/tool identity')
namespace=[]
for row in supplier['namespace']:
 p=Path(row['path']);before=state(p.lstat());r=dict(path=str(p),kind=row['kind'],state=before)
 if row['kind']=='directory':require(p.is_dir() and not p.is_symlink(),'literal namespace directory');r['entries']=sorted(x.name for x in p.iterdir())
 else:require(row['kind']=='symlink' and p.is_symlink(),'namespace named link');r['target']=os.readlink(p)
 equal(r,row,'every namespace field');equal(state(p.lstat()),before,'namespace selection');namespace.append(r)
for path in supplier['absent']:require(not os.path.lexists(path),'supplier absence')
equal(list(os.uname()),supplier['host']['uname'],'saved/current uname; no external host command invoked')
# No scientific decode: E is opaque copied source/file content with metadata rows.
etree=load(D/'E_BEFORE.json');equal(etree,sorted(oldE,key=lambda r:r['relative']),'whole preserved E baseline');current=[]
for row in etree:
 p=E/row['relative'];r=dict(relative=row['relative'],kind=row['kind'],state=state(p.lstat()))
 if row['kind']=='directory':require(p.is_dir() and not p.is_symlink(),'E literal directory');r['entries']=sorted(x.name for x in p.iterdir())
 else:require(row['kind']=='file','E ordinary file');r['identity']=identity(p)
 current.append(r)
equal(current,etree,'every complete E field');equal([sum(r['kind']=='file' for r in etree),sum(r['kind']=='directory' for r in etree)],[48,9],'E48/9');equal(sorted(str(p.relative_to(E)) for p in E.rglob('*')),sorted(r['relative'] for r in etree if r['relative']!='.'),'exact E namespace')
for name in ('tmp','runs/normal','runs/optimized'):equal(list((E/name).iterdir()),[],'no mode/science temporary content')
# Reconstruct host wrapper and preserve original actual transcript value.
host_input=B/'ri224-root-cwd-review-nyvru347/GENUINE_PREPARATION_HOST_TOOL.json';host_original=load(host_input);canonical_host=load(D/'HOST_GENUINE_TOOL.json');equal(canonical_host,host_original,'complete host original/value');require((D/'HOST_GENUINE_TOOL.json').read_bytes()==c(host_original),'exact canonical host bytes')
equal(host_original['schema'],'ri224-root-genuine-host-tool-transcript-v1','fresh host schema');equal(host_original['result']['chunk_id'],'343dae','root provided genuine host event');require(type(host_original['result']['exit_code']) is int and host_original['result']['exit_code']==0 and 'session_id' not in host_original['result'],'host genuine zero')
obs=host_original['observation'];equal(json.loads(host_original['result']['output']),obs,'entire real host stdout');equal(obs,dict(command=history['host']['argv'],environment={'PATH':'/usr/bin:/bin','LC_ALL':'C'},returncode=0,stdout=history['host']['stdout'],stderr='',uname=history['host']['uname']),'whole host observation')
host=load(D/'HOST_BEFORE.json');equal(host,dict(schema='ri209-root-host-command-record-v1',**obs,genuine_tool=ref(D/'HOST_GENUINE_TOOL.json')),'whole host wrapper')
# Bootstrap is reconstructed as plain text, never evaluated.
changes=[['# One root-admitted administrative freeze-candidate action; unchanged RI141 child monitor.','# One root-admitted administrative installation; unchanged RI141 child monitor.'],[str(OLD/'tmp'),str(D/'tmp')],['ri206_whole_unchanged_ri141_freeze_monitor','ri224_whole_unchanged_ri141_install_monitor'],[str(B/'ri160-white-fixture-custody-repair-ufok1zpo/adapter.py'),str(W/'install_freeze.py')],[str(OLD/'ADMIT_FREEZE_CANDIDATE.json'),str(D/'ADMIT_INSTALL.json')],[str(OLD/'monitor'),str(D/'monitor')],["'FREEZE', 180, expected_environment)","'INSTALL', 180, expected_environment)"]]
bootstrap=(OLD/'FREEZE_BOOTSTRAP.py').read_text()
for before,after in changes:require(bootstrap.count(before)==1,'unique literal bootstrap replacement');bootstrap=bootstrap.replace(before,after)
require(bootstrap.encode()==(D/'INSTALL_BOOTSTRAP.py').read_bytes(),'complete seven-substitution bootstrap')
equal(pre,dict(schema='ri209-root-installation-preflight-v1',status='FRESH_EXACT_INSTALLATION_PREFLIGHT',sources=ref(D/'SOURCES_BEFORE.json'),supplier=ref(D/'SUPPLIER_BEFORE.json'),E_before=ref(D/'E_BEFORE.json'),host_tool_receipts=ref(D/'HOST_BEFORE.json'),monitor_bootstrap=ref(D/'INSTALL_BOOTSTRAP.py'),source_manifest=ref(W/'SOURCE_PINS.json'),environment=env,scientific_execution=False),'all ten preflight fields')
card=dict(schema='ri209-root-freeze-installation-admission-v1',status='AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION',source_manifest=ref(W/'SOURCE_PINS.json'),source_review=ref(D/'ROOT_SOURCE_REVIEW.json'),preflight=ref(D/'INSTALL_PREFLIGHT.json'),output=str(O),environment=env,limits=limits,genuine_outer_required=True)
card_bytes=c(card);prospective=dict(path=str(D/'ADMIT_INSTALL.json'),bytes=len(card_bytes),sha256=hashlib.sha256(card_bytes).hexdigest())
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
argv=['/usr/bin/env','-i',*[k+'='+v for k,v in env.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',VENDOR,'-I','-B',str(D/'INSTALL_BOOTSTRAP.py')]
dispatch=dict(outer_argv=argv,shell_command=shlex.join(argv),cwd=str(D),login=False,admission=prospective,bootstrap=ref(D/'INSTALL_BOOTSTRAP.py'),monitor_source=ref(B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),external_timeout_seconds=960,single_attempt=True,actual_execution_not_yet_started=True)
equal(proposal,dict(schema='ri224-unissued-installation-proposal-v1',status='UNISSUED_REQUIRES_ROOT_PREFLIGHT_REVIEW',proposed_admission=card,prospective_admission_pin=prospective,proposed_dispatch=dispatch,active_card_created=False,dispatch_created=False),'whole unissued proposal, nine card fields, ten dispatch fields')
prep_source=B/'ri224-root-cwd-review-nyvru347/prepare_installation.py';equal(ref(prep_source),dict(path=str(prep_source),bytes=18455,sha256='9af0db33f4a57036b0f9bb911822dfd1ea905b6bddca1edc274d78dc00b05e80'),'exact executed administrative source pin')
# Source acceptance is independently bound to the copied reviewed draft and actual invocation.
root=prep_source.parent
verify(dict(path=str(root/'PREPARATION_SOURCE_ACCEPTANCE.json'),bytes=1815,sha256='dbe2730a6252593e48482921ab92f5b41993b56c40060ef0bf3973be540c2bf6'))
source_acceptance=load(root/'PREPARATION_SOURCE_ACCEPTANCE.json');equal(source_acceptance['source'],ref(prep_source),'accepted preparation source');equal(source_acceptance['status'],'ACCEPT_EXACT_ADMINISTRATIVE_PREPARATION_SOURCE','separate preparation source decision')
equal(source_acceptance['mandatory_invocation'],['/opt/homebrew/bin/python3','-I','-B'],'no-bytecode caller condition')
require(source_acceptance['installation_admitted'] is False and source_acceptance['qualification_credit']==0,'preparation acceptance scope')
source_hand=readref(source_acceptance['independent_review']); source_review_dir=Path(source_acceptance['independent_review']['path']).parent
equal(sorted(p.name for p in source_review_dir.iterdir()),sorted(source_hand['namespace']),'whole separate source-review seal')
for row in source_hand['files']:verify(row)
equal({k:source_hand['reviewed_copy'][k] for k in ('bytes','sha256')},{k:ref(prep_source)[k] for k in ('bytes','sha256')},'entire executed draft matches reviewed copy')
verify(dict(path=str(source_review_dir/'HANDOFF.json'),bytes=2612,sha256='44a01340d1b87d4890a78bfa5e0dc618c7df99f1f89cc5343dec5eb8bda6f508'))
equal(source_acceptance['fresh_host_tool'],ref(host_input),'fresh host selecting pin')
# The critical complete outer/child cwd relation is reconstructed as literal source text.
monitor_path=B/'ri141-white-bootstrap-source-h58ls076/prepare.py';monitor_text=monitor_path.read_text()
child_span=monitor_text[monitor_text.index('def child_run(command, out, label, seconds, env):'):monitor_text.index('def dyld_attempts(')]
popen="child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,\n                                     cwd=out, env=env, start_new_session=True)"
require(child_span.count(popen)==1 and 'chdir' not in child_span,'unchanged Popen cwd=out')
expected_child=[VENDOR,'-I','-B',str(W/'install_freeze.py'),'--admission',str(D/'ADMIT_INSTALL.json')]
expected_call='module.child_run('+repr(expected_child)+', Path('+repr(str(D/'monitor'))+"), 'INSTALL', 180, expected_environment)"
equal([line for line in bootstrap.splitlines() if line.startswith('module.child_run(')],[expected_call],'exact complete concrete bootstrap call')
guard="need(Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W,'fixed operation paths')"
require((W/'install_freeze.py').read_text().count(guard)==1,'corrected exact child guard')
cwd_contract=dict(outer_cwd=str(D),child_cwd=str(D/'monitor'),monitor=ref(monitor_path),exact_popen=popen,generated_child_call=expected_call,installer=ref(W/'install_freeze.py'),installer_guard=guard,source_text_only=True,subject_execution=False)
equal(custody,dict(schema='ri224-root-preparation-custody-v1',status='PREPARED_NOT_ADMITTED_OR_DISPATCHED',sealed_source_packet=packet,root_review_support=support,original_genuine_host=ref(host_input),canonical_genuine_host=ref(D/'HOST_GENUINE_TOOL.json'),monitor_template=ref(OLD/'FREEZE_BOOTSTRAP.py'),bootstrap_replacements=changes,cwd_contract=cwd_contract,source_domain=904,prior_roles=810,copy_history_targets=[48,124,30],source_observations=ref(D/'SOURCES_BEFORE.json'),supplier_observation=ref(D/'SUPPLIER_BEFORE.json'),E_observation=ref(D/'E_BEFORE.json'),preflight=ref(D/'INSTALL_PREFLIGHT.json'),unissued_proposal=ref(D/'INSTALLATION_PROPOSAL.json'),preparation_source=ref(prep_source),tool_origin_and_startup_are_root_premises=True,scientific_execution=False,installation_admitted=False,installation_dispatched=False,ret_paused=True),'entire closed preparation custody including cwd relation')
# Complete genuine preparation transcript, provided by root; no subject execution here.
tp=root/'GENUINE_PREPARATION_TOOL.json';verify(dict(path=str(tp),bytes=3008,sha256='f6beeef17d2e2fa6e3ed4be42eb0deb199798f2b0833829e6d46d8118c52bbe4'));transcript=load(tp)
equal(sorted(transcript),['initial','polls','schema','status'],'closed prep transcript')
equal([transcript['schema'],transcript['status']],['ri224-root-genuine-preparation-tool-v1','PREPARED_NOT_ADMITTED_OR_DISPATCHED'],'transcript scope')
command='/opt/homebrew/bin/python3 -I -B '+str(prep_source)+' --source-review-bytes 2307 --source-review-sha256 ae31240d4d29b7ccefd28cf8b75d908be318eb1bd3b94fd46aa698dc7398f5bd --host-transcript '+str(host_input)+' --host-transcript-bytes 1552 --host-transcript-sha256 1b2da050aa672834d0777603efc70d2b07019aea4254999d4f2df59d7344b6ae'
initial=transcript['initial'];equal(initial['arguments'],dict(cmd=command,workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=2600,sandbox_permissions='require_escalated',justification='Run the independently reviewed administrative preparation once with isolated/no-bytecode flags, creating nine exact preparation files and two fresh directories only; do not issue admission or execute installation.'),'whole actual preparation invocation including caller flags')
equal([initial['result']['chunk_id'],initial['result']['session_id'],initial['result']['output']],['bb233e',14557,''],'real initial pending session');require(initial['result'].get('exit_code') is None,'initial is not completed')
require(len(transcript['polls'])==1,'exact single saved terminal poll');terminal=transcript['polls'][0]
equal(terminal['arguments'],dict(session_id=14557,chars='',yield_time_ms=1000,max_output_tokens=2600),'complete actual terminal arguments');equal([terminal['result']['chunk_id'],terminal['result']['exit_code']],['581cd9',0],'genuine preparation terminal');require('session_id' not in terminal['result'],'completed real session')
printed=json.loads(terminal['result']['output']);equal(printed,dict(status='PREPARED_FOR_ROOT_PREFLIGHT_REVIEW_NO_ADMISSION',proposal=ref(D/'INSTALLATION_PROPOSAL.json'),custody=ref(D/'PREPARATION_CUSTODY.json'),exact_tool_arguments=dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000)),'complete printed values versus saved files')
# Retain the actual failed predecessor, without replaying its installer or audit.
oldfailed=B/'ri221-root-installation-ru2v15ie';fc=load(oldfailed/'POST_FAILURE_CUSTODY.json')
for row in [fc['admission'],fc['dispatch']]+fc['monitor_files']:equal(identity(row['path']),row,'old failed operation selection unchanged')
for p in fc['operation_and_mode_absences']:require(not os.path.lexists(p),'old refused/absent operation remains absent')
# Failure evidence from old reservation remains preserved and unresumed.
failure=load(B/'ri217-root-native-witness-1yj1_b61/PREPARATION_FAILURE_PARTIALS.json');equal(identity(failure['genuine_host']['path']),failure['genuine_host'],'prior partial host state')
for row in failure['empty_control_directories']:
 p=Path(row['path']);equal(state(p.lstat()),row['state'],'prior partial control state');equal(sorted(x.name for x in p.iterdir()),row['entries'],'prior empty directory')
equal(sorted(x.name for x in (B/'ri213-freeze-clock-repair-2xc_b29x').iterdir()),failure['reservation_namespace'],'prior failure exact namespace')
# Final administrative boundary check; no operation has occurred during review.
equal(sorted(x.name for x in D.iterdir()),expected_namespace,'unchanged complete preparation namespace')
for p in (O,D/'ADMIT_INSTALL.json',D/'DISPATCH.json',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json'):require(not os.path.lexists(p),'final unissued boundary')
result=dict(schema='ri224-independent-concrete-preparation-check-v1',status='PASS_CONCRETE_PREPARATION_READY_FOR_ROOT_FRESH_PREDISPATCH_AND_SEPARATE_ADMISSION',predicates=checks,distinct_identities=len(identities),identities=sorted(identities.values(),key=lambda r:r['path']),source_count=904,vendor_files=1810,vendor_bytes=48024515,tools=4,supplier_namespace=195,supplier_absences=2,E_files=48,E_directories=9,full_preflight_reconstructed=True,full_custody_reconstructed=True,full_unissued_proposal_reconstructed=True,whole_bootstrap_reconstructed=True,complete_cwd_relation_reconstructed=True,source_invocation_condition_met=True,genuine_host_chunk='343dae',genuine_prep_initial='bb233e',genuine_prep_terminal='581cd9',genuine_tool_origin_external=True,reviewer_subject_execution=False,admission_or_E_mutation=False,scientific_decode=False,preparation_scope_only=True,errors=[])
body=c(result)
with (R/'CHECK_RESULT.json').open('xb') as f:require(f.write(body)==len(body),'review result full write');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(result=dict(path=str(R/'CHECK_RESULT.json'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest()),predicates=result['predicates'],distinct_identities=result['distinct_identities'],status=result['status'])))
