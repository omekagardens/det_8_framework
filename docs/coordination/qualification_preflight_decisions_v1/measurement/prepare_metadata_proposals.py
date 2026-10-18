"""Administrative source authentication and non-authorizing proposal writer.
It reads source text/admin JSON/opaque fixed dependencies. The command string it
writes is never parsed, imported, compiled or executed by this preparation.
"""
from pathlib import Path
import hashlib,json,re,shlex,os
D=Path(__file__).resolve().parent;B=D.parent
S=B/'ri160-white-fixture-custody-repair-ufok1zpo';V=B/'ri160-independent-fixture-review-zhizl2vs';R=B/'ri160-root-fixture-adjudication-0rmgmo7y'
Q=B/'ri141-white-bootstrap-source-h58ls076';P=B/'ri135-white-preparation-repair-source-lski1ize'
QA=B/'ri140-root-source-adjudication-8796wh9l'/'RI141_ROOT_ADJUDICATION.json'
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def pin(p):
 assert p.is_absolute() and p.resolve()==p and p.is_file() and not p.is_symlink(),str(p)
 a=p.stat();h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 state=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
 assert state(a)==state(p.stat()) and n==a.st_size
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def read(p):return json.loads(p.read_bytes())
def write(name,x):
 with (D/name).open('xb') as f:f.write(canon(x))
def verify(row):assert pin(Path(row['path']))==row,row['path']
for p,n,h in [(R/'MEASUREMENT_SUCCESSOR_ASSIGNMENT.json',4276,'55d6231a3d1aaf29f698b916983407d7838d4d83bc04d5e0f01b40a8b901d78a'),(R/'RI160_ROOT_ADJUDICATION.json',2582,'667e157b07b210952b819f9b9e4907abb4eb3dddb1c7bdcce4d3d6d04ad873b4'),(S/'HANDOFF.json',14881,'a0067b9dbacf3ae293260cae242ee646c67c53a0c32ed25d0f47ab3c4056b00f'),(V/'HANDOFF.json',7293,'e25342fcaa37c812a70552e6e664aa6e026f11d16e8b40b7be7fc127fef36093')]:verify({'path':str(p),'bytes':n,'sha256':h})
identities={};packets=[]
for directory,nameskey,fileskey in [(S,'namespace','payloads'),(V,'namespace','files'),(Q,'exact_namespace','files')]:
 h=read(directory/'HANDOFF.json');assert sorted(p.name for p in directory.iterdir())==sorted(h[nameskey])
 rows=h.get(fileskey,h.get('payloads'))
 if type(rows) is dict:rows=list(rows.values())
 for row in rows:verify(row);identities[row['path']]=row
 hp=pin(directory/'HANDOFF.json');identities[hp['path']]=hp;packets.append({'root':str(directory),'namespace':h[nameskey],'payload_count':len(rows)})
manifest=read(S/'SOURCE_SET.json');assert len(manifest['dependencies'])==567
for row in manifest['dependencies']:
 assert row['path'].startswith(str(B)+'/') or row['path'].startswith('/Volumes/AI_DATA/development/det_8_framework-ret/'),'no implicit installed runtime scope'
 verify(row);identities[row['path']]=row
for p in [R/'MEASUREMENT_SUCCESSOR_ASSIGNMENT.json',R/'RI160_ROOT_ADJUDICATION.json',R/'ROOT_MANUAL_REVIEW.md',R/'ROOT_METADATA_REPLAY.json',QA,P/'prepare.py',Q/'SOURCE_CORRESPONDENCE.json']:
 identities[str(p)]=pin(p)
# Whole literal function spans only; no AST or evaluation of source.
def span(p,name):
 t=p.read_text();m=re.search('^def '+re.escape(name)+r'\(',t,re.M);assert m
 nextdef=re.search(r'^def ',t[m.end():],re.M);end=m.end()+nextdef.start() if nextdef else len(t)
 return t[m.start():end].rstrip().encode()
correspondence=[]
for name in ('need','canonical','pure','body','ref','save','monitor_text','child_run'):
 a=span(P/'prepare.py',name);b=span(Q/'prepare.py',name);assert a==b,name
 correspondence.append({'name':name,'whole_literal_span_identical':True,'bytes_without_trailing_space':len(b),'sha256':hashlib.sha256(b).hexdigest()})
facts=read(D/'FIXED_CURRENT_FACTS.json');assert facts['current_binding_equals_immutable_expected_binding'] is True
assert facts['current_selected_binding']==manifest['bootstrap_binding']
for row in facts['selected_file_observations']:
 # Current preparation fact is retained and externally bracketed later; this
 # opaque byte check is not an additional dynamic vendor/host observation.
 if row['path']==row['resolved_path']:verify({k:row[k] for k in ('path','bytes','sha256')})
monitor=B/'ri162-inert106-monitor-proposed-wb69vu5s';output=B/'ri156-operation-ri162-inert106-wb69vu5s'
envroot=B/'ri162-inert106-environment-proposed-wb69vu5s';records=B/'ri162-inert106-root-records-proposed-wb69vu5s'
paths={'monitor_output':str(monitor),'adapter_output':str(output),'environment_root':str(envroot),'tmp':str(envroot/'tmp'),'root_records':str(records),'admission':str(records/'ADAPTER_ADMISSION.json'),'request':str(records/'CONTROLS_REQUEST.json'),'preflight':str(records/'BOOTSTRAP_PREFLIGHT.json')}
assert len(set(paths.values()))==len(paths)
observed_absences={k:not os.path.lexists(v) for k,v in paths.items()};assert all(observed_absences.values())
env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':paths['tmp'],'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
bootstrap=manifest['bootstrap_binding']['path'];child=[bootstrap,'-I','-B',str(S/'adapter.py'),'--admission',paths['admission']]
monitor_pin=pin(Q/'prepare.py');request={'phase':'INERT_METADATA_ONLY'};request_bytes=canon(request)
request_pin={'path':paths['request'],'bytes':len(request_bytes),'sha256':hashlib.sha256(request_bytes).hexdigest()}
# Literal proposal only. The complete accepted module is captured/hashed,
# loaded non-main, unmodified, and only child_run is invoked. Root must inspect
# this finite command before separate admission. No wrapper implementation file.
invocation="""import hashlib, importlib.util, os, sys
from pathlib import Path
expected_environment = %r
if dict(os.environ) != expected_environment: raise RuntimeError('RI162 exact controlled environment')
if sys.executable != %r or (sys.flags.isolated, sys.flags.dont_write_bytecode, sys.flags.optimize) != (1, 1, 0): raise RuntimeError('RI162 direct normal isolated vendor')
source_path = Path(%r)
if source_path.is_symlink() or source_path.resolve(strict=True) != source_path: raise RuntimeError('RI162 literal monitor source')
before = source_path.stat()
with source_path.open('rb') as stream: captured = stream.read(67108865)
state = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
if state(before) != state(source_path.stat()) or len(captured) != %r or hashlib.sha256(captured).hexdigest() != %r: raise RuntimeError('RI162 complete monitor capture')
module_name = 'ri162_whole_unchanged_ri141_monitor'
if module_name in sys.modules: raise RuntimeError('RI162 fresh non-main monitor name')
spec = importlib.util.spec_from_file_location(module_name, source_path)
module = importlib.util.module_from_spec(spec)
exec(compile(captured, str(source_path), 'exec'), module.__dict__)
module.child_run(%r, Path(%r), 'CONTROLS', 180, expected_environment)
"""%(env,bootstrap,str(Q/'prepare.py'),monitor_pin['bytes'],monitor_pin['sha256'],child,str(monitor))
with (D/'MONITOR_INVOCATION.proposal.txt').open('x') as f:f.write(invocation)
outer=['/usr/bin/env','-i']+[k+'='+v for k,v in sorted(env.items())]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',bootstrap,'-I','-B','-c',invocation]
command=shlex.join(outer)
admission={'schema':'ri156-root-adapter-admission-v1','status':'AUTHORIZE_ONE_BOUNDED_METADATA_ACTION','action':'controls','source_manifest':pin(S/'SOURCE_SET.json'),'source_review':pin(R/'RI160_ROOT_ADJUDICATION.json'),'qualification':None,'request':request_pin,'output':str(output),'environment':env,'bootstrap_preflight':{'UNRESOLVED_ROOT_ONLY':'full fresh genuine preflight FilePin at '+paths['preflight']},'bounds':{'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864},'genuine_outer_required':True}
write('QUALIFICATION_PROPOSAL.json',{'schema':'ri162-nonauthorizing-inert106-proposal-v1','status':'PROPOSAL_ONLY_DO_NOT_PASS_THIS_OBJECT_TO_TARGET','source':pin(S/'HANDOFF.json'),'source_root_acceptance':pin(R/'RI160_ROOT_ADJUDICATION.json'),'monitor_source':monitor_pin,'monitor_source_acceptance':pin(QA),'operation_paths_not_created':paths,'observed_absences':observed_absences,'controlled_environment_proposed_not_observed_in_vendor':env,'request_fields':request,'request_future_identity':request_pin,'adapter_admission_field_proposal':admission,'monitor_call':{'function':'child_run','command':child,'out':str(monitor),'label':'CONTROLS','seconds':180,'env':env,'whole_module_non_main':True,'other_entry_functions_called':False},'outer_argv_proposal':outer,'exec_command_arguments_proposal':{'cmd':command,'workdir':str(records),'login':False,'yield_time_ms':1000,'max_output_tokens':4000},'pending_poll_arguments_proposal':{'session_id':'ACTUAL_INITIAL_RESULT_SESSION_ONLY','chars':'','yield_time_ms':1000,'max_output_tokens':4000},'current_bootstrap_binding_exact':True,'monitor_invocation_source':pin(D/'MONITOR_INVOCATION.proposal.txt'),'actual_control_execution':False,'active_admission_created':False})
write('SOURCE_AND_MONITOR_AUTHENTICATION.json',{'schema':'ri162-source-monitor-authentication-v1','complete_packet_checks':packets,'source_manifest':pin(S/'SOURCE_SET.json'),'inherited_dependencies_verified':567,'all_verified_source_evidence_identities':[identities[k] for k in sorted(identities)],'identity_count':len(identities),'monitor_ancestry':correspondence,'monitor_whole_current_pin':monitor_pin,'monitor_bound_argument_values_unchanged':True,'runtime_or_scientific_execution':False,'source_compiled_or_imported':False,'current_vendor_full_supplier_observation':False})
print(json.dumps({'authenticated_evidence_identities':len(identities),'source_dependencies':567,'monitor_unchanged_spans':len(correspondence),'prospective_paths_absent':all(observed_absences.values()),'controls_executed':0,'proposal_only':True},sort_keys=True))
