# QR-05R results: a nonnegative subset-counting contract

6 September 2026. Investigative outcome: **PASS on Q's unchanged raw
observation domain and thinning law**.

## What is established

The complete next-H polynomials have an exact counting representation:
A_s(h,o,e) is the number of retained eligible subsets with target summary h
and retained odd/even population(o,e). These are nonnegative integers,
not fitted probabilities or source-alias weights.

H determines parent and successor population sizes through B[0]=D.
At a fixed parent degree(O,E), the unnormalized Bernstein tensor basis is
invertible. Consequently, profile constancy and complete polynomial closure
are equivalent within an H fiber. The finite argument is explicit in the
[protocol](README.md), and its degree bounds, color premises and coefficient
identities are checked. This is not a Lean proof or a claim that H closes
on arbitrary orders.

All 4,447 observations and 416 actual H classes pass the counting contract.
Every one of the 4,031 nonrepresentative members has the same profile as its
class representative. No new observable, repair or stable refinement was
introduced.

| Checked object | Exact inventory |
|---|---:|
| Fine induced-subset atoms | 168,388 |
| State-to-H profile atoms | 87,522 |
| Class-profile atoms | 8,231 |
| Complete retained-grade cells | 1,400,352 |
| Power coefficient conversion cells | 1,400,352 |
| Rankwise normalization cells | 71,152 |
| Nested-composition intermediate-rank cells | 131,696 |
| Class-level nested subset pairs | 151,640 |
| Profile probability comparisons at 22 exact rates | 1,925,484 |
| Probability normalization rows | 97,834 |
| Separate public helper calls | 18,304 |

All checked residuals are exactly zero. The composition certificate checks
all 16 intermediate rank pairs per structural final target. Each final H
class fixes its final rank; other final ranks are identically zero by the
verified premise. These 131,696 integer cells are not a re-run of Q's
2,107,136 four-variable polynomial cells.

## Why the representation is useful

A profile evaluates a next-summary probability as a sum of nonnegative
terms throughout [0,1]^2. Grade-wise totals equal
choose(O,o)choose(E,e), proving normalization via the binomial theorem.
This supplies a mathematical positivity/normalization argument over the
whole parameter square; the 22-rate comparisons are supplementary checks.

Repeated thinning becomes a transparent nested-subset count. For a final
subset retaining(m,n) and an intermediate rank(k,l), the intermediate
superset factor is choose(O-m,k-m)choose(E-n,l-n).
The class-level composition agrees with direct counting, including
impossible ranks and structural zeros. Total nested choices are3^(O+E).
Fresh independent predetermined thinning remains the law; no adaptive,
correlated, growth or physical-time dynamics is added.

Both implementations expose evaluate_row(payload,rates), a bounded
summary-row helper that requires no raw order or hidden representative.
All 416 class rows were checked at all 22 rates through both implementations.
The helper retains zero-probability structural outcomes and rejects
noncanonical rationals, incorrect ranks/counts, missing normalization,
native-type coercions and exact-arithmetic bound breaches.

The caller must supply a trusted row from verified evidence.
Structural validation cannot authenticate class labels, cross-row color
maps or domain membership. This is an isolated research interface, not a
RET/production SDK integration or a demonstrated performance advantage.

## Independence, preservation and controls

The primary constructs direct subset multiplicities and expands them.
The reference reconstructs polynomial laws independently, applies an exact
Gaussian inverse basis transform, and checks a separate rank-first subset
census. A third runner independently reconstructs the full result.

All three complete analyses agree: 11,546,676 bytes, SHA256
`a8ce087b64e7da9cc05bcf4efe2b6352f99f13da2ad360f03bc66b9c4246f292`.

The supplied model is explicitly Q's raw {frames,states} projection.
Features, actual H fibers and all fine/pushed/quotient laws match Q exactly.
R does not regenerate Q's source/alias universe or re-establish expanded
minimality. Relevant complete-row digests are:

- Fine: `8e1aa78672835867ad2177cd43b8314562186ee2271444a4a14d6f7cd1ddb5db`.
- Pushed: `cbf44750c4a397073afe57954f54fb23091e7333689f4aba45649ed5bb3b6995`.
- Quotient: `66e4efa3aa046c7ad9d95f183f5ecfd34a894190d557b7f01caba48d4b770e0f`.

Controls cover all 100 bounded basis monomials, signed coefficients, fixed3
eligible exclusion, rankwise versus total normalization, absent atoms,
zero-rate outcomes, and missing intermediate binomial factors. A deliberate
degree-elevation example gives the same event law x from different parent
population sizes but different subset counts. It lies outside H's
color-preserving premises and prevents an overbroad equivalence claim.

Synthetic failed fibers retain the canonical first obstruction, scan all
members, and expose no quotient/composition. Same-cardinality wrong
memberships, coefficient/count tampering, malformed inputs and mutable
payload/cache boundaries are also tested.

## Verification and retained evidence

- Final normal suite: 192 passed in 200.51s.
- Final optimized suite: 192 passed in 201.27s; only the expected pytest
  warning about non-test assertions under -O. Production guards are explicit
  exceptions, and separate optimized subprocess checks pass.
- Preliminary independent test smoke: 4 passed in 64.19s.
- Frozen create-only capture: 86.37511979098781s.
- Exact read-only replay, normal: 87.34238220899715s.
- Exact read-only replay, optimized: 87.93420945899561s.
- Independent stdlib-only JSON postflight: 44,013,704 checks in
  28.857049915997777s, with no executor, runner or test imports.

Canonical [results.json](results.json): 12,028,200 bytes, SHA256
`cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001`.
Its six source/protocol files and all 22 prior artifacts matched their byte
ledgers before and after capture, replay and postflight. The postflight
reconstructed all retained mathematical fields and checked the declared
Q input/law bridge. Public-call metadata agrees with the independently
checked class/rate inventory; the actual helper calls occur in the runner
and test suites.

The full normal and optimized suites had no failures. This report and the
roadmap are outside the frozen ledger. Earlier evidence and unrelated
RET/core/Track-B work were not edited.

The protocol, domain, observables and mathematical criteria were fixed before
execution and were not changed in response to the outcome. Before freeze,
the reference's repeated Gaussian inverse application received a bounded
immutable-content cache; input/output validation, exact bit guards and
round-trip checks remain active. Its complete pre/post-change mathematical
bytes are identical. A separate reference smoke initially expected the wrong
last degree-three count for the event polynomial x; its expected vector was
corrected to [0,1,2,1]. Only that external check changed, not the executor or
mathematical contract. No frozen artifact was overwritten.

## Boundary and proposed next gate

This establishes a finite counting/closure contract for the supplied models
and sampling law. It does not identify spacetime geometry, derive gravity,
prove an ontology, install Lean, change RET, or extend P's consumer authority
or minimality result to arbitrary inputs.

Proposed QR-05S: derive and verify a local single-deletion criterion while
keeping the domain, H and law unchanged. Count the odd/even vertices whose
individual deletion reaches each H class, retaining vertex multiplicity.
Under subset closure and H-measurable color ranks, local profile constancy
is equivalent to full deletion-profile constancy. Reconstruct R's complete
profiles by smaller-parent induction, checking exact divisibility and the
odd/even mixed-deletion consistency identities.

This would give a local explanation and constructive certificate, not
physical-time generators or an unmeasured efficiency claim. S has not been
executed as part of R.
