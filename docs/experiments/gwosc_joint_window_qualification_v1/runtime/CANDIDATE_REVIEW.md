# RI121 runtime inventory candidate

Status: **metadata candidate prepared; root runtime acceptance, actual profile establishment and execution admission remain pending.** This reservation contains no production `RUNTIME_INVENTORY.json`, active freeze, admission card or scientific output.

The user-authorized coordinator explicitly authorized reading and hashing current candidate-runtime files. The independent collector ran with `/usr/bin/python3 -I -B`, not the candidate Homebrew/venv interpreter. It did not import, execute, compile, AST-parse or probe the accepted runtime helper, caller or scientific target. No repository/index/git actions occurred. All candidate runtime inputs were read without modification.

## Captured domain

The candidate is shaped exactly for the accepted `runtime_support.py` v2 at `ri121-synthetic-caller-repair-7ys8vsc3/runtime_support.py`,8184 bytes, SHA256 `525314ee292722c50ab0bdf635123d3c36acbb96a76d60368c9677872fc2c40f`. The file was read as text and opaquely hashed; its functions were not imported or called.

| Component | Candidate observation |
|---|---:|
| Declared whole Python roots |3|
| Regular files in installed stdlib root |2878|
| Regular files in venv site-packages root |5313|
| Regular files in system site-packages root |1719|
| Exact permitted stdlib symlinks |3|
| Ordered mandatory absence checks |8, all absent and not symlinks|
| Mandatory extra files |6|
| Conservative optional extra files |7|
| Loader bindings |1 mandatory plus7 optional|
| Unique inventoried regular files, including extras |9923|
| Total file bytes |258862951|
| Captured `.py` files |4721|
| Captured `.pyc` files |3394|

The candidate's only eight top-level keys are `schema`, `roots`, `extra_files`, `files`, `symlinks`, `absent_paths`, `loader_bindings`, and `scope`. The schema is `ri121-complete-stdlib-runtime-inventory-v2`. Roots, allowed links and absences retain the exact order and values required by v2. Extras and loader names are sorted and unique. Every loader's resolved regular-file target is included in extras. Scope explicitly labels the JSON inert and unadmitted.

`RUNTIME_INVENTORY.candidate.json`: **2806092 bytes**, SHA256 `b6f0fd3244cef06c16da19922db212695387926e2f94012d1857c7c8793f7edc`.

The six required extras are the existing venv configuration, interpreter executable, Python framework, `/bin/ps`, OpenSSL configuration and exact libcrypto3.6.0 file. The required literal libcrypto binding matches all v2 path/link/size/hash fields. The separate `INTERPRETER_BINDING.candidate.json` records the named venv interpreter's complete observed four-link chain, resolved file and pin; this is filesystem evidence, not an invocation or inferred `sys.version`/`sys.path` profile.

## Conservative optional native files

The optional additions are exactly the three additional standard-extension dylibs and four provider/engine files already inspected in `ri121-static-runtime-closure-ulnsAMI8/STATIC_LOAD_COMMAND_CANDIDATES.json`:

- libssl3.6.0, liblzma5.8.2 and libsqlite3.51.2;
- OpenSSL `legacy`, `loader_attic`, `capi` and `padlock` module files.

Their literal loader-name bindings and resolved bytes are captured. This is a finite conservative superset; it does not claim that the fixed synthetic call loads any of them. The static graph's complete dependencies/limits remain the basis for inclusion. This packet performs no new OpenSSL behavior/configuration adjudication and does not duplicate the separate QR3.14 OpenSSL review.

`OPTIONAL_NATIVE_NAMESPACES.candidate.json` separately records exact recursive member names, types and literal symlink text, without following symlinks, for three canonical library directories. Their observed membership counts are20 for OpenSSL,5 for xz and6 for sqlite. The OpenSSL recursive record explicitly includes both provider/engine subdirectories and their four files. Namespace entries for unselected archives, package metadata or link aliases are descriptive metadata, not claims that all their bytes are executable prerequisites.

**The accepted v2 helper verifies pinned files and bindings; it does not enforce these optional directory-membership records.** Root must adjudicate whether to retain this conservative candidate and how any prospective namespace custody is established. This separate evidence must not be described as an already implemented active guard.

## Source/cache selection metadata

`FILE_SELECTION_METADATA.candidate.json` records each inventoried file's device, inode, mode, size, mtime and ctime. Each `.pyc` additionally has its first16 opaque bytes. No bytecode payload was unmarshalled, disassembled, interpreted, compiled or executed. All existing cache bytes remain in the main candidate inventory.

`SOURCE_CACHE_ROUTES.candidate.json` is derived solely from those saved inventory/metadata records. It pairs53 selected installed source files relevant to startup and fixed textual imports with normal, opt-1 and standalone-bytecode candidate names.85 of these cache names exist in the captured full namespaces. All85 observed headers have timestamp format flags0 and timestamp/size fields matching the captured source metadata. These matches describe a possible selection route; **they do not prove bytecode/source equivalence or show which files actually load**. All other source/cache files remain fully captured, even where no selected-route table row is given.

The installed `_distutils_hack` startup sources/caches and Homebrew `sitecustomize` alternatives are included. `-B` inhibits bytecode writes but does not exclude cache reads. Frozen/builtin startup implementations may reside in interpreter/framework bytes, so installed Python text alone is not an actual startup trace. The missing libmpdec3 names remain absent; no mpdecimal replacement was installed and no `_decimal`/`_pydecimal` branch was invoked. Root retains responsibility for the actual fallback/profile and trusted-cache premises.

## Capture checks and evidence boundary

The collector independently traversed with `os.scandir`, never through the candidate helper. It hashed each regular file while checking descriptor/name identity, bytes and before/after metadata. It then repeated complete tree membership/link enumeration, all file selection metadata checks, all eight absences, all optional directory namespaces, loader bindings, interpreter binding and the accepted helper pin. All these checks passed for this capture. The collector itself is preserved for review; rerunning it is not necessary to understand the packet.

Actual tools: `bf9b1d` launched the metadata collector and `883303` recorded its successful completion. `211ea9` derived selected cache-route metadata from saved JSON only; `7b4d72` checked the saved header-match and namespace summaries. These are file/metadata operations, not scientific or candidate-runtime qualification.

The Apple kernel/loader/shared-cache boundary remains the explicit trusted platform premise accepted by the coordinator; this is not a whole-OS byte snapshot. Entire declared Python trees include supporting packages which were hashed opaquely, not imported. No empirical HDF5/PSD, RI116 result body, RI73 native coefficient capture, new scientific data or native operand was supplied to executable scientific code.

Independent review is complete in `INDEPENDENT_METADATA_REVIEW.md`,8296 bytes, SHA256 `510270fed72ab7bc5ed089b5059bfd4cdb26bfb7f60636620243abeaf27b97d6`. The separate reviewer rehashed all9923 files/258862951 bytes, independently reconstructed complete membership, links, absences, bindings, metadata and all53 selected cache-route rows, and found no discrepancy. This is independent verification of the metadata candidate, not an actual runtime or scientific check.

Next: root adjudication of runtime/cache/optional-namespace premises, then a separately authorized actual profile step. Root alone may turn reviewed metadata into a production inventory and proceed to admission. This candidate does not establish success of any future profile, normal/optimized execution, control campaign or scientific result.
