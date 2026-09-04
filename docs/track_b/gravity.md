# DET v8.0 — Track B: Gravity as the Geometry of the Growing Record

**Status:** Track B exploration / position note (Status M). Not a pre-registered prediction; generates no falsifier and no novelty-ledger probe.
**Date:** September 3, 2026
**Purpose:** Answer the question Track A never asked: not *"does κ source gravity?"* but *"what IS gravity, given DET's relational primitives \((V, \prec, \#)\)?"* The retired κ-gravity program failed by reifying gravity's *source* into a field; this note re-describes what the metric *is*, without touching its source. Levers 1, 2, and 4 are developed as §5, §6, and §7; lever 3 (the Metaphysics Ledger entry) is applied to `ONTOLOGY.md` §6.

---

## 1. What this is — and isn't

DET has already attempted gravity twice, and **both attempts were Track A** — they tried to make κ *source* or *modify* gravity. Both are retired (`archive/retired_kappa_gravity.md`):

1. **The mass-independent law** \(F = G_q\lambda_\gamma^2\,\kappa_1\kappa_2/r^2\) — falsified by the equivalence principle.
2. **The two-source field equation** \(\nabla^2\Phi = 4\pi G(\rho_m + \rho_\kappa)\) — withdrawn under Option B (DET is a participation/measurement theory, not a gravity-modification theory).
3. **`κ(r)` from inside-out galaxy growth** — fails the sign test (decreasing κ where flat rotation curves need increasing).
4. **SPARC rotation curves** — not reproducible from the committed tree.

The common failure was not a bug but a **category error**: those programs reified gravity's *source* into κ, which smuggled in a new physical variable and contradicted Option B. They asked "what *generates* the geometry" and answered "κ."

This note asks the ontological question instead: **what *is* the geometry?** That question is answerable with DET's primitives and needs no new field.

---

## 2. Core thesis

> **The metric \(g_{\mu\nu}\) is not an ontic entity. It is the coarse-grained (order + count) description of the relational structure of the causal record \((V, \prec, \#)\). Nothing "curves." Curvature is a property of that structure's trace.**

This is a **re-description of GR, not a modification.** GR's equations stand (Option B: gravity is standard GR). What changes is the answer to the question GR refuses to answer — *"what is curved?"* GR says "spacetime is curved" while treating spacetime as no substance, leaving the sentence a placeholder. DET supplies the referent: the geometry is the coarse-grained relational structure of *actualized events*.

The map onto primitives is direct. The re-foundation (`docs/record_kernel_physics.md` §4) takes \((V,\prec)\), \(\#\), \(R\), \(L\), \(\mathfrak D\), \(K\) as primitives. Gravity is a statement about the **first two** — the pure-relational layer that exists *before* any kernel or law map is invoked. That is why gravity is more Track B than any other force: it lives at the level of the record's own geometry, not in a field on top of it.

- **Anchor:** causal order \(\prec\) and count \(\#\) (observables — `docs/observable_anchoring.md` §2).
- **Excess:** the claim that the metric *is* the geometry of the record (rather than "is modeled by" it) is **Status M** — the ontology, not the observable.

---

## 3. The present-tense precision (the guardrail)

"Gravity operates in the present" needs one disambiguation, because it is exactly where smuggling hides.

**It does not mean gravity acts instantaneously.** Newtonian gravity is instantaneous — that is precisely the smuggling. GR already tells us gravity propagates at \(c\) (waves, retardation, finite speed).

In DET terms, "present-tense" means: at each commit event \(e\), the gravitational influence is carried **entirely by the local record \(R^- = J^-(e)\)** — the causal past, already actualized. There is no action-at-a-distance and no field "out there" waiting to be consulted. This *is* GR's locality: the metric at \(e\) is determined by matter in \(J^-(e)\) through the hyperbolic field equations.

So the correct sentence is:

> **Gravity is present-tense in the sense that it is a constraint on co-present relational structure, actualized locally at each commit — while its evolution is the growth of the record itself.**

And the payoff: GR's constraint equations are *exactly* this (see §7). This is why the "present-tense" reading is not only compatible with GR but is *the same claim* GR's own constraint structure makes.

---

## 4. Why gravity is already half-Track-B

Of the four interactions, gravity is the **only one whose theory is already purely relational**:

| Interaction | Form | Structure |
|---|---|---|
| Electromagnetic, weak, strong | field on a background | substance on a stage |
| Gravity | geometry | no background, no substance, no preferred frame |

The equivalence principle is the statement that gravity is universal (all bodies fall the same), which is the statement that gravity is **not a force but geometry**. GR is already an ontological grammar in search of its referent. DET's contribution is not to invent a new grammar but to **name what the geometry is**: the coarse-grained relational structure of the growing record.

This also explains, retrospectively, why the Track A κ-gravity program was doomed in a way deeper than its sign-test failures: it tried to find a *substance* (κ) where GR has already established there is *none*. One cannot add a field to a theory whose entire point is that there is no field.

---

## 5. Lever 1 — The Problem of Time

**The gravity deadlock DET is built to resolve.**

Canonical GR (ADM form) has the Hamiltonian as a constraint, \(H \approx 0\). The quantum version, the Wheeler–DeWitt equation \(\hat H|\Psi\rangle = 0\), is **timeless** — there is no time parameter. Yet time is experienced. This is the gravity version of the block-universe deadlock (ONTOLOGY §3.1), and sharper than the special-relativistic version because here time is not merely frame-relative but *gauge*.

The standard resolution deparametrizes against a "clock" matter field: pick one physical degree of freedom, treat it as time, and read the rest as evolving with respect to it. DET supplies the ontology that says *why* this works.

DET's answer, transferred directly:

> **Time is not a coordinate recovered from the metric. Time IS the asymmetric growth of the determinate record — the commit events \(X_e\) on \(\prec\).**

The re-foundation already redefined the participation aperture as a process-specific tick intensity (`docs/record_kernel_physics.md` §8):

\[
\Pi_a(e) = \lim_{\Delta N\to\infty} \frac{\mathbb E[\Delta N_a \mid R_e]}{\Delta N},
\]

where \(N\) is the causal event/volume count and \(N_a\) the number of ticks of process \(a\). A **clock is a process whose tick count grows with the record's commit count.** Time is the relational growth of actualized events, and the clock is a local measure of that growth.

The Problem of Time then dissolves: of course there is no time parameter in the timeless constraint surface — time was never a parameter. It is the record's growth, which the Hamiltonian constraint gauge-fixes away when one chooses a foliation.

**Compatibility check.** No preferred foliation is introduced. The boundary of the growing block is \(J^-(e)\)'s boundary, frame-dependent — the "Crystallizing Block" (Ellis 2014), which DET already inherits (ONTOLOGY §4). All observers' present-boundaries are equally valid, exactly as all inertial frames are equally valid in SR.

- **Anchor:** causal order \(\prec\), event counts \(\#\), tick counts \(N_a\).
- **Excess:** "time *is* record growth" is **Status M** — the ontology; the observable is only that order + count recover a manifoldlike time coordinate (T7, still open at the emergence step).

---

## 6. Lever 2 — Time, quantum, and gravity: one openness

**A Track B proposition.**

DET resolves three deadlocks with the *same* move — "the outcome is not yet in the record":

| Domain | "Open" means |
|---|---|
| **Time** (block universe) | The future is not yet committed — \(\Omega\) is possibility, not fact. |
| **Quantum** (Many-Worlds) | The superposition has no fact about which branch — open becoming. |
| **Gravity** (Problem of Time) | \(H = 0\) — there is no distinguished time parameter "already there." |

The gravitational case is the **classical** instance of the same openness that appears quantum-mechanically in superposition. The Hamiltonian constraint \(H = 0\) says time is open (it grows with the record, it is not pre-existing); the superposition says the outcome is open (it is not pre-fixed). **They are the same statement at different levels of the record.**

> **Proposition (Status M):** *time-openness* (\(H=0\)), *quantum-openness* (open becoming), and *gravity-openness* (no pre-existing time parameter) are one relational openness — "the outcome is not yet in the record" — expressed at different levels of the record's structure.

This is why gravity is the hardest problem in foundations, and why the block-universe deadlock and the measurement problem are two faces of one thing: both reify a *relation* into a *thing*. Block-universe reifies time into a coordinate; Many-Worlds reifies branch weights into worlds; the retired κ-gravity program reified gravity's source into a field. All three are the same category error, and DET's "the record is the trace, not the substance" corrects all three at once.

**Discriminator test** (`observable_anchoring.md` §4): no unique observable discriminates "one openness" from "three separate open features." The proposition is therefore **Status M** — a coherence and fruit claim, not an observation. Its value is scored the Track B way: does it resolve the three deadlocks *better* (with fewer independent posits) than the alternatives, and does it motivate the right program? It does the latter — it tells us the order-and-count program (T7) is *the* gravity-adjacent program, because gravity *is* order-and-count geometry.

---

## 7. Lever 4 — GR's constraints as open relational constraints

GR's dynamical split is the cleanest place to see "gravity is a relation, not a thing":

- **Constraint equations** (Hamiltonian + momentum constraints): instantaneous — they constrain what can *co-exist* on a spacelike slice, referencing no future.
- **Evolution equations**: propagate that data forward — the record's growth.

The constraints are the classical, gravitational analogue of DET's **open relational constraint** (deadlock 3.2, ONTOLOGY §3.2): a real relation that does not contain its own outcome. A constraint says *which configurations are lawful* without determining *which is actualized* — exactly as a superposition is a real, phase-bearing relation that does not contain its own outcome.

This connects gravity to the quantum deadlock structurally: the Hamiltonian constraint's timelessness is the classical face of the superposition's openness. Both are "no fact until commit."

- **Anchor:** the constraint equations are formalism — derived from GR, which is anchored to geodesic deviation, redshift, lensing (observables). Borrowed, credited (ADM/Dirac).
- **Excess:** the reading "the constraint *is* an open relation (not merely a mathematical feature)" is **Status M**.

---

## 8. The other two fruits

### 8.1 Background independence — DET never had a background to fix

GR is relational, but *quantizing* it forces a background (to define a Hilbert space, particles, a vacuum). This is the motivation for LQG and the main embarrassment of string theory's background dependence.

DET's event-graph primitivism is **natively background-free**: \((V, \prec, \#)\) are pure relations — no manifold, no fixed metric, no stage. DET has no background problem because it never had a background. This aligns DET with the relationalist program (Rovelli et al.), as an *ontology* rather than a quantization program.

### 8.2 Non-localizability of gravitational energy — a trace of relationality

Gravitational energy has **no local density**: no stress-energy tensor for the field itself, only quasi-local quantities (ADM, Bondi, Brown–York). Usually an awkward technical fact, DET's ontology gives it a *reason*: gravitational energy has no local density because gravity is not a thing localized at points — it is a property of the whole relational structure. One cannot point to "where" the geometry is, because the geometry is not anywhere; it is the connectivity. This is the κ-energy-ledger honesty (PHYSICS §1) pushed to its conclusion: gravity's energy ledger cannot be closed locally because gravity is not a local field.

---

## 9. Anti-smuggling audit

| Question | Answer |
|---|---|
| New field? | **No.** We *removed* "metric as substance" and re-described it as geometry of the record. Net: one fewer substance, not one more. |
| New free parameter? | **No.** |
| New prediction? | **No.** This is ontology; GR's predictions are untouched. |
| Contradicts any observable? | **No.** Equivalence principle ✓, Eötvös ✓, gravitational waves ✓, lensing ✓, redshift ✓. |
| Contact with gravity's *source*? | **None.** We never touch what sources the geometry. That is the separation the retired program lacked. |
| Status? | **Status M** — ontology, like the rest of Track B. Not an observable. |
| Borrowed? | **Yes, explicitly:** Ellis 2014 (Crystallizing Block); causal set theory (order + count, already T7); Rovelli relationalism (time); ADM/Dirac constraints (formalism). |

The load-bearing sentence: **the retired κ-gravity program reified the metric's *source* into κ; this reading re-describes what the metric *is* without touching its source.** That is the difference between smuggling and ontology.

---

## 10. Metaphysics Ledger entry (lever 3)

The following row is applied to the Metaphysics Ledger (`ONTOLOGY.md` §6):

| Term | Status | Physical content | Promotion criteria |
|---|---|---|---|
| Gravity as relational geometry | M | None. Re-description of GR's metric as the coarse-grained relational structure of the causal record \((V,\prec,\#)\). | Unique discriminator distinguishing "metric = geometry of the record" from "metric = primitive field" — or a structural constraint the ontology uniquely motivates (e.g., T7 manifoldlike emergence) |

There is no observable discriminator, so the entry is held for coherence and fruit, not measured — consistent with the treatment of the other Status-M rows.

---

## 11. Honest limits and what is borrowed

- This buys **no new physics**. It is a coherence + interpretation contribution, scored by (a) resolving the Problem-of-Time / background-independence deadlocks coherently, and (b) motivating the right kinematic program — which it does: it says T7 (order-and-count → metric) is *the* gravity-adjacent program, because gravity *is* order-and-count geometry. That is a motivation, not a prediction.
- The active bridge is still **L1–L3** (causal structure, conformal factor via count, metric reconstruction). **L4 is retired** — and this note confirms that retirement was correct: L4 tried to go "geometry → dynamics (Einstein)," which is standard GR, not DET. The ontology stops exactly where GR takes over. That is the correct boundary. The conformal factor is fixed by the **counting measure \(\#\)**, not by \(\Pi/\kappa\) (the retired \(\Pi\) conformal factor must not be cited — see `docs/record_kernel_physics.md`, T7).
- **No novelty-ledger probe is generated.** This note produces no falsifiable probe against a target theory, so nothing is registered in `NOVELTY_LEDGER.md`. A Track B note that produces no probe is held for coherence and fruit, not logged as a miss.
- `F11 "Cosmic Record"` (`docs/track_b/cosmic_record.md`) is adjacent but distinct, and has been reframed (Sep 2026) to treat κ as a fitted predictive-history coordinate rather than a field — it no longer re-smuggles the retired program.

---

## 12. Status and next questions

**Open, not yet developed:**

1. **Manifoldlike emergence.** The one place this reading *could* become a structural constraint is T7's open step (embedding + uniqueness of the recovered geometry). Until that is settled (it is inherited from causal set theory, not resolved by DET), "gravity = geometry of the record" remains ontology, not a derived result.
2. **Ledger-ize the openness proposition** (§6) as a second Status-M row, if it is to be treated as a standing claim rather than an in-note proposition.

**Not on the table:** any contact with gravity's *source*; any gravitational anomaly; any dark-matter/dark-energy claim. All retired under Option B.

---

**See also:** `ONTOLOGY.md` §3.1/§3.2/§4/§6, `docs/observable_anchoring.md`, `docs/record_kernel_physics.md` (§4, §8, T7), `archive/retired_kappa_gravity.md`, `docs/track_b/cosmic_record.md` (F11), `docs/track_b/law_genesis.md` (F10).
