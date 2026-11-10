# When can a stored occupation count carry rest energy?

A gain in occupation counts has a sharp energy interpretation in the three-carrier experiment. Suppose that an independent calibration gives the store a positive energy spacing $w$ and that the three carrier sectors have registered masses $M_0<M_1<M_2$, with $M_0>0$. With additive rest energies and exact conservation on every trial, the largest mean count gain is

$$
\max_\pi \mathbb E[\Delta s]=
\begin{cases}
117/2744,& w=(3M_1-M_2-2M_0)c^2>0,\\
0,&\text{otherwise}.
\end{cases}
$$

The mass ratios $1:2:4$ make the required spacing zero. The separate comparison $1:2:7/2$ permits a positive spacing of $M_0c^2/2$. The distinction follows from the energies of the carrier strings exchanged in a gain trial.

## Preparation and observable

The four labels $A,B,C,D$ have occupations $0,1,1,2$. Each of three independent, labelled carriers undergoes two marked births under the CL073 preparation. Its terminal label has integer weights $5,4,4,1$, normalized by 14. The terminal label retains those probabilities conditional on every full history $h=(t,b_1,b_2)$. The two bits distinguish four histories for each ideal $t$. An individual history has probability $q_t/4$, with $q_E=2/3$ and $q_F=1/3$. Each native step supports $A\to A$, $D\to D$, and transitions within $\{B,C\}$. Other transitions have zero probability. [Two-birth model and record access](finite_conservation_and_record_access.md)

For a carrier string $x$, let $W(x)$ be the product of its three integer weights and $J(x)$ the sum of its occupations. The store starts at $s=6$, with levels 0 through 12. A fixed permutation $\pi$ of the 64 strings sends $(x,6)$ to $(\pi x,6+J(x)-J(\pi x))$. It preserves the history. The full terminal law, with $H=(h_1,h_2,h_3)$, is

$$
P(H,x,y,s')=\frac{W(x)}{2744}\prod_{i=1}^3\frac{q_{t_i}}4
\,\mathbf 1_{\{y=\pi x\}}\,\mathbf 1_{\{s'=6+J(x)-J(y)\}}.
$$

The readout is $(H,s')$, obtained by summing over $x,y$. The store is fresh and its final level is read ideally. The permutation is chosen before preparation. $B$ and $C$ remain distinct material labels throughout.

## Which controls conserve both quantities?

Assume that a carrier of occupation $q$ has rest energy $M_qc^2$, that these energies add to $E(x)$, and that store level $s$ has energy $e_0+sw$. Both middle labels carry the same registered mass. The carrier rest energy changes by $E(y)-E(x)$. Every other material, kinetic, binding, interaction, support and actuator energy term is held fixed in the stipulated frame.

On the input slice, conservation of total energy is equivalent to

$$
F_w(\pi x)=F_w(x) \quad \text{for every }x,\qquad F_w(x)=E(x)-wJ(x).
$$

This condition suffices for reversibility on the full 832-state system. The specified slice map is injective and takes values inside the store range because $0\le J\le6$. It preserves each joint sector of total occupation $L=J+s$ and energy $T=E+e_0+sw$. In each finite sector the prescribed input and output sets have equal size. Pair the remaining inputs and outputs bijectively to complete the operation. Conversely, conservation by any such extension implies the displayed condition on the slice.

## The only exchange that can increase the mean

Within a fixed $F_w$ sector, arranging the larger probabilities on the lower output occupations minimizes the mean output occupation. Identity is already optimal in a sector unless two strings have their probabilities and current occupations both strictly increasing. The CL073 weights are shown per labelled string. Brackets give the number of strings.

| Occupation $J$ | Weight [multiplicity] |
|---:|:---|
| 0 | 125 [1] |
| 1 | 100 [6] |
| 2 | 80 [12], 25 [3] |
| 3 | 64 [8], 20 [12] |
| 4 | 16 [12], 5 [3] |
| 5 | 4 [6] |
| 6 | 1 [1] |

Only the eight all-middle strings (weight 64, occupation 3) and the three permutations of $DAA$ (weight 25, occupation 2) furnish such an inversion. One group has material energy $3M_1c^2$, the other $(M_2+2M_0)c^2$. Their adjusted energies agree precisely at the stated spacing. At any other spacing, sorting within every allowed sector leaves identity optimal even if other energies coincide. The best separate-carrier control also gives zero, since its count-only upper bound is zero and identity preserves both ledgers.

At the permitted positive spacing, exchange $DAA\leftrightarrow BBB$, $ADA\leftrightarrow BBC$, and $AAD\leftrightarrow BCB$, and fix every other carrier string. Each pair preserves $F_w$. The three lower-occupation slots account for the entire unrestricted improvement $3(64-25)/2744$, so this operation attains the constrained maximum. Its conditional store distribution is the same for each of the $8^3$ histories.

| Count change | Final store level | Probability |
|---:|---:|---:|
| +1 | 7 | 192/2744 |
| 0 | 6 | 2477/2744 |
| −1 | 5 | 75/2744 |

All other store levels have zero probability. The positive mean energy gain $117w/2744$ comes from the carriers. On a gain trial a carrier energy decrease of $w$ pays for the store step. A loss trial returns $w$ to the carriers. At a mismatched spacing the same gain transition would change total energy by $w-(3M_1-M_2-2M_0)c^2$, and the reverse transition has the opposite defect. Identity gives a sharp zero mean off resonance with $s'=6$ on every trial.

## What the mass and work calibrations add

In units of $M_0c^2$, the required positive spacing is $3M_1/M_0-M_2/M_0-2$. For $1:2:4$, a donor gain transition connects two strings of equal material energy and would require an external energy input $w$. For $1:2:7/2$, the same gain joins energies $6M_0c^2$ and $11M_0c^2/2$. If the store independently has the matching spacing, its mean gain is $117M_0c^2/5488$.

A separate spring comparison supplies $u_q=C_{\rm sp}/M_q$, with $C_{\rm sp}=KT^2$. If an independent transfer puts the store spacing on the same linear work display, with gain $g_w$ and scale $D_{\rm work}=g_w C_{\rm sp}c^2$, its required displayed value is

$$
\bar w=g_w w=D_{\rm work}\left(\frac3{u_1}-\frac1{u_2}-\frac2{u_0}\right)>0.
$$

If the work observations allow a set of scales, take the image of that same set under the displayed relation, retaining its calibration and operating constraints. The count record alone supplies neither a dimensional energy gain nor an action scale. Inferring action from sector masses and phases requires a separate phase law, a common Hamiltonian and a time reference. [Sector inertial mass ratios](sector_inertial_mass_ratios.md) · [Mass in displayed work units](spring_mass_scale_in_displayed_work.md) · [Action per occupation](action_per_occupation_from_sector_masses.md)

The theorem concerns one formal terminal operation. Physical interpretation requires evidence for the material registration, the store spectrum and the complete energy ledger. A repeatable work claim would also require accounting for preparation, operation, readout, and restoration of the store and carriers. No physical device or efficiency was measured.

## Scientific provenance

The finite count preparation, ordering bound and readable occupation store come from Classical CL073/v1 and its distinct source and QR-recipient reviews. The additional rest-energy condition and calibrated comparison were derived by DET Relational State Research and checked by DET Energy Research in E54. The description of the carrier energy change incorporates the scientific reviewer’s correction to section 1 of the frozen source. The source and review identities are listed below.

| Frozen record | SHA-256 |
|:---|:---|
| Classical CL073/v1 source | `b1683a62488740f1fa75928bb2edd793372be5abe5a05276b1a3e2591e9c83ae` |
| Classical source review | `e1ce8a00d91711e4bb5d9ad30afc07b88cb52136b203cd200a90f7def63f3983` |
| QR recipient assessment | `7a65517acbcc2e7e7077c1ca14de24397ce51fc34aed26e7f8a8113545557ffd` |
| E54 State result | `757b498bc57d049023d9f64b16b4cd35a7d9283f15b61ad2ea4b84df641b8e24` |
| E54 Energy review | `e32e57afa569609382180094d17ca5a0f96a0c7a9da89e0d28589c14cb00f9cb` |
