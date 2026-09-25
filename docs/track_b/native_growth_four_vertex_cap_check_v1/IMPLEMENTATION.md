# RI-88 — exact four-vertex-cap checker implementation

25 September 2026 UTC. **Source preparation only; no coefficient result.**
The coordinator accepted and published the unchanged
[RI-85 design](../native_growth_four_vertex_cap_v1/DESIGN.md), 28,127 bytes,
SHA-256 `e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a`.
This reservation implements exactly that finite decision. Source review and
AST compilation are not execution evidence; actual rank and feasibility are
not inferred from code or synthetic fixtures.

Only `check.py` and this note are reserved repository files. The new
`CERTIFICATE.json` remains absent until coordinator-owned admitted execution
and adjudication. Accepted sources, historical evidence and concurrent work
are not modified. The coordinator owns git/index/publication and every
execution admission; RET remains paused.

## 1. Decision and permissible conclusions

The baseline keeps the actual accepted strictly positive marked rows through
parent size five, including actual RI-63 mixed q5, and uses the common
RI-38 half-scale continuation at size six. The unmarked relative weight h
is one through six and outside the complete seven-event support

\[
 \{C_3\oplus Q: |Q|=4,\ |\operatorname{Max}(Q)|\geq2\}.
\]

There are eleven supported classes in the accepted lexicographic order.
The previous RI-84 three-class rejection remains unchanged. This is its
explicitly assigned intrinsic enlargement, not a new physical law or a
supplied geometry. No h at size eight or above is supplied.

Every full record row must be harmonic. All supported births are proper,
so the same positive global a6 cancels and the exact equations use only held
size-at-most-five probabilities. No numerical q6, q7, a6 or M6 is calculated.
The target is complete-row expected child width at P=C3 ordinal-sum A3 with
all six records zero, summing all ideals and both fair newborn marks.

The three mathematical dispositions must remain distinct:

- A canonical harmonic vector with z1=1, a strictly positive amplitude and
  strictly positive complete-row width gain: a finite-prefix construction.
- A nontrivial harmonic kernel but a signed row-span certificate forcing
  z1=0: the named width target is obstructed, not all supported perturbations.
- Rank eleven and zero kernel: no nonzero perturbation on this frozen support.

All are valid finite outcomes. A failed guard, resource stop, malformed
certificate, dependency mismatch or code defect is none of them. No outcome
authorizes a larger support, changed target, later departure, continuation
solver, new QR-05 lettered gate or wider QM/geometry/gravity conclusion.

## 2. Complete finite domain

The checker retains every labeled ideal before quotienting child classes.
Backward maximal-deletion roles are independently reconstructed and never
used as forward multiplicity weights. Unsupported correction slots remain
present; their baseline probabilities are positive but not newly evaluated.

| Required domain | Count |
|---|---:|
| Supported seven-event classes | 11 |
| Maximal-deletion roles | 27 |
| Affected six-parent classes | 5 |
| Individual ideals over the five representatives | 43 |
| Supported / unsupported individual slots | 23 / 20 |
| Complete marked parent rows | 320 |
| Expanded ideal occurrences | 2752 |
| Supported / zero-correction occurrences | 1472 / 1280 |
| Full births / strict-stem-prefix births | 320 / 960 |
| Raw deletion factors before cancellations | 2752 |
| Compact harmonic matrix | 64 by 11 |
| Complete held rows / labeled probabilities | 40 / 224 |

All parent records 0..63 are required, not just records used to detect the
preceding obstruction. The compact row order is parent first, then increasing
allowed record: eight rows each for P1/P3 and sixteen each for P2/P4/P5.
Each compact row retains its explicit representative among the 320 rows,
with omitted record bits zero; all other expanded records are checked too.

The new combinatorial work is restricted to the eleven supported children,
their deletion parents, five parents and their 43 individual forward children,
the four held classes, and the explicitly bounded natural relabelings below.
There is no new complete size-six or size-seven catalogue. An inherited
terminal-six catalogue replay inside the accepted prefix helper is distinctly
the unchanged prefix verification, not a new six-parent probability table.

### Natural-label and transport audit

For any declared seed, enumerate only permutations of that seed's at-most-
seven vertices and keep those that are natural order labelings. Class keys
are the least resulting predecessor tuples. Isomorphic realizations, not
just literal canonical tuples, determine supported child membership.

For affected parents the natural relabeling counts are 6,3,2,2,1, respectively:
fourteen actual relabelings, including automorphisms, and seven distinct
natural parent images. P2 has these three distinct images:

```text
(0,1,3,7,7,15)
(0,1,3,7,15,7)
(0,1,3,7,7,23)
```

Each other parent has one natural image, possibly reached by multiple
permutations. It would be incorrect to reuse RI-84's narrower assumption
that every natural image equals its chosen parent representative.

Transport parent order, full record and individual ideal together under each
of the fourteen relabelings. The complete comparison domain is

\[
 (6\cdot11+3\cdot9+2\cdot8+2\cdot8+1\cdot7)\,64=8448
\]

marked-ideal comparisons, including 4864 supported comparisons. Direct
transported deletion products use the same held table, without another
inherited probability query. The implementation recomputes every comparison's
factors, giving exactly 10,752 transported factor occurrences. It retains
counts, parent images and an aggregate digest of all ordered comparison
metadata, including each comparison's factor digest. Individual transported
cases/digests and their factors are incorporated into that aggregate but are
not separately serialized. They can all be rederived from the complete held
table and retained structural relabelings; an independent audit must do so.
The canonical 320 rows and all their 2752 raw factors are fully serialized.
The canonical inventory, transported comparison count and transported factor
count are separate quantities, not interchangeable coverage claims.

The proof of arbitrary marked-parent equivariance remains the inherited
factorwise transport argument and class-invariant multiplier. The finite
natural-label audit corroborates the explicitly frozen representative domain;
it is not a sweep over arbitrary new parent classes.

## 3. Held probabilities and record projections

The only new held queries are complete rows on:

| Order | Allowed complete query records | Slots |
|---|---|---:|
| C3=(0,1,3) | 0..7 | 32 |
| C4=(0,1,3,7) | 0..7, unique top zero | 40 |
| C5=(0,1,3,7,15) | 0..15, unique top zero | 96 |
| H5=(0,1,3,7,7) | 0..7, both tops zero | 56 |

Every row includes its full complement and every separate ideal probability.
Strict positivity and exact normalization are checked before parameter use.
Compared with RI-82, C3 and H5 are the only additional unmarked held classes.

Unique-top invariance follows because proper ideals exclude that top and the
full probability is their normalized complement. H5's stronger two-top
invariance follows the inherited C4 diamond b*h=c*d, not erasure by fiat:
both one-top slots are separately retained, transported and checked against
the diamond; their equality and the full complement remove both top marks.
C5 bit3 is retained. No bit0-only assumption is made, and all three stem
bits remain in the symbolic parameter domain.

For each deletion factor, its containing expanded row and ideal entry retain
the original parent/record/ideal. The factor retains the deleted subset,
kept vertices, induced order/precursor, raw transported record, locality-
restricted record, final held query, projection theorem, exponent and value.
Omitted maxima are recomputed from the retained parent/ideal. Every induced
held order is already one of the four canonical HELD tuples, which is checked
explicitly; no additional canonicalizing permutation is applied or claimed
serialized. A proper factor may erase records outside
its precursor; a full factor initially retains all records. Additional top
projections must follow the stated lemmas. Exponents are +1 for odd deletion
subset size and -1 for even size; all factors are strictly positive.

The 64 compact rows are the five symbolic row forms in RI-85 equation
(10), while expanded coefficients are reconstructed independently from the
generic deletion product. Each row then checks exact equality. Repeated
ideal slots remain repeated summands, not averaged or automorphism-divided.

## 4. Exact linear decision and width verification

Use canonical reduced rational strings and exact integer domains. Deterministic
row reduction scans columns left-to-right and takes the first eligible pivot
row, normalizes it and eliminates its column from every other row. Retain
rank, pivots, complete RREF and the canonical null basis in increasing free-
column order. Do not accept a rank flag without checking the reduction.

If the first canonical null vector with nonzero first coordinate exists,
divide by that coordinate to fix z1=1. Verify every compact and expanded
residual; choose epsilon=1/[2(1+max|z_j|)] and retain all eleven positive h7
values, each greater than one half. Check the exact open upper endpoint
min(-1/z_j over negative z_j) as well as the deterministic interior point.

The complete-row width functional is calculated by summing every target-row
ideal contribution and its actual supported child width. On the harmonic
kernel it equals (a0*g0^3/b0^3)*z1. The resulting gain divided by the unknown
positive a6 is epsilon times that strictly positive functional. No numerical
baseline expectation, support-conditioned expectation or new scale is used.

Otherwise solve M^T y=e1 exactly, with free variables zero under the same
pivot convention. The signed, unrestricted rational y is a row-span witness,
not a nonnegative optimization dual. Verify all eleven identities and lift
the witness through the declared representative-row map, without dividing by
record multiplicities. A nonzero kernel alone is not a width success; only
rank eleven permits the stronger zero-kernel rejection.

Three explicitly synthetic algebra fixtures are required to exercise positive
width success, width-only obstruction with nonzero kernel, and full-rank
obstruction, irrespective of the actual held-prefix outcome. Such fixtures
are not claimed to be DET laws or actual inherited probabilities. Their
execution, like the actual decision, awaits coordinator admission.

## 5. Accepted source closure and certificate replay

The only runtime scientific closure is the new checker plus these four
unchanged accepted inputs, all pinned before any helper loading:

| Input under docs/track_b | SHA-256 |
|---|---|
| native_growth_plancherel_graft_v1/check.py | edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c |
| native_growth_expected_defect_completion_v1/check.py | 39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b |
| native_growth_expected_defect_completion_v1/CERTIFICATE.json | f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b |
| native_growth_height_normalization_v1/CERTIFICATE.json | 3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969 |

Use RI-74's actual rebuild_prefix()/prefix_row() closure, unwrapping any
cached function before accessing its live initialized namespace. RI-63 row()
stops at four and must not substitute for actual q5. No RI-84 checker is a
runtime dependency; its accepted implementation is a read-only source pattern.
The design pin is provenance, not an additional executable dependency.

The rebuilt prefix must match actual probability manifest
`7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378`
and inherited problem identity
`dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c`.
Its 69 canonical stages and 15 inherited refusal controls are reported
separately from every new intended-reason control.

Witness mode emits a deterministic full JSON certificate to stdout only.
Saved modes rebuild the complete bounded witness from pinned actual inputs,
check every field/type/list domain, and compare the full saved JSON—not just
the reported disposition, selected residuals or a digest. The checker writes
no file and accepts no target or output override. The coordinator alone may
retain successful witness bytes as the candidate certificate.

The scientific schema is `ri88-four-vertex-cap-v1`. The saved witness has the
following strict top-level sections; no unknown fields or missing sections
are accepted by full reconstruction comparison:

| Section | Evidence bound |
|---|---|
| schema, checker_sha256, design_sha256, dependencies, domain | Exact source/design/input identities and finite scope |
| prefix | Actual held-prefix identity, stages and inherited controls |
| structure | Ordered caps/parents, all natural seed images, widths, deletion and forward lists |
| held_rows, parameters | Complete 40-row/224-slot inputs and every symbolic parameter extraction |
| compact_rows | 64 exact coefficient rows and explicit representative raw-row IDs |
| expanded_rows | All 320 rows, 2752 ideal occurrences and 2752 raw deletion factors |
| coverage | Exact finite-domain counts |
| transported_audit | Parent relabelings/images, 8448 comparison count, 10752 factor count and aggregate manifest |
| exact_decision | Complete rational reductions/operation traces, rank, pivots, null basis and canonical primal or signed-dual witness |
| width_target | All 22 ideal/newborn terms, full-row width coefficients and positive z1 multiplier |
| admission | Positive amplitude/interval/all h values/gain and 320 residuals, or the 320-coordinate dual lift and identity |
| refusal_controls | Ordered new intended-reason refusal names and explicitly synthetic branch ranks/dispositions |

The primary 64-by-11 reduction and, on obstruction branches, the 11-by-65 augmented
dual reduction retain all elementary row operations. Validation replays those
operations and separately recomputes the deterministic RREF before trusting
rank, basis or signed-dual coordinates. This is exact checking within the
producer; the separately required independent full certificate consumer is
still a distinct later obligation. Refusal inventory and final source pins
are recorded after complete source review below.

JSON parsing must reject duplicate keys, nonfinite constants and decimal
numbers. Rational fields must be canonical reduced strings. Exact integer
type checks reject booleans before domain membership and any cache lookup;
unhashable malformed values must fail the intended public guard rather than
leak an incidental cache error. Checks remain active under Python -O.

## 6. Prospective execution custody

The fresh source-only evidence root is
`/Volumes/AI_DATA/development/det-review-evidence/ri88-qr-source-6aRFc9`.
Its RUN_PROTOCOL.md specifies the prospective witness/normal/optimized arrays,
fresh original/copy/interpreter/monitor identities, exact environment, missing
authorization placeholders and exclusive attempt paths. A prepared freeze
with a null authorization hash is intentionally inadmissible.

The supervisor adapter is prepared from the previously qualified RI-84 source
with only the fresh root, every scientific target/absence path, new checker
hash and descriptive header changed. Its versioned custody schema tags stay
unchanged; the distinct scientific certificate is RI-88. Complete source-delta
review and explicit coordinator carry-forward adjudication are required.
Prior qualification is not an execution of the new source, and no old
authorization, witness receipt or scientific candidate authorizes RI-88.

The prospective per-attempt limit is 120 seconds and 512 MiB sampled owned-
process-group RSS, complemented by internal elapsed/peak checks. Sampled RSS
is not an allocator-hard cap. No automatic retry, increased limit, source
patch, domain trimming or alternate command follows a failure. Process/signal
cleanup limitations are retained from the reviewed supervisor, not erased
by successful finite qualification cases.

Child and monitor environment is exactly PATH=/usr/bin:/bin, LANG=C,
LC_ALL=C, TZ=UTC, and __CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0. The Darwin
startup addition is bound explicitly. Every child uses the isolated standard-
library interpreter with -I -S -B; optimized adds -O. Scientific progress
stderr is expected; it must not be treated as an automatic failure solely
because it is nonempty. Monitor stderr has its own strict empty requirement.

The first witness requires both repository and copied new certificates absent
before admission and after completion. Later saved replays require their own
addendum, candidate/witness pins and per-mode authorizations. Every attempt
retains preparation/admission records, full streams, all raw monitor samples,
pre/post input identities and receipt. Both a successful receipt and actual
supervisor exit zero are required; a late signal can invalidate receipt-only
success. A separate full independent certificate arithmetic audit and final
coordinator adjudication remain mandatory after actual execution.

## 7. Intended-reason refusal inventory

The source declares **90 distinct new intended-reason refusals**, with an
explicit count/uniqueness guard. This is a source inventory, not a claim of
90 executed passing controls. The fifteen inherited controls and the three
synthetic branch fixtures are separate. The ordered new names are retained
in the future certificate and in the external source-only inventory.

The controls cover strict JSON/rational encodings and dependency identities;
exact types and cache guards; bounded orders and held-query/scale refusals;
actual-prefix/full-complement/twin-diamond integrity; support ordering and
widths; complete deletion/ideal/record inventories; individual forward
multiplicities; generic factor sign/value/record provenance; both distinct
parent images and same-image automorphisms; simultaneous record/ideal
transport; exact matrix dimensions, row operations and basis selection;
signed duals and representative lifting; strict positive amplitude endpoints;
all three dispositions; complete saved-certificate fields; full-row width
conditioning/sign/fair-bit factors; and transport/design pins.

Two load-bearing mutations are explicit rather than merely numerical:

- A P1 ideal7 coefficient multiplied by four tests misuse of its four
  backward deletion roles as one forward transition's weight. The generic
  deletion-product-versus-symbolic-slot guard must refuse it.
- On moved P2=(0,1,3,7,7,23), record16, ideal23, deleting vertex3 gives
  kept vertices (0,1,2,4,5), C5 precursor15 and raw/local/query record8.
  Changing only the final query to zero is refused even if the corresponding
  actual probabilities happen to coincide. This prevents loss of the retained
  cap-root bit without assuming any particular coefficient contrast.

The algebra-only fixture ranks are analytically 1,2,11. Their expected
dispositions are positive width, width-only obstruction and full-rank
obstruction. The middle fixture deliberately requires a negative dual
coordinate, so clipping signed coefficients or dividing them by expanded
record multiplicities cannot satisfy its identity. These fixtures do not
provide additional native rows or an observed outcome for the real matrix.

## 8. Stable source review and handoff

The checker is **1,145 lines /66,081 bytes**, SHA-256
`93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568`.
The external supervisor adapter is **584 lines /30,650 bytes**, SHA-256
`76c7bf703619db3a1680824a5cb8e5d08a98fdccecf166bfc08b53244b8c7454`.
Its qualified predecessor and exact narrow changes are separately bound in
the external provenance/delta review; keeping protocol tags does not inherit
an old execution authorization.

The main worker read the complete checker. Two independent reviewers read
the full source and all final deltas and found no mathematical, domain,
transport, exact-decision, schema or intended-reason blocker. They also
reviewed the complete supervisor adaptation and prospective custody plan.
The late source changes enforce the exact 90-control inventory and retain
the internal alarm through final serialization/flushed output/resource check;
a post-output failure still invalidates acceptance through its nonzero exit.

Source-only AST parsing and compilation at optimization levels zero and one
passed, without executing any compiled target code. The checker contains
no removable assert nodes. Hash/link/hygiene and original/copy checks are
metadata checks, not mathematical coefficient verification or a measured
120-second/512-MiB performance result.

No checker/helper, synthetic fixture, supervisor, qualifier, enumeration or
coefficient calculation has run for RI-88. Both new-certificate locations and
all attempt/authorization locations are absent at the source-only handoff
snapshot. The prepared witness freeze has a null authorization hash and is
deliberately inadmissible. No saved-mode addendum or authorizations are created.
The external handoff manifest binds this note, source copies, dependency and
runtime identities, declared control inventory and review records.

This two-file packet is source-stable for complete independent coordinator
review and publication. Actual coefficients, rank, width feasibility and
performance remain unevaluated. Only a subsequent explicit admission may
create genuine execution evidence; full certificate adjudication remains a
separate obligation. No further worker source changes or execution are implied
by this handoff.
