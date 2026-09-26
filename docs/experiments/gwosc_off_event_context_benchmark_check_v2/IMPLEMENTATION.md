# RI113 — additive RI100 interface repair, source preparation

26 September 2026 UTC. **Source only; no new qualification or observed execution.**
Root accepted the diagnosis and narrow source design in
`RI113_ROOT_DIAGNOSIS_ADJUDICATION.json`, 1,488 bytes, SHA256
`c155331373baa003cff2ff72af1b7b8d509d7838615db9183960c5125191bc31`.
This source packet does not issue a freeze/admission or authorize execution.

## Confirmed problem and exact repair

The genuine pinned RI100 prior uses schema `ri98-mode-weighted-trace-v1`, phase
`fixed_saved_application` and status `all_declared_checks_passed`. Both published
RI106 observed adapters incorrectly required `all_gates_passed`. Actual admitted
RI110 normal execution failed at primary `TRACE: accepted prior status`, with
no benchmark result. Root's failed-normal review remains authoritative for its
execution/custody; the diagnosis separately checked the complete prior pin and
metadata. No prior scientific result or acceptance threshold failed here.

The new primary introduces `check_ri100_header`; its actual projection keeps the
RI83 schema check and invokes that pure production helper for RI100. The new
validator introduces `verify_ri100_header` and invokes it at the position of its
original combined header predicate. Both helpers require exactly the corrected
schema/phase/status, with intentional mapping/string typing and existing error
categories. They return `None`, do no I/O and give no body/custody authorization.
They use separately located guard logic; neither imports or calls the other.

Only those two helpers and two actual-projection guard hunks change in the
scientific modules. The exact unified diffs are part of the external source
handoff. All remaining bytes, including imports, full input pins, pre-parse hash
admission, actual wrappers, inspector replay, source loading expectations,
projection fields, numerical functions, output schema and gate checks remain
unchanged. No success-status aliases, global replacement, fixture bypass or
numeric-rule change was added. The receiving benchmark still emits
`all_gates_passed` and its twelve gates; the prior RI100 still has eleven checks.

## Inherited arithmetic and fixed scope

The RI104 design remains 32,152 bytes, SHA256
`cd7a585f0002f1aef4d16bb96884c0a745291d41b33e73ff466567cbff5f2478`.
It fixes 4,096 Hz, M=16,384, N=2,769, L=4,096, T=10,961, 131,072 samples per
detector, eight rows and four detector/side scenarios. Left/right use seven/six
previously accessed windows. Exact coordinatewise side means, n-divisor energies,
shared interval coefficients, deterministic width threshold 1/10^12, exact
binary64 interpretation and all existing metadata/flag limits are unchanged.

Primary midpoint/radius denominator-lifted contractions and the independent
validator's signed endpoint contractions remain text-identical outside the two
header-admission sites and newly added helpers. Complete raw extraction, all
26 window records, 208 raw coordinates, 416 short/long intervals, 32 means,
208 centered coordinates and six detached artifacts still require actual full
execution and independent validation. Correcting a header does not establish
runtime fit, width passage, a completed calculation or empirical suitability.

The full numerical structural specification is retained verbatim after the new
addendum in `API.md`. The original implementation note is an immutable inherited
reference, 20,615 bytes, SHA256
`e0fea15552fb7d47f6948614131673c4bf4dc8a6c176d4a009dac687f12da7e5`.
The original published RI106 API/source/qualifier/implementation, RI108 results,
RI110 active freeze and failed attempt are untouched.

## New fixed metadata-only qualification source

`interface_qualify.py` imports only `copy` and `json`. Its future caller supplies
captured primary and validator module objects. It makes exactly 22 target-helper
calls in the fixed primary-then-validator inventory: one correct three-field
header and ten one-defect variants per implementation. It calls neither actual
projection wrapper, no HDF5 inspector or numerical consumer, and opens no file.
It does not alter actual pins or parser/identity functions to fabricate observed
inputs. `API.md` gives every input, intended code and complete returned schema.

Wrong status, unknown status, both inappropriate phases, older predecessor
schema, each missing header field, a boolean status and a null mapping are
explicit refusals. The qualifier checks exact expected exception class/code,
positive None return, complete ordered inventory and unchanged input vectors.
Every check uses a runtime conditional rather than an `assert`. On failure it
raises without manufacturing a successful report; actual failed execution must
be preserved by the future caller. No fixtures were executed in source preparation.

`qualify.py` is a byte-for-byte copy of the historical full fabricated qualifier,
34,582 bytes, SHA256
`b3ba3e9344d36447fbe7c3902fb92eb9c9efd8bdba7303dfe464ba5429a2a460`.
It is available for prospective full qualification if root's applicability review
requires it. It retains 11 positive groups and 74 refusals (39 primary, 35
validator), plus the existing fabricated phase separation. None of its old
results is overwritten or promoted to cover newly authored source bytes.

## Source closure and future caller obligations

`SOURCE_CLOSURE.json` in the external handoff binds all six new packet files,
immutable RI106 originals, the accepted diagnosis/design, original numerical
design and acceptances, RI108 qualification and root RI110 failure review. It
also binds and freshly checks the full 56-pair RI110 inherited source/data closure
as immutable historical context. Every body in that inherited list is hashed
without decoding new scientific content. The captured source list includes
scientific operands in historical roles; it is not a new permission to parse them.

The new direct static imports remain:

- primary: standard-library `fractions,pathlib,hashlib,io,json,math,os,re,stat,struct`;
  lazy `h5py` only inside the separately admitted observed entry point;
- validator: standard-library `fractions,hashlib,io,json,math,os,pathlib,re,stat,struct`;
  lazy `h5py` only inside its observed entry point;
- historical qualifier: standard-library `fractions,pathlib,copy,hashlib,json,math,os,struct`;
- interface qualifier: standard-library `copy,json`.

Captured module objects are arguments; there is no ambient project import.
Observed execution additionally requires the unchanged captured RI37 inspector,
h5py and its complete accepted runtime/dependency closure. Future execution
still requires a complete concrete caller/control/worker, literal command/cwd/
environment, complete runtime inventory and source/input copies. This packet's
complete authored/direct source closure is not an executable runtime freeze.
No interpreter probe, package installation, compiler, import or target execution
was used to prepare or inspect it. Exact source diffs and ordinary metadata
hashing are the only automatic source checks so far; syntax has not been tested
by compilation or import.

RI108's genuine fabricated qualification remains evidence for its original
source bytes and executed path. Text identity of unchanged arithmetic supports
a later narrow applicability argument; it does not itself accept new source or
qualify the new header helpers. Root must commission independent complete source
review, decide qualification applicability and separately admit any tiny/full
qualification. The new helper report must be bound to actual captured source and
runtime by its caller; report labels alone never establish that custody.

For a later observed caller, preserve 180 child seconds, 524,288 KiB sampled
sole-child RSS, 0.025s target poll, 0.1s maximum sample/final gap and 0.05s ps
timeout, including full checks/validation inside the budget. These are inherited
limits, not a claim that the new source meets them. A fresh normally admitted
attempt must complete and be reviewed before any separately admitted optimized
attempt. New output locations, source closure, actual input custody and freeze
must be reviewed; never mutate/reuse RI110's failed attempt or weaken a gate.

## Authorship and remaining review

Original numerical primary/qualifier author: measurement_replay_review. Original
separate endpoint validator author: runtime_recovery_audit. Their later accepted
review/repair history is pinned by RI106/RI108. RI113 source author
`ri113_observed_interface_repair` wrote both small new header helpers, their
separate call-site repairs, interface qualifier and new documentation. The new
helpers use separate implementations and existing error machinery, but common
authorship of this interface layer is disclosed. This author is not its own
independent reviewer; root will commission that review before any execution.

The public 32-second records remain previously accessed development/calibration
data. No unbiased population covariance, chi-square law, physical noise model,
calibration envelope, SNR, coverage, protected held-out validation, native forward
map or geometry/gravity result follows. RET remains paused. Native proof work
continues independently and the wider programme is unfinished.
