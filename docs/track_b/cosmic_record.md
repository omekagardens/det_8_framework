# DET v8.0 — Track B: Cosmic Record (F11)

**Status:** Track B research module (proposed). Reframed September 3, 2026 — the "κ-field across cosmic time" framing is retired with the κ-gravity program (Option B); κ is a fitted predictive-history coordinate, not a field.
**Date:** September 3, 2026 (originally August 10, 2026)
**Purpose:** Ask, without re-smuggling a field: does the universe as a whole have a nonzero predictive-history coordinate κ — i.e., does its actualized causal record still constrain its future commit kernel beyond its present state alone?

---

## 1. The corrected definition of κ

Under the re-foundation (`docs/record_kernel_physics.md` §2), κ is **not** a physical field and **not** "structural history density at a point." It is a *fitted coordinate*:

> **κ is the minimal information about the causal record \(R^-\) that must be retained, beyond the present state \(S\), to predict the next commit kernel \(K\).**

Operationally it is the Fisher–Rao distance between two history-conditioned future kernels matched on the same present state:

\[
\kappa(h_a,h_b\mid S)=\frac{2}{\pi}\arccos\left[\sum_x\sqrt{K_a(x)K_b(x)}\right],
\qquad 0\le\kappa\le 1 .
\]

Two consequences matter for F11:

1. **κ is relative, not absolute.** It compares two histories against one matched present state. There is no well-posed "κ(x) at spacetime point \(x\)" until one specifies *which* two histories and *which* matched present state. The old "κ-field across cosmic time" silently assumed an absolute scalar field; the re-foundation removes that assumption (and notes the legacy κ profiles exceeded the \([0,1]\) normalization).
2. **Scalar κ is a rank claim, not a given.** Whether retained history is rank one (scalar), rank \(r>1\) (vector/tensor), rank zero (κ unnecessary), or nontransportable is an empirical question (T1). It cannot be assumed for the cosmos.

## 2. The reframed question

> Does the universe as a whole have a nonzero predictive-history coordinate?

Concretely: fix a coarse-grained present-state description \(S\) of the cosmos (e.g., a smoothed matter field at some epoch). Ask whether the actualized causal record \(R^-\) still predictively distinguishes the future commit kernel from a history-free baseline \(K(\cdot\mid S)\). If yes, there is a cosmic κ — a residual, history-conditioned predictive distinction. If no, the present state is state-complete and the cosmic record carries no remaining predictive weight.

This is a **rank question, not a field profile.** The honest outcomes are the same four as T1:

| Outcome | Meaning for the cosmic record |
|---|---|
| Rank zero | The present state is state-complete; cosmic history has no residual predictive consequence |
| Rank one | A single scalar κ is supported |
| Rank \(r>1\) | Cosmic history is vector/tensor-valued |
| Nontransportable | Each probe has its own nuisance history; no universal cosmic κ |

## 3. Status under Option B: purely ontological

> **No cosmological observable signature.** Under Option B, κ couples only to the participation aperture (λ_P). The retired gravity channel (`G_eff = G·κ/κ_earth`) is withdrawn, so the BAO/CMB/ISW/LSS signatures proposed by the earlier F11 are **retired** (they belong to `archive/retired_kappa_gravity.md`, not to this module). The cosmic record has no measurement program of its own.

"Reading the cosmic record" is therefore a **Track B ontological notion (Status M)**, not a cosmology experiment. It is held for coherence and fruit, not because anything is measured at cosmic scale.

Any empirical read of κ remains gated on the same local ladder as everything else — a κ rank test, then held-out transport — and even then it is a *local* predictive-history coordinate, not a cosmological field.

## 4. The cosmic record as memory (Status M)

The ontological reading survives the reframing once the substance language is removed:

The universe's record — the actualized causal past — *is* its structural memory. What "the cosmic record" names is not a field encoding that memory but the record itself; κ is the *measure* of how much of that memory remains predictively active, relative to a present-state description. The record is the trace; κ is how much the trace still bites.

| Cosmic Epoch | What the record carries (ontological, Status M) |
|---|---|
| Recombination | A nearly featureless record — little residual predictive distinction beyond a smooth state |
| Structure formation | The record accumulates predictive distinction — history begins to outrun the present state |
| Present | The record is richly structured — high residual predictive weight in some regimes |

## 5. F11 Claim Register

| Claim | Status |
|---|---|
| κ is a fitted predictive-history coordinate, not a field | FT — architectural (re-foundation §2) |
| Scalar κ is justified only by a rank-one test | Open — empirical (T1) |
| "κ varies with cosmic time" (as a field profile) | **RETIRED** — κ is relative, no absolute field profile |
| BAO/CMB/ISW/LSS constrain κ(z) | **RETIRED** — no cosmological κ signature under Option B |
| The universe has a nonzero predictive-history coordinate | Open — a rank question, not a field measurement |
| The cosmic record is the universe's structural memory | M — Track B interpretation |

## 6. Connection to F10 (Law Genesis)

F10 asks why the law map \(\mathcal L\) is stable. F11, reframed, poses the same question at the level of the record: if \(\mathcal L\) were *not* stable, the predictive-history coordinate κ would show discontinuities — epochs where the same present state yields different future kernels under the same history. The smoothness (or lack of it) of κ's predictive distinction is evidence for (or against) the stability of \(\mathcal L\). This is an ontological constraint, not a measured one.

## 7. Next steps

- Define, at the level of the record, what a "coarse-grained present-state description" of the cosmos would be, before asking whether cosmic κ is nonzero. (The question is currently under-specified without this.)
- If pursued, begin with the T1 rank test on a *local* record, not a cosmological one; cosmic κ is downstream of local κ.
- Leave the retired cosmological signatures in `archive/retired_kappa_gravity.md`; do not reintroduce them here.

---

**End of Cosmic Record (F11)**
