"""RI219 independent administrative-only reconstruction. No subject imports/runs.
Opaque file hashing, fixed namespace checks and saved administrative JSON only.
"""
from pathlib import Path
import json,hashlib,os,stat,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri218-freeze-byte-repair-x62withm';W=D/'worker_proposal';R=Path(__file__).resolve().parent;OLD=B/'ri206-root-freeze-5e_n5lj_';E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri218-freeze-install-operation-x62withm'
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
 v=dict(path=str(p),resolved_path=str(p),symlink_chain=[],bytes=n,sha256=h.hexdigest(),state=state(s));identities[str(p)]=v;return v

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
for name,size,sha in [('ROOT_SOURCE_REVIEW.json',2333,'88f7f89ca9738eb52fb09fb2dee81400a7ad754e55a613de4df7f826d5f5bd2a'),('INSTALLATION_PROPOSAL.json',4521,'4b5185ed7f576a833ef0a18abb28c6fba5491c9002423e3e0f03121b10fb3a5e'),('PREPARATION_CUSTODY.json',13814,'0e360bd2dd0859ce37198056e42de2d7c310fb2212dabc40ef045f805e82770f'),('INSTALL_BOOTSTRAP.py',2417,'76779aeb180fc09ef2c90a2c1341ff3f5285640645ac15e1d90b27014422a00a')]:verify(dict(path=str(D/name),bytes=size,sha256=sha))
review=load(D/'ROOT_SOURCE_REVIEW.json');proposal=load(D/'INSTALLATION_PROPOSAL.json');custody=load(D/'PREPARATION_CUSTODY.json');pre=load(D/'INSTALL_PREFLIGHT.json');manifest=load(W/'SOURCE_PINS.json');hand=load(W/'HANDOFF.json')
equal(review['subject'],ref(W/'HANDOFF.json'),'accepted entire source seal');equal(review['source_manifest'],ref(W/'SOURCE_PINS.json'),'source manifest acceptance');equal(review['status'],'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY','compatible source status');require(review['installation_admitted'] is False and review['scientific_execution'] is False and review['qualification_credit']==0,'source authority boundary')
equal(sorted(x.name for x in W.iterdir()),hand['namespace'],'source seal namespace')
packet=[verify(x) for x in hand['files']]+[identity(W/'HANDOFF.json')]
support=[verify(review[k]) for k in ('independent_review','root_metadata')]
# Keep every prior independent source-review payload immutable, not merely its handoff.
review_hand=readref(review['independent_review']);equal(sorted(x.name for x in Path(review['independent_review']['path']).parent.iterdir()),review_hand['namespace'],'old review namespace')
for row in review_hand['files']:verify(row)
inputs=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');graph=readref(inputs['roles']['graph']);history=readref(inputs['roles']['historical_supplier']);oldE=readref(inputs['roles']['historical_E'])
equal([len(inputs['files']),len(repair['files']),inputs['prior_role_count'],len(inputs['prior_role_rows']),len(graph['copied_files']),len(graph['history_originals']),len(graph['sources'])],[806,43,810,810,48,124,30],'full retained domains')
source_refs={}
for row in inputs['files']+repair['files']+manifest['files']+[ref(W/'SOURCE_PINS.json'),ref(D/'ROOT_SOURCE_REVIEW.json'),ref(D/'INSTALL_BOOTSTRAP.py')]:
 z=pin(row)
 if z['path'] in source_refs:equal(source_refs[z['path']],z,'nonconflicting source alias')
 source_refs[z['path']]=z
equal(len(source_refs),857,'closed current source union')
sources=load(D/'SOURCES_BEFORE.json');equal([r['path'] for r in sources],sorted(source_refs),'every sorted source path');equal(len(sources),857,'all857')
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
host_input=Path('/private/tmp/ri219_host_before_transcript.json');host_original=load(host_input);canonical_host=load(D/'HOST_GENUINE_TOOL.json');equal(canonical_host,host_original,'complete host original/value');require((D/'HOST_GENUINE_TOOL.json').read_bytes()==c(host_original),'exact canonical host bytes')
equal(host_original['schema'],'ri219-root-genuine-host-tool-transcript-v1','fresh host schema');equal(host_original['result']['chunk_id'],'00c800','root provided genuine host event');require(type(host_original['result']['exit_code']) is int and host_original['result']['exit_code']==0 and 'session_id' not in host_original['result'],'host genuine zero')
obs=host_original['observation'];equal(json.loads(host_original['result']['output']),obs,'entire real host stdout');equal(obs,dict(command=history['host']['argv'],environment={'PATH':'/usr/bin:/bin','LC_ALL':'C'},returncode=0,stdout=history['host']['stdout'],stderr='',uname=history['host']['uname']),'whole host observation')
host=load(D/'HOST_BEFORE.json');equal(host,dict(schema='ri209-root-host-command-record-v1',**obs,genuine_tool=ref(D/'HOST_GENUINE_TOOL.json')),'whole host wrapper')
# Bootstrap is reconstructed as plain text, never evaluated.
changes=[['# One root-admitted administrative freeze-candidate action; unchanged RI141 child monitor.','# One root-admitted administrative installation; unchanged RI141 child monitor.'],[str(OLD/'tmp'),str(D/'tmp')],['ri206_whole_unchanged_ri141_freeze_monitor','ri219_whole_unchanged_ri141_install_monitor'],[str(B/'ri160-white-fixture-custody-repair-ufok1zpo/adapter.py'),str(W/'install_freeze.py')],[str(OLD/'ADMIT_FREEZE_CANDIDATE.json'),str(D/'ADMIT_INSTALL.json')],[str(OLD/'monitor'),str(D/'monitor')],["'FREEZE', 180, expected_environment)","'INSTALL', 180, expected_environment)"]]
bootstrap=(OLD/'FREEZE_BOOTSTRAP.py').read_text()
for before,after in changes:require(bootstrap.count(before)==1,'unique literal bootstrap replacement');bootstrap=bootstrap.replace(before,after)
require(bootstrap.encode()==(D/'INSTALL_BOOTSTRAP.py').read_bytes(),'complete seven-substitution bootstrap')
equal(pre,dict(schema='ri209-root-installation-preflight-v1',status='FRESH_EXACT_INSTALLATION_PREFLIGHT',sources=ref(D/'SOURCES_BEFORE.json'),supplier=ref(D/'SUPPLIER_BEFORE.json'),E_before=ref(D/'E_BEFORE.json'),host_tool_receipts=ref(D/'HOST_BEFORE.json'),monitor_bootstrap=ref(D/'INSTALL_BOOTSTRAP.py'),source_manifest=ref(W/'SOURCE_PINS.json'),environment=env,scientific_execution=False),'all ten preflight fields')
card=dict(schema='ri209-root-freeze-installation-admission-v1',status='AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION',source_manifest=ref(W/'SOURCE_PINS.json'),source_review=ref(D/'ROOT_SOURCE_REVIEW.json'),preflight=ref(D/'INSTALL_PREFLIGHT.json'),output=str(O),environment=env,limits=limits,genuine_outer_required=True)
card_bytes=c(card);prospective=dict(path=str(D/'ADMIT_INSTALL.json'),bytes=len(card_bytes),sha256=hashlib.sha256(card_bytes).hexdigest())
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
argv=['/usr/bin/env','-i',*[k+'='+v for k,v in env.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',VENDOR,'-I','-B',str(D/'INSTALL_BOOTSTRAP.py')]
dispatch=dict(outer_argv=argv,shell_command=shlex.join(argv),cwd=str(D),login=False,admission=prospective,bootstrap=ref(D/'INSTALL_BOOTSTRAP.py'),monitor_source=ref(B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),external_timeout_seconds=960,single_attempt=True,actual_execution_not_yet_started=True)
equal(proposal,dict(schema='ri219-unissued-installation-proposal-v1',status='UNISSUED_REQUIRES_ROOT_PREFLIGHT_REVIEW',proposed_admission=card,prospective_admission_pin=prospective,proposed_dispatch=dispatch,active_card_created=False,dispatch_created=False),'whole unissued proposal, nine card fields, ten dispatch fields')
prep_source=B/'ri219-root-obstruction-review-la4j_k0f/prepare_installation.py';equal(ref(prep_source),dict(path=str(prep_source),bytes=16552,sha256='49373e6ccc56f6aed7101834f3d635cef5e8f04978dd5099656e89de86ddfc34'),'exact executed administrative source pin')
equal(custody,dict(schema='ri219-root-preparation-custody-v1',status='PREPARED_NOT_ADMITTED_OR_DISPATCHED',sealed_source_packet=packet,root_review_support=support,original_genuine_host=ref(host_input),canonical_genuine_host=ref(D/'HOST_GENUINE_TOOL.json'),monitor_template=ref(OLD/'FREEZE_BOOTSTRAP.py'),bootstrap_replacements=changes,source_domain=857,prior_roles=810,copy_history_targets=[48,124,30],source_observations=ref(D/'SOURCES_BEFORE.json'),supplier_observation=ref(D/'SUPPLIER_BEFORE.json'),E_observation=ref(D/'E_BEFORE.json'),preflight=ref(D/'INSTALL_PREFLIGHT.json'),unissued_proposal=ref(D/'INSTALLATION_PROPOSAL.json'),preparation_source=ref(prep_source),tool_origin_and_startup_are_root_premises=True,scientific_execution=False,installation_admitted=False,installation_dispatched=False,ret_paused=True),'entire 23-field preparation custody')
# Retained complete administrative execution transcript; actual tool origin supplied by root.
tp=Path('/private/tmp/ri219_preparation_tool_transcript.json');transcript=load(tp);ref(tp)
equal(sorted(transcript),['initial','schema','terminal'],'complete prep transcript schema');equal(transcript['schema'],'ri219-genuine-preparation-tool-transcript-v1','prep schema')
command='/opt/homebrew/bin/python3 -I -B '+str(prep_source)+' --source-review-bytes 2333 --source-review-sha256 88f7f89ca9738eb52fb09fb2dee81400a7ad754e55a613de4df7f826d5f5bd2a --host-transcript '+str(host_input)+' --host-transcript-bytes 1571 --host-transcript-sha256 c79b992eef164650580bcbbeb211864f0c80a477489e3bb4ed14b61418e1bcac'
initial=transcript['initial'];terminal=transcript['terminal'];equal(initial['arguments']['cmd'],command,'whole admitted administrative invocation');equal(initial['arguments']['yield_time_ms'],1000,'prep initial wait');equal(initial['arguments']['max_output_tokens'],3000,'prep output bound')
equal([initial['result']['chunk_id'],initial['result']['session_id']],['7f1c8b',51547],'genuine initial session');require(initial['result'].get('exit_code') is None,'initial not terminal');equal(terminal['arguments'],dict(session_id=51547,chars='',yield_time_ms=1000,max_output_tokens=3000),'same actual terminal session');equal([terminal['result']['chunk_id'],terminal['result']['exit_code'],terminal['result']['output']],['633d20',0,''],'terminal genuine success');require('session_id' not in terminal['result'],'no ongoing session')
printed=json.loads(initial['result']['output']);equal(printed,dict(status='PREPARED_FOR_ROOT_PREFLIGHT_REVIEW_NO_ADMISSION',proposal=ref(D/'INSTALLATION_PROPOSAL.json'),custody=ref(D/'PREPARATION_CUSTODY.json'),exact_tool_arguments=dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000)),'every stdout summary field against actual artifacts')
# Failure evidence from old reservation remains preserved and unresumed.
failure=load(B/'ri217-root-native-witness-1yj1_b61/PREPARATION_FAILURE_PARTIALS.json');equal(identity(failure['genuine_host']['path']),failure['genuine_host'],'prior partial host state')
for row in failure['empty_control_directories']:
 p=Path(row['path']);equal(state(p.lstat()),row['state'],'prior partial control state');equal(sorted(x.name for x in p.iterdir()),row['entries'],'prior empty directory')
equal(sorted(x.name for x in (B/'ri213-freeze-clock-repair-2xc_b29x').iterdir()),failure['reservation_namespace'],'prior failure exact namespace')
# Final administrative boundary check; no operation has occurred during review.
equal(sorted(x.name for x in D.iterdir()),expected_namespace,'unchanged complete preparation namespace')
for p in (O,D/'ADMIT_INSTALL.json',D/'DISPATCH.json',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json'):require(not os.path.lexists(p),'final unissued boundary')
result=dict(schema='ri219-independent-concrete-preparation-check-v1',status='PASS_CONCRETE_PREPARATION_READY_FOR_ROOT_FRESH_PREDISPATCH_AND_SEPARATE_ADMISSION',predicates=checks,distinct_identities=len(identities),identities=sorted(identities.values(),key=lambda r:r['path']),source_count=857,vendor_files=1810,vendor_bytes=48024515,tools=4,supplier_namespace=195,supplier_absences=2,E_files=48,E_directories=9,full_preflight_reconstructed=True,full_custody_reconstructed=True,full_unissued_proposal_reconstructed=True,whole_bootstrap_reconstructed=True,genuine_host_chunk='00c800',genuine_prep_initial='7f1c8b',genuine_prep_terminal='633d20',genuine_tool_origin_external=True,reviewer_subject_execution=False,admission_or_E_mutation=False,scientific_decode=False,preparation_scope_only=True,errors=[])
body=c(result)
with (R/'CHECK_RESULT.json').open('xb') as f:require(f.write(body)==len(body),'review result full write');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(result=dict(path=str(R/'CHECK_RESULT.json'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest()),predicates=result['predicates'],distinct_identities=result['distinct_identities'],status=result['status'])))
