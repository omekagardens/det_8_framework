# Rod mass and stiffness from two fundamental return periods

## Result and premises

For fixed, independently supplied finite positive length L, cross-sectional area A and calibrated point attachment mass d, the two retained first positive signed-tip-state return times are compatible with the stipulated rod exactly when

$$
0<T_0<T_d<\infty.
$$

For every compatible pair define

$$
z=\frac{\pi T_0}{2T_d}\in(0,\pi/2),\qquad
c=\frac{4L}{T_0}.
$$

There is exactly one finite positive rod mass, density and Young modulus:

$$
\boxed{m=d\,z\tan z,\qquad
\rho=\frac{d\,z\tan z}{AL},\qquad
E=\rho c^2=\frac{16dL}{AT_0^2}\,z\tan z.}
\tag{1}
$$

The first period fixes the wave speed relative to length. The second period, under changed boundary inertia, fixes the ratio of distributed rod mass to attachment mass. The absolute mass comes from the independently calibrated d. The result is conditional on the supplied linear elastic dynamics, boundary realization, geometry and independent pure-fundamental preparation certificate; the two return times do not establish those premises.

The unchanged uniform rod has unknown constants rho>0 and E>0 and total mass m=rho*A*L. The two observations are separate preparations, one with no end attachment and one with the same rod and a positive point mass d connected rigidly at x=L by a massless noncompliant connector. The inertial clamp is at x=0. There is no pre-existing tip mass, damping, prestress, forcing during observation, clamp motion or gravity term. Reset and attachment work lie outside the assay and are not asserted to vanish. Each preparation has a nonzero small amplitude, is released from a displacement extremum at t=0, and is independently certified to be its own boundary problem's pure lowest positive eigenmode. Amplitudes can differ.

The only retained observations are T0 and Td, in a common calibrated time scale, at the first positive return of the signed pair (u(L,t),u_t(L,t)) to that preparation's own initial state. The scientific horizon is one full fundamental period per preparation. There is no retained waveform, other frequency, force, density, weighing or stiffness measurement.

## Supplied model, source role and energy balance

The prospective control supplies

$$
\rho A u_{tt}=EA u_{xx},\quad 0<x<L,\qquad u(0,t)=0,
\tag{2}
$$

with either EA*u_x(L,t)=0 or

$$
EAu_x(L,t)=-d u_{tt}(L,t).
\tag{3}
$$

The public source is Aydin Demir, *The fundamental frequencies of longitudinally vibrating rods carrying tip mass and transversally vibrating beams carrying tip mass by using several methods*, Cumhuriyet Science Journal 42(1), 209-217 (2021), DOI 10.17776/csj.789526, [primary source](https://dergipark.org.tr/tr/download/article-file/1270494). Only section 2.1, equations (1)-(7), supplies axial-model context. The derivation below follows (2)-(3), not an approximate frequency formula. The source's prose describes its m as mass per unit length, whereas its dimensionless attachment ratio requires total rod mass. Here rho*A has mass/length units, m=rho*A*L has mass units, and d/m is dimensionless. No transverse or approximate formula is imported.

For sufficiently regular motion let

$$
H_{\rm rod}=\frac12\int_0^L\left(\rho A u_t^2+EAu_x^2\right)dx.
$$

Multiplying (2) by u_t and integrating by parts yields

$$
\frac{dH_{\rm rod}}{dt}=\left[EAu_xu_t\right]_0^L.
\tag{4}
$$

The clamp has u_t(0,t)=0. Thus the bare rod conserves H_rod. For the loaded rod (3) gives

$$
\frac{dH_{\rm rod}}{dt}=-d u_{tt}(L,t)u_t(L,t),\qquad
\frac{d}{dt}\left(H_{\rm rod}+\frac12d u_t(L,t)^2\right)=0.
\tag{5}
$$

The minus sign in (3) is mechanically necessary: the rod exerts force -EA*u_x(L,t) on the endpoint mass, and Newton's equation for that mass is d*u_tt(L,t)=-EA*u_x(L,t). The positive attachment kinetic energy cancels the boundary flux exactly. Neither the clamp nor the free attachment connection injects work during observation. Conservation applies within each assay, not across the preparation/attachment operation. This supplied Newtonian elastic energy is not an excitation-dependent rest-mass formula.

## Spectrum, lowest branch and the first return

Temporarily let a>=0 denote the boundary mass, with a=0 for the bare preparation and a=d for the loaded one. A mode u=phi(x) cos(omega*t) satisfies

$$
-EA\phi''=\omega^2\rho A\phi,\qquad \phi(0)=0,
\qquad EA\phi'(L)=a\omega^2\phi(L).
\tag{6}
$$

More generally write lambda in place of omega^2 and allow a complex eigenfunction. Multiplication by the complex conjugate of phi and integration, using the boundary condition, gives

$$
EA\int_0^L|\phi'|^2dx
=\lambda\left(\rho A\int_0^L|\phi|^2dx+a|\phi(L)|^2\right).
\tag{7}
$$

For every nonzero eigenfunction the bracket is positive. The left side is strictly positive, since phi'=0 and phi(0)=0 would imply phi=0. Therefore every eigenvalue lambda is real and strictly positive: neither a zero mode nor a negative-frequency-squared mode exists. In particular, a zero-frequency static shape would be linear, and the clamp plus zero endpoint derivative forces it to vanish. The endpoint mass is part of the positive inertia norm, not a negative boundary-energy contribution.

Set c=sqrt(E/rho), k=omega/c>0 and z=kL. The clamp implies phi(x)=B*sin(z*x/L) with B nonzero. For a=0 the remaining condition is cos z=0, so

$$
z_{0,n}=(n+1/2)\pi,\qquad n=0,1,2,\ldots.
\tag{8}
$$

For a=d>0, substitution into (6), followed by division by EA*k, yields

$$
\cos z=\frac{d\omega^2}{EAk}\sin z
=\frac{d}{\rho AL}\,z\sin z.
\tag{9}
$$

Define mu=d/m>0. Neither sin z=0 nor cos z=0 can solve (9), so it is equivalent to

$$
\mu z\tan z=1.
\tag{10}
$$

There is one and only one root in each interval (n*pi,n*pi+pi/2), n=0,1,2,...: on each interval z*tan z increases strictly from zero to infinity, since its derivative is tan z+z*sec^2 z>0. On the intervening intervals tan z<0, so (10) cannot hold. No interval endpoint solves (9). This exhausts the positive roots and establishes that the lowest loaded root is uniquely in (0,pi/2). The lowest bare root is pi/2.

Both fundamental shapes can be chosen positive for 0<x<=L. The loaded fundamental is sin(z*x/L) with 0<z<pi/2, and the bare fundamental is sin(pi*x/(2L)). Neither has an interior node, and both have nonzero endpoint displacement. Higher roots have interior zeros. This is a property of these eigenfunctions, not a test that identifies a preparation as pure: a node-free instantaneous shape or a period pair is not the independent mode-purity certificate assumed above.

Normalize the fundamental shapes to unit endpoint value:

$$
\psi_0(x)=\sin\frac{\pi x}{2L},\qquad
\psi_d(x)=\frac{\sin(zx/L)}{\sin z}.
$$

For either mode choose a real, nonzero, sufficiently small endpoint amplitude b. The tip pair is

$$
(u(L,t),u_t(L,t))=(b\cos\omega t,-b\omega\sin\omega t).
\tag{11}
$$

Its initial value is (b,0). Equality to this signed pair requires cos(omega*t)=1 and sin(omega*t)=0, hence omega*t is a multiple of 2*pi. The least positive return is 2*pi/omega. At a half period the displacement is -b, so the pair has not returned. A higher-cycle label is excluded by the first-return convention. The assumed nonzero amplitude excludes the identically zero trace.

Consequently the retained periods are exactly

$$
T_0=\frac{4L}{c},\qquad T_d=\frac{2\pi L}{cz},\qquad
r:=\frac{T_d}{T_0}=\frac{\pi}{2z}>1.
\tag{12}
$$

## Complete inverse and strict endpoints

Necessity follows from (12): finite positive rho,E,L give c>0 and T0>0; a finite positive mass ratio gives 0<z<pi/2 and thus Td>T0. Eliminating c and z from (10)-(12) gives (1). All expressions in (1) are finite and strictly positive on the claimed domain, so any compatible parameters must equal that single triple. No root ambiguity remains because the independently certified fundamental mode fixes the lowest branch.

For sufficiency, take any finite 0<T0<Td and define (m,rho,E) by (1). Then E/rho=(4L/T0)^2 and (d/m)*z*tan z=1. On this same rod, in separate preparations, prescribe

$$
u_0(x,t)=b_0\psi_0(x)\cos\frac{2\pi t}{T_0},\qquad
u_d(x,t)=b_d\psi_d(x)\cos\frac{2\pi t}{T_d},
\tag{13}
$$

where b0 and bd are any nonzero amplitudes chosen small enough for the stipulated linear strain regime. These explicit smooth motions satisfy the PDE, their respective endpoint conditions, the initial zero-velocity extremum condition and the supplied pure-fundamental registration. Equation (11) proves their first returns are precisely the requested observations. Thus the inverse is dynamically sufficient, not just an algebraic fit. This is a mathematical preparation construction; it does not build or validate a physical mode-selection apparatus.

For finite positive L,A,d and fixed finite T0, the map r in (1,infinity) exhausts all positive finite m, decreasing continuously:

$$
\frac{m}{d}=z\tan z,\qquad z=\frac{\pi}{2r}.
$$

The endpoint distinctions are strict:

- As r decreases to 1 from above, z increases to pi/2, m/d tends to infinity and d/m tends to zero. At fixed T0, rho and E both diverge with E/rho fixed. Exact Td=T0 is impossible for finite positive m and d; d=0 would be a different preparation contract.
- As r tends to infinity, z decreases to zero and m/d is asymptotic to z^2=pi^2/(4r^2). At fixed T0, m,rho,E tend to zero while E/rho stays fixed. Every finite r>1 still gives positive parameters; infinite Td or exact zero rho,E is not admitted. The clamped system has no zero mode at any finite positive parameters.
- Td<T0, equality, a nonpositive period or a nonfinite period has no solution under the control. There is no additional upper bound on the finite ratio Td/T0.

The limiting statements hold along the specified fixed-T0 family. They do not claim that rho and E have these same limits if the bare period is varied simultaneously. The packet classifies exact observations; it supplies no error bar, stability bound or empirical resolution certificate near either endpoint.

## Explicit fixture and independent reconstruction

Choose supplied units length ell, time tau and mass M*. Set

$$
L=\ell,\quad A=\ell^2,\quad d=M_*,\quad
\rho=\frac{\pi M_*}{4\ell^3},\quad
E=\frac{\pi M_*}{4\ell\tau^2}.
\tag{14}
$$

Thus in these dimensionless units L=A=d=1, rho=E=m=pi/4 and c=1. The bare shape sin(pi*x/2) has omega0=pi/2 and T0=4. The loaded choice z=pi/4 has mu=4/pi and satisfies mu*z*tan z=1, so omegad=pi/4 and Td=8. Restoring units gives T0=4*tau and Td=8*tau.

Reconstruction from the observations alone gives z=pi*4/(2*8)=pi/4 and c=4*1/4=1; (1) returns m=pi/4, rho=pi/4 and E=pi/4 exactly. Independently, direct substitution into the loaded force boundary gives

$$
EA\frac{z}{L}\cos z
=\frac{\pi^2\sqrt2}{32}
=d\omega_d^2\sin z
$$

in the dimensionless units. The bare boundary derivative vanishes separately.

An independent energy quotient checks the loaded frequency using the unnormalized shape phi(x)=sin(pi*x/4). Its generalized modal inertia and stiffness are

$$
B=\rho A\int_0^L\phi^2 dx+d\phi(L)^2
=\frac{\pi+2}{8},
$$

$$
K=EA\int_0^L(\phi')^2dx
=\frac{\pi^2(\pi+2)}{128},\qquad
\frac{K}{B}=\frac{\pi^2}{16}=\omega_d^2.
\tag{15}
$$

For the bare shape the corresponding quotient is pi^2/4. Nonzero small amplitudes in (13) realize both first returns and have conserved positive energy (5).

## Unknown attachment calibration and units

Now remove only knowledge of the positive attachment mass, retaining the same model, known L,A and common clock, and the single attachment used in the loaded assay. For every compatible pair, z and c are still fixed by (12). All possible parameter tuples are exactly

$$
\boxed{(d,m,\rho,E)
=\left(s,\ s z\tan z,\ \frac{s z\tan z}{AL},\
\frac{16sLz\tan z}{AT_0^2}\right),\quad s>0.}
\tag{16}
$$

Equivalently, multiplying one solution's d,m,rho,E by any common factor lambda>0 leaves the entire PDE and loaded boundary invariant after cancellation of that factor. With the same amplitudes, the motions and first returns remain identical; the energies multiply by lambda. Conversely (12) fixes c,z and (10) fixes m/d, so (16) contains every solution. There is one positive scale freedom and no additional ambiguity under these premises.

For the fixture, the dimensionless tuples

$$
(d,m,\rho,E)=(1,\pi/4,\pi/4,\pi/4)
\quad\hbox{and}\quad
(2,\pi/2,\pi/2,\pi/2)
$$

both give (T0,Td)=(4,8) at L=A=1. They are distinct candidate rods and attachments consistent with the same record when d has no calibration; within each candidate the rod remains unchanged between its bare and loaded preparation. The ambiguity does not change an attachment partway through a single observation. It changes the unobserved absolute scale between candidate explanations.

Precisely which standards matter is visible in

$$
\frac{m}{d}=z\tan z,\quad
\frac{\rho AL}{d}=z\tan z,\quad
\frac{EA T_0^2}{dL}=16z\tan z,\quad
\frac{cT_0}{L}=4.
\tag{17}
$$

The dimensionless period ratio fixes m/d, or equivalently d/m. It does not fix m without a mass standard. A calibrated d fixes m from that ratio even if physical length, area or the common clock's absolute conversion is unknown. Density additionally needs the physical volume AL. Young modulus needs the geometric factor L/A and the absolute time scale as well as the mass standard; wave speed needs length and time. The full two-period observation supplies c/L and the dimensionless identities in (17), rather than creating any of these units.

For example, if numerical L,A,T values are expressed in one unknown common length conversion ell and time conversion tau, with physical area proportional to ell^2, then for fixed calibrated d the reconstructed m is invariant, rho scales as ell^(-3), c as ell/tau and E as ell^(-1)*tau^(-2). If only clock conversion is unknown, rho and m remain fixed from d and geometry, while E scales as the inverse square of that conversion. A common multiplicative clock factor preserves Td/T0; unrelated clock scales for the two preparations would violate the control and would not supply this ratio.

## Scope and stopping point

The [rotational ballast comparator](rotor_angles_and_inertia_standard.md) and [impact/casing comparator](six_casing_positions_and_total_inertial_mass.md) use distinct preparation and calibration assumptions. No predecessor formula supplies this rod spectrum or inverse.

This result separates distributed inertial mass from elastic stiffness by one supplied change in boundary inertia. It transfers an independent mass standard and relies on independently registered modal preparation. It neither derives mass from the vibration's energy nor promotes excitation to changed inertial or gravitational mass. It makes no native DET-unit, gravity, ontology, empirical calibration, physical mode-purity or practical apparatus claim. Multimode recovery, higher-mode inference, damping, transverse beams, additional attachments, numerical sweeps and software work are outside this finite packet. The specified domain/inverse, spectral and preparation checks, energy identity, fixture and missing-calibration family are complete.

## Scientific review

Classical derived the spectrum and complete inverse. Its distinct reviewer checked the boundary energy, positive branches, first-return construction and a separate fixture. An independent recipient review confirmed the modal and mass-standard transfer limits. Author report SHA-256 bfbac54bb76abd69a75a7649a598ad384cbfa90d4176d5bfccdf7dde45949ce8; scientific review ab36f26fed31243cc252a2f311b13f617a7f48e4f13c90ad78201704e6dc5c2c; recipient review ae8f842fc813c82a2013274ad9146941fd98fca49e16a775d3b7dcc8aa383f5c.
