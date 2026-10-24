# RI1464: Bayesian hiding can break precursor locality

Accepted RI1463 gives a conditional six-birth counterexample. Two admitted components have positive complete histories and invertible probability-preserving history transport. Hiding their fixed selector leaves a positive, normalized, covariant marked law with complete scalar diamonds, yet its sixth-birth empty-slot probability depends on a forbidden root mark. The marginal therefore fails one original admission axiom.

This concerns finite record dependence, not spacetime nonlocality, a physical selector or a seventh-birth law.

## 1. Model and conditional source premises

Write C=(P,r) for a finite natural order and immutable vertex bits; natural labels put predecessors first. An actual ideal S is downward-closed, including empty/full. A birth appends a maximal vertex above exactly S, preserving old relations/marks, with independent fair newborn bit b.

An admitted component has strictly positive probabilities q(P,r,S) for every ideal, summing to one. For a proper S, q may read the whole unmarked parent P but only the selected marks r|S. A full slot may read all marks. In particular, at fixed P the empty-slot probability must be independent of every old mark.

Assume complete-state Markov dependence, transported marked equivariance and every contained incomparable-birth diamond. On a fixed common carrier the whole branch map is q(P,r,S)D/2 for arbitrary complex positive-semidefinite D. Diamonds equate complete unnormalized maps, including both newborn bits, equal precursors and all old marks. These model premises do not follow from DET ontology; bookkeeping births are not physical time.

The supplied primary excerpts provide these definitions (original lines 64–104), admit the coefficient/prefix data (line 141), identify c=q(C4,C4) (189–190), and give the root-bit values (312–337)

    c_0 = 81/1100 = 3240/44000,
    c_1 = 3231/44000.

C4 is the four-chain; i labels its initial root bit, not the selector. The held rows are root-only by admitted all-mark proofs, which do not make every lower/disconnected row root-only.

The extension excerpt (760–764) assumes the ratio-potential theorem: consistent sufficiently small component scales and full complements positively extend an admitted prefix. We use one further layer without reconstructing the theorem or numerical table. The original-file identity is attribution; only five retained excerpt bodies were inspected.

The prior last-layer transformation L1 is proved in [Law Dependence, historical §2](../track_b/native_theorem_package_v1/LAW_DEPENDENCE.md). At a fixed final parent size, a common 0<t<=1 multiplies every proper probability by t and replaces full a by 1-t+ta. Later rows must be rebuilt. General record sufficiency and complete-fiber augmentation descent are prior results, not new claims of this example.

## 2. Components through five births, then a rebuilt sixth layer

Fix [RI1462](RI1462_HIDDEN_LAW_MIXTURE.md)'s admitted baseline q through parent four. Choose immutable uncommitted z in {0,1}, initially half/half and independent of fair mark draws. Both components use the same arbitrary passive D. The selector is neither agency nor a preselected outcome.

Set t_0=1 and t_1=1/2. The two five-birth prefixes are

    q_z(C,S) = q(C,S),                         |P|<4,
    q_z(C,S) = t_z q(C,S),                     |P|=4, S proper,
    q_z(C,P) = 1-t_z+t_z q(C,P),                |P|=4.

L1 admits both prefixes, with marked probabilities q_z/2. Under the extension premise, fix positive admitted extensions e_z through parent five, preserving earlier rows. These are fixed component laws, not additional hidden draws or unchanged old continuation coefficients.

Let C5 denote the unmarked five-chain. Proper locality makes

    v_z = e_z(C5,r,empty) > 0

independent of every marking r. Define fixed constants

    d = min(v_0,v_1)/2,
    s_0 = d/v_0,             s_1 = d/(2v_1).

Thus d>0, 0<s_0<=1/2 and 0<s_1<=1/4. Each s_z is a fixed constant across the entire parent-five layer: every parent, marking and proper ideal. Choosing it from one chain slot is not empirical calibration or parent-specific adjustment.

Apply L1 again:

    k_z(C,S) = e_z(C,S),                       |P|<5,
    k_z(C,S) = s_z e_z(C,S),                   |P|=5, S proper,
    k_z(C,P) = 1-s_z+s_z e_z(C,P),              |P|=5.

Consequently k_0(C5,r,empty)=d and k_1(C5,r,empty)=d/2 for every r. The quantities e_z, v_z and d are existence-based choices, not tabulated numerical predictions. No parent-six transition is defined.

## 3. Positivity, complete histories and every contained diamond

For a changed row with a=e_z(C,P), the proper mass s_z(1-a) plus full mass 1-s_z+s_z a is one. All entries stay positive; on a nonempty parent each is below one because another ideal has positive mass. At the empty parent the sole ideal has probability one, and the two marked branches each have probability 1/2.

Constant scaling preserves proper locality and equivariance. Full complements retain their permitted mark dependence. The maps k_z(C,S)D/2 preserve positivity, and their complete sum over ideals and bits is identity on the fixed passive payload.

A diamond contained in six births has a base of size at most four. Below four both factors are unchanged from e_z. At a marked base A of size four, take ideals S,T of A and arbitrary old/newborn marks. Each second precursor excludes the other newborn, so it is proper in its five-vertex parent. Both routes acquire one s_z:

    e_z(A,r,S) s_z e_z(A+x_S,r+b,T)
      = e_z(A,r,T) s_z e_z(A+y_T,r+c,S).

The unscaled equality comes from the admitted extension. Either first precursor may be full, and S=T is included. Both routes multiply the same transported D by their product/4 for every D. No base-five diamond is claimed. This proves admission of each six-birth component; it does not splice old continuation rows onto changed prefixes.

For n<=6, include every ideal, both newborn bits and both selector atoms, and assign each complete history

    rho_n(z,h) = (1/2) product_(j=1..n) [k_z(C_(j-1),S_j)/2].

Each parent's children sum to its mass; induction proves positive normalized histories and truncation consistency. Preserved relations/marks make record projection commute with truncation. Only z and birth branches are random.

## 4. Posterior and exact root-bit contrast

Let C5_i be the natural five-chain with root i and all other marks fixed alike. Full births form it positively in both components, so both records and both selector states above each are reachable.

For each i, the common four-birth likelihood cancels across z; it need not agree across i. Fifth full probabilities are c_i and (1+c_i)/2, and the fixed fair mark cancels. Hence

    p_i = P(z=0 | C5_i) = 2c_i/(1+3c_i),
    P(z=1 | C5_i) = (1+c_i)/(1+3c_i),
    p_0 = 162/1343,          p_1 = 6462/53693.

The parent-five transformation changes none of these earlier probabilities. In particular, the posterior at the sixth step is not generally half/half.

Under the same sixth-commit protocol, test whether its actual precursor is empty and sum over the new bit. The component values d and d/2 give

    Q_i = P(S_6=empty | C5_i)
        = p_i d + (1-p_i)d/2
        = d(1+5c_i) / [2(1+3c_i)].

Direct cancellation yields

    Q_1-Q_0 = d(c_1-c_0) / [(1+3c_1)(1+3c_0)]
            = -9d / [44000(1+3c_1)(1+3c_0)]
            = -9900d / (1343*53693) < 0.

Equivalently the numerator of p_1-p_0 is
6462*1343-162*53693=-19800, and Q_1-Q_0=d(p_1-p_0)/2.
For a specified sixth newborn bit, the contrast is halved again and remains nonzero.

The same unmarked parent and empty selected record have different probabilities when only the unselected root bit changes. This violates proper-record locality despite whole-unmarked-parent access. The protocol, test domain, laws and prior are unchanged; physical test availability is not asserted.

## 5. Exact two-component condition on a fixed mark fiber

Fix a proper pair (P,S) and selected marks r|S. Suppose each component is local, so its slot values a_0,a_1 are constant across this fiber of reachable full markings. For the fixed joint history law let p(r)=P(z=0 | P,r). Then

    bar_k(P,r,S) = a_1 + p(r)(a_0-a_1).

The marginal slot is constant on the fiber if and only if

    [p(r)-p(r')](a_0-a_1) = 0

for every pair r,r' having the same r|S. Equal component slots tolerate arbitrary posterior variation; unequal slots require posterior constancy on that fiber. Here a_0-a_1=d/2>0 and the two posteriors differ. This criterion explains the witness; it neither constructs its admitted components nor claims that every mixture fails locality.

## 6. Actual complete-history transport and every tail

For n<=6 a complete augmented natural marked history is determined by (z,F,r): birth-label restrictions reconstruct every prefix and ideal. For an adjacent incomparable swap sigma in F, keep z fixed, carry each vertex's mark with it, replace F by sigma F, and reconstruct the entire history.

Incomparability makes the new labeling natural; positivity makes every resulting atom eligible. The prefix before the pair is unchanged. The complete component diamond equates the swapped factors and payload maps, including full first precursors.

After the pair the full probability-relevant states (z,C) are isomorphic. At every subsequent birth, transport the ideal and new mark. Component Markov dependence and equivariance identify each conditional probability and map. This covers every suffix, including both modified layers when the swap occurred earlier. A swap of births five and six uses the base-four diamond and has no tail.

The inverse swap covers all markings and both selector atoms. It preserves the prior 1/2, every factor of rho_n and the composed map on arbitrary D. This is actual invertible complete-fiber transport (FT). Summing complete fibers gives marked and unmarked covariance through six.

## 7. The marked marginal retains diamonds but loses locality

Define g_n(C)=sum_z rho_n(z,C)>0 and p_z(C)=rho_n(z,C)/g_n(C). For the child C' obtained from (S,b),

    g_(n+1)(C') / g_n(C) = (1/2) sum_z p_z(C) k_z(C,S)
                         = bar_k(C,S)/2.

Natural marked C retains its projected past, so these ratios give autonomous full-C prediction for the fixed marginal. They are positive, normalized and telescope to full histories; fair marks and maximal immutable appends persist. The maps bar_k D/2 have complete sum identity on the passive carrier.

FT equates transported marked history masses. Two-step ratios telescope to g_terminal/g_base, proving every contained complete marked diamond, including the factor 1/4 on D. Transport also proves equivariance. Neither argument assumes marginal proper locality.

Rows before parent four coincide; only the fifth factor differs and the selector posterior before it is half/half. The entire marked five-birth marginal is the admitted t=3/4 prefix: proper=3q/4, full=1/4+3q/4. Sixth-birth prediction uses updated posteriors and fails strict proper locality. The marginal is not admitted under all original axioms.

These comparisons have distinct meanings:

| Property | What is held fixed or transported | Result |
|---|---|---|
| Proper-record locality | Same P and marks restricted to S, different unselected root bit | Fails for the marginal empty slot |
| Full-state record sufficiency | Identical full C5_i, different retained z | Fails: d versus d/2 |
| Covariance | Whole marked structures transported by relabeling | Holds through the finite horizon |

Changing a root bit is not a relabeling of the whole marked structure. Covariance therefore contradicts neither failure.

If marks are also hidden, put W_n(P)=sum_r g_n(P,r) and eta_n(r|P)=g_n(P,r)/W_n(P). The unmarked row is the separate sum sum_r eta_n(r|P) bar_k(P,r,S), after summing the newborn bit. Fair draws do not make old marks uniform conditional on P. No mark-dependent factor can be pulled out of this sum, and no marked-locality conclusion is recovered by doing so.

## 8. Boundaries, provenance and unchanged gates

This conditional nonclosure result does not reject every mixture, hidden state or DET. The prefix, all-mark c_i facts and extension theorem remain load-bearing. It gives no numerical continuation, seventh-birth/all-horizon law, arbitrary-prior strong lumpability, physical selector/readout, agency, quantum dynamics, geometry, application advantage or RI1451 escape. Record-observability/minimal-statistic questions remain open.

Historical LAW_DEPENDENCE is the supplied 17,936-byte body, intact once at byte offset 5,597 (line 40) in the expanded public file. Its historical §2 supplies L1; FINITE_LAW_DEPENDENCE is a different work. The quoted extension source was not expanded by following its original path or links.

RI1463's initial premises were 6,235 bytes against a 6,144-byte cap; final premises are 6,069 bytes. Its overlapping patch failed, with unchanged-state recovery and superseded prose retained. Author final prose is recorded at 13:04:03 UTC before 13:08:21. Preparation at 13:06:15 is not completion: final all-four 13:06:29 before 13:14:21 remains attributed without its original external completion receipt in this grant. Root records the distinct review's prose at 13:46:53 and final all-nine at 13:48:49, before its 13:54:44 and 14:00:44 limits; preparation at 13:48:34 is separate. Current pins do not reconstruct historical inspection.

Inherited cap/patch/display/schema/manifest-pin-basis, superseded-prose, missing/late and attributed-completion qualifications persist. E retains complete failure behavior, cost, latency and source-to-reset closure. NE retains both-world source/reset/control/readout certification and history-wise costs. CE retains interface ownership, implementation, runtime/allocator/enforcer and hard-resource gates, with M1 held. Measurement retains actual representation/serialization, source/build/ABI/binding, resources, controls, qualification and observed-execution holds. Nominal calculation is separate from calibration or production assurance.

Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, the shared 10% stop/reset guard and RET-only pause remain. This publication candidate supplies no execution or release receipt.
