# Enclosed mass from fourteen spherical accelerations

**Conditional result.** For exterior shell density of spherical harmonic degree at most five, the fourteen calibrated readings identify enclosed mass exactly:
$$
 M=\frac{R^2}{G}\left[\frac1{15}\sum_{\rm axes}u(n)
                         +\frac3{40}\sum_{\rm diagonals}u(n)\right].       \tag{1}
$$
These are per-direction weights for six axes and eight body diagonals. They follow from finite moments below. No shell amplitude or radial interior profile is fitted. Admitting degree six destroys identification from the **entire labelled fourteen-vector**. Two explicitly nonnegative mass preparations below have the same zero vector with enclosed masses 0 and μ>0.

This uses supplied Newtonian gravity and calibrated geometry, acceleration and source information. It supplies neither native units nor an apparatus or general source inverse. The angular band is an independent premise that these readings cannot certify.

## Source and observation

Fix G,R>0, the origin, Cartesian axes and common units. The regular nonnegative spherical interior is supported strictly inside R/2 and has unknown mass M≥0. Its radial density is unrestricted. The exterior is a finite nonnegative thin shell at a_s=2R, with real surface density σ(n) of harmonic degree at most L. The density, rather than an arbitrarily assigned field, is band limited.

The directions are exactly
$$
 N_A=\{\pm e_x,\pm e_y,\pm e_z\},\qquad
 N_D=\{(s_x,s_y,s_z)/\sqrt3:s_x,s_y,s_z=\pm1\}.
$$
At the same instant retain each signed inward scalar
$$
 u(n)=-n\cdot[g(Rn)-g(0)].
$$
The central subtraction removes any common uniform acceleration. All labels, signs, gains, source positions and probes are registered. Static conditions and negligible probe backreaction are supplied.

Spherical Newtonian shell integration gives Φ_int(r)=−GM/r outside the interior support. Thus g_int(Rn)=−GM n/R², while its well-defined central field is zero by symmetry. It contributes GM/R² to every reading, regardless of the radial density. This concerns enclosed mass, not central volume density: different regular radial profiles at fixed total leave these exterior-to-interior readings unchanged.

## Shell density to radial field

Write σ=∑_{l=0}^L σ_l for its harmonic projections, each with mass-per-area units. For real harmonics orthonormal under dΩ, the Newton kernel expansion and addition theorem give, for r<a_s,
$$
 \frac1{|a_s n'-rn|}=\frac1{a_s}\sum_{l\ge0}(r/a_s)^lP_l(n\cdot n'),\qquad
 \int\sigma(n')P_l(n\cdot n')d\Omega'=\frac{4\pi}{2l+1}\sigma_l(n).
$$
Using the actual surface element a_s²dΩ' yields
$$
 \Phi_{\rm ext}(r,n)=-4\pi Ga_s\sum_l\frac{(r/a_s)^l}{2l+1}\sigma_l(n),
$$
$$
 n\cdot g_{\rm ext}(rn)=4\pi G\sum_{l\ge1}\frac{l}{2l+1}
                                      (r/a_s)^{l-1}\sigma_l(n).             \tag{2}
$$
The finite angular expansion and its derivatives are regular at the probes, with R/a_s=1/2. The monopole gives a constant interior potential and no field. The degree-one potential is linear in Cartesian coordinates, so its uniform field is exactly removed by g(0). Higher-degree gradients vanish at the center. Tangential fields do not enter the radial scalar. Therefore
$$
 u(n)=\frac{GM}{R^2}-\sum_{l=2}^Lc_l\sigma_l(n),\qquad
 c_l=\frac{4\pi Gl}{2l+1}\,2^{1-l}>0.                                    \tag{3}
$$
In particular c_4=2πG/9 and c_6=3πG/52. The minus sign records the reduction of an inward reading by an outward shell pull. A positive density does not require every differential component to be positive.

Every positive-degree harmonic has zero normalized sphere mean. Thus the continuous mean of u is GM/R² and the continuous inward flux is 4πGM, for any finite L. The central subtraction has zero continuous flux as well. The question is whether fourteen point values reproduce that mean.

## Finite moments and the degree-five statistic

Let Qf=w_A∑_{N_A}f+w_D∑_{N_D}f, with weights constant on the two rotational orbits of this array. Normalization and the fourth coordinate moment require
$$
 6w_A+8w_D=1,\qquad 2w_A+(8/9)w_D=1/5.
$$
Their unique solution is w_A=1/15 and w_D=3/40, both positive. Uniform sphere moments follow from symmetry, n_x²+n_y²+n_z²=1 and (1/2)∫_{−1}^1t⁴dt=1/5.

| Monomial type | Normalized sphere mean | Q |
| --- | ---: | ---: |
| 1 | 1 | 1 |
| n_x² | 1/3 | 2/15+1/5=1/3 |
| n_x⁴ | 1/5 | 2/15+1/15=1/5 |
| n_x²n_y², x≠y | 1/15 | (8/9)(3/40)=1/15 |

For the mixed fourth moment, expand (n_x²+n_y²+n_z²)²=1. All monomials with an odd coordinate exponent vanish both under Q and under the sphere integral by sign reflection. The table and its permutations exhaust the remaining monomials of total degree ≤5. Hence Q is exactly the normalized integral for all restricted polynomials of that degree, and annihilates harmonics 1 through 5.

Applying Q to (3) for L≤5 proves (1). On every admitted record its value is the unique nonnegative enclosed mass. A negative value rejects this exact source/metrology model; it is not correct to reject individual negative radial components. No claim that this scalar alone verifies all assumptions or arbitrary-record compatibility is needed.

With all matter absent the full vector and statistic vanish. A nonzero uniform exterior shell also has no interior acceleration, so the observation never fixes total mass including the shell. At degree ≤5 a zero fourteen-vector forces M=0 on all admitted realizations, while allowing exterior monopole matter.

[Lebedev, Quadratures on the sphere (1976)](https://www.mathnet.ru/eng/zvmmf6092) is background only. Its bibliographic record was checked; no tabulated rule replaces the direct finite-moment proof.

## Degree six: a constant alias on every node

For Cartesian x=(x,y,z), r²=x²+y²+z², define homogeneous polynomials
$$
 H_4=x^4+y^4+z^4-\frac35r^4,
$$
$$
 H_6=x^6+y^6+z^6-\frac{15}{2}\sum_{i\ne j}x_i^4x_j^2+90x^2y^2z^2 .
$$
Let h_4,h_6 be their unit-sphere restrictions. They are pure degree-four and degree-six harmonics. Indeed Δ∑x_i⁴=12r² and Δr⁴=20r². For H_6, putting S_4=∑x_i⁴ and S_22=∑_{i<j}x_i²x_j² gives
$$
 \Delta\sum x_i^6=30S_4,\quad
 \Delta\sum_{i\ne j}x_i^4x_j^2=4S_4+24S_{22},\quad
 \Delta(x^2y^2z^2)=2S_{22}.
$$
The coefficients cancel exactly. Homogeneity and harmonicity give the claimed angular degrees and zero sphere means. Direct evaluation at the actual nodes gives

| Harmonic | Any axis | Any body diagonal |
| --- | ---: | ---: |
| h_4 | 2/5 | −4/15 |
| h_6 | 1 | 16/9 |

All sign-labelled nodes share their orbit's value. The allowed degree-six combination
$$
 F(n)=\frac{35}{44}h_4(n)+\frac{15}{22}h_6(n)                              \tag{4}
$$
therefore equals one at every node: 7/22+15/22=1 on the axes and −7/33+40/33=1 on the diagonals. Its continuous sphere mean remains zero. The nonzero degree-six term is essential; degree-four alone cannot have this alias under the degree-five quadrature.

No normalized weighting of these fixed nodes can integrate all degree-six harmonic combinations: its value on F would be one instead of zero. The following construction also rules out nonlinear use of the full record and supplies actual shell matter.

## Nonnegative source realization of the full-record ambiguity

Fix μ>0 in the supplied mass units and set
$$
 s_4=\frac{315\mu}{88\pi R^2},\qquad
 s_6=\frac{130\mu}{11\pi R^2},\qquad \sigma_0=8(s_4+s_6).
$$
Both coefficients are positive surface densities. Equation (3) gives
$$
 c_4s_4=\frac{G\mu}{R^2}\frac{35}{44},\qquad
 c_6s_6=\frac{G\mu}{R^2}\frac{15}{22}.
$$
Thus the actual density perturbation s_4h_4+s_6h_6 produces inward reading −(Gμ/R²)F(n).

Nonnegative total shell density is not merely asserted. On the unit sphere put u=x²,v=y²,w=z² with u+v+w=1. Then |h_4|≤1, ∑u³≤1, ∑_{i≠j}u_i²u_j≤uv+uw+vw≤1/3 and uvw≤1/27. Therefore
$$
 |h_6|\le1+\frac{15}{2}\frac13+\frac{90}{27}=\frac{41}{6}<7.
$$
It follows that σ_0+s_4h_4+s_6h_6≥7s_4+s_6>0 everywhere. Both shell preparations below are smooth in angle, finite and nonnegative.

**Preparation A:** no interior matter, M_A=0, and shell σ_A(n)=σ_0 at 2R. Its interior field is zero, hence g_A(0)=0 and every u_A(n)=0.

**Preparation B:** a regular spherical interior of mass μ, together with shell σ_B(n)=σ_0+s_4h_4(n)+s_6h_6(n). An explicit smooth interior density is μf(r), where
$$
 f(r)=C\exp[-1/(1-16r^2/R^2)]\quad(0\le r<R/4),\qquad f(r)=0\quad(r\ge R/4),
$$
and the finite positive C is chosen so 4π∫_0^{R/4}r²f(r)dr=1. This has support strictly inside R/2, is smooth at the origin and boundary, and has zero central acceleration. The shell uses only degrees 0,4,6, so its central acceleration also vanishes. Equation (3) now gives
$$
 u_B(n)=\frac{G\mu}{R^2}[1-F(n)].                                         \tag{5}
$$
At every one of the fourteen actual nodes, F=1 and u_B=0. Thus all fourteen labelled readings, the reference central field and signs agree exactly in A and B, with the same G,R, axes, timing and any common uniform acceleration. Yet M_B=μ≠0=M_A. No channel is discarded or relabelled.

The shell totals even agree: each is 4π(2R)²σ_0, since both perturbation harmonics have zero mean. In B the continuous flux is still 4πGμ, because the continuous mean of F is zero. These are nonnegative source distributions in the stipulated static Newtonian model, rather than arbitrary field functions. No material equilibrium or shell apparatus is asserted.

A belongs to the degree-five class; B first uses degree six. Both belong to the expanded class. Consequently no function of the entire fourteen-vector can identify M throughout that class: the same input vector would need to return both 0 and μ. This does not invalidate the degree-five statement on its own domain or the continuous flux law.

## Units, information and physical scope

Surface σ has units M/L², c_l has G units L³/(M T²), and u and c_lσ_l have L/T². The potential has L²/T², μf has M/L³, and the weights/harmonics are dimensionless. Hence (R²/G)Qu has mass units supplied by calibrated G, radius and acceleration. This normalization derives no native mass, length, clock or energy unit.

Physical use requires registration of all fourteen directions and radial signs, radius and central reference, simultaneous calibrated acceleration readings, negligible backreaction, static conditions, spherical interior support and an independently qualified exterior angular band. Source monitoring and those metrology premises are additional information. Agreement of the samples cannot certify their band: the exact full-record counterexample demonstrates that limitation. Noise, positioning/gain drift or approximate band limits require a separate error model.

The statistic concerns enclosed gravitating mass, not central density, external total mass, passive response or efficiency. CL076 addressed central density in two fixed positive templates. The accepted exterior-clock and finite-force results concern different records and source/response classes. Their science is reused only as scoped context. CL077's closed rotor cycles are independent. No thermal or software programme is reopened.

A competent conventional comparator with the same fourteen readings, physical constants and source-band information obtains the same result and the same boundary. Preparation, monitoring, reference, instrument and acquisition costs have not been measured; no physical energetic advantage is claimed. No hardware, simulation or apparatus model is introduced.

## Scientific review

DET Relational State Research supplied the derivation. A distinct scientific reviewer checked the shell response, finite moments, nonnegative source construction and the entire fourteen-component record. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `259c65f03c9321b2ee5b19c42c74f53fd6e8ad07171bc84a1020fc6548edf4a9`.
- Author report SHA-256: `1577880d5f3409c1768b2f9cbd327f1806adbb757483e749826cc625f1d52747`.
- Freeze SHA-256: `f46c3ecdec8d769d7c265175d724bea0c0a0a50149a0b5dbd999c26dd58a4522`.
- Independent scientific review SHA-256: `da357350719d0ed8df248fb2c8e484120fae7ed804789c379f6abc92ff5df248`.
