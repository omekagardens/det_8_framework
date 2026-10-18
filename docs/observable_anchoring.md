# DET v8.0 — Observable Anchoring

**The discipline that keeps DET from treating an inference, a formal object, or an interpretation as a direct observation.**

## 1. The four-level evidence ladder

DET is an ontology, not a license to relabel theoretical objects as things an instrument directly records. Every empirical claim must therefore show its full evidence chain:

| Level | What belongs here | Examples | Epistemic role |
|---|---|---|---|
| **1. Instrument record** | A registered output together with its acquisition context | detector channel and outcome, local timestamp, ADC count, image pixel, beat note, interferometer readout, apparatus setting, calibration record | The direct empirical anchor |
| **2. Derived empirical quantity** | A quantity inferred from records by a stated analysis and uncertainty model | differential acceleration, frequency ratio, arrival-time delay, lensing angle, strain, correlation value, recovery time | Empirical, but conditional on calibration, localization, synchronization, preprocessing, and statistical assumptions |
| **3. Formal representation** | Mathematics used to organize or predict Levels 1–2 | \(g_{\mu\nu}\), curvature, \(J^-(e)\), ADM constraints, a Hilbert space, \(\mathfrak D\), \(K\), a causal set, sprinkling density | Never a raw observation; it may be derived within DET or borrowed from an external theory |
| **4. Interpretation / ontology** | A claim about what the formal representation means or what reality is | fact genesis, open becoming, block universe, many worlds, metric-as-record, one relational openness | Status M unless and until a predeclared observable discriminator exists |

Only Level 1 is directly observed. Level 2 is empirically warranted only through a documented inference chain. Level 3 may be extremely well supported and predictively successful without becoming an observation. Level 4 does not inherit empirical confirmation merely because it leaves a successful Level-3 model unchanged.

The failure mode is not only an interpretation entering as a measured fact. It is any upward step in the ladder being left implicit.

## 2. What DET may call an anchor

### 2.1 Instrument records

An anchor should name a record specific enough that an independent analyst could identify the acquisition process:

| Record class | Examples of the registered record |
|---|---|
| Outcome record | detector channel, pointer value, trial label, apparatus setting |
| Timing record | local clock reading, trigger edge, oscillator count, synchronization log |
| Imaging record | pixel values, exposure metadata, point-spread calibration |
| Mechanical record | accelerometer output, displacement readout, force-sensor voltage |
| Spectral record | frequency-bin counts, beat frequency, line-center fit inputs |
| Materials record | load/displacement samples, temperature log, specimen geometry |

Calibration constants, uncertainty estimates, exclusions, and preprocessing choices travel with the record. A phrase such as “causal structure was observed” is not a Level-1 description.

### 2.2 Derived empirical quantities

The following can legitimately be empirical anchors, but they are not direct observables in the narrow sense:

| Quantity | Required inference bridge |
|---|---|
| \(E_{xy}\), CHSH, \(B\) | trial selection, setting/outcome coding, coincidence rule, statistical estimator |
| \(I_2\), \(I_3\) | intensity records, background subtraction, normalization, uncertainty propagation |
| \(\tau(T)\), \(\sigma\), \(A\) | operational definitions, fitted response model, sampling and uncertainty model |
| \(\nu_A/\nu_B\) | oscillator records, transfer/synchronization model, systematic corrections |
| Differential acceleration | position/phase records, instrument response and dynamical fit |
| Arrival delay, strain, lensing angle | timing or imaging records plus localization, propagation, and source/instrument models |

DET must identify both the registered records and the bridge used to obtain the reported quantity.

### 2.3 Two especially important non-observables

- **Causal order \(\prec\).** Raw records may contain local timestamps, source/detector locations, signal detections, and precedence relations defined by the apparatus. Relativistic causal order is inferred using event-localization, synchronization, and signal-propagation assumptions. In a synthetic causal-set calculation it is an input formal structure, not an observed quantity.
- **Count \(\#\).** A count of registered detector events is a Level-1 record when the counting rule and detector efficiency are declared. A fundamental spacetime-event count, sprinkling density, or identification of count with Lorentzian volume is Level 3. It is not licensed by the existence of laboratory event counts.

These distinctions apply directly to T7 and to the gravity note.

## 3. Formalism audit: derived versus borrowed

Every Level-3 object must say whether it is derived from DET premises, fitted to records, or imported as a premise.

| Formal object | Role in DET | Classification requirement |
|---|---|---|
| Pair-kernel \(\mathfrak D\), commit kernel \(K\) | candidate DET dynamics | State the record inputs, axioms, fitted quantities, and any theorem actually proved |
| Gram vectors / Hilbert representation | spectral representation of \(\mathfrak D\) | `MATH` if obtained by theorem; this does not make Hilbert space an observation |
| NPA moment matrix, TLM/Masanes inequalities | correlation tests | Borrowed `MATH/CORR`, tied to derived correlation estimates |
| Fisher–Rao \(\kappa\) | coordinate on a fitted family of history-conditioned kernels | `FIT/CORR` unless a stronger derivation is supplied |
| \(g_{\mu\nu}\), curvature, \(J^-(e)\), ADM/Wheeler–DeWitt structures | gravitational representation | Borrowed from GR or quantum-gravity formalisms; not DET observations or DET derivations |
| Causal-set sprinkling, order-volume map, Myrheim–Meyer estimator | synthetic reconstruction scaffold | Borrowed `MATH/CORR`; successful recovery on generated data is an internal estimator test |

“Derived” means that a stated conclusion follows from declared inputs. It does not mean the inputs themselves were directly observed, and it does not establish the conclusion's ontological interpretation.

## 4. Ontology audit

Every Level-4 claim must carry (a) its Level-1/2 empirical interface, if any, (b) the Level-3 formalism through which it is discussed, (c) its Status-M excess, and (d) any independent discriminator.

| Ontology claim | Empirical interface | Formal representation | Status |
|---|---|---|---|
| “commit = fact genesis” | definite registered outcomes | \(X_e\), \(K\) | **M**; “genesis” is the reading |
| “history = mutable structural carrying” | recovery records and fitted kinetics | \(R\), fitted \(\kappa\) | **M**; “mutable carrying” is the reading |
| “superposition = open relational constraint” | interference records and derived \(I_2,I_3\) | \(\mathfrak D\) / Hilbert representation | **M** for “open” and “real relation” |
| “only the present is actual” | no unique empirical interface | causal/temporal formalisms | **M** |
| “open becoming” | outcome statistics shared with rival interpretations | \(K\), quantum formalism | **M; F8-OPEN has no unique discriminator** |
| “amplitudes are real” | interference records shared with epistemic readings | amplitude or pair-kernel formalism | **M**; realism is an ontological choice |
| “metric = coarse-grained record” | gravity records already modeled by the adopted GR baseline | GR metric plus causal-set scaffold | **M**; neither observed nor currently derived by DET |
| “time, quantum, and gravity express one openness” | none unique | heterogeneous borrowed formalisms | **M, quarantined from physical inference** |
| “agency = present enactment” | none | none | **M, quarantined** |
| “healing / grace / jubilee” | none | none | **M/H, quarantined** |

## 5. The no-sneak test

For every claim, ask three separate questions:

1. **Internal derivation:** Does the claim follow from declared premises and borrowed mathematics?
2. **Empirical contact:** What instrument records and inference procedure test it?
3. **Ontological discrimination:** What predeclared observation would distinguish this interpretation from empirically equivalent rivals?

The answers must not substitute for one another:

- An internal theorem can support mathematical consistency without supplying an empirical discriminator.
- Compatibility inherited from an unchanged external theory is not independent evidence for DET's ontology.
- A successful synthetic recovery test can validate an estimator on its generating model without showing that nature is generated by that model.
- No unique discriminator means **Status M**, even when the interpretation is coherent or fruitful.

This generalizes the F8-OPEN rule. A claim with no disclosed evidence chain and no Status-M flag is an interpretation wearing the formalism's authority.

## 6. Model baselines are choices, not observations

The retired \(\kappa\)-gravity program is the working precedent:

- **Retired:** \(\kappa\) as a new gravitational source or conformal field.
- **Current baseline:** DET leaves gravitational predictions to unmodified GR and leaves source modeling to explicitly declared conventional matter/energy models.

“Standard GR” and “standard dark-matter model” are baseline modeling choices. They are not direct observations, and observational agreement with those models does not confirm DET's interpretation of the metric.

## 7. Required claim record

Any new DET physical or ontological claim should record:

1. **Instrument records:** acquisition, calibration, uncertainty, and exclusions.
2. **Derived quantity:** estimator and assumptions linking records to the quantity.
3. **Formal dependence:** DET-derived, fitted, or borrowed; list the imported physical premises.
4. **Interpretive excess:** the Status-M content stated in one sentence.
5. **Independent discriminator:** a predeclared observable difference from named alternatives, or `none currently known`.
6. **Promotion type:** internal derivational support, empirical correspondence, empirical novelty, and ontological discrimination are reported separately.

T7 is governed by this record: it may gain internal derivational support by passing tests on synthetic sprinklings, but that cannot promote “metric = record” from Status M to a physical result.

**See also:** `ONTOLOGY.md` §4/§6, `MODEL_CARD.md`, `FALSIFICATION_LEDGER.md`, `docs/record_kernel_physics.md` §6, `docs/track_b/gravity.md`, and `archive/retired_kappa_gravity.md`.
