# What an unlabelled store-resonance catalogue measures

**DET Energy Research · Conditional inverse for three carriers**

If the complete catalogue has at least two distinct lines and is consistent with the stated model, let $L$ be its largest spacing and $S$ its second largest. The two adjacent sector rest-energy gaps are **$S$ and $2S-L$**. Their occupation labels remain ambiguous. A singleton $\{\ell\}$ identifies two equal gaps $\ell$. The rest of the catalogue tests the model, one registered transition distinguishes the two possible assignments, and the common mass offset remains free.

## 1. What counts as a spectral line

Three independent labelled carriers have states $A=00,B=10,C=01,D=11$, occupations $0,1,1,2$, and registered masses $M_0,M_1,M_1,M_2$ with $0<M_0<M_1<M_2$. Define the ordered rest-energy gaps
$$
a=(M_1-M_0)c^2,\qquad b=(M_2-M_1)c^2.
$$
The order in $(a,b)$ denotes occupation transitions $0\to1$ and $1\to2$. Either gap may be the larger. Each carrier undergoes the two marked CL073 births. Conditional on each full history, its terminal labels have weights $(5,4,4,1)/14$. Thus all 64 strings have positive probability, including strings that differ only in a $B,C$ label.

Use the accepted full joint permutation criterion. Each probe begins with a fresh store at level 6 in the range $0,\ldots,12$. Its energy is $e_0+sw$, with one independently calibrated positive spacing $w$ across the range. In a fixed rest frame, the carrier energy $E(x)$ is the sum of the three registered rest energies. Its change $E(y)-E(x)$ is included in the ledger. All other material, kinetic, binding, support, interaction and actuator energy terms are held fixed. A predeclared permutation on carriers and store preserves total occupation and total energy pointwise and leaves histories intact.

A spacing $w>0$ has a positive-mean tag exactly when a pair of strings satisfies
$$
\Delta j=J(x)-J(y)>0,\qquad E(x)-E(y)=w\Delta j .
$$
Indeed, a positive mean needs at least one gain trial. Conversely, transpose the joint states $(x,6)$ and $(y,6+\Delta j)$ and fix every other joint state. Both totals agree, the shifted store level lies within its range, and the reverse endpoint is unoccupied on the fresh slice. Only the positive-weight input $x$ moves on that slice. This is sufficiency for a positive tag at that particular spacing. Distinct spacings may have different witnessing controls. Requiring the carrier projection alone to be bijective would change the pair test.

The spectral datum $\mathcal C$ is the set of all distinct positive tagged spacings, with absence certified everywhere else. It carries no source or target labels, line multiplicities, gain magnitudes or trial probabilities. All formulas may be used in physical energy units or after dividing every spacing and gap by the same supplied positive energy standard $W$.

## 2. The complete set of slopes

For a string let $j$ be its occupation and $d$ its number of $D$ labels. It has $j-2d$ middle carriers and $3-j+d$ carriers in $A$. Its energy is
$$
 E(j,d)=3M_0c^2+a j+(b-a)d .
$$
The possible $d$'s at each $j$ follow by requiring these counts to be nonnegative integers.

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $d$ | 0 | 0 | 0, 1 | 0, 1 | 1, 2 | 2 | 3 |

Every entry is attained. For a pair with occupation difference $k>0$, subtract the entries for $j$ from those for $j+k$ and take their union over $0\le j\le6-k$. This finite subtraction gives the following numerators. For example, at $k=1$, the rows at occupations 2 and 3 allow $\Delta d=-1$, and those at 3 and 4 allow $\Delta d=2$.

| $k=\Delta j$ | Possible $\Delta d$ |
| ---: | --- |
| 1 | $-1,0,1,2$ |
| 2 | $0,1,2$ |
| 3 | $0,1,2,3$ |
| 4 | $1,2,3$ |
| 5 | $2,3$ |
| 6 | $3$ |

Dividing each row by $k$ and merging repeated values gives exactly
$$
\mathcal T=\left\{-1,\,0,\,\tfrac14,\,\tfrac13,\,\tfrac25,\,\tfrac12,\,
\tfrac35,\,\tfrac23,\,\tfrac34,\,1,\,2\right\}.
$$
The entire positive catalogue predicted by the pair test is therefore
$$
\boxed{\quad \mathcal S(a,b)=\{a+(b-a)t:\ t\in\mathcal T\}\cap(0,\infty).\quad}
$$
Pairs with $\Delta j=0$ cannot charge the store. A zero or negative candidate energy slope contributes no line. A negative coefficient $t$, however, can give a positive energy slope and must be retained until the final positivity test. The listed fractions of $t$ count distinct positions only. Each has an actual three-carrier witness, and the joint transposition establishes attainability independently of how many strings witness that position.

## 3. Sharp inverse, including orientation and offsets

The table has the symmetry $t\mapsto1-t$. Equivalently, interchange $A,D$ in each string while preserving both middle labels, then reverse the order of the two reflected strings in each oriented pair. Reflection sends $(j,d)$ to $(6-j,3-j+d)$. Reversing the pair restores its original positive occupation difference $k$ and sends $\Delta d$ to $k-\Delta d$. This is a bijection of the possible pairs. Hence $\mathcal S(a,b)=\mathcal S(b,a)$, including any removal of nonpositive slopes. The preparation probabilities of reflected strings can differ. Every string in both descriptions still has positive probability, and a feasibility tag needs only one witness. Reflection here compares possible assignments of the physical gaps to the same registered occupations. It need not preserve the preparation weights or the gain amplitude of a particular control.

Write $u=\min(a,b)$, $v=\max(a,b)$. If $u=v$, every candidate slope is $u>0$. Conversely the coefficients 0 and 1 always give both positive gap values, so a genuine singleton forces equality. For $u<v$, symmetry permits evaluation as $u+(v-u)t$, strictly increasing in $t$. The two largest coefficients in the complete table are $2$ and $1$. Both resulting positions are positive. Therefore
$$
 L=2v-u,\qquad S=v,\qquad (u,v)=(2S-L,S).
$$
Every coefficient in $[0,1]$ gives a positive line, and the only remaining candidate at the low end is $2u-v$. It is included precisely for $v<2u$. At $v=2u$ it is zero, and at $v>2u$ it is negative. Thus a consistent unequal-gap record has eleven distinct positive lines if $v<2u$, and ten if $v\ge2u$. Different coefficients coincide only in the equal-gap case.

**Decision for any proposed complete catalogue.**

1. Read the list as a set of distinct positions in a common unit. Repeated evidence at one spacing supplies one position. Reject a purported positive line with a nonfinite or nonpositive value. An empty catalogue is impossible.
2. For a singleton $\{\ell\}$ with $\ell>0$, return the sole ordered pair $(\ell,\ell)$.
3. Otherwise take the two largest distinct positions $L>S>0$ and put $u=2S-L,\ v=S$. Reject if $u\le0$, including $L=2S$. Generate $\mathcal S(u,v)$ using the displayed eleven coefficients and the strict positivity rule. Require exact set equality with $\mathcal C$. A missing predicted line or an extra reported line rejects the complete catalogue.
4. On equality, return both $(a,b)=(u,v)$ and $(v,u)$. For each orientation the complete family of masses is
$$
(M_0,M_1,M_2)=\bigl(m,\ m+a/c^2,\ m+(a+b)/c^2\bigr),\qquad m>0,
$$
with $a,b$ in energy units. Multiply values quoted in units of $W$ by $W$ first.

Necessity follows from the two extrema and the slope table. For sufficiency choose any returned orientation and any $m>0$, use the stipulated full-support preparation, and at each predicted spacing use its witnessing joint transposition. At every other positive spacing, pointwise conservation precludes every gain transition. Identity is feasible there and attains zero. This constructs the entire catalogue, including all absence tags. Shifting the three masses together adds the same constant to every three-carrier energy, so the offset is unobservable. The total mass difference $M_2-M_0=(u+v)/c^2$ is identifiable with either orientation. The two largest lines reconstruct the unordered gaps for a known valid catalogue. They cannot certify that the remainder of an arbitrary proposed catalogue is consistent.

## 4. One diagnostic at an already identified line

For unequal gaps, take the certified second-largest spacing $w=v$. Restrict a separate, registered setting to the single joint exchange
$$
(BAA,6)\ \longleftrightarrow\ (AAA,7)
$$
and identity on all other joint states. This selects the $1\to0$ transition of the first labelled carrier, with the other two in $A$. The endpoint counts are $1+6=0+7$. Their carrier rest-energy difference is exactly $a$. The exchange is admissible if and only if $a=v$.

The extra observation must certify whether this **named** exchange is feasible at that spacing. One ideal realization of the observation law supplies a predeclared, pair-selective setting that effects the complete swap when allowed and acts as identity when forbidden. It includes registered carrier labels and slots, verified exclusion of other transitions, an independent linear store calibration at $v$, the same rest-energy ledger, fresh level 6 and complete terminal readout. A certificate that the named endpoint was reached may use direct input/output registration or separately validated selectivity and the final store level. The setting is fixed before preparation. The reverse state is present in the full permutation. No controller chooses a branch after looking at a history or supplies missing energy off resonance.

On resonance, for each full native history $H$, $P(s'=7\mid H)=4\cdot5\cdot5/14^3=100/2744$ and $P(s'=6\mid H)=2644/2744$. The other levels have probability zero. Off resonance the restricted setting gives $P(s'=6\mid H)=1$. Multiply each conditional probability by $P(H)=\prod_{i=1}^3(q_{t_i}/4)$, with $q_E=2/3,\ q_F=1/3$. This retains the two bits per carrier, both ideals, every supported history and the original forbidden native paths. A positive tag gives $(a,b)=(v,u)$. Certified absence of the named tag gives $(u,v)$. Both orientations already have an unlabelled positive line at $v$. A single no-gain trial cannot certify absence, even at a perfect readout. A physical negative result would also require validated control efficacy, registration, sensitivity and failure accounting. Equal gaps need no diagnostic.

## 5. A partial list and the physical scale

With only positive detections $\mathcal P$ and no absence information, the test weakens to $\mathcal P\subseteq\mathcal S(a,b)$. For example, in units of $W$, the partial record $\{2,3\}$ fits gaps $\{1,2\}$. Its full catalogue in those units is
$$
\{1,\ 5/4,\ 4/3,\ 7/5,\ 3/2,\ 8/5,\ 5/3,\ 7/4,\ 2,\ 3\}.
$$
The true top two lines are 3 and 2, and the low outer candidate is zero. The identical partial record also fits gaps $\{2,3\}$ because the gaps themselves are lines. Its largest line is 4. These possibilities have different unordered gaps and different total mass differences. Independent certification that two lines are the extrema would supply additional information absent from these detections.

A finite number of point probes of arbitrary real spacings cannot in general establish the full catalogue. Even for equal gaps, choose a positive common gap different from every tested spacing. All probed tags are negative, while the untested singleton can be at any of the remaining values. This also applies along an adaptive protocol's finite all-negative sequence. An exact full list or an independent reason for its completeness is an input to the inverse. Finite resolution, unknown line width, missed returns or uncertain absence require their own observation law.

Restoring physical units to the inferred mass differences uses the independent spacing standard and $c^2$. A stable carrier registration, a common rest frame and reproducible sharp preparation are physical inputs. Neither a duration nor a frequency is a line coordinate here. Count positions alone give no absolute mass, native energy unit, work-gain calibration or physical Hamiltonian. The energy of a gain trial comes from the changed carrier rest energies. Preparation, apparatus, acquisition and restoration costs would enter any repeated-use claim.

The forward pair criterion is derived in [full joint-store reversibility](joint_reversible_occupation_store.md). [Registered sector mass ratios](sector_inertial_mass_ratios.md) use a separate mechanical scale.

## Scientific provenance

- Energy author SHA-256 79d7160244c9db5b5f515655606035affafa4bc1fd7b90e06c41097522cb057c.
- Independent State review SHA-256 295b42628ebfcfd6e85d4ae6cf3f9da26fd2007b05620eff23b6efcfe85a74e6.
