# One native order law, distinct auxiliary seed mechanisms

Historical author status: manual theorem candidate; independent native adjudication pending.
Subsequent independent manual review and coordinator adjudication accepted the exact conditional scope; the separate publication note below records that distinction.
Public edition: 22 October 2026.
Scope: the accepted from-empty Bernoulli native law and an explicitly
constructed causal auxiliary representation. No new physical or native law.

## 1. Result and the state whose law is being identified

For each fixed \(p\in(0,1)\), the accepted independent-edge construction
and the maximal-selected-predecessor construction below have exactly the
same native transition kernels and all finite native history laws.
They can be coupled causally so that their completed orders and marks
agree at every finite size on every realization. Their complete native
unnormalized payload maps agree as well. Nevertheless, their conditional
auxiliary subset distributions differ, and the retained seed inclusion
indicators need not be independent.

Consequently the accepted intrinsic-order likelihood identifies the
parameter of the common native law, within that family, but cannot
establish elementary independence of the actual auxiliary seed indicators.
This is nonidentifiability of a redundant auxiliary description, not a
second native law or a physical countermodel.

The declared state is \((P,r,X)\): a finite completed order, immutable
binary marks, and an arbitrary complex PSD payload on a fixed carrier.
A native birth appends one maximal vertex with strict past an individual
ideal \(S\subseteq P\), and fair bit \(b\). The admitted branch map is
\[
\mathcal B^{P,r}_{S,b}(X)=\frac{\pi_p(P,S)}2 X. \tag{1}
\]
Every native ideal, including empty and full, must have positive probability;
the complete ideal row is normalized. Equivariance, the specified
proper-precursor restriction on **mark** dependence, and complete marked
incomparable-birth diamonds are also required. Whole-unmarked-parent
dependence is allowed. Auxiliary generating subsets are not components
of this declared state.

We retain these requirements and the accepted law without changing the
marks, payload, eligibility, or completed-order observation. The new choice
is only an auxiliary subset kernel. No requirement of positive probability
for every auxiliary subset is inserted into the native axioms.

## 2. Closure fibers and the finite pushforward condition

For a finite parent \(P\) of size \(n\), let
\(C_P(U)=\downarrow_P U\) for \(U\subseteq V(P)\). For an ideal \(S\),
let \(\operatorname{Max}(S)\) mean maxima of the induced ideal, not maxima
of the whole parent. Finiteness gives
\[
C_P(U)=S
\quad\Longleftrightarrow\quad
\operatorname{Max}(S)\subseteq U\subseteq S. \tag{2}
\]
For necessity, \(U\subseteq S\), and a maximal member of \(S\) can lie
below a selected member of \(S\) only by being selected itself. Conversely,
every member of the finite ideal lies below one of its maxima. The empty
fiber consists only of the empty subset.

The original auxiliary kernel is
\[
\lambda_p(P,U)=p^{|U|}(1-p)^{n-|U|}.
\]
Its closure pushforward is the accepted native law
\[
\pi_p(P,S)=
\sum_{\operatorname{Max}(S)\subseteq U\subseteq S}\lambda_p(P,U)
=p^{|\operatorname{Max}(S)|}(1-p)^{n-|S|}. \tag{3}
\]
The maxima must be included, the outside omitted, and other members of
\(S\) are summed freely. Closure fibers partition all subsets, so (3)
is normalized and strictly positive for every ideal. At the empty parent
its only ideal has probability one; its two marked branches have weight
one half.

More generally, for a nonnegative normalized conditional auxiliary subset
kernel \(\lambda(P,r,U)\), its native ideal kernel equals (3) **if and only if**
\[
\boxed{
\sum_{\operatorname{Max}(S)\subseteq U\subseteq S}
       \lambda(P,r,U)=\pi_p(P,S)
\quad\text{for every parent, marking, and ideal }S.} \tag{4}
\]
This is simply the finite pushforward under \(C_P\). It is equality of
individual native ideal probabilities, stronger than equality only after
forgetting the parent embedding or grouping isomorphic children.

With the same independent fair bit and native payload convention (1),
(4) also gives equality of the full native marked maps. The bit and
payload conventions are essential additional specifications: an arbitrary
subset mechanism coupled to different bit or payload dynamics is not
covered merely by matching scalar ideal probabilities. Here the kernels
are functions of the current parent, so matching them at every parent
gives matching native transition kernels, not merely a one-time marginal
match at a selected size.

## 3. Retain only maximal selected predecessors

For any selected subset \(U\), define
\[
M_P(U)=\operatorname{Max}(P[U]).
\]
Every element of \(U\) lies below a maximal element of \(U\), hence
\[
C_P(M_P(U))=C_P(U),\qquad
M_P(U)=\operatorname{Max}(C_P(U)). \tag{5}
\]
For the second equality, a maximal selected element cannot be dominated
by another element of its closure: such an element lies below a selected
element, contradicting maximality. Conversely a closure maximum must
itself be selected and maximal there. Empty subsets satisfy both identities.

Draw \(U\) by the original kernel and retain \(V=M_P(U)\) as the actual
auxiliary predecessor set. Equivalently, use the following direct finite
kernel:
\[
\boxed{
\lambda^{\max}_p(P,V)=
\begin{cases}
p^{|V|}(1-p)^{n-|C_P(V)|},&V\text{ is an antichain in }P,\\
0,&V\text{ is not an antichain}.
\end{cases}} \tag{6}
\]
The empty set counts as an antichain.

To derive (6), ideals and antichains of a finite order are in bijection
under \(S\mapsto\operatorname{Max}(S)\) and \(V\mapsto C_P(V)\).
Indeed maxima are an antichain, (5) shows that closing an antichain
recovers precisely those maxima, and closing the maxima of an ideal
recovers the ideal. Thus
\[
\Pr(M_P(U)=V)=
\Pr(C_P(U)=C_P(V))
=\pi_p(P,C_P(V))
\]
for antichains, with \(|\operatorname{Max}(C_P(V))|=|V|\).
Non-antichains are impossible maxima sets.

The bijection proves normalization of (6). In the closure fiber of an
ideal \(S\), the only antichain generator is \(\operatorname{Max}(S)\);
all other generators have zero probability under (6). Therefore
\[
\sum_{V:C_P(V)=S}\lambda^{\max}_p(P,V)
=\lambda^{\max}_p(P,\operatorname{Max}(S))
=\pi_p(P,S)>0. \tag{7}
\]
This proves (4) for every finite parent, not only for a typical order.

The construction uses the full unmarked parent but no old marks. It is
equivariant because closure and maxima commute with relabeling.
Most importantly, the entire native kernel is unchanged. Its complete
positivity, normalization, mark locality and marked diamond identities,
including full-first and equal-precursor cases, therefore remain the
accepted identities. They need not be reinterpreted as constraints on
unobserved redundant subset outcomes.

There is **not** full auxiliary-subset support in (6): any subset
containing two comparable vertices has zero probability. This does not
remove any native ideal or native branch. In particular the full native
ideal is still obtained from \(\operatorname{Max}(P)\), with probability
\(p^{|\operatorname{Max}(P)|}>0\). Requiring positive probability for every
auxiliary subset would be a stronger, additional representation-level
premise, under which this particular representation would fail. It is
not one of the declared native positivity requirements.

## 4. A causal coupling at every finite size

Use the accepted countable product of mutually independent
\(E_{ij}\sim\operatorname{Bernoulli}(p)\), \(i<j\), and independent fair
bits \(b_j\). Start both processes from the same empty order and payload.
Let \(U_n=\{i\le n:E_{i,n+1}=1\}\).

The original process appends vertex \(n+1\) with past \(C_{P_n}(U_n)\).
The second process, recursively using its own current parent \(P'_n\),
sets \(V_n=M_{P'_n}(U_n)\) and appends the same vertex with past
\(C_{P'_n}(V_n)\). Both append the same bit \(b_{n+1}\).

If \(P'_n=P_n\), (5) gives equality of the two new pasts, hence
\(P'_{n+1}=P_{n+1}\), with the same inherited and newborn marks.
The initial equality and induction prove
\[
(P'_n,r'_n)=(P_n,r_n)\quad\text{for all finite }n. \tag{8}
\]
This induction holds for every elementary edge/bit array, not just with
high probability or separately on a new probability space for each horizon.
There is no use of future vertices, future comparisons, or final size.
Removing nonmaximal *selections* at a birth deletes no native vertex or
native comparison.

Conditional on the entire previous elementary history, the fresh head
\(U_n\) has the original product distribution. The current parent is already
determined. Thus \(V_n\) has conditional distribution (6) at \(P'_n\).
Conditioning down to the native history preserves that parent-dependent
kernel. The second process is a valid causal realization of the stated
maximal-seed mechanism. Its retained seeds need not be independent within
or across births.

For each shared native history \(\gamma=(S_0,b_1;\ldots;S_{N-1},b_N)\),
the native probability and native composed payload map in both descriptions
are, respectively,
\[
w_p(\gamma)=2^{-N}\prod_{n=0}^{N-1}\pi_p(P_n,S_n),
\qquad X\longmapsto w_p(\gamma)X. \tag{9}
\]
The map identity holds for every complex PSD \(X\), including zero.
If the native payload is tracked by these coarse branch updates, it agrees
along the coupled history as well. Thus all finite marked native path laws
and complete native maps coincide; forgetting marks, labels or intermediate
states cannot distinguish the descriptions. This is stronger than equality
of the one-terminal-order likelihood alone.

There is an important distinction about hidden branch weights.
One could refine a native map into auxiliary maps
\(X\mapsto\lambda(P,U)X/2\) indexed by \(U,b\).
The analogous maximal-seed refined maps need **not** agree seed by seed,
nor need their hidden unnormalized outputs agree under (8).
Only their sums over a closure fiber agree:
\[
\sum_{U:C_P(U)=S}\frac{\lambda(P,U)}2 X
=\sum_{V:C_P(V)=S}\frac{\lambda^{\max}_p(P,V)}2 X
=\frac{\pi_p(P,S)}2X. \tag{10}
\]
The theorem does not promote these hidden refinement labels or weights to
native state components. Observing them would be a different observation
contract. The pathwise native assertion (8)–(9) concerns the declared
native state and maps, not equality of enlarged seed-record states.

Using independent coins to construct this coupling does not make the
retained seed indicators independent. Formula (6) also defines a direct
finite draw without recording \(U_n\). The existence of independent
sampling randomness is distinct from independence of the mechanism's
actual retained predecessor indicators.

## 5. A reachable conditional seed counterexample

Condition on the two-vertex parent \(a\prec b\). This parent occurs from
empty with probability \(p>0\), so it is not an inaccessible supplied
prefix. The fresh third-birth edge selections are still independent
Bernoulli variables conditional on that parent. On its two vertices:

| Auxiliary subset | Original \(U\) probability | Retained \(V=M_P(U)\) probability |
| --- | --- | --- |
| \(\varnothing\) | \((1-p)^2\) | \((1-p)^2\) |
| \(\{a\}\) | \(p(1-p)\) | \(p(1-p)\) |
| \(\{b\}\) | \(p(1-p)\) | \(p\) |
| \(\{a,b\}\) | \(p^2\) | \(0\) |

The two cases \(U=\{b\}\) and \(U=\{a,b\}\) have the same retained
maximum \(\{b\}\). Their weights add to \(p(1-p)+p^2=p\).
Consequently
\[
\Pr(a\in V\mid P)=p(1-p)>0,\quad
\Pr(b\in V\mid P)=p>0,\quad
\Pr(a,b\in V\mid P)=0. \tag{11}
\]
The product of the two marginals is \(p^2(1-p)>0\), so the retained
indicators are not independent, even allowing distinct Bernoulli marginals.

The only native ideals are
\(\varnothing,\{a\},\{a,b\}\), with identical probabilities in both mechanisms:
\[
(1-p)^2,\qquad p(1-p),\qquad p. \tag{12}
\]
All are positive and sum to one. In particular the zero auxiliary probability
of \(\{a,b\}\) does not make the full native ideal impossible: retained seed
\(\{b\}\) generates it. The marks and coarse payload maps are unchanged.

These are manual symbolic conditional probabilities, not numerical
evaluations or simulated samples. At an antichain parent \(M_P(U)=U\),
so the two seed distributions agree there; the reachable chain is precisely
where redundant comparable selections expose the difference.

## 6. What the accepted likelihood can and cannot identify

The accepted theorem gives, for known deterministic \(N\ge2\) and faithful
unmarked completed-order observation,
\[
\Pr_p([P_N]=[P])=
\frac{e(P)}{|\operatorname{Aut}(P)|}
p^{c(P)}(1-p)^{i(P)}, \tag{13}
\]
where \(c\) counts covers, \(i\) incomparable pairs and \(e\) linear
extensions. Equations (7)–(9) imply exactly this same formula for the
maximal-seed description. The accepted sufficient-statistic, parameter-
identifiability and finite likelihood-maximization conclusions consequently
describe their common native family. This use is justified by the new
kernel/path equality, not by assuming the theorem applies to any changed
seed law.

There is no contradiction: different \(p\)'s give distinguishable native
distributions, but at a given \(p\), two distinct auxiliary kernels give
the very same native distribution. The map from auxiliary subset kernels
to native kernels is many-to-one. Even access to every finite native
history, including marks and the declared coarse payload maps, cannot
select between these two descriptions. In particular the order likelihood
cannot establish independent elementary retained-edge selection.

The unchanged \(p\) in (6) need not equal every retained-edge marginal:
(11) makes that distinction explicit. No alternative native-law difference
remains to report for this construction. A change violating the
pushforward condition would change the individual native ideal kernel,
but none is being manufactured here.

This is not a claim that physical interactions are redundant, that all DET
formulations omit additional live variables, or that a hidden seed can
never be observed under another contract. It is a precise statement about
the actual state declared in the supplied conditional model. No new
physical readout, clock, action, energy/work-store or law-selection premise
has been supplied. The physical native preparation/readout gap remains.
No literature novelty, estimator calibration, erasure extension, coefficient
reduction or application advantage is asserted.

## 7. Sources, evidence and author boundary

[BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md) supplies the product
construction, closure fibers, individual-ideal positivity and full native
maps. [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) supplies the actual declared state and admission
conditions. [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) distinguishes actual native probability
changes from representation changes. [BERNOULLI_ORDER_LIKELIHOOD.md](BERNOULLI_ORDER_LIKELIHOOD.md) is
the exactly accepted likelihood predecessor, not a source claiming that
its latent construction is observationally unique.

### Separate review and publication note

The source manuscript was constructed by manual mathematics. Subsequent
independent manual review and coordinator adjudication accepted the exact
conditional result in sections 1–6. Those decisions are distinct from
publication preparation and the separate editorial correspondence review.
No scientific executor, simulation or numerical probability evaluation was
used to establish this theorem.

The source author documented complete current captures of four permitted
manuscripts and two source-status records. The manuscript bodies exactly
matched previously consumed stored bodies; that prior consumption was reused,
rather than represented as fresh complete displays. The declared-state,
positivity and Bernoulli-construction passages were additionally displayed.
Both source-status records were fully displayed. Their schemas supplied
expected identities for the four manuscripts, while identities of the two
records were observed separately. No missing acceptance timestamp was
invented for the predecessor.

The independent native review was exposed to the assignment and author
metadata, not blinded. Its initial aggregate metadata display was truncated;
bounded recovery supplied the current schemas and identity maps without
claiming complete manual consumption of every nested historical receipt.
A coordinator display truncation affecting the review text was recovered
with a complete review read. Current byte and captured-string checks support
source correspondence, not mathematical proof or reconstructed historical
custody.

Author-supplied worker review and guard reports remain distinct from
independent review and direct coordinator observations. Complete source
captures remain distinct from metadata-only receipt readbacks. Historical
display and receipt failures, control halt/revalidation and custody limits
remain preserved in the private records. Present identity checks do not
retroactively repair those limits.

Under the [metadata-obscured publication policy](../../coordination/REDACTED_PUBLICATION.md),
private identifiers, local paths, private fingerprints, raw source/check
records, command receipts, administrative scripts and machine/location
metadata are withheld. The exact original and transformation correspondence
remain local. This public manuscript supplies the full mathematical
argument and its linked public dependencies; it is not an executable
installation or an independently replayable custody package.

The accepted result concerns nonidentifiability of a redundant auxiliary
description under the declared native observation. It does not establish a
new native law, physical nonidentifiability under another observation,
calibrated inference, literature novelty or application advantage. Other
lane results and successor work are outside this payload; their current
statuses are recorded separately. RET remains paused.
