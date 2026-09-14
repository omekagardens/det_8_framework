# Explicit research check registry

The [registry](research/registry.json) binds eighteen named standalone Q witness
suites to their statement documents, premises, limitations and complete local
executable source sets. The [runner](../scripts/run_research_checks.py) verifies
those identities and executes only explicitly selected suites. It is separate
from core validation, the claim registry, frozen QR capture/replay bundles and
default CI. It does not discover or execute other research directories.

A successful run means that the registered **finite witness checks** passed
against the recorded source snapshots. It does not prove a universal theorem,
adopt a reconstruction premise, validate physical availability or establish
geometry, mass or gravity. The written arguments retain those obligations.
Test counts are descriptive execution metadata, not proof strength.

## Usage

Run from the repository root with Python 3.11 or later. The runner and the eighteen
registered suites need only the Python standard library.

```sh
.venv/bin/python -B scripts/run_research_checks.py --list
.venv/bin/python -B scripts/run_research_checks.py --check
.venv/bin/python -B scripts/run_research_checks.py --suite operation-domain --suite record-context
.venv/bin/python -B scripts/run_research_checks.py --all
.venv/bin/python -B scripts/run_research_checks.py --all --optimized
```

No arguments defaults to `--list`. Both `--list` and `--check` validate the entire
manifest, document/code hashes and static import closure without executing a
suite or starting a subprocess. `--suite` is repeatable; `--all` explicitly
selects the fixed registered list. An unknown or repeated selection is refused.
`--manifest` accepts a canonical repository-relative manifest path.

Output is one JSON document on stdout. The runner creates no report, source
freeze, cache or other evidence file. A caller may deliberately retain stdout
elsewhere; report persistence is an explicit caller choice. Exit status is 0 for a valid
inventory or fully successful selected run, 1 for failed/incomplete execution
or detected source drift, and 2 for invalid registration, selection or file
access. Normal command-line syntax errors follow argparse's stderr/exit-2
convention. Skips, expected failures and empty suites are **not** successful
witness verification. Each suite has a manifest timeout of at most 60 seconds.

## Registered scope and dependency audit

| ID | Statement document | Local executable source closure |
|---|---|---|
| `strict-derivation` | [DERIVATION.md](validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md) | `check.py` |
| `operation-domain` | [OPERATION_DOMAIN.md](validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md) | `check.py` |
| `hypothesis-countermodels` | [JUSTIFICATION.md](validation/t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md) | `check_witnesses.py` |
| `chosen-law` | [RECONSTRUCTION.md](validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md) | `check_law.py` |
| `coherent-readout` | [CANDIDATE.md](validation/t8-q-coherent-readout-2026-09-12/CANDIDATE.md) | `check.py`, `algebra.py`, `reference.py` |
| `record-context` | [CONTEXT_DOMAIN.md](validation/t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md) | `check.py` |
| `controlled-context` | [CONTROLLED_CONTEXT.md](validation/t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md) | `check.py`, `model.py` |
| `first-commit-quotient` | [FIRST_COMMIT_QUOTIENT.md](validation/t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md) | `check.py`, `model.py` |
| `maximal-record-domain` | [MAXIMAL_DOMAIN_QUOTIENT.md](validation/t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md) | `check.py`, `model.py` |
| `control-selected-qubit` | [CONTROL_SELECTED_QUBIT.md](validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md) | `check.py`, `model.py` |
| `repeatable-record-instrument` | [REPEATABLE_INSTRUMENT.md](validation/t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md) | `check.py`, `model.py` |
| `joint-recordability` | [JOINT_RECORDABILITY.md](validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md) | `check.py`, `model.py` |
| `repeatability-robustness` | [ROBUSTNESS.md](validation/t8-q-repeatability-robustness-2026-09-13/ROBUSTNESS.md) | `check.py`, `model.py` |
| `joint-repeatability` | [JOINT_REPEATABILITY.md](validation/t8-q-joint-repeatability-2026-09-13/JOINT_REPEATABILITY.md) | `check.py`, `model.py` |
| `cut-closed-completion` | [CUT_CLOSED_COMPLETION.md](validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md) | `check.py`, `model.py` |
| `reversible-generator` | [REVERSIBLE_GENERATOR.md](validation/t8-q-reversible-generator-2026-09-13/REVERSIBLE_GENERATOR.md) | `check.py`, `model.py` |
| `terminal-read-observability` | [TERMINAL_READ_OBSERVABILITY.md](validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md) | `check.py`, `model.py` |
| `observation-stability` | [OBSERVATION_STABILITY.md](validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md) | `check.py`, `model.py` |

Paths in the last column are relative to that row's validation directory. Five
suites have no local imports. Coherent readout imports both its algebra and
independent reference; registering its entrypoint alone would be incomplete.
Controlled context, first-commit quotient, maximal record-domain,
control-selected qubit, repeatable record instrument, joint recordability,
repeatability robustness, joint repeatability, cut-closed completion, reversible
generator, terminal-read observability and observation stability each import
their own local model. The only directly imported standard-library modules
across these thirty-two Python files are
`collections.abc`, `dataclasses`, `fractions`, `itertools`, `math`, `types` and
`unittest`.

The seventh registration follows the coordinator's independent review and the
[QR handoff](coordination/QR_HANDOFF.md). Its three source hashes match that
handoff; the original six registration objects and all their hashes are preserved.
This chosen classical cone model has predictive rank four in each mode, with no
nontrivial residual quotient under the full declared test family. Controlled
branch cylinders use a supplied observation interface; procedure boundaries
are not physical times or committed nulls. A fixed read–switch–read program
also distinguishes the coordinates using actual committed read outcomes.

The eighth registration follows independent review and coordinator acceptance
of the first-commit quotient handoff. Its note, model and check hashes match
the handoff; all seven earlier registration objects and hashes are preserved.
The convergence theorem assumes finite-dimensional closed pointed generating
input and output cones with strictly positive mass functionals, at one fixed
record prefix and supplied complete experiment or finite internal controller.
These faithful-cone hypotheses are sufficient, not necessary or quantum-selecting.
The result preserves full committed labels and residual maps, plus complementary
never-commit probability. It forgets silent counts, paths and controller visits;
never commit does not supply a terminal residual or record, and zero-mass
branches cannot be selected. A lawful quotient must preserve mass and every
allowed continuation and terminal effect, not merely eventual output totals.
The exact classical examples include a periodic hidden controller and a
nonfaithful divergence removed by a lawful quotient. They make no physical or
QM selection, global-history or uniform model-family claim. This registration
requires no new runner dependency or execution capability.

The ninth registration follows independent review and coordinator acceptance
of the maximal record-domain handoff. Its three hashes match the handoff, and
all eight prior registration objects and hashes are preserved. This theorem
uses the entire fixed-partition PSD exact-recordability cone and its actual
real Hermitian span. Effects must be bounded by total-entry mass on that whole
cone; transformations must be fixed, real-linear, positive and
mass-nonincreasing there. Availability cannot depend on hidden residual
inspection. Under these premises the catalogue is at most cell-weight
informative. Exact residual equivalence additionally requires cell readout;
all classical preparations and transitions require further availability.
Full committed labels, precursors, records and external types remain separate.
First-commit convergence holds on the faithful quotient under the earlier
finite-label, fixed-policy and observation conditions; original kernel sums
can diverge. A zero-probability branch may retain a nonzero dark kernel but
cannot be normalized or committed. The exact code supplies finite algebraic
witnesses, not a general map classifier or a history engine. No physical
classicality, QM selection, composite or global-history claim follows. The
new suite needs only `collections.abc`, `dataclasses`, `fractions` and `unittest`,
with no runner change.

The tenth registration follows independent review and coordinator acceptance
of the control-selected qubit handoff. Its note, model and check hashes match
the accepted source; all nine earlier registration objects and hashes are
preserved. Supplied H, quarter-phase P and Z controls, all-word mass and
recordability preservation, and readout-swap calibration select a maximal
viable subcone of the full four-label exact-recordability domain. Its raw
kernels retain complex cross-block payload c. The PSD2 quotient is justified
only for the declared control-word/terminal-read catalogue; other bounded
mathematical effects can distinguish c. A positive quantum section does not
assert that the raw cone equals its image or that all preparations are
physically available. The terminal cell cut retains its full raw residual,
actual setting word, outcome and precursor, but leaves the source control
domain. A nonzero zero-probability cut cannot be selected or normalized. No
reusable instrument, arbitrary effect availability, complex-field selection,
full QM, ancilla/composite or native growth result follows. The additional
control and calibration premises remain explicit. Its direct standard-library
imports are `collections.abc`, `dataclasses`, `fractions` and `unittest`;
registration requires no runner change.

The eleventh registration follows independent review and coordinator acceptance
of the repeatable record instrument handoff. Its three source hashes match the
accepted source; all ten earlier registration objects and hashes are preserved.
On the full six-dimensional control-selected source span, positivity into the
same cone, exact Pauli-effect calibration and perfect repeatability uniquely
force the exposed-ray branch. Complex input c remains admitted; c vanishes in
the output as a consequence, and every zero-effect branch is the whole zero
kernel. Reusable availability, same-source range and full-cone calibration are
additional premises. The earlier terminal cut remains separately typed and
does not gain a reset or source continuation. Finite serial controls and
feedback retain actual words, outcomes, frames, controllers and full precursors.
From the declared central preparation, fine-history-conditioned residuals are
exactly the center and six Pauli eigenstates. Explicit randomization gives the
stabilizer octahedron only as a record-blind marginal; selectors and component
histories remain in the joint ensemble. This supplies neither full preparation
richness nor field selection, ancillary/composite closure or a native growth
law. Its direct imports are `collections.abc`, `dataclasses`, `fractions`,
`types` and `unittest`; registration requires no runner change.

The twelfth registration follows independent review and coordinator acceptance
of the polarized-reference joint-recordability handoff. Its final note, model
and check hashes match the accepted source; all eleven earlier registration
objects and hashes are preserved. Independent raw tensor composition with a
known polarized section reference and a supplied shared CNOT-then-target-H lift
excludes nonzero complex c through exact joint cross-cell forms. The maximal
surviving **local** subcone at this fixed interface is c=0; it is not a globally
selected composite cone. All c values are admitted at input and initially
recordable. The offending cross forms cancel in total mass, so positivity and
normalization alone cannot authorize the coupled record context. Product
unitaries, an unpolarized reference and CNOT alone do not give this exclusion.
All sixteen labels, reference settings, origin-tagged histories and precursors
remain intact. Positive terminal outputs equal the full normalized source cut;
zero-weight nonzero cuts and invalid prospective contexts cannot be committed.
Independence, tensor composition, the shared lift and its availability remain
explicit premises. No physical access to c, general composite preparation or
ancillary closure, native entangler, field selection or growth law follows.
The direct imports are `collections.abc`, `dataclasses`, `fractions`, `itertools`
and `unittest`; registration requires no runner change.

The thirteenth registration follows independent review and coordinator
acceptance of the repeatability-robustness handoff. Its three hashes match
the accepted source; all twelve earlier registration objects are preserved.
On the four-dimensional composite-compatible C0 span, whole-cone positivity
and exact rank-one Pauli-effect calibration classify every branch as its
effect times a fixed normalized target. An assumed uniform repeatability
defect epsilon, between zero and one half, restricts the target to a cap;
finite witnesses do not infer this uniform premise or physical availability.
The broader local-only six-dimensional C cone is separately labeled: its
nonzero input c can affect later quotient predictions through an approximate
branch, and cannot be admitted under C0's composite premises.

Both declared domains satisfy the sharp raw norm bound `2 p sqrt(epsilon)`.
On the broader C domain, the separate output-coordinate bound
`|c_out| <= epsilon p/2` is sharp; C0 range already forces c=0. For the same full normalized initial
state, nominal settings and known-history controller, at most N recorded tests
give raw leaf-error at most `min(2,2 N sqrt(epsilon))` and full-record total
variation at most `min(1,(N-1) sqrt(epsilon))` for N>=1; both vanish at N=0.
Early stops retain their leaves. The proof uses approximate positive prefixes
and ideal contractive suffixes, without assuming approximate complete
positivity or quotient descent. The sharper Clifford/Pauli coupling bound is
not an optimality claim for general longer horizons. Undeclared c-sensitive
tests, changed record alphabets, ancillary diamond norms, infinite stopping
and physical promotion remain outside scope.

This registration narrowly adds `math` to the explicit standard-library
allowlist for the independent checker's exact `isqrt` calculations. The source
closure, snapshot execution and mutation guards remain unchanged. Regression
coverage verifies declared `math` imports and large-integer square roots in
normal and optimized children, and refuses a dotted `math.fake` import.

The fourteenth registration follows independent proof and implementation review
and coordinator acceptance of the joint-repeatability handoff. Its three pins
match the accepted bundle; all thirteen preceding registration objects remain
unchanged. The general lemma assumes faithful mass, nonzero bounded first and
next effects e and g with attained normalized maxima alpha and beta, and a
real-linear, positive same-cone branch with `m B = e`. Its sharp relative
defect is `1-beta`, whereas the worst defect per unit original input mass is
`alpha(1-beta)`. These are different objectives.

The application fixes the entire four-dimensional c=0 joint image K_t, one
independently supplied Z-oriented reference, the native sixteen-label
permutation/untwist and one fixed coupler. Whole-image positivity, exact
full-cell calibration and return to that same image are premises. Full-outcome
relative defect is at least `(3-abs(t))/4`; asking only whether the next b
agrees gives `(1-abs(t))/2`. The denominator remains the first branch's weight.
The corresponding original-input-mass optima are:

| First branch and next question | Sharp input-mass coefficient |
|---|---|
| One fine (a,b) branch, then the same full outcome | `(1+abs(t))(3-abs(t))/16` |
| One fine (a,b) branch, then the same b | `(1-t^2)/8` |
| Analytically summed first-b branches, then the same b | `(1-t^2)/4` |

For t != 0, the maximizing face is one ray, forcing unique **relatively
optimal** reset branches on the full image span. Calibration alone does not
give this uniqueness, and weighted dephasing is a non-reset optimizer for
the input-mass objective. At t=0, K_t is explicitly the chosen c=0 section
image rather than the whole cone surviving RI-08d; scaled identity branches
are optimal non-resets. Algebraic attainment does not establish physical
return-operation, reset or reference-repreparation availability.

Nonzero literal terminal cuts leave K_t. Their zero-weight cuts can remain
nonzero but cannot be selected; same-image calibrated zero-effect branches
instead output the entire zero kernel. Full raw image membership, every fine
(a,b) record, known context/settings and both origin-tagged initial histories
remain intact. The next-b question and analytic sums do not erase earlier a
labels or reread stored memory. Local RI-08e bounds, ancillary complete
positivity and physical or composite-theory claims do not transfer
automatically. This suite needs only the already supported `collections.abc`,
`dataclasses`, `fractions`, `itertools` and `unittest`; the runner is unchanged.

The fifteenth registration follows independent mathematical and implementation
review and coordinator acceptance of the cut-closed-completion handoff. Its
three source pins match the accepted bundle, and all fourteen prior entries
remain unchanged. The minimal convex cone containing K_t and closed under
every literal cut is the explicitly enlarged L_t, a direct sum of four PSD2
cones with sixteen-dimensional real span. Its positive inverse reconstructs
every native entry. This closure theorem does not establish independent
four-block preparation availability or permit forgetting known selectors.

Normalization uses total-entry mass `m=sum Tr(E_alpha rho_alpha)`, generally
different from raw trace `tau=(1/4)sum Tr(rho_alpha)`. The sharp inequality
`(1-abs(t))tau <= m <= (1+abs(t))tau` makes mass faithful for fixed interior t,
but the normalized trace bound `1/(1-abs(t))` diverges toward either endpoint.
At an endpoint, positive dark additions make the normalized base unbounded.
Whole-cone mass-dominated effects satisfy `0 <= F_alpha <= E_alpha`: their
span has dimension sixteen in the interior, while endpoint effects factor
through four weights. At endpoints the positive zero-mass subcone spans four
dimensions, the common effect kernel has dimension twelve, and the single
mass kernel has dimension fifteen. Ordinary norm-bounded probes need not be
mass dominated.

Literal cuts are positive, complete and perfectly repeatable on L_t under the
new reusable operation contract. Raw completeness includes every nonzero
zero-weight endpoint cut; such outputs cannot be normalized or committed,
and positive-weight normalized ensembles alone may omit raw payload.
Equal normalized finite future-record laws are equivalent to equal weights
only for the cut-only catalogue at the same full prefix and known context.
Unnormalized inputs instead have outcome-weight measures including total
mass. The quotient API is an algebraic weight query, not a context-equivalence
predicate, an available reset or an instruction to replace residuals/history.
Extra interior effects and residual-dependent policies are outside that
catalogue; fine outcomes, settings and origin-tagged records remain intact.

RI-07 still needs its full fixed-prefix, stationary-experiment or finite
controller, positive complete branch, faithful committing-output, finite
full-label and silent-observation hypotheses. At endpoints only the explicitly
faithful weight cone qualifies after those remaining hypotheses and all
claimed descents are checked. No raw first-commit limit follows from quotient
convergence or finite partial-sum intertwining without a separate proof.
No new silent law, physical availability, ancillary/composite theory or full
QM is inferred. Its imports are the same five standard-library modules as
joint repeatability, so the runner and dependency allowlist remain unchanged.

The sixteenth registration follows coordinator acceptance and independent
proof/source audits of the reversible-generator handoff. Its three hashes
match the accepted bundle; all fifteen earlier registration objects and their
source pins are preserved. On fixed interior L_t, an all-real strongly
continuous group of real-linear maps, positive with positive inverses and
preserving native mass, has independent filtered Hamiltonian form in each
of the four cells. These are added operational-law premises on the actual
sixteen-dimensional span, not a derivation of physical time or Hamiltonians
from DET. Faithful filtering turns each positive-definite cell effect into
ordinary trace. There are twelve nontrivial real generator parameters and
four scalar gauge directions; no values, energies or rates are selected.
Weighted congruences can change ordinary raw trace while preserving native mass.

All classified flows preserve the four cell weights and commute with literal
cuts. Cut-only future laws therefore cannot identify the generators under a
common finite retained-history command/cut/stop policy. The comparison requires
normalized sources, the same known context and full committed prefix, and
identical initial pending and nominal-command metadata. Distinct actual words
remain distinct records and can affect a metadata-aware policy; neither full
residual identity nor permission to erase commands follows.

Polarized endpoints admit positive reversible dark growth with unbounded raw
trace and no faithful inverse filter. Static transpose is an orientation-reversing
individual automorphism, not a counterexample obtained by dropping parameter
continuity alone from an R-group: divisibility still excludes its orientation
and nontrivial cell permutations. The genuine discontinuous reparameterization
example is explicitly nonconstructive. Forward dephasing has a nonpositive
inverse and lies outside the reversible hypotheses.

The exact typed fixture uses t=3/5 and named rational group elements, not
additive time readings. Additional dominated effects and general generator,
endpoint, transpose and dephasing diagnostics are separate from its primary
command catalogue. All fine records, provenance and pending words remain
retained. Finite checks do not establish all-real continuity, physical
availability, native dynamics, full QM, geometry, rest mass or gravity. Its
direct imports use the same five standard-library modules as the preceding
suite; the runner and seven-module allowlist remain unchanged.

The seventeenth registration follows independent proof/source audits and
coordinator acceptance of the terminal-read-observability handoff. Its three
pins match the accepted bundle; all sixteen earlier objects are preserved.
One additional available, exactly calibrated terminal read resolves eight
full cell/sign outcomes. With the supplied common-X commands, backward-effect
ranks on the full interior L_t span are 12 for a YZ read axis, 8 for an X
axis and 16 for a tilted axis; normalized affine dimensions are 11, 7 and 15.
These are minimum homogeneous mass-retaining real-linear predictive dimensions
on the whole mathematical cone, not physical preparation or nonlinear encoding
bounds. Finite-policy equivalence requires matching known context/calibration,
full prefix, initial pending word and nominal-command metadata; known selectors
and distinct command words remain retained.

The all-interior proof is separate from the exact t=3/5 fixture, whose only
primary read has axis (3/5,0,4/5). Empty, A and AA settings reconstruct every
native entry from full outcome weights for the same supplied source. Three
resolved settings are necessary on the whole domain; randomized retained
selectors still count as distinct settings. Shared cell weights, unit mass
and positive reconstructed blocks characterize exact compatible tables.
Zero cells need no division, and incompatible tables are refused rather than
fitted or projected. This is exact model consistency, not empirical frequency
validation or finite-sample tomography accuracy.

A terminal response retains the pre-read source and full metadata but specifies
no postmeasurement residual or reusable instrument. Further commands, cuts,
reads and resets are refused; zero-weight outcomes cannot be selected. No
earlier preparation or history-selection probability is inferred. At polarized
endpoints, mass-dominated effects still see only four weights, so the faithful
interior inverse and full observability do not extend. Alternative X/Z reads
and extra-control counterexamples are diagnostic, not primary operations.
Read calibration/availability, the inherited domain and known commands remain
supplied premises: no unknown Hamiltonian, physical time, full QM, geometry,
rest mass or gravity is identified. The runner and seven-module allowlist are
unchanged.

The eighteenth registration follows coordinator acceptance and independent
mathematical/source review of the observation-stability capstone, including
the corrected raw-candidate metadata boundary. Its three source pins match
the revised accepted bundle; all seventeen preceding objects are preserved.
For the same three calibrated terminal-read settings, filtered distance is
bounded below by the largest full-law TV error and above by the sum of errors
weighted by inverse-axis column norms. Those coefficients and their sum are
sharp on the full mathematical domain. Radical constants, safe rational upper
enclosures and explanatory decimals remain distinct. The proof allows fixed
interior t; the exact primary fixture still uses t=3/5 and the accepted tilt.

The native raw-distance bound has an unavoidable factor `1/(1-abs(t))`, even
for bounded raw sources; raw distance is not a probability distance. Axis
conditioning also diverges as the read approaches either rank-loss boundary.
Small full-law errors cannot uniformly control rare-cell conditional states,
and a zero-cell conditional state is undefined. Neither finite deterministic
budgets nor matching metadata establish calibration, repeated preparation or
statistical confidence.

A supplied exact feasible candidate certifies nonemptiness and a deterministic
diameter bound. Failure of that candidate is inconclusive about other
candidates; no solver, fitting, projection or silent normalization is supplied.
Typed candidates preserve checked context/history/pending payloads. Raw-matrix
audits require `metadata=None` and reject attached metadata through every entry
point; they do not become prepared States. Audit results are not terminal
continuations or physical operations. The event-probability target corollary
is algebraic error transfer; binary expectations need the stated factor of
two. No new observation, reusable instrument, measured application result,
unknown dynamics, full QM or gravity claim follows. All six direct standard-
library imports already fit the unchanged seven-module runner allowlist.

Every statement document and executable source has a pinned SHA-256. The
manifest records a statement summary, explicit premises and limits separately
from the check entrypoint. Document cross-references and external mathematical
literature are not recursively authenticated by this registry; it is an
executable evidence inventory, not a formal proof-dependency graph.

## Execution and identity contract

1. Validate strict JSON fields, unique suite IDs, canonical relative regular
   files, no symlink components, bounded file sizes and exact source hashes.
   Repeated paths must have consistent bytes/identities across registrations.
2. Parse every registered Python source without executing it. Starting at the
   selected entrypoint, recursively account for ordinary sibling-module imports.
   Require that this closure exactly matches the declared Python source set and
   that its sorted direct standard-library imports match the manifest.
3. Check the captured document, code and manifest bytes again before execution.
   Launch the current Python executable with `-I -S -B` and optionally `-O`:
   isolated mode, no site packages and no bytecode writes. No shell is used.
   The suite directory is never added to the child's import path.
4. Supply verified local source **snapshots through stdin**. A small importer
   executes those snapshots in memory; it never rereads local source files.
   Load unittest cases only from the explicitly selected entry module, under
   `registered_research_check`, and run them. The existing scripts' `__main__`
   guards only invoke unittest; this runner supplies that invocation instead.
5. Report loaded local source identities, finite test outcomes and retained
   output. Compare actual loaded sources with the declared source set. A
   conditional import may remain unexecuted: it still must be pinned and is
   listed in `unexecuted_declared_sources`. Static coverage does not claim every
   branch or source executed. The inventory contains eighteen suites; actual
   source loading is reported separately for each selected run.
6. Check the manifest, all registered documents/code and runner bytes afterward.
   If registered bytes change, fail the overall result and stop before starting
   later checks. The reported result remains attached to the original snapshots;
   it is not silently reidentified with changed files.

JSON includes the manifest hash, all registered file identities, runner hash,
Python executable hash/version/implementation, operating-system information,
child flags, selected suite outcomes and before/after checks. Standard-library
transitive dependencies are supplied by that Python runtime; their individual
files are not claimed to have been frozen or hashed. This is not a hermetic
build or an independent authentication of the interpreter installation.

The import contract deliberately supports only the current small source
language: ordinary sibling `.py` imports and the seven stated standard-library
imports. Packages, relative/dotted local imports, undeclared sources, other
external imports and direct dynamic import/code-evaluation operations are
refused. New dependency forms require a reviewed runner/manifest extension.

The child additionally uses a Python audit hook to refuse common file writes,
filesystem mutations, new subprocesses and network sockets. This provides
defense against accidental side effects in the reviewed checks; **it is not a
sandbox or a proof about arbitrary reflective Python**. Registration requires
source review. Before/after hashes detect observed endpoint changes, not every
possible transient change later restored to identical bytes. Source snapshots
keep local executed code independent of that disk race.

## Registration and maintenance

Register another suite only after independent handoff review. Identify its
written statement and premise boundaries, inspect its actual local imports and
top-level execution, and calculate hashes for every executable dependency and
the statement document. Then verify `--check`, run the explicit new selection,
and inspect its loaded-source inventory and normal/optimized results. Do not
add a directory wildcard, silently update hashes after a failure or treat a
changed statement as interchangeable with the old one.

The completed controlled-context, first-commit quotient, maximal record-domain,
control-selected qubit, repeatable record instrument, joint-recordability,
repeatability-robustness, joint-repeatability, cut-closed-completion and
reversible-generator, terminal-read-observability and observation-stability
handoffs are now registered.
Subsequent Q research still
requires a new independent handoff review before registration.
Frozen bundles remain untouched; their own capture/replay procedures retain
their separate evidential scope.

The focused regression suite is
[test_research_registry.py](../det8/tests/test_research_registry.py). It exercises
missing/transitive dependencies, invalid and escaping paths, symlinks, conflicting
source identities, stale statements, failed/empty/skipped checks, source drift,
timeouts, explicit selection, snapshot execution and absence of cache writes.

```sh
.venv/bin/python -B -m pytest -p no:cacheprovider det8/tests/test_research_registry.py
```

This runner regression file participates in ordinary `det8/tests` discovery.
Its real-registry check is read-only; its execution cases use tiny temporary
fixtures. It does not implicitly execute the eighteen research suites. The
[RI-15 local-to-joint adapter](validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md)
and its separate coordinator launcher/tests use an explicit alias contract;
they are not registered here or included in these suite/source/witness totals.

Verification after the reviewed thirteenth registration, on Python 3.11.6: all
43 runner regressions passed, and all thirteen registered suites passed normally
and with `-O` (234 finite witness tests in each mode). All twenty-two declared
executable sources were loaded; before/after source checks reported no changes,
and no suite reported skipped checks or unexecuted declared sources. The manifest
SHA-256 was `212459d6ee478e3553db73b92069fb88802065108f3508a238a3072bc4494607`.
All 17 local Markdown links in this guide resolve. Dependency tests cover
`collections.abc`/`types` and exact `math.isqrt` execution in both modes, require
the declared import closure, and reject an undeclared dotted module rather than
accepting its allowed prefix. Ruff check and format validation passed for the
updated runner and regression file. These results
verify this bounded execution contract; they do not change the underlying
theorem or physical statuses.

Verification after the reviewed fourteenth registration: all 43 runner
regressions passed, and all fourteen suites passed in normal and optimized
children, with 264 finite witnesses in each mode. All twenty-four declared
executable sources were loaded, with no skipped checks, unexecuted declared
sources or observed before/after source drift. The manifest SHA-256 is
`68f3c5737d2513732e3193ee410ee6f607d60cbbef783612fc140404f6909f47`;
the runner remains
`35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f`.
All thirteen preceding registration objects, their pinned files and the runner
bytes were preserved from the preceding manifest
`212459d6ee478e3553db73b92069fb88802065108f3508a238a3072bc4494607`.
The guide's 18 local Markdown links resolve. The updated regression file passes
Ruff check and format validation. The additional 30 witnesses verify the
accepted joint-repeatability bundle's bounded implementation; registration
does not promote its conditional premises to physical facts.

Verification after the reviewed fifteenth registration: all 64 focused checks
passed (43 registry regressions and 21 claim/summary checks). All fifteen
research suites passed normally and with optimized children, with 296 finite
witnesses and all twenty-six local executable sources loaded in each mode.
There were no skips, missing declared sources or observed before/after source
changes. The manifest SHA-256 is
`5ec201d618252ba4d9992112a62170c4482f42a1ffd15a80d1e9af9235b84256`;
all fourteen objects from the preceding
`68f3c5737d2513732e3193ee410ee6f607d60cbbef783612fc140404f6909f47`
manifest and their pinned files are preserved. The runner and claim exporter
are unchanged. Explicit claim-artifact references extend through RI-08g;
the regenerated claim document matches the exporter, while the canonical
`claim_summary()` and `registry_document()` JSON digests remain unchanged.
The source check, scoped Ruff check/format validation and all 19 guide links
pass. This adds the accepted conditional artifact and its 32 witnesses without
altering broad claim statuses, physical evidence or public support.

Verification of the reviewed sixteenth registration: all 64 focused checks
passed (43 registry regressions and 21 claim/summary checks). The source-only
check validates sixteen suites and twenty-eight local executable sources;
the inventory contains 326 finite witnesses. Complete coordinator replays are
recorded in [review progress](coordination/REVIEW_PROGRESS.md). The manifest
SHA-256 is
`cab559036fe724ad78edd0beb7565586eb506515d24e4dc0dd4544074677f939`.
Removing the new object reconstructs the exact preceding manifest
`5ec201d618252ba4d9992112a62170c4482f42a1ffd15a80d1e9af9235b84256`.
All fifteen prior objects and pinned files, the runner, its seven-module
allowlist and the claim exporter are preserved. Explicit accepted-artifact
references extend through RI-08h. Export parity, legacy canonical claim JSON
digests, scoped Ruff check/format validation and local Markdown links pass.
RI-15 remains a separate adapter contract and is excluded from these totals.

Verification of the reviewed seventeenth registration: all 64 focused checks
passed (43 registry regressions and 21 claim/summary checks). The source-only
check validates seventeen suites and thirty local executable sources; the
inventory contains 356 finite witnesses. The manifest SHA-256 is
`aabf2b1a0a25bbb1511e33ad7e34ce63958e87bf224fa743c4c5b7369390c3c5`.
Removing the new object reconstructs the exact preceding manifest
`cab559036fe724ad78edd0beb7565586eb506515d24e4dc0dd4544074677f939`.
All sixteen prior objects and pinned files, the runner/import contract and the
exporter are preserved. Explicit accepted-artifact references extend through
RI-08i; export parity and both legacy canonical claim JSON digests are unchanged.
Scoped Ruff check/format validation and all 23 guide links pass. Complete
coordinator replay results belong to the existing review-progress record;
registration does not change broad claim statuses or physical evidence.

Verification of the reviewed eighteenth registration: all 64 focused checks
passed (43 registry regressions and 21 claim/summary checks). The complete
manifest pin/import preflight validates eighteen suites and thirty-two local
executable sources. The inventory contains 384 finite witnesses: 356 from the
seventeen earlier suites, whose normal/optimized results and source pins are
preserved, plus the capstone's 28. This is not a fresh 384-witness all-suite
replay. Coordinator integration replay is scoped to the new capstone normally
and with `-O`, complete-manifest preflight and staged registry regressions;
its results are recorded in review progress.

The manifest SHA-256 is
`a5d94f2d5451f6810855b129886500afc840bf1ee86b01dd515c98158cf5454f`.
Removing the new object reconstructs the exact preceding manifest
`aabf2b1a0a25bbb1511e33ad7e34ce63958e87bf224fa743c4c5b7369390c3c5`.
All seventeen prior objects and pinned files, the runner/import contract and
the exporter are preserved. Explicit accepted-artifact references extend
through RI-08j; export parity and both legacy canonical claim JSON digests
remain unchanged. Scoped Ruff check/format validation and all 24 guide links
pass. RI-15 remains separate, and registration changes no broad scientific,
physical-evidence or support status.
