# Closed work in active/passive mass channels

The signed cross-channel works, in units E0=G m²/d, are World I (0,0,0,0) and World II (0,-4/3,-16/9,+4/3). Thus their closed-loop works are 0 and -16/9, respectively. World I has the joint configuration potential exhibited below. World II cannot have one generating all specified cross-channel forces on a domain containing this loop. Matching the accepted aligned force-null record therefore does not suffice to attach conservative configuration-only mechanical energy to this specified channel. This is a conditional mechanical statement, not a complete physical gravity or energy-creation claim.

## 1. Premises and the matched observation

The [four-force-null comparison](local_active_passive_mass_from_force_nulls.md) supplies the two exact active/passive worlds, the collinear force convention and the limits of its static record. Here the added planar force law, prescribed trajectory and independent inertial masses are explicit premises. The calculation retains every site force and torque contribution; it does not assume a joint reciprocal potential in World II.

The matched observation is the signed sum of forces on both carriers in the aligned settings, with the same setting proportions, success record, positive gain and verified zero. Both coefficient worlds give that null at every aligned separation in the source's stated domain. Their separate carrier forces need not match. They do not share the full four-setting record: the registered reversal at R=2d gives zero in World I and +16Gm²/(9d²) in World II. The four-null inverse is unchanged.

All G,m,d,tau are strictly positive and finite. Each carrier has two material sites with body offsets (-d/2,0),(+d/2,0). Each site separately has inertial mass 2m, so each carrier has inertial mass 4m and centre moment of inertia I=2(2m)(d/2)²=m d². These inertial masses are supplied independently of the active/passive coefficients. Constraints within each carrier are ideal, rigid and massless, with zero total constraint power.

Both worlds have all active coefficients a_Ai=a_Bj=m. Write p_Ai=m u_i and p_Bj=m v_j. World I has u=v=(2,2). World II has u=(1,3), v=(3,1), always ordered by material label. Geometry, inertia, G and controls are the same in both worlds.

For r_ij=x_Bj-x_Ai, the added planar force law is exactly

```text
F_Ai<-Bj = G m² u_i r_ij/|r_ij|³,
F_Bj<-Ai = -G m² v_j r_ij/|r_ij|³.
```

Every site's force is the sum of its two cross-pair contributions. Only this cross channel is included. There is no silently supplied self, fixture, field or reservoir force or energy. External actuators prescribe the motion; no isolated physical system is asserted.

The observation is exact signed force work at all four sites, equivalently the proved force/torque power below. It is an ideal mathematical record, not a measured support reaction, calibrated subtraction or empirical permission.

## 2. Exact path, joins and finite domain

Put alpha_0=beta_0=-1/2, alpha_1=beta_1=+1/2 and q_i=2-alpha_i, so q=(5/2,3/2). Along the entire path theta_A=0 and theta=theta_B:

```text
x_Ai=(X+d alpha_i,0),
x_Bj=(X+2d+d beta_j cos(theta), d beta_j sin(theta)),
r_ij=d(q_i+beta_j cos(theta), beta_j sin(theta)).
```

With rho_ij=|r_ij|/d,

```text
rho_ij²=q_i²+beta_j²+2 q_i beta_j cos(theta),
q_i-|beta_j| <= rho_ij <= q_i+|beta_j|.
```

Consequently d <= |r_ij| <= 3d for every cross pair on every leg, including both rotations. Internal site spacing stays d. There are no point collisions. The whole path has a collision-free neighbourhood; no singular force limit is approached for fixed positive d.

On each leg let s be elapsed leg time divided by tau and h(s)=10s³-15s⁴+6s⁵. Then h(0)=0, h(1)=1,

```text
h'(s)=30s²(1-s)²,
h''(s)=60s(1-s)(1-2s).
```

Both derivatives vanish at both endpoints; h is monotone from 0 to 1. The prescribed legs and complete join data are:

| Leg | Interval | X | theta_B |
|---|---|---|---|
| 1 | 0 to tau | d h(s) | 0 |
| 2 | tau to 2tau | d | pi h(s) |
| 3 | 2tau to 3tau | d(1-h(s)) | pi |
| 4 | 3tau to 4tau | 0 | pi(1-h(s)) |

The boundary pairs (X,theta_B) are (0,0),(d,0),(d,pi),(0,pi),(0,0). At every boundary X_dot=theta_B_dot=X_ddot=theta_B_ddot=0; theta_A and its derivatives remain zero. The site velocity formula and its derivative then give zero site velocity and acceleration at every join. Position, orientation, velocity and acceleration match, so the concatenated motion is C2. At 4tau every labelled site, centre, marked orientation and velocity equals its initial value. The finite horizon is exactly 4tau.

The polynomial rates and accelerations are bounded on each compact leg. Each pair force magnitude is at most 3 G m²/d², each site force at most twice that, and each carrier torque magnitude at most 6 G m²/d. With the supplied positive finite inertias, the enforcing forces and torques below are finite and continuous. No approximation in d/tau or quasistatic limit is taken.

## 3. Full site power, torque and aligned/reversed forces

Define F0=G m²/d² and E0=F0 d. With F_A=sum_i F_Ai and F_B=sum_j F_Bj, the total force on the two carriers from this channel is

```text
F_A+F_B=F0 sum_ij (u_i-v_j)(q_i+beta_j cos(theta), beta_j sin(theta))/rho_ij³.
```

For any rigid carrier, with centre C and site offset ell_i, site velocity is C_dot+theta_dot z_cross ell_i. Thus

```text
sum_i F_i dot x_i_dot = F_net dot C_dot + tau_C theta_dot,
tau_C=sum_i (ell_i cross F_i)_z.
```

This follows termwise from F_i dot(z_cross ell_i)=(ell_i cross F_i)_z. It neither drops site work nor assumes reciprocal cross forces. Along our path the two torques, including the stationary A torque, are

```text
tau_A=E0 sum_ij u_i alpha_i beta_j sin(theta)/rho_ij³,
tau_B=E0 sum_ij v_j q_i beta_j sin(theta)/rho_ij³.
```

For the B formula, dotting its pair force with d beta_j(-sin(theta),cos(theta)) cancels the two beta_j² terms and leaves +E0 v_j q_i beta_j sin(theta)/rho_ij³. The angular velocity of A is zero, so its torque power is zero, not its torque generally. Both centre velocities are (X_dot,0), giving the exact channel power

```text
P_cross=(F_Ax+F_Bx) X_dot + tau_B theta_dot.
```

At theta=0 and pi all pair vectors point rightward and all torques vanish. The dimensionless distance matrices, rows i and columns j, are

```text
rho_al = [[2,3],[1,2]],
rho_rev = [[3,2],[2,1]].
```

In World I the four differences u_i-v_j are zero. At either endpoint pose F_Ax/F0=+2(1/4+1/9+1+1/4)=+29/9 and F_Bx/F0=-29/9.

In World II the difference matrix is [[-2,0],[0,+2]]. Aligned, the total is -2/4+2/4=0. The individual force magnitudes are

```text
F_Ax/F0=(1/4+1/9)+3(1+1/4)=37/9,
-F_Bx/F0=3(1/4+1)+(1/9+1/4)=37/9.
```

Reversed, material label 0 of B is on the right; the same lab sign convention gives

```text
F_Ax/F0=(1/9+1/4)+3(1/4+1)=37/9,
-F_Bx/F0=3(1/9+1/4)+(1/4+1)=7/3,
(F_Ax+F_Bx)/F0=-2/9+2=16/9.
```

These directly recover the inherited aligned null and reversed contrast at R=2d. They do not repeat the source's four-reading inverse or introduce a new coefficient classification.

## 4. Individual rotations and exact reversal cancellation

During either rotational leg A is held fixed and neither centre translates. Its nonzero forces and possible torque therefore do no work. Define only for this fixed-A calculation

```text
U_B(x_B0,x_B1; fixed A)=-G m² sum_ij v_j/|x_Bj-x_Ai|.
```

Its negative B-site gradients equal the B-site forces exactly. Therefore W_B=U_B(start)-U_B(end) on a rotation. In World II this is only a one-carrier-coordinate primitive: its A gradients would use v_j where the actual A forces use u_i. It is not called a joint potential.

Write S(theta)=sum_ij v_j/rho_ij(theta), so U_B=-E0 S. At the two endpoints the unweighted sums for each B label are

```text
sum_i 1/rho_i0(0)=3/2,   sum_i 1/rho_i1(0)=5/6,
sum_i 1/rho_i0(pi)=5/6,  sum_i 1/rho_i1(pi)=3/2.
```

For World I, S(0)=S(pi)=2(3/2+5/6)=14/3. Hence leg 2 work is E0[S(pi)-S(0)]=0 and leg 4 work is E0[S(0)-S(pi)]=0 individually.

For World II, S(0)=3(3/2)+5/6=16/3 and S(pi)=3(5/6)+3/2=4. Hence leg 2 work is -4E0/3 and leg 4 work is +4E0/3 individually. These values follow from their separate endpoint evaluations, not merely a cancellation assumption.

The full rotational paths also cancel exactly: h(1-s)=1-h(s), so the configuration of leg 4 at s is the configuration of leg 2 at 1-s translated by -d in x for every site. All r_ij and both force collections are unchanged by a common translation, while each B-site displacement is reversed. A-site displacements are zero on both rotations. Thus the complete four-pair site work on leg 4 is the negative of that on leg 2, consistently with the individual calculations. No rate assumption is needed to obtain this work cancellation.

## 5. Exactly two four-leg cross-channel and external-work ledgers

Translation leaves the pair vectors unchanged. Each carrier's translation work is its constant x force times the signed common displacement: +d on leg 1 and -d on leg 3. All values in the following two ledgers are divided by E0. W_A and W_B are the full work on each carrier, with both of its sites and every cross pair included. W_ext is the total work of the enforcing external controls, derived in section 6. Every leg has Delta K=0.

World I:

| Leg | W_A/E0 | W_B/E0 | W_cross/E0 | W_ext/E0 |
|---|---:|---:|---:|---:|
| 1 translate aligned | 29/9 | -29/9 | 0 | 0 |
| 2 rotate B 0 to pi | 0 | 0 | 0 | 0 |
| 3 return reversed | -29/9 | 29/9 | 0 | 0 |
| 4 rotate B pi to 0 | 0 | 0 | 0 | 0 |

Totals: W_A=W_B=W_cross=W_ext=0.

World II:

| Leg | W_A/E0 | W_B/E0 | W_cross/E0 | W_ext/E0 |
|---|---:|---:|---:|---:|
| 1 translate aligned | 37/9 | -37/9 | 0 | 0 |
| 2 rotate B 0 to pi | 0 | -4/3 | -4/3 | 4/3 |
| 3 return reversed | -37/9 | 7/3 | -16/9 | 16/9 |
| 4 rotate B pi to 0 | 0 | 4/3 | 4/3 | -4/3 |

Totals: W_A=0, W_B=W_cross=-16E0/9, W_ext=+16E0/9. The translation sum uses both moving carriers; using only A or only the endpoint net force on B would give the wrong ledger. The B torque, rather than the centre force, supplies the rotational work.

## 6. Full kinetic and external-control balance

The complete supplied carrier kinetic energy along the imposed path is

```text
K=sum_C [ (1/2)(4m)|C_dot|²+(1/2)I theta_C_dot² ]
 =4m X_dot²+(1/2)m d² theta_dot².
```

In particular K is generally positive inside a leg even though it vanishes at every boundary. Let the enforcing centre forces and centre torques be

```text
F_ext,A=4m C_A_ddot-F_A,   F_ext,B=4m C_B_ddot-F_B,
tau_ext,A=-tau_A,         tau_ext,B=m d² theta_ddot-tau_B.
```

Their y components can be nonzero while both centres have zero y velocity. Their A holding torque can be nonzero while A has zero angular velocity. These do no corresponding work, without being omitted from the required controls.

The exact external power is

```text
P_ext=sum_C [F_ext,C dot C_C_dot+tau_ext,C theta_C_dot]
 =8m X_dot X_ddot+m d² theta_dot theta_ddot-P_cross
 =dK/dt-P_cross.
```

The inertial acceleration power is explicitly retained throughout each leg. Its integral is [4m X_dot²+(1/2)m d² theta_dot²]_start^end=0 on each rest-to-rest leg. With ideal constraints contributing zero total power, integration gives

```text
W_ext,leg=Delta K_leg-W_cross,leg=-W_cross,leg,
```

which supplies every external entry in the two ledgers. Carrier by carrier, the same rest-endpoint argument gives W_ext,A=-W_A and W_ext,B=-W_B if a split by actuator carrier is wanted; no additional leg or model is needed.

Zero integrated external work in a leg does not mean zero external effort, zero instantaneous power, absence of intermediate kinetic energy, or zero energetic cost of a realizable actuator. No actuator-internal, fixture, field, heat or reservoir accounting has been supplied. In World II the displayed control input and cross-channel negative work balance the specified matter kinetic account, but this mathematical equality does not identify a physical destination for that input or close a physical apparatus's total energy.

## 7. Configuration-potential decisions and scope

For World I define, on the collision-free site configuration domain,

```text
U_I=-2G m² sum_ij 1/|x_Bj-x_Ai|.
```

This is single-valued and smooth wherever no cross-pair distance is zero. Since

```text
grad_xAi (1/|r_ij|)=+r_ij/|r_ij|³,
grad_xBj (1/|r_ij|)=-r_ij/|r_ij|³,
```

its negative gradients give both F_Ai<-Bj=+2Gm² r_ij/|r_ij|³ and F_Bj<-Ai=-2Gm² r_ij/|r_ij|³, pair by pair. Restricting this same scalar to the rigid-carrier configurations gives the corresponding forces and torques through virtual work. Thus P_cross=-dU_I/dt and every closed path in its domain has zero work. The zero loop result here is accompanied by an explicit derivative-checked potential; zero work on one loop alone would not prove this general compatibility. During rotation U_I need not be constant, despite equal endpoint values.

For World II, suppose a single-valued configuration-only U generated every specified cross-channel generalized force on a domain containing this full rigid-carrier loop. Its work one-form would be -dU, so its integral around this returned labelled configuration would be zero. The exact computed integral is instead

```text
closed integral sum_sites F_site dot dx_site = -16Gm²/(9d) != 0.
```

Therefore no such scalar exists on a domain containing the loop, even for these rigid carriers with the registered fixed A orientation and relative centre separation. This is a complete-loop obstruction, not an inference from a static nonzero total force or an assumed reciprocal law. It does not prohibit a physical completion with further dynamical state and energy/momentum channels; none is constructed here.

Both worlds fit the accepted aligned force-null record, but only World I has the specified conservative cross-channel energy attachment. The complete controlled work record supplies a different decision from the source's static four-null identifiability result. This result does not establish integrability by assuming reciprocal potentials or substituting a different internal orientation loop. Any source attachment remains conditional and requires its own physical/native correspondence.

Conventional dimensions are [G]=L³/(M T²), [a]=[p]=[m]=M, [d]=L, [tau]=T, [F0]=M L/T², [E0]=M L²/T² and [I]=M L². Angles are dimensionless. No native geometry, time, mass, G or action unit is derived. The planar inverse-square law, independent inertia, prescribed ideal control, rigid geometry and exact observation are added assumptions. No isolation, self-field completion, support subtraction, material realization, measured gravity validation, energy creation, useful engine, efficiency or software claim follows.

The construction covers exactly two fixed worlds and one common four-leg loop, with all site/torque work, external control work with inertia, noncollision and rest-endpoint certificate, and the two potential decisions.

The tested energy attachment means a scalar of the **joint labelled configuration** whose negative generalized derivatives reproduce all retained channel forces and torques. Fitting a force-null statistic or defining an energy label alone does not establish that attachment. Restricting the domain to exclude the loop changes the claim; adding dynamical state changes the configuration-only premise. Neither alternative is excluded here. An additive energy constant cannot remove the circulation.

A complete physical source claim also requires a registered mapping to its mechanical variables, a justified force/source law and unit calibration, and the relevant full energy/momentum balance. This result neither supplies those premises nor refutes a separately justified Hamiltonian or stress-source construction. Returning the labelled carrier configuration does not prove that omitted physical state returns. No quantum ontology assumption is needed, and the result provides no evidence for a particular hidden relational state or a perpetual engine. Retired kappa-gravity is not revived.

## Reviewed basis

DET Classical supplied the finite derivation and a distinct nonblind scientific review that checked the force and torque work, finite path, kinetic ledger and potentials. DET Quantum Relativity independently reviewed the restricted recipient use as a limitation on inference from the aligned-null record. Both reviews retain the supplied channel and physical-accounting boundaries above.
