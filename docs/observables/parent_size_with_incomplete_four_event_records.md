# A parent-size test with incomplete four-event records

**Decision.** Arbitrary retention requires bounding the missed contribution on the original all-start denominator. If $c$ is the complete-record fraction and $h_{\rm obs}$ its conditional mean, the sharp upper all-start means are
$$
 U_A=ch_{\rm obs}+(1-c)702,\qquad
 U_B=ch_{\rm obs}+(1-c)(702-612q_{\rm miss}).
$$
The original witness remains conclusive exactly when the relevant upper completion is strictly negative. Both missing-record envelopes are attained by actual four-orders. The registered one-pair rescue can substantially improve the completeness requirement, without measuring a whole missed order or supplying a timing law.

## 1. Observation contract

Every start is assumed to possess one definite four-vertex induced order, obtained by uniformly sampling four distinct vertices conditional on its finite parent $N\ge4$. All six edges are consistent. Parent size and order may vary across trials. Let $R=1$ mean that the complete order is retained and $R=0$ that it is missed. Its probability $c=\Pr(R=1)$ is known exactly. Retention may depend arbitrarily on parent, marks, route and order; no ignorability or event-independent erasure premise is imposed.

When $c>0$, $h_{\rm obs}=\mathbb E[H\mid R=1]$ is the exact conditional complete-case mean. In measurement A, only the missed-start count is added. In B, every missed order also yields one comparable/incomparable bit from a uniformly selected unordered pair, after that order exists. Conditional on the missed order, the auxiliary pair selection is independent of its edge values. For $c<1$, $q_{\rm miss}=\Pr(Y=1\mid R=0)$ is the exact success probability of that registered reader.

A failed or timed-out acquisition does not itself establish a completed four-order. That order's existence is a supplied model premise here, not an invented trajectory for an unverified preparation. All starts, including missing complete records and zero rescue bits, stay in the denominator.

## 2. The accepted witness and what survives selection

For a four-order, let $m\in\{0,\ldots,6\}$ count all comparable unordered pairs, including transitive relations, and let $t$ count perfect matchings whose two pairs are comparable. The accepted witness is
$$
                 H(m,t)=21m^2-333m+210t+702.   \tag{1}
$$
Its established properties on the original uniform-sampling population are
$$
 H\ge-108,\qquad
 \mathbb E[H\mid\text{parent}]\ge0
      \quad\text{for each parent with }N\ge9.  \tag{2}
$$
In particular, with $\eta=\Pr(4\le N\le8)$ under the original trial weighting,
$$
                         \mathbb E H\ge-108\eta. \tag{3}
$$
These parent constraints are not transferred to the selected complete-case distribution. The all-start decomposition is
$$
 \mathbb E H=ch_{\rm obs}+(1-c)h_{\rm miss},
 \qquad h_{\rm miss}=\mathbb E[H\mid R=0],       \tag{4}
$$
whenever both conditional statistics are defined. No assumption sets $h_{\rm miss}=h_{\rm obs}$.

The six possible edges split into three disjoint perfect matchings. Every successful matching uses two different present edges, so $2t\le m$. Equation (1) gives the useful pointwise upper line
$$
 \begin{aligned}
 H-(702-102m)
   &=21m^2-231m+210t\\
   &\le21m(m-6)\le0.
 \end{aligned}                                \tag{5}
$$
Thus
$$
                         H\le702-102m\le702.   \tag{6}
$$
No order enumeration is needed. An antichain has $m=t=0,\ H=702$. A four-chain has $m=6,t=3,\ H=90$. Both are genuine supported four-orders.

## 3. Measurement A: missed starts counted, no rescued edge

For $0<c<1$, (6) gives
$$
 \boxed{\sup\mathbb E H
       =U_A=ch_{\rm obs}+702(1-c).}             \tag{7}
$$
The supremum is a maximum: take every missed order to be an antichain, leaving the observed complete-order distribution unchanged. This completion respects the existence of actual orders and all-start weighting.

Consequently the summary forces a negative all-start witness exactly when
$$
                         U_A<0.
$$
For $h_{\rm obs}<0$, equivalently,
$$
 c>\frac{702}{702-h_{\rm obs}},\qquad
 1-c<\frac{-h_{\rm obs}}{702-h_{\rm obs}}.       \tag{8}
$$
The inequalities are strict. If $h_{\rm obs}\ge0$, then $U_A\ge0$ throughout the domain, so this summary cannot force a negative witness. At equality $U_A=0$, strictly negative completion is not forced.

This is a sharp statement about the information in this summary and the existing witness. If $U_A\ge0$, a compatible actual-order completion has nonnegative mean; it does not follow that a population of large parents exists.

## 4. Measurement B: one uniformly selected pair on each missed order

The registered rescue satisfies
$$
 \Pr(Y=1\mid\text{order},R=0)=m/6,
 \qquad \mathbb E[m\mid R=0]=6q_{\rm miss}.     \tag{9}
$$
It supplies no identities of the other five pairs, no matching of extra edges, and no complete hidden order. Averaging the pointwise line in (6) gives
$$
 h_{\rm miss}\le b(q_{\rm miss}),\qquad
                  b(q)=702-612q.              \tag{10}
$$
For every $q\in[0,1]$, this bound is attained by a missed-order mixture with antichain weight $1-q$ and chain weight $q$. Their uniform pair bits are always zero and always one respectively, so the mixture has exactly the registered success probability $q$ and mean $702-612q$.

Thus the sharp upper completion is
$$
 \boxed{\sup\mathbb E H
       =U_B=ch_{\rm obs}+(1-c)b(q_{\rm miss}),}  \tag{11}
$$
again attained by actual four-orders. Since $90\le b(q)\le702$, it is never legitimate to replace the missing witness by zero merely because a pair was rescued.

The summary forces a negative all-start mean exactly when $U_B<0$. For $h_{\rm obs}<0$,
$$
 c>\frac{b(q_{\rm miss})}{b(q_{\rm miss})-h_{\rm obs}},
 \qquad
 1-c<\frac{-h_{\rm obs}}{b(q_{\rm miss})-h_{\rm obs}}. \tag{12}
$$
Equivalently, for fixed $0<c<1$, the required rescued-pair probability is
$$
 q_{\rm miss}>
 \frac{702+c h_{\rm obs}/(1-c)}{612},
 \qquad 0\le q_{\rm miss}\le1.                 \tag{13}
$$
If the right side is negative all allowed $q$ suffice; if it is at least one none suffice. At zero, a strictly positive $q$ is required. At $q=0$, B reduces to A; at every $q>0$ and nonzero missed fraction, its upper completion is strictly smaller.

The best possible rescue summary has $q=1$, leaving penalty 90 per missed start. It cannot make the witness conclusive at or below the corresponding completeness threshold. For $h_{\rm obs}\ge0$, $U_B$ is nonnegative as well.

One may view B's observed score as $H$ on complete cases and $702-612Y$ on missed cases. Its population mean is $U_B$ and is an upper bound on $\mathbb E H$. The bound is in conditional expectation over the uniform rescue pair; $702-612Y$ is not a pointwise upper bound for each individual hidden order after one random pair. No realized finite ledger is assigned a sampling-error guarantee here.

## 5. Attainability, admissible summaries and endpoints

The admissible conditional mean range is $h_{\rm obs}\in[-108,702]$. Both endpoints are achieved by actual orders: a root below three incomparable leaves gives $H=-108$, and an antichain gives 702. Mixing them realizes every intermediate mean when only that mean is specified. Every $q_{\rm miss}\in[0,1]$ is realized by the antichain/chain mixture above.

For sharpness, keep any actual complete-order distribution consistent with the reported observations, including the exact native conditional distribution when specialized below. Give it total trial weight $c$. Give the chosen missed-order completion weight $1-c$, with the retention flag selecting those two routes. Take every parent to have $N=4$; uniform sampling then returns its entire order. This gives a legitimate underlying all-start parent/order/retention law and attains (7) or (11), without assuming the selection is independent.

This construction is a mathematical observation-law completion, not a proposed native holding-time or growth mechanism. It proves the envelope cannot be tightened from these summaries alone. It does not construct a population with all $N\ge9$.

Conditional statistics are used only where defined:

| Completeness | A | B |
|---|---|---|
| $0<c<1$ | (7), with $h_{\rm obs}$ defined | (11), with both $h_{\rm obs},q_{\rm miss}$ defined |
| $c=1$ | Exact all-start mean $h_{\rm obs}$ | Same; no missed population and no $q_{\rm miss}$ is required |
| $c=0$ | Upper completion 702; no $h_{\rm obs}$ exists | Upper completion $b(q_{\rm miss})\ge90$; no $h_{\rm obs}$ exists |

The all-start witness cannot be forced negative at $c=0$ by either summary. At $c=1$ it is conclusive precisely when the known complete mean is negative. Statistics of an empty conditional population are not assigned artificial values.

## 6. Small-parent fraction on the original denominator

For either registered measurement, let $U$ denote its sharp upper completion. Combining (3) with $\mathbb E H\le U$ gives the valid original-population bound
$$
                 \boxed{\eta\ge\max(0,-U/108).} \tag{14}
$$
For $U<0$, this excludes all parents being at least nine and certifies a positive trial fraction with four to eight vertices. At $U=0$ or $U>0$, this argument gives no positive lower fraction. Under feasible summaries $U\ge-108$, so the bound never exceeds one.

No sharpness of (14) as a parent-fraction optimum is claimed. The sharpness proved above is that of the all-start mean upper completion over actual four-orders. A nonnegative witness, even from an attaining completion, is not sufficient for a consistent larger-parent order model, overlapping-edge moments, or the full induced order law. This distinction is inherited from the accepted parent-geometry diagnostic.

## 7. Completeness thresholds for a native conditional complete record

Only now specialize the conditional complete records to the accepted native distribution. Its mean is
$$
 h_{\rm obs}(x)=-g(x),\qquad
 g(x)=\frac{1492565-62122x}{371712}>0,
 \quad 0\le x\le1.                             \tag{15}
$$
This assigns no native distribution to the missed records and does not assert that the all-start distribution has this mean.

The exact required completeness and tolerated missed fraction are:

| Measurement | Strict completeness requirement | Strict missed-fraction bound |
|---|---|---|
| A | $c>702/(702+g(x))$ | $1-c<g(x)/(702+g(x))$ |
| B at registered $q$ | $c>b(q)/(b(q)+g(x))$ | $1-c<g(x)/(b(q)+g(x))$ |
| Best B summary $q=1$ | $c>90/(90+g(x))$ | $1-c<g(x)/(90+g(x))$ |

For a guarantee uniform over the entire source interval, replace $g(x)$ by its minimum $g_{\min}=1430443/371712$. In particular:

| Uniform all-source guarantee | Strict completeness | Strict missed fraction |
|---|---|---|
| A | $c>260941824/262372267$ | $1-c<1430443/262372267$ |
| B with $q=1$ | $c>33454080/34884523$ | $1-c<1430443/34884523$ |

The two missed fractions are approximately $0.545\%$ and $4.10\%$; the exact strict fractions govern the decision. If $x=1/2$, then $g=173/44$, and the corresponding thresholds are $c>30888/31061$ for A and $c>3960/4133$ for B with $q=1$.

A finite feasible improvement example is
$$
 c=49/50,\qquad h_{\rm obs}=-173/44,\qquad q_{\rm miss}=1.
$$
Measurement A permits
$$
 U_A=\frac{22411}{2200}>0,
$$
whereas the rescue yields
$$
 U_B=-\frac{4517}{2200}<0,\qquad
              \eta\ge\frac{4517}{237600}>0.    \tag{16}
$$
At this completeness, (13) requires $q_{\rm miss}>22411/26928$, so $q=1$ suffices. The example is attained with conditional complete orders exactly at the native equal-source law and missed orders all chains, using the $N=4$ construction of section 5. With no rescue statistic the same complete record is also compatible with all missed orders antichains, giving the positive upper completion. Thus B genuinely improves this witness decision.

The exact population premise $q_{\rm miss}=1$ is not a certificate manufactured from one successful rescue or from a finite set of successes. A finite experiment would require its own uncertainty analysis and independent registration.

## 8. Timing, readout, resource and unit limits

The result allows arbitrary selection on hidden route and order. It therefore does not identify a deadline/visibility mechanism, establish a holding-time distribution, transport two-birth mark rates to four events or derive a physical clock. A proposed physical application must establish that every start has the stipulated four-order, that the complete-record flag is counted correctly, and that missed trials are not silently removed or retried to success.

B additionally requires one qualified comparability bit on every otherwise missed order, with a uniformly chosen unordered pair independent of its six edge values. Rescue availability cannot itself select an unregistered subset of missed starts. Pair failures or unresolved relations cannot be recoded as incomparability without a justified channel. The comparable-pair reader and all-start sampling must be registered the same way for the native and parent hypotheses. Complete-case probabilities alone cannot calibrate those promises.

A rescue needs random selection, access to the missed trial, relation recovery, bookkeeping and any reset or repeated-access resources. It is a smaller stipulated observation than a complete missed order, but no cost or efficiency advantage is proved. Both comparisons receive the same retained records, rescue information, preparation/selection knowledge, processing and costs; all start-to-record costs remain in the ledger.

The quantities $H,c,q,\eta,x$ and the completeness thresholds are dimensionless. The statement bounds a fraction of trials with small finite parents at the admitted event scale. It supplies no proper volume, length, spacetime dimension, calibrated duration, mass or gravity coupling. Exact population inequalities are not observed finite-frequency confidence bounds.

[Complete-order parent bound](variable_parent_size_from_four_native_events.md) · [Complete-trial readout](native_complete_trial_readout.md) · [Four-event comparison law](disjoint_pairs_in_four_native_events.md)
