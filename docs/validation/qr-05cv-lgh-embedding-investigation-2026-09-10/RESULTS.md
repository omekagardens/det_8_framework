# QR-05CV results

10 September 2026 (Pacific/Honolulu). **LGH/embedding investigation opened —
exact LMS core verified.** The discrete chain time-separation is a genuine
Lorentzian metric space: it satisfies the Lorentzian axioms exactly and is not a
Riemannian metric. 6 tests pass. This opens the research-grade program; the
embedding theory and the manifoldlikeness of the limit remain open. Supplied
geometry; no gravity claim.

## Exact core

For a finite causal set with `d(i,j) = (longest chain i→j)`, verified in
d = 2 and 3:

| Axiom | Result |
|---|---|
| A1 `d(i,i) = 0` | holds |
| A2 `d(i,j) > 0 ⇔ i ≺ j` | holds |
| A3 `d(i,j) > 0 ⇒ d(j,i) = 0` | holds |
| A4 reverse triangle `d(i,k) ≥ d(i,j) + d(j,k)` | holds (exact) |
| Riemannian triangle `d(i,k) ≤ d(i,j) + d(j,k)` | **fails** — e.g. `(0, 7, 1)` in d=2 |

So the discrete time-separation is an **LMS candidate**: the Lorentzian
(Minguzzi–Suhr) axioms hold exactly and the metric axiom fails, giving a
genuinely Lorentzian discrete structure. This is the object an LGH study must
compare with the continuum.

## The open program (opened, not solved)

1. the exact `d`-isometry statement for the natural embedding (CU gives a bounded
   upper estimate only);
2. the LGH infimum over correspondences/embeddings;
3. surjectivity/density with a commensurability defect (the continuum has extra
   points);
4. the scale/conformal class (absolute scale not identified, BL/BM/BN);
5. ensemble convergence under growing fluctuations (Sorkin);
6. manifoldlikeness of the limit (emergence — open).

## Boundaries

Research-grade and open. The exact core is verified for finite causal sets;
everything about the continuum LGH distance, embeddings and emergence is open.
No metric, manifold, curvature, dynamics or gravity is claimed. Curvature and the
imported BD operator stay parked; κ-gravity is retired and gravity is standard GR
under Option B.

## Verification and provenance

`primary.py` and `reference.py` compute the chain matrix, check the axioms and
find the Riemannian-triangle witness independently; the driver compares with a
float tolerance and refuses on any difference.

- Capture: 990 bytes;
  SHA-256 `a05681928f63d8c90b7a673acf0e90254ef05aa1493e2c1379bfed3f3633c61b`.
- Freeze: SHA-256
  `142138991bfcaf3252838b11cf622da4fd3740add20593bffd6ccee2dad618bf`.

CV continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
