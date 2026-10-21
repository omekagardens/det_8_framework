# Bernoulli-subset law and a Ferrers-retention counterexample

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: one fixed-parameter, from-empty optional law in the declared
scalar/passive marked-order model. No novelty or physical implication claimed.

## 1. Result and the precise universal claim rejected

Fix a real \(p\in(0,1)\), independently of size, marks, history and data.
At every birth independently include each old vertex in a generating subset
with probability \(p\). Take the newborn's strict past to be the downward
closure of that subset, its immutable bit independently fair, and retain
the fixed-carrier arbitrary complex PSD payload by the scalar branch map.

This gives a fully admitted all-size marked law, proved in sections 3–4.
On its single from-empty probability measure,

\[
 \boxed{
 \liminf_{N\to\infty}\frac{H_N}{N}\ge p,\qquad
 \liminf_{N\to\infty}\frac{R_{\mathcal F}(P_N)}N\ge p,\qquad
 \limsup_{N\to\infty}\frac{D_{\mathcal F}(P_N)}N\le1-p
 \quad\text{almost surely},
 }
 \tag{1}
\]

and simultaneously

\[
 \boxed{
 \mathbb E_p I(P_N)\le\frac{1-p}{p^2}N,\qquad
 \frac{I(P_N)}{N^2}\longrightarrow0
 \quad\text{almost surely}.
 }
 \tag{2}
\]

Here height counts chain vertices, \(I\) counts unordered incomparable
pairs, and \(\mathcal F\) is the unrestricted filled coordinatewise
partition-cell class, including empty. Retention and deletion are defined
by induced restriction of the completed order.

Thus the declared admission principles do **not** force negligible
unrestricted Ferrers retention or deletion fraction one. Even the additional
condition of vanishing incomparable-pair density does not force them.
The accepted factorial-power laws have negligible unrestricted retention;
this different admitted law does not. This is actual law dependence within
the stated conditional model, not a statement about every possible DET
formulation or physical spacetime.

There is no conflict with the accepted joint theorem
\(H_N=O(\sqrt N)\) and \(I(P_N)=o(N^2)\Rightarrow R_{\mathcal F}/N\to0\).
The present law violates its height premise almost surely. Its positive
retention witness is a chain, not a dense bounded-aspect two-dimensional
approximation. The original fixed dense target is still obstructed
(section 8).

## 2. Declared model and unchanged diagnostics

A state is a finite order \(P\), an immutable binary marking \(r\), and
an arbitrary complex positive-semidefinite payload \(X\) on a fixed
carrier. An individual ideal \(S\subseteq P\), including empty and full,
is a downward-closed subset. A birth \(P+S\) appends one maximal vertex
with strict past exactly \(S\). Its bit \(b\in\{0,1\}\) is fair and its
branch acts as

\[
 \mathcal B^{P,r}_{S,b}(X)=\frac{\pi_p(P,r,S)}2X.
 \tag{3}
\]

The admission conditions supplied by THEOREM_PACKAGE.md section 1 are
strict positivity of every ideal, complete normalization, marked
equivariance, proper-precursor mark locality, and complete incomparable-birth
diamond equality. The locality condition permits the whole unmarked parent
but only the marks in the selected proper ideal; a full ideal may read all
old marks. It is not a prohibition on unmarked spectators or parent-size
dependence. Fair bits and scalar passivity are declared model assumptions,
not derived here from bare DET primitives.

For a nonempty integer partition \(\lambda_1\ge\cdots\ge\lambda_r\ge1\),
a filled cell order has vertices
\(\{(i,j):1\le i\le r,\ 1\le j\le\lambda_i\}\), ordered coordinatewise.
Let \(\mathcal F\) consist of orders isomorphic to such a diagram and empty.
It is not all dimension-two orders, arbitrary planar subsets, or every
other mathematical use of “Ferrers.”

For finite \(P\),

\[
 R_{\mathcal F}(P)=
 \max\{|W|:W\subseteq V(P),\ P[W]\in\mathcal F\},\qquad
 D_{\mathcal F}(P)=|P|-R_{\mathcal F}(P).
 \tag{4}
\]

The relation in \(P[W]\) is the restriction of the completed order.
Deleting generating-DAG vertices and then recomputing reachability is
a different diagnostic. Empty is feasible, so the maximum exists.
A chain of \(k\) vertices is a one-row filled diagram \(\lambda=(k)\).
Consequently every finite parent obeys

\[
             R_{\mathcal F}(P)\ge H(P).
 \tag{5}
\]

Marks and payload remain in the process; (4) is its unmarked-order
diagnostic, not a replacement for the whole mathematical object.

At \(N=0\), \(H=I=R_{\mathcal F}=D_{\mathcal F}=0\); define normalized
fractions there to be zero. At \(N=1\), \(H=R_{\mathcal F}=1\) and
\(I=D_{\mathcal F}=0\). For \(N\ge2\), incomparable-pair density is
\(I(P_N)/\binom N2\). It is zero by convention at sizes zero and one.
For nonempty \(P\), retained and deletion fractions sum to one.

## 3. Complete individual-ideal law

Let \(n=|P|\), set

\[
 c=\frac p{1-p}>0,\qquad
 t_k=c^k,\qquad Z_n=\sum_{k=0}^n\binom nk c^k=(1+c)^n.
 \tag{6}
\]

For every individual subset \(U\subseteq V(P)\),

\[
 \Pr_p(U)=\frac{c^{|U|}}{(1+c)^n}
          =p^{|U|}(1-p)^{n-|U|}.
 \tag{7}
\]

This is a per-subset law. Its cardinality law includes the binomial
multiplicity. The right side factorizes into the independent old-vertex
selection probabilities. The algebraic reparametrization \(c=p/(1-p)\)
does not change the law; changing \(p\) generally does.

For an ideal \(S\), write \(s=|S|\) and
\(m=|\operatorname{Max}(S)|\), with maxima in the induced ideal, not the
whole parent. The exact closure fiber is

\[
 \downarrow_P U=S
 \quad\Longleftrightarrow\quad
 \operatorname{Max}(S)\subseteq U\subseteq S.
 \tag{8}
\]

To prove necessity, closure equality implies \(U\subseteq S\).
A maximal element of \(S\) can be below a selected element of \(S\)
only if it is itself selected. For sufficiency, each element of a finite
ideal lies below one of that ideal's maxima. This proof includes empty,
whose only generator is empty and whose number of maxima is zero.

Summing the individual-subset weights over (8) gives

\[
 \begin{aligned}
 \pi_p(P,r,S)
 &=\frac{c^m(1+c)^{s-m}}{(1+c)^n}\\
 &=\boxed{p^m(1-p)^{n-s}}.
 \end{aligned}
 \tag{9}
\]

Equivalently, all \(m\) maxima must be selected, all \(n-s\) outside
vertices must be omitted, and the \(s-m\) other vertices are unrestricted.
The first line sums all those choices; it does not confuse individual
ideals with isomorphism classes of children.

The fibers (8) partition all \(2^n\) subsets, so

\[
 \sum_{S\in\operatorname{Id}(P)}\pi_p(P,r,S)
   =\sum_{U\subseteq V(P)}p^{|U|}(1-p)^{n-|U|}=1.
 \tag{10}
\]

Every probability in (9) is strictly positive for \(0<p<1\).
For a nonempty parent, at least empty and full are distinct positive
terms, so every ideal probability is less than one as well.
The full-slot value is \(p^{|\operatorname{Max}(P)|}\); it is already
part of (10), not an independently chosen complement.

At the empty parent, \(n=s=m=0\), \(Z_0=1\), and the sole ideal has
probability one; its two marked branches each have probability \(1/2\).
For every parent the empty ideal has probability \((1-p)^n\).
The endpoints \(p=0,1\) are excluded: already the singleton loses a
positive full or empty branch at those endpoints. No limiting endpoint
law is silently admitted.

Relabeling transports closure, cardinalities and induced maxima, so (9)
is equivariant for every marking. It ignores all old marks, which is
stronger than the required restriction on **mark** dependence. Its
unmarked dependence on \(n,s,m\) is permitted. In particular, no stronger
structural locality or spectator-independence principle is asserted.

## 4. Every marked diamond and the from-empty measure

Let \(C\) have \(n\) vertices and let \(S,T\) be any two ideals of \(C\).
Append \(x\) with past \(S\) and bit \(b\), then \(y\) with past \(T\)
and bit \(d\), excluding \(x\) from that second precursor.
The reverse route appends \(y\) first and excludes it from the second
precursor \(S\).

In either intermediate parent, each old precursor remains an ideal and
its induced order, size and induced maxima are unchanged. The new vertex
is maximal and is not in the second precursor; it cannot become a new
predecessor of an old element. Formula (9) therefore gives

\[
 \pi_p(C+x_S,r+b,T)=(1-p)\pi_p(C,r,T),
 \qquad
 \pi_p(C+y_T,r+d,S)=(1-p)\pi_p(C,r,S).
 \tag{11}
\]

It follows, with \(s=|S|,\ t=|T|\) and their induced maximum counts
\(m_S,m_T\), that both unmarked route products equal

\[
 (1-p)\pi_p(C,r,S)\pi_p(C,r,T)
 =p^{m_S+m_T}(1-p)^{2n+1-s-t}.
 \tag{12}
\]

There was no disjointness hypothesis on \(S,T\): overlap, either
containment, equality, empty and full precursors are all covered.
If \(S=C\), it is full for the first birth and proper in \(C+y_T\);
its induced maxima remain those of \(C\), not the global maxima of the
intermediate parent. If both are full, the two newborns have the same
old full past and are incomparable. At \(C=\varnothing\), both
precursors are empty and the route product is \(1-p\), also as in (12).

The two terminal marked orders are canonically matched by identifying
each old vertex and matching \(x,b\) and \(y,d\) to the corresponding
birth on the other route. For every assignment of all old and both
newborn bits and every arbitrary fixed-carrier complex PSD \(X\), the
full composed map on each route is

\[
 X\longmapsto
 \frac{p^{m_S+m_T}(1-p)^{2n+1-s-t}}4X.
 \tag{13}
\]

This proves equality of the complete unnormalized maps, not just their
traces, normalized outputs, diagonals, or a selected nonzero payload.
When \(X=0\), both maps output zero. The classical kernel (9) is
specified independently, with no division by a trace. Scalar passivity
also gives the complete one-step sum
\(\sum_{S,b}\mathcal B_{S,b}(X)=X\).

For an explicit all-size realization, take mutually independent variables

\[
 E_{ij}\sim\operatorname{Bernoulli}(p)\quad(1\le i<j<\infty),
 \qquad b_j\sim\operatorname{Bernoulli}(1/2)\quad(j\ge1),
 \tag{14}
\]

with all edge and bit coordinates independent. This is a countable product
probability measure. At birth \(j\), set
\(U_{j-1}=\{i<j:E_{ij}=1\}\) and take its past closure in \(P_{j-1}\).
Induction shows \(P_N\) is exactly the transitive closure of the
forward-edge DAG on \([N]\).

Let

\[
 \mathcal G_n=\sigma(E_{ij}:1\le i<j\le n;\ b_1,\ldots,b_n).
 \tag{15}
\]

The entire next head-vector and next bit are independent of
\(\mathcal G_n\); conditional closure probabilities are precisely (9)
and marked branch probabilities are (9)/2. Conditioning down to the
visible marked-order history preserves those probabilities by the
tower property, since their value is a function of the current order.
The auxiliary filtration is legitimate even though the visible closure
need not reveal which redundant generating edges were selected.

This constructs consistent histories from empty at every size and
positive mass for every specified finite admissible marked history.
It does not assert positive mass for every individual infinite history.
Birth labels are bookkeeping labels used for the construction and proof,
not spacetime coordinates or physical time. No arbitrary previously
fixed prefix is preserved or spliced into this law.

## 5. A finite invariant distinguishing it from factorial laws

The accepted factorial-power family has per-subset weights
\((k!)^{-q}\) for each separately fixed integer \(q\ge1\).
At a singleton parent its full-to-empty ideal probability ratio is
one, since \(0!=1!=1\). For (9), that ratio is

\[
       \frac{\pi_p(C_1,C_1)}{\pi_p(C_1,\varnothing)}
       =\frac p{1-p}=c.
 \tag{16}
\]

If \(p\ne1/2\), (16) already differs from every factorial-power law.
If \(p=1/2\), use the two-vertex antichain \(A_2\). Its full and empty
ideals have unique full and empty generators, and their ratio is

\[
 \frac{\pi_p(A_2,A_2)}{\pi_p(A_2,\varnothing)}
      =c^2=1
      \ne 2^{-q}
      =\frac{\pi_q(A_2,A_2)}{\pi_q(A_2,\varnothing)}
      \quad(q\ge1).
 \tag{17}
\]

This two-case argument is needed: a two-antichain ratio alone could
coincide for a specially chosen \(p\), even though the singleton ratio
then differs. Together (16)–(17) distinguish every fixed \(p\in(0,1)\)
from every accepted fixed-integer factorial-power law.

These are reachable parents, not arbitrary supplied prefixes.
The first vertex always exists. The second can have empty past with
probability \(1-p>0\) under the present law and \(1/2>0\) under each
factorial-power law. Any specified two bits also have positive probability.
Thus both comparisons refer to positive-probability finite histories
of the respective from-empty measures.

Full and empty ideals are intrinsically distinguished and cannot be
exchanged by an order relabeling. A paired coordinate gauge preserving
actual normalized branch probabilities preserves their ratio.
The differing ratios therefore witness a change of law. By contrast,
(6)–(7) are equivalent descriptions of one law. Admission proves that
each proposed law meets the declared principles; it does not force
the parameter \(p\), product independence, or these weights.

## 6. A positive-density chain with a history-valid strong law

Start the greedy chain at vertex \(1\), with tip \(T_1=1\).
At each birth \(j\ge2\), define

\[
 \xi_j=E_{T_{j-1},j},\qquad
 T_j=
 \begin{cases}
 j,&\xi_j=1,\\
 T_{j-1},&\xi_j=0.
 \end{cases}
 \tag{18}
\]

Append \(j\) to the chain exactly when \(\xi_j=1\).
Every appended vertex directly selects its predecessor tip, so these
vertices form a chain in the completed order. Its length at size \(N\ge1\)
is

\[
                      L_N=1+\sum_{j=2}^N\xi_j.
 \tag{19}
\]

The adaptive choice of tip does not by itself justify independent
increments. The needed conditioning argument is as follows.
\(T_{j-1}\) is \(\mathcal G_{j-1}\)-measurable and lies in \([j-1]\).
Using independence of the fresh head-vector,

\[
 \Pr_p(\xi_j=1\mid\mathcal G_{j-1})
 =\sum_{i=1}^{j-1}\mathbf1_{\{T_{j-1}=i\}}
       \Pr_p(E_{ij}=1\mid\mathcal G_{j-1})
 =p.
 \tag{20}
\]

The conditional failure probability is \(1-p\). Since all previous
\(\xi\)'s are measurable in this past, iterating (20) proves for every
finite binary sequence \(a_2,\ldots,a_N\),

\[
 \Pr_p(\xi_2=a_2,\ldots,\xi_N=a_N)
       =\prod_{j=2}^N p^{a_j}(1-p)^{1-a_j}.
 \tag{21}
\]

Thus these increments are genuinely iid Bernoulli(\(p\)) under the
declared measure. This claim is not made for whole growing orders or
for other optional laws.

For completeness, a short elementary strong-law argument avoids
requiring more than variance, Chebyshev and Borel–Cantelli.
By (21),
\(\mathbb E L_N=1+(N-1)p\) and
\(\operatorname{Var}(L_N)=(N-1)p(1-p)\).
For each fixed \(\varepsilon>0\),

\[
 \sum_{k=1}^\infty
 \Pr_p\!\left(
 |L_{k^2}-\mathbb E L_{k^2}|>\varepsilon k^2
 \right)
 \le\frac{p(1-p)}{\varepsilon^2}
           \sum_{k=1}^\infty\frac1{k^2}<\infty.
 \tag{22}
\]

Borel–Cantelli and the countable choices \(\varepsilon=1/m\)
give \(L_{k^2}/k^2\to p\) almost surely, since the normalized mean
tends to \(p\). For \(k^2\le N<(k+1)^2\), monotonicity of \(L_N\) gives

\[
 \frac{L_{k^2}}{(k+1)^2}
 \le\frac{L_N}{N}
 \le\frac{L_{(k+1)^2}}{k^2}.
\]

Both endpoints tend to \(p\), proving the **full-sequence** conclusion

\[
                         L_N/N\longrightarrow p
                         \quad\text{almost surely}.
 \tag{23}
\]

There is no independence assumption between different square-size events.

For every realized finite order,
\(R_{\mathcal F}(P_N)\ge H_N\ge L_N\).
Combining with (23) proves all three assertions in (1).
The greedy witness uses auxiliary selection information, but its existence
certifies intrinsic, relabeling-invariant inequalities about \(H_N\)
and \(R_{\mathcal F}(P_N)\).

The proof does not identify the longest chain with this greedy chain,
prove an exact limit for \(H_N/N\) or \(R_{\mathcal F}/N\), or show that
deleting \(o(N)\) vertices suffices. Only the stated lower/upper limits
are established. A one-row retained chain is not a dense two-dimensional
target, a manifoldlike limit, or an emergent geometry.

## 7. Vanishing incomparable density under the same law

Fix \(1\le i<j\), and put \(d=j-i\ge1\).
Since every edge increases its label, reverse comparability is impossible.
If \(i\) and \(j\) are incomparable, then the direct edge is absent and
there is no two-edge path through any intermediate label:

\[
 \{i\parallel j\}
 \subseteq
 \{E_{ij}=0\}\cap
 \bigcap_{i<k<j}\{\neg(E_{ik}=1\ \text{and}\ E_{kj}=1)\}.
 \tag{24}
\]

The single coordinate \((i,j)\) and the coordinate pairs
\(\{(i,k),(k,j)\}\), for distinct \(k\), are mutually disjoint.
For example, a first edge \((i,k)\) cannot equal a last edge \((\ell,j)\)
with \(i<k,\ell<j\), since equality would require \(\ell=i\) and \(k=j\).
All these coordinates are independent under (14), even when some edges
share the head \(j\). It is this special **within-subset** product law
that permits the independence; it is not available in the factorial
subset family.

The event on the right of (24) consequently has probability
\((1-p)(1-p^2)^{d-1}\), so

\[
 \boxed{\Pr_p(i\parallel j)
       \le(1-p)(1-p^2)^{d-1}.}
 \tag{25}
\]

At \(d=1\) the intermediate intersection is empty and the bound is exact.
For larger gaps, longer paths can also make the pair comparable, so the
displayed expression is an upper bound, not a general equality.

There are \(N-d\) unordered pairs at gap \(d\). Linearity of expectation
and a geometric-series bound give for \(N\ge1\)

\[
 \begin{aligned}
 \mathbb E_p I(P_N)
 &\le(1-p)\sum_{d=1}^{N-1}(N-d)(1-p^2)^{d-1}\\
 &\le N(1-p)\sum_{d=1}^\infty(1-p^2)^{d-1}
 =\frac{1-p}{p^2}N.
 \end{aligned}
 \tag{26}
\]

The sum is empty at \(N=1\); \(N=0\) has \(I=0\) separately.
No pair-incomparability indicators have been assumed independent.
The constant is finite for each fixed \(p\in(0,1)\); no uniform
\(p\downarrow0\) or size-dependent-\(p\) assertion is supplied.
The notation \(O_p(N)\), if used informally for this bound, means a
constant depending on fixed parameter \(p\), not a new stochastic-order
claim; (26) avoids that ambiguity.

An expectation bound alone is not an almost-sure conclusion.
For every fixed \(\varepsilon>0\), Markov's inequality gives

\[
 \sum_{\ell=0}^\infty
 \Pr_p\!\left(\frac{I(P_{2^\ell})}{2^{2\ell}}>\varepsilon\right)
 \le\frac{1-p}{p^2\varepsilon}
            \sum_{\ell=0}^\infty2^{-\ell}<\infty.
 \tag{27}
\]

Borel–Cantelli, followed by a countable intersection over
\(\varepsilon=1/m\), proves
\(I(P_{2^\ell})/2^{2\ell}\to0\) almost surely.
Independence between different sizes is not required.

Old comparisons never change when a new maximal vertex is born.
Equivalently, a forward-directed path connecting old vertices cannot
pass through a later vertex and then return to an older endpoint.
Thus \(P_{N+1}|_{[N]}=P_N\) and \(I(P_N)\) is nondecreasing in \(N\).
For \(2^\ell\le N<2^{\ell+1}\),

\[
 0\le\frac{I(P_N)}{N^2}
 \le\frac{I(P_{2^{\ell+1}})}{2^{2\ell}}
 =4\frac{I(P_{2^{\ell+1}})}{2^{2(\ell+1)}}\longrightarrow0.
 \tag{28}
\]

This proves the almost-sure full-sequence statement in (2), not just
a subsequence or in-probability limit. For \(N\ge2\),

\[
 \frac{I(P_N)}{\binom N2}
     =\frac{2N}{N-1}\frac{I(P_N)}{N^2}\longrightarrow0.
 \tag{29}
\]

Intersecting the probability-one events from (23) and (28) makes
(1), (2), and (29) simultaneous on the **same** from-empty product measure.
No joint coupling with any factorial law, and no independent-pair or
independent-path assumption, is needed.

## 8. Load-bearing height premise and the fixed dense target

The accepted [joint height/density theorem](FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md) concerns exactly the class (4) and proves

\[
 H_N=O(\sqrt N),\quad I(P_N)=o(N^2)
 \quad\Longrightarrow\quad R_{\mathcal F}(P_N)/N\to0.
 \tag{30}
\]

Under the present law, (1) implies eventually \(H_N/N\ge p/2\)
on its probability-one event, so
\(H_N/\sqrt N\ge(p/2)\sqrt N\to\infty\).
Thus (30)'s square-root height assumption fails, while its vanishing
density assumption holds. Removing the height premise from that theorem
is disproved by this law. This does not prove that the square-root
condition is the weakest possible height hypothesis or classify all
intermediate height scales.

For clarity, the earlier dense target remains unchanged. Fix
\(0<\nu\le1\) and \(1\le A<\infty\).
\(\mathcal T_{\nu,A}\) contains empty and filled partition-cell orders
with at least one representation satisfying, for \(k\) cells, \(r\)
nonzero rows and width \(w\),

\[
                 k\ge\nu rw,\qquad A^{-1}\le r/w\le A.
 \tag{31}
\]

These parameters are fixed independently of size and history.
The accepted DENSE_FERRERS_INCOMPARABILITY_SCREEN.md proves

\[
 I(Q)\ge\epsilon_0\binom k2
 \quad(Q\in\mathcal T_{\nu,A},\ k\ge m_0),\qquad
 \epsilon_0=\nu^4/128,\quad m_0=\lceil16A/\nu^2\rceil.
 \tag{32}
\]

Apply (32) to any qualifying induced \(Q=P_N[W]\). Its incomparable
pairs are retained parent pairs, so

\[
                    \epsilon_0\binom{|W|}{2}
                    \le I(Q)\le I(P_N)
                    \quad(|W|\ge m_0).
 \tag{33}
\]

If the maximal dense-target retention had positive normalized limsup,
some fixed \(\eta>0\) would give unbounded sizes with \(|W|\ge\eta N\).
For large such sizes (33) would imply
\(I(P_N)/N^2\ge\epsilon_0\eta^2/4>0\), contradicting (28);
the elementary bound \(\binom k2\ge k^2/4\) applies for \(k\ge2\).
Smaller retained sizes below \(m_0\) are harmless. Therefore

\[
       R_{\nu,A}(P_N)/N\to0,\qquad D_{\nu,A}(P_N)/N\to1
       \quad\text{almost surely}.
 \tag{34}
\]

No stochastic property of the factorial law is borrowed in (34);
only the deterministic fixed-target density floor is reused.
The new stochastic premise was proved for (14).

The containment direction is

\[
 \mathcal T_{\nu,A}\subseteq\mathcal F,\qquad
 R_{\nu,A}\le R_{\mathcal F},\qquad
 D_{\nu,A}\ge D_{\mathcal F}.
 \tag{35}
\]

Hence the restricted-target obstruction (34) is compatible with
positive unrestricted retention in (1). It cannot be reversed into
an obstruction for \(\mathcal F\). Nor does the chain witness establish
a macroscopic dense-target representative. The result separates these
two already declared diagnostics without changing either target.

## 9. What depends on principles and what depends on this law

The complete positive marked-admission theorem is a theorem **about
the explicit choice** (7). Neither product independence nor its fixed
\(p\) is entailed by the basic admission conditions.

Within the fair scalar/passive model the two factors \(1/2\) entail the
\(1/4\) diamond factor. For this choice, closure fibers entail (9),
its special size dependence entails (11), and the product construction
entails the independence used in (20) and (25). These are conditional
mathematical consequences, not extra claims of DET-native derivation.

The accepted fixed-integer factorial-power results, including the [joint height/density theorem](FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md),
remain valid under their own unchanged measures. The present law is
a counterexample to extending their negligible-retention conclusion
to **all admitted laws**. It also refutes using vanishing pair density
alone to infer that conclusion for unrestricted filled Ferrers orders.
It does not identify or analyze the separately prescribed Ferrers
optimizer, reconstruct any earlier fixed coefficient prefix, or modify
an earlier law to conceal a failed target.

For each fixed \(p\), the conclusions have the stated scope.
There is no result uniform in \(p\), no \(p=p(N)\), no adaptive tuning,
and no assertion simultaneous over an unspecified coupling of all laws.
The exact chain speed \(p\) belongs to the constructed greedy chain;
it is only a lower bound on longest-chain and retention fractions.
No exact deletion limit, optimal constant or geometric approximation
algorithm is provided.

No Hilbert space, metric, Minkowski coordinates, Johnston kernel or
physical amplitudes are recovered from DET by this calculation.
The passive PSD carrier is an explicit part of the conditional model,
not a derived quantum dynamics. Present relational activity is not
identified with committed-record growth. There is no mass/gravity law,
physical clock, empirical discriminator, observation/preparation model,
application benchmark, novelty assertion or universal physical exclusion.

## 10. Sources, review categories and stopping boundary

The six literal source bodies were used as follows:

- FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md: exactly accepted predecessor,
  unrestricted target, deterministic joint implication and the accepted
  all-fixed-integer factorial-family contrast.
- FACTORIAL_POWER_LAW_FAMILY.md: from-empty comparison laws, individual-ideal
  convention and invariant finite ratios; no within-subset independence
  is transferred from that family.
- DENSE_FERRERS_INCOMPARABILITY_SCREEN.md: deterministic density premise
  (32), reused only after proving the present law's own stochastic premise.
- INTRINSIC_GEOMETRY_TARGET_SCREEN.md: exact occupancy/aspect target and
  completed-order deletion convention.
- THEOREM_PACKAGE.md: the declared marked-order admission model and full
  passive PSD maps, distinguished from the separately prescribed prefix
  and optimization problems.
- LAW_DEPENDENCE.md: actual laws versus paired coordinate gauges and
  the limits of principle-forced claims.

The source’s two literal provenance records were inspected using their
actual schemas and its six source pins matched. The public links below are
reader equivalents for those six scientific roles, not original-custody
certificates or replacements for the private evidence.

| Public reader reference | Scientific source role |
| --- | --- |
| [Joint height/density obstruction](FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md) | Accepted predecessor, unrestricted target, deterministic joint implication and fixed-integer factorial-family contrast. |
| [Factorial-power law family](FACTORIAL_POWER_LAW_FAMILY.md) | From-empty comparison laws, individual-ideal convention and invariant finite ratios; no within-subset independence is transferred. |
| [Dense Ferrers incomparability screen](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) | Deterministic density premise, reused only after proving the present law’s own stochastic premise. |
| [Intrinsic geometry target screen](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Exact occupancy/aspect target and completed-order deletion convention. |
| [Theorem package](THEOREM_PACKAGE.md) | Declared marked-order admission model and full passive PSD maps, distinct from separately prescribed prefix and optimization problems. |
| [Law dependence](LAW_DEPENDENCE.md) | Actual laws, paired coordinate gauges and limits of principle-forced claims. |

At source construction, the joint manuscript was an accepted native
predecessor. Its historical pending header was distinct from a later exact
subject-joined adjudication accepting that input, not this manuscript.
The other five inputs were public snapshots attributed by supplied metadata
to a historical publication state, without independent Git or network
verification of that attribution.

The following paragraphs retain the source manuscript’s account of its
reading and manual work. Current display failures and their recovery,
unavailable prior body stores and older failures remain separate from
this derivative’s administrative checks and later independent review.

Only the six permitted literal manuscripts and the two permitted literal
JSON files were read. Their original paths, extra adjudication members,
linked archives, protected inputs and source programs were not followed.
The source set is unchanged. Older source-contained custody, execution,
receipt-matching and display failures remain historical limitations,
not reconstructed by these checks.

All eight current native source captures are complete. Prior-turn body
stores were unavailable, so no equality to a prior consumed body is
claimed: all six current manuscript bodies were freshly displayed and
consumed. Two attempted aggregate displays of THEOREM_PACKAGE.md were
visually truncated; the actual native captured string was intact.
Three contiguous bounded slices then displayed its complete body without
omission. The factorial manuscript was displayed in two contiguous slices;
the other four manuscripts and both JSON records were displayed in full.
The display failures and recovery are retained in the private source-provenance record.

Two independent manual workers reviewed supplied mathematical context,
one for admission and finite-law separation and one for the chain and
pair-density arguments and target scope. They had no source/file access
and did not audit the sources. Their mathematical reports and full
worker-reported usage observations are separated from root-direct tool
captures. These are manual cross-checks, not a proof-assistant certificate
or native adjudication. The elementary square-subsequence exposition of
the strong law in section 6 is supplied explicitly in this manuscript.

All mathematical work here is manual symbolic reasoning.
Administrative text assembly, exact string comparisons, JSON readbacks,
native hashes, byte counts and directory inventories are not scientific
execution. No scientific/numerical executor, probability/tail/interval
evaluation, sampling, simulation, optimizer, benchmark, experiment,
dataset/network acquisition or protected validation was performed.
Separate observations are not atomic original-custody certificates.

The source record also distinguishes metadata-only own-receipt readback
summaries from full source displays: exact captured strings were compared
administratively, without presenting those readback bodies as full model
consumption. Worker reports remain supplied-context checks, not source
audits or native adjudication.

The native manuscript and its three companion source-provenance, result
and freeze records remain private. Exact source pins, metadata operations,
tail correspondence and check receipts are retained locally. Private
identifiers, filesystem locations, fingerprints and tool transcripts are
withheld. No linked source original, archive, additional manifest member,
program, repository history or protected input was followed in preparing
this public derivative.

Manual mathematical construction is separate from independent native and
editorial review. This text preparation does not itself accept the theorem
or claim machine proof or public executable custody. Native acceptance,
editorial acceptance, publication and subsequent assignments are recorded
separately by the coordinator; no later result is claimed here. Targets,
protocol boundaries and the RET-only pause remain unchanged. See the
[publication note](PUBLICATION_NOTE.md) and
[redacted-publication policy](../../coordination/REDACTED_PUBLICATION.md).
