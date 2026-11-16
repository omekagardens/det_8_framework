# Evolved tides under small coupling

For the same accepted Einstein–four-scalar family, the initially normal observer from $y=0$, and its parallel-transported initially Cartesian triad, the leading trace-free tidal matrix exists and is
$$
 \boxed{B=\lim_{\eta\downarrow0}\frac{\tau^2}{\eta^2}\mathcal A^{\rm TF}
 =\frac{5\pi^2p_*}{768}
 \begin{pmatrix}2&0&0\\0&-1&0\\0&0&-1\end{pmatrix},\qquad
 p_*=\frac{10\sqrt2-8}{7}>0.}                       \tag{1}
$$
All quantities in (1) are evaluated at the single observer event with proper parameter $r=1$. The same-event instantaneous-stress comparator satisfies
$$
 \boxed{B_{\rm inst}=B.}                            \tag{2}
$$
This equality is a leading small-coupling result for the fixed supplied source and registration. It is not an exact finite-coupling stress-to-tide identity or a general dynamical rule. The full inhomogeneous source and quadratic first-metric terms are retained. Their derived contributions exhibit a cancellation, rather than a failure of the comparator, in this test. The electric Weyl contribution is nonzero and supplies half of $B$; the Ricci contribution supplies the other half.

The [finite-horizon theorem](finite_horizon_for_small_coupling_scalar_torus.md), [registered-variance first variation](registered_variance_under_small_coupling.md), and [initial tidal response](initial_tidal_response_of_scalar_torus.md) provide the fixed prerequisites. The [local Einstein–four-scalar closure](local_einstein_four_scalar_development.md) supplies the same fixed-state source. The proof below derives the second metric coefficient and a cubic remainder for the whole coupled system, then evaluates curvature in the registered observer's transported frame.

## Family, frame and full reference source

Use the accepted dimensionless coordinates $(s,y)$ on $[0,5]\times\mathbb T_8^3$, the physical line element $(c\tau)^2\bar g$, and
$$
 \eta^2=\frac{GA_*}{c^5\tau^2},\qquad
 S_\chi^2=\frac{A_*}{c\tau^2},\qquad \chi_A=S_\chi\psi_A,
 \qquad \nu=\frac{\pi}{8\sqrt2}.
$$
Only $G$ varies. All references, phases, source and state conventions, mode profiles and native weights stay fixed. The equations are
$$
 \bar R_{ab}=8\pi\eta^2\sum_A\partial_a\psi_A\partial_b\psi_A,
 \qquad \Box_{\bar g}\psi_A=0.                    \tag{3}
$$
The curvature convention is the accepted
$[\nabla_a,\nabla_b]v^c=R^c{}_{dab}v^d$,
$R_{db}=R^a{}_{dab}$, with signature $(-+++)$.
The Jacobi tensor in an orthonormal observer frame is
$\mathcal A_{ij}=-c^2R_{\hat i\hat0\hat j\hat0}$.
The registered observer has proper parameter $r=\sigma/\tau$, initial point $(0,0)$ and initial velocity $e_0$; the spatial triad initially equals $(e_1,e_2,e_3)$ and is parallel transported. These are the fixed conventions for the same registered observer.

Retain
$$
 q_1=5\pi/4,\quad q_2=7\pi/4,\quad a_j^2=1/(512q_j),
$$
$$
 \alpha_1=q_1y^1+\delta_1,\quad\alpha_2=q_2y^2,\quad
 \cos\delta_1=(\sqrt2-1)\sqrt{5/7},\quad\delta_2=0.
$$
The four zero-coupling coefficient functions are
$$
 \psi_{f_j}^0=a_j\cos\alpha_j\cos(q_js),\qquad
 \psi_{g_j}^0=a_j\cos\alpha_j\sin(q_js).          \tag{4}
$$
Their initial values and first derivatives are independent of $\eta$. The metric data are exactly affine in $\eta$:
$$
 \bar g|_0=m,\quad \partial_s\bar g_{00}|_0=-6\nu\eta,
 \quad\partial_s\bar g_{ij}|_0=2\nu\eta\delta_{ij},
 \quad\partial_s\bar g_{0i}|_0=0.               \tag{5}
$$
The expanding sign and constraint compatibility in (5) are unchanged.

Define $P_j=e_je_j^{\mathsf T}$ for $j=1,2$, $d_j=a_j^2q_j^2=q_j/512$, and $C_j(y)=\cos(2\alpha_j)$. Direct contraction of both real coefficients in each pair gives the full trace-reversed reference source
$$
 M_{ab}:=\sum_A\partial_a\psi_A^0\partial_b\psi_A^0,
$$
$$
 M_{00}=\sum_jd_j\cos^2\alpha_j
       =\frac12\sum_jd_j(1+C_j),\qquad M_{0i}=0,
$$
$$
 M_{ij}=\sum_{a=1}^2d_a\sin^2\alpha_a(P_a)_{ij}
       =\frac12\sum_{a=1}^2d_a(1-C_a)(P_a)_{ij}.       \tag{6}
$$
This tensor is time independent at zero coupling, but spatially inhomogeneous. Its unshifted stress is
$$
 \bar T_{00}=\tfrac12(M_{00}+M_{kk})=3\pi/1024,
 \qquad \bar T_{0i}=0,
$$
$$
 \bar S_{ij}=M_{ij}+\tfrac12(M_{00}-M_{kk})\delta_{ij},
 \qquad \bar S^{\rm TF}=(M_{\rm spatial})^{\rm TF}.             \tag{7}
$$
No averaging or homogeneous-pressure substitution is used. Here and below spatial repeated indices use the reference Euclidean metric for coefficient calculations.

## Second metric coefficient from the reduced initial-value problem

Write
$$
 \bar g_{\rm app}=m+\eta h+\eta^2k.                          \tag{8}
$$
There is no factor $1/2$ in the definition of $k$. The accepted first variation is
$$
 h_{00}=-6\nu s,\qquad h_{ij}=2\nu s\delta_{ij},\qquad h_{0i}=0.
                                                                    \tag{9}
$$
It solves the linearized wave-map metric equation with (5), and its linearized Riemann tensor vanishes identically on the slab. This does not remove its quadratic contribution.

The reduced equation uses the flat-reference gauge vector
$\mathcal C^a=\bar g^{bc}\Gamma^a_{bc}$ and reduced Ricci
$R^{\rm red}_{ab}=R_{ab}-\nabla_{(a}\mathcal C_{b)}$.
To evaluate its quadratic coefficient at the already derived $h$, temporarily insert only $m+\eta h$. Its lapse and spatial factor obey
$N^2=1+6\nu\eta s$, $a^2=1+2\nu\eta s$.
This is a way to evaluate the quadratic tensor polynomial at $h$, not an ansatz for the evolved solution.

The connection identities in these components give
$$
 R_{00}=-3\left(\frac{a''}a-\frac{a'N'}{aN}\right),\quad
 R_{ij}=\frac{aa''+2(a')^2-aa'N'/N}{N^2}\delta_{ij},
$$
$$
 \mathcal C^0=\frac{3a'/a-N'/N}{N^2},\quad
 R_{i0j0}=(-aa''+aa'N'/N)\delta_{ij}.
$$
Taking their $\eta^2$ coefficients yields
$$
 R_{00}^{[h^2]}=12\nu^2,\quad R_{ij}^{[h^2]}=-2\nu^2\delta_{ij},
 \quad R_{i0j0}^{[h^2]}=4\nu^2\delta_{ij},
$$
$$
 (\mathcal C^0)_{[h^2]}=12\nu^2s,
 \qquad(\mathcal C_0)_{[h^2]}=-12\nu^2s.
\tag{10}
$$
Thus the quadratic **reduced** Ricci coefficient is
$$
 Q_{00}=24\nu^2,\qquad Q_{ij}=-2\nu^2\delta_{ij},\qquad Q_{0i}=0.
                                                                    \tag{11}
$$
In particular using the unreduced $12\nu^2$ in place of $24\nu^2$ would give the wrong initial-value problem.

At order $\eta^2$, the metric equation is
$-\tfrac12\Box_m k_{ab}+Q_{ab}=8\pi M_{ab}$.
The first scalar variation does not enter this source until order $\eta^3$. Since the exact data (5) are affine, $k|_0=k_s|_0=0$. Therefore
$$
 (\partial_s^2-\Delta)k_{00}=16\pi M_{00}-48\nu^2,
$$
$$
 (\partial_s^2-\Delta)k_{ij}=16\pi M_{ij}+4\nu^2\delta_{ij},
 \qquad k_{0i}=0.                                             \tag{12}
$$
Both the quadratic geometry and every part of (6) are present.

Let
$$
 \mu_j=8\pi d_j,\qquad D_j=\frac{\mu_j}{4q_j^2}=2\pi a_j^2,
 \qquad f_j(s)=1-\cos(2q_js),\qquad \sum_j\mu_j=6\nu^2.
$$
Since $-\Delta C_j=4q_j^2C_j$, the unique zero-data solution is
$$
 \boxed{k_{00}=-21\nu^2s^2+\sum_jD_jf_j(s)C_j(y),}
$$
$$
 \boxed{k_{ij}=s^2\left(2\nu^2\delta_{ij}
              +\frac12\sum_{a=1}^2\mu_a(P_a)_{ij}\right)
             -\sum_{a=1}^2D_af_a(s)C_a(y)(P_a)_{ij},\qquad k_{0i}=0.} \tag{13}
$$
Differentiation checks (12) and both initial conditions. The nonconstant terms in (13) are forced by the same original scalar source; there is no added oscillator, freely chosen mode, homogeneous future assumption or metric parameter.

A gauge check is available before using curvature. The linear contracted gauge vector of $k$ has
$$
 (\mathcal C^0)_{[k]}=\tfrac12\partial_s(k_{00}+k_{ii})=-12\nu^2s,
$$
$$
 (\mathcal C^i)_{[k]}=\partial_jk_{ij}
       -\tfrac12\partial_i(-k_{00}+k_{jj})=0.
$$
It cancels (10). Thus the metric trial has $\mathcal C=O(\eta^3)$, consistently with the exact constrained wave-map development. This is a check on (13), not a replacement for the already accepted exact constraint propagation.

## The scalar second coefficient and a cubic residual

The previously accepted $O(\eta^2)$ metric error cannot determine an $\eta^{-2}$ curvature limit. We instead construct a quadratic trial of the entire coupled system. Include the accepted first scalar variation $\phi$, with the existing spatial profile and
$$
 u_1+iv_1=e^{iqs}\left[i\nu qs^2-\nu s
                       +\frac{\nu}{2iq}(1-e^{-2iqs})\right].   \tag{14}
$$
Its Cauchy data vanish. To specify the necessary second scalar coefficient without an unsolved premise, write
$\psi_{\rm app}=\psi^0+\eta\phi+\eta^2\theta$.
Define the second inverse-metric coefficient
$$
 \ell^{00}=-k_{00}-36\nu^2s^2,\qquad
 \ell^{ij}=4\nu^2s^2\delta_{ij}-k_{ij},\qquad \ell^{0i}=0.       \tag{15}
$$
Because the contracted gauge vector vanishes through second order, the fully specified scalar equation is
$$
 (\partial_s^2-\Delta)\theta_A=F_A^{(2)},\qquad
 \theta_A|_0=\partial_s\theta_A|_0=0,
$$
$$
 F_A^{(2)}=(6\nu s\partial_s^2-2\nu s\Delta)\phi_A
                +\ell^{ab}\partial_a\partial_b\psi_A^0.      \tag{16}
$$
Every term on the right is the known smooth function (4), (13), (14) or (15). Equivalently this coefficient is explicitly defined by the flat torus wave propagator:
$$
 \boxed{\theta_A(s)=\int_0^s
 \frac{\sin((s-t)\sqrt{-\Delta})}{\sqrt{-\Delta}}
       F_A^{(2)}(t)\,dt,}                                    \tag{17}
$$
with the zero-spatial-frequency multiplier interpreted as $s-t$. This is the unique smooth zero-data solution of (16). The forcing has only finitely many Fourier components from the given trigonometric functions and their products; (17) is a finite expression by elementary mode integration. No additional field datum or quantum pair is selected. An explicit expansion of those integrals is unnecessary for the curvature coefficient, because $\theta$ does not enter (12). It is nevertheless included in the trial: omitting it would leave a quadratic scalar residual.

Let $U=(\bar g,\psi)$ and use the normalized reduced wave operator
$$
 P(U)=\partial_s^2-b^i(U)\partial_s\partial_i-a^{ij}(U)\partial_i\partial_j,
 \qquad P(U)U=\mathcal F_\eta(U,\partial U).
$$
The principal coefficients depend smoothly on the metric; all remaining terms use fields and first derivatives. The exact solution has the accepted uniform $H^7/H^6$ bound and hyperbolicity on the fixed slab. The trial
$U_{\rm app}=U^0+\eta U^1+\eta^2U^2$, with $U^2=(k,\theta)$, is uniformly smooth and matches every exact Cauchy datum. Equations (12), (16), and the lower-order equations cancel its residual through order two. Smooth coefficient Taylor expansion on the trial, not a parameter expansion of an unknown solution map, therefore gives
$$
 Q_\eta=P(U_{\rm app})U_{\rm app}
              -\mathcal F_\eta(U_{\rm app},\partial U_{\rm app}),
 \qquad \sup_{s\le5}\|Q_\eta\|_{H^4}\le C\eta^3.              \tag{18}
$$

For $w=U^\eta-U_{\rm app}$, exact subtraction gives
$$
 \begin{aligned}
 P(U^\eta)w={}&\mathcal F_\eta(U^\eta,\partial U^\eta)
                -\mathcal F_\eta(U_{\rm app},\partial U_{\rm app})\\
 &+[P(U_{\rm app})-P(U^\eta)]U_{\rm app}-Q_\eta.
 \end{aligned}                                               \tag{19}
$$
Coefficient differences multiply derivatives of the known smooth trial. The nonresidual right side has $H^4$ norm at most
$C(\|w\|_{H^5}+\|w_s\|_{H^4})$, by the three-dimensional Sobolev algebra and smooth-composition estimates on bounded sets. Normalizing the time coefficient before commuting four spatial derivatives avoids a commutator with uncontrolled $w_{ss}$. The accepted exact $H^7/H^6$ bound controls all coefficient and wave-energy commutators; they require at most five spatial derivatives of $w$ and four of $w_s$. Include the zero field norm in the positive energy to control the torus constant mode. Periodicity supplies no boundary term.

The same energy estimate underlying the independently accepted [variance remainder](registered_variance_under_small_coupling.md), now with residual (18), gives zero-initial-error Gronwall control:
$$
 \boxed{\sup_{s\le5}\left(\|w\|_{H^5}+\|w_s\|_{H^4}\right)
 \le C\eta^3,\qquad
 \sup_{s\le5}\|w_{ss}\|_{H^3}\le C\eta^3.}                    \tag{20}
$$
The second bound follows from the normalized equation. Spatial Sobolev embedding controls every spacetime derivative of $w$ through order two uniformly. Consequently
$$
 \operatorname{Riem}(\bar g^\eta)
       =\eta^2\mathscr R^{(2)}+O(\eta^3)\quad\hbox{in }C^0,
$$
$$
 \mathscr R^{(2)}=D\operatorname{Riem}_m[k]
              +\tfrac12D^2\operatorname{Riem}_m[h,h].         \tag{21}
$$
The omitted linear coefficient is identically zero by (9). This proves the needed curvature limit without assuming differentiability of the highest-norm solution map. Constants and a sufficiently small positive parameter neighborhood remain existential. No third-order coefficient or additional observable is calculated; the cubic bound serves only this curvature limit.

## Electric curvature and its cancellation

For the accepted Riemann convention, (10), (13) give
$$
 E_{ij}^{(2)}:=\mathscr R^{(2)}_{i0j0}
       =4\nu^2\delta_{ij}
          -\frac12\left(\partial_s^2k_{ij}
                          +\partial_i\partial_jk_{00}\right), \tag{22}
$$
since $k_{0i}=0$. Keeping both terms is essential. From (13), in matrix notation,
$$
 \partial_s^2k_{\rm spatial}
 =4\nu^2I+\sum_{a=1}^2\mu_a[1-\cos(2q_as)C_a]P_a,
$$
$$
 \operatorname{Hess}_y k_{00}
 =-\sum_{a=1}^2\mu_a[1-\cos(2q_as)]C_aP_a.
\tag{23}
$$
Thus the time-dependent factors cancel in their sum. Equations (6), (22) reduce to
$$
 \boxed{E^{(2)}=2\nu^2I-8\pi M_{\rm spatial},\qquad
       (E^{(2)})^{\rm TF}=-8\pi(M_{\rm spatial})^{\rm TF}.}     \tag{24}
$$
This cancellation was derived from the zero-data forced wave solution; it was not imposed through an instantaneous-Weyl assumption. The spatially varying terms in (13) are required to obtain it. As an initial-data consistency check, (24) agrees with the accepted initial-tide coefficient at $s=0$.

## Registered event and parallel triad

The accepted observer expansion, and the parallel-transport equation with (9), give on the needed segment
$$
 z_\eta(r)=(r-3\nu\eta r^2/2,0)+O(\eta^2),
$$
$$
 \bar e_{\hat0}=(1-3\nu\eta r)e_0+O(\eta^2),\qquad
 \bar e_{\hat i}=(1-\nu\eta r)e_i+O(\eta^2).                  \tag{25}
$$
For the spatial frame, this follows from
$(\Gamma^j_{0i})_1=\nu\delta^j_i$ and
$(\Gamma^0_{0i})_1=0$, with exactly Cartesian initial frame. The zeroth leg is the geodesic velocity. The dimensionless legs are orthonormal for $\bar g$; their physical unit legs carry the common $(c\tau)^{-1}$ factor.

More generally only their $O(\eta)$ closeness is needed. Because the first curvature coefficient vanishes identically, the event shift and all four frame contractions change the $\eta^2$ curvature term only by $O(\eta^3)$. The smoothness of $\mathscr R^{(2)}$ and (20) control this statement at the actual registered event, not just a coordinate-time point. Vanishing of the first curvature merely at that point would not have sufficed.

A physical orthonormal Riemann component is $(c\tau)^{-2}$ times its dimensionless counterpart. Hence
$$
 \tau^2\mathcal A^{\rm TF}
 =-\eta^2(E^{(2)}(1,0))^{\rm TF}+O(\eta^3),\qquad
 B=8\pi(M_{\rm spatial}(0))^{\rm TF}.                         \tag{26}
$$
The trace-free operation is in the transported orthonormal frame; replacing it by the zeroth-order frame in the coefficient is justified by the same order estimate.

At the fixed point $y=0$, $\sin^2\alpha_2=0$, $\sin^2\alpha_1=p_*$, and $d_1=5\pi/2048$. Therefore
$$
 M_{\rm spatial}(0)=d_1p_*P_1,\qquad
 8\pi d_1p_*\left(P_1-\tfrac13I\right)
 =\frac{5\pi^2p_*}{768}\operatorname{diag}(2,-1,-1).
$$
This proves (1), including its symmetry, vanishing trace and nonzero value, without a numerical calculation.

## Same-event comparator and evolved Weyl role

Physical source-frame stresses are $S_\chi^2/(c\tau)^2$ times their dimensionless counterparts. Scalar, observer and frame convergence gives at the same event
$\bar S_{\hat i\hat j}^{\rm TF}=(M_{\rm spatial}(0))^{\rm TF}+O(\eta)$.
Using $GS_\chi^2/c^4=\eta^2$, the same-event comparator is
$$
 \begin{aligned}
 B_{\rm inst}
 &=\lim_{\eta\downarrow0}\frac{\tau^2}{\eta^2}
               \frac{8\pi G}{c^2}S_{\hat i\hat j}^{\rm TF}\\
 &=8\pi(M_{\rm spatial}(0))^{\rm TF}=B.
 \end{aligned}                                               \tag{27}
$$
Thus the initial formula survives this one evolved leading-coefficient test. Equality of the limits does not establish equality at finite $\eta$, another preparation, another observer or another event. No numerical threshold for a physical coupling follows.

To determine Weyl rather than assume it, use the same Ricci/Weyl decomposition as in the accepted [initial tidal response](initial_tidal_response_of_scalar_torus.md):
$$
 (E^R)^{\rm TF}=E^W-\tfrac12(R_{ij})^{\rm TF}.
$$
Equation (3) fixes $(R_{ij}^{(2)})^{\rm TF}=8\pi(M_{\rm spatial})^{\rm TF}$. Combining this with the independently derived (24) yields
$$
 \boxed{(E^W)^{(2)}=-4\pi(M_{\rm spatial})^{\rm TF}.}           \tag{28}
$$
At the registered event it is nonzero. Its normalized acceleration contribution is $- (E^W)^{(2)}=B/2$; the Ricci part supplies the other half. The metric evolution therefore supports the same split at this leading coefficient. Weyl has neither been discarded nor inferred from the comparator before computing curvature.

## Assumptions and limits

This is a direct first-nonzero curvature response, distinct from the accepted expansion-driven variance effect whose first-order curvature is zero. It remains a result of the supplied Einstein–four-scalar model, accepted expanding-torus data, fixed two-pair Gaussian source and external reference scales. The fixed proper-time registration is mathematical, not an implemented clock or detector. Native law selection, source preparation, finite-resolution readout, reset, complete work accounting, physical normalization and empirical correspondence remain unsupplied.

The structural weights $779/1320,574/1320$, four fair suffix marks at a quarter of each branch weight, and unavailable attachment on other histories remain unchanged. There is no source retuning, energy offset, covariance reselection, extra quantum mode, homogeneous-metric replacement or extension of the accepted horizon. The scalar second coefficient in (16) is determined by the same fields and exists only to control the authorized curvature expansion; no further variance coefficient or sample is studied.

The accepted result is (1)–(2): a nonzero leading evolved trace-free tide, equal to the same-event instantaneous-stress comparator in this specified test. The conclusion is confined to that matrix and comparison; it supplies no broader stress-to-tide rule.

## Reviewed basis and source scope

DET Quantum Relativity supplied the analytic derivation. DET Relational State Research independently checked the full source contraction, quadratic reduced metric and gauge cancellation, scalar second coefficient, cubic residual and curvature control, observer and transported-frame conversion, endpoint matrix, comparator, and Weyl/Ricci split. The independent scientific verdict was PASS, with no correction required; the result was accepted within the stated conditional one-event scope. Author-side checks were not counted as that independent review.

The first-variation prerequisite was authored by DET Quantum Relativity and independently reviewed by DET Energy Research. The finite-horizon prerequisite was authored by DET Energy Research and separately reviewed by DET Relational State Research. The initial-tide prerequisite was authored by DET Quantum Relativity and independently reviewed by DET Energy Research. These accepted results are reused at their stated scope. The quadratic identities, forced metric solution, scalar second forcing and cubic residual calculation are the derivation above; no additional primary theorem is invoked.

The curvature conventions are inherited through the [initial-tide proof](initial_tidal_response_of_scalar_torus.md) from [Gourgoulhon, arXiv gr-qc/0703035v1](https://arxiv.org/pdf/gr-qc/0703035v1). The recorded independent initial-tide review inspected printed pp. 18–19, equations (2.13), (2.17) and (2.18), p. 35, equations (2.92)–(2.93), and p. 51, equation (4.2), for the curvature commutator, Ricci contraction, Weyl decomposition, Lorentzian Gauss relation and trace-reversed Einstein equation. The existing [finite-horizon](finite_horizon_for_small_coupling_scalar_torus.md) and [variance](registered_variance_under_small_coupling.md) articles record the precise versions and bounded inspection scopes of the imported hyperbolic Cauchy framework and Sobolev estimates. The evolved-tide derivation and its independent review reuse those accepted sources and conventions; they require no new external theorem or source snapshot. This article preserves those recorded inspections and does not claim a new literature read.
