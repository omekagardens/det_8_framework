# RI122 runtime and historical scope

Author: /root/ri117_t1_lemma. Source-only preparation for the retained-supervision
caller. No target or Python interpreter was invoked; no native coefficient,
scientific certificate, stdout, report, or scientific result body was decoded.
No active freeze, admission, candidate, descriptor, receipt, qualification,
root decision, repository change, or Git action is produced by this work.

## Result and exact boundary

The separate current runtime capture is complete as a **source-preparation
candidate under the owner's explicit trusted-host premise**, not a hermetic
OS image or execution claim. The whole runtime manifest must be authenticated
before parsing. Caller/source review and genuine future sequential custody are
still prerequisites; the source manifest itself authorizes no launch.

RUNTIME_CLOSURE.json: 2,862,854 bytes; SHA256
35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920.

It contains 2,988 distinct literal file identities (103,009,117 bytes counting
literal aliases separately), 258 exact directory-membership records containing
3,526 names/types, and 40 explicit lstat-ENOENT absences. Equal bytes or resolved
paths do not collapse literal paths. Each opaque file hash checks pre/post
device, inode, mode, size, mtime and ctime, plus re-resolved literal link chains;
atime is not pinned.

All recorded file identities, directory membership and absences were freshly
reconciled after the configuration correction in metadata-only chunk 795fe3.
That check also preserved all 2,986 prior file identities and 256 directory
records exactly, and confirmed the historical manifest unchanged. The complete
87-image static Mach-O graph was separately reconciled in 880098. These are
metadata checks, not execution of the
caller, producer, auditor, Python, extension modules, or dynamic libraries.

## Actual executable and launcher paths

The fixed literal launch path is /opt/homebrew/bin/python3. Fresh component
resolution observed exactly these links, in traversal order:

1. /opt/homebrew/bin/python3 ->
   ../Cellar/python@3.14/3.14.0_1/bin/python3
2. /opt/homebrew/Cellar/python@3.14/3.14.0_1/bin/python3 ->
   ../Frameworks/Python.framework/Versions/3.14/bin/python3
3. /opt/homebrew/Cellar/python@3.14/3.14.0_1/Frameworks/Python.framework/Versions/3.14/bin/python3 ->
   python3.14

The resolved launcher is
/opt/homebrew/Cellar/python@3.14/3.14.0_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14.

It is not treated as sufficient on its own: static strings name
__PYVENV_LAUNCHER__ and Resources/Python.app/Contents/MacOS/Python. The capture
therefore includes the entire small framework Resources/Python.app tree,
Resources metadata, its actual executable, the framework Python binary, and
framework code-signature metadata. Static strings are not a measured launch
trace. The launcher, app and framework dependencies were separately inspected.
The configured /opt/homebrew/opt/python@3.14 framework alias and its component
links also remain protected.

## Complete installed standard-library surface

The actual framework lib/python3.14 tree was enumerated afresh, not inferred
from a version label or an old count:

- 2,959 regular files, 244 directories, 66,694,350 regular-file bytes;
- 1,831 Python sources;
- 484 existing bytecode files: 309 normal, 175 opt-1, zero opt-2;
- all 76 extension modules;
- all remaining data, tests, build/configuration and package files;
- three literal links, retained in exact directory membership.

The two config-3.14-darwin libpython library aliases are separately hashed through
their literal links. The third link is site-packages; its subtree is deliberately
excluded under the fixed -I -S contract, while the literal link and target text
remain pinned. A directory or dangling symlink is never mislabeled absent.

The installed manual says -B suppresses bytecode writes, not bytecode reads.
All existing cache variants are therefore captured. Exact namespace membership
also rejects new cache files, import-shadowing sources, packages, extensions or
links rather than silently permitting any file omitted from the old inventory.

## Static import-path justification and its limit

This is a static installed-layout argument, not a measured sys.path or a formal
proof of CPython startup. The pinned installed configuration declares:

- version 3.14, PLATLIBDIR=lib;
- prefix and exec_prefix equal to the configured framework version directory;
- no COREPYTHONPATH/PYTHONPATH build additions.

The installed manual states that -I implies -E/-P/-s, ignores PYTHON*
environment variables, and omits the script/current unsafe path and user site
path. Its -S section and site.py lines719-722 disable ordinary site-dependent
path mutation, including on a later plain import. The caller has a fixed
minimal environment and must not explicitly invoke site.main(), mutate the
search path or introduce arbitrary loader/plugin work.

The installed library landmarks, actual framework/launcher/app links, pure
stdlib and lib-dynload namespaces are captured. Possible python314.zip paths,
venv markers, ._pth overrides and build markers in this fixed launch/layout
surface have explicit absence records. Configured-prefix aliases are retained.

The installed Makefile's FROZEN_FILES_IN/OUT declarations were read at
lines1863-1914 and both the framework binary backing and available source/cache
variants are pinned. The declaration is not a live import list. The absence of
an independently proved or measured frozen-getpath trace remains explicit;
we rely on the exact pinned CPython binary and its installed flag/configuration
contract. No source-time Python probe is permitted to disguise that limit.

## Native dependency boundary

Static load-command traversal started from the launcher, app, framework, all
76 installed extensions, /bin/ps and the small installed provider namespace:
81 initial images, 87 resolved images.
It followed all observed non-system loads recursively. Six distinct external
Homebrew library images occur: mpdecimal, libcrypto, libssl, liblzma, sqlite and
zstd. The separately captured legacy provider module depends on already-pinned
libcrypto and trusted libSystem. Capturing that module is not a claim that the
fixed hashing workload activates it. Libssl names libcrypto through an
additional Cellar literal path; that literal is preserved independently of the
opt alias.

All observed non-system load names are absolute. LC_ID_DYLIB is a recorded
install ID, not followed as an extra dependency. LC_RPATH values are recorded;
no observed dependency needs an unresolved @rpath choice. There are zero
unresolved static non-system dependencies. The actual default OpenSSL
configuration consultation during hashlib initialization is inside the required
closure, as detailed below. Arbitrary later dlopen behavior remains outside the
independently source-reviewed fixed workload; it is not used to exclude actual
configuration inputs from that workload.

Eleven named Apple system dependencies, including /usr/lib/dyld, are recorded
with source images and literal location observations. Ten are absent as ordinary
files; /usr/lib/dyld is observed as a regular file. Neither observation establishes
shared-cache membership. Cache contents and membership remain uninspected
under the owner's expressly authorized kernel/loader/Apple shared-cache
premise. No Homebrew dependency uses that exception.

The visible host identity is Darwin 25.5.0 arm64, macOS26.5.2, build25F84.
The complete uname version string and the pinned SystemVersion.plist are in
the manifest. Caller pre/admission/final observations must retain visible drift
and unavailable status. This is not a cryptographic identity of the OS image.

## Corrected OpenSSL configuration and bootstrap boundary

The initial runtime candidate omitted the default OpenSSL configuration used
by actual hashlib initialization. Root preserved that candidate, scope and
associated preliminary callers/review byte-exact in pre_config_review, with
PRE_CONFIG_REVIEW_PRESERVATION.json recording their identities. The correction
was made before execution or final sealing; the former source-only pass is not
silently retained as acceptance of the corrected closure.

The required /opt/homebrew/etc/openssl@3/openssl.cnf is now byte-pinned and its
directory has exact membership. The complete390-line file was read: its active
initialization routes only to the default provider; there are no active includes,
external module paths, explicit provider activations or engine sections. The
installed ossl-modules directory contains only legacy.dylib; that file, the
directory namespace and its static dependency row are now captured. Existing
config-directory backup/certificate/private/misc entries are names only, not
claims that their contents were accessed or hashed as SHA256 dependencies.

Upstream CPython3.14 and OpenSSL3.6 source support configuration consultation
and the builtin default-provider path. This is static correspondence with the
pinned installed binaries/configuration, not a measured startup or provider
trace. The source links, exact local evidence, scoped exclusions and attribution
are in OPENSSL_CONFIG_CLOSURE_REVIEW.md.

The exact fixed launch environment excludes OPENSSL_CONF,
OPENSSL_CONF_INCLUDE, OPENSSL_MODULES and OPENSSL_ENGINES. There is no active
include to recursively capture; a config change requires renewed review.
The fixed hashing workload does not request engine, TLS/CA or CT-log operations.
Their inactive file contents are excluded on that source/config basis, not
because Homebrew configuration is trusted as part of the operating system.

The caller imports hashlib before its own manifest checks. In-process checks
cannot retroactively authenticate already-loaded interpreter/crypto/config
bootstrap inputs. Before any future Python launch, the root owner must perform
independent external custody authentication of the pinned application runtime,
config, namespace, host premises and exact launch environment. Later caller
pre/admission/final checks detect observed drift; they are neither a sandbox
nor a proof that nothing changed between observations. No new harness,
environment override or runtime execution was introduced here.

## Historical custody — preserved separately, not replaced

I completely read the old RI115 caller contract, HISTORY_NOTES, HANDOFF,
ROOT_SOURCE_ADJUDICATION, WITNESS_APPLICABILITY and actual AUDIT_BINDING. The
main agent owns the new historical reconciliation and extension. This runtime
capture neither edits nor reinterprets old evidence.

The old 560-path inventory, original/copy paths, legacy and RI109 role
memberships, genuine zero-byte files, equal-byte distinct paths, actual witness/
normal/optimized/audit custody, known failure inventories, preparation incidents,
and superseded-reference explanations remain historical evidence. Their old
counts are not new RI122 closure counts. Actual later RI115 records must remain
included; an old source-time HANDOFF's then-unknown future outcome must not
erase records that subsequently came into existence.

The actual old audit binding names all three identical-byte candidate copies,
actual three-mode root custody and genuine outer tool records. They are
historical metadata, not future RI122 custody. Old synthetic shape qualification
does not qualify changed guards, runtime namespace logic or revised source.
All scientific payloads stay opaque. No missing old receipt is invented.

The parent's separate history extension must also retain RI117 and RI120
accepted proof/source packets, the independent owner review, current assignment
and host-platform decision, plus original/copy/runtime/failure provenance.
Nothing here transfers RET work or modifies RET's paused status.

## Reading and preparation disclosure

Required root adjudication, RI122 assignment, owner399-line review and old
contract/history/handoff/binding documents were completely read. The first
combined owner-review/contract display was truncated; the later owner-review
range221-399 was reread explicitly, completing coverage.

The first large read-only runtime inventory stdout was tool-truncated (9538d8).
Metadata parsing refused at its warning rather than accepting partial data.
It was replaced by bounded batches with exit and truncation checks. No artifact
was written from that failed parse. Full final metadata reconciliation succeeded.

Installed configuration, manual, site.py, Makefile frozen declarations and
Mach-O metadata were inspected as source/text. No claim is made that every
stdlib source was semantically read; its **complete bytes and namespace** were
opaque captured. No Python/target import, parse, AST, compilation, probe,
execution, replay, scientific decoding or arithmetic occurred.

## Bound documents read completely

- `/Volumes/AI_DATA/development/det-review-evidence/ri120-root-source-review-sksu97l1/ROOT_ADJUDICATION.json`
  4346 bytes; SHA256 `35554c18567e610ce450b3e804794edba20e3d552e7119318041691655c706d5`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-root-source-review-sksu97l1/RI122_ASSIGNMENT.json`
  3331 bytes; SHA256 `4c4d6a0ed4c2ef8ccde1d9c75f88a6f5d0af00cb34e0125e7ac7ead6c868ee6f`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-root-source-review-sksu97l1/RI122_HOST_PLATFORM_SCOPE_DECISION.json`
  2603 bytes; SHA256 `d575e6643e1cb44940218480be40d77e48a0b1ec4206e6af120365206270226b`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-independent-owner-source-qbk3z5e4/INDEPENDENT_COMPLETE_SOURCE_REVIEW.json`
  26360 bytes; SHA256 `b5dfacd3cc4b8c38c63506fb997cab961f715b1773a16c14ccd6904731511eef`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/CALLER_CONTRACT.md`
  19220 bytes; SHA256 `a283f82da1e696f468d281d7824d650ae04e87d0fdb794d625c340321d09efa2`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/HISTORY_NOTES.md`
  8680 bytes; SHA256 `95f9529c3c0d76efb8029b40aca073c7fa0a51ffe070d8b2ca8abf2fd82505c2`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/HANDOFF.md`
  5049 bytes; SHA256 `e8d3d0708859df8ea7adbdd4a2c10f2d62a6971be30247935f4142722b5015e2`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/AUDIT_BINDING.json`
  6132 bytes; SHA256 `7e0ebe85c36405143dbff61ec5a86e8f1ce346773324bf709b22b7f89b04f9e0`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/WITNESS_APPLICABILITY.json`
  4426 bytes; SHA256 `e0715838eddda9d30538e7732b12d46a9a907f85c2a30d69b39af8a665807265`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/ROOT_SOURCE_ADJUDICATION.json`
  3160 bytes; SHA256 `c1a0d6bfa5b41d4755ecb8c3b4366cdb290f2f507ed8dfaea7fb3d7c8007e3c7`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx/RUNTIME_INTERFACE.md`
  5101 bytes; SHA256 `f3c6d78e2687d4bda6dad5f97909608afcb9c0eec47ccc822580cd860b343679`.
