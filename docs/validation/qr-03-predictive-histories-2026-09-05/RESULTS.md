# QR-03 result: histories can be summarized relative to future questions

Completed September 5, 2026. **Exact finite research, not an empirical test.**
[Protocol and argument](README.md) · [Retained evidence](results.json) ·
[QR-02](../qr-02-record-coarse-graining-2026-09-05/RESULTS.md).

## Outcome

We now have a working test for the coarsest partition of source histories
that preserves a declared family of conditional quantum predictions. It checks
every initial qubit density matrix through exact polynomial coefficients,
rather than treating agreement on selected preparations as an all-state result.

The most useful example has **four Z-then-X histories but only two predictive
classes**. For the subsequent X/Y/Z measurement family, retaining the last X
outcome suffices. The earlier Z outcomes still have different occurrence
probabilities and remain in the evidence; this is not permission to erase
provenance or a claim that the past events were identical.

The summary depends on the source, the future question family and the same
supplied initial-state context. It is not a universal scalar or a probability
computed from a class label alone. No measured memory, runtime or decision
improvement is claimed.

## Results by declared future family

| Source | Future measurements | Nonzero histories → classes | Result |
|---|---|---:|---|
| Quantum-independent recorded coin | X, Y, Z | 2 → 1 | Conditional predictions match despite unequal record probabilities |
| Recorded I/Z phase error | Z only | 2 → 1 | Phase distinction is irrelevant to this restricted family |
| Same phase-error source | X, Y, Z | 2 → 2 | Proposed merge correctly rejected |
| Projective Z source | X only | 2 → 1 | Distinct quantum states give the same declared probabilities |
| Same projective source | X, Y, Z | 2 → 2 | Expanded questions correctly split the class |
| Ordered Z then X | X, Y, Z | 4 → 2 | Last X record is a valid summary |
| Repeated Z | X, Y, Z | 2 → 2 | Two other histories are never possible; control, not live compression |
| Identity/zero instrument | Z only | 1 → 1 | Zero branch retained as impossible; control, not compression |

Six proposed summaries pass and two fail. Four passing fixtures perform
nontrivial merging of possible histories; the other two are controls. These
are deliberately selected cases, not a success rate over quantum systems.

Adding questions refines the partition in both source-matched comparisons.
A summary sufficient for Z alone need not suffice for X; a summary sufficient
for one future family is not automatically sufficient for a richer one.

## Why checking a single state is insufficient

For the recorded phase-error example, the maximally mixed input `I/2` gives
the same conditional X/Y/Z probabilities in both histories. That selected
state would hide the distinction.

The all-state criterion finds a full-rank physical witness:

`rho = [[1/2, 1/4], [1/4, 1/2]]`.

For a later X+ outcome, the two conditional probabilities are **3/4 and 1/4**.
Their history probabilities are 9/25 and 16/25. The difference is not a
normalization error: numerator and history weight are retained separately.

Every failed pair in the study has an explicit physical witness. A fixed
ten-state, full-rank probe bank is sufficient to exhibit any nonzero
degree-two discrepancy in the qubit Bloch coordinates. An independent exact
rank calculation in the tests verifies this property. The coefficient
identity remains the all-state criterion; the probes make its failures concrete.

## Correct treatment of zero histories

A history that is impossible on one input is not necessarily impossible on
another. The Z=1 history has probability zero on initial `|0>` but remains a
valid history on other inputs. Its conditional prediction on that particular
input is recorded as undefined, not assigned probability zero.

An identically zero CP history is different: no initial state can realize it.
Such histories are retained as `NEVER_POSSIBLE` and excluded from the ratio
equivalence relation. Otherwise their zero numerator and denominator would
falsely make them equivalent to every history, incorrectly joining distinct
classes. Three such records are retained across the selected fixtures.

For the last-X summary, a control input with Z probabilities 3/4 and 1/4
gives same-class history weights **3/8 and 1/8**, yet identical conditional
future predictions. The test preserves this distinction between a question
about the future and a question about how likely the past history was.

## Additional analytical structure

The exact criterion also yields a useful elementary consequence. This is an
analytical deduction reviewed independently, not a newly executed general
theorem program or a claim of mathematical priority.

Let `d_h,d_k` be the nonzero history-probability linear functionals, and
`n_h,n_k` the numerators for one future question. Equivalence requires
`n_h d_k = n_k d_h`.

If `d_h` and `d_k` are not proportional, they are independent linear forms.
Using them as two coordinates in the polynomial identity forces
`n_h = p d_h` and `n_k = p d_k` for the same constant `p`. Thus that future
prediction is independent of the initial state. This holds for each declared
question. Conversely, a nonconstant shared prediction requires proportional
history-probability functionals.

For a complete one-qubit X/Y/Z family, this identifies two concrete mechanisms:

- If `d_h = lambda d_k` with `lambda>0`, equal normalized predictions imply proportional
  history maps `I_h = lambda I_k`. The labels differ in weight, but not in their
  conditional quantum output.
- If the denominators are not proportional, equivalent histories must prepare
  the same fixed normalized quantum state `tau`:
  `I_h(rho)=d_h(rho) tau` and `I_k(rho)=d_k(rho) tau`.
  The remaining state makes earlier distinctions irrelevant to those future
  measurements, even though the history weights can depend differently on input.

The denominator cases above are disjoint; the resulting structural forms
(proportional maps and common fixed-output maps) can overlap. For
restricted, non-tomographic future families, constant selected probabilities
do not establish equality of the full quantum states. The X-only/projective-Z
example explicitly retains different normalized states `|0><0|` and `|1><1|`.

## Verification and retained evidence

- **75 tests passed** in ordinary Python (0.64 s), and **75 under optimized
  Python** (0.64 s). Pytest emitted its expected optimization warning about
  assertions outside rewritten tests. Implementation validation uses explicit
  exceptions, with a separate assertion-free optimized subprocess control.
- All eight fixture analyses matched an independently implemented
  superoperator reference, including coefficients, partitions and witnesses.
- The retained analysis contains **20 history rows**, **12 nonzero-history
  pairs**, **64 question polynomials / 640 monomial coefficients**, and
  **seven physical discrepancy witnesses**. Impossible histories are not pairs.
- Work accounting is 32 initial Hermitian-basis evaluations and 192 future
  basis-image evaluations. Additional controls use one direct source-state
  execution and six history-level conditional evaluations, containing 28
  future-probability entries, two explicitly undefined on impossible inputs.
  None of these counts denotes independent physical experiments.
- Tests separately check polynomial coefficients, complex-Y signs, multi-Kraus
  sums, witness positivity/probabilities, probe-bank rank, transitivity, maximal
  partitions, stricter candidate summaries, family refinement, schema bounds,
  pinned dependencies and artifact/source/prior stability.
- Both independent source reviews cleared the mathematical argument and
  implementation. Ruff and formatting checks passed.
- Exact capture took **0.114 s**; a fresh isolated, optimized replay took
  **0.114 s**, matching source identities and retained results exactly.
- An independent retained-data audit verified all seven source hashes and
  both prior identities, reconstructed all 20 denominator rows and 96
  numerator functionals from the selected fixtures' analytical formulas, and
  checked all 640 monomial coefficients, partitions, conflicts and seven
  witnesses. It also checked the controls and retained-bit accounting without
  importing or rerunning either executor.

Capture used CPython 3.11.6 on macOS arm64. RSS high-water sampled at suite end
was 39,469,056 bytes. The largest numerator/denominator among retained case
coefficients and witnesses needed 10 bits; that is not peak intermediate
arithmetic. Timing/RSS exclude later serialization and comparison overhead
and are not deployment or performance guarantees.

The artifact is 160,562 bytes. SHA-256:

```text
2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2
```

Seven protocol/source/test files are bound by its ledger, including the two
read-only QR-01 dependencies. QR-01 and QR-02 artifact hashes are checked
before and after work and remain unchanged. This interpretation note is
subsequent to capture and outside that seven-file source ledger. Hashes
provide local integrity, not authentication or external preregistration.

## Value and next step

DET's event/record language now supports a precise question: *which distinctions
in a history matter for which future predictions?* The answer can be computed
and challenged under a declared model. It need not be either “keep everything”
or “reduce everything to one universally meaningful scalar.”

This could later inform RET evidence summaries or monitoring systems, provided
their source models, retained state, nuisance parameters and future decision
families are separately specified and validated. No RET adapter, measured
application improvement, ontology proof or observational compatibility study
has been delivered here.

The next bounded research milestone is **QR-04: record-conditioned settings
with explicit causal-past access restrictions**. It must test what an adaptive
operation is allowed to read, preserve complete quantum-plus-record outputs,
and reject dependence on unavailable or incomparable records. That remains
distinct from deriving geometry or gravity; Track-B still needs its own
record-to-order construction and scale-consistency evidence.

All additions are isolated in this directory. No RET/hardening working files,
dependency locks, shared roadmap/charter documents, prior evidence or legacy
physics modules were changed by the QR-03 work.
