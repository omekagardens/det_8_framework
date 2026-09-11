# QR-05CR: composed-model no-double-counting audit (C6)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
CN condition C6: the composed T7+T5 operator must introduce **no independent
source or coupling** — no hidden second module. This audits the CP operator for
a source (zeroth-order) term, checks the conservative (divergence) form, and
confirms the coefficient is exactly the T7 geometry. Supplied geometry; no
gravity claim.

Continue [QR-05CP](../qr-05cp-composed-operator-2026-09-10/README.md) and the
[QR-05CN](../qr-05cn-t7-t5-bridge-2026-09-10/README.md) conditions.

## 1. What is audited

Let `d = Ĝ` be the T7-reconstructed geometry. Two forms of the second-order
operator are compared:

```text
pointwise:    (S_P f)_k = d_k (f_{k+1} − 2f_k + f_{k−1})
divergence:   (S_D f)_k = ½(d_k+d_{k+1})(f_{k+1}−f_k) − ½(d_k+d_{k−1})(f_k−f_{k−1})
```

| Check | Property |
|---|---|
| **No source term** | `S(1) = 0` at every site — the zeroth-order (source/reaction) coefficient is zero |
| **Flux conservation** | `Σ_k (S_D f)_k = 0` for any `f` (telescoping) — the divergence form is conservative; the pointwise form is **not** (`Σ_k (S_P f)_k = Σ_k f_k (Δd)_k ≠ 0`) |
| **Coefficient is the T7 geometry** | recovering the coefficient from the kernel's second moment returns exactly `d` — no independently supplied field |
| **Source control** | adding a source term `c(x)` makes `S(1) = c(x) ≠ 0`, which the audit detects |

## 2. Result

The composed operator has no source term, its coefficient is exactly the T7
geometry, and the divergence form conserves flux while the pointwise form does
not — so the conservative composition is the divergence form. A deliberately
added source is detected. Numbers in [RESULTS.md](RESULTS.md).

## 3. Boundaries

A bounded audit on supplied geometry. It confirms **absence** of a source term
and of an independent coupling in the composed operator; it does **not** claim a
field equation, conservation law of physics, curvature or gravity. The operator
is a differential operator built from the reconstructed geometry. Curvature and
the imported BD operator stay parked; κ-gravity is retired and gravity is
standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` implement the reconstruction, both operator
forms and the checks independently; the driver compares with a float tolerance
and refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json`; `test_qr05cr.py` checks the absent source, the divergence
flux conservation and pointwise non-conservation, the coefficient identity, the
added-source control and route agreement. Fixed inputs make the run
deterministic. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes.
Decision record: [RESULTS.md](RESULTS.md).
