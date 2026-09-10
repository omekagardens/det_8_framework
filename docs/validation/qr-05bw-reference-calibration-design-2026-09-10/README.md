# QR-05BW: reference-calibration admissibility contract

10 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This sheet specifies what independent reference information and
same-population transfer assumptions could justify the systematic
distortion allowance that BU consumes, and what must remain conditional
when they are not supplied. It executes no mathematical engine, test
suite, calibration run, source/capture freeze, device choice or physical
acquisition. The displayed statements are analytical derivations and an
interface specification, not measured calibration.

Continue the verified [BV decision](../qr-05bv-acquisition-distortion-verification-2026-09-09/RESULTS.md)
without changing its frozen sources, first capture, quota or grid.

## 1. The gap BU left explicit

BU's main theorem uses a prospectively supplied deterministic allowance

```text
||r − q(θ_true)||∞ ≤ e,        δ_true ∈ B,
```

and its conditional extension uses the event `G = {||r − q(θ_true)||∞ ≤ e_cal}`
with `P(Gᶜ) ≤ β`. BU supplies no procedure that produces or validates such
an allowance, and its analytical review retained that explicitly. A close
fit between production frequencies and a model prediction is not that
procedure: it constrains agreement between two observable summaries, not
the distance from the record population `r` to the unobserved ideal point
`q(θ_true)`.

BW closes the specification gap, not the evidential gap. It

1. decomposes the required claim into two logically distinct claims;
2. composes them into an allowance `e_cal` by an exact triangle relation;
3. states the coverage, allowance-validity and acceptance events and
   composes their probabilities by a union bound;
4. fixes what a statistical allowance certificate must supply; and
5. returns an auditable evidence/assumption interface whose unmet premises
   stay visible.

If no independent reference and no defensible transfer premise are
supplied, the contract remains conditional and no apparatus,
geometric-identification or gravity readiness is promoted. This is the
outcome BU's review anticipated.

## 2. Notation and the calibration target

The ideal model is BU's, unchanged. With auxiliary null coordinates
`u,v`, signature `(+,−)`, supplied marks `Q=(0,1)²`, `I₁=(0,1/2)²`,
`I₂=(0,3/4)×(0,1/2)`, and density family parameter `δ`, the ideal point is

```text
q(θ) = (q₁(θ), q₂(θ)) ∈ S,      θ = (η, δ),
S = {(x₁,x₂): 0 ≤ x₁ ≤ x₂ ≤ 1},
```

the ideal target is `τ(η)`, equal to `1/4` for `η=0` and `17/80` for
`η=1`, and `B` is the externally supplied density interval containing
`δ_true`. The actual record population is `r ∈ S`; `n` iid paired attempts
have the nested law `π(r) = (1−r₂, r₂−r₁, 0, r₁)`. Write

```text
e* = ||r − q(θ_true)||∞
```

for the true (unobserved) distortion. BU's theorem needs a supplied `e`
with `e* ≤ e`; BW's object is exactly such an `e`.

Introduce a reference characterization: a population point `r_ref ∈ S`, a
nonnegative accuracy claim `a`, and the event that the reference realizes
the ideal,

```text
G_a = {||r_ref − q(θ_true)||∞ ≤ a}.
```

Introduce a same-population transfer claim `d` and event

```text
G_d = {||r − r_ref||∞ ≤ d}.
```

Both `r_ref` and `a` are supplied by the reference procedure; `d` is
supplied by the transfer argument. None of `r`, `r_ref`, `q(θ_true)` or
`θ_true` is observable as hidden truth. The two claims `G_a` and `G_d` are
the decomposition BW composes.

## 3. Independent reference truth

A reference is a procedure, independent of the record attempts, that
returns `(r_ref, a)` and asserts `G_a`. "Independent" here means:

- its generating data and its validity argument do not use the record
  attempts; and
- it does not presuppose the correctness of the record channel.

Independence is not a distributional statement; it is what lets `β_ref`
and the transfer budget below be composed by a union bound without a joint
dependence model. If the reference is derived from the same records, the
two events are not separately certifiable by the same data and a joint
validity theorem is required instead (Section 7).

`G_a` bounds the distance from the reference population to the ideal
model point. This is a *reference-validity* or *model-mapping* claim: it
says the reference realizes the same ideal geometry on the same marks, up
to `a`. It is not something the record comparison can measure, because
`q(θ_true)` is not observed by either channel.

The reference accuracy separates into a systematic and a statistical part,

```text
a = a_sys + a_stat,
G_a  ⊇  {||r_ref^∞ − q(θ_true)||∞ ≤ a_sys} ∩ {||r_ref − r_ref^∞||∞ ≤ a_stat},
```

where `r_ref^∞` denotes the reference population limit. `a_sys`
(reference mapping/systematic validity) is a *premise*: it is justified by
traceability, an independently validated model, or an engineering
argument, and it consumes no probability allocation. `a_stat`
(reference finite-sample radius) is a statistical quantity with its own
event `G_{a,stat}` and budget `β_ref = P(G_{a,stat}ᶜ)`.

A reference that merely reports a population close to the observed record
frequencies addresses `G_d` and is silent about `G_a`. It cannot establish
`a_sys`, and a model fitted to the records that are being validated is not
an independent reference at all.

## 4. Same-population transfer

The transfer claim `d` bounds `||r − r_ref||∞`. Its population limit part
is a premise set, not an estimate:

1. **Coordinate and mark correspondence.** The reference reports the same
   four cells on the same marks `Q, I₁, I₂` in the same `(x₁,x₂)`
   coordinates. A different parameterization contributes a known or
   bounded mapping error to `d_sys`.
2. **Target identity.** The reference reports the same ideal target `τ`,
   not a redefined instrument-specific quantity.
3. **Same ensemble.** Reference and record are populations of the same
   stationary physical ensemble over the comparison window.
4. **Pairing.** Either the comparison is marginal in the common frame, or
   each record attempt is associated with its reference counterpart; an
   undefined or inconsistent pairing invalidates the paired statistic.
5. **Support and loss.** No unmodeled loss, postselection or channel-specific
   deletion; any such effect is bounded and included in `d_sys`.
6. **Stationarity and iid.** The population is fixed and attempts are iid
   over both windows; drift breaks the common-`r` premise (BU's iid
   premise is not inherited by the transfer argument).

As with `a`, write

```text
d = d_sys + d_stat,
G_d  ⊇  {||r^∞ − r_ref^∞||∞ ≤ d_sys} ∩ {||r − r^∞||∞ + ||r_ref − r_ref^∞||∞ ≤ d_stat},
```

with `r^∞` the record population limit. `d_sys` (engineering/systematic
agreement) is a premise; `d_stat` (joint finite-sample radius of the
record and reference populations) is statistical with budget
`β_tr = P(G_{d,stat}ᶜ)`.

A deterministic engineering bound may replace `d_stat` entirely
(`β_tr = 0`); conversely a purely empirical agreement radius supplies only
`d_stat`. The two are not interchangeable without stating which is in use.

## 5. The composition lemma

**Proposition 1 (triangle composition).** On `G_a ∩ G_d`,

```text
e* = ||r − q(θ_true)||∞
   ≤ ||r − r_ref||∞ + ||r_ref − q(θ_true)||∞
   ≤ d + a =: e_cal.
```

Hence `G_a ∩ G_d ⊆ G = {e* ≤ e_cal}`.

The bound is tight in the worst case: if `r_ref` lies between `r` and
`q(θ_true)` along the extremal coordinate, equality holds. No probabilistic
assumption is used; Proposition 1 is a deterministic consequence of the
norm triangle inequality.

**Corollary 1 (close fit is insufficient).** Fix `a`. If the record and
reference agree in the limit, `d=0`, then `e_cal = a` and `e* ≤ a` cannot
be improved below the reference-validity error. If `a_sys` is unbounded or
unjustified, `e_cal` is unbounded however well the record fits the
reference. Perfect observable agreement is therefore consistent with an
arbitrarily large record-to-ideal distortion.

**Corollary 2 (allocation split).** With the decompositions of Sections 3
and 4,

```text
e_cal = (a_sys + d_sys) + (a_stat + d_stat),
```

where the first bracket is deterministic (given the premises) and the
second is statistical. A purely deterministic valid allowance has `β=0`
and consumes separation only, matching BU. A statistical allowance has
`β = β_ref + β_tr > 0` and changes the conservative error allowance from
`α` to `α+β`.

BU's consumption rule is unchanged: `e_cal ≥ e*` on `G_a ∩ G_d`, so
substituting `e_cal` for BU's `e` is exactly what BU's enlarged inverse and
separation certificate require. BW is a producer of `e`; BU/BV are its
consumers.

## 6. Coverage, validity and acceptance events

Keep BU's fixed design `n=65536`, `m=256`, `h=1/m`, `α=1/20`, four equal
tail allocations `ε=1/80`, and BU's sampling event

```text
E = {r ∈ C(K)},              P_r(E) ≥ 1−α,
```

which is valid for every actual `r∈S` and uses no independence between the
two questions.

Add the allowance events `G_a`, `G_d`, `G = {e* ≤ e_cal}` from Section 5,
and an optional declared **acceptance event** `H` internal to the
calibration pipeline (for example a prespecified budget check). Let `H` be
measurable in the calibration data; it need not be independent of `G`.

**Proposition 2 (union composition, no independence).** For any events
with `P(Eᶜ) ≤ α`, `P(G_aᶜ) ≤ β_ref`, `P(G_dᶜ) ≤ β_tr`,

```text
P(Gᶜ) ≤ P(G_aᶜ) + P(G_dᶜ) ≤ β_ref + β_tr =: β,
P(E ∩ G) ≥ 1 − α − β.
```

The product `(1−α)(1−β)` does not follow from marginal bounds and requires
independence that is not assumed here.

**Separation envelope.** `e_cal` is random in the statistical route. Use a
prespecified envelope `e_max` with `P(e_cal > e_max) ≤ β_env` and BU's
every-batch certificate at `e_max`,

```text
s = D(B) − 2 e_max − 2 h > 0,        n s² ≥ 10.
```

This is a deterministic width certificate (BU Section 5): with `e_max`
fixed before acquisition, the condition `C★ = {s > 0 and n s² ≥ 10}`
either holds or fails independently of the realized counts. On
`E ∩ G_a ∩ G_d ∩ {e_cal ≤ e_max}`, provided `C★` holds, BU's transfer gives

```text
P(correct singleton) ≥ 1 − α − β − β_env,
P(wrong target | singleton) ≤ α + β + β_env.
```

Absorb `β_env` into `β` and the statements are exactly BU's with `e`
replaced by `e_cal`. Substituting a realized favorable width alone remains
insufficient, as in BU.

**Acceptance and selection.** With a declared `H`:

```text
P(correct singleton) ≥ max(0, P(H) − α − β),                 (R2, unconditional)
P(correct singleton | H) ≥ 1 − (α+β)/P(H),   P(H) > 0.       (R2, conditional)
```

So reporting only accepted calibrations must divide the failure budget by
`P(H)`; the unconditional guarantee is not inherited by the accepted
subpopulation. Passing a selected budget check is not the same event as
`G`, and `H` alone never yields an accepted-batch guarantee.

**Repetition.** If the procedure repeats up to a prespecified `K` times
and reports the first accepted allowance, and each repeat's validity event
has budget `β`, a union bound over repeats gives an effective budget at
most `Kβ`:

```text
P(reported allowance invalid) ≤ Σ_{k≤K} P(G_kᶜ) ≤ Kβ.        (R3)
```

Data-dependent stopping requires a sequential/optional-stopping argument
instead; a naively unbounded repeat-until-pass rule has no such guarantee.

Regimes R1 (no selection, bound `1−α−β`), R2 (fixed acceptance) and R3
(prespecified finite repetition) are the selection-aware compositions.

## 7. Statistical allowance certificate: required form

A statistical `e_cal` must be backed by a certificate the contract does not
invent:

- **Jointness.** A joint `(1−β)` confidence region for `(r, r_ref)` in the
  nested triangle `S`, from paired or independent samples, from which
  `d_stat` follows by an explicit deterministic map. Coordinatewise
  intervals are not the nested triangle, and a paired comparison is not
  two independent single-population intervals unless that is proved.
- **Marginal validity.** `P(G_{d,stat}ᶜ) ≤ β_tr` and
  `P(G_{a,stat}ᶜ) ≤ β_ref` each hold marginally over the actual law; the
  union bound then needs nothing further.
- **No fixed-law leakage.** If the same records supply both a calibration
  statistic and the reported `K_i`, the joint law of the two events is not
  the product of their marginal bounds; a joint theorem is required, and
  the fixed sampling law and procedure must not silently change.
- **Model selection.** If the reference is also used to select the ideal
  family `η`, the density bound `B`, or the marks, that selection needs its
  own multiple-comparison control; using the reference to choose and then
  to validate the same family invalidates a bare marginal `β_ref`.

BW supplies the interface and the composition, not a bound. Any numeric
`β_ref`, `β_tr`, `a_stat`, `d_stat` or `e_max` is a property of a future
procedure, not a result of this gate. No numerical calibration allocation,
grid, or quota tuning is performed or implied here.

## 8. Premises interface

Every load-bearing premise is listed separately with its status. None is
supplied by this gate.

| # | Premise | Status | If unmet |
|---|---|---|---|
| P1 | Ideal family complete: `θ_true=(η_true,δ_true)` in the declared family | Unmet | `q(θ_true)` is not in the model; no target or separation is defined |
| P2 | Density premise `δ_true ∈ B` | Unmet | Enlarged inverse over `B` need not contain `q_true` |
| P3 | Mark identity `Q, I₁, I₂` true and unchanged across channels | Unmet | Coordinates differ; `d` is undefined |
| P4 | Target meaning: reference reports the same `τ` | Unmet | Reference and record answer different questions |
| P5 | Reference validity `||r_ref^∞−q_true||∞ ≤ a_sys`, independently justified | **Unmet (unsupplied)** | `G_a` unproved; `e_cal` unbounded by Corollary 1 |
| P6 | Same stationary ensemble and coordinate correspondence | Unmet | Transfer premise void; `d` not comparable |
| P7 | Defined attempt pairing (or marginal comparison in the common frame) | Unmet | Paired `d_stat` certificate undefined |
| P8 | Support/nesting `r ∈ S`, `P(10)=0` | Unmet | Marginal fit cannot certify it (BU negative control) |
| P9 | Iid/stationarity: fixed `r`, iid attempts over both windows | Unmet | BU's and BW's sampling statements both fail |
| P10 | No unmodeled loss/postselection in either channel | Unmet | Population changes; `a_sys`, `d_sys` inapplicable |
| P11 | Reference independent of record attempts, or a joint theorem supplied | Unmet | `α+β` composition unproved (Section 7) |
| P12 | Fixed `n,m,α,ε,β_ref,β_tr,e_max` before acquisition | Unmet | Selection/optional-stopping defects (R2/R3) |

Rule: if any load-bearing premise is unmet, the guarantee of Section 6 is
a conditional contract only. A passing arithmetic score cannot repair a
false or missing premise. In particular P5 and P11 are not implied by any
record fit, and P8 is not implied by marginal agreement.

## 9. Auditable evidence/assumption interface

The interface is a serializable record with native types, one reference
per admitted world, and explicit status flags. Its required fields:

```text
{
  "ideal_model":   { theta_family, marks, tau, B },
  "record_channel":{ n, m, alpha, tails, E, pairing },
  "reference":     { id, independent, r_ref, a_sys, a_stat, beta_ref, G_a },
  "transfer":      { d_sys, d_stat, beta_tr, G_d, ensemble, marks_match },
  "allowance":     { kind: "deterministic"|"statistical", a, d,
                     e_cal, e_max, beta_env, beta },
  "consumer":      { enlarged_inverse_rule, d_class, s, n_s2, H },
  "premises":      [ { id, statement, status: "supplied"|"unmet",
                       owner, evidence } ],
  "guarantee":     { coverage: "1-alpha-beta",
                     correct_singleton, conditional_on_H,
                     regimes: {R1, R2, R3}, caveats },
  "stop":          { conditional_only, reasons }
}
```

Consistency requirements: the reported target set is BU's discrete target
set, not a hull; `e_cal`, `a`, `d` satisfy Section 5 with the same units as
`q`; `β = β_ref + β_tr + β_env`; any `unmet` load-bearing premise forces
`stop.conditional_only = true`; and the interface must retain unmet
premises rather than dropping them. A consumer may reconstruct the Section
6 guarantee from the interface alone and must reproduce the same
`conditional_only` verdict.

## 10. Analytical failure controls

These separate the premises without a fixture bank or acquired data.

| Control | Removed/changed | Consequence |
|---|---|---|
| C1 | `G_a` dropped (`a_sys` unjustified) | `e_cal` unbounded; no BU certificate (Cor 1) |
| C2 | Transfer dropped (`d` undefined) | `G_d` unproved; composition void |
| C3 | Support/nesting violated | Inherited BU negative control: marginal `e=0` holds but `P(10)>0`; guarantees void |
| C4 | Marks or target redefined between channels | `d` and `τ` compare different objects; `G_d`, `G_a` void |
| C5 | Same records used for calibration and report | Marginal `α+β` unproved; joint theorem required |
| C6 | Repeat-until-pass, `K` unbounded | No R3 bound; selection defect |
| C7 | Report only accepted `H`, ignore `P(H)` | Conditional reliability misread as `1−α−β` |
| C8 | Reference chooses the family it validates | Hidden multiplicity; `β_ref` not marginal |

None of these is a new numerical study; each is a statement about which
premise a guarantee depends on. They are the analytical controls a future
verification would check symbolically.

## 11. Bounded successor and deferred option

The program owner directed that the next gate, **QR-05BX**, be the
apparatus-to-event interface design rather than a verification of this
contract. A reference-calibration composition verification is therefore
**deferred, not rejected**, and remains available as a later bounded gate.
If revived, it would be an exact symbolic/algebraic audit of this
conditional contract, not an apparatus calibration. It would fix complete
schemas and limits before its first helper or oracle:

- verify Proposition 1 and its worst-case tightness, and Corollaries 1–2,
  over declared symbolic norm values with exact rational arithmetic;
- verify Proposition 2 and the regimes R1–R3, including `K`-repeat union
  budgeting and the conditional-`H` division, with explicit boundary
  controls at `P(H)∈{0,1}`;
- verify the Section 9 schema round-trip and the rule that any unmet
  load-bearing premise forces `conditional_only = true`;
- retain the Section 10 controls as negative checks that each dropped
  premise voids the corresponding guarantee.

The deferred verification must not acquire data, choose or model a device,
produce a numerical `β`, `a_stat`, `d_stat` or `e_max`, sweep a fixture
probability bank, tune a grid/quota, or claim calibration, metric recovery
or gravity. Its object would be the composition algebra and the auditable
interface, and every result would stay conditional on P1–P12.

Limits for that bounded successor follow BV's pattern: sources ≤262,144
bytes, capture artifacts ≤16,777,216 bytes, analyses ≤30 seconds, suites
≤120 seconds, one cached analysis per normal/optimized mode, one full
replay per mode, and exactly one alternate-runtime reference-only audit
with complete native equality. Create-only evidence must preserve first
failures. None of these limits is exercised by BW.

## 12. Decision boundary and provenance

BW supplies a conditional specification and exact composition lemmas, not
Lean verification, an executed numerical study, a calibrated instrument or
a reference of truth. It preserves BV's first capture, BU's design record,
BT's capture and all pre-existing core/RET/application work. The separate
[decision record](RESULTS.md) records the review and the limitations; the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated.

The applicable structure is a precise division of the distortion claim
into independent reference validity and same-population transfer, with an
explicit account of coverage, validity and selection. It is not general
metric reconstruction, a gravity equation, an ontological proof, evidence
of new physics, or a calibrated measurement interface. Since no independent
reference and no defensible transfer premise are supplied, the contract
stops at the conditional boundary exactly as BU's review required.
Calibration, general densities/metrics, RET and quantum adapters remain
separate. Book work remains archival; Lean installation, clocks and later
gravity couplings stay deferred.
