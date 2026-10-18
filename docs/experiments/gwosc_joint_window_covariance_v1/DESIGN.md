# RI-118 — shared-window covariance: a minimal synthetic joint model

26 September 2026 UTC. **Analytic/design packet for independent review.**
No simulation, coefficient contraction, observed-data calculation, new data
acquisition or runtime admission has occurred. RI116's accepted result and
public-data recipe remain unchanged. This supplies a conventional arithmetic
qualification design, not a detector-noise model or native forward prediction.

RI116 is published in remotely verified `c34980cb05832a57a8b503a2d070ace430f54555`
according to the coordinator's assignment. Source identities read for this
packet are in `PREDECESSOR_PINS.json`; coordination-document pins are historical
context snapshots, not future live execution dependencies.

## 1. Use the existing expectation identity, now with a joint input

RI104 equation (5) already identifies the missing terms in `E[V]`: covariance
of the finite sample mean and dispersion of the window means. Do not rederive
that identity or treat its unknown terms as zero. Define them constructively.

For one fixed detector and side, retain `n=7` left or `n=6` right, the original
starts `s_a`, `M=16384`, `T=10961`, stride `d=8192`, and the unchanged eight-row
exact finite operator `A=Q-P`. Let `W_a` select coordinates
`[s_a,s_a+T)` from one common length-131072 nominal raw vector `X`. Its M-window
selector is `S_a`, and `B=[A,0]`, so `A W_a = B S_a`. The zero tail and first-T
crop are unchanged. Put

    L_a = A W_a,             D = stack(L_0,...,L_(n-1)),
    H_n = I_n - 11^T/n,      Pi = H_n tensor I_8.

A declared finite-second-moment model `E[X]=mu`, `Cov(X)=Sigma` then gives

    Gamma_ab = L_a Sigma L_b^T,
    Cov(bar_d) = (1/n^2) sum_(a,b) Gamma_ab,
    V(X) = X^T D^T Pi D X / n,
    E[V] = tr(Pi D Sigma D^T)/n + ||Pi D mu||^2/n.       (1)

These are the operator realization of RI104 (5), not a new expectation law.
Proof of the new representation: `Pi` is the symmetric idempotent that centers
the n eight-vectors; `||Pi D X||^2=(D X)^T Pi D X`. The displayed covariance
blocks follow by applying two fixed linear maps to the same centered X.
If `Sigma=F F^T`, the covariance contribution is `||Pi D F||_F^2/n>=0`.
This factor form supplies a joint PSD construction and a second arithmetic
route. Arbitrarily chosen cross blocks that violate PSD or shared-coordinate
identity are not models of this X.

Each scenario remains separate. No detector pooling, side selection, fitting,
new output coordinates or clock/crop changes are introduced. Cross-detector
covariance is unnecessary for these individual expectations; its absence from
this calculation is not a claim of physical detector independence.

## 2. The four existing circulant proxies do not select this joint law

RI100 supplies four finite real PSD circulant matrices `K_alpha` on M samples,
one per detector/side, and their eight-output traces `tr(B K_alpha B^T)`.
They can specify *within-window marginals*. They do not specify the cross-window
blocks `S_a Sigma S_b^T`, the raw mean vector, or an empirical stochastic law.
Overlapping windows must use one shared raw sample at every coincident index;
independent draws of whole windows generally violate this requirement.

There is a coherent completion, but choosing it is an additional premise.
For each side draw a single M-vector `Z` with covariance `K_alpha` and set
`X_j=Z_(j mod M)` throughout that side's used sample union. Circulant invariance
makes every M-window covariance equal to `K_alpha`, with shared samples exact.
Different sides can be joined as independent blocks on their disjoint used
coordinate sets and arbitrary additional blocks on the excluded gap/tail;
that independence is only one explicit mathematical completion, not evidence.

This completion imposes **exact M-periodic repeats**, including samples M apart.
Since the real recipe advances by M/2, all modeled windows alternate between
just two vectors. If their output covariance trace is t and their cross trace
is h, and the two positions occur p and q times (`p+q=n`), it gives

    E[V] = (p q / n^2) (2t-2h) + finite mean dispersion.  (2)

For the zero-mean periodic construction, the last term is zero. Equation (2)
follows from the finite identity `V=p q ||d_even-d_odd||^2/n^2`.
Here `(p,q)=(4,3)` on the left and `(3,3)` on the right. The required h is a
new cross term, not the retained scalar t. Periodic completion is a useful
stress model, not the selected first empirical noise hypothesis.

A tiny exact counterexample proves why marginal information is insufficient
in general. Take `M=4,T=3`, starts 0 and 2, `A=(1,0,-1)`, and marginal `K=I_4`.
Model W has six independent unit-variance zero-mean raw samples. Model P has
four such latent samples and raw vector `(z0,z1,z2,z3,z0,z1)`. Both models have
the same two M-window marginals, and both preserve overlapping sample identity.
Their output marginal variance is 2, but cross covariance is respectively -1
and -2. Since `V=(d0-d1)^2/4`, their expectations are **3/2 and 2**. Thus even
coherent shared-sample completions can disagree. This does not assert that
every particular singular proxy has multiple completions; it establishes that
no general cross-covariance inference follows from the existing marginal-only
contract. A chosen completion must be supplied and assessed explicitly.

## 3. Select shared raw white innovations as the smallest arithmetic model

For the first synthetic qualification select

    X = mu + sigma epsilon,
    E[epsilon]=0, Cov(epsilon)=I_131072,
    sigma=1 and mu=0 in the baseline fixture.

Use independent symmetric signs for the exact finite fixtures below. Gaussian
noise is unnecessary for these second-moment identities; no likelihood,
chi-square or distributional calibration is proposed. Synthetic units are
arbitrary. Neither sigma nor mu is estimated from the RI116 table. This extends
RI71's explicitly synthetic one-window white model to shared windows and uses
RI73's accepted coefficient/Gram premises without relabeling them as new work.

Write `Omega=A A^T`, and define `J_d[i,j]=1` iff `i=j+d`, with other entries zero.
Because `d<T<2d`, only neighboring T-windows overlap. For the selected joint law,

    Gamma_aa = sigma^2 Omega,
    Gamma_(a,a+1) = sigma^2 C,       C=A J_d A^T,
    Gamma_(a+1,a) = sigma^2 C^T,
    Gamma_ab = 0                    when |a-b|>=2.       (3)

The asymmetric C is retained; it cannot be silently symmetrized or dropped.
Summing these blocks gives the average covariance of the centered outputs,
not the covariance of the full stacked vector:

    Xi_n = (1/n) sum_a Cov(d_a-bar_d)
         = sigma^2 [(n-1)Omega/n - (n-1)(C+C^T)/n^2].     (4)

Therefore (1) becomes the directly computable two-scalar expression

    E[V] = sigma^2 [(n-1)g/n - 2(n-1)c/n^2] + b_mu,
    g = tr(Omega) = sum_(i,j) A_ij^2,
    c = tr(C) = sum_i sum_(j=0)^(T-d-1) A_(i,j+d) A_(i,j),
    b_mu = ||Pi D mu||^2/n >= 0.                          (5)

The **new** arithmetic object is the signed shift product c (and C if the full
matrix identity is checked). It is not another one-window trace refinement.
RI73's coefficient-midpoint Gram G is an enclosure reference for Omega, not
Omega itself. Reuse its actual accepted bounds; do not replace true A by its
midpoints or project midpoint rows to enforce annihilation.

There is also an analytic check independent of coefficient values. The head
and tail blocks paired by J_d are disjoint because `T<2d`; hence
`-I <= J_d+J_d^T <= I` in Loewner order. Congruence by A gives
`-Omega <= C+C^T <= Omega`, so

    sigma^2 (n-1)^2 Omega/n^2 <= Xi_n
                 <= sigma^2 (n^2-1) Omega/n^2,
    |c| <= g/2.                                         (6)

The trace factors are `[36/49,48/49]` for n=7 and `[25/36,35/36]` for n=6.
These are conditional bounds, not numerical results for the public samples.
A coefficient-enclosure implementation can bound each shifted product with
its four endpoint products, sum outward exactly and independently reconcile
the midpoint/error route. The full retained RI73 coefficient rows are needed;
a row hash, scalar radius, or RI100 trace alone cannot compute c. No such
contraction has been executed in this packet.

## 4. Mean, calibration and model error remain visible

The mean term b_mu is not bounded merely by centering the realized windows.
A common constant *nominal raw* mean cancels because the true A annihilates
constants. Arbitrary deterministic means, signals, drifts or injection effects
do not inherit that cancellation. Shared-window overlap is already represented
by (3); applying n/(n-1) would still not remove its signed c contribution.

A general nominal covariance discrepancy `Delta=Sigma_true-Sigma_model`, with
both covariances PSD and a supplied bound `||Delta||_2<=eta`, would satisfy

    |tr(Pi D Delta D^T)|/n <= eta ||Pi D||_F^2/n.         (7)

This follows from `-eta I<=Delta<=eta I` and positivity of `D^T Pi D`.
No value or validity of eta is supplied by the existing four marginal traces.
Nor does a single realized table bound b_mu or establish stationarity.

Physical calibration requires a separate observation model, for example
`X=C_cal Z+b+measurement_noise` with explicit cross-covariances if the terms
are dependent. Unknown C_cal changes both mean and covariance; nominal units
are not a bound on this operator. If a later independently justified factor F
and calibration perturbation Delta_C are supplied, the covariance contribution
change can be bounded, with `T_c=Pi D`, by

    [2 ||T_c C_0 F||_F ||T_c Delta_C F||_F
       + ||T_c Delta_C F||_F^2] / n.                    (8)

This bounds the calibrated-Z covariance contribution under that specified
factor model only. Other measurement-noise and cross terms must be accounted
for separately. It does not invent a calibration envelope or assume independent
measurement noise. RI116's blank literal Yunits, nominal V2/C02 interpretation, clear L1
NO_CW_HW_INJ flag and unresolved calibration below 10 Hz remain unchanged.

## 5. Exact prospective qualification questions

The next implementation is **synthetic only**, before any actual-operator
shift contraction or empirical comparison. Its source contract must freeze
these twelve groups, complete case inventories, expected exact values and
first-refusal reasons before execution. Nothing in this list has run here.
No observed HDF5, RI116 numeric result body, empirical PSD body or RI73 numeric
capture belongs in that first synthetic executable closure.

| Group | Fixed question and exact oracle |
|---|---|
| Q01 selectors | Toy `M=4,T=3,d=2,n=2`, raw length 6, starts 0 and 2. Compare every selector entry, shared coordinate, first-T crop and zero tail; refuse an independent replacement for the shared sample. |
| Q02 shared white | `A=(1,0,-1)`. Enumerate all 64 equally weighted sign vectors of length 6. Require full output covariance `[[2,-1],[-1,2]]`, variance of the mean `1/2`, and `E[V]=3/2`. Direct pointwise centering and (1)/(5) must agree. |
| Q03 periodic completion | Enumerate all 16 sign vectors of length 4, extend as `(z0,z1,z2,z3,z0,z1)`. Both full M-marginals remain I4; output covariance `[[2,-2],[-2,2]]`, mean variance zero and `E[V]=2`. No periodic completion is substituted into Q02. |
| Q04 dropped cross term | For Q02, independently treating the two outputs as uncorrelated predicts `E[V]=1`. Refuse this as the covariance of the declared shared-white construction, at the covariance-identity guard. |
| Q05 three windows | Same A, `M=4,T=3,d=2,n=3`, starts 0,2,4 and raw length 8. Enumerate all 256 sign vectors. Output covariance has diagonal 2, adjacent entries -1 and nonadjacent entries 0. Require `E[V]=16/9` and the full centering identity. |
| Q06 constant nominal mean | Add exactly 3 to every Q02 raw coordinate. Every output and V remains unchanged; verify using the actual A row sum, not a generic centering shortcut. |
| Q07 nonconstant mean | In Q05 add `mu_j=j^2`, j=0,...,7. Window output means are `(-4,-12,-20)`; mean-dispersion term is `128/3` and `E[V]=400/9`. Removing the deterministic term must refuse. |
| Q08 signed scaling | Apply fixed common factors -1 and 2 to complete Q02 inputs. Outputs scale by those factors and all covariance/energy quantities by 1 and 4; no absolute noise floor appears. |
| Q09 matrix orientation | Q02 with rows `(1,0,-1)` and `(0,1,-1)`. Require `Omega=[[2,1],[1,2]]`, `C=[[-1,0],[-1,0]]`, and `Xi_2=[[3/2,3/4],[3/4,1]]` entrywise. Its trace is `5/2`; transposing only one required block must refuse. |
| Q10 zero/singular cases | Zero A gives identically zero outputs/covariances/V. Q03 already supplies a nonzero singular stacked covariance. No ridge, eigenvalue tolerance or inverse is needed for these moment calculations. |
| Q11 coherent PSD construction | Verify Gamma=D F F^T D^T and all shared-coordinate equalities before using (1). The proposed scalar two-output covariance `[[2,3],[3,2]]` is not PSD and must refuse; its vector `(1,-1)` has quadratic value -2. |
| Q12 nuisance map boundary | For local toy `A=(1,0,-1)` and `C_cal=diag(1,1,2)`, `A C_cal 1=-1`: refuse universal calibrated-constant cancellation. Separately take the named algebraic bound fixture `n=2`, `D=(1,-1)^T`, hence `Pi D=D`. For (7), scalar `Sigma_model=1`, `Sigma_true=2`, `eta=1` gives contributions 1 and 2 and bound 1, attained. For (8), scalar `C_0=1`, `Delta_C=1`, `F=1` gives contributions 1 and 4 and bound 3, attained. These exact toy bounds supply no physical eta or calibration information. |

These are twelve prospective groups, not twelve executed tests. The two Q12
bound fixtures are standalone algebraic factors, not changes to the window
recipe or admitted A. Normal and optimized qualification must retain full
exact rational outputs and genuine custody,
with a separate implementation/reviewer reconstructing all finite expectations.
Assertions or Monte Carlo closeness are not substitutes for these exact guards.
All future source/runtime/resource controls must be explicit before admission;
this note supplies none and inherits no authority to run a new target.

After successful synthetic qualification, a separately reviewed integration may
reuse the complete accepted RI73 capture to enclose C/c under unchanged A,
rows, crop and coefficient premises. Preserve original gates and specify the
new result schema and meaningful enclosure checks before that contraction.
A new covariance law, Gaussian sampling, or scoring of RI116 is not automatic.

## 6. What this advances, and what stays open

This packet identifies precisely the missing joint-law premise and supplies
a minimal computable model with a signed overlap correction, a PSD construction,
a matrix bound and exact synthetic counterexamples. It does not repeat RI71's
single-window covariance or RI104's already proved expectation identity.

The next bounded task is implementation and independent exact qualification of
this synthetic joint-window arithmetic. It can proceed without more public
observations. All real-data samples used by RI116 have already been inspected;
neither this design nor new processing makes them protected validation data.
The four empirical PSD proxies use those same windows, so fitting a joint law
to their table and scoring the same table would not be independent validation.
Choosing a physical joint model, calibration bounds, mean treatment, estimation
uncertainty and a separately defined evaluation protocol remains necessary
before probabilistic interpretation. A native geometry/gravity test additionally
needs its own forward map. RET remains paused.
