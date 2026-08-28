# Findings — Pushing standard QM through D_κ to a concrete κ-bound

**Date:** August 27, 2026
**Commit:** `ea85fd0`
**Probe:** the κ-dependent decoherence functional D_κ (`det8/models/dkappa_decoherence.py`)
**Ledger status:** `executed → null` (the lens's first logged miss)

## The result in one line

Standard quantum mechanics is grade-2 (Sorkin), so its third-order interference
vanishes: I₃ = 0. D_κ predicts I₃ = κ_DET·r. The published three-slit bounds on
the normalized Sorkin parameter κ_Sorkin = I₃/I₂_ref invert through D_κ to

> **κ_DET · r < ε_exp · I₂_ref**

giving a concrete bound **κ_DET ≲ 1.5×10⁻⁵** (Kauten 2017, r = 1), or
conservatively κ_DET ≲ 5.8×10⁻⁵ (Vogl 2021 central value).

## What was done

D_κ = (1−κ)·μ₂ + κ·μ₃ is the κ-weighted convex combination of a grade-2
pair-kernel (Sorkin decoherence functional, I₃ = 0) and a grade-3 "record"
measure carrying a single triple weight r. Linearity gives I₃(μ_κ) = κ·r.
Normalizing by the pairwise reference I₂_ref reproduces the experimental Sorkin
parameter, and the published bound inverts to a bound on κ_DET·r.

## Concrete bounds (r = 1, I₂_ref = 0.146 for the default pair-kernel)

| Experiment | κ_Sorkin bound | κ_DET bound |
|---|---|---|
| Sinha et al. 2010 (*Science* 329, 418) | < 10⁻² | < 1.5×10⁻³ |
| Kauten et al. 2017 (*NJP* 19, 033017) | < 10⁻⁴ | **< 1.5×10⁻⁵** |
| Vogl et al. 2021 (*PRR* 3, 013296) | (3.96 ± 5.23)×10⁻⁴ | < 5.8×10⁻⁵ |

## What this establishes

1. The lens produced a real, experimentally-constrained number — the first
   physics-facing output that is quantitative and falsifiable rather than
   interpretative.
2. The null is the deliverable, and the machinery absorbed it correctly: the
   ontology is untouched (chosen, not evidenced); the instrument logs its first
   miss. DG-WARRANT reads **1 executed / 0 surviving → `ACTIVE`**.
3. The bound is strong where the ansatz is strong: within the single grade-3
   record-term coupling, static third-order interference is excluded to ~10⁻⁵.

## What this does NOT establish

- **Not the ontology** — Track B never required κ ≠ 0 in this channel.
- **Not κ in general** — this bounds κ via *one* coupling ansatz; the F9
  (recovery-rate) and FL-1 (clock) channels are untouched.
- **Not κ_DET alone** — the bound is on the product κ_DET·r; r is free.
- **Not dynamical κ** — the three-slit test is a *single-time (static)*
  measurement of the decoherence functional. It is blind to κ entering the
  time-evolution (the "law map L"), which is where the clock and recovery-rate
  probes look. This is consistent with the almost-quantum framing: the static
  level being exactly quantum is expected; any κ-dynamics live in the time axis.

## What this implies / needs further work

1. **Generalize the coupling beyond the single grade-3 ansatz.** The null is
   "κ does not couple via this grade-3 term"; to claim "κ does not couple to
   any higher-order interference," characterize the general grade-k (k ≥ 3)
   coupling. The certificate flags the grade-3 choice as "not derived here."
2. **Fix r, or the bound stays soft.** κ_DET·r < ε_exp·I₂_ref is a product
   bound (the same structure as the clock's λ_P·Δκ). A bound on κ_DET alone
   needs a theoretical constraint on r.
3. **State the invariant, not the specific number.** The robust claim is
   κ_DET·r/I₂_ref < ε_exp ≈ 10⁻⁴; the 1.5×10⁻⁵ uses the default pair-kernel's
   I₂_ref = 0.146.
4. **Move to the dynamical channels.** The next cheap step is F9 on real R(t)
   (the dry run proves the discriminator works; it is still blocked on data),
   then FL-1 once the F9 gates clear.
5. **Make the static/dynamical distinction explicit in the Model Card**, to
   prevent over-reading the null.

## Provenance

| Claim | Status |
|---|---|
| I₃ = 0 for grade-2 | MATH — Sorkin decoherence functional |
| I₃ = κ_DET·r under D_κ | TH-DET — the κ-coupling hypothesis |
| κ_Sorkin = I₃/I₂_ref | MATH — normalization |
| experimental \|κ_Sorkin\| bound | EXPERIMENT — Sinha 2010, Kauten 2017, Vogl 2021 |
| bound on κ_DET | CONDITIONAL — on the D_κ ansatz and the record-term weight r |

## Update — item 1 addressed (general grade-k coupling)

The single-triple ansatz is now generalized. `Grade3Measure` and `DkappaGrade3`
in `dkappa_decoherence.py` carry arbitrary triple weights w₃(i,j,k), with

    I₃({a},{b},{c}) = κ_DET · w₃({a,b,c})   (for every triple)

so the three-slit bound constrains κ_DET·w₃ for every triple, and the tightest
κ-bound uses the largest triple weight: **κ_DET < ε_exp·I₂_ref / max w₃**.

Two honest consequences:

1. **The r = 1 single-triple case is the *tightest* bound** (κ_DET < 1.5×10⁻⁵).
   Any spread of the record weight over more triples lowers max w₃ and therefore
   *weakens* the κ-bound (e.g. uniform over 4 triples gives κ_DET < 5.8×10⁻⁵).
   So the headline number is the optimistic limit, not the general one.
2. **Grade-k > 3 is also bounded.** Kauten 2017 used a 5-path interferometer,
   which bounds I₃, I₄, and I₅ simultaneously, so κ-coupling to grade-4 and
   grade-5 record terms is bounded at the same ~10⁻⁴ level; only couplings of
   grade ≥ 6 escape a 5-path experiment.

The remaining weak point is unchanged: the bound is on κ_DET·w₃, so it still
needs the record-weight distribution to be fixed (item 2).
