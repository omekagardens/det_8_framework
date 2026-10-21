# A factorial-power family of optional growth laws

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: fixed positive integer exponents, the declared scalar/passive
marked-order model, and the already fixed dense bounded-aspect Ferrers target.
No scientific execution or numerical tail evaluation.

## 1. Family theorem and quantifiers

For each **fixed integer** \(q\ge1\), define

\[
 Z_{n,q}=\sum_{k=0}^{n}\frac{\binom nk}{(k!)^q},\qquad
 \Pr_q(U_n=U)=\frac1{(|U|!)^q Z_{n,q}},\quad U\subseteq[n].
 \tag{1}
\]

The subsets are independent at distinct births. Starting from empty,
vertex \(n+1\) has strict past \(\downarrow_{P_n}U_n\), an independent fair
immutable bit, and the declared passive PSD payload map. The exponent \(q\)
does not depend on size, marks, history or observations.

Put

\[
 B=q+1,\qquad \alpha=1/B,\qquad \beta=1-\alpha.
\]

Under the probability measure of each such fixed law:

\[
 \boxed{\limsup_{N\to\infty}\frac{H_N}{N^\alpha}
        \le \frac{\mathrm e}{\alpha}=\mathrm e(q+1)
        \quad\text{almost surely},}
 \tag{2}
\]

\[
 \boxed{\frac{I(P_N)}{\binom N2}\longrightarrow0
        \quad\text{almost surely},}
 \tag{3}
\]

and, for each separately fixed dense occupancy/aspect Ferrers target
\(\mathcal T_{\nu,A}\),

\[
 \boxed{\frac{R_{\nu,A}(P_N)}N\longrightarrow0,\qquad
        \frac{D_{\nu,A}(P_N)}N\longrightarrow1
        \quad\text{almost surely}.}
 \tag{4}
\]

Here height \(H_N\) is maximum chain cardinality, \(I(P)\) counts unordered
pairs of distinct incomparable vertices, \(R_{\nu,A}\) is largest induced
retained target size, and \(D_{\nu,A}=|P|-R_{\nu,A}\).
Define the incomparable fraction to be zero at sizes zero and one.
Deletion conventions and the target are stated precisely in section 7.

The theorem also proves complete positive normalized marked admissibility
and an all-size from-empty realization. Section 8 shows that changing \(q\)
changes an intrinsic branch-probability ratio, so this is a family of
different optional laws, not a relabelling or paired coordinate gauge.

The exponent in (2) is a proved **upper-bound exponent**, not an asserted
exact height growth exponent. No matching lower bound or sharp constant
is proved. Statements (2)–(4) are for each fixed \(q\) under its own law;
there is no uniform assertion when \(q\) grows with \(N\), no unspecified
joint coupling across exponents, and no conclusion for every admitted
kernel.

## 2. Complete marked admissibility

For a finite parent order \(P\) of size \(n\), with immutable marks \(r\),
let \(S\) be an individual ideal, \(s=|S|\), and
\(m=|\operatorname{Max}(S)|\), with maxima taken in the induced ideal.
The elementary generator characterization is

\[
 \downarrow_P U=S
 \quad\Longleftrightarrow\quad
 \operatorname{Max}(S)\subseteq U\subseteq S.
 \tag{5}
\]

Indeed, closure equality requires \(U\subseteq S\), and a maximal point
of \(S\) can lie below a selected point in \(S\) only if it itself is
selected. Conversely, every point of a finite ideal lies below a maximal
point of that ideal. This also covers the empty ideal.

There are \(\binom{s-m}{k-m}\) generators of size \(k\), so

\[
 \pi_q(P,r,S)=\frac{L_q(s,m)}{Z_{n,q}},\qquad
 L_q(s,m)=\sum_{k=m}^{s}\frac{\binom{s-m}{k-m}}{(k!)^q}.
 \tag{6}
\]

These are probabilities for **individual ideals**, not isomorphism classes
of children. The closure fibers partition all subsets of the parent, hence

\[
 \sum_{S\in\operatorname{Id}(P)}L_q(|S|,|\operatorname{Max}(S)|)
 =\sum_{U\subseteq[n]}\frac1{(|U|!)^q}=Z_{n,q}.
\]

Thus every row is normalized. Every ideal has the generator
\(\operatorname{Max}(S)\), so every ideal probability is strictly positive.
The conventions \(0!=1\), \(Z_{0,q}=L_q(0,0)=1\) give the only first-birth
ideal probability one and its two marked branch probabilities \(1/2\).
At any nonempty parent the empty ideal has probability \(1/Z_{n,q}\).

Relabelling preserves downward closure, cardinalities and induced maxima,
which proves marked equivariance. The kernel ignores all old marks, so
it satisfies the declared proper-precursor restriction on mark dependence.
Its allowed structural dependence includes parent cardinality and the
induced precursor order; no stronger unspecified structural locality
axiom is claimed.

For any two ideals \(S,T\) of a common \(n\)-vertex parent \(C\), compare
incomparable births whose second precursor excludes the other newborn.
The induced order on each old precursor is unchanged by the first birth.
Consequently, writing \(L_q(S)\) for its numerator,

\[
 \pi_q(C,S)\pi_q(C+S,T)
 =\frac{L_q(S)L_q(T)}{Z_{n,q}Z_{n+1,q}}
 =\pi_q(C,T)\pi_q(C+T,S).
 \tag{7}
\]

This includes empty precursors, overlaps, containment, \(S=T\), and
full-first precursors. When a full old precursor becomes proper after
the other birth, its induced maxima and numerator remain unchanged.
Using global parent maxima instead would not be the kernel in (6).

Each newborn bit is fair. For every assignment of both bits, the two
routes act on every fixed-carrier complex PSD payload \(X\) as the same
full map

\[
 X\longmapsto
 \frac{L_q(S)L_q(T)}{4Z_{n,q}Z_{n+1,q}}X.
 \tag{8}
\]

This is equality of maps, not only equality of traces or selected entries.
At \(X=0\) both maps output zero; the classical kernel is independently
defined and involves no division by a zero trace.

Finally, for every \(n\ge0\) take the finite coordinate space
\(2^{[n]}\times\{0,1\}\) with probabilities
\(1/[2(|U|!)^qZ_{n,q}]\), and take their countable independent product.
Recursively forming the downward-closure past gives consistent finite
histories and an all-size law from empty. Conditional on the full prior
marked history, the next coordinate retains its law, yielding exactly
\(\pi_q(P,r,S)/2\) for each ideal-and-bit branch.

This is not just a collection of normalized finite rows. Every allowed
finite branch/cylinder is positive, but an individual infinite history
need not have positive mass. This construction does not preserve an
arbitrary previously fixed prefix or splice into older coefficient choices.

## 3. Upper and lower selection marginals

Let

\[
 w_{n,q}(k)=\frac{\binom nk}{(k!)^q}
 =\frac{n!}{(k!)^{q+1}(n-k)!},\quad
 K_n=|U_n|,\quad \mu_n=\mathbb E_q K_n.
\]

The cardinality law is \(w_{n,q}(k)/Z_{n,q}\); the binomial multiplicity
must not be omitted from the per-subset law (1).

For \(1\le k\le n\), factorial cancellation gives

\[
 k^{q+1}w_{n,q}(k)=(n-k+1)w_{n,q}(k-1).
\]

Summation and the index change \(j=k-1\) yield

\[
 \boxed{\mathbb E_q K_n^{q+1}+\mathbb E_q K_n=n.}
 \tag{9}
\]

The missing \(j=n\) term in the factor \(n-j\) is zero. Convexity then
gives \(\mu_n^{q+1}\le\mathbb E_qK_n^{q+1}\le n\), hence

\[
 \mu_n\le n^\alpha,\qquad
 \rho_{n,q}:=\Pr_q(i\in U_n)=\frac{\mu_n}{n}\le n^{-\beta}
 \quad(n\ge1),
 \tag{10}
\]

where exchangeability justifies the marginal for any specified old vertex.

For a lower bound, the adjacent-weight identity also gives, for \(0\le k<n\),

\[
 \frac{n-k}{(k+1)^q}w_{n,q}(k)=(k+1)w_{n,q}(k+1).
\]

The numerator makes the \(k=n\) term zero. Summing gives the exact identity

\[
 \mu_n+\mathbb E_q\!\left[\frac{K_n}{(K_n+1)^q}\right]
 =n\,\mathbb E_q[(K_n+1)^{-q}].
 \tag{11}
\]

For \(q\ge1\), \(0\le K/(K+1)^q\le1\), and
\(x\mapsto(x+1)^{-q}\) is convex for \(x\ge0\).
Jensen's inequality therefore implies

\[
 \mu_n+1\ge\frac{n}{(\mu_n+1)^q},
 \qquad \mu_n\ge n^\alpha-1.
 \tag{12}
\]

The size-zero and size-one subset terms also give \(Z_{n,q}\ge1+n\).
For \(n\ge1\),

\[
 \mu_n\ge\Pr_q(K_n\ge1)=1-\frac1{Z_{n,q}}
 \ge\frac{n}{n+1}\ge\frac12.
\]

If \(n^\alpha\ge2\), (12) yields \(\mu_n\ge n^\alpha/2\).
If \(n^\alpha<2\), the last bound yields \(\mu_n>n^\alpha/4\).
In particular the convenient all-size estimates are

\[
 \boxed{\frac14n^\alpha\le\mu_n\le n^\alpha,\qquad
 \frac1{4n^\beta}\le\rho_{n,q}\le\frac1{n^\beta}
 \quad(n\ge1).}
 \tag{13}
\]

There is no large-parent-size threshold hidden in (13). At \(n=0\),
\(K_0=\mu_0=0\), and (9), (11) remain valid. No \(\rho_{0,q}\) is defined
by division by zero. Independence within a subset has not been used.

## 4. Exact avoidance and valid conditional use

For a fixed \(D\subseteq[n]\), \(d=|D|\), the total weight of avoiding
subsets is \(Z_{n-d,q}\). Hence

\[
 \Pr_q(U_n\cap D=\varnothing)=\frac{Z_{n-d,q}}{Z_{n,q}},
 \qquad
 \frac{Z_{r-1,q}}{Z_{r,q}}=1-\rho_{r,q}\quad(r\ge1).
 \tag{14}
\]

For \(n\ge1\), telescoping and (13) imply

\[
 \begin{aligned}
 \frac{Z_{n-d,q}}{Z_{n,q}}
 &=\prod_{r=n-d+1}^{n}(1-\rho_{r,q})\\
 &\le\exp\!\left(-\sum_{r=n-d+1}^{n}\rho_{r,q}\right)
 \le\exp\!\left(-\frac{d}{4n^\beta}\right).
 \end{aligned}
 \tag{15}
\]

The product is an identity between different-size normalizers, not
independence of inclusion indicators in a single draw. For \(d=0\) it is
empty and equals one. At \(n=d=0\), the ratio is one; the expression with
\(n^\beta\) in the denominator is not used.

Use the auxiliary coordinate filtration

\[
 \mathcal G_n=\sigma(U_0,\ldots,U_{n-1},b_1,\ldots,b_n).
 \tag{16}
\]

If \(D\subseteq[n]\) is \(\mathcal G_n\)-measurable, the exact conditional
probability in (14) is \(Z_{n-|D|,q}/Z_{n,q}\), since \(U_n\) is independent
of that sigma-field. For a fixed horizon \(N\ge1\), any draw with
\(n+1\le N\) consequently obeys

\[
 \Pr_q(U_n\cap D=\varnothing\mid\mathcal G_n)
 \le\exp\!\left(-\frac{|D|}{4N^\beta}\right).
 \tag{17}
\]

This horizon form also covers \(n=d=0\).

After conditioning at the end of a completed block, a set determined by
that block is fixed, while subsequent subset coordinates remain mutually
independent with their original laws. Hit indicators involving distinct
future coordinates and that fixed set are therefore conditionally
independent. This independence is not asserted after arbitrary further
conditioning on future-derived events.

Direct selections may not be recoverable from the visible transitive-closure
order, so (16), rather than only the visible history, is used for the block
proof. The final observable will nevertheless be intrinsic to the order.

## 5. Height upper bound

Put a directed edge \(i\to j\) precisely when \(i\in U_{j-1}\).
Induction over births shows that the growing order is the transitive
closure of this increasing-label DAG. Every directed path is a chain.
Conversely, for any chain, join successive chain vertices by directed
paths. Their internal labels lie in disjoint successive label intervals,
so concatenation has no repeated interiors and contains the entire chain.
Thus maximum chain cardinality equals maximum directed-path vertex count.

For a specified increasing \(\ell\)-edge path, each required edge comes
from a distinct birth head, and so its probability is the product of
those \(\ell\) marginal selection probabilities. Define

\[
 A_{N,q}=\sum_{n=1}^{N-1}\rho_{n,q}
 \le\sum_{n=1}^{N-1}n^{\alpha-1}
 \le\int_0^{N-1}x^{\alpha-1}\,dx
 =\frac{(N-1)^\alpha}{\alpha}.
\]

If \(X_{N,\ell}\) counts increasing \(\ell\)-edge paths, there are at most
\(N\) possible starting vertices for each increasing tuple of heads.
In \(A_{N,q}^{\ell}\), each distinct head tuple occurs \(\ell!\) times,
while repeated-index terms are nonnegative. Hence

\[
 \mathbb E_qX_{N,\ell}\le\frac{N A_{N,q}^{\ell}}{\ell!}.
\]

A chain of at least \(\ell+1\) vertices gives an \(\ell\)-edge path
by truncating if necessary. Markov's inequality therefore proves, for
\(N\ge2\) and integer \(\ell\ge1\),

\[
 \begin{aligned}
 \Pr_q(H_N\ge\ell+1)
 &\le\min\left\{1,
 \frac{N((N-1)^\alpha/\alpha)^\ell}{\ell!}\right\}\\
 &\le\min\left\{1,
 N\left(\frac{\mathrm e(N-1)^\alpha}{\alpha\ell}\right)^\ell
 \right\}.
 \end{aligned}
 \tag{18}
\]

For the last step,
\(\log(\ell!)\ge\int_1^\ell\log x\,dx
\ge\ell\log\ell-\ell\), so \(\ell!\ge(\ell/\mathrm e)^\ell\).
For \(\ell\ge N\) the event is actually impossible. Separately,
\(H_0=0,H_1=1\). No independence between different paths is required.

Fix \(c>\mathrm e/\alpha\), set \(\ell_N=\lceil cN^\alpha\rceil\),
and put \(a_c=c\log(\alpha c/\mathrm e)>0\). Then (18) gives

\[
 \Pr_q(H_N\ge\ell_N+1)\le N e^{-a_cN^\alpha}.
 \tag{19}
\]

The tail is summable for each fixed \(B=q+1\). More generally, for
\(a>0\) and \(p\in\{1,2\}\),

\[
 \sum_{N\ge1}N^p e^{-aN^{1/B}}<\infty.
 \tag{20}
\]

To see this without numerical evaluation, group integers with
\(k^B\le N<(k+1)^B\). There are at most \((k+1)^B\) terms in a group;
each has \(N^p\le(k+1)^{pB}\) and \(N^{1/B}\ge k\).
The group sum is bounded by
\((k+1)^{(p+1)B}e^{-ak}\), a summable polynomial-times-geometric sequence.

The first Borel–Cantelli lemma applied to (19) gives
\(H_N\le\lceil cN^\alpha\rceil\) eventually almost surely.
Intersecting these probability-one conclusions over
\(c=\mathrm e/\alpha+1/j\), \(j\ge1\), proves (2). Independence between
different sizes is not needed. We do not assert the stronger exact
eventual inequality \(H_N\le(\mathrm e/\alpha)N^\alpha\).

## 6. Multiblock comparison and vanishing incomparable fraction

### A symbolic conditional lower-tail estimate

For a sum \(X\) of independent Bernoulli variables with mean at least
\(a>0\),

\[
 \Pr(X<a/2)\le e^{-a/8}.
 \tag{21}
\]

Indeed, \(e^{-x}\le1-x+x^2/2\) for \(x\ge0\) follows by twice
differentiating the difference. Thus \(e^{-1/2}\le5/8\).
Writing \(p_r\) for the Bernoulli parameters gives
\(\mathbb E e^{-X/2}\le\exp(-3\mathbb EX/8)\).
Markov's inequality bounds the probability in (21) by
\(\exp(a/4-3\mathbb EX/8)\le e^{-a/8}\).
The calculation is equally valid conditionally when the variables are
conditionally independent and their conditional mean is at least \(a\).

Also, the same elementary exponential inequality gives

\[
 1-e^{-x}\ge x-x^2/2\ge x/2,\qquad 0\le x\le1.
 \tag{22}
\]

### Constants, rounding and placement of the blocks

Fix a separation \(\delta\in(0,1)\). With \(B=q+1\), put

\[
 N_0(q,\delta)=\left\lceil\frac{2(B+1)}{\delta}\right\rceil,
 \qquad
 \gamma=\frac{\delta}{32B},\qquad c_t=\gamma^t
 \quad(0\le t\le B).
 \tag{23}
\]

In particular \(c_0=1\) and \(0<c_B\le c_t\le1\).
For \(N\ge N_0\) and \(1\le i<j\le N\) with
\(s=j-i\ge\delta N\), define

\[
 L=\left\lfloor\frac{s-1}{B}\right\rfloor,\qquad
 A_t=\{i+(t-1)L+1,\ldots,i+tL\},\quad1\le t\le B.
 \tag{24}
\]

The floor inequality and \(\delta N\ge2(B+1)\) imply

\[
 L\ge\frac{s-B-1}{B}\ge\frac{\delta N}{2B},
 \qquad BL\le s-1.
 \tag{25}
\]

All \(B=q+1\) blocks therefore lie strictly between \(i\) and \(j\).
For the finitely many sizes below \(N_0\), only the trivial probability
bound one is used. No other large-size threshold is implicit.

### Descendant sets and the conditional induction

Set

\[
 D_0=\{i\},\qquad
 D_t=\{k\in A_t:U_{k-1}\cap D_{t-1}\ne\varnothing\},
 \quad1\le t\le B.
 \tag{26}
\]

Inductively, each vertex of \(D_t\) is connected from \(i\) by a directed
path of \(t\) edges, and \(D_t\) is \(\mathcal G_{i+tL}\)-measurable.
Define cumulative success events

\[
 E_0=\Omega,\qquad
 E_t=\bigcap_{u=1}^t\{|D_u|\ge c_uN^{u/B}\}.
 \tag{27}
\]

At stage \(t\), condition on \(\mathcal G_{i+(t-1)L}\).
The previous set and success event are measurable there. The coordinates
with heads in \(A_t\) remain mutually independent, retain their original
laws, and are independent of that sigma-field. Every point of \(D_{t-1}\)
is older than every head in \(A_t\), so (17) applies.

On \(E_{t-1}\),

\[
 |D_{t-1}|\ge c_{t-1}N^{(t-1)/B}.
\]

For \(t=1\) this is simply \(|D_0|=1=c_0N^0\).
For each \(k\in A_t\), the conditional hit probability is at least

\[
 1-\exp\!\left(-\frac{c_{t-1}}4N^{(t-B)/B}\right).
\]

Put \(x_t=c_{t-1}N^{(t-B)/B}/4\).
Since \(t\le B\), \(c_{t-1}\le1\) and \(N\ge1\), we have
\(0<x_t\le1/4\). By (22), the hit probability is at least

\[
 \frac{c_{t-1}}8N^{(t-B)/B}.
\]

Conditional on the indicated past, each hit indicator depends only on its
own fresh subset coordinate and the fixed \(D_{t-1}\). These indicators
are therefore conditionally independent. On \(E_{t-1}\), their conditional
mean satisfies

\[
 \begin{aligned}
 \mathbb E_q[|D_t|\mid\mathcal G_{i+(t-1)L}]
 &\ge L\frac{c_{t-1}}8N^{(t-B)/B}\\
 &\ge\frac{\delta c_{t-1}}{16B}N^{t/B}
 =2c_tN^{t/B}.
 \end{aligned}
 \tag{28}
\]

Applying (21) with \(a=2c_tN^{t/B}\), then taking expectations with the
indicator of \(E_{t-1}\), gives

\[
 \Pr_q(E_{t-1}\cap E_t^c)
 \le \exp\!\left(-\frac{c_tN^{t/B}}4\right).
 \tag{29}
\]

The conditioning is refreshed at each completed block; it is not enlarged
by a future-derived event before applying independence. Cumulative success
is used only on the measurable past side of each conditional inequality.

All count thresholds are real thresholds for integer-valued variables.
They are feasible: \(c_tN^{t/B}\le\gamma N
=\delta N/(32B)\le L/16\). Thus no ceiling or hidden lower-size condition
is needed for the thresholds themselves.

### Final independent birth and pair bound

On \(E_B\), there are at least \(c_BN\) vertices in \(D_B\), each reachable
from \(i\). Because \(i+BL<j\), both \(D_B\) and \(E_B\) are
\(\mathcal G_{j-1}\)-measurable. The final coordinate \(U_{j-1}\) is still
independent of that entire sigma-field. Equation (17) implies, on \(E_B\),

\[
 \Pr_q(U_{j-1}\cap D_B=\varnothing\mid\mathcal G_{j-1})
 \le\exp\!\left(-\frac{c_BN^{1/B}}4\right).
 \tag{30}
\]

A hit supplies a path with \(B+1=q+2\) edges from \(i\) to \(j\).
The first-failure decomposition (29), followed by (30), proves

\[
 \begin{aligned}
 \Pr_q(i\nprec j)
 &\le\sum_{t=1}^{B}\exp\!\left(-\frac{c_tN^{t/B}}4\right)
      +\exp\!\left(-\frac{c_BN^{1/B}}4\right)\\
 &\le\boxed{(B+1)\exp\!\left(-\frac{c_BN^{1/B}}4\right)},
 \qquad c_B=\left(\frac{\delta}{32B}\right)^B.
 \end{aligned}
 \tag{31}
\]

The last inequality uses \(c_t\ge c_B\) and \(N^{t/B}\ge N^{1/B}\).
No independence between block-success events or between different paths
is used. Because the order increases birth labels, \(i\nprec j\) with
\(i<j\) means incomparability, not reverse comparability.
Old pair relations are unchanged by later births.

### Summable union and intrinsic pair-density limit

Let \(F_N(\delta)\) be the event that some \(i<j\le N\), with gap at least
\(\delta N\), is incomparable. Union over at most \(N^2\) pairs gives

\[
 \Pr_q(F_N(\delta))
 \le(B+1)N^2\exp\!\left(-\frac{c_BN^{1/B}}4\right)
 \quad(N\ge N_0).
 \tag{32}
\]

For fixed \(q,\delta\), \(B\) and \(c_B>0\) are constants, so (20) with
\(p=2\) proves summability. Borel–Cantelli implies that, for each fixed
\(\delta\), all such separated pairs are comparable for every sufficiently
large \(N\), almost surely. No independence across pairs or sizes is
assumed.

Intersect over the countable sequence \(\delta=1/m\), \(m\ge2\).
On this probability-one intersection, for each such \(\delta\) and all
sufficiently large \(N\), every incomparable pair has positive integer
gap less than \(\delta N\). Counting at most
\(\lceil\delta N\rceil-1\) possible later labels for each initial vertex,

\[
 I(P_N)\le N(\lceil\delta N\rceil-1)\le\delta N^2.
\]

It follows that
\(\limsup_N I(P_N)/\binom N2\le2\delta\). Letting \(\delta=1/m\downarrow0\)
proves (3), with the zero/one-size convention already stated.

This establishes the required family stochastic premise, rather than
assuming that the two-block \(q=1\) proof applies unchanged. Pair-density
convergence does not assert eventual total order or the existence of a
chain containing almost all vertices, and it is compatible with (2).

## 7. The fixed dense Ferrers obstruction survives

Keep the same target parameters \(0<\nu\le1\) and \(1\le A<\infty\),
fixed independently of size/history. The target \(\mathcal T_{\nu,A}\)
contains empty and all orders isomorphic to a Ferrers cell diagram with

\[
 \lambda_1=w\ge\cdots\ge\lambda_r\ge1,\qquad
 k=\sum_i\lambda_i\ge\nu rw,\qquad A^{-1}\le r/w\le A,
\]

ordered coordinatewise on its cells \((i,j)\).
Membership requires some qualifying representation, not a unique one.
Occupancy \(\nu\) means diagram occupancy, not event availability.

The exactly accepted DENSE_FERRERS_INCOMPARABILITY_SCREEN.md proves the
deterministic target premise

\[
 I(Q)\ge\epsilon\binom{|Q|}{2}\quad(|Q|\ge m_0),\qquad
 \epsilon=\frac{\nu^4}{128},\quad
 m_0=\left\lceil\frac{16A}{\nu^2}\right\rceil.
 \tag{33}
\]

This source result follows from an occupancy-forced contained rectangle,
aspect-controlled side lengths and crossing-cell counting; it does not
require that the entire diagram be rectangular. We use its exact accepted
premise only after proving (3) for the present family.

Define

\[
 R_{\nu,A}(P)=\max\{|W|:W\subseteq V(P),\;
                  P[W]\in\mathcal T_{\nu,A}\},\qquad
 D_{\nu,A}(P)=|P|-R_{\nu,A}(P).
\]

The empty target ensures feasibility. \(P[W]\) is the induced restriction
of the completed order, not a graph obtained by deleting generator vertices
and recomputing reachability. Therefore \(I(P[W])\le I(P)\).
For a qualifying retained size \(m\ge m_0\), (33) gives
\(\epsilon m(m-1)/2\le I(P)\); for \(m<m_0\), \(m\le m_0-1\).
Consequently, with

\[
 \mathcal B_{\nu,A}(I)
 =\max\left\{m_0-1,\;
 \left\lfloor\frac{1+\sqrt{1+1024I/\nu^4}}2\right\rfloor\right\},
\]

\[
 R_{\nu,A}(P)\le\min\{|P|,\mathcal B_{\nu,A}(I(P))\},\qquad
 D_{\nu,A}(P)\ge\max\{0,|P|-\mathcal B_{\nu,A}(I(P))\}.
 \tag{34}
\]

This is an upper bound on retention, not an attainability claim.
At empty, retained size, deletion distance and normalized deletion fraction
are zero. A singleton qualifies for every \(\nu,A\), so its deletion
distance/fraction are also zero.

By (3), \(I(P_N)=o(N^2)\) almost surely under every fixed member of the
family. All constants in (34) are fixed, so
\(\mathcal B_{\nu,A}(I(P_N))/N\to0\), giving (4).
Thus the obstruction is not specific to \(q=1\): it persists throughout
this optional fixed-integer family despite its changing height upper bounds.

## 8. A genuine optional law choice, not a gauge

Take the two-vertex antichain as parent. Its normalizer is

\[
 Z_{2,q}=3+2^{-q}.
\]

The empty ideal has only its empty generator; the full ideal must select
both vertices. Therefore

\[
 \pi_q(P,\varnothing)=\frac1{3+2^{-q}},\qquad
 \pi_q(P,P)=\frac{2^{-q}}{3+2^{-q}},\qquad
 \boxed{\frac{\pi_q(P,P)}{\pi_q(P,\varnothing)}=2^{-q}.}
 \tag{35}
\]

This is an invariant ratio between intrinsically distinguished ideals.
It changes injectively with \(q\). The parent itself is accessible with
positive probability under every family member: after the first vertex,
the second birth has empty precursor with probability \(1/2\), independent
of \(q\); any specified pair of bits also has positive probability.

A relabelling cannot exchange full and empty ideals. A genuine paired
coordinate gauge preserves actual normalized branch probabilities and
therefore preserves (35). Thus varying \(q\) changes the law, not just
its coordinates or unnormalized presentation.

Every \(q\) nevertheless obeys the same positivity, normalization, locality
and diamond identities in section 2. Those structural constraints do not
select a unique member. The optional factorial-power choice is not derived
from DET principles, and this family theorem is not universal over all
admitted kernels.

The family changes both an exact finite branch statistic and the available
height upper-bound exponent. It does **not** prove that the true asymptotic
height exponents for different \(q\) are different; that would require
additional lower-bound information absent here.

## 9. Scope, dependencies and evidence

The self-contained new mathematical work is:

- the individual-ideal admissibility and all-size product construction;
- exact moment identities, upper/lower marginal bounds and avoidance;
- the finite height tail and fixed-\(q\) almost-sure height upper bound;
- the explicit \(q+1\)-block conditional induction, summable pair union
  and intrinsic incomparable-fraction limit;
- the changing finite invariant in (35).

The deterministic dense Ferrers premise (33) is imported from the exact
accepted DENSE_FERRERS_INCOMPARABILITY_SCREEN.md. The target remains
the one fixed in INTRINSIC_GEOMETRY_TARGET_SCREEN.md section 7.
The \(q=1\) height and ordering-fraction sources identify the predecessor
construction and proof mechanisms; their conclusions are not merely
asserted for \(q>1\). The declared model and distinction between actual
laws and paired gauges are supplied by THEOREM_PACKAGE.md and
LAW_DEPENDENCE.md. No other mathematical source is required.

All quantifiers remain fixed-parameter. In particular, the block number,
\(N_0(q,\delta)\), constants \(c_t\), probability bounds and summability
argument depend on fixed \(q\). There is no statement for \(q=q(N)\) or
a history-dependent exponent. Target parameters \(\nu,A\) are also fixed.
The bounds are conservative, not optimized.

The unrestricted Ferrers class includes arbitrarily large chains with
zero incomparable pairs and therefore lacks the positive-density premise
used here. Since deletion to the unrestricted class can only be easier
than deletion to \(\mathcal T_{\nu,A}\), (4) does not settle that broader
objective. The separate optimizer is neither identified with this family
nor analyzed. No result transfers automatically to other optional laws,
and no arbitrary-prefix preservation is claimed.

The quantum payload remains explicit but passive; the theorem does not
derive a Hilbert space, amplitudes, interference dynamics or full QM.
The record-order diagnostic does not assert that committed records exhaust
live relational activity. There is no metric/manifold reconstruction,
gravity or mass law, physical prediction/observation correspondence,
readout/preparation model or application benchmark. A mathematical
target obstruction is not a physical exclusion.

All proofs are manual symbolic arguments. No mathematical executor,
numerical probability/tail/interval evaluation, optimizer, simulation,
sample history, experiment, dataset acquisition, network research or
protected validation was used. Administrative text assembly, exact
readbacks and native byte/hash observations are not scientific execution.

### Source integrity and review categories

The public exposition dependencies and their scientific roles are:

| Public source | Scientific role |
| --- | --- |
| [DENSE_FERRERS_INCOMPARABILITY_SCREEN.md](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) | Exact accepted deterministic density premise for the fixed dense occupancy/aspect target; native predecessor in the original source set. |
| [ORDERING_FRACTION_OF_FACTORIAL_LAW.md](ORDERING_FRACTION_OF_FACTORIAL_LAW.md) | Predecessor ordering-fraction mechanism and conditional-use distinctions; the family multiblock argument is proved separately. |
| [FACTORIAL_SUBSET_HEIGHT_LAW.md](FACTORIAL_SUBSET_HEIGHT_LAW.md) | Predecessor from-empty construction and height proof mechanism; earlier results are not merely asserted for larger exponents. |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Section 7 fixes the unchanged target definition with existential qualifying representations. |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Declared scalar/passive marked-order model and complete structural constraints. |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Distinction between actual normalized probability laws, optional choices and paired coordinate gauges. |

The source-author read only the six authorized literal manuscript copies
and two literal provenance records. Full native captures, hash/byte
observations and pin joins remain in the private source record. No original
paths, links, archives, source checkers, additional manifest members, Git
paths or protected materials were followed in that process. This is the
source-author's recorded evidence scope, not a fresh audit of linked
originals by the derivative preparer.

The native dense Ferrers source keeps its historical pending header.
The exact later subject-joined adjudication accepts the dense Ferrers
density premise and the factorial-law target obstruction. That is
acceptance of an input theorem, not acceptance of this family manuscript.
The link above is its public derivative; it does not imply that the native
original belonged to the five historical public exposition snapshots.
Those five public copies are attributed by supplied metadata to a public
source commit, without independent Git/network verification. Current public
navigation may contain later appended history, distinct from those source
snapshots.

The original account of source capture and historical limitations is retained:

The changed public ordering-fraction body was fully displayed and consumed.
Other bodies were exact joins to already-consumed complete bodies or
prefixes; new package/law additions were displayed and consumed. The
ordering-fraction source explicitly preserves its prior nonexecuting
administrative parse failure, along with historical capture/custody limits.
Neither current matches nor this family theorem erase or repair them.

The source-author record reports complete fresh captures without truncated
displays. Both literal provenance records were consumed. These capture
statements do not promote metadata-only own-receipt readbacks to full bodies
displayed to the model or repair historical source evidence.

The original manual-worker account is retained:

Three independent manual workers checked supplied mathematical context:
one reviewed admissibility, height and law dependence; one reviewed lower
marginals, avoidance and conditional use; one reviewed the multiblock
induction and pair-density conclusion using the separately checked
avoidance lemma. Their scopes are distinct. None performed source/file
access or scientific execution.

The original evidence-category limitations are retained:

Their full worker-reported supported usage observations are distinct from
root-direct observations. Complete native source/manuscript captures are
distinct from metadata-only summaries of own-receipt readbacks. Separate
read/hash observations are not atomic original-custody proofs. Manual
cross-checks do not constitute proof-assistant verification or native
acceptance. Actual custody requirements, protected validation and the
RET-only pause remain untouched.

Worker mathematical reviews are supplied-context summaries, not verbatim
transcripts. Their full usage responses and time brackets are worker-reported
transcriptions, not direct coordinator tool observations or source audits.
Own-receipt verification summaries remain explicitly metadata-only where
their complete bodies were not displayed to the model.

Sections 1–8 and the mathematical scope and dependency prose in section 9
above retain the source-author's manual symbolic construction verbatim.
Later native and editorial review is recorded separately. Preparation of
this derivative does not accept the theorem or provide machine verification.
Any final publication review record is conditional on the separate native,
editorial and root acceptance gates. Further coordinator decisions remain
separate; no further scientific result is claimed by this derivative.

Private identifiers, exact paths, hashes, timestamps, receipt filenames,
tool/account metadata and private adjudication records are withheld. The
original four-artifact source packet and exact correspondence remain local.
Public links identify mathematical dependencies, not executable private-source
custody. No numerical tail evaluation, scientific execution, data acquisition,
experiment, protected validation or physical readout is supplied or authorized.
RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public evidence boundary.
