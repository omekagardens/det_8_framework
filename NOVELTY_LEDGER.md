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
| Recovery-rate discriminator (F9/FL-4): τ_rec(T) T-independent vs Arrhenius | Annealing / defect-density kinetics | `unexecuted` | **cheapest**; κ→defect density, ontology unaffected, one miss |
| Operational κ̂ + L0/L1/L2 ladder | Standard materials metrology | `unexecuted` | none — L0/L1 is unconditional, publishable even if DET false |
| κ-dependent decoherence functional D_κ (three-slit I₃ = κ·r) | Grade-2 (quantum) decoherence functional (Sorkin) | `unexecuted` | existing I₃ ≈ 0 already bounds κ < ε/r; bounds this κ-coupling form, not the lens |
| RET engine (discrepancy adjudication + engine validation) | Methodological | `active` | none — methodological yield, not physics yield |

**Executed probes: 0. Surviving novelties: 0. Generative warrant: `ACTIVE`
(insufficient data to adjudicate).**

## The first push is now registered

**D_κ** (`det8/models/dkappa_decoherence.py`) is formalized: the κ-weighted
convex combination μ_κ = (1−κ)μ₂ + κμ₃ of a grade-2 pair-kernel and a
grade-3 record measure, so I₃(μ_κ) = κ·r. The grade hierarchy supplies the
well-definedness conditions (positivity, normalization); the three-slit bound
|I₃| < ε inverts to κ < ε/r — the anchor. It is a *mechanism*, not a novel
effect: the existing three-slit null already constrains κ and does not falsify
the lens.

## Operating rule

Every generated probe must be registered here with a `target_theory` and a
`cost_if_null` **before** it is used as an explanatory resource. A probe
without a null cost is decoration, not a probe.

**See also:** `FALSIFICATION_LEDGER.md` (per-prediction falsifiers, Class I/II/III),
`GOVERNANCE.md` (DG-WARRANT, decision gates), `novelty_closure.py` (novelty
hierarchy — *what kind* of novelty, distinct from this *productivity* register).
