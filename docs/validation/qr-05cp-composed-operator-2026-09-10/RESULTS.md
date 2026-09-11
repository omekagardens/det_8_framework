# QR-05CP results

10 September 2026 (Pacific/Honolulu). **Composed T7+T5 operator construction
complete — positive.** One operator whose coefficient is the T7-reconstructed
geometry: the composition is faithful, the reconstruction is accurate, and an
independently supplied coefficient fails. 7 tests pass. Supplied geometry; no
gravity claim.

## Checks (one sprinkle, Ω²=1+a sin(2πx), N=8000, 12 bins)

| Check | Value | Criterion |
|---|---|---|
| Reconstruction accuracy (corr `D`, true `Ω²`) | **0.992943** | ≥ 0.9 |
| Faithful composition (`Sf/(h²f'')` = const·`D`) | constant **0.977361**, dev **0.0** | dev ≤ 0.05 |
| Independent-coefficient control (corr with `D`) | **0.018010** | ≤ 0.5 |

`composed = true`. The constant 0.977361 is the expected O(h²) discretization
factor `(2−2cos(2πh))/(4π²h²)` at `h=1/12 ≈ 0.97736`; the deviation across sites
is exactly zero, so the operator's coefficient is precisely the T7 geometry at
every site.

## What this establishes

The T7-reconstructed geometry can serve directly as the coefficient of a genuine
T5 second-order operator — closing CN's compatibility and CO's scale-consistency
into an **actual composed model**: one record set gives both the geometry (T7)
and the operator that acts on it (T5). An operator supplied with an independent
coefficient is uncorrelated with the geometry — juxtaposition, not composition.

## Boundaries

A bounded witness on supplied geometry. It is **not** a unification theorem, not
a derivation of gravity, and it introduces no new source, dynamics or coupling.
The object is a differential operator built from the reconstructed geometry, not
a field equation. The empirical bridge and any gravitational dynamics remain
open. Curvature and the imported BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` implement the reconstruction, the composed
operator and the checks independently; the driver compares with a float
tolerance and refuses on any difference.

- Capture: 329 bytes;
  SHA-256 `27c7c5a4d585f4ff19aeab96635f8fa97ecbcf4fcb7c23880e0ff122014740f1`.
- Freeze: SHA-256
  `abe1fd9e55db9318a1d3c52655c6bfbeb1eebd48b94505c9895e3af28bd278ef`.

CP continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
