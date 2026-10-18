# QR-05BM results: bounded relative-volume verification

9 September 2026 (Pacific/Honolulu). **Bounded gate complete.** Two independent
exact implementations and a third test oracle agree on the five-world model,
all 80 membership rows, 25 histogram rows and 1,280 joint membership/Z rows.
All 28 tests pass in normal and optimized Python. Both complete replays and
the single alternate-runtime reference analysis match.

This is the first executable check of BL's unknown relative-volume model.
It verifies conditional geometric-measure identification and explicit
obstructions, not physical sampling, an inferred general metric or gravity.
The first capture passed. No source, protocol, fixture or test correction
was needed after the first mathematical evaluation.

## What the exact calculation establishes

The [prospective specification](README.md) fixes two same-order marked
geometries, a density-compensation alternative and two metric rescalings.
Geometric proper-volume integration is kept separate from the weighted
sampling measure throughout both coordinate descriptions.

| World | Proper volume V(Q) | Proper volume V(I) | Geometric target τ | Membership probability q | Bias of k/4 for τ |
|---|---|---|---|---|---|
| A: uniform flat | 1/2 | 1/8 | 1/4 | 1/4 | 0 |
| B: uniform conformal | 5/8 | 17/128 | 17/80 | 17/80 | 0 |
| C: density-compensated flat | 1/2 | 1/8 | 1/4 | 17/80 | −3/80 |
| D: fourfold metric A | 2 | 1/2 | 1/4 | 1/4 | 0 |
| E: fourfold metric B | 5/2 | 17/32 | 17/80 | 17/80 | 0 |

In the positive {A,B} menu, distinct complete population laws identify the
target under the explicitly assumed proper-volume sampler. Direct enumeration
confirms E[k/4]=q and Var(k/4)=q(1−q)/4. Unbiasedness for τ depends on
q=τ; C demonstrates exactly why the sampling premise matters.

Every valid finite membership word and every joint Z word has positive
probability in every world. No world is excluded by support from one
four-record packet. A population-law identification result is not certain
finite-shot selection, and the enumerated report is not acquired data.
The count is sufficient for this fixed iid Bernoulli law; attempt identifiers
still matter for acquisition and packet integrity.

### Whole-law density and scale obstructions

The expanded menu has exactly two complete-law classes:

| Compatible population-law class | Exact target set | What is identified? |
|---|---|---|
| {A,D} | {1/4} | Relative volume, but not absolute scale |
| {B,C,E} | {17/80,1/4} | Neither a unique relative volume nor absolute scale |

These are labeled population-law classes, not candidates chosen by one
observed frequency. The two-value target set is not the interval between
its values.

B/C equality holds for the full unnormalized point-density polynomial and
its normalizer, not just the membership mean. Thus their complete iid point
laws and all common observation channels agree, even though τ differs by
3/80. This explains why more records or richer causal comparisons alone
cannot separate them under the stipulated acquisition laws.

A/D and B/E have identical normalized point and complete record laws while
absolute proper volumes multiply by four. Fixed-quota normalized sampling
does not reveal absolute volume. None of these failures can be repaired by
quietly fitting a new acquisition density after seeing a disagreement.

### Quantum and coordinate checks

The explicit sparse projective-instrument route agrees with independent
classical fair-bit probabilities and computational-basis outer-product
states. All sixteen diagonal entries, including zeros, of every joint
branch state and normalized conditional state are retained. Off-diagonal
entries are exactly zero for these declared preparations and projectors.
Branch traces equal complete joint probabilities. Summing over Z outcomes
recovers the unnormalized membership branch P(y)(I₂/2)^⊗4 and its trace P(y);
dividing by P(y) gives the normalized conditional mixed payload.
The conditional payload at fixed Z is common across worlds. The quantum
extension neither splits the law classes nor adds geometric information.

Under U=2u+1, V=3v−1, both routes transport the metric, proper-volume
measure, scalar density and marked regions. All six scalar quantities
(two volumes, two sampling masses, target and q) agree in both charts for
all five worlds. The scalar density receives no extra Jacobian. This is
coordinate consistency of the same model, not a new physical symmetry test
or evidence that changing physical geometry leaves observations unchanged.

## Access and verification coverage

The record-only estimator accepts only the fixed four-attempt packet schema.
All sixteen membership packets and 256 membership/Z packets have the exact
estimate k/4, independently of Z. It rejects missing, duplicate, reordered,
malformed or extra fields; bool/float/subclass substitutions; mismatched
metadata; and hidden world, probability, coordinate or state fields.
Numerical candidate branch matrices stay in verifier evidence, never in
actual-world-selected observer fields. Valid syntax does not certify a
physical sampler, causal comparator, qubit preparation or detector.

The third oracle reconstructs the entire native report using endpoint
integration, independent chart expansion and scalar outcome laws. Dedicated
tests check native types, labels, complete branch entries, target sets,
source identities, protocol-byte pinning, input immutability and fresh
engine loading. Bounded tamper controls cover duplicate/noncanonical JSON,
Fraction tags, source/freeze/capture changes, late report mutations,
create-only preservation, read-only replay, regular-file limits and timer
restoration. Fault injections use temporary files or mocks; they do not
alter retained evidence or certify a hostile operating environment.

## Execution, chronology and provenance

The checkpoint began from pushed BL commit
`9c910310876f4839040c228e0926355b9810def9`. The prospective README and
machine protocol were written before the independent implementations.
Static review and syntax/lint checks preceded the first source freeze.
Pre-evaluation hardening added literal protocol-byte pinning, strict packet
key types, nonblocking regular-file reads, final freeze-byte readback and
preservation of an earlier enclosing deadline. The test suite uses an
interrupting deadline so timeout cannot merely become a recoverable test
error. These were pre-run corrections, not repairs to an observed result.

The create-only source freeze was produced at approximately 20:07:44 UTC
on 9 September, before the first fixed mathematical evaluation. It binds
eight source/evidence identities: six local specification/code/test files
and both preceding BL documents. No earlier study engine was imported or
rerun; prior evidence is context, not an inherited numerical certificate.

| Check | Observed outcome |
|---|---|
| Python 3.14.0 first capture | Complete native primary/reference agreement; 0.435884 s |
| Normal test suite | 28 passed; 15.600 s |
| Optimized test suite | 28 passed; 15.753 s |
| Normal complete replay | Exact match; 0.491704 s |
| Optimized complete replay | Exact match; 0.499712 s |
| Python 3.11.6 reference-only audit | Exactly one analysis; full native and canonical report match; 0.303085 s |

Each suite caches one complete analysis; additional lifecycle tests use
mocked small reports or retained report mutations, not extra fixture scans.
All runs stayed within the prespecified 30-second analysis and 120-second
suite bounds. No adaptive budget increase, runtime retry or post-first
source correction was required. No timing-sensitive RET rehearsal was
observed running at the preflight process checks.

Retained byte identities:

- [Source freeze](source-freeze.json): 1,056 bytes; SHA-256
  `1a1a63f64631101f1169f61b8a8aa77303b7f3f6d2137438fdba62ac68fcf000`.
- [Complete capture](results.json): 1,029,873 bytes; SHA-256
  `526412cf7a3f94dc118328fe78dda8c1912e79f68ac1ac20d99d419413795ce9`.
- Canonical mathematical report: 1,028,806 bytes; SHA-256
  `034bc866aa3e87e5ad5f93ede8e8feb6a486f075b54d804f9c0c55fab3c54a07`.
  Full reports were compared before hashing, not merely their summaries.

Final byte checks confirm all eight source identities, freeze bindings and
both retained artifact hashes are unchanged. Documentation checks cover
three scoped Markdown files: all 83 local-link occurrences resolve, heading
separation and fenced/display-math delimiters pass, and no trailing whitespace or
conflict markers were found. Ruff passes for all four Python files; Git's
whitespace check passes. These document/lint checks are not extra numerical
tests. The nine BM artifacts and owned roadmap are the only intended
publication changes. The 231 pre-existing dirty status entries, including
separate RET/core/application work and the temporary model file, remain
outside scope. No dependencies or physical devices were changed.

## Next bounded question

Propose **QR-05BN: bounded sampling-density partial identification**. Keep
geometric hypotheses explicit and ask how an independently supplied bound
on a declared sampling-density nuisance changes the exact compatible target
set. Specify the nuisance family, bounds and population-law data before
execution. Preserve world labels and discrete target sets; do not substitute
a continuous interval hull or treat a four-shot frequency as an exact law.
Such a bound is an acquisition premise to justify independently, not a
calibration inferred from these ambiguous records. BN has not started.

This gate does not close QR-05, recover arbitrary geometry, derive quantum
mechanics or gravitational dynamics, validate DET ontology, or release RET
applications. The sampler and marked causal channel remain the main physical
bridge assumptions. See the [roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
