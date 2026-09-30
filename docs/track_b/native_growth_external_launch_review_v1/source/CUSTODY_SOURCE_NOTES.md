# RI138 external custody mechanisms — author source notes

Status: SOURCE ONLY, UNEXECUTED, FOR INDEPENDENT REVIEW. This author note
does not accept the source, admit a process or claim any current runtime
match. No subject/helper import, compile, AST parse, probe, case run, current
runtime inventory, active card, fixture, scientific decode or Git operation
was performed. The expected administrative manifests were inspected as
metadata and opaque-hashed; that is not an observation of their listed files.

The implementation is `custody.py` in
`/Volumes/AI_DATA/development/det-review-evidence/ri138-native-external-launch-source-92pbd52w`.
It has no CLI, loader, process-launch call, authority writer or runtime
discovery mode. Root's separately reviewed launcher supplies its sink,
deadlines and authenticated supplemental identities. No accepted caller is
imported or patched. The module implements the file and namespace observation
mechanisms themselves; it does not delegate those mechanisms to a later gate.

## Fixed expectations and unchanged premises

Three exact administrative files are hardpinned and authenticated before
JSON decoding. They remain fixed expectations, not current observations:

| Manifest | Bytes | SHA256 |
| --- | ---: | --- |
| RI136 SOURCE_DEPENDENCIES.json | 652822 | da5708eb15abbb4da7a8c17b5a6c737b2fce9e8663c2177e4dbb1b9e2107d42c |
| RI122 RUNTIME_CLOSURE.json | 2862854 | 35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920 |
| RI122 HISTORY_RECONCILIATION.json | 2170307 | b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c |

The first is under
`/Volumes/AI_DATA/development/det-review-evidence/ri136-native-policy-dispatch-source-g_z472z7`;
the other two are under
`/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx`.
Their exact bytes were confirmed by opaque count/hash only during authoring.

The frozen base inventory has 4,374 independently recorded rows:

| Group | Rows | Actual future operation |
| --- | ---: | --- |
| manifests | 3 | Full identity of each fixed manifest. |
| source_dependencies | 373 | Full opaque identity, no protected-body decoding. |
| history | 699 | Full opaque identity, including legitimate empty regular logs. |
| runtime_files | 2988 | Complete bytes, literal/resolved paths and ordered symlink traversal. |
| runtime_directories | 258 | Twice-observed complete sorted names, types and link targets. |
| runtime_absences | 40 | Actual lstat; only ENOENT counts as absence. |
| host | 13 | uname, authenticated system-version plist, eleven visible system locations. |

Shared paths across groups retain their original group rows. Consistent
duplicate paths are permitted; conflicting expectations refuse. The helper
does not replace 373 with a smaller selected-subject subset. Root additionally
passes every identity in the new 396-entry RI138 source closure, the current
packet, current plan and accepted review references as supplemental identities.
The new source closure does not overwrite either old manifest. Within the
supplemental list exact duplicate paths are collapsed, with conflicts refused.

The accepted Darwin kernel, loader and Apple shared-cache trust premise remains
exactly the runtime manifest's text. `runtime_system_location` observes only
whether each specified install-name location is absent, a symlink or a regular
file. `shared_cache_status` is the retained explicit trusted-host premise, not
a measurement of cache contents. Named Homebrew files remain fully observed
runtime entries and gain no platform exemption. No complete OS identity,
hermeticity, continuous filesystem lock or hostile-kernel resistance is claimed.

## API and frozen data flow

`load_expected(supplemental_identities, deadline_ns) -> bytes`

The input is a list or tuple of parent-authenticated ordinary three-field or
full five-field identities. An ordinary identity implies the same resolved
path and an empty symlink list; it does not permit an unobserved alias. Full
identities retain the real accepted link chain. Byte counts are integers, not
booleans, and may be zero for regular logs. The function authenticates only
the three fixed manifest files, parses administrative metadata, checks exact
counts and original runtime/history structure, and constructs the complete
expectation inventory. It never opens their referenced body files at this
stage. A final manifest recheck precedes use of each parsed body.

The return is immutable canonical ASCII JSON bytes without a terminal newline.
Its six exact keys are `schema`, `manifest_identities`, `frozen_counts`,
`expected_interpreter`, `trust_boundary`, `objects`; schema is
`ri138-frozen-custody-spec-v1`. Each ordered object has `id`, `group`, `kind`,
`path`, `expected`, `auxiliary`. The inventory is exposed before observation
so root can identify every missing row after a forced stop. The full expected
interpreter identity is available without a fresh runtime discovery.

`extend_spec(spec_bytes, supplemental_identities) -> bytes`

This is a pure metadata operation. It parses the already frozen bytes, never
rereads a manifest or reobserves a file, preserves every existing object and
appends sorted genuinely new supplemental paths. Existing identical paths
need no extra row; conflicting identities refuse rather than overwrite the
original expectation. New preflight/authorization and closed capture identities
can therefore join postchecks without replacing an expectation after drift.
The caller must retain the old spec; if extension fails it must record that
failure and still attempt the complete old inventory. Neither validator nor
extension authenticates a saved spec's external provenance: root must bind
the exact bytes returned by genuine preparation and retain that identity.

`observe_all(spec_bytes, phase, sink, deadline_ns) -> summary`

Phase is exactly `before` or `after`. The function attempts every frozen row
independently, even after a preceding observation, mismatch or ordinary sink
failure. Each attempt yields a complete object record before advancing. Files
are fully hashed; directories, absences, uname, system plist and visible system
locations use actual filesystem/host operations. No scientific body is parsed.
The system plist is authenticated as complete bytes before plist decoding and
rechecked afterward. Missing and changed objects remain failed observations.

The synchronous `sink(record)` must append and fsync the exact canonical ASCII
record plus one newline, under the parent-owned 64-MiB journal bound. It returns
exactly `{path, offset, bytes, sha256}` for that durable byte range. The helper
checks canonical absolute path, nonnegative integer offset, exact integer
record length and record hash; this is a range reference, not a whole-file
identity. A reference dictionary alone cannot prove actual durability or tool
origin. The launcher implements those operations, and root authenticates them.
If a sink call fails, that error remains separate and later rows still run.

An object record has fourteen exact keys: `schema`, `phase`, `spec_sha256`,
`sequence`, `id`, `group`, `kind`, `path`, `expected`, `observed`, `matched`,
`observation_attempted`, `started_ns`, `finished_ns`. Successful observations
carry `observed={ok:true,identity:...}`; failures carry `ok:false`, exception
type, code and bounded message. A mismatch is not falsely relabeled as an
exception. Deadline-refused rows do not claim a completed file observation.

The nineteen summary keys are `schema`, `phase`, `spec_sha256`,
`expected_objects`, `attempted_objects`, `matched_objects`,
`observation_errors`, `mismatches`, `sink_errors`, `deadline_exhausted`,
`complete`, `groups`, `records`, `first_error`, `started_ns`, `finished_ns`,
`elapsed_ns`, `trust_boundary`, `bootstrap_provenance_established`.
Every group reports expected/attempted/matched/error/mismatch/sink counts and
its local completeness. Every returned record entry contains its id, durable
range reference and independent sink error. Global `complete` requires every
row to match, every sink call to succeed, and no elapsed deadline. A group can
be locally complete while the overall deadline invalidates the phase; only
the overall verdict plus genuine external custody can support a preflight.
`bootstrap_provenance_established` is always false.

## Bounds and hard-abort behavior

Metadata preparation is bounded by a separate 60-second deadline. Each complete
before/after observation has a separate 300-second deadline. These are not
extensions of the unchanged 120-second dispatcher process limit, 512-MiB
sampled process-group RSS, 50-ms polling or 250-ms census timeout. The parent's
reviewed total envelope is 840 seconds, including preparation, both observation
phases, active process and finalization. Performance has not been measured.

The helper reads at most 64 MiB per complete file, in at most 1-MiB chunks;
it rejects initial oversize and growth beyond the bound. This is compatible
with the fixed manifest metadata: maximum expected source file 31,528,781
bytes, runtime file 5,519,552 bytes, history file 2,634,698 bytes. These maxima
describe saved expectations only. Empty regular files remain hashable. New
directory observations are bounded by 16,384 entries and 64 MiB of encoded
entry metadata, above the saved maximum of 513 members. Frozen specifications
are at most 64 MiB and 10,000 rows. These are refusal bounds, not permission
to silently omit excess members.

Cooperative checks run between path components, chunks, entries and objects.
After ordinary deadline exhaustion, later objects receive explicit unobserved
deadline errors and the sink is still attempted for each; no successful
custody can result. Ordinary observation and sink exceptions are caught with
`Exception`. The launcher's dedicated `HardDeadline(BaseException)` therefore
propagates through the helper, as do KeyboardInterrupt/SystemExit, rather than
being swallowed as thousands of new ordinary errors. Already durable rows and
the frozen full inventory remain evidence; the unobserved remainder is
incomplete, not presumed unchanged. A forced abort need not yield a summary.

Regular-file prechecks and O_NONBLOCK reduce special-file open hazards; they
do not make arbitrary kernel filesystem stalls preemptible. The root/tool
hard deadline is a necessary external boundary, including sink fsync and
remaining failure-tail writing. This helper cannot certify or implement its
own execution provenance after it has already started.

## Source correspondence and explicit adaptations

The selected source ancestor is
`/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde/supervise.py`,
89,283 bytes, SHA256
`e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d`.
The selected complete support definitions and their callers were read as text.
No source execution or qualification transfer follows from this reuse.

| RI134 source span | New mechanism | Correspondence / explicit change |
| --- | --- | --- |
| 134–163 | Stop, need, canonical, exact_keys, hexhash | The selected definitions are unchanged; unrelated digest/timestamp helpers are not copied. |
| 165–179 | strict_json | Duplicate-key and forbidden decimal/nonfinite handling retained; the unused allow_floats/finite-float branch is removed because only administrative expectations are decoded. |
| 257–280 | resolve_links | Full component traversal, ordered links, cycle and 64-step guards retained; deadline argument and per-loop checks added. |
| 283–306 | read_file, file_identity | Same whole-byte hashing and before/after descriptor/link checks, split to optionally retain administrative bytes; adds fixed read cap, cooperative deadlines, regular-file precheck, O_NONBLOCK and final resolved-path signature comparison. |
| 309–319, 353–356 | validate_identity, canonical_path, full_identity | Same five-field and link meaning; stronger canonical/NUL, zero-or-positive integer bounded bytes, nonplaceholder digest and finite link-count checks; explicit ordinary-identity expansion added. |
| 359–408, 658–692 | validate_entries, read_expected_manifest | Same authenticated dependency/history payload roles/order/provenance and link rules; exact 373/699 counts, no global caches, hardpinned metadata and bounded complete raw reads. |
| 412–517 | validate_runtime, read_expected_manifest | Same runtime file/directory/absence/host meaning and trusted-platform boundary; exact 2988/258/40/11 counts and size/count bounds; returns local metadata rather than mutating accepted globals. |
| 553–579 | runtime_directory_identity | Same two complete sorted member observations and directory/link stability; adds deadlines and explicit finite membership/encoded-size bounds. |
| 582–591 | runtime_system_location | Exact unchanged function body. |
| 594–608 | runtime_system_version | Same authenticated plist meaning and postcheck; explicit expected file/path/deadline arguments replace global runtime lookups; bounded raw read authenticates the parsed bytes directly. |
| 322–329, 534–550, 611–655 | observe_object, observe_all, frozen object inventory | Adapts independent per-file/namespace/host attempts into durable per-object records, preserving all expected categories and adding separate mismatch/sink/deadline accounting. This is not the old snapshot function unchanged. |
| 695–696 | same | Canonical equality retained; exception code is custody instead of production prerequisite. |

New glue consists of bounded deadline checking, fixed manifest pins, immutable
spec construction/validation/extension, per-record reference validation and
summary bookkeeping. No applicability, binding, scientific object, payload
policy, metric, mass/gravity, sampling, target threshold or mathematical
calculation is added or changed.

## Integration and stopping boundary

The launcher must bind all 396 current dependency identities and current/root
source references, freeze the exact spec before observations, preserve each
journal durably, keep the old spec when extension fails, and postcheck the
complete frozen set after an early failure. Newly created closed files may be
appended through pure extension. An actively appending journal cannot honestly
pin its own final hash; root separately closes/authenticates the complete
capture and genuine completion. No self-reference cycle is introduced.

The external launcher, root preflight and real tools must authenticate this
observer's interpreter and source suppliers before its first import, retain
actual command/tool provenance, enforce hard deadlines and reconcile outputs.
Successful future file observations would establish finite before/after
matching under the accepted trust boundary only. Source preparation supplies
none of that operational evidence and issues no preflight or acceptance.

Stop after source review/handoff. No scientific execution, old-control credit,
whole-caller qualification, C2/C3 result, H30 feasibility finding, clock/RET or
measurement-lane work is claimed or authorized.
