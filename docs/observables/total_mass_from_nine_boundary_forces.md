# Total inertial mass from nine summed boundary-force readings



Impose the same known constant acceleration $a\ne0$ on both terminals while preserving their equilibrium separation. For a connected, ungrounded Hooke network with positive point masses and at most two internal degrees of freedom, the nine exact actuator-on-network force sums $F_n$, at $n\Delta$ for $n=0,\ldots,8$, determine the sum of **all** constituent masses. The needed timing condition is $e^{i\omega\Delta}\ne1$ for every force-visible internal frequency. The inverse below uses one real linear system with five unknowns and does not need either frequency. A pair of networks with the same springs shows how identification fails when this timing condition is dropped.

## Force balance under a common translation

Use inertial displacements $u_i(t)$ from an equilibrium configuration. The terminal displacements are $u_L=u_R=X(t)$, with $\ddot X=a$. Let $M$ be the positive diagonal mass matrix, $K$ the weighted spring Laplacian, and $f$ the vector of external forces, supported only at the two terminals. Newton's law gives $M\ddot u+Ku=f$ and $K\mathbf1=0$. Write $u=X\mathbf1+y$, so $y_L=y_R=0$. For the internal index set $I$ the equations become
$$
 M_I\ddot y_I+K_{II}y_I=-aM_I\mathbf1_I .
$$
For nonempty $I$, $K_{II}$ is positive definite: its quadratic form is the sum of $k_{ij}(y_i-y_j)^2$ on edges after extending $y$ by zero at the terminals. Vanishing forces the extension to be constant by connectedness and therefore zero. There is a static offset $y_*=-aK_{II}^{-1}M_I\mathbf1_I$. Subtracting it leaves a homogeneous oscillator with real symmetric positive definite mass-normalized stiffness $M_I^{-1/2}K_{II}M_I^{-1/2}$. Thus arbitrary finite opening positions and velocities contribute sines and cosines at at most two positive internal frequencies. Repeated eigenvalues are diagonalizable and create no terms growing linearly in time.

Summing the original equations cancels all internal spring forces. If $M_{\rm tot}=\sum_i m_i>0$, the signed measurement is
$$
 F(t)=f_L+f_R=M_{\rm tot}a+\mathbf1_I^{\mathsf T}M_I\ddot y_I.
$$
The static offset has zero acceleration. Each remaining mode enters only through its projected acceleration; a zero projection or an unexcited mode contributes nothing. With no internal masses the sum is exactly $M_{\rm tot}a$ at every time. No assumption of initial internal rest or known opening phase was used.

## Finite recovery from the nine samples

After sampling, merge identical complex roots and omit terms with zero net amplitude. With $z=e^{\pm i\omega\Delta}$, every physical record in the stated class has the form
$$
 F_n=M_{\rm tot}a+\sum_{z\in Z}b_z z^n,\qquad |Z|\le4,\quad z\ne1 .
$$
The sum is real by conjugacy. Different frequencies may give the same sampled root or the same conjugate pair. At $z=-1$ only the alternating sequence survives. A completely silent record has $Z=\varnothing$. All of these cases are allowed.

1. Form the eight differences $d_n=F_{n+1}-F_n$, $0\le n\le7$.
2. Find **any** real solution $p_0,\ldots,p_4$ of
   $$
   \sum_{j=0}^4p_j=1,\qquad
   \sum_{j=0}^4p_jd_{s+j}=0\quad(s=0,1,2,3).
   $$
   Ordinary elimination suffices; free variables may be set to zero after solving the pivot equations in terms of them.
3. Return
   $$
   \boxed{\displaystyle M_{\rm tot}=\frac1a\sum_{j=0}^4p_jF_j}.
   $$
   For a constant record one may take $p_0=1$ and obtain $F_0/a$.

**Existence.** The polynomial $\prod_{z\in Z}(v-z)/(1-z)$ has real coefficients, degree at most four, equals one at $v=1$ and vanishes at every active root. Its coefficient vector, padded with zeros, solves the system because $d_n=\sum_z b_z(z-1)z^n$. The empty product is one.

**Why any solution works.** Write $P(v)=\sum_{j=0}^4p_jv^j$. Its four data equations say that $\sum_z [b_z(z-1)P(z)]z^s=0$ for $s=0,1,2,3$. The first $|Z|$ rows form a square Vandermonde matrix at the distinct roots with nonzero determinant. Hence $b_z(z-1)P(z)=0$ for each root, forcing $P(z)=0$. For $Z=\varnothing$ this condition is vacuous. With $P(1)=1$ the weighted force is exactly $M_{\rm tot}a$. This proves that the answer is independent of free coefficients, hidden frequencies and which compatible physical network produced the record.

The input supplies uniform synchronized sample spacing $\Delta>0$, the common acceleration including sign, the force direction and scale, the mode-count limit and the exclusion of an oscillation sampled as a constant. It supplies no frequency values or general sub-Nyquist band. The result concerns compatible exact records. In particular an oscillation close to unit sampled phase can be difficult to separate from a constant in finite precision.

## A physical collision at unit sampled phase

Take a three-point chain. Each terminal has mass $m>0$. The two springs have the same positive stiffness $k=8\pi^2m/\Delta^2$ in both networks. The central mass $\mu$ is $m$ in the first and $4m$ in the second. Open with every displacement and velocity zero, and impose $X(t)=at^2/2$ at both terminals. If $y$ denotes the central displacement relative to $X$, then
$$
 \omega^2=2k/\mu,\qquad
 y(t)=\frac{a}{\omega^2}(\cos\omega t-1),\qquad
 F(t)=(2m+\mu)a-\mu a\cos\omega t .
$$
The central absolute acceleration is $a(1-\cos\omega t)$, consistently with both spring forces. The two angular frequencies are $4\pi/\Delta$ and $2\pi/\Delta$. Thus the oscillation is genuinely present in each continuous force, yet $F_n=2ma$ at every tag in both records. The terminal trajectories, calibrated acceleration, timing, initial relative preparation and spring constants all agree. The total masses are $3m$ and $6m$. Equilibrium spacings may be chosen larger than the maximum relative excursion to keep the sites ordered. This collision makes the need for independent timing information explicit.

## Work, calibration and relation to CL089

For displacement from an unstressed equilibrium, the inertial-frame mechanical energy and its rate are
$$
 E=\tfrac12\dot u^{\mathsf T}M\dot u+
   \tfrac12\sum_{\{i,j\}}k_{ij}(u_i-u_j)^2,\qquad
 \dot E=\dot u^{\mathsf T}(M\ddot u+Ku)
       =f_L\dot X+f_R\dot X=F(t)\dot X(t).
$$
The potential counts each edge once and is invariant under translation. A self-balanced equilibrium prestress in the ideal linear model changes the energy reference without changing these increment equations. Boundary work over the interval is $\int_0^{8\Delta}F(t)\dot X(t)\,dt=E(8\Delta)-E(0)$; the nine force tags alone need not determine that integral or the stored internal energy. The prescribed acceleration requires an external actuator and an energy source or sink. Energy accounting for preparation, measurement and reset would require their own records.

The readout has mass units through calibrated force divided by calibrated length per time squared. An unknown common force gain would leave the absolute mass scale free: scaling every mass and spring stiffness by one positive factor preserves the motions and frequencies and scales every force by that factor. This direct assay uses two signed boundary forces and supplied kinematics. The earlier six-position assay uses an independently calibrated impulse and free recoil; the displayed-work calibration uses a registered work gain, spring and tick.

The [seven-force comparison](signed_boundary_inertance_from_seven_forces.md) drove one terminal harmonically with the other clamped and measured a static-subtracted, frequency-dependent inertance. Its supported chain gives $-19m/21$ and its diamond $7m/3$, with three positive moving masses $m$ in each case. This assay measures the complete translating mass, including **both** terminal masses. A comparison requires the same registered components or an independently measured correction for the formerly clamped terminal, fixtures and moving actuator parts. It also requires consistent force signs and units, and preservation of the donor's drive frequency and static reference when quoting its inertance. The native placement law in CL089 supplies its topology weights and inactive trials; it supplies no calibrated force or acceleration here. This is an inference under conventional mechanics, with no gravitational or native mass law derived.

[Six-position recoil measurement](six_casing_positions_and_total_inertial_mass.md) · [Spring calibration in displayed work units](spring_mass_scale_in_displayed_work.md)
