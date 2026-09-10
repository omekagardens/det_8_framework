# QR-05BV results

9 September 2026 (Pacific/Honolulu). **Bounded verification complete.**
The first frozen capture passed without a mathematical-source revision.
Both independent engines agree on the complete native rational report;
all 28 tests pass in normal and optimized modes, both full replays match,
and the single Python 3.11.6 reference-only audit matches.

The [prospective contract](README.md), [fixed protocol](protocol.json),
[source freeze](source-freeze.json), and [complete capture](results.json)
retain the evidence. This verifies BU's conditional toy construction,
not a physical acquisition-error bound or an apparatus.

## Distortion margins and fixed-budget outcomes

For the admitted bound-only nested iid law classes, the exact separation
is `D_e=max(D-2e,0)`. All eight rows retain both a global lower certificate
and actual nested-law contacts attaining that distance. The signed remainder
and grid slack remain distinct from the nonnegative distance.

With n=65,536 and m=256, the sufficient test is
`slack=D-2e-1/128>0` and `n*slack²≥10`. It passes three rows and does
not certify five. The full results are:

| Class/error case | e | D_e | Grid slack | Exact score | Sufficient certificate |
|---|---:|---:|---:|---:|---|
| uniform/zero | 0 | 3/64 | 5/128 | 100 | Yes |
| uniform/quarter | 3/256 | 3/128 | 1/64 | 16 | Yes |
| uniform/contact | 3/128 | 0 | −1/128 | 4 | No: actual-law collision |
| half/zero | 0 | 1/48 | 5/384 | 100/9 | Yes |
| half/quarter | 1/192 | 1/96 | 1/384 | 4/9 | No: sufficient budget test fails |
| half/contact | 1/96 | 0 | −1/128 | 4 | No: actual-law collision |
| one/zero | 0 | 0 | −1/128 | 4 | No: inherited ideal collision |
| two/zero | 0 | 0 | −1/128 | 4 | No: inherited ideal collision |

The half/quarter case remains positively separated. Its failed sufficient
test is not an impossibility proof or a minimum-quota result. Conversely,
at the two narrow-class contact allowances the different ideal targets
share the same complete actual marked-symbol law. The common populations
are (37/160,45/128) for uniform and (53/240,65/192) for half.
The unchanged ideal targets are 1/4 and 17/80.

The certificates use the every-possible-count-box width bound, not a
favorable realized box. Under all fixed ideal-family, density, nested iid,
mark, no-unmodeled-loss and valid-e premises, a certified row has correct
singleton probability at least 19/20 and wrong-target probability conditional
on a singleton at most 1/20. These are conditional model guarantees, not
measured device success rates. No large-quota count law was evaluated.

## Exact coupled inverses and negative controls

All ten original population boxes are singletons. Forty enlarged and forty
unexpanded geometry hypotheses retain the complete shared-δ intervals,
four original affine mass constraints, and forward/latent witnesses at
every admitted endpoint. Scale copies have the same normalized intervals.

| Population box | Enlarged flat δ set | Enlarged conformal δ set | Target status | Unexpanded status |
|---|---|---|---|---|
| uniform/flat | {0} | ∅ | Singleton | Singleton |
| uniform/conformal | ∅ | {0} | Singleton | Singleton |
| uniform/midpoint_quarter | ∅ | ∅ | Empty | Empty |
| uniform/midpoint_contact | {0} | {0} | Ambiguous | Empty |
| half/flat | [16/41,1/2] | ∅ | Singleton | Singleton |
| half/conformal | ∅ | [0,18/209] | Singleton | Singleton |
| half/midpoint_quarter | ∅ | ∅ | Empty | Empty |
| half/midpoint_contact | {1/2} | {0} | Ambiguous | Empty |
| one/collision | {1} | {0} | Ambiguous | Ambiguous |
| two/collision | {1} | {0} | Ambiguous | Ambiguous |

At contact, the original singleton box perfectly covers an admissible
actual population, but the unexpanded ideal inverse is empty. Enlargement
correctly restores both targets. At the smaller midpoint allowance neither
complete ideal family is compatible; this is not an admitted true-world
example. Endpoint witnesses are duplicated for singletons to preserve the
closed-interval wire. No coordinatewise independent nuisance values are used.

The sole private boundary exercise confirms that an original box with
empty intersection with the nested triangle remains empty before
enlargement, even when the enlarged rectangle covers the triangle.

The nonnested control (9/16,3/16,1/16,3/16) preserves both flat δ=0
marginals at e=0 but has forbidden 10 mass 1/16. The first attempt alone
gives a refusal-probability lower bound above α=1/20. Thus a marginal
distortion bound cannot certify the separate nested-support premise.
The n-dependent refusal power was not evaluated. This control is outside
the admitted law, not a failure of its conditional theorem.

Both scale audits pass at identical B,e,C: masses and volumes scale by
four, derivative numerators by sixteen, and raw inverse constraints and
their endpoint values by four. Normalized classes, distortion contacts,
latent witnesses, nuisance sets and targets agree. This does not identify
absolute scale or equate arbitrary separately chosen actual populations.

All four complete ideal classes and all four freshly derived zero-error
legacy class plans exactly match the authenticated BT capture. No BT or
earlier mathematical engine was rerun.

## Verification and evidence integrity

The primary route integrates monomials and clips affine mass inequalities
in δ. The reference uses tensor Simpson integration and a shared normalized
segment parameter before independent density recovery. The third-route
test oracle uses rectangle moments and exact original-ratio root cells.
It compares the complete native report, not only selected headline values.

Static cross-review and Ruff/compilation completed before the first freeze.
Review corrected a prose line-sign convention, tightened baseline metadata
validation, and made native dictionary comparison order-insensitive while
preserving all list order and exact types. None followed a mathematical run.
No frozen mathematical source was changed afterward.

| Check | Outcome |
|---|---|
| First capture, Python 3.14.0 | Complete primary/reference agreement |
| Normal suite | 28/28 passed |
| Optimized suite | 28/28 passed |
| Normal and optimized full replays | Exact first-capture agreement |
| Single Python 3.11.6 reference-only audit | Exact complete-report agreement |
| Static Ruff and normal/optimized compilation | Passed |

The 28 tests include 15 mathematical checks and 13 input, codec, source,
publication, mutation and deadline checks. The driver authenticates full
BT bytes before parsing, passes independent fresh input copies to fresh
engine namespaces, compares native types before encoding, and checks final
source/freeze/capture bytes. Exclusive publication preserves evidence.
Limits remain 30 seconds per analysis and 120 seconds per suite; both
suites finished in under one second on the recorded runtime.

- First freeze: 1,700 bytes;
  SHA-256 `6ea9205430992e4af8d90ef69270f67cbbaa2e43b831c54271f78c1b46e18571`.
- First capture: 100,522 bytes;
  SHA-256 `44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`.
- Canonical encoded report: 98,811 bytes;
  SHA-256 `919c692f3b1e07be12d94d0a6f8df809b4ddc03e8946b50c95fe876e9acf1741`.

The twelve frozen identities are the six prospective BV sources, BU
README/RESULTS, BT README/RESULTS/capture, and the hash-pinned BM evidence
utility. This result document and the roadmap are publication records,
not prospective mathematical sources. The older BT capture remains
SHA-256 `6beb088e27e0ec0c843b9be1c0794add02d8418a2fcbce9d4ade95ca685a9adb`.

## Value, remaining gap, and next gate

The useful result is a checkable bridge from uncertainty about an actual
record population to sets of ideal geometric targets. Sampling uncertainty,
grid enclosure, bounded systematic distortion and genuine same-law target
ambiguity now have distinct operational meanings. A wider inverse can be
the correct repair; a more confident singleton is not automatically better.

The bound e is still supplied, not estimated or validated here. A close fit
to production records does not, by itself, identify the true ideal world
or certify a distortion bound relative to it. Finite absence of forbidden symbols
does not establish zero forbidden population mass or iid sampling.
No quantum advantage, formal Lean proof, general metric reconstruction,
gravity dynamics, or calibrated RET/application readiness follows.

Propose **QR-05BW: reference-calibration admissibility contract**, design-only
and not started. Specify independently justified reference information,
transfer to the same marks/population, deterministic versus statistical
allowance validity, and separate support/iid/stationarity/loss premises.
State α+β composition and acceptance/selection limits with explicit events;
do not infer accepted-batch reliability from an unconditional bound alone.
The output should be an auditable evidence/assumption interface with unmet
premises retained, not another toy fixture bank or a claimed calibration.

BW must stop at a conditional contract if no independent reference or
defensible transfer/support premises are supplied. No new numerical β,
quota tuning, device choice, acquisition, dependency install or RET coupling
is implied. Book work stays archival; clocks and later gravity couplings
remain deferred.

## Publication scope

BV began from pushed BU commit
`cfee01c011301ca74424343053e146604081983b` on authoritative branch `ret`.
Only the nine files in this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
belong to this publication. The 231 pre-existing dirty status entries,
including separate core, RET, application work and the local temporary
model sheet, remain outside it.
