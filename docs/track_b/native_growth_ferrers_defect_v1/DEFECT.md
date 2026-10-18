# RI-56 — intrinsic Ferrers defect and the exact zero-drift admission criterion

24 September 2026 UTC. **Analytic diagnostic and conditional criterion;
independent coordinator adjudication accepted.** Arbitrary exceptional vertices
give a Ferrers approximation diagnostic that changes by zero or one at each
maximal birth. Requiring the exceptional set to be an ideal instead is not
robust: one cloned rectangle maximum can make its minimum size almost the
whole order. This note proves both statements, deterministic error bounds,
conditional drift criteria, and an exact fixed-layer boundary test.

No committed vertex, relation or record is deleted. No defect-control law,
feasible new layer, all-size selection, shape limit or geometry is constructed.
The [RI-54 obstruction](../native_growth_ferrers_bottleneck_v1/BOTTLENECK.md)
and all accepted prefix rows remain unchanged.

## 1. An intrinsic diagnostic, not a history operation

A finite order is Ferrers when it is isomorphic to a finite down-set of the
coordinatewise product order on `N^2`, including the empty order. Coordinates
here describe a combinatorial representative, not a physical metric or a
growth-law input. For a finite order P on vertex set V define

\[
 \delta(P)=\min\{|K|:K\subseteq V,\ P[V\setminus K]\text{ is Ferrers}\}.
 \tag{1}
\]

The exceptional set K is **arbitrary**, not necessarily an ideal. The retained
order is induced: every original relation between retained vertices is kept.
It need not be a chronological tail, an ideal, or a possible birth prefix.
The empty retained order is allowed. Equivalently, writing `f(P)` for the
largest cardinality of an induced Ferrers suborder,

\[
 \delta(P)=|P|-f(P).
 \tag{2}
\]

Finiteness ensures the minimum exists. The definition is unmarked and
isomorphism invariant, with `delta(empty)=0`, and, for nonempty P of size N,
`0<=delta(P)<=N-1` because a singleton is Ferrers. It equals zero exactly
on the Ferrers family. The minimizer need not be unique: the two-antichain
already has two singleton retained choices exchanged by an automorphism.
Neither a unique exception selector nor an equivariant chosen optimizer is
part of this definition.

All actual records and their full order remain present. K is a set used in a
comparison, not a proposal to erase, ignore operationally, or rewrite those
records. Record count remains birth bookkeeping, not an asserted physical
clock or a claim that every present activity produces a record.

## 2. Ideal monotonicity and exact one-birth stability

**Lemma 1.** If Q is an order ideal of P, then `delta(Q)<=delta(P)`.

Choose an optimal K in (1), and let `F=P[V\K]`. For any retained x in Q,
every F-predecessor of x also belongs to Q because Q is an ideal of P.
Thus `Q[V(Q)\K]` is an ideal of F. An ideal of a Ferrers down-set is again
a Ferrers down-set. Consequently

\[
 \delta(Q)\leq|K\cap V(Q)|\leq|K|=\delta(P).
 \tag{3}
\]

This is **not** monotonicity under arbitrary induced restriction. The
three-element V, a minimum below two incomparable maxima, is Ferrers with
defect zero. Removing its minimum leaves the two-antichain, with defect one.

Every maximal birth `T=P+x_S`, with S an ideal of P, retains P as an ideal.
Lemma 1 supplies the lower bound below. For the upper bound put the newborn
into an optimal exceptional set for P, retaining the same induced F:

\[
 \delta(P)\leq\delta(P+x_S)\leq\delta(P)+1.
 \tag{4}
\]

Thus every birth increment is either zero or one. Absolute defect can never
fall along an actual history; its ratio to order size might fall. Fixed-k
sublevels `{P:delta(P)<=k}` are closed under order ideals and hence under
maximal deletion, but not asserted closed under arbitrary induced suborders.
These closure properties alone say nothing about compatible transition
probabilities or the ratio-component status of neutral increments.

### A raising option and a neutral option

For every **nonempty** P, an empty-precursor birth adds an isolated vertex.
Any induced suborder containing it and an old vertex has at least two minima,
so cannot be nonempty Ferrers. The largest retained Ferrers order after that
birth has size `max(f(P),1)=f(P)`. Equation (2) therefore gives

\[
 \delta(P+x_\varnothing)=\delta(P)+1\qquad(P\ne\varnothing).
 \tag{5}
\]

The empty parent is different: its sole birth produces a singleton, and
both defects are zero.

Every P also has at least one **neutral** birth. Choose a largest induced
Ferrers suborder F and an addable corner in a Ferrers representation of F.
Let I be that corner's strict past in F, an ideal of F. Lift it to the ideal

\[
 S=\mathord\downarrow_P I
   =\{p\in P:p\leq i\text{ for some }i\in I\}.
 \tag{6}
\]

Because F is induced and I is an ideal of F, `S intersect F=I`. Therefore
`F+x` inside `P+x_S` is exactly the enlarged Ferrers order. Keeping the
same exceptional vertices shows `delta(P+x_S)<=delta(P)`; (4) makes it an
equality. For the empty order choose its first corner and `I=S=empty`.

This is an existence argument for an eligible ideal. It does not choose a
stored optimizer, enforce record-read permissions for an implemented selector,
or prove that choices in different rows are compatible with common component
scales. No new branch law is defined by (6).

## 3. Why requiring an ideal exceptional core is unsuitable

For comparison only, define

\[
 \iota(P)=\min\{|K|:K\text{ is an ideal of }P,
                    \ P[V\setminus K]\text{ is Ferrers}\}.
 \tag{7}
\]

The empty retained order is again allowed. Always `delta(P)<=iota(P)`, but
the latter diagnostic can change extensively in one birth.

**Twin-maxima lemma.** A Ferrers order with two distinct maximal vertices
having identical strict past is exactly the three-element V.

To prove it in a diagram, write the incomparable maxima as `(i,j),(k,l)`
with `i<k` and `j>l`. Equality of their pasts forces `j=l+1`: otherwise
`(i,j-1)` is below the first but not the second. Similarly `k=i+1`, using
`(k-1,l)`. If `i>0`, the cell `(i-1,j)` still distinguishes their pasts;
if `l>0`, so does `(k,l-1)`. Hence the maxima are `(0,1),(1,0)`.
Downward closure supplies `(0,0)`. Any other cell would dominate one of
these maxima, contradicting maximality. The entire diagram is the V.

Now let R be a non-chain rectangle, the product of chains of lengths
`a,b>=2`, of size `N=ab>=4`. Let m be its unique maximum, and form T by
adding a clone y with past `B=R\{m}`. The two tops m,y have identical
strict past B and T has `N+1>=5` vertices. The lemma excludes Ferrers T.
Removing either top leaves a rectangle isomorphic to R, so

\[
 \delta(T)=1.
 \tag{8}
\]

If an ideal K contains either top, it must contain B. It has at least N
vertices; containing both costs `N+1` and leaves the allowed empty order.
If it contains neither top, both survive with equal strict past `B\K`.
A Ferrers retained order must be the V, forcing exactly one surviving B
vertex and hence `|K|=N-2`.

This latter bound is attained. Choose either coatom p of R and set
`K=R\{m,p}`, not including y. The coatom is maximal in B, so K is an
ideal of T. The retained vertices `{p,m,y}` form the V. Therefore

\[
 \boxed{\delta(T)=1,\qquad\iota(T)=N-2.}
 \tag{9}
\]

For square rectangles `a=b=s`, one birth changes iota from zero to
`s^2-2`, a fraction `(s^2-2)/(s^2+1)` of the child tending to one, while
delta changes only to one. This is a structural counterexample to the
ideal-core diagnostic's robustness, not a typical-history or shape claim.
No original vertices are actually removed by either diagnostic.

## 4. Deterministic height, width and order-density error bounds

Let K be any exceptional set of size k for an N-vertex P, and let
`F=P[V\K]` have size `m=N-k`. The following bounds hold for any induced
retained order, even before using that F is Ferrers. Height H counts vertices
in a longest chain; width W counts vertices in a largest antichain. Set both
to zero on the empty order. Intersecting a chain or antichain with F loses
at most k vertices, whereas all F chains and antichains remain in P. Thus

\[
 H(F)\leq H(P)\leq H(F)+k,\qquad
 W(F)\leq W(P)\leq W(F)+k.
 \tag{10}
\]

For `m>=1` (so also `N>=1`), dividing with the appropriate denominators gives

\[
 \left|\frac{H(P)}N-\frac{H(F)}m\right|\leq\frac{k}N,
 \qquad
 \left|\frac{W(P)}N-\frac{W(F)}m\right|\leq\frac{k}N.
 \tag{11}
\]

For example, writing `H(P)=H(F)+e`, `0<=e<=k`, the difference lies in
`[-(k/N)(H(F)/m),(k/N)(1-H(F)/m)]`. The width proof is identical. If
`m=0`, these retained normalized quantities are undefined; use (10) and
the trivial parent bounds instead. The empty parent has no normalization
by N.

For orders of size at least two define comparable-pair density by
`d(P)=C(P)/binom(N,2)`, where C counts unordered distinct pairs that are
comparable. Inducedness preserves every pair entirely inside F. The number
of remaining pairs is `binom(N,2)-binom(m,2)`. For `N,m>=2` put
`w=m(m-1)/(N(N-1))`. Then

\[
 d(P)=w\,d(F)+e,\quad 0\leq e\leq1-w,
\]
\[
 |d(P)-d(F)|\leq1-w
 =\frac{k(2N-k-1)}{N(N-1)}\leq\min(1,2k/N).
 \tag{12}
\]

The final inequality is immediate for k=0; for `k>=1` it uses
`2N-k-1<=2(N-1)`. If `m<2`, no ordinary retained pair-density denominator
exists, so (12) is not asserted. For `N>=2` only the raw counting bound
`0<=C(P)<=binom(N,2)` is then supplied; for `N<2` d(P) is also undefined.

Applying these estimates with `k=delta(P)` transfers normalized H/W and
pair-density limits from a selected sequence of optimal retained orders,
provided the relevant limits have separately been proved and `k/N->0`.
Large N then gives `m>=2` eventually for pathwise convergence, or with
probability tending to one for convergence in probability. Optimizers at
different N need not be nested; they do not automatically form their own
coherent Ferrers growth history.

For a probabilistic pair-density comparison, assign any bounded placeholder
when `m<2`. That event has vanishing probability and cannot change convergence
in probability; the placeholder is not an ordinary density on those small orders.

Sublinear defect alone supplies none of the missing shape limits. Even
defect zero includes chains, elongated rectangles and balanced rectangles.
It implies neither near-square concentration nor a spacetime dimension,
metric, measure reconstruction or source response.

## 5. Stochastic sublinearity requires a drift condition on an existing law

Assume a complete all-size family of admissible kernels has already been
fixed, with its history measure and natural filtration `F_n`. Normalized
finite-branch laws admit the [RI-39 history construction](../native_growth_history_height_v1/HISTORY_HEIGHT.md);
this section does not select such a family to control delta. Keep every
prefix row fixed. Let m be a fixed finite starting size, and put

\[
 \delta_n=\delta(P_n),\quad X_n=\delta_{n+1}-\delta_n\in\{0,1\},
 \quad\mu_n=\mathbb E[X_n\mid\mathcal F_n],
\]
\[
 C_N=\frac1N\sum_{n=m}^{N-1}\mu_n,\qquad
 M_N=\sum_{n=m}^{N-1}(X_n-\mu_n).
 \tag{13}
\]

Here C is a Cesaro drift average, not the comparable-pair count from section
4. The exact decomposition is

\[
 \frac{\delta_N}N=\frac{\delta_m}N+C_N+\frac{M_N}N.
 \tag{14}
\]

No independence between births is assumed. Conditional on `F_n`, X_n is
Bernoulli with parameter mu_n. Its centered log moment-generating function
has value and derivative zero at zero and second derivative at most `1/4`
(a tilted Bernoulli variance). Integrating this bound gives
`E[exp(s(X_n-mu_n))|F_n]<=exp(s^2/8)` for all real s. Iterating and applying
the exponential Markov inequality to both signs gives, for `N>m,t>0`,

\[
 \Pr(|M_N|\geq t\mid\mathcal F_m)
 \leq2\exp\left(-\frac{2t^2}{N-m}\right).
 \tag{15}
\]

Taking `t=epsilon N` makes the bounds summable over N for each fixed
positive epsilon. Borel-Cantelli, then a countable sequence of epsilons,
gives `M_N/N->0` almost surely. Conditional orthogonality also gives
`E[M_N^2|F_m]<=(N-m)/4`, so convergence holds in L2 and L1. No drift
regularity or rate was assumed to obtain these martingale conclusions.

Equation (14), with `0<=delta_m<=m`, now gives precise conditions:

- `C_N->0` almost surely if and only if `delta_N/N->0` almost surely.
- `C_N->0` in probability if and only if `delta_N/N->0` in probability.
- Since both nonnegative sequences lie in `[0,1]`, convergence in probability
  to zero is equivalent to L1 convergence to zero and to expectation tending
  to zero. In particular `N^(-1) sum E[mu_n]->0` is an exact expectation/L1
  criterion, up to the vanishing fixed-prefix term.

For the bounded convergence implication, any such variable Y obeys
`E[Y]<=epsilon+Pr(Y>epsilon)`; the converse follows from Markov's inequality.
Indeed, both unconditionally and conditionally on the finite starting history,

\[
 \mathbb E[\delta_N/N\mid\mathcal F_m]
 =\delta_m/N+\mathbb E[C_N\mid\mathcal F_m].
 \tag{16}
\]

Expectation or probability convergence here does not by itself supply almost
sure convergence; the corresponding almost-sure drift condition is separate.
Nor is pointwise `mu_n->0` necessary for a Cesaro condition. A deterministic
bound `mu_n<=eta_n` with `N^(-1)sum eta_n->0` would suffice almost surely,
but no such bound is established for a selected law in this note.

The finite prefix contributes a vanishing ratio without being repaired or
deleted. Its absolute defect remains a lower bound by (4). The numbers mu_n
must come from the actual compatible law and filtration; arbitrary adapted
numbers in `[0,1]` cannot be substituted as a licensed kernel. RI-38's general
extension theorem does not promise the defect drift conditions above.

## 6. Neutral increments are not ratio-component labels

For a labeled ideal S of P define the slot increment
`d_P(S)=delta(P+x_S)-delta(P)`. It is unmarked and lies in `{0,1}`, but
is not in general constant on an RI-38 proper-slot ratio component.

A minimal example is the child consisting of a two-chain plus one isolated
vertex, with predecessor masks `(0,1,0)` and defect one. Delete its isolated
maximum to get the chain `(0,1)`, defect zero: putting back the isolated
vertex is the empty-ideal birth with increment one. Delete the chain tip
instead to get the two-antichain `(0,0)`, defect one: restoring the tip with
past the old base vertex, mask 1, has increment zero.

These are directly joined proper nodes of the singleton-base diamond, with
precursors full and empty. Transporting the two newborn labels gives the
same child; all-zero records already exhibit the edge. In the unchanged
accepted prefix the actual scalar equality is

\[
 (1/3)(1/5)=(2/3)(1/10)=1/15.
 \tag{17}
\]

One side uses the chain's raising empty slot, the other the antichain's
neutral singleton slot. The whole parent and internal record coordinates
remain in each local key. Constancy of the terminal child's defect does
not make its increment constant when the two parents have different defects.
No smaller two-maximal-vertex child supplies this contrast: at size two it
is the antichain, and both singleton parents have defect zero.

Full births are also not uniformly raising. A chain's full birth gives a
longer chain and is neutral. A non-chain rectangular Ferrers parent's full
birth is not Ferrers by RI-54's intrinsic corner classification, and raises
defect from zero to one by (4).

## 7. Exact fixed-layer drift-admission criterion

Fix one size `n>=1` and the **complete actual admissible prefix** through
parent size `n-1`; in this programme the [accepted RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
is not replaced by another seed. Use the [RI-38 potential and ratio graph](../native_joint_growth_extension_criterion_v1/CRITERION.md)
with every proper node `[whole P,S,r|S]`, every mark assignment, and every
required diamond, including loops and equal-precursor pairs. For each complete
marked row j and each labeled proper ideal S, let `u_j(S)>0` be its fixed
potential and `c(j,S)` its component. Write `d_j(S)` for its increment and
`d_j(F)` for the full-ideal increment (F in this section denotes the full
slot, not the retained order from earlier sections).

A component vector alpha gives proper weights and full complement

\[
 q_j(S)=u_j(S)\alpha_{c(j,S)},\qquad
 q_j(F)=1-\sum_{S\subsetneq P_j}u_j(S)\alpha_{c(j,S)}.
 \tag{18}
\]

Every sum here is over labeled ideals, including repeated occurrences of a
component. A strict extension has all `alpha_c>0` and all full complements
positive. Its expected increment, after summing the fair newborn bit, is

\[
 \phi_j(\alpha)
 =d_j(F)+\sum_{S\subsetneq P_j}
       \bigl(d_j(S)-d_j(F)\bigr)u_j(S)\alpha_{c(j,S)}.
 \tag{19}
\]

This equals `sum_S d_j(S)q_j(S)` including the full slot. Thus `0<=phi_j<=1`
on the closed row polytope, despite possible negative coefficients in the
affine formula (19). Both newborn bits have the same unmarked increment;
their two `q/2` terms sum to q. The full passive payload D remains in the
maps; this drift observable neither replaces D nor makes it informative.

**Theorem 2 (fixed-layer criterion).** The infimum of the worst marked-row
expected increment over strict extensions is zero if and only if there is
a nonnegative boundary vector satisfying, for **every** complete marked row,

\[
 \alpha_c\geq0,\qquad
 \sum_{S\subsetneq P_j}u_j(S)\alpha_{c(j,S)}\leq1,
 \qquad\phi_j(\alpha)=0.
 \tag{20}
\]

For necessity, every component has a positive occurrence in some row, so
that row cap bounds its scale by the reciprocal of a positive incidence.
There are finitely many components and rows. The closed row polytope is
therefore compact; a sequence of strict extensions with maximum drift
tending to zero has a convergent subsequence. Continuity of all affine
phi_j gives (20). No compactness of the open strict domain is claimed.

For sufficiency, take a boundary vector alpha(0) satisfying (20) and a
strict interior extension alpha* of this same complete prefix, whose
existence RI-38 proves. For `0<t<1`, use

\[
 \alpha(t)=(1-t)\alpha(0)+t\alpha^*.
 \tag{21}
\]

All proper weights and full complements become positive, while common
component scales preserve all ratio equations, locality and equivariance.
Since (19) is affine, `phi_j(alpha(t))=t phi_j(alpha*)<=t` for every marked
row. All old rows remain fixed. This proves the claimed infimum without
admitting the zero-probability boundary as a law.

For `n>=1`, (5) and positive empty-ideal weight imply `phi_j>0` in every
strict row, so a zero infimum cannot be attained by a strict extension.
At `n=0` there is no proper-slot graph: the sole birth is neutral, of total
weight one. This exceptional trivial case is separate from Theorem 2's
nonempty-parent component argument.

### Equivalent form: only everywhere-neutral components can survive

Let `C_0` contain precisely the components whose **every** occurrence in a
complete marked row and labeled proper slot has increment zero. Consider
(19) in its nonnegative probability-sum form. If a component has even one
raising occurrence, zero drift in that row and `u_j(S)>0` force its alpha
to be zero. That also removes its neutral occurrences in other rows.
Both mixed and entirely raising components must vanish.

Conversely, with all components outside `C_0` set to zero, proper mass is
entirely neutral. Define

\[
 (A_0)_{jc}=\sum_{\substack{S\subsetneq P_j\text{ ideal}\\c(j,S)=c}}
 u_j(S)\qquad(c\in C_0).
 \tag{22}
\]

Then (20) is exactly the system

\[
 \alpha\geq0,\qquad
 A_0\alpha=\mathbf1\quad\text{on full-raising rows},\qquad
 A_0\alpha\leq\mathbf1\quad\text{on full-neutral rows}.
 \tag{23}
\]

On a full-raising row the full complement must be zero; on a full-neutral
row it can carry the remaining mass. Section 6 explains both why full
roles must be classified and why one cannot keep every slot that happens
to be neutral in its own row. Existence of a neutral ideal in every parent
does not ensure an everywhere-neutral component capable of satisfying the
simultaneous normalization constraints.

No feasibility verdict for (20) or (23) is supplied, and no new layer is
enumerated. Even a future positive finite-layer verdict would not prove
feasibility at every later layer for the prefix it creates, nor the Cesaro
drift conditions of section 5. An all-size compatible selection with those
properties would require a separate proof.

## 8. Evidence, limits and source-stable handoff

This packet is analytic. The clone example and the three-vertex mixed-component
example are proved directly; no project checker, new finite layer, numerical
search or external toy execution is used. The admitted RI-38 premises and
history-measure setup are dependencies, not newly derived DET principles.
The accepted exact-Ferrers obstruction is not undone by changing the diagnostic.

Three independent reviewers read the complete note and found no mathematical
blocker. Their separate derivations checked the ideal/twin-maxima and support
lemmas, all normalization and small-order cases, the conditional Bernoulli
martingale argument, and both forms of the marked finite-layer criterion.
The mixed-component counterexample was checked against the actual accepted
prefix probabilities. Review added an explicit bounded placeholder for
probabilistic density comparisons on the vanishing-probability small-order
event; no ordinary density is assigned there. This is analytic verification,
not a theorem-prover run or numerical feasibility test. Coordinator adjudication
is separate and recorded in the opening status.

The outputs are a frozen diagnostic definition, structural lemmas, deterministic
error bounds, conditional stochastic criteria and an exact finite admission
equivalence. There is no chosen exception selector, repaired history, feasible
defect law, proved sublinear defect, near-square concentration, informative
quantum coupling, metric, physical clock, source or gravity. Option B and
metric-as-record Status M remain unchanged; RET remains paused.

Only this new `DEFECT.md` is authored. Accepted research, measurements and
coordinator records remain untouched. The coordinator owns git/index/push.
Stop at the source-stable handoff for independent adjudication; no executor,
selection law, later-layer table or successor is started here.
