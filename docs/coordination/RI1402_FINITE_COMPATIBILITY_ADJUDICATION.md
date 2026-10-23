# RI1402: Finite compatibility, qualified admission, and remaining evidence gaps

This documentation checkpoint records root-adjudicated conditional results from RI1401, E-C011, NE-C011, CE-T003, and the selected-image/cache relation design. The current author reports and distinct reviews support the details below; root dispositions determine their admitted scope. This is a mathematical and documentary checkpoint. No experiment, scientific source execution, native calculation, controller run, fixture, measured digest workload, or benchmark result is reported. Compatibility, statistical soundness, operational admission, and physical validation remain separate claims.

| Track | Admitted result | What remains unavailable |
|---|---|---|
| QR | Exact four-query compatibility, constructive witnesses, a simultaneous-confidence rejection bound, and a finite-budget boundary-power obstruction | Physical true-predicate access, independently validated shared response, arbitrary-law identification, and a native discriminator |
| E | Full-service horizon conditions, explicit zero-horizon handling, and equality of a deterministic commanded-action receipt under complete equal inputs | A common continuous-time enclosure and sufficient feasibility or continuation certificate, complete fallback map, source-to-reset joules, and baseline competence |
| NE | A 32-block candidate-blind calibration rule with uniform model-indexed unconditional false-admission control | Trusted actual reference operation, calibration-to-target transfer, source and exact-U premises, and a complete identification protocol |
| CE | Manual finite graph/frame accounting for two frozen conventional examples and a complete-cost crossover condition | Executed correctness, timing, peak-memory or energy results; a strict runner boundary; a distinct DET mechanism |
| Measurement | Conditional composition of seven identity predicates and an interval-hole countermodel | An applicable versioned selected-image/current-cache membership and safe-composition contract, actual same-invocation binding, and execution admission |

## 1. QR: the exact four-query compatibility region

Fix the reported-positive population probabilities

\[
(u,v,w,z)=(q_{C1},q_{C2},q_{A2},q_{C3})\in[0,1]^4.
\]

The declared family has a Borel probability measure \(\mu\) on \([0,1]\) with \(\mu((0,1))>0\), true chain probabilities \(C_n=\int\theta^{n-1}\,d\mu\), and the complementary size-two predicate \(A2\). Write \(p=\int\theta\,d\mu\) and \(r=\int\theta^2\,d\mu\). One stable memoryless response, shared across all four *true-predicate* queries, has false-positive probability \(f\), true-positive probability \(t\), and slope \(s=t-f>0\), with \(0\le f<t\le1\). It gives

\[
u=t,\qquad v=f+sp,\qquad w=f+s(1-p),\qquad z=f+sr.
\]

The same source population, known sizes and query labels, fresh independent latent preparations, and independent response draws are explicit observation premises. Flipping a noisy reported C2 bit does not implement the true A2 query. These premises are assumed for this proposition, not established by fitting its four means.

From a proposed tuple define

\[
f=v+w-u,\quad t=u,\quad s=2u-v-w,\quad x=u-w,\quad y=z-f.
\]

Exact compatibility holds **if and only if**

\[
0\le f<t\le1,\qquad 0<p=x/s<1,\qquad p^2\le r=y/s<p.
\]

Equivalently, the set \(K\) consists exactly of tuples in \([0,1]^4\) satisfying

\[
0\le v+w-u<u\le1,\quad 0<x<s,\quad x^2\le sy,\quad y<x.
\]

The strict upper inequality is essential. In particular the fourth coordinate must obey \(f+(u-w)^2/s\le z<v\). The anchors fix the response and first moment; response parameters cannot absorb an arbitrary fourth coordinate.

Necessity follows from variance, \(r-p^2\ge0\), and
\(p-r=\int\theta(1-\theta)\,d\mu>0\). For sufficiency set

\[
a=r/p,\quad \lambda=p^2/r,\quad
\mu=(1-\lambda)\delta_0+\lambda\delta_a.
\]

Then \(p\le a<1\), \(0<\lambda\le1\), and the positive mass at \(a\) lies in the interior. Its moments are \(\lambda a=p\) and \(\lambda a^2=r\); the recovered response reproduces all four coordinates. At \(r=p^2\), zero variance gives the unique admitted law \(\delta_p\). At \(r=p\), the only law with mean \(p\) is \((1-p)\delta_0+p\delta_1\), which has no interior mass and is excluded. Means zero and one also force excluded endpoint point masses. Response endpoints \(f=0\) or \(t=1\) are allowed if the slope is positive; exact zero slope is excluded. Thus \(K\) is not closed.

For example, \(f=1/4,t=3/4,p=1/2\) fixes \((u,v,w)=(3/4,1/2,1/2)\) and allows exactly \(3/8\le z<1/2\). At \(z=5/12\), both the uniform law on \([0,1]\) and \((1/4)\delta_0+(3/4)\delta_{2/3}\) fit. At \(z=1/3\), the implied \(r=1/6\) violates \(p^2=1/4\). Joint falsifiable restrictions survive unknown response, but a compatible catalogue does not identify an arbitrary mixing law or validate response transfer.

### A confidence-box rejection rule without a slope floor

Before data, fix \(0<\alpha<1\), four positive integer counts \(n_j\), the four query labels, and this null \(K\). For observed Bernoulli fractions \(\widehat q_j\), let

\[
h_j=\sqrt{\frac{\log(8/\alpha)}{2n_j}},\qquad
B=\prod_{j=1}^4([\widehat q_j-h_j,\widehat q_j+h_j]\cap[0,1]).
\]

The ideal rule rejects exactly when \(B\cap K=\varnothing\), retaining all strict inequalities. Each two-sided Bernoulli mean exclusion probability is at most \(\alpha/4\), so a four-coordinate union bound gives \(\Pr_q(q\notin B)\le\alpha\). For \(q\in K\), containment \(q\in B\) itself witnesses a nonempty intersection. Hence

\[
\sup_{q\in K}\Pr_q(\mathrm{reject})\le\alpha.
\]

This argument uses no independence among transformed anchor estimates and no positive slope lower bound beyond \(s>0\). A separately justified true floor \(s\ge s_*>0\) would define a narrower null; an unproved numerical floor cannot be used to reject small-slope members of the original null. The direct inequalities avoid dividing by an estimated slope.

Positive valid counts make the box nonempty, but its anchor-feasible slice may be empty, which can legitimately certify rejection. Missing batches, invalid records, zero counts, or failure of a plug-in anchor estimate do not certify this. No feasibility implementation has been supplied. Actual rejection needs a sound exact emptiness certificate; numerical uncertainty must be inconclusive. Nonrejection means only that the rule has not rejected. The unconditional rejection bound survives sound abstention, but \(\Pr(\mathrm{reject\ or\ abstain})\le\min(1,\alpha+\Pr(\mathrm{abstain}))\) gives no completion or selected-report guarantee. Optional stopping, repeated peeking, and a data-selected catalogue are outside the stated experiment.

### Strict population exclusion does not guarantee boundary power

For fixed \(0<p<1\), take the excluded endpoint law \(\mu_0=(1-p)\delta_0+p\delta_1\) and admitted laws
\(\mu_\varepsilon=(1-\varepsilon)\mu_0+\varepsilon\delta_p\), \(0<\varepsilon<1\). Their means agree and \(r_\varepsilon=p-\varepsilon p(1-p)\). At the same response the anchors are identical and only C3 changes, by \(s\varepsilon p(1-p)\). Coupling corresponding Bernoulli trials bounds full-data total variation by \(n_4s\varepsilon p(1-p)\). Any test uniformly level \(\alpha\) on \(K\) therefore has endpoint-law rejection probability at most \(\alpha+n_4s\varepsilon p(1-p)\); letting \(\varepsilon\downarrow0\) gives power at most \(\alpha\) at this excluded boundary for every fixed finite budget. This does not erase violations such as the below-variance example. It separates population compatibility, finite rejection, and detectable separation. Rejection addresses the conjunction of law, population, response, and readout assumptions; it does not locate which premise failed.

## 2. E: full service, zero horizon, and the scope of equal receipts

The unchanged task requires both zones to enter their ±0.5 K target bands by deadline \(D\), then remain continuously in both for dwell \(W\). Overshoot above target+1 K and safety or telemetry failure are failures throughout the attempt, including before entry. A mandatory terminal reset and storage qualification follow service. In the synthetic declaration, \(\Delta t=60\) s, \(D/\Delta t=60\), and \(W/\Delta t=20\): the latest completion is 80 intervals, beyond the initial 64-step solve cap. These are synthetic design quantities, not calibrated apparatus observations.

At a valid tick, first update the common service automaton from independent observation. With positive remaining time to \(D+W\), use the common horizon \(h_n=\min(64,N_{\mathrm{latest}}(n))\), where remaining-interval rounding and clock conventions must be frozen before implementation. This is a bounded window, not evidence of service completion. A candidate needs one of two routes:

1. **Full coverage.** For every admitted uncertainty trajectory, qualifying entry occurs by \(D\), and the whole continuous dwell interval lies inside the current window, with global safety and no-overshoot constraints retained. Previously elapsed dwell counts only if independently established as uninterrupted; the remaining dwell must have no gap. A calibrated, independently reviewed continuous-time intersample enclosure is required. Sixty-second Euler samples alone cannot provide it.
2. **Certified continuation.** The terminal uncertainty state belongs to a common versioned viability set, with an independently certified causal continuation policy or recursively enforced invariant covering all remaining continuous service obligations, unchanged actuator bounds, and an enforcement rule for later replans, each still capped at 64 steps. This certificate is absent. A restoration cost or an unspecified future command is not a substitute.

Initially, full coverage with a 20-step dwell requires entry by step 44. The service deadline remains 60; 44 describes conservative planning eligibility. No proof establishes that this common subset is nonempty or sufficiently competent for a comparison. If neither route is established, the controller produces HORIZON_COVERAGE_HOLD and no fresh MPC command. Before requests this is protocol/model HOLD; after a request opens the common fallback/abort is a charged failure. It does not prove physical infeasibility or an advantage for one arm.

The logical witness is entry at step 50: by step 64 only 14 of 20 dwell intervals have passed. One continuation remains in band through 70; another leaves at 65. Equal prefixes and equal restoration-cost symbols cannot decide completion. This is a non-entailment example, not a simulated or physically reachable plant trace. Equal samples can also conceal intersample excursions.

For \(h=0\), independently established complete dwell with no failure leads to no new attempt command and mandatory reset. Success credit still waits for the common two-sample physical reset/storage qualification. Without established complete dwell, an empty horizon is failure, not a feasible command or success. A missed entry deadline differs from a valid dwell continuing past \(D\). The previously permitted first-attempt retry does not admit additional attempts or favorable retrospective anchors.

The repaired equality lemma concerns complete canonical valid bundle and service state, identical common controller version and arithmetic, and the same nonempty completed finite candidate set with identical finite objective/constraint records. Those premises give the same feasibility set, fixed-reference \(J_{\mathrm{ref}}\) eligibility and total-order minimum, hence the same selected sequence, first **commanded** action, and deterministic SemanticReceipt projection. This does not show that a real solver supplies identical candidates or that a continuous optimum is attained. Nonfinite/incomplete output and observed deadline failure retain their failure rules.

ObservedReceipt separately includes measured latency and clocks, actual application and acknowledgment, realized powers/link, safety telemetry, and source/reset costs. Equal mathematical inputs do not imply equality of those observations, joules, physical service, or future trajectories. Both eventual receipts and all costs remain required.

Fallback equality needs equal complete causal input: error class, qualified measured state and uncertainty, last applied powers/link, service/dwell mode, attempt/retry/reset/safety state, current clock/deadline, fallback version and permissions, and any further memory or observations used. A frozen deterministic map then gives equal commanded fallback output. That map is not supplied. Two SOLVER_TIMEOUT labels with last link states zero and one can lead to different commands under a hypothetical hold-last-link map; the label alone proves only equal error classification, and this example does not propose a safe real fallback.

Arm 2 retains its latest 32 raw packets including reset packets, persistent arrival prior/covariance, and typed 8×6 innovation injection. Arm 3 retains its completed-interval update and first-valid/no-anchor/retry refusal rules. Equal observations, actuators, tuning resources, safety, and latency remain mandatory; symmetric restriction alone does not establish baseline competence. Missing uncertainty is not zero.

The full source-to-reset endpoint remains \(J_a(H)=[\mathbb E(E_{\mathrm{source},a,\mathrm{request}})+K_a/H]/\Pr(Y_a=1)\), infinite at zero success, with comparison \(R=J_3/J_2\). All preparation, failures, aborts, retries, resets, support/compute and setup costs count without duplicated source branches or storage credit. Link/chamber/support W/J, physical reset and latent regeneration, restoration valuation, fallback actuation, and adequate uncertainty are missing. Internal heat transfer is not added energy. The useful-gain threshold \(R<0.90\), proposed alternative \(R=0.85\), quality/time/reliability criteria, competent baseline, evaluator-owned iid I×A×G held-out groups and zero-link/capacity controls remain unmeasured and independently gated. No energetic advantage follows.

## 3. NE: one actual calibration experiment, uniform over two possible laws

The unknown generator index \(j\in\{0,1\}\) names alternative worlds, not an operator-selectable command. Retain four cell labels \(\beta\in\{00,01,10,11\}\), settings \(c\in\{1,3/2\}\), complete cell/sign outcomes, fixed ideal effects \(Q^*_\beta\), exact structural \(U\), and independently justified shared response and increment assumptions.

One common trusted operation must supply terminal-readout-plane references \(\rho_0=I/2\) and \(\rho_d=(I+r\sigma_d)/2\), \(d=X,Y,Z\), with known \(q>0\), \(0<r\le1\), and a held-fixed justified frame. Under world \(j\), its unconditioned cell-plus probability is \(p_{\beta,j,c,i}=q\operatorname{Tr}(\rho_iQ_{\beta,j,c})\). If probes enter before \(U\), an independently justified exact transformation or correctly indexed Heisenberg effect is necessary; unevolved references cannot simply be substituted. One unchanged effect across a context's four probe blocks, complete outcomes, no hidden loss/selection, and calibration-to-target validity under each model are assumptions. Target H0/H1 outcomes or signed target statistics cannot define or fit this reference map.

One apparatus supplies four cells × two settings × four probes = **32 actual labelled blocks**. It does not supply 64 observed blocks for two counterfactual devices. With \(n\) iid trials within each block, set

\[
C(q,r)=\frac{1+2\sqrt3/r}{q},\quad \epsilon=m/C(q,r),\quad
n=\left\lceil\frac{8C(q,r)^2}{\delta_{\mathrm{cal}}m^2}\right\rceil,
\]

for predeclared \(m>0\) and \(0<\delta_{\mathrm{cal}}<1\). Bernoulli variance at most \(1/4\), squared Markov, and the 32-block union bound give
\(\Pr_j(E_j^c)\le8/(n\epsilon^2)\le\delta_{\mathrm{cal}}\), where \(E_j\) is simultaneous probability error at most \(\epsilon\). Cross-block independence is unnecessary. The symbolic count charges 32n reference preparations and 32n complete readouts; registration, reset, and source creation are additional. These are operation counts, not time or energy.

For \(Q=A I+B\cdot\sigma\), the inverse is \(A=p_0/q\), \(B_d=(p_d-p_0)/(qr)\). On \(E_j\), coefficient errors imply
\(\|\widehat Q-Q_{\beta,j,c}\|_\infty\le\epsilon/q+2\sqrt3\epsilon/(qr)=m\).
For each of eight cell/setting contexts, require a nonempty physical feasibility set of effects \(0\le Q\le I\) whose four probabilities lie within \(\epsilon\) of the observations, and

\[
\|\widehat Q_{\beta,c}-Q^*_\beta\|_\infty+m\le\eta_*.
\]

Use this same candidate-blind acceptance rule \(A(D)\) once on the actual data. The linear estimate need not itself be a physical effect. Unavailable contexts, empty feasibility, failed norm bounds or unjustified operational premises require abstention/HOLD. On \(A\cap E_j\), triangle inequality bounds every actual effect by \(\eta_*\). Therefore, with \(\mathrm{Bad}_j\) denoting violation of that actual-world bound,

\[
\sup_{j\in\{0,1\}}\Pr_j(A(D)\ \mathrm{and}\ \mathrm{Bad}_j)\le\delta_{\mathrm{cal}}.
\]

There is no factor of two for mutually exclusive worlds. This is unconditional false-admission control, not \(\Pr_j(\mathrm{Bad}_j\mid A)\), a promise of acceptance, or a deterministic simultaneous certificate of both devices. Changing a counterfactual effect can leave all observed actual-world records unchanged.

The inherited separation theorem remains conditional on *both mathematical candidate classes*. For the fixed H0=0 versus H1=(π/2)Z catalogue, with one shared response multiplier in \([1,3]\), commands 1 and 3/2, and increment errors bounded by \(1/(24\pi)\), the ideal sum of two labelled conditional-row total variations is at least \(3/320\). With exact same structural \(U\), positive source blocks of total trace one, complete complementary two-sign effects and preserved cell labels, source trace error \(\eta_P\) plus effect operator error \(\eta_Q\) gives row-TV error at most \(e=\eta_P+\eta_Q\). Thus separation is at least \(3/320-4e\), and the predeclared signed mean gap is at least \(3/160-8e\); \(e<3/1280\) is sufficient. These are sums across labelled settings, not the TV of an unspecified pooled record. For independently declared equal setting weights with labels retained, the labelled joint TV is half the sum.

Actual-context calibration alone is not a completed identification procedure or a replacement for that two-class premise. Independent source error, exact \(U\), response support, sampling, calibration-to-target transfer, drift/loss accounting, and a predeclared target decision with its own selection/error proof remain needed. No source or effect budget may be fitted from the target distinction. No physical clock, action, energy/work-store scale, observed identification, or universal generator law is established.

## 4. CE: finite manual cost counts and the runner HOLD

Only the frozen conventional F0/F1/I0/I1 menus and correctness-only CEC1 V02/V12 are considered. A node hash receives \(13+|P_x|+36\,\mathrm{indegree}(x)\) framed bytes and returns 32 key bytes; for these one-byte payloads the frame is \(14+36\,\mathrm{indegree}(x)\). Each successful initial/edit output is 513 bytes. No workload SHA-256 output was calculated and no digest inequality is assumed.

All menus charge full-graph validation and a full reverse target-ancestry walk on real accepted changes. F0 builds fresh Kahn min-ID order and recomputes all required keys. F1 may reuse a validated order after payload changes, but rebuilds after edge changes and never reuses intermediate keys across real changes. I0 uses strict off-cone eviction and a changed-key worklist. I1 first charges structural affected counting, including entering nodes, then falls back to full cone recomputation exactly when twice the affected count is at least the new cone size. Counting is not a digest-change oracle. No stronger F shortcut is substituted.

For sparse V02, \(n=128\), initial target ancestry has 128 nodes and 127 edges. The fixed edits are D(97,113), P(97,0xAB), I(97,113). Cold hashing is 128 calls over 6,364 framed bytes per actor, before non-hash cold costs.

| V02 edit | F0/F1 warm hashes / framed bytes | I0/I1 warm hashes / framed bytes | Required qualification |
|---|---:|---:|---|
| Delete 97→113 | 121 / 5,978 | 1 / 14 | Seven internal nodes leave; the required cone has 119 edges; destination 113 remains required |
| Change off-cone payload 97 | 121 / 5,978 | 0 / 0 | Raw state must still commit; no off-cone key is retained; ancestry, validation and output remain charged |
| Reinsert 97→113 | 128 / 6,364 | 8 / 400 | Seven evicted keys rebuild from current raw state, then destination; all eight frames have one predecessor |
| Three-edit total | **370 / 18,320** | **9 / 414** | Difference: 361 calls and 17,906 framed bytes, not elapsed time |

I1 counts 1, 0 and 8, so it does not fall back in V02. Initial plus three accepted outputs total 2,052 bytes per actor. The two edge frames are nine bytes each and the payload frame eight; their processing is charged. Common cold hash counts do not imply equal complete cold cost.

Dense V12 has 128 nodes and 1,552 edges; P(0,0xAB) is a real payload change. Cold and each F full evaluation use 128 hashes over 57,664 bytes. I0's all-reached-keys-change maximum is 113 hashes over 57,454 bytes: seed zero, 96 later internal nodes, and 16 targets. Its actual work can be lower if key equality stops propagation; no observed count is asserted. I1's structural affected count is 113, so it must fall back to 128 full hashes over 57,664 bytes regardless of digest equality, after counting. A standard deduplicated forward traversal scans 1,312 outgoing edges; other representations must report their actual counting cost. No extra pre-fallback seed hash is implied. The two outputs total 1,026 bytes per actor.

For a finite edit horizon \(q\), let \(C_X\) include every cold admission/index/order/hash/allocation/output cost, \(N_{X,j}\) every non-hash edit cost, and \(H_{X,j}\) actual hash cost. A particular I configuration beats a particular F configuration only if

\[
C_I-C_F+\sum_{j=1}^q(N_{I,j}-N_{F,j})
<\sum_{j=1}^q(H_{F,j}-H_{I,j}).
\]

This is the rearranged complete-cost comparison, not a measured inequality or a linear hash-price model. Validation/cycle searches, ancestry/order, counting, queue/scans/comparisons, eviction, staging/rollback/commit, output custody and cleanup all count. Framing construction/copy/allocation must appear consistently in N or H without omission or double counting. V02's opportunity can be outweighed by overhead over its three edits. V12 gives I1 no warm hash savings and adds discovery/count cost. Neither example establishes an end-to-end ordering or licenses extrapolation to the separate 64-edit CED1 workload.

I retains 4,096 published key bytes at 128 nodes or 3,872 at 121, plus indexes, cone/rank/queue structures, raw payloads, staged old/new state, framing and input/output buffers. F's 512 retained target-key bytes are not its peak: live intermediate keys, ordering and staging structures and buffers count; recomputation to reduce retention costs work. No universal F peak lower bound, RSS, elapsed latency or energy is reported.

The strict CE-R001 runner HOLD persists. The required pre-import instantaneous resident-memory ceiling and trusted controller/failure-receipt boundary are unsupported. Virtual-address limits, periodic RSS sampling and completed peak readings do not establish that exact ceiling. Wall, output, process, installed-identity and failure-custody obligations remain separate. The prospective 30-minute/one-CPU/1-GiB benchmark is ungranted; the smaller source-check contract is not an execution loophole. A later separately admitted run would need frozen implementations, independent complete-output correctness, all cold/non-hash/peak costs and adverse cases. The proposed 0.85 endpoint and adverse-family 1.20 guard are unmeasured; joules require their own approved meter and boundary. No distinct DET mechanism or practical efficiency claim follows.

## 5. Measurement: seven predicates and the missing relation

For one admitted invocation and coherent observation/use epoch \(E\), let \(a_r\) be the address actually used for required role \(r\), \(H_r\) its mapped image, \(I_r\) that image's UUID, and \(C_E\) the cache actually serving it. Manifest is the independently reviewed immutable reference, including applicability. These are mathematical variables, not acquired addresses or inferred API signatures.

One sufficient route requires all seven predicates:

1. The invocation, architecture/translation, OS/kernel, module and call roles match Manifest, and every used declaration is applicable to that exact target.
2. A reviewed selected-target protocol connects \(a_r\) to the implementation actually called, including relevant wrapper, FFI, native and indirect associations; an unused same-named symbol is insufficient.
3. An applicable address-to-image contract connects that address to the actual containing mapped image \(H_r\) at \(E\), with the return/pointer/bounds semantics needed for use.
4. A safe bounded applicable operation obtains \(I_r\) from that same image; absent or malformed identity fails, and success does not retroactively validate an unsafe input pointer.
5. For a cache-provided role, an authoritative relation \(M_E(H_r,I_r,C_E)\) binds that mapped image and UUID to the actual invocation's cache, using the exact main-cache/subcache identity convention.
6. All associations are coherent in the same mapping state and remain valid through use; mapping lifetime, unload/rebinding and pointer safety need adequate explicit contracts.
7. Exact Manifest matching covers every required role and relevant mapping with complete deduplication. Expected non-cache roles need their reviewed actual/static-image relation; missing cache identity is not automatic non-cache success.

Composition then connects the actual call to the mapped image, its UUID and cache at a coherent epoch, and finally to the reference identities under their applicability scope. UNKNOWN is not true. This is a conditional sufficient relation, not a proof that each predicate is necessary for every alternative design, an implemented mechanism, source/binary equivalence, metric truth, or physical prediction. Existing metric/ABI/Python residual hypotheses keep their admitted scope and do not waive actual same-invocation B1 admission.

The outer-interval countermodel uses cache coverage \([1000,1200)\cup[1800,2000)\) and outer extent \([1000,2000)\). A non-cache target at 1500 passes the extent test but lies in the hole. Even actual cache coverage would not attach a separately obtained header or UUID to that target. This is an abstract countermodel, not an observed system layout. A path-membership query, category flag or independent image/cache UUID endpoints also require correspondence premises. Thread-safe lookup is not a mapping-lifetime guarantee, same process is not atomicity, and before/after identity agreement does not exclude an ABA change-and-return history.

The actual blocker is an applicable **versioned selected-image/current-cache membership and safe-composition contract**. The retained mutable private-header location and historical availability do not establish immutable original source identity, installed applicability, supported public-SDK status, valid initialized input, readable bounds, malformed-input behavior, canonicalization, ownership/lifetime or safe coherent composition. No additional declaration, native prototype, installed header or acquisition is inferred. A future bounded exact authoritative input or independently reviewed alternative must close this route-specific gap.

Static anchors plus a complete independently reviewed binding mechanism may precede conditional source approval; actual same-invocation B1 must still pass before the first contrast. This packet is not that mechanism. Unsupported target/API, missing membership, unsafe/unknown pointer or lifetime, malformed identity, mismatch, extra relevant mapping, deadline or record overflow must fail before contrast, retaining bounded failure/cleanup evidence. There is no path/flag/interval fallback or alternate-interpreter retry.

Preserve selected roles, conditional R1 caller obligations including a valid initialized borrowed own-task right, source/build/compiler and qualification gates, at most 16 unique controller images and four per helper, one controller with two serial helpers and no descendants, 15 seconds per child and 30 seconds aggregate setup through close, and 128 total records with 512-byte ceilings and reserved failure/cleanup capacity. No unbounded identity preamble or extra identity process is admitted. No acquisition, source integration, compile, native call, test or observed calculation follows.

## 6. Evidence status, process limits, and unchanged gates

Root has accepted the conditional content at the scopes above while retaining process defects and uncertainty. The current administrative audit records 459 passing conditions for the eight current QR/E/NE/CE author/review packages: 51 declared members, 104 direct source-pin occurrences and 95 consumed files. It verifies current identity and direct joins only. It neither includes a new measurement scientific review nor repairs historical custody, proves scientific truth, reconstructs ownership history, or authorizes execution. The present preparation uses only its separately pinned inputs and does not repeat or expand that audit.

| Record | Retained limitation |
|---|---|
| RI1401 | Freeze is recorded 12 seconds after its declared deadline. Acceptance of mathematics does not retroactively extend that deadline or certify compliance. Older missing RI1389 author artifacts remain missing. |
| E-C011 and distinct review | Bounded-read/truncation and attributed failed-receipt limitations remain. The review's 57 administrative checks are not scientific tests. A one-second reported reset variation is retained without inferring a reset or permission. |
| NE-C011 | The first guard lacks an exact timestamp; the 322-second interval begins at the first retained clock, not at task start, and cannot certify six-active-minute compliance. Failed patch/truncated-clock history remains attributed where raw receipts are absent. The earlier NE-C010 initial raw-guard gap remains. |
| CE-T003 | Initial preflight is transcribed; no freeze timestamp or complete active-time ledger certifies the author limit. Earlier CE-T001/CE-T002 guard, reset and custody gaps remain. |
| Measurement relation design | A 7 minute 17 second elapsed interval lacks a separate active-time ledger. Six-active-minute compliance is not certified; neither invented idle deductions nor a measured active overrun is asserted. The distinct review's 67 administrative conditions do not cure this. |

Source authorship and independent review remain distinct. This report is editorial preparation of root-adjudicated content, not another independent scientific review. Exact publication review and root release authority remain separate. Current clear capacity, matching hashes and later reviews cannot retroactively repair timing, guard or original-custody gaps.

All source/reservation, experiment, protected-validation, safety, custody, resource and RET-only pause gates remain in force, including the supported account/window/reset capacity guard and stop at or below 10% remaining. Null/unavailable windows are not spare capacity. No reset, credit, account, schedule, scope or exception workaround is introduced. Source-level acceptance does not grant import, execution, calibration, apparatus use, validation or benchmarking. Missing evidence is HOLD, never a zero cost or favorable result.

The next questions may address a native discrimination premise, a common intersample certificate, calibration/target decision composition, or a concrete strict runner enforcer. They are questions only. RI1403, E-C012, NE-C012 and CE-R002 findings are outside this checkpoint. No universal DET law, physical prediction, empirical distinction, energy advantage, or executed benchmark is established here.
