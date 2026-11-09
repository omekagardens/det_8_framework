# A same-trial position triple rejects timed Markov projection, conditional on a noninvasive reader

**Independently reviewed conditional result.** The persistent target's position triple at births 1,2,3 rules out every autonomous position-only nearest-neighbor Markov sequence, even with a different probability at every site and birth. Four fresh terminal laws alone do not: one timed projection kernel reproduces all of them. The triple does not locate memory inside the moving carrier. An explicit reader that stores only the first PUBLIC report and feeds back one sitewise transition parameter reproduces the entire triple, every failure pattern and all original terminal settings, with no persistent heading in the carrier. That control needs an extra feedback-actuation capability; a passive recorder does not grant it.

## 1. Fixed transport, native histories and observation contracts

Use the accepted GDM055 geometry Z/11Z, launch X0=0, fair hidden heading, one branch-independent local update per native birth and original horizon set n=1,2,3,4. For the persistent target rho=1/2, a heading continues with probability p=3/4 and flips with q=1/4; Xi=sum_(j<=i) Hj modulo11. No signed endpoint through four aliases another lifted endpoint in [-4,4].

Keep every naturally encoded marked native history gamma in Gamma_n, its actual ideals and bits, with the original

    w_gamma=2^(-n) product_i q_Ci(Si),  sum_gamma w_gamma=1,
    B_gamma u=w_gamma u.

These are inherited accepted identities. The prescribed launch is a product with transport; no native mark, ideal, residual value or history controls motion, detection or instrument randomization. No arbitrary correlated preparation is inferred from this factorized law.

The NEW setting ends at the already allowed third birth and reads position at births 1,2,3, preserving trial identity and order. Let Oi be a true position or the distinct failure symbol perp. At each read a fresh independent fair success coin reports Xi on success and perp otherwise. In the primary comparison these reads have no effect on any hidden state or transition and cause no feedback. The other four settings keep their original fresh preparations and ONE terminal read at the chosen birth n. They never constitute a measured trajectory.

Let di=1 for a detected position and 0 for failure, and let S(o) be the set of detected coordinates of a proposed triple o. Each of the eight failure masks has unconditional probability 1/8, independently of native history, in the ideal target. All eleven sites remain possible output labels at every coordinate, with inaccessible cells exactly zero.

For a true position triple x=(x1,x2,x3) define the complete noninvasive emission kernel

    D(o|x)=(1/8) product_(i in S(o)) 1_[oi=xi],

where a coordinate not in S(o) is exactly perp. This specification gives every one of the 12^3 possible records, not an all-success-only protocol.

## 2. Entire target triple law

The eight heading words and their true position triples are:

| Heading word | (X1,X2,X3) | Persistent probability |
| --- | --- | ---: |
| +++ | (1,2,3) | 9/32 |
| ++- | (1,2,1) | 3/32 |
| +-+ | (1,0,1) | 1/32 |
| +-- | (1,0,-1) | 3/32 |
| -++ | (-1,0,1) | 3/32 |
| -+- | (-1,0,-1) | 1/32 |
| --+ | (-1,-2,-1) | 3/32 |
| --- | (-1,-2,-3) | 9/32 |

The entries come from (1/2) times the two continuation/flip factors and sum to (18+12+2)/32=1. Let G(x1,x2,x3) denote this normalized distribution, zero elsewhere. The full new joint law is

    P_triple(gamma,o)
      = w_gamma sum_x G(x) D(o|x),  gamma in Gamma_3.

For each gamma, summing over every o gives w_gamma. Every failure mask sums to w_gamma/8, including P(gamma,perp,perp,perp)=w_gamma/8. All originally distinct native histories retain their weights. Summing over gamma preserves normalization and the exact zero cells. No detection, native branch or position is postselected out.

The primary timed-Markov competitor has one sequence K1,K2,K3,K4, shared across ALL observation settings, with

    Kn(x+1|x)=p_n(x),  Kn(x-1|x)=1-p_n(x),

each p_n(x) independently arbitrary in [0,1]. It has no other dynamical state or common persistent seed. Its launch is delta0 and its true triple law is

    G_K(x1,x2,x3)=K1(x1|0)K2(x2|x1)K3(x3|x2).

The same noninvasive D and native factor w_gamma produce its complete observed law, with zeros, failures and all columns normalized. Time dependence and spatial asymmetry are fully allowed.

## 3. Exact observed witness against every timed position-only sequence

Among all-success records, inspect the four cells with X2=0. After summing native histories their probabilities on ALL prepared trials are

| O1 | O2 | O3=+1 | O3=-1 |
| --- | --- | ---: | ---: |
| +1 | 0 | 1/256 | 3/256 |
| -1 | 0 | 3/256 | 1/256 |

For a particular gamma multiply each cell by its unchanged w_gamma. The common factor 1/8 is the three independent detection coins; it is not a renormalization of the trial ensemble.

A Markov factorization would make the conditional probability of the third right step at the same birth and site equal to the one number p_3(0), regardless of X1. The first row of the displayed record forces

    p_3(0)=(1/256)/(4/256)=1/4,

while the second row forces

    p_3(0)=(3/256)/(4/256)=3/4.

Both denominators are strictly positive. Equivalently, the 2x2 cell matrix required by a position-Markov model has rank at most one, but these cells have determinant
(1*1-3*3)/256^2=-1/8192. For each native history that determinant is multiplied by w_gamma^2>0.

This excludes every stated timed sitewise sequence, not merely a fixed kernel or a symmetric candidate. Equality of COMPLETE observed laws would in particular match these four cells; dividing their common known detector factor in a proof does not delete any failure outcome. Arbitrary probabilities at other sites, at later births, or at boundaries 0 and 1 cannot make one p_3(0) have two values. The same-trial links and noninvasiveness, rather than absolute time or a heading sensor, are the operative added premises.

## 4. Constructive timed projection for every original fresh terminal law

Let f_n be the accepted persistent one-time position law. For every occupied site at birth n-1 define

    K_n^proj(y|x)=P_persistent(Xn=y | X_(n-1)=x).

At unoccupied sites choose a fair nearest-neighbor column. Every column is normalized, local and nonnegative. Since

    f_n(y)=sum_x K_n^proj(y|x) f_(n-1)(x),

induction from delta0 shows that ONE sequence reproduces f1,f2,f3,f4, not a separate fit chosen for each horizon.

An explicit completion on all eleven sites is obtained by taking every unlisted p_n(x)=1/2 and using:

| Birth update n | Occupied old site x | Right probability p_n(x) |
| --- | --- | ---: |
| 1 | 0 | 1/2 |
| 2 | +1 | 3/4 |
| 2 | -1 | 1/4 |
| 3 | +2 | 3/4 |
| 3 | 0 | 1/2 |
| 3 | -2 | 1/4 |
| 4 | +3 | 3/4 |
| 4 | +1 | 15/28 |
| 4 | -1 | 13/28 |
| 4 | -3 | 1/4 |

For example, conditional on X3=+1 the target's last heading is +1 with probability 4/7 and -1 with 3/7, from the three corresponding words in Section 2. Its next right probability is (3/4)(4/7)+(1/4)(3/7)=15/28. Reflection gives 13/28 at -1. This verifies the only less immediate projected columns; all unvisited columns remain valid and irrelevant to the prepared rows.

At each fresh terminal setting n the entire record is therefore

    P_n(gamma,detected x)=w_gamma f_n(x)/2,
    P_n(gamma,perp)=w_gamma/2.

These equal the accepted target in EACH joint native-history cell, including every unreachable site's zero cell. The first three birth-pair marginals of a projected sequence do not imply the target's triple law; Section 3 shows the lost correlation explicitly.

CL070's accepted benchmark is retained as a peer-owned source: the time-INDEPENDENT sitewise class fails at the fourth terminal law, with all-trial detected-return probabilities 7/128 versus 13/128 and gap 3/64. That proof is not repeated here. Allowing birth-specific kernels is a changed competitor class, and the construction above explains why the old endpoint obstruction does not transfer to it. No fresh-run terminal distributions are treated as positions on one trajectory.

## 5. Independent-heading positive control

For rho=0 the three directions are independent fair signs. Each of the eight words in Section 2 then has probability 1/8. Use p_n(x)=1/2 for every site and birth. This gives exactly the full TRUE triple law and, with D, the same entire observed record and all eight failure masks. Each all-success word has probability1/64 after summing native histories, with its native factor restored on each joint cell. At X2=0 the two preceding positions both imply next-right probability1/2, so the conditional-independence witness vanishes as it should.

The same uniform sequence reproduces all four accepted independent-heading fresh terminal/binomial laws. This is a matched positive control with unchanged detector and native attachment, not a claim that a different persistent model has been excluded.

## 6. A memory/feedback reader can match EVERY observed setting

Now deliberately relax the primary no-feedback premise. The moving carrier has only position, with autonomous base sequence K^proj from Section 4 and fresh transition randomness. A separate reader memory M in {empty,+1,-1} resets to empty at each preparation. This is an abstract conditional instrument control, not a proposed physical detector.

Its information and actions are precisely these:

1. If a read is scheduled at birth 1, it uses the same honest fair detection coin as before. Store M=+1 or-1 only when that PUBLIC position is reported; on failure retain M=empty. The reader never learns a failed position, heading or native history.
2. The second motion update uses the unchanged base K2. A scheduled read at birth 2 uses its own independent fair coin. Retain M; no extra hidden observation is made.
3. Before update 3 the reader can select a SITEWISE transition table based on M. Keep p_3(+2)=3/4,p_3(-2)=1/4 and the other base entries, except set

       p_3(0|M=+1)=1/4,
       p_3(0|M=-1)=3/4,
       p_3(0|M=empty)=1/2.

   Actual moves use fresh carrier randomness with these probabilities. The instrument need not learn X2: the carrier's site state selects the column of the chosen table.
4. The third read uses another independent fair coin and reports actual position or failure. No persistent heading is stored in the moving carrier. Original terminal-only settings have no earlier reads, so M stays empty during all their motion and the original K^proj sequence, including update 4, remains in force. A terminal read at birth 1 can store a value only after the final move, with no subsequent control within that setting.

The only extra actuation premise is the ability to apply these reader-memory-conditioned sitewise update 3 laws, specifically the entry at site zero. Storage of a public record alone does not grant that service. Without such feedback capability the primary autonomous-class obstruction remains. This construction does not require a privileged sensor beneath the failure outcome or a pre-shared hidden heading seed.

### Complete record proof, including failed early reads

Let d=(d1,d2,d3) be any one of the eight success masks. Coins remain independent fair draws and independent of native history, so its total probability is1/8. Future controlled motion may depend on d1; therefore these coins are NOT independent of the entire latent trajectory in the feedback model. That change is the intentional failure of noninvasiveness.

If d1=1, the report gives the actual X1. Conditional on X1=+1, the only possible X2 are2 and 0: the target's next-right probabilities at update 3 are respectively 3/4 and 1/4, exactly the controlled entries. Conditional on X1=-1, the possible sites are-2 and 0, with probabilities1/4 and3/4. Thus the instrument's entire true triple law conditional on first-read success is G, not merely its final marginal. Independently keeping or failing either later read gives all the correct recorded marginals for d1=1.

If d1=0, M=empty and the base projected sequence is used. Although its true triple law G_K differs from G, X1 is NOT reported. The joint law of the remaining two true positions is

    sum_x1 G_K(x1,x2,x3)
      =f2(x2)K3^proj(x3|x2)
      =P_persistent(X2=x2,X3=x3).

Therefore keeping or failing either later read gives exactly the target records for EVERY mask with d1=0 as well.

More explicitly, for a record o with mask d the instrument law is

    P_inst(gamma,o)
      =(w_gamma/8) sum_x G^(d1)(x)
                           product_(i:di=1)1_[oi=xi],
    G^(1)=G,  G^(0)=G_K^proj.

For d1=0 summing the unreported x1 gives the equality just proved; for d1=1 equality is immediate. Hence P_inst=P_triple in every joint native-history/output cell, including all failures, forbidden sites and zero support. Normalization on each gamma is w_gamma. The four separate terminal settings equal their targets by Section 4 since feedback has not been armed there. One base sequence and one causal instrument rule serve all five settings; no endpoint law is selected independently after observing a horizon's result.

This feedback realization has external record memory and memory-conditioned transitions. It is not an autonomous position-only Markov competitor and does not contradict Section 3. It demonstrates exactly why this finite record cannot by itself locate memory in the moving carrier or establish a unique heading variable. A passive but retaining recorder, which never feeds back, would still leave the moving position process in the excluded timed-Markov class. The instrument example matches OBSERVED records; it deliberately does not claim to match unobserved true X1 when that first read fails.

For the independent-heading control use the uniform sequence with p_3(0|M)=1/2 for every M. No feedback change is then needed and all its joint records remain the independent target.

## 7. What the observation adds and what remains supplied

The added information is a same-trial conditional dependence at a common intermediate position. Separate endpoint laws, even four of them with native weights and known birth labels, carry no such joint trajectory. The timed projection construction preserves their marginals while discarding the predictive past. Reading hidden heading would use another channel and is unnecessary for this exclusion.

The result is conditional on honest true-site-or-failure output, independent fair read coins, preserved trial identity and birth order, the fixed product launch and branch-independent local motion, and NONINVASIVENESS of the added reads. The record does not independently certify that premise: the full memory/feedback control above is observationally identical within this five-setting contract. It leaves memory outside the moving carrier and uses a changed instrumental transition rule. No global minimality, unique hidden state or arbitrary-projection reconstruction is claimed.

Resources required and unmeasured include native preparation/ideal handling and product launch, the eleven-site coordinate and local updates, three independent read attempts in the new setting, trial/birth tags, storage of the joint reports and all failures, readout reliability and noninvasiveness, acquisition, and complete source/carrier/reader reset between trials. The feedback control additionally uses a three-valued external memory, routing of the first public report, conditional site-zero transition actuation before update 3 and independent move randomness. Those are granted abstract services, not free or measured physical operations; no claim of minimal memory or optimal costs. Conventional comparators receive the stated matched information and read services in each comparison.

Birth number is a supplied label, not duration; site is a residue, not calibrated distance; probability or heading persistence is not inertial mass or energy. No physical inertia, force, units, detector implementation, empirical evidence, timing/energy efficiency or advantage follows.

## Reviewed sources

- [Fair hidden headings can change finite endpoint records](fair_heading_transport_records.md)

Classical CL070/v1 disposition SHA-256 2ab83a155803dbdf545fcb37007bbe03050c2188eae79cb45f680cc199db858c. QR recipient disposition SHA-256 ad6713ac5e4aca623ce2bcc0b15e37f69644abe2b299a5fa44f9fef45888859b. Scientific report SHA-256 7ce44b36c2468230e679f5e3c04ad7555fca704e17ad053f5866e5ec2f4f6cb9. Independent review SHA-256 2c93efc7fa404457b15c63f4a2feeec6d8194c3f5a0379f4fc716bd5cfd8c3f0.
