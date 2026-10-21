# Binding a complete probability envelope to its scientific target

21 October 2026. Prospective admission-interface design only; no validator,
endpoint producer or scientific certificate is supplied. **ABSTAIN / NOT RUN.**
The [exact envelope component](ENVELOPE_IMPLEMENTATION.md) proves a conditional
arithmetic statement from supplied bounds. This design specifies the additional
binding and review needed before a future consumer could use those bounds as a
proxy-error premise. It changes neither [D4-A](WIDTH_DIAGNOSTIC.md) nor the
[optional approximate protocol](APPROXIMATE_WIDTH_DIAGNOSTIC.md).

## 1. The exact row being bound

The current instance is D4-A's fresh six-element parent P*=C3 ordinal-sum A3,
with all old record bits zero. Fix labels `(c0,c1,c2,a0,a1,a2)`, relations
`c0<c1<c2<aj` for each j, and no order between distinct caps. Freeze the
parent embedding used by the width channel; six vertices alone do not identify
this parent. The mathematical score remains width(new order)-3.

The complete ideal list is empty, the first one and first two chain elements,
then C3 union every subset of the three caps. Encode membership with bit
positions in the label order above. Its increasing integer masks are

    0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63.

For each mask, list newborn bits 0 then 1. There are **11 ideals and 22 distinct
ideal/bit outcomes**, even when the observation ignores the bit or several
ideals yield isomorphic unmarked children. The eight cap-subset ideals alone
omit three prefix ideals. The different parent C4 ordinal-sum A2 has eight
ideals and sixteen ideal/bit outcomes; it cannot be substituted here. In
general completeness is derived from the declared parent, not a blanket count.

For the frozen original baseline B at lambda=1 and original normalized harmonic
z, z1=1, epsilon=1/4, the target probabilities are

    P_B(I,b) = q_B(P*,0,I)/2,
    P_Q(I,b) = q_B(P*,0,I) h7([P*+I])/2.

The law definition, original normalization/parent scale, harmonic-vector
identity, scalar-passive sector, marking and h7 definition are fixed exactly
as in D4-A. Naming a different seed, normalization, sector, parent, supported
child subset or conditional law is a different target. No numerical values
for the missing native row or harmonic coefficients are supplied here.

## 2. Proposed closed input contract

A future `d4a-full-row-envelope-v1` descriptor would use the fields below. It
would be a prospective local data contract, not a security credential. Two
arm descriptors must join one frozen comparison record.

| Field | Required content and binding |
| --- | --- |
| `schema` and `comparison_ref` | Exact schema version and reviewed frozen comparison artifact; protocol choice and pre-held-out selection are explicit. Unknown schema/fields or duplicate keys are rejected. |
| `target` | Arm B or Q; canonical labelled parent and order; all-zero old marking; complete fair-bit/scalar-passive sector; fixed law/normalization, lambda, epsilon and original z identity; parent/channel embedding. Bind each reference to exact local bytes and the relevant mathematical claim, not just a filename. |
| `outcome_dictionary` | The ordered 22 `(ideal_mask,newborn_bit)` pairs above. Define labels, mask orientation and bit convention. A consumer regenerates ideals from the fixed order and compares the complete sequence, not merely its length or distinctness. |
| `endpoints` | Exactly one entry per ordered pair, with lower/upper reduced integer pairs `[n,d]`, d>0, at most 256 bits per integer, and 0<=lower<=upper<=1. These bound the complete **joint ideal/bit** probability above, not ideal-only mass, conditional mass, class-aggregated mass or empirical frequencies. |
| `coverage` | Deterministic enclosure proof or statistical simultaneous-coverage claim, its exact target and conditioning/selection scope, and any justified certificate-failure allowance. Endpoint arithmetic precision is separate from coverage semantics. |
| `evidence` and `review` | Producer method/version; endpoint derivation, including outward-rounding justification if relevant; exact referenced artifacts and claims; premises and their discharge; independent review disposition tied to this target, outcome dictionary and endpoint array. Unavailable evidence remains missing. |
| `budgets` | Predeclared exact per-arm proxy allowance, envelope precision/storage limits, categorical bit width/rounding allowance, and references to the chosen protocol's separate bit/channel/effect/certificate/failure and total-cost bounds. Both arms must share the frozen comparison. |

Each integer is exact; no floating parser, implicit conversion, tolerance,
clipping or renormalization is permitted. Schema strings and arrays must fit
the implementation's bounded input profile; a future parser also needs a
predeclared finite byte/depth limit. Canonical masks make the row ordering
unambiguous. Different labels require a separately explicit, reviewed mapping;
this version does not guess an isomorphism or silently reorder rows.

Do not drop a slot because a bound or proxy weight is zero. D4-A's target row
is positive, so an upper bound of zero contradicts that target; retain the
entry and report the contradiction. A lower bound of zero by itself is not a
contradiction. This distinguishes completeness from an invented positive lower
bound or from the generic component's ability to represent zero probabilities.

## 3. Machine checks and the limits of those checks

Given a reviewed descriptor, a future bounded consumer can check the following
without obtaining native coefficients:

1. Parse the closed schema and resource profile; reject malformed or ambiguous
   values. Match target fields and exact artifact bytes to the approved local
   comparison record. Recompute the fixed order's ideals and all newborn-bit
   pairs, and require the exact ordered list with no duplicates or omissions.
2. Check rational ranges, original-box feasibility and the target's known
   support constraints. As an additional fair-bit consistency test, for each
   ideal let `L_I=max(l_I0,l_I1)` and `U_I=min(u_I0,u_I1)`. Require L_I<=U_I
   and `2 sum L_I <= 1 <= 2 sum U_I`. This tests existence of a normalized row
   having the required equal bit masses. It does not prove the actual row is
   that row, and does not replace or silently tighten the stored endpoints.
3. Check that the evidence/review records name these exact targets, all 22
   joint-probability coordinates, endpoint bytes and selected coverage mode.
   Check the declared coverage-risk accounting and budget inequalities exactly
   where numeric values are available. Missing run-only effect, bit/channel or
   availability inputs remain explicit operational blockers; they do not prevent
   completing this bounded endpoint-binding review.
4. Only after the required endpoint review is accepted, pass the exact arrays in that
   order to the envelope API, with the explicit proxy budget and resource
   limits. Recompute the complete certificate; do not trust a manually
   assembled dataclass. Accept only its conditional-certificate disposition,
   and check the resulting weights against the pinned categorical-map consumer.
   Preserve the original arrays and resulting exact witnesses together.

The fair-bit test is necessary and sufficient for *some* compatible normalized
row: select p_I in [L_I,U_I] summing to 1/2 and put both bit masses equal to
p_I. Such a selection exists by the interval-sum criterion, using affine
interpolation if the total interval width is positive, or the singleton case
otherwise. This is a consistency check, not a native endpoint certificate.

A digest or successful replay of rational arithmetic establishes byte identity
or arithmetic agreement only. It does not prove that endpoints enclose the
native law, that a referenced theorem has the stated hypotheses, that review
was independent, that held-out information was unavailable, or that an author
or reviewer is authentic. These require explicit trusted/manual review (or a
separately specified sound proof system and trust basis). Merely recording a
reviewer name, signature-like string, timestamp or matching hash supplies none
of those facts. The present API's opaque provenance string cannot replace
this review and continues to return operational ABSTAIN.

The minimum substantive review must establish: the bound's meaning as the
specified unconditional one-birth probability; every target/law parameter and
normalization premise; complete simultaneous coverage of the exact ordered
row; correct enclosure arithmetic; and validity of the selected confidence
and selection assumptions, if any. A valid theorem for another parent or a
calculation on another sector is insufficient. Historical custody failures
remain failures; this design does not reconstruct missing historical identity.

## 4. Coverage risk is separate from approximation error

For a fixed target P_a, valid deterministic enclosures establish all
`l_ai <= P_ai <= u_ai` simultaneously. Rational endpoints alone do not establish
this: a deterministic numerical algorithm may still use an unproved law map,
wrong rounding or incomplete cases. An analytic proof with discharged premises
may justify zero endpoint-certification risk within its declared model; the
word "deterministic" or a passed software test cannot assign that risk by fiat.

Statistical intervals instead need a justified bound on the event that **any**
required coordinate misses its target, covering the entire frozen producer,
calibration and selection procedure. It is not enough to attach a marginal
confidence label to each coordinate or select a favorable interval set after
inspection. If valid individual failure bounds exist for that same procedure,
a union bound can combine them across coordinates and arms without independence.
It does not invent valid bounds or justify a conditional claim from marginal
accuracy. Every probability claim must use the conditioning/selection regime
required by the selected optional protocol.

In certificate A of that protocol, the accepted endpoint events join its
pre-held-out good-certificate event G. Endpoint coverage failure belongs in
kappa together with the other justified certificate risks. It is **not** an
extra TV allowance inside eta. On G the fixed target lies in the envelope, so
the implemented deterministic proxy bound applies. Consumed-bit and channel
certificates must still hold conditional on complete history across both arms
and valid return. This fixed-row interface does not license adaptive targets,
per-draw interval revisions, favorable retries or selection on completion.

With actual reviewed certificates, a sufficient per-arm distribution allowance
would be `e_a=min(1,eta_a+gamma_a+epsilon_a)`, where gamma is the map's exact
rounding error and epsilon is a valid consumed-bit error. A predeclared proxy
budget may conservatively replace eta only after eta<=that budget is checked.
The channel allowance remains separate. The optional protocol still requires
its certified positive effect, bias margin, risk and cost inequalities and
frozen sample count. Its full-power claim needs its availability/failure bound;
the weaker wrong-terminal-decision-only option must retain that weaker label.

For certificate B, a row enclosure is only one component: it supplies no
whole-attempt joint distribution bound. For exact D4-A, even a zero-width
envelope supplies neither an exact independent sampling interface nor the
remaining exact-channel, effect and held-out premises. No protocol is amended
or automatically admitted by this design.

## 5. Fail-closed dispositions and bounded checks

An accepted target/row/enclosure binding may be recorded as
`COMPONENT_PREMISES_REVIEWED`. This is not sampling authorization, a diagnostic
PASS, or operational admission. Run-only premises can remain missing while the
bounded component review closes; the operational disposition remains ABSTAIN.

The proposed consumer returns ordered missing-premise reasons with the actual
field/claim and what evidence or correction is needed. Use ABSTAIN, not the
diagnostic's statistical FAIL, for missing/invalid schema, target binding,
complete row, endpoint semantics, proof/review, simultaneous coverage,
budget/resources or other protocol premises. No absent premise becomes true
through a default, a hash match or an arithmetic-success label. Unexpected
exceptions, interruptions or inaccessible required evidence are non-admission;
no automatic acquisition, retry or inference is authorized.

For example:

| Proposed input defect | Required reason and remedy |
| --- | --- |
| Eight cap-subset ideals, or the distinct C4/A2 row | `ABSTAIN_TARGET_OR_COMPLETENESS`: supply the correct bound parent and all eleven D4-A ideals/both bits; do not pad or reinterpret the row. |
| Correct count with one repeated pair and one omitted pair, or shuffled rows without a mapping | `ABSTAIN_ROW_DICTIONARY`: restore the exact canonical sequence with the associated endpoints and review. |
| One coordinate removed because its reported bound is zero | `ABSTAIN_ROW_COMPLETENESS`: retain the slot and adjudicate support consistency. |
| Disjoint intervals for the two fair newborn-bit masses of one ideal | `ABSTAIN_ENDPOINT_SEMANTICS`: explain/correct the incompatible target enclosures; do not average them. |
| A proof covers only supported classes, a different normalization, or selected successful returns | `ABSTAIN_PROOF_SCOPE`: provide complete joint-row coverage for the fixed unconditional target. |
| Exact fractions plus hashes but no accepted enclosure proof; marginal confidence after selection | `ABSTAIN_COVERAGE_OR_REVIEW`: provide the missing simultaneous, selection-valid justification and its risk accounting. |
| Valid envelope arithmetic but missing d, bit/channel certificate or feasible n | `ABSTAIN_PROTOCOL_PREMISE`: keep the component result separate and identify the unresolved protocol input. |

These are manual contract checks, not executions of an implemented admission
validator or fabricated endpoint certificates. The completeness count follows
from three strict chain prefixes plus 2^3 cap subsets; pairing both bits gives
22 outcomes. The fair-bit feasibility criterion follows from the interval-sum
argument above. Neither reasoning step requires acquiring a native probability.

This design closes the binding contract needed for a future certificate-producer
interface. It supplies no actual endpoints, producer, confidence calibration,
sampler, benchmark, physical channel or production qualification. The bounded
critical path is exact target/row binding, an applicable reviewed enclosure
claim, admitted arithmetic and the chosen decision's necessary premises. Full
deployment qualification remains separate. Existing custody restrictions and
the RET-only pause remain intact; publication or execution is not authorized
by the manuscript.
