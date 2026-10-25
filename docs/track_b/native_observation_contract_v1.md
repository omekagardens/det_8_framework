# Native observation: passive payloads and uncertain calibration

RI1488 — Conditional observation and identification boundaries

This standalone note combines independently reviewed QR-OBS001 and QR-OBS002. The [admitted finite model](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) uses passive scalar payload updates. Changing an intrinsic mark kernel may change native record probabilities; changes at unreachable contexts need not. Without native-record access, a parameter-independent payload/reference observer learns nothing about that kernel. A separately hypothesized record-sensitive channel can convey information, but unknown calibration can still prevent identification.

These are statements under explicit mathematical access and calibration contracts. Neither constructs a detector or identifies a GWOSC observable with a native record. Exact-law identification, finite-sample inference and physical implementation remain separate.

## Model and preparation

Fix the admitted finite horizon \(N\), eligibility and actual \(q(P,r,S)\). Use only the [positive intrinsic family](native_record_identifiability_v1.md):
\[
B_{\theta,S,b}^{P,r}(X)=q(P,r,S)p_{\theta,b}(K(S,r|_S))X,
\quad \sum_Sq=1,\quad \sum_b p_{\theta,b}(K)=1.
\]
Both sums are over complete admitted rows. No new \(q\), continuation or support is selected. For a complete naturally labelled length-\(N\) history \(h\),
\[
\Phi_{\theta,h}=L_\theta(h)\operatorname{id},\qquad
L_\theta(h)=\prod_{j=1}^N q(P_{j-1},r_{j-1},S_j)p_{\theta,b_j}(K_j).
\]
Successively summing the last complete row proves \(\sum_hL_\theta(h)=1\). Birth labels are bookkeeping, not physical time.

Prepare a normalized density operator \(\rho_{AR}\), independent of \(\theta\), on payload \(A\) and optional retained reference \(R\). Internal entanglement is allowed. Scalar branch maps act on \(A\), with identity on \(R\). Start with the stipulated empty native record; no initially correlated native side information is supplied.

## Factorization theorem

Introduce a classical register \(H\) for the complete native history. Its joint output is
\[
\Omega_\theta^{HAR}
=\sum_h L_\theta(h)|h\rangle\langle h|\otimes\rho_{AR}
=P_\theta^H\otimes\rho_{AR}.
\]
This follows directly by composing scalar branches, including their action on the reference. Marginalizing the entire native record gives
\[
\operatorname{Tr}_H\Omega_\theta=\rho_{AR}.
\]
Thus any fixed parameter-independent measurement or instrument on \(AR\) has the same output law for every \(\theta\). Reference-only and payload-only readouts are special cases. For any two parameters the accessible output distributions have total-variation distance zero; every binary test has type-I plus type-II error one, and equal-prior optimal error is \(1/2\). These are exact distributional statements, not sample-size guarantees for a detector.

## Discrete adaptive observer protocol

The same conclusion holds for a finite, externally fixed interleaving of native births and discrete observer instruments, with complete normalized finite or well-defined countable branch sums. No general continuous-outcome adaptive extension is certified. Observer instrument \(j\) has completely positive branches
\(\mathcal A_{j,z_j}^{z_{<j}}\) with trace-preserving complete sum. Branch choices may depend on previous observer outcomes, but neither on \(\theta\) nor native history, marks or native-derived timing. A fixed ancillary state independent of \(\theta\) may be absorbed into the carrier.

These operations have no influence on native \(q\), mark selection, support or horizon. Their outcome records are observer output, not additional native births. This is a mathematical access contract; it supplies no physical scheduling mechanism.

Write
\[
T_z=\mathcal A_{m,z_m}^{z_{<m}}\circ\cdots\circ\mathcal A_{1,z_1},
\qquad \nu(z)=\operatorname{Tr}T_z(\rho).
\]
At each fixed interleaving position a native branch multiplies the current operator by its scalar coefficient. Induction through the interleaving therefore yields the unnormalized joint block
\[
\Omega_\theta(h,z)=L_\theta(h)T_z(\rho).
\]
Native coefficients may depend on earlier native marks; the no-feedback premise makes them independent of \(z\). Summing complete observer instruments backwards gives \(\sum_z\nu(z)=1\). Consequently
\[
\Pr_\theta(h,z)=L_\theta(h)\nu(z),\qquad
\Omega_{\mathrm{observer}}=\sum_z|z\rangle\langle z|\otimes T_z(\rho),
\]
independent of \(\theta\), including both transcript and residual payload/reference. Own-output adaptivity cannot overcome this factorization.

Parameter-dependent preparation/controllers, native-record-conditioned control or postselection, native-dependent stopping/horizon, and record-to-detector coupling violate the premises and require separate analysis. Selection based only on a fixed observer-output event of positive probability preserves independence; selection reading native records is not covered. No hidden clock or privileged physical chronology is licensed.

## The missing observation bridge

A record-sensitive observation requires an explicit normalized kernel
\[
K(A\mid h,c),\qquad
\Pr_\theta(Y\in A\mid c)=\sum_h L_\theta(h)K(A\mid h,c),
\]
or an instrument realizing it, for registered outcome event \(A\) and fixed apparatus settings \(c\). This equation names the missing object; it does not construct one.

For two candidate parameters, this channel distinguishes their output laws exactly when some event satisfies
\[
\sum_h[L_\theta(h)-L_{\theta'}(h)]K(A\mid h,c)\ne0.
\]
Dependence of \(K\) on \(h\) alone is insufficient if differences cancel. Under the current access contract \(K(A\mid h,c)=\nu_c(A)\), so normalization forces zero contrast.

Supplying the bridge would require an operationally specified admitted record variable, legitimate record-sensitive access/coupling, parameter-independent preparation and settings, and calibration/noise/selection premises. None is supplied here. No GWOSC observable is identified with \(h\). The [QR-LD001 unitary extension](native_passivity_choice_v1.md) remains unadopted; this theorem uses the actual passive prescription. There is no quantum/gravity derivation, physical no-go, empirical discriminator, new dynamics or automatic successor.


---

# Calibration of a hypothetical binary readout

## Fixed source and hypothetical observation

Keep the admitted seed, actual \(q\), support and horizon \(N=3\). Let \(X=1\) mean the terminal three-vertex order is a chain. For the intrinsic constant mark kernel \(p_0(K)=t\), the [accepted finite record-law result](native_record_identifiability_v1.md) gives
\[
\pi(t)=\Pr_t(X=1)=\frac13\left[t\frac{19}{30}+(1-t)\frac7{15}\right]
=\frac7{45}+\frac{t}{18}.
\]
For \(H_-:t=1/3\) and \(H_+:t=2/3\),
\[
\pi_-=\frac{47}{270},\qquad \pi_+=\frac{52}{270},
\qquad \pi_+-\pi_-=\frac1{54}.
\]
These two changes affect the admitted chain-event law. Kernel changes in general may change finite record laws; unreachable changes need not.

Introduce only the hypothetical binary channel
\[
\Pr(Y=1\mid X=0)=f,\quad
\Pr(Y=1\mid X=1)=f+g,\quad
f\ge0,\ g>0,\ f+g\le1.
\]
Here \(f\) is an observation offset, not the seed function \(f(i)\). The channel is parameter-independent for a fixed apparatus and depends on the native history only through \(X\). It grants record-sensitive access as an additional mathematical premise; it is not an admitted native instrument.

Total probability gives the complete output law
\[
Y\mid(H_i,f,g)\sim\operatorname{Bernoulli}(r_i(f,g)),
\qquad r_i(f,g)=f+g\pi_i.
\]

## Three calibration questions

**Known calibration.** If \(f,g\) are known, the exact output probability gives \(\pi=(r-f)/g\); the two hypotheses are distinct. Their binary-output total-variation distance is \(g/54\).

**Common but unknown calibration.** Holding the same unknown pair fixed,
\[
r_+(f,g)-r_-(f,g)=g/54>0.
\]
This is pointwise separation. It supplies neither the numerical threshold for an uncalibrated output law nor an experiment exposing both counterfactual laws. Unknown calibration remains a nuisance parameter; no apparatus is allowed to change during an actual observation.

**Uniform exact-law identification.** Require a single rule using the exact law of \(Y\) to return the correct hypothesis for every allowed nuisance pair. Declare
\[
\mathcal C=[f_L,f_U]\times[g_L,g_U],\quad
0\le f_L\le f_U,\quad0<g_L\le g_U,\quad f_U+g_U\le1.
\]
The last condition makes the whole rectangle admissible. The exact attainable sets of output probabilities are
\[
I_i=[\,f_L+g_L\pi_i,\ f_U+g_U\pi_i\,].
\]
Monotonicity gives these endpoints. Every intermediate value is attained by moving along the straight segment joining the two corner pairs; its affine image traverses the whole interval.

Since both endpoints of \(I_+\) exceed the corresponding endpoints of \(I_-\), the sets are disjoint exactly when
\[
f_U+g_U\pi_-<f_L+g_L\pi_+,
\]
or equivalently
\[
\delta:=\frac{g_L}{54}-(f_U-f_L)
-\frac{47}{270}(g_U-g_L)>0.
\]
This is necessary and sufficient for uniform exact-law identification over \(\mathcal C\). If it holds, a threshold strictly between the intervals classifies the exact probability. Otherwise the intervals overlap, including a shared endpoint when \(\delta=0\). At any shared value, two admissible worlds give the same Bernoulli law, so no rule of that law alone can identify both correctly.

A lower bound on gain gives a positive paired contrast \(g_L/54\); offset and gain uncertainty can nevertheless make the composite sets overlap.

## Explicit rational confounding

Take
\[
f\in[0,1/54],\qquad g_L=g_U=1/2.
\]
Then \(f_U+g_U=14/27<1\), and
\[
I_-=[47/540,57/540],\qquad
I_+=[52/540,62/540].
\]
Their overlap is \([52/540,57/540]\). In particular,
\[
(H_-,f=1/108,g=1/2)
\quad\text{and}\quad
(H_+,f=0,g=1/2)
\]
both give
\[
\Pr(Y=1)=\frac{1}{108}+\frac{47}{540}
=\frac{52}{540}=\frac{13}{135}.
\]
Each possible world has its own fixed, parameter-independent channel; within either world changing the hypothesis alone still produces contrast \(1/108\). The nuisance values differ between competing explanations of the same observed law, not between samples of one apparatus. Without calibration information, the exact output law cannot select between those explanations.

## What this establishes and what remains missing

Identification from an exact law is not guaranteed identification from a realized binary outcome. Here \(0<r_i<1\), so either outcome can occur under either hypothesis even with known calibration. No sample size, repeated-world/reset contract or independence assumption is supplied. Additional calibration observations would define a different joint experiment.

A future proposal must name the admitted chain indicator and the registered output, justify record-sensitive access and the channel's parameter independence, specify preparation and selection/noise conditions, and establish fixed calibration values or defensible bounds. For guaranteed identification from this binary law alone, those bounds must separate the two attainable sets; positive gain alone is insufficient.

The physical bridge remains an actual justified mapping from the admitted record variable to a registered measurement. Positing this channel does not provide that mapping or an apparatus. QR-OBS001's passive payload-only result remains intact, at its accepted discrete-observer scope. No GWOSC mapping, physical no-go, dynamics adoption, quantum/gravity, agency, theological or Boundary conclusion follows.
