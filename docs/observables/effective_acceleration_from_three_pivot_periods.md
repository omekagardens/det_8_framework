# Effective acceleration from three pivot periods

In an inertial laboratory, three labeled periods determine the uniform field strength `g` for a pendulum with unit passive-to-inertial mass ratio, the nearest pivot's distance `s` from the centre, and the radius of gyration `k` whenever the data satisfy the test below. The test applies to both monotone and nonmonotone records. The body's mass remains a free positive scale. The inertial and passive mass centres coincide in this construction.

## The period measured by the clock

Write `h>0` for a pivot's distance from the centre, and take the stable downward orientation as angle zero. The parallel-axis theorem gives `I_h=m(k²+h²)`. The gravitational potential is `mgh(1−cos θ)`, so the torque is `−mgh sin θ`. The ideal pivot does no work. Release from rest at `θ*` gives

    I_h θ̈ = −mgh sin θ,
    ½ I_h θ̇² = mgh (cos θ − cos θ*).

The acceleration initially points toward zero, and the speed is positive in the interior of the swing from `+θ*` to `−θ*`. Reflection in the downward vertical and time reversal give four equal quarter swings up to the first return to the release extremum at rest. For `q=sin(θ*/2)`, substitute `sin(θ/2)=q sin φ` in the elapsed time from release to the downward vertical. This gives

    T/4 = √[I_h/(2mgh)] ∫₀^(θ*) dθ / √(cos θ − cos θ*)
        = √[I_h/(mgh)] K(q),
    K(q) = ∫₀^(π/2) dφ / √(1 − q² sin²φ).

Here `q` is the elliptic modulus. Since `0<q<1`, the last integrand is positive and bounded by `(1−q²)^(-1/2)`. The specified return is therefore finite at every admitted pivot and release angle. With the same dimensionless factor `F=4K(q)` for all three runs, the clock reads

    T_j = F √[(h_j + k²/h_j)/g],       h_j = s + jd,  j = 0, 1, 2.

Rossi and Zaninetti give the physical-pendulum dynamics in equation (62). The equally spaced fixed-body inverse here follows from the supplied geometry and the exact energy integral. [Rossi and Zaninetti, arXiv:physics/0510010v1](https://arxiv.org/pdf/physics/0510010v1)

## Complete data test and reconstruction

Require all three labeled periods to be finite and positive. Define the normalized squared periods `y_j=(T_j/F)^2`. Their half second difference and half outer difference are

    C = (y₂ − 2y₁ + y₀)/2,       E = (y₂ − y₀)/2.

The observations are admissible exactly when all the following conditions hold.

1. `C>0`.
2. `y₂<2y₁`.
3. Either `E≥0`, or `E²<C(y₁+C)`.

These comparisons are homogeneous in the three squared periods, so the common factor `F²` cancels from the accept/reject decision. Use the normalized readings for the reconstruction, which gives

    t = [−E + √(E² + 8C(y₁+C))]/(4C),
    a = E + Ct,       b = Ct(t²−1),
    s = d(t−1),       g = d/a,       k = d√(b/a).

To prove the test, set `t=(s+d)/d>1`, `a=d/g>0`, and `b=a(k/d)^2>0` in the forward law. It becomes `y_j=a(t+j−1)+b/(t+j−1)`. Direct differences at the middle pivot give

    C = b/[t(t²−1)],       E = a − b/(t²−1) = a − Ct.

Thus `C>0`, and substitution into `y₁=at+b/t` gives `P(t)=0` for the quadratic

    P(t) = 2Ct² + Et − (y₁+C).

For `C>0` and positive data, its constant term is strictly negative. Its roots have opposite signs, and the displayed radical is the unique positive root. For any nonnegative `z`, `z<t` holds exactly when `P(z)<0`. In particular, `P(1)=y₂−2y₁`, proving that the second condition is exactly `t>1`. Then `b>0`. If `E≥0`, `a=E+Ct>0` follows. If `E<0`, `a>0` requires `t>−E/C`. Evaluating `P(−E/C)=E²/C−(y₁+C)` proves the third condition. Its strict inequality is equivalently `2y₀y₂>y₁(y₀+y₂)`.

Conversely, given a triple passing the tests, the reconstructed `a,b,t` are physical. The predicted middle reading is `2Ct²+Et−C=y₁`, while the predicted differences give exactly `C,E`. The outer readings are consequently `y₁+C−E` and `y₁+C+E`, as recorded. Positive square roots recover the original clock times. Any admitted solution must use that same positive root and the same `a,b`.

The adjacent squared-period increments are `E−C` and `E+C`. For `C>0`, `−C<E<C` is the valley case, `E=±C` gives an adjacent equality, `E>C` gives two increases, and `E<−C` gives two decreases. `E=0` permits equal outer readings. The signs of adjacent increments agree with those of the raw periods. Curvature is tested on their squares. For example, at fixed positive `s,d,g`, the raw periods approach a constant times `√(s+jd)` as `k` tends to zero. Strict concavity in that limit gives a negative raw second difference even for sufficiently small positive `k`. A zero or negative squared-period second difference is impossible because `b>0` and `t>1`. For `C>0`, `y₂=2y₁` gives the excluded zero offset. For `E<0`, equality in the third condition gives `a=0`, incompatible with a finite positive `g`. Crossing either boundary in the opposite direction also fails its required positivity. A vanishing `k` would give zero curvature at a positive offset.

## One unchanged body and its mass scale

In the body plane put the centre at `(0,0)` and three bearing points at `(s+jd,0)`. A massless rigid frame holds particles of masses `M/2` at `(0,k)` and `(0,−k)`, for any `M>0`. The centre of mass is the origin, its central moment about the perpendicular axis is `Mk²`, and its pivot moments are `M(k²+h_j²)`. Orient the bearing axes horizontally, perpendicular to the body plane. The same frame and mass pair can be released in each suspension at the prescribed angle from its own downward equilibrium. This construction realizes every accepted solution for all three trials. At fixed readings the complete set of mass and central moment pairs is `(m,I_CM)=(M,Mk²)` with `M>0`. The determined ratio is `I_CM/m=k²`.

## Omitting the last clock reading

Fix any time `τ>0`, mass `M>0`, spacing `d>0` and allowed release angle. Use the preceding frame construction for each preparation.

| Preparation | `s` | `k²` | `g` | `(T₀/F)^2` | `(T₁/F)^2` | `(T₂/F)^2` |
| --- | --- | --- | --- | --- | --- | --- |
| A | `d` | `2d²` | `3d/τ²` | `τ²` | `τ²` | `11τ²/9` |
| B | `2d` | `6d²` | `5d/τ²` | `τ²` | `τ²` | `11τ²/10` |

In each body `k²=s(s+d)`, so `h+k²/h` takes the same value `2s+d` at either of its first two pivots. The two bodies thus reproduce the same labeled pair of full returns `Fτ,Fτ` in different gravitational fields. The final column is the prediction for the suppressed observation.

## Unknown passive coupling and supplied units

For an inertial mass `M` and passive mass `λM` at the same centre, the moment of inertia is still `M(k²+h²)`, while the torque is `−λMgh sin θ`. All three time formulas then depend on `G=λg`. The same data tests apply and the reconstruction returns `G=d/a`, `s`, and `k`. For each `u>0`, setting `g=u` and `λ=G/u` gives the identical three timings, with the independent inertial mass scale `M>0` still free. Conversely any matching pair must satisfy that product, by the uniqueness proof. Here `u` has the acceleration units of `G`.

The measured spacing sets the length unit, the elapsed-time clock sets the time unit, and `a,b` have units of time squared. Thus `s,k` are lengths and `d/a` is measured in length per clock-time squared. Interpreting that value as field strength uses the specified unit passive-to-inertial ratio. These conclusions concern three exact returns in a supplied Newtonian model. CL077's independent ballast standard enters only as a comparison with a different way of measuring inertia.

## Using the pendulum as a reference

The ratios `s/d`, `k/d` and `I_CM/(M d²)` can be recovered from period ratios. A common clock gain and the common release-angle factor cancel. Recovering the acceleration in length per time squared requires the measured spacing, clock calibration and the release angle.

In an inertial laboratory the pendulum measures `λ_p g`, where `λ_p` is its passive-to-inertial mass ratio. In a nonrotating laboratory accelerating vertically downward at `a`, the restoring acceleration has magnitude `|λ_p g − a|`. The equilibrium orientation supplies the sign relative to the designated downward direction. At equality the pendulum has no restoring swing. One such reading leaves the coupling, field and laboratory acceleration underdetermined.

Using the pendulum to calibrate immersed supports requires a matched material response or an independent relation between responses. Using it with gravity-bound modes likewise requires registration to the measured sector. Even with that match, an absolute action requires further scale and inertial-mass information. [Immersed support loads](passive_gravity_from_two_immersed_support_loads.md) · [Gravity-bound modes](gravity_bound_modes_action_and_acceleration.md)
