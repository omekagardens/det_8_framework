# DET proof synthesis and the next premise-selection problem

14 September 2026 UTC. Coordinator companion to the preserved
[original review](../../indep%20ndent_review.md), the accepted
[finite-record synthesis](FINITE_RECORD_OBSERVABILITY.md) and the maintained
[premise ledger](../coordination/OPERATIONAL_PREMISE_LEDGER.md).
Predecessor checkpoint: `8fd98734a721b07ec08fc5e5966e8c409f3bd715`.

**Decision:** consolidate the finite operational results and investigate the
composition premises needed to select strong positivity. RI-20 is a bounded
QR premise/probe audit. Its assignment is recorded in the
[implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md); this decision does
not adopt a new DET axiom or assign an approximate-protocol executor.

## 1. What the connected result now establishes

The project has moved beyond isolated examples. It has conditional domain and
instrument classifications, an observation/stability endpoint, one complete
finite weighted protocol, and a separate retained-word limit theorem. Their
combination makes the missing physical premises more specific. It does not
turn several compatible mathematical representations into a selected theory.

The domain chain has several different kinds of arrow:

| Starting point and result | Meaning of the arrow | Added premise or remaining limit |
|---|---|---|
| Maximal exact-recordability cone `K_P` → cell-weight quotient, RI-08a | Classification of all bounded full-domain effects and induced positive maps | A supplied partition and PSD domain; this maximal domain obstructs a richer operational quotient under those map/effect assumptions. |
| Supplied controls and all-word viability → local cone `C`, RI-08b | Selection relative to those controls and calibration | H/phase/Z availability and the viability rule are inputs. They are not selected by event order alone. |
| `C` → `C0`, RI-08c or RI-08d | Either the range of an actual ideal branch, or a restriction to inputs surviving a particular joint interface | A branch operation changes a state; an eligibility condition restricts a domain. These cannot be exchanged silently. `C0` is also a section image, but is not a face of `C`. |
| `C0` → joint image `K_t`, RI-08d/15 | One specified preparation, reference, coupling and exact source/history conversion | It is a four-dimensional image in a larger representation, not the entire two-qubit state space or universal ancillary compatibility. |
| `K_t` → cut-closed `L_t`, RI-08g | Minimal convex enlargement of the allowed return domain | Literal cuts become reusable on the changed type. Availability of arbitrary independent blocks is not thereby proved. |
| `L_t` → exact observation table, RI-08i/j | Injective measurement map and deterministic conditioning bounds under calibrated controls/readout | This concerns a supplied `L_t` source. It does not recover information an earlier instrument has already removed. |

The [premise ledger](../coordination/OPERATIONAL_PREMISE_LEDGER.md) supplies
links to each accepted statement and its exact cone, mass, effect and range
conditions. Here “mass” is a normalization functional, not rest mass.

Two later results close particular gaps recorded as open in the frozen
finite-record synthesis. [RI-18](../validation/t8-q-finite-protocol-composition-2026-09-14/PROTOCOL_COMPOSITION.md)
implements one finite path with its earlier branch/reference weights, exact
preterminal interchange, complete labels, zeros and unavailable stops. Its
66-coordinate scalar law preserves total incoming mass. It is not a general
interpreter for arbitrary policies or initial histories.
[RI-16](../validation/t8-q-retained-word-first-commit-2026-09-14/RETAINED_WORD_FIRST_COMMIT.md)
proves countable retained-word output convergence and uniformly bounded
word-dependent continuation for a fixed finite-input stationary policy.
That theorem supplies neither an arbitrary infinite-policy executor nor
convergence for changing models/controllers. These later closures belong in
this companion; the earlier source-bound synthesis stays unchanged.

## 2. Information must be followed from the original source

Three ranks answer three different questions. They must not be added or
substituted for one another.

* RI-08i has full rank 16 on its supplied four-block `L_t` span using three
  calibrated terminal settings. It reconstructs that supplied source.
* The complete ideal RI-18 scalar law has rank two on its original `C` span:
  it sees mass and Y expectation. Normalization leaves one affine parameter.
  The first ideal branch removes initial X, Z and both c directions.
* [RI-19](../coordination/QR_INTERFACE_ROBUSTNESS_PLAN.md) proves that the fixed
  suffix has rank four on each individual Hermitian branch payload. Its classified
  imperfect `C→C0` branches give original-input rank two, three or four when
  readiness is positive, according to their c dependence. Initial X/Z still
  do not enter. At zero readiness the rank is two.

Source snapshots and audit histories establish what a calculation used.
They are not additional observations of an unknown source. A downstream
injective read cannot undo a many-to-one upstream operation. Likewise,
comparison of scalar laws requires matched observed settings, preparation and
instrument identifiers, and all stop/read labels; an audit difference cannot
be erased if it is itself part of the declared observation alphabet.

RI-19 also separates approximation from admissibility. Arbitrarily small
repeatability error or raw distance to an ideal output can leave nonzero
output c and fail the exact polarized joint interface. Conversely, exact
`C0` output eligibility does not imply that the branch ignores input c.
For the classified branches `J2(pH+uK+vL)`, quotient descent is precisely
`K=L=0`. Restricting actual reachable inputs to `C0` is a different route to
quotient sufficiency. Either route needs its own justification; imposing
quotient descent because a qubit quotient is desired would assume the point
at issue.

## 3. The next substantial proof should address an upstream premise

The [strict finite derivation](../validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md)
explicitly starts with a complex strongly positive decoherence functional.
Its Hilbert/Gram construction and Born-form weights are conditional
consequences of that input. All the later PSD cone work inherits this
starting choice. Tensor-product preservation of PSD proves sufficiency;
it does not prove that weaker DET premises require PSD.

Original finding F3 survives the downstream progress. In particular, the
[grade-two counterexample](../../det8/models/grade2_justification.py) has the
real representing matrix

\[
D_+=\frac{J_3-I_3}{6}.
\]

Its total-entry mass is one, singleton weights are zero, pair weights are
`1/3`, and its eigenvalues are `1/3,−1/6,−1/6`. All event weights are
nonnegative. Every tensor power remains entrywise nonnegative, so positivity
of every self-composite event alone still admits this non-PSD example.
Indeed the class of normalized real entrywise-nonnegative Hermitian matrices
is closed under tensor products and convex mixtures. Bare grade two, weak
positivity and self-copy consistency therefore do not select strong
positivity. This is a mathematical extension of the existing countermodel,
not a new physical model.

### What is already known in the primary literature

Boës and Navascués prove that a non-strongly-positive functional fails to
compose with a suitable quantum functional built from two sequential
measurements (Lemma 3). They also construct, for every finite n, a functional
whose n copies satisfy positivity but whose n+1 copies fail (Lemma 2).
Consequently a fixed copy-depth test is not a universal substitute for
unbounded consistency.[^1]

Dowker and Wilkes prove that a tensor-closed class of weakly positive systems
lies either within the strongly positive class `S` or within the real
nonnegative-entry class `R+` (Theorem 4). Their Theorem 2 identifies universal
compatibility with `S` as `S` itself. Their stronger equality conclusion for
a tensor-closed class requires Galois self-duality (Theorem 3); ordinary
closure alone does not make an arbitrary class equal all of `S`.[^2]

A direct implication of the Theorem 4 dichotomy is useful here: **if an
admitted tensor-closed class contains even one resource outside `R+`, then
every member is strongly positive.** This is a logical consequence of the
cited theorem, not a DET novelty claim. One need not assume the availability
of every complex rank-one probe for this implication. One must, however,
justify mutual and repeated independent tensor composition without a fixed
copy bound, and weak positivity for every event in the resulting Boolean
algebras. A negative real event entry already excludes `R+`; this reasoning
does not select complex rather than real scalars.

For example, `b=(1,−1,1)` gives a normalized PSD resource `B=bb†` with a
negative entry. Its normalization is `|Σb_i|²=1`, not trace one. This only
exhibits a mathematical resource. It does not show that DET makes that
preparation available, or that its interfering alternatives form a
recordable probability partition. The pertinent investigation is whether
independently motivated DET composition/resource premises justify applying
the known theorem to the candidate class.

### A finite witness clarifies the resource burden

For any finite Hermitian candidate D and complex vector v, set

\[
b=(\overline v_1,\ldots,\overline v_n,
  1-\sum_{i=1}^n\overline v_i),\qquad B=bb^\dagger.
\]

Then B is PSD and has total-entry mass one. For the joint event
`E={(i,i):1≤i≤n}`, excluding the final ancillary outcome,

\[
\mu_{D\otimes B}(E)
=\sum_{i,j}D_{ij}b_i\overline b_j
=v^\dagger Dv.
\]

Thus positivity against all these available probes would force `D≥0`;
conversely PSD D composes positively with any PSD probe. The extra outcome
handles zero-sum v without division. This elementary finite calculation
illustrates the already-known universal-composition route. It imports a
rich probe family and the full joint event test; it does not derive either.
Decoherence normalization allows interfering subsets whose weights are not
probabilities in one common recorded partition.

Restricted probes change the conclusion. The normalized matrix

\[
D_i=\begin{pmatrix}1/2&i\\-i&1/2\end{pmatrix}
\]

has eigenvalues `3/2,−1/2` yet passes every test using a real PSD ancilla:
the imaginary terms cancel against the real symmetric ancillary event
matrix, leaving the PSD real part `I/2`. This does **not** defeat the
unbounded-class argument: the diagonal event in `D_i⊗D_i` already has
weight `−3/2`. Classical diagonal ancillas merely take positive weighted
sums of the original event tests. A finite phase alphabet by itself is
also not a no-go result: arbitrary magnitudes and grouping with phases
`1,−1,i,−i` can represent all complex vector directions.

These examples explain why “some probes,” “every probe,” “every self-power,”
and “every mutual product in an admitted class” are distinct premises.
Checking finitely many numerical examples cannot exchange their quantifiers.

## 4. RI-20: a decision contract for QR

The assigned [QR lane](../coordination/QR_HANDOFF.md) will audit the weakest
candidate starting point: finite Hermitian biadditive normalized kernels,
weak event positivity, and explicitly declared composition/resources, with
PSD not already assumed for the unknown kernel. It will credit the two
primary papers and distinguish importing a known theorem from establishing
its DET hypotheses.

| Obligation | Required result | Acceptance boundary |
|---|---|---|
| Global composition route | Check the one-interference-resource implication and map each hypothesis to actual DET premises or a named addition | `A⊆S` is not `A=S`; unbounded composability and full event positivity must stay explicit. |
| Probe adequacy | Establish or correct a closed-cone criterion for which allowed ancillary event tests force PSD | For Boolean incidence R and PSD B the test is `Tr(DT)` with `T=(RBR^T)^T`. Include normalization/base event tests and separation details. |
| Resource restrictions | Preserve positive-entry, real-probe, classical and finite-depth countermodels; distinguish finite fixed menus from continuously tunable or repeatedly composed resources | A finite menu of fixed linear tests cannot be confused with a finite gate alphabet generating infinitely many tests. |
| Repository premise audit | Inspect existing pair-kernel composition, fixed reference/coupler, supplied preparations and reconstruction assumptions | An accepted PSD implementation or an imported full-QM reconstruction cannot serve as a weaker independent derivation of PSD. |
| Next proof decision | Name the smallest unproved resource/closure claim that could improve the existing foundations | An honest failure or missing premise is a useful outcome; no automatic new instrument family or executor. |

A faithful preparation that distinguishes processes is a different object
from an ancillary resource that detects nonpositive event kernels. Neither
name licenses substitution. Likewise, grade-two event weights do not by
themselves fix the imaginary part of D; any chosen complex completion and
its composition law must be declared.

This audit does not yet prove its resource-cone target. It is a concrete
reviewable assignment. QR owns one new proof/design note plus its three
existing handoff/map files. Accepted statements, executable sources and the
411-witness registry remain held. Root retains independent acceptance and
scoped git/index publication. No RET or calibration work is opened.

## 5. Application value and the longer proof roadmap

The immediate application opportunity is an honest information and resource
contract. Before implementing another instrument, identify what quantity it
could distinguish and at what necessary precision. The accepted
[application corollary](../coordination/APPLICATION_WORK_PLAN.md) already
shows that sensitivity to the two c directions vanishes with readiness
and instrument strength `βκ`. For fixed known metadata and instrument,
necessary inverse constants are at least `25/(24βκ)` for u and `5/(7βκ)` for
v. A deterministic scalar-law error budget δ creates corresponding
worst-case ambiguities, capped by the balanced-source half-range `1/4`.
These are necessary limits, not an optimal estimator or sample-complexity
claim. Exact algebraic rank alone cannot promise useful precision.

That contract can support instrument comparison, impossible-target refusal
and experiment design once the resource catalogue, noise and cost model are
specified. The existing exact identifiability interface is a separate useful
route for supplied rational linear measurement maps. A measured pilot still
needs an instrument/dataset, target and tolerance, noise/calibration model,
conventional baseline, cost objective and held-out evaluation. None has
been selected here; synthetic law calculations do not fill those roles.

The substantial-proof sequence is therefore:

1. Resolve the composition premise audit and make one explicit resource or
   closure choice, or retain the countermodel showing that it is insufficient.
2. Justify a usable operational domain and transformation/preparation class
   from independent premises. Keep the known `C/C0` descent and admissibility
   obstructions as tests of any proposed choice.
3. Establish the additional instrument, composite and preparation richness
   needed for a genuine operational reconstruction. The repository's
   [conditional reconstruction](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
   already labels its larger postulate package as proposed and its theorem
   as imported; it is a benchmark for missing obligations, not their proof.
4. Connect a bounded observation target to an actual acquisition/evaluation
   contract. Extend software only where that target needs an absent operation
   or verifiable type bridge.

Strong positivity would close one upstream question under stated premises.
It would leave complex-field selection, unrestricted instruments/composites,
physical dynamics, apparatus availability and geometric limits separate.
Project wholeness means carrying those dependencies together with the
accepted results, rather than allowing a stronger downstream representation
to erase an unresolved upstream choice.

## Sources

[^1]: Paul Boës and Miguel Navascués, *Composing decoherence functionals*,
    Physical Review A **95**, 022114 (2017), [primary preprint](https://arxiv.org/abs/1609.09723),
    [full text](https://arxiv.org/pdf/1609.09723), Lemmas 2–3. Read 14 September 2026 UTC.

[^2]: Fay Dowker and Henry Wilkes, *An argument for strong positivity of the
    decoherence functional in the path integral approach to the foundations
    of quantum theory*, AVS Quantum Science **4**, 012601 (2022),
    [primary preprint v2](https://arxiv.org/abs/2011.06120v2),
    [full text](https://arxiv.org/pdf/2011.06120), Theorems 2–4 and discussion.
    Read 14 September 2026 UTC. The precise theorem hypotheses, rather than
    an abbreviated abstract characterization, are used above.
