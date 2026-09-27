# RI121 static startup/import review

Status: **candidate-only static findings; not a runtime inventory, profile,
admission or established execution trace**. This review identifies startup
premises which the proposed RI121 source packet does not yet completely guard.
The proposed RI121 packet and installed runtime were not modified.

Reviewer: `/root/ri116_saved_arithmetic_review/ri121_applicability_review`.
Only text, directory/symlink metadata, opaque hashes and16-byte cache headers
were inspected. Metadata tooling used `/usr/bin/python3 -I -B`, not the candidate
Homebrew/recovery interpreter. No candidate Python, target, caller, candidate
stdlib module, bytecode payload, compiler, AST processor or runtime probe was
invoked. No scientific input, active freeze/admission, repository or git action
occurred. Mach-O/dependent-library work belongs to the parent's separate review.

For paths below, S denotes:
`/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11`.
V denotes:
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env`.
These are abbreviations for precise local source references, not import roots
learned from a running candidate.

## Concrete startup findings

1. **A higher-priority venv configuration is outside the declared roots.**
   V/pyvenv.cfg:1–5 states the Homebrew home, version3.11.6 and
   include-system-site-packages=false. Installed S/site.py:504–513 searches
   V/bin/pyvenv.cfg first, then V/pyvenv.cfg, and uses the first existing file.
   V/bin/pyvenv.cfg was absent and not a symlink during this static inspection.
   The proposed runtime_support.py:16–22 requires V/pyvenv.cfg but its only
   declared absent path is python311.zip; it does not bind that higher-priority
   configuration absence. A fresh candidate guard must bind its absence or
   explicitly review and pin it. Present absence alone is not an active guard.

2. **Isolated mode still has an actual third-party startup hook.**
   S/site.py:160–201 executes `.pth` lines beginning with import; lines207–226
   enumerate and process `.pth` files. V/lib/python3.11/site-packages contains
   distutils-precedence.pth. Its sole line defaults SETUPTOOLS_USE_DISTUTILS to
   local and imports `_distutils_hack`, then calls add_shim. The fixed caller
   environment does not set that variable. The source-predicted startup route
   therefore installs this hook; this has not been observed by running Python.

   Both the venv and `/opt/homebrew/lib/python3.11/site-packages` copies of
   distutils-precedence.pth are151 bytes with SHA256
   `2638ce9e2500e572a5e0de7faed6661eb569d1b696fcba07b0dd223da5f5d224`.
   Both corresponding `_distutils_hack/__init__.py` sources are6299 bytes with
   SHA256 `46849a60a7cc85189cf6b5ac62b3f135004862ce6a96540a81c95ef6fbc4dc3e`.
   I read that complete source. It imports sys/os at lines2–3; add_shim and
   insert_shim at202–215 insert a finder into sys.meta_path. Its ordinary
   find_spec route at89–97 returns no replacement for unrecognized module names.
   Conditional distutils handling at99–138 imports setuptools._distutils and
   consults a relative pybuilddir.txt; pip/test handling is also conditional.
   No fixed caller/science direct import requests distutils, pip or those tests.
   Those branches must not be mistaken for an observed actual import trace.

   With the unchanged false venv setting, site.py:528–539 confines PREFIXES to
   the venv and disables user site. System-site `.pth` processing is therefore
   not the predicted route, although retaining its whole tree is conservative.
   This depends on the exact chosen config and trusted startup implementation.
   The venv `.pth` can be processed twice through site.py:531 and603; add_shim
   tests finder membership before reinsertion. Do not classify the whole process
   as stdlib-only merely because the three scientific modules are stdlib-only.

3. **Homebrew sitecustomize adds paths outside the three declared roots.**
   S/site.py:544–561 and609 import sitecustomize even in isolated mode.
   S/sitecustomize.py exists; it is3426 bytes with SHA256
   `d537eac36341d38454ed3bd8fae3e63b84de65ef89ee8632681e140360c1e160`.
   I read the complete source. Lines4–7 import re/os/site/sys. Lines19–47 rewrite
   path aliases and base prefixes, so an expected runtime profile must not be
   guessed merely from the resolved interpreter filename. Lines49–52 append:

   - `/opt/homebrew/opt/python-tk@3.11/libexec`
   - `/opt/homebrew/opt/python-gdbm@3.11/libexec`

   if those directories exist. Both opt trees/libexec paths were absent in the
   static check. They lie outside the proposed three roots. Their absence must
   be maintained by an explicit prospective guard or their resolved membership
   must be incorporated and reviewed. A post-startup sys.path comparison is
   useful evidence but does not prevent unreviewed startup code from having
   executed already. No usercustomize candidate was found in the four inspected
   stdlib/lib-dynload/venv-site/system-site roots. User customization is also
   source-disabled under the unchanged venv configuration.

## Bytecode and source-selection alternatives

`-B` prevents writes; it does not force imports to use reviewed `.py` text.
S/importlib/_bootstrap_external.py:1007–1071 reads and validates an available
cache before source compilation. The dont_write_bytecode condition is at1076
on the write path. Lines469–478 choose normal versus opt-1 cache names.
Timestamp cache validation compares truncated source mtime and size at694–700;
hash-based choices are separately handled at1043–1055. FileFinder also permits
extension, source and standalone bytecode alternatives at1733–1741.

The observations record18 cache files for12 selected source paths, plus the
two sitecustomize caches in the supplement. The selected core modules fractions,
decimal, _pydecimal, contextvars, hashlib, subprocess, pathlib and copy have
normal and opt-1 caches. Both `_distutils_hack` roots have a normal cache but no
opt-1 cache in this observation. The18 examined initial headers have flags0 and
matching source timestamp/size fields. Sitecustomize normal/opt-1 cache bytes
are equal; both are4191 bytes, SHA256
`e46ce96badf953b5c4d2a6ab93d949782b2d25885e7380cc65e9b6b4c46b2981`.

No payload was unmarshalled, disassembled, compiled or executed. Matching
timestamp/size is not proof that a cache payload corresponds to its source.
Whole-tree runtime pins must include caches as executable alternatives; a source
review alone does not establish that equivalence. Content-only pins also do not
determine timestamp-based route selection if source mtimes change. The actual
candidate review must explicitly decide its trusted-build/cache premise and/or
record the permitted selection metadata. Current loaded_files records __file__
and its pin, not the actual cache payload selected. Frozen/builtin startup code
can reside in interpreter/framework bytes; companion installed Python text is
not proof of which frozen implementation actually ran.

The source-captured science modules and captured helper loader use explicit
compile of captured bytes, which avoids their ordinary import-cache selection.
This does not remove startup and imported stdlib/site cache alternatives.

## Fixed import branches and the decimal fallback

Fixed direct science imports are fractions, itertools, json, re and copy.
Helpers add hashlib, importlib.util, os/pathlib, signal/stat, subprocess, sys and
time. These were checked textually in the proposed RI121 helper sources and accepted RI119 scientific sources.

Fractions imports Decimal at S/fractions.py:6. S/decimal.py:2–11 tries _decimal
and catches ImportError to load _pydecimal. The parent's static Mach-O review
reported an absent libmpdec.3 dependency; this review independently confirms
the textual fallback but does not establish which route would actually load.
S/_pydecimal.py imports math/numbers/sys at156–158, optionally collections at161,
contextvars at440 and re at6130. S/contextvars.py:1 imports _contextvars. Other
locale/itertools imports are conditional function paths. Both source and both
cache modes, _contextvars and its applicable libraries belong in candidate
coverage; silently presuming the fast decimal extension is unsupported.

Other source-visible alternatives include json's _json accelerator/fallback,
hashlib's _hashlib/OpenSSL versus builtin digest routes
(S/hashlib.py:82–139,169–184,303–310), and subprocess's fcntl/msvcrt/platform
branch (S/subprocess.py:57–119). copy tries org.python.core at59–62. No org or
msvcrt candidate was found in the four inspected import roots. Whole-tree
membership checks cover changes within those roots; external path/startup
alternatives still need their own guards. This is a useful branch map, not a
claim of a complete observed import graph. The parent's non-OS library/config
closure review must be combined with these findings.

## Exact remaining candidate premises

- Bind the four interpreter links and installed framework/binary bytes, the
  chosen venv config and the higher-priority config absence before startup.
- Bind the absence or exact resolved closure of both Homebrew split libexec
  paths and the declared python311.zip alternative. The additional observed
  python._pth/python3.11._pth absences in the metadata are observations only;
  this review has not established that this build consults those names.
- Include and review the actual .pth, _distutils_hack, sitecustomize and their
  cache alternatives; preserve the exact env-cleared invocation. Do not infer
  all startup behavior from -I or from scientific import statements.
- Establish actual profile/import provenance only after a root-authorized
  runtime step. No profile or active inventory was constructed here. Actual
  loader/frozen/cache behavior and complete non-OS library closure remain open.
- Preserve the root's explicit Apple shared-cache/kernel trusted-platform
  premise. It does not exempt Homebrew, setuptools, OpenSSL, mpdecimal or other
  third-party paths/configurations.

The proposed RI121 files remain unchanged. These new static findings require
root adjudication and, where needed, separately reviewed source/guard repairs
before claiming a complete admitted runtime closure. They do not retroactively
invalidate historical scientific results and do not authorize execution.

Supporting observations:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| STARTUP_STATIC_OBSERVATIONS.json | 19197 | 9485111acd97d3d83a2e1d3684bedeeb14f77e03fc09ee40a9bfefdc08dd9bae |
| STARTUP_STATIC_SUPPLEMENT.json | 6702 | 97b7609f8df4756f43b835d16bf6e5b5fdfd2ce5e775cc4a727ab32de83cd17d |

These selected static records are not a complete runtime inventory. Raw tool
evidence includes58ddc0/8e5d6e for site/hooks,182606 for decimal/cache paths,
9cdac7 for Homebrew customization and loader source,929319 for absent split
paths, and3c44b8/c2b287 for the supporting observation files.
