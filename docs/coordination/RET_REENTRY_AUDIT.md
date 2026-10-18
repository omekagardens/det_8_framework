# RI-29 — RET readiness and publication handoff

23 September 2026. Read-only coordinator audit at published commit
`a8d6890efb05676e83d40f3e571267734709b8f5`. This records the concrete next
engineering and publication decisions after the usage-limit interruption.
It does not repeat the existing bank design or authorize RET implementation.
The original independent review and all accepted QR sources remain fixed.

## Two different dependencies

The [publication backlog](PUBLICATION_BACKLOG.md) correctly separates these
lanes. G2 is the prerequisite for calibrated operating-characteristic claims,
not a prerequisite for every synthetic source preview.

| Lane | Actual next dependency | What completing it would establish |
|---|---|---|
| RI-12 synthetic comparator | Owner-coordinated review and isolated testing of its existing RET source dependencies | Reproducible fixed arithmetic and replay from published source |
| G2 evaluation pipeline | A shared evaluator consuming verified inputs, then the remaining source, consumption, rehearsal and authorization controls | First a tested engineering path; calibrated performance only after the separate evaluation gates |

The comparator makes no action-ranking, workflow-decision, closure or policy
performance claim. Its current tests explicitly check zero workflow decisions.
Publishing it still exposes the RET facade's broader planning, covariance and
workflow surface. Its 34 comparator tests alone cannot justify support for
that whole surface. The current RET owner's instruction not to begin RET
advancements was confirmed by that owner on 23 September; this audit assigns
neither source edits nor preview publication. The failed September handoff is
not accepted review evidence.

## What actually exists

Paths in this section identify the local working baseline, much of which is
not yet published. They are not a claim that the remote checkout contains RET.

- `det8/ret/benchmarks/locked_bank_reader.py` implements `BankFileReader`:
  anchored regular-file verification, caller-supplied whole-file hash checking,
  bounded element-aligned byte reads and a final full rehash. Its caller inputs
  are not authenticated authority. Static searches found no Python consumer
  or direct reader tests elsewhere in the current tree.
- `runner.py:_run_predictive` still draws its observation through the
  development RNG. `_run_replication` dispatches root-seeded scenario functions;
  `rehearsal_execution.py` calls that dispatch. There is no integrated bank
  provider or seedless shared evaluation core. `refuse_locked_validation`
  still rejects locked execution.
- Inventory, codec and public-synthetic generation already exist. The codec
  validates finite binary64 payloads, integer ranges and identical Objective
  seed columns. These checks do not provide scenario-coordinate consumption
  accounting or official ledger binding.
- The existing `ret-sdk-bank-input-generation-design-2026-09-05.md` already
  specifies the `ReplicationInputs` operations, immutable values and source
  references, consumption receipts, RNG separation and independent checks.
  That design should guide implementation rather than be rewritten here.
- `det8/tests/fixtures/ret_input_provider_reference_v1.json` contains candidate
  pre-refactor rows for replicates 0/1 across 18 scenarios. No consuming test
  was found. Its identity records the runner and candidate, not the full
  dependency/runtime closure. It needs assessment before use as an oracle;
  regenerating it after a refactor would not independently verify equivalence.
  Its development root differs from the public generator's literal
  `bytes(range(32))` root. Compare separately matched references; never compare
  different-root outputs or widen the generator's root acceptance to force
  agreement. The owner confirms 36 rows, 1,596 metric cells and four retained
  policy-trace rows; this is not a full decision/evidence trace.

## Smallest evaluator increment, when RET resumes

Reserve the predictive-family seam only: existing `runner.py`, new private
`locked_bank_inputs.py`, new input-provider and reader test files, and the
reader itself only if lifecycle tests expose a concrete defect. Cover the
three `LIN-PRED-*` scenarios before expanding to other families.

Extract the present predictive metric calculation into one seedless function
that requests its observation from a lazy input object. Preserve the existing
evaluation order, including constructing the prediction before drawing the
observation. The development adapter retains its draw order; a private test
input provider decodes exactly two little-endian
binary64 elements at scalar offset `2 * replicate` from the verified
`observations` segment. Both call the same evaluation function. This test
bridge grants no official locked-run authority.

Acceptance must demonstrate exact pre-refactor metric agreement for all three
scenarios at the unchanged development root, plus separately matched,
independently checked public-root input/evaluation references. It must verify
immutable values, independent known byte vectors, signed-zero and
subnormal preservation, coordinate/shape/dtype validation, and receipts derived
from actual reads. Patch scenario RNG, subseed and draw helpers to raise during
bank-backed tests. Exercise wrong hashes, truncation, replacement, symlink and
hard-link refusal, constructor cleanup, post-close access and final verification
failure with tiny public synthetic fixtures. A failed final check prevents
successful completion. Rehash the whole file at the owning session boundary,
not once per replication. Preserve the official locked-execution refusal.

Expansion must retain continuous training/held-out streams and the archived
correlation-stream restart. Policy potential outcomes use action occurrence,
not global look; random ordinals index the existing utility-sorted eligible
menu. Stored Objective seeds still drive deterministic SDK inference Monte
Carlo. Bootstrap resamples belong to aggregate analysis. None of these inputs
can be silently regenerated, relabeled, or converted into independent evidence
merely by assigning hashes. The existing complete design remains authoritative.

## Smallest comparator publication increment, when assigned

Prepare an isolated candidate with the eleven RET modules already listed in
the publication backlog, the reviewed tomography prerequisite, and the
accepted comparator source, tests and document. Use published initializers,
scheduler and identifiability sources. Preserve production bytes initially.

Capture the candidate's actual import closure and all its source hashes;
verify comparator arithmetic/replay in normal and optimized modes and select
the relevant existing facade, inference, covariance, provenance and replay
tests after inspecting their dependencies. Review the exposed facade before
acceptance. Do not bundle the entire dirty baseline to satisfy an import.

`det8/ret/provenance.py` inventories the RET Python files present in an
installation plus two engine files. The historical 42-path inventory is not
a hard-coded required file set, and it is not the comparator's full execution
closure. A smaller candidate can generate a different identity and fresh
manifests. Record that identity separately; do not relabel historical manifests
or represent the SDK inventory as a complete binding of application execution.

The full rehearsal, six-environment matrix, clean-wheel checks, source freeze,
named-reviewer authorization and independent custody remain separate G2 work.
No source preview establishes measured application benefit or closes G2.

## Static evidence and limits

Two independent coordinator reviews inspected the reader/evaluator seam and
the comparator publication boundary. The coordinator inspected the relevant
source and checked the remote branch independently. No project code, bank,
rehearsal, simulator or calibration evaluation was executed for this audit.
Historical test counts remain historical.

| Local source | SHA-256 at audit |
|---|---|
| `det8/ret/benchmarks/locked_bank_reader.py` | `bfd017fd7ca12075bfcaf30f0dfcb2c74b85d3ae40a59fddd06aeda4fba12e3b` |
| `det8/ret/benchmarks/runner.py` | `ff03925e6cb5e5f9e7640186dc80218af443340068af9f18343ef902f95140aa` |
| `det8/ret/benchmarks/locked_bank_inventory.py` | `731863a5cfdf0acb1f1393309ec91ed60b0565d26798328777dba2e4765c1fe0` |
| `det8/ret/benchmarks/locked_bank_generation.py` | `115779ec578c835e70abb9f458a8fc1d1fe7d6d60177e755a72504091db5c107` |
| `det8/ret/benchmarks/calibration_v1.pre_eval.json` | `6178b42509c17c91f92e7cb10b97e0eb8d8af70f74144a124c4d6dc02e916171` |
| `det8/tests/fixtures/ret_input_provider_reference_v1.json` | `52a866472a295a552846f66af597c806778edcf68585df1bff7d17feff2e88c7` |

The entry snapshot retained 1,048 tracked and 965 untracked file versions.
Only coordinator documents are reserved for this audit. The RET owner returned
a concordant read-only handoff and confirmed the explicit implementation pause;
the earlier technical reference-capture hold is a different matter. No RET
source reservation is active. QR was separately asked for an application step
using published dependencies. Its assessment does not resume RET or authorize
locked evaluation.
