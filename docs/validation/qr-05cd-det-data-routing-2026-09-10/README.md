# QR-05CD: DET data-routing design note

10 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This note maps each DET structural target to the kind of data that can
legitimately exercise it, so that a dataset is not applied to a gate it does
not instantiate. It exists because QR-05CB did exactly that: it fed a
quantum-correlation dataset into the geometry program. Nothing here executes
a run or makes a physical claim.

Continue [QR-05CB](../qr-05cb-open-data-applicability-2026-09-10/ONTOLOGY_AMENDMENT.md)
and the [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).

## 1. The two-module discipline

`docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §7: *"Connecting a quantum module
to an unrelated geometry module is not a unification."* A bridge is legitimate
only when **both** sides are present in the data or the construction.

`docs/record_kernel_physics.md` §4 fixes the primitives: causal order `(V,≺)`,
counting measure `#`, local record `R`, law map `L`, pair-kernel `𝔇`. From these
it names several *separate* structural targets; a dataset instantiates at most
some of them.

## 2. Routing table

| Target (source) | Commitment | Legitimate data | Gate |
|---|---|---|---|
| Causal geometry from order and count (T7) | geometry | a supplied Lorentzian geometry and its causal order/count (sprinkling) | QR-05 geometry chain |
| Bell / Tsirelson (PHYSICS §5, T6) | quantum correlation | setting-conditioned outcome statistics (E(α,β), CHSH) | quantum-correspondence gate |
| Quadratic commit weights / `I₃=0` (§5) | quantum possibility | multi-path interference counts | quantum-correspondence gate |
| Pointer records from redundancy (§5) | classical records | redundant records / error-rate data | record-redundancy gate |
| Diffusion / relaxation of `K` (§5) | stochastic dynamics | time series of a held-out kernel under a known channel | history-distance gate |
| Predictive history κ (§2.2) | history carrying | repeated kernel measurements on matched preparations | history-distance gate |
| κ as materials descriptor (PHYSICS §1) | materials | instrumented response, temperature, calibration | applied-physics program |
| Path irreversibility / fluctuation (§5) | thermodynamics | forward/reverse path counts | fluctuation gate |

## 3. Admissibility checklist

For a proposed dataset→gate pair, require all of:

1. **Which target** does the data instantiate (row of the table above)?
2. **Which side of the bridge** does it supply, and is the other side supplied
   or declared independently? (The CB error was fabricating the other side.)
3. **Are the gate's native objects present** — e.g. supplied marks/regions for
   a geometry gate, or setting-conditioned kernels for a correlation gate?
4. **Is the observable raw or derived?** (`docs/observable_anchoring.md`: use
   instrument registrations; a theory-dependent reduction is quarantined.)
5. **Multi-module datasets** must be split by target; one dataset is not a
   license to run every gate on it.

## 4. Worked example — QR-05CB

- Target instantiated: **Bell/Tsirelson** (E(α,β) from four-fold coincidences).
- Geometry side: **absent** (coordinates are interferometer phases, no supplied
  marks). CB declared marks by fiat, so the bridge had only one real side.
- Correct routing: the dataset belongs to a quantum-correspondence gate, not
  to the T7 geometry chain. See [the amendment](../qr-05cb-open-data-applicability-2026-09-10/ONTOLOGY_AMENDMENT.md).

## 5. Boundary

This is a routing discipline, not a result. It does not claim any gate passes;
it constrains which gate a dataset may address. It supplies no metric, no
dynamics and no physical claim, and it does not modify the CB data or capture.
