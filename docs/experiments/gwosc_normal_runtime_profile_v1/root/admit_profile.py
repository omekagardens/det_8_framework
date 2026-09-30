"""Root admission for one normal profile, after fresh source/vendor checks."""
import importlib.util,os
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
prior=m.B/'ri146-root-current-capture-9bfi4u8s';S=m.B/'ri141-white-bootstrap-source-h58ls076'
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);pre=m.load(m.D/'BOOTSTRAP_PRE.json')
assert m.load(m.D/'BOOTSTRAP_PRE_TOOL.json')['result']['exit_code']==0
assert pre['actual_environment']==layout['environment']
assert pre['selected_interpreter_binding']==layout['selected_interpreter_binding']==m.identity(layout['selected_interpreter_binding']['path'])
assert not list((Path(layout['environment_root'])/'tmp').iterdir()) and not list(op.iterdir())
for row in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
review=m.save('PROFILE_SOURCE_ADJUDICATION.json',dict(schema='ri148-root-normal-profile-source-adjudication-v1',status='ACCEPT_UNCHANGED_SOURCE_FOR_ONE_NORMAL_PROFILE',
 source_handoff=m.ref(S/'HANDOFF.json'),independent_source_review=m.ref(m.B/'ri141-bootstrap-independent-review-k5bss5xp/HANDOFF.json'),prior_root_source_decision=m.ref(m.B/'ri140-root-source-adjudication-8796wh9l/RI141_ROOT_ADJUDICATION.json'),
 accepted_capture=m.ref(prior/'RI146_ROOT_ACTUAL_ADJUDICATION.json'),baseline_acceptance=m.ref(prior/'BASELINE_ACCEPTANCE.json'),
 fresh_source_check=m.ref(m.D/'SOURCE_PRE.json'),fresh_vendor_pre=m.ref(m.D/'BOOTSTRAP_PRE.json'),genuine_vendor_pre=m.ref(m.D/'BOOTSTRAP_PRE_TOOL.json'),
 source_review_scope='Previously accepted unchanged full preparation and profile-observer source. Root reread exact authentication, predecessor acceptance, normal profile validation and production ordering. Same candidate runtime baseline and environment. Fresh PRE must equal accepted complete baseline before profile child.',
 admitted_scope='One unchanged RI141 parent, PRE/POST metadata children and one 30-second normal installed-runtime profile. No optimized profile, guards, scientific target or actual data.',
 residual_premises=['Trusted stable supplier, cache-selection and host; no full import trace','Sampled child RSS/output/gap limits; genuine parent alarm is not a process-tree quota','Independent complete actual review before normal acceptance; any failed admission and partial output retained'],ret_paused=True))
card=m.load(m.B/'ri146-genuine-current-capture-heib6de2/CAPTURE_ADMISSION.json')
card.update(phase='profile_normal',source_review=review,output=str(op/'output'),environment_root=layout['environment_root'],bootstrap_host_preflight=m.ref(m.D/'BOOTSTRAP_PRE.json'),host=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist')),baseline_acceptance=m.ref(prior/'BASELINE_ACCEPTANCE.json'))
assert len(card)==17 and all(card[k] is None for k in ['normal_acceptance','profiles_acceptance','guard_admission'])
assert card['sources']=={n:m.pure(m.ref(S/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')}
print(review);print(m.save(op/'NORMAL_ADMISSION.json',card))
print(m.save('ADMISSION_CUSTODY.json',dict(card=m.identity(op/'NORMAL_ADMISSION.json'),source_review=m.identity(m.D/'PROFILE_SOURCE_ADJUDICATION.json'),source_pre=m.ref(m.D/'SOURCE_PRE.json'),operation=str(op),genuine_operation_count=1)))
