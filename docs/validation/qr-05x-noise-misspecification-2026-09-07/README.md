# QR-05X protocol: noise-model misspecification

7 September 2026. Prospective specification fixed before X case outcomes.
Base: pushed W commit f2fb58047a86b513d8a032980bc49c316bd6d84b.

## Scope and declared dependencies

Keep W's six experiments, 482 positive histories, H2 beliefs, K3, complete
future Q3 and four N-preserving random-replacement channels unchanged.
Pin W results.json: 6,756,094 bytes, SHA256
05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a.
Its 27 prior artifacts plus W are 28 immutable producer artifacts.

For current NMT label a within the fixed whole-model distinct-label fiber
A_N, C_t(z|a)=(1-t)1[z=a]+t/|A_N|. Levels in order are 0,1/2,3/4,1.
The unobserved replacement coin may redraw a. Noise is non-disturbing and
independent of fresh K3 given H2. No extra observed coin, intermediate
report, changed prior, changed target or future-correlated noise is supplied.

X is a scoring layer, not another class-local reconstruction implementation.
The runner authenticates the pinned W artifact and projects its complete
conditional report/future laws. The generic core accepts four normalized
conditional experiments and checks shared future marginals; it does NOT
authenticate their origin or enforce the W replacement family. W-specific
claims are checked on fixed producer cases, never inferred from mere
normalization. No prior executor is imported at runtime. An independent
JSON-only raw-history postflight reauthenticates W and the X projection.

## Actual versus assumed law

Cross actual level index i and assumed index j in row-major 4x4 order.
Let w_i(z) be actual report mass and p_i(q|z) the actual future law.
The assumed forecast is f_j(q|z)=p_j(q|z), defined only if w_j(z)>0.
The scorer uses w_i and p_i, NOT the assumed report law or assumed Bayes risk.

For each actual-positive report and defined forecast, retain
Brier(f;p)=sum_q p(q) sum_r (f(r)-1[r=q])^2
          =1-2 sum_q p(q)f(q)+sum_q f(q)^2,
R(p)=1-sum_q p(q)^2,
D(p,f)=sum_q (p(q)-f(q))^2,
and verify Brier(f;p)=R(p)+D(p,f).
Sparse missing future atoms are exact zero; take the UNION of supports.
R is in [0,1]; actual risk and regret can reach 2. Zero regret holds iff
the entire future distributions agree, not just their scalar Bayes risks.

If w_i(z)>0 but w_j(z)=0, keep z and its actual mass as unsupported.
Assumed probability is [0,1]; forecast, forecast_risk and regret are null.
Do not invent a posterior, drop the report, renormalize remaining weights,
choose a fallback policy or treat unsupported as zero risk.

coverage=sum_supported w_i(z); unsupported_mass=1-coverage.
supported_bayes_risk=sum_supported w_i(z)R(p_i);
supported_forecast_risk=sum_supported w_i(z)Brier(f_j;p_i);
supported_regret=sum_supported w_i(z)D(p_i,f_j).
These are UNNORMALIZED supported contributions, not conditional averages.
Full bayes_risk=sum_all w_i(z)R(p_i) is always defined.
Full forecast_risk/regret equal supported contributions iff coverage=1,
otherwise both are null. supported_forecast_risk must equal
supported_bayes_risk+supported_regret. Full decomposition is checked only
at complete coverage; supported bounds scale with coverage.

Aggregate each pair within a case using original positive history weights.
Case coverage and supported contributions preserve original actual weights.
Case full forecast risk/regret are null if ANY positive-weight history is
incomplete. Retain aggregate Bayes risk over all reports. Never pool cases.

Preregistered consequences, not discoveries:
diagonal pairs have complete coverage and zero regret; every assumed
positive-noise W model covers every actual-positive report; assumed full
replacement has the N-conditional forecast, hence actual-law expected risk
equals W's N risk for every actual level. Distinct noise parameters need
not yield different forecasts or positive regret.
No monotonicity or symmetry of mismatch regret is presumed.
No fixed-case witness of a particular sign or size is required.

## Public exact scoring API

analyze(problem) accepts exactly
{schema_version:"det8-qr05x-problem-v1",
 family:"qr05x_noise_misspecification",beliefs:[...]}.

Each belief is exactly {belief_id,weight,channels}; IDs contiguous from 0,
positive normalized history weights. Each channels list has exactly four
entries in fixed level order, each {level,cells}.
Each cell is exactly {value,probability,prediction}; report values are
seven-component lists of native nonnegative integers of at most 64 bits.
Cells are sorted unique by report value, positive and normalized.
Each prediction is a nonempty, sorted unique list of
{value:seven-component future vector,probability:positive fraction},
normalized. Report/future vectors are opaque symbols for the generic
scorer: no assertion of geometric/physical validity is made.
Each channel has the same full unconditional future marginal per belief.
A shared marginal does NOT certify the replacement model or preserve N.

Fractions are native reduced [n,d], n>=0,d>0, each component <=4096 bits;
input probabilities/levels <=1. Zero=[0,1], one=[1,1]. Reject bool/int
subclasses, float/string/tuple fractions, duplicates, unsorted values,
unknown/missing fields, zero sparse masses and normalization repair.
Signed differences may be internal; retained scores are nonnegative <=2.
Every retained rational component is <=4096 bits; reject overflow.

No mutable result cache. Outputs must be detached from inputs and other calls.
Native tree/DAG guards run BEFORE serialization, reject cycles, depth>128,
expanded node count>8,388,608 and expanded canonical size>128MiB; valid
shared structures are accepted. Expanded, not unique-node, resource accounting.
Nodes count JSON values, not dictionary key strings; root depth is zero and
scalar leaves count toward depth. Exact ASCII canonical size includes newline.
Per-call caps: beliefs 1..512; cells/channel 1..4096; atoms/prediction 1..4096;
total input cells <=32768; total input prediction atoms <=2097152;
retained pair cells <=131072; scoring work <=16777216 support visits.
Scoring work counts, for each supported pair cell, len(actual prediction)
plus len(assumed prediction), planned and checked BEFORE pair score loops.
Retained pair-cell work counts actual cells repeated over four assumed
experiments, including unsupported cells. Never truncate on caps.
Canonical output <=128MiB; capture <=64MiB.

## Exact output schema

Output exactly
{input_sha256,levels,beliefs,aggregate,witnesses,counts}.
input_sha256 hashes the entire validated input. All hashes and captured
mathematical comparisons use compact sorted ASCII JSON plus one newline,
with exact native type checking (bool is not interchangeable with int).
levels=[[0,1],[1,2],[3,4],[1,1]].

Each belief output:
{belief_id,weight,pairs}.
pairs has 16 entries, i outer, j inner. Each entry:
{actual_index,assumed_index,cells,bayes_risk,coverage,unsupported_mass,
 supported_bayes_risk,supported_forecast_risk,supported_regret,
 forecast_risk,regret,complete,checks}.

Each retained actual-positive cell:
{value,actual_probability,assumed_probability,actual_prediction,forecast,
 bayes_risk,forecast_risk,regret,supported,predictions_equal}.
actual_prediction is the full actual law, always present.
forecast is the full assumed law or null; predictions_equal is bool when
supported, null otherwise. Cell scalar risks are CONDITIONAL, not weighted.
checks exactly
{mass_partition,supported_decomposition,full_decomposition,
 zero_regret_iff_equal}.
mass_partition and supported_decomposition are true after checks;
full_decomposition is true if complete, otherwise null.
zero_regret_iff_equal is true after checking EVERY supported cell, including
when none exist; unsupported cells make no forecast equality claim.

aggregate={total_weight,pairs}, total_weight=[1,1].
Aggregate pairs have the same pair fields EXCEPT cells, and add
{complete_beliefs,incomplete_beliefs}.
Their checks have the same meanings; zero-regret equivalence means zero
supported regret iff every supported cell across positive histories agrees.
Full decomposition is null when case coverage is incomplete.

witnesses has three length-16 lists:
{first_incomplete,first_positive_supported_regret,first_positive_full_regret}.
Each is the first matching belief ID, or null. Positive full regret requires
complete coverage; positive supported regret does not establish full risk.

counts exactly
{beliefs,input_cells,input_prediction_atoms,pair_cells,
 supported_pair_cells,unsupported_pair_cells,scoring_terms,
 complete_beliefs,incomplete_beliefs,positive_supported_regret_beliefs,
 positive_full_regret_beliefs}.
First three and scoring_terms are scalars; pair_cells and all remaining
counts are length-16 lists in pair order. Count actual retained/executed
objects, not hypothetical future experiments.

## Independent routes, controls and lifecycle

Primary computes sparse-law quadratic risk and squared-distance regret.
Reference computes expected per-outcome Brier loss independently and checks
the decomposition. No implementation imports the other or a prior executor.
Runner compares complete outputs to its own independent projection/scoring
oracle on all six cases and checks W diagonals, positive-noise coverage,
and assumed-full-replacement N-risk controls.

Tests include hand binary fair/biased priors, deterministic opposed forecasts
attaining risk/regret 2, disjoint supports/zero coverage, partial coverage,
unsupported mass and non-renormalization, identical futures despite differing
report laws, uneven history/report weights, wrong assumed weighting, full
law equality versus equal scalar risks, ownership, typed wires, DAG/resource
limits and output corruptions. Explicit normal/-O subprocess guards must
reject malformed inputs without depending on Python assertions.

A separate stdlib JSON-only audit uses raw induction, subset-Mobius feature
reconstruction, categorical vertex lifetimes and raw current/report/future
joints to authenticate the W law projection and every X output. No current
or prior executor, runner or test imports. Source content is read only for
identity hashes. The inherited fine-polynomial digest remains a pinned
producer identity, not a fresh polynomial reconstruction. Prior public APIs,
T minimality, source aliases, physical interfaces and RET are not replayed.

Freeze seven source/protocol files: README.md,misspecification.py,
reference_qr05x.py,study.py,test_qr05x.py,test_capture.py,audit_json.py.
Run full normal and optimized tests in isolated Python with explicit fresh
external -X pycache_prefix. Capture exclusively, then fresh normal/-O exact
read-only replays and JSON-only audit. Check seven sources,28 priors and
artifact before/after; also authenticate the W producer's six source hashes
during the independent inherited audit. RESULTS.md and roadmap remain outside
the frozen ledger. Disclose corrections before/after any outcome computation.
Publish only X research files/roadmap; preserve unrelated changes.

No X outcomes have been computed at protocol creation. These are hypothetical
finite observation/forecast experiments, not fitted apparatus error, a
fallback policy, robust optimization, cost/utility analysis, RET integration,
Lean verification, ontology, new physics or gravity correspondence.
Conflicting physical observations require a justified measurement model,
not an appeal to this mathematical misspecification calculation.
