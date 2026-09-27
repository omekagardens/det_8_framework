# RI122 runtime metadata interface — source preparation only

Author: `/root/ri117_t1_lemma`. This specifies a static opaque capture, not an
execution, active freeze, admission, measured import path, or OS-image identity.

`RUNTIME_CLOSURE.json` has schema `ri122-captured-application-runtime-v1` and
status `SOURCE_ONLY_CURRENT_RUNTIME_CANDIDATE`. The caller authenticates its
whole fixed byte/hash identity before parsing it. The following six groups are
mandatory: `schema`, `status`, `files`, `directories`, `absences`, `host_platform`.
Coverage/provenance extras are authenticated by that same whole-document pin.

## Files and namespace

`files` is an ordered list. Each entry is
`{role, path, identity, classification, reference_provenance}`. Roles are unique
`runtime_NNNN` names. Literal paths are unique canonical absolute paths; equal
bytes or equal resolved paths do not merge distinct literal paths. `identity`
has exactly `{path, resolved_path, bytes, sha256, symlinks}`. Each symlink has
exactly `{path, target}`, in complete component-traversal order. Opaque hashes
use stable pre/post file metadata and rechecked literal symlink resolution.

`directories` is an ordered list of
`{path, resolved_path, symlinks, entries}`. `entries` is sorted by name, and each
entry has `{name, kind}` for regular files/directories, or
`{name, kind: "symlink", target}` for literal links. Allowed kinds are exactly
`file`, `dir`, `symlink`; unsupported filesystem objects refuse capture.
Names/types/link targets are matched exactly, including all existing `.pyc`
files and directories. `-B` prevents writes, not reads. This detects inserted
import shadows instead of checking only previously existing file hashes.

`absences` is an ordered list of unique canonical absolute paths. Each must
fail `lstat` with `ENOENT`; a dangling symlink is not absence. These include
possible stdlib archives, path override files and virtual-environment markers
in the pinned executable/framework layout. No missing scientific result is
invented or placed in this runtime inventory.

Runtime file identities join the ordinary closed ordered before/after
snapshots. Directory and absence observations are independently attempted,
preserved and compared both before admission and in the finally path, including
failure. A namespace canonical hash/count is evidence about those observations,
not a replacement for preserving which path failed.

## Host-platform shape

`host_platform` has these fields:

- `expected_uname`: exactly `{sysname, release, version, machine}`; no hostname.
  Compare against the corresponding current `os.uname()` fields at preflight
  and postflight. This is static host identity, not interpreter probing.
- `system_version_plist`: `{path, expected_values}` where `expected_values`
  contains exactly `ProductName`, `ProductVersion`, `ProductBuildVersion`.
  The actual plist is also a pinned regular-file entry in `files`; its opaque
  identity is checked before/after. The three values were read as static
  metadata and are not a claim to pin the complete operating system.
- `system_dependencies`: ordered records
  `{install_name, source_images, location_status, shared_cache_status}`.
  `source_images` lists captured Mach-O image paths whose static load commands
  name the system dependency. `location_status` is one of `regular_file`,
  `symlink`, `absent`, `unavailable`; `shared_cache_status` is explicit text.
  An absent on-disk image does not prove cache membership. Cache membership is
  not probed here and remains `not_independently_inspected_trusted_host_premise`.
- `scope_decision`: the five-field opaque identity of the owner's
  `RI122_HOST_PLATFORM_SCOPE_DECISION.json`, also present in `files`.
- `trust_boundary`: explicit description of the trusted Darwin kernel/loader/
  Apple shared-cache premise and the exclusion of all Homebrew dependencies
  from that exception.

The caller must visibly preserve expected/observed host identity before and
after, including missing/unavailable observations. System dependency records
describe the source-time Mach-O dependency analysis; they do not certify every
transitive Apple shared-cache byte. No broad OS/shared-cache capture is allowed.

## Authenticated coverage extras

The capture will explicitly record: actual interpreter literal link chain;
framework and frozen-module binary backing; complete current stdlib regular
files, existing bytecode, extensions and data; exact directory membership;
recursively resolved non-system Mach-O dependencies; static `-I -S -B` search
root justification from installed configuration/manual text; excluded
site-packages with pinned literal link and reason; and unresolved platform or
static-path assumptions. It will not call the environment hermetic, infer
`sys.path` from a live probe, or transfer old runtime qualification to new guards.

Historical evidence remains in a separate reconciliation manifest owned by the
main agent. The runtime schema does not collapse original/copy/historical/
failure paths, replace actual sequential custody, or add scientific authority.
