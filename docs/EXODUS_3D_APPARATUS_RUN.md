# Exodus/DET8 3-D apparatus simulation

**Status:** Parameterized three-dimensional discriminator. This is not measured
Exodus CAD, an empirical validation, or a new DET8 force prediction.

Implementation: `det8/models/exodus_apparatus_3d.py`

Run:

```bash
python3 -m det8.models.exodus_apparatus_3d
python3 run_tests.py
```

The first command emits the complete run as JSON. The second runs the 260-test
DET8 suite.

---

## 1. Question addressed

The preceding floating-source run treated the electrode pair in a 2-D
cross-section and represented supply capacitance with lumped elements. This
run asks what changes when the electrode depth and terminal leads become
explicit three-dimensional conductors.

The primary discriminator is no longer only axial force. A lead approaching a
grounded wall can carry a much larger wall-normal load that enters a balance
through supports, cable stiffness, or geometric cross-coupling.

---

## 2. Declared apparatus

The base surrogate contains:

- a (16.0\times12.0\times10.4\ \mathrm{cm}) grounded chamber;
- (4\ \mathrm{mm}) cubic finite-difference cells;
- a (5.2\ \mathrm{cm})-high, (2.8\ \mathrm{cm})-deep blade/flat pair;
- three (1.2\ \mathrm{cm}) blades and a (1.2\ \mathrm{cm}) closest gap;
- one-cell terminal leads routed toward a chamber end wall;
- a resolved (1.6\ \mathrm{cm}) lead-to-wall clearance;
- a fixed 40 kV terminal difference.

The solver applies red-black SOR to

\[
\nabla^2V=0
\]

on the three-dimensional dielectric grid. Two unit-voltage basis solutions
give the conductor capacitance matrix and synthesize arbitrary common-mode
states. Device force is integrated from the Maxwell stress tensor on a closed
surface surrounding all internal conductors. Grounded-chamber pressure is
integrated independently as the reaction endpoint.

For the same-end lead geometry, the extracted base-grid capacitance matrix is

\[
C\approx
\begin{pmatrix}
3.01739 & -1.09263\\
-1.09263 & 2.64931
\end{pmatrix}\ \mathrm{pF},
\]

with common-mode capacitance (3.48144\ \mathrm{pF}). The independently
extracted mutual coefficients agree to (3.40\times10^{-6}) relative error.

---

## 3. Electrical topology with same-end leads

| Topology | Common mode | Device charge | Axial (F_x) | Wall-normal (F_z) |
|---|---:|---:|---:|---:|
| Grounded return, (+40/0) kV | (+20.000) kV | (+76.990) nC | (-420.193\ \mu\mathrm N) | (-1745.450\ \mu\mathrm N) |
| Prescribed bipolar, (+20/-20) kV | (0) | (+7.361) nC | (-23.597\ \mu\mathrm N) | (-441.346\ \mu\mathrm N) |
| Floating neutral, (+17.885/-22.115) kV | (-2.115) kV | approximately (0) | (+18.242\ \mu\mathrm N) | (-454.007\ \mu\mathrm N) |

The three-dimensional neutral common mode is again not the arbitrary bipolar
state. More importantly, the explicit lead-to-wall force is approximately 25
times larger than the axial floating force on the base grid. The chamber
carries the opposite vector reaction: for the neutral case it receives
((-18.183,0,+449.464)\ \mu\mathrm N), with (0.503\%) global closure error.

The large (F_z) is ordinary electrostatic attraction to the chamber. Whether
it contaminates an axial balance depends on support compliance, cable routing,
and alignment—features that a two-dimensional axial model cannot represent.

---

## 4. Lead-routing discriminator

The electrode geometry, chamber, voltage, and zero-charge constraint are held
fixed while only terminal routing changes:

| Lead routing | Common mode | (F_x) | (F_z) | Closure error |
|---|---:|---:|---:|---:|
| No explicit leads | (-2.556) kV | (+19.979\ \mu\mathrm N) | approximately (0) | (0.161\%) |
| Both leads toward same end | (-2.115) kV | (+18.242\ \mu\mathrm N) | (-454.007\ \mu\mathrm N) | (0.503\%) |
| Leads toward opposite ends | (-2.097) kV | (+18.044\ \mu\mathrm N) | (+48.328\ \mu\mathrm N) | (0.902\%) |

Lead routing barely changes the axial floating force in this declared
geometry, but changes the wall-normal force from zero to hundreds of
micronewtons and can reverse its sign. Opposite-end routing reduces the
same-end transverse load by a factor of about 9.4.

This is a direct experimental discriminator: rerouting a cable while keeping
the electrode pair fixed should not change a device-internal thrust law, but
it should change chamber-coupled Maxwell stress.

---

## 5. Grid refinement

| Grid spacing | Floating common mode | (F_x) | (F_z) | Closure error |
|---:|---:|---:|---:|---:|
| (5\ \mathrm{mm}) | (-1.535) kV | (+43.659\ \mu\mathrm N) | (-689.432\ \mu\mathrm N) | (1.849\%) |
| (4\ \mathrm{mm}) | (-2.115) kV | (+18.242\ \mu\mathrm N) | (-454.007\ \mu\mathrm N) | (0.503\%) |
| (3\ \mathrm{mm}) | (-1.997) kV | (+14.701\ \mu\mathrm N) | (-338.976\ \mu\mathrm N) | (0.183\%) |

Momentum closure improves monotonically. The force magnitudes are not fully
converged because a one-cell lead is a voxelized wire whose effective radius
changes with grid spacing. The robust statements are the force directions,
the dominance of the wall-normal lead load, and the chamber reaction—not the
last reported micronewton. A geometry-converged result requires an actual lead
radius and a body-fitted or substantially finer mesh.

---

## 6. Separate terminal-capacitance imbalance

The earlier floating model attached a lumped capacitance to the supply mean
node. The 3-D circuit layer instead allows independent capacitances (C_H)
and (C_R) from the high and return terminals to chamber ground:

\[
Q_{\rm assembly}=Q_H+Q_R+C_HV_H+C_RV_R=0.
\]

For (C_H+C_R=C_{\rm common}), changing the fraction on the high terminal
gives:

| (C_H/(C_H+C_R)) | Common mode | (F_x) | (F_z) |
|---:|---:|---:|---:|
| (0) | (+8.943) kV | (-200.737\ \mu\mathrm N) | (-706.128\ \mu\mathrm N) |
| (0.25) | (+3.943) kV | (-101.657\ \mu\mathrm N) | (-494.620\ \mu\mathrm N) |
| (0.50) | (-1.057) kV | (-2.675\ \mu\mathrm N) | (-444.078\ \mu\mathrm N) |
| (0.75) | (-6.057) kV | (+96.209\ \mu\mathrm N) | (-554.501\ \mu\mathrm N) |
| (1) | (-11.057) kV | (+194.996\ \mu\mathrm N) | (-825.889\ \mu\mathrm N) |

Capacitance imbalance reverses the axial force at unchanged differential
voltage and zero total assembly charge. Even the nominally balanced external
capacitance does not enforce exactly zero common mode because the apparatus's
intrinsic terminal capacitances are unequal.

---

## 7. Leakage-path discriminator

At fixed 40 kV differential, the DC endpoint is selected by which terminal
leaks to the chamber:

| Leakage path | Endpoint (V_H/V_R) | (F_x) | (F_z) |
|---|---:|---:|---:|
| Return only | (+40/0) kV | (-420.193\ \mu\mathrm N) | (-1745.450\ \mu\mathrm N) |
| Symmetric | (+20/-20) kV | (-23.597\ \mu\mathrm N) | (-441.346\ \mu\mathrm N) |
| High only | (0/-40) kV | (+371.437\ \mu\mathrm N) | (-1712.682\ \mu\mathrm N) |

For return-only leakage, the time-dependent model relaxes from the neutral
state to grounded return using normalized time (t/\tau):

| (t/\tau) | Common mode | Device charge | (F_x) | (F_z) |
|---:|---:|---:|---:|---:|
| (0) | (-2.115) kV | approximately (0) | (+18.242\ \mu\mathrm N) | (-454.007\ \mu\mathrm N) |
| (0.1) | (-0.010) kV | (+7.327) nC | (-23.398\ \mu\mathrm N) | (-441.338\ \mu\mathrm N) |
| (0.5) | (+6.587) kV | (+30.293) nC | (-154.041\ \mu\mathrm N) | (-586.417\ \mu\mathrm N) |
| (1) | (+11.865) kV | (+48.667) nC | (-258.680\ \mu\mathrm N) | (-904.236\ \mu\mathrm N) |
| (2) | (+17.007) kV | (+66.571) nC | (-360.746\ \mu\mathrm N) | (-1386.436\ \mu\mathrm N) |
| (5) | (+19.851) kV | (+76.472) nC | (-417.232\ \mu\mathrm N) | (-1726.212\ \mu\mathrm N) |

The path choice changes the sign of the axial endpoint; it is not enough to
quote a single leakage resistance without identifying which conductor and
which grounded structure close the circuit.

---

## 8. DET8 momentum ledger

The 3-D simulation adds no anomalous coupling. Its DET translation is:

- electrode-to-electrode stresses are internal apparatus bonds;
- electrode and lead stresses terminating on the chamber are external bonds;
- terminal capacitance and leakage determine which relational electrical
  regime is committed;
- chamber pressure supplies the opposite three-vector momentum endpoint;
- no endpoint-free apparatus momentum appears.

The lead-routing result is especially important because a force component not
aligned with the nominal thrust axis can enter the readout through ordinary
mechanical cross-coupling. A complete experiment needs a vector force budget,
not only a scalar axial trace.

---

## 9. Limits and next inputs

This model still uses voxelized one-cell leads and zero-thickness conductor
surfaces. It omits actual CAD, rounded wire radii, insulating feedthroughs,
dielectric supports, cable shields, the external supply enclosure, mechanical
stiffness, ion transport, and measured impedance. The refinement sweep shows
that the lead force remains mesh-sensitive.

The next apparatus-specific run requires:

1. chamber, electrode, lead, shield, and feedthrough CAD or measured
   dimensions;
2. dielectric constants and loss/leakage data for every support and
   feedthrough;
3. separate terminal-to-chamber capacitance measurements;
4. support stiffness and force-sensor cross-axis calibration;
5. synchronized terminal voltage, leakage current, and vector force traces.

Without those inputs, further geometric precision would be precision about
the declared surrogate rather than about the reported device. The DET-native
intervention follow-up is recorded in
`docs/EXODUS_RELATIONAL_TOMOGRAPHY.md`.
