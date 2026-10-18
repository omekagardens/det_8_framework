# QR-05F: two-stage observation consistency

6 September 2026. Bounded mathematical research based on commit
`90d40a6a430271298c5141246c5632c97a4a2d58`. No RET/core imports, dependency
changes, apparatus data, new physical laws or ontology premises. Remote sync
is deferred. Keep prior sources/artifacts immutable. Freeze the six sources
listed below after review/tests and before create-only capture.

## Question and access

Separate composition of observation laws, inverse-inclusion estimators,
conditional expectations, and access to intermediate records. An unbiased
final-sample estimator need not equal a sequential estimator or its conditional
average. Conditional support and final inclusion are different requirements.

Conditioning selection probabilities on the realized first sample is standard
two-phase sampling; see [Beaumont--Haziza (2016), section 1](https://www150.statcan.gc.ca/n1/pub/12-001-x/2016002/article/14662/01-eng.htm).
This study applies the distinction to finite chain questions and access controls;
it does not attribute conditional probability or inverse weighting to DET.

The source order is supplied for audit only. An observer knows the finite ID
frame, fixed vertices, density and two-stage design, and receives induced
transitive orders on retained IDs. It does not receive hidden source relations,
coordinates, full-chain targets or source/profile names. IDs do not encode an
available deterministic reconstruction of the missing order.

First retain eligible mask S, then a mask T subset S; fixed vertices survive
both stages. Full transcript access includes S and T and their observed orders.
Final-only access includes T and its observed order. The one proposed partial
provenance summary additionally retains the policy token r(S), defined below.
The primary route must form estimates from observed chains, not source targets.
An independent full-source chain-indicator route is an audit oracle.

## Fixed sources and ten cases

Ferrers6, standard-example S3 and chain6 use IDs 0,...,7, with bottom0 and top7.
Interior labels 1,2,3 are a_i and 4,5,6 are b_j, i,j=0,1,2. Ferrers6 has
a_i<b_j iff i<=j; S3 iff i!=j; chain6 is a total order. Add bottom below
everything and top above everything. Supplied density rho=12 in all cases.
Only the whole probe (0,7) is used, with q=0,1,2,3 internal chain vertices.

Ordinary fixed vertices are [0,7], eligible [1,2,3,4,5,6]. The additional profile
`ferrers6_fixed` is the same Ferrers6 source with fixed [0,3,7] and eligible
[1,2,4,5,6]. Its always-retained interior vertex is not randomly weighted.

Case order, exactly:

1. ferrers6 / independent
2. ferrers6 / parity_adaptive
3. ferrers6 / common_coin
4. ferrers6 / parity_hole
5. ferrers6 / first_pair
6. standard_example3 / independent
7. chain6 / parity_adaptive
8. chain6 / parity_hole
9. chain6 / first_pair
10. ferrers6_fixed / independent

For eligible-list length M, bit j refers to eligible[j]. Retain every S in
0,...,2^M-1 and every T subset S, including zero-probability transcripts.
Order transcripts by increasing S then increasing T. There are 6,804 transcript
rows, 3,534 positive joint rows, 608 first-mask rows and 608 final-mask rows.
There are 40 questions. No Monte Carlo. At most eight source events, six
eligible vertices and degree three; arithmetic components must fit 4,096 bits.

## Two-stage laws

First-stage P1(S)=2^-M except in first_pair, where every size-two S has
probability 1/binomial(M,2), all others zero. Conditional second-stage laws
are defined even for zero-P1 intermediate masks; such rows are never treated
as supported evidence.

- independent and first_pair: independently retain each member of S with r=1/2.
- parity_adaptive: independently retain each member of S with r(S)=1/3 for
  even |S|, 2/3 for odd |S|.
- parity_hole: r(S)=1 for even |S|, zero for odd |S|; the same independent
  formula becomes deterministic keep-all or keep-none.
- common_coin: one fair common coin keeps all S or discards all S. When S is
  empty, these alternatives coalesce to the single empty outcome with mass one.
  The policy token is 1/2; it denotes this design's common coin, not IID retention.

For IID laws K(T|S)=r^|T|(1-r)^(|S|-|T|) on T subset S, including 0^0=1.
For common_coin use its stated two-point law. The token is the canonical
Fraction string for r, interpreted with the known design, not a new parameter.
It reveals no extra source relation.

Define P(S,T)=P1(S)K(T|S), Pf(T)=sum_S P(S,T),
pi1(A)=P(A subset S), pi2(A|S)=P(A subset T | S), and
pif(A)=sum_S P1(S)pi2(A|S). Inclusion of the empty set is one. Conditional
inclusion is zero when A is not contained in S. Retain complete first/final
inclusion tables over the eligible frame.

## Questions, estimates and conditional support

N_q counts increasing q-element internal vertex sets A forming 0<A<7.
There is one contribution per chain set, not q! histories. Let a=A intersect E
be its eligible mask. Its coefficient scale is
alpha_q=(-1)^q/(2^(q+1)rho^q), for the coefficient of z^q, z=mass².
These are formal signed scalar coefficients, not CP maps or Born probabilities.

Use three operational estimates on every transcript, from chains observed in T:

- final_joint: sum 1/pif(a) where pif(a)>0; omit zero-inclusion terms explicitly.
- sequential_supported: sum 1/(pi1(a)pi2(a|S)) where both factors are positive;
  explicitly omit other terms, including on impossible transcript rows.
- naive_quarter: sum 4^|a|. This is a prespecified uniform-independent-quarter
  correction, not a fitted actual marginal model for every case.

The first-stage comparator H1 is sum 1/pi1(a) over chains observed in S with
positive pi1. Fixed internal vertices have eligible support empty and weight one.
Store conditional means E[Hseq|S] using the explicitly defined K, their signed
defects from H1, and question-wise conditional_full_support flags. The latter
flag is false iff an observed S-chain with positive pi1 has zero pi2; it does
not silently promote zero-P1 S to an attainable intermediate state.
On zero-P1 rows, these means are only evaluations of the specified conditional
kernel K, not conditional expectations on a probability-zero event.

For each full-source chain retain pi1, pif, and fractional path coverage

```text
gamma(a) = sum_(S contains a, pi2(a|S)>0) P1(S) / pi1(a), if pi1(a)>0;
           0 otherwise.
E[Hseq] = sum_source_chains gamma(a).
E[Hfinal] = count_source_chains with pif(a)>0.
```

Thus sequential coverage is not necessarily an integer supported-chain count.
Store every positive-P1 conditional-hole mask for each chain, first/final
supported counts, sequential coverage target, and separate full-final-support
and full-sequential-coverage flags. Empty chain families are vacuously supported.
Zero inclusion is never a divisor; zero-probability rows remain visible.

## Conditioning back to the final observation

For every positive-Pf final T, compute B(T)=E[Hseq|T] and its conditional count
covariance from the retained transcript law. The source order is fixed, so its
observed order on T is fixed too. When Pf(T)=0, both fields are null, not a
zero-conditioned estimate. B is a conditional-average diagnostic, not defined
on impossible final observations and not assumed equal to final_joint.

Retain exact mean/bias/count covariance and alpha-scaled coefficient mean/bias/
covariance for all three operational methods plus rb_sequential (B on positive
final rows). Bias always compares with the full target, not a supported target.
Verify the matrix identity

```text
Cov(Hseq) = Cov(B) + E[Cov(Hseq|T)].
```

Each covariance is a weighted centered outer-product matrix and must be positive
semidefinite. Conditional averaging preserves the sequential mean, including any
support-hole bias. This does not give a uniform variance ordering between the
separate final_joint and sequential estimators.

## One bounded partial-provenance control

For positive-probability transcripts compare three access keys:
final_only=T; policy_token=(T,r(S)); full_stage1=(T,S).
Within each key, test whether the sequential estimate vector is constant.
An unequal pair is a computability/measurability witness for that estimator,
not a theorem that no other estimator of the final sample works.

Separately ask one permitted conditional continuation question: the probability
that eligible[0] appears in an independent repeat of the same second-stage
acquisition from the same intermediate S. It equals pi2({eligible[0]}|S).
No third evolving order or quantum operation is introduced. Compare this scalar
within the same keys. Preserving one estimator is weaker than preserving this
conditional prediction; success on this scalar would still not certify the full
conditional observation law. This is the only partial-provenance extension.

Retain the first collision for each question: scan positive transcripts in
increasing (S,T), compare with the first representative for that key, and record
the first differing component. Repeat-probability witnesses use question_index=0.
Flags report exact equality, with no tolerance or classification as noise.

## Prespecified analytical controls

- Independent stages compose to IID quarter retention. Sequential, final and
  naive estimates agree pointwise. Ferrers6/S3 means(N,R)=(6,6), Var(N)=18,
  Cov(N,R)=36, and Var(R)=138/126. The fixed-interior case weights its fixed
  vertex once, never four times.
- For parity_adaptive on six eligible vertices, final inclusion by support
  size 0,...,6 is [1,1/4,5/72,1/48,17/2592,11/5184,1/46656]. Sequential and
  final means recover all targets. For T={1}, S={1} and S={1,2} have joint
  probabilities 1/96 and 1/288 and sequential N estimates 3 and 6; final N is4.
  B_N(T)=570/119, not4, and Pf(T)=1309/23328. Ferrers sequential Var(N)=21,
  final Var(N)=64/3; therefore final HT does not uniformly dominate sequential.
- For common_coin every vertex has final inclusion 1/4, but a nonempty support
  of size k has inclusion 2^(-k-1). Correct sequential/final means(N,R)=(6,6),
  while naive_quarter means are(6,12). For Ferrers, correct Var(N)=48,
  Cov(N,R)=60 and Var(R)=104.
- For parity_hole, final inclusion is positive for every chain but conditional
  support fails. Ferrers sequential means are [1,3,3,0], final means [1,6,6,0].
  Chain6 sequential means are [1,3,15/2,10], final means [1,6,15,20].
- For first_pair, chain6 degree-three first/final inclusion vanishes and its
  supported/coverage targets are zero, while the full target20 remains visible.
- The policy token suffices for the sequential estimate in every case. Under
  parity_adaptive it does not suffice for the repeat prediction: final T empty,
  S empty and S={1,2} share token1/3 but repeat probabilities are0 and1/3.
  These are both supported histories. Full S suffices for both declared targets.

## Exact wire contract

Input exactly {schema_version:"det8-qr05f-problem-v1",profile:name,design:name}.
Only the ten combinations above; reject all other keys/types/values under -O.
No implicit Boolean/integer, tuple/list or Fraction/string coercion.

```text
analysis:{profile,design,density,past,fixed,eligible,stage1_probabilities,
 final_probabilities,stage1_inclusions,final_inclusions,questions,first_rows,
 transcripts,final_rows,moments,variance_decomposition,access,counts}
questions:[{degree,scale,target_count,target_coefficient,chains,
 first_supported_count,final_supported_count,sequential_coverage_target,
 full_final_support,full_sequential_coverage}]
chains:[{vertices,eligible_mask,pi1,pif,path_coverage,conditional_hole_masks}]
first_rows:[{mask,probability,kept,past,policy_token,first_estimates,
 sequential_conditional_mean,conditional_defect,conditional_full_support,
 repeat_probability}]
transcripts:[{stage1_mask,final_mask,conditional_probability,joint_probability,
 estimates:{final_joint,sequential_supported,naive_quarter},
 omitted_terms:{final_joint,sequential_supported}}]
final_rows:[{mask,probability,kept,past,chain_counts,final_estimate,naive_estimate,
 conditional_sequential_mean,conditional_sequential_covariance}]
moments:{method:{mean_counts,bias_counts,covariance_counts,
 mean_coefficients,bias_coefficients,covariance_coefficients}}
variance_decomposition:{sequential_covariance,rb_covariance,
 mean_conditional_covariance,residual}
access:{key_name:{estimator:{measurable,first_collision},
 repeat_prediction:{measurable,first_collision}}}
first_collision:null|{question_index,
 left:{stage1_mask,final_mask,value},right:{stage1_mask,final_mask,value}}
counts:{events,eligible_events,first_rows,positive_first_rows,final_rows,
 positive_final_rows,transcript_rows,positive_transcript_rows,questions,
 chain_terms,estimator_cells}
```

All vectors are in q=0,1,2,3 order, all covariance matrices are4x4. All scalar
arithmetic values and estimate/moment vectors are canonical Fraction strings,
including integral values. Counts, degrees, masks and vertex IDs are native
integers; flags are native Booleans. Source past and chain vertices use original
IDs; each observed past uses local indices in sorted kept. Chain sets are sorted
lexicographically. All mask rows are increasing; conditional_hole_masks are
increasing and contain only positive-P1 masks containing that chain support.
Omitted-term and chain-count vectors contain integers. rb_sequential appears
only in moments, not operational transcript estimates. No unlisted output keys.

Sources bound at capture: README.md, sequential.py, reference_qr05f.py, study.py,
test_qr05f.py and test_capture.py. Bind the QR-05E artifact (SHA256
`362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41`)
and its nine priors. Reproduce full source targets and explicit first-stage
single-observation laws from pinned QR-05E JSON, never its executors. Preserve
its geometric/quantum/identification counterexamples by byte identity, without
claiming to rerun or repair them. Whole-suite native JSON round trips must pass
before capture. Replay is read-only and exact. Outcomes belong in RESULTS.md;
post-capture source corrections require a new retained version.

## Reproduction

From the checkout root using the existing environment, with a fresh external
bytecode cache for each invocation. No installation or prior-executor imports.

```sh
qr05f_test_cache=$(mktemp -d /tmp/det8-qr05f-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05f_test_cache" -m pytest -p no:cacheprovider -q docs/validation/qr-05f-two-stage-2026-09-06/test_qr05f.py docs/validation/qr-05f-two-stage-2026-09-06/test_capture.py

qr05f_opt_cache=$(mktemp -d /tmp/det8-qr05f-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05f_opt_cache" -m pytest -p no:cacheprovider -q docs/validation/qr-05f-two-stage-2026-09-06/test_qr05f.py docs/validation/qr-05f-two-stage-2026-09-06/test_capture.py

# Create only after all six sources are reviewed, tested and frozen.
# If results.json already exists, use --verify instead; never overwrite it.
qr05f_capture_cache=$(mktemp -d /tmp/det8-qr05f-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05f_capture_cache" docs/validation/qr-05f-two-stage-2026-09-06/study.py

qr05f_replay_cache=$(mktemp -d /tmp/det8-qr05f-replay.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05f_replay_cache" docs/validation/qr-05f-two-stage-2026-09-06/study.py --verify
```

The native-JSON guard and complete aggregate round trip must pass before capture.
Runtime measurements sit outside the exact mathematical suite. Lifecycle tests
use only temporary stub evidence for overwrite, symlink and corruption checks.
Read-only replay checks source/prior identities and exact suite equality without
changing the capture. Remote publication is a separate deferred operation.
