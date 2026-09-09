# QR-05BN: bounded sampling-density partial identification

9 September 2026 (Pacific/Honolulu). Prospective protocol written before
implementation or fixed numerical evaluation. This continues the
[BM result](../qr-05bm-relative-volume-verification-2026-09-09/RESULTS.md)
by replacing a few fixed density alternatives with an explicitly bounded
continuous nuisance parameter. The geometric target set stays finite.

## Model and distinct observation modes

Adopt signature (+,−), auxiliary null coordinates u,v, fixed marked events
o=(0,0), m=(1/2,1/2), t=(1,1), and their strict causal intervals
Q=(0,1)², I=(0,1/2)². For η∈{0,1}, s∈{1,4},

```text
ds²=s(1+ηuv) du dv,
dμ=s(1+ηuv) du dv/2,
ρδ=1+δuv,
ν(A)=∫Aρδdμ/∫Qρδdμ,
τ=μ(I)/μ(Q)=(16+η)/[16(4+η)].
```

The density coefficient δ is fixed across a run and is not known to the
observer. It is a scalar density relative to proper volume, not an extra
metric determinant. The declared domain is δ∈[0,2], so 1≤ρδ≤3 on Q.
Four independently stipulated closed bounds are [0,0], [0,1/2], [0,1],
[0,2]. They are alternative acquisition assumptions, not estimates or
calibration certificates obtained from these same records. All four
geometry/scale labels remain distinct even when targets coincide.

The ideal sampler draws four fresh iid points from ν; only their four
ordered membership bits Yj=1{Xj∈I} are observed. All marks, iid assumptions,
loss-free sampling and the causal-comparison channel are supplied premises.
No proper-time midpoint, calibrated detector or arbitrary metric recovery
is inferred.

The **inverse-problem input here is a stipulated exact population probability
q=ν(I)**, together with a density bound. It is not the four-bit packet, its
frequency k/4, an estimated probability or a confidence interval. This is a
different mathematical input mode from BM's record-only estimator, not a
new claim that BM's observer can access its hidden branch probabilities.
An API can refuse record packets and automatic frequency promotion; neither
a rational number nor a provenance tag can certify how a caller obtained q
or justified the density bound. Those remain external premises.

## Analytical inverse and boundary certificates

Expanding the weighted point measure gives

```text
ρδ dμ = s[1+(η+δ)uv+ηδu²v²] du dv/2.
qη(δ) = [144+9η+(9+η)δ] / [576+144η+(144+64η)δ]
       = (a+bδ)/(c+dδ).
```

Scale cancels in q and τ. The denominator is positive for the full declared
domain. Moreover bc−ad=−432(η²+20η+36)<0, so qη is strictly decreasing.
For any declared bound [0,M], feasibility is precisely
qη(M)≤q≤qη(0), including both endpoints and the degenerate M=0 case.

Solve the exact linear equation

```text
(qd−b)δ = a−qc.
```

When qd−b is nonzero, record the unique algebraic candidate and intersect
it with the supplied closed bound. When qd−b=0, do not divide. Its right-
hand side is nonzero in these nonconstant families, proving infeasibility.
A hypothetical all-δ constant-map solution is outside this model, not an
unhandled admissible branch. Coefficients retained by the implementations
are actual affine mass integrals, so their common scaling need not be the
integer normalization used in the displayed formula.

The [machine protocol](protocol.json) fixes nine rational population inputs,
including q=0 and1 (valid probabilities but model-infeasible), both inverse
poles 1/16 and5/104, the δ=2 boundaries 3/16 and173/1136, and
1/5,17/80,1/4. No input is chosen or tuned after inspecting execution.
All thirty-six bound/data cases retain all four candidate rows, including
infeasible rows and rejected algebraic candidates. Empty compatibility is
a disagreement between stipulated data and the declared model/assumptions,
not a refutation of arbitrary geometry or an apparatus diagnosis.

## Information distinctions and controls

Every feasible candidate has the same stipulated q and hence the complete
iid membership law Pq(y)=q^k(1−q)^(4−k). Record target sets exactly as
subsets of {17/80,1/4}; do not report their interval hull. The scale labels
cannot be collapsed merely because target values coincide.

Two prespecified collision controls use the widest bound:

- At q=17/80, flat δ=1 and conformal δ=0 retain BM's equality of the
  entire normalized point law despite unequal geometric targets.
- At q=1/5, flat δ=16/11 and conformal δ=45/158 have equal complete
  membership laws but unequal point laws. The latter has a nonzero u²v²
  coefficient. Richer observations could distinguish this pair if their
  channel is specified; equality of the present membership law does not
  prove their equality.

For these polynomial measures, equality of the full normalized point law
is equivalent to equality of both η+δ and ηδ, independently of s.
The constant coefficient and normalizer fix the common scaling. Compute
full point-law classes within every feasible case rather than substituting
the membership classes.

Check all adjacent bound inclusions at every q: tightening a bound can
only remove compatible labels/targets, and a surviving δ cannot change.
Check both scale pairs across every case and their geometric volume factor.

Separately retain all sixteen realized membership words under each bound.
Since every candidate's q range is strictly inside (0,1), every such word
has positive probability for every geometry and every admissible δ. A word
0000 or1111 therefore remains possible even though exact population q=0
or1 is model-infeasible. This contrast is not a confidence procedure and
does not authorize plugging k/4 into the population solver.

The nine stipulated data laws are also enumerated, sixteen ordered words
each, even when no geometric candidate realizes the supplied q. Keep their
zero-probability words at q=0,1. These are data-law tables, not additional
admitted geometric worlds or physical observations.

No new quantum-state or passive-chart enumeration is included. The common
independent quantum resource from BM is mathematically inert under this
same channel; no sensing advantage or new QM validation is claimed here.
No BM engine or prior numerical tree will be rerun.

## Exact native report contract

Independent `primary.py` and `reference.py` expose `analyze(protocol)` with
no file access or shared mathematical implementation. Native data use only
plain dict/list/str/int/bool and exact Fraction. No floats or None. Empty
sets/lists use `[]`. Computed scalar quantities always use Fraction; IDs,
exponents, labels, counts and flags use their stated native types.
Polynomials are sorted nonzero `[i,j,Fraction]` coefficient lists of u^i v^j.

- Top level: `schema`="qr05bn-report-v1", `geometries`, `cases`, `laws`,
  `monotonicity`, `finite_records`, `collisions`, `scale_pairs`.
- Each geometry in protocol order: `id`, `eta`, `scale` (metadata ints),
  `volume_Q`, `volume_I`, `target` (Fractions), `mass_I_coeffs`,
  `mass_Q_coeffs` (two Fractions each in δ-degree order),
  `derivative_numerator` (Fraction), `ranges`. Each range is
  `bound` (ID), `delta` ([lower,upper] Fractions), `q` ([min,max] Fractions).
- Cases are bound-major then population-data order, `id`=`bound/data`.
  Each has `id`, `bound`, `data`, `q` (Fraction), `hypotheses`, `worlds`
  (feasible IDs in geometry order), `targets` (distinct sorted Fractions),
  `status` ("infeasible", "identified", "ambiguous"), `point_classes`.
- Each hypothesis, including infeasible ones: `id`, `q_range` ([min,max]),
  `inverse_numerator`, `inverse_denominator` (Fractions from actual mass
  coefficients), `candidate` ([] at a pole, otherwise a singleton Fraction list),
  `delta_set` ([] or a singleton feasible Fraction list), `status` ("feasible" or
  "infeasible"), `normalized_point` (polynomial; [] when infeasible),
  `mass_Q`, `mass_I` ([] when infeasible, otherwise singleton Fraction lists).
  A nonempty algebraic candidate is not automatically an admissible δ.
- Point classes follow first feasible member order. Each is `worlds`,
  `targets` (distinct sorted Fractions), `identified` (bool).
- Each data law: `data` (ID), `q` (Fraction), `rows`; each lexicographic
  y∈(0,1)^4 row has `y` (four ints), `k` (int), `p` (Fraction).
- Each monotonicity row, adjacent-bound-major then data order: `tight`,
  `broad`, `data` (IDs), `world_subset`, `target_subset`,
  `nuisance_preserved` (bools). There are 27 rows.
- Each finite-record group in bound order: `bound`, `strict_support` (bool),
  `rows`; each lexicographic row has `y`, `k`, `frequency` (Fraction),
  `worlds` (all four IDs) and `targets` (distinct sorted Fractions).
  This is support-only record reasoning, not population-q inversion.
- Collision order is inherited_whole_point then membership_only. Each has
  `id`, `case` (widest-bound case ID), `worlds`=["flat","conformal"],
  `deltas` (two Fractions), `target_gap` (flat minus conformal Fraction),
  `membership_equal`, `point_equal` (bools). Recompute each candidate's
  full word probabilities from its own mass ratio, not equality of input q.
- Scale pairs are flat/flat_x4 then conformal/conformal_x4. Each has
  `worlds`, `volume_factor` (Fraction), `target_equal`,
  `nuisance_sets_equal`, `point_laws_equal` (bools across all cases).

The primary route integrates monomial densities and solves the exact linear
inverse before closed-bound intersection. The reference independently
integrates direct functions with tensor Simpson, derives attainable ranges,
and solves the affine equation with explicit singular/range cases; it
reconstructs point polynomials independently. A third test oracle uses
endpoint mass formulas and forward substitution to check the entire report.
Full reports are compared with exact types before canonical encoding.

## Public population-query contract

`study.identify(query)` accepts exactly a plain dict with keys `schema`,
`data_kind`, `q`, `density_bound`, `bound_basis`. Strings are plain str;
the first, second and fifth equal the corresponding protocol observer
values. `q` is exactly a two-plain-int reduced rational list with positive
denominator, and must be one of the nine fixed population inputs.
`density_bound` is one of the four named bounds. No implicit bool/float,
Fraction-object, subclass, unregistered probability, record packet, count,
quota, actual world or extra field is accepted. Failure raises ValueError.
Valid registered probabilities with no candidates return an empty set and
"infeasible", not an interface error. The return has exactly `worlds`,
`targets`, `status` and `nuisance` (feasible `id`,`delta` Fraction rows).

The solver uses only public family definitions and supplied query premises.
It must not read files, run an engine, inspect a previous result, widen a
density bound or infer q from a record. Input and output containers must be
detached. This contract does not authenticate population-law or calibration
provenance; a mislabeled four-shot frequency cannot be detected by its value.

## Reused evidence utilities and bounded execution

Use fresh authenticated bytes of BM's `study.py` only for exact codecs,
native comparison, bounded I/O, exclusive writes and deadline utilities.
Its SHA-256 is
`157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55`.
Do not invoke its analysis, estimator, freeze or capture wrappers. BN owns
its schemas, source inventory, protocol pin, analysis and publication
wrappers. Aliased utility functions retain their isolated module globals;
no ROOT rebinding is used to pretend BM's wrappers became BN wrappers.

Before fixed evaluation, create a new source freeze exclusively. Its nine
identities are BN README, protocol, primary, reference, driver and test file,
plus BM's utility driver, README and RESULTS. Recheck the utility bytes used
at load against the snapshot. No old numerical capture is consumed as a
mathematical answer table. The predecessor records authenticate context,
not automatic validation of the enlarged density family.

Use new `qr05bn-source-freeze-v1` and `qr05bn-capture-v1` schemas with
the same strict tagged-Fraction encoding, source map and freeze digest
contract as BM. Inputs are capped at 262,144 bytes per source and
16,777,216 bytes per artifact. Create-only writes, final readback, strict
JSON/native types, immutable engine inputs, fresh source execution and
read-only full replay remain required. Preserve failed evidence; any
post-first-evaluation source correction needs a separately named new freeze
and capture, never overwriting an old one.

The finite coverage is 36 cases/144 hypothesis rows, nine laws/144 ordered
data-law rows, 27 bound-monotonicity checks, 64 finite-word support rows,
two collision controls and two scale checks. No scans, loss enumeration,
random simulations, quantum-state reruns or extra fitted cases. Each complete
analysis is limited to 30 seconds and each test suite to 120 seconds.
Run one normal and one optimized suite, one complete replay in each mode,
and exactly one reference-only alternate-runtime analysis comparing the
whole native and canonical report. Cache one full analysis per suite;
use focused mocked utility integration/tamper cases rather than importing
the entire BM suite. No adaptive work-budget increase or timing-sensitive
RET rehearsal overlap, dependencies, physical devices or external data.

## Reproduction and limits

Once the retained evidence exists, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bn.py
python3 -I -O -B test_qr05bn.py
```

Initial `--freeze source-freeze.json` and `--capture results.json` are
exclusive operations; never remove evidence just to repeat them. Execution
outcomes and corrections are recorded in [RESULTS.md](RESULTS.md).
Success is exact partial identification within this bounded family, not
physical density calibration, finite-shot certainty, arbitrary metric
reconstruction, QM/gravity derivation, ontology validation or RET release.
Book work remains archival; clocks, Lean integration and later gravitational
couplings remain separate.
