# Opposite-corner propagation and the direction of three-event branching

**Decision.** The two time-oriented continuum candidates have identical normalized corner responses at every finite nonnegative scalar mass. A three-event observation separates their population laws: counting two incomparable predecessors of a common successor as $+1$, and the reversed shape as $-1$, gives means $+1/40$ and $-1/40$. On the separate native four-event support, the full incidence counters suffice to compute the corresponding random-triple mean for each terminal order.

## Why even a complete mass scan agrees

Write $a(u)=2u-1,\ b(v)=6v^2-6v+1,\ f_s=1+s\,a(u)b(v)$, $s=\pm1/2$. On the open unit square take $ds^2=-2L^2f_s\,du\,dv$ and future order increasing in both coordinates. Since $|a|\le1$ and $-1/2\le b\le1$, $1/2\le f_s\le3/2$. Both factors $a,b$ integrate to zero, so the proper area is $L^2$ and $d\mu_s=f_s\,du\,dv$ is normalized area.

Let $P=(0,0), F=(1,1)$ and $T(u,v)=(1-u,1-v)$. Under $T$, $a$ changes sign, $b$ does not, and $du\,dv$ retains its sign and magnitude. Thus $T^*g_{-s}=g_s$ and $T$ transports $\mu_s$ to $\mu_{-s}$. It exchanges the two corners and reverses every strict causal comparison. The metrics are isometric when time orientation is forgotten. Within each candidate the source is always its own registered past corner and the receiver its own future corner.

For the supplied minimally coupled retarded field with a covariant unit impulse and no reflected signal, $G_0(F,P)=1/2$. Let $x=m^2L^2/2$. Iterating the mass deformation using metric-volume convolution gives the normalized response
$$
 Q_s(x)=\frac{G_m(F,P)}{G_0(F,P)}=\sum_{n=0}^{\infty}(-x)^n I_n(s),\qquad
 I_n(s)=\int_{P\prec z_1\prec\cdots\prec z_n\prec F}\prod_{j=1}^n d\mu_s(z_j),\quad I_0=1 .
$$
There are $n+1$ massless factors before normalization and $n$ proper-area factors. A labelled chain requires one prescribed ordering of its $n$ continuous $u$ coordinates, hence $0\le I_n\le1/n!$. This bound gives absolute convergence for every finite $x$ and also bounds the ordered integrals on subdiamonds in the retarded iteration. [Wave law, equations (3)–(4) and §3.1](https://arxiv.org/pdf/1701.07212v5) · [Accepted corner normalization](massive_corner_response_and_curvature.md)

Map each chain to $(Tz_n,\ldots,Tz_1)$. This is a measure-preserving bijection onto the increasing chains in the other candidate. Thus $I_n(s)=I_n(-s)$ term by term, and $Q_s(x)=Q_{-s}(x)$ for the **entire scan**. The reversal of the integration labels matters: the retarded calculation in the second candidate still runs from its past to its future. Mass calibration or arbitrarily precise corner amplitudes alone cannot decide the sign.

## The signed triple expectation

Draw three independent points from $\mu_s$ and retain the whole oriented order outcome, scoring other shapes zero. Call a triple with one greatest event and two incomparable predecessors a join; its time reverse is a fork. Write $A(u)=u^2-u,\ B(v)=2v^3-3v^2+v$, so $A'=a,\ B'=b$ and both primitives vanish at both endpoints. The past-area fraction at $(u,v)$ is
$$
 P_s(u,v)=uv+sA(u)B(v).
$$
The probability that **one specified label** lies above the other two is $J(s)=\int f_s P_s^2\,du\,dv$. By reversal the corresponding probability for one specified label below the other two is $J(-s)$. There are three choices of the distinguished label. The other two labels are already integrated in both possible orders. A three-chain has exactly one greatest and one least element; its probability is $6I_3(s)$ since its labels can be permuted in six ways. Consequently
$$
 \Pr_s(\mathrm{join})=3J(s)-6I_3(s),\quad
 \Pr_s(\mathrm{fork})=3J(-s)-6I_3(s),\quad
 \mathbb E_s[\mathrm{score}]=3[J(s)-J(-s)] .
$$

Only the odd powers in $J(s)=\int(1+sab)(uv+sAB)^2\,du\,dv$ contribute. Its linear coefficient, with one-dimensional integrals on $[0,1]$, is
$$
 \left(\int au^2\right)\left(\int bv^2\right)+2\left(\int uA\right)\left(\int vB\right)
 =\tfrac16\cdot\tfrac1{30}+2\left(-\tfrac1{12}\right)\left(-\tfrac1{60}\right)=\tfrac1{120}.
$$
The cubic coefficient $(\int A'A^2)(\int B'B^2)$ vanishes by the endpoint values. Hence the signed mean is exactly $s/20$, or **$+1/40$ at $s=+1/2$** and **$-1/40$ at $s=-1/2$**. Distinguishing these means requires a physically registered direction of precedence and proper-area sampling. Neither coordinates nor interior clock tags are needed to score an observed triple. One draw does not determine its population mean.

## What is accessible on a native four-event order

Let $c_v$ count the strict descendants of event $v$, and $d_{\{v,w\}}$ the common strict descendants of a distinct unordered pair. On a fixed terminal order choose one of the four three-element subsets uniformly, without replacement. Its exact conditional signed mean is
$$
 \frac{1}{\binom43}\left[\sum_{\{v,w\}}d_{\{v,w\}}
               -\sum_v\binom{c_v}{2}\right].
$$
The first sum counts triples with a greatest vertex by pairing its two predecessors. The second counts triples with a least vertex by pairing its two successors. Chains occur once in both sums and cancel; each join contributes $+1$ and each fork $-1$. This identity holds on each supported order and may be averaged with its original preparation weights.

The register must start empty or with consistent prefix values. For $a\prec b$ these are $c_a=1,c_b=0,d_{\{a,b\}}=0$. A birth increments every vertex in its strict past and every old pair contained in that past, appending the newborn's zero cells. At four events the vertex and pair counts are at most three and two, respectively, so modulo-five updates have not wrapped. Both sums are invariant under relabelling; access to the two sums or to the full correctly typed counters suffices. The published bit “any pair has a common descendant” alone does not suffice. For example, a supported fork plus an isolated event and two disjoint links both yield bit zero, while their random-triple means are $-1/4$ and 0. No individual counter histories or new native growth law enter the identity. [Pair-register preparation and readout](finite_pair_incidence_register.md) · [Supported native orders](finite_interval_action_and_source_preparation.md)

**Geometric scope.** The signed statistic distinguishes an orientation-dependent distribution of branching within this prescribed pair. Any time-orientation-preserving isometry of these diamonds would preserve both normalized proper area and the signed mean. The opposite means exclude such an isometry. Forgetting the time orientation removes that distinction through the explicit isometry $T$. The scalar scan presupposes a shared source/detector gain between mass settings, normalization to a massless reference, and a calibrated mass-area product. The signed triple itself is dimensionless. Its value supplies neither an absolute length nor a generic metric reconstruction. A native order drawn from its growth law and a continuum triple drawn from proper area are distinct preparations; a common scoring rule does not establish a sampling correspondence or a physical detector. [Prior comparability and sampling distinction](order_comparability_and_curvature.md)
