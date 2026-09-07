# QR-05T results: coarsest stable refinement from local deletions

6 September 2026. Exact finite gate on S's unchanged observation domain.

## Outcome

Starting from C=(frame,B,M), multiplicity-aware single-deletion refinement
and independent full-subset refinement both split 415 classes into 416,
then stabilize. Their actual terminal fibers are identical to H=(frame,B,M,T).
H was compared after construction, not used to prescribe either refinement.

The checked premises and refinement argument establish the coarsest stable
refinement **preserving C on this finite domain**. This is new expanded-domain
evidence, not a transfer of P's smaller-domain minimality result.

| Inventory | Local route | Full-profile route |
| --- | ---: | ---: |
| Raw observations | 4,447 | 4,447 |
| Initial C classes | 415 | 415 |
| Terminal classes | 416 | 416 |
| Strict rounds / retained rounds | 1 / 2 | 1 / 2 |
| Nonrepresentative member comparisons | 8,063 | 8,063 |
| Signature atoms across both rounds | 35,296 | 175,044 |
| Canonical separation witnesses | 1 | 1 |

The smaller local signature inventory is not a runtime or product-storage
benchmark. All members and all nonzero multiplicities are checked, including
members following the first failure in a fiber.

## Witness and mathematical meaning

The local route separates states 612 and 625 from old C class 147.
Their odd-deletion counts into current class 102 are 2 and 1.
The new child has canonical ID 151. The independently ordered full-profile
witness uses the same states but target class 11 at retained rank (2,2),
with counts 0 and 3. Witness target IDs refer to the current partition;
equal witness IDs across routes are not an acceptance premise.

Each next key contains the old class and the complete current count rows,
so classes can split but cannot merge. Any stable C-refinement must refine
every round: its blocks refine the current blocks, and equal laws into
its blocks imply equal laws into their unions. The first unchanged
partition is stable, hence coarsest among these stable C-refinements.

Frame and odd/even ranks are measurable throughout. Rank-lowering
single deletions and the full-rank self delta give the prospective bound
of at most six strict rounds. Under finite subset closure and these
measurability premises, S's local/full constancy equivalence makes the two
terminal partitions identical. H is separately verified to be locally
closed and then compared by actual membership maps, not class counts alone.

This is a premise-based argument with exhaustive finite signature checks,
not enumeration of every partition or a machine-checked Lean theorem.
It proves neither unrestricted minimum memory nor closure on arbitrary orders.

## Terminal law and trust boundary

The terminal class-local table has 1,576 color/target atoms.
Two local-only constructors recover all 8,231 class-profile atoms,
agreeing with independent raw-subset enumeration. The 22,110 raw deletion
choices and 168,388 fine subset atoms are unchanged.

The terminal certificate checks 173,056 source/target cells, 34,970 base
delta equations, 57,102 color recurrences, 6,656 rank normalizations and
3,732 two-deletion operator coefficients. Direct profile and power-law
comparisons each check 1,400,352 cells. All residuals are zero.
State-profile, pushed-law and quotient-law hashes exactly match S.

The public refine_local helper receives only raw state-target local rows,
ranks, frames and the initial partition. It does not receive H, observables,
raw orders, full profiles or prior artifacts. Its output certifies local
stability of that supplied algebraic input; it cannot authenticate observed
order realization or certify full-subset integrality by itself.
The separate reconstruct_profiles helper retains S's stronger divisibility,
normalization and operator checks on class-local rows.

Three retained algebraic controls show:

- Two strict local rounds can correspond to one full-profile round.
- Equal target supports and row masses can hide unequal multiplicities.
- Identical empty rows must not merge distinct inherited classes.

These controls are not asserted to be observed C realizations.
Additional tests exercise six strict local rounds, nonintegral local systems,
wrong fibers/maps, early stopping, canonical witnesses, native-type/cache
boundaries, cyclic/shared inputs, resource caps and complete output ownership.

S's raw model is the declared dependency. The feature definitions, raw local
and full deletions, all refinement rounds, terminal profiles and laws are
reconstructed independently. Neither executor imports another route,
prior executors or mutable RET/core code. The S bridge uses a checked H-to-L
map and does not assume H equality. Source/mask aliases, the earlier
probability helper, Q's four-variable certificate and P's consumer are not
rerun.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 6,805,377 bytes,
SHA256 `f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8`.
The complete mathematical analysis is 6,312,703 canonical bytes,
SHA256 `f6b13f494a98609e1bd4e5e692554eb38ec3309ac21b87ab9bc16fc0ea333f55`.

| Check | Outcome |
| --- | --- |
| Full normal tests | 186 passed in 333.40s |
| Full optimized tests | 186 passed in 333.85s |
| Exclusive capture | 61.78955491702072s |
| Fresh normal exact read-only replay | 62.5313982089865s, exact |
| Fresh optimized exact read-only replay | 62.585160499991616s, exact |
| Separate JSON-only postflight | 27,486,952 checks in 16.752591917000245s, passed |

The optimized suite has only pytest's expected warning about assertions
outside rewritten test modules. Dedicated bounded normal/optimized subprocess
controls use explicit non-assert guards and each check 90 expected rejections.
They also verify valid shared inputs, output ownership and differing local/full
convergence speeds.

The frozen runner separately dispatches 16 public local-refinement calls,
six private full-control calls and two public terminal constructors across
both routes; it rejects 14 malformed local inputs and 14 malformed analysis
inputs. The postflight reconstructs evidence and metadata, not these dispatches.
It imports no executor, runner or test and reads source files only for hashes.
Its additional rank-bottom-up C-preserving classifier reaches the same terminal
without using either retained trace or H as an oracle.

Six source/protocol files and all 24 prior artifacts matched their pre-test
ledger after tests, capture, replays and postflight. Artifact bytes remained
unchanged after exclusive creation. All final Python runs use isolated mode
and explicit fresh external bytecode-cache prefixes. No frozen source or
artifact was changed after capture.

The protocol and mathematical acceptance criteria were fixed before outcome
execution. Before the first root analysis smoke, review corrected the root
member-comparison loop to evaluate each signature equality explicitly before
combining its flag, preventing short-circuiting after a split. Independent
routes already evaluate every declared comparison. No feature, domain, law
or acceptance criterion was revised in response to the result.
The normal/optimized suites, capture and postflight required no outcome-driven
correction. The report and roadmap are outside the frozen source ledger;
earlier evidence and unrelated RET/core/Track-B work are preserved.


## Boundary and proposed next gate

This remains an exact observation-deletion calculus. There is no physical-time
generator, new growth law, metric or gravity derivation, ontology commitment,
RET integration, apparatus calibration or Lean installation.

Proposed QR-05U: partial-observation filtering on the same domain and law.
Knowing a sufficient H class and receiving only a coarser observation are
different access assumptions. Predeclare bounded prior mixtures, rational
rate pairs, a coarse observation map and two observation stages. Propagate
exact class beliefs using the local-only terminal model, condition on records,
and compare history likelihoods, posteriors and next-question laws against
an independent raw-order oracle. Check normalization, tower identities,
posterior support and zero-likelihood rejection; retain representative/MAP
plug-in failures. Seek without assuming histories with the same latest record
but different predictions. This proposed gate does not validate an empirical
prior or justify relabeling observation stages as physical time.
No U outcome has been computed here.
