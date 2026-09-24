# RI-43 — sublinear-height selection: structural reduction and a rejected rule

24 September 2026 UTC. **Bounded analytic result; independent coordinator
adjudication accepted. The all-parent vanishing-drift target remains open.**

This note proves the cumulative actual-height drift criterion, identifies
the component structure relevant to height preservation, and gives an exact
fixed-layer zero-infimum criterion. It also constructs and rejects an explicit
all-size antichain-focused rule: antichain drift tends to zero, but its actual
histories have `H(P_N)/N -> 1` almost surely. That negative result is not an
impossibility theorem for all component-scale selections.

The actual blocker is simultaneous row balancing across successive changed
prefixes. Neither a propagating feasibility invariant yielding uniform
`delta_n -> 0` nor a general obstruction to that invariant has been proved.
The supporting drift lemma is not presented as closing this selection problem.

## 1. Fixed domain and the target not yet established

Hold the complete accepted [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through **parent size four** fixed, including its rational component scales,
all marks and the earlier `f(0)!=f(1)` feedback. Rows from size five onward
must be constructed from that actual prefix, not copied from RI-39's different
normalization. A seed law table is distinct from an observed finite history.

Retain [RI-38's premises](../native_joint_growth_extension_criterion_v1/CRITERION.md):
finite committed orders, immutable independent binary record coordinates,
strictly positive probabilities for every ideal, strict precursor-record
locality, permitted whole-parent unmarked order access, marked-parent
equivariance, one commit per step and no halt/silent branch. The newborn bit
is fair, and the complete passive map remains

\[
 \mathcal B^{P,r}_{S,b}(D)=q_{P,r}(S)D/2.
 \tag{1}
\]

All entries of the fixed-carrier complex PSD residual are retained. Equality
of two scalar multipliers is equality on the entire admitted unnormalized
kernel cone. Nothing here derives informative quantum-to-order coupling.
Record count is not a physical clock. These are conditional mathematical
premises, not DET entailment, a geometric model or a source/gravity law.

For every selected all-size extension, normalized finite branching supplies
the classical marked-history measure by the construction in
[RI-39](../native_growth_history_height_v1/HISTORY_HEIGHT.md). Its height
theorem required that note's particular normalization and is **not** inherited
by every extension. This note uses only its general history construction.

The strong requested selection target is one fixed law with

\[
 \tau_n(P,r):=\sum_{S:H(S)=H(P)}q_{P,r}(S),\qquad
 \sup_{|P|=n,r}\tau_n(P,r)\leq\delta_n,\qquad\delta_n\longrightarrow0.
 \tag{2}
\]

Here `H(empty)=0` and height counts chain vertices. Both newborn marks are
summed. All parameters are chosen from complete fixed law tables, not from
forbidden current record reads. The finite prefix may require large initial
bounds; a finite number of such bounds does not affect the limiting target.

## 2. Supporting theorem: actual cumulative conditional height drift

Write `F_n` for the complete marked history through `n` events. For `n>=4`,
let

\[
 Y_{n+1}=H(P_{n+1})-H(P_n)\in\{0,1\},\qquad
 t_n=\mathbb E[Y_{n+1}\mid\mathcal F_n]=\tau_n(P_n,r_n).
 \tag{3}
\]

The first increment, from size four to five, uses the fixed RI-41 row;
only subsequent rows are newly selected. For `N>=5`, set `m=N-4` and

\[
 A_N=\sum_{n=4}^{N-1}t_n,\qquad
 M_N=\sum_{n=4}^{N-1}(Y_{n+1}-t_n).
\]
\[
 H(P_N)=H(P_4)+A_N+M_N.
 \tag{4}
\]

This is a martingale decomposition with respect to the whole history, not
an independent-birth approximation. Conditionally on `F_n`, `Y_(n+1)` is
Bernoulli of parameter `t_n`. The centered log-moment-generating function
has value and derivative zero at the origin; its second derivative is the
variance of a tilted Bernoulli, at most `1/4`. Integrating twice gives, for
every real `s`,

\[
 \mathbb E[e^{s(Y_{n+1}-t_n)}\mid\mathcal F_n]\leq e^{s^2/8}.
 \tag{5}
\]

Iterating conditional expectations and applying exponential Markov with
`s=4 epsilon` to either sign yields

\[
 \Pr\{|M_N|\geq\epsilon m\mid\mathcal F_4\}
 \leq 2e^{-2\epsilon^2m},\qquad\epsilon>0.
 \tag{6}
\]

The right side is summable over `m`. The first Borel--Cantelli argument,
applied to a countable sequence of positive rational thresholds, proves
`M_N/m -> 0` almost surely. Since `|M_N|/m<=1`, dominated convergence gives
`E|M_N/m|^p -> 0` for every `0<p<infinity` (ordinary `L^p`-norm convergence
when `p>=1`). Orthogonality of
martingale differences also gives `E[M_N^2|F_4]<=m/4`. No convergence in
`L^infinity` or independence of increments is asserted.

### Modes of convergence

Keeping the finite offset `H(P_4)/N`, equation (4) proves:

- `H(P_N)/N -> 0` almost surely iff `A_N/N -> 0` almost surely.
- The same equivalence holds in probability.
- Exactly,
  `E H(P_N)/N = E H(P_4)/N + (1/N) sum_(n=4)^(N-1) E t_n`.

Both normalized height and predictable cumulative drift lie in `[0,1]`.
For convergence to zero, convergence in probability, convergence in `L^1`,
vanishing expectation and convergence in every finite `L^p` are therefore
equivalent for either quantity. For example, if `0<=Z_N<=1`, then
`E Z_N <= epsilon + Pr(Z_N>epsilon)`; the reverse implication follows from
Markov's inequality. The corresponding finite-`p` assertions follow from
boundedness.

Almost-sure convergence implies these weaker modes; no converse is supplied.
The concentration estimate controls `H-A`, not convergence of the random
predictable average `A_N/N`. After conditioning on another positive-probability
finite marked history, restart the sums and filtration at that history's
cutoff and retain its finite height offset to obtain the analogous exact
expectation and tail statements. Equations (4)--(6) as written use cutoff
four; unconditioning there is a finite mixture. Finite changes of cutoff do
not change the asymptotic equivalences. The same proof transfers any other
established limit of `A_N/N` to `H(P_N)/N` in the stated mode.

In particular, (2) would give `A_N/N <= (1/N) sum delta_n -> 0` pathwise
and thus sublinear height almost surely and in the weaker modes. This is
**conditional on the existence of the selector**, not a construction of it.
A constant upper bound below one half is insufficient for this conclusion.

## 3. Which ratio components can preserve height?

Fix a next layer `n>=1` and its positive RI-38 maximal-deletion potential
`u`. A proper-slot node is `[P,S,r|S]`. It determines the unmarked child

\[
 T=P+e_S.
 \tag{7}
\]

Record erasure in the quotient changes no order. A raw diamond compares two
last-birth roles in the same unmarked `T`; hence every connected component
has a fixed unmarked child type. Different record components may have the
same child type; no identification of all such components is assumed.

Because `S` is proper, `T` has at least two maximal vertices. Complete a
representative node's permitted marks to one marked child. Every
maximal-deletion role of **that completion** is represented in the node's
component: compare its newborn with any other maximal vertex using the
base obtained by deleting both. The two precursors are ideals of that base;
the admitted old/newborn marks and the positive prefix supply the raw edge.
Its endpoints may coincide in the quotient, but no such role is omitted.
This does not assert that a component exhausts every local representation
or every marked completion of the unmarked child type.

Call a maximal vertex **tallest** if a chain of length `H(T)` ends there.

**Component lemma.** There are two types of proper-slot component:

1. If `T` has at least two tallest maxima, deleting any maximal vertex leaves
   a chain of length `H(T)`. Every incoming slot preserves height. Call this
   a *preserving-only component*.
2. If `T` has exactly one tallest maximum, deleting it lowers height by
   exactly one, while deleting any other maximum leaves height unchanged.
   The component contains both a height-raising and a height-preserving slot.
   Call it *mixed*.

For the second assertion, a longest chain ending at the unique tallest
vertex leaves a chain of length `H(T)-1` after deletion; no chain of full
length remains. Distinct maxima are incomparable, so deleting one cannot
destroy a longest chain ending at another. These facts also prove the first
assertion. The fixed local record quotient does not alter either argument.

Every row has a preserving-only option. Choose a tallest maximal vertex
`v` of `P` and append a vertex with the same strict past as `v`. This is a
proper ideal of height `H(P)-1`; the child has two tallest maxima, the old
`v` and its new counterpart. This proves support exists in each row. It does
**not** show that the shared component scales can normalize all rows at once.

## 4. A precise fixed-layer completion criterion

Use RI-41's matrices, still counting every distinct labeled ideal:

\[
 A_{jc}=\sum_{S\text{ proper in row }j,\ c(S)=c}u_j(S),\qquad
 B_{jc}=\sum_{\substack{S\text{ proper in row }j,\ c(S)=c\\H(S)<H(P_j)}}u_j(S).
 \tag{8}
\]

Strict laws have `alpha>0`, `A alpha<1` and `tau=1-B alpha`. The full
complement is itself height-raising. Let `A_0` be the columns of `A` for
preserving-only components; on those columns `A_0=B_0`.

**Fixed-layer theorem.** The infimum of worst-row drift over strict
component scales is zero iff

\[
 A_0\beta=\mathbf1\quad\text{for some }\beta\geq0.
 \tag{9}
\]

**Proof.** The closed relaxation `alpha>=0,A alpha<=1` is compact: each
component has a positive occurrence in some row, bounding its coefficient.
It contains strict points by RI-38. Mixing any closed point with a strict
point approaches it through strict points, so the closed minimum of the
continuous worst-row drift equals the strict infimum.

If that minimum is zero, `B alpha=1`. Since `0<=B<=A` and `A alpha<=1`,
also `A alpha=1` and `(A-B) alpha=0`. Every mixed component has a positive
entry in `A-B`, so its coefficient must vanish. All full complements vanish
too. The remaining equations are exactly (9). Conversely, a nonnegative
solution of (9), with mixed coefficients zero, is a closed zero-drift point.
Mix it with any known strict extension `alpha*`:

\[
 \alpha_t=(1-t)\alpha_0+t\alpha^*,\qquad0<t<1.
 \tag{10}
\]

All proper probabilities and full complements are positive, and
`tau(alpha_t)=t tau(alpha*)<=t` in every row. This proves the theorem.

The boundary point (9) is an auxiliary mathematical object, **not** an
accepted law: its zero full complements violate the retained premises.
Only the mixtures in (10) are strict. A target with arbitrarily small drift
is not attained at zero inside the strict domain.

This supplies a concrete possible invariant, not an established one: prove
that appropriate choices of these strict mixtures preserve (9) for every
subsequent recomputed prefix. The current work has **not** proved (9) at
every later layer from the fixed RI-41 prefix, nor that it propagates after
a mixture is chosen. Its exact feasibility at every layer would also be
stronger than necessary: positive layer infima tending to zero could meet
(2). A failure of (9) at one finite layer would not reject that weaker route.

## 5. Cross-height diamonds narrow the choices but do not give a no-go

Take a size-`n-1` marked parent `C` of height `h`. Choose an ideal `S` with
`H(S)=h` and form `P=C+x_S`, of height `h+1`. For any old ideal `T` with
`H(T)<h`, the alternative intermediate parent `Q=C+y_T` still has height
`h`. If a uniform bound `tau_n<=delta_n` holds, the second birth at `S`
raises height in `Q`, so `q_Q(S)<=delta_n`. The full diamond gives

\[
 q_C(S)q_P(T)=q_C(T)q_Q(S),\qquad
 q_P(T)\leq\delta_n\frac{q_C(T)}{q_C(S)}.
\]
\[
 \sum_{T:H(T)<h}q_P(T)
 \leq\delta_n\frac{1-\tau_{n-1}(C,r)}{q_C(S)}.
 \tag{11}
\]

Strict positivity justifies division. Newborn marks are retained and their
fair factors cancel; the second old ideal cannot read the other newborn's
mark. The inequality is conditional on the stated uniform bound.

For pairs of old ideals both of height `h`, both second births instead
preserve height in their intermediate parents. The corresponding block
satisfies `q_C(S) K_ST=q_C(T) K_TS`, where `K_ST=q_(C+x_S)(T)`. Diagonal
and equal-precursor terms are included. They are not forced small by (11).
Nor need `q_C(S)` stay bounded away from zero as the layer changes.

Thus (11) favors births near the existing top level when its ratio is
controlled; it does not contradict normalization. The same node may have
several maximal-deletion descriptions, so one cannot choose each block's
entries independently. This is another form of the simultaneous balancing
problem, not a proof that a small-drift selector exists or fails.

## 6. An explicit all-size stress rule, and its rejection

An antichain-only obstruction is impossible in this class. Here is an
explicit construction starting **after the fixed RI-41 prefix**, at `n=5`.
It is an analytic stress rule to be rejected for (2), not a recommended law.

Let `Ant_n` denote the `n`-antichain, distinct from cumulative drift `A_N`.
Its empty-ideal node has child `Ant_(n+1)`.
Every incoming role of that child is again antichain/empty; the quotient
erases every record at the empty precursor. The node therefore forms a
one-node component with only unit loops, distinct from all others. Its
potential `u_n^0>0` is independent of all actual records.

Recompute all potentials from the current selected prefix at every layer.
Define `V_n` as the maximum, over all marked rows, of the proper-potential
sum **excluding this private component**, and set

\[
 \eta_n=\frac1{n+1},\qquad
 \alpha_n^0=\frac{1-\eta_n}{u_n^0},\qquad
 \lambda_n=\frac{\eta_n}{2(1+V_n)}.
 \tag{12}
\]

Give every other component scale `lambda_n`. This is a fixed finite-table
formula at each size, not a numerical search or an actual-record-dependent
normalizer. The other proper mass in every row is strictly below `eta_n/2`.
Consequently

\[
 q_{\mathrm{Ant}_n}(\varnothing)=1-\eta_n,\quad
 q_{\mathrm{Ant}_n}(\mathrm{Ant}_n)>\eta_n/2,\quad
 \tau_n(\mathrm{Ant}_n,r)=\eta_n,
 \tag{13}
\]

whereas in every non-antichain row the private component is absent and

\[
 q_{P,r}(P)>1-\eta_n/2,\qquad
 \tau_n(P,r)>1-\eta_n/2.
 \tag{14}
\]

Every component, every proper ideal and every full complement remains
strictly positive. The scales preserve all ratios and the exact local
quotient; all full diamonds retain (1). Induction using RI-38 supplies an
all-size law without changing any earlier table. Arbitrary prescribed
positive `eta_n<1` could replace (12)'s choice for the antichain conclusion.

This demonstrates that small antichain drift neither forces small drift
elsewhere nor yields an antichain-based universal obstruction. For the
specific choice (12), the negative outcome is stronger than worst-row failure.
Conditional on `P_5=Ant_5`, remaining an antichain through size `N>=5` has
probability

\[
 \prod_{n=5}^{N-1}(1-\eta_n)
 =\prod_{n=5}^{N-1}\frac n{n+1}=\frac5N.
 \tag{15}
\]

Only an empty-precursor birth preserves an antichain. Thus the first relation
appears at a finite size almost surely. If `P_5` is already non-antichain,
no wait is needed. A relation cannot be removed by any subsequent birth, so
the process thereafter stays non-antichain. Along almost every realized path,
(14) gives `t_n -> 1`, and hence `A_N/N -> 1`. The martingale theorem proves

\[
 \frac{H(P_N)}N\longrightarrow1
 \quad\text{almost surely and in every finite }L^p.
 \tag{16}
\]

Since `0<=H(P_N)/N<=1`, bounded convergence also gives
`E|H(P_N)/N-1|^p -> 0` for every finite positive `p`. The same limit holds
in probability and expectation. This is a complete rejection
of the declared antichain-focused rule for sublinear height, not a rejection
of every rule satisfying the structural premises. Earlier feedback remains
in the law; it does not change the proof of this asymptotic screen.
All height-density limits concern this specified birth-prefix exhaustion;
invariance under arbitrary infinite natural re-enumeration is not inferred.

## 7. What remains for typical selection and what is actually blocked

For an arbitrary fixed all-size law and threshold `zeta>0`, define realized
high-drift occupation

\[
 C_N(\zeta)=\frac1N\sum_{n=4}^{N-1}\mathbf1_{\{t_n>\zeta\}}.
 \tag{17}
\]

Pathwise,

\[
 \zeta C_N(\zeta)\leq A_N/N\leq\zeta+C_N(\zeta).
 \tag{18}
\]

Therefore sublinear predictable drift is equivalent to vanishing occupation
for every fixed positive rational threshold, in the corresponding almost-sure
or in-probability mode. Expectations obey the analogous equivalence by these
same inequalities. Expected drift weights each marked row by its **actual**
history-law probability:

\[
 \mathbb E[A_N]/N=
 \frac1N\sum_{n=4}^{N-1}\sum_{(P,r)}
       \Pr\{(P_n,r_n)=(P,r)\}\,\tau_n(P,r).
 \tag{19}
\]

The sum can use canonical naturally labeled histories; any unlabeled
aggregation must sum distinct representatives with their probabilities.
It is not an unweighted average over row types. Changing earlier scales
changes both later potentials and these occupation probabilities.

Failure of a worst-row bound alone leaves this typical route open. The rule
in section 6 fails that route too: its high-drift occupation tends to one for
every threshold below one. For another rule, small expected bad-state
occupation would establish the probability/mean modes, not automatically the
almost-sure mode. A summable bound on bad-state probabilities is one stronger
sufficient route, not a necessary condition or an assumed fact.

**Precise remaining obligation:** provide one admissible, fixed all-size
component selection extending the actual RI-41 prefix, with a proved
propagating simultaneous row-feasibility estimate and a vanishing drift
envelope; or prove an asymptotic lower obstruction for that class. The
preserving-only completion cone (9) is a concrete place to seek a sufficient
invariant. A quantitative near-completion invariant could be weaker. Neither
is established here. If a typical-only candidate is explicitly chosen instead,
it needs its own actual occupation estimate such as (18)--(19), not an assumed
favorable distribution over parents.

No larger-layer enumeration, extra seed choice, new nonpassive model or
successor packet is started. The all-parent programme remains unresolved at
the stated balancing/propagation step. This is an actual missing proof,
not a conclusion drawn from an unsuccessful optimizer run.

## 8. Evidence and source-stable handoff

All new results are analytic. No checker, certificate file, simulation or
higher-layer table was needed or created, and no project executor was run.
The fixed RI-41 certificate is a premise, not a suite replayed for this note.

A primary-source boundary check used Brightwell and Luczak's
[Order-invariant measures on causal sets, introduction](https://arxiv.org/pdf/0901.0240).
It distinguishes general order-invariant growth from the narrower classical
sequential-growth family with an additional Bell-causality condition. We do
not impose that extra condition, import its parameterization, or borrow its
asymptotic conclusions for the present record-local class. The proofs above
are given directly; no external classification theorem is a premise.

Three read-only internal reviewers read the complete note. Two independently
identified the need to restart finite-time martingale sums when conditioning
on a later history; that scope correction is incorporated in section 2 and
both verified it. All three concurred with the proofs and limitations, with
no remaining mathematical blockers. Notation separates cumulative drift,
antichains and the stress-table maximum. These are internal reviews, not
coordinator acceptance or empirical evidence. No reviewer executed code,
edited source or independently reopened the external contextual reference.
All three local Markdown targets exist; whitespace/conflict-marker checks
are clean. Final SHA-256 source identities accompany the handoff.

Only this new note is authored;
accepted sources, coordinator records, measurement work and RET remain
unchanged. Root owns git/index/publication. Release this source reservation
and stop the bounded packet at stable handoff for independent adjudication.
Option B, metric-as-record Status M and the RET pause are unchanged.
