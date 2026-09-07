# QR-05V protocol: predictive value of richer readouts

6 September 2026. Prospective gate fixed before V outcome computation.
Base: pushed U commit 7f75bd1b2c518ba8f5f200bde493f6de3daac2a0.

## Scope and dependencies

Keep U's raw domain, local summary model, six hypothetical experiments,
482 positive received histories, fixed K3 and complete Q3 target unchanged.
Pin U results.json: 1,320,664 bytes, SHA256
a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee,
and its 25 priors (26 artifacts total).
U's model, history likelihoods, current H2 posteriors and K3 rates are
explicit producer inputs, not recomputed secretly inside the readout core.
The raw audit must independently authenticate them before certifying V.

At each retained current posterior, receive an additional deterministic,
non-disturbing classical readout of CURRENT H2. Then predict Q3 after
the same fresh K3. No new thinning, rate optimization, target coarsening,
measurement disturbance, empirical calibration or physical sensor is implied.

The fixed nested menu is:
N = [frame,N0,N1,N2,N3];
NMT = [frame,N0,N1,N2,N3,M,T], evaluated at H2, not at the future state;
H = [class_id], an oracle readout of current H2.
Full H bounds the value of these readouts above and their Bayes risk below.
It is not an assumed available apparatus or a bound on future observations,
arbitrary interventions, unknown dynamics or other loss functions.

Every U posterior already fixes N through Y2. Thus its N readout has one
positive cell and zero gain by construction. That is a control, not a new
empirical discovery. Generic accepted beliefs may span different N values.

## Fixed risk convention

Use unscaled categorical Brier loss sum_q(forecast_q-1[Q3=q])^2.
For true predictive law p and Bayes forecast p, risk R(p)=1-sum_q p_q^2.
No factor1/2 is included. This formula is not the actual risk of an arbitrary
forecast such as a MAP point mass under a different true distribution.

Let k_h(q)=P(Q3=q|H2=h) at fixed K3, b be the current posterior,
p=sum_h b_h k_h, z=r(h), w_z=sum_{r(h)=z}b_h,
p_z=sum_{r(h)=z}b_h k_h/w_z for w_z>0.
For each readout:
R_r=sum_z w_z R(p_z);
G_r=R(p)-R_r=sum_z w_z sum_q(p_z(q)-p(q))^2.
Absent sparse probability atoms mean zero across the SAME complete Q3 alphabet.
Zero readout mass is omitted before division.

Check the marginal identity sum_z w_z p_z=p for every readout.
For each adjacent refinement baseline→N→NMT→H, check every positive
coarse cell's child weights, current posterior mixture, full future-law
mixture, risk reduction and squared-law identity. Global nesting is checked
on ALL model classes, including classes with zero supplied posterior mass.
Zero gain holds iff all positive fine-cell future laws equal their parent law.
Changed beliefs or distinct H classes alone are not evidence of useful gain.

H residual risk must equal sum_h b_h R(k_h). It need not be zero:
fresh K3 randomness remains after the current class is known.
Adjacent gains telescope. Do not pool six different hypothetical experiments
into an undeclared common prior.

## Public summary-only API

analyze(problem) accepts exactly
{schema_version:"det8-qr05v-problem-v1",family:"qr05v_readout_value",
 model:{classes,labels},rate,beliefs}.

The model is exactly U's local-row/label schema:
classes=[{class_id,frame_id,parent_color_sizes,odd,even}],
color rows sorted unique [{target_class,multiplicity}];
labels=[{class_id,observation:[frame,N0,N1,N2,N3],
 question:[frame,N0,N1,N2,N3,M,T]}].
Retain the S/U structural, divisibility, normalization, operator and frame/rank
guards. Class IDs need not be topological. The primary reconstructs full
profiles by smaller-parent recurrence; reference by color words/factorials.
No raw orders, H feature keys, full profiles, U histories/artifact paths,
initial prior or K1/K2 are given to this core. Local tables and supplied
labels/posteriors are structural data, not authenticated physical records.

rate is one [x_fraction,y_fraction] pair, U's fixed K3 in each case.
Each fraction is native [numerator,denominator], reduced, 0<=n<=d, d>0,
zero [0,1], one [1,1]. Rate components <=64bits.
beliefs is a contiguous belief-ID ordered nonempty list of
{belief_id,weight,posterior}.
weights are positive and sum exactly1; these are case history likelihoods.
posterior is sorted unique positive [{class_id,probability}] with mass1.
Weight/posterior components and all retained derived rationals <=4,096bits.
No implicit renormalization, bool/subclass coercion, strings, floats or tuples.
Internal signed differences may be used before squaring; weighted gain
terms, not an unweighted squared distance that can exceed1, are bounded
nonnegative scalars in[0,1].

Bounds:1..512 classes,1..512 beliefs,1..512 atoms per posterior;
total input posterior atoms<=262,144; all retained readout cells<=32,768;
readout posterior atoms<=786,432; readout prediction atoms<=1,048,576.
Local counts retain U bounds (ranks<=3 per color, multiplicities1..3,
at most3 targets per color). All bit/aggregate caps fail, never truncate.
Working JSON<=512MiB; final capture<=64MiB.
Native per-call DAG validation rejects cycles, container depth>128 and
explosive expanded trees before serialization while accepting valid shared
inputs. Validate before canonical-content caches; no mutable result caches.
All returned containers are detached from inputs and later/earlier calls.

## Exact output schema

analyze returns exactly
{model_sha256,reconstruction,rate,kernel_sha256,readout_maps,
 beliefs,aggregate,witnesses,counts}.

model_sha256 hashes the complete supplied {classes,labels}.
reconstruction={profiles_sha256,profile_atoms,certificate,operator_checks},
using the exact S reconstructed profile/certificate/operator schemas.
profiles_sha256 hashes only that profile list.
kernel_sha256 hashes positive complete class rows
[{class_id,transitions:[{target_class,probability}]}], targets sorted.
Canonical bytes are compact sorted ASCII JSON with one final newline.

readout_maps={
 NMT_to_N:[{fine:NMT_value,coarse:N_value}],
 H_to_NMT:[{fine:[class_id],coarse:NMT_value}]}.
NMT_to_N covers all distinct model question labels; H_to_NMT covers all
classes. Sort by fine value. Prefix equality is checked globally.

Each beliefs row is
{belief_id,weight,posterior,baseline,readouts,refinements,oracle_residual,checks}.
baseline={prediction,risk}, with the fixed Q3 prediction.
readouts={N,NMT,H}, each
{cells,expected_risk,gain,variance_gain}.
cells=[{value,probability,posterior,prediction,risk}],
positive and lexicographically ordered by value.
Belief atoms use {class_id,probability}; question-law atoms use
{value:seven_component_question,probability}; positive sorted native atoms.

refinements is ordered:
(baseline,N), (N,NMT), (NMT,H).
Each row={coarse,fine,risk_drop,variance_gain,parent_checks,zero_gain_iff_equal}.
A baseline cell has value[], probability1 and the supplied belief/prediction.
parent_checks rows are sorted by coarse value:
{value,probability,fine_values,mixture_sha256,
 conditional_risk_drop,conditional_variance_gain,predictions_equal}.
fine_values list all positive child values in lexical order.
mixture_sha256 hashes the canonical coarse prediction law reconstructed
from its children's normalized weights, never a digest-only premise.
conditional_risk_drop compares the parent's risk with conditional expected
child risk; conditional_variance_gain is the matching conditional weighted
squared-law distance. predictions_equal means every child future law
equals its parent. Check whole laws and posterior mixtures, not only hashes.
zero_gain_iff_equal is true after checking (risk_drop==0) iff all parents
have predictions_equal; it is not a claim that those laws actually agree.

oracle_residual is the independent class-wise sum_h b_h R(k_h).
checks={probabilities_normalized,marginal_future_preserved,nested_mixtures,
 nested_risks,oracle_residual_identity,gains_telescope,N_already_known}.
The first six booleans are true; N_already_known is true iff there is exactly
one positive N cell. It must be true for every declared U history but is
not a restriction on all valid generic input beliefs.

aggregate={total_weight,prediction,baseline_risk,expected_risk,gain,
 adjacent_gain,oracle_residual}.
total_weight=[1,1]; prediction is the case-weighted baseline Q3 law;
expected_risk and gain are maps with keysN,NMT,H; adjacent_gain is the
three weighted refinement risk drops in the fixed order.
Every aggregate is weighted by the supplied likelihoods, not uniformly
over histories or readout cells. Check aggregate nesting, telescoping and
oracle identity; no cross-case aggregate probability experiment is created.
In particular aggregate baseline_risk is sum_history weight*R(p_history),
not R of the aggregate prediction: the received history is already known.

witnesses={first_strict,first_zero,first_positive_oracle_residual,
 first_zero_oracle_residual}.
first_strict/first_zero are length3 lists, indexed by the fixed refinement
order. Entries are the first belief ID whose adjacent gain is >0 / ==0,
or null if none. Residual witnesses similarly select the first >0 / ==0.
These point to complete retained rows; no witness existence is required.

counts={classes,beliefs,profile_atoms,kernel_atoms,posterior_atoms,
 readout_cells,readout_posterior_atoms,readout_prediction_atoms,
 refinement_parents,strict_gain_beliefs,no_gain_beliefs,
 positive_oracle_residual_beliefs,known_N_beliefs}.
The three readout count fields and strict/no_gain fields are mapsN,NMT,H.
strict/no_gain count each readout's TOTAL gain from baseline, not adjacent gain.
refinement_parents is a length3 list in the fixed refinement order.
All counts refer to actual retained/checked objects, not inferred skipped work.

## Runner and independent verification

Case order/rates/history order are exactly U's six cases. For each case
belief_id is its zero-based positive-history row index, weight is that U
joint likelihood and posterior is that U CURRENT H2 distribution.
Authenticate the correspondence by recomputing U raw histories, not merely
trusting the artifact's posteriors. Raw model, actual H fibers, local rows,
features, observation/question labels and K3 laws are rebuilt on all4,447 states.
Reuse static own-lineage utilities; never import earlier executors at runtime.
No mutable RET/core imports or source/mask-alias regeneration.

Primary scores conditional posterior predictions and weighted squared-law
gains. Reference builds joint readout×Q masses before normalizing and computes
risk via1-sum_z,q J(z,q)^2/w_z. Root independently conditions raw nested
S0→S1→S2 paths and enumerates S2→S3 subsets under the unchanged law.
Derive each raw readout/future joint law and compare all complete outputs.
Verify every raw member's K3 row for the distinct case rates. Rebuild U
evidence/current posterior/prediction to authenticate every input belief;
U's broader native API/18 conditioning calls and T's refinement/minimality,
P consumer, R helper, Q four-variable certificate are not replayed.

Separate independent tests include a raw two-replica disagreement risk
oracle with correct per-cell normalization. Synthetic local models cover
identical future laws despite different current classes; odd/even singleton
mixtures at equal/unequal rates; unequal cell probabilities; positive oracle
residual; identity/deletion corners; MAP formula misuse and future-outcome
leakage; changed target/marginal/parent mapping; native/rational/DAG/depth/
bit/aggregate caps; typed caching and full output ownership.
These are algebraic controls, not additions to the fixed U experiments.

## Lifecycle and interpretation

Freeze README,readout_value.py,reference_qr05v.py,study.py,test_qr05v.py,
test_capture.py. Run normal/-O tests with fresh explicit external
-X pycache_prefix and isolated Python. Create results.json exclusively;
never overwrite. Run fresh exact normal/-O read-only replays and separate
stdlib JSON-only postflight with source bytes only for identity hashes
and no executor/runner/test imports. Check six sources,26 priors and artifact
before/after. RESULTS.md/roadmap are outside the frozen ledger.
Disclose pre-capture corrections; commit/push only scoped V research files
and roadmap, preserving all unrelated RET/core/Track-B/temp-sheet work.

This quantifies exact predictive information for supplied priors, laws,
readouts and Brier loss on a finite calculus. It does not establish sensor
availability, calibrated empirical performance, costs, an adaptive policy,
minimum physical memory, ontology, new physics, gravity, RET integration
or Lean verification. Keep strict gain, no gain and positive residual
outcomes without changing the experiment in response.
