# QR-05DB results

11 September 2026 (Pacific/Honolulu). **The metric-axiom obstruction for count-only
reconstructions: an impossibility result and a positive control.** The QR-05DA count
estimator is not a Lorentzian metric; no count-only reconstruction is simultaneously
convergent, positive on links, and axiom-compliant; the order-only longest-chain
estimator is a Lorentzian premetric whose convergence is open. 12 tests pass.
Supplied geometry; no metric, continuum, curvature or gravity claim.

## 0. Setup and axioms

A finite causal set `(X, ≺)`. A Lorentzian distance (premetric) `d` must satisfy

- **A0** `d(x,x) = 0`;
- **A1** `d(x,y) > 0 ⇔ x ≺ y` (`x ≠ y`);
- **A2 (reverse triangle)** `x ≺ y ≺ z ⇒ d(x,z) ≥ d(x,y) + d(y,z)`.

Reconstructions are compared to the directed Lorentzian distance `τ` under a global
homothety (scale-free LGH distortion; absolute scale is non-identifiable, QR-05CY).

**Count law and the convergence exponent.** In a Poisson sprinkling of density `ρ`
into `d`-dimensional Minkowski spacetime, `m_ij ≈ ρ·Vol(I(i,j))`. Every Alexandrov
interval with Lorentzian distance `τ` is the image of the standard interval
`I((0,0),(τ,0))` under a Lorentz boost, which has unit determinant and preserves `τ`;
so `Vol(I) = c_d τ^d`, a function of `τ` alone. Hence `m ≈ ρ c_d τ^d`. This is the
only imported scaling.

## 1. R1 — the QR-05DA count estimator violates A2 (unconditional)

`d(i,j) = ℓ√(1 + m_ij)` is positive exactly on the causal relation (A1 holds) but
fails A2. The three-event chain `a ≺ b ≺ c` with consecutive links has
`m_ab = m_bc = 0`, `m_ac = 1`, so `d(a,c) = ℓ√2 < 2ℓ = d(a,b) + d(b,c)`. This is not
an isolated defect: on Poisson sprinklings the violation fraction is large
(`d=2,n=64`: 4511/8987 ≈ 50%; `d=3,n=64`: 286/940 ≈ 30%), with the worst gaps
`≈ −1.2ℓ`. The directed Lorentzian distance satisfies A2, and so does the order-only
chain estimator.

**Constructive link-triple bound.** For a link triple the offset gap is
`ℓ(√(1+m_ac) − 2)`, negative for every `m_ac ≤ 2` and zero only at `m_ac = 3`. Hence
the offset form violates A2 on any link triple whose interval holds at most two
points, with gap at least `ℓ(√3 − 2)` (worst `ℓ(√2 − 2)`).

## 2. R2 — no count-only reconstruction is convergent, positive and axiom-compliant

Let `d(i,j) = ℓ·g(m_ij)` with `g ≥ 0` non-decreasing, `ℓ = ρ^{-1/d}`.

**Claim A (A2 forces shifted superadditivity).** *If A2 holds and the admissible class
contains the pure chains, then for all `x, y ≥ 0`, `g(x+y+1) ≥ g(x) + g(y)`.*

*Proof.* Take `a ≺ b ≺ c` in a pure chain with `x` elements strictly between `a, b` and
`y` strictly between `b, c`. Then `m_ab = x`, `m_bc = y`, and `m_ac = x + y + 1`
(the `x + y` points plus `b`). A2 gives the inequality. ∎

**Claim B (positivity ⇒ at-least-linear growth).** *If `g(0) > 0` and Claim A holds,
then `liminf_{m→∞} g(m)/m ≥ g(0) > 0`.*

*Proof.* With `x = y = n`, Claim A gives `g(2n+1) ≥ 2g(n)`, and induction gives
`g(2^k(n+1) − 1) ≥ 2^k g(n)`. Dividing,
`g(2^k(n+1)−1)/(2^k(n+1)−1) ≥ 2^k g(n)/(2^k(n+1)−1) → g(n)/(n+1)`.
So `liminf g(m)/m ≥ g(n)/(n+1)` for every `n`; taking `n = 0` gives `≥ g(0) > 0`. ∎

**Claim C (convergence ⇒ sublinear growth).** *If `d` converges to the Lorentzian
distance at every timelike pair in a Poisson–Minkowski sprinkling of dimension
`d ≥ 2`, then `g(m)/m → 0`.*

*Proof.* For a timelike pair, `m ≈ ρ c_d τ^d` and `d = ρ^{-1/d} g(m) → c τ`. Substituting
`τ = (m/(ρ c_d))^{1/d}` gives `g(m) → c c_d^{-1/d} m^{1/d}`: the density factors cancel,
so `g(m) ~ C m^{1/d}` and `g(m)/m ~ C m^{1/d − 1} → 0` since `1/d − 1 < 0`. ∎

**Theorem.** No count-only reconstruction `d = ℓ·g(m)` can satisfy A1 (positive on
links), A2, and convergence simultaneously. Indeed A1 forces `g(0) > 0`, so by Claims A
and B `liminf g(m)/m ≥ g(0) > 0`, contradicting Claim C. ∎

The two natural forms are the two horns: the **offset** form `g(m) = √(1+m)` has
`g(0) = 1` (A1 holds, A2 fails, R1); the **raw** form `g(m) = √m` has `g(0) = 0` (A2
holds in the continuum mean at `d = 2` where the exponent `1/2 = 1/d`, but A1 fails on
every link — 71/197/251 link pairs at `d=2,32 / d=2,64 / d=3,64`). No count-only form
evades both horns.

## 3. R3 — the order-only longest-chain estimator is a Lorentzian premetric (unconditional)

Let `L(i,j)` be the longest-chain length. If `x ≺ y ≺ z`, concatenating a longest
`x→y` chain with a longest `y→z` chain gives an `x→z` chain of length
`L(x,y) + L(y,z)`, so `L(x,z) ≥ L(x,y) + L(y,z)`. Also `L(x,x) = 0` and `L(x,y) > 0 ⇔
x ≺ y`. Hence `d = ℓ·L` satisfies A0–A2 on **every** finite causal set. The census
verifies this exactly: 0 support mismatches and 0 reverse-triangle violations across
all 21 rows (sprinklings, pure chain, random poset, antichain). It is a Lorentzian
premetric. QR-05DA shows its scale-free ceiling does not vanish, so its convergence is
not established.

## 4. R4 — the count is structurally superadditive

For `a ≺ b ≺ c`, every point strictly between `a` and `b`, or between `b` and `c`, is
strictly between `a` and `c`, and `b` itself is too; these sets are disjoint, so
`I(a,b) ⊔ I(b,c) ⊔ {b} ⊆ I(a,c)` and `m_ac ≥ m_ab + m_bc + 1`. Verified exactly: 0
violations over 11 282 triples across all 7 objects. This superadditivity is why the
count tracks the volume `∝ τ^d`, and it is also why the constraint in Claim A appears —
but it cannot rescue A2 once positivity (`g(0) > 0`) is imposed.

## 5. Adversarial non-manifoldlike controls

| control | chain (A0–A2) | count offset | count raw |
|---|---|---|---|
| `pure_chain_n8` | holds (0/56) | fails A2 (56/56) | fails A1 (7 links at 0), A2 20/56 |
| `random_poset_n12` | holds (0/12) | fails A2 (12/12) | fails A1 (11 links at 0), A2 0/12 |
| `antichain_n6` | holds (vacuous) | fails A2 vacuously (no triples) | fails A1 vacuously (no causal pairs) |

The order-only estimator satisfies the axioms even on these non-manifoldlike orders
(the axiom is poset-generic); the count estimator's failure is likewise generic.

## Findings

1. **R1 (unconditional):** `ℓ·√(1+m)` is a distance estimator, not a Lorentzian
   metric — it violates A2 on real sprinklings (§1).
2. **R2 (conditional impossibility):** with the elementary volume law, no count-only
   reconstruction is convergent, positive on links, and axiom-compliant (§2).
3. **R3 (unconditional):** `ℓ·L` is a Lorentzian premetric on every finite causal set;
   its convergence is the open part (§3).
4. **R4:** structural superadditivity of the count is exact (§4).

**Consequence.** The axiom-compliant, convergence-candidate object must be order-based
(or mixed); a count-only reconstruction cannot be it.

## What this changes and what remains

**Changes.** QR-05DA's estimator split is proved: the count form diverges from the
Lorentzian-distance axioms exactly where it gains its convergence, and vice versa. The
metric-axiom question the steering posed is answered negatively for the count-only
family, with a machine-checked witness and a conditional impossibility theorem.

**Remains.** A **constructive** vanishing bound for an order-based or **mixed**
order+count reconstruction; whether such a reconstruction can satisfy A0–A2 *and*
converge; density/commensurability; ensemble convergence; manifoldlikeness of a limit.
No metric, continuum, curvature, dynamics or gravity is claimed. Curvature and the
imported BD operator stay parked; κ-gravity is retired and gravity is standard GR under
Option B.

## Verification and provenance

`primary.py` (forward source chains, set-intersection counts, direct triple census) and
`reference.py` (backward intermediate-node chains, bitmask counts, recoded census)
build the estimators, both censuses, the structural lemma and the report
independently; the driver compares with a float tolerance and refuses on any
difference. `test_qr05db.py` pins the census with known-answer checks on hand-built
three-chains and a strict-superadditivity poset, and asserts the flags and verdict.

- Capture: `results.json`, SHA-256 `77774c21c50f1ece76216eda8c0e73078cc04623acc559caaf551fdf75fa2697`.
- Freeze: `source-freeze.json`, SHA-256 `c4d7b7708006f257ef683a9eeed9b9f4a4c9e9e2a82329f3054b752f50605014`.

QR-05DB continues the committed `qr-05-bridge` branch (from DB's predecessor, the
QR-05DA correction commit `48f652a`). Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
