# Operational premises, result boundaries and composition obligations

13 September 2026. RI-13 coordinator consolidation of the accepted review
implementation and QR results through RI-08j and RI-16, including RI-15
interoperability, accepted RI-18 finite composition and RI-19 interface
robustness below. The
[implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md) and
[progress record](REVIEW_PROGRESS.md) carry current ownership and acceptance.
The [original review](../../indep%20ndent_review.md) remains a dated assessment.

**The project now has a connected sequence of conditional mathematical
results, but it does not yet have one selected physical operational theory.**
Several useful arrows are proved; others require a new domain, an available
operation, or an explicit history-preserving interface. This ledger states
which is which. It does not modify the accepted statements or promote their
software to a validated public API.

## 1. Evidence and authorization are different coordinates

| Coordinate | Current evidence | Boundary |
|---|---|---|
| Conditional mathematics | Written arguments classify domains, effects and selected instruments, prove finite equivalence/limit results, and exhibit countermodels. | A theorem establishes its conclusion under its premises; it does not establish that the premises describe an apparatus or the physical world. |
| Executable witnesses | The [research registry](../research/registry.json) pins statement documents and complete local source closures. The [runner guide](../RESEARCH_CHECKS.md) states the execution contract. | Exact finite tests check calculations and source behavior. Normal and optimized runs repeat the same witnesses; neither is a proof of a universal quantifier. |
| Research authorization | The user authorized this implementation program and coordination with the bounded QR lane. The [development plan](../CORE_HARDENING_AND_APPLICATION_PLAN.md) recognizes that scope. | Permission to investigate does not change the broad claim's evidence level or the support status of a module. |
| Public software support | The authoritative [claim registry](../CLAIM_REGISTRY.md) separates supported core, unvalidated RET preview and experimental modules. | Accepted standalone QR bundles and the new applied helpers do not inherit core support. Broad quantum correspondence and causal-growth status remain separate from bounded proof acceptance. |
| Release and calibration | [G1 closure](../validation/g1-core-hardening-2026-09-04.md) is historical and source-bound. G2 remains open in the [RET SDK contract](../RET_SDK.md). | A dirty current checkout is not certified by an older G1 source identity. No synthetic example, research-suite count or ledger closes G2. |
| Measured application | RI-12 provides exact identification certificates and a synthetic public-API comparator fixture. | No instrument/dataset, frozen objective or empirical benefit has yet been selected and demonstrated. |

Registry hashes bind the executable versions used for acceptance; historical
pins and test counts are retained in the progress record. This ledger is a
source-linked mathematical synthesis, not another frozen validation capture.
The runner checks source identity and restricted imports; it is neither a
hostile-code sandbox nor a proof that no transient file change occurred.

## 2. The domains must be named before combining results

Here **mass** means the normalization functional, not physical rest mass.
For raw kernels it is total-entry mass unless a stated restriction makes it
equal to ordinary trace. Dimensions below are real linear-span dimensions;
normalization usually removes one affine degree of freedom.

| Domain | Dimension and normalization | What selects or defines it |
|---|---|---|
| Entire PSD raw-kernel cone | Full Hermitian span; total-entry mass is generally nonfaithful. | The rejected full-domain candidate in [operation-domain](../validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md). Its positive complete linear instruments have state-independent effects. |
| Maximal exact-recordability cone `K_P` for n events and k nonempty partition cells | Span `n²−k(k−1)`; cell-weight image `R_+^k`, kernel dimension `n²−k²`. For n=4,k=2: 14→2 with a 12-dimensional linear kernel. | PSD plus exactly vanishing complex cross-cell sums for one fixed supplied partition; [RI-08a](../validation/t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md). |
| Chosen context cones `K̂_P`, `K̂_Q` | Each is isomorphic to `R_+^4`, with a three-dimensional normalized simplex. Mass is the sum of its four coordinates. | Explicit selected generators, preparations and apparatus maps; [RI-05/06](../validation/t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md). This is a chosen classical model. |
| Local control-selected cone `C` | `D(A,c)=[[A,cZ],[conj(c)Z,ZAZ]]`, `A≥abs(c)I`, `Z=diag(1,−1)`. Span 6. Faithful `m(D)=2Tr(A)=Tr(D)`. | Supplied H/quarter-phase/Z controls, all-word mass/recordability viability and label-swap calibration; [RI-08b](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md). |
| Local section/subcone `C0` | `D(A,0)`, `A≥0`. Span 4, normalized dimension 3. `Φ(D)=2A^T` is a positive isomorphism onto PSD2, with inverse `J2(ρ)=D(ρ^T/2,0)`. | It is the range of the chosen section, a subcone containing every RI-08c ideal-branch output, and the local survivor of RI-08d's additional nonzero-polarization joint interface. Each ideal branch reaches only its single Pauli ray. Those are different reasons to use C0. |
| Fixed RI-08d surviving joint image `K_t` | Raw 16-label representation; quotient image `conj(U)(ρ⊗ρ_t)U^T`, where `ρ_t=(I+tZ)/2`. Real span 4 and normalized affine dimension 3. For `abs(t)=1`, joint density rank is at most 2. | One fixed supplied independent reference and shared coupler, restricted to local `C0`; [RI-08d](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md). It is not the full 16-dimensional Hermitian span of a two-qubit state cone. |
| Minimal cut-closed completion `L_t` | Four independent PSD2 blocks in the same 16-label native representation; real span 16. Mass `Σ_ab Tr(E_ab ρ_ab)`, with `E_ab=(I+(-1)^b tZ)/4`, differs from ordinary raw trace `τ=Σ_ab Tr(ρ_ab)/4`. | Smallest convex cone containing K_t and closed under four literal cuts; [RI-08g](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md). This changes the declared return type. It does not establish physical availability of arbitrary independent blocks. |

`C0` is a subcone and positive section image, **not a face of C**: the average
of `D(A,c)` and `D(A,−c)` can lie in C0 while both summands lie outside it.
The individual perfectly repeatable Pauli output rays are exposed faces;
that fact does not make their whole C0 span a face.

Likewise, dimension four does not identify a qubit. The chosen classical
`R_+^4` cones have simplex bases; PSD2 has a Bloch-ball base. Different
cones, effects and transformations can inhabit spaces of the same dimension.

The positive zero-mass face of `K_P` has span dimension `(n−k)²`, which is
4 in the four-event/two-cell example. It does not exhaust the 12-dimensional
linear quotient kernel: complex cross terms matter. By contrast, mass is
faithful on C and C0, so their only positive zero-mass element is zero.
An invisible `c` direction is not by itself a positive zero-mass state.
Earlier chosen-model coordinates called “dark” to a particular attempt can
have positive mass. These three uses of “dark” must not be conflated.

## 3. What each theorem actually adds

| Accepted result | Load-bearing premises | Consequence and unresolved extension |
|---|---|---|
| [Strict finite derivation](../validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md) and [record-context domain](../validation/t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md) | Finite complex Hermitian strongly positive kernels; supplied exact recordable partitions and stated conditional operations. | Valid block weights and conditional histories. A unique physical update law, complex-field selection, arbitrary partitions and QM reconstruction do not follow. |
| [Hypothesis countermodels](../validation/t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md) | Explicit weaker source fragment and each countermodel's catalogue. | Strong reconstruction axioms do not follow from that fragment. The [chosen-law completion](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md) supplies a stronger operational package; it does not discharge it. |
| [RI-05/06 lawful transitions and future tests](../validation/t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md) | Finitely many typed finite-dimensional spaces and a fixed finite branch/terminal-effect catalogue. The example separately supplies two simplicial cones and positive complete maps. | Backward effect closure decides equivalence for all finite words in that catalogue. Read–switch–read has rank 4 in each example mode: no nontrivial residual compression remains. Informative selected-cone switches need not extend positively to full `K_P`. |
| [RI-07 first commitment](../validation/t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md) | Closed pointed generating finite-dimensional cones; faithful input **and committing-output** masses; one fixed complete stationary experiment or finite internal controller at a fixed record prefix; finitely many full committing labels. | `H_r=Σ_n B_r S^n` converges in operator norm and is the least positive solution; never-commit probability is separate. Silent powers need not converge. A lawful faithful quotient carries the limit if every required map/effect factors. |
| [RI-08a maximal-domain obstruction](../validation/t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md) | Bounded effects and positive mass-nonincreasing maps on the **whole** maximal `K_P` span/cone, with fixed availability. | Effects factor through cell weights; maps induce substochastic quotient maps. Equality of the full raw map to a measure/prepare formula is not claimed. Exact operational equivalence needs available cell readout; all classical preparations/transitions are extra. |
| [RI-08b control-selected qubit quotient](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md) | Stated control/calibration premises and control-word plus terminal-read catalogue. | Maximal viable C and exact `A`-equivalence for that catalogue. Additional effects can see `c`. The section J2 is mathematical; arbitrary preparation/reset availability does not follow. Raw cuts are terminal. |
| [RI-08c ideal reusable instrument](../validation/t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md) | Full real-linear positive C→C branch, exact rank-one Pauli effect and perfect repeatability; instrument availability is supplied. | The exposed repeat face forces `B_Q(d)=e_Q(d)J2(Q)` on the full six-dimensional span, including removal of output c. Complementary branches are complete. Finite known-history serial/feedback protocols close lawfully. |
| [RI-08d ancillary compatibility](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md) | Independent normalized polarized reference `t≠0`, native tensor composition, exact index permutation/untwist, one specified shared coupler and four-cell exact readout. | Cross forms `±tc` select exactly C0 at that direct interface. PSD and total mass alone do not certify joint recordability. Product controls and maximally mixed references can be blind; arbitrary shared-unitary availability is not derived. |
| [RI-08e imperfect repeatability](../validation/t8-q-repeatability-robustness-2026-09-13/ROBUSTNESS.md) | Explicit domain C0 or separately C; real-linearity on the actual span and positivity on the whole cone, exact effects, same-domain range, available branches, assumed uniform relative defect `ε≤1/2`. | On C0, calibration alone classifies `B̃_Q=e_Q h_Q`, with normalized h_Q; defect restricts it to `e_Q(h_Q)≥1−ε`. On broader C this classification can fail through input-c dependence. Sharp one-step and finite-protocol bounds hold under the declared common-history contract. |
| [RI-08f joint repeatability](../validation/t8-q-joint-repeatability-2026-09-13/JOINT_REPEATABILITY.md) | Fixed K_t reference/coupler image; positive full-span linear branches with exact first effects and the same return range. Algebraic return-operation availability is added explicitly. | Full-outcome repeatability has a strictly positive sharp defect; a coarse subsequent b question has a different optimum while full records remain. Relative-optimal branches are unique aligned-ray resets for nonzero t; t=0 and input-mass minimax have explicit non-reset counterexamples. |
| [RI-08g minimal cut-closed completion](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md) | Fixed supplied reference/coupler frame and explicit enlargement to the minimal convex cut-closed return cone L_t; separate fixed cut/read/stop catalogue. | Four independent positive blocks give span 16 and complete repeatable literal cuts. Interior mass is faithful; endpoint nonfaithfulness leaves positive dark payload. Whole-cone mass-dominated effects see internal blocks in the interior but collapse to weights at endpoints. Cut-only outcome laws use only the four weights throughout. |
| [RI-08h reversible generators](../validation/t8-q-reversible-generator-2026-09-13/REVERSIBLE_GENERATOR.md) | Fixed interior L_t and an additional all-real strongly continuous group of real-linear cone automorphisms, positive with positive inverses and preserving mass. | Each block is invariant and admits a filtered Hamiltonian generator, unique modulo scalar. All four weights are fixed; cut-only outcomes cannot identify the twelve generator parameters. The finite-policy comparison also requires identical initial pending/nominal command metadata. No physical time, Hamiltonian selection or native dynamics is derived. |
| [RI-08i terminal-read observability](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md) | Fixed known interior L_t, the supplied common-X command catalogue, and one additionally available exactly calibrated terminal internal read. Compare common finite policies at identical context, committed prefix, pending word and nominal metadata, without a raw-state observation oracle. | Mass-retaining homogeneous linear predictive ranks are 8/12/16 for X/transverse/tilted reads. Three resolved tilted-read settings uniquely reconstruct the full native state from compatible exact full-outcome tables, without division by cell mass. The result supplies neither a postmeasurement update nor empirical preparation/calibration, finite-sample accuracy or unknown-generator identification. |
| [RI-08j observation stability](../validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md) | The fixed normalized interior cone and known three-setting calibrated terminal catalogue; compare full outcome laws. Deterministic table-error budgets are explicitly supplied, with any typed candidate retaining matched context, full prefix and pending word. | Sharp filtered-distance constants quantify observability; raw recovery has unavoidable singular polarization dependence. A verified supplied candidate proves nonempty budget feasibility and a diameter bound, while candidate failure remains inconclusive. Raw audits must have no metadata; they cannot claim a verified history. No sampling confidence, fitting, preparation availability or empirical advantage follows. |

The general RI-06 closure can stabilize after at most the sum of the typed
space dimensions in independent effect directions; rational data permits
exact construction. This does not add arbitrary new history-dependent maps
or an infinite catalogue. A finite adaptive policy choosing among already
declared maps stays inside the theorem.

The RI-07 silent operator sums mutually exclusive outcomes of one supplied
experiment. It is not a sum of incompatible actions the controller could
choose. Its observation interface forgets silent paths. If actual control
words of unbounded length must be retained in full committing labels, as in
the later word-carrying records, the finite-full-label premise may fail.
One must reformulate and prove that extension, not erase retained words to
make the existing theorem apply. Never commitment does not produce a terminal
residual or a new committed record.

## 4. Lawful and unlawful composition arrows

| Proposed arrow | Assessment | Required record/domain treatment |
|---|---|---|
| RI-08b controls on C0 | Lawful algebraic restriction of the proved controls. | `D(A,0)→D(UAU†,0)` and quotient `ρ→conj(U)ρU^T`. Keep the actual word, frame and controller; arbitrary U availability remains extra. |
| RI-08c ideal branches restricted to C0 | Lawful restriction of an already proved full-C result. | Preserve exact calibration/completeness and the original branch labels. A proof only on the four-dimensional restriction would not establish full-C uniqueness. |
| Local control/ideal-record protocols followed by RI-08d | Mathematically compatible after a C0 source or a reusable commitment that puts every relevant leaf in C0. RI-15 implements the conditional normalized-leaf interface. | Preserve each earlier leaf probability separately, source records and origin tags; append an independently supplied reference and one joint terminal cut. The adapter retains the complete original local snapshot but does not infer missing prior selection weights. |
| Raw RI-08b terminal cut fed back to a local reusable instrument | Unlawful under the present types. | Nonzero literal cuts leave C, including cuts of C0 inputs. A proposed decoder/reset would be an additional operation requiring its own domain/range proof. |
| Raw RI-08d joint terminal cut treated as a state in the same joint image | RI-08f proves that every nonzero literal cut lies outside K_t. | One surviving block cannot equal an image with four identical blocks. Its exact source cut, total-entry weight and full 16-label payload matter. A nonzero zero-weight cut cannot be normalized or committed. |
| Explicitly embed K_t into L_t, then reuse literal cuts | RI-08g proves algebraic closure, completeness and exact full-outcome repetition on the changed return cone. | Supply the new domain tag and availability premise; retain full raw payload, frame, reference and records. This does not retag an old K_t terminal object or make a nonzero zero-weight cut selectable. |
| Replace an arbitrary C input by `J2Φ(d)` before the ancillary test | Changes the test's source and can conceal the very obstruction being tested. | Nonzero-c sources can fail joint recordability while their C0 replacements pass. Declare a lawful preceding instrument or an actual C0 restriction instead. |
| Apply RI-07 to later terminal outputs because local mass is faithful | Insufficient. | Faithfulness is required on committing-output cones too. Nonfaithful raw output sums may diverge even when their faithful quotient converges. |
| Add RI-08c ideal protocols to the earlier local A-only catalogue | Preserves A-sufficiency for that enlarged finite catalogue. | Controls are A-only and the first ideal branch factors through Φ and removes c; retain all histories. This is not universal c-equivalence. |
| Add arbitrary imperfect C instruments to that catalogue | False in general. | RI-08e gives equal-Φ input states with later X probabilities 9/10 versus 1/10. If C0 is imposed at the source, those nonzero-c inputs are unavailable. |

The third row admits a useful **coordinator composition corollary**. RI-15
implements its conditional local-to-joint leaf interface; full tree and
earlier-weight orchestration remain separate. Let `{T_l}` be a finite complete local tree
whose positive leaves lie in C0, and let R_t be a fixed independent normalized
reference. A sufficient condition is an initial C0 state with range-preserving
operations, or at least one ideal reusable commitment on every nonzero leaf
followed by such operations. For the accepted joint interface define

`K_(l,α)(d) = E_α U_raw (T_l(d) ⊗ R_t) U_raw† E_α`.

Each map is positive and real-linear; joint recordability gives
`Σ_α m16(K_(l,α)(d)) = m(T_l(d))`, and completeness gives
`Σ_(l,α) m16(K_(l,α)(d)) = m(d)`.
Normalize only a strictly positive selected weight. If reference preparation
is itself selected, include that selection's probability and record; do not
silently replace it with an independently available normalized resource.
Local faithful zero branches are full zero. Joint zero-weight terminal cuts
need not be full zero, and still cannot be selected.

The accepted standalone bundles use distinct scalar, state and record classes.
The [RI-15 adapter](../validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md)
binds exactly the RI-08c and RI-08d source versions and retains full residuals,
frame, controller, actual pending word, complete committed prefix, precursors,
origin tags, reference preparation and joint permutation/coupler identity.
An immutable wrapper preserves fields absent from the older target class.
This is one reviewed interoperability contract, not a general composite SDK.
Constructor acceptance checks finite grammar and cone membership, not global
preparation reachability or empirical independence.

RI-08d's restriction is relative to a particular **direct** joint interface.
A previously allowed local C state can undergo a supplied RI-08c commitment
into C0 and then enter that interface. This does not retroactively outlaw
the earlier source. Requiring the same ancillary capability at every earlier
prefix is a further global availability premise.

## 5. What robust local reuse does and does not buy

RI-08e compares a calibrated approximate branch with the ideal pure-ray
branch at the same input weight `p=e_Q(d)`. On either declared cone,

`||B̃_Q(d) − p J2(Q)||_1 ≤ 2p√ε`.

This is the full raw Hermitian trace norm, not half trace distance. On C,
`|c_out|≤εp/2` is separately sharp; C0 range already enforces c_out=0.
The two positive-error sharpness bounds cannot both be saturated. The exact
raw/quotient norm equality used here is specific to the matched-mass
pure-ray comparison; Φ does not preserve all raw distances.

For at most N committed tests in the declared Clifford/Pauli catalogue, with
the same full normalized initial state and the same known-history policy,
the sum of raw leaf differences is bounded by
`min(2,2N√ε)`. Full-record total variation is bounded by
`min(1,(N−1)√ε)` for N≥1, with both errors zero for N=0. The sharper
Clifford/Pauli bound is `1−(1−√(ε(1−ε)))^(N−1)`; the two-record value is
sharp, not a claim of an optimal longer-horizon rate. These comparisons
include shared record-dependent early stopping and absent branches as
zero-weight leaves in the union of full record supports. For a common
unnormalized input, the raw bound scales by its mass; total variation here
compares normalized probability laws.

Exact first effects explain the N−1 record bound: an update cannot change
the probability of its own just-generated outcome. Approximate positive
prefixes and ideal signed-contractive suffixes justify the hybrid argument;
approximate complete positivity, signed contraction and quotient descent are
not assumed. Keep known changed nominal setting identifiers distinct.
Analytical ε/target parameters for models of the same experiment do not by
themselves create extra physical outcome labels.

No finite witness establishes an experimental uniform ε over the whole cone.
No ancillary diamond-norm guarantee, infinite stopping bound, complete
instrument classification on C, or automatic joint-image reuse follows.
The rational-spectrum norm oracle refuses irrational square roots rather
than rounding them; the written proof supplies the universal norm argument.

## 6. Preparation, composite and reconstruction gaps

From the specifically supplied `J2(I/2)` preparation and ideal Pauli/Clifford
protocols, RI-08c reaches seven fine-history states: the center and six Pauli
states. Explicit classical mixing gives an octahedron of record-blind
residual marginals. It does not supply every Bloch-ball preparation. If a
controller remembers the selector, retain its joint ensemble and history;
the averaged residual alone cannot replace that controller's information.

The current joint result supplies one reference and one coupler, not an
arbitrary ancillary theory, full PSD4 preparation cone, all quantum effects
or instruments, local tomography, purification, Hamiltonian law or geometry.
Complex Hermitian kernels and a quarter-phase control were supplied before
the qubit quotient appeared; the construction does not select the complex
field from field-neutral premises. The maximal-domain obstruction motivates
a restricted domain but does not uniquely choose C or its added controls.

**RI-08f is now accepted as a conditional result.** On fixed K_t the full-cell
effects pull back to `E_ab=(I+(−1)^b tZ)/4`: a is fair, and the maximum
normalized full-outcome probability is `(1+|t|)/4≤1/2`. A general first-effect
e / next-question g lemma gives relative defect `1−β` and original-input-mass
minimax defect `α(1−β)`, where α and β are the attained normalized maxima of
e and g. The two effects need not be the same.

For the fine first branch and same full outcome the relative optimum is
`(3−|t|)/4`, and the input-mass optimum is `(1+|t|)(3−|t|)/16`.
For a fine first branch and a next-b question they are `(1−|t|)/2` and
`(1−t²)/8`. Analytically summing the first branches over a leaves the relative
optimum unchanged but doubles the input-mass optimum to `(1−t²)/4`.
These sums combine separately labeled histories; both actual fine records
remain intact. They are not coarse commitments or deterministic memory reads.

Relative optimality forces outputs into the maximizing face. For nonzero t
that face is one aligned Z ray, fixing each branch uniquely by calibration.
At t=0 all calibrated positive branches are optimal; `N→N/4` is a non-reset
example. Interior weighted dephasing separately proves that input-mass
minimax optimality does not force relative-optimal reset uniqueness.
The supplied reset fixture establishes positive complete algebraic attainment,
with physical availability and reference-reset implementation still extra.

Full-outcome repeatability is therefore impossible in this return image,
although b can repeat perfectly at full polarization. A nonzero literal cut
is never a valid return state. Exact inverse/reconstruction checks retain
every native entry and work at singular reference endpoints. At t=0 K_t
still denotes the chosen c=0 section image; RI-08d does not exclude nonzero c
with an unpolarized reference. Changing the typed return cone, available
questions or preparation resources requires a new explicit premise set.

**RI-08g is accepted.** Four independent blocks `M_t(ρ_ab)` define L_t in the
accepted untwisted frame. Cutting a K_t image isolates each positive block;
finite positive sums construct all of L_t. Conversely this cone contains K_t
and is cut-closed, proving minimality without an additional topological
completion. Full-block inverse and exact native reconstruction are required;
PSD, total mass and four weights alone do not establish image membership.

Literal cuts satisfy `Σ C_ab=I` and `C_cd C_ab=δ_(ab,cd) C_ab` on the entire
span. Every strictly positive selected weight therefore gives a normalized
state with exact repeated full outcome. At the endpoints, raw completeness
still includes nonzero zero-weight cuts. Summing only probability-weighted
normalized positive branches can omit a nonzero dark remainder. These cuts
remain inspectable but cannot be normalized or committed.

On the whole cone, `0≤e≤m` is equivalent to a unique block representation
`e=Σ Tr(F_ab ρ_ab)` with `0≤F_ab≤E_ab`. At `abs(t)<1` these effects span
all 16 directions; their physical availability is an additional premise.
At `abs(t)=1`, each E has rank one, so every F is a scalar multiple of E:
the common effect kernel has dimension 12, the positive zero-mass face has
span dimension 4, and the linear kernel of mass has dimension 15. They are
different objects. Ordinary finite-dimensional norm boundedness is not the
same as domination by mass; raw trace can see positive dark payload.

For a fixed interior t, `(1−abs(t))τ≤m≤(1+abs(t))τ` makes mass faithful and
the normalized base compact. A mass-one opposite-ray block attains
`τ=1/(1−abs(t))`; the bound is not uniform as polarization approaches an
endpoint. There, adding arbitrary positive dark payload preserves mass and
destroys compactness. This is a singular-limit result, not a new silent
process or a claim that the literal cuts themselves diverge.

With only the declared full-cell read, literal cuts and finite
history-dependent stopping, two normalized sources at the same full prefix
and context have equal future outcome laws exactly when their four weights
agree. Unnormalized sources instead give outcome-weight measures, including
total mass. The raw `quotient(d,t)` helper is not a context-aware state
equivalence predicate. The mathematical positive weight section is not an
available reset. RI-07 applies in the interior only when its separate
stationary/controller, finite-full-label, completeness and faithful-output
premises also hold. At endpoints it can apply to a suitable descended
faithful quotient only after every required map/effect and other premise is
established; that does not imply a raw limit.

**RI-08h is accepted and registered.** Its additional strongly continuous
real-parameter group of positive invertible mass-preserving maps on fixed
interior L_t preserves each of the four extreme-point components and hence
each block and its mass. Filtering by `σ=E^(1/2)ρE^(1/2)` gives a trace-one
Bloch ball. Its affine automorphisms fix the center and act orthogonally;
continuity and the group law yield a constant skew generator by an elementary
integral argument, without assuming differentiability.

Thus every block has
`ρ_s=E^(-1/2) exp(-isH) E^(1/2) ρ E^(1/2) exp(isH) E^(-1/2)`.
Equivalently the generator is `Gρ+ρG†`, with `G†E+EG=0`.
Conversely each Hermitian H gives such a group. Scalar H parts act trivially,
leaving twelve nontrivial mathematical parameters, not twelve parameters
identified by the existing observations. These congruences need not be
ordinary raw unitaries or conserve raw trace.

Every flow fixes the four weights and commutes with the literal cuts. Equal
future laws require matched context, full committed prefix, initial pending
metadata and a common retained nominal-command policy. Distinct known words
remain different records even for equal group elements; a policy inspecting
unequal pending words can choose different cut/stop actions. The cut-only
catalogue cannot identify internal generators under the matched contract.

Endpoint bright-plus-`exp(s)`-dark dilation preserves singular mass while raw
trace grows without bound. Forward dephasing has a nonpositive inverse.
Static transpose is an individual orientation-reversing automorphism, but
dropping continuity alone from an R-group still cannot admit it: divisibility
excludes orientation signs and finite cell permutations. A choice-dependent
discontinuous additive reparameterization supplies the genuine continuity
counterexample; it is not executable evidence. The exact primary fixture is
only t=3/5 with six named common-X group elements. General generators,
other unitaries and endpoint maps remain diagnostics. No physical time,
Hamiltonian selection, energy units or native DET dynamics follows.

**RI-08i's conditional proof and source contract are accepted.** Under the
known common-X commands, the backward span for a terminal axis n has
per-cell rank `1+[n_x≠0]+2[(n_y,n_z)≠(0,0)]`. X, transverse and tilted
read catalogues therefore have total homogeneous linear dimensions 8, 12
and 16, with normalized affine dimensions 7, 11 and 15. Positive sections
attain the reduced quotient cones. They are algebraic right inverses, not
available resets or preparations. Minimality concerns mass-retaining linear
summaries on the actual full span, not nonlinear encodings or an available
preparation subset.

The tilted axis `(3/5,0,4/5)` and separately resolved empty/A/AA words
have determinant `−73728/78125`. Full outcome differences and shared cell
sums recover each `(q,x,y,z)` and all entries of the native kernel. The
exact table criterion requires shared q, `Σq=1`, nonnegative q and
`q²≥x²+y²+z²`. Zero-mass cells reconstruct as zero without division.
Three resolved binary settings are minimal in this catalogue; an observed
random selector counts its distinct settings. Malformed or incompatible
tables are refused without clipping or fitting. Exact probability tables
are not observed frequencies or proof of repeated preparation availability.

The all-finite policy equivalence includes commands, literal cuts, stopping
and a single terminal read, with the same full initial context, committed
prefix, pending word and nominal metadata. Policies cannot inspect retained
raw audit payload. A read directly produces the full `(a,b,sign)` record,
with no fictitious preceding cell commitment. Its typed result retains the
exact pre-read source, calibrated effect and strictly positive conditional
snapshot probability, specifies no postmeasurement residual, and refuses
continuation. Earlier preparation-selection weights remain unspecified.
An effect does not determine a reusable instrument.

The universal statement covers fixed known interior t; the executable
primary fixture is only t=3/5. It does not extend faithful filtering through
singular endpoints. Known-command state observability does not identify an
unknown generator, physical time or a DET-selected observation law. Final
registration/replay evidence and source identities belong to the progress
record, separately from these mathematical conclusions.

**RI-08j's theorem and corrected candidate contract are accepted.** For two
normalized compatible sources, let epsilon_k be full-law total variation at
each resolved empty/A/AA setting. Write d_F for half the sum of filtered
block trace norms, d_N for half the native-kernel trace norm, and b_k for
the Euclidean norms of the inverse backward-axis matrix columns. Then

`max epsilon_k ≤ d_F ≤ Σ b_k epsilon_k`,

with each weighted coefficient and their common-error sum sharp on the
full mathematical four-cell domain. Three separate small positive-center
perturbations attain the upper coefficients; moving center mass attains the
lower coefficient one. At the fixed tilt,
`b_0=b_2=125√41/768`, `b_1=5√6409/384`, and their sum is approximately
3.126749. This decimal is explanatory; the implementation uses exact
square-proved rational upper enclosures. Mathematical sharpness does not
supply physical preparation procedures.

For a unit read axis with `a=|n_x|` and `b=||n_perp||`, the exact general
column-norm formula gives `aC→1` near a=0 and `bC→25/12` near b=0.
Full rank can coexist with arbitrarily poor conditioning; at the blind
axes information is absent. The native norm satisfies

`d_F/(1+|t|) ≤ d_N ≤ d_F/(1-|t|)`.

The endpoint factor is unavoidable even with bounded raw sources: moving a
dark projector between two retained cells keeps d_N=1/4 while every full-law
TV tends to zero as `(1-t)/4`. No joint sharpness of the composed observation/
native coefficient is assumed. Native kernels need not have trace one, so
d_N is not itself a probability distance.

Given normalized full tables y_k and deterministic budgets eta_k, an exact
positive supplied candidate inside every TV budget witnesses nonempty
feasibility. Any two feasible sources have filtered distance at most
`2Σ b_k eta_k`, with the corresponding native factor above. The executable
returns safe rational upper bounds and preserves the candidate, data and
actual errors. A failed candidate is inconclusive about existence of another;
it supplies no infeasibility certificate, fitted state or table repair.
Exact reconstruction may refuse inconsistent cell masses even when a
positive candidate meets nonzero budgets.

A raw-matrix audit must use `metadata=None`; every entry point rejects
attached history metadata it cannot bind. A caller requiring exact known
context, prefix and pending-word matching must supply the typed State.
Neither audit path prepares a state, performs a read, creates a commitment
or continues from a terminal result. Full native payload and zero cells
remain intact. Rare-cell opposite states have vanishing full-law error but
conditional distance one, so conditional accuracy needs a positive weight
floor. A joint change of unknown read frame and source can preserve all
setting laws: calibration and state are not jointly identified. Deterministic
budgets do not establish confidence levels, repeated preparation or measured
benefit. The linear-target corollary transfers event-probability error; a
binary expectation difference can instead incur twice the TV budget.

## 7. Application and project integration route

The accepted observation-stability capstone closes the present round of
finite-cone refinement. The accepted
[FINITE_RECORD_OBSERVABILITY.md](../research/FINITE_RECORD_OBSERVABILITY.md) synthesis consolidates a single
conditional observability/stability argument; it does not settle operational
premise selection or measured
application obligations below. Its finite theorem needs known A/A² command
matrices and the calibrated terminal read, not the stronger all-real
continuity premise used in the separate generator classification.
The full combined proof and its cross-bundle arrows passed two independent
coordinator reviews. Its frozen open-bridge discussion predates the separately
accepted RI-16 extension below. Publication state for the
research repairs, exact identifiability, comparator and claims package is
recorded separately in the [publication backlog](PUBLICATION_BACKLOG.md).

The useful QR/application transfer at present is a disciplined answerability
contract: declare the state/model, question, allowed observations, retained
record and refusal condition. It is not a quantum algorithm or an advantage
claim for ordinary calibration.

The [exact identifiability contract](IDENTIFIABILITY_CONTRACT.md) distinguishes
`λ^T H=q` from an ambiguity witness `Hδ=0, qδ=1` for known rational mean
coefficients and unrestricted real parameters. Candidate-row separation of
one ambiguous pair is weaker than full target identification. Priors,
measurement noise, conditioning, nonlinear nuisance parameters and costs
require additional analysis; rational input exactness is not noisy certainty.

The [synthetic comparator](COMPARATOR_DEMO.md) connects observed rows to a
named model's conditional Gaussian posterior, distinct mean/predictive
variances and byte-verified public RET replay. Repeating one reference reduces
some posterior uncertainty without changing exact design rank; adding a
distinct reference changes rank. Held-out records are not assimilated into
the posterior or observed design. These facts do not identify a noisy true
parameter exactly or replace open model uncertainty with one selected model.

The [application work plan](APPLICATION_WORK_PLAN.md) retains the remaining
instrument/data, target/tolerance, objective, conventional baseline and
held-out evaluation obligations. The dataset question is open. RET source
ownership and G2 bank/freeze/custody work must be coordinated separately;
this ledger authorizes no bank change or release claim.

**RI-14 is accepted.** The separate
`det8.claims.research_activity_document()` endpoint now exposes versioned,
fully detached scoped authorization and eighteen explicitly accepted suite
references through RI-08j. The generated [claim registry](../CLAIM_REGISTRY.md)
shows the same metadata. Existing `claim_summary()` and `registry_document()`
contents, broad evidence/development statuses, priorities and module support
boundaries are unchanged. The endpoint performs no repository lookup,
research import or source verification; the separate research runner verifies
the named statement/source pins. Future entries do not become accepted by
directory discovery or automatic inclusion. New accepted references require
an explicit coordinator update and generated-summary consistency checks.

**RI-15 is accepted as a bounded research interface.** Its scope is
the exact RI-08c local snapshot to RI-08d product/coupled/terminal stages.
An immutable wrapper retains the original local object, including its pending
controls, alongside deterministic exact scalar/record conversion and explicit
reference provenance. Pending controls have already acted on the source
residual; they must not be reapplied or invented as committed records.
Source snapshots do not include past selection weights, so reported weights
are conditional on the supplied normalized local/reference snapshots.
The broader-C obstruction survives conversion; no quotient/section
replacement is made. A separate fixed-alias launcher binds both accepted
sources without changing the existing registered runner. Two source audits,
51 independent probes per mode and root's 36 regression cases passed,
including the pinned 20-witness normal and optimized executions. A default
inventory check does not execute the adapter; `--run` is explicit. The full
contract requires the wrapper, not an extracted legacy object. This interface
confers no new operation availability or public-core support.

Further substantial proofs should close a named arrow in this ledger:
an explicit internal observation interface, earlier-weight/full-protocol
composition, a declared larger preparation/instrument class, or an extended
first-commit observation interface. Each needs its own explicit premise set,
countermodels, source-stable witnesses and independent acceptance. A union of
accepted conditional results is not itself a reconstruction theorem.

## 8. Accepted retained-word first commitment — RI-16

The [RI-16 theorem](../validation/t8-q-retained-word-first-commit-2026-09-14/RETAINED_WORD_FIRST_COMMIT.md)
closes the named finite-full-label gap for one complete stationary finite
controller on finite-dimensional faithful input cones. Its complete output
is an l1 sum indexed by actual words and full committing labels/types, with
faithful base norms. Positive output norm equals total retained mass, so
first-commit truncations converge in operator norm and their exact error is
the dual base norm of survival minus never mass. Silent residuals need not
converge; never mass is neither a null record nor a terminal residual.

Chronological prefix shifts are essential in the fixed-point equation.
Without empty steps its word coefficients give uniqueness; hidden empty
loops can admit spurious dark-added positive solutions, so leastness selects
the actual law. Uniformly bounded word-dependent linear continuations
commute with the limit while preserving labels. Hidden path selectors and
discarded waiting counts do not become available observations. Nonuniform
norms, unbounded continuations, word erasure, infinite-dimensional input and
uniform-model-rate claims have explicit counterexamples.

The accepted terminal read contributes only its supplied scalar positive
effects, with full word/cell/sign labels and complete policy weights. A
probability-weighted pre-read audit source is generally nonlinear; it cannot
manufacture a postread residual. Existing literal cuts retain their declared
positive residual types. This result supplies neither physical availability
nor orchestration of earlier local/reference-selection weights. The separate
RI-18 result below supplies one bounded finite orchestration under explicit
preparation and availability premises.
Its fixed-prefix theorem does not cover arbitrary unbounded-history policies
or a changing model/controller limit.

Two independent coordinator audits accepted the theorem and exact supplement,
including separate exact theorem and native-interface probes. Root passed all
27 new witnesses in both modes and 43 registry regressions from an isolated
publication candidate. The nineteen-suite cumulative inventory is 411
witnesses; the preceding 384 source-bound results were not rerun in this cycle.
The accepted RI-15 adapter remains a separate inventory and interface.


## 9. Accepted bounded finite composition — RI-18

The [RI-18 theorem and adapter](../validation/t8-q-finite-protocol-composition-2026-09-14/PROTOCOL_COMPOSITION.md)
close the earlier-weight and preterminal type/context arrow for one fixed
finite route. Executable inputs are normalized full-C local sources with the
fixed interface, empty starting record/pending prefixes and root weight one.
A complete ready/unavailable reference law, independence, preparation IDs,
branch availability, polarized reference, adopted L_t return and calibrated
terminal read are explicit supplied premises. None is inferred from source
provenance or from positivity. The written theorem also states the homogeneous
incoming-mass extension; the executable refuses wider initial histories.

The actual Y branch sends the lawful nonzero-c input into C0. After actual
local Z, reference selection and the RI-15 coupling, the new conversion
preserves every native entry of the coupled preterminal source and its full
original context. It neither reuses a terminal nor prepares or couples again.
The local pending Z stays anchored while the distinct joint word is committed.
The finite command choice sees only the retained cut pair; scalar terminal
outputs and unavailable stops retain full labels and prior audit anchors.
Every conditional weight occurs once, zero weights produce no selected state
or record, and planned read-setting IDs remain on all 66 law coordinates.
Retaining the planned setting on a stop does not perform a read.

Positive linear full-law composition preserves total incoming mass. For the
primary normalized fixture sixteen read leaves total 2/3, two stops weigh
4/15 and 1/15, and forty-eight read coordinates are zero. The complete scalar
law depends only on initial mass and Y expectation: rank two on the real
span, one affine parameter on normalized states, with exact normalized
TV=|delta y|/2 at fixed settings/reference law. Known original audit inputs
may differ even when observation laws coincide. They are not additional
observations or a way to recover discarded X/Z/c coordinates.

Independent full proof/source reviews and supplementary source probes passed.
The isolated pinned candidate passed 65 launcher regressions, including the
actual 31 new witnesses normally and under optimization. Its separate
[launcher](../../scripts/run_qr_finite_protocol.py) and
[guide](../RESEARCH_CHECKS.md#separate-ri-18-finite-protocol-launcher) leave
the 411-witness registry and all 60 predecessor/design sources unchanged.
This result is bounded finite composition, not a general process SDK,
approximate interface theorem, selected physical theory or measured benefit.


## 10. Accepted exact admission and approximate-law stability — RI-19

The [RI-19 conditional proof/design](QR_INTERFACE_ROBUSTNESS_PLAN.md)
classifies all real-linear positive C→C0 branches with a specified calibrated
rank-one effect p=e_Q(d): B̃_Q(D)=J2(pH+uK+vL). Hermitian H,K,L have
traces 1,0,0, and positivity is equivalent to the whole-circle condition
H+(cos θ K+sin θ L)/2≥0. The projected input cone is exactly p≥2|c|.
The note derives the exact uniform-repeatability condition, proves that
branchwise Φ descent holds precisely when K=L=0, and recovers the unique
ideal reset at zero defect. These are whole-domain arguments, not a sampled
preparation grid or an ancillary complete-positivity theorem.

Arbitrarily near-ideal positive full-C outputs can retain nonzero output c
and fail the exact polarized joint interface. Small defect or raw distance
is therefore insufficient for admission. The classified C→C0 range is an
additional premise. Conversely, C0 output need not erase input-c dependence.
Under the fixed positive-readiness suffix, the two branch payloads are
observed injectively and the initial scalar-law rank is exactly
2+rank{(K0,K1),(L0,L1)}. At readiness zero it is two. Initial X/Z remain
unobserved, so even the admitted rank-four family is not full tomography.

With matched complete scalar labels, exact first-effect calibration and the
same expressly input/outcome-independent reference law, normalized law error
is bounded by β sum_r p_r sqrt(ε_r), hence β sqrt(ε). Two same-Y inputs
obey β min(1,2sqrt(ε)). The proof contracts the C0 base/raw-trace norm
directly into the complete scalar law; it assumes no native L_t raw-trace
contraction. Zero branches, scalar stops and incoming-mass versions are
explicit. Different observed settings or instrument IDs cannot be erased to
invoke these bounds; unequal source/audit objects are not compared as equal.

The truthful approximate prefix and its forward-bound adapters are specified
but unimplemented. RI-15 checks a c.State snapshot and grammar; RI-18
additionally derives its actual ideal prefix. Neither supplies the new
approximate type or certifies a substituted output. Exact raw admission,
executed typed interchange and physical availability remain distinct.

Independent full theorem/API reviews passed. Root's native audit passed
193 exact assertions for the signed map, rank and positive-domain separators,
without a new executor or registered suite. The separate coordinator
[application corollary](APPLICATION_WORK_PLAN.md)
quantifies necessary inverse constants and deterministic worst-case target
error as βκ becomes small. It assumes a fixed known instrument and error
budget, not measured calibration or sampling confidence. The next substantial
choice is consolidation plus operational-premise selection or a measured
application contract, rather than another automatic operation-family extension.
