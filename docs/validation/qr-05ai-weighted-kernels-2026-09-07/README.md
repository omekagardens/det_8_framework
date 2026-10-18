# QR-05AI protocol: weighted causal-kernel refinement

7 September 2026. Prospective specification, before fixed AI computations.
Base: pushed AH commit c387b55054eeb2b33bd6a9027b3178701968e3c9.
Unrelated RET/core/governance sources, dependencies and prior evidence stay unchanged.

## Question, status and access

Connect local cell-volume marks to the first three scalar causal-propagation
coefficients on AH's existing bounded nested partitions. Separate finite
weighted targets, continuum comparison, annotation truth and selection support.
This is a PRIVATE exact diagnostic on authenticated supplied fixtures, not a
new hardened generic production API. It does not expand AG/AH's public contracts.
No RET integration, Lean, physical calibration, metric reconstruction, continuum
limit, quantum CP map, finite-mass kernel accuracy or gravity is claimed.

Two independent stdlib mathematical engines consume the same authenticated
source/design DATA, not each other's code or computed answers. Each recomputes
cell areas, source strict order, clipped volumes, pair integrals, record-local
chains, full sampling moments and union-inclusion covariance. AH data reuse
is explicit, not claimed independent reconstruction of AH's fixture generation.
The independent engine is also the read-only replay/audit route; it is not
counted as a third independently implemented mathematical engine.

Each engine exposes build_case(case_id,level,source,design), observe(packet),
and causal_area(a,b,c,d) for the one-dimensional directed integral
integral_[a,b] integral_[c,d] 1(x<y) dy dx, with rational endpoints.
The private observer packet contains ONLY
{frame_size,fixed,eligible,probes,mask_probabilities,record};
record is {kept,past,marks}, the unchanged AH/AG native record wire.
No source coordinates, bounds, missing marks, family/level name, parent links
or source targets enter observe. Inputs are trusted bounded native fixtures;
basic consistency errors fail explicitly, but no adversarial generic-API
resource-safety contract is claimed. No hidden artifact reads in either engine.

## Supplied scalar comparison and zero-weight markers

Use ds²=du dv and dmu=du dv/2. Strict order is u_x<u_y AND v_x<v_y.
For each fixed timelike probe (a,b), Q is its open rectangle; boundaries have
zero volume. V=mu(Q), tau²=2V. Set alpha=[1/2,-1/4,1/8].
Degree q counts q INTERNAL eligible cell representatives. Fixed bookkeeping
markers have ZERO quadrature weight, even when they lie inside another probe.
No self-pair or null/equal-coordinate representative pair is counted.

For q=0 the single empty chain exists iff a precedes b, with weight1.
For q=1 each eligible representative in Q is one chain of weight w_i.
For q=2 each directed a<i<j<b strict causal chain has weight w_i*w_j,
counted once. Increasing original IDs naturally order these chains.
T_q is alpha_q times the full supplied-weight chain sum.
G_q uses true geometric cell volumes g_i instead of supplied w_i.
Continuum coefficients are [1/2,-V/4,V²/32].
These are formal coefficients in mass-squared, not probabilities or a CP map.

The supplied flat scalar baseline follows the convention discussed in
[Johnston, Particle propagators on discrete spacetime, §§3.1–3.2](https://arxiv.org/pdf/0806.3083).
The weighted deterministic quadrature studied HERE is a declared comparison,
not Johnston's Poisson-sprinkling convergence result or a DET-derived law.
AF's earlier internal-event count includes fixed internal markers; merely
substituting cell weights for inverse density is therefore NOT an exact
numerical replay of every AF coefficient. AF is preserved by identity only.

## Pair-integral discrepancy, not an inherited kernel bound

For each cell i, h_i=mu(cell_i intersect Q), including cells whose representative
lies outside Q. Define R_ij=1(rep_i precedes rep_j), including R_ii=0.
Let J_ij be the integral of 1(x precedes y) over
(cell_i intersect Q) x (cell_j intersect Q), with volume measure on each factor.
Retain ALL ordered cell pairs (i,j), including diagonal, reverse-ID directions,
incomparable representatives and zero-volume clips.

The integral factorizes as one-quarter times the two directed 1D integrals.
Both implementations must use independently written exact integral algorithms.
For a positive rectangle clip, J_ii=h_i²/4. This is the positive measure of
two DISTINCT causally ordered continuum points inside one cell, not the
zero-measure diagonal x=y. Empty clips contribute zero.

Let P_g=sum over representative chains i<j in Q of g_i*g_j (unscaled).
K=sum over ALL i!=j R_ij*h_i*h_j.
Jcross=sum over ALL i!=j J_ij (not only representative-comparable pairs).
Jdiag=sum_i J_ii. Independently verify J=Jcross+Jdiag=V²/4.

    P_g - J = (P_g-K) + (K-Jcross) - Jdiag.

Call these boundary_error, cross_order_error, omission_error, respectively.
Multiply by1/8 to compare q2 coefficients. This decomposition depends on the
declared intermediate K; the terms are not unique physical mechanisms.
Neither its summands nor total point error is assumed monotone under refinement.
AH's one-cell [L,U] certificate is NOT reused as a bilinear-kernel error bound.

## Fixed inputs and observation laws

Consume AH's 27 cases, in their exact retained order, using each case's
case_id,level,source,design. Five families grid,warp,warp_stale,boost,dilate;
three levels l0,l1,l2 with6,7,8 eligible cells. The coordinates/bounds/points,
fixed marker IDs, probe order and stale marks are exactly AH's supplied data.
Authenticate AH input first; no outcome-based fixture alteration or new splits.

Grid/warp at every level use identity,iid_half,singleton. Other families
use identity only. Enumerate all4,032 masks, including3,079 structural zeros
and953 positive rows. No cross-level coupling or conditional transport.

For support mask A, pi(A)=sum_(S contains A) p(S), pi(empty)=1.
Methods, in order: raw and joint_supported.
Raw sums alpha_q times the retained chain weight.
joint_supported divides by pi(A) when positive, otherwise omits explicitly.
Every singleton marginal is positive; pair support may vanish.
A zero-probability record remains as possible:false and is not empirical evidence.
Never divide by a zero pair inclusion or infer full-target support from one record.

Expected joint_supported equals the supported supplied target T_q^+.
Mean minus full T_q includes unsupported terms; keep that bias even when the
supported mean is exact. For each method retain coefficient errors:
mean-C_q=(mean-T_q)+(T_q-G_q)+(G_q-C_q).
Source-aware support inventories and covariances are not observer output.

For ordered source chain pairs A,B with pi(A),pi(B)>0, compute
Cov(q,r)=alpha_q*alpha_r*sum w_A*w_B*
[pi(A union B)/(pi(A)*pi(B))-1].
Keep overlapping chains, diagonal/shared cells, negative cross-degree signs,
and zero union-inclusion terms. Up-to-four distinct eligible cells may occur.
Also compute both methods' complete covariance by the same full original law;
primary uses centered products, reference uses second moments minus mean products.
Do not treat an unsupported full-target estimator as unbiased because its
variance is zero.

## Complete retained wire

All scalar mathematical values are reduced [numerator,positive_denominator]
native integer pairs; indices/counts native ints, flags native bools.
Canonical JSON uses sorted keys, compact separators, ensure_ascii and newline.
Every retained integer component at most4096bits; no floats in mathematics.
Runtime metadata is outside the mathematical suite.

build_case returns exactly
{case_id,level,source,design,geometry,population,samples,moments,union_covariance,counts}.

geometry is probe-ordered. Each item exactly
{probe,volume,cell_clips,pair_cells,pair_discrepancy}.
cell_clips is eligible ordered [{event,volume}].
pair_cells is full eligible Cartesian order, first outer then second:
[{first,second,representative_precedes,clipped_product,causal_integral}].
pair_discrepancy exactly
{geometric_target,clipped_order_sum,cross_cell_integral,within_cell_integral,
 continuum_pair,boundary_error,cross_order_error,omission_error,total_error}.
These are UNSCALED pair measures P_g,K,Jcross,Jdiag,J and their signed differences.

population is probe order then degree0,1,2. Each item exactly
{probe,degree,scale,chains,supplied_target,geometric_target,continuum_target,
 supported_target,unsupported_chains,annotation_error,quadrature_error,
 full_target_supported}.
All targets/errors here are SCALED COEFFICIENTS. scale=alpha_q.
chains, lexicographic original-ID vertex order:
[{vertices,eligible_mask,inclusion,weight}]; weight is unscaled supplied product.
unsupported_chains contains vertex lists of pi=0 chains; supported_target
omits those. full_target_supported means no actual full-source chain omitted.
An empty source-chain set is supported vacuously; do not invent a support failure.

samples, in mask order, exactly
{mask,probability,possible,record,packet_sha256,questions}.
Questions exactly {probe,degree,chains,unsupported_observed_terms,estimates};
chains is the same retained-only chain wire above, and estimates exactly
{raw,joint_supported}, scaled coefficients.
observe(packet) returns this complete sample object; packet hash includes
only the declared observer fields. record must be detached input data.
No source population or geometry in observe output.

moments exactly {raw,joint_supported}; each
{mean,bias,covariance,errors}.
Vectors/full square matrices follow population question order.
errors rows {probe,degree,sampling_bias,annotation_error,quadrature_error,total_error}.
union_covariance is the full joint_supported coefficient covariance matrix.
counts exactly
{mask_rows,positive_rows,questions,source_chain_terms,observed_chain_terms,
 ordered_supported_chain_pairs,zero_union_pairs,max_union_size}.
ordered_supported_chain_pairs counts all supported source terms across all
ordered question pairs, including degree0 empty chains; max_union_size is
maximum popcount of their union, zero if none.

Suite exactly {cases,controls,prior_bridges,totals,scope}.
totals sums each case counts field EXCEPT max_union_size, whose aggregate is max;
add cases27. These are enumeration counts, not independent experiments.
controls contains {refinement,boost,dilation,stale_marks}.
refinement: source-family ordered, then coarse level, then probe:
[{source,coarse,fine,probe,geometric_coefficient_change,
 signed_error_change,absolute_error_change,within_cell_change}].
The first three changes are q2 scaled fine-minus-coarse; within_cell_change
is unscaled Jdiag fine-minus-coarse. Report all outcomes, no monotonicity demand.
boost and dilation: level ordered
[{level,volume_factor,full_geometry_scaling,full_population_scaling,
 sample_coefficients_scaling,full_moment_scaling}].
factor1 and4. Degreeq coefficients scale factor^q, covariance(q,r)
factor^(q+r), all pair measures factor²; inclusion law/order unchanged.
Compare all applicable fields, not selected booleans without numerical checks.
stale_marks: level ordered
[{level,public_samples_equal_grid,geometric_pair_data_equal_warp}].
Public equality covers records, hashes, all sample questions; geometry equality
is complete geometry wire. Stale annotations are not repaired.

prior_bridges exactly
{AH_case_ids,AH_sources_designs_equal,AH_sample_records_equal,
 AH_linear_populations_equal,AH_raw_inclusion_means_covariances_equal,
 AF_math_replayed:false,other_prior_math_replayed:false}.
Compare all27 source/design/record wires against AH. Reconstruct every AH
linear population row (members, overlaps, T,G,V and signed errors).
For q1 mean and covariance, raw corresponds to AH raw, joint_supported to
AH inclusion, with factors -1/4 and1/16. Retain boolean equality results
only after actual complete projected checks; no historical engine imports.

scope all false:
generic_production_API_hardened,unknown_geometry_reconstructed,
marks_authenticated,kernel_error_bound_established,continuum_limit_established,
cross_level_observation_transport_proved,quantum_channel_constructed,
gravity_derived,empirical_data_used,ret_integration_tested.

## Verification, identities and publication

Pin AH results.json:14,297,174 bytes, SHA256
49b911c74a2e1428cb3b378ec2bf33c77feb80ab8cab213a26cd005531429bb8.
Authenticate AH's38 prior captures as39 captures total, its seven sources,
and the seven AG sources authenticated through AG's retained ledger.
No historical mathematics beyond stated AH projections is replayed.

Freeze these five AI sources before fixed execution:
README.md,kernel.py,reference.py,study.py,test_qr05ai.py.
Implementations and generic hand tests precede fixed calculation. Primary
and reference MUST NOT execute fixed build_case until root explicitly releases
the frozen comparison. Root may inspect source and generic synthetic hands.
Test collection/generic hands must not build the fixed cases implicitly.
Disclose every later source/protocol/fixture correction; never hide mismatches.

Root orchestrates exact full case and full suite equality, independent integral
hands, mutation tests, native serialization, source/prior identities and capture
lifecycle. Reference replay/audit uses its own case mathematics and no primary
engine; shared study orchestration checks comparison controls/provenance but
is not an independent third arithmetic route. No generic admission/fuzz or
all-live-cap coverage is advertised for this private diagnostic.
Capture cap96MiB, working mathematical suite cap128MiB; max27cases,
8cells,5probes,256masks per case. Scope stays bounded.

Use isolated Python with fresh external bytecode caches, no dependency installs.
After first comparison, external create-only preflight, frozen normal/-O tests,
exclusive final capture and fresh read-only exact primary/reference replays.
Keep final/source/prior bytes unchanged. No overwriting or symlink following
for evidence. Lifecycle tests use only temporary paths. Never write Python
bytecode into the checkout. RESULTS.md and roadmap are outside the frozen ledger.
Normal scoped lint/format/whitespace checks must pass before source freeze.
Gate publication includes only this directory and research roadmap.
