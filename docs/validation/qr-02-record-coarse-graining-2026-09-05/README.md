# QR-02: when can a record be forgotten?

Date: September 5, 2026. Bounded, exact mathematical research. This extends
[QR-01](../qr-01-quantum-records-2026-09-05/RESULTS.md) under the
[quantum-record charter](../../QUANTUM_RECORD_STRUCTURE_RESEARCH.md). It does
not change RET, QR-01 evidence, physical laws or application acceptance gates.
Executed findings belong in the separate `RESULTS.md` and `results.json`.

## Research question and adopted mathematics

A source instrument produces an unnormalized quantum block `I_x(rho)` and a
classical fine record `x`. A fixed deterministic grouping `g(x)=z` forgets
distinctions between records but retains the quantum state:

`C_z(rho) = sum_{x:g(x)=z} I_x(rho)`.

This is ordinary classical postprocessing of a quantum instrument. Sum the
CP maps (equivalently concatenate their Kraus lists); do **not** coherently sum
Kraus amplitudes. Never renormalize or prune branches while composing maps.
Classical grouping is not a model of recombining coherent histories before a
record exists. Repeated deterministic grouping is associative by finite sums;
that algebra alone does not guarantee preservation of future record access.

Fix fine-record-conditioned future instruments `F[x,y]`, a proposed coarse-only
future instrument `G[z,y]`, and a common retained future outcome `y`. Compare:

`A[z,y] = sum_{x:g(x)=z} F[x,y] composed with I_x`

`B[z,y] = G[z,y] composed with C_z`.

The declared output is the full quantum state plus the coarse and future
records `(z,y)`. Equality of their full linear maps certifies this candidate
for every initial density matrix in the fixed finite Hilbert space and every
subsequent measurement of that retained output. It does not preserve the
forgotten fine label or future controls that secretly continue to read it.

### Three distinctions the verifier must keep separate

1. **Arbitrary classical-quantum inputs.** For independently variable blocks
   `sigma_x`, a fixed candidate factors the fine future through grouping iff
   `F[x,y] = G[g(x),y]` on the whole operator space for every fine label and
   future outcome. Equality within every group is necessary here, not merely
   sufficient: vary one input block at a time.
2. **Reachable source outputs.** With the specified source `I_x(rho)`, only
   `A[z,y] = B[z,y]` is required. This is weaker. Fine branches share one
   initial state and occupy a restricted subspace; quantum outputs can retain
   a classical distinction, or fixed branch probabilities can permit an
   averaged replacement. A failed arbitrary-block condition is not a failed
   reachable candidate. Aggregate equality need not hold term by term.
3. **Existence of any physical replacement.** Failure of this candidate does
   not prove impossibility. Equal coarse states with unequal required future
   outputs do prove impossibility for a coarse-only operation. Even existence
   of a linear factor is insufficient: a physical quantum instrument needs
   completely positive maps and trace-preserving summed outcomes. An inverse
   linear map may fail positivity. This study checks explicit candidates and
   two analytical impossibility controls, not a general channel-synthesis solver.

For linear maps, let `K(rho) = direct_sum_z C_z(rho)` be the complete grouped
source output. The general identifiability condition is kernel inclusion
`ker(K) subset ker(A)`, where `A` is the required coarse-plus-future output
map defined above. It identifies a linear factor on the image only;
it does not provide a completely positive, trace-preserving extension. No
general kernel/SDP/positivity solver is implemented in QR-02.

## Fixed wire contract

`schema_version = det8-qr02-problem-v1` with exactly these fields:

```text
qubits: 1 or 2
source: instrument
groups: [{fine: fine_label, coarse: coarse_label}, ...]
fine_future: [{fine: fine_label, instrument: instrument}, ...]
coarse_future: [{coarse: coarse_label, instrument: instrument}, ...]

instrument = {
  support: [sorted unique qubit indices],
  outcomes: [{label: label, kraus: [full_matrix, ...]}, ...]
}
```

Each supplied instrument has one or two outcomes, each with one or two Kraus
operators. Matrices and bounded Gaussian-rational cells use QR-01's wire
schema. Fine labels must match the source outcomes exactly, with no duplicates
or missing zero outcomes. The group map is total; its image defines the coarse
labels. Exactly one future instrument is supplied per fine/coarse label. All
future instruments have the same fixed outcome-label inventory. Labels use
`[A-Za-z0-9_+.-]{1,128}`. Unknown fields and callbacks are rejected.

There is one source stage and one future stage, with at most four retained
`(coarse,future)` blocks. The source precedes the future by construction; no
spacelike or incomparable-record access is modeled. The small explicit
conditioning table is only for this QR-02 comparison, not the adaptive graph,
causal-past API, or scheduler generalization deferred to QR-04.

All supplied instruments are checked for exact Kraus completeness, dimensions
and declared tensor support. Grouped source maps may implicitly contain up to
four Kraus terms per coarse outcome; they are retained as sums of maps and
are not incorrectly forced into QR-01's two-Kraus input bound.

## Prespecified fixture inventory

| Fixture | Proposed replacement | Arbitrary-block equality | Reachable equality |
|---|---|---:|---:|
| `independent_x_after_z` | Forget Z record; same X measurement afterward | Yes | Yes |
| `no_merge_control` | Keep both labels, retain their separate future controls | Yes | Yes |
| `naive_controlled_x` | Forget Z record; replace record-controlled I/X with I | No | No |
| `reachable_reset_repair` | Same fine process; use a complete reset-to-zero channel | No | Yes |
| `erased_record_irrecoverable` | Source measures Z then resets; forget outcome before controlled I/X | No | No |
| `coin_averaged_future` | Fixed 9/25–16/25 coin; replace I/S controls with their channel mixture | No | Yes |
| `two_qubit_local_forgetting` | Forget local A record, retain full AB state and local B future | Yes | Yes |
| `multi_kraus_grouping` | Merge two weighted dephasing outcomes before a common Y measurement | Yes | Yes |
| `zero_branch_control` | Keep an identically zero source branch in the contract | No | Yes (unreachable-branch control) |
| `phase_flip_nonphysical_inverse` | Forget a phase-error label before undoing it; propose identity | No | No |

`S=diag(1,i)` and coin amplitudes `3/5,4/5` permit exact rational
calculations. Fixtures are selected research cases, not measurements, a random
sample of channels, or an externally preregistered experiment. The no-merge
and zero-branch controls must not be advertised as nontrivial compression.

Additional explicit controls:

- Forgetting a recorded Z outcome dephases `|+>`; coherently summing its
  projectors gives identity instead. A later X+ probability is 1/2 versus 1.
- For measure-and-reset followed by I/X control, initial `|0>` and `|1>` give
  the same coarse state `|0><0|`, but different required future states. This
  proves no coarse-only future can satisfy both, not just failure of identity.
- A forgotten random phase error has channel `K(rho)=9/25 rho+16/25 Z rho Z`.
  Fine-label correction recovers `rho`. K is linearly invertible, but its
  unique inverse sends `|+><+|` to diagonal 1/2 and off-diagonal -25/14, which
  has negative expectation in `|+>`. Thus no everywhere-positive/CPTP recovery
  exists, even though a linear inverse does. This is not a nonphysical Kraus
  instrument smuggled through validation: the inverse is an algebraic negative
  control outside the candidate API.
- Coarse record probabilities alone do not replace the quantum output: after
  forgotten Z measurement, `|0>` and `|1>` have the same sole coarse-label
  probability but are distinguished by a later Z measurement.

## Implementation and independent reference

`coarse.py` uses QR-01's frozen exact operator executor to propagate each
matrix unit through fine and grouped branches. It checks the reachable routes
and the unrestricted candidate separately. `reference_qr02.py` independently
validates the QR-02 wire contract and composes/sums full superoperators using
QR-01's independent reference. Neither reference imports the executor.
The reused QR-01 source bytes are SHA-pinned; they are never modified.

The six returned map bundles are `source_fine`, `source_coarse`,
`fine_then_forget`, `forget_then_candidate`, `unrestricted_fine_future` and
`unrestricted_coarse_future`. In the last two, a `fine` key indexes the
independently selectable **input** block used to test arbitrary CQ inputs;
it is not a fine output record secretly available after coarse-graining.

`study.py` compares every retained map from both paths, saves the complete
inputs and outputs and discrepancy witnesses, and runs the analytical controls.
Tests have separate fixtures. The study's explicit validation remains active
under `python -O`. There are no DET8/RET package imports, new dependencies,
Monte Carlo draws, floating-point equality tolerances or experimental data.

The result source ledger covers this README, `coarse.py`, `reference_qr02.py`,
`study.py`, `test_qr02.py`, plus the two reused QR-01 arithmetic/execution
sources. It checks source stability before/after work, creates results without
overwriting an existing file, and requires a fresh replay to match both source
identities and the exact retained result bytes. Source hashes are local
integrity checks, not authentication or proof of correctness. Inputs and
artifact files are small trusted local research objects, not an untrusted
network service or a general resource sandbox.

## Execution and boundaries

Coordinate with RET before numerical/test work. Use the existing environment,
isolated Python and an external fresh bytecode directory:

```sh
qr02_cache=$(mktemp -d /tmp/det8-qr02-bytecode.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr02_cache" -m pytest docs/validation/qr-02-record-coarse-graining-2026-09-05/test_qr02.py -q -p no:cacheprovider
.venv/bin/python -I -X pycache_prefix="$qr02_cache" docs/validation/qr-02-record-coarse-graining-2026-09-05/study.py
```

Use a new cache and add `-O` plus script option `--verify` for read-only replay.
Retain failures in separately versioned evidence; do not overwrite results.
Runtime/RSS are run accounting, not a performance benchmark; retained rational
bit lengths are not peak intermediate-allocation measurements.

Useful success means distinguishing a valid compression, a bad replacement,
true lost information and an unphysical inverse. No storage speedup, calibrated
decision benefit, observational compatibility, ontology proof or gravitational
derivation is established. QR-03 may later investigate summaries for specified
future families; QR-04 covers genuinely adaptive causal-past restrictions.
Track-B still needs an explicit quantum-to-record-to-order construction and
scale-consistency tests. RET integration waits for its own hardened contracts.
