# RI-84 — source-only first-departure verifier

25 September 2026 UTC. **Checker implementation independently source-reviewed;
no coefficient execution authorized or performed. Actual feasibility remains
unknown.**
The coordinator accepted the [RI-82 design](../native_growth_first_departure_v1/DESIGN.md)
and authorized only `check.py` and this implementation note. A new
`CERTIFICATE.json` must remain absent until separately authorized execution.

## 1. What this implementation decides

This is the exact bounded realization of one already frozen question,
not another support search or a new mathematical law. Relative to the
actual accepted marked prefix, does the following three-class first
departure admit a nonzero record-blind perturbation with positive h and
a strictly positive complete-row expected-width gain?

| Ordered variable | Seven-event class | Natural canonical representative | Width |
|---|---|---|---:|
| T1 | C4 ordinal-sum A3 | (0,1,3,7,15,15,15) | 3 |
| T2 | C5 ordinal-sum A2 | (0,1,3,7,15,31,31) | 2 |
| T3 | C4 ordinal-sum (C2 disjoint A1) | (0,1,3,7,15,15,31) | 2 |

Here h=1 through size six and off these three seven-event classes.
Values at size eight and above are **unspecified**. The checker does not
complete an all-size record-blind harmonic transform.

Both mathematical dispositions are legitimate verifier outcomes:

- Every exact balance vanishes: the prescribed nonzero direction, positive
  interior amplitude and positive one-step width gain are certified.
- Some balance does not vanish: an exact nonzero reference minor rejects
  **every nonzero perturbation on this support**, with h=1 elsewhere at
  size seven. It does not exclude other supports or later departures.

Neither a resource failure nor an implementation/refusal-test failure is
a mathematical rejection. The checker must not require the first disposition
to succeed as a verifier. No actual disposition is claimed in this note.

## 2. Complete finite domain and lower-row access

All seven maximal-deletion roles of T1/T2/T3 give exactly two affected
six-parent classes:

- P_A=(0,1,3,7,15,15), ideals 0,1,3,7,15,31,47,63;
- P_B=(0,1,3,7,15,31), ideals 0,1,3,7,15,31,63.

The supported forward slots are P_A:15→T1, P_A:31→T3,
P_A:47→T3, P_B:31→T2 and P_B:15→T3. The two P_A→T3
ideals remain separate occurrences. Three backward deletions of T1 do
not create three forward P_A→T1 transitions.

Canonicalization means the least predecessor tuple over natural labelings.
It recognizes a whole unmarked class, including the other natural T3
presentations, not just the displayed literal tuple. New combinatorial
work is restricted to these three children, their seven deletions, two
parents and 15 labeled forward extensions, plus the held chains C4/C5.
No new global six- or seven-order inventory is authorized.

| Coverage | Required count |
|---|---:|
| Complete affected marked parent rows | 128 |
| Labeled row/ideal occurrences | 960 |
| Supported coefficient occurrences | 320 |
| Zero-correction occurrences | 640 |
| Full births, all with zero correction | 128 |
| Held actual C4/C5 marked rows | 32 |
| Held labeled probability slots | 176 |
| Base markings | 16 |
| Compact balance equations | 32 |

A zero correction is not a zero probability. The 960 entries are not a
new q6 table. No numerical M6 or a6 is needed: every supported birth is
proper, so the common positive scale cancels from the normalization
equations. Neither q6 nor q7 may be queried.

The only new held-row queries are C4=(0,1,3,7) and
C5=(0,1,3,7,15), at xi=0,…,15, with the C5 top bit zero.
Every slot of each held row is retained, including the full complement.
The distinct full masks are 15 for C4 and 31 for C5.

The inherited actual-prefix replay is a named exception to the ban on
new global inventories: RI-74 replays its unchanged accepted RI-63 proof
and existing terminal-six catalogue. That replay verifies the held prefix;
it does not construct a six-parent growth law or normalization maximum.
The 69 canonical stages and 15 inherited intended-reason controls remain
separate from RI-84's new controls.

## 3. Mathematical identities the certificate must preserve

Write q_xi=actual q4(C4,xi,15), p_xi=actual q5(C5,xi,15),
v_xi=actual q5(C5,xi,31), and alpha_xi=p_xi²/q_xi. All are
positive. The two six-parent coefficients are

```text
A_xi = (alpha_xi, 0, 2*v_xi)
B_xi = (0, v_xi, p_xi)
```

Every r=0,…,63 projects to xi=r&15 by the RI-82 invariance proof.
Records and ideals must first be transported together through each
maximal deletion. A retained C5 top mark is then removed using the proved
top-bit irrelevance, not by making an unauthorized top-bit-one query.
Both raw transport and the reduced held-row query belong in the audit.

With k=alpha_0/(2*v_0) and ell=p_0/v_0, the reference rows are
independent and force z=(1,k*ell,-k) up to nonzero scale. The complete
system passes exactly when all xi satisfy

```text
alpha_xi - 2*v_xi*k = 0
p_xi - v_xi*ell = 0
```

The fixed first failure order is xi=0,…,15, A before B. A failing row
is paired with A_0,B_0, using

```text
det(A_0,B_0,A_xi) = 2*v_0*(alpha_0*v_xi-v_0*alpha_xi)
det(A_0,B_0,B_xi) = alpha_0*(v_0*p_xi-p_0*v_xi)
```

No all-minors sweep or optimizer is needed. A direct three-by-three
determinant can independently check the specified formula.

If and only if the balances pass, choose epsilon=1/(2*k). It lies in
the strict interval 0<epsilon<1/k and yields h(T1)=1+1/(2*k),
h(T2)=1+ell/2, h(T3)=1/2. At P_A with all six record bits zero,
the scaled complete-row width functional is
3*alpha_0*z1+4*v_0*z3=alpha_0; the exact gain is
epsilon*a6*alpha_0=a6*v_0>0. This sums every ideal and both fair
newborn bits; no proper-birth or support conditioning is substituted.

RI-82 proves that a passing witness defines a complete positive prefix
through seven births and satisfies the hypotheses of RI-38's distinct
continuation theorem. RI-84 does not enumerate all new diamonds or
re-prove that theorem computationally. It verifies the finite coefficients
and structural premise needed to apply the reviewed symbolic proof.

## 4. Source closure and accepted-prefix interface

The future runtime closure consists only of the new `check.py` plus:

| Accepted relative path under track_b | SHA256 |
|---|---|
| native_growth_plancherel_graft_v1/check.py | edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c |
| native_growth_expected_defect_completion_v1/check.py | 39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b |
| native_growth_expected_defect_completion_v1/CERTIFICATE.json | f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b |
| native_growth_height_normalization_v1/CERTIFICATE.json | 3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969 |

The input bytes must be pinned before a helper is loaded and checked
again before successful completion. RI-74 is loaded without running its
main, pure-Ferrers checks or graft checks. Only its `rebuild_prefix()` and
`prefix_row()` interface is used. The cached row wrapper must be unwrapped
to inspect the actual initialized function namespace: it must agree with
`rebuild_prefix()`'s globals, contain a live HELPER and 2961 Q5 entries.
The returned report must retain the actual q5 manifest
`7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378`
and problem identity
`dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c`.

RI-63's ordinary `row()` stops at four and is not a substitute for the
actual q5. RI-77, RI-79 and their certificates are mathematical context,
not additional runtime dependencies. No foreign growth law, supplied
metric, amplitudes, Hilbert-space reconstruction or physical model is
inserted by this checker.

## 5. Execution boundary

This source phase runs no helper, canonicalization, coefficient calculation,
solver, witness generation, refusal control or saved-certificate replay.
Source reading, file hashes and source hygiene are not mathematical test
results. The source must receive complete independent review and coordinator
adjudication before a fresh execution freeze can authorize even one attempt.

The future per-attempt envelope is 120 seconds and 512 MiB sampled RSS.
Internal elapsed/peak checks and a wall alarm complement an external
owned-process watchdog. The inherited helper's looser checks do not replace
this stricter outer envelope. This is not an allocator-hard-cap claim.

No failure may trigger a quiet retry, source patch followed by an unapproved
rerun, dropped row, expanded support, approximate fraction or increased
resource cap. Preserve the failure and stop for coordinator review.

### Prospective command and custody plan

The durable source-only handoff directory is
`/Volumes/AI_DATA/development/det-review-evidence/ri84-qr-source-nXfTxS/`.
For an eventual approved attempt, its `closure/` subdirectory is the
copied track_b root. Source-only preparation copies the checker and four
accepted runtime inputs there; it does not authorize execution. The final
handoff pins every original/copy pair. No new certificate is included.

The exact prospective child command arrays are:

```json
["/opt/homebrew/bin/python3", "-I", "-S", "-B", "/Volumes/AI_DATA/development/det-review-evidence/ri84-qr-source-nXfTxS/closure/native_growth_first_departure_check_v1/check.py", "--witness"]
["/opt/homebrew/bin/python3", "-I", "-S", "-B", "/Volumes/AI_DATA/development/det-review-evidence/ri84-qr-source-nXfTxS/closure/native_growth_first_departure_check_v1/check.py"]
["/opt/homebrew/bin/python3", "-I", "-S", "-B", "-O", "/Volumes/AI_DATA/development/det-review-evidence/ri84-qr-source-nXfTxS/closure/native_growth_first_departure_check_v1/check.py"]
```

The working directory for each is the absolute copied `closure/` above.
These arrays are prospective only. If the coordinator chooses another
destination or interpreter, a replacement freeze must name its exact
arrays and input identities before execution; paths may not be silently
substituted in a receipt.

Before the first run, coordinator approval must cover:

1. The final source and complete source-review disposition, immutable
   source snapshot and copied bytes of all four accepted dependencies.
2. Exact original/copy byte lengths and SHA256 identities, interpreter
   identity, command array, working directory, mode and schema.
3. A reviewed, byte-pinned external supervisor that owns only this child,
   samples its RSS frequently, measures monotonic elapsed time and kills
   its owned process group on the first resource breach. It must preserve
   a non-success receipt for timeout, memory breach or abnormal exit.
4. Fresh exclusive stdout, stderr, prepared-input and completion-receipt
   paths. Prospective labels are `witness-01`, `normal-01` and
   `optimized-01`; no file is opened for overwrite. Witness and saved
   replays receive their own independent 120-second/512-MiB envelopes.

Use standard-library CPython 3.14 with exact `Fraction` and integer
arithmetic. The checker itself performs no downloads, subprocesses or
file writes. A separately approved supervisor may create the frozen
evidence logs. Its pre-run receipt must be durable before launching the
child; its post-run receipt records exit/stop reason, elapsed time, sampled
peak RSS, stdout/stderr pins and every source/input post-pin. A missing or
changed input, unavailable required RSS sampling, incomplete receipt or
failed source pin is not a successful attempt.

A successful witness run is still not saved-certificate validation. The
coordinator must separately preserve and freeze the generated JSON bytes
as `CERTIFICATE.json`, record its hash, then authorize normal and optimized
saved-certificate replay through an addendum naming the newly complete
input closure and exact log paths. A certificate-only independent arithmetic
audit must check all held-row normalizations, transported-factor products,
32 residuals, rank/disposition and the positive target if applicable. It
must not merely accept the producer's verdict or a stored digest.

Normal and optimized modes must rebuild the same full expected witness and
compare every saved field exactly. New intended-reason controls are
reported separately from the 15 inherited controls. Source review is not
evidence that those controls have already run or that the program meets
its prospective time/memory envelope.

Stop after the approved finite result and independent review. A rank-three
result does not authorize a different support; a positive result does not
authorize continuation implementation, an all-size harmonic solver,
geometry inference or an adopted DET law. All git, coordinator records,
ledger/navigation updates and publication remain with the coordinator.

## 6. Certificate schema and exact replay contract

The schema identifier is `ri84-first-departure-v1`. The certificate is a
single JSON object with exactly these top-level fields:

| Fields | Meaning |
|---|---|
| `schema`, `checker_sha256` | Format identity and the exact producing checker bytes |
| `design_reference` | Original reviewed and accepted RI-82 note identities; not a runtime dependency |
| `dependencies`, `accepted_prefix` | Four runtime byte pins and the actual inherited prefix report |
| `scope` | Explicit frozen-domain and non-computation declarations |
| `structure` | Ordered support, natural isomorphism witnesses, seven deletions and all 15 forward slots |
| `held_rows`, `parameters` | All 32 complete held rows /176 probabilities and all 16 q,p,v,alpha records |
| `compact_rows`, `expanded_rows` | All 32 balances and all 128 complete rows /960 labeled perturbation entries |
| `equivariance`, `coverage` | Transported marked-ideal comparison manifest and exact domain counts |
| `decision` | Reference rows, candidate direction, every-outcome rank disposition and the applicable witness |

Rationals are canonical reduced `Fraction` strings, never JSON decimal
approximations. Other numeric indices/counts are exact integers, not
booleans. Object keys are unique. Whole-certificate validation enforces
the recursively exact object/list/type shape and canonical JSON equality
with a rebuilt expected witness; it does not rely on Python's equality
between `False` and zero or between tuples and decoded lists. Unknown
fields, missing fields or entries, duplicate keys and nonfinite/decimal
JSON values are refused. Every retained field is compared, not merely a
manifest or a success flag.

The ordered support has zero-based indices 0,1,2 corresponding to T1,T2,T3.
Canonical tuple sorting must not reorder the variables. Parent indices
0,1 are P_A,P_B. Held rows are ordered xi=0,…,15, C4 before C5;
compact rows are xi=0,…,15, A before B. Expanded rows are parent index
then record 0,…,63, preserving the ascending individual ideal list.

Each supported occurrence retains every nonempty omitted-maximum deletion
subset, surviving vertices, induced order/precursor, raw transported record,
local-read record, top-zero held query, exponent and exact factor value.
There are 448 such factor occurrences: five per marked P_A row and two
per marked P_B row. The values multiply/divide with their inclusion-exclusion
exponents and must agree with the compact coefficients. Unsupported
occurrences retain a zero correction and no factors, not an invented q6.

The compact certificate distinguishes the equation-(11) residual from
the candidate's row dot product: for A they agree, whereas for B the dot
product is minus k times the residual. The first failed residual therefore
selects the same failing row, with the correct determinant sign and scale.
Every expanded row also carries its complete direction residual.

A rank-two decision carries the strict interior epsilon, all positive h
values, the upper endpoint, complete-row width functional, gain divided
by a6 and all 128 normalization corrections. Its minor is null. A rank-three
decision instead carries the first failed compact index, all entries of
the reference three-by-three matrix, its direct determinant and the frozen
formula value. Its admission is null: no feasible amplitude is fabricated.
Both dispositions retain the reference-normalized candidate, but only
rank two calls it feasible.

Natural relabeling comparisons on the two fixed parent representatives
also transport every record and ideal together. They corroborate the finite
coefficient equivariance; arbitrary-label and complete full-D diamond
coverage continue to rest on RI-82's symbolic proof, not on a claim that
this checker enumerates all possible labels or quantum payloads.

## 7. Refusal controls and the limits of each validator

The final source specifies **71** new intended-reason refusals, separate
from the 15 inherited controls. This is a static inventory, not a claim
that those refusals have run:

- 27 exact domain/type/cache guards, including warm boolean aliases,
  unhashable arguments, forbidden top-one held queries, q6/q7 and global
  scale requests, and bounded transport dimensions;
- 16 support/closure/coverage/multiplicity/transport checks, including
  literal-T3 misclassification, merged ideals, incomplete marked rows,
  erased raw records and an unreduced retained top mark;
- 5 held-prefix/full-slot/pin checks, including a full complement wrongly
  replaced by one minus only p, row normalization and non-actual q5;
- 11 explicitly synthetic amplitude/width/rank-witness checks, covering
  both amplitude endpoints, nonpositive h, the width sign/conditioning,
  both A/B failure minors, first-failure selection and fabricated admission;
- 1 forged actual-disposition check and 11 JSON/rational/saved-certificate
  checks, including explicit residual, factor probability and exponent
  corruptions.

The three synthetic algebra fixtures are not additional inherited rows,
not a proposed growth law and not evidence for the actual result. They
reuse the fixed slot labels to exercise rank two, first failure in A and
first failure in B regardless of the actual held prefix's disposition.
They make no helper query and are not substituted into the actual witness.
They, too, have not run during this source phase.

The transport-only validator checks coordinates, reductions and exact
types. It does **not** independently authenticate a saved factor's value
or exponent. During construction, the deletion-product builder obtains
each factor from the retained held rows, applies its inclusion-exclusion
exponent and reconciles its product with the compact coefficients. During
saved replay, full witness reconstruction plus exact canonical comparison
protects every saved factor field; the new probability/exponent mutations
specifically exercise that layer. The later independent certificate-only
audit must separately check these arithmetic products. These are distinct
verification responsibilities, not interchangeable claims.

## 8. Source-phase status and remaining admission

The final checker is 933 lines /50,869 bytes, SHA256
`1574221fc0c91a6268aa6d59f13586930715207cc1196ba9b2c7542d4193c639`.
The author, this worker and two complete independent source reviewers
concur on its mathematics, source/API behavior, guards, schema and outcome
boundaries. An explicit residual-mutation gap found in source review was
closed before this final identity; saved-factor mutations were added at
the same time. No scientific attempt was made on an earlier source.

Static AST parsing and compilation with optimization levels 0 and 1 pass;
the compiled objects were **not executed**. There are no `assert`-dependent
gates. Those checks establish syntax only, not refusal-control behavior,
resource compliance or mathematical feasibility. No checker/helper import,
probability/coefficient evaluation, enumeration or solver run occurred.

An authoring usage-limit interruption was preserved in the external
`AUTHOR_INTERRUPTION.json`; the same author resumed the existing files.
The preliminary snapshot records a later in-progress boundary explicitly,
not an executed attempt or an exact snapshot of the interruption itself.

The coordinator additionally requested source-only preparation of an
external native supervisor and prospective freeze. That preparation is
separate from the repository checker and must receive its own complete
review and qualification before a scientific launch. The three child
commands and 120-second/512-MiB limits above remain unchanged. Root approval
and a durable prelaunch authorization are still required, and saved replay
requires a separate certificate/addendum freeze.

No new `CERTIFICATE.json` exists, no actual rank has been determined, and
no law has been adopted. The worker does not edit accepted sources, RET,
measurement, coordinator records or git/index. Final acceptance, publication
and authorization of the next concrete phase remain with the coordinator.
