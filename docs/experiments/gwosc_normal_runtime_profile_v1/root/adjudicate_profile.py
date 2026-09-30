"""Root accepts one genuine normal profile after complete independent review."""
import importlib.util,tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
R=m.B/'ri148-independent-normal-review-fbnud7fq';P=m.B/'ri146-root-current-capture-9bfi4u8s'
m.verify(R/'HANDOFF.json',dict(bytes=6852,sha256='dda8890bc60be37f1391c88972eb11a67d4e52d68fa860ca01a92042e1c6c276'))
h=m.load(R/'HANDOFF.json');v=m.load(R/'VERDICT.json')
assert h['status']==v['status']=='ACCEPT_BOUNDED_NORMAL_PROFILE_EVIDENCE' and v['blocking_findings']==[]
assert len(h['files'])==16 and sorted(p.name for p in R.iterdir())==sorted(h['exact_namespace'])
for r in h['files']:m.verify(r['path'],r)
assert m.ref(R/'INDEPENDENT_NORMAL_REVIEW.md')==m.load(m.D/'ROOT_REVIEW_READ.json')['narrative']
report=m.load(R/'SAVED_NORMAL_CHECKS.json');assert report['status']=='PASS' and len(report['predicates'])==46449
for row in report['read_inputs']:m.verify(row['path'],row)
for row in m.load(R/'FINAL_INPUT_CUSTODY.json')['additional_read_inputs']:m.verify(row['path'],row)
for row in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
for row in m.load(m.D/'OPERATION_FINAL_IDENTITIES.json')['identities']:assert m.identity(row['path'])==row
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);out=op/'output';card=m.load(op/'NORMAL_ADMISSION.json')
checks=m.load(out/'CHECKS.json');rebuilt=m.load(R/'RECONSTRUCTED_PROFILE_CHECK.json');assert checks['profile']==rebuilt
decision=m.save('RI148_ROOT_ACTUAL_ADJUDICATION.json',dict(schema='ri148-root-normal-profile-adjudication-v1',status='ACCEPT_GENUINE_NORMAL_RUNTIME_PROFILE',independent_review=m.ref(R/'HANDOFF.json'),independent_verdict=m.ref(R/'VERDICT.json'),independent_reconstruction=m.ref(R/'RECONSTRUCTED_PROFILE_CHECK.json'),root_read_scope=m.ref(m.D/'ROOT_REVIEW_READ.json'),root_actual_check=m.ref(m.D/'ROOT_PROFILE_CHECK.json'),root_check_tool=m.ref(m.D/'ROOT_CHECK_TOOL.json'),genuine_outer=m.ref(m.D/'GENUINE_OUTER.json'),genuine_tool=m.ref(m.D/'GENUINE_TOOL_COMPLETE.json'),accepted_baseline=m.ref(P/'BASELINE_ACCEPTANCE.json'),
 actual=dict(initial_chunk='24c0ff',session=50493,terminal_chunk='9ddbb4',exit_code=0,independent_check='d8ab59 exit0',independent_seal='67f558 exit0',modules=71,descriptor_fields=213,full_runtime_bindings=113,observer_main=1,sentinels=99,absent_cache_fields=0,ordered_dyld_attempts=10,monitor_samples=121,baseline_snapshots_byte_equal=True),
 limits=v['limits'],timing=v['timing'],preserved_reviewer_failures=h['preserved_failed_reviewer_attempts'],scientific_qualification=False,actual_data_admission=False,full32_qualified=False,next_optimized_admission_created=False,
 reading_diagnostic='331237 displayed the real handoff but two guessed ancillary filenames were absent; correct VERDICT/PUBLICATION_SUBSET and complete summary/commands were read in ec4708. No source or actual result changed.',ret_paused=True))
print(decision)
normal=dict(schema='ri133-root-preparation-stage-review-v1',status='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage='normal',sources=card['sources'],packet=card['packet'],environment_root=card['environment_root'],completions={'profile_normal':m.ref(out/'COMPLETE.json')},genuine_outer={'profile_normal':m.ref(m.D/'GENUINE_OUTER.json')},independent_review=m.ref(R/'HANDOFF.json'),scientific_execution=False)
assert len(normal)==10
print(m.save('NORMAL_ACCEPTANCE.json',normal))
nextdir=Path(tempfile.mkdtemp(prefix='ri150-root-optimized-profile-',dir=m.B))
print(m.save('MEASUREMENT_NEXT_ACTION.json',dict(schema='ri150-root-optimized-profile-assignment-v1',status='RESERVED_NEXT_PHASE_NOT_OPERATIONAL_ADMISSION',owner='root',reservation=str(nextdir),predecessor=decision,normal_acceptance=m.ref(m.D/'NORMAL_ACCEPTANCE.json'),baseline_acceptance=m.ref(P/'BASELINE_ACCEPTANCE.json'),environment_root=card['environment_root'],source_packet=str(m.B/'ri141-white-bootstrap-source-h58ls076'),
 next='Fresh full source/supplier/host checks, one separate profile_optimized card and exclusive output in same environment. PRE/POST equal accepted complete baseline. Unchanged observer-I-B-O under30seconds; independent full report and both-mode relation review before profiles acceptance. Different optimized cache descriptors are retained, not forced to whole-report byte equality. Both-mode acceptance precedes65guards,WHITE/full32 and public-data reproduction.',operational_admission_created=False,scientific_credit=False,ret_paused=True)))
