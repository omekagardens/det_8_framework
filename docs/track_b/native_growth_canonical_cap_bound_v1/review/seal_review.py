"""Seal this independent manual review; administrative custody only."""
import hashlib
import importlib.util
import json
from pathlib import Path

R = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-independent-cap-review-wt1tl1ip')
Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-correlated-capacity-proof-tusjyk77')
A = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-root-review-jco7p6tf/NATIVE_REVIEW_ASSIGNMENT.json')
HELPER = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
b = HELPER.read_bytes()
if len(b) != 3144 or hashlib.sha256(b).hexdigest() != 'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':
    raise ValueError('trusted metadata helper pin')
spec = importlib.util.spec_from_file_location('ri157_seal_metadata', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D = R
names = ['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_PROOF_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(x.name for x in R.iterdir()) != names:
    raise ValueError('review preseal namespace differs')
report = m.load(R/'METADATA_CHECK.json')
if m.pure(m.identity(R/'METADATA_CHECK.json')) != {'bytes':3070932,'sha256':'c342bdd15842ed987200f645ea9551a9b75fd077b4d9039708fd1695472c34c1'}:
    raise ValueError('review check report differs')
for original in report['observed_identities']:
    if m.identity(original['path']) != original:
        raise ValueError('selected source drift: ' + original['path'])
if len(report['observed_identities']) != 234:
    raise ValueError('observation coverage differs')
h = m.load(Q/'HANDOFF.json')
if sorted(x.name for x in Q.iterdir()) != sorted(h['namespace']) or len(h['namespace']) != 10:
    raise ValueError('subject namespace drift')
for p in h['payloads']:
    m.verify(p['path'], p)
if m.load(R/'VERDICT.json')['repairs_required'] != []:
    raise ValueError('narrative/verdict disagreement')
review_payloads = [m.ref(R/n) for n in names]
final_ref = m.save('FINAL_PIN_CHECK.json', dict(schema='ri157-independent-final-pin-check-v1', status='MATCH_NO_SCIENTIFIC_EXECUTION',
 source_count=234, source_observations=m.ref(R/'METADATA_CHECK.json'), subject=m.ref(Q/'HANDOFF.json'), assignment=m.ref(A),
 subject_namespace=h['namespace'], subject_payload_count=9, fresh_full_source_state_equal=True, reviewer_preseal_payloads=review_payloads,
 trusted_helper=m.ref(HELPER), historical_state_compared_to_current=False))
all_names = sorted(names + ['FINAL_PIN_CHECK.json','HANDOFF.json'])
payloads = [m.ref(R/n) for n in all_names if n != 'HANDOFF.json']
sealed = m.save('HANDOFF.json', dict(schema='ri157-independent-review-handoff-v1',status='SEALED_SOURCE_REVIEW_FOR_ROOT_ADJUDICATION',
 recommendation='ACCEPT_ACTUAL_CANONICAL_CAP_AND_SIGNED_CONTRAST_BOUNDS_WITH_CAPACITY_GAP',
 reservation=str(R), subject=m.ref(Q/'HANDOFF.json'), assignment=m.ref(A), namespace=all_names, payloads=payloads,
 compact_publication_subset=[n for n in all_names if n != 'METADATA_CHECK.json'], external_only_diagnostics=[m.ref(R/'METADATA_CHECK.json')],
 independence='Nonauthor of RI157; prior native review and separately accepted RI149 O01 authorship disclosed; earlier WHITE/caller/bootstrap authorship is unrelated and inherited only.',
 actual_check=dict(chunk='8dcf5b',exit_code=0,predicates=15407,dependencies=223,selected_bytes=9791698,inherited=193,additions=30,administrative_bodies=77,historical_typed_refs=1616,current_typed_refs=89,historical_extended_identities=17,counterparts=4,literal_refs=6,fresh_identity_rechecks=234),
 final_pin_check=final_ref, repairs_required=[],
 accepted_increment=['Actual F_i<35743/12100<71/24<E_0,E_1 and retained Mcap=max E, Z=R.','Complete marked row bounds, signed disjunction and0<v<1147/9092160.','Necessary pass conditions lambda<1147/15370080 and D_minus>213d7; equivalent8733 component comparison.'],
 retained_gaps=['Actual capacity sign and marked separation/lambda magnitude.','Global M6/rho identification; actual small-scale criterion.','Global final-vector grid is unaccepted, implication conditional only.','Adequate q/v budget, W/C2/C3 and shared H30.'],
 preserved=dict(RET='paused',measurement='separate',P2_P3=True,numerical_Y='1/4',focused=31,policy=139,native_deeper=20,audit_deeper=42,other_eight_parents=True,five_Di=True,shared_T1=True,strict_endpoints=True,ideal_multiplicities=True),
 subject_execution=False,scientific_body_decode_or_evaluation=False,engine_or_global_enumeration=False,runtime_card_or_admission=False,repository_or_Git_write=False,physical_claim=False,
 root_owns_adjudication_admission_successor_Git_publication=True, no_successor_assigned=True, immutable_after_seal=True))
for p in payloads:
    m.verify(p['path'], p)
if sorted(x.name for x in R.iterdir()) != all_names:
    raise ValueError('review final namespace differs')
print(json.dumps(dict(status='SEALED',handoff=sealed,namespace_count=len(all_names),payload_count=len(payloads),fresh_source_identity_count=234,subject_execution=False), sort_keys=True))
