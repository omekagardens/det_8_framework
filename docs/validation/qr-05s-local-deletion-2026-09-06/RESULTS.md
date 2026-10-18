# QR-05S results: full thinning profiles from local deletion counts

6 September 2026. Finite exact audit on Q/R's unchanged raw observation domain.

## Outcome

The unchanged H=(frame,B,M,T) summary has constant odd/even single-deletion
count rows throughout all 416 fibers. Two local-only constructors recover
all 8,231 class-profile atoms exactly: smaller-parent recurrence and ordered
deletion words divided by their color factorials. A third raw-subset audit
agrees with both, and the complete state/class profiles and polynomial laws
match pinned R.

| Retained inventory | Count |
| --- | ---: |
| Raw observations / H classes | 4,447 / 416 |
| Nonrepresentative members checked | 4,031 |
| Raw single-vertex deletion choices | 22,110 |
| Fine local color/target atoms | 17,648 |
| Class-local color/target atoms | 1,576 |
| Full fine subset atoms | 168,388 |
| Full state-profile / class-profile atoms | 87,522 / 8,231 |
| All source/target cells, including incompatible zeros | 173,056 |
| Equal-rank base delta equations | 34,970 |
| Color-specific recurrence equations | 57,102 |
| Rank-normalization cells | 6,656 |
| Direct profile / power comparison cells | 1,400,352 each |
| Two-deletion operator coefficient cells | 3,732 |

All residuals are zero. The 1,576 local entries are a smaller specification
of this certified law, not a measured runtime or storage-product benchmark.
Vertices with identical successor summaries still contribute separately to
multiplicity.

## Mathematical meaning

For source rank(O,E), target class g of rank(m,n), and local deletion
multiplicities L, the full subset count A satisfies

    sum_h L_odd(s,h) A_h(g) = (O-m) A_s(g),
    sum_h L_even(s,h) A_h(g) = (E-n) A_s(g).

Only equations with a positive corresponding denominator are used;
both are checked when available. Equal-rank values are the identity delta;
other-frame and impossible-rank values are zero. Class IDs need not be
topological. Division is exact integer division, never rounding.

Independently, one fixed color-order word gives

    (L_odd^a L_even^b)[s,g] = a! b! A_s(g,O-a,E-b).

The observed raw domain is finite and closed under single deletions, hence
under all subsets. H fixes the frame and eligible color ranks. Under these
premises, full-profile constancy implies local constancy by selecting the
single-deletion ranks. Conversely, local constancy and smaller-parent
induction imply full-profile constancy. The gate supplies a constructive
argument and finite executable certificate, not a machine-checked Lean proof
or a claim of H closure on arbitrary orders.

The class operators pass complete structural-map identities:

    L_odd L_even = L_even L_odd = A at rank(O-1,E-1),
    L_odd² = 2 A at rank(O-2,E),
    L_even² = 2 A at rank(O,E-2).

Their weighted row masses are OE, O(O-1) and E(E-1).
Across classes, the odd-odd/even-even/mixed word masses total
1,708 / 1,740 / 2,521. Distinct target-map counts are 603 / 617 / 1,256;
the 3,732 coefficient checks count both mixed orders.

## Trust boundary and independence

The public reconstruct_profiles input contains only class IDs, frames,
ranks and two local count rows. It does not receive raw observations,
full subset profiles, fine kernels or prior artifacts. The runner separately
calls both public constructors and checks every returned profile against
raw-subset ground truth, as well as rank lattices in both ID orders.

Valid row totals alone are insufficient: controls reject fractional
reconstruction and incompatible odd/even word orders. Tests also cover
multiplicity, same-color factorials, wrong total-parent divisors,
zero-deletion identity, equal-rank distinct classes, empty colors,
frame/rank errors, missing successors, mutated fibers, native-type
coercions, resource guards, changed inputs and detached outputs.

Structural/algebraic validation cannot authenticate H labels, certify raw
domain membership, or prove that an arbitrary local table is realizable
by observed orders. Trusted use still requires the checked raw-domain bridge.
The prospective parser cap is 512 classes, not a new domain expansion.

R's retained raw model is an explicit input dependency. All features,
induced deletions, actual H fibers, direct full subset profiles and laws are
recomputed. Neither executor imports the other or previous executors, reads
prior results, or uses mutable RET/core code. The runner's prior bridge
compares every state/class profile with R. Source/mask aliases, R's public
probability helper and Q's four-variable certificate are not rerun.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 7,128,993 bytes,
SHA256 `8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3`.
The complete mathematical analysis is 6,647,202 canonical bytes,
SHA256 `2305b5918fdce8c952160b1f7ac0fb40b4c1421397e22e7581afc86d29b640a4`.

| Check | Final outcome |
| --- | --- |
| Full normal tests | 183 passed in 134.08s |
| Full optimized tests | 183 passed in 134.05s |
| Exclusive capture | 43.8135322080052s |
| Fresh normal exact read-only replay | 44.52357120800298s, exact |
| Fresh optimized exact read-only replay | 44.68569320900133s, exact |
| Separate JSON-only postflight | 35,032,228 checks in 20.27752554201288s, passed |

The optimized suite has only pytest's expected warning about assertions
outside rewritten test modules. Its dedicated subprocess uses explicit
non-assert guards, including 52 malformed-input rejections; two bounded
shared-DAG subprocess modes each check 11 rejections and valid alias acceptance.

The runner made 12 separate local-only public calls across two routes and
three distinct local models, including reversed class IDs. First-return
comparisons cover 17,262 profile atoms; repeated calls verify output ownership.
It rejected 16 invalid local calls and 16 invalid analysis inputs.

Six source/protocol files and all 23 prior artifacts matched their ledgers
before and after final tests, capture, replays and postflight. The latter
reconstructs the retained mathematics and inventory metadata; actual public
constructor dispatches occur in the frozen runner and test suites. No executor,
runner or test is imported by the postflight, and source bytes are read only
for identity checks.

The protocol, domain, observables and mathematical criteria were fixed before
execution and were not changed in response to outcomes. Before capture:

- Native parsers gained cycle/depth handling and per-call shared-DAG
  accounting. Expanded value-node counts lower-bound serialized JSON bytes;
  repeated subtrees retain multiplicity while being walked once. The depth-40
  doubling-DAG controls reject before JSON serialization. This is not a
  general performance claim.
- The runner restored native model validation before canonical-content
  caching, preventing serialization-equivalent subclass inputs from
  bypassing validation.
- Review strengthened malformed-edge controls to start from valid models
  and added an isolated missing-transitivity case.
- The first full normal/optimized runs each had 182 passes and one ownership
  failure. The reference's frame-key helper exposed both input frame lists.
  It now copies fixed/eligible lists; the existing test was retained.
  Full mutable-container disjointness and later-call checks pass. Complete
  mathematical bytes are unchanged.
- Exploratory reference smokes initially set the bytecode prefix through
  an environment variable ignored by isolated Python. The two resulting
  local bytecode files were moved to a scoped external quarantine, and
  corrected normal/optimized smokes used explicit verified external
  -X pycache_prefix settings. Final tests, capture, replays and postflight
  use explicit external caches.

No frozen artifact was overwritten. All final source identities cover these
corrections. The report and roadmap are outside the frozen ledger; earlier
evidence and unrelated RET/core/Track-B work were preserved.

## Boundary and proposed next gate

This is an exact finite observation-deletion calculus. It introduces no
physical-time generator, growth dynamics, geometry, gravity derivation,
ontology, RET integration or Lean installation. It does not extend P's
minimality/consumer authority to the expanded domain.

Proposed QR-05T: local stable refinement on Q/R/S's unchanged raw domain.
Build from raw deletions, using H only for comparison. Start from C=(frame,B,M),
refine using multiplicity-aware odd/even deletion
rows until stable, and independently compare with full-profile refinement
and the actual H fibers. Retain any additional splits or strict coarsening;
do not assume H is minimal. A proof of coarsest stable C refinement would
be restricted to this finite input, with frame/rank measurability checked.
The previous P minimality result is not a substitute for this test.
No T outcome has been computed here.
