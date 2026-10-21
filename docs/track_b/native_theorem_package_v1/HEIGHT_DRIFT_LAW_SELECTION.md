# Height drift as a necessary law-selection test

21 October 2026. Manual conditional native-order mathematics.
Independent review is recorded separately from this source manuscript.
No scientific computation, optimization, dataset or experiment.

## 1. Result and uncertainty closed

For a birth with precursor ideal \(S\) in a parent order \(P\),
longest-chain vertex height increases precisely when
\[
                         h(S)=h(P).
\]
The complete conditional probability of this event is
\[
                p(P,r)=\sum_{S:\,h(S)=h(P)}q(P,r,S),          \tag{1}
\]
not merely the full-birth probability \(q(P,r,P)\).
Both newborn-bit outcomes have already been summed in (1).

For any selected admitted all-size law with its classical history measure,
let \(P_n,r_n\) be the actual marked parent after \(n\) births and set
\(p_n=p(P_n,r_n)\). Then
\[
 \boxed{\quad
 \frac{h(P_N)}N-\frac1N\sum_{n=0}^{N-1}p_n\longrightarrow0
 \quad\text{almost surely and in }L^2 .
 \quad}                                                     \tag{2}
\]
In particular, almost-sure sublinear height is **equivalent** to
almost-sure vanishing of this actual-history conditional-drift Cesaro
average. This equivalence is about height, not about target membership
or geometry.

Sublinear induced-deletion distance to any fixed target with a uniform
sublinear height envelope requires (2)'s vanishing condition.
It is not sufficient to suppress the full slot, and it is not sufficient
to prove sublinear height alone.

A separate full-component finite-layer height-drift objective is formulated
below. Compactness and strict restoration give a conditional formal
admissibility prescription, not a proved sublinear-height law.
Its expected Cesaro estimate and the stronger pathwise requirement remain
unproved. No existing Ferrers-defect objective is replaced.

## 2. Declared family, selected law and observation access

The admitted model from [THEOREM_PACKAGE](THEOREM_PACKAGE.md), §§1 and 9, consists of finite
orders \(P\), immutable binary marks \(r\), and an arbitrary complex
positive-semidefinite payload \(\mathfrak D\). A birth appends one
maximal vertex with strict past exactly an ideal \(S\subseteq P\).
Old relations and marks are retained. Every ideal, including empty
and full, is eligible and has strictly positive probability. The
complete marked branch is
\[
 \mathcal B_{S,b}^{P,r}(\mathfrak D)
     =\frac{q(P,r,S)}2\mathfrak D,\qquad
 b\in\{0,1\},\qquad \sum_{S\text{ ideal}}q(P,r,S)=1.          \tag{3}
\]
Proper slots retain the declared precursor-record locality, whole
unmarked-parent access and marked equivariance. Complete incomparable
birth diamonds, including equal precursors and all marks, remain premises.

The ratio-component characterization and positive continuation theorem
are admitted mathematical inputs. This packet does not derive them from
bare DET, authenticate original coefficients, or choose an actual
coefficient branch. The scalar-passive payload does not produce
informative quantum dynamics here. The classical \(q/2\) kernel is declared
separately: for zero payload the branch maps vanish, and no \(0/0\) trace
normalization is attempted.

Fix a particular compatible all-size law when making probabilistic
statements. Its complete finite-history probabilities define the admitted
infinite classical history measure. The filtration \(\mathcal F_n\)
contains the entire marked history through cardinality \(n\).
No iid native births, stationary shape distribution, or observed-data
law selection is assumed.

Finite natural birth labels index this filtration, not a physical clock.
Height is an intrinsic unlabelled-order statistic. The conditional
quantity \(p_n\) additionally uses the selected law and old marks.
Neither is automatically a physical readout.

## 3. Exact height increment, including the empty parent

Set \(h(\varnothing)=0\), and count vertices, not edges, in a chain.
Any chain in \(P+S\) that omits the newborn has length at most \(h(P)\).
Any chain containing it ends there, and all preceding vertices lie
in \(S\), so its length is at most \(1+h(S)\).
Conversely, an old longest chain remains, and a longest chain in \(S\)
can be followed by the newborn. Therefore
\[
                 h(P+S)=\max\{h(P),1+h(S)\}.                \tag{4}
\]
Since \(S\) is an induced suborder and heights are integers,
\(h(S)\le h(P)\). Consequently
\[
 e_P(S):=h(P+S)-h(P)
       =\mathbf1_{\{h(S)=h(P)\}}\in\{0,1\}.                 \tag{5}
\]
This is independent of the newborn bit but not of the precursor ideal.

When \(P=\varnothing\), its sole ideal is also empty,
\(q(\varnothing,\varnothing)=1\), and (4)–(5) give first-birth increment
one. There is no proper slot at this layer. In particular (1) gives
\(p_0=1\). Empty is not incorrectly classified as height-neutral there.
For nonempty \(P\), the empty precursor is height-neutral.

Let \(S_n\) be the chosen ideal at parent size \(n\), and
\(I_{n+1}=e_{P_n}(S_n)=H_{n+1}-H_n\), where \(H_n=h(P_n)\).
The full marked row yields
\[
 \begin{split}
 E[I_{n+1}\mid\mathcal F_n]
 &=\sum_{S\text{ ideal of }P_n}\sum_{b=0}^1
        \frac{q(P_n,r_n,S)}2 e_{P_n}(S)\\
 &=\sum_{S:\,h(S)=H_n}q(P_n,r_n,S)=p_n.                     \tag{6}
 \end{split}
\]
There is no remaining factor \(1/2\). Every individual ideal occurrence
is counted, even if several births have isomorphic children.
Old marks may affect \(q\), though height itself ignores them.

## 4. Pathwise decomposition and bounded martingale

Fix any deterministic finite starting size \(n_0\ge0\).
The initial marked history can be random; do not replace it by an
unmarked representative. For \(N=n_0+m\), define
\[
 \Gamma_{n_0,N}=\sum_{n=n_0}^{N-1}p_n,\qquad
 M_{n_0,N}=\sum_{n=n_0}^{N-1}(I_{n+1}-p_n).
\]
Summing the exact increments gives the pathwise identity
\[
 \boxed{\quad H_N=H_{n_0}+\Gamma_{n_0,N}+M_{n_0,N}.\quad}      \tag{7}
\]
The process \(M_{n_0,N}\), starting at zero, is a martingale for the
full filtration because each difference has conditional mean zero.
Its conditional range is \([-p_n,1-p_n]\), of length one, and its
conditional variance is \(p_n(1-p_n)\le1/4\).

This is the compensator of the **actual complete height increments**.
Replacing \(p_n\) by full-birth probability would give only a lower
witness and would destroy the exact equality (7).

For \(m=0\), both sums vanish and (7) is \(H_N=H_{n_0}\).
All expressions below dividing by \(m\) are restricted to \(m\ge1\).

## 5. Self-contained concentration and strong law

For a Bernoulli variable of parameter \(p\in[0,1]\), put
\[
 f_p(t)=\log(1-p+pe^t)-pt .
\]
For \(p=0\) or \(1\), \(f_p=0\). Otherwise
\(f_p(0)=f'_p(0)=0\), and
\[
 f''_p(t)=w_t(1-w_t)\le1/4,\qquad
 w_t=\frac{pe^t}{1-p+pe^t}.
\]
For every real \(t\), integrating twice gives
\[
 f_p(t)=t^2\int_0^1(1-v)f''_p(vt)\,dv\le t^2/8 .
\]
Apply this pointwise to the conditional Bernoulli distribution of
\(I_{n+1}\), whose parameter \(p_n\) is \(\mathcal F_n\)-measurable:
\[
 E[e^{t(I_{n+1}-p_n)}\mid\mathcal F_n]\le e^{t^2/8}.          \tag{8}
\]
Iterated conditional expectation, not independence, now gives
\[
 E[e^{tM_{n_0,N}}\mid\mathcal F_{n_0}]\le e^{mt^2/8}.
\]
For \(x>0\), conditional Markov with \(t=4x/m\), and separately
with its negative for the lower tail, proves
\[
 \boxed{\quad
 P(|M_{n_0,N}|\ge x\mid\mathcal F_{n_0})
       \le \min\{1,\,2e^{-2x^2/m}\}.
 \quad}                                                     \tag{9}
\]
At \(x=0\), use the trivial bound one. All statements are almost-sure
conditional statements, or statements on positive-probability finite
initial histories; no null-history conditioning is used.

For fixed \(\epsilon>0\), averaging (9) over the prefix gives
\[
 P(|M_{n_0,n_0+m}|\ge\epsilon m)
       \le2e^{-2\epsilon^2m},\qquad m\ge1.
\]
The exponential series is finite. For every \(K\), the probability
that any such event occurs at \(m\ge K\) is bounded by the corresponding
series tail, which tends to zero. Hence only finitely many occur
almost surely. Intersect over positive rational \(\epsilon\) to obtain
\[
                M_{n_0,N}/m\longrightarrow0
                \quad\text{almost surely}.                 \tag{10}
\]
Since \(n_0\) is fixed, \(m/N\to1\), proving the same assertion
with denominator \(N\). No independence between the tail events
was needed.

The martingale differences are orthogonal in conditional second moment:
for earlier difference \(d_i\) and later \(d_j\), the tower property
gives \(E[d_i d_j\mid\mathcal F_{n_0}]=0\).
Thus
\[
 E[M_{n_0,N}^2\mid\mathcal F_{n_0}]\le m/4,\qquad
 E[|M_{n_0,N}|\mid\mathcal F_{n_0}]\le\sqrt m/2.             \tag{11}
\]
The second-moment bound is \(m/4\); the \(L^2\) norm bound is
\(\sqrt m/2\), not \(m/4\). In particular \(M_{n_0,N}/N\to0\)
also in \(L^2\), hence in \(L^1\) and probability.

Equations (7), (10) and \(0\le H_{n_0}\le n_0\) prove (2).
The finite prefix contributes only a bounded term divided by \(N\);
it need not obey any later drift design rule.

## 6. Exactly which convergence statements follow

Write
\[
 Z_N=H_N/N,\qquad
 \bar p_N=\frac1N\sum_{n=0}^{N-1}p_n,\qquad N\ge1 .
\]
Both lie in \([0,1]\). Equation (2) implies, on one probability-one event,
\[
 \liminf Z_N=\liminf\bar p_N,\qquad
 \limsup Z_N=\limsup\bar p_N.                               \tag{12}
\]
If either sequence has a limit, the other has the same limit.
No existence or deterministic value of that limit is asserted.
In particular,
\[
             Z_N\to0\ {\rm a.s.}
          \quad\Longleftrightarrow\quad
             \bar p_N\to0\ {\rm a.s.}                       \tag{13}
\]

Expectations are separately exact:
\[
       E[H_N]=\sum_{n=0}^{N-1}E[p_n],\qquad
       E[Z_N]=E[\bar p_N].                                 \tag{14}
\]
For a general fixed prefix, add \(E[H_{n_0}]\) and begin the sum at
\(n_0\). The expectation of a conditional drift is not its value
on a realized history.

For any \(0\le X_N\le1\), \(E[X_N]\to0\) is exactly \(L^1\)
convergence to zero and implies convergence in probability by Markov.
Conversely,
\[
 E[X_N]\le\epsilon+P(X_N>\epsilon)
\]
shows that convergence in probability to zero implies expectation
convergence by letting \(\epsilon\downarrow0\).
Therefore the following are equivalent:
\[
 \begin{gathered}
 E[H_N]/N\to0,\quad Z_N\to0\text{ in }L^1,\quad
 Z_N\to0\text{ in probability},\\
 \frac1N\sum_{n<N}E[p_n]\to0,\quad
 \bar p_N\to0\text{ in }L^1,\quad
 \bar p_N\to0\text{ in probability}.                        \tag{15}
 \end{gathered}
\]
Almost-sure sublinearity implies (15) by bounded convergence.
The converse is not supplied by the expectation calculation or
martingale concentration: (9) controls \(Z_N-\bar p_N\), not random
fluctuations of \(\bar p_N\) around its expectation.

To obtain (13)'s vanishing condition one must prove a pathwise drift
estimate or another sufficient argument. For example, a proved
deterministic envelope \(p_n(P,r)\le b_n\) on every marked row, with
\(N^{-1}\sum_{n<N}b_n\to0\), would suffice. A proved summable tail bound
for \(\{\bar p_N>\epsilon\}\), for each positive rational \(\epsilon\),
would also suffice by the same union-tail argument.
Neither kind of estimate is established for a new candidate here.
No auxiliary stochastic countermodel is asserted to be an admitted law.

## 7. Target screen: necessary direction only

Fix an isomorphism-invariant target class \(\mathcal T\) containing empty,
and a finite-valued nonnegative function \(g\) with \(g(0)=0\),
\[
        h(Q)\le g(|Q|)\quad(Q\in\mathcal T),\qquad g(k)=o(k).
\]
Neither target nor envelope may be loosened with the observed outcome
or with \(N\). Let \(D_{\mathcal T}(P)\) be the smallest number of
vertices whose deletion leaves an induced target order.
The minimum exists because deleting everything is allowed.

The accepted [target-screen proof](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) gives, for every finite order,
\[
 h(P)\le D_{\mathcal T}(P)+g(|P|-D_{\mathcal T}(P))
       \le D_{\mathcal T}(P)+G(|P|),\qquad
 G(N)=\max_{0\le k\le N}g(k).                               \tag{16}
\]
Indeed a longest chain loses at most the number of deleted vertices.
The nonmonotone envelope matters: \(g(N)\) cannot be substituted
without a valid monotonicity or maximum argument.

For completeness, \(g=o(k)\) implies \(G=o(N)\): given \(\epsilon>0\),
choose \(K\) with \(g(k)\le\epsilon k\) for \(k\ge K\);
the finitely many smaller values have maximum \(C_K<\infty\), so
\(G(N)\le\max(C_K,\epsilon N)\) for \(N\ge K\).

Thus, for a selected admitted all-size law,
\[
 \boxed{\quad
 D_{\mathcal T}(P_N)/N\to0\ {\rm a.s.}
 \ \Longrightarrow\ H_N/N\to0\ {\rm a.s.}
 \ \Longleftrightarrow\ \bar p_N\to0\ {\rm a.s.}
 \quad}                                                     \tag{17}
\]
The analogous necessary implication holds for expectation/\(L^1\)/
in-probability sublinearity, using (16) and (15).
The arrow from target distance to height is not reversed.
The empty-only target already illustrates that a small height does
not control every permitted target distance: its distance is \(N\)
on every nonempty order. This is a logical target example, not an
alternative growth model.

The accepted [half-scale baseline](HALF_SCALE_HEIGHT_GROWTH.md) has \(p_n\ge q(P_n,r_n,P_n)>1/2\)
for all \(n\ge6\). It therefore fails (17)'s necessary drift condition,
consistently with the accepted deletion-fraction liminf of at least
one half. That is a result for the selected baseline, not for every
admissible law.

The dense bounded-aspect Ferrers target in the predecessor is one
optional target to which (17) applies. Its occupancy/aspect assumptions
are not DET-derived manifold criteria. Unrestricted Ferrers orders
contain chains and do not have the required sublinear envelope.
Neither their defect nor the existing defect optimizer is settled.

## 8. Full births miss a genuine proper-ideal mechanism

For every nonempty parent,
\[
 p(P,r)=q(P,r,P)+
        \sum_{\substack{S\subsetneq P\\h(S)=h(P)}}q(P,r,S).
                                                               \tag{18}
\]
Every term is nonnegative. Thus vanishing Cesaro full-birth probability
is necessary for vanishing total drift, but it does not control the
second sum. Pointwise decay of the full slot is a stronger full-slot
condition, still not a bound on those missing terms.

For an exact finite example take \(P=\{x<y\}\sqcup\{z\}\).
Its six ideals are
\[
 \varnothing,\ \{x\},\ \{z\},\ \{x,z\},\ \{x,y\},\
 \{x,y,z\}.
\]
Here \(h(P)=2\). Exactly two ideals have height two: the proper ideal
\(\{x,y\}\) and the full ideal. A birth over \(\{x,y\}\) creates
the chain \(x<y<v\) while leaving \(z\) outside its past.
For every marking,
\[
                 p(P,r)=q(P,r,P)+q(P,r,\{x,y\}).            \tag{19}
\]
The admitted all-ideal positivity premise makes the second term
strictly positive; the source package also explicitly contains this
edge-plus-isolate parent. No numerical branch value is needed.

Equation (19) establishes an admissible finite event mechanism.
It does **not** construct an alternative complete all-size law whose
full probability tends to zero but whose height remains linear.
Such a stronger counterexample would have to establish positivity,
normalization, locality, equivariance, all marked diamonds and the
claimed infinite-history asymptotics. It remains open here.

The last-layer changes admitted in the source do not fill this gap:
later potentials and rows must be rebuilt from the changed prefix.
Keeping old later rows or repeating a naive proper-only scaling
can violate a mixed full/proper diamond. Suppressing only the full
slot is not a geometry construction.

## 9. A separate finite-layer height objective on the full polytope

Fix a free parent size \(n\ge1\) and an already admitted strictly
positive lower prefix. A finite complete set of marked parent
representatives is indexed by \(j=(P_j,r_j)\).
Every old marking is included. Relabeling transports the rows.

In the specified maximal-deletion-potential convention,
\[
 u_j(S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P_j)\setminus S}
 q(P_j\setminus A,r_j|_{P_j\setminus A},S)^{(-1)^{|A|+1}},
 \qquad S\subsetneq P_j.                                   \tag{20}
\]
These smaller-input evaluations do not erase committed records.
All values are positive and finite. The admitted component key
\(c(j,S)\) retains the whole unmarked parent and selected marks.
It cannot be replaced by just an ideal size or child shape.

Form the full component-capacity matrix and closed polytope
\[
 A_{jc}=\sum_{\substack{S\subsetneq P_j\\c(j,S)=c}}u_j(S),
 \qquad
 K_n=\{\alpha:\alpha_c\ge0,\ A\alpha\le\mathbf1\}.            \tag{21}
\]
Every individual ideal occurrence contributes, including isomorphic
aliases; forward ideal multiplicity is not a backward deletion count.
All marked row constraints remain, even if a chosen weighting were
zero on some rows.

For \(\alpha\in K_n\), the nonnegative complete row is
\[
 q^\alpha_j(S)=u_j(S)\alpha_{c(j,S)}\ (S\subsetneq P_j),
 \qquad q^\alpha_j(P_j)=1-\sum_{S\subsetneq P_j}
                              u_j(S)\alpha_{c(j,S)}.        \tag{22}
\]
Boundary vectors may have zero branches and are **not** themselves
members of the strictly positive admitted family. They are a
closed optimization domain used before strict restoration.

Set \(e_j(S)=\mathbf1_{\{h(S)=h(P_j)\}}\).
Since \(e_j(P_j)=1\), the exact conditional height-increase objective
at a specified marked parent is the affine function
\[
 \begin{split}
 p_j(\alpha)
 &=1+\sum_{S\subsetneq P_j}(e_j(S)-1)
                           u_j(S)\alpha_{c(j,S)}\\
 &=1-\sum_{\substack{S\subsetneq P_j\\h(S)<h(P_j)}}
                           u_j(S)\alpha_{c(j,S)}.
                                                               \tag{23}
 \end{split}
\]
The objective rewards allocation to height-neutral ideals.
Allocation to a height-raising proper ideal merely replaces a
height-raising full birth and has zero direct coefficient in (23).
Shared component constraints still couple all such allocations.

Let \(\pi_{n,j}\) be the actual probability that the selected lower
prefix reaches the complete marked parent class \(j\), summing
**all natural histories** in that class with all their \(q/2\) factors.
Then \(\pi_{n,j}\ge0\) and \(\sum_j\pi_{n,j}=1\).
There is no uniform-over-shapes or uniform-over-markings substitution.

The proposed separate one-step criterion is
\[
 \Psi_n^H(\alpha)=\sum_j\pi_{n,j}p_j(\alpha),\qquad
 m_n^H=\min_{\alpha\in K_n}\Psi_n^H(\alpha).                 \tag{24}
\]
It is the expected next height increment for that fixed prefix.
At this layer \(u,\pi\) are fixed before choosing \(\alpha\).
Under a new recursive law they must be recomputed from its own
changed prefix at every later layer.

Minimizing a single row, a worst row, or a differently weighted
average is a different design criterion. A minimizer of (24)
need not minimize every \(p_j\), and greedy one-step minimization
need not minimize eventual height. No long-horizon optimality is
proved. This criterion is not the existing expected-Ferrers-defect
objective \(\Phi_n\) in [THEOREM_PACKAGE](THEOREM_PACKAGE.md) §9; that objective, its
canonical instance and all its open questions are unchanged.

## 10. Existence of the finite minimum and strict restoration

There are finitely many rows, ideals and components at a fixed size.
Discard no occurring component: for each \(c\), some \(A_{jc}>0\),
so the constraint at that row bounds \(\alpha_c\le1/A_{jc}\).
Thus \(K_n\) is nonempty (it contains zero), closed and bounded
in a finite-dimensional space, hence compact.
The continuous affine objective attains its minimum, with
\(0\le m_n^H\le1\). A boundary minimizer need not be unique.

If a definite prescription is wanted, a predeclared isomorphism-based
canonical component ordering and successive coordinate minimization
among primary optima selects a unique vector \(\alpha_n^*\).
This is an additional optional selector, not a DET principle.
No selector, coordinate list or optimum is numerically evaluated here.

For a strict interior reference, define from the **whole marked layer**
\[
 T_j=\sum_{S\subsetneq P_j}u_j(S),\qquad
 B_n=\max_jT_j,\qquad a_n=\frac1{2(1+B_n)},\qquad
 \alpha_n^\circ=a_n\mathbf1 .                              \tag{25}
\]
For \(n\ge1\), \(0<B_n<\infty\). Every proper branch of this
reference is positive and its full complement is at least
\(1/2+a_n>1/2\). The ratio theorem supplies its compatibility;
this is the specified potential convention, not a gauge-invariant
meaning of “common coefficient.”

For a declared deterministic sequence \(0<\eta_n<1\), set
\[
        \widetilde\alpha_n
           =(1-\eta_n)\alpha_n^*+\eta_n\alpha_n^\circ .
                                                               \tag{26}
\]
Each proper probability is at least \(\eta_n a_nu_j(S)>0\),
and its full complement is at least
\(\eta_n(1/2+a_n)>0\). Together with the admitted ratio-component
theorem, locality and equivariant component construction, this gives
a strictly admissible next layer, retaining complete marked diamonds.
The full map factors \(q/2\) and two-step payload factors \(1/4\)
are unchanged in form.

Applied inductively to its own lower prefixes, a fixed selector and
restoration prescription define a formal compatible positive
all-size law under the admitted continuation theorem.
This is conditional **existence/admissibility**, not a proved successful
sublinear-growth construction. No such recursion is implemented or
its coefficients calculated in this packet.
At \(n=0\) the sole ideal has probability one; the polytope construction
is unnecessary. A preserved finite prefix can instead be left entirely
unchanged, with the new criterion beginning at a declared later free
layer, such as \(n=6\).

## 11. What restoration bounds, and what remains unproved

At the fixed layer, affinity gives for every marked row
\[
 p_j(\widetilde\alpha_n)
   =(1-\eta_n)p_j(\alpha_n^*)+\eta_np_j(\alpha_n^\circ),
 \qquad
 |p_j(\widetilde\alpha_n)-p_j(\alpha_n^*)|\le\eta_n.          \tag{27}
\]
The rowwise change need not be nonnegative: \(\alpha_n^*\) minimizes
the weighted objective, not every individual row.

Let \(r_n^H=\Psi_n^H(\widetilde\alpha_n)\).
Optimality of \(\alpha_n^*\), and \(0\le\Psi_n^H(\alpha_n^\circ)\le1\),
give the different, weighted statement
\[
                       m_n^H\le r_n^H\le m_n^H+\eta_n.
                                                               \tag{28}
\]
These quantities refer to the proposed height-design recursion and
its own actual prefix-history weights, not to the old defect
optimizer or the unchanged half-scale baseline.

Let \(n_*\ge1\) be the fixed first free parent size after the preserved
finite prefix. If the restoration weights have vanishing Cesaro average,
\[
             \frac1N\sum_{n=n_*}^{N-1}\eta_n\to0,
\]
then (14), (28) and the fixed finite prefix imply
\[
 \boxed{\quad
 \frac{E[H_N]}N\to0
 \quad\Longleftrightarrow\quad
 \frac1N\sum_{n=n_*}^{N-1}m_n^H\to0
 \quad}                                                     \tag{29}
\]
for this fully specified recursive prescription.
By (15) this is also equivalent to \(L^1\) and in-probability
normalized sublinear height. The right-hand Cesaro estimate is
**not proved**. Finite-layer existence or small individual minima
would not establish it along recursively changing prefixes.

Even if (29) were proved, almost-sure sublinear height still requires
(13)'s actual-history condition. Equation (27) says that, when the
Cesaro restoration cost vanishes, this pathwise condition is
equivalent to
\[
 \frac1N\sum_{n=n_*}^{N-1}
       p_{j_n}(\alpha_n^*)\longrightarrow0
       \quad\text{almost surely under the restored law},    \tag{30}
\]
where \(j_n\) is its **actual** marked parent.
These are boundary row values evaluated along the restored history;
they are not histories generated by a boundary law.
A small weighted \(m_n^H\) is not a pathwise bound on (30).
No proof of (30), uniform row envelope, or summable drift-tail
estimate is supplied.

Restoration itself can obstruct the target if its weight persists.
The full-complement lower bound gives, on every history,
\[
 p_n\ge\eta_n(1/2+a_n)\ge\eta_n/2.
\]
Using (12), for a deterministic prescribed restoration sequence,
\[
 \liminf_{N\to\infty}\frac{H_N}N
    \ge\frac12\liminf_{N\to\infty}
               \frac1N\sum_{n=n_*}^{N-1}\eta_n
       \quad\text{almost surely}.                          \tag{31}
\]
A positive lower Cesaro restoration weight forces positive linear
height. Vanishing Cesaro weight removes only this particular
obstruction; it does not prove (29), (30), or a geometry limit.

No symbolic condition here is a numerical asymptotic estimate.
There is no coefficient sweep, optimum value, actual branch decision,
tail evaluation, simulator or implemented alternative law.

## 12. Probability-changing design is not a coordinate gauge

For a positive component gauge \(t_c\), the paired change
\[
        u'_j(S)=t_{c(j,S)}u_j(S),\qquad
        \alpha'_c=\alpha_c/t_c
\]
leaves every proper product, full complement, complete marked branch,
\(p_j\), history mass and objective value unchanged.
The capacity polytopes correspond by this bijection.
Such a representation change cannot alter height drift or evade
the target obstruction.

The common-coordinate interior reference in (25) is convention-dependent.
If reselected afresh after an unequal gauge change, it can describe
a different actual law; the corresponding reference must instead be
transported to compare the same law. Optional tie-breakers likewise
must be specified and transported, not inferred from a coordinate name.

Changing actual component allocations or a lower prefix changes
later potentials, history weights, capacities and optima.
Those new objects cannot be replaced by old-law tables.
The mathematical identities (4)–(17) hold for each admitted law
on its own measure; the half-scale floor, design estimates (28)–(31),
and any eventual asymptotic success depend on the selected prescription.

## 13. Decision table and remaining obligations

| Item | Status now | Exact boundary or remaining obligation |
| --- | --- | --- |
| Height raises iff precursor height equals parent height | Theorem in the declared birth model | Includes empty parent and the complete two-bit row |
| Exact height compensator and bounded-martingale tail/SLLN | Theorem for each admitted all-size law | Requires its actual classical history measure, not iid births |
| Vanishing actual conditional-drift Cesaro iff a.s. sublinear height | Theorem | Does not prove the condition for a proposed law |
| Expected/\(L^1\)/in-probability equivalences | Theorem | Must not be promoted to a.s. convergence without another argument |
| Sublinear target deletion requires sublinear height/drift | Necessary design test proved | Fixed target with uniform sublinear height envelope; no converse geometry claim |
| Proper ideals can raise height | Exact finite mechanism proved | No complete alternative stochastic asymptotic countermodel constructed |
| Full-component height objective and strict restoration bounds | Conditional finite-layer theorem and proposed separate criterion | Whole marked rows, actual history weights and all ideal multiplicities retained |
| Formal all-size restored recursion | Conditional admissibility prescription | Depends on admitted ratio theorem and optional selector/mixing choices; not successful target construction |
| Sublinear height for that recursion | Unresolved | Prove expected minima Cesaro decay for weak modes; prove actual-history drift decay for a.s. mode |
| Sublinear distance or geometry for a candidate | Unresolved, stronger obligation | Prove the actual target approximation/structure, not just low height; justify chosen target independently |
| Native mathematical observation | Height intrinsic; drift law/mark-dependent | No physical access, preparation, calibration, missing-record model or readout supplied |

The uncertainty closed is the exact quantity a candidate must control:
the complete probability of choosing **any** height-spanning ideal,
averaged along its actual history. Full-slot suppression and a finite
low-drift optimization certificate are not substitutes.

The all-size challenge is not mere existence of some positive continuation.
It is a fully admitted, explicitly selected continuation together with
the required drift estimate and, separately, a proof of the desired
target structure. An unsuccessful candidate may be rejected without
changing the target or reclassifying a fixture as an emergent result.

Cardinality is not physical time. No physical clock, metric, manifold
dimension, Lorentzian embedding, mass/gravity/QM, empirical discriminator
or application-performance conclusion is licensed.
The completed prospective GWOSC replay and rejected C256 raw-cost
advantage remain separate projects; neither is reinterpreted here.
RET, frozen protocols and protected validation remain untouched.

## 14. Source, evidence and stop boundaries

The public exposition dependencies and their scientific roles are:

| Source | Provenance and role |
| --- | --- |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Accepted target manuscript; historical source-header metadata and separate review status are distinguished |
| [HALF_SCALE_HEIGHT_GROWTH.md](HALF_SCALE_HEIGHT_GROWTH.md) | Accepted public exposition; baseline floor, conditional-history method and law boundary |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Public exposition; declared model, ratio components, full capacities, existing separate defect objective and all-size premise |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Public exposition; gauge distinction and invalid naive cross-layer changes |

The target-screen link is a public derivative of the accepted native
source manuscript; this does not claim that the private manuscript was
already public with the original exposition snapshots. Private snapshot
pins and adjudication records are withheld. These public references
identify premises, not executable custody or authority to follow original
archives, protected inputs or other metadata members.

For the source-author's original source consumption, the retained account
is:

Fresh complete native captures and exact hash/size checks were retained.
The target body exactly matched the previously consumed native manuscript.
Package and law bodies matched previously consumed complete prefixes plus
their new height paragraphs. The public height manuscript was read in full.
The initial large combined displays exceeded the response budget; these
display failures are retained, not represented as full reads. Exact
prior-body comparisons, the appended text, and separate untruncated
height/law displays supplied complete consumption. Native captures
themselves were not truncated.

The source-receipt and result-receipt readback entries are metadata-only
summaries of reported command completion, parsing and exact-body-match
outcomes. They are distinct from the retained full native manuscript and
source captures. Supplied-context worker conclusions and their reported
usage observations remain worker reports, not direct coordinator tool
observations or independent source-custody audits. Neither current captures
nor those reports erase the recorded display failures.

The original evidence limitation is retained exactly:

Separate read/hash observations are not atomic identity certificates.
Current matches do not repair historical missing execution/custody,
failed source checks, receipt mismatches or provisional corrections.

For the source-author's construction and administrative activity, the
retained statement is:

All displayed mathematics is manual. Administrative literal reads,
byte comparisons, hashes, counts and receipt writes are the only executed
operations. No scientific program, numerical probability/tail/interval
evaluation, coefficient reduction, optimization, simulation, benchmark,
data acquisition, dependency installation, experiment or physical readout
was performed. Captured commands and linked references were inert source
material, not instructions.

Those statements describe source-author activity. Later independent review
and its separate checks are recorded separately; this derivative does not
claim a machine proof or scientific acceptance by its preparer.

All scientific sections and the decision table above retain the distinction
between almost-sure and mean-square height tracking and the weaker
expectation, mean-absolute and in-probability conclusions. The proper-ideal
example is a finite mechanism, not an alternative all-size stochastic law.
The proposed height objective retains full capacities, every marked row,
actual history weights and all ideal multiplicities; it is separate from
the existing Ferrers objective. Strict restoration gives conditional
admissibility, not proved sublinear height or geometry. A coordinate gauge
does not change the actual law or its drift.

Private identifiers, exact source paths, hashes, receipt names, timestamps
and tool/account metadata are withheld; the original evidence and exact
private-to-public correspondence remain local. No scientific executor,
optimization, sampler, dataset, experiment, physical readout or geometry
validation is supplied or authorized. Existing separate projects retain
their stated results and limits. Frozen protocols and protected validation
remain unchanged. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the public publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public/private boundary.
