# QR-05C: finite coarse-dynamics consistency

5 September 2026. Research after QR-05B commit
`1678e8b090f0148175870368b8ade9206450f7a3`. This protocol will be frozen before
retained capture; subsequent outcomes belong in RESULTS.md. Prior artifacts,
RET/core sources, and dependencies remain untouched.

## Question and bound

When can a coarse description predict growth without access to the fine record
it discarded? Compare growing then coarsening with coarsening then growing,
including two-step composition. This is information-resolution consistency of
a finite classical–quantum model, not physical spatial rescaling, random
thinning of spacetime, a continuum limit, or gravitational dynamics.

Enumerate all naturally labeled orders and binary records at n=0,...,4.
The fine history counts are 1,2,8,56,640. A birth chooses an order ideal S,
appends a maximal event with past S and outcome x, and acts on one fixed qubit.
The selected setting is retained and is determined intrinsically by
b=sum of the outcome bits in S modulo two. Use the QR-05A weak-phase or
grouped-dephasing instruments, with D0=diag(3/5,4/5), D1=diag(4/5,3/5),
V=diag(1,i), Z=diag(1,-1):

- weak_phase: Kraus V^b D_x;
- weak_dephase: grouped Kraus (3/5)V^b D_x and (4/5)Z V^b D_x.

The birth CP map is B=q(C,S) I[b,x]. Percolation uses
q=p^(maximal elements of S) (1-p)^(n-|S|), with empty powers one.
One control uses uniform choice among ideals instead. Its rows are normalized
and relabeling-equivariant, although its complete natural-history path weights
are not birth-label invariant. That distinction must remain visible.

Five fixed cases: weak_phase at p=2/5, weak_dephase at p=2/5, weak_phase at
p=0, weak_phase at p=1, and weak_phase with uniform-over-ideals growth.
Names match QR-05A: weak_phase, grouped_dephase, zero_link_boundary,
chain_boundary, normalized_noncovariant_growth. The last is a control, not a
new proposed physical law. There are 706 outcome-resolved birth edges per case
for parent levels 0 through 3. Two-step comparisons start at levels 0 through 2.

## Classical–quantum coarse transition contract

For fine CQ blocks tau_h, define P_n(tau)_a=sum_{h:pi_n(h)=a} tau_h.
The quantum payload is preserved; only the declared classical label is merged.
For a fine parent h, the outcome-resolved coarse row is

`K_n(h,b) = sum_{h': pi_(n+1)(h')=b} B(h'|h)`.

A universal coarse birth map exists for this partition family exactly when
K_n(h,b)=K_n(k,b) for all coarse targets b and all parents h,k having the same
coarse label. Equality is of full maps on arbitrary intermediate operators,
not just trace probabilities and not just one source-produced state.

Necessity follows by applying the putative intertwining identity to a CQ input
supported on either fine parent, with the same arbitrary quantum block.
Sufficiency follows by choosing the common row as barT_n(a,b). It is a CP
instrument, and P_(n+1) T_n = barT_n P_n. When every intervening level satisfies
the condition, repeated composition gives the corresponding multi-step identity.
Nonselective measurement preserves the total trace, not generally the quantum
state; never impose an identity-channel condition on the summed instrument.

For each class choose its lowest-index fine history as a representative.
Even if the criterion fails, its row defines a normalized *trial* coarse model.
Compare this fixed trial with direct fine dynamics. A trial is not certified
by normalization, by one matching parent, or by averaging hidden parent rows.
Different representatives can give different failed trials.

Also report whether each actual-minus-trial row vanishes after composition
with the fixed original-source map J_h. This is an all-fixed-source-branches
check, weaker than the arbitrary-intermediate-block criterion. It is not a
claim about every possible preparation or a coarsest conditional summary.
Zero J_h values stay retained; they can hide a universal discrepancy.

## Nested resolution family

At every level use four summaries, in this order:

1. marked_order: canonical order isomorphism with (setting,outcome) marks;
2. shape_ones: canonical unmarked order plus total number of recorded ones;
3. link_counts_ones: (n,links,incomparable pairs,total ones);
4. size_ones: (n,total ones).

Each is a well-defined coarsening of the preceding one. Retain and check the
partition maps at every level. The reduced link-count tuple deliberately omits
minimal/maximal counts: QR-05B's five-count tuple happens to distinguish all
unmarked orders through size four and would duplicate shape_ones at this bound.

Marked classes are expected to number 1,2,7,32,192; shape_ones classes
1,2,6,20,80; link_counts_ones classes 1,2,6,16,50; size_ones classes
1,2,3,4,5. No larger-order reconstruction claim.
Marked-order closure follows from a bijection of precursor ideals under a
mark-preserving relabeling: growth weights, settings, quantum operations and
target classes are preserved. This argument also applies to uniform-ideal
growth. It does **not** require the separate birth-diamond/path-covariance
condition from QR-05A.

Compute original-source maps J_h from the empty history's identity map by
following the unique natural history path. Check their equality within marked
classes separately from quotient closure, through level four. Compare all
levels through three with QR-05A's pinned maps, including the uniform-growth
control. For the four common positive cases, also reproduce QR-05B's retained
three-parent-birth continuation outputs (m,b,x) by composing these new kernels
with J_h and summing the corresponding ideals.

## One- and two-step comparisons

One-step comparisons retain every fine parent's row to every coarse target,
the representative rows, all conflicting parent/representative pairs and
their discrepant target indices. Compare on the full operator basis.

For two steps, explicitly compose fine birth edges and then sum into target
classes. Independently compose the representative coarse rows from the two
adjacent levels. Compare for every fine parent and target class. Do not replace
the direct path calculation by associativity of a previously grouped table.
Retain both full tables and the first physical discrepancy witness.

Witnesses use full-rank input states with Bloch vectors (0,0,0), (1/2,0,0),
(0,1/2,0), (0,0,1/2), in that order, and effects P0,P1,P+X,P+Y. These two
banks span the Hermitian operator space, so a difference between these maps
has a witness. They illustrate exact-map discrepancies, not an approximate
replacement for the equality criterion. Inputs are arbitrary intermediate
payload states, not necessarily a specified original-source preparation.

## Analytical and conceptual controls

At p=2/5, the two-event chain records 01 and 10 share shape_ones (and every
coarser label). Into the three-event fork with one total recorded one, their
row maps are (6/25) D0(.)D0 and (6/25) V D0(.)D0 V-dagger. They have the same
trace functional but different quantum outputs. On E01 the coefficients are
72/625 and -72i/625. Retain the complete maps; matrix units are not physical
states.

For a delayed failure, start at the one-event record 1 under shape_ones.
Its one-step row matches its trial exactly because its parent class is a
singleton. Two steps toward the fork with one total one yield, on P+X,

`actual = [[486,-864],[-864,1536]]/78125`,

`trial = [[486,-864i],[864i,1536]]/78125`.

Both traces are 2022/78125, but a final P+X effect gives 147/78125 versus
1011/78125. The intermediate chain record 10 was replaced for prediction by
representative 01. This is a failure in the stated growth model, not an added
synthetic hidden-memory model. The pure P+X control supplements the full-rank
witness bank and does not require conditional division.

Retain the all-zero fork/join control in link_counts_ones: its parents have
the same reduced counts but the next total incomparable-pair count remains
one with probabilities 4/25 versus 2/5. Also retain QR-05B's same-shape
record-location pair 001/010; its effect on coarse transition rows is tested
here rather than assumed to be identical to QR-05B's more detailed probes.

Multiplicity control: the quotient generator sums child transitions from
**one** representative parent. P_n already sums populations across equivalent
parents. Summing those equivalent parents' generator rows again produces
trace equal to the class size. Use the first non-singleton marked class at
n=2; it has two members and the wrong row has trace two on I/2, not one.

## Frozen interface and canonical output

Input is exactly `{schema_version:"det8-qr05c-problem-v1",case:case_name}`.
Reject other fields/types/names, including under optimized Python. The interface
is a bounded research fixture, not a general-purpose or streaming SDK.

Maps are diagonal 4x4 superoperators in row-major matrix-unit order. Each full
map is encoded by its four diagonal `[real,imag]` rational-string cells; all
other entries are zero and direct execution verifies that fact. Intern maps
into `map_bank`: zero is index 0, remaining unique diagonals are lexicographically
sorted by their flattened canonical strings. Every `source`, `kernel`, and
dense row entry below is an index into that bank. Structural zero edges survive.

```text
case,map_bank
levels:[{births,histories:[{order,outcomes,settings,source}]}]
fine_steps:[{births,rows:[[{target,precursor,growth_weight,setting,outcome,kernel}]]}]
quotients:[{name,partitions:[[{key,members}]],
  steps:[{births,actual_rows,representative_rows,consistent,
          all_fixed_source_branches_equal,conflicts,first_witness}],
  two_steps:[{births,actual_rows,representative_rows,consistent,
              all_fixed_source_branches_equal,conflicts,first_witness}]}]
refinements:[{fine,coarse,levels:[{births,parent_classes,valid}]}]
source_covariance:[{births,constant,conflicts:[[representative,history],...]}]
controls:{chain_record,delayed,fork_join,record_location,wrong_parent_sum}
counts:{level_histories,raw_birth_edges,marked_classes,one_step_checks,
        two_step_checks,map_bank_entries}
```

Histories are sorted by their strict-past tuple then binary outcome tuple.
Fine edge rows are sorted by precursor tuple then x (not target index).
Partitions are sorted by first member and members are increasing. Their keys
are respectively `{relation,marks}`, `{relation,ones}`, `{n,links,incomparable,
ones}`, `{n,ones}`. Relations are row-major n*n binary strings minimized over
all n! permutations, jointly with marks for marked_order. Empty relation is
the empty string. Marks are `[setting,outcome]` pairs.

`actual_rows` has one dense row per fine parent; `representative_rows` one
per coarse parent class. Target columns follow the partition at n+1 or n+2.
Conflicts are `{history,representative,targets}` in increasing history order,
only nonempty target lists. First witness uses the first conflict, its first
target, and the input/effect bank order above; fields are `{history,
representative,target,input_bloch,effect,actual_probability,proposed_probability}`.
`refinements.parent_classes` maps fine-class index to coarse-class index.

Controls store actual history/target indices resolved by order and record,
map-bank references, and exact derived values. Detailed control fields are
fixed by the implementation and cross-checked by the independent reference;
they never replace the exhaustive comparison tables. Every retained map must
be CP. Proper fine, actual-coarse and representative-coarse complete rows must
be trace preserving; individual branch/source maps need not be. The deliberate
wrong-parent-sum control is CP but has a nonnormalized row and is not required
to pass trace preservation.

## Verification and evidence discipline

The primary route applies Kraus matrices to operator units using pinned QR-01
exact arithmetic. The reference derives diagonal coefficients and independently
enumerates orders, ideals, quotient partitions, transitions, two-step sums,
source-map comparisons, and witnesses. No new executor imports the other.
Rational arithmetic is exact with a 4,096-bit component guard; no randomness,
floating-point equality tolerance, data fitting, or empirical claims.

Retain source identities, six prior artifact identities, all inputs and complete
analyses, rejected cases, analytical controls, runtime and rational growth.
Capture is create-only and replay read-only. Run short checks with the existing
Python environment, -I, a fresh external -X pycache_prefix, and no pytest cache.
Source-ledger documents freeze at capture; later interpretation belongs outside
that ledger. Hashes are integrity evidence, not experimental authentication.

Passing this bounded dynamic-consistency study does not establish a spatial
scale transformation, a manifold, Lorentz symmetry, a metric, or gravity.
Failing a candidate summary is a useful completed investigation, not permission
to excuse the discrepancy as noise or to promote the failed coarse model.

## Wire and verification clarifications

`one_step_checks` and `two_step_checks` count dense full-map comparisons:
fine-parent count times coarse-target count, summed over the four summaries
and tested start levels. They include zero and representative comparisons,
not distinct-map or matrix-unit-execution counts. `source_covariance.conflicts`
is sorted lexicographically by representative, then history. All witness
effect strings are P0,P1,P+X,P+Y.

The analytical control schemas are:

```text
chain_record:{births,quotient,histories,target,kernels,input_bloch,outputs,
              trace_probabilities,probabilities_Px}
delayed:{births,quotient,history,representative,target,one_step_exact,actual,
         proposed,input_bloch,outputs,trace_probabilities,probabilities_Px}
fork_join:{births,quotient,histories,parent_class_same,one_step_rows_equal,
           counts_probe_incomparable,probabilities}
record_location:{births,quotient,histories,parent_class_same,row_equal,
                 first_target,kernels}
wrong_parent_sum:{births,quotient,parent_class,members,correct_row,wrong_row,
                  correct_trace,wrong_trace}
```

Control kernel/actual/proposed/row fields reference the map bank. `outputs`
are ordinary 2x2 complex-rational wire matrices for the stated pure P+X input.
The fork/join probabilities use I/2 and sum over all coarse targets with total
incomparable count one. `first_target` is null and `kernels` empty when the
record-location rows coincide. The wrong-parent trace also uses I/2.

At p=1, the reduced-count summary is expected to fail universally at parent
size three while size_ones closes. Closure therefore need not be monotone
along the resolution hierarchy. The fixed-source tests and bounded two-step
tests can still pass because their relevant intermediate states avoid the
conflicting fork. Neither pass repairs the universal one-step failure.

For these diagonal matrix-unit maps, exact CP checking reduces to Hermiticity
of the 2x2 supported Choi block, nonnegative endpoint coefficients, and
`d0*d3 >= |d1|^2`. The runner checks every bank entry once per case, including
the intentionally nonnormalized multiplicity maps, and separately checks
proper row normalization and source-level total trace.

## Reproduction

From the checkout root, use a fresh external bytecode cache for each run:

```sh
qr05c_test_cache=$(mktemp -d /tmp/det8-qr05c-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05c_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05c-coarse-dynamics-2026-09-05/
qr05c_opt_cache=$(mktemp -d /tmp/det8-qr05c-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05c_opt_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05c-coarse-dynamics-2026-09-05/
```

Capture only if results.json does not yet exist:

```sh
qr05c_capture_cache=$(mktemp -d /tmp/det8-qr05c-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05c_capture_cache" docs/validation/qr-05c-coarse-dynamics-2026-09-05/study.py
```

After capture, replay read-only:

```sh
qr05c_replay_cache=$(mktemp -d /tmp/det8-qr05c-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05c_replay_cache" docs/validation/qr-05c-coarse-dynamics-2026-09-05/study.py --verify
```

The source ledger covers this protocol, dynamics.py, reference_qr05c.py,
study.py, test_qr05c.py, test_capture.py, and the pinned QR-01 exact arithmetic
source. Six earlier result artifacts are separately pinned. The runner checks
the schema/canonical envelope, current source/prior identities, exact suite,
and unchanged bytes on replay. Runtime metadata is retained but excluded from
mathematical equality. Lifecycle tests use only temporary stub artifacts.
Source changes require a new capture version, never an overwrite. RESULTS.md
and the research plan are interpretation documents outside the source ledger.
