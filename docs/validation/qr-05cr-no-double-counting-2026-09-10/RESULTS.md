# QR-05CR results

10 September 2026 (Pacific/Honolulu). **Composed-model no-double-counting audit
(C6) complete — positive.** The composed T7+T5 operator has no source
(zeroth-order) term, its coefficient is exactly the T7 geometry, and the
conservative (divergence) form conserves flux; a deliberately added source is
detected. 8 tests pass. Supplied geometry; no gravity claim.

## Checks (one sprinkle, Ω²=1+a sin(2πx), N=8000, 12 bins)

| Check | Value | Meaning |
|---|---|---|
| Source term `S(1)` | 0.0 (pointwise and divergence) | no source/reaction (zeroth-order) term |
| Flux, divergence form `Σ(S_D f)` | **0.0** | conservative (telescopes) |
| Flux, pointwise form `Σ(S_P f)` | **−0.790447** | not conservative — the divergence form is required |
| Coefficient recovered from kernel moment | dev **0.0** | equals the T7 geometry exactly — no independent field |
| Added-source control | 0.096593 | a source `c(x)` is detected |

`no_double_counting = true`. So the composition introduces **no** hidden second
module: no source term, no independent coupling, and a conservative divergence
form.

## The distinction it records

The pointwise-coefficient form `d·f''` (CP's form) and the divergence form
`(d f')'` both have no source term, but only the **divergence form** conserves
flux when `d` varies (`Σ_k(S_P f)_k = Σ_k f_k (Δd)_k ≠ 0`). C6 therefore selects
the divergence form as the conservative composed operator.

## Boundaries

A bounded audit on supplied geometry. It confirms the **absence** of a source
term and of an independent coupling in the composed operator; it does **not**
claim a field equation, a physical conservation law, curvature or gravity. The
operator is a differential operator built from the reconstructed geometry.
Curvature and the imported BD operator stay parked; κ-gravity is retired and
gravity is standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` implement the reconstruction, both operator
forms and the checks independently; the driver compares with a float tolerance
and refuses on any difference.

- Capture: 613 bytes;
  SHA-256 `a050adcb2c495d6173e19057f1c3f346f280cad66bc3f8ae2ddf802d236a7eb1`.
- Freeze: SHA-256
  `b0ad30dd7321c56fabcfa0452cad8f5f1932369bcf908f5624badcab2450457a`.

CR continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
