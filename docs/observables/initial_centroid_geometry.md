# Initial centroid acceleration and omitted constituent geometry

This reviewed conditional comparator, CL118/v1, uses exactly two preparations at a/R=1/4 in one prescribed inverse-square field, their sole uniform-field control, and a potential-gradient check of those same cases. Its scientific proof and recipient scope received distinct review. No empirical experiment or native gravity correspondence is asserted.

The exact initial centroid accelerations are

\[
A_{\parallel}=-\frac{272}{225}g_0 e_x,\qquad
A_{\perp}=-\frac{64}{17\sqrt{17}}g_0 e_x,
\qquad g_0=\frac{GM}{R^2}>0.
\]

Both y and z components vanish. With e_x outward from the source, the specified signed normalized difference is

\[
\boxed{\Delta=\frac{e_x\cdot(A_{\parallel}-A_{\perp})}{g_0}
=\frac{64}{17\sqrt{17}}-\frac{272}{225}<0.}
\]

Identical universal constituent coupling permits this difference. The common record omits the direction of the relative positions despite their known magnitude. In the uniform-field control both centroid accelerations equal -g0 e_x. These are instantaneous second derivatives only, without a calculated trajectory or maintained extent.

## Check 1 — admissible states and common record

G,M,m,R are positive and a=R/4 exactly. The source is fixed at the origin and supplies

\[
b(x)=-GM\frac{x}{|x|^3}\quad(x\ne0).
\]

Each independent probe has constant inertial mass and passive gravitational mass m/2 and satisfies ddot x_+=b(x_+), ddot x_-=b(x_-). Each force is (m/2)b. Mutual forces, recoil/backreaction, binding, collisions and any rigid or supporting structure are absent by assumption. This external prescribed-field model is supplied, not derived from DET.

The parallel initial positions are (5R/4)e_x and (3R/4)e_x. The transverse positions are R e_x+(R/4)e_y and R e_x-(R/4)e_y, each at radius sqrt(17)R/4. Since 3<sqrt(17)<5, all four source distances lie between the positive values 3R/4 and 5R/4. The constituent separation within either pair is 2a=R/2>0. All force evaluations and local spatial derivatives below are admissible. No later noncollision interval is claimed.

Both preparations have zero constituent velocities, total mass m and mass-weighted centroid

\[
X(0)=\frac{x_+(0)+x_-(0)}2=R e_x,\qquad \dot X(0)=0.
\]

Each constituent is exactly a from its centroid. The full relative-position vector is 2a e_x in the parallel preparation and 2a e_y in the transverse preparation. These are different complete states with the same extent magnitude, composition and coupling law. The reduced record retains m, X(0), dot X(0), G,M,R, the common field and simultaneous initial acquisition convention. The common size a=R/4 is known. Relative-position direction is omitted; no hidden initial velocity difference is used.

## Check 2 — mass-weighted force average

For constant equal masses m_+=m_-=m/2,

\[
X=\frac{m_+x_++m_-x_-}{m},\qquad
m\ddot X=m_+\ddot x_++m_-\ddot x_-=F_++F_-.
\]

The stipulated passive/inertial equality therefore yields

\[
A:=\ddot X(0)=\frac{F_+(0)+F_-(0)}m
=\frac{b(x_+(0))+b(x_-(0))}{2}.
\]

The probe mass m cancels. There is one factor 1/2; the acceleration field is not divided again by a constituent mass. Signs come from the attractive vector field at each actual position. Its average has not been replaced by the field at the centroid.

## Check 3 — exact vectors and signed comparison

In the parallel preparation both vectors point along +e_x, so

\[
b(x_+^{\parallel})=-\frac{GM}{(5R/4)^2}e_x=-\frac{16}{25}g_0e_x,
\quad
b(x_-^{\parallel})=-\frac{GM}{(3R/4)^2}e_x=-\frac{16}{9}g_0e_x.
\]

Each y,z component is zero. Their average is

\[
A_{\parallel}=-\frac12\left(\frac{16}{25}+\frac{16}{9}\right)g_0e_x
=-8\frac{9+25}{225}g_0e_x=-\frac{272}{225}g_0e_x.
\]

The transverse positions R(e_x +/- e_y/4) have common cubed radius 17sqrt(17)R^3/64. Consequently

\[
b(x_+^{\perp})=-\frac{64}{17\sqrt{17}}g_0e_x-\frac{16}{17\sqrt{17}}g_0e_y,
\]
\[
b(x_-^{\perp})=-\frac{64}{17\sqrt{17}}g_0e_x+\frac{16}{17\sqrt{17}}g_0e_y.
\]

The z components vanish and the opposite y components cancel, giving

\[
A_{\perp}=-\frac{64}{17\sqrt{17}}g_0e_x.
\]

The signed radial subtraction gives the displayed Delta. Its strict sign follows without a series or decimal approximation: 272/225>1, whereas

\[
0<\frac{64}{17\sqrt{17}}<1
\quad\hbox{because }64^2=4096<4913=17^3.
\]

Hence Delta<0. The parallel centroid has the more negative outward-radial component, equivalently the larger inward acceleration magnitude. No angle or a/R variation was used.

The assignments [G]=length^3/(mass time^2), [M]=[m]=mass and [R]=[a]=length give [g0]=[A]=length/time^2. All displayed coefficients and Delta are dimensionless. Mass cancellation follows from the supplied equal passive/inertial masses and weighting, not a derived native mass definition.

## Check 4 — alternate check through the point-potential gradient

The scalar phi(q)=-GM/|q| is an algebraic potential for the stipulated field. At q!=0, differentiation gives partial_i phi=GM q_i/|q|^3, hence -grad phi=b. Using this verified primitive adds no source law.

For d equal to one of the two prescribed offsets, define the instantaneous coordinate expression

\[
U_d(X)=\frac{m}{2}\phi(X+d)+\frac{m}{2}\phi(X-d).
\]

Its common-translation gradient satisfies

\[
-\nabla_X U_d=F_++F_-,\qquad
A=-\frac1m\nabla_X U_d\big|_{X=Re_x}.
\]

This spatial derivative holds d fixed as a coordinate of the same instant's sum. It imposes no rigid constraint or time law for separation. Below u is only a differentiation variable and only u=R is evaluated. Constants R and a=R/4 remain fixed when differentiating u; a is not differentiated as u/4. There is no additional preparation or trajectory.

For d=a e_x and X=u e_x near R>a,

\[
U_{\parallel}(u,0,0)=-\frac{mGM}{2}
\left[\frac1{u+a}+\frac1{u-a}\right],
\]
\[
-\frac1m\partial_u U_{\parallel}\big|_{u=R}
=-\frac{GM}{2}\left[\frac1{(R+a)^2}+\frac1{(R-a)^2}\right]
=-\frac{272}{225}g_0.
\]

The full U_parallel(X) is even in the centroid y and z coordinates at this axis, so its y,z derivatives there vanish. The complete parallel vector is recovered.

For d=a e_y and X=u e_x,

\[
U_{\perp}(u,0,0)=-\frac{mGM}{\sqrt{u^2+a^2}},
\]
\[
-\frac1m\partial_u U_{\perp}\big|_{u=R}
=-\frac{GMR}{(R^2+a^2)^{3/2}}
=-\frac{64}{17\sqrt{17}}g_0.
\]

The full U_perp(X) is even in centroid y because its two terms exchange under y reversal, and even in z because each squared distance is. Its y,z derivatives at (R,0,0) vanish. Scalar differentiation thus recovers the complete transverse vector and the same signed Delta. Phi has units length^2/time^2 and U has units mass length^2/time^2, consistent with the force and acceleration gradients. No empirical energy measurement is claimed.

## Check 5 — sole uniform-field control and label exchange

For the same preparations replace b by b_u(x)=-g0 e_x, with unchanged masses, frame and exact initial access. Each constituent then has acceleration -g0 e_x, so

\[
A_{\parallel,u}=A_{\perp,u}=-g_0e_x,
\qquad \frac{e_x\cdot(A_{\parallel,u}-A_{\perp,u})}{g_0}=0.
\]

There is no orientation dependence in this control because the different evaluation points receive the same vector. This is the sole replacement field.

Exchanging + and - permutes equal masses and the two terms in X, dot X, A and U_d. Equivalently it changes d to -d in a symmetric sum. Each centroid and computed centroid acceleration is unchanged in both fields. Label names cannot explain the signed difference.

## Check 6 — ledger, interpretation and limits

All vectors in this exact initial-event ledger are normalized by g0.

| Field and geometry | b(x_+)/g0 | b(x_-)/g0 | Centroid A/g0 |
|---|---|---|---|
| Inverse-square, parallel | -(16/25)e_x | -(16/9)e_x | -(272/225)e_x |
| Inverse-square, transverse | -[64/(17sqrt(17))]e_x - [16/(17sqrt(17))]e_y | -[64/(17sqrt(17))]e_x + [16/(17sqrt(17))]e_y | -[64/(17sqrt(17))]e_x |
| Uniform, parallel | -e_x | -e_x | -e_x |
| Uniform, transverse | -e_x | -e_x | -e_x |

Every row has mass m, centroid R e_x, centroid velocity zero and constituent offset magnitude a=R/4. Every z component is zero. The inverse-square signed radial difference is 64/(17sqrt(17))-272/225<0; the uniform difference is zero. The direct and alternate routes agree on both inverse-square vectors.

A single-valued function of the common reduced record would return the same initial A for the two identical retained inputs. The distinct inverse-square A values refute such a prediction on this two-preparation domain. The missing information is relative-position direction, not an undisclosed size, source, clock, mass or coupling. Retaining the specified constituent geometry and literal field permits the direct average; no minimality claim for additional observations is required.

The mismatch alone therefore cannot diagnose nonuniversal constituent coupling. Equal inertial and passive gravitational mass has been imposed for every constituent, with the same field in both preparations. The difference arises from averaging that spatially varying field at different full positions. It establishes no physical equivalence-principle violation, composition-dependent gravity, stochastic full-state dynamics or different dynamical regime. The uniform control isolates spatial variation within these supplied cases; it does not classify all fields or preparations.

The independent point-probe states, external Newtonian field, universal coupling, absence of interactions/backreaction/support, coordinates, clock, physical units and exact initial acquisition are supplied. The mass-weighted relation, exact signed vectors, strict inequality, uniform equality and reduced-record consequence are derived. Positions lie in the smooth nonzero-source domain, but no positive-time trajectory, maintained orientation, binding, disruption estimate, error bound, finite release interval or later-body assertion is made. No source inverse, extra angle/ratio, series/multipole hierarchy, native correspondence, calibration or empirical observation is included. This is synthetic conditional theory, not empirical-execution permission.

## Recipient scope and publication

The retained record uses supplied simultaneous Newtonian inertial Cartesian coordinates and one common time parameter. Acceleration is the prediction target, not an extra predictor input. Exact instantaneous acquisition is an idealization; no finite sampling instrument, uncertainty, duration or calibration is supplied. Source mass M parametrizes the external field and is not obtained from a source solution. Probe-mass cancellation does not establish an independently derived active/inertial mass relation.

A recipient may reuse this comparator while retaining constituent geometry, or supply a separately justified coarse approximation and its validity/error limits. No DET history-to-position/update/readout map, relativistic centroid equation, Einstein mean source, physical preparation, native clock, calibrated native unit or empirical equivalence-principle result is supplied. The fixed extent is not a small-extent expansion. No automatic successor follows.

This public derivative preserves the admitted calculation and limitations. Private controls, exact source custody, reviewer runtime identities and correspondence records are withheld under the [publication policy](../coordination/REDACTED_PUBLICATION.md). The [public manifest](../publications/initial-centroid-geometry/PUBLICATION_MANIFEST.json) identifies only the public payloads; hashes establish identity, not scientific truth.
