# DET v8.0 — Novelty Ledger

**The register of the lens's productivity — the falsification surface for DET *as an instrument*.**

DET is a lens for generating falsifiable probes against target theories, not a
ToE. The ontology is chosen, not evidenced; it cannot be falsified. What *can*
be falsified is whether the lens's probes produce surviving novelties above the
null rate. This ledger records that, one probe at a time.

**Implementation:** `det8/models/novelty_ledger.py`

## Schema

Every probe is registered as:

| Field | Meaning |
|---|---|
| `probe` | The generated falsifiable probe (what is measured) |
| `target_theory` | The standard theory it discriminates against |
| `status` | `gated` · `unexecuted` · `executed` · `active` |
| `outcome` | `null` · `surviving_novelty` (only when `executed`) |
| `cost_if_null` | What a null result costs the **instrument** (not the ontology) |

`outcome` and `cost_if_null` are the load-bearing columns: a null probe costs
the ontology nothing, but it costs the lens one logged miss.

## Generative warrant (DG-WARRANT)

The lens's generative warrant is derived, not asserted:

> After `downgrade_after` executed probes with **zero** surviving novelties,
> the generative warrant downgrades (`ACTIVE → DOWNGRADED`). A surviving
> novelty sustains it (`SUSTAINED`).

This is the DG-gate pattern applied to the instrument rather than to a claim.
It replaces the old demand for kill criteria on metaphysical claims — which,
under the lens framing, was aimed at the wrong object.

## Current contents

| Probe | Target | Status | cost-if-null |
|---|---|---|---|
| Clock anomaly (FL-1): Δν/ν = λ_P·κ/(1+λ_P·κ) | Standard physics (null clock universality) | `gated` | one miss; λ_P·Δκ product bound only (prerequisites missing) |
| Recovery-rate discriminator (F9/FL-4): τ_rec(T) T-independent vs Arrhenius | Annealing / defect-density kinetics | `unexecuted` | literature (densified silica, E_a = 2.64 eV) predicts the Arrhenius null; no (T, τ) data ingested |
| Operational κ̂ + L0/L1/L2 ladder | Standard materials metrology | `unexecuted` | none — L0/L1 is unconditional, publishable even if DET false |
| κ-dependent decoherence functional D_κ (three-slit I₃ = κ·r) | Grade-2 (quantum) decoherence functional (Sorkin) | `executed` → `null` | κ_DET·r/I₂_ref(DET) < ε_exp ≈ 10⁻⁴ (r free; I₂_ref is a model convention, not the experimental I₂) — consistent with standard QM |
| RET engine (discrepancy adjudication + engine validation) | Methodological | `active` | none — methodological yield, not physics yield |

**Executed probes: 1. Surviving novelties: 0. Generative warrant: `ACTIVE`
(one logged miss, below the downgrade run).**

## The first push is now executed

**D_κ** (`det8/models/dkappa_decoherence.py`) is formalized and now pushed
against standard quantum mechanics: the κ-weighted convex combination
μ_κ = (1−κ)μ₂ + κμ₃ of a grade-2 pair-kernel and a grade-3 record measure, so
I₃(μ_κ) = κ·r. The grade hierarchy supplies the well-definedness conditions
(positivity, normalization); standard QM is grade-2 (I₃ = 0), and the
published three-slit bounds invert through the normalization
κ_Sorkin = I₃/I₂_ref = κ_DET·r/I₂_ref to a concrete bound

    κ_DET · r < ε_exp · I₂_ref(DET),

i.e. the invariant **κ_DET·r / I₂_ref(DET) < ε_exp ≈ 10⁻⁴**. I₂_ref(DET) is a
model convention (a seed-dependent toy pair-kernel, not the experimental I₂),
so this bounds the product κ_DET·r, not κ_DET alone. The outcome is **null**:
κ_DET is consistent with zero, so the lens logs its first miss.

## The three κ channels

κ couples through three *independent* channels, with very different status:

| Channel | Coupling | Bound | Status |
|---|---|---|---|
| **Static** interference (D_κ) | κ_static·w₃ | κ_static·w₃/I₂_ref(DET) < 10⁻⁴ (three-slit) | **closed** — null, first logged miss |
| **Clock** (FL-1) | λ_P·κ | ≲ 10⁻¹⁸ (Lange 2021) | **executed null** — product bound; λ_P unconstrained |
| **Recovery** (F9) | κ_dyn (τ_rec) | — | **unexecuted** — literature reference (E_a = 2.64 eV); no data ingested |

The static channel is closed. The clock and recovery channels are *dynamical*
(κ in the time-evolution), invisible to the three-slit null, and remain the
open frontier.

## Operating rule

Every generated probe must be registered here with a `target_theory` and a
`cost_if_null` **before** it is used as an explanatory resource. A probe
without a null cost is decoration, not a probe.

**See also:** `FALSIFICATION_LEDGER.md` (per-prediction falsifiers, Class I/II/III),
`GOVERNANCE.md` (DG-WARRANT, decision gates), `novelty_closure.py` (novelty
hierarchy — *what kind* of novelty, distinct from this *productivity* register).
