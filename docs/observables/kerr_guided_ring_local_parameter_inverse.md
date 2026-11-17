# Kerr guided-ring records and a regular local parameter inverse

Under the supplied exact metric, apparatus and readout conventions, the three-record map below is smooth on an admissible neighborhood of the registered point

\[
p_0=(\mu,\alpha,w)=(1/12,1/48,0),
\]

and its Jacobian, with rows \((y_+,y_-,y_A)\) and columns \((\mu,\alpha,w)\), satisfies

\[
\boxed{\det DY(p_0)=-\frac{29579\pi^2}{115200}\ne0.}
\]

The inverse function theorem therefore supplies a regular local inverse near this point. This is a conditional conventional record-map certificate, with one reference point and exactly three records. It does not derive the Kerr metric or native quantities, establish a global inverse, or certify an empirical apparatus or quantitative noise tolerance.

## 1. Supplied metric, preparation and records

The model is the supplied exact Kerr exterior with signature \((-+++)\), Boyer–Lindquist coordinates \((t,r,\theta,\phi)\), infinity-normalized time \(t\) in seconds, and an oriented azimuth \(\phi\) of period \(2\pi\). Define

\[
m=\frac{GM}{c^2},\qquad a=\frac{J}{Mc},\qquad
\Sigma=r^2+a^2\cos^2\theta,\qquad
\Delta=r^2-2mr+a^2.
\]

Here \(M>0\), \(J\) is signed, and \(m,a\) have length units. The supplied line element is

\[
\begin{aligned}
ds^2={}&-\left(1-\frac{2mr}{\Sigma}\right)(c\,dt)^2
-\frac{4mar\sin^2\theta}{\Sigma}(c\,dt)\,d\phi
+\frac{\Sigma}{\Delta}\,dr^2+\Sigma\,d\theta^2\\
&+\left(r^2+a^2+\frac{2ma^2r\sin^2\theta}{\Sigma}\right)
\sin^2\theta\,d\phi^2.
\end{aligned}
\]

The positive scales \(G,c,R\) are supplied independently. In particular, \(R\) is a Boyer–Lindquist coordinate radius tag; it is neither a measured circumference nor an inferred areal radius.

The supported emitting receiver and both guided null signals remain at \(r=R,\theta=\pi/2\). The receiver has \(\phi=\Omega t\). Source mass \(M\), source angular momentum \(J\), receiver rotation \(\Omega\) and \(R\) remain constant throughout acquisition. Both pulses start at the same emission event \(t=0,\phi=0\) and retain their direction labels. Their prescribed return events are their first relative windings \(+2\pi\) and \(-2\pi\) with respect to the receiver. The update integrates the constant angular rates and receiver proper clock to those events.

The ideal guides, support, calibrated clock, signed radial acceleration readout, stationarity and negligible backreaction are supplied premises. The pulse paths are constrained null paths, not free null geodesics. The supported test structures are not a closed massive apparatus.

There are exactly three ideal real records, in this order:

\[
y_+=\frac{c\tau_+}{R},\qquad
y_-=\frac{c\tau_-}{R},\qquad
y_A=\frac{A_{\rm rad}R}{c^2}.
\]

Here \(\tau_\pm\) are the elapsed proper times from emission to the respective tagged first returns, read on the same emitting receiver's clock. \(A_{\rm rad}\) is the receiver's signed proper acceleration at emission, projected along its outward orthonormal radial axis. The direction tags and radial sign are part of the readout convention. No measured \(\Omega\), coordinate return time, independent lapse/redshift, circumference, gyroscope, orbit frequency or asymptotic source observation is added. The three-record count is conditional on the supplied preparation, scales and conventions; it does not make their cost or calibration free, or certify finite-precision experimental records.

The dimensional units are: \(\tau\), time; \(A_{\rm rad}\), length/time squared; \(M\), mass; \(J\), mass times length squared/time; and \(\Omega\), inverse time. The normalized records and parameters below are dimensionless. Their normalization does not derive native standards.

[Tartaglia, gr-qc/9806019v1](https://arxiv.org/html/gr-qc/9806019v1), version dated 4 June 1998, supplies conventional metric and guided-ring context only. The donor author and distinct scientific reviewer read the metric and section II.1 through equation 9. Its opposite signature and parameter \(a=J/M\) are translated to the convention above. The donor review reports an event-sign inconsistency in rendered equation 7 relative to the preceding relative-winding equations. The derivation below uses the direct relative-winding conditions, without importing that rendered sign. This is the retained donor finding, not an independent literature recheck by the assembler. No weak-field, numerical, geodesic, empirical or local-inverse result is borrowed from the paper.

Earlier accepted same-clock, signed-orientation and finite-record scope boundaries (CL059, CL088 and CL001) inform the acquisition conventions and limits only. Their flat or spherical formulas and inverse results are not mathematical premises here; their foundation boundaries do not establish a native correspondence. CL114 and active QR/PIM results are not premises of this calculation.

## 2. Ring metric and first proper-return times

Use dimensionless variables

\[
T=ct/R,\qquad \mu=m/R,\quad\alpha=a/R,\quad w=\Omega R/c,
\]

and the following abbreviations:

\[
\begin{aligned}
A&=1-2\mu,& B&=2\mu\alpha,& K&=1+(1+2\mu)\alpha^2,\\
D&=B^2+AK=1-2\mu+\alpha^2,& Q&=\sqrt D,\\
H&=B-Kw,& F&=A+2Bw-Kw^2,& \beta&=\sqrt F.
\end{aligned}
\]

The supplied full metric reduces at the ring to

\[
\frac{ds^2}{R^2}=-A\,dT^2-2B\,dT\,d\phi+K\,d\phi^2.
\]

In particular, its dimensional mixed coefficient is \(g_{t\phi}=-2mac/R\), so that the line element has cross term \(-4mac\,dt\,d\phi/R\). This fixes the factor of two and the spin-orientation sign. Every term in \(ds^2\) has length squared units.

The two ring-null angular rates, \(z_\pm=R\omega_\pm/c\), are the roots of \(Kz^2-2Bz-A=0\):

\[
z_\pm=\frac{B\pm Q}{K}.
\]

For the receiver, \(ds^2=-c^2Fdt^2\), hence \(d\tau=\beta\,dt\). On the admissible neighborhood specified below, \(z_-<w<z_+\). The relative phases are linear functions of \(T\), with positive directed gaps

\[
z_+-w=\frac{Q+H}{K},\qquad w-z_-=\frac{Q-H}{K}.
\]

Their first nonzero relative windings therefore occur at

\[
t_+=\frac{2\pi R/c}{z_+-w},\qquad
t_-=\frac{2\pi R/c}{w-z_-}.
\]

There is no earlier receiver return: before these times the corresponding strictly monotone relative phase lies strictly between zero and its first \(\pm2\pi\) value. Pulse-pulse crossings do not change the tagged receiver events. No division by \(w\) is used, so the registered \(w=0\) is regular.

Using \(D-H^2=KF\), the normalized proper readings are exactly

\[
\boxed{
 y_+=\frac{2\pi K\beta}{Q+H}=\frac{2\pi(Q-H)}{\beta},\qquad
 y_-=\frac{2\pi K\beta}{Q-H}=\frac{2\pi(Q+H)}{\beta}.
}
\]

Coordinate return times and the lapse \(\beta\) appear in the derivation only; neither is added as an observed record.

## 3. Actual local admissibility and the fixed horizon

At the one registered point,

\[
A_0=5/6,\quad B_0=1/288,\quad K_0=13831/13824,\quad
D_0=1921/2304,\quad Q_0=\sqrt{1921}/48,\quad F_0=A_0.
\]

The point lies strictly inside \(1/20<\mu<1/10\), \(|\alpha|<\mu/2\), \(|w|<1/10\). In that enclosing guard, \(|a|<m/2\) and \(R>2m\), so the ring is exterior to the subextremal outer horizon of the supplied metric. At the point, the receiver is timelike, \(D_0,K_0>0\), and the null roots are distinct.

For an explicit strict margin, \(Q_0>9/10\), \(0<B_0<1/100\) and \(K_0<11/10\). The first inequality follows by squaring positive quantities: \(192100>186624\). Thus

\[
z_+(p_0)>9/11>1/2,\qquad
-z_-(p_0)>89/110>1/2.
\]

Continuity supplies a nonempty open neighborhood \(\mathcal O\) of \(p_0\), contained in the guard, on which \(F,D,K>0\) and both relative gaps exceed \(1/2\). This yields the uniform acquisition bound

\[
0<t_\pm<4\pi R/c<20\pi R/c\qquad\text{throughout }\mathcal O.
\]

It also gives \(Q\pm H>0\), finite positive proper-return readings and their smoothness. This is an existence certificate for an actual local neighborhood with a fixed strict margin, not a classification of the entire guard box. Neither the reference point nor the scientific horizon was changed.

## 4. Signed radial acceleration and the held-fixed derivative

Let \(k=\partial_t+\Omega\partial_\phi\). For this calculation only, vary \(r\) at the equator while holding the dimensional \(m,a,\Omega\), equivalently \(M,J,\Omega\), fixed. The helical norm is \(g(k,k)=-c^2F(r)\), where

\[
F(r)=1-\frac{2m}{r}+\frac{4ma\Omega}{cr}
 -\left(r^2+a^2+\frac{2ma^2}{r}\right)\frac{\Omega^2}{c^2}.
\]

Since \(k\) is Killing and \(k(F)=0\), \(U=k/\sqrt F\) satisfies \(g(U,U)=-c^2\), and the Killing identity gives

\[
\nabla_U U=\frac{c^2}{2F}\operatorname{grad}F.
\]

At the equator, \(g_{rr}=r^2/\Delta\), so

\[
n_{\rm rad}=\frac{\sqrt\Delta}{r}\partial_r
\]

is an outward unit vector orthogonal to \(U\). Equatorial reflection symmetry makes the transverse \(\theta\) derivative vanish there. Consequently the prescribed signed radial projection is

\[
A_{\rm rad}=\frac{c^2\sqrt\Delta}{2rF}\,\partial_rF.
\]

Differentiating the displayed dimensional \(F(r)\), rather than freezing \(\mu,\alpha,w\), gives

\[
R\,\partial_rF\big|_R=2\{\mu(1-\alpha w)^2-w^2\}.
\]

Writing \(N=\mu(1-\alpha w)^2-w^2\), the third record is therefore

\[
\boxed{y_A=\frac{A_{\rm rad}R}{c^2}=\frac{QN}{F}.}
\]

An outward acceleration is positive. The sign is not replaced by a norm or an absolute value. \(A_{\rm rad}\) has units of length/time squared; \(y_A\) is dimensionless.

## 5. One reference-point Jacobian certificate

The exact record map, at fixed \(R,G,c\) and apparatus conventions, is

\[
Y(\mu,\alpha,w)=
\left(\frac{2\pi(Q-H)}{\sqrt F},\frac{2\pi(Q+H)}{\sqrt F},\frac{QN}{F}\right).
\]

All derivatives in this section vary \((\mu,\alpha,w)\) at fixed \(R,G,c\); this is different from the dimensional held-fixed radial derivative in section 4. We evaluate rank only at \(p_0\).

For transparent manual algebra, re-express the same records as

\[
Z_1=\frac{y_+y_-}{4\pi^2}=K,\qquad
Z_2=\frac{y_--y_+}{4\pi}=V=\frac{H}{\sqrt F},\qquad
Z_3=y_A.
\]

This transformation is invertible near the positive return readings. Its determinant is

\[
\det\frac{\partial Z}{\partial Y}
 =\frac{y_++y_-}{16\pi^3}=\frac{Q}{4\pi^2\sqrt F}>0.
\]

Thus it neither adds a datum nor changes differential rank. In particular, the algebraic quantity \(K\) is obtained from the two supplied time readings; no circumference measurement is inserted.

Let \(L_0=1+2\mu_0=7/6\). Differentiation of the exact map gives the following one reference-point Jacobian in these equivalent record coordinates:

\[
DZ(p_0)=
\begin{pmatrix}
2\alpha_0^2 & 2\alpha_0L_0 & 0\\
\dfrac{2\alpha_0(1-\mu_0)}{A_0^{3/2}} &
\dfrac{2\mu_0}{\sqrt{A_0}} &
-\dfrac{D_0}{A_0^{3/2}}\\
\dfrac{Q_0}{A_0^2}-\dfrac{\mu_0}{Q_0A_0} &
\dfrac{\mu_0\alpha_0}{Q_0A_0} &
-\dfrac{2Q_0\mu_0\alpha_0}{A_0^2}
\end{pmatrix}.
\]

For example, its first row is \((1/1152,7/144,0)\), and its second row is
\((11/(288A_0^{3/2}),1/(6\sqrt{A_0}),-1921/(2304A_0^{3/2}))\). No derivative at a second reference is used.

Here is a manual determinant certificate. In the next identities every symbol carries its reference value; omitted subscripts are only typographic shorthand for \(p_0\). Define

\[
v=(L,-\alpha,2\alpha/D).
\]

The cross product of the first two rows and the directional derivative of the third are

\[
\nabla K\times\nabla V=-\frac{2\alpha D}{A^{3/2}}v,
\qquad
\nabla y_A\cdot v=\frac{(1-\mu)(L+\alpha^2)}{AQ}.
\]

For direct checking, the numerator of the latter expression before cancellation, over the denominator \(QA^2\), is

\[
DL-\mu AL-\mu\alpha^2A-4\mu\alpha^2
 =A(1-\mu)(L+\alpha^2).
\]

It follows that

\[
\det DZ(p_0)=-\frac{2\alpha_0Q_0(1-\mu_0)(L_0+\alpha_0^2)}{A_0^{5/2}}.
\]

Restoring the original registered record coordinates gives

\[
\begin{aligned}
\det DY(p_0)
&=\det DZ(p_0)\frac{4\pi^2\sqrt{A_0}}{Q_0}\\
&=-\frac{8\pi^2\alpha_0(1-\mu_0)(L_0+\alpha_0^2)}{A_0^2}\\
&=-\frac{29579\pi^2}{115200}\ne0,
\end{aligned}
\]

where \(L_0+\alpha_0^2=2689/2304\). This proves rank three for the one prescribed map at the one prescribed reference. Smoothness on \(\mathcal O\) and the inverse function theorem yield a neighborhood \(\mathcal U\subset\mathcal O\) on which \(Y\) has a smooth, hence regular \(C^1\), local inverse.

## 6. What the acceleration record contributes

The two-time subrecord differential at this same point has rank two. In the equivalent \((K,V)\) coordinates, its minor in columns \((\alpha,w)\) is

\[
(2\alpha_0L_0)(-D_0/A_0^{3/2})\ne0.
\]

Its one-dimensional kernel is spanned by

\[
v_0=(7/6,-1/48,96/1921).
\]

This perturbation leaves both proper-return readings unchanged to first order while varying source and observer parameters. In particular, \(\delta\mu=7/6\), \(\delta w=96/1921\) and \(\delta(\mu\alpha)=13/576\) for the stated vector normalization. The acceleration derivative along it is strictly positive:

\[
Dy_A(p_0)v_0=
\frac{(1-\mu_0)(L_0+\alpha_0^2)}{A_0Q_0}>0.
\]

The acceleration row therefore supplies the missing third independent differential direction. This comparison is a first-order statement at \(p_0\), not a constructed exact finite family with the same two records. No global two-record degeneracy or general nonlinear nonidentifiability theorem is inferred from rank alone.

## 7. The two prescribed limit controls

**Flat geometric limit.** Take \(m,a\to0\) together, at fixed \(R\) and \(|w|<1\). This is a limit of geometric parameters, without defining \(J/M\) at \(M=0\). Then \(A=D=K=Q=1\), \(B=0\), \(H=-w\), \(F=1-w^2\), and

\[
y_+=\frac{2\pi\sqrt{1-w^2}}{1-w},\qquad
y_-=\frac{2\pi\sqrt{1-w^2}}{1+w},\qquad
y_A=-\frac{w^2}{1-w^2}.
\]

These are the guided-ring Minkowski return readings of a rotating receiver and its inward centripetal proper acceleration, negative under the outward-axis convention. Positive \(w\) lengthens the plus return relative to the minus return, as the relative-winding derivation requires.

**Schwarzschild supported-observer limit.** Set \(a=0\), retaining signed \(w\), and require \(A-w^2>0\), where \(A=1-2\mu\). Now \(D=A\), \(K=1\), \(B=0\), and

\[
y_+=\frac{2\pi\sqrt{A-w^2}}{\sqrt A-w},\qquad
y_-=\frac{2\pi\sqrt{A-w^2}}{\sqrt A+w},\qquad
y_A=\frac{\sqrt A(\mu-w^2)}{A-w^2}.
\]

At zero receiver rotation these reduce to \(y_+=y_-=2\pi\) and \(y_A=\mu/\sqrt A\), the outward static-support value. The sign of \(w\) exchanges the two labelled readings. These are only the two stipulated algebraic controls; no additional reference-point rank evaluations or parameter survey are made.

## 8. Scope and unresolved premises

The accepted result is: exactly the two tagged proper-return times and the signed radial acceleration possess a regular local inverse near the registered admissible point. At fixed supplied scales, the corresponding dimensional variables are

\[
M=\mu c^2R/G,\qquad
J=\mu\alpha c^3R^2/G,\qquad
\Omega=cw/R.
\]

This change of parameters is regular because \(\mu_0>0\). Thus the local certificate distinguishes the supplied source mass and oriented angular momentum from supported observer rotation in this ideal exact model. It does not assert a global distinction across all spin signs or parameter regions.

The unresolved physical premises are the exact Kerr exterior, independent radius tag and scales, sustained supported ring and guides, direction tags, calibrated clock and signed acceleration observation, stationarity during acquisition, and neglect of backreaction. The calculation supplies no observational data and no permission for empirical execution. A local smooth inverse is not a quantitative conditioning, noise-error, calibration or practical-sensitivity certificate.

The dimensionless normalization does not establish native \(G,c\), mass, spin, action, length or time. The finite-record language does not supply DET ontology, gravity dynamics, manifold emergence, a native detector kernel, physical heat from information loss, or quantum/classical divergence. No result from the active QR or PIM lanes is assumed. Retired kappa-gravity remains retired. Any future use must preserve the supplied state, update and readout assumptions.

The local result is a conditional conventional three-record correspondence target for future gravity, mass and native-quantity modelling. It can be retained without an immediate integration consumer. A later comparison must supply its own state, update, observation and parameter map; matching a formal record pattern does not establish a native realization.

The inverse theorem gives no numerical neighborhood radius, full-box injectivity, global all-spin inverse, quantitative conditioning, noisy-data error bound or empirical calibration. There is no second-radius, different-reference, additional-record, unsigned-acceleration or differently labelled readout result. The two-time comparison remains differential only. Source-interior dynamics, apparatus realization and backreaction control are unresolved physical premises.

This article **derives** a conditional map and local analytic inverse certificate from supplied conventional laws. Its displayed proof and two stated limits provide the finite mathematical checks. It reports no implemented apparatus, empirical run, agreement with observed data or derivation of native units. These achievements remain separate.

## 9. Source and review provenance

This article assembles the accepted CL115/v1 result. The Classical lane author produced the proof; Classical root performed a distinct nonblind scientific review and admitted the unchanged result. That reviewer had prospective design, metric/sign and held-fixed acceleration convention exposure, but did not compute the selected map, rank or determinant before the author. A separate recipient review admitted retention with the assumptions and gaps stated here, and the coordinator accepted that limited use. The assembler performed that recipient review, but was neither the donor author nor its proof reviewer. Article assembly reuses these reviews; it adds no new scientific case or proof.

The following byte counts and SHA-256 values identify the accepted archived artifacts. They are provenance identifiers, not scientific validation and not public reproduction links. The metric, derivation, local certificate and limitations needed to assess the result are included above; the versioned primary source is linked in section 1.

| Archived artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Coordinator scope disposition | 5844 | `8a10796064bb2dfea7d29982139fb77c983d033b4257e8c11de191e4511e427d` |
| CL115/v1 supplied control | 13542 | `18a3a1f4deefffe353a21f27bfadad5bc87b4b683284c5917098628dec5f2577` |
| CL115/v1 author result | 15357 | `684f94f9633cd70d6b7775c1b3a205573cfcb9e6aa4b4fe4e0c6c82084be78f4` |
| CL115/v1 author manifest | 9709 | `8d8db9fede720cce5e9b1a5cb5a4c8e615389d328048b2434759de12e3651817` |
| CL115/v1 distinct scientific review | 9907 | `924a9aba90ab69f054a5364176deaaa625ee58046c7f5840003da5e81d0a5e19` |
| CL115/v1 scientific review manifest | 7312 | `8f9a9b4d3f064d6d39a300098ed908d740061ced93cbd8417a0a55614c7b1a3a` |
| CL115/v1 donor disposition | 5354 | `d67e415e0ccc98bac12b6ab730c58e5874f9fcb460d8bba6ee7a1a9abace5655` |
| Recipient scope review | 12007 | `792f5084fc41d802b0dd6765ad0f496b3aef24b8e4314650f58fc03171bc5bc9` |
| Recipient review manifest | 9961 | `6e6ad6af770e3770edc9e9ee7a21198d67697e904b92cd82817afa7b1e962751` |

The donor primary-source archive is the cited Tartaglia v1 HTML: 248976 bytes, SHA-256 `22495948aa4a9b20698a11c2295be9136cd7dfdf281c32772f4b6da16c5a7bd3`. Its content was read by the donor author and reviewer within the scope stated above; assembly preserves that source role.
