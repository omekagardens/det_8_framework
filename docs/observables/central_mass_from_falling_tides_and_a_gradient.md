# Central mass from a falling clock's tides and one spatial derivative

**Result.** The complete calibrated tidal history on the stipulated finite radial free fall does not identify the central mass. There is an exact continuous family of different positive masses and genuinely varying admissible worldlines with the same proper-time record. A single co-located outward spatial derivative of the invariant tidal amplitude, combined with its already recorded proper-time derivative, fixes the missing radius and central metric mass. The spatial derivative must be in the instantaneous comoving orthonormal frame; replacing its boost factor by the static-frame factor gives the wrong inverse.

This is a conditional analytic Kottler comparison, not a detector, native mass calibration or empirical gravitational result.

The exterior metric, radial geodesics and freely falling tidal coefficients are supplied by the Kottler model. The calculation uses physical proper time and restores the factors of $c$ and $G$. [Vandeev and Semenova, equations 2–3, 8–11, 16 and 19–21](https://doi.org/10.1140/epjc/s10052-021-09427-8) · [Single-site support comparison](local_mass_from_tides_and_support.md) · [Two-site clock comparison](two_site_tides_and_radar_mass.md)

## Radial motion and the time record

Write μ=GM and b=Λc²/3. The supplied exterior and dimensionless future Killing energy e obey
$$
 ds^2=-f c^2dt^2+f^{-1}dr^2+r^2d\Omega^2,\quad
 f=1-\frac{2\mu}{c^2r}-\frac{br^2}{c^2}>0,
$$
$$
 e=f\dot t>0,\qquad
 \dot r^2=c^2(e^2-f),\qquad
 \ddot r=-\mu/r^2+br. \tag{1}
$$
Dots mean the same calibrated onboard proper time τ. These equations include turns; the second-order radial equation is not obtained by dividing by a possibly zero radial speed.

The recorded radial and transverse relative-acceleration eigenvalues are
$$
 R=2p+b,\quad H=-p+b,\qquad
 p=\frac{R-H}{3}=\frac{\mu}{r^3}>0,\quad
 b=\frac{R+2H}{3}\ge0.
$$
The radial free-fall coefficients do not require the observer to be momentarily at rest. The clock record determines b, hence Λ=3b/c², and the density-like tidal combination p(τ), not M and r separately.

Define
$$
 u=-\dot p/(3p)=\dot r/r.
$$
Equation (1) implies
$$
 \dot u+u^2=b-p. \tag{2}
$$
Thus the history determines the radius ratios r(τ)/r(τ0)=[p(τ0)/p(τ)]^(1/3) and fractional radial rate, including the direction of motion. It does not independently measure a spatial distance or absolute radial velocity.

For exact arbitrary proposed histories, necessary time-record conditions are p>0, constant b≥0, sufficient differentiability and (2). They are also sufficient for some admissible scale on the compact interval I. For any candidate μ>0 put r=(μ/p)^(1/3) and
$$
 e^2=1+\frac{r^2}{c^2}(u^2-2p-b).
$$
The right side is constant: differentiating r²(u²−2p−b) using (2) and dot p=−3pu gives zero. The constructed radius satisfies the second-order radial equation. Precisely the scales
$$
 0<M<M_*,\qquad
 M_*=\frac{c^3}{G}\min_{\tau\in I}
               \frac{p(\tau)}{[2p(\tau)+b]^{3/2}} \tag{3}
$$
keep f>0 throughout I. The minimum exists and is positive on the finite compact interval. At such a scale e²=f+dot r²/c²>0. Choose the positive e and integrate dot t=e/f; this supplies a future timelike geodesic with norm −c². Conversely every realization must have this radius, energy and patch condition.

Equation (3) is a sharp open mass interval within this record/model contract. Its upper restriction comes from requiring the entire observed segment to remain in the static patch; it is not a measured boundary crossing or a unique mass. The time record can therefore constrain scales without identifying one. It also fixes the combination
$$
 (e^2-1)/\mu^{2/3}
   =(u^2-2p-b)/(c^2p^{2/3}),
$$
rather than separately fixing e and μ.

## Exact collision on actual moving geodesics

Starting with any admissible varying-radius realization, choose 0<s<1 and set
$$
 M_s=s^3M,\quad r_s(\tau)=s\,r(\tau),\quad
 \Lambda_s=\Lambda,\quad
 e_s^2=1+s^2(e^2-1).
$$
Then p_s=p and b_s=b at every identical proper-time tag. Along the rescaled worldline,
$$
 f_s(r_s)=1-s^2(1-f)>0,\qquad
 e_s^2-f_s=s^2(e^2-f)=\dot r_s^2/c^2.
$$
Both e_s² and f_s are positive. Also ddot r_s=(b−p)r_s, so the radial geodesic equation is preserved. Integrating dot t_s=e_s/f_s supplies the new unobserved static time. The normalization, full geodesic motion, future direction and static patch all hold, not merely the algebraic tidal ratio. The same elapsed proper time and all R,H readings are preserved, while the mass changes. No physical units or clock rates were rescaled.

For an explicit genuinely infalling segment take Λ=0, e=1, a compact interval [τa,τb] with τc>τb and
$$
 0<\mu<\frac34c^3(\tau_c-\tau_b),\qquad
 r_\mu(\tau)=(9\mu/2)^{1/3}(\tau_c-\tau)^{2/3}.
$$
Direct differentiation gives dot r=−√(2μ/r), ddot r=−μ/r² and
$$
 p(\tau)=\frac{2}{9(\tau_c-\tau)^2},\qquad b=0.
$$
The displayed μ bound ensures r>2μ/c² over the entire interval. The masses μ/G and μ/(8G) have radii r and r/2, both e=1, and exactly the same nonconstant tidal history. e=1 here is an admissible local geodesic choice, not an observed launch reference at infinity. These are two different central masses in the same fixed clock, G and c units.

## What the comoving spatial derivative supplies

At a present event let j=n(p) be the measured directional proper-length derivative, with n the outward radial unit spacelike vector orthogonal to the observer's four-velocity. For U=dot t ∂t+dot r ∂r and (1), that vector is
$$
 n=\frac{\dot r}{c^2f}\partial_t+e\,\partial_r.
$$
It has g(n,n)=1, g(U,n)=0 and positive radial component e. It is the outward radial axis of the instantaneous comoving frame. Along radial geodesic motion this radial orthonormal axis is parallel transported.

Because p is a static spherical invariant,
$$
 j=e\,\partial_rp=-3ep/r<0,\qquad
 \dot p=\dot r\,\partial_rp=-3p\dot r/r. \tag{4}
$$
The spatial factor is e, not √f; those coincide only when dot r=0. A static-frame radial derivative would be −3p√f/r and is a different measurement. This is the required boost correction.

Put k=−j/(3p)>0 and retain u=−dot p/(3p). Dividing the timelike normalization by r² yields
$$
 \mathcal Q:=k^2+\frac{2p+b-u^2}{c^2}=\frac1{r^2}.
$$
Equivalently,
$$
 \mathcal Q=
 \frac{j^2-\dot p^2/c^2}{9p^2}
 +\frac{2p+b}{c^2}. \tag{5}
$$
The difference j²−dot p²/c² is the spacelike norm of the gradient of p, not an unregistered spatial sample inferred from elapsed time.

The supplemented record therefore has the unique reconstruction
$$
 \boxed{\displaystyle
 r=\mathcal Q^{-1/2},\quad
 M=\frac{p}{G\mathcal Q^{3/2}},\quad
 \Lambda=\frac{3b}{c^2},\quad
 \dot r=\frac{u}{\sqrt{\mathcal Q}},\quad
 e=\frac{k}{\sqrt{\mathcal Q}}.} \tag{6}
$$
No starting radius, support acceleration or independently known Killing energy is used.

## Compatibility, turns and static balance

At a single event the strict local conditions are p>0, b≥0, j<0 and
$$
 |\dot p|<c|j|. \tag{7}
$$
They make k²−u²/c²>0 and Q>0, and the reconstruction gives
$$
 f=(k^2-u^2/c^2)/\mathcal Q\in(0,1),\qquad
 e^2-\dot r^2/c^2=f.
$$
These conditions are necessary and sufficient for a local radial timelike state with the specified p,b,dot p,j in this metric class: (6) explicitly constructs it, and the radial geodesic initial-value problem then has a local solution. Equality in (7) is the excluded f=0 case. A zero or positive j is inconsistent with the registered outward derivative of positive μ/r³ in the static patch.

For the entire supplemented history, require the time-history conditions above, including (2), and the mass from (6) to lie in (3). These are sufficient: r(τ)=[GM/p(τ)]^(1/3) and the constructed constant e reproduce the whole tidal history as already proved, and (4) reproduces the spatial datum at its event. No orbit fit is needed. A local spatial datum alone does not guarantee that an arbitrary later history remains in the patch. On compatible observations the added datum fixes exactly one previously free scale.

At an ordinary turning event dot r=dot p=u=0,
$$
 \mathcal Q=k^2+(2p+b)/c^2,\qquad
 \ddot p=3p(p-b).
$$
The inverse remains regular; it never divides by dot p. If p=b at a turn, radial uniqueness gives the static-balance geodesic. A constant history is compatible with such a geodesic precisely at b=p>0. Without j it retains 0<r<c/√(3p) and its continuous positive mass interval. With j<0,
$$
 r=[j^2/(9p^2)+3p/c^2]^{-1/2}
$$
fixes the radius and mass even there. All geodesics have zero proper acceleration; that zero is not a substitute for the different static support-acceleration channel in the prior paper.

## Calibration and observation limits

The quantities R,H,p,b have inverse-time-squared units, dot p inverse-time-cubed, j inverse-length times inverse-time-squared, Q inverse-length-squared, r length, dot r speed and e dimensionless. The mass in (6) is the central metric mass in the supplied exterior, not a redshifted lens mass, an internal constituent inertia or energy measured by the observer.

The time arm requires calibrated proper time, tidal response and parallel radial/transverse axes; c and G are supplied standards. It identifies Λ in calibrated inverse-length-squared units and the combinations/bounds above, while a longer record on an admitted finite interval still leaves a nontrivial scale family. No launch radius or boundary information is smuggled in.

The supplemental channel supplies an independent spatial proper-length derivative at the same event and in the moving observer's rest space. Replacing it by a finite-baseline estimate requires an additional preparation, simultaneity, transport and error model. Repeated onboard time samples alone give dot p=dot r ∂r p with unregistered dot r, not j. The exact rescaling collision proves that time resolution alone cannot repair that missing registration under this contract.

A physical protocol would need qualified tidal/gradient instrumentation, probe separation and backreaction control, clocks, axes, signal retention and uncertainty accounting. Numerical differentiation and near-boundary error amplification are not resolved by an exact inverse; no finite-error guarantee or detector qualification is claimed. Matched alternatives receive the same data and calibration. The supplied Kottler law and its time/length/mass standards are not derived from DET order counts, and no native–continuum or empirical gravity correspondence is established.
