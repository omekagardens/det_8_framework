# A half-step observation tests equal free fall in a binary

**Include the observation at $h/2$.** With only $0,h,2h$, the eccentricity vector can make one full turn between successive readings. Every constant three-reading record then admits both equal and unequal passive-to-inertial mass ratios. The schedule $0,h/2,h,2h$ decides equality on every compatible record. It also fixes the signed difference except when a nonzero equilibrium leaves a range of allowed precession rates.

## Physical inputs and exact evolution

Register the two bodies in a fixed order and measure both signed components of the eccentricity vector $e$ in the same inertial orbital plane. Its positive real axis is the direction of the fixed projected external field. The supplied law and bounds are
$$
\dot e=i\omega e+i a\delta,\quad
\delta=P_1/I_1-P_2/I_2,\quad a>0,\quad |\delta|\le D,\qquad
\omega_-=\frac{\pi}{2h}\le\omega\le\omega_+=\frac{2\pi}{h}.
$$
Here $h,D>0$. The constant $\omega$ and launch vector are unknown before the experiment. The signed forcing, positive rotation convention and constant external field are fixed throughout the window. Binary eccentricity as a probe of differential acceleration has a physical precedent; the exact averaged law, frequency band and vector readouts used here are stipulated. [Damour & Schäfer (1991)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.66.2549)

The forced centre $C=-a\delta/\omega$ is **real**. Writing $z=e(0)$ gives
$$
e(t)=C+(z-C)e^{i\omega t}.
$$
The free eccentricity $z-C$ can have either component and can vanish. Require complete finite labelled vectors, $|z|\le E$, and the supplied weak-eccentricity domain $E+2haD\le e_{\rm small}\ll1$. Indeed $|e(t)|\le E+2aD/\omega\le E+4haD/\pi$ on the closed interval. Thus every parameter choice below stays in the model for the entire observation. Failure of an input check or an empty parameter set makes the record incompatible.

## Original schedule at $0,h,2h$

Denote the three vectors by $z_0,z_1,z_2$, and set $u=z_1-z_0,\ v=z_2-z_1$. A step of size $h$ rotates about $C$ by the factor $q=e^{i\omega h}$, so $v=qu$.

- **If $u\ne0$**, form $q=v/u$. Require $q=e^{i\theta}$ for $\theta\in[\pi/2,2\pi)$. This checks unit modulus and the allowed oriented arc and excludes $q=1$, which would have made $u=0$. There is exactly one such angle. Set
  $$
  \omega=\theta/h,\qquad C=(z_1-qz_0)/(1-q),\qquad \delta=-\omega C/a .
  $$
  Require $C\in\mathbb R$ and $|\delta|\le D$. If all checks pass, this pair is the full inverse. The centre equation reproduces $z_1$; $v=qu$ reproduces $z_2$. Equality of ratios is forced if $C=0$ and excluded otherwise. This includes $z_2=z_0$ for $q=-1$ and the lower frequency endpoint $q=i$.
- **If $u=0$ and $v\ne0$**, there is no solution.
- **If $u=v=0$**, let the common value be $z$. The full solution set is
  $$
  \{(\omega_+,\delta): -D\le\delta\le D\}
  \ \cup\
  \{(\omega,-\omega z/a):\omega_-\le\omega<\omega_+,\ z\in\mathbb R,\ \omega|z|\le aD\}.
  $$
  At $\omega_+$, $q=1$ returns every vector to its starting point. At each lower allowed frequency $q\ne1$, so a constant sample requires $z=C$, a true equilibrium. These exhaust the possibilities because $u=(q-1)(z-C)$. The full-turn branch alone makes equality ambiguous for every such record, even if its actual preparation was an equilibrium.

## Schedule with the additional labelled vector at $h/2$

Write $z_{1/2}=e(h/2)$ and $w=z_{1/2}-z_0$. The first three epochs $0,h/2,h$ are equally spaced. Their rotation factor $r=e^{i\omega h/2}$ lies on the closed arc with angle $\pi/4\le\psi\le\pi$. This arc excludes $1$, includes $-1$, and gives a unique angle for each factor.

- **If $w\ne0$**, form $r=(z_1-z_{1/2})/w$. Require $r=e^{i\psi}$ on that arc and set
  $$
  \omega=2\psi/h,\qquad C=(z_{1/2}-rz_0)/(1-r),\qquad \delta=-\omega C/a.
  $$
  Require $C\in\mathbb R,\ |\delta|\le D$, and the final tagged vector $z_2=C+(z_0-C)r^4$. These checks are necessary and sufficient. The recurrence reproduces the first three readings and the fourth-power condition reproduces the last one, including any repeated vector. The full inverse is this single pair. Equality is forced exactly at $C=0$, and excluded otherwise. In particular, if the original three readings coincide but $z_{1/2}\ne z_0$, then $r=-1,\ \omega=\omega_+$ and $C=(z_{1/2}+z_0)/2$.
- **If $w=0$**, then $(r-1)(z_0-C)=0$ forces $z_0=C$. Require all four vectors to coincide at one real value $z$. The full set is
  $$
  \{(\omega,-\omega z/a):\omega_-\le\omega\le\omega_+,\ \omega|z|\le aD\}.
  $$
  At $z=0$ every allowed frequency gives $\delta=0$. At $z\ne0$, feasibility requires $\omega_-|z|\le aD$. Every allowed $\delta$ then has sign opposite to $z$, with sharp magnitude interval
  $$
  |\delta|\in\left[\frac{\omega_-|z|}{a},\
                    \min\!\left(D,\frac{\omega_+|z|}{a}\right)\right].
  $$
  Both endpoints are attained. The magnitude varies exactly when $\omega_-|z|<aD$. Contact at $\omega_-|z|=aD$ fixes $\omega=\omega_-$ and $|\delta|=D$. In a nonzero equilibrium the measurement directly fixes the combination $\delta/\omega=-z/a$; an independent apsidal-rate measurement would fix $\delta$.

Thus the extra epoch removes the ambiguity in the equality decision, even at the full-turn frequency and even when the orbit reveals no precession because the free component vanishes.

## Same three readings, different half-step outcomes

Use the allowed frequency $\omega_+=2\pi/h$ and the same launch $z=iE/2$ in both worlds (also valid at $E=0$). Keep the fixed field, transfer, clock, body labels and reference axes identical. The entire deterministic records are

| Passive/inertial difference | $e(0)$ | $e(h/2)$ | $e(h)$ | $e(2h)$ |
| --- | --- | --- | --- | --- |
| $\delta=0$ | $z$ | $-z$ | $z$ | $z$ |
| $\delta=D/2$ | $z$ | $-z-aD/\omega_+$ | $z$ | $z$ |

The half-step is a half turn, giving $2C-z$ in each world. The difference is a nonzero real displacement along the registered field axis. The baseline records coincide at every labelled epoch; the augmented records separate them without lengthening the observation.

The numerical coefficient $\delta$ is dimensionless in the supplied normalization. Reporting it requires the dimensionless eccentricity scale, the sign and orientation of both components, body ordering, elapsed time $h$, and the differential-acceleration transfer $a$ in compatible inverse-time units. The recovered scale factor is $\omega/a$. A zero difference establishes equality between the two registered ratios; their common value remains undetermined. This is an exact result for the stated constant-field law and error-free observations. Applying it to a binary would require a justified secular model and recovery of these calibrated vector records from observations. The calculation supplies no DET mass calibration or empirical bound.

See [registered active and inertial mass](registered_active_and_inertial_mass.md) for the separate same-carrier measurement assumptions.

## Scientific provenance

- QR author SHA-256 d1e909c6d922cbbba2bc41dc186ec9a3333fcf39b68218d30282a145abdfdd90.
- Independent mass-registration review SHA-256 6c94b70aa72b694c0256ae87a3235213bfd3471a6693ecbd902e2985bc27b2d4.
