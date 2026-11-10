# Does interval-action weighting give one dynamics at three and four events?

**Decision.** Only $\lambda=0$ makes the three-event weighted law equal the three-event marginal of the four-event weighted law. For every nonzero finite real coupling, the proposed rule defines two valid fixed-size ensembles whose probabilities for the already recorded third birth disagree. Reject this prescription as a horizon-independent model of backreaction on the specified source-zero preparation. The interval action remains a well-defined observable under the original law.

## Preparation and necessary and sufficient test

Start at the registered $a\prec b$ prefix with marks $(0,0)$ and consistent counters $(1,0)$. Use the native laws $P_3,P_4$ conditional on that prefix, with all actual ideal choices and fair later marks. Denote a complete third-event history by $H$; it contains the predecessor ideal of $x$ and its mark. Write $K(y\mid H)$ for the native probability of a fourth-birth continuation, including its ideal and mark. For each prescribed terminal size form
$$
 S_n=n-2n_0+4n_1-2n_2,\qquad Q_n(H_n)=P_n(H_n)e^{-\lambda S_n(H_n)}/Z_n ,
$$
where $n_j$ counts comparable endpoint pairs with exactly $j$ intervening vertices. The real positive exponential weight is a candidate modelling choice. The action coefficients use the accepted dimensionless convention. Fixed-cardinality action ensembles provide context; the reference distribution here is exclusively the source-zero native law. [Action convention, equation (1.1)](https://arxiv.org/pdf/1011.5191v2) · [Fixed-size ensemble background](https://arxiv.org/abs/1110.6244v1) · [Prepared law](native_source_readout_response.md)

Define the conditional continuation factor
$$
 R(H)=\sum_y K(y\mid H)\exp[-\lambda(S_4(H,y)-S_3(H))].
$$
The four-event marginal at $H$ is $P_3(H)e^{-\lambda S_3(H)}R(H)/Z_4$. Since all supported prefixes have positive probability, marginal equality holds **if and only if** $R(H)$ is the same for every supported $H$. When constant it equals $Z_4/Z_3$ by summing over $H$. Normalizing each terminal ensemble separately does not enforce this condition.

## Exhausting the source-zero prefixes

There are three predecessor ideals for $x$: empty ($E$), $\{a\}$ ($F$), and $\{a,b\}$ ($C$). These produce an edge plus an isolate, a fork, and a three-chain. Their respective actions are $1,-1,3$. Grouping the published source-zero structural numerators by $\Delta S=S_4-S_3$ gives:

| Third prefix | $S_3$ | $\Delta S=-5$ | $-3$ | $-1$ | $+1$ | $+3$ | Row sum |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $E$ | 1 | 0 | 33 | 11 | 201 | 19 | 264 |
| $F$ | −1 | 172 | 0 | 5 | 5 | 38 | 220 |
| $C$ | 3 | 0 | 0 | 19 | 798 | 19 | 836 |

The structural row sums divided by 1320 are $1/5,1/6,19/30$. Divide a row's cells by its row sum to obtain the conditional increment law. Each of the 15 original structural rows splits into four equal marked histories for the two newborn bits. At size three each fixed newborn mark has half its structural mass. The source-zero continuation probabilities depend on neither newborn mark, and the action ignores them. Hence the table tests each of the six **marked** third-event histories; no isomorphic rows or mark assignments have been discarded. [Complete action and source table](finite_interval_action_and_source_preparation.md) · [Original fair-mark convention, Part A](../track_b/native_mark_law_geometry_v1.md)

Set $t=e^{-2\lambda}>0$ and $T_i=e^\lambda R(i)$. The extra factor is common to all three prefixes. The table gives
$$
 T_E=\frac{33/t^2+11/t+201+19t}{264},\qquad
 T_F=\frac{172/t^3+5/t+5+38t}{220},\qquad
 T_C=\frac{1/t+42+t}{44}.
$$
Clearing positive denominators in the two required equalities gives
$$
\begin{aligned}
264t^2(T_E-T_C)&=(t-1)(13t^2-38t-33),\\
220t^3(T_F-T_C)&=(t-1)(33t^3-172t^2-172t-172).
\end{aligned}
$$
The quadratic has exactly one positive root: its roots have opposite signs, and its values at 0 and 4 are $-33$ and $23$. That root is below 4. Any positive root of the cubic must satisfy $33t^3=172(t^2+t+1)>172t^2$, hence $t>172/33>5$. There is no shared positive root of those factors. At $t=1$ both equalities hold, giving precisely $\lambda=0$, for which $Q_n=P_n$.

## An observable recorded before the fourth birth

Retain the third predecessor ideal as a categorical record. For example, compare the odds of $E$ against $C$. The direct three-event odds and the odds after marginalizing the four-event law are
$$
 O_3=\frac6{19}e^{2\lambda},\qquad
 O_{4\to3}=O_3\,\frac{T_E}{T_C}.
$$
These formulae also apply with either value of the third mark fixed. At zero coupling both odds equal $6/19$. Under the native table the conditional means of $\Delta S$ in rows $E,C$ are $37/66,1$. Differentiating the conditional exponential weights therefore gives
$$
 \log\frac{O_{4\to3}}{O_3}=\frac{29}{66}\lambda+O(\lambda^2).
$$
Equivalently the direct and projected log-odds slopes at zero are $2$ and $161/66$. This is a third-event structural diagnostic; a lone newborn bit stays fair in both ensembles. At one nonzero coupling the particular $E:C$ odds coincide accidentally. The $F:C$ odds in that same categorical record detect the discrepancy there, as the second polynomial proves.

## Which probabilities realize the four-event ensemble?

Let $W(H)=\sum_y K(y\mid H)e^{-\lambda S_4(H,y)}$. To generate the fixed-four law sequentially from the registered starting pair, choose the third history with probability $P_3(H)W(H)/Z_4$, then the fourth continuation with probability
$$
 K^{[4]}(y\mid H)=K(y\mid H)e^{-\lambda S_4(H,y)}/W(H).
$$
Their product is exactly $Q_4(H,y)$. This preserves the fair conditional mark splits. A design stopping at three instead chooses $H$ with probability $P_3(H)e^{-\lambda S_3(H)}/Z_3$. The prefix test above is exactly the condition for using that same third-birth transition in both designs. At nonzero coupling the choice of terminal size changes an earlier probability in the ensemble definition. It describes a difference between sampling rules, with no empirical claim that a future birth acts on the past. No native transition, gravitational coupling or physical action scale is derived from this test.
