# QR-05E: sampling-aware order and propagation questions

6 September 2026. Bounded research after QR-05D commit
`07703e939c4b2932bb6bd87d914b756fa3a42a1d`. Keep prior sources and captures,
RET/core work and dependencies unchanged. Freeze this protocol and executable
sources before create-only capture; later outcomes belong in RESULTS.md.

## Question and boundary

Which interval/chain questions survive a known finite observation law? Test
inverse joint-inclusion weighting, exact design means and covariances, and
what individual retained samples fail to determine. The underlying finite
order is fixed; randomness comes only from a declared sampling design.

This is a finite sampling contract, not a new growth law, reconstruction of
unknown geometry, Poisson-sprinkling validation, quantum channel, or gravitational
dynamics. Supplied density remains fixed. No unknown density fit, data-driven
sampling law, experimental observations or RET integration. The scalar kernel
coefficients are not CP maps or Born probabilities.

The weighting principle is standard finite-population sampling, applied here
to chain vertex-sets rather than individual vertices. See
[Horvitz--Thompson (1952)](https://doi.org/10.1080/01621459.1952.10483446) and the
induced-vertex motif estimator in [Klusowski--Wu, section 2.1](https://proceedings.mlr.press/v75/klusowski18a/klusowski18a.pdf).
Our exact finite study and retained counterexamples are the contribution here;
the sampling principle is not attributed to DET.

## Population, access and fixed probes

There are four possible supplied source orders, with naturally labeled strict
past lists. Only the 17 order/design combinations below are admitted.

- `ferrers6`: interiors a_i < b_j iff i <= j, i,j=0,1,2, ordered a then b.
- `standard_example3`: interiors a_i < b_j iff i != j, with the same labels.
- `chain6`: six interiors in one total order, used only with singleton sampling.

For these three sources, add bottom 0 and top 7; interior labels are 1,...,6.
Bottom/top are always retained, all six interiors are eligible, rho=12 is a
supplied algebraic scale, and the only probe is `whole` (0,7).

- `mesh3_center`: the eleven-event tilted mesh3 from QR-05D. Its interiors
  (i,j), i,j=1,2,3 in lexicographic order, have product-grid order
  `(i,j) < (k,l)` iff i<=k, j<=l and the pairs differ. Add bottom 0, top 10.
  Fixed events are 0,5,10; eligible labels are 1,2,3,4,6,7,8,9. Rho=18.
  Probes, in order: `whole` (0,10), `bottom_to_middle` (0,5),
  `middle_to_top` (5,10). No new coordinates or geometric errors are fitted.

The observer receives the original IDs of retained events and the **induced
transitive order** on them. It knows the finite ID frame, fixed probes, density
and sampling design, but is not given the missing order relations, full chain
inventory, target values, geometric coordinates or fixture/source name. Source
names such as `chain6` are audit metadata, not observer information that reveals
the hidden source. This is an explicit access
assumption: retained Hasse edges alone would be a different observation channel.
Original IDs do not by themselves reveal missing relations; no deterministic
coordinate-to-ID reconstruction is available to the observer.

The primary estimator constructs chains only in this received induced order.
Full-source chains and targets are retained for audit and support classification,
not used to insert missing contributions into a sample estimate. The reference
may use full-source chain indicators as a separate oracle calculation to check
the observed-order route. The entire source family remains mathematical input,
not a claimed apparatus model.

## Exact sampling designs

Let E be the ordered eligible list, M=|E| (6 or 8), and S a retained subset of E.
Encode S by the integer mask whose bit j refers to E[j]. Keep all 2^M masks in
evidence, including structural probability-zero rows. Fixed probes are not in
the random mask and never receive a random-vertex weight.

For ferrers6, standard_example3 and mesh3_center, use each of these five designs:

1. `identity`: retain all E with probability one.
2. `iid_half`: each eligible vertex independently retained with probability 1/2.
3. `heterogeneous`: independent probabilities 1/3,2/3,1/3,2/3,... by eligible-list
   position. These probabilities are known design inputs, not estimated density.
4. `all_or_none`: empty S and full S each have probability 1/2, all others zero.
5. `fixed_size2`: every two-element subset has probability 1/binomial(M,2).

Additionally use `singleton` for ferrers6 and chain6: each one-element subset
has probability 1/6, all other masks zero. Thus there are 17 fixtures, 2,048
retained mask rows and 847 positive-probability rows. No Monte Carlo draws.

For every subset A of E compute its joint inclusion probability
`pi(A)=sum_(S superset A) P(S)`, including pi(empty)=1. The same M-bit index
convention applies to this complete inclusion table. Every vertex marginal is
positive in these designs, but higher joint inclusions need not be.

## Questions, estimators and support

For each fixed probe (a,b), take degrees q=0,1,2,3 in that order. A contribution
is an increasing q-element internal vertex-set A forming the chain a<A<b;
q=0 is the empty internal set. There is one chain per such set, not q! paths.
Let T=A intersect E be its random eligible support. Other fixed probe events
may occur inside A and contribute no inclusion factor.

The count target is N_q(a,b), and the corresponding scalar-kernel coefficient
is `alpha_q N_q`, where `alpha_q=(-1)^q/(2^(q+1) rho^q)` for z^q, z=mass².
This extends the QR-05D all-pair questions by one formal coefficient, not by a
finite-mass approximation or a new scalar-field law. Question order is probe
order then degree. There are 4 or 12 questions per fixture, 108 in total.

For each observed sample, sum over its observed chains only, using four methods:

- `raw`: weight one.
- `marginal_product`: weight 1/product_(i in T) pi({i}).
- `uniform_rate`: weight 1/pbar^|T|, pbar=mean eligible-vertex marginal.
- `joint_supported`: weight 1/pi(T) when pi(T)>0; omit pi(T)=0 terms explicitly.

All empty products are one. The first three methods remain defined on all
retained masks. For `joint_supported`, retain the count of omitted observed
terms in every question. These can occur only on probability-zero sample rows.
No division by zero is permitted, and zero rows are never conditionally normalized.

For each question separately retain all full-source chain sets, their eligible
masks and inclusion probabilities, the list of zero-inclusion chain sets,
the supported target count and `full_target_supported`. If the latter is false,
`joint_supported` estimates only the supported projection, **not** the full target.
An empty full-chain family is vacuously supported even if unrelated subset
inclusions vanish. The support classification is a full-source audit result,
not information inferred from one observed sample.

The exact expectation identity is linearity:

```text
E[sum_(observed A, pi(T)>0) 1/pi(T)] = number of supported source chains.
```

It equals the full count only when all target chains have positive inclusion.
Multiplying vertex marginals is justified for independent sampling, not general
correlated selection. A uniform scalar rate is still less informative under
heterogeneous retention. Keep density fixed; do not use realized |S|/volume.
The usual rho->p*rho equivalence for uniform thinning requires every internal
vertex to be eligible. It does not hold unchanged for the fixed-center mesh.

## Exact variability, not just averages

Enumerate each method's exact mean, bias against the full source target, count
covariance, and corresponding coefficient mean/bias/covariance by multiplication
with alpha. Also retain, for each question and the entire vector, the probability
that its sample estimate equals the full source target exactly. Equality uses
rationals, not a tolerance or a claim of practical statistical accuracy.

Independently compare the enumerated joint-supported count covariance with

```text
Cov(H_q,H_r) = sum_(supported A,B) [pi(T_A union T_B)/(pi(T_A)pi(T_B)) - 1].
```

This covariance is an oracle diagnostic using the source/design, not an unbiased
variance estimate available from one sample. A zero union inclusion is allowed
and contributes a negative term; do not divide by it. Cancellation matters for
fixed-size designs. The covariance is positive semidefinite as the exact weighted
sum of outer products of centered vectors, not because scalar kernels are CP.

## Prespecified analytical and access controls

- Under iid_half, Ferrers6 and S3 both have HT means (N,R)=(6,6), Var(N)=6
  and Cov(N,R)=12, but Var(R)=34 versus 30. Their entire unthinned endpoint
  polynomials agree in QR-05D; their thinning-response laws need not agree.
  In either case the corrected R estimate is a multiple of four, hence it
  never equals the full target six in a single sample, despite unbiasedness.
- Under all_or_none, joint weighting uses factor two for every nonempty
  eligible support. Marginal products use 2^|T| instead. For either six-event
  two-level order the wrong mean R is 12 instead of 6, and the wrong z² mean
  is 1/96 instead of 1/192. A single density rescaling cannot fix all degrees.
- fixed_size2 supports every one-/two-eligible-vertex contribution but not
  three-eligible-vertex chains in mesh3_center. Keep the unsupported degree-3
  chains visible. This is a limitation of the chainwise estimator, not a proof
  of universal statistical nonidentifiability. Repeated labeled size-two
  observations can in principle expose each relation.
- The singleton Ferrers6 and chain6 observation laws are exactly identical:
  each received labeled order is bottom < chosen vertex < top with probability
  1/6. Yet the full related-pair targets are 6 versus 15, and degree-3 counts
  are 0 versus 20. No estimator based solely on this declared observation law
  can be unbiased for those different targets over both sources, even with
  any fixed number of independent repetitions. This is a genuine channel-relative
  identification obstruction, not merely a zero-inclusion warning.
- Restrict the original Hasse link matrix to the retained vertices, then take
  reachability. Store whether each fixed probe remains connected under this
  deliberately wrong channel. The correct induced order retains each probe
  comparison; erasing intermediate links can lose it. Retain the first
  positive-probability mismatch and total mismatch probability, not just an
  impossible zero-weight example.

No sample is called an experimental anomaly. The preserved QR-05D local-volume
ambiguity and S3 embedding obstruction are not repaired by unbiased count
correction. Nor are the QR-05C record-location or delayed quantum-map failures.

## Canonical interface and output

Input is exactly `{schema_version:"det8-qr05e-problem-v1",order:name,design:name}`,
with only the 17 declared combinations. Reject other keys, types and values
including under -O. This is a fixed-fixture research interface, not a new SDK.

```text
analysis:{order_name,design,density,past,fixed,eligible,probes,
          inclusion_probabilities,questions,samples,moments,
          joint_covariance_formula,observation_law,hasse_control,counts}
probes:[{name,source,target}]
questions:[{probe,degree,scale,target_count,target_coefficient,chains,
            zero_inclusion_chains,supported_count,full_target_supported}]
chains:[{vertices,eligible_mask,inclusion}]
samples:[{mask,probability,kept,observed_past,chain_counts,
          unsupported_observed_terms,estimates,hasse_only_reachability}]
estimates:{raw,marginal_product,uniform_rate,joint_supported}
moments:{method:{mean_counts,bias_counts,covariance_counts,
                mean_coefficients,bias_coefficients,covariance_coefficients,
                exact_target_probabilities,vector_exact_target_probability}}
observation_law:[{kept,past,probability}]
hasse_control:{mismatch_probability,first_mismatch}
first_mismatch:null | {mask,kept,probes}
counts:{events,eligible_events,mask_rows,positive_rows,questions,chain_terms,
        estimator_cells}
```

`probe` in a question is the probe's name. Source past and chain vertices use
original IDs. `observed_past` and observation-law past rows use local indices
in sorted `kept`; absent relations are not disclosed. Observation law contains
only positive-probability rows in increasing mask order; this is not a deletion
from the full retained sample table. First mismatch also uses increasing mask
order and contains the names of probes whose Hasse-only reachability is false.

Question chains are lexicographically sorted vertex lists. Every estimator
vector is in question order; covariances are square row-major matrices in that
same order. Estimates and moments are canonical Fraction strings, including
integral values. Count and mask fields are exact integers, flags are Booleans.
Every arithmetic component must fit 4096 bits. No implicit tuple/list or
Boolean/integer coercions: use a recursive native-JSON guard and canonical-byte
comparison on complete executor outputs, the aggregate suite and replay.

The primary route generates samples from the design, restricts the transitive
order, and enumerates chains in each observed order. The reference independently
counts full-source chain indicators and computes subset probabilities and
moments. Both calculate the covariance identity independently. Tests additionally
check analytical controls, strict schemas, aggregate wire round trips and safe
create-only capture/read-only replay, normally and optimized.

Pin QR-05D results-v2.json and earlier evidence. Reproduce all four endpoint
chain counts/coefficient targets for Ferrers6, S3 and mesh3 from QR-05D, and
its first three local-probe coefficients for mesh3; record the direct dependency
checks. Preserve the prior geometric and quantum counterexamples by identity,
not by importing prior executors or claiming new tests of their physics.

Sources bound at capture: this protocol, thinning.py, reference_qr05e.py,
study.py, test_qr05e.py and test_capture.py. Runtime measurements are outside
the exact mathematical suite. Original evidence is immutable; any required
post-capture source correction needs a new version with retained failure history.

## Reproduction and freeze discipline

From the checkout root, using its existing Python environment; no installation
or RET/core imports are needed. Each invocation gets a fresh external cache.

```sh
qr05e_test_cache=$(mktemp -d /tmp/det8-qr05e-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05e_test_cache" -m pytest -p no:cacheprovider -q docs/validation/qr-05e-sampling-aware-2026-09-06/test_qr05e.py docs/validation/qr-05e-sampling-aware-2026-09-06/test_capture.py

qr05e_opt_cache=$(mktemp -d /tmp/det8-qr05e-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05e_opt_cache" -m pytest -p no:cacheprovider -q docs/validation/qr-05e-sampling-aware-2026-09-06/test_qr05e.py docs/validation/qr-05e-sampling-aware-2026-09-06/test_capture.py

# Run this create-only step only if results.json does not exist.
qr05e_capture_cache=$(mktemp -d /tmp/det8-qr05e-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05e_capture_cache" docs/validation/qr-05e-sampling-aware-2026-09-06/study.py

qr05e_replay_cache=$(mktemp -d /tmp/det8-qr05e-replay.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05e_replay_cache" docs/validation/qr-05e-sampling-aware-2026-09-06/study.py --verify
```

Run the whole aggregate JSON round-trip test before capture. Freeze all six
listed sources after review and passing tests; capture binds their exact bytes
and nine prior artifacts, including both retained QR-05D versions. Replay checks
the full native mathematical suite and identities without modifying the report.
Tests of writes and corruption use temporary stub evidence only.
