# How large can the axial pair-force imbalance be at finite separation?

Independently reviewed conditional result, 9 November 2026.

**Theorem.** Fix the two active and two passive totals, with $P_1/A_1=P_2/A_2>0$. Place the point active sources at the registered centers a distance $R>2a$ apart. Each rigid carrier has an independent positive, inversion-symmetric finite atomic passive measure strictly inside its radius-$a$ ball. Under the supplied additive Newtonian response to the other carrier's field, put $\eta=a/R$ and $F_0=GA_1P_2/R^2=GA_2P_1/R^2$. With positive axis from body 1 to body 2, the exact attainable set of the signed axial **sum** of the two matter forces divided by $F_0$ is
$$
 (-D(\eta),D(\eta)),\qquad
 D(\eta)=\frac{1+\eta^2}{(1-\eta^2)^2}-\frac{1}{(1+\eta^2)^{3/2}} .
$$
Both signs and zero are attained. The endpoints are limits. Even the complete prior clock, lift and spring law can be identical throughout this interval at fixed totals. The law for local passive response in a nonuniform field is an additional physical premise.

## 1. Force on an inversion-symmetric pair of atoms

Let $n$ be the unit vector from center 1 to center 2, $y$ an offset in the common spatial frame from the receiving body's center, $w=y/R$, and $g(w)=(n-w)/|n-w|^3$. Let $\pi_i=\nu_i/P_i$ be the passive probability measure on the physical offsets of body $i$. The point-source attraction, added over receiving atoms with their positive passive weights, gives the full vectors
$$
 \frac{\mathbf F_{1\leftarrow2}}{F_0}=\int g(y/R)\,d\pi_1(y),\qquad
 \frac{\mathbf F_{2\leftarrow1}}{F_0}=-\int g(-y/R)\,d\pi_2(y).
$$
The two equal prefactors use only equality of the total ratios. The opposite signs follow from the order of the centers. By inversion symmetry the second integral equals $\int g(y/R)\,d\pi_2(y)$ before applying its minus sign. Each atom of body 1 has positive axial attraction and each atom of body 2 negative axial attraction since $a<R$. An oblique inversion pair can have a transverse force because the two atoms are at different distances from the source. The theorem asks for a single signed component. The attaining examples below have zero transverse force.

Each admitted inversion-symmetric finite atomic probability measure is a convex combination of unit orbit measures $Q_y=(\delta_y+\delta_{-y})/2$, counting the center once. For an orbit let $t=|y|/R$, $x=|n\cdot y|/R$ and $q=1+t^2$. Every $x$ in $[0,t]$ is attained by an orientation in the three-dimensional ball. The unit normalized axial attraction of this orbit is
$$
 K(t,x)=\tfrac12[f_t(x)+f_t(-x)],\qquad
 f_t(x)=\frac{1-x}{(q-2x)^{3/2}}.                                          \tag{1}
$$
Each body's positive axial magnitude divided by $F_0$ is the mean of this kernel over its orbits. Write these means as $k_1,k_2$. The normalized signed sum is $k_1-k_2$.

## 2. Sharp interval and strict endpoints

At fixed $0<t\le\eta<1/2$, on $[-t,t]$ direct differentiation gives
$$
 f'_t(x)=\frac{2-t^2-x}{(q-2x)^{5/2}},\qquad
 f''_t(x)=\frac{9-6t^2-3x}{(q-2x)^{7/2}}>0 .
$$
The denominator is positive since $q-2x\ge(1-t)^2$, and the numerator exceeds $9-6/4-3/2>0$. Thus $f'_t$ is strictly increasing. By (1), $\partial_xK=[f'_t(x)-f'_t(-x)]/2>0$ for $x>0$. This checks the angular optimization over the full ball. For both bodies the minimum at radius $Rt$ is perpendicular to the axis and the maximum is on the axis. The respective values are
$$
 L(t)=K(t,0)=(1+t^2)^{-3/2},\qquad
 U(t)=K(t,t)=\tfrac12[(1-t)^{-2}+(1+t)^{-2}]
          =\frac{1+t^2}{(1-t^2)^2}.                                        \tag{2}
$$
At $t=0$ both equal one. For $t>0$, $L$ decreases strictly and $U$ increases strictly, as seen directly from (2). On the physical open ball every orbit, hence every allowed positive mean, lies strictly between $L(\eta)$ and $U(\eta)$.

For the converse, fix any $k$ in this open interval. By continuity choose one $0<t<\eta$ with $L(t)<k<U(t)$. At that radius mix the perpendicular and axial orbits with axial fraction $(k-L(t))/(U(t)-L(t))$. The finite measure is positive, inversion-symmetric, strictly interior and has mean exactly $k$. Both component orbits have zero transverse force. Multiplying by $P_i$ restores the specified total.

Let $m_c=[U(\eta)+L(\eta)]/2$. For any $|b|<D(\eta)=U(\eta)-L(\eta)$, choose $k_1=m_c+b/2,\ k_2=m_c-b/2$. The preceding construction realizes both independently, including $b=0$, with the specified inertias and totals. For the positive limiting endpoint take the first orbit axial and the second perpendicular at the same $Rt<a$, and let $t\uparrow\eta$. The difference approaches $D(\eta)$. Interchanging the two orientations approaches $-D(\eta)$. Attaining either endpoint would require the excluded boundary values of both one-body means.

## 3. Same full prior observations, different forces

For clarity, fix one joint law for all three registered sectors $i=0,1,2$. Let $d_i=i+1$, let each active source be $A_i\delta_0$ relative to its own center with $A_i=m d_i$, take $P_i=p d_i$, and choose the same spring inertia $M_i=C$ for every sector, with $m,p,C>0$. Select sectors 1 and 2 for the force question. Their common $P/A=p/m$ and $F_0=6Gmp/R^2$ are fixed. The following readings do not involve either normalized passive profile.

- **Springs.** Use the registered rest release $0<D_{\rm sp}<L_{\rm sp}$, common tick $T>0$ and stiffness $C/T^2$. Every $u_i=1$, so all three signed ratios are $y_{01}=y_{02}=y_{12}=\cos\sqrt2$ on the strict first lobe, in both protocols.
- **Twelve clocks.** Use the calibrated positions $2a\omega,4a\omega$ for each of the six signed coordinate unit vectors $\omega$, with zero affine background and common gain $g_s>0$. All six outer-minus-inner readings in sector $i$ are $g_sGA_i/(4ac^2)$, retained as one ordered vector. Only the central active source enters this Newtonian field.
- **Uniform lifts.** In fields $j=1,2$ choose positive potential gaps $j\phi$ with matched held clocks reading $z_j=g_c j\phi/c^2$, common positive clock and work gains, and independently zeroed offsets. Set $H_j=0$, $P_\emptyset=0$, $D^+_{ij}=p\phi$ and $D^-_{ij}=0$ on all six allowed rows. Use field 1 with blank, 0, 1 and field 2 with blank, 1, 2. The signed store readings are
$$
       (w^+_{ij},w^-_{ij})=g_w(P_i j\phi+p\phi,\,-P_i j\phi).
$$
  Each blank reads $(g_wp\phi,0)$. With initial store energy $8p\phi$, the turning level is at least $p\phi$. Each cycle ends with $7p\phi$ in the store and transfers $p\phi$ to the sink. Maintain the same rigid translation, registration, return to rest, holders, installation boundaries, negligible backreaction and losses in both worlds. A uniform gradient gives the same potential change at every translated passive atom. Integrating the change gives $P_i j\phi$, irrespective of spatial distribution.

For the full population law choose the two protocols independently of preparation with probability $1/2$ each. At $i=0,1,2$ prepare $\delta_{00},\delta_{10},\delta_{11}$. Each load's eight native histories $h=(s,b_1,b_2)$ have probability $p_i(h)=q_s[1+\eta_s{\bf1}_{i=1}/2]/4$, with $(q_E,\eta_E)=(2/3,1/8448)$, $(q_F,\eta_F)=(1/3,-1/4224)$. The table gives the joint weights **including** protocol choice. For any reading event multiply by the indicator that the setting's entire specified reading belongs to it.

| Recorded setting | Native record | Joint weight |
| --- | --- | --- |
| Clock protocol, spring $i\ell=01,02,12$ | Independent $h,h'$ | $p_i(h)p_\ell(h')/12$ |
| Clock protocol, source $i$ | $h$ | $p_i(h)/12$ |
| Lift protocol, same three labelled springs | Independent $h,h'$ | $p_i(h)p_\ell(h')/18$ |
| Lift protocol, each of the four labelled loads | $h$ | $p_i(h)/18$ |
| Lift protocol, each of the two blanks | Distinguished empty token | $1/18$ |

The native histories and point readings across the $216+226=442$ cells, including the two leg signs in each lift, exhaust the probability law. Every other outcome, including failure, has zero probability. Each carrier has one fixed configuration across its settings in each world and sector 0 may keep the same passive profile throughout.

Take any fixed perpendicular direction $e$ and set $t_0=a/(2R)>0$. In the first world use the orbit $Q_{Rt_0 e}$ for both normalized passive profiles of the selected pair. The axial factors are both $L(t_0)$, so the two full forces sum to zero. In the second world switch only the first body's passive profile to $Q_{Rt_0 n}$. The axial sum in units of $F_0$ is now $U(t_0)-L(t_0)>0$, still with zero transverse sum. Every active profile, all three passive totals, both calibrations of the clock protocols, work gain, holders, losses, spring inertias and native weights retain their values. Thus every prior observed cell agrees. The same independence permits every interior imbalance in §2 at this fixed prior law. The forces in the two worlds are separate model evaluations and add no event to that law.

If a positive exterior weak-field amplitude tolerance $\varepsilon$ is prescribed, choose $3Gm/(ac^2)<\varepsilon$. The clock samples are at least $2a$ from their central source, and each selected passive atom is more than $R-a>a$ from the other active center. For a uniform lift path of fixed station spacing $d>0$, set the potential to zero at the starting center and choose $2\phi(1+a/d)/c^2<\varepsilon$. This bounds the potential on the whole swept load for an axial linear lift potential. These choices preserve the force comparison and all record equalities between worlds. The exact Newton potential was supplied only for the stated model. No assertion about a weak field at a point source's own singularity is needed.

## 4. Large separation, calibration and momentum

The positive half-width is $D(\eta)=\tfrac92\eta^2+O(\eta^4)$ as $\eta\to0$, by expanding (2). For a fixed profile the first surviving shape term is also explicit. Define
$$
 Q_i^{(2)}=\int [3(n\cdot y)^2-|y|^2]\,d\pi_i(y).
$$
Expanding the paired expression (1) in $t$ with $x=t|\cos\theta|$ gives $K=1+(9x^2-3t^2)/2+O(t^4)$. Odd terms cancel by inversion and the fourth derivatives are uniformly bounded for $|t|\le1/2,\ |\cos\theta|\le1$, since both squared distances stay at least $1/4$. Consequently the normalized axial sum is $3(Q_1^{(2)}-Q_2^{(2)})/(2R^2)+O((a/R)^4)$. The leading monopole terms cancel exactly. The dimensional supremum is $F_0 D(a/R)$, of order $GA_1P_2 a^2/R^4$ at fixed totals and $a$.

Normalization removes the common strength $GA_1P_2=GA_2P_1$. A common change of length units preserves $a/R$. A dimensional force requires the calibrated separation, $G$, and active and passive scales in consistent units. The prior experiments supply their own clock positions, gains, work store and spring scale. A uniform lift with unknown gain constrains a scaled passive response, and static clock records alone do not certify a central point source. The range is conditional on the supplied totals, reference geometry and independent passive distributions.

If one additionally postulates the same local proportionality $d\nu_i=k\,d\mu_i$ for each body's passive and active measures in physical space, both passive profiles here are fixed at the central active atoms and their forces cancel exactly. More generally the same local proportionality in an additive reciprocal Newton kernel weights each cross-body pair by the same product $k\,d\mu_1(x)d\mu_2(y)$ in both directions. The vectors $(y-x)/|y-x|^3$ and $(x-y)/|x-y|^3$ cancel term by term. The previous records constrain totals and do not establish that stronger local premise.

The imbalance computed here is the sum of two stipulated external-on-matter forces for a held geometry. The model includes no self-force, apparatus or field momentum ledger, and the earlier protocols contain no pair-force or recoil measurement. A conclusion about the actual momentum of a closed system would require an independently specified system boundary, dynamics and observations.

## Reviewed sources

- [Can the same three carriers have proportional passive and active gravitational coefficients?](joint_active_and_passive_gravitational_mass.md)
- [When signed lifting work excludes a common passive-to-inertial mass ratio](signed_lift_work_and_passive_mass.md)
- [How twelve exterior clocks can exclude active-to-inertial mass proportionality](twelve_clock_active_mass_bounds.md)
- [Testing proportionality of active and inertial mass across three carrier sectors](registered_active_and_inertial_mass.md)

Scientific report SHA-256 9444bc98aa137f7595b4462d35f47f43be4446ef0135a1fecfc8774c998bf0c4. Independent review SHA-256 a86ddaafd9575814f9f9c405fe089e6e769d6af38900ba002c117c51fdee908e.
