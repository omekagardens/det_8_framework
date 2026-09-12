# QR-05DF: a physical pair-kernel — light cones and orientation from the free propagator

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — a model, not a physical claim.** E's next step: replace the toy `𝔇` of
[QR-05DE](../qr-05de-pair-kernel-orientation-2026-09-11/README.md) with a **physical-
flavored, directed kernel** and test whether the conformal/orientation reading survives.
It does: the propagator's **support is the directed light cone**, the symmetric part is
the undirected (conformal) comparability, and orientation is the **sign of the phase** —
while strong positivity remains a genuine constraint.

## 1. Pre-specification

- **Question (E next step).** Does a physical (directed, local) pair-kernel recover the
  light cones and the orientation, and can it be strongly positive?
- **Kernel.** Link matrix `L` (covers of the causal set); the free path-sum propagator
  `K = Σ_{k≥0} Lᵏ = (I − L)⁻¹`, `K(x,y)` = number of link-chains `x → y`; then
  `G = K + Kᵀ` (symmetric), `Ω = K − Kᵀ` (antisymmetric), `𝔇_K = G + iΩ`.
- **Objects.** `2-chain`, `V`, `3-chain`, `diamond`, and 1+1 sprinklings `n = 6, 8`.
- **Status.** Track-B exploratory; a *model* of a physical `𝔇` (the follow-up is a true
  Sorkin–Johnston / quantum-sequential-growth kernel).

## 2. Results

| object | n | directed light cone = supp(K) | undirected comparability = supp(G) | phase sign = orientation | `𝔇_K` strongly positive |
|---|---|---|---|---|---|
| 2-chain | 2 | ✓ | ✓ | ✓ | ✓ |
| V | 3 | ✓ | ✓ | ✓ | ✓ |
| 3-chain | 3 | ✓ | ✓ | ✓ | ✓ |
| diamond | 4 | ✓ | ✓ | ✓ | ✗ |
| sprinkle_d2_n6 | 6 | ✓ | ✓ | ✓ | ✗ |
| sprinkle_d2_n8 | 8 | ✓ | ✓ | ✓ | ✗ |

- **F1 — light cones.** `supp(K)` off the diagonal is exactly the **directed** causal
  relation (`K(x,y) > 0 ⇔ x ≺ y`): the local propagator recovers the causal order.
- **F2 — conformal.** `supp(G)` is the **undirected** comparability, and `G` is
  orientation-invariant.
- **F3 — orientation.** The **sign of `arg 𝔇_K`** is the orientation (`+` for `x≺y`,
  `−` for `y≻x`). Orientation lives in the phase, exactly as E found.
- **F4 — time reversal.** `τ` (`≺ ↦ ≺ᵒᵖ`) acts as conjugation: `K ↦ Kᵀ`, `G ↦ G`,
  `Ω ↦ −Ω`, `|𝔇_K| ↦ |𝔇_K|` (checked on all 6 objects). The magnitude stays
  orientation-blind.
- **F5 — strong positivity is a constraint.** The naive symmetrisation `𝔇_K = G + iΩ` is
  strongly positive for only **3 of 6** objects (the simple orders), failing for the
  diamond and the sprinklings. So the physical kernel does not automatically satisfy the
  pair-kernel axiom — *the same coupling E found*.

## 3. The strong no / coupled yes — DET's relational-coupling view (Status M)

E's result was "no in the strong sense, yes in a coupled sense," and QR-05DF confirms it
for a directed physical kernel. This **is** DET's ontological view, stated explicitly:

- **Strong no:** the pair-kernel does **not** reduce to — and does not subsume — the
  causal order. `𝔇` and `≺` are **non-redundant**.
- **Coupled yes:** they are **mutually constrained** — the conformal class is the shared
  object (`Re 𝔇` / `supp`), orientation is the directed remainder (`arg 𝔇` / `Im`), and
  strong positivity bounds how they combine.

So the two primitives stand in a **relational coupling**, not a reduction — which is
exactly the ontology DET adopts. This is used **exploratorily**: DET may be **missing
primitives** for a complete account (the true physical `𝔇` is not yet built, and the
coupling's strength `r*` is uninterpreted), so the result is **Status M**, coherent and
motivating but **not hardened** into a core claim.

## 4. Boundaries

A bounded study of a **model** kernel (`MATH`): the free link-path propagator, **not**
Sorkin–Johnston or quantum sequential growth, and not a metric, continuum, curvature or
gravity claim. It shows the *shape* of the bridge (support = light cone; phase =
orientation; strong positivity = constraint) without establishing that any physical `𝔇`
takes this form. The next steps are (i) a true physical `𝔇` (SJ / QSG) and (ii) an
interpretation of the coupling strength.

## 5. Evidence

`primary.py` (interval causality; power-sum propagator `Σ Lᵏ`; principal-minor strong
positivity) and `reference.py` (light-cone-dominance causality; fixed-point propagator
`K = I + L·K`; LDL strong positivity) compute the light cones, the conformal/orientation
split, the time-reversal action and strong positivity independently; the driver refuses
on any difference. `test_qr05df.py` (10 tests) pins the 2-chain propagator
(`K = [[1,1],[0,1]]`, phase `±π/4`), the diamond covers (4 links), and the flags.
`study.py` writes create-only `results.json` and `source-freeze.json`. Design note:
[E_PAIR_KERNEL_GEOMETRY.md](../../track_b/E_PAIR_KERNEL_GEOMETRY.md). Decision record:
[RESULTS.md](RESULTS.md).
