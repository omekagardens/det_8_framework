# QR-05BM: bounded relative-volume verification

9 September 2026 (Pacific/Honolulu). Prospective executable protocol,
written before implementations or fixed numerical evaluation. This tests
the [BL model](../qr-05bl-relative-volume-design-2026-09-09/README.md),
not a detector, RET integration or gravitational dynamics. The analytical
identities in BL are predictions to verify, not new acquired observations.

## Frozen question and mathematical domain

Can the complete accessible membership law identify one unknown relative
spacetime volume in a declared proper-volume-sampled family, while preserving
the exact density-compensation and absolute-scale obstructions?

Use signature (+,−), null coordinates u,v and five worlds fixed by
[protocol.json](protocol.json). In each world,

```text
ds²=s(1+ηuv) du dv,
dμ=s(1+ηuv) du dv/2,
ρ=1+δuv,
ν(A)=∫Aρdμ/∫Qρdμ,
τ=μ(I)/μ(Q),  q=ν(I).
```

The protocol field `density_uv` is δ, a scalar sampling weight coefficient
relative to proper volume, not a geometric determinant. The worlds are
A=(η,s,δ)=(0,1,0), B=(1,1,0), C=(0,1,1), D=(0,4,0), E=(1,4,0).
Q=(0,1)² and I=(0,1/2)² are the causal intervals marked by
o=(0,0), m=(1/2,1/2), t=(1,1). The same marks and causal comparator are
assumed available in every world. No midpoint or clock measurement is implied.
All boundary cases have zero measure for these smooth positive densities.

Fix N=4 fresh iid points from ν, with the actual world hidden and fixed
throughout the run. The only geometric observation is Yj=1{Xj∈I}.
Retain all sixteen ordered membership words, with probability
q^k(1−q)^(4−k), and all five count bins with their multiplicities.
The estimate is k/4. Compute its full-law expectation, variance and bias
relative to τ, rather than treating one word as an exact target measurement.
This is a fixed quota, not a Poisson count or a thinning model.

For the optional QM extension, four independent qubits I₂/2 carry no world
information. Local Πz=(I₂+zZ)/2, z∈{−1,+1}, act on fresh separate factors.
For each y and z word, retain the unnormalized sixteen-dimensional branch
state P(y) Jz((I₂/2)^⊗4), its trace and normalized conditional state.
The independent classical comparator uses four fair bits. Computational
basis order is 0000 through 1111, with +1 selecting bit0 and −1 bit1.
All sixteen diagonal entries, including zeros, are retained; every omitted
off-diagonal entry is identically zero for the declared diagonal product
preparation and projectors. This representation specifies the full states,
not marginal states. No arbitrary-state instrument-map equality is claimed.

## Prespecified passive-coordinate control

Use exactly U=2u+1 and V=3v−1. Its inverse is u=(U−1)/2,
v=(V+1)/3 and du dv=dU dV/6. Thus

```text
ds²=s[1+η(U−1)(V+1)/6] dU dV/6,
dμ=s[1+η(U−1)(V+1)/6] dU dV/12,
ρ'=1+δ(U−1)(V+1)/6.
```

The transported marks are (1,−1), (2,1/2), (3,2);
Q'=(1,3)×(−1,2), I'=(1,2)×(−1,1/2). Transport metric,
measure, scalar density and marked regions together. Never give the scalar
density a second Jacobian. Independently integrate the transported densities.
Each proper volume and weighted normalizer, not just their ratios, must
equal its original-chart counterpart. These are the same five worlds, not
additional hypotheses, new points or extra observer coordinates.

## Identification and negative controls

Compare entire ordered-law vectors, preserving world labels. For both the
positive {A,B} and expanded {A,B,C,D,E} menus, compute labeled equivalence
classes, sorted target sets, class/menu identification flags and support-only
candidate sets for every membership word. Repeat law classification using
complete joint membership/Z probabilities. Conditional quantum states must
also be world-independent, so probability-only classification does not hide
an additional quantum channel.

Require the following together, without priors or fitted noise:

- The proper-volume A/B targets and laws differ, and their sample means are
  unbiased under the declared sampler. All finite words still have positive
  probability, preventing zero-error finite-shot identification.
- B/C have equal entire weighted point-density polynomials and normalizers,
  but different relative geometric volumes. The collision is not merely
  equality of q or a finite selection of moments.
- A/D and B/E have equal normalized point and record laws and targets, but
  their absolute volumes differ by the declared scale four.
- The membership/Z law marginalizes to membership and has the same
  target-identification classes. Identical independent qubits add no
  statistical information over the complete membership experiment.
- Passive coordinates preserve the geometric and sampling integrals.

Exact synthetic disagreement must be retained as an implementation or
premise failure, not dismissed as physical noise. Calibration can exclude
nuisance worlds only through additional independently justified information.

## Exact native report contract

Both independent engines expose `analyze(protocol)` without file access,
shared mathematical helpers, imports from one another or result lookups.
They must not mutate protocol. Native reports use only exact `Fraction`,
plain `int`, `bool`, `str`, `list` and `dict`, never floats. All computed
scalars (even integral-valued probabilities) use Fraction. Integers label
degrees, outcomes, counts and schema metadata; booleans are not integers.

Polynomials are canonical lists `[i,j,Fraction]` of nonzero coefficients
of the first-coordinate power i and second-coordinate power j, sorted
lexicographically. Zero polynomials use an empty list. Report keys are:

- Top level: `schema`="qr05bm-report-v1", `quota`=4, `worlds`, `menus`,
  `controls`. World order is protocol order; words use lexicographic order
  with y∈(0,1)^4 and z∈(−1,+1)^4.
- Each world: `id`, `geometry`, `membership`, `histogram`, `moments`, `cq`.
- `geometry`: `metric_uv`, `density_uv`, `proper_uv`, `weighted_uv`,
  `normalized_uv` polynomials; Fraction fields `volume_Q`, `volume_I`,
  `mass_Q`, `mass_I`, `target`, `q`; and `chart`. `metric_uv` is the
  coefficient of du dv, twice the off-diagonal metric-matrix entry.
- `chart`: `metric_UV`, `density_UV`, `proper_UV`, `weighted_UV`,
  `normalized_UV` polynomials and the same six scalar fields as geometry.
- Each `membership` row: `y` (four ints), `k` (int), `p` (Fraction),
  `estimate` (Fraction). Each `histogram` row: `k`, `multiplicity` (ints),
  `p` (Fraction), in k=0,...,4 order.
- `moments`: Fraction fields `mean`, `variance`, `bias`.
- Each `cq` row: `y`, `z` (four ints each), `p`, `trace` (Fractions),
  `diagonal`, `conditional_diagonal` (sixteen Fractions each).
- Each menu: `id`, `worlds` (IDs in protocol order), `classes`, `cq_classes`,
  `identified` (bool), `support`. Each class has `worlds`, `targets`
  (distinct Fractions in increasing order), `identified` (bool). Class
  order follows the first member's menu position. Each support row is
  `y`, `worlds` (positive-probability compatible IDs, menu order).
- `controls`: `density_equal` (bool; both full polynomial and normalizer),
  `density_target_gap` (τC−τB, Fraction), `scale_pairs` (A/D then B/E),
  `chart_invariant` (list of IDs passing all six scalar equalities),
  `cq_marginals_match`, `cq_conditionals_common` (bools).
  Each scale row has `worlds`, `volume_factor` (Fraction),
  `normalized_equal`, `target_equal`, `law_equal`, `cq_equal` (bools).

The primary route uses monomial polynomial algebra/integration and explicit
local quantum projectors/tensor products. The reference independently uses
tensor Simpson integration (exact for this bounded polynomial degree),
classical Bernoulli/fair-bit probabilities and independently constructed
computational-basis outer-product diagonals. It constructs its own polynomial
coefficients and law classes. A third test route uses rectangle endpoint
antiderivatives and exact expected identities. Sharing the input/schema is
allowed; sharing mathematical implementation or computed answers is not.

## Observer packet and refusal contract

`study.estimate(packet)` receives exactly a plain dict with keys
`protocol`, `query`, `variant`, `records`. The first two values are exactly
"qr05bm-v1" and "o-m-t". Variant is "membership" or "membership-z".
`records` is exactly a plain list of four plain dicts in attempt order 1..4.
Each has exactly `attempt` (plain int) and `y` (plain int0 or1); the Z
variant additionally requires exactly one `z` (plain int−1 or+1).
All string values are plain strings. No implicit bool/float conversion,
list reorder, missing attempt, duplicate attempt, unknown query/variant,
extra key or undeclared nested object is accepted. Failure raises ValueError.
The return is exactly Fraction(sum(y),4); optional Z outcomes do not alter it.

Public candidate predictions are allowed as model knowledge, but an actual-
world-selected label, probability, numerical ensemble/branch state, target,
density, scale, seed or sample coordinate is never an observer field.
Physical normalized conditional qubits may be retained in the mathematical
experiment; the packet codec does not serialize a hidden numerical state.
No producer-to-observer apparatus implementation is certified by this schema.
Nondetections require a future expanded law, not y=0 or omitted rows.

## Evidence, freeze and work bounds

`study.py` is the small independent evidence driver, with no RET/core imports
or dependencies beyond Python's standard library. Before fixed evaluation,
create `source-freeze.json` exclusively with byte identities of this README,
protocol, both engines, driver, test file and both preceding BL documents.
It includes runtime identity and does not contain computed mathematical
results. Engines are freshly executed from checked source bytes, not cached
imports. Input protocol bytes must match the fixed protocol in this gate.

Compare entire native reports with exact types before encoding. Encode a
Fraction only as `{"$fraction":[numerator,denominator]}` with positive
denominator and reduced canonical terms; plain ints/bools remain distinct.
Reject duplicate JSON keys, nonfinite/float values, unknown tags, missing or
extra capture fields, noncanonical fractions and type-changing substitutions.
The capture binds the full report, all source identities and freeze digest.
Create-only writes require exclusive creation and readback; replay is read-
only and recomputes both complete engines. Final byte identities are checked
again. This is local reproducibility protection, not hostile-host security.

No adaptive fixture/menu/quota/chart changes. Any post-first-evaluation source
correction requires documented failure and a new, separately named freeze
and capture; never overwrite evidence. Pre-evaluation review corrections
may be incorporated before the first freeze and must be distinguished from
observed failures. Tests may use disposable temporary files for corruption
controls but never alter retained evidence or live source files.

Fixed coverage: five worlds, 80 membership rows, 25 histogram rows and
1,280 joint membership/Z rows. No loss-law enumeration or random simulation.
Maximum source file is 262,144 bytes; any input/output artifact is capped at
16,777,216 bytes. Each analysis has a 30-second wall-time bound; each test
suite has a 120-second bound, with no automatic budget expansion. Execute
one normal suite, one optimized suite, normal/optimized full replay and
exactly one reference-only alternate-runtime analysis (30-second bound).
Tests cache one full driver analysis per suite; no subprocess stress loops
or unrelated inherited research trees. Runtime violations stop the gate
for recorded review. Do not overlap a timing-sensitive RET rehearsal.

The bounded alternate analysis compares the complete canonical reference
report, not only a digest or scalar summary, with the retained mathematical
report. No new package installation, physical data or broader repository
test suite belongs to this gate.

## Interpretation and reproduction

Success establishes exact agreement for this finite mathematical model,
including failures of identification in its expanded menu. It is not
arbitrary-metric reconstruction, quantum advantage, measured compatibility,
calibrated sampling, ontological evidence or gravitational field dynamics.
No independently known uniform acquisition process is supplied by the
Bernoulli calculation itself.

After capture, run from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bm.py
python3 -I -O -B test_qr05bm.py
```

The initial `--freeze source-freeze.json` and `--capture results.json`
commands are create-only; existing evidence must not be deleted to repeat
them. Execution results and any corrections are recorded separately in
[RESULTS.md](RESULTS.md). The preceding [BL decision](../qr-05bl-relative-volume-design-2026-09-09/RESULTS.md)
is context, not inherited execution evidence. Book work stays archival;
Lean, RET interfaces, clocks and later gravity couplings remain separate.
