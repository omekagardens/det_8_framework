# RI112 — exact all-record one-column rank decision

Implementation specification, 26 September 2026. No execution,
scientific operand decoding, coefficient evaluation, fixture run, runtime
probe, import/compilation or active admission is authorized by this file.
Producer uses Fraction/list polynomials; auditor uses normalized integer
pairs/sparse polynomials and direct power endpoints. Neither imports the
other, a prefix/checker, a solver, or a scientific runtime helper.

## Accepted operands and source pins

Producer inputs are fixed sibling paths beneath its executing source directory:

- inputs/ri88.json: 1828149 bytes,
  ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b.
- inputs/ri111.md: 20656 bytes,
  ca07943f8d2f9d9c396b4484193dc5797900f6c7a18c5f8c2a5b8333759ccf53.
- inputs/ri109_adjudication.json: 4849 bytes,
  26ddd81d5fc1ae80c30d68aeadcb0ada0e18168bf3892b0995643294e6a64ddf.
- inputs/ri111_adjudication.json: 3838 bytes,
  fc4e9147db50ceb750d1f9fdcf503ffbb53363d2f1379557d1713bb844093249.

Roles in this order: ri88, ri111, ri109_adjudication, ri111_adjudication.
These input files are NOT created during source preparation. Root may
later copy and bind actual input custody after source acceptance.
Producer source may retain old --witness versus saved replay modes:
witness stdout only; replay compares complete canonical CERTIFICATE.json
next to its source. All input/source/saved bytes must be rechecked before
emitting success. External owned-group supervision and admission remain
root prerequisites. No new supervisor or caller is assigned here.

Verify every fixed input pin before decoding scientific JSON. At future
execution parse only the selected24 rows into rational operands; all other
scientific values remain unused/unconverted. Pin validation and designated
root-adjudication metadata checks precede scientific reconstruction.
Root-adjudication schemas/statuses must match their actual records:
ri109-root-final-mathematical-adjudication-v1 /
ACCEPT_INDEPENDENT_RESTRICTED_27_CHILD_REPAIR_OBSTRUCTION;
ri111-root-analytic-adjudication-v1 /
ACCEPT_CONDITIONAL_COMPLETE_28_CHILD_REDUCTION_ONLY.
Require the RI111 historical fields actual_28_child_feasibility="UNRESOLVED",
new_native_coefficients_or_scales_evaluated=false and
new_numerical_execution_admitted=false. They describe that accepted analytic
sitting; they are not claims about, or authority for, a later RI112 run.
Their identities, not invented acceptance-equivalent JSON, are authoritative
incoming premises. They do not authorize this future execution.

## Arithmetic/input envelope

Preserve predecessor bounds: input rational bits32768, working bits1048576,
transient integer bits2097154, counted operations200000, rational text20000
characters, input/output8MiB, active-child120seconds, sampled owned-group
512MiB external cap. No automatic retries or budget relaxation.
Exact rational strings are reduced, canonical and finite. Reject booleans
where actual integers are required, decimal/nonfinite JSON and duplicate
keys. Every division has an explicit nonzero divisor.

Use exactly C3=(0,1,3), C4=(0,1,3,7), H5=(0,1,3,7,7).
Selected order is shape-major, record-minor, each record0 through7.
Individual ideal masks are respectively:
(0,1,3,7); (0,1,3,7,15); (0,1,3,7,15,23,31).
All24 complete rows /128 slots must be retained in certificate inputs.
Preserve existing RI88 source/dependency/prefix/admission/40-row224-slot
provenance checks. Selected rows must be unique and in exact order.
Do not convert C5 probabilities or any H/z values.

Require positive normalized complete selected rows. Require empty-birth
equality across all8 records for each shape. Require every selected proper
precursor's probabilities agree for records with equal bits inside that
precursor (compare r & mask): this is a fixed domain closure, not additional
record erasure. Require both H5 one-top slots15 and23 equal for each record.
Cap marks are represented as zero solely through accepted unique/twin-top
and maximal-record transport; include that stated provenance. Do not create
off-domain probability queries or validate by replaying the prefix.

## Complete canonical certificate

Schema ri112-one-column-rank-certificate-v1. Exact top-level fields (19):

schema, accepted_inputs, accepted_sources, inputs, selected_parent, records,
scale_domain, reference_contrasts, pivot_root_certificate, minors,
common_gcd, decision, coverage, limitations, arithmetic_limits,
checker_sha256, fixtures, gcd_fixtures, refusal_controls.

Canonical JSON is sorted keys, compact separators, ASCII, one terminal
newline; no floats/NaN. Full typed equality and whole-byte equality are
required for saved replay and independent reconstruction.

accepted_inputs = {ri88:{bytes,sha256}}.
accepted_sources has ri111,ri109_adjudication,ri111_adjudication, each
{bytes,sha256}. No producer self-certification of execution custody.

inputs has:
held_rows (24 exact selected RI88 entries);
selected_order (C3:0,...,C3:7,C4:0,...,H5:7);
prefix_replayed:false; H_or_z_values_read:false;
transport_basis:"RI111 maximal-bit and RI85 unique/twin-top transport";
proper_locality_checked:true.
selected_parent = [0,1,3,7,7,7,7].

records has8 entries in record order0..7. Retain predecessor record evidence:
record,E_terms (four),E_one_cap_total,E_two_cap_total,E,v_star,K_terms(four),
K,c,h,j,U_padded(five rational strings). Add p=K_terms[3] as a rational
string and p_is_core_K_term:true; independently derive the same core
expression a^3*g^6/b^8. Here v_star is RI111's nu, not correction v1.
E=sum A*G^3/B^3+3h^2/c+3j; K=sum A^3*G^6/B^8.
U=[4,-4E,6j,4v_star,K]. No coefficient is evaluated in preparation.

scale_domain keeps predecessor fields:
R,selected_E (ONLY E0,E1),interval:"0<rho<=R",
lower_full_margins_at_R (ONLY two values1-R*E0,1-R*E1),
actual_rho_evaluated:false,amplitude:"1/4",seed_unchanged:true.
R=1/[2(1+max(E0,E1))], unchanged from accepted RI109.
Do NOT replace this with max over8 records or impose its two margins on
records2..7. Actual s, beta, Gamma and parent feasibility are not computed.

reference_contrasts has7 entries, record1..7. Exact fields:
record,delta_p,delta_E,delta_j,delta_v_star,delta_K,
P_padded(four),U_minus_reference_padded(five),fixed_divisor:"rho",
quotient_matches_closed_formula:true,degree,is_zero.
Difference means record minus0. P=[-4DeltaE,6Deltaj,4Deltav,DeltaK].
Independently verify U_r-U_0=[0]+P. Degree of the zero polynomial is -1.
Only pivot record1 must have nonzero delta_j and nonzero P.
Other contrasts may be zero; never divide by Delta_p.

pivot_root_certificate is a complete inherited root certificate of P1 at R,
independently reconstructed by both programs using the unchanged rational
polynomial/Sturm engines. Require its distinct real root count0, consistent
with the accepted fixed-input RI109 premise. A mismatch refuses; it does
not silently weaken the pivot theorem or change baseline.

minors has6 entries, record2..7, with exact fields:
record,delta_p,pivot_delta_p,left_padded,right_padded,M_padded,
raw_U_combination_padded,fixed_divisor:"rho",
quotient_matches_closed_formula:true,degree,is_zero.
left = Delta_r p * P1; right = Delta_1 p * P_r; M=left-right.
All padded polynomial arrays have4 entries except raw_U_combination has5:
Delta_r p*(U1-U0)-Delta_1 p*(Ur-U0)=[0]+M.
Each minor is retained, including zero minors. No degree may exceed3.

## Common gcd and root evidence

For a nonzero family, its monic gcd has exactly the common roots of the
six minors: divisibility makes every gcd root a root of every minor, and
the Euclidean identities express the gcd as a rational-polynomial linear
combination of the nonzero minors, giving the converse. Zero members add
no restriction. Square-free reduction preserves this root set. Thus zero
distinct roots on (0,R] is a necessary-rank obstruction, not a numerical
choice of rho or a positive-feasibility result. The all-zero family must
remain separate because every scale then passes only this rank condition.

common_gcd exact fields:
branch,nonzero_records,zero_records,folds,gcd_monic,divisibility,
root_certificate,all_minors_identically_zero.

Each family input is exactly6 labeled cubic-or-lower polynomials in fixed
record order2..7. Retain nonzero/zero record lists in this same order.

All zero:
branch="all-zero-minors"; nonzero_records=[]; zero_records=[2,...,7];
folds=[]; gcd_monic=null; divisibility=[]; root_certificate=null;
all_minors_identically_zero=true. Do not invoke a nonzero-gcd/root routine.

Otherwise branch="nonzero-gcd"; all_minors_identically_zero=false.
Start with the first nonzero minor. Its first fold uses previous_gcd=[],
input_polynomial=that minor, gcd_euclidean=[] and its exact monic result
obtained by the inherited euclidean(input,[]) routine. Subsequent folds
take previous monic gcd and the next nonzero minor in order; do not omit
later folds merely because gcd became constant.
Each fold fields: record,previous_gcd,input_polynomial,gcd_euclidean,gcd_monic.
Retain every quotient/remainder division and degree-drop/reconstruction
identity from the inherited routine. Its cubic step bound suffices.
gcd_monic is the final exact monic polynomial, nonzero.

divisibility has all6 entries, even zero minors:
record,polynomial,quotient,remainder,reconstructed_polynomial.
Divide each minor by final gcd; require zero remainder and reconstruction.
Zero minor quotient/remainder/reconstruction are empty arrays.

root_certificate is the complete inherited square-free/Sturm evidence for
the final gcd at unchanged R, including constant gcd cases. Keep exact
derivative, gcd-with-derivative trace, square-free quotient/remainder and
reconstruction, square-free coprimality trace, unrescaled negative-remainder
Sturm chain, all division witnesses, endpoint rational values/signs/
zero-omitting variations and distinct root count. Count is V(0)-V(R),
which excludes0 and includesR with the inherited square-free conventions.
No repeated-root count is double-counted; no arbitrary chain normalization.
The root certificate field names are identical to the accepted predecessor.

decision exact fields:
disposition,common_gcd_degree,distinct_common_real_roots,
rank_condition_identically_true,no_common_real_root_on_admissible_interval,
restricted_28_child_repair_rejected,rational_root_decision_performed,
rational_roots_remaining_asserted,actual_scale_root_asserted,
positive_repair_asserted,all_positive_extensions_rejected,
actual_scale_computed,remaining_parent_feasibility_decided.

All-zero disposition="unresolved-identically-zero-minors", gcd degree/count
null, rank_condition_identically_true=true; no exclusion/rejection.
Otherwise degree is actual gcd degree0..3, count0..3, rank-condition
identically true=false. Count0 gives disposition="certified-rank-obstruction",
both no_common_real_root... and restricted_28... true. Positive count gives
"unresolved-common-real-roots" with both false. The final seven assertion
fields (starting rational_root_decision_performed) are always false.
A real survivor does not locate actual rho, prove rationality or positivity,
or decide the other parent systems. Only this fixed support may be rejected.

coverage = {held_rows:24,held_probability_slots:128,records:8,
reference_contrasts:7,rank_minors:6,H_or_z_arithmetic_values:0,
new_q6_q7_rows:0,native_polynomial_degree_cap:3}.
limitations keeps predecessor flags, adds
remaining_parent_feasibility_not_decided:true and
rank_compatibility_not_positive_repair:true.
arithmetic_limits retains exact predecessor key names/values.
checker_sha256 is observed producer source hash, independently pinned by
auditor after producer source stabilizes.

## Source-defined synthetic cases (NOT RUN IN PREPARATION)

Retain all16 accepted root fixtures and their exact coefficient/radius/
expected-count declarations. Each fixture output:
name,expected_distinct_real_roots,root_certificate,native_model_claimed:false.
No native decision is attached to synthetic root fixtures.

Add ten synthetic SIX-minor families. Listed active prefix polynomials are
padded with empty zero polynomials to exactly6 members. Coefficients are
ascending canonical rational strings; radius and expected gcd/count follow.

1. all-zero: prefix[]; R1; expected gcd null, count null.
2. zero-plus-constant: [[],["2"],["-1","1"]]; R1; gcd["1"], count0.
3. coprime-linears: [["-1","1"],["-2","1"]]; R1; gcd["1"], count0.
4. common-excluded-zero: [["0","1"],["0","0","1"]]; R1;
   gcd["0","1"], count0.
5. common-included-upper: [["-1","1"],["-2","2"]]; R1;
   gcd["-1","1"], count1.
6. repeated-common-upper: [["1","-2","1"],["-1","3","-3","1"]]; R1;
   gcd["1","-2","1"], count1.
7. degree-drop-negative-scaling: [["-1","1","0","0"],["2","-2"]]; R1;
   gcd["-1","1"], count1.
8. common-both-endpoints: [["0","-1","1"],["0","-2","2"]]; R1;
   gcd["0","-1","1"], count1.
9. common-irrational: [["-1","-1","1"],["-2","-2","2"]]; R2;
   gcd["-1","-1","1"], count1.
10. common-no-real: [["1","0","1"],["2","0","2"]]; R1;
    gcd["1","0","1"], count0.

Each gcd_fixtures entry fields:
name,input_polynomials (all6 declared arrays INCLUDING trailing zeros),
R,expected_gcd,expected_distinct_real_roots,common_gcd,decision,
native_model_claimed:false. Shared common-gcd function trims arithmetic
polynomials; expected declared operands are retained separately.
All-zero expected degree/root certificate is null, not a fictitious gcd.

## Intended producer refusal inventory

The producer defines one explicit ordered list of (name,reason) declarations
and matching source-defined refusal actions. The independent auditor retains
the same declarations without importing or executing producer code. Retain old parser/type/bit/degree/provenance/lookup/
saved-canonical controls with adapted record8 and24-row boundaries.
Add fixed input pins for all four roles; complete proper-locality checks;
missing/duplicate/reordered minor labels; wrong core p, sign and cross-factor;
zero-member omission; nonmonic/wrong gcd/fold/divisibility; all-zero fictitious
gcd; forged constant and surviving-root outcomes; positive-feasibility,
actual-scale or broader-rejection flags. Mutations must differ for every
possible unknown native branch. Branch-specific mutations target named
synthetic families, not assumptions about native results. Do not compute
controls now. Auditor reconstructs declaration names/reasons from its own
source constants, not from producer claims; declaration is not execution.
Consumer independent input/failure guards also need an intended refusal
inventory in the final contract, not a claimed executed campaign.

## Independent auditor descriptor/custody interface

Keep the predecessor six-key descriptor shape:
schema,phase,files,accepted_sources,audit_source,custody_dependencies.
schema="ri112-independent-audit-input-v1";
phase="fixed_saved_certificate_audit".

files roles: ri88,ri111,ri109_adjudication,ri111_adjudication,candidate (5).
accepted_sources roles:
ri111,ri109_adjudication,ri111_adjudication,checker,protocol,contract (6).
audit_source: actual executing auditor source (1).
custody_dependencies retain the exact ordered five roles:
producer_witness_stdout,producer_witness_custody,producer_normal_custody,
producer_optimized_custody,consumer_source_review.

Every entry has exactly path,bytes,sha256; custody entries add role.
Only the three proof/adjudication files may alias across files/sources,
with exact identical entries. Thus17 role bindings/14 distinct payload
paths/15 postchecks including the separate descriptor. No other alias.
All paths literal canonical absolute, symlink-free regular files, positive
actual integer sizes<=8MiB, canonical lower-case hashes. Candidate and
genuine witness stdout are distinct paths with equal complete bytes.
Pin all known source/input identities. Producer/protocol/contract source
pins will be filled after stabilization, before final source review.
No active descriptor/candidate/source acceptance is created here.

Preserve accepted auditor custody mechanics: capture actual own source before
descriptor parsing; all file/source/custody pins before scientific parsing;
independent postchecks even on failure; own source and descriptor protected;
canonical full-body equality against independently reconstructed certificate;
bounded emergency failure evidence, no suppressed late failure. Update
explicit counts from14 old postchecks to15 and every corresponding failure
coverage bound. Do not trust producer scientific flags. Retained custody
bodies are pinned, not self-adjudicated: future root caller must bind actual
accepted custody and genuine outer completion. Fresh audit-source/applicability
and concrete execution admission remain external, not a worker assertion.

Auditor final report retains whole reconstructed certificate, all19 section
hashes, exact role identities/17 bindings/14 payload paths/15 successful
postchecks, producer control declarations explicitly not consumer-executed,
16 independently rebuilt root fixtures plus10 gcd fixtures, and claim limits.
CLI remains DESCRIPTOR BYTES SHA256 with -I -S -B; no scientific imports.
Use new RI112 report/failure schemas and no inherited27-child rejection label.

## Source review and handoff

No Python parsing/AST/import/compilation, fixture or target execution during
preparation. Static source text comparison, literal metadata hashing and
complete manual independent source reviews only. The final packet includes
this IMPLEMENTATION.md, AUDIT_CONTRACT.md, source/provenance metadata and
a stable handoff after both implementations agree. Root owns review acceptance,
source publication, all input/candidate copies and all actual admissions.
