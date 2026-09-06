# Quantum records to geometric structure: research plan

Started 5 September 2026. Authorized mathematical exploration in the primary
checkout, following the discussion of the standalone quantum–record calculus.
This plan does not reopen retired gravitational sources or clock couplings.

## Current status

QR-05A completed its bounded investigative gate on 5 September 2026:
117 tests passed in normal and optimized Python; eight independent exact
analyses and a create-only capture/read-only replay agree. Positive quantum
birth examples satisfy the stated comparisons, while prespecified controls
separate noncommutation, stage artifacts, noncovariant growth, and conflicts
hidden by zero weights. This does not close QR-05 as a whole.

The first concrete constraint on geometric summaries is a fork/join collision:
two nonisomorphic three-event orders have exactly the same complete quantum
payload map. Payload-only information therefore cannot reconstruct the retained
order in this model. The complete order record still distinguishes them.
See [QR-05A results](../validation/qr-05a-quantum-births-2026-09-05/RESULTS.md).

**Next executable gate: QR-05B.** Declare a hierarchy of future question
families—payload-only probes, order/count probes, and order-sensitive
continuations—then test the sufficiency and refinement behavior of candidate
summaries. Use the fork/join collision as a retained negative control. Do not
infer a spacetime metric from quantum-map equivalence.

## Outcome sought

Determine whether a single, precisely specified model of quantum operations,
classical records, and event relations can support useful scale-dependent
geometric descriptions. Ordinary quantum mechanics and general relativity
remain comparison baselines. An interpretation of geometry as presently carried
relational structure motivates the questions; it is not a premise proving them.

The first result may be a consistency theorem, a counterexample, or a rejected
summary. None requires a different physical law. A failed candidate must remain
visible rather than being described as noise or a setup artifact without evidence.

## Checkpoint and ownership

- QR-01 through QR-03 were already committed. QR-04 was replayed, committed as
  `1fac1352ffe14dbbd6227dd1806bd8f6432ba0e4`, and pushed to `origin/ret` before
  this new work began. Its 96 tests and retained exact replay passed again.
- The temporary `temp_qr.md` remains local and uncommitted. This research must
  not require that temporary file to survive.
- Existing dirty RET, core, governance, and earlier Track-B work belongs to its
  respective tracks. Do not include it in research commits or alter its sources.
- New work uses isolated research directories. No RET imports, API integration,
  dependency changes, shared acceptance-rule changes, or large compute jobs.
- Lean/Physlib was discussed, not installed or authorized as part of this first
  executable milestone. Formalization can be planned after definitions stabilize.

## Premises that must stay distinguishable

1. Quantum state, classical record, and a prediction-sufficient summary are
   different objects. A classical record alone need not determine the state.
2. An event order supplied by a model is not an observed spacetime geometry.
3. Invariance under birth labels or execution schedules is not Lorentz or
   diffeomorphism covariance.
4. Apparent history dependence is relative to a specified present description,
   future question family, and model. No universal scalar history coordinate
   or new gravitational source is assumed.
5. Coherent alternative sums and classical mixtures of orders are different.
   No superposition of event orders is silently introduced.

## Gated sequence

| Gate | Concrete question and deliverable | Acceptance boundary |
|---|---|---|
| QR-05A: joint quantum birth consistency | Grow a finite classical order while appending recorded quantum operations; compare complete quantum–record maps under birth relabeling and incomparable-birth swaps | Independent exact reference; positive, negative, and zero-weight controls; explicit distinction between source-reachable and universal intermediate checks |
| QR-05B: record and order summaries | Specify which future questions a grouped history/order representation must preserve; test candidate summaries and refinement diagrams | Summing recorded CP maps, not amplitudes; retain path multiplicity; detect predictive information lost by a proposed summary |
| QR-05C: scale consistency | Compare direct coarse descriptions with repeated fine-to-coarse descriptions across a bounded refinement family | Commuting comparison diagrams or explicit failures; track changed measurement access and context; no assumed preferred scale |
| QR-05D: geometric correspondence | On supplied generating models and non-geometric adversaries, test whether summaries preserve declared order/count and propagation-related quantities | Separate estimator accuracy from manifold emergence; state density, sampling, localization, and boundary assumptions |
| Later: physical bridge and dynamics | Define an apparatus-to-event interface; only then assess geometric interpretation and dynamical correspondence | No claim that a metric or Einstein dynamics follows from passing earlier gates; measured tests and uncertainty models require a separate protocol |

Proceed gate by gate. A mathematical failure that identifies a missing premise
can complete an investigative gate without certifying the failed construction.
Do not automatically promote a finite example to a theorem for all growth laws.

## First executable scope: QR-05A

Use at most three births and one fixed qubit payload. Each birth chooses a
precursor order ideal, appends a fresh event and binary outcome, and applies a
CP quantum outcome map. The fixed Hilbert space is deliberate: no creation of
quantum degrees of freedom, tensor-space embedding, or spacelike locality is
claimed. Multiple abstract events act on the same payload.

The positive growth law is the standard transitive-percolation rule, not a
new derivation. Its probability is independent of the record. A past-parity
policy chooses between diagonal weak measurements with different phases;
the resulting quantum maps commute in every relevant context. A second
positive case has genuinely multi-Kraus outcome maps.

Controls will deliberately separate:

- classical growth normalization from birth covariance;
- past-local reads from quantum commutation;
- stage-dependent setting artifacts from genuine event dependence;
- weighted equality from conflicts hidden by zero growth probabilities;
- complete residual quantum maps from immediate outcome probabilities.

Retain every naturally labeled path before grouping by isomorphism. Include
settings as well as outcomes in comparisons. Count each path once; no blind
factorial or automorphism multiplication. Preserve every zero branch.

The detailed protocol, implementation, independent reference, tests, and
retained result will be confined to
`docs/validation/qr-05a-quantum-births-2026-09-05/`.

## Mathematical motivation and later interpretation

QR-04 establishes a finite fixed-order adaptive composition contract. Existing
T8 work establishes different, classical growth contracts. A joint quantum
birth construction is a new bridge between them, not a result obtained merely
by placing the modules side by side. Record-dependent growth is a later
extension, and coherent sums over orders would be a separate construction.

Only after grouping/refinement tests should we ask whether a stable summary
acts like geometry. Similarity of future predictions is not itself spacetime
distance. The interpretation sought is useful relational structure, not an
identity between a stored archive and everything presently real.

Background: [quantum-record charter](../QUANTUM_RECORD_STRUCTURE_RESEARCH.md),
[Track-B gravity](gravity.md), [classical order/record growth](covariant_record_growth.md),
[Rideout–Sorkin classical sequential growth](https://arxiv.org/abs/gr-qc/9904062).
The mutable local Track-B notes are conceptual context, not executable
dependencies or imported evidence for this gate.
