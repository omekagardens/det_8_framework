# QR-05AX results: bounded bilinear field-error realization

8 September 2026 (Honolulu). Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AW commit `2557a122da2341c87f0bdf544909676ea74ae5c5`.

## Main result

The explicitly integrated, bounded bilinear field-error class has sharp
maximum normalized shared gain **1 in both supplied geometries**, compared
with 4 for AW's larger local-moment box. Both families have **26 strictly
smaller shared row bounds** and 38 ties (33 zero, five positive).

This comparison changes the admitted error body, not the geometry, receiver,
measurements, decoder or target reference units. It does not demonstrate
improved equal-noise sensor precision. The 48 field-corner coordinates still
map invertibly to 48 local moments: there is no dimension reduction.

A useful additional outcome is that ALL 64 integrated normalized response
rows have nonnegative coefficients in both fixed families. The actual
positive constant field attains each upper row bound, with the negative
constant attaining each lower bound. This is verified for the declared
bilinear class; it does not yet certify pointwise positivity of the response
kernel or sharpness over arbitrary bounded fields.

| Unit bounded-bilinear-field certificate | Grid | Warp |
|---|---:|---:|
| Positive cells / tiles | 8 / 12 | 8 / 12 |
| Corner / bank / receiver / target coordinates | 48 / 48 / 37 / 64 | 48 / 48 / 37 / 64 |
| Defined / undefined targets | 64 / 0 | 64 / 0 |
| Sharp shared maximum | 1 | 1 |
| All shared maximizing rows | 6,7,15,23,31 | 6,7,15,23,31 |
| Maximum enclosing receiver-box gain | 135/4 | 1523/180 |
| Unique enclosure maximizing row / target | 18 / (3,3) | 18 / (3,3) |
| Largest rowwise enclosure-minus-field gap | 67/2 | 739/90 |
| Unique largest-gap row | 18 | 18 |
| Strict field-versus-enclosure gaps / ties | 22 / 42 | 22 / 42 |
| Strict field-versus-AW shared reductions / ties | 26 / 38 | 26 / 38 |
| Strict new-versus-AW enclosure reductions / ties | 28 / 36 | 28 / 36 |
| Strict receiver-radius reductions / ties | 29 / 8 | 29 / 8 |
| Nonnegative / nonpositive / mixed / zero rows | 64 / 33 / 0 / 33 | 64 / 33 / 0 / 33 |

The five maximizing targets are (1,9), (1,10), (2,10), (3,10), (4,10).
Row 18 has field gain 1/4, not the maximum 1: subtracting the two domain
maxima would therefore give the WRONG largest rowwise gap.
The identical maximum does not imply identical row gains or response maps;
row 1, for example, is 1/4 in grid and 1/8 in warp.

## From actual fields to error coordinates

The measure is dmu=du*dv/2. V is probe volume, h_t tile volume, h_C cell volume,
and sigma_(C,D)=V² h_C h_D. Both fixed probes have V=1/2; all their target
scales are positive. On each actual tile, use local coordinates xi,eta in
[0,1] and the corner basis in order 00,10,01,11. For epsilon>=0:

```text
phi = ((1-xi)(1-eta), xi(1-eta), (1-xi)eta, xi eta)
deltaF_t = V² sum_a c_ta phi_a,       |c_ta| <= epsilon.

x_t = integral_tile deltaF_t (1,xi,eta,xi eta) dmu / (V² h_t) = Q c_t
e_t = integral_tile deltaF_t (1,u,v,uv) dmu = P_t c_t = W_t x_t

Q = [[1/4,  1/4,  1/4, 1/4],
     [1/12, 1/6,  1/12,1/6],
     [1/12, 1/12, 1/6, 1/6],
     [1/36, 1/18, 1/18,1/9]]
U = inverse(Q)
P_t = W_t Q; Z_t = inverse(W_t)
```

The nonnegative partition of unity gives actual pointwise extrema
V² min(c_t), V² max(c_t). Q's nonnegative row sums are
(1,1/2,1/2,1/4), proving containment in AW's moment cube. Both two-sided
inverse identities for Q/U and W/Z are checked. W uses the actual tile origin,
widths and volume; a stale coarse-cell block is not interchangeable with it.
Raw bank errors e, normalized local moments x and corners c remain distinct.
Applying Z to e recovers Qc; applying U afterward recovers c.

Signed perturbations need not preserve nonnegativity of a total source.
Tile-boundary jumps are permitted (edges have zero area). The class is not
required to be continuous, empirically calibrated or physically prepared.
The standalone integration API additionally admits arbitrary signed corners,
partial tile coverage and no tiles; it is not confined to the witness cube.
Coefficients and moments are linear in corners, but extrema are not.

The unchanged complete bank identity and the new propagation are

```text
D B = G on the FULL bank, not just selected errors.
H = B P; J = G P = D H; A_i = J_i / sigma_i.
beta_l = sum_j |H_lj|; E_il = D_il beta_l / sigma_i.
alpha_i = sum_j |A_ij|; gamma_i = sum_l |E_il|.

shared field-class bound: |normalized target_i| <= epsilon alpha_i
enclosing receiver box:   |y_l| <= epsilon beta_l
receiver-box bound:       |normalized target_i| <= epsilon gamma_i
```

Each bound is sharp in its OWN stated domain, with actual attaining endpoints.
The larger receiver box discards the dependence y=B P c. It need not be
field-realizable, and a Cartesian box does not assert stochastic independence.
No receiver-box preimage or general feasibility solver is supplied.

AW's selected geometry, W/Z blocks and baseline maps/gains are explicitly
rechecked against its pinned capture. This selected recalculation is part of
AX; AW's witnesses and all older executors are not replayed. No source
dictionary, measurement or inferred normalization row is added; no old
source/target integral, repair overlay, decoder fit, filter choice or rank is
recomputed. The NEW error-field integrals above are explicitly computed.

## Complete positive-row comparison

All indices are zero-based original target rows. All 31 positive rows appear
below; the other 33 have zero shared AND enclosure gains in both fixed
families. Full baseline enclosure values and every comparison partition are
retained in the evidence.

| Row / target | Grid field | Warp field | Grid enclosure | Warp enclosure | AW grid shared | AW warp shared |
|---|---:|---:|---:|---:|---:|---:|
| 0 / (1,1) | 1/4 | 1/4 | 9/4 | 9/4 | 5/2 | 23/8 |
| 1 / (1,2) | 1/4 | 1/8 | 1/4 | 1/8 | 1 | 1/2 |
| 2 / (1,3) | 3/4 | 5/8 | 13/4 | 49/24 | 3/2 | 7/4 |
| 3 / (1,4) | 1/2 | 1/2 | 3/2 | 3/2 | 5/4 | 23/16 |
| 4 / (1,5) | 1/2 | 1/2 | 3/2 | 3/2 | 2 | 2 |
| 5 / (1,7) | 1/2 | 1/2 | 3/2 | 3/2 | 5/4 | 23/16 |
| 6 / (1,9) | 1 | 1 | 1 | 1 | 1 | 1 |
| 7 / (1,10) | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 / (2,2) | 1/4 | 1/4 | 1/4 | 1/4 | 4 | 4 |
| 10 / (2,3) | 1/2 | 1/2 | 1/2 | 1/2 | 2 | 2 |
| 11 / (2,4) | 3/4 | 7/8 | 3/4 | 7/8 | 3/2 | 5/4 |
| 13 / (2,7) | 3/4 | 7/8 | 3/4 | 7/8 | 3/2 | 5/4 |
| 14 / (2,9) | 3/4 | 19/24 | 3/4 | 19/24 | 3/2 | 17/12 |
| 15 / (2,10) | 1 | 1 | 2 | 12/7 | 1 | 1 |
| 18 / (3,3) | 1/4 | 1/4 | 135/4 | 1523/180 | 4 | 4 |
| 19 / (3,4) | 1/4 | 3/8 | 15/4 | 55/24 | 1 | 3/2 |
| 21 / (3,7) | 1/4 | 3/8 | 15/4 | 55/24 | 1 | 3/2 |
| 22 / (3,9) | 3/4 | 19/24 | 29/4 | 199/72 | 3/2 | 17/12 |
| 23 / (3,10) | 1 | 1 | 4 | 40/21 | 1 | 1 |
| 27 / (4,4) | 1/4 | 1/4 | 45/4 | 171/28 | 5/2 | 23/8 |
| 29 / (4,7) | 1/2 | 1/2 | 3/2 | 3/2 | 5/4 | 23/16 |
| 30 / (4,9) | 1/4 | 7/24 | 15/4 | 19/8 | 1 | 7/6 |
| 31 / (4,10) | 1 | 1 | 1 | 1 | 1 | 1 |
| 36 / (5,5) | 1/4 | 1/4 | 21/4 | 13/4 | 4 | 4 |
| 38 / (5,9) | 1/2 | 1/2 | 7/2 | 13/6 | 2 | 2 |
| 39 / (5,10) | 1/2 | 1/2 | 7/2 | 13/6 | 2 | 2 |
| 45 / (7,7) | 1/4 | 1/4 | 33/4 | 93/20 | 5/2 | 23/8 |
| 47 / (7,10) | 1/2 | 1/2 | 11/2 | 31/10 | 2 | 2 |
| 54 / (9,9) | 1/4 | 1/4 | 49/4 | 169/36 | 5/2 | 61/24 |
| 55 / (9,10) | 1/2 | 1/2 | 7/2 | 13/6 | 2 | 2 |
| 63 / (10,10) | 1/4 | 1/4 | 77/4 | 403/60 | 4 | 4 |

The 22 strict field-versus-enclosure rows are
0,2,3,4,5,15,18,19,21,22,23,27,29,30,36,38,39,45,47,54,55,63;
42 tie, including nine positive and 33 zero rows.
The 26 strict shared reductions relative to AW are
0,1,2,3,4,5,9,10,11,13,14,18,19,21,22,27,29,30,36,38,39,45,47,54,55,63.
Five positive shared ties are precisely the new maximizing rows.

The old AW maximizing rows 9,18,36,63 each decrease from 4 to 1/4, so they
are no longer the shared maximizers. Previously discussed row 63=(10,10)
has field gain 1/4 and enclosure 77/4 (grid), 403/60 (warp).
These are bounds in AX's new domain, not a revision of AW's evidence.

Reducing both bounds does NOT guarantee that their gap decreases. A retained
unit-tile synthetic control with B=I and D=G=[1,-1,-1,1] has old
alpha0=gamma0=8, new alpha=1/2 and gamma=9/2: the gap grows from 0 to 4.
All four comparison partitions are computed separately, including explicit
undefined rows and complete maximum ties.

## Field endpoints, constants and nulls

Each family retains 128 signed field endpoints, 128 signed receiver-box
endpoints, and TWO additional complete constant-field controls. Every field
endpoint actually reconstructs local/global polynomial coefficients and
integrates all raw/local moments; separately it executes

```text
c -> synthesize(Q,c) -> local moments x
c -> synthesize(P,c) -> bank error e
e -> synthesize(Z,e) -> recovered x -> synthesize(U,x) -> recovered c
e -> produce(B,e) -> observed y -> apply(D,y)
e -> produce(G,e) -> direct target response
```

Integrated and synthesized moments agree. All corner roundtrips, complete
off-target raw outputs, normalized outputs and actual tile extrema agree,
and all receiver/target bounds hold. Every designated signed bound is attained,
including zero-response rows. Negative endpoints reverse the signed field and
responses, with extrema transformed in the correct order.

In both fixed cases the positive constant control is deltaF=V²=1/4 across the
probe. Its normalized response vector equals the full vector of shared gains;
the negative constant gives its negative. The canonical row-specific positive
maximizers are +1 on corners of tiles 0,1 for rows 6,7; tile 2 for row 15;
tile 3 for row 23; tiles 4,5 for row 31, and zero elsewhere. Negative witnesses
reverse them. All individual maximizing target ties are retained; these sign
vectors do not enumerate full maximizing faces.

Zero rows belong to BOTH nonnegative and nonpositive coefficient classes.
Accordingly the negative constant attains the upper bound only on the 33
zero rows, while attaining the lower bound on every row. These lists describe
integrated A coefficients, not pointwise kernel signs.

A generic unit-tile signed-response control with B=I4 and D=G=[-1,2,0,0] has
A=(-1,1,-1,1)/6, shared gain 2/3, enclosure gain 4 and constant response 0.
The maximizing field is (2u-1)/4. Thus neither constant reaches the upper
bound for arbitrary G, and fixed-case positivity is not built into the API.

Generic null-cell targets have sigma=0 and zero G but can have a nonzero
cancelling D row. Their normalized maps, gains and designated witnesses are
NULL; full raw outputs remain present, including potentially nonzero
receiver-box outputs. Defined zero-response targets are different: the
duplicate-receiver cancellation control has shared gain 0 but enclosure 4.
All-undefined queries have null target maxima and empty maximizing lists,
yet retain receiver radii and BOTH actual constant-field controls.
An empty receiver list also has explicit empty-domain comparison semantics.

Synthetic positive affine changes transport the complete model with
F'=k²F, V'=kV, sigma'=k^4 sigma and k=ac>0. Q,U,c and local moments are
invariant, P'=S P, W'=S W and Z'=Z S^-1. The same explicit transported
B'=T B S^-1, G'=k^4 G S^-1 and D'=k^4 D T^-1 preserve normalized shared
bounds, constants and nulls. General receiver mixing changes an axis-aligned
reboxing; signed monomial mixing preserves its gains. These synthetic checks
do not claim that the two fixed families are related by one global affine
change or establish physical coordinate covariance.

## Application meaning and next boundary

The calculus now turns a stated pointwise bound on a specified bilinear
perturbation into exact response-error budgets, with actual integrating
witness fields. It can support geometry-supplied numerical validation and
response-tolerance analysis where this field class is justified. It keeps
field errors separate from independently acquired measurement errors.

The smaller bounds quantify the effect of enforcing this declared bilinear
field class. AW also admits moment combinations incompatible with a pointwise
cap, but AX does not characterize the full bounded-field moment body.
The bounds do not measure apparatus noise or establish practical robustness,
calibration, hidden
geometry reconstruction, full-field stability or physical source preparation.
RET integration, quantum channels, gravity, Lean and ontology remain separate.

The next useful question is whether the actual response functional has a
pointwise sign certificate, allowing stronger bounds over ALL bounded
measurable signed fields. Nonnegative integrated AX coefficients alone do
not answer that question; even k(xi,eta)=xi-1/4 changes sign while its four
integrated bilinear-corner coefficients are positive. This is an analytic
prospective caution, not a new fixed-family calculation.

**Proposed QR-05AY: kernel sign certificates and bounded-field envelopes.**
Evaluate the actual tilewise bilinear kernel
k_it(u,v)=sum_j G_i,tj (1,u,v,uv)_j at all four tile corners. If every tile
kernel is sign-definite, certify
(V²/sigma_i) sum_t |integral_tile k_it dmu| and authenticate signed
tile-constant extremizers through the unchanged response pipeline.
Different tiles can require different signs; a global constant need not work.

If a tile changes sign internally, retain its corner obstruction and a finite
rational upper envelope using h_t max_corner |k_it|, alongside admitted
lower witnesses. Leave the simple exact route explicitly uncertified, not
unbounded or zero. Do not silently integrate absolute mixed bilinear kernels,
claim sharpness of a loose envelope, add measurements or change physics.
No fixed AY kernel sign, envelope or witness calculation has run.

## Representation and verification

Across both families, input geometry contributes 168 rational occurrences and
input matrices 14,432. Retained geometry contributes 170; coordinate blocks
and scales 1,248; selected AW baselines 16,170; complete new maps 45,152;
gains 334; comparison values 466; constant-response diagnostics 128.

The 256 field endpoints retain 163,328 rational occurrences and 6,144
separately counted signs. The 256 receiver-box endpoints retain 42,496
occurrences and 4,736 signs. The four constant controls retain another 2,548
rational occurrences. Counts include zeros and repetitions but exclude nulls,
labels and target indices. Each 4x4 Q and U is retained once per family,
not once per tile, and no dense 48x48 coordinate matrix is stored.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Input problem | 47,365 | 47,433 |
| Geometry | 979 | 1,102 |
| Coordinate blocks and scales | 5,284 | 5,905 |
| Selected AW baseline | 49,665 | 50,226 |
| Complete coefficient maps | 138,898 | 140,386 |
| Field-class bounds and witnesses | 542,017 | 546,072 |
| Enclosure bounds and witnesses | 146,986 | 148,383 |
| Complete comparisons | 2,588 | 2,714 |
| Positivity and constant controls | 10,852 | 11,743 |
| Complete native family | 946,014 | 955,344 |

The suite is 1,904,029 bytes. These overlapping projections are not additive
unique storage, a minimal encoding or a measured-value transmission packet.

All **65 tests pass normally and optimized**: 281.04 s / 282.13 s in concurrent
runs. Before freeze, 55 generic tests passed in each mode (48.64 s / 48.96 s),
with all ten fixed tests deselected. Source collection keeps fixed input
projection, geometry and field computations lazy until explicitly released.

Primary derives separable corner integrals, triangular coordinate blocks and
blockwise products, then integrates expanded physical polynomials.
Reference independently evaluates exact tensor-Simpson integrals, reconstructs
physical coefficients by pivoted inversion, probes response columns and checks
interval bounds. The third oracle uses polynomial dictionaries, independent
antiderivatives, scalar contractions and small-cube vertex enumeration.
Complete native family wires agree, not merely designated maxima or ranks.
The fixed 48-dimensional cube is not enumerated: exact coefficient maps plus
actual attaining signs certify its linear extrema.

Each isolated normal/-O guard subprocess checks **514 explicit ValueError
rejections**: 231 malformed cases, 11 additional overflow/cycle cases and
15 pre-arithmetic admission checks PER engine. All **1,241 non-noop mutations**
pass: 799 generic-family, 418 fixed-family, eight suite and 16 selected-history
changes. Six deliberately unselected old endpoint/ancillary changes remain
admitted by selective bridge helpers; complete actual prior captures are
still byte-pinned. Nine synthetic selected-projection rejections also pass.

Controls cover signed/translated/unequal tiles, full positive affine transport,
matching tile/column permutations, null and defined-zero targets, raw undefined
outputs, no receivers, signed constant and nonconstant extrema, arbitrary
signed and partial/empty integration, both inverse roundtrips, actual endpoint
API call inventories, input/output detachment, shared children versus cycles,
cancelling large intermediate terms, retained overflow and admission ordering.
Separate bounded workloads exercise cap edges, including 256 tiles and
320 receivers. Combined worst-case admission limits are not a resource bound.

Authors' independent normal/-O hand suites and root's five literal synthetic
cases passed before freeze. Root's signed-response hand separately checks
the exact polynomial (2u-1)/4, its local moments and actual raw integrals;
translated and all-undefined controls distinguish reference amplitude, raw
outputs and constant-control preservation. Ruff check/format and scoped
whitespace checks pass. The optimized pytest warning concerns assertions
outside rewritten test modules; engine admission uses explicit exceptions
and is separately checked under -O. No exhaustive hostile-input or generic
production hardening claim is made.

## Freeze and evidence lifecycle

The five sources were frozen at **2026-09-09 00:50:21 UTC**, before any
assembled fixed AX projection, geometry check, selected baseline calculation,
field integral, corner map, gain or witness calculation. The identity bracket
covers **148 artifacts**: five current sources, 54 prior captures and
89 ancestor sources. AW's selected capture remains 1,341,549 bytes with its
published SHA256 e14e357309ff98f9f93c8f23c603f62d9bf17b01b4515ee122a464671b205916.

1. First external primary/reference comparison: 19.6359 s.
2. Exactly ONE independent normal reference-only read-only audit: 12.2698 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 19.3536 s.
5. Exclusive final comparison capture: 19.4299 s.
6. Fresh primary-normal / reference--O read-only replays: 8.4819 s / 12.1206 s.

The independent audit and full tests ran concurrently after the first
comparison. Both finished before preflight. First, preflight and final
non-runtime fields agree exactly, and every source identity and retained
capture byte remains unchanged. The runner uses isolated Python and external
fresh caches, no dependency installation and create-only final writes.

Before freeze, the protocol wording was clarified to distinguish linear
coefficients/moments from nonlinear field extrema. The third test harness
corrected a numeric-literal serialization mistake: its mixed scientific-wire
encoder intentionally preserves integer labels/counts, so numeric test
literals and tuple vertices needed a separate rational-array encoder.
The initial seven complete generic family comparisons had already passed;
no engine or oracle formula changed. Ordinary prefreeze Ruff cleanup
included explicit loop-variable binding in the runner's endpoint helper.
There were **NO post-first source, protocol, fixture or mathematical
corrections**. Subsequent explanatory report edits remained outside the
five-source ledger.

Verification timing is not an application benchmark. The 128 MiB capture
and 192 MiB serialized working caps do not bound process memory or work.
For example, the first comparison's recorded RSS high water was
289,226,752 bytes. No worst-case or production resource-hardening claim follows.

Final capture: **1,925,803 bytes**, SHA256
`80020730e21d2c5731b6f6d5a94add1faa6739c815ac3e82087126d45667f1b0`.
Suite: **1,904,029 bytes**, SHA256
`90553510269f3692a07292032a8dce8ae750a2bf7b9b3478687a480b312209d1`.

Only this gate's seven files and the bridge roadmap belong to its publication.
Previous captures and the unrelated RET/core/governance work remain untouched;
the local temporary model sheet is not included.
