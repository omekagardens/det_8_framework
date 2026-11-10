# Identical impact records, different finite free-flight admissibility

The supplied two positive-mass targets have identical four-impact records and identical immediate projectile velocity, centre velocity and angular velocity for the selected shot. Nevertheless, over the entire registered interval after that shot, the depth-zero target's free candidate is geometrically admissible and strictly separated, while the depth-a target's formal free candidate lies strictly inside the forbidden finite rectangle. The four recorded ratios therefore do not authorize free continuation. The omitted normal centre depth matters even though the impulse inverse has already identified mass, central inertia, tangential centre and restitution.

This is an exact conditional Newtonian construction using a supplied rigid collision exclusion. It is not evidence that a material realizes that exclusion, and it does not determine the actual motion of the penetrating candidate under an additional contact law.

## 1. Frozen scope, realization and source roles

The accepted [four-impact inverse](rigid_target_inertia_from_four_impacts.md) supplies the immediate frictionless Newton–Euler/restitution map and its restricted inverse. It leaves normal centre depth and finite subsequent contact outside that identified state.

Fix finite m,a,u > 0. Coordinates are x right and y up; positive rotation is counterclockwise. The initial closed collision region is

    B0 = [−3a,3a] × [0,2a].

Its interior excludes the point projectile. For each of exactly two values d=0 and d=a, a rigid massless structure carrying this same rectangle supports exactly two positive masses 3m/2 at (+2a,d) and (−2a,d). These are a concrete ideal mass distribution on the stipulated rigid structure. Their total mass, centre and planar central inertia are

    M = 3m,
    C_d(0) = (0,d),       c = 0,
    I = (3m/2)(2a)² + (3m/2)(2a)² = 12ma².       (1)

The masses lie on the lower boundary for d=0 and inside the region for d=a. Nothing requires a homogeneous rectangle, added face inertia or a finite projectile radius. The same collision region and same mass values/relative central positions are used; only the common normal depth of the mass pair changes. All three initial impact sites −a,0,+a are strictly inside the lower face and distinct from the point masses. A projectile arriving vertically from y<0 reaches the designated site before any other part of the supplied region or attached point mass.

For each target, the four shots are independent fresh-rest preparations at the same orientation, with projectile masses m,m,m,m/2 and sites −a,0,+a,0. Their incoming speed is u. A common instantaneous frictionless law with e=0 acts at each boundary; there is no tangential or external impulse. Only the four labeled signed outgoing/incoming projectile velocity ratios and supplied reference masses/sites/axes are retained. This is not a sequence of shots on one evolving target.

Only the m-projectile shot at +a receives a candidate continuation. No gravity acts. The candidate imposes zero projectile force and zero resultant target force/torque after the impulse. For a rigid target, the latter statement does not set the individual constituent forces to zero: internal constraint forces can maintain the rigid mass pair's rotation. The continuation is tested against the finite exclusion, rather than assumed admissible.

## 2. Deriving the common four-shot record

For projectile mass μ at lower-face site x, write J e_y for the target's impulse. Linear and angular impulse balance, with the target initially at rest, give

    v = u − J/μ,
    V = (J/M)e_y,
    ω = Jx/I.

The contact's normal velocity is V_y+ωx. The centre-to-contact vector is (x,−d), so its cross product with the normal impulse is xJ: d does not enter the normal torque. The tangential contact velocity ωd is unconstrained by frictionless impact. The common e=0 condition is v−V_y−ωx=0. Consequently,

    H(x) = 1/M + x²/I = 1/(3m) + x²/(12ma²),
    D_μ(x) = 1/μ + H(x) > 0,
    J = u/D_μ(x),
    r_μ(x) = v/u = μH(x)/[1+μH(x)].               (2)

Thus H(±a)=5/(12m) and H(0)=1/(3m). Substituting, rather than assuming the planning values, gives the following table for each d:

| Shot | μ | x | J/(mu) | v/u | V_y/u | ωa/u |
|---|---:|---:|---:|---:|---:|---:|
| 1 | m | −a | 12/17 | 5/17 | 4/17 | −1/17 |
| 2 | m | 0 | 3/4 | 1/4 | 1/4 | 0 |
| 3 | m | +a | 12/17 | 5/17 | 4/17 | 1/17 |
| 4 | m/2 | 0 | 3/7 | 1/7 | 1/7 | 0 |

Every impulse is positive. The signed outgoing velocities are positive, which is consistent with e=0 and a moving target contact. The retained record is exactly

    (r_−,r_0,r_+,r_4) = (5/17, 1/4, 5/17, 1/7). (3)

For explicit comparison to the accepted inverse, y_j=1/(1−r_j) gives (17/12,4/3,17/12,7/6). With mass ratio q=1/2, the accepted inverse variable is

    t_inv = (q y_0−y_4)/(q−1) = 1,
    A = 1/12,       B = 0,       Y = 4/3.

The compatibility conditions t_inv∈[1/2,1], A>0 and Y>t_inv hold. The inverse returns e=0, c/a=0, M/m=3 and I/(ma²)=12. It neither identifies d nor supplies a finite collision region or a continuing-contact law. In particular, this pair is not an ambiguity in the four quantities the accepted inverse claims to identify. It is a same-record ambiguity in the later admissibility question.

## 3. Exact selected-shot free candidates

For the +a shot, (2) fixes the immediate post-impact state

    X_d(0) = (a,0),           C_d(0) = (0,d),
    Xdot_d = (0,5u/17),       Cdot_d = (0,4u/17),
    θ(0)=0,                  ω = u/(17a).         (4)

The normal contact velocities are equal at t=0: 5u/17 = 4u/17 + ωa. This is solely an instantaneous normal equality. For d=a the contact point also has tangential velocity ωa, whereas the projectile has zero tangential velocity; e=0 does not impose attachment.

The force-free candidates are therefore

    X_d(t) = (a,5ut/17),
    C_d(t) = (0,d+4ut/17),
    θ(t) = ut/(17a).

The predeclared time horizon is T=17πa/(4u), so θ ranges exactly over [0,π/4]. This dimensionless range is derived from the boundary angular velocity and the fixed horizon, not selected after testing the gap.

The target's occupied collision region at time t is

    B_d(t) = C_d(t) + R(θ(t))[B0−(0,d)],

where R is counterclockwise rotation. Inverting this rigid transformation maps the projectile back to the initial rectangle:

    q_d(t) = R(−θ)[X_d(t)−C_d(t)] + (0,d).

Because X_d−C_d=(a,aθ−d), direct matrix multiplication gives

    q_d,x = a cosθ + (aθ−d)sinθ,
    h_d = q_d,y = d(1−cosθ) + a(θcosθ−sinθ).       (5)

The sign of h is the inward sign at the lower face, and qx determines whether that face's finite span is relevant. Equation (5) agrees with the disclosed hypothesis only after this derivation.

## 4. Entire finite interval: signs, side/top edges and point masses

Write b=π/4, so 0<b<1. The endpoint t=0 has q_d=(a,0) in both geometries: it is the prescribed lower-face boundary contact and is retained. All following strict conclusions concern 0<t≤T, equivalently 0<θ≤b.

### Depth zero: the free candidate stays outside

For d=0 define

    f_0(θ)=h_0/a=θcosθ−sinθ,
    p_0(θ)=q_0,x/a=cosθ+θsinθ.

Their derivatives are

    f_0'(θ)=−θsinθ < 0,
    p_0'(θ)= θcosθ > 0             (0<θ≤b).

As f_0(0)=0 and p_0(0)=1, the exact finite bounds are

    (b−1)/sqrt(2) ≤ h_0/a < 0,
    1 < q_0,x/a ≤ (1+b)/sqrt(2) < sqrt(2) < 2.    (6)

Thus the projectile remains strictly below the lower face in target coordinates for every positive time in the interval. Its tangential projection remains strictly within the finite face and never reaches either side x=±3a. Its negative y coordinate excludes the upper face y=2a as well as the interior. There is no later lower-face recollision since h_0 never returns to zero. The body-frame point masses are (±2a,0); (6) excludes them by both the negative gap and the bound q_0,x<2a. At t=0 the projectile coordinate a is also distinct from ±2a. All corners and other finite boundary contacts are excluded. This candidate is geometrically admissible and strictly separated over (0,T] under the supplied zero-force dynamics and exclusion.

### Depth a: the free candidate penetrates the finite interior

For d=a define

    f_a(θ)=h_a/a=1−cosθ+θcosθ−sinθ,
    p_a(θ)=q_a,x/a=cosθ+(θ−1)sinθ.

Now

    f_a'(θ)=(1−θ)sinθ > 0,
    p_a'(θ)=(θ−1)cosθ < 0          (0<θ≤b),

because b<1. Starting at f_a(0)=0, p_a(0)=1 gives

    0 < h_a/a ≤ 1+(b−2)/sqrt(2) < 1,
    0 < b/sqrt(2) ≤ q_a,x/a < 1.                 (7)

The upper bound for h_a is strictly below 1 because b−2<0; its positivity follows from the positive derivative. Every positive time therefore satisfies

    −3a < q_a,x < 3a,       0 < q_a,y < a < 2a.

This is strictly inside the open forbidden rectangle. The formal candidate does not escape around an edge or pass through the upper face. It has no later lower-face boundary point, and neither side nor a corner is reached. The attached masses have initial coordinates (±2a,a); q_a,x<a and q_a,y<a exclude either mass even on this inadmissible formal path. They do not rescue its failed collision-region exclusion. At t=0 the only relevant projectile contact is again the specified lower-face point (a,0).

The two sign proofs and the finite coordinate bounds apply to every time in the required interval, not merely to a Taylor expansion or an infinite-line approximation. The depth-a failure occurs arbitrarily soon after the boundary and persists through T. It is therefore impossible for this exact free candidate to be the allowed post-impact trajectory in that geometry. Additional contact dynamics must change the proposed free evolution if an admissible actual continuation is to be specified. This packet does not choose or solve those dynamics, establish their uniqueness or existence for the given idealization, or infer universal sticking or separation from e=0.

## 5. Complete mechanical ledger

Use one fixed initial inertial origin O=(0,0) throughout. In two dimensions, r×p means r_x p_y−r_y p_x, with counterclockwise sign positive. Target angular momentum is always decomposed as its centre orbital term plus central spin; the projectile contributes its own orbital term.

For any of the four jumps, before impact P_before=μu e_y and L_O,before=μxu. Immediately after the jump,

    P_after = μv e_y + M V = (μv+J)e_y = μu e_y,
    L_O,after = (x,0)×(0,μv)
                + (0,d)×(0,J) + Iω
              = μxv + 0 + xJ
              = μxu.                                           (8)

Thus full-system linear and angular momenta are conserved for both depths in all four independent boundaries. There is no omitted target orbital term: it is explicitly zero about this origin because the target centre and its impulse both lie on the y axis. The impulse at (x,0) transfers xJ of angular momentum to target spin, independent of d.

For each selected-shot formal continuation, the full-system momentum is, at every t,

    P(t) = (0,5mu/17) + (0,12mu/17) = (0,mu).

The full angular momentum about the same fixed origin is

    L_O(t) = X_d(t)×m Xdot_d(t)
             + C_d(t)×M Cdot_d(t) + Iω
           = 5mau/17 + 0 + 12mau/17
           = mau.                                               (9)

Both orbital terms have been included. The target spin stays constant because the planar central inertia and angular velocity are constant. The centre and projectile positions evolve vertically, leaving their orbital values constant. The d=a formal candidate obeys (8) and (9) despite violating nonpenetration; these conservation identities cannot certify its geometric admissibility or describe a substituted contact trajectory.

At any jump the initial mechanical kinetic energy is μu²/2. The full outgoing value, including target translation and rotation, is

    K_after = μ(u−J/μ)²/2 + J²/(2M) + J²x²/(2I)
            = μu²/2 − uJ + J²D_μ(x)/2.

For e=0, J=u/D_μ(x), hence

    ΔK = K_before−K_after = u²/[2D_μ(x)] = uJ/2 > 0. (10)

For completeness the four separate immediate energy accounts are identical at both depths:

| Shot | K_before/(mu²) | ΔK/(mu²) | K_after/(mu²) |
|---|---:|---:|---:|
| 1, at −a | 1/2 | 6/17 | 5/34 |
| 2, at 0 | 1/2 | 3/8 | 1/8 |
| 3, at +a | 1/2 | 6/17 | 5/34 |
| 4, mass m/2 at 0 | 1/4 | 3/14 | 1/28 |

Only shot 3 continues in this packet. Its post-impact component energies are

    K_projectile = (1/2)m(5u/17)² = 25mu²/578,
    K_target,translation = (1/2)(3m)(4u/17)² = 48mu²/578,
    K_target,rotation = (1/2)(12ma²)[u/(17a)]² = 12mu²/578.

Their sum is 85mu²/578 = 5mu²/34. The loss from mu²/2 is 6mu²/17, agreeing with (10). Under each imposed formal force-free candidate all three speed magnitudes and ω remain constant, so K(t)=5mu²/34 on [0,T]. For d=0 this is the kinetic energy along the admissible candidate. For d=a it is merely the constant energy of the rejected formal path. No continuing-contact energy account is inferred for a replacement path.

The instantaneous restitution law supplies a loss of mechanical kinetic energy, not its microscopic destination. It does not assert conservation of mechanical energy across e=0 impact or supply the energy costs of four rest preparations, resets or an actual contact material.

## 6. Finite decision and supplied standards

The same record (3) identifies M/m, I/(ma²), c/a and e and is compatible with both explicit targets. Under the additional supplied finite collision geometry and candidate dynamics, the truth of free-flight admissibility over [0,T] differs between them. The record is therefore insufficient to decide that later property. Adequate state/premises for that decision must retain the normal centre position relative to the exclusion region (or equivalent geometry), along with whatever continuation/contact law is to be used. Equal instantaneous normal velocities alone do not settle it.

The supplied premises are the two ideal rigid mass distributions and massless collision structures, the rectangular unilateral exclusion, point projectiles, independent fresh-rest preparations and common axes, the exact frictionless e=0 boundary law, zero external force/torque for the candidate, and the predeclared finite horizon. Mass m and length a supply standards; u supplies speed and a/u the time scale. Absolute impulses use mu, angular momenta mau and kinetic energies mu². The four dimensionless ratios alone supply none of those absolute units and do not observe d. The horizon's physical registration and exact geometry are independent inputs, not consequences of the inverse.

The result is limited to exactly two depths, the four independent boundaries for each, and one selected-shot candidate per depth on [0,17πa/(4u)]. There was no simulator, numerical sweep, empirical execution, material validation, new contact-law solution, further restitution case, native-mass or gravity inference, efficiency claim, software maintenance or external outreach. Symbolic inequalities resolve the whole finite interval.

## Scientific review

Classical derived the two finite geometry cases and complete mechanical ledger. Its distinct reviewer checked the entire prescribed interval. Independent recipient review confirms that this preserves the prior inertia inverse while limiting its use for later continuation. Author report SHA-256 0ff272aba47b2609f7a8ab13e8780c0a3073f12c6a5c3a8fcaee4ff554626c3b; scientific review cf96b80d39f16671bae5cfc9498d52ee2cd06d95f1fbe59407150410a6e973ec; recipient review 422ac7aad103bd263b9aa6eea58a845d949b5b60020844c3cf32dfa8c0abdd8d.
