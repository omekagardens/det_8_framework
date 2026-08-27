# Exodus/DET8 floating-source simulation

**Status:** Charge-constrained extension of the declared 2-D blade/flat
surrogate. It is not a reconstruction of the Exodus apparatus, an empirical
validation, or a new DET8 force prediction.

Implementation: `det8/models/exodus_floating_supply.py`

Run:

```bash
python3 -m det8.models.exodus_floating_supply
python3 run_tests.py
```

The first command emits the full floating-source run as JSON. The second runs
the 260-test DET8 suite.

---

## 1. Why this run was needed

The preceding field simulation showed that force at a fixed 40 kV electrode
difference depends strongly on the two electrodes' common-mode voltage
relative to the grounded chamber. Its bipolar case prescribed (+20/-20)
kV, however. That is a chosen voltage pair, not yet the solution for an
electrically isolated device.

An ideal floating two-terminal source fixes

\[
V_H-V_R=V_d,
\]

while the common-mode voltage must be solved from the assembly's net charge
and capacitance to its environment. For a neutral device without a parasitic
supply capacitance, the second condition is

\[
Q_H+Q_R=0.
\]

This run imposes both conditions.

---

## 2. Capacitance-matrix extraction

Two Laplace basis fields are solved on the same chamber and electrode grid:

1. (V_H=1, V_R=0);
2. (V_H=0, V_R=1).

Surface flux on the two conductors gives the Maxwell capacitance relation

\[
\begin{pmatrix}Q_H\\Q_R\end{pmatrix}
=
\begin{pmatrix}C_{HH}&C_{HR}\\C_{RH}&C_{RR}\end{pmatrix}
\begin{pmatrix}V_H\\V_R\end{pmatrix}.
\]

For the base grid and the declared 1 cm extrusion depth, the extracted matrix
is

\[
C \approx
\begin{pmatrix}
0.595662 & -0.366006\\
-0.366006 & 0.568738
\end{pmatrix}\ \mathrm{pF}.
\]

The two independently extracted mutual coefficients agree to
(2.42\times10^{-6}) relative error before symmetrization. The device
common-mode capacitance is

\[
C_{\rm common}=C_{HH}+C_{HR}+C_{RH}+C_{RR}
=0.432389\ \mathrm{pF}.
\]

At fixed (V_d), write (V_R=c) and (V_H=c+V_d). A lumped supply stray
capacitance (C_s), connected from the supply's mean-potential node to the
chamber, gives the charge constraint

\[
Q_{\rm target}
=Q_H+Q_R+C_s\frac{V_H+V_R}{2}.
\]

The code solves this linear equation for (c), then synthesizes the field
from the two basis solutions. All topology and sensitivity points therefore
share the same underlying electrostatic solution space.

---

## 3. Grounded, arbitrary bipolar, and charge-neutral topologies

All three cases retain (V_H-V_R=40) kV:

| Topology | (V_H/V_R) vs chamber | Direct device charge | Device force | Chamber force |
|---|---:|---:|---:|---:|
| Grounded return | (+40.000/0.000) kV | (+9.1862) nC | (-307.172\ \mu\mathrm N) | (+306.958\ \mu\mathrm N) |
| Prescribed bipolar | (+20.000/-20.000) kV | (+0.5385) nC | (+0.528\ \mu\mathrm N) | (-0.530\ \mu\mathrm N) |
| Floating neutral | (+18.755/-21.245) kV | (-0.000018) nC | (+20.328\ \mu\mathrm N) | (-20.317\ \mu\mathrm N) |

The important distinction is that (+20/-20) kV is not charge-neutral for
this asymmetric electrode/chamber geometry. The zero-charge solution has a
common-mode voltage of (-1.245) kV. Direct surface integration gives
(+18.94734) nC on the high electrode and (-18.94735) nC on the return.

Neutral floating operation suppresses the base-grid grounded-return force by
a factor of about 15.1, but it does not make the chamber interaction vanish.
A neutral asymmetric dipole can still exchange force with a finite conducting
boundary. In every case, independently integrated chamber pressure supplies
the opposite momentum endpoint.

---

## 4. Floating-neutral grid refinement

| Grid spacing | Common mode | Floating force | Chamber force | Closure error |
|---:|---:|---:|---:|---:|
| (4\ \mathrm{mm}) | (-1.284) kV | (+15.122\ \mu\mathrm N) | (-15.055\ \mu\mathrm N) | (0.2233\%) |
| (2\ \mathrm{mm}) | (-1.245) kV | (+20.328\ \mu\mathrm N) | (-20.317\ \mu\mathrm N) | (0.0278\%) |
| (1\ \mathrm{mm}) | (-1.298) kV | (+12.789\ \mu\mathrm N) | (-12.788\ \mu\mathrm N) | (0.00356\%) |

The common-mode solution and force sign are stable, and momentum closure
improves by nearly an order of magnitude at each refinement. The residual
floating force is a small subtraction of larger field stresses and is not
monotonically converged: the three grids span (12.8)–(20.3\ \mu\mathrm N).
It should be treated as an order-of-magnitude result. The fine-grid value is
about 25 times smaller than the fine-grid grounded-return force.

---

## 5. Net-charge sensitivity

The charge scale is the (+9.1863) nC carried by the grounded-return device
according to the capacitance matrix. The sweep changes total device charge
while retaining the 40 kV electrode difference:

| Charge fraction | Target charge | Common mode | Device force |
|---:|---:|---:|---:|
| (-0.5) | (-4.593) nC | (-11.868) kV | (+192.274\ \mu\mathrm N) |
| (-0.1) | (-0.919) nC | (-3.370) kV | (+54.280\ \mu\mathrm N) |
| (0) | (0) | (-1.245) kV | (+20.328\ \mu\mathrm N) |
| (+0.1) | (+0.919) nC | (+0.879) kV | (-13.405\ \mu\mathrm N) |
| (+0.5) | (+4.593) nC | (+9.377) kV | (-146.154\ \mu\mathrm N) |

Sub-nanocoulomb charge changes cross the force through zero and reverse its
direction in this surrogate. A practical experiment therefore needs direct
common-mode or net-charge diagnostics; differential voltage alone is
insufficient to define the electrostatic state.

---

## 6. Supply stray-capacitance sensitivity

For an otherwise neutral isolated assembly, increasing a symmetric lumped
capacitance from the supply mean node to the chamber pulls the common mode
toward the prescribed bipolar state:

| (C_s/C_{\rm common}) | (C_s) | Common mode | Device force |
|---:|---:|---:|---:|
| (0) | (0) pF | (-1.245) kV | (+20.328\ \mu\mathrm N) |
| (0.1) | (0.0432) pF | (-1.132) kV | (+18.525\ \mu\mathrm N) |
| (0.5) | (0.2162) pF | (-0.830) kV | (+13.720\ \mu\mathrm N) |
| (1) | (0.4324) pF | (-0.623) kV | (+10.419\ \mu\mathrm N) |
| (5) | (2.1619) pF | (-0.208) kV | (+3.823\ \mu\mathrm N) |

This is a deliberately simple supply model. Real cables and transformers
have separate capacitances from each terminal to the chamber, which can shift
the common mode in either direction and must be included as additional
conductors or measured circuit elements.

---

## 7. Return-leakage sensitivity

The declared leakage model lets the initially floating return relax toward
chamber ground with time constant (	au), while an ideal source preserves
40 kV differential voltage:

\[
V_R(t)=V_{R,0}e^{-t/\tau},\qquad V_H(t)=V_R(t)+40\ \mathrm{kV}.
\]

| (t/\tau) | Return voltage | Device charge | Device force |
|---:|---:|---:|---:|
| (0) | (-21.245) kV | approximately (0) | (+20.328\ \mu\mathrm N) |
| (0.1) | (-19.224) kV | (+0.874) nC | (-11.779\ \mu\mathrm N) |
| (0.5) | (-12.886) kV | (+3.614) nC | (-111.141\ \mu\mathrm N) |
| (1) | (-7.816) kV | (+5.807) nC | (-189.233\ \mu\mathrm N) |
| (2) | (-2.875) kV | (+7.943) nC | (-264.128\ \mu\mathrm N) |
| (5) | (-0.143) kV | (+9.124) nC | (-305.039\ \mu\mathrm N) |

The state approaches the (-307.172\ \mu\mathrm N) grounded-return result.
Even weak leakage can cross and reverse the force early in the charging
transient. The exponential is a boundary-condition sensitivity test, not a
measured time prediction; physical time requires the apparatus leakage
resistance and capacitance network.

---

## 8. DET8 interpretation and experimental discriminator

The floating-source run sharpens the DET ledger without introducing a new
force law:

- internal high-to-return stress remains part of the apparatus inventory;
- device-to-chamber Maxwell stress is an external relational bond;
- charge neutrality changes that bond but does not remove it;
- leakage changes the committed electrical regime and hence the chamber bond;
- the chamber always carries the opposite force within numerical closure.

The decisive experimental record should include, synchronously with force:

1. both terminal voltages relative to the chamber, not only their difference;
2. net device charge or a calibrated common-mode proxy;
3. cable, feedthrough, transformer, and supply capacitances to the chamber;
4. leakage current and the resulting (RC) time constant;
5. force or displacement at the chamber/support reaction endpoint.

A claimed isolated-device signal should remain after the measured electrical
boundary conditions are inserted into a full apparatus field model and all
external Maxwell-stress endpoints close below the force uncertainty.

---

## 9. Limits and next run

The simulation is still a 2-D, one-cell-thick conductor surrogate. It omits
the actual CAD, electrode thickness and curvature, dielectric structure,
three-dimensional cable and feedthrough fields, support forces, ion flow, and
measured circuit impedance. The lumped supply capacitance is connected to the
mean-potential node by definition rather than extracted from supply geometry.

The declared 3-D lead and terminal-capacitance follow-up is recorded in
`docs/EXODUS_3D_APPARATUS_RUN.md`. The next apparatus-specific run should
import actual conductor and dielectric CAD, include every
cable/feedthrough/supply conductor, and assign each one a measured
fixed-potential, fixed-charge, or impedance boundary condition. Until those
inputs exist, these remain discriminator studies of how ordinary
chamber-coupled force changes at the same nominal 40 kV.
