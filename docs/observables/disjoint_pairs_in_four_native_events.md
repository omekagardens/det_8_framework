# Disjoint comparable pairs in the native four-event record

On this native four-birth law, if one pair is causally comparable, the other disjoint pair is less likely to be comparable. For every admitted source mixture, the negative covariance rules out four independent, identically distributed event draws from one fixed causal geometry and sampling measure. It also rules out conditionally independent and identically distributed draws given a geometry and sampling measure shared within each trial.

Use the empty-prepared active residual law, exactly four births, its original fair reference marks, all actual ideals, all histories and the actual source state $\rho(x)=(x,1-x)$, $0\le x\le1$. There is no prepared chain prefix. The source coefficient is an actual mixture coordinate, not a prior over unknown coefficients. The only new readout is the supplied independent uniform perfect matching of the four terminal vertices, with a fair ordering of the two pairs. Both sides receive the same complete order access, pair reader, matching randomness, information, registration and cost contract.

This is a finite population-law calculation and a necessary-model test. It supplies no physical detector, independently verified preparation, repeated-trial model, statistical error bound, metric calibration, curvature measurement, efficiency result or execution permission.

## A birth-name-independent pair statistic

For a realized strict four-vertex order $E$, let
$$
 m(E)=\#\{\{u,v\}:u,v\text{ comparable in }E\},
$$
counting all comparable pairs, including transitive relations, rather than only covers. Let
$$
 t(E)=\#\{\text{perfect matchings of the four vertices whose two pairs
 are both comparable}\}.
$$
There are three unordered perfect matchings, so $0\le t\le3$. Both $m$ and $t$ are invariants of the unlabelled order; neither uses birth ranks, terminal marks or a retained root.

Write $Y_1,Y_2$ for the comparable/incomparable bits of the fairly ordered matching. Conditional on $E$,
$$
 \Pr(Y_1=1\mid E)=\Pr(Y_2=1\mid E)=m(E)/6,\qquad
 \Pr(Y_1=Y_2=1\mid E)=t(E)/3.                    \tag{1}
$$
Each of the six unordered vertex pairs occurs in exactly one matching and has probability $1/2$ of being first, proving the marginal formula. The second formula counts the successful matchings. Thus
$$
 p(x)=\mathbb E_x[m]/6,\qquad d(x)=\mathbb E_x[t]/3. \tag{2}
$$
The matching is sampled independently of the native trial. It neither selects terminal shapes nor removes any history.

For checking $t$ during the last birth, let $P$ be the three-vertex parent and $S$ the actual ideal below the newborn $z$. Every matching pairs $z$ with one old vertex $v$. It succeeds exactly when $v\in S$ and the other two old vertices are comparable. Consequently
$$
 m(P+S)=m(P)+|S|,\quad
 t(P+S)=\sum_{v\in S}{\bf1}\{P\setminus\{v\}\text{ is a comparable pair}\}.
                                                               \tag{3}
$$
This formula uses actual ideal occurrences and is invariant under their transported names.

## Complete reference aggregation

Let $w_h=2^{-4}\prod q$ be the original fair-mark complete-history reference mass. Its total is one. The accepted three-birth reference shapes and their total probabilities, already summed over natural histories and fair marks, are
$$
 W_A=1/6,\quad W_E=1/5,\quad W_F=1/12,\quad
 W_J=11/30,\quad W_C=11/60.                       \tag{4}
$$
Here $A$ is the antichain, $E$ an edge plus isolate, $F$ a fork with one lower root, $J$ a join with two lower roots, and $C$ the chain. These probabilities sum to one.

For an explicit multiplicity check, the structural products for one natural occurrence are respectively $1/6,1/15,f_i/3,11/30,h_i/3$, where
$$
 f_0=1/6,\ f_1=1/3,\quad h_0=19/30,\ h_1=7/15.
$$
There are three edge-plus-isolate natural occurrences; the other four shapes have the single occurrence factors already specified in the accepted structural calculation. Summing the fair marks gives (4), with $\bar f=1/4$, $\bar h=11/20$. These are natural-history sums, not uniform weights on unlabelled shapes. There is no additional $4!$, automorphism divisor or permutation multiplier.

The last-birth conditional ideal probabilities below are sufficient to reproduce every entry. Put $e=1/44$. Role names only describe each unmarked parent; equal-role ideals are retained separately.

| Parent | Actual ideal slots, with their probabilities after the correct conditional mark average |
|---|---|
| $A$ | empty: $e$; each of 3 singletons: $1/110$; each of 3 pairs: $1/20$; full: $4/5$ |
| $E$, $u<v$, isolate $w$ | empty: $e$; $w$: $e$; $u$: $5/176$; $uv$: $1/16$; $uw$: $1/8$; full: $65/88$ |
| $F$, root $u<v,w$ | empty: $e$; $u$: $e$; each of $uv,uw$: $1/20$; full: $47/55$ |
| $J$, roots $u,v<w$ | empty: $e$; each of $u,v$: $e$; $uv$: $e$; full: $10/11$ |
| $C$, $u<v<w$ | empty: $e$; $u$: $e$; $uv$: $e$; full: $41/44$ |

Every row sums to one, with every actual ideal included. The newborn's two fair bits sum to one. The conditional mark average matters: for $E$, the edge-root mark is fair, so its $f,h$ averages give $5/176$ and $1/16$. For $F$, the probability of the parent already contains $f_i$; its root mark has conditional probabilities $f_i/(f_0+f_1)$, not $1/2$. Therefore
$$
 \mathbb E[h_i/f_i\mid F]=(h_0+h_1)/(f_0+f_1)=11/5,
$$
and each root-plus-leaf slot has probability $e(11/5)=1/20$. This retains rather than discards the mark/geometry dependence. Other mark dependence has either summed out or is absent from the displayed slot.

Using (3) gives the following check on the two required moments:

| Parent | Reference probability | $\mathbb E[m(P+S)\mid P\text{ shape}]$ | $\mathbb E[t(P+S)\mid P\text{ shape}]$ |
|---|---:|---:|---:|
| $A$ | $1/6$ | $30/11$ | $0$ |
| $E$ | $1/5$ | $641/176$ | $39/44$ |
| $F$ | $1/12$ | $1053/220$ | $199/110$ |
| $J$ | $11/30$ | $53/11$ | $21/11$ |
| $C$ | $11/60$ | $129/22$ | $63/22$ |
| Total moment | $1$ | $5839/1320$ | $205/132$ |

For example, in $E$, $t=1$ just for $w,uw,$ and full, whose probabilities sum to $39/44$. In $F$, each root-plus-leaf slot contributes one and full contributes two. In $J$, $t$ counts selected roots. In $C$, all three old pairs are comparable, so $t=|S|$.

A second, entirely unlabelled aggregation of the same complete reference mass is:

| $(m,t)$ | Reference probability |
|---|---:|
| $(0,0)$ | $1/264$ |
| $(1,0)$ | $1/110$ |
| $(2,0)$ | $9/220$ |
| $(2,1)$ | $1/220$ |
| $(3,0)$ | $401/2640$ |
| $(3,1)$ | $1/24$ |
| $(4,1)$ | $141/880$ |
| $(4,2)$ | $1/120$ |
| $(5,2)$ | $1079/2640$ |
| $(6,3)$ | $41/240$ |

These ten disjoint invariant blocks partition the full reference probability; a block may contain more than one order-isomorphism class. Their probabilities sum to one, the antichain block has the required mass $a=1/264$, and their weighted $m,t$ sums reproduce the preceding table. Exact rational sums were checked using existing arithmetic tools, without simulation or software development.

Thus the reference pair probabilities are
$$
 P:=p_{\rm ref}=5839/7920,\qquad
 D:=d_{\rm ref}=205/396=4100/7920.                \tag{5}
$$

## Apply the complete active law to every source mixture

The accepted complete-history identity is
$$
 L_i(h)=w_h[1+(-1)^i\theta(Z(E_h)-a)],\quad
 \theta=1/32,\ a=1/264,
$$
where $Z$ indicates a terminal antichain. Linearity in the actual state gives
$$
 L_x(h)=w_h[1+(2x-1)\theta(Z(E_h)-a)].
$$
Every non-antichain history has the common multiplier
$$
 k(x)=1-\frac{2x-1}{8448}
     =\frac{8449-2x}{8448},\qquad
 8447/8448\le k(x)\le8449/8448.                 \tag{6}
$$
The antichain has multiplier $1+(2x-1)\theta(1-a)$, keeping its full positive mass. Since $m=t=0$ on it, both moments in (2) are simply multiplied by $k$. Nothing is conditioned away. Explicitly,
$$
 \boxed{p(x)=\frac{5839(8449-2x)}{66908160},\qquad
 d(x)=\frac{4100(8449-2x)}{66908160}.}           \tag{7}
$$
The complete exchangeable two-bit law is
$$
 \Pr(11)=k\,4100/7920,\qquad
 \Pr(10)=\Pr(01)=k\,1739/7920,\qquad
 \Pr(00)=1-k\,421/440.                         \tag{8}
$$
All entries are positive throughout the source interval and sum to one. This table retains both failed-comparability outcomes and the all-incomparable outcome.

Write $C(x)=d(x)-p(x)^2$. Equations (5)–(7) give the exact factorization
$$
 \boxed{C(x)=\frac{k(x)}{62726400}
               [32472000-34093921\,k(x)].}     \tag{9}
$$
Its sign is strictly negative for every $0\le x\le1$, because
$$
 32472000-34093921\,\frac{8447}{8448}
       =-\frac{13667894687}{8448}<0.
$$
The positive factor $k$ never vanishes on this interval. Therefore the zero set there is empty. In fact (9) decreases as $k$ increases on the allowed interval: the derivative numerator is $32472000-68187842k<0$. Since $k$ decreases with $x$, the covariance increases with $x$ but remains negative:

| Actual state | $k$ | Exact covariance $C$ |
|---|---:|---:|
| pure $\delta_1$, $x=0$ | $8449/8448$ | $-116056161287521/4476701874585600$ |
| equal mixture, $x=1/2$ | $1$ | $-1621921/62726400$ |
| pure $\delta_0$, $x=1$ | $8447/8448$ | $-115452706421089/4476701874585600$ |

Consequently the shortfall below the independent-pair joint probability is at least
$$
 p(x)^2-d(x)\ \ge\
 \frac{115452706421089}{4476701874585600}>0.    \tag{10}
$$
There is no source-mixture setting that passes either covariance sign test.

## Fixed causal geometry and iid event sampling

Let $G$ denote one fixed causal geometry together with its sampling measure and fixed reader parameters. Under the supplied comparison premise, four locations $X_1,\ldots,X_4$ are iid conditional on $G$, and a pair is read by the same deterministic symmetric function of its two locations, or by that reader with independent per-pair measurement noise.

For any fixed matching, the two pair readers use disjoint independent location variables and independent noise. Their common comparable probability is a number $q_G$. Hence
$$
 \Pr(Y_1=Y_2=1\mid G,\text{matching})=q_G^2.
$$
All matchings have the same conditional two-bit law, by iid sampling. Averaging an independent uniform matching and its fair pair order preserves that law:
$$
 p=q_G,\qquad d=q_G^2,\qquad d-p^2=0.          \tag{11}
$$
This does not assume flatness, constant density or a particular dimension. Curvature and nonuniform density may change $q_G$, but cannot alter the disjoint-sample factorization.

The strictly negative (9) rules out this fixed-geometry iid interpretation of the specified native matched record for each pure source and every admitted mixture. It tests the sampling premise itself, rather than retuning the previously excluded flat four-point benchmark or fitting a curvature to one mean. Agreement of a single comparability fraction with a continuum formula cannot repair the failed joint law.

## Trial-random common geometry: weaker test also fails

Now allow $G$, including its sampling measure, to vary across trials, while retaining conditional iid locations within each trial and the same pair-reader contract. No independence between different trials is needed for the population identity. Conditional on $G$, (11) holds, so
$$
 p=\mathbb E[q_G],\quad d=\mathbb E[q_G^2],\quad
 \boxed{d-p^2=\operatorname{Var}(q_G)\ge0.}     \tag{12}
$$
This is weaker than demanding a single fixed $G$. It still fails for every native source coefficient: representing (9) by (12) would require a negative between-trial variance. No nonnegative amount of geometry variability supplies these two bits under the stipulated conditional iid model.

At the two-bit level only, zero covariance is sufficient for independence because the common binary marginals and $d$ determine all four cells. Nonnegative covariance also permits an abstract mixture of iid Bernoulli pairs: for any valid exchangeable binary law with $p^2\le d\le p$ and $p>0$, a latent probability equal to $d/p$ with probability $p^2/d$, and zero otherwise, has the required first two moments (with the degenerate boundary treated directly). Neither statement constructs a spacetime or satisfies the remaining four-event order constraints. The native negative covariance fails even this weaker abstract latent-probability condition.

If one relaxes conditional iid pair independence while retaining equal conditional marginals $q_G$, the total-covariance identity becomes
$$
 C(x)=\mathbb E[c_G]+\operatorname{Var}(q_G),\qquad
 c_G=\operatorname{Cov}(Y_1,Y_2\mid G).
$$
Thus any such representation must have
$$
 \mathbb E[c_G]=C(x)-\operatorname{Var}(q_G)\le C(x)<0.
$$
The required average negative conditional covariance has magnitude at least the exact shortfall in (10); adding common-geometry variability only increases that requirement. This diagnoses what conditional independence fails to provide, without selecting a replacement mechanism.

## Conditioning, source labels and identifiability

Conditional on a realized finite order, a uniform matching need not give independent bits. The exact decomposition is
$$
 C(x)=\mathbb E_x[t(E)/3-(m(E)/6)^2]
          +\operatorname{Var}_x(m(E)/6).       \tag{13}
$$
The first term can be negative because the matching partitions one finite order. Under iid locations on fixed $G$, the unconditional ensemble sum in (13) must nevertheless be zero by (11). It is the negative unconditional value (9), not an assertion of conditional independence given a realized order, that excludes that ensemble. Random partitions and independent new event samples are distinct conditionings.

For source-conditioned comparisons use $x=1$ for $\delta_0$ and $x=0$ for $\delta_1$; both fail. A separately certified mixed preparation with fixed actual coefficient $x$ has (7)–(9) and fails. If a justified trial population instead selects these two pure sources with frequencies $x,1-x$ and the recorded source is ignored, its marginal law is the same convex mixture. Algebraically,
$$
 C(x)=x C(1)+(1-x)C(0)
           +x(1-x)[p(1)-p(0)]^2.
$$
The nonnegative between-source term is already included; it does not change the sign. This identity is not a prior over uncertain $x$ and is not a repetition guarantee. If source settings are retained, apply the test within each setting. A source-dependent fixed geometry or geometry distribution remains covered by the corresponding source-conditioned iid necessity.

The unlabelled matched record determines these invariants and their law but does not identify the cause of the dependence. It does not distinguish underlying generation mechanisms or certify a unique physical matter/geometry coupling. The failed class specifically assumes disjoint iid sampling conditional on a common trial geometry/measure and independently acting pair readers. Pair-selected four-event gates, sampling without replacement from finite atoms, correlated readout noise or a different preparation change that class; they are not repaired or classified here. In particular no prepared-chain substitution is permitted.

The calculation uses the [four-birth structural probabilities](../track_b/native_mark_law_geometry_v1.md), the [active source law](../track_b/native_active_residual_v1.md) and the [complete-trial source weights](native_complete_trial_readout.md). The earlier [pair-comparability reader](order_comparability_and_curvature.md) motivates testing the sampling assumption. The [flat four-point comparison](four_birth_flat_interval_comparison.md) used a different observable.
