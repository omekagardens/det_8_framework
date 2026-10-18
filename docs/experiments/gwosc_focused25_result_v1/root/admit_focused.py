"""Root exact one-operation admission after source adjudication and real PRE."""
import importlib.util,os,shlex
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri139-focused-bootstrap-repair-source-XP8iNwMw';R=m.B/'ri139-bootstrap-independent-review-VMq4RmI9'
decision=m.load(m.D/'RI139_ROOT_ADJUDICATION.json');assert decision['source_accepted'] is True and decision['execution_admitted'] is False
rec=m.load(m.D/'ROOT_SOURCE_RECONCILIATION.json')
for row in rec['observations']:assert m.identity(row['path'])==row
deps=m.load(S/'DEPENDENCIES.source-only.json');layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);cards=op/'cards';envroot=op/'environment';out=op/'output';env=layout['environment']
assert sorted(p.name for p in op.iterdir())==['cards','environment'] and not list(cards.iterdir()) and not list((envroot/'tmp').iterdir())
for sealed in deps['sealed_namespace_roots']+[str(p) for p in m.B.iterdir() if p.is_dir() and p!=op]:
 p=Path(sealed);assert op!=p and op not in p.parents and p not in op.parents
pre=m.load(m.D/'BOOTSTRAP_PRE.json');tool=m.load(m.D/'BOOTSTRAP_PRE_TOOL.json');assert tool['result']['exit_code']==0 and 'session_id' not in tool['result']
assert pre['actual_environment']==env and pre['selected_interpreter_binding']==deps['selected_bootstrap_binding']==layout['selected_interpreter_binding']
assert m.identity(pre['selected_interpreter_binding']['path'])==pre['selected_interpreter_binding']
for row in pre['bindings']:assert m.identity(row['path'])==row
preflight=m.save('BOOTSTRAP_HOST_PREFLIGHT.json',dict(schema='ri139-root-genuine-direct-bootstrap-preflight-v1',status='APPLICABLE_TO_ONE_FRESH_FOCUSED25_OPERATION',source_decision=m.ref(m.D/'RI139_ROOT_ADJUDICATION.json'),source_reconciliation=m.ref(m.D/'ROOT_SOURCE_RECONCILIATION.json'),fresh_pre=m.ref(m.D/'BOOTSTRAP_PRE.json'),genuine_pre_tool=m.ref(m.D/'BOOTSTRAP_PRE_TOOL.json'),selected_interpreter_binding=pre['selected_interpreter_binding'],actual_environment=env,trusted_premises=pre['trusted_premises'],deadline='Explicit default SIGALRM and 960-second alarm before direct Python exec; unblocked mask and Darwin scheduling premises; prior genuine benign termination retained',prior_deadline_probe=m.ref(m.B/'ri137-root-launch-adjudication-ie1m0jc_/DEADLINE_PROBE_INITIAL.json'),timeout_cleanup='Parent alarm does not kill separate child group; any timeout requires actual child identification/cleanup and rejection',genuine_actual_completion_pending=True,scientific_candidate_qualification=False))
copies=[]
for name,p in [('review.json',R/'HANDOFF.json'),('adjudication.json',m.D/'RI139_ROOT_ADJUDICATION.json'),('preflight.json',m.D/'BOOTSTRAP_HOST_PREFLIGHT.json')]:
 q=cards/name
 with q.open('xb') as f:f.write(p.read_bytes());f.flush();os.fsync(f.fileno())
 copies.append(dict(original=m.ref(p),operational=m.ref(q)));assert m.pure(copies[-1]['original'])==m.pure(copies[-1]['operational'])
ids=['F01_'+x for x in ('positive','pre_admission_read','occupied','mkdir','post_admission_read','initial_source_read','attempt_open','attempt_partial','secondary_post','secondary_source','secondary_namespace','secondary_checks','three_secondary','final_partial')]+['F02_'+x for x in ('positive','named_path','resolved_path','link_literal','link_order','link_omitted','target_bytes','target_sha','provenance_missing','snapshot_alias','snapshot_target')]
sources={name:m.pure(m.ref(Path(deps['ri135_module']['path']).parent/name)) for name in deps['ri135_source_names']}
control=dict(schema='ri135-root-fault-control-admission-v1',status='AUTHORIZE_F01_F02_NONSCIENTIFIC_CONTROLS_ONLY',sources=sources,controls=ids,output=str(out/'controls'),independent_source_review=deps['ri135_independent_review'],genuine_outer_required=True)
controlpath=cards/'controls.json'
with controlpath.open('xb') as f:f.write(m.canonical(control));f.flush();os.fsync(f.fileno())
bootstrap=pre['selected_interpreter_binding']['path'];cardpath=cards/'launcher.json';command=[bootstrap,'-I','-B',str(S/'launch_controls.source-only.py'),'--admission',str(cardpath)]
limits=dict(child_seconds=180,child_rss_kib=524288,poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,stream_bytes=67108864,file_bytes=67108864,namespace_bytes=536870912,namespace_entries=25000,parent_soft_seconds=900,genuine_outer_timeout_seconds=960)
premises=dict.fromkeys(('genuine_bootstrap_host_preflight_external','genuine_tool_completion_external','stable_supplier_host_and_no_descendants','apple_loader_and_cache_external','sampled_child_only_not_parent_or_group_quota','saved_parent_pid_not_authenticated_child_identity'),True)
card=dict(schema='ri139-root-focused-launcher-admission-v1',status='AUTHORIZE_ONLY_RI135_FOCUSED25',launcher_handoff=m.ref(S/'HANDOFF.json'),launcher_review=m.ref(cards/'review.json'),launcher_adjudication=m.ref(cards/'adjudication.json'),bootstrap_host_preflight=m.ref(cards/'preflight.json'),controls_admission=m.ref(controlpath),output=str(out),environment_root=str(envroot),launcher_command=command,child_command=[bootstrap,'-I','-B',deps['ri135_control']['path'],'--admission',str(controlpath),'--output',str(out/'controls')],environment=env,limits=limits,external_premises=premises)
with cardpath.open('xb') as f:f.write(m.canonical(card));f.flush();os.fsync(f.fileno())
outer=['/usr/bin/env','-i']+[k+'='+v for k,v in env.items()]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+command
invocation=dict(cmd='exec '+shlex.join(outer),workdir=str(op),login=False,yield_time_ms=1000,max_output_tokens=3000)
print(m.save('ROOT_DISPATCH.json',dict(schema='ri139-genuine-root-single-operation-admission-v1',status='AUTHORIZE_EXACT_SINGLE_FOCUSED25_EXECUTION',authority='Ongoing user-authorized independent review implementation; root actual source/preflight adjudication in this thread',operation=str(op),tool='exec_command',invocation=invocation,source_adjudication=m.ref(m.D/'RI139_ROOT_ADJUDICATION.json'),preflight=preflight,copies=copies,cards=[m.ref(p) for p in sorted(cards.iterdir())],control_count=25,prior_attempt_remains_rejected=True,new_source_new_operation=True,retry_authorized=False,actual_completion_at_admission=False)))
print(invocation)
