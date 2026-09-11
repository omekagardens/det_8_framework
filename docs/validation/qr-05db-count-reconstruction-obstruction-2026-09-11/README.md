# QR-05DB: the metric-axiom obstruction for count-only reconstructions

11 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: an impossibility result plus a positive control.** The QR-05DA count
estimator is shown **not** to be a Lorentzian metric (it violates the reverse-triangle
inequality on real sprinklings), no count-only reconstruction can be simultaneously
convergent, positive on links, and axiom-compliant, and the order-only longest-chain
estimator **is** a Lorentzian premetric — though its convergence is the open part.
No metric, continuum, curvature or gravity is claimed.

Follows [QR-05DA](../qr-05da-lgh-convergence-2026-09-10/README.md) and the pre-specified
Next in the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).

## 1. Pre-specification (fixed before the computation)

The steering asked for the following to be specified beforehand; `protocol.json`
fixes the parameters and the report echoes this spec.

- **Question.** Can an order+count reconstruction be constructed with a provable
  vanishing error bound *while satisfying the required Lorentzian metric-space
  properties*?
- **Admissible causal-set class.** Fixed-count iid (Poisson) sprinklings into the
  unit causal diamond of `d`-dimensional Minkowski spacetime, `d ∈ {2, 3}`; plus
  adversarial non-manifoldlike controls (pure chain, random poset, antichain). The
  impossibility result R2 assumes the axioms are required on the *full* causal-set
  class, so pure chains are admissible.
- **Sampling/density.** `n` iid points in the diamond; mean spacing `ℓ = n^{-1/d}`.
- **Reconstruction formula.** Count-only `d(i,j) = ℓ·(m_ij + s)^a`, `m_ij = #{k : i ≺ k ≺ j}`;
  tested forms: **offset** `(s = 1, a = 1/2)` (QR-05DA) and **raw** `(s = 0, a = 1/2)`.
  Order-only: `d = ℓ·L`, `L` the longest-chain length.
- **Scale/anchor.** Homothety only; the absolute scale and reference are
  non-identifiable from the order (QR-05CY).
- **Lorentzian metric axioms.** `A0 d(x,x)=0`; `A1 d(x,y)>0 ⇔ x ≺ y`; `A2 x ≺ y ≺ z ⇒
  d(x,z) ≥ d(x,y) + d(y,z)`.
- **Convergence notion.** Scale-free LGH distortion → 0; pointwise `d_ij → c·τ_ij`.
  The count law is `m ≈ ρ·Vol(I)` with the elementary volume law
  `Vol(I(p,q)) = c_d·d(p,q)^d` (below).
- **Constructive bounds.** A link-triple violation bound (§3); the structural
  superadditivity `m_ac ≥ m_ab + m_bc + 1`.
- **Adversarial controls.** `pure_chain_n8`, `random_poset_n12`, `antichain_n6`.

### The volume law (elementary, used for the convergence exponent)

All Alexandrov intervals with the same Lorentzian distance `d(p,q)` are related by a
Lorentz boost, which has unit determinant and preserves `d`; so `Vol(I(p,q))` is a
function of `d(p,q)` alone. By scaling, `Vol(I(p,q)) = c_d · d(p,q)^d`. Hence in a
Poisson sprinkling of density `ρ`, the intermediate count satisfies
`m ≈ ρ·c_d·τ^d`. This is used only as the convergence scaling; it is not re-derived
here.

## 2. Three estimators, three axiom censuses

For each object and each estimator the gate records the **support** mismatches
(`A1`), the number of causal pairs assigned zero distance, and the **reverse-triangle**
violations over all triples `i ≺ j ≺ k` with the worst gap and a witness.

`support_mism` = pairs where `(d>0) ≠ (i≺j)`; `zero_on_causal` = causal pairs with
`d = 0`; `RT` = reverse-triangle violations / triples.

| object | estimator | support_mism | zero_on_causal | RT violations / triples | worst gap |
|---|---|---|---|---|---|
| sprinkle_d2_n32 | **chain** | 0 | 0 | **0** / 1121 | +0.0000 |
| sprinkle_d2_n32 | count_offset | 0 | 0 | 744 / 1121 | −1.0193 |
| sprinkle_d2_n32 | count_raw | 71 | 71 | 119 / 1121 | −0.6503 |
| sprinkle_d2_n64 | **chain** | 0 | 0 | **0** / 8987 | +0.0000 |
| sprinkle_d2_n64 | count_offset | 0 | 0 | 4511 / 8987 | −1.2042 |
| sprinkle_d2_n64 | count_raw | 197 | 197 | 1131 / 8987 | −0.9294 |
| sprinkle_d3_n32 | **chain** | 0 | 0 | **0** / 166 | +0.0000 |
| sprinkle_d3_n32 | count_offset | 0 | 0 | 49 / 166 | −0.6822 |
| sprinkle_d3_n32 | count_raw | 75 | 75 | 0 / 166 | +0.4142 |
| sprinkle_d3_n64 | **chain** | 0 | 0 | **0** / 940 | +0.0000 |
| sprinkle_d3_n64 | count_offset | 0 | 0 | 286 / 940 | −0.7639 |
| sprinkle_d3_n64 | count_raw | 251 | 251 | 1 / 940 | −0.0863 |
| pure_chain_n8 | **chain** | 0 | 0 | **0** / 56 | +0.0000 |
| pure_chain_n8 | count_offset | 0 | 0 | 56 / 56 | −1.0863 |
| pure_chain_n8 | count_raw | 7 | 7 | 20 / 56 | −0.6968 |
| random_poset_n12 | **chain** | 0 | 0 | **0** / 12 | +0.0000 |
| random_poset_n12 | count_offset | 0 | 0 | 12 / 12 | −0.6822 |
| random_poset_n12 | count_raw | 11 | 11 | 0 / 12 | +0.4142 |
| antichain_n6 | (all three) | 0 | 0 | 0 / 0 | +0.0000 |

## 3. The three-event chain and the minimal violation

`a ≺ b ≺ c` with consecutive links: `m_ab = m_bc = 0`, `m_ac = 1`, `τ_ac = 2`.

| quantity | `d(a,b)` | `d(b,c)` | `d(a,c)` | reverse triangle `d(a,c) ≥ d(a,b)+d(b,c)` |
|---|---|---|---|---|
| directed Lorentzian distance | 1 | 1 | 2 | holds (equality) |
| order-only chain `ℓ·L` | 1 | 1 | 2 | holds (equality) |
| count raw `ℓ·√m` | 0 | 0 | 1 | holds, but link distances are 0 (fails A1) |
| count offset `ℓ·√(1+m)` | 1 | 1 | √2 ≈ 1.414 | **fails: √2 < 2** |

**Constructive link-triple bound.** For a link triple the offset gap is
`ℓ·(√(1+m_ac) − 2)`, which is negative for every `m_ac ≤ 2` and equals `0` only at
`m_ac = 3`. So the offset form provably violates A2 on *any* link triple whose
interval contains at most two points, with gap at least `ℓ(√3 − 2)` (worst
`ℓ(√2 − 2) ≈ −0.586ℓ`).

## 4. Findings

1. **The QR-05DA count estimator is not a metric (R1, unconditional).** `ℓ·√(1+m)` is
   positive exactly on the causal relation but violates A2 on every sprinkling and
   non-degenerate control tested (up to ~50% of triples at `d = 2, n = 64`). It is a
   distance *estimator*, not a Lorentzian metric.
2. **No count-only reconstruction can be convergent, positive and axiom-compliant
   (R2, conditional impossibility).** With the elementary volume law, convergence
   forces the exponent `a = 1/d` and forces `g(m)/m → 0`. But positivity on links
   (`g(0) > 0`) plus A2 on the admissible chains forces `g` to grow **at least
   linearly** (`liminf g(m)/m ≥ g(0) > 0`). The two are incompatible for `d ≥ 2`. The
   raw form `ℓ√m` evades the positivity branch only by having `g(0) = 0` — i.e. by
   failing A1. (See RESULTS.md for the proof.)
3. **The order-only longest-chain estimator is a Lorentzian premetric (R3,
   unconditional).** `ℓ·L` satisfies A0–A2 on every finite causal set (longest chains
   concatenate: `L(x,z) ≥ L(x,y)+L(y,z)`), verified exactly on all objects. But
   QR-05DA shows its scale-free ceiling does not vanish.
4. **The count is structurally superadditive (R4).** `I(a,b) ⊔ I(b,c) ⊔ {b} ⊆ I(a,c)`,
   so `m_ac ≥ m_ab + m_bc + 1` (0 violations over 11 282 triples); this is the
   mechanism behind the trade-off, and it is *not* enough to rescue A2 once positivity
   forces an offset.

**Consequence for the steering's question.** A count-only reconstruction cannot be
the axiom-compliant convergent object. The axiom-compliant route is **order-based**;
whether an order-based or **mixed** order+count reconstruction has a provable
vanishing bound remains open.

## 5. Boundaries

A bounded computation on supplied geometry and finite causal sets. It states and
machine-verifies the finite witnesses of an obstruction; it does **not** prove the
convergence or non-convergence of any reconstruction (the volume law is used as
imported scaling), does not establish manifoldlikeness, and makes no metric,
continuum, curvature, dynamics or gravity claim. Curvature and the imported BD
operator stay parked; κ-gravity is retired and gravity is standard GR under Option B.

## 6. Evidence and limits

`primary.py` (forward source chains, set-intersection counts, direct triple census)
and `reference.py` (backward intermediate-node chains, bitmask counts, recoded
census) build the estimators, both censuses, the structural lemma and the report
independently; the driver compares with a float tolerance and refuses on any
difference. `test_qr05db.py` (12 tests) pins the census with known-answer checks on
hand-built three-chains and a strict-superadditivity poset, and asserts the
flags/verdict. `study.py` writes create-only `results.json` and `source-freeze.json`.
Fixed seeds make the run deterministic. Limits: sources ≤ 262 144 bytes, artifacts
≤ 16 777 216 bytes. Decision record: [RESULTS.md](RESULTS.md).
