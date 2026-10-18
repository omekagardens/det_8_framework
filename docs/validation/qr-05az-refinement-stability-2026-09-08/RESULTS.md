# QR-05AZ results: refinement stability of bounded-field responses

8 September 2026 (Honolulu). Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AY commit
`f40149f5db5edcb62981e0a969df45e22574a99e`.

## Main result

Quartering every supplied integration tile preserves the exact response gains
for ALL measurable signed fields bounded by V² almost everywhere, in both
supplied geometries. All 64 parent certificates per family are inherited.
The sharp maximum remains **1** at rows 6,7,15,23,31.

The conservative corner envelope strictly decreases on **26 rows per family**.
Its largest excess over the exact gain falls from **3/4 to 5/16**.
The envelope is still loose on those 26 rows: refinement improves the
certificate's approximation, not the underlying measurement precision.
There are 38 envelope ties, including 33 zero rows and five positive rows.

Independently integrated parent and child moment maps, kernel integrals,
Bernstein coefficients, raw responses and normalized responses obey every
declared transport identity exactly. The actual paired field pipelines
give the same receiver observations and decoded outputs on both partitions.
The receiver count stays 37; the decoder, physical kernels and target scales
are unchanged. Increasing bank coordinates from 48 to 192 is a different
representation, not 144 extra measurements.

| Fixed result, identical census in grid and warp | Parent | Child |
|---|---:|---:|
| Positive cells | 8 | 8 |
| Integration tiles | 12 | 48 |
| Raw global-moment coordinates | 48 | 192 |
| Receiver / target coordinates | 37 / 64 | 37 / 64 |
| Defined / undefined target rows | 64 / 0 | 64 / 0 |
| Certified / uncertified rows | 64 / 0 | 64 / 0 |
| Globally nonnegative / nonpositive / zero kernels | 64 / 33 / 33 | 64 / 33 / 33 |
| Nonzero nonnegative / zero target-tile kernels | 46 / 722 | 184 / 2,888 |
| Mixed target-tile kernels | 0 | 0 |
| Sharp maximum C=L=S | 1 | 1 |
| Corner-envelope maximum U | 1 | 1 |
| Rows maximizing U | 20 | 5 |
| Rows with U>S | 26 | 26 |
| Largest rowwise U-S | 3/4 | 5/16 |

Zero kernels belong to both nonnegative and nonpositive row lists.
Target-tile counts count all 64 times 12 or 48 pairs, not geometric tiles.

All rows have unchanged C, L and certified S. For either lower-gain
comparison, the maximum gap is zero and ALL 64 rows tie. For U, the largest
decrease is **7/16**, at rows 9,18,36,63, targets (2,2),(3,3),(5,5),(10,10).
These rows have S=1/4 and U changing from 1 to 9/16. Thus the remaining
gap is 5/16; comparing only global maxima would miss this improvement.

The exact maximizing rows 6,7,15,23,31 are targets
(1,9),(1,10),(2,10),(3,10),(4,10). The child envelope now has exactly these
same maximizing rows. The parent envelope maximizers were
2,4,6,7,9,10,11,13,14,15,18,22,23,31,36,38,39,47,55,63.

The 26 strict decreases, also the 26 still-loose rows, are
0,1,2,3,4,5,9,10,11,13,14,18,19,21,22,27,29,30,36,38,39,45,47,54,55,63.
All remaining rows are ties. There are no unavailable comparisons and no
newly certified or still-uncertified fixed rows.

## Mathematical contract and why it holds

Use dmu=du*dv/2, probe volume V, and target scales
sigma_i=V² h_C h_D. Normalized statements apply only when sigma_i>0.
The kernel on tile t is the supplied bilinear polynomial

```text
k_it(u,v) = sum_j G_i,4t+j (1,u,v,uv)_j
response_i(deltaF) = sum_t integral_tile deltaF * k_it dmu
```

The measurable-field uncertainty set is |deltaF|<=V² almost everywhere
on the SAME probe at both levels. Discontinuities across tile boundaries
are admitted; the boundaries have measure zero. In particular, refinement
does not change the uncertainty set by requiring a smaller child-based
amplitude or new continuity assumptions.

Let e contain the actual raw global moments of a field, in order (1,u,v,uv).
R simply adds each child's four entries into its named parent block:

```text
e_parent = R e_child
B_child = B_parent R
G_child = G_parent R
D_child = D_parent
D B = G                         at both levels, over the full raw bank
```

No child volume or Jacobian factor belongs in R. Normalized local moments
would require a different transport; they are not the bank variables here.

For parent corners c, E evaluates the parent bilinear basis at each actual
child vertex. Each row of E is nonnegative and sums to one. Consequently
E c stays in the child unit cube whenever c is in the parent unit cube,
and it represents EXACTLY the same physical field. The gate stores sparse
4-by-4 restriction blocks and lineage, not dense R or E matrices.

Each P block is independently obtained by integrating its own physical
corner-basis fields deltaF=V² sum_a c_a phi_a against global monomials.
The comparison checks, rather than defines, these identities:

```text
P_parent = R P_child E
integral_parent k = sum_children integral_child k
Bernstein_parent = Bernstein_child E
J_parent = J_child E               J = V² Bernstein
A_parent = A_child E               A_i = J_i / sigma_i
```

The same global polynomial is used on each named parent's children.
Complete coefficient, moment, observed, direct, decoded and normalized
residuals for the prescribed parent/child field pairs are exactly zero.
A null target's normalized output would remain NULL; it is not changed
to zero by a zero raw field response.

For a defined target, retain

```text
C = (V²/sigma) sum_t |integral_tile k dmu|
L = sum_t,a |A_ta|
S = (V²/sigma) integral_probe |k| dmu
U = (V²/sigma) sum_t h_t max_corner |k|

C <= L <= S <= U
C_child >= C_parent
L_child >= L_parent
U_child <= U_parent
```

C is the sharp tile-constant gain, L the sharp corner-bilinear gain, and S
the analytic sharp gain over the full measurable-field domain. The signed
field V² sign(k) attains S. C monotonicity follows from the triangle
inequality under additive integrals. L monotonicity follows from inclusion
of the parent cube through E in the independent child cube. For U, each
child's kernel extrema lie between parent corner extrema, and child
volumes sum to their parent volume. These arguments give weak inequalities,
not a strict-improvement or convergence-rate promise.

S is representation-invariant because neither the kernel nor the
measurable-field domain changes. Parent sign-definite tiles remain
sign-definite under restriction. On any fully sign-certified row,
S=C=L and signed tile constants attain it. A mixed parent may resolve
or remain mixed after a finite subdivision. The gate does not integrate
absolute mixed bilinear polynomials or promote an uncertified NULL to a
numerical exact value in the parent-level record.

Both fixed probes have V=1/2 and actual positive constant field V²=1/4.
All fixed kernels are globally nonnegative. Therefore the positive
constant attains every fixed sharp upper response bound simultaneously at
both levels, and its negative attains every lower bound. This fixed
property is stronger than generic tilewise sign certification.

## Complete positive-row comparison

Indices are zero-based original target rows. In every entry below,
S=C=L at BOTH levels. All other 33 rows are identically zero at both levels.
Equal maxima do not imply equal row gains across the two geometries.

| Row / target | Grid S | Warp S | Grid U parent → child | Warp U parent → child |
|---|---:|---:|---:|---:|
| 0 / (1,1) | 1/4 | 1/4 | 3/4 → 15/32 | 13/16 → 63/128 |
| 1 / (1,2) | 1/4 | 1/8 | 1/2 → 3/8 | 1/4 → 3/16 |
| 2 / (1,3) | 3/4 | 5/8 | 1 → 7/8 | 1 → 13/16 |
| 3 / (1,4) | 1/2 | 1/2 | 3/4 → 5/8 | 13/16 → 21/32 |
| 4 / (1,5) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 5 / (1,7) | 1/2 | 1/2 | 3/4 → 5/8 | 13/16 → 21/32 |
| 6 / (1,9) | 1 | 1 | 1 → 1 | 1 → 1 |
| 7 / (1,10) | 1 | 1 | 1 → 1 | 1 → 1 |
| 9 / (2,2) | 1/4 | 1/4 | 1 → 9/16 | 1 → 9/16 |
| 10 / (2,3) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 11 / (2,4) | 3/4 | 7/8 | 1 → 7/8 | 1 → 15/16 |
| 13 / (2,7) | 3/4 | 7/8 | 1 → 7/8 | 1 → 15/16 |
| 14 / (2,9) | 3/4 | 19/24 | 1 → 7/8 | 1 → 43/48 |
| 15 / (2,10) | 1 | 1 | 1 → 1 | 1 → 1 |
| 18 / (3,3) | 1/4 | 1/4 | 1 → 9/16 | 1 → 9/16 |
| 19 / (3,4) | 1/4 | 3/8 | 1/2 → 3/8 | 3/4 → 9/16 |
| 21 / (3,7) | 1/4 | 3/8 | 1/2 → 3/8 | 3/4 → 9/16 |
| 22 / (3,9) | 3/4 | 19/24 | 1 → 7/8 | 1 → 43/48 |
| 23 / (3,10) | 1 | 1 | 1 → 1 | 1 → 1 |
| 27 / (4,4) | 1/4 | 1/4 | 3/4 → 15/32 | 13/16 → 63/128 |
| 29 / (4,7) | 1/2 | 1/2 | 3/4 → 5/8 | 13/16 → 21/32 |
| 30 / (4,9) | 1/4 | 7/24 | 1/2 → 3/8 | 7/12 → 7/16 |
| 31 / (4,10) | 1 | 1 | 1 → 1 | 1 → 1 |
| 36 / (5,5) | 1/4 | 1/4 | 1 → 9/16 | 1 → 9/16 |
| 38 / (5,9) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 39 / (5,10) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 45 / (7,7) | 1/4 | 1/4 | 3/4 → 15/32 | 13/16 → 63/128 |
| 47 / (7,10) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 54 / (9,9) | 1/4 | 1/4 | 3/4 → 15/32 | 109/144 → 181/384 |
| 55 / (9,10) | 1/2 | 1/2 | 1 → 3/4 | 1 → 3/4 |
| 63 / (10,10) | 1/4 | 1/4 | 1 → 9/16 | 1 → 9/16 |

## Controls against misleading refinement claims

On a unit probe/tile, V=1/2 and sigma=1/16, take k=u-1/4.
The parent has C=L=1/2, U=3/2 and an uncertified exact gain.

- Splitting at u=1/2 keeps part of the kernel mixed. Child C remains 1/2,
  L rises to 7/12, and U falls to 1. The child A row is
  (-1,1,-1,1,5,7,5,7)/48. A child maximizer uses corner signs
  (-1,1,-1,1,1,1,1,1), outside the parent-bilinear image. The finite
  subclass has enlarged, but the full bounded-field set has not.
- Splitting at u=1/4 resolves the sign boundary. The child is newly
  certified with C=L=S=5/8, while U=5/4 remains loose. The parent's
  exact-gain field stays NULL, even though the child certificate now
  gives the sharp gain of the same physical functional.
- A one-child identity leaves all level records equal. For k=u*v,
  C=L=S=1/2 while U=2: a certificate is not envelope sharpness.

Additional controls cover an unresolved mixed saddle, opposite signed
tiles, unequal/reordered partitions, translated/scaled geometries, two-stage
restriction and raw-aggregation composition, fields outside the parent
image, cancellation, empty receivers, defined zeros, mixed/null rows and
an all-undefined query. Raw global moments are checked against the tempting
but incorrect unweighted summation of normalized local moments.

The root's literal parent pattern on the unit mixed example has corners
(-1,0,1,1/2), physical global coefficients (-1/4,1/4,1/2,-3/8),
and raw moments (1/64,1/96,1/48,1/96). At the midpoint split the child
corners are (-1,-1/2,1,3/4,-1/2,0,3/4,1/2), with the same global
coefficients on both children. Adding their raw moments reproduces
the parent values exactly.

## Actual witnesses and observation access

The retained canonical maximum witnesses select the FIRST maximizing row,
row 6 in both families, while every tied maximum remains in the bound records.
Parent tile signs are +1 on tiles 0,1 and zero elsewhere; the corresponding
child signs are +1 on tiles 0 through 7 and zero elsewhere. Bilinear signs
repeat these tile signs four times. Negative witnesses negate every sign.
All four selected signed maxima attain +/-1.

Each family retains eight actual parent/child PAIRS and four standalone
child pipelines. These include signed nonconstant patterns, signed global
constants, parent constant/bilinear maxima carried through E, and child
constant/bilinear maxima. Each pipeline actually executes

```text
corners -> integrate -> physical coefficients, extrema and raw moments e
e -> produce(B,e) -> observed error -> apply(D,observed)
e -> produce(G,e) -> direct error
```

All off-target outputs remain present. Actual field bounds, equality of
direct and decoded errors, rowwise bounds and prescribed signed attainment
are checked. No full per-row endpoint bank is claimed: there are 20
pipelines per fixed family, requiring 20 integrate, 40 produce and 20 apply
calls. The reference additionally performs 48+192=240 produce/apply pairs
for independent full-bank column probes, not extra field witnesses.

A generic all-undefined family still executes four PAIRS, hence eight
pipelines; the four maximizing groups are NULL. It does not substitute
empty constant fields. Nonzero cancelling decoder rows and raw outputs
are preserved separately from normalized availability.

## Historical, computational and application boundaries

Only AY's pinned nine-field problems supply the fixed inputs. Each actual
parent tile is quartered once at its two midpoints, in frozen parent-outer,
00/10/01/11 child order. No subdivision was selected after seeing a gain.
Independent parent geometry, kernels, maps, bounds and certificates agree
with the selected AY records exactly.

AY witnesses, comparison records and counts are not replayed; neither
are AX auxiliary maps, older executors, source/target integrals, overlays,
decoder fits, filters or ranks. New AZ parent/child basis, kernel and
field integrals are explicitly part of the gate.

Useful application: change an integration mesh while preserving an
already justified measurement/response contract, and tighten a finite
error enclosure without confusing discretization with physical information.
The generic controls also show where richer finite field coordinates
expose behavior excluded by a coarse bilinear ansatz. This is a supplied-
geometry calculus contract, not reconstruction of unknown geometry.

No apparatus uncertainty was calibrated, no sensor was improved, no total
source nonnegativity or global continuity was guaranteed, no full-field
recovery or stability was proved, and no quantum channel, gravity dynamics,
ontology, RET integration or Lean proof was established. Separate input
caps and 4096-bit retained rational checks are bounded admission controls,
not exhaustive hostile-graph, memory, work or generic production hardening.

## Complete retained counts and bytes

Counts include rational zeroes and repeated occurrences, not NULLs, signs,
labels, lineage indices or the integer count values themselves. Both fixed
families have the same count vector; values and byte lengths can differ.

| Retained census | Per family | Both families |
|---|---:|---:|
| bilinear_strict | 0 | 0 |
| bound_entries | 520 | 1,040 |
| cells | 8 | 16 |
| certification_bridge_entries | 64 | 128 |
| child_bank_values | 192 | 384 |
| child_kernel_entries | 36,864 | 73,728 |
| child_map_entries | 49,152 | 98,304 |
| child_problem_geometry_entries | 228 | 456 |
| child_problem_matrix_entries | 21,760 | 43,520 |
| child_tiles | 48 | 96 |
| child_witnesses | 4 | 8 |
| comparison_entries | 195 | 390 |
| constant_strict | 0 | 0 |
| defined_rows | 64 | 128 |
| geometry_entries | 133 | 266 |
| inherited_rows | 64 | 128 |
| input_geometry_entries | 276 | 552 |
| input_matrix_entries | 7,216 | 14,432 |
| newly_certified_rows | 0 | 0 |
| parent_bank_values | 48 | 96 |
| parent_kernel_entries | 9,216 | 18,432 |
| parent_map_entries | 12,288 | 24,576 |
| parent_paired_witnesses | 8 | 16 |
| parent_tiles | 12 | 24 |
| positive_cells | 8 | 16 |
| receiver_values | 37 | 74 |
| restriction_entries | 2,400 | 4,800 |
| sign_entries | 300 | 600 |
| still_uncertified_rows | 0 | 0 |
| target_rows | 64 | 128 |
| transport_entries | 19,968 | 39,936 |
| undefined_rows | 0 | 0 |
| upper_strict | 26 | 52 |
| witness_entries | 18,124 | 36,248 |

| Canonical JSON projection, bytes | Grid | Warp |
|---|---:|---:|
| certification_bridge_bytes | 690 | 690 |
| child_problem_bytes | 139,798 | 140,074 |
| comparison_bytes | 2,443 | 2,465 |
| geometry_bytes | 1,483 | 1,654 |
| input_bytes | 49,725 | 49,901 |
| level_bytes | 704,971 | 711,753 |
| native_family_bytes | 1,169,163 | 1,185,057 |
| restriction_bytes | 20,298 | 22,131 |
| transport_bytes | 122,628 | 123,714 |
| witness_bytes | 125,707 | 131,255 |

Byte sizes are canonical JSON plus newline for overlapping projections.
They are not additive unique storage, minimal encodings, packets, physical
sensor costs or application benchmarks. The mathematical suite is
2,356,999 bytes, SHA256
`1201523d977ee92d55a45d96ca7b767b840d1eeba18d88c3df2ad0a7e5b9fb5a`.

## Verification and evidence lifecycle

Three separately authored routes were used: primary global monomial
antiderivatives and separable basis blocks; reference physical polynomial
interpolation and tensor-Simpson integration with independent column probes;
and a third polynomial-dictionary/antiderivative test oracle. No mathematical
helper was shared across these routes and no older executor was imported.
The root read every current source. Each engine received its own synthetic
checks; independent runner and test lifecycle/history reviews cleared.

Before any fixed AZ projection or calculation, the final generic suite
passed **62 tests, 10 fixed tests deselected**, normal in 32.50 s and
optimized in 32.46 s. Separate normal/optimized root literal checks passed
seven synthetic scenarios on both engines. The primary author's independent
checks covered 24 complete synthetic wires; the reference author's covered
45, including independently transformed cases. These are bounded controls,
not a production-hardening claim or independent physical evidence.

The retained tests include **299 explicit rejection cases per engine**:
143 family, 29 produce, 29 apply, 37 integrate, 35 inspect,
11 additional overflow/cycle, and 15 staged pre-arithmetic controls.
Both engines are tested in separate normal and optimized guard subprocesses:
598 explicit rejections per isolated mode. Separate cap-edge cases do not
claim a combined worst-case memory or work test.

Complete wire-comparison corruption coverage is **1,047 non-noop mutations**:
607 across three generic families, 418 across two fixed families (209 each),
eight suite mutations, and 14 selected-history mutations. Four unselected
historical mutations are deliberately admitted by the selected bridge.
Eleven malformed synthetic fixed-shaped projections are rejected.
This bounded mutation menu is not exhaustive corruption detection.

Five sources were frozen at **2026-09-09 02:18:38.164284 UTC**, before
constructing fixed child rectangles or evaluating their mathematics.
The inventory is **160 distinct identities**: five current sources,
56 prior captures and 99 ancestor sources. The external freeze receipt
is 23,108 bytes, SHA256
`99ba43a498023a29057ed90973905e95a9a7b91cc589969ff0615919e20d9c27`.

| Frozen source | Bytes | SHA256 |
|---|---:|---|
| README.md | 20,218 | e531de45243fad55765e1bbf54828635e826c7c74f41d6a4b00c343b45a49063 |
| kernel.py | 43,881 | 8c24549232629024e2161b67059b7c832113946553d642a985a6bb18307ea5a9 |
| reference.py | 46,261 | b0ef360abe4b82fd6e9b83e744ea2d0bb574a2701d6ea2a47599ba5cbb35356d |
| study.py | 40,941 | 198237a7269eea66b21db378b3b27fb3c39338a26dd1bdf21a094d2dde1806d0 |
| test_qr05az.py | 101,655 | 68cf550796b6d1a23ff80adb36b02d9772f5288632a64477e2b2d00139ab121c |

The first comparison passed in 26.9043 s, producing 2,380,557 bytes,
SHA256 `24770d78b68515e1d1356003009380dd2cac849b0cf581b11575c9b400c8ab96`.
Exactly ONE independent normal reference-only read-only audit passed
in 17.5143 s. Before/after brackets preserved all 160 identities, the
freeze receipt and every first-capture byte.

The full suite passed **72 tests** normally in **292.24 s** and optimized
in **289.39 s**. Optimized pytest emitted its expected warning about
ordinary non-rewritten assertions; engine admission uses explicit errors
and the optimized guard subprocess checks passed. Post-test identity and
first-capture-byte brackets passed.

The external create-only comparison preflight passed in 26.9257 s:
2,380,560 bytes, SHA256
`6b49865acbabd480d6e4fbf997aab0f823c5d90442295ac982e3cc9bab82b439`.
The exclusive final comparison capture passed in 26.7913 s:
**2,380,556 bytes**, SHA256
`cbb04f7a4af49a5714ecf80652393933557f490f7e16dab0848b8d32cda27585`.

Fresh read-only replays then passed: primary normal **11.6308 s**,
reference optimized **17.0568 s**. A final bracket confirmed all
160 source/evidence identities and all first/preflight/final capture bytes
unchanged. All three captures have identical non-runtime records and
the same complete mathematical suite. There were no post-first source,
protocol, input, fixture, schema or mathematical-result corrections.

Capture runtime is verification timing, excluding final serialization;
it is not an application benchmark. The final capture's runtime records
Python 3.11.6, isolated normal compare mode, a fresh external cache and the
actual high-water RSS. The 128 MiB capture and 192 MiB serialized-working
bounds are not process-memory or computational-work limits.

Disclosure: no engine or mathematical-formula correction was needed.
Before freeze, the primary author's external synthetic harness required a
loop-variable rename after shadowing its maximum helper; the test author's
first generic run passed 56 tests before its corruption-leaf helper treated
an integer list as a rational pair. That test-only helper was corrected,
then both complete generic modes passed. Root runner drafting included
mechanical naming/import/format cleanup and an explicit full DB=G/zero
bank-residual assertion, all before freeze. A report-only wording
clarification distinguishes sharp response limits S from loose envelopes U.
No frozen source or fixed-result correction has occurred.

Reproduction uses the existing Python 3.11.6 environment, isolated mode,
fresh external caches, and no new dependency installation. From the checkout:

```sh
.venv/bin/python -I -X pycache_prefix=/tmp/qr05az-reader-normal -m pytest -q -p no:cacheprovider docs/validation/qr-05az-refinement-stability-2026-09-08/test_qr05az.py
.venv/bin/python -I -O -X pycache_prefix=/tmp/qr05az-reader-opt -m pytest -q -p no:cacheprovider docs/validation/qr-05az-refinement-stability-2026-09-08/test_qr05az.py
.venv/bin/python -I -X pycache_prefix=/tmp/qr05az-reader-primary docs/validation/qr-05az-refinement-stability-2026-09-08/study.py --verify --route primary
.venv/bin/python -I -O -X pycache_prefix=/tmp/qr05az-reader-reference docs/validation/qr-05az-refinement-stability-2026-09-08/study.py --verify --route reference
```

Choose previously unused external cache paths for fresh reproductions.
Verification is read-only; normal capture creation refuses to overwrite an
existing artifact. RESULTS and the roadmap are deliberately outside the
five-source ledger. Publication is limited to the gate's seven files plus
the roadmap, preserving all unrelated RET/core/governance work and
the untracked temporary model sheet.

## Next proposed gate: QR-05BA

Compose field-model error with a SEPARATELY declared acquisition-error
set at the 37 receiver outputs, keeping the frozen linear response map.
For y=B e(deltaF)+n, declare |deltaF|<=epsilon V² and
|n_j|<=eta rho_j. The Cartesian product is a deterministic admissibility
assumption, not statistical independence or empirical calibration.
Do not count the field-induced receiver error a second time as n.

For defined rows, a declared receiver box has gain
gamma_i=sum_j |D_ij| rho_j / sigma_i. The sharp composed full-domain
expression is epsilon S_i+eta gamma_i. Supply a numerical exact value
where the field gain is certified, or where epsilon=0 makes the field
term irrelevant. Otherwise retain attainable constant/bilinear lower
bounds plus the receiver term and the conservative U upper envelope.

A prospective BA protocol should freeze its budgets, coordinate units,
selected input quantities and actual joint signed-witness requirements
before fixed evaluation. Preserve off-target outputs, null normalized rows
with potentially nonzero raw D n, all maxima/ties, and degenerate budgets.
Receiver-coordinate changes must transport the uncertainty set; a fresh
axis-aligned box usually changes it. No BA fixed calculation has run.
