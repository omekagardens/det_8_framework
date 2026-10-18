# RI-49 — a power-schedule family: sublinear width, density one

24 September 2026 UTC. **Conditional analytic family tradeoff; independent
coordinator adjudication accepted.** This note defines an explicitly new
family, one law for each fixed real `0<a<1`, with

\[
 \eta_n=(n+1)^{-a}\quad(n\geq5).
 \tag{1}
\]

It retains RI-46's private preferred-component construction, remaining
component scaling and complete RI-41 prefix, but **not** RI-46's harmonic
schedule. Neither [RI-46](../native_growth_clone_selection_v1/SELECTION.md)
nor its [RI-48 analysis](../native_growth_clone_regime_v1/REGIME.md) is changed.

For each fixed `a` in this open interval, the new law is admissible and

\[
 \mathbb E H_N=\Theta(N^{1-a}),\qquad
 H_N/N\longrightarrow0,\quad H_N\longrightarrow\infty
 \quad\text{almost surely}.
 \tag{2}
\]

But its unordered comparable-pair density `d_N` and relative width satisfy

\[
 d_N\longrightarrow1,\qquad W_N/N\longrightarrow0
 \quad\text{almost surely, in probability and in }L^1.
 \tag{3}
\]

Thus this family removes the harmonic law's macroscopic-width obstruction
while driving almost all pairs to comparability. It fails a stipulated
target of a deterministic density strictly between zero and one. No value
of `a` is selected as a dimension, fit or physical parameter; density one
does not mean that these finite orders are chains or that gravity has been
derived or universally excluded.

## 1. Fixed premises and a new recursive law for each parameter

Keep the entire [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through parent size four, not just its height bound. Free selections begin
at parent size five. Retain the [RI-38 domain](../native_joint_growth_extension_criterion_v1/CRITERION.md):
all finite orders and independent binary record assignments, strictly
positive probabilities for every ideal, precursor-record locality, permitted
whole-unmarked-parent access, marked-parent equivariance, fixed context,
one committed birth per step and fair newborn records. Full scalar-passive
maps retain the complete unnormalized complex PSD residual,

\[
 \mathcal B^{P,r}_{S,b}(D)=q_{P,r}(S)D/2.
 \tag{4}
\]

There is no silent/halt branch, new record permission, nonpassive quantum
coupling or change to the accepted prefix. For each chosen `a`, recompute
the local maximal-deletion potential at every new size from the **actual
previously selected law for that same parameter**:

\[
 u_{P,r}(S)=\prod_{\varnothing\ne B\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus B,\,r|_{P\setminus B}}(S)^{(-1)^{|B|+1}},
 \qquad S\subsetneq P.
 \tag{5}
\]

Potentials and table maxima below depend on `a`, though that superscript
is suppressed. In particular later harmonic-law potentials are not reused.

A suitable parent is `C op Ant_k`, `k>=1`, with preferred ideal `C`.
RI-46's structural proof does not depend on its schedule: the preferred
child is `C op Ant_(k+1)`, all last-birth roles return to the same local
marked-core node, and every incident ratio is a unit loop. The component
is private to that parent/core-record isomorphism class. Core records are
retained modulo actual core automorphisms; equal numerical values do not
merge classes. Each suitable row has exactly one labeled preferred ideal,
and unsuitable rows have none.

Let `K_n` collect all these preferred components and define

\[
 V_n=\max_{|P|=n,\,r}
 \sum_{\substack{S\subsetneq P\text{ ideal}\\c(P,S,r|S)\notin K_n}}
        u_{P,r}(S),\qquad
 \lambda_n=\frac{\eta_n}{2(1+V_n)},
\]
\[
 \alpha_c=\begin{cases}(1-\eta_n)/u_c,&c\in K_n,\\
                         \lambda_n,&c\notin K_n,
          \end{cases}
 \qquad
 q_{P,r}(S)=\alpha_{c(P,S,r|S)}u_{P,r}(S)\quad(S\subsetneq P),
\]
\[
 q_{P,r}(P)=1-\sum_{S\subsetneq P\text{ ideal}}q_{P,r}(S).
 \tag{6}
\]

The maximum is over the complete marked table and excludes **all** preferred
components. Sums retain every labeled ideal. Finite positive inherited
potentials give a finite `V_n>=0`; `0<eta_n<1` and `lambda_n>0`.
All scales are fixed law-table constants, not actual-record-dependent
normalizers. Proper evaluations use only their permitted local keys; a
full precursor may read the entire parent records.

Write `beta_n(P,r)` for the total probability of the nonpreferred **proper**
ideals. Then

\[
 0\leq\beta_n(P,r)\leq\lambda_nV_n<\eta_n/2.
 \tag{7}
\]

A suitable row has preferred mass `1-eta_n` and full complement
`eta_n-beta_n>eta_n/2`. An unsuitable row has full complement
`1-beta_n>1-eta_n/2>eta_n/2`. Every ideal/bit branch is strictly positive,
and the row sums are one.

Component-constant scaling preserves all RI-38 ratios. New diamond second
precursors are proper, so the full complements introduce no conflicting
new equation. Locality and equivariance hold for (5)–(6), and equality of
scalar multipliers is equality of the entire maps (4) for every admitted
`D`. These are exactly the premises for the next extension. Induction
therefore proves all-size admissibility for each fixed `a`, without a
finite-layer search, rationality assumption or efficient-evaluation claim.

## 2. Height: an admissible sublinear, diverging family

Use the associated marked-history measure and whole-history filtration
`F_n`. Let `U_n` indicate an unsuitable parent, and let
`t_n=E[H_(n+1)-H_n|F_n]`. Full births restore suitability and raise height
one; preferred births preserve suitability and height. Equation (7) gives

\[
 \Pr(U_{n+1}=1\mid\mathcal F_n)<\eta_n/2,\qquad
 \Pr(\text{full birth at size }n\mid\mathcal F_n)>\eta_n/2,
 \qquad t_n\leq\eta_n+U_n.
 \tag{8}
\]

These are whole-history bounds, with both fair newborn marks summed.
Fix a finite admitted history `h_m`, `m>=5`, and restart all following
sums there. For `n>=m+1`, `E[U_n|F_m]<=n^(-a)/2`. For `N>m`, therefore,

\[
 H_m+\tfrac12\sum_{k=m+1}^{N}k^{-a}
 <\mathbb E[H_N\mid\mathcal F_m]
 \leq H_m+U_m+\sum_{k=m+1}^{N}k^{-a}
                  +\tfrac12\sum_{n=m+1}^{N-1}n^{-a}
 \leq H_m+U_m+\tfrac32\sum_{k=m+1}^{N}k^{-a}.
 \tag{9}
\]

Integral comparison places the sum between
`((N+1)^(1-a)-(m+1)^(1-a))/(1-a)` and
`(N^(1-a)-m^(1-a))/(1-a)`. This proves conditional and unconditional
`Theta(N^(1-a))` expected height for fixed `a,m`.

At dyadic sizes, Markov's inequality gives
`Pr(H_(2^j)/2^j>epsilon|h_m)=O_(a,m,epsilon)(2^(-aj))`, summable because
`a>0`. The first Borel--Cantelli argument and height monotonicity between
dyadic endpoints prove `H_N/N->0` almost surely. Boundedness in `[0,1]`
gives all finite positive normalized moments as well.

For every deterministic `l>=5`, conditional iteration gives

\[
 \Pr(\text{no full birth at sizes }l,\ldots,N-1\mid\mathcal F_l)
 \leq\prod_{n=l}^{N-1}(1-\eta_n/2)
 \leq\exp\left(-\tfrac12\sum_{n=l}^{N-1}(n+1)^{-a}\right)
 \longrightarrow0.
 \tag{10}
\]

The sum diverges for the assigned interval. Continuity from above and the
countable union over `l` prove infinitely many full births almost surely,
hence `H_N->infinity`. No independence, expected-count shortcut, or
almost-sure asymptotic power-rate equivalence for height is asserted.

## 3. Reset age and the current maximal set

Let `T_n=|Max(P_n)|`. A full birth resets this number to one; any other
birth can increase it by at most one. Fix the same cutoff `m>=5`.
Define `A_n`, for `n>=m`, to count births **since** the latest full birth
among parent sizes `m,...,n-1`, excluding that full birth itself. If none
has occurred in that interval, set `A_n=n-m`. In particular `A_m=0`.
Let `Z_(m,n)` be the event of no full birth in that interval, with
`Z_(m,m)` certain. Then pathwise

\[
 T_n\leq1+A_n+(T_m-1)\mathbf1_{Z_{m,n}}.
 \tag{11}
\]

After an actual reset the bound is `1+A_n`; without one it is `T_m+A_n`.
This retains the initial maximal set. It does not invent a physical reset
at `m` or incorrectly assume `T_m<=A_m+1`.

For integers `1<=k<=n-m`, the event `A_n>=k` is exactly the absence of a
full birth at parent sizes `n-k,...,n-1`. Since `eta_j>=n^(-a)` there,
successive conditional failure bounds from (8), followed by conditioning
back to `F_m`, give, with `h_n=n^(-a)/2`,

\[
 \Pr(A_n\geq k\mid\mathcal F_m)
 \leq\prod_{j=n-k}^{n-1}(1-\eta_j/2)
 \leq(1-h_n)^k,
 \qquad
 \Pr(Z_{m,n}\mid\mathcal F_m)\leq(1-h_n)^{n-m}.
 \tag{12}
\]

For `k>n-m` the age tail is zero. Summing the geometric upper bounds,

\[
 \mathbb E[A_n\mid\mathcal F_m]
 \leq\sum_{k=1}^{\infty}(1-h_n)^k
 =2n^a-1,
\]
\[
 \mathbb E[T_n\mid\mathcal F_m]
 \leq2n^a+(T_m-1)(1-h_n)^{n-m}
 \leq2n^a+T_m-1.
 \tag{13}
\]

At `n=m`, the actual age is zero and (11) is exact; the displayed
expectation bounds remain valid upper bounds. The fallback factor is also
at most `exp(-(n-m)/(2n^a))`. For fixed cutoff this proves expected age
and current maximal count `O(n^a)`. The proof uses uniform conditional
hazards, not independent waiting times or a stationary age distribution.

## 4. Incomparable-pair production and its expected total

Let `I_N` count unordered distinct incomparable pairs in `P_N`. Existing
relations and incomparabilities are unchanged by a maximal birth, so this
cumulative count is nondecreasing. A newborn at an ideal `S` is comparable
to exactly its `|S|` predecessors among the `n` old vertices. Consequently

\[
 I_{n+1}-I_n=n-|S|.
 \tag{14}
\]

For a preferred birth in a suitable `C op Ant_k`, the only incomparable
old vertices are its `k=T_n` tops. The full birth contributes zero.
Nonpreferred proper births contribute at most `n`, and their combined
conditional probability is below `eta_n/2`. If the parent is unsuitable
there is no preferred branch; it is not silently treated as having one.
For every history,

\[
 \mathbb E[I_{n+1}-I_n\mid\mathcal F_n]
 \leq (1-U_n)(1-\eta_n)T_n+n\,\beta_n(P_n,r_n)
 \leq T_n+\tfrac12n(n+1)^{-a}.
 \tag{15}
\]

Here `r_n` denotes the current records. Full births are excluded from the
proper mass in (7), even though they are nonpreferred:
their sometimes large probability creates no incomparable pair.

Apply (13), sum from the actual cutoff, and use
`n(n+1)^(-a)<=n^(1-a)`. For `N>=m`,

\[
 \mathbb E[I_N\mid\mathcal F_m]
 \leq I_m+(T_m-1)(N-m)
              +2\sum_{n=m}^{N-1}n^a
              +\tfrac12\sum_{n=m}^{N-1}n^{1-a}
\]
\[
 \leq I_m+(T_m-1)(N-m)
       +\frac{2}{1+a}(N^{1+a}-m^{1+a})
       +\frac{1}{2(2-a)}(N^{2-a}-m^{2-a}).
 \tag{16}
\]

Both summands are increasing functions of `n`, so the final upper integral
bounds are in the displayed direction. All finite-start terms are retained;
`I_m` is not set to zero. For fixed `a,m`, (16) is
`O(N^(1+a)+N^(2-a))`. This is an upper bound, not an asserted sharp
asymptotic or a claim that the two contributions are independent.

## 5. Density limits: expectation, probability and almost surely

Define the incomparable and comparable fractions, for `N>=2`, by

\[
 f_N=\frac{I_N}{\binom N2},\qquad d_N=1-f_N.
 \tag{17}
\]

All unordered distinct pairs are either comparable or incomparable; neither
Hasse-edge counts nor reflexive pairs are used. Equation (16) implies

\[
 \mathbb E[f_N\mid h_m]
 =O_{a,m}\bigl(N^{-(1-a)}+N^{-a}+N^{-1}\bigr)\longrightarrow0.
 \tag{18}
\]

The finite-start constant can also depend on the fixed history, or be
bounded uniformly using `T_m<=m` and `I_m<=binom(m,2)`.
Since `f_N>=0`, (18) gives `L^1` convergence to zero and convergence in
probability by Markov's inequality. It does not alone prove almost-sure
convergence. For that, at sizes `N=2^j`, (16) gives

\[
 \Pr\{I_{2^j}/2^{2j}>\epsilon\mid h_m\}
 =O_{a,m,\epsilon}\bigl(2^{-j(1-a)}+2^{-ja}+2^{-j}\bigr).
 \tag{19}
\]

For fixed `0<a<1` this series is summable. Borel--Cantelli at positive
rational thresholds proves `I_(2^j)/2^(2j)->0` almost surely. If
`2^j<=N<2^(j+1)`, monotonicity of the **cumulative count**, not of its
density, gives

\[
 \frac{I_N}{N^2}\leq
 4\frac{I_{2^{j+1}}}{2^{2(j+1)}}\longrightarrow0.
 \tag{20}
\]

As `f_N=2(I_N/N^2)/(1-1/N)`, this proves `f_N->0` and `d_N->1` almost
surely. Because `0<=f_N<=1`, every finite positive moment of `|1-d_N|`
also tends to zero. Taking `m=5` and the finite mixture over its admitted
histories gives all unconditional claims. Conditioning on a later history
requires restarting the age and sums at that cutoff as above; none of the
limits changes.

## 6. Width, and what density one does not mean

An antichain of maximum size `W_N` contributes `binom(W_N,2)` incomparable
pairs. Keeping the finite-size correction,

\[
 W_N(W_N-1)\leq2I_N,
 \qquad
 (W_N/N)^2\leq\frac{2I_N}{N^2}+\frac1N
                =(1-1/N)f_N+\frac1N.
 \tag{21}
\]

Therefore relative width tends to zero almost surely. The same inequality
controls its second moment by `(1-1/N)E f_N+1/N`; or bounded convergence
gives every finite positive moment directly. In particular `W_N/N->0`
in probability and `L^1` as claimed.

Width itself still diverges almost surely: rank by longest chain ending
at each vertex partitions a finite order into `H_N` antichains, giving
`N<=H_N W_N`, and section 2 proves `H_N/N->0`. Thus vanishing relative
width and density one do not assert bounded width or a literal chain.
Nor do they determine an almost-sure power exponent or a manifold dimension.

The proved tradeoff is specific: every fixed member of the assigned open
parameter interval has vanishing relative width but comparable density one.
It cannot meet an additional requirement `d_N->rho` for a deterministic
`0<rho<1`, whether in probability, almost surely or `L^1`. It is not a
statement that every geometric target must have such a limit. The finite
diagnostics are intrinsic, but all limit claims use this birth-prefix
exhaustion and these explicitly chosen laws.
They are history-law limits, not uniform-over-rows or `L^infinity` results.

No limit uniform in `a`, exchange of `a` and `N` limits, or endpoint case
`a=0`, `a=1` or `a>1` is proved here. Constants and convergence rates
may deteriorate near the endpoints. No physical dimension fit, metric,
source, matter/mass response, clock or gravity follows. The conditional
seed, scalar passivity and choice of schedule remain extra mathematical
structure, not DET entailment. Option B and metric-as-record Status M
are unchanged. No alternate law or successor is started.

## 7. Evidence and bounded handoff

All new results are analytic. No executor, table, simulation, numerical
certificate, optimizer or external fit was created or run. Earlier
accepted checks are premises, not replayed suites.

Three read-only internal reviewers read the complete note and independently
passed its mathematics and scope with no blockers. They checked the
parameter-dependent recurrence, strictness/locality/diamonds, conditional
height cutoffs, full-birth product, reset-age indexing and initial-maxima
fallback, the sharper geometric sum `2n^a-1`, exact pair-production
partition, finite-start terms and integral directions in (16), dyadic
interpolation of the cumulative count, binomial width correction, limit
modes and endpoint caveats. A missing LaTeX backslash in (6) was corrected;
no mathematical revision was required. No reviewer edited source or ran a
research executor. These reviews are not machine-checked proofs, empirical
validation or independent coordinator acceptance.

All four local Markdown targets exist. Scoped trailing-whitespace and
conflict-marker scans are clean. Read-only SHA-256 checks pin the four
referenced accepted sources; their identities and the new note's final
identity accompany the handoff. Accepted source files were not modified.
Coordinator adjudication is separate and recorded in the opening status.

Only this new note is authored. Accepted sources, coordinator records,
measurement work and RET remain unchanged; RET remains paused. The
coordinator owns git/index/publication. Stop this bounded packet at
source-stable handoff for independent adjudication.
