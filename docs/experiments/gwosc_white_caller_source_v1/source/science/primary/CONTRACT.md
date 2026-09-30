# RI125 exact joint-window application: source contract, revision 2

27 September 2026 UTC. Source preparation only. The implementation packet is
incomplete until every item in PREPARATION_RECORD.md is finished and independently
reviewed. This document fixes the new result structures and arithmetic choices;
it does not supply an active descriptor, runtime, admission or result. No target
or fixture may be run during preparation. No existing evidence may be changed.

Normative mathematics: accepted RI123 DESIGN.md, 31586 bytes, SHA256
4e725c42d77097e66b5b5cf5c3cc014f97b2a42663b0ef0ee3f78d8b4161699b.
Root acceptance: RI123_ROOT_DESIGN_ADJUDICATION.json, 2948 bytes, SHA256
2963dbd483539f90ef52b744e93b52451265975cbd041ff2d59df26f0d94936a.
The separately authored validator must not import the primary, its arithmetic,
its parser, or its computed expected dictionaries. It owns complete reconstruction.

## 1. Exact types and encoding

All objects below have **exactly** the named keys; optional means a prescribed
null value, not an omitted key. Integers exclude bool. JSON duplicate keys,
nonfinite literals and decimal-number tokens refuse. No numeric float is used
except an admitted PSD's canonical binary64 hexadecimal conversion. Canonical
JSON is ASCII, sorted keys, indent two, ensure_ascii true, allow_nan false,
one terminal newline. List order and exact types matter recursively.

`Int` is a plain integer. `S` is a two-element list of canonical signed lowercase
hex integer strings [numerator,denominator], gcd one, denominator strictly
positive; zero is ["0","1"]. No -0, leading zero, +, prefix or empty string.
Each completed integer, numerator and denominator is at most 262144 bits.
Each integer text has at most 65537 characters including sign. Guards cover
lifted integer sums/products as well as reduced rational results. Intermediate
Python allocation is not claimed bounded by this completed-object guard.
`I` is [S,S] with low<=high. `Vec(t,k)` is a list of exactly k values of t;
`Mat(t,r,c)` is r such rows. `Pin` is {bytes:Int>0,sha256:64 lowercase hex}.
`MaybePin` is Pin or null. `Check` is {id:literal string,passed:bool};
`Checks` is {inventory:list of exact ids,counts:{total:Int,passed:Int,failed:Int},
results:list of Check in inventory order}. Counts are derived, never trusted.

The production dimension is r=8, N=2769,L=4096,T=10961,M=16384,d=8192,
raw_samples=131072,fs=4096,rows=[0,1,27,805,1384,2741,2767,2768]. Left starts
are [0,8192,16384,24576,32768,40960,49152]; right starts are
[69632,77824,86016,94208,102400,110592]. Scenario order is
["H1:left","H1:right","L1:left","L1:right"]. No inferred or selectable domain.

`Phase` is exactly "fabricated_qualification" or "fixed_saved_application".
Actual entry functions must reject fabricated identities before numeric decode.
Fabricated functions use conspicuous context tags and cannot call actual entry
functions with real bodies. No test writes a fake historical acceptance.

`Provenance` has keys sources,inputs,acceptance,runtime. sources is exactly
{design:Pin,contract:Pin,primary:Pin,white_kernel:Pin,validator:Pin,qualifier:Pin,
cases:Pin,kernel_refusals:Pin,white_refusals:Pin,fabricated_interfaces:Pin}; inputs is an
ordered list of {role:literal,pin:Pin}; acceptance is
{design:Pin,qualification:MaybePin,custody:MaybePin,dependencies:list of
{role:literal,pin:Pin}}; runtime is {fingerprint:Pin,inventory:Pin,interpreter:Pin}.
Fabrication has qualification=custody=null and no claims of completed real
dependencies. Actual provenance needs genuine root-approved references and
full external original/copy/source/runtime/history custody. Fixed actual body
pins are checked in source before parsing. A Pin alone is not execution truth.
The final implementation's stable source pins are bound only after completion.
The new white entry source is present, but no permissible actual admission is
supplied: complete separately authored validator, qualifier and caller remain
required. No actual entry is called during preparation.

## 2. White kernel and result

The source-only primary kernel accepts declared exact interval strips and an
inherited Gram record. It does not open files, admit phases or manufacture a
predecessor. Its only domains (r,T,d) are (1,3,2),(2,3,2),(8,10961,8192), with
n in (2,3,6,7). Toy domains are qualifier-only. The singular all-zero primitive
tests `derive_shift` only; it must not receive a fictitious SPD Gram certificate.

`StripRows` is Vec({row:Int,head:Vec(I,T-d),tail:Vec(I,T-d)},r).
The row labels are [0] or [0,1] in toy domains and the fixed production rows.
`Gram` is {G:Mat(S,r,r),H:Mat(S,r,r),delta:S,inverse:Mat(S,r,r),gamma:S,rho:S}.
H is the actual RI73 key; H_G is notation only. Require symmetric G,H,inverse,
H>=0 entrywise, positive LDL pivots of G, both inverse products I,
delta=max row sum H, gamma=max row sum abs(inverse), rho=delta*gamma,
0<=rho<=1/10^12. These tiny inherited-matrix consistency checks do not recompute
the coefficient Gram or reprove its enclosure. Its acceptance/capture link is
still mandatory. Zero gamma, failed inherited usefulness or arbitrary same-shaped
unbound G/H refuse; the new usefulness gate has separate semantics below.

`Shift` has keys orientation,center,error,direct,midpoint_polarization,
trace_center,trace_error. orientation="earlier_tail_times_later_head_transpose";
center,error,midpoint_polarization are Mat(S,r,r), direct is Mat(I,r,r), and
trace_center,trace_error are S. Compute K=U0 H0^T and all three terms in
E=abs(U0)RH^T+RU abs(H0)^T+RU RH^T. Error entries are nonnegative.
For all directed entries, require midpoint_polarization=K exactly and nonempty
intersection of direct four-endpoint box with [K-E,K+E]. Retain both boxes;
never intersect/tighten the primary or symmetrize K.

`WhiteResponse` has exact keys n,a,b,center,error,entry_intervals,trace_interval,
trace_from_g_c,structural_trace_interval,delta,ell,eps,enclosure_state,
usefulness_state. n is Int; a,b,delta,ell,eps are S; center,error are Mat(S,r,r);
entry_intervals is Mat(I,r,r); three trace fields are I.
a=(n-1)/n,b=(n-1)/n^2,Z=aG-b(K+K^T),F=aH+b(E+E^T). Record [Z-F,Z+F], sum
its diagonal, and independently calculate a(trG±trH)-2b(trK∓trE).
Require identical two trace routes and intersection with
[(n-1)^2/n^2*(1-rho)*trG,(n^2-1)/n^2*(1+rho)*trG].
delta=max row sum F, ell=(n-1)^2/n^2*(1-rho)/gamma>0, eps=delta/ell.
enclosure_state="valid_conditional_enclosure". usefulness_state is exactly
"usefulness_passed" when eps<=1/10^12, otherwise "accuracy_failed".
Accuracy failure preserves the entire valid output; it is not a refusal, retry,
precision change, eigenvalue clipping, fallback or physical failure.

`WhiteMethod` is {model:"shared_raw_white_unit_response",dimensions:
{r:8,N:2769,L:4096,T:10961,M:16384,d:8192,raw_samples:131072,fs:4096},
rows:fixed list,n_order:[7,6],crop:"first_T",integer_bit_limit:262144,
precision_limit:S(1/10^12),centering:"divisor_n_shared_samples"}.
`RowIdentity` is {row:Int,source_row_pin:Pin,short_count:2769,long_count:10961,
head_pin:Pin,tail_pin:Pin,a_row_sum_interval:I,contains_zero:true}.
Strip pins hash canonical lists of retained I values, not numeric midpoint arrays.
`WhiteOperator` is {capture:Pin,ri73_result:Pin,ri73_gram_detail:Pin,
shape:[8,10961],row_identities:Vec(RowIdentity,8),gram:Gram,
inherited_gate_inventory:Vec(string,92),inherited_gates_all_passed:true}.
The exact 92 historical ids/order come from the fixed full admitted RI73 body
and are compared against the literal checked-in inventory before any contraction.

WHITE_COUPLING.json has keys schema,phase,status,method,provenance,operator,
shift,white_responses,checks,limitations. schema="ri125-white-coupling-v1";
method=WhiteMethod,provenance=Provenance,operator=WhiteOperator,shift=Shift,
white_responses=[WhiteResponse(n=7),WhiteResponse(n=6)]. status is
"enclosure_and_usefulness_passed" iff both usefulness states pass, else
"enclosure_valid_accuracy_failed". Checks records numerical usefulness results
separately from all mandatory true enclosure/input checks. Exact check ids and
limitations are in section 6. No physical sigma2 or b_mu is inferred here.

The actual wrapper must validate the full fixed RI73 result header, mode,
92 gate ids and true results, integration:gram and integration:accuracy details,
and original acceptance chain. It must fully frame/decode all 109840 captured
intervals and eight short/long rows; reject a ninth item/trailing bytes, preserve
both descriptor/path before/after identities and hash the complete consumed body.
Maximum capture 64 MiB, each row 8 MiB. Only the two strips survive each row;
actual head/tail equal long rows because they are outside short support. No
actual capture is parsed during preparation. These wrappers are supplied by
the new unexecuted `white_path.py`, not by `white_kernel.py`. Their independent
source review and fabricated qualification remain pending.

## 3. Periodic result

PERIODIC_COMPLETION.json keys: schema,phase,status,method,provenance,mode_domain,
scenarios,checks,limitations. schema="ri125-periodic-completion-v1";
status="all_declared_checks_passed". method is
{model:"periodic_completion_of_retained_proxy",M:16384,d:8192,fs:4096,
integer_bit_limit:262144,mean:"zero_for_stress_subcase_only",
joint_law:"one_latent_M_vector_repeated_exactly",physical_adequacy:false}.
mode_domain is {first:1,last:8192,count:8192,odd_count:4096,even_count:4096,
interior_pair_weight:2,nyquist_pair_weight:1,dc:
"inherited_true_annihilation_and_even_parity",ri96_rows_pin:Pin,
ri100_mode_terms_pin:Pin}. scenarios is four `PeriodicScenario` records.

`Parity` is {count:Int,center:S,error_tau:S,error_alpha:S,error:S}.
`PeriodicScenario` is {id:fixed id,n:7|6,p:4|3,q:3,source_identity:Pin,
even:Parity,odd:Parity,total:{center:S,error_tau:S,error_alpha:S,error:S},
raw_marginal:I,raw_cross:I,factor:S,centered:I,naive_difference:I,
retained_final_trace:I,checks:{source_record_match:true,full_sums_match:true,
primary_within_naive:true,width_bound:true},physical_adequacy:false,
mean_premise:"zero_stress_subcase_not_inferred_from_sample_centering"}.
The n/p/q association is determined by side, never optimized or fitted.

The operand set contains complete RI100 and RI96 results and genuine predecessor
acceptance, because RI100 lacks PSD values. Require all original source_record
identities, <f8/[8193] framing, finite nonnegative canonical float.hex strings,
exact little-endian raw-array SHA and all bins. lambda is 4096*PSD at endpoints,
2048*PSD elsewhere. Existing c/h_tau/h_alpha include pair weights; do not double
again. Accumulate separately by k parity; even+odd must reproduce full original
RI100 center/error_tau/error_alpha. Error is the sum of the two named parts.
Raw marginal=[C_all±E_all], cross=[C_even-C_odd±E_all]. factor=4pq/n^2,
centered=factor*[C_odd±E_odd], naive=(2pq/n^2)*(raw_marginal-raw_cross).
Keep negative endpoints and exact containment/width checks. Do not treat prior
final intervals as additive terms. No FFT, PSD estimation or coefficient rebuild.

The independent oracle must rebuild all 8192 complete c/h terms from all eight
RI96 row_proofs, exact Q256 rectangles and alpha bounds. For component endpoint
sum m, width w and d0=2*2^256, its terms are m^2/d0^2,
w(2abs(m)+w)/d0^2, alpha*((2abs(m)+2w)/d0+alpha). Only the real component is
active at Nyquist. It applies direct centered mode weight
2pq/n^2*(1-(-1)^k) and reconstructs every field with independent integer pairs.

## 4. Four-row deterministic join

APPLICATION_COMPARISON.json keys: schema,phase,status,method,provenance,scenarios,
nuisance_premises,checks,limitations. schema="ri125-application-comparison-v1";
phase="fixed_saved_application"; status="conditional_comparison_complete" if
white usefulness passes, else "conditional_comparison_precision_inconclusive".
method={scenario_order:fixed list,rows:fixed list,crop:"first_T",divisor:"n",
units:"nominal_strain_squared_for_observation_and_periodic_stress",
selection:"all_four_retained_scenarios_unchanged",fit_performed:false}.

Each scenario has keys id,starts,n,rows,historical,historical_projection_pin,
unit_white,periodic_stress,physical_adequacy. `historical` is exactly
{U:I,M:I,V:I,trace:{id:fixed id,interval:I,source_identity:Pin,
model:"postulated_finite_circulant_from_empirical_psd",
units:"nominal_strain_squared_sum_of_eight_centered_coordinates"}}.
It copies RI116 energy.U, energy.M, energy.V and the complete trace record.
The key is M, never Mbar. The projection pin hashes canonical
{id,starts,n,rows,historical}; raw/mean/centered vector records remain bound by
the whole original RI116 result, not spuriously revalidated by these copies.
`unit_white`={kappa:I,units:"dimensionless_unit_input_variance_response",
expression:"sigma2*kappa+b_mu",sigma2:null,b_mu:null,usefulness_state:literal}.
`periodic_stress`={interval:I,source_result:Pin,label:
"hypothetical_joint_completion_not_physical_prediction",zero_mean_assumed:true,
exact_repetition_assumed:true}. physical_adequacy="not_established".

nuisance_premises is exactly {covariance_error_eta:null,population_mean_bound:null,
calibration_envelope:null,model_adequacy:"not_established",units_literal:"",
release:"V2/C02_nominal",l1_no_cw_hw_inj_flag:"clear_in_retained_metadata",
injection_effect:"unresolved",below_10Hz_calibration:"unresolved",
data_role:"previously_inspected_public_development_calibration",
protected_validation:false,native_forward_map:null,ret_paused:true}.
No fit, standardized ratio/rank, difference-based acceptance, likelihood, SNR,
p-value, physical adequacy or independent-detector claim is produced.

Join inputs must be accepted complete white/periodic outputs and complete fixed
RI116 result with its actual custody and independent review. A valid white
accuracy_failed state yields the explicit inconclusive join, never a silent
missing dependency. A refused/incomplete dependency prevents a join. Exact
intervals only: decimal display is not part of this source contract.

## 5. Resources, refusal and qualification output

Caller limits remain 180 s active numerical child, 524288 KiB sampled sole-child
RSS, 25 ms target polling, 100 ms maximum/final gap, 50 ms ps timeout. Those are
caller obligations, not asserted runtime measurements by these kernels. Full
64 MiB per admitted JSON/capture and 8 MiB per capture row remain ceilings;
an output is capped at 64 MiB by bounded canonical serialization. No integer,
memory, time, precision, row, sample or input changes follow failure. A source
packet whose eventual full execution does not fit stays failed. Internal exact
arithmetic creates no promise about temporary allocation or execution time.

Refusal object is exactly {schema:"ri125-application-refusal-v1",status:"REFUSED",
phase:Phase,stage:"white"|"periodic"|"join"|"qualification",code:fixed code,
message:bounded string,scientific_disposition_emitted:false,postchecks:list of
{role:literal,pin:Pin|null,unchanged:bool,error:string|null}}. A later failure
invalidates earlier apparent success. Each admitted operand and source postcheck
is attempted independently, preserving first error; external caller evidence
also retains partial stdout/stderr and genuine tool completion. Kernels raise
ApplicationError(code,message); they do not themselves create a refusal file.

QUALIFICATION.json keys are schema,phase,status,method,cases,controls,checks,
limitations. schema="ri125-application-synthetic-qualification-v1";
phase="fabricated_qualification";status="all_declared_checks_passed".
method={inputs:"fixed_fabricated_only",actual_capture_evaluated:false,
actual_psd_evaluated:false,physical_law_established:false}.
cases follow CASES.md's literal order and each has {id,kind,operand_pin:Pin,
primary_result_pin:Pin,independent_result_pin:Pin,full_fields_match:true,
expected_fields_match:true}. Complete case operands/results must be retained
as separate canonical fixture artifacts with full pins. A case result conforms
to its precisely specified primitive/new-result schema, never a fake historical
predecessor. Controls follow the future complete REFUSALS.md's literal order and each has
{id,implementation:"primary"|"validator",expected_code,observed_code,
first_refusal_verified:true}. Primary and validator controls are actually called
separately in a future admitted qualification; labels are not execution evidence.
An independent fresh reference and full saved-report comparator remain mandatory.

## 6. Exact check inventories and limitations

White check order is admission:phase,admission:inputs,admission:source,
operator:gram,operator:capture,operator:rows,shift:direct,shift:polarization,
response:7,trace:7,structural:7,accuracy:7,response:6,trace:6,structural:6,
accuracy:6,completion:stable. Only the two accuracy ids may be false in a valid
white result; counts and status must reflect them exactly.
Periodic order is admission:phase,admission:inputs,admission:source,
mode:complete,scenario:H1:left,scenario:H1:right,scenario:L1:left,
scenario:L1:right,completion:stable. Join order is admission:dependencies,
historical:complete,scenario:H1:left,scenario:H1:right,scenario:L1:left,
scenario:L1:right,nuisance:unresolved,completion:stable. These latter checks
all must pass or refuse. Qualification inventory is case ids then each paired
primary/validator refusal id from the sealed concrete manifests; no hidden test.

All three application results use exactly this ordered limitations list:
1. Conditional conventional moments of fixed operators and explicitly postulated joint laws only.
2. Numerical enclosure and usefulness bounds are not statistical or physical model error.
3. All four public development/calibration scenarios remain unchanged and are not protected validation.
4. Shared-white amplitude and population mean are unresolved; sample centering does not establish zero population mean.
5. Exact periodic repetition is a hypothetical completion, not established detector noise.
6. Nominal V2/C02, blank Yunits, clear L1 NO_CW_HW_INJ, possible injection effects and below-10-Hz calibration remain unresolved.
7. No significance, fitted model, calibrated measurement, native forward map or geometry/gravity result is established; RET remains paused.

Actual fixed predecessor pins, full inherited header/Gram extraction, all 92
literal RI73 ids, bounded complete capture decoding and white assembly/refusal
wrappers are now source-defined. They are unexecuted. The independent validator,
full qualifier, periodic and join executables, and root-reviewed caller/source/
runtime/history admission remain required before complete packet acceptance.

## 7. White wrapper boundary and exact request (new, unexecuted)

`FileRef` is exactly {path:absolute literal resolved nonsymlink path, pin:Pin}.
Every file must be regular, single-link, nonempty and <=64 MiB. The prospective
interpreter FileRef is its resolved regular executable, not a symlink spelling;
the root caller separately binds the selected executable and its normal/-O
invocation. The accepted host-platform and installed-source/cache premises,
complete runtime namespace/selection custody, source capture/load/parse and
outer watchdog still belong to that caller. This wrapper is not a runtime
inventory or approval service. No interpreter is launched by this source.

`WhiteRequest` has exactly {schema:"ri125-white-request-v1",
phase:"fixed_saved_application",inputs,sources,design_acceptance:FileRef,
qualification:FileRef,custody:FileRef,runtime,admission:FileRef,output:absolute
literal absent path}. inputs has exactly these FileRef keys in provenance order:
capture,ri73_result,ri73_source,ri73_reconciliation,ri73_final_review,
ri73_audit_freeze. Their six literal whole-body pins are fixed in white_path.py.
The reconciliation and complete independent review bind the actual snapshot to
the full accepted report and arithmetic audit. The exact pinned audit freeze
retains their original receipts/source closure. These three metadata bodies are
verified as opaque originals; their authority is the already accepted historical
review, not new source-only re-adjudication or numeric parsing of a display rho.

sources is the ten-role FileRef map from section 1. `primary` is white_path.py;
`white_kernel` is the preserved kernel. `white_refusals` is the executable
white_controls.py (its complete literal control inventory is also documented in
WHITE_REFUSALS.md, which is bound through the source-contract manifest used by
the caller). `cases` is CASES.md and `fabricated_interfaces` is its companion.
The future complete qualifier binds every remaining protocol/text manifest,
including WHITE_REFUSALS.md and KERNEL_REFUSALS.md, in its full root-owned source
closure. `kernel_refusals` names KERNEL_REFUSALS.md. No primary source imports
the independent validator or qualifier; their complete reviewed bodies and
actual accepted qualification are mandatory input bindings.

runtime has exactly fingerprint,inventory,interpreter FileRefs. The complete
inventory bytes and associated installed closure are adjudicated by root,
not traversed by this application. `custody` is a genuine new root adjudication
binding this exact application/source/qualification/history/runtime; it is not
an old numeric result relabeled as current permission. The root-owned caller
must check its semantic authority and source/input selection before import.
The wrapper independently hashes every required file both before numeric decode
and on exit. A correctly formatted dictionary alone does not constitute root
authorization, source approval, qualification, transitive-history coverage,
runtime applicability, or genuine execution.

`WhiteAdmission` exactly matches white_path.admission_check's literal object:
schema:"ri125-white-admission-v1",phase:"fixed_saved_application",
status:"ROOT_ADMITS_ONE_WHITE_RUN",inputs:the six Pin map,sources:the ten Pin map,
design_acceptance:Pin,qualification:Pin,custody:Pin,runtime:three Pin map,
output:same literal path,limits:{seconds:180,sampled_rss_kib:524288,poll_ms:25,
max_gap_ms:100,ps_timeout_ms:50},history_and_runtime_adjudicated_by_root:true,
protected_validation:false,physical_covariance_accepted:false,ret_paused:true.
This packet supplies its **schema only**, no card/template with active values.
The request is pinned externally by the caller after the admission is fixed,
avoiding a circular request/admission hash. Function
`run_white(request_body:bytes,expected_request_pin:Pin)` checks that external
pin before request parsing, rejects any nonactual phase before operand body
decoding, validates all fixed pins and source paths, and then hashes every
required full file. Only after exact admission binding does it parse RI73.

The loaded primary/kernel paths must match the source references. Matching
path/file bytes does not itself establish already-loaded-code equivalence:
the accepted prospective capture/load/parse caller supplies that prerequisite.
No dynamic source import, own-source execution, alternate science module or
fallback loader is provided here.

`ri73_operand` checks every full-result top-level key, fixed mode/status,
source identity, row/dimension/model/sample-spacing and admission flags; all
92 exact gate ids/order/true flags; complete integration reconstruction
metadata; exact accepted Gram certificate keys; mathematical/accuracy detail
records; and all tiny Gram consistency checks. The full accepted report pin
authenticates other historical details; no fixture or Gaussian CDF is rerun.
For every captured row, the wrapper independently recomputes the complete
short/long array identity using the historical compact encoding and compares
it to that report's `vector_identities`. It decodes all 109840 intervals,
preserves every endpoint, compares the complete row-sum interval, and only
retains head/tail strips after the row. The parser explicitly consumes the
eighth row, expected footer and end of file, rejects a ninth row, and checks
the entire consumed body plus descriptor/path states. Head/tail have 2769
entries each and are outside short support. Gram parentage is inherited through
the accepted full report/capture/audit chain; it is not reconstructed or assumed
from arbitrary same-shaped matrices. Shift is always newly derived in the same
call and no saved Shift input is accepted by the wrapper.

The output is exclusive, bounded canonical JSON; file and directory identity
are checked after closing and the output is again checked with all required
input/source references at exit. Every registered postcheck is attempted
independently, even when an earlier read/computation/write/postcheck failed.
The first substantive exception is retained. Any later failure invalidates
scientific success, without deleting or overwriting a retained partial output.
The caller must reject any file from a refused/incomplete attempt.

Return envelope is exactly {result:WHITE_COUPLING object|null,
output_pin:Pin|null,refusal:Refusal|null,postchecks:list of Postcheck}. On
success refusal=null; on refusal result=null. A nonnull output_pin on refusal
describes a retained **unaccepted** file, not a scientific disposition.
Refusal scientific_disposition_emitted=false means no accepted scientific
disposition, even if a later postcheck invalidated an already written file.
The caller must preserve this envelope, raw stdout/stderr, partial artifacts
and genuine final completion and perform its own final custody before accepting
the result. No automatic retry, reprecision, threshold change or cleanup exists.

## 8. Coverage repairs and remaining work

F01–F04 are addressed as source specifications in CASES.md revision 2,
KERNEL_REFUSALS.md WK38, FABRICATED_INTERFACES.md and white_controls.py.
They are **not executed coverage**. The new white-control source is primary
qualification infrastructure only; it is not an independently authored oracle.
The independent author must implement full-field reconstruction and its own
controls without importing primary arithmetic/parser/expected dictionaries.
The unchanged rho gate and new eps gate have different semantics; negative
periodic lower endpoints are retained. All periodic/join/mean-error executable
interfaces above remain expressly unimplemented subsequent work. No source,
qualification, actual covariance contraction or physical result is accepted by
this source checkpoint.
