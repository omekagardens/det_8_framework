"""Independent RI154 administrative identity/map review, no subject execution.
Only the root-authenticated metadata helper is loaded. Scientific files opaque.
"""
import collections, hashlib, importlib.util, json, os
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri154-independent-relocation-review-_2275plo'
A=B/'ri154-white-mode-preparation-42_uvw15'
S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
Q=B/'ri141-white-bootstrap-source-h58ls076'
helper=B/'ri122-root-execution-review-6whn_vky/metadata.py'
b=helper.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':
 raise ValueError('root metadata helper drift')
spec=importlib.util.spec_from_file_location('trusted_metadata',helper)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
checks=[]; observed={}; total=0

def require(value,label):
 checks.append({'label':label,'passed':bool(value)})
 if not value: raise ValueError(label)
def pin(path,expected=None):
 global total
 x=m.identity(str(path)); total+=1
 if expected is not None:require(m.pure(x)=={k:expected[k] for k in ('bytes','sha256')},'pin '+str(path))
 if str(path) in observed: require(x==observed[str(path)],'full current identity unchanged '+str(path))
 observed[str(path)]=x
 return x
def admin(path):
 # Only caller/author declarations and root acceptance metadata named below.
 return json.loads(Path(path).read_bytes())
def typed_equal(x,y):
 return json.dumps(x,sort_keys=True,ensure_ascii=True,allow_nan=False)==json.dumps(y,sort_keys=True,ensure_ascii=True,allow_nan=False)
H=admin(A/'HANDOFF.json')
pin(A/'HANDOFF.json',{'bytes':7336,'sha256':'48aa2c11468fab405a1e15793916c42e38ee4562a6212d71987149076c8814d6'})
require(len(H['files'])==14 and len(H['exact_namespace'])==15,'14 payloads and 15 declared entries')
actual=sorted(p.name for p in A.iterdir())
require(actual==sorted(H['exact_namespace']),'exact author namespace')
for row in H['files']:
 require(Path(row['path']).parent==A,'payload confined to author reservation')
 pin(row['path'],row)
require(all(p.is_file() and not p.is_symlink() for p in A.iterdir()),'all author entries regular no links')
D=admin(A/'DEPENDENCIES.json');G=admin(A/'BINDING_GRAPH.source-only.json');P=admin(A/'PREPARATION_CHECK.json');I=admin(A/'INTERFACE_FIELDS.source-only.json')
deps=admin(Q/'DEPENDENCIES.source-only.json')
require(typed_equal(D['inherited_ri141'],deps['opaque_files']) and len(deps['opaque_files'])==442,'entire inherited 442 ordered pins unchanged')
require(len(D['complete_read_files'])==463 and len({x['path'] for x in D['complete_read_files']})==463,'463 unique permitted input paths')
lookup={r['path']:r for r in D['complete_read_files']}
for row in D['complete_read_files']:
 require((str(Path(row['path'])).startswith(str(B)+'/') or str(Path(row['path'])).startswith('/Volumes/AI_DATA/development/det_8_framework-ret/')) and '/env/' not in row['path'],'only historical source/evidence domain '+row['path'])
 pin(row['path'],row)
for row in deps['opaque_files']:require(lookup[row['path']]==row,'inherited row retained '+row['path'])
additional=[r for r in D['complete_read_files'] if r['path'] not in {x['path'] for x in deps['opaque_files']}]
require(len(additional)==21,'exact 21 additional paths')
require(typed_equal(G['evidence'],D['direct_premises']) and len(G['evidence'])==19,'all 19 direct role references retained')
for name,row in G['evidence'].items():require(row==lookup[row['path']],'direct premise '+name)
E=Path(G['prospective_root'])
require(str(E)==str(B/'ri154-white-execution-proposed-42_uvw15') and not os.path.lexists(E),'literal prospective root remains absent')
require(G['root_created'] is False and G['all_proposed_copies_uncreated'] is True and G['source_changes']==[],'no copied source or active root claim')
sh=admin(S/'HANDOFF.json');t=admin(S/'TARGET_CLOSURE.source-only.json');h=admin(S/'HISTORY_CLOSURE.source-only.json')
originals=sorted([r['relative'] for r in sh['artifacts']]+['HANDOFF.json'])
require(len(originals)==48 and sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_file())==originals,'exact original 48-file namespace')
require(not any(x.is_symlink() for x in S.rglob('*')),'original sealed source namespace link-free')
require([r['relative'] for r in G['copied_files']]==originals,'all 48 copy names in original order')
for row in G['copied_files']:
 name=row['relative'];require(row['source']==lookup[str(S/name)] and row['destination']==str(E/name),'exact unchanged proposed copy '+name)
require(len(t['sources'])==30 and len(G['sources'])==30 and G['target_count']==30,'30 complete source records')
for old,new in zip(t['sources'],G['sources']):
 expected={'relative':old['relative'],'original':old['original'],'copy':str(E/old['relative']),'pin':old['pin']}
 require(typed_equal(new,expected),'entire source pair '+old['relative'])
 for path in (old['original'],str(S/old['relative'])):
  require({k:lookup[path][k] for k in ('bytes','sha256')}==old['pin'],'original/copy pin relationship '+path)
helpers=['control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','profile_observe.source-only.py','guard_controls.source-only.py','TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json']
require(G['helper_count']==11 and len(G['helpers'])==11,'11 helpers/declarations')
for name,row in zip(helpers,G['helpers']):require(row=={'path':str(E/name),'pin':{k:lookup[str(S/name)][k] for k in ('bytes','sha256')}},'full helper mapping '+name)
require(typed_equal(G['history_originals'],h) and len(h)==124 and G['history_count']==124,'all 124 original history roles unmodified')
for row in h:require(lookup[row['path']]==row,'history retains actual pin '+row['path'])
roles=dict(zip(['white_kernel','white_path','wrapper_controls','white_contract','cases','kernel_refusals','fabricated_interfaces','white_refusals_text','white_source_handoff','fixtures','kernel_controls','orchestrator','stage_contract','control_expectations','validator','validator_controls'],['science/primary/white_kernel.py','science/primary/white_path.py','science/primary/white_controls.py','science/primary/CONTRACT.md','science/primary/CASES.md','science/primary/KERNEL_REFUSALS.md','science/primary/FABRICATED_INTERFACES.md','science/primary/WHITE_REFUSALS.md','science/primary/HANDOFF.json','science/qualifier/white_fixtures.py','science/qualifier/kernel_controls.py','science/qualifier/qualify_white_only.py','science/qualifier/STAGE_CONTRACT.md','science/qualifier/CONTROL_EXPECTATIONS.json','science/validator/white_validator.py','science/validator/validator_controls.py']))
expected={k:{'path':str(E/v),'pin':{x:lookup[str(S/v)][x] for x in ('bytes','sha256')}} for k,v in roles.items()}
expected['white_root_disposition']={'path':t['white_root']['path'],'pin':{k:t['white_root'][k] for k in ('bytes','sha256')}}
require(typed_equal(G['stage_bindings'],expected) and G['stage_role_count']==17,'complete 17 role mapping including unmoved decision')
require(G['integrated_root']==t['integrated_root'],'integration unchanged')
union=set(helpers)|{r['relative'] for r in t['sources']}
require(len(set(originals)-union)==7,'seven full packet provenance files outside helper/target union')
guard=admin(G['evidence']['guard_acceptance']['path']);profiles=admin(G['evidence']['profiles_acceptance']['path'])
require(G['prior_original_guard_helpers']==guard['helpers'],'actual old helper paths preserved')
require(guard['helpers']!=G['helpers'],'R01 actual literal helper mismatch')
for old,new in zip(guard['helpers'],G['helpers']):require(old['pin']==new['pin'] and old['path']==str(S/Path(new['path']).name),'R01 same bytes only '+new['path'])
require(profiles['packet']==str(S) and profiles['environment_root']==G['old_environment_root'] and profiles['environment_root']!=str(E),'R02 actual original packet and old environment mismatch')
require(G['proposed_environment']=={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(E/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'},'complete prospective ten-field environment')
# Independent transcription of literal interfaces manually checked against code.
fields={
'caller_source_acceptance':'schema status helpers sources history targets limits source_review packet_handoff target_executed ret_paused',
'freeze':'schema status phase context claim root inputs sources helpers limits environment interpreter runtime_inventory expected_runtime evidence runs mode_admissions',
'guard_acceptance_required':'schema status helpers all_declared_guards_passed scientific_targets_executed report genuine_outer independent_review',
'normal_acceptance_required':'schema status freeze all15_cases_and_W09_assembly both179_controls complete_saved_reconstruction all57_artifacts_74_postchecks_3_trees runtime_post_custody_passed genuine_outer independent_review post_runtime_metadata outputs',
'normal_outputs':'stdout stderr worker_receipt receipt custody claim',
'pre_mode_runtime_record_required':'schema mode freeze runtime_acceptance selection_unchanged optional_namespaces_unchanged host_identity_unchanged observed_dyld_routes metadata_record',
'ri141_genuine_outer':'schema status command environment exit_code completion raw_tool_receipt external_timeout_seconds',
'ri141_parent_completion':'schema phase status command environment admission sources artifacts first_error independent_tail_errors elapsed_seconds scientific_targets_executed actual_data_admitted full32_qualified ret_paused runtime_acceptance_created genuine_outer_created',
'ri141_preparation_admission':'schema status phase sources source_review packet output environment_root bootstrap bootstrap_host_preflight host baseline_acceptance normal_acceptance profiles_acceptance guard_admission bounds genuine_outer_required',
'ri141_stage_acceptance':'schema status stage sources packet environment_root completions genuine_outer independent_review scientific_execution',
'runtime_acceptance_required':'schema status helpers sources runtime_inventory expected_runtime interpreter complete_pure_python_stdlib site_startup_surface_bound non_os_shared_library_closure_bound fresh_actual_profile_checked source_cache_selection_checked optional_native_namespaces_checked observed_dyld_routes_checked trusted_host_scope_explicit scientific_targets_executed profile_normal profile_optimized profile_review selection optional_namespaces observed_dyld_routes host_scope',
'separate_mode_admission':'schema status mode phase freeze caller_source_acceptance command launcher_command pre_runtime_metadata normal_acceptance',
'stage_envelope':'result report_pin artifacts postchecks tree_postchecks namespace refusal',
'stage_report':'schema phase status context scope limits source_bindings cases complete_capture_assembly controls fresh_saved_comparison artifacts limitations',
'supervisor_before':'sources source_admission mode_admission runtime profile loaded',
'supervisor_postchecks':'freeze sources source_admission mode_admission runtime profile loaded namespace',
'supervisor_retained_outputs':'stdout stderr worker_receipt custody claim',
'supervisor_success':'schema mode phase context freeze limits command launcher_command environment before postchecks monitor_attempts samples peak_sampled_rss_kib child_exit_code child_elapsed_seconds final_sample_to_reap_gap_seconds final_sample_gap_passed stop_reason status error worker_check mode_relation retained_outputs full32_qualified actual_data_admitted ret_paused child_pid ownership_tail pre_receipt_namespace',
'worker_before':'sources source_admission mode_admission runtime profile loaded',
'worker_custody_success':'schema mode phase freeze status error entry_invocations entry_returned envelope_pin saved_custody namespace_after full32_qualified actual_data_admitted',
'worker_postchecks':'freeze sources source_admission mode_admission captured_targets runtime profile loaded namespace saved_custody',
'worker_success':'schema mode phase context freeze limits source_count actual_scientific_inputs entry entry_phase entry_invocations entry_returned target_load_witness before postchecks saved_custody namespace_after error status full32_qualified actual_data_admitted ret_paused captured_targets loaded_after_capture envelope_pin elapsed_seconds custody_pin'}
require(set(I['field_sets'])==set(fields)==set(I['field_counts']),'all 22 interface domains')
for name,text in fields.items():
 want=text.split();require(len(set(want))==len(want) and I['field_sets'][name]==want and I['field_counts'][name]==len(want),'entire manually traced interface '+name)
# Reconcile recorded administrative predicates by operation classes, not science.
require(P['status']=='PASS' and len(P['checks'])==4071,'author reported 4071 metadata predicates')
for row in P['checks']:require(set(row)=={'check','passed'} and type(row['check']) is str and row['passed'] is True,'literal successful administrative predicate')
classes=collections.Counter(row['check'].split('/Volumes')[0] for row in P['checks'])
wanted={'prospective root absent; never created':1,'permitted source/evidence domain ':766,'not installed runtime ':766,'regular opaque input ':766,'stable opaque read ':766,'all47 sealed RI130 payloads':1,'opaque expected pin ':622,'exact48 original source regular namespace':1,'sealed source namespace has no links':1,'repeat input unchanged ':303,'complete30 target records':1,'complete124 historical roles':1,'complete442 inherited preparation dependencies':1,'original/copy body ':60,'all17 distinct prospective roles':1,'old guard bytes equal proposed helper ':11,'old guard card cannot satisfy new literal helper paths':1,'old environment root differs from prospective WHITE root':1,'actual profiles bind original packet only':1}
require(dict(classes)==wanted,'full author predicate class census reconciles 4071 bookkeeping checks')
require(P['counts']=={'ri130_files':48,'prospective_copies':48,'target_pairs':30,'helpers':11,'history_roles':124,'stage_roles':17,'inherited_dependencies':442,'unique_opaque_inputs':463},'all author count fields')
for key in ('qualification_claim','driver_implemented','proposed_root_created'):require(P[key] is False,'no qualification claim '+key)
require(P['prohibited_actions_performed']==[],'no prohibited action claimed')
commands=admin(A/'ACTUAL_ADMIN_COMMANDS.json');final=admin(A/'FINAL_INPUT_CHECK.json');tool=admin(A/'FINAL_CHECK_TOOL.json')
require(commands['preparation']['tool_result']['chunk_id']=='c005ce' and commands['preparation']['tool_result']['exit_code']==0,'recorded author c005ce success descriptor')
require(commands['failed_administrative_checks']==[] and tool['tool_result']['chunk_id']=='e77f0a' and tool['tool_result']['exit_code']==0 and final['changed']==[] and final['checked']==463,'author retained administrative outcomes only')
require(final['dependency_manifest']=={'path':str(A/'DEPENDENCIES.json'),**m.pure(observed[str(A/'DEPENDENCIES.json')])},'author final result binds dependency declaration')
# Stable whole-file final checks for all observed source/evidence only.
for path,old in list(observed.items()):require(m.identity(path)==old,'final identity unchanged '+path)
result={'schema':'ri154-independent-administrative-map-review-v1','status':'PASS','subject_execution':False,'scientific_body_decode':False,'runtime_observation':False,'root_created':False,'counts':{'author_namespace':15,'author_payloads':14,'input_files':463,'inherited':442,'added':21,'copies':48,'target_pairs':30,'helpers':11,'history_roles':124,'stage_roles':17,'interface_domains':22,'author_administrative_predicates':4071,'fresh_reviewer_predicates':len(checks),'input_bytes':sum(x['bytes'] for x in D['complete_read_files']),'unique_observed_paths':len(observed)},'additional_inputs':additional,'author_predicate_classes':dict(classes),'checks':checks,'observed':list(observed.values()),'scope':'Fresh opaque identity and manual-transcription metadata checks. Recorded original tool descriptors are not independently authenticated process receipts. No subject or scientific engine executed.'}
m.save('METADATA_CHECK.json',result)
print(json.dumps({'status':'PASS','counts':result['counts']},sort_keys=True))
