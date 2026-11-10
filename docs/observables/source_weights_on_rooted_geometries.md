# Can a geometric action weight reproduce a prepared source response?

On four events, two source preparations give different probabilities for rooted orders with the same bulk interval action. Including the change in action on removing the root distinguishes every observed geometry. The exact likelihood ratios can then be tabulated, but they fail the proposed two-coefficient exponential model.

## Rooted observation and the insertion statistic

Both preparations begin with the registered prefix $a<b$, marks $(i,0)$, $i=0,1$, and use the same unchanged fair-mark/all-ideal law through birth four. The two further births are $x,y$. Every structural row has four suffix-bit continuations of equal conditional weight; none is discarded.

The observed outcome $g$ is the isomorphism class of the unmarked terminal order with **root $a$ retained**. The prefix partner $b$, suffix marks and birth ranks are not tagged in this record. The value $i$ labels the preparation, not an extra output coordinate that would make the two rooted-geometry supports disjoint.

Use the prescribed dimensionless action and induced deletion:
$$
 S(C)=|C|-2n_0(C)+4n_1(C)-2n_2(C),\qquad
 I_a(C)=S(C)-S(C\setminus\{a\}).
$$
The root is minimal, although it need not be the unique minimum. For any two other endpoints, $a$ cannot lie strictly between them, so deleting $a$ changes none of their open intervals. Only the root itself and comparable pairs starting at $a$ disappear. If
$$
 r_j(a)=\#\{v>a: |(a,v)|=j\},\quad j=0,1,2,
$$
then
$$
 \boxed{I_a=1-2r_0(a)+4r_1(a)-2r_2(a).}                 \tag{1}
$$
Incomparable vertices contribute no root pair. The deletion is induced-order deletion, not removal of an arbitrary term without checking other interval interiors. Both $S$ and $I_a$ are rooted-isomorphism invariants.

## Complete rooted aggregation with history multiplicities

Number the 15 structural rows in the order printed in the [published structural probability table](finite_interval_action_and_source_preparation.md#complete-finite-law). Each row already sums its four suffix marks. Aggregating rooted-isomorphic outcomes merges exactly
$$
 \{3,7\},\quad \{4,12\},\quad \{9,10,13\};
$$
the remaining rows are singletons. Swapping suffix names merges the first two pairs. For the three-row group, permutations of $b,x,y$ move the long versus short branch while fixing $a$; this is permitted because $b$ is untagged.

Here each representative lists only cover relations, with transitive closure understood; an omitted fourth vertex is isolated. Root $a$ remains fixed throughout. $W_i=1320P_i(g)$.

| Outcome | Structural rows | Representative cover relations | $(r_0,r_1,r_2)$ | $(S,I_a)$ | $W_0$ | $W_1$ | $P_1/P_0$ |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| $g_1$ | 1 | $a<b$, $x,y$ isolated | $(1,0,0)$ | $(2,-1)$ | 6 | 6 | 1 |
| $g_2$ | 2 | $a<b,\ x<y$ | $(1,0,0)$ | $(0,-1)$ | 6 | 6 | 1 |
| $g_3$ | 3,7 | $a<b,\ a<x$, $y$ isolated | $(2,0,0)$ | $(0,-3)$ | 10 | 20 | 2 |
| $g_4$ | 4,12 | $a<b,\ b<x$, $y$ isolated | $(1,1,0)$ | $(4,3)$ | 38 | 28 | $14/19$ |
| $g_5$ | 5 | $a<b,\ a<y,\ x<y$ | $(2,0,0)$ | $(-2,-3)$ | 33 | 33 | 1 |
| $g_6$ | 6 | $a<b,\ b<y,\ x<y$ | $(1,1,0)$ | $(2,3)$ | 195 | 195 | 1 |
| $g_7$ | 8 | $a<b,\ a<x,\ a<y$ | $(3,0,0)$ | $(-2,-5)$ | 5 | 10 | 2 |
| $g_8$ | 9,10,13 | $a<b,\ b<x,\ a<y$ | $(2,1,0)$ | $(2,1)$ | 57 | 42 | $14/19$ |
| $g_9$ | 11 | $a<b,\ a<x,\ b<y,\ x<y$ | $(2,0,1)$ | $(-6,-5)$ | 172 | 392 | $98/43$ |
| $g_{10}$ | 14 | $a<b,\ b<x,\ b<y$ | $(1,2,0)$ | $(6,7)$ | 19 | 14 | $14/19$ |
| $g_{11}$ | 15 | $a<b,\ b<x,\ x<y$ | $(1,1,1)$ | $(4,1)$ | 779 | 574 | $14/19$ |
| Total | all 15 | | | | 1320 | 1320 | |

For example $g_3$ has weights $5+5=10$ and $10+10=20$; $g_4$ has $19+19=38$ and $14+14=28$; $g_8$ has $3(19)=57$ and $3(14)=42$. These are sums of actual natural-history probabilities. No automorphism division, additional linear-extension factorial, uniform distribution over orders, or selected-history renormalization is inserted. Each original row's four conditional mark weights sum back to its tabulated row weight, accounting for all 60 marked continuations per preparation.

The representatives inside each declared group are root-isomorphic. Conversely all eleven displayed $(S,I_a)$ pairs are distinct, so no two listed groups can be root-isomorphic. This verifies that the aggregation is exhaustive and has no missing mergers. In particular, retaining the root matters; forgetting it would be a different observation problem.

## General criterion for positive feature reweighting

For a predeclared statistic $T(g)$, consider
$$
 Q_w(g)=\frac{P_0(g)w(T(g))}
                 {\sum_hP_0(h)w(T(h))},\qquad w>0.
$$
All eleven outcomes have positive probability in both laws. Such a model equals $P_1$ exactly if and only if $R(g)=P_1(g)/P_0(g)$ is constant on every observed $T$-fibre. Necessity follows because the normalizer is global. Conversely, set $w(t)$ to that constant ratio on each supported fibre; its $P_0$ expectation is $\sum_gP_1(g)=1$.

Equivalently, positive feature reweighting cannot change $P_0(g\mid T)$. This is a criterion for the full rooted law, not merely a fit to selected means.

## Bulk action alone fails; its marginal can nevertheless be matched

The two rooted outcomes $g_2,g_3$ have the same bulk action zero but different ratios,
$$
 R(g_2)=1,\qquad R(g_3)=2.
$$
Therefore **no** positive $w(S)$ reproduces the full rooted geometry law. This rules out arbitrary nonlinear bulk lookup weights, not only an exponential bulk coupling.

The coarse action marginals themselves have common positive support and can always be matched. Here their exact weights are:

| $s$ | $1320P_0(S=s)$ | $1320P_1(S=s)$ | $r_S(s)=P_1(S=s)/P_0(S=s)$ |
| --- | ---: | ---: | --- |
| −6 | 172 | 392 | $98/43$ |
| −2 | 38 | 43 | $43/38$ |
| 0 | 16 | 26 | $13/8$ |
| 2 | 258 | 243 | $81/86$ |
| 4 | 817 | 602 | $14/19$ |
| 6 | 19 | 14 | $14/19$ |

The unique normalized action-only reweighted distribution having those six totals is
$$
 \widetilde P_S(g)=P_0(g)r_S(S(g)).
$$
Its normalizer is already one. Apart from a common scaling of raw weights, no other $S$-only weights match all these totals. It reproduces the whole action marginal and all functions of $S$, including the previously computed action mean, while preserving the wrong rooted conditional laws.

An exact discrepancy is
$$
 \widetilde P_S(g_3\mid S=0)=P_0(g_3\mid S=0)=5/8,
 \qquad P_1(g_3\mid S=0)=10/13.
$$
The conditional gap is $15/104$. Unconditionally,
$$
 \widetilde P_S(g_3)=\frac{10}{1320}\frac{13}{8}
                  =\frac{13}{1056},\qquad
 P_1(g_3)=\frac{20}{1320}=\frac{16}{1056},
$$
so
$$
 \boxed{P_1(g_3)-\widetilde P_S(g_3)=1/352.}              \tag{2}
$$
This is a concrete error of the fully coarse-class-matched surrogate, with the same rooted observation and original multiplicities. It is not an empirical error bar or a claim of optimal approximation in any other divergence.

## Arbitrary positive bulk-plus-insertion weights succeed

On this support $T=(S,I_a)$ distinguishes all eleven rooted outcomes. The general criterion therefore passes. One explicit normalized construction is:

$$
 w(S,I_a)=
 \begin{cases}
 1,&(S,I_a)\in\{(2,-1),(0,-1),(-2,-3),(2,3)\},\\
 2,&(S,I_a)\in\{(0,-3),(-2,-5)\},\\
 14/19,&(S,I_a)\in\{(4,3),(2,1),(6,7),(4,1)\},\\
 98/43,&(S,I_a)=(-6,-5).
 \end{cases}                                           \tag{3}
$$
For these weights $P_0(g)w(S(g),I_a(g))=P_1(g)$ in every table row, and $\sum_gP_0w=1$. All weights are strictly positive. Their values on unsupported feature pairs may be set to any positive numbers without affecting the result. On the observed pairs the normalized ratios are fixed; a common multiplier of unnormalized weights is immaterial.

Thus the two statistics permit an exact positive terminal-distribution representation. In this finite rooted support their joint value is a lossless outcome label, so the freedom to use arbitrary weights is a lookup capability. It does not derive those weights from the action formula, establish a compact coupling law, or prove applicability beyond these preparations. It also does not reconstruct a dynamical reweighting of unseen histories or establish a physical source field.

## The two-parameter exponential still fails

Suppose, with real $\theta,\eta$ and normalization $Z>0$,
$$
 R(g)=Z^{-1}\exp[\theta S(g)+\eta I_a(g)].
$$
The pair $g_1,g_2$ has equal insertion $-1$, action difference $2$, and likelihood-ratio quotient $1$. Hence
$$
 R(g_1)/R(g_2)=e^{2\theta}=1,
$$
forcing $\theta=0$.

The pair $g_3,g_5$ has equal insertion $-3$, the same action difference $2$, but quotient $2$. It would require
$$
 R(g_3)/R(g_5)=e^{2\theta}=2.
$$
The two requirements contradict each other. Neither $\eta$ nor $Z$ can change this, as both cancel in the within-pair comparisons.

Equivalently the parameter-free log-contrast is
$$
 \log R(g_1)-\log R(g_2)-\log R(g_3)+\log R(g_5)
       =-\log2,
$$
whereas every proposed exponential gives zero. This exact finite discrepancy tests the specified family; there is no numerical fitting or selection of a new statistic. Arbitrary positive $w(S,I_a)$ succeeds while its two-parameter log-linear subfamily fails.

## Observation and physical interpretation

The record retains the actual root identity and the rooted unmarked order, not merely a counter multiset, a one-bit action probe or a mean. Those are different access contracts. The accepted one-bit protocol can determine an action mean under its stated operations, but it does not supply the rooted conditional probabilities used here. Full rooted-order readout and induced root deletion are supplied mathematical observations, not derived apparatus capabilities.

The two source-conditioned laws use one unchanged growth rule and original fair suffix marks. The calculations do not change the growth weights, release the mark postulate, select endpoint classes, erase unwanted trials or assume independence between the source and geometry. A rooted-isomorphism aggregation is a pushforward of actual history probabilities, not a new preparation.

The insertion statistic is computed from the prescribed interval action. No source mark is identified with energy, inertial or gravitating mass, and no exponential coefficient is a measured gravitational or thermal coupling. The public action convention supplies no probability law for the native histories by itself. Conversely, an exact positive lookup representation is not a derivation of gravitational dynamics, a continuum measure or a path integral.

[Discrete interval action convention, Eq. (1.1)](https://arxiv.org/pdf/1011.5191v2) · [Native source preparations](native_source_readout_response.md)
