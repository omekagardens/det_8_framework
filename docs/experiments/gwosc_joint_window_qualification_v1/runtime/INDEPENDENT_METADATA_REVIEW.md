# Independent RI121 runtime candidate metadata review

Verdict: **the reviewed candidate matches the accepted v2 source domain and the
independently re-read current filesystem metadata/bytes**. No metadata mismatch
was found. This is a candidate review only: it does not establish an actual
Python profile, bytecode equivalence, import/load trace, runtime admission,
resource fit, qualification or scientific result.

Reviewer: `/root/ri116_saved_arithmetic_review/ri121_applicability_review`.
The reviewer did not write or execute the collector. I read its full source and
independently used `/usr/bin/python3 -I -B` for opaque filesystem/JSON checks.
No candidate interpreter, accepted helper or target was imported, compiled,
AST-processed, probed or executed. No bytecode payload was interpreted. This
review is the only file written by the reviewer in this candidate reservation.
Existing RI119/RI121 source packets and repository/git state were untouched.

## Source requirements checked

The complete accepted repaired runtime_support.py was read and hashed:
8184 bytes, SHA256
`525314ee292722c50ab0bdf635123d3c36acbb96a76d60368c9677872fc2c40f`.
Its exact inventory requirements are:

- schema `ri121-complete-stdlib-runtime-inventory-v2`, with exactly the eight
  keys schema, roots, extra_files, files, symlinks, absent_paths, loader_bindings,
  and scope;
- three ordered root paths, three exact allowed tree links and eight ordered
  absent paths;
- six mandatory extra files, within sorted unique extras;
- one mandatory literal libcrypto loader binding, including its exact alias,
  target path, symlink chain,4874704-byte target and SHA256;
- any additional bindings must have the exact four-field shape, sorted unique
  named paths, matching live resolution and resolved targets in extra_files;
- complete regular-file membership and pins must match the declared roots plus
  extras, including targets of the two allowed framework aliases.

The source does not require eight loader bindings. This candidate intentionally
adds seven to its one required binding. All eight are individually checked below.

## Independent complete verification

Tool8f1641 independently parsed canonical candidate JSON with duplicate-key and
nonfinite rejection, walked the three trees with a separate os.walk route and
raising error handler, and reconstructed the complete file/link membership.
It hashed every one of the9923 listed regular files,258862951 bytes in total.
Each descriptor/name state and before/after metadata was checked. Every size
and SHA256 matched the candidate. This was not a sample or reliance on the
collector's success label.

The regular root counts were2878 for the installed stdlib,5313 for the recovery
venv site-packages, and1719 for system site-packages. The thirteen extras contain
the six mandatory files and seven conservative optional files. The resulting
unique total is9923, with no missing/extra inventory member and no unexpected
tree link. All file rows have the declared closed shape and plain integer sizes.

All9923 selection-metadata rows matched the same current files: device, inode,
mode, size, mtime_ns and ctime_ns. All3394 `.pyc` records also matched their exact
first16 opaque bytes and explicit unparsed-payload flag. The inventory contains
4721 `.py` files. Whole tree membership/link/count enumeration and every saved
selection-metadata state were checked again after hashing.

The eight absences were independently confirmed as both nonexistent and not
symlinks: python311.zip; the higher-priority env/bin/pyvenv.cfg; the two Homebrew
tk/gdbm opt roots; and the four declared libmpdec.3 paths. Values and order match
the helper, not a relaxed substitute list. These are current observations;
the accepted helper's future guard still has to run under actual admission.

All eight loader-name resolutions were reconstructed component by component
without calling the accepted binding helper. Literal link chains, resolved
paths and full target bytes match, and every target is an inventoried extra.
The required libcrypto binding matches the source exactly. The additional
libssl, liblzma, libsqlite and four provider/engine bindings are permitted
conservative additions, not claims of actual loading.

The named recovery interpreter independently resolves through the recorded four
links to the same52640-byte candidate binary, SHA256
`033d83a12ab74b7bcade8248b1bca644f275d3965350b61fe485c2645e1f68e8`.
No invocation or inferred sys.version/sys.path result accompanies that check.

The optional native namespace records were separately reconstructed, including
recursive names, member types and literal link text without symlink traversal.
They match the saved OpenSSL/xz/sqlite records. These observations are descriptive:
the accepted v2 helper does not enforce those optional directory inventories.
The parent's CANDIDATE_REVIEW.md correctly states this limitation. Root must
adjudicate their intended future custody rather than call them existing guards.

The actual saved pins of the four outputs named by CAPTURE_OBSERVATIONS match
the observation record. Its totals, root counts, selection counts, absence
records, thirteen extras and eight bindings agree with the independent check.
No production RUNTIME_INVENTORY.json, EXPECTED_RUNTIME.json, AUTHORIZED_FREEZE.json
or either mode admission exists in this reservation at the check.

## Source/cache table and its limits

Tool25ee98 independently reconstructed all53 selected source/cache route rows
from the saved complete inventory and selection metadata. Each source pin and
metadata record matches its underlying full-capture row. Each row has the
expected normal, opt-1 and standalone candidate filename. All present/absent
flags match the complete namespace, and all85 present cache pins/metadata/header
fields agree. Their flags are0 and timestamp/size fields match the corresponding
captured source selection metadata.

This establishes the correctness of a descriptive table, not bytecode/source
equivalence or a record of which route executed. No marshal payload, code object
or import finder was evaluated. The full inventory preserves all remaining
source/cache files, not only these53 selected routes. Current file metadata is
adequate to describe these candidate selection alternatives; the accepted v2
helper's file pins alone do not enforce this separate mtime/ctime/inode record.
The actual runtime decision must explicitly state its installed-supplier/cache
premises and any intended future selection-metadata checks.

Startup hooks (_distutils_hack and Homebrew sitecustomize), both decimal routes
and their relevant cache alternatives are retained. Actual frozen/builtin
selection, Python profile, decimal fallback, successful dylib loading and the
OpenSSL configuration/provider interpretation remain separate evidence. This
review deliberately does not duplicate the assigned QR3.14 OpenSSL review.
The root's Apple kernel/loader/shared-cache trusted-platform premise is retained;
it supplies no exemption for third-party dependencies.

## Reviewed artifacts

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| RUNTIME_INVENTORY.candidate.json | 2806092 | b6f0fd3244cef06c16da19922db212695387926e2f94012d1857c7c8793f7edc |
| INTERPRETER_BINDING.candidate.json | 1057 | 622bc49403bfda7ce3cb090af44a9a698d8927dea73d733b9191f04869c6c158 |
| FILE_SELECTION_METADATA.candidate.json | 3820963 | 23211b59946b46e5c6f051b04d67bf5f8ed178ec9f27a30371887077ae86ea74 |
| OPTIONAL_NATIVE_NAMESPACES.candidate.json | 4056 | 8d49533bb80070e02defe236348a5528bcac4f4ce23ca214f781dd612475ac1d |
| SOURCE_CACHE_ROUTES.candidate.json | 170354 | be2f886575e752271ccc5a736be838bbaaf8a56c65486bd11263b3da5686de8a |
| CAPTURE_OBSERVATIONS.json | 2926 | 3738cb6877511b22264669794734bc1988c1889aa9a6cd26e77352147e353e29 |
| collect_metadata_candidate.py | 13938 | 78f11d59e909981433c879d363be9a7761d8e8391293712cb4f1d0a219090bd6 |

No blocking discrepancy was found in this metadata candidate. Root may use it
as reviewed metadata when deciding the outstanding runtime/cache/namespace
premises and the separately authorized actual profile step. It must not be
promoted to actual-runtime acceptance or execution evidence by renaming a file
or reinterpreting this review. RET remains paused.
