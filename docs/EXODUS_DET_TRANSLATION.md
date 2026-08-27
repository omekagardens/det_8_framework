# Exodus electrostatic-pressure equations in DET8

**Status:** Governed research sandbox; not a DET8 prediction and not evidence
that the reported Exodus force is physical.

**Primary source:** C. R. Buhler IV, *System and method for generating forces
using asymmetrical electrostatic pressure*,
[US 11,511,891 B2](https://patents.google.com/patent/US11511891B2/en).

**Reference electrodynamics:** MIT OpenCourseWare,
[*Electromagnetics and Applications*, section 5.2](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/d3be4ea78b036a6362230fb41780cf54_MIT6_013S09_notes.pdf)
and [*Forces in Electric Field Systems*, section 8.3](https://ocw.mit.edu/courses/res-6-003-electromechanical-dynamics-spring-2009/emd_part2.pdf).

Implementation: `det8/models/exodus_simulation.py`

Run:

```bash
python3 -m det8.models.exodus_simulation
python3 run_tests.py
```

The first command emits the full simulation result as JSON. The second runs
the 260-test DET8 suite, including the Exodus translation, phase-2
discriminator, and geometry-aware field tests.

---

## 1. What was translated

The patent begins with a center-of-mass energy expression

\[
0=\frac12 Mv^2+U, \tag{1}
\]

and rewrites it as

\[
Mv=-\frac{2U}{v}. \tag{2}
\]

After replacing \(v\) with \(dx/dt\), imposing stationarity on the
energy-time product, and inserting the electrostatic field energy

\[
U=\frac{\epsilon_0}{2}\int E^2\,d\tau, \tag{6}
\]

the patent arrives at

\[
P(t)=Mv=\epsilon_0t
\left(E_2^2A_2-E_1^2A_1\right), \tag{10}
\]

and, for a static field,

\[
F=\frac{dP}{dt}=\epsilon_0
\left(E_2^2A_2-E_1^2A_1\right). \tag{11}
\]

The code implements equation (11) exactly as written:

```python
F_patent = epsilon_0 * (E2**2 * A2 - E1**2 * A1)
```

The patent's time-varying extension is

\[
P(t)=\epsilon_0tD(t),
\qquad
D(t)=E_2^2(t)A_2-E_1^2(t)A_1, \tag{12}
\]

so direct differentiation gives

\[
F(t)=\epsilon_0\left[D(t)+t\dot D(t)\right]. \tag{13}
\]

Equations (12) and (13) are also implemented literally, with the derivative
evaluated rather than approximated.

The patent reports about \(237\ \mu\mathrm N\) in one test sequence with a
power supply capable of \(+40\ \mathrm{kVDC}\), but does not publish enough
dimensions and field-map values to reconstruct that test article. The code
therefore uses a clearly labeled *effective calibration geometry*: two
\(1\ \mathrm{cm^2}\) patches separated by \(1\ \mathrm{cm}\), with one field
gain fitted to reproduce \(237\ \mu\mathrm N\) at \(40\ \mathrm{kV}\). This is
a formula test fixture, not a physical reconstruction.

---

## 2. DET8 translation

| Exodus quantity | DET8 representation | Meaning |
|---|---|---|
| Electrode or selected surface region | Node/regime \(G_i\) | The local record carrying field and geometry data |
| Field-mediated interaction | Bond \(\sigma_{ij}\) | A relation between two physical endpoints |
| Pressure impulse | Bond momentum \(\pi_{ij}\) | Required antisymmetry \(\pi_{ij}=-\pi_{ji}\) |
| Apparatus surface sum | A cut through the bond network | May be locally nonzero without being globally closed |
| Candidate reaction endpoint | Member of \(\Omega\) | Internal support, external boundary, or no endpoint |
| Conservation law | Constraint \(\mathcal C\) | Rejects nonzero global momentum residual |
| Charging/conditioning history | Optional \(\kappa\) record | A sensitivity ansatz only; never a force source |

For an apparent impulse \(J=F\Delta t\), the simulator constructs three
candidate closures:

### Internal endpoint

\[
\Delta p_{\rm patch}=+J,
\qquad
\Delta p_{\rm apparatus\ remainder}=-J.
\]

The local stress is nonzero, but

\[
\Delta p_{\rm apparatus}=0.
\]

This is ordinary internal electrostatic loading.

### External boundary endpoint

\[
\Delta p_{\rm apparatus}=+J,
\qquad
\Delta p_{\rm environment}=-J.
\]

The apparatus can move, but only because a broader relational regime carries
the opposite momentum. This is the DET-native boundary hypothesis.

### No endpoint

\[
\Delta p_{\rm apparatus}=+J,
\qquad
\Delta p_{\rm rest}=0.
\]

The global residual is \(+J\). DET8's conservation gate rejects this member of
\(\Omega\). Calling the missing term a field, vacuum, or relational substrate
does not repair the model; the endpoint must acquire a measurable state and an
opposite momentum entry.

This gives the central DET result:

\[
\boxed{
\text{local pressure imbalance}
\not\Rightarrow
\text{closed-apparatus thrust}
}
\]

Instead, the imbalance is either internal, externally attached, or an
incomplete momentum ledger.

---

## 3. Equation audit

### 3.1 Equation (11) is a selected-patch expression

The patent uses \(\epsilon_0E^2\) as pressure. Standard electrostatic pressure
normal to a conductor is

\[
p=\frac12\epsilon_0E^2.
\]

The factor of two in equation (11) enters through the patent's earlier
energy-time manipulation. More importantly, neither scalar expression is a
complete apparatus force. A complete electrodynamic calculation uses the
Maxwell stress tensor

\[
T_{mn}=\epsilon E_mE_n-
\frac12\epsilon\delta_{mn}E_kE_k
\]

and integrates its traction over a closed boundary, while also accounting for
field momentum when fields vary in time. The simulation therefore labels the
standard \(\epsilon_0E^2/2\) value only as a *selected-patch comparison*.

For the effective \(40\ \mathrm{kV}\) calibration:

| Calculation | Result |
|---|---:|
| Patent equation (11) | \(237.00\ \mu\mathrm N\) |
| Standard pressure on the same two selected patches | \(118.50\ \mu\mathrm N\) |
| Net force on a complete isolated apparatus | Requires a closed stress/momentum inventory |

The factor-of-two observation does not by itself explain the reported signal.
It shows that equation (11) is not yet a closed Maxwell-force calculation.

### 3.2 The DC equation produces the stated scaling

The literal equation (11) implementation gives:

| Voltage | Force |
|---:|---:|
| \(10\ \mathrm{kV}\) | \(14.8125\ \mu\mathrm N\) |
| \(20\ \mathrm{kV}\) | \(59.2500\ \mu\mathrm N\) |
| \(30\ \mathrm{kV}\) | \(133.3125\ \mu\mathrm N\) |
| \(40\ \mathrm{kV}\) | \(237.0000\ \mu\mathrm N\) |

This confirms \(F\propto V^2\) and polarity invariance inside the patent
ansatz. Those signatures are shared by ordinary electrostatic forces and are
therefore necessary but not distinctive evidence for propulsion.

### 3.3 The AC prose does not match equations (12)-(13)

For a common sinusoidal field

\[
E_i(t)=C_i\sin(\omega t+\phi),
\]

write \(D(t)=D_0\sin^2(\omega t+\phi)\). Directly averaging the derivative in
equation (13) from \(t=0\) over one period gives

\[
\left\langle F\right\rangle_{\rm exact}
=\epsilon_0D_0\sin^2\phi.
\]

The prose after equation (15) instead assigns half the necessary magnitude to
the \(t\dot D\) contribution, which corresponds to

\[
\left\langle F\right\rangle_{\rm prose}
=\epsilon_0D_0
\left(\frac12-\frac14\cos2\phi\right).
\]

The simulation obtains:

| Starting phase | Exact derivative of eq. (12) | Patent prose |
|---:|---:|---:|
| \(0^\circ\) | approximately \(0\ \mu\mathrm N\) | \(59.25\ \mu\mathrm N\) |
| \(90^\circ\) | \(237.00\ \mu\mathrm N\) | \(177.75\ \mu\mathrm N\) |

This is an internal factor-of-two mismatch in the patent's AC derivation.

There is a deeper problem. Equation (12) contains absolute \(t\), so equation
(13) gives different forces one period apart even though \(E\) and \(\dot E\)
are then identical. In the reference run at \(1\ \mathrm{kHz}\):

| Same waveform state | Equation (13) force |
|---:|---:|
| \(t=0.125\ \mathrm{ms}\) | \(0.30464\ \mathrm{mN}\) |
| \(t=1.125\ \mathrm{ms}\) | \(1.79375\ \mathrm{mN}\) |

The difference is \(1.48911\ \mathrm{mN}\). A physical law may depend on a
recorded turn-on history, but it cannot depend on an unspecified shift of the
coordinate time origin. DET8 therefore cannot adopt equations (10)-(13) as a
law map without an additional, physical state variable and a conserved
momentum endpoint. Merely renaming absolute time as \(R^-\) would be smuggling.

---

## 4. Relational Boundary Sweep

To make the discussion's boundary proposal executable, the sandbox declares
the following phenomenological coupling:

\[
\chi(d,\epsilon_r,s)=
\chi_0
\left[1+\frac12\frac{\epsilon_r-1}{\epsilon_r+1}\right]
(1-s)
\frac{1}{1+(d/\ell)^2},
\]

where \(d\) is wall distance, \(s\) is shielding fraction, and
\(\ell=0.25\ \mathrm m\) in the reference run. If an external endpoint exists,

\[
F_{\rm apparatus}=\chi F_{\rm Eq.11},
\qquad
F_{\rm boundary}=-F_{\rm apparatus}.
\]

At \(\epsilon_r=1\) and \(s=0\), the illustrative sweep is:

| Wall distance | \(\chi\) | Apparent force |
|---:|---:|---:|
| \(0.05\ \mathrm m\) | 0.96154 | \(227.885\ \mu\mathrm N\) |
| \(0.10\ \mathrm m\) | 0.86207 | \(204.310\ \mu\mathrm N\) |
| \(0.20\ \mathrm m\) | 0.60976 | \(144.512\ \mu\mathrm N\) |
| \(0.50\ \mathrm m\) | 0.20000 | \(47.400\ \mu\mathrm N\) |
| \(1.00\ \mathrm m\) | 0.05882 | \(13.941\ \mu\mathrm N\) |

These numbers are not predictions. They demonstrate the shape of a
discriminator: any real external endpoint must produce a repeatable transfer
function when its boundary conditions are varied. A null result constrains
that particular boundary channel; it does not prove reactionless momentum.

The decisive measurement is simultaneous:

\[
F_{\rm apparatus}(t)+F_{\rm enclosure}(t)+F_{\rm supply}(t)
+\frac{dP_{\rm EM}}{dt}=0
\]

within uncertainty. Moving a grounded enclosure while failing to measure its
reaction force leaves the DET regime incomplete.

---

## 5. Matched-final-state history test

The sandbox also implements the discussion's two voltage paths:

\[
0\rightarrow30\rightarrow50\ \mathrm{kV}
\]

and

\[
70\rightarrow50\ \mathrm{kV}.
\]

An explicitly optional relaxation model updates \(\kappa\) toward a
voltage-dependent target and applies

\[
F=F_{\rm Eq.11}
\left[1+\lambda_H(\kappa-\kappa_{\rm target})\right].
\]

With \(\lambda_H=0.2\), one-second dwells, and a five-second relaxation time,
the two paths differ by \(8.973\ \mu\mathrm N\) at the same final
\(50\ \mathrm{kV}\). This is a sensitivity demonstration only. Setting
\(\lambda_H=0\) removes it completely, and ordinary dielectric absorption,
charge trapping, thermal lag, creep, power-supply settling, and mechanical
memory can all create the same signature. A DET interpretation becomes
eligible only after those recorded material histories fail quantitatively.

---

## 6. What the simulations establish

They establish four mathematical results about the translation:

1. The patent's DC patch formula is easy to encode in DET8 and reproduces its
   \(V^2\) and polarity signatures.
2. DET8 adds no thrust term. Its bond antisymmetry forces every accepted
   impulse to have another endpoint.
3. An external-boundary explanation is coherent and experimentally
   discriminating, but it is a hypothesis with a measurable reaction, not a
   reactionless drive.
4. The patent's AC extension is internally inconsistent: its prose average
   does not follow from its equation (12), and the resulting force depends on
   the arbitrary absolute time coordinate.

They do **not** establish that the reported \(237\ \mu\mathrm N\) is an
artifact, an external momentum exchange, or new physics. That requires raw
time-series data, complete geometry and materials, a closed electromagnetic
model, and independent force measurements on every candidate endpoint.

The most productive next experiment is therefore not a larger thrust claim.
It is a **closed momentum inventory plus a relational boundary sweep** with
pre-registered null channels and a matched dummy load.
