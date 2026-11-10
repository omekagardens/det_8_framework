# Registering centre curvature with a tip-to-tip clock

**Result.** Within the specified conformal diamond family, the population probability of pair comparability fixes the shape parameter. One calibrated proper-time reading on the maximizing worldline then fixes the length scale and the dimensional centre scalar curvature. An unknown-duration tick leaves a continuous scale ambiguity for every nonzero curvature.

## Which clock to read

Use the closed unit square in future-increasing null coordinates, with past tip $P=(0,0)$, future tip $F=(1,1)$, and supplied metric
$$
 ds^2=-2L^2[1+\theta(2u-1)(2v-1)]\,du\,dv,\qquad L>0,\quad |\theta|\le\tfrac12.
$$
Let $D$ denote the largest proper **length** of a future-directed causal curve from $P$ to $F$. An ideal clock measures elapsed proper time $\tau=D/c$ along a maximizing path, with $c$ expressed in the chosen length and time units.

Put $t=(u+v)/2,\ x=(u-v)/2$. For an absolutely continuous future causal curve, monotonicity of $u,v$ gives $|\Delta x|\le\Delta t$. Its image is therefore a Lipschitz graph $x(t)$ on $[0,1]$, up to pauses, with $x(0)=x(1)=0$ and $|x'|\le1$ almost everywhere. Conversely these conditions give an admissible curve. Writing $A(t)=1+\theta(2t-1)^2$, the proper length divided by $\sqrt2 L$ is
$$
 I[x]=\int_0^1\sqrt{(A-4\theta x^2)(1-x'^2)}\,dt.
$$

Symmetry identifies a candidate worldline, but when $\theta<0$ the conformal factor grows off the diagonal. To control the full trip, apply the arithmetic–geometric mean inequality to $(A-4\theta x^2)/\sqrt A$ and $\sqrt A(1-x'^2)$. Both are nonnegative, including on null portions. Since $A\ge 1/2$ and $|\theta|\le1/2$,
$$
 I[x]-I[0]\le\int_0^1\!\left(-\frac{2\theta}{\sqrt A}x^2-\frac{\sqrt A}{2}x'^2\right)dt
 \le\sqrt2\int_0^1x^2\,dt-\frac{1}{2\sqrt2}\int_0^1x'^2\,dt .
$$
The endpoints give $\int_0^1x'(s)\,ds=0$. Thus $x(t)=\int_0^1(\mathbf1_{[0,t]}(s)-t)x'(s)\,ds$, and Cauchy–Schwarz gives $x(t)^2\le t(1-t)\int_0^1x'^2\,ds$. Integrating over $t$ bounds $\int x^2$ by $\tfrac16\int x'^2$. Consequently
$$
 I[x]-I[0]\le-\frac{1}{6\sqrt2}\int_0^1 x'^2\,dt .
$$
Every nonconstant $x$ gives strictly less elapsed time. The unique maximizing image is $u=v$, including at $\theta=\pm 1/2$. Along it, symmetry of the integral about the midpoint gives
$$
 D=\sqrt2\,L\,J(\theta),\qquad J(\theta)=\int_0^1\sqrt{1+\theta z^2}\,dz>0.
$$

## What the joint record determines

The accepted proper-area population law gives $p=1/2+\theta/9$. This uses two independent proper-area samples or the registered pooled equivalent with an independent fair complementary mask per candidate. With the accepted curvature sign convention, the total proper area is $L^2$ and the centre scalar curvature is $R_c=8\theta/L^2$. For $4/9\le p\le5/9$ and the calibrated maximizing time $\tau>0$, the inverse is
$$
 \theta=9(p-\tfrac12),\qquad L=\frac{c\tau}{\sqrt2\,J(\theta)},\qquad
 R_c=\frac{16\theta J(\theta)^2}{(c\tau)^2}.
$$
Hence $R_c$ has reciprocal-length-squared units. For the flat member $J(0)=1$, $D=\sqrt2L$, and $p=1/2$ already fixes $R_c=0$.

This protocol requires a complete clock worldline with both endpoint coincidences and the maximizing path registered. The same clock is initialized or phase-tagged at $P$ and read at $F$, so two distant clocks need no mutual synchronization. Its uniform proper-time rate and the conversion through $c$ supply the length standard. A shorter, unregistered path supplies only $c\tau_{\rm path}\le D$. The formula uses the population $p$ and an exact elapsed reading. Finite pair statistics, endpoint timing errors and clock-rate errors would require their own uncertainty analysis.

## What survives with an uncalibrated tick

Let $\delta>0$ be the common, constant but unknown proper duration per tick. Let $N=\tau/\delta$ be an exact elapsed tick reading, with endpoint phases registered. An integer counter with unknown fractional endpoint phases would give a range instead. The observations determine
$$
 \frac{L}{c\delta}=\frac{N}{\sqrt2\,J(\theta)},\qquad
 R_c(c\delta)^2=\frac{16\theta J(\theta)^2}{N^2},\qquad
 R_cD^2=16\theta J(\theta)^2 .
$$
The exact rescaling $(L,\delta)\mapsto(\lambda L,\lambda\delta)$ leaves $p,N$ fixed for every $\lambda>0$ while $R_c\mapsto R_c/\lambda^2$. For instance $\theta=1/2$ gives $p=5/9$. Doubling both the length and tick duration preserves the count and changes $4/L^2$ to $1/L^2$ in the original units.

A four-event native order supplies a realized comparability fraction or a chain cardinality. Relating either to these tips, a sampling law, and an elapsed duration per tick requires an independent correspondence. Even for a fixed number of continuum events sampled independently from proper area, the normalized density is $f_\theta\,du\,dv$ at every $L$. The entire sampled order law is invariant under the rescaling above. This clock result uses no calibrated scalar mass, corner propagator or physical area measurement. It concerns only the centre scalar in the supplied family.

[Accepted order and curvature conventions](order_comparability_and_curvature.md) · [Calibrated massive corner comparison](massive_corner_response_and_curvature.md) · [Order and corner readouts](oriented_triples_and_corner_propagation.md)
