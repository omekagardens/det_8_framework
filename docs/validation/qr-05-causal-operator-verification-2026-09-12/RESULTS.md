# Causal-operator verification: exact results and decision

12 September 2026. **This bounded verification gate is complete.** The first
capture passed without source repair. Independent finite-power and exact-
elimination implementations agree on all 52 rows and 304 path records.
All 27 tests pass in each normal and optimized mode; three complete replays,
including the single Python 3.11 replay, match the first capture exactly.

The [prospective contract](README.md) and
[prior analytical design](../qr-05-causal-operator-design-2026-09-12/README.md)
define a supplied finite order and chosen rational response matrix. This
result is not physical wave-operator selection, acquired geometry, calibrated
inversion, RET readiness or gravitational dynamics.

## What the full report verifies

Each row retains the complete world (C,A,d), cover matrix, powers through
A^n, M=dI−A, G=M^(-1), Δ=G−G^T, both inverse products, every strict path and
its rational contribution, support masks, closures and all missing/extra
relation witnesses. Native Fraction/int/bool distinctions are checked before
serialization. Target orders and case IDs are not observation encodings.

| Retained quantity | Verified total |
|---|---:|
| Base cases / labelled variant rows | 13 / 52 |
| Event occurrences / cells per reported matrix | 148 / 452 |
| Strict ordered pairs / covers | 120 / 92 |
| Nonzero A / off-diagonal G entries | 100 / 100 |
| Paths: trivial / one-edge / two-edge | 148 / 120 / 36 |
| Zero-contribution paths, retained | 24 |
| Rows with direct support equal to the supplied order | 36 |
| Rows with reachability equal to the supplied order | 48 |
| Explicit same-channel/different-order witnesses | 12 |

The four variants are identity, cyclic relabeling, fixed-label order reversal
and joint positive rescaling of A,d. Symmetric duplicates are retained. These
are 52 specified algebraic checks, not 52 independent statistical trials.

The independent test oracle selects G from the analytical base-entry table,
not from either implementation. It reconstructs and compares the full report.
Tests also verify the transformation of powers and complete path data, the
nilpotent finite sum, both inverse products, cover identities, actual sign
predicates and every collision target pair.

## The constructive result survives exact verification

The analytical theorem says

`TC(nonzero off-diagonal G) = TC(nonzero A) ⊆ C`.

All 52 rows satisfy this equality. The entire supplied order is recovered
by that reachability precisely when all cover weights are nonzero. This
occurs in 48 rows, including the signed cancellation examples. The other
four are the deliberately missing-cover case and its three transforms.

Direct entrywise support is stronger and holds in only 36 rows. Besides
missing_cover, it fails in signed_diamond, toy_cancel and
signed_relabelled_chain, each under all four variants. Those signed cases
retain the order through surviving paths even though a direct response
vanishes. The tests keep these two outcomes separate.

The pointwise sign theorem is checked under its full premise: A is entrywise
nonnegative AND all cover weights are positive. Positive cover weights alone
do not exclude a negative noncover contribution. No exact-support result is
a uniform threshold guarantee for noisy or arbitrarily small responses.

The finite report checks the fixed subclass. The proof for arbitrary finite
strict orders remains the analytical result in the prior design; enumeration
of these examples is not a substitute for that proof.

## Counterexamples retained, not explained away

In toy_cancel at d=3, the endpoint contributions are exactly −1/3 and +1/3.
They cancel. At d=5, the adjacent response is 3/25 while the endpoint response
is −6/125. The audit's old whole-inverse sign convention is checked explicitly
through M=−H, G=−H^(-1); the two conventions are not mixed.

The signed diamond cancels its two nonzero cover-path contributions. Its
zero-weight direct noncover path is also retained in the report, so zero
coupling and signed cancellation remain visible as different contributions.

All twelve declared information-loss witnesses survive:

- The missing-cover chain and a single-edge order with an isolated event
  have identical full G but different orders. Full G recovers its chosen
  matrix, not additional latent relations outside the matrix's reachability.
- A forward pair and a reversed pair with a signed coupling share Δ.
- A fork and a nonisomorphic signed chain also share Δ, even though every
  cover is nonzero in each. Their full directed G matrices differ.

A common function of an identical Δ cannot split those worlds. Conversely,
a supplied compatible topological ordering changes the interface and can
resolve the receiving side; supplying d then completes the diagonal of G.
The negative result is not a claim of impossibility after new information
has been supplied. Nor can a chosen function of the previous O,P,T channels
remove their established geometric ambiguity.

## API and evidence checks

The 17 mathematical/API tests and ten evidence tests cover all specified
native refusals, invalid orders and forbidden weights, no automatic repair,
arbitrary labels, shared-input-row acceptance, fresh containers and input
nonmutation. Inclusive 128-bit rational boundaries are accepted, including
valid outputs exceeding the input bit bound. Oversized inputs are refused.

A separately named maximum-depth API control verifies the four-event chain:
A³_30=1, A⁴=0, G_30=1 and the unique three-edge contribution. It is not an
extra fixed-study row or a post-run fixture search. The shared-row and maximum-
depth controls, and the clarified no-input-alias-output wording, were fixed
before source freeze and before any new mathematical execution.

The [source freeze](source-freeze.json) binds nine files: six new contract/
implementation/test files, both prior design documents and the pinned BM
evidence utility. Only evidence helpers from that old utility were used;
no prior mathematical executor or rejected branch engine ran. Capture and
replay authenticate the sources and freeze bytes before analysis, recheck
them afterward, publish exclusively and read back. Tests exercise malformed
metadata, native type mismatch, source drift, tampering and publication races.

The complete [first capture](results.json) has a canonical encoded report
of 165,114 bytes with SHA-256:

```text
1fdeebb292c84bd8a4617f9515082a8b06b199f1c87ff4816f75b65de36d9bca
```

The [verification log](verification.json) retains the actual command outputs.
The primary runtime was CPython 3.14.0; the alternate replay used CPython 3.11.6.
Both 27-test suites completed in under half a second. Every run stayed within
its declared analysis/suite bound. No post-first-run source changes, repeated
capture, threshold tuning, random sampling or new empirical data were needed.

Final read-only metadata review matched all 37 source bindings across the
new gate and prior joint-geometry, reconciliation and BV bundles. All four
captures bind their source identities and freeze digests; the earlier artifacts
remain unchanged. All 112 checked local Markdown links resolve and the tracked
diff passes whitespace checks. All 235 preexisting status entries remain
present, including the 231 unrelated entries; only the new verification
directory was added to the status inventory during this gate.

## Roadmap decision

The finite causal-operator design now has its independent exact executable
check. Next is a **design-only supplied-measure/divergence-operator contract**:
fix node measure, edge conductances, coordinates and boundary fluxes, then
derive weighted conservation, adjoint/energy identities and the actual
selected kernel's first two moments. This directly addresses the audited
CR mismatch rather than extending the signed-path example set.

Keep supplied coefficients and measure distinct from quantities recovered
from O,P,T. Exact finite-grid identities do not establish smooth-limit scaling
or a physical spacetime wave operator. Correspondence/noncollapse, uniform
bounds, stochastic growth/null calibration and empirical interfaces remain
subsequent separate work. RET/application readiness is not promoted; book
work remains archival and deferred clocks/retired couplings stay closed.

The authoritative branch remains ret at published checkpoint
`47262b616296c632189d4e8b3e2582ed2016a6d8`. This gate and the preceding local
research gates remain uncommitted. No commit/push, dependency installation,
core/RET edit or temp_qr.md edit was made in this gate.
