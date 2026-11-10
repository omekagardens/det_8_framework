# Comparing orbital and lensing masses for one source

**Decision.** The exterior lens images and their signed delay give one redshifted lens mass. A tagged, reverberating circular ring gives a closed interval of redshifted dynamical masses. The common, unknown redshift cancels in their ratio. In the worked record the orbital mass can range from one half to four times the lens mass, with equality and both endpoints attained.

## Registered observables and their domain

The lens arm tags a background flash, its two exterior signed angles $+p,-m$ about the known centre in radians, and its arrival difference $\Delta t=t(-m)-t(p)$. For finite $p>m>0$ and finite $\Delta t>0$, the accepted calibration gives
$$
B(s)=(s-s^{-1})/2+\log s,\qquad L_z=(1+z)M_{\rm lens}
     =\frac{c^3\Delta t}{4G B(p/m)}>0 .
$$
This is the mass of the compact component, excluding any external sheet. To realize the exterior tags one may choose any sheet factor $0<\lambda\le1$, angular strength $A=\lambda pm$, source offset $\beta=\lambda(p-m)$ and positive lens time coefficient $T_{\rm lens}=\Delta t/[A B(p/m)]$. A compact point profile suffices.

The ring arm tags a different flash at that compact source. Near and far echo times are measured relative to the same observed central pulse. An independently tracked tracer gives the full observed orbital period $P$; spectral calibration gives the rest-frame line-of-sight velocity amplitude $K$. Assume a pressureless, negligible-mass ring outside the source in a circular Newtonian orbit, no competing radial acceleration, and the supplied speed cap $0<v\le v_{\max}\ll c$. By hypothesis the lens sheet contributes neither to the orbit nor to the echo geometry. Delayed emission as a probe of geometry is the motivation; the two tagged rays and shared local-response delay used here are explicit assumptions. [Blandford & McKee (1982)](https://adsabs.harvard.edu/pdf/1982ApJ...255..419B)

Put $Z=1+z>0$, $s_i=\sin i$, and use the time quantities
$$
q=P/(2\pi),\qquad H=(t_{\rm far}+t_{\rm near})/2,\qquad
d=(t_{\rm far}-t_{\rm near})/2 .
$$
The period equation gives $Zr=qv$, and the velocity amplitude gives $v s_i=K$. With one shared observer-frame response lag $\ell\ge0$, the two echo equations reduce to
$$
H=\ell+qv/c,\qquad d=qv s_i/c=qK/c .
$$
The half-difference tests the independently measured period and amplitude. Once those are given it contributes no second equation for the inclination. The mean combines geometrical light-travel time with the response lag.

Require finite labelled readings, calibrated $G,c>0$, the lens domain above, $P>0,\ 0<K\le v_{\max}$, and
$$
d=qK/c,\qquad H\ge d .
$$
These conditions make $t_{\rm far}>t_{\rm near}\ge0$. Zero near delay is allowed at $H=d$. Failed consistency gives an empty model class before either mass is compared.

## Sharp inverse and equality decision

The allowed speeds are exactly
$$
K\le v\le V,\qquad V=\min(v_{\max},cH/q).
$$
The lower bound comes from $s_i\le1$; the second upper bound comes from $\ell\ge0$. Both endpoints are included. For each such $v$ and any common $Z>0$, set
$$
s_i=K/v,\qquad \ell=H-qv/c,\qquad r=qv/Z,\qquad
M_{\rm dyn}=\frac{qv^3}{GZ},\qquad M_{\rm lens}=\frac{L_z}{Z}.
$$
These choices give the observed period, Doppler amplitude, near and far times $H\mp d$, and $v^2=GM_{\rm dyn}/r$. Using the exterior lens solution gives the two signed angles and the recorded lens delay in the same world. No ring distance or angular radius is used. Conversely every realization satisfies these equations. The inclination and response lag vary together with $v$; their projected intervals cannot be chosen independently.

Let $D_-=qK^3/G$, $D_+=qV^3/G$. The strictly increasing map from $v$ gives
$$
 Z M_{\rm dyn}\in[D_-,D_+],\qquad
 \frac{M_{\rm dyn}}{M_{\rm lens}}\in[D_-/L_z,D_+/L_z].
$$
For a feasible record, the decision is exact.

| Position of the lens mass | Verdict on physical mass equality |
| --- | --- |
| $L_z<D_-$ or $L_z>D_+$ | Excluded. All permitted orbital masses lie on the same side of the lens mass. |
| $D_-=D_+=L_z$ | Forced. |
| $D_-<D_+$ and $D_-\le L_z\le D_+$ | Possible. At $v=(G L_z/q)^{1/3}$ the masses agree; all other allowed speeds give inequality. |

A singleton occurs exactly when $K=v_{\max}$ or $H=d$ on the feasible domain. The latter forces $v=K,\ s_i=1,\ \ell=0$. Contact with one endpoint of a nondegenerate interval permits equality at that endpoint. An independently calibrated inclination sine fixes $v=K/s_i$; an independently measured observer-frame lag fixes $v=c(H-\ell)/q$. In either case the inferred speed must belong to $[K,V]$, and it then fixes the redshifted dynamical mass and the equality verdict. A source-frame lag would also require conversion to the observer's time convention.

The lens delay, echo times and orbital period use common calibrated observer units. The source-frame orbital period is $P/Z$, while $qv/c=Zr/c$ is an observed geometrical light-travel time. The ratio for a specified speed is $4 B(p/m)(q/\Delta t)(v/c)^3$, dimensionless. The individual redshifted masses use the dimensional clock, $G$ and the rest-frame speed calibration; a known $Z$ gives the corresponding unredshifted masses. Redshift alone leaves the speed ambiguity intact. All these gravitational, source-registration and readout laws are supplied physical correspondences.

## One complete record admits equal and unequal masses

Choose a time unit $T_0>0$ and a small positive angle $\alpha$ in radians. Put $K_0=c/200$, $D_0=T_0 K_0^3/G$, with $v_{\max}=c/50$. Specify the labelled point readings as follows.

| Arm and tag | Reading |
| --- | --- |
| Background flash, positive and negative images | $+2\alpha,-\alpha$ |
| Background flash, negative arrival minus positive arrival | $\Delta t=8T_0(K_0/c)^3B(2)>0$ |
| Ring periodic tracer, full observer period | $P=2\pi T_0$ |
| Ring spectrum, rest-frame velocity amplitude | $K=K_0$ |
| Central-pulse near response | $t_{\rm near}=T_0/200$ |
| Same central pulse, far response | $t_{\rm far}=3T_0/200$ |

The lens tags give $L_z=2D_0$. The ring tags give $q=T_0,\ d=T_0/200=qK_0/c,\ H=T_0/100>d$. Thus $V=c/100=2K_0<v_{\max}$. The sharp redshifted orbital range is $[D_0,8D_0]$, or a mass ratio in $[1/2,4]$.

Hold $Z=2$, the source registration and all lens parameters fixed in both worlds, using $\lambda=1$. The following ring assignments differ only in unmeasured parameters.

| Quantity | Equal masses | Unequal masses |
| --- | --- | --- |
| Orbital speed $v$ | $2^{1/3}K_0$ | $K_0$ |
| Inclination sine | $2^{-1/3}$ | $1$ |
| Observer response lag $\ell$ | $(2-2^{1/3})T_0/200$ | $T_0/200$ |
| Ring radius $r$ | $T_0 2^{1/3}K_0/2$ | $T_0 K_0/2$ |
| $M_{\rm dyn}/M_{\rm lens}$ | $1$ | $1/2$ |

Both have $Zr/v=T_0,\ v\sin i=K_0$, the same mean echo time $H$, and the same echo half-difference $d$. Both produce the entire tagged record. The upper ratio 4 is also attained at $v=2K_0,\ \sin i=1/2,\ \ell=0$. Imposing instantaneous response on this record would select that upper endpoint without an independent lag measurement.

The lens calibration and same-carrier mass comparison use their own measurement records. [Two lensed images and central mass](two_lensed_images_and_central_mass.md) · [Registered active and inertial mass](registered_active_and_inertial_mass.md)

## Scientific provenance

DET Quantum Relativity derived the conditional E56 inverse. DET Relational State Research independently checked the feasibility conditions, closed endpoints, calibrations and matched examples. Frozen QR report SHA-256 0252cd169d241062f03e94ecbab42b954cdca74adf98c828dbd9e596dc40b872. Independent State review SHA-256 2d021ea5ec44991eee533c0ca824989aadc71cb07dc92cc0a4284e9b0ad5c6b0.
