# RI119 fixed synthetic interface — source preparation

This is an unexecuted implementation contract for the accepted RI118 design.
All rationals use canonical decimal strings `str(Fraction)`, including integers
as strings (zero `"0"`, no leading sign/zero, positive denominator, reduced).
Structural dimensions/indices/counts are plain integers; bool is not int.
JSON is ASCII sorted keys, indent 2, allow_nan false, terminal newline.
Target modules have no import-time I/O, CLI, data loader or ambient project
imports. Standard library only. Source constants/oracles are declarations.

## Scientific result and APIs

`primary.build_result()` enumerates the complete fixed sign domains and returns
one canonical-serializable scientific result. `primary.compare_result(given,
expected)` is the full retained-report guard against a fresh complete primary
result; caller/qualifier owns that reference, never an external supplied oracle.
The normal saved path must compare against a fresh primary result and run the
separately authored `validator.validate_result(given)`. Validator reconstructs
all expected entries using independent selectors and moment/factor algebra;
it may not import/call primary or enumerate the primary's full sign cubes.
Both expose `parse_result(body)` (duplicate/nonfinite/noncanonical refusal),
`canonical(result)`, and typed `PrimaryError` / `ValidationError` with `.code`.
Validator returns exactly `{'status':'all_fields_independently_match',
'cases':9,'bounds':3,'groups':12}` on complete success, or deliberately raises.

Scientific result keys exactly `schema,phase,status,method,cases,bounds,groups,
limitations`. Schema `ri119-joint-window-synthetic-v1`; phase
`fabricated_joint_window_qualification`; status `all_declared_checks_passed`.
`method` is the fixed object:
`{'rational_encoding':'reduced_decimal_strings','arithmetic':'exact_rational',
'primary_route':'complete_sign_enumeration','validator_route':'independent_moment_selector_factor_algebra',
'inputs':'fixed_synthetic_only','divisor':'n','real_operator_evaluated':false,
'empirical_inputs_evaluated':false,'physical_model_validated':false}`.
Groups are strings Q01,...,Q12 in that exact order. Limitations are the literal
list written identically in both source modules from this protocol:
- `Synthetic joint-window arithmetic only; no empirical data or actual coefficient capture.`
- `Shared sample and covariance refusals concern the declared fixed model, not every alternative model.`
- `Finite circulant marginals do not select a physical joint window law.`
- `Mean, calibration and model-error premises are explicit and not estimated here.`
- `No significance, physical calibration, protected validation or native forward claim; RET remains paused.`

## Complete fixed case inputs

Case order and IDs: `Q02_white_two`, `Q03_periodic_two`, `Q05_white_three`,
`Q06_constant_mean`, `Q07_quadratic_mean`, `Q08_scale_minus_one`,
`Q08_scale_two`, `Q09_oriented_matrix`, `Q10_zero_map`.
Every case has M=4,T=3,stride=2. n=3 (starts0,2,4, raw length8) only for Q05/Q07;
otherwise n=2 (starts0,2, raw length6). Baseline A is the one-row `(1,0,-1)`.
Q09 has rows `(1,0,-1),(0,1,-1)`; Q10 has one zero row.
Raw factor F is the identity of raw length except Q03, whose latent dimension
is4 and whose six rows select latent coordinates `(0,1,2,3,0,1)`.
Raw mean is zero except Q06 all3 and Q07 entry j*j. Scale is1 except the two Q08 cases, which use -1 and 2 respectively;
scale multiplies both raw factor and raw mean, not A. All 2^latent_dimension
sign vectors with lexicographic product order `(-1,+1)` are mandatory.
No Monte Carlo approximation, fitted scale or random seed is involved.
For every Q06 sign vector, primary also checks the actual A row sums are zero
and output equals the same-sign zero-mean, unit-scale output. For every Q08
vector, it checks output equals the signed scale times that same-sign baseline
(not absolute scale). These mandatory pointwise guards occur before the sign
is counted. Their complete support is the case's sign_count; no mere comparison
of second moments is substituted for these properties.

Each case has exactly `id,model,selectors_M,selectors_T,output_map,raw_mean,
raw_covariance,window_marginal_covariances,stacked_output_mean,
stacked_output_covariance,cross_blocks,mean_output_covariance,
centered_covariance_average,mean_dispersion,covariance_contribution,
expected_V,direct_average_V,expected_U,mean_output_energy,sign_count`.
`model` exactly `kind,M,T,stride,n,starts,raw_length,latent_dimension,
output_dimension,A,raw_factor,raw_mean,scale` (all matrices/vectors rational
strings except dimension/index ints). `kind` is `shared_periodic` for Q03,
otherwise `shared_raw_white`. The model's raw_factor/raw_mean are UNscaled
base F/mu; numerical moments include scale. Selectors contain integer0/1.
Output_map stacks A times T-selectors; it excludes scale and maps nominal X.
All matrix fields are nested rational-string lists, including zero entries.
Vectors are rational-string lists. Scalars are single rational strings.
`cross_blocks[a][b]` is the full oriented output_dim by output_dim block,
including both directions. `window_marginal_covariances` contains n full4x4
raw M-window covariances. `mean_output_covariance` is covariance of the finite
output mean. `centered_covariance_average` is average covariance of centered
outputs (deterministic mean dispersion removed), not the stacked covariance.
`expected_U` averages E||d_a||^2; `mean_output_energy` is E||bar_d||^2.
`direct_average_V` is the primary's mean of the pointwise V values; validator
must reconstruct it through moments and require equality to expected_V.

## Bounds and nuisance factors

Three ordered records with closed forms (each scalar/matrix rational encoded):
1. `Q12_calibrated_constant`, keys `id,output_dimension,A,C_cal,input,output,
constant_annihilation_claim`: output_dimension1,A[[1,0,-1]],C_cal diag(1,1,2),
input[1,1,1],output[-1],constant_annihilation_claim=false.
2. `Q12_covariance_error`, keys `id,n,output_dimension,D,Pi,Sigma_model,
Sigma_true,eta,model_contribution,true_contribution,absolute_difference,bound`.
n2,output_dimension1,D[[1],[-1]],Pi[[1/2,-1/2],[-1/2,1/2]], scalar covariances
as 1x1 matrices1 and2,eta1, contributions 1 and 2, difference1,bound1.
3. `Q12_calibration_error`, keys `id,n,output_dimension,D,Pi,C0,DeltaC,F,
model_contribution,true_contribution,absolute_difference,bound`.
n2,output_dimension1,same D/Pi, C0/DeltaC/F all1x1[1], contributions 1 and 4,
difference3,bound3. These dimensioned factor toys do not use eight output rows.

## Comparison order and stable first-refusal codes

Each comparator first checks result mapping/exact root keys (`SCHEMA`), then
schema (`SCHEMA`), phase (`PHASE`), status (`RESULT`), method (`SCOPE`),
groups/case IDs/bound IDs (`INVENTORY`) and limitations (`SCOPE`). Then validate
all rational strings and plain dimensions recursively (`EXACT` / `DIMENSION`).
For each case in fixed order: check fixed dimension values (`DIMENSION`),
then Q02/Q03 PSD guard, then compare full model (`MODEL`), M selectors
(`SHARED_INDEX`), T selectors (`CROP`), output_map (`OPERATOR`), raw means
(`MEAN_TERM`), raw/window/stacked/cross/mean-output/centered covariance fields
(`COVARIANCE_MODEL`), stacked output mean and mean_dispersion (`MEAN_TERM`),
sign_count (`ENUMERATION`), then scalar energy fields (`ENERGY`).
For bound records, exact keys/dimensions first; require the universal
constant-annihilation claim to be false (`CALIBRATION`); supplied eta must be finite/nonnegative (`BOUND`);
then complete remaining entrywise equality (`BOUND`).
A named `require_psd_2x2(matrix)` guard accepts symmetric2x2 rational covariance
within the arithmetic resource bounds iff a>=0,c>=0,a*c-b*b>=0, and
otherwise raises `PSD` for a mathematical failure. Each product is bounded
before subtraction; an oversized product raises `RESOURCE` even if it would cancel. It is used in production
on the Q02/Q03 scalar two-window covariance blocks before field comparison;
source qualifiers exercise the exact same guard on [[2,3],[3,2]].
No general full-matrix eigensolver or tolerances are introduced. Complete
factor/selector-derived entrywise validation supplies the remaining PSD route.

`parse_result` requires bytes, duplicate-free finite JSON and exact canonical
whole bytes; serialization defects use `CANONICAL`. Rational string defects
are diagnosed by result comparison (`EXACT`), not silently normalized.
Malformed dimensions/types never succeed because Python bool equals int.

## Planned source files and qualification envelope

`primary.py`, separately authored `validator.py`, `qualify.py`, this contract,
`IMPLEMENTATION.md`, and source-only dependency/hand-off metadata. Qualifier
receives captured primary/validator module objects from a later root-admitted
caller, imports neither, and has no file/subprocess/scientific-data access.
It runs one complete primary enumeration, both guards on its full result,
then the frozen mutation inventory against that same complete reference.
Validator builds expectations independently. Qualifier retains original
scientific result and complete case/refusal/expected/actual outcomes, checks
no input/reference mutation, and returns a distinct closed qualification
report. Saved canonical report validation and actual normal/optimized byte
identity/custody remain required; concrete caller source comes later.

## Complete expected-field oracle declaration

There is no saved scientific output in this source packet. The following fixes
all expected values algebraically before execution; the separately authored
validator implements this declaration without reading primary source. Let the
literal model above have scale s, unscaled F and mu, n windows and q outputs.
Set R=sF, m=s*mu, W_a the declared first-T selector, D_a=A W_a, D the stack,
L=(1/n)[I_q ... I_q], P=I_(nq)-1_n 1_n^T/n tensor I_q, and G=DR.
Then every numerical field is completely fixed as follows:

| Field | Declared complete expectation |
|---|---|
| selectors_M/selectors_T | Every entry is 1 iff column=start_a+row, otherwise 0, for exactly M/T rows. |
| output_map | Full D, including every zero tail entry. |
| raw_mean/raw_covariance | m and RR^T. |
| window_marginal_covariances | Full S_a RR^T S_a^T for each M-selector S_a. |
| stacked_output_mean/covariance | Dm and GG^T. |
| cross_blocks[a][b] | Full D_a RR^T D_b^T with the specified orientation. |
| mean_output_covariance | LGG^T L^T. |
| centered_covariance_average | Sum of the n diagonal q-by-q blocks of PGG^T P divided by n. |
| mean_dispersion | ||PDm||^2/n. |
| covariance_contribution | ||PG||_F^2/n. |
| expected_V/direct_average_V | (||PG||_F^2+||PDm||^2)/n; the primary independently averages pointwise V. |
| expected_U | (||G||_F^2+||Dm||^2)/n. |
| mean_output_energy | ||LG||_F^2+||LDm||^2. |
| sign_count | Exactly 2^latent_dimension. |

The primary's pointwise sample mean and the validator's factor algebra must
agree in every complete field, not merely these descriptive scalar examples:

| Fixed case | Declared expected V | Declared expected U | Declared mean-output energy |
|---|---|---|---|
| Q02_white_two | 3/2 | 2 | 1/2 |
| Q03_periodic_two | 2 | 2 | 0 |
| Q05_white_three | 16/9 | 2 | 2/9 |
| Q06_constant_mean | 3/2 | 2 | 1/2 |
| Q07_quadratic_mean | 400/9 | 566/3 | 1298/9 |
| Q08_scale_minus_one | 3/2 | 2 | 1/2 |
| Q08_scale_two | 6 | 8 | 2 |
| Q09_oriented_matrix | 5/2 | 4 | 3/2 |
| Q10_zero_map | 0 | 0 | 0 |

Q09 specifically requires C=[[-1,0],[-1,0]], reverse block C^T,
Omega=[[2,1],[1,2]], centered average [[3/2,3/4],[3/4,1]]. The scalar trace does
not replace any entrywise obligation. Q07 has mean vector[-4,-12,-20],
mean-dispersion128/3 and covariance contribution16/9. All numbers in this
section are prospective rational declarations, not executed evidence.

## Frozen negative-control inventory and first refusal

Each control mutates one complete fresh copy of the baseline. The literal
paths and values in `qualify.MUTATIONS` are part of this contract. There are
33 full-report mutations, five parser controls and three public PSD controls,
each run separately against both implementations:41 per implementation.
Unexpected exceptions or unexpected success fail the whole qualification.
The exact expected labels, in mandatory order, are:

| ID | Intended defect | First refusal |
|---|---|---|
| M01_missing_root_key | missing limitations | SCHEMA |
| M02_wrong_phase | empirical-validation phase | PHASE |
| M03_wrong_result_status | pending status | RESULT |
| M04_physical_scope | physical-model claim | SCOPE |
| M05_missing_case | missing final case | INVENTORY |
| M06_shared_coordinate | shared M selector entry removed | SHARED_INDEX |
| M07_first_T_crop | first-T selector entry removed | CROP |
| M08_output_map | first operator entry zero | OPERATOR |
| M09_declared_factor | first raw-factor entry zero | MODEL |
| M10_nonPSD_covariance | [[2,3],[3,2]] | PSD |
| M11_dropped_cross_term | declared Q02 off-diagonal covariance zero | COVARIANCE_MODEL |
| M12_transposed_cross_block | transpose only Q09 block[0][1] | COVARIANCE_MODEL |
| M13_omitted_mean_dispersion | Q07 mean term zero | MEAN_TERM |
| M14_wrong_n_divisor | Q02 V changed to3 | ENERGY |
| M15_wrong_direct_energy | Q02 direct V zero | ENERGY |
| M16_rational_boolean | rational replaced by bool | EXACT |
| M17_unreduced_rational | rational string2/2 | EXACT |
| M18_scientific_float | binary float1.5 | EXACT |
| M19_wrong_sign_count |63 rather than64 | ENUMERATION |
| M20_boolean_sign_count | bool count | DIMENSION |
| M21_calibrated_constant_claim | universal cancellation true | CALIBRATION |
| M22_negative_eta | eta=-1 | BOUND |
| M23_understated_covariance_bound | bound0 | BOUND |
| M24_understated_calibration_bound | bound2 | BOUND |
| M25_wrong_nuisance_dimension | q=8 rather than1 | DIMENSION |
| M26_missing_case_field | raw_mean omitted | SCHEMA |
| M27_incomplete_covariance_row | Q09 row entry omitted | DIMENSION |
| M28_boolean_selector | bool index entry | DIMENSION |
| M29_oversized_rational_component |2468 decimal digits | RESOURCE |
| M30_boolean_model_kind | bool replacing string | EXACT |
| M31_wrong_group_inventory | Q01 omitted | INVENTORY |
| M32_zeroed_oriented_covariance | Q09 centered[0][1] zero | COVARIANCE_MODEL |
| M33_oversized_malformed_scalar |2468 nonnumeric characters | RESOURCE |
| P01_duplicate_keys | duplicate JSON key | CANONICAL |
| P02_nonfinite | JSON NaN | CANONICAL |
| P03_missing_terminal_newline | incomplete canonical body | CANONICAL |
| P04_body_over_limit |2MiB+1 bytes | RESOURCE |
| P05_nonbytes | string instead of bytes | CANONICAL |
| G01_nonsymmetric | [[2,0],[1,2]] | PSD |
| G02_negative_diagonal | [[-1,0],[0,1]] | PSD |
| G03_oversized_cancelled_products | all four entries2^4096; products exceed8192 bits before cancellation | RESOURCE |

All case/bound shape, key and exact scalar types are checked globally first.
Then each case's fixed dimension VALUES are checked before its PSD guard and
ordered field identities; after all cases, each bound's dimension values precede
its calibrated-constant/eta/entrywise checks. Positive baseline Q03 explicitly
allows singular PSD covariance. The public PSD API requires canonical strings;
its argument shapes use DIMENSION and scalar syntax uses EXACT/RESOURCE.

## Closed qualification report

`qualify.run(primary,validator)` accepts only later caller-captured module
objects, creates one fresh primary reference and returns the closed report.
Root keys exactly `schema,phase,status,scientific_result,baseline,
mutation_refusals,parser_refusals,psd_refusals,coverage,
control_count_per_implementation,scientific_case_count,bound_count,group_count,
input_and_reference_unchanged,limitations`.
Schema=`ri119-joint-window-qualification-v1`, phase as above,
status=`all_qualification_checks_passed`. The full scientific result is retained.
Baseline records exact success objects from both implementations. Each refusal
record is exactly `id,expected,primary,validator`; actual deliberate codes must
match the frozen inventory. `coverage` is the literal Q01..Q12 evidence mapping
in qualify.py. Counts are41,9,3,12 respectively. Immutability flag true is set
only after canonical before/after equality checks; it does not claim language
sandboxing. The five qualification limitations are the literal `LIMITATIONS`
in qualify.py and are distinct from the scientific result's limitations.

`qualify.audit(report,primary,validator,reference)` checks the entire expected
report and repeats complete scientific reconstruction; the reference must be
fresh and caller-owned. Success exactly `{'status':'all_saved_fields_match',
'historical_controls_reexecuted':false,'scientific_independent_reconstruction':true}`.
This audit compares saved control records with fixed expectations; it does not
re-execute the historical controls, so genuine child/source custody remains
mandatory. `run` includes serialize/parse and full audit before returning.
`qualify.canonical`/`parse_report` require canonical finite duplicate-free ASCII
JSON at most2MiB. The fixed schema is identical in normal and optimized modes;
there is no mode-dependent science, timestamp or provenance in this report.
