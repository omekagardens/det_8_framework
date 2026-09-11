# QR-05DC results

11 September 2026 (Pacific/Honolulu). **The max-plus closure: a constructive,
A2-compliant mixed order+count reconstruction whose uniform bound is order-dominated.**
The closure satisfies A0–A2 exactly and is the minimal such reconstruction dominating a
given weight; it dominates the weighted longest chain; but its scale-free `L∞`
distortion equals the order-only longest-chain estimator's for every link weight tested
and is strictly worse than the count's. The mixed uniform vanishing bound reduces to the
order-only problem. 13 tests pass. Supplied geometry; no metric, continuum, curvature or
gravity claim.

## 0. Setup

Causal-set axioms (`A0 d(x,x)=0`; `A1 d(x,y)>0 ⇔ x ≺ y`; `A2 x ≺ y ≺ z ⇒ d(x,z) ≥
d(x,y)+d(y,z)`), the max-plus closure
`D_w(i,j) = max over chains i = p_0 ≺ … ≺ p_k = j of Σ_t w(p_{t-1}, p_t)`,
and the mixed weight `w_a = a·ℓ` on links (`m = 0`), `w_a = ℓ·√(1+m)` elsewhere.
The distortion is the scale-free `L∞` distance `δ(D) = min_{c>0} max_{ij}|D_ij − cτ_ij|`
to the directed Lorentzian distance `τ`. All matrices are normalised by the mean
positive entry (a global scale, absorbed by the minimisation over `c`).

## 1. T1 — the closure is the minimal A2-compliant reconstruction dominating its weight

**Claim.** `D_w` is superadditive; if `w > 0` on every causal pair then `D_w` satisfies
A0–A2 with exact causal support; and `D_w` is the pointwise-minimal superadditive
function `≥ w`.

*Proof.* Superadditivity: for `x ≺ y ≺ z`, concatenate an optimal `x→y` chain and an
optimal `y→z` chain at `y`; the result is an `x→z` chain of weight `D_w(x,y)+D_w(y,z)`,
so the maximum `D_w(x,z)` is at least that (A2). `D_w(x,x)=0` by convention (A0). For
`x ≺ y`, the direct edge gives `D_w(x,y) ≥ w(x,y) > 0`, and `D_w(x,y)=0` when `x ⊀ y`
(A1). Minimality: let `D` be superadditive with `D ≥ w`. Iterating A2 along any chain
`p_0 ≺ … ≺ p_k` gives `D(p_0,p_k) ≥ Σ_t D(p_{t-1},p_t) ≥ Σ_t w(p_{t-1},p_t)`; the
maximum over chains gives `D ≥ D_w`. ∎

So the A2-compliant reconstructions dominating `w` are exactly the superadditive
functions between `D_w` and the pointwise-maximal one; the mixed order+count object
`D_{w_a}` is the *least* A2-compliant reconstruction that already uses the count. The
census confirms 0 support mismatches and 0 reverse-triangle violations for
`closure(a=1)` on all six objects, against 470–38071 count violations (§README).

## 2. T2 — the closure dominates the weighted longest chain (exact)

**Claim.** `D_w(i,j) ≥ w(i,j)` and `D_w(i,j) ≥ Σ over the longest chain i→j of w(links)
= a·ℓ·L(i,j) ≥ (min link weight)·L(i,j)`.

*Proof.* The direct edge gives the first. For the second: the longest chain's
consecutive pairs are links (a longer chain would otherwise exist), so it is an
admissible chain and `D_w` is at least its weight sum. ∎

Verified: 0 violations of `D_w(i,j) ≥ a·ℓ·L(i,j)` across all 30 object × weight rows
(`domination_violations = 0` everywhere).

## 3. T3 — the uniform bound is order-dominated (measured)

The scale-free `L∞` distortion is **not monotone under pointwise domination**: raising
`D` at a pair above `cτ` increases `|D − cτ|` while `cτ − D` falls, so T2 does not by
itself constrain `δ`. The order-domination is therefore *measured*:

| object | count | chain | best closure over a ∈ {0,.25,.5,.75,1} |
|---|---|---|---|
| sprinkle_d2_n32_s0 | 0.6376 | 1.0251 | 0.9420 |
| sprinkle_d2_n32_s1 | 0.5391 | 0.6394 | 0.6394 |
| sprinkle_d2_n64_s0 | 0.5208 | 0.7823 | 0.6756 |
| sprinkle_d2_n64_s1 | 0.4637 | 0.6903 | 0.5551 |
| sprinkle_d2_n128_s0 | 0.4810 | 0.8926 | 0.7826 |
| sprinkle_d2_n128_s1 | 0.3922 | 0.6598 | 0.6061 |

On every object the best closure distortion (0.56–0.94) exceeds the count's
(0.39–0.64), and at `a = 1` the closure equals the chain to within `≤2%`. Shrinking the
link weight toward `0` — even to the A1-violating limit — does not lower the closure to
the count's ceiling. The mechanism is that `D_w` is a **maximum over chains**: its
value is set by the most inflated chain, which reproduces the longest chain's large
probe fluctuations (QR-05DA's slow ceiling), not the count's smaller ones.

## 4. Findings

1. **T1:** an A2-compliant mixed order+count reconstruction exists (the closure), and
   it is minimal among those dominating a weight. Axiom compliance is attainable.
2. **T2:** the closure dominates the weighted longest chain pointwise, exactly.
3. **T3:** but its uniform scale-free `L∞` distortion equals the order-only
   longest-chain estimator's and exceeds the count's best, for every link weight
   tested. The count's smaller ceiling (QR-05DA/DB) is not accessible once A2 is
   imposed.
4. **Consequence.** The mixed order+count *uniform (max-over-pairs)* vanishing bound
   reduces to the order-only longest-chain uniform problem, which QR-05DA leaves open.
   A count-only reconstruction cannot be the axiom-compliant convergent object (DB);
   nor does closing it up into an A2-compliant mixed reconstruction improve the uniform
   bound (DC). The open question is now sharply the order-only one.

## 5. What this changes and what remains

**Changes.** The steering's "can a mixed order+count reconstruction be built?" is
answered: yes, constructively (the closure), and its axioms hold exactly — but the
uniform bound is order-dominated, so A2 compliance does not buy the count's ceiling.
This closes the count-only/mixed axis of the convergence problem: the remaining
obstruction is entirely order-only.

**Remains.** A **non-uniform** link weight (e.g. one calibrated per pair by a local
density estimate) is untested and is the only apparent escape; whether *any*
A2-compliant reconstruction has a vanishing uniform bound is not decided; and the
order-only longest-chain uniform bound itself remains open. Density/commensurability and
ensemble convergence are untouched. No metric, continuum, curvature, dynamics or
gravity is claimed. Curvature and the imported BD operator stay parked; κ-gravity is
retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (per-source longest-path closure, forward source chains, set-intersection
counts) and `reference.py` (Floyd–Warshall max-plus closure, backward intermediate-node
chains, bitmask counts) build the estimators, the axiom census, the domination check,
the weight sweep and the report independently; the driver compares with a float
tolerance and refuses on any difference. `test_qr05dc.py` pins the closure with
known-answer checks on a hand-built poset (constant weight ⇒ longest-chain estimator; a
weight-5 edge reroutes the closure to 7) and asserts the flags and verdict.

- Capture: `results.json`, SHA-256 `57c9f18672c9484d717b70dccf78ba2c1590c4e55fbb0186d29ced59136d8c54`.
- Freeze: `source-freeze.json`, SHA-256 `db18c119fe55981bb012e36c7866f36c6a1fbad24ca2c308412a0e213f74ce87`.

QR-05DC continues the committed `qr-05-bridge` branch (from QR-05DB commit `da73c39`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
