# Central mass from two crossing clocks and opposite light rays

Two freely falling observers with distinct radial velocities pass through the same event. In the static Kottler exterior, their measured rates of change of the tides and two opposite light rays determine the central mass. With only one ray, masses differing by a factor of eight can reproduce both complete tidal histories and the individual optical readings.

Let $R$ and $H$ be the measured radial and transverse tidal relative-acceleration eigenvalues. The prescribed metric has lapse factor $f=1-2GM/(c^2r)-\Lambda r^2/3>0$, with positive central mass and nonnegative cosmological constant. The observers use calibrated proper clocks and tidal readouts. [Kottler radial geodesics and tidal coefficients, Vandeev and Semenova (2021)](https://doi.org/10.1140/epjc/s10052-021-09427-8) · [Single falling clock with a spatial gradient](central_mass_from_falling_tides_and_a_gradient.md)

## Opposite rays determine the relative boost

At the crossing, use a static orthonormal radial frame (E0,Er) only as an unobserved mathematical basis, with norms −1,+1 and Er outward. Parameterize the two future four-velocities by
$$
 U_i=c(\cosh\eta_i\,E_0+\sinh\eta_i\,E_r).
$$
Let a_i>0 be observer i's unknown optical gain, constant across directions. A common outward null vector and a common inward null vector give readings
$$
 Y_i^+=a_i\Omega_+e^{-\eta_i},\qquad
 Y_i^-=a_i\Omega_-e^{+\eta_i}, \tag{1}
$$
where Ω±>0 absorb each ray's independent normalization and the frequency convention. The contraction −g(U_i,k±) gives these signs. Each Ω is common to both observers for its own ray, with no relation or coherence required between the directions.

Define recorded ratios in the fixed observer order
$$
 \rho_+=Y_2^+/Y_1^+,\qquad
 \rho_-=Y_2^-/Y_1^-,\quad h=a_2/a_1.
$$
Then
$$
 \rho_+=he^{-\delta},\quad \rho_-=he^{+\delta},\qquad
 \boxed{\delta=\tfrac12\log(\rho_-/\rho_+),\quad
        h=\sqrt{\rho_+\rho_-}},\quad \delta=\eta_2-\eta_1. \tag{2}
$$
Both ratios must be finite and positive. This determines the signed relative rapidity and relative gain without absolute emitted frequency, calibrated relative optical gain or a static-frame velocity measurement. Individual gains and ray normalizations remain free up to common multiplicative choices.

The cancellation requires the same wavevector for both observers in each direction and direction-independent gain within each observer. Two unrelated photons of unregistered normalizations, or direction-dependent gains, would not obey (2). The known tidal-clock standard is separate from these unknown optical readout gains.

## Temporal projections reconstruct a spatial gradient

The radial tides must agree at the common event:
$$
 p_1=p_2=p>0,\quad b_1=b_2=b\ge0,\quad
 p=(R-H)/3=GM/r^3,\quad b=(R+2H)/3=\Lambda c^2/3.
$$
Let d_i=dp/dτ_i be the calibrated signed proper-time slopes. Write j_i=n_i(p) for the outward derivative in observer i's rest frame. The radial Lorentz transformation is
$$
 U_2=\cosh\delta\,U_1+c\sinh\delta\,n_1,\quad
 n_2=(\sinh\delta/c)U_1+\cosh\delta\,n_1.
$$
For δ≠0 it gives the missing derivative directly:
$$
 \boxed{j_1=\frac{d_2-\cosh\delta\,d_1}{c\sinh\delta}},\qquad
 j_2=(\sinh\delta/c)d_1+\cosh\delta\,j_1. \tag{3}
$$
The units of j_i are inverse length times inverse time squared. This is not a finite-difference use of the observers' separation: they are co-located and supply two different timelike projections.

Their invariant gradient norm is
$$
 \mathcal N=j_1^2-d_1^2/c^2
 =\frac{d_1^2+d_2^2-2\cosh\delta\,d_1d_2}
             {c^2\sinh^2\delta}. \tag{4}
$$
In the supplied static patch, ∂r p=−3p/r and the gradient is radial spacelike, so N=9p²f/r²>0. The one-observer gradient relation therefore yields
$$
 \mathcal Q=\frac{\mathcal N}{9p^2}+\frac{2p+b}{c^2}=\frac1{r^2},
\qquad
 \boxed{r=\mathcal Q^{-1/2},\quad
 M=\frac{p}{G\mathcal Q^{3/2}},\quad \Lambda=3b/c^2.} \tag{5}
$$
This fixes the central metric mass without a separately measured radial baseline, direct spatial derivative, launch energy or support acceleration. Calibrated proper-time/tidal units and the imported c,G remain dimensional standards.

## Compatibility and actual crossing worldlines

For a local exact nondegenerate record, necessary and sufficient conditions are common feasible p,b, finite positive ρ± with δ≠0, and
$$
 \mathcal N>0,\qquad j_1<0. \tag{6}
$$
The outward sign matters. These inequalities imply j1<−|d1|/c and also j2<0, with the same positive N in both frames. Q is then positive.

To prove sufficiency in the actual metric, use (5) and construct
$$
 \dot r_i=-rd_i/(3p),\qquad e_i=-rj_i/(3p)>0,\qquad
 f=1-\frac{(2p+b)r^2}{c^2}
   =\frac{r^2\mathcal N}{9p^2}\in(0,1).
$$
They satisfy e_i²−dot r_i²/c²=f. The derived transformations give
$$
 e_2=\cosh\delta\,e_1+(\sinh\delta/c)\dot r_1,\quad
 \dot r_2=\cosh\delta\,\dot r_1+c\sinh\delta\,e_1,
$$
so the relative rapidity is indeed the measured δ, not a separately invented velocity. Radial geodesic initial-value problems through one common r,t and angular position, with these tangents and dot t_i=e_i/f, yield future timelike solutions on a sufficiently small common static neighbourhood. They have distinct velocities for δ≠0 and hence form a genuine crossing. Choose any a1>0, a2=h a1 and suitable positive ray normalizations; these realize the optical ratios. Thus both the gravity and optical portions have explicit physical-model witnesses.

If complete histories are also supplied, each must satisfy the single-observer history test u_i=−dot p_i/(3p_i), dot u_i+u_i²=b−p_i with constant common b. The recovered M must lie inside both full-interval static-patch bounds. Then r_i(τ_i)=[GM/p_i(τ_i)]^(1/3), the constant e_i and integrated static times with the same crossing origin reproduce both histories. No orbit fit is required.

If N≤0, even a formally positive Q does not rescue the record: it fails the strictly static spacelike-gradient premise. N=0 is the excluded f=0 boundary. A wrong j1 sign fails the registered outward direction. Unequal-velocity data with d1=d2, including both slopes zero, cannot satisfy (6).

When δ=0, the rays give only ρ+=ρ-=h. Compatibility requires d1=d2. Equal future radial velocities at the same event are the same tangent; geodesic uniqueness makes the two worldlines locally identical, rather than an isolated crossing with distinct velocities. If such comoving devices are allowed, they duplicate the old one-observer information and leave its mass-scale ambiguity. If the record additionally asserts a genuine distinct-velocity crossing, δ=0 rejects that assertion. Differing full histories at aligned proper origins would likewise fail geodesic compatibility in this case.

A single observer turning at the crossing causes no singularity when δ≠0; only the relative-boost denominator is divided out. Near δ=0 the exact inverse may be poorly conditioned; at fixed p,b, N approaching zero approaches the excluded patch boundary. No positive uniform error margin or practical detector precision is inferred from exact identification.

## A one-ray collision preserving both complete histories

One direction alone gives ρ+=h e^(−δ). An unknown positive h can absorb a change in δ. The following construction preserves the entire measured time functions and has a true crossing with distinct radial velocities.

Fix a time standard τ0>0, Λ=0 and windows |τ_i|≤τ0/4, with the crossing tagged τ1=τ2=0. For each μ=GM define e1=e2=1 and
$$
 r_1(\tau_1)=(9\mu/2)^{1/3}(\tau_0-\tau_1)^{2/3},\qquad
 r_2(\tau_2)=(9\mu/2)^{1/3}(\tau_0+\tau_2)^{2/3}.
$$
These are infalling and outgoing radial geodesics, with dot r_i=∓√(2μ/r_i). Choose static-time integration constants t1(0)=t2(0)=0 and the same angular position; they cross at the same event. The full tidal histories are
$$
 p_1(\tau_1)=2/[9(\tau_0-\tau_1)^2],\quad
 p_2(\tau_2)=2/[9(\tau_0+\tau_2)^2],\quad b=0,
$$
independent of μ. At the crossing p=2/(9τ0²) and (d1,d2)=(4/(9τ0³),−4/(9τ0³)).

Take precisely these two worlds:

| Quantity | A | B |
| --- | --- | --- |
| μ | 3c³τ0/32 | 3c³τ0/256 |
| Crossing radius | 3cτ0/4 | 3cτ0/8 |
| Static-frame velocities divided by c | (−1/2,+1/2) | (−1/4,+1/4) |
| Relative δ | log 3 | log(5/3) |
| Optical gains (a1,a2) | (1/√3,√3) | (√(3/5),√(5/3)) |
| Retained outward ratio ρ+ | 1 | 1 |
| Unretained inward ratio ρ− | 9 | 25/9 |

Both obey μ<3c³(3τ0/4)/4, which ensures r_i>2μ/c² throughout both complete windows. Their timelike normalization and geodesic equations are the exact radial solution with e=1, with the outgoing sign added by reversal of the radial motion. Distinct velocities and positive lapse hold at the common crossing; no limiting or nonphysical worldline is used.

For a fixed positive Ω+, the gains in the table are a_i=e^(η_i). Equation (1) then gives both raw outward readings Y1+=Y2+=Ω+ in both worlds. Thus even retaining the two separate outward amplitudes, rather than just their ratio, does not break this example. The gains are constant across directions within each world, as required. Their unknown values differ between compatible worlds; no known clock or calibration is changed. No relation between Ω+ and the unmeasured Ω− is assumed.

The masses differ by a factor of eight. Every retained tidal reading at every proper time, the genuine crossing tag and the whole one-ray optical record agree. The two opposite-direction records would distinguish them, through ρ−, and recover their different masses by (2)–(5). More dense time sampling or more exact knowledge of these same time functions cannot supply the missing relative optical calibration.

## Observation and unit boundaries

The earlier four-ray diamond observable involves propagation between different events and a residual gain combination. Here both observers sample each ray at the same event; local Doppler factors have opposite signs in the two directions, enabling the cancellation. No integrated-curvature record, remote clock comparison, common emitted frequency or phase-coherent relay has been added.

The invariant N has units length⁻² time⁻⁴; Q has length⁻², r is a length and M is the supplied central metric mass. Λ is already fixed by the common tides. The static rapidities in the proof are not observed inputs. Proper-clock calibration, the radial frame and local light-speed standard supply the normalization needed to convert two temporal projections into the inferred spatial norm. Absolute optical gain remains unnecessary under the stated shared-direction response.

Physical implementation still needs registered coincidence, two correctly identified opposite common wavevectors, stable per-observer gain across directions, calibrated tidal slopes on separate proper clocks, orientation, repeatability and error/backreaction control. A finite baseline, nonradial motion, direction-dependent gain or uncertain coincidence requires another contract. The mass inverse is conditional on this geometry, the proper-clock standard and calibrated $G,c$.
