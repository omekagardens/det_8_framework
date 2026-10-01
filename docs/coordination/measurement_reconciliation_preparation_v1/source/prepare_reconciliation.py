"""SOURCE-ONLY RI229 root read-only reconciliation preparation writer. Do not run before root review.

Author: /root/ri116_complete_caller_review, also RI209/213/218/222 installer and RI226 recovery author;
this is preparation assistance, not an independent source acceptance.
Future execution is administrative only. It imports only the exact retained
root metadata helper, never installer, checker, monitor, vendor or scientific
sources. Future writes are exclusive and confined to the fixed D226 root; the existing accepted review/source remains untouched.
It creates no E member or operation directory and dispatches no command.
Root owns genuine transcript origin, bootstrap trust, admission and execution.
Keep partials and the actual preparation failure; never rerun in place.
"""
import argparse, hashlib, importlib.util, json, os, shlex, stat, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri226-directory-custody-recovery-yvfg_p1b';W=D/'worker_proposal'
PW=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal'
OLD=B/'ri206-root-freeze-5e_n5lj_'
E=B/'ri154-white-execution-proposed-42_uvw15'
O=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
LIMITS=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864)
def ref(path,n,sha):return dict(path=str(path),bytes=n,sha256=sha)
MANIFEST={'bytes': 1412, 'path': '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/worker_proposal/SOURCE_PINS.json', 'sha256': '83c1c226126113aacefe71b049be0113a1088ed6f1ca439534cae418b040fb0f'}
HANDOFF={'bytes': 9657, 'path': '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/worker_proposal/HANDOFF.json', 'sha256': 'bead93928f1f1af37379f4d8add4c5e254b31633fa8d00acb274a2739d237fdc'}
REVIEW={'bytes': 2289, 'path': '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/ROOT_SOURCE_REVIEW.json', 'sha256': '4fdaddb780e94c2dbf0f4773d4301439421ef80586482535ec7b0842fc2c40f6'}
DEPENDENCIES={'path': '/Volumes/AI_DATA/development/det-review-evidence/ri229-reconciliation-preparation-t93t1607/worker_proposal/DEPENDENCIES.json', 'bytes': 250788, 'sha256': '0985323c819a7396189153bff0edccf0f3718b42efce27e29aa26442ceab1f2b'}
BOOTSTRAP_SOURCE={'path': '/Volumes/AI_DATA/development/det-review-evidence/ri229-reconciliation-preparation-t93t1607/worker_proposal/RECONCILE_BOOTSTRAP.source-only.py', 'bytes': 2454, 'sha256': '2621315b8a7bf8e57ce05e1a9da3e3f12d15d44d1ab6ef2f8e11dbf0a08acaba'}
# Root supplies actual, externally authenticated future pins after acceptance and
# a fresh genuine host call. Neither historical observation nor author source
# supplies its own authority. Exact root review path is fixed below.
arguments=argparse.ArgumentParser()
arguments.add_argument('--preparation-manifest-bytes',required=True,type=int)
arguments.add_argument('--preparation-manifest-sha256',required=True)
arguments.add_argument('--preparation-review',required=True)
arguments.add_argument('--preparation-review-bytes',required=True,type=int)
arguments.add_argument('--preparation-review-sha256',required=True)
arguments.add_argument('--host-transcript',required=True)
arguments.add_argument('--host-transcript-bytes',required=True,type=int)
arguments.add_argument('--host-transcript-sha256',required=True)
args=arguments.parse_args()
for n,digest in ((args.preparation_manifest_bytes,args.preparation_manifest_sha256),(args.preparation_review_bytes,args.preparation_review_sha256),(args.host_transcript_bytes,args.host_transcript_sha256)):
 if not (0<n<=67108864 and len(digest)==64 and set(digest)<=set('0123456789abcdef')):raise ValueError('RI229_PREP: invalid external root pin')
if not Path(args.host_transcript).is_absolute():raise ValueError('RI229_PREP: absolute genuine host transcript required')
if not Path(args.preparation_review).is_absolute():raise ValueError('RI229_PREP: absolute actual preparation-source review required')
PREP_MANIFEST=ref(PW/'SOURCE_PINS.json',args.preparation_manifest_bytes,args.preparation_manifest_sha256)
PREP_REVIEW=ref(args.preparation_review,args.preparation_review_bytes,args.preparation_review_sha256)
TEMPLATE=ref(OLD/'FREEZE_BOOTSTRAP.py',2401,'ddc3b0f906130d036777250055bf1cc088c194dd888c76a4f9a20d9add54e319')
MONITOR=ref(B/'ri141-white-bootstrap-source-h58ls076/prepare.py',45721,'8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe')
HOST_INPUT=ref(args.host_transcript,args.host_transcript_bytes,args.host_transcript_sha256)
HELPER=ref(B/'ri122-root-execution-review-6whn_vky/metadata.py',3144,'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7')
def need(ok,msg):
 if not ok:raise ValueError('RI229_PREP: '+msg)
h=Path(HELPER['path']);raw=h.read_bytes()
need(len(raw)==HELPER['bytes'] and hashlib.sha256(raw).hexdigest()==HELPER['sha256'],'retained administrative helper pin')
s=importlib.util.spec_from_file_location('ri229_root_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def eq(a,b,msg):need(m.canonical(a)==m.canonical(b),msg)
def opaque(row):
 value=m.identity(row['path']);eq(m.pure(value),m.pure(row),'exact opaque pin '+row['path']);return value

def load(row):
 initial=opaque(row);data=Path(row['path']).read_bytes();eq(m.pin(data),m.pure(row),'whole read pin')
 def pairs(rows):
  value={}
  for k,v in rows:need(k not in value,'duplicate metadata key');value[k]=v
  return value
 def bad(v):raise ValueError('nonfinite administrative JSON')
 value=json.loads(data,object_pairs_hook=pairs,parse_constant=bad)
 eq(m.identity(row['path']),initial,'read selection');return value

# No current supplier observation is claimed until this draft is actually run.
need(D.resolve()==D and D.is_dir() and not D.is_symlink(),'literal existing reservation')
need(not os.path.lexists(O),'fresh read-only operation')
for name in ('ADMIT_NORMAL.json','ADMIT_OPTIMIZED.json'):need(not os.path.lexists(E/name),'no scientific mode card')
output_names=['HOST_GENUINE_TOOL.json','HOST_BEFORE.json','RECONCILE_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','RECONCILE_PREFLIGHT.json','RECONCILIATION_PROPOSAL.json','PREPARATION_CUSTODY.json']
for name in output_names+['tmp','monitor','ADMIT_RECONCILE.json','DISPATCH.json']:need(not os.path.lexists(D/name),'no retry or replacement '+name)
root_namespace_before=sorted(p.name for p in D.iterdir())
prep_manifest=load(PREP_MANIFEST);need(set(prep_manifest)=={'schema','status','files'},'closed preparation source manifest');eq([prep_manifest['schema'],prep_manifest['status']],['ri229-preparation-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'preparation declaration only')
eq([Path(r['path']).name for r in prep_manifest['files']],['BOOTSTRAP_DIFF.patch','DEPENDENCIES.json','PROTOCOL.md','RECONCILE_BOOTSTRAP.source-only.py','prepare_reconciliation.py'],'entire ordered preparation source')
for r in prep_manifest['files']:need(Path(r['path']).parent==PW,'fixed preparation source path');opaque(r)
need(Path(__file__).resolve()==PW/'prepare_reconciliation.py','fixed reviewed writer source')
prep_decision=load(PREP_REVIEW);eq(prep_decision['source_manifest'],PREP_MANIFEST,'actual preparation review manifest');eq(prep_decision['status'],'ACCEPT_RI229_PREPARATION_SOURCE_ONLY','actual source review only');eq(prep_decision['recovery_source_review'],REVIEW,'exact accepted recovery source prerequisite')
preparation_support=[opaque(PREP_MANIFEST),opaque(PREP_REVIEW)]+[opaque(r) for r in prep_manifest['files']]
dependencies=load(DEPENDENCIES);dependency_states=[opaque(r) for r in dependencies['files']]
hand=load(HANDOFF);eq(sorted(p.name for p in W.iterdir()),sorted(hand['namespace']),'entire sealed19 recovery namespace')
need(len(hand['files'])==18 and len(hand['namespace'])==19,'whole sealed recovery packet')
packet=[opaque(r) for r in hand['files']]+[opaque(HANDOFF)]
manifest=load(MANIFEST);eq(manifest['status'],'SOURCE_ONLY_NOT_ADMISSION','manifest status')
eq([Path(r['path']).name for r in manifest['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py'],'five ordered payloads')
review=load(REVIEW);eq(review['source_manifest'],MANIFEST,'actual source acceptance pin');eq(review['packet'],HANDOFF,'actual accepted whole packet')
eq(review['status'],'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY','actual source acceptance status')
review_support=[opaque(review[k]) for k in ('independent_review','root_metadata_check','root_manual_review')]
inputs=load(manifest['files'][0]);repair=load(manifest['files'][2]);need(len(inputs['files'])==806 and len(repair['files'])==157,'806+157 preserved declared inputs')
g=load(inputs['roles']['graph']);history=load(inputs['roles']['historical_supplier']);original_E=load(inputs['roles']['historical_E']);retained_obs=load(repair['roles']['original_observations']);old_E=retained_obs['E_after'];old_complete=load(repair['roles']['original_complete']);postflight=load(repair['roles']['postflight']);original_before=load(repair['roles']['original_before']);supersession=load(repair['roles']['supersession'])
need(len(g['copied_files'])==48 and len(g['history_originals'])==124 and len(g['sources'])==30,'all48/124/30 roles')
eq(g['prospective_root'],str(E),'literal E')
eq(review['retained_failure'],repair['roles']['original_complete'],'root explicitly binds original refused complete');eq(review['retained_postflight'],repair['roles']['postflight'],'root explicitly binds whole postflight')
eq(old_complete['status'],'REFUSED_RETAIN_ALL_PARTIALS','actual old attempt remains refused');eq(old_complete['first_error'],dict(type='ValueError',message='RI209: root device inode mode links',secondary=[]),'exact retained first error');eq(supersession['status'],'OPERATIONAL_READINESS_SUPERSEDED_AFTER_ACTUAL_POSTWRITE_REFUSAL','old readiness remains superseded')
eq(sorted(original_E,key=lambda r:r['relative']),original_before['E'],'whole original prewrite E baseline')
old_by={r['relative']:r for r in original_before['E']};after_by={r['relative']:r for r in old_E}
need(len(old_by)==57 and len(after_by)==58 and set(after_by)==set(old_by)|{'AUTHORIZED_FREEZE.json'},'retained exact sole member addition')
eq(old_by['.'],postflight['root_before'],'entire historical before root');eq({k:after_by['.'][k] for k in ('state','entries')},postflight['root_after'],'entire retained resulting root');eq(old_by['.']['state'][:3],after_by['.']['state'][:3],'stable historical root device inode mode');eq([old_by['.']['state'][3],after_by['.']['state'][3]],[23,24],'exact pinned historical link transition');eq(after_by['.']['entries'],sorted(old_by['.']['entries']+['AUTHORIZED_FREEZE.json']),'sole historical root member addition')
for name,row in old_by.items():
 if name!='.':eq(after_by[name],row,'whole original member unchanged '+name)
eq(after_by['AUTHORIZED_FREEZE.json']['identity'],postflight['installed_partial'],'whole historical installed partial identity')
original_sources=load(repair['roles']['original_sources']);need(len(original_sources)==904,'all904 original full source identities');eq(original_sources,original_before['source_observations'],'whole original source baseline')
for row in original_sources+list(original_before['bindings'].values()):eq(m.identity(row['path']),row,'entire original selection retained before preparation')
original_output=Path(repair['roles']['original_complete']['path']).parent
eq(sorted(p.name for p in original_output.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'],'unchanged refused original namespace')
accepted=load(inputs['roles']['candidate_acceptance']);eq(accepted['status'],'ACCEPT_COMPLETE_ADMINISTRATIVE_FREEZE_CANDIDATE','actual candidate acceptance')
eq(accepted['result'],inputs['roles']['result'],'complete accepted candidate')
need(accepted['candidate_is_complete_canonical_result'] is True and accepted['freeze_installed'] is False,'candidate scope, never installation credit')
# Genuine host observation must come from the fresh root tool transcript, not
# a subprocess invented here or reuse of the historical RI217 or RI219 observation.
host_original_state=opaque(HOST_INPUT);host_transcript=load(HOST_INPUT);need(set(host_transcript)=={'schema','arguments','result','observation'},'closed genuine host transcript');eq(host_transcript['schema'],'ri229-root-genuine-host-tool-transcript-v1','actual root host transcript schema')
need(type(host_transcript['result']['chunk_id']) is str and len(host_transcript['result']['chunk_id'])>0,'retained genuine root-host event identifier')
need(type(host_transcript['result']['exit_code']) is int and host_transcript['result']['exit_code']==0 and 'session_id' not in host_transcript['result'],'genuine completed host event')
observation=host_transcript['observation'];eq(json.loads(host_transcript['result']['output']),observation,'entire observation versus real stdout')
need(set(observation)=={'command','environment','returncode','stdout','stderr','uname'},'closed original host observation');need(type(observation['returncode']) is int,'integer-preserving genuine returncode')
eq(observation,dict(command=history['host']['argv'],environment={'PATH':'/usr/bin:/bin','LC_ALL':'C'},returncode=0,stdout=history['host']['stdout'],stderr='',uname=history['host']['uname']),'complete host history and current genuine observation')
state=lambda a:[a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
def tree():
 rows=[];total=0
 def visit(p,depth):
  nonlocal total
  a=p.lstat();need(depth<=16 and len(rows)<25000 and not stat.S_ISLNK(a.st_mode),'bounded no-link E tree')
  row=dict(relative=str(p.relative_to(E)),state=state(a))
  if stat.S_ISDIR(a.st_mode):row.update(kind='directory',entries=sorted(x.name for x in p.iterdir()))
  else:
   need(stat.S_ISREG(a.st_mode) and a.st_size<=67108864,'bounded regular E member');identity=m.identity(p)
   need(identity['resolved_path']==str(p) and identity['symlink_chain']==[] and identity['state'][3]==1,'literal single-link E member');total+=identity['bytes'];need(total<=536870912,'tree total cap');row.update(kind='file',identity=identity)
  rows.append(row)
  if row['kind']=='directory':
   for name in row['entries']:visit(p/name,depth+1)
   eq(sorted(x.name for x in p.iterdir()),row['entries'],'E membership stable')
  eq(state(p.lstat()),state(a),'E selection stable')
 visit(E,0);return sorted(rows,key=lambda r:r['relative'])
etree=tree();eq(etree,sorted(old_E,key=lambda r:r['relative']),'whole unchanged accepted E baseline')
need(len(etree)==58 and sum(r['kind']=='file' for r in etree)==49 and sum(r['kind']=='directory' for r in etree)==9,'E49 files nine directories');eq(m.identity(E/'AUTHORIZED_FREEZE.json'),postflight['installed_partial'],'whole current existing freeze identity');candidate_row=inputs['roles']['result'];opaque(candidate_row);need((E/'AUTHORIZED_FREEZE.json').read_bytes()==Path(candidate_row['path']).read_bytes(),'complete retained candidate bytes');eq(m.identity(E/'AUTHORIZED_FREEZE.json'),postflight['installed_partial'],'freeze identity across byte reread')
for name in ('tmp','runs/normal','runs/optimized'):need(list((E/name).iterdir())==[],'empty unadmitted E path '+name)
vendor=[opaque(r) for r in history['vendor']];tools=[opaque(r) for r in history['tools']]
eq(vendor,history['vendor'],'all complete current vendor states');eq(tools,history['tools'],'all complete current tool states')
need(len(vendor)==1810 and sum(r['bytes'] for r in vendor)==48024515 and len(tools)==4,'unchanged supplier counts')
namespace=[]
for row in history['namespace']:
 p=Path(row['path']);a=p.lstat();actual=dict(path=str(p),kind=row['kind'],state=state(a))
 if row['kind']=='directory':need(stat.S_ISDIR(a.st_mode),'supplier directory');actual['entries']=sorted(x.name for x in p.iterdir())
 else:need(row['kind']=='symlink' and stat.S_ISLNK(a.st_mode),'supplier link');actual['target']=os.readlink(p)
 eq(actual,row,'whole current supplier namespace');eq(state(p.lstat()),state(a),'supplier namespace stable');namespace.append(actual)
need(len(namespace)==195 and len(history['absent'])==2 and all(not os.path.lexists(p) for p in history['absent']),'195 namespaces and two actual absences')
eq(list(os.uname()),observation['uname'],'current uname and real host command')
# Whole unchanged monitor is read only as bytes, never imported by preparation.
opaque(MONITOR);opaque(TEMPLATE)
opaque(BOOTSTRAP_SOURCE);bootstrap=Path(BOOTSTRAP_SOURCE['path']).read_text();eq(m.pin(bootstrap.encode()),m.pure(BOOTSTRAP_SOURCE),'complete pre-reviewed bootstrap text')
changes=[('# One root-admitted administrative freeze-candidate action; unchanged RI141 child monitor.', '# One root-admitted read-only reconciliation; unchanged RI141 child monitor.'), ('/Volumes/AI_DATA/development/det-review-evidence/ri206-root-freeze-5e_n5lj_/tmp', '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/tmp'), ('ri206_whole_unchanged_ri141_freeze_monitor', 'ri229_whole_unchanged_ri141_reconcile_monitor'), ('/Volumes/AI_DATA/development/det-review-evidence/ri160-white-fixture-custody-repair-ufok1zpo/adapter.py', '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/worker_proposal/reconcile_freeze.py'), ('/Volumes/AI_DATA/development/det-review-evidence/ri206-root-freeze-5e_n5lj_/ADMIT_FREEZE_CANDIDATE.json', '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/ADMIT_RECONCILE.json'), ('/Volumes/AI_DATA/development/det-review-evidence/ri206-root-freeze-5e_n5lj_/monitor', '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/monitor'), ("'FREEZE', 180, expected_environment)", "'RECONCILE', 180, expected_environment)")]
original_bootstrap=Path(TEMPLATE['path']).read_text()
for old,new in changes:need(original_bootstrap.count(old)==1,'exact one historical bootstrap adaptation');original_bootstrap=original_bootstrap.replace(old,new)
eq(bootstrap,original_bootstrap,'entire fixed bootstrap versus retained route')
need(repr(ENV) in bootstrap,'whole literal environment')
# The outer tool/bootstrap cwd is D. Unchanged child_run sets Popen cwd=out,
# so the reconciler cwd is the separate literal D/monitor. Verify this exact
# generated source interface without importing or executing either subject.
monitor_body=Path(MONITOR['path']).read_bytes();eq(m.pin(monitor_body),m.pure(MONITOR),'captured complete monitor source pin')
monitor_text=monitor_body.decode('ascii')
child_span=monitor_text[monitor_text.index('def child_run(command, out, label, seconds, env):'):monitor_text.index('def dyld_attempts(')]
expected_popen="child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,\n                                     cwd=out, env=env, start_new_session=True)"
need(child_span.count(expected_popen)==1 and 'chdir' not in child_span,'unchanged real monitor child cwd=out')
expected_child=[VENDOR,'-I','-B',str(W/'reconcile_freeze.py'),'--admission',str(D/'ADMIT_RECONCILE.json')]
expected_call='module.child_run('+repr(expected_child)+', Path('+repr(str(D/'monitor'))+"), 'RECONCILE', 180, expected_environment)"
need([line for line in bootstrap.splitlines() if line.startswith('module.child_run(')]==[expected_call],'generated child out is exactly literal D/monitor')
reconciler_body=Path(manifest['files'][4]['path']).read_bytes();eq(m.pin(reconciler_body),m.pure(manifest['files'][4]),'captured complete reconciler source pin')
expected_guard="need(Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W,'fixed operation paths')"
need(reconciler_body.decode('ascii').count(expected_guard)==1,'reconciler requires the inherited exact child cwd')
cwd_contract=dict(outer_cwd=str(D),child_cwd=str(D/'monitor'),monitor=MONITOR,exact_popen=expected_popen,generated_child_call=expected_call,reconciler=manifest['files'][4],reconciler_guard=expected_guard,source_text_only=True,subject_execution=False)
# All writes below are root-preparation outputs only; first failure stops and
# partial files/directories remain. No reconciliation action has been dispatched.
produced={}
def emit(name,data):
 need(name in output_names and type(data) is bytes and len(data)<=67108864,'exclusive output whitelist and bound')
 p=D/name;produced[name]=dict(path=str(p),**m.pin(data))
 with p.open('xb') as f:
  n=f.write(data);need(n==len(data),'complete administrative write');f.flush();os.fsync(f.fileno())
 need(p.read_bytes()==data,'saved preparation bytes');actual=m.ref(p);eq(actual,produced[name],'whole captured preparation output pin');return actual
def save(name,value):return emit(name,m.canonical(value))
(D/'tmp').mkdir(mode=0o700);(D/'monitor').mkdir(mode=0o700)
host_raw=save('HOST_GENUINE_TOOL.json',host_transcript)
host=save('HOST_BEFORE.json',dict(schema='ri209-root-host-command-record-v1',**observation,genuine_tool=host_raw))
boot=emit('RECONCILE_BOOTSTRAP.py',bootstrap.encode())
expected={}
for row in inputs['files']+repair['files']+manifest['files']+[MANIFEST,REVIEW,boot]:
 prior=expected.get(row['path']);need(prior is None or m.pure(prior)==m.pure(row),'same-path source declarations agree');expected[row['path']]=row
need(len(expected)==971,'closed actual source domain971')
sources=[opaque(expected[path]) for path in sorted(expected)]
source_ref=save('SOURCES_BEFORE.json',sources)
supplier=dict(absent=history['absent'],environment=ENV,host=dict(argv=observation['command'],exit_code=observation['returncode'],stdout=observation['stdout'],stderr=observation['stderr'],uname=observation['uname']),namespace=namespace,observed_at_unix_ns=time.time_ns(),tools=tools,vendor=vendor)
eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in history.items() if k not in ('environment','observed_at_unix_ns')},'complete inherited supplier scope')
supplier_ref=save('SUPPLIER_BEFORE.json',supplier);E_ref=save('E_BEFORE.json',etree)
# Recheck complete observations at the end of preparation; root still performs
# immediate fresh predispatch checks and genuine post-operation host capture.
for row in sources+vendor+tools+packet+review_support+preparation_support+dependency_states+original_sources+list(original_before['bindings'].values())+[host_original_state]:eq(m.identity(row['path']),row,'fresh complete selection retained')
for row in namespace:
 p=Path(row['path']);eq(state(p.lstat()),row['state'],'namespace state retained')
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'],'namespace members retained')
 else:eq(os.readlink(p),row['target'],'namespace link retained')
need(all(not os.path.lexists(p) for p in history['absent']),'absences retained');eq(tree(),etree,'whole E still unchanged')
eq(m.identity(HOST_INPUT['path']),host_original_state,'whole original host selection retained');need(not os.path.lexists(O),'unowned read-only operation');eq(m.identity(E/'AUTHORIZED_FREEZE.json'),postflight['installed_partial'],'same retained existing freeze')
for name in ('tmp','monitor'):need(list((D/name).iterdir())==[],'empty administrative control directory')
eq(sorted(p.name for p in original_output.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'],'original refused namespace retained after preparation reads')
pre=save('RECONCILE_PREFLIGHT.json',dict(schema='ri226-root-reconciliation-preflight-v1',status='FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT',sources=source_ref,supplier=supplier_ref,E_before=E_ref,host_tool_receipts=host,monitor_bootstrap=boot,source_manifest=MANIFEST,environment=ENV,scientific_execution=False))
proposed_card=dict(schema='ri226-root-read-only-reconciliation-admission-v1',status='AUTHORIZE_ONE_READ_ONLY_RECONCILIATION',source_manifest=MANIFEST,source_review=REVIEW,preflight=pre,output=str(O),environment=ENV,limits=LIMITS,genuine_outer_required=True)
# No future admission FilePin is invented. Root may later issue the actual card,
# freshly read its real identity, and add admission to the actual dispatch.
outer=['/usr/bin/env','-i',*[k+'='+v for k,v in ENV.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',VENDOR,'-I','-B',str(D/'RECONCILE_BOOTSTRAP.py')]
proposed_dispatch=dict(outer_argv=outer,shell_command=shlex.join(outer),cwd=str(D),login=False,bootstrap=boot,monitor_source=MONITOR,external_timeout_seconds=960,single_attempt=True,actual_execution_not_yet_started=True)
proposal=save('RECONCILIATION_PROPOSAL.json',dict(schema='ri229-unissued-reconciliation-proposal-v1',status='UNISSUED_REQUIRES_ROOT_PREFLIGHT_REVIEW',proposed_admission_fields=proposed_card,future_admission_path=str(D/'ADMIT_RECONCILE.json'),dispatch_fields_without_admission=proposed_dispatch,active_card_created=False,dispatch_created=False))
custody=save('PREPARATION_CUSTODY.json',dict(schema='ri229-root-preparation-custody-v1',status='PREPARED_NOT_ADMITTED_OR_DISPATCHED',sealed_source_packet=packet,root_review_support=review_support,preparation_source_manifest=PREP_MANIFEST,preparation_source_review=PREP_REVIEW,preparation_support=preparation_support,preparation_dependency_states=dependency_states,retained_failure=repair['roles']['original_complete'],retained_postflight=repair['roles']['postflight'],original_genuine_host=HOST_INPUT,canonical_genuine_host=host_raw,monitor_template=TEMPLATE,bootstrap_replacements=changes,cwd_contract=cwd_contract,source_domain=971,original_source_observation=repair['roles']['original_sources'],original_bindings=original_before['bindings'],root_namespace_before=root_namespace_before,root_namespace_expected_after=sorted(root_namespace_before+output_names+['tmp','monitor']),produced_before_custody=dict(produced),prior_roles=inputs['prior_role_count'],copy_history_targets=[48,124,30],source_observations=source_ref,supplier_observation=supplier_ref,E_observation=E_ref,preflight=pre,unissued_proposal=proposal,preparation_source=m.ref(Path(__file__).resolve()),tool_origin_and_startup_are_root_premises=True,scientific_execution=False,reconciliation_admitted=False,reconciliation_dispatched=False,E_read_only=True,ret_paused=True))
eq({name:m.ref(D/name) for name in produced},produced,'all nine actual preparation output pins');eq(sorted(p.name for p in D.iterdir()),sorted(root_namespace_before+output_names+['tmp','monitor']),'exact final preparation additions only')
for name in output_names:
 p=D/name;need(not p.is_symlink() and p.is_file() and p.stat().st_nlink==1 and p.stat().st_size<=67108864,'single-link bounded preparation output')
for name in ('tmp','monitor'):need(list((D/name).iterdir())==[],'final empty controls')
need(not os.path.lexists(O) and not os.path.lexists(D/'ADMIT_RECONCILE.json') and not os.path.lexists(D/'DISPATCH.json'),'no operational ownership or admission or dispatch');eq(tree(),etree,'final entire E unchanged after all preparation outputs')
print(json.dumps(dict(status='PREPARED_FOR_ROOT_PREFLIGHT_REVIEW_NO_ADMISSION',proposal=proposal,custody=custody,exact_tool_arguments=dict(cmd=shlex.join(outer),workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000))))
