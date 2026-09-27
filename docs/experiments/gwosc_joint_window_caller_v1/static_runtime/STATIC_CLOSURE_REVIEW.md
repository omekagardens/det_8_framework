# RI121 static candidate runtime closure review

Status: **candidate closure findings only; fresh runtime establishment and root admission remain outstanding.** RI121 and RI119 originals are unchanged. No candidate interpreter, caller, helper, scientific target, sign enumeration, target import, compilation, AST parse or runtime probe was invoked. No active inventory, profile, freeze or admission was created. This report uses textual reads, filesystem metadata and Apple static Mach-O tools. A separate `/usr/bin/python3 -I -B` metadata script parsed saved `otool` text and named-path metadata; it did not load candidate code.

The controlling platform boundary is the root's `ri120-root-source-review-sksu97l1/RI122_HOST_PLATFORM_SCOPE_DECISION.json`: Darwin kernel/loader/Apple system shared-cache implementation may be explicit trusted premises. Homebrew and other third-party dependencies are outside that exception. These findings do not reclassify historical RI115/RI116 runs.

## Finding and recommended finite next action

The existing three-tree RI121 inventory domain is a useful conservative Python-file domain, but it is insufficient by itself to establish the runtime closure. Before any execution admission, the successor needs explicit guards for the core OpenSSL library/configuration, the startup alternatives identified below, and the missing decimal-library fallback. The installed scientific source still uses only standard-library import names; that does **not** mean the actual supporting runtime is free of third-party native libraries or startup hooks.

1. Bind the actual `_hashlib` load name `/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib` through its literal `opt` link to `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libcrypto.3.dylib`; pin the selected bytes and `/opt/homebrew/etc/openssl@3/openssl.cnf`. Preserve and verify the fixed environment without `OPENSSL_*` or `DYLD_*` overrides. Root must adjudicate the pinned default-provider/no-external-activation premise, or explicitly capture and constrain the finite optional provider/engine set below.
2. Preserve explicit absence or separately reviewed binding of `env/bin/pyvenv.cfg`, the Homebrew `python-tk@3.11/libexec` and `python-gdbm@3.11/libexec` alternatives, and the existing `python311.zip` alternative. These are concrete installed-source lookup routes. The present RI121 inventory schema fixes `absent_paths` to the ZIP alone; it cannot encode all these premises unchanged.
3. Decide explicitly to retain the currently indicated `_pydecimal` fallback, subject to fresh actual root verification, or establish a different runtime separately. Do not relabel mpdecimal4 as the requested mpdecimal3 ABI. Retaining the fallback requires controlling the missing literal libmpdec3 name and applicable fallback alternatives, and recording that the pure-Python decimal branch is part of the candidate closure. A missing optional acceleration library is not by itself a failed scientific result.
4. Treat all usable normal/optimized standard-library/startup bytecode as executable alternatives, covered by the whole-tree byte inventory. Do not infer executable equivalence from `.py` text alone. The actual RI119 scientific source is captured and loaded by the reviewed source route; this point concerns supporting imports.
5. Use the exact external dependencies and conservative optional list below when root establishes the runtime. A full75-extension static dependency superset is supplied to make that decision finite. It is not a claim that all75 modules are loaded, nor a reason to run unused modules.

The immutable RI121 `control.file_pin` checks a final nonsymlink file but does not by itself bind symlinked ancestor components. Canonical extra-file pins alone cannot establish which bytes an `opt` load name selects. Its existing `control.binding` provides the relevant finite name/link/target model, if adopted in the separately reviewed successor. No new guard implementation is supplied here.

## Exact static Mach-O coverage

`STATIC_LOAD_COMMAND_CANDIDATES.json` is a parse of two saved complete `otool -l` outputs: executable, framework and all75 installed standard-library extension images, followed by eight existing candidate non-OS libraries/modules. It contains85 image records. Install IDs (`LC_ID_DYLIB`) are explicitly separate from load edges. It is a static graph, with no runtime acceptance schema or byte inventory.

The exact CPython executable is:

`/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/bin/python3.11`

It is an arm64 Mach-O executable. Its sole non-OS `LC_LOAD_DYLIB` edge is the sibling framework:

`/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/Python`

The framework is arm64 and has only Apple CoreFoundation and libSystem dependencies. Its `/opt/homebrew/opt/python@3.11/.../Python` line in `otool -L` is its **install ID**, not an additional dependency. The framework declares `LC_RPATH /opt/homebrew/lib`. None of the observed85 images has an `@rpath`, `@loader_path`, or `@executable_path` load edge. The only other observed rpath is sqlite's `/opt/homebrew/Cellar/sqlite/3.51.2/lib`. No observed image has an `LC_DYLD_ENVIRONMENT` command. These rpaths do not convert an absolute mpdecimal load name into a search for libmpdec4.

## Fixed-import non-OS dependency and missing branch

| Installed extension | Static non-OS load name | Current static resolution and implication |
|---|---|---|
| `_hashlib.cpython-311-darwin.so` | `/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib` | `opt/openssl@3 -> ../Cellar/openssl@3/3.6.0`; actual target `.../3.6.0/lib/libcrypto.3.dylib`; only libSystem transitive Mach-O dependency. Hashlib is directly imported by the caller custody helpers. |
| `_decimal.cpython-311-darwin.so` | `/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib` | Missing. `opt/mpdecimal -> ../Cellar/mpdecimal/4.0.1` contains libmpdec4, not3. `fractions.py` imports Decimal; `decimal.py:2–10` tries `_decimal`, then catches ImportError and imports `_pydecimal`. The actual selected branch has not been executed here. |

`hashlib.py:170` attempts `_hashlib`, and its constructor setup can fall back to `_md5`, `_sha1`, `_sha256`, `_sha512`, `_sha3`; `_blake2` is deliberately preferred. All those fallback extension files were included in the75-image inspection and have only Apple libSystem edges. JSON's `_json`, subprocess's `_posixsubprocess`/`select`/`fcntl`, mathematical `math`, and `_pydecimal`'s `contextvars -> _contextvars` likewise add no non-OS Mach-O edge in the inspected build. This statement concerns observed files and installed source routes; it is not a runtime-loaded-module trace.

Observed absent decimal names: `/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib`, `/opt/homebrew/lib/libmpdec.3.dylib`, `/usr/local/lib/libmpdec.3.dylib`, `/usr/lib/libmpdec.3.dylib`. Installed `/usr/share/man/man1/dyld.1:110–116` describes `/usr/local/lib:/usr/lib` as the default fallback for older binaries, with no default fallback for newer binaries. Do not infer the complete actual platform loader search from these filesystem absences alone: root must state the applicable host-loader premise. The extra `/opt/homebrew/lib` observation is conservative metadata, not an assertion that the absolute edge uses that rpath.

## Optional75-extension superset, not demonstrated fixed-call reachability

Only three additional extension types among all75 introduce further non-OS names:

| Optional extension | Literal name and current selected file | Transitive non-OS edge |
|---|---|---|
| `_ssl` | `/opt/homebrew/opt/openssl@3/lib/libssl.3.dylib` -> `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libssl.3.dylib` | Exact Cellar `libcrypto.3.dylib`, plus Apple libSystem. `_ssl` also directly loads the opt `libcrypto.3.dylib` name. |
| `_lzma` | `/opt/homebrew/opt/xz/lib/liblzma.5.dylib`; `opt/xz -> ../Cellar/xz/5.8.2`; target `/opt/homebrew/Cellar/xz/5.8.2/lib/liblzma.5.dylib` | None; Apple libSystem only. |
| `_sqlite3` | `/opt/homebrew/opt/sqlite/lib/libsqlite3.0.dylib`; `opt/sqlite -> ../Cellar/sqlite/3.51.2`, file link `libsqlite3.0.dylib -> libsqlite3.3.51.2.dylib`; target `/opt/homebrew/Cellar/sqlite/3.51.2/lib/libsqlite3.3.51.2.dylib` | None; Apple libSystem/libz only. |

These are finite conservative alternatives, not asserted necessary imports for the fixed scientific call. Capturing them is one possible conservative root choice; excluding them requires a justified import-path/runtime premise, not just observing that they are absent from the scientific top-level imports. All remaining extension load edges are Apple paths and are recorded in the static graph. In particular this build's `_ctypes` uses Apple `/usr/lib/libffi.dylib`, and `readline` uses Apple libedit/libncurses, not Homebrew variants.

## OpenSSL inputs outside the Mach-O load table

The installed libcrypto strings name `OPENSSLDIR /opt/homebrew/etc/openssl@3`, `MODULESDIR /opt/homebrew/Cellar/openssl@3/3.6.0/lib/ossl-modules`, and `ENGINESDIR /opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3`. Installed OpenSSL3.6 documentation (`share/man/man3/OPENSSL_init_crypto.3ssl:229–245`) states that loading configuration is a default initialization option. `_hashlib`'s static undefined symbols include `EVP_MD_fetch`, `EVP_MD_do_all_provided` and other provider-sensitive functions. No actual initialization was performed here.

The currently read `openssl.cnf` is12324 bytes and has no active `.include` directive. Its active `openssl_init` selects `provider_sect`, which names only `default_sect`; the `activate` line is commented, and there is no active external-provider/engine module path. The config is copied as textual evidence, not treated as already frozen. The installed default-provider manual describes automatic default-provider selection if no other provider has been loaded. This supports a **candidate no-external-activation premise**, not a dynamic-load observation.

Four optional module files exist in the embedded directories:

- `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/ossl-modules/legacy.dylib`
- `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/loader_attic.dylib`
- `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/capi.dylib`
- `/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/padlock.dylib`

All four were statically inspected. Each loads the exact Cellar3.6.0 libcrypto and Apple libSystem only. Their existence does not mean hashing loads them. Conversely, excluding the configuration/provider question on the basis of `otool -L` alone would miss an actual class of runtime inputs. No certificates, keys, CA operations, network destinations or unrelated sample-config paths are treated as scientific dependencies merely because they occur in the example config.

## Startup, bytecode and path alternatives

The companion `STARTUP_IMPORT_REVIEW.md` supplies independent source-line evidence and static observations. Key consequences:

- `-I -B` does not disable `site`, `.pth` processing, or `sitecustomize`. The unchanged venv config says `include-system-site-packages=false`. The venv `.pth` imports nonstdlib `_distutils_hack`, which installs a meta-path finder. Its source/bytecode is inside the captured venv tree. The system-site `.pth` is a conservative whole-tree member, not source-predicted active under that venv setting.
- Installed `site.py` prefers `env/bin/pyvenv.cfg` if present. It is absent now but lies outside the current three roots and current required-file list. Guard its absence or bind any separately reviewed replacement.
- Installed Homebrew `sitecustomize.py` rewrites base-prefix/path aliases and conditionally adds the `python-tk@3.11/libexec` and `python-gdbm@3.11/libexec` directories. Those opt trees/libexec names are absent in this read. Root must retain explicit absence or review/capture their actual closure before admission.
- Source and normal/opt-1 `.pyc` are distinct import alternatives. `-B` suppresses writes, not reads. Actual whole-tree bytes and actual import origins/profile must be established later. Pinned cached bytecode is a runtime premise; text review is not proof of its equivalence to the displayed source.

The report does not prove an arbitrary future Python process hermetic. The fixed environment, captured science, installed startup branch, complete selected-support bytes, named load bindings, relevant absence constraints, trusted host-loader boundary and future actual root qualification jointly define the bounded candidate to be reviewed.

## Evidence and remaining limits

Primary static artifacts are the complete `otool -L/-l` records, `STATIC_LOAD_COMMAND_CANDIDATES.json`, `STATIC_NAMED_PATH_OBSERVATIONS.json`, `_hashlib` undefined symbols, selected libcrypto strings, the read-only config copy and independent startup review. The graph records all inspected library edges; the path observations are finite candidate metadata, not executable runtime inventory or acceptance.

Root still owns fresh actual platform/runtime identity, any cache qualification or trust decision, exact normal/optimized profiles, source successor review, execution admission, actual controls, endpoint scientific checks and custody. No thresholds or scientific acceptance conditions are changed by this review. No historical success is supplied as changed-target qualification.
