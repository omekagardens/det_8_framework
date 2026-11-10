# Opposite boundary inertances in two positive-mass spring networks

At the same drive frequency, seven signed force readings give a boundary inertance of $-19m/21$ on a chain and $+7m/3$ on a diamond. Each network contains three moving masses of mass $m>0$. The measurement isolates a particular frequency component even when the two interior masses begin with unknown positions and velocities.

## Trial and force convention

Start from the two-handle prefix $a<b$ with marks $(0,0)$ and counts $(1,0)$. After two births under the specified precursor law, the registered descendant counts $(3,2,1,0)$ select the chain $s-u-v-t$ and $(3,1,1,0)$ select the diamond formed by $s-u-t$ and $s-v-t$. The count-one pair in the diamond is unordered. All other supported histories are inactive. The unconditional probabilities of chain, diamond and inactivity are respectively $779/1320$, $172/1320$ and $369/1320$. An inactive trial has no apparatus or force reading. [Carrier and attachment rule](terminal_counts_and_field_placement.md)

Clamp $t$, attach the three equal point masses to $s,u,v$, and put a linear spring of stiffness $k>0$ on each undirected cover. The actuator prescribes $x=q_s=A\cos[\omega(t_{\rm clock}-3\Delta)]$ with $A>0$, $\Omega=\sqrt{k/m}$, $\Delta=\pi/(2\Omega)$ and $\omega=\sqrt{5/4}\,\Omega$. The seven readings $F_n$ are the forces **exerted by the actuator on the network** at $t_{\rm clock}=n\Delta$, $n=0,\ldots,6$. The displacement maximum occurs at sample 3.

## Static baseline and driven response

For interior displacements $y=(q_u,q_v)^\top$, the force and interior equations are
$$
F=m\ddot x+k(d x-b^\top y),\qquad m\ddot y+k B y=k b x .
$$
For the chain, $d=1$, $b=(1,0)^\top$ and $B$ has diagonal entries 2 and off-diagonal entries $-1$. For the diamond, $d=2$, $b=(1,1)^\top$ and $B=2I$. Static equilibrium gives $K(0)=k(d-b^\top B^{-1}b)$. At the drive tone $r=m\omega^2/k=5/4$, the particular force per unit displacement is $K(\omega)=k[d-r-b^\top(B-rI)^{-1}b]$. The term $-r$ accounts for the driven endpoint's own inertia.

| Graph | Modelled static stiffness $K(0)$ | Driven stiffness $K(\omega)$ | $[K(0)-K(\omega)]/\omega^2$ |
| --- | ---: | ---: | ---: |
| Chain | $k/3$ | $41k/28$ | $-19m/21$ |
| Diamond | $k$ | $-23k/12$ | $+7m/3$ |

The flag identifies the graph before any force reading. With the supplied spring constants and masses, it selects the equilibrium baseline and predicts the entries in the table. An independently measured force trace would test the dynamic prediction. All seven recorded forces belong to the driven experiment.

## Removing interior oscillations

The homogeneous interior motion contributes arbitrary sine and cosine amplitudes at $\Omega,\sqrt3\,\Omega$ for the chain and at $\sqrt2\,\Omega$ for the diamond. The antisymmetric diamond mode cancels in the force sum. Define real coefficients $p_n$ by
$$
\sum_{n=0}^6p_n z^n=\prod_{j=1}^{3}\bigl(1-2z\cos(\sqrt j\,\pi/2)+z^2\bigr).
$$
The polynomial vanishes at both sampled phases of every possible free tone. With $\beta=\omega\Delta$, the centered drive has gain $G=8\prod_{j=1}^3[\cos\beta-\cos(\sqrt j\,\pi/2)]$. The angles $\pi/2,\beta,\sqrt2\,\pi/2,\sqrt3\,\pi/2$ are distinct and lie in $(0,\pi)$, so $G\ne0$. The common readout is
$$
\widehat K=\frac{\sum_{n=0}^6p_nF_n}{AG}.
$$
A single central force can be zero in both networks. At the displacement maximum, adding a symmetric homogeneous displacement to the two interior masses can cancel either network's particular force. Errors in the seven readings enter the same weighted sum. Experimental precision would require a force-error model.

On either active trial, the mechanical energy is the sum of the three kinetic energies and one positive quadratic extension energy per spring. Its time derivative is $F\dot x$ because the clamp is stationary. Both signs of the boundary response are compatible with positive stored energy. The native growth law supplies the carrier and its probability. Force and time standards, constitutive laws and any coupling to gravity require independent physical inputs. The separate spring-sector protocol measures positive inertial mass ratios under its own registration. [Sector mass ratios](sector_inertial_mass_ratios.md) · [Milton and Seppecher, finite-network background, 2011, v1](https://arxiv.org/abs/1105.0941v1)
