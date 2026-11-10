# A finite interval action responds to the prepared source

**Decision.** Under the unchanged four-birth law, switching the prepared source bit from zero to one changes the mean dimensionless interval action from $93/44$ to $9/22$. Access to the complete terminal order determines that action on every trial. The original bit, the terminal vertex-count multiset, and even the fully readable vertex and common-descendant pair counters each lose information needed on some trials. The same supported pair of orders witnesses all three failures.

## Preparation and interval convention

Let $P_i$ be the continuation law conditional on the registered prefix $a\prec b$ with marks $(i,0)$ and consistent descendant counters $(1,0)$, $i=0,1$. Keep this prefix fixed in each preparation. The two births $x,y$ are maximal when born and each has all members of its chosen ideal as strict predecessors. Every later bit is fair. Each of the 15 structural sequences below has four marked continuations of equal conditional weight. No terminal-class selection, mark averaging of the prepared bit, or feedback from counters into the growth law enters the calculation. [Prepared source law](native_source_readout_response.md)

For $k=0,1,2$, let $n_k$ count endpoint pairs $u\prec v$ whose open interval contains exactly $k$ vertices. At this horizon the prescribed action is
$$
S=4-2n_0+4n_1-2n_2 .
$$
Thus $n_0$ counts links. A diamond contributes once to $n_2$ for its bottom-to-top interval, even though there are two paths between those endpoints. This is equation (1.1) with inclusive intervals of sizes 2, 3 and 4, in the specified dimensionless normalization. [Benincasa, Dowker & Schmitzer, arXiv:1011.5191v2, Eq. (1.1)](https://arxiv.org/pdf/1011.5191v2)

## Complete finite law

In the table, $I_x,I_y$ are the actual predecessor ideals. Concatenation denotes a set, so $ab=\{a,b\}$. Each terminal relation consists of $a\prec b$, the pairs $u\prec x$ for $u\in I_x$, and $u\prec y$ for $u\in I_y$. This specifies every open interval. The final columns give the structural probability numerators over 1320.

| $I_x$ | $I_y$ | $(n_0,n_1,n_2)$ | $S$ | $1320P_0$ | $1320P_1$ |
| --- | --- | --- | ---: | ---: | ---: |
| $\varnothing$ | $\varnothing$ | (1,0,0) | 2 | 6 | 6 |
| $\varnothing$ | $x$ | (2,0,0) | 0 | 6 | 6 |
| $\varnothing$ | $a$ | (2,0,0) | 0 | 5 | 10 |
| $\varnothing$ | $ab$ | (2,1,0) | 4 | 19 | 14 |
| $\varnothing$ | $ax$ | (3,0,0) | −2 | 33 | 33 |
| $\varnothing$ | $abx$ | (3,1,0) | 2 | 195 | 195 |
| $a$ | $\varnothing$ | (2,0,0) | 0 | 5 | 10 |
| $a$ | $a$ | (3,0,0) | −2 | 5 | 10 |
| $a$ | $ab$ | (3,1,0) | 2 | 19 | 14 |
| $a$ | $ax$ | (3,1,0) | 2 | 19 | 14 |
| $a$ | $abx$ | (4,0,1) | −6 | 172 | 392 |
| $ab$ | $\varnothing$ | (2,1,0) | 4 | 19 | 14 |
| $ab$ | $a$ | (3,1,0) | 2 | 19 | 14 |
| $ab$ | $ab$ | (3,2,0) | 6 | 19 | 14 |
| $ab$ | $abx$ | (3,2,1) | 4 | 779 | 574 |
| **Total** | | | | **1320** | **1320** |

The weights are products of the two native structural transition probabilities. For example the diamond row has incoming weights $1/6,1/3$ and conditional final weights $43/55,49/55$, respectively. This gives $172/1320,392/1320$. In *every* row a specified ordered pair of newborn marks has one quarter of the tabulated probability. This accounts for all 60 actual marked histories per preparation exactly once, including sequences with isomorphic endpoints.

Summing rows by action gives the two probability laws and the signed contrast. All entries below have denominator 1320.

| $S$ | −6 | −2 | 0 | 2 | 4 | 6 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| $1320P_0(S)$ | 172 | 38 | 16 | 258 | 817 | 19 |
| $1320P_1(S)$ | 392 | 43 | 26 | 243 | 602 | 14 |
| $1320(P_1-P_0)(S)$ | 220 | 5 | 10 | −15 | −215 | −5 |

The weighted action sums are $2790/1320=93/44$ and $540/1320=9/22$. The source-one minus source-zero mean difference is $-75/44$, and the total variation distance is $235/1320=47/264$. Each action value occurs under both preparations. The distribution distinguishes the preparations statistically; one action value cannot identify the source with certainty.

## What the observer can determine on a trial

Direct terminal order access suffices by enumerating the ordered comparable endpoints, counting their strict interiors and applying the action formula. To test the weaker interfaces, take the fourth and fifth table rows. Choose newborn marks $0,0$ in both. Each specified marked history has positive probability under either root preparation.

- **Fourth row.** The order is $a\prec b\prec y$ with $x$ isolated. Its action is $4$. The terminal strict-descendant counts in proof order $(a,b,x,y)$ are $(2,1,0,0)$. Only the pair $\{a,b\}$ has a common strict descendant, namely $y$, giving pair count 1.
- **Fifth row.** The order has exactly $a\prec b,\ a\prec y,\ x\prec y$. Its three links give action $-2$. The counts are $(2,0,1,0)$. Only the pair $\{a,x\}$ has a common strict descendant, again $y$, giving pair count 1.

Both give $Y=1$ for “some counter equals two” and the same count multiset $\{2,1,0,0\}$. On the jointly handle-bound vertex and pair register, swapping $b,x$ between the two outputs preserves **every** entry, fixes the prepared root $a$ and the last vertex $y$, and also matches the chosen marks. Handles permit addressing cells, but birth indices, separately retained prefix-role labels and histories are outside this terminal observation. Even granting access to all pair cells leaves the actions different on these indistinguishable records. The published pair-register bit alone supplies less information. [Vertex register](finite_incidence_register.md) · [Pair register](finite_pair_incidence_register.md)

The collision concerns exact determination on **every** trial. For example, the multiset $\{3,2,1,0\}$ already fixes $S=4$ on this support. Also, the $Y$ distribution itself responds to the source. These facts do not determine the action on a trial in the colliding class. Of the tested interfaces only a registered full-order readout supplies an exact action on all trials.

## Interpretation

The conditional native law supplies the weights and the orders. The interval coefficients are an external choice. Physical use would require an implemented observation of the necessary order information, a justified relation to spacetime sampling and volume or curvature, and a dimensional action scale. Neither the means nor their contrast establishes those calibrations. This calculation uses the prepared continuation weights above throughout; no alternative four-birth ensemble or reweighting enters the result.

## Scientific review

DET Quantum Relativity supplied the calculation. DET Relational State Research independently verified the interval counts, source laws and simultaneous vertex-and-pair counter collision. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `47e4a612877f951258871a535a03238638c012039051dde779d910a927688fcc`.
- Author report SHA-256: `cf9ed8131b2e70ced4556f1db88d4219ccc978858814489178270f5695867c92`.
- Author freeze SHA-256: `851889dd2cb865e5eb73387bc2ec53e22821ecd4943e3cbc923b5c9fc72fc1bb`.
- Independent scientific review SHA-256: `55f378c277587f832a95fdde5e0b7ded9400017e82a70abff8f1f85aade10b3f`.
