# QR-05: bounded exact correspondence/noncollapse verification

12 September 2026 (Pacific/Honolulu). Prospective implementation contract for
the [analytical design](../qr-05-correspondence-noncollapse-design-2026-09-12/README.md).
This document is frozen before first mathematical execution. Outcome and
publication status belong in RESULTS.md, not in this prospective source.

## Scope and independence

Exactly seven comparison bases under four separate variants and four closure
bases under four separate variants. Inputs, order, orientation and named
controls are specified in the preceding design and fixtures.py. No random
sampling, continuous optimizer, geometry simulation or physical calibration.
The no-half distance convention is D_C=min_R dis(R). Input kernels have
source rows, target columns; no Q/G-to-distance inference is made.

primary.py enumerates all relation bitmasks and explicit strict-order paths.
reference.py independently uses nonempty row-neighborhood products and a
topological max-plus recurrence. Neither imports the other's code. Shared
fixture inputs and serialization do not share mathematical implementation.
Full native results must agree with exact type distinctions retained.

## Native mathematical API

Both engines export inspect_kernel(d), relation_record(d,e,members),
compare(d,e), and closure(order,w). They use only standard-library imports.
Input matrices use exact native list/tuple containers and square rows,
n=1..3. Container subclasses are rejected, including relation containers
and their pairs. Every kernel/weight entry
must have exact type fractions.Fraction, be nonnegative, have numerator and
denominator at most 128 bits, and have zero diagonal. No coercion of bool,
int, float, string or Fraction subclasses. Outputs use dictionaries and
lists only, with exact Fraction/int/bool/str/None leaves. Inputs are not mutated.

Malformed container/value types raise TypeError; invalid shape, size, range,
order or relation structure raises ValueError. The order is a square matrix
of exact bool, of the same size as w, irreflexive and transitive. Positive
weights outside the supplied order are rejected; off-order zeros are not
traversable. Kernels failing causal admissibility are reported, not rejected.
For multiply invalid inputs the first reported defect may differ by engine;
no identical precedence is promised. The 128-bit cap applies to inputs,
not exact derived values: a closure endpoint may require 129 bits.

inspect_kernel returns exactly:

- n, kernel, diameter, support (bool matrix), strict_support (bool),
  conditional_residuals (lexicographic [i,j,k,dik-dij-djk] rows for positive
  dij,djk), causal_valid (strict support and nonnegative such residuals);
- gamma (full profile-distance matrix), gap (minimum off-diagonal gamma,
  None for singleton), twins (sorted classes, smallest representatives first),
  quotient (kernel on these representatives), distinguishes (all singleton).

relation_record requires a list/tuple of distinct two-index list/tuple
members, exact int indices in range, onto both inputs. It sorts members
lexicographically. Its output is {members, raw, normalized}. raw is
{errors, maximum, argmax}, retaining the full ordered member-pair error
matrix and all [row,column] attaining indices in row-major order. normalized
has the same structure after independent diameter normalization, or None
if either diameter is zero.

compare returns exactly {x,y,relations,raw_distance,normalized_distance,
raw_minimizers,normalized_minimizers,bijections,raw_bijection_distance,
normalized_bijection_distance,raw_bijection_minimizers,
normalized_bijection_minimizers,bitmask_universe,safe_gap}. x,y are inspections;
relations is sorted lexicographically by its complete members tuple. Every
minimizer/bijection list holds indices into relations. Bijections and their
minimizers/distances are None for unequal cardinalities, not an empty list.
Normalized quantities/minimizers are None if normalization is unavailable.
bitmask_universe=2**(len(d)*len(e)); it counts the primary candidate universe,
not actual reference enumeration work. safe_gap is true iff 2*raw_distance
is strictly below every nonsingleton gap; singleton gaps are unbounded.

closure returns exactly {order,weights,covers,paths,closure,cover_closure,
maximizers,cover_maximizers,input_support,closure_support,
positive_reachability,input_residuals,residuals,covers_positive}.
Matrices retain every diagonal/off-order zero. paths holds ALL strict-order
paths with at least one edge, sorted lexicographically by node tuple; each
is {nodes,weights,sum,cover_only}. maximizers and cover_maximizers hold one
{pair:[i,j],paths:[indices into paths]} per comparable pair in row-major
order, retaining all attaining paths, including zero-sum paths.
input_residuals and residuals are all [i,j,k,hik-hij-hjk] for i≺j≺k, sorted
lexicographically. input_support and closure_support are positive bool
matrices; positive_reachability is the transitive closure of input_support.
covers_positive is true when every cover weight is positive (vacuously true
for a singleton). No order is inferred from numeric zeros.

## Fixture and report contract

fixtures.py exports comparison_cases(), closure_cases(), controls(), and
EXPECTED_CENSUS. No mathematical engines are imported there. Every comparison
case is {id,base,variant,x,y,x_map,y_map,scale}, and every closure case is
{id,base,variant,order,weights,map,scale}. Maps explicitly give old→new labels;
inverse maps are recoverable and retained by the study driver. Named variants
are identity, cyclic, reversal and rescale. Reversal transposes both kernels
or both order and weights; rescale multiplies weights/kernels by 3/2 without
composing another transformation. Identical named rows are not deduplicated.

The native report is {schema,comparison_rows,closure_rows,controls,census}.
Each row retains the full input case, inverse maps, and the common exact
engine result after type-strict route agreement. Both complete outputs are
compared before only one is serialized, avoiding duplicate evidence bytes.
Controls retain their inputs, exact outputs, fixed witnessing relations or
residuals and checks. Runtime/timing information stays outside the report.

The prospective comparison census is 28 rows,132 input nodes,332 input
square cells,4,752 candidate bitmasks,2,380 onto relations,12,576 relation
members,69,976 raw discrepancy cells,69,960 normalized discrepancy cells
and 64 bijection records. Closure:16 rows,40 nodes,112 square cells and
36 comparable slots. These are bounded exact occurrences, not statistical
sample sizes. All input and output zeros remain represented.

## Evidence contract and stopping rules

Nine sources are bound: this README, fixtures.py, primary.py, reference.py,
study.py, test_calculus.py, test_evidence.py, and the two preceding design
Markdown files. No unbound local executable helpers. Read source files as
bounded regular nonsymlink files; verify exact source hashes before engine
loading and again after a run. Execute authenticated bytes, not a later
unchecked re-read. Preserve the first capture; replay never overwrites it.

Source cap 262,144 bytes each; artifact cap 16,777,216 bytes each; each study
run capped at 30 seconds and each complete unittest suite at 60 seconds.
Caps are enforced with process alarms as well as final elapsed checks.
All resources and test inventory are settled before freeze. A mismatch,
resource failure or mathematical source defect after first execution closes
this gate unsuccessfully: retain evidence and propose a new repair gate.
No post-execution source editing or fixture tuning in this gate.

The freeze stores exact sources and runtime metadata. JSON is canonical
UTF-8: sorted string keys, compact separators, ensure_ascii=False,
allow_nan=False and exactly one trailing newline. Native Fractions become
{"fraction":[numerator,denominator]}; exact ints/bools remain distinct.
Duplicate JSON keys, noncanonical bytes, nonfinite values, unrecognized
schemas and altered capture/source bindings are rejected. Capture contains
{schema,freeze_sha256,sources,report}. Report equality is type-strict, not
merely Python equality between bool and int. Every retained rational is
tagged, including integral-valued Fractions.

The metadata/wire validator checks bindings and canonical tagged rationals;
full nested mathematical equality is checked by the replay and test oracle,
not inferred from successful JSON parsing. Each route receives its own deep
copy of the input, and mutation is rejected. Capture/replay pin one source
snapshot before loading and recheck it afterward. Publication is read back;
an existing capture prevents a new freeze as well as a new capture.

## Pre-execution resource review

The two discrepancy channels contain 139,936 cells in total. For these fixed
inputs a serialized rational tag needs at most 24 bytes, including a cell
separator. Even allowing every cell to attain its maximum adds under one
million bytes of argmax index pairs. Relation wrappers, member lists, array
delimiters, kernel inspections, closure records and the small fixed controls
leave a conservative total estimate below 8 MiB, within the 16 MiB cap.
This is a schema/count estimate, not a captured byte count. Engine relations
have at most nine members and closure paths at most three nodes; there is
no unbounded search or matrix dimension in this gate. Wall-clock caps still
apply, and a resource failure must be retained as failure.

## Exact entry points and fixed inventory

From this directory, use the following sequence. The `freeze` command is
metadata-only; `capture` is the first mathematical execution. `tests` loads
authenticated test bytes, binds the authenticated driver for their imports,
checks all 39 tests and enforces the combined 60-second suite deadline.
Fail-fast execution stops on any test error/failure, including a deadline;
the suite rechecks its original capture bytes and source bindings at the end.
No repository-wide test discovery or old mathematical replay is included.

```text
python3 study.py freeze
python3 study.py capture
python3 study.py tests
python3 -O study.py tests
python3 study.py replay
python3 -O study.py replay
python3.11 study.py replay
python3 study.py sources
```

Exactly three dedicated complete replays are required, one using Python 3.11.
Normal/optimized suites also compare a full report to the saved capture;
these are reported as suite verification, not additional dedicated replay
commands. Before freeze, AST parsing and formatting/lint may inspect sources
but must not import engines, build fixtures or run the mathematical tests.

The 22 mathematical/API test methods are:

```text
test_complete_native_comparison_oracle
test_complete_report_schema_and_retained_named_controls
test_complete_native_closure_oracle
test_fixed_census_and_cardinality_polynomials
test_seven_analytical_optima_and_scale_bounds
test_analytical_gamma_twins_quotient_and_causal_anchors
test_every_relation_transport_reversal_and_rescaling
test_named_correspondence_beats_every_bijection
test_all_retained_fiber_bounds_and_safe_gap_minimizers
test_named_zero_leg_cover_only_and_idempotence_controls
test_all_closure_paths_transport_and_zero_sum_ties
test_safe_gap_and_zero_distance_quotient_controls
test_named_triangle_composition_symmetry_and_strict_gap_boundary
test_named_one_sided_fit_witness_and_paired_list_scale_factor
test_named_full_supremum_trim_and_sharp_lipschitz
test_pure_api_tuple_inputs_sorted_members_and_fresh_outputs
test_shared_zero_rows_accepted_without_aliasing_caller
test_native_type_refusals
test_shape_range_diagonal_and_relation_refusals
test_invalid_causal_kernels_reported_not_repaired_or_rejected
test_order_and_off_order_zero_boundaries
test_inclusive_128_bit_inputs_and_exact_large_derived_output
```

The 17 evidence test methods are:

```text
test_01_nine_source_bindings
test_02_canonical_capture_and_size
test_03_native_type_distinctions
test_04_noncanonical_duplicate_and_nonfinite_json
test_05_changed_source_rejected_before_loading
test_06_symlink_and_oversize_source_rejected
test_07_malformed_freeze_and_typed_binding_rejected
test_08_capture_binding_and_schema_rejections
test_09_capture_is_write_once
test_10_artifact_byte_caps
test_11_alarm_and_elapsed_caps
test_12_full_native_report_matches_saved_capture
test_13_route_mismatch_rejected_type_strictly
test_14_original_evidence_unchanged
test_15_malformed_rational_tags_rejected
test_16_snapshot_change_rejected_before_execution
test_17_publication_readback_and_existing_capture_guard
```

The cardinality-stratified combination oracle and permutation-of-node-path
oracle are independent of both engine traversals. Fixed analytical tables
anchor distances, profile gaps and endpoint closures. Additional API controls
are singleton/self-comparison, antichain/shared-zero rows, tuple/sorted-member
acceptance, nonaliasing, exact 128-bit endpoints, malformed inputs and invalid
causal kernels. These are not extra study rows or empirical cases. Tampered
files and mocked publication failures exist only in disposable test copies;
the actual frozen sources and first capture are never edited by the tests.

The first successful capture, both suite outcomes, three replay outcomes and
static review are recorded in verification.json and RESULTS.md afterward.
These outcome artifacts and the live roadmap are not retrospective inputs
to the mathematical source freeze. They must not change the preceding design.
