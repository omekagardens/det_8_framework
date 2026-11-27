# Two record laws for the same mean Newtonian potential

An expectation value specifies an average field. To predict what a single observation records, one must also specify a probability law. For four fixed smooth sources, consider two proposals. The first records the potential averaged over source labels on every trial. The second samples a label and records that label’s potential. Both give the same average potential for every input density matrix. Only the sampled rule can arise from one fixed quantum measurement over the full input domain.

## Sources and observations

Let $a,b\in\{0,1\}$, $G,m,d>0$, and $\eta=d/4$. Each of the four configurations has density

$$
\rho_{ab}(x)=m f_\eta(x-ad\,e_1)+m f_\eta(x-(3+b)d\,e_1).
$$

Here $f_\eta$ is the normalized smooth radial bump supported in the ball of radius $\eta$ from the [smooth Newtonian source construction](smooth_newtonian_constraint_interface.md). Use its canonical potentials $\Phi_{ab}$ in the real homogeneous Sobolev space $\dot H^1(\mathbb R^3)$, with $L^6$ representatives. They satisfy the weak field equation

$$
\int\nabla\Phi_{ab}\cdot\nabla v=-4\pi G\int\rho_{ab}v .
$$

The proof needs just two distinct potentials. Write $g_3=f_\eta(\cdot-3d e_1)$ and $g_4=f_\eta(\cdot-4d e_1)$. Their supports are disjoint. Testing the difference of the equations for labels $00$ and $01$ with $g_3$ gives

$$
\int\nabla(\Phi_{00}-\Phi_{01})\cdot\nabla g_3
=-4\pi Gm\int g_3^2\ne0 .
$$

Thus $\Phi_{00}\ne\Phi_{01}$ in the gradient norm. The readout takes values in the convex hull of the four potentials, equipped with the Borel sets of this norm. The hull is compact because it is the continuous image of the four-label probability simplex. In particular, observing one specified potential is a well-defined mathematical event.

## The event that separates the laws

Supply a four-dimensional quantum system with orthonormal source-label basis $\lvert ab\rangle$ and rank-one projectors $\Pi_{ab}$. Given an arbitrary density matrix $\varrho$, write $p_{ab}=\operatorname{Tr}(\varrho\Pi_{ab})$ and $\bar\Phi=\sum_{ab}p_{ab}\Phi_{ab}$. The proposed laws for one observation are

$$
 Q^{\rm det}_{\varrho}=\delta_{\bar\Phi},
 \qquad Q^{\rm samp}_{\varrho}=\sum_{ab}p_{ab}\delta_{\Phi_{ab}} .
$$

A fixed positive operator-valued measure $M$ assigns event $E$ probability $\operatorname{Tr}[\varrho M(E)]$. This probability is affine in the input state. The same apparatus must work for every input, with a single copy, fixed settings, and no preparation label, state description or postselection.

Take the event $E_0=\{\Phi_{00}\}$. On input $\Pi_{00}$ its probability under either law is one. On $\Pi_{01}$ it is zero. A fixed measurement must therefore assign probability $1/2$ to this event on their equal mixture. The deterministic rule assigns zero because its only possible record is the midpoint $(\Phi_{00}+\Phi_{01})/2$, which differs from $\Phi_{00}$. This contradiction excludes every fixed POVM for the deterministic law over the stipulated input domain.

The following fixed measurement realizes the sampled law.

$$
 M_{\rm samp}(E)=\sum_{ab}\mathbf 1_E(\Phi_{ab})\Pi_{ab}.
$$

Each effect is positive and the full record space gives the identity. For disjoint events each label contributes to at most one event, so the effects are countably additive. Taking the trace against any density matrix gives exactly the sampled probabilities, including for coherent inputs. Coincident record values would simply collect the corresponding projectors.

The vector first moment of each law is $\bar\Phi$. Nevertheless, at the equal mixture the sampled rule gives $E_0$ probability $1/2$ and the deterministic rule gives it probability zero. A constraint on the mean alone leaves this observation undecided.

## Scope and provenance

This conditional calculation uses supplied Euclidean geometry, $G,m,d$, a quantum carrier, the Born rule and ideal noiseless access to an entire potential. A semiclassical field equation for an expectation value does not itself postulate the deterministic single-trial record tested here. Detector resolution, coupling, calibration and empirical applicability remain open. The calculation supplies no DET-native units or gravity dynamics.

The input pair, event and proof strategy were registered in advance and known to the author. An independent scientific review checked the smooth-source distinction, mixture test, sampled measurement and first moments. The research record retains an earlier out-of-scope point-source calculation and a capacity-check incident. Neither supplied evidence for this proof.
