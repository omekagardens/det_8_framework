# RI125 fixed fabricated cases — revision 1, unexecuted

All numbers below are exact rationals; an integer denotes that integer over one.
These are complete mathematical operand recipes, not saved actual results. The
future qualifier constructs canonical fixtures from these recipes and retains
them. It must not read actual capture, PSD, strain or historical scientific bodies.
No case has been run. A complete independent result reconstruction is mandatory
for every field; the explicitly stated invariant checks below supplement it.

For exact white rows A, take singleton coefficient intervals, G=A A^T,H=0,
delta=rho=0,inverse=G^-1 and gamma=max row sum abs(inverse). These formulas
define fixture construction only and are independently checked. No inversion
of an actual operator occurs. All-zero A uses only the shift primitive.

The literal case order is the W01–W10, P01–P09, N01–N05, J01–J02 order below.

## White cases

- **W01_single_white_two**: r=1,T=3,d=2,A=[1,0,-1],n=2.
  K=[[-1]],E=0,G=[[2]],inverse=[[1/2]],gamma=1/2;
  response center=trace=3/2, error=eps=0.
- **W02_single_white_three**: same A,n=3. Exact response=16/9.
- **W03_oriented_two**: r=2,T=3,d=2,A=[[1,0,-1],[0,1,-1]],n=2.
  G=[[2,1],[1,2]],inverse=[[2/3,-1/3],[-1/3,2/3]],gamma=1.
  K=[[-1,0],[-1,0]],E=0,response=[[3/2,3/4],[3/4,1]],trace=5/2.
  Its transpose as a replacement for K fails complete directed-field equality.
- **W04_negative_scale**: W03 with every A entry multiplied by -1.
  Complete G/K/response outputs equal W03, including off-diagonal orientation.
- **W05_double_scale**: W03 with every A entry multiplied by 2.
  G/K/response are four times W03, inverse/gamma one quarter; eps remains zero.
- **W06_interval_mixed**: shift only, r=1,T=3,d=2,head=[[1,2]],
  tail=[[-2,-1]]. K=-9/4,E=7/4,primary=[-4,-1/2],direct=[-4,-1].
  The unchanged primary is wider than the direct box; do not replace it.
- **W07_interval_crosses_zero**: shift only, head=[[-1,1]],tail=[[-2,2]].
  K=0,E=2,primary=direct=[-2,2]. Enumerate all four endpoint products.
- **W08_zero_shift**: shift only, r=1,T=3,d=2,head=tail=[[0,0]].
  All six numeric Shift fields are exactly zero. No fictitious inverse is used.
- **W09_production_boundary_sparse**: actual r/T/d and eight row labels,
  a complete fabricated capture with every short coefficient zero. Long rows
  are zero except row 0 positions 0=1,8192=2,3000=-3; row 1 positions
  2768=3,10960=-1,3001=-2; for ordinal i=2,...,7, positions 3000+2i=1 and
  3001+2i=-1. All intervals singleton. Every row sum is zero. No endpoint or
  offset is omitted. G=diag(14,14,2,2,2,2,2,2), inverse reciprocal diagonal,
  gamma=1/2,K=diag(2,-3,0,0,0,0,0,0),E=0. For n=7 then n=6,
  kappa=40*(n-1)/n+2*(n-1)/n^2, eps=0. This is not the RI73 capture.
- **W10_usefulness_boundaries**: standalone sufficient-bound decision primitive
  with (delta,ell)=(1/10^12-1/10^24,1),(1/10^12,1),
  (1/10^12+1/10^24,1), and (1,1). States pass,pass,accuracy_failed,
  accuracy_failed. These explicitly fabricated bound pairs exercise the
  inclusive sufficient gate; they are not claimed derived actual Gram data.

## Periodic cases

All tiny periodic cases have M=4,d=2,one output and exact orthonormal DFT
convention. A latent vector has independent equiprobable signs unless a stated
factor multiplies it. Enumeration is limited to its sixteen sign vectors.
Default B=(1,0,-1,0), constant mean zero, K=I4, nonzero saved-mode centers
(c1,c2)=(2,0) with pair weights (2,1), all errors zero. The same FS=4096
PSD encoding uses (1/4096,1/2048,1/4096), giving every eigenvalue one.
Source Q256 rectangles follow the exact DFT entries; no FFT is called.

- **P01_periodic_two**: default, n=2,p=q=1. t=2,h=-2,E[V]=2;
  this differs from W01's shared-white 3/2 despite identical marginal t.
- **P02_periodic_three**: default, n=3,p=2,q=1. E[V]=16/9.
- **P03_seven_multiplicity**: default, n=7,p=4,q=3. factor=48/49,
  E[V]=96/49. Enumeration is still sixteen latent sign vectors, not 2^28.
- **P04_six_multiplicity**: default, n=6,p=q=3. factor=1,E[V]=2.
- **P05_even_nyquist_only**: B=(1,-1,1,-1),M=4 full-M toy, all eigenvalues one.
  c1=0,c2=4,t=h=4. For n=2 E[V]=0. This B is not a production first-T row.
- **P06_mixed_parity**: B=(1,0,0,-1),full-M toy,all eigenvalues one,n=2.
  k1 rectangle is exact real=1/2,imaginary=1/2; k2 exact real=1.
  c1=c2=1,t=2,h=0,E[V]=1. Both signs of the cross formula are exercised.
- **P07_dc_only_psd**: default B with PSD=(1/4096,0,0),n=2.
  All nonzero contributions and E[V] are zero. Retain the declared DC input;
  neither fabricate its omission nor drop it from the raw-array identity.
- **P08_nonzero_interval_errors**: mode-aggregation primitive, M=4,n=2,
  lambda1=lambda2=1,terms c=(2,3),h_tau=(1/8,1/4),h_alpha=(1/16,1/8).
  Exact odd error=3/16,even error=3/8,total center=5,error=9/16;
  h center=1,periodic interval=[29/16,35/16],naive=[23/16,41/16].
  This deliberately declared mode-term fixture is not presented as a Q256
  transformation; the Q256 reconstruction path is covered by P01–P07/P09.
- **P09_production_zero_spectra**: actual eight row labels, M=16384 and four
  scenario ids. Every row Q256 rectangle and alpha is zero; every original
  PSD bin is binary64 +0.0. Generate all 65544 rectangles, 8192 mode records,
  32772 PSD bins and exact original array identities; all contributions zero.
  Preserve all rows/bins/phase labels; fabricate no RI96/RI100 acceptance pin.

## Mean and calibration boundary cases

- **N01_constant_mean**: default white W01 with deterministic raw mean 3 at
  every shared coordinate. True A annihilates it; b_mu=0. No midpoint-row
  projection is allowed. Compare each sign's output with the centered version.
- **N02_quadratic_mean**: W02 with common raw mu_j=j^2 at starts (0,2,4).
  Deterministic output means are (-4,-12,-20), mean -12 and b_mu=128/3.
  White covariance contribution remains 16/9; total expectation=400/9.
  Finite sample centering must not change the population-mean premise to zero.
- **N03_calibrated_constant**: standalone RI119 Q12 identity,
  A=(1,0,-1),C=diag(1,1,2),input=(1,1,1). Output=-1, so a general calibrated
  nominal constant is not annihilated by the uncalibrated A premise.
- **N04_covariance_error**: D=(1,-1)^T,n=2,Pi=H2,Sigma_model=[1],
  Sigma_true=[2],eta=1. Model=1,true=2,absolute difference=bound=1.
- **N05_calibration_error**: same D/Pi/n,C0=1,DeltaC=1,F=1.
  Model=1,true=4,absolute difference=bound=3. No independent-noise premise added.

## Join cases

- **J01_four_rows_exact**: use W09's exact complete white responses and P09's
  zero periodic records under conspicuously fabricated phase tags. Historical
  comparison fixture has all four fixed ids/starts/rows; U=M=V=[0,0], trace
  interval=[0,0], all source identities are pins of explicit fixture bodies.
  Copy every field and preserve unresolved nuisance fields. This exercises the
  join kernel only, never the actual fixed-result entry function.
- **J02_precision_inconclusive**: same zero comparison/periodic fixture, but
  declare eight fabricated full rows with A[i,3000+2i]=1 and
  A[i,3001+2i]=-1 for i=0,...,7, all other coefficients zero. G=2I8, inverse=I8/2,
  gamma=1/2, head/tail zero, K=E=0. Declare the valid deliberately loose
  artificial bound H=(2/10^12)I8, delta=2/10^12, rho=1/10^12. It encloses the
  exact Omega=G; it is not claimed to be RI73's radius-derived certificate.
  For each n, eps=n/((n-1)*(1-1/10^12))*1/10^12 is strictly above the new
  threshold, while the inherited sufficient bound passes at equality.
  Rebuild both full white responses from this explicit artificial operand.
  Only conditional_comparison_precision_inconclusive is valid; no missing
  dependency or inconsistent edited output is accepted.

The implementation must retain all 26 case operands and outputs, with complete
typed primary/independent equality. Tiny enumerations and endpoint products are
future qualifier code, not actions performed to write this file. The production
sized recipes test framing/exhaustion with fabricated entries only. No case
value is a measurement, actual operator contraction or qualified result.
