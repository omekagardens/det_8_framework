# QR-05 concurrent-branch audit and selective reconciliation

12 September 2026 (Pacific/Honolulu). **Decision: selectively adapt useful mathematics;
do not merge the concurrent branch or inherit its gate-completion and physical-closure
claims.** The main working checkout remains authoritative. This report is an audit and
adoption record, not an experimental validation of DET, a geometry-emergence result, or
an apparatus-readiness certificate.

## 1. Sources, scope and meaning of the review

The reviewed source is the immutable `qr-05-bridge` commit
[`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`](https://github.com/omekagardens/det_8_framework/tree/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8),
compared with the main checkout's QR-05BV baseline
[`8b34191a8d05966cb8f60e856bfdbf1e30c2da45`](https://github.com/omekagardens/det_8_framework/tree/8b34191a8d05966cb8f60e856bfdbf1e30c2da45).
The concurrent branch contains 51 intervening commits and 45 gate directories,
QR-05BW through QR-05DO: 39 executable gates and six design-only gates. The complete
diff spans 380 files, with 46,974 inserted and 28 deleted lines. Those figures describe
scope, not evidential strength.

The review combined:

- A metadata inventory of all 45 gate directories and the executable gates' stored
  sources, freezes and captures.
- Targeted reading of research contracts, implementations, tests and summaries, with
  independent checks of central mathematical implications.
- Selective execution of 18 existing suites: **194 tests passed** in an isolated archive
  of the pinned commit. No historical captures or freezes were rewritten.
- New bounded diagnostic calculations and exact counterexamples where the existing
  suites did not test the claimed implication.
- Comparison of physical operator/state names with primary literature.

This is **not exhaustive verification of all 39 executable gates**, every historical
claim, every input configuration, or the branch's repository-wide test suite. Test
counts below must not be read as 45 accepted gates. Several significant conclusions
are false despite their tests passing.

| Selectively executed suites | Tests passed |
|---|---:|
| CA, CB, CC, CE | 11 + 9 + 10 + 7 = 37 |
| DC, CR, CY | 13 + 8 + 11 = 32 |
| DE, DF, DG, DH, DN | 11 + 10 + 9 + 10 + 18 = 58 |
| DI, DJ, DK, DL, DM, DO | 10 + 10 + 9 + 11 + 12 + 15 = 67 |
| Total: 18 suites | 194 |

The concurrent branch is useful exploratory work. It assembles relevant questions,
small examples, model distinctions and potential verification targets. Its strongest
contribution is not that it has finished the physical bridge, but that it exposes
concrete structures which can be narrowed, corrected and tested independently here.

## 2. Adoption decision and protection of the main checkout

No wholesale merge, cherry-pick series, supported-core promotion, or automatic transfer
of BW–DO completion labels is warranted. In particular, the concurrent DN edit to
`det8/claims.py` overlaps the independently dirty core/RET work in this checkout and is
withheld. Existing core, RET and application changes remain owned by their workstreams.

The appropriate unit of adoption is a **precisely stated result**, with its assumptions,
domain, proof or independent test, and failure cases—not a passing flag or a gate name.

| Material from the concurrent branch | Reconciliation decision |
|---|---|
| Observational equivalence and channel separation | Adopt as a finite common-world calculus, with explicit nonidentifiability witnesses. |
| Reference/production/model distinction | Adopt as a calibration-evidence contract; retain every unsupplied physical premise. |
| Positive path-sum support on a finite poset | Retain as elementary combinatorics, not continuum light-cone reconstruction. |
| Positivity obstruction for the naive pair kernel | Retain the proof; repair fixture and spectral-bound details. |
| SJ positive-part matrix construction | Retain the finite linear-algebra theorem; separate it from the wrongly named operator and geometry claims. |
| E closed; conformal geometry identified by the real kernel | Do not adopt. The claimed implications are unsupported or contradicted. |
| DN correspondence-registration intent | Retain the nonpromotion principle; defer registry integration and repair its checks. |
| Gate counts, repeated route agreement and passed suites | Retain as provenance/diagnostics only, not proofs of untested implications. |

The local follow-on is specified in [CALCULUS.md](CALCULUS.md): a bounded, ontology-free
measurement-channel utility on one common finite world class. Its first frozen
verification passes 19 tests in each normal/optimized mode and three exact full-report
replays, including Python 3.11. See [local results](RESULTS.md). This is separate from
the 194 archived-branch tests and does not validate the concurrent branch wholesale.

## 3. Additional calibration, geometry and growth findings

The highest-impact findings outside the pair-kernel sequence are summarized here.
The linked reports give pinned source locations, explicit counterexamples, scope
limits and proposed repairs. These are reasons to narrow or withhold a conclusion,
not reasons to dismiss the branch's entire research direction.

| Gate(s) | Finding | Local disposition |
|---|---|---|
| BW/BX | Valid marginal failure bounds compose by union bound without independence; population/estimate meanings are mixed, and probability distortion cannot be unbounded | Corrected conditional calibration contract; physical reference evidence remains absent |
| CA | Seal omits analysis-changing `case`; inverse uses point frequencies and a finite nuisance list; metric/dynamics statuses echo supplied flags | Retain as synthetic plumbing only, not the hardened BV inference or physical verification |
| CE | Curve half-range is not a general CHSH witness: a deterministic local correlation matrix passes its visibility threshold | Retain descriptive curve calculations; require an actual four-correlator/statistical contract |
| CR | A moment identity is checked for the pointwise operator, while the selected conservative operator has a different coefficient | Repair the actual divergence-kernel moment audit before reuse |
| CU–CZ | Trimmed mean is not a supremum bound; an optimum over bijections is not the unrestricted correspondence infimum | Rename finite diagnostics; retain CZ's genuine directed-distance correction |
| DC | A valid three-chain distance exceeds the closure of its link weights; the asserted universal reduction is false | Retain all-pair max-plus closure, not the link-only characterization or mixed-family closure |
| DD | The report fits `U/mean_L` instead of declared `ell U`; a finite fit does not prove uniform convergence | Define normalization/noncollapse and retain the selected trend without a convergence promotion |
| CY/DO | Identification on separate one-variable families does not imply joint identification; one conformal world mixes two sampled panels | Rebuild on one common world class; explicitly label the injected scale oracle |
| DI–DM | Interpolation is not a matched realization; chosen thresholds can reject a genuine Minkowski sample; a no-go flag has an invalid trigger | Retain exploratory profiles and stronger adversary construction; require whole-realization null calibration or a proof |
| DJ/DL | Record association is not a covariance violation; DL's repaired density still has a stale zero-density verdict | Keep correctly scoped diagnostics and the preserved correction history |

Details: [calibration, acquisition and Bell data](AUDIT_CALIBRATION.md),
[geometry and operators](AUDIT_GEOMETRY.md), and
[growth and anchors](AUDIT_GROWTH_ANCHORS.md).
The Bell audit does not claim the underlying experiment failed its own Bell test;
the growth diagnostic is not a false-positive-rate estimate. Small exact counterexamples
are stronger evidence against the specific universal implications than passing
fixtures are evidence for them.

## 4. Pair-kernel and state sequence: blocking mathematical findings

### P1. QR-05DH's operator is not the cited Benincasa–Dowker operator

The [DH implementation](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/primary.py#L73-L83)
uses binomial layer coefficients, and its
[contract](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/README.md#L16-L25)
calls the result Benincasa–Dowker (BD), with layer count and normalization treated as
conventions. For the frozen value N = 3, the implemented matrix is

`B_toy = -I + 3 A_1 - 3 A_2 + A_3`,

where A_k selects comparable pairs containing k−1 intervening elements. With the
diagonal normalized to −1, the standard two-dimensional layer expression is

`B_2,norm = -I + 2 A_1 - 4 A_2 + 2 A_3`.

The four-dimensional expression, again displaying the dimensionless bracket with
diagonal −1, is

`B_4,norm = -I + A_1 - 9 A_2 + 16 A_3 - 8 A_4`.

The two-dimensional expression is given in
[Sorkin, equations (1)–(2)](https://arxiv.org/html/gr-qc/0703099); the four-dimensional
one, including its length-dependent prefactor, in
[Benincasa–Dowker, equation (2)](https://arxiv.org/html/1001.2725v4).
No overall scalar can turn the implemented coefficient ratios into these ratios.
The layer count is also part of the dimension-specific construction, not a freely
interchangeable convention.

**Consequence:** the captured experiment is a binomial-layer toy calculation, not the
claimed implementation of a sourced physical BD operator. Positivity of a subsequently
constructed matrix does not repair that misidentification.

**Resolution:** preserve the toy only under its actual name. A future physical-operator
gate must specify dimension, coefficients, normalization, density/length scale, domain
and boundaries, then verify those quantities independently before attaching BD or
Klein–Gordon interpretations.

### P2. DH's exact support and orientation claims have small counterexamples

The [DH contract](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/README.md#L29-L30)
asserts nonzero Pauli–Jordan entries exactly at causal pairs, with sign recovering
orientation. Its [result explanation](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/RESULTS.md#L15-L19)
infers nonzero entries from triangularity. That implication is invalid: triangularity
and incidence-algebra support constrain where entries may occur; they do not exclude
cancellation among contributions at an allowed pair.

Use the already included three-chain, 0≺1≺2, and write a = 1+m². Its implemented matrix
and the decisive inverse entry are

```text
B_toy - m² I = [ -a   0   0 ]
               [  3  -a   0 ]
               [ -3   3  -a ]

G_20 = 3(a-3)/a³,      G_10 = G_21 = -3/a².
```

For Δ = G−Gᵀ:

- At m² = 2, a = 3 and Δ_02 = 0 exactly, although 0≺2.
- At m = 2, a = 5 and Δ_01 = 3/25 > 0 while Δ_02 = −6/125 < 0. Both pairs have
  the same forward orientation. This sign failure occurs at a mass already in the
  frozen experiment.

Independent diagnostics reproduced both facts in both routes. At the floating input
m = √2, both returned Δ_02 approximately −7.4×10⁻¹⁷; the exact rational calculation at
a = 3 gives zero. At m = 2, both returned approximately +0.12 and −0.048 for the two
forward entries.

The [actual test inside the report builder](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/primary.py#L245-L257)
checks absolute nonzero support at only four masses; it never checks the claimed sign.
Thus its passing flags do not test the stronger statement printed in the prose.

The physical distinction is important too. Johnston's continuum massive 1+1 retarded
propagator contains a Bessel J₀ factor, so zeros and sign changes are possible inside
the causal region; the massless 3+1 expression is supported on the null boundary rather
than every timelike pair. These are direct cautions against turning causal support
containment into pointwise equality or orientation recovery.
[Johnston, equations (3), (7)](https://arxiv.org/html/0909.0944v2).

**Resolution:** state causal-support containment as the general result. Demand a
separate noncancellation theorem wherever equality is needed. Preserve the exact
three-chain cancellation and sign reversal as mandatory regressions, not as numerical
noise or setup defects.

### P3. The symmetric SJ covariance is not identified with conformal geometry

DH's [physical reading](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dh-sj-vacuum-bd-2026-09-11/README.md#L50-L56)
and the [E synthesis](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/track_b/E_PAIR_KERNEL_GEOMETRY.md)
identify the conformal part with |Δ| = √(−Δ²). Neither symmetry nor invariance under
Δ↦−Δ establishes such an identification.

The operator absolute value is not the entrywise absolute value. On DH's V fixture,
0≺1 and 0≺2 with incomparable leaves 1 and 2, at m = 0 one has

```text
Δ = [  0   3   3 ]
    [ -3   0   0 ]
    [ -3   0   0 ].
```

Its SJ covariance satisfies

`Re W_12 = 3/(2√2) > 0`,

although 1 and 2 are incomparable. Both routes returned approximately 1.06066017.
Spectral square roots can therefore introduce covariance support at spacelike pairs;
this is not itself a violation of microcausality, which concerns the commutator.
Furthermore, changing the model's mass changes |Δ| without changing its supplied order.
An orientation-invariant matrix is not thereby a recovered conformal class.

**Resolution:** use the precise term *symmetric state covariance*. A geometry claim
needs an explicit reconstruction map, an equivalence relation, a domain of admissible
models and a proof of identification. Those requirements remain open here.

### P4. DE's named diamond is not transitive

Both [DE primary](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05de-pair-kernel-orientation-2026-09-11/primary.py#L140-L143)
and its [reference](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05de-pair-kernel-orientation-2026-09-11/reference.py)
construct the named diamond from four cover edges but omit the transitive relation
0≺3. This is a Hasse graph passed as if it were an order matrix.

The published r* = 0.50 belongs to that invalid relation. For the actual transitive
four-element diamond, the operator norm of iΩ is √5, so the exact upper endpoint is

`r* = 1/√5 ≈ 0.4472135955`.

Both existing implementations return 0.44 on their 0.01 grid after adding the missing
relation, instead of the published 0.50. Their agreement therefore shares a fixture
error. The exhaustive enumeration results and the separately hand-built example must
not be conflated.

**Resolution:** validate every fixture's order axioms; distinguish cover matrices from
transitive order matrices. Report exact spectral bounds separately from lower grid
approximations. The V and three-chain displayed values are also grid values, not their
exact thresholds.

### P5. Magnitude blindness does not prove full-kernel nonidentifiability

The [DE consequence](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05de-pair-kernel-orientation-2026-09-11/RESULTS.md#L57-L73)
and the E synthesis infer that the kernel and order are necessarily nonredundant from
the time-reversal blindness of kernel magnitudes. That changes the observation map in
mid-argument: magnitude-only observations discard information which the full complex
kernel retains.

Indeed the branch's own family, `D_r = I + i r Ω`, recovers the directed relation by
`Im(D_r[i,j]) > 0` for every r>0, where Ω_ij is +1 for i≺j, −1 for j≺i and zero
otherwise. The exact PSD requirement is

`r ||iΩ||_op ≤ 1`.

For any finite nontrivial order a sufficiently small positive r exists. For n>0,
dividing by n also gives a normalized finite additive event kernel: the antisymmetric
entries sum to zero, so `D_r(X,X)/n = 1`. This is an explicit mathematical encoding of
order; it is not an ontological or physical derivation of that order.

The valid negative result is narrower: **the elementwise magnitudes of these specified
kernels do not distinguish an order from its reversal on fixed labels.** It neither
rules out full-kernel reconstruction nor proves that nature needs two independent
primitives. Conversely, the existence of an encoding does not show that a physical
kernel must carry that encoding.

**Resolution:** formulate each recovery question using a fixed observation map and
world class. Retain the positivity coupling as a construction-dependent constraint,
not a theorem of ontological nonredundancy. Do not adopt E's closure on this argument.

### P6. DG's grid does not establish a physical critical mass

The [DG model and results](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dg-sorkin-johnston-2026-09-11/README.md)
use `G_R = (I−exp(−m)L)⁻¹` and set the symmetric part to `G_R+G_Rᵀ`. This is an
explicit toy family. It is not the sourced causal-set scalar propagator: Johnston's
2D and 4D formulas respectively use `aC(I−abC)⁻¹` and `aL(I−abL)⁻¹`, with
`b=−m²/ρ` and dimension-specific a. Here C is the strict causal matrix and L the
link matrix. [Johnston, equations (16)–(17)](https://arxiv.org/html/0909.0944v2).

DG's reported critical masses are only the first passing values on its five-point
grid. It neither solves for exact thresholds nor justifies interpreting the damping
parameter as an experimentally calibrated physical mass. Its statement that light
fields require this IR regularization is not established. DH recognizes the
naive-symmetrization artifact, but the older physical assertions remain in the
concurrent E synthesis and should not survive reconciliation.

**Resolution:** keep this, if useful, as a damping-parameter experiment for a named
toy kernel. Remove its physical critical-mass conclusion.

## 5. What survives in the pair-kernel mathematics

The errors above do not erase the sound finite structures:

1. **Naive-glue obstruction.** For a comparable pair, the Hermitian principal block
   `[[1,1+i],[1−i,1]]` has determinant −1. Consequently the branch's particular
   `C+iΩ` construction is PSD only for an antichain. This is an elementary proof,
   not a fitted observation.
2. **Spectral orientation budget.** `I+i r Ω` is PSD exactly within the spectral
   constraint in P5. This is useful for constructing and testing admissible finite
   kernels, once valid order fixtures and exact/grid distinctions are enforced.
3. **Positive link-path support.** For a finite poset's cover matrix L, the finite
   path sum `K=I+L+⋯+L^(n−1)` has K_ij>0 off the diagonal exactly when i≺j.
   Every comparable pair is connected by a cover chain and every summand is
   nonnegative. This proof applies to DF's combinatorial path sum; it does not
   transfer unchanged to signed inverses such as DH's.
4. **SJ positive part.** For any real antisymmetric finite Δ,
   `W=Pos(iΔ)=(√(−Δ²)+iΔ)/2` is Hermitian PSD and has `W−conj(W)=iΔ`.
   Time reversal Δ↦−Δ gives the conjugate W. This is valid spectral mathematics,
   independently of whether Δ arose from a physically correct operator.

The last construction is a distinguished prescription, not uniqueness among all PSD
matrices having the same commutator: `W+tI`, t>0, gives immediate alternatives.
A physical or axiomatic uniqueness statement must include the additional conditions
that select the SJ state and the field-space inner product. The cited
[Jones analysis](https://arxiv.org/html/2412.07832v1) makes physical assumptions and an
L² field-space choice explicit. Those assumptions are not derived by DH's PSD tests.
Neither a normalized histories decoherence functional nor an observational interface
should be silently identified with a Wightman covariance merely because each admits
a positive-matrix representation.

The correct opportunity is therefore a disciplined connection between finite order,
admissible kernels and positive covariances. It remains conditional on the supplied
structures; it is not the claimed physical closure of E.

## 6. Evidence lifecycle and reproducibility

### Stored evidence is useful but not equivalent to the main checkout's contract

The metadata scan found that none of the 39 executable captures contains both a
top-level source identity map and a `freeze_sha256` binding. External inspection can
still compare files with their declared freezes, but the captures do not themselves
implement the main checkout's complete freeze-to-result binding.
The complete [source inventory](branch-source-inventory.json) records every gate's
kind, current README identity and, for executable gates, freeze/capture identities
and observed mismatches.

Two concrete frozen-source drifts were found:

| Gate/source | Stored frozen identity | Identity at pinned branch tip |
|---|---|---|
| CB `README.md` | 4,367 bytes; SHA-256 `b22c802ad438b7ac065f9fcf5f089f66338cd919bb04c02c1ad23b727c41e034` | 4,525 bytes; SHA-256 `e7b2c0cba78be645af689c0150ebcff0fb5bd67386280b38aba8a49d43269094` |
| CY `../../../det8/claims.py` | 26,158 bytes; SHA-256 `02266a1529c312521b755d4e724aa068112aa2ff27dbb5ef8505644fecde7bd2` | 27,418 bytes; SHA-256 `b1106b90841e430433e582c488cda61e9fd3451af6e446b02b102fba5e23e7f2` |

These are provenance mismatches, not evidence that the mathematical outputs have
necessarily changed. They do prevent treating the old captures as authenticated runs
of every source now present at the branch tip. Preserve the historical artifacts and
identify any replacement verification separately; do not silently overwrite their
freezes.

The reviewed DE/DF/DG/DH/DN files all match their own declared frozen identities at the
pinned tip. Nevertheless, DF, DG and DH each import
`det8/models/order_count_geometry.py` without including that dependency in their
six-source freeze. See, for example, the
[DF source list](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05df-physical-pair-kernel-2026-09-11/study.py#L15-L18)
and [external module path](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05df-physical-pair-kernel-2026-09-11/primary.py#L35-L36).

### Agreement must cover the mathematical quantities being claimed

DH's routes calculate intermediate matrices, but their report principally contains
flags and counts rather than B, G_R, Δ and W. Comparing the reports therefore does
not independently compare those matrices across routes. Its square-root primitive is
shared Jacobi code; the reference's opening docstring still claims Newton–Schulz.
The two-chain and diagonal-square-root tests are useful, but do not catch P2 or P3.

Several reviewed drivers use a file-existence check followed by `write_bytes` for
their create-only operation, rather than atomic exclusive creation. Their `--run`
path need not authenticate an existing freeze, and memoized report execution can
reuse earlier in-process results. The
[DF driver](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05df-physical-pair-kernel-2026-09-11/study.py#L61-L115)
illustrates this lifecycle. These issues are reasons to use the local hardened
evidence workflow for adopted work, not to discard every historical calculation.

Several drivers compare encoded reports rather than full native results. Coercion
and rounding can erase distinctions such as Boolean versus integer, a rational
versus its wire representation, or a tuple versus a list. New adopted work should
compare the complete typed mathematical object, then separately verify its canonical
wire, source binding and publication lifecycle.

## 7. DN: useful governance intent, incomplete integration contract

The pinned [T7 registry entry](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/det8/claims.py#L202-L224)
is genuinely classified as a bounded correspondence, remains `DEFERRED`, has no
priority and is absent from the primary development sequence. The estimator remains
`EXPERIMENTAL` and outside the supported core exports. These are valuable safeguards.

However, the claim that all scope and promotion boundaries are executable is too
strong:

- [DN primary](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dn-t7-link-2026-09-11/primary.py#L181-L197)
  assigns `scope_recorded=True` and `open_gaps_recorded=True`; the reference does the
  same. This does not validate the substantive scope or gap text in the registry.
- [Gap resolution](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dn-t7-link-2026-09-11/primary.py#L98-L107)
  checks only file existence, ignoring declared anchors. Replacing a gap pointer in
  memory with `PHYSICS.md#DELIBERATELY-NOT-A-HEADING` still produces a passing gap
  check, even though its own resolver reports `anchor_ok=False`.
- The [frozen-fixture test](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dn-t7-link-2026-09-11/test_qr05dn.py#L159-L163)
  computes a new freeze from the live file and compares that hash with the same live
  file. It does not read the stored freeze, so it cannot detect historical drift.
- The [decision record](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dn-t7-link-2026-09-11/RESULTS.md)
  explicitly says the registry boundary test was not committed with the change. That
  test file is absent from the pinned archive. Its separate hardening dependency must
  be reconciled before integration.
- The falsifier mixes scope violations with a possible future discovery of a
  manifoldlike growth law. A stronger future result would not, by itself, falsify the
  existing conditional estimator benchmark. Keep a scope limitation distinct from a
  universal no-go claim.

**Resolution:** preserve the document-level scope and nonpromotion policy now. Revisit
registry adoption only after independently verifying the accepted estimator content,
repairing the checks, and coordinating the authoritative registry and boundary tests
with the local core/RET work. No registry change is required for the finite calculus
developed in this reconciliation.

## 8. New local work and remaining repairs

The new [finite calculus contract](CALCULUS.md) starts with one nonempty world class W,
all observation channels on that same W, and one joint target. Identification means
target constancy on every equal-observation class. Equivalently, a selected channel
set must separate every pair of worlds with different targets. This is useful for
turning a proposed bridge into a checkable question without assuming its physical
answer.

The declared local verification uses five fixed packets and 27 channel subsets. It
distinguishes slice-wise from joint identification, inclusion-minimal from
minimum-cardinality channel sets, and a supplied external anchor from a validated
instrument. Its calibration discussion keeps ideal, reference and production
populations separate, with explicit validity events and error budgets. It also retains
named counterexamples learned from this audit. The first capture and independent
oracle now agree; [RESULTS.md](RESULTS.md) and [verification.json](verification.json)
record the completed bounded verification, separately from the old branch's labels.
The factorization theorem is standard finite-set mathematics, not a claim of a newly
discovered physical law. Its value here is an explicit reusable implementation and
better-controlled bridge questions.

The repaired research sequence is:

1. Use the completed finite calculus to specify a common-world geometric target/channel
   design. State the joint world class, observation sources and collision witnesses
   before another simulation. Do not treat a perfect anchor channel as calibration.
2. Carry forward the reference/production/model evidence checklist and distinguish
   reference validity, statistical coverage, transport, support, marks and selection.
   None is established merely by agreement between two synthetic implementations.
3. Revisit geometry estimators only with explicit generating-model assumptions,
   observational targets, admissible nuisances and valid adversaries. Separate
   correspondence on supplied geometry from emergence of geometry.
4. Before reopening a physical operator/state track, repair P1–P6 and compare full
   intermediate quantities. State containment, reconstruction and covariance as
   different propositions.
5. Integrate any accepted registry pointer separately with its boundary tests; keep
   physical, ontology and supported-software evidence statuses distinct.

No step in this audit retires an open problem by renaming it, turns a toy damping
parameter into a physical mass, validates an acquisition apparatus, or supplies a new
physical law. The value of the concurrent work is the reusable mathematics and sharper
failure cases it provides for the next defensible local questions.
