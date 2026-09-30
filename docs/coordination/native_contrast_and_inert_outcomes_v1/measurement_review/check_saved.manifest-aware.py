"""Independent finite RI162 saved metadata review; no target code import or execution.
All expectations are literals/manually derived from the accepted source read.
Only metadata records, inert fixture metadata and byte identities are consumed.
"""
import hashlib,json,math,os,pathlib,stat,sys,time,shlex
E=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence')
R=E/'ri162-inert106-root-records-proposed-wb69vu5s'
O=E/'ri156-operation-ri162-inert106-wb69vu5s'
M=E/'ri162-inert106-monitor-proposed-wb69vu5s'
S=E/'ri160-white-fixture-custody-repair-ufok1zpo'
HERE=pathlib.Path(__file__).parent
checks=0; observed={}; outcomes=[]
def need(ok,why):
 global checks
 checks+=1
 if not ok:raise ValueError(why)
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def eq(a,b,why):need(canon(a)==canon(b),why)
def st(p):
 s=os.lstat(p);return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,expected=None):
 p=pathlib.Path(p);a=st(p);need(stat.S_ISREG(a[2]),'regular file '+str(p));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  while True:
   x=f.read(1024*1024)
   if not x:break
   h.update(x);n+=len(x)
 eq(st(p),a,'stable read '+str(p));need(n==a[4],'file size '+str(p))
 r={'path':str(p),'bytes':n,'sha256':h.hexdigest()};observed[str(p)]=r
 if expected:
  for k in ('path','bytes','sha256'):
   if k in expected:eq(r[k],expected[k],'identity '+k+' '+str(p))
  if 'state' in expected:eq(a,expected['state'],'current state '+str(p))
  if 'resolved_path' in expected:eq(str(p.resolve(strict=True)),expected['resolved_path'],'resolved identity')
  if 'symlink_chain' in expected:eq(expected['symlink_chain'],[],'direct original file chain')
 return r
def load(p):
 p=pathlib.Path(p);a=st(p);raw=p.read_bytes();eq(st(p),a,'metadata read stability')
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'duplicate key '+str(p));out[k]=v
  return out
 def bad(x):raise ValueError('nonfinite JSON '+x)
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def refwalk(x):
 if isinstance(x,dict):
  if {'path','bytes','sha256'}<=set(x) and type(x['path']) is str and x['path'].startswith('/'):
   pin(x['path'],x)
  else:
   for v in x.values():refwalk(v)
 elif isinstance(x,list):
  for v in x:refwalk(v)
def tree(root):
 root=pathlib.Path(root);rows=[]
 def visit(p):
  a=st(p);r={'relative':str(p.relative_to(root))}
  if stat.S_ISLNK(a[2]):r.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(a[2]):r['kind']='directory'
  else:
   f=pin(p);r.update(kind='file',bytes=f['bytes'],sha256=f['sha256'])
  rows.append(r)
  if r['kind']=='directory':
   names=sorted(os.listdir(p))
   for name in names:visit(p/name)
   eq(sorted(os.listdir(p)),names,'directory read membership')
  eq(st(p),a,'stable tree entry')
 visit(root);return sorted(rows,key=lambda r:r['relative'])
def projected(rows,prefix):return [dict(r,relative='.' if r['relative']==prefix else r['relative'][len(prefix)+1:]) for r in rows if r['relative']==prefix or r['relative'].startswith(prefix+'/')]
def err(s):return None if s is None else {'type':'ValueError','message':s}
def group_shape(g,ids):
 eq(g['order'],ids,'exact group order');eq([x['id'] for x in g['controls']],ids,'exact row order')
 eq(g['counts'],{'total':len(ids),'passed':len(ids),'failed':0},'typed complete counts');eq(g['status'],'ALL_DECLARED_PASSED','all declared pass')
 for c in g['controls']:
  eq(set(c),set(('id','passed','error','evidence')),'closed control') if False else need(set(c)=={'id','passed','error','evidence'},'closed control')
  need(c['passed'] is True and c['error'] is None and type(c['evidence']) is dict,'actual successful evidence '+c['id'])
def run():
 known={R/'ACTUAL_RUN_SUMMARY.json':(2752,'6cb30ad211c8be4fe25e9bc036dcf7ee4ba3ef6341f7ce43f655ca64dfff4847'),R/'POST_CUSTODY.json':(3326313,'bf909414a3df6397ae261a284df2316b05c67f351d92a900a69e17ebec0633ab'),O/'RESULT.json':(3245944,'838059a30c617a6df1694fa97477bb214d5e3c379baadd80fc03abcafff7a0c9'),O/'COMPLETE.json':(3455655,'5a4c0ba0ab2b963e3dc946c183e69ec19575157413fc86d777bc33ba98d2532c'),S/'SOURCE_SET.json':(147447,'3c01d5825ce66ccf0b071329c46341ea01e28ef4cb76320e5776dd3ae6b53a4f')}
 for p,(n,h) in known.items():pin(p,{'bytes':n,'sha256':h})
 pre=load(R/'BOOTSTRAP_PREFLIGHT.json');a=load(R/'ADAPTER_ADMISSION.json');s=load(S/'SOURCE_SET.json');sb=load(R/'SOURCES_BEFORE.json');rt=load(R/'RUNTIME_BEFORE.json');post=load(R/'POST_CUSTODY.json');summary=load(R/'ACTUAL_RUN_SUMMARY.json')
 eq(post['summary'],summary,'whole post/summary equality');refwalk(pre);refwalk(summary);refwalk(a)
 d160=load(pre['source_acceptance']['path']);need(d160['status']=='ACCEPT_EXACT_UNEXECUTED_FIXTURE_CUSTODY_REPAIR_SOURCE_WITH_QUALIFICATION_PREREQUISITES','accepted source decision')
 need(s['status']=='UNEXECUTED_SOURCE_NOT_ADMISSION','historical source scope preserved');eq(pre['selected_interpreter_binding'],s['bootstrap_binding'],'accepted selected bootstrap')
 refwalk(d160);refwalk(s);refwalk(sb)
 need(len(s['dependencies'])==567 and len(sb['sources'])==582,'source closure counts')
 declared={r['path']:(r['bytes'],r['sha256']) for r in s['dependencies']+[s['adapter']]+list(s['modules'].values())+[a['source_manifest']]}
 before={r['path']:(r['bytes'],r['sha256']) for r in sb['sources']};before_manifest={**before,sb['source_manifest']['path']:(sb['source_manifest']['bytes'],sb['source_manifest']['sha256'])};need(all(before_manifest.get(k)==v for k,v in declared.items()),'every source-set member in before closure')
 need(len(before)==582,'source uniqueness');eq(a['source_review'],pre['source_acceptance'],'source acceptance exact reference');eq(a['source_manifest'],sb['source_manifest'],'manifest before binding')
 need(a['action']=='controls' and a['qualification'] is None and a['genuine_outer_required'] is True and pre['scientific_execution_authorized'] is False,'inert-only admission')
 eq(a['bounds'],{'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':.025,'maximum_sample_gap_seconds':.1,'ps_timeout_seconds':.05,'file_bytes':67108864},'fixed bounds')
 eq(load(a['request']['path']),{'phase':'INERT_METADATA_ONLY'},'request scope');eq(a['environment'],rt['environment'],'real controlled env');eq(a['output'],str(O),'fixed operation path')
 need(len(rt['vendor'])==1810 and len(rt['namespace'])==195 and len(rt['tools'])==4,'whole vendor/namespace/tools cardinality')
 for row in rt['vendor']+rt['tools']:pin(row['path'],row)
 need(len({r['path'] for r in rt['vendor']})==1810 and len({r['path'] for r in rt['namespace']})==195,'runtime membership uniqueness')
 for row in rt['namespace']:
  p=pathlib.Path(row['path']);eq(st(p),row['state'],'current runtime namespace state')
  if row['kind']=='directory':need(p.is_dir() and not p.is_symlink(),'runtime directory');eq(sorted(os.listdir(p)),row['entries'],'full runtime directory membership')
  else:need(row['kind']=='symlink' and p.is_symlink(),'runtime link kind');eq(os.readlink(p),row['target'],'runtime link target')
 for p in rt['absent']:need(not os.path.lexists(p),'declared absent runtime path')
 eq(list(os.uname()),rt['host']['uname'],'current kernel metadata same');need(rt['host']['exit_code']==0 and not rt['host']['stderr'],'genuine prior host observer')
 # External post tree hashes every final node, including COMPLETE, not self-covered by adapter.
 small_trees={}
 for name,rows in post['trees'].items():
  need(len({r['relative'] for r in rows})==len(rows),'post tree unique')
  base=pathlib.Path(rows[0]['path']);current=tree(base);small=[]
  for row in rows:
   eq(st(row['path']),row['state'],'post current node state');r={k:row[k] for k in ('relative','kind')}
   if row['kind']=='file':pin(row['path'],row['identity']);r.update({k:row['identity'][k] for k in ('bytes','sha256')})
   elif row['kind']=='directory':eq(sorted(os.listdir(row['path'])),row['entries'],'post directory membership')
   else:eq(os.readlink(row['path']),row['target'],'post link');r['target']=row['target']
   small.append(r)
  eq(current,small,'entire external post tree '+name);small_trees[name]=current
 # Genuine tool occurrences are root-transcribed and separately supplied by root, not fixture credentials.
 initial=load(R/'GENUINE_INITIAL_TOOL.json');terminal=load(R/'GENUINE_TERMINAL_TOOL.json');eq(initial['actual'],terminal['initial'],'genuine dispatch correlation')
 eq(initial['actual']['chunk_id'],'f3f711','root genuine initial chunk');eq(initial['actual']['session_id'],66856,'genuine session');eq(terminal['poll_arguments']['session_id'],66856,'poll session')
 eq(terminal['actual']['chunk_id'],'9921e9','root genuine terminal chunk');eq(terminal['actual']['exit_code'],0,'genuine terminal exit');eq(terminal['actual']['output'],'','genuine output');need('exit_code' not in initial['actual'],'initial genuinely pending')
 dispatch=initial['dispatch'];eq(dispatch['admission'],pin(R/'ADAPTER_ADMISSION.json'),'dispatch admission');eq(dispatch['preflight'],pin(R/'BOOTSTRAP_PREFLIGHT.json'),'dispatch preflight');need(dispatch['single_attempt'] is True,'single actual attempt')
 tokens=shlex.split(dispatch['exec_command']['cmd']);need(tokens[:2]==['/usr/bin/env','-i'],'clean environment prefix');envargs=tokens[2:12];eq(dict(x.split('=',1) for x in envargs),a['environment'],'genuine exact outer env')
 need(tokens[12:15]==['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;'],'actual external deadline wrapper')
 eq(tokens[15:19],[s['bootstrap_binding']['path'],'-I','-B','-c'],'actual isolated vendor');script=tokens[19];need(len(tokens)==20,'closed outer argv')
 for literal in ['8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe',str(S/'adapter.py'),str(R/'ADAPTER_ADMISSION.json'),str(M),'180, expected_environment','(1, 1, 0)']:need(literal in script,'reviewed direct monitor capture literal')
 need(dispatch['exec_command']['login'] is False and dispatch['exec_command']['workdir']==str(R),'outer cwd/login')
 mc=load(M/'CONTROLS.COMPLETION.json');ma=load(M/'CONTROLS.ATTEMPT.json');command=[s['bootstrap_binding']['path'],'-I','-B',str(S/'adapter.py'),'--admission',str(R/'ADAPTER_ADMISSION.json')]
 eq(mc['command'],command,'child command');eq(ma['command'],command,'attempt command');eq(mc['environment'],a['environment'],'completion env');eq(ma['environment'],a['environment'],'attempt env')
 need(ma['scientific_target_entry'] is False and type(ma['pid_owner']) is int and ma['pid_owner']>0,'real parent ownership declaration')
 need(mc['passed'] is True and mc['first_error'] is None and mc['stop_reason'] is None and mc['tail_errors']==[],'monitor all successful boundaries');eq(mc['child_exit_code'],0,'zero actual child exit');eq(mc['wall_seconds'],180,'fixed monitor wall')
 need(0<mc['elapsed_seconds']<=180,'elapsed bound');need(len(mc['monitor_attempts'])==len(mc['samples'])==130,'all130 exact records')
 last=0.;peak=0;gaps=[]
 for i,(raw,sample) in enumerate(zip(mc['monitor_attempts'],mc['samples'])):
  need(set(raw)=={'elapsed_seconds','returncode','stdout','stderr'},'closed raw attempt');need(set(sample)=={'elapsed_seconds','rss_kib','gap_seconds'},'closed sample')
  eq(raw['returncode'],0,'successful real ps return');eq(raw['stderr'],'','real ps stderr');need(raw['stdout'].strip().isdigit(),'numeric RSS')
  t=raw['elapsed_seconds'];need(type(t) in (int,float) and math.isfinite(t) and last<=t<=mc['elapsed_seconds'],'sample timing');eq(sample['elapsed_seconds'],t,'raw/sample timestamps')
  rss=int(raw['stdout']);eq(sample['rss_kib'],rss,'raw RSS identity');need(0<=rss<=524288,'RSS limit');gap=t-last
  need(abs(gap-sample['gap_seconds'])<=8*math.ulp(max(t,1.0)),'sample gap arithmetic');need(0<=gap<=.1 and 0<=sample['gap_seconds']<=.1,'both sample gap bounds');last=t;peak=max(peak,rss);gaps.append(gap)
 eq(peak,67040,'independent peak');eq(mc['peak_sampled_rss_kib'],peak,'saved peak');eq(mc['final_sample_to_reap_gap_seconds'],mc['elapsed_seconds']-last,'reap gap');need(mc['final_sample_gap_passed'] is True and mc['elapsed_seconds']-last<=.1,'actual final deadline')
 for role in ('stdout','stderr'):pin(mc[role]['path'],mc[role]);eq(mc[role]['bytes'],0,'empty actual output '+role)
 eq(max(gaps),summary['maximum_sample_gap_seconds'],'summary max gap');eq(len(gaps),summary['samples'],'summary samples');eq(peak,summary['peak_sampled_rss_kib'],'summary peak')
 # Complete receipt closes actual source, cards, dependencies and fixture output tails.
 result=load(O/'RESULT.json');complete=load(O/'COMPLETE.json');attempt=load(O/'ATTEMPT.json')
 for path,obj in [(O/'RESULT.json',result),(O/'COMPLETE.json',complete),(O/'ATTEMPT.json',attempt)]:eq(path.read_bytes().decode('ascii'),canon(obj).decode('ascii'),'canonical actual output')
 need(complete['first_error'] is None and complete['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW' and complete['scientific_execution'] is False and complete['root_acceptance_created'] is False and complete['ret_paused'] is True,'full successful conditional completion')
 eq(attempt,{'schema':'ri156-exclusive-metadata-attempt-v1','action':'controls','admission':pin(R/'ADAPTER_ADMISSION.json'),'no_retry':True,'scientific_execution':False},'entire attempt')
 obs=complete['tail_observations'];tails=complete['independent_tails'];need(len(tails)==9 and all(v['error'] is None for v in tails.values()),'all9 tails error null')
 eq(complete['admission'],pin(R/'ADAPTER_ADMISSION.json'),'complete admission');eq(tails['admission']['value'],complete['admission'],'admission tail');eq(tails['request']['value'],a['request'],'request tail');eq(tails['dependencies']['value'],s['dependencies'],'whole567 dependency tail')
 eq(complete['authenticated_source_before'],obs['sources'],'full13 source states before/after');eq(tails['sources']['value'],obs['sources'],'source tail');refwalk(obs['sources'])
 actual_sources={**s['modules'],'adapter':s['adapter'],'manifest':a['source_manifest']}
 eq({k:{z:v[z] for z in ('path','bytes','sha256')} for k,v in obs['sources'].items()},actual_sources,'accepted actual module closure')
 for name in ('ATTEMPT.json','RESULT.json'):eq(complete['produced_output_pins'][name],pin(O/name),'complete output identity');eq(tails['output:'+name]['value'],pin(O/name),'actual output tail')
 current_without_complete=[r for r in small_trees['operation'] if r['relative']!='COMPLETE.json'];eq(obs['namespace'],current_without_complete,'actual adapter final tree excludes only own COMPLETE');eq(tails['namespace']['value'],current_without_complete,'actual namespace successful tail')
 for role in ('inert-fixtures','integration-fixtures'):
  current=projected(current_without_complete,role)
  for saved in (result['fixture_trees'][role],obs['fixture_trees'][role],obs['namespace_fixture_trees'][role],tails['fixture:'+role]['value']):eq(saved,current,'complete raw/normalized fixture tree '+role)
  eq(obs['namespace_fixture_comparisons'][role],{'compared':True,'expected_available':True,'matched':True},'actual fixture comparison eligibility')
 for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):eq(obs[key],[],'actual mismatch inventory')
 # The fixed literal case order is independent of parsing Python source.
 old='monitor_positive monitor_exit_race monitor_missing monitor_rss monitor_gap monitor_final_gap monitor_exception monitor_peak monitor_bool_exit mode_positive mode_supervisor_extra mode_worker_missing mode_custody_missing mode_loaded_origin mode_parent_tail mode_claim mode_namespace mode_command mode_child_rss stage_positive stage_missing_artifact stage_missing_post stage_tree_tail relation_positive relation_changed_file relation_wrong_link relation_extra_field io_positive io_changed_pin io_link io_partial_json io_duplicate_json io_exclusive_output tail_first_preserved tail_all_after_first tail_output_failure shape_supervisor shape_worker shape_custody shape_mode_order copy_positive copy_occupied copy_bad_original copy_changed_after copy_tmp_member observation_duplicate observation_card_extra observation_source_pin observation_directory_missing guard_path_positive guard_path_changed_helper guard_path_pending_controls guard_path_false_execution profile_wrong_environment arithmetic_missing_field_reconstruction'.split()
 new='A01_unchanged A02_pre_module A03_pre_manifest A04_pre_adapter A05_late_module A06_late_manifest A07_late_adapter O01_attempt_drift O02_result_drift O03_sidecars_unchanged O04_inventory_drift O05_selection_drift O06_optional_drift O07_dyld_drift O08_host_drift O09_mode_review_unchanged O10_mode_review_drift O11_partial_sidecars O12_simultaneous_failures O13_namespace_only_drift O14_failure_before_action_output O15_final_write_collision C01_fixture_trees_unchanged C02_fixture_tree_drift M01_unchanged M02_final_root_drift M03_primary_and_final_drift M04_post_and_final_drift M05_unverified_post L01_both_unchanged L02_inert_bytes L03_inert_add L04_inert_delete L05_inert_missing_root L06_inert_file_type L07_inert_link L08_inert_root_file L09_inert_root_link L10_integration_bytes L11_integration_add L12_integration_delete L13_integration_missing_root L14_integration_file_type L15_integration_link L16_integration_root_file L17_integration_root_link L18_primary_both L19_ordinary_both L20_primary_ordinary_both L21_partial_no_expectations L22_success_without_expectations'.split()
 group_shape(result,old+new);group_shape(result['groups']['retained55'],old);group_shape(result['groups']['integration51'],new)
 eq(result['controls'],result['groups']['retained55']['controls']+result['groups']['integration51']['controls'],'complete group records identical')
 for obj in (result,result['groups']['retained55']):
  for flag in ('scientific_execution','runtime_or_tool_evidence_genuine','actual_admission_coverage','arithmetic_or_15_case_credit','full32_credit','ri131_credit'):need(obj[flag] is False,'no false credit '+flag)
 need(result['groups']['integration51']['actual_authentication_or_runtime_credit'] is False and result['groups']['integration51']['scientific_execution'] is False,'integration scope')
 by={c['id']:c['evidence'] for c in result['controls']}
 # Literal exact first refusals; nested result records use the same typed closed evidence.
 refusals={
 'monitor_missing':'RI156_MONITOR: complete attempts/samples','monitor_rss':'RI156_MONITOR: exact bounded rss','monitor_gap':'RI156_MONITOR: gap arithmetic','monitor_final_gap':'RI156_MONITOR: final sample deadline','monitor_exception':'RI156_MONITOR: closed raw monitor attempt','monitor_peak':'RI156_MONITOR: peak arithmetic','monitor_bool_exit':'RI156_MONITOR: genuine zero child exit',
 'mode_supervisor_extra':'RI156_IO: whole30 successful supervisor','mode_worker_missing':'RI156_IO: whole27 worker','mode_custody_missing':'RI156_IO: whole13 worker custody','mode_loaded_origin':'RI156_IO: loaded origin outside whole declared closure','mode_parent_tail':'RI156_IO: parent tail failure profile','mode_claim':'RI156_IO: entire exclusive attempt','mode_namespace':'RI156_IO: exact final namespace adds only supervisor receipt','mode_command':'RI156_IO: literal complete supervisor success header','mode_child_rss':'RI156_MONITOR: exact bounded rss',
 'stage_missing_artifact':'all57 artifact files','stage_missing_post':'all74 exact source/artifact postchecks','stage_tree_tail':'all3 exact tree postchecks','relation_changed_file':'exact mode file identity W11-primary.json','relation_wrong_link':'every control-tree field under exact link relation','relation_extra_field':'closed qualifier return envelope',
 'io_changed_pin':'RI156_IO: FilePin drift','io_link':'RI156_IO: literal resolved path','io_duplicate_json':'RI156_IO: duplicate metadata key',
 'shape_supervisor':'RI156_IO: inert exact field shape','shape_worker':'RI156_IO: inert exact field shape','shape_custody':'RI156_IO: inert exact field shape','shape_mode_order':'RI156_IO: separate accepted normal before optimized',
 'copy_occupied':'RI156_IO: fresh absent copy root','copy_bad_original':'RI156_IO: FilePin drift','copy_changed_after':'RI156_IO: complete relocated copy bytes','copy_tmp_member':'RI156_IO: unexpected root member tmp/unexpected','observation_duplicate':'RI156_IO: duplicate saved tree member','observation_card_extra':'RI156_IO: whole stage card domain','observation_source_pin':'RI156_IO: complete source tree pin','observation_directory_missing':'RI156_IO: complete copy/card/root domain',
 'guard_path_changed_helper':'RI156_IO: guard relocation bindings','guard_path_pending_controls':'RI156_IO: additional path controls unresolved','guard_path_false_execution':'RI156_IO: guard interpretation flags','profile_wrong_environment':'RI156_IO: new environment profile applicability','arithmetic_missing_field_reconstruction':'RI156_IO: separate actual arithmetic outcomes'}
 for key,message in refusals.items():eq(by[key].get('result',by[key]),{'expected':message,'observed':message,'type':'ValueError'},'intended literal first refusal '+key)
 for key in old[9:19]:
  q=by[key];need(q['actual_production_verifier_called'] is True and q['genuine_process_records_are_explicit_inert_metadata'] is True and q['scientific_execution'] is False and q['whole_authentic_entry_qualified'] is False,'mode substitute scope')
  eq(q['source_authority_role_substitutes'],['K.validate_static','K.source_admission','K.mode_admission','K.stage_bindings'],'exact four substitutes')
 for key,race in [('monitor_positive',False),('monitor_exit_race',True)]:
  q=by[key];eq({k:q[k] for k in ('raw_attempts','numeric_samples','peak_sampled_rss_kib','child_elapsed_seconds','final_sample_to_reap_gap_seconds','terminal_malformed_exit_race_source_premise')},{'raw_attempts':2 if race else 1,'numeric_samples':1,'peak_sampled_rss_kib':32,'child_elapsed_seconds':.04,'final_sample_to_reap_gap_seconds':.015,'terminal_malformed_exit_race_source_premise':race},'complete inert monitor positive')
 q=by['mode_positive']['result'];eq(q['whole_supervisor_fields'],30,'whole supervisor count');eq(q['whole_worker_fields'],27,'whole worker count');eq(q['whole_custody_fields'],13,'whole custody count');need(q['scientific_qualification_accepted'] is False and q['actual_data_admitted'] is False and q['arithmetic_recomputed'] is False and q['full32_qualified'] is False,'inert mode no science');refwalk(q['outputs']);refwalk(q['genuine_outer']);eq(q['genuine_outer']['initial_chunk'],'INERT_NOT_A_REAL_TOOL','fake credential conspicuous')
 for key in ('stage_positive',):
  q=by[key];eq([q['artifact_count'],q['source_artifact_postchecks'],q['tree_postchecks']],[57,74,3],'saved metadata positive counters');need(q['actual_data_admitted'] is False and q['arithmetic_recomputed_by_this_check'] is False,'stage no science')
 q=by['relation_positive'];eq(len(q['byte_identical_artifacts']),53,'relation complete53');eq(len(q['propagated_pin_artifacts']),4,'relation4propagated');need(q['complete_envelopes_compared'] is True and q['scientific_fields_omitted'] is False and q['full32_qualified'] is False,'relation scope')
 eq(by['io_positive'],{'inert':True},'positive io');eq(by['io_exclusive_output'],{'exclusive_output_collision_preserved':True,'original':{'inert':True}},'exclusive io');need(by['io_partial_json']['actual_type']=='JSONDecodeError' and by['io_partial_json']['framing_refused'] is True,'partial JSON intended framing')
 for key in ('tail_first_preserved','tail_all_after_first','tail_output_failure'):
  q=by[key];eq(q['rows'],{'first':{'value':None,'error':err('inert first')},'second':{'value':'retained','error':None},'third':{'value':None,'error':err('inert third')}},'all three tail outcomes')
  eq(q['first'],{'type':'INERT','message':'earlier'} if key=='tail_first_preserved' else err('inert first'),'first error preservation')
  if key=='tail_output_failure':need(q['final_write_failure_escapes'] is True,'escaped final collision')
  else:eq(q['complete_trace'],['first','second','third'],'all direct tails ran');need(q['direct_tail_boundary_not_whole_driver'] is True,'direct scope')
 for key in old[40:49]:
  q=by[key]
  if 'direct_function_reduced_graph' in q:need(q['direct_function_reduced_graph'] is True and q['actual48_source_or_authority_coverage'] is False,'reduced graph coverage');eq(q['entire_tree'],tree(O/'inert-fixtures'/key/'copy'),'retained copy fixture')
 for key in old[49:]:
  q=by[key];need(q['read_body_observer_substitutes'] is True and q['authentic_historical_or_runtime_traversal'] is False and q['whole_entry_credit'] is False,'policy observer scope')
  if key=='profile_wrong_environment':eq(q['trace'],[['read','INERT_PROFILE']],'first profile read refusal')
  elif key=='arithmetic_missing_field_reconstruction':eq(q['trace'],[['read','INERT_MODE_REVIEW'],['read','INERT_ARITHMETIC']],'earliest arithmetic refusal')
  elif key!='guard_path_positive':eq(q['trace'],[['read','INERT_DECISION'],['read','INERT_OLD'],['read','INERT_REPORT']],'guard earliest refusal')
 # Full integrated A/O/C outcomes and each real retained COMPLETE are reconciled.
 targets={'O01_attempt_drift':'ATTEMPT.json','O02_result_drift':'RESULT.json','O04_inventory_drift':'runtime_inventory.json','O05_selection_drift':'selection.json','O06_optional_drift':'optional_namespaces.json','O07_dyld_drift':'observed_dyld_routes.json','O08_host_drift':'host_scope.json','O10_mode_review_drift':'MODE_REVIEW.json'}
 for key in new[:24]:
  q=by[key];base=O/'integration-fixtures'/key;owned=base/'owned-output'
  if key in ('A02_pre_module','A03_pre_manifest','A04_pre_adapter'):
   role={'A02_pre_module':'inert_module','A03_pre_manifest':'manifest','A04_pre_adapter':'adapter'}[key];eq(q['caught'],err('RI156_IO: authenticated source baseline pin '+role),'preownership source refusal');eq(q['trace'],['observe:inert_module','observe:adapter','observe:manifest'],'complete baseline first');need(q['owned_output_absent'] is True and not os.path.lexists(owned),'preownership no invented result');continue
  action='sidecars' if key in ('O03_sidecars_unchanged','O04_inventory_drift','O05_selection_drift','O06_optional_drift','O07_dyld_drift','O08_host_drift','O11_partial_sidecars','O14_failure_before_action_output') else 'verify_mode' if key in ('O09_mode_review_unchanged','O10_mode_review_drift') else 'controls' if key.startswith('C') else 'observe'
  produced=['ATTEMPT.json'];trace=['observe:inert_module','observe:adapter','observe:manifest','ref:inert-boundary.json','ref:inert-boundary.json','write:ATTEMPT.json','action:'+action]
  if action=='sidecars' and key!='O14_failure_before_action_output':
   side=['runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'][:2 if key=='O11_partial_sidecars' else 5];trace+=['write:'+x+'.json' for x in side];produced+=[x+'.json' for x in side]
  if action=='verify_mode':trace+=['write:MODE_REVIEW.json'];produced+=['MODE_REVIEW.json']
  if key not in ('O11_partial_sidecars','O12_simultaneous_failures','O14_failure_before_action_output'):trace+=['write:RESULT.json'];produced+=['RESULT.json']
  trace+=['observe:inert_module','observe:adapter','observe:manifest','body:inert-boundary.json','body:inert-request.json','ref:inert-dependency.json']+['ref:'+x for x in sorted(produced)]
  if action=='controls':trace+=['tree:inert-fixtures','tree:integration-fixtures']
  trace+=['tree:owned-output','write:COMPLETE.json'];eq(q['trace'],trace,'complete action and tail ordering '+key)
  if key=='O15_final_write_collision':need(q['caught']['type']=='FileExistsError' and q['final_write_is_external_failure'] is True,'whole final write failure');eq((owned/'COMPLETE.json').read_bytes().decode(),'INERT occupied final receipt\n','collision preserved');eq(q['complete_tree'],tree(owned),'collision complete tree');continue
  report=q['report'];eq(report,load(owned/'COMPLETE.json'),'actual integrated report '+key);eq(q['output_tree'],tree(owned),'actual complete owned output '+key)
  message=None
  if key.startswith(('A05','A06','A07')):message='RI156_IO: all module source state stable'
  if key in targets:message='RI156_IO: produced output pin drift '+targets[key]
  message={'O11_partial_sidecars':'INERT partial sidecar action failure','O12_simultaneous_failures':'INERT primary action failure','O13_namespace_only_drift':'RI156_IO: final namespace produced pin RESULT.json','O14_failure_before_action_output':'INERT action before extra output','C02_fixture_tree_drift':'RI156_IO: entire retained control fixture tree inert-fixtures'}.get(key,message)
  eq(report['first_error'],err(message),'exact integrated first error '+key);eq(report['status'],'REFUSED_RETAIN_ALL_PARTIALS' if message else 'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW','integrated status')
  eq(sorted(report['produced_output_pins']),sorted(produced),'all and only produced pins');tailnames=['sources','admission','request','dependencies']+['output:'+x for x in produced]+(['fixture:inert-fixtures','fixture:integration-fixtures'] if action=='controls' else [])+['namespace'];eq(sorted(report['independent_tails']),sorted(tailnames),'all independent integration tails')
  t=report['independent_tails'];ob=report['tail_observations']
  if message is None:need(all(v['error'] is None for v in t.values()),'every positive tail')
  if key in targets:need(t['output:'+targets[key]]['error'] is not None and t['namespace']['error'] is not None,'both direct and whole output failures')
  if key=='O13_namespace_only_drift':need(t['output:RESULT.json']['error'] is None and t['namespace']['error'] is not None,'late-only output catch')
  if key=='O12_simultaneous_failures':need(all(t[x]['error'] is not None for x in ('sources','request','output:ATTEMPT.json','namespace')) and t['admission']['error'] is None and t['dependencies']['error'] is None,'all independent failures still retained')
  if key=='O11_partial_sidecars':need(t['output:runtime_inventory.json']['error'] is not None and t['output:selection.json']['error'] is None,'partial sidecar later success')
  if key=='C02_fixture_tree_drift':need(t['fixture:inert-fixtures']['error'] is not None and t['fixture:integration-fixtures']['error'] is None,'both fixture tails reached')
  if key in ('O11_partial_sidecars','O12_simultaneous_failures','O14_failure_before_action_output'):need(not os.path.lexists(owned/'RESULT.json'),'no invented early failure output')
  eq(ob['namespace'],[x for x in tree(owned) if x['relative']!='COMPLETE.json'],'saved integration final raw scan')
  need(q['authentication_and_action_substituted'] is True and q['authentic_whole_entry_credit'] is False and q['actual_runner_baseline_ownership_outputs_and_tails_used'] is True,'integration actual-vs-inert boundary')
 # Saved-mode final tails: observer substitutions remain explicit.
 for key in new[24:29]:
  q=by[key];z=q['result'];eq(z,load(O/'integration-fixtures'/key/'MODE_REVIEW.json'),'whole mode result')
  message={'M01_unchanged':None,'M02_final_root_drift':'RI156_IO: whole final root matches verified post-copy observation','M03_primary_and_final_drift':'INERT saved-check first failure','M04_post_and_final_drift':'INERT post-runtime first failure','M05_unverified_post':'RI156_IO: complete actual post-copy/root namespace'}[key];eq(z['first_error'],err(message),'mode first reason')
  eq(sorted(z['independent_tails']),sorted(['post_runtime','source_copies','source_admission','mode_admission','full_root_namespace']),'all5 mode tails')
  want=['copy_states','validate:frozen','validate:normal_completed','root_observe:1']
  if key!='M05_unverified_post':want+=['runtime:pre','saved_check']
  if key not in ('M03_primary_and_final_drift','M05_unverified_post'):want+=['validate:normal_admitted']
  want+=['runtime:post','copy_states','source_admission','mode_admission','root_observe:2'];eq(q['trace'],want,'all mode sequence')
  eq(z['independent_tails']['full_root_namespace']['error'],err('RI156_IO: whole final root matches verified post-copy observation') if key in ('M02_final_root_drift','M03_primary_and_final_drift','M04_post_and_final_drift') else None,'mode secondary tail error')
  need(z['qualification_accepted'] is False and z['arithmetic_recomputed'] is False and q['runtime_saved_source_and_card_observers_substituted'] is True and q['authentic_mode_or_science_credit'] is False,'mode no runtime/math credit')
 # New22 fixed-oracle controls, independent physical reconstruction and exact full-field prefix relation.
 def byteid(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 base_rows=[{'relative':'.','kind':'directory'},{'relative':'alpha.txt','kind':'file',**byteid(b'INERT fixture alpha\n')},{'relative':'link','kind':'symlink','target':'alpha.txt'},{'relative':'nested','kind':'directory'}]
 kinds=['bytes','add','delete','missing_root','file_type','link','root_file','root_link'];roles=['inert-fixtures','integration-fixtures']
 for index,key in enumerate(new[29:]):
  q=by[key];z=q['report'];ob=z['tail_observations'];t=z['independent_tails'];root=O/'integration-fixtures'/key;owned=root/'owned-output'
  eq(z,load(owned/'COMPLETE.json'),'whole actual late-case receipt');eq(q['complete_case_tree'],tree(root),'entire late fixture raw bytes')
  scan=[r for r in tree(owned) if r['relative']!='COMPLETE.json'];eq(q['final_scan'],scan,'actual late raw scan');eq(ob['namespace'],scan,'complete retained final scan')
  eq(q['expected_fixed_rows'],base_rows,'independent fixed oracle rows')
  partial=index==20;missing=index==21;primary=index in (17,19,20);ordinary=index in (18,19)
  changes={}
  if 1<=index<=8:changes[roles[0]]=kinds[index-1]
  elif 9<=index<=16:changes[roles[1]]=kinds[index-9]
  elif index in (17,18,19):changes={roles[0]:'bytes',roles[1]:'link'}
  members=[];outputs=[];errors=[];mutations=[]
  for role in roles:
   expected=[dict(r) for r in base_rows];kind=changes.get(role)
   if kind=='bytes':expected[1].update(byteid(b'INERT fixture beta\n'))
   elif kind=='add':expected.append({'relative':'extra.txt','kind':'file',**byteid(b'INERT new member\n')})
   elif kind=='delete':expected=[r for r in expected if r['relative']!='alpha.txt']
   elif kind=='missing_root':expected=[]
   elif kind=='file_type':expected[1]={'relative':'alpha.txt','kind':'directory'}
   elif kind=='link':expected[2]['target']='nested'
   elif kind=='root_file':expected=[{'relative':'.','kind':'file',**byteid(b'INERT root replacement\n')}]
   elif kind=='root_link':expected=[{'relative':'.','kind':'symlink','target':'INERT_missing_target'}]
   expected=sorted(expected,key=lambda x:x['relative']);eq(projected(scan,role),expected,'independently derived all late rows '+key+'/'+role);eq(ob['namespace_fixture_trees'][role],expected,'normalized rows preserve every raw field')
   available=not(partial or missing);eq(ob['namespace_fixture_comparisons'][role],{'expected_available':available,'compared':available,'matched':role not in changes if available else None},'honest expectation availability')
   if kind:mutations.append({'root':role,'kind':kind,'timing':'final_whole_tree_entry_after_individual_tails'})
   if kind in ('root_file','root_link'):members.append({'name':role,**err('RI156_IO: output member type')})
   if kind or missing:errors.append({'name':role,**err('RI156_IO: '+('complete captured control fixture expectation ' if missing else 'final namespace control fixture tree ')+role)})
   if available:eq(t['fixture:'+role]['value'],base_rows,'whole earlier tail succeeded before late mutation');eq(ob['fixture_trees'][role],base_rows,'original earlier observation preserved')
  if ordinary:outputs=[{'name':'RESULT.json',**err('RI156_IO: final namespace produced pin RESULT.json')}];mutations.append({'root':'RESULT.json','kind':'bytes','timing':'final_whole_tree_entry_after_individual_tails'})
  eq(q['mutations'],mutations,'exact declared actual mutations');members.sort(key=lambda x:x['name']);eq(ob['namespace_member_mismatches'],members,'complete structural mismatches');eq(ob['namespace_output_mismatches'],outputs,'complete ordinary mismatches');eq(ob['namespace_fixture_mismatches'],errors,'complete both-root mismatches')
  allerrors=members+outputs+errors;late={k:allerrors[0][k] for k in ('type','message')} if allerrors else None;eq(t['namespace']['error'],late,'earliest late reason');first=err('INERT primary fixture action failure') if primary else late;eq(z['first_error'],first,'primary preserved over late');eq(z['status'],'REFUSED_RETAIN_ALL_PARTIALS' if first else 'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW','late completion status')
  prod=['ATTEMPT.json']+([] if partial else ['RESULT.json']);eq(sorted(z['produced_output_pins']),prod,'no invented output expectation');names=['sources','admission','request','dependencies']+['output:'+x for x in prod]+([] if partial or missing else ['fixture:'+x for x in roles])+['namespace'];eq(sorted(t),sorted(names),'complete eligible tails')
  need(all(t[x]['error'] is None for x in names if x!='namespace'),'all earlier eligible tails succeeded')
  if partial or missing:need('fixture_trees' not in ob,'no invented earlier fixture observation')
  if partial:need(not os.path.lexists(owned/'RESULT.json'),'partial no result')
  trace=['observe:inert_module','observe:adapter','observe:manifest','ref:inert-boundary.json','ref:inert-boundary.json','write:ATTEMPT.json','action:controls']+([] if partial else ['write:RESULT.json'])+['observe:inert_module','observe:adapter','observe:manifest','body:inert-boundary.json','body:inert-request.json','ref:inert-dependency.json']+['ref:'+x for x in prod]+([] if partial or missing else ['tree:inert-fixtures','tree:integration-fixtures'])+['tree:owned-output','write:COMPLETE.json'];eq(q['trace'],trace,'complete late-control order')
  need(q['individual_tails_succeeded_before_late_mutation'] is (not(partial or missing)) and q['authentication_and_action_substituted'] is True and q['actual_runner_and_final_comparison_used'] is True and q['authentic_whole_entry_credit'] is False and q['current_runtime_or_science_credit'] is False,'late control credit boundary')
 for c in result['controls']:outcomes.append({'id':c['id'],'review':'PASS_saved_outcome_and_declared_scope','evidence_pin':byteid(canon(c['evidence']))})
 return {'status':'PASS_COMPLETE_INDEPENDENT_INERT106_OUTCOME_REVIEW','checks':checks,'controls':len(outcomes),'control_evidence':outcomes,'genuine_execution':{'initial_chunk':'f3f711','session':66856,'terminal_chunk':'9921e9','outer_exit':0,'child_exit':0,'elapsed_seconds':mc['elapsed_seconds'],'samples':130,'peak_rss_kib':peak,'maximum_gap_seconds':max(gaps),'final_gap_seconds':mc['elapsed_seconds']-last},'current_closure':{'sources':582,'vendor_files':1810,'runtime_namespace':195,'inspection_tools':4,'source_manifest_dependencies':567,'operation_nodes':3002,'operation_files':2468,'inert_fixture_nodes':2194,'integration_fixture_nodes':804},'evidence':{str(p):pin(p) for p in known},'inert_fixture_credentials_genuine':False,'scientific_qualification_or_runtime_closure_credit':False,'ret_paused':True}
if __name__=='__main__':
 try:
  result=run();result['finite_checker']=pin(__file__);result['completed_at_unix_ns']=time.time_ns();target=HERE/'CHECK_RESULT.json'
 except BaseException as exc:
  target=HERE/('CHECK_FAILURE-'+str(time.time_ns())+'.json');result={'status':'CHECKER_FAILURE_RETAINED','checks_completed':checks,'error_type':type(exc).__name__,'error':str(exc)}
  with target.open('xb') as f:f.write(canon(result))
  print(str(target),result);raise
 with target.open('xb') as f:f.write(canon(result))
 print(json.dumps({'path':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'status':result['status'],'checks':checks},sort_keys=True))
