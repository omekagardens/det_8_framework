# RI120 — complete connected-sensitivity decision, source-only contract

26 September 2026. Preparation only. No target import, AST, compilation,
runtime probe, fixture run, native arithmetic or execution admission.
The accepted RI117 reduction is conditional; this packet asks whether
both connected profiles are nonconstant at the unchanged actual baseline.

## 1. Analytic result and remaining decision

Use the accepted RI117 full-ideal formulas, not an assumed universal
record sensitivity. For eight stem records xi and sixteen chain records
eta=xi+8 sigma, write A=q(C3), B=q(C4), G=q(H5), D=q(C5), with
stem ideals S=0,1,3,7. Let c=B(15), h=G(15)=G(23), j=G(31),
e=D(15), ell=D(31), and m=h^2/c. Every denominator is positive.

    E=sum_S A(S)G(S)^3/B(S)^3+3m+3j
    V=E-m-2j
    E2=sum_S D(S)G(S)/B(S)+e*h/c+h+j+ell
    C2=sum_S A(S)G(S)^3 D(S)/B(S)^4+e*h^2/c^2
    A2=E+2E2-j,       B2=2m+2j+ell
    U3=[2,-(1+V),V], U2=[3,-A2,B2,C2]

Arrays give ascending coefficients in rho. The full profiles are
f3=1-s U3 and f2=1-s U2. Thus f3 is constant exactly when all seven
Delta V vanish. With Q2_eta=[-Delta A2,Delta B2,Delta C2], f2 is
constant at actual rho exactly when all fifteen Q2_eta(rho)=0.
Keep all eight V and sixteen connected profiles, all seven/fifteen
contrasts and all zero members; do not select a favorable pair.

The bounded analytic check preserves the actual size-five strict
mixture. In particular its C5 extra-bit contrasts cancel; the later
half-scale must not be substituted backward. Those simplifications
do not justify dropping any assigned output or evaluating a new row.
The accompanying analytic notes are proof work, not native execution.

The unchanged outer interval is (0,R], with
R=1/[2(1+max(E0,E1))]. Only these two E values define R; never replace
them by a maximum over eight records or choose actual rho. The accepted
half-scale theorem puts actual rho in that interval. Since s rho and
s rho(1-rho) are positive, the stated contrast criteria follow.

## 2. Fixed input roles and historical premise closure

Eight fixed sibling files under inputs/, in this role order:

| Role / filename | Bytes | SHA-256 |
| --- | ---: | --- |
| ri88 / ri88.json | 1828149 | ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b |
| ri111 / ri111.md | 20656 | ca07943f8d2f9d9c396b4484193dc5797900f6c7a18c5f8c2a5b8333759ccf53 |
| ri109_adjudication / ri109_adjudication.json | 4849 | 26ddd81d5fc1ae80c30d68aeadcb0ada0e18168bf3892b0995643294e6a64ddf |
| ri111_adjudication / ri111_adjudication.json | 3838 | fc4e9147db50ceb750d1f9fdcf503ffbb53363d2f1379557d1713bb844093249 |
| ri115_adjudication / ri115_adjudication.json | 6678 | a23c0ac1208c78cc28590727675869968e2f579c863857aad67a9ea08b1d2480 |
| ri117 / ri117.md | 15564 | 9726383aabb01cfa922b90f64bd572ac0a04a390111f57e722ed29d896289194 |
| ri117_connected / ri117_connected.md | 11893 | ede2d82067a4259266d61988e0897756507e06b28040d8d5bd324991aa79dad0 |
| ri117_adjudication / ri117_adjudication.json | 4617 | 862545fde8a9006dd39593c0aca7f47d6d82426dc47ffccea140e6f64957aec3 |

These files are not created/copied during preparation. Authenticate every
input and executing source before scientific JSON parsing. The executing
producer captures and rechecks its source, but its self-computed hash is
not independent authentication: the outer root caller must first bind it
to the admitted expected identity. The auditor independently enforces
that producer source pin. Preserve the
RI112 RI88 exact top-level schema, source/design pins, four dependency
hashes, actual probability-manifest/problem identities, 69-stage prefix,
positive-finite-width-bias disposition, amplitude1/4 and no-numerical-a6
historical fields. Those historical claims do not grant new admission.

Retain RI109/RI111 adjudication schemas/statuses and RI111 scope checks
exactly as the accepted predecessor source. Add:

- RI115 schema ri115-root-final-native-mathematical-adjudication-v1,
  status ACCEPT_EXACT_ZERO_MINOR_RESULT_WITH_FEASIBILITY_OPEN;
  mathematical_result_accepted=true, whole_positive_extension_established=false.
- RI117 schema ri117-root-coupled-family-adjudication-v1,
  status ACCEPT_COMPLETE_CONDITIONAL_COUPLED_REDUCTION_ONLY;
  active_execution_admission=false, fixed_28_child_repair_rejected=false,
  full_positive_repair_proved=false.

No scientific value outside the forty held rows is converted to a
rational operand. H/z, actual scale, solver and prefix replay are forbidden.
Whole-file pins authenticate unused historical fields without treating
them as numerical inputs. Outer root custody must preserve the actual
historical dependency closure and failed-attempt inventories; this target
does not replace that closure by an acceptance-looking local manifest.

## 3. Complete fixed held domain and arithmetic envelope

Shape-major order C3,C4,C5,H5, record-minor increasing:
C3=(0,1,3), records0..7, ideals0,1,3,7;
C4=(0,1,3,7), records0..7, ideals0,1,3,7,15;
C5=(0,1,3,7,15), records0..15, ideals0,1,3,7,15,31;
H5=(0,1,3,7,7), records0..7, ideals0,1,3,7,15,23,31.
Exactly forty complete rows/224 slots, no excluded held shape or record.

Every entry has exactly order,record,probabilities. Validate strict types,
literal inventories, uniqueness/order, canonical rational strings,
strict positivity and complete normalization before extraction. Require
empty-record equality within each fixed order, proper-precursor locality
within that same order/ideal for every matching r&mask pair, twin
equality G(15)=G(23), and the held whole-map identity
B(7)*G(15)=B(15)*D(7) for both C5 sigma records. Retain all full slots.
Transport is the accepted unique/twin-top and maximal-record proof,
not a new probability query or parity assumption.

Bounds unchanged: input rational32768 bits, working1048576 bits,
transient2097154 bits, counted operations200000, rational text20000
characters, input/output8MiB, active child120seconds, externally sampled
owned-group512MiB. No retry or relaxed limits. Parse no floats/NaN,
duplicate JSON keys, boolean integers or noncanonical fractions. Every
division checks nonzero. All checks survive optimized Python.

Producer uses bounded Fraction/dense polynomials/Horner evaluation.
Auditor is separately authored integer-pair/sparse polynomial arithmetic
with direct coefficient-times-power endpoints. Neither imports the
other or any scientific/prefix/helper module. Reviewed old arithmetic
may be copied with exact provenance; changed-target qualification is new.

## 4. Literal complete canonical certificate

Schema ri120-connected-sensitivity-certificate-v1. Exactly19 top-level
fields: schema,accepted_inputs,accepted_sources,inputs,stem_profiles,
connected_profiles,scale_domain,V_contrasts,Q2_contrasts,common_gcd,
decision,coverage,limitations,arithmetic_limits,checker_sha256,
root_fixtures,family_fixtures,decision_fixtures,refusal_controls.
Canonical encoding: sorted keys, compact separators, ASCII, one newline.
Saved replay requires recursive exact-type/value equality AND whole bytes.

accepted_inputs={ri88:{bytes,sha256}}. accepted_sources has the other
seven roles in section2, each {bytes,sha256}. checker_sha256 is actual
executing producer source digest, independently pinned by the auditor.

inputs has held_rows (all40 original entries), selected_order
(C3:0,...,C5:15,H5:0,...,H5:7), prefix_replayed:false,
H_or_z_values_read:false, proper_locality_checked:true,
twin_diamond_checked:true, transport_basis:
"RI117 complete connected profiles; RI111 maximal-bit and RI85 unique/twin-top transport".

stem_profiles: eight entries in xi order, fields record,E_terms (four
individual A G^3/B^3 terms),c,h,j,m,E,V,U3_padded (three).
All arithmetic entries are canonical rational strings, record an integer.

connected_profiles: sixteen entries in eta order, fields record,
stem_record (eta&7),sigma (eta>>3),e,ell,E2_terms,E2,C2_terms,C2,A2,B2,
U2_padded. E2_terms are the four D G/B terms followed by e*h/c,h,j,ell
(eight individual entries); C2_terms are four A G^3 D/B^4 followed by
e*h^2/c^2 (five). U2_padded has four entries. Do not merge duplicates.

scale_domain has R,selected_E (E0,E1 only),interval:"0<rho<=R",
lower_full_margins_at_R (two1-R*E values, both>1/2),
actual_rho_evaluated:false,amplitude:"1/4",seed_unchanged:true.

V_contrasts: seven entries record1..7, fields record,V,V0,delta_V,is_zero.
Q2_contrasts: fifteen entries record1..15, fields record,delta_A2,
delta_B2,delta_C2,Q2_padded (three),U2_difference_padded (four),
fixed_divisor:"rho",quotient_matches_closed_formula:true,degree,is_zero.
Require U2_eta-U2_0=[0]+Q2_padded; degree of zero is -1.
An independent auditor also sums RI117's14/12 individual proper-ideal
potentials to cross-check the closed coefficient formulas before reporting.

## 5. Zero-safe gcd and exact real-root decision

Apply deterministic monic Euclidean gcd to all nonzero Q2 in record
order, retaining zero members in the fifteen-member original family.
The gcd has exactly their common roots: it divides every polynomial;
the Euclidean identities express it in their generated ideal. Retain
all folds even after reaching a constant, every quotient/remainder and
reconstruction identity, and divisibility evidence for all fifteen.
Native degree cap2; no actual rho or s is evaluated.

common_gcd has branch,nonzero_records,zero_records,folds,gcd_monic,
divisibility,root_certificate,all_Q2_identically_zero. Allzero branch
is "all-zero-Q2", folds/divisibility empty, gcd/root_certificate null,
all_Q2_identically_zero:true. Otherwise branch="nonzero-gcd", false.
Fold fields retain predecessor exact names record,previous_gcd,
input_polynomial,gcd_euclidean,gcd_monic; initial previous_gcd=[] and
first euclidean trace=[] as monic normalization of the first member.
Divisibility fields: record,polynomial,quotient,remainder,
reconstructed_polynomial; zero members use empty arithmetic arrays.

Retain complete predecessor root-certificate schema and evidence:
derivative, gcd-with-derivative divisions, square-free quotient and
reconstruction, coprimality, unrescaled negative-remainder Sturm chain,
all divisions, exact endpoint values/signs/zero-omitting variations and
distinct root count. Constants have count0. The count V(0)-V(R)
excludes0 and includesR. Repeated roots are counted once; no arbitrary
negative chain rescaling. Allzero never calls this nonzero routine.

decision has exactly f2_status,f3_status,disposition,common_gcd_degree,
distinct_common_real_roots,no_common_real_root_on_admissible_interval,
restricted_28_child_repair_rejected,rational_root_decision_performed,
rational_roots_remaining_asserted,actual_scale_root_asserted,
positive_repair_asserted,all_positive_extensions_rejected,
actual_scale_computed,remaining_parent_feasibility_decided.
Statuses: f3="constant" iff all DeltaV zero, otherwise "nonconstant";
f2="constant" for allzeroQ2, "nonconstant" for nonzero gcd/count0,
"undetermined" for positive common-root count. Null degree/count only
in allzero. no_common_real_root... iff f2="nonconstant".
Both nonconstant give disposition="certified-connected-obstruction"
and restricted_28_child_repair_rejected:true. Every other case has
disposition="unresolved-connected-sensitivity" and rejection:false.
The last seven claim fields starting rational_root_decision_performed
are always false. Rational-root exclusion is NOT part of this packet.
Surviving roots are not actual rho, rational roots or a positive repair.

coverage has held_rows:40,held_probability_slots:224,stem_records:8,
connected_records:16,V_contrasts:7,Q2_contrasts:15,
H_or_z_arithmetic_values:0,new_q6_q7_rows:0,native_polynomial_degree_cap:2.
limitations has all eight true fields: real_roots_do_not_imply_rational_roots,
roots_in_outer_interval_do_not_locate_actual_scale,
complete_all_size_extension_not_claimed,QM_geometry_gravity_derivation_not_claimed,
restricted_candidate_only,external_custody_required,
remaining_parent_feasibility_not_decided,sensitivity_not_positive_repair.
arithmetic_limits retains the predecessor exact eight field names/values.

## 6. Complete synthetic branch/endpoint fixtures, not yet run

root_fixtures retains all16 source-declared RI112 root fixtures, literal
operands and expected counts, using the unchanged cubic-cap root engine.
That test-engine cap does not enlarge native Q2's degree2 domain.

family_fixtures has ten FIFTEEN-member families, padding the declared
active prefix with [] through record15. Retain input trailing zeros.
Use predecessor fields name,input_polynomials,R,expected_gcd,
expected_distinct_real_roots,common_gcd,decision,native_model_claimed:false.
Its decision uses a fixed synthetic nonconstant V family (DeltaV1=1,
others0), not native values. Active prefix/R/expected monic gcd/count:

1. all-zero: [] /1/null/null.
2. zero-plus-constant: [[],[2],[-1,1]] /1/[1]/0.
3. coprime-linears: [[-1,1],[-2,1]] /1/[1]/0.
4. common-excluded-zero: [[0,1],[0,0,1]] /1/[0,1]/0.
5. common-included-upper: [[-1,1],[-2,2]] /1/[-1,1]/1.
6. repeated-common-upper: [[1,-2,1],[2,-4,2]] /1/[1,-2,1]/1.
7. degree-drop-negative-scaling: [[-1,1,0],[2,-2]] /1/[-1,1]/1.
8. common-both-endpoints: [[0,-1,1],[0,-2,2]] /1/[0,-1,1]/1.
9. common-irrational: [[-1,-1,1],[-2,-2,2]] /2/[-1,-1,1]/1.
10. common-no-real: [[1,0,1],[2,0,2]] /1/[1,0,1]/0.

All displayed numbers serialize as canonical rational strings. Every
family member carries its fixed record label1..15 during arithmetic.

decision_fixtures are the six cross-product cases in order: Q2 family
all-zero,zero-plus-constant,common-included-upper, each paired first with
allzero V contrasts then V1=1/other0. Fields name,family_fixture,
V_deltas (seven),expected_f2_status,expected_f3_status,
expected_rejected,decision,native_model_claimed:false. Names are
familyname+"--V-constant" or familyname+"--V-nonconstant".
Only zero-plus-constant--V-nonconstant rejects. These cases enforce
that proving one sensitivity alone never becomes a native rejection.

## 7. Refusal and future invocation contract

Producer owns a literal ordered CONTROL_PAIRS inventory and matching
future-executed intended-first-refusal actions. Auditor independently
reconstructs the same declarations; it never runs producer controls.
Retain applicable parser/type/bit/degree/division/input-pin/provenance,
held-order/record/slot/locality/twin, exact saved-field/type/value/byte,
gcd zero/constant/common-root and endpoint controls from RI112.
Replace obsolete minors/pivot/C5-forbidden checks with all40-row and
7V/15Q2 inventories, native quadratic cap, full two-profile decision,
Q2 fixed-division sign, no skipped zero members and both-sensitivity
requirement. Add twin-diamond corruption and all new root-premise pins
and statuses. No native-branch assumption in a mutation: use fixed
synthetic branch fixtures for allzero/constant/surviving-root changes.
Each changed mathematical output family must have a specific mutation
whose first failure is declared. Include forbidden actual-scale,
positive-repair, rational-root and general-extension claims.

Final source review must trace each declaration to its action and each
action to its intended first reason; an unexplained count is insufficient.
The final sources must instantiate every literal ordered refusal pair and
all sixteen root fixture operand/count declarations; a document reference
alone is not executable coverage or an admissible placeholder.
Source declarations are not claims of executed fixtures or qualification.

Producer interface: --witness emits the full canonical certificate only;
no flag independently reconstructs and compares sibling CERTIFICATE.json,
then emits canonical PASS summary with schema,checker_sha256,
certificate_sha256,witness_sha256,decision,root_fixture_count,
family_fixture_count,decision_fixture_count,refusal_count,
producer_replay_is_independent_audit:false. No output files are written
by either target. All originals/source/saved bytes are protected and
rechecked before success; root's separately admitted outer caller must
perform independent failure-path custody checks even on target failure.

Auditor descriptor, independent reconstruction, complete protected
postchecks and report are fixed in AUDIT_CONTRACT.md. No descriptor,
candidate, input copy, receipt, freeze, authorization or admission is
created now. Root alone controls actual staged witness/normal/optimized/
auditor execution, fresh qualification applicability, publication and Git.
