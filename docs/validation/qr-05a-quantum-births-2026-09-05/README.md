# QR-05A: finite growing orders with quantum outcome records

5 September 2026. New bounded mathematical research after QR-04; results belong
in RESULTS.md after execution. No empirical gravity, Lorentz-covariance,
record-dependent growth, coherent-order, or RET integration claim.

## Mathematical model

An order C of n naturally labeled events is a tuple of strict-past sets P_j,
each contained in {0,...,j-1}, with i in P_j implying P_i is contained in P_j.
Each event has one binary outcome R_j and its selected setting s_j. The record
is append-only. A birth selects an order ideal S of C and appends a new
maximal event with strict past S. The quantum payload remains H=C^2 throughout.

For transitive percolation with rational 0<=p<=1,

`q(C,S) = p^m(S) (1-p)^(n-|S|)`,

where m(S) counts maximal elements of S and empty powers equal one, including
0^0. The weights sum to one over ideals. The full path weight is
`W_p(C) = p^(number of links) (1-p)^(number of incomparable pairs)`.
This is adopted classical causal-set mathematics, not a DET-native law.
A normalized uniform-over-ideals rule is retained only as a negative control.

For fixed parent record R and chosen S, a policy selects a setting and a binary
instrument `I[C,R,S,x](A) = sum_a M_a A M_a^dagger`. The quantum birth submap is

`B[C,R,S,x](A) = q(C,S) I[C,R,S,x](A)`.

The scalar q multiplies the map; no irrational square root is needed in the
exact representation. Summing all ideals and outcomes is trace preserving.
Branch states remain unnormalized, including zero maps. The selected setting
and outcome are both recorded. This is a classical mixture of order births,
not a coherent sum over alternative orders.

## Fixed bounded input schema

```text
{
  schema_version: "det8-qr05a-problem-v1",
  births: 1 | 2 | 3,
  growth: {kind: "percolation", p: canonical_rational_string}
       | {kind: "uniform_ideals"},
  instrument: "weak_phase" | "weak_dephase" | "parity_zx" | "stage_zx"
}
```

These are named, fixed mathematical fixture families, not arbitrary user
callbacks or a general public SDK. Unknown fields, booleans as birth counts,
noncanonical/nonfinite/out-of-range/oversized probabilities, invalid rule
names, and bounds violations are rejected explicitly. Probability input
components are bounded to 64 bits; exact complex arithmetic has a 4096-bit
guard. Outcome and setting sets are specified below, not inferred from data.

Let D_0=diag(3/5,4/5), D_1=diag(4/5,3/5), V=diag(1,i), and Z=diag(1,-1).
For the first three families a mechanically supplied read context contains
only outcome bits from S. Its parity is c=sum_{j in S}R_j modulo two.

- weak_phase: setting `weak0`/`weak1`; one Kraus V^c D_x per outcome.
- weak_dephase: setting `dephase0`/`dephase1`; two Kraus operators
  (3/5)V^c D_x and (4/5)Z V^c D_x per outcome. This is a grouped phase-noise
  channel, not two separately recorded outcomes.
- parity_zx: setting `Z` for c=0, `X` for c=1; ordinary projectors P_0,P_1
  or Q_+=(I+X)/2,Q_-=(I-X)/2, labeled outcomes 0,1 respectively.
- stage_zx: setting `Z` for even current n, `X` for odd n. It reads no
  records but intentionally depends on ambient birth count: a negative
  covariance control, not a permitted example of intrinsic past-local law.

All quantum operations act on the same fixed qubit. Past-scoped classical
reads do not imply that this shared payload is physically local to spacelike
separated events. The positive families supply algebraic commutation only.

## Three distinct comparisons

1. **Normalization:** enumerate all labeled parent orders and outcome records
   below the birth bound, including source-impossible ones. Check growth-row
   normalization, instrument completeness, and the summed birth map's trace
   action on every matrix unit.
2. **Universal birth diamonds:** enumerate all parents of size at most
   births-2, every binary record, and every ordered pair of ideals (S,T),
   including S=T. Compare the two incomparable births S then T and T then S,
   neither of which includes the other new event in its past. Identify the
   new record slots as A and B on both sides. Compare setting labels and all
   four outcome-resolved maps on arbitrary intermediate operators, both with
   and without the growth weights. These are not necessarily source-reachable
   intermediate states. Weighted zero maps never excuse an unweighted failure.
3. **Full birth relabeling:** enumerate every natural terminal order and binary
   record, and every linear extension of that terminal order. Transport the
   order, outcomes, and selected-setting record through that relabeling. Compare
   with the independently composed map of the resulting natural birth history
   from every original quantum input. Include automorphisms mapping an order
   and outcomes to themselves; a changed setting record still fails equality.

Universal diamonds are stronger than fixed-source full-history equality.
For the chosen equivariant growth and intrinsic past-parity rules, unchanged
past contexts plus the complete diamond identities give full birth-label
equality through adjacent incomparable swaps. The stage control can violate
setting-record equality independently of how terminal labels are grouped.

After all labeled paths have been retained, separately form the pushforward
to isomorphism classes of orders decorated with setting/outcome pairs, summing
the complete CP maps of distinct natural histories exactly once. This is an
aggregation of a specified generative sample space; it is not an average per
labeling and does not assert equivalence of arbitrary fine-record feedback.

At three births, there are 1,2,8,56 natural outcome-marked histories at levels
0,1,2,3, and 11 parent normalization rows. There are nine ordered-pair diamond
contexts (one at size zero; eight from size-one records/ideal pairs), each with
four outcome pairs. Terminal comparisons include the identity relabeling and
must report nonidentity comparisons separately.

## Canonical analysis output

Both implementations expose `analyze(wire)` and return identical ordinary
JSON-compatible data. Complex cells are `[canonical_real, canonical_imag]`
rational-string pairs; superoperators use row-major matrix units, output first.
Orders are lists of sorted strict-past lists. Histories at each level are sorted
by order tuple then outcome tuple; setting labels are derived and retained.

```text
levels: [{births, histories: [{order, outcomes, settings, weight, superoperator}],
          total_map, trace_preserving}]
normalization: [{order, outcomes, growth_sum, instrument_complete,
                 birth_sum_trace_preserving}]
diamonds: [{order, outcomes, left_ideal, right_ideal,
            forward_weight, reverse_weight, unweighted_equal, weighted_equal,
            branches: [{outcomes: [x,y], forward_settings, reverse_settings,
                         forward, reverse, weighted_forward, weighted_reverse}]}]
relabelings: [{history, permutation, target, settings_expected,
               settings_equal, map_equal, equal}]
classes: [{key: {relation, record}, members, superoperator}]
flags: {normalized, unweighted_diamonds_equal, weighted_diamonds_equal,
         terminal_relabeling_equal}
counts: {level_histories, normalization_rows, diamond_contexts,
          diamond_outcome_pairs, terminal_relabelings, nonidentity_relabelings,
          terminal_classes, zero_terminal_maps}
```

Diamond contexts are sorted by parent order, outcome record, S, then T; both
S and T range over sorted ideals. Their branch outcomes are (0,0),(0,1),(1,0),
(1,1). Both setting lists are in the identified new-event order [A,B], including
when B was executed first. A diamond equality flag requires matching settings
and maps for every outcome pair; all maps and settings remain in the output.

`permutation` lists old event indices in new natural birth order. Include every
linear extension in lexicographic order, including automorphisms and identity.
The target indexes the same terminal history inventory; compare its actual
settings with the transported expected settings, not just its outcomes.

Class `relation` is the row-major string of n*n binary precedence entries in
an arbitrary relabeling, with entry (i,j)=1 iff i precedes j. Class `record` is
the corresponding list of [setting,outcome]. Choose the lexicographically
smallest (relation, tuple(record)) over all n! permutations; sort classes by
that key and member indices increasingly. Do not discard zero members.
`level_histories` lists counts from zero through the declared birth bound.

## Independent routes and retained evidence

The primary route applies Kraus operations directly to all four qubit matrix
units. The reference builds and multiplies exact 4x4 superoperators using a
separate complex-number representation. Both independently enumerate ideals,
validate inputs, select instruments, transport labels, and group terminal
histories. Reuse only SHA-pinned QR-01 arithmetic, not mutable T8/RET sources.

An additional closed-form oracle covers every positive-family terminal map.
Let n0,n1 count the outcome bits and k count events with odd strict-past parity.
Set A=diag((3/5)^n0(4/5)^n1, i^k(4/5)^n0(3/5)^n1). For weak_phase the map is
`rho -> W_p(C) A rho A^dagger`; for weak_dephase the same expression has its
off-diagonal entries additionally multiplied by (-7/25)^n. For uniform growth,
replace W_p by its actual product of growth probabilities; no label-free
percolation identity is asserted for that negative growth law.

Eight prespecified three-birth cases: weak_phase and weak_dephase at p=2/5;
weak_phase at p=0 and p=1; parity_zx at p=2/5 and p=0; stage_zx at p=2/5;
and weak_phase with uniform-over-ideals growth. Predictions before running:
the first four pass all comparisons; parity_zx at p=2/5 conflicts; its p=0
version retains an unweighted conflict hidden by zero order weights;
stage_zx fails complete record covariance; uniform growth fails weighted
diamonds/full birth covariance despite commuting quantum operations.

An independently derived, pre-capture non-reconstruction control compares the
three-event fork (one minimal event preceding two) and join (two minimal events
preceding one), with all outcomes zero. They are nonisomorphic but both have
two links, one incomparable pair, k=0, and amplitude D_0^3. At p=2/5 both maps
are `(12/125) D_0^3 rho D_0^3` for every input. This checks that the payload
map and its branch probability alone cannot recover the retained event order.
The complete order records still distinguish the two histories.

Retain full maps, explicit zero branches, count conventions, first discrepancy
witnesses, complete inputs, rejection cases, source identities, prior artifact
identities, runtime, and rational bit growth. A source-ledger change requires
a fresh result version, never an overwrite of retained evidence. Capture is
create-only and replay is read-only. No random sampling or tolerance equality.

### Running and replaying

From the checkout root, use the existing Python 3.11 environment and a fresh
external bytecode cache for each command. The runner rejects non-isolated
execution, a cache inside the checkout, and a filesystem-root cache prefix.

```sh
qr05_test_cache=$(mktemp -d /tmp/det8-qr05-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05a-quantum-births-2026-09-05/
qr05_opt_cache=$(mktemp -d /tmp/det8-qr05-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05_opt_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05a-quantum-births-2026-09-05/
```

Capture exactly once, only when `results.json` does not already exist:

```sh
qr05_capture_cache=$(mktemp -d /tmp/det8-qr05-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05_capture_cache" docs/validation/qr-05a-quantum-births-2026-09-05/study.py
```

After capture, replay without writing the artifact:

```sh
qr05_replay_cache=$(mktemp -d /tmp/det8-qr05-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05_replay_cache" docs/validation/qr-05a-quantum-births-2026-09-05/study.py --verify
```

The source ledger covers this protocol, both implementations, the runner,
both test files, and two SHA-pinned QR-01 arithmetic sources. Four earlier
result artifacts are pinned separately. Source identities are checked before
and after execution; replay checks the result schema, ledgers, exact suite,
and unchanged artifact bytes. Runtime metadata is retained but excluded from
mathematical equality. The results note and research plan are interpretation
documents outside the source ledger; changing them does not change the capture.

## Boundaries and next gate

This first construction addresses joint mathematical consistency, not recovery
of spacetime or gravity. No new quantum degrees of freedom are born, no order
feedback from records is enabled, and no classical-record summary is equated
with a metric. Grouping/refinement adequacy is QR-05B work, not a consequence
of taking an isomorphism-class pushforward here. See the
[research plan](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
