"""Author-only source text derivation, no generated program imported or run."""
from pathlib import Path
import difflib,hashlib,json
W=Path(__file__).resolve().parent;B=W.parents[1];D=W.parent;O=B/'ri204-root-adapters-f04k2tg9';P=O/'worker_proposal';changes=[]
def once(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def emit(name,oldname,text):
 with (W/name).open('x') as f:f.write(text)
 changes.extend(difflib.unified_diff((P/oldname).read_text().splitlines(True),text.splitlines(True),fromfile=str(P/oldname),tofile=str(W/name)))
prep=(P/'prepare_adapters.py').read_text()
prep=prep.replace("D=B/'ri204-root-adapters-f04k2tg9'","D=B/'ri206-root-freeze-5e_n5lj_'")
prep=prep.replace('UNEXECUTED RI204 proposal. Root review must precede use; prepares one adapters admission only.','UNEXECUTED RI206 proposal. Root review must precede use; prepares one freeze-candidate action admission only.')
start=prep.index('# Root authenticates the sealed proposal');end=prep.index('for row in refs.values():keep(row)',start)
prep=prep[:start]+'''# Root authenticates this sealed source before use. No captured source or
# accepted-looking candidate status provides its own authority.
W=Path(__file__).resolve().parent
for name in ('prepare_freeze.py','predispatch.py','check_freeze.py','CLOSURE_SEEDS.json','PROPOSAL_NOTES.md'):keep(m.ref(W/name))
seeds=load(dict(path=str(W/'CLOSURE_SEEDS.json'),bytes=10348,sha256='1177344b3b26ca618c2155773ac0458375949bc53a81235b97245aa7d2cdc5a5'))
assert seeds['status']=='PROPOSAL_NOT_ADMISSION'
refs['request']=seeds['request'];refs['adapters_acceptance']=seeds['adapters_acceptance']
assert refs['request']==dict(path=str(B/'ri204-root-adapters-f04k2tg9/FREEZE_REQUEST.json'),bytes=825,sha256='51b909b39939e545938eaf7f4903ecd4ab52842025a1826c28ee08aeaf68e0c2')
assert refs['adapters_acceptance']==dict(path=str(B/'ri204-root-adapters-f04k2tg9/ADAPTERS_ACCEPTANCE.json'),bytes=3842,sha256='21929f3fcc989233cdc0a479f7f5319ddc5458163f569dee3907a1f1965edcf9')
for row in seeds['administrative_records']:keep(row)
prior_sources=m.load(B/'ri204-root-adapters-f04k2tg9/SOURCES_BEFORE.json')
prior_supplement=m.load(B/'ri204-root-adapters-f04k2tg9/CLOSURE_SUPPLEMENT.json')
assert len(prior_sources['sources'])==722 and prior_supplement['current_additional_identities']==[]
assert len(prior_supplement['prior_role_rows'])==810
for row in prior_sources['sources']+prior_supplement['prior_role_rows']:keep(row)
def keep_refs(value):
 if type(value) is dict:
  if {'path','bytes','sha256'}<=set(value):keep({k:value[k] for k in ('path','bytes','sha256')});return
  if set(value)=={'path','pin'} and type(value['pin']) is dict and set(value['pin'])=={'bytes','sha256'}:keep(dict(path=value['path'],**value['pin']));return
  for item in value.values():keep_refs(item)
 elif type(value) is list:
  for item in value:keep_refs(item)
for row in seeds['administrative_records']:
 if Path(row['path']).name in ('ADAPTERS_ACCEPTANCE.json','FREEZE_REQUEST.json','RI206_MEASUREMENT_ASSIGNMENT.json','ROOT_PREPARATION_DECISION.json','INDEPENDENT_PREPARATION_REVIEW.json','INDEPENDENT_CONCRETE_PREFLIGHT_REVIEW.json','INDEPENDENT_ACTUAL_ADAPTERS_REVIEW.json','ACTUAL_ADAPTERS_POSTCHECK.json','GENUINE_TERMINAL_ARGUMENTS.json','MEASUREMENT_NEXT_ACTION.json'):
  keep_refs(m.load(row['path']))
request=refs['request'];request_value=load(request);accepted=load(refs['adapters_acceptance'])
assert set(request_value)=={'accepted_adapters'} and set(request_value['accepted_adapters'])=={'caller','guards','runtime'}
assert accepted['schema']=='ri204-root-actual-adapters-adjudication-v1' and accepted['status']=='ACCEPT_COMPLETE_ADMINISTRATIVE_ADAPTERS'
assert accepted['cards_are_complete_canonical_result_values'] is True and accepted['scientific_execution'] is False and accepted['freeze_issued'] is False and accepted['mode_admission_issued'] is False
assert request_value['accepted_adapters']==accepted['accepted_adapters']
prior_result=load(accepted['result']);cards={}
for key,row in request_value['accepted_adapters'].items():
 cards[key]=load(row);assert Path(row['path']).read_bytes()==m.canonical(prior_result[key]);keep_refs(cards[key])
assert set(prior_result)=={'caller','guards','runtime'} and cards['runtime']['profile_review']==refs['profiles']
# Opaque referenced scientific/history bodies are never decoded; only these
# declared administrative graph, admission and source-declaration records are.
''' + prep[end:]
old="""for key,field in {'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}.items():
 assert Path(request_value['sidecars'][key]['path']).read_bytes()==m.canonical(snapshots[0][field])"""
new="""assert m.canonical(cards['runtime']['interpreter'])==m.canonical(snapshots[0]['interpreter'])
for key,field in {'selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}.items():
 assert Path(cards['runtime'][key]['path']).read_bytes()==m.canonical(snapshots[0][field])
assert Path(cards['runtime']['runtime_inventory']['path']).read_bytes()==m.canonical(snapshots[0]['runtime_inventory'])
# Full static source-declaration roles used by the unchanged freeze consumer.
for key in ('caller','guards','runtime'):assert not Path(request_value['accepted_adapters'][key]['path']).is_relative_to(Path(g['prospective_root']))
keep(g['integrated_root'])
for name in ('TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json'):
 keep(m.ref(Path(g['prospective_root'])/name))"""
# is_relative_to is unavailable in the selected vendor3.9? It exists since3.9;
# use parent membership anyway to keep the administrative script conservative.
new=new.replace("not Path(request_value['accepted_adapters'][key]['path']).is_relative_to(Path(g['prospective_root']))", "Path(g['prospective_root']) not in Path(request_value['accepted_adapters'][key]['path']).parents")
prep=once(prep,old,new)
prep=prep.replace("operation=B/'ri156-operation-ri204-adapters-f04k2tg9'","operation=B/'ri156-operation-ri206-freeze-5e_n5lj_'")
start=prep.index("m.save('CLOSURE_SUPPLEMENT.json'");end=prep.index("m.save('SOURCES_BEFORE.json'",start)
prep=prep[:start]+'''m.save('CLOSURE_SUPPLEMENT.json',dict(schema='ri206-prior-role-custody-supplement-v1',
 prior=prior_supplement['prior'],prior_role_rows=prior_supplement['prior_role_rows'],
 ri204_source_record=m.ref(B/'ri204-root-adapters-f04k2tg9/SOURCES_BEFORE.json'),
 ri204_supplement=m.ref(B/'ri204-root-adapters-f04k2tg9/CLOSURE_SUPPLEMENT.json'),
 ri204_prior_source_rows=prior_sources['sources'],prior_roles=810,ri204_distinct_sources=722,
 current_additional_identities=[],total_current=len(sources),all_prior_roles_in_current_source_map=True,
 historical_states_are_not_current_observations=True,scientific_execution=False))
''' +prep[end:]
prep=prep.replace('ri204-root-adapters-preflight-v1','ri206-root-freeze-preflight-v1').replace('FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_ADAPTERS_ACTION','FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_FREEZE_CANDIDATE_ACTION').replace('exact accepted RI202 request','exact accepted RI204 request')
prep=prep.replace("action='adapters'","action='freeze'").replace('ADMIT_ADAPTERS.json','ADMIT_FREEZE_CANDIDATE.json').replace('ADAPTERS_BOOTSTRAP.py','FREEZE_BOOTSTRAP.py').replace('administrative adapters action','administrative freeze-candidate action').replace('ri204_whole_unchanged_ri141_adapters_monitor','ri206_whole_unchanged_ri141_freeze_monitor').replace("'ADAPTERS'","'FREEZE'")
emit('prepare_freeze.py','prepare_adapters.py',prep)
pre=(P/'predispatch.py').read_text().replace(str(O),str(D)).replace('ri204-fresh-predispatch-custody-v1','ri206-fresh-predispatch-custody-v1').replace("a['action']=='adapters'","a['action']=='freeze'")
emit('predispatch.py','predispatch.py',pre)
post=(P/'check_adapters.py').read_text().replace("D=B/'ri204-root-adapters-f04k2tg9'","D=B/'ri206-root-freeze-5e_n5lj_'").replace('saved adapters','saved freeze candidate').replace('ADAPTERS','FREEZE').replace("action='adapters'","action='freeze'").replace("complete['action']=='adapters'","complete['action']=='freeze'")
start=post.index('# Reconstruct every candidate field');end=post.index("summary=dict(schema=",start)
post=post[:start]+'''# Reconstruct the whole17-field freeze candidate as administrative data.
# Do not call bindings.freeze_record, retained_contract or another target helper.
def same(left,right):assert m.canonical(left)==m.canonical(right)
request=m.load(dispatch['request']['path']);same(request,m.load(sources['inputs']['request']['path']))
assert set(request)=={'accepted_adapters'} and set(request['accepted_adapters'])=={'caller','guards','runtime'}
accepted=m.load(sources['inputs']['adapters_acceptance']['path'])
assert accepted['status']=='ACCEPT_COMPLETE_ADMINISTRATIVE_ADAPTERS' and accepted['cards_are_complete_canonical_result_values'] is True
same(request['accepted_adapters'],accepted['accepted_adapters'])
prior_result=m.load(accepted['result']['path']);cards={}
for key,row in request['accepted_adapters'].items():
 m.verify(row['path'],row);cards[key]=m.load(row['path']);assert Path(row['path']).read_bytes()==m.canonical(prior_result[key])
g=m.load(sources['graph']['path']);runtime_card=cards['runtime'];root=Path(g['prospective_root'])
limits={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05}
expected_environment={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(root/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
same(g['proposed_environment'],expected_environment)
expected={'schema':'ri130-white-fabricated-freeze-v1','status':'ROOT_AUTHORIZED_WHITE_FABRICATED_ONLY',
 'phase':'fabricated_white_qualification','context':'RI125_FABRICATED_ONLY_NOT_HISTORICAL',
 'claim':'Fixed fabricated WHITE qualification only; full32 application, actual data and physical claims remain unqualified; RET paused.',
 'root':str(root),'inputs':[],'sources':g['sources'],'helpers':g['helpers'],'limits':limits,'environment':expected_environment,
 'interpreter':runtime_card['interpreter'],'runtime_inventory':runtime_card['runtime_inventory'],'expected_runtime':runtime_card['expected_runtime'],
 'evidence':{'integration':g['integrated_root'],**request['accepted_adapters']},'runs':{},'mode_admissions':{}}
for mode in ('normal','optimized'):
 prefix=[runtime_card['interpreter']['named_path'],'-I','-B']+(['-O'] if mode=='optimized' else [])
 freeze_path=str(root/'AUTHORIZED_FREEZE.json');run=root/'runs'/mode
 expected['runs'][mode]={'command':prefix+[str(root/'worker.py'),freeze_path,mode],
  'launcher_command':prefix+[str(root/'launch.py'),freeze_path,mode],
  'stdout':str(run/'CALLER_ENVELOPE.json'),'stderr':str(run/'stderr'),'worker_receipt':str(run/'WORKER.json'),
  'receipt':str(run/'SUPERVISOR.json'),'claim':str(run/'ATTEMPT.json'),'custody':str(run/'CUSTODY.json'),'stage':str(run/'white-stage')}
 expected['mode_admissions'][mode]=str(root/('ADMIT_'+mode.upper()+'.json'))
assert len(expected)==17 and all(len(r)==9 for r in expected['runs'].values())
assert (out/'RESULT.json').read_bytes()==m.canonical(expected)
# Reconcile the actual static source/acceptance premises without importing K.
# Both declaration JSONs contain source/admin pins, never numeric fixture bodies.
target_pin={'bytes':10760,'sha256':'69d927acb494c05ee45326b8e02159c99a583b7ee2533c947a1762b550b1ed83'}
history_pin={'bytes':29806,'sha256':'f78ca32b9de47f5390d20c4de44a87aa462b871ba1b51b3bc1329e08c8c6aafa'}
m.verify(root/'TARGET_CLOSURE.source-only.json',target_pin);m.verify(root/'HISTORY_CLOSURE.source-only.json',history_pin)
decl=m.load(root/'TARGET_CLOSURE.source-only.json');history=m.load(root/'HISTORY_CLOSURE.source-only.json')
same(decl['packet_counts'],{'primary':13,'validator':8,'qualifier':9})
assert decl['schema']=='ri130-white-target-source-closure-v1' and decl['status']=='UNEXECUTED_SOURCE_DECLARATION_ONLY'
assert len(decl['sources'])==30 and len({row['relative'] for row in decl['sources']})==30
sources_from_decl=[{'relative':r['relative'],'original':r['original'],'copy':str(root/r['relative']),'pin':r['pin']} for r in decl['sources']]
same(expected['sources'],sources_from_decl);same(expected['evidence']['integration'],decl['integrated_root'])
assert len(history)==124
for row in history:m.verify(row['path'],row)
helper_names=('control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','profile_observe.source-only.py','guard_controls.source-only.py','TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json')
same([Path(row['path']).name for row in expected['helpers']],list(helper_names))
for row,name in zip(expected['helpers'],helper_names):same(row['path'],str(root/name));m.verify(row['path'],row['pin'])
integration=m.load(expected['evidence']['integration']['path'])
assert integration['status']=='ACCEPT_BOUNDED_UNEXECUTED_WHITE_VALIDATOR_AND_QUALIFIER_INTEGRATION' and integration['source_execution'] is False and integration['qualification_accepted'] is False
caller=cards['caller'];guards=cards['guards']
assert set(caller)=={'schema','status','helpers','sources','history','targets','limits','source_review','packet_handoff','target_executed','ret_paused'}
same([caller['schema'],caller['status'],caller['history'],caller['targets'],caller['target_executed'],caller['ret_paused']],['ri130-root-caller-source-review-v1','ACCEPT_RI130_WHITE_FABRICATED_CALLER_SOURCE_ONLY',history_pin,target_pin,False,True])
for key in ('helpers','sources','limits'):same(caller[key],expected[key])
for key in ('source_review','packet_handoff'):m.verify(caller[key]['path'],caller[key])
same([guards['schema'],guards['status'],guards['helpers'],guards['all_declared_guards_passed'],guards['scientific_targets_executed']],['ri130-root-guard-qualification-v1','ACCEPT_EXACT_CALLER_GUARD_EXECUTION',expected['helpers'],True,False])
for key in ('report','genuine_outer','independent_review'):m.verify(guards[key]['path'],guards[key])
# Full exact ordered65 control IDs copied as literal administrative inventory;
# this consumes accepted saved outcomes only, never invokes a guard.
guard_ids=[side+'_'+kind for side in ('parent','worker') for kind in ('source','caller','runtime_acceptance','mode','late','late_postcheck')]
guard_ids+=['capture_'+x for x in ('positive','changed_copy','buffer_drift','occupied')]
guard_ids+=['monitor_'+x for x in ('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap')]
guard_ids+=['runtime_'+x for x in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config')]
guard_ids+=['static_'+x for x in ('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command')]
guard_ids+=['acceptance_'+x for x in ('positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile')]
guard_ids+=['mode_'+x for x in ('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift')]
guard_ids+=['relation_'+x for x in ('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped')]
assert len(guard_ids)==65
report=m.load(guards['report']['path']);same(report['control_order'],guard_ids);same([row['id'] for row in report['controls']],guard_ids)
same(report['counts'],{'total':65,'passed':65,'failed':0})
assert report['schema']=='ri130-nonscientific-caller-guards-v1' and report['status']=='all_declared_guards_passed' and report['helpers_unchanged'] is True
assert report['target_or_scientific_helper_imported'] is False and report['scientific_fixtures_or_controls_executed'] is False and all(row['passed'] is True for row in report['controls'])
executed_helpers={'control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py'}
helper_pins={Path(row['path']).name:row['pin'] for row in expected['helpers'] if Path(row['path']).name in executed_helpers}
same(report['helpers_before'],helper_pins);same(report['helpers_after'],helper_pins)
same([runtime_card['schema'],runtime_card['status'],runtime_card['helpers'],runtime_card['sources'],runtime_card['scientific_targets_executed']],['ri130-root-current-runtime-review-v1','ACCEPT_CURRENT_WHITE_CALLER_RUNTIME',expected['helpers'],expected['sources'],False])
for key in ('runtime_inventory','expected_runtime','interpreter'):same(runtime_card[key],expected[key])
for key in ('complete_pure_python_stdlib','site_startup_surface_bound','non_os_shared_library_closure_bound','fresh_actual_profile_checked','source_cache_selection_checked','optional_native_namespaces_checked','observed_dyld_routes_checked','trusted_host_scope_explicit'):assert runtime_card[key] is True
for key in ('profile_normal','profile_optimized','profile_review','selection','optional_namespaces','observed_dyld_routes','host_scope'):m.verify(runtime_card[key]['path'],runtime_card[key])
# The authoritative-looking candidate strings are the retained schema. Neither
# this RESULT nor this postcheck writes AUTHORIZED_FREEZE or a mode admission.
assert not os.path.lexists(root/'AUTHORIZED_FREEZE.json')
assert all(not os.path.lexists(root/('ADMIT_'+mode.upper()+'.json')) for mode in ('normal','optimized'))

''' + post[end:]
post=post.replace('ri204-root-adapters-postcheck-v1','ri206-root-freeze-postcheck-v1').replace('PASS_SAVED_CANDIDATE_BINDINGS_PENDING_INDEPENDENT_ROOT_REVIEW','PASS_SAVED_FREEZE_CANDIDATE_PENDING_INDEPENDENT_ROOT_REVIEW')
post=once(post,"request=dispatch['request'],candidate_fields=['caller','guards','runtime'],candidate_field_counts={key:len(value) for key,value in expected.items()},", "request=dispatch['request'],candidate_fields=sorted(expected),candidate_field_count=len(expected),run_field_counts={key:len(value) for key,value in expected['runs'].items()},")
post=post.replace('ACTUAL_ADAPTERS_POSTCHECK.json','ACTUAL_FREEZE_POSTCHECK.json')
emit('check_freeze.py','check_adapters.py',post)
with (W/'SOURCE_DIFF.patch').open('x') as f:f.write(''.join(changes))
print(json.dumps({'sources':[dict(path=str(W/n),bytes=len((W/n).read_bytes()),sha256=hashlib.sha256((W/n).read_bytes()).hexdigest()) for n in ('prepare_freeze.py','predispatch.py','check_freeze.py')],'source_programs_executed':False},indent=2))
