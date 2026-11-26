# Scalar curvature from seven prepared timelike volumes

This conditional geometric result recovers scalar curvature from seven prepared geodesic-volume channels and bounds the error of a finite-duration estimate. Smooth Lorentzian geometry, full initial relative rest, calibrated proper length, the prescribed velocities, positive volumes and independent third-derivative bounds are supplied assumptions. No Einstein equation is required.

\[
\boxed{\left|S_d-R_g(p)\right|
\le \frac d3\left[\frac12\sum_{i=1}^3(M_{i+}+M_{i-})+7M_0\right].}       \tag{1}
\]

The finite record determines an interval for the scalar, not its exact value. The exact identity uses ideal derivatives at preparation.

## 1. Supplied geometry and channel assumptions

Let \(g\) be a supplied smooth Lorentzian metric of signature \((-+++)\) on the needed neighborhood of \(p\). Use its Levi-Civita connection and
\[
R^\rho{}_{\sigma\mu\nu}
=\partial_\mu\Gamma^\rho_{\nu\sigma}
-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma},
\quad \operatorname{Ric}_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}.         \tag{3}
\]
Thus \((\nabla_X\nabla_Y-\nabla_Y\nabla_X-\nabla_{[X,Y]})Z=R(X,Y)Z\).

Provide an orthonormal tetrad \(e_0,e_1,e_2,e_3\) at \(p\), \(e_0\) future-directed. The seven fixed velocities are
\[
U_0=e_0,\qquad U_{i\pm}=\sqrt2\,e_0\pm e_i,\quad i=1,2,3.            \tag{4}
\]
For the six moving channels, \(g(U,U)=-2+1=-1\) and \(g(U,e_0)=-\sqrt2<0\); all seven are future unit timelike. The parameter \(s=c\tau_{\rm proper}\) has length units. No new Fock boost representation is asserted.

Assume all seven central geodesics, their prepared Jacobi fields and normalized positive volumes are defined on the same supplied interval \([0,d]\), \(d>0\). Supply finite bounds \(M_U\ge\sup_{[0,d]}|v_U'''|\). Smoothness gives local existence and local bounded derivatives; it does not certify an arbitrary prescribed duration from endpoint readings. The interval, positivity and bounds remain explicit premises. No Einstein equation is used for the kinematic identity or bound.

## 2. Realization of full initial relative rest

Fix one of the seven \(U\). Let \(E_1,E_2,E_3\) be any orthonormal basis of \(U^\perp\) at \(p\). Put
\[
p(y)=\exp_p\!\left(\sum_i y^iE_i\right)
\]
for small \(y\). Parallel transport \(U\) along the radial geodesic from \(p\) to \(p(y)\), obtaining a smooth future unit field \(V(y)\). At \(y=0\),
\[
\partial_i p=E_i,\qquad V(0)=U,\qquad \nabla_{\partial_i p}V(0)=0.    \tag{5}
\]
The last identity follows by differentiating along each radial axis, on which \(V\) was defined by parallel transport.

Now vary the unit geodesic initial data:
\[
F(s,y)=\exp_{p(y)}(sV(y)),\qquad
\gamma(s)=F(s,0),\qquad J_i(s)=\partial_iF(s,0).                    \tag{6}
\]
Smooth geodesic ODE dependence supplies this variation locally. If the central solution extends smoothly over the stated compact interval, nearby initial data extend over that interval after restricting \(y\); the volume positivity premise supplies the required nondegeneracy along the central channel. This is a local geodesic variation, not a global spacetime foliation.

Coordinate derivatives of \(F\) commute. Torsion-freeness therefore gives
\[
J_i(0)=E_i,\qquad D_sJ_i(0)=\nabla_{\partial_i p}V(0)=0,
\qquad D_s^2J_i=R(U,J_i)U.                                        \tag{7}
\]
Here \(U(s)=\dot\gamma(s)\), parallel along \(\gamma\). Equation (7)'s sign follows directly from
\(\nabla_U\nabla_JU=\nabla_J\nabla_UU+R(U,J)U\) and \(\nabla_UU=0\).

Every varied geodesic in (6) is unit timelike. Differentiating its normalization in \(y^i\) yields \(g(U,D_sJ_i)=0\). Consequently \(d_s g(U,J_i)=0\), and its zero initial value gives
\[
g(U,J_i(s))=0.                                                    \tag{8}
\]
Thus the Jacobi triad remains spatial along the central observer.

This realizes the stipulated full covariant initial-rest condition. In arbitrary coordinates it is
\[
\dot J_i^\mu(0)=-\Gamma^\mu_{\alpha\beta}(p)U^\alpha E_i^\beta,       \tag{9}
\]
not a coordinate-zero-derivative prescription and not merely \(v_U'(0)=0\). The construction is repeated for the fixed seven channels only. Smooth local existence provides some common short interval because there are finitely many channels; the supplied actual \(d\) must still satisfy the registered existence/positivity premises.

## 3. The spatial volume and its initial acceleration

Parallel transport the \(E_a\) along \(\gamma\), and write \(J_i=A^a{}_iE_a\). From (7),
\[
A(0)=I_3,\qquad A'(0)=0,\qquad
A''{}^a{}_i(0)=g(E_a,R(U,E_i)U).                                  \tag{10}
\]
The normalized Gram volume is
\[
v_U(s)=\sqrt{\det[g(J_i,J_j)]}
      =\sqrt{\det(A^{\mathsf T}A)}=|\det A(s)|.                     \tag{11}
\]
Because \(A(0)=I\) and the volume is positive throughout \([0,d]\), the determinant has positive sign there. Hence \(v_U=\det A\), with \(v_U(0)=1\) and \(v_U'(0)=0\).

For clarity about the spatial idealization, on a sufficiently small spacelike slice \(y\mapsto F(s,y)\), let \(H_{ij}(s,y)\) be its induced metric. For the coordinate cube \(C_\epsilon=[-\epsilon/2,\epsilon/2]^3\), the geometric three-volume satisfies
\[
\epsilon^{-3}\int_{C_\epsilon}\sqrt{\det H(s,y)}\,d^3y
\longrightarrow \sqrt{\det H(s,0)}=v_U(s).
\]
The corresponding ratio to the initial cube's volume tends to \(v_U(s)/v_U(0)\). This realizes the Gram volume as an infinitesimal spatial-volume ratio. No finite-\(\epsilon\) apparatus accuracy or error rate, and no interchange of this limit with later derivatives, is asserted: the theorem uses the defined Gram volume.

Differentiating the determinant at the initial identity gives
\[
v_U''(0)=\operatorname{tr}A''(0)
+(\operatorname{tr}A'(0))^2-\operatorname{tr}(A'(0)^2)
=\sum_a g(E_a,R(U,E_a)U).                                         \tag{12}
\]
With convention (3),
\[
\operatorname{Ric}(U,U)
=\sum_a g(E_a,R(E_a,U)U);
\]
the timelike contribution to the orthonormal trace vanishes because \(R(U,U)=0\). Antisymmetry in the curvature's first two operator arguments therefore yields
\[
\boxed{Q_U:=-v_U''(0)=\operatorname{Ric}_g(U,U).}                   \tag{13}
\]
No zero-shear condition over a finite interval was used. Full initial rest eliminates the initial deformation terms in (12); subsequent shear can develop.

## 4. Seven contractions and the finite-duration error

Write \(R_{ab}=\operatorname{Ric}_g(e_a,e_b)\) at \(p\). Symmetry of the metric Ricci tensor and (4) give
\[
Q_0=R_{00},\qquad
Q_{i\pm}=2R_{00}+R_{ii}\pm2\sqrt2\,R_{0i}.
\]
Thus, with exactly the registered coefficients,
\[
\mathcal I[g,p]:=\frac12\sum_{i=1}^3(Q_{i+}+Q_{i-})-7Q_0
=-R_{00}+\sum_iR_{ii}=R_g(p).                                    \tag{14}
\]
No source isotropy or special Ricci form is assumed. The scalar is independent of the chosen tetrad, although the individual channel readings and their preparation depend on it.

For each fixed channel, Taylor's formula with integral remainder and (13) gives
\[
v_U(d)=1-\frac12 Q_Ud^2+
\frac12\int_0^d(d-s)^2v_U'''(s)\,ds.
\]
The registered estimator is therefore
\[
F_U(d)=-\frac{2}{d^2}\left(\frac{v_U(d)}{v_U(0)}-1\right)
=Q_U-\frac1{d^2}\int_0^d(d-s)^2v_U'''(s)\,ds,
\]
and
\[
|F_U(d)-Q_U|\le \frac{M_Ud}{3}.                                   \tag{15}
\]
Apply the triangle inequality to
\[
S_d=\frac12\sum_i(F_{i+}(d)+F_{i-}(d))-7F_0(d).
\]
Equations (14) and (15) prove (1), including all signs and weights. The finite record determines this certified interval for \(R_g(p)\), not an exact scalar value. The exact value is the ideal preparation-event object (14).

If the two raw readings in channel \(U\) are \(a_U\mathcal V_U(0)\) and \(a_U\mathcal V_U(d)\), their defined ratio cancels a constant nonzero gain \(a_U\). Positive volumes and an available nonzero initial reading are required. Different channels need not share that absolute volume gain. Drift within a pair, clock/length scale, relative velocity, initial rest and the independent third-derivative bounds do not cancel. Here \(F_U,R\) have length\(^{-2}\) units and \(M_Ud\) does too. There is no stochastic sampling, noise, preparation-yield or instrument-feasibility assertion.

## 5. Scope and provenance

This article includes only the geometric identity and finite-duration bound. The source packet separately analyzes an ideal source variation; that application is not a premise or conclusion of this article. No finite-duration discrimination between two physical source metrics, native geometry or units, physical preparation/readout apparatus, empirical calibration, or complete curvature reconstruction is established. The volume-size limit, temporal derivative and metric variation are not interchanged.

The record consists of seven ratios (fourteen raw volume readings), with the stated gain, clock/length, velocity, full-rest and derivative-bound premises. A constant gain cancels only within its own pair. Neither the needed derivative bounds nor successful preparation follow from those two readings.

Source: DET Quantum Relativity, `qr-seven-volume-scalar-readout-20261126/REPORT.md`, sections 1–4; SHA256 `a3bdd573b6f4f19c7fa8cdce75a4409faa1c8be6b6c58c5bfa8d61285c16e578`. Equation numbers are retained from that source. The original distinct State result review and coordinator disposition govern scientific acceptance; independent publication review checks this extraction and its scope. Earlier exploratory exposure remains disclosed, and no blind-first-exposure claim is made.

Scientific review: `qr-seven-volume-scalar-readout-20261126-review/REVIEW.md`, SHA256 `70ba59302db3f914ab5dd496000db03fe02c962e9d7c563b33cdb3e5ad8a1c6c`; coordinator admission: `followthrough-0823-20261126/QR_RESULT_DISPOSITION.json`, SHA256 `46133578ea0e9505b7fe6b6f66530de10aa5f84d2c87bde99405005d4574ec9b`.
