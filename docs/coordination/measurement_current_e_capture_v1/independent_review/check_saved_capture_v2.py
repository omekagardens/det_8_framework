"""RI186 independent administrative saved-evidence checker; no subject import/execution."""
import hashlib, json, os, stat, sys, traceback, shlex
from pathlib import Path
D=Path(__file__).resolve().parent
B=D.parent; R=B/'ri183-root-parent-capture-review-2mnanskj'
C=B/'ri170-current-e-capture-proposed-gikj2giy'; E=B/'ri154-white-execution-proposed-42_uvw15'
RR=B/'ri170-current-e-root-records-proposed-gikj2giy'; S=B/'ri141-white-bootstrap-source-h58ls076'
A=R/'RI186_REVIEW_ASSIGNMENT.json'; checks=0; observed={}; decoded=[]; sections=[]
def canonical(x): return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False,ensure_ascii=True)+'\n').encode('ascii')
def require(ok,reason):
 global checks
 checks+=1
 if not ok: raise ValueError(reason)
def equal(x,y,reason): require(canonical(x)==canonical(y),reason)
def keys(x,expected,reason): require(type(x) is dict and set(x)==set(expected),reason)
def state(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pure(row):return {k:row[k] for k in ('bytes','sha256')}
def identity(path):
 p=Path(path); require(p.is_absolute(),'absolute identity '+str(p))
 if str(p) in observed:return observed[str(p)]
 pending=list(p.parts[1:]); at=Path('/'); links=[]
 while pending:
  item=pending.pop(0)
  if item=='.':continue
  if item=='..':at=at.parent;continue
  q=at/item; st=q.lstat()
  if stat.S_ISLNK(st.st_mode):
   require(len(links)<64,'link bound'); target=os.readlink(q);links.append({'path':str(q),'target':target});t=Path(target)
   if t.is_absolute():at=Path('/');pending=list(t.parts[1:])+pending
   else:pending=list(t.parts)+pending
  else:at=q
 before=at.lstat(); require(stat.S_ISREG(before.st_mode),'regular identity '+str(at))
 h=hashlib.sha256();size=0
 with os.fdopen(os.open(at,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  equal(state(os.fstat(f.fileno())),state(before),'identity opened')
  while True:
   b=f.read(1024*1024)
   if not b:break
   h.update(b);size+=len(b)
  equal(state(os.fstat(f.fileno())),state(before),'identity descriptor stable')
 equal(state(at.lstat()),state(before),'identity final stable')
 require(size==before.st_size and p.resolve(strict=True)==at,'identity complete resolution')
 for link in links:equal(os.readlink(link['path']),link['target'],'identity link stable')
 row={'path':str(p),'resolved_path':str(at),'symlink_chain':links,'bytes':size,'sha256':h.hexdigest(),'state':state(before)}
 observed[str(p)]=row;return row
def ref(p): return {k:identity(p)[k] for k in ('path','bytes','sha256')}
def verify(row,full=False):
 r=identity(row['path']); equal(r if full else pure(r),row if full else pure(row),'opaque identity '+row['path']);return r
def load(p):
 p=Path(p);b=p.read_bytes();equal(digest(b),pure(identity(p)),'metadata stable read '+str(p))
 def pairs(items):
  out={}
  for k,v in items:
   require(k not in out,'duplicate metadata key');out[k]=v
  return out
 def bad(v): raise ValueError('nonfinite metadata '+v)
 x=json.loads(b,object_pairs_hook=pairs,parse_constant=bad);decoded.append(str(p));return x
def save(name,x):
 with (D/name).open('xb') as f:f.write(canonical(x));f.flush();os.fsync(f.fileno())
def tree(root,pins=False):
 rows=[];root=Path(root)
 for parent,dirs,files in os.walk(root,followlinks=False):
  for name in sorted(dirs+files):
   p=Path(parent)/name;s=p.lstat();row={'relative':p.relative_to(root).as_posix()}
   if stat.S_ISLNK(s.st_mode):row.update(kind='symlink',target=os.readlink(p))
   elif stat.S_ISDIR(s.st_mode):row['kind']='directory'
   else:
    require(stat.S_ISREG(s.st_mode),'ordinary tree member');row['kind']='file'
    if pins:row.update(pure(identity(p)))
   rows.append(row)
 return sorted(rows,key=lambda r:r['relative'])
def binding(row):
 keys(row,('named_path','resolved_path','symlink_chain','target'),'binding fields')
 fresh=identity(row['named_path'])
 equal([fresh['resolved_path'],fresh['symlink_chain'],pure(fresh)], [row['resolved_path'],row['symlink_chain'],row['target']],'complete named/resolved binding')
def check():
 equal(pure(identity(A)),{'bytes':4541,'sha256':'db880dbc1be4d2d315cd301b2a7c14e131cda902be6adcf5fbf3ad93bc28dc4c'},'assignment anchor')
 assignment=load(A);equal(assignment['reservation'],str(D),'exclusive reservation')
 for row in assignment['pins']:verify(row)
 pf=load(R/'CAPTURE_PREFLIGHT.json'); source=load(R/'CAPTURE_SOURCE_ADJUDICATION.json')
 for container in [pf,source]:
  for row in container.values():
   if type(row) is dict and set(row)=={'path','bytes','sha256'}:verify(row)
 layout=load(pf['observation']['path']); post=load(R/'CAPTURE_POST_CUSTODY.json')
 equal(post['observation'],layout,'whole external PRE/POST custody');require(post['admission_and_source_review_unchanged'] is True,'post custody scope')
 equal(layout['E'],str(E),'installed E');require(layout['scientific_decode'] is False and layout['subject_execution'] is False,'preflight scope')
 equal({k:len(layout[k]) for k in ('sources','copies','vendor','tools','vendor_namespace','files','directories')},{'sources':612,'copies':48,'vendor':1810,'tools':4,'vendor_namespace':195,'files':48,'directories':8},'layout complete counts')
 for group in ('sources','copies','vendor','tools'):
  require(len({r['path'] for r in layout[group]})==len(layout[group]),'no duplicate '+group)
  for row in layout[group]:verify(row,True)
  sections.append({'name':group,'identities':len(layout[group])})
 for n in layout['vendor_namespace']:
  p=Path(n['path']);equal(state(p.lstat()),n['state'],'vendor namespace state')
  if n['kind']=='directory':require(p.is_dir() and not p.is_symlink(),'vendor directory');equal(sorted(os.listdir(p)),n['entries'],'complete vendor members')
  else:equal(n['kind'],'symlink','vendor other kind');equal(os.readlink(p),n['target'],'vendor literal link')
 for p in layout['absent']:require(not os.path.lexists(p),'vendor absence')
 vendor_names={r['path'] for r in layout['vendor']}|{r['path'] for r in layout['vendor_namespace']}
 for row in layout['vendor_namespace']:
  if row['kind']=='directory':require(all(str(Path(row['path'])/n) in vendor_names for n in row['entries']),'vendor complete parent-child closure')
 equal(tree(E),sorted([{'relative':n,'kind':'file'} for n in layout['files']]+[{'relative':n,'kind':'directory'} for n in layout['directories']],key=lambda r:r['relative']),'full installed E namespace')
 equal(sorted(str(Path(r['path']).relative_to(E)) for r in layout['copies']),layout['files'],'E exact copy domain')
 for n in ('tmp','runs/normal','runs/optimized'):equal(list((E/n).iterdir()),[],'empty pre-profile namespace '+n)
 custody=load(R/'CAPTURE_ADMISSION_CUSTODY.json')
 for row in custody.values():verify(row,True)
 card=load(RR/'ADMIT_CAPTURE.json');complete=load(C/'COMPLETE.json');attempt=load(C/'ATTEMPT.json');outer=load(R/'GENUINE_OUTER.json'); genuine=load(R/'GENUINE_CAPTURE_COMPLETE.json');initial=load(R/'GENUINE_CAPTURE_INITIAL.json')
 keys(card,('schema','status','phase','sources','source_review','packet','output','environment_root','bootstrap','bootstrap_host_preflight','host','baseline_acceptance','normal_acceptance','profiles_acceptance','guard_admission','bounds','genuine_outer_required'),'closed admission')
 equal(card['schema'],'ri141-root-preparation-admission-v1','admission schema');equal(card['status'],'AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION','admission scope')
 equal(card['bounds'],{'snapshot_seconds':180,'profile_seconds':30,'guard_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864,'driver_soft_seconds':900,'genuine_outer_timeout_seconds':960},'all unchanged limits')
 equal([card[k] for k in ('baseline_acceptance','normal_acceptance','profiles_acceptance','guard_admission')],[None]*4,'no later stage admission')
 equal([card['phase'],card['output'],card['environment_root']],['capture',str(C),str(E)],'capture binding');require(card['genuine_outer_required'] is True,'genuine required')
 equal(card['source_review'],ref(R/'CAPTURE_SOURCE_ADJUDICATION.json'),'source review binding');equal(card['bootstrap_host_preflight'],ref(R/'CAPTURE_PREFLIGHT.json'),'host preflight binding')
 env={'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(E/'tmp'),'TZ':'UTC','VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
 equal(layout['environment'],env,'exact controlled environment')
 vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
 command=[vendor,'-I','-B',str(S/'prepare.py'),'--admission',str(RR/'ADMIT_CAPTURE.json')]
 expected_argv=['/usr/bin/env','-i']+[k+'='+v for k,v in sorted(env.items())]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+command
 equal(genuine['dispatch']['outer_argv'],expected_argv,'genuine complete outer argv')
 equal(shlex.split(genuine['dispatch']['exec_command']['cmd']),expected_argv,'literal dispatched shell equals argv')
 equal(genuine['dispatch']['exec_command'],{'cmd':genuine['dispatch']['exec_command']['cmd'],'login':False,'max_output_tokens':2000,'workdir':str(RR),'yield_time_ms':1000},'genuine dispatch options')
 equal(initial['dispatch'],genuine['dispatch'],'initial complete dispatch');equal(initial['initial'],genuine['initial'],'initial raw session')
 equal(genuine['initial']['session_id'],66579,'genuine session');equal(genuine['terminal'],{'chunk_id':'5c0651','wall_time_seconds':0.000007542,'exit_code':0,'original_token_count':0,'output':''},'actual terminal receipt')
 require('exit_code' not in genuine['initial'] and genuine['initial']['output']=='','initial remains nonterminal');require(genuine['dispatch']['single_attempt'] is True,'one dispatch')
 equal(genuine['dispatch']['environment'],env,'dispatch env');equal(genuine['dispatch']['admission'],ref(RR/'ADMIT_CAPTURE.json'),'dispatch exact admission');verify(genuine['dispatch']['command_proposal'])
 keys(outer,('schema','status','command','environment','exit_code','completion','raw_tool_receipt','external_timeout_seconds'),'closed genuine outer')
 equal(outer,{'schema':'ri133-root-genuine-outer-v1','status':'ACTUAL_TOOL_COMPLETION','command':command,'environment':env,'exit_code':0,'completion':ref(C/'COMPLETE.json'),'raw_tool_receipt':ref(R/'GENUINE_CAPTURE_COMPLETE.json'),'external_timeout_seconds':960},'complete outer relation')
 keys(complete,('schema','phase','status','command','environment','admission','sources','artifacts','first_error','independent_tail_errors','elapsed_seconds','scientific_targets_executed','actual_data_admitted','full32_qualified','ret_paused','runtime_acceptance_created','genuine_outer_created'),'closed parent result')
 equal(complete['schema'],'ri133-preparation-completion-v1','completion schema');equal(complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','completion stage');equal(complete['command'],command,'parent command');equal(complete['environment'],env,'parent env')
 equal(complete['phase'],'capture','parent phase');equal(complete['admission'],ref(RR/'ADMIT_CAPTURE.json'),'parent admission');equal(complete['sources'],card['sources'],'parent complete sources')
 equal([complete['first_error'],complete['independent_tail_errors']],[None,[]],'all parent errors/tails');require(type(complete['elapsed_seconds']) is float and 0<complete['elapsed_seconds']<900,'parent elapsed limit')
 for k in ('scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created'):require(complete[k] is False,'scope '+k)
 require(complete['ret_paused'] is True,'RET paused')
 equal(attempt,{'schema':'ri133-preparation-attempt-v1','phase':'capture','sources':card['sources'],'admission':ref(RR/'ADMIT_CAPTURE.json'),'environment':env,'scientific_execution':False},'entire parent attempt')
 equal(sorted(card['sources']),['DEPENDENCIES.source-only.json','prepare.py','runtime_metadata.py'],'exact source triple')
 for n,row in card['sources'].items():equal(pure(identity(S/n)),row,'preparation source '+n)
 artifacts={'PRE':'PRE.stdout','POST':'POST.stdout','PRE_completion':'PRE.COMPLETION.json','POST_completion':'POST.COMPLETION.json','checks':'CHECKS.json','namespace':'NAMESPACE.json'}
 equal(complete['artifacts'],{k:ref(C/n) for k,n in artifacts.items()},'all artifact role/path/pins')
 ns=load(C/'NAMESPACE.json');keys(ns,('schema','root','entries','excluded_not_yet_written'),'namespace fields')
 equal([ns['schema'],ns['root'],ns['excluded_not_yet_written']],['ri133-retained-namespace-v1',str(C),['NAMESPACE.json','COMPLETE.json']],'namespace closure')
 finaltree=tree(C,True);equal(finaltree,sorted(ns['entries']+[{'relative':n,'kind':'file',**pure(identity(C/n))} for n in ('NAMESPACE.json','COMPLETE.json')],key=lambda r:r['relative']),'saved final exact namespace')
 equal([r['relative'] for r in finaltree],sorted(['ATTEMPT.json','CHECKS.json','NAMESPACE.json','COMPLETE.json']+[label+suffix for label in ('PRE','POST') for suffix in ('.ATTEMPT.json','.COMPLETION.json','.stdout','.stderr')]),'literal twelve outputs')
 final_saved=load(R/'OPERATION_FINAL_IDENTITIES.json');equal(final_saved['root'],str(C),'root saved output root');equal(final_saved['entries'],finaltree,'root complete output entries')
 for row in final_saved['identities']:verify(row,True)
 equal(load(C/'CHECKS.json'),{'post_metadata':'PASS','source_and_admission_postcheck':'PASS'},'closed checks labels; independently reconstructed below')
 monitors=[]
 for label in ('PRE','POST'):
  child=load(C/(label+'.COMPLETION.json'));a=load(C/(label+'.ATTEMPT.json'))
  keys(child,('child_exit_code','command','elapsed_seconds','environment','final_sample_gap_passed','final_sample_to_reap_gap_seconds','first_error','monitor_attempts','passed','peak_sampled_rss_kib','samples','stderr','stdout','stop_reason','tail_errors','wall_seconds'),'closed child result')
  expected=[vendor,'-I','-B',str(S/'prepare.py'),'--snapshot',str(RR/'ADMIT_CAPTURE.json')]
  equal(child['command'],expected,'child complete argv');equal(child['environment'],env,'child env');equal(child['wall_seconds'],180,'child wall bound')
  keys(a,('command','environment','wall_seconds','pid_owner','scientific_target_entry'),'child attempt fields')
  equal([a['command'],a['environment'],a['wall_seconds'],a['scientific_target_entry']],[expected,env,180,False],'full child attempt relation');require(type(a['pid_owner']) is int and a['pid_owner']>0,'parent pid receipt only')
  equal([child['child_exit_code'],child['first_error'],child['stop_reason'],child['tail_errors'],child['passed']],[0,None,None,[],True],'child all error/terminal predicates')
  require(type(child['elapsed_seconds']) is float and 0<child['elapsed_seconds']<=180,'actual child duration')
  require(type(child['samples']) is list and len(child['samples'])>0 and len(child['samples'])==len(child['monitor_attempts']),'complete monitor one-to-one domain')
  previous=0
  for n,(sample,raw) in enumerate(zip(child['samples'],child['monitor_attempts'])):
   keys(sample,('elapsed_seconds','gap_seconds','rss_kib'),'sample fields');keys(raw,('elapsed_seconds','returncode','stdout','stderr'),'raw ps fields')
   require(type(raw['returncode']) is int and raw['returncode']==0 and raw['stderr']=='','ps successful observation');require(type(raw['stdout']) is str and raw['stdout'].strip().isdigit(),'ps decimal output')
   equal(sample['elapsed_seconds'],raw['elapsed_seconds'],'sample raw stamp');require(type(sample['rss_kib']) is int and sample['rss_kib']==int(raw['stdout']) and 0<=sample['rss_kib']<=524288,'RSS raw and bound')
   require(type(sample['elapsed_seconds']) is float and type(sample['gap_seconds']) is float and 0<=sample['gap_seconds']<=.1 and sample['elapsed_seconds']>=previous,'initial/interior gap and order')
   require(abs(sample['elapsed_seconds']-previous-sample['gap_seconds'])<1e-9,'saved timestamp subtraction');previous=sample['elapsed_seconds']
  equal(child['peak_sampled_rss_kib'],max(r['rss_kib'] for r in child['samples']),'complete actual peak')
  require(type(child['final_sample_to_reap_gap_seconds']) is float and 0<=child['final_sample_to_reap_gap_seconds']<=.1 and child['final_sample_gap_passed'] is True,'final sample to wait bound')
  require(abs(child['elapsed_seconds']-previous-child['final_sample_to_reap_gap_seconds'])<1e-9,'final reap arithmetic')
  for stream in ('stdout','stderr'):equal(child[stream],ref(C/(label+'.'+stream)),'stream exact role pin');require(child[stream]['bytes']<=67108864,'bounded final stream')
  equal(child['stderr']['bytes'],0,'empty stderr')
  monitors.append({'label':label,'samples':len(child['samples']),'elapsed_seconds':child['elapsed_seconds'],'peak_rss_kib':child['peak_sampled_rss_kib'],'max_gap_seconds':max(r['gap_seconds'] for r in child['samples']),'final_gap_seconds':child['final_sample_to_reap_gap_seconds'],'parent_pid_only':a['pid_owner']})
 require((C/'PRE.stdout').read_bytes()==(C/'POST.stdout').read_bytes(),'entire PRE/POST byte equality')
 snap=load(C/'PRE.stdout');equal(snap,load(C/'POST.stdout'),'all decoded metadata equality')
 keys(snap,('actual_data_admission','cache_scope','host_bootstrap','interpreter','optional_namespaces','preobserved_dyld_routes','root_counts','runtime_inventory','schema','scientific_execution','selection','sources'),'entire snapshot field domain')
 equal(snap['schema'],'ri133-complete-current-metadata-snapshot-v1','snapshot schema');require(snap['actual_data_admission'] is False and snap['scientific_execution'] is False,'snapshot scope')
 deps=load(S/'DEPENDENCIES.source-only.json')
 for name in ('historical_runtime','historical_interpreter','historical_interpreter_provenance','historical_optional_namespaces','bootstrap_selection_provenance'):verify(deps[name]);require(deps[name] in deps['opaque_files'],'premise present in opaque closure')
 equal(snap['runtime_inventory'],load(deps['historical_runtime']['path']),'entire historical runtime identity bridge')
 equal(snap['interpreter'],load(deps['historical_interpreter']['path']),'entire historical candidate binding')
 provenance=load(deps['historical_interpreter_provenance']['path']);equal(provenance['schema'],'ri121-reviewed-runtime-metadata-candidate-handoff-v1','candidate binding provenance schema');equal(provenance['status'],'METADATA_CANDIDATE_INDEPENDENTLY_VERIFIED_NOT_RUNTIME_ADMITTED','candidate binding provenance scope');equal([r for r in provenance['files'] if r['path']==deps['historical_interpreter']['path']],[deps['historical_interpreter']],'authentic full binding reference')
 equal(snap['optional_namespaces']['directories'],load(deps['historical_optional_namespaces']['path'])['directories'],'historical optional member domain')
 equal(snap['sources'],{'opaque_files':deps['opaque_files'],'packet_namespace':deps['packet_namespace'],'science_files_opened_as_opaque_hash_streams_only':True,'scientific_body_decode':False},'exact original-source-only snapshot')
 for row in deps['opaque_files']:verify(row)
 equal(tree(Path(deps['packet_root']),True),deps['packet_namespace'],'complete original packet namespace')
 equal(len(deps['opaque_files']),442,'historical opaque closure count')
 bootstrap=snap['host_bootstrap']['bootstrap'];equal(bootstrap['named'],card['bootstrap'],'named bootstrap');equal(bootstrap['actual'],card['bootstrap'],'actual descriptor supplier');binding(bootstrap['named']);binding(bootstrap['actual'])
 equal([bootstrap['executable'],bootstrap['isolated'],bootstrap['dont_write_bytecode'],bootstrap['optimize']],[vendor,1,1,0],'actual saved bootstrap flags')
 equal(pf['selected_interpreter_binding'],layout['selected_interpreter_binding'],'selected preflight supplier');verify(layout['selected_interpreter_binding'],True)
 equal(layout['selected_interpreter_binding'],deps['selected_bootstrap_binding'],'historical selected vendor full state')
 equal(load(deps['bootstrap_selection_provenance']['path'])['selected_bootstrap_binding'],deps['selected_bootstrap_binding'],'selected vendor genuine historical provenance')
 equal({'uname':snap['host_bootstrap']['uname'],'system_version':snap['host_bootstrap']['system_version']},card['host'],'host complete contract');equal(list(os.uname()),card['host']['uname'],'current host uname');verify(card['host']['system_version']);equal(layout['host']['uname'],card['host']['uname'],'outer host relation');require(layout['host']['exit_code']==0 and layout['host']['stderr']=='','saved sw_vers observation')
 names=[];module_bindings=0
 for row in bootstrap['modules']:
  names.append(row['name']);keys(row,('name','file','origin','cached','loader_type')+(('binding',) if row['file'] is not None else ()),'module descriptor exact fields')
  if row['file'] is not None:equal(row['binding']['named_path'],row['file'],'module binding role');binding(row['binding']);module_bindings+=1
 equal(names,sorted(set(names)),'complete sorted distinct module descriptors')
 runtime=snap['runtime_inventory']; selection=snap['selection']['files'];equal(snap['selection']['status'],'CURRENT_OPAQUE_SELECTION_NOT_PROVEN_IMPORT_TRACE','selection scope')
 equal([r['path'] for r in selection],[r['path'] for r in runtime['files']],'full ordered selection domain');equal(len(selection),9923,'runtime count')
 saved_runtime=load(R/'RUNTIME_POST_IDENTITIES.json');equal([r['path'] for r in saved_runtime['identities']],[r['path'] for r in runtime['files']],'root runtime domain')
 pyc=0
 for row,sel,saved in zip(runtime['files'],selection,saved_runtime['identities']):
  fresh=verify(row);equal(fresh,saved,'fresh versus root final runtime identity')
  expected={'path':row['path'],**dict(zip(('device','inode','mode','bytes','mtime_ns','ctime_ns'),[fresh['state'][i] for i in (0,1,2,4,5,6)]))}
  if row['path'].endswith('.pyc'):
   with open(row['path'],'rb') as f:header=f.read(16)
   expected.update(pyc_first16_hex=header.hex(),pyc_payload_not_parsed_or_executed=True);pyc+=1
  equal(sel,expected,'entire saved selection/header metadata')
 paths=set();links=[];counts=[]
 for root in runtime['roots']:
  rows=tree(root);count=0
  for row in rows:
   p=Path(root)/row['relative']
   if row['kind']=='file':paths.add(str(p));count+=1
   elif row['kind']=='symlink':
    links.append({'path':str(p),'target':row['target']});resolved=p.resolve(strict=True)
    if resolved.is_file():paths.add(str(resolved))
    else:require(resolved.is_dir(),'runtime link resolves regular or dir')
  counts.append({'root':root,'regular_files':count})
 paths.update(runtime['extra_files']);equal(sorted(paths),[r['path'] for r in runtime['files']],'fresh full recursive runtime membership plus13 extras');equal(counts,snap['root_counts'],'all runtime root counts');equal(sorted(links,key=lambda x:x['path']),runtime['symlinks'],'entire runtime link domain')
 for p in runtime['absent_paths']+snap['preobserved_dyld_routes']['absent_paths']:require(not os.path.lexists(p),'required runtime/dyld absence')
 for row in runtime['symlinks']+snap['preobserved_dyld_routes']['symlinks']:equal(os.readlink(row['path']),row['target'],'runtime/dyld literal link')
 for row in runtime['loader_bindings']+[snap['interpreter']]:binding(row)
 for space in snap['optional_namespaces']['directories']:
  rows=[]
  for row in tree(space['root']):
   item={'relative_path':row['relative'],'kind':{'file':'regular','directory':'directory','symlink':'symlink'}[row['kind']]}
   if row['kind']=='symlink':item['literal_target']=row['target']
   rows.append(item)
  equal(rows,space['recursive_members_no_symlink_traversal'],'complete optional namespace')
 # Final state/link replay for every opaque file read; excludes atime intentionally.
 for r in list(observed.values()):
  equal(state(Path(r['resolved_path']).lstat()),r['state'],'final all-file state stability')
  require(Path(r['path']).resolve(strict=True)==Path(r['resolved_path']),'final path resolution')
  for link in r['symlink_chain']:equal(os.readlink(link['path']),link['target'],'final ordered link stability')
 equal(tree(C,True),finaltree,'final output namespace stability')
 return {'status':'ALL_INDEPENDENT_ADMINISTRATIVE_PREDICATES_PASSED','monitors':monitors,'parent_seconds':complete['elapsed_seconds'],'runtime_files':len(runtime['files']),'runtime_bytes':sum(r['bytes'] for r in runtime['files']),'pyc_opaque_headers':pyc,'bootstrap_module_descriptors':len(names),'bootstrap_file_bindings':module_bindings,'source_groups':sections,'capture_entries':len(finaltree),'installed_e_files':48,'installed_e_directories':8,'snapshot_pin':ref(C/'PRE.stdout'),'same_PRE_POST_bytes':True,'scientific_body_decode':False,'subject_vendor_helper_execution':False,'new_runtime_capture':False,'runtime_baseline_acceptance_created':False}
try:
 result=check();result.update(predicates=checks,opaque_unique_identities=len(observed),decoded_administrative_files=sorted(set(decoded)),administrative_python=sys.executable)
 save('IDENTITIES.json',{'identities':[observed[k] for k in sorted(observed)],'scientific_body_decode':False})
 save('ADMIN_CHECK.json',result);print(json.dumps({k:result[k] for k in ('status','predicates','opaque_unique_identities','runtime_files','runtime_bytes','capture_entries','monitors')},sort_keys=True))
except BaseException as exc:
 result={'status':'FAILED_ADMINISTRATIVE_CHECK','predicates_completed':checks,'error_type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc(),'decoded_administrative_files':decoded,'opaque_unique_identities':len(observed)}
 save('ADMIN_FAILURE_V2.json',result);print(result['traceback'],file=sys.stderr);raise
