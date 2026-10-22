# Finite-height diagnosis without the original size

Status: manual theorem candidate; independent native adjudication pending.
Date: 2026-10-22.
Scope: one fixed-size experiment, bounded vertex loss, faithful completed
survivor order, and two specified optional law families.

## 1. Answer and observation contract

Exact external knowledge of the original deterministic size is **not
mathematically indispensable** for this diagnostic. A rule using only the
observed order and size, the predeclared absolute loss budget, and fixed
design constants has uniform finite wrong-label bounds. It abstains at
small observed sizes. A guaranteed decision requires a separate size
condition, stated below rather than hidden in the input.

Fix before observation:

- \(p_0\in(0,1)\), an integer absolute erasure budget \(d\ge0\), and
  desired errors \(\varepsilon_{\mathrm B},\varepsilon_{\mathrm F}\in(0,1)\);
- the two law families defined below and the rule in section 2;
- an integer cutoff parameter \(r\) satisfying (1).

The original size \(N\ge2\) is deterministic but is **not supplied to the
observer**. Under each separately fixed law, generate its history from
empty to size \(N\). A channel may inspect the entire generated history
and choose a random or deterministic erased set \(A\), with
\(a=|A|\le\min\{d,N\}\). It supplies exactly
\(Q=P_N[V\setminus A]\), up to arbitrary relabeling, and \(m=|Q|=N-a\).
The available relation contains every true comparison between survivors.
It is restriction of the completed order, not deletion in a generating
DAG followed by recomputed reachability.

Formally the channel is a probability kernel on allowed erased sets
conditional on the finite history. The joint law integrates this kernel
against the stated fixed-\(N\) history law, preserving that marginal.
There is no erasure independence assumption. Postselection of original
histories, a changed generative marginal, inserted vertices, wrong or
unknown survivor comparisons, and a false budget are outside the contract.

The law families are the accepted from-empty constructions:

- \(\mathrm B(p_0)\): each fixed \(p\in[p_0,1)\). At every birth,
  independently select each old vertex with probability \(p\), independently
  across births, and give the newborn the downward closure of that subset
  as its strict past.
- \(\mathrm F\): each fixed integer \(q\ge1\). At a birth with \(j\) old
  vertices, independently of previous birth coordinates select an individual
  subset \(U\subseteq[j]\) with probability
  \[
  \frac{1}{(|U|!)^q Z_{j,q}},\qquad
  Z_{j,q}=\sum_{k=0}^j\frac{\binom jk}{(k!)^q},
  \]
  and again take its downward closure as the newborn's strict past.

Both retain the declared fair immutable marks and fixed-carrier arbitrary
complex PSD payload with scalar-passive branch maps. The present statistic
uses only their unmarked order. These are optional laws in the conditional
model, not laws forced by DET or new quantum dynamics. All parameters are
fixed independently of history and data.

## 2. The rule and its uniform statement

Choose, without knowing \(N\), any integer
\[
r\ge\left\lceil\max\left\{
1,\ \frac{6d}{p_0},\
\frac{1}{\varepsilon_{\mathrm B}p_0^2},\
\left(\frac{16\mathrm e}{p_0}\right)^2,\
\left(\frac{8}{p_0\log2}\right)^2,\
\frac{8\log(1/\varepsilon_{\mathrm F})}{p_0\log2}
\right\}\right\rceil,\qquad M=r+1. \tag{1}
\]
Natural logarithms are used. These are conservative symbolic sufficient
conditions; no numerical tail or size evaluation is performed.

Let height count chain vertices, with empty height zero. The observer uses
\[
\boxed{
\delta(Q;m,p_0,d,M)=
\begin{cases}
\bot,&m<M,\\
\mathrm B,&m\ge M,\quad H(Q)\ge t(m)+1,\\
\mathrm F,&m\ge M,\quad H(Q)<t(m)+1,
\end{cases}
\quad
t(m)=\left\lceil\frac{p_0(m-1)}2\right\rceil-d .
} \tag{2}
\]
The threshold need only be computed when \(m\ge M\).
Here \(\bot\) means abstain, not a third candidate law. The function of
\(m\) is predeclared; it is not a threshold fitted after inspecting height.
The design tolerances and \(M\) are chosen constants, not extra facts
about the inaccessible parent.

**Theorem.** For every deterministic \(N\ge2\), every allowed channel \(K\),
and each separately fixed law in the respective class,
\[
\Pr_{p,N,K}(\delta=\mathrm F)\le\varepsilon_{\mathrm B}
\quad(p\in[p_0,1)),\qquad
\Pr_{q,N,K}(\delta=\mathrm B)\le\varepsilon_{\mathrm F}
\quad(q\in\{1,2,\ldots\}). \tag{3}
\]
These bounds count wrong labels, not abstentions. For \(N<M\), both
wrong-label probabilities are zero because the procedure always abstains.

For \(N\ge M\), put, **in the proof only**,
\[
n=N-1,\quad k_N=\lceil p_0n/2\rceil,\quad
s_N=\left\lceil\frac{p_0(n-d)}2\right\rceil-d . \tag{4}
\]
The stronger finite statements are
\[
\Pr_{p,N,K}(\delta=\mathrm F)
\le b_{\mathrm B}(N):=\min\{1,1/(np_0^2)\}, \tag{5}
\]
\[
\Pr_{q,N,K}(\delta=\mathrm B)
\le b_{\mathrm F}(N):=
\min\left\{1,\frac{N(2\sqrt n)^{s_N}}{s_N!}\right\}
\le
\min\left\{1,N\left(\frac{2\mathrm e\sqrt n}{s_N}\right)^{s_N}\right\}.
\tag{6}
\]
The unknown \(N\) indexes mathematical guarantees; it is not an input to
(2), nor must the observer evaluate (5)–(6). The common tolerances (3)
are available from the design. This is a uniform family of fixed-\(N\),
unconditional class-conditional error guarantees, **not** a data-dependent
confidence statement or a guarantee conditional on the observed \(m\)
or on returning a label.

## 3. Deterministic transfer and integer conditions

For any finite order \(P\), deleting \(a\) vertices from a longest chain
removes at most \(a\) chain members. Every remaining comparison is retained,
and every survivor chain was a parent chain. Thus
\[
\max\{0,H(P)-a\}\le H(P[V\setminus A])
\le\min\{H(P),|P|-a\}. \tag{7}
\]
In particular, writing \(H=H(P_N)\) and \(h=H(Q)\),
\(H-d\le h\le H\), and \(N-d\le m\le N\), simultaneously for all
allowed erasures.

If \(N<M\), then \(m\le N<M\), proving the asserted automatic abstention.
Otherwise \(n\ge r\ge6d/p_0\). This gives \(d<n\), including \(d=0\),
and
\[
\begin{aligned}
s_N
&\ge p_0(n-d)/2-d\\
&=p_0n/2-(1+p_0/2)d\\
&\ge p_0n/2-\tfrac32d
\ge p_0n/4>0 .
\end{aligned} \tag{8}
\]
Since \(s_N\) is an integer, \(s_N\ge1\). Also
\(s_N\le k_N-d\le n\).
The deterministic size interval and monotonicity of the ceiling imply
\[
s_N\le t(m)\le k_N-d. \tag{9}
\]
When a decision is made, \(m-1\ge r\) and
\(d\le p_0(m-1)/6\), so
\[
t(m)\ge p_0(m-1)/3>0,\qquad
t(m)\le m-1,\qquad 2\le t(m)+1\le m. \tag{10}
\]
This validates the finite threshold; it cannot lie above all possible
observed heights or be nonpositive in the decision region.

For every generated history and every allowed erasure,
\[
\{\delta=\mathrm F\}\subseteq\{H<k_N+1\},\qquad
\{\delta=\mathrm B\}\subseteq\{H\ge s_N+1\},
\quad N\ge M. \tag{11}
\]
For the first inclusion,
\(H-d\le h<t(m)+1\le k_N-d+1\).
For the second, \(H\ge h\ge t(m)+1\ge s_N+1\).
Abstaining outputs belong to neither left-hand error event.

These inclusions hold pointwise, before any averaging. Integrating their
indicators against an arbitrary allowed kernel proves channel-uniform
bounds by the corresponding original fixed-\(N\) height probabilities.
No probability law at the random observed size is inserted.

## 4. Finite stochastic bounds and sufficient constants

### Bernoulli premise and error

Start a chain at vertex 1 and append each new vertex exactly when it
selects the current tip. Conditional on the entire previous history, that
fresh selection has probability \(p\). Iterating the conditional
probabilities gives iid Bernoulli increments for this chain, even though
its tip is chosen adaptively. On the law's own measure,
\[
H\ge1+B_n,\qquad B_n\sim\operatorname{Binomial}(n,p).
\]
Thus \(H<k_N+1\) implies
\[
B_n\le k_N-1<p_0n/2,\qquad np-B_n>np_0/2.
\]
The strict ceiling inequality \(\lceil x\rceil-1<x\) also holds at integer
\(x\). Since \(\operatorname{Var}(B_n)=np(1-p)\le n/4\), Chebyshev gives
\(\Pr_p(H<k_N+1)\le1/(np_0^2)\), clipped at one.
Together with (11), this proves (5). Equation (1) then implies the
Bernoulli half of (3).

### Factorial premise and error

For completeness the required common finite tail is independent of any
asymptotic height claim. Write
\(w_j(k)=\binom jk/(k!)^q\), and \(J=|U|\) at a \(j\)-parent birth.
The identity
\(k^{q+1}w_j(k)=(j-k+1)w_j(k-1)\), summed and normalized, gives
\(\mathbb E J^{q+1}+\mathbb E J=j\).
Convexity and exchangeability yield, for any specified old vertex,
\[
\rho_{j,q}=\Pr_q(i\in U)=\mathbb E J/j
\le j^{-q/(q+1)}\le j^{-1/2},\quad j\ge1. \tag{12}
\]
There is no division by \(j=0\), and no assumed independence within a
single subset.

The completed order is the transitive closure of the forward birth DAG.
A chain of at least \(u+1\) vertices yields a directed path with at least
\(u\) edges by concatenating witness paths between successive chain
vertices: their increasing-label intervals have disjoint interiors.
Truncate to \(u\) edges. For a specified such path, the required selections
have distinct birth heads and hence independent coordinates. There are
at most \(N\) starting vertices for each increasing set of \(u\) heads.
Put \(A_{N,q}=\sum_{j=1}^n\rho_{j,q}\le2\sqrt n\); the last inequality
follows by integrating \(x^{-1/2}\) on \([0,n]\).
Expanding \(A_{N,q}^u\) counts each distinct-head product \(u!\) times.
Path counting and Markov therefore give, for integer \(1\le u\le n\),
\[
\Pr_q(H\ge u+1)\le
\min\{1,N A_{N,q}^u/u!\}
\le\min\{1,N(2\sqrt n)^u/u!\}. \tag{13}
\]
Different paths need not be independent.
The inequality \(u!\ge(u/\mathrm e)^u\) follows from
\(\log(u!)\ge\int_1^u\log x\,dx\ge u\log u-u\), including \(u=1\).
Use \(u=s_N\), permitted by (8), and (11) to obtain (6).

Finally (8) and the sufficient size conditions in (1) give
\[
\frac{2\mathrm e\sqrt n}{s_N}\le\frac{8\mathrm e}{p_0\sqrt n}
\le\frac12,\qquad
b_{\mathrm F}(N)\le(n+1)2^{-p_0n/4}. \tag{14}
\]
Here the needed entry of (1) is explicitly \(n\ge(16\mathrm e/p_0)^2\).
For \(n\ge1\), \(\log(n+1)\le\sqrt n\): the difference is positive at 1,
and its derivative is
\((\sqrt x-1)^2/[2\sqrt x(x+1)]\ge0\).
The entry \(n\ge[8/(p_0\log2)]^2\) consequently implies
\[
(n+1)2^{-p_0n/4}
\le \exp[-(p_0\log2)n/8]\le\varepsilon_{\mathrm F}, \tag{15}
\]
using the last entry of (1). This proves the factorial half of (3).
Ceilings preserve the nonstrict sufficient inequalities at their endpoints.
The bounds are conservative; no optimized constants are claimed.

## 5. Abstention is a real cost, not a concealed success

For either class and every allowed channel:
\[
\begin{array}{c|c}
\text{Original size (proof parameter)}&\text{Abstention behavior}\\ \hline
N<M&\Pr(\delta=\bot)=1\\
M\le N<M+d&\text{No nontrivial channel-uniform upper bound below 1}\\
N\ge M+d&\Pr(\delta=\bot)=0 .
\end{array} \tag{16}
\]
The middle interval is empty when \(d=0\).
In that interval a channel can always erase
\(a=N-M+1\le d\) vertices, giving \(m=M-1\), so it can force abstention.
The no-erasure channel instead guarantees \(m=N\ge M\) and a decision.
The last line follows from \(m\ge N-d\ge M\).

If abstention is counted as failure, the disjoint events give
\[
\Pr(\text{wrong label or abstention})
=\Pr(\text{wrong label})+\Pr(\bot)
\le\min\{1,\varepsilon_C+\Pr(\bot)\}, \tag{17}
\]
with \(C=\mathrm B\) or \(\mathrm F\) and its corresponding tolerance.
For \(N\ge M\), \(b_C(N)\) may replace \(\varepsilon_C\).
Only for \(N\ge M+d\) does this construction guarantee a decision and
total failure at most the designated tolerance uniformly over channels.
For fixed \(d,p_0\), the finite error bounds also tend to zero as the
unknown deterministic \(N\) increases; abstention is then absent.

There is therefore no external size-lower-bound premise for (3).
There **is** an exposed original-size condition for guaranteed
non-abstention. The theorem does not claim a successful decision at every
size. Empty and singleton outputs abstain. Complete erasure, when allowed,
also abstains. At \(d=0\), the classified-region threshold is the unerased
threshold with \(m=N\); the entire procedure still adds small-size abstention.

Neither (3) nor observing \(m\ge M\) supplies
\(\Pr(\text{wrong label}\mid m)\) or
\(\Pr(\text{wrong label}\mid\delta\ne\bot)\le\varepsilon_C\).
A history-dependent channel can make these conditioning events selective.
If the decision probability is positive, the elementary conditional upper
bound is only
\(\min\{1,\varepsilon_C/\Pr(\delta\ne\bot)\}\) from (3), which may be trivial.
No class posterior or observed-data confidence level is asserted.

Unknown deterministic \(N\) is not a random stopping time. Uniform separate
fixed-\(N\) bounds do not authorize scanning a growing history and choosing
its reported size or stopping at a favorable observation. For a random
size, merely having every fixed-size marginal available does not establish
the needed law conditional on the selected size. No optional-stopping,
simultaneous-size or data-selected-size theorem is supplied here.

## 6. Available inputs, computation, and remaining limits

The mathematical rule needs \(p_0,d,M,m\) and the exact completed order
on the \(m\) survivors. It requires no parent size, birth labels, deleted
identities, generating edges, parent embedding, marks or payload entries.
Relabeling leaves height and the decision unchanged.

A sufficient representation is the \(m\)-by-\(m\) Boolean strict-relation
matrix. Once \(m\ge M\), topological ordering and longest-chain dynamic
programming compute height in \(O(m^2)\) relation inspections and integer
operations. Every relation path is a chain and successive vertices of
every chain have relation entries, proving correctness with transitive
entries included. Under indexed matrix access, sufficient bookkeeping
cost is \(O(m^2\log m)\) bit work and \(m^2+O(m\log m)\) matrix/workspace
bits. This is not physical acquisition cost or an optimality claim.

For finite exact computation, it suffices to predeclare rational
\(p_0=a/b\), \(0<a<b\), and an integer \(r\) satisfying the symbolic design
inequalities. Exact threshold arithmetic uses
\(\lceil a(m-1)/(2b)\rceil-d\).
If numerator and denominator have at most \(L\) bits, a sufficient separate
bound is \(O((L+\log(m+d+r+2))^2)\) bit operations and
\(O(L+\log(m+d+r+2))\) additional input/workspace bits.
For arbitrary real \(p_0\), the mathematical definition does not supply an
exact-real computational oracle. No numerical cutoff preparation or
algorithm execution is performed.

An inconsistent matrix may be rejected as malformed input; validity checks
do not certify that a valid order is the true completed restriction.
Unknown or false loss budgets, damaged comparisons and arbitrary channel
corruptions remain outside the theorem. The mechanism for obtaining a
faithful order and certifying its loss budget is still unsupplied.

This is not a classifier for all admitted laws, an empirical discriminator,
a full-QM derivation, manifold reconstruction, mass/gravity law, physical
clock, metric-as-record promotion or application-value result. A separate
benchmark, baselines, physical preparation/readout, costs, specified
failures and held-out evaluation would still be needed for an application
claim. Records are not declared to exhaust present relational activity.

## 7. Evidence boundary and stop

The six permitted literal manuscripts supply: the accepted bounded-erasure
predecessor; its finite-height predecessor; the Bernoulli and factorial
law constructions; and the conditional-model and law-dependence scope.
The six public dependencies and their scientific roles are:

- [Bounded vertex-erasure height diagnostic](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md): faithful completed induced survivor orders and bounded-erasure transfer.
- [Finite intrinsic-height law separation](FINITE_HEIGHT_LAW_SEPARATION.md): the predeclared finite two-family height test.
- [Bernoulli-subset law](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md): the admitted Bernoulli construction and greedy-chain bounds.
- [Factorial-power law family](FACTORIAL_POWER_LAW_FAMILY.md): the separately fixed integer family and factorial-moment path bounds.
- [Conditional theorem package](THEOREM_PACKAGE.md): the declared growth-model premises and their conditional scope.
- [Law dependence](LAW_DEPENDENCE.md): optional law selection versus principle-forced identities.

The source's private provenance records were inspected and their exact source
and predecessor-adjudication pins joined. The bounded-erasure predecessor
had been accepted before this manuscript was constructed; that historical
acceptance did not accept this manuscript. The supplied public snapshot
identifier was metadata, not independently verified Git or network history.
No embedded source paths, archive links or additional adjudication members
were followed. Prior-turn captured bodies were unavailable in the source
worker's tool store, so none was reused on an unverified equality claim.
All six source bodies and both provenance records were freshly consumed.
Two combined displays were truncated; intact native captures were retained
and complete consumption recovered by bounded displays. Those failures and
older source-contained limitations remain recorded; current checks do not
reconstruct historical custody.

One supplied-context manual review checked the theorem, constants, endpoints
and fixed-size/selection distinctions and reported PASS without a mathematical
correction. That source-stage report was not a source audit, proof-assistant
verification or native acceptance. Worker-reported usage observations remain
separate from coordinator-direct captures. Full source and manuscript captures
remain distinct from metadata-only receipt readbacks.

The source construction used only manual symbolic mathematics and administrative
text, JSON, exact readback, hash, size and inventory operations. No scientific
executor, numerical probability/tail/interval evaluation, coefficient
reduction, simulation, optimizer, benchmark, dataset/network acquisition,
protected validation, repository/Git operation or public replay was done.
The exact private source, correspondence map, raw provenance and check receipts
remain local under the [publication policy](../../coordination/REDACTED_PUBLICATION.md).
This public derivative supplies the theorem and public dependencies, not an
executable reconstruction of private custody.

### Separately added native-adjudication and publication note

The pending-adjudication status at the beginning is the frozen author's
historical status. After that freeze, an independent reviewer completed
a manual derivation before reading this candidate, then reviewed its exact
text; the problem and predecessors were disclosed, so the review was not
blinded. The coordinator subsequently accepted this exact theorem within
its stated conditional mathematical scope. Manual source construction,
supplied-context reports, independent native review, coordinator acceptance
and editorial publication checks are separate acts. Administrative identity
checks are not a machine proof or a new scientific calculation.

The accepted result gives finite unconditional wrong-label guarantees with a
declared cutoff and exact abstention accounting even though the original size
is not an observer input. It retains a fixed deterministic original size,
a hard deletion bound, the faithful completed induced survivor order and
a kernel preserving the specified law marginal. It supplies no physical
prediction, acquisition channel, application evaluation or universal classifier.
Publication does not establish conditional-on-decision confidence.

A separately assigned finite intrinsic-order likelihood and Bernoulli-parameter
identifiability problem is pending and excluded from this result. No further
erasure-channel relaxation is selected. The measurement, E, NE and CE lanes
have separate scoped design dispositions and execution holds; their bodies and
pending follow-up work are not part of this theorem publication. RET remains paused. The separate completed
public-data replay is not reopened.
