# QR-05W protocol: imperfect classical readouts

7 September 2026. Prospective specification fixed before W case outcomes.
Base: pushed V commit 971d2fd002d86bf6f13fd3d7888453cd23b44790.

## Scope and declared dependencies

Keep U's six hypothetical experiments, 482 positive received histories,
current H2 beliefs, history likelihoods, K3 and complete future Q3 unchanged.
Pin V results.json (3,493,736 bytes), SHA256
eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7,
and its 26 priors: 27 immutable producer artifacts total.

V's raw/model/U-history/readout outputs are declared dependencies. The runner
must authenticate raw H2 histories and V's complete deterministic readout
analysis independently before accepting them. The public W core receives
none of these artifact paths or raw histories. No prior executor is imported
at runtime; static own-lineage algebra/audit helpers may be carried locally.

N=[frame,N0,N1,N2,N3], A=NMT=[frame,N0,N1,N2,N3,M,T] are CURRENT labels.
H is the certified current class. Future Q3 has the same seven-component
alphabet but is evaluated after a separate fresh K3 transition. Receiving a
noisy current report does not reveal the future outcome or change H2/K3.

## Fixed channel family and timing

For each N value in the WHOLE model, let A_N be its sorted DISTINCT A labels.
Do not weight this alphabet by class multiplicity, restrict it to posterior
support, or rebuild it after receiving a report. Alphabet includes classes
of zero supplied posterior mass. Single-symbol fibers remain unchanged.

For current true label a in A_N, report z in A_N through
C_t(z|a)=(1-t)1[z=a]+t/|A_N|.
Use exactly four levels, in order: t=0,1/2,3/4,1.
Replacement is uniform over the entire fiber, including the original label.
The coin indicating replacement is NOT observed. Random report labels can
be false-but-valid labels; this is not an erasure flag.

The report is a non-disturbing classical channel of current H2. Its fresh
randomness is independent of K3 given H2. For each level the actual received
experiment consists of ONE report. Intermediate reports/coins used to prove
a Markov coupling are NOT additionally supplied to the forecaster.

Adjacent level comparisons use garbling levels 1/2,1/2,1, respectively:
C_0 C_1/2=C_1/2, C_1/2 C_1/2=C_3/4, C_3/4 C_1=C_1.
Check composition on every full-model source symbol, not only live beliefs.
Uniform replacement is idempotent within each fixed N fiber.

## Risk and complete-law identities

Retain unscaled categorical Brier Bayes risk R(p)=1-sum_q p(q)^2.
For b_h, k_h(q)=P(Q3=q|H2=h), form
J_t(z,h,q)=b_h C_t(z|a_h) k_h(q), w_t(z)=sum_h,q J_t(z,h,q).
For w_t(z)>0, retain the full current posterior and future predictive law.
Omit zero cells before division; missing sparse atoms mean exact zero.

R_t=sum_z w_t(z) R(p_t(.|z)).
G_t=R_baseline-R_t=sum_z w_t(z)||p_t(.|z)-p_baseline||^2.
Also retain gain_over_N=R_N-R_t, distinguishing added NMT information from
N itself for generic beliefs spanning N. Actual U beliefs already know N.
If gain_over_N at t=0 is positive, retained_gain_fraction is the ratio of
that level's gain_over_N to the clean gain; otherwise it is null, not zero.

For each adjacent earlier/final pair (s,t), let D be its fixed garbling.
The proof coupling is P(z,w,h,q)=J_s(z,h,q) D(w|z).
Retain every positive report pair P(z,w)=w_s(z)D(w|z), both marginals,
and each later cell's reverse weights P(z,w)/w_t(w). They must reconstruct
its complete CURRENT posterior and FUTURE law, not merely its scalar risk.
No deterministic-parent assignment is possible in general: channels overlap.

Check per later cell and globally:
R_t-R_s=sum_z,w P(z,w)||p_s(.|z)-p_t(.|w)||^2 >= 0.
Zero loss iff all positively coupled earlier future laws equal their later
law. Distinct posteriors or symbols alone do not imply positive loss.
This is EXPECTED-risk monotonicity, not a pointwise claim for each realized
report. Conditional risk can decrease for some symbol as noise increases.

Check unchanged marginal current belief and future law at every level;
R_H<=R_0<=R_1/2<=R_3/4<=R_1=R_N<=R_baseline;
the losses telescope; H residual equals sum_h b_h R(k_h).
At t=0 cells equal clean NMT cells. At t=1 each report within a positive
N fiber has mass P(N)/|A_N| and the N-conditional posterior/future law.
This establishes information equivalence to N, NOT literal record equality.

Family-implied interpretation, recorded before W outcomes:
within N, alpha_a=P(A=a|N), m=|A_N| and clean future laws p_a give
w_z(t)=(1-t)alpha_z+t/m and
G_t(within N)=(1-t)^2 sum_z alpha_z^2/w_z(t) ||p_z-p_N||^2.
Terms with zero alpha contribute zero; the t=0 expression uses only
positive-alpha terms. Hence strict added gain survives every t<1 iff clean
added gain exists. Strict-history survival is not independent robustness
evidence. Quantitative risk/gain/retention are the informative case outcomes.

Aggregate only within each case using its original history likelihoods.
Baseline aggregate risk is the weighted mean of history-conditioned risks,
not the risk of the averaged prediction. Aggregate retention is the ratio
of weighted gains, not a weighted mean of per-history retention ratios.
Never introduce a common prior over the six experiments.

## Public summary-only API and guards

analyze(problem) accepts exactly
{schema_version:"det8-qr05w-problem-v1",family:"qr05w_noisy_readouts",
 model:{classes,labels},rate,beliefs}.
Model/rate/beliefs are exactly V's structural schema:
classes=[{class_id,frame_id,parent_color_sizes,odd,even}],
color rows=[{target_class,multiplicity}], sorted unique;
labels=[{class_id,observation:N,question:A}], covering every class.
Class IDs are contiguous but need not be topological. Frame is 0 or 1;
color ranks 0..3, at most 3 targets/color, multiplicities 1..3. Retain
precise frame/rank loss, row masses, divisibility, normalization and commuting
color-operator checks. N0=1,N1=odd+even+frame, 0<=N2<=choose(N1,2),
0<=N3<=choose(N1,3), 0<=M,T<=choose(odd,2)choose(even,2).
Question prefix must equal observation on ALL classes.

rate is one [x_fraction,y_fraction] pair, with components at most 64 bits.
beliefs=[{belief_id,weight,posterior}], contiguous IDs, positive weights
summing to 1. posterior=[{class_id,probability}], sorted unique positive
atoms summing to 1. All fractions are native reduced [n,d], 0<=n<=d,d>0;
zero=[0,1],one=[1,1]. Belief/weight/retained derived components <=4096 bits.
No bool/subclass coercion, float/string/tuple fractions or normalization
repair. Signed differences are allowed internally. Unweighted squared-law
distance may exceed 1; only its properly weighted retained contribution is
bounded in [0,1]. No mutable result cache; outputs fully detached.

Caps: 1..512 classes, 1..512 beliefs, <=512 atoms per posterior;
total input posterior atoms <=262144; global positive channel atoms across
four levels <=1048576; composition product terms across three edges <=4194304;
all retained N-control plus four-level cells <=32768;
their posterior atoms <=1048576 and prediction atoms <=2097152;
all retained report-pair coupling atoms <=1048576;
all receiving-cell checks across three edges <=32768.
Retain V's class-local/profile caps (3072 local atoms,32768 profile atoms).
Reject cap overflows; never truncate. Check planned composition work before
its product loops. Working canonical JSON <=512MiB, capture <=64MiB.
Native per-call DAG checks precede serialization/content caches: reject
cycles, depth>128 and explosive expanded trees, accept valid shared input.

## Exact output schema

Output exactly
{model_sha256,reconstruction,rate,kernel_sha256,channel_model,
 beliefs,aggregate,witnesses,counts}.
Model/reconstruction/kernel hashes and reconstruction fields retain V's
exact definitions: reconstruction={profiles_sha256,profile_atoms,certificate,
operator_checks}; profiles hash is of profiles alone. Kernel hashes complete
positive class rows [{class_id,transitions:[{target_class,probability}]}].
All hashes use compact sorted ASCII JSON plus one newline.

channel_model={
 alphabet:[{N:N_vector,values:[A_vectors]}],
 channels:[{level,rows:[{source:A_vector,
                        transitions:[{value:A_vector,probability}]}]}],
 composition_checks:[{from_index,to_index,garbling_level,row_comparisons,
                      product_terms,positive_composed_atoms,
                      composed_sha256,exact}]}.
Alphabet sorted by N, each values list sorted unique. Each channel's rows
sorted by source over ALL distinct A labels. Transitions sorted positive.
Channels in fixed level order; composition_checks in fixed adjacent order.
composed_sha256 hashes the ACTUALLY multiplied complete destination rows
(without the level wrapper), not an assumed destination digest.
product_terms counts positive source/intermediate/target products evaluated.
exact is true only after full native row equality.

Each belief row:
{belief_id,weight,posterior,baseline,controls,channels,garblings,checks}.
baseline={prediction,risk}.
controls={N:{cells,expected_risk,gain},H:{expected_risk,gain}}.
N is exact deterministic current N; H expected risk is class-wise residual.
channels=[{level,cells,expected_risk,gain,variance_gain,
           gain_over_N,retained_gain_fraction}] in fixed level order.
All cells=[{value,probability,posterior,prediction,risk}], positive and
lexicographically sorted. N control values are five-component N vectors;
channel values seven-component A vectors. Belief atoms use class_id;
future-law atoms use {value:Q_vector,probability}, sorted positive.

garblings=[{from_index,to_index,garbling_level,risk_increase,variance_loss,
            couplings,receiving_checks,zero_loss_iff_equal}].
couplings=[{earlier:A_vector,later:A_vector,probability}], positive and
lexicographically sorted by (earlier,later), with unconditional belief-level
pair probability. receiving_checks sorted by later value:
{value,probability,earlier_values,posterior_mixture_sha256,
 prediction_mixture_sha256,conditional_risk_increase,
 conditional_variance_loss,predictions_equal}.
earlier_values lists all positive incoming symbols in lexical order.
Mixture hashes cover actually reconstructed complete posterior/future wires.
zero_loss_iff_equal is true after checking the equivalence, not a statement
that the loss is zero.

checks={probabilities_normalized,marginal_current_preserved,
 marginal_future_preserved,garbling_marginals,conditional_mixtures,
 risk_order,endpoint_information_equivalence,losses_telescope,N_already_known}.
First eight are true after checks. Last is computed from positive N cells;
it is required true only for actual U histories, not generic public inputs.

aggregate={total_weight,prediction,baseline_risk,N_risk,H_risk,
 channels:[{level,expected_risk,gain,gain_over_N,retained_gain_fraction}],
 adjacent_risk_increase:[three fractions]}.
total_weight=[1,1]; all terms likelihood-weighted within this case;
prediction is its weighted unchanged baseline Q3 law.
N/H controls, nesting, endpoints and telescoping remain checked.

witnesses={first_strict_gain,first_zero_gain,first_strict_loss,first_zero_loss,
 first_positive_oracle_residual,first_zero_oracle_residual}.
Gain witness lists have four entries and use gain_over_N, NOT total gain.
Loss witness lists have three entries. Each entry is the first belief ID
meeting >0 or ==0, or null if absent. No witness existence is required.

counts={classes,beliefs,profile_atoms,kernel_atoms,alphabet_fibers,
 alphabet_values,global_channel_atoms,posterior_atoms,
 channel_cells,channel_posterior_atoms,channel_prediction_atoms,
 N_cells,N_posterior_atoms,N_prediction_atoms,coupling_atoms,receiving_checks,
 strict_gain_beliefs,no_gain_beliefs,strict_loss_beliefs,no_loss_beliefs,
 positive_oracle_residual_beliefs,known_N_beliefs}.
global_channel_atoms and channel_* and gain counts are length-four lists;
coupling_atoms,receiving_checks and loss counts are length-three lists.
Gain counts use gain_over_N; all other counts refer to actual retained
objects, not unexecuted work or logical extrapolation.

## Independent routes, controls and lifecycle

Primary retains local rank recurrence and conditional posterior scoring.
Reference retains independent color-word/factorial reconstruction and joint
readout/current/future masses. Root independently authenticates U/V producer
evidence and derives noisy current/future joints from raw nested subsets,
then full stochastic couplings. Every raw member's fixed K3 law is checked.
Prior U/V public helper calls, T minimality, P consumer, R helper, Q
four-variable certificate and original source/alias universe are NOT replayed.

Separate raw tests include two-replica disagreement risk per noisy cell,
correct reverse-Bayes coupling mixtures and full-wire comparisons.
Hand controls cover fair/biased binary labels, identity future, singleton
fibers, identical future laws despite distinct labels, whole-model
zero-posterior labels, duplicate classes versus distinct labels, generic
multi-N beliefs, unequal cell/history weights, no gain and positive H
residual, identity/deletion corners, unflagged versus observed replacement
coin, pointwise versus expected-risk monotonicity and future-correlated
noise leakage. Native/DAG/caps/typed-cache/ownership and output-corruption
controls remain explicit, including bounded normal/-O subprocesses.

Freeze six files: README.md,noisy_readout.py,reference_qr05w.py,study.py,
test_qr05w.py,test_capture.py. Run full normal/-O tests in isolated Python
with explicit fresh external -X pycache_prefix. Create results.json
exclusively, then fresh exact normal/-O read-only replays. Run a separate
stdlib JSON-only postflight, no executor/runner/test imports and source bytes
only for identity hashes. Check six sources,27 priors,artifact before/after.
RESULTS.md and roadmap stay outside frozen ledger. Disclose pre-capture
corrections. Publish only W research files/roadmap; preserve unrelated work.

This is hypothetical classical observation-channel calculus. No empirical
noise calibration, apparatus, causal intervention, adaptive sensing policy,
cost/utility model, RET integration, Lean verification, ontology, new physics
or gravity correspondence is asserted. Conflicting physical observations
cannot be dismissed as noise without a separately justified measurement model.
