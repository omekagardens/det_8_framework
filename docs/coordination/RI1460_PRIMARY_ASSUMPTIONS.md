# RI1460: What record interfaces supply to a growth theorem

Root-adjudicated RI1459 separates immutable record semantics from probability-law premises. Valid commits preserve old relations and append maximal events, but do not establish record sufficiency, complete normalization or transport between birth orders.

Its finite witness has identical records and fair marks, yet next-relation probabilities 1/4 and 3/4; the record-only average is 1/2. This source-bounded separation supplies no physical realization or failure of augmentation descent.

## 1. Four different kinds of premise

Write X=(C,Z): C=(V,prec,R_comm) is the committed snapshot; Z includes residual state, its interface and relevant controller context. The [record-process contract](../track_b/RECORD_PROCESS_CONTRACT.md), §§1–3, distinguishes silent operations, already-selected commits and passive access.

A commit uses a fresh integer ID and a full strict predecessor ideal, a downward-closed set. It appends one maximal event, retaining old relations and immutable payloads. IDs are not times. Selected probabilities must lie in (0,1]; the interface neither samples nor certifies a complete normalized instrument. Residual encoding does not establish positivity or physical admissibility. API immutability is not a security or physical-storage guarantee.

| Kind | Supplied content | Missing implication |
|---|---|---|
| Interface | Valid append; retained relations | Complete history law |
| Stochastic/model premise | Normalization, state sufficiency, fairness, locality or passivity | Derivation from native dynamics |
| Sufficient certificate | Full swap transport, or local matching plus tails | A candidate satisfying it |
| Physical/interpretive premise | Operational bridge or Status-M reading | Availability and empirical discrimination |

Changing Z need not edit C. Silent evolution, logged nulls, missing access and delayed receipts remain distinct: a logged null appends an event; passive access does not; receipt may follow formation. Call order and append count supply no physical clock.

[Ontology](../../ONTOLOGY.md), §§2–4 and 7, retains Status M: present activity need not equal record growth, local language does not construct covariance, and agency is not a hidden control register. [Observable Anchoring](../observable_anchoring.md), §§1–5, separates registrations, inference, formalism and interpretation. Formal order is not a detector record or calibrated geometry.

## 2. Probability histories are additional input

For a finite birth horizon N, let H_n be finite/countable complete histories, including all relevant marks, residual choices and controller distinctions. Assume rho_n(h)>=0, initial total one, and

    rho_n(h) = sum_(g extending h) rho_(n+1)(g),  n<N.

Include every positive branch. Projection pi_n(h)=F_n retains the completed birth-label relation and commutes with truncation; each extension appends above an actual ideal S without deleting comparisons.

Valid commit sequences support the projection property, not the probability law. Silent segments may be included, but delayed/never-commit mass must be accounted for. Dropping it does not normalize a next-birth row. Conditioning on eventual commitment is a different experiment requiring positive commitment probability.

Define the full projected fiber mass

    W_n(F) = sum_(h:pi_n(h)=F) rho_n(h).

Partitioning all child histories by their last actual ideal, using nonnegative countable summation, gives labeled coherence:

    W_n(F) = sum_(S in I(F)) W_(n+1)(F+S).

At W_n(F)>0, the effective conditional row is

    q_eff(F,S) = W_(n+1)(F+S) / W_n(F).

F_n encodes its projected past: restrictions give F_k, and each newborn's predecessors give its birth ideal. The ratio therefore conditions on that past while averaging hidden histories; their individual laws need not coincide. A lossy view or anonymous endpoint need not retain the past. Zero-mass parents have no defined ratio.

This [RI1458](RI1458_AUGMENTATION_DESCENT.md) step needs neither microscopic sufficiency nor covariance.

## 3. Covariance and the marked corollary need more

Full-fiber transport FT requires probability-preserving bijections between complete positive-history fibers for every adjacent incomparable swap. Reindexing gives equal natural-realization masses. Positive anonymous support through the horizon then gives positive equivariant ratios; matched two-birth products telescope to the same child/parent mass.

FT is sufficient, not necessary, for equal aggregate masses. Arbitrary event IDs, anonymous endpoint information, and immutability establish no such equality.

A local certificate needs complete product-preserving two-step matching, including every augmentation choice and full first precursor, AND reversible continuation transport preserving every later branch probability. Equal unmarked endpoints do not match memory. Isomorphic complete augmented Markov states with transitions intertwining under relabeling can certify tails. Without tail control, local equality leaves an implication unproved; it does not prove covariance false.

The immutable-mark corollary stipulates complete state (F,r), no extra memory or payload-dependent law, normalized q(F,r,S)/2 branches, Markov dependence, transported equivariance and all marked diamonds, including full first precursors. Two fair bits give 1/4; the diamond equates the affected products, while state sufficiency and equivariance equate tails. Existing marks may affect q.

The historical [Law Dependence](../track_b/native_theorem_package_v1/LAW_DEPENDENCE.md) body, §§2/4, states these model restrictions and says they are not derived from bare DET. Listed function arguments do not eliminate native residual/controller dependence; payload immutability proves neither fairness nor passivity.

Exact targets, uniform induced sampling and positive support remain separate premises. The RI1451 obstruction retains its scope; its targets are not API consequences. Removing a premise constructs no escape. Continuous fibers, interfering amplitudes and arbitrary payload evolution remain outside this theorem.

## 4. A complete two-birth separation

This is a declared finite law consistent with the named valid-selected-commit semantics. It is not derived from an implementation or physical kernel.

Start at empty C with retained residual Z=("propensity-bit",z), z=0 or 1 with probability 1/2 each. Its type is fixed and nonempty, its encoding immutable. No residual evolution is used.

Append event 0 above the empty set with independent fair immutable bit b0, branch probability 1/2, fixed outcome kind/label and tuple payload (b0,). No committed field reveals z.

At this singleton the actual ideals are the proper empty ideal and the full ideal {0}. For the second append, event 1, set

| z | q_z(empty) | q_z({0}) |
|---|---:|---:|
| 0 | 3/4 | 1/4 |
| 1 | 1/4 | 3/4 |

Each S has independent fair immutable bit b1 and branch probability q_z(S)/2, fixed outcome kind/label and payload (b1,); z is retained. Empty S gives incomparability; S={0} gives 0 precedes 1. Both alternatives are positive.

Fresh IDs, actual ideals, maximal appends and unchanged old data satisfy the specified semantics. Selected probabilities 1/2,1/8,3/8 are admissible. This is a manual semantic check, not implementation certification.

For each fixed z and first mark, the four second branches have probabilities 1/8,1/8,3/8,3/8 in the appropriate order. Their sum is

    2*(1/8 + 3/8) = 1.

Initial z histories have mass 1/2; first histories (z,b0) have mass 1/4. Second histories (z,b0,S,b1) have mass

    (1/2)(1/2) q_z(S)/2 = q_z(S)/8,

equal to 1/32 or 3/32. Four children sum to 1/4, two first marks to 1/2, and both z to one: the declared law is complete, normalized and prefix-consistent through two births.

Now fix the identical committed singleton C with b0=0. Each z contributes joint mass 1/4, so C has mass 1/2 and each z has conditional probability 1/2. For the next-order event B={0 precedes 1},

    P(B | C,z=0) = 1/4,
    P(B | C,z=1) = 3/4,
    P(B | C)     = (1/2)(1/4) + (1/2)(3/4) = 1/2.

A function of C alone cannot equal both full-state conditional laws. Record-only sufficiency fails, but the C-only mixture and posterior-averaged effective row exist. Fair immutable marks and valid commits therefore do not imply full marked-record sufficiency.

The bit changes a propensity while both outcomes remain possible; it is neither agency nor a future-outcome register. No silent operation is needed, unlike the older silent-flip/readout witness. No FT failure, all-horizon extension, complete native scalar certificate, RI1451 realization, quantum derivation or physical availability follows. Interface consistency is not ontological compatibility.

## 5. The existing factorization criterion and the native obligation

The September [QR-MAP theorem](../track_b/QR_MAP_RECORD_SUFFICIENCY.md), §§1–2, already gives the general criterion. Fix reachable states and common continuation experiments over each C, with the same interface, intervention policy, observation mechanism, control context and complete outcome space.

Record-only predictors exist exactly when every declared t satisfies

    C(x)=C(y)  implies  P_t(. | x)=P_t(. | y)

for reachable x,y. Necessity evaluates one predictor at C; sufficiency defines it using any representative, with equality ensuring independence of that choice. Unreachable records receive no prediction. Measurability is additional, automatic on finite/countable discrete spaces but not arbitrary quotients.

One next-record marginal is weaker than all continuation laws. Operational equivalence proves neither ontological identity nor a unique autonomous Markov law. The older conditional first-commit result retains never-commit mass and restricts its quantum map-convergence claims; it supplies no native silent/commit family.

RI1459 contributes the audit and two-birth witness, not this criterion. Native application needs actual dynamics, reachable full states, protocols/controller context and a normalized future-record law including silent, delayed and never-commit behavior. For each common protocol u, prove

    Law(C_future | C,Z,u) = Law(C_future | C,Z',u)

for equal specified C, including no further commit. Do not omit differing apparatus context or replace the committed state by an assumed complete observer log.

This supplies candidate-specific sufficiency, not a general-FT requirement or covariance proof. An instrument/readout bridge is a different obligation. No dynamics or successor answer is adopted.

## 6. Source coverage, custody and unchanged holds

Coverage is the supplied record contract, ontology, observable anchoring, law-dependence body, public descent result and older sufficiency criterion. Linked implementations/theorem packages and other versions were not inspected; this is not exhaustive DET study.

Historical law locators use the 17,936-byte body, SHA256
`68c38eeb7232f7fd471c6a6bbf74316350408031cbdbd849495ff890a534444a`.
It occurs contiguously at zero-based byte 5,597, physical line 40, in the 36,531-byte public LAW_DEPENDENCE, SHA256
`db448fa7e84c19529fd9351958be8b2bb5749884829e52080022b268b60a100e`.
Its historical §2, §4 and §6 are the relevant model/choice/classification passages. FINITE_LAW_DEPENDENCE is a different work; its title is not a substitute source.

RI1459 author prose is recorded complete at 11:05:58 UTC before 11:11:10. Final 11:07:48, before 11:17:10, remains attributed: its original all-four receipt is absent, and declaration at 11:07:31 is not completion. Reviewer prose is recorded at 11:46:33 before 11:54:19; final all-nine 11:48:13 before 12:00:19 is attributed to the supported handoff, without its original external receipt here.

Retained failures include author display recovery, in-memory shortening and citation reread; reviewer display recovery, its own incorrect quote-punctuation assertion, and over-cap 12,849/12,507-byte drafts reduced to 12,028. The author's quotation was correct. Root recovered a mistaken PREMISES.json lookup and oversized metadata display. Earlier cap/patch, manifest-pin-basis, attributed-completion, missing RI1389 and late RI1401/RI1419 custody limits persist. Current pins do not recreate history.

E retains operator/actuator failure behavior and full cost, latency and source-to-reset closure. NE retains source/reset/control/readout certification in both candidate worlds and history-wise costs. CE retains interface ownership, implementation, runtime/allocator/enforcer and hard-resource gates, with M1 held. Measurement retains bounded record representation/serialization, source/build/ABI/binding, resources, controls, qualification and observed-execution holds. Nominal calculation remains separate from calibration/production assurance; no new calibration or trace prerequisite is imposed.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% stop/reset guard and RET-only pause remain. No physical prediction, agency theorem, operational admission or release receipt follows.
