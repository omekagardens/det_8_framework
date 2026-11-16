# PIM001 finite integrated result

The finite integrated baseline runs and reproduces the complete registered
growth/readout results and the specified Gaussian attachment results. It preserves
the demonstrated failure of full endpoint field-state covariance. This is a
finite computational result accepted with scope after distinct DET Energy
Research integrated-output review and coordinator disposition. It is not a
physical theory admission. Option B / Status M are unchanged.

## Exact outcomes

Both prepared bits enumerate exactly 60 distinct, positive marked histories with
conditional mass one: 15 structural sequences times four suffix-bit pairs.
The literal accepted 15-row structural ledger is checked for both preparations,
including every exact terminal counter tuple and D/Y value. Every actual ideal,
including empty, partial and full slots, has its original positive q; complete
structural and fair-mark rows normalize exactly. Marks remain immutable and
terminal counters equal strict descendant counts, with no wrap.

| Quantity | i=0 | i=1 |
| --- | --- | --- |
| Joint cells (00,01,10,11), denominator 1320 | (246,295,0,779) | (456,290,0,574) |
| P(D=1) | 779/1320 | 574/1320 |
| P(Y=1) | 1074/1320 | 864/1320 |
| Valid causal-commutator / old W₂ checks | 60 / 60 | 60 / 60 |
| Cover-link mean range on complete support | [1/2,5/2] | [1/2,5/2] |

The registered contrasts are ΔD=−41/264 and ΔY=−7/44, with
ΔY=(42/41)ΔD and ΔY−ΔD=−1/264. D is contained in Y on this support; their
positive distinction masses are 295/1320 and 290/1320.

At every prepared, third-birth and fourth-birth stage, the computed target-first
matrix obeys K=C−Cᵀ. Every appended field leaves earlier coefficients and exact
V and W blocks unchanged, including W₂/β=½[[1,−i],[i,1]]. The unread mixtures
retain that block using the original complete probability law. Exact leading
principal determinants of V/β are positive for every stage and history; W
positivity is inherited from the displayed canonical Gaussian factorization.

The supported Iₓ=∅, Iᵧ={x} witness retains the central x variance β/2 at stage
three and gives Kᵧₓ=1 at stage four. Each marked history has weight 1/880 under
either preparation. Thus no kernel-as-zero quotient has been silently imposed.

For all four named mark assignments of the accepted i=0 u/v swap, both original
structural weights are 19/1320, individual marked weights 19/5280, and endpoint
counters are (3,1,0,0). The endpoint order and marks agree. Literal L, C, K and
covariance fixtures reproduce the accepted report. The computed difference is
V₊−V₋=(β/2)diag(0,0,−1,1); eᵤ Weyl exponents are −β/2 and −3β/4.
**Full endpoint field-state covariance: FAIL, explicitly demonstrated.** The
fixed cover-link mean separately equals 2 on both histories. It is not a full-law
equality. The corresponding i=1 cases execute with their unchanged structural
weights 14/1320 each and the same field comparisons.

## Actual execution evidence

The author executed the standard-library implementation and tests:

```text
python3 -B -m unittest -v test_model.py
Ran 8 tests in 0.338s
OK
exit status: 0

python3 -B runnable_model.py
exit status: 0
```

All eight test groups passed, with no skipped tests or expected-failure markers.
They check 120 complete marked histories against literal source fixtures and
stagewise invariants; named-swap testing includes eight matched mark/preparation
pairs. An explicit inequality assertion verifies the covariance failure, so test
success does not relabel the failed property as successful or merely unproved.

The initial test and summary executions occurred between 23:08:25 UTC and
23:11:53 UTC on 16 November 2026. These are recorded bounds, not exact
command-start times. The author subsequently ran the complete-history command
`python3 -B runnable_model.py --histories` twice:

| Execution | Start UTC, 16 November 2026 | End UTC | Exit status |
| --- | --- | --- | ---: |
| Complete histories, first run | 23:14:36.551129 | 23:14:36.691410 | 0 |
| Complete histories, repeat | 23:14:36.693088 | 23:14:36.831198 | 0 |

Both outputs were 386189 bytes with SHA-256
`04e00434996019b519109cce19cf7796e354faeb7d09f6fc9b24b04761a5b75b`.
The byte-identical JSON outputs parsed successfully, containing all 120 histories,
normalized masses, 120 commutator/W₂ passes, the explicit covariance FAIL and
swap means 2 with full matrices. No model or test failure occurred in this
baseline. Author-side fixture/code assistance is separate from the distinct
Energy scientific review.

Energy independently ran the eight test groups at 23:18:21.333470–23:18:21.612663
UTC on 16 November 2026: exit 0, no skips or expected-failure markers, with
unittest reporting 0.220 seconds. Summary and repeated full-history commands
ran at 23:19:26.556428–23:19:26.926766 UTC, exited successfully and reproduced
the same full-output bytes and hash. A separate reviewer process parsed the
accepted source tables without importing the model or its fixture module and
checked every serialized history's probabilities, order, marks, counters,
readouts, L/C/K/covariance/ordered-moment matrices and cover mean. This reuses
the accepted proofs and validates this finite integration; it is not a new
foundational proof or empirical test.

## Four achievement distinctions

| Claim | Status and precise scope |
| --- | --- |
| Runs | YES: actual summary command and exact tests exited successfully. |
| Reproduces specified results | YES: both complete registered laws, contrasts, branch restrictions, retained center and named covariance/mean fixtures. Known-answer regression, not new empirical evidence. |
| Derives from DET | NO new ontology derivation: supplied original q, register access, Gaussian representation, β and diagnostics remain premises/choices. Previously accepted scoped mathematical derivations are preserved. |
| Agrees with observations | NOT TESTED: no empirical dataset, fitted constant, calibration or holdout. |

No first-birth ensemble, fifth-birth law, field feedback, probability retuning,
postselection, endpoint repair or physical units were added. Birth schedule is an
implementation order, not a physical global present. No continuum/all-size,
physical clock, action, mass, energy, stress, gravity coupling, balance law,
instrument, ontology proof or native quantum reconstruction is claimed.

## Sources and review status

The [README](README.md#boundaries-and-sources) links the complete accepted
mathematical inputs; [ASSUMPTIONS.json](ASSUMPTIONS.json) records their public
identities and every component's premises, calibration status and known failures.
The unchanged [model](runnable_model.py) and [tests](test_model.py) are included.
**Integrated scientific review: ACCEPT_WITH_SCOPE.** DET Energy Research
independently reviewed the exact author implementation and results; the
coordinator accepted them with no correction. Acceptance covers only the
registered prepare-then-step restriction, tested renamings and complete finite
horizon. It does not qualify arbitrary fabricated State/Field objects, a
general-purpose validation API, other prefixes or larger horizons. The public
Python files preserve the reviewed author bytes exactly.
