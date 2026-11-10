# Regional composition of the finite interval action

For two finite order patches joined at one common endpoint, the action of the join is determined by the regional actions and two endpoint counts from each side. The counts can be collected separately. Their contribution to the action involves products across the junction. Even arbitrary additive corrections based on each entire patch fail on four joins made from native-supported chain and diamond probes.

## Which intervals change

Use the supplied dimensionless convention $S(X)=|X|-2n_0(X)+4n_1(X)-2n_2(X)$, where $n_k$ counts comparable endpoint pairs with exactly $k$ elements strictly between them. Each pair counts once regardless of the number of paths connecting its endpoints. This is the open-interval notation for the published two-dimensional action. Counting contributions by putting the two endpoints in specified regions also appears in the bi-action literature. The result below specializes the counting to one shared vertex. [Benincasa, Dowker and Schmitzer, eq. (1.1)](https://arxiv.org/pdf/1011.5191v2) · [Dowker, Liu and Lloyd-Jones, §2.2, eqs. (4)–(6)](https://arxiv.org/pdf/2501.00139v1)

Identify the greatest event of $P$ with the least event of $Q$, call it $r$, and take transitive closure. Write $J=P\cup_r Q$. Define
$$
 a_i=\#\{x<_P r: |(x,r)_P|=i\},\qquad
 b_j=\#\{y>_Q r: |(r,y)_Q|=j\}.
$$
Thus $a_0$ counts immediate predecessors of $r$; $a_1$ counts earlier endpoints with exactly one intervening event. The future counts have the corresponding forward meanings.

Every interval with both endpoints in one patch has the same interior after gluing, including intervals ending or starting at $r$. Every new pair is uniquely $x<r<y$, and its open interval is the disjoint union $(x,r)_P\sqcup\{r\}\sqcup(r,y)_Q$. A pair of types $i,j$ therefore contributes at size $i+1+j$. There are no new links, $a_0b_0$ new one-interior pairs, and $a_1b_0+a_0b_1$ new two-interior pairs. Larger intervals have zero coefficient. The common vertex was counted twice in the two regional cardinalities. Together these give the exact defect
$$
 \boxed{D(P,Q):=S(J)-S(P)-S(Q)
       =-1+4a_0b_0-2a_1b_0-2a_0b_1.}
$$
For a singleton on either side this reduces to $-1$, as it must: the join then equals the other patch.

## Four supported probe choices rule out independent additive corrections

The four-chain $C$ has $(n_0,n_1,n_2)=(3,2,1)$, $S(C)=4$, and endpoint profile $(1,1)$ for layers zero and one. The four-diamond $D$ has $(4,0,1)$, $S(D)=-6$, and profile $(2,0)$. Both are self-dual, so the same profile applies at the appropriate end on either side. Both structural rows have positive native support, with marks permitting the same mark at the registered junction in all four comparisons. [Accepted four-event support and action table](finite_interval_action_and_source_preparation.md)

| Past | Future | New one-interior pairs | New two-interior pairs | Defect $D(P,Q)$ | Joined action |
|---|---|---:|---:|---:|---:|
| Chain | Chain | 1 | 2 | −1 | 7 |
| Chain | Diamond | 2 | 2 | 3 | 1 |
| Diamond | Chain | 2 | 2 | 3 | 1 |
| Diamond | Diamond | 4 | 0 | 15 | 3 |

If the defect were $F(P,r)+G(Q,r)+k$, its diagonal sum minus its off-diagonal sum on this table would vanish, even for arbitrary functions of each complete marked patch. The actual contrast is $(-1)+15-3-3=8$. Holding the junction mark fixed prevents it from supplying any information about the partner. Changing the convention for subtracting the single shared vertex by a constant also leaves this contrast unchanged.

## What the two probe actions identify

Suppose the same past patch, or identically prepared copies with the same past counts, can be paired with each labelled future probe. The record supplies the exact joined actions, the known $S(P)$, and the probe actions. Set $Y_Q=S(P\cup_r Q)-S(P)-S(Q)+1$. Substitution gives
$$
 Y_C=2a_0-2a_1,\qquad Y_D=8a_0-4a_1.
$$
The coefficient determinant is $8$, so
$$
 \boxed{a_0=(Y_D-2Y_C)/4,\qquad a_1=a_0-Y_C/2.}
$$
These equalities include degenerate profiles with a vanishing count. A negative or nonintegral inferred count rules out an exact record under the stipulated preparation. Unmatched population averages would require their own preparation assumptions to support a trial-level inference.

**Observational equivalence.** Conditional on the same known regional action and compatible junction mark, two past patches give identical joined actions against both probes if and only if their $(a_0,a_1)$ agree. In that case their joined actions agree against *every* compatible future patch in this gluing rule. Necessity uses the two-probe inverse; sufficiency follows directly from the defect. If the regional action itself is part of the record, the full signature is $(S(P),a_0,a_1)$ within each fixed compatibility class. This characterizes information independently of labels or how the two integers are encoded.

Higher endpoint counts need not be recoverable. As a purely finite-order check, compare a five-chain with the five-element order having two incomparable minima below a common three-element chain. Each has $(n_0,n_1,n_2)=(4,3,2)$, action $5$, and $(a_0,a_1)=(1,1)$ at its top. Their $a_2$ are one and two, respectively. Every future-probe action agrees. On a restricted candidate list, extra facts can of course be inferred from membership in that list.

## Registration and physical scope

These counts concern strict interval interiors. With greatest $r$, each earlier vertex has exactly one more strict descendant than the number in its interval to $r$. An exact descendant-count histogram on $P$ therefore gives $a_0,a_1$ through its bins for one and two descendants. On $Q$ the analogous statement uses strict *predecessor* counts. Computing a histogram on a known order and physically reading it from a register are distinct premises. The published handle-bound register result supplies a particular four-event access contract. [Terminal count access](terminal_counts_and_field_placement.md)

The theorem is conditional finite combinatorics. The native source establishes individual support for the four-event patches. The seven-event join and the five-element equivalence example are formal orders here. No joint preparation law, native composite history, transition probability, change in growth weights or physical gluing operation has been derived. The action coefficients were supplied. A physical gravitational action interpretation would additionally require a correspondence for the regions and their junction, a spacetime sampling and boundary prescription, and a dimensional action normalization. The finite mixed difference by itself measures none of these. [Stopped-horizon weighting](interval_action_and_stopping_horizon.md) · [Induced-order readout](stopped_and_induced_interval_actions.md)
