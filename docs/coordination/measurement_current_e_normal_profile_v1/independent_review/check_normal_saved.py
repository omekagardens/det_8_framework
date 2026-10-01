"""RI190 independent administrative normal-profile saved-evidence checker; no subject import/execution."""
import hashlib, json, os, stat, sys, traceback, shlex
from pathlib import Path
D=Path(__file__).resolve().parent
B=D.parent; R=B/'ri188-root-endpoint-profile-review-1jg_i948'
C=B/'ri170-current-e-profile-normal-proposed-gikj2giy'; E=B/'ri154-white-execution-proposed-42_uvw15'
RR=B/'ri170-current-e-root-records-proposed-gikj2giy'; S=B/'ri141-white-bootstrap-source-h58ls076'
A=R/'RI190_REVIEW_ASSIGNMENT.json'; checks=0; observed={}; decoded=[]; sections=[]
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
 equal(pure(identity(A)),{'bytes':6859,'sha256':'8bbc25f3bf896d36c87686c96688cf18df1f8304f7a9f46d68addfdfa1cb2d21'},'assignment anchor')
 assignment=load(A);equal(assignment['reservation'],str(D),'exclusive reservation')
 for row in [assignment['admission'],assignment['baseline']]+list(assignment['sources'].values()):verify(row)
 pf=load(R/'PROFILE_NORMAL_PREFLIGHT.json'); source=load(R/'PROFILE_NORMAL_SOURCE_ADJUDICATION.json')
 for container in [pf,source]:
  for row in container.values():
   if type(row) is dict and set(row)=={'path','bytes','sha256'}:verify(row)
 layout=load(pf['observation']['path']); post=load(R/'PROFILE_NORMAL_POST_CUSTODY.json')
 equal(post['observation'],layout,'whole external PRE/POST custody');require(post['admission_and_source_review_unchanged'] is True,'post custody scope')
 equal(layout['E'],str(E),'installed E');require(layout['scientific_decode'] is False and layout['subject_execution'] is False,'preflight scope')
 equal({k:len(layout[k]) for k in ('sources','copies','vendor','tools','vendor_namespace','files','directories')},{'sources':623,'copies':48,'vendor':1810,'tools':4,'vendor_namespace':195,'files':48,'directories':8},'layout complete counts')
 for group in ('sources','copies','vendor','tools','runtime'):
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
 custody=load(R/'PROFILE_NORMAL_ADMISSION_CUSTODY.json')
 for row in custody.values():verify(row,True)
 card=load(RR/'ADMIT_PROFILE_NORMAL.json');complete=load(C/'COMPLETE.json');attempt=load(C/'ATTEMPT.json');outer=load(R/'GENUINE_OUTER.json'); genuine={'dispatch':load(R/'PROFILE_NORMAL_DISPATCH.json'),'initial':load(R/'GENUINE_PROFILE_NORMAL_INITIAL.json'),'terminal':load(R/'GENUINE_PROFILE_NORMAL_COMPLETE.json')};initial=genuine['initial']
 keys(card,('schema','status','phase','sources','source_review','packet','output','environment_root','bootstrap','bootstrap_host_preflight','host','baseline_acceptance','normal_acceptance','profiles_acceptance','guard_admission','bounds','genuine_outer_required'),'closed admission')
 equal(card['schema'],'ri141-root-preparation-admission-v1','admission schema');equal(card['status'],'AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION','admission scope')
 equal(card['bounds'],{'snapshot_seconds':180,'profile_seconds':30,'guard_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864,'driver_soft_seconds':900,'genuine_outer_timeout_seconds':960},'all unchanged limits')
 equal([card[k] for k in ('normal_acceptance','profiles_acceptance','guard_admission')],[None]*3,'no later stage admission');equal(card['baseline_acceptance'],assignment['baseline'],'independently accepted baseline required')
 equal([card['phase'],card['output'],card['environment_root']],['profile_normal',str(C),str(E)],'capture binding');require(card['genuine_outer_required'] is True,'genuine required')
 equal(card['source_review'],ref(R/'PROFILE_NORMAL_SOURCE_ADJUDICATION.json'),'source review binding');equal(card['bootstrap_host_preflight'],ref(R/'PROFILE_NORMAL_PREFLIGHT.json'),'host preflight binding')
 env={'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(E/'tmp'),'TZ':'UTC','VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
 equal(layout['environment'],env,'exact controlled environment')
 vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
 command=[vendor,'-I','-B',str(S/'prepare.py'),'--admission',str(RR/'ADMIT_PROFILE_NORMAL.json')]
 expected_argv=['/usr/bin/env','-i']+[k+'='+v for k,v in sorted(env.items())]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+command
 equal(genuine['dispatch']['outer_argv'],expected_argv,'genuine complete outer argv')
 equal(shlex.split(genuine['dispatch']['exec_command']['cmd']),expected_argv,'literal dispatched shell equals argv')
 equal(genuine['dispatch']['exec_command'],{'cmd':genuine['dispatch']['exec_command']['cmd'],'login':False,'max_output_tokens':2000,'workdir':str(RR),'yield_time_ms':1000},'genuine dispatch options')
 equal(initial['chunk_id'],'2b5d3e','genuine initial chunk')
 equal(genuine['initial']['session_id'],63779,'genuine session');equal(genuine['terminal'],{'chunk_id':'9aba56','wall_time_seconds':0.736710916,'exit_code':0,'original_token_count':0,'output':''},'actual terminal receipt')
 require('exit_code' not in genuine['initial'] and genuine['initial']['output']=='','initial remains nonterminal');require(genuine['dispatch']['single_attempt'] is True,'one dispatch')
 equal(genuine['dispatch']['environment'],env,'dispatch env');equal(genuine['dispatch']['admission'],ref(RR/'ADMIT_PROFILE_NORMAL.json'),'dispatch exact admission');verify(genuine['dispatch']['command_proposal'])
 keys(outer,('schema','status','command','environment','exit_code','completion','raw_tool_receipt','external_timeout_seconds'),'closed genuine outer')
 equal(outer,{'schema':'ri133-root-genuine-outer-v1','status':'ACTUAL_TOOL_COMPLETION','command':command,'environment':env,'exit_code':0,'completion':ref(C/'COMPLETE.json'),'raw_tool_receipt':ref(R/'GENUINE_PROFILE_NORMAL_COMPLETE.json'),'external_timeout_seconds':960},'complete outer relation')
 keys(complete,('schema','phase','status','command','environment','admission','sources','artifacts','first_error','independent_tail_errors','elapsed_seconds','scientific_targets_executed','actual_data_admitted','full32_qualified','ret_paused','runtime_acceptance_created','genuine_outer_created'),'closed parent result')
 equal(complete['schema'],'ri133-preparation-completion-v1','completion schema');equal(complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','completion stage');equal(complete['command'],command,'parent command');equal(complete['environment'],env,'parent env')
 equal(complete['phase'],'profile_normal','parent phase');equal(complete['admission'],ref(RR/'ADMIT_PROFILE_NORMAL.json'),'parent admission');equal(complete['sources'],card['sources'],'parent complete sources')
 equal([complete['first_error'],complete['independent_tail_errors']],[None,[]],'all parent errors/tails');require(type(complete['elapsed_seconds']) is float and 0<complete['elapsed_seconds']<900,'parent elapsed limit')
 for k in ('scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created'):require(complete[k] is False,'scope '+k)
 require(complete['ret_paused'] is True,'RET paused')
 equal(attempt,{'schema':'ri133-preparation-attempt-v1','phase':'profile_normal','sources':card['sources'],'admission':ref(RR/'ADMIT_PROFILE_NORMAL.json'),'environment':env,'scientific_execution':False},'entire parent attempt')
 equal(sorted(card['sources']),['DEPENDENCIES.source-only.json','prepare.py','runtime_metadata.py'],'exact source triple')
 for n,row in card['sources'].items():equal(pure(identity(S/n)),row,'preparation source '+n)
 artifacts={'PROFILE':'PROFILE.stdout','PROFILE_completion':'PROFILE.COMPLETION.json','PRE':'PRE.stdout','POST':'POST.stdout','PRE_completion':'PRE.COMPLETION.json','POST_completion':'POST.COMPLETION.json','checks':'CHECKS.json','namespace':'NAMESPACE.json'}
 equal(complete['artifacts'],{k:ref(C/n) for k,n in artifacts.items()},'all artifact role/path/pins')
 ns=load(C/'NAMESPACE.json');keys(ns,('schema','root','entries','excluded_not_yet_written'),'namespace fields')
 equal([ns['schema'],ns['root'],ns['excluded_not_yet_written']],['ri133-retained-namespace-v1',str(C),['NAMESPACE.json','COMPLETE.json']],'namespace closure')
 finaltree=tree(C,True);equal(finaltree,sorted(ns['entries']+[{'relative':n,'kind':'file',**pure(identity(C/n))} for n in ('NAMESPACE.json','COMPLETE.json')],key=lambda r:r['relative']),'saved final exact namespace')
 equal([r['relative'] for r in finaltree],sorted(['ATTEMPT.json','CHECKS.json','NAMESPACE.json','COMPLETE.json']+[label+suffix for label in ('PRE','PROFILE','POST') for suffix in ('.ATTEMPT.json','.COMPLETION.json','.stdout','.stderr')]),'literal sixteen outputs')
 final_saved=load(R/'OPERATION_FINAL_IDENTITIES.json');equal(final_saved['root'],str(C),'root saved output root');equal(final_saved['entries'],finaltree,'root complete output entries')
 for row in final_saved['identities']:verify(row,True)
 saved_checks=load(C/'CHECKS.json');keys(saved_checks,('post_metadata','source_and_admission_postcheck','profile'),'closed checks');equal([saved_checks['post_metadata'],saved_checks['source_and_admission_postcheck']],['PASS','PASS'],'base check labels reconstructed below')
 monitors=[]
 for label in ('PRE','PROFILE','POST'):
  child=load(C/(label+'.COMPLETION.json'));a=load(C/(label+'.ATTEMPT.json'))
  keys(child,('child_exit_code','command','elapsed_seconds','environment','final_sample_gap_passed','final_sample_to_reap_gap_seconds','first_error','monitor_attempts','passed','peak_sampled_rss_kib','samples','stderr','stdout','stop_reason','tail_errors','wall_seconds'),'closed child result')
  limit=30 if label=='PROFILE' else 180
  expected=([str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python'),'-I','-B',str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py')] if label=='PROFILE' else [vendor,'-I','-B',str(S/'prepare.py'),'--snapshot',str(RR/'ADMIT_PROFILE_NORMAL.json')])
  equal(child['command'],expected,'child complete argv');equal(child['environment'],env,'child env');equal(child['wall_seconds'],limit,'child wall bound')
  keys(a,('command','environment','wall_seconds','pid_owner','scientific_target_entry'),'child attempt fields')
  equal([a['command'],a['environment'],a['wall_seconds'],a['scientific_target_entry']],[expected,env,limit,False],'full child attempt relation');require(type(a['pid_owner']) is int and a['pid_owner']>0,'parent pid receipt only')
  equal([child['child_exit_code'],child['first_error'],child['stop_reason'],child['tail_errors'],child['passed']],[0,None,None,[],True],'child all error/terminal predicates')
  require(type(child['elapsed_seconds']) is float and 0<child['elapsed_seconds']<=limit,'actual child duration')
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
 equal([r['path'] for r in selection],[r['path'] for r in runtime['files']],'full ordered selection domain');equal(len(selection),9923,'runtime count');equal(layout['runtime'],load(R/'RUNTIME_POST_IDENTITIES.json')['identities'],'complete preflight runtime versus final identity domain')
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
 # Reconstruct the complete accepted baseline chain and namespace independently.
 baseline=load(card['baseline_acceptance']['path'])
 keys(baseline,('schema','status','stage','sources','packet','environment_root','completions','genuine_outer','independent_review','scientific_execution'),'closed baseline acceptance')
 equal([baseline['schema'],baseline['status'],baseline['stage'],baseline['scientific_execution']],['ri133-root-preparation-stage-review-v1','ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','baseline',False],'baseline acceptance scope')
 for field in ('sources','packet','environment_root'):equal(baseline[field],card[field],'baseline same current stage binding')
 equal(list(baseline['completions']),['capture'],'baseline completion domain');equal(list(baseline['genuine_outer']),['capture'],'baseline outer domain')
 verify(baseline['independent_review']);verify(baseline['completions']['capture']);verify(baseline['genuine_outer']['capture'])
 bc=load(baseline['completions']['capture']['path']);bo=load(baseline['genuine_outer']['capture']['path']);bp=Path(baseline['completions']['capture']['path']).parent
 equal([bc['phase'],bc['status'],bc['first_error'],bc['independent_tail_errors']],['capture','CAPTURED_FOR_INDEPENDENT_REVIEW',None,[]],'accepted baseline actual outcome')
 for field in ('sources','environment'):equal(bc[field],complete[field],'baseline sources and controlled environment')
 equal(bo['completion'],baseline['completions']['capture'],'baseline genuine completion');equal(bo['command'],bc['command'],'baseline genuine command');equal(bo['environment'],env,'baseline genuine environment');equal([bo['schema'],bo['status'],bo['exit_code'],bo['external_timeout_seconds']],['ri133-root-genuine-outer-v1','ACTUAL_TOOL_COMPLETION',0,960],'baseline actual outer schema/status/limits');verify(bo['raw_tool_receipt'])
 for row in bc['artifacts'].values():verify(row)
 bns=load(bc['artifacts']['namespace']['path']);equal(bns['root'],str(bp),'baseline namespace root');equal(bns['excluded_not_yet_written'],['NAMESPACE.json','COMPLETE.json'],'baseline final exclusions')
 equal(tree(bp,True),sorted(bns['entries']+[{'relative':n,'kind':'file',**pure(identity(bp/n))} for n in ('NAMESPACE.json','COMPLETE.json')],key=lambda x:x['relative']),'entire accepted baseline namespace')
 require((C/'PRE.stdout').read_bytes()==Path(bc['artifacts']['POST']['path']).read_bytes(),'normal PRE equals full accepted baseline bytes')
 equal(layout['accepted_baseline'],card['baseline_acceptance'],'preflight baseline pin')
 rootdecision=B/'ri183-root-parent-capture-review-2mnanskj/RI186_ROOT_ADJUDICATION.json'
 equal(pure(identity(rootdecision)),{'bytes':2455,'sha256':'ac8ffe54952e49ad9534c4b8da612e8c2371213ff32d1232244a133a2492e4ef'},'root independently adjudicated RI186 anchor')
 # Interpret saved normal runtime/profile fields; no executing any scientific or runtime subject.
 profile=load(C/'PROFILE.stdout')
 keys(profile,('boundary','decimal','hashlib','modules','profile_after','profile_before','schema','scientific_targets_imported_or_executed','startup','uname'),'closed entire profile')
 equal([profile['schema'],profile['scientific_targets_imported_or_executed'],profile['boundary']],['ri121-installed-runtime-profile-observation-v1',False,'Installed-runtime observation under pinned supplier, cache-selection and host premises; no scientific qualification.'],'precise profile scope')
 venv=str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env');stdlib='/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11'
 expected_runtime={'base_exec_prefix':'/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11','base_prefix':'/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11','byteorder':'little','dont_write_bytecode':1,'exec_prefix':venv,'executable':venv+'/bin/python','implementation':'cpython','isolated':1,'optimize':0,'path':[str(Path(stdlib).parent/'python311.zip'),stdlib,stdlib+'/lib-dynload',venv+'/lib/python3.11/site-packages'],'prefix':venv,'version':'3.11.6 (main, Nov  2 2023, 04:39:43) [Clang 14.0.3 (clang-1403.0.22.14.1)]','version_info':[3,11,6,'final',0]}
 equal(profile['profile_before'],expected_runtime,'entire before runtime observation');equal(profile['profile_after'],expected_runtime,'entire after runtime observation');equal(profile['uname'],snap['host_bootstrap']['uname'],'profile same host')
 equal(profile['startup'],{'distutils_hook_loaded':True,'enable_user_site':False,'site_prefixes':[venv],'sitecustomize_loaded':True,'usercustomize_loaded':False},'complete startup observation')
 decimal=profile['decimal'];keys(decimal,('decimal_class_is_fallback','extension_import_error','extension_loaded','fallback_loaded','fraction_class_module'),'full decimal report')
 equal([decimal[k] for k in ('decimal_class_is_fallback','extension_loaded','fallback_loaded','fraction_class_module')],[True,False,True,'fractions'],'accepted fallback observation');keys(decimal['extension_import_error'],('message','type'),'entire import error');equal(decimal['extension_import_error']['type'],'ImportError','observed import refusal type')
 # Deliberately split the entire three-line record and rebuild it, rather than use the subject parser.
 message=decimal['extension_import_error']['message'];require(type(message) is str,'dyld message string');lines=message.split('\n');equal(len(lines),3,'exact complete dyld lines')
 ext=stdlib+'/lib-dynload/_decimal.cpython-311-darwin.so'
 equal(lines[0],'dlopen('+ext+', 0x0002): Library not loaded: /opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib','entire dyld initial line')
 prefix='  Referenced from: <';require(lines[1].startswith(prefix),'dyld image prefix');guid,separator,tail=lines[1][len(prefix):].partition('> ');equal(tail,ext,'entire referenced image path');equal(separator,'> ','image delimiter')
 groups=guid.split('-');equal([len(g) for g in groups],[8,4,4,4,12],'image UUID groups');require(all(c in '0123456789ABCDEF' for g in groups for c in g),'image UUID alphabet')
 reasonprefix='  Reason: tried: ';require(lines[2].startswith(reasonprefix),'full attempts prefix');rest=lines[2][len(reasonprefix):]
 ordered=[]
 while rest:
  require(rest.startswith("'/"),'absolute quoted attempt');path,sep,remaining=rest[1:].partition("' (");equal(sep,"' (",'attempt path separator');reason,end,remaining=remaining.partition(')');equal(end,')','closed reason')
  require(reason in ('no such file','no such file, not in dyld cache'),'exact allowed complete reason');require(str(Path(path))==path and '..' not in Path(path).parts,'literal attempted path');require(path in snap['preobserved_dyld_routes']['absent_paths'],'attempt preobserved before execution')
  ordered.append({'path':path,'reason':reason})
  if remaining:require(remaining.startswith(', ') and len(remaining)>2,'complete nontrailing separator');rest=remaining[2:]
  else:rest=''
 equal(len(ordered),10,'ten complete ordered attempts')
 rebuilt=lines[0]+'\n'+prefix+guid+'> '+ext+'\n'+reasonprefix+', '.join("'"+r['path']+"' ("+r['reason']+")" for r in ordered);equal(rebuilt,message,'no dropped dyld text')
 hashes=profile['hashlib'];keys(hashes,('available_openssl_names','openssl_sha256_empty','sha256_empty'),'complete hash observations')
 equal([hashes['sha256_empty'],hashes['openssl_sha256_empty']],['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']*2,'retained two empty-hash observations')
 require(type(hashes['available_openssl_names']) is list and all(type(x) is str for x in hashes['available_openssl_names']),'hash algorithm list types');equal(hashes['available_openssl_names'],sorted(set(hashes['available_openssl_names'])),'complete sorted distinct algorithm names')
 require(type(profile['modules']) is dict and '__main__' in profile['modules'],'complete module object');equal(len(profile['modules']),71,'71 module identities')
 require(not set(profile['modules']).intersection({'white_kernel','white_path','white_controls','white_fixtures','kernel_controls','white_validator','validator_controls','qualify_white_only'}),'no declared science modules')
 files={r['path']:r for r in runtime['files']};descriptors=[];descriptor_kinds={'sentinel':0,'main_source':0,'absent_cache':0,'bound_file':0}
 for name in sorted(profile['modules']):
  r=profile['modules'][name];keys(r,('cached','file','loader_type','origin'),'all four module descriptor fields');require(type(r['loader_type']) is str,'loader type string')
  for field in ('file','cached','origin'):
   path=r[field];item={'module':name,'field':field}
   if path is None or type(path) is str and path in ('built-in','frozen'):item['value']=path;descriptor_kinds['sentinel']+=1
   elif name=='__main__':
    require(field=='file','main nonfile descriptors must be null');equal(path,str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py'),'original RI130 main observer identity');item['identity']=ref(path);descriptor_kinds['main_source']+=1
   else:
    require(type(path) is str and Path(path).is_absolute(),'absolute descriptor name');p=Path(path)
    if not os.path.lexists(path):
     require(field=='cached' and path not in files and any(path.startswith(root+'/') for root in runtime['roots']) and p.resolve()==p,'only in-domain absent cache alternative');item.update(path=path,absent_from_complete_inventory=True);descriptor_kinds['absent_cache']+=1
    else:
     now=identity(path);require(now['resolved_path'] in files,'descriptor target in full accepted inventory');equal(pure(now),pure(files[now['resolved_path']]),'descriptor target bytes');item['binding']={'named_path':path,'resolved_path':now['resolved_path'],'symlink_chain':now['symlink_chain'],'target':pure(now)};descriptor_kinds['bound_file']+=1
   descriptors.append(item)
 equal(len(descriptors),213,'three descriptors per all71 modules')
 reconstructed={'status':'SAVED_PROFILE_FIELDS_RECONCILED_NOT_RUNTIME_ACCEPTANCE','expected_runtime':expected_runtime,'all_descriptors':descriptors,'ordered_actual_dyld_attempts':ordered,'full_dyld_error':decimal['extension_import_error'],'preobserved_domain':snap['preobserved_dyld_routes'],'hash_algorithm_names':hashes['available_openssl_names'],'supplier_cache_and_stable_host_premises_retained':True,'full_import_trace_claim':False,'scientific_qualification':False}
 equal(saved_checks['profile'],reconstructed,'entire profile consumer result independently reconstructed')
 equal([r['samples'] for r in monitors],[52,10,54],'all116 actual monitored samples')

 # Final state/link replay for every opaque file read; excludes atime intentionally.
 for r in list(observed.values()):
  equal(state(Path(r['resolved_path']).lstat()),r['state'],'final all-file state stability')
  require(Path(r['path']).resolve(strict=True)==Path(r['resolved_path']),'final path resolution')
  for link in r['symlink_chain']:equal(os.readlink(link['path']),link['target'],'final ordered link stability')
 equal(tree(C,True),finaltree,'final output namespace stability')
 return {'status':'ALL_INDEPENDENT_ADMINISTRATIVE_PREDICATES_PASSED','profile_modules':len(profile['modules']),'profile_descriptors':len(descriptors),'profile_descriptor_kinds':descriptor_kinds,'ordered_dyld_attempts':ordered,'normal_profile_pin':ref(C/'PROFILE.stdout'),'monitors':monitors,'parent_seconds':complete['elapsed_seconds'],'runtime_files':len(runtime['files']),'runtime_bytes':sum(r['bytes'] for r in runtime['files']),'pyc_opaque_headers':pyc,'bootstrap_module_descriptors':len(names),'bootstrap_file_bindings':module_bindings,'source_groups':sections,'capture_entries':len(finaltree),'installed_e_files':48,'installed_e_directories':8,'snapshot_pin':ref(C/'PRE.stdout'),'same_PRE_POST_bytes':True,'scientific_body_decode':False,'subject_vendor_helper_execution':False,'new_runtime_capture':False,'runtime_baseline_acceptance_created':False}
try:
 result=check();result.update(predicates=checks,opaque_unique_identities=len(observed),decoded_administrative_files=sorted(set(decoded)),administrative_python=sys.executable)
 save('IDENTITIES.json',{'identities':[observed[k] for k in sorted(observed)],'scientific_body_decode':False})
 save('ADMIN_CHECK.json',result);print(json.dumps({k:result[k] for k in ('status','predicates','opaque_unique_identities','runtime_files','runtime_bytes','capture_entries','monitors')},sort_keys=True))
except BaseException as exc:
 result={'status':'FAILED_ADMINISTRATIVE_CHECK','predicates_completed':checks,'error_type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc(),'decoded_administrative_files':decoded,'opaque_unique_identities':len(observed)}
 save('ADMIN_FAILURE.json',result);print(result['traceback'],file=sys.stderr);raise
