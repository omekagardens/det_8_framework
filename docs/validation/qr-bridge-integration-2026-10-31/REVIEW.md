# Independent correction review — QR bridge integration

31 October 2026 (Pacific/Honolulu); review observations on 1 November 2026 UTC.

**Recommendation: PASS_SCOPED_CONDITIONAL_MATHEMATICS.** The final versions
pinned below are suitable for the proposed static, conditional mathematical
integration. No remaining substantive error was identified in this bounded
manual correction review after the three additional findings below were
repaired. This is a reviewer recommendation, not the coordinator's adoption,
formal proof verification, completed protocol verification, or an execution
receipt. The companion checker sources remain **UNEXECUTED / UNREPRODUCED**
in this integration.

## Reviewer, method and guard

Reviewer: `/root/bridge_integration_preflight`. The identity corrections were
authored by `/root/bridge_identity_repair`, the Tier I corrections by
`/root/bridge_tier1_repair`, and the adoption ledger and coordination prefixes
by `/root`. This reviewer authored none of those inputs and changed only this
review file. Findings were returned to the original correction authors rather
than repaired by the reviewer.

The task was a twelve-minute manual correction audit, begun at
2026-11-01 00:10:10 UTC. I read the amended identity and Tier I notes, their
amendments, relevant original-version diffs, the proposed adoption ledger and
the four new coordination prefixes. I independently worked through the
spectral proof and the mathematical distinctions listed below. The source
inspection of the three checkers and the execution-route records from my
preceding read-only assessment was also used. This does not claim an audit of
every historical dependency or all previous coordination entries.

Fresh supported usage checks passed the shared 3% guard; detailed account
observations are retained in private coordination evidence.

## Exact versions reviewed

All paths in this table are relative to `docs/validation/`. The original
branch is pinned at `50be57d85aab1bf0396143694b4f9c32632010de`; the integration
baseline is `2af9fdcaeb6b7830a6ce94f1288dabbbcf8f60a5`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md` | 57240 | `4d3b7bd9d29a36408224bab7a0e37d00d4e9ee08ec38b193d33bfc7ca9c7fd25` |
| `t8-q-relational-identity-completion-2026-10-31/AUDIT_AMENDMENT.md` | 8814 | `ccd8686309986de95a86708753a551b9a7916b375db63cdd775ce53651c84def` |
| `t8-q-tier1-foundational-closure-2026-10-31/TIER1_CLOSURE_THEOREMS.md` | 72184 | `69697362a5826758b4de502ca60a55ee8e8572c2718fbf1a679d68e46de71154` |
| `t8-q-tier1-foundational-closure-2026-10-31/AUDIT_AMENDMENT.md` | 6173 | `3438b471267925180c9ed2dc15d77a863f750908ae4a7782b959c3369d289201` |
| `t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md` | 39007 | `843f2a2cbe3fa45a2ea61c2e3170089f97c5c9c28beea695c7ce74ed939075f2` |
| `qr-bridge-integration-2026-10-31/ADOPTION.md` | 9255 | `2f1f8463cefe54d72845340775d0ceddd0202ed6ae2c77e20a59ec7c4e681b6f` |

The last ledger version is explicitly `PENDING_CORRECTION_REVIEW`. Subsequent
coordinator status/disposition changes are not included in its hash above.
Any new scientific claim or changed premise would require further review.
The source manifest was awaiting regeneration after the late fixes; this
review does not endorse an earlier manifest as the final source inventory.

Unchanged protocol and checker identities:

| Package | Protocol SHA-256 | Checker SHA-256 |
| --- | --- | --- |
| Pair bridge | `45995746829d9a7cb91dfcf500a42dca537791e274d76d3ec634a04a1fe8ebee` | `7cce895f6ff26d52dcf0d069f4b6b5e020f1485d2fa04c4d198555fcf32e0f4a` |
| Identity bridge | `f66ebc53e5be10aeb5422c1d81005bde5a4b8c6500a2c77aba6d84b645f974c6` | `a591981cd1fb64c144a6358860b7e705bd035693c7b5183a82621dc5320d9f96` |
| Tier I | `754d88d3af8f0c003e4a9c4a21a959e7fd8d203f6895b3004d94df822612d346` | `3b0b99420527fd7d26b4e5d9e7f780be1728d6a45176517c7366eea7e9d901c7` |

## Additional findings raised and resolved during independent review

1. **Tier I Walsh normalization.** The initially frozen correction still said
   that the integer-Walsh inverse tensor fixes the joint vector. In fact
   `H_2^{-1} tensor H_2^{-1} = (H tensor H)/2` scales it by one half.
   The final text correctly uses the normalized Hadamard and matches the
   internal blocks explicitly: `(H_2 tensor H_2) sigma
   (H_2 tensor H_2)/16 = sigma/4`. I rechecked the prefactors. The intended
   `N' = (J_2 tensor J_2)(sigma)` identity survives.
2. **Encoded ancilla versus raw diagonal preparation.** The initial identity
   correction conflated `J_2(E_00)` with raw diagonal `D_{+Z}`. Substituting
   into the displayed section gives the two blocks
   `(1,1;1,1)/4` and `(1,-1;-1,1)/4`, namely
   `J_2(E_00) = S_H(D_{+Z}) = D_{+X}`. The final note calls it a distinct
   encoded ancilla, requires its Hadamard preparation, and propagates this
   premise through the tensor inputs, summary and coverage description. The
   raw diagonal resource is not silently substituted. The adoption ledger
   now carries the same distinction.
3. **Optional ancilla-free integer coupler.** A final parenthetical claimed a
   determinant readout using integer `U_0` with `U_0 U_0^T = 2I` without its
   normalization. Unscaled, this doubles mass and the determinant weight.
   Normalizing by `1/sqrt(2)` produces a unitary matrix but not a dyadic one.
   The author removed this optional parenthetical and recorded its
   non-adoption. I verified its removal. The main even-`k`, prepared-ancilla
   construction and its dyadic unitary are unaffected.

The original correction freezes were not adopted: the identity note at
`246afd759e6636c9a04bd786487c279fd34b8c74bf79bc48200e02677ffcd094`
and Tier I note at
`dfd78f6c34d69a4df7fa8f53843d8b5904235a4aeeca5966ba72aebdd8fc8ed2`
were replaced, and the intermediate identity ancilla repair was further
revised for finding 3. The final-version table, rather than mixed revisions,
defines this recommendation.

## Manual mathematical assessment

**General spectral proof.** For `z_r = exp(-i(2r+1)pi/m)` and
`v_{r,j}=z_r^j`, the finite geometric sum gives
`T_m v_r = ((1+z_r)/(1-z_r)) v_r`; multiplication by `i` gives the stated
cotangent eigenvalue. The `m` distinct values give the full spectrum, with
extrema `+Lambda_m` and `-Lambda_m`. Thus the negative eigenvalue of the
candidate comes from `r=n-1`, not `r=0`. For `n>=3`, strict increase of
`Lambda_m` makes the declared rational-parameter interval nonempty and every
proper principal restriction strictly positive. Two nonpositive eigenvalues
would span a two-dimensional nonpositive subspace intersecting a positive
codimension-one coordinate restriction, a contradiction. Exactly one
eigenvalue is negative and all others are positive, so the determinant is
negative. The separate `n=2` eigenvalues `1/2 +/- t_2` avoid division by zero.
This repairs the general argument; the finite `n=2,3,4,5` examples alone
would not. The conclusion remains a principal-minor-sign catalogue bound.

**Growth and diamonds.** The unanchored cancellation argument requires
full unnormalized branch-map diamonds on the entire residual space, with
strictly positive matching scalar factors. The revised statement supplies
that premise; scalar diamonds alone cannot do the job. The anchored
construction uses separately supplied origin marks and tensor-local
instruments. Its order incomparability is not a spacetime metric. The
identity candidate's context-dependent CP maps do not refute the previously
restricted homogeneous families, and its finite single-wing contrast has the
stated classical comparator. No physical control availability follows.

**Dimension and degree.** In the multiplicative polynomial argument,
`d(2x)=d(2)d(x)` forces a single monomial and `d(1)=1` fixes its coefficient.
The supplied `d(2)<=4` bound leaves powers one and two; the binomial/Stirling
coefficients follow. This identifies dimensions and coefficients, not cones,
effects or composition. The separate amplitude-family argument uses its
localized preparation and rotated partition-conservation premise to force
degree two. Those premises are not inferred from dimension counting.

**Selective update and readout arithmetic.** Positivity and calibrated trace
annihilate the complementary block; non-disturbance on the entire repeat face
fixes the retained block. Positivity of `t^2 |psi><psi| + t X` for every real
`t` forces each quadratic form of Hermitian `X` to vanish, including the
imaginary cross-block directions. The arbitrary-projector Lüders uniqueness
argument therefore survives. The displayed dyadic-real operational lift is
only for coordinate projectors. The actual three Pythagorean controls recover
four real repeat-face coordinates; they are not the frozen protocol's
purported four controls. The probability inverse and Frobenius bound are
valid analytically for real estimates and errors. Exact rational certificate
arithmetic needs rational data and bounds/enclosures.

**Walsh section, quotient and CP scope.** The signed-permutation determinant
sum and padded-coordinate mass argument apply to the explicitly selected
sections and prepared ancillas. The raw-ancilla kernel-overlap proof supports
only its two-dimensional, two-copy, two-permutation-sector obstruction.
The local test quotient identifies `A` and discards `c`; it does not establish
stability under arbitrary joint tests on every representative. Reference-
complete CP and faithful-probe assumptions must be transferred separately.
The displayed Choi/Kraus arguments support the supplied CP maps but do not
deliver the promised Gaussian-rational Kraus decomposition. A 17-operator
representation is not Kraus rank 17. These restrictions are present in both
amendments and in the proposed ledger.

**First-package clarification and supplemental review.** I independently
checked the small final diff and its exact pin: whole-carrier contractions of
the stated bilinear formula give `M(E)D` and `M(D)E`, reducing to `D,E` on
normalized inputs. The notice accurately preserves all-real-rectangular-map
naturality and the unexecuted-source boundary. The coordinator separately
relayed a broader first-package proof review by
`/root/bridge_tier1_repair`, who did not author that first package. That
reported supplemental review is not presented as my re-performance of the
entire first-package audit, nor as independent review of that agent's own
Tier I corrections; the latter are reviewed here by me.

## Protocol, execution and integration disposition

The amendments truthfully preserve unmet prospective promises: the broader
raw obstruction, arbitrary-reference quotient extension, Gaussian-rational
Kraus construction, arbitrary-projector dyadic lift, the control-family
substitution, preparation correction, and normal/optimized checker runs.
Committed protocol-before-result order establishes source history, not
independently observed reasoning chronology. None of these deviations is
retroactively declared fulfilled.

The suites have 8, 7 and 8 named tests. Their source is finite evidence design,
not executed evidence here. The pair suite includes a 1024-by-1024 exact
matrix and a rank calculation with sectors supplied by the written proof.
Identity uses selected reduced matrices, covariance representatives and 580
finite diamond comparisons. Tier I has 832 selected branch comparisons,
including eight full 256-by-256 superoperator pairs; its 32 perturbation basis
checks do not prove the arbitrary-combination Lüders statement. No checker,
scientific script, import, compilation, test or benchmark was run in this
review or my preceding admission assessment.

No admitted execution route for these new suites was established. The
previously inspected `SHARED_ROUTE.json`
(`47354a01193793a6aa53827b1d8a1e9adb8b1a642e2d51f64a35b612f3fe2d2a`)
records a selected-route gap. RET019's preparation contract
(`0f1e20f1bb12c20909bcf22b8764b7e09ac32333d0a07204f1c077069a770bf0`)
targets six different RET016 cases. Its 60-second outer, 30-second CPU and
output policies cannot simply be transferred to these suites; it supplies
no demonstrated binding for this execution. A branch-specific contract must
name exact runtime/source pins, commands and budgets, memory/output policy,
outer coverage from bootstrap to final exit, and cleanup of the owned process
group after observer failure. Tool yield and returned-token limits are not
those controls. This is neither a universal execution prohibition nor a
claim of host impossibility. RET5858 and actual execution gates remain.

The proposed `ADOPTION.md` is suitable at its pinned scope: it preserves the
raw-domain obstruction, conditional physical premises, unaccepted GDM007
state and separate programme objectives. The first 19 lines of each following
coordination file are consistent with it; historical bodies were not
re-audited:

| Repository path | SHA-256 of observed complete file |
| --- | --- |
| `REVIEW_IMPLEMENTATION_PLAN.md` | `ffa17377f0e0b40013c2e9d57f95a05da64990572dc67815dcfc1ff4d631d1ef` |
| `docs/coordination/REVIEW_PROGRESS.md` | `791c28ee7106079ac935d52b3eace5c3b76956a3d1790f834513ac8cd14d7eea` |
| `docs/coordination/QR_HANDOFF.md` | `8c787337f3fd653f0c5c1c9c441bb98f43bf89ebb37afdad19a06f1ad0cdeee6` |
| `docs/coordination/OPERATIONAL_PREMISE_LEDGER.md` | `5631211165987d1433773611bdd310ce4ed847b13c97d14cc631f8c61cfe6921` |

Accordingly, recommend coordinator disposition and scoped integration of the
reviewed conditional mathematics with explicitly unreproduced companion
source. This review does not authorize scientific execution, physical
adoption, a schedule change, or automatic successor work. The regular-work
hold remains through the audited merge and coordinator reconciliation.
Hashes establish identity, not scientific acceptance or semantic completeness.
