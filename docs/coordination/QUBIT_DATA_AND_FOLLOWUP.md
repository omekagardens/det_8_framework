# RI-25 — experimental data readiness and follow-up directions

14 September 2026 UTC. Coordinator companion to the user-approved
[qubit-and-record assignment](../../REVIEW_IMPLEMENTATION_PLAN.md).
The primary deliverable is an ordinary-qubit worked specification, simulator,
record format and withheld-setting prediction check. **No evaluated dataset
has yet met the measured-data requirements for that experiment.** This does
not block its independent mathematical specification or simulator.

The [complete worked qubit model](../experiments/qubit_record_v1/EXPERIMENT.md)
is independently accepted and published in verified `9f463f2`, with isolated execution and source identities
recorded in the [progress record](REVIEW_PROGRESS.md). Its simulation does not
change the measured-data readiness assessment below.

## Model choice and the experimental question

Adopt trace-one qubit states, explicitly available bounded Born effects and
specified projective updates. Fit fresh comparable preparation records in
X/Y/Z, then predict a separately acquired oblique setting
W=(0,3/5,4/5), whose outcomes are withheld until predictions are frozen.
The opposite-phase control has identical Z distributions but different Y
and W distributions. Conventional tomography receives the same training
observations and assumptions. Better numerical accuracy is not presumed.

The explicit C0 embedding connects the model to DET's accepted record work.
It does not realize the four-cell L_t apparatus, select physical QM from
ontology or turn simulator access to the true state into an observation.
The [RI-23 contract](SCALAR_VALUE_ERROR_CONTRACT.md) remains unchanged:
trace normalization and the restricted operational encoding are declared
rather than treating unrestricted quadratic probes as detector probabilities.

## Public measured-data candidate reviewed

The strongest reviewed candidate is the superconducting-qubit experiment of
Aasen, Di Giovanni and colleagues. Its methods use six Pauli calibration
states, 25 target states and X/Y/Z measurements, with Rabi/Ramsey/readout
calibration. The described protocol does not provide an additional W batch.
The paper also identifies preparation error and drift as limitations; the
review did not establish a quantified drift budget for our experiment.[^1]

The associated public KIT repository identifies a roughly 102.4 MB dataset,
DOI `10.35097/RNbuograoVUFQNBB`, with the license label **CC BY-ND 4.0**.
That is distinct from the article's license. A reviewer inspected metadata
and a bounded archive prefix identifying an embedded `DATA.zip`; the
compressed scientific payload was not inspected or imported.[^2]

| Item | Current readiness |
|---|---|
| Genuine experimental source | Identified, with public methods and dataset metadata. |
| Raw observations | Raw bit/count schema, trial order, timestamps, discarded attempts and failure accounting remain unverified. |
| Calibration evidence | Nominal procedures are described; per-run calibration records and quantitative uncertainty suitable for our bounds remain unverified. |
| Preparation correspondence | No mapping to RI-25's particular preparations and common reference sessions has been established. |
| Withheld setting | The published XYZ protocol does not establish an independently acquired W batch. |
| Redistribution | No scientific dataset or transformed fixture has been added to this repository; retain the source's actual license metadata in any later provenance review. |

The supplement describes experimental figure folders without specifying a
raw-shot record schema. Its `theory_depol` data are explicitly simulated,
so that folder cannot fill the measured-data requirement.[^3]

**Consequence of the protocol comparison:** an XYZ-only dataset cannot be
relabeled as measured W outcomes. Withholding Y from X/Z inference leaves
an unrestricted qubit's phase undetermined in general; withholding extra shots at an
already trained axis tests a different prediction question. Those may support
separate experiments, but they do not complete the frozen RI-25 question.
A larger archive download would not by itself repair the documented setting
mismatch. No experimental score or calibration result is claimed here.

A nearby Wigner-tomography experiment uses many readout angles, but its
data-availability statement says data are available on request. Neither the exact required W
coverage nor a suitable calibration payload was acquired in this review.[^4]
No provider was contacted and no account, hardware job or paid acquisition
was used. Local IBM ingestion was also reviewed: its T1/T2 summaries are not
the required tomography trial records.

## Concrete acquisition requirement

A further bounded public-data review examined two additional experimental
leads. Neither currently qualifies for the fixed RI-25 acquisition contract;
this is not a claim that the literature has been exhausted.

| Additional lead | Material inspected and remaining gap |
|---|---|
| Stricker et al., ion single-setting tomography | The experiment uses four-outcome nonorthogonal measurements. The public dataset lists five small CSVs; inspected files contain figure-level timing, fidelity and purity summaries. A raw all-attempt/calibration-linked acquisition payload was not established. This measurement interface cannot be relabeled as the binary W batch.[^8] |
| An et al., photonic self-guided/shadow tomography | The experimental SGQT control uses adaptive projective directions; the shadow apparatus uses six Pauli eigenstates. Small inspected archives contained figure spreadsheets whose scientific table schemas were not validated. Postselection, discarded detections, adaptive setting logs and applicable calibration/drift bounds leave the full acquisition contract unresolved. No fixed-W batch was established.[^9] |

Only public metadata and small payloads were inspected by the reviewer; no
scientific data were imported into this project. The adaptive oblique protocol
could inform a separately preregistered future variant if its actual settings,
observations and calibration evidence become available. It does not change
RI-25's frozen W or convert a reconstructed expectation into a measurement.

The next measured step needs X/Y/Z and independently acquired W records for
the same declared preparation/reference sessions. Preserve all attempted
trials, their acquisition order and calibration links, including missing or
failed detections. Alternative settings use fresh preparations; sequential
measurements have their own update and history contract.

Before importing a source, establish:

1. **Observable payload:** actual outcomes or explicitly labeled aggregate
   counts, total attempted acquisitions and loss/failure counts. Aggregate
   data must not be expanded into invented ordered trial histories.
2. **Preparation and setting identity:** nominal recipes, axes/frame, session
   linkage and comparability assumptions. Nominal target states are not
   independently measured ground truth.
3. **Calibration and drift:** a justified effect/probability error bound and
   preparation-reference drift bound, with their applicable window and any
   confidence allocation. A reported average fidelity or T1/T2 value does not
   automatically supply either bound.
4. **Frozen evaluation:** training/withheld split, estimator, probability band,
   sampling allowance, score and missing-data/exclusion rules fixed before
   W outcomes are revealed. Calibration fitting cannot silently consume the
   withheld outcomes.
5. **Source provenance:** original location and byte identity, actual license,
   acquisition context and any transformation lineage. A derived model value
   is not substituted for a missing observed setting.

The initial simulator can supply independent binary-read trials followed by
explicit erasure. That is one declared detection model, not a description of
every detector. Outcome-dependent erasure can be retained conservatively;
arbitrary failure/POVM mechanisms need a calibrated forward law or an explicit
refusal. Finite-count uncertainty, calibration error and preparation drift
remain separate contributions. An analytic sampling bound is conditional on
its independence/fixed-sample assumptions, not a proof of physical calibration.

Conventional linear and physical tomography are established comparison
methods.[^5] The DET-facing contribution being tested here is coherent record
formation, disciplined observer access, information-loss/refusal boundaries
and transparent measurement selection. A simulated prediction agreeing with
its generator is a functioning-model result, not measured superiority.

## Practical RET direction retained

The voltage-comparator pilot remains the practical application direction in
the [application plan](APPLICATION_WORK_PLAN.md): compare prediction and
calibration quality, uncertainty and acquisition cost on suitable data, with
conventional baselines and a frozen withheld evaluation. The existing
[publication backlog](PUBLICATION_BACKLOG.md) still records the comparator's
RET source prerequisites. The qubit task does not alter them or open a
calibration bank or a new RET implementation.

A useful measured comparator source needs actual voltage/reference records,
units, ordering/timing, instrument calibration, an agreed prediction target
and tolerance, noise/drift assumptions and acquisition cost. The currently
accepted synthetic comparator remains synthetic until those inputs exist.

## Secondary observer-and-expansion model

The [RI-26 observer/signal model](../experiments/observer_signal_v1/EXPERIMENT.md)
is independently accepted and published in verified `0fde8b2`, following
the primary qubit deliverable in `9f463f2`. It uses supplied static, expanding and contracting geometries
and explicit signal propagation to model local observers,
local clock readings, emission/reception events and inferred redshifts.
Retain the observer's accessible signals separately from global simulator
coordinates. A standard supplied geometry/propagation calculation is one
model result; it does not derive geometry from record actualization.

Any proposed actualization-to-geometry rule must specify its variables,
equations and parameters, then predict a difference in observer-accessible
quantities relative to the supplied-geometry baseline. Without such a rule,
there is no additional observable consequence to calculate. The accepted secondary
model provides a baseline for assessing such a proposal; it does not supply
a derivation of physical time, mass or gravity.

The bounded assignment supplies a flat radial metric, an exponential scale
factor with constant H (plus static control), comoving ideal clocks and null
propagation. The selected primary reference separates those standard
kinematics from the further dynamical equations.[^6] Root and a separate
reviewer derived the simple exponential arrival/frequency formulas for the
assignment. Exact horizon decisions and a finite observation cutoff must
remain distinct from local receipt records. A finite absent receipt is not
an observation of the infinite future; the Hubble radius is not treated as
a universal causal horizon.[^7]

The implementation distinguishes instantaneous frequency redshift
from finite pulse-spacing ratios, retains unknown clock offsets, and demonstrates
that the same redshift can arise from different supplied parameter pairs.
Three final reviews accepted the source. Root passed 51 isolated tests per
mode, reproduced 52 matching exports and reconciled 331 independent exported-
data checks. Source identities and publication status are in the
[progress record](REVIEW_PROGRESS.md).
There is still no supplied actualization-to-geometry feedback law.

The originating discussion assistant is not monitoring this work until the
user returns there. This coordinator retains the authorized project work,
independent review and scoped commit/push follow-through.

## Sources

[^1]: Aasen et al., [Readout error mitigated quantum state tomography tested on superconducting qubits](https://arxiv.org/html/2312.04211v2),
    sections IV.2 and V; published in [Communications Physics 7, 301 (2024)](https://www.nature.com/articles/s42005-024-01790-8).

[^2]: Di Giovanni, Rotzinger and Ustinov, [KIT dataset metadata](https://radar.kit.edu/radar/en/dataset/RNbuograoVUFQNBB),
    DOI 10.35097/RNbuograoVUFQNBB; [KITopen catalog and license metadata](https://publikationen.bibliothek.kit.edu/1000173044).
    The reviewer inspected repository metadata and an archive prefix, not the
    compressed scientific observations.

[^3]: [Article supplementary information, Note 5](https://media.springernature.com/original/springer-static/esm/art:10.1038%2Fs42005-024-01790-8/MediaObjects/42005_2024_1790_MOESM2_ESM.pdf).

[^4]: [Wigner-tomography experimental article and data-availability statement](https://link.springer.com/article/10.1007/s11128-024-04550-3).
    This is a request-only lead, not data acquired by the project.

[^5]: James et al., [On the Measurement of Qubits](https://arxiv.org/abs/quant-ph/0103121),
    for established linear and likelihood-based reconstruction. A radial Bloch
    projection is unweighted constrained least squares, not maximum likelihood.


[^6]: Carroll, [General Relativity notes, section 8](https://preposterousuniverse.com/wp-content/uploads/grnotes-eight.pdf),
    equations 8.1, 8.66–67 and 8.71–72 for metric, frequency ratio and null
    propagation; Einstein dynamics is a further step.

[^7]: Davis and Lineweaver, [Expanding Confusion](https://arxiv.org/abs/astro-ph/0310808),
    for the distinctions among cosmological horizons and the Hubble sphere.

[^8]: Stricker et al., [Experimental Single-Setting Quantum State Tomography](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.3.040310);
    [public data, DOI 10.5281/zenodo.7054827](https://zenodo.org/records/7054827).

[^9]: An et al., [Efficient Characterizations of Multiphoton States with an Ultra-thin Optical Device](https://arxiv.org/html/2308.07067v2),
    experimental sections and Supplementary Notes 3 and 5;
    [public data metadata, DOI 10.5281/zenodo.10674374](https://zenodo.org/api/records/10674374).
