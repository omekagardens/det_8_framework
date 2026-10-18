# RI-86 — finite colored covariance proxy and exact operator envelopes

25 September 2026 UTC. **Design independently accepted by the coordinator.
No RI-86 implementation, qualification or application run has occurred.**
This note freezes the mathematical model, finite output and prospective gates;
it does not modify a predecessor.

## 1. The bounded result and its premises

Use each of RI-83's four accepted mean PSD arrays to specify a separate finite
circulant covariance **proxy**. Prove and, in the next implementation, evaluate
an exact pair of 8-by-8 covariance bounds for the already fixed context-difference
operator. This connects the conventional public-data spectral description to
the accepted finite operator mathematics without rerunning a filter, accessing
raw strain, estimating a significance, or relabeling estimated noise as known.

Three objects have different status:

1. The retained binary64 Welch mean PSD is an empirical finite statistic of the
   declared public record, window and side. RI-83 independently accepted its
   computation and custody, not its identification with population noise.
2. The mapping below **defines** a real, positive-semidefinite, 16384-coordinate
   circulant matrix. Treating it as the covariance of a noise vector is an
   additional finite model postulate. Its PSD eigenvalues are exact dyadic
   functions of those retained numbers; they are not uncertainty bounds on
   true detector noise.
3. An adequate physical detector covariance, its estimation uncertainty and
   calibration/response/time dependence remain unqualified. No equality of that
   physical covariance with this proxy is asserted.

The useful first output is four reproducible lower/upper matrix envelopes,
with eight marginal-variance intervals and a trace interval for each scenario.
It answers: **under this precisely declared periodic proxy, what variance bounds
follow for the existing finite context-difference operator?** Wide envelopes
are a legitimate outcome. There is no selection of a best side, adaptive band,
floor, ridge, extra detrending or refit after the application is inspected.
The initial packet does not compute the full colored output covariance, its
inverse, an observed residual score, a whitening filter, SNR, p-value or law.

## 2. Fixed inputs, coordinates and units

The four scenarios, in immutable order, are `H1:left`, `H1:right`, `L1:left`,
`L1:right`. Read only their existing `mean_psd` records in the accepted RI-83
scientific result; do not use the separately retained conventional reference
PSDs, ASD squared, segmentwise minima, a pooled mean or a different revision.
Each source record is
`detectors[d].sides[s].mean_psd`, with `d=0,1` for H1,L1 and `s=0,1` for
left,right. It has exactly the keys `dtype`, `shape`, `values_hex`, `sha256`,
with dtype `<f8`, shape `[8193]` and its little-endian binary64 byte identity.
Preserve all 8193 canonical float-hex strings, including endpoint values and
signed-zero byte identity. Arithmetic identifies either signed zero with exact
rational zero; this does not authorize altering the retained bytes.

The inherited statistic is fixed at `fs=4096 Hz`, `M=16384`, `df=fs/M=1/4 Hz`,
periodic Hann, 8192-sample stride, arithmetic segment-mean subtraction before
the window, backward-normalized real FFT, no padding, endpoint weights one
and interior weights two, density denominator `fs*sum(window**2)`, and arithmetic
mean of segment periodograms. Frequencies are exactly `k/4 Hz`, `k=0..8192`.
Left uses seven starts `0,8192,...,49152`; right uses six starts
`69632,77824,...,110592`. The exclusion `[65536,69632)` and unused right tail
`[126976,131072)` remain unchanged. A mean of thirteen periodograms or a merged
H1/L1 spectrum would define a different model and is outside this packet.

The PSD unit is nominal released strain squared per Hz. Multiplying a PSD by
`fs` therefore gives nominal strain squared, as required for a sample-covariance
eigenvalue. The finite filter coefficients and its row matrix are dimensionless;
its output covariance has nominal strain squared units. The literal HDF5
`Yunits` is blank; the nominal V2/C02 interpretation is inherited publisher
context, not a new calibrated uncertainty statement.

The inputs are known public development data with prior display/context access.
The full RI-37 flags remain attached: DQ masks 127, H1 injection masks 31, L1
injection masks 23. **L1 `NO_CW_HW_INJ` is clear for all 32 seconds.** The label
“off-event” specifies the inherited exclusion, not absence of signal or injection.
It establishes neither stationarity nor Gaussianity. No detector cross-spectrum,
independence assumption, joint H1/L1 covariance or stacking is introduced.

### Fixed predecessor identities

Paths below are relative to `docs/experiments/`. These are exact input anchors,
not claims that a hash alone supplies a proof or execution custody. The source
and acceptance chain accompanying them must also be retained in the future
execution freeze.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `gwosc_off_event_spectra_result_v1/RESULT.json` | 38952074 | `e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f` |
| `gwosc_off_event_spectra_result_v1/run_observed.py` | 21098 | `979a27b7af9ad432dd3c9d7abbe87197a8984226b5bc6e016ab93ef92108737b` |
| `gwosc_off_event_spectra_v1/DESIGN.md` | 24390 | `3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce` |
| `gwosc_off_event_spectra_implementation_v1/validate_result.py` | 18529 | `00514faa329cb4bc05d83de74db49d3b603fe8512f9435844f9af48c0c032a63` |
| `gwosc_off_event_spectra_implementation_v1/QUALIFICATION.json` | 63464716 | `f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d` |
| `gwosc_noise_operator_covariance_v1/RESULT.json` | 11180937 | `3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe` |
| `gwosc_noise_operator_covariance_v1/DESIGN.md` | 29545 | `08e6e99d0f884e26b9b4a2422789431d6d6acf077dbb751dd73144b5c6409cd6` |
| `gwosc_noise_operator_covariance_v1/check.py` | 68018 | `574f5f1b8900221a47bc30ea62e6bed378a8fd1c8b4aa904e0549ade8ceb2887` |
| `gwosc_context_operator_v2/operator.py` | 30531 | `ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af` |
| `gwosc_context_operator_v1/oracle.py` | 9484 | `37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651` |
| `gwosc_context_noise_v1/DESIGN.md` | 24027 | `74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921` |

The RI-83 result identity is the root-accepted normal/optimized scientific
byte identity. Its separate saved-evidence audit accepted both modes and all
470 retained array artifacts; this design has not reopened their numerical
values. The repository publication locator may be finalized by the coordinator
without changing any input identity. The admitted RI-73 integration passed all
92 gates and supplied the exact certificate used below; no new reconstruction
is claimed here. Retain RI-73's and RI-80's earlier failures and runtime history.

## 3. One-sided PSD to a finite real circulant covariance

For one scenario let `p[k]` be its finite nonnegative binary64 mean PSD,
interpreted as the **exact dyadic rational represented by that number**.
Do not round through a decimal string or calculate `fs*p` in floating arithmetic.
Define a length-M spectrum by

```text
lambda[0]   = fs*p[0],
lambda[M/2] = fs*p[M/2],
lambda[k] = lambda[M-k] = fs*p[k]/2,     1 <= k < M/2.       (1)
```

Let `F[k,j]=exp(-2*pi*i*k*j/M)/sqrt(M)` be the unitary DFT, and define

```text
K = F* diag(lambda) F,                                      (2)
K[a,b] = df * (p[0] + p[M/2]*(-1)**(a-b)
                  + sum(k=1..M/2-1) p[k]*cos(2*pi*k*(a-b)/M)).
```

Here `F*` is the conjugate transpose. The conjugate-paired interior eigenvalues
make K real symmetric, periodic in the lag modulo M and positive semidefinite:
`v*Kv=sum_k lambda[k]*abs((Fv)[k])**2 >= 0`. Its exact zero-lag value is

```text
q_proxy = K[a,a] = (1/M)*sum(lambda) = df*sum(k=0..M/2) p[k]. (3)
```

This identity checks the units and both endpoint factors. K is a covariance on
a *chosen finite periodic domain*, not an infinite-record covariance recovered
uniquely from Welch averages. The period is four seconds. Its selected
T-coordinate block inherits wraparound correlations for long lags; because
`T=10961>M/2`, those identifications matter. They are explicit model premises,
not an unmentioned Toeplitz approximation or padding prescription.

Equation (3) uses the exact rational sum of retained PSD numbers. RI-83's saved
`q` and Parseval integral are separately rounded binary64 calculations with
its already fixed numerical budget. Do not print an exact equality between
`q_proxy` and that saved `q`. Retain `q` as a hex string and the exact difference
`q_proxy - Fraction.from_float(q)` as descriptive evidence, with no new
acceptance threshold or interpretation as noise-estimation error. Acceptance
of RI-83's numerical consistency remains inherited; it is not tightened here.

For clarity, an optional *mathematical* zero-mean Gaussian construction is

```text
x[j] = sqrt(df*p[0])*Z0 + sqrt(df*p[M/2])*(-1)**j*Znyquist
       + sum(k=1..M/2-1) sqrt(df*p[k]) *
           (Zk_cos*cos(2*pi*k*j/M) + Zk_sin*sin(2*pi*k*j/M)), (4)
```

with independent standard normal coordinates. Direct multiplication gives (2).
A zero coefficient omits its mode. This proves existence, without a sampler,
seed, Gaussianity test or claim about the actual data. A non-Gaussian vector
with the same finite covariance is equally compatible with the matrix bounds.
The real mode count is
`rank(K)=1[p0>0]+1[pNyquist>0]+2*count(positive interior p)`.

The DFT sign, real endpoint and unitary-normalization conventions agree with
the [NumPy 2.1 FFT documentation](https://numpy.org/doc/2.1/reference/routines.fft.html#implementation-details).
Equations (1)–(4) and the envelope proof below are derived here; this initial
consumer needs no FFT, numerical trigonometry or construction of dense K.

## 4. Crop/filter propagation and exact elimination of DC

Keep the RI-71/73 lengths and row order:

```text
N=2769, L=4096, T=N+2L=10961,
I=(0,1,27,805,1384,2741,2767,2768).
```

Let `F_n` denote the held exact rational finite filter of length n, using the
same admitted binary64 SOS coefficients as exact rationals, all 17 ordered
stages, odd extension, constant-prehistory initialization, reversals and
unpadding. This `F_n` is distinct from the Fourier matrix F above. Let E inject
the N-vector into the central T positions, `C=E^T` select those positions, and
J select I. Then the held row matrices are

```text
P = J F_N C,       Q = J C F_T,       A = Q-P.                (5)
```

Select the first T entries of the M-coordinate proxy with `S=[I_T,0]`;
its transpose `S^T` embeds a T-vector into those entries. Thus
`Gamma=S K S^T` and `B=A S=[A,0]`. The modeled output covariance is

```text
Omega_proxy = A Gamma A^T = B K B^T
 = Q Gamma Q^T + P Gamma P^T - Q Gamma P^T - P Gamma Q^T.    (6)
```

The extended coordinate zero corresponds, in the historical context layout,
to raw index 61440; no actual residual or raw vector is read here. A simultaneous
cyclic shift of all selected coordinates leaves this circulant submatrix
unchanged. There is no independent re-centering of the two filter paths.
Both paths act on the **same modeled vector**; omitting either cross term or
using independent short/long noise is a different covariance. Cropping and
finite filtering do not commute. Multiplication of the PSD by an infinite
filter transfer magnitude does not implement (5)–(6), including their endpoint
states. The Hann/detrending operation belongs to the *PSD statistic*: do not
apply another Hann or mean subtraction to Gamma or A.

**Exact DC proof.** For a section with denominator
`1+a1+a2 != 0`, let `g=(b0+b1+b2)/(1+a1+a2)`. Constant prehistory initialized at
the input constant and g times that constant makes every output equal to g
times the input: substitute these values in the exact second-order recurrence.
The admitted oracle's `_pass_fraction` implements that prehistory, and the
RI-60 operator's `_constants`/`_forward_exact_pass` gives the equivalent state
form. Odd extension preserves constants; reversal and unpadding do too.
A two-pass stage therefore multiplies a constant by the square of its product
of section gains. Composing stages gives a length-independent gain h, including
the possibility h=0. Consequently

```text
F_N 1_N = h 1_N,   F_T 1_T = h 1_T,
P 1_T = Q 1_T = h 1_8,   A 1_T=0,   B 1_M=0.             (7)
```

This is a structural property of the exact held filter, not a floating row-sum
threshold. RI-73's interval row sums containing zero are consistent checks,
not a standalone proof of exact equality. Its coefficient midpoint rows need
not sum exactly to zero. Do not project the midpoint matrix, overwrite its
Gram, or silently claim that it inherits (7).

The PSD's DC bin can be nonzero: demeaning before Hann does not force the
windowed transform's DC to vanish. Retain it in K, in q_proxy and in rank(K).
It is absent from the output bounds only because (7) proves that B annihilates
the constant eigenspace. Nyquist and every other bin remain included.

## 5. Exact non-DC envelope theorem

Define the exact extrema over **all** non-DC eigenvalues:

```text
ell = min(lambda[1],...,lambda[M-1]),
u   = max(lambda[1],...,lambda[M-1]).                        (8)
```

Equivalently compare `fs*p[k]/2` for every `1<=k<8192` and `fs*p[8192]`.
This is 8192 distinct one-sided entries representing 16383 real dimensions.
Retain every tied extremizer index, in ascending one-sided order. Excluding DC
is the sole analytic omission; exclude no low-frequency bin, notch, endpoint,
zero, flagged frequency or apparently exceptional peak.

For any real v in R^8, `B^T v` is orthogonal to `1_M` by (7). Applying the
spectral bounds on precisely that subspace proves

```text
ell * A A^T <= Omega_proxy <= u * A A^T.                    (9)
```

RI-73's independently accepted exact certificate has a positive midpoint
Gram G and exact `rho=delta*gamma`, with `0<=rho<=10^-12<1`, and establishes

```text
(1-rho) G <= A A^T <= (1+rho) G.                            (10)
```

Here G is the Gram of the enclosed coefficient midpoint, not the midpoint of
an interval Gram and not a claim that G equals the exact output covariance.
Nonnegativity of ell,u permits composition of (9)–(10):

```text
Lower = ell*(1-rho)*G,
Upper = u*(1+rho)*G,
Lower <= Omega_proxy <= Upper.                             (11)
```

All entries of the two displayed endpoints are exact rational functions of
stored PSD numbers and the held certificate. No new actual coefficient
reconstruction, Fourier enclosure or dense T-by-T matrix is needed. This is
reuse of RI-73's proved *operator* statement, **not** passing an estimated
Sigma to its unit-white checker, changing its model, or claiming a new run of
its 92 gates. The proxy output itself generally has algebraic, non-rational
entries; (11) supplies rational matrix bounds without computing those entries.

Loewner bounds are bounds on every quadratic form, not entrywise covariance
intervals. The eight diagonal intervals `[Lower[i,i],Upper[i,i]]` and trace
interval `[trace(Lower),trace(Upper)]` do follow. Off-diagonal entries of Lower
and Upper must not be labeled lower/upper scalar confidence limits. Keep all
64 entries of both matrices as the matrix certificate; do not discard them
in favor of only marginal displays.

If ell>0, (11) and G positive definite prove rank(Omega_proxy)=8. Algebraically,
with the held `V=G^-1`, inverse order would give
`V/[u*(1+rho)] <= Omega_proxy^-1 <= V/[ell*(1-rho)]`.
The first implementation does not export/use these inverses or a score.
If ell=0, the zero lower matrix gives no positive-definiteness conclusion:
K can be singular while Omega_proxy still has full rank. Retain the bound
`rank(Omega_proxy)<=min(8,r_nonDC)` with
`r_nonDC=1[pNyquist>0]+2*count(positive interior p)`.
If u=0, (7) proves Omega_proxy=0 exactly, rank zero and support `{0}`, even
when p0>0. If u>0 and ell=0, report rank unresolved by this envelope, together
with the rank upper bound; if that upper bound is below eight, singularity is
proved but the exact nonzero rank/support remain unresolved. A ridge, small
positive floor, numerical eigenvalue tolerance or pseudoinverse fallback is
not an authorized resolution.

More generally the exact support is the span of B applied to the positive
real Fourier modes in (4). This is a characterization, not a claim that the
initial application computes those mode images or a support projector.

## 6. Small exact qualification, independent routes and failure gates

The next source packet must implement deterministic rational fixtures first.
The fixture oracle constructs only the tiny M=4 circulant by its explicit
rational cosine table `(1,0,-1,0)` and Nyquist signs, then multiplies dense
rational matrices directly. It must not call the primary extrema-to-envelope
routine to construct its expected values. There is no stochastic coverage or
large-M trigonometric experiment. Keep the following fixed cases and their
actual values in the qualification report.

Use the inherited two-row FIR example

```text
P=[[0,7/4,1/2,0], [0,3/4,3/2,0]],
Q=[[1/2,5/4,1/2,0], [0,1/2,5/4,1/2]],
A=[[1/2,-1/2,0,0], [0,-1/4,-1/4,1/2]],
G=A A^T=[[1/2,1/8],[1/8,3/8]], rho=0.                      (12)
```

1. **White normalization.** At M=4, fs=4 and variance `s=1` then `s=2^-140`,
   set `p=(s/4,s/2,s/4)`. Require all four lambda equal s, K=sI,
   q_proxy=s, Omega=sG and both envelope endpoints equal sG. The tiny scale
   catches an absolute numerical floor; all comparisons are exact. A constant
   one-sided PSD including endpoints is not white under (1).
2. **Genuinely colored case.** Use `p=(7/4,1,3/4)`, hence
   `lambda=(7,2,3,2)` and K with first row `(7/2,1,3/2,1)`.
   Require q_proxy=7/2 and
   `Omega=[[5/4,1/8],[1/8,13/16]]`. The non-DC extrema are ell=2,u=3.
   Require `Omega-2G=(1/16)[[4,-2],[-2,1]]` (PSD rank one) and
   `3G-Omega=(1/16)[[4,4],[4,5]]` (SPD, determinant 1/64).
   Independently evaluate all four shared-noise terms in (6) and require
   equality. In particular `(QKP^T)[0,1]=309/32` while
   `(QKP^T)[1,0]=37/4`; treating this cross covariance as symmetric fails.
3. **DC invariance and cancellation.** In case 2 replace lambda0=7 by 0 and
   by 11, changing p0 accordingly; Omega and (11) remain exactly unchanged,
   although K and q_proxy change. For DC-only `lambda=(d,0,0,0)` with d=4,
   require rank(K)=1, Omega=0 and output rank zero. Also require all-zero PSD
   to give K=Omega=Lower=Upper=0. With identity filtering P=Q, any fixed K
   gives Omega=0 despite nonzero marginal filter covariance.
4. **Nyquist-only and interior-only support.** For `lambda=(0,0,n,0)`, n=4,
   require `Omega=(n/16)[[4,-2],[-2,1]]`, rank one and support span(2,-1).
   For `lambda=(0,m,0,m)`, m=2, require
   `Omega=(m/16)[[4,4],[4,5]]`, rank two despite ell=0.
   This explicitly refutes declaring output singular merely from a zero
   minimum input eigenvalue. No approximate rank threshold is used.
5. **Crop congruence.** For the colored K in case 2 use T'=3,
   `S'=[I_3,0]` and `A'=[1,-1,0]`. Require
   `A'(S'KS'^T)A'^T=[5]` and `[A',0]K[A',0]^T=[5]`, with
   `A'A'^T=[2]` and the exact bounds 4<=5<=6. This separate tiny fixture
   makes the crop/embedding identity observable, not only a dimension check.
6. **Positive nonzero inherited rho.** With case 2's exact A,G and an
   independently supplied *weaker but valid* Gram certificate rho=1/4,
   require Lower=(3/2)G, Upper=(15/4)G and verify the exact Loewner bounds
   by two-by-two principal minors. This qualification-only algebraic fixture
   does not pass the actual RI-73 usefulness gate; explicitly reject it as
   an application certificate. The actual consumer retains rho<=10^-12.
7. **Homogeneity.** Multiply case 2's entire p by exactly 4. Require K,
   q_proxy, ell,u,Omega and both endpoints to scale by 4, all extremizer
   indices/ranks to stay unchanged, and no ratio involving zero to be formed.
   This tests common amplitude-squared scaling, not calibration uncertainty.

Freeze intended-reason refusals in source before qualification: wrong PSD
length/dtype/order/frequency spacing, duplicate JSON/nonfinite or noncanonical
float hex, negative finite PSD, array byte-hash or whole-result mismatch,
changed fixed side/flags/units, use of reference PSD or ASD, missing/duplicate
RI-73 integration gate, failed/incomplete prior result, wrong N/L/T/rows,
asymmetric G/H, negative H, nonpositive exact LDL pivot, incorrect LDL
reconstruction or inverse products, wrong delta/gamma/rho identity, rho<0,
rho>=1, rho>10^-12, altered sources/runtime, and invalid prospective custody.
No negative input is clipped; small positive PSDs remain positive exactly.

Qualification must additionally demonstrate refusal of deliberately wrong
normalization/claim variants: halving either endpoint, failing to halve an
interior bin, using df in place of fs in (1), including DC in the declared
non-DC extrema, dropping Nyquist or another eligible bin, forgetting a tied
extremizer, deleting a cross term, and claiming a nonzero lower bound or exact
rank from the unresolved singular case. These are checks against the fixed
expected fixture values and schema, not runtime method options. A fixture
should fail for its intended mathematical or admission reason, with the
actual exception/check result retained. Explicit checks must work under -O;
Python assertions must not carry acceptance gates.

No new approximate tolerance is needed for (1), (3), (8)–(12), matrix products,
minor signs, rank examples, extrema or output serialization: use exact integers
and Fractions. Keep the RI-73 exact numerator/denominator cap of 262144 bits
for parsed/derived rationals. Overflow/resource exhaustion is an unresolved
attempt, not rounding, clipping or permission to change the method. This cap
is an execution bound, not an error allowance or a calibrated confidence level.

## 7. Complete application output and bounded execution contract

The later source packet defines a closed schema `ri86-colored-proxy-envelope-v1`.
It must retain the following fields; exact key spelling/order and their tests
are frozen with the implementation before either qualification or application.
The schema is small enough to review without another generic framework.

- Header: schema, phase (`fabricated_qualification` or `fixed_saved_application`),
  completed gate inventory/counts/status, fixed scenario/row order, model kind
  `postulated_finite_circulant_from_empirical_psd`, dimensions, exact fs/df,
  source/input/acceptance/runtime pins, and the limitations in sections 1–2.
  A fabricated report cannot be admitted as an actual saved application.
- Predecessor certificate: the exact selected RI-73 G,H,LDL factors/pivots,V,
  delta,gamma,rho, their source gate ID, and the local exact recheck results.
  The selected source path is the unique gate `integration:gram`, under
  `gates[*].detail.certificate`. Require the pinned top-level full-integration
  status, model `known_synthetic_unit_white`, dimensions/row order and all
  92 passed gates. This model label remains unchanged in the inherited record.
  Recheck symmetry, H>=0, positive pivots, LDL reconstruction, GV=VG=I,
  `delta=max row-sum H`, `gamma=max row-sum abs(V)`, and `rho=delta*gamma`.
  It is the accepted prior interval proof that connects G/H with A; these
  local checks do not pretend to reconstruct that connection anew.
- For each of the four scenarios: exact source JSON pointer and complete
  original array record identity/shape/count, saved q hex, exact q_proxy and
  difference to q, endpoint eigenvalues, 8192 exact non-DC one-sided
  eigenvalues in ascending k order (k is implicit from position 1..8192),
  exact ell,u and complete tied index lists, zero/positive interior counts,
  full spectral rank and non-DC rank bound, and retained side/flag/unit context.
  Those eigenvalues are sufficient to reconstruct all 16384 lambda values
  using (1). The original 8193-bin PSD remains in the immutable input result;
  no source values are discarded or replaced by a summary.
- Each scenario also retains both complete 8-by-8 matrices Lower/Upper,
  eight diagonal pairs, a trace pair and rank status: `positive_definite_rank8`
  when ell>0; `zero_rank0` when u=0; otherwise
  `unresolved_by_envelope` with the exact rank upper bound and an explicit
  `singularity_proved` flag when that upper bound is below eight. Do not
  present componentwise off-diagonal intervals, pseudo-confidence or a
  fabricated Omega matrix. The model's support is computed only in the tiny
  qualification fixtures; the actual report says so.

Use RI-73's reduced lowercase hexadecimal numerator/positive-denominator pair
for every exact scalar, with zero `['0','1']`; reject noncanonical or unreduced
input pairs. Scientific JSON is UTF-8/ASCII-compatible, sorted keys, indent two,
finite-only, with exactly one trailing newline and no mode/path/time-specific
content. Execution paths/times and captured failure text belong in separate
custody receipts. A duplicate-sensitive reader validates all nested fields,
shapes, algebraic relationships and claimed statuses. Independently recompute
the four extrema, mappings and matrix scalings from the retained inputs; do
not accept producer booleans as evidence.

Source preparation is followed by independent review and a prospective freeze,
then fabricated normal/-O qualification. Only after its adjudication does a
separate saved-result application read the already accepted RI-83/73 bodies.
Neither stage opens raw HDF5, reconstructs coefficients, reads an observed
context residual, constructs an FFT/window, downloads data or changes the
runtime. No new user permission is needed for authorized continuation through
these review/execution boundaries; the coordinator owns the concrete freeze.

Bind both accepted result bodies before parsing either. Admit exact whole-file
pins and the finalized root acceptance/saved-audit chain, then inspect the
required closed metadata/array/certificate schema and byte identities.
Published gate reports are prior evidence, not newly executed checks. The
accepted whole-byte identities mean this consumer need not rerun RI-83's
full spectral validator or RI-73's coefficient reconstruction. Any changed
input requires refusal rather than substitution. Carry the complete relevant
source/dependency provenance from the accepted predecessor freezes; execute
only newly reviewed retained consumer/oracle/validator/helper bytes. This
keeps scientific dependency evidence distinct from actually imported code.

Use the existing recovered qualified CPython 3.11.6 environment unchanged:
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python`.
Retain its admitted named symlink chain, resolved interpreter bytes and full
runtime inventory/fingerprint, including NumPy 2.1.3, SciPy 1.14.1, h5py 3.12.1,
HDF5 1.12.2 and NumPy build configuration. A runtime metadata admission probe
may use the existing qualified routine; the exact scientific consumer itself
needs only stdlib integer/Fraction/JSON/struct/hash operations. This is not
permission to install packages or substitute a merely version-matched build.

Reuse the reviewed bounded supervisor envelope rather than designing a new
monitor: one worker, serial normal and -O commands with -I -B, wall limit
180 seconds, sampled RSS threshold 524288 KiB, target poll 0.025 seconds,
maximum sample gap 0.1 seconds and ps timeout 0.05 seconds. Retain the explicit
macOS environment binding and a fresh durable TMPDIR, resolved source paths,
exclusive result/stdout/stderr/receipt destinations and complete pre/post
source/input/runtime checks. Sampled RSS is monitoring, not a hard OS memory
cap. Monitor failure, final sampling-gap violation, timeout or resource excess
is a failed retained attempt. No retry or enlarged limit is implicit.

Normal/-O scientific application bytes must agree exactly; receipts do not.
A separate independent saved-evidence review checks exact fixture results,
all four application arrays/envelopes, complete inventories, actual exits,
resources and before/after identities. Existing pipeline controls may be reused
with explicitly reviewed adapter deltas; do not create a new generic harness
or repeat unrelated qualification solely to add gates. The resource cap and
fixed arithmetic domain are prospective here, not a claim of measured success.

## 8. Acceptance and the substantive successor

Design acceptance requires independent agreement on the normalization,
constant-annihilation argument, held-certificate premises, crop/cross-term
identity, non-DC Loewner proof, singular interpretation and exact fixtures.
Implementation acceptance requires those fixtures and intended-reason refusals
in both modes, a checked closed result schema and retained source/runtime
custody. Saved-application acceptance requires the two exact accepted result
identities, all four unmodified scenarios, complete successful output and
independent reconciliation under the frozen limits. None is a statistical
noise-adequacy test. In particular, there is no gate requiring a narrow ell/u
spread or a preferred detector/side outcome.

This advances a concrete conditional colored-noise application using already
qualified public-data products and a substantial exact operator theorem. It
also measures where the coarse spectral envelope loses information. If it is
too broad for a later scientific question, record that limitation. A subsequent
refinement may separately design certified Fourier-mode images of A and sharper
colored output covariance bounds, using RI-73's retained coefficient intervals;
it would need a new reviewed method, not an adaptive change to this packet.

Physical interpretation still needs a justified noise/estimation-uncertainty
model, stationarity and signal/injection treatment, a calibration response law
with its correlations, mean/template and timing/detector response conventions.
RI-40's nearest-time C02 summaries do not close these premises, particularly
below 10 Hz. Even an independent off-source covariance estimate does not make
a substituted quadratic statistic have the held known-covariance chi-square
law. An exact baseline-reproduction claim also needs a matched version,
parameters and named observable; this proxy is not that claim. A DET gravity
comparison additionally needs a native quantitative forward map. Those remain
separate work, and RET remains paused.

No numerical PSD values, eigenvalue extrema or application conclusions were
inspected to choose this design. Only source, design and already stated
acceptance identities were read. The exact small fixtures were derived by
algebra and separately checked by another agent without execution. This
external draft has not run a target, numerical import, synthetic check, raw-data
read or saved-result consumer, and does not create a scientific RESULT.

## Coordinator acceptance and implementation assignment

Root read the complete revised design, independent review and held filter/Gram
source interfaces. The mathematical design is accepted with every stated
model, numerical, custody and physical limitation intact. The reviewed draft
was 31251 bytes, SHA-256
`284a59b0cca963c0e4d1ece56c50c23bec89ee0910f8a45117bf49b4ea3e695c`.
Only this acceptance header and appendix differ from that reviewed draft.

Independent review: /Volumes/AI_DATA/development/det-review-evidence/ri86-independent-design-review-33jm04x3/FINAL_INDEPENDENT_DESIGN_REVIEW.json,
7419 bytes, SHA-256 `f15c35465864a4135228c9957800afb7c3f7998516ad8cf134e00158c99c71b7`.
Root source/proof adjudication and pinned predecessor identities are retained
in /Volumes/AI_DATA/development/det-review-evidence/ri86-design-publication-20260925T0300/ROOT_DESIGN_ADJUDICATION.json.

RI-87 is assigned only the exact consumer, independent tiny fixture oracle,
closed validator and implementation contract. It must prepare source before
fabricated qualification; actual saved-result application remains a separate
admission after qualification acceptance. No PSD values were inspected in
choosing this design. Native RI-85 continues independently and RET remains paused.
