# QR-05DO (direction B): the anchor calculus

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory /
correspondence-level (Status M) — no physical claim.** QR-05CY computed the observational
quotient for a *single* declared interface. Direction B asks the quantitative follow-up:
**what is the minimal additional channel/anchor that makes scale + reference + geometry
identifiable?** This gate extends CY's criterion to a calculus over **channel sets** and
computes the lattice — where each target flips, and what the minimal anchor set is.

## 1. Pre-specification

- **Question.** What is the minimal additional channel/anchor that makes scale + reference
  + geometry identifiable?
- **Channel universe** (5 channels — 32 subsets):

| channel | content | kind |
|---|---|---|
| `order` | ordering fraction | internal |
| `order_signs` | interval signs | internal |
| `counts` | normalized binned count density | internal |
| `distance_ratio` | normalized chain-distance signature | internal |
| `anchor` | the world's unit in a fixed **external** standard | **external** |

- **World class (CY's families, re-used as a frozen fixture).** `dimension` — a sprinkle in
  `d = 2, 3, 4`; `scale` — one geometry at `c = 1, 2, 4`; `conformal` — the same fixed events
  under `Ω² = 1 + b·x`, `b = 0, 2`. Targets: `dimension`, `absolute_scale`,
  `conformal_factor`; joint target `(dimension, conformal_factor, absolute_scale)`.
- **Criterion (CY's P1).** `τ` is identifiable through `O_S` iff `τ` is constant on every
  `O_S`-class.
- **Protocol.** `seed 6`, `n_base 48`, `n_dim 64`, `n_bins 10`, reference family
  `{mean, max, min, median, rms, positive_fraction}`.

## 2. Results (all 32 subsets)

- **Monotonicity.** Identifiability is monotone under channel refinement: **0 one-step
  violations** over the lattice (a violation of the general property exists iff one exists
  for a one-step refinement, since refinement is transitive).
- **Each target flips on a single channel.** Minimal identifying sets:

| target | inclusion-minimal sets |
|---|---|
| `absolute_scale` | `{anchor}` |
| `conformal_factor` | `{counts}` |
| `dimension` | `{counts}`, `{distance_ratio}`, `{order}`, `{order_signs}` |

- **The joint minimum, as computed.** `joint_k_min = 2` with the unique inclusion-minimal set
  **`{anchor, counts}`** — the count profile *also* separates the declared dimension worlds
  on this finite class, so `counts` doubles as the geometry channel. Recorded as a lattice
  fact with the caveat below (proposition B5), **not** read as a mechanism.
- **The one-channel-per-blind-direction design is identifying:** `{order, counts, anchor}`
  identifies all three targets (it is identifying but not minimal).
- **The anchor is genuinely external.** No internal channel separates the scale witness pair
  (`scale1`, `scale2`) — `order`, `order_signs`, `counts`, `distance_ratio` all agree — while
  `anchor` does. On the **whole anchor-free half of the lattice** (all 16 subsets) every
  reference built from the channel is blind on that witness class, and on all 16
  anchor-bearing subsets it is sighted: CY's P2, lattice-wide. `absolute_scale` is
  `NON_IDENTIFIABLE` for every anchor-free subset.

## 3. Findings

1. **The anchor calculus is a monotone lattice.** Identifiability is not a scatter of
   one-off results: it is monotone in the channel set, so a *minimal* anchor set is
   well defined and each blind direction has a single-channel flip.
2. **One channel per blind direction.** Geometry ← `order`; conformal factor ← `counts`
   (marks); absolute scale ← an **external** unit. Only the last is unavailable from the
   record channel, which is exactly CY's P3 sharpened into a lattice statement.
3. **Reference validity flips with scale, not separately.** Because every internal channel is
   blind on the scale witness class, no internal reference can certify a scale-varying target
   — the two blockers are the *same* one, and one anchor clears both.
4. **A finite channel universe can flatter the lattice (B5).** `{anchor, counts}` is minimal
   *on this class* because a count profile happens to separate three dimension worlds; on a
   larger class that coincidence can fail. The gate therefore reports the lattice minimum
   **and** the per-direction design, and records the accidental separation explicitly.

## 4. Boundaries

The world class, the channel semantics and the targets are **declared choices**; the
statements are verified **finite instances**, as CY's were, not theorems about all worlds.
The `anchor` is modelled as "the world's unit expressed in a fixed external standard" — the
semantics of an independent calibration — and the gate verifies only the property that
matters (no internal channel separates the witness class). The `counts` channel on the
causal-diamond families is family-invariant, so its binning convention cannot affect any
verdict there (it is exact on the conformal family's box). Novelty is **low–moderate**: the
individual facts are elementary; the lattice formulation and the minimal-set computation are
the contribution. No metric, continuum, curvature, dynamics or gravity claim.

## 5. Evidence

`primary.py` (union-find quotient, CY's constructions imported via the frozen fixture) and
`reference.py` (re-coded constructions — recursive-memo longest chains, agreement-row
grouping, one-step refinement monotonicity) compute the same report independently;
`study.py` refuses on any difference and freezes the gate sources plus
`qr-05cy/primary.py` and `order_count_geometry.py` by hash. `test_qr05do.py` (15 tests) pins
the lattice, the monotonicity check (with a synthetic known-answer violation), the minimal
sets, the joint minimum and design, the lattice-wide blindness, the external-anchor property
and the re-coded chain distance against CY's own. Decision record: [RESULTS.md](RESULTS.md).
