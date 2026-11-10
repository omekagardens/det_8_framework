# Local constituent rest mass from gravitating energy and pressure

**Decision.** For a nonempty massive gas alone, nonnegative principal pressures and $E>P_r+2P_t$ are necessary and sufficient locally. With $S=P_r+2P_t>0$ and $\Theta=E-S$, the exact constituent rest-energy inventory per static proper volume is
$$
                  \Theta<\rho_{\rm rest}c^2\le\sqrt{E\Theta}.
$$
The upper endpoint is attained; the lower endpoint is only an infimum. Zero gas pressure forces the cold value $E/c^2$. An unresolved nonnegative isotropic vacuum changes the sharp feasible set: whenever that model is feasible, the rest density has infimum zero, never attained by its stipulated nonempty massive gas.

## 1. Measured tensor and particle model

Andréasson and Rein give the local energy and principal-pressure integrals in Eqs. (2.5), (2.6) and (2.11). The construction below starts from a local particle measure. [Andréasson and Rein, gr-qc/0611053v1](https://arxiv.org/pdf/gr-qc/0611053v1)

Use the accepted static orthonormal frame, signature $(-+++)$, covariant components
$$
              T_{\hat a\hat b}=\operatorname{diag}(E,P_r,P_t,P_t),
$$
and zero momentum density. All three entries are finite, in energy-per-proper-volume units. The geometric-side cosmological term is zero by convention; an optional vacuum is kept explicitly on the matter side. The local inventory requested is the sum of invariant constituent masses in the static observer's proper volume, not the energy density divided by $c^2$, not a stress trace, and not a global mass integral.

## 2. Local mass-shell moments and what the trace measures

It suffices to use one arbitrary fixed species mass $m_0>0$. Let $d\nu(\mathbf v)$ be its nonnegative number measure per static proper volume, supported on $|\mathbf v|<c$, and let
$$
 \gamma(\mathbf v)=(1-|\mathbf v|^2/c^2)^{-1/2},\qquad
 d\zeta=m_0c^2\,d\nu.
$$
Atoms and cold streams are allowed. Finite total energy is assumed. Write
$\mathcal R=\rho_{\rm rest}c^2=\int d\zeta$. Then
$$
 E=\int\gamma\,d\zeta,\qquad
 P_i=\int\gamma\,\frac{v_i^2}{c^2}\,d\zeta,
 \quad (P_1,P_2,P_3)=(P_r,P_t,P_t).             \tag{1}
$$
Opposite beams used below cancel momentum density exactly and leave off-diagonal stresses zero. For a nonempty measure $\mathcal R>0$, while $\mathcal R\le E<\infty$.

Summing the pressure moments gives
$$
 S=P_r+2P_t=\int(\gamma-\gamma^{-1})\,d\zeta,\qquad
 \boxed{\Theta=E-S=\int\gamma^{-1}\,d\zeta.}     \tag{2}
$$
Thus $T^{\hat a}{}_{\hat a}=-\Theta$. The trace gap is a reciprocal-Lorentz-factor weighted rest-energy inventory, whereas $\mathcal R$ has no such weight. The chosen inventory per observer volume is frame dependent; the contracted stress trace has a different meaning. Zero total momentum density does not require every constituent to be at rest.

Since every particle is massive and strictly subluminal, a nonempty gas has $\Theta>0$, even if its speeds have no common bound below $c$. A positive finite energy with $S=E$ is therefore not attained by this model. Null particles or limiting velocities cannot be inserted at that boundary.

## 3. Complete feasibility and sharp gas-only range

The exact local gas-only consistency cases are:

| Measured tensor | Massive-gas decision and rest density |
|---|---|
| $E>0,\ P_r\ge0,\ P_t\ge0,\ \Theta=E-P_r-2P_t>0$ | Feasible and nonempty; ranges below |
| $E=P_r=P_t=0$ | Only the empty particle measure, with $\rho_{\rm rest}=0$ |
| Every other finite tensor | No positive massive-particle measure fits |

If a nonempty gas is required also in the first model, simply omit the empty case. The vacuum model below explicitly requires a nonempty gas and never uses that case.

Necessity follows from (1)–(2). The constructions in the next section prove sufficiency, with one fixed positive species mass and the measured anisotropy. Nonnegativity of the pressure sum alone is insufficient: each measured principal pressure must be nonnegative in the gas-only model.

When $S=0$, nonnegative pressure integrands force every occupied velocity to vanish. The unique rest inventory is
$$
                 \boxed{\mathcal R=E=\Theta.}  \tag{3}
$$
Its number measure may consist solely of the cold atom.

For $S>0$, (2) gives the strict lower inequality $\Theta<\mathcal R$. Equality would force $\gamma=1$ almost everywhere and contradict positive pressure. Cauchy–Schwarz with the positive measure $d\zeta$ gives
$$
 \mathcal R^2
 =\left(\int\sqrt\gamma\,\gamma^{-1/2}\,d\zeta\right)^2
 \le\left(\int\gamma\,d\zeta\right)
        \left(\int\gamma^{-1}\,d\zeta\right)
 =E\Theta.
$$
Therefore
$$
 \boxed{\mathcal R\in(\Theta,\sqrt{E\Theta}]
       \quad\text{when }S>0.}                  \tag{4}
$$
Equality at the upper endpoint requires one common Lorentz factor on the occupied particle support. It is attainable with different directions, so it does not require isotropic pressure. The next construction realizes every point of (4) and proves that its open lower endpoint is sharp.

## 4. Constructive local populations for all bounds and interiors

Assume $S>0$ and choose any finite
$$
             \Gamma\ge\Gamma_0=\sqrt{E/\Theta}>1,\qquad
             \beta_\Gamma^2=1-\Gamma^{-2}.
$$
For each static spatial axis $i$, assign total energy density
$$
 H_i=\frac{P_i}{\beta_\Gamma^2}
$$
to two opposite beams of speed $c\beta_\Gamma$, splitting the energy equally between them. Each beam has number density $H_i/(2\Gamma m_0c^2)$. Omit any pair whose measured pressure is zero. Add a cold population with energy density
$$
 E_0=E-\sum_iH_i
     =\Theta-\frac{S}{\Gamma^2-1}\ge0.          \tag{5}
$$
Its number density is $E_0/(m_0c^2)$. The radial beam pair and the two equal tangential beam pairs give precisely $P_r,P_t,P_t$, zero momentum and zero off-diagonal stress. If desired, the tangential pairs can be replaced by a uniform ring of the same total energy in the tangent plane, leaving the moments unchanged.

The total energy is $E$. All speeds are strictly below $c$, all weights are nonnegative, and their rest-energy inventory is
$$
 \mathcal R(\Gamma)=E_0+\frac{\sum_iH_i}{\Gamma}
                  =\Theta+\frac{S}{\Gamma+1}. \tag{6}
$$
At $\Gamma=\Gamma_0$, the cold population vanishes and (6) equals $\sqrt{E\Theta}$, attaining the upper endpoint. As $\Gamma\to\infty$, it decreases to $\Theta$, with no finite member attaining that lower value. For any specified $\mathcal R$ in (4), take the finite value
$$
                   \Gamma=\frac{S}{\mathcal R-\Theta}-1
$$
to realize it exactly.

Anisotropy and zero principal pressures cause no further local obstruction: the corresponding beam weights are simply zero. No constituent of any realization is massless. The limiting sequence has increasingly fast, increasingly sparse moving particles plus cold matter; it is not a population containing particles at speed $c$. These are local velocity measures, not an annulus-wide stationary solution.

## 5. Add one unknown nonnegative isotropic vacuum contribution

Now let the same observed total tensor be the sum of a vacuum with energy density $u\ge0$ and pressures $-u$, and a strictly nonempty massive gas. For each candidate $u$, the gas entries are
$$
 E_g=E-u,\qquad P_{rg}=P_r+u,\qquad P_{tg}=P_t+u,
$$
$$
 S_g=S+3u,\qquad \Theta_g=E_g-S_g=\Theta-4u.     \tag{7}
$$
The factor four is required by the vacuum's full stress trace, not by its energy alone.

Define
$$
          L=\max(0,-P_r,-P_t),\qquad U=\Theta/4.
$$
The exact vacuum feasibility interval is
$$
                    \boxed{L\le u<U.}         \tag{8}
$$
It exists precisely when $L<U$. Indeed the lower bound enforces all gas principal pressures and $u$ nonnegative, while the strict upper bound enforces $\Theta_g>0$. These imply $E_g=S_g+\Theta_g>0$, so no extra gas-energy condition is missing. Conversely every nonempty massive gas requires all these conditions. In particular a feasible total has $E>0$.

For every $u$ in (8), the sharp **joint** vacuum/rest-inventory set is:

| Gas at this $u$ | Allowed $\mathcal R=\rho_{\rm rest}c^2$ |
|---|---|
| $S_g=0$ | $\mathcal R=E-u=\Theta-4u$ |
| $S_g>0$ | $\Theta-4u<\mathcal R\le\sqrt{(E-u)(\Theta-4u)}$ |

These conditions, together with (8), are necessary and sufficient. Apply the cold construction or (5)–(6) to the gas entries and then add the stated vacuum tensor. The cold branch can occur only at $u=L$ with $P_r=P_t=-u$; its feasibility additionally has $E>u$, already contained in (8).

Every lower rest endpoint in the positive-pressure row is excluded, and each upper endpoint is attained by a finite-speed population. The vacuum endpoint $u=U$ is excluded: it would give zero gas trace gap, impossible for a nonempty strictly massive distribution. The tensor can be a perfectly valid geometric stress while failing this particular gas-plus-vacuum interpretation. For example a pure positive vacuum tensor $P_r=P_t=-E$ has $L=U=E$ and cannot contain the required nonempty massive gas.

## 6. What remains of a rest-mass lower bound

Suppose $L<U$. The upper endpoint
$$
              B(u)=\sqrt{(E-u)(\Theta-4u)}
$$
is continuous and strictly decreasing on $[L,U)$. Both factors are positive there and decrease with $u$. As $u\to U^{-}$, $\Theta_g\to0$, while $E_g$ has a positive finite limit: at $U>L$, both limiting gas principal pressures are strictly positive.

Consequently $B(u)\to0$. Each $B(u)$ is attained by its one-speed gas, and these populations remain nonempty at every finite stage. Varying $u$ therefore gives the exact projected rest-inventory range
$$
 \boxed{\mathcal R\in
       \left(0,\sqrt{(E-L)(\Theta-4L)}\right].}  \tag{9}
$$
Every point in this interval is attained: use the continuous upper-endpoint curve $B(u)$. Its largest value is attained at $u=L$. Zero is only an infimum and is never attained under the stipulated nonempty massive-gas condition. Thus feasible total stress observations do not force any strictly positive uniform lower bound when the vacuum contribution is unresolved.

Even an observed pressureless total $P_r=P_t=0,\ E>0$ illustrates the distinction. Gas alone is cold with $\mathcal R=E$. Gas plus vacuum permits $0\le u<E/4$ and the projected range $0<\mathcal R\le E$. Positive gas pressures $u$ can be cancelled by vacuum pressures $-u$; zero total pressure does not then certify cold constituents.

No rest mass is attributed to the vacuum in this inventory definition. Its contribution to the trace gap $\Theta$ is $4u$, and to $T^{\hat a}{}_{\hat a}$ is $-4u$; neither quantity alone supplies a constituent mass count.

## 7. Radius units, dimensional density and particle number

The orbit and tidal measurements supply
$$
 K_R=\frac{c^4}{8\pi G R^2},\qquad
 (E,P_r,P_t)=K_R(\bar E,\bar P_r,\bar P_t).
$$
Use all formulas above directly with the dimensionless barred stresses and
$\bar{\mathcal R}=\mathcal R/K_R,\ \bar u=u/K_R$. The dimensional mass inventory is
$$
 \boxed{\rho_{\rm rest}
   =\frac{K_R}{c^2}\bar{\mathcal R}
   =\frac{c^2}{8\pi G R^2}\bar{\mathcal R}.}     \tag{10}
$$
It has units of mass per the static observer's proper volume. Radius-unit observations give only these scaled bounds until $R$, or an equivalent dimensional radius/tick registration, is supplied with physical $c,G$. A common scaling of radius and time leaves the barred stress record unchanged and scales dimensional densities as $R^{-2}$.

If the gas is independently identified as one species of known invariant mass $m_0$, its static-observer number density is exactly
$$
                 n_{\rm stat}
                  =\rho_{\rm rest}/m_0
                  =\mathcal R/(m_0c^2).        \tag{11}
$$
Divide every applicable sharp rest-inventory interval by $m_0c^2$. In the cold gas-only case this gives the unique $E/(m_0c^2)$; in the positive-pressure case it gives the open/closed interval from (4), and in the unresolved-vacuum case the range from (9). The mean velocities and full distribution remain unmeasured.

No dimensionful constituent mass or species identification is supplied here. Taking a different positive $m_0$ and inversely scaling the number weights in the constructions preserves all stresses and rest-mass inventories while changing particle number. Neither the earlier fixture's baseline mass nor its tested response is a constituent-mass identification by name alone.

## 8. Local feasibility versus equilibrium and global mass

The constructions establish a nonnegative local mass-shell measure with the required tensor at one event. They do not solve a stationary Vlasov equation on an open annulus, satisfy prescribed radial boundary conditions, supply an equation of state or prove orbital, fluid or kinetic stability. Zero momentum and diagonal pressure at one event are not a proof of hydrostatic or kinetic equilibrium.

An inventory on a full static slice would require a registered density profile and the slice's proper volume. Its rest mass would integrate $\rho_{\rm rest}\,dV$, with no lapse weighting of the particle count. An exterior mass, a pressure-weighted gravitational integral, and an integrated local energy are different objects. The density-jump construction obtains a global baryon inventory only with its additional equation of state, number/chemical anchors and interface assumptions; none transfers to this unknown-speed local gas. This task supplies no interior completion, baryon normalization, binding model or universal fixture response.

Related constructions: [local stress from an orbit and tides](local_density_and_pressure_from_orbit_and_tides.md), [baryonic mass across a density jump](baryonic_mass_across_a_density_jump.md), and [fixture response from two free recoils](fixture_mass_response_from_two_free_recoils.md).
