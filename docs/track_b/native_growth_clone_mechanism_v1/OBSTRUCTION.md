# RI-51 — a schedule-independent clone/full counting obstruction

24 September 2026 UTC. **Conditional analytic mechanism theorem; independent
coordinator adjudication accepted.** For every fixed deterministic sequence
`0<eta_n<1`, `n>=5`, the private-clone construction extends the complete
RI-41 prefix to an admissible all-size law. For every such law,

\[
 H_N/N\longrightarrow0\text{ and }W_N/N\longrightarrow0
 \quad\text{in probability}
 \quad\Longrightarrow\quad
 d_N\longrightarrow1\text{ in probability and }L^1.
 \tag{1}
\]

If both antecedents hold almost surely, density tends to one almost surely.
Here `H_N` is height, `W_N` width, and `d_N` the fraction of unordered
distinct pairs that are comparable in the specified birth prefix.
This is an **implication**, not an assertion that every schedule has
sublinear height or width.

Thus changing a fixed deterministic schedule alone cannot produce the
conjunction of sublinear height, sublinear width and a deterministic
interior density limit `0<rho<1` within this mechanism. No monotonicity,
power law, limit of `eta_n`, independent births or continuum premise is
needed. No theorem says every geometry must require that conjunction.

## 1. Admissibility for an arbitrary fixed deterministic schedule

Keep the complete [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through parent size four and the [RI-38 domain](../native_joint_growth_extension_criterion_v1/CRITERION.md):
strict positive ideal probabilities, immutable independent binary record
coordinates, precursor-record locality, whole-unmarked-parent access,
marked-parent equivariance, fixed context, one committed birth per step
and fair newborn marks. Full passive maps remain `B_(S,b)(D)=q(S)D/2`,
retaining the complete unnormalized complex PSD residual.

Fix the entire deterministic sequence `eta_5,eta_6,...` with each entry
strictly between zero and one. It is shared by every row of its size, not
chosen from actual current records. For this one schedule, recursively
recompute the positive local RI-38 potential from its actual prior rows:

\[
 u_{P,r}(S)=\prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus A,\,r|_{P\setminus A}}(S)^{(-1)^{|A|+1}},
 \qquad S\subsetneq P.
 \tag{2}
\]

A suitable parent is `C op Ant_k`, `k>=1`, with preferred precursor `C`.
As proved in [RI-46](../native_growth_clone_selection_v1/SELECTION.md),
its preferred ratio component is one private local marked-core node with
unit loops. Every suitable row has exactly one such labeled ideal;
unsuitable rows have none. The structural proof is independent of schedule.
Core records remain distinguished modulo core automorphisms; excluded top
marks are absent only from the local key, not from the committed state.

Let `K_n` be the set of all preferred components. Choose

\[
 V_n=\max_{|P|=n,r}
       \sum_{\substack{S\subsetneq P\text{ ideal}\\c(P,S,r|S)\notin K_n}}
       u_{P,r}(S),\qquad
 \lambda_n=\frac{\eta_n}{2(1+V_n)},
\]
\[
 \alpha_c=\begin{cases}(1-\eta_n)/u_c,&c\in K_n,\\
                         \lambda_n,&c\notin K_n,
          \end{cases}
 \quad q_{P,r}(S)=\alpha_{c(P,S,r|S)}u_{P,r}(S)\quad(S\subsetneq P),
\]
\[
 q_{P,r}(P)=1-\sum_{S\subsetneq P\text{ ideal}}q_{P,r}(S).
 \tag{3}
\]

The maximum uses the complete marked table, excludes every preferred
component and counts all labeled ideals in each row. It is finite at each
size because all inherited probabilities are positive. All scales are
positive and fixed for that table. Proper-slot evaluation reads only its
local marks; full evaluation may read the full parent records.

Let `beta_n(P,r)` be the total mass of nonpreferred **proper** ideals,
and let `q_n^full(P,r)=q_(P,r)(P)`. Then

\[
 0\leq\beta_n\leq\lambda_nV_n<\eta_n/2<q_n^{\rm full}.
 \tag{4}
\]

Indeed a suitable row has preferred mass `1-eta_n` and full complement
`eta_n-beta_n>eta_n/2`; an unsuitable row has full complement
`1-beta_n>1-eta_n/2>eta_n/2`. Every ideal/bit branch is positive and
normalization holds.

Component-constant scaling preserves all new ratios. New diamond second
precursors are proper, so no new full complement imposes an additional
ratio constraint. Inherited rows are unchanged. Locality and equivariance
of the potential and component keys carry through to the new probabilities,
and scalar equality proves equality of the entire passive maps, not just
their masses. Induction establishes all-size admissibility for every fixed
sequence in the stated interval. No regularity or asymptotic property of
the sequence enters this proof. Later rows from a different schedule must
not be copied into this recurrence.

## 2. Counts and a direct whole-history concentration bound

First fix an admitted finite history at a cutoff `m>=5`. Write `F_n` in
calligraphic form `\mathcal F_n` for its whole-history filtration. For
`N>=m`, let `B_N` count nonpreferred proper births and `F_N` count full
births at parent sizes `m,...,N-1`. These ordinary-letter counts depend
on the chosen cutoff; both are zero at `N=m`.

The three disjoint birth classes are full, preferred proper, and all other
proper births. Both newborn marks are summed in each class. Put

\[
 X_{n+1}=\mathbf1_{\{\text{other proper at }n\}}
          -\mathbf1_{\{\text{full at }n\}}\in\{-1,0,1\},
 \qquad Z_N=B_N-F_N=\sum_{n=m}^{N-1}X_{n+1}.
 \tag{5}
\]

Conditional on `F_n`, write `beta=beta_n(P_n,r_n)` and
`q=q_n^full(P_n,r_n)`. Equation (4) implies
`E[X_(n+1)|F_n]=beta-q<=0`. For every real `s>=0`, the exact conditional
moment-generating function obeys

\[
 \mathbb E[e^{sX_{n+1}}\mid\mathcal F_n]
 =1+(\beta+q)(\cosh s-1)+(\beta-q)\sinh s
 \leq\cosh s\leq e^{s^2/2}.
 \tag{6}
\]

The first inequality uses `beta+q<=1`, `beta<=q`, and nonnegative
`cosh(s)-1` and `sinh(s)`. For the second,
`log cosh(s)=integral_0^s tanh(t) dt<=s^2/2` since `tanh(t)<=t` for
`t>=0`. No independence assumption or named concentration theorem is used.

Tower iteration over the `L=N-m` increments gives
`E[exp(s Z_N)|F_m]<=exp(L s^2/2)`. Exponential Markov with `s=t/L`
therefore yields, for `N>m` and `t>0`,

\[
 \Pr(Z_N\geq t\mid\mathcal F_m)
 \leq\exp\left(-\frac{t^2}{2(N-m)}\right).
 \tag{7}
\]

At `N=m` the count difference is zero, with no division by zero needed.
For `epsilon>0`, use `t=epsilon N`: the resulting upper bound is at most
`exp(-epsilon^2 N/2)` because `N-m<=N`. It is summable over `N`.
The first Borel--Cantelli argument at every positive rational threshold
proves

\[
 Z_N^+/N\longrightarrow0\quad\text{almost surely},
 \qquad Z_N^+=\max(Z_N,0).
 \tag{8}
\]

This controls only the positive excess. It does not assert `B_N<=F_N`
pathwise, or `|B_N-F_N|/N->0`; a large negative difference is allowed.

### Any earlier finite cutoff: retain a finite-prefix offset

The fixed RI-41 rows at sizes below five have not been proved to satisfy
(4). For an arbitrary cutoff `m>=0`, put `ell=max(m,5)` and `r=ell-m`.
For `N>ell`, split the signed count at `ell`. The initial part is at most
`r` pathwise; the later part satisfies (7) conditional on `F_ell`.
Tower conditioning back to `F_m` gives

\[
 \Pr(Z_N\geq r+t\mid\mathcal F_m)
 \leq\exp\left(-\frac{t^2}{2(N-\ell)}\right),\qquad t>0.
 \tag{9}
\]

For `m<=N<=ell`, simply `Z_N<=N-m<=r`. The tail denominator is used
only when positive. For large `N`, choose `t=epsilon N-r>0` in (9),
which is at least `epsilon N/2` eventually. The tail remains summable,
so (8) holds after every finite cutoff. No pre-size-five domination or
fictional change to the fixed prefix is assumed.

## 3. Deterministic counting bounds

Let `I_N` count unordered distinct incomparable pairs in `P_N` and set

\[
 f_N=1-d_N=\frac{I_N}{\binom N2},\qquad N\geq2.
 \tag{10}
\]

Each birth appends a maximal vertex at an ideal without changing any old
relation. Old incomparabilities persist, width is nondecreasing, and a birth
at `S` creates exactly `n-|S|` new incomparable pairs.

A preferred birth in `C op Ant_k` is incomparable only to the `k`
current tops, an antichain of size at most `W_n<=W_N`. A full birth
creates no incomparable pair. Every other proper birth creates at most
`n<=N` such pairs. Summing through the block therefore gives, for any
cutoff including the finite prefix,

\[
 I_N\leq I_m+(N-m)W_N+N B_N\leq I_m+N W_N+N B_N.
 \tag{11}
\]

The first term retains every initial incomparable pair. It is not set to
zero by conditioning on a history. Every full birth raises height by one,
and no birth lowers height, so

\[
 F_N\leq H_N-H_m,\qquad
 B_N=F_N+Z_N\leq H_N-H_m+Z_N^+.
 \tag{12}
\]

Combining (10)–(12), with the exact finite-size normalization, gives

\[
 0\leq f_N\leq\frac{2I_m}{N(N-1)}
   +\frac{2}{N-1}\left(W_N+H_N-H_m+Z_N^+\right),\qquad N\geq2.
 \tag{13}
\]

No replacement of `binom(N,2)` by `N^2/2` has been made. Similarly,
the always-valid width count is `W_N(W_N-1)<=2I_N`, not `W_N^2<=2I_N`;
this theorem uses (11), not a converse inference from small width alone.

## 4. A finite conditional expectation inequality

For `m>=5`, summing the nonpositive conditional drifts in (5) gives
`E[B_N|F_m]<=E[F_N|F_m]`. For an arbitrary earlier cutoff, its at-most-`r`
initial contribution gives

\[
 \mathbb E[B_N\mid\mathcal F_m]
 \leq\mathbb E[F_N\mid\mathcal F_m]+r
 \leq\mathbb E[H_N\mid\mathcal F_m]-H_m+r,
 \qquad r=(5-m)_+.
 \tag{14}
\]

For `N<=ell`, the same inequality follows from the finite deterministic
bound; for `N>ell`, use the tower rule for the free part. Taking expectations
in (11), for `N>m` and `N>=2`, proves

\[
 \mathbb E[f_N\mid\mathcal F_m]
 \leq\frac{2I_m}{N(N-1)}
 +\frac{2}{N-1}
   \left(\mathbb E[W_N+H_N\mid\mathcal F_m]-H_m+r\right).
 \tag{15}
\]

Every expectation is under the **same** conditioned finite history. There
is no square-root fluctuation remainder here: (15) uses the signed drift
bound on expected counts directly. It does not discard `Z_N^+` from the
pathwise inequality (13), nor claim the pathwise domination `B_N<=F_N`.

## 5. The two convergence implications

Work under a fixed admitted finite-history conditional law, or under the
unconditional law by a finite mixture of histories at size five.

**Probability antecedents.** Suppose `H_N/N->0` and `W_N/N->0` in
probability. Both variables lie in `[0,1]`, so their expectations tend to
zero: for any such variable `Y_N`,
`E Y_N<=epsilon+Pr(Y_N>epsilon)`. Equation (15) then gives `E f_N->0`.
Thus `d_N->1` in `L^1` and in probability by Markov's inequality. The
same boundedness gives all finite positive moments of `|1-d_N|` tending
to zero. An almost-sure density limit is not inferred from these weaker
antecedents alone.

**Almost-sure antecedents.** Suppose instead both normalized height and
width tend to zero almost surely. Equation (8) controls the remaining
positive signed-count term, including the finite-prefix correction.
Equation (13) therefore proves `f_N->0`, hence `d_N->1`, almost surely.
Boundedness also supplies the probability and moment conclusions. No
independence, summability of `eta_n`, or uniform positive full-birth hazard
is needed for this implication.

These conclusions apply conditionally after any admitted finite history;
their unconditional forms follow as stated. The deterministic diagnostics
are intrinsic to each finite order, while all limiting statements refer
to this chosen birth-prefix exhaustion. No `L^infinity` convergence or
uniform-over-rows asymptotic is asserted.

## 6. Minimal premises and the exact obstruction

The counting theorem uses less structure than the law's admissibility
proof. Its sufficient counting premises are:

- One new vertex per step, with old comparabilities and incomparabilities
  preserved, so width cannot decrease.
- A three-way birth partition: preferred births add at most current width
  many incomparable pairs; full births add none; remaining births add at
  most the current vertex count.
- Height never decreases, and each full birth raises it by at least one.
- Conditional on the whole history, the probability of the remaining
  birth class is at most that of the full class, apart from an allowed
  finite initial segment.

For these premises, the supermartingale count and deterministic inequalities
already prove the obstruction. Strict positivity, the exact `eta` formula,
fair bits, passive kernels, record locality and diamonds are not extra
steps in the counting proof; they remain load-bearing requirements for
the particular admitted family constructed in section 1.

To evade this theorem while retaining all three target properties, at
least one counting premise must fail: for example its pair-production
bound or its conditional probability domination could no longer hold.
Alternatively a target property must be abandoned. Such a change is
necessary, not sufficient, and is not a proposed replacement law or
permission to alter committed records. Merely changing the schedule within
section 1 leaves all counting premises intact.

The abstract counting proof permits arbitrary history dependence **when
its conditional premises hold**. That observation does not prove locality,
equivariance or diamonds for an arbitrarily adaptive normalization rule.
Only fixed deterministic schedules have been admitted here. No adaptive
construction, endpoint tuning, optimizer or alternative candidate is opened.

The harmonic [RI-48 result](../native_growth_clone_regime_v1/REGIME.md)
fails the relative-width antecedent, so is not contradicted. The power
[RI-49 family](../native_growth_clone_power_family_v1/FAMILY.md) meets both
sublinear antecedents and exhibits the forced density-one conclusion.
This note does not classify which arbitrary schedules meet the antecedents,
exclude density one itself, or determine any sharp growth rate.

An interior density requirement must come from a separately stated target;
it is not asserted necessary for all continuum geometry, all DET-native
growth or gravity. No dimension, metric, physical clock, source or mass
law follows. The conditional seed and scalar passivity remain unpromoted;
Option B and metric-as-record Status M are unchanged.

## 7. Evidence and bounded handoff

All new results are analytic. No simulator, table, executor, optimization,
numerical certificate or external fit was created or run. Accepted checks
are premises, not replayed suites.

Three read-only internal reviewers read the complete note and independently
passed its mathematics and scope with no blockers or requested corrections.
Their checks covered arbitrary fixed-sequence admissibility, the exact
conditional moment-generating function and one-sided tail, positive excess
rather than absolute count imbalance, the pre-size-five offset and positive
tail denominators, pair/height counts and exact finite-size normalization,
the signed-expectation bound without a fluctuation remainder, both separate
convergence implications and the minimal-premise/adaptive-rule boundary.
No reviewer edited source or ran a research executor. These are internal
analytic reviews, not machine-checked proofs, empirical validation or
independent coordinator acceptance.

All five local Markdown targets exist. Scoped trailing-whitespace and
conflict-marker scans are clean. Read-only SHA-256 checks of the five
referenced accepted sources match their accepted identities, including the
unchanged RI-46/48/49 notes. Their pins and the final new-source identity
accompany the handoff. Coordinator adjudication is separate and recorded
in the opening status.

Only this new note is authored. Accepted research, coordinator records,
measurement sources and RET remain unchanged; RET stays paused. The
coordinator owns all git/index/publication. Stop this bounded packet at
source-stable handoff for independent adjudication.
