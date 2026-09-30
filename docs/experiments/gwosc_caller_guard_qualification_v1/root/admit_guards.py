"""Root's separate admission of exactly the unchanged65 nonscientific guards."""
import importlib.util
import os
import sys
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
prior=m.B/'ri150-root-optimized-profile-0ydjxad3';base=m.B/'ri146-root-current-capture-9bfi4u8s';S=m.B/'ri141-white-bootstrap-source-h58ls076';G=m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
# This decision is produced only after root reads and adjudicates the sealed
# fresh nonauthor source review. It is not inferred from an author packet.
decision=m.load(m.D/'PREFLIGHT_ROOT_ADJUDICATION.json')
assert decision['status']=='ACCEPT_UNCHANGED_SOURCE_FOR_ONE_65_GUARD_PHASE'
for row in decision['review_objects']:m.verify(row['path'],row)
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);pre=m.load(m.D/'BOOTSTRAP_PRE.json')
assert m.load(m.D/'BOOTSTRAP_PRE_TOOL.json')['result']['exit_code']==0
assert pre['actual_environment']==layout['environment']
assert pre['selected_interpreter_binding']==layout['selected_interpreter_binding']==m.identity(layout['selected_interpreter_binding']['path'])
assert pre['host']==list(os.uname())
assert not list((Path(layout['environment_root'])/'tmp').iterdir()) and not list(op.iterdir())
for row in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
helpers=('control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py')
ids=([side+'_'+kind for side in ('parent','worker') for kind in ('source','caller','runtime_acceptance','mode','late','late_postcheck')]
 +['capture_'+x for x in ('positive','changed_copy','buffer_drift','occupied')]
 +['monitor_'+x for x in ('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap')]
 +['runtime_'+x for x in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config')])
ids+=(['static_'+x for x in ('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command')]
 +['acceptance_'+x for x in ('positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile')]
 +['mode_'+x for x in ('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift')]
 +['relation_'+x for x in ('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped')])
assert len(ids)==len(set(ids))==65 and ids==decision['control_order']
review=m.ref(m.D/'PREFLIGHT_ROOT_ADJUDICATION.json')
guard=dict(schema='ri130-root-guard-admission-v1',status='AUTHORIZE_RI130_NONSCIENTIFIC_CALLER_GUARDS_ONLY',packet=str(G),harness=m.pure(m.ref(G/'guard_controls.source-only.py')),helpers={n:m.pure(m.ref(G/n)) for n in helpers},controls=ids,output=str(op/'output/GUARD_REPORT.json'),source_review=review,genuine_outer_required=True)
guardref=m.save(op/'CALLER_GUARD_ADMISSION.json',guard)
card=m.load(m.B/'ri150-genuine-optimized-profile-eb4vq_ba/OPTIMIZED_ADMISSION.json')
card.update(phase='guards',source_review=review,output=str(op/'output'),environment_root=layout['environment_root'],bootstrap_host_preflight=m.ref(m.D/'BOOTSTRAP_PRE.json'),host=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist')),baseline_acceptance=m.ref(base/'BASELINE_ACCEPTANCE.json'),normal_acceptance=None,profiles_acceptance=m.ref(prior/'PROFILES_ACCEPTANCE.json'),guard_admission=guardref)
assert len(card)==17 and card['sources']=={n:m.pure(m.ref(S/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')}
print(guardref);print(m.save(op/'GUARDS_ADMISSION.json',card))
print(m.save('ADMISSION_CUSTODY.json',dict(card=m.identity(op/'GUARDS_ADMISSION.json'),guard_card=m.identity(op/'CALLER_GUARD_ADMISSION.json'),source_review=m.identity(m.D/'PREFLIGHT_ROOT_ADJUDICATION.json'),source_pre=m.ref(m.D/'SOURCE_PRE.json'),operation=str(op),genuine_operation_count=1)))
