# RI-61 — summable component suppression and the remaining defect drift

24 September 2026 UTC. **Conditional analytic consequences of the accepted
RI-59 law; independent coordinator adjudication accepted.** No selection rule
is changed. The existing canonical minimizer eliminates every nonnegative
objective coefficient. Strict mixing restores these proper components with
total row probability less than `eta_n/2`. Their expected total birth count
after the fixed prefix is at most `1/10`, and their count is finite almost
surely.

This controls more than one-shot rectangle cloning. An intrinsic class of
children all of whose incoming roles raise defect has summable occupation;
it includes repeatable twin-top towers. However, suppressing a clone need
not lower defect: its full alternative can raise just as much. The remaining
negative-coefficient mixed roles and noncritical full complements are isolated
below. Their asymptotic contribution is not proved small.

## 1. Fixed law, records and intrinsic diagnostic

Use the complete [RI-59 construction](../native_growth_expected_defect_v1/EXPECTED_DEFECT.md),
including the actual accepted prefix through parent size four, unconditional
history weights, potential normalization, canonical component order,
lexicographic tie-break and strict mixture. Its accepted source SHA-256 is
`94e6b03345a81c1f8718bced306dad2bf03c3061b1d16525ebc6ffea09a8fa2a`.
No seed, earlier row, future-law optimization or realized-state policy is
substituted. The [RI-38 model](../native_joint_growth_extension_criterion_v1/CRITERION.md)
still retains every ideal, every binary record assignment, strict
precursor-record locality, whole unmarked parent access, equivariance and
all natural-label diamonds. The full passive map remains `q(S)D/2` for
each newborn bit; the entire unnormalized kernel D is retained.

Let P_n be the order after n births. The
[RI-56 defect](../native_growth_ferrers_defect_v1/DEFECT.md) is

\[
 \delta(P)=\min\{|K|:P[V(P)\setminus K]\text{ is Ferrers}\}.
 \tag{1}
\]

Here Ferrers means an order isomorphic to a finite down-set of the product
order on `N^2`, including the empty order. K is arbitrary, not constrained
to be an ideal. It is used only for a comparison: no committed vertex,
relation or record is deleted. Defect is ideal-monotone and its increment
at a maximal birth is zero or one. Birth number is not a physical clock.

Fix a free parent layer `n>=5`. Index complete marked-parent classes by j
and all proper ratio components by c. Write

\[
 d_j(S)=\delta(P_j+x_S)-\delta(P_j),\qquad f_j=d_j(P_j).
 \tag{2}
\]

These increments depend on the unmarked orders, not the newborn bit.
All the RI-59 data `pi_j>0`, `u_j(S)>0` and `c(j,S)` are retained. Each
row sum below counts every labeled ideal occurrence, even when several
slots share a canonical node. History weights sum actual naturally labeled
marked-history probabilities, including their fair-bit factors.

## 2. Which component coordinates the exact minimizer eliminates

Expanding the accepted objective gives

\[
 \Phi_n(\alpha)=B_n+\sum_c\beta_{n,c}\alpha_c,
 \qquad B_n=\sum_j\pi_j f_j,
\]
\[
 \beta_{n,c}=\sum_j\pi_j
   \sum_{\substack{S\subsetneq P_j\text{ ideal}\\c(j,S)=c}}
        (d_j(S)-f_j)u_j(S).
 \tag{3}
\]

The feasible set is exactly RI-59's compact polytope

\[
 K_n=\left\{\alpha\geq0:
       \sum_{S\subsetneq P_j\text{ ideal}}
       u_j(S)\alpha_{c(j,S)}\leq1\quad\text{for all }j\right\}.
 \tag{4}
\]

It is coordinatewise downward closed: decreasing nonnegative coordinates
relaxes every cap. Therefore:

**Elimination lemma.** If `beta_(n,c)>0`, every minimizer has coordinate c
zero. If `beta_(n,c)=0`, RI-59's canonical lexicographic minimizer has
coordinate c zero as well.

For a positive coefficient, replacing a positive coordinate by zero preserves
feasibility and strictly reduces (3), contradicting optimality. For a zero
coefficient the same replacement preserves the objective and every other
coordinate. At the canonical minimization stage for c it preserves all
previously fixed coordinates and attains the lowest possible value, zero.
This handles the zero-cost case without assuming uniqueness of the whole
optimal face before tie-breaking.

Define the deterministic layer sets

\[
 \mathcal E_n=\{c:\beta_{n,c}\geq0\},\qquad
 \mathcal N_n=\{c:\beta_{n,c}<0\}.
 \tag{5}
\]

The support of `alpha_n^min` is contained in `N_n`; a negative coefficient
does not guarantee a positive coordinate because other caps may bind.
For clarity, write a negative coefficient as the difference of two explicit
nonnegative sums:

\[
 L_{n,c}=\sum_j\pi_j\!
   \sum_{\substack{S:c(j,S)=c\\f_j=1,\ d_j(S)=0}}u_j(S),\qquad
 G_{n,c}=\sum_j\pi_j\!
   \sum_{\substack{S:c(j,S)=c\\f_j=0,\ d_j(S)=1}}u_j(S),
\]
\[
 \beta_{n,c}=G_{n,c}-L_{n,c}.
 \tag{6}
\]

All sums in (6) are over proper ideals. Thus a negative component has more
weighted neutral-for-raising-full benefit than raising-for-neutral-full cost.
It must contain a neutral occurrence in a full-raising row. It can still
contain raising occurrences elsewhere.

In particular, if a proper component is **everywhere raising**, meaning
`d_j(S)=1` at every occurrence in every complete marked row, then

\[
 \beta_{n,c}=\sum_j\pi_j
      \sum_{S:c(j,S)=c}(1-f_j)u_j(S)\geq0.
 \tag{7}
\]

Such a component is eliminated at the boundary. This is a statement about
the entire component, not about a single raising slot. An empty-ideal birth
always raises from a nonempty parent, but its component can be mixed, as
RI-56's two-chain/antichain diamond demonstrates. No general suppression of
all empty births follows.

## 3. Uniform summable leakage, without occupation assumptions

Keep precisely the accepted mixture

\[
 M_n=\max_j\sum_{S\subsetneq P_j\text{ ideal}}u_j(S),\quad
 c_n=\frac1{2(1+M_n)},\quad \eta_n=\frac1{(n+1)^2},
\]
\[
 \alpha_n=(1-\eta_n)\alpha_n^{\min}+\eta_n c_n\mathbf1.
 \tag{8}
\]

For every `c in E_n`, the actual coordinate is exactly `eta_n c_n`.
Consequently, in every complete marked row j, the total proper-birth
probability through **all** these components is

\[
 s_n(j)=\sum_{\substack{S\subsetneq P_j\text{ ideal}\\
                       c(j,S)\in\mathcal E_n}}q_j(S)
       =\eta_n c_n\sum_{S:c(j,S)\in\mathcal E_n}u_j(S)
       \leq\frac{\eta_n M_n}{2(1+M_n)}<\frac{\eta_n}{2}.
 \tag{9}
\]

Both fair newborn bits are summed: `(q/2)+(q/2)=q`. There is no additional
bit factor or division by an ideal orbit. Everywhere-raising components
are a subset of this same total, not separate budgets to be added.

Let Z_n be the event that the actual birth at parent size n uses a proper
component in E_n, and let \(\mathcal F_n\) denote the complete history
sigma-algebra. Conditional on every such history,
\(\Pr(Z_n\mid\mathcal F_n)=s_n(j_n)<\eta_n/2\). Tonelli gives

\[
 \mathbb E\sum_{n=5}^{\infty}\mathbf1_{Z_n}
 \leq\frac12\sum_{n=5}^{\infty}\frac1{(n+1)^2}
 \leq\frac12\int_5^{\infty}x^{-2}\,dx=\frac1{10}.
 \tag{10}
\]

The count is finite almost surely, without independence. The probability
of any such post-prefix birth is at most `1/10`. The count is **not** bounded
by `1/10` pathwise. In contrast, the predictable rate sum itself is bounded
by `1/10` on every history because (9) is a uniform deterministic envelope.
This distinction differs from RI-59's one-shot rectangle hazard argument.

For any `m>=5`, the same bound and conditional expectation give

\[
 \mathbb E\!\left[\sum_{n=m}^{\infty}\mathbf1_{Z_n}
                       \mid\mathcal F_m\right]\leq\frac1{2m},\qquad
 \Pr(\text{some }Z_n,\ n\geq m\mid\mathcal F_m)\leq\frac1{2m}.
 \tag{11}
\]

These are consequences of the already defined law, not a new selector or
a conditioning-based reoptimization of its parameters.

## 4. Terminal-child invariance and an intrinsic occupation theorem

For a proper local node `[P,S,r|S]`, associate the unmarked terminal order
`T(P,S)=P+x_S`, up to isomorphism. Erasing outside-precursor marks does not
alter this order, and a transported node isomorphism transports its child.
For each complete RI-38 ratio edge, the two nodes are

\[
 [C+x_S,T,r|T],\qquad[C+y_T,S,r|S].
\]

Their terminal children are the same order `C+x_S+y_T`, after transporting
the named newborns. This covers equal precursors, loops, reversed edges and
all old/new record assignments. Therefore terminal-child unmarked order is
constant on every whole connected proper ratio component. The converse
that one terminal type determines one component is not assumed; marks may
split components.

Define the intrinsic class

\[
 \mathcal C=\{Q:|\operatorname{Max}(Q)|\geq2,\quad
       \delta(Q\setminus\{v\})=\delta(Q)-1
       \text{ for every }v\in\operatorname{Max}(Q)\}.
 \tag{12}
\]

Every incoming maximal birth into Q in C has parent `Q\{v}`. Its precursor
is proper because another maximal vertex remains incomparable with v.
It raises defect by (12). Terminal invariance makes every occurrence of
that incoming node's entire component another such raising role. Thus all
incoming components for Q are everywhere raising, for all records.

At a given parent row, the union of all births into C is a subset of the
single event Z_n. No sum over terminal classes or maximal-deletion
multiplicities is required. In particular, for child size `n>=6`,

\[
 \Pr(P_n\in\mathcal C\mid\mathcal F_{n-1})
       \leq s_{n-1}(j_{n-1})<\frac{\eta_{n-1}}2,
\]
\[
 \sum_{n=6}^{\infty}\Pr(P_n\in\mathcal C)\leq\frac1{10}.
 \tag{13}
\]

The entire union class C is visited only finitely often almost surely.
This is an occupation result under the actual endogenous law, not merely
a conditional bound on an individual named transition.

It also controls drift **from** critical parents. If `mu_n(j)` is the actual
row drift, then `0<=mu_n(j)<=1`, so

\[
 \sum_{n=6}^{\infty}\mathbb E[
     \mathbf1_{\{P_n\in\mathcal C\}}\mu_n(j_n)]\leq\frac1{10}.
 \tag{14}
\]

The same bound holds with any feasible boundary row drift in place of mu,
evaluated under the actual pi_n. Starting that sum at parent size five
adds at most `Pr(P_5 in C)`, an unchanged fixed-prefix term; it is not
assumed zero or bounded by the new mixing schedule. Actual defect-raising
births from critical parents likewise have finite expected count and occur
only finitely often almost surely.

The multiple-maximum restriction is essential. Let Q be a non-chain
rectangle followed by one full birth. It has a unique maximum and satisfies
the deletion-defect equality in (12), but its incoming role is full and
outside the proper ratio graph. This refutes applying the proper-role
argument to unique-max children; it is not a computed violation of a
probability bound for the selected law.

## 5. A repeatable twin-top tower, including its zero-cost trap

Let R be a product of chains of lengths `a,b>=2`, of size `N=ab>=4`, and
let B be R with its unique maximum removed. For every `k>=1`, define

\[
 P_k=B\oplus\operatorname{Ant}_k,
 \tag{15}
\]

where the k incomparable tops are above every point of B. These are finite
order constructions, not supplied spacetime coordinates. Write I_0,I_1
for R's two axis ideals. The
[RI-54 intrinsic corner lemma](../native_growth_ferrers_bottleneck_v1/BOTTLENECK.md)
identifies them up to interchange and proves that they are the only Ferrers
births from R. A full extension of R is not Ferrers.

### Largest retained orders and exact defect

The RI-56 twin-maxima lemma says that a Ferrers order with two distinct
maxima having identical strict past is exactly the three-element V.
Any induced Ferrers suborder of P_k containing at least two old tops
therefore has at most three vertices. With at most one top it has at most
N vertices. Retaining all of B and one top attains N. Since `N>=4`, every
largest retained Ferrers order is exactly B plus one top, a copy of R.
Consequently

\[
 \delta(P_k)=(N-1+k)-N=k-1.
 \tag{16}
\]

This proof allows arbitrary exceptional sets; it does not impose an
ideal-only deletion diagnostic.

### Exactly two neutral birth slots

Suppose a birth `P_k+x_S` is neutral. Its largest retained Ferrers order G
has N+1 vertices, must include x, and has an N-vertex old part. That old
part is an ideal of G, since x is a maximal birth; it is Ferrers and is
therefore exactly `R'=B plus one retained top`. The corner lemma forces
`S intersect R'` to be I_0 or I_1.

S cannot contain the retained top. Nor can S contain an omitted old top:
ideal closure would force all of B into S, whereas
`|B|=ab-1>max(a,b)` exceeds either axis size. Thus S contains no top and
equals one of the two axis ideals. Conversely, either axis birth extends
a retained R to a Ferrers order of size N+1, so is neutral. We have proved

\[
 d_{P_k}(S)=0\ \Longleftrightarrow\ S=I_0\text{ or }I_1.
 \tag{17}
\]

In particular, the B birth clones another top, giving P_(k+1), and raises
defect. The full birth also raises. Every marked tower row therefore has
drift `1-q(I_0)-q(I_1)`; making its clone probability small does not by
itself make that drift small.

### The entire clone component, not one convenient representative

The terminal child of the clone slot `[P_k,B,r|B]` is P_(k+1). All its
maxima are its twin tops; deleting any one gives P_k and restores it using
exactly B. Terminal invariance therefore forces every occurrence of the
clone component to have this parent/precursor form. In fact, for each
core-mark orbit the canonical local key is the same at every such role:
outside top marks are excluded, core marks are retained. Its component is
a single local node with only unit-gain loops. For `k=1`, the equal/full-
precursor diamond is based at B; it is not omitted from the graph.

At every occurrence both the clone slot and the full alternative have
increment one. Hence its coefficient in (3) is **exactly zero**, not merely
nonnegative. RI-59's canonical tie-break is essential to eliminating it:
an arbitrary expected-drift minimizer need not set a zero-cost coordinate
to zero. Its actual free-layer probability is entirely the strict mixture,

\[
 q_{P_k,r}(B)=\eta_n c_n u_{P_k,r}(B)<\eta_n/2,
 \qquad n=|P_k|\geq5.
 \tag{18}
\]

Reducing this boundary coordinate shifts its row mass into a full birth
which also raises. Its suppression is therefore not a direct proof of
reduced defect drift in that row.

There are k+1 possible maximal deletions of the child, but **one** clone
ideal B in a fixed parent row. Its two newborn branches have weights
`q(B)/2` each, for every complete parent marking. No multiplier k+1 and
no division by a top-permutation symmetry belongs in (18). Actual history
weights retain all distinct labeled marked cylinders.

Every `P_k` with `k>=2` belongs to C: deleting any maximal top gives
P_(k-1), whose defect is one less. Thus (13)–(14) control occupation and
drift of the union of these tower parents, across all permitted R and k,
not just repeated cloning from one fixed rectangle. Finite tower prefixes
remain possible because the admitted law is strict; infinitely many such
post-prefix visits have probability zero. The unchanged four-event
rectangle's birth to the five-event P_2 belongs to the fixed prefix and
is not governed by (18). The case `k=0` is a full birth from B to R and
is outside the proper-clone claim.

## 6. Exact remaining drift: mixed roles and full complements

Let q^0 be the auxiliary boundary layer from `alpha_n^min`, and q^I the
strict interior layer from `c_n 1`. Both have their full complements.
Neither is a substituted history law: all expectations here use the actual
RI-59 pi_n. At this one layer,

\[
 q_j=(1-\eta_n)q_j^0+\eta_n q_j^I
 \tag{19}
\]

for full and proper slots alike. Define

\[
 A_n=\sum_j\pi_j
      \sum_{\substack{S\subsetneq P_j\text{ ideal}\\
                       c(j,S)\in\mathcal N_n}}d_j(S)q_j^0(S),
 \qquad F_n=\sum_j\pi_j f_j q_j^0(P_j).
 \tag{20}
\]

Every positive proper contribution in A_n belongs to a **mixed** component:
an everywhere-raising component cannot have a negative coefficient, and an
everywhere-neutral component contributes no raising slot. Hence exactly

\[
 m_n=A_n+F_n,\qquad
 r_n:=\mathbb E[\delta(P_{n+1})-\delta(P_n)]
      =(1-\eta_n)(A_n+F_n)+\eta_n\Phi_n(c_n\mathbf1).
 \tag{21}
\]

Split A and F according to whether the parent belongs to C, writing
`A_n^C,F_n^C` and `A_n^out,F_n^out`. The critical boundary drift is bounded
by its occupation, so

\[
 \sum_{n=5}^{\infty}(A_n^{\mathcal C}+F_n^{\mathcal C})
 \leq\Pr(P_5\in\mathcal C)+\frac1{10}<\infty.
 \tag{22}
\]

In particular the critical full-complement contribution is summable; so
is the critical part of the mixed contribution. The exact remaining
expectation-level obligation can therefore be written

\[
 \frac1N\sum_{n=5}^{N-1}
       (A_n^{\mathrm{out}}+F_n^{\mathrm{out}})\longrightarrow0.
 \tag{23}
\]

By RI-59, (23) is equivalent to normalized defect tending to zero in
expectation, L1 and probability for this same law. Both terms are
nonnegative; their separate Cesaro means must vanish. No such decay is
established here. A small occupation of critical parents does not bound
full-raising noncritical parents or the raising roles of negative-coefficient
mixed components.

For an actual-path formulation, let V_n be a raising full birth or a raising
proper birth in N_n. Then

\[
 \delta(P_N)=\delta(P_5)+\sum_{n=5}^{N-1}\mathbf1_{V_n}+H_N,
 \quad H_N=\sum_{n=5}^{N-1}\mathbf1_{Z_n\ \mathrm{and\ raising}}.
 \tag{24}
\]

The nondecreasing H_N has a finite almost-sure limit with expectation at
most `1/10`. Its normalized contribution vanishes almost surely and in L1.
Births from critical parents may also be removed from the V count with a
finite almost-sure, finite-mean remainder by (14) and the size-five term.
This is an exact removal of bounded contributions from the *analysis*, not
removal of any records. The corresponding pathwise Cesaro residual-drift
condition remains necessary for an almost-sure conclusion via RI-56's
martingale result; (23) alone is not that condition.

### A genuine negative mixed component at every free layer

There is a concrete reason not to regard the remaining class as empty.
Let F be the five-vertex Ferrers hook `(4,1)`, with predecessor masks
`(0,1,3,7,1)`: a four-chain and an extra short-arm vertex above its minimum.
Let G be the four-vertex hook `(3,1)`. For `n>=5`, take the parent
`P_n^hook=F disjoint-union Ant_(n-5)`. Every nonempty Ferrers order has a unique
minimum, so a retained Ferrers suborder of a disjoint union must lie within
one component. Its largest size here is five, and `delta(P_n^hook)=n-5`.
Deleting the long-arm tip leaves G plus the same isolates, of defect n-5.
Thus this parent is never critical. Repeated empty births give a permissible order
path with no critical occupation and normalized defect tending to one.

Its empty birth has terminal `Q_t=F disjoint-union Ant_t`, where `t=n-4>=1`.
Every maximal deletion of this terminal has one of three parent/role types:

| Deleted terminal maximum | Parent | Restoring increment d | Full increment f | d-f |
|---|---|---:|---:|---:|
| An isolate | F plus t-1 isolates | 1 | 1 | 0 |
| Long-arm tip | G plus t isolates | 0 | 1 | -1 |
| Short-arm tip | Four-chain plus t isolates | 0 | 0 | 0 |

Here are the full-birth checks, rather than an assumed diagram identity.
Adding a universal top to F gives a six-vertex order of height five, not a
chain. A Ferrers order with a unique maximum is a rectangle; the non-chain
six-vertex rectangle has height four, so this order is not Ferrers. Its
largest retained size stays five. Adding a universal top to G gives a
non-chain five-vertex order, which cannot be a rectangle; its largest
retained size stays four. A four-chain instead extends to a five-chain.
Old isolates cannot enlarge these retained orders: combining two old
components, even under the new universal top, leaves multiple minima.
These facts prove all full increments in the table. The restoring increments
follow from the corresponding retained sizes five, four and four.

Terminal invariance means every occurrence in the empty-birth component
has one of these nonpositive reduced costs. It also contains a strictly
negative occurrence. In the old base `G plus t-1 isolates`, use the two
ideals consisting of the empty set and G's three-vertex long-arm chain.
Appending the long-arm tip first gives P_n^hook and then its empty birth;
appending the isolate first gives G plus t isolates and then the neutral
restoration of F. This is an actual complete ratio edge between the first
and second types. Compatible internal marks and both newborn bits are
included; `pi_j u_j(S)>0` at its negative occurrence. Therefore

\[
 \beta_{n,c}<0
 \quad\text{for this mixed component, for every }n\geq5.
 \tag{24a}
\]

All sums retain the actual labeled ideal occurrences in each parent row
and their history weights. The empty precursor occurs once in a fixed row;
terminal maximal-deletion multiplicities introduce no additional factor.
The empty role itself raises, so negative-coefficient
mixed components genuinely contain repeatable raising roles outside C.
Nevertheless, a negative coefficient does not force the constrained
optimizer to allocate positive boundary mass to that component. Nor does
positive probability of every finite path imply positive probability of
the infinite repeated-empty path. This is not a counterexample to RI-59,
an asymptotic lower bound, or a proof that its residual fails to decay.

## 7. Explicit comparison bounds without another law or an executed LP

At each actual recursively generated prefix, any certified vector
`gamma_n in K_n` provides

\[
 0\leq m_n\leq\Phi_n(\gamma_n).
 \tag{25}
\]

A nonnegative bound `Phi_n(gamma_n)<=epsilon_n` with vanishing Cesaro
average is sufficient for (23). Feasibility must hold for every complete
marked row and for the potentials and history weights of **this** actual
prefix. A feasible vector for another seed, another future-law distribution
or only a selected collection of rows is not such a comparison. These
vectors are proof witnesses, not replacements for the canonical optimizer.

One explicit comparison needs no optimization theorem beyond the existing
row caps. In general, if N_n is empty, elimination gives
`alpha_n^min=0` and `m_n=B_n`. The hook construction (24a) rules out that
case at every actual free layer here. With N_n nonempty, put

\[
 T_n=\max_j\sum_{\substack{S\subsetneq P_j\text{ ideal}\\
                            c(j,S)\in\mathcal N_n}}u_j(S)>0,
 \quad \Lambda_n=\sum_{c\in\mathcal N_n}(-\beta_{n,c})>0,
\]
\[
 (\gamma_n)_c=\begin{cases}1/T_n,&c\in\mathcal N_n,\\
                             0,&c\notin\mathcal N_n.
              \end{cases}
 \tag{26}
\]

Every proper row mass of this vector is at most one, so it is feasible.
This proves the explicit envelope

\[
 0\leq m_n\leq\epsilon_n:=
 \begin{cases}
 B_n,&\mathcal N_n=\varnothing,\\
 B_n-\Lambda_n/T_n,&\mathcal N_n\ne\varnothing.
 \end{cases}
 \tag{27}
\]

Nonnegativity of epsilon follows from its being a feasible expected drift;
the subtraction is not assumed positive without that reason. The data are
finite and rational at each layer, but their evaluation can be expensive.
By (24a), `Lambda_n/T_n>0` at every free layer, so `m_n<=epsilon_n<B_n`:
the boundary optimum strictly improves on the all-full comparison. There
is no size-uniform improvement bound, no requirement that a particular
negative component receive mass, and no claim that the strictly mixed
actual drift is below B_n.

No layer enumeration, coefficient table, trial vector or LP has been
numerically evaluated in this note. No decay of (27) is proved.

## 8. Three sufficient estimates with different conclusions

For any nonnegative envelope `epsilon_n>=m_n`, including (27), these
implications are valid for the retained law:

- If `N^(-1) sum_(5<=n<N) epsilon_n -> 0`, normalized defect tends to zero
  in expectation, L1 and probability.
- If `sum_(n>=5) epsilon_n/(n+1) < infinity`, normalized defect tends to
  zero almost surely as well.
- If `sum_(n>=5) epsilon_n < infinity`, total post-prefix defect increments
  have finite expectation and finite count almost surely; defect eventually
  becomes constant with an integrable limit.

The first and third follow from RI-59. For the middle statement, let
`X_n=delta(P_(n+1))-delta(P_n)`. It is nonnegative and RI-59 gives
`E X_n<=m_n+eta_n`. Thus

\[
 \mathbb E\sum_{n=5}^{\infty}\frac{X_n}{n+1}
 \leq\sum_{n=5}^{\infty}\frac{\epsilon_n+\eta_n}{n+1}<\infty.
 \tag{28}
\]

Tonelli makes the random series finite almost surely. On such a path, for
any fixed `m>=5` and `N>m`,

\[
 \frac1N\sum_{n=m}^{N-1}X_n
       \leq\sum_{n=m}^{\infty}\frac{X_n}{n+1}.
 \tag{29}
\]

The fixed initial part divided by N vanishes; the right-hand tail tends
to zero as m grows. This proves the almost-sure assertion without inferring
it from expectation convergence alone. Weighted summability is weaker than
summability of epsilon and does not require finitely many increments.
None of these estimates for the candidate's actual sequence is supplied
by coefficient signs, terminal invariance or critical occupation alone.

## 9. Evidence, scope and handoff

This is one analytic note. No executor, global finite-layer table, LP run,
numerical search, alternative seed or redesigned law has been introduced.
The history distribution and all actual record assignments remain those of
the accepted recursion. Bounds count complete labeled branches and both
newborn bits; terminal invariance is not a payload-only identification.

The main author and three independent reviewers read the complete core
note and the added hook/comparison argument. Analytic reviews found no
mathematical or scope blockers. They prompted an explicit clarification
that terminal isolate-deletion multiplicities do not multiply a fixed
parent's unique empty slot; the final wording retains the actual row
occurrences and history weights. The source was read back after correction.
These are human-readable proof reviews, not theorem-prover verification
or executed optimization. All four local links resolve; the accepted
RI-59 source hash matches the identity above. Scoped whitespace and
conflict-marker checks are clean. The reserved directory contains only
this note.

Proved here are component elimination under the exact tie-break, summable
leakage, a terminal-invariant critical occupation theorem, the repeatable
tower classification, and exact residual/comparison reductions. Open are
the decay of the residual in (23), the envelope in (27), any needed
almost-sure drift estimate, balanced morphology, metric reconstruction,
informative quantum coupling, source response, clocks and gravity. The law
and its premises are still conditional chosen structure, not newly derived
from DET primitives. Option B and metric-as-record Status M are unchanged.

Only this `SUPPRESSION.md` is authored. Accepted sources, measurement work,
RET and coordinator records remain untouched; RET stays paused. The
coordinator owns git/index/commit/push. Stop at the source-stable one-file
handoff for independent adjudication; no successor computation is opened
by this note.
