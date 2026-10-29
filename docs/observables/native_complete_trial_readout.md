# Complete-trial source response under a shared observation channel

This independently reviewed conditional result concerns a population contrast in one fixed finite classical model. It supplies no physical transducer, calibration capability, finite-sample guarantee or unique-mechanism identification.

## Fixed law and observation contract

Use precisely the [active residual-to-structure law through four births](../track_b/native_active_residual_v1.md), with the original fair-mark structural rule in [Part A of the marked-law specification](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). Its fixed coefficients are theta=1/32, t=1/2 and (a_0,a_1,a_2,a_3,a_4)=(1/264,1/264,1/176,1/44,1). The linked law specifies every branch map B on every actual ideal, all immutable binary marks and the common two-state positive cone. Its complete matrix history identity is the mathematical dependency used here. No law, support or horizon is changed.

Each trial starts at empty with the actual pure residual delta_i, i=0 or 1, supplied in the same carrier coordinates. Record the source selection before the trial; use the same dynamics and detector for both settings. Exactly four births complete the trial. There is no separately prepared singleton, intermediate intervention/readout, first-mark conditioning, early stopping, overwrite or retry. Every first mark and continuation is included. Four births is bookkeeping, not calibrated duration.

The sole native event is Z(E)=1 when the complete terminal unmarked four-vertex order E is an antichain, and Z(E)=0 otherwise. Terminal marks and failure flags may remain audit metadata; neither they nor residual measurements are additional decision features.

Report Y in {0,1,perp}, with perp an explicit erasure. For one common tuple xi=(f,n,e), with false-positive rate f, false-negative rate n and erasure rate e, the complete detector is:

| Report Y | True Z=0 | True Z=1 |
| --- | ---: | ---: |
| 0 | (1-e)(1-f) | (1-e)n |
| 1 | (1-e)f | (1-e)(1-n) |
| perp | e | e |

Its independently specified uncertainty domain is the nonempty closed box
C=[f_-,f_+] x [n_-,n_+] x [e_-,e_+],
with intervals in [0,1], e_+<1 and f_++n_+<1. These are assumptions, not measured bounds. The same unknown tuple applies to both settings. Conditional on Z, the detector has no additional dependence on source, residual state, old marks, terminal shape or history; erasure is independent of Z and setting. This conditional channel does not assert independent repeated trials or independent calibration estimates. The entire box, including all parameter combinations, is retained.

## Complete native endpoint laws

Write a=1/264, s_i=(-1)^i, u=(1/2,1/2)^T, v=(1/2,-1/2)^T and W=[u v]. For a complete naturally encoded marked history h, let
w_h=2^-4 product_(four births) q_C(S).
The full-history identity of the linked active law is
B_h=w_h W [[1,theta(H(E)-H(empty))],[0,1/16]] W^-1,
where H(P)=a_(|P|) times the indicator that P is an antichain. At the terminal horizon H(E)=Z(E), while H(empty)=a. Since 1^T W=(1,0) and W^-1 delta_i=(1,s_i)^T, its complete history mass is
L_i(h)=w_h[1+s_i theta(Z(E_h)-a)].

Natural birth names 1–4 are only a counting convention. Each actual ideal choice and newborn bit appears once; there is no additional permutation or automorphism multiplier. Complete reference-row normalization gives sum_h w_h=1. A terminal antichain requires the empty ideal at all four births. The structural factors are 1,2/3,1/4,1/44, independent of marks. Summing the four fair bits contributes (1/2+1/2)^4=1, so sum_(h:Z=1) w_h=a, with all other histories of total weight 1-a. An extra 4! would count these naturally encoded histories again.

Every L_i(h) is positive because |theta(Z-a)|<1, and its full sum is 1+s_i theta(a-a)=1. Thus the complete binary laws are
p_i(1)=a[1+s_i theta(1-a)],
p_i(0)=(1-a)[1-s_i theta a].
Every entry is positive and each row sums to one. All table entries share denominator D=2,230,272:

| Empty input | Z=0 numerator | Z=1 numerator |
| --- | ---: | ---: |
| delta0 | 2,221,561 | 8,711 |
| delta1 | 2,222,087 | 8,185 |

Put p_i=p_i(1). Then
Delta=p_0-p_1=2theta a(1-a)=263/1,115,136>0.
This is the complete-trial antichain event, not a selected-prefix or singleton contrast.

## Entire paired reported-law image

For xi in C, set k=1-f-n and z_i=f+k p_i. Detector composition gives, in outcome order (0,1,perp),
mu_i(xi)=((1-e)(1-z_i),(1-e)z_i,e).
Because z_i=f(1-p_i)+(1-n)p_i is a convex combination of numbers in [0,1], each mu_i is a probability vector. Permitted detector boundaries can give zero mass to a reported outcome even though every native history remains positive.

The exact full paired image is
R={ (((1-e)(1-f-kp_0),(1-e)(f+kp_0),e),
      ((1-e)(1-f-kp_1),(1-e)(f+kp_1),e)) :
      f in [f_-,f_+], n in [n_-,n_+], e in [e_-,e_+], k=1-f-n }.
One tuple is shared throughout each pair. The nonempty compact box and continuous map make R nonempty and compact; this is the whole image, not unrelated component bounds.

Equivalently, a pair of three-outcome probability vectors belongs to R exactly when their erasure components agree at an e in the stipulated interval and, defining
z_i=mu_i(1)/(1-e),
k=(z_0-z_1)/Delta,
f=z_0-kp_0,
n=1-f-k,
the reconstructed f and n lie in their respective stipulated intervals. Both denominators are positive. Substitution reconstructs both vectors with one detector. This is population-law membership, not estimation from finite counts.

The difference is
mu_1(xi)-mu_0(xi)=((1-e)k Delta,-(1-e)k Delta,0).
Consequently the exact minimum over the entire box is
Gamma=inf_(xi in C) ||mu_1(xi)-mu_0(xi)||_1
     =2Delta(1-e_+)(1-f_+-n_+)
     =(263/557,568)(1-e_+)(1-f_+-n_+)>0.
Both positive factors decrease towards their upper calibration endpoints, and that corner belongs to C. The contrast is therefore uniform over all permitted shared tuples. Widening uncertainty within this informative class cannot increase the guaranteed minimum.

The erasure factor remains in Gamma. Success-only conditioning would change the question. At f=n=e=0, when used as an allowed limit/check, the pointwise law is the native binary law with zero erasure and pointwise L1 distance 2Delta; this does not set a larger box's minimum to 2Delta. Marginal source-law regions may overlap under different nuisance tuples. The result concerns the paired same-detector source response, not perfect single-record classification or a finite-sample confidence statement.

## Controls with the same complete denominator

For the same normalized residual rho under both labels, put s=rho_0-rho_1. The complete laws become
p_rho(1)=a[1+s theta(1-a)],
p_rho(0)=(1-a)[1-s theta a].
The labels then give the same mu_rho and zero contrast. This equal-source control supplies no approximate-purity guarantee.

If detector columns coincide, the two source laws report the same column. For e<1 this occurs at f+n=1, giving mu_0=mu_1=((1-e)(1-f),(1-e)f,e). For total erasure e=1, both laws are (0,0,1), whatever f,n. These explicit null controls lie outside the informative promise.

The passive reference d=0,T=I gives B_h=w_h I. The forward-only reference d=0,T=M(0) gives B_h=w_h M(0)^4; column stochasticity makes its total history mass w_h for any normalized source. Thus both references have antichain probability a under either empty input and the common complete reported law
nu(xi)=((1-e)[1-f-(1-f-n)a],(1-e)[f+(1-f-n)a],e).
Their source-setting contrast is zero over the same box, with all branches, four births and erasures retained. These controls do not classify every alternative law: larger static-seed realizations and conventional classical descriptions remain possible. A source-dependent detector or unverified actual preparation changes the premises and is not covered by Gamma.

## Observation applicability and open physical mapping

Intended source labels do not certify actual delta0 and delta1. This contract assumes the pure preparations in common coordinates; uncertain or mixed physical preparations require their own justification. The physical preparation and reset maps, four-event completion certificate, complete order readout and independently calibrated detector remain unsupplied.

Every assigned attempt must remain in the ledger and denominator, including erasures and preparation, completion or acquisition failures. Missing or ambiguous relations never certify incomparability; without a complete four-event order certificate, report perp. An unverified failed preparation is not assigned an invented ideal trajectory or Z. Such failures belong to the mathematical common erasure row only when that model is independently justified; otherwise retain them and mark physical application inapplicable. Failure flags are audit metadata, not extra decision features with an unstated joint law.

Calibration must independently justify the intervals, common-channel stability, conditional factorization and event-independent erasure, using justified labels and provenance. The desired source contrast cannot calibrate its own detector. Record N_i(0), N_i(1), N_i(perp) with denominator N_i=sum_y N_i(y); no discarded failures or retry-until-detection. Counts do not by themselves supply a repetition/drift model, sample-size theorem or statistical error bound.

A competent conventional baseline receives the same source-label access at analysis, complete records, calibration/provenance, preprocessing and detector blinding. Account for every source-to-reset cost: preparation, record formation, failures, completion monitoring, acquisition, relation recovery, calibration, storage, processing and analysis. No efficiency or application-validation result follows.

This conditional construction supplies no energy, action, physical time, phase, acceleration, GWOSC, quantum or gravity correspondence. No unique physical mechanism, approximate-preparation guarantee, experiment or execution permission follows. Option B, Status M and all scientific, independent-review, calibration, custody and execution gates remain. The [native mapping programme](../coordination/NATIVE_MASS_MAPPING.md) retains physical source and readout correspondence as open work.
