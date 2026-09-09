# QR-05AY results: kernel sign certificates and bounded-field envelopes

8 September 2026 (Honolulu). Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AX commit `ba75d99766fed10b7b826119fbf579cad6125c86`.

## Main result

The earlier bilinear-field gains are now certified sharp for **ALL measurable
signed perturbations bounded by V² almost everywhere**, in both supplied
geometries. Every actual response kernel is nonnegative on every tile.
All 64 target rows per family are certified, with sharp maximum normalized
gain **1** at rows 6,7,15,23,31, targets (1,9),(1,10),(2,10),(3,10),(4,10).

This conclusion comes from the ACTUAL kernel corner signs and exact
integrals, not merely the nonnegative integrated coefficients found in AX.
The all-positive constant field attains every upper response bound, and
the all-negative constant attains every lower response bound, including
zero rows. The broader field class changes none of these fixed row gains.

This is a stronger mathematical error certificate for the SAME supplied
geometry and response maps. It does not establish apparatus noise levels,
improved equal-noise precision, unknown geometry, physical field preparation,
a quantum channel, a gravity law or an ontological premise.

| Bounded-measurable-field certificate | Grid | Warp |
|---|---:|---:|
| Positive cells / tiles | 8 / 12 | 8 / 12 |
| Bank / receiver / target coordinates | 48 / 37 / 64 | 48 / 37 / 64 |
| Defined / undefined target rows | 64 / 0 | 64 / 0 |
| Certified / uncertified rows | 64 / 0 | 64 / 0 |
| Globally nonnegative / nonpositive / zero kernels | 64 / 33 / 33 | 64 / 33 / 33 |
| Nonnegative nonzero / zero target-tile kernels | 46 / 722 | 46 / 722 |
| Mixed target-tile kernels | 0 | 0 |
| Sharp all-bounded-field maximum S | 1 | 1 |
| All sharp maximizing rows | 6,7,15,23,31 | 6,7,15,23,31 |
| Corner-envelope maximum U | 1 | 1 |
| Envelope maximizing rows, count | 20 | 20 |
| Strict envelope-minus-sharp gaps / ties | 26 / 38 | 26 / 38 |
| Largest rowwise envelope gap | 3/4 | 3/4 |
| All largest-gap rows | 9,18,36,63 | 9,18,36,63 |

Zero kernels belong to both nonnegative and nonpositive row lists.
There are 31 nonzero rows and 33 zero rows in each family. Target-tile counts
include all 64*12 pairs; they are not numbers of geometric tiles.

The corner envelope has the same global maximum 1, but is **not sharp on
26 individual rows**. Its 20 maximizing rows are
2,4,6,7,9,10,11,13,14,15,18,22,23,31,36,38,39,47,55,63.
Only five of these maximize the actual sharp gain. In particular,
rows 9,18,36,63 have S=1/4 and U=1, so the largest rowwise gap is 3/4,
not the difference 0 between the two global maxima.

## Why the larger field class is certified

Use the supplied measure dmu=du*dv/2. Write V for probe volume, h_t for
tile volume and sigma_i=V² h_C h_D for target i=(C,D).
The normalized formulas below use defined targets sigma_i>0 and epsilon>=0.
For a bank with monomial order (1,u,v,uv), its target kernel on tile t is

```text
k_it(u,v) = sum_j G_i,4t+j (1,u,v,uv)_j
response_i(deltaF) = sum_t integral_tile deltaF * k_it dmu

S_i = (V²/sigma_i) sum_t integral_tile |k_it| dmu
|response_i(deltaF)| / sigma_i <= epsilon S_i
                 when |deltaF| <= epsilon V² almost everywhere.
```

The inequality follows pointwise; equality is attained by the admitted
measurable field deltaF=epsilon V² sign(k_i). Thus S is an analytic sharp
gain for the full bounded-field class, not a sampled maximization claim.
No continuity or total-source nonnegativity is assumed.

A bilinear kernel is the convex combination of its four actual corner
values in order 00,10,01,11. Four nonnegative corners therefore certify
nonnegativity throughout the tile; four nonpositive corners certify the
opposite sign. Zero edges/corners are allowed. If every tile is sign-definite,
a tilewise constant sign field attains S without integrating the absolute
value of a sign-changing polynomial.

The finite quantities retained in this gate are

```text
C_i = (V²/sigma_i) sum_t |integral_tile k_it dmu|
A_i,4t+a = (V²/sigma_i) integral_tile k_it * phi_ta dmu
L_i = sum_t,a |A_i,4t+a|
U_i = (V²/sigma_i) sum_t h_t max_corner |k_it|

C_i <= L_i <= S_i <= U_i.
Every tile sign-definite: certified S_i = C_i = L_i.
```

Here C is attained by signed tile constants, L is the sharp bilinear-class
gain from AX's nonnegative corner basis, and U is a finite corner-supremum
envelope. U need not be attained even when exact S is certified.
AY does not compute absolute mixed-bilinear integrals or general mixed
sign-field moments.

On both fixed probes V=1/2, so the positive constant control is deltaF=1/4.
All kernels are globally nonnegative, not just separately sign-definite;
the same constant therefore attains all upper bounds simultaneously.
This is a verified property of these two families, not a generic API promise.
The canonical maximizing row witnesses instead use normalized corner signs
+1 on tiles 0,1 for rows 6,7; tile 2 for row 15; tile 3 for row 23;
tiles 4,5 for row 31, and zero elsewhere. The corresponding physical field
is V² times those signs. Negative witnesses reverse them.

All 64 fixed rows have C=L=S, matching AX's bilinear row gains exactly.
The strict U-S rows in both families are
0,1,2,3,4,5,9,10,11,13,14,18,19,21,22,27,29,30,36,38,39,45,47,54,55,63.
The 38 ties consist of 33 zero rows and the five positive sharp maximizers.

## Complete positive-row comparison

Indices are zero-based original target rows. Every one of the 31 positive
rows is listed; the other 33 have C=L=S=U=0 in both families.

| Row / target | Grid S=C=L | Warp S=C=L | Grid U | Warp U |
|---|---:|---:|---:|---:|
| 0 / (1,1) | 1/4 | 1/4 | 3/4 | 13/16 |
| 1 / (1,2) | 1/4 | 1/8 | 1/2 | 1/4 |
| 2 / (1,3) | 3/4 | 5/8 | 1 | 1 |
| 3 / (1,4) | 1/2 | 1/2 | 3/4 | 13/16 |
| 4 / (1,5) | 1/2 | 1/2 | 1 | 1 |
| 5 / (1,7) | 1/2 | 1/2 | 3/4 | 13/16 |
| 6 / (1,9) | 1 | 1 | 1 | 1 |
| 7 / (1,10) | 1 | 1 | 1 | 1 |
| 9 / (2,2) | 1/4 | 1/4 | 1 | 1 |
| 10 / (2,3) | 1/2 | 1/2 | 1 | 1 |
| 11 / (2,4) | 3/4 | 7/8 | 1 | 1 |
| 13 / (2,7) | 3/4 | 7/8 | 1 | 1 |
| 14 / (2,9) | 3/4 | 19/24 | 1 | 1 |
| 15 / (2,10) | 1 | 1 | 1 | 1 |
| 18 / (3,3) | 1/4 | 1/4 | 1 | 1 |
| 19 / (3,4) | 1/4 | 3/8 | 1/2 | 3/4 |
| 21 / (3,7) | 1/4 | 3/8 | 1/2 | 3/4 |
| 22 / (3,9) | 3/4 | 19/24 | 1 | 1 |
| 23 / (3,10) | 1 | 1 | 1 | 1 |
| 27 / (4,4) | 1/4 | 1/4 | 3/4 | 13/16 |
| 29 / (4,7) | 1/2 | 1/2 | 3/4 | 13/16 |
| 30 / (4,9) | 1/4 | 7/24 | 1/2 | 7/12 |
| 31 / (4,10) | 1 | 1 | 1 | 1 |
| 36 / (5,5) | 1/4 | 1/4 | 1 | 1 |
| 38 / (5,9) | 1/2 | 1/2 | 1 | 1 |
| 39 / (5,10) | 1/2 | 1/2 | 1 | 1 |
| 45 / (7,7) | 1/4 | 1/4 | 3/4 | 13/16 |
| 47 / (7,10) | 1/2 | 1/2 | 1 | 1 |
| 54 / (9,9) | 1/4 | 1/4 | 3/4 | 109/144 |
| 55 / (9,10) | 1/2 | 1/2 | 1 | 1 |
| 63 / (10,10) | 1/4 | 1/4 | 1 | 1 |

Equal maxima do not imply identical geometry, row gains or response maps.
For example, row 1 has gain 1/4 in grid and 1/8 in warp.

## Counterexamples and endpoint checks

Three small synthetic controls distinguish the certificate from weaker claims.
The first two use a unit probe/tile with B=I4 and sigma=1/16:

- k=u-1/4 has corners (-1/4,3/4,-1/4,3/4), but its integrated normalized
  coefficients are (1/24,5/24,1/24,5/24), all positive. C=L=1/2 and U=3/2.
  AY correctly retains the mixed-tile obstruction and leaves exact gain
  NULL. Positive integrated coefficients do not establish pointwise positivity.
- k=u*v has zero edges but nonnegative corners. It is certified with
  C=L=S=1/2, while U=2: certification does not make the envelope sharp.
- With two half-width tiles and kernels +1 and -1 respectively, C=L=S=U=2.
  A signed tile-constant field attains the bound; either global constant
  has response zero. Opposite signs across tiles do not obstruct certification.

Additional saddle, mixed/null, cancelling-decoder, defined-zero and
all-undefined cases preserve the distinctions between an undefined
normalization, an uncertified exact gain and a genuinely zero response.
For a mixed tile, every obstruction is retained with canonical first
positive/negative corner indices; it is not reclassified as unbounded or zero.
An all-undefined query still runs both complete constant pipelines.

Each fixed family retains 128 signed tile-constant endpoints, 128 signed
bilinear endpoints and two additional global constants. EVERY endpoint
actually executes the new standalone integration API and the same pipeline:

```text
corners -> actual field coefficients, extrema and integrated raw moments e
e -> produce(B,e) -> observed error -> apply(D,observed)
e -> produce(G,e) -> direct target error
```

All raw off-target values remain present. Direct and decoded responses
agree, normalized responses equal A times corners, fields satisfy the
pointwise amplitude bound, all defined outputs stay inside L and U, and
each designated signed C or L is attained. Both constants retain their
complete pipelines even where designated normalized row witnesses are null.

Per family the endpoint pipeline requires 258 integrate, 516 produce and
258 apply calls. The reference adds 48 produce/apply pairs for independent
full-bank column probes. Full DB=G is checked before restricting errors.
Neither a refit nor agreement only on witness fields can replace it.

## Historical and application boundary

Only AX's same nine problem fields supply the fixed cases. Newly computed
geometry, bilinear maps J/A, row gains L and actual positive constant
responses match the selected pinned AX values. AX endpoint records,
Q/W/inverses, AW baselines and all older executors are not replayed.
New AY kernel and field integrals are explicitly part of this gate.

The calculus can turn a justified pointwise field-error cap into an exact
finite response-error budget even when the perturbation has arbitrary
measurable structure within tiles. For these fixed kernels, restricting that
perturbation to be bilinear was unnecessary to obtain the sharp row bounds.
This is useful for geometry-supplied numerical checks and tolerance analysis.
It does not characterize the entire bounded-field moment body or recover
the field from finitely many responses.

Errors in an acquired receiver reading remain a different input domain.
No empirical amplitude, sensor model, statistical independence, measurement
accuracy, RET integration, Lean proof or physical geometry inference is
established here. The generic supplied G is algebraically admitted; its
physical interpretation is not rederived by validating a rectangle partition.

## Next proposed gate: QR-05AZ, refinement stability

Keep the physical kernel, probe, target-cell regions, reference scales and
receiver observations fixed while subdividing the existing integration tiles.
Check additive raw moments and kernel integrals, preservation of the same
response functional and certified exact gain, and the behavior of the
corner envelope under refinement.

The full bounded-measurable-field domain is unchanged by a finer partition.
A parent bilinear field, however, restricts to correlated child corner data;
allowing independent bilinear fields on children enlarges that FINITE subclass.
These two comparisons must remain explicit. More integration coordinates
must not be reported as more physical measurements.

This is a representation/scale check on supplied geometry, not reconstruction
of unknown geometry or a continuum/gravity derivation. Detailed AZ inputs,
transports, acceptance tests and freeze must precede any fixed AZ calculation.
No fixed AZ refinement has run. Field-plus-acquisition error composition can
follow separately, with apparatus calibration and RET still independently gated.

## Representation and verification

Across both families, input geometry contributes 168 rational occurrences
and input matrices 14,432. Retained geometry contributes 170, kernels 18,432,
maps 24,576, bounds 520 and comparisons 390.

The two signed witness groups contain 512 endpoints, retaining 252,928
rational occurrences. Tile signs contribute 1,536 separately counted entries
and bilinear signs 6,144. The four additional global constants retain 1,972
rational occurrences. Counts include zeros and repetitions, not nulls,
labels, corner/target indices or the count values themselves.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Input problem | 47,365 | 47,433 |
| Geometry | 979 | 1,102 |
| Kernel values and integrals | 64,566 | 65,211 |
| Complete maps | 75,249 | 75,827 |
| Bounds and maxima | 1,879 | 1,911 |
| Certification and obstruction lists | 2,179 | 2,179 |
| Witnesses and constants | 844,595 | 851,661 |
| Comparisons | 2,278 | 2,302 |
| Complete native family | 1,040,572 | 1,049,108 |

The canonical suite is 2,092,414 bytes. These overlapping projections are
not additive unique storage, a minimal encoding or measurement packets.

All **70 tests pass normally and optimized**, in concurrent runs of
168.25 s / 169.25 s. Before freeze, all 60 generic tests passed in each mode
(10.97 s / 10.96 s); the ten fixed tests were deselected. Fixed input loading,
geometry and kernel calculations remain lazy during generic collection/tests.

Primary uses physical monomial antiderivatives and explicit global corner
evaluation with separable corner-basis expansion. Reference independently
interpolates physical vertices, uses exact tensor-Simpson integration and
full raw response-column probes, and reconstructs physical field coefficients
by a Vandermonde inverse. This inverse is not AX's coordinate inverse.
The third oracle uses polynomial dictionaries, antiderivatives and scalar
contractions; small synthetic cubes are enumerated.

Complete native family records, including all endpoint records, agree with
the independent oracle. Each engine's family builder executes every endpoint;
fixed tests additionally re-execute representative endpoints and both constants.
They do not enumerate an infinite-dimensional field ball or re-execute every
endpoint a second time. The sharp general-field conclusion uses the analytic
sign certificate and actual attaining fields.

Each isolated normal/-O guard subprocess checks **522 explicit ValueError
rejections**: per engine, 235 malformed cases, 11 additional overflow/cycle
cases and 15 pre-arithmetic admission checks. All **677 non-noop mutations**
pass: 386 generic-family, 272 fixed-family, eight suite and 11 selected-history
changes. Seven deliberately unselected old endpoint/ancillary changes remain
admitted by selective bridge helpers; actual complete prior capture bytes
remain pinned. Nine synthetic selected-projection rejections also pass.

Controls cover mixed physical signs hidden by positive integrated coefficients,
zero edges, opposite tile signs, saddle fields, undefined and defined-zero
rows, all-undefined constants, no receivers, signed/unequal/translated tiles,
matching tile/column permutations, actual endpoint API call inventories,
positive affine transport, partial/empty public geometry, detached outputs,
shared children versus cycles, retained overflow and cancelling unretained
terms. Shapes and scalar values are admitted before expensive arithmetic.
Separate bounded workloads test cap edges, including 256 tiles and 320
receivers; combined worst-case capacities are not a process resource bound.

Under the declared synthetic affine convention u'=a*u+b,v'=c*v+d,k=ac>0,
the physical field scales by k², kernel corners by k, kernel integrals by k²
and target scales by k⁴. Full raw moment/receiver/target transports and
normalized gains, sign classes, comparisons and witness responses are checked.
The fixed grid and warp are not asserted to be related by a global affine
transformation; no fixed affine variants run.

Authors' independent normal/-O hand suites and root's six literal synthetic
cases passed before freeze. Root separately checked exact mixed-kernel
corners/integrals, the hidden-sign diagnostic, a zero-edge loose envelope,
opposite tile signs, cancelling null targets, all-undefined constants, and
empty inspection/integration. Ruff check/format passes. The staged default
whitespace check flags one extra blank line at EOF in the frozen README;
it is intentionally retained to preserve the source ledger. All other scoped
whitespace checks pass with only that blank-at-EOF category disabled.
The optimized pytest warning concerns assertions outside rewritten test
modules; engine guards use explicit exceptions and are separately exercised
under -O. This is not exhaustive hostile-input or generic production hardening.

## Freeze and evidence lifecycle

The five sources were frozen at **2026-09-09 01:35:06 UTC**, before
assembling fixed AY inputs or evaluating any fixed AY kernel corners,
integrals, maps, bounds or witnesses. The identity bracket covers **154
artifacts**: five current sources, 55 prior captures and 94 ancestor sources.
AX's selected capture remains 1,925,803 bytes with SHA256
`80020730e21d2c5731b6f6d5a94add1faa6739c815ac3e82087126d45667f1b0`.

1. First external primary/reference comparison: 25.6094 s.
2. Exactly ONE independent normal reference-only read-only audit: 13.8678 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 26.1170 s.
5. Exclusive final comparison capture: 25.8542 s.
6. Fresh primary-normal / reference--O read-only replays: 13.4388 s / 13.7660 s.

The independent audit and full tests ran concurrently after the first
comparison; both finished before preflight. Final replay processes used
distinct fresh caches and ran concurrently after the exclusive final capture.
First, preflight and final non-runtime fields agree exactly. Every source
identity and retained capture byte remains unchanged. The runner uses
isolated Python, fresh external caches and create-only evidence writes.
No dependencies were installed.

Before freeze, two authors corrected EXTERNAL hand-harness plumbing:
one needed to rational-encode integer coordinate literals; the other renamed
a list that shadowed its matrix-subtraction helper. Neither correction
changed an engine or an oracle formula. The third test suite passed without
mathematical corrections; ordinary Ruff cleanup bound loop variables and
simplified comprehensions.

During a limited lifecycle review AFTER the primary source was held,
a mistaken line-range request briefly displayed primitive scalar helpers
from the test source. No oracle reconstruction was inspected or used, and
the primary remained unchanged. This is disclosed rather than claiming
absolute source isolation throughout the subsequent reviews.

There were **NO post-first source, protocol, fixture or mathematical
corrections**. Subsequent explanatory report/roadmap edits remain outside
the five-source ledger.

Verification timing is not an application benchmark. The 128 MiB capture
and 192 MiB serialized-working caps do not bound process memory or work.
The first comparison's recorded RSS high water was 275,873,792 bytes.
No combined worst-case or production resource-hardening claim follows.

Final capture: **2,115,070 bytes**, SHA256
`a4dda392b4dd8f148389cb82c4187611c10b11e3f3e05f82e2779fbe3bf90874`.
Suite: **2,092,414 bytes**, SHA256
`5a49a6fc4eed33d3977b2e62b7038f5b71234ef1f36acb868cd3ab0b74491621`.

Only this gate's seven files and the bridge roadmap belong to its publication.
Previous captures and unrelated RET/core/governance work remain untouched;
the local temporary model sheet is not included.
