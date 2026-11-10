# Later spin after a central oblique impulse

For the specified homogeneous 2:1 prolate spheroid, the central impulse $(J,J,0)$ produces no instantaneous spin, but the subsequent free motion has
$$
 -\frac{\nu}{4}\ \leq\ \omega(T)\ \leq\
 -\frac{\nu}{4}\cos\frac1{16}<0,
 \qquad T=\frac1{4\nu},\qquad
 \nu^2=\frac{(b-a)J^2}{Iab}.
$$
The negative sign means clockwise in the registered plane. At every time through this horizon the generalized spatial angular impulse about the fixed initial origin is exactly zero: the positive orbital term equals the magnitude of the negative intrinsic term. The fresh-rest principal-axis impulse $(J,0,0)$ gives zero rotation throughout the same interval. These statements use the actual kinetic coefficients of one body and its surrounding potential flow; they do not conserve bare-body momentum in place of the coupled system.

## Model, source roles and exact coefficients

The body has semiaxes $(2\ell,\ell,\ell)$, $\ell>0$, homogeneous material mass $m>0$, volume $V=8\pi\ell^3/3$, and coincident geometric and mass centres. Its exterior contains homogeneous incompressible inviscid irrotational fluid of density $\rho_f>0$. The fluid is unbounded, has zero circulation, obeys slip/no-penetration on the hull, and its velocity decays at infinity. There is no gravity, free surface or other boundary. The complete system begins at rest. Body axes $\mathbf e_1,\mathbf e_2,\mathbf e_3=\mathbf e_1\times\mathbf e_2$ are registered, with the long axis along $\mathbf e_1$; initially $x=0$ and planar angle $\theta=0$. Positive angle is counterclockwise when viewed along positive $\mathbf e_3$ toward the origin.

Only the exact translational factors and principal-axis comparison are reused from the accepted [two-immersed-impulse comparator](material_mass_from_two_immersed_impulses.md). With
$$
 n=\frac{2\log(2+\sqrt3)}{3\sqrt3}-\frac13,\qquad
 p=\frac{n}{1-n},\qquad q=\frac{1-n}{1+n},\qquad 0<p<q,
$$
define $D=\rho_fV$, $a=m+pD$, $b=m+qD$. Thus $0<a<b$. The homogeneous body's transverse moment is
$$
 I_b=\frac m5\big((2\ell)^2+\ell^2\big)=m\ell^2.
$$
That translational comparator does not supply a freely selectable rotational moment or the present instantaneous preparation.

The public mechanics source supplies the body-plus-fluid quadratic kinetic action and the generalized impulse equations, which are specialized and checked below. Its equation (6) includes the orbital term about the fixed spatial origin; equations (9)–(18) give the kinetic matrix, symmetry reduction and Kirchhoff equations. No controls, vehicle tests, drag, buoyancy or efficiency results are imported. [Chyba, Haberkorn and Smith, May 4, 2006 PDF, §2, equations (3)–(18), PDF pp. 4–5](https://math.hawaii.edu/~mchyba/documents/publications/dcds06.pdf). Tuckerman distinguishes translational and rotational potential-flow inertia for an ellipsoid and treats the prolate case; its context supports using the same hull for both coefficients. The construction below establishes the needed rotational coefficient without reading a numerical value from its tables. [Tuckerman, NACA Report 210, printed p. 3 and §4 on printed p. 7, PDF pp. 5 and 9](https://ntrs.nasa.gov/api/citations/19930091277/downloads/19930091277.pdf). The manifest pins the exact local PDF versions actually read.

## The same-hull rotational Neumann energy

Let $r=(r_1,r_2,r_3)$ be coordinates from the centre and let $n_S$ point outward from the body into the fluid. The unit-angular-velocity potential must satisfy
$$
 \Delta\psi=0,\quad \psi\longrightarrow0\text{ at infinity},\qquad
 \partial_{n_S}\psi=(\mathbf e_3\times r)\cdot n_S.
$$
Here is an explicit construction demonstrating that this problem has a finite, nonzero energy for this exact hull. Put $s_1=4\ell^2$, $s_2=s_3=\ell^2$, and define the confocal coordinate $\lambda\geq0$ outside the spheroid by
$$
 \sum_{i=1}^3\frac{r_i^2}{s_i+\lambda}=1.
$$
Set
$$
 F(\lambda)=\int_\lambda^\infty
 \frac{ds}{(4\ell^2+s)^{3/2}(\ell^2+s)^2},\quad
 c_0=\frac5{4\ell^2},\quad d_0=\frac3{4\ell^2},\quad
 h_0=c_0F(0)+2F'(0).
$$
The integrand is positive, $F'(0)=-1/(8\ell^7)$, and
$$
 0<F(0)<\frac1{8\ell^3}\int_0^\infty\frac{ds}{(\ell^2+s)^2}
 =\frac1{8\ell^5},\qquad h_0<-\frac3{32\ell^7}<0.
$$
Consequently the finite coefficient $C=d_0/h_0$ is well defined. Take
$$
                         \psi(r)=C\,r_1r_2F(\lambda(r)).
$$
For a direct harmonicity check, write $h_i=s_i+\lambda$ and $S=\sum r_i^2/h_i^2$. Implicit differentiation yields
$$
 \partial_i\lambda=\frac{2r_i}{h_iS},\quad
 |\nabla\lambda|^2=\frac4S,\quad
 \Delta\lambda=\frac2S\sum_i\frac1{h_i}.
$$
It follows that
$$
 \Delta(r_1r_2F(\lambda))=
 \frac{4r_1r_2}{S}\left[
 F''+\left(\frac1{h_1}+\frac1{h_2}
              +\frac12\sum_i\frac1{h_i}\right)F'\right]=0,
$$
because $F'=-(h_1h_2\sqrt{h_1h_2h_3})^{-1}$. On the surface let
$N=\sqrt{\sum r_i^2/s_i^2}$. Then $n_{S,i}=r_i/(s_iN)$, $\partial_{n_S}\lambda=2/N$, and
$$
 \partial_{n_S}\psi=\frac{Cr_1r_2}{N}
       [c_0F(0)+2F'(0)]
 =\frac{d_0r_1r_2}{N}
 =(-r_2,r_1,0)\cdot n_S.
$$
The confocal coordinate and potential are smooth up to this smooth surface. At infinity $\lambda$ grows as $|r|^2$, so $F=O(|r|^{-5})$, $\psi=O(|r|^{-3})$, and $\nabla\psi=O(|r|^{-4})$. Thus
$$
 0<I_f:=\rho_f\int_{\mathrm{exterior}}|\nabla\psi|^2\,dV<\infty,
 \qquad I=I_b+I_f>0.
$$
Strict positivity follows because the prescribed normal velocity is nonzero where $r_1r_2\ne0$; zero Dirichlet energy would force a constant, hence zero, potential. Green's identity, using the fluid domain's inner outward normal $-n_S$, also gives the sign check
$$
 \int_{\mathrm{exterior}}|\nabla\psi|^2dV
 =-\int_S\psi\,\partial_{n_S}\psi\,dS>0.
$$
The decaying finite-energy Neumann solution is unique: apply the same identity to a difference with homogeneous normal data to obtain zero gradient. This fixes $I$ by the geometry, density and material mass. It is neither adjustable nor inferred from the later spin readout. No special-function evaluation of $I_f$ is needed for the certificate.

## Symmetry, kinetic reduction and signs

At a fixed pose the exterior potential is linear in the body's translational and angular velocities. For a translation along axis $i$, uniqueness and the hull reflections make the unit-speed potential odd in $r_i$ and even in the other coordinates. For rotation about axis $i$, its potential is even in $r_i$ and odd in each of the other two coordinates (or identically zero). In particular each translational potential is odd under central inversion, while each rotational potential is even. The mixed energy integrand $\nabla\phi_i\cdot\nabla\psi_j$ is therefore odd under central inversion and integrates to zero. Reflection in an individual coordinate similarly eliminates all off-diagonal entries within the translational and rotational blocks. These integrals converge; the decaying translational potentials have finite energy as in that comparator, and the rotational construction above and axial symmetry supply the needed rotational fields.

The body's translation-rotation terms vanish because its mass centre is the coordinate origin; its homogeneous inertia tensor is diagonal. Transverse rotational symmetry then gives the full translational matrix $M=\operatorname{diag}(a,b,b)$ and rotational matrix $\mathcal I=\operatorname{diag}(c,I,I)$. Here $c=2m\ell^2/5>0$: rotation about the long symmetry axis has zero normal velocity, hence zero fluid potential. The positivity of both blocks makes the velocity-to-impulse map nonsingular.

Let the body velocity be $U$, its angular velocity $\Omega$, and let $Q$ rotate body vectors to spatial vectors. The free kinetic action gives the body-frame Kirchhoff equations
$$
 \frac d{dt}(MU)=(MU)\times\Omega,\qquad
 \frac d{dt}(\mathcal I\Omega)=
       (\mathcal I\Omega)\times\Omega+(MU)\times U.
$$
For $U=(u,v,0)$, $\Omega=(0,0,\omega)$, the first right-hand side has only components 1 and 2 and the second only component 3. Thus the planar subspace is invariant by uniqueness; it is not an additional forcing constraint. In this subspace, $Q$ is the positive planar rotation $R(\theta)$, and
$$
 K=\tfrac12(au^2+bv^2+I\omega^2),\quad
 \dot x=R(\theta)(u,v),\quad \dot\theta=\omega,
$$
$$
 a\dot u=bv\omega,\qquad b\dot v=-au\omega,\qquad
                         I\dot\omega=(a-b)uv.                 \tag{1}
$$
These signs can be checked directly without trusting an anticipated equation. Write $E=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ and $U=R^T\dot x$. Since $x$ is cyclic, the spatial conjugate impulse
$P=R(au,bv)$ is constant in free motion. Differentiating $R^TP$ gives $(a\dot u,b\dot v)=-\omega E(au,bv)$, the first two equations. At fixed $\dot x$, $\partial_\theta U=-EU=(v,-u)$, so
$\partial_\theta K=(a-b)uv$. The angular Euler-Lagrange equation gives the third. This also derives the planar equations from the admitted action rather than adopting the control's disclosed design guesses as premises.

## Instantaneous preparation and finite horizon

During the registered instantaneous jump, the position and orientation do not change. External virtual work is the central force dotted with $\delta x$, with no moment multiplying $\delta\theta$. The generalized impulse boundary therefore gives
$$
 P(0^+)=(J,J),\quad I\omega(0^+)=0,\qquad
 u(0^+)=J/a,\quad v(0^+)=J/b,\quad\omega(0^+)=0.       \tag{2}
$$
The zero pre-state is the complete body-fluid rest state. This boundary is an additional ideal instantaneous preparation; it is not silently identified with the comparator's finite axial pulses. In particular the impulse is not set equal to $m\dot x$.

From constant $P=(J,J)$,
$$
 au=J(\cos\theta+\sin\theta),\qquad
 bv=J(\cos\theta-\sin\theta),\qquad
 uv=\frac{J^2}{ab}\cos2\theta.
$$
Substitution into (1) yields the scalar equation
$$
 \ddot\theta=-\nu^2\cos2\theta,\qquad
 \theta(0)=\dot\theta(0)=0,
 \qquad\nu^2=\frac{(b-a)J^2}{Iab}>0.                    \tag{3}
$$
Its first-order vector field is smooth and globally Lipschitz in $(\theta,\omega)$. More concretely, $|\dot\omega|\leq\nu^2$ implies $|\omega(t)|\leq\nu^2t$ and $|\theta(t)|\leq\nu^2t^2/2$ for every nonnegative time of local existence. Hence no finite-time escape is possible; the solution extends through the supplied $T$. Reconstruction gives $|u|\leq\sqrt2J/a$, $|v|\leq\sqrt2J/b$, so $x$ also remains finite on every finite interval. The smooth pose and velocities reconstruct the same finite-energy harmonic flow around a smooth hull in the unbounded domain. This is existence in the stipulated potential-flow kinetic model, not a stability theorem for arbitrary fluid perturbations.

On the entire interval $[0,T]$, the unconditional bound gives
$$
 |\theta(t)|\leq\tfrac12\nu^2t^2\leq\tfrac1{32},\qquad
                         \cos2\theta(t)\geq\cos\tfrac1{16}>0.
$$
It is not assumed that the angle already has one sign. Integrating (3) now proves
$$
 -\nu^2t\leq\omega(t)\leq-\nu^2t\cos\tfrac1{16},\qquad
 -\tfrac12\nu^2t^2\leq\theta(t)\leq
              -\tfrac12\nu^2t^2\cos\tfrac1{16}.            \tag{4}
$$
At the exact specified horizon,
$$
 -\frac\nu4\leq\omega(T)\leq-\frac\nu4\cos\tfrac1{16}
 \leq-\frac{511\nu}{2048}<0,
 \qquad
 -\frac1{32}\leq\theta(T)\leq-\frac1{32}\cos\tfrac1{16}.
$$
The rational bound uses $\cos z\geq1-z^2/2$. Thus the initial acceleration $-\nu^2$ is supplemented by a quantitative certificate across the whole prescribed interval, not an unspecified short-time assertion. No numerical trajectory, parameter sweep or orbit classification is used.

For the matched fresh-rest principal-axis control, the central impulse is instead $(J,0,0)$. Equations (1) and the nonsingular impulse boundary have the exact solution
$$
 u=J/a,\quad v=\omega=\theta=0,\quad x=(Jt/a,0).
$$
Uniqueness makes this the control evolution on the same $T=1/(4\nu)$ registered from the oblique trial's supplied coefficients and component $J$. Its spatial impulse is $(J,0)$, angular impulse is zero and kinetic energy is $J^2/(2a)$.

## Complete kinetic and generalized impulse balances

For the oblique trial, equation (1) gives
$$
 \dot K=buv\omega-auv\omega+(a-b)uv\omega=0,
 \qquad K=K_0=\frac{J^2}{2a}+\frac{J^2}{2b}.           \tag{5}
$$
The material and fluid contributions are separately defined by the same velocities:
$$
 K_b=\tfrac12m(u^2+v^2)+\tfrac12I_b\omega^2,\qquad
 K_f=\tfrac12D(pu^2+qv^2)+\tfrac12I_f\omega^2,
 \qquad K=K_b+K_f.
$$
Their initial values are $mJ^2(a^{-2}+b^{-2})/2$ and
$DJ^2(pa^{-2}+qb^{-2})/2$, respectively, and sum to (5). They need not be individually conserved as the flow exchanges energy with the body. Since the pre-state was at rest, the preparation supplies the finite kinetic energy $K_0>0$. This is an energy jump of the ideal preparation; no ambiguous product of a delta force with a discontinuous velocity is used to define work. It is not a claim about actuator energy, recovery, reset cost or efficiency.

The total spatial linear Noether impulse is
$$
                         P=R(\theta)(au,bv)=(J,J).          \tag{6}
$$
For the cross product of planar vectors use $x\times P=x_1P_2-x_2P_1$. Invariance under a simultaneous spatial rotation of $x$ and body orientation gives the angular Noether impulse about the fixed initial origin:
$$
                         L_O=I\omega+x\times P.           \tag{7}
$$
Direct differentiation checks every term:
$$
 \frac d{dt}(x\times P)=\dot x\times P
 =(u,v)\times(au,bv)=(b-a)uv,
 \qquad \frac d{dt}(I\omega)=(a-b)uv.
$$
Thus $L_O$ is constant and, from (2) and $x(0)=0$, equals zero. In particular
$$
 x(t)\times P=-I\omega(t),\qquad
 \frac{I\nu}4\cos\tfrac1{16}
 \leq x(T)\times P\leq\frac{I\nu}4.
$$
The intrinsic generalized spin is negative and its orbital counterpart positive. During the finite interval $uv>0$, so their rates have these opposite signs as well. The central external impulse supplied no angular impulse about the origin; the free motion redistributes the coupled system's intrinsic and orbital contributions.

Here $P$, $I\omega$, and $L_O$ are precisely the finite generalized Kirchhoff/Noether quantities derived from the reduced body-plus-fluid kinetic action. The orbital term is about the fixed spatial origin; the intrinsic term uses the instantaneous body centre. Material intrinsic spin is only $I_b\omega$, and bare-body linear momentum is only $m\dot x$. Neither is being substituted for the coupled quantities. The fluid additions are responses of a spatially varying potential field, not a rigid fluid parcel. No unspecified integral $\int_{\mathbb R^3\setminus B}\rho_f v_f\,dV$ or its angular analogue is asserted to converge absolutely or to equal these quantities. This avoids assigning an unjustified infinite-volume momentum to the fluid while retaining the precise conserved impulses supplied by the action.

## Dimensions, calibration and limits

Using base dimensions mass $\mathsf M$, length $\mathsf L$, time $\mathsf T$: $m,D,a,b$ have dimension $\mathsf M$; $\rho_f$ has $\mathsf M\mathsf L^{-3}$; $\ell,x$ have $\mathsf L$; $J,P$ have $\mathsf M\mathsf L\mathsf T^{-1}$; $I_b,I_f,I$ have $\mathsf M\mathsf L^2$; $L_O$ and $I\omega$ have $\mathsf M\mathsf L^2\mathsf T^{-1}$; $K$ has $\mathsf M\mathsf L^2\mathsf T^{-2}$; and $\nu,\omega$ have $\mathsf T^{-1}$. Angle, $p,q$, and the numerical sign-bound constants are dimensionless. The unit-angular-velocity potential $\psi$ has dimension $\mathsf L^2$, so $\rho_f\int|\nabla\psi|^2dV$ has rotational-inertia dimensions. The prepared observation time has dimension $\mathsf T$.

The geometry, homogeneous material mass, fluid density, same-hull actual inertias, impulse components and time standard must be supplied or calibrated independently of $\omega(T)$. The initial rest state, labelled long and transverse axes, handedness, signed angular readout, central application and absence of applied moment are also retained preparation data. These determine $\nu$ and the clock setting before reading the spin. The result is an evolution and balance certificate with supplied units, not an inverse that estimates those quantities from its own horizon.

The certificate concerns one instantaneous preparation, one finite free interval and one fresh-rest principal-axis control under the stated ideal continuum model. It makes no empirical execution claim, no viscous or container correction, no finite-duration oblique-pulse equivalence, no actuator/reset efficiency assertion, and no native DET mass, gravity, time or source-coupling derivation. Possible QR use is a conventional comparator for complete coupled-state balances: later intrinsic spin can coexist with zero external angular impulse when the retained orbital term exactly compensates it. No further dynamical extension is included.

The principal-axis control retains the same hull and impulse component $J$. It does not have the same total impulse magnitude or initial energy as the oblique trial.

## Scientific review

Classical derived the same-hull rotational Neumann energy, finite spin bound and complete kinetic/Noether balances. Its distinct scientific reviewer checked the construction and signs. An independent recipient review confirmed the complete-state, instantaneous-preparation, horizon and calibration limits. Author report SHA-256 5d1d372291fc834fd447c0a74deef8198baa9daad77e4fba5185a661ba442d36; scientific review 41b572c5a1d7cfb194f17066a5f1f12c3e0d840a83eccf7ce3821d494fc22623; recipient review ba2688b83a565909327479d5d005bf704310399684ce84981ea30ead257324f0.
