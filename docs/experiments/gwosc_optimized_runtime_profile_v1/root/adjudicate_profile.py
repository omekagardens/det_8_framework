"""Root bounded optimized/both-mode acceptance after independent actual review."""
import importlib.util,tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
R=m.B/'ri150-independent-optimized-review-zlcd4ret';N=m.B/'ri148-root-normal-profile-qfvdi_75';B=m.B/'ri146-root-current-capture-9bfi4u8s'
m.verify(R/'HANDOFF.json',dict(bytes=6593,sha256='fab678fdf26173fdd952e2e3aab9fce54fee092d298c8f756c5120cb99d0719f'))
h=m.load(R/'HANDOFF.json');v=m.load(R/'VERDICT.json')
assert h['status']==v['status']=='ACCEPT_BOUNDED_OPTIMIZED_AND_BOTH_MODE_PROFILE_EVIDENCE' and v['blocking_findings']==[]
assert len(h['files'])==17 and sorted(p.name for p in R.iterdir())==sorted(h['exact_namespace'])
for r in h['files']:m.verify(r['path'],r)
assert m.ref(R/'INDEPENDENT_OPTIMIZED_REVIEW.md')==m.load(m.D/'ROOT_REVIEW_READ.json')['narrative']
report=m.load(R/'SAVED_OPTIMIZED_CHECKS.json');assert report['status']=='PASS' and len(report['predicates'])==48024 and len(report['read_inputs'])==580
for r in report['read_inputs']:m.verify(r['path'],r)
for r in m.load(R/'FINAL_INPUT_CUSTODY.json')['additional_input_pins']:m.verify(r['path'],r)
for r in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(r['path'])==r
for r in m.load(m.D/'OPERATION_FINAL_IDENTITIES.json')['identities']:assert m.identity(r['path'])==r
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);out=op/'output';card=m.load(op/'OPTIMIZED_ADMISSION.json')
assert m.load(out/'CHECKS.json')['profile']==m.load(R/'RECONSTRUCTED_PROFILE_CHECK.json')
mode=m.load(R/'BOTH_MODE_RELATION.json')
assert all(mode[k] is True for k in ['adjusted_expected_runtime_equal','complete_ordered_dyld_attempts_equal','hash_algorithm_names_equal'])
assert mode['whole_report_byte_equality_required'] is False
assert mode['normal_descriptors']==m.load(m.B/'ri148-independent-normal-review-fbnud7fq/RECONSTRUCTED_PROFILE_CHECK.json')['all_descriptors']
decision=m.save('RI150_ROOT_ACTUAL_ADJUDICATION.json',dict(schema='ri150-root-optimized-both-mode-adjudication-v1',status='ACCEPT_GENUINE_OPTIMIZED_AND_BOTH_MODE_PROFILES',independent_review=m.ref(R/'HANDOFF.json'),independent_verdict=m.ref(R/'VERDICT.json'),independent_reconstruction=m.ref(R/'RECONSTRUCTED_PROFILE_CHECK.json'),both_mode_relation=m.ref(R/'BOTH_MODE_RELATION.json'),root_read_scope=m.ref(m.D/'ROOT_REVIEW_READ.json'),root_actual_check=m.ref(m.D/'ROOT_PROFILE_CHECK.json'),root_check_tool=m.ref(m.D/'ROOT_CHECK_TOOL.json'),genuine_outer=m.ref(m.D/'GENUINE_OUTER.json'),genuine_tool=m.ref(m.D/'GENUINE_TOOL_COMPLETE.json'),genuine_call_details=m.ref(m.D/'GENUINE_TOOL_CALL_DETAILS.json'),accepted_baseline=m.ref(B/'BASELINE_ACCEPTANCE.json'),accepted_normal=m.ref(N/'NORMAL_ACCEPTANCE.json'),actual=dict(initial_chunk='ed392e',session=91856,terminal_chunk='8b8828',exit_code=0,independent_check='5d796f exit0',independent_seal='e035fc exit0',counts=v['counts'],baseline_snapshots_byte_equal=True),limits=v['remaining_premises'],timing=v['timing'],resource_interpretation=v['resource_interpretation'],preserved_adaptation_failure=h['preserved_adaptation_failure'],scientific_qualification=False,actual_data_admission=False,full32_qualified=False,guards_executed=False,next_guard_admission_created=False,ret_paused=True))
print(decision)
normal=m.load(N/'NORMAL_ACCEPTANCE.json')
profiles=dict(schema='ri133-root-preparation-stage-review-v1',status='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage='profiles',sources=card['sources'],packet=card['packet'],environment_root=card['environment_root'],completions=dict(profile_normal=normal['completions']['profile_normal'],profile_optimized=m.ref(out/'COMPLETE.json')),genuine_outer=dict(profile_normal=normal['genuine_outer']['profile_normal'],profile_optimized=m.ref(m.D/'GENUINE_OUTER.json')),independent_review=m.ref(R/'HANDOFF.json'),scientific_execution=False)
assert len(profiles)==10
print(m.save('PROFILES_ACCEPTANCE.json',profiles))
nextdir=Path(tempfile.mkdtemp(prefix='ri152-root-guard-qualification-',dir=m.B))
print(m.save('MEASUREMENT_NEXT_ACTION.json',dict(schema='ri152-root-guard-qualification-assignment-v1',status='RESERVED_NEXT_PHASE_NOT_OPERATIONAL_ADMISSION',owner='root',reservation=str(nextdir),predecessor=decision,profiles_acceptance=m.ref(m.D/'PROFILES_ACCEPTANCE.json'),baseline_acceptance=m.ref(B/'BASELINE_ACCEPTANCE.json'),environment_root=card['environment_root'],source_packet=str(m.B/'ri141-white-bootstrap-source-h58ls076'),guard_packet=card['packet'],next='Fresh complete source/supplier/host preflight, separate root65-guard card with exact original harness and all seven helpers, one separately admitted guards phase in same environment with prospective full PRE/POST and unchanged bounds. Independently review complete outcomes and actual custody before any runtime acceptance or later WHITE15/two179/full32/public-data stage. Guard doubles remain nonscientific control evidence.',operational_admission_created=False,scientific_credit=False,ret_paused=True)))
