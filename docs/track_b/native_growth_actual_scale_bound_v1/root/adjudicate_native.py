"""Root adjudication after manual proof and complete nonauthor review."""
import importlib.util,tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
Q=m.B/'ri147-native-scale-membership-q4lxbpke';R=m.B/'ri147-independent-scale-review-5qddsve3'
m.verify(R/'HANDOFF.json',dict(bytes=5529,sha256='1d99faefe8ad0934898b9521b2ba5d7c62707833b55051599d46343b9db8afb3'))
h=m.load(R/'HANDOFF.json');assert h['recommendation']=='ACCEPT_EXACT_CONDITIONAL_ANALYTIC_INCREMENT_WITH_ACTUAL_COEFFICIENT_GAP' and not h['repair_findings']
assert sorted(p.name for p in R.iterdir())==sorted(h['namespace']) and len(h['payloads'])==6
for r in h['payloads']:m.verify(r['path'],r)
assert h['subject_handoff']==m.ref(Q/'HANDOFF.json')
for r in m.load(Q/'HANDOFF.json')['payloads']:m.verify(r['path'],r)
for r in m.load(m.D/'ROOT_NATIVE_CHECK.json')['identities']:assert m.identity(r['path'])==r
decision=m.save('RI147_ROOT_ADJUDICATION.json',dict(schema='ri147-root-native-analytic-adjudication-v1',status=h['recommendation'],source_handoff=m.ref(Q/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),root_manual_review=m.ref(m.D/'ROOT_MANUAL_REVIEW.json'),root_metadata_check=m.ref(m.D/'ROOT_NATIVE_CHECK.json'),
 actual_checks=dict(root_initial_seal='ce266b exit0',root_closure='647ce5 exit0',independent_closure='b5dc04 exit0',independent_final_seal='844e7b exit0'),
 accepted=['Actual singleton-component factorization and intrinsic root-mark separation without coefficient ordering','Complete signed v/D3 and q/D3 relations, zero-safe singleton factor and signed-part floor','Complete H5 variance decomposition: M5>1,theta<1/144,j>71/72','All five selected six-parent proper sums; M6>71/24 and actual rho<12/95, stronger held capZ','Monotone reference sums and sharper conditional two-endpoint weighted envelope; positive-denominator actual canonical contrast threshold'],
 remaining_actual_premise=h['remaining_actual_premise'],actual_rho_in_delta0_proved=False,actual_W_C2_C3_signs_decided=False,full_H30_decided=False,scientific_execution=False,preserved=h['preserved'],ret_paused=True))
print(decision)
nextdir=Path(tempfile.mkdtemp(prefix='ri149-singleton-hook-incidence-',dir=m.B))
print(m.save('NATIVE_SUCCESSOR_RESERVATION.json',dict(schema='ri149-native-singleton-hook-assignment-v1',status='ASSIGNED_ANALYTIC_PROOF_ONLY_AFTER_RI147_ADJUDICATION',owner_thread='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',reservation=str(nextdir),predecessor=decision,
 question='Derive the complete intrinsic incidence reduction for the two actual C5 singleton-hook components with terminal(5,1). Retain both maximal-deletion parent shapes, all inherited/newborn mark transport and any further marked subdivisions. Derive their symbolic contributions to every incident complete row cap and history-weighted objective. Use the actual canonical primary/lexicographic constraints to prove a justified exchange or dual-face inequality for delta_kappa, or isolate precisely which fixed face/other-coordinate relation still prevents RI147 synthesis equation5 and its joint sensitivity budget. Do not assume ordering from component index or neutrality. Preserve all other coordinates and complete canonical tie-break constraints; no free-coefficient countermodel.',
 permitted='Manual analytic proof and literal accepted source/premise reading; bounded fresh administrative identity/reference checks. No actual coefficient/maximum/scale/H/z evaluation, scientific-body decoding, engine, subject/helper import/compile/AST/probe/run, global graph enumeration, controller/runtime inventory/card/admission, repository/index/Git or predecessor mutation.',
 expected='A complete symbolic incidence/optimization comparison or precise actual canonical-face blocker, sealed with checks and premise closure for nonauthor review. Do not repeat only the existing small-x or rho cap theorem.',preserved=h['preserved'],measurement='Separate root RI148 normal profile review active',ret_paused=True)))
