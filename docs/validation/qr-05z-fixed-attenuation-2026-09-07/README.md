# QR-05Z protocol: fixed attenuation of supported forecasts

7 September 2026. Prospective specification before Z case outcomes.
Base: pushed Y commit 67468abfa9fc8e20622651f0cb1fb33ac1e903d5.

## Scope and question

Keep Y's six experiments,482 positive histories,H2,K3,Q3 and four ordered
actual/assumed levels [0,1/2,3/4,1]. Pin Y results.json:
16,474,309 bytes, SHA256
c4189b0f1bb0df4bb3e5f14c1969ede0ee754f59b4bc99e89aeac8d6b065891f.
Y plus its29 immutable prior artifacts gives30 producer artifacts.

For each history/report/assumed model let f be Y's completed forecast:
the assumed conditional future law when assumed report mass is positive,
otherwise the supplied current-N-prefix fallback g. Exact zero selects
fallback, not an epsilon. Keep one g table shared across every setting.
Compare exactly THREE fixed retained-detailed weights a=[0,1/2,1]:

    h_a = (1-a)g + a f.

Zero is coarse-only,one is Y. Apply every rule independently of actual
noise index, hidden current state, replacement coin and future outcome.
No fitted weights, actual-index selection, adaptive threshold, retrospective
winner, new noise setting or optimized policy. This gate adds the midpoint
tradeoff and its complete-law certificate, not new endpoint findings.

Y's original W family is unflagged, non-disturbing uniform replacement
within each whole-model current NMT alphabet:
C_t(z|b)=(1-t)1[z=b]+t/|A_N|. The current N prefix is
[frame,N0,N1,N2,N3], not a prefix of the future Q3 question. All physical,
apparatus, empirical and calibration premises remain outside this gate.

## Exact identities and prospective boundaries

Score EVERY mixed forecast, including both endpoints and fallback cells,
under the original actual conditional future law p and report mass w.
For unscaled Brier loss L(h;p)=1-2<p,h>+||h||²,
regret=L-R(p)=||p-h||² and R(p)=1-||p||².
Retain complete sparse mixed laws; absent coordinates are zero, but strictly
positive midpoint atoms cannot be pruned. Endpoints omit exactly-zero atoms.

For D=||f-g||², keep the exact cell identity and its original-weight versions:

    L(h_a;p) = (1-a)L(g;p)+a L(f;p)-a(1-a)D,
    gain_over_coarse(a) = a gain_over_coarse(1)+a(1-a)D,
    gain_over_base(a) = L(f;p)-L(h_a;p)
                     = gain_over_coarse(a)-gain_over_coarse(1).

Here base means the completed Y policy, never an incomplete X score.
D,risk,regret are in[0,2]; signed gains in[-2,2]. Inputs and every retained
rational component are bounded to4096 bits; unretained intermediates may
exceed that and cancel. Check normalization, complete-law zero-regret
equivalence, both exact endpoints, the quadratic identities, and Jensen's
risk upper bound by the endpoint average. Jensen does not guarantee that
the midpoint beats either endpoint. No sign or strict improvement is required.

Fallback-used cells have f=g, so D=0 and all three forecasts/risks coincide.
Generic fallback regret may be positive and must remain so. Neither mixed
forecasts nor their actual-weight marginal are required to equal the actual
future law: forecasts are decision rules, not actual observation channels.

Preserve the ENTIRE Y analysis, including all nested X nulls, support,
forecasts, scores, counts and witnesses, as an explicit baseline. All report
and history aggregation uses ORIGINAL positive actual probabilities, without
renormalization. Do not pool the six cases. Totality is confined to the
declared report union, not arbitrary unseen apparatus reports.

For W specifically, actual full replacement gives p=g. Hence
gain_over_coarse(a)=-a² D, before and after weighting. Nonzero retention can
remain harmful; uniform dominance over coarse-only is not an acceptance
criterion. At correctly specified actual/assumed levels f=p, mixed regret
equals (1-a)²D. At assumed full replacement f=g, all blends coincide.
These are predicted family controls, not empirical robustness discoveries.
The generic API must not enforce them for arbitrary supplied experiments.

## Public standalone API and strict native contract

analyze(problem) accepts exactly
{schema_version:"det8-qr05z-problem-v1",
 family:"qr05z_fixed_attenuation",experiment:<Y problem>}.
No additional weights, selector, artifact path or metadata fields are accepted.
The embedded experiment has exactly
{schema_version:"det8-qr05y-problem-v1",
 family:"qr05y_explicit_fallback",beliefs:[...]}.

Each belief is exactly {belief_id,weight,channels,fallbacks}; contiguous IDs
start at zero and positive likelihood weights sum to one.
There are four ordered channels {level,cells} at[[0,1],[1,2],[3,4],[1,1]].
Cells are {value,probability,prediction}, sorted unique by report value.
Report values are seven-component native nonnegative integers <=64 bits.
Each prediction is a sorted unique nonempty list of {value,probability},
with seven-component future values under the same integer rule.
All sparse probabilities are strictly positive; each cell law and channel
report law sums to one. Channels share the complete unconditional future
marginal within a belief. Fallbacks are sorted unique {value,prediction}
with five-component prefix keys EXACTLY covering the report-prefix union
over all four channels, including keys unused in a particular comparison.
Their laws need not equal actual conditional laws and may add future symbols.

All fractions are reduced native[n,d],d>0,each component<=4096 bits.
Input probabilities satisfy0<=n<=d; sparse masses and weights are positive.
Reject bool/subclass coercion, floats, strings/tuples, missing/extra fields,
duplicate/unsorted support, normalization repair and implicit defaults.
Native JSON tree/DAG checks on the OUTER wrapper precede serialization:
root depth zero (including scalar leaves),depth<=128,expanded value
nodes<=8388608 (object keys not nodes),expanded sorted ASCII JSON+newline
bytes<=128MiB. Reject cycles/explosive sharing; accept benign shared containers.
No mutable result cache; outputs detached from inputs and other calls.

Carry each route's own Y validator/scorer statically in its Z source file,
without runtime imports of Y or the other route. Reuse of source lineage is
declared, not an independent rederivation of the Y mathematics. The complete
Y baseline is recomputed locally, not accepted as an unvalidated input.

Inherited live caps (same names/values in both cores):
MAX_BELIEFS=512, MAX_CELLS_PER_CHANNEL=4096,
MAX_ATOMS_PER_PREDICTION=4096, MAX_INPUT_CELLS=32768,
MAX_INPUT_PREDICTION_ATOMS=2097152, MAX_FALLBACKS_PER_BELIEF=16384,
MAX_INPUT_FALLBACKS=32768, MAX_INPUT_FALLBACK_ATOMS=2097152,
MAX_PAIR_CELLS=131072, MAX_SCORING_TERMS=33554432,
MAX_BITS=4096, MAX_DEPTH=128, MAX_NODES=8388608, MAX_BYTES=134217728.

New live caps:
MAX_BLEND_CELLS=393216, MAX_BLEND_ATOMS=8388608,
MAX_TOTAL_WORK_TERMS=167772160.

Plan all new structural/work counts from validated input BEFORE ANY Y or Z
forecast-scoring loop. A pair cell has actual law p, chosen Y law f and g.
For each of the three weights, explicitly traverse BOTH f and g when
constructing the mixture, even at endpoints; count len(f)+len(g).
Retain positive union support at1/2, exactly g support at0, f support at1.
Distance work is len(f)+len(g) ONCE per pair cell. Every blend is rescored,
with len(p)+len(h_a) score visits. Both cores must use linear support loops,
not uncounted quadratic outcome-coordinate loops. Independent tests/audit
may use literal outcome-coordinate sums.

total_work_terms=Y completed_scoring_terms+Y coarse_scoring_terms
                 +mixture_terms+distance_terms+blend_scoring_terms.
Enforce all planned caps before score loops, and compare executed counts.
No truncation or post-outcome cap adjustment. Full canonical output<=128MiB;
exclusive final capture<=64MiB. Core output retains the full Y baseline but
does not redundantly repeat its actual/endpoint laws inside each Z blend.

## Exact output wire

Output exactly
{input_sha256,levels,retained_weights,baseline,beliefs,aggregate,witnesses,counts}.
input_sha256 hashes the whole validated OUTER wrapper using compact sorted
ASCII JSON plus newline. levels are the four noise fractions; retained_weights
are exactly[[0,1],[1,2],[1,1]]. baseline is the complete unchanged Y output,
whose own input_sha256 hashes the inner experiment.

beliefs is [{belief_id,weight,pairs}], same IDs/weights/order as baseline.
Each pairs list is16 row-major actual/assumed settings (actual outermost).
A Z pair is exactly
{actual_index,assumed_index,cells,forecast_distance,blends,checks}.
Cells match the corresponding baseline cell order and report values exactly.
A Z cell is exactly {value,forecast_distance,blends}.
Actual laws/masses, Y/coarse forecasts and fallback flags are in the matching
baseline cell; no information is dropped from the complete output.

forecast_distance is D at cell level and original-report-weight expected D
at pair level. Cell blends are ordered exactly by retained_weights and are
{retained_weight,forecast,forecast_risk,regret,gain_over_coarse,gain_over_base,
 predictions_equal}.
forecast is the complete positive sparse mixed law; predictions_equal means
equality with the complete actual law, not agreement with another forecast.
All cell scores are conditional, not report-weighted.

Pair blends are exactly
{retained_weight,forecast_risk,regret,gain_over_coarse,gain_over_base}.
They use original actual report weights. checks has exactly eight true fields
after verification:
{normalization,score_decomposition,quadratic_risk_identity,
 quadratic_gain_identity,endpoint_recovery,fallback_preserved,
 zero_regret_iff_equal,jensen_bound}.
These cover all three cell laws and weighted scores, exact0/1 endpoint laws
and scores, both gains, unchanged fallback cells and zero regret iff all
positive-weight actual future laws match. No assumed nonnegative gain.

aggregate={total_weight:[1,1],pairs}; aggregate pairs are the same as Z pairs
EXCEPT cells. Scores and forecast_distance use original history weights;
retained_weight is an identifier, not weighted/averaged. The same eight checks
apply to the complete positive-weight collection.

counts exactly
{beliefs,pair_cells,blend_cells,blend_atoms,mixture_terms,distance_terms,
 blend_scoring_terms,baseline_scoring_terms,total_work_terms,
 positive_deviation_beliefs,positive_regret_beliefs,
 better_than_coarse_beliefs,equal_to_coarse_beliefs,worse_than_coarse_beliefs,
 better_than_base_beliefs,equal_to_base_beliefs,worse_than_base_beliefs}.
beliefs,blend_atoms,and all five work counts are scalars.
pair_cells and positive_deviation_beliefs are length16.
blend_cells and the seven regret/comparison lists are length48, indexed
12*actual_index+3*assumed_index+blend_index. Counts refer to actual retained
or evaluated objects, not extrapolations. Baseline detailed counts stay nested.

witnesses exactly
{first_positive_deviation,first_positive_regret,first_better_than_coarse,
 first_equal_to_coarse,first_worse_than_coarse,first_better_than_base,
 first_equal_to_base,first_worse_than_base}.
First-positive-deviation is length16; others length48. Each entry is the
first matching belief ID or null, using original-weight belief-level scores.
Equal risk need not mean equal laws; retain both distinctions.

## Verification and publication

Primary: sparse quadratic score and direct weighted-vector mixture.
Reference: independent expected loss and its own mixture/deviation loops,
with separately carried Y lineage. No cross-imports. Root runner pins Y plus
30-artifact lineage, compares entire baseline to Y and independently verifies
all Z laws/scores/output. Full source native/canonical comparisons distinguish
bool from int. No previous public APIs are replayed.

Separate JSON-only stdlib audit carries its own Y/X/W raw-law reconstruction,
including induced subsets,Mobius/H,local rows,K3,lifetime histories and N/noisy
conditional laws. It rebuilds the complete Y baseline and Z output from raw
evidence. Authenticate seven sources each for Z,Y,X and six for W,plus30 prior
artifacts, before/after. Source content is bytes for identity only; no executor,
runner or test imports. Inherited polynomial digest remains producer identity,
not a new polynomial derivation or broader operator/minimality certificate.

Tests: all six complete case wires; fair truth between opposed forecasts
(midpoint can beat equal-risk endpoints); coarse-correct but harmful detailed
forecast; correct detail shrunk toward wrong coarse; positive generic fallback
regret unchanged at every blend; extra future atoms and exact endpoint pruning;
uneven report/history weights; multi-prefix fallback; tiny-positive support;
full-law versus scalar equality; no actual-index-dependent chosen law;
strict wrapper/inner native fields, all live caps, bounded normal/-O explicit
guard subprocesses, retained-bit overflow versus internal cancellation,
DAG accounting, ownership and nonvacuous output/producer corruptions.

Freeze seven files:
README.md,attenuation.py,reference_qr05z.py,study.py,test_qr05z.py,
test_capture.py,audit_json.py. Complete a create-only external preflight and
audit before final freeze if useful. Then full normal/-O tests with isolated
Python and fresh external bytecode caches, exclusive results.json capture,
fresh exact read-only normal/-O replays and final audit. Verify identities
throughout; disclose corrections. RESULTS.md and roadmap are outside the
frozen ledger. Publish only Z research files/roadmap, preserving other work.

No Z case outcomes have been computed at protocol creation. No fitting,
sensor calibration, empirical validation, RET integration, Lean proof,
ontology, new physical law, metric reconstruction or gravity correspondence.
