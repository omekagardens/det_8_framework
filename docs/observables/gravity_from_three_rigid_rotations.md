# Local gravity from three rigid rotations

Prepare three steady rigid rotations in the same annulus. Match each signed tracer rate to the outer-minus-inner surface level in that preparation. Three distinct rates are necessary and sufficient to recover the local downward acceleration $g$, camera angular velocity $W$ and differential gauge offset $b$ from compatible exact data. With equally spaced rates, gravity alone needs just the spacing and the second difference of the three levels. The precision threshold below determines whether the readings put a finite upper bound on $g$.

## From each preparation to one matched reading

Take $z$ upward, with a nonaccelerating origin, a known vertical, uniform $g>0$, and the same oriented azimuth in all runs. Import CL085's steady inviscid Euler balance, a free surface at constant pressure, and universal coupling to the downward body acceleration. In run $i$ the supplied rigid velocity is $v_\phi=A_i r$, with no radial or vertical flow. Thus $p_r=\rho A_i^2r$ and $p_z=-\rho g$. Differentiating $p(r,h_i(r))=p_{\rm atm}$ gives $g h_i'(r)=A_i^2r$, so the true level difference is
$$
H_i=h_i(2R)-h_i(R)=\frac{3R^2 A_i^2}{2g}.
$$
The outward surface rise is nonnegative for either sign of spin. An arbitrary common height zero in a run cancels in $H_i$. A differential zero error between the two gauges survives and is assumed stable across runs.

Let $u_i=\Delta\phi_i/T_i=A_i-W$ be the signed, unwrapped material advance relative to the same steadily rotating camera over a calibrated duration $T_i>0$. Let $s_i$ denote the **reported** outer-minus-inner level difference multiplied by $2/(3R^2)$. Put $x=1/g>0$. The whole record model is
$$
s_i=x(u_i+W)^2+b+e_i,\qquad |e_i|\le\eta.
$$
Here $b$ is the common offset in normalized units. An individual $s_i$ may be negative. The error bounds apply separately to each run, with every combination in the error box allowed. They require no error distribution.

## Why three distinct rates are minimal

For exact heights set $e_i=0$ and expand the response as $s(u)=xu^2+mu+c$, where $m=2xW$ and $c=xW^2+b$. For $u_1<u_2<u_3$, let $k_{ij}=(s_j-s_i)/(u_j-u_i)$. Then
$$
x=\frac{k_{23}-k_{12}}{u_3-u_1},\qquad
m=k_{12}-x(u_1+u_2),\qquad c=s_1-xu_1^2-mu_1 .
$$
The record admits finite positive gravity exactly when $x>0$. In that case it gives $g=1/x,\ W=m/(2x),\ b=c-xW^2$ and $A_i=u_i+W$. The constant and linear coefficients can be arbitrary real numbers for every $x>0$.

With only two distinct exact tags, take **any** $x>0$, and set
$$
W_x=\frac12\left(\frac{k_{12}}{x}-u_1-u_2\right),\qquad
b_x=s_1-x(u_1+W_x)^2,\qquad A_i=u_i+W_x .
$$
The first level holds by construction. The level change is $x(u_2-u_1)(u_1+u_2+2W_x)=s_2-s_1$, so the second level also holds. Choosing $x$ and $2x$ gives two exact physical parameter sets with different gravity for the very same record. With one tag, any $x>0$ and any $W$ work by choosing $b=s_1-x(u_1+W)^2$. Repeated exact tags at the same rate add no equation. These families use one common camera and offset within each candidate explanation. The three-state construction also works when one inertial spin vanishes or two of the spins have equal magnitudes.

## Sharp finite-error interval

Take exactly matched rates $u_0-d,u_0,u_0+d$, $d>0$. Denote their reported levels by $s_-,s_0,s_+$. For
$$
D=s_--2s_0+s_+,\qquad
D=2d^2 x+(e_--2e_0+e_+),
$$
the linear and constant parts cancel. Thus the **complete feasible set** is
$$
\mathcal X=(0,\infty)\ \cap\ [L,U],\qquad
L=\frac{D-4\eta}{2d^2},\quad U=\frac{D+4\eta}{2d^2}.
$$

To prove attainability, choose any $x\in\mathcal X$ and put $\delta=D-2d^2x$. Choose errors $(e_-,e_0,e_+)=(\delta/4,-\delta/4,\delta/4)$. Each lies in its allowed interval. After subtracting these errors and $xu_i^2$ from the three reported levels, the residual has zero second difference, so one affine function $mu_i+c$ fits all three. The preceding inverse gives finite $W,b$ shared by the runs. The rigid states $A_i=u_i+W$ have the free surfaces just derived, up to per-run vertical origins. This constructs the entire measured triple for every feasible $x$, including every positive endpoint. At the untrimmed endpoints the errors have alternating extreme signs when $\eta>0$.

| Observed contrast | Feasible $1/g$ | Feasible $g$ |
|---|---|---|
| $D\le-4\eta$ | Empty | Incompatible with any finite positive gravity |
| $-4\eta<D\le4\eta$ | $(0,U]$ | $[1/U,\infty)$ |
| $D>4\eta$ | $[L,U]$ | $[1/U,1/L]$ |

Zero inverse gravity is excluded, even at $D=-4\eta$. At $D=4\eta>0$, arbitrarily large finite gravity remains feasible. At $\eta=0$, only $D>0$ passes and the two endpoints coincide. The estimator $D/(2d^2)$ has a sharp absolute error bound $2\eta/d^2$ in inverse-gravity units.

## Precision, preparation and units

For a *given* compatible record, $D>4\eta$ is necessary and sufficient for a finite upper bound on $g$. Before measurement, the ideal contrast is $2d^2/g$. Guaranteeing a finite upper bound for **every** allowed error triple at that true gravity requires $2d^2/g>8\eta$, since the observed contrast can fall $4\eta$ below the ideal. Equality allows a record at the unbounded threshold. If the error bound on each reported raw height **difference** after its fixed bias is $\epsilon_H$, use $\eta=2\epsilon_H/(3R^2)$. In raw length units the observed second difference must then exceed $4\epsilon_H$. If each individual gauge reading has error at most $\epsilon_h$, a worst-case difference budget is $\epsilon_H=2\epsilon_h$.

The protocol costs three independently prepared and settled rigid states at distinct measured rates. The equal-spacing interval requires the measured rates to have the stated spacing. Each state supplies two surface heights, or one differential gauge reading, and one signed material advance over a timed exposure. The matching between rate and level must be retained. Reconstructing $W,b$ uses the individual tags. Common camera spin, stable differential gauge bias, common $g$, rigidity, registration of the two radii and angular sense, adequate fluid depth, and absence of translational acceleration are preparation or metrology premises. A single tracer yields a rigid state's relative rate once rigidity has been supplied or independently checked. Producing and resetting the spins, maintaining their steadiness and reading the instruments may require work and time. The model supplies neither a drive mechanism nor an energy or settling-time budget.

$R,H_i$ have units of length, $s_i,b,\eta,D$ of inverse length, $u_i,W,d$ of inverse time, and $x$ of time squared per length. For a common exposure $T$, the measured angle spacing is $dT$ radians. The exact dimensionless result is $gT^2/R=2(dT)^2/(RD)$. Its conversion to acceleration uses the separately calibrated factor $R/T^2$. Rate, radius and clock errors lie outside the height-only interval, as do run-specific gauge offsets or camera drift.

CL085's one rigid surface supplies $A^2/g$ from its ideally referenced shape and $A-W$ from its tracer, which admit every $g>0$. Repeating that shape at further radii leaves the same combinations. Changing the prepared rate while preserving the frame and height offset supplies a measurable curvature *across preparations*. This is an analytic calibration of local effective acceleration under the stated gravity and fluid premises. The optical-ring comparison supplies context for the common frame rate. Its optical and metric laws do not enter this inverse. Physical attribution and dimensional calibration come from the supplied premises; the derivation establishes no source mass, native DET scale or empirical result.

[Single-state annular gravity comparison](gravity_from_an_annular_free_surface.md)
