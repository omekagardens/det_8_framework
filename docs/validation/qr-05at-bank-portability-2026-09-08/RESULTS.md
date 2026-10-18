# QR-05AT results: bank-level structural portability

8 September 2026. Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AS commit `e55e9c8869efa2e5a0d0fce029aafc3abf7f73f0`.

## Main result

The SAME frozen AS receiver is structurally exact on every raw bank vector
for all 64 warp responses and 63 of 64 grid responses. Grid's remaining
response, zero-based row63=(10,10), has a nonzero affine defect. Every original
normalized-source identity still holds exactly in both families.

This is a useful separation: the warp result extends the frozen response
map beyond its original source model; the grid result identifies one precise
normalization-dependent limitation. Neither changes AS's five-extra-readout
minimum on the declared simplex. The grid failure does not by itself show
that the existing measurements are insufficient.

| Per family | Grid | Warp |
|---|---:|---:|
| Unchanged source columns | 108 | 108 |
| Coarse / bank / supplemental values | 32 / 48 / 5 | 32 / 48 / 5 |
| Receiver input values | 37 | 37 |
| Structurally exact response rows | 63 | 64 |
| Source-exact but not unrestricted-bank-exact rows | 1 | 0 |
| Nonzero intercept entries | 1 | 0 |
| Nonzero bank-defect coefficients | 12 | 0 |
| Prespecified zero/unit-bank controls | 49 | 49 |
| Controls with a nonzero residual | 49 | 0 |
| Nonzero source-column residuals | 0 | 0 |

The row counts include inherited identically-zero responses. They are algebraic
classifications, not success probabilities. Forty-nine failed grid controls
do not mean forty-nine independent missing directions.

## What was verified

AR's authenticated rectangle lineage yields the coarse parent-sum map C.
Both families have eight coarse tiles and twelve bank tiles. Their ordered
bank-child lists are

```text
[[0,1], [2,3], [4,5], [6], [7,8], [9], [10], [11]].
```

Every global monomial moment is summed into its named parent with coefficient
one. These are raw integrals, not area-weighted averages. Positive bounds,
disjoint interiors, containment and exact parent coverage were rechecked.
Original fine-tile links, ownership, bounds containment and tile-major moment
labels were separately verified. No moments, sources or targets were integrated.

Write O for coarse source measurements, R for the bank source matrix, Q for
target source values, G for AR's full bank response map, F for the five frozen
AS filters, and a,L for the frozen receiver. Partition L=[Lc Lh]. The complete
retained identities are

```text
O = C R,              Q = G R,
H = F R = Q_selected,
a*1^T + L*[O;H] = Q,
K = Lc C + Lh F,      E = K-G,
a*1^T + E R = 0.
```

For any raw bank vector z, the pipeline's signed response error is

```text
d(z) = a + E z.
```

Thus unrestricted-bank correctness requires BOTH a=0 and E=0. The weaker
source-column equality cannot establish those coefficient conditions.
All matrices, including their zero entries and complete source restrictions,
are retained. No map was refitted or filter reselected.

Primary constructs the dense composed map. Reference recovers each K column
from actual frozen pipeline evaluations at a unit input minus the zero-input
evaluation. The third oracle uses direct parent/basis-indexed scalar sums.
The three routes agree on the complete family wires.

## The exact grid limitation

Only target (10,10) has a nonzero intercept, a63=1/864. Only that row of E is
nonzero. Its twelve nonzero coefficients are on the zeroth-moment coordinate
of every bank tile:

| Zero-based bank coordinate | E coefficient |
|---|---:|
| 0, 4, 28, 32, 36, 40 | -1 |
| 8, 12, 16, 20 | -2 |
| 24, 44 | -1/2 |

Every other coefficient and every other intercept is zero. Explicitly,

```text
d_(10,10)(z) =
  1/864
  - (z0 + z4 + z28 + z32 + z36 + z40)
  - 2*(z8 + z12 + z16 + z20)
  - (z24 + z44)/2.
```

This formula describes the retained discrepancy. Its unequal mass weights
must not be relabeled ordinary total-field normalization or imposed as a new
off-model admissibility condition. No such constraint was fitted or assumed.

At zero bank input, the full geometric map gives zero but the frozen grid
receiver gives 1/864 at (10,10). This is the first prescribed failure.
At each unit input ej, the residual is a+E[:,j], not E[:,j]:

| Unit coordinate class | Residual at (10,10) |
|---|---:|
| Coefficient -1 | -863/864 |
| Coefficient -2 | -1727/864 |
| Coefficient -1/2 | -431/864 |
| All 36 other coordinates | 1/864 |

All other response rows have zero residual for every control.
The grid receiver remains exact on the declared normalized source simplex,
as certified independently by both source-residual constructions.

## Application meaning and limits

Warp's a=0,E=0 is a full coefficient identity. Conditional on AR's supplied
geometry and integral meaning of G, and correctly obtained common-bank
coarse/supplemental values, it gives the same response functionals beyond
the finite normalized source family. The same applies to grid's 63 structural
rows. This is response evaluation, not reconstruction of the incoming field.

The identified grid limitation concerns this particular canonical affine
receiver. A different receiver using the SAME 37 values might remove it;
AT neither constructs such a receiver nor proves it impossible.

Every retained bank control used the actual file-blind producer and receiver
APIs. The bank vector, coarse values, five supplements, concatenated input,
truth, prediction, residual and independently evaluated affine defect are all
retained. Unknown measured values are still required: supplied geometry only
provides coefficients.

Zero/unit controls diagnose algebra. They do not establish prepared physical
sources, a violation of known observables, sensor precision, noise robustness,
or gravitational dynamics. No empirical noise model, quantum channel, RET
adapter or Lean proof was introduced. If a later study derives coarse and
supplemental values from one noisy bank, their errors share that primitive
input; independent output-error boxes describe a different model.

## Representation and validation

Across both families, the capture retains 42,752 input rational occurrences,
3,072 coarse-map entries, 6,144 effective-map entries, 6,144 defect entries,
84,024 source-check matrix entries and 37,044 rational occurrences in the
98 complete bank controls. Counts include zeros and repetitions.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Inherited problem and selected lineage | 135,824 | 138,674 |
| Lineage certificate | 52,511 | 53,451 |
| Full composition certificate | 252,778 | 254,440 |
| Row classification | 365 | 330 |
| All bank controls | 118,738 | 118,393 |
| Frozen receiver map alone | 14,809 | 14,822 |
| Complete native family | 560,963 | 566,034 |

The suite is 1,128,907 bytes. These overlapping verification scopes are not
additive unique storage or measured-value transmission packets.

All 57 tests pass normally and optimized: 53.36 s / 53.06 s in recorded
concurrent runs. Before freeze, all 47 generic tests passed in both modes
(3.20 s / 3.19 s); all ten fixed tests were deselected.

Synthetic controls cover exact portability, linear defects hidden by source
dependencies, intercept cancellation on normalized sources, all-unit-pass but
zero-fail examples, mixed row classifications, unequal child areas, empty
supplements, arbitrary raw widths, nonzero offsets at width zero, shared inputs
and detached outputs. Same-map signed basis changes, positive dilation,
transported probes and tile permutations are checked without recanonicalization.
Restricted producer/receiver call inventories are verified, including repeats.

Each isolated subprocess mode performs 326 explicit rejection checks across
both engines. These cover malformed schemas, partitions, values, source
identities, overflow/cycles and admission-before-arithmetic. Seven additional
generic original-tile bounds rejections check the selected lineage helper.
Unretained intermediate cancellation is distinguished from retained overflow.

All 260 non-noop corruption checks pass: 155 generic family, 77 fixed family,
eight suite and twenty selected historical-producer mutations. The fixed
original-tile mutation redirects a repair tile to the wrong same-owner,
same-coarse-parent sibling and is rejected by bounds containment. Three
deliberately unselected historical changes remain admitted by selective bridge
helpers; the real complete prior captures remain pinned. No old ranks, decoder
fits, witnesses or collisions
were replayed.

The expected optimized pytest warning concerns assertions outside test modules;
engine guards use explicit exceptions and separate normal/-O subprocess tests.
These checks are not exhaustive hostile-input, memory or production guarantees.

## Freeze and evidence lifecycle

Five AT sources were frozen at 2026-09-08 22:30:03 UTC before any fixed AT
projection, partition check, C/K/defect calculation or bank-control evaluation.
All 124 identities were bracketed: five AT sources, fifty prior captures and
sixty-nine ancestor sources.

1. First external primary/reference comparison: 5.1529 s.
2. Exactly ONE independent normal reference-only read-only audit: 3.2374 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 5.1599 s.
5. Exclusive final comparison capture: 5.1633 s.
6. Fresh primary-normal / reference--O read-only replays: 2.9722 s / 3.2129 s.

The audit and full tests ran concurrently after the first comparison; both
finished before preflight. All non-runtime first/preflight/final fields agree,
with every identity and capture byte unchanged.

Prefreeze review strengthened original-fine-link bounds containment and canonical
owner/parent comparisons, and clarified that limited provenance check in the
protocol. A test mutation gained a fallback so it did not presume a particular
same-owner sibling existed. An author's separate synthetic harness corrected
generated integer empty-sum values to rational pairs; no engine mathematics
changed. There were NO post-first source, protocol, fixture or mathematical
changes.

Final capture: 1,147,189 bytes, SHA256
`3fe96ced94f7b4d45feec43d0415a908d656825e21f04a6796329825de4d651a`.
Suite: 1,128,907 bytes, SHA256
`f3a7cf3fda178227b5666cb9b7118e5e5a327da3125dac8d78d39ca24135940e`.

## Next proposed gate

QR-05AU should ask whether the unchanged interface x=[Cz;Fz] admits a
zero-intercept decoder for Gz on unrestricted raw bank vectors.

Test exact row-space membership against [C;F], WITHOUT a normalization row.
If possible, construct and certify an explicitly NEW receiver; do not rewrite
AT's frozen-map result. If impossible, retain exact raw-bank null-direction
countercontrols and state their algebraic domain. Do not infer physical-source
insufficiency from an unrestricted-vector counterexample.

Keep geometry, source dictionary, target functions, five filters and 37-value
interface unchanged. No extra acquisition, new normalization law, noise tuning
or minimality claim. Settle this receiver question before a shared-bank error
study. No AU rank, decoder, null-witness or other calculation has run.
