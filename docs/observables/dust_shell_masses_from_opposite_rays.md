# Two radial rays at one event distinguish the masses of a dust shell

Write $P=T_+$ for the outward ray and $Q=T_-$ for the inward ray. With both transfers defined as exterior over interior Killing energy, the exact compatibility set is the open square $0<P<1,\ 0<Q<1$, including its interior diagonal. At independently known areal radius $R$, a compatible pair gives
$$
 M=\frac{Rc^2}{2G}(1-PQ),\qquad
 \mu=\frac{Rc^2}{G}\sqrt{(1-P)(1-Q)},\qquad
 u=\frac{P-Q}{2\sqrt{(1-P)(1-Q)}}.
$$
Here $M$ is the exterior Schwarzschild mass, $\mu$ is the conserved material proper mass, and $cu=dR/d\tau$ is the outward-signed radius rate on the shell clock. In particular $P<Q$ records collapse.

## The two energy comparisons

Use the flat interior and Schwarzschild exterior of a spherical transparent neutral shell. Write $F_i=1,\ F_o=f=1-2GM/(Rc^2)>0$. In coordinates $(x^0,r)=(ct,r)$ the radial metric on each side is $-F(dx^0)^2+dr^2/F$. The flat time is normalized to an inertial clock at rest in these coordinates, the Schwarzschild time to a static clock at infinity. The two standards are registered independently of the inference. Each test ray is transmitted with continuous phase along the shell, and both sample the same shell state without recoil. This uses the two local null-coordinate derivatives in Harada, Cardoso and Miyata's Eq. (3.5), evaluated at one event. [Harada, Cardoso and Miyata, Sec. III and App. A](https://arxiv.org/pdf/1811.05179v3)

Let $s=+1$ or $-1$ indicate increasing or decreasing photon radius in the future. A future-directed radial photon of positive Killing energy $E=-c p_0$ has covector $p_a=(E/c)(-1,s/F)$. The future-directed shell velocity is $U^a=c(\beta/F,u)$, where $\beta=\sqrt{F+u^2}>|u|$. The shell-frame photon energy is
$$
 -p_a U^a=E\frac{\beta-su}{F}=\frac{E}{\beta+su}.
$$
Continuity of the tangential phase derivative equates this energy on the two sides for each ray separately. With $A=\sqrt{1+u^2}$ and $B=\sqrt{f+u^2}$, this gives
$$
 P=\frac{B+u}{A+u},\qquad Q=\frac{B-u}{A-u}.
$$
For the incoming ray the incident energy is $E_o$ and the transmitted energy is $E_i$. Thus its transmitted-to-incident factor is $1/Q$, while its registered value is $Q=E_o/E_i$. A single comoving frequency gives only the contraction above. A local static exterior observer measures $E_o/\sqrt f$, so converting that energy to the registered standard requires its lapse. There is no reflected segment in this record.

## Necessity, sufficiency and branch signs

Put $h=G\mu/(Rc^2)$. The ordinary outward normals on both sides give the signed dust junction $A-B=h>0$. This is the dust junction used in the [known-exterior-mass traverse](shell_proper_mass_from_crossing_times.md). Here both masses are free and either sign of $u$ is allowed. [Berezin, Eqs. (21)–(23)](https://arxiv.org/pdf/gr-qc/9602020v1)

Since $A>B>|u|$, both transfers lie strictly between zero and one. The root identities $A^2-u^2=1$, $B^2-u^2=f$ give
$$
 PQ=f,\qquad 1-P=h(A-u),\qquad 1-Q=h(A+u).
$$
Multiplication of the deficits gives $h^2$, and their difference gives $2hu=P-Q$. These fix the positive mass branch and the stated inverse.

Conversely, choose any ordered pair in the open square and set $x=1-P,\ y=1-Q,\ h=\sqrt{xy}$. Take $u=(y-x)/(2h)$, $A=(x+y)/(2h)$ and $B=A-h$. Then $A-u=x/h>0,\ A+u=y/h>0$, with product one. The identities
$$
 B+u=P(A+u)>0,\qquad B-u=Q(A-u)>0
$$
give $B>|u|$ and $B^2-u^2=PQ=f$. Thus $A,B$ are the required positive roots, the unsquared difference is $h$, and both forward transfers recover the data. One has $0<f<1$, $M,\mu>0$, and finite $u$ for each such pair. The future-directed shell has $U^aU_a=-c^2$ on each side. This proves pointwise sufficiency and uniqueness without introducing a second junction orientation.

## Local motion, including the diagonal

Set $\ell=c\tau,\ a=G\mu/c^2,\ m=GM/c^2$, and let $r(\ell)$ be the evolving areal radius, initially $R$. Primes on $r$ denote derivatives in $\ell$. The signed constraint and the difference of the squared roots fix
$$
 A(r)=\frac{m}{a}+\frac{a}{2r},\qquad B(r)=\frac{m}{a}-\frac{a}{2r},\qquad (r')^2=A(r)^2-1.
$$
These functions equal the reconstructed roots at $R$. To include initial rest, use the zero-pressure component of the junction. With the ordinary outward normal the angular and time mixed curvature components on a side are $\beta/r$ and $(r''+\tfrac12\,dF/dr)/\beta$ in length units. Zero surface pressure sets the sum of their exterior-minus-interior jumps to zero. Thus
$$
 \frac{r''+m/r^2}{B}-\frac{r''}{A}=\frac{a}{r^2},
 \qquad r''=-\frac{aA(r)}{2r^2}.
$$
The reduction uses $A-B=a/r$ and $B-m/a=-a/(2r)$, with no division by $r'$. [Berezin, Eqs. (16), (18), (19) and (22)](https://arxiv.org/pdf/gr-qc/9602020v1)

The smooth second-order equation has a local solution for data $r(0)=R,\ r'(0)=u$. It preserves $(r')^2-A(r)^2+1=0$ because its derivative is $2r'[r''-A(r)\,dA/dr]=0$. The strict conditions $f(r)>0,\ B(r)>0,\ A(r)>0$ persist on a neighborhood. There $B(r)^2=(r')^2+f(r)$, and the full signed constraint holds. This realizes both open motion branches as well as the diagonal.

If $P=Q=t$, then $u=0,\ f=t^2,\ h=1-t$. The acceleration at that event is $d^2r/d\tau^2=-G\mu/(2R^2)<0$. The solution expands just before the event, attains a strict local maximum of radius, and collapses just after it. A shell held at this radius would require a different stress. The diagonal therefore describes a momentary rest event for every $0<t<1$.

## Reduced records and mass scale

A single outward reading $P=1/2$ admits the following two exact states at the same $R$, even with advance knowledge of collapse. Write $S=Rc^2/G$.

| $P$ | $Q$ | $M/S$ | $\mu/S$ | $u$ |
|---|---|---|---|---|
| $1/2$ | $7/8$ | $9/32$ | $1/4$ | $-3/4$ |
| $1/2$ | $31/32$ | $33/128$ | $1/8$ | $-15/8$ |

In both rows the exterior and interior positive-root sums give the reported $P$, and both pairs lie in the proved realizable set. More generally every fixed $P\in(0,1)$ admits every $Q\in(P,1)$ on collapse. At fixed $Q$ the same ambiguity follows by varying $P$ in $(0,Q)$.

Erasing both direction labels preserves $f,h,M,\mu$ and $|u|$ at known $R$. For unequal entries the two assignments give precisely $u$ and $-u$. At equal entries the speed is zero for either assignment. If instead the ordered pair and energy standards are retained but $R$ is unknown, it still gives $GM/(Rc^2)=(1-PQ)/2$, $G\mu/(Rc^2)=h$, their ratio and signed $u$. Every rescaling $(R,M,\mu)\mapsto\lambda(R,M,\mu)$, $\lambda>0$, preserves both transfers and admits a local history. These exhaust the ambiguity because specifying any positive $R$ fixes both masses. The absolute mass scale comes from the independently supplied $R,c,G$. The result concerns this ideal classical record and its specified standards.

The known-mass traverse registers elapsed proper time between two radii. An optical-volume exposure samples the vacuum exterior and determines total compactness from its split count means. Neither supplies the pair of exterior-to-interior energy comparisons made at the single event here. An echo crossing a moving shell on entry and exit samples two different events. [Split optical volume](radially_split_reflected_light_counts.md)
