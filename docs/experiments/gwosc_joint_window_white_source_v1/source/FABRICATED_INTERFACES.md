# RI125 fabricated interfaces, revision 1 — source only

These interfaces are separate from actual WhiteOperator, PeriodicScenario,
APPLICATION_COMPARISON, RI73 results and historical acceptance. Nothing here
has been generated or executed. Literal case identifiers and order are CASES.md
revision 2. All objects have exactly the listed keys; all Int/S/I/Gram/Shift/
WhiteResponse types and bounded canonical JSON follow CONTRACT.md. Context is
always `RI125_FABRICATED_ONLY_NOT_HISTORICAL`, phase is always
`fabricated_qualification`, historical_acceptance is always null and
physical_claim is always false. These four fields are present in every result.
No fabricated function calls the actual `run_white` entry point or supplies an
accepted-looking fake historical receipt. Refused malformed interface candidates
are explicit control inputs, not acceptance artifacts.

## White primitives and complete assembly

`WhiteFixture` is {schema:"ri125-fabricated-white-operands-v1",context,
case_id,domain:{r:Int,T:Int,d:Int},strips:StripRows,gram:Gram|null,
n_order:list of allowed n,full_rows:list|null}. `full_rows`, when present, is
exactly eight {row:fixed label,short:Vec(I,2769),long:Vec(I,10961)} records.
It is present for W09,W13–W15,J01,J02, absent (null) otherwise.
W01–W05 use one response with their stated n; W06–W08/W11/W12 are shift-only
(gram=null,n_order=[]); W09/J01/J02 have n_order=[7,6]; W13–W15 use [7].
W10 instead uses the distinct BoundFixture below. The full rows and strips
must be independently reconciled for the complete-row cases. A deliberately
loose Gram error matrix is labeled in the literal case recipe; it is never
claimed to come from an inherited actual row-radius calculation.

`WhiteFixtureResult` has keys schema:"ri125-fabricated-white-primitive-v1",
phase,context,case_id,domain,gram,shift,responses,historical_acceptance,
physical_claim. Domain/gram are exact copies of the validated operand; responses
is the complete ordered list of WhiteResponse, empty for shift-only cases.
No production provenance, accepted input pin or passed RI73 gate is fabricated.
The eventual qualifier constructs this envelope around the pure kernel calls;
the separate validator derives every field with its own parser/arithmetic.

`BoundFixture` is {schema:"ri125-fabricated-bound-operands-v1",context,
case_id:"W10_usefulness_boundaries",pairs:Vec({delta:S,ell:S},4)}.
`BoundResult` has keys schema:"ri125-fabricated-bound-result-v1",phase,context,
case_id,results:Vec({delta:S,ell:S,eps:S,usefulness_state:literal},4),
historical_acceptance,physical_claim.

Full capture framing is the production compact dimensions/row_order/rows
encoding, but has schema **ri125-fabricated-capture-v1** at the footer. The
fixed actual capture pin is forbidden before any row decoding in this route.
`fabricated_white(capture:FileRef,gram:Gram,case_id,context)` is implemented
only for W09/J01/J02 and returns the exact `FabricatedAssembly` object:
{schema:"ri125-fabricated-white-assembly-v1",phase,case_id,context,capture:Pin,
gram:Gram,row_identities:Vec(RowIdentity,8),shift:Shift,
white_responses:[WhiteResponse(7),WhiteResponse(6)],historical_acceptance,
physical_claim}. This is not a production WHITE_COUPLING result and contains
no source/runtime acceptance. Source helper `assemble_white(...,fabricated=True)`
uses the full framing/count/endpoint/resource checks but cannot authenticate
Gram parentage; the independent fabricated qualifier owns that derivation.

## Periodic primitives (executable implementation still pending)

`PeriodicFixture` is {schema:"ri125-fabricated-periodic-operands-v1",context,
case_id,M:4|16384,rows:list of Int,n:Int,p:Int,q:Int,
kind:"rectangles"|"terms",lambda:list of S,dc:list|null,
rectangles:list|null,terms:list|null}.
n is exactly the case recipe value, including 2 and 3 in tiny cases. There are
M/2 modes in increasing k=1..M/2 order and all recorded row labels are retained.
Rectangles mode uses records {k:Int,rows:list of
{row:Int,real:Vec(Int,2),imaginary:Vec(Int,2),alpha:S}}. Integer endpoints are
Q256 fixed-point endpoints. `dc` has exactly the same row records without k;
all its real/imaginary endpoints and alpha are zero in these fixed recipes.
It is retained separately and is not one of the M/2 contributing modes. Terms
is null. In terms mode (P08 only), dc and rectangles
are null and terms is the full ordered list {k:Int,center:S,error_tau:S,
error_alpha:S}. lambda has exactly M/2 entries and is retained even where a
center is zero. P09 produces four independent scenario fixtures with fixed
scenario order. Its 8 DC plus 8*8192 non-DC rectangles retain the stated 65544
complete row/mode records. For each tiny rectangle case and all four P09 cases,
the complete PSD fixture is separately retained as {schema:
"ri125-fabricated-psd-v1",context,case_id,scenario_id:string|null,fs:4096,
M:4|16384,dtype:"<f8",shape:[M/2+1],bins:Vec(canonical float.hex,M/2+1),
raw_array_pin:Pin}. The pin covers all little-endian binary64 bins including
DC and Nyquist. Tiny scenario_id=null; P09 uses its exact four ids. These
fixture bins are explicitly prescribed in CASES.md, never fetched or fitted.
P10 uses the same unit-eigenvalue PSD as P01. P08 is terms-only and has no
claimed reconstructed PSD fixture. The source-only white successor does not
implement these future spectral writers or parse any actual PSD.

`ComponentTerm` is {midpoint:S,radius:S,center:S,error_tau:S,error_alpha:S,
active:bool}. For Nyquist imaginary, active=false and **all five scalars are
zero**, regardless of the saved zero rectangle; no imaginary alpha contribution
is silently included. `ModeTerm` is {k:Int,pair_weight:1|2,lambda:S,rows:list of
{row:Int,real:ComponentTerm,imaginary:ComponentTerm},center:S,error_tau:S,
error_alpha:S,error:S}. For P08, rows=[] explicitly records its component bypass.

`PeriodicFixtureResult` has keys schema:"ri125-fabricated-periodic-result-v1",
phase,context,case_id,M,rows,n,p,q,dc:the complete operand dc record or null,
mode_terms:list of ModeTerm,even:Parity,
odd:Parity,total:{center:S,error_tau:S,error_alpha:S,error:S},raw_marginal:I,
raw_cross:I,factor:S,centered:I,naive_difference:I,
checks:{full_sums_match:true,primary_within_naive:true,width_bound:true},
historical_acceptance,physical_claim. Its full mode/row fields are reconstructed
independently; nothing imports primary expected dictionaries. It has no actual
source_identity, retained_final_trace or claimed physical adequacy. P09 wraps
four such results in {schema:"ri125-fabricated-four-periodic-v1",phase,context,
case_id,scenario_order:fixed list,scenarios:Vec({id:fixed,result:PeriodicFixtureResult},4),
historical_acceptance,physical_claim}. Primary negative endpoints are retained.

## Nuisance and join primitives (executable implementation still pending)

`NuisanceResult` is {schema:"ri125-fabricated-nuisance-result-v1",phase,context,
case_id,kind:"constant_mean"|"nonconstant_mean"|"calibration_constant"|
"covariance_error"|"calibration_error",output_means:list of S,
population_mean_energy:S|null,covariance_energy:S|null,total_energy:S|null,
model:S|null,truth:S|null,absolute_difference:S|null,bound:S|null,
historical_acceptance,physical_claim}. N01 has output_means=[0,0],
population_mean_energy=0,covariance_energy=total_energy=3/2, other optional
fields null. N02 has [-4,-12,-20],128/3,16/9,400/9 respectively. N03 has
output_means=[-1], with all optional fields null. N04/N05 have output_means=[];
the three energies are null, model/truth/difference/bound are the literal
CASE values (1,2,1,1 and 1,4,3,3). These are exact primitive results, not
nominal strain measurements. Future sign enumeration retains every sign result
in separate typed fixture artifacts and checks those exact aggregates.

`FabricatedJoinOperands` is {schema:"ri125-fabricated-join-operands-v1",context,
case_id,white:FabricatedAssembly,periodic:FabricatedFourPeriodic,
historical:list of {id,starts,n,rows,energy:{U:I,M:I,V:I},trace:{id,interval:I,
source_identity:Pin,model:"fabricated_comparison_only",units:"fabricated_units"}}}.
The pins refer only to explicit fabricated bodies. `FabricatedJoinResult` is
{schema:"ri125-fabricated-join-result-v1",phase,context,case_id,
status:"conditional_comparison_complete"|"conditional_comparison_precision_inconclusive",
scenarios:list of {id,starts,n,rows,historical:the complete input record,
unit_white:{kappa:I,usefulness_state:literal,sigma2:null,b_mu:null},
periodic_stress:{interval:I,label:"fabricated_hypothetical_completion"}},
nuisance_premises:the unchanged CONTRACT nuisance object,
historical_acceptance,physical_claim}. This separate join never uses phase
fixed_saved_application. Its production counterpart's strict guards remain.
