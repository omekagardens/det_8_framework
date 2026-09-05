# QR-03: predictive history summaries for declared future questions

September 5, 2026. Bounded exact mathematical research, following
[QR-02](../qr-02-record-coarse-graining-2026-09-05/RESULTS.md). Completed QR-01,
QR-02 and the charter are preserved in commit `e3c891e` on `origin/ret`.
This directory is a new research milestone, not a RET SDK change.

## Question and scope

Which distinct source histories give the same conditional predictions for a
declared family of future measurements, for every initial quantum state?
Find the coarsest valid partition of the possible histories and test an
explicit proposed summary against it. A summary valid for one future family
need not work after the family expands.

This is a **predictive equivalence** test, not QR-02's synthesis/comparison of
a physical coarse-only replacement channel. Equivalent labels do not make
the underlying quantum states identical unless the future family is rich
enough to determine them. Nor do they preserve all past-history probabilities,
record-controlled feedback, unmodeled side information or every multi-step
future process. No raw experimental records are deleted.

The first implementation uses one qubit, one or two fixed source events,
at most four histories, and one to three future instruments. Each instrument
has one or two outcomes and one or two Kraus operators per outcome. A future
setting is fixed independently of the hidden fine history; a policy that uses
only the declared summary to choose among these settings inherits the one-step
probability guarantee. General adaptive graphs remain QR-04 work.

All initial density matrices of the qubit are covered analytically by the
coefficient test below. The ten probe states supply exact physical discrepancy
witnesses; they are not substituted for the all-state coefficient criterion.

## Conditional probabilities and an exact polynomial criterion

For source history `h`, let `I_h` be its unnormalized completely positive map.
For future setting `u`, outcome `y`, let `F[u,y]` be the quantum outcome map.
Define real linear functionals on Hermitian input operators:

`d_h(rho) = trace(I_h(rho))`

`n_h[u,y](rho) = trace(F[u,y](I_h(rho)))`.

When `d_h(rho)>0`, the conditional prediction is `n_h/d_h`. Two nonzero
histories are equivalent for the selected future family exactly when

`n_h[u,y](rho) d_k(rho) - n_k[u,y](rho) d_h(rho) = 0`

for every setting/outcome and every input where both histories are possible.

Use real Hermitian basis `(P0, P1, X, Y)` and real coordinate vector `t`.
If `a,b,c,e` are the coefficients of `d_h,n_h,d_k,n_k`, the homogeneous
quadratic has diagonal coefficients `b_i c_i - e_i a_i` and off-diagonal
coefficients `b_i c_j + b_j c_i - e_i a_j - e_j a_i` for `i<j`. Store these
ten monomial coefficients directly; no extra symmetric-matrix factor of 1/2.

Every nonzero CP history is possible on a full-rank density matrix, in
particular `I/2`: its probability there is a positive sum of Kraus squared
norms divided by dimension. Thus all nonzero histories share an open domain
where denominators are positive. Ratio equality is transitive there. Scaling
trace-one positive-definite matrices to the full positive-definite cone and
using homogeneity shows that equality on physical inputs is equivalent to
vanishing of all real polynomial coefficients. This supplies an equivalence
relation and a unique coarsest partition of the nonzero histories.

**Zero histories must be removed from this ratio comparison first.** An
identically zero CP map has no conditional distribution; cross-multiplication
alone would falsely identify it with every history and break transitivity.
They remain explicitly retained as `NEVER_POSSIBLE`, not as prediction classes.
A nonzero history that is impossible only for a particular input is not removed.

The conditional prediction, not the history probability `d_h`, is what the
partition preserves. Both functions remain in the evidence. Forgetting a fine
label can lose evidence about past events or other hypotheses; this result
does not license dropping provenance from RET or from measured data.
The class identifies a prediction function of the same supplied initial state
`rho`, not a probability computable from the class label alone without its
source model and input-state context.

## Guaranteed physical witnesses

Use full-rank density matrices `(I + x X + y Y + z Z)/2` at these ten Bloch
vectors: the origin, positive/negative half-unit steps along each axis, and
the three positive half-unit pair combinations `(1/2,1/2,0)`, `(1/2,0,1/2)`,
`(0,1/2,1/2)`. Their lengths are strictly below one.

A polynomial of degree at most two in `(x,y,z)` is determined by these ten
points: the center determines its constant, opposite axial pairs its linear
and square terms, and the three paired points its cross terms. Consequently
each nonzero ratio-difference polynomial has an explicit witness in this
bank, with both history denominators strictly positive. Store the input
density matrix, the setting/outcome, both history probabilities and both
unequal conditional probabilities. No random search or numerical positivity
solver is required.

## Fixed input contract

The wire object has exactly these fields:

```text
schema_version: "det8-qr03-problem-v1"
source: QR-01 problem (qubits=1; one or two events)
schedule: [event_id, ...]   # a complete permitted source schedule
futures: [{setting: bounded_label, instrument: {support: [...], outcomes: [...]}}]
summary: [{record: [[record_id, outcome_label], ...], label: bounded_label}, ...]
```

Future instruments use the QR-02 instrument shape but are validated directly
through the pinned QR-01 paths. There must be one to three unique settings.
The summary table must cover every source record exactly, including zero-map
records. Records must be canonical, sorted, unique tuples on decoding; the
table has at most four rows. Summary labels and settings use the bounded
QR-01 identifier grammar. Unknown fields, incomplete instruments, hidden
support violations, cyclic/invalid schedules and missing zero records fail.

Candidate-summary validity is checked only on nonzero histories: every pair
sharing a candidate label must be predictively equivalent. Zero records keep
their candidate label as metadata but never acquire a conditional prediction.
The number of computed prediction classes excludes them, and vacuous controls
are identified explicitly.

## Prespecified fixtures

| Fixture | Future questions | Expected live classes | Candidate |
|---|---|---:|---|
| `coin_tomography` | X, Y, Z after quantum-independent coin | 1 from 2 | Merge valid |
| `phase_z_only` | Z after recorded I/Z phase error | 1 from 2 | Merge valid |
| `phase_tomography` | X, Y, Z after same source | 2 from 2 | Merge invalid |
| `projective_z_x_only` | X after Z measurement | 1 from 2 | Merge valid |
| `projective_z_tomography` | X, Y, Z after same source | 2 from 2 | Merge invalid |
| `two_stage_zx` | X, Y, Z after ordered Z then X | 2 from 4 | Keep last X record only; valid |
| `repeated_z_zeros` | X, Y, Z after ordered Z then Z | 2 from 2, plus 2 never possible | Keep last Z; valid control |
| `zero_branch_control` | Z after identity/zero instrument | 1 from 1, plus 1 never possible | Valid but no live compression |

The coin uses rational amplitudes `3/5` and `4/5`. No rates are fitted.
For `phase_tomography`, testing only the maximally mixed input misleadingly
suggests equality; the complete criterion and full-rank witness bank must
detect the difference. For the one-qubit tomography family, equality of X/Y/Z
probabilities fixes the normalized quantum state; smaller families need not.
This informational completeness statement is not generalized to two qubits.

The expanded families must refine, never merge, previously distinct classes.
The two source-matched family pairs above demonstrate strict refinement.
For the two-stage case, earlier Z history probabilities remain distinct even
though last-X alone suffices for these future measurements.

## Independent routes, evidence and boundaries

`predictive.py` propagates the Hermitian basis through source/future operations
using the SHA-pinned QR-01 exact executor. `reference_qr03.py` independently
validates the schema and obtains the same real functionals through the pinned
independent superoperators. Polynomial comparison, zero handling, partitions
and conditional witnesses are independently implemented in each path.

The shared output contract (used by the study) is:

- `histories`: canonical record list, status, denominator coefficients, and
  numerator coefficient rows keyed by `(setting,outcome)`;
- `pairs`: every unordered live-history pair, all per-question quadratic
  coefficient rows, equality flag and a full-rank witness for each failure;
- `classes`: canonical lists of live records in each maximal class;
- `never_possible`: canonical zero-record list;
- `candidate_valid` and `candidate_conflicts`: full failed same-summary pairs.

Scalar coefficients and probabilities are canonical rational strings. Matrices
use QR-01 rational-complex wire cells. Coefficients have a 4096-bit arithmetic
guard; validated source/future components retain the 64-bit input bound.
Internal helpers are trusted research code, not public hardened APIs.

`study.py` retains fixtures, all coefficients, pair comparisons, physical
witnesses, class partitions and controls. The source ledger covers this README,
the four new Python files, and the two reused QR-01 sources. Completed QR-01
and QR-02 artifact identities remain bound and unchanged. Capture is create-only;
fresh optimized replay checks source identity, exact results and byte stability.
Hashes are local integrity evidence, not authentication or preregistration.

Coordinate with concurrent RET timing work, then run in the existing Python
environment with `-I`, an external fresh `-X pycache_prefix`, and no pytest
cache. Use `study.py --verify` in a fresh optimized process to replay. No RET
imports, dependency changes, sampling, floating-point equality tolerances,
new measured data or application gate advancement are part of this study.

The value sought is a precise, limited summary contract, not an ontology proof,
an experimental accuracy claim, a universal scalar kappa, or a gravity model.
Track-B still needs a record-to-order construction and scale-consistency tests;
RET still needs its own hardening and application-specific calibration.
