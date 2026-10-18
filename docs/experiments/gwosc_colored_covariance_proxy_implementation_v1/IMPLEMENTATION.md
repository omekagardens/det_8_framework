# RI-87 — exact colored-proxy consumer, source-only implementation

25 September 2026 UTC. **Prospective source packet. No qualification or saved
application has run.** This implements the independently accepted
[RI-86 design](../gwosc_colored_covariance_proxy_v1/DESIGN.md), 32470 bytes,
SHA-256 `2a00cac0017f0b749ed958efef4d623143c97e33ba36c60454a65ef9069dc04e`.
The coordinator owns later source adjudication, execution freezes, genuine
reports, publication and git operations. This packet contains only
`consumer.py`, `validate_result.py`, `qualify.py` and this note. There is no
`QUALIFICATION.json` or `RESULT.json` to imply an execution outcome.

## Scientific implementation

`consumer.py` is a stdlib-only pure library. It maps the complete retained mean
PSD of each fixed H1/L1 left/right side to a separate postulated finite
circulant model. Binary64 values retain their canonical hex spelling and raw
little-endian identity; numerical operations convert each to an exact dyadic
Fraction without decimal conversion or a floating multiplication by fs.
Signed zeros keep their original source bytes and both mean rational zero.

At M=16384 and fs=4096, endpoint eigenvalues are fs times the endpoint PSD;
interior eigenvalues are fs/2 times the interior PSD and are mirrored in the
implicit full spectrum. The non-DC minimum and maximum include every index
1..8192, with Nyquist's distinct normalization. Every tied index is retained.
The inherited exact finite-filter theorem gives A1=0, so the DC mode is omitted
only from these extrema and the output covariance action. DC is retained in
full spectral rank and the exact integrated power `q_proxy=(1/4)sum(p)`.

The projected RI-73 certificate retains G,H,LDL factors/pivots/reconstruction,V,
delta,gamma,rho and the unchanged unit-white source model label. Exact local
checks establish G symmetry, nonnegative symmetric H, positive pivots, exact
LDL reconstruction, both inverse identities, delta and gamma row-sum identities,
and rho=delta*gamma with 0<=rho<=10^-12<1. The accepted prior coefficient
interval proof connects this G/H to the held actual operator. These local
checks do not reconstruct coefficients or rerun the predecessor's 92 gates.

For each scenario the source returns both complete rational matrices

```text
Lower = ell*(1-rho)*G,
Upper = u*(1+rho)*G,
Lower <= Omega_proxy <= Upper.
```

The complete output also retains all 8192 one-sided non-DC eigenvalues, both
endpoints, exact integrated power and its difference from the saved rounded q,
all extrema/ties, spectral counts, output rank status and upper bound, eight
diagonal pairs and a trace pair. The full original 8193-bin PSD record is
retained alongside them. A separate upper/lower display is not a computed
Omega, and matrix inequalities are not off-diagonal scalar confidence bounds.

Positive ell establishes output rank eight. Zero u establishes rank zero even
with positive DC. Otherwise zero ell leaves rank unresolved, subject to the
exact upper bound from the count of positive non-DC real modes. Singular K can
still give full output rank. No ridge, floor, dropped row, eigenvalue tolerance,
pseudoinverse, observed residual or statistical score is supplied.

The pure algebra helper also admits exactly the design's M=4,fs=4,dimension1/2
fixture domain. Its rho<1 mathematical domain permits the design's deliberately
weaker rho=1/4 fixture. The application path fixes M=16384,fs=4096,dimension8
and requires the inherited rho<=10^-12 gate. A weaker fixture certificate is
explicitly refused as an application certificate; it is not an alternative
runtime setting for the application.

## Captured-call interfaces and input admission

`build_scenario(psd, fs, G, rho, application=False)` returns exact internal
Fractions and tuples. `decode_psd` checks the complete dtype, length, canonical
finite float-hex values, nonnegativity and reconstructed byte SHA. It accepts
only three bins for the tiny fixture or 8193 for production-shaped inputs.
Rational strings use RI-73's reduced lowercase hexadecimal numerator and
positive denominator, with canonical zero `['0','1']`. Every parsed or derived
rational is subject to the unchanged 262144-bit numerator/denominator bound.
This is a finite resource bound, not a numerical tolerance.

`admit_spectra(report)` checks the fixed RI-83 schema, complete method/grid,
original side selection, both detector orders, all inherited indices and
units. It reconstructs the complete published RI-37 metadata report from the
retained input metadata and verifies its exact 31096-byte SHA-256 identity.
This closes the full nested flags, blank Yunits and other metadata without
opening HDF5. All segment index/flag rows are checked. In particular, expected
L1 injection mask 23 and clear `NO_CW_HW_INJ` remain attached to both scenarios.
Only original `mean_psd` records are numerically consumed; reference spectra,
ASD, individual segment spectral values and signal means are not substitutes.

`admit_ri73(report)` requires the unchanged actual fixed-operator status, model,
lengths/rows, complete ordered 92-gate inventory and all passed flags. Its
expected inventory and complete source-dependency table are transcribed from
held checker source, not inferred by reading an observed numerical report.
The unique `integration:gram` detail supplies the certificate; its exact
matrix/scalar checks occur locally. Checker/dependency pins and runtime metadata
remain bound to the accepted predecessor. Whole-result identities and the
external acceptance chain close the historical report; a fabricated report
with matching metadata does not by itself establish that history.

`build_result(ri83obj, ri73obj, provenance, phase='fabricated_qualification')`
is a pure assembler for qualification and a captured actual caller. It cannot
establish external observation custody. Its default phase clearly labels
fabricated schema tests. `run_saved(ri83body,ri73body,provenance)` is the sole
actual scientific entry point: it verifies **both complete published byte
identities before parsing either body**, applies the full fixed admission and
assembler, and rechecks those immutable byte bodies after calculation. It
performs no filesystem access and cannot authorize itself.

The actual input identities are fixed by the design:

| Input | Bytes | SHA-256 |
|---|---:|---|
| RI-83 `gwosc_off_event_spectra_result_v1/RESULT.json` | 38952074 | `e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f` |
| RI-73 `gwosc_noise_operator_covariance_v1/RESULT.json` | 11180937 | `3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe` |

No source preparation reads either report's numerical values. Future qualification
uses the published `gwosc_input_qualification_v1/INPUT_REPORT.json` metadata
only, whose pin is `31096/a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80`.
All production-shaped qualification arrays and certificates are independently
authored fabrication. Their body pins must differ from the actual input pins;
the outer phase stays fabricated and its qualification acceptance pin is null.
A full-shaped fake report must never be published as an actual saved application.

## Closed result and independent consumer

The closed schema is `ri86-colored-proxy-envelope-v1`. Its header fixes phase,
model, dimensions, fs/df, scenario/row order and the complete limitations. Four
ordered scenarios retain source JSON pointers, complete original PSD records,
rounded-q strings, exact derived results and fixed metadata context. A unique
projected certificate and seven ordered completed application gates are
retained. Every exact number uses the same canonical rational encoding; binary64
source numbers remain their original hex strings. Canonical output is sorted
indent-two ASCII JSON with one final newline, without mode/path/time fields.

`validate_result.py` imports no producer or numerical package. Its
`validate_result(report, expected_phase=None)` independently checks every
nested key/type/shape and literal context, reconstructs little-endian source
bytes, calculates all 8193 PSD dyadics, mappings, extrema/ties, ranks, 64 entries
of each envelope, diagonal/trace pairs and q difference. It verifies the held
LDL reconstruction directly and both exact inverse products, separately from
the producer's LDL calculation. It accepts no producer boolean in place of an
algebraic check. `load_result` also rejects duplicate keys, decimal/nonfinite
scientific literals, and noncanonical serialization.

The provenance schema contains exact pins for all four implementation files
plus the design, both scientific inputs, RI-83/73/86 acceptance and the later
qualification acceptance, and the complete runtime inventory/fingerprint and
interpreter. Internal pin syntax or equality is not external custody proof.
The future caller must bind these entries to independently frozen records,
actual retained byte snapshots, named interpreter and source closure. The
runtime fingerprint pin is the canonical-byte identity of the complete
qualified runtime dictionary; it must equal that in the held RI-73 report.
The consumer checks this equality. The external gate independently compares
a fresh qualified runtime probe and its full byte/build inventory.

The validator's `expected_phase='fixed_saved_application'` refuses fabricated
output. The fabricated phase requires a null qualification acceptance pin;
the actual phase requires a non-null admitted pin. Different source/runtime,
input/acceptance or output paths cannot be legitimized by rewriting the report's
provenance fields: the caller compares them with the frozen manifest.

## Independent qualification source

`qualify.py` supplies a direct four-point real-cosine table and independent dense
Fraction matrix products. Its expected small matrices never call the primary
mapping/envelope routine. The seven fixed families cover white normalization
at unit and 2^-140 variance, a genuinely colored covariance and its two oriented
cross terms, DC changes/cancellation, Nyquist/interior-only rank counterexamples,
crop congruence, the weaker nonzero-rho algebraic certificate, and common scale
four. The oracle checks exact principal minors/ranks and the declared support
in the tiny singular example; it does not simulate noise or use numerical
trigonometry.

The qualification API is `run(consumer, validator, input_report, provenance)`.
It receives already captured producer/validator modules, pinned RI-37 metadata
and explicit fabricated provenance. `fabricated_runtime()` and
`fabricate_inputs(consumer, input_report)` prepare clearly marked schema fixtures
inside the admitted qualification worker. Their fabricated runtime fingerprint
is a fixture operand, not actual process/build evidence; the outer worker must
separately admit and retain the genuine qualified runtime. No fake runtime pin
may replace that external check. The run builds full-shaped fake RI-83/73 inputs,
checks a complete encoded/decoded result with the independent validator, and
mutates specific fields or calls actual guards to require named failure codes. Controls preserve the method's intended failures: every endpoint
factor, interior pairing, fs normalization, DC/Nyquist selection, ties, cross
terms and singular-rank claims; complete fixed metadata and predecessor gates;
LDL/inverse/error/rho algebra; source/runtime/custody/phase and canonical bytes.
The source records the exact finite inventory and caught reason for each case.
Unused predecessor numerical fields are explicitly labeled placeholders: these
admission-interface fixtures do not claim to pass RI-83's full spectral validator
or reproduce RI-73's operator computation. The qualification report itself must
come from a real admitted run. No catch-all success, fabricated execution receipt,
assertion-only gate or replay of an observed input is part of qualification.

Qualification results must retain the fixture operands, directly computed
matrices, expected/primary values and refusal evidence. The source fixes seven oracle families, twelve tiny primary comparisons, four
independently expected production-shaped scenarios and 106 named refusals:
seven decoder, eleven certificate, five algebra, twelve wrong-formula, thirteen
serialization/binding, thirty-four metadata/prior-admission and twenty-four
full-schema controls. The complete inventory/count is retained with the final
source handoff and must be checked from actual normal/-O reports. Source inspection is not a claim that those cases
have run or that the execution limits have passed.

## Required next execution preparation

The source-only stage ends with source/API/mathematical review, final pins and
an exact copy of the four-file packet. It must not be represented as qualified.
The next external preparation uses the existing reviewed supervisor and runtime
admission with only the concrete phase/source/argument/output adapters required
by this packet. No new general harness, scientific tolerance or method option
is needed.

Before any launch the coordinator reviews and freezes:

1. All four implementation sources, the accepted design, RI-37 metadata source,
   complete relevant RI-83/73 predecessor source/acceptance chains and exact
   copied/original identities. No imported local source can remain unbound.
   Qualification must not open the two actual scientific result bodies; their
   hashes may be checked as historical input anchors without parsing values.
2. The existing recovered CPython 3.11.6 named interpreter symlink chain, resolved
   target bytes and unchanged admitted runtime inventory/full fingerprint,
   including NumPy 2.1.3, SciPy 1.14.1, h5py 3.12.1, HDF5 1.12.2 and NumPy build
   configuration. A new environment or install is outside this packet. The
   consumer/oracle/validator require only stdlib arithmetic and serialization;
   a runtime admission probe is separate from scientific calculation.
3. Exact serial normal and optimized commands with -I -B, one worker, explicit
   macOS environment including fresh durable TMPDIR, absolute copied-source
   paths, and exclusive stdout/stderr/result/receipt destinations. The reviewed
   supervisor keeps wall180s, sampledRSS524288KiB, targetpoll0.025s,
   maximumsamplegap0.1s and pstimeout0.05s, including final-gap/failure evidence.
   Sampled RSS is not an OS hard allocation cap. Keep real failures; no automatic
   retry, modified limit or invented receipt follows from refusal.
4. Genuine normal/-O qualification execution and independent complete saved
   evidence adjudication. Only then may a distinct saved-result application
   freeze bind both exact RI-83/73 snapshots, admitted acceptance records and
   actual provenance, parse values, call `run_saved`, and validate its complete
   output. Both application scientific byte streams must be identical; their
   execution receipts remain separate. Reopen source/input/runtime identities
   and independently reconcile every output array and matrix before publication.

This note deliberately provides no runnable unfrozen launch command or fabricated
success report. A source handoff fixes prospective callable interfaces; the
separately reviewed external worker fixes concrete command/path custody. Those
are ordinary coordinator continuation gates within the user's authorization.

## Claim boundary and present verification

This packet keeps empirical finite spectra, postulated finite circulant
covariance, and physically justified/calibrated noise covariance separate. A
passed exact computation would establish the stated conditional envelopes,
not noise adequacy or useful narrowness. DC is omitted by an exact operator
theorem, not because the spectral estimator has no DC. Broad or zero lower
bounds remain recorded outcomes. The whole program continues toward its native
and measurement objectives; no DET prediction, physical gravity test, official
matched-baseline reproduction, confidence level or RET resumption follows.

At source preparation, verification consists only of static syntax/API review,
mathematical reasoning, version-specific primary-source convention review
in RI-86 and source/metadata hash checks. No target module or numerical import,
synthetic case, observed spectrum, raw HDF5 or coefficient reconstruction has
been executed here. Runtime success, exact normal/-O equality, resource outcome,
all-bin/matrix application values and final scientific reports remain unrun.
