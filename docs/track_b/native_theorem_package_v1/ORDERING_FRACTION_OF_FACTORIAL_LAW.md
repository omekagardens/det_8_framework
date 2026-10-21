# Ordering fraction of the factorial-subset law

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: one fixed optional from-empty growth law. No law redesign, scientific
execution, numerical tail evaluation or physical-geometry claim.

## 1. Result and its precise meaning

For the accepted factorial-subset law, the fraction of incomparable
unordered vertex pairs converges to zero almost surely:

\[
 \boxed{\frac{I(P_N)}{\binom N2}\longrightarrow0
        \quad\text{almost surely}.}
 \tag{1}
\]

The ratio is defined as zero at sizes zero and one. Equivalently, for sizes
at least two, the comparable-pair fraction tends to one. This is pair-density
convergence, not eventual total ordering, not a linear-height assertion,
and not a change to the accepted \(H_N=O(\sqrt N)\) almost-sure upper bound.

There is a deterministic consequence for a **separately declared, fixed**
isomorphism-closed target class whose sufficiently large members have at
least a fixed positive fraction of incomparable pairs: only \(o(N)\) vertices
of \(P_N\) can be retained as an induced order in that class, almost surely.
The normalized vertex-deletion distance therefore tends to one, not zero.
The target hypothesis and exact retained-size bound are stated in section 8.

No assertion is made that the earlier bounded-aspect Ferrers target class
satisfies this additional density premise. Its definition is not changed.
The conclusion is not an exclusion of manifolds, metrics, Lorentzian
geometry, gravity or any physical model.

## 2. Fixed process, intrinsic observable and auxiliary filtration

At parent size \(n\), the accepted law draws \(U_n\subseteq[n]\) with

\[
 \Pr(U_n=U)=\frac1{|U|!\,Z_n},\qquad
 Z_n=\sum_{k=0}^{n}\frac{\binom nk}{k!}.
 \tag{2}
\]

The coordinates \(U_0,U_1,\ldots\) are independent across births. The newborn
\(n+1\) has strict past \(\downarrow_{P_n}U_n\), an independent fair immutable
bit, and passive scalar action on the full fixed-carrier PSD payload.
The law is fixed from empty at every size. There is no splice onto an
arbitrary earlier prefix or adjustment based on the diagnostic.

Write \(K_n=|U_n|\), \(\mu_n=\mathbb E K_n\), and, for \(n\ge1\),

\[
 \rho_n=\Pr(i\in U_n)=\mu_n/n
 \quad\text{for any specified }i\in[n].
\]

Exchangeability within one subset gives the marginal; independence of
different inclusion indicators **within** that subset is not assumed.
In particular, (2) is a per-subset law, not a law assigning cardinality
\(k\) a weight \(1/k!\) without its multiplicity \(\binom nk\).

Define intrinsic incomparable-pair count and fraction by

\[
 I(P)=\#\{\{x,y\}\subseteq V(P):x\ne y,\;
               x\nprec y,\;y\nprec x\},
 \qquad
 \eta(P)=
 \begin{cases}
 0,&|P|\le1,\\
 I(P)/\binom{|P|}{2},&|P|\ge2.
 \end{cases}
 \tag{3}
\]

Pairs are unordered and distinct, counted once. The comparable-pair count
is \(\binom{|P|}{2}-I(P)\); its fraction is \(1-\eta(P)\) for \(|P|\ge2\).
If a value is needed at sizes zero and one, set that fraction to zero too;
the complement identity is restricted to sizes at least two.

For the proof, put a directed edge \(i\to j\) when \(i\in U_{j-1}\).
The accepted construction identifies \(P_N\) with the transitive closure
of this increasing-label DAG. Each directed path implies comparability.
Adding a new maximal vertex leaves all old pair relations unchanged.

Use the auxiliary product-coordinate filtration

\[
 \mathcal G_n
 =\sigma(U_0,\ldots,U_{n-1},b_1,\ldots,b_n),
 \tag{4}
\]

after the first \(n\) births. Future subset coordinates retain their product
law independently of \(\mathcal G_n\). This filtration contains the visible
marked-order history but can contain more information: direct selected
edges need not be recoverable from their transitive closure. Every random
direct-successor set below is made measurable using (4), not silently
inferred from the record order.

The proof uses construction labels; the final observable \(\eta(P)\) is
isomorphism invariant. Birth indices are not geometric coordinates or an
assertion that record growth exhausts present relational activity.

## 3. Lower marginal and exact avoidance probabilities

Put \(w_n(k)=\binom nk/k!\). For \(0\le k<n\),

\[
 \left(\frac{n+1}{k+1}-1\right)w_n(k)
 =\frac{n-k}{k+1}w_n(k)
 =(k+1)w_n(k+1).
\]

The left side is zero at \(k=n\). Summation and division by \(Z_n\) give

\[
 \boxed{\mu_n=(n+1)\mathbb E\!\left[\frac1{K_n+1}\right]-1.}
 \tag{5}
\]

This includes \(n=0\), where \(K_0=\mu_0=0\). The function
\(x\mapsto1/(x+1)\) is convex on \(x\ge0\), so Jensen's inequality gives

\[
 \mu_n+1\ge\frac{n+1}{\mu_n+1},
 \qquad
 \mu_n\ge\sqrt{n+1}-1.
\]

Thus, for \(n\ge1\),

\[
 \boxed{\rho_n\ge
   \frac{\sqrt{n+1}-1}{n}
   =\frac1{\sqrt{n+1}+1}.}
 \tag{6}
\]

This complements the accepted upper bound \(\mu_n\le\sqrt n\); no
\(\rho_0\) is needed.

For any fixed \(D\subseteq[n]\) with \(d=|D|\), all avoiding subsets are
subsets of the remaining \(n-d\) vertices with the same per-subset weights.
Consequently

\[
 \Pr(U_n\cap D=\varnothing)=\frac{Z_{n-d}}{Z_n}.
 \tag{7}
\]

Taking \(d=1\) and using exchangeability proves

\[
 \frac{Z_{n-1}}{Z_n}=1-\rho_n,\qquad n\ge1.
 \tag{8}
\]

Telescoping (8) and applying \(1-x\le e^{-x}\) to each factor yields

\[
 \begin{aligned}
 \frac{Z_{n-d}}{Z_n}
 &=\prod_{r=n-d+1}^{n}(1-\rho_r)\\
 &\le\exp\!\left(-\sum_{r=n-d+1}^{n}\rho_r\right)
 \le\exp\!\left(-\frac{d}{\sqrt{n+1}+1}\right).
 \end{aligned}
 \tag{9}
\]

The indices in the product are always at least one when it is nonempty.
For \(d=0\) the product is empty and equals one; for \(n=d=0\) both ratio
and exponential are one. No independent-inclusion model was introduced:
the product is an identity between normalizers at different sizes.

If \(D\subseteq[n]\) is random but \(\mathcal G_n\)-measurable, independence
of \(U_n\) from \(\mathcal G_n\) gives the exact conditional form of (7),
with \(d=|D|\). More generally, conditioning on a completed first block
makes any set selected there fixed, while all future coordinates remain
mutually independent. Hit events formed from separate future coordinates
and that fixed set are conditionally independent. This statement does not
license further conditioning on arbitrary events depending on those future
coordinates.

For \(n+1\le N\), (6) and (9) give the convenient bounds

\[
 \rho_n\ge\frac1{2\sqrt N}\quad(n\ge1),\qquad
 \Pr(U_n\cap D=\varnothing)\le e^{-d/(2\sqrt N)},
 \tag{10}
\]

because \(\sqrt{n+1}+1\le\sqrt N+1\le2\sqrt N\).
The same avoidance bound holds conditionally as just specified.

## 4. A symbolic Bernoulli lower-tail lemma

Let \(X\) be a sum of finitely many independent, not necessarily identically
distributed, Bernoulli variables with mean \(\mu\ge a>0\). Then

\[
 \Pr(X<a/2)\le e^{-a/8}.
 \tag{11}
\]

For completeness, the elementary inequality
\(e^{-x}\le1-x+x^2/2\) for \(x\ge0\) follows by differentiating the difference
twice, using its zero value and zero first derivative at zero.
At \(x=1/2\) this gives \(e^{-1/2}\le5/8\).
If the Bernoulli parameters are \(p_r\), independence and \(1-y\le e^{-y}\)
give

\[
 \mathbb E e^{-X/2}
 =\prod_r\{1-p_r(1-e^{-1/2})\}
 \le e^{-3\mu/8}.
\]

Markov's inequality therefore bounds
\(\Pr(X<a/2)\) by
\(e^{a/4}\mathbb E e^{-X/2}\le e^{a/4-3\mu/8}\le e^{-a/8}\).
The same calculation works under a conditioning sigma-field when the
Bernoulli variables are conditionally independent and their conditional
mean is at least \(a\). This is a symbolic estimate, not a numerically
evaluated tail.

## 5. Three-edge comparison of separated pairs

Fix \(\delta\in(0,1)\), an integer \(N\ge N_0(\delta):=\lceil4/\delta\rceil\),
and labels \(1\le i<j\le N\) with gap \(s=j-i\ge\delta N\). Define

\[
 L=\left\lfloor\frac{s-1}{2}\right\rfloor,\qquad
 A=\{i+1,\ldots,i+L\},\qquad
 B=\{i+L+1,\ldots,i+2L\}.
 \tag{12}
\]

Since \(s\) is an integer and \(\delta N\ge4\),

\[
 L\ge\frac{s-2}{2}\ge\frac{\delta N}{4},
 \qquad 2L\le s-1.
 \tag{13}
\]

Thus these are disjoint consecutive blocks strictly between \(i\) and
\(j\). This is the only lower-size requirement for the construction.
No separated-pair estimate is asserted for \(N<N_0(\delta)\); the trivial
probability bound one suffices for those finitely many sizes.

### First block: many direct successors

Let

\[
 D=\{h\in A:i\in U_{h-1}\},\qquad X=|D|.
\]

Its indicators are independent because their heads are distinct births,
and (10), (13) imply

\[
 \mathbb E X\ge\frac{L}{2\sqrt N}\ge\frac{\delta\sqrt N}{8}.
\]

Set \(G_1=\{X\ge\delta\sqrt N/16\}\). By (11),

\[
 \Pr(G_1^c)\le e^{-\delta\sqrt N/64}.
 \tag{14}
\]

Every vertex of \(D\) has a direct edge from \(i\).
The set \(D\) and event \(G_1\) are \(\mathcal G_{i+L}\)-measurable.

### Second block: a linear number of two-edge descendants

Condition on \(\mathcal G_{i+L}\). The set \(D\) is now fixed, and the draws
with heads in \(B\) remain independent of this sigma-field and of one
another. On \(G_1\), for each \(k\in B\), (9)–(10) imply

\[
 \begin{aligned}
 \Pr(U_{k-1}\cap D\ne\varnothing\mid\mathcal G_{i+L})
 &\ge1-\exp\!\left(-\frac{|D|}{\sqrt k+1}\right)\\
 &\ge1-e^{-\delta/32}
 =:p_\delta>0.
 \end{aligned}
 \tag{15}
\]

Let
\(E=\{k\in B:U_{k-1}\cap D\ne\varnothing\}\) and \(Y=|E|\).
Conditional on \(\mathcal G_{i+L}\), the defining hit indicators depend on
distinct future coordinates and hence are independent. On \(G_1\), their
conditional mean is at least \(Lp_\delta\ge\delta p_\delta N/4\).

With \(G_2=\{Y\ge\delta p_\delta N/8\}\), (11) gives, on \(G_1\),

\[
 \Pr(G_2^c\mid\mathcal G_{i+L})
 \le e^{-\delta p_\delta N/32}.
 \tag{16}
\]

In particular \(\Pr(G_1\cap G_2^c)\) is at most the same deterministic
bound, by conditional expectation. Every vertex of \(E\) is connected
from \(i\) by a two-edge path through some vertex of \(D\).

### Final birth: hit the second-block descendant set

Both sets and both preceding success events are
\(\mathcal G_{j-1}\)-measurable, since \(i+2L<j\). The draw \(U_{j-1}\)
remains independent of that entire sigma-field. On \(G_1\cap G_2\),

\[
 \begin{aligned}
 \Pr(U_{j-1}\cap E=\varnothing\mid\mathcal G_{j-1})
 &\le\exp\!\left(-\frac{|E|}{\sqrt j+1}\right)\\
 &\le e^{-\delta p_\delta\sqrt N/16}.
 \end{aligned}
 \tag{17}
\]

A hit supplies \(i\to h\to k\to j\) with \(h\in D\), \(k\in E\), so
\(i\prec j\). No assumption about independence between the two success
events or between different candidate paths is needed.

### Combined finite bound

If \(i\nprec j\), either \(G_1\) failed, or \(G_1\) held and \(G_2\)
failed, or both held and the final hit failed. Taking expectations in
(16)–(17) and adding (14) proves

\[
 \boxed{
 \Pr(i\nprec j)
 \le e^{-\delta\sqrt N/64}
    +e^{-\delta p_\delta N/32}
    +e^{-\delta p_\delta\sqrt N/16},
 \quad p_\delta=1-e^{-\delta/32}.
 }
 \tag{18}
\]

All count thresholds are real thresholds for integer-valued variables;
no unmentioned floors are needed. The only explicit block floor is (12).
All constants depend only on the fixed \(\delta\). Because labels increase
along every order relation, \(i\nprec j\) for \(i<j\) is precisely
incomparability, not the possibility of the reverse order.

## 6. Summable pair union and almost-sure separated comparability

For fixed \(\delta\), let \(F_N(\delta)\) be the event that some pair
\(i<j\le N\) with \(j-i\ge\delta N\) is incomparable. There are at most
\(N^2\) candidate pairs, so (18) and the union bound give

\[
 \Pr(F_N(\delta))\le N^2
 \left(
 e^{-\delta\sqrt N/64}
 +e^{-\delta p_\delta N/32}
 +e^{-\delta p_\delta\sqrt N/16}
 \right),\qquad N\ge N_0(\delta).
 \tag{19}
\]

For any fixed \(c>0\), the series
\(\sum_{N\ge1}N^2e^{-c\sqrt N}\) converges. Indeed, grouping
\(k^2\le N<(k+1)^2\) bounds each group by

\[
 (2k+1)(k+1)^4e^{-ck},
\]

and the resulting polynomial-times-geometric series converges.
The terms \(N^2e^{-cN}\) are summable as well (or are bounded by the same
square-root-exponential terms for \(N\ge1\)).
Thus (19) is summable. The finitely many smaller sizes do not affect this.

The first Borel–Cantelli lemma proves that, for every fixed
\(\delta\in(0,1)\), almost surely there is a finite random threshold after
which every pair with gap at least \(\delta N\) is comparable. There is no
independence assertion between different pair events or different sizes.

This is a probability-one statement for each fixed \(\delta\), not a
uniform finite threshold over all \(\delta>0\). The next step uses only a
countable intersection.

## 7. Intrinsic incomparable fraction tends to zero

Intersect the probability-one events of section 6 over the countable
sequence \(\delta=1/m\), \(m\ge2\). Fix a history in that intersection and
one such \(\delta\). For all sufficiently large \(N\), every incomparable
pair has positive integer gap less than \(\delta N\). Put

\[
 L_N=\min\{N-1,\lceil\delta N\rceil-1\}.
\]

Counting pairs with those possible gaps gives

\[
 \begin{aligned}
 I(P_N)
 &\le\sum_{g=1}^{L_N}(N-g)
 =NL_N-\frac{L_N(L_N+1)}2\\
 &\le N(\lceil\delta N\rceil-1)
 \le\delta N^2.
 \end{aligned}
 \tag{20}
\]

For \(N\ge2\), this implies
\(\eta(P_N)\le2\delta N/(N-1)\) eventually, and hence
\(\limsup_N\eta(P_N)\le2\delta\).
Letting \(\delta=1/m\downarrow0\), with \(\eta\ge0\), proves (1).

The countable-intersection argument does not say that each finite order is
total, nor does it find a chain containing almost all vertices. Pair-density
one and sublinear maximum-chain cardinality are distinct properties. Thus
the result and the accepted \(O(\sqrt N)\) height theorem can hold for the
same law. Height alone was not used to infer the pair-density limit:
sections 3–6 supply an independent argument from the subset law.

## 8. A deterministic diagnostic for a separately declared target class

This section is conditional on a new, explicit premise about a fixed target
class; it is not a redefinition of any existing target class.

Let \(\mathcal C\) be a fixed isomorphism-closed class of finite orders
containing the empty order. Declare constants

\[
 0<\epsilon\le1,\qquad m_0\in\mathbb N,\quad m_0\ge2,
\]

such that every \(Q\in\mathcal C\) with \(m=|Q|\ge m_0\) satisfies

\[
 I(Q)\ge\epsilon\binom m2.
 \tag{21}
\]

Neither \(\epsilon\), \(m_0\), nor the class may be weakened with increasing
sample size in the following conclusion. Induced-suborder closure of
\(\mathcal C\) is not required.

For any finite order \(P\), define largest retained size and vertex-deletion
distance by

\[
 r_{\mathcal C}(P)
 =\max\{|W|:W\subseteq V(P),\ P[W]\in\mathcal C\},
 \qquad
 d_{\mathcal C}(P)=|P|-r_{\mathcal C}(P).
 \tag{22}
\]

The empty-order convention makes this maximization feasible even if no
nonempty induced order qualifies. If \(P\) is empty, set both quantities
and the normalized deletion fraction to zero. For \(|P|\ge1\), the latter
is \(d_{\mathcal C}(P)/|P|\).

Here \(P[W]\) means the induced restriction of the **already defined order**.
Comparabilities among retained vertices remain even if a generating DAG
path used deleted vertices. Deleting DAG vertices and recomputing its
reachability would be a different operation and would not justify the
following inequality.

For every retained \(W\), incomparabilities among its vertices are exactly
their old incomparabilities, so

\[
 I(P[W])\le I(P).
\]

If \(m=|W|\ge m_0\) and \(P[W]\in\mathcal C\), (21) implies
\(\epsilon m(m-1)/2\le I(P)\). Solving this quadratic and respecting the
integer size gives

\[
 m\le
 \left\lfloor\frac{1+\sqrt{1+8I(P)/\epsilon}}2\right\rfloor.
\]

If \(m<m_0\), instead \(m\le m_0-1\). Define

\[
 B_{\epsilon,m_0}(I)
 =\max\left\{m_0-1,\;
 \left\lfloor\frac{1+\sqrt{1+8I/\epsilon}}2\right\rfloor\right\}.
\]

Combining the cases proves the deterministic bounds

\[
 \boxed{
 r_{\mathcal C}(P)
 \le\min\{|P|,B_{\epsilon,m_0}(I(P))\},
 \qquad
 d_{\mathcal C}(P)
 \ge\max\{0,|P|-B_{\epsilon,m_0}(I(P))\}.
 }
 \tag{23}
\]

These are bounds, not attainability claims. They include \(I(P)=0\) and
small retained sets, without assuming that \(\mathcal C\) contains every
one-point or other small order.

For any sequence of \(N\)-vertex orders with \(I(P_N)=o(N^2)\),
\(B_{\epsilon,m_0}(I(P_N))/N\to0\): the fixed term vanishes after division by
\(N\), and the square-root term divided by \(N\) tends to zero.
Thus

\[
 \boxed{
 \frac{r_{\mathcal C}(P_N)}N\longrightarrow0,\qquad
 \frac{d_{\mathcal C}(P_N)}N\longrightarrow1.
 }
 \tag{24}
\]

For the factorial-subset law, (1) implies \(I(P_N)=o(N^2)\) almost surely,
so (24) holds almost surely for every separately declared fixed class
satisfying (21). It rules out approximation by retaining all but \(o(N)\)
vertices in such a class; indeed, even a fixed positive retained fraction
is eventually impossible.

This is a diagnostic under the density premise (21). It does not establish
that the previous dense bounded-aspect Ferrers class has that premise,
does not change its constraints, and does not turn an isomorphism-invariant
finite-order obstruction into a physical-geometry exclusion.

## 9. What is closed, and what is not

The bounded uncertainty is resolved affirmatively: this fixed optional
factorial-subset law becomes almost totally ordered **in pair density**,
despite its sublinear-height upper bound. The rigorous negative diagnostic
is the conditional induced-target obstruction (23)–(24).

This does not invalidate the law's accepted positivity, normalization,
marked equivariance, complete diamonds, consistent all-size realization
or height theorem. It separates two different structural tests. Passing
the height requirement alone did not establish target approximation.

The scope remains narrow:

- No new growth law, coefficient choice, optimizer or continuation is
  introduced. All probabilities come from the accepted law (2).
- The weights are optional, not a DET-forced selector. No primitive-input
  bridge or full QM reconstruction is claimed.
- The quantum PSD payload and binary record marks remain in the declared
  process. They are passive/independent here; the pair-density observable
  does not derive their dynamics or replace the full mapping by order alone.
- The diagnostic concerns the record-producing order. It does not equate
  that order with all live relational activity.
- No physical dimension, metric, manifold approximation, gravity, mass,
  empirical discriminator, readout/preparation model or application
  benchmark is established or ruled out.
- All proof steps are manual symbolic arguments. No probability or tail
  was numerically evaluated; no sample histories, scientific executor,
  optimizer, simulation, experiment or public-data acquisition was used.

No successor, new lettered gate, protocol expansion or repository action
is selected by this packet. It ends with the theorem candidate, conditional
target diagnostic and four frozen artifacts.

## 10. Exact source and review provenance

The public exposition dependencies and their scientific roles are:

| Public source | Scientific role |
| --- | --- |
| [FACTORIAL_SUBSET_HEIGHT_LAW.md](FACTORIAL_SUBSET_HEIGHT_LAW.md) | Fixed optional from-empty factorial-subset process, all-size admissibility, DAG representation and sublinear intrinsic height; native predecessor in the original source set. |
| [HEIGHT_DRIFT_LAW_SELECTION.md](HEIGHT_DRIFT_LAW_SELECTION.md) | Complete height drift, actual-history tracking and distinct convergence modes; height control alone is not target approximation. |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Declared marked-order model, passive PSD payload and complete structural constraints; historical finite-prefix scope. |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Optional selected laws versus structural identities, arbitrary-prefix preservation and coordinate-gauge limits. |
| [HALF_SCALE_HEIGHT_GROWTH.md](HALF_SCALE_HEIGHT_GROWTH.md) | Linear intrinsic height under a different optional selected law; no universal law conclusion. |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Earlier fixed target screen and its Ferrers scope; no positive incomparable-density premise for that target is supplied here. |

The source-author read six literal manuscripts and two literal provenance
records in the assigned source set. Full actual native captures, hash/byte
checks and pin joins remain in the private source record. Fresh bodies were
joined exactly to already-consumed complete bodies or prefixes; the only
new manuscript text in those comparisons was the two appended neutral-support
sections, both displayed and consumed. No linked source originals, archives,
extra adjudication members, datasets, source checkers or Git paths were
followed in that process. This is the recorded source-author capture account,
not a fresh audit of linked originals by the derivative preparer.

The native factorial-subset source preserves its historical pending header.
Its supplied later adjudication accepts the optional all-size factorial-subset
height law, with a matching exact subject hash and byte count. That later
adjudication establishes the predecessor's supplied acceptance status.
Its link above is the public derivative, not a claim that the native original
was part of the five public snapshots in the original source set. Review of
this ordering-fraction manuscript is recorded separately; preparation of this
derivative does not provide its native acceptance.

The five public exposition copies are attributed by the supplied pin record
to a public source commit. This is pinned metadata, not independent Git or
network verification. Their historical statements that earlier finite-prefix
results did not establish sublinear height are not rewritten; the later
accepted all-size result belongs to its own law. Current public navigation
can include later appended history, distinct from those original snapshots.

The original manual-worker account is retained:

Two independent manual workers reviewed supplied mathematical context.
One checked the marginal/avoidance route, three-edge construction, filtration,
constants, summability and intrinsic pair-density conclusion. The other
checked the marginal/avoidance identities, conditional-use restrictions,
fraction counting and deterministic target diagnostic; it did not claim
an independent proof of the three-edge step. Neither worker read sources
or executed mathematical programs.

The original distinction between evidence categories and limits is retained:

Worker-reported supported usage observations are labelled separately from
root-direct observations. Full native source/manuscript captures are
distinguished from metadata-only summaries of own-receipt readbacks.
These checks do not constitute proof-assistant verification or native
acceptance. Historical custody failures, actual protected validation and
the RET-only pause remain untouched. No clock, book or retired-gravity
work is performed.

The worker summaries and usage transcriptions are supplied-context reports,
not direct coordinator observations or source audits. The two workers'
different proof-review scopes remain distinct. Separate read/hash observations
do not establish atomic identity or reconstruct original custody, and current
matches do not repair earlier source, execution or receipt failures.

The author also recorded a nonexecuting administrative parse failure while
preparing a TeX spacing correction. The call failed before its intended edits
or stores ran; corrected string quoting was followed by the authorized
formatting edit and readback. This is a model-observed administrative failure
and recovery, not a native shell receipt or a mathematical execution.

All nine scientific sections above retain the source-author's manual symbolic
construction and its stated limitations. References there to the theorem
candidate and four frozen artifacts describe the original source packet.
Later independent native and editorial review remain separate from that
construction. A final publication review record is conditional on the separate
native, editorial and root acceptance gates; the preparer does not adjudicate
the theorem or supply a proof-assistant certificate.

Private identifiers, exact paths, hashes, timestamps, receipt filenames,
tool/account metadata and private adjudication records are withheld. Exact
original text and correspondence remain local. Public links identify
mathematical dependencies, not executable private-source custody. No numerical
tail evaluation, scientific execution, data acquisition, experiment, protected
validation or physical readout is supplied or authorized. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public evidence boundary.
