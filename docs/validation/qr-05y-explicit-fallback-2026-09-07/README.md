# QR-05Y protocol: explicit N-forecast fallback

7 September 2026. Prospective specification fixed before Y case outcomes.
Base: pushed X commit de4bfb06a2f0d6715d0ff6f4cd7a4cd7c514bbb0.

## Scope and dependencies

Keep X's six experiments, 482 current histories, H2 beliefs, K3, complete Q3
and four actual/assumed readout levels unchanged. Pin X results.json:
8,842,933 bytes, SHA256
1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4.
X plus its 28 immutable prior artifacts gives 29 producer artifacts.
W's deterministic N-conditional laws supply the explicitly declared fallback.

This is a forecast-completion policy gate. It does not retroactively fill
X's undefined scores or change any physical/observation law. For W,
N=[frame,N0,N1,N2,N3] is the current report prefix, not the future Q3 prefix.
The fixed whole-model NMT alphabet and non-disturbing unflagged replacement
C_t(z|a)=(1-t)1[z=a]+t/|A_N| remain as in W, with t=0,1/2,3/4,1.
Replacement is independent of fresh K3 given H2; its coin is not observed.

## Declared policy and actual-law scores

For each current history supply ONE fallback table g_N, shared across every
actual and assumed experiment. Given assumed index j and received report z,
use f_j(z)=p_j(.|z) if assumed report mass w_j(z)>0, otherwise g_prefix(z).
The rule depends on the assumed model, report and declared history/fallback,
not on the actual level i, hidden current class or future outcome.
Exact zero, not a numerical threshold, determines the branch.

For actual conditional law p_i(.|z), score the chosen forecast and the
coarse-only comparator g_prefix(z) under the SAME actual report/future law.
Brier(f;p)=1-2<p,f>+||f||^2=R(p)+||p-f||^2.
Bayes risk R(p) is in [0,1]; forecast risk and regret are in [0,2].
Sparse future atoms absent in one law mean exact zero over the union.
A fallback may assign probability to future symbols missing from the actual
or assumed sparse laws; the generic scorer must include those coordinates.

Preserve X coverage, unsupported mass, full Bayes risk, supported Bayes/risk/
regret contributions and original full forecast risk/regret/complete flag.
Original full scores remain null unless X coverage is one. Supported
forecasts and their actual-weighted contributions are unchanged.

Separately retain fallback Bayes/risk/regret contributions, using ORIGINAL
actual weights, not normalized fallback weights. Completed policy risk is
supported_forecast_risk+fallback_forecast_risk; completed regret is
supported_regret+fallback_regret. Full Bayes risk is supported+fallback
Bayes contributions. Verify both completed and coarse risk decompositions.

gain_over_coarse=coarse_forecast_risk-completed_forecast_risk
                =coarse_regret-completed_regret.
This is SIGNED in [-2,2], not guaranteed nonnegative. On fallback-used cells
the two forecasts coincide, so local gain is zero. All aggregate gain comes
from supported cells, giving |gain_over_coarse|<=2*coverage.
Zero regret iff complete future laws agree; equal scalar risks do not suffice.

Aggregate each pair with the original positive history likelihoods. Retain
all probability mass; never renormalize reports or histories. Do not pool
the six cases. The completed rule is total on the declared report union,
not on arbitrary unseen apparatus outputs.

## Preregistered consequences and limits

On fixed W, an unsupported report under a clean assumed model has zero
clean-label probability inside N. Under positive actual replacement its
likelihood is constant across current states in that fiber, hence its
actual current posterior and future law are exactly N-conditional.
Thus the declared fallback is Bayes-correct on those missing reports:
fallback_regret=0; completed_regret=X supported_regret;
completed_risk=X supported_forecast_risk+X bayes_risk-X supported_bayes_risk.
Verify complete posterior/future-law equality, not just this scalar identity.
These are predicted family consequences, not a new robustness discovery.

Any X-complete pair uses no fallback and matches X's full scores. Diagonals
remain Bayes-correct. On W the coarse-only risk equals W's N risk for every
actual level. Supported misspecified forecasts may still make the completed
rule worse than N-only; preserve negative gains and all witnesses.
No particular improvement, sign, threshold or witness existence is required.

Generic shared future marginals do NOT certify W noise or make g_N a true
N-conditional law. In the generic API this is a supplied prefix-grouped
forecast. It can have positive fallback regret, and its coarse-only risk
can vary with actual level. Include non-W countercontrols for both facts.
Do not infer fallback optimality or empirical calibration.

## Public exact API

analyze(problem) accepts exactly
{schema_version:"det8-qr05y-problem-v1",
 family:"qr05y_explicit_fallback",beliefs:[...]}.
Each belief is {belief_id,weight,channels,fallbacks}.
IDs are contiguous from zero; positive history weights sum exactly to one.
channels retain X's exact four ordered {level,cells} inputs at
[[0,1],[1,2],[3,4],[1,1]]. A cell is {value,probability,prediction}.
Report values are sorted unique seven-component nonnegative native integer
vectors with components <=64 bits; positive cell masses sum to one.
Prediction is a sorted unique nonempty list of {value,probability}, with
seven-component future vectors and positive probabilities summing to one.
Each channel has the same complete unconditional future marginal per belief.

fallbacks is a sorted unique nonempty list of {value,prediction}; value is a
five-component prefix vector with the same native 64-bit component rule.
Keys must EXACTLY cover the union of report prefixes across all four
channels, including entries unused by a particular pair. No extra/missing
keys, implicit defaults or posterior repair. Fallback predictions follow
the same future-law schema. They need not equal an actual conditional law.

Input fractions are native reduced [n,d], 0<=n<=d,d>0, each component <=4096
bits. Sparse probabilities and weights are positive; zero=[0,1],one=[1,1].
Reject bool/subclass coercion, floats, tuple/string fractions, unknown or
missing fields, unsorted/duplicate support and normalization repair.
All retained rational components are <=4096 bits. Internal arithmetic may
temporarily exceed that limit and cancel; only inputs/retained values are
bit-bounded. Signed retained gain fractions permit -2<=n/d<=2 and reduced
positive denominator. Other score fractions remain nonnegative.

No mutable result cache. Outputs detached from input and other calls.
Native tree/DAG checks precede serialization: reject cycles, depth>128
(root depth zero including scalar leaves), expanded value nodes>8388608
(keys are not nodes), expanded exact sorted ASCII JSON+newline>128MiB.
Accept benign shared containers and count their expanded occurrences.

Caps: beliefs1..512; cells/channel1..4096; atoms/prediction1..4096;
fallbacks/belief1..16384; total input cells<=32768;
total channel prediction atoms<=2097152; total fallbacks<=32768;
total fallback prediction atoms<=2097152; retained pair cells<=131072.
Evaluate BOTH chosen-policy and coarse-only scores for EVERY pair cell.
Completed scoring terms count len(actual law)+len(chosen law); coarse terms
count len(actual law)+len(coarse law). Planned sum<=33554432 before score
loops, and executed counts must agree. No uncounted quadratic loops in the
cores; independent audit/tests may use literal outcome-coordinate sums.
Do not truncate. Canonical output<=128MiB, capture<=64MiB.

## Exact output

Output exactly {input_sha256,levels,beliefs,aggregate,witnesses,counts}.
input_sha256 hashes the complete validated input using compact sorted ASCII
JSON plus newline. Full-wire comparisons preserve native types, not Python
bool/int coercion. levels retain the four exact ordered pairs.

Each belief output is {belief_id,weight,pairs}. Each pairs list is row-major
16 actual/assumed combinations with actual index outermost. Pair exactly:
{actual_index,assumed_index,cells,x_scores,
 fallback_bayes_risk,fallback_forecast_risk,fallback_regret,
 completed_forecast_risk,completed_regret,
 coarse_forecast_risk,coarse_regret,gain_over_coarse,checks}.

x_scores exactly retains the nine corresponding X fields:
{coverage,unsupported_mass,bayes_risk,supported_bayes_risk,
 supported_forecast_risk,supported_regret,forecast_risk,regret,complete}.
Full forecast_risk/regret are null when incomplete. These are not Y's
always-defined completed scores.

Each cell exactly:
{value,actual_probability,assumed_probability,actual_prediction,
 assumed_forecast,coarse_forecast,forecast,supported,used_fallback,
 bayes_risk,forecast_risk,regret,coarse_risk,coarse_regret,gain_over_coarse,
 predictions_equal,coarse_predictions_equal}.
All report/future laws are complete sparse wires. assumed_forecast is null
only on unsupported cells (assumed_probability=[0,1]); coarse_forecast and
forecast are always defined. Cells sorted by actual-positive report value.
Cell risks/gains are conditional, not weighted. used_fallback is not an
observed noise coin: it records which declared forecast branch was selected.

checks exactly
{policy_total,mass_partition,split_decomposition,completed_decomposition,
 coarse_decomposition,gain_identity,supported_forecasts_preserved,
 zero_regret_iff_equal}.
All true after checks. Last checks completed AND coarse regret-law equality;
split decomposition checks both supported and fallback contributions.
Gain identity includes gain only from supported cells and the coverage bound.

aggregate={total_weight:[1,1],pairs}; aggregate pairs have the same pair
fields EXCEPT cells, plus {complete_before_beliefs,incomplete_before_beliefs}.
All scalar fields are original-history-weighted; aggregate x_scores remain
null when any positive-weight history is incomplete. The same checks apply.

witnesses has six length-16 lists:
{first_fallback,first_positive_fallback_regret,first_positive_completed_regret,
 first_better_than_coarse,first_equal_to_coarse,first_worse_than_coarse}.
Each first matching belief ID or null. Fallback witness means positive mass;
better/equal/worse use the sign of gain_over_coarse.

counts exactly
{beliefs,input_cells,input_prediction_atoms,input_fallbacks,input_fallback_atoms,
 pair_cells,supported_pair_cells,fallback_pair_cells,
 completed_scoring_terms,coarse_scoring_terms,
 complete_before_beliefs,incomplete_before_beliefs,
 positive_fallback_regret_beliefs,positive_completed_regret_beliefs,
 better_than_coarse_beliefs,equal_to_coarse_beliefs,worse_than_coarse_beliefs}.
The five input counts and two scoring-term counts are scalars; all remaining
counts are length-16 lists. Count retained/evaluated objects, not extrapolations.

## Verification, provenance and publication

Two independent summary-only implementations: primary quadratic sparse-law
scoring, reference linear expected-per-outcome loss. No runtime imports of
each other or prior executors. Runner pins X/W inputs, independently scores
Y, matches every retained X score/support/forecast, and checks W controls.

Independent tests cover full six-case wires and hand controls: no/partial
fallback, exact-zero versus tiny-positive assumed support, uneven report/
history weights, harmful supported forecasts, generic positive fallback
regret, extra fallback future symbols, multi-prefix/coarse-risk variation,
signed gain, detached/shared values, strict typed/DAG/caps and corruptions.
Explicit normal/-O subprocess guards must not rely on Python assertions.

The separate stdlib JSON-only audit carries its own raw induction, subset-
Mobius features/H, local/subset rows, categorical lifetimes and raw W noisy/N
cell reconstruction. It authenticates Y channels against X and raw evidence,
fallback table against raw N cells, complete X scoring and full Y outputs.
No executor/runner/test imports; their source contents are bytes only for
identity checks. Do not regenerate source aliases, replay prior public APIs,
or broaden operator/minimality certificates. The inherited fine-polynomial
digest remains pinned producer identity, not a fresh polynomial derivation.

Freeze seven files: README.md,fallback.py,reference_qr05y.py,study.py,
test_qr05y.py,test_capture.py,audit_json.py. A create-only external temporary
preflight may exercise the audit before final freeze. Run full normal/-O
tests in isolated Python with explicit fresh external -X pycache_prefix.
Capture results.json exclusively, then fresh normal/-O exact read-only
replays and final audit. Check seven sources,29 priors and artifact before/
after; audit also authenticates X's seven and W's six producer sources.
RESULTS.md and roadmap are outside the frozen ledger. Disclose corrections;
publish only Y research files/roadmap and preserve unrelated work.

No Y outcomes have been computed at protocol creation. No noise tuning,
fallback optimization, sensor calibration, empirical validation, RET
integration, Lean verification, ontology, new physics or gravity
correspondence is asserted. This is an explicit rule on supplied finite laws.

