"""Root acceptance of independently reviewed saved metadata, not a new execution."""
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
D=m.D;A=m.B/'ri146-independent-capture-review-i7o8n5j_';op=Path(m.load(D/'OPERATION_LAYOUT.json')['operation'])
m.verify(A/'FINAL_HANDOFF.json',dict(bytes=6372,sha256='74af846af4c7dd7869da1813f1cec7be521962db13418a960e8ff9b9e24d25ad'))
h=m.load(A/'FINAL_HANDOFF.json');assert h['status']=='ACCEPT_BOUNDED_CURRENT_METADATA_CAPTURE'
assert sorted(x.name for x in A.iterdir())==h['exact_current_namespace']
for row in h['files']:m.verify(row['path'],row)
v=m.load(A/'VERDICT.json');assert v['blocking_findings']==[] and v['source_author_independent']
log=m.load(A/'SAVED_CAPTURE_CHECKS.json');assert log['status']=='PASS' and log['checks_passed']==103901
for row in log['read_inputs']:m.verify(row['path'],row)
for row in m.load(D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
for row in m.load(D/'OPERATION_FINAL_IDENTITIES.json')['identities']:assert m.identity(row['path'])==row
expected=m.load(D/'OPERATION_FINAL_IDENTITIES.json')['entries']
assert sorted(x.relative_to(op).as_posix() for x in op.rglob('*'))==sorted(x['relative'] for x in expected)
completion=op/'output/COMPLETE.json';c=m.load(completion);outer=m.load(D/'GENUINE_OUTER.json')
assert len(c)==17 and len(outer)==8 and outer['completion']==m.ref(completion)
assert outer['command']==c['command'] and outer['environment']==c['environment']
assert m.load(D/'GENUINE_TOOL_COMPLETE.json')['terminal']['exit_code']==0
err=m.load(A/'WORDING_ERRATUM.json');assert err['numeric_results_or_acceptance_changed'] is False and len(err['corrections'])==2
result=dict(schema='ri146-root-actual-capture-adjudication-v1',status='ACCEPT_GENUINE_CURRENT_METADATA_CAPTURE',
 independent_actual_review=m.ref(A/'FINAL_HANDOFF.json'),original_review_seal=m.ref(A/'HANDOFF.json'),binding_erratum=m.ref(A/'WORDING_ERRATUM.json'),full_findings=m.ref(A/'INDEPENDENT_CAPTURE_REVIEW.md'),independent_summary=m.ref(A/'SAVED_CHECK_SUMMARY.json'),
 independent_check_tool=dict(chunk_id='08a999',exit_code=0),root_actual_check=m.ref(D/'ROOT_CAPTURE_CHECK.json'),root_check_tool=dict(initial='f9ac19',session=25396,terminal='9be99c',exit_code=0),
 root_review='Read complete independent findings, structured verdict, all actual command records, complete input-custody record, summary and binding erratum. Root separately reconstructed full monitors/output, fresh9923 opaque file/selection identities,471source states and4609 historical device-only changes. Reauthenticated every saved reviewer input and all14review files and current complete operation. Numerical subject replay was neither needed nor run.',
 genuine_outer=m.ref(D/'GENUINE_OUTER.json'),genuine_arguments=m.ref(D/'GENUINE_TOOL_ARGUMENTS.json'),completion=m.ref(completion),
 metadata_baseline_only=True,historical_selection=m.ref(D/'ROOT_SELECTION_HISTORY_CHECK.json'),
 historical_device_difference='4609 records differ only in device number. Exact historical runtime byte/domain/binding equality and fresh selection stability passed the existing contract; no whole historical-selection equality or relaxed acceptance is claimed.',
 timer_scope='Owned-child times include child startup/authentication. Parent internal timer excludes preownership authentication and final COMPLETE construction/write; genuine outer deadline/terminal covers both.',
 remaining=['Separate normal30-second profile and independent acceptance, then optimized and review','Separate65guards and WHITE15/full32 qualifications','Conventional public GWOSC reproduction; physical calibration and native forward map','Supplier/host, Apple loader/cache, source/cache distinction, finite sampled-child resource and genuine tool-origin premises'],
 scientific_runtime_or_data_credit=False,ret_paused=True,reviewer_metadata_predicates_not_tests=103901,blocking_findings=[])
print(m.save('RI146_ROOT_ACTUAL_ADJUDICATION.json',result))
card=m.load(op/'CAPTURE_ADMISSION.json')
baseline=dict(schema='ri133-root-preparation-stage-review-v1',status='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage='baseline',sources=card['sources'],packet=card['packet'],environment_root=card['environment_root'],completions={'capture':m.ref(completion)},genuine_outer={'capture':m.ref(D/'GENUINE_OUTER.json')},independent_review=m.ref(A/'FINAL_HANDOFF.json'),scientific_execution=False)
print(m.save('BASELINE_ACCEPTANCE.json',baseline))
nextdir=Path(tempfile.mkdtemp(prefix='ri148-root-normal-profile-',dir=m.B))
print(m.save('MEASUREMENT_NEXT_ACTION.json',dict(schema='ri148-root-normal-profile-assignment-v1',status='ACTIVE_ROOT_PREPARATION_NOT_OPERATIONAL_ADMISSION',owner='root',reservation=str(nextdir),predecessor=m.ref(D/'RI146_ROOT_ACTUAL_ADJUDICATION.json'),baseline=m.ref(D/'BASELINE_ACCEPTANCE.json'),environment_root=card['environment_root'],source_packet=str(m.B/'ri141-white-bootstrap-source-h58ls076'),next='Fresh whole source/supplier/host checks, one separate genuine profile_normal admission, both current snapshots equal accepted baseline,30-second profile and independent full saved actual review. No optimized or65 admission before predecessor acceptance.',operational_admission_created=False,scientific_credit=False,ret_paused=True)))
print(m.save('FINAL_REVIEW_RECONCILIATION.json',dict(status='PASS',review_files=14,reviewer_inputs=len(log['read_inputs']),source_states=471,operation_entries=len(expected),original_seal_preserved=True,erratum_binding=True,subject_rerun=False)))
