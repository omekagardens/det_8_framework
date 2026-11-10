# Contact placement in finite-mass scalar propagation

On the registered four-chain, a positive contact inside the mass deformation reduces the change in the normalized response as the positive control increases. The two registered positive settings identify that contact through the slope of the reciprocal deformation. An exterior contact gives a zero slope for every contact value. Releasing the setting ratio admits an exact collision across all off-site pairs.

## Supplied benchmark

The v5 primary text gives the discrete mass deformation in Eq. (9), the strict massless comparison $K_0=C/2$ in Eq. (14), and its ordered-chain expansion in Eqs. (15)–(16). Those equations supply the benchmark and the mass-insertion convention. The control supplies the two alternatives for adding a contact. Source inspection covered the relevant text in §2 and §2.1. [Nomaan X, Dowker and Surya, arXiv:1701.07212v5](https://arxiv.org/pdf/1701.07212v5)

## Registered order and scalar readout

The prepared prefix is $a\prec b$, with marks $(i,0)$ and descendant counters $(1,0)$ for fixed $i\in\{0,1\}$. The ordered ideals $I_x=\{a,b\}$, $I_y=\{a,b,x\}$ yield the chain $a\prec b\prec x\prec y$. Its structural probability is $779/1320$ under $P_0$ and $574/1320$ under $P_1$. Each ordered pair of suffix marks has one quarter of its row probability. The same prefix, chain event and mark custody apply at every setting.

Use source $a$ and the two labelled target pairs $(b,a)$ and $(x,a)$, with target first. They have zero and one strict intermediate, respectively. The complete conditional means refer to that registered chain and those same pairs. The supplied response has the same value on each of the four marked continuations because their causal matrices agree. All assigned starts and attempts enter the preparation and cost ledger, including outcomes outside the chain event. The original conditional weights determine the occurrence of the recorded order. The scalar map acts on that order after growth.

Let $C_{rs}=1$ when $s\prec r$, with zero diagonal and $C^4=0$. The supplied deformation is
$$
 F_u(K)=K(I+uK)^{-1},\qquad u\ge0.
$$
The alternatives are $K_{\rm in}=F_u(\delta I+\beta C)$ and $K_{\rm out}=\delta I+F_u(\beta C)$ with $\beta>0$, $\delta\ge0$. The zero setting and two distinct positive controls obey $t_0=0<t_1<t_2$, $u_j=\kappa t_j$, with common unknown $\kappa>0$. The declared readings have registered zero offsets, arbitrary positive gains $g_j$ common to both pairs within setting $j$, and fixed positive pair gains $r_L,r_P$. The response of the second pair is signed.

## Finite deformation

For the inside placement set $a_u=1+u\delta>0$ and $z=u\beta/a_u$. Factoring $I+u(\delta I+\beta C)=a_u(I+zC)$ gives
$$
 F_u(\delta I+\beta C)
    =\frac{\delta}{a_u}I+
       \frac{\beta}{a_u^2}C(I+zC)^{-1}.
$$
Indeed, multiplying the right side by $I+u(\delta I+\beta C)$ gives $\delta I+\beta C$. The factor $I+zC$ has finite inverse $I-zC+z^2C^2-z^3C^3$. This calculation also holds at $\delta=0$, using the inverse of $I+uK$ for the singular strict kernel.

For the outside placement the strict part is $\beta C(I+u\beta C)^{-1}$. In either case, write the strict part as $h(C-zC^2+z^2C^3)$, with
$$
 (h,z)_{\rm in}=(\beta/a_u^2,u\beta/a_u),\qquad
 (h,z)_{\rm out}=(\beta,u\beta).
$$
For a strict pair with $m\in\{0,1,2\}$ intermediates, $(C^2)_{rs}=m$ and $(C^3)_{rs}=\binom m2$. The intermediates in the four-chain have a unique strict ordering. Its off-site entry is therefore
$$
                          h(1-z)^m.                \tag{1}
$$
For all reverse pairs the entry is zero. Both placements give $\beta$ on every forward pair at $u=0$. At a fixed positive $u$ and positive $\delta$, the inside placement gives both a smaller link amplitude $h$ and a smaller $z$ than the outside placement at the same $\beta,u$. The inside contact affects propagation through these two factors. An outside contact contributes to the diagonal alone. Unknown run gains can absorb the change in $h$.

## Removing the gains and testing the calibrated settings

Write the link and one-intermediate readings as $L_j,P_j$, respectively. Equation (1) gives
$$
 L_j=g_j r_L h_j,\qquad P_j=g_j r_P h_j(1-z_j),\qquad
 h_0=\beta,\quad z_0=0 .
$$
The link is strictly positive at every setting, and $P_0>0$. Form
$$
               z_j=1-\frac{P_j/L_j}{P_0/L_0},
                         \qquad j=1,2.              \tag{2}
$$
The within-setting quotient removes the common amplitude and run gain. The zero-setting quotient supplies $r_P/r_L$. Equation (2) remains defined when $P_j=0$ or $P_j<0$ at a positive setting.

Set $\alpha=\kappa\beta>0$. The inside placement has
$$
     z_j=\frac{\alpha t_j}{1+\chi t_j},\qquad \chi=\kappa\delta,
$$
and the outside placement has $z_j=\alpha t_j$. For positive $z_j$, let $v_j=t_j/z_j$. From the two points $(t_1,v_1),(t_2,v_2)$ obtain the intercept and slope
$$
 A_0=\frac{t_2v_1-t_1v_2}{t_2-t_1},\qquad
 A_1=\frac{v_2-v_1}{t_2-t_1}.                        \tag{3}
$$
Inside, $v_j=1/\alpha+(\chi/\alpha)t_j$. Outside, $v_j=1/\alpha$.

For finite readings with $L_0,L_1,L_2,P_0>0$, the following gives the full decision for the six displayed values.

| Recovered deformations | Compatible placements |
|---|---|
| $0<z_1<z_2<(t_2/t_1)z_1$ | Inside with $\delta>0$ |
| $0<z_1<z_2=(t_2/t_1)z_1$ | Inside with $\delta=0$, or outside with any $\delta\ge0$ |
| All other cases | Incompatible with both supplied hypotheses |

For positive $z_1,z_2$, $A_0>0$ is equivalent to $z_2>z_1$, and $A_1\ge0$ is equivalent to $z_2\le(t_2/t_1)z_1$. Both statements follow directly by multiplying (3) by the positive denominators. In the feasible region $\alpha=1/A_0$. The inside fit has
$$
            \chi=A_1/A_0,\qquad \delta/\beta=A_1.     \tag{4}
$$
The strict decision corresponds to $z_1/t_1>z_2/t_2$. The equality class leaves the outside contact unrestricted. These are exact inequalities for the stipulated readings.

## Gain and normalization information

The zero-setting measurements determine $g_0r_L\beta=L_0$ and $g_0r_P\beta=P_0$. The pair gain ratio is $P_0/L_0$. In the inside fit, (4) identifies both insertion products $\kappa\beta$ and $\kappa\delta$, and fixes the relative run gains by
$$
          \frac{g_j}{g_0}=\frac{L_j}{L_0}(1+\chi t_j)^2.
$$
The outside fit identifies $\kappa\beta$ with relative run gains $L_j/L_0$ and freely varying $\delta$. At the overlap both formulas for the relative run gains agree.

These also prove sufficiency of the table. For either fit choose any $\beta,g_0>0$. Set $\kappa=\alpha/\beta$, $r_L=L_0/(g_0\beta)$ and $r_P=P_0/(g_0\beta)$. Choose $\delta=\beta A_1$ inside or any permitted $\delta$ outside, and assign the positive relative run gains just given. The link values are reproduced by construction, and (2) reproduces the signed one-intermediate readings. The two freely chosen positive quantities parameterize all inside fits. The free outside contact adds one parameter to the outside fits.

The separation of an absolute kernel scale from mass conversion or gain requires an external anchor. For example, multiplying $\beta,\delta$ by a positive factor and dividing $\kappa,g_j$ by that factor preserves the data with the same pair gains. An additional exchange of a common positive factor between the run gains and the pair gains preserves their products.

## Removing relative setting calibration

Retain the ordered positive settings, the zero setting, the labelled chain and the gain structure. When $u_2/u_1$ is free, any inside response can be reproduced outside. Use the same $\beta$ and set
$$
        u'_j=\frac{u_j}{1+u_j\delta},\qquad
        g'_j=\frac{g_j}{(1+u_j\delta)^2}.              \tag{5}
$$
The function $u/(1+u\delta)$ is strictly increasing, so positive setting order is preserved. The effective $z_j$ and the gain-weighted $h_j$ agree, and the zero setting and pair gains agree. Equation (1) then gives identical readings on all six forward pairs with the same pair gains in the two fits. All reverse-pair readings are zero in both. The outside contact can be chosen equal to the inside contact. The gains in (5) are permitted values of the registered nuisance parameters.

For a concrete collision choose $\beta=\delta=1$ and unit gains throughout the inside fit. Use $u_1=1,u_2=2$. The outside fit uses $\beta=\delta=1$, $u'_1=1/2,u'_2=2/3$, run gains $1/4,1/9$ at the two positive settings, and unit zero-setting and pair gains. The displayed readings on any forward pair are

| Number of strict intermediates | Zero setting | First positive setting | Second positive setting |
|---:|---:|---:|---:|
| 0 | 1 | $1/4$ | $1/9$ |
| 1 | 1 | $1/8$ | $1/27$ |
| 2 | 1 | $1/16$ | $1/81$ |

The inside ratio is $2$, and the outside ratio is $4/3$. With ratio $2$ registered, the displayed values give $z_1=1/2,z_2=2/3$ and identify the positive inside contact. With the relative calibration released both assignments meet the same order and gain contract.

More generally the free-ratio data domain, with the same positivity checks on the baseline and links, is $0<z_1<z_2$. Outside, choose $u_j=z_j/\beta$. Inside, choose any $\beta>0$ and $0<\delta<\beta/z_2$, then set $u_j=z_j/(\beta-\delta z_j)$, an increasing positive function of $z_j$ on the observed range. In each case choose positive run gains to match the links and use the baseline pair ratio. Thus both placements with positive contacts fit every feasible two-pair record in the released calibration, and the all-pair collision follows from (1) and (5).

## Physical registration

The quantities $u\beta,u\delta,z$ are dimensionless, since $uK$ must be dimensionless. The fitted products $\kappa\beta,\kappa\delta$ have reciprocal control units, and the contact ratio $\delta/\beta$ is dimensionless. An absolute kernel normalization would anchor $\beta$. Applying the paper's strict two-dimensional convention would additionally require registering the scalar map and sampling density for its insertion $m^2/\rho$. A physical mass parameter or native length needs an independent dimensional calibration and a correspondence for that operator. The uniform-drive length inverse in the pinned notes concerns its own operator and observation. Transferring its length would require a separate identification with the present pair kernel.

The result concerns exact complete conditional means and registered multiplicative gains. A precision claim needs uncertainty on the signed readings, zero offsets, relative controls and gain stability. Growth supplies the supported marked trials and their original weights. The scalar algebra determines conditional responses on one order, while a continuum comparison requires its own sampling and convergence result.


Related accepted inputs: [Point-source scalar propagation](point_source_propagation_on_finite_orders.md), [scalar response and interval action](scalar_response_length_and_interval_action.md), [unknown mass offset](scalar_length_with_unknown_mass_offset.md), and [finite interval action and source preparation](finite_interval_action_and_source_preparation.md).
