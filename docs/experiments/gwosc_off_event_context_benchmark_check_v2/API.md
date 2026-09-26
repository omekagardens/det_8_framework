# RI113 — v2 predecessor-header compatibility protocol

Source-only repair packet, 26 September 2026 UTC. No new source qualification or
observed execution is claimed. The inherited RI106 structural protocol follows
verbatim below this addendum; its historical preparation language concerns RI106.
The inherited numerical protocol and its scientific limitations are unchanged.

## Exact predecessor header

The RI100 result admitted by both observed wrappers remains exactly 8,844,567
bytes, SHA256 `37dc6865be52e6888bcf325022a18cef65e5b3dd8bf1ba2a9f287e1c12d929dc`.
The accepted prior has schema `ri98-mode-weighted-trace-v1`, phase
`fixed_saved_application`, status **only** `all_declared_checks_passed` and eleven
checks. The receiving benchmark retains schema `ri104-observed-context-benchmark-v1`,
phase `fixed_observed_application`, status `all_gates_passed` and twelve gates.

Primary `check_ri100_header(value)` and separate validator
`verify_ri100_header(value)` take a plain dictionary, require string keys and the
three exact string-valued prior fields, and return `None` on success. Other
full-result fields may be present; these helpers do not validate a closed full
report, numerical scenarios, provenance, body identity or execution custody.
Missing fields or non-mapping/non-string values refuse deliberately. Primary
schema/mapping errors use `INPUT`, phase errors `PHASE`, status errors `TRACE`;
all validator header errors use its existing `INPUT` category.

The actual wrappers call their own production helper only after unchanged full
input-byte admission and JSON parse, before scenario projection. The primary
keeps the separate RI83 schema check. No helper success replaces complete input
pins, projection/provenance validation, actual input custody or full arithmetic.
`all_gates_passed` is never an accepted RI100 status alias.

## Metadata-only qualifier

`interface_qualify.qualify_interface(primary, validator)` receives already captured
module objects from a separately admitted caller. It imports neither scientific
module and performs no file, HDF5, subprocess or numerical input access. The only
calls into those modules are their two production header helpers. It runs exactly
one positive vector plus ten named refusals on each implementation, in primary
then validator order. It rejects unexpected exceptions, wrong typed error/code,
missing refusal, non-None positive return and input mutation. No assertion is an
acceptance gate. Failure raises `InterfaceQualificationError`; no successful
report is returned from a failed inventory.

| Vector | Change from the exact three-field prior header | Primary code | Validator code |
|---|---|---|---|
| H00:accepted_header_contract | none | success/None | success/None |
| H01:legacy_status | status=`all_gates_passed` | TRACE | INPUT |
| H02:unknown_status | status=`success_unchecked` | TRACE | INPUT |
| H03:fabricated_prior_phase | phase=`fabricated_qualification` | PHASE | INPUT |
| H04:receiving_phase_substitution | phase=`fixed_observed_application` | PHASE | INPUT |
| H05:older_predecessor_schema | schema=`ri93-frequency-band-proxy-v1` | INPUT | INPUT |
| H06:missing_status | remove status | TRACE | INPUT |
| H07:missing_phase | remove phase | PHASE | INPUT |
| H08:missing_schema | remove schema | INPUT | INPUT |
| H09:nonstring_status | status=true | TRACE | INPUT |
| H10:nonmapping_header | null replaces mapping | INPUT | INPUT |

The closed returned report has keys `schema,phase,status,scope,counts,inventory,
results,limitations`. Schema is `ri113-fabricated-interface-qualification-v1`;
phase is `fabricated_interface_qualification`; successful status is
`all_header_contract_checks_passed`; scope is
`fixed_RI100_header_contract_only_no_observed_or_scientific_execution`.
Counts are plain integers `{implementations:2,positive:2,refusals:20,helper_calls:22}`.
The inventory is exactly `primary:` followed by the eleven IDs above, then
`validator:` followed by the same eleven IDs. Each result has keys
`id,implementation,helper,input,expected,actual,passed`. Expected keys are
`outcome,code`; actual adds `error_class`. Outcome is `header_only_pass` or
`refusal`; successful positives have null code/error_class. Refusals name the
actual `ContextError` or `ValidationError` class and its expected code. `passed`
is a plain true boolean. Inputs are retained as the complete fabricated vectors.
Limitations are the fixed complete list in the qualifier.

The caller must retain the entire canonical report (ASCII sorted keys, indent2,
no NaN, terminal newline), genuine completion, and exact source/runtime/admission
bindings. The report deliberately contains no invented observed result or source
acceptance. Caller custody is external, so none of these source-known strings or
input vectors is supplied with a real observed body identity. A helper pass is
only a protocol check and cannot authorize an observed attempt.

The optional wrapper refusal mentioned in the accepted design is not implemented
or counted. No actual projection wrapper is called by this qualifier. Legacy
`qualify.py` is copied byte-for-byte for any separately admitted full fabricated
qualification; its original inventory and phase remain unchanged. Its inclusion
is availability, not a claim that it has executed against these new source bytes.

## Source and evidence boundaries

This v2 packet has six files: `consumer.py`, `validate.py`, `qualify.py`,
`interface_qualify.py`, `API.md`, `IMPLEMENTATION.md`. Scientific result provenance
continues to use its original six source keys, including `qualifier` for the
historical full `qualify.py`. The new metadata-only `interface_qualify.py` belongs
to the outer caller's complete source closure and its distinct qualification
record; adding it does not change the scientific result schema or pretend that
its two helpers validate interval arithmetic.

The primary and endpoint validator retain separate arithmetic. Their new header
helpers use their respective guard machinery and do not import/call each other.
Both narrow repairs and the new interface qualifier have one RI113 author; this
is not a claim of independent authorship for that interface layer. Independent
complete source review remains required before any target execution.

RI108 qualifies its original executed source bytes and fixed fabricated path.
RI110 failed before benchmark construction; its failed attempt is immutable.
Root must separately accept new source, qualification/applicability and concrete
caller custody before issuing any fresh observed admission. All numerical and
resource thresholds, protected-validation prerequisites and RET pause remain.

---

# RI106 shared structural contract — source preparation

This file specifies record structure, not shared arithmetic. The accepted RI104
scientifically unchanged published32,152-byte design remains fixed. No source is executed by this preparation.
Primary consumer: midpoint/radius integer contractions. Separate validator:
signed endpoint contractions and independently decoded source rows.

## Entry points and boundaries

Primary `build_result(raw_bodies, capture_path, projection, provenance,
artifact_dir, *, phase='fabricated_qualification')` returns the complete report,
writing exactly the six exclusive application artifacts. `raw_bodies` is a
closed H1/L1 dict of bytes, each 131072 little-endian binary64 values.
`capture_path` points to a complete fixed-format RI73 capture, synthetic in
qualification. `projection` is the complete closed input projection below.
Neither this function nor imports open observed HDF5 or predecessor files.

Primary `run_observed(hdf_bodies, capture_path, ri83_body, ri100_body,
metadata_body, provenance, artifact_dir, inspector)` first checks both complete
HDF5 bodies, capture file, RI83/100 and metadata bodies against actual fixed
pins, before either HDF5 parse or predecessor numerical decode. It then replays
captured inspector `_inspect` on each same HDF5 byte object and compares the
complete accepted RI37 report. Lazy h5py reads extract each full float64 vector,
shape131072, exporting exact `<f8` bytes. It builds the actual projection from
the pinned reports and calls build_result in `fixed_observed_application`.
Inspector/NumPy/h5py source/runtime are admitted by the future outer caller;
no ambient project imports are permitted. No executable caller is written now.

Separate validator APIs: `validate_result(report, raw_bodies, capture_path,
projection, provenance, artifact_dir, *, expected_phase)` independently streams
capture, derives all results, and validates the six artifacts; returns
`{'status':'all_fields_independently_match','windows':26,'raw':208,
'short_long':416,'mean':32,'centered':208,'scenarios':4,'artifacts':6}`.
`load_result(body)` strictly parses duplicate-free canonical JSON and returns
its object (arithmetic validation remains explicit).
`validate_observed(report,hdf_bodies,capture_path,ri83_body,ri100_body,
metadata_body,provenance,artifact_dir,inspector)` independently binds all bodies
before parse, re-extracts both COMPLETE arrays, derives the actual projection
and calls validate_result; cannot merely trust segment hashes because those
omit the exclusion/tail. Lazy HDF5 import occurs only in this actual function.

Public arithmetic guard APIs for tiny qualification: primary `dot_box(lo,hi,v,
*, enforce_width=True)` accepts equal-length sequences of exact Fractions and
returns the dot record below WITHOUT `row`; primary `square(interval)`,
`energy(raw_dots,mean_dot,centered_dots)` return exact encoded records below.
Tiny exact domain is1 or3 coordinates,1 or2 rows,2 or3 windows; full production
entry stays exact fixed dimensions. Separate validator may expose
`verify_dot(record,lo,hi,v,*,enforce_width=True)`, `verify_square(record,interval)`
and `verify_energy(record,raw_dots,mean_dot,centered_dots)` using its own endpoint
arithmetic. Full validator must use these same arithmetic guards or underlying
reconstruction, not a fixture-only alternative. Late schema guards may be
exposed to avoid rerunning every production contraction for a mutation.

## Encodings and constants

Canonical JSON: ASCII, sorted keys, indent2, allow_nan=False, terminal newline.
Scalar rational `[signed_hex_numerator,positive_hex_denominator]` is reduced,
canonical, no0-prefix/negativezero; interval is `[scalar_lo,scalar_hi]`.
Plain int/bool types are distinct. BITS262144 guards all admitted integers and
completed explicitly guarded integer/Fraction operations, not hidden Python
transient products. Fixed full dimensions N2769,L4096,T10961,M16384,fs4096,
raw131072; rows[0,1,27,805,1384,2741,2767,2768]; four scenarios H1:left,H1:right,
L1:left,L1:right; starts exactlyRI104; no new scientific modes or parameters.

Errors use `.code`. Shared intended categories: SCHEMA,EXACT,RESOURCE,PHASE,
SOURCE,INPUT,METADATA,FLAGS,DOMAIN,ROW,INTERVAL,DOT,WIDTH,CENTER,ENERGY,TRACE,
ARTIFACT,CANONICAL,RESULT,PROVENANCE. An API mistake must be repaired before
frozen qualification, never reclassified after a run.

## Projection and provenance

Projection keys exactly `context,metadata,hdf5,capture,ri83,ri100,segments,traces`.
Context is `fabricated_inputs_not_observed` or `accepted_fixed_observed_inputs`.
metadata is the complete pinned accepted RI37 report (contains only structural,
flag, finite/missing-count information; no strain values). Qualification may
use this source-known metadata explicitly without impersonating observed data.
hdf5 is closed dict H1/L1 of pins. capture,ri83,ri100 are pins. Each pin has
plain int bytes>0 and lowercase SHA25664. Fabricated hdf5/capture/ri83/ri100 pins
must differ from actual pins. Segments are the ordered26 records
`{id,detector,side,start,end,raw_sha256}` with id `H1:left:0`, etc.
Traces are four `{id,interval,source_identity,model,units}` records. Actual
interval and source_identity are exactly the accepted RI100 scenario `final`
and `source_identity`; model `postulated_finite_circulant_from_empirical_psd`,
units `nominal_strain_squared_sum_of_eight_centered_coordinates`.
Fabricated traces have the same fields but model `fabricated_trace_not_observed`.
No actual comparison is a magnitude gate. Full projected body identity is bound.

Provenance keys exactly `sources,input,acceptance,runtime`:
- sources closed keys design,consumer,validator,qualifier,implementation,api;
  each pin; design is published RI104 cd7a585f.../32152 (only measurement-plan link differs from accepted32200-byte draft).
- input is canonical projection pin.
- acceptance closed design,ri100,qualification,custody; firsttwo fixed root
  accepted pins. qualification/custody are null in fabrication, pins in actual.
- runtime closed fingerprint,inventory,interpreter, allpins. These are genuine
  captured runtime identities, never fabricated version labels. Outer execution
  enforces them and complete source closure; inner module validates fields.
There is no claimed qualification/actual custody success at source-only stage.

## Closed scientific result

Topkeys exactly schema,phase,status,method,provenance,inputs,operator,scenarios,
checks,limitations. schema `ri104-observed-context-benchmark-v1`; phase exactly
fabricated_qualification/fixed_observed_application; status `all_gates_passed`.
Method and limitations are complete fixed literals to be pinned in consumer.py,
independently replicated by validator after source review. Method will include
accepteddesign/dimensions/rows/starts/crop/no-preprocess/exact arithmetic/width
1/10^12/n-divisor/square/units/no-magnitude-test/bitlimit. No conditional omission.

inputs keys exactly `projection,artifacts`. Projection is retained complete.
Artifacts sorted by name exactly H1-left-mean.json,H1-raw.f64le,H1-right-mean.json,
L1-left-mean.json,L1-raw.f64le,L1-right-mean.json. Each inventory row keys
`name,bytes,sha256,dtype,shape`. Raw dtype`<f8`,shape[131072],bytes1048576;
mean dtype`reduced_hex_rational`,shape[10961]. Means files are canonical JSON
objects `{schema:'ri106-coordinatewise-mean-v1',id:'H1:left',values:[scalars...]}`.
Artifact directory contains exactly these6 regular nonsymlink nlink1 files,
no nested nodes, outputs exclusively created/fsynced. Full HDF5/capture input
snapshots are external input closure, not counted as output artifacts.

operator keys exactly `capture,schema,dimensions,row_order,rows,
constant_annihilation`. dimensions exactly{N:2769,L:4096,T:10961}; schema
ri73-reconstructed-intervals-v1; constant_annihilation
`accepted_true_A_annihilation_midpoints_not_projected` in actual and
`fabricated_row_fixture_not_observed` in fabricated. Row records exact keys
`row,short_count,long_count,source_row_pin,a_midpoint_sum,a_radius_sum,
a_row_sum_interval,contains_zero`. source_row_pin is the exact compact canonical
captured row bytes excluding delimiter; counts2769/10961. Row sum interval must
contain0, but midpoint sum need not be0. All8 rows in fixedorder; exhaustion
must reject every ninth item including None. Capture64MiB and row8MiB ceilings.

scenarios exact ordered4 records, each keys `id,detector,side,count,windows,
mean,centered,energy,trace`. Trace is corresponding projected record unchanged.
Window record keys `start,slices,raw_sha256,outputs`; slices closed M,T,short.
Each slice record keys `start,end,gps_start_offset,gps_end_offset,flag_rows,
dq_masks,injection_masks`. GPS offsets are reduced rational seconds relative
to1126259446; indices are integer. flags cover floor(start/fs)..ceil(end/fs)-1.
Output record keys `row,short,long,delta,route_intersection`; short/long and
intersection are interval encodings; delta is dot record including row.
Each fixed selected output's exact absolute sample index is
window.slices.short.start + row, recoverable without another floating clock.
No raw output coordinate omitted: field `output_indices` will NOT be added;
this formula is part of literal method, all8 rows retained explicitly.

Mean keys `artifact,outputs`, outputs8 dot records including row.
Centered is list of n records `{start,outputs}`, each outputs8 dot records.
Dot record keys `row,interval,center,radius,width,input_max,width_limit,
width_pass`; every value except row/bool is rational or interval. Tiny API omits
row. width_limit=input_max/10^12; zero input requires exact[0,0]; width_pass true
only when numerical gate passes. Wide primitive controls set enforce_width=False
and retain actual false width_pass, never claim full-result success.

Energy keys `components,U,M,V,identity_intersection`. Components8 records
`{row,raw_squares,mean_square,centered_squares,U,M,V,identity_intersection}`;
raw_squares/centered_squares ordered n intervals; mean_square interval. U and V
are n-divisor sums of their squares; M is mean_square. Sum8 components for total
U/M/V. Identity intersection is overlap of U and V+M, must exist, does not
replace primary intervals. Tiny primary energy API omits row and returns one
component's exact record; no component total hidden in that primitive.

checks keys `inventory,counts,results`. Fixed inventory:
admission:phase,admission:inputs,admission:metadata,admission:segments,
operator:complete,operator:constant_sum,scenario:H1:left,scenario:H1:right,
scenario:L1:left,scenario:L1:right,artifacts:complete,completion:stable.
counts {total:12,passed:12,failed:0}; results ordered12 `{id,passed:true}`.
Full numerical measured evidence is in all row/dot/energy records, not these
booleans. Separate validator completion belongs to external caller custody;
no self-referential future independent acceptance is inserted into report.

## Stage status

The concrete primary/qualifier and independent validator are being authored.
All future named fixture/refusal inventories and original/copy/runtime/caller
closure must be separately source-reviewed and frozen before any execution.
