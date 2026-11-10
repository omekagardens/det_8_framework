# What two Ricci scalar readings determine about particle rest mass

Let $\mathcal R_1,\mathcal R_b$ be the measured Ricci scalars at scale factors $1$ and $b>1$. The exact compatibility conditions for a nonempty conserved collisionless massive gas on a homogeneous isotropic expanding background and a constant nonnegative vacuum are
$$
 \mathcal R_1>0,\qquad b^{-3}\mathcal R_1\le\mathcal R_b<\mathcal R_1.
$$
Every compatible pair gives a strictly positive, attained minimum for the constituent rest-energy density in the first epoch's proper volume,
$$
 \boxed{\displaystyle U_{\min}
   =\frac{c^4}{8\pi G}\,\frac{\mathcal R_1-\mathcal R_b}{1-b^{-3}} .}
$$
At $\mathcal R_b=b^{-3}\mathcal R_1$ this is the unique value. For every pair with strict inequalities, every finite $U\ge U_{\min}$ is possible. A large inventory can be carried by fast massive particles whose energy density and pressure largely cancel in the trace.

## Trace of the transported gas

Normalize $a=1$ at the first reading. In the homogeneous comoving frame, let $d\mu(s)$ be the nonnegative measure of constituent rest energy per unit first-epoch proper volume at initial momentum magnitude $s=|\mathbf p(1)|/(mc)$. Its total $U=\int d\mu$ is finite and positive. Isotropy specifies the angular distribution. It suffices to use one fixed particle mass $m>0$ throughout. Collisionless redshift gives $|\mathbf p(a)|/(mc)=s/a$, so $\gamma_a(s)=\sqrt{1+s^2/a^2}$. Conservation of particle number dilutes the proper number density by $a^{-3}$, and the rest-energy density at $a$ is $U/a^3$.

The mass-shell energy and isotropic pressure moments are
$$
 E_g(a)=a^{-3}\!\int\gamma_a\,d\mu,\qquad
 3p_g(a)=a^{-3}\!\int\frac{s^2/a^2}{\gamma_a}\,d\mu .
$$
The pressure moment follows from momentum times velocity, summed over the three axes. Subtracting it from the energy leaves $E_g-3p_g=\int k_a(s)\,d\mu(s)$, where
$$
 k_a(s)=\frac{a^{-3}}{\sqrt{1+s^2/a^2}} .
$$
These are the homogeneous massive collisionless moments with the comoving energy expressed using $s$. No assumption about a thermal spectrum or perturbations enters the subtraction. [Ma and Bertschinger, v1, Eq. (52)](https://arxiv.org/pdf/astro-ph/9506072v1) · [Accepted local rest-density and trace relation](constituent_rest_density_from_local_stress.md)

Use signature $(-+++)$ with the convention $G_{\mu\nu}=8\pi G T_{\mu\nu}/c^4$ and no separate geometric cosmological term. A constant vacuum energy density $u_\Lambda\ge0$ has pressure $-u_\Lambda$ and contributes $4u_\Lambda$ to the energy density minus three times the pressure. In density units the two observations are
$$
 X=\frac{c^4\mathcal R_1}{8\pi G}=V+\int k_1\,d\mu,\qquad
 Y=\frac{c^4\mathcal R_b}{8\pi G}=V+\int k_b\,d\mu,\qquad V=4u_\Lambda .
$$
The same measure and the same $V$ occur in both equations. The inputs are scalar readings alone. The earlier static orbit and tidal result supplies the sign and stress conventions; its measurements of separate pressure components are absent here. [Local curvature and stress convention](local_density_and_pressure_from_orbit_and_tides.md)

## Exact data domain and the minimum

The ratio of the second to first gas kernels is
$$
 r(s)=\frac{k_b(s)}{k_1(s)}
     =b^{-2}\sqrt{\frac{1+s^2}{b^2+s^2}}.
$$
For $b>1$ it rises strictly from $r_0=b^{-3}$ at $s=0$ toward $r_\infty=b^{-2}<1$ as $s\to\infty$. This follows, for example, by differentiating $(1+s^2)/(b^2+s^2)$ with respect to $s^2$. The kernel difference $D(s)=k_1(s)[1-r(s)]$ is strictly positive at each finite $s$. Both factors decrease away from zero momentum, so $D(s)$ decreases strictly from $D_0=1-b^{-3}$ to zero. Hence
$$
 \Delta=X-Y=\int D(s)\,d\mu(s)>0,\qquad
 Y-r_0X=(1-r_0)V+\int k_1(s)[r(s)-r_0]\,d\mu(s)\ge0 .
$$
Also $X>0$. A pair outside $r_0X\le Y<X$ with $X>0$ fails. In particular, even an arbitrarily hot nonempty massive gas causes a strictly positive decline; a constant trace from vacuum alone cannot fit the stipulated gas.

Since $D(s)\le D_0$, the rest inventory must obey $U\ge \Delta/D_0$. Equality holds exactly when the entire gas is cold. For sufficiency on the whole domain, put rest weight $U_{\min}=\Delta/D_0$ at $s=0$ and choose the constant vacuum trace
$$
 V_{\rm cold}=X-U_{\min}=\frac{Y-r_0 X}{1-r_0}\ge0 .
$$
This reproduces $X$ and $Y$ exactly. At the boundary $Y=r_0 X$ both nonnegative terms in $Y-r_0X$ must vanish. Thus the gas is cold, $V=0$, and $U=X$. In the strict interior a cold gas still attains the minimum, with $V_{\rm cold}>0$; other compatible gases can exceed it.

## Interior pairs have no finite upper bound

Fix any data with $r_0X<Y<X$. A construction with two momentum shells keeps even the vacuum fixed while the rest inventory grows. Choose a first-epoch **gas trace** $A$ satisfying
$$
 \frac{\Delta}{1-r_0}<A<
       \min\!\left(X,\frac{\Delta}{1-r_\infty}\right).
$$
This open interval is nonempty because $X>U_{\min}$ and $r_\infty>r_0$. Set $V=X-A>0$. The required gas trace ratio is then $r_*=1-\Delta/A$, strictly between $r_0$ and $r_\infty$.

Choose any finite momentum $S$ large enough that $r(S)>r_*$. Split the first-epoch gas trace between a cold shell and an isotropic shell at $S$ in the fractions $1-h$ and $h$, with
$$
 h=\frac{r_*-r_0}{r(S)-r_0}\in(0,1),\qquad
 d\mu_S=A(1-h)\,\delta_0+\frac{Ah}{k_1(S)}\,\delta_S .
$$
Here $\delta_s$ denotes a unit atom in momentum magnitude. The first trace of this measure is exactly $A$. Its second trace is $A[(1-h)r_0+h r(S)]=Ar_*=A-\Delta$. Adding the same $V$ returns the two prescribed readings for every $S$. Each realization carries its own conserved population from the first epoch to the second by the given redshift and dilution laws.

As $S\to\infty$, $h$ tends to the strictly positive value $(r_*-r_0)/(r_\infty-r_0)$ while $k_1(S)\to0$. Thus
$$
 U_S=A(1-h)+Ah/k_1(S)\longrightarrow\infty .
$$
Both shells use strictly massive particles. Each finite member has finite energy density and pressure at both epochs. The sequence has no uniform upper bound on those unmeasured stresses.

For any specified finite $U>U_{\min}$, take one such member with $U_S\ge U$. Mix its rest-energy measure with the cold minimum measure using weight $(U-U_{\min})/(U_S-U_{\min})$ for the former. Use the same weights for their two constant vacuum densities. The resulting single measure, transported at both epochs, has the chosen $U$, finite stress and at most the same two shells of one species. The corresponding vacuum is constant and nonnegative. Linearity gives the identical two observed scalars. This fills the entire interval $[U_{\min},\infty)$ under the unknown-vacuum premise. The cold boundary has only the singleton $\{X\}$.

## Mass, volume and physical registration

Dividing the inferred rest-energy density by $c^2$ gives constituent rest mass per unit proper volume at the first epoch. The second-epoch density is smaller by $b^3$. In a comoving cell of known first-epoch proper volume $V_1$, the conserved rest mass is $V_1U/c^2$. The expansion ratio alone supplies no absolute cell volume, particle count or individual constituent mass. The Ricci scalars require a calibrated inverse-length-squared scale. If available only as $L^2\mathcal R$ for a reference length $L$, the result fixes a density in units of $c^4/(8\pi G L^2)$; a physical $L$ and the conversions $c,G$ give energy per physical volume. The compatibility ratios do not depend on that absolute scale.

The interpretation requires a shared homogeneous isotropic expanding preparation, an independently registered ratio $b$, free redshifting of the same conserved particles, calibrated curvature at both epochs, and one constant vacuum with the specified pressure. The accepted single-epoch analysis permits rest density arbitrarily close to zero in the presence of unknown vacuum. Here the observed decline eliminates its constant contribution and gives the positive bound. The two readings supply no measurement of separate gas energy and pressure, expansion rate, elapsed time or preparation and readout work. This analytic result assumes the gravitational and transport laws; it supplies no native mass, length or energy unit and uses no empirical cosmological data.
