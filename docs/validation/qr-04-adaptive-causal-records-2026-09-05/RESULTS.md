# QR-04 result: adaptive quantum order depends on record context

Completed September 5, 2026. **Exact finite mathematical research, not an
empirical experiment or RET gate closure.** [Protocol](README.md) ·
[Retained evidence](results.json) ·
[Previous QR-03 result](../qr-03-predictive-histories-2026-09-05/RESULTS.md).

## Outcome

We now have an independently checked executor for finite quantum events whose
settings are selected from explicitly available causal-past outcomes. It retains
the selected setting, observed outcome, remaining quantum state, and every
zero branch. It rejects attempts to read unavailable, incomparable, future,
self, or unknown records, including in branches that never occur.

The useful distinction is not simply “adaptive versus fixed.” **Which past
record controls an operation determines which combinations of settings must
be compared.** Two same-qubit measurements sharing one selector can commute
in every permitted control context, while independently selected versions of
those measurements can conflict. Missing a dependency edge or running an
event earlier in a scheduler never grants permission to read its record.

All eight selected examples matched the independently implemented reference.
Seven preserve the complete source-to-output map across their permitted
schedules; one is a deliberate conflict. One of the seven has only one
schedule, so six are nontrivial schedule comparisons. These are selected
diagnostic cases, not a success rate over quantum processes.

## Two different certificates

| Certificate | What is compared | What passing establishes |
|---|---|---|
| Full source-to-output schedules | Every complete recorded map on every original quantum input operator | Order does not matter for this fixed process and source |
| Universal pair-context swaps | Every incomparable pair on arbitrary intermediate operators and every formal read context | A stronger sufficient guarantee for schedule independence |

The stronger test passes in five fixtures, including the one-schedule vacuous
control. Two other fixtures pass only the source-to-output test. Their source
restricts what can actually reach the later operations, hiding failures on
unreachable classical contexts or unreachable quantum states. A failed stronger
certificate therefore does **not** automatically refute a source-specific result.

The conditional argument is straightforward: incomparable events cannot read
each other's fresh records; their shared past is unchanged by swapping them.
If the corresponding outcome-and-setting-resolved maps commute in every read
context, the complete controlled classical–quantum maps commute. Adjacent
incomparable swaps connect all linear extensions of the finite event order.
This is standard commuting-map reasoning with explicit record access, not a
new physical law or a proof of relativistic covariance.

## What the fixtures show

| Fixture | Schedules | Source-to-output | Universal swaps |
|---|---:|---|---|
| Ordered Z followed by outcome-controlled I/X reset | 1 | Equal; ordered control | Vacuous |
| Shared selector chooses the same Z/X basis for two overlapping measurements | 2 | Equal | Equal |
| Independent selectors choose the two measurement bases separately | 6 | Different | Different |
| Two parent outcomes jointly select I/S through an XOR rule | 2 | Equal | Equal |
| Shared selector controls complex local measurements on separate qubits | 2 | Equal | Equal |
| Adaptive multi-Kraus damping/reset with an independent local measurement | 2 | Equal | Equal |
| Measure-and-reset source before Z and controlled damping | 2 | Equal | Different |
| Identity/zero source hides a phase-setting conflict | 2 | Equal | Different |

The two-read fixture checks parent reordering followed by a genuinely
two-input policy; it is not a comparison of two incomparable adaptive children.
The shared-selector and disjoint-complex fixtures do compare such children.
The disjoint complex case additionally retains the expected Bell-state
correlations under its selected local settings.

### Shared control is not independent setting choice

A parent coin with Kraus amplitudes 3/5 and 4/5 records 0 or 1. Both later
same-qubit measurements read that same record and select Z for 0 or X for 1.
The relevant setting pairs are (Z,Z) and (X,X), whose outcome maps commute.
Treating the settings as independently selectable would insert (Z,X) and
(X,Z), which are not produced by this policy. The shared record must have one
consistent value on both sides of the comparison.

Giving each measurement its own independent coin instead makes the mixed
contexts available and exposes a genuine failure. For initial state
`P0 = |0><0|`, retain the complete record

`(A:Z0, B:X0, C:coin0, D:coin1)`.

The joint selector probability is `(9/25)(16/25) = 144/625`. In schedule
`C,A,D,B`, the branch output is `(72/625) P+`. In schedule `C,D,B,A`, it is
`(36/625) P0`, where `P+ = |+><+|`. Even the branch probabilities differ.
Both full schedules are permitted by the deliberately insufficient event
order; its proposed order independence is correctly rejected.

These are familiar quantum operations. The diagnostic benefit is making the
control relationships part of the object being certified, not attributing
noncommutation to an unexplained physical effect.

### A source can restrict the quantum states that matter

The source measures Z and resets the qubit to zero in either outcome branch:

`J0(rho) = rho00 P0`, `J1(rho) = rho11 P0`.

Two subsequent incomparable events perform recorded Z measurement and
source-outcome-controlled amplitude damping. Damping has survival/jump
amplitudes `(a,b) = (3/5,4/5)` or `(4/5,3/5)`, according to the source record.
On every reachable intermediate state, both operations leave `P0` unchanged
and their complete recorded outputs agree, for **every original input rho**.

On intermediate input `P1`, however, the branch with Z outcome 1 and a damping
jump gives `b^2 P0` for Z then damping, but zero for damping then Z. This is a
physical state witnessing universal noncommutation, explicitly **unreachable
after this source**. Both source branches themselves are nonzero maps; this
is not explained by deleting an impossible classical outcome.

The separate identity/zero fixture covers that latter situation. A parent
outcome that is never possible selects S instead of I before comparison with
X. The formal impossible context fails the universal test, while every full
source-to-output schedule agrees. The policy row and its zero output record
remain visible; the verifier does not silently prune them.

## Access safety and exact verification

The policy language is deliberately small: explicit total lookup tables over
at most two declared readable past outcome slots. Every setting is validated,
even if unused; every formal read context must have a row, even if unreachable.
The available/read distinction is separate from causal ancestry. Policies
cannot inspect scheduler counters, callbacks, prior settings, or hidden state.
This is a property of the bounded declarative interface, not a security claim
about arbitrary Python programs or physical communication in an apparatus.

Verification and accounting:

- **96 tests passed** in ordinary isolated Python (3.99 s), and **96 passed
  under optimized Python** (3.69 s). The latter emits Pytest's expected warning
  about assertions outside rewritten tests. Implementation checks use explicit
  exceptions; an assertion-free optimized subprocess checks rejection directly.
- Eight complete exact analyses agree with an independent direct-superoperator
  reference. Its policy validation, ancestry/availability checks, branching,
  comparisons, and arithmetic route are separate from the operator executor.
- The retained artifact contains **19 schedules, 166 full-schedule maps,
  10 incomparable pairs, 20 pair contexts, and 140 pair maps**: 306 maps total.
  Five pair contexts fail as expected. Forty-six full-schedule blocks are
  identically zero and are retained, including repeated appearances across
  schedules; this is not a count of 46 distinct physical events.
- The direct route uses **380 matrix-unit executions**. Analytical controls
  apply 20 retained full-process blocks and four retained pair blocks to
  specified physical states, without additional matrix-unit propagation.
- Twelve invalid fixture wires are retained with rejection by both paths.
  Additional tests cover complex phases, multi-Kraus sums, shared versus
  independent selector contexts, two-read transitive access, labels, support,
  bounded numerics, pinned sources and in-memory artifact failure scenarios.
- Both independent source reviews found no remaining mathematical or capture
  blocker. Ruff and formatting checks passed. No source-ledger files were
  changed after capture.
- Create-only capture took **2.098 s**. A fresh isolated optimized replay took
  **2.106 s**, reproducing the complete exact suite and checking source, prior
  artifact, and result-byte identities.
- An independent retained-data audit verified all seven source hashes and
  three prior identities, independently enumerated the schedules and 20 pair
  contexts, checked 35 supplied settings and 37 policy rows, and verified every
  recorded setting/outcome triple. All 306 maps passed exact-entry, dimension,
  Hermiticity-preservation, and trace-sum consistency checks. All 46 zero
  schedule blocks, mismatch entries, flags, counts, and bit fields matched.
- That audit additionally reconstructed 46 full maps from closed-form fixture
  formulas and checked all 20 physical full-map applications and four pair
  witness applications, without importing either implementation or rerunning
  the study. Supplied Kraus completeness/support were independently checked;
  the audit did not separately reprove complete positivity for every composite
  map using a general positivity solver.

Capture used CPython 3.11.6 on macOS arm64. Process RSS high-water sampled at
suite end was 45,137,920 bytes. The largest retained map rational numerator
or denominator needed 12 bits; this excludes peak intermediate allocations
and separate explanatory-control arithmetic. Runtime/RSS exclude subsequent
serialization/comparison overhead and are not application performance claims.

The artifact is 2,440,727 bytes. SHA-256:

```text
a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70
```

Seven protocol/source/test identities are bound in its ledger, including the
two reused QR-01 sources. All three prior QR artifacts remain byte-identical.
This result note is a subsequent interpretation outside the source ledger.
Hashes establish local integrity, not experimental authentication or external
preregistration. No measured observations or fitted nuisance models were used.

## Applicable value and next boundary

The DET event-and-record description now supports a tested adaptive contract:
**which records may control an operation, which setting combinations follow,
and what complete process is preserved under reordering**. Together with
QR-02/QR-03, this prevents conflating record access, physical recoverability,
predictive summaries, and full process equivalence.

This may inform later evidence workflows and measurement planning, but it
does not integrate the RET SDK, validate a quantum adapter, establish a storage
or decision-quality advantage, or close RET G2. The supported core and its
existing conflict policies are unchanged; these are isolated research modules.

The next research question in the charter is QR-05: specify a compatible
quantum-history-to-record-to-order mapping and test its behavior under grouping
and refinement. That construction has not been implemented here. An event
order is not automatically a spacetime geometry, and this result supplies no
clock coupling, gravity source, Lorentz-covariance claim or Einstein dynamics.

All seven new files are confined to this research directory. Existing QR
evidence, RET/hardening sources, dependencies, shared roadmap/charter files,
and gate acceptance rules were not modified. RET reported no timing/source
hold before the short runs. No ontological commitment or new physical law is
required by the result.
