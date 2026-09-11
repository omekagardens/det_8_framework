# QR-05CV: LGH / embedding investigation (research-grade; exact LMS core)

10 September 2026 (Pacific/Honolulu). **Research-grade investigation, opened.**
This opens a Lorentzian Gromov–Hausdorff (LGH) route for causal sets, with a
bounded **exact core** verified here and the open program stated explicitly. It
promotes nothing; the embedding theory and the manifoldlikeness of the limit
remain open. Supplied geometry; no gravity claim.

Continue [QR-05CU](../qr-05cu-lgh-distance-2026-09-10/README.md) (the bounded LGH
upper estimate).

## 1. The framework (Minguzzi–Suhr)

A **Lorentzian metric space** (LMS) is a set `X` with a time-separation
`d : X×X → [0,∞)` such that (`x,y,z` arbitrary):

- **A1** `d(x,x) = 0`;
- **A2** the causality relation `x ≺ y :⇔ d(x,y) > 0` is a (strict partial) order;
- **A3** (antisymmetry of causality) `d(x,y) > 0 ⇒ d(y,x) = 0`;
- **A4** (reverse triangle) `d(x,z) ≥ d(x,y) + d(y,z)`;
- plus non-degeneracy/continuity conditions used in the embedding theorems.

The **LGH distance** is defined à la Gromov–Hausdorff through
*`d`-isometric embeddings*: `(X,d)` and `(Y,d')` are within `ε` if there are maps
`f : X → Y`, `g : Y → X` that are approximately inverse and satisfy
`|d(x,y) − d'(fx,fy)| ≤ ε`, with a commensurability/covering condition. Convergence
means recovery of the causal (conformal) structure, not the full metric.

## 2. The exact core verified here

For a finite causal set with the **discrete chain time-separation**
`d(i,j) = (longest-chain length from i to j)`, i.e. `0` if `i ⊀ j`:

| Axiom | Holds? |
|---|---|
| A1 `d(i,i) = 0` | ✓ |
| A2 `d(i,j) > 0 ⇔ i ≺ j` | ✓ |
| A3 `d(i,j) > 0 ⇒ d(j,i) = 0` | ✓ |
| A4 reverse triangle `d(i,k) ≥ d(i,j) + d(j,k)` | ✓ (exact — chains concatenate) |
| Riemannian triangle `d(i,k) ≤ d(i,j) + d(j,k)` | **fails** (a witness exists) |

So the discrete chain time-separation is a genuine **LMS candidate**: it
satisfies the Lorentzian axioms exactly and is *not* a Riemannian metric. This is
the object an LGH study must compare with the continuum.

## 3. The open research program

1. **d-isometry defect of the natural embedding.** Measured as a bounded upper
   estimate in CU; the exact `< . . . >`-isometry statement is open.
2. **The LGH infimum.** Requires the infimum over correspondences/embeddings
   (bottleneck-assignment / embedding theory), not just the natural map.
3. **Surjectivity and density.** The continuum has points absent from the
   sprinkle; a *dense* embedding (or a commensurability map with a covering
   defect, as in §2 of the framework) is needed, not a bijection.
4. **Scale.** `d` is defined only up to a scale (the discreteness `ℓ`); absolute
   scale is not identified (BL/BM/BN), so the LG class is a *conformal* one.
5. **Fluctuations.** In 2D the discrete/continuum defect does not vanish
   pointwise; the convergence is of the *ensemble* (a measure-theoretic LGH), and
   Sorkin notes the fluctuations grow with `1/ℓ`.
6. **Manifoldlikeness of the limit.** Whether the LG limit *is* a Lorentzian
   manifold is exactly the emergence question, which stays open (charter §7.5).

None of these is solved by the bounded steps CF–CU; they are the investigation
this gate opens.

## 4. Boundaries

Research-grade and open. The exact core (A1–A4) is verified for finite causal
sets; everything about the continuum LGH distance, embeddings, and emergence is
open. No metric, manifold, curvature, dynamics or gravity is claimed; κ-gravity
is retired and gravity is standard GR under Option B.

## 5. Evidence and limits

`primary.py` and `reference.py` compute the chain matrix, check the axioms and
find the Riemannian-triangle witness independently; the driver compares with a
float tolerance and refuses on any difference. `study.py` writes create-only
`results.json` and `source-freeze.json` (freezing the gate sources and the T7
module by hash); `test_qr05cv.py` checks the axioms, the Riemannian failure, the
witness and route agreement. Fixed seeds make the run deterministic. Limits:
sources ≤262,144 bytes, artifacts ≤16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
