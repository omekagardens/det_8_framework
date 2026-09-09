# QR-05BK results: analytic upper-admission boundary

9 September 2026. **Bounded gate complete.** The sharp positive-θ admission
boundary for the fixed asymmetric response has an exact algebraic certificate.
The declared collection now has **126/126 exact position sets and 105/105
exact menu hypothesis/target sets**, up from BJ's 125/126 and 103/105.
No data, sampling positions, supplied geometry or quantum observation law changed.

All 39 dedicated tests pass in normal and optimized Python. Both full replays
and the single independent-runtime reference audit match. The first capture
passed; no post-first-run source, protocol, test or mathematical correction
was needed. This closes the remaining *fixed-collection admission uncertainty*,
not geometric inference, empirical calibration or unique target identification.

## Exact positive boundary

For the unchanged asymmetric corners,
r=1/2−5u/6+v/6−uv/3, b=u(1−u)v(1−v), f=r+θb and
T=13/216+θ/144 on the supplied unit square.
The complete positive-parameter validity set is the closed interval **[0,β]**.

The primitive leading-positive defining polynomial, equal to the raw
eliminant with normalization scalar 1, is

```text
P(v) = 2v^5 + 25v^4 + 90v^3 − 676v^2 + 553v − 120.
```

There are exactly two roots in (0,1), retained in increasing order:

| Isolating cell, with denominator 2^24=16,777,216 | Classification |
|---|---|
| [6,869,898, 6,869,899]/2^24 | Rejected: v<1/2 cannot satisfy the unsquared stationary condition |
| [8,524,160, 8,524,161]/2^24 | Admissible: v>1/2 and k>0 |

Let α be the unique root in the second cell. The exact contact and threshold
are the following rational images of that same algebraic root:

```text
u* = (−33+77α−22α²)/(15−24α−7α²+2α³),
v* = α,
β  = (−25+40α+30α²+4α³)/(−66α+198α²−132α³).
```

The numerator/denominator coefficient lists are retained unreduced as
specified. The root polynomial is not asserted irreducible or minimal.
No rational enclosure endpoint or midpoint replaces α or β.

The exact interval-Horner threshold enclosure is

```text
11043935778039808000 / 819523745093185407
    ≤ β ≤
4240876516676218975361 / 314690002119691714560.
```

It implies the strict, display-only decimal bounds **13.4760 < β < 13.4764**.
The contact is near u=0.35115, v=0.50808; its precise meaning is the algebraic
definition and retained rational image enclosures, not those rounded numbers.
Both image denominators and k are strictly positive on the admitted cell.
The contact is interior and β>0. The value, u-derivative and v-derivative
numerator remainders modulo P are all exactly zero.

## Why this is global, sharp and closed

For θ≥0 the lower response bound is automatic: f≥r≥−1/2.
The remaining requirement is θ≤h(u,v) throughout the open square, where

```text
h=(1−r)/b
 = (1/2)/(uv) + (4/3)/((1−u)v)
 + (1/3)/(u(1−v)) + (3/2)/((1−u)(1−v)).
```

Each reflected reciprocal product has positive-definite Hessian;
the unreflected determinant is 3/(u⁴v⁴)>0. Positive corner-gap weights
therefore make h strictly jointly convex. Also 1−r≥1/3 and b tends to zero
at the boundary, so h diverges on every boundary approach. There is one
interior global minimum, not an arbitrary choice among stationary points.

At the verified contact f=1. For every θ>β,
fθ(u*,v*)−1=(θ−β)b(u*,v*)>0. Thus β itself is admitted and every larger
positive parameter is excluded. Along the square's boundary b=0 and r is
already valid. These arguments establish the global statement; a resultant,
a vanishing derivative, or sampled regression checks alone would not.

Primary elimination squares the explicit one-variable radical derivative,
divides its exact positive factor C, and uses Sturm root counts.
The reference independently eliminates the two stationarity equations and
uses Bernstein/Descartes counts. The test verifier constructs a Sylvester
determinant and uses rational Hermite trace-form signatures and congruence
inertia. All produce the same primitive polynomial, canonical cells, sign
classification, rational images and complete report. Denominator-unit checks
protect the independent quotient-algebra contact arithmetic.

## What changed in the declared target sets

Write t*=13/216+β/144. Only asymmetric/wide/near_corner gains a different
answer. Its exact θ interval is **[304/27,β]**, with exact targets
**[269/1944,t*]**.

BJ had sufficient θ≤151/12 and necessary θ≤128/9 here.
The former unresolved portion now splits into newly certified
(151/12,β] and newly excluded (β,128/9].
The corresponding target split is (85/576,t*] versus (t*,103/648].
Failure of the old sufficient bound was never, by itself, a violation.

Two algebraic readouts illustrate the distinction; they are consequences
of the retained certificate, not additional fitted tests or engine runs:

| θ | Near-corner mean | Target | Global status |
|---|---|---|---|
| 13 | 69/256 | 65/432 | Valid, although not certified by BJ's inner bound |
| 14 | 39/128 | 17/108 | Invalid at the algebraic contact, although not excluded by BJ's outer bound |

Both means lie in the same supplied wide interval [5/24,11/24].
Thus the new result refines global admission without acquiring another
measurement or changing the assumed response interval.

The two previously bounded menus now have exact disconnected target sets:

| Asymmetric wide menu | Exact target union | Open gap |
|---|---|---|
| all | [29/540,221/1728] ∪ [269/1944,t*] | (221/1728,269/1944) |
| center_near | [2/27,11/108] ∪ [269/1944,t*] | (11/108,269/1944) |

Their gaps are unchanged. Neither set should be replaced by its convex hull.
Both menus remain feasible and target-ambiguous. Exactness means the whole
possible set is known; it does not mean a single value has been identified.

The other 17 asymmetric position sets and 13 already exact asymmetric menus
are unchanged. Point and narrow near_corner remain excluded. The other six
cases retain all 108 position sets and 90 menus in the unchanged BJ report.
Every old exact set and every settled classification is preserved; the complete
collection still has 26 feasible/identified, 74 feasible/ambiguous and five
infeasible menus. Point⊆narrow⊆wide nesting and position-labeled hypothesis
filtering remain exact.

## Deliberately unresolved and unchanged

The global negative-θ admission boundary was not solved.
Its inherited sufficient negative set is [−61/4,0], while the necessary
set is [−52/3,0]. That gap is explicitly retained. On every *supplied data
interval*, however, the negative inner and outer pieces already coincide.
Those pieces are preserved exactly and combined with the new positive result.
No claim of a sharp full global θ interval is made.

The whole BJ mathematical report is independently recomputed and matched,
including its whole embedded BI mathematics: supplied geometry, inverse maps,
all seven cases, 224 coupled affine quantum branches and 42 endpoint checks.
The historical restriction confirms 112 quarter patches, 1,008 coefficient
pairs, 175 witnesses, 126 position intervals and 105 menus.
No historical executor or earlier validation lifecycle is rerun.
The quantum law family remains present only once in the nested baseline.

There is still no new quantum advantage, observation law, ontology proof,
unknown-metric reconstruction, continuum or gravitational dynamics result.
The supplied response intervals are not confidence intervals, apparatus
calibration or a fault/noise model. Algebraic endpoints and a bounded
fail-closed comparator are not a general algebraic-number or global
optimization SDK.

## Verification and chronology

The authoritative base is pushed ret commit
e608e472b9fd6251e294a988010ee4c1bc04f183.
The initial method was recorded before implementation; interface and guard
clarifications were made only during static review, before any fixed
polynomial evaluation or root isolation. These included midpoint ownership,
Fraction-only inputs, bounded degree representation, declared boolean metadata,
root sign classification, descriptive input types and denominator-unit checks.
A test-call wiring issue and source-assembly issue were corrected statically.
Formatting and syntax checks preceded the source freeze.

The first source freeze began at **2026-09-09 18:47:02 UTC**.
The first source-bound capture succeeded. Both implementations were held
unchanged thereafter. Narrow checks found no active timing-sensitive RET
rehearsal before execution. No dependencies, RET/core sources, application
artifacts or temp_qr.md were changed.

| Check | Outcome |
|---|---|
| Static Ruff and syntax checks | Passed |
| First native-type independent comparison/capture | Passed |
| Python 3.14.0 normal dedicated suite | 39 tests passed, 71.105 seconds |
| Python 3.14.0 optimized dedicated suite | 39 tests passed, 70.449 seconds |
| Normal full evidence replay | Exact match |
| Optimized full evidence replay | Exact match |
| Exactly one Python 3.11.6 reference-only analyze audit | Whole mathematical report matched, 0.686135 seconds |
| Final six sources + five historical inputs + freeze + capture | All 13 byte identities unchanged |

The alternate audit made exactly one reference analyze call, retained input
ownership, and matched the canonical complete report: **552,609 bytes**,
SHA256 **790e359bf9816997550657276fe6c80f415cd634588fc8c597a6c19a37ea7070**.
It did not rerun both engines or claim a new empirical replication.

The tests cover all root cells and rejected roots; known roots, endpoint and
rational-midpoint handling; degree/depth/node caps; strict input types;
unresolved endpoint-order refusals; exact closed unions and gaps; negative
piece preservation; contact identities; quantum-law lineage; whole-report
mutations; source/authentication, publication and replay races.
Regression checks support the documented algebraic proof; this is not a
Lean-checked formal theorem.

The create-only [source freeze](source-freeze.json) is **2,330 bytes**,
SHA256 **d42bbbb8bbd20beec82525a8e1c27fdd1de1fb258f6e92522ad0e1eb0117e7a1**.
The unchanged [capture](results.json) is **3,350,395 bytes**,
SHA256 **dee443f657b267f6a082ea24f600f76fce15611eeeb0c129297df8e9c0c5b56b**.
All eleven source/input hashes are recorded there; the four-million-byte cap
was not expanded. No post-first-run scientific/source/test correction or
adaptive extra isolation budget was needed.

## Application value and next gate

The practical mathematical gain is an exact admission-and-identification
boundary for this supplied nonlinear response family. A response that passes
the local interval check can now be correctly accepted or excluded globally;
possible geometric-response targets retain honest disconnected sets and
algebraic endpoints. This is useful certificate structure for later inverse
problems, but it does not turn an assumed apparatus or geometry into measured
evidence. RET integration remains under its own release/calibration gates.

**Next proposed gate: QR-05BL, geometry-identifiability design checkpoint.**
Do not make the unused negative-boundary optimization a prerequisite.
Instead specify one genuinely unknown geometric quantity and an observable
record law that depends on it, separating supplied structure from inferred
structure before another executable study.

A bounded candidate is one relative causal-interval volume V(I)/V(Q) over
two declared conformal-volume hypotheses with the same causal order.
An explicitly assumed iid sampler uniform in each hypothesis's proper volume
would yield causal-membership records. Its complete forward law, observer
access and population-identification criterion must be derived and frozen,
not smuggled in as a supplied volume mark or geometry-encoded quantum phase.

Reuse the existing order-only and density-compensation ambiguities as controls:
unknown sampling density can hide changed geometric volume, and normalized
membership laws cannot identify an absolute scale. Identical
geometry-independent quantum payloads must not be claimed to repair these
failures. Finite-shot uncertainty, unsupported or correlated retention,
apparatus calibration and RET integration remain separate.
BL is proposed design work, not an executed geometry result.

See the [prospective contract](README.md), [frozen input](protocol.json),
[preceding BJ results](../qr-05bj-fixed-interval-refinement-2026-09-09/RESULTS.md)
and [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
