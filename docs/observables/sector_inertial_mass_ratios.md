# Inertial mass ratios from three relative-extension readings

**Conditional result accepted on 9 November 2026.** Suppose the three faithfully prepared sector pairs share one stiffness and tick duration, and each phase lies strictly between zero and $\pi$. One exact extension ratio per pair determines $M_1/M_0$ and $M_2/M_0$, enough to test $M_0+M_2=2M_1$. The readings fix $KT^2/M_i$ for each sector. Absolute masses require a calibration of the common mass scale $KT^2$. When each setting may have its own stiffness, an additive and a nonadditive mass triple can give the same law for every retained outcome.

## Native preparations and the retained record

The four native states have order $(00,10,01,11)$ and sector labels $Q=(0,1,1,2)$. Every supported transition stays in its sector. Assigning a positive inertial coefficient to each sector therefore gives a pathwise conserved row $(M_0,M_1,M_1,M_2)$ on each copy. The assignment of mechanical inertia to that row is a new premise. NE042's additivity over the two bits **of one carrier** gives the rectangle equation $M_0+M_2=2M_1$. The two moving bodies below are independent copies of the entire carrier. Sector zero has a positive baseline inertia $M_0$.

Choose the labelled setting $s=(i,j)$ uniformly from $\{(0,1),(0,2),(1,2)\}$. Prepare each copy externally with $\delta_{00},\delta_{10},\delta_{11}$ for sectors $0,1,2$, respectively. In particular the preparation for sector 1 is fixed even though that sector contains two basis states. Faithful sector preparation and persistence of the same $M_i$ across settings are supplied.

For one copy the committed history is $h=(a,b_1,b_2)$, with $a=E,F$ the second ideal and $b_1,b_2$ the two labelled bits. Write $(q_E,\eta_E)=(2/3,1/8448)$ and $(q_F,\eta_F)=(1/3,-1/4224)$. Substitution of the three preparations into the adopted full history law gives, for **each** bit pair,

$$
p_i(h)=\frac{q_a}{4}\left(1+\frac{\eta_a}{2}\mathbf 1_{\{i=1\}}\right).
$$

Each $p_i$ sums to one since $\sum_a q_a=1$ and $\sum_a q_a\eta_a=0$. In particular $p_0=p_2$. The external setting identifies those preparations. Given the setting, the two native histories are independent, and the mechanical reading depends only on the masses and release parameters. For any set of readings $B$, the complete ideal law is

$$
\Pr(s=(i,j),h_1,h_2,y\in B)
=\tfrac13 p_i(h_1)p_j(h_2)\,\mathbf 1_{\{y_{ij}\in B\}} .
$$

This specifies a point mass at $y_{ij}$ for each of the $3\times8\times8=192$ labelled setting/history cells. Both marks and all histories enter with their original weights. Native intermediate and terminal states have been summed over with their original support zeros. The independent-history and negligible-feedback premises allow this product law throughout both comparisons. The inversion uses the reading at each of the three settings. A finite sequence of randomized settings can omit one of them.

## Relative motion, recoil and energy

For this derivation write $K_s>0$ for the stiffness in a setting. Both bodies start at rest on a common inertial axis, with separation $L+D$, $0<D<L$, and a massless ideal spring of equilibrium length $L$. Let $x=X_2-X_1-L$. Releasing both ends together gives

$$
M_i\ddot X_1=K_s x,\qquad M_j\ddot X_2=-K_s x,\qquad
\ddot x=-\omega_s^2 x,\qquad
\omega_s^2=K_s(1/M_i+1/M_j).
$$

The solution from $x(0)=D,\ \dot x(0)=0$ is $x(t)=D\cos(\omega_s t)$. The separation stays at least $L-D>0$. The common positive tick $T$ gives the ideal reading $y_{ij}=x(T)/D=\cos(\omega_s T)$. The shared equilibrium reference and stable linear extension scale at release and at readout make this signed ratio available. A common multiplicative scale cancels in the ratio. The tick is an external sampling operation. The native birth labels supply the order of the two births.

The center of mass stays at rest because the spring forces are opposite. In particular
$\dot X_1=-M_j\dot x/(M_i+M_j)$ and
$\dot X_2=M_i\dot x/(M_i+M_j)$.
Define the reduced mass $\mu_{ij}=M_iM_j/(M_i+M_j)$, so $\mu_{ij}\omega_s^2=K_s$. After ideal release, with stored energy $E_s=K_sD^2/2$, the full ledger is

| Component | Energy at time $t$ |
| --- | --- |
| Body 1 | $E_s\,M_j/(M_i+M_j)\,\sin^2(\omega_s t)$ |
| Body 2 | $E_s\,M_i/(M_i+M_j)\,\sin^2(\omega_s t)$ |
| Spring | $E_s\cos^2(\omega_s t)$ |

The two kinetic terms sum to $\mu_{ij}\dot x^2/2$, and all three terms sum to $E_s$ throughout the release. An ideal reversible loading from equilibrium deposits $E_s$ in the spring. Actual preparation, holding and switching, timing, readout, failures and repeated-use/reset costs require their own accounting. The retained record gives the labelled extension ratio and both native histories. Measuring loading work or force would require additional access.

## Exact common-stiffness certificate

Set $K_s=K>0$ in all settings and keep a common $T>0$. The scientific premise is $0<\omega_s T<\pi$ **in every setting in each candidate world**. Cosine is a bijection on this domain onto $(-1,1)$. For a proposed triple with $-1<y_{ij}<1$, form

$$
d_{ij}=(\arccos y_{ij})^2\in(0,\pi^2),\qquad u_i=KT^2/M_i.
$$

The three equations $d_{ij}=u_i+u_j$ have the unique solution

$$
u_0=(d_{01}+d_{02}-d_{12})/2,\quad
u_1=(d_{01}+d_{12}-d_{02})/2,\quad
u_2=(d_{02}+d_{12}-d_{01})/2 .
$$

**Admissibility is equivalent to $u_0,u_1,u_2>0$** in addition to the three open reading bounds. These are strict triangle inequalities in the *squared* phases. Equality would give a zero inverse-mass parameter, outside the positive finite-mass domain. Necessity follows from the positive finite masses. For sufficiency choose any positive mass scale $C$ and any common $T>0$. Set $M_i=C/u_i$ and $K=C/T^2$. Then each phase is exactly $\sqrt{d_{ij}}\in(0,\pi)$, so this world reproduces all readings and the full joint law. Conversely every common-stiffness explanation has these same $u_i$ and arises with its own $C=KT^2$ and $T$. The dimensionless ratios are therefore $M_i/M_j=u_j/u_i$. Choosing $M_0$ as a reporting unit is one possible normalization.

On this feasible domain the exact additivity test is

$$
F(u)=u_1(u_0+u_2)-2u_0u_2=0 .
$$

Indeed $M_0+M_2-2M_1=C F(u)/(u_0u_1u_2)$, whose denominator and scale are positive. In the additive family $M_q=M_0+q\,b$, positivity requires $M_0>0$ and $b>-M_0/2$. Decreasing, constant and increasing sector inertias are all allowed within that range. The test uses the measured ratios, without a vacuum zero or an orientation convention.

The phase restriction supplies information. A single cosine value also has phase representatives differing by whole periods and sign. The inverse above uses independent assurance that the tick lies strictly inside the first lobe for every trial. Knowledge of the tick in seconds and the absolute stiffness is unnecessary for the ratios, while assurance of a common tick, repeatable stiffness and the phase domain remains essential to this certificate.

## Deterministic joint error feasibility

For finite reported $z_{ij}$ and supplied finite errors $\epsilon_{ij}\ge0$, admit every coordinate combination satisfying $|z_{ij}-y_{ij}|\le\epsilon_{ij}$. Use the same $\epsilon$ in all three coordinates when a common bound is specified. For each coordinate take
$I_{ij}=[z_{ij}-\epsilon_{ij},z_{ij}+\epsilon_{ij}]\cap(-1,1)$.
An empty interval excludes the model. Otherwise transform the whole interval to

$$
J_{ij}=\{(\arccos y)^2:y\in I_{ij}\}.
$$

Explicitly, if $\ell=\max(-1,z_{ij}-\epsilon_{ij})$ and $r=\min(1,z_{ij}+\epsilon_{ij})$, the lower and upper phase-square bounds are $(\arccos r)^2$ and $(\arccos\ell)^2$. Include each endpoint exactly when its original endpoint belongs to $I_{ij}$. An interior singleton is allowed. A singleton at $+1$ or $-1$ is empty after intersection. A reported extreme or an out-of-range report can still have interior candidates when its error band reaches them.

Use one triple $d\in J_{01}\times J_{02}\times J_{12}$. Apply the linear inversion above and define
$$
\mathcal S=\{d: d_{ij}\in J_{ij}\text{ for all settings},\ u_0(d),u_1(d),u_2(d)>0\}.
$$
The unrestricted common-stiffness class is feasible exactly when $\mathcal S$ is nonempty. Test the two subsets
$\mathcal A=\mathcal S\cap\{F=0\}$ and
$\mathcal N=\mathcal S\cap(\{F<0\}\cup\{F>0\})$, evaluating $F$ at $u(d)$.
These finite-dimensional tests use interval constraints, strict linear inequalities and a quadratic equality or strict inequality. Necessity follows by mapping any candidate world's three ideal readings into the intervals. Conversely each feasible point constructs a single mass triple, stiffness and tick by the sufficiency proof. This enforces the common parameters and the three first-lobe conditions jointly.

| Additive subset | Nonadditive subset | Implication within the common-stiffness model |
| --- | --- | --- |
| Empty | Empty | The reports and error bounds are inconsistent with the model. |
| Empty | Nonempty | The bounds exclude additivity. |
| Nonempty | Empty | Every feasible explanation is additive. |
| Nonempty | Nonempty | The reports leave additivity unresolved. |

In particular, if an additive world has slack in all three error bands, a sufficiently small change in $M_2$ preserves the bands and the strict scientific domains while breaking equality. The classification concerns deterministic compatibility. A sampling distribution, coverage probability and physical detector precision would require additional premises.

## Setting-specific stiffness and the complete-record ambiguity

In the comparison class allow $K_{ij}>0$ separately, preserving the common $T,L,D$, identity, preparations and record access. For any positive mass triple and any interior reading triple, choose

$$
K_{ij}=\frac{(\arccos y_{ij})^2}{T^2(1/M_i+1/M_j)} .
$$

Each resulting phase lies strictly between $0$ and $\pi$. Thus in this class both mass hypotheses are feasible for every interior reading triple. With the specified coordinate errors both are feasible exactly when all three $I_{ij}$ are nonempty.

The following pair makes the ambiguity explicit even for data generated with a common spring. Fix $m>0$, a common tick $T>0$, and $K_*=m/T^2$. World A has additive masses $m(1,2,3)$ and common stiffness $K_*$. World B has nonadditive masses $m(1,2,4)$. Use the same $0<D<L$, rest preparation and gain in both.

| Setting | $K^A_{ij}/K_*$ | $K^B_{ij}/K_*$ | $(\omega_{ij}T)^2$ in both |
| --- | ---: | ---: | ---: |
| $01$ | $1$ | $1$ | $3/2$ |
| $02$ | $1$ | $16/15$ | $4/3$ |
| $12$ | $1$ | $10/9$ | $5/6$ |

For example, in setting $02$ world B gives $(16/15)(1+1/4)=4/3$, and in setting $12$ it gives $(10/9)(1/2+1/4)=5/6$. Each phase square is strictly in $(0,\pi^2)$ in both worlds. Their readings $\cos\sqrt{d_{ij}}$ agree setting by setting. Their setting probabilities and both native factors also agree, so the two laws coincide on every one of the 192 labelled cells, including the location and weight of its mechanical point mass.

The release energies in world B relative to A are $1,16/15,10/9$ across the three settings. The extension ratio at the tick agrees in each setting while the stored energy and reversible loading work differ in settings 02 and 12. The two moving bodies carry the kinetic portions in the ledger above, with the respective world's inertia fractions. An observed work value or separate body-velocity measurement would change the observation contract.

This is an inertial consequence of the supplied Newtonian attachment to conserved NE042 sectors. Absolute mass, energy, physical clock or action calibration and the implementation of faithful preparation and stable readout require independent physical premises. The result assigns no duration per native birth. The native law and its access assumptions are given in [Finite conservation, additive quantities and record access](finite_conservation_and_record_access.md).

## Scientific review

Frozen Energy proof SHA-256 `bd9c48fe5f137067779b30deb9e22cbbed0add8f8cfb6284e8fdbcace1be6aa3`. Independent scientific review SHA-256 `d2f364a6f69b8164ebc96f0903884c95245d569871b16ed52aec253c9f1425e8`.
