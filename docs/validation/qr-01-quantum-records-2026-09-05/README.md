# QR-01: exact quantum operations with retained records

Date: 2026-09-05. Status: executable, bounded research protocol; see the separate
`RESULTS.md` for the executed outcome. This is the first implementation of
[the research charter](../../QUANTUM_RECORD_STRUCTURE_RESEARCH.md), not a RET
SDK component, application benchmark, empirical experiment or new physical law.

## Question and useful structure

Can a finite event-order description carry ordinary quantum instruments while
preserving both quantum states and classical outcome records, independently of
which permitted event schedule an executor chooses?

The adopted quantum mathematics is standard. DET contributes the research
framing: distinguish possible instrument outcomes from committed records, give
records explicit identities, and audit what is preserved under event ordering.
A demonstrated benefit here would be a stronger check of schedule equivalence,
including detection of false equivalence after discarding records. This is not
evidence that this vocabulary is unique or that DET ontology is physically true.

For outcome `x` of event `e`, use the unnormalized map

`I[e,x](rho) = sum_a M[e,x,a] rho M[e,x,a]^dagger`.

Every outcome is completely positive by its Kraus representation. Exact
`sum_(x,a) M^dagger M = identity` makes the whole instrument trace preserving.
The trace of each positive output block is its outcome probability. Do not
normalize branches while composing maps; never discard a zero-probability
branch merely because it vanishes on one chosen state.

Retain a classical record tuple keyed by fixed `record_id`, independent of
execution order. These are mathematical output labels, **not** a claim that
remote records are instantaneously accessible. Event IDs and record IDs occupy
separate namespaces; distinct events cannot write the same record slot.

For every incomparable pair, compare the full outcome-resolved composite maps
in both orders. If all such maps commute, adjacent swaps connect any two linear
extensions of the finite partial order without changing the final map. This is
a sufficient condition within the fixed model. It is not necessary for every
restricted input/future-measurement family, and failure says nothing by itself
about a possible weaker, explicitly specified equivalence.

## Frozen finite scope

- One or two qubits; zero to four fixed, nonadaptive events in the accepted
  schema; one or two outcomes per event; one or two Kraus operators per outcome.
- Full complex operator space, checked using all `d^2` matrix units, including
  non-Hermitian units. These units are a linear-algebra basis, not physical
  preparation claims. Qubit 0 is the most-significant basis bit.
- Gaussian-rational arithmetic using pairs of exact `Fraction` values. Input
  rational components are canonical strings bounded to 64 numerator/denominator
  bits; computed components have a 4096-bit guard. No floats, tolerance, random
  seed, sampling, numerical eigensolver or Cholesky positivity shortcut.
- At most 24 schedules per selected problem. Declared operator support is
  checked entrywise as `local operator tensor spectator identity`; a graph
  declaration alone cannot make a nonlocal operation local.
- Unique outcome labels and record writes, exact instrument completeness,
  acyclic precedence and complete schedules. Unknown schema fields and
  record-conditioned/adaptive callbacks are rejected.
- Empty problems and one-schedule controls are valid algebraic cases, never
  nontrivial demonstrations of scheduling independence. An identically zero
  Kraus outcome is retained explicitly.

The parsers are the validated wire boundary. Internal matrix functions and
manually constructed dataclasses are research helpers, not a supported public
API. Input is a small trusted in-memory fixture, not an untrusted JSON service;
the runner does not claim a hardened streaming parser or an operating-system
resource sandbox. Bounds are a finite research scope, not a general QM SDK.

## Prespecified main fixtures

| Fixture | Comparison | Expected result |
|---|---|---|
| `disjoint_z` | Local Z on A and B, including Bell-state regression | Full recorded maps commute |
| `complex_disjoint` | Local Y on A and Z on B | Commute with complex entries retained |
| `damping_disjoint` | A damping instrument with two Kraus operators in one outcome; X on B | Commute; sum operator contributions, not amplitudes |
| `four_event_diamond` | CNOT predecessor, incomparable local Z/Y events, parity-measurement successor | Both full schedules agree |
| `four_event_antichain` | Local Z and phase unitaries on A/B | All 24 schedules agree, including overlapping commuting supports |
| `ordered_zx` | Same-qubit Z precedes X | Valid ordered control; pair condition vacuous |
| `unordered_zx` | Same-qubit Z and X incorrectly declared incomparable | Full recorded maps differ; expected counterexample |
| `zero_outcome` | Zero Kraus operator plus identity outcome | Both blocks retained; pair condition vacuous |

The damping coefficients are `4/5` (survival amplitude) and `3/5` (jump amplitude).
They are selected to make completeness exact; no measured damping rate is fit.

For the same-qubit Z/X counterexample, both outcome-discarded channels compose
to `trace(rho) I/2`. Starting from `|0>`, joint record probabilities differ.
Starting from `I/2`, every joint record has probability `1/4` in either order,
but branch states differ. Thus even complete joint probabilities can miss a
failure of equivalence for later quantum measurements. The study retains both
exact maps and explicit discrepancy entries; the negative control is not
reported as a successful commutation certificate.

Additional controls check Bell Z correlations, the zero outcome, and remote
Z/damping instruments on B: after summing all remote outcomes and tracing out
B, A's operator is unchanged on every two-qubit matrix unit. This establishes
the ordinary unconditional no-signalling identity **under the adopted tensor
locality and completeness assumptions**. It does not establish physical
spacelike separation, apparatus isolation or relativistic covariance.

## Independent routes and retained evidence

`exact.py` executes Kraus operations through outcome-record branches on every
matrix unit, then recovers each full superoperator column. `reference.py` uses
separate exact arithmetic, independently validates the wire contract, directly
constructs `S[(i,j),(k,l)] = sum_a M[i,k] conjugate(M[j,l])`, and composes those
superoperators. It imports neither the executor nor DET8. These are distinct
implementations of the same adopted mathematics, not independent experimental
evidence. Analytic controls and adversarial tests reduce common-mode risk;
they cannot eliminate it or exhaust all valid instruments.

`study.py` checks every full schedule and both orders of every incomparable
pair against the reference. `results.json` retains the complete fixture wires,
record-resolved maps, pair comparisons, explicit mismatch witnesses, counts,
runtime identity and memory high-water mark. Its source ledger covers exactly
the five named protocol/source/test files, not the repository or directory as
a whole. Hashes are local integrity checks, not authentication. Source equality
is checked before/after execution. Output is create-only; `--verify` performs
a fresh, read-only recomputation and checks the same source ledger.

Reported rational bit growth is the maximum among retained **main schedule
maps**, not the peak of all intermediate Fraction allocations. Reported RSS is
the process high-water mark, not an isolated allocation delta or performance
benchmark. Pair, explanatory and remote-control work is separately counted.

## Run and review

From the primary checkout, use the existing Python environment; no dependency
or lockfile changes are needed. Coordinate with concurrent RET timing work
before computation. Use a fresh external bytecode directory for each run:

```sh
qr01_cache=$(mktemp -d /tmp/det8-qr01-bytecode.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr01_cache" -m pytest docs/validation/qr-01-quantum-records-2026-09-05/test_qr01.py -q -p no:cacheprovider
.venv/bin/python -I -X pycache_prefix="$qr01_cache" docs/validation/qr-01-quantum-records-2026-09-05/study.py
```

For a fresh-process replay, create another external cache directory, add `-O`
to Python and add `--verify` after the script path. Study checks use explicit
exceptions and remain active under optimization. Do not overwrite an old result
to hide a discrepancy: retain it and open a separately versioned study.

## Boundaries and next bridge

No RET files, calibration state, application gates or legacy physics modules
are modified by this study. No measured observables are analyzed, so it cannot
establish general observational compatibility or a noise explanation for any
discrepancy. Schedule independence is not Lorentz covariance, emergence of a
metric, Einstein dynamics, a derivation of QM, or proof of DET ontology.

The next bounded question (QR-02) is which coarse-grainings of classical
records preserve stated future predictions and composition. QR-03 can then ask
what predictive history summaries suffice. A Track-B geometry bridge still
requires an explicit quantum-to-record-to-order model and scale-consistency
tests before geometry or dynamics claims. RET integration remains gated on the
separately hardened SDK and application-specific validation.
