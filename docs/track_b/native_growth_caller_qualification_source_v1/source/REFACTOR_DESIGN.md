# Minimal Caller Refactor to Expose Metadata Validation Boundaries

This is a follow-on design requested by the coordinator after the RI132
reachability finding. It is not implemented or authorized for execution here.
RI129 remains immutable. A new caller version would need fresh complete source
review, qualification and root acceptance before any scientific invocation.

## The actual blocker

Several RI129 policies are inline after fixed-path file reads and whole-byte
authentication. The dependency parser accepts only one literal manifest pin;
source-card policy is inside a fixed-file consumer; the 15/4/71 checks follow
genuine completed-mode custody reads; and the eight-object audit checks follow
real binding and producer custody. Changing a synthetic value at the wrong
layer fails an earlier authentication guard. It does not test the deeper policy.

Neither monkeypatching global paths/pins nor replacing authenticated bytes with
fabricated acceptance records is legitimate qualification of this interface.
Direct argument-boundary cases in RI132 therefore leave these deeper guards
explicitly unqualified. Existing no-argument functions cannot acquire argument
coverage merely because an equivalent predicate was written in a test helper.

## Proposed extractions in a new source version

Preserve the native and independent-audit implementations and their distinct
failure codes. Names below are prospective interfaces, not functions added now.

| New pure function boundary | Exact existing policy to move | Production authentication retained outside it |
| --- | --- | --- |
| `validate_dependency_payload(value)` | Complete schema/status/scope, ordered dep roles, canonical paths, full identity shapes, nonsymlink policy and provenance types from `dependency_prepare` | Literal full manifest byte/hash check before JSON parsing; final identity recheck; only validated entries cached |
| `validate_source_decision_payload(decision, expected_identities)` | Exact RI129 source-card keys, source-only status, six identities, false execution and false qualification transfer | Original/copy/runtime/history/dependency checks and raw-byte-authenticated fixed source-card read |
| `validate_source_review_payload(review, expected_identities)` | Independent review schema/status, no blockers, six source identities and false execution | Fixed review path and complete authenticated metadata read; recursive reference closure |
| `validate_current_target_checks(review)` | Exact three integer fields 15/4/71, completed-check flag true and inherited-qualification flag false | Every genuine source/receipt/freeze/outer/prior-custody check remains before the actual root/independent review is consumed |
| `validate_applicability_payload(card, mode, expected_identities, command)` | Exact source-only stage fields, mode, full identity bindings, argv/cwd/environment/limits | Fixed applicability path and authenticated body; command and expected identities constructed from fixed production constants/observations |
| `validate_audit_binding_payload(binding, expected_references)` | Exact no-descriptor binding shape, source-only status, three candidate identities and all three genuine modes | Fixed AUDIT_BINDING path, whole raw identity, positive identities and actual reference observations before caching or argv formation |
| `validate_audit_object_observations(observations, expected_identities)` | Exactly eight ordered fixed paths, positive bounded regular objects, nonsymlink ancestry, unique device/inode pairs and certificate binding | Real fixed-path traversal/open/fstat and full file identities; no synthetic observation accepted in production |

The last function consumes observations, not files or a path-discovery callback.
Qualification can supply deliberately invalid argument observations. Production
must obtain those observations from its unchanged actual filesystem checks.
Such direct observation tests alone still do not qualify actual filesystem races,
physical alias detection, namespace custody or genuine process completion.

## Proof and test obligations for the refactor

The extraction must preserve statement order, exact key/type checks, comparison
semantics and intended first failure code/message. In particular, booleans must
not become integers, observed identity and expected identity must not be swapped,
and the audit's identity failure codes must not silently become native prerequisite
codes through a shared helper. Do not replace canonical typed comparison with
Python's looser equality where the existing route distinguished types.

Production entry must still authenticate the same complete fixed bytes before
calling a pure function. There is no new command-line switch, alternate path,
test-mode global, callback injection, environment exception, permissive parser,
or alternate acceptance route. Source-only cards must not become run permission.
Keep whole historical/reference closure, five scientific inputs, fourteen result
sections, eight protected audit objects, three candidate copies and all limits.

Require an exact before/after source correspondence for every moved block and a
fresh nonauthor review of both the extracted predicate and each production call
site. Direct tests must call the actual newly reviewed function, not a copied
assertion in a test implementation. Test each intended first refusal with all
earlier predicate conditions satisfied in an explicitly fabricated argument,
plus an admissible argument control. Those arguments are never historical or
active acceptance records and are never installed at the production fixed paths.

Retain genuine unchanged-entry negative invocations and externally owned
before/after runtime/custody checks as a separate evidence class. Preserve the
read-only pre-Attempt gate and repeated in-attempt validation. Early refusal
still needs genuine external process and custody evidence; extraction must not
invent an attempt receipt or eliminate final in-attempt failure checks.

## Deliberate limits

This design does not promise complete qualification after seven extractions.
Deep serial receipt, actual filesystem mutation, monitor/time/RSS/signal and
late-output branches still need exact retained-evidence applicability or their
own genuinely reachable controls. The full RI132 52/69 correspondence remains
the coverage ledger; a pure metadata predicate is not whole-entry evidence.

Root may select this narrow source repair after independently adjudicating
RI132. It is not implemented here, not a new scientific question and not
permission to change the actual native sign/H30 target, support, epsilon,
thresholds, q6/q7 laws or resource ceilings.
