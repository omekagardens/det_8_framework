# Recovering a scalar length with one hidden event

The same three visible events $a,b,y$ can be part of either a four-event diamond or a four-event chain. Two calibrated settings of a scalar probe, with three addressed responses at each setting, determine the model length, mass-term offset, chain fraction and common gain. At one setting, different values of all four parameters can give the same readings.

In the diamond the full order has $a$ below both $b$ and $x$, with $y$ above both. In the chain the order is $a<b<x<y$. The hidden event $x$ participates in propagation but cannot be driven or read. The layer matrix $L_j$ connects strict pairs whose open interval contains $j-1$ events. Each positive setting $u$ is an increment in inverse-length-squared units; the actual scalar mass term is $u+d$ with unknown common $d\ge0$. [Finite-order point-source law](point_source_propagation_on_finite_orders.md) · [Scalar-length calibration](scalar_length_with_unknown_mass_offset.md)

## Observation model

The mixture has chain probability $\pi\in[0,1]$ and diamond probability $1-\pi$. The preparation holds this mixture fixed at both settings. It is not inferred from an unobserved selector bit or equated to either original preparation's tabulated row probabilities. The two selected structural rows are supported; conditional fair marks can remain unchanged, since they do not enter the stipulated field matrix.

A matrix entry has target row and source column. Set
$$
 h=2/\ell^2>0,\quad a=d+h>0,\quad t(u)=u+a,\quad r(u)=h/t(u).
$$
Because $u>0,d\ge0$, $0<r<1$. For each full order,
$$
 G(u)=(tI-hN)^{-1}
 =t^{-1}I+ht^{-2}N+h^2t^{-3}N^2+h^3t^{-4}N^3,
 \qquad N=2L_1-4L_2+2L_3.
$$
The finite identity follows from $N^4=0$, not a convergence approximation. Write the measured mean strict responses
$$
 A(u)=g\,\mathbb E[G_{ba}],\quad
 B(u)=g\,\mathbb E[G_{yb}],\quad
 C(u)=g\,\mathbb E[G_{ya}],\qquad g>0.
$$
The sources are separate known unit impulses with the same normalization. All pairs and settings share $g,h,d,\pi$; exact blank subtraction is assumed. Negative strict responses are allowed. An inaccessible event is not physically removed, clamped to zero field, or omitted when determining a full-order layer.

## 2. Full forward law

The relevant powers, taken on each full order before averaging, are:

| Full order and strict pair | $N$ | $N^2$ | $N^3$ |
| --- | ---: | ---: | ---: |
| Diamond $a\to b$ | 2 | 0 | 0 |
| Diamond $b\to y$ | 2 | 0 | 0 |
| Diamond $a\to y$ | 2 | 8 | 0 |
| Chain $a\to b$ | 2 | 0 | 0 |
| Chain $b\to y$ | −4 | 4 | 0 |
| Chain $a\to y$ | 2 | −16 | 8 |

For example, the diamond outer pair has two two-link paths, contributing $8$. The chain outer pair has two one-stop paths with products $2(-4)$ and $(-4)2$, and one three-link path with product $8$. The registered pair $b\to y$ is a link only in the diamond: $x$ lies between it in the chain.

Consequently
$$
 \boxed{A=\frac{2gh}{t^2}>0,}
$$
$$
 \boxed{B=A[\,1-3\pi+2\pi r\,],\qquad
 C=A[\,1+4(1-3\pi)r+4\pi r^2\,].}                 \tag{1}
$$
**Corrected exact averaging identity for this two-order family.** Use the common address order $(a,b)\mid(x,y)$, and write
$$
 N_i=\begin{pmatrix}P&0\\K_i&P\end{pmatrix},\quad
 P=\begin{pmatrix}0&0\\2&0\end{pmatrix},\quad
 K_D=\begin{pmatrix}2&0\\2&2\end{pmatrix},\quad
 K_{Ch}=\begin{pmatrix}-4&2\\2&-4\end{pmatrix}.
$$
These blocks give precisely the full-order layer coefficients used above. Only $K_i$ varies. For every integer $m\ge1$, the diagonal blocks of $N_i^m$ are $P^m$ and its lower-left block is
$$
 \sum_{j=0}^{m-1}P^jK_iP^{m-1-j}.
$$
Each term is linear in $K_i$: a directed path crosses the block boundary at most once. Therefore, with $\bar N=(1-\pi)N_D+\pi N_{Ch}$,
$$
 \boxed{\mathbb E[N_i^m]=\bar N^m\quad(m\ge1).}
$$
Since the inverse is the finite polynomial already displayed, this proves
$$
 \boxed{\mathbb E[(tI-hN_i)^{-1}]=(tI-h\bar N)^{-1}.}
$$
Equivalently, put $T=tI_2-hP$. The diagonal blocks of the full inverse are $T^{-1}$ and its lower-left block is $hT^{-1}K_iT^{-1}$, again affine in the variable block. The gain is common, so the identity survives the readout gain and visible restriction.

Thus (1) can be derived either by averaging per-order inverse responses or by using the averaged **full four-event** matrix. This equality relies on the displayed shared block structure; averaging nonlinear matrix functions is not generally justified for arbitrary order families. Here the mean block is
$$
 \bar K=\begin{pmatrix}2-6\pi&2\pi\\2&2-6\pi\end{pmatrix},
$$
which retains the hidden address and its mixture-dependent coefficients. It is not a layer matrix freshly recomputed on the visible three-chain. At positive increments the forward law still requires the full positive-setting formula, rather than substitution of zero-mass responses from the zero-mass point-source comparison.

For pure diamond, $B/A=1$, $C/A=1+4r>1$.
For pure chain, $B/A=-2+2r\in(-2,0)$, $C/A=1-8r+4r^2$, whose sign need not be positive. Both endpoints are admitted without changing the inverse below.

## 3. Eliminating $x$ retains a setting-dependent visible operator

Let $F=tI-hN$, $V=(a,b,y)$, and partition visible and hidden coordinates. The hidden equation, with zero external source at $x$, gives
$$
 \phi_x=-F_{xx}^{-1}F_{xV}\phi_V,\qquad F_{xx}=t>0.
$$
Thus the visible field satisfies
$$
 F_{\rm eff}(u)\phi_V=J_V,\qquad
 F_{\rm eff}=F_{VV}-F_{Vx}t^{-1}F_{xV},\qquad
 G_{VV}=F_{\rm eff}^{-1}.                         \tag{2}
$$
Every diagonal of $F_{\rm eff}$ is $t$, and every unlisted strict or backward entry vanishes. Its strict coefficients are:

| Target, source | Diamond $F_{\rm eff}$ | Chain $F_{\rm eff}$ |
| --- | --- | --- |
| $b,a$ | $-2h$ | $-2h$ |
| $y,b$ | $-2h$ | $4h-4h^2/t$ |
| $y,a$ | $-2h-4h^2/t$ | $-2h+8h^2/t$ |

For the diamond, $F_{yx}=-2h,F_{xa}=-2h$; for the chain, $F_{yx}=-2h,F_{xa}=4h,F_{xb}=-2h$. These entries directly give (2), including its signs. Inverting these three-by-three triangular operators reproduces every entry in the full-order table and (1).

This is elimination of an unregistered degree of freedom, not deletion of its physical contributions. In addition to retaining full-order layer assignments, it adds the paths through $x$, with coefficients depending on $u$. At the population level the observed visible kernel is
$$
 (1-\pi)F_{{\rm eff},D}^{-1}+\pi F_{{\rm eff},Ch}^{-1}
 =\boxed{\big[(1-\pi)F_{{\rm eff},D}+\pi F_{{\rm eff},Ch}\big]^{-1}}
 \quad\text{for this family}.
$$
To verify the equality rather than assume it, write each effective operator in visible order $(a,b)\mid y$ as
$$
 F_{{\rm eff},i}=\begin{pmatrix}T&0\\w_i&t\end{pmatrix},
 \qquad
 F_{{\rm eff},i}^{-1}
 =\begin{pmatrix}T^{-1}&0\\-t^{-1}w_iT^{-1}&t^{-1}\end{pmatrix}.
$$
Here the same $T=tI_2-hP$ and $t>0$ occur in both orders; only the row $w_i=((F_{\rm eff})_{ya},(F_{\rm eff})_{yb})$ varies. The inverse is affine in that row, proving the identity. The averaged effective operator has diagonal $t$ and
$$
 (\bar F_{\rm eff})_{ba}=-2h,\quad
 (\bar F_{\rm eff})_{yb}=(-2+6\pi)h-4\pi h^2/t,\quad
 (\bar F_{\rm eff})_{ya}=-2h+(-4+12\pi)h^2/t.
$$
Moreover, the full $F_{Vx}$ (only its $y$ component is $-2h$) and $F_{xx}=t$ are common to both orders. Only $F_{xV}$ varies. Hence
$$
 \overline{F_{\rm eff}}
 =\overline{F}_{VV}-\overline{F}_{Vx}t^{-1}\overline{F}_{xV}
 =\operatorname{Schur}_x(\overline F).
$$
Averaging the full operator then eliminating $x$, or eliminating on each order then averaging the effective operator, gives the same operator here. Inverting it gives the correctly averaged visible response. These are family-specific equalities, not general rules for arbitrary mixtures.

The retained $h^2/t$ terms and the mixture-dependent entries encode the unregistered event. Losing access to $x$ therefore does not justify discarding it from the assumed field model. An exact averaged operator, which uses this information, remains different from a law rebuilt using only the induced three-event order.

Recomputing on the induced three-chain $a<b<y$ instead gives layer entries $N_{ba}=N_{yb}=2,N_{ya}=-4$, and no hidden contribution. For any positive candidate $h'$, common gain $g'$, and offset $d'$, put $t'=u+d'+h'$. Its strict responses would obey
$$
 A'=B'=\frac{2g'h'}{t'^2},\qquad
 \frac{C'}{A'}=-2+\frac{2h'}{t'}.                  \tag{3}
$$
These are a different propagation law on the same registered addresses.

## 4. Visible-order compatibility decision

For every $\pi>0$, (1) gives
$$
 \frac BA=1-\pi(3-2r)<1.
$$
Equation (3) requires $B'/A'=1$. Hence a single setting already rejects the induced-order model on this branch, independently of its candidate length or offset.

For $\pi=0$, the full responses instead have $A=B>0$, $C/A=1+4r>1$. With the stipulated candidate $d'\ge0,g'>0$, (3) gives $-2<C'/A'<0$, again rejecting it at a single setting.

The two-setting rejection remains true even if “any offset/gain” is read as allowing arbitrary real $d'$ and $g'$, provided its responses exist and $h'>0$. A match to $A_i>0$ forces $g'>0$. In pure diamond, matching $C_i/A_i>1$ forces $t'_i>0$. The ratio $A_1/A_2$ then uniquely fixes $d'+h'=a$ (as proved below), so $t'_i=t_i$. The two outer ratios would require
$$
 2h'=3t_i+4h\quad(i=1,2),
$$
impossible because $t_2-t_1=u_2-u_1\ne0$. Thus no offset, positive length and common gain rescues the induced-order model across the requested data. A signed offset could remove the one-setting pure-diamond sign obstruction, but cannot remove this two-setting contradiction.

The rejection concerns recomputing this particular stipulated layer law on the induced order. A conventional calculation retaining the full law or its exact elimination has the same information and succeeds.

## 5. Necessary-and-sufficient two-setting inverse

Relabel the two settings so $0<u_1<u_2$. Let $A_i,B_i,C_i$ be the six exact real readings. Every step below is a finite algebraic decision; all equality checks are exact.

**Locate the shared pole parameter.** Require $A_1,A_2>0$, set
$$
 R=\sqrt{A_1/A_2}.
$$
Require $1<R<u_2/u_1$ before division, and set
$$
 a=\frac{u_2-Ru_1}{R-1},\qquad t_i=u_i+a.
$$
The ratio bounds imply $a>0$. Then $t_i>0$ and $R=t_2/t_1$. The pole at $-a$ is recovered without observing contact and without measuring at zero or negative increment. This is interpolation within the asserted response family, not a physical observation at that pole.

**Separate mixture and length.** Define
$$
 q_i=B_i/A_i,\quad z_i=C_i/A_i,\quad
 \zeta=\frac{q_1-q_2}{2(t_1^{-1}-t_2^{-1})},\quad
 \pi=\frac{1-q_1+2\zeta/t_1}{3}.                 \tag{4}
$$
Equation (1) reads $q_i=1-3\pi+2\zeta/t_i$, with $\zeta=\pi h$. The denominator in (4) is strictly positive. Require the resulting $\pi\in[0,1]$.

- If $0<\pi\le1$, require $\zeta>0$ and set $h=\zeta/\pi$.
- If $\pi=0$, require $\zeta=0$ and $q_1=q_2=1$. Set
  $$
    h=(z_1-1)t_1/4,
  $$
  and require also $h=(z_2-1)t_2/4$.
- Reject every other case.

**Check physical parameter range and all readings.** Require $0<h\le a$, and set
$$
 d=a-h\ge0,\qquad \ell=\sqrt{2/h},\qquad
 g=A_1t_1^2/(2h)>0.
$$
Finally require both $A_i=2gh/t_i^2$, both $q_i=1-3\pi+2\pi h/t_i$, and both
$$
 z_i=1+4(1-3\pi)h/t_i+4\pi h^2/t_i^2.            \tag{5}
$$
The final checks explicitly reject arbitrary inconsistent data. In particular, equality of the two $q_i$ is feasible only at $q_i=1,\pi=0$; a constant different value would imply $h=0$. No positivity restriction is imposed on $B_i$ or $C_i$.

**Necessity, sufficiency and uniqueness.** Necessity follows by substituting (1). Conversely, if these tests pass, prepare the two supported rows with the recovered weights, use the recovered $h,d,g$, and retain the hidden event in the operator. Equation (1) then reproduces all six readings, so the tests are sufficient. The positive square root fixes $a$ uniquely because both $t_i>0$. The two distinct inverse $t_i$ fix $\pi,\zeta$ uniquely. If $\pi>0$, their quotient fixes $h$; if $\pi=0$, (5) fixes $h$. Then $d,\ell,g$ follow uniquely. Thus no two feasible tuples survive.

The pure-chain case is simply the $\pi=1$ endpoint of the positive-$\pi$ branch. The pure-diamond case has its separate nonsingular algebraic branch using $C$. A zero offset is the allowed $h=a$ endpoint. A vanishing or increasing $A$, a nonpositive recovered $a$, a negative offset, an out-of-range mixture, or any failed forward equality rejects the supplied model.

These are exact identifiability statements. Narrow setting separation, $R$ near one, or a small positive chain weight can make parameter estimation sensitive to error. No finite-precision, finite-sample or instrument-resolution guarantee is established.

## 6. One-setting collision, with all standards held fixed

Let the single declared positive calibrated increment be $u=U>0$, and let $g_0>0$. Use the same visible addresses, unit impulses, blank convention and output standard in two admissible worlds:

| Parameter | World A | World B |
| --- | --- | --- |
| $h$ | $U$ | $6U$ |
| $d$ | $0$ | $U$ |
| Chain fraction $\pi$ | $1/4$ | $1/3$ |
| Gain $g$ | $g_0$ | $8g_0/3$ |
| $t(U)$ | $2U$ | $8U$ |
| $r(U)$ | $1/2$ | $3/4$ |
| Length $\ell$ | $\sqrt{2/U}$ | $\sqrt{1/(3U)}$ |

Both worlds give exactly
$$
 \boxed{(A,B,C)=\left(\frac{g_0}{2U},\frac{g_0}{4U},
                         \frac{7g_0}{8U}\right).} \tag{6}
$$
Indeed $B/A=1/2,C/A=7/4$ in each world. All parameters are within the stated ranges; the source mixtures are supplied preparations of the two supported rows. Unknown gains may differ between candidate worlds, while remaining common to all pairs in each world, as the nuisance-parameter contract permits. Neither the input increment nor its calibration changes.

The ambiguity in ratios can also be checked directly: at one setting, writing $q=B/A,z=C/A,k=(z-1)/4$, elimination of $\pi$ gives
$$
 (1+q)r^2-(3q+2k)r+3k=0,\qquad
 \pi=(1-q)/(3-2r).
$$
For (6) its two feasible roots are $r=1/2,3/4$, giving the two displayed fractions. The amplitude is then matched by the stated gains.

Even if the mixture were separately fixed, one setting could not fix length and offset. Starting from any feasible world at $U$, for any $\lambda\ge1$ replace
$$
 h\mapsto\lambda h,\quad
 d\mapsto\lambda(U+d)-U,\quad
 g\mapsto\lambda g,\quad \pi\mapsto\pi.
$$
Then $t(U)\mapsto\lambda t(U)$, so all three readings remain unchanged and the new offset is nonnegative. This covers both pure-chain and pure-diamond worlds as well. It is a one-setting ambiguity with fixed calibrated $U$; it does not preserve two distinct calibrated settings.

For the particular worlds in the table, their $A(u)$ curves already agree at a positive $u$ only if $u=U$: equality reduces to $u+7U=4(u+U)$. Thus their second-setting separation does not require accessing $x$.

## 7. Dimensional scale and information allocation

The layer assignments and integer path products are dimensionless order information. The choices $2,-4,2$, the inverse operator, $h=2/\ell^2$, and a scalar mass-term offset are the stipulated dynamics; order counts alone do not select them. The three visible addresses identify response channels, not the hidden topology of an individual trial. The inferred $\pi$ is a population preparation weight within exactly the supplied two-row family, not an event tag or a reconstruction of all possible native orders.

The calibrated $u_i$ carry inverse-length-squared units. Then $a,h,d,\zeta$ have those units, $t^{-1}$ has length squared, and (1) has units $g$ times length squared for the declared unit impulse. The common gain assumption lets pair ratios cancel detector normalization and lets the two-setting amplitude ratio locate $a$. A known common impulse normalization is necessary to interpret the recovered $g$ as gain; an extra unknown overall drive factor would merge with it. Pair-specific or setting-specific unknown gains are outside this inverse.

If instead the displayed settings are $v_i$ and $u_i=k v_i$ with unknown $k>0$, the same procedure identifies exactly
$$
 H=h/k,\quad D=d/k,\quad \Gamma=g/k,\quad \pi,
 \qquad \ell\sqrt{k}=\sqrt{2/H}.
$$
The forward formula in $v$ has exactly the same form with $h,d,g$ replaced by $H,D,\Gamma$. For every $\lambda>0$,
$$
 (k,h,d,g,\ell,\pi)\mapsto
 (\lambda k,\lambda h,\lambda d,\lambda g,\ell/\sqrt\lambda,\pi)
$$
preserves all six displayed readings. Conversely the two-setting uniqueness proof fixes $H,D,\Gamma,\pi$, so this common scale is the entire remaining ambiguity. Absolute $\ell,d,g$ are lost, while $\pi$, $d/h$, $g/h$ and whether $d=0$ survive. The external setting standard supplies the absolute dimensional scale.

[Supported four-event preparations](finite_interval_action_and_source_preparation.md) · [Aggregate scalar response](scalar_response_length_and_interval_action.md)
