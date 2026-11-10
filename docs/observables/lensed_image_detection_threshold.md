# Receiver sensitivity for the two-image mass measurement

**Receiver decision.** Let $+p,-m$ be the registered exterior images, $p>m>\rho>0$, and let $\rho$ be the known angular radius of the uniform disk. A receiver returns every resolved image at or above a relative flux threshold $\varepsilon>0$, using $+p$ as its reference. The largest threshold at which a two-image record still enforces the ideal E55 point-fraction bound is
$$
\boxed{\displaystyle \varepsilon_{\max}=
\min\left\{\left(\frac m p\right)^2,\,
\frac{1-(m/p)^2}{(pm/\rho^2-1)^2}\right\}.}
$$
Equality is sufficient. The first term ensures that the receiver can return the fainter exterior image. The second ensures that it can detect at least one central image whenever a pair exists.

## Record and exterior mass

Use the accepted circular, transparent, single-plane lens and a common nonaligned point flash. The record contains both signed exterior angles, their finite positive delay $\Delta t=t(-m)-t(p)$, and no further returned image or critical-image tag. Rays are associated and individually resolved, including arbitrarily close pairs. The detector uses the same linear response at every image. There are no measured flux values in this record.

With $\lambda=1-\kappa\in(0,1]$, $A=\lambda pm$ and $\beta=\lambda(p-m)$, the exterior derivative is $d\beta/d\theta=\lambda(1+pm/\theta^2)$. The supplied circular magnification law gives
$$
|\mu(+p)|=\frac{p^2}{\beta\lambda(p+m)},\qquad
|\mu(-m)|=\frac{m^2}{\beta\lambda(p+m)}.
$$
The relative exterior fluxes are 1 and $e=(m/p)^2<1$. Thus $\varepsilon>e$ makes the observed record impossible even for a pure point lens; $\varepsilon=e$ returns both rays.

For $s=p/m$ and $B(s)=(s-s^{-1})/2+\log s$, the two positions and signed delay fix $TA=\Delta t/B(s)$. Under the supplied time-to-mass conversion, the redshifted total compact mass is $M_z=(1+z_L)M=c^3\Delta t/[4G B(s)]$. This includes the central point and disk and excludes the sheet. For every permitted fraction below, any $0<\lambda\le1$ and $T=\Delta t/[\lambda pm B(s)]$ realize the same exterior record. The detector adds a constraint on $f$, the fraction of $M$ in the central point.

## Which central images the receiver returns

Write $h=pm/\rho^2,\ C=h-1,\ b=(p-m)/\rho$. Then $C>b>0$ because $\rho<m$. A negative interior ray at $-\rho x$, $0<x<1$, obeys
$$
b=N_f(x)=(C-hf)x+hf/x .
$$
On this interval $N_f=Cx+hf(1/x-x)>0$, so the positive side, with signed map $-N_f$, contributes no ray for this source. At the disk edge $N_f(1)=C>b$, the centre is singular for $f>0$, and circular symmetry confines all images to the source axis. The accepted census defines
$$
f_*=\frac{C-\sqrt{C^2-b^2}}{2h}.
$$
There are no interior rays for $f_*<f\le1$. At $f=f_*$ the one distinct interior ray has zero Jacobian and always produces the stipulated critical-image tag. This endpoint is excluded by the record at every threshold.

For $0<f<f_*$ put $d=hf,\ a=C-d$ and $D=\sqrt{b^2-4ad}$. Here $0<d<C/2,\ a>0,\ 0<D<b$. The two interior images are at $-\rho x_\pm$, with $x_\pm=(b\pm D)/(2a)$. These are the two roots of $ax^2-bx+d=0$ inside the disk. At each root $xN_f'(x)=2ax-b=\pm D$. Since the absolute signed-map derivative there is $\lambda|N_f'(x)|$, the two relative fluxes are
$$
R_\pm(f)=\frac{|\mu(-\rho x_\pm)|}{|\mu(+p)|}
       =K\frac{x_\pm^2}{D},\qquad K=\frac{\rho(p+m)}{p^2}.
$$
Each image has its own deterministic return tag $R_\pm\ge\varepsilon$, independent of whether the other passes. The larger-radius interior image is always brighter. Thus both are missed exactly when $R_+(f)<\varepsilon$.

The brighter flux is strictly increasing throughout the two-ray branch. In fact
$$
R_+(f)=\frac{K}{4a^2}\left(D+2b+\frac{b^2}{D}\right).
$$
As $d$ increases, $a=C-d$ decreases and $D$ decreases since $d(C-d)$ increases for $d<C/2$. On $0<D<b$ the derivative of the bracket with respect to $D$ is $1-b^2/D^2<0$. Both positive factors therefore increase. The endpoint limits are
$$
R_0=\lim_{f\downarrow0}R_+(f)=K\frac{b}{C^2}
=\frac{1-e}{C^2}>0,\qquad
\lim_{f\uparrow f_*}R_+(f)=+\infty .
$$
The first is an infimum because $f=0$ is outside the model. The second is a limit of distinct noncritical images. The observed tag at the tangent follows directly from the separate critical-image rule.

## Sharp inverse for exactly two returned images

Assume valid angles, the stated positive delay, and the fixed calibrated threshold.

| Receiver threshold | Feasible central point fractions $f$ |
| --- | --- |
| $\varepsilon>e$ | Empty |
| $0<\varepsilon\le\min(e,R_0)$ | $(f_*,1]$ |
| $R_0<\varepsilon\le e$ | $(0,f_\varepsilon)\ \cup\ (f_*,1]$ |

In the last row $f_\varepsilon$ is the unique root of $R_+(f_\varepsilon)=\varepsilon$ in $(0,f_*)$, by continuity, strict increase and the endpoint limits. At $f_\varepsilon$ the brighter ray is returned, so that endpoint is excluded. At $\varepsilon=R_0$ the brighter ray of every allowed pair exceeds the threshold. Equality at the exterior threshold remains detectable. If $R_0\ge e$, every threshold capable of the observed exterior pair preserves the ideal bound.

These sets are sufficient as well as necessary. For every listed fraction keep the same exterior solution and split its compact strength between the point and disk with that fraction. The derived tags then return exactly the observed positions and delay. In particular, arbitrarily small positive point masses can reproduce the record precisely when $R_0<\varepsilon\le e$. Even then an interval immediately below $f_*$ is excluded because its brighter central ray is detectable. Multiply the feasible set of fractions by $M_z$ to obtain redshifted central point masses, or by $M$ if the lens redshift is known.

## Two receivers on the same lens geometry

For $p=5\rho/3,\ m=5\rho/4$, the values are $e=9/16,\ C=13/12,\ b=5/12,\ f_*=1/50$ and $R_0=63/169$. A receiver reaching $\varepsilon=1/3$ preserves $f>1/50$ whenever it returns only the exterior pair. A receiver reaching $\varepsilon=1/2$ still returns both exterior images but admits the disconnected low-fraction interval in the table.

For a specific lens take $f=1/100$. Its two extra rays have $x_+=1/3,\ x_-=1/17$ and $D=7/24$. Their relative fluxes are $2/5$ and $18/1445$, respectively. The $1/3$ receiver returns the exterior pair and the brighter central ray. The $1/2$ receiver returns only the exterior pair. With that receiver a pure point lens of the same total compact mass, at the same sheet and time coefficient, gives precisely the same tags, signed exterior angles and delay.

The common flash intensity, overall photometric gain and the factor $\lambda^{-2}$ cancel in the flux ratios. A common angular-unit conversion cancels from $e,C$ and the sensitivity boundary. Registered signed angles, a known centre and a disk radius on the same angular scale remain inputs. The dimensional mass uses a calibrated clock and an independently associated common emission. The sensitivity calculation uses angular ratios and a calibrated relative flux threshold. Applying the bound to data would require evidence of completeness at that threshold across the full central search region and arrival window, adequate resolution, common photometric response, and the stated transparent point-source geometry. The critical tag here is an ideal geometric-optics convention. Finite-source brightness at a caustic would require its own observation law.

The reference lens inverse supplies the two exterior positions, signed delay and ideal count. [Two lensed images and central mass](two_lensed_images_and_central_mass.md)

## Scientific provenance

- QR author SHA-256 68d514b567657b978157f741e1a28d0c443a4f8ffe1c00b608fc40daf445fc26.
- Independent Energy review SHA-256 b57f967c19f3104046050b14eeb3a08eb20604f66db8562da3334da399757a91.
