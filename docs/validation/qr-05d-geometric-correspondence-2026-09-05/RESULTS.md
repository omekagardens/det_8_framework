# QR-05D results: what order-derived propagation does and does not recover

5 September 2026. **Bounded geometric-correspondence investigation completed.**
All 200 tests pass normally and under optimized Python. The version-two capture
replays exactly. The original capture is preserved with its documented
container-serialization defect, not silently replaced.

## Main result

The retained event order supports a precise new family of questions: causal
support, interval counts, and density-dependent retarded scalar-kernel
coefficients. We compared these with nine supplied order/coordinate fixtures
using two independent exact implementations. The comparisons identify useful
correspondence and explicit failures of geometric identification.

The kernel formula is an established comparison construction, not new DET
physics. Our contribution here is the bounded diagnostic, independently checked
implementation, and controls connecting it to the quantum-record research.
The tested spacetime geometry is supplied, not recovered from first principles.

The order kernel is

```text
K(z) = C/2 - z C²/(4 rho) + z² C³/(8 rho²) + ... ,  z = mass².
```

C is the strict causal matrix; C² counts intervening events and C³ counts
related pairs inside an interval. On supplied timelike pairs, compare with
the coefficients `1/2, -tau²/8, tau⁴/128` of the standard 1+1-dimensional
retarded scalar Green function. These formulas come from the established
chain-sum and continuum expressions; no QFT derivation is asserted here.
[Johnston, equations 3.23 and 3.31](https://arxiv.org/pdf/0806.3083).

These are signed scalar-kernel coefficients, not quantum channels, Born
probabilities or amplitudes to be summed across the earlier classical record
alternatives. No interaction between this kernel and the fixed qubit has been
introduced. Only coefficients through z² are compared for every pair; the
complete finite endpoint polynomial is also retained.

## Positive correspondence, with calibration visible

The deterministic meshes have 9,25,49 interior events and known 1+1 flat
coordinates. Their causal matrices agree exactly with the supplied light-cone
comparisons. This verifies implementation consistency with the generator;
it is not independent evidence that the generator is physical.

A specified Lorentz boost preserves every interval and diagnostic exactly.
A dilation, which is not a Lorentz isometry, rescales the coefficients correctly
when the supplied density changes consistently. Keeping the old density instead
produces a whole-region volume estimate of 1/2 where the supplied volume is 2.
That deliberately wrong density is retained as an error, not adjusted away.

For the meshes, rho is set to N divided by the supplied whole-diamond volume.
Thus the whole-diamond count-volume match, and its coefficient -1/8 at z,
are true by calibration. The higher coefficient asks a different question:

| Interior events N | Order-derived z² coefficient | Supplied continuum value | Exact excess |
|---|---|---|---|
| 9 | 1/96 | 1/128 | 1/384 |
| 25 | 1/100 | 1/128 | 7/3200 |
| 49 | 15/1568 | 1/128 | 11/6272 |

The excess decreases across these three sizes but remains nonzero. Local
volumes also remain biased. For the 25-point mesh, either midpoint half-interval
has count-derived volume 4/25, versus coordinate volume 1/8.

These are deterministic mesh discrepancies, not statistical fluctuations or
experimental noise. The tilted meshes avoid null/coincident pairs but are not
Poisson sprinklings. A transformed fixture is not a Lorentz-invariant sampling
ensemble; three mesh sizes are not a validated continuum limit.

## Local geometry can change while every order diagnostic stays the same

Actively relocate the 25 mesh points by `(u,v)->(u²,v²)`, while retaining the
same flat-metric convention. This preserves the order, the global diamond,
total count and calibrated global density. All order-derived coefficients stay
identical, but the local sampling density and coordinate intervals change.

The two intervals adjoining the central event both still have kernel
coefficients `1/2, -1/25, 19/20000`. Their supplied local volumes are:

| Interval | Before relocation | After relocation | Count-derived volume |
|---|---|---|---|
| Bottom to middle | 1/8 | 1/32 | 4/25 |
| Middle to top | 1/8 | 9/32 | 4/25 |

This is an explicit local ambiguity, not a statement that physical geometry
changes under a passive coordinate transformation. A passive transformation
would also transform the metric. The control shows why order and one global
density do not identify a local metric/volume profile without further premises.

## Even the complete endpoint polynomial can miss an embedding obstruction

Two six-event interior orders have identical event, relation, link,
incomparability, minimal/maximal and height counts. After adding bottom/top
probe events, both have the full endpoint chain array
`[1,6,6,0,0,0,0]`. At the same algebraic density parameter their entire endpoint
kernel is exactly

```text
1/2 - z/8 + z²/192.
```

One is supplied with valid 1+1 flat coordinates. The other is the standard
example S3. Exhaustive checks find 57 linear extensions and two ordered
two-extension realizers for the coordinate example; S3 has 48 extensions and
no such realizer. The protocol also gives the short cycle-based obstruction
proof. Their local interval tables differ despite the endpoint match.

This obstructs an exact order embedding of S3 into this 1+1 flat null-product
model, preserving and reflecting all comparisons. It does not establish that
S3 is non-geometric in every dimension or every curved spacetime. In particular,
endpoint-kernel agreement is not a certificate that an order comes from the
chosen geometry.

## What this adds to the quantum-record calculus and Track-B

The geometric diagnostics answer questions about the retained order. They do
not subsume the quantum payload or the location of recorded outcomes. Six
parent-order analyses from QR-05C were recomputed independently, while their
quantum/count discrepancies were preserved as pinned prior witnesses:

- Fork and join still have equal endpoint chain polynomials despite different
  local orders and unequal next-birth count predictions.
- Same-order histories with different record locations have identical new
  order diagnostics but unequal retained quantum predictions.
- The earlier delayed quantum-state failure remains a separate witness;
  QR-05D does not repair or reinterpret it.

The practical mathematical structure is therefore a set of separately typed,
question-specific descriptions: the quantum operation, the marked event order,
and a geometric comparison using stated density/localization assumptions.
A proposed summary must preserve the questions actually needed on each layer.

This gives Track-B a concrete research constraint: supply or identify a local
volume/sampling model, and test spatially resolved questions before interpreting
global count or propagation agreement as geometry. The continuum order/volume
motivation is useful context, but it does not supply those missing finite-data
premises. [Surya, sections 2--3](https://arxiv.org/html/1903.11544).

## Evidence and the replay correction

The original 133 tests passed normally and optimized, but the first full replay
found one aggregate-container mismatch: a Python tuple was serialized as a JSON
list. A recursive comparison found no changed numerical or mathematical value.
The original six sources and [v1 capture](results.json) remain intact.
See the [version-two correction](REVISION_V2.md) for the exact failure and repair.

The corrected driver uses a native-JSON guard on the entire mathematical suite,
not only individual executor outputs. It must reproduce the preserved v1
mathematical JSON exactly before creating or replaying the version-two artifact.
Comparisons use canonical bytes, preserving the Boolean/integer distinction
that ordinary Python equality can miss. The regression suite includes both
that distinction and the previously missing aggregate round trip.

The final combined suite passes **200 tests in 3.67 s normally and 3.65 s
optimized**, including the 67 version-two regression/lifecycle cases. Optimized
pytest emitted its expected warning about assertions outside rewritten test
modules; executable validators use explicit exceptions. Ruff checks pass.

The retained mathematical inventory comprises nine full fixture analyses,
213 events across fixtures, 6,495 matrix positions, 19,485 coefficient cells,
2,154 supplied geometric-pair comparisons and 5,553 ordered realizer-pair checks.
There are also two independent collision-interior checks and six prior-parent
checks. These counts describe different checks and should not be combined into
a claim about that many independent observations.

A separate JSON-only audit, without importing either executor, verified all
17 retained order analyses, all geometric comparisons and coefficients, the
realizer obstruction and prior witnesses. It checked the canonical rational
strings and maximum component size of 96 bits. No empirical data, tolerance
fitting, RET integration or new dependencies were used.

The current [results-v2.json](results-v2.json) is 2,523,927 bytes, SHA-256:

```text
18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32
```

It binds nine source identities and eight prior artifacts, including the
unchanged version-one capture. The final JSON-only audit verified its hash,
all source/prior identities, preservation of the original source ledger, and
type-sensitive equality of the complete v1/v2 mathematical suites. The earlier
independent mathematical audit therefore applies unchanged.

Isolated Python 3.11.6 on macOS arm64 used a
fresh external cache. Capture took 1.145 s with a 90,128,384-byte process RSS
high-water mark; fresh optimized replay took 1.133 s and left the artifact
bytes unchanged. These times exclude artifact serialization and are not
application-performance claims. Use the [version-two reproduction commands](REVISION_V2.md#corrected-reproduction-commands).

## Recommended next gate

QR-05E should test **sampling-aware geometric questions** before attempting a
physical apparatus bridge. Start with bounded exact thinning of a supplied
finite order: specify inclusion probabilities, retained endpoints and which
interval/chain questions must survive. Separate equality in expectation from
per-realization prediction, and include nonuniform or correlated-selection
controls. Do not infer an unknown density field by fitting away the warp error.

This is a proposed next protocol, not an executed result. It cannot by itself
resolve the embedding ambiguity or supply a quantum-to-geometry coupling.
The separately planned QR-06 RET quantum adapter remains distinct and subject
to its own SDK and calibration gates. Physical observables, uncertainty and
selection models, continuum dynamics, and gravity remain later work.
