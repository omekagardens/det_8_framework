# QR-05DC: the max-plus closure and the order-domination of the mixed bound

11 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: a constructive existence result with a negative uniform-bound result.** The
max-plus closure of the count weight is the canonical **A2-compliant mixed
order+count** reconstruction, and it satisfies A0–A2 exactly — but its uniform
(scale-free `L∞`) distortion equals the **order-only longest-chain** estimator's for
every link weight tested, and is strictly worse than the count's. Enforcing A2
therefore forfeits the count's smaller ceiling; the mixed uniform vanishing bound
**reduces to the order-only problem** that QR-05DA leaves open. No metric, continuum,
curvature or gravity claim.

Follows [QR-05DB](../qr-05db-count-reconstruction-obstruction-2026-09-11/README.md) and
the pre-specified Next in the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).

## 1. Pre-specification (fixed before the computation)

- **Question.** Can a *mixed* order+count reconstruction be constructed with a
  provable vanishing error bound while satisfying the Lorentzian metric-space axioms
  A0–A2?
- **Reconstruction.** The **max-plus (longest-path) closure** of an edge weight `w`:
  `D_w(i,j) = max over chains i = p_0 ≺ … ≺ p_k = j of Σ_t w(p_{t-1}, p_t)`. Mixed
  weight `w_a = a·ℓ` on links (`m = 0`) and `w_a = ℓ·√(1+m)` on every other causal
  pair, so the order (the chains) and the count (the segment weights) both enter.
- **Admissible class / sampling.** Poisson sprinklings of 1+1 Minkowski into the unit
  diamond, mean spacing `ℓ = √(AREA/n)`, `n ∈ {32, 64, 128}`, seeds `{0, 1}`.
- **Scale/anchor.** Homothety only; matrices normalised by the mean positive entry;
  the absolute scale is non-identifiable (QR-05CY).
- **Axioms.** `A0 d(x,x)=0`; `A1 d(x,y)>0 ⇔ x ≺ y`; `A2 x ≺ y ≺ z ⇒
  d(x,z) ≥ d(x,y)+d(y,z)`.
- **Convergence notion.** Scale-free `L∞` distortion `min_{c>0} max_{ij}|D_ij − c τ_ij|`
  to the directed Lorentzian distance `τ`.
- **Constructive bounds.** Pointwise domination `D_w ≥ w` and `D_w ≥ (min link
  weight)·L` (§3).
- **Controls.** The count estimator (A1 holds, A2 fails) and the longest-chain
  estimator (A0–A2 hold); the `a = 0` weight is a diagnostic in which links get zero
  distance (A1 fails).

## 2. The closure is the A2-compliant mixed reconstruction

`D_w` is superadditive by **max-plus transitivity**: concatenating an optimal `x→y`
chain with an optimal `y→z` chain gives an `x→z` chain, so `D_w(x,z) ≥ D_w(x,y) +
D_w(y,z)` (A2); `D_w(x,x) = 0` (A0); and when `w > 0` on every causal pair the direct
edge gives `D_w(i,j) > 0 ⇔ i ≺ j` (A1). Conversely, every A2-compliant reconstruction
equals the closure of its own link weights. So the axiom-compliant mixed family is
exactly these closures — the count can enter A2-compliantly only through the closure.

Verified on every object (`closure_a1`): 0 support mismatches, 0 reverse-triangle
violations. By contrast the plain count estimator violates A2 heavily:

| object | count RT violations / triples | closure(a=1) RT violations |
|---|---|---|
| sprinkle_d2_n32_s0 | 470 / 739 | 0 |
| sprinkle_d2_n32_s1 | 536 / 752 | 0 |
| sprinkle_d2_n64_s0 | 4224 / 7679 | 0 |
| sprinkle_d2_n64_s1 | 5515 / 8282 | 0 |
| sprinkle_d2_n128_s0 | 24916 / 56460 | 0 |
| sprinkle_d2_n128_s1 | 38071 / 65676 | 0 |

## 3. Order-domination: the closure does not recover the count's ceiling

Scale-free `L∞` distortion (`×1`; smaller is better). The closure is swept over the
link weight `a ∈ {0, 0.25, 0.5, 0.75, 1.0}` (`a = 0` fails A1, shown for diagnosis).

| object | count | chain | closure a=0 | a=0.25 | a=0.5 | a=0.75 | a=1.0 | best closure |
|---|---|---|---|---|---|---|---|---|
| sprinkle_d2_n32_s0 | 0.6376 | 1.0251 | 0.9420 | 1.1965 | 1.0733 | 0.9835 | 1.0251 | 0.9420 |
| sprinkle_d2_n32_s1 | 0.5391 | 0.6394 | 0.6997 | 0.8671 | 0.7496 | 0.6488 | 0.6394 | 0.6394 |
| sprinkle_d2_n64_s0 | 0.5208 | 0.7823 | 0.6756 | 0.7878 | 0.7877 | 0.7918 | 0.7811 | 0.6756 |
| sprinkle_d2_n64_s1 | 0.4637 | 0.6903 | 0.5551 | 0.6284 | 0.6148 | 0.6027 | 0.6903 | 0.5551 |
| sprinkle_d2_n128_s0 | 0.4810 | 0.8926 | 0.7826 | 0.8730 | 0.8460 | 0.8504 | 0.8744 | 0.7826 |
| sprinkle_d2_n128_s1 | 0.3922 | 0.6598 | 0.6061 | 0.6365 | 0.6300 | 0.6427 | 0.6592 | 0.6061 |

Three facts, all flagged in the report:

1. **The closure dominates the weighted longest chain (T2, exact).**
   `D_w ≥ w` and `D_w ≥ (min link weight)·L` pointwise (0 violations of `D_w(i,j) ≥
   a·ℓ·L(i,j)` over all 30 object×weight rows). So the closure can never sit strictly
   below a rescaled longest-chain estimator at any pair.
2. **The closure tracks the chain (T3, measured).** For `a = 1` the closure's
   distortion equals the chain's to within `≤2%` on every object, and its *best* over
   `a` (0.56–0.94) is still far above the count's (0.39–0.64). Tuning the link weight
   down does **not** recover the count's ceiling — not even at the `a = 0` limit.
   The reason is that the closure is a **maximum over chains**: the max-plus
   inflation is fluctuation-dominated, and it reproduces the longest chain's large
   probe fluctuations rather than the count's smaller ones.
3. **Pointwise domination does not transfer to the uniform bound.** The scale-free
   `L∞` distortion is *not* monotone under pointwise domination (raising `D` at a
   pair above `cτ` while the band is fixed can increase `|D − cτ|`), so T2 alone does
   not imply anything about δ; T3 is measured, not derived.

## 4. Findings

1. **A2-compliant mixed order+count reconstructions exist (T1, exact).** The max-plus
   closure is one, and all of them are closures of their link weights.
2. **The closure dominates the weighted longest chain (T2, exact).**
3. **But the closure's uniform bound is order-dominated (T3, measured).** For every
   link weight tested, the closure's scale-free `L∞` distortion equals the
   longest-chain estimator's and exceeds the count's best. The count's smaller
   ceiling (QR-05DA/DB) is **not accessible** once A2 is imposed.
4. **Consequence.** The mixed order+count *uniform* vanishing bound reduces to the
   order-only (longest-chain) uniform problem, which QR-05DA leaves open. There is no
   free lunch: the count improves the count-only estimator, but A2 enforcement—max
   over chains—reinstates the order-only fluctuation.

## 5. Boundaries

A bounded computation on supplied geometry. It states and machine-verifies a
constructive existence result and a pointwise domination lemma, and it measures (does
not prove) the order-domination of the uniform bound on 6 sprinkled objects. It does
**not** prove that no A2-compliant reconstruction can have a vanishing uniform bound
(non-uniform link weights are untested), does not establish convergence or
non-convergence, and makes no metric, continuum, curvature, dynamics or gravity claim.
Curvature and the imported BD operator stay parked; κ-gravity is retired and gravity is
standard GR under Option B.

## 6. Evidence and limits

`primary.py` (per-source longest-path closure, forward source chains, set-intersection
counts) and `reference.py` (Floyd–Warshall max-plus closure, backward intermediate-node
chains, bitmask counts) build the estimators, the axioms, the domination check, the
weight sweep and the report independently; the driver compares with a float tolerance
and refuses on any difference. `test_qr05dc.py` (13 tests) pins the closure with
known-answer checks (constant weight ⇒ longest-chain estimator; a heavy edge reroutes
the closure; superadditivity exact) and asserts the flags/verdict. `study.py` writes
create-only `results.json` and `source-freeze.json`. Fixed seeds make the run
deterministic. Limits: sources ≤ 262 144 bytes, artifacts ≤ 16 777 216 bytes. Decision
record: [RESULTS.md](RESULTS.md).
