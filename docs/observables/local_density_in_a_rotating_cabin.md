# Local density from free probes in a rotating cabin

Two signed, nonparallel launches at the cabin origin determine its instantaneous angular velocity. Subtracting the resulting centrifugal contribution from the sum of the three displaced rest readings gives the local Poisson density. With only the first launch, compatible readings give a sharp lower bound and allow every density above it.

## Coordinates and acceleration

At the common measurement instant let $e_1,e_2,e_3$ be the calibrated right-handed cabin axes. Write $X=c+Qr$, with $Q$ mapping cabin components to inertial components, and use the same Newtonian time for both derivatives. Set $W=Q^\mathsf{T}\dot Q$, so $Wv=\omega\times v$ with $\omega$ in cabin components. Orthogonality makes $W$ skew and $\dot Q=QW$, hence
$$
\dot X=\dot c+Q(\dot r+Wr),\qquad
\ddot X=\ddot c+Q\{\ddot r+2W\dot r+(\dot W+W^2)r\}.
$$
Here $\dot Wv=\dot\omega\times v$. Let $T$ be the inertial derivative of the affine field $g$ and $S=Q^\mathsf{T}TQ$ its representation in the cabin triad. Field conservativity makes $S$ symmetric, and the supplied Newtonian Poisson law gives $\operatorname{tr}S=-4\pi G\rho$. Unit passive-to-inertial response means $\ddot X=g(X)$ for each free probe. Using the exact spatial affinity on the common neighbourhood gives the cabin coordinate acceleration at position $r$ and cabin velocity $v$,
$$
a(r,v)=b+(S-\dot W-W^2)r-2Wv,\qquad b=Q^\mathsf{T}[g(c)-\ddot c].
$$
The origin rest preparation has $a(0,0)=b$. Every reported difference cancels this same vector, including the entire translational acceleration.

Denote the three normalized longitudinal readings by $d_i=e_i\cdot[a(Le_i,0)-a(0,0)]/L$; write $D=d_1+d_2+d_3$. The Euler contribution has zero longitudinal projection because $e_i\cdot\dot W e_i=0$, even for changing angular velocity. The double cross product gives $-W^2=|\omega|^2 I-\omega\omega^\mathsf{T}$, so
$$
d_i=S_{ii}+|\omega|^2-\omega_i^2,\qquad
D=\operatorname{tr}(S-\dot W-W^2)=-4\pi G\rho+2|\omega|^2.
$$
Thus the measured trace is the trace of the *coordinate-acceleration derivative at rest* in the cabin. Rotation adds $2|\omega|^2$ to the gravitational trace. Spatial affinity makes the readings exact for the supplied finite $L>0$.

## Six preparations

Write $p=a(0,Ue_1)-a(0,0)$ and $q=a(0,Ue_2)-a(0,0)$ for the signed launch differences. Write $\omega=(x,y,z)$. The velocity term gives all six components,
$$
p=2U(0,-z,y),\qquad q=2U(z,0,-x).
$$
For arbitrary finite readings and known $U>0$, the complete vector tests are
$$
p_1=0,\qquad q_2=0,\qquad p_2+q_1=0.
$$
On this branch the common angular velocity is unique,
$$
x=-q_3/(2U),\qquad y=p_3/(2U),\qquad z=-p_2/(2U)=q_1/(2U).
$$
The remaining test is $D\le 2(x^2+y^2+z^2)$. Failure of any test gives an empty model set. When all pass, the unique density and the three gravitational diagonal entries are
$$
\rho=\frac{2|\omega|^2-D}{4\pi G},\qquad
S_{ii}=d_i-|\omega|^2+\omega_i^2 .
$$
A strict inequality certifies positive density, and equality certifies local vacuum. Each of the three independent symmetric off-diagonal entries of $S$ is free. The record gives these diagonal entries and angular velocity in the cabin triad. The absolute inertial orientation, field offset, translational acceleration and instantaneous angular acceleration can be freely chosen in the realization below.

## Five preparations

Retain $p$ and all $d_i$; omit $q$ in its entirety. If $p_1\ne0$, the density set is empty. Otherwise $y=p_3/(2U)$ and $z=-p_2/(2U)$ are fixed and $x$ is free. Put $s=y^2+z^2$ and $C=2s-D$. The trace condition becomes $4\pi G\rho=C+2x^2$. The exact set is
$$
\boxed{\quad \rho\in\left[\max\!\left(0,\frac{C}{4\pi G}\right),\ \infty\right).\quad}
$$
Necessity follows from $x^2\ge0$ and $\rho\ge0$. For any member of the interval choose $x=\pm\sqrt{(4\pi G\rho-C)/2}$. This also proves attainability of the lower endpoint. For $C>0$ the minimum is strictly positive and requires $x=0$. For $C=0$, $x=0$ realizes vacuum. For $C<0$, $x=\pm\sqrt{-C/2}$ realizes vacuum. Every compatible record allows arbitrarily high density, since there is no bound on the unmeasured spin component. A negative or zero value of $C$ therefore permits both vacuum and positive density.

## One field and one frame for each fit

Take the measurement at $t=0$, $c(0)=0$ and $Q(0)=I$, aligning the inertial basis with the instantaneous cabin triad. Choose the recovered $\omega$ for a complete record, or the constructed $(x,y,z)$ for a specified reduced-record density. Set $S$ symmetric with the diagonal above and arbitrary symmetric off-diagonals. For any constant $f$, the local potential and its field
$$
\Phi(X)=\Phi_0-f\cdot X-\tfrac12 X^\mathsf{T}S X,\qquad
g(X)=-\nabla\Phi=f+SX
$$
hold on an open ball containing the four distinct positions. The Laplacian is $-\operatorname{tr}S=4\pi G\rho$ throughout that ball. A common rigid rotation with any prescribed instantaneous angular acceleration is $Q(t)=\exp(tW+\tfrac12t^2 A)$ for arbitrary skew $A$. This real rotation has $\dot Q(0)=W$ and $\ddot Q(0)=A+W^2$, giving $\dot W(0)=A$ in the kinematic formula. A common translation $c(t)=tv_c+\tfrac12t^2a_c$ allows any translational velocity and acceleration at the instant. A fixed inertial rotation of the entire construction gives any desired initial orientation.

For each listed cabin preparation $(r,v)$ set the inertial initial data $X(0)=r$, $\dot X(0)=v_c+v+Wr$. In particular the displaced cabin-rest probes carry the inertial velocity $v_c+Wr$; the launch probes have the stated cabin velocities at the origin. The smooth affine field gives each initial condition a local solution of $\ddot X=g(X)$. The probes can be negligible and noninteracting, or prepared in separate copies matched to this same field and frame state. Substitution returns every reported $d_i$ and launch vector simultaneously at $t=0$, for six preparations or the five retained. This proves sufficiency of the tests, including when an inferred density vanishes. The potential provides a local Poisson realization. A global isolated-source distribution with boundary conditions is a separate problem.

## An explicit common reduced record

Take any rate $\nu>0$, fixed $L,U,G>0$, and the synthetic readings
$$
(d_1,d_2,d_3)=(\nu^2,\nu^2,0),\qquad p=(0,-2U\nu,0).
$$
Here $D=2\nu^2$, $s=\nu^2$, $C=0$. With $\omega=(0,0,\nu)$ choose $S=0$. The centrifugal diagonal is $(\nu^2,\nu^2,0)$ and the local density is zero. With $\omega=(\nu,0,\nu)$ choose $S=\operatorname{diag}(0,-\nu^2,-\nu^2)$. The centrifugal diagonal is now $(\nu^2,2\nu^2,\nu^2)$; adding the gravitational diagonal returns exactly the same three readings. Both spins give the same $p$, while the second field has $\rho=2\nu^2/(4\pi G)>0$. Each fit may take $A=0$, $c=0$ and $f=0$ above. Restoring the omitted launch would yield $q=(2U\nu,0,0)$ in the vacuum fit and $q=(2U\nu,0,-2U\nu)$ in the positive-density fit.

## Scope of the inference

These are externally supplied *coordinate* accelerations in the cabin axes at one common instant. The calculation assumes a registered orthonormal triad, calibrated ruler, clock, signed $U$, known $G>0$, a common frame and field, and negligible free probes. The $d_i$ have units of inverse time squared, $p,q$ of acceleration, and $\omega$ of inverse time. Dividing the corrected trace by $G$ gives mass per volume. These calibrations and the Newtonian laws enter as premises. The proof supplies a conditional comparator for QR and leaves instrument calibration, native units and physical validation open.

CL018 supplies the inertial trace observation for two prescribed quadratic fields. CL076 illustrates why finite displacements in a nonaffine field can fail to report the central derivative. CL085 separates rotating-camera and fluid motion in a different observation. This packet adds the rigid-cabin kinematics and the local affine field class. The selection had already suggested the Coriolis and centrifugal terms and the undetermined spin component. The component tests, sharp set and synthetic realization above follow analytically from the frozen preparations. The scientific horizon is the shared observation instant. Administrative elapsed time does not enter the inverse.

## Recipient applicability

**Finite baseline.** See [the finite-baseline comparator](finite_baseline_and_central_density.md). The three differences equal derivative entries because the entire donor field is affine over the measured neighbourhood. The recipient’s ball-and-eight-corners model has a nonlinear exterior-mass contribution. Its corner field has zero infinitesimal central gradient and nonzero finite axial response. The six compatible axial readings there give a central-density interval whose upper endpoint is the finite-trace report; an additional registered component resolves that model’s two amplitudes. Correcting the cabin’s rotation cannot supply the missing spatial field relation. Applying CL096 to finite arms requires independent exact affinity, or a justified error bound converting those differences to local derivatives. The source-specific interval from the finite-baseline note cannot be combined directly with the donor’s one-launch interval.

**Probe response and acceleration gain.** See [the paired probe-response comparison](paired_probe_response_and_acceleration_gain.md). The recipient’s paired clock and motion record determines the active source scale and the product of acceleration gain with probe response. That identification does not certify either factor separately. In the cabin derivation, a constant positive response $\beta$ in $\ddot X=\beta g(X)$, with physical coordinate accelerations otherwise calibrated, would replace the inferred density by $\beta\rho$. The velocity differences would still determine cabin rotation. Unit response or independently known $\beta$ is therefore required for the quoted density magnitude. A positive inferred product can still certify positivity under a positive response, while a numerical lower bound on $\rho$ requires a corresponding upper bound on that response.

An unknown display gain is a further issue. If it multiplies all physical acceleration differences by $k>0$ while the launch speed is independently known, the naive launch inversion yields $k\omega$, whereas the rest trace is $kD$. The squared centrifugal correction and the displayed trace therefore scale differently. It is essential to recover physical accelerations before applying the density formula. Calibrating a gain by assuming the same probe has unit response would repeat the recipient’s response/gain ambiguity. Neither a shared display scale nor the native source contrast supplies that calibration.

**Relativistic tides.** See [the orbit and tidal inverse](local_density_and_pressure_from_orbit_and_tides.md). The accepted spherical result uses a signed orbital record and infinitesimal Jacobi readings in two registered velocity frames, including an affine sensor calibration from the polar readings. Those data determine separate curvature components and, through Einstein’s equations, the local energy density and both pressures. The Newtonian cabin’s acceleration-coordinate transformation is an appropriate conventional frame check within its own assumptions. It is not the general transformation law for those finite-velocity relativistic curvature components.

For comparison using the recipient’s sign convention, a complete local sum of stretching-positive geodesic-deviation coefficients in one comoving orthonormal frame is $-c^2R_{00}$. With its zero cosmological term and diagonal stress this equals $-4\pi G(\epsilon+p_r+2p_t)/c^2$. Thus interpreting that trace as $-4\pi G\epsilon/c^2$ would require a justified negligible-pressure limit. The spherical orbit/tide inverse recovers $\epsilon$ through its additional components. Its common event, free-fall, tetrad, time, infinitesimal-separation and finite-arm qualifications remain required for a recipient measurement.

All donor slopes have inverse-time-squared units, its launches acceleration units, and its angular velocity inverse-time units. Known length, clock and $G$ convert the corrected trace to mass per volume. This is the source density in the supplied Poisson law. Constituent rest inventory, inertial source mass, empirical resolution and DET-native length or time need their own physical links. This recipient decision adds no measurements or finite-error model.
