# RI176 schema correspondence

The seven source-role names, seven-field request, 22-field complete collection, 15-field case report, original 17-field subject receipt, saved-checker output fields, bounds and exclusive namespaces are retained from the exact pinned RI171 SCHEMAS.md. RI171 schema strings and request/operation/reviewer prefixes remain literal for compatibility; protocol.py fixes this successor source directory. Historical cards cannot substitute its exact role pins. This is a new source interface despite unchanged outer version strings; source identity is mandatory.

The active checker closes every trace event in its literal `shapes` table. Added/changed event payloads, besides common event and actual monotonic_ns:

- fsync_complete, close_complete: exactly `{tag}`; emitted only after the real operation returns. close_complete may precede the named late_close injected exception, which still makes that subject capture non-durable.
- sync_base_complete: exactly `{ordinal}`; emitted after the original base sync and explicit fixture-directory sync. A later receipt_post_receipt exception remains a required failure.
- popen_acquired: exactly `{handle_id, kind, pid}`. handle_id is the consecutive positive integer assigned to the actual acquired handle before any ownership fault.
- observer_entry: exactly `{deadline_monotonic_ns}`, the actual argument passed to the original function. Its source expression remains current monotonic time + 400,000,000 ns.
- file_mutation: exactly `{tag, fault, before, after, before_first_byte}`. before/after are full FilePins `{path,bytes,sha256}` of the actual fixture pathname. before_first_byte is the first octet or null for an empty file. Drift and size predicates require a nonempty input and validate their respective exact transformations.
- leaf_recovery_signal: exactly `{identity, signal}`, emitted after real killpg returns; identity is the complete newly observed `{pid,ppid,pgid,birth}`. It is never absence proof.

Owned recovery rows are now exactly `{handle_id,kind,pid,returncode,reaped}` or `{handle_id,kind,pid,error}`. The complete list must match actual acquisitions in order, including the typed ordinal/identity. The independent leaf row retains the original closed forms: unavailable `{kind,identity_unavailable,requires_external_recovery_review}`; failure `{kind,identity,error,requires_external_recovery_review}`; signalled `{kind,identity,kill_sent,absence_proven,requires_external_recovery_review}`. There is no arbitrary additional-row fallback. Leaf membership is required for the two descendant cases and prohibited otherwise.

CASE_OBLIGATIONS.json contains schema, status, not_operational_input and rows. Each of its 92 literal rows has id, kind, fault, terminal, input_tag, healthy, subject_reap. The corresponding pinned checker map uses id as key and the remaining six fields as value. The JSON rendering is authoring/inspection metadata only: it is not read at operation time and cannot alter policy independently of the checker hash. `healthy` maps a required stream to its complete literal R-byte length. Incomplete cases use separately enumerated consumed-prefix, actual EOF and explicit unverified-reap predicates; an empty healthy map is not blanket acceptance.

No current runtime, actual object or numerical input is encoded in these prospective schema descriptions. Administrative source text edits and opaque metadata comparisons are not fixture execution.
