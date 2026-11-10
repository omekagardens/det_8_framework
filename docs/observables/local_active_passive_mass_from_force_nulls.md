# Four force nulls and local active/passive mass

**Include the registered reversal.** For two rigid, two-site carriers with positive, stable point coefficients, the four specified net-force readings vanish exactly when all four material sites share a single ratio of passive to active mass. Even an exact aligned null at every separation leaves a local mismatch possible.

## The observed sum

Place carrier A to the left of B and take rightward force as positive in both poses. The aligned offsets are $-d/2,+d/2$ for material labels $0,1$ on each carrier. Let $t=R/d>1$. For A-site $i$ and B-site $j$, define
$$
D_{ij}=p_{Ai}a_{Bj}-a_{Ai}p_{Bj}.
$$
The first product pulls A rightward, and the second pulls B leftward. At separation $d s_{ij}$, the pair contributes $G D_{ij}/(d^2s_{ij}^2)$ to the signed sum of the two forces on matter. The recorded value is that sum times a common positive gain, with verified zero offset. Write $S$ for the sum with the positive factor $G/d^2$ removed. Each of the four settings has probability 1/4 and gives its indicated point reading with success probability one. Only the setting, success and summed reading are observed. The point-force law, fixed weights, negligible backreaction, registered distances and separate treatment of support reactions are premises of this test.

## What the four zeros imply

Aligned, the two equal-label pairs are both at distance $R$. The near pair is $10$, and the far pair is $01$. Thus
$$
S_{\rm al}(t)=\frac{D_{10}}{(t-1)^2}
 +\frac{D_{00}+D_{11}}{t^2}
 +\frac{D_{01}}{(t+1)^2}.
$$
At $t=2,3,4$, multiply each zero equation by $36,144,3600$, respectively. The coefficient matrix on $(D_{10},D_{00}+D_{11},D_{01})$ becomes
$$
\begin{pmatrix}36&9&4\\36&16&9\\400&225&144\end{pmatrix}.
$$
Its determinant is $2588$. Hence $D_{10}=D_{01}=0$ and $D_{11}=-D_{00}$. These equations already imply every aligned null for $t>1$.

After reversing B alone, its material label $1$ is on the left. The near pair becomes $11$, the far pair $00$, and the other two pairs are at $R$. The lab force sign stays fixed. The fourth equation is therefore
$$
0=S_{\rm rev}(2)=D_{11}+\frac{D_{10}+D_{01}}4+\frac{D_{00}}9
 =-\frac89D_{00}.
$$
All four differences vanish. Dividing $D_{ij}=0$ by $a_{Ai}a_{Bj}>0$ gives $p_{Ai}/a_{Ai}=p_{Bj}/a_{Bj}$ for every cross-carrier pair, connecting all four sites to one $k>0$. Conversely, if every site obeys $p=k a$, every pair cancels in either pose. This proves both directions using only sums.

## Matched aligned records

Take all four active weights equal to $m>0$. The passive entries below are in units of $m$, with each row ordered by the material labels.

| World | A passive $(0,1)$ | B passive $(0,1)$ | Common site ratio |
|---|---|---|---|
| I | $(2,2)$ | $(2,2)$ | $k=2$ |
| II | $(1,3)$ | $(3,1)$ | Ratios 1 and 3 both occur |

Each carrier has active total $2m$ and passive total $4m$ in both worlds. In world II, $D_{10}=D_{01}=0$ and $(D_{00},D_{11})=(-2,2)m^2$. Every aligned reading vanishes in both worlds. Using identical setting proportions, success probability one and the same gain gives identical full aligned records. Reversal at $R=2d$ gives physical net force zero in I and $+16Gm^2/(9d^2)$ in II before gain. The reversal changes the distances weighting the two formerly cancelling terms.

## Calibration and scope

The four nulls establish equality of local ratios within this fixture. Each world satisfying them has a unique ratio, but every numerical $k>0$ is compatible with the null record. For example, fix all active weights and choose all passive weights equal to $k$ times their respective active weights. The ratio has units of passive coefficient per active coefficient, dimensionless when the two use the same mass unit. A numerical conversion, including a claim of $k=1$ in a chosen convention, requires independent scale information. The nulls likewise leave $G$, the force gain and the absolute mass and force scales undetermined. The matched totals above are extra facts used to strengthen the control example.

This is an exact inverse for the declared point-force comparison and verified instrumental zero. An unknown offset can turn a nonzero physical sum into a reported null. The prior axial-force result supplied the termwise cancellation argument. Earlier clock, lift, spring and binding results concern different observables and supply no site-resolved registration or direct pair-force sum for this test. The conclusion concerns these four sites and the measured forces on matter. Inertial mass, conversion of native energy and total momentum of a closed apparatus require separate premises.

## Reviewed sources

The [finite-separation axial-force bound](finite_separation_axial_force_bounds.md) proves termwise cancellation under local proportionality for a reciprocal Newtonian kernel. The [registered total active and passive mass comparison](joint_active_and_passive_gravitational_mass.md) and [binding-energy response](gravitational_binding_and_passive_response.md) involve different instruments. DET Quantum Relativity derived the four-pose inverse. DET Relational State Research independently verified its algebra, placement signs and matched-record control.
