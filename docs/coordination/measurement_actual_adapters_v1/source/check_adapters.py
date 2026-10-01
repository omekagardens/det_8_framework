"""UNEXECUTED root postcheck proposal for saved adapters. No subject import; no acceptance issued."""
import hashlib, importlib.util, os, stat, subprocess, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri204-root-adapters-f04k2tg9'
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
assert sorted(p.name for p in mon.iterdir())==['ADAPTERS.ATTEMPT.json','ADAPTERS.COMPLETION.json','ADAPTERS.stderr','ADAPTERS.stdout']
assert genuine['actual_arguments']['cmd']==dispatch['shell_command'] and genuine['actual_arguments']['workdir']==str(D) and genuine['actual_arguments']['login'] is False
assert genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and 'session_id' not in genuine['actual_result']
if 'session_id' in genuine['initial_result']:
 terminal=m.load(D/'GENUINE_TERMINAL_ARGUMENTS.json')
 assert terminal['actual_arguments']['session_id']==genuine['initial_result']['session_id'] and terminal['actual_arguments']['chars']==''
 assert terminal['actual_result']==genuine['actual_result']
 assert terminal['original_genuine_record']==m.ref(D/'GENUINE_TOOL.json')
else:assert genuine['initial_result']==genuine['actual_result']
c=m.load(mon/'ADAPTERS.COMPLETION.json');result=m.load(out/'RESULT.json');complete=m.load(out/'COMPLETE.json');attempt=m.load(out/'ATTEMPT.json')
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
ma=m.load(mon/'ADAPTERS.ATTEMPT.json');assert set(ma)=={'command','environment','wall_seconds','pid_owner','scientific_target_entry'} and ma['command']==command and ma['environment']==c['environment'] and ma['wall_seconds']==180 and type(ma['pid_owner']) is int and ma['pid_owner']>0 and ma['scientific_target_entry'] is False
assert attempt==dict(schema='ri156-exclusive-metadata-attempt-v1',admission=dispatch['admission'],action='adapters',no_retry=True,scientific_execution=False)
assert set(complete)=={'schema','action','status','admission','artifacts','first_error','independent_tails','elapsed_seconds_before_complete_write','authenticated_source_before','produced_output_pins','tail_observations','scientific_execution','root_acceptance_created','ret_paused'}
assert complete['schema']=='ri156-adapter-completion-v1' and complete['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW'
assert complete['admission']==dispatch['admission'] and complete['action']=='adapters' and complete['first_error'] is None and complete['scientific_execution'] is False and complete['root_acceptance_created'] is False and complete['ret_paused'] is True and 0<=complete['elapsed_seconds_before_complete_write']<=180
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
# Reconstruct every candidate field using authenticated administrative operands.
# Never call acceptance_adapters, retained_contract, or a candidate subject.
def same(left,right):assert m.canonical(left)==m.canonical(right)
request=m.load(dispatch['request']['path']);same(request,m.load(sources['inputs']['request']['path']))
assert set(request)=={'root_decisions','profiles_acceptance','sidecars'}
decisions=request['root_decisions'];sidecars=request['sidecars'];g=m.load(sources['graph']['path'])
assert set(decisions)=={'source_review','independent_source_review','packet_handoff','guard_path_review','runtime_applicability'}
for row in list(decisions.values())+list(sidecars.values()):m.verify(row['path'],row)
source_decision=m.load(decisions['source_review']['path']);app=m.load(decisions['runtime_applicability']['path'])
limits={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05}
same([source_decision['schema'],source_decision['status'],source_decision['graph'],source_decision['helpers'],source_decision['sources'],source_decision['limits'],source_decision['independent_review'],source_decision['target_executed']],
 ['ri156-root-relocated-source-decision-v1','ACCEPT_EXACT_RELOCATED_WHITE_SOURCE',sources['graph'],g['helpers'],g['sources'],limits,decisions['independent_source_review'],False])
same([app['schema'],app['status'],app['root'],app['profiles_acceptance'],app['helpers'],app['sources']],
 ['ri156-root-current-runtime-applicability-v1','ACCEPT_CURRENT_RELOCATED_RUNTIME_APPLICABILITY',g['prospective_root'],request['profiles_acceptance'],g['helpers'],g['sources']])
profiles=m.load(request['profiles_acceptance']['path']);same(request['profiles_acceptance'],sources['inputs']['profiles'])
normal=m.load(profiles['completions']['profile_normal']['path']);optimized=m.load(profiles['completions']['profile_optimized']['path'])
pre=m.load(normal['artifacts']['PRE']['path']);report=m.load(normal['artifacts']['PROFILE']['path'])
for completion in (normal,optimized):same(pre,m.load(completion['artifacts']['PRE']['path']));same(pre,m.load(completion['artifacts']['POST']['path']))
names={'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}
assert set(sidecars)==set(names)
for key,field in names.items():assert Path(sidecars[key]['path']).read_bytes()==m.canonical(pre[field])
# These two literal pins are retained_contract constants, read as source only.
history={'bytes':29806,'sha256':'f78ca32b9de47f5390d20c4de44a87aa462b871ba1b51b3bc1329e08c8c6aafa'}
targets={'bytes':10760,'sha256':'69d927acb494c05ee45326b8e02159c99a583b7ee2533c947a1762b550b1ed83'}
caller=dict(schema='ri130-root-caller-source-review-v1',status='ACCEPT_RI130_WHITE_FABRICATED_CALLER_SOURCE_ONLY',helpers=g['helpers'],sources=g['sources'],history=history,targets=targets,limits=limits,source_review=decisions['independent_source_review'],packet_handoff=decisions['packet_handoff'],target_executed=False,ret_paused=True)
same(decisions['packet_handoff'],g['evidence']['ri130_handoff'])
gd=m.load(decisions['guard_path_review']['path']);old=m.load(g['evidence']['guard_acceptance']['path']);guardreport=m.load(old['report']['path'])
same([gd['schema'],gd['status'],gd['graph'],gd['old_guard_acceptance'],gd['helpers'],gd['root'],gd['additional_required_controls'],gd['guard_code_unchanged'],gd['path_sensitive_review_complete'],gd['new_guard_execution_claimed']],
 ['ri156-root-guard-path-applicability-v1','ACCEPT_EXACT_CODE_AND_REVIEWED_PATH_APPLICABILITY',sources['graph'],g['evidence']['guard_acceptance'],g['helpers'],g['prospective_root'],[],True,True,False])
same(old['helpers'],g['prior_original_guard_helpers']);assert len(old['helpers'])==len(g['helpers'])==11
for left,right in zip(old['helpers'],g['helpers']):same(Path(left['path']).name,Path(right['path']).name);same(left['pin'],right['pin'])
assert guardreport['packet']=='/Volumes/AI_DATA/development/det-review-evidence/ri130-white-qualification-caller-source-Q4Aq7hZg'
guards={**old,'helpers':g['helpers']}
runtime_candidate=dict(schema='ri130-root-current-runtime-review-v1',status='ACCEPT_CURRENT_WHITE_CALLER_RUNTIME',helpers=g['helpers'],sources=g['sources'],
 runtime_inventory={'path':sidecars['runtime_inventory']['path'],'pin':m.pure(sidecars['runtime_inventory'])},
 expected_runtime=report['profile_before'],interpreter=pre['interpreter'],scientific_targets_executed=False,
 profile_normal=normal['artifacts']['PROFILE'],profile_optimized=optimized['artifacts']['PROFILE'],profile_review=request['profiles_acceptance'],
 selection=sidecars['selection'],optional_namespaces=sidecars['optional_namespaces'],observed_dyld_routes=sidecars['observed_dyld_routes'],host_scope=sidecars['host_scope'])
for key in ('complete_pure_python_stdlib','site_startup_surface_bound','non_os_shared_library_closure_bound','fresh_actual_profile_checked','source_cache_selection_checked','optional_native_namespaces_checked','observed_dyld_routes_checked','trusted_host_scope_explicit'):
 assert app[key] is True;runtime_candidate[key]=True
expected={'caller':caller,'guards':guards,'runtime':runtime_candidate}
assert set(result)=={'caller','guards','runtime'} and len(caller)==11 and len(runtime_candidate)==23
# Whole canonical bytes compare catches extra/missing fields and bool/int drift.
assert (out/'RESULT.json').read_bytes()==m.canonical(expected)
# Selection/cache/loader/runtime contents remain inherited accepted observations,
# not newly observed execution evidence and not source/cache equivalence.

summary=dict(schema='ri204-root-adapters-postcheck-v1',status='PASS_SAVED_CANDIDATE_BINDINGS_PENDING_INDEPENDENT_ROOT_REVIEW',
 genuine_tool=m.ref(D/'GENUINE_TOOL.json'),preflight=dispatch['preflight'],sources_before=m.ref(D/'SOURCES_BEFORE.json'),runtime_before=m.ref(D/'RUNTIME_BEFORE.json'),
 sources_rechecked=len(sources['sources'])+len(supplement['current_additional_identities']),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),prior_role_rows_preserved=len(supplement['prior_role_rows']),
 vendor_files_rechecked=len(runtime['vendor']),vendor_bytes_rechecked=sum(r['bytes'] for r in runtime['vendor']),namespace_entries_rechecked=len(runtime['namespace']),primitives_rechecked=len(runtime['tools']),
 host_uname_unchanged=True,host_version_unchanged=True,complete_file_externally_included=True,result=m.ref(out/'RESULT.json'),complete=m.ref(out/'COMPLETE.json'),monitor=m.ref(mon/'ADAPTERS.COMPLETION.json'),
 request=dispatch['request'],candidate_fields=['caller','guards','runtime'],candidate_field_counts={key:len(value) for key,value in expected.items()},
 all_complete_candidate_fields_matched=True,E_unchanged=True,operation_files=3,all_seven_independent_tails_passed=True,
 elapsed_seconds=c['elapsed_seconds'],peak_sampled_rss_kib=c['peak_sampled_rss_kib'],samples=len(c['samples']),maximum_sample_gap_seconds=max(s['gap_seconds'] for s in c['samples']),final_gap_seconds=c['final_sample_to_reap_gap_seconds'],
 runtime_capture_executed=False,scientific_execution=False,candidate_acceptances_issued=False,freeze_issued=False,ret_paused=True,observed_at_unix_ns=time.time_ns())
print(m.save('POST_CUSTODY.json',dict(summary=summary,trees=trees)))
print(m.save('ACTUAL_ADAPTERS_POSTCHECK.json',summary))
