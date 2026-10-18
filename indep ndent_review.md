**Independent review of DET: project wholeness, Q/QM, substantial proofs, QR-MAP opportunities and applications**

13 September 2026. Reviewed the current working tree at `/Volumes/AI_DATA/development/det_8_framework-ret`, including uncommitted material. Git HEAD was `c42cac057ba8666ae9195cc7f8f7e1f0bf0a20e2`; that commit alone does not identify the reviewed working tree. “Q/QM” here covers the pair-kernel/quantum-measure program, operational quantum reconstruction, and its connection to record growth and geometry.

Concurrent research updates appeared during final review. The assessment incorporates the new [record-context domain study](docs/validation/t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md) and its 10 witness checks. That study advances the conditional domain construction and sharpens the remaining problem to lawful context transitions; it does not remove the physical selection gap. The source snapshot and file-preservation limits are recorded in section 8.

This is an independent assessment of the available arguments, implementations and evidence, with separate reviews of foundations, project integration, and QR opportunities. It is not an exhaustive audit of every historical model, a fresh release certification, or evidence that DET describes nature. Recommendations are proposed work; no source, governance, experiment or existing research artifact was changed for this review.

**1. Overall assessment**

DET has become a more credible research framework than its older “derivation” vocabulary suggests. Its strongest current assets are a disciplined distinction between assumptions and conclusions, useful exact counterexamples, careful record/process semantics, and a substantial body of finite inference and information-preservation work. The September 12–13 Q research is a material improvement: it states actual general mathematical arguments, rejects attractive constructions when they fail, and identifies the operational premises that remain missing.

The project is nevertheless incomplete in three different senses. **As software**, the supported core is narrower and better controlled than the surrounding research modules, and RET calibration remains unfinished. **As mathematics**, the recent results do not yet form one operational theory with selected preparations, transformations, composites and growth dynamics. **As physics**, there is no DET-derived complex quantum theory, manifold-producing law, mass mechanism or Einstein limit, and no validated DET-specific experimental advantage. These are distinct gaps; more software tests cannot close the latter two.

The central scientific bottleneck is now **selection of the operational domain and law**. Granting a strongly positive complex pair-kernel produces a Gram representation, but does not determine which preparations exist, which tests are allowed, which updates occur, how systems compose, or why the selected law should generate spacetime. The newer classical and real-quantum countermodels make this a logical obstruction, not merely unfinished algebra. Adding explicitly labeled principles is a legitimate way forward, already permitted in the current research record; it changes the theorem's premise set and must remain visible.

The best near-term route to substantial proofs is a connected theory of **predictive sufficiency, lawful domain transitions, silent-process elimination, and record-preserving composition**, together with a narrowly stated operational reconstruction. A second, independent lane should investigate order generation. It should first exclude fixed-width and other degeneracies before attempting a continuum theorem. Mass and gravity can guide candidate construction, but should not serve as the success criterion for another collection of supplied-geometry calculations.

The most promising practical value is equally concrete: determine what information a measurement decision needs, what can safely be forgotten, when available observations cannot identify a quantity, and which additional measurement would resolve that limitation. RET and QR already contain substantial ingredients for that program. They need consolidation, calibrated comparisons and one actual user/data problem more than additional application labels.

My recommendation is to organize the next work around **one publishable mathematical argument and one bounded application evaluation**, while maintaining a separately scoped foundations investigation. Retain the negative results. They identify exactly where DET must acquire new explanatory content.

**2. What is established, and what remains open**

| Area | Defensible present result | What it does not establish |
|---|---|---|
| Supported formal core | Explicit exported API; local G1 engineering closure with dated environment/source evidence | Correctness of every importable research module, empirical validation, or a current whole-tree release |
| RET | Implemented offline inference, action ranking, provenance, replay and guarded workflows | Closed G2 calibration, measured application advantage, general time-series inference, or autonomous experiment control |
| Pair-kernel mathematics | Given Hermiticity, biadditivity, normalization and strong positivity: finite Gram representation and norm-squared event weights | Strong positivity from grade-2 alone; physical measurement operators; unique updates; full QM |
| Conditional QM completion | A stated operational reconstruction framework, compatible kernel encoding and chosen finite instrument/growth protocol | Derivation of that framework from the older DET premises, or uniqueness of the chosen law |
| Non-entailment results | Compatible classical, real-quantum and restricted-system examples defeat specific proposed implications | Impossibility of every stronger DET theory; independence of every reconstruction axiom |
| Activity/commit/access | Useful immutable semantic separation; record-fiber sufficiency theorem; conditional first-commit construction including nontermination | A native silent dynamics, occurrence mechanism, physical duration or eventual-commit guarantee |
| Operation-domain obstruction | Full-cone, positive-linear, total-entry-normalized instruments have state-independent branch probabilities; residual sums can diverge | Impossibility of informative restricted-domain theories or of conditional quantum image cones |
| Record-context domains | Closed convex exact-recordability cones for supplied partitions; informative readouts and conditional cuts; serial-closure and selector counterexamples | Physically selected preparations/contexts, unique updates, or a lawful general transition between contexts |
| QR finite summaries | Exact, domain-relative closure/minimality, query admission, uncertainty and identifiability results | Universal minimal memory, demonstrated computational superiority, unrestricted transport, or spacetime emergence |
| Order/geometry | Finite correspondence and inverse-problem mathematics; a general width-two obstruction for the current two-port law | A native manifoldlike limit or physical count-to-volume identification |
| Mass/gravity | Explicitly authorized research targets; unchanged GR remains the physical baseline | A derived mass spectrum, stress-energy coupling, gravitational response or Einstein equation |
| Ontology | A coherent research vocabulary with increasingly explicit Status-M boundaries | Empirical preference for presentism, agency, open becoming or metric-as-record |

The main source trail is [the public core boundary](det8/core/__init__.py), [G1 closure](docs/validation/g1-core-hardening-2026-09-04.md), [RET SDK](docs/RET_SDK.md), [QR-MAP](docs/track_b/QR_MAP.md), [strict derivation](docs/validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md), [hypothesis audit](docs/validation/t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md), [operation-domain analysis](docs/validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md), and [geometry dependency plan](docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md).

**3. Findings that should change decisions**

**F1 — The project needs one current dependency/status map. High priority for project wholeness.**

The root documents describe different execution states. [README](README.md), lines 13–17, and the [progress record](docs/validation/core-hardening-progress.md), lines 3–19, say G1 is locally closed and G2 is progressing. [ROADMAP](ROADMAP.md), lines 13–37, still makes core hardening the first implementation priority and says to begin the original baseline work. Older blanket deferrals also coexist with explicit later research exceptions.

This review does **not** interpret the active research as unauthorized. The [September 5 charter](docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md), lines 18–23, explicitly permits a parallel mathematical lane; the opening authorization updates in [QR-MAP](docs/track_b/QR_MAP.md) and the [expanded plan](docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md) record later permission for additional axioms, mass and gravity research. [PHYSICS](PHYSICS.md), section 5, itself combines that update with an older blanket deferral.

The practical problem is discoverability: a new contributor cannot reliably determine the active premise set, authoritative result, supported interface or next obligation from the landing documents. A current map should distinguish release gates, separately authorized research, and retired physics. It should mark superseded prose explicitly and point to one owner for each live claim. Historical entries should remain historical rather than compete with current instructions.

**F2 — New mathematical qualifications have not propagated consistently to old executable research. High priority before reuse.**

The public [core facade](det8/core/__init__.py), lines 1–7, expressly excludes research predictions. That boundary matters: the following findings concern experimental research modules, not evidence that the supported core or RET failed G1.

| Location | Verified issue | Consequence |
|---|---|---|
| [pair_kernel.py](det8/models/pair_kernel.py), lines 89–130 | `is_positive_semidefinite()` uses a Cholesky path that rejects zero pivots. The normalized PSD matrix `diag(1,0)` returns `psd=False`, `valid=False`. | Singular states, nullspaces and pure-state examples central to the current theory cannot use this as their positivity oracle. |
| Same file, lines 164–167 | `commit_kernel()` returns raw block weights without checking a complete, disjoint, recordable partition. For `[[4,-2],[-2,1]]`, singleton weights are `[4,1]`. | A normalized PSD kernel does not make arbitrary block weights probabilities. A consumer can silently cross the exact recordability boundary. |
| Same file, lines 175–185 | The docstring says additivity holds “iff” exact decoherence. `[[1/2,i/4],[-i/4,1/2]]` is additive on the singleton partition but has nonzero off-diagonal decoherence functional. | Exact decoherence is sufficient; ordinary weight additivity does not force the full complex cross terms to vanish. The current diagnostic reports this case as consistent. |
| [why_complex.py](det8/models/why_complex.py), lines 17–28 | Its opening inference still treats a nonzero symplectic form plus reversibility as forcing the claimed compatible complex structure. | The newer strict derivation already gives a counterexample to the unqualified `J²=-I` claim; testing a compatible family does not justify arbitrary inputs. |
| [grade2_justification.py](det8/models/grade2_justification.py), line 42 | The certificate abbreviates the implication to “grade-2 ⇒ Gram/Hilbert.” | Strong positivity is an additional, essential hypothesis; see F3. |

The first two limitations were already recognized in the [September 5 charter](docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md), section 3. They are unresolved integration debt, not newly discovered foundations objections. The present exact derivation checks correctly avoid the defective oracle. The necessary follow-up is a research-interface repair or explicit quarantine with migration guidance, followed by adversarial cases that exercise the actual contract. Do not merely add another cautionary paragraph elsewhere.

**F3 — Strong positivity needs its own place in the proof roadmap. High scientific priority.**

The latest [strict derivation](docs/validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md), sections 1–2, correctly assumes strong positivity. Some older summaries compress “given grade-2” into a Hilbert-space conclusion. That implication is false without additional hypotheses.

A small independent counterexample makes the distinction exact. Let the alternative set have three elements and define

\[
\mu(A)=\frac{|A|(|A|-1)}{6}.
\]

This is nonnegative on every event, normalized on the full set, and grade-2: it is a sum of pair contributions, so the third-order interference expression vanishes on disjoint sets. Every singleton has weight zero, while every two-element event has weight `1/3`. If a strongly positive matrix represented it, each diagonal entry would be zero. PSD Cauchy–Schwarz then forces every off-diagonal entry to vanish, contradicting the pair weights.

Thus absence of third-order interference does not establish strong positivity or a Gram representation. Even an idealized `I₃=0` result would leave that obligation open; a finite experimental bound is weaker still. A substantial DET argument must either justify strong positivity through an independently stated operational/composition principle or retain it as a premise. This counterexample is elementary and is not claimed as novel mathematics.

**F4 — “All-level extension gives quantum” needs a precise endpoint. High priority for the Q/QM roadmap.**

[correlation_frontier.py](det8/models/correlation_frontier.py), lines 8–19 and 219–235, still equates the full NPA limit with an unqualified quantum set `Q`, while simultaneously leaving the equivalence between DET extension and NPA extension open. [record_extendability.py](det8/models/record_extendability.py) uses related language. Two separate implications are being compressed.

First, projective consistency of pair-kernels is not automatically the NPA word algebra with its operator identities and locality relations. That translation needs a proof. Second, the original NPA convergence theorem explicitly gives a representation by **commuting measurements**. In general this is not the closure of finite-dimensional tensor-product correlations: `C_qa` is strictly contained in `C_qc`. These distinctions are stated in the primary [NPA paper](https://arxiv.org/abs/0803.4290) and [MIP*=RE](https://arxiv.org/abs/2001.04383).

Before pursuing this route, define whether the target is fixed finite-dimensional QM, the union/closure of finite tensor-product models, or a commuting-operator theory. State the required additional dimension, tensor-product or realization assumptions. A CHSH/Tsirelson check does not decide among these endpoints. This qualification does not invalidate the separately stated finite operational reconstruction; it prevents an older all-level argument from being mistaken for that reconstruction.

**F5 — The operational-domain obstruction is the immediate foundations bottleneck.**

The [September 13 domain theorem](docs/validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md), section 3, is a sound and consequential rejection of a particular attempted completion. On the full PSD cone, the normalization functional is

\[
m(d)=\mathbf 1^\dagger d\mathbf 1=\operatorname{Tr}(\Gamma d),
\qquad \Gamma=\mathbf1\mathbf1^\dagger.
\]

For globally positive linear complete branches, their effects sum to the rank-one `Γ`; each is consequently a scalar multiple of `Γ`. All normalized inputs yield the same branch probabilities. This remains true for recorded adaptive controls within the stipulated full-cone class. The theorem does not require complete positivity.

The same note supplies a positive zero-mass direction along which residual first-commit sums diverge even as outcome probabilities converge. These are not incidental numerical problems. They show that an unqualified “PSD kernel = operational state” identification fails under the proposed normalization and operation class.

There are legitimate escapes: restricted preparation/test cones, compatible quantum encodings, a well-defined operational quotient, or a different explicitly proposed interpretation of transformations. The existing quantum encoding already demonstrates one conditional escape. **None selects itself physically.** Merely changing total-entry normalization to trace, or choosing a familiar operator, would insert the answer unless its role is openly declared.

The next work should therefore classify domains and transitions, asking which support informative records, coherent composition and controlled residual limits. Strictly positive normalization is one useful sufficient condition, not the only possible escape. A recordable restricted cone can still contain zero-mass positive elements; the operation-domain note explicitly recognizes this in section 5.

**Late update: an actual conditional domain construction now exists.** The new [record-context study](docs/validation/t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md), sections 2–4, defines `K_P` by PSD plus vanishing aggregate cross terms for a supplied partition `P`. It proves closed convexity, normalized informative weights and admissible conditional cuts, retaining the `3/4` versus `1/4` coherence witness. This is meaningful progress on the first part of P1 below; it should not be described as still awaiting its first mathematical example.

Its counterexample shows why the harder task remains: two partitions can both be exactly recordable initially, yet conditioning on an outcome of one takes the residual outside the other's recordable domain. The note also proves that a specified deterministic, kernel-only, relabeling-covariant selector cannot always choose a nontrivial recordable context. A record/apparatus-conditioned transition or explicitly proposed stochastic selector remains possible, but must be specified and justified. The immediate target is now **context-transition closure and availability**, rather than another fixed-context normalization proof. The new zero-mass examples also reinforce the need for O2–O3.

**F6 — The newer countermodels rule out a proof of full QM from the presently admitted premises.**

The [hypothesis audit](docs/validation/t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md), lines 24–46, fixes a defensible source theory before testing implications. Its classical completion has no purification of a mixed bit by a pure classical joint state. Its real-quantum completion has joint distinctions invisible to all product effects. Its powers-of-two-only classical system catalogue cannot efficiently and losslessly realize a three-state face as a whole available system. The arguments quantify over the relevant classes; they are not just failed searches.

The constructive response is to state a stronger theory and prove what it entails. The [principle-selection report](docs/validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md), sections 6 and 9, already distinguishes a state/effect/reversible-structure route from the full-instrument CDP route. The latter requires the full operational framework and its postulates, including purification with the specified uniqueness. The [primary CDP reconstruction](https://arxiv.org/abs/1011.6451) is a benchmark, not a theorem that follows from the word “record.”

Choose one endpoint and complete its premise audit. Do not accumulate attractive axioms from different reconstruction schemes and inherit whichever conclusion is strongest. Identity-atomicity, continuous reversible controllability, local tomography, face closure, and energy observability have different jobs and different background requirements. Even a successful state-space classification does not select a Hamiltonian or the precursor/growth law.

**F7 — Geometry work needs a new generator; the current finite protocol is structurally unsuitable.**

The [geometry plan](docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md), section 1, proves that the present `L_XYZ` histories are unions of two port chains and have width at most two. A causally faithful, volume-filling approximation to a spatially extended Lorentzian neighborhood must eventually sample three mutually unrelated positive-volume regions. Width two forbids that. Increasing the residual Hilbert dimension or repeating quantum checks cannot fix this order obstruction.

The limitation is qualified correctly: it does not exclude sparse worldline traces or representations that discard the source order. Nor is poset width the same as order dimension or spacetime dimension. The protocol remains useful as a finite quantum-record example.

The same proof excludes any fixed finite number of chain-forming ports from arbitrarily fine, volume-filling approximations: width is bounded by the port count, while a spatial neighborhood contains arbitrarily many mutually unrelated small regions. Adding a third fixed port is therefore not a general solution. Conversely, unbounded width alone proves very little; a pure antichain already has that property without supplying Lorentzian geometry.

The broader point is already recognized by [QR-05 adjudication](docs/track_b/QR05_ADJUDICATION.md), lines 54–74: a metric, growth distribution or separation kernel supplied to an inverse calculation is an input, not an emergent output. Modern order-and-number reconstruction results concern precisely specified classes and sampling information; they do not make every finite poset a spacetime. See [Braun's reconstruction paper](https://arxiv.org/abs/2507.01907) and the hypotheses recorded in the local geometry plan.

Require a candidate generator specified independently of target coordinates, then an existence/convergence argument for a declared limiting object. The first screen should include growth of antichains, local finiteness, degeneracy and sampling/measure behavior. Passing those screens is necessary evidence about a candidate, not sufficient evidence of manifoldlikeness.

**F8 — Engineering evidence is extensive but fragmented; it does not currently bind the whole research program.**

The earlier G1 closure has persisted source/runtime-bound reports. However, [capture_baseline.py](scripts/capture_baseline.py), lines 51–53, excludes all `docs/validation/` paths from its source inventory. Many active QR implementations and tests now live under that directory. [pyproject.toml](pyproject.toml) sets default pytest discovery to `det8/tests`; the regular checkout validation does not thereby execute the separate QR studies.

This is not a finding that QR evidence has no hashes: numerous bundles have their own source identities, independent references and replay checks. The gap is the absence of a clear, unified research inventory connecting each result to its complete executable dependency set and supported invocation. A core pass must not be presented as coverage of those research sources.

There is also a concrete retention limitation. The [RET bank-generation checkpoint](docs/validation/ret-sdk-bank-generation-implementation-2026-09-05.md), lines 154–161, gives hashes for JUnit files under a temporary directory. The cited `candidate-bound-full.xml` was absent during this review. The written checkpoint remains useful evidence of a reported run; the absent raw report cannot be independently inspected here. This does not retroactively invalidate the persisted G1 artifacts.

Finally, that checkpoint's “Remaining gate work,” lines 171–182, still lists the bank-only evaluator, consumption/freeze bindings, full 38,000-replication development evaluation, fresh audit, final matrix and wheel checks. G2 remains open. Completing a generator or passing arithmetic tests is not calibrated action-selection performance.

**F9 — The application roadmap exceeds the present RET model class.**

[RET SDK](docs/RET_SDK.md), lines 163–177, exposes Gaussian linear/correlated inference and a bounded exponential response, with no general mixture, change-point or stochastic parameter-drift interface. Deterministic time features can support ordinary drift regression. The thermal demonstration uses a static drift coefficient, supplied temperature response, predetermined acquisitions and four terminal held-out records; it is candid about this at lines 27–39.

The [materials plan](docs/CORE_HARDENING_AND_APPLICATION_PLAN.md), lines 146–166, appropriately calls for real drift/recovery data and conventional alternatives that may include random walks, state-space behavior and multiple timescales. The gap is not solved by calling the current thermal example a monitoring system. Select an initial task compatible with the existing model family, or scope and calibrate the missing inference extension before claiming monitoring utility. Evaluate future prediction and decision quality across time/device splits, rather than only fitting historical curves.

There are also specific defects in older applied comparisons that should be resolved before they become pilot evidence. They are outside the supported RET facade and are consistent with the existing MM-02 repair backlog:

| Source | Finding | Required interpretation or repair |
|---|---|---|
| [applied_tests.py](det8/applied_physics/applied_tests.py), lines 245–249; [adversarial.py](det8/applied_physics/adversarial.py), lines 87–102 | The baseline fits both slope and intercept but passes one fitted parameter to the BIC comparison. | Audit the likelihood and fitted-parameter accounting. The DET grid also searches five named quantities at lines 38–57 but some comparisons pass four; determine identifiable model dimension rather than replacing a number mechanically. |
| [applied_tests.py](det8/applied_physics/applied_tests.py), lines 178–192 | The qubit comparison returns negative squared roughness discrepancies through the BIC result interface. Its independent-noise reference is `0.02`, although the statistic sums 19 neighboring differences. | These are heuristic scores, not BIC. Under the stated independent noise with standard deviation `0.1`, the expected sum is `19 × 2 × 0.1² = 0.38`; calibrate the whole statistic and use realistic alternatives. |
| [applied_physics.md](docs/applied_physics.md), lines 122–129 | The log-linear form `a log(1+t)+bt+c` is described as monotonic. | Its derivative `a/(1+t)+b` can change sign. Retain curvature-capable baselines, but correct the stated rationale and independently reproduce the historical fit before reusing its quantitative claims. |

The same applied narrative says that `κ` “remains useful” after a negative GNSS result. Practical usefulness is still to be established by the held-out application gate. A negative comparison neither rules out every possible engineering descriptor nor demonstrates that this particular descriptor helps.

**F10 — Ontological wholeness needs an explanatory ledger, not promotion by mathematical association.**

The activity/commit/access distinction repairs an important ambiguity: a record trace is not automatically the full present state, and no new record does not imply no residual activity. The current [record-process contract](docs/track_b/RECORD_PROCESS_CONTRACT.md) and [sufficiency theorem](docs/track_b/QR_MAP_RECORD_SUFFICIENCY.md) make that separation precise. They improve the ontology's formal expression without deriving first-outcome formation or a physical time parameter.

The repository's own [comparative adjudication](docs/deadlock_adjudication.md) is stronger than some compressed “standard deadlock” descriptions in [ONTOLOGY](ONTOLOGY.md), especially lines 72, 95 and 101. The adjudication correctly asks for symmetric comparisons and separates interpretive usefulness from empirical preference. That standard should govern the landing narrative too.

For every major claim, state whether DET explains a mechanism, provides an interpretation, proves a consistency condition, or organizes an experimental question. Commit-as-primitive is a permissible ontological commitment; it is not a derivation of occurrence. Removing an agency variable prevents a hidden physical adjustment; it does not establish agency. A sufficient history coordinate can be useful even when every effect has a conventional cause. These distinctions let the project become more whole without pretending that every layer validates every other layer.

**4. A roadmap to substantial proofs**

A substantial result should quantify over a declared model class, reduce a live uncertainty, and expose the hypotheses under which it fails. A short no-go theorem can meet that standard. A large exact enumeration can also be valuable, but only proves its stated finite domain unless supported by a general argument. Formal verification can strengthen a correct formalization; it cannot repair a missing premise or supply physical meaning.

The following is a proposed dependency order, not new official gates or a promise that foundational problems can be completed on a schedule.

| Work package | Concrete mathematical deliverable | Completion or stopping condition |
|---|---|---|
| P0 — Consolidate the theory being proved | A typed premise/result map: record grammar, admitted pair-kernel extension, operational completion, selected law, observation interface | Every active theorem identifies its precise premises and source; contradictory executable certificates are repaired or explicitly excluded. |
| P1 — Operational domains and transitions | Build on the new exact-recordability cones: specify record/apparatus-conditioned transitions, normalization, mixing and allowed composites; prove when sequential probabilities and updates remain well-defined | A conditional informative domain now exists. Complete transition closure/availability or give a counterexample identifying the failed requirement. Do not assume the full cone is one physical system. |
| P2 — Predictive quotient and minimal retained information | A constructive characterization of future-test equivalence for finite controlled residual processes, including domain changes and controller context | Give a finite decision method and a separating future experiment when equivalence fails; state exactly what minimality means. |
| P3 — Silent activity and complete record processes | General first-commit existence with nontermination, plus compatibility of quotienting with silent elimination and append branches | Prove convergence on the selected spaces, preserve never-commit probability, and expose tail/error bounds where available. A scalar probability sum alone is insufficient. |
| P4 — One operational QM endpoint | A complete implication from an explicit stronger premise set to either state/effect structure or the full instrument theory | Discharge or explicitly assume every premise; show how the audited countermodels are excluded. If a further model survives, retain it and narrow the theorem. |
| P5 — Unbounded record-process consistency | Under measurable, normalized typed transitions, construct a countable-history probability law and prove the precise relabeling/schedule invariance claimed | Verify extension hypotheses, quotient measurability and scheduling/fairness assumptions; distinguish classical record probability from an infinite quantum decoherence functional. |
| P6 — Native order-generation candidate | A fixed law producing precursor ideals and full residual updates, with analytic growth/nondegeneracy results | Reject fixed-width candidates for volume-filling roles; stop or redesign when a target metric or external growth rule supplies the claimed conclusion. |
| P7 — Limit, matter and coupling | For a surviving candidate, a declared topology/measure limit, then justified propagation and matter–geometry dynamics | Prove existence before using reconstruction uniqueness; distinguish inserted scales, a spectral gap, inertial mass, gravitational source and Einstein dynamics. |

P1–P3 are the strongest near-term mathematical program because they connect directly to both the new obstructions and existing useful finite results. P4 can proceed with openly adopted quantum assumptions while P6 develops an independent order law. They need meet only for a joint quantum–geometry claim. RET calibration and a bounded application can proceed in parallel without claiming that those foundations are settled.

**What P0 should contain.** Distinguish at least five objects now too easy to conflate: an event-algebra decoherence functional, a residual operational state, a transition instrument, a committed record poset, and an accessible observation. Record each object's type, normalization, available operations and relationship to the others. Distinguish an algebraic identity from an operation's physical availability. The existing `ProcessState` representation is useful scaffolding, but its arbitrary immutable residual payload is not itself a state-cone theorem.

**What P4 should aim to prove.** There is no prospect of proving a conclusion already refuted by compatible countermodels without strengthening or restricting the source theory. A credible paper can instead establish “this independently motivated extension of DET has exactly this operational structure.” The hard contribution is the motivation and sufficiency of that extension, or a new impossibility result about it; re-encoding the published quantum conclusion is a representation result. The current conditional completion should remain a reference model against which a proposed stronger principle is tested.

**The bridge from exact proofs to measurements.** Alongside P2–P4, develop bounds for approximate recordability, imperfect branch-map commutation, finite-horizon error accumulation and truncated silent-process tails. Conditional-state estimates must expose their dependence on small branch probabilities; a tiny error in an unnormalized rare branch need not imply a tiny error after conditioning. A uniform first-commit tail requires a proved or calibrated contraction condition, not normalization alone. These bounds should identify where a claim becomes inconclusive. They would contribute more to an empirical interface than another exact known-answer quantum fixture.

**What P5 must keep separate.** Consistent classical finite record distributions on suitable countable/standard measurable spaces can support a conventional extension argument. A law on labeled append sequences, a law invariant under causal reorderings, and a measure on unlabeled infinite causal structures are different constructions. In particular, different schedules must not silently change which interventions happen or starve an available event. An infinite-history quantum kernel additionally needs its own positivity and continuity/countable-additivity conditions; it does not follow just because finite record probabilities extend.

**What P7 would require.** A meaningful geometry theorem needs a specified scaling sequence, topology of convergence, local measure and nondegenerate limit. An inertial-mass statement needs a defensible time/energy and momentum/translation interpretation, then dispersion or response appropriate to that regime. A graph eigenvalue alone is not mass. A gravitational statement additionally needs a source, conservation, backreaction and a controlled relation to GR or its weak-field limit. These are a research program with uncertain feasibility, not the next few finite certificates.

The first consolidation cycle should end with P0, a sharply specified P1 candidate, and one completed theorem/counterexample from P2 or P3. The next cycle should turn that result into an independently reproducible mathematical note and test whether an application actually benefits. Avoid promising a date for full QM, continuum emergence or gravity before a viable premise set and generator exist.

**5. Separate assessment of opportunities in the current QR work**

The QR work has not missed the obvious objections. It already recognizes supplied geometry, restricted domains, loss of quantum payload, nontermination, and the difference between schedule invariance and relativity. It also already has finite minimal-summary algorithms. The opportunities below are connections or extensions that remain underdeveloped; they should not be presented as discoveries of concepts the repository already contains.

**O1 — Connect finite thinning summaries to residual-process prediction.**

[QR-05P](docs/validation/qr-05p-minimal-summary-2026-09-06/RESULTS.md), lines 23–84, proves a coarsest closed refinement of a specified finite baseline and implements a consumer that refuses unsupported questions. Its result is not unrestricted predictive minimality. The September 13 [record-fiber theorem](docs/track_b/QR_MAP_RECORD_SUFFICIENCY.md), lines 53–97, instead characterizes sufficiency by all declared future tests but supplies no general executable decision procedure.

For a fixed finite-dimensional real vector space `V` of unnormalized states, a finite action/outcome alphabet, linear branch maps `T_a`, and declared terminal effects, define `W₀` as the span of those effects and recursively set

\[
W_{k+1}=\operatorname{span}\bigl(W_k\cup\{T_a^*f:f\in W_k,\ a\text{ allowed}\}\bigr).
\]

Require each generated word to be a lawful experiment: the maps are available on the declared invariant interface, or legal sequencing is encoded by a finite controller. The dimensions can strictly increase only finitely often; an equality step makes the subspace invariant. On this declared model, two states give identical probabilities to every finite test word exactly when their difference annihilates the terminal invariant space. Store a test word with each added basis effect to obtain an explicit distinguishing experiment when they differ. Finite controllers and finitely many types can be represented by a direct sum; unbounded history-dependent laws do not automatically satisfy these finite-dimensional hypotheses. An executable exact decision procedure also needs coefficients permitting decidable exact linear algebra, such as rational or algebraic numbers, or a certified linear-dependence oracle. Arbitrary real entries give the finite-dimensional mathematical characterization without automatically giving an implementable exact rank test.

This supplies a concrete bridge from finite summaries to a residual-state equivalence algorithm. Include all required terminal observations; extending the conclusion to infinite/no-commit outcomes requires their stated probabilistic/limit semantics. Arbitrary ancillary equivalence also needs the ancillary test family in the model. Minimal linear predictive dimension does not mean minimum physical Hilbert dimension or minimum possible bit storage.

This is established mathematical territory, not a novelty claim: [predictive state representations](https://papers.nips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html) and [finite quantum-process equivalence algorithms](https://arxiv.org/abs/quant-ph/0604085) provide clear comparators. DET's potential contribution is a theorem and usable checker that preserve its full record labels, domain restrictions, silent branches and refusal semantics. Benchmark that contribution against direct state simulation and ordinary equivalence/refinement methods.

**O2 — Generalize first-commit convergence beyond the supplied quantum cone.**

There is a short conditional result worth making explicit before searching for a more ambitious classification. Let each state space be finite-dimensional, with a closed, pointed, generating positive cone `K` and a linear normalization `u` strictly positive on every nonzero element of `K`. Its normalized base is compact, so for some constant `c`, `||z|| ≤ c u(z)` on `K`. Use analogous output cones and normalizations `u_r`. Let a positive linear silent map `Q:V→V` and finitely many positive linear commit maps `B_r:V→V_r` satisfy

\[
uQ+\sum_r u_rB_r=u.
\]

Then the partial maps `H_{r,N}=Σ_{n<N}B_rQⁿ` converge in operator norm. For positive input `x`, their increments are positive; the scalar masses of their partial sums increase and are bounded by `u(x)` through telescoping. The compact-base bound makes the vector partial sums Cauchy. Choose a finite basis from the generating cone to extend convergence to all inputs and hence operator norm. Closedness preserves positivity in the limit. The limiting survival functional retains the never-commit probability.

This proof needs positivity, not a preselected complex Hilbert representation. It explains why the unrestricted total-entry example fails: a nonzero positive zero-mass direction defeats the norm bound. It also shows exactly which part of the existing trace/Choi proof is doing essential work. Complete positivity across specified ancillary systems would require a corresponding argument on those composite cones; it is not inferred from positivity alone.

The compact-base fact is elementary. The substantial research target is a necessary/sufficient or useful sharp characterization of the **allowed domains or operational quotients** on which this construction works, including transitions between them. Strict positivity is sufficient, not a proof that every admissible theory must have it, and none of these conditions selects QM physically.

**O3 — Ask whether divergent residual coordinates are operationally irrelevant.**

The full-cone theorem says every stipulated finite complete record test ignores the normalized residual distinction. In that restricted test theory, all such residuals at a fixed record/context have the same predictive class even though matrix coordinates can diverge. This is a legitimate synthesis of the no-information theorem and future-test quotient, not a contradiction of the claim that the full matrix-valued sum diverges.

The decisive condition is that every allowed continuation, including later domain transitions, respects the equivalence. If a restricted future readout can distinguish the discarded coordinate, the quotient is not lawful for that larger experiment family. Prove this descent condition before discarding information. The result would sharpen the project's recurring “retain the full payload” rule into an exact statement of what must be retained for the claimed questions.

**O4 — Extract a quantitative order-recovery theorem from the causal-operator work.**

The [causal-operator result](docs/validation/qr-05-causal-operator-verification-2026-09-12/RESULTS.md), lines 45–69, establishes an exact reachability theorem and explicitly lacks a noise-threshold guarantee. A useful conditional extension follows without reconstructing an unstable full inverse.

Assume a finite labeled strict order `C`, a matrix `A` supported on `C`, `d>0`, and `G=(dI−A)⁻¹`. Suppose every cover edge has `|A_ij|≥a_min>0` and all measured off-diagonal entries have simultaneous error at most `ε`. A cover has no intermediate causal path, so `G_ij=A_ij/d²`. A noncausal pair has `G_ij=0`. If

\[
\frac{a_{\min}}{d^2}>2\varepsilon,
\qquad
\varepsilon<\theta<\frac{a_{\min}}{d^2}-\varepsilon,
\]

threshold the off-diagonal `|Ĝ_ij|` at `θ` and take transitive closure. Every retained edge is causal, and every cover survives, so the recovered closure is exactly `C`. Signed cancellations on noncover responses do not defeat the conclusion. This is a conditional mathematical consequence derived in this review, not a tested estimator or a new physical result.

The application burden is to justify or calibrate the cover margin and simultaneous error bound, account for missing entries, and quantify failure when the margin is absent. This could support response-network topology identification. It does not reconstruct spacetime or distinguish a true zero coupling from an arbitrarily small unobserved one without additional information.

**O5 — Turn identifiability certificates into measurement-design outputs.**

The atlas contains reusable work on query-specific information, moment reuse, support/placement uncertainty, interval-valued responses and acquisition distortion. For example, [QR-05AM](docs/validation/qr-05am-query-reuse-2026-09-07/RESULTS.md) already distinguishes reusable moments from queries requiring refinement and makes the costs visible. The opportunity is a consumer that returns: identifiable answer, valid interval, explicit indistinguishable alternatives, or the additional observation needed to separate them.

For a finite declared candidate set, a proposed measurement separates some currently indistinguishable pairs. Selecting measurements to cover those pairs gives a concrete combinatorial design problem. With bounded error, use a required separation margin rather than exact inequality; with a continuous domain, prove coverage or retain a partial-identification interval instead of substituting a finite grid. Adaptive policies and correlated acquisition errors require their own guarantees.

The deliverable should be one end-to-end decision problem with measured cost/error benefit against a conventional design baseline. Further synthetic atlas expansion is useful only if it resolves an identified obstruction in that problem or proves a broader theorem.

**O6 — Use record formation versus access as an observation-model discipline.**

The new semantics naturally distinguish a committed null, an absent commitment, an inaccessible record and a delayed receipt. This can prevent silent selection bias in event logs, censored sensor data or intermittent measurement streams. The mathematical opportunity is to factor the latent process, formation mechanism and acquisition channel, then prove which parameters or questions remain identifiable under each declared observation model.

It is not enough to introduce four labels in an API: real data must contain information that distinguishes them, or the output must admit ambiguity. This is a particularly useful connection between QR and the current RET missingness contract, which already requires the adapter to justify the observation mechanism. It is also a prerequisite for treating observed event counts as any physical volume proxy.

**6. Application opportunities, ranked by current fit**

The rankings below are judgments about fit to the reviewed implementation, not market validation or demonstrated performance.

| Priority and opportunity | Existing advantage to test | Missing work and fair comparison | Success criterion |
|---|---|---|---|
| 1 — Offline calibration and next-measurement adviser | RET's explicit covariance, cost, inadequacy, provenance and replay machinery | Complete scoped calibration; use measured comparator/resonator or other suitable calibration data; compare fixed schedules and conventional design methods at matched cost | Calibrated uncertainty and lower decision/measurement cost, including reliable abstention |
| 2 — Question-aware record compression and verification | QR-05P consumer, exact refusal of unsupported questions, future-test semantics | Consolidated library/contract; unseen-domain rejection; realistic sequential-log workload; compare direct storage/simulation and standard refinement | Preserved declared predictions with measured memory/time benefit and explicit separating witnesses |
| 3 — Partial-identification and measurement-design workbench | Exact intervals, query supplements, acquisition-error and identifiability calculations | One real response-network or metrology inverse problem; justified uncertainty/coverage; compare standard constrained estimation/design | Useful bounds and fewer measurements to meet a specified decision tolerance |
| 4 — Materials history/drift pilot | RET provenance plus the proposed history-sufficiency/rank program | Adequate raw data, sample history and environment; model family appropriate to dynamics; chronological/device holdouts and conventional baselines | Improved held-out forecast/alert utility; retain a history coordinate only if it adds value |
| 5 — Quantum protocol and calibration diagnostics | Complete instrument records, branch accounting, schedule checks, residual-memory questions | A narrow offline quantum adapter and validated likelihoods; comparison with standard quantum simulation/tomography and fixed characterization schedules | Detection of real protocol/model errors or reduced characterization cost, not a QM-foundations claim |

For the first opportunity, conventional metrology is a serious baseline. NIST already describes [calibration designs that remove linear thermal drift](https://www.itl.nist.gov/div898/handbook/mpc/section3/mpc342.htm) and [drift monitoring with check standards and uncertainty treatment](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc453.htm). RET should earn its place through decision quality under an explicit covariance, resource and model-inadequacy problem, not by comparing only with an intentionally weak heuristic.

For the quantum opportunity, [IBM's QPU information documentation](https://quantum.cloud.ibm.com/docs/en/guides/qpu-information) provides a concrete data-interface reference for timestamped properties and calibration exports. Its [real-time benchmarking workflow](https://quantum.cloud.ibm.com/docs/en/tutorials/refresh-backend-properties-with-real-time-benchmarking) is an existing characterization alternative. This makes an offline “when is another calibration measurement worth its cost?” study plausible. It does not establish that the available metadata alone identifies a noise process, nor that this checkout has executed such a pilot.

The initial materials question should be “does recorded history improve future prediction beyond conventional present-state variables?” Test rank zero, rank one and higher-dimensional alternatives. This follows the repository's own [predictive-history proposal](docs/record_kernel_physics.md), sections 2–2.1. A scalar `κ` should be earned by transport and sufficiency evidence; do not force a scalar into data requiring several memory coordinates. Engineering value can survive a failure of universal `κ`.

Anomaly triage remains a reasonable later application, but should return bounded model/data conclusions and useful next measurements. A residual unexplained by the available model set is not evidence for a DET mechanism. Clocks, gravitational modification, autonomous laboratory control and broad hosted products have a substantially larger dependency burden than these offline opportunities.

**7. How to make the project whole without expanding it indiscriminately**

Use one compact result record per live contribution: statement, hypotheses, supported domain, proof or counterexample, independent check, executable source/dependencies, observation assumptions, exclusions, and current successor obligation. Link it from the current map. This would reduce the work required to distinguish a theorem, a finite capture, a calibration run and a proposal. Counts of tests, modules and ledger entries should be secondary metadata.

Maintain the useful separation between the supported core, RET, research and retired material, but add explicit interfaces between them. In particular, separate research **source** from research **output** in provenance inventories; register isolated QR checks without implying they belong to the release gate. Preserve reproducible evidence at a durable location when it supports a milestone. A hash printed for a missing file cannot substitute for the file.

A mathematical consolidation should combine the best QR results into a small number of arguments: what a record summary preserves, how continuation can reveal missing information, which operation domains are lawful, and what reconstruction is impossible without added data or premises. Credit finite-state minimization, operational reconstruction and causal-set mathematics directly. Novelty should be assessed at the level of a new theorem, interface or measured algorithmic benefit, not DET vocabulary.

Prioritize independent effort where it changes confidence: adversarial countermodels, a proof reviewer reconstructing an argument without the implementation, an implementation using a different method, and an external analyst replaying an application. Two programs that share a mistaken premise do not independently validate that premise. The present review used separate review passes, but it is not a substitute for external scholarly peer review or independent laboratory replication.

The most defensible integrated project description today is: **an ontological research framework, a conditional record/process calculus with useful finite mathematics, and an offline experimental-inference prototype under calibration**. It can become a substantial contribution by making one of those mathematical connections or practical benefits decisive. Full physical unification is a further objective whose missing premises and construction problems should remain explicit.

**8. Review checks and limits**

The review used local source and argument inspection, three parallel specialist reviews, selected primary literature, and focused read-only execution. The following distinct checks passed in the current local environment:

| Check | Count |
|---|---:|
| `det8.tests.test_record_process` and `det8.tests.test_record_stabilization_scope` | 42 |
| `det8/tests/test_quantum_correctness.py` | 46 |
| `t8-q-strict-derivation-2026-09-12/check.py` | 8 |
| `t8-q-operation-domain-2026-09-13/check.py` | 9 |
| `t8-q-hypothesis-justification-2026-09-13/check_witnesses.py` | 5 |
| `t8-q-operational-completion-2026-09-12/check_law.py` | 9 |
| `t8-q-record-context-domain-2026-09-13/check.py` — late update | 10 |
| **Total distinct focused checks** | **129** |

The hypothesis and chosen-law scripts were run by the foundations review pass; the first four rows and the late-update script were also run directly in the main review. Repeated runs of the same checks are not counted again. Bytecode writing was disabled; pytest plugin autoload and its cache provider were disabled for the focused pytest invocation. No full release matrix, large QR atlas replay, RET calibration bank or empirical experiment was rerun.

Three additional direct calls reproduced the `PairKernel` findings in F2. The grade-2 counterexample in F3 and the proposed conditional arguments in O1–O4 are written mathematical reasoning, not machine-verified new theorem packages. Their intended next step is explicit independent proof review under the stated hypotheses.

The working tree already contained many modified and untracked files. This review performed no cleanup, formatting, source repair, staging or commit. An intermediate before/after inventory of the 3,575 existing files outside `.git` and `.venv`, excluding this requested report, matched on paths, sizes and modification times. During final checks, concurrent work outside this review added the record-context note, its check script and a Ruff cache entry, and updated QR-MAP, the geometry plan and the operation-domain note. Those changes were left untouched; a final whole-tree “unchanged” claim would therefore be inaccurate. All write operations performed by this review targeted this report alone.

The late-update snapshot inspected here had SHA-256 `5b519778ba04a34c974e078e3b6ac3018045c419123633bba801109b4f37b4aa` for `CONTEXT_DOMAIN.md` and `0a273d2c16f9e9a69178c494170f7b15294c7e2faf0fa82f94e23c233131da86` for its `check.py`. The latter passed all 10 tests in this review. These identify that incorporated update, not a frozen whole-repository or empirical certificate.

The highest-value next decision is to commit the research program to **operational-domain selection plus a constructive predictive-sufficiency theorem**, and the application program to **one calibrated offline measurement decision**. Keep a separately stated order-generation problem for the geometry lane. Those choices would turn the current breadth into connected, assessable progress while preserving the strongest feature of the recent work: a willingness to report exactly what has and has not been proved.
