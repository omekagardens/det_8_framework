# Bounded D4-A envelope admission component

21 October 2026. Implements a deliberately narrower profile of
[ENVELOPE_ADMISSION.md](ENVELOPE_ADMISSION.md). **Operational ABSTAIN / NOT RUN.**
No actual native endpoints, endpoint producer, accepted scientific review,
sampler, observation, experiment or diagnostic result is supplied. The frozen
exact and approximate protocols and the existing envelope constructor are
unchanged.

The [adapter](../../../det8/models/envelope_admission.py) supports one static
comparison containing both B and Q rows for the fixed labelled D4-A parent,
under **approximate certificate A only**. Other protocol choices, adaptive rows,
conditional laws, label remappings and other parents are refused. Missing
run-only premises do not block this component review; every result's
`operational_admission` remains `ABSTAIN`.

## Caller trust boundary and usage

```python
from det8.models.envelope_admission import admit_d4a_envelope

result = admit_d4a_envelope(
    descriptor_bytes,       # plain bytes, bounded UTF-8 JSON
    comparison_bytes,       # independently supplied frozen comparison bytes
    reference_bytes,        # plain dict: required role -> exact plain bytes
    trusted_review_applicable=False,
)
```

The default cannot invoke the certificate factory. A trusted caller may set
`trusted_review_applicable=True` **only as its separate assertion that an
independent scientific review applies to these exact target, ordered outcome
row, endpoint arrays, coverage, selection, risk and reference bytes**. This is
neither a UI permission nor a test of reviewer authenticity. The module does
not establish that the caller is trusted. An untrusted producer must not control
this argument. Names, matching hashes, claim strings and successful arithmetic
cannot supply the assertion. Ordinary frozen records are not credentials.

That review must establish the actual unconditional joint-probability meaning,
original law/z/normalization and parent embedding, complete simultaneous
enclosures, correct enclosure arithmetic and applicable confidence/selection
assumptions with justified risks. The adapter verifies byte identity and declared
scope, not the truth of these claims or independence/history of the review.

The [synthetic tests](../../../det8/tests/test_envelope_admission.py) contain an
invented serialization fixture. Their `True` argument simulates the trusted
boundary to test control flow; no fixture receives scientific acceptance.

## Closed profile

Every listed object has exactly its listed fields; no optional/default fields,
duplicate keys, unknown fields, floats, booleans, nulls or implicit conversions
are accepted. Arrays retain their original order.

| Object | Exact fields and content |
| --- | --- |
| Descriptor | `schema="d4a-full-row-envelope-v1"`, `comparison_sha256`, `target`, `outcome_dictionary`, `arms`, `review_scope_sha256` |
| Comparison | `schema="d4a-frozen-comparison-v1"`, `protocol="approximate-certificate-A"`, `selection="pre-held-out-fixed-comparison"`, `target`, `references`, `budgets` |
| Target | Exact structure returned by `canonical_d4a_target()`, including labels, all strict relations, zero old bits, mask convention, sector, original law/normalization, lambda=1, epsilon=1/4, z1=1, score and reference roles |
| Outcome dictionary | Exact sequence returned by `canonical_d4a_outcomes()`: regenerate order ideals from the fixed relation, then bit 0 followed by 1; masks are `0,1,3,7,15,23,31,39,47,55,63` |
| Arms | Exactly `B` and `Q`; each has `arm`, `endpoints`, `coverage`, `evidence` |
| Endpoints | Exactly 22 objects with `lower` and `upper`, each a reduced `[numerator,positive_denominator]` probability pair |
| Coverage | `mode` is `deterministic` or `statistical`; `scope="simultaneous-full-unconditional-joint-row"`; `selection` matches the comparison; `failure` is an exact rational pair |
| Evidence | For arm `a`, exactly `{"derivation":"a_enclosure","coverage":"a_coverage"}` with `a` replaced by B or Q |
| References | Seven roles: `law_z_normalization`, `parent_embedding`, `B_enclosure`, `Q_enclosure`, `B_coverage`, `Q_coverage`, `independent_review`. Each has `sha256` and the literal `claim` from `REFERENCE_CLAIMS`. The separately supplied byte dictionary has exactly these keys. |
| Budgets | `B`, `Q`, `other_certificate_risk`, `kappa_budget`, `max_intermediate_bits`, `max_work_bits`. Each arm budget has exact rational `proxy`, integer `bit_width` in 0..256, and exact rational `rounding`. |

`comparison_sha256` identifies the exact comparison bytes. Each reference digest
identifies the exact separately supplied bytes. `review_scope_sha256` hashes the
descriptor with that field removed, serialized with Python JSON options
`sort_keys=True, separators=(",", ":"), ensure_ascii=True`, then ASCII encoded.
It names the whole declared target/row/endpoint/coverage/comparison scope and
does not authenticate review. Original descriptor and comparison bytes, all
reference bytes, and original reduced endpoint pairs are retained with a
successful component result; the canonical digest does not replace them.

The deterministic mode in this profile requires a reviewed zero failure bound.
For either coverage mode the exact accounting is
`endpoint_failure_sum = failure_B + failure_Q` and
`total_certificate_risk = endpoint_failure_sum + other_certificate_risk`.
Require `total_certificate_risk <= kappa_budget < 1/20`. Coverage failure stays
in kappa; it is never added to eta. These inequalities check declared numbers,
not their justification, and do not complete certificate A's run conditions.

## Bounds, arithmetic and refusal

Each JSON input is 1..65,536 bytes of UTF-8, with maximum depth 10, 2,048 nodes
(keys count), 64 items per object/array, and 256 characters per string. Each of
the seven opaque reference byte strings is 1..8,192 bytes. A separate combined
ceiling is 196,608 bytes. Integer tokens have at most 78 decimal digits and each
integer magnitude has at most 256 bits. These are finite parser limits; the
byte/depth and integer-token bounds precede JSON tree/arbitrary-size integer
creation. The bounded tree is then checked before rational arithmetic. Plain
bytes/dictionaries only are accepted; paths, callbacks, adapters and subclasses
cannot enter the admission API.

This conservative profile requires declarations of exactly **32,768 intermediate
bits** and **67,108,864 logical work bits** (`2048 * 32768`). Smaller reservations
refuse before rational-array arithmetic or the certificate factory; larger
declarations are outside this fixed profile. With 22 coordinates, 44 endpoint
denominators contribute at most 11,264 bits per arm. The existing factory's
construction reservation is at most 22,537 bits and its budget comparison at
most 22,794. Fair-bit interval sums use at most those denominator products;
the four-term risk/budget arithmetic is smaller. The map accepts only 256-bit
weights and a width at most 256; even a product bound over its 22 rational TV
terms and budget comparison stays below 32,768 bits. The fixed work reservation
covers both arm witness sets and map/adapter arithmetic with slack. This is a
logical integer-magnitude reservation, **not an OS/RSS/time guarantee**; parser
objects, allocator/gcd internals and retained byte storage are separately bounded
inputs but not measured process memory.

Checks require the original box to contain a normalized row. They additionally
intersect each pair of bit intervals and require
`2 sum(max(lower_0,lower_1)) <= 1 <= 2 sum(min(upper_0,upper_1))`, with nonempty
pair intersections. This establishes existence of some normalized nonnegative
equal-bit row, not enclosure of the actual row or strict positivity. The original
arrays are never silently tightened or replaced. An explicit upper zero conflicts
with this positive target and is refused; a lower zero is permitted. No slot is
dropped, including zero proxy weights or zero map-cell counts.

Only after all these checks and the separate trusted decision does the adapter
call `certify_probability_envelope` for each arm, with the original arrays,
explicit proxy allowance and resource reservation. Only a newly factory-produced
`CONDITIONAL_PROXY_CERTIFICATE` is accepted. Its exact weights enter the existing
`CategoricalMap` constructor; its exact rounding TV must meet the predeclared
rounding allowance. No words are mapped and no random bits are obtained.

Success is `COMPONENT_PREMISES_REVIEWED`, with complete original inputs and exact
envelope/map witnesses. Refusal returns the first reason in deterministic check
order, with field and remedy; no partial arm certificate is exposed. Expected
schema/resource/binding/endpoint/review/risk/budget failures return ABSTAIN codes.
Unexpected ordinary exceptions return no usable component; interruptions
propagate without a result and must also be treated as non-admission. There is
no retry. Effect/bias, conditional bit/channel, availability, frozen schedule
and total-cost premises remain explicit operational blockers.

The external isolated author harness ran only the new synthetic test module
against byte-pinned copies of the existing two arithmetic dependencies. The
focused integration command is `python3 -B -m unittest det8.tests.test_envelope_admission -v`.
Exact test receipts and source pins are retained privately under the publication policy.
