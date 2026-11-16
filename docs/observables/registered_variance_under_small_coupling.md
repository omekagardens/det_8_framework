# Registered variance under small coupling

For the unchanged accepted Einstein–four-scalar family, the initially normal observer launched at the registered point has
$$
 \boxed{V_\eta=V_0+\eta V_1+O(\eta^2),\qquad
 V_0=\frac{4-2\sqrt2}{896\pi},}
$$
$$
 \boxed{V_1=\frac1{7168\sqrt2}
 \left[(3-2\sqrt2)\left(-2+\frac4{5\pi}\right)
       -2-\frac4{7\pi}\right]<0.}                 \tag{1}
$$
Here $V_\eta=\sum_A\psi_A^\eta(z_\eta(1))^2$; the event is at one proper reference duration $\tau$. The derivative is the right derivative at $\eta=0$. The error constant and admissible positive coupling neighborhood are existential. No second-order coefficient is computed. The quadratic remainder establishes this first variation; it does not open a higher-order investigation.

This is conditional dynamical observable information in the already supplied model. The first-order effect is due to its constraint-compatible initial expansion, proportional to $\eta$, while the explicit Einstein matter multiplier is proportional to $\eta^2$. It is not a newly derived gravitational law, a calibrated prediction, a native-law selection, or evidence of a physical implementation.

The [finite-horizon theorem](finite_horizon_for_small_coupling_scalar_torus.md) supplies the common smooth development and registered observer used here. Its prerequisites are the [local Einstein–four-scalar closure](local_einstein_four_scalar_development.md), the [expanding-torus initial data](expanding_torus_initial_data_for_scalar_source.md), and the [local scalar source](local_scalar_source_for_four_chain_field.md). The first-variation argument below adds the controlled parameter remainder needed to compute the variance at this one event.

## Unchanged data and the observable

Use the finite-horizon theorem's dimensionless coordinates $z=(s,y)$ on $[0,5]\times\mathbb T_8^3$, $s=t/\tau$, $y=x/(c\tau)$. The physical line element is $(c\tau)^2\bar g_{ab}dz^adz^b$. Define the abbreviation $\nu=\pi/(8\sqrt2)>0$. The parameter, field normalization and equations remain
$$
 \eta^2=\frac{GA_*}{c^5\tau^2},\quad
 G=\frac{c^5\tau^2}{A_*}\eta^2,\quad
 S_\chi^2=\frac{A_*}{c\tau^2},\quad
 \chi_A=S_\chi\psi_A,
$$
$$
 \bar R_{ab}=8\pi\eta^2\sum_A\partial_a\psi_A\partial_b\psi_A,
 \qquad \Box_{\bar g}\psi_A=0.                  \tag{2}
$$
Only $G$ varies; $c,\tau,A_*,\kappa$, the source convention, two oscillator pairs, fixed Gaussian functional, phases and native weights remain fixed. The metric initial data in the common flat-reference wave-map gauge are
$$
 \bar g|_0=m=\operatorname{diag}(-1,1,1,1),\quad
 \partial_s\bar g_{00}|_0=-6\nu\eta,\quad
 \partial_s\bar g_{ij}|_0=2\nu\eta\delta_{ij},\quad
 \partial_s\bar g_{0i}|_0=0.                    \tag{3}
$$
These are the accepted expanding-sign data, $\beta=-\nu\eta$, not a new choice of expansion. They satisfy the exact constraints in the accepted family.

Retain
$$
 q_1=5\pi/4,\quad q_2=7\pi/4,\quad
 a_j^2=\frac1{512q_j},\quad
 \alpha_1=q_1y^1+\delta_1,\quad\alpha_2=q_2y^2,
$$
$$
 \cos\delta_1=(\sqrt2-1)\sqrt{5/7},\qquad\delta_2=0.
$$
Here $a_j$ denotes the finite-horizon theorem's dimensionless scalar amplitude, not the similarly named canonical sample amplitudes in the earlier scalar-source document. For each pair,
$$
 (\psi_{f_j},\partial_s\psi_{f_j})|_0
       =(a_j\cos\alpha_j,0),\qquad
 (\psi_{g_j},\partial_s\psi_{g_j})|_0
       =(0,a_jq_j\cos\alpha_j).               \tag{4}
$$
At zero coupling,
$$
 \psi_{f_j}^0=a_j\cos\alpha_j\cos(q_js),\qquad
 \psi_{g_j}^0=a_j\cos\alpha_j\sin(q_js),\qquad \bar g^0=m. \tag{5}
$$
The observer is the same geodesic as in the accepted theorem, with proper parameter $r=\sigma/\tau$, initial point $(0,0)$, initial velocity $e_0$, and $\bar g(\dot z,\dot z)=-1$. Its parameter value $r=1$ is the sole sample investigated here.

## Metric variation from the reduced Cauchy problem

First construct a linearized solution; the controlled remainder below then proves that it is the actual parameter variation. Write $\bar g_{\rm app}=m+\eta h$. In the accepted reduced Einstein equations, the first-derivative metric terms are quadratic about $m$, and the matter source has an explicit factor $\eta^2$. Thus the first-order reduced metric equation is
$$
 \Box_m h_{ab}=0.
$$
Its zero initial value and spatially constant velocity from (3) uniquely give
$$
 \boxed{h_{00}=-6\nu s,\qquad h_{ij}=2\nu s\delta_{ij},\qquad h_{0i}=0.} \tag{6}
$$
The linearized contracted Christoffels vanish. In particular
$\delta\Gamma^0=\tfrac12\partial_sh_{00}
 +\tfrac12\sum_i\partial_sh_{ii}=0$, and $\delta\Gamma^i=0$.
The inverse components are therefore
$$
 \bar g^{00}_{\rm app}=-1+6\nu\eta s+O(\eta^2),\quad
 \bar g^{ij}_{\rm app}=(1-2\nu\eta s)\delta^{ij}+O(\eta^2).
$$
Equation (6) is the unique solution of the linearized initial-value problem. A homogeneous metric was not substituted for the nonlinear evolution. The full inhomogeneous scalar stress remains in (2); it simply has no first-order source contribution at this endpoint.

## Scalar variation from the same wave equation

Write $\psi_{\rm app}=\psi^0+\eta\phi$. Vanishing linearized contracted Christoffels yields
$$
 (-\partial_s^2+\Delta)\phi
 +(6\nu s\partial_s^2-2\nu s\Delta)\psi^0=0,
 \qquad \phi|_0=\partial_s\phi|_0=0.          \tag{7}
$$
All fields remain spacetime functions in this derivation. Only the linearized problem has translation-invariant coefficients, so uniqueness and its forcing imply the original spatial profile for each first variation. This is not an assumption that the exact nonlinear fields retain separated profiles.

For one frequency $q$, let $u=\cos(qs),v=\sin(qs)$ and let $u_1,v_1$ be the corresponding first-order time amplitudes. Equation (7) becomes
$$
 u_1''+q^2u_1=-4\nu q^2s\cos(qs),\qquad
 v_1''+q^2v_1=-4\nu q^2s\sin(qs),             \tag{8}
$$
with zero values and derivatives initially. One explicit smooth solution, with complex notation used only to package the same two real functions, is
$$
 u_1+iv_1=e^{iqs}\left[
 i\nu q s^2-\nu s+\frac{\nu}{2iq}(1-e^{-2iqs})\right]. \tag{9}
$$
Differentiating (9) verifies (8) and both initial conditions. No complex field, new quantum amplitude or extra mode has been added.

For the quadratic sum, real Duhamel integration also gives directly
$$
 \begin{aligned}
 2(uu_1+vv_1)
 &=-4\nu q\int_0^s t\sin\bigl(2q(s-t)\bigr)\,dt\\
 &=\nu\left[-2s+\frac{\sin(2qs)}q\right].
 \end{aligned}                                                   \tag{10}
$$
This independent expression checks the sign and factor in (9).

## A controlled remainder, beyond continuous dependence

The accepted theorem provides exact solutions on the fixed slab with a common bound in $H^7\times H^6$, uniform spacelike hyperbolicity and smooth persistence. It asserts continuity, not differentiability of the solution map in that highest norm. We do not strengthen it by assertion. The primary article itself distinguishes highest-norm continuity from stronger regularity; its Theorem III and subsequent regularity remark give the local framework. Its Sobolev composition/product estimates and coefficient estimates supply the standard tools for the following lower-norm calculation. [Hughes, Kato and Marsden, 1977, pp. 274, 281–287](https://www.cds.caltech.edu/~marsden/bib/1977/02-HuKaMa1977/HuKaMa1977.pdf). The finite-slab existence result is reused, not reproved or extended. The source version and bounded inspection scopes are recorded below.

Here is the remainder proof for this specific smooth parameter curve. Let $U=(\bar g,\psi)$ comprise the fourteen reduced unknowns. Normalize each equation by its nonzero time coefficient, writing
$$
 P(U)U=F_\eta(U,\partial U),\qquad
 P(U)=\partial_s^2-b^i(U)\partial_s\partial_i
                     -a^{ij}(U)\partial_i\partial_j.             \tag{11}
$$
The principal coefficients depend smoothly on the metric, not its derivatives. All remaining terms are smooth functions of fields, first derivatives and $\eta$; in particular the prescribed gravitational multiplier remains $\eta^2$. The actual solutions have vanishing gauge vector. For a trial field, retain the full scalar wave expression, including its contracted-Christoffel term. Its linearization vanishes by (6), so (7) is still the correct linearized system.

The explicit trial $U_{\rm app}=U^0+\eta U^1$, where $U^1=(h,\phi)$ is (6)–(9), is uniformly smooth on the fixed slab. It exactly matches every Cauchy datum (3)–(4), since those data are affine in $\eta$. Its normalized residual is
$$
 Q_\eta=P(U_{\rm app})U_{\rm app}
            -F_\eta(U_{\rm app},\partial U_{\rm app}),\qquad
 \sup_{0\le s\le5}\|Q_\eta\|_{H^4}\le C\eta^2.                  \tag{12}
$$
This follows from Taylor expansion of smooth coefficient functions on a compact hyperbolic neighborhood: the constant residual vanishes by (5), the linear residual vanishes by (6)–(8), and the trial has uniformly bounded derivatives of every required order. It does not use a Taylor expansion of the unknown exact solution.

Set $w=U^\eta-U_{\rm app}$. Exact subtraction gives
$$
 \begin{aligned}
 P(U^\eta)w={}&F_\eta(U^\eta,\partial U^\eta)
             -F_\eta(U_{\rm app},\partial U_{\rm app})\\
 &+[P(U_{\rm app})-P(U^\eta)]U_{\rm app}-Q_\eta.               \tag{13}
 \end{aligned}
$$
The first two terms on the right, before the residual, obey the bound
$$
 \|\text{those terms}\|_{H^4}
 \le C\bigl(\|w\|_{H^5}+\|\partial_sw\|_{H^4}\bigr).          \tag{14}
$$
Indeed $H^4(\mathbb T_8^3)$ is a multiplication algebra. Smooth composition is Lipschitz on the bounded field/first-derivative ranges supplied by the uniform $H^7/H^6$ bound. Coefficient differences in the principal term multiply second derivatives of the known smooth trial, not second derivatives of $w$. The constants are independent of sufficiently small $\eta$.

Commute (13) through at most four spatial derivatives and use the positive wave energy, including the zeroth field norm to control the torus constant mode. Normalizing in (11) first avoids a commutator containing uncontrolled $\partial_s^2w$. Equivalently use the first-order wave system for $(w,\partial_sw,\partial_iw)$. The uniform exact coefficient bounds control its commutators; at most five spatial derivatives of $w$ and four of $\partial_sw$ are needed. Periodicity gives no boundary flux. With $\mathcal E$ a norm equivalent uniformly to $\|w\|_{H^5}+\|\partial_sw\|_{H^4}$, the energy estimate and (14) give
$$
 \mathcal E(s)\le C\mathcal E(0)+C\int_0^s
       [\mathcal E(t)+\|Q_\eta(t)\|_{H^4}]\,dt.
$$
Here $\mathcal E(0)=0$. Gronwall and (12) prove
$$
 \boxed{\sup_{s\le5}
 (\|U^\eta-U^0-\eta U^1\|_{H^5}
 +\|\partial_s(U^\eta-U^0-\eta U^1)\|_{H^4})\le C\eta^2.}     \tag{15}
$$
The normalized equation also gives
$\sup_{s\le5}\|\partial_s^2w\|_{H^3}\le C\eta^2$.
Thus the right first variation is justified in
$C([0,5];H^5)\cap C^1([0,5];H^4)$, with the stated second-time-derivative bound. No differentiability of the general $H^7/H^6$ solution map is presumed. The trial need not satisfy the nonlinear constraints exactly: it is an approximation to the accepted reduced development, whose exact constraints and gauge propagation are already proved. Its quadratic residual accounts for that distinction.

## Observer registration and gauge separation

Sobolev embedding applied to (15) and its time-derivative bounds supplies a uniform $O(\eta^2)$ remainder for the metric and its connection, with enough derivative control for the geodesic equation. The connection expansion has
$$
 (\Gamma^0_{00})_1=3\nu,\qquad(\Gamma^i_{00})_1=0.
$$
For $z_\eta=z_0+\eta\zeta+O(\eta^2)$, $z_0(r)=(r,0)$, its linearized equation and unchanged initial point and normal give
$$
 \zeta(0)=\dot\zeta(0)=0,\quad
 \ddot\zeta^0=-3\nu,\quad\ddot\zeta^i=0,
$$
$$
 \boxed{\zeta(r)=(-3\nu r^2/2,0),\qquad
 \|z_\eta-z_0-\eta\zeta\|_{C^1([0,1])}\le C\eta^2.}         \tag{16}
$$
For the remainder, insert this smooth approximate trajectory in the exact geodesic equation. The connection expansion gives an $O(\eta^2)$ residual, the initial data agree exactly, and bounded connection derivatives on the already buffered slab give the bound by ODE Gronwall. No normal-coordinate chart or continued normality of the exact observer is assumed. The first-order absence of spatial displacement follows from its equation; it is not an imposed fixed-coordinate detector.

At any parameter value needed in deriving the endpoint,
$$
 \psi_A^\eta(z_\eta(r))
 =\psi_A^0(r,0)+\eta[\phi_A(r,0)+\zeta^0(r)\partial_s\psi_A^0(r,0)]
   +O(\eta^2).                                                \tag{17}
$$
The observer/time-registration contribution to the summed quadratic is
$$
 \zeta^0\partial_s\sum_A(\psi_A^0)^2=0,                      \tag{18}
$$
because each zero-coupling sine/cosine pair has a time-independent squared sum. Individual component corrections do not vanish. In complex notation the registered first correction is (9) with $i\nu q r^2$ replaced by $-i\nu q r^2/2$; its real amplitude correction is unchanged. This explicitly separates the time-coordinate phase shift from the amplitude effect.

All second derivatives of (6) vanish, so its linearized curvature is zero. This does not make the registered scalar result a pure coordinate effect. The fixed family has a changing initial extrinsic curvature and identified scalar data. Removing a local metric perturbation also transforms those data and the observer. A spatial dilation is not a globally periodic diffeomorphism of the fixed torus. More generally, under an infinitesimal coordinate change the variations of $\phi_A$ and $\zeta^a\partial_a\psi_A^0$ cancel in their sum in (17), when the same initial-data and observer identification is retained. The lapse contribution has been explicitly accounted for; it cannot cancel (10).

## Endpoint, sign and existing quantum variance

Combining (10), (17) and (18) at the sole registered endpoint $r=1$ gives
$$
 V_1=\nu\sum_{j=1}^2a_j^2\cos^2\delta_j
       \left[-2+\frac{\sin(2q_j)}{q_j}\right].                \tag{19}
$$
The exact stipulated numbers are
$$
 a_1^2\cos^2\delta_1=\frac{3-2\sqrt2}{896\pi},\qquad
 a_2^2\cos^2\delta_2=\frac1{896\pi},\quad
 \sin(2q_1)=1,\quad\sin(2q_2)=-1.
$$
They give (1). Both weights are positive, $-2+4/(5\pi)<0$, and $-2-4/(7\pi)<0$; hence the coefficient is strictly negative without numerical evolution or a parameter scan. The quadratic remainder and strict sign imply $V_\eta<V_0$ for all sufficiently small positive $\eta$, without an evaluated threshold. This is a derivative in $\eta$, the specified square-root coupling parameter, not a finite derivative in $G$ at zero.

The accepted [four-scalar closure](local_einstein_four_scalar_development.md) uses the same centered Gaussian functional and fixed canonical operators $R_A=(Q_1,P_1,Q_2,P_2)$, with symmetric covariance $\delta_{AB}/2$. Since
$\Psi=\sum_AR_AF_A$, $F_A=\sqrt{2/\kappa}\,S_\chi\psi_A$,
$$
 \omega(\Psi)=0,\qquad
 \boxed{\operatorname{Var}_\omega\Psi(z_\eta(1))
  =\frac12\sum_AF_A(z_\eta(1))^2
  =\frac{S_\chi^2}{\kappa}V_\eta.}                            \tag{20}
$$
The prefactor is fixed and positive. Thus (1) is precisely a first-order decrease of the existing finite-model Gaussian field variance at that registered event. It adds no operator, state-selection or general-QFT assumption. At $\eta=0$, (20) is the old flat equal-time variance $\tfrac12\sum_jB_j^2\cos^2\delta_j$. At positive coupling the inherited stationary sample identity is not preserved to first order at this endpoint. No claim about other samples or unequal-time covariances is made.

## Scope of the result

The dependencies remain the supplied Einstein coupling, four wave equations, accepted constrained data and source normalization, fixed Gaussian functional, mathematical normal-launch observer and external $c,\tau,A_*,\kappa$ references. The accepted existence neighborhood may be shrunk to ensure the common estimates; neither its threshold nor error constant is evaluated. This does not certify any particular physical value of $G$.

The supported native chain retains probabilities $779/1320,574/1320$, each with four fair suffix marks of one quarter its branch weight. Other histories keep their weights and lack this attachment. No native reweighting, mass calibration, physical preparation, apparatus clock realization, finite-resolution readout, reset or complete work-store boundary is supplied. The existing Gaussian is not reselected as an instantaneous ground state. The two-pair field remains a finite-rank construction, not full continuum QFT.

## Reviewed basis and primary-source scope

DET Quantum Relativity supplied the analytic derivation. DET Energy Research independently reviewed the linearized metric and scalar initial-value problems, the lower-norm residual and derivative accounting, proper-time registration, exact endpoint coefficient, and fixed-Gaussian covariance contraction. The independent scientific verdict was PASS, with no correction required, and the result was accepted within the conditional first-variation scope stated here. Author-side checks were not counted as that independent review. The finite-horizon prerequisite was authored by DET Energy Research and separately reviewed by DET Relational State Research; that accepted prerequisite supplies the smooth common slab and exact constraint propagation.

The primary source is Hughes, Kato and Marsden, *Well-posed quasi-linear second-order hyperbolic systems with applications to nonlinear elastodynamics and general relativity*, the 1977 original article in *Archive for Rational Mechanics and Analysis* 63, 273–294, [author-hosted original PDF](https://www.cds.caltech.edu/~marsden/bib/1977/02-HuKaMa1977/HuKaMa1977.pdf). The first-variation author's inspection covered printed p. 274 for the highest-norm continuity distinction, pp. 281–282 for Theorem III, its hypotheses and persistence, and pp. 282–287 for product/composition, coefficient and energy estimates. The distinct scientific reviewer inspected p. 274, p. 282 for the local theorem, persistence and product estimates, and pp. 283–284 for smooth composition and positive energy structure. The specific residual and parameter-variation proof is the derivation above, not a theorem attributed to that paper.

The compact-manifold framework is reused through the accepted [finite-horizon theorem](finite_horizon_for_small_coupling_scalar_torus.md), whose corroborating source is Gasperín and Valiente Kroon, *Spinorial Wave Equations and Stability of the Milne Spacetime*, [arXiv:1407.3317v1](https://arxiv.org/pdf/1407.3317v1). The inherited inspection covers the title/version page, Appendix E, printed pp. 34–35, equation (68) and Theorem 2, and reference 15 on p. 36. The exact v1 source bears the July 11, 2014 arXiv version stamp and a June 18, 2021 printed title-page date. Its literal open-to-closed endpoint assertion (iii) and ambiguous final time endpoint in (iv) are not used. No Milne, conformal or global-stability conclusion is imported, and no new theorem from this source is invoked for the first variation.

This article preserves the accepted proof and recorded source inspections. Its conclusion is the single nonzero right first variation (1), with the controlled quadratic remainder; it supplies no second-order coefficient, additional endpoint or broader gravity claim.
