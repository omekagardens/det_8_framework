# RI98 source-only schema and authoring interface

This is an unexecuted implementation of accepted RI97. No actual numerical
operand has been decoded. The separately authored validator is now assigned
and written; complete peer source reviews passed, while root acceptance remains
pending. Exact reviewed identities are retained in the source-only handoff. Root owns source acceptance,
future qualification freeze, execution and publication.

`consumer.py` is standard-library only and has no import-time I/O or CLI.
The actual entry is `run_saved(ri96_body: bytes, provenance: dict) -> dict`.
It binds the exact 41,673,703-byte RI96 identity before JSON decoding, makes
the fixed projection below, then invokes the fixed production computation.
It rechecks the immutable input identity afterward. External caller custody
and runtime/source admission are separate required premises, never inferred
from producer booleans.

The pure qualification entry is
`build_result(projection, provenance, *, phase='fabricated_qualification')`.
It accepts only production shapes; tiny fixtures use `derive_modes` and
`derive_scenario` directly in declared size/row domains. Fabricated projection
bytes and context are conspicuously distinct from actual accepted RI96 bytes.
There is no fabricated RI93/96 execution receipt.

Expected independent API:
`validate_result(report, projection, expected_provenance, *, expected_phase)`;
`load_result(body, projection, expected_provenance, *, expected_phase)`;
`validate_saved(report, ri96_body, expected_provenance)`.
For every tiny declared positive,
`validate_case(row_proofs, held_scenario, mode_terms, result_scenario, *, size)`
runs the same independent reconstruction and returns status
all_fields_independently_match, rows=len(row_proofs), modes=size//2, scenarios=1.
The validator must independently decode/admit its projection, regenerate all
mode terms using the product-of-magnitudes expression, derive every scalar
field and compare the complete closed result. No consumer import. It inherits
the accepted transform certificate and does not execute a new FFT.

## Encodings and fixed objects

Plain integer metadata excludes booleans/floats. Exact rational is a two-item
list of canonical lowercase signed-hex numerator and positive-hex denominator,
reduced by gcd; integer zero is `0`, not `-0`. The inherited262144-bit gate
checks decoded/explicit integers and the numerator/denominator of each guarded
completed Fraction operation. It does not promise that Python's internal
temporary products or allocations never exceed that size. Existing checked
operation boundaries remain unchanged; no new arithmetic/rejection domain is
introduced. Floats occur only as canonical `float.hex`
strings inside pinned original little-endian binary64 PSD records.
Q=2^256, M=16384, fs=4096, dimensions/rows/scenarios exactly RI97.
No arithmetic tolerance. Closed JSON rejects duplicate keys and nonfinite
JSON literals. Canonical output is sort_keys=True, indent=2, ensure_ascii=True,
allow_nan=False followed by one LF.

Complete production `projection` keys:
`context`, `held_identity`, `rows`, `row_proofs`, `scenarios`,
`held_provenance_identity`, `held_limitations`.

- context: `accepted_ri96_saved_output` or
  `fabricated_projection_not_observed`.
- held_identity: actual complete RI96 pin, or canonical fabricated fixture
  operand tag pin chosen independently of this projection; it is not an
  assertion that a fake predecessor ran.
- rows: the exact eight production row integers.
- row_proofs: eight objects, keys `row`, `alpha`, `midpoint_modes`,
  `mode_identity`. Each midpoint_modes is 8193 lists of four canonical Q256
  endpoint integers [re_lo,re_hi,im_lo,im_hi]; mode_identity pins its complete
  canonical JSON representation. Alpha is a nonnegative exact rational.
  Both endpoint imaginary rectangles must contain zero. True DC action is
  omitted; no midpoint DC real value is changed or rechecked as a transform.
- scenarios: four objects in fixed order. Keys `id`, `source_record`,
  `band_extrema`, `C_minus`, `C_plus`, `delta_minus`, `delta_plus`, `trace`,
  `prior_trace`. source_record has exactly dtype='<f8', integer shape=[8193],
  values_hex, sha256 over the original little-endian array bytes. Full DC and
  Nyquist entries remain retained. band_extrema retains index, ell, u,
  minimum_indices, maximum_indices for each fixed band. C matrices are 8x8
  exact reduced rationals. deltas are nonnegative rationals, trace and
  prior_trace are closed two-rational intervals; prior_trace must be contained
  in trace. These are inherited valid band/global enclosures, not newly
  reconstructed cross-coordinate covariance matrices.
- held_provenance_identity: canonical pin of original RI96 provenance, or
  canonical pin of the explicit fabricated marker.
- held_limitations: original RI96 literal string list; fabricated uses only
  `Fabricated RI98 projection; no observed input or predecessor execution.`

Actual projection is taken only after whole body authentication from RI96
row_proofs; scenario `prior_trace` is `scalar_intersections.trace`, and all
other named scenario keys are retained verbatim. No original intervals or
other actual report is a new numerical operand.

`provenance` keys: `sources`, `input`, `acceptance`, `runtime`.
sources keys: design, consumer, validator, qualifier, implementation (pins).
input is actual RI96 body pin in actual phase, canonical projection pin in
fabricated phase. acceptance keys: design, ri96, qualification, custody;
design and ri96 are fixed accepted root records; qualification and custody
are null in fabricated phase, nonnull pins in actual phase. runtime keys:
fingerprint, inventory, interpreter (full qualified record identities).
The caller validates actual contents/closure of these records separately.

## Complete result

Top keys are exactly `schema`, `phase`, `status`, `method`, `provenance`,
`mode_terms`, `scenarios`, `checks`, `inherited_premises`, `limitations`.
schema=`ri98-mode-weighted-trace-v1`, status=`all_declared_checks_passed`;
phase is fabricated_qualification or fixed_saved_application.
Method and limitations are exact fixed literals in consumer.py; the validator
copies those literals independently after source review.

mode_terms is exactly8192 objects, each keys k, pair_weight, c, h_tau, h_alpha,
in increasing k. h=h_tau+h_alpha. All three scalar terms are nonnegative.

Scenario keys are exactly:
`id`, `source_identity`, `center`, `error_tau`, `error_alpha`, `error`,
`raw`, `ri96_raw_band`, `ri96_prior`, `final`, `band_spread`, `band_margin`,
`band_width`, `widths`, `equalities`, `ratios`, `direct_upper_le_band_upper`.
widths keys raw,ri96,final. equalities keys final_equals_ri96,final_equals_raw.
ratios keys ri96_over_final_width,ri96_over_raw_width,raw_upper_over_lower,
ri96_upper_over_lower,final_upper_over_lower. Each ratio has exactly value
and undefined_reason; value is a rational or null. Reason is null if defined,
otherwise zero_width_denominator or nonpositive_lower_endpoint as applicable.
PSD source_identity pins the complete canonical source_record; the original
PSD is retained once in the admitted projection, not duplicated in output.

checks keys inventory,counts,results. Inventory is the fixed GATES tuple;
counts has plain integers total=passed=len(GATES),failed=0; each result has id
and plain boolean passed. Conditional mathematical containment is not an
observed physical gate. inherited_premises keys labels,projection_identity,
held_provenance_identity,held_limitations, with fixed labels and exact copies.

## Qualification and controls

Q1–Q11 are the exact cases frozen in RI97, not new transforms. Tiny kernel
domains are (M,rows)=(4,1),(4,2),(8,1),(8,8) and production (16384,8), all
with fs4096; production build_result has no size parameter. The M4 divisor2
and alpha construction are fixture declarations. The full production zero
projection, canonical result/reload and separately authored validation must
be retained. Actual input parsing remains uncalled during qualification.
Exact case encodings, artifact names and intended refusal inventory are
literal in qualify.py and reconciled in IMPLEMENTATION.md before source
handoff. No successful QUALIFICATION record is created during authoring.

Consumer errors have `.code` in SCHEMA,EXACT,RESOURCE,INPUT,SOURCE,PHASE,
PROVENANCE,DOMAIN,ROW,MODE,INTERVAL,ALPHA,PSD,BAND,ENVELOPE,CANONICAL.
Independent validator additionally uses RESULT for a derived-field mismatch;
specific structural/admission failures retain their corresponding code.
No proposed caller, freeze or source authorization is created here.
