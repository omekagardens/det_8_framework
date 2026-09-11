# QR-05CB: open-data applicability run (Bell-test CHSH)

10 September 2026 (Pacific/Honolulu). **Executable, real open data, bounded.**
This gate runs the QR-05 record model's applicability test against a real,
publicly available measurement dataset, to determine whether it can serve as
a physical substrate for the BZ protocol. It acquires the data, applies
explicit declared mappings, and measures the exact gap to the declared ideal
family. It is not a calibration and makes no claim about the experiment.

Continue the [BZ protocol](../qr-05bz-physical-protocol-design-2026-09-10/README.md),
the [BY preregistration](../qr-05by-metric-dynamics-design-2026-09-10/README.md)
and the [apparatus interface](../qr-05bx-apparatus-event-interface-design-2026-09-10/README.md).

## 1. Dataset

`data/VBI_Coincidence_20230707.dat` — raw single and coincidence counts from a
four-photon frustrated-interference CHSH experiment, 1,184 rows × 29 columns
(a 37 α-step × 32 β-step grid).

- Source: Dryad deposit `10.5061/dryad.7m0cfxq59` (CC0-1.0), retrieved via
  the authors' mirror `github.com/NJU-Malab/Violate-CHSH-in-FI`.
- SHA-256 `a3e687354b71895096aee4e28d113d629e157953c7d240d33de3bd0aca653254`,
  179,104 bytes. `data/readme.md` and `data/main.m` are the deposit's own
  documentation and analysis script.

Columns used: 5–8 single counts on channels 1–4; 9 four-fold coincidence
(channels 1–4); 10 coincidence of channels 1–2 (Alice pair); 11 coincidence of
channels 3–4 (Bob pair).

## 2. Why this is an applicability test, not a measurement

The QR-05 model needs a nested four-symbol population `r=(r₁,r₂)∈S`,
`π(r)=(1−r₂, r₂−r₁, 0, r₁)`, compared against the ideal family `q(η,δ)` with
targets `τ(0)=1/4`, `τ(1)=17/80`. The dataset does not come with those marks,
so a mapping must be **declared**. Three are evaluated:

| Mapping | r₁ | r₂ | Nesting |
|---|---|---|---|
| `single_normalized` | `cc4/single1` | `cc_alice/single1` | `cc4 ≤ cc_alice ≤ single1` |
| `trigger_conditioned` | `cc4/cc_alice` | `cc_alice/cc_alice` | `cc4 ≤ cc_alice` |
| `bob_normalized` | `cc4/single1` | `cc_bob/single1` | `cc4 ≤ cc_bob ≤ single1` |

In every mapping the four-fold coincidence is a subset of the pair
coincidence, so the forbidden symbol `10` is impossible **by construction** —
the nested support premise (P8) is imposed, not measured. The reference
validity and independence premises (P5, P11) remain unsupplied.

## 3. Result

The run measures the exact sup-norm distance from each mapped population to
the declared finite ideal family `η∈{0,1}`, `δ∈{0,1/2,1,2}`, and the number of
settings admitted under the declared allowance `e_cal=3/200` (from the BW
composition `a_sys=1/100`, `d_sys=1/200`). Details and exact fractions are in
[RESULTS.md](RESULTS.md). The decisive quantity is that the ideal family's
second coordinate spans a narrow band while the mapped data's second
coordinate does not overlap it in any declared mapping, so no setting is
admitted.

This is a **category mismatch, not a model failure** (see the
[ontology amendment](ONTOLOGY_AMENDMENT.md)): the Bell dataset instantiates
DET's quantum-correlation commitment, not the T7 geometry commitment, so the
mapping fabricated the geometric side and the protocol is simply not
applicable to it. The geometry path needs a supplied Lorentzian geometry /
sprinkling (T7) or a purpose-built geometric-probe apparatus (BX).

## 4. Boundaries

Not a measurement of the QR-05 model, not apparatus calibration, not a
metric or dynamics result. The mapping is a declared premise; the verdict is
reported per mapping and is not independent of that choice. The data is used
only as a real-count test input. No device, no acquisition, no RET coupling,
no gravity claim. Sources and data are hash-pinned; the run is exact-rational
and offline apart from the one-time acquisition.

## 5. Evidence and limits

`primary.py` and `reference.py` independently parse and reduce the file and
must produce identical reports; `study.py` compares them and writes the
create-only `results.json` and `source-freeze.json`. Tests in
`test_qr05cb.py` re-check the dataset hash, the grid shape, the nesting
inequality, the family range, the per-mapping gaps and the zero-admission
verdict. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes. The
separate [decision record](RESULTS.md) records the outcome; the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md) keeps
later work gated.
