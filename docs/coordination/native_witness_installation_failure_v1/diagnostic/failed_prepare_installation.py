"""SOURCE-ONLY RI217 root preparation draft. Do not run before root review.

Author: /root/ri116_complete_caller_review, also RI209/213 installer author;
this is preparation assistance, not an independent source acceptance.
Future execution is administrative only. It imports only the exact retained
root metadata helper, never installer, checker, monitor, vendor or scientific
sources. Future writes are exclusive and confined to the fixed D213 root.
It creates no E member or operation directory and dispatches no command.
Root owns genuine transcript origin, bootstrap trust, admission and execution.
Keep partials and the actual preparation failure; never rerun in place.
"""
import hashlib, importlib.util, json, os, shlex, stat, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri213-freeze-clock-repair-2xc_b29x';W=D/'worker_proposal'
OLD=B/'ri206-root-freeze-5e_n5lj_'
E=B/'ri154-white-execution-proposed-42_uvw15'
O=B/'ri213-freeze-install-operation-2xc_b29x'
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
LIMITS=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864)
def ref(path,n,sha):return dict(path=str(path),bytes=n,sha256=sha)
MANIFEST=ref(W/'SOURCE_PINS.json',1372,'1608ecb0332a964c3726d87fab41d009ed6a74dc01f4c0e2001424b0eff6354e')
HANDOFF=ref(W/'HANDOFF.json',7600,'f8e4ab402fe4621352c7fe1f9b3d3bfeb6d5bc1194afcc7fb98cf34f8eb2f512')
REVIEW=ref(B/'ri215-root-margin-review-a1inhpxr/RI213_ROOT_SOURCE_REVIEW.json',2606,'55ac3d5a93fa4d3dc6d7326c76d1d11eb4c7b9ed4266ad3675728b4344ea20c6')
TEMPLATE=ref(OLD/'FREEZE_BOOTSTRAP.py',2401,'ddc3b0f906130d036777250055bf1cc088c194dd888c76a4f9a20d9add54e319')
MONITOR=ref(B/'ri141-white-bootstrap-source-h58ls076/prepare.py',45721,'8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe')
HOST_INPUT=ref('/private/tmp/ri217_host_before_transcript.json',1893,'708a0963e35fe66c504c0fd2b93a11711c0ba7ae5a57b1b5f61b028441ca211b')
HELPER=ref(B/'ri122-root-execution-review-6whn_vky/metadata.py',3144,'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7')
def need(ok,msg):
 if not ok:raise ValueError('RI217_PREP: '+msg)
h=Path(HELPER['path']);raw=h.read_bytes()
need(len(raw)==HELPER['bytes'] and hashlib.sha256(raw).hexdigest()==HELPER['sha256'],'retained administrative helper pin')
s=importlib.util.spec_from_file_location('ri217_root_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
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
need(not os.path.lexists(O) and not os.path.lexists(E/'AUTHORIZED_FREEZE.json'),'fresh operation and absent freeze')
for name in ('ADMIT_NORMAL.json','ADMIT_OPTIMIZED.json'):need(not os.path.lexists(E/name),'no scientific mode card')
output_names=['HOST_GENUINE_TOOL.json','HOST_BEFORE.json','INSTALL_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','INSTALL_PREFLIGHT.json','INSTALLATION_PROPOSAL.json','PREPARATION_CUSTODY.json']
for name in output_names+['tmp','monitor','ADMIT_INSTALL.json','DISPATCH.json']:need(not os.path.lexists(D/name),'no retry or replacement '+name)
hand=load(HANDOFF);eq(sorted(p.name for p in W.iterdir()),sorted(hand['namespace']),'entire sealed15 namespace')
need(len(hand['files'])==14 and len(hand['namespace'])==15,'whole sealed packet')
packet=[opaque(r) for r in hand['files']]+[opaque(HANDOFF)]
manifest=load(MANIFEST);eq(manifest['status'],'SOURCE_ONLY_NOT_ADMISSION','manifest status')
eq([Path(r['path']).name for r in manifest['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'five ordered payloads')
review=load(REVIEW);eq(review['source_manifest'],MANIFEST,'actual source acceptance pin');eq(review['subject'],HANDOFF,'actual accepted whole packet')
eq(review['status'],'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY','actual source acceptance status')
review_support=[opaque(review[k]) for k in ('independent_review','root_metadata')]
inputs=load(manifest['files'][0]);repair=load(manifest['files'][2]);need(len(inputs['files'])==806 and len(repair['files'])==19,'806+19 preserved declared inputs')
g=load(inputs['roles']['graph']);history=load(inputs['roles']['historical_supplier']);old_E=load(inputs['roles']['historical_E'])
need(len(g['copied_files'])==48 and len(g['history_originals'])==124 and len(g['sources'])==30,'all48/124/30 roles')
eq(g['prospective_root'],str(E),'literal E')
accepted=load(inputs['roles']['candidate_acceptance']);eq(accepted['status'],'ACCEPT_COMPLETE_ADMINISTRATIVE_FREEZE_CANDIDATE','actual candidate acceptance')
eq(accepted['result'],inputs['roles']['result'],'complete accepted candidate')
need(accepted['candidate_is_complete_canonical_result'] is True and accepted['freeze_installed'] is False,'candidate scope, never installation credit')
# Genuine observation came from root tool50ecd4, not a subprocess invented here.
host_original_state=opaque(HOST_INPUT);host_transcript=load(HOST_INPUT);eq(host_transcript['schema'],'ri217-root-genuine-host-tool-transcript-v1','actual root host transcript schema')
eq(host_transcript['result']['chunk_id'],'50ecd4','genuine root-host event')
need(type(host_transcript['result']['exit_code']) is int and host_transcript['result']['exit_code']==0 and 'session_id' not in host_transcript['result'],'genuine completed host event')
observation=host_transcript['observation'];eq(json.loads(host_transcript['result']['output']),observation,'entire observation versus real stdout')
need(set(observation)=={'command','environment','returncode','stdout','stderr','uname'},'closed original host observation')
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
   need(identity['resolved_path']==str(p) and identity['symlink_chain']==[],'literal E member');total+=identity['bytes'];need(total<=536870912,'tree total cap');row.update(kind='file',identity=identity)
  rows.append(row)
  if row['kind']=='directory':
   for name in row['entries']:visit(p/name,depth+1)
   eq(sorted(x.name for x in p.iterdir()),row['entries'],'E membership stable')
  eq(state(p.lstat()),state(a),'E selection stable')
 visit(E,0);return sorted(rows,key=lambda r:r['relative'])
etree=tree();eq(etree,sorted(old_E,key=lambda r:r['relative']),'whole unchanged accepted E baseline')
need(len(etree)==57 and sum(r['kind']=='file' for r in etree)==48,'E48 files nine directories')
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
bootstrap=Path(TEMPLATE['path']).read_text()
changes=[('# One root-admitted administrative freeze-candidate action; unchanged RI141 child monitor.','# One root-admitted administrative installation; unchanged RI141 child monitor.'),(str(OLD/'tmp'),str(D/'tmp')),('ri206_whole_unchanged_ri141_freeze_monitor','ri217_whole_unchanged_ri141_install_monitor'),(str(B/'ri160-white-fixture-custody-repair-ufok1zpo/adapter.py'),str(W/'install_freeze.py')),(str(OLD/'ADMIT_FREEZE_CANDIDATE.json'),str(D/'ADMIT_INSTALL.json')),(str(OLD/'monitor'),str(D/'monitor')),("'FREEZE', 180, expected_environment)","'INSTALL', 180, expected_environment)")]
for old,new in changes:need(bootstrap.count(old)==1,'exact one bootstrap replacement');bootstrap=bootstrap.replace(old,new)
need(repr(ENV) in bootstrap,'whole literal environment')
# All writes below are root-preparation outputs only; first failure stops and
# partial files/directories remain. No installer action has been dispatched.
def emit(name,data):
 need(name in output_names and type(data) is bytes and len(data)<=67108864,'exclusive output whitelist and bound')
 p=D/name
 with p.open('xb') as f:
  n=f.write(data);need(n==len(data),'complete administrative write');f.flush();os.fsync(f.fileno())
 eq(p.read_bytes(),data,'saved preparation bytes');return m.ref(p)
def save(name,value):return emit(name,m.canonical(value))
(D/'tmp').mkdir(mode=0o700);(D/'monitor').mkdir(mode=0o700)
host_raw=save('HOST_GENUINE_TOOL.json',host_transcript)
host=save('HOST_BEFORE.json',dict(schema='ri209-root-host-command-record-v1',**observation,genuine_tool=host_raw))
boot=emit('INSTALL_BOOTSTRAP.py',bootstrap.encode())
expected={}
for row in inputs['files']+repair['files']+manifest['files']+[MANIFEST,REVIEW,boot]:
 prior=expected.get(row['path']);need(prior is None or m.pure(prior)==m.pure(row),'same-path source declarations agree');expected[row['path']]=row
need(len(expected)==833,'closed actual source domain833')
sources=[opaque(expected[path]) for path in sorted(expected)]
source_ref=save('SOURCES_BEFORE.json',sources)
supplier=dict(absent=history['absent'],environment=ENV,host=dict(argv=observation['command'],exit_code=observation['returncode'],stdout=observation['stdout'],stderr=observation['stderr'],uname=observation['uname']),namespace=namespace,observed_at_unix_ns=time.time_ns(),tools=tools,vendor=vendor)
eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in history.items() if k not in ('environment','observed_at_unix_ns')},'complete inherited supplier scope')
supplier_ref=save('SUPPLIER_BEFORE.json',supplier);E_ref=save('E_BEFORE.json',etree)
# Recheck complete observations at the end of preparation; root still performs
# immediate fresh predispatch checks and genuine post-operation host capture.
for row in sources+vendor+tools+packet+review_support+[host_original_state]:eq(m.identity(row['path']),row,'fresh complete selection retained')
for row in namespace:
 p=Path(row['path']);eq(state(p.lstat()),row['state'],'namespace state retained')
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'],'namespace members retained')
 else:eq(os.readlink(p),row['target'],'namespace link retained')
need(all(not os.path.lexists(p) for p in history['absent']),'absences retained');eq(tree(),etree,'whole E still unchanged')
opaque(HOST_INPUT);need(not os.path.lexists(O) and not os.path.lexists(E/'AUTHORIZED_FREEZE.json'),'unowned operation and freeze still absent')
for name in ('tmp','monitor'):need(list((D/name).iterdir())==[],'empty administrative control directory')
pre=save('INSTALL_PREFLIGHT.json',dict(schema='ri209-root-installation-preflight-v1',status='FRESH_EXACT_INSTALLATION_PREFLIGHT',sources=source_ref,supplier=supplier_ref,E_before=E_ref,host_tool_receipts=host,monitor_bootstrap=boot,source_manifest=MANIFEST,environment=ENV,scientific_execution=False))
proposed_card=dict(schema='ri209-root-freeze-installation-admission-v1',status='AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION',source_manifest=MANIFEST,source_review=REVIEW,preflight=pre,output=str(O),environment=ENV,limits=LIMITS,genuine_outer_required=True)
card=ref(D/'ADMIT_INSTALL.json',len(m.canonical(proposed_card)),hashlib.sha256(m.canonical(proposed_card)).hexdigest())
outer=['/usr/bin/env','-i',*[k+'='+v for k,v in ENV.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',VENDOR,'-I','-B',str(D/'INSTALL_BOOTSTRAP.py')]
proposed_dispatch=dict(outer_argv=outer,shell_command=shlex.join(outer),cwd=str(D),login=False,admission=card,bootstrap=boot,monitor_source=MONITOR,external_timeout_seconds=960,single_attempt=True,actual_execution_not_yet_started=True)
proposal=save('INSTALLATION_PROPOSAL.json',dict(schema='ri217-unissued-installation-proposal-v1',status='UNISSUED_REQUIRES_ROOT_PREFLIGHT_REVIEW',proposed_admission=proposed_card,prospective_admission_pin=card,proposed_dispatch=proposed_dispatch,active_card_created=False,dispatch_created=False))
custody=save('PREPARATION_CUSTODY.json',dict(schema='ri217-root-preparation-custody-v1',status='PREPARED_NOT_ADMITTED_OR_DISPATCHED',sealed_source_packet=packet,root_review_support=review_support,original_genuine_host=HOST_INPUT,canonical_genuine_host=host_raw,monitor_template=TEMPLATE,bootstrap_replacements=changes,source_domain=833,prior_roles=inputs['prior_role_count'],copy_history_targets=[48,124,30],source_observations=source_ref,supplier_observation=supplier_ref,E_observation=E_ref,preflight=pre,unissued_proposal=proposal,preparation_source=m.ref(Path(__file__).resolve()),tool_origin_and_startup_are_root_premises=True,scientific_execution=False,installation_admitted=False,installation_dispatched=False,ret_paused=True))
print(json.dumps(dict(status='PREPARED_FOR_ROOT_PREFLIGHT_REVIEW_NO_ADMISSION',proposal=proposal,custody=custody,exact_tool_arguments=dict(cmd=shlex.join(outer),workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000))))
