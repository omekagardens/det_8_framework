# QR-05U protocol: exact filtering under partial observation

6 September 2026. Prospective bounded gate fixed before U outcome computation.
Base: pushed T commit 9dd30b3c25d77afd10b0827409cba36992c5fe18.

## Question and input boundary

T certifies a sufficient finite summary when its current class is known.
Here the received record is coarser. Does propagation and conditioning of
a belief over current classes exactly reproduce raw-order inference and
future question laws under the declared prior and observation access?

Keep exactly T's 4,447 raw observations, 416 terminal/H classes, frames,
features and independent fresh two-color thinning law. T results.json is
6,805,377 bytes, SHA256
f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8.
Pin it and its 24 priors (25 artifacts). The raw model, terminal local rows
and class membership/feature tables are declared producer dependencies.
Independently rebuild raw features, actual H fibers, raw induced subsets
and class-local rows to authenticate their bridge. Do not replay T's
refinement/minimality proof, source/mask aliases, P consumer, R probability
helper or Q four-variable certificate. No prior executor runtime imports
or mutable RET/core dependencies; static own-lineage utilities are allowed.

Core input is summary-only: local class deletion rows, an explicit
class-to-record/question label table, a declared class prior and three
rate pairs. The local deletion table alone does not determine those labels.
The separate raw bridge must check every member's labels and local row.
Neither core receives raw orders, H feature keys, full subset profiles or
artifact paths. Model validation cannot authenticate raw realization.

## Temporal and observation convention

The prior is on S0/H0. Apply K1, receive Y1; apply fresh K2, receive Y2;
then use a separately declared K3 to predict Q3, without receiving Y3.
Posterior coordinates refer to CURRENT H2, not the initial source H0.
Inferring the initial source would be a different smoothing problem.

For raw state s in its supplied frame, retain S's chain counts N0..N3,
colored induced K2,2 count M, and colored induced P4 count T.
Received observation: [frame_id,N0,N1,N2,N3].
Future question: [frame_id,N0,N1,N2,N3,M,T].
These are declared classical maps, not calibrated apparatus or quantum
measurement models. Both must be constant throughout every H fiber.
Original-vertex membership is not silently supported.

For parent eligible ranks(O,E), a particular retained subset of ranks(m,n)
has probability x^m(1-x)^(O-m)y^n(1-y)^(E-n). Structural subsets are counted
even where a rate makes their probability zero; probabilistic outputs retain
only positive atoms, with absence meaning exact zero.

## Fixed experiment menu

Use the already retained T obstruction states 612 and 625, both frame0,
ranks(3,3), with N=[1,6,4,0], M=0 and respectively T=0/1.
These were selected from prior evidence, not by a U outcome search.
Three explicitly hypothetical raw priors:
- left: delta at state612;
- right: delta at state625;
- mixture: half at each.

Use both prespecified schedules, each (K1,K2,K3):
- balanced: ((1/2,1/2),(2/3,1/3),(1/2,1/2));
- biased: ((2/3,1/3),(1/3,2/3),(2/3,2/3)).
Case order is left_balanced,left_biased,right_balanced,right_biased,
mixture_balanced,mixture_biased. Class priors are the exact raw pushforwards,
not uniform over classes. They are not empirically inferred/calibrated priors.

For each case, independently move each initial class mass to that fiber's
first raw member, and separately to its last raw member. Recompute raw
history evidence, current H posteriors and future question laws. They must
equal the original lift; raw-state posteriors themselves need not agree.
This tests redistribution only within the same initial H masses.

The raw oracle enumerates fresh induced subsets and exact weighted nested
paths, not class profiles. At most two starting states give at most
2*3^6 received paths or 2*4^6 paths including prediction per lift/schedule.
No arbitrary population-prior experiment or domain expansion is claimed.

## Public input and rational wire format

analyze(problem) accepts exactly:
{schema_version:"det8-qr05u-problem-v1",family:"qr05u_partial_observation",
 model:{classes,labels},prior,rates}.

classes use unchanged S local rows:
{class_id,frame_id,parent_color_sizes,odd,even},
odd/even sorted unique [{target_class,multiplicity}].
Retain S's structural, integral reconstruction, rank normalization,
commutation/operator and resource guards. Class IDs need not be topological.
The primary reconstructs by smaller-parent recurrence; the reference by
ordered deletion words divided by color factorials, using static own copies.

labels are contiguous class-ordered
{class_id,observation:[frame,N0,N1,N2,N3],
 question:[frame,N0,N1,N2,N3,M,T]}.
The question prefix must equal observation; frame equals its local row.
N0=1; N1=O+E+frame_id for these exact frame conventions;
0<=N2<=choose(N1,2), 0<=N3<=choose(N1,3);
0<=M,T<=choose(O,2)choose(E,2). These are structural checks, not authentication.

Fractions are native [numerator,denominator], nonnegative, denominator>0,
coprime, zero exactly[0,1], one exactly[1,1]. Input components <=64bits.
prior is sorted unique positive [{class_id,probability}], support1..16,
total exactly1. rates is exactly three [x_fraction,y_fraction] pairs in[0,1].
Returned probability fractions are reduced with components <=4,096bits.
No bool/int subclass coercion, strings, floats, tuples or implicit normalization.

Bounds:1..512 classes; local edges per color<=3, multiplicities1..3,
frame0/1 and ranks0..3; S reconstruction guards retained.
At most512 first observations,16,384 positive two-record histories,
262,144 history posterior atoms and262,144 history prediction atoms.
Bound breaches fail, never truncate. Working native JSON<=512MiB,
final capture<=64MiB. Public native validation rejects cycles, excessive
container height above128 and explosive shared DAGs before serialization, retaining per-call
memoization for valid shared inputs. Validate before canonical caches.
Outputs share no mutable containers with inputs or other calls.

## Calculation and exact output

Let K be reconstructed from local counts; e and q are explicit labels.
For a belief b and received y:
bminus(j)=sum_i b(i)K(i,j);
Z=sum_{e(j)=y} bminus(j);
bnew(j)=1[e(j)=y]bminus(j)/Z only when Z>0.
The class route uses sequential normalized Bayes updates; the independent
reference accumulates unnormalized joint class-path masses before normalizing.
All retained laws are compared to raw nested-path enumeration.

Belief atoms: {class_id,probability}, positive sorted by class_id.
Question-law atoms: {value:question_vector,probability}, positive sorted
lexicographically by value. Records/histories are ordered lexicographically
by observation or pair of observations. Full native objects, not only hashes,
are the equality criterion.

analyze output is exactly:
{model_sha256,reconstruction,prior,rates,kernel_sha256,
 first,histories,latest_only,unconditional,controls,checks,counts}.
reconstruction={profiles_sha256,profile_atoms,certificate,operator_checks};
profiles/certificate/operator schemas are exactly S reconstruct_profiles output.
model_sha256 hashes the complete supplied {classes,labels} model;
profiles_sha256 hashes only the S profiles list.
kernel_sha256 has three hashes of complete class rows
[{class_id,transitions:[{target_class,probability}]}], positive sorted atoms.

first rows={observation,likelihood,posterior}, for every positive Y1.
histories rows={observations:[Y1,Y2],likelihood,conditional_likelihood,
 posterior,prediction}, for every positive received pair.
likelihood=P(Y1,Y2); conditional_likelihood=P(Y2|Y1).
latest_only rows={observation,likelihood,posterior,prediction}, for every
positive Y2 after discarding Y1 under the SAME prior and schedule.
unconditional={after_first,after_second,after_third,next_prediction};
the first three are class beliefs, last is the Q3 pushforward.

controls={history_witness,forgetting_witness,map_witness}.
A null witness means no difference found in the fixed menu, not global equality.
history_witness={left:[Y1,Y2],right:[otherY1,Y2],question,
 left_probability,right_probability}.
Compare unordered lexicographically ordered positive history pairs sharing Y2.
Retain the first pair with differing actual Q3 laws, then first differing
question value. Different posteriors alone are insufficient.
forgetting_witness={observations,question,history_probability,latest_only_probability};
first history, then first question with full-history/latest-only difference.
map_witness={observations,map_class_id,question,mixture_probability,map_probability};
MAP maximizes the current posterior, ties resolved by smallest class ID,
then propagates that point mass through K3. Retain first history/question
with a difference from the mixture prediction. Witness existence is an outcome,
not acceptance. Do not substitute histories from different priors/schedules.

checks={first_normalization,joint_normalization,posterior_normalization,
 posterior_support,tower_first,tower_latest,three_step_composition,
 max_abs_residual}; seven booleans true, residual[0,1].
Check all posterior masses/support, sum_y1 P(y1)=1, sum_y1,y2 P(y1,y2)=1.
For every y1, averaging predictions over P(y2|y1) equals b1 K2 K3 pushed to q.
For every y2, averaging full-history predictions over P(y1|y2) equals the
latest-only prediction. Marginalized current posteriors equal unconditional
class beliefs. The unconditional three-step class law equals the direct
law at componentwise products of all three rate pairs.
These are not permission to discard informative intermediate evidence.

counts={classes,profile_atoms,kernel_atoms,first_histories,histories,
 first_posterior_atoms,history_posterior_atoms,history_prediction_atoms,
 latest_observations,latest_posterior_atoms,latest_prediction_atoms,
 history_pairs_compared,history_pairs_different,
 forgetting_comparisons,forgetting_differences,map_comparisons,map_differences}.
kernel_atoms is three integers. Comparisons actually evaluate every eligible
pair/history, even after finding a witness. map/forgetting comparisons equal
the number of positive histories; differences count unequal whole Q3 laws.

filter_history(problem,records) accepts the same problem and exactly two
known observation vectors. Unknown/malformed observations raise ValueError.
Validate both complete records before any zero-evidence branch.
A known but impossible history returns exactly
{status:"impossible",failed_stage:1 or2,likelihood:[0,1],posterior:null,prediction:null}.
A positive history returns the same keys, status:"possible",failed_stage:null
and its exact joint likelihood/current posterior/Q3 law.
No zero-vector posterior, prior reset, MAP fallback or pseudo-count is allowed.

## Independent audit and controls

The root runner independently reconstructs all raw features, H fibers,
local rows and record/question labels on both frames, compares the supplied
local-only model to T, and builds direct raw subset laws. It independently
constructs complete outputs by unnormalized raw nested paths for all six
cases, checks each class kernel against all raw members at every distinct
schedule rate and the three-rate products, and checks whole outputs against
both routes. The prior-lift comparisons use first/last raw representatives.
Raw/model/label/census dependencies and audits are explicit in the artifact.

Use an independent test oracle and normal/-O tests for Bayes orientation,
joint vs conditional evidence, current vs initial posterior, complete
question laws, canonical witness selection, forgetting and MAP controls,
zero likelihood at each stage, unknown records, boundary rates0/1, identity
idempotence, absorbing fixed-only frames, identifiable current-state
observations, rational/native/cache/DAG/cap/ownership boundaries and tampering.

Retain the first raw within-H pair differing on original vertex1 membership,
if any, to document why unsupported named-ID observation is not certified.
Do not reinterpret such a violation as noise. The public schema has no custom
observation predicate/vertex-ID query option.

Runner calls both public analyze routes on every case. It separately calls
filter_history for the first positive history of every case, and additionally
the last positive history of the first case, a known frame1 first observation
(impossible at stage1), and a possible first observation followed by known
frame1 (impossible at stage2). Choose lexicographically first frame1 observation.
These total18 separate public conditioning calls. Tests separately check
detached ownership and synthetic/boundary conditions.

## Lifecycle and interpretation

Canonical JSON is sorted compact ASCII with one final newline. Freeze README,
filtering.py,reference_qr05u.py,study.py,test_qr05u.py,test_capture.py.
Run full tests normally and optimized with fresh explicit external
-X pycache_prefix and isolated Python. Create results.json exclusively;
never overwrite. Run fresh normal/-O exact read-only replays and a separate
stdlib JSON-only postflight: no executor/runner/test imports, source bytes
only for identity checks. Check six sources,25 priors and artifact before/after.
RESULTS.md and roadmap are outside the frozen ledger. Disclose pre-capture
corrections; publish only scoped U research files/roadmap, preserving other work.

This is exact prior/design-relative classical filtering on a supplied finite
observation calculus. It is not identification of the actual raw order,
empirical prior calibration, new physics, a physical-time generator,
geometry/gravity derivation, ontology, RET integration or Lean installation.
Passing may show useful belief-state compression or retain no memory witness
in this menu. Either outcome must remain visible without changing the menu.
