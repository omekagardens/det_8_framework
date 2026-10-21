# Factorial-subset law and sublinear intrinsic height

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: an optional all-size marked-order law initialized from empty, not a
DET-forced law and not an extension preserving an arbitrary previously fixed
prefix. No scientific execution was performed.

## 1. Result and assumptions

Within the declared scalar/passive marked-order model, the following is a
complete admitted growth family:

\[
 \Pr(U_n=U)=\frac{1}{|U|!\,Z_n},\qquad
 Z_n=\sum_{k=0}^{n}\frac{\binom nk}{k!},\qquad U\subseteq[n].
 \tag{1}
\]

Draw the subsets independently at distinct births. Give vertex \(n+1\) strict
past \(S=\downarrow_{P_n}U_n\), and draw its immutable binary mark independently
and fairly. Here \(P_n\) is the old \(n\)-vertex order. Empty downward closure is
empty; \(0!=Z_0=1\). For every individual ideal \(S\) of \(P_n\), with
\(s=|S|\) and \(m=|\operatorname{Max}(S)|\), its probability is

\[
 q_F(P_n,r,S)=\frac{L(s,m)}{Z_n},\qquad
 L(s,m)=\sum_{k=m}^{s}\frac{\binom{s-m}{k-m}}{k!}.
 \tag{2}
\]

Maxima in (2) are taken in the **induced ideal**, not in the whole current
parent. This distinction matters in the incomparable-birth diamonds.

Let \(H_N\) be maximum chain cardinality in the resulting \(N\)-vertex order.
The construction satisfies, for \(N\ge2\) and integer \(\ell\ge1\),

\[
 \Pr(H_N\ge\ell+1)
 \le \min\left\{1,\frac{N(2\sqrt{N-1})^\ell}{\ell!}\right\}
 \le \min\left\{1,N
       \left(\frac{2\mathrm e\sqrt{N-1}}{\ell}\right)^\ell\right\}.
 \tag{3}
\]

In particular,

\[
 \boxed{\limsup_{N\to\infty}\frac{H_N}{\sqrt N}\le2\mathrm e
        \quad\text{almost surely}.}
 \tag{4}
\]

Thus this admitted optional law has \(H_N=O(\sqrt N)\) almost surely and
\(H_N/N\to0\) almost surely. The constant is an upper bound, not an optimum or
an asserted limit. There is no matching lower bound here.

The model being checked has finite orders, immutable binary marks, all
individual ideals as possible birth precursors, positive normalized ideal
probabilities, marked equivariance, proper-precursor record locality, and
complete incomparable-birth diamonds. A branch with newborn bit \(b\) acts on
an arbitrary fixed-carrier complex PSD payload \(D\) by
\(D\mapsto q_F(P,r,S)D/2\). Payload dynamics are passive. These are precisely
the constraints used below; an unspecified stronger structural locality
condition is not assumed or claimed.

This theorem is a mathematical existence result in that declared class.
It neither derives the choice (1) from DET nor supplies a full QM derivation,
spacetime geometry, dimension, gravity, mass, a physical time variable, or an
empirical discriminator.

## 2. Exact ideal probabilities

For any ideal \(S\) in a finite parent \(P\),

\[
 \downarrow_P U=S
 \quad\Longleftrightarrow\quad
 \operatorname{Max}(S)\subseteq U\subseteq S.
 \tag{5}
\]

To prove necessity, closure equality implies \(U\subseteq S\). If \(x\) is
maximal in \(S\), some selected \(u\in U\) has \(x\preceq u\); since \(u\in S\),
maximality forces \(u=x\). For sufficiency, every point of a finite ideal lies
below a maximal point of that ideal. Consequently a subset containing all
those maxima and no points outside \(S\) has downward closure exactly \(S\).

A size-\(k\) generator must contain the \(m\) maxima and may select its other
\(k-m\) points from the remaining \(s-m\). Summing their per-subset probabilities
gives (2). This is a probability for each individual ideal, not an isomorphism
class of children. Different ideals with isomorphic induced orders remain
different branches.

The fibers of \(U\mapsto\downarrow_P U\) partition all \(2^n\) subsets.
Therefore

\[
 \sum_{S\in\operatorname{Id}(P)}L(|S|,|\operatorname{Max}(S)|)
 =\sum_{U\subseteq[n]}\frac1{|U|!}=Z_n,
 \qquad \sum_S q_F(P,r,S)=1.
 \tag{6}
\]

Each ideal has the generator \(U=\operatorname{Max}(S)\), so its probability
is strictly positive. For the empty ideal \(L(0,0)=1\) and its probability is
\(1/Z_n\). At the empty parent the only ideal is both empty and full,
\(q_F=1\); the two marked branches still have probabilities \(1/2\).

The construction uses **per-subset** weight \(1/k!\). Its cardinality law is
\(\Pr(|U_n|=k)=\binom nk/(k!\,Z_n)\). Omitting \(\binom nk\) from that
cardinality law would define a different process. It is neither a uniform
choice of cardinality nor a construction with independent inclusion
indicators within one subset.

## 3. Complete marked admissibility and the all-size measure

### Equivariance and record locality

An order relabelling carries subsets, their closures, and their induced
maxima bijectively to the relabelled objects while preserving cardinalities.
This proves marked equivariance. The ideal kernel ignores all old marks.
It therefore obeys the declared proper-precursor restriction on dependence
on marks, and also does not need unrestricted mark dependence on a full
precursor. It may read parent cardinality and the induced order on \(S\);
no new structural locality requirement is silently added.

### Complete diamonds, including full-first and equal precursors

Let \(C\) be any \(n\)-vertex marked order, and let \(S,T\) be any two ideals
of \(C\). Compare births with precursors \(S\) and \(T\), where the second
precursor excludes the other newborn, so that the two newborns are
incomparable. In \(C+S\), the old set \(T\) is still an ideal and its induced
order, cardinality and induced maxima are unchanged. The analogous assertion
holds for \(S\) in \(C+T\). Writing \(L(S)\) for the numerator in (2), both
two-step unmarked probabilities are therefore

\[
 q_F(C,S)q_F(C+S,T)
 =\frac{L(S)L(T)}{Z_nZ_{n+1}}
 =q_F(C,T)q_F(C+T,S).
 \tag{7}
\]

This proof includes \(S=T\), overlapping or nested precursors, the empty
precursor, and either or both first precursors equal to all of \(C\).
For example, a full old precursor becomes proper after the other newborn
is added, but its **induced** maxima and hence its numerator do not change.

For any assigned bits \(b,c\), each path in the diamond multiplies its
probability by \(1/4\). On the entire PSD carrier, both routes are the same
map

\[
 D\longmapsto\frac{L(S)L(T)}{4Z_nZ_{n+1}}\,D.
 \tag{8}
\]

This is equality of maps for every PSD \(D\), not only equality of traces,
selected entries or a chosen state. For \(D=0\) both outputs are zero; the
classical probability kernel is independently defined by (1)–(2), with no
division by a zero trace.

### All sizes, not a finite-prefix extrapolation

For each \(n\ge0\), use the finite coordinate space
\(2^{[n]}\times\{0,1\}\) with probabilities
\(1/(2|U|!\,Z_n)\). The countable product of these independent finite
probability spaces defines the infinite sequence of choices. Recursively
taking downward closures constructs consistent finite histories from empty.

Conditional on the complete prior marked history, the next subset coordinate
retains (1), because that history depends only on earlier coordinates.
Consequently the next ideal-and-bit branch has exactly probability
\(q_F(P_n,r,S)/2\). This verifies that the independent-coordinate realization
is the desired all-size marked history measure, not merely a collection of
normalized rows.

Every permitted finite branch sequence has positive probability. No claim is
made that an individual infinite history has positive measure. The initial
law is fixed by (1) at every size; nothing here splices it onto an arbitrary
pre-existing prefix or establishes preservation of previously chosen
coefficient branches. The direct construction and diamond proof do not rely
on solving or executing a finite coefficient continuation.

## 4. Selection-size identity and old-vertex marginal

Let \(K_n=|U_n|\), \(w_n(k)=\binom nk/k!\), and
\(\mu_n=\mathbb E K_n\). For \(1\le k\le n\), cancellation of factorials gives

\[
 k^2 w_n(k)=(n-k+1)w_n(k-1).
 \tag{9}
\]

Summing (9), changing index \(j=k-1\), and noting that the missing \(j=n\)
term in the factor \(n-j\) is zero, gives

\[
 \sum_{k=0}^n k^2 w_n(k)
 =\sum_{j=0}^{n-1}(n-j)w_n(j)
 =nZ_n-\sum_{j=0}^n j w_n(j).
\]

Division by \(Z_n\) yields the exact identity

\[
 \boxed{\mathbb E K_n^2+\mathbb E K_n=n.}
 \tag{10}
\]

Variance nonnegativity implies \(\mu_n^2+\mu_n\le n\). By exchangeability
of the \(n\) old vertices, for any specified one and \(n\ge1\),

\[
 \rho_n:=\Pr(i\in U_n)
 =\frac{\mu_n}{n}
 \le\frac{\sqrt{1+4n}-1}{2n}
 \le\frac1{\sqrt n}.
 \tag{11}
\]

The same marginal holds conditional on the complete prior history. No
independence of two inclusion indicators in the same \(U_n\) was used.
At \(n=0\), \(K_0=0\) and (10) holds; \(\rho_0\) is unnecessary and is not
defined by division by zero.

## 5. Intrinsic height as directed-path height

Label the vertices \(1,\ldots,N\) in birth order and place a directed edge
\(i\to j\) exactly when \(i\in U_{j-1}\). Every edge increases its label.
Induction over births shows that the reachability order of this DAG is
exactly the order produced by the downward-closure rule: the ancestors of
the new vertex are the old downward closure of its selected vertices.

Every directed path is a chain in that reachability order. Conversely, given
a chain \(v_1\prec\cdots\prec v_h\), choose directed paths joining consecutive
chain vertices. Internal labels of each joining path lie strictly between
its endpoint labels. The interiors for consecutive joins are therefore
disjoint, and concatenation is a directed path containing all \(h\) chain
vertices. The maximum chain cardinality thus equals the maximum directed
path vertex count.

It follows that \(H_N\ge\ell+1\) entails the existence of an \(\ell\)-edge
directed path; a longer path can be truncated. These labels are construction
indices, not supplied geometric coordinates or elapsed physical time.

## 6. Path counting and the finite-size tail

For a specified increasing sequence \(i_0<\cdots<i_\ell\), the event of all
its directed edges has probability

\[
 \Pr(i_0\to i_1\to\cdots\to i_\ell)
 =\prod_{r=1}^{\ell}\rho_{i_r-1}.
 \tag{12}
\]

There is one required inclusion in each of \(\ell\) distinct subset
coordinates. Their independence across births proves (12); no independence
within a subset, between arbitrary edges, between different paths, or
between different values of \(N\) is asserted.

Let \(X_{N,\ell}\) count increasing \(\ell\)-edge paths. Its first moment is

\[
 \mathbb E X_{N,\ell}
 =\sum_{2\le j_1<\cdots<j_\ell\le N}
       (j_1-1)\prod_{r=1}^{\ell}\rho_{j_r-1}.
 \tag{13}
\]

There are \(j_1-1\) possible initial vertices for that head sequence.
Set \(A_N=\sum_{n=1}^{N-1}\rho_n\). Replacing \(j_1-1\) by \(N\) overcounts.
In the expansion of \(A_N^\ell\), every distinct increasing head sequence
occurs in \(\ell!\) permutations, and repeated-index terms are nonnegative.
It follows that

\[
 \mathbb E X_{N,\ell}\le \frac{N A_N^\ell}{\ell!}.
 \tag{14}
\]

Also, using (11) and the integral of the decreasing function \(x^{-1/2}\),

\[
 A_N\le\sum_{n=1}^{N-1}n^{-1/2}
 \le\int_0^{N-1}x^{-1/2}\,dx=2\sqrt{N-1}.
 \tag{15}
\]

The path-height equivalence and Markov's inequality give the first bound
in (3). For integer \(\ell\ge1\),

\[
 \log(\ell!)\ge\int_1^\ell\log x\,dx
 =\ell\log\ell-\ell+1\ge\ell\log\ell-\ell,
\]

so \(\ell!\ge(\ell/\mathrm e)^\ell\), proving the second bound. If
\(\ell\ge N\), the path count is zero and the event is impossible; this
stronger exact edge-case statement is consistent with the displayed upper
bounds. Separately, \(H_0=0\) and \(H_1=1\).

No finite-size probability, interval, or tail value was evaluated
numerically. Equations (9)–(15) are symbolic identities and inequalities.

## 7. Almost-sure sublinear height

Fix any real \(c>2\mathrm e\), and define

\[
 \ell_N=\lceil c\sqrt N\rceil,\qquad
 \beta_c=c\log\!\left(\frac{c}{2\mathrm e}\right)>0.
\]

Since \(2\mathrm e\sqrt{N-1}/\ell_N\le2\mathrm e/c<1\), (3) implies

\[
 \Pr(H_N\ge\ell_N+1)
 \le N\exp(-\beta_c\sqrt N).
 \tag{16}
\]

This is summable in \(N\): for \(k^2\le N<(k+1)^2\), the sum of those terms
is at most
\((2k+1)(k+1)^2\exp(-\beta_c k)\).
The resulting polynomial-times-geometric series converges.
The first Borel–Cantelli lemma, which needs no independence between these
events, now gives

\[
 H_N\le\lceil c\sqrt N\rceil
 \quad\text{eventually almost surely}.
 \tag{17}
\]

Intersect the probability-one conclusions (17) for the countable sequence
\(c_j=2\mathrm e+1/j\). Taking limsups proves (4). This is **not** the
stronger assertion \(H_N\le2\mathrm e\sqrt N\) eventually, which has not
been proved here.

Consequently \(H_N/N\to0\) almost surely under this law. Because
\(0\le H_N/N\le1\), bounded convergence also gives convergence to zero in
\(L^1\) (and, in fact, every fixed finite \(L^p\)), hence in probability.
The almost-sure conclusion came from a summable path tail, not from
expectation convergence alone.

## 8. The complete height drift, not only full-precursor births

For a nonempty parent \(P\), let \(T(P)\) be the set of **top/terminal
endpoints** of chains of maximum cardinality \(h(P)\), and put
\(t(P)=|T(P)|\). Every element of \(T(P)\) is maximal in \(P\): otherwise
its maximum chain could be extended.

The downward closure of \(U\) has height \(h(P)\) if and only if
\(U\cap T(P)\ne\varnothing\). One direction holds because a selected terminal
endpoint brings its entire maximum chain into the closure. Conversely,
a maximum chain contained in \(\downarrow U\) ends at some \(x\in T(P)\).
Since \(x\preceq u\) for a selected \(u\), maximality of \(x\) forces \(u=x\).

A birth with past \(S\) has height

\[
 h(P+S)=\max\{h(P),1+h(S)\}.
\]

Therefore, writing \(n=|P|\ge1\), its complete height-increase probability is

\[
 \boxed{p_F(P)=\Pr(U_n\cap T(P)\ne\varnothing)
             =1-\frac{Z_{n-t(P)}}{Z_n}.}
 \tag{18}
\]

Indeed, the total unnormalized weight of subsets avoiding \(T(P)\) is
\(Z_{n-t(P)}\), since exactly \(n-t(P)\) vertices remain available with the
same per-subset weights. For the empty parent the first birth always
increases height, so \(p_F(\varnothing)=1\); formula (18) is expressly
restricted to nonempty parents.

This drift need not be small at every parent of large size. On the
\(n\)-element antichain, \(t(P)=n\), so

\[
 p_F(P)=1-\frac1{Z_n}\ge\frac{n}{n+1},
 \qquad Z_n\ge1+n.
 \tag{19}
\]

Such rows are admissible; no uniform decay over all rows can be inferred.
The almost-sure theorem controls histories of the selected law instead.

For contrast, a full-precursor birth occurs exactly when
\(\operatorname{Max}(P)\subseteq U_n\). Choosing any one maximal vertex
of a nonempty parent gives

\[
 q_F(P,P)\le\rho_n\le n^{-1/2}.
 \tag{20}
\]

Equation (20) bounds only one part of the complete drift. Substituting it
for (18) would be invalid and is not used in the height proof.

Finally, apply the accepted height-drift tracking theorem to this admitted
all-size history measure and its full prior-history filtration. With
\(p_n=p_F(P_n)\), including \(p_0=1\), that theorem states

\[
 \frac{H_N-\sum_{n=0}^{N-1}p_n}{N}\longrightarrow0
 \quad\text{almost surely}.
\]

Together with (4) it follows that

\[
 \frac1N\sum_{n=0}^{N-1}p_F(P_n)\longrightarrow0
 \quad\text{almost surely}.
 \tag{21}
\]

This is the actual-history Cesàro drift conclusion for this law only.
It neither asserts a uniform bound on all rows nor proves a rowwise
optimizer, and does not turn a mean conclusion into an almost-sure one.

## 9. Relation to the accepted obligations and limits

The new result answers an existence question left open by the finite-prefix
neutral-support and height-selection analyses: an explicit all-size
admitted family can have sublinear intrinsic height. It is a new optional
choice, not a claim that every admissible family does so.

The half-scale law's accepted linear-height conclusion is not contradicted:
that result and (4) concern different selected laws. Their contrast makes
law dependence concrete. The older finite-size zero-support witnesses do
not themselves prove this all-size construction; sections 2–7 supply its
independent proof.

The target screen gives a necessary implication from approximation by
certain stipulated sublinear-height targets to sublinear height of the
approximating history. This note supplies the latter property for one law.
It does not reverse that implication. No closeness to a manifoldlike
target, deletion distance, intrinsic dimension, embedding, metric, volume,
Lorentzian structure, or geometric limit has been proved.

In particular:

- The factorial weights are proposed, not derived from DET primitives.
- The quantum payload remains explicitly present but passive. Equations
  (7)–(8) do not reconstruct interference, Hilbert space or quantum dynamics.
- Record growth counts committed births. It does not establish that
  committed records exhaust live relational activity.
- No arbitrary fixed prefix, earlier optimizer choice or coefficient
  continuation is preserved by adopting this from-empty law.
- No empirical correspondence, gravitational novelty, metric-as-record
  promotion, mass law, physical dimension or discriminator follows.
- No scientific code, numerical evidence, simulated histories, or optimization
  was used to support these claims. This is manual symbolic verification,
  not a proof-assistant certificate.

No successor, expanded protocol, physical test or new lettered gate is
selected by this packet. The bounded obligation ends with this theorem
candidate and its provenance. Native acceptance and any later decision
remain separate.

## 10. Source and review provenance

The public exposition dependencies and their scientific roles are:

| Public source | Scientific role |
| --- | --- |
| [NEUTRAL_SUPPORT_FEASIBILITY.md](NEUTRAL_SUPPORT_FEASIBILITY.md) | Separate finite-prefix neutral-support feasibility and its unresolved all-size obligations; native predecessor in the original source set. |
| [HEIGHT_DRIFT_LAW_SELECTION.md](HEIGHT_DRIFT_LAW_SELECTION.md) | Complete height drift and actual-history almost-sure tracking; weaker convergence modes remain distinct. |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Declared scalar/passive marked-order model, positive ideal kernels, marked equivariance, locality and complete diamonds. |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Structural identities versus optional law choices; fixed-prefix and coordinate-gauge limits. |
| [HALF_SCALE_HEIGHT_GROWTH.md](HALF_SCALE_HEIGHT_GROWTH.md) | Linear intrinsic height for a different selected law; comparison does not imply a universal law. |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Necessary intrinsic-height target screen, without a converse from sublinear height to target approximation or geometry. |

The source-author read six literal manuscripts and two literal provenance
records from the authorized source set. Exact paths, complete native
captures, native hash/byte observations and pin joins remain in the private
source record. No linked archives, source originals, datasets, Git paths
or protected materials were followed in that process.

The supplied source pin record attributes five public exposition snapshots
to a public source commit. That attribution is pinned metadata, not an
independent Git/network verification. The neutral-support manuscript was
instead the exact native subject of a separate conditional acceptance for
neutral-support and finite-prefix feasibility. Its historical pending
header did not supersede that later adjudication. Its link above is the
public derivative, not a claim that the native original belonged to the
five public snapshots at the historical source commit. Current public
navigation may contain later appended history; the original source pins
remain distinct from the public links supplied here.

The source-author's receipt reports full fresh source captures. The
neutral-support, half-scale-height and target-screen bodies matched
previously fully consumed complete bodies. Package and law snapshots
matched previously consumed complete prefixes plus displayed height-drift
additions; the current public height-drift body was separately displayed
and consumed. No truncation was reported for those author source captures.
These statements describe that source-author record, not a fresh audit of
linked originals by the derivative preparer. Historical custody, display,
execution and receipt limitations are retained.

The original manual-worker account is retained:

Two independent manual workers reviewed the supplied mathematical setup:
one checked admissibility, moments and complete drift; the other checked
path counting, indexing and the summable almost-sure bound. Neither read
sources nor executed mathematical programs. Their agreement is a manual
cross-check, not native adjudication or formal verification. Their reported
usage receipts are distinguished from the root's direct native observations.

Those worker messages and usage transcriptions are supplied-context reports,
not direct coordinator observations or independent source audits. Current
full captures, metadata-only receipt readbacks and worker reports remain
different evidence categories. Separate read/hash observations do not
establish atomic identity or reconstruct original custody.

The original evidence limitation is retained:

Full direct source/manuscript read captures and metadata-only summaries of
own-receipt readbacks are labelled separately in the receipts. Historical
custody or receipt defects in prior sources are not erased or repaired by
this new packet. Prior accepted and rejected empirical work stays separate;
no RET, clock, book or retired-gravity work is performed.

All nine scientific sections above retain the source-author's manual
symbolic construction and its stated limits. No scientific computation,
simulation, numerical tail evaluation or proof-assistant certificate is
supplied. Later independent native review is recorded separately from
source construction; preparation of this derivative is not mathematical
acceptance. A final publication review record is conditional on the
separate native, editorial and root acceptance gates.

Private identifiers, source paths, hashes, timestamps, receipt filenames,
tool/account metadata and private adjudication records are withheld.
Exact original text and correspondence remain local. Public source links
identify mathematical dependencies, not executable private-source custody.
No scientific execution, dataset, experiment, protected validation or
physical readout is supplied or authorized. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) for the public evidence scope.
