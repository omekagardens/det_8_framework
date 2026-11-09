# CL068/v1 — Gravitational work compatible with an exterior field and a polar moment

For the three supported spherical layers specified in the control, the measured exterior field and polar moment allow every gravitational dispersal work in the closed interval
$$
\frac{65}{112}\frac{GM^2}{R}\ \le B\le\ \frac{41}{64}\frac{GM^2}{R}.
$$
An inward field reading in the gap at $R/2$ selects exactly one profile and work value whenever $0\le g_i\le 3GM/(2R^2)$.

## Which profiles give the two measurements?

Let $x,y,z$ be the masses at $R/3,2R/3,R$, respectively, divided by $M$. The exterior shell field gives $M=4R^2g_o/G>0$. With $x+y+z=1$, the prescribed diametral moment reads
$$
\frac{I}{MR^2}=\frac{2}{27}(x+4y+9z)=\frac49.
$$
Eliminating $z$ gives $8x+5y=3$. The complete family is therefore
$$
(x,y,z)=\left(t,\frac{3-8t}{5},\frac{2+3t}{5}\right),\qquad 0\le t\le\frac38 .
$$
The inner and middle masses impose the two bounds. The outer mass is positive throughout. Conversely, every such $t$ gives nonnegative masses and satisfies both records. The endpoints are $(0,3/5,2/5)$ and $(3/8,0,5/8)$. Each is available because the control admits empty layers.

## Gravitational energy and its extrema

Set $q_j=\sum_{i=1}^j m_i/M$, with $q_0=0$, $q_3=1$, and $s_j=r_j/R$. Consider uniform assembly from the inside out. While adding an increment $M\,du$ at $r_j$, the interior mass and the fraction $u$ already added at that radius give potential $-GM(q_{j-1}+u)/r_j$ relative to infinity. Integrating $u$ from $0$ to $m_j/M$ gives negative assembly energy. Reversing the sign for dispersal gives the term $(q_j^2-q_{j-1}^2)/(2s_j)$ in $b=B/(GM^2/R)$. Its expansion counts the layer’s quadratic self term with a half and its interaction with each earlier layer once. In particular a layer retains its self cost even when its neighbor has zero mass.

Summing and collecting adjacent squares gives
$$
2b=q_3^2/s_3+(1/s_2-1/s_3)q_2^2+(1/s_1-1/s_2)q_1^2
   =1+\tfrac12 q_2^2+\tfrac32 q_1^2 .
$$
Now $q_1=t$ and $q_2=3(1-t)/5$, so
$$
b(t)=\tfrac12+\tfrac{9}{100}(1-t)^2+\tfrac34t^2
     =\frac{65}{112}+\frac{21}{25}\left(t-\frac3{28}\right)^2.
$$
The unique minimum occurs at $t=3/28$, with mass fractions $(3,12,13)/28$. The quadratic is strictly convex, so its maximum occurs at an endpoint. The endpoint values $b(0)=59/100$ and $b(3/8)=41/64$ put the unique maximum at $(3/8,0,5/8)$. From $3/28$ through $3/8$ the continuous quadratic increases from the minimum to the maximum and attains every intermediate value. Thus the same two records can give distinct works even with exact ideal measurements.

## Reconstruction from the gap field

At $R/2$ the probe lies outside the first layer and inside the other two. Only the first layer contributes to its acceleration, so the signed inward reading is $g_i=4GMt/R^2$. For an arbitrary real report form $h=g_iR^2/(GM)$. If $h<0$ or $h>3/2$, the joint record is impossible. Otherwise set $t=h/4$, recover $(m_1,m_2,m_3)=M(t,(3-8t)/5,(2+3t)/5)$, and evaluate
$$
B=\frac{GM^2}{R}\left[\frac12+\frac9{100}(1-h/4)^2+\frac{3h^2}{64}\right].
$$
This reconstruction recovers $g_i$ on substitution and preserves both original observations. At $h=0$ and $h=3/2$ it gives the two endpoint profiles above. Strict increase of $h=4t$ proves uniqueness of the profile, including at zero field.

## Physical inputs and scope

The preparations use matched profiles, known geometry, common units and $G$, a negligible field probe, and the supplied infinitesimal common rotation about a diameter. The shell theorem gives the interior and exterior fields. The polar moment, energy reference at infinity and ideal access are specified by the control. $GM/R^2$ sets the acceleration scale, $MR^2$ the inertia scale, and $GM^2/R$ the energy scale. The positive work includes dispersing the material of each shell as well as separating shells. Static supports contribute zero to the defined functional by assumption. Total apparatus disassembly would also require its mechanical work and energy budget. This is a conditional Newtonian calculation on synthetic profiles. [Newton, *Principia*, Book I, Section XII, Propositions LXX–LXXI](https://en.wikisource.org/wiki/The_Mathematical_Principles_of_Natural_Philosophy_%281729%29/Book_1/Section_12)

## Recipient scope

All profiles in this family share the same exterior potential with the common zero at infinity. Their binding energy can still differ. The diametral moment describes rotation of the three layers. Connecting it to the [translational spring measurement](sector_inertial_mass_ratios.md) requires a separate model for the complete package. The interior acceleration at $R/2$ supplies the extra information in this benchmark.

Frozen proof SHA-256 `b173f991b7e883cec0730ebf0255670e6821077cbddbabd5a7a71f8448af38b2`. Independent scientific review SHA-256 `57dc53eac4f12a2e1bc8c4a98c50c088bd71b7a5d4e01b010e7a945eb8d64935`.
Recipient review SHA-256 `b04881606667ab8301807a8ed001f33a19187d4ff5b700d0df118bd5430560a4`.
