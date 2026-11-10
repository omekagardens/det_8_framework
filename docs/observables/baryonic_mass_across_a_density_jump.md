# What fixes the baryonic rest mass across a density jump?

One registered baryon density in the outer phase determines the whole star’s baryonic rest mass **if the same baryon charge can equilibrate across the interface**. If transfer and conversion are frozen, one additional scalar material measurement is necessary and sufficient. Pressure continuity gives mechanical balance in both cases. Only chemical equilibrium fixes the ratio of the inner and outer baryon densities at the jump.

## Reconstruction on each side

Use local energy density $\epsilon$ (including rest energy) and pressure $p$ in $\mathrm{J\,m^{-3}}$, baryon number density $n>0$ in $\mathrm{m^{-3}}$, and $w=\epsilon+p>0$. The lapse $\alpha>0$ is normalized to one at infinity. On the static fluid-rest slice, with enclosed gravitational mass $m(r)$ in kilograms, the proper volume of a spherical layer is
$$
 dV=\frac{4\pi r^2\,dr}{\sqrt{1-2Gm(r)/(rc^2)}} .
$$
Write $o,i$ for the outer and inner phases and $t$ for their interface. All interface values of material fields below are one-sided limits. There is no surface inventory in the two-fluid model.

The cold first law on a connected phase gives
$$
 d\ln n=\frac{d\epsilon}{w},\qquad
 \mu=\frac{d\epsilon}{dn}=\frac{w}{n},\qquad
 d\ln\mu=\frac{dp}{w}.
$$
Here $\mu$ is the local chemical potential, equal to enthalpy per baryon and measured in joules per baryon. Integrating the first equation along a phase determines $n$ up to one positive multiplier. Independently, static hydrostatic balance gives $dp=-w\,d\ln\alpha$. Consequently
$$
 C_a=\alpha\mu_a=\text{constant on phase }a,\qquad
 n_a(r)=\frac{\alpha(r)w_a(r)}{C_a},\qquad
 B_a=\int_a n_a\,dV=\frac{H_a}{C_a},\qquad
 H_a=\int_a\alpha w_a\,dV .
 \tag{1}
$$
The known $H_a$ is a redshifted enthalpy integral in joules. The baryon count $B_a$ itself uses proper volume with no lapse weight. The outer reading $n_o(r_*)=n_*>0$ fixes $C_o=\alpha(r_*)w_o(r_*)/n_*$. Applying the differential first law separately on the smooth branches avoids assuming a thermodynamic path through the density discontinuity. [Haensel and Potekhin, Eqs. 1–5](https://doi.org/10.1051/0004-6361:20041722)

**Exchange in chemical equilibrium.** The local Gibbs energy per baryon is equal on the two sides at their common pressure $p_t$. The lapse is continuous, so $\mu_{i,t}=\mu_{o,t}$ gives $C_i=C_o=C$ and
$$
 \frac{n_{i,t}}{n_{o,t}}=\frac{\epsilon_{i,t}+p_t}{\epsilon_{o,t}+p_t}>1,
 \qquad
 M_b=m_b(B_o+B_i)=\frac{m_b}{C}(H_o+H_i). \tag{2}
$$
The inequality follows from the inward increase in energy density. If the material anchor is withdrawn, the jump ratio survives, while $n_o,n_i$ can both be multiplied by any common positive factor. The known rest mass $m_b$ converts an identified baryon count to kilograms. Equating a zero-pressure surface chemical potential with $m_b c^2$ would require an independent surface binding convention. [Chamel et al., author manuscript v2, §3.1, Eqs. 1–2](https://arxiv.org/pdf/1205.0983v2)

**Frozen transfer.** A stationary contact permits different one-sided chemical potentials. Both baryon currents are tangent to the static interface, so their normal fluxes vanish regardless of the density jump. The jump ratio is $(w_{i,t}/w_{o,t})(C_o/C_i)$, and separate conservation leaves $C_o/C_i$ free. With the same outer reading the complete rest-mass family is
$$
 M_b=m_b\left(\frac{H_o}{C_o}+\frac{H_i}{C_i}\right),\qquad 0<C_i<\infty.
 \tag{3}
$$
Its range is $(m_bB_o,\infty)$ in this continuum model, since the inner phase has positive enthalpy and nonzero volume. One inner number-density reading, an inner chemical potential at a known point, or a calibrated jump ratio fixes $C_i$. Without either density anchor there are two independent positive multipliers. In both interface models the total mass can then take any positive value. A measured total count would directly fix $M_b$ and give one constraint on the two frozen phase normalizations.

## One equilibrium, two material completions

Fix an energy density $E>0$, transition pressure $p_t=E/100$ and central pressure $p_c=2p_t$. Take
$$
 \epsilon_o(p)=E+2p\quad(0\le p\le p_t),\qquad
 \epsilon_i(p)=2E+3p\quad(p_t\le p\le p_c).
$$
The inward jump is $E+p_t>0$. Both branches have positive enthalpy, $w_o=E+3p$ and $w_i=2E+4p$.

These branches admit a common hydrostatic geometry. For this existence check use $G=c=1$ and write $u(r)$ for enclosed mass in length units. Take the regular TOV solution at $p_c$ on the smooth inner branch, with $u(r)=4\pi\epsilon_i(p_c)r^3/3+O(r^5)$ and $p=p_c+O(r^2)$. Continue outward on the outer branch when $p=p_t$. Up to the first zero of $p$, $E\le\epsilon\le\epsilon_{\max}=2E+3p_c$. As long as $2u/r<1$, the mass equation and TOV give
$$
 -p'=\frac{(\epsilon+p)(u+4\pi r^3p)}{r^2(1-2u/r)}
 \ \ge\ \frac{4\pi}{3}E^2 r .
$$
Hence $p$ reaches zero at a radius $R\le r_b$, where $r_b^2=3p_c/(2\pi E^2)$, provided continuation is regular. On that interval $2u/r\le (8\pi/3)\epsilon_{\max} r_b^2=4\epsilon_{\max}p_c/E^2<1$, which ensures continuation. Both connected phases have positive extent. The mass and pressure match at $p_t$, and $d\ln\alpha/dr=(u+4\pi r^3p)/[r^2(1-2u/r)]$ has a common limit there. Integrating with the Schwarzschild surface normalization gives a positive continuous lapse. The induced metric and extrinsic curvature match at the contact and at the zero-pressure surface. A density jump in the bulk requires no material shell.

Keep all these profiles fixed. At $p_*=p_t/2$ on the outer branch, choose the one measured density to be $n_*=E/(4m_b c^2)$ in physical units. Keep this reading in both completions. Let $n_{o,t}$ be its interface value from the following formula, and let $n^{\rm eq}_{i,t}=n_{o,t}w_i(p_t)/w_o(p_t)$. The two material completions are given, including their normalization, by
$$
 n_o(p)=n_*\left[\frac{w_o(p)}{w_o(p_*)}\right]^{2/3},\qquad
 n_i^{(\lambda)}(p)=\lambda n^{\rm eq}_{i,t}
       \left[\frac{w_i(p)}{w_i(p_t)}\right]^{3/4},
 \qquad \lambda=1\ \text{or}\ 2 .
$$
Both satisfy $d\ln n=d\epsilon/w$ identically. Each monotone branch can be inverted to give $\epsilon(n)$ with $p=n\,d\epsilon/dn-\epsilon$. For $\lambda=1$ the interface chemical potentials agree. Even if the two expressions are extended locally through $p_t$, $d\ln(\mu_i/\mu_o)/dp=1/w_i-1/w_o<0$, so the inner phase has lower chemical potential on the high-pressure side and the outer phase on the low-pressure side. For $\lambda=2$, the inner chemical potential is halved at each pressure. The jump persists in a constrained static state when conversion is frozen. Its inner count doubles and its total rest mass exceeds the first by $m_b B_i^{(1)}>0$. Every gravitational and stress profile and the outer calibration are identical. The charge unit and $m_b$ are fixed in both completions. What changes is the unmeasured energy per inner baryon.

## Where the pressure enters the energy ledger

Returning to SI units, the integrated local matter energy is $E_{\rm proper}=\int\epsilon\,dV$. The exterior mass $M$ of this isolated static star is also its infinity-normalized Komar mass. Summing the three equal principal pressures gives
$$
 Mc^2=\int\alpha(\epsilon+3p)\,dV
     = C_o B_o+C_i B_i+2\int\alpha p\,dV . \tag{4}
$$
The last identity uses $\epsilon+p=\mu n$. Each $C_aB_a=H_a$ stays fixed even if the inferred $B_a$ changes. The pressure correction enters (4) with a **plus** sign. In chemical equilibrium one may therefore recover $B_o+B_i=[Mc^2-2\int\alpha p\,dV]/C$ with the one calibrated $C$. For frozen transfer the same subtraction gives only the weighted sum $C_o B_o+C_i B_i$. [Reviewed static mass integral](static_radial_length_and_proper_matter_energy.md)

With the convention that a positive mass defect means $M_b>M$, its energy is
$$
 (M_b-M)c^2=\sum_{a=o,i}(m_b c^2-C_a)B_a-2\int\alpha p\,dV .
$$
The local energy above the chosen baryonic rest reference is $E_{\rm proper}-M_b c^2=\int(\epsilon-m_b c^2 n)\,dV$. No sign of the whole mass defect is assumed. The proper energy, exterior mass and pressure integral are determined by the supplied continuum fields. Turning them into a baryonic rest mass additionally requires the material registrations above. These ideal profiles, the cold first law, interface kinetics and calibrated baryon identity are inputs. The construction makes no inference about stability, stellar observations or a native DET mass standard.
