"""RI152 independent administrative SAVED-evidence review. No target imports/runtime reads."""
from pathlib import Path
import hashlib,json,os,stat,collections,re,traceback
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri152-independent-actual65-review-ssaGIKOi';D=B/'ri152-root-guard-qualification-pd116byo'
O=B/'ri152-genuine-caller-guards-6p72zuof';P=O/'output'
N=B/'ri148-genuine-normal-profile-yfilag7e/output';NR=B/'ri148-independent-normal-review-fbnud7fq'
Q=B/'ri141-white-bootstrap-source-h58ls076';S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
PRIOR=B/'ri146-root-current-capture-9bfi4u8s'
V=str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env')
L='/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11'
BOOT='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
checks=[];reads={};summary={};extras={}
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def ok(v,label):
 checks.append({'check':label,'passed':bool(v)})
 if not v:raise AssertionError(label)
def same(a,b,label):
 if type(a) is bytes or type(b) is bytes:ok(type(a) is bytes and type(b) is bytes and a==b,label)
 else:ok(canon(a)==canon(b),label)
def fields(x,n,label):same(sorted(x),sorted(n.split()),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def data(p):
 p=Path(p);ok(p.is_absolute() and (p.is_relative_to(B) or p.is_relative_to(Path('/Volumes/AI_DATA/development/det_8_framework-ret'))) and '/env/' not in str(p),'review read is external saved/source evidence: '+str(p))
 s=p.lstat();ok(stat.S_ISREG(s.st_mode) and p.resolve()==p,'literal saved regular file: '+str(p))
 with p.open('rb') as f:b=f.read()
 same(state(p.lstat()),state(s),'saved read stable: '+str(p))
 reads[str(p)]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 return b
 def_unreachable=None
def ref(p):data(p);return reads[str(p)]
def pure(x):return {k:x[k] for k in ('bytes','sha256')}
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate administrative key '+k)
  d[k]=v
 return d
def load(p,canonical=True):
 b=data(p);x=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
 if canonical:same(b.decode('ascii'),canon(x).decode('ascii'),'canonical admin JSON: '+str(p))
 return x
def pinned(row,parse=False):
 same(ref(row['path']),{k:row[k] for k in ('path','bytes','sha256')},'exact pinned bytes: '+row['path'])
 return load(row['path']) if parse else row
def identity_saved(row):
 pinned(row);p=Path(row['path']);same(str(p.resolve()),row['resolved_path'],'literal resolution: '+str(p));same(row['symlink_chain'],[],'source/evidence no link: '+str(p));same(state(p.lstat()),row['state'],'full saved identity: '+str(p))
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  st=p.lstat();n=str(p.relative_to(root))
  if stat.S_ISREG(st.st_mode):rows.append(dict(relative=n,kind='file',**pure(ref(p))))
  elif stat.S_ISDIR(st.st_mode):rows.append(dict(relative=n,kind='directory'))
  elif stat.S_ISLNK(st.st_mode):rows.append(dict(relative=n,kind='symlink',target=os.readlink(p)))
  else:raise AssertionError('special evidence member')
 return rows

def digest(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def check_json(path,expected,label):same(load(path),expected,label)
def scalar_error(message):return dict(type='ValueError',message=message)
def out_value(value=None,error=None):return dict(value=value,error=error)
def env_for(root):
 return dict(PATH='/usr/bin:/bin',LC_ALL='C',TZ='UTC',TMPDIR=str(root/'tmp'),OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
def runpaths(root,mode):
 base=root/'runs'/mode;cmd=['/nonexecuted/guard-interpreter','-I','-B']+(['-O'] if mode=='optimized' else [])
 return dict(command=cmd+[str(root/'worker.py'),str(root/'AUTHORIZED_FREEZE.json'),mode],launcher_command=cmd+[str(root/'launch.py'),str(root/'AUTHORIZED_FREEZE.json'),mode],stdout=base/'CALLER_ENVELOPE.json',stderr=base/'stderr',worker_receipt=base/'WORKER.json',receipt=base/'SUPERVISOR.json',custody=base/'CUSTODY.json',claim=base/'ATTEMPT.json')
try:
 pre=load(D/'SOURCE_PRE.json');post=load(D/'SOURCE_POST.json');same(post,dict(identities=pre['identities'],unchanged=True),'whole599 source PREPOST')
 same(len(pre['identities']),599,'599 exact source predecessor inputs');same(len({r['path'] for r in pre['identities']}),599,'599 unique source inputs')
 for row in pre['identities']:identity_saved(row)
 deps=load(Q/'DEPENDENCIES.source-only.json');smap={r['path']:r for r in pre['identities']}
 same(len(deps['opaque_files']),442,'442 dependencies')
 for row in deps['opaque_files']:same({k:smap[row['path']][k] for k in ('path','bytes','sha256')},row,'source inclusion '+row['path'])
 same(tree(S),deps['packet_namespace'],'complete RI130 original namespace')
 card=load(O/'GUARDS_ADMISSION.json');guardcard=load(O/'CALLER_GUARD_ADMISSION.json');layout=load(D/'OPERATION_LAYOUT.json')
 fields(card,'schema status phase sources source_review packet output environment_root bootstrap bootstrap_host_preflight host baseline_acceptance normal_acceptance profiles_acceptance guard_admission bounds genuine_outer_required','closed17 parent card')
 bounds=dict(snapshot_seconds=180,profile_seconds=30,guard_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864,driver_soft_seconds=900,genuine_outer_timeout_seconds=960)
 env=env_for(B/'ri146-genuine-current-capture-heib6de2/environment');same(layout['environment'],env,'fixed env');same(card['environment_root'],str(B/'ri146-genuine-current-capture-heib6de2/environment'),'same environment root')
 same([card[k] for k in ('schema','status','phase','packet','output','normal_acceptance','genuine_outer_required')],['ri141-root-preparation-admission-v1','AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION','guards',str(S),str(P),None,True],'parent phase scope')
 same(card['bounds'],bounds,'all bounds unchanged');same(card['sources'],{n:pure(ref(Q/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')},'exact current sources')
 decision=pinned(card['source_review'],True);same(decision['status'],'ACCEPT_UNCHANGED_SOURCE_FOR_ONE_65_GUARD_PHASE','root source decision');same(decision['actual_guards_executed_at_decision'],0,'source-only original decision')
 for r in decision['review_objects']:pinned(r)
 ids=load(B/'ri152-independent-guard-preflight-qvsy2hmk/OPAQUE_PREFLIGHT_CHECK.json')['ordered_guard_ids'];same(len(ids),65,'literal65 IDs')
 helpers=('control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py')
 fields(guardcard,'schema status packet harness helpers controls output source_review genuine_outer_required','closed9 guardcard')
 same(guardcard,dict(schema='ri130-root-guard-admission-v1',status='AUTHORIZE_RI130_NONSCIENTIFIC_CALLER_GUARDS_ONLY',packet=str(S),harness=pure(ref(S/'guard_controls.source-only.py')),helpers={n:pure(ref(S/n)) for n in helpers},controls=ids,output=str(P/'GUARD_REPORT.json'),source_review=card['source_review'],genuine_outer_required=True),'entire separate guardcard')
 same(card['guard_admission'],ref(O/'CALLER_GUARD_ADMISSION.json'),'parent separate card pin')
 same(card['profiles_acceptance'],ref(B/'ri150-root-optimized-profile-0ydjxad3/PROFILES_ACCEPTANCE.json'),'genuine accepted profiles pin')
 same(card['baseline_acceptance'],ref(PRIOR/'BASELINE_ACCEPTANCE.json'),'genuine baseline decision pin')
 for stage,key,expected in [('baseline','baseline_acceptance',['capture']),('profiles','profiles_acceptance',['profile_normal','profile_optimized'])]:
  accepted=pinned(card[key],True);fields(accepted,'schema status stage sources packet environment_root completions genuine_outer independent_review scientific_execution','predecessor closed '+stage)
  same([accepted[k] for k in ('schema','status','stage','scientific_execution')],['ri133-root-preparation-stage-review-v1','ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage,False],'predecessor scope '+stage)
  for k in ('sources','packet','environment_root'):same(accepted[k],card[k],'predecessor exact '+stage+k)
  same(list(accepted['completions']),expected,'complete predecessors '+stage);same(list(accepted['genuine_outer']),expected,'complete predecessor outers '+stage);pinned(accepted['independent_review'])
  for phase in expected:
   previous=pinned(accepted['completions'][phase],True);outer=pinned(accepted['genuine_outer'][phase],True);pinned(outer['raw_tool_receipt'])
   same([previous[k] for k in ('schema','phase','status','first_error','independent_tail_errors')],['ri133-preparation-completion-v1',phase,'CAPTURED_FOR_INDEPENDENT_REVIEW',None,[]],'predecessor completed '+phase)
   same(outer['completion'],accepted['completions'][phase],'outer predecessor pin '+phase);same(outer['exit_code'],0,'outer predecessor exit '+phase);same(outer['command'],previous['command'],'outer predecessor command '+phase);same(outer['environment'],env,'outer predecessor env '+phase)
   for r in previous['artifacts'].values():pinned(r)
   ns=pinned(previous['artifacts']['namespace'],True);base=Path(accepted['completions'][phase]['path']).parent
   same(tree(base),sorted(ns['entries']+[dict(relative=n,kind='file',**pure(ref(base/n))) for n in ('NAMESPACE.json','COMPLETE.json')],key=lambda r:r['relative']),'entire retained predecessor namespace '+phase)
 # Whole saved current snapshot and root's actual post-observation, not new runtime reads.
 a=load(P/'PRE.stdout');same(data(P/'PRE.stdout'),data(P/'POST.stdout'),'complete current snapshots identical')
 same(data(P/'PRE.stdout'),data(B/'ri146-genuine-current-capture-heib6de2/output/POST.stdout'),'whole accepted baseline equal')
 same(pure(ref(P/'PRE.stdout')),dict(bytes=7142026,sha256='ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e'),'exact snapshot bytes')
 same(a['sources']['opaque_files'],deps['opaque_files'],'all source snapshot observations');same(a['sources']['packet_namespace'],deps['packet_namespace'],'captured packet namespace')
 same(a['runtime_inventory'],pinned(deps['historical_runtime'],True),'full historical runtime bridge');same(a['interpreter'],pinned(deps['historical_interpreter'],True),'authentic historical interpreter bridge')
 same(a['optional_namespaces'],dict(directories=pinned(deps['historical_optional_namespaces'],True)['directories']),'full optional namespace bridge')
 runtime={x['path']:x for x in a['runtime_inventory']['files']};selection={x['path']:x for x in a['selection']['files']}
 same(len(runtime),9923,'runtime9923');same(sum(x['bytes'] for x in runtime.values()),258862951,'runtime258862951bytes');same(sorted(selection),sorted(runtime),'complete selection domain')
 runtimepost=load(D/'RUNTIME_POST_IDENTITIES.json');same(runtimepost['scientific_body_decode'],False,'root runtime opaque');same(runtimepost['subject_execution'],False,'root runtime not subjectexecution');same([x['path'] for x in runtimepost['identities']],sorted(runtime),'rootpost entire domain')
 for row in runtimepost['identities']:
  path=row['path'];same({k:row[k] for k in ('path','bytes','sha256')},runtime[path],'saved runtime full hash '+path);same(row['resolved_path'],path,'runtime literal '+path);same(row['symlink_chain'],[],'runtime no alias '+path)
  same([row['state'][i] for i in (0,1,2,4,5,6)],[selection[path][k] for k in ('device','inode','mode','bytes','mtime_ns','ctime_ns')],'whole selection saved '+path)
 # Unchanged genuine profile predecessors: previously independently reconstructed full objects.
 checks_saved=load(P/'CHECKS.json');fields(checks_saved,'guards prior_normal prior_optimized post_metadata source_and_admission_postcheck','closed current checks')
 for mode,rdir,odir in [('normal','ri148-independent-normal-review-fbnud7fq','ri148-genuine-normal-profile-yfilag7e'),('optimized','ri150-independent-optimized-review-zlcd4ret','ri150-genuine-optimized-profile-eb4vq_ba')]:
  rebuilt=load(B/rdir/'RECONSTRUCTED_PROFILE_CHECK.json');saved=load(B/odir/'output/CHECKS.json')['profile'];same(checks_saved['prior_'+mode],rebuilt,'every current predecessor profile check equals independent reconstruction '+mode);same(saved,rebuilt,'unchanged accepted whole profile check '+mode)
  same(rebuilt['preobserved_domain'],a['preobserved_dyld_routes'],'same full preobserved route domain '+mode)
 same([checks_saved['post_metadata'],checks_saved['source_and_admission_postcheck']],['PASS','PASS'],'current tail results')
 # Entire65 recorded outcomes and retained exact finite metadata operands.
 report=load(P/'GUARD_REPORT.json');fields(report,'schema status packet helpers_before helpers_after helpers_unchanged controls control_order counts fixture_root admission target_or_scientific_helper_imported scientific_fixtures_or_controls_executed runtime_observation_substitutions_explicit production_runtime_qualified actual_data_admitted full32_qualified ret_paused','closed65report')
 fixed=dict(schema='ri130-nonscientific-caller-guards-v1',status='all_declared_guards_passed',packet=str(S),helpers_before=guardcard['helpers'],helpers_after=guardcard['helpers'],helpers_unchanged=True,control_order=ids,counts=dict(total=65,passed=65,failed=0),admission=ref(O/'CALLER_GUARD_ADMISSION.json'),target_or_scientific_helper_imported=False,scientific_fixtures_or_controls_executed=False,runtime_observation_substitutions_explicit=True,production_runtime_qualified=False,actual_data_admitted=False,full32_qualified=False,ret_paused=True)
 same({k:v for k,v in report.items() if k not in ('controls','fixture_root')},fixed,'whole guardheader')
 F=Path(report['fixture_root']);ok(F.parent==P and F.name.startswith('ri130-nonscientific-guards-') and F.resolve()==F,'fixture owner');same([x['id'] for x in report['controls']],ids,'all65 ordered rows')
 rows={x['id']:x['evidence'] for x in report['controls']}
 for row in report['controls']:fields(row,'id passed evidence error','guard record '+row['id']);same(row['passed'],True,'passed '+row['id']);same(row['error'],None,'no escaped error '+row['id'])
 limits=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05)
 CASE_IDS=['W01_single_white_two','W02_single_white_three','W03_oriented_two','W04_negative_scale','W05_double_scale','W06_interval_mixed','W07_interval_crosses_zero','W08_zero_shift','W09_production_boundary_sparse','W10_usefulness_boundaries','W11_asymmetric_rational_radii','W12_sparse_lifted_denominators','W13_full_response_below','W14_full_response_equal','W15_full_response_above']
 MODULES=['white_kernel','white_path','white_controls','white_fixtures','kernel_controls','white_validator','validator_controls','qualify_white_only']
 PHASE='fabricated_white_qualification';CONTEXT='RI125_FABRICATED_ONLY_NOT_HISTORICAL'
 fixture_roots=[];case_oracles=[]
 # Reconstruct all12 entire saved failure receipts, all6 worker custody records.
 for side in ('parent','worker'):
  for kind in ('source','caller','runtime_acceptance','mode','late','late_postcheck'):
   cid=side+'_'+kind;e=rows[cid];fields(e,'checks counts receipt','failure evidence '+cid);p=Path(e['receipt']['path']);pinned(e['receipt']);g=p.parent.parent.parent;fixture_roots.append(g)
   reason='late' if kind=='late_postcheck' else kind;late=reason=='late';error=scalar_error('isolated_'+reason);freeze=digest(canon({'guard_metadata_double_only':True}));same(data(g/'AUTHORIZED_FREEZE.json'),canon({'guard_metadata_double_only':True}),'failure labelled freeze '+cid)
   counts=dict(helpers=(3 if side=='parent' else 2) if late else 0,runtime=2 if late else 0,profile=2 if late else 0,loaded=2 if late else 0,sources=2,science=0,child=0);same(e['counts'],counts,'exact failure counters '+cid)
   cs=dict(refused=True,first_error_preserved=True,no_scientific_entry=True,no_child=True,both_source_attempts=True)
   cs.update(dict(retained_runtime_attempted_twice=True,profile_attempted_twice=True,loaded_attempted_twice=True) if late else dict(no_first_helper_in_tail=True,no_runtime_in_tail=True))
   if kind=='late_postcheck':cs['tail_error_retained']=True
   same(e['checks'],cs,'complete failure checks '+cid)
   before={};posts={'freeze':out_value(freeze),'sources':out_value(None,error) if reason=='source' else out_value([dict(guard_only=True)])}
   if reason!='source':before['sources']=[dict(guard_only=True)]
   if reason in ('mode','late'):before['source_admission']=dict(guard_only='source/runtime acceptances substituted');posts['source_admission']=out_value(before['source_admission'])
   if late:
    before.update(mode_admission=dict(guard_only='mode acceptance substituted'),runtime=dict(guard_only='runtime verification substituted'),profile=dict(guard_only='profile substituted'))
    for k in ('mode_admission','runtime','profile'):posts[k]=out_value(before[k])
    posts['loaded']=out_value(dict(guard_only='loaded-file observation substituted'))
    if kind=='late_postcheck':posts['runtime']=out_value(None,scalar_error('isolated_runtime_tail_failure'))
   rec=load(p);common=dict(mode='normal',phase=PHASE,context=CONTEXT,freeze=freeze,limits=limits,before=before,postchecks=posts,status='refused_or_failed',error=error,full32_qualified=False,actual_data_admitted=False,ret_paused=True)
   if side=='worker':
    elapsed=rec['elapsed_seconds'];ok(type(elapsed) in (float,int) and 0<=elapsed<180,'inner worker duration '+cid)
    custody=dict(schema='ri130-white-worker-custody-v1',mode='normal',phase=PHASE,freeze=freeze,status='refused_or_failed',error=error,entry_invocations=0,entry_returned=False,envelope_pin=None,saved_custody=None,namespace_after=None)
    check_json(p.parent/'CUSTODY.json',custody,'entire worker custody '+cid)
    want=dict(common,schema='ri130-white-worker-v1',source_count=30,actual_scientific_inputs=[],entry='qualify_white_only.run_white_qualification',entry_phase='fabricated_qualification',entry_invocations=0,entry_returned=False,target_load_witness=[],saved_custody=None,namespace_after=None,elapsed_seconds=elapsed,custody_pin=pure(ref(p.parent/'CUSTODY.json')))
    allowed=['AUTHORIZED_FREEZE.json','runs','runs/normal','runs/normal/WORKER.json','runs/normal/CUSTODY.json','tmp']
   else:
    paths=runpaths(g,'normal');ret={}
    for name in ('stdout','stderr','worker_receipt','custody','claim'):ret[name]=out_value(None,dict(type='FileNotFoundError',message="[Errno 2] No such file or directory: '"+str(paths[name])+"'"))
    want=dict(common,schema='ri130-white-supervisor-v1',command=paths['command'],launcher_command=paths['launcher_command'],environment=env_for(g),monitor_attempts=[],samples=[],peak_sampled_rss_kib=0,child_exit_code=None,child_elapsed_seconds=None,stop_reason=None,worker_check=None,mode_relation=None,retained_outputs=ret,ownership_tail={})
    if late:want['pre_receipt_namespace']=out_value(None,dict(type='AttributeError',message="'types.SimpleNamespace' object has no attribute 'tree_snapshot'"))
    allowed=['AUTHORIZED_FREEZE.json','runs','runs/normal','runs/normal/SUPERVISOR.json','tmp']
   same(rec,want,'whole failure receipt '+cid);same([x['relative'] for x in tree(g)],sorted(allowed),'complete failure fixture namespace '+cid)
   case_oracles.append(dict(id=cid,whole_receipt_reconstructed=True,first_error=error,tail_errors=[v['error'] for v in posts.values() if v['error'] is not None],source_counter_checks=True))
 for kind in ('positive','changed_copy','buffer_drift','occupied'):
  want=dict(reads=MODULES[:5] if kind=='changed_copy' else MODULES,loads=MODULES if kind=='positive' else [])
  if kind!='changed_copy':want['scientific_module_imported']=False
  same(rows['capture_'+kind],want,'complete capture evidence '+kind)
 # Deterministic observed synthetic monitor values are reconstructed, not executed.
 timeout="Command '['/bin/ps', '-o', 'rss=', '-p', '424242']' timed out after 0.05 seconds"
 for kind in ('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap'):
  elapsed={'wall':181.0,'initial_gap':.101,'sample_gap':.101,'no_sample':0.,'timeout':0.,'final_gap':.102}.get(kind,.001)
  has=kind in ('positive','sample_gap','rss','final_gap');stamp=.101 if kind=='sample_gap' else .001; rss=524289 if kind=='rss' else 1
  samples=[dict(elapsed_seconds=stamp,gap_seconds=stamp,rss_kib=rss)] if has else []
  raw=[]
  if kind=='timeout':raw=[dict(elapsed_seconds=0.,exception='TimeoutExpired',message=timeout,stdout='partial',stderr='timed out')]
  elif kind not in ('no_sample','wall','initial_gap'):raw=[dict(elapsed_seconds=stamp,returncode=1 if kind=='nonzero' else 0,stdout='bad' if kind=='malformed' else str(rss),stderr='')]
  reasons={'positive':None,'no_sample':'no_rss_sample','wall':'wall_time_limit','initial_gap':'rss_sample_deadline_missed','sample_gap':'rss_sample_deadline_missed','rss':'sampled_resident_memory_limit','nonzero':'rss_monitor_unavailable','malformed':'rss_monitor_unavailable','timeout':'no_rss_sample','final_gap':'rss_final_sample_deadline_missed'}
  gap=elapsed-stamp if has else None;rec=dict(samples=samples,monitor_attempts=raw,peak_sampled_rss_kib=rss if has else 0,child_exit_code=0,child_elapsed_seconds=elapsed,stop_reason=reasons[kind],final_sample_to_reap_gap_seconds=gap,final_sample_gap_passed=gap is not None and gap<=.1)
  same(rows['monitor_'+kind],dict(record=rec,observed_exception=dict(type='TimeoutExpired',message=timeout) if kind=='timeout' else None,owned_signals=[] if kind in ('positive','no_sample','final_gap') else [424242],actual_child_started=False),'entire synthetic monitor evidence '+kind)
 for kind in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config'):
  e=rows['runtime_'+kind];g=Path(e['fixture_root']);fixture_roots.append(g)
  msg={'positive':None,'absent_file':'previously absent startup/import/loader path appeared','absent_dangling_link':'previously absent startup/import/loader path appeared','missing_loader':'mandatory loader binding omitted or changed','changed_loader_declaration':'mandatory loader binding omitted or changed','changed_loader_path':'non-OS loader binding changed','missing_config':'interpreter/framework/monitor/config runtime files omitted'}[kind]
  same(e,dict(id='runtime_'+kind,fixture_root=str(g),pass_=True) if False else {'id':'runtime_'+kind,'fixture_root':str(g),'pass':True,'expected_failure':msg,'observed_failure':None if msg is None else scalar_error(msg),'actual_scanner_and_verify_used':True,'substituted_domain_constants':['ROOTS','REQUIRED_FILES','ALLOWED_LINKS','ABSENT_PATHS','REQUIRED_LOADER_BINDINGS']},'full runtime evidence '+kind)
  files={'stdlib/tiny.py':b'fixture only\n','openssl.cnf':b'# isolated inactive configuration\n','libcrypto.fixture':b'not an executable library\n'};links={'libcrypto.alias':'other-lib' if kind=='changed_loader_path' else 'libcrypto.fixture'};dirs=['stdlib','venv_site','system_site']
  if kind=='absent_file':files['absent-1']=b'appeared\n'
  if kind=='absent_dangling_link':links['absent-1']='missing'
  if kind=='changed_loader_path':files['other-lib']=b'changed\n'
  if kind=='positive':
   inventory=dict(schema='ri121-complete-stdlib-runtime-inventory-v2',roots=[str(g/x) for x in dirs],extra_files=sorted(str(g/x) for x in ('openssl.cnf','libcrypto.fixture')),files=[dict(path=str(g/x),**digest(files[x])) for x in sorted(files)],symlinks=[],absent_paths=[str(g/('absent-'+str(i))) for i in range(8)],loader_bindings=[dict(named_path=str(g/'libcrypto.alias'),resolved_path=str(g/'libcrypto.fixture'),symlink_chain=[dict(path=str(g/'libcrypto.alias'),target='libcrypto.fixture')],target=digest(files['libcrypto.fixture']))],scope='isolated nonscientific regression fixture')
   files.update({'fixture-inventory.json':canon(inventory),'interpreter.fixture':b'not executable\n'})
  for n,b in files.items():same(data(g/n),b,'runtime fixture entire bytes '+kind+n)
  want=[dict(relative=n,kind='file',**digest(b)) for n,b in files.items()]+[dict(relative=n,kind='symlink',target=t) for n,t in links.items()]+[dict(relative=n,kind='directory') for n in dirs]
  same(tree(g),sorted(want,key=lambda x:x['relative']),'whole runtime fixture tree '+kind)
 for kind in ('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command'):same(rows['static_'+kind],dict(actual_static_validator_used=True,card_written=False,kind=kind),'full static evidence '+kind)
 for kind,count in [('positive',11),('source_execution',0),('caller_binding',0),('caller_history',0),('caller_ret',0),('guards_absent',2),('runtime_binding',4),('runtime_loader',4),('runtime_profile',4)]:same(rows['acceptance_'+kind],dict(actual_source_acceptance_semantics_used=True,opaque_io_and_static_layer_substituted=True,reads=['/guard/opaque']*count),'full acceptance exactreadprefix '+kind)
 # Actual saved six guard-mode metadata trees; no actual admission created here.
 for kind in ('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift'):
  cid='mode_'+kind;same(rows[cid],dict(actual_mode_admission_parser_used=True,isolated_guard_metadata_only=True,no_real_stage_admitted=True),'mode evidence '+kind)
  choices=[x for x in F.iterdir() if x.name.startswith('mode-'+kind+'-')];same(len(choices),1,'unique mode fixture '+kind);g=choices[0];fixture_roots.append(g)
  mode='normal' if kind in ('normal_positive','wrong_command','pre_missing') else 'optimized';fbody=canon(dict(isolated_guard_only=True))
  same(data(g/'AUTHORIZED_FREEZE.json'),fbody,'mode labelled freeze '+kind);same(data(g/'OPAQUE_GUARD_ONLY.json'),fbody,'mode labelled opaque '+kind)
  opaque=ref(g/'OPAQUE_GUARD_ONLY.json');freeze=pure(ref(g/'AUTHORIZED_FREEZE.json'));paths=runpaths(g,mode)
  pp=dict(schema='ri130-root-pre-mode-runtime-custody-v1',mode=mode,freeze=freeze,runtime_acceptance=opaque,selection_unchanged=kind!='pre_missing',optional_namespaces_unchanged=True,host_identity_unchanged=True,observed_dyld_routes=opaque,metadata_record=opaque)
  check_json(g/'PRE_GUARD_ONLY.json',pp,'complete mode pre metadata '+kind);normalref=None;allowed=['AUTHORIZED_FREEZE.json','OPAQUE_GUARD_ONLY.json','PRE_GUARD_ONLY.json','ADMIT_'+mode.upper()+'.json']
  if mode=='optimized':
   outputs={};np=runpaths(g,'normal')
   for name in ('stdout','stderr','worker_receipt','receipt','custody','claim'):
    expected=b'changed guard\n' if kind=='normal_drift' and name=='stdout' else b'guard only\n';same(data(np[name]),expected,'mode original output '+kind+name)
    outputs[name]=dict(path=str(np[name]),**digest(b'guard only\n'));allowed.append(str(np[name].relative_to(g)))
   expected=dict(schema='ri130-root-normal-white-review-v1',status='ACCEPT_NORMAL_WHITE_EXECUTION_AND_CUSTODY',freeze=freeze,all15_cases_and_W09_assembly=True,both179_controls=kind!='normal_incomplete',complete_saved_reconstruction=True,all57_artifacts_74_postchecks_3_trees=True,runtime_post_custody_passed=True,genuine_outer=opaque,independent_review=opaque,post_runtime_metadata=opaque,outputs=outputs)
   check_json(g/'NORMAL_GUARD_ONLY.json',expected,'full guard-only fake normal '+kind);normalref=ref(g/'NORMAL_GUARD_ONLY.json');allowed+=['runs','runs/normal','NORMAL_GUARD_ONLY.json']
  expected=dict(schema='ri130-root-white-mode-admission-v1',status='AUTHORIZE_ONE_WHITE_FABRICATED_MODE',mode=mode,phase=PHASE,freeze=freeze,caller_source_acceptance=opaque,command=[] if kind=='wrong_command' else paths['command'],launcher_command=paths['launcher_command'],pre_runtime_metadata=ref(g/'PRE_GUARD_ONLY.json'),normal_acceptance=normalref)
  check_json(g/('ADMIT_'+mode.upper()+'.json'),expected,'entire guard-only mode object '+kind);same([x['relative'] for x in tree(g)],sorted(allowed),'mode complete namespace '+kind)
 # Full18 metadata-stage doubles across9 cases. Only administrative markers are decoded.
 spec_path=S/'science/qualifier/CONTROL_EXPECTATIONS.json';spec=load(spec_path)
 order=['WK%02d'%i for i in range(1,39)]+['WC%02d'%i for i in range(1,27)]+['WG%02d'%i for i in range(1,93)]+['WC%02d'%i for i in range(27,47)]+['WT01','WT02','WT03'];same(spec['order'],order,'179 source expectations')
 controls=[dict(id=x['id'],expected_code=x['code'],expected_message=x['message'],observed_code=x['code'],observed_message=x['message'],passed=True) for x in spec['refusals']]
 posts=[dict(role='first',pin=None,unchanged=False,error='GUARD ONLY: changed'),dict(role='second',pin=digest(b'b'),unchanged=True,error=None)]
 controls.append(dict(id='WT01',passed=True,postchecks=posts))
 for ident,code,message in [('WT02','EXACT','first-error'),('WT03','CUSTODY','one or more final source/input postchecks failed')]:controls.append(dict(id=ident,passed=True,refusal=dict(schema='ri125-application-refusal-v1',status='REFUSED',phase='fixed_saved_application',stage='white',code=code,message='GUARD ONLY: '+code+': '+message,scientific_disposition_emitted=False,postchecks=posts)))
 roles=['white_kernel','white_path','wrapper_controls','white_contract','cases','kernel_refusals','fabricated_interfaces','white_refusals_text','white_source_handoff','fixtures','kernel_controls','orchestrator','stage_contract','control_expectations','validator','validator_controls','white_root_disposition'];bindings={n:dict(path=str(spec_path),pin=pure(ref(spec_path))) for n in roles}
 casesfiles=['W%02d-%s.json'%(i,k) for i in range(1,16) for k in ('operand','primary','independent')];assemblyfiles=['W09-complete-capture.json','W09-primary-assembly.json','W09-independent-assembly.json'];trees=['primary-kernel-controls','primary-wrapper-controls','independent-controls'];treefiles=[x.upper()+'_TREE.json' for x in trees];controlfiles=['PRIMARY_KERNEL_CONTROLS.json','PRIMARY_WRAPPER_CONTROLS.json','PRIMARY_ALL_CONTROLS.json','INDEPENDENT_ALL_CONTROLS.json']
 artnames=casesfiles+assemblyfiles+[treefiles[0],controlfiles[0],treefiles[1],controlfiles[1],controlfiles[2],treefiles[2],controlfiles[3],'FRESH_SAVED_COMPARISON.json','WHITE_ONLY_QUALIFICATION.json']
 six=['fixed_operand_schema_and_recipe','complete_result_shape','literal_case_anchor','full_directed_shift_consistency','correct_gram_presence_and_inherited_gate','correct_response_presence_and_new_gate'];four=['fixed_bound_operand_recipe','complete_bound_result_shape','literal_predicate_results','fabricated_identity_only']
 stage_limits=dict(seconds=180,sampled_rss_kib=524288,poll_ms=25,max_gap_ms=100,ps_timeout_ms=50,file_bytes=67108864,capture_row_bytes=8388608,completed_integer_bits=262144)
 for kind in ('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped'):
  expected=dict(isolated_metadata_only=True,kind=kind)
  if kind not in ('control_message','tail_dropped'):expected['all_fixture_files_retained']=True
  same(rows['relation_'+kind],expected,'complete relation outcome '+kind)
  found=[x for x in F.iterdir() if x.name.startswith('metadata-relation-'+kind+'-')];same(len(found),1,'one relation tree '+kind);g=found[0];fixture_roots.append(g)
  same(data(g/'GUARD_ONLY_NOT_QUALIFICATION.txt'),b'Metadata double only; no scientific fixture, control, reconstruction or qualification executed.\n','exact guard-only marker '+kind)
  for mode in ('normal','optimized'):
   stage=g/mode;targetrows=[]
   for name in casesfiles:
    body=dict(isolated_nonscientific_caller_guard=True,marker='different' if mode=='optimized' and kind=='science_file' and name in ('W11-primary.json','W11-independent.json') else 'same')
    if name=='W09-operand.json':body['gram']=dict(isolated_guard_gram=True)
    check_json(stage/name,body,'complete fake case metadata '+kind+mode+name)
   check_json(stage/assemblyfiles[0],dict(isolated_guard_capture=True),'fake capture '+kind+mode)
   for name in assemblyfiles[1:]:check_json(stage/name,dict(isolated_guard_assembly=True),'fake assembly '+kind+mode+name)
   for t,n in zip(trees,treefiles):
    tr=[dict(name='.',kind='directory',pin=None,target=None)];wanttree=[]
    if t!='primary-kernel-controls':
     link=str(stage/t/'WC19-seed.fabricated')+('-wrong' if mode=='optimized' and kind=='wrong_link' else '')
     tr += [dict(name='WC19-link.fabricated',kind='symlink',pin=None,target=link),dict(name='WC19-seed.fabricated',kind='file',pin=digest(b'a'),target=None)]
     wanttree=[dict(relative='WC19-link.fabricated',kind='symlink',target=link),dict(relative='WC19-seed.fabricated',kind='file',**digest(b'a'))]
     same(data(stage/t/'WC19-seed.fabricated'),b'a','full guard link seed '+kind+mode+t)
    check_json(stage/n,dict(schema='ri125-fabricated-control-tree-v1',records=tr),'entire fake tree inventory '+kind+mode+t);same(tree(stage/t),wanttree,'exact fake owned control tree '+kind+mode+t)
   for name,schema,selected,independent in [(controlfiles[0],'ri125-primary-kernel-controls-v1',controls[:37],False),(controlfiles[1],'ri125-primary-white-controls-v1',controls[37:],False),(controlfiles[2],'ri125-primary-complete-white-controls-v1',controls,False),(controlfiles[3],'ri125-independent-white-controls-v1',controls,True)]:
    header=dict(schema=schema,phase='fabricated_qualification',context=CONTEXT,actual_scientific_input_opened=False,independent_validator_run=independent,controls=selected,counts=dict(total=len(selected),passed=len(selected),failed=0),status='all_declared_controls_passed')
    check_json(stage/name,header,'every fake179 typed control field '+kind+mode+name)
   def aref(name):return dict(name=name,pin=pure(ref(stage/name)))
   cases=[]
   for i,cid in enumerate(CASE_IDS,1):
    ci=four if i==10 else six;cases.append(dict(id=cid,kind='bound_predicate_only' if i==10 else 'white_primitive',operand=aref('W%02d-operand.json'%i),primary=aref('W%02d-primary.json'%i),independent=aref('W%02d-independent.json'%i),full_fields_match=True,expected_checks=dict(inventory=ci,counts=dict(total=len(ci),passed=len(ci),failed=0),results=[dict(id=x,passed=True) for x in ci])))
   fresh=dict(schema='ri125-white-only-fresh-saved-comparison-v1',phase='fabricated_qualification',cases=[dict(id=x['id'],fresh_result_pin=x['independent']['pin'],all_fields_match=True) for x in cases],assembly=dict(id=CASE_IDS[8],fresh_result_pin=aref(assemblyfiles[2])['pin'],all_fields_match=True),saved_control_envelopes_fully_checked=True,controls_rerun_by_comparator=False,actual_data_evaluated=False,full_application_qualified=False)
   check_json(stage/'FRESH_SAVED_COMPARISON.json',fresh,'full fake saved comparison '+kind+mode)
   wanted=dict(schema='ri125-white-only-qualification-v1',phase='fabricated_qualification',status='all_white_only_gates_passed',context=CONTEXT,scope=dict(white_case_ids=CASE_IDS,white_case_count=15,full_application_case_count=32,full_application_qualified=False,actual_data_admitted=False,periodic_mean_or_join_executed=False,physical_claim=False),limits=stage_limits,source_bindings=bindings,cases=cases,complete_capture_assembly=dict(id=CASE_IDS[8],capture=aref(assemblyfiles[0]),gram_pin=digest(canon(dict(isolated_guard_gram=True))),primary=aref(assemblyfiles[1]),independent=aref(assemblyfiles[2]),full_fields_match=True),controls=dict(order=order,per_implementation=179,kernel_per_implementation=38,wrapper_and_tail_per_implementation=141,primary_kernel=aref(controlfiles[0]),primary_wrapper=aref(controlfiles[1]),primary_complete=aref(controlfiles[2]),independent_complete=aref(controlfiles[3]),both_exact_inventories_and_first_refusals_passed=True,trees=[dict(name=t,inventory=aref(n)) for t,n in zip(trees,treefiles)]),fresh_saved_comparison=aref('FRESH_SAVED_COMPARISON.json'),artifacts=[aref(n) for n in artnames[:-1]],limitations=['Only W01-W15 and their white controls are covered.','The full 32-case application, periodic/mean/join paths and actual-data admission remain pending.','Separate root source/runtime/history/caller custody and genuine completion remain required.','Exact fabricated arithmetic is not detector covariance, calibration, native geometry/gravity or physical validation.','Original precision, domain, resource and protected-validation boundaries remain; RET is paused.'])
   check_json(stage/'WHITE_ONLY_QUALIFICATION.json',wanted,'entire full fake stage report '+kind+mode)
   expectedtop=sorted(artnames+trees+(['unexpected'] if mode=='optimized' and kind=='extra_namespace' else []));same(sorted(x.name for x in stage.iterdir()),expectedtop,'closed complete57fakefiles3trees '+kind+mode)
   if mode=='optimized' and kind=='extra_namespace':same(data(stage/'unexpected'),b'guard','explicit namespace mutation')
  same(sorted(x.name for x in g.iterdir()),['GUARD_ONLY_NOT_QUALIFICATION.txt','normal','optimized'],'relation full root '+kind)
 same(sorted(x.name for x in F.iterdir()),sorted(x.name for x in fixture_roots),'all34 fixture roots no extras')
 same(len(fixture_roots),34,'12failure7runtime6mode9relation fixture roots')
 allfixtures=tree(F);same(len(allfixtures),1385,'whole1385 fixture entries');same(collections.Counter(x['kind'] for x in allfixtures),dict(file=1172,directory=169,symlink=44),'fixture1172files169dirs44links')
 same(checks_saved['guards'],dict(status='ALL65_SAVED_ENVELOPES_RECONCILED_NOT_ROOT_ACCEPTANCE',controls=report['controls'],fixture_root=str(F),all_tree_entries=allfixtures,scientific_controls_passed=0,runtime_substitutions_are_guard_doubles=True),'complete current guard checks object')
 summary['guard_outcomes']=dict(cases=65,fixture_entries=1385,files=1172,directories=169,symlinks=44,roots=34,failure_receipts=12,worker_custodies=6,synthetic_monitor_records=10,metadata_stages=18,scientific_credit=False,in_memory_refusals_source_mediated=True)
 # Every complete monitor attempt, sample, stream, command, ownership and final reap.
 complete=load(P/'COMPLETE.json');fields(complete,'schema phase status command environment admission sources artifacts first_error independent_tail_errors elapsed_seconds scientific_targets_executed actual_data_admitted full32_qualified ret_paused runtime_acceptance_created genuine_outer_created','17-field parent completion')
 same(complete['schema'],'ri133-preparation-completion-v1','parent schema');same(complete['phase'],'guards','parent phase');same(complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','parent saved status');same(complete['sources'],card['sources'],'parent source binding');same(complete['admission'],ref(O/'GUARDS_ADMISSION.json'),'parent actual card');same(complete['environment'],env,'parent exact environment')
 command=[BOOT,'-I','-B',str(Q/'prepare.py'),'--admission',str(O/'GUARDS_ADMISSION.json')];same(complete['command'],command,'parent exact direct command')
 same(complete['first_error'],None,'no parent first error');same(complete['independent_tail_errors'],[],'no independent tail error')
 for k in ['scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created']:same(complete[k],False,'no scope inflation '+k)
 same(complete['ret_paused'],True,'RET pause');ok(type(complete['elapsed_seconds']) in (int,float) and 0<complete['elapsed_seconds']<900,'parent saved soft interval')
 artifact_names={'PRE':'PRE.stdout','PRE_completion':'PRE.COMPLETION.json','GUARD_REPORT':'GUARD_REPORT.json','GUARDS_completion':'GUARDS.COMPLETION.json','POST':'POST.stdout','POST_completion':'POST.COMPLETION.json','checks':'CHECKS.json','namespace':'NAMESPACE.json'}
 same(sorted(complete['artifacts']),sorted(artifact_names),'exact eight artifact roles')
 for role,filename in artifact_names.items():same(complete['artifacts'][role],ref(P/filename),'artifact role binding '+role)
 same(load(P/'ATTEMPT.json'),dict(schema='ri133-preparation-attempt-v1',admission=ref(O/'GUARDS_ADMISSION.json'),sources=card['sources'],phase='guards',environment=env,scientific_execution=False),'entire actual owned parent attempt')
 monitor=[];owners=[]
 for label,seconds in [('PRE',180),('GUARDS',180),('POST',180)]:
  child=load(P/(label+'.COMPLETION.json'));attempt=load(P/(label+'.ATTEMPT.json'))
  cmd=([V+'/bin/python','-I','-B',str(S/'guard_controls.source-only.py'),'--packet',str(S),'--admission',str(O/'CALLER_GUARD_ADMISSION.json'),'--output',str(P/'GUARD_REPORT.json')] if label=='GUARDS' else [BOOT,'-I','-B',str(Q/'prepare.py'),'--snapshot',str(O/'GUARDS_ADMISSION.json')])
  fields(child,'command environment wall_seconds samples monitor_attempts peak_sampled_rss_kib stop_reason child_exit_code first_error tail_errors elapsed_seconds final_sample_to_reap_gap_seconds final_sample_gap_passed stdout stderr passed','complete child fields '+label)
  same(child['command'],cmd,'real child command '+label);same(child['environment'],env,'child exact env '+label);same(child['wall_seconds'],seconds,'child unchanged bound '+label)
  same([child[k] for k in ['first_error','stop_reason','child_exit_code','tail_errors','passed','final_sample_gap_passed']],[None,None,0,[],True,True],'child outcome fields '+label)
  fields(attempt,'command environment wall_seconds pid_owner scientific_target_entry','owned attempt fields '+label)
  same({k:v for k,v in attempt.items() if k!='pid_owner'},dict(command=cmd,environment=env,wall_seconds=seconds,scientific_target_entry=False),'whole nonscientific attempt '+label);ok(type(attempt['pid_owner']) is int and attempt['pid_owner']>0,'parent pid owner positive '+label);owners.append(attempt['pid_owner'])
  samples=child['samples'];raw=child['monitor_attempts'];ok(len(samples)>0 and len(raw)==len(samples),'all numeric actual ps attempts have samples '+label)
  prev=0.;residuals=[]
  for i,(s,t) in enumerate(zip(samples,raw)):
   fields(s,'elapsed_seconds rss_kib gap_seconds','sample fields '+label+str(i));fields(t,'elapsed_seconds returncode stdout stderr','raw attempt fields '+label+str(i))
   same(t['returncode'],0,'raw monitor rc '+label+str(i));same(t['stderr'],'','raw monitor stderr '+label+str(i));ok(type(t['stdout']) is str and t['stdout'].strip().isdigit(),'raw numeric stdout '+label+str(i))
   same([s['elapsed_seconds'],s['rss_kib']],[t['elapsed_seconds'],int(t['stdout'].strip())],'sample exact raw pair '+label+str(i))
   ok(type(s['rss_kib']) is int and 0<=s['rss_kib']<=524288,'raw RSS bound '+label+str(i));ok(type(s['elapsed_seconds']) in (float,int) and type(s['gap_seconds']) in (float,int) and prev<=s['elapsed_seconds']<=seconds and 0<=s['gap_seconds']<=.1,'actual exact time/gap bounds '+label+str(i))
   res=abs(s['elapsed_seconds']-prev-s['gap_seconds']);ok(res<1e-9,'source-specified arithmetic consistency '+label+str(i));residuals.append(res);prev=s['elapsed_seconds']
  same(child['peak_sampled_rss_kib'],max(s['rss_kib'] for s in samples),'peak recomputation '+label)
  same(child['final_sample_to_reap_gap_seconds'],child['elapsed_seconds']-prev,'complete final reap recomputation '+label)
  ok(prev<=child['elapsed_seconds']<=seconds and 0<=child['final_sample_to_reap_gap_seconds']<=.1,'final and wall bounds '+label)
  for stream in ['stdout','stderr']:same(child[stream],ref(P/(label+'.'+stream)),'full stream bytes '+label+stream);ok(child[stream]['bytes']<=67108864,'stream cap '+label+stream)
  same(child['stderr']['bytes'],0,'empty stderr '+label)
  monitor.append(dict(label=label,wall_seconds=seconds,elapsed_seconds=child['elapsed_seconds'],sample_count=len(samples),raw_attempt_count=len(raw),peak_sampled_rss_kib=child['peak_sampled_rss_kib'],maximum_sample_gap_seconds=max(s['gap_seconds'] for s in samples),final_sample_to_reap_gap_seconds=child['final_sample_to_reap_gap_seconds'],arithmetic_max_residual=max(residuals)))
 same(len(set(owners)),1,'same saved parent owner across three children')
 ok(sum(x['elapsed_seconds'] for x in monitor)<complete['elapsed_seconds'],'sequential child durations inside parent saved interval')
 summary['monitors']=monitor;summary['parent_elapsed_seconds']=complete['elapsed_seconds'];summary['saved_parent_pid']=owners[0]
 same(ref(P/'GUARDS.stdout')['bytes'],0,'no guard stdout');same(sum(len(load(P/(x+'.COMPLETION.json'))['monitor_attempts']) for x in ('PRE','GUARDS','POST')),148,'all148 actual raw attempts numeric; no terminal malformed actual record')
 ns=load(P/'NAMESPACE.json');fields(ns,'schema root entries excluded_not_yet_written','full namespace schema');same(ns['schema'],'ri133-retained-namespace-v1','namespace type');same(ns['root'],str(P),'namespace output owner');same(ns['excluded_not_yet_written'],['NAMESPACE.json','COMPLETE.json'],'exact2exclusions')
 actualtree=tree(P);want=ns['entries']+[dict(relative=n,kind='file',**pure(ref(P/n))) for n in ('NAMESPACE.json','COMPLETE.json')]
 same(actualtree,sorted(want,key=lambda x:x['relative']),'whole1403 output entries final2');same(len(actualtree),1403,'1403 output entries');same(len([x for x in actualtree if '/' not in x['relative']]),18,'18 top entries')
 ok(len(actualtree)<=25000 and sum(x.get('bytes',0) for x in actualtree)<=536870912,'whole namespace member and aggregate bounds')
 operation=load(D/'OPERATION_FINAL_IDENTITIES.json');same(operation['root'],str(O),'complete operation root');same(tree(O),operation['entries'],'complete1406 operation entries');same(len(operation['entries']),1406,'1406 operation entries')
 for row in operation['identities']:identity_saved(row)
 custody=load(D/'ADMISSION_CUSTODY.json');same(custody['genuine_operation_count'],1,'one admitted operation');same(custody['source_pre'],ref(D/'SOURCE_PRE.json'),'admission source-before binding')
 for k in ('card','guard_card','source_review'):identity_saved(custody[k])
 ok(Path(card['profiles_acceptance']['path']).stat().st_mtime_ns < (O/'GUARDS_ADMISSION.json').stat().st_mtime_ns < (P/'ATTEMPT.json').stat().st_mtime_ns,'accepted profiles then actualcard then ownedattempt filesystem order')
 outer=load(D/'GENUINE_OUTER.json');fields(outer,'schema status command environment exit_code completion raw_tool_receipt external_timeout_seconds','eight-field outer')
 same(outer,dict(schema='ri133-root-genuine-outer-v1',status='ACTUAL_TOOL_COMPLETION',command=command,environment=env,exit_code=0,completion=ref(P/'COMPLETE.json'),raw_tool_receipt=ref(D/'GENUINE_TOOL_COMPLETE.json'),external_timeout_seconds=960),'entire genuine outer')
 raw=load(D/'GENUINE_TOOL_COMPLETE.json',False)
 same(raw['initial'],dict(chunk_id='318cda',wall_time_seconds=1.00360725,session_id=56357,original_token_count=0,output=''),'genuine initial savedtool')
 same(raw['terminal'],dict(chunk_id='2afc57',wall_time_seconds=2.085414084,exit_code=0,original_token_count=0,output=''),'genuine terminal savedtool')
 shell_prefix='exec /usr/bin/env -i '+' '.join(k+'='+v for k,v in env.items())+" /usr/bin/perl -e '$SIG{ALRM}=\"DEFAULT\"; alarm 960; exec @ARGV; die $!;' "
 wanted=shell_prefix+' '.join(command)
 same(raw['command'],wanted,'literal full recorded command');same(raw['arguments'],dict(cmd=wanted,login=False,max_output_tokens=1200,yield_time_ms=1000),'exact initial tool args')
 same(raw['terminal_arguments'],dict(session_id=56357,chars='',yield_time_ms=1000,max_output_tokens=1200),'exact terminal call/session');same(raw['cwd_resolution'],dict(argument_omitted=True,default_cwd='/Volumes/AI_DATA/development/det_8_framework-ret'),'omitted cwd and actual default');same(raw['retry_count'],0,'no recorded retry')
 # Complete vendor PRE/POST and all saved module origins against full vendor namespace.
 vendor=load(D/'BOOTSTRAP_PRE.json');same(data(D/'BOOTSTRAP_PRE.json'),data(D/'BOOTSTRAP_POST.json'),'whole1690947 vendor PRE/POST byte equality');same(vendor['actual_environment'],env,'complete actual vendor environment');same(vendor['selected_interpreter_binding'],deps['selected_bootstrap_binding'],'full direct vendor authentic provenance');same(vendor['host'],card['host']['uname'],'vendor host unchanged');same(pinned(card['bootstrap_host_preflight'],True),vendor,'actual preflight card binding')
 selected=vendor['selected_interpreter_binding'];same(card['bootstrap'],dict(named_path=BOOT,resolved_path=BOOT,symlink_chain=[],target=pure(selected)),'card full direct bootstrap')
 pinned(vendor['collector']);pinned(vendor['metadata_helper']);same(pure(vendor['metadata_helper']),dict(bytes=3144,sha256='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'),'trusted metadata helper pin')
 fw=vendor['framework_namespace'];same(len(fw),2004,'entire saved vendor namespace');same(len({x['path'] for x in fw}),2004,'unique vendor names');vfiles={x['path']:x['identity'] for x in fw if x['kind']=='file'}
 same(sum(x['bytes'] for x in vfiles.values()),vendor['framework_file_bytes'],'saved vendor byte total');same(vendor['framework_file_bytes'],48024515,'retained vendor bytes')
 for name,bind in [(x['path'],x) for x in vendor['bindings']]:
  if bind['resolved_path'] in vfiles:same(pure(bind),pure(vfiles[bind['resolved_path']]),'vendor tool binding full namespace '+name)
 for mod in vendor['bootstrap_descriptor']['modules']:
  if 'identity' in mod:
   ident=mod['identity'];ok(ident['resolved_path'] in vfiles or ident['path'] in (str(D/'observe_bootstrap.py'),vendor['metadata_helper']['path']),'vendor module within supplier/reviewed collectors '+mod['name'])
   if ident['resolved_path'] in vfiles:same(pure(ident),pure(vfiles[ident['resolved_path']]),'complete saved vendor module pin '+mod['name'])
   else:identity_saved(ident)
 same(vendor['bootstrap_descriptor']['executable'],BOOT,'actual direct bootstrap executable');same([vendor['bootstrap_descriptor'][k] for k in ['isolated','dont_write_bytecode','optimize']],[1,1,0],'vendor actual flags')
 for phase,chunk in [('PRE','8f26b4'),('POST','809cd4')]:
  tool=load(D/('BOOTSTRAP_'+phase+'_TOOL.json'),False);same(tool['result']['chunk_id'],chunk,'actual supplier tool '+phase);same(tool['result']['exit_code'],0,'actual supplier tool success '+phase)
  wanted=shell_prefix.replace('alarm 960','alarm 240')+' '.join([BOOT,'-I','-B',str(D/'observe_bootstrap.py'),phase]);same(tool['command'],wanted,'literal supplier invocation '+phase);same(tool['arguments']['cmd'],wanted,'supplier argument command '+phase);same(tool['arguments']['login'],False,'supplier shell no login '+phase)
  ok(str(D/('BOOTSTRAP_'+phase+'.json')) in tool['result']['output'] and ref(D/('BOOTSTRAP_'+phase+'.json'))['sha256'] in tool['result']['output'],'supplier actual output file/hash linkage '+phase)
 # PRE/POST child bootstrap complete descriptors came from same supplier.
 boot=a['host_bootstrap']['bootstrap'];same(boot['named'],card['bootstrap'],'child named supplier');same(boot['actual'],card['bootstrap'],'child actual supplier');same(boot['executable'],BOOT,'child actual bootstrap descriptor');same([boot[k] for k in ('isolated','dont_write_bytecode','optimize')],[1,1,0],'snapshot bootstrap flags')
 for mod in boot['modules']:
  if 'binding' in mod:
   bi=mod['binding'];rp=bi['resolved_path'];ok(rp in vfiles or rp in (str(Q/'prepare.py'),str(Q/'runtime_metadata.py')),'saved child bootstrap file domain '+mod['name'])
   expect=pure(vfiles[rp]) if rp in vfiles else pure(ref(rp));same(bi['target'],expect,'child bootstrap complete module pin '+mod['name'])
 # Verify the root's lossless data-only archive against every already-reviewed actual entry.
 import base64
 package=load(D/'FIXTURE_BYTES.json');fields(package,'entries original_root relocated_execution_authorized schema scientific_results scope source_namespace source_report','closed data-only package')
 same(package['original_root'],str(F),'package literal historical root');same(package['schema'],'ri152-nonscientific-fixture-bytes-v1','package schema');same(package['relocated_execution_authorized'],False,'no execution relocation');same(package['scientific_results'],False,'package not science');same(package['source_report'],ref(P/'GUARD_REPORT.json'),'package actual report pin');same(package['source_namespace'],ref(P/'NAMESPACE.json'),'package actual namespace pin')
 same([r['relative'] for r in package['entries']],[r['relative'] for r in allfixtures],'complete1385 ordered archive bijection')
 for entry,actual in zip(package['entries'],allfixtures):
  if actual['kind']=='file':
   fields(entry,'relative kind bytes sha256 body_base64','packed regular fields '+entry['relative']);same({k:entry[k] for k in actual},actual,'packed exact file pin '+entry['relative'])
   b=base64.b64decode(entry['body_base64'],validate=True);same(b,data(F/entry['relative']),'entire packed original body '+entry['relative']);same(base64.b64encode(b).decode(),entry['body_base64'],'canonical base64 '+entry['relative'])
  else:same(entry,actual,'literal packed directory/link '+entry['relative'])
 summary.update(source_files=599,inherited_dependencies=442,runtime_files=9923,runtime_bytes=258862951,output_entries=1403,operation_entries=1406,operation_files=len(operation['identities']),vendor_entries=len(fw),vendor_files=len(vfiles),vendor_file_bytes=48024515,snapshot_bootstrap_modules=len(boot['modules']),root_vendor_modules=len(vendor['bootstrap_descriptor']['modules']),snapshot=ref(P/'PRE.stdout'),guard_report=ref(P/'GUARD_REPORT.json'),genuine_outer=ref(D/'GENUINE_OUTER.json'),lossless_fixture_package=ref(D/'FIXTURE_BYTES.json'))
 # Supplementary root conclusions are read after the independent checks.
 rootcheck=load(D/'ROOT_GUARD_CHECK.json');same(rootcheck['runtime_files'],9923,'root supplementalruntime');same(rootcheck['parent_seconds'],summary['parent_elapsed_seconds'],'root supplemental interval');same(rootcheck['fixture_entries'],1385,'root supplemental fixturecount')
 for n in ('ROOT_MANUAL_GUARD_REVIEW.json','ROOT_CHECK_TOOL.json','FIXTURE_PACK_CHECK.json'):load(D/n,False)
 result=dict(schema='ri152-independent-actual65-check-v1',status='PASS',summary=summary,checks=checks,read_inputs=sorted(reads.values(),key=lambda x:x['path']),failure_case_reconstructions=case_oracles,scope='Administrative saved-evidence and deliberately nonscientific guard fixture reconciliation only. No subject/helper replay/import, new current runtime observation, scientific numerical decoding or admission. Some messages/in-memory mutations are enforced by authenticated executed source but not separately serialized; they are not independent saved exception traces.')
 with (R/'SAVED_CHECK.json').open('xb') as f:f.write(canon(result))
 with (R/'SUMMARY.json').open('xb') as f:f.write(canon(dict(status='PASS',checks=len(checks),read_inputs=len(reads),summary=summary)))
 print(json.dumps(dict(status='PASS',checks=len(checks),read_inputs=len(reads),summary=summary),sort_keys=True))
except BaseException as exc:
 failure=dict(status='FAILED_REVIEWER_CHECK',error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()),summary=summary,checks=checks,read_inputs=sorted(reads.values(),key=lambda x:x['path']))
 with (R/('FAILED_CHECK_%02d.json'%(len(list(R.glob('FAILED_CHECK_*.json')))+1))).open('xb') as f:f.write(canon(failure))
 raise
