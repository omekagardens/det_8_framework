# RI-97 — direct mode-weighted bounds for the same selected-output trace

25 September 2026 UTC. **Source-only proof and prospective design.** This note
does not implement a consumer, run a transform or process actual numerical
operands. No new observation, qualification run, caller or authorization is
created. RI-96 and every predecessor remain unchanged.

RI-96 reduced the four global trace widths by approximately 203–4455 times,
yet the resulting upper/lower trace ratios remain about 156042–601515. Those
are conditional proxy bounds, not detector-noise accuracy measurements. The
next question is precise: **how much of the remaining selected trace width is
due to fixed-band spectral spread, and how much is deterministic enclosure
slack?** Existing certified mode rectangles suffice to pose and compute a
directly weighted scalar bound. No new Fourier or adjoint construction is
needed. Whether the eventual interval is useful remains unknown.

## 1. Exact inherited objects and scientific scope

Keep the RI-92/93/96 objects without selection or retuning: fs=4096, M=16384,
N=2769, L=4096, T=10961, and the eight rows
I=(0,1,27,805,1384,2741,2767,2768). Let A be the same 8-by-T finite difference
between the long and centered short processing operators. S=[I_T,0] crops
the first T coordinates of the same M-vector; B=AS=[A,0]. There is no new
recentring, extra independent short/long input, ignored cross-covariance or
replacement by an infinite-record filter response.

Use U[k,j]=exp(-2*pi*i*k*j/M)/128, with zero-based indices and conjugate
transpose denoted by *. For each of the four separate scenarios, in order
H1:left, H1:right, L1:left, L1:right, the same postulated covariance is

```text
K_s = U* diag(lambda_s) U,
Omega_s = B K_s B^T,
v_k = B U* e_k.
```

Every original one-sided PSD bin p_s[0..8192] remains authenticated as its
original binary64 bytes and interpreted as the exact corresponding dyadic
rational. Keep

```text
lambda_s[0] = fs*p_s[0],       lambda_s[8192] = fs*p_s[8192],
lambda_s[k] = lambda_s[M-k] = fs*p_s[k]/2,  1 <= k < 8192.
```

The pair factor below is separate from this PSD normalization. Real rows give
v_(M-k)=conj(v_k), real Nyquist v_8192, and the accepted constant-annihilation
premise gives v_0=0. Only that true operator action is omitted, not the input
DC value. All 8192 non-DC representatives, including singleton Nyquist, enter
the calculation. There is no removal of low-frequency, zero or unfavorable
bins and no inference about calibrated meaning below 10 Hz.

For a hypothetical M-vector x with finite second moments and covariance K_s,
let d=B x at these eight selected output coordinates. The application quantity
is the **centered** processing-discrepancy energy

```text
t_s = E ||d-E d||^2 = tr(Omega_s).
```

This identity needs neither Gaussianity nor independent row/mode errors. In
contrast, E||d||^2=t_s+||E d||^2; this work supplies no mean-zero premise. The
trace is a sum over eight coordinates, not an average and not a bound on all
2769 outputs. Its nominal units are input strain squared under the inherited
publisher interpretation, without resolving the existing calibration limits.
The four scenarios are not pooled, fitted or interpreted as independent draws.

## 2. Retained enclosures and a direct scalar theorem

The accepted RI-96 result retains each row's coefficient radius sum alpha_i
and the complete Q256 rectangles enclosing the exact midpoint transform. For
one rectangle [a,b]+i[c,d], its integer endpoints represent values divided by
Q=2^256. Define exact rational values, without another rounding step,

```text
X=(a+b)/(2Q),       tauR=(b-a)/(2Q),
Y=(c+d)/(2Q),       tauI=(d-c)/(2Q),
alpha_i=(sum_j r_ij)/128,
eR=tauR+alpha_i,    eI=tauI+alpha_i.
```

These are inherited certified enclosures of the true mode component errors.
They already include midpoint-input conversion, twiddle and butterfly rounding
in tau, and the source coefficient enclosure in alpha. No independence or
cancellation between those errors is assumed. Half-grid centers remain exact
rationals, including the extra denominator bit.

For Nyquist, require the retained imaginary rectangle to contain zero and use
**Y=tauI=eI=0** analytically, including zero imaginary alpha contribution.
Do not project the midpoint DC transform to zero. Its actual real component
and transform-only Parseval check stay part of the inherited RI-96 certificate.
RI-97 does not repeat or alter that check. It verifies the exact identity and
accepted custody of the complete result containing it.

For non-DC representative k set w_k=2 for 1<=k<8192 and w_8192=1. Define

```text
c_k = w_k sum_i (X_ik^2 + Y_ik^2),
h_k = w_k sum_i (2|X_ik| eR_ik + eR_ik^2
                 + 2|Y_ik| eI_ik + eI_ik^2).
```

For a real component z=X+u with |u|<=e,
|z^2-X^2|=|2Xu+u^2|<=2|X|e+e^2. Summing over components and pair multiplicity
therefore gives

```text
| tr(R_k) - c_k | <= h_k,
R_k = w_k (Re(v_k) Re(v_k)^T + Im(v_k) Im(v_k)^T).
```

Every lambda_s[k] is nonnegative. Thus, for each separate scenario,

```text
C_s = sum_(k=1..8192) lambda_s[k] c_k,
E_s = sum_(k=1..8192) lambda_s[k] h_k,
raw_s = [C_s-E_s, C_s+E_s],
t_s in raw_s.                                                   (1)
```

This is an exact finite sum of deterministic enclosures, valid with arbitrarily
correlated coefficient/transform errors. It does not assert their joint
attainability, infer a confidence interval or discard covariance cross-terms:
trace depends only on the diagonal of the same full covariance. It constructs
no covariance inverse or new matrix envelope. In particular, it does not
pretend that the old Gram G identifies spectral response.

## 3. Exact uncertainty and band-width diagnostics

Retain a fixed nonnegative split, not a statistical variance decomposition.
For each active real/imaginary component let

```text
h_tau_component = 2|X| tau + tau^2,
h_alpha_component = 2|X| alpha + 2*tau*alpha + alpha^2.
```

After applying w and summing rows/components, h_k=h_tau,k+h_alpha,k exactly.
At Nyquist the imaginary component contributes zero to both terms. Therefore

```text
E_tau,s   = sum_k lambda_s[k] h_tau,k >= 0,
E_alpha,s = sum_k lambda_s[k] h_alpha,k >= 0,
E_s = E_tau,s+E_alpha,s,
W_direct,s = 2 E_s.
```

The alpha term includes its interaction with transform width. It is not an
independent source of random noise, and the split does not establish that one
term dominates before the actual fixed computation is admitted and completed.

Keep the same fourteen bands B_b={2^b,...,2^(b+1)-1}, b=0,...,12, and
B_13={8192}. From the already accepted RI-96 fields, for each scenario use
its C_minus, C_plus, delta_minus and delta_plus. With D=8,

```text
S_band,s = tr(C_plus-C_minus)
         = sum_b (u_s,b-ell_s,b) sum_(k in B_b) c_k >= 0,
M_band,s = 8*(delta_plus+delta_minus) >= 0,
W_band,s = S_band,s + M_band,s.                                (2)
```

Equation (2) is exactly the width of RI-96's **raw band trace interval**,
before any scalar intersection with global bounds. The first term measures
fixed-band spectral spread using the retained center response. The second is
the old matrix error margin, including row-sum inflation as well as transform
and coefficient uncertainty. It is not simply the direct trace error 2E_s.
Report these terms and 2E_tau,s, 2E_alpha,s together, without calling any of
them PSD-estimation uncertainty or physical covariance error.

There is a useful one-sided consistency theorem. For each k, c_k,h_k>=0 and
lambda_s[k]<=u_s,b. Hence

```text
C_s+E_s <= tr(C_plus)+tr(sum_b u_s,b H_b)
         <= tr(C_plus)+8*delta_plus = band_upper_s.           (3)
```

The second inequality follows because H_b is symmetric entrywise nonnegative
and each diagonal entry is bounded by its row sum. Equation (3) does not
prove direct raw-lower dominance or a whole raw-width improvement. Those
claims are not gates. For example, a broad symmetric square-error enclosure
can have a negative raw lower endpoint despite a valid positive prior bound.

## 4. Scalar intersection, undefined quantities and reporting

Let I96_s=[l96_s,u96_s] be RI-96's already accepted trace scalar intersection,
which retains its global information. Preserve raw_s verbatim and compute

```text
l_s = max(C_s-E_s, l96_s),
u_s = min(C_s+E_s, u96_s),
final_s = [l_s,u_s].                                         (4)
```

Both intervals contain the same t_s under the same premises. Thus their
intersection is valid. Empty intersection is a consistency failure. It must
never trigger rebinning, a PSD floor, clipping, a new precision choice or
weaker acceptance. Keep negative raw lower endpoints even when (4) has a
positive lower endpoint. Nonnegativity of true variance is a separate fact;
this first computation introduces no additional max(0,...) operation.

There is no required improvement factor. The intersection can equal I96_s,
and then the width-reduction factor is exactly one whenever that width is
nonzero. Freeze these scalar diagnostics:

- Raw, RI-96 and final interval widths, and exact flags final==RI96 and
  final==raw.
- RI-96-width/final-width and RI-96-width/raw-width, only when the denominator
  is strictly positive; otherwise null with reason `zero_width_denominator`.
- Upper/lower ratios for raw, RI-96 and final, only when the corresponding
  lower endpoint is strictly positive; otherwise null with reason
  `nonpositive_lower_endpoint`.
- Exact S_band, M_band, W_band, E_tau, E_alpha, 2E and reconstruction of
  the arithmetic identities and consistency inequalities in (1)–(4),
  including direct_upper<=band_upper. Membership of the unknown true t_s is
  supplied by the conditional proof under inherited premises, not a measured
  computational gate or a direct check of physical covariance.

Zero-width [0,0] is valid; its upper/lower and 0/0 width ratios remain undefined.
An exact positive point interval has upper/lower ratio one, but a width ratio
with its zero width in the denominator remains undefined. Never substitute
infinity, zero, one or a decimal epsilon for an undefined ratio. Decimal
summaries are downstream displays of the exact retained rationals.

## 5. Concrete input projection and trust boundary

The sole new actual numerical operand is the complete accepted RI-96 RESULT.
Its needed projection is fixed: exact method/row/scenario/provenance fields;
all eight alpha values; every original 8193 midpoint rectangle per row and
their array identities; each complete original PSD `source_record` in the
four prior/scenario records; and the four old scenario trace endpoints,
scalar-intersection traces, C_minus/C_plus, delta_minus/delta_plus and band
extrema. Keep the entire operand authenticated before projection. Never
substitute an extracted text table, G-only summary or the decimal note.

| Required accepted artifact | Bytes | SHA-256 |
|---|---:|---|
| RI-96 complete RESULT | 41673703 | `5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580` |
| RI-96 independent AUDIT_REPORT | 108637 | `943a9d88eddb66ea6f7cba6070d7b937a182b24491a9877c11a5b5fbdd1702d6` |
| RI-96 root result adjudication | 6551 | `c7842d05fa0d34dddf60d5b3963abb0dbbcae6090ebfcc28af7ca525f61cc836` |
| RI-96 completed audit custody review | 11453 | `21dfdf8472fe8ed9c79ccb600f0608d7183f30cb619b54143fe06850e63bf9be` |
| RI-92 accepted design | 23384 | `1176d5bb3ebab7fd7ba59cc33da494ffeab7a0f0981652734e65714ad873c811` |

The result/audit/source/contract exact copies are under the project directory
`docs/experiments/gwosc_frequency_resolved_proxy_result_v1/`. The original
result is under `det-review-evidence/ri96-execution/application-preparation-wvp1hizx/controls/normal/RESULT.json`,
with an equal optimized result. The original audit is under
`det-review-evidence/ri96-saved-audit-execution/preparation-ex2gupks/controls/normal/REPORT.json`.
The root decision is under
`det-review-evidence/ri96-result-checkpoint-m4z2kzhh/RI96_ROOT_RESULT_ADJUDICATION.json`;
the custody review is under
`det-review-evidence/ri96-independent-completed-audit-review-fo3q2x5f/INDEPENDENT_COMPLETED_AUDIT_REVIEW.json`.
These `det-review-evidence` paths are relative to `/Volumes/AI_DATA/development/`.

Future admission must bind the complete RI-96 actual normal/optimized inputs,
outputs, qualified recursive validation, independent saved audit, genuine
outer completions and root decisions, including their source/runtime closure.
The new caller may inherit those accepted arithmetic premises explicitly; it
must not label hash matching alone a proof of transform validity. Preserve
the existing RI-73 interval/capture and RI-90 PSD/Gram custody dependencies,
all acceptance thresholds, source identities and original historical results.
There is no need to decode the original RI-73 snapshot or rebuild its alpha
in this new scalar step: accepted RI-96 independently bound those values to
that snapshot. Their validity remains a named inherited premise.

No missing prerequisite has been identified at the design stage: RI-96 retains
all needed rectangles, radii summaries, PSDs and prior trace fields. This is
source/schema availability, not a fresh numerical read of those operands. If
any exact artifact or accepted custody chain cannot be reopened later, stop
the dependent computation rather than replace it with a reconstruction.

## 6. Minimal prospective computation and evidence schema

The future actual consumer has one fixed operation. Admit the full source,
runtime and the exact operand bytes; decode the closed RI-96 structure;
verify original array/PSD identities and all declared dimensions/row/order;
derive centers/radii exactly; visit k=1,...,8192 in that order; accumulate
c_k, h_tau,k, h_alpha,k and four sets of exact weighted scalar sums. Derive
(2) from retained fields and independently reconcile its spectral-spread
identity with the same c_k and old extrema. Compute (3), (4) and the frozen
diagnostics. Recheck consumed input/source identities on completion. No FFT,
adjoint, whitening, linear solver or full covariance reconstruction occurs.

Keep the current integer ceiling of 262144 bits, exact reduced hexadecimal
numerator/positive-denominator pairs, fixed Q256 convention and standard
library rational/integer operations. Detect malformed/nonreduced encodings,
nonfinite/negative PSDs, mixed bool/int metadata, unexpected keys, substituted
method/rows/bands or source/phase mismatch. All scientific outputs are exact;
there is no new floating tolerance or fitted floor.

Freeze the next output shape now, with no claim that it exists:

- Top level: `schema`, `phase`, `status`, `method`, `provenance`, `mode_terms`,
  `scenarios`, `checks`, `inherited_premises`, `limitations`.
- `method`: the fixed dimensions, row order, fs, Q256/bit ceiling, unitary
  divisor 128, exact PSD endpoint/interior map, pair weights, true-DC omission,
  analytic Nyquist imaginary rule and equations (1)–(4).
- `provenance`: exact current design/implementation/validator/qualifier pins,
  full RI-96 input and root acceptance, actual runtime and inherited closure
  records. Fabricated qualification has an explicit separate phase and cannot
  claim actual-input custody or accepted real execution.
- `mode_terms`: exactly 8192 records in index order, each with
  `k`, `pair_weight`, `c`, `h_tau`, `h_alpha`. No repeated 8-by-8193 rectangle
  copy is needed; the full original operand and its exact array pins remain
  available. h is exactly the sum of its two retained terms.
- `scenarios`: exactly four records in inherited order. Each binds its full
  source PSD identity, C, E_tau, E_alpha, E, raw interval, RI-96 raw band and
  prior-intersection intervals, final interval, S_band/M_band/W_band,
  exact widths, equality flags, ratio records `{value, undefined_reason}`
  and the upper-bound consistency check. A defined ratio uses a reduced
  rational and null reason; an undefined ratio uses null value and one of
  the two fixed reasons above.
- `checks`: closed prospective inventory, explicit plain-integer counts and
  actual results. An independent saved-result validator must reconstruct
  every mode term and all four scalar records from the admitted operand,
  using separately authored arithmetic; reported booleans are insufficient.
- `inherited_premises` and `limitations`: exact explicit reference to original
  row/transform enclosure validity, accepted upstream custody, the finite
  circulant/noise/calibration distinction, eight-coordinate scope and RET pause.

The 8192 scalar mode records are sufficient for reviewable independent dot
products and for exposing exact accumulation errors, while avoiding another
large copy of all operator coordinates. The independent validator should use
the alternative product form `(|X|+e)^2-X^2` for each diagonal component and
independently derive the transform-only subtraction, not import the producer
or merely compare its output to itself. It need not independently execute a
third Fourier transform; the inherited completed validation must stay explicit.

Resource suitability is an actual later gate, not an assumption from algebra.
Release whole parsed aliases when unnecessary, avoid copies of full predecessor
objects, and accumulate finite scalars with bounded lifetimes. Preserve the
existing envelope: 180 active-child seconds, 524288 KiB sampled sole-child RSS,
0.025-second target polling, 0.1-second maximum/final sample gaps and 0.05-second
ps timeout, with actual raw monitor evidence. A measured failure is preserved
and requires a source-equivalent repair/review or an explicit blocker; it never
authorizes threshold relaxation or dropping bins/evidence. No such execution
is authorized by this note.

## 7. Fixed prospective analytic qualification

These are **unexecuted, fabricated mathematical cases**, not actual-input
admissions or synthetic copies of a successful custody receipt. The tiny
arithmetic kernel may expose dimension only in qualification; the real entry
remains M=16384, eight rows and the same four spectra. No test calls a FFT.
Analytic mode values or valid enclosing rectangles are supplied directly.
The source implementation must freeze exact case encodings and reason codes
before normal/-O qualification, including the complete saved output validator.

For cases Q1–Q5, use M=4, T=3 and rows (1,-1,0), (0,1,-1), padded to M. Their
unitary mode images are v1=((1-i)/2,(1+i)/2), v2=(1,-1), so c1=c2=2,
all tau/alpha are zero and t=2*lambda1+2*lambda2. DC is zero. Keep fs=4096
in the PSD mapping; dimensions alone differ in the labeled tiny fixture.
For Q1–Q7, the M=4 unitary divisor is 2 and alpha is the coefficient-radius
sum divided by 2; the actual M=16384 entry retains divisor 128 throughout.

| ID | Fixed case | Exact expected result |
|---|---|---|
| Q1 | lambda1=2, lambda2=5, lambda0=7 | C=14, E=0, raw=[14,14]; changing only DC to 13 changes nothing |
| Q2 | White eigenvalues lambda1=lambda2=3 | C=12, E=0; endpoint PSD=3/4096, interior PSD=6/4096, not a flat one-sided PSD |
| Q3 | Interior only: lambda1=2, lambda2=0 | Exact trace 4; catches a missing conjugate-pair factor |
| Q4 | Nyquist only: lambda1=0, lambda2=5 | Exact trace 10; catches doubled Nyquist weight |
| Q5 | DC only: lambda0=7, lambda1=lambda2=0 | Exact [0,0], zero widths and undefined ratios; midpoint Parseval is not projected or rerun |
| Q6 | One row (a,-a,0), a in [1,2], M=4; Nyquist lambda2=4, X=3/2, tau=0, alpha=1/2 | c=9/4, h_tau=0, h_alpha=7/4; C=9,E=7, raw=[2,16], enclosing the actual family [4,16] |
| Q7 | Q6 with valid widened real midpoint interval tau=1/4 | h_tau=13/16, h_alpha=2, h=45/16; raw=[-9/4,81/4]. Against legitimate prior [4,16], final=[4,16], width reduction 1, raw upper/lower ratio undefined |
| Q8 | Pure response algebra at M=8: one real row has X2=X3=1, other modes zero, no errors; lambda2=1, lambda3=3 in band {2,3} | c2=c3=2; direct=[8,8], raw band=[4,12], S_band=8, M_band=0; zero-width denominator remains undefined |
| Q9 | M=8, eight response rows with only first two active at k=2: X=1,tauR=1,alpha=0,Y=tauI=0; lambda2=lambda3=1 | C=4,E=12,direct=[-8,16]. Old band H has a 2-by-2 block of 6, delta_minus=delta_plus=12; raw band=[-92,100], S_band=0, M_band=192 |
| Q10 | Full production-shaped zero response: 8-by-8193 zero rectangles, alpha=0, all PSD p=1/4096 | Exact zero outputs with all coordinates/bins visited, including zero-width/undefined ratios; this PSD is not labeled white |
| Q11 | Double all centers, tau and alpha in Q7, with prior interval multiplied by four | C,E,raw,prior,final and widths each multiply by four; defined dimensionless ratios unchanged, undefined statuses unchanged |

Q8/Q9 are pure response-algebra fixtures: impose conjugate symmetry and zero
DC to realize real periodic row responses; they do not claim to be the fixed
finite processing operator or to validate its crop. Q10 is a fabricated zero
operator, not a successful real RI-73 positive-Gram admission. The actual path
must reject attempts to relabel any such fixture as actual saved input.

Freeze additional intended-reason refusal/wrong-formula controls before source
acceptance, rather than invent success records: wrong actual input/source pin;
fabricated-to-actual phase substitution; extra/missing/reordered row or mode;
wrong PSD size/dtype/byte hash; duplicate JSON key/unknown field; noncanonical
or excessive-bit rational; negative/nonfinite PSD; reversed rectangle or
negative alpha; Nyquist imaginary interval excluding zero; wrong endpoint
or pair factor (Q3/Q4); missing lambda error weight (Q6); imaginary alpha
at Nyquist (Q6); alpha incorrectly included in a transform-only term (Q7);
discarded negative raw lower endpoint (Q7); false white-PSD normalization
(Q2); altered band-width identity (Q8/Q9); empty intersection; finite numeric
replacement of a required undefined ratio; and altered mode/scenario scalar
fields caught by the independent validator. Intended reasons and case counts
belong to the future reviewed source contract; none has been executed here.

Qualification must include a full canonical fabricated-result round trip and
intended-reason mutations of the actual closed validators, with identical
normal/-O scientific outputs. No observed operand is decoded during fabricated
qualification. Only after independent complete source/qualification review may
root separately admit the single fixed actual saved-input operation and its
independent saved-result review. This note creates no new general-purpose
verification system, caller or recurring measurement campaign.

## 8. Decision and limits

The direct scalar bound is justified by existing response evidence. Proceed
to independent proof/design review; if accepted, the minimal next implementation
is the exact finite aggregation and validator specified above. No numerical
result, performance success or informative improvement is asserted yet.

Even a narrow eventual interval would concern the stipulated four-second
circulant proxy and its long-lag wraparound. It would not qualify empirical
PSD estimation uncertainty, population covariance, stationarity, detector
independence, mean/template adequacy or public-data calibration. Preserve the
nominal V2/C02 provenance, blank literal Yunits, clear L1 NO_CW_HW_INJ flag,
prior access and already-used 32-second development/calibration status.
Protected held-out validation, physical adequacy and a native DET forward map
remain separate prerequisites. There is no SNR, p-value, physical geometry or
gravity test, native-law result or RET work in this design.
