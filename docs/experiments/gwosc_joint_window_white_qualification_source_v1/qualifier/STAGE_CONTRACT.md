# RI125 white-only qualification source contract

Status: UNEXECUTED SOURCE FOR INDEPENDENT REVIEW. No source acceptance,
fabricated qualification, runtime feasibility, actual-data admission or physical
result is asserted. The original white packet is immutable. This is a separate
15-case stage; it cannot satisfy the full 32-case application qualification.

The immutable predecessor is
`ri125-white-source-completion-bg27qfdn/HANDOFF.json`, 5379 bytes,
SHA256 `4f5e547c359b8e1c3e4ee87f7b2351ce8259b705e7a3e033509b4072f3862468`.
Its CONTRACT.md, CASES.md revision 2, FABRICATED_INTERFACES.md,
KERNEL_REFUSALS.md and WHITE_REFUSALS.md remain the exact scientific and refusal
specifications. Its kernel, wrapper and 142-control source are used unchanged.
Root's bounded unexecuted-source disposition is
`ri127-root-proof-review-tz7oyfkj/RI125_WHITE_SOURCE_DISPOSITION.json`, 2174 bytes,
SHA256 `90c66df22b5ff16b578f38a4aba811638ec9f10f2b6089f898227691aa8219db`.
Acceptance of that predecessor is not acceptance of this new qualifier.

## Interfaces and ownership

Root alone reviews and admits a future caller, interpreter/runtime, complete
transitive source/history closure, execution modes and namespace. No active
freeze, admission, caller, capture-load path or runtime profile is created here.
The source modules have no CLI, import-time file access or automatic execution.
Their normal imports are source code only, and have not been performed.

Prospective primary entry:

```
run_white_qualification(directory: str, source_bindings: dict,
                        validator: ModuleType, validator_controls: ModuleType,
                        *, phase: str)
```

The keyword has no default in executable source: it must be explicitly supplied.
`directory` is a literal absolute nonsymlink path, absent before creation, with an
existing parent. Every source is outside that directory. A future caller must
capture and load reviewed bytes and bind the returned genuine completion; a
matching module `__file__` plus a disk hash is not proof of loaded-code identity.
Mode-specific separate absent directories are mandatory; there are no retries,
overwrites or implicit fallback modes. Normal qualification must be independently
accepted before separate optimized admission under the retained root flow.

The agreed independently authored interfaces are:

```
white_validator.validate_fixture_bytes(body: bytes) -> WhiteFixtureResult | BoundResult
white_validator.validate_fabricated_assembly(capture_ref, gram, case_id, context)
    -> FabricatedAssembly
validator_controls.run_controls(directory: str) -> IndependentControls
```

The fixture validator receives only immutable canonical operand bytes, never a
primary result, saved answer or expected dictionary. It must independently
validate the literal case recipe as well as reconstruct every field; a different
internally consistent operand under the same case ID is not an accepted fixture.
The assembly validator receives the fabricated capture reference and explicit
Gram operand and must independently derive and reconcile the complete rows,
strips and Gram. This stage invokes assembly only for W09. Definitions of J01/J02
in a validator do not give this stage join coverage. The validator and its
controls are authored in a separate reservation and are not included, replaced
or self-authored here. Root reconciles their final sources and this interface
before any acceptance. Their own source-only declarations are not execution.

`source_bindings` has exactly these 17 keys, each a FileRef:

```
white_kernel, white_path, wrapper_controls, white_contract, cases,
kernel_refusals, fabricated_interfaces, white_refusals_text,
white_source_handoff, white_root_disposition, fixtures, kernel_controls,
orchestrator, stage_contract, control_expectations, validator, validator_controls
```

Paths are distinct. The first ten roles have exact immutable byte/hash constants
in the orchestrator; the remaining seven must be independently reviewed and
bound by root's future caller, rather than accepted because they self-name a
hash. All 17 are registered before any is opened and independently postchecked.
All additional transitive modules, interpreter, standard library, native
dependencies, environment and trusted host premises remain root caller duties;
these 17 roles do not purport to constitute the whole runtime closure.

## Types and exact scientific coverage

All objects below are closed: no additional or omitted keys, `bool` is not Int,
and complete equality is recursively type-sensitive. `Pin={bytes:Int,sha256:str}`
uses complete bytes and lowercase SHA256; ordinary source/artifact pins are
positive and at most 67108864 bytes. `FileRef={path:str,pin:Pin}`. `Artifact` is
`{name:str,pin:Pin}`, with a literal basename below the owned directory. Values
`S`, `I`, `Gram`, `Shift`, `WhiteResponse`, `RowIdentity`, `WhiteFixture`,
`WhiteFixtureResult`, `BoundFixture`, `BoundResult` and `FabricatedAssembly` mean
the complete exact nested predecessor schemas, not field-name summaries. S is a
reduced signed-hex integer pair; I preserves both ordered endpoints. Canonical
artifact JSON is ASCII, sorted keys, indent 2 and a terminal newline. The full
fabricated capture alone uses sorted compact JSON with no terminal newline.

Literal case order is the complete CASE_IDS tuple in white_fixtures.py:
W01_single_white_two, W02_single_white_three, W03_oriented_two,
W04_negative_scale, W05_double_scale, W06_interval_mixed,
W07_interval_crosses_zero, W08_zero_shift, W09_production_boundary_sparse,
W10_usefulness_boundaries, W11_asymmetric_rational_radii,
W12_sparse_lifted_denominators, W13_full_response_below,
W14_full_response_equal, W15_full_response_above.

W01–W05 retain all directed scalar/two-row products, their exact Grams and full
responses. W06–W08/W11/W12 are shift-only; no inverse is invented. W06 preserves
the wider primary enclosure and negative endpoints. W11 contains unequal
nonzero directed error entries; W12 supplies all 44304 interval strip entries
(8 rows, two strips of 2769), with unequal denominators and nontrivial endpoints.
No coordinate or zero entry can be omitted from complete reconstruction.

W09/W13–W15 each provide 109840 complete intervals (8 rows times 2769+10961),
all 44304 strip intervals and the complete eight-dimensional Gram. W09 uses
both exact support endpoints, has n=[7,6] and additionally exercises complete
capture assembly and exhaustion. W13–W15 use n=[7], the exact deliberately loose
H=hI prescription and q=10^-12 plus respectively -10^-24, 0, +10^-24. All old
rho gates pass strictly; complete new response epsilon is q, with pass/pass/fail
states. The H bound is valid for the fabricated exact rows but is not an actual
radius-derived RI73 certificate. Both complete trace routes and the structural
interval are retained. W10 remains four standalone bound pairs with a distinct
result schema and check inventory, not a claim of response-boundary coverage.

For each ordinary white case the supplementary primary anchors return
`ExpectedChecks={inventory:list[str],counts:{total:Int,passed:Int,failed:Int},
results:list[{id:str,passed:bool}]}` with exactly these six ordered IDs:

```
fixed_operand_schema_and_recipe, complete_result_shape, literal_case_anchor,
full_directed_shift_consistency, correct_gram_presence_and_inherited_gate,
correct_response_presence_and_new_gate
```

For W10 only, the exact four IDs are fixed_bound_operand_recipe,
complete_bound_result_shape, literal_predicate_results, fabricated_identity_only.
On success all bits are true and counts are 6/6/0 or 4/4/0. These literal anchors
are primary checks, not an independent validator. They supplement complete
type-sensitive primary/independent equality and the fresh saved reconstruction.

## Control calls and exact refusal envelopes

The exact ordered 179 IDs are WK01–WK38, WC01–WC26, WG01–WG92,
WC27–WC46, WT01–WT03. `CONTROL_EXPECTATIONS.json` contains exactly
`{schema:"ri125-white-only-control-expectations-v1",
phase:"source_specification_only",order:list[179 IDs],
refusals:list[176 {id,code,message}],tails:["WT01","WT02","WT03"]}`.
Every first-refusal code and normalized message is literal. This file records
expectations only. It was prepared from source text, without invoking a control.

kernel_controls.py supplies every WK01–WK37 call. The sealed 142-control module
supplies WK38, WC01–WC46, WG01–WG92 and WT01–WT03. Thus each complete implementation
must execute 38 kernel and 141 wrapper/tail controls: 176 refusals plus three
positive tail checks. No count treats WK38 twice. WK25's changed off-diagonal G
reaches the inverse-product check at (0,0) before the later symmetry check;
its exact first refusal, like WK28, is GRAM / both inverse products. WK38 reaches
STRUCTURAL / trace structural interval intersection. No RI73 accepted body is
fabricated: the old malformed header scaffolds stop at their specified header
or one of 92 gate guards before the deliberately absent scientific body.

Primary kernel and wrapper reports respectively have schema
`ri125-primary-kernel-controls-v1` and `ri125-primary-white-controls-v1`, counts
37 and 142. Their complete original reports are separately retained. The
aggregate primary schema is `ri125-primary-complete-white-controls-v1`; the
independent schema is `ri125-independent-white-controls-v1`. All four use exactly:

```
{schema, phase:"fabricated_qualification",
 context:"RI125_FABRICATED_ONLY_NOT_HISTORICAL",
 actual_scientific_input_opened:false, independent_validator_run:bool,
 controls:list, counts:{total:Int,passed:Int,failed:Int}, status:str}
```

The independent flag is true only for the separately authored report. A passing
complete report has total=passed=179, failed=0 and status
`all_declared_controls_passed`. Primary partial reports use their stated counts;
their failed calls are retained with status `control_failure`. The stage requires
every complete report field and every actual refusal to agree with the literal
manifest. Scientific field comparison is never relaxed by control normalization.

Each refusal record has **six fields total**:
`{id,expected_code,expected_message,observed_code,observed_message,passed}`.
Passed requires exact code and exact normalized message, not merely any exception.
WT01 instead is `{id:"WT01",passed:true,postchecks:list[2 TailPostcheck]}`.
TailPostcheck is `{role:str,pin:Pin|null,unchanged:bool,error:str|null}`. Roles are
first then second; first is false/null/nonempty bounded diagnostic, second is
true/valid Pin/null. This witnesses that the second postcheck was attempted
despite failure of the first. WT02/WT03 are `{id,passed:true,refusal:TailRefusal}`.
TailRefusal is exactly:

```
{schema:"ri125-application-refusal-v1",status:"REFUSED",
 phase:"fixed_saved_application",stage:"white",code:str,message:str,
 scientific_disposition_emitted:false,postchecks:list[2 TailPostcheck]}
```

These are retained original tail-function outputs inside fabricated controls,
not actual phase admissions. WT02 preserves EXACT / first-error; WT03 invalidates
apparent success with CUSTODY / one or more final source/input postchecks failed.
After the implementation-specific exception-class prefix and code prefix are
removed, these messages remain exact. Each report must retain precisely its
WT01 postchecks in WT02 and WT03. Whole diagnostic reports and control trees are
saved. Across implementations, path/error-class details may differ; the exact
prescribed first-error and complete-attempt semantics may not.

## Prospective sequence and saved artifacts

1. Validate explicit fabricated phase, 17 source references, fixed predecessor
   pins, loaded module paths and independent function interfaces. Capture all
   source prechecks; require a new absent owned output directory.
2. For each of the 15 fixed cases, create and exclusively save canonical operand,
   primary result and separately reconstructed independent result. Check complete
   typed equality and fixed-case anchors; release large temporary objects before
   the next case.
3. Save one compact W09 fabricated capture. Run primary and independent complete
   assembly, preserving all row identities, own-derived Shift and both full
   responses. Compare every typed field and retain both results.
4. Execute new kernel, unchanged wrapper and independent controls in three
   separate fresh subdirectories. Each tree is reserved before its call and
   inventoried even if the call fails; save all original returned reports before
   comparing them. Form the exact primary aggregate and require both complete
   reports to satisfy the full 179-control contract.
5. Read every saved operand and reconstruct the independent result afresh. Compare
   every field with both saved results and all anchors. Independently reconstruct
   full W09 assembly from its saved capture again. Check both saved complete
   control envelopes. This last control check is **not another control run**.
6. Exclusively save the comparison and white-only report. Independently attempt
   every tree and source/artifact postcheck even after failure. Inventory the
   whole owned namespace, including partial files and intentional bad links;
   require complete successful artifact identities and unchanged control trees.
   Preserve the first error; any late failed check invalidates an apparent report.

On complete success there are exactly 57 top-level artifact files plus the three
owned control subdirectories and their retained contents: 45 case files,
W09-complete-capture.json and two assembly files (3), three tree inventories,
four original/aggregate control reports, FRESH_SAVED_COMPARISON.json and
WHITE_ONLY_QUALIFICATION.json. The white-only report's artifact list has 56
entries, excluding itself to avoid a recursive pin. The returned list has all
57, and 17+57=74 ledger postchecks plus three tree postchecks. Partial failure
does not fabricate these counts or complete an unfinished stage.

Case files are W01-operand.json/W01-primary.json/W01-independent.json through
W15 with the same suffixes. Assembly files are W09-primary-assembly.json and
W09-independent-assembly.json. Original controls are PRIMARY_KERNEL_CONTROLS.json,
PRIMARY_WRAPPER_CONTROLS.json, PRIMARY_ALL_CONTROLS.json,
INDEPENDENT_ALL_CONTROLS.json. Tree subdirectories are primary-kernel-controls,
primary-wrapper-controls and independent-controls; inventory basenames are their
uppercase name plus `_TREE.json` (hyphens remain hyphens).

`CaseRecord={id,kind,operand:Artifact,primary:Artifact,independent:Artifact,
full_fields_match:true,expected_checks:ExpectedChecks}`. Kind is
bound_predicate_only only for W10, white_primitive otherwise.
`AssemblyRecord={id:"W09_production_boundary_sparse",capture:Artifact,
gram_pin:Pin,primary:Artifact,independent:Artifact,full_fields_match:true}`.

Fresh comparison has exactly:

```
{schema:"ri125-white-only-fresh-saved-comparison-v1",
 phase:"fabricated_qualification",
 cases:list[15 {id,fresh_result_pin:Pin,all_fields_match:true}],
 assembly:{id:"W09_production_boundary_sparse",fresh_result_pin:Pin,all_fields_match:true},
 saved_control_envelopes_fully_checked:true,controls_rerun_by_comparator:false,
 actual_data_evaluated:false,full_application_qualified:false}
```

The report has exactly schema, phase, status, context, scope, limits,
source_bindings, cases, complete_capture_assembly, controls,
fresh_saved_comparison, artifacts, limitations. Schema is
`ri125-white-only-qualification-v1`; status is `all_white_only_gates_passed`.
Scope is exactly `{white_case_ids:list[15 IDs],white_case_count:15,
full_application_case_count:32,full_application_qualified:false,
actual_data_admitted:false,periodic_mean_or_join_executed:false,physical_claim:false}`.
Cases, assembly and fresh comparison have the preceding types. Controls is
exactly `{order:list[179 IDs],per_implementation:179,kernel_per_implementation:38,
wrapper_and_tail_per_implementation:141,primary_kernel:Artifact,
primary_wrapper:Artifact,primary_complete:Artifact,independent_complete:Artifact,
both_exact_inventories_and_first_refusals_passed:true,
trees:list[3 {name,inventory:Artifact}]}`. Limitations is the literal ordered five
strings in the orchestrator, with no freedom to infer a wider acceptance.

The return envelope is exactly `{result:Report|null,report_pin:Pin|null,
artifacts:list[Artifact],postchecks:list[TailPostcheck],
tree_postchecks:list[{name,unchanged:bool,error:str|null}],
namespace:{inventory:TreeInventory|null,error:str|null},refusal:StageRefusal|null}`.
TreeInventory is `{schema:"ri125-fabricated-control-tree-v1",
records:list[{name:str,kind:"directory"|"symlink"|"file",pin:Pin|null,target:str|null}]}`.
Names are relative to that inventory root, whose name is `.`; files retain whole
content identities, including zero-byte partial files in this diagnostic schema
only. Directories have null pin/target; symlinks have null pin and their literal
target, never followed. Deliberate hardlinks are retained control evidence, not
admitted scientific inputs. Private initial lstat states are independently
compared with final states. Each inventory is bounded to depth 8, fewer than or
equal to 1024 records and 64 MiB per regular file; targets are at most 4096 chars.
If an inventory cannot complete, the bounded failure diagnostic is retained;
no complete-inventory claim is emitted. No pre-existing rejected output namespace
is opened: inspection requires the directory to have been created by this call.

StageRefusal is `{schema:"ri125-white-only-qualification-refusal-v1",
status:"REFUSED",phase:"fabricated_qualification",code:str,message:str,
white_stage_qualified:false,full_application_qualified:false,actual_data_admitted:false}`.
The first primary ApplicationError preserves its code; other exception types
produce FAILURE and preserve the bounded original diagnostic. No output is
deleted or rewritten on failure. Registered incomplete writes fail custody;
the namespace record attempts to preserve their actual contents. A report file
left by an attempt later refused is not accepted evidence. The external caller
must retain the complete return envelope and genuine outer completion, and carry
out its own complete pre/post source/runtime/output checks. This module does not
write its own final receipt or claim to recover after process termination.

## Resources, unresolved premises and next boundary

Original limits are unchanged: 180 seconds; sampled tree RSS 524288 KiB;
25 ms polling; maximum gap 100 ms; ps timeout 50 ms; 67108864-byte file ceiling;
8388608-byte capture-row ceiling; 262144-bit completed integers. Monitoring and
actual measured completion remain external caller duties. This module records
those limits and enforces its file/integer/parser boundaries, but cannot prove
wall time or peak memory by source inspection. Full-size zero operands are still
fully present and traversed; no sparse omission weakens the checks. There is no
claim that the fixed 15-case campaign fits the runtime limits until genuinely
admitted and observed. Failed precision keeps its valid conditional enclosure
and accuracy_failed state. No new rho/epsilon threshold, zero clipping or altered
support convention is introduced.

Pending: complete independent review of this new source, separately authored
validator and controls; exact reconciled closure and caller; root-only source and
runtime acceptance; genuinely admitted normal then separately admitted optimized
fabricated qualification; complete retained receipts and independent saved review.
The additional ten periodic, five mean/calibration and two join cases and their
executable consumers/validators remain future work. The full application and
actual-data gates cannot accept this white-only report as their 32-case report.

All protected-validation, freeze/custody, public-development-only and experimental
prerequisites remain. Unit-white amplitude, population mean and real cross-window
covariance are unresolved. Periodic completion remains hypothetical; actual H and
M names remain distinct from notation H_G/Mbar. Calibration/model error premises,
nominal V2/C02, blank Yunits, L1 NO_CW_HW_INJ/injection and below-10-Hz limitations
are not resolved by synthetic arithmetic. No significance, fitted model, native
forward map, geometry/gravity law or physical validation follows. RET alone stays
paused. No fetch, actual capture/PSD decode or repository/Git operation was made.
