"""Root administrative admission: no target/launcher import, compilation or execution."""
import importlib.util, os, shlex, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri137-focused-control-launcher-source-nykv2tsg'; R=m.B/'ri137-launcher-independent-review-5q_931ea'
pins={S/'HANDOFF.json':(4642,'95112c29b0448f7f48810fb34d9510b6d7b6079826054383795758e3f70b2cbd'), R/'HANDOFF.json':(3396,'ca1a29eec2d789f474b9dad13d09f433d12713bb8ccef0de70fe3de47d961009')}
observations=[]
for p,(n,h) in pins.items():
 observations.append(m.verify(p,dict(bytes=n,sha256=h)))
 handoff=m.load(p);assert sorted(x.name for x in p.parent.iterdir())==sorted(['HANDOFF.json']+[Path(x['path']).name for x in handoff['files']])
 for row in handoff['files']:observations.append(m.verify(row['path'],row))
deps=m.load(S/'DEPENDENCIES.source-only.json')
for row in deps['opaque_files']:observations.append(m.verify(row['path'],row))
assert len(deps['opaque_files'])==276
sourcecheck=m.save('ROOT_PRE_ADMISSION_SOURCE_CHECK.json',dict(schema='ri137-root-opaque-pre-admission-v1',source=m.ref(S/'HANDOFF.json'),review=m.ref(R/'HANDOFF.json'),observations=observations,source_names=6,review_names=7,dependencies=276,target_execution=False))
review='''# RI137 root adjudication and actual focused-control admission

Root accepts the exact six-file RI137 source packet after the fresh independent nonauthor review and root reading of the complete 373-line launcher, full protocol, review, and retained RI135 repair/monitor context. Root independently reconciles the seven-file sealed review, six-file source and all 276 opaque dependencies before issuing cards. The source decision is ACCEPT_EXACT_UNEXECUTED_FOCUSED25_LAUNCHER; it does not report tests as executed.

The wrapper authenticates complete source captures before the single unchanged child_run call. Preownership refusals do not create output. Every fallible owned operation lies inside the protected body; all five late groups are attempted independently, while failures inside a group may stop that group. All 25 complete control envelopes, fixed first errors/counters, historical binding mutations and both retained namespaces are checked. Source/authentication doubles inside the controls are explicit; no current scientific runtime or data is tested. Failed final writes cannot manufacture missing inner evidence and must remain unaccepted partial attempts.

The actual source review supports one genuine externally admitted execution of the existing 25 controls, using the reviewed 180-second child monitor, 512 MiB sampled child RSS ceiling, 25 ms polling, 100 ms maximum sample gap and 50 ms ps timeout. No thresholds change. The 900-second soft parent bound is complemented by the exact outer Perl alarm/exec prefix at 960 seconds. Root's genuine benign one-second alarm/exec trial ended with tool exit 142 (SIGALRM); it ran sleep, not the launcher. The literal prefix resets SIGALRM to its default disposition. An applicable unblocked signal mask, stable host and Darwin delivery remain premises; this is not a hard real-time guarantee. The timer starts in Perl before Python replacement and does not cover earlier env/Perl startup. It does not kill the child's separate process group: a timeout requires actual surviving-child identification and cleanup and cannot be accepted as complete custody.

Root's external PRE collector observed the selected Apple Xcode Python 3.9 executable, whole installed framework namespace, loader/module file descriptors, absence points, fixed vendor command bindings and host. That collector uses trusted root tools and Apple vendor Python; it does not bootstrap its own authenticity, establish source/cache equivalence, inventory the Homebrew scientific candidate or trace all kernel/shared-cache instructions. Darwin kernel/Apple loader/cache and stable supplier are explicit trusted premises. POST uses the identical collector to compare all applicable preobservations. Root will retain actual tool completion and review the control artifacts separately before any result acceptance.

Only the exact fresh operation/card/environment and source bytes bound by ROOT_DISPATCH are admitted. Cards are issued after this adjudication, with exact-byte operational copies of the genuine review/adjudication/preflight documents. Their origin is the tool-mediated root/independent review in this thread, not the contents of PASS labels. No retry, current candidate qualification, preparation profile, 65 guard campaign, WHITE fixture, native scientific evaluation, physical claim or RET resumption is authorized here.

Primary deadline sources: https://perldoc.perl.org/functions/exec ; https://perldoc.perl.org/functions/alarm ; https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/execve.2.html .
'''
with (m.D/'ROOT_SOURCE_REVIEW.md').open('x') as f:f.write(review)
decision=m.save('RI137_ROOT_ADJUDICATION.json',dict(schema='ri137-root-source-adjudication-v1',status='ACCEPT_EXACT_UNEXECUTED_FOCUSED25_LAUNCHER',source=m.ref(S/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),root_review=m.ref(m.D/'ROOT_SOURCE_REVIEW.md'),opaque_check=sourcecheck,source_accepted=True,actual_control_results_accepted=False,controls_executed_at_decision=0,source_decision_alone_admits_execution=False))
pre=m.load(m.D/'BOOTSTRAP_PRE.json');assert len(pre['framework_namespace'])==2004
probe=m.load(m.D/'DEADLINE_PROBE_INITIAL.json');assert probe['result']['exit_code']==142 and 'session_id' not in probe['result']
for row in pre['bindings']:assert m.identity(row['path'])==row
preflight=m.save('BOOTSTRAP_HOST_PREFLIGHT.json',dict(schema='ri137-root-genuine-external-bootstrap-preflight-v1',status='APPLICABLE_FOR_ONE_FOCUSED25_VENDOR_BOOTSTRAP_RUN',pre=m.ref(m.D/'BOOTSTRAP_PRE.json'),deadline_probe=m.ref(m.D/'DEADLINE_PROBE_INITIAL.json'),source_decision=decision,source_check=sourcecheck,root_review=m.ref(m.D/'ROOT_SOURCE_REVIEW.md'),trusted_premises=pre['trusted_premises'],signal_premise='SIGALRM default explicitly restored; unblocked mask applicable from same genuine tool context; benign termination observed',genuine_tool_completion_pending=True,current_scientific_candidate_qualified=False))
op=Path(tempfile.mkdtemp(prefix='ri137-focused25-run-',dir=m.B));cards=op/'cards';cards.mkdir();envroot=op/'environment';envroot.mkdir();(envroot/'tmp').mkdir();out=op/'output'
for sealed in deps['sealed_namespace_roots']+[str(p) for p in m.B.iterdir() if p.is_dir() and p!=op]:
 p=Path(sealed);assert op!=p and op not in p.parents and p not in op.parents
copies=[]
for name,p in [('review.json',R/'HANDOFF.json'),('adjudication.json',m.D/'RI137_ROOT_ADJUDICATION.json'),('preflight.json',m.D/'BOOTSTRAP_HOST_PREFLIGHT.json')]:
 q=cards/name
 with q.open('xb') as f:f.write(p.read_bytes());f.flush();os.fsync(f.fileno())
 assert m.pure(m.ref(q))==m.pure(m.ref(p));copies.append(dict(original=m.ref(p),operational=m.ref(q)))
ids=['F01_'+x for x in ('positive','pre_admission_read','occupied','mkdir','post_admission_read','initial_source_read','attempt_open','attempt_partial','secondary_post','secondary_source','secondary_namespace','secondary_checks','three_secondary','final_partial')]+['F02_'+x for x in ('positive','named_path','resolved_path','link_literal','link_order','link_omitted','target_bytes','target_sha','provenance_missing','snapshot_alias','snapshot_target')]
sources={name:m.pure(m.ref(Path(deps['ri135_module']['path']).parent/name)) for name in deps['ri135_source_names']}
control=dict(schema='ri135-root-fault-control-admission-v1',status='AUTHORIZE_F01_F02_NONSCIENTIFIC_CONTROLS_ONLY',sources=sources,controls=ids,output=str(out/'controls'),independent_source_review=deps['ri135_independent_review'],genuine_outer_required=True)
controlpath=cards/'controls.json';controlpath.write_bytes(m.canonical(control))
env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(envroot/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
cardpath=cards/'launcher.json';command=['/usr/bin/python3','-I','-B',str(S/'launch_controls.source-only.py'),'--admission',str(cardpath)]
limits=dict(child_seconds=180,child_rss_kib=524288,poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,stream_bytes=67108864,file_bytes=67108864,namespace_bytes=536870912,namespace_entries=25000,parent_soft_seconds=900,genuine_outer_timeout_seconds=960)
premises=dict.fromkeys(('genuine_bootstrap_host_preflight_external','genuine_tool_completion_external','stable_supplier_host_and_no_descendants','apple_loader_and_cache_external','sampled_child_only_not_parent_or_group_quota','saved_parent_pid_not_authenticated_child_identity'),True)
card=dict(schema='ri137-root-focused-launcher-admission-v1',status='AUTHORIZE_ONLY_RI135_FOCUSED25',launcher_handoff=m.ref(S/'HANDOFF.json'),launcher_review=m.ref(cards/'review.json'),launcher_adjudication=m.ref(cards/'adjudication.json'),bootstrap_host_preflight=m.ref(cards/'preflight.json'),controls_admission=m.ref(controlpath),output=str(out),environment_root=str(envroot),launcher_command=command,child_command=['/usr/bin/python3','-I','-B',deps['ri135_control']['path'],'--admission',str(controlpath),'--output',str(out/'controls')],environment=env,limits=limits,external_premises=premises)
cardpath.write_bytes(m.canonical(card))
outer=['/usr/bin/env','-i']+[k+'='+v for k,v in env.items()]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+command
invocation=dict(cmd='exec '+shlex.join(outer),workdir=str(op),login=False,yield_time_ms=1000,max_output_tokens=3000)
dispatch=m.save('ROOT_DISPATCH.json',dict(schema='ri137-genuine-root-single-operation-admission-v1',status='AUTHORIZE_EXACT_SINGLE_FOCUSED25_EXECUTION',root_authority='Ongoing user-authorized DET independent-review implementation and root adjudication in this thread',operation=str(op),tool='exec_command',invocation=invocation,source_adjudication=decision,preflight=preflight,source_check=sourcecheck,copies=copies,cards=[m.ref(p) for p in sorted(cards.iterdir())],control_count=25,control_scope='2 positive and 23 declared refusal constructions with explicit doubles',retry_authorized=False,actual_execution_or_completion_at_admission=False))
print(dispatch);print(invocation)
