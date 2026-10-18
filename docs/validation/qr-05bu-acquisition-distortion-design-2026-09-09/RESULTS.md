# QR-05BU decision record

9 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone contract](README.md) now connects a bounded systematic
population distortion to ideal geometric target sets, without changing
BT's frozen evidence. This gate ran no mathematical engine, test suite,
confidence table, simulation or acquisition. Its displayed fractions are
analytical results, not a new numerical capture.

## Main result

Let q be the ideal marked-probability pair, r the actual fixed iid nested
record law, and e an externally justified bound on ||r−q||∞.
The observed confidence box covers r, not automatically q. Inverting the
box enlarged by e on each side restores coverage of the unchanged ideal
relative-volume target.

An explicit nested-population witness proves that this enlarged-box
inverse is exact for the bound-only model, provided the original box
admits a nested population. Coupled mass inequalities retain one shared
density δ. An inconsistent original box stays empty; enlargement must
not manufacture a fictitious actual-law witness.

For ideal class separation D, the full actual-law classes have exactly

```text
D_e = max(D−2e,0).
```

The lower proof is a triangle inequality; interpolating the retained ideal
nearest pair attains it inside the nested-probability triangle. This is a
continuous-class theorem, not a finite grid or selected-fixture comparison.

For the unchanged n=65,536,m=256 design, a sufficient certificate is

```text
s_e = D−2e−1/128 > 0,       65,536 · s_e² ≥ 10.
```

It ensures that EVERY possible count box has full width plus 2e strictly
below D. Under all stated model/acquisition/density/distortion premises,
the SAME coverage event therefore gives at least 19/20 probability of
a correct singleton and at most 1/20 wrong-target probability conditional
on a singleton. A favorable realized width alone does not establish those
unconditional or selection-conditional guarantees.

A deterministic valid e consumes separation, not another failure
allocation. A statistically calibrated allowance instead needs its own
validity theorem; a separate calibration failure budget β generally changes
the conservative error allowance to α+β. Selecting only calibration
outputs that pass a budget check requires another selection argument.

## What the analytical controls distinguish

| Density premise | Ideal D | Illustrative allowance e=D/4 | Remaining D_e | Fixed-budget score | First bound-only collision allowance |
|---|---:|---:|---:|---:|---:|
| uniform | 3/64 | 3/256 | 3/128 | 16; certified | 3/128 |
| half | 1/48 | 1/192 | 1/96 | 4/9; not certified | 1/96 |

The half-class example remains positively separated and has positive
grid slack, but the conservative budget test fails. That is not an
impossibility result. By contrast, at the collision allowance the midpoint
of the ideal contact pair is an actual nested law allowed by both targets:

- Uniform: r=(37/160,45/128), with ideal densities (0,0).
- Half: r=(53/240,65/192), with ideal densities (1/2,0).

Both hypotheses then produce the same complete marked-symbol distribution
and the same iid record law for every quota, while the ideal targets remain
1/4 and 17/80. No procedure can give a correct-singleton probability above
1/2 to both hypotheses under that common law. For this enlarged-common-box
rule, both targets are retained on the same population-coverage event.

This is an obstruction for maximal bound-only nuisance classes, which
permit hypothesis-specific actual-law choices. It does not prove that
one specified known instrument channel creates that collision, nor that
the distorted continuous-point densities are identical. The older one/two
ideal whole-point collision remains a separate, stronger obstruction.

The midpoint singleton population box is also an exact counterexample to
using the unexpanded inverse: it covers an admissible actual law perfectly
at e=D/2, yet the old ideal inverse is empty. Enlargement correctly returns
both targets. These are algebraic population boxes, not acquired confidence
outputs.

A second negative control keeps the ideal flat δ=0 marginals exactly but
uses actual symbol probabilities (9/16,3/16,1/16,3/16). It passes the
marginal e=0 comparison while violating the required P(10)=0.
The probability of a forbidden record is not controlled by α.
Thus even a perfect marginal match cannot establish acquisition support,
iid behavior, correct pairing or calibration.

## Applicable value and boundaries

The calculus now separates four limitations:

- Finite-sample uncertainty depends on the quota and actual record law.
- Grid rounding is a computational enclosure.
- Systematic population distortion consumes a nonvanishing separation allowance.
- Identical allowed record laws make some different ideal targets unidentifiable.

A calibration validity probability is distinct again: it governs whether
the supplied allowance is trustworthy. More samples do not turn a false
or unjustified allowance into a valid premise.

This is useful structure for a future auditable measurement interface:
state which ideal target is being estimated, which actual law generates
the records, and which uncertainty bridges them. It does not yet supply
that instrument, a calibration method, a general metric or gravity dynamics.
No RET integration or application readiness is inherited. The ideal family,
density bound, fixed marks, nested iid attempts and no-unmodeled-loss premise
remain essential. Ideal all00/all11 probability controls cannot simply
be copied to a distorted actual law.

At e=0, the confidence inverse and budget reduce to the prior construction.
At identical supplied B,e,C, scale copies have equal ideal families,
allowed actual-law classes and target inverses; no absolute scale is
identified. Arbitrarily chosen actual populations in different scale
worlds are not asserted to coincide.

## Review and next gate

Independent analytical reviews checked:

- The continuous-class lower bound, attaining actual-law pairs and every
  fraction in the fixed eight-row planning table.
- Exact nested latent-population box witnesses, shared-density inversion,
  closed midpoint contacts and ten prospective population-box controls.
- Coverage transfer, the factor of two, the every-batch width quantifier,
  conditional singleton reliability and calibration/acceptance-event limits.
- The forbidden-support counterexample and exclusions of unsupported
  drift, loss, dependence, mark changes and physical-channel claims.

Review tightened the every-batch width quantifier, explicitly defined the
calibration-validity event, and clarified complete-family midpoint bounds
and same-input scale comparisons. These are analytical drafting corrections,
not changes prompted by a numerical study. No formal Lean proof is claimed.

Accept BU as the design checkpoint. Propose **QR-05BV: bounded acquisition-
distortion verification**, not started. The fixed future domain is eight
class/error rows, ten singleton population-box controls, one nonnested
negative control and two scale comparisons. It preserves n,m,α and all tail
allocations. Freeze complete independent sources and exact report schemas
before execution; compare e=0 projections with authenticated stored BT,
never a historical mathematical rerun.

BV must retain both successful and failed sufficient certificates, actual
collision witnesses, complete nuisance intervals and native type-exact
evidence. The contract forbids count-space sweeps, adaptive allowance/quota/
grid tuning, new acquisition, dependencies and RET coupling.

## Provenance and publication

BU began from pushed BT commit
`58ef13c24fa09657fcdb537333be07c084c6c12e`.
Metadata-only checks preserve BT's first freeze and capture and all twelve
frozen source identities; these checks do not revalidate its mathematics.

- BT freeze: 1,673 bytes;
  SHA-256 `436ce2004806f163074f94e14f3b088b77329932ba276e1518c613d1af47aeb2`.
- BT capture: 48,175 bytes;
  SHA-256 `6beb088e27e0ec0c843b9be1c0794add02d8418a2fcbce9d4ade95ca685a9adb`.

Publication is only this decision record, [README.md](README.md), and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
applications and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
