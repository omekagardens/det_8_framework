# QR-05AE protocol: history-level safety diagnostic

7 September 2026. Prospective specification before any AE fixed coefficient,
history-risk decomposition or outcome. Base: pushed AD commit
070f4795ddf48513839a1e85f3121681c943c645.

## Scope and frozen evidence

Pin AD results.json: 5,003,206 bytes, SHA256
099c9df18db91545fdd3a08a383e2e4ed96bf5734f6b80a9e492c3bc954c611a.
AD plus its34 priors gives35 immutable producer artifacts. Keep all six
experiments,482 original positive-weight histories, H2/K3/Q3, four levels
[0,1/2,3/4,1], finite actual sets t<=u, frozen forecasts, complete AD
point/whole-interval policies and its canonical common witness mechanisms.
History counts77,77,78,78,86,86 are prior metadata, not AE outcomes.

Do not reoptimize any policy, choose a convenient interval representative,
change history weights, or select a replacement mechanism per history.
This diagnoses the PARTICULAR retained global witnesses. A witness
maximizing aggregate risk need not maximize individual-history risk; other
tied aggregate-maximizing mechanisms can redistribute local harm. Absence
of harm here is NOT robustness over the whole replacement simplex.

For history H, assumed s, actual t and its fixed common witness, define
the CONDITIONAL-history excess polynomial

    Q_H,s,t(a) = A_H,s,t a^2 - 2 B_H,s,t a.

History weight w_H is NOT inside these conditional coefficients. Producer
uses report-mass conditional-vector squared distances/cross products.
Auditor uses literal actual-outcome indicator expansion against the
conditional-H unnormalized joint J_H,t(z,q), whose total mass is1:

    A_H = sum_(z,q) J_H,t(z,q) sum_k (f_s(z,k)-g(z,k))^2
    B_H = sum_(z,q) J_H,t(z,q)
                sum_k (I[q=k]-g(z,k))(f_s(z,k)-g(z,k)).

Then sum_H w_H(A_H,B_H) MUST equal AD's complete actual-world coefficients.
No fitting to alpha samples, pooled cases, double history weighting or
replacement of conditional risk by its weighted case contribution.

## Generic diagnostic API

Two independent stdlib engines export analyze(problem). Input exactly:

    {schema_version:"det8-qr05ae-problem-v1",
     family:"qr05ae_history_safety",
     levels:[[0,1],[1,2],[3,4],[1,1]],
     histories:[{belief_id,weight}],
     profiles:[{assumed_index,actual_index,
                coefficients:[{quadratic_coefficient,half_linear_coefficient}]}],
     decisions:[{assumed_index,bound_index,policy}]}

Histories:1..128, belief_id exactly0..H-1, positive weights<=1 summing to1.
Exactly16 profiles ordered s outer/t inner; exactly H coefficient rows
aligned to histories. A in[0,2], B in[-2,2]. Exactly16 decisions ordered
s outer/u inner. policy is exactly {kind:"point",weight:a},0<=a<=1, OR
{kind:"interval",lower:[0,1],upper:[1,1]}. No other intervals or fields.

All inputs use exact native JSON types, native indices (not bool/subclass)
and reduced native fraction pairs with positive denominator and4096-bit
components. The generic API diagnoses SUPPLIED polynomials and a SUPPLIED
policy. It authenticates neither Brier realizability, policy optimality,
laws, history origin nor robustness of a mechanism class. Harmful aggregate
or conditional outcomes are valid generic results, never rejection grounds.

## Shared-alpha sign partition and decomposition

For point policies retain a single point stratum at the supplied a.

For interval policies, independently for each (s,t) profile, form the
complete sorted distinct knot list {0,1} plus roots2B_H/A_H only when
0<2B_H<A_H. Never form an outside, endpoint or irrelevant ratio. Retain
one root record for EACH eligible history (including duplicate roots),
in history order, and deduplicate only the knot list.

Include a singleton at EVERY knot, plus EVERY intervening open interval,
ordered point0,open,point,...,point1. There is no sampled midpoint or
selected interval policy. All worlds/histories share the same symbolic a,
though their sign partitions may differ; no joint simultaneous-world
claim is inferred from separate existential summaries.

Factorization Q_H=a(A_H a-2B_H) proves signs on open strata. Handle flat
A=B=0, signed linear A=0/B!=0, B=0/A>0 and endpoint root2B=A explicitly.
An aggregate-polynomial zero is NOT a new history sign-change knot.

Each stratum retains complete positive/negative/zero history-index sets,
their original-weight likelihood masses and their weighted coefficient
subtotals. Separate probability mass from risk contribution.

    P(a)=sum_positive w_H Q_H(a)
    N(a)=sum_negative w_H Q_H(a)       (SIGNED, nonpositive on this stratum)
    Z(a)=sum_zero w_H Q_H(a).

Retain ALL THREE group polynomials. At a singleton, Z can have NONZERO
coefficients despite Z(a)=0. P+N+Z equals the aggregate coefficientwise
everywhere. On an open stratum Z is identically zero. At each point,
P>=0,N<=0,Z=0 and aggregate=P+N; benefit magnitude is -N.
Positive weights make nonempty sign sets equivalent to positive group mass.

No per-history weighted scalar contribution is retained: w_H Q_H is an
internal product. Conditional Q_H values, group polynomials/masses,
point group values and aggregate values ARE retained and bit-checked.
Intermediate products/sums may exceed4096 bits and cancel exactly.

## Resource and work contract

Live caps in both engines:
MAX_BITS=4096, MAX_DEPTH=128, MAX_NODES=2097152,
MAX_BYTES=33554432, MAX_HISTORIES=128, MAX_PROFILES=16,
MAX_DECISIONS=16, MAX_WORLD_CERTIFICATES=40,
MAX_ROOT_DIVISIONS=2048, MAX_STRATA=4096,
MAX_MEMBERSHIPS=524288, MAX_POINT_EVALUATIONS=600000,
MAX_TOTAL_WORK=2000000.

Native preflight before whole serialization: root-zero depth including
leaves; expanded value nodes excluding keys; exact ensure_ascii canonical
bytes plus newline; early width/string/depth guards, benign-DAG memoization,
cycle/exponential-expansion rejection. Detached outputs, no mutable
cross-call cache. Each engine may statically carry ONLY its own native
guard lineage. This is a new API, not a replay of old admission boundaries.

Parse ALL schemas and normalization first. Fixed labels give40 decision-
world certificates. Let P be point-policy world occurrences,J=40-P.
Let R be profiles used by at least one interval world, and i_p the number
of eligible interior-root histories in each such profile. Comparisons and
multiplication by2 for root classification are permitted planning work;
NO root division, risk evaluation, coefficient aggregation or group work
occurs before ALL reservations/caps.

Conservatively reserve using root MULTIPLICITY before division/dedup:

    I = sum_(distinct interval-used profiles p) i_p
    Sr = P + sum_(interval world occurrences using p) (2 i_p + 3)
    Tr = P + sum_(interval world occurrences using p) (i_p + 2)
    Or = Sr-Tr
    Mr = H Sr
    Er = (H+4) Tr
    Wr = (16+R)H + I + 2H Sr + 4Tr + Sr + 40.

Reserve root divisions I, strata Sr, memberships Mr, point evaluations Er
and total work Wr against the respective caps. Reservations are deliberate
upper bounds; duplicate roots may shrink execution. Do not retroactively
admit an input whose conservative reservation exceeds a cap.

After planning, compute each eligible history's root ONCE per distinct
interval-used profile, not per repeated bound/world occurrence. Every new
retained root, group coefficient/mass and scalar has reduced4096-bit
components. Generic Q and aggregate values lie in[-4,6]; P in[0,6],
N in[-4,0], benefit magnitude in[0,4]. All profile/group A in[0,2],
B in[-2,2]. Producer Brier excesses additionally lie in[-2,2].
Groups of empty histories have mass and both coefficients zero.

Nonpublic hooks:
_root(A,B)->2B/A for eligible histories only;
_profile_term(w,A,B)->(wA,wB), UNRETAINED internal products;
_evaluate(A,B,a)->Aa^2-2Ba, retained range[-4,6];
_open_sign(A,B,lower,upper,root)->native -1/0/1, no alpha sample;
_accumulate(group,w,A,B,value)->updated four-tuple
(mass,quadratic_sum,half_linear_sum,point_sum), where value is None on
open strata; products/intermediate accumulator entries are UNRETAINED.
All these hooks follow the complete reservation. Classification planning
uses only parsed inputs; other scalar validation/copy/identity operations
are outside the following declared visit inventory, not claimed CPU cost.

Executed named counts:
profile_aggregation_terms=16H, root_classification_terms=RH,
root_divisions=I,
history_point_evaluations=HT, group_point_evaluations=3T,
aggregate_point_evaluations=T, open_sign_classifications=HO,
group_accumulation_terms=HS, stratum_certifications=S,
world_certifications=40,
total_work_terms=(16+R)H+I+2HS+4T+S+40.
Here actual S/T/O use DEDUPLICATED roots, T point strata, O open strata.
All named visits count even zero coefficients/empty groups/tied roots.
Actual work must not exceed reserved work.

## Complete generic output

Exactly {input_sha256,levels,histories,profiles,decisions,counts}.
Hash canonical input ensure_ascii bytes plus newline; labels/histories
are detached exact copies.

Each profile exactly:
{assumed_index,actual_index,aggregate_polynomial,
 interval_root_records,interval_knots}.
A polynomial is exactly {quadratic_coefficient,half_linear_coefficient}.
For a profile not used by an interval world both interval fields are null.
Otherwise root records are [{history_index,weight}], in history order,
and interval_knots is the sorted distinct0/roots/1 list. Empty root records
are not null for an interval-used profile.

Each decision exactly:
{assumed_index,bound_index,policy,worlds,harm_possible_world_indices,checks}.
worlds contains every original t<=u in order.
Decision checks exactly true after verification:
declared_worlds_complete,shared_policy_preserved,no_historywise_selection.

Each world exactly:
{actual_index,profile_index,strata,potentially_harmed_history_indices,
 potentially_benefited_history_indices,all_policy_weights_history_safe,checks}.
The two index lists are sorted unions across strata; safety means no positive
history in ANY stratum at this world under this mechanism/policy set.
harm_possible_world_indices keeps exactly worlds with nonempty positive union.
These are separate per-world existential summaries, not a chosen alpha
simultaneously harming every listed world/history.
World checks exactly true:
policy_domain_covered,all_history_strata_preserved,no_policy_reoptimization.

Each stratum exactly {region,groups,point_values,checks}.
region is {kind:"point",weight} OR {kind:"open_interval",lower,upper}.
groups has exactly positive,negative,zero, each exactly
{history_indices,likelihood_mass,polynomial}.
point_values is null on open strata; otherwise exactly
{history_excesses,positive_contribution,negative_contribution,
 zero_contribution,aggregate_excess,benefit_magnitude}.
history_excesses is every conditional-history Q in original order.
All groups' coefficients/masses must sum to the profile aggregate/one.
Point values are checked both by group polynomial evaluation and direct
weighted conditional-risk addition. Do not claim a coefficientwise P+N
identity at singleton zero crossings without Z.
Stratum checks exactly true:
complete_sign_partition,constant_sign_on_region,original_weight_masses,
weighted_polynomial_decomposition,point_or_parametric_decomposition.

counts exactly:
histories,profiles:16,decisions:16,world_certificates:40,
point_world_certificates:P,interval_world_certificates:J,
interval_profiles:R,interior_root_candidates:I,
distinct_interior_roots:<sum unique root counts across interval-used profiles>,
strata:S,point_strata:T,open_strata:O,history_memberships:HS,
reserved_strata:Sr,reserved_point_strata:Tr,reserved_open_strata:Or,
reserved_history_memberships:Mr,reserved_point_evaluations:Er,
reserved_total_work_terms:Wr,
plus EVERY executed named count above including total_work_terms.

## Producer suite and independent authentication

Suite exactly {producer,cases,independent_route_equal,public_controls,totals}.
producer={artifact:"qr-05ad-continuous-retention-2026-09-07/results.json",
bytes:5003206,sha256:<pinned AD>}.
Each case exactly {case_id,problem,analysis,baseline,producer_controls}.
baseline is a detached EXACT copy of the entire AD case, retaining all old
AC/AA failures, forecasts, policies, mechanisms and world certificates.

Derive all16 conditional-history profile tables from the common witness
laws and frozen endpoint forecasts, not from aggregate AD coefficients.
Check every original history weight/ID, forecast law and witness channel.
Authenticate the full baseline mathematically using carried independent
oracles; no prior engine/runner is imported.

Every weighted profile must match AD's all-four-world polynomials. Every
point-policy world aggregate must match AD's complete actual excess vector
and bound minimum. Interval-world aggregate polynomials retain AD's
whole-family inequalities and upper zero polynomial.
Independently literally rescore each history at EVERY unique (s,t,a)
appearing in a point stratum (including all interval knots); cache only
within one call. This enumerates proof boundaries, not policy choices.
Open strata follow complete factorization/root proofs, never midpoints.
The raw auditor independently reconstructs all generic output and the
complete baseline/suite through its own raw-history chain.

True producer controls exactly:
AD_baseline_preserved,original_history_weights,
common_witness_and_policy_preserved,complete_conditional_history_coefficients,
coefficients_aggregate_to_AD_world_polynomials,literal_history_point_scores,
complete_history_sign_partitions,interval_policies_not_point_selected,
harm_benefit_cancellation_visible,case_average_certificates_recovered,
no_historywise_weight_or_mechanism_selection.
False fields exactly:
origin_authenticated_by_generic_API,all_replacement_mechanisms_audited,
historywise_robustness_established,raw_history_reconstruction_performed_by_this_runner.

public_controls exactly:
{analyze_calls:12,invalid_analyze_calls_rejected:16,
 raw_laws_or_prior_artifacts_given_to_core:false,
 policy_reoptimized:false,mechanism_reoptimized_per_history:false,
 interval_representative_selected:false,whole_replacement_class_audited:false}.
totals={cases:6,analyze_calls:12,invalid_analyze_calls_rejected:16,
 plus sums of EVERY scalar analysis counts field}. No pooled risk.

## Verification, interpretation and next boundary

Seven frozen files: README.md,safety.py,reference_qr05ae.py,study.py,
test_qr05ae.py,test_capture.py,audit_json.py.
Raw auditor imports no engine/runner/test; statically carry own AD chain.
Authenticate35 priors +7 sources each AE/AD/AC/AB/AA/Z/Y/X +6 W =97
source/prior identity targets before/after, plus current capture identity.
Inherited polynomial identities are not new derivations; old public APIs,
runtime counters and broader operator/minimality claims are not replayed.

Hands precede fixed outcomes: aggregate zero hiding positive/negative
history risks, unequal weights, shared alpha versus per-history optimizing,
2B/A versus B/A, duplicate/near roots, all singleton ties, endpoint and
double roots, signed linear/flat histories, nonzero singleton-zero-group
polynomial, aggregate roots omitted from history partition, every cap
before hooks, conservative duplicate-root reservations, output/native
DAG/depth/bytes/ownership, retained root/group overflow despite aggregate
cancellation and accepted oversized cancelling internal products.
Corruption tests must be nonvacuous and check whole outputs, input
coefficients/weights, baseline identity, complete partitions and case links.
Normal/-O guard subprocesses use explicit exceptions, not assertions.

First fixed complete comparison only after protocol/two cores/runner exist
and hands pass, with4 source identities and35 priors before/after.
Then exclusive external preflight/full raw audit, freeze7 sources,
isolated normal/-O tests with fresh external caches, exclusive results.json,
fresh read-only exact replays and final full raw audit.
Capture/suite caps remain64MiB/128MiB. Publish only AE research files and
roadmap; preserve unrelated RET/core/governance work. RESULTS.md/roadmap
stay outside the frozen source ledger.

Report positive, zero and negative history outcomes without rewriting
the old aggregate guarantees. This gate is a bounded diagnostic under fixed
witnesses, NOT full-class history robustness, empirical safety, calibration,
RET integration, a geometric reconstruction, new physics or ontology proof.
After AE, prepare the small supplied-geometry interface/protocol, possibly
inside the first resumed geometry gate; do not automatically add further
forecasting optimization gates. No AE outcomes exist at protocol creation.
