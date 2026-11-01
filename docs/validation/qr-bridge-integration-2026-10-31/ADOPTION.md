# QR bridge integration: conditional results and remaining obligations

31 October 2026 (Pacific/Honolulu). **ACCEPTED_SCOPED_CONDITIONAL_MATHEMATICS; CHECKER_REPRODUCTION_OPEN.**

Coordinator disposition at 2026-11-01 00:16:33 UTC (31 October 14:16:33 HST): accept the exact corrected theorem sources recommended in [REVIEW.md](REVIEW.md), with every qualification and unfulfilled verification obligation below. The independent reviewer did not author the corrections. This status update adopts no additional scientific claim.

This is the coordinator's current claim and premise ledger for the three
packages introduced by `qr-pair-kernel-bridge` at
`50be57d85aab1bf0396143694b4f9c32632010de`. The integration baseline is
`2af9fdcaeb6b7830a6ce94f1288dabbbcf8f60a5`. Six commits added nine files;
the original protocols and checker sources are preserved unchanged. Committed
protocol-before-result order establishes source history, not independently
observed reasoning or execution chronology. Original versions remain in Git.

The coordinator adopts **conditional mathematics only**, with the
qualifications below. It is not blanket acceptance of “all foundational gaps
closed,” a formal proof verification, completed protocol verification, or
empirical validation. The [source manifest](SOURCE_MANIFEST.json) establishes
identity and direct-link coverage; it does not establish semantic completeness
or acceptance of every dependency.

## Results and their exact scope

| Result | Admitted premises and conclusion | Boundary retained |
| --- | --- | --- |
| [Pair bridge, Theorem 1](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) | Complex Hermitian, real-bilinear composition, unit and naturality under **all real rectangular maps** give a one-parameter family; declared phase-control interchange selects the tensor product. | Boolean grouping alone is weaker than the real-map premise; neither the field nor physical controls are derived. RI-22's weaker-premise countermodel remains valid. |
| Pair bridge, Theorem 2 | Single-copy additivity plus nonzero composition coefficient and two-copy coincidence grouping force complex cross-cell decoherence. | Cell sums do not eliminate hidden zero-sum cross-block payload. |
| Pair bridge, Theorem 3 | A supplied Hadamard operation creates a normalized determinant-witness seed from a diagonal preparation; declared bipartite controls give CHSH 14/5. | The first determinant witness addresses sub-cell atoms. CHSH excludes the stated Bell-local, setting-independent comparator; the mixed-state classical single-system counterexample remains. |
| [Identity bridge, Theorem 1](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md) | The trace-normalized Walsh section, its Hadamard-prepared ancillas and explicitly supplied joint couplers turn principal minors into coarse-cell weights. | The encoded ancilla is diagonal in decoded coordinates, not on the raw four-label carrier. This changes the encoded domain and admitted controls. The raw obstruction is only the proved two-copy, two-dimensional, two-permutation-sector case. |
| Identity bridge, Theorem 2 | The declared single-system test quotient has complex-qubit trace geometry. Further selection results retain identity-atomicity, generator-observability and minimum-rank premises. | Joint-test/reference completeness for every representative of the larger cone is unproved. Operational future-test equivalence does not establish enduring physical or personal identity. |
| Identity bridge, Theorem 3 | A new context-dependent CP candidate gives a finite four-birth probability contrast 263/1,115,136 with the stated full-map diamonds. | It is not the old scalar-passive model and does not refute the homogeneous-family results NM009–NM011. A four-state classical model matches the selected single-wing table. The promised Gaussian-rational Kraus construction is not delivered. |
| [Tier I, Theorem 1](../t8-q-tier1-foundational-closure-2026-10-31/TIER1_CLOSURE_THEOREMS.md) | Full branch-map diamonds are required for the unanchored commutation obstruction. The separately anchored tensor-local construction supplies conditional Bell birth probabilities. | Scalar diamonds alone are insufficient. “Spacelike” means order-incomparable here, without Lorentzian geometry. The PR-box counterexample shows the role of subsystem locality. |
| Tier I, Theorem 2 | The specified amplitude-scaling/conservation family selects degree two. Multiplicative polynomial dimension with the supplied d(2) bound selects n or n². | Dimension does not identify a positive cone, effect family, composition rule or complete quantum theory. |
| Tier I, Theorem 3 | Positivity, calibrated effect and non-disturbance on the **entire repeat face** select the Lüders map for arbitrary projectors. | Ordinary repeatability is insufficient. The explicit dyadic operational lift is restricted to coordinate/coarse-cell projectors. |
| Tier I, Theorem 4 | The corrected spectral argument supplies the stated proper-minor counterexample, including a separate n=2 case. The encoded trace-domain probability catalogue has an explicit inverse and error bound. | The copy obstruction concerns the stated minor-sign catalogue, not every measurement strategy. Exact rational certificates require rational data/enclosures. The raw-domain RI-23 obstruction remains valid. |

The [identity amendment](../t8-q-relational-identity-completion-2026-10-31/AUDIT_AMENDMENT.md)
and [Tier I amendment](../t8-q-tier1-foundational-closure-2026-10-31/AUDIT_AMENDMENT.md)
record corrections and prospective-contract deviations. They preserve the
original promises as history rather than declaring them fulfilled retroactively.

## Verification and execution boundary

The original spectral argument had an incorrectly oriented eigenvector and a
false bound that included the negative extremal eigenvalue. Finite examples
cannot repair that all-dimension proof. Its corrected argument passed
distinct mathematical review, recorded with the other corrections in
[REVIEW.md](REVIEW.md).

The three unchanged standard-library checker suites contain 8, 7 and 8 named
tests. **No checker was independently executed, imported or compiled during
this integration.** Commands in the original notes and matching source hashes
are not execution receipts. The prospective requirement for normal and `-O`
runs remains unfulfilled by this audit. These sources are published as
unreproduced companion checkers, not passing or resource-qualified software.

Static coverage is finite: the first suite's rank calculation pre-imposes
sectors justified in its written proof and includes a 1024×1024 matrix; the
identity suite uses reduced matrices for selected n=3 examples and samples
covariance representatives; Tier I's 832 finite comparisons include eight
full 256×256 superoperator pairs. Its 32 Lüders basis directions do not alone
prove the universal statement. Universal conclusions depend on the proofs.

No reusable admitted runner for these new suites was established. The existing
RET019 preparation contract covers six different RET016 cases and cannot be
transferred. A branch-specific contract still needs exact checker/runtime
pins, normal/optimized commands, wall/CPU/output and memory policies, and a
supported runner binding covering bootstrap through final exit and owned
process cleanup after observer failure. Tool yield time and displayed-output
limits are not those guarantees. This is a specific execution limitation,
not a claim that the host cannot run Python or that RET5858 bans all scripts.

Manual proof adoption and publication of explicitly unexecuted source are
separate from that executable qualification. No benchmark, speed, memory,
calibration, production or physical-readiness claim is made.

## Programme reconciliation

These results connect several formerly separate conditional obligations.
Do not reassign tensor selection, coincidence decoherence, the selected
coarse-cell witness, or the stated Lüders uniqueness problem under the same
premises merely because an older summary lists them as open. Different
domains or weaker premises remain different questions. Older accepted
countermodels and dispositions are retained, not overwritten.

The raw RI-23 obstruction, joint-test quotient extension, rational Kraus
promise and checker reproduction are explicit remaining obligations, with
no automatic infrastructure or theory successor. The full native ontology,
complex-field selection, physical control availability, physical calibration,
native energy/mass/gravity and continuum limits remain distinct.

The sustaining-regime/mass objective remains active programme intent.
GDM007's author run was interrupted by a platform limit before final
verification and handoff; its result remains unaccepted. This quantum
equivalence package does not complete that assignment. After the audited
merge and coordinator reconciliation, QR is the relevant first consumer for
assessing that preserved work. Measurement, Relational State, Energy,
Comp-Sci and RET receive no automatic task merely from this integration;
physical instruments, data, calibration and their execution gates are not
supplied by a mathematical probability catalogue. Free Thinker material and
personal journals are outside this publication.

The coordinator has reconciled the programme above and authorizes release of
the integration-specific hold only after this reviewed revision is merged and
the remote target is verified. QR is the first relevant recipient for bounded
recovery of its preserved, unaccepted GDM007 package; this does not adopt that
result or authorize new derivation under an expired budget. Other tracks
retain their actual input and execution blockers and receive no automatic
successor. Resumption remains subject to the shared 3% usage guard and all
independent-review, custody and execution requirements. Schedules and model
settings are unchanged.
