# QR-05BW decision record

10 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone contract](README.md) now specifies what independent
reference information and same-population transfer assumptions could
justify the systematic distortion allowance that BU consumes. This gate ran
no mathematical engine, test suite, calibration procedure, source/capture
freeze, device choice or acquisition. Its displayed statements are
analytical derivations and an interface specification, not a calibrated
measurement.

## Main result

BU requires a supplied bound `e ≥ ||r−q(θ_true)||∞` but provides no
procedure for it. BW decomposes that single claim into two logically
distinct claims and composes them exactly:

```text
e* = ||r − q(θ_true)||∞
   ≤ ||r − r_ref||∞ + ||r_ref − q(θ_true)||∞
   ≤ d + a =: e_cal.
```

- `G_a = {||r_ref − q(θ_true)||∞ ≤ a}` is **reference validity**: the
  reference really realizes the same ideal geometry on the same marks.
- `G_d = {||r − r_ref||∞ ≤ d}` is **same-population transfer**: the record
  population agrees with the reference population.

On `G_a ∩ G_d`, `e_cal` is a valid allowance in BU's sense, so BU's
enlarged inverse and separation certificate consume it unchanged. The
composition is the deterministic triangle inequality
`G_a ∩ G_d ⊆ G = {e* ≤ e_cal}`; no independence or distributional premise
is used.

The probability composition is likewise a union bound with no
independence. With BU's sampling event `E` of budget `α` and allowance
sub-budgets `β_ref`, `β_tr`,

```text
P(Gᶜ) ≤ β_ref + β_tr =: β,        P(E ∩ G) ≥ 1 − α − β.
```

The product `(1−α)(1−β)` does **not** follow from marginal bounds alone.

A statistical allowance uses a prespecified envelope `e_max` with
`P(e_cal>e_max) ≤ β_env` and BU's every-batch certificate
`s = D(B) − 2 e_max − 2h > 0`, `n s² ≥ 10`. On the intersection of the
coverage, validity, envelope and certificate events,

```text
P(correct singleton) ≥ 1 − α − β − β_env,
P(wrong target | singleton) ≤ α + β + β_env.
```

A deterministic valid allowance has `β=0` and consumes separation only,
recovering BU's original statement.

## What the analytical controls distinguish

| Control | Removed or changed | Consequence |
|---|---|---|
| C1 | `G_a` dropped: `a_sys` unjustified | `e_cal` unbounded; perfect record–reference fit gives no bound |
| C2 | Transfer dropped: `d` undefined | `G_d` unproved; composition void |
| C3 | Support/nesting violated | Inherited BU negative control: marginal `e=0` holds but `P(10)>0` |
| C4 | Marks or target redefined between channels | `G_d`, `G_a` compare different objects |
| C5 | Same records for calibration and report | Marginal `α+β` unproved; joint theorem required |
| C6 | Repeat-until-pass, `K` unbounded | No R3 bound; selection defect |
| C7 | Report only accepted `H`, ignore `P(H)` | Conditional reliability misread as `1−α−β` |
| C8 | Reference chooses the family it validates | Hidden multiplicity; `β_ref` not marginal |

**Corollary (close fit is insufficient).** With perfect agreement `d=0`
the allowance is `e_cal=a`, so the certified distortion can never be
bettered below the reference-validity error `a`. If `a_sys` is unbounded or
unjustified, `e_cal` is unbounded however well the record fits the
reference. This is the precise sense in which "a close fit to production
records does not identify the true ideal world."

**Selection-aware composition.** Three regimes replace a single
unconditional claim:

```text
R1 (no selection):  P(correct) ≥ 1 − α − β.
R2 (fixed H):       P(correct) ≥ max(0, P(H) − α − β),
                    P(correct | H) ≥ 1 − (α+β)/P(H),   P(H) > 0.
R3 (≤K repeats):    reported-allowance budget ≤ Kβ.
```

Reporting only accepted calibrations must divide the failure budget by
`P(H)`; the unconditional guarantee is not inherited by the accepted
subpopulation. Passing a selected budget check is a different event from
allowance validity, and `H` alone never yields an accepted-batch
guarantee. Data-dependent stopping needs a sequential/optional-stopping
argument that a bare repeat-until-pass rule does not supply.

## Statistical certificate and evidence interface

A statistical allowance must be backed by a joint `(1−β)` confidence
region for `(r, r_ref)` in the nested triangle `S`, not by coordinatewise
intervals, with marginal validity `P(G_{a,stat}ᶜ) ≤ β_ref` and
`P(G_{d,stat}ᶜ) ≤ β_tr`. If the same records also supply the reported
counts, a joint theorem is required because the fixed-law premise may not
survive; if the reference selects the family it then validates, the
selection needs its own multiplicity control. BW fixes this interface and
supplies no numeric `β`, `a_stat`, `d_stat` or `e_max`.

The auditable interface records the ideal model, record channel,
reference, transfer, allowance, consumer, a per-premise
`supplied`/`unmet` status list, the composed guarantee, and a
`conditional_only` flag. Every load-bearing premise P1–P12 is currently
**unmet**, including the two that no record fit can supply: reference
validity (P5) and independence or a joint theorem (P11), and the
support/nesting premise (P8) that marginal agreement cannot certify. Any
unmet load-bearing premise forces `conditional_only = true`.

## Applicable value and boundaries

The calculus now separates four limitations that were previously
conflated:

- finite-sample uncertainty in the record experiment (`α`);
- grid rounding, a computational enclosure;
- systematic record-to-ideal distortion, now split into an independent
  reference-validity claim `a` and a same-population transfer claim `d`;
- allowance validity and acceptance/selection (`β`, `H`, regimes R1–R3).

The contract states which ideal target is estimated, which populations are
compared, and which assumptions bridge them. It does not supply a
reference, a calibration method, a device, a general metric or gravity
dynamics. No RET integration or application readiness is inherited. The
ideal family, density bound, fixed marks, nested iid attempt law and
no-unmodeled-loss premises remain essential, and the BU negative control
against marginal-only support certification carries over unchanged. At
`e_cal=0` the construction reduces to BU's `e=0` projection; no absolute
scale is identified.

## Review and next gate

Independent analytical review checked the triangle composition and its
worst-case tightness, the reference/transfer split and the roles of
`a_sys,d_sys` versus `a_stat,d_stat`, the union-bound composition without
independence, the envelope and every-batch certificate, and the R1–R3
selection bounds including the conditional-`H` division and the `K`-repeat
budget. Review also confirmed that the interface retains unmet premises
and that no record-fit argument can supply P5, P8 or P11.

Accept BW as the design checkpoint. The program owner directed that the
next gate, **QR-05BX**, be the apparatus-to-event interface design. The
reference-calibration composition verification proposed here is
**deferred, not rejected**: if revived it would verify Proposition 1 and
Corollaries 1–2, the Proposition 2 union bound, regimes R1–R3 and their
boundary controls, and the Section 9 schema round-trip, with the Section 10
controls as negative checks. It must not acquire data, model a device,
produce a numerical `β`, sweep a fixture bank or tune a quota, and every
result stays conditional on P1–P12. If no independent reference or
defensible transfer premise is supplied, the program stops at this
conditional contract and does not promote apparatus or
geometric-identification readiness.

## Provenance and publication

BW began from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on authoritative branch `ret`.
No BV source, freeze or capture was modified or re-executed; the BV first
capture remains 100,522 bytes, SHA-256
`44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`, and
BU's README/RESULTS remain the authenticated design record.

Publication is only this decision record, [README.md](README.md), and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
application work and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
