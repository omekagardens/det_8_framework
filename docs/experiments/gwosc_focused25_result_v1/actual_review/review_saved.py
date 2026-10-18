"""Independent saved-administrative review. No subject import/execution/runtime observation."""
import copy, hashlib, json, math, os, shlex, stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri139-root-bootstrap-adjudication-goau3dIc';O=B/'ri139-focused25-run-6_wa8gqh';U=O/'output';C=U/'controls';Q=B/'ri139-focused-bootstrap-repair-source-XP8iNwMw';P=B/'ri135-white-preparation-repair-source-lski1ize';R=B/'ri139-focused25-independent-review-FQU9u14Y'
READ={}
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def raw(p):
 p=Path(p);assert str(p).startswith(str(B)+'/') or str(p).startswith('/Volumes/AI_DATA/development/det_8_framework-ret/')
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and p.resolve()==p and a.st_size<=67108864
 with p.open('rb') as f:
  assert state(os.fstat(f.fileno()))==state(a);b=f.read();assert state(os.fstat(f.fileno()))==state(a)
 assert state(p.lstat())==state(a)
 READ[str(p)]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'state':state(a)};return b
def pin(p):
 raw(p);return {k:v for k,v in READ[str(p)].items() if k!='state'}
def pure(p):return {k:v for k,v in pin(p).items() if k!='path'}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def eq(a,b):assert enc(a)==enc(b),(a,b)
def js(p):
 def pairs(xs):
  d={}
  for k,v in xs:assert k not in d;d[k]=v
  return d
 def bad(x):raise ValueError(x)
 return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=bad)
def canonical_js(p):
 v=js(p);assert enc(v)==raw(p);return v
def verify(row):eq(pin(Path(row['path'])),row)
def keys(d,expected):assert type(d) is dict and set(d)==set(expected.split())
def tree(p):
 p=Path(p);out=[]
 for root,dirs,files in os.walk(p,followlinks=False):
  for n in dirs+files:
   x=Path(root)/n;s=x.lstat();r={'relative':str(x.relative_to(p))}
   if stat.S_ISDIR(s.st_mode):r['kind']='directory'
   elif stat.S_ISLNK(s.st_mode):r.update(kind='symlink',target=os.readlink(x))
   else:assert stat.S_ISREG(s.st_mode);r.update(kind='file',**pure(x))
   out.append(r)
 assert len(out)<=25000 and sum(x.get('bytes',0) for x in out)<=536870912
 return sorted(out,key=lambda x:x['relative'])
def err(message,typ='ValueError'):return {'type':typ,'message':message}
def env(root):return {'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(root/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
F01=['positive','pre_admission_read','occupied','mkdir','post_admission_read','initial_source_read','attempt_open','attempt_partial','secondary_post','secondary_source','secondary_namespace','secondary_checks','three_secondary','final_partial']
F02=['positive','named_path','resolved_path','link_literal','link_order','link_omitted','target_bytes','target_sha','provenance_missing','snapshot_alias','snapshot_target'];IDS=['F01_'+s for s in F01]+['F02_'+s for s in F02]
deps=js(Q/'DEPENDENCIES.source-only.json');handoff=js(Q/'HANDOFF.json');sr=js(B/'ri139-bootstrap-independent-review-VMq4RmI9/HANDOFF.json')
packet=handoff['files']+[pin(Q/'HANDOFF.json')];reviewfiles=sr['files']+[pin(Path(sr['reservation'])/'HANDOFF.json')]
for row in packet+reviewfiles+deps['opaque_files']:verify(row)
assert len(deps['opaque_files'])==310 and sum(x['bytes'] for x in deps['opaque_files'])==21106955
assert sorted(p.name for p in Q.iterdir())==sorted(Path(x['path']).name for x in packet)
rec=js(D/'ROOT_SOURCE_RECONCILIATION.json');assert len(rec['observations'])==325
expected={x['path']:x for x in packet+reviewfiles+deps['opaque_files']}
assert set(expected)=={x['path'] for x in rec['observations']}
for x in rec['observations']:
 eq({k:x[k] for k in ['path','bytes','sha256']},expected[x['path']]);eq(READ[x['path']]['state'],x['state']);assert x['resolved_path']==x['path'] and x['symlink_chain']==[]
adj=js(D/'RI139_ROOT_ADJUDICATION.json');assert adj['source_accepted'] is True and adj['execution_admitted'] is False
for k in ['independent_review','reconciliation','root_review','source']:verify(adj[k])
dispatch=js(D/'ROOT_DISPATCH.json');assert dispatch['status']=='AUTHORIZE_EXACT_SINGLE_FOCUSED25_EXECUTION' and dispatch['retry_authorized'] is False and dispatch['actual_completion_at_admission'] is False
for x in dispatch['cards']:verify(x)
for pair in dispatch['copies']:
 for x in pair.values():verify(x)
 assert raw(pair['original']['path'])==raw(pair['operational']['path'])
card=canonical_js(O/'cards/launcher.json');control=canonical_js(O/'cards/controls.json');preflight=canonical_js(O/'cards/preflight.json')
keys(card,'schema status launcher_handoff launcher_review launcher_adjudication bootstrap_host_preflight controls_admission output environment_root launcher_command child_command environment limits external_premises')
for k in ['launcher_handoff','launcher_review','launcher_adjudication','bootstrap_host_preflight','controls_admission']:verify(card[k])
assert card['schema']=='ri139-root-focused-launcher-admission-v1' and card['status']=='AUTHORIZE_ONLY_RI135_FOCUSED25'
limits={'child_seconds':180,'child_rss_kib':524288,'poll_seconds':.025,'maximum_sample_gap_seconds':.1,'ps_timeout_seconds':.05,'stream_bytes':67108864,'file_bytes':67108864,'namespace_bytes':536870912,'namespace_entries':25000,'parent_soft_seconds':900,'genuine_outer_timeout_seconds':960}
premises=dict.fromkeys(['genuine_bootstrap_host_preflight_external','genuine_tool_completion_external','stable_supplier_host_and_no_descendants','apple_loader_and_cache_external','sampled_child_only_not_parent_or_group_quota','saved_parent_pid_not_authenticated_child_identity'],True)
eq(card['limits'],limits);eq(card['external_premises'],premises);eq(card['environment'],env(O/'environment'));assert card['output']==str(U) and card['environment_root']==str(O/'environment')
bootstrap=deps['selected_bootstrap_binding']['path'];launcher=[bootstrap,'-I','-B',str(Q/'launch_controls.source-only.py'),'--admission',str(O/'cards/launcher.json')];child=[bootstrap,'-I','-B',str(P/'fault_controls.source-only.py'),'--admission',str(O/'cards/controls.json'),'--output',str(C)]
eq(card['launcher_command'],launcher);eq(card['child_command'],child)
sources4={n:pure(P/n) for n in ['prepare.py','runtime_metadata.py','fault_controls.source-only.py','DEPENDENCIES.source-only.json']};sources3={k:v for k,v in sources4.items() if k!='fault_controls.source-only.py'}
eq(control,{'schema':'ri135-root-fault-control-admission-v1','status':'AUTHORIZE_F01_F02_NONSCIENTIFIC_CONTROLS_ONLY','sources':sources4,'controls':IDS,'output':str(C),'independent_source_review':deps['ri135_independent_review'],'genuine_outer_required':True})
initial=js(D/'GENUINE_TOOL_INITIAL.json');final=js(D/'GENUINE_TOOL_FINAL.json');eq(initial['invocation'],dispatch['invocation']);assert initial['result']['chunk_id']=='7538a9' and initial['result']['session_id']==12210 and initial['result']['output']==''
assert final['chunk_id']=='0982f4' and final['exit_code']==0 and final['output']==''
argv=shlex.split(dispatch['invocation']['cmd']);expected_outer=['exec','/usr/bin/env','-i']+[k+'='+v for k,v in card['environment'].items()]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+launcher;eq(argv,expected_outer)
assert dispatch['invocation']['workdir']==str(O) and dispatch['invocation']['login'] is False
eq(tree(O/'environment'),[{'relative':'tmp','kind':'directory'}]);assert sorted(x.name for x in O.iterdir())==['cards','environment','output']
assert sorted(x.name for x in (O/'cards').iterdir())==['adjudication.json','controls.json','launcher.json','preflight.json','review.json']
pre=js(D/'BOOTSTRAP_PRE.json');post=js(D/'BOOTSTRAP_POST.json');assert raw(D/'BOOTSTRAP_PRE.json')==raw(D/'BOOTSTRAP_POST.json')
assert pure(D/'BOOTSTRAP_PRE.json')=={'bytes':1690949,'sha256':'cb536ed79a79c47570b66bc0bd0b159243a36fc5ea15985524c898fbe76a7f0c'}
eq(pre['selected_interpreter_binding'],deps['selected_bootstrap_binding']);eq(preflight['selected_interpreter_binding'],pre['selected_interpreter_binding']);eq(pre['actual_environment'],card['environment']);eq(preflight['actual_environment'],card['environment'])
for k in ['fresh_pre','genuine_pre_tool','source_decision','source_reconciliation','prior_deadline_probe']:verify(preflight[k])
for phase,chunk in [('PRE','f24636'),('POST','792c37')]:
 t=js(D/('BOOTSTRAP_'+phase+'_TOOL.json'));assert t['result']['exit_code']==0 and t['result']['chunk_id']==chunk
 v=shlex.split(t['invocation']['cmd']);assert v[-5:]==[bootstrap,'-I','-B',str(D/'observe_bootstrap.py'),phase]
 assert pin(D/('BOOTSTRAP_'+phase+'.json'))['sha256'] in t['result']['output']
 eq(t['invocation']['workdir'],str(O))
framework={x['path']:x for x in pre['framework_namespace']};assert len(framework)==2004
assert sum(x.get('identity',{}).get('bytes',0) for x in framework.values())==pre['framework_file_bytes']==48024515
assert framework[bootstrap]['identity']==pre['selected_interpreter_binding']
for x in pre['framework_namespace']:
 assert Path(x['path']).is_relative_to(pre['prefix'])
 if x['kind']=='file':assert x['identity']['path']==x['path'] and 0<=x['identity']['bytes']<=67108864
 elif x['kind']=='symlink':assert type(x['target']) is str
 else:assert x['kind']=='directory'
for name in ['collector','metadata_helper']:verify(pre[name])
desc=pre['bootstrap_descriptor'];assert desc['executable']==bootstrap and desc['isolated']==desc['dont_write_bytecode']==1 and desc['optimize']==0
assert desc['path']==[pre['prefix']+'/lib/python39.zip',pre['prefix']+'/lib/python3.9',pre['prefix']+'/lib/python3.9/lib-dynload',pre['prefix']+'/lib/python3.9/site-packages']
module_rows=[]
for m in desc['modules']:
 if 'identity' in m:
  p=m['identity']['path']
  if p in framework:eq(framework[p]['identity'],m['identity'])
  else:assert p in [pre['collector']['path'],pre['metadata_helper']['path']];eq({k:m['identity'][k] for k in ['path','bytes','sha256']},pin(p))
  module_rows.append({'name':m['name'],'identity':m['identity'],'cached':m['cached'],'cache_recorded':m['cached'] in framework if m['cached'] else None})
# All saved monitor attempts and arithmetic; 1e-12 equality tolerance only for double subtraction, never a bound relaxation.
mon=canonical_js(U/'FOCUSED25.COMPLETION.json');ma=canonical_js(U/'FOCUSED25.ATTEMPT.json');wa=canonical_js(U/'ATTEMPT.json');complete=canonical_js(U/'COMPLETE.json')
keys(mon,'command environment wall_seconds samples monitor_attempts peak_sampled_rss_kib stop_reason child_exit_code first_error tail_errors elapsed_seconds final_sample_to_reap_gap_seconds final_sample_gap_passed stdout stderr passed')
eq(mon['command'],child);eq(mon['environment'],card['environment']);assert mon['wall_seconds']==180 and mon['child_exit_code']==0 and mon['passed'] is True and mon['stop_reason'] is None and mon['first_error'] is None and mon['tail_errors']==[]
eq({k:v for k,v in ma.items() if k!='pid_owner'},{'command':child,'environment':card['environment'],'wall_seconds':180,'scientific_target_entry':False});assert type(ma['pid_owner']) is int and ma['pid_owner']>0
for k in ['stdout','stderr']:verify(mon[k]);assert mon[k]['bytes']==0
assert len(mon['samples'])==len(mon['monitor_attempts'])==30
last=0.;sample_records=[]
for i,(a,s) in enumerate(zip(mon['monitor_attempts'],mon['samples'])):
 keys(a,'elapsed_seconds returncode stderr stdout');keys(s,'elapsed_seconds gap_seconds rss_kib')
 assert a['returncode']==0 and a['stderr']=='' and a['stdout'].strip().isdigit();assert int(a['stdout'])==s['rss_kib'];assert type(s['rss_kib']) is int and 0<=s['rss_kib']<=524288
 assert a['elapsed_seconds']==s['elapsed_seconds'] and math.isfinite(s['elapsed_seconds']) and s['elapsed_seconds']>last
 calculated=s['elapsed_seconds']-last;assert math.isclose(calculated,s['gap_seconds'],rel_tol=0,abs_tol=1e-12);assert 0<s['gap_seconds']<=.1
 sample_records.append({'index':i,'raw_rss':a['stdout'],'time':s['elapsed_seconds'],'gap':s['gap_seconds'],'recomputed_gap':calculated,'rss_kib':s['rss_kib']});last=s['elapsed_seconds']
assert 0<mon['elapsed_seconds']<=180;finalgap=mon['elapsed_seconds']-last;assert finalgap==mon['final_sample_to_reap_gap_seconds'] and 0<=finalgap<=.1 and mon['final_sample_gap_passed'] is True
assert mon['peak_sampled_rss_kib']==max(s['rss_kib'] for s in mon['samples'])==65952
wa_expected={'schema':'ri139-focused-launcher-attempt-v1','admission':pin(O/'cards/launcher.json'),'child_command':child,'environment':card['environment'],'limits':limits,'external_premises':premises,'loaded_module':deps['ri135_module'],'captured_loaded_bytes':sources4['prepare.py'],'scientific_execution':False};eq(wa,wa_expected)
report=canonical_js(C/'REPORT.json');header={k:v for k,v in report.items() if k!='controls'}
eq(header,{'schema':'ri135-focused-fault-control-report-v1','order':IDS,'counts':{'total':25,'passed':25,'failed':0},'sources_before':sources4,'sources_after':sources4,'sources_unchanged':True,'status':'ALL25_FOCUSED_CONTROLS_PASSED','admission':pin(O/'cards/controls.json'),'fixture_root':str(C),'all_substitutions_explicit':True,'runtime_profiles_or_65_caller_guards_executed':False,'scientific_execution':False,'production_admission_created':False,'actual_current_runtime_qualified':False,'ret_paused':True})
assert len(report['controls'])==25;historical=canonical_js(deps['historical_interpreter']['path']);verify(deps['historical_interpreter']);verify(deps['historical_interpreter_provenance'])
case_checks=[]
for identifier,row in zip(IDS,report['controls']):
 keys(row,'id passed evidence error');assert row['id']==identifier and row['passed'] is True and row['error'] is None;e=row['evidence'];kind=identifier[4:]
 if identifier.startswith('F01_'):
  keys(e,'substitutions events calls first_error escaped returncode attempted_completion retained_tree actual_runtime_or_production_admission');base=C/identifier;out=base/'owned-output';fixture=base/'FABRICATED_CONTROL_METADATA.json'
  eq(e['substitutions'],['authentication','runtime snapshot/processes','source observation']);assert e['actual_runtime_or_production_admission'] is False;eq(e['retained_tree'],tree(base))
  admission={'schema':'ri135-FABRICATED_CONTROL_NOT_ADMISSION','phase':'capture','output':str(out),'environment_root':str(base/'ENVIRONMENT_DOUBLE'),'sources':sources3,'baseline_acceptance':None,'normal_acceptance':None,'profiles_acceptance':None,'guard_admission':None,'bootstrap':{'CONTROL_DOUBLE_NOT_RUNTIME':True},'host':{'uname':['CONTROL'],'system_version':{'CONTROL':True}}};eq(canonical_js(fixture),admission)
  events=['AUTHENTICATION_SUBSTITUTED'];counts=dict.fromkeys(['checks','complete','post','pre','source_set','source_tail','tree'],0)
  preerrors={'pre_admission_read':'CONTROL_PRE_ADMISSION_READ','occupied':'one fresh root-owned preparation output','mkdir':'CONTROL_MKDIR_FAILURE'}
  if kind in preerrors:
   if kind!='occupied':events+=['admission_ref_preownership']
   eq(e['events'],events);eq(e['calls'],counts);eq(e['first_error'],err(preerrors[kind]));eq(e['escaped'],e['first_error']);assert e['returncode'] is None;eq(e['attempted_completion'],[])
   if kind=='occupied':assert sorted(x.name for x in out.iterdir())==['UNRELATED_OCCUPIED'] and raw(out/'UNRELATED_OCCUPIED')==b'preserve me\n'
   else:assert not os.path.lexists(out)
  else:
   counts.update(checks=1,complete=1,post=1,pre=int(kind=='positive'),source_set=1 if kind=='post_admission_read' else 2,source_tail=1,tree=1);eq(e['calls'],counts)
   events+=['admission_ref_preownership','admission_ref_owned']
   if kind!='post_admission_read':events+=['sources_1']
   if kind not in ['post_admission_read','initial_source_read']:events+=['save_ATTEMPT.json']
   if kind=='positive':events+=['child_PRE_SUBSTITUTED']
   events+=['child_POST_SUBSTITUTED','sources_1' if kind=='post_admission_read' else 'sources_2','source_tail_SUBSTITUTED','save_CHECKS.json','namespace_tail']
   if kind not in ['secondary_namespace','three_secondary']:events+=['save_NAMESPACE.json']
   events+=['save_COMPLETE.json'];eq(e['events'],events)
   first=None if kind=='positive' else err({'post_admission_read':'CONTROL_POST_ADMISSION_READ','initial_source_read':'CONTROL_INITIAL_SOURCE_READ','attempt_open':'CONTROL_ATTEMPT_OPEN'}.get(kind,'CONTROL_ATTEMPT_PARTIAL'))
   eq(e['first_error'],first);eq(e['escaped'],err('CONTROL_FINAL_RECEIPT_WRITE') if kind=='final_partial' else None);eq(e['returncode'],None if kind=='final_partial' else int(kind!='positive'))
   assert len(e['attempted_completion'])==1;c=e['attempted_completion'][0]
   tailmap={'secondary_post':[('post_metadata','CONTROL_SECONDARY_POST')],'secondary_source':[('source_admission','CONTROL_SECONDARY_SOURCE')],'secondary_namespace':[('retain_namespace','CONTROL_SECONDARY_NAMESPACE')],'secondary_checks':[('save_checks','CONTROL_SECONDARY_CHECKS')],'three_secondary':[('post_metadata','CONTROL_SECONDARY_POST'),('source_admission','CONTROL_SECONDARY_SOURCE'),('retain_namespace','CONTROL_SECONDARY_NAMESPACE')]}
   tails=[dict(tail=t,**err(m)) for t,m in tailmap.get(kind,[])];artifacts={};checks={}
   for label,do in [('PRE',kind=='positive'),('POST',kind not in ['secondary_post','three_secondary'])]:
    if do:
     eq(canonical_js(out/(label+'.stdout')),{'CONTROL_METADATA_DOUBLE_ONLY':True,'host_bootstrap':{'bootstrap':{'named':admission['bootstrap']},**admission['host']}});eq(canonical_js(out/(label+'.COMPLETION.json')),{'CONTROL_CHILD_COMPLETION_DOUBLE_ONLY':True})
     artifacts[label]=pin(out/(label+'.stdout'));artifacts[label+'_completion']=pin(out/(label+'.COMPLETION.json'))
   if kind not in ['secondary_post','three_secondary']:checks['post_metadata']='PASS' if kind=='positive' else 'CAPTURED_WITHOUT_SUCCESSFUL_PRE'
   if kind not in ['secondary_source','three_secondary']:checks['source_and_admission_postcheck']='PASS'
   if kind!='secondary_checks':eq(canonical_js(out/'CHECKS.json'),checks);artifacts['checks']=pin(out/'CHECKS.json')
   else:assert not os.path.lexists(out/'CHECKS.json')
   if kind not in ['secondary_namespace','three_secondary']:
    ns=canonical_js(out/'NAMESPACE.json');eq(ns,{'schema':'ri133-retained-namespace-v1','root':str(out),'entries':[x for x in tree(out) if x['relative'] not in ['NAMESPACE.json','COMPLETE.json']],'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json']});artifacts['namespace']=pin(out/'NAMESPACE.json')
   else:assert not os.path.lexists(out/'NAMESPACE.json')
   assert type(c['elapsed_seconds']) is float and math.isfinite(c['elapsed_seconds']) and 0<=c['elapsed_seconds']<=900
   expected_c={'schema':'ri133-preparation-completion-v1','phase':'capture','status':'CAPTURED_FOR_INDEPENDENT_REVIEW' if kind=='positive' else 'REFUSED_RETAIN_ALL_PARTIALS','command':['/usr/bin/python3','-I','-B',str(P/'prepare.py'),'--admission',str(fixture)],'environment':env(base/'ENVIRONMENT_DOUBLE'),'admission':pin(fixture),'sources':sources3,'artifacts':artifacts,'first_error':first,'independent_tail_errors':tails,'elapsed_seconds':c['elapsed_seconds'],'scientific_targets_executed':False,'actual_data_admitted':False,'full32_qualified':False,'ret_paused':True,'runtime_acceptance_created':False,'genuine_outer_created':False};eq(c,expected_c)
   if kind=='final_partial':assert raw(out/'COMPLETE.json')==b'{"CONTROL_PARTIAL_COMPLETE":'
   else:eq(canonical_js(out/'COMPLETE.json'),c)
   if kind=='positive':eq(canonical_js(out/'ATTEMPT.json'),{'schema':'ri133-preparation-attempt-v1','admission':pin(fixture),'sources':sources3,'phase':'capture','environment':env(base/'ENVIRONMENT_DOUBLE'),'scientific_execution':False})
   elif kind in ['post_admission_read','initial_source_read','attempt_open']:assert not os.path.lexists(out/'ATTEMPT.json')
   else:assert raw(out/'ATTEMPT.json')==b'{"CONTROL_PARTIAL_ATTEMPT":'
  case_checks.append({'id':identifier,'passed':True,'events':e['events'],'calls':e['calls'],'first_error':e['first_error'],'escaped':e['escaped'],'returncode':e['returncode'],'complete_fields_reconstructed':len(e['attempted_completion'])==1,'namespace_entries':len(e['retained_tree'])})
 else:
  keys(e,'current_binding_control_operand genuine_historical_binding historical_provenance reads calls refusal snapshot_observers_substituted provenance_after_authentication_mutated_in_memory actual_current_interpreter_observed');want=copy.deepcopy(historical)
  if kind=='named_path':want['named_path']+='.changed'
  if kind=='resolved_path':want['resolved_path']+='.changed'
  if kind in ['link_literal','snapshot_alias']:want['symlink_chain'][0]['target']='./python3.11'
  if kind=='link_order':want['symlink_chain'].reverse()
  if kind=='link_omitted':want['symlink_chain']=want['symlink_chain'][1:]
  if kind=='target_bytes':want['target']['bytes']+=1
  if kind in ['target_sha','snapshot_target']:want['target']['sha256']='0'*64
  snapshot=kind.startswith('snapshot_');reads=([deps['historical_optional_namespaces']['path']] if snapshot else [])+[deps['historical_interpreter_provenance']['path']]+([] if kind=='provenance_missing' else [deps['historical_interpreter']['path']]);calls=dict.fromkeys(['host','sources','absences','namespaces','routes','loaders','interpreter','walk'],0)
  if snapshot:calls.update(host=1,sources=1,absences=1,namespaces=1,routes=1,loaders=8,interpreter=1)
  refusal=None if kind=='positive' else err('historical interpreter handoff identity' if kind=='provenance_missing' else 'candidate interpreter differs from authentic historical binding','RuntimeError')
  eq(e,{'current_binding_control_operand':want,'genuine_historical_binding':deps['historical_interpreter'],'historical_provenance':deps['historical_interpreter_provenance'],'reads':reads,'calls':calls,'refusal':refusal,'snapshot_observers_substituted':snapshot,'provenance_after_authentication_mutated_in_memory':kind=='provenance_missing','actual_current_interpreter_observed':False})
  case_checks.append({'id':identifier,'passed':True,'entire_envelope_reconstructed':True,'calls':calls,'reads':reads,'refusal':refusal})
control_tree=tree(C);eq(canonical_js(C/'NAMESPACE.json'),{'schema':'ri135-focused-controls-retained-namespace-v1','root':str(C),'entries':[x for x in control_tree if x['relative']!='NAMESPACE.json'],'excluded_not_yet_written':['NAMESPACE.json'],'partial_failure_artifacts_retained':True})
fulltree=tree(U);eq(canonical_js(U/'NAMESPACE.json'),{'schema':'ri139-retained-launcher-namespace-v1','root':str(U),'entries':[x for x in fulltree if x['relative'] not in ['NAMESPACE.json','COMPLETE.json']],'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json'],'all_partials_retained':True})
admin={'report':pin(C/'REPORT.json'),'namespace':pin(C/'NAMESPACE.json'),'controls':IDS,'count':25,'complete_administrative_envelopes_checked':True,'scientific_evaluation':False};eq(canonical_js(U/'ADMINISTRATIVE_CHECKS.json'),admin);eq(canonical_js(U/'ENVELOPE_CHECKS.json'),{'report':pin(C/'REPORT.json'),'checks':[{'id':i,'error':None} for i in IDS]})
assert type(complete['elapsed_seconds']) is float and mon['elapsed_seconds']<=complete['elapsed_seconds']<=900
expected_complete={'schema':'ri139-focused-launcher-completion-v1','status':'CAPTURED_FOR_ROOT_REVIEW','admission':pin(O/'cards/launcher.json'),'launcher_command':launcher,'child_command':child,'environment':card['environment'],'limits':limits,'external_premises':premises,'first_error':None,'independent_tail_errors':[],'checks':{'controls':admin,'source':'PASS','dependency':'PASS','card':'PASS','namespace':pin(U/'NAMESPACE.json')},'artifacts':{'attempt':pin(U/'ATTEMPT.json'),'administrative_checks':pin(U/'ADMINISTRATIVE_CHECKS.json')},'child':mon,'elapsed_seconds':complete['elapsed_seconds'],'scientific_execution':False,'runtime_qualification':False,'ri130_65_guards_executed':False,'genuine_tool_completion_created':False,'ret_paused':True};eq(complete,expected_complete)
# Recorded timestamp order corroborates the genuine root chronology; it is not an independent clock/authenticator.
chronology=['RI139_ROOT_ADJUDICATION.json','BOOTSTRAP_PRE.json','BOOTSTRAP_HOST_PREFLIGHT.json','ROOT_DISPATCH.json']
times=[(D/n).stat().st_mtime_ns for n in chronology]+[(U/'ATTEMPT.json').stat().st_mtime_ns,(U/'COMPLETE.json').stat().st_mtime_ns,(D/'BOOTSTRAP_POST.json').stat().st_mtime_ns];assert times==sorted(times)
oldfailure=js(B/'ri137-root-launch-adjudication-ie1m0jc_/GENUINE_TOOL_INITIAL.json');assert oldfailure['result']['exit_code']==1
result={'schema':'ri139-independent-saved-focused25-check-v1','all_checks_passed':True,'reviewer':'/root/ri116_complete_caller_review','root_dispatch':pin(D/'ROOT_DISPATCH.json'),'outer_initial':pin(D/'GENUINE_TOOL_INITIAL.json'),'outer_final':pin(D/'GENUINE_TOOL_FINAL.json'),'actual_tool_chain':{'initial_chunk':'7538a9','session':12210,'terminal_chunk':'0982f4','exit_code':0,'origin_premise':'Parent genuine tool history binds terminal poll to session; final saved object itself has no session field.'},'source_and_dependency_rows_checked':325,'dependencies':310,'all_recorded_static_states_unchanged':True,'pre_post_bytes_identical':True,'bootstrap_saved_rows':2004,'bootstrap_file_bytes':48024515,'bootstrap_file_modules':module_rows,'current_runtime_observed_by_reviewer':False,'controls':case_checks,'counts':{'F01':14,'F02':11,'total':25,'passed':25,'declared_positives':2,'expected_refusals':23},'monitor':{'samples':sample_records,'count':30,'peak_rss_kib':mon['peak_sampled_rss_kib'],'maximum_recorded_gap_seconds':max(s['gap_seconds'] for s in mon['samples']),'final_gap_seconds':finalgap,'child_elapsed_seconds':mon['elapsed_seconds'],'wrapper_elapsed_seconds':complete['elapsed_seconds'],'pid_owner':ma['pid_owner'],'pid_is_parent_not_authenticated_child':True,'arithmetic_tolerance_only':1e-12,'thresholds_unrelaxed':True},'control_namespace':control_tree,'full_output_namespace':fulltree,'all_read_file_identities':list(READ.values()),'recorded_chronology':list(zip(chronology+['output/ATTEMPT','output/COMPLETE','BOOTSTRAP_POST'],times)),'next_current_preparation_prerequisite':'Reconcile unchanged RI135 BOOTSTRAP=/usr/bin/python3 real PRE/POST snapshot command route before actual capture; focused F01 snapshots are explicit doubles and do not qualify that route. Then separately admit current baseline capture, accepted normal then optimized profile, separately admitted65 guards.','RI137_prior_attempt_remains_rejected':True,'subject_reexecution':False,'source_import_compile_ast_probe':False,'new_runtime_observation':False,'scientific_decode':False,'new_admission_or_fixture':False,'repo_or_git_actions':False}
with (R/'SAVED_EVIDENCE_CHECK.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'artifact':pin(R/'SAVED_EVIDENCE_CHECK.json'),'controls':result['counts'],'monitor':{k:v for k,v in result['monitor'].items() if k!='samples'},'control_tree_entries':len(control_tree),'output_tree_entries':len(fulltree),'all_checks_passed':True},indent=2))
