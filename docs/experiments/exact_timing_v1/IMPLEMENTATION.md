# RI-35 — exact two-way clock compatibility consumer

24 September 2026 UTC. Standalone implementation of the exact timing target in
the accepted [RI-33 contract](../observer_channel_v1/CONTRACT.md). That document
remains unchanged at SHA-256
`6dc0df2c94747df68f251114d75ba6e568cc69b75f27c8946b680aeac7d54f66`.
This bundle accepts two messages with four timestamped events, optional finite
delay/asymmetry bounds and an explicit precision tolerance. It calculates
conditional compatibility and constructs attaining witnesses from those inputs.

It implements neither native geometry nor a physical clock calibration. No
GWOSC data, uncertain-clock solver, multiexchange fit, Poisson estimator, RET
source, protected evaluation or historical model is used. Supplied model and
calibration references are premises, not independently verified facts.

## 1. Complete executable scope

| File | Purpose |
|---|---|
| [timing.py](timing.py) | Validated exact input types, declaration identity, inference and witnesses. |
| [test_timing.py](test_timing.py) | Independently authored standard-library tests against the agreed contract. |
| [run_checks.py](run_checks.py) | Runs only this test module, or exports the seven deterministic worked fixtures. |
| This document | Interface, replay and claim limits. |

There are no project-package or third-party imports. Python 3.11 is the replay
target. The accepted mathematical proof is over real inputs; this implementation
uses finite exact `fractions.Fraction` inputs and rational outputs.

## 2. Inputs, roles and validation

The Python interface in `timing.py` exposes frozen `Interval`, `Bounds`, `Record`,
`Request`, `Report` and `Witness` dataclasses, plus `fingerprint`, `infer` and
`witness`. Required `Request` declarations include exchange ID, two distinct
clock IDs, common unit, premise reference, clock/uncertainty models, the full
record tuple, optional-bound container and nonnegative precision tolerance.

An admitted timing request explicitly names
`clock_model="shared_unit_rate_constant_offsets"` and
`uncertainty_model="exact"`. The clock premise is
`C_A(t)=t+beta_A`, `C_B(t)=t+beta_B` in one supplied common time parameter.
Separate unit rates relative to each clock's own proper time do not establish it.

Each record retains its ID, exchange, slot, clock, message, unit, role, selection,
reading/status, error declaration and disposition reason. Slots are `A1`, `B2`,
`B3`, `A4`. Only **actual and selected** rows enter inference. Proposed, withheld
and unselected rows stay in the request and identity. A nonempty disposition
reason is required for nonactual, unselected or nonreading rows. An unknown ID
or a matching message string does not authenticate emission, receipt or custody.

`reading` requires an exact value. `missing` and `not_received_by_cutoff` require
no value; the latter is allowed only at receipt slots. This minimal status has
no numeric cutoff and supports an insufficient-record result only. It cannot
establish a quantitative absence duration, nonemission or an infinite horizon.

All rational fields require actual `Fraction` values, including zeros and
errors: floats, integers and booleans are refused. Bounds are ordered; forward
and reverse delay bounds are nonnegative. Tolerance/error are nonnegative.
There are at most 64 records, with unique record IDs. Required strings are
nonempty and at most 128 characters; disposition reasons may be empty only
where allowed above. Numeric request fields have at most 256 bits each in the
reduced numerator and denominator. These limits bound this API, not the proof.

`Interval` itself allows larger exact endpoints so that computed results are
representable. The input bit limit is enforced on the complete `Request` and
again at public entrypoints. Witness targets are exact Fractions with no such
bit limit, so an attaining derived endpoint is not rejected merely for having
grown during exact arithmetic. Frozen objects are an API convention, not a
security boundary against hostile Python execution.

Malformed declarations raise `ValueError`; well-formed unsupported, incomplete
or incompatible requests produce distinct reports. Caller-supplied reasons,
premise IDs and clock/exchange IDs remain declarations. Physical drift or
quantization cannot be detected from four values if falsely labeled exact:
unsupported models or nonzero errors must actually be declared to obtain the
corresponding refusal.

## 3. Deterministic dispositions

After validating the complete request and calculating its identity, inference
applies the following order. This avoids silently choosing a favorable subset.

| Check | Result / reason |
|---|---|
| Unsupported clock model, then nonexact uncertainty model | `unsupported_clock_or_channel_model` / `clock_model` or `uncertainty_model` |
| Repeated effective slot | Unsupported / `ambiguous_slots` |
| Any missing slot or effective nonreading status | `insufficient_records` / `incomplete_exchange` |
| Exchange/clock/message association mismatch | Unsupported / `record_association` |
| Unit mismatch | Unsupported / `unit` |
| Positive error on an effective reading | Unsupported / `nonexact_reading` |
| Negative turnaround, then negative round-trip remainder | `incompatible_given_premises` / `negative_turnaround` or `negative_roundtrip` |
| Empty intersection with the optional bounds | Incompatible / `empty_compatibility` |
| Nonempty exact intersection | `compatible_given_premises` / `exact_projection` |

For the selected four readings, `u=B2-A1`, `v=A4-B3`, `r=B3-B2`.
The base interval for `theta=beta_B-beta_A` is `[-v,u]`, with the optional
intersections proved in RI-33. A compatible report returns interval, midpoint,
half-width and whether that radius is at most the supplied tolerance. This
last field is a deterministic precision condition, not `abs(theta)<=tolerance`,
a confidence level, a calibration certificate or an actuation decision.
All four inference fields are `None` for every noncompatible disposition.

`witness(request, theta)` returns `None` for a noncompatible request or a target
outside its interval. For an admitted target it returns the same input identity,
`beta_A=0`, `beta_B=theta`, shared times `(A1,B2-theta,B3-theta,A4)`, and the
forward/reverse/turnaround durations. These reproduce the supplied readings and
all constraints. The gauge choice is explicit; no hidden simulator state is read.

## 4. Declaration identity

`fingerprint(request)` is a domain/version-separated SHA-256 over canonical
exact JSON. Every supplied field, optional bound, role, reason, selection flag,
nontraining row, tolerance and record-tuple order participates. Reordering rows
may preserve inference but changes declaration identity. Changing an unused
reading must not improve precision, even though it changes that identity.

The digest identifies supplied declarations under SHA-256's usual assumptions.
It does not automatically hash referenced calibration/source files, verify
their truth, authenticate acquisition or prove custody. A caller needing those
properties must retain and independently qualify the external evidence and
its binding manifest. This bundle supplies no report-authentication service.

## 5. Replay and worked fixtures

Use the three Python files from a reviewed checkpoint listed in the
[progress record](../../coordination/REVIEW_PROGRESS.md); the working project's
other modules and environment are not required. From this directory:

```sh
python3 -I -S -B run_checks.py
python3 -I -S -B -O run_checks.py
python3 -I -S -B run_checks.py --worked
```

The launcher adds only its own directory for the bundle imports and disables
bytecode writes. It fails on test failures, an empty suite, skips or expected
failures. `--worked` writes JSON to stdout and no repository file. Fractions
are represented by decimal numerator/denominator strings. The seven cases are
RI-33's supplied readings; they are neither simulations of a native law nor
observed physical data. Compatible cases include lower, midpoint and upper
witnesses, even when these coincide for a singleton interval.

For a clean replay, extract only this directory from the reviewed Git commit
into a temporary directory and invoke that copy with the same flags. Source
identities, actual independent review and run results belong to the progress
record. Generated output is not a new registered research witness collection.

## 6. Remaining work and boundaries

Correlated/uncertain timestamps cannot be replaced by midpoint readings or
independent difference boxes and treated as exact. RI-33's full joint feasible
set and chronology examples remain the requirements for any later solver.
Multi-exchange shared clocks, latent rates, drift and endpoint calibration
would likewise require explicit new scope and premises.

GWOSC qualification and eventual conventional strain reproduction remain a
separate input type and work packet. This exact timing consumer neither acquires
that data nor creates the missing native-to-instrument map. Existing native
proofs, geometry/gravity premises, original review and RET pause remain held.
No scientific release, protected evaluation, hardware acquisition or new QR
successor follows automatically from the software result.
