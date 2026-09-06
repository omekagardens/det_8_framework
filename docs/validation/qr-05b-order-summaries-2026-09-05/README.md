# QR-05B: question-relative summaries of quantum-record orders

5 September 2026. Bounded research following QR-05A commit
`9a53d55d1f37842a104c573d347808cd200dada3`. This protocol is fixed before
retained capture; outcomes belong in RESULTS.md. No RET integration or gravity claim.

## Question and adopted model

What must a compressed present description retain to preserve a declared
family of future quantum/order questions? Distinguish per-history sufficiency
from summing a known fine-grained mixture. The latter always permits an exact
pushforward; it does not establish a closed predictive law on the summary.

Use the 56 three-birth natural histories retained by QR-05A, separately for
weak_phase, grouped_dephase, zero_link_boundary, and chain_boundary. These
are its four consistent examples. The parent order, settings, binary outcomes,
and source CP map J_h come from the SHA-pinned QR-05A result artifact. No
QR-05A source is modified or executed. One additional birth uses the same
record-independent transitive-percolation rule and same quantum instrument.
This does not extend QR-05A's four-event covariance certificate: only the
specified one-step continuation questions are examined here.

The quantum payload remains one fixed qubit. Quantum maps and their classical
records are not spacetime, and abstract incomparable events are not thereby
physically spacelike. This model supplies order probes; an experimental
interface giving access to those probes is a separate problem.

## Future question families and sufficiency

Write c(C)=(n,links,incomparable pairs,minimal elements,maximal elements).
For a precursor ideal S, let b(S)=sum of its past outcome bits modulo two.
The next-birth setting is fixed by b, and its recorded outcome is x in {0,1}.
Let I[b,x] denote the weak-phase or grouped-dephase outcome map and

`q(C,S) = p^(number of maximal elements of S) (1-p)^(n-|S|)`.

Define three probe kernels, each retaining the residual quantum payload:

1. `payload`: one outcome, map J_h.
2. `order_counts`: outcome a has map 1[c(C)=a] J_h. This is a mathematical
   nondisturbing read of already retained classical order data.
3. `next_birth`: outcome (m,b,x) has map
   `T_h[m,b,x] = sum_{S ideal: |S|=m, b(S)=b} q(C,S) I[b,x] composed with J_h`.
   Ideals with the same recorded output are mixed as CP maps, not amplitudes.

The three cumulative families are F0={payload}, F1=F0+order_counts,
F2=F1+next_birth. Order-count outcomes range over the sorted count tuples of
all retained parent orders; next-birth outputs include all 16 triples with
0<=m<=3 and b,x in {0,1}, including zero branches. Summing the payload or
order-count probe's outcome maps gives J_h exactly. Summing next-birth
outcomes preserves its trace functional, not generally J_h itself: a
nonselective quantum measurement can change the residual state. The initial
development assertion conflated these two conditions and was corrected after
its first direct-executor check failed, before any result capture.

Two histories are equivalent for F precisely when their complete map-valued
signatures agree for every probe/outcome in F. A candidate summary is sufficient
when every pair given the same summary label is equivalent. Compare maps, not
a selected set of input states. This preserves joint history/future-outcome
probabilities and residual quantum output for every initial qubit state and
every later common payload measurement. It is deliberately stronger than
QR-03's conditional-probability equivalence and is not claimed to be its
coarsest partition.

All zero source maps remain in the inventory. They have zero signatures and
can share an operational class, even when their formal order records differ.
No conditional prediction is assigned to a never-possible branch. Equality of
these kernels is not structural identity or deletion permission for records.

The calculated equivalence classes are the coarsest classes for this declared
finite signature. Expansion F0 to F1 to F2 must refine, never merge, classes.
This is not a claim about all possible interventions or arbitrarily many births.

## Candidate summaries

Test the following fixed partitions separately in each source fixture:

- `constant`: forget every fine-history distinction.
- `source_effect`: keep only the source probability functional trace(J_h(rho)).
- `payload_map`: keep the complete unnormalized J_h.
- `payload_counts`: keep (J_h,c(C)).
- `decorated_order`: keep the order up to isomorphism, decorated by the
  transported (setting,outcome) pairs. Ignore natural birth labels, not marks.

Decorated isomorphism is expected to suffice for F2 in these intrinsic,
birth-covariant fixtures. This can be checked independently of a candidate's
name. It is not assumed that basic counts reconstruct a larger order, or that
this small question family always reconstructs the marked order.

Prespecified nonboundary prediction: the weak-phase and grouped-dephase
fixtures each give 26 F0 classes, 29 F1 classes, and 32 F2 classes. The first
split resolves three fork/join payload collisions. The last resolves record
locations on one-edge orders and a chain collision. Boundary p=0 and p=1
must retain all zero histories; payload_map is expected to suffice for their
restricted F2 source kernels even if it fails at p=2/5.

## Analytical controls fixed before execution

For the all-zero fork and join at p=2/5, QR-05A retained the identical source
map `(12/125) D_0^3 rho D_0^3`. Their next-precursor size probabilities are
respectively `(27,18,60,20)/125` and `(27,36,12,50)/125` for m=0,1,2,3,
after summing quantum outcomes. In particular the full-parent precursor has
probability 4/25 for the fork and 2/5 for the join. These are conditional
growth probabilities given either nonzero history; no new growth law is used.

A stronger collision uses the one-edge order `[[],[],[0]]`, with records
(0,0,1) and (0,1,0). Both have all settings weak0, weight 18/125, the same J_h,
and identical counts (3,1,2,2,2). Yet the next-birth event (m=1,b=1), summed
over x, has conditional probability 0 versus 18/125. The two histories have
the same separate m distribution and the same b distribution (P(b=1)=2/5).
Their lost information is an order/record correlation, not either marginal.

To produce physical witnesses for invalid candidates, test a fixed
informationally complete bank only after the exact signature comparison:
four full-rank input states with Bloch vectors (0,0,0), (1/2,0,0), (0,1/2,0),
(0,0,1/2), and effects P0, P1, P+X, P+Y. Each bank spans the Hermitian operator
space. Therefore any distinct Hermiticity-preserving maps have a witness in
these 16 input/effect combinations. Retain source probabilities and unequal
joint probabilities, not conditional values on zero histories.

## Aggregation and refinement checks

Retain each distinct natural history once, including zero ones. Compare
direct summation to count classes with summation via decorated-order classes;
then compare direct total summation with both staged routes. Perform the
comparisons on the entire F2 signature, not just on total trace. Count classes
are a well-defined coarsening of decorated-order classes. Every equality is
finite associativity of sums with the same members, not a scale-limit result.

As a negative multiplicity control, average maps within each decorated class
and then sum the class averages. Compare its source map and trace on I/2 to
the correct total. This deliberately replaces distinct generative paths with
one representative-equivalent contribution. It is expected to lose probability
mass where live class multiplicities exceed one; the p=1 chain boundary can
hide the mistake because its live classes have one member each.

Successful aggregation is compatible with failed per-history sufficiency.
Computing aggregate next-birth maps from a known fine mixture uses information
that the current aggregate payload map alone may no longer contain. The
fork/join and record-location controls obstruct a universal payload-only or
payload-plus-counts continuation rule on the declared domain.

## Fixed input and canonical output contract

Input is exactly `{schema_version: "det8-qr05b-problem-v1", case: case_id}`,
where case_id is one of the four names above. Unknown fields, types, schemas,
or names are rejected explicitly, including under optimized Python. This is
a fixed in-memory research fixture interface, not a public general-purpose SDK.

All source and future maps in these four diagonal-instrument families are
diagonal as 4x4 superoperators in row-major matrix-unit order. Retain a map as
its four diagonal entries, each `[canonical_real,canonical_imag]`. The twelve
off-diagonal entries are zero by construction and are checked on source
decoding and direct continuation. This compact encoding retains the full map.

```text
case, count_keys, birth_keys
histories: [{order,outcomes,settings,counts,decorated_key,source,next_birth,zero_source}]
candidates: [{name,classes}]
families: [{name,classes,refines_previous,candidate_checks:[{
  name,valid,conflicts:[[i,j],...],first_witness: object|null
}]}]
aggregation: {direct_counts,via_decorated_counts,direct_total,via_counts_total,
              via_decorated_total,counts_equal,totals_equal,
              wrong_average_source,wrong_average_trace,correct_trace}
controls: {fork_join,record_location}
counts: {histories,zero_sources,continuation_blocks,decorated_classes,
         family_classes,candidate_checks,candidate_conflicts}
```

Histories retain QR-05A terminal inventory order. Count keys and birth keys
are lexicographically sorted integer lists. A decorated_key is `{relation,
record}` as in QR-05A. Classes are sorted by first member; members and all
conflict pairs are increasing. Candidate/family order is as listed above.
`refines_previous` is null for F0, a boolean otherwise.

A signature is `{source:diag,counts:[diag per count_key],birth:[diag per birth_key]}`.
Aggregation count entries are `{key,members,signature}`. All total signatures
retain every branch. A first witness uses the first conflict pair, first
different probe in payload/counts/birth order, first output in its bank, first
input in the specified bank, then first effect in P0,P1,P+X,P+Y order. Its
fields are `{histories,probe,outcome,input_bloch,effect,source_probabilities,
joint_probabilities}`; outcome is null, a count tuple, or a birth triple.

Controls identify histories by their actual order/outcome record, not by
hardcoded index. fork_join records the two indices and each exact distribution
of m; record_location records two indices, each joint (m,b) table, both
marginals, and source/count equality. Fractions are canonical strings. The
control arrays use the same increasing m,b order throughout. Controls are
reported for each case, even when boundary zero weights make a conditional
source statement unavailable; growth distributions there are formal model
quantities, explicitly separate from source reachability.

Both control objects have fields `{histories,source_live,source_equal,
counts_equal,distributions}`. `source_live` contains two booleans; each
distribution has `{joint,size,parity}`. The joint table has four rows (m)
and two columns (b). The other two arrays are its corresponding marginals.

## Independent routes and evidence discipline

The primary route applies exact Kraus operators to source-output matrix units
using SHA-pinned QR-01 arithmetic. The independent reference directly derives
the diagonal continuation coefficients and independently enumerates ideals,
counts, marked isomorphisms, partitions, witnesses, and aggregation. Both read
the same SHA-pinned QR-05A source artifact; this is new verification of
summaries/continuations, not an independent recreation of that prior study.

All rational arithmetic is exact. The bounded fixed sources have small
components; new arithmetic has a 4,096-bit guard. Retain inputs, full analyses,
rejected cases, closed-form controls, source identities, prior artifact hashes,
runtime and observed retained component growth. Capture is create-only,
replay read-only; no edits to prior evidence or mutable RET/T8 imports.

For each retained source, continuation, and aggregation map, also check exact
complete positivity. A diagonal matrix-unit superoperator has Choi support
on the two-dimensional span of |00>,|11>; its nonzero block has entries
`[[d0,d1],[d2,d3]]`. Hermiticity, nonnegative diagonal entries, and
`d0*d3 >= |d1|^2` give an exact check for this special form. This is not a
general-purpose positivity solver. Repeated maps in different retained
locations count as repeated checks, not distinct mathematical maps.

### Reproduction

From the checkout root, use fresh external cache directories for every run:

```sh
qr05b_test_cache=$(mktemp -d /tmp/det8-qr05b-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05b_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05b-order-summaries-2026-09-05/
qr05b_opt_cache=$(mktemp -d /tmp/det8-qr05b-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05b_opt_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05b-order-summaries-2026-09-05/
```

Capture only when results.json does not exist:

```sh
qr05b_capture_cache=$(mktemp -d /tmp/det8-qr05b-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05b_capture_cache" docs/validation/qr-05b-order-summaries-2026-09-05/study.py
```

Thereafter replay read-only:

```sh
qr05b_replay_cache=$(mktemp -d /tmp/det8-qr05b-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05b_replay_cache" docs/validation/qr-05b-order-summaries-2026-09-05/study.py --verify
```

The source ledger covers this protocol, both executors, study.py, both test
files, and the pinned QR-01 exact arithmetic source. Five earlier result
artifacts are separately pinned. The result schema, canonical envelope,
source/prior identities, exact suite, and byte stability are checked on replay.
Runtime metadata is retained but excluded from mathematical equality. Hashes
provide local integrity evidence, not authentication or independent experimental
preregistration. Source changes require a new version, never an overwrite.
RESULTS.md and the research plan remain interpretation documents outside the
source ledger. Lifecycle tests use temporary stub artifacts, not real captures.

Run short checks in the existing Python environment with -I and a fresh
external -X pycache_prefix, disabling pytest's checkout cache. Do not install
Lean, dependencies, or plugins. This gate does not establish QR-05C scale
consistency, an apparatus-to-order mapping, a metric, or Einstein dynamics.
