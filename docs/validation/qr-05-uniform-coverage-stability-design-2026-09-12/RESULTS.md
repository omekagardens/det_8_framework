# Uniform coverage/stability: analytical decision

12 September 2026 (Pacific/Honolulu). **The analytical design gate is
complete.** The [standalone contract](README.md) gives an explicit conditional
route from coverage and calibrated pairwise intervals to a stable directed
geometry comparison. No new mathematical executor, fixture enumeration,
test suite, simulation or acquired data is produced by this gate.

## Main constructive result

For a known strict order C and simultaneously valid bounds l≤d≤u on a
C-superadditive target d, closing the LOWER bounds gives

`l ≤ T_Cl ≤ d ≤ u`, hence `||T_Cl−d||∞ ≤ ||u−l||∞`.

Unlike a generic two-sided noisy closure, this conservative route has no
graph-height multiplier. It avoids accumulated positive overshoot, while
retaining its explicit downward bias. It is not claimed to be optimal or
unbiased. The intervals and order must be justified; closure does not make
unverified intervals statistically calibrated.

There is also an exact feasibility criterion: some C-superadditive kernel
fits the intervals iff T_Cl≤u. The three-chain intervals with lower values
(1,1,0) and upper values (1,1,3/2) fail despite every individual interval
being nonempty. Raising the endpoint upper bound to 2 makes them feasible.
This supplies a potential future anomaly-triage check, not a diagnosis of
which instrument, order or model assumption failed.

With supplied global profile modulus ω, sample fill bound h and interval
width v, the combined approximation bound is

`D_C(M,T_Cl) ≤ 2ω(h)+v`.

Thus vanishing fill radius and interval width imply convergence under the
stated premises without a height-dependent noise requirement. A measured
finite matrix alone does not establish those premises.

## Useful geometry link and retained obstructions

The design specializes the coverage argument to a supplied Minkowski
rectangle [0,T]×[−L,L]. It derives the global square-root profile modulus
sqrt((2T+4L)q), the sharper sample graph bound
min(T,sqrt(2(2T+4L)h)), and an explicit positive-diameter certificate.
Exact rational null-boundary examples show why a Lipschitz assumption would
be wrong there. Generic rational coordinates still produce irrational
separations; no silent conversion to exact Fractions is authorized.

The remaining obstructions are explicit:

- Identical observed kernels and exact diameters can conceal different
  ambient coverage. A hidden midpoint gives a finite witness.
- Generic centered positive noise can accumulate along paths. A unit-
  interval chain has vanishing entrywise noise but constant raw closure
  error; diameter normalization hides that scale error entirely.
- Changing the supplied order can create order-one closure changes even
  when the numeric input barely changes.
- Finite point distinction is compatible with gaps tending to zero.
  A fixed positive minimum gap is incompatible with arbitrarily fine
  coverage of an infinite compact distinguishing quotient.
- IID coverage rates require supplied covering and lower-mass bounds plus
  simultaneous measurement-error control. The analytical union bound is
  not an empirical validation of a DET growth process or a fitted exponent.

The prior DD scale-factor distinction remains unchanged. Calibrated scale,
sampling mass and finite-resolution distinction are different requirements.
No new physical law, ontology, spacetime acquisition or RET readiness follows.

## Next bounded gate

Implement the finite certificate checks in section 9: five coverage bases
under four separate variants (20 rows) and six interval bases under four
separate variants (24 rows). The prospective coverage census includes 128
ordered graph discrepancy cells; the interval census includes 184 cells
per full matrix and 80 strict paths. Twenty interval rows should be feasible
and four infeasible. Four named control families have five fixed instances.

All are analytical predictions, not executed counts. The next gate must
freeze nine sources before its first mathematical execution, retain full
exact evidence, run normal/optimized tests and obtain three dedicated
capture-matching replays including one Python 3.11 replay. Infinite-domain
coverage, asymptotic rates and sampling/calibration assumptions remain
analytical or externally supplied—not proved by those finite checks.

## Review, evidence and publication boundary

Three independent analytical reviews confirm the geometry constants/null
boundary, fixed-order and interval proofs, sampling/packing claims and
prospective census. Their precision corrections make finite fill radius,
positive hidden masses, the full interval/operator domain and sample-label
transport explicit. They also distinguish sufficient normalization bounds
from necessary conditions on every possible sequence.

Metadata checks confirm all 55 prior frozen source bindings and all six
saved capture hashes are unchanged. Repository validation is limited to
those metadata checks, local links and diff hygiene; no prior mathematical
suite or capture is replayed. All seven local links in this new design and
the current roadmap section resolve; the directory contains only its two
Markdown documents. All 231 pre-existing status entries are preserved.

The preceding correspondence gate is published on `ret` as
`a5c7f6c2f93e5f0f01b3019bc177630b65547244`. This publication contains only
the two-file design and live research roadmap. All 231 unrelated dirty
core/RET/application entries remain excluded. No old frozen source,
temporary model sheet, RET dependency/API or application code is edited.

Growth/null calibration, empirical metrology and observable validation remain
separate; gravitational dynamics and the book/clock deferrals are unchanged.
