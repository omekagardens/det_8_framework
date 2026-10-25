# Statistical information in complete marked endpoints

RI1484 — Conditional finite-experiment theorem

This extension uses the exact assumptions and equal-fibre result of [What complete records identify](native_record_identifiability_v1.md), and the hypothetical sampling contract of [Finite records and rare reachable contexts](native_finite_record_access_v1.md). It preserves the fixed finite growth law and positive intrinsic family.

## Object and reconstruction channel

Fix the same q, finite horizon N, support and intrinsic positive scalar-kernel family as RI1479/RI1481. Let H be the finite set of distinct complete naturally labelled marked history encodings, and E the set of complete unlabelled marked endpoint classes. Let pi:H->E forget birth labels while retaining every mark and completed order comparison.

For e in E define F_e={h:pi(h)=e} and t_e=|F_e|>0. These are sets of distinct encodings, not vertex permutations counted with automorphism multiplicities. Fixed support makes them parameter-independent.

For parameter p, write P_p(h) for its history law and Q_p(e) for its endpoint law. The admitted marked diamonds, equivariance and suffix transport imply the RI1479 equal-fibre identity
\[
 P_p(h)=Q_p(e)/t_e\quad(h\in F_e).
 \tag{1}
\]
No equality for mark-erased fibres is assumed.

Define the mathematical random channel
\[
 U(e,h)=\mathbf1_{\{\pi(h)=e\}}/t_e,
 \qquad D(h,e)=\mathbf1_{\{\pi(h)=e\}}.
 \tag{2}
\]
Each row sums to one. U is independent of p. Its definition is uniform over distinct encodings; no enumeration algorithm or execution is supplied.

## Two-way simulation

For each h, only e=pi(h) contributes, so
\[
 (Q_pU)(h)=Q_p(\pi(h))/t_{\pi(h)}=P_p(h).
\]
Conversely,
\[
 (P_pD)(e)=\sum_{h\in F_e}P_p(h)=Q_p(e).
 \tag{3}
\]
Thus the history and marked-endpoint experiments simulate one another exactly, using the same channels for every admitted p.

Moreover UD is the identity on endpoints. DU is generally not the identity on individual histories: it replaces a history by a uniform draw from its fibre, while preserving each admitted law P_p. Choosing one plausible encoding deterministically fails to reproduce the history law whenever a positive-probability fibre has more than one member; other members then receive zero reconstructed mass despite (1).

Under the explicitly hypothetical premise of m independent same-law records, independent channel randomization gives
\[
 Q_p^{\otimes m}U^{\otimes m}=P_p^{\otimes m},
 \qquad P_p^{\otimes m}D^{\otimes m}=Q_p^{\otimes m}.
 \tag{4}
\]
This proves equivalence of the finite statistical experiments, not availability of independent physical resets.

## What transfers

For any randomized history-based decision kernel A(h,B), where B is a measurable action set, define the endpoint rule by first drawing h using U and then applying A. Equations (3)-(4) give exactly the same distribution of actions for each p, for one or m observations. Conversely an endpoint rule can be applied after D. Hence attainable testing errors, estimation risks for bounded parameter/action losses, and abstention probabilities coincide when randomization is allowed. No deterministic-only or equal-computational-cost assertion follows.

For any pair p,p', equality of total variation is also direct:
\[
 \tfrac12\sum_h|P_p(h)-P_{p'}(h)|
 =\tfrac12\sum_e t_e
       |Q_p(e)/t_e-Q_{p'}(e)/t_e|
 =\operatorname{TV}(Q_p,Q_{p'}).
 \tag{5}
\]
The same argument holds for product fibres at m observations.

RI1481's rare-context obstruction therefore persists unchanged for complete marked endpoints. Its conditional single-context procedure can also be transferred as a randomized endpoint decision rule, with the same additional reachability, separation and hypothetical repetition premises and the same risk bounds. A hit count in the synthesized history is not a recovered count along the actual unobserved chronology.

## Boundary

U produces a statistically correct synthetic encoding conditional on the endpoint. It does not recover which birth sequence actually occurred. Losses referring to that hidden actual sequence, interventions on it, or physical acquisition costs are not parameter/action losses covered above.

The theorem requires the complete marked endpoint and equal-fibre law. Missing marks, incomplete comparisons, changing support or abandoning the admitted invariance need separate arguments. It derives no physical sampling protocol, efficient enumeration, quantum/gravity dynamics or Boundary interpretation. Scientific, custody, ABSTAIN, Status M, zero qualification and RET-only pause gates persist.
