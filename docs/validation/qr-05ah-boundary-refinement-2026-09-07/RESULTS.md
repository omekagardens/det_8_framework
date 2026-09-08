# QR-05AH: partition refinement and boundary-error certificates

7 September 2026. Bounded supplied-geometry diagnostic after pushed AG commit
`f603b02ffba1d6965695eb13e572ad554f7d1827`.
The [prospective protocol](README.md) fixes the contract, nested partitions,
sampling laws and countercontrol before fixed AH computations.
The gate is complete; verification and claim boundaries are recorded below.

## Main result

Both independent new certificate engines and a literal oracle agree on the
five prescribed partition families and the separate counterexample. Every
geometric enclosure contains both the representative-weighted geometric sum
and the true supplied rectangle volume. Refinement never widens the enclosure.

Ten of fifty consecutive-level boundary-gap comparisons tighten strictly;
forty stay unchanged. All fifty absolute quadrature-error changes are zero
in the main family. The prespecified counterexample demonstrates a stronger
warning: the enclosure gap halves while the absolute quadrature error grows
from 1/10 to 3/20. A tighter valid certificate is not the same as a more
accurate point estimate.

This is useful finite error accounting with supplied geometry, not geometry
recovered from a retained causal record. For these rectangles the true volume
is already directly computable from the supplied bounds. The certificate
verifies the partition/refinement/error contract; it does not extract new
geometric information beyond that input.

## Two interfaces with different information

The new source-aware `certify(problem)` receives the domain, all cell bounds,
strict-interior representatives, positive supplied marks, probe rectangles
and parent lineage. One implementation proves rectangular coverage using
interior-disjointness and area totals; the independently written reference
uses endpoint-arrangement tiles. Both require local parent containment,
complete child partitions and exact supplied-mark additivity. A global volume
check alone cannot authenticate a partition or its lineage.

The observation interface is AG's unchanged `analyze(problem)`, run through
its two pinned implementations. It receives retained induced order, fixed
marker IDs, the full eligible-ID selection law and retained-cell marks only.
It receives no coordinates, cell boundaries, missing marks, parent labels or
source certificate. Reusing these AG engines is not counted as independently
implementing the new certificate. The source-aware audit relates the outputs
without leaking geometry into the observer.

## Exact enclosure and refinement accounting

In the supplied flat null coordinates, rectangle volume is Δu Δv/2. For a
probe Q, let g_i be cell area, w_i its supplied mark, and define:

- L: sum of g_i for cells wholly contained in Q.
- U: sum of g_i for cells with positive-area intersection with Q.
- G: sum of g_i for cells whose representative lies strictly inside Q.
- T: the same representative sum using w_i instead.
- V: the supplied geometric volume of Q.

Boundary-only contact contributes nothing to outer membership. The contract is

    L ≤ G ≤ U,     L ≤ V ≤ U,
    G − U ≤ G − V ≤ G − L,     |G − V| ≤ U − L.

There is no assumed ordering between G and V. Strict interiority makes every
inner cell a representative member and every representative member an outer
cell. Partition coverage bounds V between inner and outer volumes. Under a
true child partition, inner parents contribute entirely to fine inner volume,
and fine outer children lie in coarse outer parents. Additivity therefore
gives L_fine ≥ L_coarse and U_fine ≤ U_coarse. These elementary implications
depend on the declared geometry/partition premises; the bounded executable
checks are not a machine-checked proof for unrestricted partitions.

Supplied marks may be stale, so T need not lie in [L,U]. The observation audit
keeps the exact signed identity

    mean − V = (mean − T) + (T − G) + (G − V)
             = sampling bias + annotation error + quadrature error.

The geometric certificate is not an error bar for an individual random record.

## Prescribed three-level family

Start with AG's six-cell 3-by-2 partition. Split c_1_0 vertically at base
u=1/2, then split its left child horizontally at base v=1/4. Cell counts are
six, seven and eight. New base representatives are child midpoints; retired
parent points are not kept. Unchanged cells preserve their points and names.

The five families are grid, coordinatewise-square warp, that same warp with
stale base-area marks, boost (2u,v/2), and dilation (2u,2v). Bounds, probes
and declared representatives are all transformed; warped representatives are
not recentered. Both true areas and supplied marks add across parent/child
links, even in the stale family.

The whole, lower-aligned and upper-aligned probes have L=U=G=V at every level
in every family. The unaligned bounds are:

| Family / probe | Level 0 [L,U] | Level 1 [L,U] | Level 2 [L,U] |
| --- | --- | --- | --- |
| Grid lower | [0, 1/6] | [0, 1/6] | [1/48, 1/6] |
| Grid upper | [1/12, 1/3] | [1/12, 7/24] | [1/12, 7/24] |
| Warp lower | [0, 1/18] | [0, 1/18] | [5/1152, 1/18] |
| Warp upper | [5/24, 4/9] | [5/24, 41/96] | [5/24, 41/96] |

The following point estimates and errors stay unchanged at all three levels:

| Family / probe | G | V | G − V |
| --- | ---: | ---: | ---: |
| Grid lower | 1/6 | 3/25 | 7/150 |
| Grid upper | 1/12 | 3/25 | -11/300 |
| Warp lower | 1/18 | 18/625 | 301/11250 |
| Warp upper | 5/24 | 168/625 | -907/15000 |

These related finite controls are not fifty independent experiments. They
demonstrate enclosure improvement without point-estimate improvement, not a
convergence rate or a continuum limit.

## Explicit non-monotone point-error counterexample

The separate generic example uses the unit-square domain and query
[0,1/5] × [0,1], with V=1/10. Initially one cell has representative (3/4,1/2)
and true mark 1/2. Split it into left/right half-width children with true
marks 1/4 and representatives (1/10,1/2), (3/4,1/2).

| Level | [L,U] | G | G − V | Absolute error |
| --- | --- | ---: | ---: | ---: |
| Coarse | [0, 1/2] | 0 | -1/10 | 1/10 |
| Fine | [0, 1/4] | 1/4 | 3/20 | 3/20 |

The gap decreases by 1/4 but absolute error increases by 1/20, while the signed
quadrature error changes from negative to positive. No stale mark or
observation noise is involved. This is a constructive
counterexample under the generic representative contract, not a member of the
main midpoint-generated family or a claim about every midpoint refinement.
Its full input, output and both strict comparison booleans are retained.

## Stale annotations and transformations

At every level, stale-warp geometric certificate fields equal the correct
warp's fields, while complete identity-observation sample packets and analyses
equal the grid's. In probe order (whole, lower aligned, upper aligned, lower
unaligned, upper unaligned), stale annotation errors remain
[0, +1/9, -1/8, +1/9, -1/8].

For the unaligned lower probe the stale target 1/6 exceeds geometric U=1/18;
for the upper probe the stale target 1/12 is below geometric L=5/24. Refinement
does not turn a correct geometric certificate into a certificate for wrong
marks. Stale unaligned total errors remain +517/3750 and -1391/7500.

All complete boost certificate, observer and moment checks agree with grid.
Dilation multiplies volume/error quantities and parent totals by four, and
covariances by sixteen. These checks cover all three levels, not a selected
probe. They do not establish a Lorentz-invariant random ensemble.

## Refined sampling and covariance

At each level, grid and warp use identity, independent-half and singleton
selection; the other families use identity only. Each level has a fresh
eligible-ID frame derived from its base points, preserved under transformations
at that level. IDs are not asserted to persist across levels. These are
separate level-specific designs, not a coupled observation/coarsening process.

Every inclusion-corrected mean equals T. Full centered covariance, second
moments and the ordered-cell joint-inclusion formula agree. Singleton's zero
distinct-pair inclusion affects covariance without invalidating the linear
mean identity. Source-aware variance is not inferred from one retained packet.

| Family / design | Whole variance, level 0 | Level 1 | Level 2 |
| --- | ---: | ---: | ---: |
| Grid / independent half | 1/24 | 11/288 | 43/1152 |
| Grid / singleton | 0 | 5/288 | 7/144 |
| Warp / independent half | 175/2592 | 2765/41472 | 44165/663552 |
| Warp / singleton | 67/432 | 8987/41472 | 23429/82944 |

Identity variances are zero. The disjoint aligned-probe covariance is zero
under independent-half selection; singleton values stay -1/72 for grid and
-5/432 for warp. Negative covariance entries are retained.

Refinement lowers the listed independent-half whole variances, but raises
the singleton variances. Selecting one cell from the newly unequal weights
and changed frame is not the same experiment as selecting from the old grid.
No cross-level conditional transport or monotone sampling-error theorem follows.

## Verification and provenance

Before fixed execution, both independent engines passed generic normal/-O
hands. Root additionally compared twelve generic synthetic problems through
both engines in each mode, with exact literal outputs: twenty-four route
comparisons per mode. These were separate from the fixed main family. The
first 265 generic/admission/lifecycle tests passed before fixed calculations.

Prospective read-only review clarified that generic one-child refinements may
rename or move a representative (the main unchanged cells do neither), added
authentication of all seven AG source files to every prior-identity check,
and strengthened the three separate enclosure error-identity controls.
These changes and source formatting preceded the first fixed execution.

The first complete fixed comparison passed in 35.986008625004615s. Four frozen
protocol/implementation sources, 38 prior captures and seven AG sources stayed
unchanged. Mathematical suite identity: 14,290,247 bytes, SHA256
`d7f1e490bf3b4974dd98deccd3a666bea71692fef6fece0edf8c3f4f41536aa8`.
No mathematical, implementation or fixture correction followed that run.

The suite has 27 cases and 4,032 mask rows: 953 positive and 3,079 structural
zeros. It retains 135 case-specific probe questions, 405 source-member terms,
32,832 observed-member terms and 6,237 ordered probe-cell pairs, including
1,152 zero-joint pairs. There are twelve ordinary new-certificate calls,
8,064 ordinary reused-observer calls and sixteen malformed-certificate
rejections. These are finite enumeration counts, not physical experiments.

All nine complete AG level-zero case objects match after dropping only AH's
level field and restoring the original case ID. This consumes grid/warp with
identity, half and singleton, plus stale/boost/dilate identity. Other AG and
historical mathematics is authenticated by identity, not replayed.

The first independent raw reconstruction passed immediately in 9.755736333s
with 13,412,222 checks. It imports no engines, runner or tests. It separately
reconstructs endpoint-tile partition/parent proofs, clipped cell integrals,
strict-u/v source orders, all sampling packets and three errors, covariance
and the nine complete AG bridges.

All seven AH sources were held before exclusive external preflight. That
capture passed in 44.98228599999857s; the raw audit passed in
13.150611334000132s with 27,567,114 checks. Its mathematical suite matched the
first comparison exactly. The audit authenticates seven AH sources, 38 prior
captures and seven AG sources: 52 identity targets plus the current capture.

Full agent-run tests passed 305 tests in normal and optimized Python (136.24s
each): 270 main and 35 capture-lifecycle tests. Coverage includes all eleven
live caps, 206 malformed fixtures, 546 explicit ValueError rejections and
sixty pre-serialization controls per guard mode. Forty-four nonvacuous
corruptions cover 24 certificate, twelve observation-case and eight suite
mutations. All five certificate families, 27 complete sampling cases and
the nine prior bridges are independently reconstructed. The expected pytest
optimization warning is not suppressed; explicit rejection guards still run.

After the external preflight/audit, root reran the frozen full tests: all 305
passed in normal Python (136.57s) and optimized Python (136.50s), with only
the expected optimization warning. Scientific review and an independent
read-only comparison of every report table to the preflight evidence passed.
Review clarified the counterexample's wording: the signed error changes
sign, not the absolute error. No frozen source or evidence was changed.

The final capture was exclusively created in 43.83287937499699s. Its entire
mathematical suite equals the first comparison and preflight. Every envelope
field except runtime metadata equals the preflight exactly. Final identity:

- Path: `results.json`.
- Bytes: 14,297,174.
- SHA256: `49b911c74a2e1428cb3b378ec2bf33c77feb80ab8cab213a26cd005531429bb8`.
- Environment: isolated Python 3.11.6, macOS arm64, optimization off,
  fresh external bytecode cache.
- Suite-end RSS high-water: 624,443,392 bytes. Runtime/RSS exclude final
  report serialization and are not application-performance benchmarks.

Fresh isolated read-only replays passed normally in 46.04808820800099s and
optimized in 45.09095695900032s. The final raw audit passed in
13.674065999999584s with 27,567,114 checks. These checks include 77 geometric
enclosure questions, 1,044 partition tile-cell checks, 135 certificate/observer
probe bridges, nine complete AG case bridges, 1,215 upper-triangle centered
covariance entries, 42,885 centered product terms, 1,341 full cell-covariance
entries, 6,237 ordered probe-cell pairs, 1,152 zero-joint pairs and 405 signed
three-error decompositions. Replays and audit used separate fresh processes
and ran concurrently; timings are verification observations, not performance
comparisons.

All 52 source/prior identity targets and final capture bytes stayed unchanged.
Historical API-call counts are metadata, not newly executed historical calls.
Ruff checks and formatting checks pass for all six gate Python files. The
standard scoped whitespace check passes without a frozen-source exception.
Publication is limited to this gate and its research roadmap; unrelated
RET/core/governance work and temporary model notes are excluded.

## Next question: weighted causal-kernel refinement

Proposed QR-05AI reconnects AF's scalar causal-propagation comparison to AG/AH
local-volume marks. On the same bounded partitions and probes, compare finite
weighted one-cell and comparable-distinct-cell chain targets with supplied
continuum coefficient targets, preserving complete chain/support evidence.
Identity and half-retention can serve as supported controls; singleton must
retain its distinct-pair support failure rather than borrowing the linear
volume success.

Keep boundary and annotation errors separate from missing pair support,
unresolved within-cell pairs and partially causal cross-cell products.
A representative-order Boolean need not describe all pairs of continuum
points in those cells. Pair-target covariance may require up-to-four-cell
joint inclusion, not only individual or pair marginals. AH's one-cell volume
enclosure does not automatically certify a two-cell causal kernel.

Preserve AG/AH's zero-volume bookkeeping markers; AF's earlier internal-chain
count can include fixed internal probe events, so replacing density factors
by cell marks is not automatically an exact numerical AF bridge. Prespecify
all normalizations, weighted-event/chain conventions, representative rules,
laws and output before computing AI. This is a formula-free proposal, not
a completed test. No additional forecasting prerequisite is introduced.

This remains a supplied flat-geometry scalar comparison. It neither constructs
a quantum CP map nor establishes metric reconstruction, a continuum limit or
gravitational dynamics. RET integration, Lean and apparatus calibration remain
separate. No AI computations have been performed.
