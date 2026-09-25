# RI-92 — certified frequency-resolved bounds for the fixed covariance proxies

25 September 2026 UTC. **Source-only proof and prospective computation design;
not an execution authorization.** No transform, coefficient reconstruction,
colored covariance calculation, qualification or additional data acquisition
has been performed for this note.

[RI-90](../gwosc_colored_covariance_proxy_result_v1/RESULT_REVIEW.md) established
the exact global spectral envelopes for four separately postulated finite
circulant covariances. Their upper/lower scalar factors are approximately
4.223e12, 4.462e12, 2.906e12 and 7.443e12. This motivates retaining the operator's
frequency response instead of assigning every direction the global minimum
and maximum. The following bounds are conditional mathematical results for
those same proxies. Whether their numerical implementation yields useful
improvement remains unknown.

## 1. Unchanged objects and the additional available evidence

Use precisely the four RI-83 mean PSD records, in order H1:left, H1:right,
L1:left, L1:right. Keep all 8193 binary64 values and their exact dyadic
interpretations, fs=4096 Hz, M=16384, df=1/4 Hz, and RI-86's eigenvalues

```text
lambda[0] = fs*p[0],       lambda[M/2] = fs*p[M/2],
lambda[k] = lambda[M-k] = fs*p[k]/2,    1 <= k < M/2.       (1)
```

The inherited filter has N=2769, L=4096, T=10961 and row order
I=(0,1,27,805,1384,2741,2767,2768). With central injection E, C=E^T and row
selection J, its exact rational rows are

```text
P = J F_N C,       Q = J C F_T,       A = Q-P.              (2)
```

F_n includes the same 17 stages, coefficient rationals represented by the
admitted binary64 SOS, odd extensions, initialized passes, reversals and
unpadding. Nothing here substitutes an infinite-record transfer function for
that finite, boundary-dependent operator. The coordinate order is left,
center, right; the historical extended origin is raw index 61440.

RI-73's published result stores summaries and identities, not all row
coefficients. However, its actual accepted execution also retained two equal
complete external snapshots:

```text
/Volumes/AI_DATA/development/det-review-evidence/ri73-execution/
  prep-20260924T213357Z-4493c189/actual-normal/INTERVALS.json
  prep-20260924T213357Z-4493c189/actual-optimized/INTERVALS.json
```

Each is 51,891,508 bytes, SHA-256
`fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba`.
Both still exist and their complete bytes were independently reopened for this
design. The capture schema `ri73-reconstructed-intervals-v1` stores
8*(2769+10961)=109840 short/long coefficient intervals, including every
endpoint as a reduced hexadecimal rational. RI-73's accepted capture binds
these vectors to the scientific reconstruction gate; its independent saved
interval audit binds them to the published Gram/error certificate. The
retained `FINAL_RECONCILIATION.json` is 2098 bytes, SHA-256
`5263ab139542d6591af03300ded7f2d7c9fba5fd3585347b4f7b4bfb7605f232`.

These are usable external operands, not a reason to rerun adjoint construction.
Future admission must reopen the exact snapshot, original capture/caller
receipts, RI-73 audit input freeze, successful audit receipts and root decision;
bind the full accepted source/runtime chain; check the complete schema, row
order and dimensions; and reconcile the retained vector identities. A hash
alone is not proof of enclosure. If this actual snapshot or its custody chain
is unavailable, stop this computation: G, H, maximum radii and row hashes
cannot replace the missing row intervals. Reconstruction would be a separately
reviewed task, not a silent fallback.

From short intervals [s-,s+] and long intervals [q-,q+], form each A interval
as [q-,q+] outside the center and [q--s+,q+-s-] inside it. In particular use
`long[:L] + (long[L:L+N]-short) + long[L+N:]`, with interval subtraction;
never concatenate the two external pieces before the central piece. Let

```text
m_ij = (a-_ij+a+_ij)/2,      r_ij = (a+_ij-a-_ij)/2 >= 0,
A = m+D,                    |D_ij| <= r_ij.               (3)
```

The coefficients and their enclosure proofs are inherited premises. This note
inspects their source/schema and actual file identities; it does not decode
the snapshot to compute new coefficient or spectral quantities. All original
RI-60/73 precision, width, rho and acceptance gates remain unchanged.

| Fixed scientific input | Bytes | SHA-256 |
|---|---:|---|
| [RI-83 spectra](../gwosc_off_event_spectra_result_v1/RESULT.json) | 38952074 | `e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f` |
| [RI-73 certificate](../gwosc_noise_operator_covariance_v1/RESULT.json) | 11180937 | `3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe` |
| [RI-90 result](../gwosc_colored_covariance_proxy_result_v1/RESULT.json) | 6994965 | `c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf` |
| [RI-86 design](../gwosc_colored_covariance_proxy_v1/DESIGN.md) | 32470 | `2a00cac0017f0b749ed958efef4d623143c97e33ba36c60454a65ef9069dc04e` |

## 2. Exact mode images, crop and endpoint factors

Let S=[I_T,0] select the first T coordinates of the M-vector. Define the
unitary Fourier matrix U by U[k,j]=exp(-2*pi*i*k*j/M)/sqrt(M), with zero-based
indices. Here sqrt(M)=128 exactly. The unchanged proxy and mode images are

```text
K = U* diag(lambda) U,       Gamma = S K S^T,
B = A S = [A,0],            v_k = B U* e_k,
(v_k)_i = (1/128) sum(j=0..T-1) A_ij exp(+2*pi*i*k*j/M),
Omega_proxy = B K B^T = sum(k=0..M-1) lambda[k] v_k v_k*.   (4)
```

Star denotes conjugate transpose. The final covariance is real symmetric.
This placement retains the original crop and long-lag circular wraparound;
there is no recentering, extra padding model, independent short/long input or
missing P/Q cross covariance.

The accepted theorem A*1_T=0 gives v_0=0 exactly. Real rows imply
v_(M-k)=conj(v_k); v_(M/2) is real. Writing v_k=x_k+i*y_k, define real PSD
response matrices

```text
R_k = 2*(x_k x_k^T + y_k y_k^T),    1 <= k < M/2,
R_(M/2) = x_(M/2) x_(M/2)^T.
Omega_proxy = sum(k=1..M/2) lambda[k] R_k,
sum(k=1..M/2) R_k = A A^T.                                (5)
```

Indeed the imaginary skew parts of v_k v_k* cancel between conjugate modes;
the pair has equal eigenvalues. The factor two is the pair multiplicity, not
another one-sided PSD normalization. Nyquist has multiplicity one. DC is the
only omitted action, proved zero analytically; its input value remains stored.
There are 8192 non-DC representatives and 16383 non-DC Fourier modes. No
low-frequency bin, notch, zero or endpoint is removed.

## 3. What the Gram certificate does and does not identify

RI-73 certifies G=m m^T and (1-rho)G <= A A^T <= (1+rho)G, with the fixed
rho<=10^-12 gate. It does not identify R_k or bandwise allocations of A A^T.
Even exact knowledge of A A^T generally cannot do so.

For the precise non-identifiability premise, put
Pi=I_T-1_T*1_T^T/T and Gamma_0=Pi*Gamma*Pi. Suppose Gamma_0 restricted to
the zero-sum subspace is not a scalar multiple of its identity. Then there
are real unit vectors u,w perpendicular to 1_T with
u^T*Gamma*u != w^T*Gamma*w. The one-row operators u^T and w^T both annihilate
constants and both have Gram [1], but their colored variances differ. An
orthogonal transformation fixing 1_T maps these vectors to one another.
More generally right multiplication of a row matrix by such a transformation
preserves its Gram and constant annihilation while changing its spectral
orientation. Complete orthonormal row frames give the same obstruction for
eight-row operators in this domain.

This is an information counterexample, not a proposal to replace the known
fixed A. The extra premise concerns the *compressed zero-sum covariance*;
unequal eigenvalues of the full K alone need not prove that premise for an
arbitrary crop. If Gamma_0=c*Pi, the obstruction disappears and
A*Gamma*A^T=c*A*A^T. No such isotropy is assumed here. The actual row
intervals, rather than G alone, supply the response information needed in (4).

## 4. Fixed bands and exact band-envelope theorem

Fix the partition now, before any new response evaluation:

```text
B_j = {2^j,...,2^(j+1)-1},  j=0,...,12;
B_13 = {8192}.                                             (6)
```

These fourteen bands cover every non-DC representative once. They depend only
on M, not on peak locations or favorable numerical outcomes. For each band
and each of the four spectra separately, define

```text
W_b = sum(k in B_b) R_k >= 0,
ell_b = min(k in B_b) lambda[k],   u_b = max(k in B_b) lambda[k].
L_exact = sum_b ell_b W_b,         U_exact = sum_b u_b W_b.   (7)
```

For any real output vector t,
t^T*(Omega_proxy-L_exact)*t=sum_b sum(k in B_b)
(lambda[k]-ell_b)*t^T*R_k*t >= 0. Applying the same argument to
u_b-lambda[k] proves

```text
L_exact <= Omega_proxy <= U_exact.                         (8)
```

With global extrema ell,u, the ideal band endpoints also obey
ell*A*A^T <= L_exact and U_exact <= u*A*A^T. This follows from
ell_b>=ell, u_b<=u and W_b>=0. It is a theorem about exact responses;
finite enclosure errors can conceal the numerical improvement. No guaranteed
improvement factor is asserted for the still-uncomputed certified endpoints.

## 5. Carrying row and transform uncertainty into matrix bounds

The first implementation will transform the midpoint rows m, zero-padded to M,
using a proved interval transform. Suppose its returned rectangles enclose
the exact midpoint image z_k=[m,0]*U*e_k. Let their exact rational centers
be X_ik,Y_ik and half-widths tauR_ik,tauI_ik. These widths must include input
conversion, all twiddle uncertainty and every arithmetic rounding operation.
Centers and half-widths remain exact even if halving a grid interval gives an
extra denominator bit; do not round them again without accounting for it.
Define from the actual retained coordinate radii

```text
alpha_i = (1/128) sum(j=0..T-1) r_ij,
eR_ik = tauR_ik + alpha_i,      eI_ik = tauI_ik + alpha_i.  (9)
```

Since |cos|,|sin|<=1, the real and imaginary parts of
[D,0]*U*e_k each have absolute value at most alpha_i. Thus
|(x_k)_i-X_ik|<=eR_ik and |(y_k)_i-Y_ik|<=eI_ik. This bound uses the
sum of retained radii, not a substituted maximum or an independence model.
It remains valid when coefficient errors are correlated across modes/rows.

For Nyquist, reality proves y=0: require the transform's midpoint imaginary
interval to contain zero and use Y=eI=0 for that endpoint. Do not set the
midpoint's DC transform to zero: interval midpoints need not annihilate
constants. Retain its actual enclosure, require compatibility with the exact
A DC identity through (9), and use true A's v_0=0 only in (5) and the bounds.

For w_k=2 in the interior and w_(M/2)=1, form exact rational matrices

```text
C_k = w_k*(X_k X_k^T + Y_k Y_k^T),
H_k,ij = w_k*( |X_ik|*eR_jk + eR_ik*|X_jk| + eR_ik*eR_jk
             + |Y_ik|*eI_jk + eI_ik*|Y_jk| + eI_ik*eI_jk ). (10)
```

Expansion of each scalar product proves |R_k,ij-C_k,ij|<=H_k,ij.
H_k is symmetric and entrywise nonnegative. Exact Nyquist imaginary zeros
make the second line vanish there. Let C_b=sum(k in B_b) C_k and
H_b=sum(k in B_b) H_k. Then |W_b-C_b|<=H_b entrywise. For each spectrum set

```text
C_minus = sum_b ell_b C_b,    H_minus = sum_b ell_b H_b,
C_plus  = sum_b u_b C_b,      H_plus  = sum_b u_b H_b,
delta_minus = max_i sum_j H_minus,ij,
delta_plus  = max_i sum_j H_plus,ij,
L_cert = C_minus - delta_minus*I_8,
U_cert = C_plus  + delta_plus*I_8.                          (11)
```

All eigenvalues and their extrema are nonnegative, so these weighted error
matrices bound the corresponding endpoint errors entrywise. For a real
symmetric error E with |E|<=H, ||E||_2<=||E||_infinity<=max row sum(H).
Consequently L_cert<=L_exact and U_exact<=U_cert, and (8) yields

```text
L_cert <= Omega_proxy <= U_cert.                           (12)
```

The weights must also multiply H; an unweighted common error margin is not
valid. No statistical independence of rounding errors or Fourier modes is
used. C_b is PSD, but L_cert may be indefinite; do not clip its eigenvalues,
add a ridge or infer that the actual proxy lost the rank eight already proved
by RI-90. Loewner bounds concern quadratic forms, not componentwise intervals
on off-diagonal entries. Diagonal and trace endpoint pairs are scalar bounds.

Keep RI-90's global endpoints alongside (12). If useful, certify matrix
dominance by an exact PSD test of L_cert-L_global and U_global-U_cert; absence
of that certificate is not a disproof of (12). Entrywise maxima/minima of
matrix endpoints are not a legitimate Loewner intersection. Intersecting the
two scalar diagonal or trace intervals *is* valid. Report a ratio only when
its certified scalar lower endpoint is strictly positive; no floor is fitted.

Mode responses, C_b and H_b are dimensionless. Lambda and the final endpoints
have nominal released strain-squared units. That unit bookkeeping does not
establish a calibration uncertainty model.

## 6. Frozen minimal next computation and exact transform contract

The next implementation is a saved-interval consumer, not another adjoint
reconstruction. It computes eight certified M-point midpoint transforms once,
the fourteen pairs (C_b,H_b), and the four distinct band-extrema consumers
in (11). It does not construct dense M-by-M K, calculate residuals, whiten
data, fit spectra or evaluate a detector statistic. It retains mode enclosures
and errors as external artifacts so band sums can be independently reproduced.

Fix this first transform method rather than treating an ordinary FFT as a
certificate:

1. Use integers/rationals with outward dyadic endpoints on the fixed grid
   2^-256 for **new transform arithmetic**. Every conversion and primitive
   operation rounds its lower endpoint down and upper endpoint up. Preserve
   the original row intervals exactly before this conversion; the grid does
   not redefine the admitted operator or its existing significant-bit rules.
   It is dimensionless arithmetic, not an absolute strain acceptance floor.
2. Use a positive-sign, radix-two iterative decimation-in-time transform,
   explicit bit-reversal and stages n=2,4,...,16384. For final normalization,
   divide each interval endpoint exactly by 128, then round outward to the
   same Q256 grid; include that rounding in tau. Within each length-n block
   and j=0,...,n/2-1, set
   t=omega_n^j*z[block+j+n/2], u=z[block+j], then replace that pair by
   u+t,u-t. Each stage's powers are j=0,...,n/2-1. The exact direct sums obey
   D_n(k)=D_even(k mod n/2)+omega_n^k*D_odd(k mod n/2);
   at k+n/2 the second term changes sign. Induction from length one, with
   bit-reversal supplying the even/odd order, proves these butterflies equal
   the unnormalized direct sum. Inclusion-preserving interval primitives
   enclose the same invariant at every stage. The source must implement that
   invariant, with no permutation or sign left implicit.
   No ambient NumPy/SciPy FFT, unproved libm trigonometry or binary64 twiddle
   rounding supplies the enclosure.
3. Certify stage roots from exact c_2=0, s_2=1 for angle 2*pi/4 and
   c_r=sqrt((1+c_(r-1))/2), s_r=sqrt((1-c_(r-1))/2), r=3,...,14.
   The n=2 root is exactly -1. Positive-quadrant signs and the half-angle
   identities select the intended roots. Generate each stage's powers in
   fixed increasing order by outward complex multiplication; reset from 1
   at each stage. Range intersections may use only proved [0,1] bounds for
   these first-quadrant base sines/cosines, never data-dependent clipping.
4. Enclose sqrt(q), q>=0, by exact integer square-root isolation: for
   q=n/d, take a=isqrt(floor(n*2^512/d)); the lower endpoint is a/2^256,
   and the upper is the same if its square equals q, otherwise (a+1)/2^256.
   For an input interval use the lower and upper argument endpoints with
   directed isolation. Check the squared inequalities exactly. No precision
   search or unreported higher-precision retry is permitted.
5. Carry real/imaginary interval multiplication by its exact four-product
   extrema and directed rounding. Zero padding, normalization, pair weights,
   alpha, matrices and aggregate margins use the fixed definitions above.
   Retain the inherited 262144-bit exact intermediate ceiling; exceedance,
   reversed/invalid intervals or unavailable evidence is a refusal, not a
   reason to enlarge the domain.

This freezes a mathematically sufficient scheme, not a claim of acceptable
speed or achieved precision. Exact scalar/matrix accumulation must also be
resource bounded and source reviewed. The initial execution envelope remains
180 seconds and 524288 KiB sampled child RSS, 0.025-second target polling,
0.1-second maximum/final sample gaps and 0.05-second monitor timeout. Existing
RI-73 reconstruction limits are not permission to raise this new bound. Its
old saved-interval audit used 694400 KiB (about 678.1 MiB), so reusing that whole-object
allocation strategy would be unjustified here: admit/hash the 51.9 MB body,
parse/release rows with bounded lifetimes, and retain exact row/mode evidence
without keeping redundant decoded snapshots. Resource failure is retained;
there is no automatic relaxed-limit attempt.

The exact schema/implementation, outward primitives and transform are the
currently **unqualified prerequisites**. No certified response array or band
Gram has yet been produced. Source review, a prospective source/runtime/input
freeze, fabricated qualification and its independent review must precede one
separately authorized real saved-interval attempt. Bind the complete source
closure and same admitted recovered runtime, not just version labels. The
coefficient snapshot's accepted provenance remains distinct from proving the
new transform and its accumulated error bounds.

## 7. Qualification obligations and useful output

Keep the fabricated transform sizes to 4,16 and the fixed production 16384;
their unitary divisors 2,4,128 are exact. The implementation must pin its full
case inventory before a run. At minimum it must establish these substantive
families, with intended-reason refusals at the actual guards:

- Independently derive a direct scalar transform at sizes 4 and 16, including
  complex sign, bit-reversal and normalization checks, against the interval
  butterflies. The oracle must not call the butterfly implementation. Exact
  endpoint roots and independently isolated radical values at size 16 prevent
  a shared floating FFT from becoming the only oracle.
- At M=16384 use fixed zero, constant, alternating-sign, quarter-rate cosine,
  quarter-rate sine and coordinate-zero impulse vectors. Their exact DC,
  Nyquist, conjugate pair and flat impulse images check the production indexing
  and factors. Scaling a fixture by two must scale its response matrices by
  four, with enclosure containment rather than a false bitwise scaling rule
  for rounded interval widths.
- Use size 4, T=3 and rows (1,-1,0), (0,1,-1), padded by one zero. Direct
  algebra gives R_1=I_2, R_2=[[1,-1],[-1,1]] and Gram
  [[2,-1],[-1,2]]. Lambda_1=2, lambda_2=5 gives
  Omega=[[7,-5],[-5,7]]. This checks crop, common-input cross terms, real
  conjugate pairing and Nyquist multiplicity without an FFT oracle.
- For the preceding 2-by-3 midpoint rows with radius 1/16 in each of the six
  coordinates, enumerate all 64 corners by direct rational Fourier algebra.
  Set lambda_0=0, lambda_1=lambda_3=2, lambda_2=5: arbitrary corners need not
  annihilate constants, so this fixture does not assume that theorem for them.
  Check every
  entrywise error enclosure and both final Loewner margins; combine this with
  rectangles widened by exactly 1/256 on each real/imaginary side. Separately
  take the size-4 row (a,-a,0,0), a in [1,2], and Nyquist-only lambda_2=4.
  At a=2 the true scalar covariance is 16. The midpoint response is 3/2,
  its radius is 1/2, C=9/4 and H=7/4. The correct upper endpoint is 16;
  failing to multiply H by lambda gives 43/4 and must be rejected. This is
  a correlated coefficient-error case with an explicit intended inequality
  failure. These fixtures test sufficient enclosures, not actual
  coefficient-error independence or an empirical coverage probability.
- Reconcile midpoint Parseval: the full midpoint transform, **including its
  generally nonzero DC mode**, must enclose the exact retained G=m*m^T using
  transform-only errors. The A-response band sum instead encloses A*A^T and
  need not equal G. Reject conflating these two identities.
- Use white spectra with lambda_k=sigma^2 for all k, for sigma^2=1 and 4:
  their one-sided PSDs are p_0=p_Nyquist=sigma^2/fs and
  p_interior=2*sigma^2/fs. A flat one-sided PSD including its endpoints is
  not this white spectrum. Also use all-zero, DC-only, interior-only and
  Nyquist-only spectra. Verify white-mode reduction, exact A DC removal,
  factors/rank limitations and band partition coverage; retain all source
  bins. Zero lower bands or a negative certified lower endpoint must remain
  unresolved, never be repaired by flooring, discarding modes or clipping.
- Reject wrong snapshot/status/source/runtime/row identities, reversed
  endpoints, malformed rationals, changed crop or normalization, missing or
  repeated band indices, altered PSD mapping, underestimated transform/error
  rectangles and resource/domain changes. Refusals must occur before the
  affected scientific claim, with no successful observed qualification label.

For the actual saved operands, retain all input/source/custody identities;
the eight alpha values and midpoint transform enclosures; proved twiddle and
arithmetic error evidence; every band's index set, C_b,H_b; every scenario's
min/max values with all ties; delta_minus/plus and full L_cert,U_cert;
diagonal/trace pairs and their valid intersections with RI-90. Publish exact
values and round display values only afterward. Report whether the new bounds
are tighter, too broad or fail a fixed resource/qualification gate. Do not
select bands or transform precision again after viewing their performance.

## 8. Measurement interpretation remains a separate question

This step asks how much information is lost by RI-90's global spectral
extrema. It does not remove the four-second periodic covariance, crop-induced
wraparound, empirical PSD estimation or calibration premises. The bins at
6.25/6.5 Hz remain included even though inherited calibration evidence does
not justify a calibrated physical interpretation there. Nominal V2/C02,
blank literal Yunits, and L1's clear NO_CW_HW_INJ flag remain attached.

If the certified envelopes become informative, a subsequent conventional
public-data question is whether the same operator's observed variances and
correlations on independently selected off-event stretches agree with the
frozen proxy predictions, with a separately designed estimation-uncertainty
and calibration treatment. The already used 32-second inputs and their
left/right spectra are calibration/development evidence, not newly independent
held-out samples. Even agreement would not by itself establish Gaussianity,
detector independence, an exact chi-square law or a native gravity prediction.
No covariance inverse, score, SNR, p-value or physical adequacy claim is added.
The native forward-map obligation remains separate, and RET remains paused.
