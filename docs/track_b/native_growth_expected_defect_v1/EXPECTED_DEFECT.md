# RI-59 — a history-weighted expected-defect candidate

24 September 2026 UTC. **Conditional all-size candidate construction;
independent coordinator adjudication accepted.** This note specifies one
reproducible rational selection law extending the actual accepted prefix.
At each free layer it minimizes the next expected defect increment under
the already-fixed history distribution, resolves ties canonically, and mixes
with a summably small strict interior contribution. Compatibility and the
all-size history measure follow. Sublinear defect does not yet follow.

The precise unresolved obligation is the asymptotic Cesaro behavior of the
minimum values produced by this very recursion. No layer is numerically solved
here, and no executor, new table, alternative seed or empirical claim is added.

## 1. Fixed premises and what is being selected

Retain the complete [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through parent size four, including its actual rational seed and every record
assignment. Its [certificate](../native_growth_height_normalization_v1/CERTIFICATE.json)
has SHA-256
`3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`;
the canonical roots/default/overrides parameter identity is
`465c5de48c69527fc59e8df1f494fd8cea33f8aec243f59b9b2820bd5b1c07a7`.
No previously fixed row or coefficient is optimized again.

Use the [RI-38 conditional model](../native_joint_growth_extension_criterion_v1/CRITERION.md):
one maximal committed birth per step, every ideal eligible, strictly positive
ideal/bit weights, fair immutable binary marks, strict precursor-record reads,
permitted whole-unmarked-parent order access, marked-parent equivariance and
complete natural-label diamonds. Context and residual carrier remain fixed.
The full passive maps are

\[
 \mathcal B^{P,r}_{S,b}(D)=\frac{q_{P,r}(S)}2D.
 \tag{1}
\]

The entire unnormalized kernel D, including its off-diagonal entries, is
retained. Probabilities are independent of D in this chosen model; no
informative quantum coupling is derived.

Use [RI-56's intrinsic defect](../native_growth_ferrers_defect_v1/DEFECT.md),
the minimum number of arbitrary exceptional vertices leaving an induced
Ferrers order. It is a diagnostic, not deletion of committed history. At
each maximal birth the increment is zero or one, and defect is nondecreasing
along the actual history. Birth count is bookkeeping, not a physical clock.

The new choices are the expected-increment objective, canonical tie-breaking
convention and mixing schedule below. They define an explicit candidate,
not a uniquely derived DET principle or a physical optimization law.

## 2. RI-58 has weighted content, but not an asymptotic no-go

Fix a naturally labeled marked history h_R ending at a non-chain rectangle R
of size n. Let B be its strict past below the unique maximum and I_0,I_1
its two axis ideals. Put `p=q_R(B)` and `a_i=q_R(I_i)`. All these factors
are positive and evaluated at the complete inherited record of h_R.

The clone successor P has defect one and exactly the two neutral axis slots.
The corner successors F_i are Ferrers; their restored-top slots B raise.
The [RI-58 diamonds](../native_growth_defect_bottleneck_v1/OBSTRUCTION.md) give,
for both first-newborn marks u,v,

\[
 p\,x_i=a_i z_i,\qquad
 x_i=q_{P,r+u}(I_i),\quad z_i=q_{F_i,r+v}(B).
 \tag{2}
\]

Locality excludes u from x_i and v from z_i. Each next-step drift satisfies
`mu_P(u)=1-x_0-x_1` and `mu_(F_i)(v)>z_i` in a strict law, since the
distinct empty-ideal slot in each F_i also raises with positive probability.
Let bars denote the average over the corresponding fair newborn bit.
The three types of first branch have actual weights `p/2,a_0/2,a_1/2`
per bit. All other first-child drifts are nonnegative. Therefore

\[
 \mathbb E[\delta_{n+2}-\delta_{n+1}\mid h_R]
 \geq p\,\overline\mu_P+\sum_i a_i\overline\mu_{F_i}
 >p\left(1-\sum_i x_i\right)+\sum_i a_i z_i=p.
 \tag{3}
\]

The two labeled corner cylinders both occur in this sum even if their marked
successor rows are isomorphic. They are not divided out by symmetry. The
first-step increment from R is exactly one except at the two axis ideals,
so its expectation is `1-a_0-a_1`. It follows that

\[
 \mathbb E[\delta_{n+2}-\delta_n\mid h_R]
 >1-a_0-a_1+p.
 \tag{4}
\]

These are conditional history-weighted statements, not merely a maximum
over counterfactual rows. On a nonnegative boundary extension the same proof
gives the corresponding non-strict inequalities.

### The actual finite-prefix example

For `R=(0,1,1,7)` and complete record mask 1 (root bit one, all others zero),
the unchanged prefix gives

\[
 p=\frac{539}{625},\qquad a_0=a_1=\frac{1267}{44000},\qquad
 1-a_0-a_1+p=\frac{198529}{110000}.
 \tag{5}
\]

The particular labeled marked history builds the singleton, a two-chain,
the fork and then this rectangle. Its ideal factors are
`1,1/3,1/3,49/55`. Thus its scalar path weight and actual probability are

\[
 W(h_R)=1\cdot\frac13\cdot\frac13\cdot\frac{49}{55}
       =\frac{49}{495},\qquad
 \Pr(h_R)=2^{-4}W(h_R)=\frac{49}{7920}.
 \tag{6}
\]

The fork-full factor is `49/55`: its proper weights are `1/44,1/44,7/220,7/220`,
whose complement gives that fraction. Equation (6) is one specified marked
history cylinder, not an unlabeled probability or an orbit multiplicity rule.

### Why rectangle cloning cannot by itself force persistent drift

Let C_n be the event that P_n is a **non-chain** rectangle and the next
ideal is `P_n\{its unique maximum}`, irrespective of the newborn bit.
On C_n the defect rises from zero to one. Ideal monotonicity then excludes
every later whole Ferrers order, hence every later C_k. The events C_n are
mutually exclusive along each path, so

\[
 \sum_n\mathbf1_{C_n}\leq1,
\]
\[
 \sum_n\mathbb E\!\left[
 \mathbf1_{\{P_n\text{ non-chain rectangle}\}}
 q_{P_n,r_n}(P_n\setminus\{\max P_n\})\right]
 =\sum_n\Pr(C_n)\leq1.
 \tag{7}
\]

The displayed rate is defined to be zero off the indicated rectangle event.
The second assertion is an expectation bound, not a pathwise upper bound
of one for the predictable rate sum. Non-chain qualification is essential:
cloning the maximum of a two-chain gives the Ferrers V and does not raise
defect. Equation (7) bounds these certified clone contributions only. It
does not bound all actual drift contributions, prove finite total defect,
or establish sublinearity. It explains why this mechanism alone cannot
supply a persistent positive Cesaro-drift lower bound.

## 3. The distribution used at a free layer

Start at parent size `n=5`. Inductively suppose the entire strict law has
already been fixed through parent size `n-1`. For every naturally labeled
marked history h_n on `[n]={0,...,n-1}`, compute

\[
 \nu_n(h_n)=\prod_{k=0}^{n-1}\frac{q_{h_k}(S_k)}2.
 \tag{8}
\]

Its full natural order and marks uniquely specify its birth sequence by
restriction to the earlier labels. All factors in (8) belong to the fixed
prefix; no unknown size-n probability occurs. Normalization gives total
mass one over these finitely many histories.

Let j range over complete **marked-parent isomorphism classes**, retaining
all n marks. Define

\[
 \pi_j^{(n)}=\sum_{h_n:\,[h_n]=j}\nu_n(h_n).
 \tag{9}
\]

This is the unconditional size-n distribution from the empty history under
the already selected law. It is not a distribution conditioned on a realized
finite state. All distinct labeled histories in a class contribute their
own probabilities; fair-bit factors and labeled multiplicities are retained.
One scalar path weight W, a uniform distribution on rows, or a blind count
of linear extensions is not a substitute for (9).

Every finite order admits a natural labeling and every assignment of binary
marks can be born on it. At each step the chosen precursor is an ideal and
its ideal/bit branch has positive probability. Thus every complete marked
class has at least one positive history term:

\[
 \pi_j^{(n)}>0\quad\text{for every row }j,\qquad
 \sum_j\pi_j^{(n)}=1.
 \tag{10}
\]

There is no size-uniform positive lower bound on these weights in this proof.
If instead one conditioned on a particular realized finite state, many rows
could be unreachable and (10) would fail. That is not the candidate defined
here. The actual accepted prefix means a complete law table, not a selected
realized history.

## 4. Canonical component order and the exact finite minimization

Use all RI-38 proper-slot nodes `[P,S,r|S]` at size n. Retain the whole
unmarked parent, erase only marks outside S, and include every labeled ideal
occurrence in row sums. Include all old-base diamonds, full record cubes,
newborn marks, loops and equal-precursor pairs; seed isolated nodes too.

For reproducibility, on carrier `[n]` encode a strict order by
`E(P)=sum_(i prec j) 2^(n*i+j)`. Encode subsets and one-valued mark sets
by their binary masks. The canonical local key is the lexicographic minimum
of `(E(P),mask(S),mask(r|S))` over **all** vertex permutations transporting
order, ideal and marks together. A complete marked-row key similarly
minimizes `(E(P),mask(r))` over all permutations.

Order the proper ratio components by their minimum canonical local key,
in increasing integer-triple lexicographic order, and index them
`c=0,...,d_n-1`. Distinct components have distinct minimum keys. This fixes
the coordinate order used below without privileging a natural labeling.
It is an explicit tie-breaking convention, not a physical principle.

Fix the potential normalization itself by RI-38's formula, rather than
choosing arbitrary component rescalings:

\[
 u_{P,r}(S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus A,\,r|_{P\setminus A}}(S)^{(-1)^{|A|+1}}
 \quad(S\subsetneq P).
 \tag{11}
\]

All factors use smaller-parent rows and are positive. Induced labels and
marks are transported to those rows. Each factor reads only precursor marks;
RI-38 proves locality, equivariance and every required ratio identity.

For each complete marked row j, let `d_j(S)` be the zero-or-one defect
increment for its labeled ideal S, including the full ideal. Let `c(j,S)`
be the proper slot's component. For component vector alpha define

\[
 U_j(\alpha)=\sum_{S\subsetneq P_j\text{ ideal}}
                    u_j(S)\alpha_{c(j,S)},\qquad
 K_n=\{\alpha\geq0:U_j(\alpha)\leq1\text{ for every }j\},
 \tag{12}
\]

and the affine drift

\[
 \phi_j(\alpha)=d_j(P_j)+
 \sum_{S\subsetneq P_j\text{ ideal}}
       (d_j(S)-d_j(P_j))u_j(S)\alpha_{c(j,S)}.
 \tag{13}
\]

The full complement is `1-U_j(alpha)`. Therefore (13) is a nonnegative
probability-weighted sum of increments and lies in `[0,1]` on K_n, even
though some displayed coefficients can be negative. All proper components
are retained; neutral slots are not assumed to form complete components.

K_n is nonempty (it contains zero), closed and bounded: every component
has a positive occurrence in some row, whose cap bounds that coordinate.
Hence it is compact. All current data are rational by induction from the
accepted rational seed: finite history sums, positive finite products and
ratios in (11), and integer defect increments preserve rationality.

Define the current expected-drift objective and its minimum by

\[
 \Phi_n(\alpha)=\sum_j\pi_j^{(n)}\phi_j(\alpha),\qquad
 m_n=\min_{\alpha\in K_n}\Phi_n(\alpha).
 \tag{14}
\]

A compact rational polytope and rational affine objective give an attained
rational optimum. For a fully specified unique minimizer, start with
`K_n^(0)={alpha in K_n:Phi_n(alpha)=m_n}`. Successively, for
`c=0,...,d_n-1`, set

\[
 t_c=\min_{\alpha\in K_n^{(c)}}\alpha_c,\qquad
 K_n^{(c+1)}=\{\alpha\in K_n^{(c)}:\alpha_c=t_c\}.
 \tag{15}
\]

Each face is nonempty compact and rational. After all coordinates are fixed
exactly one vector remains; call it `alpha_n^min`. Its entries are rational.
Finite vertex enumeration and exact rational linear algebra, or exact linear
optimization at each stage, establish finite computability. Finite enumeration
of orders, markings, ideals, permutations and induced subsets also computes
all input data and defect values. No efficient algorithm or physical means
of performing this calculation is claimed, and none is run in this packet.

Because all pi_j are positive and all phi_j are nonnegative,

\[
 m_n=0\quad\Longleftrightarrow\quad
 \text{RI-56's simultaneous zero-drift boundary system is feasible.}
 \tag{16}
\]

Changing to history weights does not evade a finite exact zero-drift
obstruction. It changes which positive drift costs are minimized. The
minimum may be positive at every finite size while its long-run average
could still vanish; no such asymptotic behavior is presumed.

## 5. Strict mixing defines a complete all-size law

Compute from the same fixed-prefix potentials

\[
 M_n=\max_j\sum_{S\subsetneq P_j\text{ ideal}}u_j(S),\qquad
 c_n=\frac1{2(1+M_n)},\qquad
 \boldsymbol c_n=c_n\mathbf1.
 \tag{17}
\]

Every proper probability `u_j(S)c_n` is positive, total proper row mass is
less than one half, and every full complement exceeds one half. This is an
explicit RI-38 strict interior vector in K_n.

For every `n>=5`, choose exactly

\[
 \eta_n=\frac1{(n+1)^2},\qquad
 \alpha_n=(1-\eta_n)\alpha_n^{\min}+\eta_n\boldsymbol c_n.
 \tag{18}
\]

Define the new complete layer by

\[
 q_{P,r}(S)=u_{P,r}(S)(\alpha_n)_{c(P,S,r|S)}\quad(S\subsetneq P),
 \qquad q_{P,r}(P)=1-\sum_{S\subsetneq P}q_{P,r}(S).
 \tag{19}
\]

Every component scale is positive. Every full complement is a convex mixture
of a nonnegative boundary complement and an interior complement, hence exceeds
`eta_n/2`. All ideal probabilities sum to one; each newborn bit receives
half its ideal probability through (1).

All ratio edges have their endpoints scaled by the same component constant,
so the complete scalar-map diamonds hold. Full complements enter no new
diamond as second precursors. Canonical keys and component ordering preserve
marked-parent equivariance. Proper probabilities have only the allowed
precursor-record dependence; the full ideal may read all parent marks.
Earlier rows are unchanged. This supplies a valid strict prefix for the
next inductive step.

### Global law construction is not a realized-state record read

Equations (8)–(18) use the distribution of **all counterfactual histories**
to set fixed layer parameters once. That is part of defining the complete
law. They do not condition on the realized current history or recompute the
optimizer after inspecting its outside-precursor marks. At runtime, the
proper slot uses only its whole unmarked P, its ideal S and r restricted
to S, through its local key and the directly local potential (11). There
is no runtime lookup of pi at the actual full marked row in (19).

This distinction is load-bearing. A state-conditioned or continually
reoptimized policy would be a different candidate and could violate the
stated locality or positivity arguments. All current data here depend only
on already-fixed smaller-parent laws: pi_n uses births up to parent n-1,
as do the potentials. The recursion has no lookahead or circular dependence
on its own new layer.

Starting from the actual size-four prefix, induction therefore defines a
strict rational all-size family. Its normalized finite-history distributions
are consistent, so the [RI-39 construction](../native_growth_history_height_v1/HISTORY_HEIGHT.md)
gives the classical infinite-history measure. The complete passive kernel
on a cylinder remains its probability times D. No all-size informative
quantum extension or physical interpretation is inferred from that measure.

## 6. What performance is proved for this very recursion

Let `r_n=E[delta_(n+1)-delta_n]` under the law just defined. The distribution
of its size-n parent rows is exactly the pi_n used in that step, since the
new layer cannot change earlier history probabilities. Affinity gives

\[
 r_n=\Phi_n(\alpha_n)
     =(1-\eta_n)m_n+\eta_n\Phi_n(\boldsymbol c_n),
\]
\[
 0\leq r_n-m_n
 =\eta_n\bigl(\Phi_n(\boldsymbol c_n)-m_n\bigr)\leq\eta_n,
 \quad\text{so}\quad m_n\leq r_n\leq m_n+\eta_n.
 \tag{20}
\]

Here `Phi_n(c_n)>=m_n` because the interior vector belongs to the same K_n,
and its expected drift is at most one. The deterministic numbers m_n are
**endogenous** to this recursion: today's choice changes later history
weights and potentials. They are not optima over complete future laws,
finite horizons or arbitrary trajectories, and need not be monotone in n.

The mixing errors are summable; for example
`sum_(n>=5) eta_n<=integral_5^infinity x^(-2) dx=1/5`. For `N>=5`,

\[
 \mathbb E\delta_N=\mathbb E\delta_5+
                 \sum_{n=5}^{N-1}m_n+e_N,
 \qquad0\leq e_N\leq\sum_{n=5}^{N-1}\eta_n\leq\frac15.
 \tag{21}
\]

The actual finite-prefix defect is retained, not assumed zero or repaired.
Its finite expectation divided by N vanishes. Hence

\[
 \mathbb E[\delta_N/N]\longrightarrow0
 \quad\Longleftrightarrow\quad
 \frac1N\sum_{n=5}^{N-1}m_n\longrightarrow0.
 \tag{22}
\]

Since `0<=delta_N/N<=1`, expectation convergence to zero is equivalent to
L1 and convergence in probability to zero. For example bounded Y satisfies
`E[Y]<=epsilon+Pr(Y>epsilon)`, and Markov's inequality gives the converse.
Thus the same Cesaro condition is necessary and sufficient for those three
versions of normalized sublinear defect for this candidate.

It does **not** by itself establish almost-sure sublinearity. On a realized
history the conditional drift is `mu_n=phi_(j_n)(alpha_n)`; (20) bounds only
its expectation, not every row or its pathwise value. RI-56's separate
martingale result says `delta_N/N->0` almost surely exactly when
`N^(-1)sum mu_n->0` almost surely. No such pathwise condition is proved here.

### A stronger sufficient condition

If `sum_(n>=5)m_n<infinity`, then (20) and Tonelli give

\[
 \mathbb E\!\left[\sum_{n=5}^{\infty}
           (\delta_{n+1}-\delta_n)\right]
 =\sum_{n=5}^{\infty}r_n
 \leq\sum_{n=5}^{\infty}m_n+\sum_{n=5}^{\infty}\eta_n<\infty.
 \tag{23}
\]

The total number of post-prefix defect increments is then finite almost
surely and in expectation. Since increments are nonnegative integers, defect
eventually becomes constant on almost every path, with an integrable limit;
monotone convergence also gives L1 convergence of delta_N to that limit.
Conversely finite expected total increments forces summable m_n by (20).
Almost-sure finiteness alone need not imply finite expectation. None of
these summability premises is established for the candidate.

## 7. The first cost is positive; the asymptotic obligation stays open

RI-58 and (16) already imply `m_5>0`. A quantitative history-weighted lower
bound follows without evaluating the new optimization. For every alpha in
K_5, use the non-strict boundary version of (3), condition on the particular
h_R from (6), and use nonnegative drift on all other histories. The old
distribution is fixed independently of alpha. Therefore

\[
 \Phi_5(\alpha)\geq\Pr(h_R)p
 =\frac{49}{7920}\frac{539}{625}
 =\frac{2401}{450000},\qquad
 m_5\geq\frac{2401}{450000}>0.
 \tag{24}
\]

This uses both fair newborn-bit choices in the clone and two labeled corner
branches: six first-step marked cylinders. Using only their zero-bit rows
would lose a factor of one half. Grouping isomorphic marked row states in
pi_5 sums these cylinder weights; it does not remove their multiplicity.
Equation (24) is a lower bound, not a computed optimum m_5.

A positive cost at this single layer contributes only a finite term to
(21). It neither decides (22) nor forces a divergent sum in (23). Likewise
the mutually exclusive exact-rectangle cloning mechanism in (7) cannot
alone resolve the future expected-drift sequence.

The remaining proof obligation for this fully specified candidate is to
establish or refute

\[
 \boxed{\frac1N\sum_{n=5}^{N-1}m_n\longrightarrow0}
 \tag{25}
\]

along the prefixes generated by (8)–(19). Summability of m_n would be a
stronger sufficient result. An almost-sure sublinearity claim instead needs
the separate pathwise condition stated after (22), or another valid argument.
Compactness, positive history support, myopic minimization and summable
mixing do not themselves prove any of these missing estimates.

## 8. Analytic evidence and bounded handoff

This packet is a mathematical definition and proof, not an executed optimizer.
No new executor, finite-layer table, linear-program run or numerical search
was performed. Prefix fractions (5)–(6) and (24) are derived analytically
from the accepted constants. The all-size statement is conditional on the
same declared model and seed, not a derivation of them from DET primitives.

The main author and three independent reviewers read the complete note.
Their analytic reviews found no mathematical or scope blockers: the weighted
rectangle argument and exact history factors, canonical rational optimization
and runtime locality, and performance/convergence distinctions were checked.
These are human-readable proof reviews, not theorem-prover verification or
executed optimization. All six local links resolve; the RI-41 certificate
hash matches the identity above. Scoped whitespace/conflict-marker checks
found no issues, and the reserved directory contains only this note.

The construction proves a compatible strict candidate and exact performance
reductions. It does not prove asymptotic decay of m_n, sublinear defect,
balanced Ferrers morphology, near-square concentration, horizon/global
optimality, a metric, source response, physical clock, gravity or informative
quantum coupling. Option B and metric-as-record Status M are unchanged.

Only this new `EXPECTED_DEFECT.md` is authored. All actual records, accepted
sources, measurement work and coordinator records remain untouched; RET
stays paused. The coordinator owns git/index/push. Stop at the source-stable
one-file handoff for independent adjudication; no finite enumeration or
successor implementation is automatically authorized by this note.
