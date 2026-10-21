# Exact probability-envelope component

20 October 2026. Deterministic implementation of the conditional construction in
[PROXY_ENVELOPE.md](PROXY_ENVELOPE.md). **Operational status: ABSTAIN / NOT RUN.**
This component computes arithmetic certificates from supplied rational bounds.
It supplies no actual native intervals, interval producer, source/channel
certificate, numerical effect bound, held-out result or physical observation.
The [exact diagnostic](WIDTH_DIAGNOSTIC.md) and [optional approximate
protocol](APPROXIMATE_WIDTH_DIAGNOSTIC.md) remain unchanged.

The [module](../../../det8/models/certified_probability_envelope.py) exposes
`certify_probability_envelope(outcomes, lower, upper, *, proxy_budget=None,
resource_limits=None, provenance_reference=None)`. It returns immutable input,
resource and disposition records. Successful arithmetic additionally returns
the complete common-denominator witnesses, tightened endpoints, normalized
rational proxy `q`, exact uniform-in-envelope TV bound `eta`, and any exact budget
comparison products. The construction and proof remain those of the design
note; this implementation makes no minimax or universally sharp-bound claim.

For example, the following invented inputs are covered by the deterministic
tests:

```python
from fractions import Fraction as F
from det8.models.certified_probability_envelope import certify_probability_envelope

result = certify_probability_envelope(
    ("a", "b", "c"),
    (F(1, 5), F(1, 10), 0),
    (F(3, 5), F(1, 2), F(1, 5)),
    proxy_budget=F(3, 16),
    provenance_reference="synthetic example; unverified",
)
if result.status == "CONDITIONAL_PROXY_CERTIFICATE":
    certificate = result.certificate
    # q = (39/80, 31/80, 1/8), eta = 3/16, exactly.
    # result.operational_admission is still "ABSTAIN".
```

The provenance reference is an opaque, unverified string, not an authenticated
claim. In particular, providing a string does not establish simultaneous valid
coverage, a complete outcome dictionary, conditional-on-history validity or
scientific applicability. Frozen dataclasses provide ordinary immutability,
not a security boundary or authenticated credentials. Use factory-produced
results; do not treat manually assembled records as verified certificates.

## Input and disposition contract

All three containers are plain lists or tuples, with matching lengths in
1..256. Outcome identifiers are distinct nonempty plain strings of at most 128
characters. Endpoint values and an optional budget are plain integers, plain
`Fraction` values, or already reduced `(numerator, positive_denominator)`
tuples. Each numerator and denominator has at most 256 bits. Booleans, floats,
numeric/container subclasses, generators and implicit adapters are rejected.
The provenance reference is `None` or a plain string of 1..1024 characters.
These interface limits do not certify outcome completeness or endpoint origin.

Every endpoint and budget lies in [0,1]; each lower endpoint must not exceed its
upper endpoint. Endpoint vectors need not themselves sum to one. The original
box must contain a normalized row: sum(lower)<=1<=sum(upper). No clipping,
rescaling, outcome dropping or favorable selection is performed, including for
zero-probability outcomes. Missing `proxy_budget` means no budget claim; it is
not an inferred allowance.

| Disposition | Meaning |
| --- | --- |
| `CONDITIONAL_PROXY_CERTIFICATE` | Arithmetic and consumer precision checks completed; any supplied budget passed. External scientific premises remain unverified. |
| `INFEASIBLE_ENVELOPE` | The original endpoint totals exclude normalization. No certificate is returned. |
| `ABSTAIN_RESOURCE` | A declared reservation is insufficient, or the derived proxy exceeds the categorical map's 256-bit weight limit. No certificate is returned. |
| `ABSTAIN_BUDGET` | The computed bound exceeds the supplied allowance. Only the compared bound is retained diagnostically, with no complete certificate or proxy. This is not a statistical FAIL or proof that no better bound/proxy exists. |

Malformed types, sizes and ranges raise `TypeError` or `ValueError`. After
bounded input parsing, resource admission intentionally precedes inverted-bound
cross-products and feasibility: resource refusal can therefore precede either
an inverted-endpoint `ValueError` or an infeasible-envelope result. Derived
consumer precision refusal precedes the final budget comparison. Unexpected
runtime exceptions, including allocation failure, return no result; consumers
must treat them as non-admission/ABSTAIN, never as acceptance. No retry or
partial complete certificate is produced.

## Resource policy and categorical-map interface

The implementation admits both `C` and `C_compare` from the design note before
LCM, endpoint cross-products or proxy construction. `C_compare=0` denotes an
absent budget; otherwise it is `C+K_tau+1`. The default maximum intermediate
precision is 262,413 bits; callers may choose a smaller nonnegative cap. The
large-denominator budget counterexample is explicitly tested: construction
bound 21 alone cannot admit a 255-bit budget, for which the declared comparison
reservation is 277 bits.

`EnvelopeResourceLimits` also applies a conservative logical integer-storage
reservation of `(32*m+64)*max(256,C,C_compare)` bits. The slot policy covers the
explicit endpoint fractions, common-denominator arrays, output fractions and
scalar arithmetic workspace with slack. It is an admission policy for logical
integer magnitudes, **not a measured or enforced process-memory bound**. Python
object overhead, allocator/gcd internals, caller input creation and retained
text are not counted as RSS. Text has the separate length bounds above. The
default storage cap is the formula's supported-profile maximum; lower declared
caps can cause abstention even when a more economical implementation might fit.
A deployment needing hard memory/time limits must enforce them separately.

The exact reduced output weights must independently fit the existing
[categorical map](CATEGORICAL_MAP.md). Bounded input denominators alone do not
guarantee this. A successful `certificate.proxy_weights` tuple can be passed
directly to `CategoricalMap`; this does not acquire bits or execute a sampler.
The external error composition remains
`min(1, eta + rounding_tv + conditional_bit_error)`, with a separate channel
allowance and the frozen protocol's certificate/failure budgets. No bit error,
channel bound, effect, availability rate or feasible sample count is supplied.

## Checks and remaining work

The [15 stdlib unittest cases](../../../det8/tests/test_certified_probability_envelope.py)
use only invented exact rational inputs. They cover the documented witnesses
and map interface, singleton and forced-zero cases, infeasibility, tiny/zero
budgets, strict types and profile limits, immutable copies, comparison and
storage preflight refusal, derived-weight precision blowup, permutation
equivariance, and 216 small boxes checked against independently enumerated
quarter-grid normalized triples and all eight events. These finite checks do
not prove the all-real-target theorem or certify scientific inputs.

The source-inspected isolated author runner loaded only the new test module,
new source preview and an exact copy of the existing categorical-map dependency. It reported
**15 tests passed, exit 0**, with unittest time 0.026 seconds. This is a software
check duration, not a benchmark cost or failure-rate estimate. After integration,
the focused repository command is:

```sh
python3 -B -m unittest det8.tests.test_certified_probability_envelope -v
```

The next interface question is how an independently reviewed certificate
producer will supply complete-row outcome/provenance and simultaneous-coverage
evidence. That contract remains separate from obtaining actual native intervals
or running any sampler. No acquisition, scientific sampling, diagnostic
threshold change, historical custody repair, production qualification or RET
research follows from this component. The [publication evidence
boundary](PUBLICATION_NOTE.md) remains in force.


## Complete-row admission boundary

The [prospective admission design](ENVELOPE_ADMISSION.md) binds endpoints and
simultaneous coverage to the declared law, parent, sector, old marking and
complete ordered row. The frozen diagnostic uses eleven ideals and twenty-two
marked outcomes; the distinct eight-ideal P4 theorem cannot substitute for it.
Structural checks do not establish mathematical validity or authenticity.
No adapter, native interval certificate or operational admission is supplied.
