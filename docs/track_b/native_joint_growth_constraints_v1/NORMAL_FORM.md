# RI-34 — strict-local normalization before selecting a growth law

24 September 2026 UTC. **Bounded proof/premise note; independent coordinator
review accepted.** This note gives an elementary row-normalization theorem and
the first scalar-passive full-payload diamond boundary. It specifies no new
growth law, selects no coefficient table and supplies no executor. Neither
mathematical novelty nor native-law existence is claimed.

The scope follows [NG-01](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md)
after the accepted [RI-32 family rejection](../native_joint_growth_v1/DOSSIER.md).
The original [strict precursor-record permission](../../validation/t8-q-licensed-growth-2026-09-12/BIRTH_F.md)
is unchanged. Normalization must respect that permission, not bypass it through
a record-dependent denominator. The result below concerns normalized ideal
marginals, not arbitrary propensities or a proposed physical process.

## 1. Domain, slots and read permission

Fix a finite committed order `C=(V,prec)`, an admitted normalized full residual
`D`, and the complete setting/type/controller/context `gamma`. Let `J(C)` be
the set of its order ideals. For this conditional theorem admit **every**
binary record assignment `r in {0,1}^V`, independently of the fixed residual
and context. This mathematical preparation domain is an added premise, not
DET entailment, physical availability or permission to overwrite a record.
Comparisons are between different admissible states.

Use a fixed finite common envelope of slots `(S,b)`, with `S in J(C)` and
newborn record `b` in a declared alphabet. Ineligible slots are explicitly
zero maps; an eligible slot becoming zero remains in the envelope. Eligibility
or outcome omission must not conceal a forbidden record read. This small
domain has one committed birth per step and total branch mass one: no silent,
halt, absorption or never-commit mass is admitted. This is a scope restriction,
not a rejection of the [activity/commit distinction](../RECORD_PROCESS_CONTRACT.md).
Adding such alternatives changes the partition and its normalization equation.

For outcome-resolved unnormalized branch maps `B^X_(S,b)`, define

\[
 q_S(r|_S;D,\gamma)
   =\sum_b m_{S,b}\!\left(\mathcal B^X_{S,b}(D)\right),
 \qquad X=(C,r;D,\gamma).
 \tag{1}
\]

Here `m_(S,b)` is the declared target mass functional. Each admitted branch
has nonnegative mass. Strict precursor-record locality requires that the
selector and residual update read records only in `S`; hence (1) depends on
`r` only through `r|S` when the other inputs are fixed. Untouched old records
are nevertheless retained in the output history. Locality of the update does
not mean erasing those records or equating differently marked output histories.

The first theorem uses only these scalar marginals. It neither constructs the
maps in (1) nor infers operational linearity, positivity/closure of full maps,
or a quantum instrument from their masses. For the algebraic equivalence we
can first allow real-valued local tables, imposing nonnegativity separately.
Suppress the fixed `C,D,gamma` arguments until stated otherwise.

## 2. Exact finite-parent normal form

**Theorem.** Every local function `q_S:{0,1}^S -> R` has a unique expansion

\[
 q_S(r|_S)=\sum_{A\subseteq S}\theta_{S,A}\prod_{v\in A}r_v,
 \qquad
 \theta_{S,A}=\sum_{B\subseteq A}(-1)^{|A|-|B|}q_S(\mathbf1_B).
 \tag{2}
\]

The empty product is one. In `1_B`, exactly the coordinates in `B` are one;
all coordinates of `S\B` are zero. The coefficients are functions of the
fixed parent, residual and context if those inputs are subsequently varied.

Normalization on the full binary cube,

\[
 \sum_{S\in J(C)}q_S(r|_S)=1\quad\text{for every }r\in\{0,1\}^V,
 \tag{3}
\]

holds **if and only if**

\[
 \sum_{S\in J(C)}\theta_{S,\varnothing}=1,
 \qquad
 \sum_{\substack{S\in J(C)\\ A\subseteq S}}\theta_{S,A}=0
 \quad(\varnothing\ne A\subseteq V).
 \tag{4}
\]

For these to be stochastic rows, require separately

\[
 q_S(r|_S)\geq0\quad\text{for every }S\in J(C),\ r\in\{0,1\}^V.
 \tag{5}
\]

Equations (3) and (5) then also give `q_S<=1`. Individual coefficients need
not be nonnegative. Strict positivity, where used later, is an extra condition.

**Proof.** Evaluating a multilinear expansion at `1_B` gives
`q_S(1_B)=sum_(A subset B) theta_(S,A)`. Boolean subset-lattice Mobius
inversion gives (2), proving existence and uniqueness. Sum the expansions
over `S`, extending each to the cube on `V`. The coefficient of the empty
monomial is the first sum in (4); that of any nonempty monomial with support
`A` is the second sum. Uniqueness of multilinear functions on the full cube
makes equality with the constant function one equivalent to precisely (4).
Conversely those identities make the summed expansion identically one.
This argument is algebraic and does not establish (5), which together with
(4) is necessary and sufficient for nonnegative normalized rows. This proves
the statement for every finite parent, including the empty one.

The full independent cube is load-bearing. Agreement on reachable records,
a subset of preparations, averages over marks or a favored residual cannot
establish these coefficient identities on a larger domain. Conversely, an
explicitly smaller domain would require its own theorem rather than this
one's unrestricted coefficients. No coefficient matching across different
parents, relabeling equivariance or birth-order covariance follows from (4).

The all-zero row is retained exactly: `q_S(0)=theta_(S,empty)`. It must satisfy
normalization and every separately required map identity; it is not an average
record assignment that can be discarded after a positive-coupling check.

### Corollary: feedback requires compensating marginal changes

Fix a vertex `v`, all other marks, and the same `C,D,gamma`. Let `Delta_v q_S`
be the change from `r_v=0` to `r_v=1`. Locality and normalization imply

\[
 \Delta_v q_S=0\quad(v\notin S),\qquad
 \sum_{\substack{S\in J(C)\\ v\in S}}\Delta_v q_S=0.
 \tag{6}
\]

Indeed the first equality is the read permission, and subtracting two
normalized rows proves the second. If, **for this fixed flip and background**,
all affected ideal marginals change in a common weak direction (all changes
nonnegative, or all nonpositive), every change is zero. Any nonzero response
therefore requires both a positive and a negative change among ideals
containing `v`. The conclusion holds at every finite parent without dividing
by a branch probability, so support-changing zero values do not evade it.

This is a scoped no-go for common-sign response of **normalized ideal
marginals**. It is not a no-go for record feedback generally. Different ideals
may have opposite monotonicity directions; that is exactly the compensation
allowed by (6). Nothing comparable has been proved about raw weights before
normalization, the distribution of newborn outcomes within an ideal, or
processes with other mass-bearing alternatives. Marginal compensation can
also disappear when ideals are aggregated to the same unlabeled order question.

## 3. Additional premises for the first full-payload boundary

For the prefix calculation in sections 3–5, restrict to scalar-passive maps
with a fair binary newborn mark:

\[
 \mathcal B^{C,r}_{S,b}(D)=\frac{q_{C,r}(S)}2D,
 \qquad b\in\{0,1\}.
 \tag{7}
\]

The carrier is fixed, finite and nonempty; `D` is any complex Hermitian PSD
kernel with total-entry mass `m(D)=sum_(alpha,beta) D_(alpha,beta)=1`, and the full
kernel is retained. The scalar `q` is independent of `D`; (7) extends to the
unnormalized cone, so sequential composition multiplies the scalars without
normalizing away their weights. The context does not change. Append creates
one fresh maximal event with exactly precursor `S` and mark `b`, retaining
all old order and records. Fair marks and passivity are additional mathematical
restrictions, not DET consequences or a mechanism of quantum record formation.

Also assume **marked-parent equivariance**: transport the entire order,
records, precursor and newborn mark together under any isomorphism. Transport
both residual indices if the alternative carrier is renamed. This is needed
to use common functions across isomorphic parents and across exchanged
vertices of an antichain. It is not Lorentz covariance.

Initially require every ideal marginal to be strictly positive on every mark
assignment. The weak-positivity boundary is treated separately in section 5.
We classify only rows at parents of sizes zero, one and two, and all
incomparable-birth diamonds based at parents of sizes zero and one. Thus the
largest diamond terminal has three births. No diamonds based at size two or
larger, history extension or all-size covariant process are asserted.

### Rows forced by locality and normalization

The empty parent has `q_empty=1`. At a singleton `v` marked `r`, write
`q_empty=a`. The empty precursor cannot read `r`, and normalization forces
`q_{v}=1-a`. Both are mark-independent.

For a two-chain `v prec w`, the ideal marginals have the form

\[
 q_\varnothing=c,\qquad q_{\{v\}}=f(r_v),\qquad
 q_{\{v,w\}}=1-c-f(r_v).
 \tag{8}
\]

Strict locality makes `c` constant and allows `q_{v}` to read only the root
mark. Normalization then removes any tip-mark dependence from the full ideal.

For a two-antichain with marks `r_1,r_2`, locality, equivariance and
normalization instead give

\[
 q_\varnothing=d,\qquad q_{\{v_i\}}=g(r_i),\qquad
 q_{\{v_1,v_2\}}=1-d-g(r_1)-g(r_2).
 \tag{9}
\]

There is no mixed two-mark interaction, but normalization alone has not yet
made `g` constant. The two singleton ideals are distinct labeled transitions,
even when their children are isomorphic. They both contribute to the row sum.

## 4. Every incomparable-birth pair in the stated prefix

Take `S,T` as ideals of the **same old parent**. Birth `x` at `S` with mark
`b` and birth `y` at `T` with mark `h` are left incomparable: neither newborn
is inserted into the other's precursor. After canonical newborn identification
the required equality is

\[
 \mathcal B^{C+(S,b)}_{T,h}\circ\mathcal B^C_{S,b}
 =\mathcal B^{C+(T,h)}_{S,b}\circ\mathcal B^C_{T,h}.
 \tag{10}
\]

The notation includes the inherited records. Both sides have the same final
fully marked order, carrier and context after transport. Equality is of the
whole unnormalized maps, for every admitted `D` and both values of each
newborn mark, not just their masses or conditional residuals. In (7), the
displayed scalar identities suffice on the whole cone; mass-one `D` is
nonzero, so they are also necessary on the admitted normalized domain.

**Empty parent: `(empty,empty)`.** The first marked birth has scalar `1/2`.
The second, incomparable marked birth has scalar `a/2`, whichever newborn
comes first. Both compositions give `a D/4`. This holds for all `b,h`, using
the singleton's established mark-independence.

**Singleton parent: `(empty,empty)`.** Both intermediates are two-antichains.
Their empty-ideal probabilities are `d`, independent of every mark. Both
full maps give `a d D/4`.

**Singleton parent: `(full,full)`.** Here `full={v}` means the full **old**
singleton, not the full intermediate chain. Each intermediate is a two-chain;
the second birth again has precursor `{v}`, not `{v,x}` or `{v,y}`. Both
full maps give `(1-a) f(r_v) D/4`. Tip/newborn marks cannot enter `f`.
This equal-precursor case imposes no additional condition on `f(0),f(1)`.

**Singleton parent: mixed `(full,empty)`.** Adding `x` at `{v}` then `y` at
`empty` yields `(1-a)c D/4`. Adding `y` at `empty` then `x` at `{v}` yields
`a g(r_v) D/4`. Thus

\[
 (1-a)c=a\,g(r)\qquad\text{for each }r\in\{0,1\}.
 \tag{11}
\]

The reversed ordered pair `(empty,full)` gives the same equality in reverse,
with the newborn marks transported. There are no other ideals or pairs at
these base-parent sizes. Equal precursor sets have not been removed as
duplicates, and no averaging over newborn outcomes was used.

For the strictly positive family, `0<a<1`, so (11) forces

\[
 g(0)=g(1)=g=\frac{(1-a)c}{a}.
 \tag{12}
\]

Only now may the antichain full-ideal marginal in (9) be written `1-d-2g`.
All its ideal marginals are then record-independent. Exact strict-positive
row feasibility, together with every stated prefix diamond, is characterized
by (8), (9), (12) and

\[
 0<a<1,\quad c>0,\quad
 0<f(r)<1-c\ (r=0,1),\quad
 d>0,\quad d+2g<1.
 \tag{13}
\]

These imply `c<1` and `g>0`. Conversely they make each displayed row
strictly positive and normalized, and the four case calculations establish
all the declared prefix diamonds. This is a symbolic finite-prefix
classification, not a selected numerical table or a prescription beyond
these parents. No values of `a,c,d,f` are selected here.

In particular, these equations do not force `f(0)=f(1)`. From a two-chain,
the root-only precursor makes a fork and the full precursor makes a
three-chain; these are different unlabeled orders. A change in `f` therefore
survives that unlabeled order question, compensated by the opposite change
in the full-ideal probability. Under strict positivity and fair marks, both
root-mark values occur in chain histories with the same conditional full
residual and context. This is **finite-prefix freedom only**, not an
extendible candidate law, a full-domain/all-size covariance theorem, or a
quantum-to-geometry coupling.

The all-zero case `r=b=h=0` is included in every calculation; (11) must hold
there as well. Coincidence of the normalized residual `D` across two paths
would not prove (10) if their scalar weights differed.

## 5. Weak positivity and nonfaithful mass are different issues

The endpoints `a=0` and `a=1` are **outside** the strictly positive family.
In a separately considered weakly nonnegative prefix, retain equations
(8)–(11), require `0<=a<=1`, `c>=0`, `f(r)>=0`, `c+f(r)<=1`, and require
`d>=0`, `g(r)>=0`, `d+g(r_1)+g(r_2)<=1` for every pair of marks.
Keep (11) undivided:

- At `a=0`, it forces `c=0`, not constancy of `g(r)`. The mixed comparison
  has a zero factor on the antichain-first route. Antichain rows still obey
  their own positivity and normalization obligations.
- At `a=1`, it forces `g(r)=0`; it adds no condition on `c` or `f` beyond
  the remaining row constraints.
- For `0<a<1` in this weak family, (12) still follows, but `c` and `g` may
  be zero and the other inequalities may be saturated.

All equal-precursor calculations remain valid with their zero factors. In
the admitted all-parent domain, a parent unreachable from the designated
empty start does not thereby lose its obligations. Restricting the domain
would be an explicit premise change. In scalar maps (7), `q=0` is the literal
zero map; no conditioning or division by that mass is performed.

That last fact cannot be generalized from scalar maps to all total-entry-mass
kernels. For example,

\[
 N=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0,\qquad
 N\ne0,\qquad \sum_{i,j}N_{ij}=0.
 \tag{14}
\]

It is a nonzero unnormalized null-mass kernel, not an admitted normalized
state. Hence a zero-probability output of a more general branch need not be
the zero full payload or map. Structurally absent slots may be declared zero
maps, but that convention must not erase a nonzero null-mass output of an
eligible map. General full-map diamonds must retain those sectors; equality
of scalar masses alone does not establish (10).

## 6. Premise ledger, actual checks and stop

The proved statements are (2)–(6) on the full independent binary record cube
at every finite parent, and the explicitly restricted prefix classification
(7)–(13). Binary independent availability, complete one-commit mass, common
slots, and the scalar-passive/fair-mark subfamily are stated premises. Strict
record-read locality is retained, not relaxed. Equivariance is explicitly
added for the prefix classification. No factorwise past-stability condition
from another construction is asserted to be necessary for a general joint
law: compensating joint factors remain a separate possibility.

These elementary results supply admission constraints, not a native source
for joint weights, a quantum instrument, an all-size compatible family, a
history measure, a width law or geometric emergence. No target metric,
coordinates, supplied mesh, growth kernel, Hilbert space or preparation
amplitudes enter the proofs. Absence of those inputs is not a derivation from
DET. Physical clocks, mass, gravity, Option B and metric-as-record Status M
are unchanged; no new physical or empirical claim follows.

**Actual checks:** analytical Mobius inversion and coefficient matching;
subtraction of normalized rows; locality/equivariance reduction of the
empty, singleton and two-parent rows; every incomparable-birth pair at the
declared base sizes; strict versus weak positivity; and the null-mass kernel.
Two independent reviewers read the complete note and confirmed the mathematics
and scope without blockers; coordinator independent adjudication has also passed. No
project sources were executed, no finite enumeration or numerical pass count
is claimed, and no simulator, data acquisition or higher-parent search was run.
All four local document links resolve; scoped whitespace/conflict-marker checks
found no issues. These text checks are separate from mathematical validity.

**One bounded recommendation:** independently review and retain this
conditional normalization theorem and scoped boundary as prerequisites for
any later candidate selection. Do not implement the rejected RI-32 family or
promote the remaining prefix freedom to a growth law. A new candidate or an
extension problem requires its own centrally authorized scope and complete
full-payload obligations; none is specified or started here.

This single new note is the entire source reservation. No accepted maps,
sources, coordinator records, RI-33 observation work or RET implementation
are edited. Root owns git/index and publication. Release this reservation at
the source-stable handoff and stop for independent coordinator adjudication;
no automatic successor, NG-02, QR-05 series or retired work is opened.
