# RI-81 — local-mixture criterion and record-blind harmonic construction

24 September 2026 UTC. **Proof-only structural result; independently accepted
by the coordinator.** No new probability table, solver,
numerical search, adopted law or further cutoff test is introduced.

## 1. Objects, scope and conditional-probability domain

This note stays in the finite-order, fair-record, scalar-passive joint-map
setting of [RI-77](../native_growth_random_cutoff_locality_v1/LOCALITY.md)
and [RI-79](../native_growth_delayed_cutoff_locality_v1/LOCALITY.md).
It is not a theorem about arbitrary noncommuting quantum instruments.

P is a finite naturally labeled order, r assigns one immutable bit to each
vertex, and S is an individual labeled ideal of P. Write P+S for the
unmarked child formed by appending one new maximal vertex with past S.
The new bit is b. A component law i supplies, on every complete marked
parent, nonnegative probabilities q_i(P,r,S) summing to one over all S.
Its joint transition sends the whole unnormalized payload D to
\[
 \mathcal B^i_{S,b}(D)=\tfrac12 q_i(P,r,S)D.
 \tag{1}
\]
Precursor-record locality means q_i(P,r,S)=q_i(P,r',S) whenever
\(r|_S=r'|_S\), at the same whole unmarked P. It does **not** mean that
the whole-parent order may be discarded.

Assume each component is precursor-record-local, marked-order equivariant
and covariant: its products are independent of the natural construction
of the same terminal marked order, with full passive-map diamonds. For any
history ending at (P,r), strip the common fair-bit factor from its cylinder
probability:
\[
 W_i(P,r)=2^{|P|}\mu_i(P,r)=\prod q_i,
 \qquad 0\leq W_i(P,r)\leq1,\quad W_i(\varnothing)=1.
 \tag{2}
\]
These are central weights of an individual history, not probabilities
summed over all natural labelings. Covariance makes them terminal-order
quantities. They satisfy, for either newborn bit,
\[
 W_i(P+S,r\mathbin{\|}b)=W_i(P,r)q_i(P,r,S).
 \tag{3}
\]
The upper bound in (2) follows from the product of ideal probabilities;
it uses the stated fair-bit scalar architecture.

The component laws are given even at their own zero-weight histories.
Their declared local q_i may be used there, but cannot be recovered by
dividing (3) by zero. A central weight without such a complete component
law does not supply those missing conditionals.

Let I be finite or countable. A prior is a fixed family
\(\pi_i\geq0\), \(\sum_i\pi_i=1\), independent of the history and
records. Its mixture weight and induced probability are
\[
 W_\pi(P,r)=\sum_i\pi_iW_i(P,r),\qquad
 q_\pi(P,r,S)=
 \frac{\sum_i\pi_iW_i(P,r)q_i(P,r,S)}{W_\pi(P,r)}
 \quad\text{when }W_\pi(P,r)>0.
 \tag{4}
\]
Every sum here is finite in value by (2). Zero mixture weight leaves the
conditional undefined; it is not a probability-zero row and is not silently
assigned a fallback law.

## 2. What history mixing preserves without a locality theorem

The mixture of the normalized component cylinder probabilities is
normalized and prefix-consistent. At each finite depth there are finitely
many marked histories, so finite summation and a nonnegative countable
mixture interchange directly. Marked-order equivariance and centrality
also survive linear combination with the fixed prior.

At a positive-weight parent, (3)–(4) give the child/parent ratio for q_pi.
Summing over the finite ideal set proves normalization; each specified
newborn bit still contributes its separate factor 1/2. Along k births
through positive-weight parents, the full maps telescope to the
terminal/initial W_pi ratio multiplying the whole D/2^k.

If a first transition has zero mixture weight, every cylinder extending
that zero-weight child has weight zero. Its path contribution is therefore
zero without evaluating an undefined conditional at that child. This
preserves the cylinder-level diamond identity from a positive starting
history. No covariant or local *complete extension at zero-weight parents*
is asserted. If W_pi is positive everywhere, the ratio law is everywhere
defined and has the full passive-map covariance properties.

None of these facts alone proves record locality. The weights in (4) are
posterior weights, not generally the original prior.

## 3. Exact pointwise criterion for prior-robust record locality

Fix the same P and S and two assignments r,r' agreeing on S. For each
component put
\[
 A_i=W_i(P,r),\quad B_i=W_i(P,r'),\quad
 c_i=q_i(P,r,S)=q_i(P,r',S)\in[0,1].
 \tag{5}
\]
The equality defining c_i uses the component's declared locality. For a
prior pi define
\[
 L_A=\sum_i\pi_iA_i,\qquad L_B=\sum_i\pi_iB_i.
\]
An **admissible comparison prior** has \(0<L_A,L_B<\infty\). A prior
with either denominator zero does not define the comparison.
For abstract nonnegative arrays, finiteness is an explicit requirement;
for the component weights (2) it is automatic.

Call this fixed test **prior-robustly local** when its two conditionals
agree for every finite-support normalized admissible prior. Then:

**Theorem 1.** Prior-robust locality of this test is equivalent to
\[
 (A_iB_j-A_jB_i)(c_i-c_j)=0\qquad\text{for every pair }i,j.
 \tag{6}
\]

**Proof.** For any finite-support admissible prior, subtraction gives
\[
 (q_\pi(P,r,S)-q_\pi(P,r',S))L_AL_B
 =\sum_{i<j}\pi_i\pi_j
       (A_iB_j-A_jB_i)(c_i-c_j).
 \tag{7}
\]
Indeed, the ungrouped double sum has terms
\(\pi_i\pi_jA_iB_j(c_i-c_j)\); its diagonal vanishes and its two
orientations give each displayed pair. Thus (6) is sufficient.

Conversely, if a pair product in (6) is nonzero, its determinant is nonzero.
At least one A among that pair and at least one B among it are positive.
Any prior supported on those two indices with both masses positive is
therefore admissible. Equation (7) has just the one nonzero pair term,
contradicting prior robustness. This proves necessity even if one or more
individual likelihoods are zero. If no admissible finite prior exists,
all A's or all B's vanish; every determinant vanishes and both sides of
the theorem are vacuously satisfied. No posterior equality is then claimed
at an undefined comparison. \(\square\)

For a whole family of component laws, prior-robust record locality means
that (6) holds at **every** P,S and same-S record pair. The theorem is
pointwise and does not replace those global quantifiers by one test.

### Countable priors

For any countable prior with finite positive L_A,L_B,
\[
 \sum_{i,j}\pi_i\pi_j A_iB_j|c_i-c_j|
 \leq L_AL_B<\infty.
 \tag{8}
\]
Hence the double-series expansion and grouping in (7) are justified by
absolute convergence. Equivalently, the sum of absolute values of the
unordered pair terms is at most L_A L_B, since
\(|A_iB_j-A_jB_i|\leq A_iB_j+A_jB_i\).
Thus (6) also gives locality for every admissible countable prior. The
converse follows because finite-support priors are included. In the growth
setting the likelihood sums are at most one, although their positivity
must still be checked.

## 4. Active-vector dichotomy, including one-sided zeros

Discard only indices for which \((A_i,B_i)=(0,0)\), since they cannot
affect either conditional and their c_i are unconstrained. Call all other
indices active. On this active set, (6) is equivalent to the following
inclusive alternative:

1. All c_i are equal; or
2. All nonzero likelihood vectors \((A_i,B_i)\) lie on one common
   nonnegative ray, meaning they are positive scalar multiples of one
   fixed nonzero vector.

**Proof.** Either alternative plainly implies (6). For the converse,
suppose active c_i are not all equal and select i,j with c_i≠c_j.
Equation (6) forces their determinant to vanish. Nonzero nonnegative
two-vectors with zero determinant are positive scalar multiples. For any
other active k, if c_k≠c_i use the pair k,i; otherwise use k,j.
In either case its vector is proportional to the same ray. \(\square\)

Under a nonempty admissible-prior domain, the ray in alternative 2 has
both coordinates positive. An axis ray would make one entire likelihood
sum zero. One-sided-zero active components are therefore not harmless:
if contrasts differ, they can obstruct the common-ray condition.

In alternative 1 the common transition probability makes posterior
changes irrelevant to this test. In alternative 2 write
\((A_i,B_i)=t_i(a,b)\). Whenever both conditionals exist, their posterior
weights are identical:
\[
 \frac{\pi_iA_i}{L_A}=
 \frac{\pi_it_i}{\sum_j\pi_jt_j}=
 \frac{\pi_iB_i}{L_B}.
 \tag{9}
\]
The alternative is pointwise in P,S,r,r'; it is not one globally uniform
choice of branch for every record-locality question.

## 5. One fixed prior is weaker than prior robustness

For a single admissible prior define posterior vectors
\(\alpha_i=\pi_iA_i/L_A\), \(\beta_i=\pi_iB_i/L_B\).
Locality for this one test is precisely
\[
 \sum_i(\alpha_i-\beta_i)c_i=0.
 \tag{10}
\]
The series is absolutely summable. This is an orthogonality/cancellation
condition, not equality of the posteriors or a pairwise condition.
With exactly two positively weighted active components, (7) has only one
pair term, so equality already forces that pair product to vanish. A
zero prior mass or an inactive component is not a two-component test.

### Algebraic cancellation example — not a native growth model

Take only the following arrays at a single hypothetical comparison:
\[
 \pi=(1/3,1/3,1/3),\quad
 A=(1/4,1/2,3/4),\quad B=(1/2,1/2,1/2),\quad
 c=(1/4,3/4,1/4).
 \tag{11}
\]
Both denominators are 1/2 and both numerators are 5/24, so both posterior
means are 5/12. Yet the unweighted pair products in (7), in order 12,13,23,
are \(1/16,0,-1/16\). They cancel for this prior, but do not individually
vanish. Replacing the prior by \((1/2,1/2,0)\) gives means 7/12 and 1/2,
with difference 1/12.

The likelihood entries and transition probabilities in (11) lie in (0,1),
and its prior is normalized. No claim is made that these arrays extend to
complete normalized covariant local
component laws on every order. This example establishes only the algebraic
distinction between fixed-prior cancellation and prior robustness.

## 6. RI-77 and RI-79 as applications, not further cutoff predictions

At the already studied parent Q=K_m⊕1, fix the appended record bit and
compare the inherited old markings r,r'. Write
\(L_r=W_B(K_m,r)>0\),
\(b_r=q_B(K_m,r,K_m)=1-a_mU_m(K_m,r)\), and let
\(g=q_B(Q,r\mathbin{\|}0,\varnothing)>0\), independent of all records.
For the component cutoff R, the likelihood two-vector and empty-precursor
probability at Q are:

| Component | Likelihood vector at Q | c_R |
|---|---|---:|
| R=m | \((L_r,L_{r'})\) | 0 |
| R=m+1 | \((L_rb_r,L_{r'}b_{r'})\) | 0 |
| R≥m+2 | \((L_rb_r,L_{r'}b_{r'})\) | g |

The first component has already bridged; the second is now at its bridge;
the last group still follows B. Fair-bit factors have been stripped exactly
as in (2). The only possibly nonzero pair products are between R=m and
R≥m+2. Each equals
\[
 -L_rL_{r'}g(b_{r'}-b_r).
 \tag{12}
\]
For a prior with first positive atom w_m and tail s_(m+2)>0, these terms
all have the same nonzero sign when b varies. No three-component
cancellation is available. Equation (7) reduces to the previously proved
\[
 \Delta q_\pi(\varnothing)=
 -\frac{s_{m+2}g w_m a_m\,\Delta U_m}
 {(w_m+s_{m+1}b_{r'})(w_m+s_{m+1}b_r)}.
 \tag{13}
\]
Here Delta means r' minus r, the opposite subtraction order from (7).

RI-77 supplies its exact m=6 witness for its specified prior; RI-79
supplies the exact m=7 witness for the stated first-atom-seven/s9>0 class.
The structural criterion explains those failures without repeating their
arithmetic or extending them to later first cutoffs. It also does not
reject priors excluded by those notes or every latent-state construction.

## 7. A positive record-blind harmonic subclass

Fix a strictly positive normalized equivariant covariant record-local
baseline B in the architecture (1)–(3). Let h(P) be a finite strictly
positive function of the **unmarked isomorphism class** of P, with
h(empty)=1. Require, for every complete record row r,
\[
 \sum_{S\text{ individual ideal of }P}
 q_B(P,r,S)h(P+S)=h(P).
 \tag{14}
\]
This is simultaneous harmonicity for all record rows, not an average over
records or a condition only on a selected support.

**Theorem 2.** Under (14),
\[
 q_h(P,r,S)=q_B(P,r,S)\frac{h(P+S)}{h(P)}
 \tag{15}
\]
defines another strictly positive normalized equivariant record-local
law with fair newborn bits and full passive-map covariance. Its central
weights are
\[
 W_h(P,r)=W_B(P,r)h(P).
 \tag{16}
\]

**Proof.** Positivity is immediate; (14) divided by h(P) gives
normalization. For fixed P,S the multiplier in (15) reads no record, so
the baseline's precursor-record locality is preserved. Parent/ideal
isomorphisms preserve the multiplier and baseline row, giving equivariance.
Along any finite growth path the h factors telescope to h(terminal)/
h(initial). Thus each incomparable-birth diamond multiplies both baseline
routes by the same h(terminal)/h(parent); the entire D/4 payload identity
is preserved, not only its scalar trace. The same telescoping from the
empty root, with h(empty)=1, proves (16) and all finite-history covariance.
The separate fair newborn-bit factor in (1) is unchanged. \(\square\)

### Exact preservation of the actual held prefix

Take B to have the actual accepted marked rows at parents n<6. Requiring
\[
 h(P)=1\quad\text{for every unmarked order with }|P|\leq6
 \tag{17}
\]
preserves all those rows exactly: each relevant parent and child in (15)
has size at most six. Conversely, if every such held row is preserved,
strict positivity of q_B forces h(child)=h(parent) along every edge through
six births. Starting at h(empty)=1 and using any natural construction of
each finite order proves (17). This is an equivalence for the positive
subclass, not a condition only on sampled or graft-supported histories.

## 8. Converse for record-independent relative central weights

**Theorem 3.** Let i be another strictly positive normalized equivariant
covariant fair-bit scalar law. If
\[
 \frac{W_i(P,r)}{W_B(P,r)}
 \quad\text{is independent of r for each fixed P},
 \tag{18}
\]
then this ratio is exactly an h satisfying (14), and the law is (15).

**Proof.** Both weights are positive and finite. Their ratio defines a
positive finite h(P), normalized at the root. Equivariance makes this
record-independent function invariant under unmarked isomorphisms.
Divide the two last-birth identities (3), using (18) at both parent and
child. This gives
\(q_i(P,r,S)=q_B(P,r,S)h(P+S)/h(P)\).
Normalization of each complete q_i row then gives (14). \(\square\)

Together Theorems 2 and 3 characterize the **record-independent relative
weight subclass with respect to the fixed B**. They do not characterize
all record-local laws or all mixtures that happen to preserve locality.
The constant-transition branch of Theorem 1, and fixed-prior cancellations,
must not be silently discarded to claim such a converse.

## 9. Compatible finite and countable mixtures stay in the subclass

Let every h_i satisfy the positive conditions (14) with respect to the
same B, and let pi be any finite or countable normalized nonnegative prior.
At any fixed marked history, Theorem 2 and normalization give
\[
 0<h_i(P)=\frac{W_i(P,r)}{W_B(P,r)}
 \leq\frac1{W_B(P,r)}<\infty.
 \tag{19}
\]
The right-hand side is uniform in i at this fixed history. It is not a
uniform bound over all histories or sizes. Consequently
\[
 h_\pi(P):=\sum_i\pi_i h_i(P)
\]
is finite and strictly positive at each P, and h_pi(empty)=1. Positivity
uses the strict positivity of every h_i and at least one positive prior
mass; for merely nonnegative components it would need a separate check.

All terms are nonnegative, the parent has finitely many labeled ideals,
and the pointwise bounds also hold at each child. Hence interchange is
justified and
\[
 \sum_Sq_B(P,r,S)h_\pi(P+S)
 =\sum_i\pi_i\sum_Sq_B(P,r,S)h_i(P+S)
 =\sum_i\pi_ih_i(P)=h_\pi(P).
 \tag{20}
\]
Thus h_pi satisfies every harmonic row and defines a law in the same
subclass. If all h_i obey (17), so does h_pi. Furthermore
\[
 W_\pi=W_Bh_\pi,\qquad
 q_\pi=q_B\frac{h_\pi(P+S)}{h_\pi(P)},\qquad
 \mathbb P(i\mid P,r)=\frac{\pi_i h_i(P)}{h_\pi(P)}.
 \tag{21}
\]
The last expression depends on the unmarked parent but not its records.
It is generally not the original prior. For the pointwise test in
Theorem 1, each likelihood vector is
\(h_i(P)(W_B(P,r),W_B(P,r'))\), which is exactly its common-ray branch.
This proves prior-robust locality without relying on cancellation.

These are finite-cylinder statements. No single infinite-path density,
uniform-integrability claim or asymptotic geometric conclusion is inferred
from the finite-history ratios.

## 10. Harmonicity as simultaneous exact linear constraints

Assign one variable x_T=h(T) to each unmarked order isomorphism class T.
For a parent P and each child class T represented by P+S, define
\[
 a_{P,r,T}=\sum_{S:\,[P+S]=T}q_B(P,r,S).
 \tag{22}
\]
The sum is over **every individual labeled ideal** producing that child
class. Distinct ideals that happen to yield isomorphic children retain
their contributions; no orbit division or representative-ideal substitution
is permitted. The same x_T is shared across all occurrences of that child
class, including occurrences under different parents.

Choose one reference record assignment r0 for P. Equation (14) for all
record rows is equivalent to
\[
 \sum_T a_{P,r_0,T}x_T=x_{[P]},\qquad
 \sum_T(a_{P,r,T}-a_{P,r_0,T})x_T=0
 \quad\text{for every complete record assignment r}.
 \tag{23}
\]
Necessity follows by subtracting the reference equation from each row.
Sufficiency follows by adding it back. Thus the admission problem has a
reference-row normalization and every record-row difference annihilation
equation, together with positivity, the root condition and any held-prefix
conditions. Each parent's block is finite; the all-size problem couples
all such blocks through the shared variables. When the baseline entries
are exact rationals these are exact rational linear constraints; their
form does not require rationality in general.

The trivial solution h≡1 always satisfies them by normalization, reproduces
B, and yields no new mixture dynamics. The remaining research problem is
whether there exists a **nonconstant, strictly positive, all-size** solution
with the held prefix, and, separately, whether any such solution proves a
specified nontrivial geometric property. No nonconstant solution is supplied
or claimed here. A finite truncation, a merely signed solution or one that
satisfies only an averaged record row would not discharge that problem.

This is an admission/construction criterion for a future native-law
question. It establishes neither a unique DET derivation nor shape
improvement, informative quantum dynamics, emergent geometry, mass or
gravity. No successor search or adopted-law change is started.

## 11. Review and handoff

This one-file note received two complete independent mathematical reviews
and a separate complete adversarial edge-case review. They checked the
zero-aware pairwise equivalence, active-vector dichotomy, absolute
convergence, fixed-prior example, accepted-cutoff applications, harmonic
construction/converse, exact held-prefix equivalence, countable closure
and shared-variable linear constraints. All passed. The review clarified
the explicit component-locality premise and the probability-array wording;
neither correction required a new example or calculation.

The three-component example was checked by exact hand arithmetic. It is
an algebraic illustration, not a numerical experiment or a full native
model. These are mathematical proof reviews, not proof-assistant
formalization or executable verification. No inherited checker, solver,
new coefficient calculation or probability-row reconstruction was run.

Durable worker evidence is in
`/Volumes/AI_DATA/development/det-review-evidence/ri81-qr/worker-pjmHy2/`:
the final note snapshot, `SOURCE_CHECK.json`, `REVIEW_RECORD.json` and
`HANDOFF_MANIFEST.json`. The source check covers byte identity, local
references, equation labels and whitespace; it does not claim to verify
the theorems mechanically.

The source-stable one-file packet is ready for coordinator adjudication.
Only the trivial h≡1 solution is guaranteed here. The actual nonconstant,
positive all-size construction problem remains open, and no successor is
started. Accepted sources, RET, measurement, ledgers/coordinator records
and git/index remain outside this worker's edits. Worker review is not
coordinator acceptance or publication.

## 12. Coordinator adjudication

The coordinator independently read the complete mathematical note and verified
the worker source/evidence and published application references. A separate
complete reviewer also accepted every proof, including null-history domains,
countable convergence, the restricted converse and the finite-history scope.
The original 20613-byte worker note has SHA-256
`60b09934159f2db29be27cd0b82e8e22472d62db355963d8da2c7592dba669f1`.
The independent review is retained at
`/Volumes/AI_DATA/development/det-review-evidence/ri81-root-review/INDEPENDENT_REVIEW-20260924T233510Z-d39569a6.json`,
11198 bytes, SHA-256
`6ce4004ac523c3afb4eb95c856ae333bd08f64c810764b64ab04e037e2a3b41a`.
This is mathematical review, with no new probability execution or proof-assistant
claim. The mathematical text is unchanged by this acceptance update.

RI-82 is now separately assigned: an explicitly bounded first-departure
construction question with complete parent-deletion closure and a finite
expected-width bias target. Its source/domain/resource design precedes any
coefficient execution. No nonconstant positive all-size h or asymptotic
geometric improvement follows from the present acceptance.
