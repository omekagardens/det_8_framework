# RI-118: accepted joint-window covariance design

26 September 2026 UTC. Root accepts the [unchanged design](DESIGN.md) after
complete independent proof review. The result identifies a missing joint-law
premise in the observed context comparison and supplies a minimal synthetic
model with an exact signed overlap correction. It does not select a physical
detector-noise law or qualify an implementation.

## What is established

Each window selects coordinates from one common raw vector. This preserves
identical samples at overlapping indices. Under an explicit finite-second-moment
joint input model, the centering projection realizes the already accepted
RI-104 expectation identity. The within-window marginal covariance alone does
not determine the cross-window terms.

The design gives a concrete counterexample. Two coherent models share the same
identity covariance for each four-sample window. With the same three-coordinate
difference operator and overlapping windows, independent raw samples give
expected centered energy 3/2, while an exactly periodic latent construction
gives 2. Both preserve the shared raw sample. Thus a marginal-only contract
cannot generally justify a particular joint expectation. A periodic completion
of the existing circulant proxies is possible but adds exact repeated samples;
it is not an inferred property of the detector data.

For the explicitly synthetic shared-white model, put `g=tr(A A^T)` and
`c=tr(A J_d A^T)`, where the shift d joins identical coordinates in neighboring
windows. The exact conditional expectation is

    E[V] = sigma^2 ((n-1)g/n - 2(n-1)c/n^2) + b_mu.

Here `b_mu` is the nonnegative dispersion of the window output means. It is not
removed from the expectation merely by centering a realized sample. The new
quantity is the signed cross-window product c. The prior one-window trace does
not determine it.

For the fixed geometry `d=8192 < T=10961 < 2d`, only adjacent T-windows overlap.
Their paired head/tail coordinate blocks are disjoint. This proves a matrix
Loewner bound and `|c| <= g/2`, including zero and singular operators. Under this
synthetic model, the covariance-contribution trace lies between `36g/49` and
`48g/49` for the seven left windows, and between `25g/36` and `35g/36` for the six
right windows, multiplied by sigma squared. These are analytic bounds, not
measurements of the public data.

The mean term, any covariance discrepancy bound eta, and calibration-factor
perturbations remain separate explicit premises. No value for these unknowns
is supplied by the observed result. A calibration map need not preserve nominal
constant cancellation; dependent measurement-noise cross terms require their
own accounting.

## Review and actual checks

The [independent proof review](INDEPENDENT_PROOF_REVIEW.json) checks all eight
displayed identities/bounds, exact support endpoints, matrix orientation,
identical-marginal counterexample, and all twelve prospective qualification
groups. The reviewer performed 38 tiny exact matrix/support checks, with
successful recorded completion `7f3a71`. Those checks did not enumerate sign
vectors and did not execute the proposed twelve-group qualification campaign.
Root separately read the whole design and reviewed its algebra and domains.

The original left M-window union is `[0,65536)` and right union
`[69632,126976)`. The gap and unused tail stay untouched. Adjacent T-windows
share 2769 samples; distance-two supports are disjoint. No new data, coefficient
capture or observed numerical body was read for this design review.

[Root adjudication](ROOT_ADJUDICATION.json) preserves these boundaries and binds
the exact source and independent evidence. The accepted design is 15,602 bytes,
SHA256 `d128bcab94f453bb9aa506595cd76a6b3907533924f5d1b3ed3df202706d03a4`.
Its original preparation header remains historical. Full reviewer evidence is
retained externally in `det-review-evidence/ri118-independent-joint-proof-licthAD1/`;
root evidence is in `det-review-evidence/ri118-root-review-pbvX2sYK/`.
The complete source pin check confirms required scientific documents are already
committed. Historical coordination snapshots are not future executable inputs.

## Next step and remaining premises

RI-119 is assigned source preparation for the smallest synthetic implementation
and a separately authored exact validator. It must freeze complete case IDs,
expected full outputs, first-refusal reasons and runtime/resource boundaries
before actual qualification. Primary sign enumeration and independent matrix
moment reconstruction must agree exactly under genuine normal and optimized
executions before any implementation result is accepted.

Keep the full asymmetric cross blocks in Q09: a scalar trace can miss a
transpose error. Q12's standalone one-output algebraic fixtures are distinct
from the actual eight-output operator. The first executable closure excludes
empirical inputs, RI-116's numeric result and the actual RI-73 coefficient
capture. Only a later separately reviewed integration may compute the actual
shifted coefficient cross term under the unchanged operator premises.

The public windows remain previously inspected development/calibration data.
Physical joint covariance, means, calibration, stationarity and estimation
uncertainty remain unestablished; no p-value or probabilistic score follows.
Literal blank Yunits, nominal V2/C02 meaning, the clear L1 NO_CW_HW_INJ flag and
possible injection effects, and unresolved below-10-Hz calibration remain.
Native geometry/gravity requires its own forward map. RET remains paused.
