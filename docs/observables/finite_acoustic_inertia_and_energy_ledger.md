# Finite acoustic inertia and energy ledger

The instantaneous incompressible added-mass law does **not** reproduce either registered acoustic velocity. For the fixed pulse and material mass specified below, the acoustic velocity at one sound-crossing time is strictly larger than the incompressible value; at two sound-crossing times it is strictly smaller. Exact finite scalar integrals and analytic sign certificates establish both statements. The body, finite fluid annulus, prescribed-force work and independently calculated outer acoustic flux satisfy the complete energy ledger at both cuts.

## 1. Model, source context and limits

The incompressible comparison uses only the spherical case of the accepted
[material-mass and displaced-fluid analysis](material_mass_from_two_immersed_impulses.md):
ideal effective inertia is material mass plus half the displaced-fluid mass.
Its prolate inverse and calibration results are not premises here.

Public primary context is A. N. Norris, *Impedance of a sphere oscillating in an
elastic medium with and without slip*,
[arXiv:cond-mat/0601186v1](https://arxiv.org/html/cond-mat/0601186v1),
10 January 2006. Consultation covered the abstract and sections 1–2 through
equations (1)–(10); the beginning of section 3 was displayed but is not used.
This source concerns harmonic elastic/viscoelastic impedance and interface slip.
It supplies context, not a zero-past acoustic pulse solution or a fluid-limit
theorem. All equations for the response below follow from the supplied wave,
pressure and body laws.

Supply positive radius a, equilibrium fluid density ρ₀, sound speed cₛ and impulse J. Set

    D = 4πρ₀a³/3,   m = D,   T = a/cₛ,   V = J/D,
    s = t/T,   x = r/a,   u(s) = U(t)/V,   E₀ = J²/D.

Here D and m have mass units, T time, V velocity and E₀ energy. Coordinates and clocks, these scales and the constitutive/dynamical laws are supplied. The formal amplitude η=V/cₛ is small; the response is linear and the energy is its quadratic energy. There is no quantitative finite-amplitude nonlinear error bound or empirical apparatus claim.

The fluid is unbounded, initially quiescent, inviscid, irrotational and compressible, with zero potential and time derivative and zero past history. Its supplied equations in the reference exterior r≥a are

    φ_tt = cₛ² Δφ,   v_f = ∇φ,   p′ = −ρ₀φ_t.

The rigid sphere translates on z without rotation, with boundary φ_r(a,θ,t)=U(t)cosθ and tangential slip. Its actual pressure force and equation are

    F_f = −∮_(r=a) p′ cosθ dA,   D U_dot = F_ext + F_f.

There is no incoming or additional free wave. The reference boundary is fixed for this linearized fluid problem; no exact finite-displacement moving-domain solution is claimed. No shear, viscosity, thermal loss, vorticity, gravity or nonlinear convection is introduced.

The sole prescribed drive is F_ext=(J/T)f(s), where

    h(s) = 0                         (s≤0),
           10s³−15s⁴+6s⁵            (0<s<1),
           1                         (s≥1),
    f(s) = h′(s) = 30s²(1−s)²       (0<s<1), and 0 otherwise.

Thus h is globally C², f is C¹, f and f′ vanish at both pulse endpoints, and ∫₀¹f ds=1. No delta source or impulse substitution occurs. The only registered cuts are s=1 and s=2; the only observation annulus is 1<x<2.

## 2. The causal field and actual fluid force

Let a prime on y denote derivative with respect to its dimensionless argument, and set y and all derivatives used below to zero on negative arguments. Define ζ=s−x+1 and

    P(x,s) = y′(ζ)/x + y(ζ)/x²,
    φ(r,θ,t) = a V P(x,s) cosθ.                         (1)

To check the full wave equation, the scalar outgoing monopole y(s−x+1)/x solves the dimensionless three-dimensional radial wave equation for x>0. Minus its Cartesian z/a derivative is P cosθ. Spatial differentiation commutes with the wave operator. Equivalently, direct substitution gives P_ss=P_xx+2P_x/x−2P/x², the l=1 radial wave equation. This keeps both radial near-field terms; a plane-wave or far-field replacement would not do so.

The normal forcing is purely l=1. The constructed field therefore has the required angular sector. Within the causal smooth finite-energy class, any difference from it with the same data has zero external drive, zero initial body/fluid state, and homogeneous coupled boundary conditions. Multiplication by the corresponding velocities gives a nonnegative total body-plus-fluid energy with zero derivative and zero initial value. Causal finite-support propagation removes the flux at spatial infinity at every finite time. The difference vanishes (up to a constant potential fixed to zero by the preparation). This also excludes unforced higher harmonics or a hidden free field; an incoming-wave assumption has not been used as a substitute for initial data.

Useful derivatives of (1) are

    A(x,s) := P_x = −y″(ζ)/x − 2y′(ζ)/x² − 2y(ζ)/x³,
    B(x,s) := P/x = y′(ζ)/x² + y(ζ)/x³,
    C(x,s) := P_s = y″(ζ)/x + y′(ζ)/x².               (2)

Hence v_r=V A cosθ, v_θ=−V B sinθ and p′=−ρ₀cₛ V C cosθ. The normal boundary condition yields

    u = −y″−2y′−2y.                                    (3)

At x=1 the direct pressure-traction integral, using ∫cos²θ dΩ=4π/3, gives

    F_f(t) = (J/T)[y″(s)+y′(s)].                       (4)

The outward body-surface convention matters: p′ carries a minus sign and the force definition carries another. Equation (4), derived from the actual pressure, is the fluid-force law for this fixed preparation. It is not an instantaneous added-mass postulate.

The body equation is u′=f+y″+y′. Integrating once with zero initial values gives u=h+y′+y. Combining this with (3) gives the exact causal reduction

    y″+3y′+3y = −h,    y(0)=y′(0)=0,
    u = h+y′+y.                                       (5)

No arbitrary integration constant or unrecorded initial field has been removed. Equations (1), (4), (5) specify the entire registered solution.

For explicit finite quadratures define α=3/2, β=√3/2 and, for z≥0,

    H(z) = e^(−αz) sin(βz)/β,
    k(z) = H′(z) = e^(−αz)[cos(βz)−√3 sin(βz)].

For 0≤s≤2 the exact solution and required derivatives are

    y(s)  = −∫₀ˢ H(s−r) h(r) dr,
    y′(s) = −∫₀ˢ k(s−r) h(r) dr,
    y″(s) = −h(s)−3y′(s)−3y(s).                       (6)

These finite elementary-kernel quadratures are also explicit instructions for every energy integrand below. The use of (5) for y″ follows from the wave/body solution, not an energy residual.

The convolution solution has y∈C⁴ globally and is piecewise analytic at the retarded pulse endpoints; u∈C². Near s=0⁺, y=−s⁵/2+O(s⁶), y′=−5s⁴/2+O(s⁵), and y″=−10s³+O(s⁴). Thus (1) and its needed derivatives match the zero exterior state smoothly across ζ=0. The retarded endpoint ζ=1 is also sufficiently regular for the wave and energy integrations; no distributional force appears there. In particular the outer sphere x=2 has identically zero field for s≤1, including the front itself. At s=2 the causal front has passed x=2; the remaining response is not assumed to have cleared merely because the prescribed force ended at s=1.

## 3. Exact velocities and both comparison certificates

For convenience write the causal response to the fixed force as

    G(z) = 2/3 + k(z)/3,          z≥0,
    u(s) = ∫₀^min(s,1) f(r) G(s−r) dr.                (7)

This follows directly from (5)–(6): for a unit step h, u=1−H−∫H; its derivative is −H−k=k′/3 and its initial value is 1, giving G above. Superposition with f=h′ then gives (7). This derivation introduces no impulsive physical preparation; the actual smooth f is retained throughout.

The two exact dimensionless records are

    u₁ := D U(T)/J
        = 2/3 + (1/3)∫₀¹ 30r²(1−r)² k(1−r) dr,
    u₂ := D U(2T)/J
        = 2/3 + (1/3)∫₀¹ 30r²(1−r)² k(2−r) dr.      (8)

Every argument, coefficient and integration interval in these finite scalar integrals is fixed. They are exact values, not unspecified transfer-function claims or simulated approximations.

For the same drive and initial rest, the accepted ideal incompressible equation is (D+D/2)U_inc_dot=F_ext. Its dimensionless solution is u_inc(s)=(2/3)h(s). Therefore both comparison records equal 2/3.

**First cut: u₁>2/3.** Because f(r)=f(1−r), the excess is (1/3)∫₀¹f(r)k(r)dr. Put S(r)=e^(−αr)sin(βr), so k=S′/β. Integration by parts (f vanishes at both endpoints) gives

    u₁−2/3 = −(1/(3β))∫₀^(1/2) f′(r)[S(r)−S(1−r)]dr. (9)

For 0<r<1/2, f′(r)=60r(1−r)(1−2r)>0. To prove S(1−r)>S(r), set L(r)=log S(r) and q(r)=L(1−r)−L(r). Then

    q′(r)=2α−β{cot[β(1−r)]+cot(βr)} < 0.             (10)

Indeed cot is strictly convex on (0,π/2), both arguments lie in that interval, and their sum is β. Their cotangent sum is at least 2cot(β/2). Further, β/2=√3/4<π/6, so βcot(β/2)>β√3=α. Since q(1/2)=0, (10) implies q(r)>0 for r<1/2. The bracket in (9) is strictly negative on that open interval, proving the asserted strict excess without numerical evaluation.

**Second cut: u₂<2/3.** The ages z=2−r lie in (1,2). Rewrite

    k(z)=2e^(−αz)cos(βz+π/3).

For 1≤z≤2, π/2<βz+π/3<3π/2; equivalently π/6<βz<7π/6. These strict inequalities follow already from 3<π<4 and 4/3<√3<2. Thus k(z)<0 throughout the integration range, while f(r)>0 in its interior. The second excess in (8) is strictly negative.

There is no loss of positivity of the forward response hidden in this comparison: G(z)≥(2/3)(1−e^(−αz))>0 for z>0, and G(0)=1. Hence both u₁ and u₂ are positive. No optimal bound, late-time limit, sound-speed limit or additional observation is being inferred.

The causal acoustic state can therefore not be replaced by the instantaneous incompressible inertia law for these two registered observations. This is a regime/preparation distinction under supplied ordinary continuum laws. It does not turn the time-dependent fluid reaction into a change of the material mass D.

## 4. Independently specified finite energy records

All quantities below are divided by E₀=J²/D. At s=1 or 2, define the following exact records from (2), (6), (7):

    K_s/E₀ = u_s²/2,

    E_ann,s/E₀ = (1/2)∫₁² x² [A(x,s)²+2B(x,s)²+C(x,s)²] dx,

    W_ext,s/E₀ = ∫₀¹ f(z) u(z) dz,

    F_out,s/E₀ = −4∫₀ˢ C(2,z) A(2,z) dz.             (11)

For W_ext the integral is identical at the two cuts because f vanishes after 1. In its integrand u(z)=∫₀ᶻ f(r)G(z−r)dr, for 0≤z≤1, so the work is a completely specified finite double integral. The annulus record is a scalar integral with y,y′,y″ supplied by (6) at ζ=s−x+1. It includes both tangential kinetic energy (the 2B² term) and compressional energy (C²). At cut 1 the retarded arguments range from 0 to 1, and at cut 2 from 1 to 2; there is no omitted interior subvolume or missing near field.

To check the factors in (11), the physical acoustic energy density is

    e = (ρ₀/2)[|∇φ|²+φ_t²/cₛ²].

Using (2), ∫cos²θ dΩ=4π/3 and ∫sin²θ dΩ=8π/3 gives the annulus coefficient D V²/2=E₀/2. The physical energy-flux density is p′∇φ. Its radial component is −ρ₀cₛ V² C A cos²θ. Integrating over the fixed x=2 sphere and over dt=T ds gives exactly the −4 in (11). Positive F_out means energy leaving the annulus; no absolute-value or positive-part substitution has been made.

In particular, the two outer-flux records can be displayed with no implicit field notation:

    F_out,1/E₀ = 0,

    F_out,2/E₀
      = (1/4)∫₀¹ [2y″(w)+y′(w)]
                    [2y″(w)+2y′(w)+y(w)] dw.         (12)

The first equality uses the causal front, not conservation. In the second, substitute ζ=z−1 into the x=2 values of (2). As an independent sign/factor check, integration by parts in (12), using y(0)=y′(0)=0, gives

    F_out,2/E₀ = ∫₀¹ y″(w)²dw
                  + (3/4)y′(1)²+(1/2)y′(1)y(1)+(1/8)y(1)²
                = ∫₀¹ y″(w)²dw
                  + (3/4)[y′(1)+y(1)/3]²+y(1)²/24 > 0. (13)

Strict positivity follows from y″=−10w³+O(w⁴) near zero. The boundary terms in (13) are finite near-field contributions to the integrated flux. This identity does not assert that the instantaneous flux at every time is positive, or replace the signed flux definition by a radiation-zone approximation.

Equations (6)–(8), (11)–(12) are exact finite quadratures for every registered record. No energy term is defined as the difference of the others. These completely specified finite quadratures are exact values; a decimal evaluation or closed elementary expansion is not needed for the two comparison and balance statements.

## 5. Independent complete balance proof

The wave equation gives the local identity

    ∂_t e = ρ₀ ∇·(φ_t∇φ),
    ∂_t e + ∇·(p′∇φ)=0.                              (14)

For the fluid annulus, its inner outward normal is −e_r. Hence its inner outward flux is

    ∮_(r=a) −p′φ_r dA
       = −U∮_(r=a) p′cosθ dA = U F_f.

Therefore the actual integrated field equation is

    dE_ann/dt = −(outward flux rate at 2a)−U F_f.      (15)

The actual body equation, multiplied by U, gives

    dK/dt = U F_ext+U F_f.                            (16)

Adding (15) and (16) cancels the interface power once. Integrating with the zero initial preparation proves, independently of any evaluation of (11),

    K_s + E_ann,s + F_out,s = W_ext,s,   s=1,2.       (17)

Thus the explicit cut records satisfy

    u₁²/2 + (1/2)∫₁² x²[A(x,1)²+2B(x,1)²+C(x,1)²]dx
       = ∫₀¹ f(z)∫₀ᶻ f(r)G(z−r)dr dz,

    u₂²/2 + (1/2)∫₁² x²[A(x,2)²+2B(x,2)²+C(x,2)²]dx
       + (1/4)∫₀¹ [2y″+y′][2y″+2y′+y]dw
       = ∫₀¹ f(z)∫₀ᶻ f(r)G(z−r)dr dz.              (18)

The physical units of every line of (17) are energy. At the second cut, a strictly positive amount of acoustic energy has crossed the observation sphere, even though that sphere is not a wall. External work is the supplied actuator input; this is not the energy of a fully isolated actuator/body/fluid apparatus. Equilibrium background pressure has no omitted net body force or net power for this translating dipole: its angular integral against cosθ vanishes.

## 6. Finite conclusion and limitations

The finite verdict is strict mismatch at both cuts, with opposite signed velocity differences: U(T)>2J/(3D) and 0<U(2T)<2J/(3D). The causal outgoing solution, actual pressure force and complete finite energy ledger are explicitly supplied. The work/flux/field calculation uses the same pulse, boundary state and clock as the velocity comparison. No claim requires an empirical dataset, frequency scan or asymptotic horizon.

The consequence is conditional linear acoustics, useful as a finite comparison reference when deciding whether an observation can use an instantaneous added-mass law. It supplies no native unit/mass calibration, gravitational inference, heat/efficiency claim, physical sensor realization, microscopic driver model, nonlinear error guarantee or DET ontology validation. Outgoing radiation here means sound. It is distinct from the relativistic photon fluid in the [radiation-loaded membrane calculation](radial_energy_of_a_radiation_loaded_membrane.md): the media, speeds, states, boundaries and energy functionals differ. No coefficient or physical interpretation transfers between those models merely because both account for interface power.


## Scientific provenance

The Classical research programme admitted this finite result on 16 November
2026 after distinct nonblind scientific review. The reviewer had designed the
prospective question and disclosed outgoing-dipole/response and energy-cancellation
feasibility hypotheses, but did not author or edit the frozen result. The review
verified the complete response, both strict comparisons and independently
specified energy records without requiring a preferred sign.

A separate recipient assessment admitted the result as a conditional classical
reference under the same assumptions and limitations, reusing the completed
proof review. This article presents that accepted result; it adds no new
calculation, observation or physical qualification.
