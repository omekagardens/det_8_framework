# QR-05BU: bounded acquisition-distortion contract

9 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This sheet separates systematic population distortion from finite-sample
uncertainty. It derives an enlarged inverse, a correct-singleton budget
condition and an exact bound-only ambiguity threshold. No new mathematical
engine, test suite, confidence table, source/capture freeze, simulation or
physical acquisition is executed here. Displayed fractions are analytical
derivations and prospective controls, not measured or simulated results.

Continue the verified [BT decision](../qr-05bt-separation-budget-verification-2026-09-09/RESULTS.md)
without changing its frozen sources, first capture, quota or grid.

## 1. Standalone ideal model and unchanged target

Use auxiliary null coordinates u,v, signature (+,−), and supplied marks
Q=(0,1)², I₁=(0,1/2)², I₂=(0,3/4)×(0,1/2), with I₁⊂I₂⊂Q.
For η∈{0,1}, s∈{1,4}, δ∈[0,2], the comparison model is

```text
ds² = s(1+ηuv)du dv,       dμ = s(1+ηuv)du dv/2,
ρδ = 1+δuv,
M_z(δ) = (s/2)[z+(η+δ)z²/4+ηδz³/9],
q_i(η,δ) = M_zi(δ)/M_1(δ),      z₁=1/4, z₂=3/8,
τ(η) = μ(I₁)/μ(Q) = (16+η)/[16(4+η)].
```

Thus the ideal target is 1/4 for η=0 and 17/80 for η=1.
It remains an IDEAL relative proper volume, not the distorted record
frequency or a redefined instrument-specific target. Scale cancels from q
and τ. No ontological commitment or different physical law is required.

The external density premise B=[0,b] is uniform, half, one or two, with
b=0,1/2,1,2. It must contain the true δ. Define complete ideal families

```text
F_η(B) = {q(η,δ): δ∈B},
S = {(x₁,x₂): 0≤x₁≤x₂≤1}.
```

S is the closed nested-probability triangle. Every ideal point is strictly
inside its three category boundaries. Each F_η is a compact line segment:
for either region product z,

```text
q_0,z(δ) = (1−t₀)z+t₀z²,          t₀=δ/(4+δ),
q_1,z(δ) = (1−t₁)(4z+z²)/5
                         +t₁(9z²+4z³)/13,  t₁=13δ/(45+13δ).
```

Both coordinates use the same δ and segment parameter. The class distance
in the sup norm is

```text
D(B) = min {||p₀−p₁||∞: p₀∈F₀(B), p₁∈F₁(B)}
     = 3(1−b)/[16(4+b)] if b<1, and 0 otherwise.
```

For b<1 the attaining ideal densities are (b,0). Their gap is
D(4/5,1): every flat second coordinate is at least that of q(0,b),
and every conformal second coordinate is at most that of q(1,0).
This supplies a global lower bound, not just an endpoint comparison.
For b≥1, q(0,1)=q(1,0)=P=(17/80,21/64), so the distance is zero.

## 2. Actual records and the new external premise

One fixed actual population pair r∈S generates n independent,
identically distributed paired attempts. Their law, in 00,01,10,11 order, is

```text
π(r) = (1−r₂, r₂−r₁, 0, r₁).
```

Within-attempt dependence is expected; independence is required across
attempts. Unlike the ideal family, the actual law may have boundary
probabilities. Do not impose strict category positivity on r.

For one fixed true ideal world θ=(η,s,δ), posit a prospectively supplied
deterministic allowance e≥0 satisfying

```text
||r−q(θ)||∞ ≤ e,       δ∈B.
```

The letter e denotes population distortion, not the four sampling tail
allocations ε=1/80. It is not a sample deviation, standard error, grid step,
per-shot error probability or validated sensor specification. Neither r
nor q is supplied to a record receiver as known hidden truth. Their
relationship is a model premise, not something inferred from a small
difference between observed frequencies and a fitted prediction.

Keep fixed marks/target meaning, correct pairing and attempt association,
fixed n, no unmodeled loss or postselection, and the nested iid law.
A mark or response error is covered only if its entire effect satisfies
this bound relative to the SAME ideal marks and preserves these premises.
The allowance does not itself establish any of them.

No common known acquisition matrix or mechanism is specified. The
bound-only alternative classes permit hypothesis-specific nuisance choices
of r. A restriction requiring the same known channel across hypotheses
would be a different, potentially smaller uncertainty class.

## 3. Confidence remains about the actual population

Keep n=65,536, m=256, h=1/m, α=1/20 and four equal tail allocations
ε=1/80 fixed before acquisition. Validate every paired attempt before
forming K_i=Σ_jY_ji. Under the admitted law, 0≤K₁≤K₂≤n and each marginal
K_i is Binomial(n,r_i); their joint law is not a product of binomials.

For k∈{0,…,n}, define inclusive tails and closed outward-grid endpoints:

```text
T⁺(k;p) = Σ_(j=k)^n binom(n,j)p^j(1−p)^(n−j),
T⁻(k;p) = Σ_(j=0)^k binom(n,j)p^j(1−p)^(n−j),
G_m = {j/m: j=0,…,m},
L(k) = max({0} ∪ {g∈G_m: T⁺(k;g)≤ε}),
U(k) = min({1} ∪ {g∈G_m: T⁻(k;g)≤ε}),
C(K) = [L(K₁),U(K₁)] × [L(K₂),U(K₂)].
```

Use the explicit degenerate binomial laws at p=0,1. Defaults give L(0)=0
and U(n)=1; equality is included. The count-tail monotonicity argument
bounds each event r_i<L(K_i) or r_i>U(K_i) by its one-sided allocation:
for fixed p, the offending counts themselves form a tail whose probability
is no greater than ε. A union bound therefore gives, for every r∈S,

```text
E = {r∈C(K)},              P_r(E) ≥ 1−α.
```

No independence between the questions is used. These facts are the
[BQ continuous-parameter theorem](../qr-05bq-finite-record-uncertainty-design-2026-09-09/README.md)
applied to r, not to an unverified ideal q. Count intervals share the same
endpoint functions, which increase with k; thus valid nested counts
produce C∩S≠∅.

The [BS width argument](../qr-05bs-separation-budget-design-2026-09-09/README.md)
is likewise uniform over actual r. Writing W(C)=max_i(U_i−L_i),

```text
W(C) ≤ min(1, 2sqrt(ln(80)/(2n))+2h).
```

For completeness, the centered Bernoulli log-moment-generating function
has second derivative at most 1/4. Integration and exponential Markov
give each deviation tail at most exp(−2na²). Applying this to the exact
tail roots bounds each root within empirical frequency ±sqrt(ln(80)/(2n));
outward rounding adds less than h per endpoint. This is a deterministic
width bound for every count, not another failure event. BU evaluates
neither logarithms nor the n-dependent tail/count space.

## 4. Enlarge before ideal-model inversion

For a rectangular population box C=[L₁,U₁]×[L₂,U₂] with endpoints in
[0,1] and ordered coordinate intervals, define the exact bound-only inverse

```text
Θ_B,e(C) = {(η,s,δ): δ∈B, ∃r'∈C∩S with ||r'−q(η,δ)||∞≤e},
T_B,e(C) = {τ(η): (η,s,δ)∈Θ_B,e(C)}.
```

Here r' is an existential nuisance witness, not an estimate of the true r.
If C∩S is empty (equivalently L₁>U₂), Θ is empty BEFORE any enlargement.
That mathematical empty inverse is distinct from malformed input or an
operational refusal of an impossible 10 record.

When C∩S≠∅, this is exactly inversion of the enlarged box, with

```text
L_i^e = max(0,L_i−e),       U_i^e = min(1,U_i+e),
q(η,δ) ∈ [L₁^e,U₁^e] × [L₂^e,U₂^e].
```

The equivalence retains a nested r' witness. For any ideal q∈S in that
enlargement, put A_i=max(L_i,q_i−e), B_i=min(U_i,q_i+e).
Then A_i≤B_i. Also A₁≤B₂: the needed cross inequalities follow from
L₁≤U₂, q₁≤q₂ and individual interval feasibility. Consequently
r'=(A₁,max(A₂,A₁)) belongs to C∩S and is within e of q. The reverse
implication is immediate. Without checking C∩S first, an enlarged
inconsistent box could falsely acquire a latent nested-population witness.

Since M_Q>0 and all masses are affine in δ, exact candidate intervals
remain the intersection with B of FOUR linear inequalities:

```text
M_Ii(δ) − L_i^e M_Q(δ) ≥ 0,
U_i^e M_Q(δ) − M_Ii(δ) ≥ 0,       i=1,2.
```

Use the same δ in both coordinates. Retain empty or closed nuisance
intervals per labeled geometry; keep singleton endpoints and both scale
labels. The target set is a discrete subset of {17/80,1/4}, not its hull.
The rule depends on records, declared B,e and the model, not true η,δ,r.

On E and the true external premises, q_true lies in the enlargement.
Therefore

```text
E ⇒ θ_true∈Θ_B,e(C) ⇒ τ_true∈T_B,e(C),
P(τ_true∈T_B,e(C)) ≥ 1−α.
```

At e=0 this is the old ideal-law inverse exactly. For fixed C,B, enlarging
e can only add candidates/targets; this is monotone conservatism, not
evidence for any newly admitted alternative.

## 5. Correct-singleton transfer and the factor of two

Let d be a certified lower bound on distance from q_true to the ENTIRE
opposite ideal family. For an admitted opposite q', take its actual-law
witness r'∈C∩S. On E,

```text
||q'−q_true||∞
 ≤ ||q'−r'||∞ + ||r'−r||∞ + ||r−q_true||∞
 ≤ e + W(C) + e.
```

One e accounts for the true law's distortion; the other accounts for a
competing candidate's allowed distortion. For a particular batch the
implication is E∩{W(C)+2e<d} ⇒ correct singleton. The width is random.
If the prespecified design ensures W(C)+2e<d for EVERY possible count box,
as the rational certificate below does, the SAME event E alone gives

```text
P(correct singleton) ≥ 19/20,
P(wrong target | singleton) ≤ 1/20.
```

To prove the conditional statement, let a and w be correct- and
wrong-singleton probabilities. Then a≥1−α and a+w≤1, so
w/(a+w)=1−a/(a+w)≤1−a≤α. Singleton probability is positive.
Ordinary coverage without separation does not supply this conclusion.

The full box width, two distortion allowances and strict inequality are
all necessary for this sufficient argument. The result is not conditional
certainty for a chosen packet, and does not apply merely because a
particular output is singleton.

The unchanged width bound gives the conservative rational certificate

```text
s_e = d−2e−2h > 0,       n s_e² ≥ 10.
```

Indeed the positive exponential series gives
Σ_(j=0)^5 5^j/j!=1097/12>80, hence ln(80)<5; therefore the rational test
implies the required STRICT width inequality, including score equality.
Keep the sign test separate from squaring. This is sufficient, not
equivalent to actual identification or to its necessary sample budget.

Use the whole-class margin D(B) for an operational uniform budget.
A pointwise d consumes a declared true fixture and remains a research
planning quantity. A false density, distortion or acquisition premise
cannot be repaired by a passing arithmetic score. A deterministic valid
e consumes separation, not an additional probability allocation.

## 6. Exact actual-law class separation and collision

Define the full bound-only classes in actual-probability space:

```text
A_η(B,e) = {r∈S: dist∞(r,F_η(B))≤e},
D_e(B) = dist∞(A₀(B,e),A₁(B,e)).
```

These sets are compact. For arbitrary actual alternatives r₀,r₁, select
ideal witnesses p₀,p₁ at distance at most e from their respective r's.
The triangle inequality gives D≤2e+||r₀−r₁||∞. Thus

```text
D_e(B) ≥ max(D(B)−2e,0).
```

This lower bound is attained. Take an ideal minimizing pair p₀,p₁.
If D>0 and 0≤e≤D/2, put

```text
r₀ = (1−e/D)p₀ + (e/D)p₁,
r₁ = (e/D)p₀ + (1−e/D)p₁.
```

Convexity keeps both actual points in S. Their displacements from their
ideal witnesses have norm e, and their mutual norm is D−2e.
For e≥D/2 use the common midpoint; if D=0 use the inherited common point.
These cases never divide by zero. Therefore, exactly,

```text
D_e(B) = max(D(B)−2e,0).
```

For the narrow bounds, p₀−p₁=D(4/5,1), so before collision the actual
contacts are p₀−e(4/5,1) and p₁+e(4/5,1). The inherited normal (0,1)
also gives the global signed lower bound D−2e. After contact use norm
nonnegativity for the zero lower bound, not a negative claimed distance.

| Bound | Ideal density contacts | First collision allowance e=D/2 | Shared actual pair |
|---|---|---:|---|
| uniform | (0,0) | 3/128 | (37/160,45/128) |
| half | (1/2,0) | 1/96 | (53/240,65/192) |
| one, two | (1,0) | 0 | (17/80,21/64) |

At or above a collision allowance the common actual pair gives the same
ENTIRE nested marked-symbol law π(r) under different ideal targets,
hence the same iid record law for any fixed quota. Correct-singleton
probabilities for the two targets then sum to at most one under that
common law. No procedure can make both exceed 1/2 uniformly.

For this enlarged-common-box procedure, on the same event r∈C both
colliding ideal targets are admitted, so P(both targets)≥1−α.
That stronger statement uses this procedure; it is not a claim about every
confidence-set construction. The new collision is at the marked-record
interface, not a proof of identical distorted continuous-point densities.
The old one/two collision already had the stronger ideal whole-point equality.

These are obstructions for the stated maximal bound-only classes.
They do not assert that one specified known physical channel causes the
collision. Restricting allowed mechanisms could change the result.
By contrast, failing the finite-budget certificate while D_e>0 is not
an information-theoretic impossibility proof.

## 7. Calibration validity and acquisition exclusions

As a conditional extension, suppose a calibration procedure supplies a
nonnegative allowance e_cal. Define G={||r−q_true||∞≤e_cal}, and use e_cal
in the enlarged inverse, with all other model/acquisition premises still
in force. BU supplies no such procedure. If a separate proof gives
P(Gᶜ)≤β, and the unchanged sampling event still has P(Eᶜ)≤α, union
bounding gives
P(E∩G)≥1−α−β without independence. The coverage transfer applies on
that intersection. If the separation certificate also holds throughout
it, correct-singleton probability is at least 1−α−β and conditional
wrong-singleton probability is at most α+β, provided α+β<1.

A supplied e is not such a calibration theorem. Neither a product
(1−α)(1−β) nor nominal error conditional on valid calibration follows
from marginal error bounds alone. Those require independence or an
appropriate conditional sampling guarantee. Same-record calibration
requires genuine marginal validity for both events and cannot silently
change the fixed sampling law or procedure.

If random calibration passes separation only on an acceptance event H,
only E∩G∩H⇒correct singleton is automatic; the corresponding unconditional
lower bound is P(H)−α−β, truncated below by zero. Reporting only accepted
calibrations/batches or repeating until success needs a separate selection
argument. BU provides no β, calibration method or accepted-batch guarantee.

A population marginal bound alone does not even establish nested support.
For any ideal q choose 0<λ≤min(q₁,1−q₂) and consider the iid four-symbol law

```text
(1−q₂−λ, q₂−q₁+λ, λ, q₁−λ).
```

Its marginals remain r=q, satisfying e=0, but P(10)=λ>0.
For the existing flat δ=0 point, λ=1/16 gives (9/16,3/16,1/16,3/16).
The probability of at least one 10 is 1−(15/16)^n, at least 1/16>α.
Do not numerically evaluate this large power here. This law is OUTSIDE
the admitted nested channel: a marginal-only check would miss the defect.
Refuse a 10 per attempt; aggregate K₁≤K₂ or seeing no 10 does not certify
its population probability is zero. Never delete, relabel or postselect it
to manufacture admissibility.

Unmodeled loss, attempt dependence, nonstationary drift, changed ideal
marks/targets and unsupported geometry/density families remain outside
the theorem. Within-attempt dependence is not a defect. Ideal inequalities
q₁≤1/4 and q₂≤3/8 do not hold unchanged for r when e>0, so BQ's particular
all00/all11 ideal-law probability controls are not silently inherited.

## 8. Fixed analytical controls and bounded successor

Propose **QR-05BV: bounded acquisition-distortion verification**.
It is not implemented or executed by BU. Fix complete schemas, source
identities and work limits before its first helper, oracle, engine or test.

Keep n=65,536,m=256,α=1/20, four ε=1/80. Use exactly eight class/error
rows: uniform and half at e=0,D/4,D/2, and one/two only at e=0.
These derived allowances test geometry and budget logic; none is a
calibrated instrument tolerance or an optimum found by scanning.

| Bound | e | Exact D_e | Planning slack D−2e−1/128 | Score | Analytical expectation |
|---|---:|---:|---:|---:|---|
| uniform | 0 | 3/64 | 5/128 | 100 | Certified |
| uniform | 3/256 | 3/128 | 1/64 | 16 | Positive-distortion certificate |
| uniform | 3/128 | 0 | −1/128 | 4 | Attained collision |
| half | 0 | 1/48 | 5/384 | 100/9 | Certified |
| half | 1/192 | 1/96 | 1/384 | 4/9 | Separated but not budget-certified |
| half | 1/96 | 0 | −1/128 | 4 | Attained collision |
| one | 0 | 0 | −1/128 | 4 | Inherited collision |
| two | 0 | 0 | −1/128 | 4 | Inherited collision |

Retain ideal contacts/segments, actual contacts and complete π laws,
distortion displacements, exact lower/attainment certificates, signed
planning slack/score and eligibility. Preserve failures; do not optimize
e,n,m to make them pass. In these rows D−2e≥0, but the general theorem
must still distinguish signed remaining allowance from a nonnegative
distance and handle the D=0 branch without division.

Use exactly ten derived singleton POPULATION-box controls:

- For each narrow bound, at e=D/4 take C={p₀}, C={p₁}, and C={midpoint}.
  The first two retain only their respective ideal target; the third
  retains neither because each complete ideal family is at distance D/2
  from the midpoint: the ordered second coordinates give the lower bound,
  and the two retained ideal contacts attain it. The empty case has no
  admissible true ideal world
  at that allowance, not a coverage-theorem failure.
- For each narrow bound also take C={midpoint}, e=D/2. Both targets are
  admitted at the closed ideal contact densities (b,0). The unexpanded
  inverse is empty despite exact coverage of this admissible actual r.
  This explicitly refutes applying the old ideal inverse unchanged.
- For one and two take C={P}, e=0, retaining the inherited collision.

These are eight narrow-bound controls plus two broad-bound controls.
They are not claimed to be newly acquired binomial confidence outputs.
Retain exact shared-δ intervals, complete forward constraints and actual
r' witnesses; never replace coupled admission with coordinatewise
independent densities. A hypothetical C∩S=∅ is an input-boundary control,
not an additional main population fixture.

For the half-bound positive boxes, the nontrivial own-family intervals
are analytically flat δ∈[16/41,1/2] for C={p₀}, and conformal δ∈[0,18/209]
for C={p₁}, both at e=1/192. The original four mass inequalities determine
these intervals, not separate per-coordinate choices. At the midpoint
with e=1/96, the admitted densities are exactly flat {1/2}, conformal {0}.

Also retain the single λ=1/16 nonnested negative control above without
enumerating words or calculating its n-dependent refusal law, and the two
fixed scale-pair algebraic comparisons. These compare equal ideal curves,
actual-law classes and inverses at identical supplied B,e,C. They do not
assert equality of arbitrarily chosen actual r across scale worlds.
Do not add a fixture probability bank. At e=0 compare the four complete
class certificates and planning
projections with authenticated stored BT evidence, not a BT rerun.

Primary and reference routes must independently construct masses/segments,
actual contact/lower certificates and box inverses. One may use affine
mass inequalities and the other shared segment-parameter clipping with
explicit nested actual-law witnesses. Tests should use direct forward
laws, global lower inequalities and a third exact inverse check; agreement
between rounded summaries is insufficient.

Before execution, freeze the six new BV source/schema/test files, the two
BU Markdown files, BT README/RESULTS/capture and the authenticated BM
evidence-utility source. Use the literal stored BT capture pin and fresh
utility authentication before parsing/executing those respective inputs.
This is twelve identities; it is not inherited execution of old mathematics.
Sources remain ≤262,144 bytes, capture artifacts ≤16,777,216 bytes,
analyses ≤30 seconds and suites ≤120 seconds. Use one cached analysis
per normal/optimized suite, one full replay per mode and exactly one
alternate-runtime reference-only audit with complete native equality.
Create-only evidence and final byte readbacks must preserve first failures.

No large-quota tail/count table, numerical logarithm, probability/geometry
sweep, new record-observer API, dependency installation, RET integration,
timing-sensitive RET overlap or physical acquisition. BV is a bounded
verification of this contract, not apparatus calibration.

## 9. Decision boundary and provenance

BU supplies analytical theorems and a prospective verification scope,
not Lean verification or executed numerical evidence. It preserves BT's
first capture and all pre-existing core/RET/application work.
The separate [decision record](RESULTS.md) records review and limitations;
the [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated.

The applicable structure is a precise ideal-to-observed-law robustness
contract: record uncertainty can be propagated into discrete geometric
target sets, with systematic ambiguity distinguished from sampling and
rounding limitations. It is not general metric reconstruction, a gravity
equation, an ontological proof or evidence of new physics. Calibration,
general densities/metrics, RET and quantum adapters remain separate.
Book work remains archival; Lean installation, clocks and later gravity
couplings stay deferred.
