# PSR J1738+0333 · Can five clock residuals resolve the propagation delay?

Keep the white-dwarf companion as a conditional target for a future independently registered timing experiment. The cited campaign establishes neither an eligible five-reading record nor a sufficiently small error on those readings. Decline an emitter-mass experiment on the same basis alone. Even exact inclined-orbit readings leave the pulsar mass undetermined when the phase-aligned instrumental or emission lag is free. The conclusions below concern the CL080 observation design for this one binary.

## Inputs and their dependencies

| Source | Role in this design |
| --- | --- |
| Antoniadis et al., Paper I, §§4.2, 4.7 and Table 2 | The adopted white-dwarf mass $M_c=0.181^{+0.007}_{-0.005} M_\odot$ uses spectroscopy and a finite-temperature mass–radius relation. The reported $i=32.6^\circ\pm1.0^\circ$ also uses the timing mass function and mass ratio $8.1\pm0.2$. The optical velocity analysis held the period and ascending-node epoch at radio timing values. The quoted mass and inclination intervals are 68% marginal intervals. Their estimates supply a design point. [Paper I, v3](https://arxiv.org/pdf/1204.3948v3) |
| Freire et al., Paper II, §2.4 and Table 1, note (b) | The adopted range $r=0.8915\,\mu\mathrm{s}$ and shape $s=0.53877$ were fixed from the combined optical/radio analysis. They agree with $r=(4.925490947\,\mu\mathrm{s}) M_c/M_\odot$ and $s=\sin i$ at the reported precision. Use the tabulated central values. [Paper II, v1](https://arxiv.org/pdf/1205.1450v1) |
| Freire & Wex, equations (3)–(7) and (9), and CL080 | Supply the GR propagation law and Keplerian interpretation. CL080 supplies five signed residuals in seconds at phases $0,\pi/6,\pi/2,7\pi/6,3\pi/2$ over three quarters of an orbit, all tied to one independent ephemeris. The controlled nuisance consists of a constant and one stable sine term at that registered phase. [Timing convention](https://arxiv.org/pdf/1007.0933v1) · [Accepted CL080 comparison](./five_pulse_arrivals_and_binary_masses.md) |

The radio analysis uses the sole arXiv version of Paper II, dated 7 May 2012. The optical parameters use Paper I v3, dated 10 July 2012. [Radio paper](https://arxiv.org/abs/1205.1450v1) · [Optical paper](https://arxiv.org/abs/1204.3948v3)

## One contrast and its sharp error bound

Write $u=\sin\phi$, $y_u=B+ku-2r\ln(1-su)$ and $k=x+b$, where $x$ is the projected geometric light-travel time and $b$ is the stable lag. For $h=1/2,1$, form $E_h=(y_h+y_{-h})/2-y_0=-r\ln(1-s^2h^2)$. Their combination $J=E_1-4E_{1/2}$ cancels the leading $r s^2$ term. With $z=s^2$,
$$
J=r[-\ln(1-z)+4\ln(1-z/4)]=\tfrac38r z^2+O(rz^3).
$$
The numerical predictions use the full logarithms.

| Predicted statistic | Seconds, nominal | Nanoseconds, nominal | Range in ns over the marginal 68% input rectangle |
| --- | ---: | ---: | ---: |
| $E_{1/2}$ | $6.7162\times10^{-8}$ | 67.16 | 61.64–73.76 |
| $E_1$ | $3.0567\times10^{-7}$ | 305.67 | 278.25–338.57 |
| $J$ | $3.7025\times10^{-8}$ | 37.02 | 31.68–43.55 |

The range uses $M_c\in[0.176,0.188]M_\odot$, $i\in[31.6^\circ,33.6^\circ]$ as a sensitivity check. All three predictions increase with both inputs on this interval. For $J$, its derivative in $z$ is $r[(1-z)^{-1}-(1-z/4)^{-1}]>0$. The rectangular endpoints do not describe a joint confidence interval. Direct substitution of Paper I's central $M_c,i$ changes $J$ by less than 0.001 ns.

If each corrected signed reading has unknown error $|e_u|\le\delta$, then in the specified **time order** the coefficient vector of $J$ is $w=(3,-2,1/2,-2,1/2)$. The coefficient $+3$ retains the same central reading used in both even contrasts. Thus
$$
|\widehat J-J|\le\|w\|_1\delta=8\delta .
$$
The independent box permits $e=\delta(1,-1,1,-1,1)$, attaining $+8\delta$, and its negative attains $-8\delta$. No statistical independence or noise distribution is needed. A common offset cancels. Correlated nuisance errors require their own joint description before assigning a smaller uncertainty.

For an **observed** positive contrast, the interval excludes zero exactly when $\widehat J>8\delta$. At a reading equal to the nominal prediction this requires $\delta<4.63$ ns per reading (about 3.96 ns at the low rectangular corner). For **prospective guaranteed separation** in this scalar statistic, both the true nominal signal and the zero-contrast null may suffer adverse errors. Their possible observed intervals are disjoint only if $J-8\delta>8\delta$, or $\delta<2.31$ ns at the nominal point. Equality allows contact. These are two interpretations of the same attainable error bound. Resolving $J$ alone neither identifies two masses nor proves the origin of a delay.

## What the published record supplies

- **Time and phase.** Paper II §2.2 documents a common clock convention, observatory corrections to terrestrial time, barycentring with DE/LE421 and reporting in TCB. The pulse template, iterative folding and timing solution share data. Table 1's period $0.3547907398724(13)$ d and ascending-node epoch MJD $54600.20040012(5)$ are fitted; parentheses denote last-digit 1σ uncertainties. A future product needs the independently established pulse count, emission and orbital phase reference, phase uncertainties, and transfer of site, backend and template offsets to the five records. [Paper II, §2.2 and Table 1](https://arxiv.org/pdf/1205.1450v1)
- **Harmonics and circularity.** A free quadrature term $d\cos\phi$ changes $J$ by $3d$ at the prescribed phases, so even the companion test requires an independently registered phase or bounded leakage. Near-circularity alone is insufficient here. Equation (6)'s leading eccentric correction $x[\kappa\sin(2\phi)-\eta\cos(2\phi)]/2$ contributes $-\sqrt3\,x\kappa$ to $J$. Inserting Paper II's $x=0.343429130(17)$ light-seconds and $\kappa=e\cos\omega=(3.1\pm1.1)\times10^{-7}$ gives about **−184 ns** before correction. This calculation illustrates a possible bias in this contrast. Paper II's ELL1 eccentricity estimate assumes the adopted Shapiro signal. A future correction needs independently constrained parameters or a demonstrated joint bound on the residual leakage. [Equation (6)](https://arxiv.org/pdf/1007.0933v1) · [Paper II, §2.4 and Table 1](https://arxiv.org/pdf/1205.1450v1)
- **Noise, dispersion and subtraction.** Paper II reports a **1.56 µs weighted residual RMS**. Its dispersion model includes eight derivatives, and its analysis adds 0.5 µs in quadrature to the individual estimated timing uncertainties. A separate fit gives the orthometric amplitude $h_3=9\pm13$ ns versus a 22 ns prediction. That statistic differs from $J$. None of these numbers provides a five-reading maximum error or the covariance after a compatible subtraction. [Paper II, abstract and §§2.3–2.4](https://arxiv.org/pdf/1205.1450v1)
- **Coverage and release.** Figure 4 combines post-fit orbital-phase residuals, including averages over 0.01 orbital cycles. Figure 3's independent Westerbork readings use the full Table 1 prediction, which already includes the orbital amplitude and an assumed propagation term. The reviewed sources identify no versioned public product containing the five required signed residuals. They do not establish that such records are unavailable elsewhere. [Paper II, Figs. 3–4 and Table 1(b)](https://arxiv.org/pdf/1205.1450v1)

## Decisions for the two masses

**Companion (white dwarf).** A future experiment could test the predicted curvature against a constant and a phase-aligned first harmonic. To infer $r,s$ it must also resolve both even contrasts and their ratio, check that both corrected odd slopes agree, and propagate the joint timing and phase uncertainty through the inverse on the inclined branch. The GR conversion $M_c=c^3r/G$ then gives the companion mass. A custodian release from the timing team or observatory archive would need a stable version, five phase tags with actual epochs and exposure windows, pre-fit signed seconds relative to an independent emission prediction that preserves the orbital and Shapiro terms, and the clock, template, dispersion, eccentricity and other subtraction records. It must document correlations, including shared ephemeris and the central reading, and support the stated error model. No such release is identified by this screen.

**Emitter (pulsar).** The odd slopes give only $k=x+b$. Even if a future record qualifies for the companion measurement, determining the emitter mass requires an independent calibration of $b$ or of geometric $x$, a registered $n,G,c$, and common orbital and gravitational masses. The published $x$ and mixed optical/radio mass ratio already use timing. Reusing them as independent lag evidence would assume the needed separation. With free lag the CL080 compatible emitter masses satisfy $0<M_e\le\epsilon^3c^3/(Gn)-M_c$ when feasible. That ceiling comes from the model speed restriction $\epsilon=0.01$, not from this target's five readings. The current decision is **defer the companion test pending qualified records; decline a two-mass inference without independent lag or geometric calibration**.
