# RI107 — independent RI105 arithmetic consumer, source preparation

26 September 2026. Only this note and audit_saved_certificate.py are
authored by this reviewer. No scientific body, native operand, candidate,
prefix/helper, producer, auditor, fixture or qualification target has been
read for arithmetic, imported, compiled or executed in this preparation.
No candidate, descriptor, authorization, active freeze or receipt is
created. No repository or git mutation is performed. Source-only review
and metadata hashes are not an executed arithmetic result.

## 1. Accepted interface and fixed scope

This implements the accepted 646-line RI105 AUDIT_CONTRACT.md:
33257 bytes, SHA-256
28d516a20457f45accd7d5f30fae9c56f08f425156e99ef177478dfd64a1f213.

The accepted producer is RI105 check.py:
34820 bytes, SHA-256
6ff26aef5214ebcbdf13adc62dacdf33ba615769e2e64f3a39cf44368310655e.
Its IMPLEMENTATION.md is 20203 bytes, SHA-256
7108bdc0d6b0f4dcc9da2acdbea647f1eddea71db1b11529eef780f2e52a8e04.

The constructor uses only the six C3/C4/H5 complete rows at records 0 and
1, totaling 32 rational probabilities, from the accepted RI88 body:
1828149 bytes, SHA-256
ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b.
Only those lists are converted to rational operands. The other held row
metadata are inspected solely to locate and verify the selected inventory;
other probabilities remain authenticated unconverted strings. H and z
values are not inspected. There is no deletion-factor inventory, q6/q7
table, new record, amplitude choice, global M6/M7 or actual scale.

The raw accepted proof inputs are RI103 REPAIR.md, 20198 bytes,
SHA-256 8a2a4bf9142341e2511763cbfd799183860e907372d577b9b32d8c1cf24a955c,
and RI94 AMPLITUDE.md, 25150 bytes,
SHA-256 65645454993a81b70a0d9cd278eb137cd6b218055b1cb026f9950b7cb8895844.
They are authenticated before any scientific JSON parsing and are not
parsed for numerical coefficients. Their mathematics remains an inherited
premise; source identity alone does not accept that mathematics.

## 2. Separately written arithmetic

There is no fractions.Fraction dependency and no imported/copied producer,
prefix, checker, solver or supervisor implementation. Fixed interface
names, source identities and fixture/control declarations are necessarily
shared data. The author read the producer; independence is not blind
authorship.

Rationals are normalized integer pairs (n,d), d positive, gcd(|n|,d)=1.
Zero is exactly (0,1). Exact types reject booleans. Addition factors the
common denominator gcd; multiplication cross-cancels before integer
products; division uses the normalized reciprocal and checked products.
Ordering comparisons check bounded integer cross-products. Powers have
fixed integer exponents at most eight. Equality of normalized pairs is
structural, without a new unbounded arithmetic path.

The E and K summands use a quotient-first arrangement: A*(G/B)^3 and
A^3*(G/B)^6/B^2, respectively. v is H*(H/C)^2. This independently written
grouping differs from the producer's power/multiply/divide sequence while
retaining the accepted exact formulas. Every term, cap total and sum is
rebuilt; no candidate coefficient is read as a construction input.

Polynomials are sparse exponent-to-pair maps, with actual integer exponents
0 through 4. Zero coefficients are omitted internally. Euclidean division
uses sparse leading monomial cancellation; every result is independently
checked by denominator times quotient plus remainder. The remainder degree
must drop. The native root polynomial has degree at most three; its linear
coefficient is checked nonzero. A four-entry padded contrast and five-entry
padded U vectors remain distinct from trimmed evidence polynomials.

P is built directly from the differences of E,j,v,K. Separately subtracting
the two padded U vectors must give [0]+P. E is positive, R is reconstructed
as 1/[2(1+max(E0,E1))], and both margins 1-R E exceed 1/2 exactly.

The gcd is made monic; the square-free quotient retains its original
scale. A second Euclidean trace confirms coprimality. Sturm members use
unscaled negative exact remainders, including the final zero remainder in
the division evidence but not in the chain. No monic rescaling of chain
members is allowed. Endpoint values are direct sums of coefficient times
endpoint powers, not the producer's Horner loop. Zero signs are deleted
before counting variations, so V(0)-V(R) counts distinct roots in (0,R].
All traces, values, signs and variations are independently rebuilt.

There are only two native outcomes: no real roots certifies the prescribed
record contrast and rejects the specified RI103 27-child repair; surviving
real roots leave the question unresolved. No rational-root calculation or
root approximation is performed. In particular, surviving irrational
roots are not dismissed and no root is substituted for the actual scale.

## 3. Entire canonical saved body

The expected certificate has exactly the producer's sixteen top-level
sections, with every nested key, exact type, ordered list and scalar:
schema, accepted_inputs, accepted_sources, inputs, selected_parent,
records, scale_domain, contrast, root_certificate, decision, coverage,
limitations, arithmetic_limits, checker_sha256, fixtures, refusal_controls.

The auditor first reconstructs the whole expected object from accepted
operands and its own arithmetic. It then recursively compares every field
and serializes that expected object as sorted-key compact ASCII JSON,
exactly one terminal newline. The complete reconstructed body must equal
both the candidate and separately pinned genuine witness stdout bytes.
Extra/missing fields, boolean/integer aliases, list reorderings, altered
signs/traces/claims, extra whitespace or semantically equivalent alternate
fraction strings are not accepted.

All sixteen synthetic polynomials and full root certificates are rebuilt,
including the common-zero endpoint trap, repeated roots, excluded zero,
included R, constant and negative-leading cases, irrational positive root
and nonunit radius. Each retains native_model_claimed=false. Mechanical
fixture decision flags are not native conclusions.

All seventy ordered producer name/reason pairs are reproduced as static
interface declarations and checked for exact inventory/uniqueness. The
auditor does not execute those producer mutations and does not claim
independent control qualification. Actual producer control execution
remains part of separately accepted witness/replay custody. No additional
native or synthetic fixture domain is introduced by this source packet.

## 4. Closed future descriptor and source custody

The sole future CLI is:

    /opt/homebrew/bin/python3 -I -S -B /ABS/audit_saved_certificate.py /ABS/DESCRIPTOR.json BYTES SHA256

The concrete absolute paths and descriptor identity remain unissued.
Only a separately admitted invocation may supply them. No data, radius,
polynomial, record, fixture or output override exists.

The descriptor has exactly schema, phase, files, accepted_sources,
audit_source and custody_dependencies. Schema is
ri105-independent-audit-input-v1 and phase is
fixed_saved_certificate_audit. It is authenticated before parsing.

- files has exactly ri88, ri103, ri94, candidate.
- accepted_sources has exactly ri103, ri94, checker, protocol, contract.
- audit_source is one source entry matching the absolute executing source
  path and the future root-pinned complete consumer bytes.
- custody_dependencies is exactly the ordered five-entry list:
  producer_witness_stdout, producer_witness_custody,
  producer_normal_custody, producer_optimized_custody,
  consumer_source_review.

Each file/source entry has exactly path, bytes, sha256; custody entries add
exactly role. Paths are normalized absolute literals, with symlink-free
regular-file validation when opened. Byte counts are positive actual
integers bounded by 8 MiB, and hashes lowercase 64-digit hexadecimal.
All fixed input and accepted-source pins are hardcoded, not merely trusted
from the descriptor. The candidate, genuine producer stdout, custody and
future auditor identity must be concrete admitted values, not placeholders.

The two proof objects in accepted_sources exactly alias the corresponding
files objects, including paths and pins. No other payload aliases are
allowed. The 15 bindings therefore reference exactly 13 unique payload
paths, all distinct from the descriptor. Candidate and genuine stdout are
distinct files with equal pins and equal entire bodies. No own successful
output or own execution receipt is a descriptor prerequisite.

The executing source is first independently captured before any descriptor
read or validation, including malformed CLI path/count/hash and flag
checks. An invalid descriptor entry is not opened merely for a postcheck;
the failure report marks whether that descriptor read was admitted while
retaining its own-source check. This observed identity is not self-authorization: a
valid descriptor must subsequently match it exactly and be independently
admitted by the caller. A malformed or missing descriptor therefore does
not omit before/after custody of the known source.

Every unique payload is captured before scientific JSON parsing. Each read
compares literal resolved path, lstat, open/fstat, final fstat/lstat and
device/inode/size/mtime/ctime, complete length and SHA. The final component
is opened O_NOFOLLOW. Every associated role binding is separately checked
against the captured bytes.

The source catches an arithmetic/comparison failure only to perform final
custody checks. It independently attempts all thirteen unique payload
checks and the descriptor, even if another check fails; no boolean
short-circuit skips later inputs. The own source is one of these payloads.
Uncaptured or changed inputs prevent success. Late signal/resource failure
also invalidates success. Failure diagnostics use a separate bounded stderr
serializer, with 2048-character text fields and at most fourteen postcheck
records, rather than reapplying an already-exhausted normal budget and
discarding those checks. This is not a successful arithmetic fallback or
a relaxed execution envelope. External monitoring may terminate the process
before cleanup completes, so the source does not guarantee that every
failure emits a final report.

The consumer checks custody file identities, not their semantic acceptance.
The separately reviewed caller/coordinator must authenticate actual
producer witness/normal/optimized statuses and genuine outer completions,
actual zero exits, role-order-versus-role-set semantics, raw monitoring,
cleanup and before/after identities. Arbitrary bytes with correct hashes
do not self-authorize the auditor.

## 5. Report, bounds and failure behavior

A successful audit report embeds the complete reconstructed certificate,
all sixteen section byte identities and the whole identity, descriptor,
auditor and accepted-source identities, all fifteen role bindings,
fourteen completed postchecks, the independent operation count and the
restricted scientific disposition inside the reconstructed certificate.
It explicitly separates rebuilt fixtures, declared-only producer controls,
accepted premises and custody semantics that remain external.

Exact input rationals are capped at 32768 numerator/denominator bits,
working reduced pairs at 1048576 bits and transient integers at 2097154.
Rational arithmetic and ordering operations pass a 200000-operation
counter; this independent implementation's count need not equal the
producer's. Integer-gcd machine steps and structural equality/index tests
are not counted as primitive rational operations. All computed values
remain checked, with exact bounded degrees and loop lengths.

Input rational/JSON integer text is capped at 20000 characters; each file,
descriptor, canonical candidate and emitted report is capped at 8388608
bytes. The report embeds a candidate plus metadata and therefore may hit
the output cap even if that candidate alone fits; this is a failure, not
permission to enlarge the cap or omit evidence. No runtime-success estimate
is made from source inspection.

The internal elapsed-time/RSS checks use 120 seconds and 536870912 bytes.
The alarm stays active through serialization, output flush and the last
budget check. A late nonzero exit invalidates any bytes already printed.
No file is written. The external caller captures stdout/stderr and retains
failures without automatic retry, different data or relaxed limits.

The separately admitted caller retains ENV5:
PATH=/usr/bin:/bin, LANG=C, LC_ALL=C, TZ=UTC,
__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0; actual interpreter flags must include
-I -S -B. It binds interpreter/monitor byte and symlink identities, exact
cwd/argv, owned-group sampled RSS, the 120-second/512-MiB envelope, 50-ms
waits and monitor calls capped by min(250ms, remaining deadline).
Sampling is not a hard allocator limit or uninterrupted process census.
An optimized run is a separate future authorization, not this source task.

## 6. Remaining gates

The first complete source draft had two source-review findings, both
corrected without execution: its failure serializer reapplied the exhausted
normal budget before printing retained diagnostics, and its own-source
capture occurred too late to cover malformed descriptors. A subsequent
review also moved the remaining early CLI entry validation behind that
capture, preserving source custody even for bad descriptor arguments. Their corrected
paths are described above. They were source defects, not executed failed
arithmetic or qualification attempts; no historical evidence is rewritten.

The source and this note require complete independent reading, exact
source pins and explicit root source acceptance. None of the arithmetic,
fixtures, guards or custody paths is claimed to have run or passed.
No compile/import or native operand decoding is part of this preparation.

The real candidate and accepted three-mode producer custody do not exist
for this source task. Root must obtain and accept them, prepare the exact
descriptor, review/qualify or explicitly accept the precise caller
carry-forward, freeze ordered concrete inputs and issue fresh authorization.
Only then can one attempt run. Genuine outer completion, complete saved
streams and resource/identity evidence must be independently reconciled
before mathematical adjudication.

RI103/RI94 accepted formulas remain theorems assumed by this arithmetic
audit. Even successful root exclusion rejects only the specified private-
full 27-child repair, not every positive extension, all-size geometry,
QM, mass/gravity or DET ontology. RET and unrelated work remain untouched.
