# Bounded observed GWOSC replay — 20 October 2026

One prospective conventional GWOSC calculation is complete at its declared
scope. Both detectors passed the fixed numerical gates; normal and optimized
execution produced 16 byte-identical scientific output files. An independent
checker confirmed the residual and threshold arithmetic over the stored
outputs. This is evidence for this calculation, with the limits below.

## Inputs, method and acceptance rule

The inputs are the public GW150914 32-second H1 and L1 records, each containing
131,072 samples at 4,096 samples per second. The selected files are
[H1](https://gwosc.org/GW150914data/H-H1_LOSC_4_V2-1126259446-32.hdf5) and
[L1](https://gwosc.org/GW150914data/L-L1_LOSC_4_V2-1126259446-32.hdf5).
Their complete bodies and decoded arrays passed the predeclared identity and
format checks before calculation.

The `NO_CW_HW_INJ` annotation is set for H1 and remains clear throughout L1.
All samples were retained. This run makes no claim that a possible continuous-wave
hardware injection is absent or has negligible effect.

The fixed 17-stage scalar calculation was evaluated in binary64 and against an
80-significant-digit Decimal reference using the same frozen inputs and coefficients. For
each detector, all 131,072 full-record residuals and all 4,096 comparisons with
the retained historical crop were checked. The fixed crop is the zero-based
half-open interval `[65536:69632]` for each detector. The detector-specific tolerance was
fixed before the run:

`tolerance = Decimal80(1e-9) × max(abs(full raw input))`.

There is **no unit floor** in this rule. The reference precision, coefficients,
crop selection and numerical thresholds were unchanged by the transport and
environment repairs. Decimal80 supplies a high-precision comparison; it is not
an interval enclosure or a proof of exact recurrence evaluation.

## Recorded numerical result

Values below are rounded summaries of the retained full-precision results.

| Detector | Maximum primary/reference residual | Maximum primary/historical-crop residual | Fixed tolerance | Historical crop bitwise matches |
| --- | ---: | ---: | ---: | ---: |
| H1 | `3.8468068135232064e-33` | `2.044184676079958e-33` | `7.706262192397465e-28` | `0 / 4,096` |
| L1 | `1.0796810220840996e-32` | `9.810934460719992e-33` | `1.8697138664279764e-27` | `0 / 4,096` |

Every declared sample-level gate passed. The historical crops agree within the
declared numerical tolerance but differ in every binary64 sample. Numerical
agreement does not establish historical bitwise identity or recover historical
custody. The separate normal/optimized comparison concerns the two new runs:
their 16 scientific files agree byte for byte.

## Independent arithmetic scope

The independent checker examined the normal run and represented its stored
binary64 and decimal numbers as exact rational values. Root separately verified
the 16-file byte equality with the optimized run; the arithmetic checker did not
open or adjudicate the optimized run. It checked all **262,144 full-record residuals** and
**8,192 historical-crop residuals**, their declared Decimal80 rounding, maxima,
first maximizing indices, detector-specific thresholds and every threshold
decision. The exact unrounded comparisons also lie below the exact tolerance.
The checker completed successfully with no stderr; root checked its actual
receipt and output and accepted this bounded arithmetic result.

A separate independent review verified all 36 current output identities, the
16-file cross-mode comparison, decoded-array joins, the new L1 body and retained
reuse evidence. It checked the completed arithmetic evidence without running it
again. Original external runtime, scientific-source and static-input bodies were
joined through the recorded contracts; that pass did not reopen every dependency.

That check did **not** rerun the reference recurrence or independently derive
the processing model. Its conclusion is consistency of residual arithmetic
with the stored values. It does not prove universal implementation correctness,
independent reproduction from this public edition, or accuracy for other data.

## Transport, environment and preserved failures

The original H1 acquisition failed on an absent Content-Type header. A later,
explicitly authorized H1-only exception admitted the exact pinned H1 file. L1
then failed on the same absent header because the H1 permission did not cover
L1; the method stopped before consuming L1 body bytes. A separately reviewed
and human-approved L1-only retry used a fresh execution namespace, reused the
accepted H1 and staged environment read-only, and admitted only the exact fixed
L1 body. Both header exceptions remained artifact-specific; expected sizes,
full hashes, TLS, encoding rules and numerical gates were retained.

Intervening preflight failures also remain recorded: runtime identity changed,
and installed NumPy native files did not match their unchanged RECORD. A new
prospective runtime binding and an exact fresh NumPy wheel were reviewed and
admitted; both packages passed complete wheel RECORD and CRC checks. The retained
h5py wheel was reused. No mismatched installed module was accepted and no old
failure was rewritten. The driver changed only its runtime-hash binding; the
scientific kernels and thresholds remained fixed.

## What this result does and does not close

The bounded portable-calculation and independent-residual-check deliverable is
closed. **Production qualification receives zero credit** from this replay;
closed production routes and historical custody failures remain closed. This
conventional calculation supplies no DET-native gravity prediction, physical
validation or demonstrated application-benchmark advantage. The separate
[width diagnostic](WIDTH_DIAGNOSTIC.md) remains ABSTAIN / NOT RUN. The
[observation-channel requirements](OBSERVATION_IDENTIFIABILITY.md), unchanged
GR baseline, Status M and RET pause remain in force.

This public document is a scoped result report. Exact private provenance,
machine/custody metadata, original receipts, administrative scripts and raw
outputs remain local under the
[metadata-obscured publication policy](../../coordination/REDACTED_PUBLICATION.md).
This edition does not claim to supply an executable or independently replayable
custody package. See the [publication note](PUBLICATION_NOTE.md) for the related
synthetic and mathematical results.
