# Exodus/DET8 relational endpoint tomography

**Status:** Synthetic intervention and model-selection study calibrated to the
declared 3-D apparatus surrogate. It is a DET-native methodology experiment,
not a new force prediction or a fit to Exodus measurements.

Implementation: `det8/models/exodus_relational_tomography.py`

Run:

```bash
python3 -m det8.models.exodus_relational_tomography
python3 run_tests.py
```

The first command emits the full tomography study as JSON. The second runs the
260-test DET8 suite.

---

## 1. Novel path being tested

Previous runs asked whether ordinary electrostatic boundaries can produce and
close a force. This run changes the question:

\[
\boxed{
\text{Which interventions identify the force's relational endpoint?}
}
\]

The method varies independently:

- device orientation;
- chamber orientation;
- wall distance;
- terminal common mode at fixed 40 kV difference;
- lead routing;
- preparation path.

This turns DET's instruction to expand the physical regime into an endpoint
tomography protocol. Rather than merely repeating one apparent-force
measurement, the protocol maps which relationships control each vector
component.

---

## 2. Reduced-order calibration

At fixed differential voltage, Maxwell stress is quadratic in common-mode
voltage because the electrostatic potential is linear and the stress tensor is
quadratic in the field. Quadratic response surfaces were extracted from the
grounded-return, bipolar, and high-grounded states of the same-end-lead 3-D
run.

For common mode (c) in kV and force in micronewtons:

\[
F_x(c)=
-0.0019523c^2-19.79075c-23.59704,
\]

\[
F_z(c)=
-3.21930c^2-0.81920c-441.34562.
\]

At the charge-neutral (c=-2.1145) kV state these reproduce

\[
(F_x,F_z)=(+18.242,-454.007)\ \mu\mathrm N.
\]

Wall-distance dependence is a declared inverse-square intervention shape. It
is used to test experimental discriminability, not asserted as the exact 3-D
apparatus law.

---

## 3. Candidate endpoint models

The synthetic observations are fitted by nested models:

| Model | Allowed relation |
|---|---|
| Null | No force |
| Device-internal | Constant force along the device axis |
| Common-mode only | Electrical state changes the device-axis force |
| Boundary electrode | Common mode plus wall distance |
| Lead only | Lead routing and chamber normal |
| Full relational | Boundary-electrode plus lead/chamber relations |
| Full plus Earth | Full model plus an Earth-fixed vector |
| Full plus history | Full model plus a matched-state preparation term |

The intervention grid contains 144 apparatus states and 432 scalar force
measurements. At (20\ \mu\mathrm N) Gaussian noise, conservative BIC model
selection chooses the exact full-relational model. Its recovered amplitude
coefficients are

\[
\hat a_{\rm boundary}=0.9998,
\qquad
\hat a_{\rm lead}=1.0043.
\]

The device-internal model is rejected by

\[
\Delta\mathrm{BIC}\approx2047.
\]

---

## 4. Monte Carlo endpoint recovery

Two hundred synthetic experiments were run at each force-noise level:

| Per-component noise | Relational-family selection | Exact full model, AIC | Exact full model, BIC |
|---:|---:|---:|---:|
| (5\ \mu\mathrm N) | (100\%) | (70.0\%) | (98.5\%) |
| (20\ \mu\mathrm N) | (100\%) | (74.0\%) | (97.0\%) |
| (50\ \mu\mathrm N) | (100\%) | (74.0\%) | (97.5\%) |
| (100\ \mu\mathrm N) | (100\%) | (68.5\%) | (98.0\%) |

The intervention pattern identifies the relational family even when single
measurements are noisy compared with the axial signal. But AIC adds a
nonexistent Earth or history term in roughly one quarter to one third of
trials. BIC's stronger complexity penalty reduces those false additions to
about (1.5)–(3\%).

This is a substantive DET governance result: discovering a relational
endpoint and justifying an additional novel channel are different inference
tasks. The second requires a stricter complexity gate.

---

## 5. Rotation tomography

At the neutral same-end-lead state:

| Intervention | (F_x) | (F_y) | (F_z) |
|---|---:|---:|---:|
| Reference | (+18.242) | (0) | (-454.007) |
| Rotate device only by (90^\circ) | approximately (0) | (+18.242) | (-454.007) |
| Rotate chamber only by (90^\circ) | (-435.765) | (0) | approximately (0) |
| Reverse chamber only by (180^\circ) | (+18.242) | (0) | (+454.007) |

The small axial component follows the electrode/device axis in this calibrated
model. The dominant lead load follows the chamber wall normal. Independently
rotating those relations separates them without requiring either component to
be dismissed as unreal.

An Earth-fixed candidate remains unchanged under both interventions and is
therefore separately identifiable.

---

## 6. Nested DET regime closure

The same-end floating state gives the following closure ladder:

| Regime cut | Residual norm | Conservation status |
|---|---:|---|
| Electrodes and leads only | (454.374\ \mu\mathrm N) | Fails—endpoint omitted |
| Add grounded chamber | (4.544\ \mu\mathrm N) | Passes declared grid tolerance |
| Continuum-extrapolated closed regime | (0) | Closed |

Adding the chamber improves closure by a factor of approximately 100. The
remaining base-grid residual is the already measured finite-grid transport
error; it decreases under refinement in the 3-D field run. An orphan-force
counterfactual retains the full (454.374\ \mu\mathrm N) residual and fails
the DET conservation gate.

The emerging DET role is therefore algorithmic:

1. begin with the apparent-force apparatus cut;
2. measure the vector residual;
3. add candidate relational endpoints one at a time;
4. retain the smallest experimentally supported regime that closes;
5. reject endpoint-free candidates.

---

## 7. Matched-state history audit

The original exploration proposed different voltage paths reaching the same
final state. The new simulation adds an important confound: after a finite
dwell, the two paths can retain opposite (0.30) kV common-mode errors even
though both have the same 40 kV differential voltage.

With 40 repeats per path and (3\ \mu\mathrm N) force noise:

| Scenario | Naive path difference | Naive significance | Electrically corrected difference | Corrected significance |
|---|---:|---:|---:|---:|
| Electrical memory only | (-10.947\ \mu\mathrm N) | (18.1\sigma) | (+0.896\ \mu\mathrm N) | (1.48\sigma) |
| Injected (5\ \mu\mathrm N) matched-state history | (-6.517\ \mu\mathrm N) | (9.35\sigma) | (+5.390\ \mu\mathrm N) | (7.61\sigma) |

The electrical-only case would look like a very strong history effect if only
differential voltage were recorded. Conditioning each observation on its
measured common mode removes it. Conversely, the deliberately injected
matched-state term survives the correction.

This sharpens the DET (R^-) protocol:

\[
\boxed{
\text{History is tested only in the residual after the complete present
electrical, thermal, dielectric, and mechanical state is matched.}
}
\]

---

## 8. What emerged for DET

No new force term emerged. A potentially novel DET methodology did:

### Relational Endpoint Tomography

Treat chamber geometry, electrical topology, orientation, and history as
independent interventions. Fit vector-response models, expand the regime cut
until momentum closes, and apply a conservative complexity penalty before
adding an unobserved endpoint.

This is more specific than saying that all systems are relational. It is an
executable procedure for discovering which relation carries a measured
effect—and for determining when ordinary relations are insufficient.

---

## 9. Limits and next path

The observations are synthetic and generated from the same reduced-order
model tested by the fits. The distance law is declared, noise is independent
Gaussian, and no mechanical cross-axis transfer matrix is included. The
Monte Carlo results demonstrate the information content of the intervention
design, not its success on real Exodus data.

The adaptive tomography scheduler is implemented and recorded in
`docs/EXODUS_ADAPTIVE_SCHEDULER.md`. Its next extension is a cost-aware
live-data interface connected to real force records when apparatus
measurements become available.
