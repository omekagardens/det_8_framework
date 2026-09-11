# QR-05CY: Observational quotient and internal-reference no-go

10 September 2026 (Pacific/Honolulu). **Executable, DET-instantiated, bounded.**
This gate separates *identifiability* from *empirical applicability*. On a small
declared class of DET-style worlds it computes the observational quotient exactly,
classifies each target as identified or not (with an explicit witness pair), and
instantiates the internal-reference no-go on BW's reference channel. It makes **no
ontological claim**: observational equivalence is not ontological identity
(GOVERNANCE §3 F8-OPEN v2; ONTOLOGY.md §5). Supplied geometry; the apparatus branch
(BX/BW/BZ) remains open.

Follows [QR-05CX](../qr-05cx-lgh-scale-2026-09-10/README.md) and the blocked-gate
review; continues [QR-05BW](../qr-05bw-reference-calibration-design-2026-09-10/README.md).

## 1. The criterion

Let `W` be a declared class of admissible worlds and `O` a declared observational
interface on the DET primitives `(V, ≺, #, L, 𝔇)`. Two worlds are observationally
equivalent, `W1 ~_O W2`, when `O` cannot tell them apart.

- **P1 (factorization).** `τ` is identifiable through `O` iff `τ` is constant on
  every `O`-class — equivalently `τ` factors through `W/~_O`. *(Elementary.)*
- **P2 (internal-reference no-go).** If `W1 ~_O W2` and `τ(W1) ≠ τ(W2)`, then no
  `σ(O)`-measurable function — in particular no reference `r_ref = f(O)` built from
  the same channel — can identify `τ` on `{W1,W2}`. *(Elementary.)*

`τ` is classified **IDENTIFIED** iff every pair with equal observation has equal
target; otherwise **NON_IDENTIFIABLE**, with a witness pair. This is exactly the
criterion the gate evaluates, on fixed, declared constructions — not a parameter
choice.

## 2. The declared world class and the computed classification

| family | interface `O` | target `τ` | verdict | witness |
|---|---|---|---|---|
| dimension (d = 2,3,4) | ordering fraction | dimension | **IDENTIFIED** | — |
| scale (c = 1,2,4) | normalized distances | absolute scale | **NON_IDENTIFIABLE** | scale1, scale2 |
| scale (c = 1,2,4) | normalized distances + anchor | absolute scale | **IDENTIFIED** | — |
| conformal (b = 0, 2; same events, Ω² = 1+b·x) | interval signs (order) | conformal factor | **NON_IDENTIFIABLE** | omega0.0, omega2.0 |
| conformal (b = 0, 2; sprinkled) | binned count density | conformal factor | **IDENTIFIED** | — |

Three findings:

1. **Dimension factors through the quotient** (positive control: the framework is
   not uniformly negative).
2. **Absolute scale does not** (`P3`). Normalized order/count observables are
   invariant under `d → c·d`, so the scale class is a single `O`-class with distinct
   targets; **an independent external anchor is logically necessary**, and adding
   one (`scaled_distance+anchor`) makes the target identified. This re-derives the
   CW/CX free-scale degeneracy as a quotient statement. It is a statement about
   *identifiability*, not about scale being unreal.
3. **The causal order is exactly blind to the conformal factor** (`P4`): the
   conformally flat worlds `Ω² = 1 + b·x` share the same interval signs, so the
   order channel cannot separate `b`; the **count density (marks) identifies it**,
   matching T7's `conformal_invariance_of_order` and `recover_conformal_factor`.

## 3. The internal-reference no-go (BW P5)

On the witness class `{scale1, scale2}` — equal observations, different targets —
every reference constructor `f` in the declared family (mean, max, min, median,
rms, positive fraction; all **functions of `O`**) returns identical values, and by
P2 the same holds for **every** `σ(O)`-measurable reference. So a reference
constructed from the same record channel cannot certify which target is actual.
This closes the **non-empirical half** of the current BW/P5 blockage *negatively*
(the other premise-level results — `conditional_only`, unmet P1–P12 — are
unchanged). It does not supply apparatus evidence, and it does not satisfy P5
physically.

## 4. Blockage taxonomy on the existing registry

The gate records a per-target *blockage kind* — `DATA` (identifiable in principle,
not measured), `CHANNEL` (absent from the declared law; a new observable is
required), `MATH` (needs a theorem, not apparatus), `GAUGE` (invariant freedom) —
and maps each target onto the **existing** `det8.claims` evidence axes
(`CORRESPONDENCE_ONLY`, `NO_EMPIRICAL_SUPPORT`, `BOUNDED_CONDITIONAL_RESULT`, …).
The gate validates that mapping against `det8/claims.py` and introduces **no new
status vocabulary**; adopting the blockage kind into `det8.claims` would be a
governance change through its validator, not this gate.

## 5. Boundaries

An exact, bounded computation on a declared finite world class. It establishes P1,
P2 and their finite instances P3/P4, and the no-go on the declared channel. It does
**not** establish that any `O`-class corresponds to one ontology (P5, Status M), nor
any apparatus fact, metric, continuum limit or gravity. Curvature and the imported
BD operator stay parked; κ-gravity is retired and gravity is standard GR under
Option B. Branch B (BX/BW/BZ) remains `OPEN — PHYSICAL EVIDENCE REQUIRED`.

## 6. Evidence and limits

`primary.py` (tolerant union–find partition) and `reference.py` (rounded canonical
grouping) build the worlds, the observables, the classification and the no-go
independently; the driver compares with a float tolerance and refuses on any
difference. `study.py` writes create-only `results.json` and `source-freeze.json`
(freezing the gate sources, the T7 module and `det8/claims.py` by hash);
`test_qr05cy.py` checks each probe verdict and witness, the no-go, the registry
mapping and the Status-M guard. Fixed seeds make the run deterministic. Limits:
sources ≤ 262,144 bytes, artifacts ≤ 16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
