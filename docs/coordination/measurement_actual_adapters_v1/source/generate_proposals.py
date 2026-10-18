"""Author-only literal text transformations; never executes generated sources."""
import difflib,hashlib,json
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=Path(__file__).resolve().parent;OLD=B/'ri200-root-sidecars-ofv27lvp';D=W.parent
changed=[]
def once(s,a,b):
 assert s.count(a)==1,(a,s.count(a))
 return s.replace(a,b)
def emit(name,oldname,text):
 p=W/name
 with p.open('x') as f:f.write(text)
 changed.append(''.join(difflib.unified_diff((OLD/oldname).read_text().splitlines(True),text.splitlines(True),fromfile=str(OLD/oldname),tofile=str(p))))
prep=(OLD/'prepare_sidecars.py').read_text().replace(str(OLD),str(D)).replace("D=B/'ri200-root-sidecars-ofv27lvp'","D=B/'ri204-root-adapters-f04k2tg9'")
prep=once(prep,'Root administrative custody and one sidecars admission; never loads a subject.','UNEXECUTED RI204 proposal. Root review must precede use; prepares one adapters admission only. Never loads a subject.')
closure='''# Root authenticates the sealed proposal before running this administrative
# preparation. These source captures extend custody, not self-authentication.
W=Path(__file__).resolve().parent
for name in ('prepare_adapters.py','predispatch.py','check_adapters.py','CLOSURE_SEEDS.json','PROPOSAL_NOTES.md'):
 keep(m.ref(W/name))
seeds=load(dict(path=str(W/'CLOSURE_SEEDS.json'),bytes=11142,sha256='bd796aae39a7984fe4fb4c6d57f6741bbe141fcd155af8f7c7e7f3093ef1824b'))
assert seeds['status']=='PROPOSAL_NOT_ADMISSION'
refs['request']=seeds['request']
assert refs['request']==dict(path=str(B/'ri202-root-two-maxima-review-kw07pwnj/ADAPTERS_REQUEST.json'),bytes=3021,sha256='d74665367f305626d445534f1591098e541d1c7b0836bc7ebdd096886b50ee11')
for row in seeds['administrative_records']:keep(row)
prior_sources=m.load(B/'ri200-root-sidecars-ofv27lvp/SOURCES_BEFORE.json')
prior_supplement=m.load(B/'ri200-root-sidecars-ofv27lvp/CLOSURE_SUPPLEMENT.json')
# Preserve every old role, but freshly observe all immutable body references.
assert len(prior_sources['sources'])==659 and len(prior_supplement['current_additional_identities'])==9
assert len(prior_supplement['prior_role_rows'])==810
for row in prior_sources['sources']+prior_supplement['current_additional_identities']+prior_supplement['prior_role_rows']:
 keep(row)
# Traverse FilePins only in explicitly administrative records. Referenced bodies
# remain opaque unless explicitly selected below; no scientific operand decoding.
def keep_refs(value):
 if type(value) is dict:
  if {'path','bytes','sha256'}<=set(value):keep({k:value[k] for k in ('path','bytes','sha256')});return
  if set(value)=={'path','pin'} and type(value['pin']) is dict and set(value['pin'])=={'bytes','sha256'}:keep(dict(path=value['path'],**value['pin']));return
  for item in value.values():keep_refs(item)
 elif type(value) is list:
  for item in value:keep_refs(item)
for row in seeds['administrative_records']:
 name=Path(row['path']).name
 if name in ('SIDECARS_ADJUDICATION.json','INDEPENDENT_SIDECARS_REVIEW.json','ACTUAL_SIDECARS_ROOT_REVIEW.json','GENUINE_TERMINAL_ARGUMENTS.json','ADAPTERS_REQUEST.json','RELOCATED_SOURCE_DECISION.json','INDEPENDENT_MEASUREMENT_INPUT_REVIEW.json','MEASUREMENT_NEXT_ACTION.json'):
  keep_refs(m.load(row['path']))
request=refs['request'];request_value=load(request)
assert set(request_value)=={'root_decisions','profiles_acceptance','sidecars'}
assert set(request_value['root_decisions'])=={'source_review','independent_source_review','packet_handoff','guard_path_review','runtime_applicability'}
assert set(request_value['sidecars'])=={'runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'}
assert request_value['profiles_acceptance']==refs['profiles']
for key in ('source_review','guard_path_review','runtime_applicability'):
 value=load(request_value['root_decisions'][key]);keep_refs(value)
prior_sidecars=m.load(B/'ri200-root-sidecars-ofv27lvp/ACTUAL_SIDECARS_ROOT_REVIEW.json')
assert request_value['sidecars']==prior_sidecars['sidecars']
assert m.load(B/'ri200-root-sidecars-ofv27lvp/SIDECARS_ADJUDICATION.json')['status']=='ACCEPT_FIVE_WHOLE_FIELD_ADMINISTRATIVE_SIDECARS'
'''
prep=once(prep,'for row in refs.values():keep(row)',closure+'\nfor row in refs.values():keep(row)')
prep=once(prep,"assert snapshots[0]==snapshots[1]","""assert snapshots[0]==snapshots[1]
for key,field in {'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}.items():
 assert Path(request_value['sidecars'][key]['path']).read_bytes()==m.canonical(snapshots[0][field])
# Native static and prior preflight are read as administrative premises, now pinned
# and included before the source observation is finalized.
static=B/'ri164-root-static-review-xr1qffz8/RI164_ROOT_ADJUDICATION.json'
load(dict(path=str(static),bytes=2910,sha256='001baa675b4bcc7a514537bdaaad9811f79b3170d85e3615368bf8320188ffb7'))
oldpre=load(m.ref(R/'BOOTSTRAP_PREFLIGHT.json'))""")
prep=prep.replace("operation=B/'ri156-operation-ri200-sidecars-ofv27lvp'","operation=B/'ri156-operation-ri204-adapters-f04k2tg9'")
prep=once(prep,"m.save('SOURCES_BEFORE.json',dict(sources=list(sources.values()),inputs=refs,graph=m.ref(gpath)))","""m.save('CLOSURE_SUPPLEMENT.json',dict(schema='ri204-prior-role-custody-supplement-v1',
 prior=prior_supplement['prior'],prior_role_rows=prior_supplement['prior_role_rows'],
 ri200_source_record=m.ref(B/'ri200-root-sidecars-ofv27lvp/SOURCES_BEFORE.json'),
 ri200_supplement=m.ref(B/'ri200-root-sidecars-ofv27lvp/CLOSURE_SUPPLEMENT.json'),
 ri200_prior_source_rows=prior_sources['sources'],ri200_prior_additional_identities=prior_supplement['current_additional_identities'],
 prior_roles=810,ri200_distinct_sources=668,current_additional_identities=[],
 total_current=len(sources),all_prior_roles_in_current_source_map=True,
 historical_states_are_not_current_observations=True,scientific_execution=False))
m.save('SOURCES_BEFORE.json',dict(sources=list(sources.values()),inputs=refs,graph=m.ref(gpath)))""")
prep=once(prep,"static=B/'ri164-root-static-review-xr1qffz8/RI164_ROOT_ADJUDICATION.json';m.verify(static,dict(bytes=2910,sha256='001baa675b4bcc7a514537bdaaad9811f79b3170d85e3615368bf8320188ffb7'))\noldpre=m.load(R/'BOOTSTRAP_PREFLIGHT.json')",'# Static/prior-preflight inputs already pinned in the finalized source closure.')
prep=prep.replace('ri200-root-sidecars-preflight-v1','ri204-root-adapters-preflight-v1').replace('FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_SIDECARS_ACTION','FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_ADAPTERS_ACTION')
prep=once(prep,"request=m.save('SIDECARS_REQUEST.json',dict(profiles_acceptance=refs['profiles']));assert m.pure(request)==dict(bytes=271,sha256='58779511da1b24febd2e000415bb9e115c1870699bdba2812466032364411db1')",'# The exact accepted RI202 request is consumed at its original path; never regenerated.\nassert request==refs[\'request\']')
prep=prep.replace("action='sidecars'","action='adapters'").replace('ADMIT_SIDECARS.json','ADMIT_ADAPTERS.json').replace('SIDECARS_BOOTSTRAP.py','ADAPTERS_BOOTSTRAP.py').replace('administrative sidecars action','administrative adapters action').replace('ri200_whole_unchanged_ri141_sidecars_monitor','ri204_whole_unchanged_ri141_adapters_monitor').replace("'SIDECARS'","'ADAPTERS'")
emit('prepare_adapters.py','prepare_sidecars.py',prep)
pre=(OLD/'predispatch.py').read_text().replace(str(OLD),str(D)).replace('ri200-fresh-predispatch-custody-v1','ri204-fresh-predispatch-custody-v1')
pre=once(pre,"sources=m.load(D/'SOURCES_BEFORE.json');runtime=m.load(D/'RUNTIME_BEFORE.json');dispatch=m.load(D/'DISPATCH.json')","""sources=m.load(D/'SOURCES_BEFORE.json');runtime=m.load(D/'RUNTIME_BEFORE.json');dispatch=m.load(D/'DISPATCH.json')
# Root checks proposal/source identity before invoking this script; all proposal
# files themselves are among the freshly compared full source rows below.""")
pre=once(pre,"a=m.load(dispatch['admission']['path']);assert a['environment']==runtime['environment']", "a=m.load(dispatch['admission']['path']);assert a['action']=='adapters' and a['request']==sources['inputs']['request'] and a['environment']==runtime['environment']")
pre=once(pre,"source_files=len(sources['sources']),vendor_files", "source_files=len(sources['sources']),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),prior_role_rows=len(supplement['prior_role_rows']),vendor_files")
emit('predispatch.py','predispatch.py',pre)
post=(OLD/'check_sidecars.py').read_text().replace(str(OLD),str(D)).replace("D=B/'ri200-root-sidecars-ofv27lvp'","D=B/'ri204-root-adapters-f04k2tg9'")
post=once(post,'Independent root replay of saved administrative sidecars; no subject import.','UNEXECUTED root postcheck proposal for saved adapters. No subject import; no acceptance issued.')
post=post.replace('SIDECARS','ADAPTERS').replace("action='sidecars'","action='adapters'").replace("complete['action']=='sidecars'","complete['action']=='adapters'")
post=once(post,"names={'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}\nproduced_names=['ATTEMPT.json','RESULT.json',*[k+'.json' for k in names]]","produced_names=['ATTEMPT.json','RESULT.json']")
# Genuine root evidence must retain the complete initial/terminal relationship;
# labels alone do not establish origin, which remains external root provenance.
post=once(post,"assert genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and 'session_id' not in genuine['actual_result']","""assert genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and 'session_id' not in genuine['actual_result']
if 'session_id' in genuine['initial_result']:
 terminal=m.load(D/'GENUINE_TERMINAL_ARGUMENTS.json')
 assert terminal['actual_arguments']['session_id']==genuine['initial_result']['session_id'] and terminal['actual_arguments']['chars']==''
 assert terminal['actual_result']==genuine['actual_result']
 assert terminal['original_genuine_record']==m.ref(D/'GENUINE_TOOL.json')
else:assert genuine['initial_result']==genuine['actual_result']""")
post=once(post,"profiles=m.load(sources['inputs']['profiles']['path']);normal=m.load(profiles['completions']['profile_normal']['path']);pre=m.load(normal['artifacts']['PRE']['path'])\nexpected={key:m.ref(out/(key+'.json')) for key in names};assert result==expected\nfor name,field in names.items():assert (out/(name+'.json')).read_bytes()==m.canonical(pre[field])",'''# Reconstruct every candidate field using authenticated administrative operands.
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
''')
start=post.index("summary=dict(schema='ri200-root-sidecars-review-v1'")
post=post[:start]+'''summary=dict(schema='ri204-root-adapters-postcheck-v1',status='PASS_SAVED_CANDIDATE_BINDINGS_PENDING_INDEPENDENT_ROOT_REVIEW',
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
'''
emit('check_adapters.py','check_sidecars.py',post)
with (W/'SOURCE_DIFF.patch').open('x') as f:f.write(''.join(changed))
print(json.dumps({'generated':[{'path':str(W/n),'bytes':len((W/n).read_bytes()),'sha256':hashlib.sha256((W/n).read_bytes()).hexdigest()} for n in ['prepare_adapters.py','predispatch.py','check_adapters.py','SOURCE_DIFF.patch']],'generated_source_executed':False},indent=2))
