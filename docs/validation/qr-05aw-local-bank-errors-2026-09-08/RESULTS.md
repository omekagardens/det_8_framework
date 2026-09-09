# QR-05AW results: local bank error coordinates

8 September 2026 (Honolulu). Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AV commit `c8be4ee4b571953a9e79a9c2ab2695085b3a3b59`.

## Main result

The new tile-local moment-error model has sharp maximum normalized shared
gain **4 in both supplied geometries**. In each family, preserving the common
bank structure gives strictly smaller bounds than the enclosing receiver box
for **21 of 64 targets**; the other 43 tie (33 zero, ten positive).

The common maximum does not mean the two complete response maps or every
row's bound agree. For example, row 0 has shared gain 5/2 in grid and 23/8 in warp.
Nor is this an improvement over AV at equal noise: AW declares a DIFFERENT
error body and target reference units. The receiver, readouts and noiseless
response identity remain unchanged.

| Local-coordinate unit-box certificate | Grid | Warp |
|---|---:|---:|
| Positive fine cells / repair tiles | 8 / 12 | 8 / 12 |
| Bank / receiver / target coordinates | 48 / 37 / 64 | 48 / 37 / 64 |
| Defined / undefined targets | 64 / 0 | 64 / 0 |
| Strict shared-versus-enclosure gaps / ties | 21 / 43 | 21 / 43 |
| Maximum sharp shared gain | 4 | 4 |
| All maximizing target rows | 9,18,36,63 | 9,18,36,63 |
| Maximum receiver-enclosure gain | 48 | 572/45 |
| Unique maximizing row / target | 18 / (3,3) | 18 / (3,3) |
| Largest rowwise enclosure-minus-shared gap | 44 | 392/45 |
| Unique maximizing gap row / target | 18 / (3,3) | 18 / (3,3) |

The four shared maximizing targets are (2,2), (3,3), (5,5) and (10,10).
In these cases row 18 attains both domain maxima, so the maximum rowwise gap
happens to equal their difference. That equality is not a general rule.
Counts are not probabilities; the grid/warp numbers do not rank intrinsic
geometric robustness or calibrated sensor precision.

## Declared geometry-local calculus

The supplied measure is dmu=du*dv/2. Let V be probe volume, h_t the actual
repair-tile volume and h_C a fine-cell volume (zero for an explicit null cell).
For each positive tile [a,a+du] x [b,b+dv], define local coordinates
xi=(u-a)/du and eta=(v-b)/dv. The declared local moment-error vector is

```text
x_t = integral_tile deltaF * (1,xi,eta,xi*eta) dmu / (V^2 h_t)
      when an underlying field perturbation is specified.

w_t = V^2 h_t
W_t = w_t * [[1,    0,      0,     0],
             [a,    du,     0,     0],
             [b,    0,      dv,    0],
             [a*b,  du*b,   a*dv,  du*dv]]
e_t = W_t x_t,                  x_t = Z_t e_t, Z_t = inverse(W_t).
sigma_(C,D) = V^2 h_C h_D.
```

AW admits x as freely supplied moment-coordinate errors with |x_j|<=epsilon.
It does NOT impose a pointwise bound on deltaF, construct an underlying field,
or certify positivity of a perturbed source. The factor V^2 is a declared
reference-amplitude convention, not a measured uncertainty or apparatus law.
W uses each ACTUAL repair tile, never the old coarse cell or whole probe.
The ordered four raw coordinates remain (1,u,v,uv).

Both two-sided inverse identities W_t Z_t=Z_t W_t=I4 are checked blockwise.
All blocks, inverses, bank scales, fine-cell volumes and target scales are
retained. Both fixed probes have V=1/2; every fixed fine cell has positive
volume, so all 64 target normalizations are defined.

The frozen maps obey the same complete bank identity D B=G. With W denoting
blockwise synthesis, the newly checked propagation maps are

```text
K = D B = G,              H = B W,
J = G W = D H = L,        A_i = J_i / sigma_i,
beta_l = sum_j |H_lj|,
E_il = D_il beta_l / sigma_i,
alpha_i = sum_j |A_ij|,   gamma_i = sum_l |E_il|,
gap_i = gamma_i - alpha_i >= 0.
```

For each defined target, the shared-error interval is
[-epsilon*alpha_i,+epsilon*alpha_i], sharp on the declared local primitive
box. The larger box |y_l|<=epsilon*beta_l has sharp receiver bound
[-epsilon*gamma_i,+epsilon*gamma_i]. It discards the relations y=B W x;
a Cartesian box does not assert stochastic independence.

The complete raw maps K,H,J,L and both zero residuals are retained, as are
the normalized A,E maps. The full D B=G check cannot be replaced by a weaker
restriction that hides a defective decoder. No decoder refit, new measurement,
filter reselection, inferred normalization row or source integration occurred.

AV's supplied B,G,D and target labels are joined to AR's supplied probe,
fine cells, retained repair tiles and bank/target labels. AV's G must equal
AR's retained geometric repair matrix. Selected rectangle containment,
disjoint interiors, coverage and volumes are newly checked; AR's overlay,
integrals, moments, ranks and fits are not regenerated. Provenance authentication
of these supplied data is not empirical authentication of a physical geometry.

## Every strict row

All indices are zero-based original target rows. The same 21 rows are strict in
both families; every unlisted row ties, including ten positive and 33 zero rows.

| Row / target | Grid shared | Grid enclosure | Grid gap | Warp shared | Warp enclosure | Warp gap |
|---|---:|---:|---:|---:|---:|---:|
| 0 / (1,1) | 5/2 | 7/2 | 1 | 23/8 | 29/8 | 3/4 |
| 2 / (1,3) | 3/2 | 9/2 | 3 | 7/4 | 31/12 | 5/6 |
| 3 / (1,4) | 5/4 | 7/4 | 1/2 | 23/16 | 29/16 | 3/8 |
| 5 / (1,7) | 5/4 | 7/4 | 1/2 | 23/16 | 29/16 | 3/8 |
| 15 / (2,10) | 1 | 5 | 4 | 1 | 27/7 | 20/7 |
| 18 / (3,3) | 4 | 48 | 44 | 4 | 572/45 | 392/45 |
| 19 / (3,4) | 1 | 5 | 4 | 3/2 | 17/6 | 4/3 |
| 21 / (3,7) | 1 | 5 | 4 | 3/2 | 17/6 | 4/3 |
| 22 / (3,9) | 3/2 | 17/2 | 7 | 17/12 | 13/4 | 11/6 |
| 23 / (3,10) | 1 | 7 | 6 | 1 | 55/21 | 34/21 |
| 27 / (4,4) | 5/2 | 14 | 23/2 | 23/8 | 58/7 | 303/56 |
| 29 / (4,7) | 5/4 | 7/4 | 1/2 | 23/16 | 29/16 | 3/8 |
| 30 / (4,9) | 1 | 4 | 3 | 7/6 | 8/3 | 3/2 |
| 36 / (5,5) | 4 | 8 | 4 | 4 | 16/3 | 4/3 |
| 38 / (5,9) | 2 | 4 | 2 | 2 | 8/3 | 2/3 |
| 39 / (5,10) | 2 | 4 | 2 | 2 | 8/3 | 2/3 |
| 45 / (7,7) | 5/2 | 21/2 | 8 | 23/8 | 261/40 | 73/20 |
| 47 / (7,10) | 2 | 6 | 4 | 2 | 18/5 | 8/5 |
| 54 / (9,9) | 5/2 | 15 | 25/2 | 61/24 | 349/54 | 847/216 |
| 55 / (9,10) | 2 | 4 | 2 | 2 | 8/3 | 2/3 |
| 63 / (10,10) | 4 | 24 | 20 | 4 | 48/5 | 28/5 |

Previously discussed row 63=(10,10) now has shared gain 4 in both families,
with enclosure 24 in grid and 48/5 in warp. These are AW-domain results;
AV's different-domain row 63 evidence remains unchanged.

## Endpoints, nulls and coordinate transport

Every defined target retains positive and negative SHARED and ENCLOSURE
endpoints, including complete cross-target raw output vectors. That is 128
shared and 128 enclosure endpoints per family, counting zeros and repetitions.

Each shared endpoint actually executes

```text
x -> synthesize(W,x) -> bank error e
e -> synthesize(Z,e) -> recovered x
e -> produce(B,e) -> y -> apply(D,y)
e -> produce(G,e) -> independent direct response.
```

The roundtrip equals x, the full decoded and direct responses agree, all
receiver and target bounds hold, and the designated target attains its signed
bound. No clipping or intercept is introduced.

For the four maximum shared rows 9,18,36,63, the canonical positive local
primitive is (+1,-1,-1,+1) on coordinates 8..11,12..15,24..27,44..47,
respectively, and zero elsewhere, in BOTH families. Negative endpoints reverse
all signs. These are local moment errors, not prepared field perturbations.

Enclosure endpoints instead pass their supplied receiver vector through D.
For row 18 the sign pattern is (+1,-1,-1,+1) on receiver 4..7 and -1 on 33,34,
zero elsewhere; each sign is multiplied by its own beta, not a raw unit value.
No bank preimage is fabricated. A tied gain does not establish reachability of
its canonical enclosure endpoint; no general feasibility solver was run.

All maximizing target indices are retained. Individual witnesses need not
simultaneously maximize every target, and a canonical sign vector is not an
enumeration of the entire maximizing face.

Generic null-cell cases have sigma=0, zero G rows and NULL normalized maps,
gains and designated witnesses. Their full raw vectors remain present:
D can have a nonzero cancelling row, so an enclosure endpoint may produce a
nonzero UNDEFINED raw output. Replacing that raw value by zero is incorrect.
If every queried target is undefined, maxima are NULL and maximizing lists
empty, while receiver radii remain complete.

A separate positive-scale zero-response control has alpha=0 but gamma=4:
B has duplicate mass rows, D=[1,-1], G=0 on the unit rectangle. It is defined,
not null; common errors cancel but the receiver box admits noncancelling errors.
The mixed-null literal control also retains a raw undefined enclosure value
of +/-1/8 while its normalized component is NULL.

Synthetic positive affine coordinate changes transport the entire model
under the explicit convention F'=k^2 F, k=determinant of the coordinate
rescaling. Then W'=S W, Z'=Z S^-1, sigma'=k^4 sigma,
B'=T B S^-1, G'=k^4 G S^-1 and D'=k^4 D T^-1.
Normalized A, shared gains, signs, null domains and full raw endpoint transport
agree. Arbitrary receiver mixing T can change the axis-aligned enclosure;
signed monomial T preserves its gains. No physical row units are inferred.
These SYNTHETIC transports are not a claim that grid and warp are related by
one such global affine transformation. No fixed transformed families were run.

## Application meaning and limits

This supplies a precise geometry-aware reference convention for moment-error
budgets and turns a declared local error budget into 64 response budgets.
Retaining common-bank dependence can prevent unnecessarily loose bounds when
the receiver values genuinely arise from one bank. Independent acquisition
errors require their own justified model.

The benefit is clearer and transport-consistent mathematical error semantics,
not better sensors. Measured noise magnitudes, acquisition architecture,
tolerances and correlations still require calibration. A finite bound alone
does not establish practical robustness.

The next useful distinction is between arbitrary moment-coordinate errors and
errors generated by an explicitly bounded field class. Neither the present
sharpness certificate nor coordinate invariance settles that distinction.

No full-field recovery/stability, unknown-geometry inference, quantum-channel
construction, gravity derivation, empirical sensor validation, RET integration,
new minimality proof or Lean verification was performed. This gate does not
change ordinary physical laws or establish an ontology.

## Representation and verification

Across both families, input geometry contributes 168 rational occurrences and
input matrices 14,432. Retained geometry contributes 170 and block coordinates 792
(24 weights plus 24 forward and 24 inverse 4×4 blocks). Complete maps contribute
45,152 entries; receiver radii, gains, gaps and maxima 464.

The 256 shared endpoints contain 95,744 retained rational occurrences and 6,144
separately counted signs. The 256 enclosure endpoints contain 42,496 rational
occurrences and 4,736 signs. Nulls, labels and target indices are not counted as
rational values; zeros and repeated entries are counted.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Input problem | 47,365 | 47,433 |
| Geometry | 979 | 1,102 |
| Coordinate blocks and scales | 3,089 | 3,384 |
| Complete coefficient maps | 137,698 | 138,475 |
| Shared bounds and witnesses | 318,753 | 321,838 |
| Enclosure bounds and witnesses | 146,801 | 148,189 |
| Complete comparison | 672 | 687 |
| Complete native family | 656,311 | 662,062 |

The suite is 1,320,632 bytes. These overlapping projections are not additive
unique storage, a minimal representation or a measured-value transmission packet.

All 64 tests pass normally and optimized: 128.00 s / 128.11 s
in concurrent runs. Before freeze, all 54 generic tests passed in both modes
(24.37 s / 24.28 s), with all ten fixed tests deselected.

Primary uses triangular coordinate formulas and blockwise products.
Reference uses independent corner differences, pivoted inversion, actual
column probes and interval bounds. The third oracle uses indexed monomial
expansions, scalar contractions and an independent endpoint-grid partition
check. SMALL synthetic cube vertices are exhausted; fixed 48-dimensional cube
vertices are not enumerated, since exact coefficient maps and attaining
signs certify the linear bounds.

Each isolated normal/-O subprocess performs 432 explicit ValueError rejections:
194 malformed fixtures, ten overflow/cycle and 12 early-admission checks PER
engine. Nine additional synthetic selected-projection rejections pass.
All 576 non-noop mutation checks pass: 362 generic families, 192 fixed families,
eight suite and 14 selected-history changes. Six deliberately unselected old
mathematical changes remain admitted by selective bridge helpers; complete
actual prior captures remain byte-pinned.

Synthetic cases cover unequal translated/signed-origin tiles, arbitrary tile
order with matching columns, wrong labels/bases/ownership, thin positive
rectangles, null versus defined-zero targets, mixed/all-undefined subsets,
nonzero undefined raw enclosure outputs, no receiver rows, cancellations,
all signed endpoints, epsilon scaling, actual evaluator call inventories,
detachment, shared children versus cycles, and shape-before-arithmetic guards.
Separate small workloads exercise cap edges, including 256 tiles; combined
worst-case admission limits are not a work or memory guarantee.

Authors' normal/-O hand suites and root's independent three-case literal
checks passed. Ruff check/format checks and scoped whitespace pass. The expected
optimized pytest warning concerns assertions outside rewritten test modules;
engine guards use explicit exceptions and isolated subprocess tests.
This is not exhaustive hostile-input or generic production API hardening.

## Freeze and evidence lifecycle

Five sources were frozen at 2026-09-09 00:12:28 UTC before any assembled fixed
AW input, geometry check, synthesis, scale, map, gain or witness calculation.
All 142 identities were bracketed: five current sources, 53 prior captures and 84
ancestor sources. The selected AR capture is already in AV's authenticated
ancestry and is not counted twice.

1. First external primary/reference comparison: 13.7786 s.
2. Exactly ONE independent normal reference-only read-only audit: 9.2168 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 13.6513 s.
5. Exclusive final comparison capture: 13.6089 s.
6. Fresh primary-normal / reference--O read-only replays: 5.6398 s / 9.1609 s.

The audit and full tests ran concurrently after the first comparison; both
finished before preflight. All non-runtime first/preflight/final fields match
and all source identities/capture bytes remain unchanged. Timing is verification
cost, not an application benchmark. Capture and serialized working caps do not
bound process memory or computation.

Before preregistration, the published AR schema and rectangle inventories were
inspected to specify this bridge; no assembled fixed AW input, scales or error
calculus was computed. Before freeze, one prose ambiguity was clarified:
positive-scale zero-response means zero SHARED gain, not necessarily zero
enclosure gain. All independently authored mathematics already used that
distinction. There were NO post-first source, protocol, fixture or mathematical
corrections.

Final capture: 1,341,549 bytes, SHA256
`e14e357309ff98f9f93c8f23c603f62d9bf17b01b4515ee122a464671b205916`.
Suite: 1,320,632 bytes, SHA256
`7cfca83fa97f9dbbf015cd21fd64195dbeb8e3531c5fce94fea440af47f17096`.

## Next proposed gate: QR-05AX

Test a declared tilewise bilinear signed field-error class,
deltaF=V^2 sum_corner c_a phi_a(xi,eta), |c_a|<=1, with the four nonnegative
bilinear corner basis functions. Derive its exact local moment map Q and
authenticate endpoint fields and their actual integrals before passing
x=Q c and e=W x through the SAME B,G,D and target scales.

This is a smaller error body, not fewer coordinates or improved measurements.
Keep corner coefficients, local moments and raw moments distinct; inverse W
recovers Q c, not c. Check sharp field-class bounds against AW's larger box,
including all null semantics and coordinate transport. Check any positivity
or constant-field extremizers explicitly rather than assuming them for generic G.

The field may jump at tile boundaries; signed perturbations need not preserve
nonnegativity of a total source. Do not claim empirical calibration, arbitrary
bounded-field sharpness, a new source dictionary, physical realization or
gravity. No fixed AX field synthesis, moment map, gain or witness calculation
has run.
