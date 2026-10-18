# QR-05G results: prediction-relative compression

6 September 2026. **Completed bounded investigative gate.** This is a finite
classical acquisition/summary result in the geometric research branch, not a
new quantum law, spacetime reconstruction or gravitational dynamics.

## Main finding

The information needed depends on the question. Under the declared ten-case
universe, policy provenance is enough to compute the current sequential
estimator, support-graded chain counts preserve repeat-acquisition means, and
fixed-marked order isomorphism preserves the entire joint chain-count law.
None of these compressed candidates preserves the fully labeled repeat-order
law across the whole universe. Full intermediate records do, but can contain
unnecessary detail for a particular target or degenerate acquisition context.

The known design, density, fixed/eligible frame, and final observed order are
part of **every** candidate. Hidden source-profile names are not part of any
key; matching public contexts are pooled across profiles.

| Candidate | Classes | Current estimator | Future means | Joint count law | Labeled order law |
|---|---:|:---:|:---:|:---:|:---:|
| Final record only | 407 | No | No | No | No |
| + policy token | 521 | Yes | No | No | No |
| + policy and tagged membership | 703 | Yes | No | No | No |
| + policy and plain chain counts | 1,688 | Yes | No | No | No |
| + policy and support-graded counts | 1,706 | Yes | Yes | No | No |
| + policy, graded counts and tagged membership | 2,041 | Yes | Yes | No | No |
| + policy and boundary-anchored unmarked order | 2,023 | Yes | No | No | No |
| + policy and correctly fixed-marked order | 2,040 | Yes | Yes | Yes | No |
| + full intermediate record | 3,379 | Yes | Yes | Yes | Yes |

These are finite class counts, not compressed byte sizes or source probabilities.
The exact coarsest partitions refining the public base have respectively
519, 1,686, 1,833 and 3,321 classes for the four targets. In particular, marked
order is a sufficient but not minimal representation of the count-law question.
The target-signature quotient is an audited finite lookup construction; its
existence does not provide an efficient scalable representation.

## Mathematical structure

For observed intermediate order S, let C[q][k] count q-internal-vertex chains
with exactly k eligible vertices. The known repeat design gives an inclusion
factor eta_k: eta_0=1, eta_k=r(S)^k for IID retention, and eta_k=1/2 for
nonempty common-coin supports. Therefore

```text
E[N_q(U) | S] = sum_k C[q][k] eta_k.
```

This supplies an explicit mean-preserving map from graded counts and policy
to the prediction. Fixed internal vertices are never weighted as eligible ones.
For chain supports a,b, the covariance contains

```text
Cov(N_p,N_q | S)
  = sum_(a in p-chains, b in q-chains)
      [pi2(a union b | S) - pi2(a | S) pi2(b | S)].
```

Support overlaps can differ despite equal graded totals, explaining why mean
preservation is weaker than distribution preservation. The full count law is
the pushforward of K(U|S) through the observed induced U-order's chain counts.
A fixed-mark-preserving isomorphism and equal token preserve it for the
exchangeable laws used here. This argument does not extend automatically to
nonuniform label-sensitive acquisition.

For any declared target F and public base B, R*=(B,F) is the coarsest finite
partition refining B on which F is constant. If candidate R retains B and
F=g(R), equal R implies equal (B,F), so R refines R*. The capture checks actual
fiber constancy, not just matching class counts, and retains the first supported
collision for every failing candidate/target pair.

The definition-level hierarchy is:

```text
labeled repeat-order law -> joint count law -> count means
```

The complete enumeration additionally finds count-law equivalence implies
current-estimator equivalence **in this finite family**. This was not assumed
and is not a general estimator/prediction theorem. Means alone do not imply
current-estimator equivalence.

The nonzero alpha_q factors merely rescale these count questions into the
previous formal scalar retarded-kernel coefficient questions. They do not
turn the scalar polynomial into a CP map or a Born-probability model.

## Retained counterexamples and positive controls

1. **Equal means, different distributions.** Ferrers star S={1,4,5,6} and
   path S={1,2,4,5}, with final T empty, have counts [1,4,3,0], equal graded
   tables and the same tagged membership. Under IID half-retention their
   relation-count variances are 15/16 and 13/16, despite common mean 3/4.
   The joint atom N=3,R=0 has mass 1/16 for the star and zero for the path.
   Histories 521/155 each have positive joint mass 1/1024. Under adaptive
   r=1/3, histories 1250/884 instead give variances 4/9 and 32/81 and atom
   masses 2/81 and 0; each history has joint mass 1/324.

2. **Fixed marks are predictive information.** With interior vertex 3 fixed,
   eligible S={2,5} versus S={4,6} have counts [1,3,1,0] and the same
   unmarked order. The relation joins eligible--eligible versus fixed--eligible
   vertices, giving repeat means R=1/4 versus 1/2. Histories 6594/6660 retain
   this supported failure; grading and fixed-marked order distinguish it.

3. **Isomorphism is sufficient, not necessary.** Up-star mask 57 and down-star
   mask 39 are nonisomorphic directed orders but have identical entire joint
   repeat-count laws under independent acquisition. Histories 521/281 fall
   into different marked-order classes and the same count-law class.

4. **Unlabeled structure does not preserve labeled predictions.** One-edge
   S={1,4} and S={2,5} have identical marked-order/count-law summaries, but
   ID1 appears in a repeat with probabilities 1/2 and 0. Histories 29/87
   distinguish the fully labeled order laws.

5. **No hidden-profile shortcut.** Ferrers6 and S3 full-S, final-empty histories
   665/4310 have the same public base and count means. Their repeat relation
   variances are 17/8 and 15/8. Their mask laws agree, but the induced order and
   count laws do not. These are the uncorrected repeat-count counterparts of
   the earlier corrected-variance collision; no contradiction with QR-05E.

6. **Compression is context dependent.** Under common_coin, plain counts
   determine the count law; that claim fails globally. Under parity_hole,
   the supported final order already determines the repeat-order law:
   an odd S gives the empty eligible record, while an even S is fully kept.
   Histories 2187/2188 have different S records and policy tokens yet the same
   future empty-record law. No general dispensability of provenance follows.

7. **Means and current estimation remain distinct.** Adaptive Ferrers
   histories 731/735, S={1} versus S={1,2}, final T={1}, both have repeat mean
   vector [1,2/3,0,0], but sequential estimates [1,3,0,0] and [1,6,0,0].
   This is a retained illustration of the observed non-refinement, not a
   separately fitted or newly simulated witness.

## Verification and artifact identity

- **96 tests passed** in isolated normal Python (28.97s).
- **96 tests passed** in isolated optimized Python (28.78s), with only the
  expected pytest warning about non-test assertions under -O. Executors use
  explicit rejection guards; a subprocess test also verifies optimized valid
  execution and 22 explicit malformed-input rejections across the two routes.
- Ruff check and format check pass. All tests precede source freeze/capture.
- Create-only capture: **13,935,276 bytes**, suite time 11.866182416s.
- Exact read-only replay: normal 12.975529083s; optimized 12.914076208s.
  Runtime timings are descriptive, not performance acceptance criteria.
- Independent JSON-only postflight: all six source identities, eleven prior
  identities, 13 complete partitions and 36 candidate/target assessments pass.
  Artifact bytes remained unchanged.

[results.json](results.json) SHA256:

```text
62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74
```

Research base commit: 490c443186dbe1b862d377e197f3281ee261ad56.
Remote publication remains deferred; no push was attempted for this gate.

The six frozen sources are README.md, compression.py, reference_qr05g.py,
study.py, test_qr05g.py and test_capture.py. The primary predicts from induced
intermediate observations; the independently written oracle uses full-source
chain indicators. A third reconstruction checks every supported partition,
member list, joint mass, first collision and refinement. No prior executor
is imported. QR-05F JSON comparisons cover all 608 intermediate states,
6,804 current histories/estimates and 6,804 repeat-kernel probabilities.
All 11 earlier pinned artifacts retain their identities and claim boundaries.

All 6,804 histories remain visible: 3,534 supported and 3,270 zero-joint-mass.
Zero histories have null predictive/candidate class IDs. There are 608 states,
510 with positive first-stage probability; 4,872 repeat rows have positive
conditional probability, including diagnostic states with zero first mass.
The current estimator retains 27,216 exact cells. Maximum retained rational
or integer component is 59 bits, below the 4096-bit guard.

Class masses sum to 10, the sum of ten normalized design experiments.
No source-profile prior was introduced, so these masses are not a pooled
posterior. Future laws at zero-P1 states are evaluations of a specified
kernel, not conditional probabilities inferred on null events.

During pre-freeze review, the runner's density string needed explicit Fraction
parsing, and the oracle needed an exact string-key guard for subclass inputs.
Both were repaired and tested before any capture. No frozen artifact was
overwritten. Compact sorted canonical JSON with a trailing newline avoids
whitespace inflation while retaining all rows and signatures.

## Applicable value and limits

This gate makes an observer-relative mathematical statement usable: choose the
prediction first, then verify which parts of provenance it requires. It gives
a candidate contract for future diagnostic or geometric-summary interfaces:
declare the acquisition law, fixed/eligible distinction, question family and
support domain before claiming information has been safely discarded.

It does not establish empirical prediction accuracy, inference of an unknown
sampling law, recoverability of S from one observation, geometry identification,
continuum convergence, recursive closure or Einstein dynamics. It does not
validate DET ontology, construct a new quantum channel or integrate the RET SDK.
The standalone temporary model sheet and all RET/core work are unchanged.

The predictive-equivalence principle is established mathematics, not a novelty
claim; see the primary-source attribution in [the protocol](README.md).
The contribution here is the reproducible finite comparison, explicit
factorization contracts and retained counterexamples for these order questions.

## Proposed next gate: QR-05H

Test **observation-law portability**. Freeze a small public menu of continuation
laws, including label-sensitive/nonuniform acquisition and a correlated control.
Ask which G summaries preserve count questions for every law in that menu.
Keep the same supported history domain and public current-record base; attach
the whole vector of policy-specific predictions to each history. Its partition
is the common refinement of the policy-specific target partitions, not a union
of disjoint (history,policy) contexts. Retain failures of plain marked-order
equivalence when the law breaks that symmetry, and test a law-marked sufficient
control whose permitted isomorphisms transport the whole declared kernel,
including correlations. Declare transport on fully labeled observation laws
before pushing forward to counts, and check target-within-source support at
each supported history. Count-law and record-law support are not interchangeable;
do not infer missing outcomes from a zero-support policy. Predictive sufficiency
does not by itself certify weight measurability or recursive state updates.

This is a proposed bounded protocol, not yet executed or accepted. It directly
tests whether a useful compressed description survives a declared change of
measurement procedure. It remains distinct from physical dynamics, empirical
apparatus calibration and the independently gated QR-06 RET adapter.
