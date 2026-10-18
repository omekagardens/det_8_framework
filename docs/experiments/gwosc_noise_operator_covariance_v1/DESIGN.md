# RI-71 — fixed-operator covariance under synthetic unit white noise

24 September 2026 UTC. **Prospective design; independently accepted.**
This document authorizes no coefficient reconstruction, sampling or observed
input processing. The next implementation requires a separate reservation,
source review and execution freeze. No result of the proposed covariance gate
is known yet.

The objective is one deterministic certificate for the unchanged eight-output
context-minus-short operator under a deliberately specified mathematical noise
model. It follows [RI-67](../gwosc_context_noise_v1/DESIGN.md), whose surrogate
simulation was qualified in RI-68, and the exact finite operator already
qualified in [RI-60](../gwosc_context_operator_v2/IMPLEMENTATION.md). Surrogate
sampling success does not qualify the covariance of this operator. This step
addresses that missing integration before considering a sampler or data score.
It advances ME-02 of the [measurement plan](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md);
ME-03 still requires a quantitative native source/observer forward law.

## 1. Fixed operator, domain and synthetic model

Keep N=2769, L=4096, T=N+2L=10961 and the ordered central rows
I=(0,1,27,805,1384,2741,2767,2768). F_m is the exact rational finite filter of
RI-55/60, including all 17 ordered stages, per-stage odd extension, initialized
forward/reverse passes and unpadding. Its coefficients are the exact rationals
represented by the admitted binary64 SOS entries. Rounded SciPy or Decimal80
evaluations are not the definition of F_m.

Let E inject N central coordinates into T coordinates, C=E^T select them, and
J select I from an N-vector in the stated order. Define eight-by-T matrices

```text
P = J F_N C,        Q = J C F_T,        A = Q-P.                 (1)
```

The extended coordinate order is left context, center, right context. Central
coordinate i is extended coordinate L+i. The sample spacing remains 1/4096
second. The recorded RI-64 windows were center [65536,68305) and extended
[61440,72401), but no recorded vector is an input to this design or its first
implementation. Here a length-T vector is only a synthetic algebraic input.
The existing filter, grid, rows, window lengths and arithmetic remain fixed.

Select the fixed known model xi ~ N(0,I_T), with zero mean and one arbitrary
synthetic input unit of standard deviation per coordinate. Then

```text
Y=A xi,       Omega=A A^T
 = Q Q^T + P P^T - Q P^T - P Q^T.                              (2)
```

The short and extended outputs share the same xi. Their cross covariance is
Q P^T, generally not symmetric; its transpose supplies the other cross term.
Independence cannot be inferred from distinct filter lengths. Unit-white
covariance is an explicit assumption, not an estimate from H1/L1. Omega has
squared synthetic input units because A is dimensionless. No detector noise,
spectral stationarity, amplitude, calibration or physical strain uncertainty
has been qualified by selecting this model. No second detector or assumed
inter-detector independence is added in this step.

## 2. Coefficient custody and reconstruction prerequisite

RI-60's qualification JSON retains row summaries, hashes, proof traces and
maximum radii; it does **not** archive every coefficient interval. RI-64 also
retains identities rather than the full adjoint vectors. A hash alone cannot
be multiplied into a covariance. A separately authorized implementation must
reconstruct all sixteen adjoints from the pinned sources, then reconcile all
eight summaries with the accepted RI-60 qualification before any Gram work.
There is no reconstruction in this design-only task.

Use the published RI-60 `admission`, `build_rows` and `row_summary` interfaces
or an independently reviewed wrapper executing those same retained bytes.
Each short seed is e_i in length N, each extended seed is e_(L+i) in length T.
Retain the actual interval vectors in memory for this execution. Form P's row
by embedding the short interval vector between L exact zeros on either side;
form Q's row from the corresponding complete extended interval vector. For
the center, an A coefficient interval is [Q_lo-P_hi,Q_hi-P_lo]; outside the
center it is Q's interval. Equivalently its row is (b_left,a,b_right), with
the original RI-60 b order split at L. Never concatenate all of b before a.

Verify lengths, order, exact Fraction types, finite ordered endpoints, all
existing gain-width and row-status conditions, all eight accepted row summaries,
and all sixteen proof/interval identities. Preserve the per-coordinate radii;
the reported scalar maximum is not a replacement for them. Check the inherited
constant-annihilation consequence: every A row's interval sum contains zero.
This follows from the same finite filter's length-independent constant gain;
it does not imply that interval midpoints sum to zero exactly.

The critical existing identities are:

| Dependency | Bytes | SHA-256 |
|---|---:|---|
| RI-60 operator.py | 30531 | `ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af` |
| RI-60 check.py | 38088 | `a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02` |
| RI-60 QUALIFICATION_REPORT.json | 9413345 | `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f` |
| Reused RI-57 exact oracle.py | 9484 | `37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651` |
| RI-44 COEFFICIENTS.json | 7698 | `700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0` |
| RI-55 DESIGN.md | 21702 | `e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45` |
| RI-62 DESIGN.md | 19255 | `636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2` |
| RI-67 DESIGN.md | 24027 | `74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921` |

These are anchors, not the entire executable closure. Before running a helper,
read and size/hash-bind every transitively loaded source, recipe, coefficient
manifest and prior receipt, including RI-60's pinned failed predecessor and
RI-44 dependencies. Execute only those retained verified byte snapshots.
Reject duplicate/nonfinite JSON, wrong status, incomplete gate inventories,
changed sources, stages, padding, runtime or manifest. RI-60's 196 passed gates
remain prior qualified evidence; they are not relabeled as newly executed.
Current reconstruction must reproduce the eight accepted enclosure summaries.
Bind this design and the new checker source as well; the new implementation's
result must identify its exact complete input/source closure.

Use the already qualified CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1,
h5py 3.12.1 and HDF5 1.12.2 environment, including full platform/build,
byte-order and NumPy configuration equality. No installation or environment
substitution is allowed. h5py is metadata-only; no HDF5 file is opened. Do not
read CROP, REFERENCE, OBSERVED_CONTEXT, raw strain or other observational
bodies. The fixed source interface is not a hostile Python sandbox.

## 3. Exact midpoint Gram and rigorous error enclosure

For each of the 8T coefficient intervals [l_ik,u_ik], define exactly

```text
M_ik=(l_ik+u_ik)/2,    R_ik=(u_ik-l_ik)/2 >= 0,
G=M M^T,
H_ij=sum_k (|M_ik| R_jk + R_ik |M_jk| + R_ik R_jk),
delta=max_i sum_j H_ij.                                        (3)
```

G is the Gram of the **coefficient** midpoint matrix. It is not the entrywise
midpoint of an interval Gram matrix, and it is not asserted to equal Omega.
All quantities in (3) are exact Fractions, with no floating dot products,
eigenvalues or tolerance-based simplification. Compute upper triangles and
mirror them, so G and H are exactly symmetric; H is entrywise nonnegative.

**Enclosure proof.** Write A=M+B, with |B_ik|<=R_ik. Expansion of
Omega-G=M B^T+B M^T+B B^T and the triangle inequality give
|Omega_ij-G_ij|<=H_ij. This proof does not assume independent rounding errors.
For the symmetric error Delta=Omega-G,

```text
||Delta||_2 <= ||Delta||_infinity <= delta.                     (4)
```

The first inequality follows from ||Delta||_2<=sqrt(||Delta||_1
||Delta||_infinity) and symmetry. Dropping off-diagonal H entries is unsound.
The elementwise box is an enclosure of the one true Gram, not a claim that
every matrix in the box is PSD or attainable.

Also compute a direct interval Gram K_A from the A intervals. For off-diagonal
entries use the minimum/maximum of the four endpoint products per coordinate;
for diagonal entries use the interval square, whose lower endpoint is zero
when the coefficient interval crosses zero. Independently compute interval
QQ^T, PP^T and QP^T from their retained vectors, and the expansion in (2).
Preserve QP orientation and obtain PQ as its transpose. Require symmetry of
the resulting covariance enclosures and a nonempty common intersection of
K_A, the cross-term expansion and [G-H,G+H] in every entry. These are redundant
consistency checks, not independent evidence that the underlying intervals
are correct. Their overestimation can differ because dependencies were bounded
differently. Use the fixed H-based delta for the following theorem; do not
select a smaller route after seeing the numerical answer.

The exact structural fact Omega=A A^T proves PSD regardless of enclosure
width. A floating eigenvalue of the interval midpoint is unnecessary. Full
rank and useful inverse control require the stronger gates below.

## 4. Positive pivots, inverse and relative covariance theorem

Compute the unpivoted exact LDL^T factorization of G in the unchanged output
order I. Require every pivot strictly positive, verify LDL^T=G entrywise,
and solve for an exact symmetric inverse V. Verify both GV=I_8 and VG=I_8.
There is no pivot tolerance, diagonal ridge, eigenvalue clipping, dropped row
or row-dependent rescaling. This fixes a reproducible sufficient SPD test.

Set gamma=max_i sum_j |V_ij| and rho=delta*gamma. Gamma is an exact upper
bound for ||G^-1||_2 because V is symmetric. Freeze two distinct gates:

* Mathematical certificate gate: G has the verified positive pivots and rho<1.
* Numerical usefulness gate: rho<=1/10^12.

Both must pass for the first admitted-operator integration to be accepted.
The usefulness threshold is prospective; no computation of the actual rho
has been performed in preparing this design. Failure does not permit a new
precision, different rows, expanded window or alternative chosen norm.

**Theorem.** Under these gates, Omega is strictly positive definite of rank
eight and

```text
(1-rho)G <= Omega <= (1+rho)G,
V/(1+rho) <= Omega^-1 <= V/(1-rho),                            (5)
```

where inequalities are in Loewner order. Indeed V has largest eigenvalue
at most gamma, hence G >= I/gamma. Equations (3)–(4) imply
-delta I <= Delta <= delta I, and delta I <= rho G. This proves the first
line; inversion reverses positive-definite order and proves the second.
No eigenvectors or approximate Cholesky factors are needed to certify (5).
Changing a common input unit scales G, H and delta by its square and V and
gamma by its inverse square, so rho is invariant under this common scaling.

For any fixed y in R^8, define q_G(y)=y^T V y. Then

```text
q_G(y)/(1+rho) <= y^T Omega^-1 y <= q_G(y)/(1-rho).             (6)
||Omega^-1-V||_2 <= rho*gamma/(1-rho).                        (7)
```

For (7), conjugate Omega by G^-1/2. The resulting symmetric perturbation has
eigenvalues in [-rho,rho]; the inverse-minus-identity has norm at most
rho/(1-rho). Multiplication on both sides by G^-1/2 supplies ||V||_2<=gamma.
Equation (6) is preferable when a particular score is wanted. For y=0 both
endpoints are exactly zero, without a relative-error division by zero.

G being singular does not establish that the unknown exact Omega is singular.
If a nonpositive pivot stops the sufficient test, retain its exact location
and value and report `unresolved_by_fixed_gate`; a negative pivot inconsistent
with an exact Gram after positive preceding pivots is an implementation error.
Likewise rho>=1 leaves rank/inversion unresolved by this certificate, even
when all compatible matrices might actually be full rank. If 0<=rho<1 but
rho>10^-12, retain the valid theorem bounds with status `accuracy_failed`.
Neither status authorizes an accepted inverse-based inference.

Do not infer a singular rank from floating tolerances or install a pseudoinverse
fallback for the actual eight rows. A general rank-deficient certificate would
need an exact common kernel and a proved positive restriction; it is outside
this first integration. Exact singleton singular and all-zero tiny fixtures
must still validate rank, all four Moore-Penrose identities and support. At
rank zero support is {0}; a nonzero vector fails support even though its
pseudoinverse quadratic is zero. These fixtures do not change the actual gate.

## 5. Deterministic output error and conditional law comparison

Numerical coefficient enclosures are not noise standard deviations. They
provide a deterministic set containing one fixed operator. For a fixed exact
synthetic vector z, let y=M z and

```text
e_i=sum_k R_ik |z_k|,   E1=sum_i e_i,   Y1=sum_i |y_i|,
B_score=gamma*(2*Y1*E1+E1^2)/(1-rho).                         (8)
```

Then |(Az-y)_i|<=e_i. Cauchy-Schwarz and
||Omega^-1||_2<=gamma/(1-rho), with Euclidean norms bounded by the stated
one-norms, show that the true quadratic of Az belongs to

```text
[max(0,q_G(y)/(1+rho)-B_score), q_G(y)/(1-rho)+B_score].        (9)
```

This is a conservative deterministic enclosure, not an estimated uncertainty
bar. A later rounded output y_hat with a separately proved component-error
bound may use the same argument around y_hat. A binary64/Decimal comparison
alone is not such a uniform bound. RI-64's actual-input endpoint tests cannot
be reused as an error guarantee for arbitrary random inputs. There are no
observed y, residuals, fitted means or scores in the present implementation.

The first implementation evaluates (8)–(9) only for the fixed T-dimensional
synthetic probes z=0, z=ones, and z=e_(L+i) for each i in I, in that order.
These ten rational probes are fixed before execution; they do not enumerate
the filter basis. Check exact nonnegative ordered score intervals, the zero
probe's exact-zero result and containment of zero for the constant probe,
using the inherited exact A*ones=0 identity. Report all ten complete results.
No usefulness threshold is silently imposed on a nearly zero probe score.

There is also a law comparison with no sampler. Under the ideal model of
section 1, use the same xi to couple Y=A xi and Y_M=M xi. Exactly

```text
E ||Y-Y_M||_2^2 = ||A-M||_F^2 <= eta2=sum_ik R_ik^2.          (10)
```

For any t>0, Markov gives P(||Y-Y_M||_2>=t)<=min(1,eta2/t^2).
The second-moment statement needs only mean zero and covariance I_T;
Gaussianity is needed for the following distributional statement.

If (5) passes, q_Omega(Y) has the exact chi-square law with eight degrees of
freedom under the fixed ideal Gaussian model. In contrast q_G(Y) is generally
a weighted sum of eight independent squared standard normals, with weights
in [1-rho,1+rho]. Diagonalize G^-1/2 Omega G^-1/2 to obtain this statement;
using the same eight normals bounds this weighted sum between
(1-rho) times chi-square_8 and (1+rho) times chi-square_8. Thus, for t>=0,

```text
F_8(t/(1+rho)) <= P(q_G(Y)<=t) <= F_8(t/(1-rho)).              (11)
```

The exact law of q_G(Y_M) is chi-square_8 when Y_M is an ideal Gaussian with
the exact covariance G. Neither assertion turns a finite PRNG stream or a
rounded matrix sampler into an exact Gaussian draw. No sampler is part of
the first implementation; (10)–(11) are its numerical-law comparison.

For a single frozen display threshold t=16, use the fixed upper bound
rho_bar=10^-12 after verifying rho<=rho_bar. Replacing rho by rho_bar in
(11) weakens the bounds conservatively. Evaluate these two CDF bounds using
exact rational intervals, not a distribution-library quantile. This fixed
coarsening also prevents the actual rho's potentially large denominator from
causing unnecessary degree-128 rational growth. It is chosen before the run;
the exact rho is still retained for (5)–(10). For
x>=0, F_8(x)=1-exp(-x/2)*sum_(j=0..3)(x/2)^j/j!. At each rational argument
u=8/(1+rho_bar), 8/(1-rho_bar), set S=sum_(j=0..128)u^j/j! and
R_tail=(u^129/129!)/(1-u/130). Require 0<=u<130. Positive series terms give
1/(S+R_tail)<=exp(-u)<=1/S. This is through degree 128, **129 terms**, with
the term-129 remainder. Propagate interval endpoints through the positive
tail polynomial and subtraction from one; require each CDF interval width
<=2^-100. Report the lower endpoint for the lower CDF and upper endpoint for
the upper CDF as a conservative probability interval in (11).

Freeze the probability-interval width gate at 10^-10, conditional on the
rho usefulness gate. This is not a Monte Carlo coverage test or significance
claim. It is conservative: the chi-square_8 density has maximum
9/(4*exp(3))<1, so the true CDF spread is at most
32*rho_bar/(1-rho_bar^2); two CDF-oracle widths add at most 2*2^-100. At
rho_bar=10^-12 this sum is below 10^-10. Even if the reconstructed rho is
zero, use this same prospective conservative comparison; do not switch to
a tighter selected display. The separate exact-rho theorem still applies.

## 6. Independent exact fixtures and refusal coverage

The implementation must pass these deterministic fixtures before admitted
row reconstruction. They use exact rational inputs and independently authored
expected answers; no selected-seed draws, actual filter coefficients or data
are needed. Preserve each named result, all expected matrices and failed gates.

1. **Shared FIR.** Reuse the independently published tiny DFI oracle on SOS
   (1,1/2,0,1,0,0), padlen 0, N=2, L=1, T=4 and both central rows. Reconstruct
   its full tiny matrices by basis vectors. Expected
   P=[[0,7/4,1/2,0],[0,3/4,3/2,0]] and
   Q=[[1/2,5/4,1/2,0],[0,1/2,5/4,1/2]]. With singleton intervals,
   G=Omega=[[1/2,1/8],[1/8,3/8]], determinant 11/64,
   V=[[24/11,-8/11],[-8/11,32/11]], H=0, rho=0.
   QP^T=[[39/16,27/16],[3/2,9/4]]; it must not be symmetrized before the
   expansion. For raw e0, output=(1/2,0) and score=6/11.
   Reject QQ^T+PP^T=[[43/8,53/16],[53/16,39/8]] as this fixture's covariance.
2. **Shared cancellation.** At the same lengths use the identity filter:
   P=Q=C, A=0, Omega=0 even though both marginal covariances are I_2.
   A nonzero output fails support. Reject replacing the covariance by 2I_2.
3. **Full-rank singleton.** A=diag(1,2) gives G=diag(1,4), LDL pivots (1,4),
   V=diag(1,1/4), gamma=1 and delta=rho=eta2=0. At y=(2,2), score=5.
4. **Off-diagonal interval errors.** M=I_2 and R=[[0,e],[e,0]] give
   G=V=I_2, H=[[e^2,2e],[2e,e^2]], delta=rho=2e+e^2, eta2=2e^2.
   Use both fixed e=1/10^15 and e=1/10. The first passes the usefulness gate;
   the second proves SPD by (5) but fails usefulness with rho=21/100.
   For all four endpoint matrices [[1,s*e],[t*e,1]], s,t in {-1,1}, check
   the exact covariance boxes, Loewner differences by exact PSD elimination,
   inverse bounds, (6), and (9) on z=(0,0),(1,0),(0,1),(1,1),(1,-1).
   The s=t=1 corner attains spectral error 2e+e^2. Omitting off-diagonal H
   would understate it as e^2 and must be rejected by this fixture.
5. **Sufficient-gate failure without singularity.** Diagonal A entries each
   lie in [1/2,3/2], off-diagonal entries are zero. G=I_2, H=(5/4)I_2 and
   rho=5/4. Every compatible A is full rank, but report unresolved by the
   fixed gate. Do not report singularity or switch methods to rescue the run.
6. **Midpoint distinction.** Scalar A in [1,3] gives M=2, G=4, direct Gram
   interval [1,9] with midpoint 5, H=5 and rho=5/4. Computing G=5 is wrong.
7. **Rank ambiguity.** A=[[1,0],[1,h]], h in [-1/100,1/100], has midpoint
   Gram [[1,1],[1,1]]. Compatible h=0/nonzero have ranks one/two, respectively.
   Return unresolved rank, never an exact rank-one covariance claim.
8. **Exact singular support.** Singleton A=[[1,0],[1,0]] has covariance
   W=[[1,1],[1,1]], rank one, W^+=W/4 and support {(u,u)}. Verify all four
   Moore-Penrose identities. Score((2,2))=4; (1,-1) fails support despite
   having pseudoinverse score zero. Include the exact all-zero case separately.
9. **Output-error and law oracles.** Check the separately supplied output-error
   corollary of (8)–(9) with V=I_2, rho=0, y=(1,0) and a proved output-error
   bound (1/10,0): B_score=21/100 and interval [79/100,121/100] contains both
   endpoint quadratics 81/100 and 121/100. This bound is a generic output-error
   fixture, not a coefficient-derived R error when rho=0. Check zero exactly.
   Check the exponential oracle at rho=0 and rho=10^-12 against the exact
   series/remainder construction; reverse either CDF argument as a negative
   control. These are exact enclosure checks, not synthetic coverage runs.

In addition to the targeted wrong answers above, explicitly refuse malformed
dimensions/row order/padding, float/bool/nonfinite endpoints, reversed intervals,
negative radii, an asymmetric G or H, a wrong pivot/reconstruction/inverse,
incorrect delta or gamma, a wrong Moore-Penrose identity or support decision,
rho<0, unauthorized estimated/colored covariance, coefficient/receipt/source
drift, mismatched runtime, missing or incomplete reconstruction, and each
resource limit. Wrong-source/runtime controls must fail before executing that
helper; missing-row controls must fail before Gram work. Exercise intended
failure reasons, not only an unrelated earlier rejection. A changed gate or
silent fallback is itself a failed contract check. All checks survive `-O`.

## 7. Bounded implementation, replay and evidence

After design acceptance, the concrete successor is one new standalone checker
and one combined result, separately reserved and reviewed. It reconstructs
sixteen current certificates once, reconciles them, computes the bounded Gram
and theorem records, and evaluates the ten deterministic probes and the one
CDF comparison. It accepts no observational path, replacement covariance,
row list, precision, sampler seed or threshold. A development `--fixtures`
mode may run only the tiny exact fixtures with explicit mode labeling; such
output cannot be mistaken for admitted-operator integration.

The implementation must preserve every RI-60 engine cap: 256-bit directed
bound arithmetic, fixed power search 2^0 through 2^20, maximum input integer
size 512 bits, intermediate numerator/denominator size 262144 bits, proof
integer size 12288 bits and rounding exponent magnitude 16384. Lengths are
at most 10961 (padded pass 11015), stages at most 17, sections at most 20,
padding at most 27 and state updates at most 440600 per certified adjoint.
This design changes none of those caps or the accepted arithmetic method.

New Gram, LDL, inverse, probe and probability calculations use exact Fraction
arithmetic with a declared maximum of 262144 bits for **each** numerator and
denominator of each intermediate result. Check bounds after every elementary
operation and accumulation, including rejected candidates, not only at output.
This is an exact derived-algebra resource cap, not an increased adjoint
precision. Reject cap overflow; no truncation, underflow or approximate
replacement is allowed. Matrices to factor/invert have dimension at most eight;
identity input covariance is implicit. Never allocate T-by-T covariance or a
full filter matrix. Only tiny fixtures may enumerate their complete bases.

The admitted Gram computation visits 36*T coordinate pairs for each of G,
H, direct K_A, QQ and PP, and 64*T for QP: at most 244*T=2674484 such visits.
Mirror symmetric entries and transpose QP; no additional covariance route
or adaptive tightness search is allowed. The ten probe loops are bounded by
10*8*T. Exact matrix factorization/inverse checks use fixed dimension-eight
loops. Use one worker, 1800 seconds and a sampled 2 GiB resident-memory
watchdog per complete execution. Sampling memory is not a hard allocator cap.
Serialized result size is capped at 64 MiB. Exceeding time, memory, integer
or output limits yields unresolved evidence and a nonzero exit; do not change
the protocol to obtain a pass. The tractability of these fixed limits is not
claimed before the authorized run.

New exact result scalars use the two-element JSON array
`[numerator_hex,denominator_hex]` for the reduced numerator and positive
denominator. Each entry is a lowercase hexadecimal integer string without
`0x` or leading zeros. Nonnegative numerators and positive denominators have
no sign; a negative numerator has exactly one leading `-`. The `+` sign is
forbidden, and zero is exactly `0` (with denominator `1`), never `-0`.
This avoids altering Python's decimal integer-string limit.
Array identities hash canonical JSON with sorted keys,
compact separators, ASCII encoding and no nonfinite values; schema labels,
dimensions, row/domain order and endpoint pairs are included in every identity.
Retain existing RI-60 encodings unchanged for reconciliation. Decimal display
strings may be added with a fixed explicit context but never decide a gate.

Retain one complete result with source/receipt/runtime identities, fixed model
and arithmetic configuration, every fixture/gate/status and failure reason,
all sixteen reconstructed proof/vector identities and eight reconciled summaries,
A/P/Q/M/R identities and dimensions, exact G/H/direct/cross covariance boxes,
delta/gamma/rho/eta2, LDL factors/pivots, inverse and both identity products,
all score/probability endpoints and thresholds. Include exact dimension/count
summaries, no machine input paths or elapsed time in the canonical result.
Full 8T coefficient arrays need not become a second repository artifact:
their identities are reproduced from the pinned source closure on replay.
The report must say that it contains identities, not pretend to store the arrays.

Review source and freeze all dependencies before the first admitted rebuild.
Run isolated copied sources with the qualified Python using `-I -B`, normally
and with `-O`, serially outside the checkout. Root captures stdout; the checker
writes no project files. Require identical canonical result bytes, all source
and interval identities and all gates in both modes. Keep launch mode, timing,
stderr and watchdog metadata in a separate execution receipt. Numerical or
rank failures must retain the complete available deterministic record and all
failed gates with nonzero exit; structural/custody refusal must occur before
dependent work and must not produce an apparent accepted certificate.

An independent reviewer must derive fixture answers before reading the new
source, then replay tiny tests and audit every actual covariance entry and
derived scalar from separately retained reconstructed interval snapshots after
authorization. Such temporary snapshots may stay external. A hashes-only
report audit must explicitly say it did not recompute the coefficient dots.
No full-filter basis or observed-data reprocessing is needed for this audit.
If independent reconstruction or entrywise arithmetic reconciliation is not
completed, do not label the actual covariance calculation independently replayed.

## 8. What passing would establish and what remains missing

A pass would establish reproducible numerical control of the exact unchanged
finite operator's covariance under the explicitly known synthetic unit-white
model, with rank, inverse and conditional score/law bounds. It would not validate
Gaussianity, whiteness or any noise scale for a detector. Finite-context
boundary conventions remain part of this operator; no physical continuation
or full 32-second filtering equivalence is inferred.

Before scoring public observations, separately freeze a conventional estimand,
mean/response, timing, analysis band, conditioning, gaps/flags and selection
history, plus a defensible noise covariance or PSD estimation procedure and
its uncertainty. A longer official off-source product may be needed; it has
not been acquired or qualified here. Known-covariance chi-square laws do not
survive merely substituting an estimated covariance, even from independent
data. Inspected GW150914 windows remain development data, not a blind holdout.

The [RI-40 calibration](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
summaries are pointwise statistical descriptions, not a joint detector/time/
frequency covariance or simultaneous deterministic envelope. Keep their
response-ratio orientation and qualified frequency bounds. Preserve L1's
NO_CW_HW_INJ-clear annotation; this design does not relabel it injection-free.
The [RI-53 scalar reference](../gwosc_nr_comparison_v1/COMPARISON.md) still has
data-informed provenance, printed rather than asserted exact sample times,
limited support and historical illustrative placement. Its source response,
timing/version compatibility and calibration are not supplied by an interior
row selection or a white-noise calculation.

A quantitative native law with source/observer response, identifiable parameters,
selection and competing GR baseline remains necessary for a native discriminator.
This design supplies no calibrated confidence region, detection significance,
physical gravity result or DET-versus-GR proof. RET's implementation pause is
unchanged. Any later sampler, colored/estimated covariance, detector stacking
or observed score requires its own bounded design after this gate is adjudicated.
