"""Independent finite administrative review. Never imports or invokes subjects."""
from pathlib import Path
import hashlib, importlib.util, json, os, re, shlex, subprocess, sys, datetime
D=Path(__file__).resolve().parent
B=D.parent
S=B/'ri162-inert-qualification-preflight-wb69vu5s'
T=B/'ri160-white-fixture-custody-repair-ufok1zpo'
V=B/'ri160-independent-fixture-review-zhizl2vs'
Q=B/'ri141-white-bootstrap-source-h58ls076'
P=B/'ri135-white-preparation-repair-source-lski1ize'
R=B/'ri160-root-fixture-adjudication-0rmgmo7y'
A=B/'ri161-root-qualification-review-0dyyjyuy'/'MEASUREMENT_REVIEW_ASSIGNMENT.json'
H=B/'ri122-root-execution-review-6whn_vky'/'metadata.py'
b=H.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted administrative helper pin')
spec=importlib.util.spec_from_file_location('ri162_trusted_admin_only',H)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=D
checks=[];identities={};expected={}
def test(ok,description):
    checks.append({'check':description,'passed':bool(ok)})
    if not ok:raise ValueError(description)
def same(a,b,description):test(m.canonical(a)==m.canonical(b),description)
def observed(path):
    path=str(path)
    if path not in identities:identities[path]=m.identity(path)
    return identities[path]
def pin(path):return {k:observed(path)[k] for k in ('path','bytes','sha256')}
def verify(row,label):
    same(pin(row['path']),row,label)
    test(observed(row['path'])['resolved_path']==row['path'] and observed(row['path'])['symlink_chain']==[],label+' literal and component links')
    if row['path'] in expected:same(expected[row['path']],row,label+' no conflicting declared identity')
    expected[row['path']]=row
    return row
try:
    verify({'path':str(A),'bytes':1693,'sha256':'7d1aecb0b5a7d94adabac54a6f7f4f5178027da4a60a7574ab5a5ee841661415'},'root assignment')
    verify({'path':str(S/'HANDOFF.json'),'bytes':8931,'sha256':'97b16e9424e415dc03d3ff654785ea3bfb691964dbfa7c4c1e1a26db3e1207bf'},'subject handoff')
    subject=m.load(S/'HANDOFF.json')
    same(sorted(x.name for x in S.iterdir()),subject['namespace'],'subject exact namespace')
    test(len(subject['namespace'])==13 and len(subject['payloads'])==12,'subject 13/12 closure')
    same(sorted(Path(x['path']).name for x in subject['payloads']),sorted(set(subject['namespace'])-{'HANDOFF.json'}),'each payload exactly once')
    for row in subject['payloads']:verify(row,'subject payload '+row['path'])
    auth=m.load(S/'SOURCE_AND_MONITOR_AUTHENTICATION.json');proposal=m.load(S/'QUALIFICATION_PROPOSAL.json');facts=m.load(S/'FIXED_CURRENT_FACTS.json');manifest=m.load(T/'SOURCE_SET.json')
    derived={};packets=[]
    for directory,nameskey,fileskey in ((T,'namespace','payloads'),(V,'namespace','files'),(Q,'exact_namespace','files')):
        h=m.load(directory/'HANDOFF.json');names=h[nameskey];rows=h.get(fileskey,h.get('payloads'))
        if isinstance(rows,dict):rows=list(rows.values())
        same(sorted(x.name for x in directory.iterdir()),sorted(names),'complete predecessor namespace '+str(directory))
        same(sorted(Path(x['path']).name for x in rows),sorted(set(names)-{'HANDOFF.json'}),'exact predecessor payload domain '+str(directory))
        for row in rows:verify(row,'predecessor payload '+row['path']);derived[row['path']]=row
        hp=pin(directory/'HANDOFF.json');derived[hp['path']]=hp
        packets.append({'root':str(directory),'namespace':names,'payload_count':len(rows)})
    same(packets,auth['complete_packet_checks'],'complete predecessor packet declarations')
    test(len(manifest['dependencies'])==567,'567 inherited source dependencies')
    test(len(set(row['path'] for row in manifest['dependencies']))==567,'dependency uniqueness')
    for row in manifest['dependencies']:verify(row,'opaque dependency '+row['path']);derived[row['path']]=row
    for path in (R/'MEASUREMENT_SUCCESSOR_ASSIGNMENT.json',R/'RI160_ROOT_ADJUDICATION.json',R/'ROOT_MANUAL_REVIEW.md',R/'ROOT_METADATA_REPLAY.json',B/'ri140-root-source-adjudication-8796wh9l'/'RI141_ROOT_ADJUDICATION.json',P/'prepare.py',Q/'SOURCE_CORRESPONDENCE.json'):
        row=pin(path);derived[row['path']]=row
    declared=auth['all_verified_source_evidence_identities']
    same(declared,[derived[k] for k in sorted(derived)],'complete exact independently reconstructed 623-entry closure')
    test(len(derived)==623 and auth['identity_count']==623,'623 distinct source review provenance objects')
    for row in declared:verify(row,'declared source evidence '+row['path'])
    same(auth['source_manifest'],pin(T/'SOURCE_SET.json'),'source manifest relation')
    def span(path,name):
        text=path.read_text();begin=re.search('^def '+re.escape(name)+r'\(',text,re.M)
        test(begin is not None,'source function present '+name+' '+str(path))
        endmatch=re.search(r'^def ',text[begin.end():],re.M)
        end=begin.end()+endmatch.start() if endmatch else len(text)
        return text[begin.start():end].rstrip().encode('utf-8')
    ancestry=[]
    for name in ('need','canonical','pure','body','ref','save','monitor_text','child_run'):
        before=span(P/'prepare.py',name);after=span(Q/'prepare.py',name)
        test(before==after,'whole literal inherited span '+name)
        ancestry.append({'name':name,'whole_literal_span_identical':True,'bytes_without_trailing_space':len(after),'sha256':hashlib.sha256(after).hexdigest()})
    same(ancestry,auth['monitor_ancestry'],'all eight exact ancestry records')
    same(pin(Q/'prepare.py'),proposal['monitor_source'],'whole monitor pin in proposal')
    same(auth['monitor_whole_current_pin'],proposal['monitor_source'],'monitor authentication relation')
    paths=proposal['operation_paths_not_created'];test(len(paths)==8 and len(set(paths.values()))==8,'eight distinct prospective paths')
    absences={name:not os.path.lexists(path) for name,path in paths.items()}
    test(all(absences.values()),'all eight proposed paths remain genuinely absent')
    for name in ('root_records','environment_root','monitor_output','adapter_output'):
        p=Path(paths[name]);test(p.parent==B and p.resolve()==p,'literal immediate child '+name)
    same(paths['tmp'],str(Path(paths['environment_root'])/'tmp'),'exact controlled TMPDIR')
    for name,filename in (('request','CONTROLS_REQUEST.json'),('admission','ADAPTER_ADMISSION.json'),('preflight','BOOTSTRAP_PREFLIGHT.json')):same(paths[name],str(Path(paths['root_records'])/filename),'root-owned '+name)
    test(Path(paths['adapter_output']).name.startswith('ri156-operation-'),'adapter output prefix')
    same(sorted(paths),sorted(('monitor_output','adapter_output','environment_root','tmp','root_records','admission','request','preflight')),'closed prospective path roles')
    env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':paths['tmp'],'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
    same(proposal['controlled_environment_proposed_not_observed_in_vendor'],env,'full exact ten-field environment')
    vendor=manifest['bootstrap_binding']['path']
    child=[vendor,'-I','-B',str(T/'adapter.py'),'--admission',paths['admission']]
    same(proposal['monitor_call'],{'function':'child_run','command':child,'out':paths['monitor_output'],'label':'CONTROLS','seconds':180,'env':env,'whole_module_non_main':True,'other_entry_functions_called':False},'complete concrete monitor call')
    invocation=(S/'MONITOR_INVOCATION.proposal.txt').read_text()
    test(len(invocation.splitlines())==17 and invocation.endswith('\n'),'17 complete literal invocation lines')
    lines=invocation.splitlines()
    expected_lines=[
        'import hashlib, importlib.util, os, sys','from pathlib import Path',
        'expected_environment = '+repr(env),
        "if dict(os.environ) != expected_environment: raise RuntimeError('RI162 exact controlled environment')",
        "if sys.executable != "+repr(vendor)+" or (sys.flags.isolated, sys.flags.dont_write_bytecode, sys.flags.optimize) != (1, 1, 0): raise RuntimeError('RI162 direct normal isolated vendor')",
        'source_path = Path('+repr(str(Q/'prepare.py'))+')',
        "if source_path.is_symlink() or source_path.resolve(strict=True) != source_path: raise RuntimeError('RI162 literal monitor source')",
        'before = source_path.stat()',"with source_path.open('rb') as stream: captured = stream.read(67108865)",
        'state = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)',
        "if state(before) != state(source_path.stat()) or len(captured) != 45721 or hashlib.sha256(captured).hexdigest() != '8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe': raise RuntimeError('RI162 complete monitor capture')",
        "module_name = 'ri162_whole_unchanged_ri141_monitor'","if module_name in sys.modules: raise RuntimeError('RI162 fresh non-main monitor name')",
        'spec = importlib.util.spec_from_file_location(module_name, source_path)','module = importlib.util.module_from_spec(spec)',
        "exec(compile(captured, str(source_path), 'exec'), module.__dict__)",
        'module.child_run('+repr(child)+', Path('+repr(paths['monitor_output'])+"), 'CONTROLS', 180, expected_environment)"]
    same(lines,expected_lines,'all 17 lines independently reconstructed as inert text only')
    outer=['/usr/bin/env','-i']+[k+'='+v for k,v in sorted(env.items())]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',vendor,'-I','-B','-c',invocation]
    same(proposal['outer_argv_proposal'],outer,'complete exact outer env Perl alarm vendor invocation')
    args={'cmd':shlex.join(outer),'workdir':paths['root_records'],'login':False,'yield_time_ms':1000,'max_output_tokens':4000}
    same(proposal['exec_command_arguments_proposal'],args,'complete proposed actual-tool arguments')
    same(shlex.split(args['cmd']),outer,'shell quote roundtrip without shell invocation')
    same(proposal['pending_poll_arguments_proposal'],{'session_id':'ACTUAL_INITIAL_RESULT_SESSION_ONLY','chars':'','yield_time_ms':1000,'max_output_tokens':4000},'no invented pending session')
    request={'phase':'INERT_METADATA_ONLY'};requestpin={'path':paths['request'],**m.pin(m.canonical(request))}
    same(request,proposal['request_fields'],'closed inert request only')
    same(requestpin,proposal['request_future_identity'],'prospective request metadata identity')
    admission={'schema':'ri156-root-adapter-admission-v1','status':'AUTHORIZE_ONE_BOUNDED_METADATA_ACTION','action':'controls','source_manifest':pin(T/'SOURCE_SET.json'),'source_review':pin(R/'RI160_ROOT_ADJUDICATION.json'),'qualification':None,'request':requestpin,'output':paths['adapter_output'],'environment':env,'bootstrap_preflight':{'UNRESOLVED_ROOT_ONLY':'full fresh genuine preflight FilePin at '+paths['preflight']},'bounds':{'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864},'genuine_outer_required':True}
    same(proposal['adapter_admission_field_proposal'],admission,'all 12 inert proposed admission fields and unchanged limits')
    test(len(admission)==12 and proposal['schema']!='ri156-root-adapter-admission-v1','proposal is not an operational admission')
    fixed=[]
    for old in facts['selected_file_observations']:
        current=m.identity(old['path']);identities[old['path']]=current;fixed.append(current)
        same(current,old,'fresh full six-field selected observation '+old['path'])
    same(fixed[0],manifest['bootstrap_binding'],'fresh direct vendor full binding equals immutable accepted selection')
    test(len(fixed)==6,'exactly six selected fixed files')
    sw=subprocess.run(['/usr/bin/sw_vers'],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10,check=False)
    sw_record={'command':['/usr/bin/sw_vers'],'returncode':sw.returncode,'stderr':sw.stderr.decode(),'stdout':sw.stdout.decode(),'timeout_seconds':10}
    uname=os.uname();host={'sw_vers':sw_record,'uname':{k:getattr(uname,k) for k in ('sysname','release','machine','version')}}
    same(host,facts['host'],'fresh permitted OS host facts match source preparation facts')
    test(sw.returncode==0 and not sw.stderr,'permitted OS utility actual success')
    fixed_after=[m.identity(row['path']) for row in fixed]
    same(fixed_after,fixed,'finite selected-file before/after observation stability')
    same(sorted(x.name for x in S.iterdir()),subject['namespace'],'subject namespace still immutable at completion')
    for row in subject['payloads']:same({k:m.identity(row['path'])[k] for k in ('path','bytes','sha256')},row,'subject payload still exact '+row['path'])
    result={'schema':'ri162-root-administrative-review-v1','status':'ALL_FINITE_ADMINISTRATIVE_CHECKS_PASSED','checks':checks,'predicate_count':len(checks),'source_evidence_count':len(derived),'source_dependency_count':len(manifest['dependencies']),'unique_observed_identities':len(identities),'identities':[identities[k] for k in sorted(identities)],'source_evidence_bytes':sum(x['bytes'] for x in derived.values()),'inherited_spans':ancestry,'current_fixed_files':fixed,'fresh_fixed_file_post':fixed_after,'fresh_host':host,'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prospective_path_absences':absences,'controls_defined':106,'controls_executed':0,'vendor_target_monitor_helper_control_invoked':False,'scientific_body_decoded':False,'runtime_inventory_or_card_created':False,'administrative_interpreter':sys.executable,'limitations':['Six fixed files and selected OS facts only; no whole supplier/framework inventory or runtime selection observation.','Opaque identity equality is not scientific or operational qualification.','Future invocation is compared as text and shell argument metadata, never Python parsed/compiled/imported/run.']}
    row=m.save('METADATA_CHECK.json',result)
    print(json.dumps({'status':result['status'],'predicates':len(checks),'source_evidence_count':len(derived),'source_dependencies':567,'unique_observed_identities':len(identities),'source_evidence_bytes':result['source_evidence_bytes'],'eight_unchanged_spans':len(ancestry),'current_selected_files':6,'current_selected_binding_exact':True,'all_paths_absent':True,'controls_executed':0,'result':row},sort_keys=True))
except BaseException as exc:
    m.save('FAILED_ADMIN_ATTEMPT.json',{'checks':checks,'type':type(exc).__name__,'message':str(exc),'identities_observed':len(identities)})
    raise
