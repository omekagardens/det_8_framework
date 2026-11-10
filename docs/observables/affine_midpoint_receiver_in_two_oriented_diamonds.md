# Distinguishing two oriented diamonds with a receiver at null affine midpoints

The prescribed receiver has past proper-area fraction $(\sqrt5-1)/4$ in the positive-sign diamond and $(3-\sqrt5)/4$ in the negative-sign diamond. At one calibrated nonzero scalar mass its normalized response distinguishes the two. If the mass-area product is shared across receivers but only known to lie in the weak band below, one additional reading at the future corner suffices. All predictions concern the two stipulated continuum metrics and the supplied retarded field.

## Registering the event separately in each diamond

Use the donor’s representation $0\le u,v\le1$, $P=(0,0)$ the marked past corner, $F=(1,1)$ the future corner, and $u,v$ increasing to the future. With the boundary understood by smooth extension,
$$
 ds_s^2=-2L^2 f_s\,du\,dv,\qquad
 f_s=1+s(2u-1)(6v^2-6v+1),\qquad s=\pm\tfrac12 .
$$
The metric is regular on the boundary since $1/2\le f_s\le3/2$. Its proper-area measure divided by its total area $L^2$ is $d\mu_s=f_s\,du\,dv$. The time-reversing isometry $T(u,v)=(1-u,1-v)$ carries $s$ into $-s$. Reversing the labels of each integrated chain under $T$ preserves all its ordered volumes from $P$ to $F$, hence both opposite-corner responses agree at every mass in the donor’s model. Each candidate still uses its own past corner as source.

Mark the two future-directed null segments from $P$ to the spacelike corners. On $v=0$, an affine parameter $\lambda$ along the null geodesic satisfies
$$
 \frac{d^2u}{d\lambda^2}
 +(\partial_u\log f_s)\left(\frac{du}{d\lambda}\right)^2=0.
$$
Thus $d\lambda/du$ is a constant times $f_s(u,0)$. The same equation with $u,v$ interchanged holds on the other side. Put $A(t)=t^2-t$ and $B(t)=2t^3-3t^2+t$. Dividing each accumulated affine interval by its own full interval gives
$$
 \ell_u(t)=t+sA(t),\qquad \ell_v(t)=t-sB(t).
$$
Both are strictly increasing from 0 to 1. Since $B(1/2)=0$, $v_s=1/2$ is the unique affine midpoint on $u=0$. On $v=0$, solving $u_s+s(u_s^2-u_s)=1/2$ gives exactly one root on the segment in either case. Launch the other null family from each midpoint. The two future rays intersect once, at $E_s=(u_s,1/2)$.

| Sign $s$ | $u_s$ | Past area of $E_s$ divided by $L^2$ |
|---|---:|---:|
| $+1/2$ | $(\sqrt5-1)/2$ | $(\sqrt5-1)/4$ |
| $-1/2$ | $(3-\sqrt5)/2$ | $(3-\sqrt5)/4$ |

Indeed, the normalized past area of $(u,v)$ is $uv+sA(u)B(v)$. At $v=1/2$ only $u_s/2$ remains. Denote the two fractions by $a_+,a_-$. Their difference is $(\sqrt5-2)/2>1/10$.

The midpoint condition is the fraction $(\lambda-\lambda_P)/(\lambda_{\rm end}-\lambda_P)=1/2$, invariant under any affine change of parameter with nonzero slope. For increasing regular null coordinates $U=U(u),\,V=V(v)$, the transformed coefficient of the metric is $f_s/(U'V')$. Along $v=0$, its product with $dU$ is $f_s\,du/V'(0)$. That side-dependent constant cancels in the fraction. The same cancellation holds on $u=0$. Reversing coordinate labels also preserves the geometrically directed intervals when their endpoints and future directions are carried along. Exchanging the two families merely interchanges the two rays defining the crossing. These computations use coordinates within each candidate; comparison uses the marked source, side endpoints, affine fractions, and ray intersection. Equal affine fractions are a physical registration premise. Endpoint causal order gives no affine spacing, and elapsed proper time along a null segment is zero.

## A finite nonzero-mass measurement

Put $x=m^2L^2/2$, where $m$ is the inverse-length mass parameter in the supplied wave equation. Let $Q_s(x)=G_m(E_s,P)/G_0(E_s,P)$ and $C(x)=G_m(F,P)/G_0(F,P)$. The massless timelike kernel is $1/2$; its convolution with the metric volume generates the donor’s retarded series. Restricting every interior integration to the causal interval from $P$ to the chosen receiver gives
$$
 Q_s(x)=\sum_{n=0}^{\infty}(-x)^n I_{n,s},\qquad
 I_{0,s}=1,\quad I_{1,s}=a_s .
$$
Here $I_{n,s}$ integrates $d\mu_s^{\,\otimes n}$ over one ordered $n$-chain in the interval. For $n$ independent draws from its area measure conditioned on that interval, an increasing chain requires one specified order of their $u$ coordinates. The chance of that order is $1/n!$, by exchangeability and zero tie probability. Restoring the unconditioned area factors gives $0\le I_{n,s}\le a_s^n/n!$. For the full corner the same argument uses $a=1$. This accounts for every omitted order of the series.

Writing the response for either interval as $1-ax+e$, the factorial majorant gives
$$
 |e|\le\frac{(ax)^2}{2(1-ax/3)}
$$
when $0\le ax<3$: after order two the ratio of successive majorant terms is at most $ax/3$. Both receiver fractions are less than $1/3$. Uniformly for $0<x\le1/8$ this gives $|e_s|\le(4/71)x^2$, and for the corner $|e_F|\le(12/23)x^2$.

**One known setting.** Choose $x=1/8$, or $m^2L^2=1/4$. The midpoint of the two *linear* receiver predictions is $1-x/4=31/32$. Both fractions satisfy $|a_s-1/4|=(\sqrt5-2)/4>1/20$. The all-orders receiver value $Q_+$ lies below $31/32$, and $Q_-$ above it, each by more than
$$
 1/160-1/1136>1/200 .
$$
One normalized interior reading with absolute error at most $1/200$ therefore decides the sign for this exact mass setting. No detectable difference exists at zero mass.

## A shared mass setting known only within a band

Suppose the setting is reproducible between the corner and interior measurements, and independently known to satisfy $1/16\le x\le1/8$. The future-corner function is the same for both candidates. It supplies a reference for the actual setting. At that one mass form the measured statistic
$$
 D=(1-Q_s)-\tfrac14(1-C).
$$
Its linear term is $x(a_s-1/4)$. The remainder obeys
$$
 |D-x(a_s-1/4)|
 \le (4/71+3/23)x^2 < x^2/5.
$$
Consequently $D_+>x/40$ and $D_-<-x/40$ everywhere on the band. The minimum guaranteed margin exceeds $1/640$. If the final interior and corner ratios each have absolute error at most $1/1000$, the statistic changes by at most $1/800$; its sign still decides the orientation. This uses one massive setting and a massless reference at each receiver. The setting need not be estimated by inverting a response curve.

The distinction between a fixed known mass and this nuisance band matters even for exact data. Both $a_s$ lie strictly between $3/16$ and $5/16$. At $x=1/16$ either interior deficit $1-Q_s$ is at most $5/256+1/4544<1/50$, whereas at $x=1/8$ it is at least $3/128-1/1136>1/50$. Absolute convergence gives continuity. Hence **both** candidates can give the interior reading $49/50$ at some allowed setting if only that one reading is retained. The paired corner observation removes that ambiguity while enforcing a common $x$ within each proposed explanation.

## Physical scope

The prescribed rule requires a marked time orientation, registered boundary endpoints, physical access to affine midpoint fractions, and transfer of the two other null rays to a common crossing. The scalar comparison assumes the same covariantly normalized impulse and ideal minimally coupled retarded law, a signed linear response, and no reflected contribution. At each receiver, massless and massive readings must share the source normalization and the same nonzero multiplicative gain, with any offset removed. Local ratios permit different gains at the two receivers. The paired test requires a stable geometry, the same proper area and massive setting across measurements, and the stated prior band. The design tolerances apply to the normalized readings including reference error; source or placement errors must fit that budget or be bounded separately.

The calculation fixes an area fraction and separates two specified oriented continuum models. It supplies no absolute length, dimensional scalar mass, null or timelike clock, physical detector, or procedure deriving those objects from DET primitives. Both the geometry and the propagation law enter as inputs. No proper-area sampling of events or detector run was performed.

[Oriented diamonds and opposite-corner propagation](oriented_triples_and_corner_propagation.md) · [Finite-mass corner comparison](massive_corner_response_and_curvature.md)
