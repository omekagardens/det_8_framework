"""Root one-operation administrative admission; does not load preparation source."""
import importlib.util, os
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
B=m.B;S=B/'ri141-white-bootstrap-source-h58ls076';P=B/'ri143-root-feasibility-review-b9bt7rgh'
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);pre=m.load(m.D/'BOOTSTRAP_PRE.json')
assert m.load(m.D/'BOOTSTRAP_PRE_TOOL.json')['result']['exit_code']==0
assert pre['actual_environment']==layout['environment']
assert pre['selected_interpreter_binding']==layout['selected_interpreter_binding']==m.identity(layout['selected_interpreter_binding']['path'])
assert not list((op/'environment/tmp').iterdir()) and not (op/'output').exists()
for row in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
decision=dict(schema='ri146-root-capture-source-adjudication-v1',status='ACCEPT_EXACT_SOURCE_FOR_ONE_NONSCIENTIFIC_CAPTURE',
 source_handoff=m.ref(S/'HANDOFF.json'),independent_source_review=m.ref(B/'ri141-bootstrap-independent-review-k5bss5xp/HANDOFF.json'),
 prior_root_source_decision=m.ref(B/'ri140-root-source-adjudication-8796wh9l/RI141_ROOT_ADJUDICATION.json'),
 fresh_source_check=m.ref(m.D/'SOURCE_PRE.json'),fresh_vendor_pre=m.ref(m.D/'BOOTSTRAP_PRE.json'),genuine_vendor_pre=m.ref(m.D/'BOOTSTRAP_PRE_TOOL.json'),
 focused15_actual_acceptance=m.ref(P/'RI144_ROOT_ACTUAL_ADJUDICATION.json'),review_annotation_correction=m.ref(P/'ROOT_ACTUAL_REVIEW_CORRECTION.json'),
 focused25_inheritance='Explicitly retain accepted RI139 outcomes only for unchanged RI141 F01/F02 source paths under disclosed doubles. No new25 execution or real-bootstrap credit.',
 actual15_scope='Selected-bootstrap isolated controls, including authentic six-field direct supplier provenance; production startup/real metadata capture must now be observed.',
 admitted_scope='One capture parent and its PRE/POST metadata children using unchanged RI141 source, exact historical candidate runtime and fixed limits. No candidate interpreter, profile, guard, scientific target or data execution.',
 residual_premises=['Stable supplier and host; Apple loader/shared cache and source/cache distinction','Genuine root tool origin and parent-only external alarm; identify and reap any surviving owned group on outer failure','Sampled child RSS/output/gaps, not hard process-tree quotas; reviewed no-descendant bootstrap','Independent complete saved actual review precedes baseline acceptance'],ret_paused=True)
review=m.save('CAPTURE_SOURCE_ADJUDICATION.json',decision)
sel=layout['selected_interpreter_binding']
card=dict(schema='ri141-root-preparation-admission-v1',status='AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION',phase='capture',
 sources={n:m.pure(m.ref(S/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')},source_review=review,
 packet=str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg'),output=str(op/'output'),environment_root=str(op/'environment'),
 bootstrap=dict(named_path=sel['path'],resolved_path=sel['resolved_path'],symlink_chain=sel['symlink_chain'],target=m.pure(sel)),
 bootstrap_host_preflight=m.ref(m.D/'BOOTSTRAP_PRE.json'),host=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist')),
 baseline_acceptance=None,normal_acceptance=None,profiles_acceptance=None,guard_admission=None,
 bounds=dict(snapshot_seconds=180,profile_seconds=30,guard_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,file_bytes=67108864,driver_soft_seconds=900,genuine_outer_timeout_seconds=960),genuine_outer_required=True)
print(review);print(m.save(op/'CAPTURE_ADMISSION.json',card))
print(m.save('ADMISSION_CUSTODY.json',dict(card=m.identity(op/'CAPTURE_ADMISSION.json'),source_review=m.identity(m.D/'CAPTURE_SOURCE_ADJUDICATION.json'),source_pre=m.ref(m.D/'SOURCE_PRE.json'),operation=str(op),genuine_operation_count=1)))
