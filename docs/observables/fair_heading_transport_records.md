# Fair hidden headings can change finite endpoint records

GDM055 establishes a conditional finite transport result attached to the accepted [active residual law through four births](../track_b/native_active_residual_v1.md). A persistent fair heading and an independent fair heading have equal one-step marginals but different endpoint record laws at fixed horizons two through four. This is a supplied transport model, not a derivation of physical matter or native geometry.

## Fixed joint law

Keep every eligible actual ideal and native bit in the source law

\[
B_{C,S,b}=\frac{q_C(S)}2M(r_C(S)),\qquad
M(r)=\tfrac12\begin{pmatrix}1+r+t&1-r-t\\1+r-t&1-r+t\end{pmatrix},\quad t=1/2.
\]

The linked source fixes \(q_C(S)\) and \(r_C(S)\), their support and the horizon. The two-state cone is nonnegative, \(e^T=(1,1)\), and \(u=(1,1)^T/2\). Accepted identities include branch positivity, normalization, \(B_{C,S,b}u=(q_C(S)/2)u\), the nonselective map \(M(0)\), covariance, complete unnormalized marked diamonds and their allowed suffixes through four births.

Supply an additional state \((x,h)\in\mathbb Z/11\mathbb Z\times\{-1,+1\}\) and, for \(\rho\in\{0,1/2\}\), the kernel

\[
T_\rho(x',h'\mid x,h)=\frac{1+\rho hh'}2
\mathbf1\{x'=x+h'\pmod {11}\}.
\]

Attach exactly one branch-independent update per native birth:

\[
\widehat B_{C,S,b}=B_{C,S,b}\otimes T_\rho.
\]

This acts on the full 44-dimensional nonnegative cone, including correlated inputs. Position space, heading, product attachment and the update convention are supplied premises. No native mark, ideal, birth name or setting enters \(T_\rho\).

Each column of \(T_\rho\) sums to one; forbidden displacements retain exact zero probability. Thus joint normalization holds on the full cone. Native branch eligibility remains positive there. The nonselective joint map is \(M(0)\otimes T_\rho\), not an identity map. Native relabelings act trivially on transport. Every exact native diamond equality tensors with \(T_\rho^2\); an allowed common suffix tensors with further powers of \(T_\rho\). Hence complete marked diamonds and suffixes survive, for arbitrary correlations, with old marks, bits and actual ideals retained. No detector diamond is asserted. Also

\[
(I_2\otimes j^T)(B\otimes T_\rho)=B(I_2\otimes j^T),
\]

where \(j^T\) sums the transport states. There is no transport feedback into the native marginal even on correlated inputs.

## Preparation and complete records

Choose \(n\in\{1,2,3,4\}\) before preparation. Prepare \(u\otimes\tau_0\), where \(\tau_0(x,h)=\mathbf1\{x=0\}/2\). The initial heading is hidden and fair, not fixed. For a complete naturally labelled native history \(\gamma\) with all actual ideals and bits retained,

\[
w_\gamma=e^TB_\gamma u=2^{-n}\prod_{i=1}^nq_{C_i}(S_i),
\qquad B_\gamma u=w_\gamma u,\qquad\sum_\gamma w_\gamma=1.
\]

Distinct encodings are not quotiented away. The conditional transport output is \(T_\rho^n\tau_0\); write its endpoint marginal as \(f_{\rho,n}(x)\).

A common supplied detector has twelve outcomes: the eleven cyclic positions and failure \(\bot\). It reports the actual position with probability \(1/2\), otherwise failure with probability \(1/2\); it never reports heading. The full joint record law is

\[
P_{\rho,n}(\gamma,x)=\frac{w_\gamma}{2}f_{\rho,n}(x),
\qquad P_{\rho,n}(\gamma,\bot)=\frac{w_\gamma}{2}.
\]

All failures and zeros are retained; the law sums to one. At \(n<4\), this is an external terminal readout of a fixed native prefix, not an added native early-stop branch or a fifth birth. Native history and transport are independent for this product preparation; arbitrary correlated preparations are covered by the operator identities, not by this factorized observation formula.

## Exact finite endpoint table

Put \(p=(1+\rho)/2\) and \(q_f=(1-\rho)/2\), distinguishing \(q_f\) from native ideal weights. A heading word \((h_1,\ldots,h_n)\) has probability

\[
\tfrac12\prod_{i=2}^n
\begin{cases}p,&h_i=h_{i-1},\\q_f,&h_i\ne h_{i-1}.\end{cases}
\]

Its endpoint is \(\sum_i h_i\pmod {11}\). The integers from -4 through 4 are distinct cyclic residues, so these fixed horizons have no endpoint aliasing. Grouping all \(2^n\) heading words gives:

| Horizon | Endpoint | Persistent \(\rho=1/2\) | Independent \(\rho=0\) |
|---|---|---:|---:|
| 1 | each of \(\pm1\) | 1/2 | 1/2 |
| 2 | each of \(\pm2\) | 3/8 | 1/4 |
| 2 | 0 | 1/4 | 1/2 |
| 3 | each of \(\pm3\) | 9/32 | 1/8 |
| 3 | each of \(\pm1\) | 7/32 | 3/8 |
| 4 | each of \(\pm4\) | 27/128 | 1/16 |
| 4 | each of \(\pm2\) | 3/16 | 1/4 |
| 4 | 0 | 13/64 | 3/8 |

Every unlisted cyclic endpoint has probability zero. The grouping formulas are: at horizon two, each extreme has \(p/2\) and the center \(q_f\); at three, each extreme has \(p^2/2\) and each inner endpoint \(pq_f+q_f^2/2\); at four, each extreme has \(p^3/2\), each \(\pm2\) endpoint \(pq_f\), and zero \(pq_f+q_f^3\). These formulas and the word law account for every history and its multiplicity.

Fairness is preserved because each heading receives \((p+q_f)/2=1/2\). Thus both comparators have the same single-step direction marginal at every step and zero mean displacement. At horizon one their complete record laws coincide: \(P(\gamma,\pm1)=w_\gamma/4\) and \(P(\gamma,\bot)=w_\gamma/2\).

## Distances, primary contrast and boundary

Including all native histories, position outcomes and failures, total variation is

\[
D_n=\tfrac12\sum_{\gamma,o}|P_{1/2,n}(\gamma,o)-P_{0,n}(\gamma,o)|
=\tfrac14\sum_x|f_{1/2,n}(x)-f_{0,n}(x)|.
\]

Consequently

\[
(D_1,D_2,D_3,D_4)=(0,1/8,5/32,19/128).
\]

For the primary horizon-two detected event \(x\in\{-2,+2\}\), probabilities are \(3/8\) and \(1/4\), with difference \(1/8\). This uses all trials, including failure; it is not postselected on detection. The endpoint differences at horizon four are \(+19/128\) at each extreme, \(-8/128\) at each \(\pm2\), and \(-22/128\) at zero, which yields the stated distance. Horizon four has smaller distance than three; these are separate endpoint readouts, not an accumulated transport record.

The comparison detects serial directional correlation after matching the fair initial heading and detector. Replacing this persistent model with this independent comparator loses endpoint predictions. It does not prove a unique hidden-state representation or rule out another correlated model or a static seed encoding the same finite laws. Native history contributes no additional information about \(\rho\) for the fixed product preparation.

There is no derivation of position units, clock, energy, momentum, inertia, mass, relativity, gravity, stable physical objects or calibrated detectors. Probability mass and the parameter \(\rho\) are not physical mass. The attached model has no native feedback; Option B/Status M claim boundaries remain. No new horizon, forcing, kernel, experiment or implementation is authorized by this finite result.

## Provenance

Scientific source GDM055 report SHA256 `0679f40f1e860f11e570e6e9d4e71f01acf004cdccd181e18144ebf2e07a386d`; independent review `8b1c15d3e547e2f864a97af7e2e3bf4bb0675133082223a10b5e2df9e96b90b4`; coordinator disposition `2f407b3e5f0c33516d550a2eca91273079382e509456a89a4259b033875f654f`. GDM054's prior procedural qualifications remain historical. This result has no scientific dependency on GDM053. The earlier E37 publication-author attempt remains incomplete without an artifact; this prospective assembly does not qualify it retrospectively.
