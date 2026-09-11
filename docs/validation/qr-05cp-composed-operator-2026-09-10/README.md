# QR-05CP: composed T7+T5 operator construction

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
CN witnessed that the T5 kernel can be derived from the T7 record structure and
CO that the bridge is scale-consistent; this **closes the compatibility into a
model** — one operator whose coefficient is the T7-reconstructed geometry.
Supplied geometry; no gravity claim.

Continue [QR-05CN](../qr-05cn-t7-t5-bridge-2026-09-10/README.md) and
[QR-05CO](../qr-05co-scale-consistency-2026-09-10/README.md).

## 1. The composed operator

From one sprinkle with `Ω²(x) = 1 + a sin(2πx)`:

1. **T7** reconstructs `D(x)` — the conformal factor — from binned counts;
2. the **composed operator** uses that reconstructed geometry as its
   coefficient: `S f(x_k) = D_k (f_{k+1} − 2f_k + f_{k−1})` on the periodic
   lattice of bin centers, so the operator acts on the T7 geometry rather than
   on an independently supplied kernel.

## 2. What is verified

| Check | Criterion |
|---|---|
| **Reconstruction accuracy** | corr(`D`, true `Ω²`) high |
| **Faithful composition** | `S f / (h² f'')` equals a single constant times `D` at every site (`composition_dev` small) — i.e. the operator's coefficient is exactly the T7 geometry, up to the known O(h²) discretization constant |
| **Independent coefficient fails** | an operator supplied with a different coefficient (`1 + a cos`) is uncorrelated with the T7 geometry — juxtaposition, not composition |

## 3. Result

The composition is faithful, the reconstruction is accurate, and the
independent-coefficient control fails; numbers in [RESULTS.md](RESULTS.md). So
the T7 geometry can serve directly as the coefficient of a genuine T5
second-order operator — one model, not two modules.

## 4. Boundaries

A bounded witness on supplied geometry. It is **not** a unification theorem, not
a derivation of gravity, and it introduces **no** new source, dynamics or
coupling. The operator is a differential operator built from the reconstructed
geometry, not a field equation. The empirical bridge and any gravitational
dynamics remain open. Curvature and the imported BD operator stay parked;
κ-gravity is retired and gravity is standard GR under Option B.

## 5. Evidence and limits

`primary.py` and `reference.py` implement the reconstruction, the composed
operator and the checks independently; the driver compares with a float
tolerance and refuses on any difference. `study.py` writes create-only
`results.json` and `source-freeze.json`; `test_qr05cp.py` checks reconstruction
accuracy, faithful composition, the independent-coefficient control and route
agreement. Fixed inputs make the run deterministic. Limits: sources ≤262,144
bytes, artifacts ≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
