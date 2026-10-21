# Quadratic subset penalty: a law-dependence screen

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: one explicit optional fixed law in the declared scalar/passive
marked-order model. Manual symbolic proof only.

## 1. Result and fixed definitions

Fix the sequence, once for all sizes,

\[
 t_k=2^{-k(k-1)/2}\quad(k\ge0),\qquad
 Z_n=\sum_{k=0}^{n}\binom nk t_k,\qquad
 \Pr(U_n=U)=\frac{t_{|U|}}{Z_n},\quad U\subseteq[n].
 \tag{1}
\]

Birth subsets are independent across distinct births. Starting from empty,
vertex \(n+1\) receives strict past \(\downarrow_{P_n}U_n\), an independent
fair immutable bit, and the declared passive PSD payload map. The sequence
in (1) never depends on size, history, marks or observations; only its finite
normalizer depends on parent size.

Let \(H_N\) be maximum chain cardinality in \(P_N\), and let \(I(P_N)\)
count unordered pairs of distinct incomparable vertices. Put
\(H_0=0,H_1=1\), and define incomparable-pair fraction to be zero at sizes
zero and one. Write \(\log_2\) for the base-two logarithm and \(\ln\) for
the natural logarithm.

Under the single all-size measure constructed below,

\[
 \boxed{H_N\le
 \left\lceil16\mathrm e[\log_2(N+1)]^2\right\rceil
 \quad\text{eventually almost surely},}
 \tag{2}
\]

and

\[
 \boxed{\liminf_{N\to\infty}
 \frac{I(P_N)}{\binom N2}\ge\frac1{4096}
 \quad\text{almost surely}.}
 \tag{3}
\]

The probability-one conclusions hold simultaneously. In particular this
strictly positive admitted law has a sublinear height upper bound but
does not have vanishing incomparable-pair fraction. The constants are
conservative. No matching height lower bound, limiting incomparable
constant, sharp threshold or optimal constant is claimed.

This answers an existence/law-dependence question inside the declared
model. It does not derive (1) from DET, change any accepted historical law,
or prove that this process approximates any Ferrers target or geometry.

## 2. Exact individual-ideal kernel and all-size admission

For an individual ideal \(S\) of a finite parent \(P\), let
\(n=|P|,\ s=|S|\), and \(m=|\operatorname{Max}(S)|\), with maxima taken
in the induced ideal, not in the whole parent. Then

\[
 \downarrow_P U=S
 \quad\Longleftrightarrow\quad
 \operatorname{Max}(S)\subseteq U\subseteq S.
 \tag{4}
\]

Closure equality requires \(U\subseteq S\). A maximal point of \(S\)
cannot lie strictly below another selected point of \(S\), so it must itself
be selected. Conversely, every point of a finite ideal lies below one of
its maximal points. This proves (4), including the empty case.

The numerator and normalized ideal probability are therefore

\[
 L(s,m)=\sum_{k=m}^{s}
       \binom{s-m}{k-m}2^{-k(k-1)/2},\qquad
 \pi(P,r,S)=\frac{L(s,m)}{Z_n}.
 \tag{5}
\]

The binomial coefficient counts generators of the specific ideal; these
are probabilities over individual ideals, not child isomorphism classes.
Closure fibers partition all subsets, giving

\[
 \sum_{S\in\operatorname{Id}(P)}
 L(|S|,|\operatorname{Max}(S)|)
 =\sum_{U\subseteq V(P)}t_{|U|}=Z_n.
\]

Every term of (1) is strictly positive, and every ideal has the generator
\(\operatorname{Max}(S)\). Thus all ideal probabilities are positive and
every row is normalized. Here \(t_0=t_1=1,\ Z_0=L(0,0)=1\).
At empty the sole ideal has probability one, and its two bit branches
each have probability \(1/2\). At a nonempty parent the empty ideal has
probability \(1/Z_n>0\).

Relabelling preserves cardinality, induced maxima and downward closure,
so the marked kernel is equivariant. It ignores all old marks and hence
satisfies the declared proper-precursor restriction on mark dependence.
Parent cardinality and the induced precursor order are still allowed
structural inputs; no stronger unprovided structural locality axiom is
asserted.

For any two ideals \(S,T\) of a common parent \(C\), \(|C|=n\), compare
incomparable births, so that the second precursor excludes the other
newborn. The induced order on each old precursor is unchanged after the
first birth. Abbreviating its numerator by \(L(S)\),

\[
 \pi(C,S)\pi(C+S,T)
 =\frac{L(S)L(T)}{Z_nZ_{n+1}}
 =\pi(C,T)\pi(C+T,S).
 \tag{6}
\]

This includes empty ideals, overlap, containment, \(S=T\), and full-first
precursors. An old full precursor becoming proper at the intermediate
parent retains its induced maxima; replacing them with global parent
maxima would be a different kernel.

Each bit is fair and immutable. For every assignment of both newborn bits,
the two routes have the same final marked order under the natural exchange
of newborn labels, and the same full map on every fixed-carrier complex
PSD payload \(X\):

\[
 X\longmapsto\frac{L(S)L(T)}{4Z_nZ_{n+1}}X.
 \tag{7}
\]

This is map equality, not merely trace equality or equality on selected
matrix entries. It includes \(X=0\). The classical probabilities are
defined separately and do not divide by a possibly zero trace. The
one-step maps \(X\mapsto\pi(P,r,S)X/2\) are positive scalar maps, and their
sum over ideals and bits is the identity map.

For each \(n\ge0\), take the finite coordinate space
\(2^{[n]}\times\{0,1\}\) with probabilities \(t_{|U|}/(2Z_n)\).
Their countable independent product supplies an all-size probability
measure. Forming the downward-closure past recursively, from empty, gives
consistent finite marked histories. Conditional on the full prior
coordinate history, the fresh coordinate retains its original law, so
closure-fiber summation yields exactly \(\pi(P_n,r,S)/2\) for an
ideal-and-bit branch. The same kernel holds conditional on the visible
marked history.

Every allowed finite branch/cylinder has positive probability; an individual
infinite history need not have positive mass. This constructs a new law
from empty, not an extension preserving an arbitrary previously fixed
prefix. The supplied quantum carrier remains explicit and passive, not
derived from primitive inputs.

## 3. A logarithmic selection-mean upper bound

Let

\[
 K_n=|U_n|,\quad \mu_n=\mathbb E K_n,\qquad
 w_n(k)=\binom nk2^{-k(k-1)/2}.
\]

Then \(K_n\) has probabilities \(w_n(k)/Z_n\); the binomial multiplicity
must be included. For \(0\le k<n\), direct cancellation gives

\[
 \frac{w_n(k+1)}{w_n(k)}
 =\frac{n-k}{(k+1)2^k}.
 \tag{8}
\]

For \(n\ge1\), set \(m_n=\lceil\log_2(n+1)\rceil\).
The elementary inequality \(2^n\ge n+1\), proved by induction for integers
\(n\ge1\), gives \(1\le m_n\le n\). For \(m_n\le k<n\),

\[
 \frac{w_n(k+1)}{w_n(k)}
 \le\frac{n}{(m_n+1)2^{m_n}}
 \le\frac{n}{(m_n+1)(n+1)}
 \le\frac12.
 \tag{9}
\]

Hence \(w_n(m_n+j)\le2^{-j}w_n(m_n)\) whenever the index exists.
Since \(w_n(m_n)/Z_n\le1\),

\[
 \mathbb E(K_n-m_n)_+
 =\sum_{j=1}^{n-m_n}
   j\,\frac{w_n(m_n+j)}{Z_n}
 \le\sum_{j\ge1}j2^{-j}=2.
\]

The last series identity follows, for example, by writing
\(j=\sum_{a=1}^j1\), interchanging nonnegative sums, and summing two
geometric series. It is symbolic, not a numerical tail evaluation.
Consequently, with \(\log_2(n+1)\ge1\),

\[
 \boxed{\mu_n\le\lceil\log_2(n+1)\rceil+2
 \le\log_2(n+1)+3\le4\log_2(n+1).}
 \tag{10}
\]

Exchangeability under permutations of old labels now gives, for each
specified old vertex,

\[
 \boxed{\rho_n:=\Pr(i\in U_n)=\frac{\mu_n}{n}
 \le\min\left\{1,\frac{4\log_2(n+1)}n\right\},
 \qquad n\ge1.}
 \tag{11}
\]

At \(n=0\), \(K_0=\mu_0=0\); no \(\rho_0\) is defined by division.
Neither (8)–(11) nor any later argument assumes independent selection
indicators within one subset. No lower selection-marginal bound from
the factorial-power family is used.

## 4. Directed paths and the height bound

Put an edge \(i\to j\) precisely when \(i\in U_{j-1}\).
Induction over births shows that \(P_N\) is the transitive closure of this
increasing-label DAG. Every directed path is a chain. Conversely, join
successive vertices of any chain by directed paths. Their interiors have
labels in disjoint successive intervals, so concatenation has no repeated
interiors and contains the chain. Maximum chain cardinality therefore
equals maximum directed-path vertex count.

Write \(G_N=\log_2(N+1)\) and
\(A_N=\sum_{n=1}^{N-1}\rho_n\), with \(A_0=A_1=0\).
For \(N\ge2\),

\[
 \begin{aligned}
 A_N
 &\le4G_N\sum_{n=1}^{N-1}\frac1n
 \le4G_N(1+\ln N)
 \le8G_N^2.
 \end{aligned}
 \tag{12}
\]

The harmonic bound follows by comparison with the integral of \(1/x\).
The last inequality uses \(1\le G_N\) and \(\ln N\le G_N\);
indeed \(\ln2\le1\).

For a fixed increasing \(\ell\)-edge path, the required edges have distinct
birth heads. Its probability is therefore the product of their marginal
probabilities, by independence of distinct subset coordinates.
If \(X_{N,\ell}\) counts such paths, there are at most \(N\) starting
vertices for each increasing tuple of heads. Each distinct head tuple
occurs \(\ell!\) times in the expansion of \(A_N^\ell\), and all other
terms there are nonnegative. Thus

\[
 \mathbb E X_{N,\ell}\le\frac{N A_N^\ell}{\ell!}.
\]

A chain with at least \(\ell+1\) vertices gives an \(\ell\)-edge path
by truncation if necessary. Markov's inequality yields, for
\(N\ge2\) and integers \(\ell\ge1\),

\[
 \begin{aligned}
 \Pr(H_N\ge\ell+1)
 &\le\min\left\{1,\frac{N(8G_N^2)^\ell}{\ell!}\right\}\\
 &\le\min\left\{1,
 N\left(\frac{8\mathrm e G_N^2}{\ell}\right)^\ell\right\}.
 \end{aligned}
 \tag{13}
\]

Here \(\ell!\ge(\ell/\mathrm e)^\ell\) follows from
\(\log(\ell!)\ge\int_1^\ell\log x\,dx
\ge\ell\log\ell-\ell\). If \(\ell\ge N\), the event is impossible;
the separate empty/singleton height conventions still apply.

Choose

\[
 \ell_N=\lceil16\mathrm e G_N^2\rceil.
\]

Since \(\ell_N\ge16\mathrm e G_N^2\) and \(\ell_N\ge4G_N\),
(13) implies

\[
 \Pr(H_N\ge\ell_N+1)
 \le N2^{-\ell_N}
 \le\frac{N}{(N+1)^4}
 \le N^{-3}\quad(N\ge2).
 \tag{14}
\]

This is summable over all integer sizes. The first Borel–Cantelli lemma
proves (2), and in particular

\[
 \limsup_N\frac{H_N}{[\log_2(N+1)]^2}\le16\mathrm e
 \quad\text{almost surely}.
\]

Thus \(H_N/N\to0\) almost surely, since a fixed logarithmic square is
\(o(N)\). No independence between paths or between sizes was used.
The proof supplies an upper bound, not an exact asymptotic height law.

## 5. Summing all paths between fixed endpoints

For fixed \(i<j\), let \(X_{ij}\) count all directed paths from \(i\) to
\(j\). Such a path is uniquely specified by a subset of intermediate
labels \(\{i+1,\ldots,j-1\}\), traversed in increasing order.
For that fixed path, the required edges again have distinct birth heads.
Exchangeability makes the marginal at head \(h\) equal to \(\rho_{h-1}\)
for any specified predecessor, and independence of distinct birth
coordinates makes their product the path probability.

Summing over all choices of intermediate labels gives the exact identity

\[
 \mathbb E X_{ij}
 =\rho_{j-1}\prod_{h=i+1}^{j-1}(1+\rho_{h-1}).
 \tag{15}
\]

The empty intermediate subset contributes the direct edge. If \(j=i+1\),
the product is empty and equals one. There is no \(\rho_0\) because
\(j-1\ge1\).

Comparability \(i\prec j\) is precisely the event \(X_{ij}\ge1\).
Thus

\[
 \Pr(i\prec j)
 \le\min\left\{1,\rho_{j-1}
          \prod_{h=i+1}^{j-1}(1+\rho_{h-1})\right\}
 \le\min\left\{1,\rho_{j-1}
          \exp\left(\sum_{h=i+1}^{j-1}\rho_{h-1}\right)\right\}.
 \tag{16}
\]

This is a first-moment bound, not a product formula for the probability
of a union. Different paths may share heads and edges and are not assumed
independent. Only the edges of one specified path have the distinct-head
property needed for its probability.

## 6. A late-label band with few comparable pairs

For every integer \(N\ge2\), define the auxiliary band and its cardinality

\[
 B_N=\{\lceil31N/32\rceil,\ldots,N\},\qquad
 b_N=N-\lceil31N/32\rceil+1=\lfloor N/32\rfloor+1.
 \tag{17}
\]

The cardinality identity uses
\(\lceil N-x\rceil=N-\lfloor x\rfloor\) for integer \(N\).
If \(b_N<2\), statements about pairs within the band are vacuous.

For any \(i<j\) in \(B_N\), each possible head \(h\) of a path from \(i\)
to \(j\) has

\[
 h-1\ge i\ge N/2,\qquad h\le N.
\]

Therefore (11) gives, including for the final head \(j\),

\[
 \rho_{h-1}\le \frac{8\log_2N}{N}.
 \tag{18}
\]

The number of possible intermediate heads is
\(j-i-1\le N/32\). Consequently

\[
 \sum_{h=i+1}^{j-1}\rho_{h-1}\le\frac{\log_2N}{4}.
\]

Since \(\ln2=\int_1^2x^{-1}\,dx\ge1/2\),

\[
 \exp(\log_2N/4)=N^{1/(4\ln2)}\le N^{1/2}.
\]

Substitution in (16) proves the uniform finite-horizon pair bound

\[
 \boxed{\Pr(i\prec j)\le
 \min\{1,\ 8\log_2N\,N^{-1/2}\}
 \quad(i<j,\ i,j\in B_N).}
 \tag{19}
\]

All generating paths between these endpoints have increasing labels
between \(i\) and \(j\). They cannot leave this interval and return.
Thus (15) counts every possible path, not just paths in an arbitrarily
restricted subgraph. The right side of (19) may be large at small sizes;
the minimum with one and the vacuous-band convention handle those cases.

Let \(C_N\) count unordered comparable pairs within \(B_N\) in the order
\(P_N\). A pair with \(i<j\) cannot satisfy \(j\prec i\), so (19) and
linearity of expectation yield

\[
 \mathbb E C_N
 \le\binom{b_N}{2}\,8\log_2N\,N^{-1/2}
 \le4N^{3/2}\log_2N.
 \tag{20}
\]

No independence between pairs is needed. Markov's inequality now gives

\[
 \Pr(C_N>N^{7/4})
 \le\min\{1,\ 4\log_2N\,N^{-1/4}\}.
 \tag{21}
\]

The threshold is a real threshold for the integer-valued count \(C_N\);
no rounding adjustment is required.

## 7. Dyadic summability and the full intrinsic density liminf

At dyadic horizons \(M=2^r\), \(r\ge1\), (21) implies

\[
 \Pr(C_{2^r}>2^{7r/4})\le4r\,2^{-r/4}.
 \tag{22}
\]

This is summable in \(r\), since it is a polynomial times a geometric
sequence with fixed ratio \(2^{-1/4}<1\). No numerical tail evaluation is
involved. Borel–Cantelli gives

\[
 C_M\le M^{7/4}
 \quad\text{eventually almost surely along dyadic }M.
 \tag{23}
\]

For dyadic \(M\ge32\), \(M/32\) is an integer and
\(b_M=M/32+1\) exactly. Incomparable pairs inside the band are included
among all incomparable pairs in \(P_M\). Hence, on the probability-one
event in (23), for all sufficiently large dyadic \(M\),

\[
 \begin{aligned}
 I(P_M)
 &\ge\binom{M/32+1}{2}-M^{7/4},\\
 \frac{I(P_M)}{M^2}
 &\ge\frac1{2048}+\frac1{64M}-M^{-1/4}.
 \end{aligned}
 \tag{24}
\]

It remains essential to cover every size, not only a subsequence.
For any sufficiently large integer \(N\), choose the unique dyadic \(M\)
such that \(M\le N<2M\).

Old pair relations are preserved by later births. In the DAG description,
a path between two old vertices could not use a newer vertex and return
to an older label. In the recursive order description, each birth extends
rather than changes the old order. In particular an old incomparable
pair stays incomparable, and

\[
 I(P_N)\ge I(P_M).
\]

Because \(\binom N2<2M^2\) and \(I(P_M)\ge0\),

\[
 \begin{aligned}
 \frac{I(P_N)}{\binom N2}
 &\ge\frac{I(P_M)}{2M^2}\\
 &\ge\frac1{4096}+\frac1{128M}-\frac12M^{-1/4}.
 \end{aligned}
 \tag{25}
\]

One may replace the final right side by its maximum with zero.
Taking the liminf through all integer \(N\) proves (3).
This argument uses no independence across horizons, pairs, or paths.
It also does not condition on a future-derived success event before
asserting any coordinate independence.

Birth labels and the bands are auxiliary proof devices. The final
quantity \(I(P_N)/\binom N2\) is intrinsic to the finite order, independent
of its labelling, and (25) controls that full-order observable rather than
just the chosen band. No intrinsic interpretation of the band as a
physical region is required or claimed.

The event proving (2) and the event proving (3) each have probability one
under the same measure from section 2. Their intersection proves the
requested conjunction, not merely separate claims under unrelated laws.

## 8. Distinction from every fixed-integer factorial-power law

For the two-vertex antichain \(A_2\), full and empty ideals each have a
unique generator, so the full/empty probability ratio for (1) is
\(t_2/t_0=1/2\). This coincides with the \(q=1\) factorial-power ratio
and therefore cannot alone establish the required distinction.

Instead use the three-vertex antichain \(A_3\). Its full and empty ideals
again have unique generators, giving

\[
 \boxed{\frac{\pi(A_3,r,A_3)}{\pi(A_3,r,\varnothing)}
 =\frac{t_3}{t_0}=\frac18.}
 \tag{26}
\]

For the accepted family with weights \((k!)^{-q}\), the same intrinsic
ratio is \(6^{-q}\). At \(q=1\), it is \(1/6\ne1/8\).
For every integer \(q\ge2\), it is at most \(1/36<1/8\).
Thus (26) distinguishes this candidate from every fixed integer
\(q\ge1\) in that family.

The antichain parent is accessible with positive probability under each
law: repeatedly choose the empty precursor, whose probability is always
positive, and any fixed assignment of fair bits also has positive
probability. The ratio therefore concerns accessible branches, not an
unreachable hypothetical state.

Full and empty ideals are intrinsically distinguished; a relabelling
cannot exchange them. A paired coordinate gauge preserving actual
normalized branch probabilities preserves their ratio. The distinction
is therefore an actual law difference, not a gauge or a change of
unnormalized notation. No claim about every possible real exponent or
every other admitted law is needed.

The sequence (1) is an additional optional input. Admission to the
declared model and these theorems do not make it DET-forced. Accepted
factorial-power laws are left unchanged, and their own conclusions
remain valid under their own measures.

## 9. What this does and does not close

The earlier accepted fixed-integer factorial-power family has vanishing
incomparable-pair fraction despite sublinear height. The present fixed
law has a logarithmic-squared height upper bound and a strictly positive
almost-sure incomparable-fraction liminf. Consequently, the declared
positivity, normalization, mark locality and diamond constraints do not
force the vanishing-fraction conclusion across all admitted laws.

This is the closed uncertainty: an explicit strictly positive admitted
law can escape that particular necessary obstruction while keeping
sublinear height. It is not an assertion that all geometric obstructions
have disappeared.

The supplied dense Ferrers result has a different logical role: for the
fixed target with occupancy \(0<\nu\le1\) and aspect bound
\(1\le A<\infty\), sufficiently large target members require a positive
incomparable-pair fraction, at least \(\nu^4/128\). Its deletion obstruction
for earlier laws used the additional stochastic fact \(I(P_N)=o(N^2)\).
That stochastic premise is false here by (3), so that argument cannot
simply be transferred to this new law.

It does not follow that the present order has a large qualifying induced
Ferrers suborder. A lower bound on the total number of incomparable pairs
neither identifies their pattern nor supplies an embedding, a retained
suborder, a matching upper bound on deletion distance, or even a limiting
pair fraction. We do not change the target's occupancy/aspect requirements,
infer restricted or unrestricted Ferrers approximation, or analyze the
separate optimizer. Nor is (3) compared as though it determined the actual
density relative to every target's numerical floor.

There is no metric, manifold, dimension or Lorentzian reconstruction,
gravity/mass law, physical prediction, physical discriminator, application
benchmark or observational fit. The proof concerns record-producing
order events; it does not assert that committed records exhaust live
relational activity. The fair marks and passive supplied quantum payload
remain present, but neither their carrier nor amplitudes, interference,
full QM or readout/preparation dynamics are derived.

No matching height lower bound, limiting height coefficient, limiting
incomparable constant, optimal band, sharp transition, universality, or
arbitrary-prefix preservation is claimed. The one fixed law is not
replaced by a size-dependent exponent or an adaptively selected sequence.

## 10. Dependencies, evidence and stop boundary

Sections 2–8 provide the new proof: exact admission, logarithmic marginal
bound, height tail, fixed-endpoint path sum, late-band bound, dyadic
summability, full-sequence intrinsic density liminf, and finite branch
invariant. The final pair-density conclusion is not borrowed from either
the factorial-power family or its lower marginal/multiblock argument.

The six permitted literal sources have the following roles:

- FACTORIAL_POWER_LAW_FAMILY.md is the exactly accepted native predecessor
  against which the distinct optional law and stochastic result are compared.
- DENSE_FERRERS_INCOMPARABILITY_SCREEN.md supplies only the prior
  target-specific necessary-density premise and its logical scope.
- ORDERING_FRACTION_OF_FACTORIAL_LAW.md documents the earlier
  law-specific conclusion and first-moment/conditional distinctions;
  its stochastic conclusion is not applied to (1).
- INTRINSIC_GEOMETRY_TARGET_SCREEN.md fixes the unchanged target and the
  distinction between structural tests and actual induced approximation.
- THEOREM_PACKAGE.md supplies the declared marked-order/passive-payload
  model and structural constraints.
- LAW_DEPENDENCE.md supplies the distinction between actual law choices,
  paired gauges and arbitrary-prefix claims.

The source manuscript was constructed from only those six literal copies
and two literal provenance records. The links below give current public
reader equivalents for those six scientific roles. They do not replace
the original custody evidence or turn public pages into original native
captures.

| Public reader reference | Scientific source role |
| --- | --- |
| [Factorial-power law family](FACTORIAL_POWER_LAW_FAMILY.md) | Accepted native predecessor at source construction; comparison with the distinct optional law and its stochastic result. |
| [Dense Ferrers incomparability screen](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) | Prior target-specific necessary-density premise and its logical scope only. |
| [Ordering fraction of the factorial law](ORDERING_FRACTION_OF_FACTORIAL_LAW.md) | Earlier law-specific conclusion and first-moment/conditional distinctions; its stochastic conclusion is not applied to the new law. |
| [Intrinsic geometry target screen](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Unchanged intrinsic target and the distinction between structural tests and actual induced approximation. |
| [Theorem package](THEOREM_PACKAGE.md) | Declared marked-order/passive-payload model and structural constraints. |
| [Law dependence](LAW_DEPENDENCE.md) | Actual law choices, paired gauges and arbitrary-prefix limitations. |

At source construction, the factorial-power manuscript was the accepted
native predecessor; the other five scientific inputs were public snapshots.
The predecessor retained its historical pending header, while a later
exact subject-joined adjudication recorded its acceptance. That predecessor
acceptance did not accept this manuscript. The supplied metadata attributed
the five public snapshots to a historical publication state; no fresh
Git or network verification of that state was claimed.

The following paragraphs retain the source manuscript’s account of its
own source consumption and manual work. They are historical provenance
statements, distinct from this public derivative’s administrative checks
and any later independent native, editorial or coordinator review.

The changed public dense Ferrers body was fully displayed and consumed.
Unchanged fresh bodies were exactly joined to already consumed complete
bodies; package/law additions were displayed and consumed after exact
prefix joins. Both literal JSON records were fully displayed and consumed.
The ordering-fraction source retains its historical nonexecuting
administrative parse failure and receipt/custody limitations. These
current joins do not erase, reconstruct or repair them.

Three manual workers checked supplied mathematical context only: one
checked the mean and height argument, one checked the band/dyadic proof
assuming the separately verified marginal bound, and one checked
admissibility and the small-parent law distinction. None performed
source/file access or scientific execution. Their full worker-reported
supported usage observations are kept distinct from root-direct captures.
An optional stronger band estimate and an optional sharper height limsup
suggested during review are not used or claimed here.

All proof work was manual symbolic reasoning. No mathematical executor,
numerical probability/tail/interval evaluation, sampling, simulation,
optimizer, benchmark, experiment, dataset/network acquisition or protected
validation was used. Bounded inert text assembly, exact string/readback
comparisons, native hashes and byte counts are administrative checks,
not scientific execution.

Complete native source/manuscript captures are distinguished from
metadata-only summaries of own-receipt readbacks. Separate observations
are not atomic original-custody proofs. Manual cross-checks are not
proof-assistant verification or native acceptance. Actual custody failures,
physical/application separation, and the RET-only pause remain unchanged.

The native manuscript and its three companion provenance, result and freeze
records remain private. Exact local source pins, declared metadata
substitutions, source-tail correspondence and publication checks are retained
separately. Private run identifiers, local paths, content fingerprints and
tool receipts are withheld here. No original source path, linked archive,
additional manifest member, source program, repository history or protected
material was followed in preparing this public derivative.

The source’s manual mathematical construction is distinct from subsequent
independent review. This derivative is a faithful text preparation, not
scientific acceptance, machine proof or public executable custody. Native
acceptance, editorial acceptance, publication and later assignments are
recorded separately by the coordinator; no later result is claimed here.
The original protocol boundaries, physical/application separation and
RET-only pause remain unchanged. See the [publication note](PUBLICATION_NOTE.md)
and [redacted-publication policy](../../coordination/REDACTED_PUBLICATION.md).
