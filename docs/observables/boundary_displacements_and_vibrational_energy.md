# Which initial vibrational energies fit three boundary displacements?

**CL075/v1 · Classical author result.** On the four-chain, every real boundary triple determines one initial velocity vector and one total energy. On the four-diamond, the consistent triples form a plane. Each such triple permits every energy from a computable minimum to infinity. One squared middle-pair separation, measured at the first sample, determines the excess above that minimum even when the boundary triple vanishes.

## Native support and actual placements

Condition throughout on the prepared prefix $a<b$ with marks $(0,0)$ and descendant counts $(1,0)$. Births $x,y$ retain the accepted all-ideal probabilities and independent fair newborn marks. Each birth increments the count of every old actual handle in its ideal and appends a zero at the newborn. Induction counts exactly the strict descendants, since membership in the ideal means the new vertex is a strict descendant. The largest possible count is three, so the finite register never wraps on this preparation.

Here is the complete structural ledger in three rows of conditional factors. In each row $F=\{a,b,x\}$, $e=1/44$, and the fourth ideals and factors correspond in the order displayed. Every entry represents four marked histories, each of weight $p_3q_4/4$. The letters in this ledger are proof coordinates.

| Third ideal | $p_3$ | Fourth ideals | Conditional factors $q_4$ | Eligible entries |
| --- | ---: | --- | --- | --- |
| $\varnothing$ | $1/5$ | $\varnothing,\{x\},\{a\},\{a,b\},\{a,x\},F$ | $e,e,5e/6,19e/6,11e/2,65/88$ | none |
| $\{a\}$ | $1/6$ | $\varnothing,\{a\},\{a,b\},\{a,x\},F$ | $e,e,19e/5,19e/5,43/55$ | $F$ gives D |
| $\{a,b\}$ | $19/30$ | $\varnothing,\{a\},\{a,b\},F$ | $e,e,e,41/44$ | $F$ gives C |

The conditional rows each sum to one, as do the three incoming weights. A unique maximum would have to be the last newborn above every old handle, which requires $F$. The first full entry retains two minima. Thus the active weights are $p_C=(19/30)(41/44)=779/1320$ and $p_D=(1/6)(43/55)=172/1320$, four marked histories each. The remaining 24, 16 and 12 marked histories in the respective rows carry $264/1320,48/1320,57/1320$. Their total $p_I=369/1320$ gives a distinguished inactive record $\perp$ with no mechanical energy assigned. These probabilities cover all 60 marked histories without a prefix probability, ordering multiplicity or active-branch renormalization.

Use the accepted count selector on its prepared support. The multisets $\{0,1,2,3\}$ and $\{0,1,1,3\}$ select C and D respectively. All others give $\perp$. The actual device receives a faithfully bound count for each handle on the opaque roster and can register covariant placement commands. On C the strictly decreasing count sequence $3,2,1,0$ registers $s,u,v,t$ with covers $su,uv,vt$. On D the unique counts 3 and 0 register $s,t$, and the count-one set $\{u,v\}$ registers the four covers $su,sv,ut,vt$. A multiset alone supplies no actual port addresses. The observer is explicitly granted the class flag and the measurements below. No history, marks, birth order, derivative, or resolved interior displacement is needed as an observer input.

## Mechanical flow and finite samples

After the last birth, fix $q_t=0$. Install identical masses $m>0$ at the free handles and identical scalar springs $k>0$ on the undirected covers. All displacements share a calibrated oriented axis and equilibrium zero. The clock and the physical values of $m,k$ are supplied. Set $q(0)=0$, write $v_0=\dot q(0)$ for an arbitrary real initial free velocity, and allow unforced evolution through $3\Delta$ with no further growth, impulses, damping, onsite terms or other coupling. Both sensors are ideal, calibrated and nondisturbing. In proof order $(s,u,v)$, the grounded Laplacians are

$$
 L_C=\begin{pmatrix}1&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix},
 \qquad L_D=\begin{pmatrix}2&-1&-1\\-1&2&0\\-1&0&2\end{pmatrix}.
$$

For a free vector extended by zero at $t$, the quadratic form $q^\top Lq$ equals the sum of $(q_i-q_j)^2$ over all covers, counting each edge once. Connectedness to the clamp gives positive definiteness. On these two graphs every degree is at most two. Summing $(z_i-z_j)^2\leq 2(z_i^2+z_j^2)$ on covers with $z_t=0$ gives $L\leq4I$ in the quadratic-form sense.

The evolution $m\ddot q=-kLq$ conserves the total energy on every active trajectory since

$$
 E(\tau)=\tfrac m2\|\dot q(\tau)\|^2+\tfrac k2q(\tau)^\top Lq(\tau),
 \qquad \dot E=\dot q^\top(m\ddot q+kLq)=0,\qquad E(0)=\tfrac m2\|v_0\|^2 .
$$

The reaction at $t$ can be nonzero but supplies zero power because $\dot q_t=0$. This conservation statement applies after preparation on the frozen graph.

For each unit eigenvector $\phi_j$ with eigenvalue $\lambda_j>0$, define

$$
 b_j=\phi_j^\top v_0,\quad \omega_j=\sqrt{k\lambda_j/m},\quad
 \theta_j=\omega_j\Delta=\sqrt{\lambda_j}/4,\quad
 f_j(\tau)=\sin(\omega_j\tau)/\omega_j,\qquad
 \Delta=\tfrac14\sqrt{m/k}.
$$

The normal-coordinate solution is $q(\tau)=\sum_j\phi_j b_j f_j(\tau)$ in an orthonormal eigenbasis, by the scalar oscillator equations and the two initial conditions. Write $y=(y_1,y_2,y_3)^\top$ for the signed readings at $s$ relative to $t$ at the three specified times on the same trial. Then $y_n=\sum_j(\phi_j)_s b_j f_j(n\Delta)$. All eigenvalues lie in $(0,4]$, so $0<\theta_j\leq1/2<\pi$, $\sin\theta_j>0$, and distinct eigenvalues have distinct cosines $c_j=\cos\theta_j$. With $d_j=(\phi_j)_s f_j(\Delta)$, column $j$ of the sampling matrix is

$$
 M_j=d_j\, (1,\ 2c_j,\ 4c_j^2-1)^\top .
$$

This uses the exact double- and triple-angle identities. For three distinct frequencies and three nonzero $d_j$, the determinant is $8(\prod_j d_j)\prod_{i<j}(c_j-c_i)$, by the Vandermonde determinant for these three polynomials. For two such frequencies the first two rows alone give determinant $2d_1d_2(c_2-c_1)$. These rank arguments use only the three recorded times.

## Chain

A chain eigenvector with zero source coordinate must vanish. Its first row forces its second coordinate to vanish, then its second row forces its third to vanish. A repeated eigenvalue of this real symmetric matrix would have an eigenspace of dimension at least two, containing a nonzero vector with zero first coordinate. Thus all three eigenvalues are distinct and all source components are nonzero.

For explicit evaluation, take the three roots in increasing order of $\lambda^3-5\lambda^2+6\lambda-1=0$, obtained from $\det(\lambda I-L_C)$. Normalize $(1,1-\lambda,(2-\lambda)(1-\lambda)-1)^\top$ for each root, by the first two eigenvector equations. Form $M_C=[M_1\ M_2\ M_3]$ above. For every finite $y\in\mathbb R^3$,

$$
 b=M_C^{-1}y,\qquad v_0=\sum_j b_j\phi_j,\qquad
 \mathcal E_C(y)=\{m\|b\|^2/2\}.
$$

Invertibility proves that each such triple has exactly the listed preparation and energy. In particular $y=0$ requires rest, and every nonzero triple requires positive energy.

## Diamond

Use the three orthonormal directions $g=(1,0,0)^\top,\ h=(0,1,1)^\top/\sqrt2,\ a=(0,1,-1)^\top/\sqrt2$. The last direction changes sign under a middle swap. On $g,h$, the diagonal entries of $L_D$ are 2 and both off-diagonal entries are $-\sqrt2$. The visible unit eigenvectors are $\phi_-=(g+h)/\sqrt2,\ \phi_+=(g-h)/\sqrt2$, with eigenvalues $2-\sqrt2,2+\sqrt2$ and common source component $1/\sqrt2$. The remaining eigenvector $a$ has eigenvalue 2 and source component zero.

Using the preceding definitions at the two visible eigenvalues, form $M_D=[M_-\ M_+]$. Let $B$ be its first two rows. For a real $y$, compute

$$
 (b_-,b_+)^\top=B^{-1}(y_1,y_2)^\top,\qquad
 v_{\rm vis}=b_-\phi_-+b_+\phi_+,\qquad
 E_{\min}=\tfrac m2(b_-^2+b_+^2).
$$

The two-column determinant above proves $B$ is invertible. Compatibility requires and suffices that the third row of $M_D$ times this pair equals $y_3$. Equivalently,

$$
 y_3=2(c_-+c_+)y_2-(4c_-c_++1)y_1 .
$$

Indeed each column obeys this identity and the first two coordinates are free. Failure gives empty velocity and energy sets. On this plane the full velocity fiber and energy set are

$$
 \{v_{\rm vis}+\alpha a:\alpha\in\mathbb R\},\qquad
 \mathcal E_D(y)=\{E_{\min}+\tfrac m2\alpha^2:\alpha\in\mathbb R\}
 =[E_{\min},\infty).
$$

Every listed energy is attained by choosing the corresponding magnitude of $\alpha$. The zero triple permits all nonnegative energies, including rest. For other consistent triples $E_{\min}>0$.

### Squared separation at the first time

The optional D probe supplies $z=(q_u(\Delta)-q_v(\Delta))^2$ on the unordered middle pair. Set $F_a=\sin(\sqrt2/4)/\sqrt{2k/m}>0$. Equal middle entries in both visible modes cancel in the difference, while the difference for $a$ is $\sqrt2$ in the chosen proof ordering. Hence $z=2F_a^2\alpha^2$. For a compatible boundary triple and any real $z\geq0$, the complete compatible initial velocities are

$$
 v_{\rm vis}+\alpha a,\quad \alpha\in
 \left\{-\frac{\sqrt z}{\sqrt2 F_a},\,\frac{\sqrt z}{\sqrt2 F_a}\right\},
 \qquad \mathcal E_D(y,z)=\left\{E_{\min}+\frac{m z}{4F_a^2}\right\}.
$$

At $z=0$ the two choices coalesce at $v_{\rm vis}$. For $z>0$ the two assignments differ by middle-handle exchange, so their energy agrees even on actual handles whose signed velocities are unresolved. A negative $z$ or a failed boundary-plane test gives empty sets. Thus $(0,0,0)$ with $z>0$ certifies strictly positive energy, and the all-zero augmented reading certifies rest. C retains its three-sample record and $\perp$ has no mechanical coordinates.

## Full-law witness and interpretation

Fix any $E_*>0$ in the supplied physical energy units. Use the same native law in both settings. Setting R initializes all active masses at rest. Setting H keeps C at rest. On every D history set the source velocity to zero and give the unordered middle pair the two opposite velocities $+\sqrt{E_*/m},-\sqrt{E_*/m}$, choosing the two actual assignments with probability $1/2$ each. This is a supplied preparation kernel with no preferred middle handle. It gives $\alpha^2=2E_*/m$ and energy $E_*$ for either assignment. It leaves each native marked-history weight intact. No distribution on the arbitrary unknown velocities used in the compatibility calculation has been presumed.

Write $O=(0,0,0)$, and use $\delta$ for a point mass. The complete basic records have laws

$$
 P_{\rm basic}^{R}=P_{\rm basic}^{H}=
 \tfrac{779}{1320}\delta_{(C,O)}
 +\tfrac{172}{1320}\delta_{(D,O)}
 +\tfrac{369}{1320}\delta_{\perp}.
$$

The class flag keeps the chain and diamond atoms separate even at zero displacement. The augmented laws are

$$
 \begin{aligned}
 P_{\rm aug}^{R}&=\tfrac{779}{1320}\delta_{(C,O)}
 +\tfrac{172}{1320}\delta_{(D,O,0)}+\tfrac{369}{1320}\delta_{\perp},\\
 P_{\rm aug}^{H}&=\tfrac{779}{1320}\delta_{(C,O)}
 +\tfrac{172}{1320}\delta_{(D,O,\,4F_a^2 E_*/m)}+\tfrac{369}{1320}\delta_{\perp}.
 \end{aligned}
$$

Each law sums to one. Both assignments contribute to the same diamond record in H. The equal basic laws include a positive-probability diamond branch whose pointwise energies differ. The augmented result determines energy separately for every compatible active trial. An energy distribution for other unknown preparations would require their preparation law.

For any simultaneous renaming of the handles, the count classes, commanded covers, clamp and sensor positions transport together. The permutation conjugates $L$, carries initial data and their unique trajectory to their images, and preserves the kinetic norm, cover energy, source displacement and squared unordered-pair reading. The diamond sign exchange in H is itself invariant in law. The signed axis, equilibrium zero, clamp, mechanical initialization, uniform masses and springs, calibrated clock, class-flag access and optional probe are apparatus premises. The native growth law supplies the selected carriers and weights. The earlier static and dissipative responses do not supply the mechanical evolution or these measurements.

The matrices and eigenvalues are dimensionless. $m/k$ has units of time squared, $\omega_j$ inverse time, and $f_j,F_a$ time. The $b_j,\alpha$ have velocity units. Thus the three $y_n$ have length units and $z$ has length-squared units. Each energy formula has units of mass times length squared divided by time squared, including the additional $mz/(4F_a^2)$. All identification claims use the exact calibrated records over the stated finite horizon.

## What QR must register

QR use requires registered covers, the clamp, equal positive masses $m$, identical Hooke stiffness $k$, the postgrowth mechanical law and initial zero displacements. The signed displacement axis, length zero and gain, calibrated clock, class-flag access and simultaneous nondisturbing unordered-pair probe are supplied. In physical units $F_a$ is a time, $z$ a squared length, and the inferred energy has units of mass times squared length per squared time. Native selection establishes carrier placement and probabilities. Applying the inference to DET would require an independently justified mechanical attachment and calibration of mass, length and time.

The handle-bound source and accepted placement rules are described in [terminal counts and field placement](terminal_counts_and_field_placement.md) and [the finite incidence register](finite_incidence_register.md).

## Scientific provenance

- Classical CL075/v1 SHA-256 b193e01bcbf0d8267e86e842fbb0f7c88177730f9e80097b013d44f7a0f2e38e.
- Independent Classical source review SHA-256 a31822006dda02b9db1c5697428c76d576cfb39279fafc6e681df4cc7a96ce20.
- Independent QR recipient assessment SHA-256 6fe7253068833c458b8d4488a73846c1a0c50116e0edd0cfb5a22015e92a4692.
