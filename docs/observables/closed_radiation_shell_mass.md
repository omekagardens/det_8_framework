# A conserved radiation-shell source and its leading active mass

This independently reviewed conditional calculation fixes the supporting shell tension to τ = uR/6 and gives M_active = E_total/c² for the complete source in the stated linearized gravitational model. Supporting stress cancels the radiation contribution to the integrated spatial stress; the wall's energy remains included. These are results under supplied continuum assumptions, not native DET derivations or empirical calibration.

## 1. Fixed source and distribution convention

Use the supplied signature(-,+,+,+), x0=ct and c,G,R,u,σ>0. Write B_R for the ball, S_R for its boundary, V=4πR³/3 and A_S=4πR². Put p=u/3 and P_ij=δij−n_i n_j on S_R, where n=x/R there. The source is exactly

\[
\begin{aligned}
T_{00}&=u\mathbf1_{B_R}+\sigma c^2\delta(r-R),&T_{0i}&=0,\\
T_{ij}&=p\delta_{ij}\mathbf1_{B_R}-\tau P_{ij}\delta(r-R).
\end{aligned}
\]

The radial delta means ∫f(x)δ(r−R)d³x=∫_{S_R}f dS. The shell lies away from the origin because R>0; n is used only on the shell. σ is independent of τ. No material equation of state, energy condition, external support or extra source is assumed.

All conservation statements below are distributions on the whole of R³. Static T00 and zero T0i make the energy component of flat-background conservation immediate. The nontrivial condition is ∂iTij=0. Raising spatial indices makes no sign change, and the two time indices in T00 also leave its energy-density value unchanged.

## 2. Distributional conservation fixes the tension

Let f be any smooth compactly supported vector test function. The definition of distributional differentiation and the divergence theorem give

\[
\begin{aligned}
\langle\partial_iT_{ij},f_j\rangle
&=-p\int_{B_R}\partial_j f_j\,d^3x
  +\tau\int_{S_R}P_{ij}\partial_i f_j\,dS\\
&=-p\int_{S_R}n\cdot f\,dS
  +\tau\int_{S_R}P_{ij}\partial_i f_j\,dS.
\end{aligned}
\]

For the second term, decompose f on the sphere into its tangential part f_T and normal part (n·f)n. The integrated surface divergence of f_T is zero on the closed sphere. The normal part contributes (2/R)(n·f), since the sphere has two tangent directions and ∂_i n_j=(δij−n_i n_j)/R there. Hence

\[
\int_{S_R}P_{ij}\partial_i f_j\,dS
=\frac2R\int_{S_R}n\cdot f\,dS.
\]

Consequently

\[
\boxed{\partial_iT_{ij}
=\left(\frac{2\tau}{R}-p\right)n_j\delta(r-R).}
\]

This formula is sufficient when its coefficient vanishes. It is also necessary: choose a smooth compactly supported f equal to x in a neighborhood of S_R, for which ∫_{S_R}n·f dS=R A_S>0. Thus conservation holds if and only if 2τ/R=p, giving τ=uR/6>0.

This test-function derivation includes both shell and origin. It never differentiates a fictitious continuation of n through r=0, so there is no hidden point-source term. There is no volume force away from S_R, and the shell divergence term cancels the radiation boundary term. No external tether is left in the distributional divergence.

## 3. Complete energy and spatial-stress integrals

The complete energy is

\[
E_{\rm total}=E_{\rm rad}+E_{\rm wall},\qquad
E_{\rm rad}=uV,\qquad E_{\rm wall}=\sigma c^2 A_S.
\]

For the spatial stress, spherical symmetry gives

\[
\int_{S_R}n_i n_j\,dS=\frac{A_S}{3}\delta_{ij},
\qquad
\int_{S_R}P_{ij}\,dS=\frac{2A_S}{3}\delta_{ij}.
\]

Therefore

\[
\int T_{ij}\,d^3x
=\left(pV-\frac{2\tau A_S}{3}\right)\delta_{ij}=0
\]

at the derived tension. In particular,

\[
\int\sum_i T_{ii}^{\rm rad}\,d^3x=3pV=E_{\rm rad},\qquad
\int\sum_i T_{ii}^{\rm wall}\,d^3x=-2\tau A_S=-E_{\rm rad}.
\]

This is an integrated cancellation. Neither local radiation pressure nor local shell stress vanishes. The source energy still includes the wall's independent positive energy E_wall.

## 4. Whole-space field compatibility and the monopole

The supplied equations and boundary convention are

\[
\nabla^2\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu},
\qquad
h_{\mu\nu}=\bar h_{\mu\nu}
-\tfrac12\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta},
\qquad \bar h_{\mu\nu}\longrightarrow0\quad(r\to\infty).
\]

Since ∇²(1/|x|)=−4πδ³(x), their whole-space Newton-potential solution is

\[
\bar h_{\mu\nu}(x)=\frac{4G}{c^4}
\int\frac{T_{\mu\nu}(y)}{|x-y|}\,d^3y,
\]

where surface terms are interpreted using the stated delta measure. Each source component is a compact finite measure with smooth volume or surface density; its potential is well defined, regular off the prescribed source, finite at the origin and decaying at infinity. No extra point source is introduced. The difference of two allowed solutions is a harmonic distribution on all space. It is therefore smooth; decay at infinity and the harmonic uniqueness principle make it zero. A singular 1/r addition would carry an extra delta source and is excluded, not an allowed integration constant.

Conservation also supplies the de Donder compatibility. Differentiation of the convolution and distributional integration by parts give ∂i bar(h)_iν as the Newton potential of ∂iT_iν, which vanishes. Time derivatives vanish. Thus the decaying solution obeys ∂^μ bar(h)_μν=0. This is why an unconserved radiation-plus-wall-energy ledger cannot simply be used in the same gauge system after omitting its supporting stress.

For r=|x|→∞, compact support implies

\[
\bar h_{\mu\nu}(x)=\frac{4G}{c^4r}
\int T_{\mu\nu}\,d^3y+O(r^{-2}),
\]

with fixed source-dependent constants in the remainder. Only the leading coefficient is used. With the supplied signature,

\[
h_{00}=\tfrac12\left(\bar h_{00}+\sum_i\bar h_{ii}\right),
\]

so the leading active mass is

\[
M_{\rm active}=\frac1{c^2}
\int\left(T_{00}+\sum_iT_{ii}\right)d^3y.
\]

The spatial-stress integral from section3 vanishes. Hence h00=2G E_total/(c⁴r)+o(1/r), which proves the result stated above in the fixed asymptotic convention. This coefficient is not asserted to be an arbitrary-gauge local observable or an apparatus output.

The complete monopole ledger is:

| Component of this one source | Energy integral | Spatial-trace integral | Contribution to c²M_active |
| --- | ---: | ---: | ---: |
| Radiation | E_rad | E_rad | 2E_rad |
| Supporting wall | E_wall | −E_rad | E_wall−E_rad |
| Complete source | E_rad+E_wall | 0 | E_rad+E_wall |

If one keeps the radiation pressure term and wall energy but drops the wall stress from this ledger, the apparent numerator becomes 2E_rad+E_wall, exceeding the correct one by E_rad. That omission also leaves ∂iTij=−p n_jδ(r−R), so it is not another isolated equilibrium or a compatible source of the stipulated full gauge system. This is a diagnosed bookkeeping error inside the fixed comparison, not a second cavity calculation. Component ledger entries need not all be positive because no material energy condition was imposed; the complete active mass is positive for the supplied parameters.

## 5. Weak-field and unit ledger

Let

\[
q=\frac{\sigma c^2}{uR},\qquad
 t=\frac{\tau}{uR},\qquad
 g=\frac{GuR^2}{c^4},\qquad
 M_\star=\frac{uR^3}{c^2}.
\]

The supplied weak-field conditions are g≪1 and gq=GσR/c²≪1. Conservation gives t=1/6. The characteristic field contribution of the shell stress scales as

\[
\frac{G\tau R}{c^4}=gt=\frac g6,
\]

so the derived tension introduces no additional large gravitational scale beyond the already declared radiation scale. Radiation, wall energy and wall stress all remain at their appropriate retained order. This checks ordering; it is not an all-orders error bound or a proof of stable self-gravitating equilibrium.

The dimensionless results are

\[
\boxed{t=\frac16,\qquad
\frac{E_{\rm total}}{uR^3}
=\frac{M_{\rm active}}{M_\star}
=4\pi\left(\frac13+q\right),\qquad
\frac{M_{\rm active}c^2}{E_{\rm total}}=1.}
\]

R is a supplied length, u an energy per volume, σ a mass per area and τ an energy per area. δ(r−R) has inverse-length units. Thus every source component has energy-density units; G T/c⁴ has inverse-length-squared units, consistent with dimensionless h. M_star is an energy divided by c² and has mass units.

These dimensionless combinations and ratios do not change under a consistent change of measurement units. Choosing M_star as a normalization does not determine its numerical physical value, q, G or c. The source state, continuum coordinates, radiation equation of state, gravitational coupling and calibration meanings remain supplied.

Matter is held at zeroth order while the metric is computed to first field order. Self-gravity corrections to the shell/radiation equilibrium, gravitational binding energy and nonlinear field terms are not computed. The equality above is the exact coefficient identity in that approximation, not a claimed equality including uncalculated corrections. No remainder bound for a full nonlinear solution is supplied.

## 6. Meaning for the programme and remaining limits

This gives one complete conventional source baseline: pressure participates in the gravitational source, and supporting stresses must accompany the energy whose static configuration they maintain. The cancellation concerns this closed source's integrated monopole, not a universal permission to ignore pressure or spatial stress locally. It provides a concrete energy-and-stress relationship that a claimed native source mapping would need to address in the corresponding regime.

The calculation supplies neither a native stress tensor nor an inertial-response experiment for this cavity. The [conditional boost comparison](conditional_boost_mass_relation.md) concerns a different supplied two-level model and is not used to infer the kinetic mass of this shell. There is no new equivalence-principle derivation, quantum reconstruction, native geometry, physical mass spectrum or empirical validation here.

σ was independent of τ throughout. No constitutive law, satisfaction of a material energy condition, manufacturing possibility, cavity stability or load/unload energy accounting has been proved. There is no second source, time evolution or inverse source reconstruction. The mathematical result is not a claim that a physical apparatus can measure the ideal coefficient without calibration.

The reusable result is this complete source ledger. It does not by itself establish the inertial response of the same cavity.
