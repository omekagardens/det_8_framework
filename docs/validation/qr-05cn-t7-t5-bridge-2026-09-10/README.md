# QR-05CN: T7/T5 compatibility bridge (design + bounded witness)

10 September 2026 (Pacific/Honolulu). **Design gate with a bounded executable
witness.** This defines a *single compatible history/composition model* that
ties the T7 order/count geometry and the T5 local-kernel operator together, so
they belong to one model rather than two unrelated modules
(`docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §7.2: *"attaching an unrelated
quantum module to an unrelated geometry module is not a unification"*). Supplied
geometry; no gravity, no new dynamics.

Continue [QR-05CL](../qr-05cl-t5-wave-kernel-2026-09-10/README.md) /
[QR-05CM](../qr-05cm-t5-drift-diffusion-2026-09-10/README.md) (T5) and
[QR-05CK](../qr-05ck-metric-reconstruction-2026-09-10/README.md) (T7).

## 1. The problem

- **T7** reads geometry (dimension, conformal structure, conformal factor) from
  the causal order and counting measure `(≺, #)`.
- **T5** reads a continuum operator (diffusion / drift-diffusion / wave) from a
  **local kernel** `K` via its moments.

If `K` is supplied *independently* of `(≺, #)`, the two are juxtaposed, not
unified. The bridge must make `K` a functional of the same record structure.

## 2. Shared structure

`docs/record_kernel_physics.md` §4 fixes the primitives `(V, ≺, #, L, 𝔇)`. Both
modules must be read off **one** such structure: T7 from `(≺, #)`, T5 from a
local kernel derived from the same `(≺, #, L)`. Composing them requires the
kernel to be **derived**, not declared.

## 3. Compatibility conditions

| # | Condition | Why it is needed |
|---|---|---|
| C1 | **One event set**: T7 and T5 use the same `(V, ≺)` | otherwise two unrelated modules |
| C2 | **Derived kernel**: `K` is a functional of `(≺, #, L)` | no independently supplied kernel |
| C3 | **Geometric consistency**: the T5 operator's coefficients are expressions of the T7-reconstructed geometry (density / conformal factor) | the operator must respect the reconstructed geometry |
| C4 | **One shared scale**: both are defined up to a single common scale, not two conventions (BL/BM/BN) | otherwise the coupling is ambiguous |
| C5 | **Scale consistency** (charter §7.3): grouping records at two scales gives consistent geometry *and* operator | the bridge must survive coarse-graining |
| C6 | **No double counting**: the operator introduces no independent source, stress or coupling | avoids a hidden second module |

## 4. Modeled versus reconstructed (charter §7.1)

- **Modeled**: the event order relation, the kernel's functional form, the
  attempt/record definition.
- **Reconstructed**: dimension, conformal factor (T7) and the operator
  coefficients (T5) — all read from the same records.
- Instrument registrations remain the empirical anchor; no reconstruction is
  promoted to a physical claim here.

## 5. The witness (bounded, executable)

A minimal operational test of C1–C3 on supplied geometry: from **one** sprinkle
with conformal factor `Ω²(x) = 1 + a sin(2πx)`,

1. **T7 route** reconstructs the conformal profile `P₇` from binned counts;
2. **T5 route** builds the kernel as a functional of the *same* points — a
   count-based (KDE) density `d₅` — instead of supplying it independently;
3. **Compatibility**: `P₇` and `d₅` are the same profile up to one scale
   (correlation ≈ 1);
4. **Negative control**: an independently supplied kernel with a *different*
   profile (`1 + a cos(2πx)`) is uncorrelated with `P₇` — juxtaposition, not
   unification.

See [RESULTS.md](RESULTS.md) for the numbers. This witnesses the *derived-kernel*
requirement; it does not construct the full composed model.

## 6. Boundaries

A design plus a bounded witness on supplied geometry. It is **not** a
unification theorem, not a derivation of gravity, not curvature, and it
introduces **no** new source, dynamics or coupling. The full composed-model
construction and scale consistency (C5) remain open. Curvature and the imported
BD operator stay parked; κ-gravity is retired and gravity is standard GR under
Option B.
