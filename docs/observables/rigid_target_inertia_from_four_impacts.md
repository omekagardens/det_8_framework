# Four impact readings identify a rigid target's inertia

The four exact signed projectile velocity ratios determine a unique finite positive target mass, positive central moment of inertia, tangential centre offset and common restitution coefficient whenever the compatibility test below passes. The changed projectile mass at the middle site separates restitution from the body's response. The three original readings alone admit a continuous family, including the explicit pair below. Normal centre depth and the detailed mass distribution remain unobserved.

This is a conditional conventional Newtonian boundary calculation. It supplies neither a native mass unit nor an empirical contact law. It concerns four fresh-rest instantaneous velocity jumps, not four consecutive impacts on a moving target, and not the trajectories between or after those jumps.

## 1. Premises and source use

CL023 supplies the distinction between translational and angular impulse ledgers, with Newton–Euler response supplied rather than derived from ontology. CL077 demonstrates transfer of an independent mechanical mass/inertia standard; it supplies no standard to this experiment. CL083 protects the distinction between an internally moving component and total target inertia. The present target is stipulated rigid, so its entire mass and central inertia enter its contact response. These inputs do not already imply a common restitution law or matched fresh-rest preparations: those are explicit additions in the control.

Take a fixed inertial laboratory basis with tangent unit vector **t**, normal unit vector **n** pointing into the initially stationary target, and **k** = **t** × **n**. A straight massless rigid face contains the three registered sites x = −a, 0, +a, with a > 0. The tangential centre coordinate is c; the normal centre depth is unrestricted by the readout. The target has finite M > 0 and finite planar central I > 0. Three reference projectiles have mass m > 0; the fourth has mass m′ > 0, m′ ≠ m, and repeats x = 0. All these masses and a are finite.

Before each shot the same unchanged body, or an exactly matched copy, is at rest in the same orientation. Each projectile is a point mass moving initially at u_j **n**, with finite u_j > 0. At the instantaneous boundary there is only one frictionless normal contact impulse. No tangential or external impulse acts during the jump; the contact geometry is fixed for that update. The common restitution coefficient e lies in [0,1]. The signed projectile outgoing normal velocity v_j is read immediately after the jump in the same inertial frame, with a known zero and common scale. It can be positive, zero or negative. All data are exact mathematical values; there are no measured data or noise estimates here.

## 2. One boundary: impulse, rotation and restitution

For a shot with projectile mass μ, site x and incoming speed u, let J **n** be the impulse on the target. Its opposite acts on the projectile. Write V for target centre velocity and ω for its scalar angular velocity along **k**. Linear and angular impulse balance give

    v = u − J/μ,
    V = (J/M) n,
    ω = J(x−c)/I.

The centre's normal depth drops out of the normal torque arm. The target contact point's normal velocity is

    w = V·n + ω(x−c) = J h(x),
    h(x) = 1/M + (x−c)²/I > 0.

Tangential contact-point velocity may be nonzero after an off-centre impact; frictionless contact does not constrain it. By the specified normal restitution rule,

    v − w = −e u.

Consequently, with D_μ(x) = 1/μ + h(x) > 0,

    J = (1+e)u / D_μ(x) > 0,
    v/u = r_μ(x) = [μ h(x)−e] / [1+μ h(x)],
    1−r_μ(x) = (1+e) / [1+μ h(x)].                 (1)

Every denominator is finite and strictly positive. The target's translational and angular velocities follow from the same J above; no target velocity observation has been added. At a centre-aligned site x = c the angular response is zero, while the translational response remains positive. For finite positive M and I, equation (1) implies

    −e < r_μ(x) < 1.

A zero impulse is impossible for finite u > 0 under this law. A zero outgoing projectile velocity is possible: it means μh(x) = e, requiring e > 0. A positive outgoing velocity is not evidence of an absent collision or negative impulse.

## 3. Complete compatibility test and inverse

Label the four ratios as r_−, r_0, r_+, r_4, where the first three use mass m at −a, 0, +a and the fourth uses m′ at 0. Define q = m′/m, so q > 0 and q ≠ 1.

First require that the registered inputs have finite positive m, m′, a and u_j, that m′ ≠ m, and that all v_j are finite. Then perform these exact tests in the stated order:

1. Require r_j = v_j/u_j < 1 for all four shots, and form

       y_j = 1/(1−r_j).

   These are finite positive numbers. A ratio r_j = 1 is excluded before this division; a ratio above 1 is incompatible with the positive impulse.

2. The two middle-site readings fix

       t = (q y_0 − y_4)/(q−1).

   Require 1/2 ≤ t ≤ 1. This includes both restitution endpoints. The known denominator q−1 is nonzero. In particular t = 0, or a t outside this closed interval, is rejected rather than assigned an infinite or inadmissible restitution.

3. Form the coefficients of the unique quadratic through the original three y values, using z = x/a:

       A = (y_+ + y_− − 2y_0)/2,
       B = (y_+ − y_−)/2,
       y(z) = A z² + B z + y_0.

   Require A > 0 before dividing by A. Define its vertex value

       Y = y_0 − B²/(4A),

   and require Y > t.

These conditions are necessary and sufficient. If any test fails there is no finite positive rigid target with the declared common e and preparation. If all pass, the complete inverse for the four requested parameters is

    e       = 1/t − 1,
    c/a     = −B/(2A),
    M/m     = t/(Y−t),
    I/(ma²) = t/A.                                  (2)

In particular M and I are finite and strictly positive. There is no second (M,I,c,e) solution for these four readings at fixed m,m′,a. There remains the intended freedom in normal centre depth, shape and mass distribution; equation (2) does not identify them.

### Necessity

Set t = 1/(1+e). From (1), for each original mass-m shot,

    y(z) = t[1 + m/M + (ma²/I)(z−c/a)²].            (3)

Therefore t lies in [1/2,1], A = tma²/I > 0, B = −2A(c/a), and Y = t(1+m/M) > t. At the repeated middle site the changed mass gives

    y_4 = t[1 + q m h(0)] = q y_0 + (1−q)t,       (4)

which fixes exactly the t in step 2. These identities prove every test and every recovered value in (2).

### Sufficiency and uniqueness

Suppose the tests pass and define (M,I,c,e) by (2). Completing the square in the data polynomial gives

    y(z) = A[z+B/(2A)]² + Y
         = t[1 + m/M + (ma²/I)(z−c/a)²].

Thus (1) reproduces the three original ratios. Equation (4), an identity from the definition of t, reproduces y_4 and hence r_4. All four impulses are finite positive, with the shared target parameters and e. Section 4 realizes those target parameters by one positive mass distribution. Conversely, equation (4) uniquely fixes t, while the three sites uniquely fix A,B,Y. Equations (2) then force all four requested parameters. The criterion therefore proves existence as well as exclusion and uniqueness, rather than merely fitting a formal quadratic.

### Boundary cases and strict exclusions

The t endpoints are included: t = 1/2 means e = 1 and t = 1 means e = 0. There is no singular inverse at either endpoint if A > 0 and Y > t. For e = 0, every ratio must be strictly between 0 and 1. For e = 1, ratios may be negative, zero or positive, but remain strictly between −1 and 1. All accepted ratios obey r_j > −1; data at or below −1 fail the tests. Indeed the original y values are at least Y > t ≥ 1/2, and y_4 = t + q(y_0−t) > t.

A = 0 is excluded even if B = 0: finite positive I and nonzero a force positive curvature. A < 0 is excluded as well. At A > 0, Y = t would require 1/M = 0, hence an infinite target mass, which is outside the control. Y < t would require a nonpositive target mass. These limiting descriptions do not enlarge the admitted domain. Very small positive A or Y−t are allowed exact finite values; no practical precision or stability claim follows.

The repeated middle reading must satisfy

    y_4−y_0 = (q−1)(y_0−t),   y_0−t > 0.

Thus increasing the projectile mass strictly increases its middle-site outgoing ratio. Equal middle-site ratios at distinct projectile masses are incompatible with a finite target here. This is also covered by the main tests: equality gives t = y_0 and therefore Y ≤ t. A zero outgoing ratio is admitted when compatible; a zero velocity change r_j = 1 never is. An equal-mass fourth projectile q = 1 would supply no equation for t, but that setup is explicitly outside the frozen experiment. No denominator at that forbidden setup is used.

## 4. One common positive-mass rigid target

For every accepted triple (M,I,c), let

    ρ = sqrt(I/M) > 0,
    d = 2ρ,
    L = a + |c| + ρ.

Use the face y = 0, −L ≤ x ≤ L, and attach two point masses M/2 at

    (c, ρ),   (c, 3ρ).

Connect them rigidly to the face with a massless scaffold lying on the y ≥ 0 side. The body is planar. Both masses are positive and finite; the centre is (c,2ρ), and the central moment is

    (M/2)ρ² + (M/2)ρ² = Mρ² = I.

The three registered face sites x = −a,0,+a are strictly inside the face and have the same inward normal **n**. An incoming point projectile from y < 0 reaches its designated face site without another contact at the boundary. The scaffold contributes no mass or inertia, exactly as the control permits. There is no hidden restriction tying I/M or c to a homogeneous face or prescribed outer size.

Use this same target geometry and mass distribution, reset to the same rest state and orientation, for the four shots. Assign the same stipulated restitution coefficient e to the four contacts. Each shot then has the torque arm x−c, the normal response h(x), and the impulse update already derived. This establishes one common-body realization of all four instantaneous boundary records. It does not derive e from the construction's material constitution, nor supply a finite contact-duration force history.

The relative normal velocity after each jump is v−w = −eu. At e > 0 this gives initial local normal separation at the contact. At e = 0 it gives equality of normal velocities at that instant only. Continued contact, separation, subsequent face rotation, possible recollision, and reset dynamics require additional evolution laws and are not established here. In particular, the e = 0 boundary is not asserted to make the point projectile permanently stick to the rotating body. The proof does not claim that four free subsequent trajectories implement the four supplied fresh-rest preparations.

## 5. Kinetic energy at each boundary

The initial target has no translational or rotational kinetic energy. For one shot,

    K_before = μu²/2,
    K_after  = μ(u−J/μ)²/2 + J²/(2M) + J²(x−c)²/(2I)
             = μu²/2 − uJ + J²D_μ(x)/2.

Substitution of J = (1+e)u/D_μ(x) gives the exact mechanical kinetic-energy loss

    ΔK = K_before−K_after
       = (1−e²)u² / [2D_μ(x)] ≥ 0.                (5)

For finite u > 0 and positive finite masses and inertia, equality occurs exactly at e = 1. Every 0 ≤ e < 1 has strictly positive kinetic-energy loss. The e = 0 loss is u²/[2D_μ(x)], with equal immediate normal contact velocities as above. This accounting includes the target's entire translational and rotational energies, including off-centre rotation. It is dimensionally an energy because D_μ has units of inverse mass.

For the four reset preparations the sum of their separate collision losses is

    Σ_j ΔK_j = (1−e²)/2 · Σ_j u_j² / D_{m_j}(x_j).

This is not the net energy cost of carrying out and resetting the experiment. The restitution law specifies the lost mechanical energy without identifying its microscopic destination. Dissipation and preparation/reset resources may involve an external reservoir; no reservoir closure or physical actuator is derived. A passive instantaneous velocity update and its nonnegative loss do not establish a later contact trajectory.

## 6. What the original three shots leave ambiguous

Remove only the changed-mass fourth reading. The first three positive y values still fix A,B,Y. Their exact finite-body compatibility condition is A > 0 and Y > 1/2, with all original r_j < 1. Every allowed target is then described by

    t ∈ [1/2,1] with t < Y,
    e = 1/t−1,
    c/a = −B/(2A),
    M/m = t/(Y−t),
    I/(ma²) = t/A.                                 (6)

Necessity follows from (3); sufficiency follows by the same construction as above. Because Y > 1/2, the allowed t interval always contains more than one point. Thus the three-shot domain has a continuous mass/restitution ambiguity, although c/a is already fixed. If Y ≤ 1 then t = Y is excluded by finite M; if Y > 1 the full closed interval [1/2,1] is available. No fourth velocity or additional control is used to establish this family.

Here is one explicit synthetic pair, using the same supplied reference mass m, spacing a, original incoming speeds u_−,u_0,u_+ > 0 and original three sites:

| Target | M | I | c | e | (r_−,r_0,r_+) |
|---|---:|---:|---:|---:|---|
| P | m | ma² | 0 | 1 | (1/3, 0, 1/3) |
| Q | 2m | (4/3)ma² | 0 | 1/2 | (1/3, 0, 1/3) |

For P the mass-m middle response is mh(0) = 1 and the side responses are mh(±a) = 2. For Q they are 1/2 and 5/4. Equation (1) gives the displayed identical ratios. The original outgoing velocities are exactly (u_−/3, 0, u_+/3) in both preparations, even when the three positive incoming speeds differ. Both restitution coefficients are positive, so this witness does not rely on assigning a subsequent evolution to an e = 0 contact.

Explicitly realize both targets on the same massless face y = 0, −2a ≤ x ≤ 2a, with a massless spine from (0,0) to (0,3a). For P attach masses m/2 at (0,a) and (0,3a). For Q attach masses m at

    (0, 2a−a sqrt(2/3)),   (0, 2a+a sqrt(2/3)).

Both centres have x = 0 and depth 2a. The masses are positive, lie on the spine, and give the respective moments ma² and (4/3)ma². All three contact sites and parallel normals are preserved. Each target is unchanged across its own repeated fresh-rest preparations.

For the prescribed changed mass m′ = qm at the middle site, their predictions are

    r_4(P) = (q−1)/(q+1),
    r_4(Q) = (q−1)/(q+2),
    r_4(P)−r_4(Q) = (q−1)/[(q+1)(q+2)] ≠ 0.        (7)

This separates the pair for every allowed finite q > 0, q ≠ 1, using the same fourth incoming speed in each candidate. Both denominators are positive. When q = 2 the predictions are 1/3 and 1/4; the conclusion itself does not restrict the frozen projectile mass to that example. The two candidates dissipate different energies while sharing the first three projectile ratios: P is elastic, while Q's losses from (5) are m u_0²/4 at the middle and m u_±²/6 at each side. That distinction uses unobserved target energies and does not add an observable to the three-shot record.

## 7. Standards, invariances and the finite claim

The supplied projectile mass establishes the mass scale; a establishes the length scale. The ratios alone, with known q and site labels −1,0,+1, identify

    e,   c/a,   M/m,   I/(ma²),

and therefore I/(Ma²) = (Y−t)/A. If m's absolute standard is unspecified, multiplying M,I,m,m′ by a common positive mass factor preserves every velocity ratio. If a's absolute standard is unspecified, multiplying all lengths, including c and the target geometry, by a common positive factor and I by its square preserves the same ratios. Thus M is determined relative to m even without an absolute length standard; c and I additionally require the appropriate supplied length scale. Neither the mass nor length unit is created by the impact law.

A common unknown positive velocity gain multiplies every incoming and outgoing signed velocity by the same factor and leaves v_j/u_j and the inverse unchanged. A known velocity zero is essential: an unknown additive offset generally does not cancel in these ratios. Absolute impulses and velocities require the velocity calibration, and absolute energies require its square along with the mass standard. The algebraic identifiability result therefore does not supply calibrated energy values from ratios alone.

The required preparations are one common rigid target and contact law, four rest resets in one inertial frame, the stated reference masses and spacing, signed common-zero velocity readout, and the instantaneous Newton–Euler/restitution update. No physical registration, experimental precision, mass–gravity relation, constituent mass law, DET ontology, native unit, practical collision material, or software system is inferred. The retained workload is exactly four independent impact boundaries, one common-body construction, one kinetic-energy identity and one explicit three-shot ambiguity pair. All calculations here are symbolic derivations; no empirical measurement, numerical sweep, scientific script or contact simulation was performed.

## Relation to the three recipient mass studies

**Boundary impulse with endpoint kinetic-energy certificates.** [Accepted comparison](inertial_mass_from_impulse_and_endpoint_energy.md). That network permits hidden relative motion and uses $J=M\Delta V+\Delta p$. Two independently certified endpoint kinetic-energy caps bound the unobserved momentum change and yield a conditional mass interval. Without those caps, its positive hidden-mass family has no upper mass bound from impulse alone. CL097 excludes those internal modes by its rigid-target premise and explicitly includes the allowed rotational response through $I,c$. Its inverse neither contradicts the network family nor supplies its missing energy certificates. Applying it to an uncharacterized deformable target would therefore exceed the accepted result. Rest preparation must cover the target's full relevant mechanical state, not merely a stationary visible marker.

**Total mass from two sampling intervals.** [Accepted comparison](total_mass_with_two_sampling_intervals.md). That result uses one continuous driven spring-network trajectory, a bounded number of modes, calibrated force and acceleration, and exact sample timing to isolate total mass. Its finite-precision ambiguity survives in its own unrestricted-frequency family. CL097 uses four reset rigid-target preparations and a stipulated contact model instead. Neither source establishes the other's preparation assumptions, and exact four-shot uniqueness gives no uniform finite-resolution or experimental robustness guarantee. One cannot replace the single continuous trajectory in the sampling result with independently reset runs.

**Two immersed impulses.** [Accepted comparison](material_mass_from_two_immersed_impulses.md). The immersed body's measured response contains material mass plus direction-dependent added fluid inertia. Its separation uses a fixed spheroidal geometry, an ideal-fluid model, centred impulses, principal directions and independent fresh-rest preparations. CL097's free rigid-target response has no such fluid term. An immersed target, attachments or an externally coupled medium cannot be inserted into this inverse unchanged and interpreted as material mass. Cross-assay comparison requires the same registered body/material state and system boundary, together with the independently justified medium model where applicable. The immersed unknown impulse gain leaves an absolute mass scale free; CL097 instead supplies the reference projectile mass scale.

## Standards, energy and QR boundary

The ratios determine $e,c/a,M/m,I/(ma^2)$. Absolute $M$ requires the supplied mass standard; absolute $c$ requires the length standard, and absolute $I$ requires both. An unknown common positive multiplicative velocity gain cancels, while an unknown additive velocity offset generally does not. Incoming and outgoing readings must retain the matched calibration required by the control. Absolute impulse and collision energy still require the appropriate speed calibration.

The donor's kinetic-energy balance includes target translation and rotation. Its nonnegative loss $(1-e^2)u^2/[2(1/\mu+h(x))]$ describes the immediate mechanical jump. It neither locates the lost energy microscopically nor prices projectile preparation, target restoration, measurement or reservoir reset. Summing four jump losses does not establish whole-experiment work or efficiency.

Recipient use is a conventional, conditional inertial comparator. No assignment of this Newtonian mass to a DET-native carrier or occupation variable, no native energy/unit calibration, no relativistic rest-mass identity, and no active/passive gravitational-mass relation follows. There is no gravity or native bridge promotion. The accepted endpoint-energy and immersed boundaries remain in force.
