# QR-05O results: obstruction-targeted path observable

6 September 2026. **Completed investigative gate; finite candidate closes.**
Research base: pushed QR-05N checkpoint `0be2929`.

## Outcome

On the unchanged 2,470-observation N domain, adding the prespecified
induced colored-path count T gives a closed summary

    H(S) = (frame, B(S), M(S), T(S)).

Both independent implementations agree. H has 167 classes and splits
exactly one of the 166 C=(frame,B,M) fibers. This is a finite constructive
repair of N's obstruction, not a coarsest-refinement or minimum-memory
claim. No stable-refinement search was executed.

| Summary on the same observations | Classes | Complete next-summary law |
|---|---:|:---:|
| Frame and pair-overlap tensor B | 165 | Not closed |
| Frame, B and K2,2 count M | 166 | Not closed |
| Frame, B, M and induced P4 count T | 167 | Closed |

The old failures remain unchanged in the base analysis; they were not
reclassified as successes. The source family and sampling law were not
modified to obtain the new result.

## The added observable

T counts four-element observed eligible supports with exactly two vertices
of each named color, no same-color comparisons, and exactly three uniformly
oriented cross-color comparisons. The fourth cross pair is incomparable.
Each support counts once.

The underlying undirected comparability graph is P4. This is not a directed
three-step chain, a cover-graph path, a noninduced embedding count or a
Feynman trajectory. A complete K2,2 contributes M=1 and T=0. The recognizer
uses only the observed kept IDs, supplied strict transitive relation and
eligibility marks; no source identity, state/class lookup or future law
enters feature construction.

N's witness becomes visibly distinguishable:

    A: 1<4, 1<6, 3<2, 5<2       T=0
    B: 1<2, 1<6, 3<4, 5<2       T=1

Both still have equal complete D/B tensors, M=0 and N=(1,6,4,0).
B's unique P4 support is {1,2,5,6}; A has two disjoint two-edge stars.
Their unequal next-C laws remain retained exactly in N's projection.
This local distinction motivates the feature; closure was then checked on
every H class, not inferred from this pair alone.

Across the domain, 1,203 observations have positive T, with 2,955 support
occurrences and maximum T=6. Complete K3,3 in either orientation gives
T=0,M=9; removing one incidence gives T=4,M=5. These are multiplicities,
not Bernoulli-valued motif flags.

## Expected survival and full recursive prediction

Because observation is induced restriction, a T support survives precisely
when all four of its eligible vertices survive. No new T support appears
when outside vertices are removed. In particular, an outside intermediary
that already establishes the fourth comparison cannot be removed to turn
K2,2 into a new induced P4: that comparison remains in the restricted
transitive relation.

Independent odd/even vertex retention therefore gives

    E[T(U) | S] = x² y² T(S).

Linearity does not require independent survival of overlapping supports.
The retained K2,3-minus-one-edge control has two T supports with expectation
2x²y². Their joint survival is x²y³, not x⁴y⁴: at half retention the
probabilities are 1/32 and 1/256 respectively. All 32 induced outcomes
are retained.

This expectation identity alone would not establish recursive sufficiency.
The separate closure test pushes each complete fine transition row to H
and compares every member of every actual fiber coefficientwise. All rows
agree, giving an exact parameterized quotient under the fixed observation
law for all (x,y) in [0,1]².

Fresh independent stages additionally satisfy

    Q_(x,y) Q_(a,b) = Q_(xa,yb).

The certificate compares all four-variable coefficients, not just a
same-rate grid. Structural atoms remain present even when a selected rate
makes their probability zero. There is no adaptive-rate, reused-coin or
correlated-stage composition claim.

## Domain and evidence preservation

O uses exactly N's 1,030 profiles, 65,888 provenance aliases, 2,470
deduplicated observations and 99,180 fine atoms. Density, fixed probes,
original-ID color marks, six-eligible-vertex bound and thinning law are
unchanged. The 22 synthetic recognizer controls do not expand this domain.

Removing only the new `path_observable` object reproduces N's complete
analysis type-exactly. N's audit, controls and prior M bridge also agree
exactly. That preserves the old states, aliases, tensors, motif supports,
fine and pushed polynomials, failed partitions and expectation evidence.

The original 257-state M restriction still has its own 110-class closed
quotient and 295,424 verified composition cells. This is retained old
evidence, not an assertion that the new H partition equals M's partition.

| New exact check | Total |
|---|---:|
| Path feature rows | 2,470 |
| T expected-update coefficient cells | 39,520 |
| H state-pushed atoms / coefficient cells | 48,768 / 780,288 |
| H rational-rate atom evaluations, at 22 points | 1,072,896 |
| Deterministic state/corner rows | 9,880 |
| H quotient atoms | 2,364 |
| H two-hop intermediate paths | 15,571 |
| H four-variable composition cells | 605,184 |
| H plus retained old M composition cells | 900,608 |

N's 12,646,400 D/B and 39,520 M expected-update cells are also replayed
unchanged. None is used as a substitute for the new complete-law check.

## Verification and frozen artifact

The primary recognizes observed eligible quartets directly; the reference
uses the unique central edge of an induced P4. Their complete native-wire
outputs agree. The runner and tests separately reconstruct feature
supports, class memberships, pushed laws and the closure decision.

Validation passed:

- 154 tests normally (312.13s) and 154 optimized (313.09s), in isolated
  Python 3.11.6 with external bytecode caches and no pytest repository
  cache. The runs were concurrent, not performance benchmarks.
  Optimized pytest emits its standard non-test-assertion warning;
  executor/runner guards explicitly raise and optimized rejection controls
  pass. A separate focused run passed 34 tests in 104.24s.
- Ruff check/format and all six new-source whitespace checks passed before
  freezing. Source identities stayed unchanged across the test runs.
- Exclusive create-only capture: 27,143,093 bytes, below the 64 MiB cap;
  suite time 49.68680270801997s.
- Exact read-only replay: normal 52.293522416992346s, optimized
  52.387039417022606s. Both reproduce the complete suite, including N's
  D/B/M checks, without altering the artifact.
- Independent JSON-only postflight: 8,044,182 explicit checks in 10.607s,
  importing no executor, runner or test. It rebuilt all 2,470 T support
  lists, checked all 99,180 fine atoms and support heredity, actual H
  fibers, all pushed laws, expectation and composition cells, rate/corner
  controls, 22 synthetic cases and 32 overlap atoms. It checked all six
  source and 19 prior identities before/after; capture bytes stayed fixed.
  N's complete analysis and three retained suite fields were preserved
  here through type-exact pinned projection, not a separate reconstruction
  of its D/B/M certificates in this O-specific postflight.

Mutation controls reject corrupt or duplicate supports, boolean/integer
substitutions, equally sized wrong fibers, bad expectation and transition
coefficients, false closure, fabricated failures/quotients and altered
composition counts or prior projection. A test-private empty recognizer
recovers N's failed 166-class C exactly, including its witness and empty
quotient/null semigroup. No cached successful repair survives that change.
Lifecycle negatives use temporary stub evidence, never the real capture.

Artifact SHA-256:
`3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1`.

All six source identities are frozen in [results.json](results.json);
the artifact was created once and not overwritten. RESULTS.md and the
roadmap are human reports outside that ledger. Prior evidence, RET/core,
the temporary model sheet and unrelated checkout work were left untouched.
No dependency installation or application integration occurred.

## Applicable value and next gate

The useful mathematical result is an observed structural statistic that
repairs a specified prediction failure without using source provenance or
a law-defined lookup feature. Within this finite domain and observation
contract, once a record is encoded as H, future H distributions can be
updated from its quotient without reopening the full underlying order.
Functions of H, including the retained chain counts, inherit that
prediction contract. Arbitrary other graph questions do not.

This is a potential building block for relational-summary validation and
controlled thinning studies. It is not yet a packaged application,
measured speed/memory improvement, materials result, anomaly detector
or RET adapter. Encoding H may itself require the observed order; fewer
classes do not prove cheaper storage or computation.

**Next proposed gate: QR-05P, finite minimality comparison and application
contract.** Independently construct the coarsest closed refinement of N's
C partition under the same complete polynomial transition law, compare
actual memberships with H, and state exactly what a summary-only consumer
can predict. Retain any discrepancy; equal class counts are insufficient.
No outcome of that comparison is asserted here.

General portability to larger or differently layered orders remains open.
For Track B, this supplies a checked finite relational description under a
declared observation model. It does not derive a metric, event-growth law,
physical time, gravity, a continuum limit or ontology, and it does not
identify these paths with quantum amplitudes. No empirical validation or
noise-model exemption follows. Lean formalization and RET quantum
integration retain their separate gates.
