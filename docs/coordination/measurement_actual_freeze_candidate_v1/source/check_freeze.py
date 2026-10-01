"""UNEXECUTED root postcheck proposal for saved freeze candidate. No subject import; no acceptance issued."""
import hashlib, importlib.util, os, stat, subprocess, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri206-root-freeze-5e_n5lj_'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
sources=m.load(D/'SOURCES_BEFORE.json');runtime=m.load(D/'RUNTIME_BEFORE.json');dispatch=m.load(D/'DISPATCH.json');genuine=m.load(D/'GENUINE_TOOL.json')
for name in ('admission','request','preflight','bootstrap','monitor_source'):m.verify(dispatch[name]['path'],dispatch[name])
supplement=m.load(D/'CLOSURE_SUPPLEMENT.json')
preflight=m.load(dispatch['preflight']['path'])
assert preflight['source_observation']==m.ref(D/'SOURCES_BEFORE.json')
assert preflight['source_supplement']==m.ref(D/'CLOSURE_SUPPLEMENT.json')
assert preflight['runtime_observation']==m.ref(D/'RUNTIME_BEFORE.json')
assert preflight['E_observation']==m.ref(D/'E_BEFORE.json')
for r in sources['sources']+supplement['current_additional_identities']+runtime['vendor']+runtime['tools']:assert m.identity(r['path'])==r
state=lambda st:[st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
for r in runtime['namespace']:
 p=Path(r['path']);assert state(p.lstat())==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert p.is_symlink() and os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in runtime['absent']) and list(os.uname())==runtime['host']['uname']
host=subprocess.run(runtime['host']['argv'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==runtime['host']['exit_code']==0 and host.stdout.decode()==runtime['host']['stdout'] and host.stderr.decode()==runtime['host']['stderr']==''
def tree(root):
 rows=[]
 for p in [root,*sorted(root.rglob('*'))]:
  assert not p.is_symlink();kind='directory' if p.is_dir() else 'file';rel='.' if p==root else str(p.relative_to(root))
  row=dict(relative=rel,kind=kind,state=state(p.lstat()))
  if kind=='file':assert p.stat().st_nlink==1;row['identity']=m.identity(p)
  else:row['entries']=sorted(x.name for x in p.iterdir())
  rows.append(row)
 return rows
def compact(rows):return sorted([dict(relative=r['relative'],kind=r['kind'],**(m.pure(r['identity']) if r['kind']=='file' else {})) for r in rows],key=lambda r:r['relative'])
def observe(path):return {k:m.identity(path)[k] for k in ('path','bytes','sha256','state')}
admit=m.load(dispatch['admission']['path']);out=Path(admit['output']);mon=D/'monitor';E=B/'ri154-white-execution-proposed-42_uvw15'
trees={k:tree(p) for k,p in [('operation',out),('monitor',mon),('tmp',D/'tmp'),('E',E)]}
assert trees['E']==m.load(D/'E_BEFORE.json') and list((D/'tmp').iterdir())==[]
assert all(row['identity']['bytes']<=67108864 for key in ('operation','monitor') for row in trees[key] if row['kind']=='file')
produced_names=['ATTEMPT.json','RESULT.json']
assert sorted(p.name for p in out.iterdir())==sorted(produced_names+['COMPLETE.json'])
assert sorted(p.name for p in mon.iterdir())==['FREEZE.ATTEMPT.json','FREEZE.COMPLETION.json','FREEZE.stderr','FREEZE.stdout']
assert genuine['actual_arguments']['cmd']==dispatch['shell_command'] and genuine['actual_arguments']['workdir']==str(D) and genuine['actual_arguments']['login'] is False
assert genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and 'session_id' not in genuine['actual_result']
if 'session_id' in genuine['initial_result']:
 terminal=m.load(D/'GENUINE_TERMINAL_ARGUMENTS.json')
 assert terminal['actual_arguments']['session_id']==genuine['initial_result']['session_id'] and terminal['actual_arguments']['chars']==''
 assert terminal['actual_result']==genuine['actual_result']
 assert terminal['original_genuine_record']==m.ref(D/'GENUINE_TOOL.json')
else:assert genuine['initial_result']==genuine['actual_result']
c=m.load(mon/'FREEZE.COMPLETION.json');result=m.load(out/'RESULT.json');complete=m.load(out/'COMPLETE.json');attempt=m.load(out/'ATTEMPT.json')
command=[m.load(sources['inputs']['source_manifest']['path'])['bootstrap_binding']['path'],'-I','-B',str(B/'ri160-white-fixture-custody-repair-ufok1zpo/adapter.py'),'--admission',dispatch['admission']['path']]
assert c['command']==command and c['environment']==runtime['environment']==admit['environment'] and c['wall_seconds']==180
assert c['child_exit_code']==0 and c['first_error'] is None and c['tail_errors']==[] and c['stop_reason'] is None and c['passed'] is True
assert 0<c['elapsed_seconds']<180 and c['peak_sampled_rss_kib']<=524288 and c['final_sample_gap_passed'] is True
assert 0<len(c['samples'])<=len(c['monitor_attempts'])<=len(c['samples'])+1
last=0
for a,sample in zip(c['monitor_attempts'],c['samples']):
 assert a['returncode']==0 and a['stderr']=='' and int(a['stdout'].strip())==sample['rss_kib']
 assert a['elapsed_seconds']==sample['elapsed_seconds'] and abs(sample['gap_seconds']-(sample['elapsed_seconds']-last))<1e-12
 assert 0<=sample['gap_seconds']<=0.1 and 0<=sample['rss_kib']<=524288;last=sample['elapsed_seconds']
if len(c['monitor_attempts'])>len(c['samples']):
 a=c['monitor_attempts'][-1];assert set(a)=={'elapsed_seconds','returncode','stdout','stderr'} and a['returncode']==1 and a['stdout'].strip()=='' and a['stderr']=='' and last<=a['elapsed_seconds']<=c['elapsed_seconds']
assert abs(c['final_sample_to_reap_gap_seconds']-(c['elapsed_seconds']-last))<1e-12 and 0<=c['final_sample_to_reap_gap_seconds']<=0.1
assert c['peak_sampled_rss_kib']==max(s['rss_kib'] for s in c['samples'])
for key in ('stdout','stderr'):m.verify(c[key]['path'],c[key]);assert c[key]['bytes']==0
ma=m.load(mon/'FREEZE.ATTEMPT.json');assert set(ma)=={'command','environment','wall_seconds','pid_owner','scientific_target_entry'} and ma['command']==command and ma['environment']==c['environment'] and ma['wall_seconds']==180 and type(ma['pid_owner']) is int and ma['pid_owner']>0 and ma['scientific_target_entry'] is False
assert attempt==dict(schema='ri156-exclusive-metadata-attempt-v1',admission=dispatch['admission'],action='freeze',no_retry=True,scientific_execution=False)
assert set(complete)=={'schema','action','status','admission','artifacts','first_error','independent_tails','elapsed_seconds_before_complete_write','authenticated_source_before','produced_output_pins','tail_observations','scientific_execution','root_acceptance_created','ret_paused'}
assert complete['schema']=='ri156-adapter-completion-v1' and complete['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW'
assert complete['admission']==dispatch['admission'] and complete['action']=='freeze' and complete['first_error'] is None and complete['scientific_execution'] is False and complete['root_acceptance_created'] is False and complete['ret_paused'] is True and 0<=complete['elapsed_seconds_before_complete_write']<=180
ct=complete['independent_tails'];assert set(ct)=={'admission','dependencies','namespace','request','sources',*('output:'+n for n in produced_names)} and all(set(v)=={'value','error'} and v['error'] is None for v in ct.values())
manifest=m.load(sources['inputs']['source_manifest']['path']);all_sources={**manifest['modules'],'adapter':manifest['adapter'],'manifest':sources['inputs']['source_manifest']}
expected_sources={k:observe(row['path']) for k,row in all_sources.items()}
assert complete['authenticated_source_before']==ct['sources']['value']==complete['tail_observations']['sources']==expected_sources
assert ct['dependencies']['value']==manifest['dependencies'] and ct['admission']['value']==dispatch['admission'] and ct['request']['value']==dispatch['request']
outputs={name:m.ref(out/name) for name in produced_names}
assert complete['produced_output_pins']==complete['tail_observations']['outputs']==outputs
for name,pin in outputs.items():assert ct['output:'+name]['value']==pin
assert complete['artifacts']==dict(attempt=outputs['ATTEMPT.json'],result=outputs['RESULT.json'])
namespace=[r for r in compact(trees['operation']) if r['relative']!='COMPLETE.json']
assert ct['namespace']['value']==complete['tail_observations']['namespace']==namespace
assert set(complete['tail_observations'])=={'sources','outputs','namespace','namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'}
for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):assert complete['tail_observations'][key]==[]
for key in ('namespace_fixture_trees','namespace_fixture_comparisons'):assert key not in complete['tail_observations']
# Reconstruct the whole17-field freeze candidate as administrative data.
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

summary=dict(schema='ri206-root-freeze-postcheck-v1',status='PASS_SAVED_FREEZE_CANDIDATE_PENDING_INDEPENDENT_ROOT_REVIEW',
 genuine_tool=m.ref(D/'GENUINE_TOOL.json'),preflight=dispatch['preflight'],sources_before=m.ref(D/'SOURCES_BEFORE.json'),runtime_before=m.ref(D/'RUNTIME_BEFORE.json'),
 sources_rechecked=len(sources['sources'])+len(supplement['current_additional_identities']),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),prior_role_rows_preserved=len(supplement['prior_role_rows']),
 vendor_files_rechecked=len(runtime['vendor']),vendor_bytes_rechecked=sum(r['bytes'] for r in runtime['vendor']),namespace_entries_rechecked=len(runtime['namespace']),primitives_rechecked=len(runtime['tools']),
 host_uname_unchanged=True,host_version_unchanged=True,complete_file_externally_included=True,result=m.ref(out/'RESULT.json'),complete=m.ref(out/'COMPLETE.json'),monitor=m.ref(mon/'FREEZE.COMPLETION.json'),
 request=dispatch['request'],candidate_fields=sorted(expected),candidate_field_count=len(expected),run_field_counts={key:len(value) for key,value in expected['runs'].items()},
 all_complete_candidate_fields_matched=True,E_unchanged=True,operation_files=3,all_seven_independent_tails_passed=True,
 elapsed_seconds=c['elapsed_seconds'],peak_sampled_rss_kib=c['peak_sampled_rss_kib'],samples=len(c['samples']),maximum_sample_gap_seconds=max(s['gap_seconds'] for s in c['samples']),final_gap_seconds=c['final_sample_to_reap_gap_seconds'],
 runtime_capture_executed=False,scientific_execution=False,candidate_acceptances_issued=False,freeze_issued=False,ret_paused=True,observed_at_unix_ns=time.time_ns())
print(m.save('POST_CUSTODY.json',dict(summary=summary,trees=trees)))
print(m.save('ACTUAL_FREEZE_POSTCHECK.json',summary))
