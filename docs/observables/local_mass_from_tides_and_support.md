# Local mass inference from tides and signed support

**Result.** The radial and transverse tides fix the cosmological constant and the ratio of central mass to areal radius cubed. A compatible nonzero signed support reading fixes both radius and mass. At static balance the full record still permits a continuous interval of positive masses.

## Local tidal readings

Take the prescribed Kottler exterior with known positive G and c, central metric mass M > 0, cosmological constant Λ ≥ 0, and the event at unknown r > 0 with f(r) > 0. The primes on f denote spatial derivatives within one metric at fixed M and Λ. The observer released from rest follows a radial timelike geodesic by spherical symmetry and zero angular momentum. Choose its parallel orthonormal frame coincident at release with the static axes, radial axis outward. Initial relative velocities of the infinitesimally separated probes vanish. The radial eigenvalue R and either transverse eigenvalue H give relative acceleration per initial separation in the central geodesic's proper time. Spherical symmetry repeats H on the second transverse axis.

Vandeev and Semenova use the opposite metric signature and geometrized units. Their Eqs. 2–3 specify the same metric function f, and Eqs. 19–21 give the relative-acceleration coefficients in radial free fall. These coefficients depend only on position and apply at the instant of rest. Reversing a basis axis reverses both the component of separation and that of relative acceleration. Positive thus measures stretch, as the positive radial Schwarzschild coefficient confirms. Restore the length mass GM/c² and the proper length of elapsed time cτ. Converting two time derivatives contributes c². [Published equations, EPJ C 81, 610 (2021)](https://link.springer.com/article/10.1140/epjc/s10052-021-09427-8)

    f = 1 − 2GM/(c²r) − Λr²/3
    p = GM/r³,       b = Λc²/3
    R = −c² f″/2    = 2p + b
    H = −c² f′/(2r) = −p + b

Here p, b, R and H all have dimensions of inverse time squared. The signed acceleration of the holding apparatus is a separate channel. The freely falling central observer has zero proper acceleration.

## Exact feasible set for a finite pair (R,H)

Solving the linear system gives p = (R − H)/3 and b = (R + 2H)/3. Thus the pair is feasible exactly when

    R > H     and     R + 2H ≥ 0.

Necessity follows from p > 0 and b ≥ 0. These conditions imply R = 2p + b > 0. With either condition violated, the feasible set and its mass projection are empty. Otherwise define L = c/√R. At a candidate event compatible with the pair, f = 1 − (2p + b)r²/c² = 1 − (r/L)². The sharp joint set in the requested order and its mass projection are

    (M, Λ, r) = (pr³/G, 3b/c², r),    0 < r < L
    0 < M < pL³/G.

For every radius in this interval, the displayed parameters determine an exact allowed metric with positive f at the event and hence on a neighbourhood. A static observer and a geodesic launched with the same timelike tangent both exist there. Substitution gives exactly the pair. Conversely every solution has this form. The cubic is continuous and strictly increasing and takes every mass in the projected interval. The lower endpoint requires zero radius and mass. The upper endpoint has f = 0, where a fixed-coordinate worldline loses timelikeness. L bounds candidate radii across metrics compatible with the data. It is inferred from a tide and need not be a horizon location within any particular candidate metric. No areal-radius measurement enters the pair.

## Appending the signed support reading

In the stated metric a fixed-(r,θ,φ) future observer has Uᵗ = dt/dτ = 1/√f. Its radial four-acceleration is Aʳ = Γʳ_tt (Uᵗ)², with

    Γʳ_tt = −(gʳʳ/2)∂ᵣg_tt = c²ff′/2,
    Aʳ = c²f′/2.

The outward unit vector is √f ∂ᵣ, so the signed proper component a = g(A,√f ∂ᵣ) = Aʳ/√f is

    a = c²f′/(2√f) = (GM/r² − Λc²r/3)/√f = −Hr/√(1 − r²/L²).

Positive a denotes outward support. We took the field derivative inside one metric before restricting its value to the tidal solution family. Differentiating the identity f = 1 − r²/L² along that family would instead vary the mass. The tagged triple requires the same event parameters and coincident frames on matched preparations.

For fixed feasible tides put g(r) = r/√(1 − r²/L²). It has g′(r) = (1 − r²/L²)^(−3/2) > 0, with limits zero and positive infinity at the two open endpoints. Thus the range of a = −H g(r) is (0,∞) for H < 0, (−∞,0) for H > 0, and {0} for H = 0. The full inverse for finite real data is as follows.

| Tides and signed support | Feasible joint parameters |
|---|---|
| Infeasible tidal pair, any a | Empty |
| Feasible, H ≠ 0, aH ≥ 0 | Empty, including zero support |
| Feasible, H ≠ 0, aH < 0 | One triple with r = abs(a)/√(H² + a²R/c²), M = pr³/G, Λ = 3b/c² |
| Feasible, H = 0, a ≠ 0 | Empty |
| Feasible, H = 0, a = 0 | Entire tidal family 0 < r < L, with the same mass interval |

For the singleton, squaring yields a² = (H² + a²/L²)r². The stated root is positive and strictly below L because H² > 0. Its denominator has units of inverse time squared. The original unsquared equality holds because aH < 0 and both r and √f are positive. This establishes sufficiency and eliminates the reversed-sign solution introduced by squaring. The mass projection for a singleton consists solely of its stated mass.

At balance, H = 0 forces p = b = R/3 > 0, hence Λ = R/c² > 0 and GM = Λc²r³/3. Each member's static worldline at its chosen radius is itself geodesic. The distinct observer and apparatus preparations remain well-defined throughout the open interval. With Λ = 0, b = 0, R = −2H > 0 and H = −p < 0. Every positive support is attained uniquely at those tides, and zero or inward support is inconsistent. As r tends up to L at fixed tides, nonzero-branch support diverges in magnitude. On the balance family support stays zero up to the limit. The horizon endpoint itself admits no static observer in either case. As r tends to zero across compatible worlds, M tends to zero and support tends to zero. Radius zero and mass zero are both excluded.

## Two exact checks

Let T > 0 be a time scale. For the record (R,H,a) = (1/T²,0,0), choose r₁ = cT/2 and r₂ = cT/4. Their common cosmological constant is Λ = 1/(c²T²). Their masses are M₁ = c³T/(24G) and M₂ = c³T/(192G). Both have GMᵢ/rᵢ³ = 1/(3T²) = Λc²/3. The values of f at the events are 3/4 and 15/16, respectively. Thus two positive masses differing eightfold give precisely the same full record.

For an inward-support check take r = 3cT/5, M = 27c³T/(500G) and Λ = 3/(2c²T²). Then p = 1/(4T²) and b = 1/(2T²), giving R = 1/T², H = 1/(4T²) and f = 16/25. The acceleration is a = −3c/(16T), with units of length/time squared. Cosmological repulsion at this radius requires inward holding. The inverse denominator is 5/(16T²), recovering 3cT/5. The outward report of the same magnitude would violate aH < 0.

## Comparison and source scope

This conditional classical comparison uses a specified spherically symmetric static Einstein exterior, known G and c, calibrated time and lengths, and registered outward and tangential axes. Application to QR would require a mapping from its source and field preparations to this family and its central mass parameter, agreed event and preparation labels, negligible or bounded probe and apparatus backreaction, and independently calibrated responses and uncertainties for the differential tidal measurements and the signed static accelerometer. Resolving the balance case experimentally would also require treating the attainable precision around zero. The proofs use exact pointwise reports and establish parameter compatibility under the supplied model.

CL018 supplies context on directional tides and the Newtonian trace, CL026 on the scope of static-observer readings, and CL041 on dependence of tides on the prescribed field. The localized-source clock/freefall note supplies the existing weak-field protocol and calibration context. Their observables do not enter these equations. The selected published reference supplies only the forward metric and free-fall relative-acceleration coefficients. All inversions, the signed support derivation, admissibility proofs and witnesses above were obtained analytically for this packet.

## Scientific review and QR use

Classical’s independent CL072/v1 review verified the forward observables, both endpoints of the mass interval, signed support and the balance counterexample. An independent QR recipient assessment accepted this as a benchmark for a registered source and local instruments in the specified metric. The existing [weak-field clock and free-fall map](localized_source_clock_freefall.md) uses separate source and response assumptions.
