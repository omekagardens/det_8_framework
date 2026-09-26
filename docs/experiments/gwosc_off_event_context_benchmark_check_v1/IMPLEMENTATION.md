# RI106 — fixed observed-context benchmark implementation

26 September 2026 UTC. **Source-only packet; no RI106 qualification or observed execution has occurred.**
This note completes the interrupted RI106 preparation for the accepted RI104 design.
It is not an execution authorization, root source acceptance, a runtime freeze,
or a completed scientific result. Original sources and the two review repairs
remain retained separately. No target was imported, compiled or executed while
writing this note; no numerical HDF5/capture/result body was decoded.

## Fixed design and exact source packet

The published design is
`/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_off_event_context_benchmark_v1/DESIGN.md`,
32152 bytes, SHA-256 `cd7a585f0002f1aef4d16bb96884c0a745291d41b33e73ff466567cbff5f2478`.
Its accepted source text differs from the original32200-byte note only in one
portable measurement-plan link. The accepted mathematics and experimental
conditions are unchanged. Root design adjudication remains10268 bytes,
`63b781b8a87c0ac86dfdf145ddf2b7073b71137eabd6c4778b5c8b10aabf8267`.

The complete application API/schema is `API.md`. Four source identities below
are frozen for review. The external `SOURCE_HANDOFF.json` records this note's
identity without a self-referential hash, all five packet files, published
design, review records, known history and prospective predecessor references.
A source handoff does not substitute for the later complete executable closure.

| File | Bytes | SHA-256 |
|---|---:|---|
| `API.md` | 11181 | `4ed999253bf865b68d8a722b0635893a5c44950250c8a94d01f51119b7e4d524` |
| `consumer.py` | 34964 | `8b13ace9bdc768cb77401b24458d199e249a9687e5d0fbf02108eb079aa5a4f7` |
| `validate.py` | 53383 | `00a2777378b94b7a2ff59cbef08eafc5dc6213fc5071017d6bbc590b5c3b4ce9` |
| `qualify.py` | 34582 | `b3ba3e9344d36447fbe7c3902fb92eb9c9efd8bdba7303dfe464ba5429a2a460` |

All imports and entry points must be captured from admitted source bytes by a
later caller. None of these modules imports another local implementation.
`consumer.py` and `validate.py` use standard-library exact arithmetic, byte,
JSON and path helpers; their HDF5 import is lazy inside the actual wrapper.
`qualify.py` receives primary and validator module objects and imports neither.
The actual wrappers additionally require the captured unchanged RI37 inspector,
h5py and its genuine qualified NumPy/HDF5 dependencies. Current static import
names are enumerated in the handoff; that list is not a full interpreter or
extension-library inventory and must not be used as a reduced runtime freeze.

## Exact computation and independent route

The fixed dimensions are fs4096, M16384, N2769, L4096, T10961 and131072 raw
binary64 samples per detector. Row order is0,1,27,805,1384,2741,2767,2768.
Each detector uses seven left and six right windows at the unchanged RI104
starts. T is the first10961 samples of each M window; the N center begins at
L4096. Output i has absolute index window start+4096+i. GPS offsets, partial
one-second flag coverage, raw M hashes, exclusion and unused tail stay explicit.

The operator is A=Q-P with P embedded only on[L,L+N); the accepted complete RI73
short/long interval rows supply the coefficients. The consumer's common integer
denominator contraction calculates c=sum(midpoint*x), e=sum(radius*abs(x)),
D=[c-e,c+e]. The validator independently parses the source and contracts signed
lower/upper endpoints with separate denominator lifting. It does not call or
import consumer arithmetic. Each raw contraction also retains signed P and Q
and intersects D with Q-P only as a consistency check. Primary endpoints remain
unchanged. Accepted true A annihilates constants, but midpoint rows are never
projected or renormalized; interval row sums must contain zero.

Raw binary64 values are exact dyadic inputs. A side's mean is coordinatewise
across that side's windows, with unequal fixed counts7 and6. Centered inputs
are computed exactly before applying A. Exact center linearity, mean interval
overlap and zero within the sum of centered intervals are checked. The same
uncertain coefficients serve every window: this is not independent interval
noise or subtraction of separately bounded outputs. The square map has zero
lower endpoint precisely when the interval crosses zero. U,M,V use divisor n;
all per-component square records and totals remain explicit. U intersects V+M
as a consistency identity; this does not tighten the reported intervals.

Every raw, mean and centered direct A interval must satisfy the unchanged
width <= maxabs(input)/10^12 threshold; zero input must produce[0,0]. There is
no small-output or empirical magnitude gate. Decoded and explicitly guarded
completed integer/Fraction operations retain262144-bit limits, not a promise
about hidden temporary allocation inside Python arithmetic. Rows are streamed
and released; no new filter, FFT, coefficient reconstruction or PSD fit occurs.

The full result has exactly the ten closed API sections and retains26 windows,
208 raw A intervals,416 P/Q intervals,32 mean A intervals,208 centered A intervals
and four separate scenarios. It writes exactly six application artifacts:
H1/L1 complete raw f64le arrays, each1048576 bytes, and four complete10961-value
canonical rational mean files. Original signed-zero raw bits are retained.
The independent validator reopens all six complete bodies, not just their pins;
it reconstructs every numerical and metadata field and rejects extra/missing
membership, changed bytes, symlinks and nonexclusive files.

These six artifacts are distinct from scientific RESULT/stdout, qualification
fixtures and external monitoring/custody receipts. Complete raw HDF5 snapshots
and the RI73 capture are input closure, not application output artifacts.

## Actual input boundaries

`run_observed` and `validate_observed` first bind both complete HDF5 bodies,
the complete capture, RI83 and RI100 bodies and the accepted full RI37 metadata
before any HDF5 parse or predecessor numerical decode. The same captured HDF5
bytes feed the complete unchanged inspector and full raw extraction. Both
wrappers independently reproduce the exact inspector report, complete sample
arrays and26 original M-segment hashes. No inverse-demeaning of the rounded
RI83 exports and no fallback acquisition is allowed. Capture parsing requires
all eight ordered rows, canonical reduced rational intervals, fixed framing,
EOF and ninth-item exhaustion, before/after complete identities and filesystem
state; limits remain8MiB per row and64MiB per capture.

Pure `build_result` and `validate_result` can receive fabricated raw arrays;
their `fixed_observed_application` phase is not sufficient evidence of actual
provenance. Only the separately admitted actual wrappers plus genuine outer
source/runtime/input custody establish that claim. The qualifier never opens
observed files or calls either actual wrapper. Its projection phase/pin refusal
is not represented as actual-wrapper execution coverage. A later actual caller
review must inspect and admit those byte-before-parse paths explicitly.

All four accepted RI100 trace intervals and source identities are carried
through unchanged. Side-centering gives a finite descriptive second moment,
not an unbiased covariance estimate: overlap and unknown means/cross-window
covariance remain. The same previously inspected windows supplied the proxy
PSDs, so the comparison is development evidence. Finite circulant covariance,
calibration including below10Hz, V2/C02, blank Yunits, and the clear retained L1
NO_CW_HW_INJ flag retain their qualifications. No physical waveform accuracy,
SNR, significance, held-out validation, native forward map or gravity result
follows. RET remains paused.

## Prospective qualification: closed cases and retained evidence

The entry is
`qualify.run(primary, validator, provenance_template, artifact_dir, metadata_body)`.
It requires an exclusively new canonical output directory and the complete
source-known RI37 structural metadata at its fixed pin. Primary/validator module
objects and genuine source/runtime provenance come from the future admitted
caller. The generated synthetic projection replaces only the provenance input
pin; qualification/custody acceptance fields remain null. No fictional runtime
fingerprint or future acceptance record may be supplied.

There are eleven positive groups:

1. Q1 labeled full131072-sample index arrays, excluded/tail sentinels,26 windows,
   78 slice records and208 output indices, exact first-T/means/centered inputs,
   all26 raw segment hashes and complete clocks/flags.
2. Q2 three-window and Q3 two-window A0 point cases, all two-component outputs,
   means, centered values, energies and independent hand-derived anchors.
3. Q4 zero, Q5 common exact constant, Q6 signed amplitude -1 and Q7 amplitude2,
   with exact output signs and quadratic energy scales.
4. Q8 all64 radius1/16 endpoint matrices on both side sets, non-corner center
   point cases, full output/mean/centered/energy containment and independent
   signed endpoint equality.
5. Q9 shared scalar coefficient[1,2], inputs1 and3, direct centered[-2,-1] and
   [1,2], V=[1,4], and the strictly wider separate-output subtraction reference.
6. Q10 complete production-shaped zero-result fixture, serialized/reloaded and
   independently validated over all counts/fields and all six real artifact bodies.
7. Q11 square endpoint cases: wholly negative/positive, crossing zero, zero and
   nonzero point intervals.

Wide Q8/Q9 boxes use the same exact primitives with width enforcement explicitly
false; their computed width-pass value is retained. They do not qualify as
successful full-path inputs. Q10 and all actual full paths retain the fixed
gate. Q10 is a fabricated zero operator and does not establish actual coefficient
custody or observed nonzero performance.

There are39 primary and35 validator refusals,74 total. Each must fail with its
exact first `.code`; unexpected acceptance, ordinary exception without that
code, or another code fails qualification. This is a prospective inventory,
not evidence any refusal has run. All guards are full-path guards or the same
underlying primitives. The complete ordered inventory follows.

| Refusal | First code |
|---|---|
| `P:duplicate_json` | `SCHEMA` |
| `P:nonfinite_json` | `EXACT` |
| `P:noncanonical_hex` | `EXACT` |
| `P:zero_denominator` | `EXACT` |
| `P:unreduced_rational` | `EXACT` |
| `P:integer_ceiling` | `RESOURCE` |
| `P:crossed_interval` | `INTERVAL` |
| `P:nonexact_dot_input` | `EXACT` |
| `P:dot_dimensions` | `DOMAIN` |
| `P:overwide_interval` | `WIDTH` |
| `P:raw_length` | `INPUT` |
| `P:raw_nonfinite` | `INPUT` |
| `P:missing_flags` | `FLAGS` |
| `P:false_L1_CW_flag` | `FLAGS` |
| `P:changed_metadata` | `METADATA` |
| `P:alternate_segment_start` | `INPUT` |
| `P:raw_segment_hash` | `INPUT` |
| `P:swapped_trace` | `TRACE` |
| `P:crossed_trace` | `INTERVAL` |
| `P:actual_phase_fabrication` | `PHASE` |
| `P:extra_projection_field` | `INPUT` |
| `P:changed_capture_pin` | `INPUT` |
| `P:changed_source_design` | `SOURCE` |
| `P:claimed_qualification` | `PHASE` |
| `P:changed_projection_binding` | `INPUT` |
| `P:extra_provenance_field` | `PROVENANCE` |
| `P:missing_source_row` | `ROW` |
| `P:wrong_row_order` | `ROW` |
| `P:wrong_row_length` | `ROW` |
| `P:duplicate_source_key` | `SCHEMA` |
| `P:noncanonical_source_row` | `CANONICAL` |
| `P:crossed_source_interval` | `INTERVAL` |
| `P:extra_ninth_source_row` | `ROW` |
| `P:missing_artifact_record` | `ARTIFACT` |
| `P:changed_artifact_pin` | `ARTIFACT` |
| `P:extra_artifact_record` | `ARTIFACT` |
| `P:wrong_artifact_name` | `ARTIFACT` |
| `P:unsupported_dot_size` | `DOMAIN` |
| `P:unsupported_energy_count` | `DOMAIN` |
| `V:extra_top_field` | `SCHEMA` |
| `V:wrong_phase` | `PHASE` |
| `V:changed_design` | `SOURCE` |
| `V:claimed_qualification` | `PHASE` |
| `V:wrong_input_identity` | `INPUT` |
| `V:relaxed_width_method` | `DOMAIN` |
| `V:n_minus_one_method` | `DOMAIN` |
| `V:scalar_temporal_centering` | `DOMAIN` |
| `V:false_status` | `RESULT` |
| `V:missing_gate` | `RESULT` |
| `V:false_gate` | `RESULT` |
| `V:float_gate_count` | `RESULT` |
| `V:changed_limitations` | `SCHEMA` |
| `V:wrong_signed_dot` | `DOT` |
| `V:wrong_dot_scale` | `DOT` |
| `V:wrong_square_lower` | `ENERGY` |
| `V:wrong_energy_divisor` | `ENERGY` |
| `V:missing_artifact_record` | `ARTIFACT` |
| `V:changed_artifact_pin` | `ARTIFACT` |
| `V:swapped_scenario_trace` | `TRACE` |
| `V:wrong_scenario_count` | `DOMAIN` |
| `V:duplicate_json` | `SCHEMA` |
| `V:noncanonical_result` | `CANONICAL` |
| `V:missing_source_row` | `ROW` |
| `V:wrong_row_order` | `ROW` |
| `V:wrong_row_length` | `ROW` |
| `V:duplicate_source_key` | `SCHEMA` |
| `V:noncanonical_source_row` | `CANONICAL` |
| `V:crossed_source_interval` | `INTERVAL` |
| `V:extra_ninth_source_row` | `SCHEMA` |
| `V:unsupported_dot_size` | `DOMAIN` |
| `V:unsupported_energy_count` | `DOMAIN` |
| `V:missing_mean_file` | `ARTIFACT` |
| `V:changed_artifact_body` | `ARTIFACT` |
| `V:alternate_T_crop` | `DOMAIN` |

The source-recovery repair preserves the old metadata-only artifact controls
under accurate names. New physical controls use fresh isolated fabricated
copies: one five-file directory omits H1-left-mean.json, while another six-file
directory replaces that mean file's terminal newline by a space with unchanged
size. Valid original inventory/expected bodies force the actual membership or
complete-byte guard to reject. The successful six application files are never
changed. Exact retained negative-file identities, difference and expected
inventory are included in refusal evidence. The new T-crop mutation changes
T=[0,10961) to[2711,13672) inside the first M window with consistent exact clock
and flags; the full scenario slice guard must reject DOMAIN. The existing
M-start control is accurately named alternate_segment_start.

The qualifier retains exactly33 files beneath its artifact directory:

| Group | Files |
|---|---:|
| Root evidence: BOX_CORNERS, DEPENDENCY_CASE, INDEX_H1/L1, INDEX_RECORDS, PROJECTION, RESULT, SYNTHETIC_CAPTURE, TINY_CASES | 9 |
| Successful application subdirectory: two complete raw arrays plus four exact means | 6 |
| Seven complete malformed synthetic coefficient captures | 7 |
| Physical missing-mean fixture: five unchanged copied files | 5 |
| Physical changed-body fixture: six copied files, one same-size changed body | 6 |

All33 bodies are exclusively created, fsynced, inventoried and retained. The
qualification return itself, captured stdout and external receipts are separate
outputs. Normal and optimized qualification must compare the entire canonical
return and every33 artifact bodies; mode-specific resource/custody evidence is
separate. The return's closed fields are schema,phase,status,provenance,scope,
counts,positive,refusal_inventory,refusals,artifacts,limitations. Its prospective
schema is ri106-fabricated-qualification-v1 and successful status is
all_fabricated_gates_passed; no such completed report exists from this source work.

## Qualified predecessors and required caller changes

The known reusable supervision reference is the actually qualified RI98 caller,
recorded by root adjudication4283 bytes/SHA-256
`312e023d13618f3343cbbbdd042656cf56a329e44a9768ed278da0042080aee9` at
`/Volumes/AI_DATA/development/det-review-evidence/ri98-qualification-root-ftbqnblc/RI98_ROOT_FINAL_QUALIFICATION_ADJUDICATION.json`.
Its preserved control/worker/launcher sources are in RI100 preparation's
`predecessor/ri98.*.py`; exact hashes are in the handoff. The completed RI100
application and saved-audit caller patterns supply actual-input custody and
saved-result validation precedents. Their source-only contracts and historical
handoffs remain historical records, not current authorization or evidence that
RI106 already ran. Accepted RI100 root adjudication remains7451 bytes,
`499fddd1a5315fb8c14c39ae8d161ab11e12f53f8f640d814b1ed81e2f780d21`.

A later bounded adapter must preserve the accepted captured-source loader,
supervisor, genuine exits, exclusive outputs and monitoring loop, with explicit
full-source/AST diffs and independent applicability review. Required deltas are
RI106 source/API/acceptance closure; the qualifier metadata-body argument;
11/39/35/74 counts and33 fixture-body retention; scientific ten-section schema;
and six detached actual application artifacts. The observed branch additionally
captures both raw HDF5 files, complete RI73 capture, RI83/RI100 bodies and full
RI37 inspector/metadata, admits them before parsing, and invokes the exact actual
wrappers and full independent validator. A saved arithmetic admission must bind
the successful observed modes and independently reopen raw/capture/input bodies
and all six outputs, not merely reuse producer success flags. No supervisor or
adapter source is implemented or issued by this packet.

The expected recovered runtime is CPython3.11.6, NumPy2.1.3, SciPy1.14.1,
h5py3.12.1 and HDF5 1.12.2. Those names are required compatibility metadata,
not fresh fingerprint evidence. The qualified interpreter locator is
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python`.
The future caller must freshly bind its complete symlink/target/build/runtime
inventory and captured dependencies, including the unchanged inspector. No
runtime probe, installation, dependency reduction or environment change occurred
here. All concrete paths/argv/cwd/environment/output nodes require a new reviewed
freeze; a historical command is not safe to replay merely because it is printed.

Keep180 child seconds,524288KiB sampled sole-child RSS,0.025s polling target,
0.1s maximum successful sample/final sample-to-reap gap and0.05s ps timeout.
This is sampled child RSS, not a hard OS cap or whole-process-tree accounting.
Runtime probe and complete validation inside the scientific child count toward
its budget. No source-only size or arithmetic estimate establishes runtime fit.
Preserve every raw attempt, sample, failure, partial output, genuine outer/child
exit and before/after source/runtime/input identity; never overwrite failed runs
or relax a threshold to obtain a pass.

Root must first accept the complete source packet and prospective concrete
qualification caller/closure. Then root alone issues normal admission; actual
completion, raw resource evidence and complete output custody are reviewed
before separately admitting optimized mode. Only accepted real two-mode
qualification permits preparation/review of actual observed custody and its
own separate serial admissions. Isolated -I -B flags and -O only for optimized,
one numerical worker, exact environment and complete identical scientific
outputs/artifacts remain mandatory. Fresh actual HDF5/capture custody and later
full independent saved arithmetic/custody review cannot be inferred from
qualification. These tasks are authorized programme follow-through, not a
request for user reapproval, and root retains execution/index ownership.

## Authorship, repairs and current remaining work

Original API/consumer/qualifier author was measurement_replay_review. The
separate validator author was runtime_recovery_audit. Their work was interrupted
before the implementation note and final source handoff. Early independent
review found the public tiny-domain mismatch; preserved source history records
the correction to dot sizes1/3/T and energy counts2/3/6/7. Recovery reviewer
ri106_recovery_review read the complete design/API/consumer/qualifier, then root
authorized only the named physical artifact and T-crop qualification repairs.
That reviewer authored this note and is not its own independent reviewer.
ri106_validator_recovery_review independently read the entire validator and
reviewed the exact qualifier repair and first guards. Final independent protocol
and handoff review plus root adjudication remain distinct requirements.

All historical sources, early review, initial recovery review and repair delta
are pinned in SOURCE_HANDOFF.json. One harmless zsh source-discovery glob found
no matching guessed RI98 directory and was corrected to explicit known paths;
no target or scientific operand was accessed. The finished packet still needs
root source acceptance, a separate concrete caller review/freeze, actual
fabricated qualification and separately admitted observed/saved arithmetic
work. This note completes source preparation only; the wider measurement and
native-law programme remains open.
