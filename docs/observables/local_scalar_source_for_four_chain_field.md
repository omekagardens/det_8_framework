# A local scalar source lift of the two-mode four-chain field

Conditional finite construction with a global gravity limitation

The proposed scalar attachment works. One real two-standing-mode field on a supplied flat three-torus simultaneously reproduces the accepted changed-prefix samples at one local probe, with one common field unit, and reproduces the full positive generator through its action-derived integrated Hamiltonian. Its symmetric kinetic stress tensor is locally conserved, and its product-ground-state energy density is finite, positive and spatially uniform. The same source does not admit the attempted static periodic weak-field gravitational solution: its nonzero spatial mean violates the periodic Poisson compatibility condition.

This is a conditional source construction on a prescribed background. It is not a native spatial or gravitational derivation, an isolated compact source, a material cavity, a full continuum quantum field theory, or an empirical preparation and measurement claim. The source and global-gravity decisions are distinct.

The [stationary two-mode construction](stationary_dynamics_for_four_chain_fields.md) supplies the dimensionless operators and changed-prefix Gaussian state. The [Gaussian field-transport construction](gaussian_field_transport_on_native_histories.md) supplies the kinematic context; its original saturated prefix remains excluded. The [static stress example](stress_quadrupole_at_equal_energy.md) identifies the separate need for spatial source information.

Retain exactly the two canonical pairs, $[Q_j,P_k]=i\delta_{jk}I$, on $L^2(\mathbb R^2)$, and the centered product Gaussian with quadrature variances $1/2$. Define
$$
 \theta_1=\frac{5\pi}{4},\quad\theta_2=\frac{7\pi}{4},\qquad
 a_1^2=\frac{\beta}{2}(\sqrt2-1),\quad
 a_2^2=\frac{\beta}{2}(\sqrt2+1),\quad a_j>0,\ \beta>0,
$$
$$
 K=\frac12\sum_{j=1}^2\theta_j(Q_j^2+P_j^2),\qquad
 \phi_n=\sum_{j=1}^2a_j\bigl(Q_j\cos n\theta_j+P_j\sin n\theta_j\bigr).
 \tag{1}
$$
The unaliased advances in (1), not just their residues at integer samples, are stipulated. The admitted four ticks are $n=0,1,2,3$, representing the supported chain $a<b<x<y$. The native law supplies neither their physical separation nor their spatial coordinates.

Supply $c,\tau,A_*,\kappa>0$: propagation speed, physical duration per tick, action reference, and scalar kinetic-density normalization. Use a flat spatial torus with one common side $L$ and volume $V=L^3$. Supply the orthogonal axes $e_1,e_2,e_3$ and wavevectors
$$
 k_1=\frac{2\pi}{L}5e_1,\qquad k_2=\frac{2\pi}{L}7e_2,\qquad
 \omega_j=c|k_j|=\frac{\theta_j}{\tau}.
$$
Both frequency equalities require the same relation
$$
 \boxed{L=8c\tau.} \tag{2}
$$
It is a compatibility relation within these chosen integer modes and the supplied wave equation. It does not calibrate $c,\tau$ or $L$ from native order.

Choose the single scalar kinetic action
$$
 {\cal S}_{\rm sc}=\frac{\kappa}{2}\int dt\int_{\mathbb T_L^3}d^3x
 \left[\frac{\dot\Psi^2}{c^2}-|\nabla\Psi|^2\right].
 \tag{3}
$$
Its classical equation is $c^{-2}\ddot\Psi-\nabla^2\Psi=0$. Its two-mode restriction is quantized with the supplied action reference $A_*$. For real standing profiles $u_j(x)=\cos(k_j\cdot x+\delta_j)$, periodic integration gives
$$
 \int u_ju_k\,d^3x=\frac V2\delta_{jk},\qquad
 \int\nabla u_j\cdot\nabla u_k\,d^3x=\frac V2|k_j|^2\delta_{jk}.
 \tag{4}
$$
These identities hold for the phase choices below. In particular each mode has zero spatial mean, and the cross integrals vanish.

Writing $\Psi=\sum_jq_j(t)u_j(x)$, the reduced action is the sum of two oscillators:
$$
 {\cal L}_{\rm red}=\sum_j\frac{\mu}{2}(\dot q_j^2-\omega_j^2q_j^2),
 \qquad \mu=\frac{\kappa V}{2c^2},\qquad p_j=\mu\dot q_j.
 \tag{5}
$$
The coefficient $\mu$ is a generalized mode inertia; it is not an independently measured carrier mass. Set
$$
 B_j=\sqrt{\frac{2A_*c^2}{\kappa V\omega_j}},\qquad
 X_j(t)=Q_j\cos\omega_jt+P_j\sin\omega_jt,\qquad
 Y_j(t)=P_j\cos\omega_jt-Q_j\sin\omega_jt,
$$
$$
 \Psi(t,x)=\sum_j B_j u_j(x)X_j(t),\qquad
 q_j=B_jX_j,\qquad p_j=\mu B_j\omega_jY_j.
 \tag{6}
$$
Then $[q_j,p_k]=iA_*\delta_{jk}I$ because $\mu B_j^2\omega_j=A_*$. The field is real in the sense of self-adjoint linear quadratures and solves the wave equation exactly on the retained modes.

The energy density and its integral from the same action are
$$
 {\cal H}(t,x)=\frac{\kappa}{2}
   \left[\frac{\dot\Psi^2}{c^2}+|\nabla\Psi|^2\right],\qquad
 H_{\rm sc}=\int{\cal H}\,d^3x.
$$
Using (4) and (6), including the vanishing cross-mode integrals,
$$
 H_{\rm sc}
 =\sum_j\frac{\kappa V B_j^2\omega_j^2}{4c^2}
        (X_j^2+Y_j^2)
 =\frac12\sum_jA_*\omega_j(Q_j^2+P_j^2)
 =\boxed{\frac{A_*}{\tau}K}. \tag{7}
$$
The rotation identity $X_j^2+Y_j^2=Q_j^2+P_j^2$ preserves operator ordering. Thus $e^{itH_{\rm sc}/A_*}$ generates (6) with the standard positive-time Heisenberg convention. No unrelated mode energies or identity offset were assigned.

Now fix one local probe and one set of spatial phases:
$$
 x_*=0,\qquad
 \delta_2=0,\qquad
 \delta_1=\arccos\!\left[(\sqrt2-1)\sqrt{\frac57}\right],\qquad
 F_*=\frac{B_2}{a_2}>0. \tag{8}
$$
The argument of the arccosine lies strictly between zero and one. The Hamiltonian normalization fixes $B_1/B_2=\sqrt{7/5}$, while $a_1/a_2=\sqrt2-1$. Consequently
$$
 B_1\cos\delta_1=F_*a_1,\qquad
 B_2\cos\delta_2=F_*a_2.
$$
For all four assigned ticks this proves the operator identity
$$
 \boxed{\Psi(n\tau,0)=F_*\phi_n,\qquad n=0,1,2,3.} \tag{9}
$$
Only one common local field sample is used. There is no mode-dependent detector gain, change to the native $a_j$, or replacement of the point probe by a weighted spatial readout. The chosen standing phases are disclosed spatial-attachment data, selected to achieve the match; they are not independently predicted native phases.

In particular, in the same product ground state,
$$
 \langle\Psi(n\tau,0)\Psi(m\tau,0)\rangle
   =\frac{F_*^2}{2}\sum_ja_j^2e^{-i(n-m)\theta_j},\qquad
 [\Psi(n\tau,0),\Psi(m\tau,0)]
   =iF_*^2\beta\,\operatorname{sign}(n-m)I\quad(n\ne m). \tag{10}
$$
After dividing the covariance by $F_*^2$, the positive-lag entries at lags $0,1,2,3$ are exactly
$$
 \frac{\beta}{\sqrt2},\quad
 \frac{\beta}{2\sqrt2}+\frac{i\beta}{2},\quad
 \frac{i\beta}{2},\quad
 -\frac{\beta}{2\sqrt2}+\frac{i\beta}{2},
$$
with negative lags given by conjugation. Thus the complete accepted four-tick covariance, its positivity and the changed prefix are preserved. The original saturated $W_2$ remains excluded. Equation (10) is a quantum covariance identity, not a joint classical measurement distribution for noncommuting samples.

Take $x^0=ct$, $\eta=\operatorname{diag}(-1,1,1,1)$, and the symmetric kinetic tensor associated with (3), with no improvement term:
$$
 T^{\mu\nu}=\kappa\left[
 \frac12\{\partial^\mu\Psi,\partial^\nu\Psi\}
 -\frac12\eta^{\mu\nu}Z\right],\qquad
 Z=\frac12\eta^{\alpha\gamma}
       \{\partial_\alpha\Psi,\partial_\gamma\Psi\}.
 \tag{11}
$$
This is the Weyl-ordered form of the minimally coupled scalar kinetic stress. Choosing this tensor rather than an improved tensor is part of the conventional attachment. In diagonal coordinates $Z=-(\dot\Psi/c)^2+|\nabla\Psi|^2$, so $T^{00}={\cal H}$, exactly the density integrated in (7).

All fields and derivatives are finite linear combinations of canonical operators. Their quadratic products and the displayed identities are defined on the common Schwartz domain in $L^2(\mathbb R^2)$, invariant under the oscillator evolution. On this domain $T^{00}$ is a nonnegative quadratic form, a sum of squares with positive coefficients. No ultraviolet sum or subtraction is needed for this finite-mode calculation. It is not a claim about the vacuum of the untruncated scalar field.

Differentiating the symmetric products in (11), the mixed-derivative terms cancel the derivative of $Z$, leaving
$$
 \partial_\mu T^{\mu\nu}
 =\frac{\kappa}{2}\{\Box\Psi,\partial^\nu\Psi\}=0,
 \qquad \Box=-c^{-2}\partial_t^2+\nabla^2. \tag{12}
$$
This is a local operator identity on the stated domain. Each standing mode obeys $\Box\Psi=0$, and the profiles and all derivatives match periodically. The tensor is symmetric and its energy integral is the Hamiltonian already matched in (7).

For complete ground-source expectations, let
$$
 \alpha_j(x)=k_j\cdot x+\delta_j,\quad
 E_j=\frac{A_*\omega_j}{2},\quad \rho_j=\frac{E_j}{V},\quad
 d_1=e_1,\quad d_2=e_2.
$$
In the product ground state, $\langle X_j^2\rangle=\langle Y_j^2\rangle=1/2$,
$\langle\{X_j,Y_j\}\rangle=0$, and all cross-mode contractions vanish. Hence
$$
 \langle\Psi\rangle=0,\qquad
 \langle\Psi^2(t,x)\rangle=\frac12\sum_j B_j^2\cos^2\alpha_j,
$$
$$
 \left\langle\frac{\dot\Psi^2}{c^2}\right\rangle
 =\frac12\sum_j B_j^2|k_j|^2\cos^2\alpha_j,\qquad
 \langle\partial_a\Psi\,\partial_b\Psi\rangle
 =\frac12\sum_j B_j^2|k_j|^2
       \sin^2\alpha_j\,d_j^a d_j^b.
$$
Substitution gives every source component:
$$
 \boxed{\langle T^{00}\rangle=\rho_1+\rho_2>0,\qquad
 \langle T^{0a}\rangle=0,}
$$
$$
 \boxed{\langle T^{ab}\rangle
 =\sum_{j=1}^2\rho_j
 \left[d_j^a d_j^b+
       (\delta^{ab}-d_j^a d_j^b)\cos(2\alpha_j)\right].} \tag{13}
$$
There is no time dependence in these expectations. Explicitly the spatial tensor is diagonal:
$$
 \langle T^{11}\rangle=\rho_1+\rho_2\cos2\alpha_2,\quad
 \langle T^{22}\rangle=\rho_2+\rho_1\cos2\alpha_1,\quad
 \langle T^{33}\rangle=\rho_1\cos2\alpha_1+\rho_2\cos2\alpha_2.
$$
Its divergence vanishes: each mode's longitudinal entry is constant and its varying transverse entries have no derivative along their own divergence direction. This also checks (12) directly in the specified state.

The integrated ground energy and stresses are
$$
 E_1=\frac{5\pi A_*}{8\tau},\quad
 E_2=\frac{7\pi A_*}{8\tau},\quad
 E_0=E_1+E_2=\frac{3\pi A_*}{2\tau}>0,
$$
$$
 \int\langle T^{ab}\rangle d^3x
 =\operatorname{diag}(E_1,E_2,0),\qquad
 \int\left\langle T^{00}+\sum_aT^{aa}\right\rangle d^3x=2E_0.
 \tag{14}
$$
In particular the conserved periodic source does not have vanishing integrated stress. The compact isolated-source identity obtained by integrating $\partial_a(x_bT^{ac})$ cannot be used here: $x_b$ is not a single-valued periodic function and its boundary terms do not cancel. The torus is a compact spatial manifold, not an isolated compact source in $\mathbb R^3$. We infer neither a boost-defined whole-carrier mass nor an asymptotically defined active monopole from (14).

Finite mode count also does not supply the full local canonical field algebra. With $\Pi=\kappa\dot\Psi/c^2$,
$$
 [\Psi(t,x),\Pi(t,y)]
 =iA_*\frac2V\sum_{j=1}^2u_j(x)u_j(y), \tag{15}
$$
the projector kernel onto the two standing profiles, rather than a periodic spatial delta function. Equal-time field-field and momentum-momentum commutators vanish. There are two oscillator pairs on an infinite-dimensional Hilbert space, not a finite-dimensional Hilbert space. “Local tensor” here means a density formed from field derivatives at the same point obeying local conservation. It does not establish microcausality, a Lorentz-invariant truncation or the complete scalar quantum field theory. The absent constant scalar mode does not remove the nonzero constant Fourier component of the quadratic energy density.

The global gravitational limit is explicit. If one attempts the static periodic linearized Einstein-source equation in the usual flat-background convention,
$$
 \nabla^2\bar h_{00}=-\frac{16\pi G}{c^4}\langle T_{00}\rangle,
$$
integration over the torus requires
$$
 0=-\frac{16\pi G}{c^4}E_0,
$$
which is impossible for the positive $E_0$ in (14). The corresponding lapse equation
$\nabla^2h_{00}=-(8\pi G/c^4)\langle T_{00}+\sum_aT_{aa}\rangle$
fails the same mean-source condition, with integrated source $2E_0$. No choice of the constant metric potential repairs a nonzero right-hand-side mean. There is no asymptotic exterior on this spatial geometry.

Thus this work supplies a conserved test-source tensor on the prescribed flat torus, not a solved static gravitational field or a self-consistent gravitating periodic ground state. Subtracting the source mean, adding a compensating source, changing the background to a cosmology or supplying walls would change the problem; none is done here. No stronger nonlinear existence or impossibility claim is made.

The full native probability bookkeeping is retained from the [finite source table](finite_interval_action_and_source_preparation.md). At the fixed prepared $a<b$ with marks $(i,0)$, the two later predecessor ideals have the following structural numerators over $1320$; concatenation denotes a set.

| $I_x$ | $I_y$ | $1320P_0$ | $1320P_1$ |
|---|---|---:|---:|
| $\varnothing$ | $\varnothing$ | 6 | 6 |
| $\varnothing$ | $x$ | 6 | 6 |
| $\varnothing$ | $a$ | 5 | 10 |
| $\varnothing$ | $ab$ | 19 | 14 |
| $\varnothing$ | $ax$ | 33 | 33 |
| $\varnothing$ | $abx$ | 195 | 195 |
| $a$ | $\varnothing$ | 5 | 10 |
| $a$ | $a$ | 5 | 10 |
| $a$ | $ab$ | 19 | 14 |
| $a$ | $ax$ | 19 | 14 |
| $a$ | $abx$ | 172 | 392 |
| $ab$ | $\varnothing$ | 19 | 14 |
| $ab$ | $a$ | 19 | 14 |
| $ab$ | $ab$ | 19 | 14 |
| $ab$ | $abx$ | 779 | 574 |
| **Total** | | **1320** | **1320** |

Each row has four fair ordered suffix-mark pairs, each with one quarter of that row's probability. There are 60 marked histories per preparation. The last row alone is the selected chain: its probabilities are $779/1320,574/1320$, and each marked instance has weight $779/5280,574/5280$. The same conditional scalar attachment and ground state apply to those four instances. Every other row keeps its listed weight and has no scalar-source attachment supplied by this construction; if an attachment-availability tag is recorded, its value is “unavailable” on those rows. There is no field feedback or reweighting of the native process. Conditional calculations on the chain do not promote its probability to one or claim an all-branch dynamics. The physical clock and the spatial point in (9) are supplied attachments to the four labels.

The normalization and unit relations are explicit:
$$
 F_*^2=\frac{4A_*c^2}
 {\kappa V\omega_2\,\beta(\sqrt2+1)},\qquad
 \frac{L}{c\tau}=8,\qquad
 \frac{E_0\tau}{A_*}=\frac{3\pi}{2},\qquad
 \frac{E_2}{E_1}=\frac75,
$$
$$
 \langle T^{00}\rangle=\frac{E_0}{V}
 =\frac{3\pi A_*}{1024c^3\tau^4}. \tag{16}
$$
These are derived relations for the specified modes and action. If $\Psi$ has field units ${\cal F}$, then $F_*,B_j,q_j$ have units ${\cal F}$, $\kappa$ has units energy/(${\cal F}^2$ length), $p_j$ has units action/${\cal F}$, and $\mu$ has units energy time squared/${\cal F}^2$. Every component of $T^{\mu\nu}$ has energy-density units. The dimensionless $Q,P,\phi,\beta,\theta$, chosen wavevector integers and phases do not independently specify physical energy, action, length or time.

Given $c,\tau,A_*,\kappa$, the matching equations fix $L,B_j,F_*$ in this construction. They do not determine the numerical physical values of those inputs. Rescaling the field unit by $\Psi\mapsto s\Psi$ and $\kappa\mapsto\kappa/s^2$, $s>0$, changes $B_j,F_*$ accordingly and leaves the stress and Hamiltonian unchanged. The cancellation of $\kappa$ and the dimensionless sample normalization from (16) does not remove the independently supplied energy scale $A_*/\tau$. The unaliased frequencies and the spatial phases remain stipulated; four sampled ticks alone do not identify that unaliased spectrum or geometry.

The zero-offset convention matters. An added $CI$ in the integrated Hamiltonian would leave Heisenberg samples unchanged, but it would no longer equal the unshifted action-derived integral in (7) without changing the source convention. Normal-ordering away the ground energy would also change the requested match and the source tensor. This report makes neither change and does not claim a physically selected absolute vacuum energy. A gravitational use of any alternative offset or stress improvement would require its own explicit source prescription.

The supplied operations and standards include preparation of the Gaussian ground state, restriction to the two mode profiles, their spatial phases, a common tick and action reference, local field calibration and probe localization. A mathematical point sample is not an implemented finite-resolution detector. No joint sequential measurement protocol for the four noncommuting samples is derived. Preparation, mode control, timing, readout disturbance, work transfer and restoration costs remain unassigned. A finite positive Hamiltonian and two modes do not give an apparatus energy budget, a repeatable free cycle or an excitation's physical rest mass.

This construction directly joins the accepted sampled generator to one explicit conventional local tensor. It does not select the ultimate law, restore the excluded prefix, change a native history, infer a spatial map from order, or settle the separate retarded, coherent-inertia or Classical assignments.

The single next-use decision is to retain this as a conditional local scalar source attachment with its exact added normalization, clock, action and geometry premises. Any subsequent claim of a global gravitational observable must first supply a compatible global source/background or boundary model. No such replacement is introduced by this report.

## Scientific review

Energy derived the conditional local-sample, generator and stress attachment. Quantum Relativity independently verified its operator identities, native weights, dimensional relations and global periodic-source obstruction. Author report SHA-256 37d4a998cad850ccd508fe7a1cf1075deff4b9faec260038c84fb1194cded483; independent review 0252a3c952425bd0609e57c54454ee7fe775376912d6d890c10b1cb17f1e3728.
