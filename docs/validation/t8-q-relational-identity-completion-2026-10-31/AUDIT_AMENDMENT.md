# Audit amendment — relational-identity bridge

31 October 2026 (Pacific/Honolulu). **CORRECTION AUTHOR DRAFT; DISTINCT REVIEW AND COORDINATOR DISPOSITION REQUIRED.**

This amendment records the current scope of the companion
[`RELATIONAL_IDENTITY_BRIDGE.md`](RELATIONAL_IDENTITY_BRIDGE.md) after the manual
integration audit. It preserves the prospective contract and makes its unmet
parts visible. It does not itself adopt a scientific claim or report a test run.

The audited original is commit
`50be57d85aab1bf0396143694b4f9c32632010de`. The protocol commit `2631552` precedes
the original result commit `2e68a48`; that proves committed source order, not
the time of every derivation or execution. Original files remain recoverable at
the pinned commit. The protocol and checker in this directory are unchanged:

| Source | SHA-256 at the audited commit |
| --- | --- |
| `PROTOCOL.md` | `f66ebc53e5be10aeb5422c1d81005bde5a4b8c6500a2c77aba6d84b645f974c6` |
| Original `RELATIONAL_IDENTITY_BRIDGE.md` | `88c3a7acdd1571c0c5f8ab6756d0f92e6b5a07244d2ba58346a4a2ef26cb90bc` |
| `check.py` | `a591981cd1fb64c144a6358860b7e705bd035693c7b5183a82621dc5320d9f96` |

The amended theorem note, together with this amendment and any subsequent
explicit coordinator disposition, governs current claims. Broader language in
the preserved protocol or checker introduction is historical scope, not a
fulfilled result.

## 1. Coarse-cell minors and the raw-ancilla obstruction

Theorem 1A is a construction on selected Walsh sections and their declared
product preparations. Its dyadic linear construction preserves dyadic
Gaussian-rational entries **when the input has them**; arbitrary complex input
entries are not thereby made rational. With the specified controls, ancillas
and cell-weight nonnegativity, the determinant catalogue gives the stated PSD
criterion. Control availability is supplied, and no physical apparatus is
derived.

The original Theorem 1A(2) incorrectly identified the encoded ancilla
`J_2(E_00)` with the raw diagonal `D_{+Z}`. Direct substitution into the section
formula instead gives `J_2(E_00)=S_H(D_{+Z})=D_{+X}`: its two raw blocks have
entries `(1,1;1,1)/4` and `(1,-1;-1,1)/4`. The corrected construction calls this
matrix `mathsf A_0`, distinct from coarse cell `A_0`, and explicitly requires
the declared silent Hadamard preparation. Only decoded `E_00` is diagonal.
The theorem input, tensor products, summary and checker-coverage description
now use that convention. The preserved protocol/checker descriptions calling
this ancilla raw diagonal do not establish the stronger preparation claim.
This is an additional prospective-preparation deviation; it does not alter
the determinant argument on the specified encoded input. The checker’s
three-dimensional minor cases use decoded `E_00`, not a raw diagonal-ancilla
substitute.

The optional final parenthetical in Theorem 1A's original proof also omitted
normalization in its ancilla-free `n=2` construction. Its integer `U_0` obeys
`U_0 U_0^T=2I`; using it unscaled doubles total mass and the determinant target.
Scaling by `1/sqrt(2)` repairs normalization but makes that matrix non-dyadic.
This optional parenthetical is removed and its route is not adopted as the
theorem's dyadic-unitary construction. The main even-`k`, prepared-ancilla
construction is unchanged. The preserved checker implements a normalized
congruence for its additional two-dimensional example; that finite check does
not establish the omitted dyadic-unitary assertion.

Theorem 1B proves an obstruction for a two-dimensional raw candidate, **two
copies**, one four-label ancilla in the stated cone, and the readout on the
**two permutation sectors**. Its controlled-unitary branches preserve the raw
ancilla mass. The more general raw `D` tensor-power target in the prospective
protocol and checker introduction is not proved. The scoped obstruction is
retained without declaring Walsh encoding necessary among all alternatives.

## 2. Local equivalence does not establish stability under all joint tests

Theorem 2A defines equivalence using exactly the single-system Clifford-control
and two-cell-readout family. It identifies the `A` coordinate and discards `c`
at that scope. It supplies a trace order unit on this operational-model
quotient, not a physical identity assertion.

Theorem 1A gives joint couplers on selected `J_n(D)` sections; for the
two-dimensional case these choose `c=0` representatives. No general proof here
shows that adding arbitrary joint couplers preserves equivalence or
recordability for every `D(A,c)` representative. A downstream theorem that
needs such a reference-complete quotient must supply that additional transfer
proof. It cannot substitute Theorem 2A plus the selected-section construction.

Theorem 2B's reference-complete CP operations and faithful probes are
additional comparison-model premises. Its identity-atomicity result and
Theorem 2C's generator-observability result compare the specified classical,
real and complex cones under those premises; they do not establish a unique
state space from bare causal posets. Theorem 2D retains its explicit positive
real metric and minimum-rank hypothesis. The original mixed-rank counterexample
remains valid when the rank condition is removed.

Here “identity” means agreement under a declared family of future tests. It
does not establish a sustained regime, an interaction contribution to physical
mass, or personal continuity. It does not complete the separate GDM007
sustaining-regime/mass question.

## 3. CP construction and the unmet rational-Kraus promise

The Choi argument and displayed Kraus representation support complete
positivity of the supplied branch maps. The latter is a **17-operator
representation**, not a claim of Kraus rank 17. Its coefficients include square
roots: at `q=2/3` and `t=1/2`, the coherent coefficient is `1/sqrt(6)`.

The protocol promised an explicit Gaussian-rational Kraus decomposition. That
construction and its verification were not supplied; the checker tests Choi
positivity rather than constructing those rational Kraus operators. The audit
therefore retains the CP result and records this prospective-contract deviation.
It does not assert that a rational decomposition is impossible, and does not
open a general Kraus-construction successor.

The active law retains the reference structural factor but adds an explicitly
chosen, context-dependent CP residual family. It is not the unchanged
scalar-passive model. Its dependence on the whole unmarked parent is permitted
by the stated proper-mark locality; it does not claim dependence on the
induced precursor alone. The homogeneous-family results, including
NM009–NM011, remain valid. “Spacelike” diamonds mean incomparable births here,
without a derived Lorentzian metric.

The four-birth endpoint contrast remains `263/1,115,136` under the supplied
family. The four-state classical mixed comparator reproduces its discrete
single-wing table. This table therefore does not by itself exclude arbitrary
classical models. The separate Bell result retains its Bell-local,
setting-independent comparison class.

## 4. Verification coverage and remaining status

This correction used manual source inspection. No import, compilation,
scientific runtime, checker invocation or normal/optimized-mode test run
was performed by the correction author. Independent execution remains a
separate coordinator obligation under the existing execution rules. A source
hash establishes identity, not successful execution or proof completeness.

The seven checker methods are finite supplements to the proofs. In particular:

- The two-dimensional minor example materializes the full raw two-copy matrix;
  the three-dimensional minor examples use reduced untwisted matrices after
  checking the selected section.
- The raw-ancilla checks select boundary states and permutation branches; they
  are not an enumeration of all controlled unitaries.
- The local quotient check explores the 24 Clifford images for a selected
  pair of representatives, not arbitrary reference extensions.
- The CP test checks cone behavior on six supplied inputs. Relabeling checks
  enumerate permutations for the first four listed parents at each of sizes
  two and three. General cone invariance and covariance rely on the written
  arguments.
- The 580 diamond comparisons and 640 marked histories belong to the declared
  finite horizon. They establish no all-horizon growth extension.

Only the theorem note and this amendment are changed by this correction.
Original protocols, checker bytes, accepted older results and other programme
lanes remain unchanged. Distinct review must examine the corrections and any
dependent uses before the coordinator decides adoption and integration.
