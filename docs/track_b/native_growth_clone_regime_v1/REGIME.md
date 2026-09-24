# RI-48 — macroscopic common-past layers and sparse-density subsequences

24 September 2026 UTC. **Conditional analytic regime screen; independent
coordinator adjudication accepted.** Keep the exact accepted
[RI-46 law](../native_growth_clone_selection_v1/SELECTION.md), including its
RI-41 prefix and `eta_n=1/(n+1)`. This law's sublinear, diverging height
does not imply vanishing relative width or a positive limiting order density.
In fact, writing `W_N=width(P_N)` and `d_N` for the fraction of unordered
distinct pairs that are comparable,

\[
 \liminf_{N\to\infty}\Pr(W_N/N\geq\theta)\geq1-\theta
 \quad(0<\theta<1),\qquad
 \limsup_{N\to\infty}W_N/N=1\quad\text{almost surely},
 \tag{1}
\]
\[
 \liminf_{N\to\infty}d_N=0\quad\text{almost surely},
 \qquad d_N\text{ does not converge in probability to any constant }\rho>0.
 \tag{2}
\]

The wide antichains here can be the entire top layer with one common strict
past, not just scattered incomparable subsets. These statements reject this
particular law for targets requiring vanishing relative width or a positive
deterministic limiting comparable-pair density. They are not a universal
continuum or gravity no-go theorem, nor a replacement growth law.

## 1. Fixed law, histories and the finite diagnostics

No parameter, seed, record law, eligibility condition or component scale
is changed. Retain the complete RI-41 prefix through parent size four and
RI-46's fixed recursive table at every parent size `n>=5`. In particular,
RI-38's strictly positive scalar-passive maps, record locality, whole
unmarked-parent access, marked-parent equivariance and diamonds remain
inherited premises. Newborn bits are fair and the complete unnormalized
kernel is transported by `B_(S,b)(D)=q(S)D/2`; there is no informative
quantum feedback added by these calculations.

Use RI-46's classical marked-history measure and whole-history filtration
`F_n`. Every finite admitted history has positive cylinder probability.
For the finite committed order `P_N`, let

\[
 W_N=\max\{|A|:A\subseteq P_N\text{ is an antichain}\},
 \qquad
 M_N=\#\{\{x,y\}\subseteq P_N:x\ne y,\ x\prec y\text{ or }y\prec x\},
\]
\[
 d_N=\frac{M_N}{\binom N2},\qquad N\geq2.
 \tag{3}
\]

Each unordered distinct comparable pair is counted once. This is neither
the number of Hasse edges nor a count of reflexive or ordered pairs.
`W_N` and `d_N` are intrinsic finite-order quantities. Their asymptotics
below use this specified birth-prefix exhaustion; invariance under arbitrary
infinite natural re-enumeration is not inferred.

Recall that a suitable parent is `C op Ant_k`, `k>=1`: every top vertex
has exactly the core `C` as its strict past. Its unique preferred precursor
is `C`, of probability `n/(n+1)` at size `n`. Preferred birth preserves
suitability and height. For an unsuitable parent the full-birth probability
obeys

\[
 q_{P_n,r_n}(P_n)>1-\frac1{2(n+1)}.
 \tag{4}
\]

A full birth from any parent yields a suitable child with a unique top.
These are the precise admitted facts used to construct the block event.

## 2. Exact preferred runs, with one-step recovery

Fix integers `m>=5` and `N>=m+1`. Define `E_(m,N)` using the state at
the block's start, not a condition on a favorable future history:

- If `P_m` is suitable, take preferred births at parent sizes
  `m,m+1,...,N-1`.
- If `P_m` is unsuitable, take a full birth at parent size `m`, then
  preferred births at sizes `m+1,...,N-1`.

Both rules sum all newborn bit assignments. The event is determined by
the complete history through `N`, so is `F_N`-measurable.

### Suitable starting state

Write `P_m=C op Ant_k`, with `|C|+k=m`. Every preferred birth preserves
this core and has conditional probability `n/(n+1)`, whatever the marks
in the realized history. Iterated conditional probabilities telescope:

\[
 \Pr(E_{m,N}\mid\mathcal F_m)
 =\prod_{n=m}^{N-1}\frac n{n+1}=\frac mN.
 \tag{5}
\]

The terminal order is exactly `C op Ant_(k+N-m)`, retaining all old
relations and records and adding `N-m` tops. These tops are incomparable
and share the same strict past `C`; their record bits need not agree.

### Unsuitable starting state

The first full birth makes `P_m op Ant_1`. Subsequent preferred births
have core `P_m`. Thus the terminal order is exactly
`P_m op Ant_(N-m)` and

\[
 \Pr(E_{m,N}\mid\mathcal F_m)
 =q_{P_m,r_m}(P_m)\prod_{n=m+1}^{N-1}\frac n{n+1}
 =q_{P_m,r_m}(P_m)\frac{m+1}{N}
 >\frac{m+1/2}{N}>\frac mN.
 \tag{6}
\]

For `N=m+1` the second product is empty and equals one, so the same
formula gives the exact one-step recovery probability. Requiring a full
birth from an already suitable parent would be a different event and would
not supply (5). The successful first step is chosen by suitability as above.

The factors in (5)–(6) are ideal probabilities, not one-bit branch weights.
Prescribing any one newborn bit word of length `N-m` instead multiplies
the displayed probability by `2^(-(N-m))`; summing those words restores
the formulas. No independence of growth steps is used. Future preferred
probabilities are exactly size-dependent on every successful marked path,
which is enough for the conditional product.

Consequently, for **every** starting marked history,

\[
 \Pr(E_{m,N}\mid\mathcal F_m)\geq m/N,
 \qquad E_{m,N}\ \Longrightarrow\ W_N\geq N-m.
 \tag{7}
\]

More precisely, on this event the terminal order is `B op Ant_(N-c)`
with a fixed core `B` of size `c<=m`, and the entire common-past top
antichain has at least `N-m` vertices. In the suitable case `B=C,c=m-k`;
in the recovery case `B=P_m,c=m`. Its exact width and comparable count are

\[
 W_N=\max\{width(B),N-c\},\qquad
 M_N=M(B)+c(N-c),
 \tag{8}
\]

where `M(B)` counts unordered comparable pairs inside the core. Height is
unchanged in the suitable case and rises exactly one in the recovery case.
The core may contain all earlier irregularities; this does not assert that
the whole history was always a sequence of pure antichain layers.

### Run length is not an infinite-lived layer

For a suitable start let `L` be the number of consecutive preferred births
before the first nonpreferred birth. For integers `ell>=0`, (5) gives

\[
 \Pr(L\geq\ell\mid\mathcal F_m)=\frac m{m+\ell},\qquad
 \Pr(L=\ell\mid\mathcal F_m)
       =\frac m{(m+\ell)(m+\ell+1)}.
 \tag{9}
\]

Thus `L` is finite almost surely but has infinite conditional expectation:
its tail sum diverges. A nonpreferred birth can still be full and suitable;
ending a preferred run is not the same as leaving the suitable class.

## 3. Fixed-size macroscopic-width tails

Fix `0<theta<1` and set, with exact integer rounding,

\[
 m_N=\lfloor(1-\theta)N\rfloor=N-\lceil\theta N\rceil.
 \tag{10}
\]

For all sufficiently large `N`, `5<=m_N<N`. The block event from `m_N`
has `W_N>=N-m_N=ceil(theta N)`. Applying (7) and the tower rule gives

\[
 \Pr(W_N/N\geq\theta)\geq\frac{\lfloor(1-\theta)N\rfloor}{N}
 \geq1-\theta-\frac1N.
 \tag{11}
\]

Taking the limit inferior proves the first part of (1). The same lower
bound holds conditional on **any fixed earlier finite history** `h_l`,
once `m_N>=max(5,l)`: take conditional expectation of (7) given `F_l`.
No replacement of the actual history distribution by a uniform row average
is involved. The event in fact supplies a suitable terminal with a
common-past top antichain at least this large, not just a width witness.

## 4. Almost-sure nearly exhaustive top layers

Fix an integer ratio `R>=2` and an integer starting cutoff `m_0>=5`.
Use geometric endpoints and disjoint birth blocks

\[
 m_j=m_0R^j,\qquad E_j=E_{m_j,m_{j+1}},\qquad j\geq0.
 \tag{12}
\]

The block starting at size `m_j` includes births at parent sizes
`m_j,...,m_(j+1)-1`, so it shares no birth with the next block.
Equations (7) and (12) give

\[
 \Pr(E_j\mid\mathcal F_{m_j})\geq1/R,
 \qquad
 E_j\Longrightarrow W_{m_{j+1}}/m_{j+1}\geq1-1/R.
 \tag{13}
\]

The events need not be independent. For integers `K>=0,L>=1`, successive
conditioning is legitimate because every preceding block failure is known
at the next block start. Therefore

\[
 \Pr\left(\bigcap_{j=K}^{K+L-1}E_j^c\ \middle|\ \mathcal F_{m_K}\right)
 \leq(1-1/R)^L\longrightarrow0.
 \tag{14}
\]

For each `K`, continuity from above rules out no further successes after
block `K`. A countable union over `K` shows infinitely many successful
blocks almost surely. Intersect these probability-one conclusions over
the countable integers `R>=2`. On that intersection,

\[
 \limsup_N W_N/N\geq1-1/R\quad\text{for every }R\geq2.
 \tag{15}
\]

Since width is at most `N`, its limit superior is one. More strongly,
one can choose increasing successful endpoints with `R` tending to infinity;
the common-past top antichain itself occupies a fraction tending to one
along that subsequence. Independence between the different geometric grids
is neither asserted nor needed for their countable intersection.

After conditioning on a finite `h_l`, start with `m_0>=max(5,l)` and use
the same conditional product; all these almost-sure conclusions remain
valid. This argument proves a limit superior, not convergence of relative
width or persistence forever of any one top layer.

### Current maxima are not historical width

Let `T_N=|Max(P_N)|`. The successful blocks above have their entire top
antichain maximal, so they also give `limsup T_N/N=1` almost surely.
RI-46 separately proves infinitely many full births almost surely. At each
such birth from size `n`, the child has exactly one maximal vertex, so
`T_(n+1)/(n+1)=1/(n+1)`. These sizes tend to infinity. Consequently

\[
 \liminf_N T_N/N=0,\qquad \limsup_N T_N/N=1
 \quad\text{almost surely}.
\]

This reset of the current maximal set does **not** reset width: old
incomparable pairs are unchanged. At a full birth from a nonempty parent,
`W_(n+1)=W_n`, and width is nondecreasing under all births. No conclusion
that `liminf W_N/N=0` is drawn from the maximal-set reset.

## 5. Comparable-pair density: two distinct limit statements

Any antichain of size `w` supplies `binom(w,2)` incomparable pairs. Thus,
for every finite order with `N>=2`,

\[
 0\leq d_N\leq1-\frac{W_N(W_N-1)}{N(N-1)}.
 \tag{16}
\]

In particular, on `E_(m,N)` this upper bound can use `N-m` in place of
`W_N`. Equation (8) also computes the exact comparable count on that event;
no supplied geometry enters either calculation.

### Almost-sure sparse subsequences

By section 4, almost every history has increasing sizes on which
`W_N/N->1`. On those sizes (16) forces `d_N->0`. Since `d_N>=0`,
`liminf d_N=0` almost surely, including after every fixed finite-history
conditioning. This proves the first part of (2), not full convergence.

### No positive deterministic limit in probability

An almost-sure limit inferior by itself would not exclude a positive
limit in probability. Use the fixed-size bound separately. Fix `0<b<1`
and choose `theta` with `sqrt(1-b)<theta<1`. On `W_N/N>=theta`,

\[
 d_N\leq1-
 \frac{\lceil\theta N\rceil(\lceil\theta N\rceil-1)}{N(N-1)}
 \longrightarrow1-\theta^2<b
 \quad\text{as an upper-bound sequence}.
 \tag{17}
\]

Thus for sufficiently large `N` that event is contained in `{d_N<=b}`.
By (11), `liminf Pr(d_N<=b)>=1-theta`. Taking the supremum of these
bounds over `theta>sqrt(1-b)` yields the quantitative statement

\[
 \liminf_N\Pr(d_N\leq b)\geq1-\sqrt{1-b}>0,
 \qquad 0<b<1.
 \tag{18}
\]

The same proof gives (18) conditional on a fixed admitted finite history.
If `d_N` converged in probability to a constant `rho in (0,1]`, choosing
`b=rho/2` would instead force this probability to zero, a contradiction.
Constants above one are already excluded by `0<=d_N<=1`. This proves
the second part of (2). It does **not** prove convergence in probability
to zero, vanishing expected density, a density distributional limit or
any positive lower bound for the density limit superior.

## 6. Adjudication of this regime, not of every geometry

The exact RI-46 law fails either of the following additional target
requirements, if that requirement is stipulated:

- Vanishing relative width `W_N/N->0` in probability. Equation (11)
  prevents this, so convergence to zero almost surely or in mean is also
  excluded. Equation (15) gives the stronger almost-sure limit superior one.
- A positive deterministic limiting comparable-pair density in probability
  (and therefore also a requirement of such an almost-sure or mean limit).
  Equation (18), not merely the almost-sure sparse subsequence, excludes it.

Here convergence in mean means `L^1` convergence, not just convergence of
the numerical expectations. A positive limit of `E d_N` alone has **not**
been excluded. Neither has a zero limiting density been established.

RI-46's logarithmic expected height, sublinear diverging height and
diverging width remain true. The present results show why those screens
alone cannot certify the additional regime requirements above. Common-past
layers with macroscopic, sometimes nearly exhaustive, antichains are a
proved feature of this law, while detailed morphology inside their retained
cores is not classified here.

No theorem is asserted that every continuum approximation must have either
of those additional limits. Relating a particular sampling/exhaustion and
target geometry to such criteria requires separate stated premises. No
Lorentzian metric, dimension, source, matter, mass, clock or gravity claim
is produced or universally rejected. The conditional seed and passive
payload premises remain unpromoted; Option B and metric-as-record Status M
are unchanged. The calculation neither tunes `eta` nor opens a replacement
model, larger finite search or automatic successor.

## 7. Evidence and source-stable handoff

The new results are direct analytic consequences of the fixed accepted
law. No simulation, new table, executor, certificate, external numerical
input or optimizer was created or run. The earlier source checks are
inherited premises, not suites replayed for this note.

Three read-only internal reviewers read the complete note and independently
passed the proofs and scope with no mathematical blockers. Their checks
included the two exact run probabilities and fair-bit words, terminal
ordinal-sum counts, finite-lifetime/infinite-mean run tails, integer rounding,
finite-history restart, conditional geometric-block failure products,
the countable intersection and subsequence, current maxima versus historical
width, and both distinct density-limit arguments. They also checked the
strict slack needed in (17) and the distinction between `L^1` convergence
and convergence of numerical expectations. No reviewer edited source or
executed a research check. These reviews are not machine-checked proofs,
empirical evidence or independent coordinator acceptance.

The local Markdown target exists. Scoped trailing-whitespace and
conflict-marker scans are clean. The referenced accepted RI-46 source has
SHA-256 `5069d0a1bdfdd7e2725d16a3bce9f7b985f2ac720e9b104200f426c62541b3b7`,
matching its published identity; it was not modified. A final new-source
identity accompanies the handoff. Coordinator adjudication is separate and
recorded in the opening status.

Only this new note is authored. Accepted sources, coordinator records,
parallel measurement work and RET remain unchanged. RET remains paused;
the coordinator owns git/index/publication. Stop this bounded packet at
source-stable handoff for independent adjudication.
