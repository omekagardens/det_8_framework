# Reusing a visibly blank device in the finite mass test

Two preparations of the same device give exactly the accepted CL078 response on the first trial at every setting. After a silent first trial their second-trial responses differ. In the comparison below, a click occurring only on the second trial is possible with the fresh response and impossible with the other preparation. This changes both the finite probability of certification and the set of logs that reject the respective models.

## 1. Registered experiment and device

Condition throughout on the [CL078 finite mass test](finite_store_log_and_absolute_sector_masses.md), including its exact labelled spring record, its mass ray (1, r₁, r₂), the independently calibrated positive seed W and a fixed admissible world with baseline mass m. The same physical masses m(1, r₁, r₂) apply to the spring and the three store-arm sectors. Write α = r₁ − 1 > 0. The pretest candidate set is the CL078 set ℳ, with N = 1 for equal gaps or N = 10 or 11 for unequal gaps. Schedule the distinct wₖ = mₖc²α for mₖ ∈ ℳ in increasing order. Acquire both trials at *every* setting. Exactly one setting has wₖ = a, where a = mc²α is the true first gap. Infeasible pretest records have no candidate world. No distribution over m, seed sources or possible device preparations is introduced.

Each trial receives a new physical level-6 store and three newly prepared, ordered carriers. Write H = (h₁,h₂,h₃) with hᵢ = (zᵢ,bᵢ₁,bᵢ₂), zᵢ ∈ {E,F}, bᵢⱼ ∈ {0,1}. The native mass of a history and ordered terminal label string x, just before the probe, is

$$
Q(H)\rho^{\otimes 3}(x)
=\prod_{i=1}^3 (q_{z_i}/4)\rho(x_i),\qquad
(q_E,q_F)=(2/3,1/3),\quad \rho(A,B,C,D)=(5,4,4,1)/14 .
$$

All 512 registered histories have positive probability. The conditional probability of the single ordered BAA string is p = (4·5·5)/14³ = 25/686 for each H. Denote 1−p by u = 661/686. All native supplies are independent across the preset slots conditional on m and independent of the pair's initial controller. The probe follows the two births on every carrier. Write C for an observed true level 7 (click) and S for true level 6 (silence). The symbol C in an outcome pair denotes a click, separate from the carrier label C.

Use one controller with three equal-energy, equal-count internal states R, A₁ and D₁. R and A₁ both enable the command. D₁ inhibits it. The physical command at w is fixed for all trials and both preparations. Holding the controller state fixed, it applies the full transposition (BAA,6) ↔ (AAA,7) if enabled and w = a. Every other joint state is fixed. The inhibited or off-resonance command is the identity on the whole carrier/store space. This is the same ideal resonance-selective actuation premise as CL078 on the enabled branch. Its realization is supplied. Nothing estimates m or reads x to decide the command.

There is one fixed interval operation **between the two trials of a pair**. With the first terminal store present, it exchanges the controller states A₁ and D₁ if the physical level is 6, leaves R fixed, and acts as identity on every other level. The interval map fixes the store level and carriers. This is a controlled permutation on the whole state space. The fixed terminal registration always records the native histories and true store level. Before the next shot the visible display is blank in both arms and the first physical store is detached. An archive may keep the entry. The interval coupling is automatic, with the same wiring and timing for either observed level. No operator chooses a subsequent test from the data.

* **Preparation R** supplies the controller in R at the start of each pair. The same controller serves both trials. R survives either interval outcome and realizes the fresh response in both slots.
* **Preparation A₁** supplies that controller in A₁ at the start of each pair. It remains A₁ after C and enters D₁ after S. The same controller serves trial two with the resulting state.

The initial state for each setting is supplied independently of all preceding trials. Both preparations are fixed before the schedule and require no hidden-label access or selection of successful trials. The sole preparation difference is the initial internal state. Both states initially enable the same probe. The three-state controller, store and carrier supplies, blank presentation, probe command, interval operation and readout are identical across arms. Neither arm has a spare controller.

## 2. Conditional second response and complete law

Let L contain the **entire** accessible earlier log, including all earlier settings' records and the first history and level when conditioning trial two. Fix m, the setting wₖ and the complete present history H. Define tₖ = p·1{wₖ = a}. For every supported conditioning event, the first-trial click probability is tₖ in either arm. The second-trial click probabilities are

| First registered outcome | Preparation R | Preparation A₁ |
| --- | ---: | ---: |
| C | tₖ | tₖ |
| S | tₖ | 0 |

The corresponding silence probabilities are the complements. H has probability Q(H) conditional on L in either slot. Given L and H the current string still has law ρ⊗³, and the first registered level fixes the internal state in preparation A₁. This proves the table conditional on all the recorded native histories, including the second one. A preceding C off resonance, an earlier impossible pair, or an invalid history has zero mass in the relevant world and arm. A conditional prediction on such an event is undefined. Entries in the pair law below are unconditional given a supported pair start and may be zero.

The ordered probabilities in a pair, after taking out **only** Q(Hₖ₁)Q(Hₖ₂), are

| Ordered true levels | R, resonant | A₁, resonant | Either, off resonance |
| --- | ---: | ---: | ---: |
| CC (7,7) | p² | p² | 0 |
| CS (7,6) | pu | pu | 0 |
| SC (6,7) | up | 0 | 0 |
| SS (6,6) | u² | u | 1 |

In either resonant column the entries sum to one. For A₁ the first click has mass p, then an independent new BAA string clicks with probability p. A first silence has mass u, and even an eligible new string then stays at level 6. Its p and u second-string branches give u(p+u) = u. For R the second trial is enabled on every branch. For distinct settings use independent pair starts and fresh native inputs. With B the corresponding table entry, the probability of the complete ordered log in preparation j ∈ {R,A₁} is

$$
P_{m,j}(\mathcal L)=
\prod_{k=1}^{N} Q(H_{k1}) Q(H_{k2})
 B_{j,k}(Y_{k1},Y_{k2}),\qquad Y_{kn}\in\{C,S\}.
$$

The factors condition on the supplied pretest and schedule. At fixed native H and x, appending the indicator of the deterministic probe and interval outputs leaves the native input weight unchanged. If native paths are resolved more finely, multiply their original path weights by the same output indicator and sum over unobserved paths. A forbidden native path remains null. No survival conditioning or discarded silence enters this law.

## 3. Inverse, rejection and a complete matched log

Reject an infeasible pretest, any level outside {6,7}, a wrong setting, missing/extra slots, or an incomplete or malformed history under the registered full-log contract. Let G be the set of settings with at least one click in a well-formed record. The set returned below is the baseline mass set. Multiply each element by (1,r₁,r₂) for the labelled triplet.

| Full log pattern | Compatible m under R | Compatible m under A₁ |
| --- | --- | --- |
| All SS | ℳ | ℳ |
| One gain setting w, pair CC or CS there | {w/(c²α)} | {w/(c²α)} |
| One gain setting w, pair SC there | {w/(c²α)} | Empty |
| At least two distinct gain settings | Empty | Empty |

Each nonempty entry follows by strict positivity of the table entries for that pattern at every required setting. The silence of a different named setting has unit probability, even when some other possible exchange would resonate there. Under A₁ an SC pair rejects that device model in *every* mass world. Under R the same observation certifies a single mass when all other pairs are SS. If the preparation is unknown but known to belong to this two-arm set, compatibility is the union of the columns. The SC record then rules out A₁ and retains its R mass. On shared-support records the exact arm still matters to likelihood. An unknown mixing weight supplies no numerical arm-averaged certification rate.

For a specified full collection of histories let $Q_{*}=\prod_k Q(H_{k1})Q(H_{k2})$. The all-silent log has probability $Q_{*}u^2$ for R and $Q_{*}u$ for A₁ in **every** candidate world. Summing over histories gives u² and u respectively. For N > 1 unique certification has probability 1−u² = 33675/470596 under R and p = 25/686 under A₁. In each case this is also the chance of any click. For N = 1 the pretest has already certified the mass, so uniqueness has probability one in both arms and their respective click probabilities remain 1−u² and p. Rejection has probability zero when each arm is tested against its own model. With the R law generating and A₁ used to interpret, rejection has probability up = 16525/470596 from the otherwise valid SC pair at the true setting. With A₁ generating, R rejects with probability zero, although its assigned log probabilities differ. A supported silent sequence retains every pretest candidate.

For the CL078 unequal-gap fixture take the same ray (1,2,4), W = 3m₀c² with m₀ the generating baseline, U = W/3, and the ten previously registered increasing settings. U is resonant in this world. Set every individual history to (E,0,0) in all 20 trials. Their joint factor is 6⁻⁶⁰. Place an SC pair at U and SS at the other nine settings. The matched log has probability 6⁻⁶⁰up under R in this world, zero under R in the other nine worlds, and zero under A₁ in all ten. Replacing SC by SS yields the same history factor times u² or u in all ten worlds. These calculations use exactly the prescribed budget.

## 4. Resource ledger and sufficient reset decision

* Each arm uses 2N true level-6 store inputs, 6N carrier inputs and 12N carrier births. All 2N registered levels and all 6N marked two-birth histories are retained. Every store and triple leaves service after its slot, including a silent one. There are N independent prepared pair starts and N automatic interval operations. R can persist physically across settings. A₁ is supplied ready again at each new setting even if the previous pair left it inhibited. The common preparation facility may reinitialize the one module at pair boundaries. That readiness is a supplied resource.
* At w = a a forward click moves BAA to AAA, lowering carrier count 1→0 and resting energy by a. The store advances 6→7, gaining one count and w in energy under Eₛ = e₀+sw. Thus total count is seven at both endpoints and total energy is equal. The inverse endpoint is part of the same bijection although true initial level 6 gives it zero preparation mass. All unexchanged inputs leave both ledgers unchanged. The controller stays fixed during the probe. The interval permutation conserves its degenerate count and energy assignments and leaves the first terminal store intact.
* Distinct ready stores for the two slots prevent an earlier click from feeding a level-7 input into the next shot. The used store retains its final level, the used triple retains its probe output, and the controller may retain a consequence of the output. Both arms have equal access to the same materials, fixed operations and archive/display arrangement. No replacement controller is consumed between slots. Energy, work and time of initial preparation, restoring the next pair start, providing a fresh store, detached records, calibration and display blanking have no assigned cost model. The closed probe ledger supplies no cost bound on these ancillary operations.

A sufficient reset condition concerns the **conditional joint input to the response** at each actual slot. Fix m and the setting, and condition on every supported full earlier accessible log L. One sufficient preparation supplies the fresh history/current-label law Q(H)ρ⊗³(x), physical s = 6, and a controller implementing the registered fresh response on every jointly supported input. Correlation with an archive is harmless if this conditional response law still holds for every reachable L. Component marginals alone do not establish it.

More generally let μ be the actual conditional law of (H,x,s,d), including all other input degrees of freedom on which the actual registered transition depends in d. Include any apparatus randomness in d or in its transition kernel. Keep the stipulated true initial level and fixed native supplies. Pushing μ through the fixed transition and retaining the complete present H and level Y must give, for every supported L,

$$
P(H,C\mid L,m,w_k)=Q(H)t_k,\qquad
P(H,S\mid L,m,w_k)=Q(H)(1-t_k)
$$

with zero mass for any other output. In this controller class, on resonance, the click term is precisely the joint mass of H, x = BAA, s = 6 and an enabled controller. Thus dependence between controller, history and labels must be checked on the actual eligible inputs. Even under fresh marginals of H and x a correlation which inhibits just some eligible strings reduces the click mass. Disabled states occurring only on ineligible inputs do not change the registered transition there. Off resonance identity suffices. Equality of these pushforwards is the operational condition for the specified observation law on reachable inputs. It allows correlations invisible to the complete output at every such conditional step.

Multiplying the conditional factors for two successive slots gives Q(H₁)fₖ(Y₁)Q(H₂)fₖ(Y₂), where fₖ(C)=tₖ and fₖ(S)=1−tₖ. Repeating the chain rule over the fixed schedule gives the entire CL078 log law, including its impossible records. Starting from the same pretest, zero-probability branches cannot be reached by any prefix satisfying the condition. Conversely a difference at a supported prefix changes the joint law there. Preparation A₁ violates the click condition after a resonant first silence. For each second H the click mass drops from Q(H)p to zero. The display is blank on this branch and the second store and carriers are genuinely fresh.

CL065's signed canonical pair (Q,−P) was retained by the machine in its own recording experiment. It gives no dynamics to the controller here. An inaccessible archive may likewise keep its record so long as the conditional registered transition satisfies the stated law. CL078 already grants independent fresh responses. For a reused device, restoration of that joint conditional response on its actual support suffices to transfer the finite inference. The decision requires no additional reset operation or claim of minimum physical work.

## Scientific review

Classical supplied the reversible controller model and its complete observation laws. A distinct Classical reviewer checked the proof. DET Quantum Relativity assessed the conditions for applying it to the finite mass test. The coordinator accepted the conditional result on 9 November 2026 HST.

- Donor control SHA-256: `dee8a262e9fc3a69f275169462fdca56f2ac2cd216f15159f70375ceb47cecc5`.
- Author report SHA-256: `24df2a2fdde071cc9dd3e5ec2f2ae084ae95f7d7b4ff6ae262978edc23aa71f4`.
- Author freeze SHA-256: `36be99b2514541332cc68ce6ee1e27783d5c6639f49d3c1b2e8421b263d40675`.
- Independent scientific review SHA-256: `e6d09d2fbb74801fad860e89710e34f1fb80ff1a9835b39fcc72024cc64430ac`.
- Classical disposition SHA-256: `c08abaab768662c911c31cda7059ef47f4c70a7a3b568c165e6dd0752df0195e`.
- QR recipient assessment SHA-256: `5463639214199533c287de500a087c095282c759fc4ce31fac15024288bf130d`.
