# Centre curvature from nested causal diamonds

Two causal diamonds can have the same pair-order probabilities, the same probability for every whole-diamond event count and the same maximum tip-to-tip proper time, yet have different curvature at the centre. The example below keeps the length scale and the event density fixed. In the specified three-coefficient family, mean counts in four registered nested diamonds recover the centre curvature and the density in clock units.

## Geometry and clock

On the unit square let $d=u-v$ and set
$$
ds^2=-2L^2 f(d)\,du\,dv,\qquad f(d)=1-Ad^2-Bd^4-Cd^6,\qquad 0<f(d)\le1 .
$$
Future-directed order increases in both null coordinates. The area measure is $L^2f(d)\,du\,dv$. In the curvature convention $R=2\partial_u\partial_v\log f/(L^2f)$, the centre scalar is $R_c=4A/L^2$. The path $u=v$ has proper length $\sqrt2L$. Every causal path between the same tips has length at most $\sqrt2L$ by $f\le1$ and Cauchy–Schwarz applied to $\sqrt{\dot u\dot v}$. Equality requires the same central path up to parametrization. Its proper time $T=\sqrt2L/c$ therefore registers fractional positions along that diagonal. [Clock and curvature conventions](proper_time_and_curvature_of_a_diamond.md)

## Equal global observations at different curvatures

Let $I(f)=\int f\,du\,dv$ and define $Q(g,h)$ by integrating $g(u-v)h(u'-v')$ over comparable pairs of points in the square. For two independent proper-area draws the probability of comparability is $Q(f,f)/I(f)^2$. Exchangeability splits it equally between the two labelled time directions. The independently supplied count observation is Poisson with mean $\rho L^2I(f)$. These population observations and the central clock constitute the global record. [Pair-order measurement](order_comparability_and_curvature.md)

Take $\alpha=21/26$, $\varepsilon=1/2000$ and
$$
h(d)=14d^2-95d^4+112d^6,\qquad f_\pm(d)=1-\alpha d^2\pm\varepsilon h(d).
$$
The coefficient multiplying $-d^2$ in each factor lies between $\alpha-221\varepsilon>0$ and $\alpha+221\varepsilon<1$, so both metrics obey the bounds over the full square. Direct polynomial integration gives
$$
\int h=0,\quad Q(1,h)=-1/180,\quad Q(d^2,h)=-13/1890.
$$
These identities follow by integrating over the past and future rectangles of one vertex. For $Q(1,h)$ this gives $2\int uv\,h(u-v)\,du\,dv$. For $Q(d^2,h)$ the corresponding weight is $2[uv(u-v)^2/3+u^2v^2/6]$ under the integral, using reflection symmetry for the future rectangle.

Consequently $I(f_\pm)=45/52$ and $Q(1-\alpha d^2,h)=0$. The remaining quadratic term in $Q(f_\pm,f_\pm)$ is identical for both signs. The two worlds agree on the full supplied pair law, the whole-window Poisson law including empty windows, and $T$, while
$$
R_{c,-}-R_{c,+}=\frac{7}{125L^2}.
$$

## Localizing the count observation

Use the central clock to mark the fractions $(1-s)/2$ and $(1+s)/2$ of its duration. Their intervening causal diamond is the centred square of side $s$. Let $m_s$ be the exact population mean count in that square with the same proper-area density $\rho$ throughout. The rescaled means satisfy
$$
\frac{m_s}{s^2}=P(s^2),\qquad
P(x)=\sigma\left(1-\frac A6x-\frac B{15}x^2-\frac C{28}x^3\right),\qquad \sigma=\rho L^2 .
$$
The factors $1/6,1/15,1/28$ are the unit-square averages of $d^2,d^4,d^6$. The four side fractions $1,1/2,1/3,1/4$ give four distinct nodes for cubic interpolation. If $P(x)=p_0+p_1x+p_2x^2+p_3x^3$, the inverse is
$$
\sigma=p_0,\qquad (A,B,C)=(-6p_1,-15p_2,-28p_3)/p_0.
$$
Within the collision above, the half-side mean alone separates the pair by $m_{1/2}^+-m_{1/2}^-=\varepsilon\sigma/8$. Four means recover the whole stipulated family. The nested counts may overlap within each realization.

For a feasible record, $p_0>0$ and $1-Az-Bz^2-Cz^3$ must lie in $(0,1]$ at the endpoints and all interior stationary points on $0\le z\le1$. Additional global records must have the pair and count laws of this same recovered shape. A calibrated $T$ yields $R_c=8A/(cT)^2$ and $\rho=2\sigma/(cT)^2$. For an exact count of $N=T/\Delta$ ticks of unknown duration $\Delta$, the recovered combinations are
$$
R_c(c\Delta)^2=8A/N^2,\quad \rho(c\Delta)^2=2\sigma/N^2,\quad R_c/\rho=4A/\sigma .
$$
Scaling $L$ and $\Delta$ by the same factor and scaling $\rho$ by its inverse square preserves the observations. This inverse depends on shared density, the finite metric family and causal registration of all four windows. Connecting the sampled points or the clock to native DET events requires independent physical evidence.
