# RI122 OpenSSL configuration closure correction

Author: /root/ri117_t1_lemma, author of the runtime capture.
Status: corrected source-only candidate, pending independent complete review.
This is not an independent review of my own capture, execution admission,
runtime qualification, measured startup trace or a scientific result.

## Finding and bounded repair

The earlier runtime inventory pinned libcrypto but omitted its default
configuration, which is relevant to the actual hashlib import path. The old
blanket exclusion of configuration-triggered provider behavior was therefore
too broad for this workload. Root preserved the superseded candidate and
associated review/callers before repair. PRE_CONFIG_REVIEW_PRESERVATION.json
binds the preserved originals; none was silently rewritten in place there.

The correction adds exactly two files and two directory-membership records:

| Added file | Bytes | SHA256 |
| --- | ---: | --- |
| /opt/homebrew/etc/openssl@3/openssl.cnf | 12,324 | f6045e326b439e8ee31d4efd020ddf660d616c67d03e0e8e7a927eb14cbb5d1f |
| /opt/homebrew/Cellar/openssl@3/3.6.0/lib/ossl-modules/legacy.dylib | 148,976 | eeb20f1e97dc03a19f17fe8924035ae65e7823f0f1bc915c2021574207f9d5f9 |

Both files have no literal symlinks in their current component-resolution chain.
The exact parent directories are additionally recorded, with no recursive
capture of certificates, private material, utilities or engine files.

The provider module's static image/dependency row is added. Its only observed
loads are already-pinned Cellar libcrypto and trusted Apple libSystem. All
2,986 prior file identities, classifications and provenance strings remain
unchanged, as do all 256 prior directory records and 40 absence constraints.
Roles are resequenced over unique sorted literal paths. The historical
reconciliation manifest remains byte-identical.

## Source-level correspondence

These short findings are source attribution, not claims to have executed or
formally matched the installed binaries against an upstream build.

- [CPython3.14.0 _hashopenssl.c](https://raw.githubusercontent.com/python/cpython/v3.14.0/Modules/_hashopenssl.c):
  its OpenSSL3 branch uses default-context digest fetching; module setup also
  enumerates provider-supplied digests. Relevant locations are lines51–54,
  1856–1858 and the module execution slots.
- [OpenSSL3.6.0 provider_core.c](https://raw.githubusercontent.com/openssl/openssl/openssl-3.6.0/crypto/provider_core.c):
  default-context provider enumeration requests configuration loading before
  activating fallbacks; see lines1429–1441.
- [OpenSSL3.6.0 provider_predefined.c](https://raw.githubusercontent.com/openssl/openssl/openssl-3.6.0/crypto/provider_predefined.c):
  the predefined table identifies the default provider as a builtin fallback,
  with its initialization function already in libcrypto; see lines17–27.
- [OpenSSL3.6 initialization documentation](https://docs.openssl.org/3.6/man3/OPENSSL_init_crypto/):
  configuration loading is the default initialization behavior; suppressing
  loading is a separate nondefault choice. The fixed caller introduces no such
  suppression or new environment override.

No upstream source file was copied into this packet or executed. Derived
descriptions here are deliberately short, with no long quotations.

## Complete local configuration review

All390 lines of the installed configuration were read in af8e5e and252f10.
Installed OpenSSL headers declare version3.6.0. Static libcrypto strings name:

- OPENSSLDIR: /opt/homebrew/etc/openssl@3;
- MODULESDIR: /opt/homebrew/Cellar/openssl@3/3.6.0/lib/ossl-modules;
- ENGINESDIR: /opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3.

The only active loader-routing directives occur at lines17,54,58:

    openssl_conf = openssl_init
    providers = provider_sect
    default = default_sect

There is no active .include, external module path, explicit provider activation,
engine section, algorithm section or external OID file directive. The example
FIPS include and activate entry are comments. Non-initialization CA/request/TSA/
CMP example sections do not authorize this hashing workload to perform their
operations. No such operation was executed during this work.

The default provider is thus supported by the already-pinned libcrypto under
the reviewed static source/configuration correspondence. Its builtin path is
not replaced with an invented external default.dylib. The installed provider
directory has exactly one entry, legacy.dylib; pinning that small complete
namespace is conservative custody, not a claim of legacy activation.

The exact five-key launch environment must remain fixed. It excludes
OPENSSL_CONF, OPENSSL_CONF_INCLUDE, OPENSSL_MODULES and OPENSSL_ENGINES.
Consequently no extra configuration, include or provider path is supplied
through those variables. This is an environment contract, not a live
environment trace.

## Explicit exclusions

The captured config-directory membership records the names of backup config
files, CT-log files, certificate/private directories, misc utilities and the
cert.pem link. Their contents are not claimed captured as hashing dependencies.
There is no active include that reaches a backup, CT-log file or other config.
The fixed hashing work requests neither engines nor TLS/CA/CT-log operations.

Engine directory names and provider paths observed during read-only discovery
do not automatically become loaded inputs. Engine binaries, certificate data
and private material are excluded on the fixed source/configuration basis.
They are not treated as trusted OS components. If configuration, launch
environment or workload changes, this bounded closure must be reviewed again.

## External bootstrap custody remains load-bearing

hashlib is imported before the caller's in-process manifest checks. Therefore
those checks cannot retroactively authenticate the code and configuration
already used to initialize them. Before any future Python launch, the root
owner must independently authenticate the exact pinned interpreter/app/framework,
stdlib/caches/extensions, crypto/config/provider surface, namespace, host
premises and fixed environment through external custody checks.

In-process pre/admission/final snapshots remain valuable drift observations.
They do not establish bootstrap authenticity by themselves, do not constitute
a sandbox, and do not prove absence of changes between observations. This repair
does not introduce a new wrapper, harness, OpenSSL flag, environment variable or
runtime probe to hide that boundary.

## Final reconciliation and counts

The corrected RUNTIME_CLOSURE.json is 2,862,854 bytes, SHA256:

35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920

Its actual recounted inventory is:

- 2,988 distinct literal file identities, 103,009,117 literal-file bytes;
- 258 directory records, 3,526 entry names/types;
- 40 unchanged absence constraints;
- 81 initial images and87 resolved static images;
- eleven Apple system dependency names under the unchanged host premise.

Metadata-only check795fe3 rehashed every current file, checked every current
directory and absence, proved all prior captured entries unchanged, and verified
the historical manifest still matches its accepted2,170,307-byte
b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c pin.
Check880098 independently re-read all87 static image load-command rows,
confirmed all non-system dependency literals are protected, and reconciled
system source-image lists. No unresolved static dependency was found.

No OpenSSL executable, Python interpreter, caller, producer, auditor, extension
or provider was invoked/imported/parsed as code/compiled during this correction.
Only metadata, opaque file bytes, installed text and primary upstream source
were inspected. This record carries no execution or scientific authority.

