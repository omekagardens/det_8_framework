# DET v8.0 — Track B: Anthropic Principle (F12)

**Status:** Track B research module (proposed)
**Date:** August 12, 2026 (v2: κ-gravity binding folded into the SPR criterion; prior-sensitivity sweep added)
**Purpose:** Examine whether DET can provide counter-proofs, or evidence for or against, the Anthropic Principle — using ONLY DET primitives. No standard-physics constants are imported.
**Module:** `det8/models/anthropic_principle.py`

---

## 1. The Core Question

> Does DET have anything to say about why the universe appears "fine-tuned" for observers?

The standard Anthropic Principle has two readings of the fine-tuning observation:

| Position | Claim | Standard motivation |
|---|---|---|
| **Weak Anthropic Principle (WAP)** | We can only observe from a universe that permits observers | Selection effect |
| **Strong Anthropic Principle (SAP)** | The universe *must* permit observers | Necessity (often teleological) |
| **Fine-tuning premise** | ~20 dimensionless constants each require improbable tuning | Underlies both WAP and SAP |

The recent ultralight-axion / strong-CP work is one more entry in the standard fine-tuning catalogue (why is the axion decay constant \(f_a\) or the angle \(\theta\) small?). DET does **not** import \(f_a\), \(\theta\), \(m_a\), or any other standard constant. Instead it reframes the *same kind of question* — "why is this parameter in the observer-permitting range?" — in its own vocabulary. That reframing is the subject of this module.

---

## 2. The DET-Native Reframing

DET has no standard-model constants to tune. Its only free parameters are its own primitives:

\[
\lambda_P,\ \lambda_\gamma,\ G_q,\ \kappa_{eq},\ \tau_{rec},\ D,\ K
\]

The one that gates observer-existence is the **structural history field** \(\kappa\), acting through the participation aperture:

\[
\Pi(\kappa) = \frac{1}{1 + \lambda_P \kappa}
\qquad
\text{(all other }\Pi\text{ factors held at unity)}
\]

Higher \(\kappa\) → lower \(\Pi\) → slower participation per event. In the limit \(\kappa \to 1\), \(\Pi \to 1/(1+\lambda_P)\) and present participation stalls.

So the anthropic question becomes:

> "Why does the \(\kappa\)-field settle into a range that permits structured participation?"

This is a *different kind* of question than the standard one, because \(\kappa\) is a **dynamical field with an attractor**, not a fixed constant. DET's candidate answer is therefore not "multiverse" or "design," but "the attractor of the structural-history dynamics."

---

## 3. The DET-Native Observer (Structured Participation Regime)

The Anthropic Principle requires a definition of "observer." DET's minimal analogue is the **Structured Participation Regime (SPR)**:

> A connected record-regime that is (i) gravitationally **self-bound** by its own κ-gravity and (ii) keeps its participation aperture \(\Pi\) above a floor, so present participation keeps producing measurable fruit.

This is deliberately **not** biological life and **not** consciousness — both are quarantined (Status M) in DET. The SPR is the minimal thing that can *measure*, i.e., the minimal DET-native bearer of an anthropic selection effect.

Binding and participation together impose a **window** on \(\kappa\):

\[
\boxed{\,\kappa_{bind}\;\le\;\kappa\;\le\;\kappa_{obs}\,}
\]

- **Binding (lower bound):** \(\kappa \ge \kappa_{bind}\) — κ-gravity holds the regime together.
- **Participation (upper bound):** \(\kappa \le \kappa_{obs} = (1/\Pi_{min}-1)/\lambda_P\).

This is DET's native "Goldilocks" window: too little structural history cannot self-bind; too much stalls participation. It replaces the standard ~20 fine-tuned constants with **one scalar that must fall in one interval**.

---

## 4. The κ-Attractor, the Binding Threshold, and the Window

### 4.1 The κ-attractor

DET's own \(\kappa\)-dynamics (homogeneous, in recovery-time units):

\[
\frac{d\kappa}{ds} = \beta (1-\kappa) - (\kappa - \kappa_{eq}),
\qquad
\beta = \alpha R \tau_{rec}
\]

with fixed point:

\[
\kappa^* = \frac{\kappa_{eq} + \beta}{1 + \beta}
\]

### 4.2 The binding threshold (two-source law)

Under the two-source gravity law (`gravity_v2`), a clump of \(N\) nodes each of mass \(m\) (total \(M = Nm\)), radius \(R\), in a κ-field has self-acceleration \(a = G_{eff}M/R^2 = G(1+\alpha\chi)\,Nm/R^2\), with \(\chi = (\kappa-\kappa_{eq})/\kappa_{earth}\). Binding requires \(a \ge a_{disp}\), giving:

\[
\kappa_{bind} = \begin{cases}
\kappa_{eq}, & \text{if } G\,N\,m/R^2 \ge a_{disp}\ \text{(Newton alone binds)}\\[6pt]
\kappa_{eq} + \dfrac{\kappa_{earth}}{\alpha}\left(\dfrac{a_{disp}\,R^2}{G\,N\,m} - 1\right), & \text{otherwise}
\end{cases}
\]

**Status: P** (proposed). Binding is provided by mass first; κ only contributes when Newton alone is insufficient. Uses \(G\) (empirical, via `gravity_v2`), \(\alpha\), \(\kappa_{eq}\), \(\kappa_{earth}\), and record-side quantities \(a_{disp}, R, m, N\).

### 4.3 The window

The SPR condition \(\kappa^* \in [\kappa_{bind}, \kappa_{obs}]\) is:

\[
\kappa_{bind} \le \kappa^* \quad\text{and}\quad Z := \lambda_P\,\kappa^* \le \left(\frac{1}{\Pi_{min}} - 1\right)
\]

Two structural consequences follow:

1. **One scalar in one interval, not ~20 constants.** The observer condition constrains the single scalar \(\kappa^*\) to a single interval. The upper bound is one combination \(Z = \lambda_P\kappa^*\); the lower bound is \(\kappa_{bind}\).
2. **Attractor, not initial condition.** \(\kappa^*\) is an attractor, so the observer condition is independent of the initial \(\kappa\). Initial-condition fine-tuning (the analogue of the flatness problem) is dissolved: any \(\kappa(0)\) relaxes to the same \(\kappa^*\).

The module verifies both: from six initial values \(\kappa(0) \in \{0, 0.2, \dots, 1\}\) with \(\kappa_{eq}=0.3,\ \beta=0.5\), all converge to \(\kappa^* = 0.5333\) within \(10^{-3}\).

---

## 5. Results: Evidence For and Against

The module runs a Monte Carlo ensemble over DET's *own* parameter space (prior: \(\lambda_P\) log-uniform over \([10^{-2},10^2]\), \(\kappa_{eq}\) uniform \([0,1]\), \(\beta\) log-uniform over \([10^{-2},10^2]\), \(\kappa_{bind}\) uniform \([0,1]\); seed 42, 20,000 draws, \(\Pi_{min}=0.5\)). All symbols are DET primitives.

### 5.1 Ensemble statistics

| Quantity | Prior mean | Posterior mean (given SPR) | Shift |
|---|---|---|---|
| \(P(\text{SPR})\) | — | — | **0.389** |
| \(\lambda_P\) | 10.94 | 0.278 | **0.025** ↓ |
| \(\kappa_{bind}\) | 0.501 | 0.416 | **0.829** ↓ |
| \(\kappa_{eq}\) | 0.501 | 0.551 | **1.10** ↑ |
| \(\beta\) | 10.79 | 13.46 | **1.248** ↑ |

The selection is **two-sided**, and this is the load-bearing new result:

- \(\lambda_P\) and \(\kappa_{bind}\) are selected **downward** — observers loosen both window bounds (raise \(\kappa_{obs}\), lower \(\kappa_{bind}\)).
- \(\kappa_{eq}\) and \(\beta\) are selected **upward** — observers raise the κ-attractor \(\kappa^*\) so it clears the binding floor.
- \(\lambda_P\) is the **most-selected parameter** (shift 0.025), consistent with its role as the single multiplicative lever on the participation bound.

### 5.2 Evidence FOR the Weak Anthropic Principle (selection)

Conditioning on "an SPR is present" produces a coherent, non-trivial, *two-sided* selection effect. The posterior concentrates on looser bounds and a higher attractor. This confirms that the WAP is a well-defined, executable selection mechanism in DET — and DET makes the normally-hand-wavy phrase "we can only observe from an observer-permitting region" precise: an observer is, by construction, a record-regime that already exists.

**Status: CI** (computed instance).

### 5.3 Counter-proof to the Strong Anthropic Principle (necessity)

DET's law map \(\mathcal L\) fixes the *form* of the κ-dynamics but not the free parameters. There are now **two independent ways** to build a consistent observer-free DET universe:

1. \(\kappa_{eq} \to 1\) or \(\beta \to \infty\) drives \(\kappa^* \to 1\), above \(\kappa_{obs}\) (participation stalls).
2. \(\kappa_{bind} \to 1\) raises the binding floor above any attainable \(\kappa^*\) (the window shuts).

Hence "the universe *must* permit observers" is **not a theorem of DET** — observers are contingent. This is a finite counter-construction to SAP *as a claim about DET's own ontology*.

**Status: FT** (finite theorem / counter-example).

**Caveat:** This refutes SAP only if one adopts DET's ontology. It does not, by itself, refute SAP in standard physics, which this module does not engage.

### 5.4 Evidence AGAINST the fine-tuning premise (reduction)

The fine-tuning premise — many independent constants each improbably tuned — does not survive translation into DET. There is **one scalar \(\kappa^*\) in one interval** \([\kappa_{bind}, \kappa_{obs}]\), and one attractor, not ~20 free coincidences. The window itself is the DET-native analogue of the standard "force strong enough to bind but weak enough to not over-bind" structure — but it lives entirely in κ.

**Status: FT/CI** (structural reduction + computed instance).

### 5.5 A DET-native corollary

Because \(\lambda_P\) is the only parameter that enters the observer condition as a multiplicative lever on the participation bound, DET predicts that anthropic selection — if it operates — should single out \(\lambda_P\) specifically. This is consistent with DET's independent result that \(\lambda_P\) is empirically tiny (bounded at \(\sim 10^{-17}\) by the Track A clock program), while \(\kappa_{eq}\) and \(\beta\) are ordinary dynamical quantities. The module does not claim to *explain* the smallness of \(\lambda_P\); it shows that, within DET, \(\lambda_P\) is the unique natural target of any anthropic selection.

**Status: P** (proposed; prior-dependent in magnitude).

---

## 6. Prior-Sensitivity Sweep

The magnitudes above depend on the chosen priors. The module therefore reruns the ensemble under seven prior specifications (varying the \(\lambda_P\) and \(\beta\) log-ranges and the \(\kappa_{bind}\) prior) to separate prior-robust findings from prior-dependent ones.

| Config | \(P(\text{SPR})\) | \(\lambda_P\) shift | \(\kappa_{bind}\) shift | \(\kappa_{eq}\) shift | \(\beta\) shift |
|---|---|---|---|---|---|
| baseline | 0.389 | 0.025 | 0.829 | 1.100 | 1.248 |
| narrow \(\lambda_P\) | 0.405 | 0.227 | 0.820 | 1.086 | 1.201 |
| wide \(\lambda_P\) | 0.384 | 0.003 | 0.833 | 1.105 | 1.263 |
| narrow \(\beta\) | 0.391 | 0.025 | 0.797 | 1.096 | 1.141 |
| wide \(\beta\) | 0.387 | 0.025 | 0.843 | 1.104 | 1.274 |
| \(\kappa_{bind}\in[0,0.5]\) | 0.491 | 0.027 | 0.961 | 1.043 | 1.013 |
| \(\kappa_{bind}\in[0.5,1]\) | 0.290 | 0.021 | 0.942 | 1.203 | 1.629 |

**Prior-dependent:** \(P(\text{SPR})\) ranges 0.29–0.49, and the exact shift magnitudes vary.

**Prior-robust:** the *qualitative* signature is invariant across all seven configs —
1. necessity is always false (SAP rejected);
2. \(\lambda_P\) and \(\kappa_{bind}\) are always selected downward;
3. \(\kappa_{eq}\) and \(\beta\) are always selected upward.

The verdicts (SAP rejected; WAP selection real; two-sided selection) are robust to prior choice; only their magnitudes are not.

---

## 7. Relationship to Ultralight-Axion Fine-Tuning (Contrast, Non-Smuggling)

Standard anthropic arguments ask why a *fixed* constant is small. The axion example asks why \(f_a\) (or \(\theta_{QCD}\)) sits in the narrow window consistent with structure formation / dark matter / absence of strong CP violation.

DET does not import \(f_a\), \(\theta\), \(m_a\), or their window. The contrast is:

| Standard (axion example) | DET-native analogue |
|---|---|
| A *fixed* constant \(f_a\) is "tuned" | A *dynamical* field \(\kappa\) has an attractor |
| Why is \(f_a\) in the permitted window? | Why does \(\kappa^*\) sit in \([\kappa_{bind}, \kappa_{obs}]\)? |
| Answer sought: multiverse / design | Answer offered: the damage–recovery attractor |
| ~20 independent tunings | One scalar in one interval |

The module's axion content is **zero**: the anti-smuggling audit lists \(f_a\), \(m_a\), and \(\theta_{QCD}\) as deliberately excluded, and no standard-physics constant appears in the code. The axion literature serves only as motivation for the *shape* of the question, never as an input.

---

## 8. Claim Register

| Claim | Status | Notes |
|---|---|---|
| \(\Pi(\kappa) = 1/(1+\lambda_P \kappa)\) is the κ-only participation slice | A | Consistent with `det8_core.participation_aperture` |
| \(\kappa^* = (\kappa_{eq}+\beta)/(1+\beta)\) is the κ-attractor | FT | From DET's own κ-dynamics |
| \(\kappa_{bind}\) from the two-source law (mass binds first; κ when needed) | P | DET two-source gravity (`gravity_v2`) |
| SPR ⟺ \(\kappa^* \in [\kappa_{bind}, \kappa_{obs}]\) | FT | Window structure, prior-independent |
| Observer condition independent of initial κ | FT | Attractor convergence verified |
| Observers are contingent (SAP fails within DET) | FT | Two explicit counter-constructions |
| WAP selection effect is coherent and two-sided | CI | Posterior: λ_P/κ_bind down, κ_eq/β up |
| λ_P is the most-selected parameter | CI/P | Shift 0.025; magnitude prior-dependent |
| Fine-tuning reduces to one scalar in one interval | FT | Structural, not statistical |
| \(P(\text{SPR}) \approx 0.39\) under the documented prior | CI | Prior-dependent number (0.29–0.49 in sweep) |

---

## 9. Anti-Smuggling Audit

The observer condition (participation + binding window) uses DET primitives: \(\kappa\), \(\kappa_{eq}\), \(\lambda_P\), \(\tau_{rec}\), \(\beta\), \(\Pi\), \(\Pi_{min}\), \(C\), \(\kappa_{obs}\), \(Z\), plus the two-source gravity quantities \(\chi\), \(\alpha\), \(\kappa_{earth}\), \(a_{disp}\), \(R\), \(m\), \(N\), and Newton's \(G\) (empirical input via `gravity_v2`). Deliberately excluded: \(c\), \(\hbar\), \(\Lambda\), \(\alpha_{em}\), \(f_a\), \(m_a\), \(\theta_{QCD}\), electron/proton masses, dark matter/energy, and all cosmological parameters (\(\Omega_\Lambda\), \(H_0\), \(T_{CMB}\)).

Note (Round 3): self-binding is now computed from the two-source gravity law, which uses Newton's \(G\) as an empirical input (mass is the conserved source; κ modifies the response via \(\chi\)). This is a *correspondence*, not a derivation of \(G\) from DET primitives — consistent with the anti-smuggling discipline. The ultralight-axion / strong-CP question is still not imported.

---

## 10. Open Questions

| Question | Status |
|---|---|
| Is \(\kappa_{bind}\) (Status P) tied to a specific measured regime or to inhomogeneous κ? | Open — the binding ansatz is not yet derived from a concrete bound structure |
| Is \(P(\text{SPR})\) robust under a principled prior justified from DET's κ-gravity/BAO constraints? | Open — the sweep uses agnostic width changes, not a physically justified prior |
| Can "λ_P is the selection target" be turned into a pre-registered prediction? | Open — requires a multiverse/ensemble sampling model |
| Does the window survive when κ is spatially inhomogeneous (diffusion on bonds)? | Open — v2 is homogeneous/mean-field |
| Can the WAP selection be made observationally falsifiable (not just structurally coherent)? | Open — requires an ensemble-level discriminator |

---

## 11. Next Steps

- Replace the agnostic \(\kappa_{bind}\) prior with a distribution derived from \(G_q, \lambda_\gamma, a_{disp}, R, N\).
- Inhomogeneous \(\kappa\) on a bond network with diffusion, so "regime" and "window" become spatial concepts.
- Derive a DET-native prior for \((\lambda_P, \kappa_{eq}, \beta, \kappa_{bind})\) from the existing κ-gravity / BAO / cluster constraints.
- Consider whether the "λ_P is the anthropic selection target" claim can be promoted from P to a pre-registered prediction under a stated multiverse sampling model.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md, docs/track_b/law_genesis.md (F10), docs/track_b/cosmic_record.md (F11).**
