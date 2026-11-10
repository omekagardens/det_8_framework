# What two elapsed-time gates reveal about a marked waiting law

Two gates recover both dimensionless rates, up to exchanging the mark names, **if the waiting time is exponential conditional on the first mark**. A clock independent of the entire growth route can reproduce the same five probabilities at both gates and the same untagged timing law throughout this single interval. For unequal conditional rates, one additional first-gate probability for a terminal pair of zero marks distinguishes these two descriptions and assigns the rates to the marks within the exponential family.

## Eight native histories and the five observed cells

Use the accepted CL013/v1 actual-ideal law at $\lambda=1,\ t=1/2$. The first birth from empty is certain. Write $b$ for its immutable mark and $c$ for the second mark. Each newborn bit is fair on every allowed branch. The empty ideal of the singleton produces the antichain $A$ with probability $2/3$. Its full ideal produces the chain $C$ with probability $1/3$. The following are all-start probabilities, with each ordered pair of marks counted once in each shape.

| Native route | $bc=00$ | $bc=01$ | $bc=10$ | $bc=11$ |
| --- | ---: | ---: | ---: | ---: |
| $A$, empty ideal | $1/6$ | $1/6$ | $1/6$ | $1/6$ |
| $C$, full ideal | $1/12$ | $1/12$ | $1/12$ | $1/12$ |

The row totals are $2/3$ and $1/3$. Let $E$ denote the mixed-mark antichain. At either fixed first mark, $P(E\mid b)=(2/3)(1/2)=1/3$. Its complement includes both equal-mark antichains and every chain.

Start elapsed time at the first birth. The new assumption is $W\mid b\sim\mathrm{Exp}(r_b)$ with $0<r_b<\infty$, independent of the second branch given $b$. For the common gate scale $\tau>0$ write $x_b=\exp(-r_b\tau)$. Each native route in column $bc$ contributes its table entry multiplied by its respective factor
$$
1-x_b,\qquad x_b-x_b^2,\qquad x_b^2
$$
for $W\in(0,\tau]$, $W\in(\tau,2\tau]$, and $W>2\tau$. These factors sum to one on each route. With
$$
m=(x_0+x_1)/2,\qquad v=(x_0^2+x_1^2)/2,
$$
the three all-start bin totals are $1-m,\ m-v,\ v$. Conditional branch independence and the common $1/3$ chance of $E$ at each $b$ split each completed bin in the proportions $1/3,2/3$. Thus in the order $E_1,\bar E_1,E_2,\bar E_2,\mathrm{censored}$ the full record is
$$
\left(\frac{1-m}{3},\frac{2(1-m)}{3},\frac{m-v}{3},\frac{2(m-v)}{3},v\right).
$$
The last cell pools every late route with no mark or order output. The five cells sum to one.

## Exact compatibility and recovery

Given five finite real inputs $(e_1,n_1,e_2,n_2,h)$, require nonnegativity, unit sum, and $n_i=2e_i$ for each completed bin. Put $D_i=e_i+n_i$, $m=1-D_1=D_2+h$ and $v=h$. The remaining necessary and sufficient conditions for the primary family are
$$
0<m<1,\qquad 0\le v-m^2<\min\{m,1-m\}^2 .
$$
Indeed $v-m^2=(x_0-x_1)^2/4$. The candidate survivals are precisely the roots of $X^2-2mX+2m^2-v=0$, namely $x_-=m-d,\ x_+=m+d$ for $d=\sqrt{v-m^2}$. The lower bound keeps the roots real and admits their equality. The strict upper bound is exactly $x_->0,\ x_+<1$. Equality at that upper bound yields a zero survival (infinite-rate limit), a unit survival (zero rate), or both at $m=1/2$. Beyond it at least one root is outside the probability interval. The endpoint means $0,1$ are also excluded. These checks apply even to normalized records with the correct structural split. Conversely the displayed conditions give two admitted roots whose moments reproduce $m,v$, hence all five cells.

All allowed ordered pairs $(r_0\tau,r_1\tau)$ are the assignments of $-\log x_-$ and $-\log x_+$ to the two marks. For $d=0$ there is just the common value $-\log m$. For $d>0$ the five cells identify the fast-to-slow rate ratio $(-\log x_-)/(-\log x_+)$, with two assignments of the faster rate. In particular, a single positive finite exponential rate fits exactly on the primary boundary $v=m^2$, subject to the cell and mean checks.

For an exact one-gate collision, take $(x_0,x_1)=(1/4,3/4)$ or $(1/2,1/2)$. Both yield $(1/6,1/3,1/2)$ for early $E$, early complement and all late trials. At $2\tau$ the censoring probabilities are $5/16$ and $1/4$ respectively. More generally the matched single exponential with survival $m$ at $\tau$ predicts censoring $m^2$, whereas the split-rate model predicts $m^2+d^2$.

## A clock independent of the entire native route

A proper, almost surely positive finite $W$ independent of the route gives $P(E,W\in B)=P(W\in B)/3$ for each completed bin $B$. For arbitrary inputs the exact conditions for this description are nonnegativity, unit sum, and $n_i=2e_i$. They allow empty bins, including zero censoring or complete censoring. To realize any such record, allocate clock mass $D_1,D_2,h$ to one finite point in each of $(0,\tau],(\tau,2\tau],(2\tau,\infty)$, independently of the route. This same construction permits a non-exponential clock even at a record admitting equal exponential rates. A failed bin split rules out both descriptions on the stipulated growth law. When only the primary moment or rate-domain checks fail, the independent description still fits a valid split record.

For every primary pair there is also a common continuous independent clock for this *same one holding interval*. Draw a separate fair bit, independent of both marks and the ideal, and use its value to pick between $r_0,r_1$. Its survival at elapsed $s\ge0$ is
$$
S(s)=\tfrac12(e^{-r_0s}+e^{-r_1s}).
$$
It is proper, positive and finite almost surely. For unequal rates it is non-exponential because $S(2\tau)-S(\tau)^2=d^2>0$. Under the primary construction $P(E,W>s)=\sum_b(1/2)(1/3)e^{-r_bs}=S(s)/3$. Its complement has joint survival $2S(s)/3$. The independent construction gives exactly these same functions by factorization. Differences of survivals therefore agree on any observation subinterval, including the two declared bins. This is an identity of the untagged population laws for the one waiting time. At equal rates the continuous construction is itself exponential. Equality at *every* time then fixes that exponential marginal, although the two fixed gates still admit a non-exponential independent alternative as above.

## One terminal mark flag

Let $z=P(W\le\tau,\ b=c=0)$, pooling the two shapes. The all-start flag is zero on every late trial. On early trials its positive cases lie in the complement of $E$, and the terminal pair needs no chronological label. Its native mass is $1/6+1/12=1/4$. The following are joint tests with the five cells.

| Description | Required five-cell conditions | All admissible values of $z$ |
| --- | --- | --- |
| Primary, exponential given first mark | Cell, mean and moment conditions above | $\{(1-m-d)/4,\ (1-m+d)/4\}$ |
| Arbitrary clock independent of the whole route | Nonnegative normalized cells, $n_i=2e_i$ | $\{D_1/4\}=\{(1-m)/4\}$ |

For the first row every both-zero route has first mark zero, so $z=(1-x_0)/4$. Each listed value is realized by the corresponding root assignment. For the second row the complete-route independence multiplies $1/4$ by $D_1$, and the independent bin construction attains it. Thus either row's conditions are sufficient even when testing the supplemental flag.

For an admissible primary main record with $d>0$, the two primary values differ from the independent prediction by $\pm d/4$. The larger flag assigns the faster rate to mark zero. Specifically, $x_0=1-4z,\ x_1=2m-x_0$. These give the named $r_b\tau=-\log x_b$ and their named ratio $r_0/r_1=\log x_0/\log x_1$. The midpoint supports only the independent description of the two. Any other value outside the three predictions fits neither. At $d=0$ the two descriptions share the sole flag value $D_1/4$ and both marks have the same primary rate. For a valid split record outside the primary moment and rate domain, the independent row still requires its exact flag value. For the one-gate example with unequal rates and the displayed assignment, the flag is $3/16$. Exchanging mark assignments gives $1/16$, and the independent clock gives $1/8$.

## What survives exchange of incomparable births

The two mixed antichain paths $01$ and $10$ lead to the same terminal marked order. The native law assigns each total weight $1/6$, preserving the integrated scalar diamond. Their two elapsed-bin masses and unobserved late contributions, prior to pooling, are
$$
\frac16(1-x_0,\ x_0(1-x_0),\ x_0^2),\qquad
\frac16(1-x_1,\ x_1(1-x_1),\ x_1^2).
$$
For unequal rates the first-bin entries differ, as do the late entries. The second-bin difference is $(x_0-x_1)(1-x_0-x_1)/6$. It can vanish at $x_0+x_1=1$ even for distinct rates. Integrating each vector gives $1/6$. A timing law conditioned solely on the final marked order gives the same conditional dwell to these two routes. It therefore cannot implement the displayed routewise joint law at unequal rates. It can pool the two waits to give the correct endpoint marginal. At equal rates the common exponential implements both orderings exactly.

The flag can reject independence from the **entire route** under the fixed structural law. Its assignment of a rate specifically to the first mark uses the stipulated exponential family and conditional branch independence. The finite record does not determine general conditional holding-time distributions or select the underlying cause of an observed correlation. The gate probabilities supply dimensionless products $r_b\tau$ and rate ratios within the primary model. Converting a product to an inverse-second rate requires $\tau$ in calibrated seconds. The native weights and birth count provide no elapsed-time scale. The result concerns one supplied interval, exact population probabilities and synthetic dynamics. Detector access, sampling precision and physical calibration are outside the premises.

The mixture comparison and the two-zero terminal flag were specified when the model was designed.

## Applying a time gate to a four-event geometry record

The complete-trial geometry construction uses the empty-prepared **active residual** law, exactly four births, all actual ideals, original fair reference marks, and every natural history and continuation. At actual normalized source $\rho(x)=(x,1-x)$, the history measure is $L_x(H)=w_H[1+(2x-1)(Z_H-1/264)/32]$, where $Z_H$ is the terminal four-event antichain flag. Source settings and complete trials share the registered detector. The disjoint-pairs construction then uses an independent uniform perfect matching on the *four* vertices, retains both comparison bits, and obtains negative population covariance for every admitted $x$. Its two zero **pair-comparability bits** are different observations from the donor’s two zero **birth marks**.

To see the missing link, suppose a proposed timing gate accepts completed history $H$ with probability $a_x(H)$. Even before any change to the pair reader, a selected-only population would have weights $L_x(H)a_x(H)/\sum_{H'}L_x(H')a_x(H')$ when the denominator is positive. Whole-history independence at each registered source, together with unchanged independent matching and readout, would preserve the conditional history distribution. CL095 establishes no such independence for four births, no extension of the one holding interval through completion, and no acceptance probabilities $a_x$. Even a gate constant across histories within each source can change pooled source proportions when its acceptance fraction varies between settings. The source coefficient describes an actual normalized preparation; uncertainty about it supplies no averaging prior. Neither a successful split nor $K=0$ certifies unbiased timing selection.

Keep all assigned attempts, incomplete acquisitions and erasures visible. A missing order cannot certify incomparability; the existing erasure row requires independent justification. To apply the donor diagnostic would require independent registration of its start, two-birth marginal and eight route weights, mark and order tags, censoring, the same two gate times, and a readout reaching the stated all-start probabilities without altering the native law. The QR four-birth access assumptions do not provide this prefix instrumentation or a clock. The original endpoint and covariance claims remain statements about their complete population. No finite-sample false-positive rate, elapsed-time selection license or generic causal interpretation follows.

[Complete-trial source response](native_complete_trial_readout.md) · [Comparability in a four-event geometry record](disjoint_pairs_in_four_native_events.md)
