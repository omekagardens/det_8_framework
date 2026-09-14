**Independent-review implementation progress**

13 September 2026. Coordinator-owned. See the root
[implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md) for scope and file
reservations, and [QR_HANDOFF.md](QR_HANDOFF.md) for the QR owner's current work.

| Item | Current evidence | Next action |
|---|---|---|
| QR coordination / RI-05–08j and RI-16–18 | **Conditional synthesis and retained-word extension published.** RI-16 passed two independent audits, 27 new witnesses per mode and 43 isolated registry regressions. | RI-17 design is published in verified `ad04963`; RI-18 is active. Root launcher infrastructure passed 62 isolated fixture/refusal cases and provisional review. Final artifact pins and actual protocol execution await QR acceptance. |
| RI-01 status reconciliation | **Accepted.** Six landing/status documents updated; coordinator reviewed current versus historical scope and checked 117 local file links across them and the new trackers/runner guide, with no missing targets. Scoped whitespace checks pass. | Maintain current-source evidence distinctions as later work lands. |
| RI-02 kernel contract | **Accepted.** Coordinator inspected factorization and recordability contracts and independently reran 97 focused pytest cases successfully. Implementer also reports 49 existing consumer checks and clean scoped lint/whitespace checks. | Keep this research interface separate from the validated public core. `cholesky()` now returns an original-event-order pivoted Gram factor, not necessarily triangular. |
| RI-03 research registry | **Accepted for nineteen suites.** Cumulative411 witnesses/34 executable sources: prior384 source-bound results with unchanged pins plus27 new RI-16 checks per mode. Full preflight and43 isolated registry regressions pass. | Preserve execution boundaries;411 is not a fresh all-suite replay. RI-15 remains separate; the deferred claims endpoint remains its explicit18-reference subset. |
| RI-04 current mathematical certificates | **Accepted.** Eight research modules and narrow legacy groups reconciled; coordinator reran 141 focused cases successfully. Implementer reports 80 impacted legacy checks with no failures/errors/skips. MODEL_CARD current O1/O2 assessment is reconciled; Previous remains historical. | RI-11 is now accepted separately; general reconstruction/physical premise selection remains open. |
| RI-11–12 applied work | **RI-11 published in verified `f8339ea`:** 105 focused tests and 33 legacy checks passed in isolation after numerical/chronology and snapshot review. RI-12 exact identifiability is published; synthetic comparator remains locally accepted with RET publication prerequisites. | Measured instrument/dataset, target, tolerance and evaluation objective remain open. |
| RI-13–15 project wholeness | **Ledger, scoped metadata and exact adapter accepted.** The [operational premise ledger](OPERATIONAL_PREMISE_LEDGER.md) includes RI-08j and the accepted conditional local-to-joint interface. The separate claim endpoint lists eighteen accepted references and retains unchanged legacy outputs. RI-15 passed two source audits and root's 36 regression cases, including normal/optimized pinned witnesses. | Keep full earlier probability/tree orchestration and general interoperability separate from the accepted conditional adapter. Measured application data/objectives remain open. |
| Recurring follow-up | Hourly thread follow-up created and active: `det-review-follow-through`. | Read current ownership and results each run; review QR handoffs and advance the next bounded item. |
| Remote checkpoints | Latest application checkpoint: [f8339ea](https://github.com/omekagardens/det_8_framework/commit/f8339ea4a4ce886ddc4513d989a2cecbad9d8dca). Latest QR design checkpoint: `ad04963`; QR theorem checkpoint: `22eca4e`; synthesis: `50d652f`; research/identifiability repairs: `38be4c0`. All pushed normally to `origin/ret` and independently verified. Root owns git/index. | Continue scoped publication after review, preserving QR reservations and the deferred baseline. |

The source tree already contained extensive edits before implementation began.
This progress record reports only the scoped review-follow-through work. No
release gate or physical claim is closed by starting these assignments.

Accepted work is not all published. The current
[publication backlog](PUBLICATION_BACKLOG.md) records source dependencies and
the published RI-02/RI-04 plus RI-12 identifiability checkpoint.

**RI-02 acceptance detail**

Changed `det8/models/pair_kernel.py` and added
`det8/tests/test_pair_kernel_contracts.py`. Singular real/complex PSD kernels
now have a Gram factor with null directions retained. The numerical PSD check
has an explicit entrywise backward-error tolerance; it does not claim exact
positivity for floating-point data. Commitment requires a complete disjoint
partition, exactly zero represented cross-cell interference and valid raw
probability weights. It does not renormalize an invalid input. Exact complex
decoherence implies additivity; additive real event weights alone do not imply
complex decoherence. Approximate diagnostics account for accumulated cross
terms and cannot authorize commitment.

Coordinator rerun: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest
-p no:cacheprovider det8/tests/test_pair_kernel_contracts.py
det8/tests/test_quantum_correctness.py det8/tests/test_reproducibility_contracts.py
-q` — **97 passed**. Independent cases cover singular complex and permuted
Gram matrices, extreme finite scales, indefinite and malformed inputs, zero-mass
nonzero blocks, unlicensed raw weights, same-diagonal/different-readout states,
and the existing Gram-sum consumer. These focused results do not recertify the
whole dirty checkout or alter historical G1 evidence.

**RI-03 acceptance detail**

New files: `docs/research/registry.json`, `scripts/run_research_checks.py`,
`det8/tests/test_research_registry.py` and `docs/RESEARCH_CHECKS.md`.
The initial registry bound six statement documents and eight executable sources.
The runner validates the inventory without executing code by default, and
executes only selected suites from checked source snapshots. Its isolation and
audit hook prevent common accidental side effects; they are not a hostile-code
sandbox. Endpoint source checks do not detect a transient change restored to
identical bytes. Standard-library files are not individually frozen.

Coordinator checks on CPython 3.11.6, Darwin arm64:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider det8/tests/test_research_registry.py -q` — **38 passed**.
- `.venv/bin/python -B scripts/run_research_checks.py --all` — **56 passed** across 6 named suites.
- The same command with `--optimized` — **56 passed**, no skipped or expected-failure witnesses in either mode.
- Suite counts: strict derivation 8, operation domain 9, hypothesis countermodels 5, chosen law 9, coherent readout 15, record context 10.
- Manifest SHA-256: `228663a5cf77b43df8ba14839e090e844c6d9f95d26961800a49ec0243fa8a89`.
- Runner SHA-256: `4cfadda07b4e17a8bfdefc11885b4fadcbdbc5b1eba6758d8ae98112e1f70b85`.
- Python executable SHA-256: `033d83a12ab74b7bcade8248b1bca644f275d3965350b61fe485c2645e1f68e8`.

Normal and optimized modes are repeat checks of the same finite witnesses,
not 112 independent scientific results. Source identity and passing examples
do not establish the universal statements or their physical premises.

After RI-05/RI-06 acceptance, a seventh registration binds the completed
controlled-context note, `model.py` and `check.py` to their handoff hashes.
The six earlier registration objects remain unchanged. The runner's narrow
standard-library contract now also permits the actually used `collections.abc`
and `types` imports. Coordinator replay: **40 runner regressions passed** and
**79 finite witnesses passed in each mode**, including the 23 controlled-context
checks. Every declared executable source loaded, with no observed source drift.

Seventh-registration manifest SHA-256:
`c0ace97756ab7a22c9fc1797fcf4aeda91a4074884559043363e2be5c905cc85`.
Seventh-registration runner SHA-256:
`0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613`.
The original six-suite hashes above retain their historical meaning. These
new normal/optimized executions do not create additional independent proofs.

**RI-05/RI-06 bounded proof acceptance**

The coordinator read the complete
[controlled-context note](../validation/t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md),
inspected source and independent tests, and reviewed a separate read-only
mathematical assessment. The supplied generators have positive eigenvalues,
mass one and an injective classical-cone encoding. Nonnegative branch matrices
and complete mass identities prove forward closure for every positive input.
The selected switch has no positive linear extension to the full recordable
cone, so its domain restriction is mathematically necessary for this map.

Typed backward effect closure stabilizes by finite dimension. Closure under
every allowed pullback proves sufficiency for all finite word probabilities;
the stored legal basis words prove necessity and supply separating tests.
The fixed read–switch–read joint record law directly equals the four input
coordinates. Predictive rank is four: no nontrivial residual compression is
licensed by the full test family. Changing the available tests changes the
quotient; an attempt-only identification is broken by later read access.

Acceptance includes these qualifications: the operational cone/composite are
classical; apparatus maps and policies are supplied; arbitrary initial
histories are checked structurally, not authenticated as reachable; the
structural append helper assumes a positive selected branch and the actual
transition path enforces it; protocol boundaries are not physical timestamps;
tensor-local map commutation is not whole-history schedule covariance.
Internal independent review is not external peer review or formal proof
verification. The general theorem exceeds the executable's two-mode instance.

Coordinator directly reran the new `check.py` with `.venv/bin/python -B` and
with `-B -O`: **23 tests passed in each mode**. The QR owner reports 106 scoped
regression tests in both modes; those wider counts are owner-reported, not an
additional whole-tree acceptance. The seventh source registration now binds
and reruns the final formatted source snapshot. The QR handoff retains its
source hashes and exact reproduction commands.

The next QR assignment, RI-07, has been sent and acknowledged. It should establish finite typed first-commit
map convergence under explicit compact-base hypotheses, the complementary
never-commit mass, and descent through a quotient invariant under every lawful
continuation. It must state what observation information elimination forgets
and retain full first-commit labels/residuals. Neither faithful mass nor
convergence may be presented as selecting QM. Counterexamples and sufficient
conditions are useful results without an unsupported general classification.

**RI-04 certificate and input-domain acceptance**

Changed the approved current research modules `why_complex.py`,
`correlation_class.py`, `correlation_frontier.py`, `record_extendability.py`,
`grade2_justification.py`, `born_rule_uniqueness.py`, `quantum_deadlock.py` and
`u1_emergence.py` under `det8/models`, their eight affected legacy runner
groups, and new `det8/tests/test_research_claim_contracts.py`. Pre-existing
grade-2 input-validation work remains in place. Historical captured results
were not rewritten.

Emitted results now distinguish assumed complex compatibility from field
selection; grade-two interference from strong positivity/Gram representation;
the NPA commuting endpoint `C_qc` from tensor closure `C_qa`; `Q_{1+AB}` from
ordinary `Q1`; and TLM correlator membership from arbitrary biased behavior
membership. Direct consumers no longer turn these conditional calculations
into an ontology validation or a proof of U(1) emergence. The uniform-preserving
noninjective channel provides a concrete counterexample to deriving
reversibility from uniform-state preservation.

The independent input review additionally found that signed normalized
no-signalling tables could pass probability validation. Finite/nonnegative
validation and invalid-membership refusal now prevent that false result.
`tlm_sums`/`tlm_margin` reject invalid or out-of-range inputs without clipping;
the historical `is_quantum_masanes` callable remains a scoped projection
predicate. Legacy report keys are retained with adjacent scope metadata.
The real-kernel interference fixture is normalized and has `I₂=1/3`.

Coordinator reproduction:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_research_claim_contracts.py \
  det8/tests/test_pair_kernel_contracts.py \
  det8/tests/test_quantum_correctness.py -q
```

**141 passed**: 48 new research-contract cases, 47 pair-kernel cases and 46
quantum-correctness cases. These overlap the earlier kernel checks and must
not be added as independent evidence. Exact rational witnesses, preserving
and nonpreserving generators, Lp controls, singular extensions, biased tables
with common correlators, and invalid probability tables supplement metadata
regressions. One preview test incorrectly squared a floating square root in
an exact oracle; its oracle was corrected to direct real/imaginary squares,
while floating production output retains a numerical tolerance.

The implementer reports **80 affected legacy checks passed**, with no
failures/errors/skips, and clean Ruff checks for the eight modules/new tests
and owned runner groups. The broad legacy runner still has 120 unrelated Ruff
findings; this was not presented as a whole-runner lint cleanup. Coordinator
scoped whitespace checks pass. All first-cycle implementation reservations
are released. A final file-target check across ten status/tracker/application/
runner documents resolved **124 local links** with no missing targets.

**Continuation after the first cycle:** initial repairs and the P1/P2 handoff were
accepted; RI-07 was assigned in QR, RI-11 remained the next independent coordinator
repair, and the hourly follow-up remains active. No release, G2 calibration,
physical experiment, full-QM reconstruction or geometry claim is closed by
this cycle. No staging, commit or push was performed.

**RI-07 acceptance — finite first-commit maps and lawful quotients**

The coordinator read the complete
[FIRST_COMMIT_QUOTIENT.md](../validation/t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md),
inspected `model.py` and its independent check inventory, and obtained separate
mathematical and executable-source reviews. No algebraic blocker was found.
Both independent reviewers reran all 23 new checks normally and under `-O`,
with bytecode writing disabled. The broader 129-test QR replay remains
owner-reported, not a whole-tree acceptance or the root review's differently
composed historical 129-test set.

The proof controls positive first-commit increments by their output mass,
bounds the scalar sums by complete mass accounting, and uses a finite positive
basis to obtain operator-norm convergence. The first-commit map is the least
positive solution of `H=B+HS`. The periodic dark-mode example shows why neither
convergence of silent residuals nor invertibility of `I−S` is needed, and why
an arbitrary subnormalized fixed-point solution can invent commitments.

The quotient proof includes every declared continuation and terminal effect.
Faithful mass descends and makes the normalized quotient base a compact image
of the original base, proving closedness, pointedness, generation and faithful
normalization. Finite partial first-commit sums intertwine; continuity passes
this identity to their limits. The arbitrary PSD projection example fails
the mass hypotheses and correctly has a nonclosed image.

Accepted scope is each stated finite model/prefix/controller, with faithful
mass on **both input and committing output cones**. Elimination retains full
committing labels, precursors and output residuals, but discards silent counts,
paths and intermediate controller visits from the target observation interface.
Never mass is a limiting path probability; it supplies neither a terminal
residual nor a finite diagnosis. Hidden-controller reduction fails if a newly
available readout or postselected edge exposes the discarded phase. An eventual
output quotient does not by itself preserve primitive tests. Nonfaithful
examples show both convergence and divergence; a lawful quotient may converge
even when the original residual sums do not. No nonexistent original limit is
used, and no uniform model-family/history result is claimed.

The exact examples remain chosen classical models. Positivity here does not
establish complete positivity for unstated ancillas, select QM, justify physical
operations or produce geometry. This is internal independent acceptance, not
external peer review or proof-assistant certification. The original controlled-
context bundle's three hashes remain unchanged.

Accepted RI-07 source identities:

| New bundle file | SHA-256 |
|---|---|
| `FIRST_COMMIT_QUOTIENT.md` | `a702625b5e5af97881292e06750f94cef16319a0d0f3c065058207991818fe0c` |
| `model.py` | `42c67879fc4ccba35d7155ab517275f76fadce68371a30c36438c237b636c8d0` |
| `check.py` | `0ab1fdc92eb391e2a52462f5b1cc77ab68adf641a0010600c6563faf08385970` |

The coordinator has assigned RI-08a to QR in a new isolated bundle. Its
conjecture is that every bounded effect on maximal `K_P` is a linear combination
of cell weights `q_P`, and every positive mass-nonincreasing full-domain
`K_P→K_Q` transition factors as `q_Q T=A_T q_P` with a substochastic matrix.
The requested proof/refutation includes arbitrary finite partitions, actual
linear spans, quotient surjectivity, operation availability, full labels and
the faithful-quotient first-commit consequence. Exact classical equality needs
the corresponding readout/preparation availability; a restricted catalogue
can be less informative. This is a conjecture under investigation, not an
accepted conclusion.

The proposed result would generalize the earlier one-cell full-cone obstruction
and the nonextension of one selected switch. A smaller-domain operation would
identify an excluded premise, not refute the full-domain claim. No conclusion
about nature or a selected quantum preparation domain is authorized. The
measurement-answerability application remains in the parallel RI-12 lane;
RI-11 remains the next independent coordinator repair.

**Eighth-registration acceptance and current continuation**

Added `first-commit-quotient` to `docs/research/registry.json`, updated the
explicit inventory regression and `docs/RESEARCH_CHECKS.md`. All seven prior
registration objects and hashes remain unchanged. No runner or dependency
allowlist change was needed. The new entry separates sufficient faithful-cone
premises, retained full-label residuals/never mass, observation losses and
quotient invariance from the selected finite examples and open physical claims.

Coordinator independently reran the registry regression command:
**40 passed**. Both `.venv/bin/python -B scripts/run_research_checks.py --all`
and its `--optimized` variant passed **102 finite witnesses** across eight
suites: 8 strict derivation, 9 operation domain, 5 hypothesis countermodels,
9 chosen law, 15 coherent readout, 10 record context, 23 controlled context
and 23 first commit/quotient. All 12 executable sources loaded; source and
runner endpoint checks found no changes. These repeat modes and overlapping
regressions are not independent scientific proofs.

Eighth-registration manifest SHA-256:
`fc41b4e45a5efe2d112e2463d113e4389d06b29d7b436982eca2e76aff0be787`.
Unchanged runner SHA-256:
`0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613`.
The registry implementer reports scoped Ruff lint/format and whitespace checks
passed; coordinator checked 22 local file links in the updated plan, progress
record and runner guide, with no missing targets. Registration source
reservations are released.

RI-07 acceptance and the RI-08a assignment were sent to QR. QR acknowledged
RI-08a and is working in a new isolated bundle, preserving accepted sources.
The hourly follow-up remains active; RI-11 is still the next independent
coordinator repair. No RET source/bank, historical review, release threshold,
physical claim, staging, commit or push was changed in this handoff cycle.

**RI-08a acceptance and ninth registration**

The coordinator read the complete
[maximal-domain proof](../validation/t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md)
and implementation and obtained separate mathematical and source reviews.
No blocker was found. Positive shifts establish the actual real span;
dark-block polarization and both real and imaginary constant-mass cross
families establish the bounded-effect classification. Pulling back each
output cell effect gives the unique substochastic map and its composition
law. This is a theorem on the entire specified cones and real spans, with
fixed operation availability, rather than a consequence of finite examples.

The positive section makes the quotient exactly the orthant. Exact residual
equivalence still requires cell-readout availability; a full classical
operational catalogue requires further preparation/transition availability.
Zero branch mass can coexist with a nonzero dark output, which cannot be
normalized or selected. Full committed records, labels, precursors and known
apparatus types remain retained. The full-domain congruence counterexample
shows that RI-07 first-commit convergence applies to the faithful quotient
while original nonfaithful residual sums can diverge.

Accepted RI-08a identities:

| File | SHA-256 |
|---|---|
| `MAXIMAL_DOMAIN_QUOTIENT.md` | `57e509ffd245d24f244e052a0433bc7c1a46233387f2a54a9cfb618079780ad6` |
| `model.py` | `c3d1d33f117e5d9b7ad3af1ec5efc420bd6d9a6b415ee885211bd7d94b6bc606` |
| `check.py` | `1f4de15abcb2178666ab2a6b5c4af32ac3b140479679347c51e6c32ab68e9804` |

Added `maximal-record-domain` as the ninth registration; the eight earlier
objects and all accepted source bytes remain unchanged. Only the registry,
guide and explicit inventory regression changed; the runner and dependency
allowlist did not. Coordinator rerun: **40 registry regressions passed**, and
all nine suites succeeded both normally and under `--optimized`: **125 finite
witnesses per mode**, with all 14 executable sources loaded and no skips or
observed source/runner drift. Independent source review also checked 400 exact
Hermitian 2-by-2 PSD cases and the zero-weight nonzero cell-cut example.
QR's separately reported 152-test scope is a different inventory; it is not
added to the registered total. Repeated modes are not independent proofs.

Ninth-registration manifest SHA-256:
`e3fa04c1f533d1c9789c8d910527f6a83d4a0c567e843b1653abcfe02bc96b63`.
Unchanged runner SHA-256:
`0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613`.
Registry regression SHA-256:
`e05cd97db81d069c9a478c2d04a200e7e3fddd461579d13d35a568151f2b8c03`.
Guide SHA-256:
`81b36df65e339a996efc0fc4a1339e4851c5256f5859e5779015fc92003f908a`.

**RI-08b successor and parallel applied repair**

QR acknowledged the next concrete assignment: start from the full four-label
exact-recordability domain for partition `{0,1}|{2,3}` and investigate a
maximal viable cone under explicitly supplied H, quarter-phase and Z controls,
mass/recordability preservation for all control words, and Z exchange of
terminal readout labels. The conjectured raw form is
`D=[[A,cZ],[conj(c)Z,ZAZ]]`, `A >= |c|I`; its proposed operational quotient is
`q(D)=2 A^T`, with the existing qubit image as a positive section at `c=0`.
These are assigned proof targets, not accepted results.

The task must retain the possible invisible cross-block coordinate and prove
equivalence for the declared control-word/terminal-read catalogue. Additional
bounded effects may reveal that coordinate. A literal cell cut leaves the
source control domain: its full output must enter a separately typed terminal
target, with no silent reuse of source controls. Reusable instruments, all
quantum effects, composites and physical complex-field selection remain
separate obligations. Deletion checks will examine which tailored control or
calibration identities are doing the work. This advances beyond assuming an
image cone while making the extra operational premises explicit.

RI-11 implementation is proceeding in parallel under the reservations in the
master plan, including the two audited script consumers. The intended repair
replaces unsupported model-winner outputs with descriptive fit reporting,
correct Gaussian arithmetic and refusal, correct roughness moments and actual
elapsed chronology. An independent reviewer is preparing arithmetic and
boundary probes; acceptance and any remaining obligations will be recorded
after the sources are stable. RET source/banks and the dated review remain
outside this repair batch.

**RI-08b acceptance and tenth registration**

The coordinator read the entire
[control-selected qubit note](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md),
model and independent tests, and obtained a separate skeptical proof/source
review. No blocker was found. On the full initial Hermitian recordability
space, the supplied control/calibration identities force `F=cZ` and `B=ZAZ`.
The resulting six-dimensional real span retains complex c. Full raw positivity
is exactly `A >= |c|I`; algebraic conjugation proves sufficiency for all words
and inverses, rather than a depth-bounded simulation.

The positive quotient `rho=2 A^T` has image `PSD2` and the c=0 positive section.
I/H/P readout gives the correct X/Z/Y tomography and conjugate-U/transpose-U
control convention. Equivalence is exact for the declared catalogue, not for
all bounded effects. The c± example has identical predictions and identical
full same-word terminal cuts, while an extra source/pre-read effect separates
it. The invariant mixed-state ray shows why maximal mathematical viability
does not grant physical preparation richness. Deletion families and finite
closed action groups establish relative roles of the supplied premises.

Every nonzero literal cell cut leaves the source cone. Its full raw output,
setting word, outcome and precursor enter the distinct terminal type.
Nonzero zero-weight cuts cannot normalize or append. Constructors check
admissibility/history grammar, not global preparation reachability. The
accepted theorem supplies neither reusable instruments nor a physical
complex-field choice, ancilla theory, full QM or geometry.

Accepted source identities:

| RI-08b bundle file | SHA-256 |
|---|---|
| `CONTROL_SELECTED_QUBIT.md` | `b9ce11fc5c8e11a8aeefa57e7da76b528673a720c54e6e6858f02380742233a2` |
| `model.py` | `82a0e42a714cf744e9288618016f8cd12617eb0b92b1a1b59813e340db875cd4` |
| `check.py` | `8417baaa17d5ea6ab8a6ceef3492a63eccb413b02ff3fc3417ea81999425cbc5` |

The coordinator independently passed all 24 new tests normally and under
`-O`, checking the three pins before and after. Tenth registration
`control-selected-qubit` preserves the nine prior objects exactly and needs
no runner/dependency change. Final coordinator registry replay passed **149
finite witnesses in each mode**, across ten suites, with all **16** declared
executable sources loaded, none unexecuted, no skips and no observed source
or runner drift. QR's wider reported 176-test inventory is separate; it is
not added to these counts. These internal checks do not replace universal
proof review, external peer review or physical premise justification.

Tenth-registration manifest SHA-256 (historical after the eleventh registration below):
`bd125dfd0aa777a0f5ace13d7e310cf90f1558346c66063e693bfef75d3e3bd3`.
Unchanged runner SHA-256:
`0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613`.
Registry regression SHA-256:
`39953ecd3ac0cff7972730bb2a0942d19bb9071cf5e994fa389e8a22e532b486`.
Guide SHA-256:
`479fa1cdfbfb8808276a7144f5d8bcf46d2042197e090decbf35453604711d88`.

QR acknowledged RI-08c and is working in a new isolated bundle. The target
is an exposed-ray classification of same-cone positive branches with the
prescribed Pauli effects and perfect same-setting repeatability. If valid,
these new operational premises force the rank-one update and its zero branch,
rather than assuming a Kraus formula. Existence/physical availability and
return from the old terminal type must remain distinct. Explicit frames,
actual controls, feedback, full records and precursors are required. A second
target is exact preparation reachability from the mixed state with finite
Clifford controls, these instruments and separately declared randomization:
the proposed octahedron is not the full Bloch ball. These are active proof
targets, not accepted results.

**RI-11 implementation acceptance**

Accepted after source review, direct consumer inspection, independent
numerical/chronology probes and corrected boundary reruns. The final source
changes cover three applied modules, the two clock-analysis scripts, one
legacy test group, a new applied contract test file and the directly affected
operational-test assertion. [Application documentation](../applied_physics.md)
now distinguishes current corrections from preserved historical tables.

Gaussian arithmetic includes the proper likelihood constants and variance
parameter distinction. Ordinary BIC requires an explicit caller declaration
of regular identifiable likelihood fitting and sampling assumptions. Unknown-
variance zero RSS is unavailable, while known positive covariance permits
zero residual. The clipped finite κ bank reports descriptive errors and its
scale-confounded parameter combinations, not an invented independent count.
The linear baseline counts its fitted intercept; log-linear rank and possible
nonmonotonicity, zero-amplitude and insufficient-design degeneracy are explicit.

Roughness uses the full Gaussian difference covariance, including shared
adjacent errors. The n=20, sigma=0.1 constant-mean null has mean 0.38 and
variance 0.0224; the lower-noise generator declares its own deterministic and
noise contributions. No squared-discrepancy BIC or diffusion-identification
claim remains. All ten synthetic examples report descriptive fit families;
causal winner/count fields are unset. Historical generator aliases remain
callable, but old winner semantics are intentionally retired.

The shared aging report sorts and retains dated source records, elapsed days,
gaps, time systems and the existing leap-second contract. Both configured
single-pass scripts consume it. Unsupported missing chronology is refused,
including legacy `.clk.Z` records that do not provide dates. Clock covariance
and interval averaging remain unmodeled; this is not a new analysis of the
historical GNSS dataset or a calibrated likelihood comparison.

Independent review found and repaired positive-square underflow in RSS,
roughness and variance calculations. A positive profile variance MLE that
underflows has an explicit representability status, while its log-domain
likelihood can remain finite. Known-covariance whitening cannot silently
report zero quadratic residual for a nonzero input. The exponential bank
skips only an explicitly constant design; it propagates arithmetic refusal
rather than choosing a minimum from an incompletely scored bank. These
guards cover the detected boundaries, not all floating-point cancellation.

Final coordinator command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_applied_comparison_contracts.py \
  det8/tests/test_operational_scripts.py det8/tests/test_research_registry.py -q
```

**94 passed:** 49 new applied contract cases, five operational cases and 40
registry regressions. The separately invoked legacy `test_applied_physics`
group passed **12**, with zero failures, errors or skips. Independent review
passed additional numerical/chronology/consumer probes and normal/optimized
checks of the final affected paths; these overlapping checks are not added
into a scientific evidence count. The implementer reports scoped seven-file
Ruff and whitespace checks passed; the coordinator checked final source hashes.

| Accepted RI-11 source | SHA-256 |
|---|---|
| `det8/applied_physics/adversarial.py` | `d0135d04988899cfa33a4e49bc74fa458c8a82fb260fefa61a17ed9277613de1` |
| `det8/applied_physics/applied_tests.py` | `2284a9530109e642cc3c06cbfca9c3a51314d9ef20564a8e6250ca1cdcde93b4` |
| `det8/applied_physics/discriminator.py` | `a5fec004745446b3328357d982a70ddf4234ff4bf4aa44547c6687a28ecd07a5` |
| `det8/tests/test_applied_comparison_contracts.py` | `ff661ad6958d4c27e70a189189a828538c4bc7b23e3c4a4a64a435ca11bbceae` |
| `det8/tests/test_operational_scripts.py` | `bc1c2316780fdfe1e152e21757611398cd84de4822d374ba4dde5e0fac78844d` |
| `scripts/full_year_aging.py` | `2b496223b7340de4fbfcaf4644064b0f2cb7b897eefb9b0a082852588504cc29` |
| `scripts/g11_quadratic.py` | `2a5d5e60f12b1fa8537f169d3f1d97e5a1ed2c0ac3b679a21e9b6815f9babe43` |

The `ast.get_source_segment` bytes for `run_tests.py:test_applied_physics`
hash to `88425be14b1141ac9377759ff9cd72a9e646a90f13d00c7627c69d4c53dc2d9a`.
Only this group was reserved for the repair; unrelated existing runner work
was preserved. All RI-11/registry source reservations are released.

The next independent coordinator task is RI-12's small data-identifiability
contract before a measured pilot or RET changes. Actual data, independent
noise calibration, policy comparison and RET owner coordination remain later
dependencies. The hourly follow-up remains active. No RET source/bank,
historical review/table values, release thresholds, staging, commit or push
was changed in this acceptance cycle.

Final documentation verification checked **32 local file links** across the
master plan, progress, application plan, runner guide and applied-physics
document: no missing targets or trailing whitespace. Scoped tracked whitespace
checks also passed. Current active ownership remains QR's new RI-08c bundle,
maps and handoff; the coordinator's next independent item is RI-12.

**RI-08c acceptance and eleventh registration — 13 September continuation**

The coordinator read the complete
[repeatable-instrument proof](../validation/t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md),
inspected the new branch, record, mixture and terminal-type implementation,
and reviewed an independent mathematical/source assessment. No blocker remained.
Root separately replayed all **28** new checks normally and with `-O` while
checking the three handoff pins before and after; all passed without drift.

The general exposed-ray lemma is the substantive result: if a positive
real-linear branch on the full generating source cone has calibrated mass
effect e and perfectly repeatable outputs, and the repeat face is the ray h,
then the full signed-space map must be `B=e⊗h`. On this six-dimensional
candidate cone, the rank-one quotient face forces output c=0. This is a
consequence of positivity and the output-face premise, while complex input c
remains allowed. Faithful mass forces the entire zero raw output when e=0.
The rank-one quotient update follows after that proof.

The branch stays in the same cone and preserves complete probabilities under
finite serial/known-record feedback. The fixed-frame control word acts once
on the current residual. A positive commitment stores the actual word, axis,
outcome, frame, controller and full precursor, then clears only the pending
word. Old literal cuts remain terminal with their separately defined target
effects; no return/reset operation is inferred. Nonrepeatable positive resets
and larger-range literal cuts show why the added premises matter.

Starting at the supplied maximally mixed section, fine-history conditioning
with these controls and Pauli outcomes reaches exactly seven residual states.
Explicit classical randomization permits record-blind marginals in the
stabilizer octahedron; selectors and component histories remain available.
Those marginals cannot replace the joint ensemble for selector-aware feedback.
Rational weights give rational-coordinate points; real weights give the closed
octahedron. Neither this set nor the mathematical Bloch ball establishes full
physical preparation richness. The universal proof is distinct from its
finite witnesses and from the new operations' physical availability.

| Accepted RI-08c source, in `t8-q-repeatable-record-instrument-2026-09-13` | SHA-256 |
|---|---|
| `REPEATABLE_INSTRUMENT.md` | `7870bfa7549cb134a6dea54cd1b98ef3451736067ad6ebe6a86498576a40a62c` |
| `model.py` | `173ad68ab8be40036a28e2806bfdb03dde8bd42030772a41084736d31e05fb86` |
| `check.py` | `302ee08be226fab9d89d0031277e2357d71cfb5f9d0c56d6a6662681759f5677` |

The new `repeatable-record-instrument` registration changes only the registry,
its inventory regression and the runner guide. Removing the appended object
and reproducing the existing JSON serialization recovers the tenth manifest
hash above; its ten earlier objects are preserved. The runner is unchanged.
Root reran **40 registry regressions**, then **177 witnesses per mode across
11 suites**. All **18** declared executable sources loaded. Both executions
reported `successful=true`, `source_check_before=matched`, empty unexecuted
source/drift lists and `runner_source_changed=false`. These two modes repeat
the same witnesses. QR's separately reported 204 scoped tests overlap this
inventory and are not added to it.

| Eleventh-registration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `30f3ba85172e10fb0e235a978318d327b409b3bffa0e5e1cb7a1e2a493d1765a` |
| `scripts/run_research_checks.py` | `0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613` |
| `det8/tests/test_research_registry.py` | `f023fd7cdc93e6b6f189d0481d17c3e83df3e17abb30a46809d759841ab4aea8` |
| `docs/RESEARCH_CHECKS.md` | `ed877052500dea479fa338e0ebabdadd84d25405626f7f20d9450d30143f91b8` |

**RI-12 exact design-identifiability contract accepted**

Added [the exact helper](../../det8/applied_physics/identifiability.py),
[independently authored tests](../../det8/tests/test_applied_identifiability.py)
and [the theorem/interface note](IDENTIFIABILITY_CONTRACT.md). For a declared
rational mean map H and linear target q on unrestricted real parameters, the
helper returns either exact row weights `λᵀH=q` or an exact null direction
`Hδ=0, qδ=1`. Results retain detached immutable input coefficients and coordinate
order. Every candidate is analyzed separately against the base design. A
measurement can separate the displayed pair while leaving the target
unidentified; combined measurements need a fresh combined-design analysis.

Root reviewed the elimination proof and implementation and the independent
substitution/inverse-based tests. Root replay passed **162 focused tests**:
108 new identifiability cases plus 49 applied-comparison and five operational
cases. The independent test author also passed the 108 new cases under `-O`.
Root's scoped Ruff check passed. The input envelope is eight parameters,
32 base rows, 16 candidate rows and 64-bit reduced input coefficients; derived
exact witnesses are not rounded or truncated to that bit bound. Containers
are consumed once with bounded materialization. Floats, booleans and malformed
inputs are refused. A measured dense boundary benchmark motivated this small
envelope, without promising a fixed latency.

The helper proves structural identification, not finite-noisy-data certainty,
conditioning, physical feasibility, causal explanation or action utility. A
proper prior can supply finite uncertainty in a direction the data do not
identify. The single-channel comparator is a new explicit example: the existing
RET apparatus supplies two axes at distinct reference levels and can already
have rank two in one fully observed action. Its behavior is not misdiagnosed
as single-level ambiguity.

| Accepted RI-12 source | SHA-256 |
|---|---|
| `det8/applied_physics/identifiability.py` | `136588b80cc9d1935137c81885dc26446947dc52f81c120a0652a75b7fb268d9` |
| `det8/tests/test_applied_identifiability.py` | `896951787410eb9a286591720f5659f7ffe3a357bdf32342941d90108d201088` |
| `docs/coordination/IDENTIFIABILITY_CONTRACT.md` | `a519949a308a77269574de1971eeb869739d86074ed0ead5ebf2f04eb7f6a219` |

All RI-12 and registry source reservations are released. The next coordinator
item is an isolated synthetic public-API comparator fixture outside RET source.
The [application plan](APPLICATION_WORK_PLAN.md) now records actual observed-row
and parameter-order bindings, multi-axis action blocks, parameter uncertainty
versus predictive noise, and the current policy objective's limits. It also
records held-out raw-source identity and shared-noise obligations: separate
source hashes must represent actual separate captures, not invented independence.
SDK source changes require owner coordination; real data and benefit evaluation
remain subsequent dependencies. No real pilot or G2 closure is claimed.

**Next QR assignment: RI-08d ancillary compatibility**

Acceptance and the following bounded assignment were delivered to the existing
Quantum Relativity task. This is a proposed theorem under added premises,
awaiting proof and coordinator review.

Use the full local `D(A,c)` cone, compose with an independently prepared known
reference section `B=(I+tZ)/4`, and explicitly regroup the full 16 event labels
into four joint cells. In untwisted coordinates supply the common joint-system
lift of `U=(I⊗H) CNOT`. The candidate cross-cell form is `tc`: the coordinator
independently checked the t=1 coefficient with exact arithmetic. If correct,
joint recordability for a nonzero calibrated polarization excludes every
nonzero complex c, while the c=0 section remains lawful for every A≥0.
Classify the maximal surviving **local** subcone relative to this fixed
composition interface, without postulating the whole composite state space.

Required countercontrols are local product controls and a maximally mixed
reference, neither of which should exclude c in the stated single joint test.
Preserve reference/input histories, full residual payload, actual coupler
metadata and precursor dependence. Product preparation, independence, coupler
availability and joint viability are new explicit premises. Earlier image-cone
reconstruction and coherent-readout algebra work already imposed narrower
cones; they did not establish this exclusion of the larger c sector.

This assignment does not establish native entanglers, arbitrary ancillary
complete positivity, all composites, full preparation richness, field
selection or quantum advantage. Approximate-repeatability robustness remains
a separate queued question. QR must return a proof or precise obstruction,
independent witnesses and source pins before another successor is assigned.
The hourly coordination follow-up remains active. The original review,
accepted QR source bytes, RET source/banks, historical evidence and release
thresholds were preserved; nothing was staged, committed or pushed.

Final coordinator documentation checks found **40 local file links**, all
resolving, and no trailing whitespace across the master plan, progress,
application plan, new contract and registry guide. Final RI-12 and registry
source hashes match the tables above. The coordinator also reconstructed the
previous ten-entry manifest and independently recovered its historical hash.

QR acknowledged RI-08c acceptance and RI-08d on the existing thread. Its new
reserved bundle is `docs/validation/t8-q-joint-recordability-2026-09-13/`,
with separate proof, model and test work in progress. Its preliminary check
reports opposite cross forms `tc` and `−tc`: their cancellation can preserve
total mass despite failure of exact recordability. The handoff must therefore
distinguish a normalized prospective kernel from a lawful source. This is a
new proof obligation under review, not an accepted RI-08d conclusion.

**RI-08d acceptance and twelfth registration — 13 September continuation**

The coordinator read the complete
[joint-recordability proof](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)
and inspected the explicit native tensor, signed permutation, prospective
validation and terminal source-cut implementation. A separate mathematical
review independently rederived the result; an additional source/record audit
passed 14 behavioral probes normally and with `-O`. No mathematical or
transition/source-cut blocker remained.

The theorem retains every local `D(A,c)` input initially. Its independent
product with the declared reference is PSD, normalized and exactly recordable.
The specified native lift produces cross forms `tc` and `−tc`, with conjugate
reverses and all other off-cell forms zero. A nonzero real reference
polarization therefore removes precisely the two real c directions, leaving
every positive A with c=0. This is maximal **local** subcone selection relative
to that fixed additional interface. It is not selection of a complete
composite state space, physical measurement of c, or a dynamics removing c.

The opposite cross forms cancel in total mass. Thus a c≠0 prospective output
can remain PSD and normalized while being inadmissible for the joint record
partition. The implementation preserves that full 16-label kernel as data and
refuses lawful promotion/commitment. All c=0 states survive every common shared
unitary algebraically, without granting availability. Universal countercontrols
show why local product controls, a maximally mixed reference, and CNOT alone
do not provide this exclusion. SWAP changes total-entry mass off the surviving
domain while preserving ordinary trace. The transpose/conjugation convention
for the surviving joint quotient is explicit.

The full origins, separate input histories, reference orientation/polarization,
independence declaration, permutation and coupler metadata survive. Joint
precursors retain origin tags, so equal integer event IDs are not merged or
given an artificial cross-origin causal order. A positive terminal residual
must equal the exact full normalized source cut; a nonzero zero-weight cut
cannot be committed. Snapshot construction proves declared grammar/cone
validity, not trajectory reachability or empirical independence.

The additional record audit found that numerically equivalent float/bool
permutation entries were retained as metadata. QR kept the existing equality
check and now stores the canonical built-in-integer permutation in both
snapshots and records. One-shot inputs remain supported. This correction does
not change the theorem or arithmetic, and its regression extends an existing
case rather than increasing the count. Root inspected the exact repair and
replayed all **28 final checks in both modes**, with the final pins matched
before and after. QR's earlier 232-case wider replay predates this narrow
repair; it is not represented here as a new full replay at the final pins.

| Accepted RI-08d source, in `t8-q-joint-recordability-2026-09-13` | SHA-256 |
|---|---|
| `JOINT_RECORDABILITY.md` | `34d7fb69bc72764de2d0ee239ee5af3f132ec37247d67e6674a41f98e0beb444` |
| `model.py` | `666d3366e9b1be24d3b930973bb82b478a7af7901fe5b1321aecc06e47d26c30` |
| `check.py` | `f088d2e99379d4ad6e852d4157b78760a50351cd74e48f690cab364b5a7f92c9` |

The twelfth `joint-recordability` registration changes only the registry,
its inventory regression and the guide. The eleven earlier objects remain
byte-identical: root removed the appended object in memory, serialized the
previous inventory and recovered the eleventh manifest hash recorded above.
No runner or import-policy change was needed.

Root replay passed **205 finite witnesses in each mode across 12 suites**, with
all **20** declared executable sources loaded, `source_check_before=matched`,
no unexecuted sources or observed drift, and `runner_source_changed=false`.
All **40** registry regressions passed within the 236-case command below.
Repeated modes and overlapping QR scoped checks are not additional independent
proofs, and these checks do not establish the supplied physical premises.

| Twelfth-registration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `87c5bc7faf07bf4b08e9872d33991be1205ad063f10f903c1d1df36c3e53c02f` |
| `scripts/run_research_checks.py` | `0c1e8f00971a509e8b354f9e2cdecd400175688e7a41b4deea34c3894cb1c613` |
| `det8/tests/test_research_registry.py` | `35f27f65c431650d399c2187e0d1b5ad11f6192d714e414ab4a0ef740c2e4dfb` |
| `docs/RESEARCH_CHECKS.md` | `760ea4e04bec708660cee05635cdbca9097d66ae35c3ee6ba1ac57cc88d3b729` |

**RI-12 synthetic public-API comparator fixture accepted**

Added [the comparator fixture](../../det8/applied_physics/comparator_demo.py),
[independent tests](../../det8/tests/test_comparator_demo.py), and
[the explanation and exact Gaussian oracles](COMPARATOR_DEMO.md). It consumes
only public RET contracts and inference/replay functions. It writes no result
files, accesses no private posterior, and makes no workflow/closure decision.

The fixed single-channel example uses `y=gx+b`, proper independent prior
`(g,b)~N((1,0),I)`, known observation variance 1/4, and references −1, 0, +1.
Its two branches add either a repeated +1 reading or a distinct −1 reading
after the same first reading. Predictions and parameter comparisons are
conditional on the named gain/offset model; the required open alternative
remains present. The fixture does not imply model-family selection.

Repeated +1 readings reduce same-level mean variance from 2/9 to 2/17 while
structural rank stays one and the unseen −1 target remains unidentified.
Adding the distinct reference gives rank two; both parameter variances remain
1/9. Public future-prediction covariance includes the known 1/4 observation
noise, which is separately removed for the named model's mean variance.
Independent exact two-by-two batch inverses verify the SDK's sequential
Gaussian summaries and predictions. The full analytic covariance matrices
are test oracles, not private SDK fields exposed by the fixture.

Every exact design row binds an actually assimilated observed axis to its
record digest, action, source hash, reference and parameter order. Proposed
candidate rows remain prospective. Four retained validation records leave
the posterior, model probabilities and structural design unchanged. Seven
actual deterministic synthetic byte strings cover the two branches, and both
branch manifests replay with their exact byte subsets. Tests separately verify
raw JSON/evidence semantics; hash identity alone is not an extraction proof.
Corrupt, missing, extra and inconsistent replay data are refused.

These fixed dyadic values are arithmetic fixtures, not Gaussian draws or
physical captures. Repeated/distinct branches do not establish counterfactual
experimental replay, a calibrated apparatus, target-optimal policy or measured
benefit. Distinct synthetic source hashes do not establish physical noise
independence. The existing two-axis RET apparatus is unaffected.

Final root command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_comparator_demo.py det8/tests/test_applied_identifiability.py \
  det8/tests/test_applied_comparison_contracts.py \
  det8/tests/test_operational_scripts.py det8/tests/test_research_registry.py -q
```

**236 passed:** 34 comparator, 108 identifiability, 49 applied-comparison,
five operational and 40 registry cases. The independent comparator test author
also passed all 34 new cases under optimized Python. Root read the complete
fixture, note and tests, checked final hashes, and passed scoped Ruff. This is
focused integration evidence, not a full SDK release or G2 calibration run.

| Accepted comparator source | SHA-256 |
|---|---|
| `det8/applied_physics/comparator_demo.py` | `594c1ae0899fd89eb68816d536d744ca1c9c17def9073fc8a3b91d70f866d751` |
| `det8/tests/test_comparator_demo.py` | `2a2185761135329bceafcb76fe595e89c5536dfe3df934e3fec216177d359958` |
| `docs/coordination/COMPARATOR_DEMO.md` | `7023a20a71b030ba7009d12e196e69963ebe9bd62568d8619fb596108529ef92` |

All comparator and registry source reservations are released. Root compared
the 40 RET Python files before and after verification: the sorted-path/content
aggregate SHA-256 remained
`0145cd88412c1673372716db28d0ed2ad5f0187e030f074d9656fd374f720bba`.
No RET source/bank, accepted identifiability helper, protected evidence or
release threshold changed. The measured instrument/dataset question has been
put to the user and remains open; no missing data is silently replaced by a
measured-success claim.

**RI-08e assigned and acknowledged; RI-13 next independent work**

QR acknowledged final RI-08d acceptance and is working in
`docs/validation/t8-q-repeatability-robustness-2026-09-13/`, with separate proof,
model and exact-test work. The following are proposed targets, not accepted
conclusions or experimentally calibrated error bounds.

The first obligation is to reconcile domains. Imposing RI-08d's added composite
viability leaves C0, where c=0 and Φ is injective. The candidate classification
asks whether positivity and exact rank-one input-effect calibration already
force a measure/prepare branch `B=e_Q⊗h_Q` on C0, before repeatability is imposed.
On the broader local-only C cone, approximate branches may instead depend on
the invisible input c. Such a counterexample cannot be used as a lawful
nonzero-c input while simultaneously imposing RI-08d's extra premises.

For an assumed uniform repeatability defect ε≤1/2 on the entire declared cone,
the proposed sharp one-step raw trace-norm bound is `2p√ε`, with full zero output
when calibrated branch mass p=0. A separate broader-C output bound is
`|c_out|≤εp/2`; C0 range instead requires c_out=0. The finite-protocol target
compares identical initial states and known-history controllers, retaining all
records and subnormalized residuals. It distinguishes a proposed residual
trace-norm bound `min(2,2N√ε)` from a classical record-law total-variation bound
`min(1,(N−1)√ε)` for at most N≥1 tests. Ideal suffixes and approximate prefixes
must justify contraction without assuming approximate complete positivity or
quotient descent. A sharper Pauli/Clifford coupling bound is optional and must
be proved separately; no optimal general horizon rate is presumed.

Exact witnesses must include nonuniqueness, sharpness, broader-C hidden-payload
dependence, zero branches and finite feedback/early stopping. No finite test
establishes the uniform physical ε premise, ancillary diamond norm or an
unbounded-stopping theorem. QR must stop at a source-stable reviewed handoff.

The next independent coordinator item is RI-13: consolidate the accepted
theorems into a domain/premise/operation compatibility ledger. In particular,
larger and smaller input cones, terminal and reusable outputs, and local and
composite availability cannot be merged by collecting green test counts.
The hourly follow-up remains active. The original independent review and
accepted source history are preserved; nothing was staged, committed or pushed.

Final documentation verification checked **48 local file links** across the
master plan, progress, application plan, both application notes and registry
guide: all resolve. Those documents and the new comparator source/test have
no trailing whitespace; scoped tracked whitespace checks passed. QR's current
handoff confirms RI-08e is in progress under the reserved new bundle.

**RI-13 accepted — operational premise and composition ledger**

The coordinator wrote [OPERATIONAL_PREMISE_LEDGER.md](OPERATIONAL_PREMISE_LEDGER.md)
from the accepted statement sources, public claim/status contracts and the
application evidence. Three independent read-only preparatory reviews covered
the predecessor cone/limit results, local-to-joint compatibility and project/
application boundaries. Two reviewers then examined the complete ledger.
The final document has 28 local link occurrences, all resolving to existing
sources, and SHA-256
`4a2435e19a114e50c484b9ebe834a3dd9fb5dbf68dff911435f8f50891bee509`.

The ledger distinguishes full PSD, maximal recordability, chosen classical
cones, local C, composite-compatible C0 and the four-dimensional fixed joint
image. It records that C0 is not a face of C and that each ideal Pauli branch
reaches one ray, not all of C0. It separates exact mathematical quotients from
available operations, full preparation richness and executable state conversion.
The finite protocol constants explicitly assume a normalized common input;
unnormalized raw bounds scale with mass. These review corrections were applied
without changing any accepted QR statement or code.

A conditional local-tree/reference/joint-terminal composition corollary states
its complete mass accounting and source-range conditions. It is not an accepted
cross-bundle software adapter: full words, controller/frame, origin-tagged
records, precursors, independent-reference preparation and terminal payloads
still need a lossless interface. Local faithful zero branches and joint
nonzero zero-weight cuts remain distinct. RI-07's finite full committing-label
and faithful output-mass premises cannot be inferred from local C0 alone or
met by discarding an unbounded retained control word.

Public supported-core, experimental research/helpers, unvalidated RET preview,
historical source-bound G1 and open G2 remain separate. The current generated
claim summary still matches `det8.claims` (`export_claim_registry.py --check`
passed). The next independent item, RI-14, will add scoped authorization and
accepted-artifact metadata alongside the broad claim registry, preserving its
evidence/support boundaries. Its source reservation has not yet begun.
RI-13's file reservation is released. No extra code tests were introduced for
this document; proof/source review and link/format verification are its checks.

**RI-08f assigned and acknowledged — joint return range and question granularity**

After RI-08e proof/source acceptance, the coordinator assigned a new isolated
joint-repeatability bundle to **Quantum Relativity**. QR acknowledged the
scope and source reservations and will stop at a source-stable handoff. The
candidate is not registered or accepted as a completed QR result.

An independent coordinator derivation and 65 exact cross-checks of the accepted
RI-08d model suggest that fixed-image full-cell effects pull back to
`E_ab=(I+(-1)^b t Z)/4`, independent of a. Thus their normalized maximum is
`(1+|t|)/4`, and a calibrated positive branch returning to that same image has
candidate minimum uniform relative repeat defect `(3-|t|)/4`. Algebraic
measure/prepare branches appear to attain it, but map existence does not supply
physical reset or reusable-operation availability. The error denominator is
branch mass; normalization by original input mass gives a different bound.

The coarse subsequent question b has candidate defect `(1-|t|)/2`, while the
full actual record remains (a,b). QR must independently prove or refute the
bounds, exact effects, sharp complete positive attainment and history/domain
contract. Changing a question is distinct from erasing a committed record,
rereading classical memory, changing the coupler/reference or enlarging the
return cone. At t=0 the candidate K_t denotes the c=0 section image; no local
c-exclusion is inferred from RI-08d with an unpolarized reference.

The hourly follow-up remains active. The measured instrument/dataset and
frozen application objective remain open; other unblocked work continues.

**RI-08e accepted and registered — final robustness evidence**

Root read the complete proof and implementation, reviewed the independent
rational norm/leaf checks, and replayed all 29 new checks normally and with
`-O`, with matching before/after source pins. Two independent read-only
reviews found no blocker in the C0 branch classification, broader-C
counterinstrument, full signed raw norm argument, ideal-suffix hybrid,
Clifford/Pauli coupling bound or complete record/zero-branch contract.

Additional independent probes exercised record-dependent early stopping
reachable only in the approximate model, asymmetric leaf supports, ε=0 and
ε=1/2, and refusal to round an irrational trace norm. At ε=1/5, one new
three-test policy had exact record TV 9/25 and full raw leaf error 122/125.
These probes are separate finite review evidence, not added to the registered
witness count and not an empirical uniform-error certificate.

The accepted primary C0 classification assumes full-span real-linearity,
whole-cone positivity, exact rank-one effects and same-cone range. It forces
`B̃=e_Q h_Q` before repeatability; ε>0 permits a cap of normalized targets.
On broader local-only C, hidden input c can instead affect later quotient
predictions. Those nonzero-c sources cannot be simultaneously admitted under
C0 composite viability. The raw bound `2p√ε`, separately sharp output-c bound,
finite raw bound `min(2,2N√ε)` and full-record TV bound
`min(1,(N−1)√ε)` retain their distinct scopes. Finite-protocol constants assume
a common normalized full initial state, declared catalogue and shared
known-history controller. The sharper catalogue bound does not claim optimality
for arbitrary longer horizons. No ancillary or infinite-history result follows.

| Accepted robustness source | SHA-256 |
|---|---|
| `docs/validation/t8-q-repeatability-robustness-2026-09-13/ROBUSTNESS.md` | `071187b895bc159dfdc2107dddbcd009364c0b2e3e21858fce7c441fece03d22` |
| `docs/validation/t8-q-repeatability-robustness-2026-09-13/model.py` | `61ca79626aeaa77a81638076ea28ae1eaef4ee929d809fe8376227d8ddef627d` |
| `docs/validation/t8-q-repeatability-robustness-2026-09-13/check.py` | `fd0e6fce4cd1d093c7339587e723d3a1bacaf876ccd4d9c6ac5ad3a32037055e` |

The thirteenth `repeatability-robustness` registration includes the complete
local model/check import closure. The runner's only code change adds `math`
to the exact module allowlist for `isqrt`. New regressions require its declared
closure, execute an exact large-integer square root in normal/optimized modes,
and reject `math.fake`; snapshot, path, drift and side-effect guards remain.
All twelve prior registration objects reconstruct the preceding manifest bytes
with SHA-256
`87c5bc7faf07bf4b08e9872d33991be1205ad063f10f903c1d1df36c3e53c02f`.

Root made the normalized-input premise explicit in the new manifest summary
and guide, then verified the final identities below. Final root commands:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_research_registry.py -q
.venv/bin/python -B scripts/run_research_checks.py --all
.venv/bin/python -B scripts/run_research_checks.py --all --optimized
```

**43 registry regressions pass. All 13 suites pass: 234 finite witnesses and
22 loaded executable sources per mode.** Both final runner reports give
`source_check_before: matched`, `source_changes_after: []`,
`runner_source_changed: false`, zero skipped tests and no unexecuted declared
sources. Normal and optimized modes repeat the same witnesses. The owner also
reports 261 distinct scoped QR checks per mode; that is a different inventory,
not another quantity to add to 234. No full application/SDK matrix was rerun
for this isolated research registration and documentation consolidation.

| Final integration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `212459d6ee478e3553db73b92069fb88802065108f3508a238a3072bc4494607` |
| `scripts/run_research_checks.py` | `35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f` |
| `det8/tests/test_research_registry.py` | `d5b4e09ddc4502b0f3824c9dde0443a36a655f23fb1b1bfca980f236fbd4b4c0` |
| `docs/RESEARCH_CHECKS.md` | `0cd9e610bf7dba2d5935c36f4393ce6026ea1e40b0bbe45defd908cf9258f398` |

All registration implementation reservations are released. Earlier accepted
bundles, the original independent review, RET sources/banks, protected evidence
and release thresholds were not edited by this cycle. Nothing was staged,
committed or pushed. Current next work is RI-08f in QR and RI-14 for coordinator
integration, with the user's measured-application choice still open.

Final documentation verification checked **81 local links** across the master
plan, progress, operational ledger, registry guide and three application
contracts/plans: all resolve. No trailing whitespace or malformed ledger table
rows were found. Root Ruff check/format and scoped tracked whitespace checks
passed. The final ledger hash still matches its acceptance record.

**RI-08f accepted and registered — same-image joint repeatability**

Root read the complete proof/model and relevant independent exact certificates,
then passed all 30 new checks normally and under `-O`. The three final source
pins matched before and after. A separate mathematical reviewer independently
verified the general first-effect/next-question lemma, effect pullbacks,
maximizing-face uniqueness and every normalization coefficient. A separate
implementation audit passed 340 additional explicit checks per mode, including
adaptive early stopping, complex inputs, singular references, negative signed
branches, provenance mismatch and nonzero zero-weight literal cuts. These
review probes are not added to the registered witness count.

For fixed K_t, full-cell effects have maximum `(1+|t|)/4`; full repeatability
therefore has relative defect at least `(3-|t|)/4`. The next-b question instead
has relative optimum `(1-|t|)/2`. The general e/g lemma distinguishes relative
optimum `1-beta` from original-input-mass minimax `alpha(1-beta)`. The three
input-mass coefficients are `(1+|t|)(3-|t|)/16` for full repetition,
`(1-t^2)/8` for next b after one fine branch, and `(1-t^2)/4` after analytically
summed first-b branches. The actual fine histories remain separate.

Nonzero-t relative optimality uniquely selects aligned-ray reset branches.
At t=0, scaled identity branches are optimal non-resets; weighted dephasing
at interior t separately shows that input-mass minimax does not imply that
uniqueness. Exact whole-image inversion works at both singular endpoints.
Every nonzero literal cut lies outside K_t, including some zero-weight cuts.
The supplied same-image return fixture adds algebraic operation availability;
it does not infer a physical reference reset or repeated coupler. No full
composite theory, automatic RI-08e extension or physical promotion follows.

| Accepted RI-08f source | SHA-256 |
|---|---|
| `docs/validation/t8-q-joint-repeatability-2026-09-13/JOINT_REPEATABILITY.md` | `4dd17ccb2900a888f7e7f7362c1a9e84d168c9cb636d59fbb9290a4e0354cd2a` |
| `docs/validation/t8-q-joint-repeatability-2026-09-13/model.py` | `6c07d351a03159ca9963ec8d86eac1af0f7ed995c20aac18a9e347a8a3882386` |
| `docs/validation/t8-q-joint-repeatability-2026-09-13/check.py` | `23cf5654c05033b167075c237fa1fb7afdaaea3815cc5dd9e09da6e4d3abce40` |

Root reviewed the fourteenth registration and replayed all suites after the
source-quiet handoff. **264 witnesses pass in each mode across 14 suites**,
with all 24 declared executable sources loaded, no skips or omitted sources,
`source_check_before: matched`, `source_changes_after: []`, and
`runner_source_changed: false`. All thirteen prior entries reconstruct the
preceding manifest SHA
`212459d6ee478e3553db73b92069fb88802065108f3508a238a3072bc4494607`.
The runner remains unchanged. QR's separately reported 291 scoped checks are
a different inventory and are not added to the registered total.

| Final fourteenth-registration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `68f3c5737d2513732e3193ee410ee6f607d60cbbef783612fc140404f6909f47` |
| `det8/tests/test_research_registry.py` | `0fc3b091e4dcd94edb0caf70c1dc661453b3c3a3847089ee166a668e1bda2c16` |
| `docs/RESEARCH_CHECKS.md` | `01e82f454e2caf134a205113332924aa439eba77dd6c23fe188a06264927becc` |
| Unchanged `scripts/run_research_checks.py` | `35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f` |

**RI-14 accepted — scoped authorization alongside existing public claims**

The new `det8.claims.research_activity_document()` returns versioned native
JSON with one bounded research authorization and fourteen explicitly listed
accepted suite/statement references through RI-08f. Private frozen records and
tuples back fully detached output. It performs no filesystem discovery,
research import, execution or source verification. The existing research
registry/runner retains the actual statement/source pins. New directory or
manifest entries do not automatically join the accepted collection.

The generated claim summary now displays the scoped quantum/record and
mass/geometry/gravity authorization alongside unchanged broad evidence and
development statuses. Retired κ-gravity, the primary sequence, source-bound
historical G1, open G2/later gates, experimental research and RET preview
boundaries remain explicit. No public-core scientific claim is promoted.

Existing ClaimRecord and ModuleClassification shapes, classifications and
legacy document contents are unchanged. Root independently reproduced their
canonical JSON identities (`sort_keys=True`, compact separators):

| Existing output | Unchanged SHA-256 |
|---|---|
| `claim_summary()` | `6d763bf478f9268d9e1ce235beef81c32cb980641cf58f5e42c06e7e172c1c32` |
| `registry_document()` | `f7e11f82a3a6b6f46c485ccede9d6ad82a1d5dbf957272f4fbcf03c255e01e2c` |

An independent final audit accepted metadata immutability/detachment, all
fourteen references and source bindings, authorization/evidence boundaries,
and stdlib-only isolated loading. Returned documents have disjoint mutable
container graphs. Tests mutate every nested container and verify a fresh
response is unaffected. Normal/optimized isolated checks deny file access and
reject research imports. Existing retirement and supported-facade tests remain.

Final root focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_claim_boundaries.py det8/tests/test_claim_summary.py \
  det8/tests/test_research_registry.py -q
```

**64 passed:** 21 claim-boundary/generated-summary cases and 43 registry cases.
The independent metadata reviewer also passed eight targeted checks. This is
focused metadata and research-runner evidence, not a new full G1 source closure,
a wheel/release matrix or RET calibration run. The existing summary test was
not edited. All four RI-14 source reservations are released.

| Accepted RI-14 source | SHA-256 |
|---|---|
| `det8/claims.py` | `25030d058f6b05d36152e06ee6dff5dc2bdf2073cccace2b94b10c7f853768a4` |
| `scripts/export_claim_registry.py` | `3e5ecae69905e6daa6ebdf925ffb2157455c6b66090bf8e5e60bad3aa1021717` |
| `docs/CLAIM_REGISTRY.md` | `f7d97a84c646c6dc877d67d97fcb23c2a1b06c9d29453a814a1e27ed0aa1a078` |
| `det8/tests/test_claim_boundaries.py` | `476de890f2de76be5dd082babbb42fbb2fa9753e59aee643a5941f373702b46a` |

**RI-08g acknowledged; RI-15 next coordinator integration**

QR acknowledged the new isolated cut-closed-completion obligation. It will
independently investigate the proposed minimal convex cone L_t with four
independent PSD2 image blocks, on which literal cuts would become reusable
because the declared return range changes. Candidate results distinguish
interior faithful mass/compact bases from endpoint nonfaithfulness, cut-only
four-weight equivalence from the larger interval of effects `0<=e<=m`, and
fixed-t compactness from the mass-one raw-trace blowup `1/(1-|t|)`.

The coordinator and an independent reviewer derived the candidate before
assignment. It is not an accepted new bundle. The endpoint positive zero-mass
subcone, common effect kernel and kernel of mass have candidate dimensions
4, 12 and 15 respectively; these are not interchangeable. The task must keep
nonzero zero-probability cuts, full native payloads, actual fine outcomes and
original source/reference provenance, and state RI-07 applicability only
under its separate finite-label/controller hypotheses. No physical reset,
new coupler or unavailable control is inferred. QR stops at a source-stable
handoff without starting a successor.

The operational ledger has been updated through accepted RI-08f and RI-14,
with RI-08g clearly labeled as under development. RI-15 is the next independent
coordinator item: specify and implement one bounded exact local-to-joint
interchange contract, preserving existing sources and full histories rather
than treating duplicated classes as already interoperable. Reserve exact
implementation files before editing. The measured-application dataset/objective
question remains open; hourly follow-through is active. No RET source/bank,
protected evidence, accepted QR source or original independent review was
edited by this cycle; nothing was staged, committed or pushed.

Final cycle verification: all **126 local file links** across the master,
progress, operational ledger, research guide, generated claim summary and
application plans/contracts resolve. No trailing whitespace or malformed
ledger table rows were found. Export parity, scoped Ruff check/format and
tracked whitespace checks pass. The updated operational ledger SHA-256 is
`4a3fd4db83c8f960eb7ace1dbfa947c5f041dd433d169e618871f5837ef68cd9`;
its earlier acceptance hash remains historical above.

**RI-08g accepted — changed return cone and polarization boundary**

Coordinator read the complete [cut-closed-completion argument](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md),
reviewed its block reconstruction, effect, cut and history implementation, and
received an independent full proof/source audit. The minimal convex cone L_t
contains four independent PSD2 blocks in the fixed native frame, has real
span 16, and is closed under complete repeatable literal cuts. Minimality is
constructive using finitely many cuts and positive sums; arbitrary physical
preparation of those blocks remains an extra premise.

The full native inverse/reconstruction matters even at t=0 and ±1. Positive
mass and block weights alone can admit a false fixed-reference image. The
accepted domain tag cannot be substituted for the older K_t return type.
Raw completeness includes every zero-weight cut, although nonzero such cuts
cannot be normalized or committed. Endpoint positive-branch ensembles may
therefore omit a nonzero dark remainder from the original raw state.

The whole-cone effect interval is exactly `0≤F_ab≤E_ab` blockwise. It spans
16 directions in the interior and collapses to four weights at endpoints;
endpoint common effect kernel, positive dark span and mass kernel dimensions
are respectively 12, 4 and 15. A fixed cut/read/stop catalogue has only the
four-weight information even in the interior. Normalized future probability
equivalence requires the same full prefix/context; unnormalized source
weights also retain total mass. Availability of all mathematical effects or
the positive quotient section is not inferred.

The sharp mass-one raw-trace witness `1/(1−abs(t))` proves loss of uniform
compactness near an endpoint. Interior RI-07 applications still need its
other controller, finite-full-label, branch and faithful-output premises.
Endpoint quotient results cannot be used to infer an original raw limit.

Root passed **32 bundle checks in each mode**, source pins unchanged. A
separate in-memory audit passed **147 probes per mode**, including mixed
reference block tampering, complex same-cell payload, endpoint dark
remainders and exact provenance/precursor refusals. The explicit endpoint
fixture has raw trace 7, positive-branch ensemble trace 5/2 and omitted dark
trace 9/2 while probabilities sum to one. These probes are not added to the
registered suite count. QR's 323 scoped checks are another separate inventory.

| Accepted RI-08g source | SHA-256 |
|---|---|
| `CUT_CLOSED_COMPLETION.md` | `23392a688924b6518e8a823f062ba87b0089c85f711f0a468f7d582b4b2897f9` |
| `model.py` | `356212757e27cbde1f63f6047b3f4395011d5816ffaaefe14453b1be2c3710ba` |
| `check.py` | `1e37921c80dba78bd424e22519c929080173ef49f2687fdfcd5914c7fd77e483` |

**Fifteenth registration and explicit accepted-reference update**

The new manifest entry preserves the fourteen previous objects exactly;
reconstructing their prior serialization gives the historical manifest hash
`68f3c5737d2513732e3193ee410ee6f607d60cbbef783612fc140404f6909f47`.
No runner or exporter code changed. The separate research authorization
metadata and generated claim summary now explicitly include the fifteenth
accepted reference. Canonical legacy `claim_summary()` and
`registry_document()` identities remain the RI-14 values recorded above.

Final coordinator replay passed **15 suites / 296 finite witnesses / 26
declared executable sources per mode**, normal and optimized, with no skips,
unexecuted declared source, observed source drift or runner change. The
focused registry/claim command recorded above passed **64 cases**. These
are research and metadata checks, not a new public-core closure or RET run.
All six registration/reference source reservations are released.

| Fifteenth integration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `5ec201d618252ba4d9992112a62170c4482f42a1ffd15a80d1e9af9235b84256` |
| `docs/RESEARCH_CHECKS.md` | `7be9f479c1d4b8293faaa0b320d969f24edde4d6900c9114e81d5807af65029e` |
| `det8/tests/test_research_registry.py` | `dfa94b4b447f32db98f211b6701a00be9da3243f86a81778b6f834f32657a067` |
| `det8/claims.py` | `e1cad35924ab93a962027140ac3f110ad43d4c21dc51d9dfa5b8bb92dea643cc` |
| `det8/tests/test_claim_boundaries.py` | `192d286f1a5765723528dd07e13e4e48248a9f590364ec747cb1b94359a21003` |
| `docs/CLAIM_REGISTRY.md` | `8ff60f3d920e760845dd591f5512fc1b261e6f5bdc4841d6b7034c35c75213ff` |
| Unchanged `scripts/run_research_checks.py` | `35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f` |
| Unchanged `scripts/export_claim_registry.py` | `3e5ecae69905e6daa6ebdf925ffb2157455c6b66090bf8e5e60bad3aa1021717` |

**RI-08h acknowledged; RI-15 implementation active**

QR acknowledged one isolated reversible-generator assignment after RI-08g
acceptance. The coordinator and an independent reviewer derived a candidate
classification under an additional continuous real-parameter group premise:
four weighted block-unitary generators at fixed interior t, with scalar
Hamiltonian parts canceling. It is not a selected Hamiltonian, physical clock
or accepted successor theorem. Retained command names do not make the
existing cut-only outcomes identify these generator parameters.

The assignment requires endpoint dark-dilation and one-sided dephasing
countermodels. A standalone transpose distinguishes disconnected positive
automorphisms, but does not isolate lack of continuity for an R-group:
divisibility already excludes its orientation sign. Exact rational rotation
witnesses check selected group elements, not a continuum of physical times.
QR owns only its new isolated bundle/maps/handoff and stops after delivery.

RI-15 proceeds independently in five newly reserved implementation/test
files. The agreed bridge wraps the exact original local snapshot alongside
the converted joint stages. It retains pending controls without applying
them twice and reports conditional weights only; previous branch-selection
weights are not present in the source snapshot. Full-C conversion must keep
the ancillary obstruction visible. The launcher uses explicitly pinned
aliases for the two existing `model.py` sources and changes neither accepted
bundle nor the registered runner. Independent tests and source audit are
active; no RI-15 acceptance is recorded yet.

**RI-15 accepted — exact conditional local-to-joint interoperability**

Five new files implement the [adapter contract](../validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md)
and independent checks. The original RI-08c `State` survives in an immutable
context through RI-08d product, coupled and terminal stages. Every exact real
and imaginary Fraction component is converted directly. Committed IDs,
settings and precursors survive, with axis/controller/source-kind/frame
fields represented explicitly in target-record payloads. The original local
object retains pending controls even with no earlier record. Those controls
have already acted on the residual and are not applied a second time.

Every target wrapper must match the complete forward construction from its
retained context. A separately valid PSD or recordable target cannot replace
the actual source. Nonzero complex c survives conversion: product sources
can be valid before polarized coupled promotion refuses their nonzero cross
forms. At t=0 the broader accepted source remains allowed. The full terminal
cut, full outcome and tagged input histories are retained; zero-weight cuts
cannot be committed and terminal wrappers cannot continue or reset.

Weights are conditional on the supplied normalized local/reference snapshots.
Neither recorded history nor textual reference provenance supplies the missing
earlier selection probabilities. The adapter does not claim a complete
weighted protocol, global preparation reachability, empirical independence,
new physical operation or supported core/RET interface.

The separate launcher pins both accepted model/statement versions, the new
adapter/check/contract and the existing runner. Fixed unique aliases solve
the two `model.py` basenames without copying or modifying either source.
Static closure uses virtual sibling names in memory; actual execution uses
captured original bytes and reports all four real source paths. A successful
run requires nonempty unskipped checks, exact loaded-source inventory and no
observed endpoint drift. The general registry/runner is unchanged; these 20
witnesses are not added to its 296-witness total at this checkpoint.

Root and a separate auditor read the adapter, launcher and contract. The
auditor passed **51 independent probes in each mode**, normal and optimized,
with unchanged captured-source pins. The independent test author supplied
**20 exact witnesses**, including equal residuals with different complete
histories, preserved distinct terminal records, native cut/weight oracles,
four conditional weights summing to one and no invented previous weight.
The final pinned launcher passed these in **26.750 s normal / 26.834 s
optimized**, below its 60 s per-run timeout, with all four sources loaded and
no failures/errors/skips/omissions or source changes.

Root's first complete regression run had **35 passes and one test-harness
failure**: the inventory test's global subprocess guard intercepted the
standard library's uncached `platform.platform()` call to `uname -p` on
macOS. Root isolated that metadata lookup in the test; no launcher, adapter,
contract, witness or accepted source changed. Final command:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_qr_local_joint_adapter.py -q
```

**36 passed in 54.12 s**, including fresh normal/optimized exact-source runs.
All five implementation/test reservations are released. This is focused
research-interface acceptance, not a wheel/release or RET calibration run.

| Accepted RI-15 source | SHA-256 |
|---|---|
| `scripts/run_qr_local_joint_adapter.py` | `50c742867a13693a402650360ab848dd8d36c7d92f040d70b6f55f84aea4678c` |
| `adapter.py` | `0d94c188cbff0ccfe92f7d3335c36bd5e638333b3d9b13c1d6f4ac00c9a0e8e6` |
| `ADAPTER.md` | `5d03f62504ae1ddc3b0bc1d30b7ef83ab58b228ab49dd72211e94a50ea571947` |
| `check.py` | `faab57484d8c8e05a924d37d8325c10ecbf4f325a1f91ee3af66163b5a2e9d94` |
| `det8/tests/test_qr_local_joint_adapter.py` | `a9635b842787033ffcfce9b4278250347f08206950cc0623a0d1607c26b9d365` |

The launcher also binds the original RI-08c/08d model hashes
`173ad68ab8be40036a28e2806bfdb03dde8bd42030772a41084736d31e05fb86`
and `666d3366e9b1be24d3b930973bb82b478a7af7901fe5b1321aecc06e47d26c30`,
their statements and unchanged runner `35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f`.
Runtime: CPython 3.11.6, macOS arm64, executable SHA
`033d83a12ab74b7bcade8248b1bca644f275d3965350b61fe485c2645e1f68e8`.

RI-08h arrived while this acceptance was underway. It was reviewed in parallel
without displacing the adapter task. Independent complete proof and source
audits found no remaining blocker, and 67 additional in-memory source probes
passed. The coordinator has reserved six existing registration/reference
files for its explicit sixteenth entry; final integration verification is
pending. QR remains at the source-stable handoff, with no successor started.

**RI-08h accepted — conditional generators and observation limits**

Root read the complete [generator proof](../validation/t8-q-reversible-generator-2026-09-13/REVERSIBLE_GENERATOR.md)
and the new source/type/record implementation. Two independent complete
proof/source audits accepted the result. Another **67 exact in-memory probes**
passed, covering both filter orientations, weighted congruences and tangents,
signed/foreign-image refusals and all eight endpoint dark-only block cases.
These probes are separate from the registry inventory.

The continuous all-real group premises, faithful filtering, block preservation,
Bloch-ball center argument and elementary integral generator proof are sound.
Each block has a Hermitian generator modulo scalar, giving twelve nontrivial
mathematical parameters. Mass preservation does not imply ordinary raw trace
preservation. Existing cut outcomes cannot identify these parameters under
the same context, committed prefix, initial pending/nominal metadata and common
finite history policy. Equal group elements do not erase known command words;
a pending-dependent stopping counterexample establishes the qualification.

Endpoint positive dark dilation, inverse-dephasing failure and the precise
continuity boundary are explicit. A standalone transpose cannot enter an
R-group simply by dropping continuity, since divisibility still excludes its
orientation and finite cell permutations. The additive discontinuous example
uses a choice-dependent Hamel basis and is not executable evidence. The
typed exact fixture is t=3/5 with six named common-X group elements; general
Hamiltonians, other unitaries and endpoint actions remain diagnostics.

| Accepted RI-08h source | SHA-256 |
|---|---|
| `REVERSIBLE_GENERATOR.md` | `fae1ebf0ddf2ab6e74d45c542ec3d7023752b68cc59f4cee4724134673c90b11` |
| `model.py` | `071bb9ca1cdca4aca6d37132ad48c6f8dd1f519bad181fe52c8fa1530c23eb2f` |
| `check.py` | `57289a41ec40e2a494c1c25426685ea1dda1aeb6f3ca1187c368a335974445fd` |

**Sixteenth registration verified**

The explicit new registry entry and claim reference preserve all fifteen prior
objects. Removing the sixteenth entry reconstructs prior manifest SHA
`5ec201d618252ba4d9992112a62170c4482f42a1ffd15a80d1e9af9235b84256`.
The runner, exporter, seven-module stdlib allowlist and both canonical legacy
claim JSON identities remain unchanged. The claim endpoint still performs no
filesystem discovery or research execution. The separate adapter is not
silently included in the general runner.

The implementer passed **64 focused registry/claim checks in 2.28 s**, export
parity, scoped Ruff and 66 guide/generated-summary links. Final root replay:

| Mode | Suites | Finite witnesses | Loaded executable sources | Result |
|---|---:|---:|---:|---|
| Normal | 16 | 326 | 28 | Passed; 101.496 s |
| Optimized | 16 | 326 | 28 | Passed; 101.779 s |

All **30 new RI-08h checks passed per mode**. No skips, expected failures,
omitted declared source, observed source drift or runner change occurred.
QR's 353 scoped checks are a separate inventory and are not added here.
All six registration/reference source reservations are released.

| Sixteenth integration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `cab559036fe724ad78edd0beb7565586eb506515d24e4dc0dd4544074677f939` |
| `det8/tests/test_research_registry.py` | `e02d1e58ff029d5bbf4671066a920ef9faf8b885c9ddcfe6db4a6f33fdaf1b88` |
| `docs/RESEARCH_CHECKS.md` | `4f1323305dbe06af469c726e88d5a67edad319b2d0b4c7475d13d5230657d811` |
| `det8/claims.py` | `5a49da0a87735205e02db24cdfaaf5797ccd6e82e416b2adcda61aadf927e7a4` |
| `det8/tests/test_claim_boundaries.py` | `ac5132faed4572444147ded5eb2b48477c1eeaf84c00ecaacb30a56cca104ac6` |
| `docs/CLAIM_REGISTRY.md` | `735dd2ed63ae57f29e503d6e8a0a7088d39387d60285c476ae1443792b790c48` |

**RI-08i acknowledged — one terminal internal read**

The coordinator and an independent reviewer derived the next candidate:
under existing common-X commands, a calibrated terminal binary read has
per-cell effect rank `1+[n_x≠0]+2[(n_y,n_z)≠(0,0)]`. Z-only, X-only and
tilted reads therefore have proposed total ranks 12, 8 and 16. A tilted
axis `(3/5,0,4/5)` with the empty word, A and AA has determinant
`−73728/78125`; root verified the exact three-setting inverse. The target
includes attained minimal linear predictive quotients, separating experiments,
three-setting minimality and exact compatible-probability-table conditions.

QR acknowledged this isolated obligation and is authoring its proof/model/
independent checks. Added readout availability/calibration is a premise.
The new read is terminal: retain the exact pre-read source and full
`(a,b,±)` outcome without fabricating a separate cell commitment, leave a
postmeasurement residual unspecified and refuse continuation. Full outcome
weights must not be confused with weights conditioned on a cell or an
unavailable earlier preparation history. State observability under known
commands is not generator identification, finite-sample accuracy or empirical
availability. No successor is started automatically.

**User-authorized commit and push cadence**

The user subsequently requested commits and pushes during work updates.
This supersedes earlier no-commit/no-push boundaries for future scoped
checkpoints; their historical statements above remain accurate. Root inspected
the empty index, `ret` branch and configured `origin/ret` upstream, fetched the
remote and confirmed no divergence at `c42cac0`. QR acknowledged that root
will handle git/index operations centrally. The existing hourly heartbeat
now explicitly includes reviewed scoped commits, remote pushes and verification.

The first checkpoint scope is the self-contained accepted research registry
and its complete pinned source/statement closure, the separate RI-15 interface
and review/coordination notes. Its executable closure requires no uncommitted
core, RET, claims or application implementation. Broader coordination notes
describe the reviewed working tree and can reference separately deferred local
work; this checkpoint is not a full project/release snapshot. Unrelated
pre-existing changes, protected evidence and the active RI-08i sources are
excluded. Commit and verified remote identities are recorded after execution.

Before staging, the source-identity guard detected that QR's live handoff had
advanced to include unaccepted RI-08i results; the index remained empty.
The checkpoint therefore uses an explicitly labeled accepted-only handoff
snapshot, preserving its historical RI-08h-and-earlier sections. The live
handoff and active QR maps remain in the working tree for the ongoing task;
no active theorem/model/test is included. This separates the published
checkpoint from later local work without rewriting the owner's live files.

**First remote checkpoint published**

[Commit faad1e96d9c2818bbc91e7600dd575538259e5d8](https://github.com/omekagardens/det_8_framework/commit/faad1e96d9c2818bbc91e7600dd575538259e5d8)
contains the accepted research closure, exact adapter and review/coordination
records: 50 changed files from a 61-path allowlist; eleven dependencies
already matched HEAD. Its tree is `753e50d465602fdf618896a3413e22fae49bdc49`.
The sole changed previously tracked research statement is the reviewed
eight-line subsequent-result paragraph in `OPERATION_DOMAIN.md`, required by
the accepted manifest pin. No active RI-08i artifact or unrelated implementation
was staged. The accepted-only published handoff SHA-256 is
`33261b7720f9c6af008c1d28e5c309527209f2e242ff08e4956d46694249327e`;
the QR owner's live working-tree handoff remains intact for the next review.

A checkout materialized from the exact staged index passed **79 focused
registry/adapter regressions in 56.53 s**, including the adapter's normal and
optimized witnesses. Both CLI preflights also passed under `-I -S -B`,
verifying all sixteen registrations and the separate adapter without relying
on uncommitted core/RET/claim/application code. This validates the executable
checkpoint boundary; broader coordination notes remain working-tree reviews.
The prior complete registry result is 326 witnesses per mode, recorded above.

`git push origin HEAD:ret` succeeded from `c42cac0` to `faad1e9`.
An independent `git ls-remote --heads origin refs/heads/ret` returned the exact
full checkpoint commit. The index was empty afterward. No force push,
rebase, cleanup or modification of the live QR handoff was needed.
Subsequent documentation-only publication records do not alter this tested
source-tree identity. Further completed updates will be committed and pushed
under the user's instruction and the updated hourly follow-through contract.

**Next review received during publication**

QR delivered RI-08i after the first source checkpoint was pushed. Its live
handoff and summaries are source quiet, and its owner stopped without starting
a successor. Independent proof and implementation audits have begun; the
result is not accepted or registered yet. The owner's 30 new checks per mode
and 383 scoped checks are reported evidence, not a coordinator acceptance.
The bundle is `docs/validation/t8-q-terminal-read-observability-2026-09-13/`:

| Pending RI-08i source | Supplied SHA-256 |
|---|---|
| `TERMINAL_READ_OBSERVABILITY.md` | `aaf1d0bd828b22c5eae9b551bae5989dc27dd1ba04631181f4c642f3d410adb7` |
| `model.py` | `0e60694bad07016886ec2451f4b17a5ac7dd24c089c8953dabb926620c8148d8` |
| `check.py` | `cf508d61ef6260926123185814edefdf4b5b8393880aab01ba0645cba0bd8f22` |

The next follow-through must read the live handoff, complete that independent
acceptance, and publish its own reviewed source checkpoint before assigning
another QR result. It must also preserve the remaining local application,
core/RET and evidence scope rather than add it indiscriminately. This
documentation update records the verified first push and the pending review;
it does not change the already tested research or adapter sources.

**RI-08i independent proof and source acceptance**

The coordinator accepts the bounded terminal-read theorem and typed source
contract after two independent reviews. One reviewer checked the complete
proof, exact rank and reconstruction identities; the other inspected the
full implementation and independent witness source and passed 94 additional
exact in-memory probes in 2.591 s. The coordinator read the proof and changed
implementation paths, checked the complete read/table contract and reviewed
the new registry and QR roadmap diffs. The only requested proof-note repair
clarifies that the retained object has sixteen labels and every entry of a
16×16 kernel. Its final SHA-256 is
`ac00c0aa13b3b47c504b85ce9296d38ee16c5529a5c5932aca73c4e1f00ca1ad`;
the earlier pending note pin remains historical. Executable pins are unchanged:

| Accepted RI-08i source | SHA-256 |
|---|---|
| `model.py` | `0e60694bad07016886ec2451f4b17a5ac7dd24c089c8953dabb926620c8148d8` |
| `check.py` | `cf508d61ef6260926123185814edefdf4b5b8393880aab01ba0645cba0bd8f22` |

The proof classifies backward effects under the full common-X word catalogue,
with ranks 8/12/16 and attained minimal homogeneous mass-retaining linear
summaries. This is a full-span statement; available preparation subsets and
arbitrary nonlinear encodings are outside its lower bound. The positive
sections are mathematical, not preparation or reset operations.
Empty/A/AA resolve a tilted read with determinant `−73728/78125` and an
exact inverse. Shared cell sums and positive reconstructed blocks characterize
compatible full-outcome probability tables, including zero cells without
division. Three resolved settings are minimal in this catalogue. An added
nonparallel pi-Z control still leaves the Z-read blind X direction intact.

All-finite policy equivalence retains the same context, committed prefix,
initial pending word and nominal metadata; raw audit payload cannot drive the
policy. The terminal response keeps the complete pre-read source, calibrated
effect and actual `(a,b,sign)` outcome, invents no separate cell commitment,
specifies no postmeasurement residual and refuses continuation or zero-weight
selection. Current-snapshot probabilities do not supply missing earlier
preparation or reference selection weights. The general interior proof is
separate from the t=3/5 exact fixture, and no endpoint inverse, unknown
generator, physical clock, repeated preparation or finite-sample claim follows.

The seventeenth registration preserves all sixteen earlier objects exactly:
removing its final object reconstructs manifest
`cab559036fe724ad78edd0beb7565586eb506515d24e4dc0dd4544074677f939`.
Its manifest is `aabf2b1a0a25bbb1511e33ad7e34ce63958e87bf224fa743c4c5b7369390c3c5`.
The unchanged runner and seven-module standard-library contract require no
new import mechanism. The implementer passed 64 focused registry/claim checks
in 2.42 s, export parity, scoped Ruff/format and 68 guide/generated-summary
links. Both legacy canonical JSON digests and the exporter remain unchanged.
All six integration reservations are released. The claim implementation and
its generated reference remain a separately deferred local baseline; this
publication includes the self-contained research registry and its closure.

The QR owner also repaired two stale current-roadmap cells to distinguish
already accepted conditional cones from the still-open DET selection and
actual availability obligations. Historical theorem handoffs remain dated.
Root checked 179 local links across the coordinator and research documents,
with no missing targets. These reviews and finite tests are internal checks,
not external peer review or formal proof verification. The independent 94
probes and QR's 383-check inventory are not added to the registered total.

**Seventeenth registration — exact staged-checkout replay**

The initial six-path index contains only the three new RI-08i artifacts and
three registry integration files. It was materialized into an isolated
checkout; all other sources came from the already published parent. Its
source-stage tree identity was `6f7b9285396795af8c6a125635fb67d5f2470637`.
The complete runner executed under `-I -S -B`, with `--optimized` adding
`-O` to every child. Final results:

| Mode | Suites | Witnesses | Loaded executable sources | Result |
|---|---:|---:|---:|---|
| Normal | 17 | 356 | 30 | Passed; 117.208 s |
| Optimized | 17 | 356 | 30 | Passed; 116.920 s |

All thirty new checks passed per mode. No failures, errors, skips, expected
failures, omitted declared source, observed registered-source drift or runner
change occurred. The same staged checkout passed **43 registry regressions
in 2.23 s** with bytecode/cache writing disabled. This verifies the current
research source closure independently of the broader uncommitted core, RET,
claim and applied implementations. RI-15 is unchanged and its earlier
separate acceptance remains valid; no new adapter or release count is added.
Subsequent acceptance/publication edits to coordinator and QR documents do
not change this tested executable closure.

| Seventeenth integration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `aabf2b1a0a25bbb1511e33ad7e34ce63958e87bf224fa743c4c5b7369390c3c5` |
| `det8/tests/test_research_registry.py` | `7a1965eb6d2208891093a057063d4dbbc4570e9d837102e369f8ba5fa67e1cbe` |
| `docs/RESEARCH_CHECKS.md` | `93827d533b6af50349794640dcebda3ccb78e16b3112e2638cac71bd03ce7996` |
| Local `det8/claims.py` | `de8089909025559910ebd0913a12fb832cd029ceb8e1e42f390ae3a9b815b5f0` |
| Local `det8/tests/test_claim_boundaries.py` | `b0011fac57077689ef5967b689aa548d6da096bd0826d6664d58d2847b5678d2` |
| Local `docs/CLAIM_REGISTRY.md` | `0974e1402f7104094e17d425563babc80b7b27e4120da0287da044cab0b02d62` |

The next checkpoint includes these accepted research sources and reviewed
coordinator/QR summaries. It preserves the separately deferred local baseline
and original dated review. Root remains the sole git/index owner; normal
push and independent remote-ref verification follow source capture.

**RI-08i remote checkpoint published; bounded capstone assigned**

[Commit 8714772534b5407db79e0989c2a526a1c5370afd](https://github.com/omekagardens/det_8_framework/commit/8714772534b5407db79e0989c2a526a1c5370afd)
contains the twelve reviewed paths: the three RI-08i artifacts, three registry
integration files, three QR handoff/map documents and three coordinator
plan/progress/ledger documents. Final tree identity:
`d5410668a8f9f2aea153cb1546d8b3b29b825be8`.
A tree comparison with the tested staged source snapshot found only the six
subsequently updated Markdown coordination/map files; the tested executable,
registry and theorem-note bytes are identical. The index allowlist, source
hashes and scoped whitespace checks passed. No broader local baseline was
included, and the dated original review is unchanged.

A fresh fetch before capture found no local/remote divergence.
`git push origin HEAD:ret` advanced `99157c1` to `8714772`; an independent
`git ls-remote --heads origin refs/heads/ret` returned the exact full new
commit. The index was empty afterward. Root notified QR of the verified
checkpoint and released the source hold before sending the next assignment.
This follow-up publication record changes no tested source.

Two separate read-only planning reviews checked the next obligation against
the original review. Their recommendation is **one robustness capstone, then
consolidation**, rather than an unbounded series of finite quantum fixtures.
RI-08j is now assigned to the existing Quantum Relativity thread, reserving
only a new `t8-q-observation-stability-2026-09-13/` bundle and its existing
three QR documents. It must return an independent proof/source review,
normal/optimized exact checks and stable hashes, then stop for root acceptance.
Root continues to own registry/claim integration and all git operations.

The proposed theorem uses the full eight-outcome laws at empty/A/AA. For
compatible normalized sources in the same known context, let epsilon_k be
per-setting total variation, d_F half the sum of filtered block trace norms,
and d_N half the native-kernel trace norm. If B is the inverse matrix of
backward axes and b_k its column Euclidean norms, the candidate bound is
`max epsilon_k ≤ d_F ≤ Σ b_k epsilon_k`. The best coefficient for a common
maximum error is proposed to be `Σb_k`, attained on three independently
perturbed cells. At the accepted tilt it is approximately 3.126749; the
implementation must use exact expressions or certified upper enclosures.
This is a candidate requiring QR proof, not an accepted empirical guarantee.

The target also separates sharp filtered conditioning from the valid raw
bound `d_N≤d_F/(1-|t|)`. The latter factor is unavoidable even for bounded
raw sources, while the combined coefficient's sharpness is not assumed.
Axis limits expose actual invisible directions; vanishing cell weights
preclude uniform cell-conditioned precision. Supplied deterministic table
error budgets and an exact positive feasible candidate should certify a
nonempty compatible error set and its bounded diameter. Failure of one
candidate is inconclusive without an infeasibility proof. Inconsistent exact
tables can admit a feasible source under nonzero budgets, so exact inversion
refusal and bounded-error feasibility must remain different contracts.

No added preparation, control, reusable instrument, numerical fitting solver,
finite-sample confidence or measured advantage is assigned. Full native data,
zero cells, retained context/history and terminal-only semantics remain.
A simple linear-target error corollary may connect this to the existing
identifiability contract without changing application or RET sources.
After the capstone, the next decision is a single premise-to-conclusion
consolidation and the retained-word first-commit gap, with measured
instrument/data/objective choices still explicitly open.

**RI-08j capstone — independent acceptance and provenance repair**

QR delivered a source-stable observation-stability theorem, exact model and
27-test suite. Root read the complete statement, compared inherited code with
the accepted RI-08i source, and inspected every new certificate path and the
QR map/handoff diffs. The mathematical reviewer accepted the sharp constants,
axis limits, native norm comparison, singular and rare-cell witnesses,
unknown-calibration ambiguity and deterministic feasible-set diameter argument.
That reviewer passed **63 independent exact probes in 2.607 s** on the initial
submission. The theorem and numerical constants have not changed since.

Root and the implementation auditor identified one provenance ambiguity:
a raw matrix could carry SnapshotMetadata that the certificate never bound
to a typed source. This did not invalidate the diameter theorem, but could
misrepresent the audit's history contract. QR repaired the common raw-candidate
validator to reject all non-None metadata. Matching context, complete prefix
and pending word now requires the typed State. The raw path remains an
explicit mathematical fixture and never manufactures a prepared state.

The new 28th regression reproduces the old acceptance and checks the factory
and direct FeasibleWitness/CandidateFailure constructors, covering successful
and failing candidates: unannotated raw matrices remain valid, annotated raw
matrices refuse, matched typed inputs succeed and mismatched typed metadata
refuses. The note's section 5 and current handoff/maps state this rule.
No predecessor source or theorem was modified. Owner and test-author replays
passed all **28 revised checks in each mode**; owner times were 25.446 s and
25.381 s. Scoped lint/format, 96 local links and whitespace checks passed.
The earlier 27-check submission and H/I replay counts are historical, not the
final capstone inventory.

The full-source auditor inspected the repair and passed **7 independent
adversarial cases in each mode** against captured final source bytes, with
`-I -S -B` and additionally `-O` for optimized execution. Cases included a
positive off-image kernel preserving coarse weights, one-shot inputs, deep
input detachment, a 10^-400 rare cell, nested provenance mismatch, distinct
per-setting budgets and exact coefficient squares. No failure, skip, error
or source drift remained. Those cases are separate audit evidence, not new
registered witnesses. Root accepts the corrected bounded source contract.

| Final RI-08j artifact | SHA-256 |
|---|---|
| `OBSERVATION_STABILITY.md` | `ca7e241399b1d4170b8181e42f510438c34951f2b601020e0146034b40bf2c88` |
| `model.py` | `6e761e6e107fba9d3415276a6e0b6170e7f3b34441de2133e8c3874cc2099bea` |
| `check.py` | `2deb8a90236a51c367c9086d090c9416a49b20473c8b909f26bf816a5339c88d` |

The sharp theorem compares full eight-outcome laws and filtered block trace
norms: `max epsilon_k≤d_F≤Σb_k epsilon_k`. Each inverse-column coefficient
and their common-error sum are attained on the full positive four-cell
mathematical domain. The exact general-axis formula distinguishes full-rank
poor conditioning from actual blind directions. Native reconstruction obeys
`d_F/(1+|t|)≤d_N≤d_F/(1-|t|)`; bounded raw states prove the endpoint factor
cannot be removed. The composed coefficient is valid but not claimed jointly
sharp, and raw kernels are not trace-one probability states.

Certified rational enclosures of the radical coefficients support an explicit
error-budget audit. A supplied feasible positive source proves nonemptiness
and a diameter bound; a failing candidate is inconclusive. Inconsistent exact
tables can have a feasible source under nonzero budgets. There is no fitting,
clipping, inferred infeasibility or confidence level. Zero cells and all native
entries remain intact; rare-cell conditional precision needs a positive mass
floor. Unknown calibration, preparation availability and measured advantage
remain independent obligations.

The capstone closes the assigned finite-cone refinement branch. The planned
consolidation will state one conditional finite-record observability/stability
argument, without a new executable fixture. Known A/A² matrices suffice for
its finite theorem; the stronger continuous-group classification remains a
separate proposition. The construction route and RI-15 adapter must preserve
all domain/range/history qualifications. RI-07's finite-label first-commit
result remains separate from the unproved extension to unbounded retained
command words. Source quiet continues through registration and publication;
root will make the already authorized consolidation assignment afterward.

**Eighteenth registration — scoped staged-checkout verification**

The eighteenth explicit registry object binds the final corrected capstone
note/model/check. Removing it reconstructs the preceding manifest
`aabf2b1a0a25bbb1511e33ad7e34ce63958e87bf224fa743c4c5b7369390c3c5`
exactly. All seventeen earlier objects and their source/statement bytes remain
unchanged. The new suite declares six direct standard-library imports,
including `math.isqrt`; the existing seven-module allowlist already permits
them. The runner and exporter are unchanged.

The six publication source paths—three J artifacts and three registry files—
were captured from the index into an isolated checkout. Initial tested tree:
`7a1c417ca6e2ec1d6e539d2e2c73c00f8a4e28a2`. Under `-I -S -B`, the full
manifest preflight passed with **18 suites and 32 declared executable sources**.
The coordinator then explicitly selected only the new observation-stability
suite from that checkout:

| Mode | New witnesses | Loaded new sources | Result |
|---|---:|---:|---|
| Normal | 28 | 2 | Passed; 25.128 s |
| Optimized | 28 | 2 | Passed; 24.971 s |

There were no errors, failures, skips, expected failures, unexecuted declared
J sources, observed registered-source changes or runner change. The same
staged checkout passed **43 registry regressions in 2.31 s**. The integrator
also passed **64 local registry/claim checks in 2.56 s**, export parity,
scoped lint/format and 70 guide/generated-summary links. Root checked 161
local links across the coordinator, QR and capstone documents with no missing
target. All six integration reservations are released.

The **384-witness total is the cumulative accepted inventory**: the prior
356 passed normally and optimized at their unchanged source identities,
plus these 28. This cycle did not rerun all 384 or count repeat executions as
independent results. Neither the separate RI-15 witnesses nor additional
review probes are added. The staged research closure again needs no local
unpublished core/RET/claim/application source. Source acceptance does not
recertify the whole checkout or close a release/physical claim.

| Eighteenth integration source | SHA-256 |
|---|---|
| `docs/research/registry.json` | `a5d94f2d5451f6810855b129886500afc840bf1ee86b01dd515c98158cf5454f` |
| `det8/tests/test_research_registry.py` | `7e03399135aac8effa890692fcf8a2636fc718bad85dcd2031f13abc492c3a65` |
| `docs/RESEARCH_CHECKS.md` | `8ee8e516b0a650ca221c8e07e6e5eb9b233579df8aa47d96ce6306eccc47c43c` |
| Local `det8/claims.py` | `a96028a7c731ba1ab53c46d78ac872348155289b3123f6879d2e18a15108872a` |
| Local `det8/tests/test_claim_boundaries.py` | `786746967daef985c64f5e61478f844f18bb991045853638251d4a52475091a0` |
| Local `docs/CLAIM_REGISTRY.md` | `2c974180402c491c867b663f2487098484b232896b8a8d385f78b8fededc72d5` |

Both legacy canonical claim JSON outputs remain identical to their preceding
accepted digests. The claim implementation/generated reference remain part
of the separately deferred local baseline; the publication scope is the
self-contained research closure and reviewed coordination/QR documents.
Only Markdown status/acceptance changes follow the tested source capture.

**RI-08j checkpoint pushed; conditional synthesis assigned**

[Commit da8fe99a1b1b91dab962ec0ed17bde349a06458c](https://github.com/omekagardens/det_8_framework/commit/da8fe99a1b1b91dab962ec0ed17bde349a06458c)
publishes the twelve reviewed capstone/registry/QR/coordinator paths. Its
final tree is `197f2e7a701746ff9e57d9319df7a7e0fc244768`.
The final tree differs from the tested source-stage tree only in six
Markdown plan/ledger/progress/handoff/map files. All six tested source paths
were byte-compared with the materialized checkout before capture, and the
three live QR document hashes matched the owner's quiet handoff. The exact
index allowlist and scoped whitespace checks passed; no separately deferred
local baseline or unaccepted successor was included.

`git push origin HEAD:ret` advanced `e4d4bd4` to `da8fe99`. Independent
`git ls-remote --heads origin refs/heads/ret` returned the full new commit,
and the index was empty afterward. Root notified QR of the verified remote
checkpoint and released its temporary source hold. This publication record
changes none of the tested source identities.

Root then assigned the existing QR thread one synthesis document,
`docs/research/FINITE_RECORD_OBSERVABILITY.md`, plus its existing three QR
map/handoff documents. The already authorized program covers this separate
bounded assignment; no new user permission is needed. No new executable
fixture, accepted-source edit, registry change, RET/application work or
automatic successor is assigned. Root retains coordinator/registry and git
ownership. QR must deliver one source-stable document with independent review
of the combined proof and its exact cross-bundle arrows.

The synthesis will center on the conditional finite-record observation and
stability theorem with enough native-map/filter, matrix/inverse, compatibility
and norm argument to assess it directly. It will distinguish the minimal
known-command/read premises from the separate continuous-group classification,
and label the local/joint/changed-return-domain route and RI-15 interface
without implying a globally selected physical operational theory. It must
retain the endpoint, rare-cell, calibration and failed-candidate boundaries.

The final open-bridge section will specify why finitely many full committing
labels do not cover unbounded retained command words, and what a countable-word
output/norm/convergence/continuation theorem would still require. It will also
retain the measured instrument/data, target/tolerance, noise or budget,
cost, baseline and held-out evaluation dependencies. The document adds no
sampling confidence, physical QM or measured benefit. Current accepted pins
and formula/link checks suffice for this documentation synthesis; another
complete witness replay is not required solely to rewrite the argument.

**Research repairs and exact identifiability — isolated publication candidate**

14 September 2026 UTC. Three independent publication audits examined the
accepted research repairs, applied consumers and claims package against
published HEAD while QR completed the assigned synthesis. The research repairs
and exact identifiability interface have a complete independent source closure.
Claims, chronology-dependent reporting and the RET comparator need the specific
prerequisites in the [publication backlog](PUBLICATION_BACKLOG.md); none is
silently included here. The newly received QR synthesis remains a separate
submission pending coordinator review.

The candidate starts from `9a0832939435c5d998cf680135d23a3d353af8db`.
It overlays fourteen complete selected source files plus a published-runner
snapshot containing only these eight accepted group replacements:

- `test_correlation_class`, `test_correlation_frontier`;
- `test_grade2_justification`, `test_record_extendability`, `test_why_complex`;
- `test_born_rule_uniqueness`, `test_quantum_deadlock`, `test_frontier_research`.

AST comparison verifies the exact set of changed top-level functions, equality
of those eight functions to the working source, and equality of every other
function and top-level statement to published HEAD. The unchanged
`test_pair_kernel` group is also exercised. The working runner is preserved;
its unrelated core/RET and other local consumer changes are not staged.
The shared validation helper uses only the standard library. Its inclusion
does not certify deferred consumers or expand the public-core support claim.

The final source audit accepted the full selected model diffs, test files and
helper. Two inherited statements were narrowed before the final test capture:
the pair-kernel header now separates pairwise structure and strong positivity,
and the Gram-sum report distinguishes its exact identity from numerical
reconstruction with reported error and tolerance. Independent delta review
accepted both qualifications and rechecked the exact identifiability theorem.

From this isolated candidate, using CPython from the existing development
environment with bytecode and pytest cache writing disabled:

- `pytest det8/tests/test_pair_kernel_contracts.py
  det8/tests/test_research_claim_contracts.py
  det8/tests/test_applied_identifiability.py -q`: **203 passed in 0.19 s**
  (47 kernel, 48 certificate and 108 identifiability cases).
- The eight selected legacy groups and unchanged kernel group:
  **90 PASS, 0 FAIL, 0 ERROR**.

These results verify the selected publication candidate, not the whole
dirty checkout, old G1 evidence, a RET calibration or physical selection of
quantum premises. Exact identifiability concerns unrestricted real parameters
under supplied rational coefficients; it does not certify noisy precision,
feasibility or measured utility. No accepted QR executable or registry pin
changes in this checkpoint, so the unchanged 384-witness cumulative inventory
is not replayed or counted as new evidence.

Only coordinator publication/status Markdown accompanies the fifteen source
paths. Their tested SHA-256 identities follow.

| Tested publication source | SHA-256 |
|---|---|
| `det8/models/pair_kernel.py` | `d45e3b09c3f923b08c7aa27ce0d78a610de6c98dc4c51c1b65a393b6ddb77cf7` |
| `det8/models/why_complex.py` | `3353967424554efafa08b2c01ab9a291d0efe899fb1b9f65e7c0c42d41a01708` |
| `det8/models/grade2_justification.py` | `ba76691e82c07f284adc97ccc23229d22a96abd838e48ce2b3674cfbf476768f` |
| `det8/models/correlation_class.py` | `72bee81017c25dcf351cea57204a773095b25d734aa2db0587172a298a2d209e` |
| `det8/models/correlation_frontier.py` | `8f3fbbf530e8325c3188260efd4e155065bcc3ebb6afba76d4220904af14e8b1` |
| `det8/models/record_extendability.py` | `e62508ed69763a4f9c0fc351f1b4bc1d29113b605221fc938b78a5b45c7935d2` |
| `det8/models/born_rule_uniqueness.py` | `b7d31d290f43f5e9db8a49fa9885cd239b1645e2c018f9f3a19779097f01f386` |
| `det8/models/quantum_deadlock.py` | `5e97e3ab1defd63e5f122b3b4e99d3dc2e7b4cdb387c3c2673d968d8e40158ec` |
| `det8/models/u1_emergence.py` | `61a36bb7da2f89756cffe819f7b8af760f41e4b20b411df391f8676d3751008c` |
| `det8/models/validation.py` | `e29bdba205a2709eccfaadbde51771b0612e24c9622329df9b3d720a27dd232d` |
| `det8/tests/test_pair_kernel_contracts.py` | `2d738f0dbac23cc6abc6b804acea4de246a4620fb84d2874367cce418de6abf3` |
| `det8/tests/test_research_claim_contracts.py` | `b55d3e6cd27786847a9ea0fa02b054a4d288fe632acd51e5a0b359b44af8f5e3` |
| `det8/applied_physics/identifiability.py` | `136588b80cc9d1935137c81885dc26446947dc52f81c120a0652a75b7fb268d9` |
| `det8/tests/test_applied_identifiability.py` | `896951787410eb9a286591720f5659f7ffe3a357bdf32342941d90108d201088` |
| `run_tests.py` | `67db5c364573dda855d645963d07a7ebe171790884f3110718f010d3d00d6ddf` |

**Research/identifiability checkpoint published**

[Commit 38be4c0c941c62329b9175883748d4e586b9745e](https://github.com/omekagardens/det_8_framework/commit/38be4c0c941c62329b9175883748d4e586b9745e)
contains the fifteen tested source paths above and four coordinator Markdown
files. Final tree: `431c290916cd9fcd46911db111508213421baaa7`.
Before committing, root checked the exact nineteen-path index allowlist,
byte-compared every staged source with the tested candidate and passed scoped
whitespace checks. The working runner retained SHA-256
`819fc4e5cce73a3e5eabf970bdaa24931c1e480e7968471ac4d228e2ea0914de`.
No unaccepted QR synthesis, unrelated core/RET baseline or claims/application
dependency was staged. `git push origin HEAD:ret` advanced `9a08329` to
`38be4c0`; independent `git ls-remote --heads origin refs/heads/ret` returned
the full commit above. The index was empty afterward. These publication
records do not change the tested source identities.

**Conditional finite-record synthesis accepted**

QR delivered the single assigned
[synthesis](../research/FINITE_RECORD_OBSERVABILITY.md), plus its three
existing map/handoff documents, without a new executable or successor.
Submitted synthesis SHA-256:
`a82cbda6bc4a9eb27a2a40d75e1fde0b7fde9f28641f743c808a78e6fc18d50d`.
Root read the whole argument and accepted it after two independent reviews:
one checked the full inverse, compatibility, sharp filtered constants,
native norm and feasible-budget proofs; the other audited each construction
arrow, record/type interface and the limits of first commitment and applied
transfer. Neither found a substantive blocker. The mathematical reviewer
also passed 29 independent exact arithmetic/path checks.

Root verified all **50 unique registered statement/source pins** against
both the manifest and published source bytes, and all **123 local links**
in the four submitted documents. This is broader pin coverage than the
author's reported 36-pin subset; neither check reran the witness inventory.
All executable sources and the registry remain unchanged. The main theorem
body is preserved byte-for-byte after review: reversing its two-line status
change reconstructs the submitted SHA-256 exactly. The three QR documents
receive only acceptance/status additions beyond their reviewed submission.

The synthesis establishes one conditional finite-dimensional endpoint under
the known interior native image, fixed commands, calibrated full terminal
read and matching context/history. Its route table does not turn domain
restrictions into dynamics, identify C with its quotient, invent previous
selection probabilities, or convert terminal audit wrappers into reusable
states. The all-real generator classification is a separate result. Exact
budget feasibility remains a supplied-candidate check with deterministic
diameter bounds, not an infeasibility solver or statistical confidence claim.

The named retained-word first-commit gap is the next bounded proof target.
The measured pilot remains dependent on instrument/data and its frozen
evaluation objective. Neither gap is closed by the synthesis, and no further
finite-cone refinement or RET implementation is assigned in this checkpoint.

| Accepted synthesis/status source | SHA-256 |
|---|---|
| `docs/research/FINITE_RECORD_OBSERVABILITY.md` | `55b6164f120f1b56bd75905be02a05d6a77a1ec0ab6aa08343746a96862c7966` |
| `docs/coordination/QR_HANDOFF.md` | `26e6e4afe452e395c7eae310e0df43109b827667ee6f37d17361982c10ddec0a` |
| `docs/track_b/QR_MAP.md` | `e4f764ee53c4866b9023aa2eb10fb42aeba42a60cc60499cfe8aab05c59236bf` |
| `docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md` | `ecf492d8ca376557bb2001a28222107eccb1a9970b7c2c05439df6f9b585eb47` |

**Synthesis checkpoint pushed; RI-16 dispatched**

[Commit 50d652fd8ef963905fbc4b58bc0bc2ddc2b9d473](https://github.com/omekagardens/det_8_framework/commit/50d652fd8ef963905fbc4b58bc0bc2ddc2b9d473)
publishes the accepted synthesis and eight related Markdown documents.
Final tree: `6e4891c14c4061eeb85f4082535789a18d4d35fc`.
Root checked the exact nine-path allowlist, staged/working byte equality,
scoped whitespace/conflict markers and 206 local links across those documents.
A final independent status review passed after one stale candidate reference
was corrected. The original review and working runner remain unchanged.
The normal push advanced `38be4c0` to `50d652f`; independent remote-ref lookup
returned the full commit above, and the index was empty afterward.

Only after that verification, root sent the existing Quantum Relativity
thread the bounded RI-16 assignment in the root plan. Its new isolated bundle
will address countably retained words with a declared complete output norm,
operator convergence, full mass/never accounting, prefix-shift recurrence and
bounded word-dependent continuations. A preliminary feasibility review
identified the base-norm proof route and counterexamples; it does not count
as acceptance of an unwritten successor theorem.

RI-16 explicitly distinguishes retained words from hidden paths. Its terminal
read specialization may use supplied scalar effects with full labels, but
may not invent a postread residual or treat the nonlinear probability-weighted
pre-read audit source as a positive linear instrument. Literal-cut outputs
retain their existing type and map. No physical availability, uniform rate
over models, infinite-dimensional-input theorem or never-commit state is
presumed. The proof, exact supplement and independent handoff remain pending.

QR owns only the three new bundle files and its existing three maps/handoff;
the accepted synthesis and executable bundles remain stable. Root keeps
registry, coordinator and git/index ownership. The next independent root
publication item is the RI-11 chronology/consumer prerequisite audit described
in the backlog. RET baseline publication and the measured instrument/data
decision remain separate dependencies; neither is silently resolved here.

**RI-16 retained-word first commitment accepted and registered**

QR returned the assigned three-file bundle and three map/handoff documents.
Root read the complete theorem and model. Independent mathematical review
accepted the Banach l1 output construction, faithful base-norm identities,
operator convergence and exact survival-minus-never tail, chronological
prefix-shift recurrence, leastness with hidden empty steps and uniqueness
without them, bounded continuation interchange and all counterexamples.
Eighteen additional exact checks used a mixed empty-step/retained-letter law.

A separate complete source audit accepted full retained contexts, immutable
prefixes, pending-word handling, symbolic tails, positive selection and the
checked last-new-letter effect family. It added 108 exact assertions on the
native L_t image, complex payload, total-entry mass, partial-trace inverse,
tilted scalar effect and metadata without replaying prior pending commands.
Both reviews found no blocker. They do not create additional registered
witnesses or prove physical availability.

Reviewed note SHA-256:
`b975fad1e382cd3068f35e19da379e1a9a6746414d387db403d6c2655214eedb`.
Root changed only its two-line administrative acceptance status. Reversing
that substitution reconstructs the reviewed digest exactly; the entire
mathematical body and both executable sources are unchanged.

The nineteenth explicit registry object passed a separate metadata audit.
Removing it reconstructs the preceding eighteen-object manifest exactly;
all earlier object contents and source/document pins are preserved. The
new code imports only dataclasses, fractions, itertools and unittest,
already allowed by the unchanged runner. No claims/core/RET, earlier QR
executor or default-CI source was edited for this integration.

Root materialized published base `d8d6a35f76bd43ac4e53f0de463af51bba7551ff`
and overlaid the three RI-16 artifacts and three registry/guide files into an
isolated publication candidate. Full pin/import preflight passed with
**19 suites, 34 executable sources and 53 unique statement/source paths**.
The runner's identity list additionally includes the manifest itself.
Only the new suite was selected for execution:

| Mode | New checks | Loaded declared sources | Result |
|---|---:|---:|---|
| Normal | 27 | 2 | Passed; 0.946 s |
| Optimized | 27 | 2 | Passed; 0.955 s |

There were no errors, failures, skips, expected failures, unexecuted declared
sources or observed source drift. The candidate also passed **43 registry
regressions in 2.30 s**. The cumulative inventory is now **411 witnesses**:
the previous 384 retain their accepted normal/optimized source identities,
and these 27 passed in both modes. This is not a fresh 411-witness replay;
neither the independent review probes nor the separate RI-15 inventory are
added to it. Subsequent guide/acceptance edits are Markdown only.

| Final RI-16 registration source | SHA-256 |
|---|---|
| `RETAINED_WORD_FIRST_COMMIT.md` | `5af27962b038b219bc852c9abd77d99e71f086f03cbf8a8e35fd3c447e4c0a2f` |
| `model.py` | `7b14f8d99a1983d3b244c70fefb10262cf99d6d3eef522784bdce07d0c94fda6` |
| `check.py` | `995a01325ec7d4c4af6726c1a11d6ebe698e99b8e1749c7b40eaeb6dd356a1c2` |
| `docs/research/registry.json` | `6f1074841770f3677217c1383c5173c27a53360cfce9650eccfdb7304d06a257` |
| `det8/tests/test_research_registry.py` | `485497a72b306176ada7c385c48e009b42d9e0cb80f87817cc6a3d96e7fe2a1e` |

This closes the named retained-word gap under the declared finite-input,
stationary-policy and complete faithful-output-norm premises. It does not
close arbitrary growing-history policies, earlier selection probabilities,
general protocol/type orchestration, physical selection or measured benefit.
The local unpublished claims endpoint remains its explicit eighteen-reference
subset through RI-08j; its broad core/RET support dependencies remain deferred.


**RI-16 checkpoint pushed; RI-17 design dispatched**

[Commit 22eca4e7eb1b73b84db6fe3b6ff613df932b15c1](https://github.com/omekagardens/det_8_framework/commit/22eca4e7eb1b73b84db6fe3b6ff613df932b15c1)
publishes thirteen reviewed RI-16/registry/status paths. Its tree is
`0078050a51566498254b472e21609e86b996753c`. Root checked the exact staged
allowlist and candidate bytes, pushed normally to `origin/ret`, and verified
the full remote branch ref independently. The index was empty afterward.

Only after that verification, root assigned the existing Quantum Relativity
thread the RI-17 design described in the root plan. It must inspect the actual
APIs along one finite local preparation, reference selection, RI-15
preterminal coupling, adopted L_t return and terminal-read route. Every
transition must account for the full record, type and unnormalized weight.
Earlier selection probabilities are supplied by a complete declared policy;
provenance cannot infer them. The design must distinguish implemented adapters
from missing adapters or availability premises. RI-16 does not supply this
finite orchestration automatically. No executor or new registry entry is
assigned before independent design acceptance.

QR owns only the new composition plan and its three existing maps/handoff.
Root retains coordinator and git/index ownership and advances RI-11
independently. RET baseline publication and the measured instrument/data
decision remain separate dependencies.


**RI-11 publication audit: initial integration failure**

A frozen candidate based on `22eca4e` included the complete reviewed clock
reader and direct consumers, clock-only snapshots of two existing test files,
and only the two affected legacy runner groups. Independent snapshot review
confirmed the exact selected function bodies, all twelve source/document
pins, nine whole-file matches and the unchanged runner remainder. No
unpublished core/RET source or downloader implementation was required.
The retained downloader references call only published pure URL/calendar
helpers, with no download.

The four focused test files passed **101 cases in 0.16 s**. The legacy ingest
group passed **21 checks**. The applied group then exposed an integration
regression in the new shape-norm guard: the ordinary cavity demo includes
positive tail terms whose individual squares underflow even though its total
shape norm is representable. The strict per-term norm check therefore stopped
a valid descriptive fit. This failed candidate was not staged or published.
The subsequent repair and its final validation are recorded below; the initial
101-case result alone does not establish successful integration.


**RI-11 complete chronology/consumer candidate accepted**

The final source candidate is based on `22eca4e` and includes eleven Python
paths plus `docs/applied_physics.md`. It closes the earlier missing chronology
dependency without copying unrelated downloader, IBM, polling, core or RET
work. The two clock scripts use the same dated reader/report contract.
Their corrupt-input CLI regression now covers both scripts.

The published-format clock reader preserves the six NVALS fields in order,
continuations, calendar/time system, uncertainty values, source identity and
rejection details. NVALS=2 means bias plus bias uncertainty; NVALS=3 adds rate.
GLO is aligned to UTC(SU)+3 hours, so its inserted-second boundaries differ
from UTC-labelled coordinates. These format claims follow the official
[RINEX clock 3.04 specification](https://files.igs.org/pub/data/format/rinex_clock304.txt).
The pinned coverage uses the [IERS leap-second history](https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat)
and [Bulletin C 72](https://datacenter.iers.org/data/16/bulletinc-072.txt):
UTC support starts at 1980-01-01 and ends at the declared 2027-01-01 boundary,
with GLO labels shifted by three hours. Unknown scales must be unambiguous
under both UTC and GLO interpretations.

The audit repaired five chronology failure classes: unknown-scale GLO leap
ambiguity, missing lower table coverage, invalid interior time-system rows,
nonfinite/nonzero-underflow rate arithmetic, and inconsistent plain/gzip/legacy
header refusal. Legacy rows now retain dates/time scale/source hash and share
modern ordering, duplicate and overlap checks, including mixed collections.
Independent review of the complete reader and new 36-case chronology suite
added 188 exact/boundary assertions across all 18 supported leap transitions.
No remaining blocker was found in that bounded contract.

Two separate numerical failures were also repaired: a zero represented
relaxation shape norm could silently drop a better bank candidate, and a
clock quadratic fit could falsely report exact RSS=0 when nonzero residual
squares underflowed. The first aggregate-norm repair was too strict for
ordinary tiny tails, as recorded above. The final denominator uses `hypot`
before squaring: representable aggregate norms survive tiny individual tails;
a zero aggregate or entirely underflowed shape refuses the complete bank,
including when another candidate was already evaluated. Strict residual
square guards remain unchanged. Independent geometric-series and exact
Fraction aggregate witnesses cover the corrected distinction. These are
bounded representability guards, not accuracy or optimizer certificates.

Final isolated verification:

| Focused file/group | Passed |
|---|---:|
| Applied comparison contracts | 53 |
| Clock chronology contracts | 36 |
| Clock-only ingestion snapshot | 12 |
| Clock-only operational snapshot | 4 |
| Legacy applied group | 12 |
| Legacy ingestion group | 21 |

The four pytest files passed **105 cases in 0.17 s**. Both legacy groups
completed with **33 passes, zero failures, zero errors and zero skips**; this
includes the ordinary cavity demo that failed in the initial candidate.
No unchanged QR, research, RET, G1, wheel or full calibration suite was replayed.
The earlier local counts remain historical checkpoints.

The independent snapshot audit confirmed the twelve candidate pins, nine
whole-file copies, selected clock function bodies and byte-identical runner
remainder. Only the downloader-validation tail and polling-only root-path
entry were removed from copied test bodies; their broader working files are
preserved. The unchanged legacy downloader references use published pure
URL/calendar helpers only. The final two-source norm correction received its
own delta review. No external datasets/services or tokens were accessed.

Limits remain explicit: source hashes assume stable paths during parsing and
later hashing, rather than immutable acquisition; legacy external decompression
lacks the modern reader's stream-size bounds; generic satellite concatenation
and synthetic temperature/forcing are demonstration mappings. Headerless
snippets are conditional support, not complete strict RINEX certification.
Interval averaging, clock-noise covariance, physical identification and
measured application benefit remain outside this acceptance.

| Final RI-11 candidate path | SHA-256 |
|---|---|
| `det8/applied_physics/adversarial.py` | `d0135d04988899cfa33a4e49bc74fa458c8a82fb260fefa61a17ed9277613de1` |
| `det8/applied_physics/applied_tests.py` | `2284a9530109e642cc3c06cbfca9c3a51314d9ef20564a8e6250ca1cdcde93b4` |
| `det8/applied_physics/discriminator.py` | `bbcf8c0af6d735512c5d089f9c779a9da519be626dc83d9fc8835abfc61db07d` |
| `det8/applied_physics/ingest.py` | `78003b73f195d074c0a737bc377a475670aafdc5430f527e3d0e783b0e33ea28` |
| `scripts/full_year_aging.py` | `2b496223b7340de4fbfcaf4644064b0f2cb7b897eefb9b0a082852588504cc29` |
| `scripts/g11_quadratic.py` | `4bd85520884f46bf6c58db2998b1f2ff907f5ff13a0ea04f32e13e69e3f9fa5a` |
| `det8/tests/test_applied_comparison_contracts.py` | `f5cf9b40eb2081aa461e56829226867e19d260244ab191c6bc1ed39bd0dc4e03` |
| `det8/tests/test_clock_chronology_contracts.py` | `620c91a9bf147bfd08bf3bb39462ecdc8b2ef821801524ed426e684bb5fcbf67` |
| `docs/applied_physics.md` | `435b2a2ed496cc084f2b75c485f0ec4ea52c0ce0b9fec72004a3ab6376a5843e` |
| `det8/tests/test_ingestion.py` | `3bfd221008b52421844f41a8a80602ac880e3c0229dd223609c7d8e9dfd31c25` |
| `det8/tests/test_operational_scripts.py` | `ec8378c6af6eeb128433974cf330554d2b04604e09e095407bb2a1944fbf945f` |
| `run_tests.py` | `72ff241d1019ed2c5217a11fe1da0cd7a74ac914632486dadda4729249272647` |

The three selectively staged paths retain broader working versions. Their
unchanged working hashes are:

| Preserved working path | SHA-256 |
|---|---|
| `det8/tests/test_ingestion.py` | `4056dbf30e61d435c3c164c362f2af2a4a2941e235a734f1cb0394e22598ecbf` |
| `det8/tests/test_operational_scripts.py` | `05c697d88733a4dc008d9eaa2e995d455a959065e009534ab9ae82b592b9cdd4` |
| `run_tests.py` | `819fc4e5cce73a3e5eabf970bdaa24931c1e480e7968471ac4d228e2ea0914de` |


**RI-11 checkpoint pushed and remotely verified**

[Commit f8339ea4a4ce886ddc4513d989a2cecbad9d8dca](https://github.com/omekagardens/det_8_framework/commit/f8339ea4a4ce886ddc4513d989a2cecbad9d8dca)
publishes the twelve-path candidate and four coordinator documents. Its tree
is `a2bcce4e6e3af3ad3b9c19aa6522368db70f1d7e`. Root verified the exact
sixteen-path allowlist, every tested Python byte and updated Markdown byte,
scoped whitespace/conflict markers and local Markdown targets before commit.
The two clock scripts retain their executable working modes.

The normal push advanced `22eca4e` to `f8339ea`; independent remote-ref lookup
returned the full commit above. The index was empty afterward. The broader
working ingestion/operational tests and runner retain their recorded hashes;
the original independent review remains unchanged. QR's active RI-17 design
and three map/handoff paths were excluded, as were all unrelated baseline,
RET, downloader/IBM/polling and evidence changes.


**RI-17 composition design accepted; RI-18 implementation scoped**

QR returned the source-quiet four-document design handoff. Root read the
complete design and all three summary deltas. QR obtained independent full
mathematical and actual-API/record reviews. Separate root-side mathematical
and integration reviews accepted final submitted design SHA-256
`436013e51936146f6b36a2df7965be7c9428490bf65c17b55a1f21cf1d573524`.
No implementation or new witness suite was included.

Two root review corrections are explicit in that final source: selected
branch accounting includes incoming mass exactly once, and the cross-model
equality uses the actual raw matrix and exact Fraction arguments. The only
adaptive decision receives (a,b), because even a read-only full joint record
would expose source kernels through its context. The final contract retains
one selected reference record and full preceding terminal/stop audit anchors.
The integration review additionally freezes the implementation to its declared
empty-prefix/root-weight boundary: fixture-specific IDs must not accompany
unrestricted history acceptance. That precision is in the RI-18 assignment.

The conditional theorem composes the supplied local Y/Z maps, independent
ready/unavailable law, exact preterminal coupling, expressly adopted L_t
return, literal cut, record-selected empty/A word and scalar terminal read.
It is a positive finite scalar-output map preserving incoming mass. The
primary legitimate nonzero-c input reaches C0 through an actual branch, not
projection. Existing APIs do not yet supply the weighted orchestration or
lossless RI-15-to-i conversion; the plan specifies those two missing pieces.

Independent exact algebra supports all displayed probabilities: 64 read-path
coordinates plus two stops, with 16 positive reads totaling 2/3, two stops
4/15 and 1/15 totaling 1/3, and 48 zero read coordinates. Zero coordinates
create no selected source/record. This design arithmetic is not an executed
multi-API protocol, physical availability result or a new test count. The
registered inventory remains 411 witnesses with prior source identities.

Root changed only one administrative status fragment in each QR document.
Reversing each substitution reconstructs its full reviewed digest; the
mathematical/design body is unchanged. Final accepted identities:

| Accepted design/status source | SHA-256 |
|---|---|
| `docs/coordination/QR_PROTOCOL_COMPOSITION_PLAN.md` | `ae4558101ec1b1fa48c1f1eb259755a2af8c45a9f9887d59e9b0f3602615a696` |
| `docs/track_b/QR_MAP.md` | `8b385cf0c37e35237c56f572d91bbf37648cb210ae6a1fb46fd3f70873d644aa` |
| `docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md` | `5f1ca33b5ba47661ec0e1f86b0371b8136c49166b2449c0941c0e7373c33a846` |
| `docs/coordination/QR_HANDOFF.md` | `1575a93a49547b064fb4c7300f2ac2837e42a73853477e05f4edf28922c292cf` |

The next bounded assignment is RI-18, recorded in the root plan for dispatch
after verified design publication. QR owns three new bundle files and its
three summaries; root owns the separate six-alias launcher/regressions and
git/index. The accepted plan and all dependencies remain fixed. A temporary
author check loader does not constitute accepted launcher integration.
Independent proof/source review, exact finite-law/refusal checks and isolated
pinned execution are required before implementation acceptance. No broader
SDK, RET work, measured pilot or physical reconstruction is assigned.


**RI-17 design checkpoint pushed; RI-18 dispatched**

[Commit ad04963b28a9232b6496f233d2f475c12f333d4c](https://github.com/omekagardens/det_8_framework/commit/ad04963b28a9232b6496f233d2f475c12f333d4c)
publishes the four accepted design/status documents and four coordinator
records. Its tree is `5f6cfddfe21c56d001e5b8d5ad9ceebfddafc385`. Root
verified the exact eight-path Markdown scope, 163 local links and scoped
whitespace/conflict markers. All 59 accepted dependency paths and the registry
remained unchanged, as did the original review, RI-11 published source pins
and three broader working snapshot files. The normal push succeeded;
independent remote-ref lookup returned the full commit above.

After verification, root sent the existing Quantum Relativity thread the
complete RI-18 implementation assignment and accepted design hash. The
three new bundle files and three existing QR summaries are reserved to QR.
The six aliases, finite input boundary, complete weight accounting, full
metadata/audit anchors, independent native/tree checks and refusal obligations
are fixed in that assignment. Root retains the separate pinned launcher and
regression work for integration after the public callable contract is stable.
The author must report imports, source pins and actual normal/optimized
checks, obtain independent proof/source reviews and stop for acceptance.
No further permission request or automatic broader successor is implied.


**Heartbeat: RI-18 launcher infrastructure and an answerability consequence**

The coordinator read the current plan, progress and QR handoff, confirmed
branch `ret`/upstream `origin/ret` at verified `d72d430`, and inspected the
empty index and existing dirty baseline. Quantum Relativity is actively
implementing the assigned three-file RI-18 bundle with independent native
arithmetic and proof work. No duplicate assignment or successor was sent.
Root confirmed the six aliases/import boundary and reserved only its two
new launcher/regression paths. Active QR source and summaries remain excluded
from this coordinator publication.

Root's launcher implementer produced a separate fixed six-alias source
contract using the unchanged pinned research runner. Four published executable
dependencies and their statements are bound, along with the accepted design;
new RI-18 adapter/check/statement identities are explicitly pending. Pending
identity refuses both inventory and execution before loading those artifacts.
Synthetic fixtures replace only the new protocol/check and statement data;
they load the actual published c/d/RI-15/i modules under the agreed aliases.
Assertions verify bridge.c and bridge.d are the same module instances used
by the new import graph.

Independent read-only review of both complete launcher/test sources found no
provisional infrastructure blocker. Root also read both files and captured
them over published base `d72d430` in an isolated checkout. That candidate
passed **62 focused pytest cases in 2.54 s**. These include normal/optimized
fixture children, six-source execution/hash accounting, fixed alias/statement
refusals, absent or skipped execution, malformed child results, captured-byte
execution after disk replacement, endpoint drift and no generated fixture
files/caches. The author also passed Ruff lint/format checks. These 62 cases
include pending-production refusal tests; they are not a new protocol witness
count and do not establish RI-18 execution.

| Provisional root source; not published in this checkpoint | SHA-256 |
|---|---|
| `scripts/run_qr_finite_protocol.py` | `27a3df7ebbcc9b1833b6e75d1f20702cbf8097cc08d79dd4de1bb32c9eddc9ff` |
| `det8/tests/test_qr_finite_protocol.py` | `bc8dec78d9f57f4015e9175f4f7f0ebe81da99fd1fe3b00d7b3f4b31d5e8bff5` |

Final integration still requires the QR callable/import contract, independent
proof/source acceptance, reviewed adapter/check/statement hashes, exact
actual witness-count assertions and normal/optimized execution of all six
real sources. Neither source identity nor endpoint drift checks establish an
atomic filesystem capture or a sandbox for hostile code. The accepted general
runner and old four-alias launcher remain unchanged.

A separate coordinator application review derived and documented the chosen
protocol's information boundary in the [application plan](APPLICATION_WORK_PLAN.md).
On the full local span (m,x,y,z,Re c,Im c), the complete scalar outcome law is
((m+y)/2) k0 direct-sum ((m-y)/2) k1. The fixed continuation laws are complete
and have disjoint retained-r labels. Hence its linear rank is exactly two,
its kernel is m=y=0, and normalized output-law total variation is exactly
|delta y|/2. This statement excludes pre-existing source audit data and does
not condition an actual zero-probability event. A lawful opposite-X pair
with different complex-c payloads demonstrates positive-domain ambiguity.
At y=+/-1 positivity gives exceptional singleton fibers, not general tomography.

Root passed **172 exact supplemental assertions** using the full 66-coordinate
table, the accepted c model and the published identifiability helper, including
reference probabilities 0, 1/3, 2/3 and 1, rank/nullspace certificates, distance
identities and a lawful distinct-raw/quotient pair with identical Y branches.
A separate mathematical reviewer accepted the proof and reported 68 exact
scalar-table checks plus independent native-branch checks. Root incorporated
its two wording refinements: define continuations from supplied reset states
rather than impossible conditioning, and call an X question one sufficient
separating experiment rather than a uniquely necessary one. These checks
supplement the written argument; no registered witness total is increased.

The accepted c source is pinned at
`173ad68ab8be40036a28e2806bfdb03dde8bd42030772a41084736d31e05fb86`;
the identifiability helper at
`136588b80cc9d1935137c81885dc26446947dc52f81c120a0652a75b7fb268d9`.
Its bounded row solver receives the at most eighteen nonzero rows; the full
scalar table still retains all structurally zero outcome labels. The finding
was sent to QR for the new proof's limitation section without changing the
accepted design or executor scope. Completing RI-18 can establish finite
accounting; downstream observations after the reset cannot recover the lost
initial coordinates. Measured apparatus/application benefit remains separate.
