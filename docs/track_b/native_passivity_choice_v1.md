# Payload passivity and the meaning of normalization

RI1487 — Conditional law-dependence counterfamily

The [admitted model](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) explicitly prescribes passive scalar payload updates. This independently reviewed result, QR-LD001, studies a separate proposed extension while keeping its finite record-growth coefficients fixed. It distinguishes trace normalization from an identity nonselective map; neither the extension nor its hypothetical readout is adopted as native physics. The reconstruction criterion referenced below is stated in [Record probabilities and residual payload information](native_payload_information_v1.md).

## 1. What is relaxed

The admitted equation B_(S,b)(X)=q(P,r,S)X/2 explicitly defines a passive payload. A non-scalar update cannot satisfy that equation. The accepted model is unchanged.

Consider instead a **separate proposed extension** replacing only its payload-update prescription. Keep the actual finite q, existing horizon, all eligible ideals, strictly positive q rows, independently fair newborn marks, locality, equivariance and complete marked diamonds. No q optimization, coefficients or longer horizon are introduced.

Added premises: use a common two-dimensional complex matrix carrier with a fixed basis; order relabelings act trivially on that internal carrier. This carrier convention and the following unitary are supplied choices, not DET derivations. For one dimensionless parameter 0<=theta<=pi set
\[
 U_\theta=\operatorname{diag}(1,e^{i\theta}),\qquad
 \mathcal C_\theta(X)=U_\theta XU_\theta^\dagger,\qquad
 \mathcal B^{P,r;\theta}_{S,b}(X)
 =\frac{q(P,r,S)}2\,\mathcal C_\theta(X). \tag{1}
\]
The same channel is used at every admitted birth, independent of the precursor, marks and numerical labels. Theta=0 recovers the passive prescription on this carrier. No action, energy or physical time scale is attached.

## 2. Normalization, fairness and covariance

Each branch has Kraus operator sqrt(q/2) U_theta. It is completely positive and trace-nonincreasing, since 0<q<=1. For every positive X,
\[
 \operatorname{Tr}\mathcal B_{S,b}^{\theta}(X)
 =\frac q2\operatorname{Tr}X,\qquad
 \sum_{S,b}\mathcal B_{S,b}^{\theta}(X)=\mathcal C_\theta(X).
 \tag{2}
\]
The complete sum preserves trace; normalized input therefore gives a normalized finite instrument and the same positive branch weights q/2. Conditional on any past and selected S, each newborn bit has probability one half. Summing over S keeps it fair conditional on the whole past.

For proper S, q reads only the allowed old marks and the unmarked parent. The fixed C_theta reads no marks, so the full branch inherits that locality. Relabeling transports P,r,S and preserves q; its stipulated trivial action on the carrier leaves C_theta unchanged. Eligibility and immutable marks are retained.

**Normalization distinction.** The sum in (2) is generally not the identity map. Trace normalization and sum_S q=1 are retained; the original nonselective identity map was a consequence of its passive defining equation. If one independently demands sum_(S,b) B_(S,b)=Id as a map, this counterfamily does not qualify.

Indeed that extra demand, together with positivity and the fixed input-independent weights q/2, would force passivity. For a pure input rho, positive branch outputs summing to the rank-one rho must each be supported on its one-dimensional range. Their fixed traces give B_(S,b)(rho)=(q/2)rho. Pure projectors span Hermitian matrices; linearity gives the passive formula on every matrix. This separates the two meanings of normalization rather than silently identifying them.

## 3. Complete diamonds and suffix transport

For incomparable births x over S with bit b and y over T with bit c, the two full composed maps on X are
\[
 \frac{q(C,r,S)q(C+S,r+b,T)}4\,\mathcal C_\theta^2(X),
 \qquad
 \frac{q(C,r,T)q(C+T,r+c,S)}4\,\mathcal C_\theta^2(X).
 \tag{3}
\]
The supplied all-mark q diamond equates their coefficients. Thus the unnormalized maps agree on every matrix, not merely in trace. This includes all four b,c choices, all old markings, S=T, and a formerly full precursor becoming proper after the other birth. Comparable births are not swapped.

After this swap the marked parents agree under transport. Every subsequent precursor and q evaluation is transported identically, and the channel remains the same. Composing the same transported suffix preserves the full-map equality, including suffix ideals containing swapped vertices. Adjacent incomparable swaps connect the natural encodings of a given marked endpoint, so full natural-label transport survives.

For any admitted n-birth history h,
\[
 \mathcal B^\theta_h(X)=L_{\rm fair}(h)\,\mathcal C_\theta^n(X),
 \qquad L_{\rm fair}(h)=\prod_{j=1}^n \frac{q(P_{j-1},r_{j-1},S_j)}2.
 \tag{4}
\]
Every actual q factor remains. Equal endpoint-fibre weights and common n give equal full maps within each fibre. RI1485's uniform-label reconstruction therefore still applies on this stipulated carrier. This is not a classification of non-scalar extensions.

## 4. Identical classical records, separated hypothetical payloads

The decisive record-law identity is
\[
 \operatorname{Tr}\mathcal B^\theta_h(\rho)=L_{\rm fair}(h)
 \quad\text{for every normalized input }\rho. \tag{5}
\]
It holds for every theta and each admitted prefix or terminal history. Hence no classical marked-record observation or further record summary identifies theta within this family. The unchanged records do not imply unchanged residual payloads.

A smallest witness uses the first birth, already inside the existing horizon. **Additional access premise:** prepare the same known
rho_+=|+><+|, |+>=(|0>+|1>)/sqrt(2), and after that first birth perform the same payload test E_+=rho_+, in the fixed carrier basis, under either candidate. This is a hypothetical preparation/readout contract; it is not supplied by the records.

The empty parent has its sole ideal with q=1. Both newborn bits retain probability one half, while the conditional and unselected payload is C_theta(rho_+). The stipulated test gives
\[
 \Pr_\theta(+)=\operatorname{Tr}[E_+\mathcal C_\theta(\rho_+)]
 =\left|\frac{1+e^{i\theta}}2\right|^2
 =\frac{1+\cos\theta}{2}. \tag{6}
\]
It is one at theta=0 and zero at theta=pi. Thus the two members are perfectly distinguishable under this added access, although their classical marked histories have identical laws.

The preparation and test are held fixed across candidates; a change of carrier coordinates must also transform them. This is conditional operational distinction, not selection of a physical frame. Access after one birth is explicit: no separation claim for every later terminal observation is made, and repeated updates can alias. The bookkeeping birth index is not a physical clock.

## 5. Scientific limitation

The retained structural requirements do not select passivity under trace normalization and the stated carrier convention. They permit this supplied payload evolution independently of record selection. This does not derive that evolution from DET, make it novel, or admit it as native dynamics.

Choosing among these candidates needs an additional model principle fixing the update, or a justified preparation/readout and empirical comparison that actually constrains it. Neither is supplied here. Classical marked records alone cannot choose, by (5). A separately required identity nonselective map would instead exclude the alternatives as shown above.

No physical instrument, non-scalar native adoption, quantum/gravity reconstruction, action scale or Boundary inference follows. All protected validation/custody, ABSTAIN, Status M, zero qualification and RET-only pause gates remain.
