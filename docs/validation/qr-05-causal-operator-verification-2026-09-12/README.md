# QR-05: bounded exact causal-operator verification contract

12 September 2026. Prospective executable contract. Freeze all sources before
the first mathematical execution; no tuning after that run. This implements
the [analytical design](../qr-05-causal-operator-design-2026-09-12/README.md),
not a physical operator, instrument, ontology or gravity-dynamics claim.

## Fixed domain and independent routes

Use exactly the thirteen cases and four variants in [protocol.json](protocol.json),
in case-major then variant order. relation entries are [receiving row,sending
column]; weights are [row,column,numerator,denominator]. They explicitly list
the full transitive order, not only its covers. Missing weights are Fraction(0).
Variants are identity, cyclic relabel old i→(i+1) mod n, transpose both C,A,
and jointly multiply d,A by c=3/2. No compositions or deduplication.

There are 52 rows, 148 event occurrences, 452 cells per reported matrix,
120 strict pairs, 92 covers and 100 nonzero entries each in A and off-diagonal
G. The 304 paths include 148 trivial, 120 one-edge, 36 two-edge and 24 zero-
contribution paths. Direct support equals C in 36 rows and reachability in 48.
These expected counts come from the prospective design, not a fitted search.

Primary computes G by the finite matrix-power sum. Reference uses exact
Gauss–Jordan inversion and an independent explicit path enumeration. They
must not read/import each other or share a mathematical helper. Each independently
constructs the fixed inputs. The driver checks them against the protocol.
Both report full powers, paths and matrix identities, not only predicates.

## Pure API

Both modules provide evaluate(world) and analyze(). evaluate accepts exactly a
plain dict {C,A,d}; C,A are square plain lists of plain lists, 1≤n≤4. C entries
are plain ints 0/1, never bool. A and d are plain Fractions with absolute-
numerator/denominator bit lengths≤128; d>0. C must be irreflexive and transitive,
and A must vanish outside C. Reject malformed types, subclasses, wrong shapes,
cycles, missing transitive relations or forbidden support with ValueError.
Never coerce/repair input. Arbitrary valid labellings are accepted. No I/O or
randomness is allowed. Functions must not mutate inputs or return mutable
containers aliased to caller inputs. Otherwise-valid shared input rows are
accepted and copied, not rejected solely because their identities coincide.
Outputs have no extra rational-bit cutoff; all calculations are exact and
the fixed n/input bound controls their size. Tests include acceptance at the
inclusive 128-bit boundary and refusal beyond it, without a fixture sweep.

analyze() takes no arguments and independently generates just the fixed 52
rows and the twelve witness records below. It has no I/O or caches. IDs and
target C are verifier information, never smuggled into G/Delta/support values.

## Exact evaluate row schema

An evaluate row has EXACTLY these keys:

- world: fresh {C,A,d}.
- L: plain-int cover matrix.
- powers: n+1 Fraction matrices [I,A,...,A^n].
- M,G,Delta,MG,GM: Fraction matrices; M=dI−A, Delta=G−G^T.
- paths: all strict paths, including one-event paths, sorted first by number
  of edges, then lexicographically by the complete node list. A path is
  {nodes,weights,contribution}; nodes go sender→receiver, weights are the
  successive A entries, contribution=product(weights)/d^(edges+1).
  For a trivial path weights=[] and contribution=1/d. Retain zero terms.
- support_A,support_G,closure_A,closure_G: plain-int matrices. Support masks
  mean nonzero off-diagonal entries only; closures are strict directed TC.
- covers: all covers in receiving-row-major order, each exactly
  {pair:[i,j],A:Fraction,G:Fraction,expected:Fraction}, expected=A_ij/d².
- missing_direct,extra_direct,missing_reachable,extra_reachable: complete
  [receiving row,sending column] pair lists in row-major order, comparing
  C with support_G or closure_G respectively. Missing means C=1/result=0;
  extra means C=0/result=1. Retain empty lists.
- flags: exactly the seven plain bools direct_equal,reachability_equal,
  closures_equal,covers_nonzero,covers_positive,A_nonnegative,positive_sign_rule.
  The first three are actual matrix equalities; cover predicates quantify all
  covers, vacuously true for an antichain. A_nonnegative checks every A entry.
  positive_sign_rule is the ACTUAL condition on all i,j that
  (Delta_ij>0 iff C_ij=1) AND (Delta_ij<0 iff C_ji=1), not an implication
  automatically true outside a premise. All diagonal entries are included.

These tests must distinguish nonnegative A plus positive covers from positive
covers with signed noncover edges. A zero G entry need not mean no causal path.

## Exact analyze report schema

Top-level keys are EXACTLY schema,rows,witnesses. schema is
qr05-causal-operator-report-v1. Each rows entry adds id,base,variant to the
evaluate row. id is base + ':' + variant. Ordering is case-major then variants
in protocol order, including symmetric duplicates.

Witnesses enumerate the three protocol pairs, pair-major then variant order.
Each is exactly {kind,variant,channel,rows,value,targets}. rows is the two IDs
in protocol order, channel is G or Delta, value is their shared Fraction
matrix, and targets is [left C,right C] as plain-int matrices. Targets must
actually differ; channel values must actually agree. The same-G missing-cover
pair and both same-Delta pairs are retained under every corresponding variant.

## Verification obligations

Compare complete native primary/reference reports and an independent test
oracle with analytically declared base G entries. Tests check all input
worlds and census counts, full powers including A^n=0, both inverse products,
every path contribution and path-summed G, complete support/closure masks and
omission witnesses, cover identities, all seven flags and the three collision
pairs. Check finite signed reachability preservation, the nonzero-cover iff,
and the positive sign theorem only under its full premise. Include exact toy
cancellation at d=3 and mixed signs at d=5, with the earlier whole-sign convention
explicitly distinguished. No floating tolerances or physical propagator labels.

Check cyclic conjugation, reversal G→G^T/Delta→−Delta and joint positive
rescaling G→(2/3)G, including powers/path data. Validate all documented input
refusals and inclusive bit bounds, fresh containers and lack of input mutation.
No additional mathematical fixture bank is authorized beyond named API/proof
boundary controls. Use one cached full analysis per test suite.
The named maximum-depth control is the full four-event chain with unit cover
weights and d=1: A³_30=1, A⁴=0, G_30=1, and the path [0,1,2,3] contributes 1.
It exercises the API's allowed depth beyond the fixed study's two-edge paths;
it is not a fifty-third study row or a changed prospective census.

## Evidence discipline

Freeze NINE sources: this README, protocol.json, primary.py, reference.py,
study.py, test_causal_operator.py, both prior design documents and the
literal-SHA-pinned BM evidence utility. Existing freezes/captures remain
unchanged. Publication RESULTS and verification logs are not prospective inputs.

Authenticate the bounded regular utility bytes before loading; use evidence
helpers only, never its mathematical executor. Validate literal dependency
and protocol pins before new engine execution. Capture/replay must bind all
source identities and freeze bytes before analysis, recheck afterward, publish
by exclusive create and read back. Compare Fraction/int/bool native types before
canonical serialization. Test malformed metadata, source changes, route mismatch,
capture tampering, publication and freeze-lifecycle refusals.

Limits are 30 seconds per full analysis, 60 seconds per suite, 262,144 bytes
per source and 16,777,216 per artifact. Sequence: static review/formatting,
freeze, FIRST capture, normal and optimized suites, both full replays, then
exactly one Python 3.11 full replay. Preserve any failure and use a separately
named revision if repair is needed; never tune these sources after first run.

This is exact finite supplied-operator verification. It does not establish
physical geometry recovery, stable noisy inversion, apparatus calibration,
RET readiness or new physics. Ordinary transpose does not choose a physical
measure or advanced operator. Later operator/measure/boundary and convergence
contracts remain open; book, clock and retired-coupling deferrals are unchanged.
