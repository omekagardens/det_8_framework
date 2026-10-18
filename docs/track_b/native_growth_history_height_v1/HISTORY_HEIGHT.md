# RI-39 — classical histories and a linear-height screen

24 September 2026 UTC. **Conditional probability and regime-screening note;
independent coordinator adjudication accepted.** The fixed
[RI-38 extension](../native_joint_growth_extension_criterion_v1/CRITERION.md)
defines a classical probability measure on infinite, naturally labeled,
binary-marked histories. Its particular normalization also implies

\[
 \liminf_{N\to\infty}\frac{H(P_N)}N\geq\frac12
 \quad\text{almost surely}.
 \tag{1}
\]

Thus this normalization is rejected for a declared approximation target
requiring vanishing height density along the same birth-prefix exhaustion.
This does not reject all RI-38 selections, all geometries, or DET. Height is
not measured proper time; no dimension, width or gravitational conclusion
is drawn. The measure construction and the height argument are separate:
normalization suffices for the former, whereas the chosen full-birth lower
bound drives the latter.

## 1. Fix the law before discussing a realized history

Fix one admissible finite **seed law table**, retaining any chosen
`f(0)!=f(1)` feedback. Complete it at every later size with RI-38's explicit
maximal-deletion potentials `u` and fixed level scale

\[
 M_N=\max_{|P|=N,r}\sum_{S\subsetneq P\text{ ideal}}u_{P,r}(S),
 \qquad \varepsilon_N=\frac1{2(1+M_N)},
 \tag{2}
\]

\[
 q_{P,r}(S)=\varepsilon_Nu_{P,r}(S)\quad(S\subsetneq P),\qquad
 q_{P,r}(P)=1-\varepsilon_N\sum_{S\subsetneq P}u_{P,r}(S)>\frac12.
 \tag{3}
\]

Let `n_0>=1` be a finite cutoff such that (2)–(3) apply to every parent size
`N>=n_0`. All earlier tables are held fixed; this is a law choice, not a
condition that any particular history has occurred. Each scale was chosen
from the complete fixed law table, never from actual current records.

Retain strict positivity on every ideal/mark assignment, strict precursor-
record locality, complete marked-parent equivariance, one commit with total
mass one, fair newborn bits and the fixed context. The residual maps remain

\[
 \mathcal B^{P,r}_{S,b}(D)=\frac{q_{P,r}(S)}2D,
 \qquad b\in\{0,1\},
 \tag{4}
\]

with the complete fixed-carrier complex PSD kernel retained. Its mass is the
sum of all entries, initially one. The scalar probabilities are independent
of `D`. These are the previously admitted conditional model premises, not
physical preparation claims or a derivation from DET. Label/birth count is
bookkeeping, not a physical clock. There is no halt or silent branch in this
model; this does not identify every present activity with a committed record.

## 2. Canonical finite histories and cylinder probabilities

Let `H_N` denote the **finite set of histories** whose terminal carrier is
`[N]={0,...,N-1}`, whose order is naturally labeled, and whose records are
binary. In this section `H_N` is a set; longest-chain height is written
`H(P)` below. A naturally labeled order has `i<j` whenever `i prec j`.

An element `h_N` is equivalently its full marked terminal order or the birth
sequence `(S_0,b_0),...,(S_(N-1),b_(N-1))`. Every `S_j` is an ideal of the
already existing parent on `[j]`. The equivalence is exact: restriction to
the first `j` labels recovers that parent and the strict past of event `j`
recovers `S_j`. No future vertex was present at an earlier birth.

Define the weight of this **one labeled history** by

\[
 p_N(h_N)=\prod_{j=0}^{N-1}\frac{q_{h_j}(S_j)}2,
 \qquad p_0(\varnothing)=1.
 \tag{5}
\]

There is no sum over alternative natural constructions in (5). With RI-38's
notation it equals `2^(-N) W(h_N)`, not `W` itself. Its full unnormalized
payload is `p_N(h_N)D`, including every off-diagonal entry.

Let `pi_N:H_(N+1)->H_N` delete the last-born label and its record. Because
all distinct ideal/newborn-bit children are retained,

\[
 \sum_{h_{N+1}:\pi_N(h_{N+1})=h_N}p_{N+1}(h_{N+1})
 =p_N(h_N)\sum_{S\in J(h_N)}\sum_{b=0}^1\frac{q_{h_N}(S)}2
 =p_N(h_N).
 \tag{6}
\]

Induction gives total mass one at every finite level. Repeated use of (6)
proves consistency under restriction from any later finite level to an
earlier one. No independence between births is assumed: `q` can depend on
the retained marked parent.

For a fixed finite marked abstract order, RI-38's full diamonds and
equivariance give the same construction weight under natural relabelings.
But its finite **unlabeled** probability is the sum over distinct naturally
labeled marked terminal representatives. Labeled ideals with isomorphic
children are separate transitions. One must not replace this sum by one
`W`, or blindly multiply by a number of linear extensions: automorphisms
can identify permutations that produce the same labeled representative.

## 3. Existence and uniqueness of the classical history measure

Define the sample space

\[
 \Omega=\{(h_0,h_1,\ldots):h_N\in H_N,
                      \ \pi_N(h_{N+1})=h_N\text{ for all }N\}.
 \tag{7}
\]

Every finite history has an extension because every row has children; the
resulting order on the natural numbers is past-finite. Define its cylinder
`[h_N]={omega: omega_N=h_N}` and let `A` be the algebra of finite unions of
cylinders. Common-level refinement and (6) define a well-defined finitely
additive probability `mu_0` on `A`, with

\[
 \mu_0([h_N])=p_N(h_N),\qquad \mu_0(\Omega)=1.
 \tag{8}
\]

The foundational theorem used here is the finite-measure case of
**Caratheodory extension**: a nonnegative, countably additive premeasure on
an algebra, of finite total mass, extends uniquely to a measure on the
sigma algebra generated by that algebra. Countable additivity on an algebra
means additivity whenever a countable disjoint union is itself in the
algebra. See Scott Sheffield's primary
[MIT probability lecture, slides 12–14](https://ocw.mit.edu/courses/18-175-theory-of-probability-spring-2014/a6ba5c8f804fb87f3d76d4fd274367b2_MIT18_175S14_Lecture2.pdf).
Finite additivity alone would not meet that hypothesis; it is established
next for this particular history space.

Give each finite set `H_N` its discrete topology. The product of these finite
spaces is compact, and the compatibility conditions in (7) are closed, so
`Omega` is compact. In this countable finite-branch setting compactness also
follows by a diagonal subsequence or the infinite-branch argument for a
finitely branching tree. Cylinders are both open and closed in `Omega`.
Thus every member of `A` is open and compact.

Suppose disjoint `A_i in A` have union `A_* in A`. They form an open cover
of compact `A_*`, so finitely many already cover it. Disjointness forces
every other `A_i` to be empty. Finite additivity therefore supplies the
required countable additivity. This proves that `mu_0` is a finite premeasure,
not just a consistent notation for finite probabilities.

Caratheodory now yields a unique probability

\[
 (\Omega,\mathcal F,\mu),\qquad
 \mathcal F=\sigma\{[h_N]:N\geq0,h_N\in H_N\},
 \qquad \mu([h_N])=p_N(h_N).
 \tag{9}
\]

The sets are finite at each level and countable over levels, so this is also
the Borel sigma algebra of the described history space. No arbitrary
nonmeasurable set of histories is assigned a probability. No stronger
infinite quantum extension theorem is being used. Measure existence needed
normalized rows and nonterminating finite branching, not (3)'s height bound.
Strict positivity additionally makes each legal finite cylinder positive;
it does not make each individual infinite history a positive-probability atom.

### Conditioning and the scalar payload

A realized seed history `h_(n_0)` is distinct from the seed **law table**.
Its cylinder has positive probability. Conditional future probabilities are
`mu(A intersect [h_(n_0)])/mu([h_(n_0)])`, and the unchanged future rows
still determine the next birth. No records or law tables are rewritten.

For a fixed normalized full kernel `D`, define

\[
 \nu_D(A)=\mu(A)D,\qquad A\in\mathcal F.
 \tag{10}
\]

This finite-dimensional kernel-valued measure is countably additive entrywise
and in norm, with total-entry mass `mu(A)`. It agrees with the composed
scalar map on every cylinder. Conditioning on an event of positive mass
leaves the full residual `D`; no zero-mass conditioning is used. This retains
the payload's proper role without pretending that a classical scalar measure
derives a quantum decoherence functional, interference or informative
quantum-to-order coupling.

## 4. A modest measurable covariant event algebra

For a finite binary-marked order `T`, define its **marked stem event**

\[
 E_T=\{\omega:\text{some finite down-set of the infinite marked order}
                    \text{ is isomorphic to }T\}.
 \tag{11}
\]

A down-set includes all predecessors of each of its members. For a fixed
finite set of labels `I`, the condition that `I` is such a stem is determined
by a prefix through every label in `I`: no future-born vertex can precede
one of those earlier events. Its order, marks and down-set status can therefore
be checked at that finite level. That instance is a finite union of cylinders.
There are countably many finite `I`, so `E_T` is measurable.

Equivalently let `E_(T,N)` mean that some down-set of `P_N` is isomorphic
to `T`. Then these events increase with `N`,
`E_T=union_N E_(T,N)`, and `mu(E_T)=lim_N mu(E_(T,N))`. This is not merely
the event that the first `|T|` labels form `T`; a stem can be recognized later.

Marked stem events are invariant under any isomorphism of the complete
infinite order and records. Define

\[
 \mathcal F_{\rm stem}=\sigma\{E_T:T\text{ finite marked order}}
          \subseteq\mathcal F
 \tag{12}
\]

and restrict `mu` to it. Invariance is preserved by complements and countable
unions, so this is a specified measurable covariant event algebra. No claim
is made that it contains every covariant measurable event, separates every
infinite isomorphism class, or supplies a complete quotient-space measure.
Finite natural-label covariance by itself does not establish those stronger
statements or invariance under every infinite rescheduling transformation.

## 5. The height bound without independent births

Let `H(P)` be the largest number of vertices in a chain of finite `P`, with
`H(empty)=0`. Fix any possible realized history at size `n_0`, and write
`H_0=H(P_(n_0))`. All statements below are under its conditional history
measure; the bounds are uniform in that history and also hold conditionally
on the complete sigma field at size `n_0`.

For the next `m` births let `F_j` retain the entire marked history through
size `n_0+j`. Define

\[
 X_j=\mathbf1\{\text{birth }j\text{ uses the full current parent as precursor}\},
 \quad S_m=\sum_{j=1}^mX_j,\quad
 p_j=\mathbb E[X_j\mid\mathcal F_{j-1}]>\tfrac12.
 \tag{13}
\]

The conditional probability is `q(P)`, **not** `q(P)/2`: both newborn bits
are summed. The `X_j` need not be independent or identically distributed.
Each full-precursor birth raises height by exactly one. Other births do not
decrease height, so pathwise

\[
 H(P_{n_0+m})\geq H_0+S_m.
 \tag{14}
\]

For `t>=0`, conditioning on the whole preceding history gives

\[
 \mathbb E[e^{-t(X_j-1/2)}\mid\mathcal F_{j-1}]
 =p_je^{-t/2}+(1-p_j)e^{t/2}
 \leq\cosh(t/2)\leq e^{t^2/8}.
 \tag{15}
\]

The first bound uses `p_j>=1/2`. For the second,
`log cosh x<=x^2/2`: both sides vanish at zero and `tanh x<=x` for `x>=0`,
with evenness handling negative `x`. Iterating conditional expectations in
(15) gives `E exp[-t(S_m-m/2)]<=exp(mt^2/8)`. Exponential Markov and `t=4 delta`
then yield, for `m>=1` and `0<delta<=1/2`,

\[
 \Pr\!\left(
 H(P_{n_0+m})\leq H_0+(1/2-\delta)m
 \ \middle|\ h_{n_0}\right)
 \leq e^{-2\delta^2m}.
 \tag{16}
\]

Indeed the height event is contained in `S_m<=m/2-delta*m` by (14). The
inclusive inequality is valid even when the threshold is not an integer.
At `delta=0` the bound one is trivial; for `delta>1/2` the event is empty.
At `delta=1/2`, the sharper upper bound `2^(-m)` follows from needing no
full births. No independent-Bernoulli replacement was used at any step.

### Almost-sure conclusion and finite-seed offsets

For each rational `delta in (0,1/2)`, the sum over `m` of the right side
of (16) is finite. By the first Borel–Cantelli argument, the height event
occurs only finitely often: its probability of occurring after arbitrarily
large `M` is at most `lim_(M->infinity) sum_(m>=M) exp(-2 delta^2 m)=0`.
This uses a union bound and no independence.

Taking countably many such `delta` decreasing to zero, and retaining the
finite offsets, gives almost surely

\[
 \liminf_{m\to\infty}\frac{H(P_{n_0+m})}{n_0+m}
 \geq\lim_{\delta\downarrow0}\lim_{m\to\infty}
       \frac{H_0+(1/2-\delta)m}{n_0+m}=\frac12.
 \tag{17}
\]

This also holds under the unconditioned measure by summing over the finite
set of possible size-`n_0` histories. In a finite-`N` tail bound, `m` means
`N-n_0`, and `H_0` must not be dropped. Strict `p_j>1/2` at each step has
not supplied a uniform positive gap from `1/2`. This proof asserts neither
a strictly larger limiting fraction nor existence of a height-density limit.

## 6. Exact rejection and its scope

Declare the target screen to be

\[
 H(P_N)/N\longrightarrow0
 \quad\text{along the model's specified birth-prefix sequence}.
 \tag{18}
\]

The normalization (2)–(3) fails this screen: (17) holds almost surely,
and for every fixed `a<1/2`, the probability that `H(P_N)/N<=a` tends to
zero. In particular there is no convergence to zero either almost surely
or in probability. Any approximation target that explicitly requires (18)
under the same exhaustion is incompatible with this selected law.

This is not a theorem that every admissible RI-38 scale fails (18), nor that
every geometric model requires it. Applying the screen to a particular
Lorentzian reference ensemble requires that ensemble's actual sampling,
region, density and limiting assumptions; none are supplied here. Linear
height does not establish bounded width, a dimension, an elapsed time,
proper time or a gravity law.

Finite `H(P_N)` is intrinsic to that finite order, but an infinite natural
re-enumeration may change which down-set has size `N`. For example, the same
infinite order consisting of a chain disjoint from countably many isolated
vertices can be enumerated with chain vertices at square-numbered positions
(height density zero) or isolated vertices at those positions (height density
one). Both enumerate every vertex in natural order. This is a structural
illustration, not a positive-probability counterexample to (17).

Thus (16)–(18) are statements on the specified labeled history measure and
exhaustion. They are not automatically events of `F_stem` or invariant under
arbitrary infinite natural re-enumerations. The marked-stem construction does
not erase that distinction.

## 7. Smallest next law-selection question

The next question is not whether more finite cycle tests pass:

> For one fixed admissible prefix, can the remaining positive normalization
> freedom reduce height-raising probability while preserving locality, every
> ratio identity and all labeled row sums?

RI-38's proper potentials need not use the particular half-mass scale (2).
For fixed potentials `u`, write `U_j=sum_proper u_j(S)` and `M=max_j U_j`
over the complete next-layer table. Any **fixed** common scale
`0<epsilon<1/M` gives strictly positive full complements and preserves the
homogeneous ratio equations. Fixed positive scales per ratio-graph component
also preserve those equations, subject to every labeled proper-row sum
remaining strictly below one. Scales cannot depend on forbidden actual
record reads. Choosing a different scale changes later prefix tables and
potentials; their future values cannot simply be held unchanged.

Suppressing full births is only part of this question. For any ideal,

\[
 H(P+e_S)=\max\{H(P),H(S)+1\},\qquad
 \tau(P,r)=\sum_{S:H(S)=H(P)}q_{P,r}(S)
 \tag{19}
\]

is the actual conditional probability of raising height. A nonfull ideal
can contain a longest chain while omitting an unrelated vertex. Thus
`q(P)<=tau(P,r)`, and merely removing the full-birth floor does not prove
sublinear height. A fixed-prefix normalization decision should distinguish
these quantities and its chosen class of parent states. Failure of a uniform
worst-row suppression target would not alone reject a typical asymptotic
regime: those worst rows might rarely be visited.

No new scale, simulator, optimization executor, nonpassive model or physical
growth law is selected here. Positive extension, asymptotic behavior and a
geometric correspondence remain different obligations. The present rejection
is of a particular normalization **for target (18)**, not of the conditional
history construction or its retained record feedback.

## 8. Actual verification and handoff

The work is analytic: finite row refinement, compact-cylinder premeasure
construction, the stated extension theorem, stem measurability/invariance,
full scalar payload accounting, conditional exponential moments, the tail
bound and summable-tail argument. The primary measure-theorem source above
was checked directly; the probability bounds are derived here rather than
imported as an independence-based inequality. Independent internal proof and
scope reviews by three read-only reviewers covered the complete written note
and found no proof or scope blockers. Their concurrence is internal review,
not independent empirical evidence or coordinator acceptance. The reviewers
did not execute code or independently reopen the external theorem source.

No checker or simulation was needed or created, and no project source was
executed. There is no arbitrary probability-test count. Exact local link,
text-hygiene and source-identity checks are distinct from the proofs. The one
local Markdown target exists; the one external theorem source was checked
directly. Whitespace/conflict-marker checks were clean, and the reserved
directory contains only this note. SHA-256 source identities accompany the
handoff rather than a self-referential hash inside this file.

**Recommendation:** independently adjudicate this history measure and the
chosen-normalization rejection, then reserve the single fixed-prefix
height-raising normalization question in section 7 if further law selection
is desired. Its later asymptotic implications still require proof. This note
does not start that successor.

Only this new file is authored. Accepted sources, summaries, coordinator
records, public inputs, registry and RET files remain unchanged. Root owns
all git/index/publication operations. Release the source reservation at
stable handoff and stop this packet for independent coordinator review;
the wider authorized programme continues under root ownership. Option B,
metric-as-record Status M and the RET pause are unchanged.
