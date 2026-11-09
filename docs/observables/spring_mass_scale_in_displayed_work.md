# A spring mass scale in displayed work units

Independently reviewed conditional result, 9 November 2026.

**Result.** Two echoes measure $L/(cT)$. The signed stroke pairs at $L$ and $2L$ bound $g_w K L^2/2$. Together they determine the exact feasible interval for $D=g_wKT^2c^2$, the spring's common mass scale times $c^2$ in displayed work units. For known redshift gain $g_c>0$, a common passive-to-inertial ratio $k$ has exactly the feasible values $g_c s/D$, where $s$ runs over the signed-lift slope set and $D$ independently runs over this interval. In the worked record these values are $[8/5,2]$. Relaxing the shared work-gain premise admits $k=1$ with the same complete record.

## 1. The fifteen settings and what transfers

Select the original spring/lift arm or the apparatus calibration arm with probability $1/2$ each, independently of preparation. Within each arm choose uniformly among its nine or six settings. Use fresh registered trials. The stable Hooke stiffness $K>0$ in the pair springs also applies to the engaged static strokes over both lengths. The stroke and lift meters have the same positive gain $g_w$, verified signed delivered-work convention and zero. Both stroke alternatives start at the same fixture reference at each length. The spring starts unstretched in each engaged stroke. Endpoints are rigid and at rest, release and reset occur at declared boundaries, and no unmetered moving-leg input is allowed. The fixture can have a different conservative rise at the two lengths. In either apparatus independent nonnegative leg losses enter a passive sink. The conservative assembly returns to its starting state. Store depletion and sink gain over a cycle persist. Initial store level and range must support the signed transfers in each trial.

Use the calibrated *fractional* redshift convention $z_j=g_c\Delta\Phi_j/c^2>0$, registered endpoints, and the accepted conservative passive load work $P_i\Delta\Phi_j$ in each stable weak external field. $P_i$ and $M_i$ use compatible mass units, $\Phi$ has units of speed squared, $K$ has units of mass per time squared, and $g_w$ converts physical energy to displayed work. Supply the same speed $c>0$ in the potential normalization and the round-trip propagation law. Both echoes use the actual one-way stroke lengths, the same mechanical tick $T>0$, and one fixed nonnegative additive delay in tick units. No absolute value of $K,T,L$ or $g_w$ is supplied.

As in the accepted law, sector $i=0,1,2$ prepares $\delta_{00},\delta_{10},\delta_{11}$, respectively, on the same registered whole carrier whenever used. Both internal states of sector 1 share its coefficients. For each eight-valued history $h=(a,b_1,b_2)$ use $p_i(h)=q_a[1+\eta_a{\bf1}_{i=1}/2]/4$, with $(q_E,\eta_E)=(2/3,1/8448)$ and $(q_F,\eta_F)=(1/3,-1/4224)$. The full population law has the following joint weights, including arm choice.

| Setting | Record | Joint probability at the specified reading |
| --- | --- | --- |
| Original spring $i\ell=01,02,12$ | Independent $h,h'$, signed ratio $y_{i\ell}$ | $p_i(h)p_\ell(h')/18$ |
| Original lift, field 1 with 0 or 1, field 2 with 1 or 2 | $h$, ordered $(z_j,w^+_{ij},w^-_{ij})$ | $p_i(h)/18$ |
| Original lift, blank in each field | Empty token and its own ordered triple | $1/18$ |
| Calibration stroke, length $jL,\ j=1,2$, blank or engaged | Labelled outward and return readings $(v^+_{rj},v^-_{rj})$, $r=0,1$ | $1/12$ |
| Calibration echo at each length $jL$ | Delay $d_j$ in tick units | $1/12$ |

Require finite point readings constant across the histories of a setting. For a Borel event multiply the indicated probability by the indicator of the complete reading. Every listed cell has failure flag zero. Both original spring histories, all loaded histories and both empty tokens are retained. The four strokes and two echoes have apparatus labels only. The $192+32+2+6=232$ cells exhaust the law. All other outcomes, including failures, have zero probability.

## 2. Original arm, including the unrestricted test

The relative-extension reading after release from rest at $0<D_{\rm rel}<L_{\rm eq}$ has its assured first-lobe phase in $(0,\pi)$. Require $-1<y_{i\ell}<1$ and put $b_{i\ell}=(\arccos y_{i\ell})^2=b_{\ell i}$. Require all $u_i=(b_{i\ell}+b_{im}-b_{\ell m})/2>0$ for distinct indices. This fixes $KT^2/M_i=u_i$ and reproduces every $y_{i\ell}=\cos\sqrt{u_i+u_\ell}$.

Write $S_1=\{\emptyset,0,1\}$, $S_2=\{\emptyset,1,2\}$ for the lift fields' allowed rows. In each field require the same $z_j>0$ on all its rows including the blank. At known $g_c$, the gaps $c^2z_j/g_c$ must satisfy the supplied local weak-field premises. A prescribed amplitude tolerance has to hold on the actual path. Define $\ell_{ij}=-w^-_{ij},\ h_{ij}=w^+_{ij}$. Require $\ell_{ij}\le h_{ij}$. The finite unrestricted lift test is existence of $x_i>0,\ x_\emptyset=0$, with
$$
 z_j(x_b-x_a)\le h_{bj}-\ell_{aj}
             \quad\text{for all }a,b\in S_j,\quad j=1,2 .                   \tag{1}
$$
Here $x_i=g_wc^2 P_i/g_c$. Indeed one holder per field lies in every interval $[\ell_{ij}-z_jx_i,h_{ij}-z_jx_i]$ exactly when all the lower endpoints meet all the upper bounds. The accepted signed-lift theorem gives an explicit one-variable unrestricted test, or (1) can be tested directly by finite linear elimination.

For $P_i=kM_i$ take $x_i=s a_i,\ a_i=1/u_i,\ a_\emptyset=0$. The **observable slope set** $\mathcal S$ consists of all $s>0$ satisfying (1) under this substitution. In each inequality $A s\le B$ retain $B\ge0$ when $A=0$, the closed lower bound $B/A$ when $A<0$, and the closed upper bound $B/A$ when $A>0$. Their intersection with $s>0$ is exact, including positive singleton contact. The slope is $s=kD/g_c$. Even if $\mathcal S$ is empty, the original arm can have unrestricted positive masses. Failure of (1) itself with free $x_i$ makes the whole stipulated law infeasible.

## 3. Stroke and echo inverse

For each calibration row put $l_{rj}=-v^-_{rj}$, $h^c_{rj}=v^+_{rj}$ and require $l_{rj}\le h^c_{rj}$. Its conservative displayed rise $V_{rj}$ can be any member of this closed interval. The two physical losses are then $(h^c_{rj}-V_{rj})/g_w$ and $(V_{rj}-l_{rj})/g_w$. In particular zero width forces zero loss on each leg. A positive width fixes only their displayed sum. For a signed work pair $(v^+,v^-)$ and a displayed reset level $B_0$, the turning and final levels are $B_0-v^+$ and $B_0-v^+-v^-$. Apply the same capacity check to the lift work pairs. Calibration reset and any replenishment are outside both measured legs.

Let $E=g_wKL^2/2$. At each length the blank and engaged rises are $b_j^c$ and $b_j^c+j^2E$, with one common holder shift $b_j^c=g_w H_j^c$. Integration of the stipulated Hooke force from zero extension gives the $j^2$ factor. Eliminating both holder shifts gives
$$
 \mathcal E=(0,\infty)\ \cap\
 \bigcap_{j=1}^2
 \left[\frac{l_{1j}-h^c_{0j}}{j^2},
       \frac{h^c_{1j}-l_{0j}}{j^2}\right].                               \tag{2}
$$
For necessity subtract the possible blank rise from the possible engaged rise. For sufficiency the intervals $[l_{0j},h^c_{0j}]$ and $[l_{1j}-j^2E,h^c_{1j}-j^2E]$ intersect exactly under (2), given nonnegative row widths. Choose $b_j^c=\max(l_{0j},l_{1j}-j^2E)$ and recover both losses on each row as above. A positive common endpoint is attained. A nonpositive common upper bound excludes a positive spring scale. Both lengths use the same $E$.

In tick units $d_j=d_0+2jL/(cT)$. Define
$$
       \delta=d_2-d_1,\qquad \lambda=\delta/2,\qquad d_0=2d_1-d_2 .
$$
Require $\delta>0$ and $d_0\ge0$, with the zero delay admissible. These are necessary and sufficient for the two echoes at positive $L,T$. They fix $\lambda=L/(cT)$ and the intercept exactly. At any $T>0$ the choice $L=cT\lambda$ realizes both delays. Consequently the exact permitted scale on unrestricted admissible data is
$$
             \mathcal D=\frac{2}{\lambda^2}\mathcal E
                        =\frac{8}{(d_2-d_1)^2}\mathcal E .                 \tag{3}
$$
Here $D=g_w KT^2 c^2$ has displayed work units. The clock offset cancels in the difference, and a negative inferred intercept still rejects the apparatus model. Equations (2)–(3) implement strict positivity, including the possibility of an interval open only at zero.

## 4. Equality decision, construction and reporting unit

After the law, unrestricted lift, mechanics, echoes, strokes and physical-domain checks pass, the exact joint set for $D$ and a common $k$ is
$$
 \{(D,k): D\in\mathcal D,\ k>0,\ kD/g_c\in\mathcal S\}.
$$
Thus the positive ratio set is $g_c\,\mathcal S/\mathcal D$, an interval when nonempty. This denotes all ratios with one independently chosen element of each interval. For a proposed $k>0$ a finite test is $\mathcal D\cap(g_c/k)\mathcal S\ne\varnothing$, preserving the boundary types. In particular equality across all sectors is feasible exactly when $\mathcal D\cap g_c\mathcal S\ne\varnothing$. An empty slope set rejects every proportional model. When both sets are nonempty but the equality intersection is empty, the records exclude equality while admitting proportionality. A unique scale requires a positive singleton in (2). With fixed gain a unique common ratio requires positive singletons for both scale and slope, since their choices are independent.

To prove joint sufficiency pick $D$ in (3), take $E=D\lambda^2/2$, and choose any positive $T,g_w$ in consistent units. Set
$$
 L=cT\lambda,\quad K=\frac{D}{g_wT^2c^2},\quad
 M_i=\frac{D}{g_wc^2u_i},\quad \Delta\Phi_j=\frac{c^2z_j}{g_c},\quad
 P_i=\frac{g_c x_i}{g_wc^2}.
$$
Use an unrestricted lift solution $x$, or for a proposed common ratio use $x_i=s/u_i$ with $s=kD/g_c$. One lift holder per field is $b_j=\max_{i\in S_j}(\ell_{ij}-z_jx_i)$ in displayed units. Take the physical rise $b_j/g_w$. For a lift row with $V=b_j+z_jx_i$, losses $(h_{ij}-V)/g_w,(V-\ell_{ij})/g_w$ are nonnegative. The calibration holders and losses from §3 reproduce both signed stroke pairs at each length. Spring release, weak stationary lift paths, echo zero and travel geometry, store range and reset must satisfy the declared premises. These parameters reproduce every arm-labelled point mass and every blank, history and support zero. This proves that (3) is independent of $\mathcal S$ except for the proposed relation between $D$ and $k$.

For a specified positive reference $W_{\rm ref}$ in displayed work units, define one reporting mass unit as $m_{\rm ref}=W_{\rm ref}/(g_wc^2)$. The exact joint inertial assignments in that convention are
$$
       (M_i/m_{\rm ref})_{i=0}^2
           =\left(D/(W_{\rm ref}u_i)\right)_{i=0}^2,
          \qquad D\in\mathcal D.                                           \tag{4}
$$
The three values share the same $D$. Relative inertias, echo length in light-travel ticks and displayed scale bounds follow from the observations and attachments. Choosing $W_{\rm ref}$ is a convention. The physical Hooke law, signed store, shared gains, tick and path transfer, redshift response, speed $c$ and compatible passive and inertial mass conventions are supplied. Multiplying $K,M_i,P_i$ and physical energies by one positive factor and dividing $g_w$ by it preserves these records when the store is specified in display units. A numerical SI mass requires independent dimensional calibration. Multiplication by $c^2$ in (4) is a choice of reporting unit and supplies no rest-energy measurement or native energy conversion.

## 5. A complete record excluding equality

Choose any displayed work reference $W>0$. For the known $g_c>0$, take $\epsilon>0$ sufficiently small for the stipulated weak-field regime. Write $n=(1,2,4)$, $n_\emptyset=0$. Define the original nine settings by the history law in §1 and the following point values.

- The spring ratios are the cosines of the square roots of $3/2,5/4,3/4$ in order $01,02,12$. These give $u_i=1/n_i$ with strictly positive finite inertias.
- For the two original fields in their allowed blank/load combinations set $z_j=g_c j\epsilon$ and $(w^+_{ij},w^-_{ij})=(4W n_i j\epsilon,-4W n_i j\epsilon)$. The reversible blank fixes each lift holder to zero, and the four loaded rows fix $x_i=4Wn_i/g_c$. Thus $\mathcal S=\{4W/g_c\}$.

For the calibration arm let $d_1=3,\ d_2=5$. The extra four signed work rows are

| Length | Spring | $v^+/W$ | $v^-/W$ | Conservative bracket divided by $W$ |
| --- | --- | ---: | ---: | --- |
| $L$ | blank | 0 | 0 | [0,0] |
| $L$ | engaged | 5/4 | −1/2 | [1/2,5/4] |
| $2L$ | blank | 0 | 1 | [−1,0] |
| $2L$ | engaged | 5 | −4 | [4,5] |

The echoes give $\lambda=1,\ d_0=1$. The two stroke intervals for $E/W$ are $[1/2,5/4]$ and $[1,3/2]$, so $\mathcal E=[W,5W/4]$ and $\mathcal D=[2W,5W/2]$. The shared-gain record therefore gives
$$
                        8/5\ \le k\le 2 .
$$
Both endpoints are attained. With $W_{\rm ref}=W$, the inertia readings in reporting units are the triples $(t,2t,4t)$ with $2\le t\le5/2$. The original nine settings alone allow $k=1$ by choosing the previously free $D=4W$.

**Shared-gain realization.** Choose $g_w=g>0,\ T>0,\ L=cT$, $K=2W/(gL^2)$, $C=KT^2$, and a common rest release within the first lobe as above. Then $D=2W$, $M_i=Cn_i$, $P_i=2Cn_i$ and $k=2$. Use $\Delta\Phi_j=c^2j\epsilon$, stable linear potentials from zero at the lower endpoint, and lossless lifts with zero holders. For any positive endpoint amplitude tolerance take $2\epsilon$ below the tolerance. Both echo rows have the same unit tick-delay intercept. The stroke holders are zero. In row order as displayed above the outward/return **physical losses** are
$$
                 \frac Wg(0,0),\quad\frac Wg(1/4,1/2),\quad
                 \frac Wg(0,1),\quad\frac Wg(1,0).
$$
With conservative displayed rises $0,W,0,4W$, they give exactly the four work pairs. Each blank and every loaded cycle returns its conservative elements to their reference state. Dissipated energy is retained by the sink. For all trials take displayed initial store level $B_0=(10+40\epsilon)W$, with capacities covering each reported turning and final level. Every signed pair leaves nonnegative stored energy since the maximum outward deliveries are $5W$ on strokes and $32W\epsilon$ on lifts. External reset before an independent trial restores the displayed initial level.

**Control with independent work gains.** Change just the model requirement equating the stroke gain and lift gain. Keep the actual lift gain $g$, $P_i$, $g_c$, fields, holders, lift losses and lift store levels as in the previous world. Keep $T,L,c$, path normalization and echo delay. Use $K'=2K$ for **both** the pair release and static engaged strokes, $M_i'=2M_i=P_i$, and stroke gain $g_{\rm st}'=g/2$ on all four stroke rows. The spring pair phases and each history weight agree exactly. The physical stored spring energy at each length doubles. Double the stroke physical losses listed above, including the nonzero loss on the second blank, and retain zero holders. Multiplication by $g/2$ returns every original forward and reverse stroke reading. The stroke store initialized at $B_0/(g/2)$ gives the same displayed initial, turning and final levels as before, while each lift retains its original physical store initialization $B_0/g$. Initializations are independent, registered in display units, with capacity sufficient for both physical fillings. No independently known common physical fill is supplied. The doubled stroke sink gains match the actual stroke-store losses. This world has $k=1$ on the identical 232-cell law, including the six apparatus-only rows. Equivalently the strokes now constrain $g_{\rm st}'K'T^2 c^2=2W$ while the lift compares to $gK'T^2 c^2=4W$. Its restriction to the original arm is the promised equality witness without stroke calibration.

If the common fractional redshift gain is itself free, (1)–(3), $\mathcal S$, the displayed mass scale and the reporting-unit inertia triples can still be tested. For given $D,s,k>0$ the required gain is $g_c=kD/s$. Use precisely those gains for which $z_j/g_c$ are physically admissible weak gaps on the registered paths and all other external calibrations hold. With unrestricted positive gain in the algebraic coefficient law, every $k>0$ fits when $\mathcal D,\mathcal S$ are nonempty. Independent weak-field or gain bounds can narrow that projection. The two echoes calibrate a travel-time ratio and cannot by themselves set the redshift gain.

## Reviewed sources

- [When signed lifting work excludes a common passive-to-inertial mass ratio](signed_lift_work_and_passive_mass.md)
- [Inertial mass ratios from three relative-extension readings](sector_inertial_mass_ratios.md)
- [Testing proportionality of active and inertial mass across three carrier sectors](registered_active_and_inertial_mass.md)

Scientific report SHA-256 4f22efcaf358d95bc8e3671e654b0d6b7d65bd02691164e803b83bcc17c7c8fe. Independent review SHA-256 981326ab8e1ebac14612b9916160fcc145f2fcf94173563c3f1e24f18c0a7e93.
