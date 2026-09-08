# QR-05AU results: source-independent receiver construction

8 September 2026. Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AT commit `c99368b7ffc9ef84b3f1b700ca1e48570cdc76dd`.

## Main result

Both grid and warp admit an explicitly NEW zero-intercept receiver that
recovers every one of the 64 target responses from the SAME 37 measured values,
for every raw bank vector. The construction uses only the interface and target
coefficient maps, not the original source columns or a normalization equation.

This resolves AT's open receiver question positively. The earlier grid
limitation belonged to its frozen affine decoder, not to a missing measurement
for these targets. AT's unchanged evidence still records that decoder's failure.

| Per family | Grid | Warp |
|---|---:|---:|
| Coarse / supplemental / total input values | 32 / 5 / 37 | 32 / 5 / 37 |
| Raw bank coordinates / original source columns | 48 / 108 | 48 / 108 |
| Interface / target / joint rank | 37 / 24 / 37 | 37 / 24 / 37 |
| Recovered / failed target rows | 64 / 0 | 64 / 0 |
| Identically-zero target rows included above | 33 | 33 |
| Nonzero coefficients in new decoder | 80 | 80 |
| Prescribed zero/unit-bank controls | 49 | 49 |
| Nonzero bank or source residual entries | 0 | 0 |
| Separating bank collisions | 0 | 0 |

The 64 rows are not 64 independent measurements or a success probability.
The rank-37 interface still has an 11-dimensional kernel on the 48-coordinate
raw bank domain. All requested targets ignore those invisible directions.
Recovering those responses is not identifying the full bank or incoming field.

## Source-independent coefficient identity

Retain AT's authenticated coarse map C, the SAME five AS filters F, and the
full geometric target map G. Define

```text
B = [C; F]                 (37 by 48),
x = B z,
D B = G                   (D is 64 by 37),
D x = G z.
```

No constant coordinate or hidden offset is present. No source normalization,
source dictionary, positivity assumption, or fitted off-model constraint enters
the certificate. The exact coefficient identity extends by linearity to real
as well as rational raw bank vectors; executable inputs remain bounded reduced
rational pairs as specified in the protocol.

For each target row, the certificate retains its exact expansion in the greedy
first independent ORIGINAL rows of B. All 37 input rows are independent here,
so row_basis is exactly 0 through 36 in both families. The target rank is 24;
adding every target row leaves interface rank 37 unchanged. Full coefficients,
pivot/free columns, membership classifications and dense decoders are retained.

Primary uses Gauss–Jordan elimination with an original-row transform.
Reference independently uses forward echelon construction and back substitution.
The third test oracle uses exact rational Gram–Schmidt row and column projections,
without square roots or either elimination implementation. Complete native
family records agree, not merely ranks or aggregate residual counts.

The public certificate accepts ONLY B and G. Source matrices R, O and Q are
used afterward to verify the unchanged restrictions

```text
C R = O,              G R = Q,
B R = [O; Q_selected],
D (B R) = Q.
```

Those equalities are consistency checks, not fitting equations. Synthetic
source replacements, including changed column counts, leave the certificate
and decoder identical when C, F and G are held fixed.

### The previously problematic grid target

For zero-based target row63=(10,10), the new decoder in BOTH families is

```text
response_(10,10) = (x28 - x29 - x30 + x31) / 2.
```

These are four existing coarse input coordinates; no supplement or constant
term appears in this row. In particular the new prediction is zero at zero
bank input. This formula is read directly from the new certified map, not
obtained by modifying or replaying AT's old affine decoder.

## Controls, failure semantics and application value

Every zero vector and bank unit vector passes through actual restricted
producer and receiver calls. The capture retains the bank input, coarse and
supplemental values, concatenated input, truth, prediction and residual.
Every control is exact for every target in both fixed families.

These are algebraic coordinate probes. For example unit bank coordinates45
or46 give true and predicted row63 equal to -1/2, while coordinates44 or47
give +1/2. A raw moment coordinate chosen in isolation need not be the moment
bank of a realizable nonnegative field. These values are not negative
probabilities, prepared physical sources, or conflicts with known observables.

The generic interface also correctly handles partial and empty recovery.
Failed rows have null coefficients, are absent from the indexed decoder, and
cannot be silently represented by zero forecasts. For failure, a deterministic
free-column-first null direction w retains the raw pair 0 and w, with Bw=0
but Gw nonzero. Such a collision excludes any decoder on the declared
unrestricted bank domain, not automatically on an admissible physical subset.

A specific synthetic normalization trap has B=[1,-1], G=[1,1] and w=[1,1].
The raw inputs 0 and w have the same observation and different targets.
Their unequal total mass must not be normalized away: adding a ones row is
a different interface. The failed fixture remains failed.

The practical mathematical value is a reusable response map independent of
the original finite normalized source model. Conditional on the supplied
geometric integral maps and correctly obtained common-bank measurements,
the same 37 values evaluate the requested response functionals without
identifying the source or reconstructing its field. Geometry supplies
coefficients, not the unknown measured values.

This gate does not implement an RET adapter, calibrate sensor errors, construct
a quantum channel, infer unknown geometry, establish gravitational dynamics,
or provide a Lean proof. The five-readout AS result on its declared source
simplex remains intact; no expanded minimality analysis was performed.

## Representation and validation

Across both families, the capture retains 40,800 input rational occurrences,
3,552 interface entries, 42,552 source-check entries, 4,736 compact and 4,736
dense decoder entries, 6,144 bank predictions and 6,144 bank residuals,
13,824 source predictions and 13,824 source residuals, and 30,772 entries in
the 98 complete bank controls. Counts include zeros and repetitions.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Input problem | 129,434 | 132,263 |
| Interface B | 10,744 | 10,751 |
| Source restrictions | 131,656 | 133,663 |
| Membership certificate | 15,005 | 15,027 |
| Decoder and its full predictions/residuals | 136,894 | 137,858 |
| All bank controls | 98,623 | 98,695 |
| Indexed receiver map alone | 14,600 | 14,622 |
| Complete native family | 523,200 | 529,101 |

The canonical suite is 1,054,313 bytes. These overlapping verification
projections are not additive unique storage or measured-value packets.

All 61 tests pass normally and optimized: 59.77 s / 59.83 s in the recorded
concurrent runs. Before freeze, 51 generic tests passed in both modes
(3.31 s / 3.23 s), with all ten fixed tests deselected.

Each isolated normal/-O guard subprocess performs 386 explicit ValueError
rejections across the two engines, including 173 malformed fixtures plus eight
overflow/cycle and twelve early-admission checks per engine. Seven additional
synthetic historical-projection rejections cover the selected input boundary.

All 390 non-noop mutation checks pass: 259 generic family, 114 fixed family,
eight suite and nine selected historical-producer changes. Six deliberately
unselected historical changes remain admitted by selective bridge helpers;
the complete actual prior captures remain byte-pinned. No old affine decoder,
defect, classification, bank control, geometry partition or other historical
mathematics was replayed.

Synthetic coverage includes zero/duplicate/dependent rows, empty interfaces,
partial recovery, free-column-first versus target-first witnesses, invisible
earlier free columns, tiny exact pivots, retained overflow versus canceled
intermediates, cycles versus shared children, detached outputs, arbitrary raw
widths, actual two-argument certificate calls and actual producer/application
calls. Coordinate-change controls distinguish a transported map or witness
from a newly canonicalized one; their coefficients need not be identical.

The expected optimized pytest warning concerns assertions outside test modules.
Engine guards are explicit exceptions and have separate normal/-O subprocess
checks. This is not exhaustive hostile-input, memory, computation or production
API hardening. Recorded timing is verification timing, not an application
benchmark; the capture and serialized-working caps do not bound process memory.

## Freeze and evidence lifecycle

Five AU sources were frozen at 2026-09-08 22:55:50 UTC before any fixed AU
input projection, rank, decoder, null-witness or bank-control calculation.
All 130 distinct identities were bracketed: five AU sources, 51 prior captures
and 74 ancestor sources.

1. First external primary/reference comparison: 5.2255 s.
2. Exactly ONE independent normal reference-only read-only audit: 3.3243 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 5.2668 s.
5. Exclusive final comparison capture: 5.2488 s.
6. Fresh primary-normal / reference--O read-only replays: 2.7332 s / 3.2619 s.

The audit and full tests ran concurrently after the first comparison; both
completed before preflight. All non-runtime first/preflight/final fields agree,
with every source identity and capture byte unchanged.

Before freeze, an unnecessary dead conditional in a test assertion was removed.
Initial generic test runs were deliberately interrupted at the admitted-cap
fixture, then that fixture was split into maximum interface/target dimensions
at one source column and maximum source columns with a small map. Boundary
coverage was retained without multiplying all maxima in one case. No engine
mathematics or protocol changed. There were NO post-first source, protocol,
fixture or mathematical corrections.

Final capture: 1,073,452 bytes, SHA256
`25e2fabfcf9e18df3ee3bf41fcac15a8b18cf3be1c4e14858be87316b48257ad`.
Suite: 1,054,313 bytes, SHA256
`b8d010ca28f2926521936e2294b6c9d25d9bab1977eeba41b4bf4ae5d799b5cc`.

## Next proposed gate

QR-05AV should investigate errors in a SHARED primitive bank, with AU's new
B, G and D held fixed. If the observed input is B(z+e), its target error is
D B e=G e. This is different from independently perturbing each of the
37 receiver coordinates.

First preregister the primitive error coordinates, numerical reference units
and target scales, without tuning them after seeing gains. For a prescribed
bank-error box, retain every sharp target-row bound and signed maximizing
witness, the actual common induced receiver error, direct and decoded target
errors, and all zero/tie cases. Compare with the conservative receiver-coordinate
box obtained by bounding each component of B e independently.

A gap measures lost dependence or cancellation in that enclosure, not improved
sensor precision. Enclosure-only witnesses need not correspond to a common
bank perturbation. Raw unit boxes are coordinate-dependent numerical models,
not empirical or dimensionally universal apparatus noise. No new fit, filter,
source normalization or physical calibration is implied. No fixed AV error,
gain or witness calculation has run.
