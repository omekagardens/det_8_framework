# Exodus/DET8 geometry-aware electrostatic field run

**Status:** Parameterized 2-D surrogate. This is not a reconstruction of the
Exodus article, an empirical validation, or a new DET8 force prediction.

Implementation: `det8/models/exodus_field_solver.py`

Run:

```bash
python3 -m det8.models.exodus_field_solver
python3 run_tests.py
```

The first command emits the complete field-run results as JSON. The second
runs the 260-test DET8 suite.

---

## 1. Geometry and numerical method

The patent drawings show a shaped/bladed electrode facing a flatter return,
but they do not supply enough dimensions and field data to reconstruct the
reported test article. The declared surrogate uses:

- a \(16\times12\ \mathrm{cm}\) grounded rectangular chamber;
- a \(5\ \mathrm{cm}\)-high high-voltage spine;
- three \(1.2\ \mathrm{cm}\) blades pointing toward a flat return;
- a \(1.0\ \mathrm{cm}\) closest electrode gap;
- a \(1.0\ \mathrm{cm}\) extrusion depth;
- a base grid spacing of \(2\ \mathrm{mm}\).

The solver applies red-black successive over-relaxation to

\[
\nabla^2V=0
\]

in the dielectric region. The electric field is

\[
\mathbf E=-\nabla V,
\]

and force is obtained from the electrostatic Maxwell stress tensor

\[
T_{ij}=\epsilon_0
\left(E_iE_j-\frac12\delta_{ij}E^2\right).
\]

Stress is integrated around separate electrode contours, a complete-device
contour, and an outer contour adjacent to the chamber. Normal electric
pressure is also integrated independently on the grounded chamber. Agreement
between the transported device force and chamber pressure is the numerical
momentum-closure test.

---

## 2. Centered 40 kV result

For the base grid with the return electrode and chamber both grounded:

| Quantity | Axial force |
|---|---:|
| High-electrode contour | \(+19.696\ \mathrm{mN}\) |
| Return-electrode contour | \(-20.172\ \mathrm{mN}\) |
| Device force transported through outer contour | \(-307.172\ \mu\mathrm N\) |
| Independently integrated chamber force | \(+306.958\ \mu\mathrm N\) |
| Global residual | \(-0.214\ \mu\mathrm N\) |

The internal electrode loads are about \(20\ \mathrm{mN}\) and mostly cancel.
The surviving apparatus force is paired with the chamber, not orphaned.
Base-grid closure error is \(0.0349\%\).

The numerical magnitude is close to the patent's reported
\(237\ \mu\mathrm N\), but this is not a successful prediction: the surrogate
dimensions were chosen for numerical transparency, not taken from the article,
and the result changes strongly with chamber and source topology.

---

## 3. Grid refinement

| Grid spacing | Device force | Chamber force | Closure error |
|---:|---:|---:|---:|
| \(4\ \mathrm{mm}\) | \(-356.250\ \mu\mathrm N\) | \(+354.290\ \mu\mathrm N\) | \(0.2758\%\) |
| \(2\ \mathrm{mm}\) | \(-307.172\ \mu\mathrm N\) | \(+306.958\ \mu\mathrm N\) | \(0.0349\%\) |
| \(1\ \mathrm{mm}\) | \(-320.321\ \mu\mathrm N\) | \(+320.293\ \mu\mathrm N\) | \(0.00443\%\) |

The fine-grid force differs from the base value by \(4.28\%\), while momentum
closure improves by nearly an order of magnitude at each refinement. The sign,
boundary attachment, and order of magnitude are stable; quoting better than a
few-percent geometric accuracy would not be justified.

---

## 4. Translation through the chamber

The electrode geometry is held fixed while its center moves horizontally
inside the same chamber:

| Center from left wall | Device force | Chamber reaction | Closure error |
|---:|---:|---:|---:|
| \(4.2\ \mathrm{cm}\) | \(-3.159\ \mathrm{mN}\) | \(+3.157\ \mathrm{mN}\) | \(0.0223\%\) |
| \(6.0\ \mathrm{cm}\) | \(-963.730\ \mu\mathrm N\) | \(+963.128\ \mu\mathrm N\) | \(0.0312\%\) |
| \(8.0\ \mathrm{cm}\) | \(-307.172\ \mu\mathrm N\) | \(+306.958\ \mu\mathrm N\) | \(0.0349\%\) |
| \(10.0\ \mathrm{cm}\) | \(-99.990\ \mu\mathrm N\) | \(+99.927\ \mu\mathrm N\) | \(0.0315\%\) |
| \(11.8\ \mathrm{cm}\) | \(-16.752\ \mu\mathrm N\) | \(+16.845\ \mu\mathrm N\) | \(0.2768\%\) |

The force changes by a factor of about 189 without changing the internal
electrode geometry or voltage. That behavior is incompatible with a purely
device-internal thrust law and characteristic of chamber coupling.

---

## 5. Orientation reversal

Mirroring the blade/flat geometry about the chamber center gives

\[
F_x^{\rm forward}=-307.172\ \mu\mathrm N,
\qquad
F_x^{\rm reversed}=+307.172\ \mu\mathrm N.
\]

The chamber forces reverse with them. Transverse force remains zero to
numerical precision. Geometry controls the direction, but the chamber carries
the reaction.

---

## 6. Chamber-size sweep

The device remains centered while the chamber expands:

| Chamber width | Chamber height | Device force |
|---:|---:|---:|
| \(12\ \mathrm{cm}\) | \(10\ \mathrm{cm}\) | \(-754.624\ \mu\mathrm N\) |
| \(16\ \mathrm{cm}\) | \(12\ \mathrm{cm}\) | \(-307.172\ \mu\mathrm N\) |
| \(20\ \mathrm{cm}\) | \(14\ \mathrm{cm}\) | \(-154.150\ \mu\mathrm N\) |

Increasing the relational boundary reduces the net device force even though
the electrode pair is unchanged.

---

## 7. Voltage scaling

The same converged field map rescales exactly as \(V^2\):

| Differential voltage | Device force |
|---:|---:|
| \(20\ \mathrm{kV}\) | \(-76.793\ \mu\mathrm N\) |
| \(40\ \mathrm{kV}\) | \(-307.172\ \mu\mathrm N\) |
| \(60\ \mathrm{kV}\) | \(-691.137\ \mu\mathrm N\) |

This demonstrates why \(V^2\) scaling alone cannot distinguish anomalous
propulsion from ordinary electrostatic boundary force.

---

## 8. Power-source topology at fixed differential voltage

The base-grid common-mode sweep keeps

\[
V_{\rm high}-V_{\rm return}=40\ \mathrm{kV}
\]

while changing both electrodes' voltage relative to the grounded chamber:

| High / return relative to chamber | Device force |
|---|---:|
| \(0/-40\ \mathrm{kV}\) | \(+327.595\ \mu\mathrm N\) |
| \(+20/-20\ \mathrm{kV}\) | approximately \(0.55\ \mu\mathrm N\) on the base grid |
| \(+40/0\ \mathrm{kV}\) | \(-307.172\ \mu\mathrm N\) |
| \(+60/+20\ \mathrm{kV}\) | \(-595.541\ \mu\mathrm N\) |

Because the bipolar force is a small difference, its base-grid sign is not
numerically stable. The fine-grid bipolar result is

\[
F_x=-7.497\ \mu\mathrm N,
\]

compared with \(-320.321\ \mu\mathrm N\) for the fine-grid grounded-return
case. Bipolar operation therefore suppresses the boundary force by a factor of
about 42.7 in this surrogate while maintaining the same electrode difference.

This is the most important geometry-run result:

\[
\boxed{
F\neq f(\Delta V,\text{internal geometry})\ \text{alone};
\quad
F=f(V_{\rm common},\text{chamber boundary},\text{geometry}).
}
\]

The apparent thrust follows the device-to-chamber relation. A test powered by
an externally referenced high-voltage supply and grounded return is not an
isolated-device test.

---

## 9. DET8 interpretation

The field solve gives explicit content to the DET bond ledger:

- high-to-return stress is predominantly internal and cancels within the
  apparatus;
- high/return-to-chamber stress is an external bond;
- the chamber records the opposite committed momentum;
- no endpoint-free member of \(\Omega\) is required.

This does not prove that every reported Exodus signal is a chamber artifact.
It proves that a patent-like asymmetric field geometry readily produces a
same-scale, \(V^2\), polarity-insensitive signal through an ordinary external
electrostatic endpoint unless common-mode voltage and chamber reaction are
measured.

---

## 10. Limits and next inputs

The surrogate omits:

- the actual CAD dimensions and electrode thicknesses;
- spatially varying dielectric permittivity;
- three-dimensional end effects;
- cables, supports, feedthroughs, coatings, and charge leakage;
- detailed three-dimensional supply and cable capacitances;
- measured voltage and force time series.

The charge-constrained 2-D follow-up is recorded in
`docs/EXODUS_FLOATING_SUPPLY_RUN.md`. The next apparatus-specific run should
import an actual 2-D field slice or 3-D CAD mesh and specify each conductor's
electrical boundary condition: fixed
potential, floating with fixed net charge, grounded, or connected through a
measured supply impedance. Without those distinctions, "40 kV" does not define
the relational regime.
