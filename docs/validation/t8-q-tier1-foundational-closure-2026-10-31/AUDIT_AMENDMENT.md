# Audit amendment to the Tier I conditional bridges

31 October 2026 (Pacific/Honolulu). Status: **CORRECTION_AUTHORED; DISTINCT_REVIEW_AND_COORDINATOR_DISPOSITION_PENDING**.

This amendment accompanies the corrected `TIER1_CLOSURE_THEOREMS.md`. The original version remains available at commit `50be57d85aab1bf0396143694b4f9c32632010de` (the original theorem note has SHA-256 `54d3bcf208158d34de679812c3ebb8dd0551df06b2ceaf1d8cf3d15535c5d37d`). The prospective protocol and checker are preserved byte-for-byte; their original wording is historical, not an override of these explicit corrections. Committed protocol-before-result order establishes source order, not independent evidence of when reasoning or execution occurred.

## Corrections and prospective-contract deviations

| Item | Original issue | Corrected disposition proposed for review |
| --- | --- | --- |
| Theorem 4A spectral proof | The displayed vector powers were inconsistent, the sign did not match the specified \(iT_m\), and the asserted bound on all non-leading absolute eigenvalues included the negative extremal eigenvalue. The \(n=2\) upper bound divided by zero. | Use \(v_{r,j}=\exp(-i(2r+1)\pi j/m)\), derive the full cotangent spectrum by a geometric sum, and identify \(-\Lambda_n\) as the relevant extremum. Strict positivity of a codimension-one principal restriction excludes a second nonpositive eigenvalue. Handle \(n=2\) by eigenvalues \(1/2\pm t_2\), with \(t_2>1/2\). The conclusion is for the declared principal-minor sign catalogue, not every bounded-copy strategy. |
| Theorem 1A | The statement listed scalar diamonds while the cancellation proof used full branch-map diamonds. | Add full incomparable-birth diamonds of the complete unnormalized branch maps on all of \(V\), for every base, ideal pair and newborn-mark pair. Scalar diamonds alone are insufficient. |
| Theorem 1B Walsh normalization | Independent review caught the false claim that the integer-Walsh inverse tensor fixes \(\lvert\psi_{\mathrm{joint}}\rangle\); it scales this vector by \(1/2\). | The normalized \(H\otimes H\) fixes the vector. Explicitly match the coupled internal block \(\sigma_{\mathrm{joint}}/4\) to \((H_2\otimes H_2)\sigma_{\mathrm{joint}}(H_2\otimes H_2)/16=\sigma_{\mathrm{joint}}/4\). Thus the stated \(N'=(J_2\otimes J_2)(\sigma_{\mathrm{joint}})\) identity and normalization survive with all existing section prefactors preserved. |
| Theorem 2C | The polynomial dimension result was presented as classical-simplex or complex-Hermitian cone selection. | Retain \(d(n)=n\) or \(n^2\) and the exact Stirling/binomial coefficients under multiplicativity and the explicitly supplied \(d(2)\le4\) bound. No cone, effects or composition are identified by dimension alone. Transfer of the restricted two-outcome quotient bound is an assumption. |
| Theorem 3B projector lift | The protocol and summary implied an exact dyadic-real lift for arbitrary \(P\), although the displayed lift uses coordinate \(P_R\). | Retain arbitrary-projector Lüders uniqueness under 1-positivity, calibration and non-disturbance on the entire repeat face. Restrict the explicit dyadic-real lift to coordinate/coarse-cell projectors. |
| Theorem 3B subspace controls | The frozen protocol says “four” controls but lists three Clifford controls; the theorem and checker use three Pythagorean controls. | Record the substitution as a prospective-contract deviation. The actual family is \(\{I,\mathcal W^{R,\mathrm{Pyth}}_{01},\mathcal W^{I,\mathrm{Pyth}}_{01}\}\). The four measured real coordinates have rank four; there are three controls, not four. No equivalence between unavailable physical control implementations is claimed. |
| Theorem 4B arithmetic | Real estimates and error bounds were followed by an unconditional rational-radius assertion. | The analytic bounds hold for real inputs. Exact rational inverse entries, squared radius and certificate arithmetic additionally require rational supplied estimates and error bounds. |
| Consolidated conclusions | “All four foundational gaps closed” conflated section results, cone reconstruction and physical availability. | List separate conditional connections. The single-system quotient is not proved stable under arbitrary added joint tests on every representative. RI-23's raw-domain obstruction, physical control/readout access, global reconstruction, mass/gravity and continuum questions remain separate. “Spacelike” means order incomparability only. |

## Verification identity and limits

The correction author read the frozen protocol, the theorem note and the complete checker source. Required source context included the admitted growth-model conditions, the Walsh-section and active-residual constructions, and repository governance. This was manual proof and static source work. No scientific program, calculator, test, compilation, import, benchmark or external query was executed, and no Git/index mutation was performed by this author.

Preserved source identities:

- `PROTOCOL.md`: SHA-256 `754d88d3af8f0c003e4a9c4a21a959e7fd8d203f6895b3004d94df822612d346`.
- `check.py`: SHA-256 `3b0b99420527fd7d26b4e5d9e7f780be1728d6a45176517c7366eea7e9d901c7`.

Neither the normal nor optimized checker command has been independently reproduced by this correction author. The commands in the theorem note are instructions, not retained execution receipts. The checker's introductory universal wording is historical; its eight methods contain finite checks. In particular, its 832 branch comparisons cover the displayed finite parents and only eight comparisons materialize full 256-by-256 superoperators. Its spectral examples are \(n=2,3,4,5\). Its Lüders perturbation check visits 32 basis directions, so arbitrary linear combinations rely on the written proof. These finite checks do not repair a failed universal proof or constitute all-horizon enumeration.

The next action is distinct review of the corrected proof and scope, followed by coordinator disposition and separately admitted checker reproduction. This amendment does not authorize execution, a new research successor, physical adoption or resumption of regular work.
