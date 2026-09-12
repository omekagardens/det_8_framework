# Reconciliation results and next decision

12 September 2026. The current `ret` checkout remains the working authority.
The review takes useful structure from `qr-05-bridge` at
`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`, without merging it or treating
BW–DO as locally accepted completions.

## Outcome

The branch is valuable as a source of candidate constructions and adversarial
questions, but its stronger geometry, pair-kernel and joint-anchor conclusions
cannot be inherited. Passing its selected tests did not establish those
conclusions. See the [audit](README.md) and its detailed reports.

A corrected finite measurement-channel calculus is now implemented locally.
It formalizes identification of a **joint target on one common world class**.
Observation partitions and an independent pair-separator/hitting-set oracle
agree on the full native report for all five fixed packets and 27 subsets.

| Fixed packet | Inclusion-minimal identifying channel sets | Minimum size |
|---|---|---|
| Joint (a,b), channels a,b,xor | {a,b}, {a,xor}, {b,xor} | 2 |
| Colour and scale, duplicate colour channel, injected scale oracle | {colour,external_scale}, {colour_copy,external_scale} | 2 |
| Constant target, no channels | Empty set | 0 |
| Distinct targets, constant observation | None | Impossible |
| Target a, channels a,b,xor | {a}, {b,xor} | 1 |

The XOR example identifies the varying coordinate on either axis slice but
not the joint target on all four worlds. This directly blocks the inference
from DO's separate familywise checks to joint identification. The scale
example makes the external anchor an explicit supplied oracle, not a proved
instrument. Redundant internal channels do not resolve its scale ambiguity.

The general finite-set equivalence between fiber constancy and hitting every
different-target pair's separator set is proved in [CALCULUS.md](CALCULUS.md).
The finite tests verify the implementation and fixed controls; they are not
a machine-checked proof for every input or a statistical performance estimate.

Practical mathematical uses include identifying redundant measurements, finding
the smallest channel sets for a declared target, and exhibiting precisely what
information an added reference must supply. Quantum/geometry comparisons can
use the same interface when their channels and joint model class are defined.
Applying it to noisy instruments or RET policy selection still requires a
probabilistic observation model, costs and calibrated uncertainty; the exact
table does not provide those automatically.

## Verification

Six sources were frozen before the first new mathematical execution:
contract, protocol, implementation, driver, tests and the literal-hash-pinned
BM evidence utility. That utility supplies evidence helpers only; no older
mathematical executor was run by this study.

- First capture: 5 cases, 4,349 canonical report bytes; successful.
- CPython 3.14.0 normal suite: 19 tests passed (reported 0.042 s).
- CPython 3.14.0 optimized suite: 19 tests passed (reported 0.041 s).
- Normal and optimized full-report replays: exact match.
- One CPython 3.11.6 full-report replay: exact match.
- Static AST parsing and scoped Ruff checks passed.
- No frozen source was changed after the first execution.
- Final metadata checks match all six new frozen identities and all 12 BV
  identities; BV mathematics was not rerun. All 83 checked local and pinned
  source-document links resolve to existing files (pinned line anchors are in range).

The 19 tests include the independent oracle, refinement and collision
witnesses, minimal-versus-minimum distinctions, malformed native inputs,
mutation refusal, exact native type preservation, authenticated evidence
round trips and create-only publication. Four named exact regressions retain
the same-data union-bound, link/all-pair max-plus, visibility/CHSH and signed
inverse-path cancellation lessons.

Analysis is limited to 30 seconds and each suite to 60 seconds. Fixed packet
limits are eight channels, 64 worlds and eight target coordinates. These are
research-interface bounds, not a comprehensive hostile-input resource proof:
plain string and integer payload sizes are not separately capped by the pure
in-memory utility. The study itself consumes the fixed byte-pinned protocol.

Evidence:

- [First source freeze](source-freeze.json):
  `5ab341a61d4d94c3da23b2a71a38d85b204b0364304017b02e574d381df05156`.
- [First capture](results.json):
  `23fa47dba62e1688aeb8b59a18290ec74b2a3e18a4d784ddbe07da3ca08b4291`.
- Canonical native report:
  `d4e63ec2f667b0ad462e6f3f1a5f11bc9c975935ea6be9f3f5d02a68eb9ea4fc`.
- [Recorded verification outputs](verification.json).
- [All 45 branch gate source/capture inventories](branch-source-inventory.json).

For read-only reproduction from the repository root:

```sh
python3 -B docs/validation/qr-05-bridge-reconciliation-2026-09-12/test_calculus.py
python3 -B -O docs/validation/qr-05-bridge-reconciliation-2026-09-12/test_calculus.py
python3 -B docs/validation/qr-05-bridge-reconciliation-2026-09-12/study.py --replay docs/validation/qr-05-bridge-reconciliation-2026-09-12/results.json
```

Do not overwrite the retained freeze or capture. Publication prose, source
inventory and this verification summary are not prospective mathematical
inputs and are intentionally outside the six-source freeze.

## What was adopted, and what was not

Adopted here: CY/DO's target-specific observational-quotient idea, corrected
to one common world class; BW/BX's useful calibration-layer separation,
corrected for population/estimate semantics and probability composition;
exact regression witnesses to prevent several overclaims recurring.

Retained as future candidates, not yet imported implementations:
order/count controls, all-pair max-plus completion, properly named
finite-difference and spectral-positive-part constructions, interval-density
and matched-adversary diagnostics.

Not adopted: a physical E/pair-kernel closure, a BD operator identified by
the wrong coefficients, general order recovery from a signed inverse,
bijection-only results labeled unrestricted Lorentzian GH optima, empirical
fits labeled uniform convergence, uncalibrated growth tests as universal
no-go results, or DN registry promotion. The local core/RET/claim-registry
work was not changed. No branch captures were regenerated or repaired in
place. `temp_qr.md` remains unrelated and untouched.

The final status comparison retains all 231 pre-existing dirty entries, adding
only this reconciliation directory and the quantum/gravity research roadmap.
No merge, commit or remote push was performed in this audit turn; the new work
is local and ready for a scoped research commit.

## Next bounded step

Specify a **common-world geometric target/channel contract**, design-only:

1. Declare one world class and joint targets covering the proposed geometric
   questions: order/orientation, conformal structure, density and scale.
2. State exactly what each channel receives. Supplied coordinates, labels,
   an order matrix or a kernel cannot silently become measured information.
3. Give exact equal-observation/different-target witnesses; identify which
   additional channel would split each collision and what would justify it.
4. Keep ideal population channels separate from finite, noisy acquisition.
   Carry calibration and selection premises before claiming usable inference.

Then separately repair the pair-operator/causal-order contract, the precise
correspondence-distance and noncollapse target, and stochastic growth/null
calibration. Do not combine these repairs into a claim that one passed gate
establishes physical geometry.

RET hardening need not block this isolated finite mathematics. It still
gates calibrated SDK integration and downstream application readiness.
Materials monitoring and anomaly triage require their own measured-data
evaluation. No Lean installation, acquisition, new law, ontology, gravity
dynamics, book revival or deferred clock coupling is implied.
