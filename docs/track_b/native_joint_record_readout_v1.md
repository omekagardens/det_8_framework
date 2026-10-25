# Joint record readout with a shared mark orientation

This note assembles accepted conditional finite results for two separate complete three-birth records. Part A gives the admitted model and fixed structural prefix. Part B reproduces the complete single-record argument from the [record-readout note](native_record_readout_v1.md), including the outcome table and optional error model used by Part C. Part C gives the joint-law result.

Repeated preparation, the declared conditional product laws and optional independent response errors are imported mathematical premises. A common relative mark dictionary is required for the joint readout. No physical preparation, reset, detector, calibration or empirical law selection is supplied, and no physical repeated-trial independence is inferred. The ideal information statements retain all outcomes and do not admit execution.

## A. Original model and the fixed four-birth structural prefix

A state consists of a finite order \(P\), immutable binary marks \(r:P\to\{0,1\}\), and an arbitrary complex positive-semidefinite payload \(\mathfrak D\) on a fixed carrier. An ideal \(S\subseteq P\) is a downward-closed subset, including the empty and full ideals. A birth appends one maximal vertex with strict past exactly \(S\); write the resulting order \(P+S\). The newborn mark \(b\) is independently fair. The branch map is

\[
 \mathcal B^{P,r}_{S,b}(\mathfrak D)
       =\frac{q(P,r,S)}2\,\mathfrak D .
 \tag{1}
\]

The admitted model requires:

- Every ideal is eligible, \(q(P,r,S)>0\), and the complete ideal sum is one.
- A proper-slot probability may read the whole unmarked order \(P\), but only the marks in \(S\). A full slot may read all old marks.
- Relabeling transports order, ideal and marks together; probabilities are equivariant.
- Two incomparable births commute as complete unnormalized marked maps. Both newborn bits, equal-precursor pairs and all inherited marks are included.
- There is one committed birth at a step. This bookkeeping step is not a physical clock and is not a claim that every present relational activity creates a record.

For two ideals \(S,T\) of a base \(C\), with the new vertices excluded from the second precursors, the diamond identity is

\[
 q(C,r,S)q(C+S,r+b,T)
   =q(C,r,T)q(C+T,r+c,S).
 \tag{2}
\]

Both sides multiply the same transported terminal payload by \(1/4\). Equation (2) is not merely agreement of normalized probabilities or diagonal payloads.

For a proper ideal in a nonempty parent, let \(M=\operatorname{Max}(P)\setminus S\). Its fixed maximal-deletion potential is

\[
 u(P,r,S)=
 \prod_{\varnothing\ne A\subseteq M}
 q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}} .
 \tag{3}
\]

These are evaluations of smaller mathematical inputs, not erasure of committed history. Full smaller-parent slots retain their full induced marks.

The admitted ratio-component theorem says that (3) satisfies all inherited ratio equations and that every positive solution at the next layer has the form
\(q(P,r,S)=\alpha_{\mathcal C(P,S,r|S)}u(P,r,S)\) on proper slots. The component key keeps the whole unmarked parent and selected marks. All labeled ideal occurrences contribute separately to row sums. Full slots are normalization complements.

### The fixed instance, not a uniquely selected law

The smaller seed is prescribed:

\[
 a_{\rm seed}=2/3,\quad c_{\rm seed}=1/5,\quad d_{\rm seed}=1/4,
 \quad f_{\rm seed}(0)=1/6,\quad f_{\rm seed}(1)=1/3,
\]
\[
 g_{\rm seed}=1/10,\quad k_{\rm seed}=11/20,\quad
 h_{\rm seed}(0)=19/30,\quad h_{\rm seed}(1)=7/15,\quad e=1/44 .
\]

The singleton, two-chain and two-antichain ideal rows are
\((a_{\rm seed},1-a_{\rm seed})\),
\((c_{\rm seed},f_{\rm seed}(i),h_{\rm seed}(i))\), and
\((d_{\rm seed},g_{\rm seed},g_{\rm seed},k_{\rm seed})\).
The parent-three proper rows are:

| Parent | Proper ideal probabilities |
| --- | --- |
| Three-antichain | Empty \(e\); each singleton \(eg_{\rm seed}/d_{\rm seed}\); each pair \(ek_{\rm seed}/d_{\rm seed}\) |
| Edge \(u<v\), isolate \(w\) | Empty and \(w\): \(e\); \(u\): \(ef_{\rm seed}(r_u)/c_{\rm seed}\); \(uv\): \(eh_{\rm seed}(r_u)/c_{\rm seed}\); \(uw\): \(ek_{\rm seed}/g_{\rm seed}\) |
| Fork | Empty and root: \(e\); each root-plus-leaf ideal \(eh_{\rm seed}(i)/f_{\rm seed}(i)\) |
| Join | Empty, each root singleton and root pair: \(e\) |
| Three-chain | Empty, root and initial pair: \(e\) |

Every full slot is the complete complement.

## B. Conditional record discrimination

### 1. Outcomes, common channels and invariant blindness

At a fixed horizon \(n\le4\), let \(\Gamma_n\) contain every naturally encoded complete marked history, with each ideal occurrence and newborn bit retained. Equivalently, a record may be its canonical marked endpoint: the endpoint probability sums all distinct natural encodings, rather than treating an isomorphism class as one history. Let \(F\) flip every bit without changing the order. Accepted whole-law transport gives
\[
 L_1(\gamma)=L_0(F\gamma),\qquad L_*=(L_0+L_1)/2.
\]
We compare \(L_0\) with \(L_*\), not \(L_0\) with \(L_1\).

Declare one common observation kernel \(R(B\mid\gamma)\), where \(B\) is an outcome event. It cannot depend on the unknown hypothesis. If
\(R(B\mid F\gamma)=R(B\mid\gamma)\) for every \(B,\gamma\), then
\[
 P_1^R(B)=\sum_\gamma L_0(F\gamma)R(B\mid\gamma)
 =\sum_\eta L_0(\eta)R(B\mid F\eta)=P_0^R(B).
\]
Hence \(P_*^R=P_0^R\). This covers unmarked order observations and stochastic readouts of global-bitflip orbits. It is a restriction on the declared channel, not a no-go for all physical measurements.

Global mark-name symmetry differs from vertex relabeling: the former exchanges zero and one everywhere; the latter transports each vertex's attached mark while renaming vertices. A readout may respect the latter and break the former.

The original payload contributes no independent distinction. For either hypothesis, a complete history acts on any common prepared payload/reference state \(\rho_{AR}\) as \(L_s(\gamma)\rho_{AR}\). Summing every record gives
\[
 \sum_\gamma L_s(\gamma)\rho_{AR}=\rho_{AR}.
\]
Thus fixed unselected payload/reference measurements agree, even for entangled preparations. This assumes the same initial state, without a hypothesis already encoded in the reference or a new record-dependent interaction.

### 2. First distinguishing horizon and complete probabilities

At \(n=0,1,2\), both component laws coincide: the empty/singleton transitions are mark-independent and all newborn bits are fair. Consequently \(L_0=L_*\) on complete records there.

At \(n=3\), use the actual prefix
\[
 a=2/3,\ d=1/4,\ g=1/10,\ c=1/5,\ k=11/20,
\]
\[
 f_0=1/6,\ f_1=1/3,\qquad h_0=19/30,\ h_1=7/15.
\]
The structural weight of one natural encoding is \(1/6,1/15,f_i/3,11/30,h_i/3\) for antichain, edge plus isolate, fork, join and chain. Multiply by \(1/8\) for its specified three bits. These follow respectively from \(ad\), \(ag=c/3\), \(f_i/3\), \(ak\), and \(h_i/3\). In the fork \(i\) is the unique root mark; in the chain it is the unique minimum mark. Under \(L_*\), replace \(f_i\) by \(1/4\) and \(h_i\) by \(11/20\) for these history weights.

The following table partitions all outcomes. Counts list complete histories and canonical marked endpoints; probabilities sum all marks not specified in the row.

| Record sector | Histories | Endpoints | \(P_0\) | \(P_*\) | \(P_0-P_*\) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Antichain | 8 | 4 | \(1/6\) | \(1/6\) | 0 |
| Edge plus isolate | 24 | 8 | \(1/5\) | \(1/5\) | 0 |
| Join | 8 | 6 | \(11/30\) | \(11/30\) | 0 |
| Fork, root 0 | 4 | 3 | \(1/36\) | \(1/24\) | \(-1/72\) |
| Fork, root 1 | 4 | 3 | \(1/18\) | \(1/24\) | \(+1/72\) |
| Chain, minimum 0 | 4 | 4 | \(19/180\) | \(11/120\) | \(+1/72\) |
| Chain, minimum 1 | 4 | 4 | \(7/90\) | \(11/120\) | \(-1/72\) |
| Total | 56 | 32 | 1 | 1 | 0 |

For an antichain, the four endpoint classes have zero-count multiplicities \(1,3,3,1\). Each edge-plus-isolate marking has three natural encodings. Fork leaves and join roots are unordered: equal marks have multiplicity one, mixed marks multiplicity two. A marked chain has one encoding. These give all 56 histories and 32 marked endpoint classes with no extra automorphism factor.

More finely, each fork/chain history has signed difference of magnitude \(1/288\): negative for fork-root zero and chain-minimum one, positive for the other two sectors. For example,
\[
 \frac{f_0-1/4}{24}=-\frac1{288},\qquad
 \frac{h_0-11/20}{24}=\frac1{288}.
\]
Every other history has zero difference. Within each canonical marked endpoint all histories have the same sign, so quotienting by vertex relabeling causes no cancellation. Thus the complete-history and complete-endpoint distances both equal
\[
 d_{\rm TV}(P_0,P_*)=\frac12\sum_\gamma|L_0(\gamma)-L_*(\gamma)|
 =\frac12\frac{16}{288}=\frac1{36}.
\]
Together with the zero distances at earlier horizons, this proves earliest distinction at three births.

### 3. An intrinsic optimal binary readout

Define
\[
 E=\{\text{three-chain with minimum mark }0\}
 \ \cup\ \{\text{three-fork with root mark }1\},
 \qquad Y=\mathbf1_E.
\]
This event is intrinsic and vertex-relabel-equivariant. It uses only order shape and its unique root/minimum mark, not leaf marks, birth labels or the unknown hypothesis.

It includes every positive signed-difference outcome and none of the negative ones. Therefore
\[
 P_0(Y=1)=\frac{29}{180},\qquad P_*(Y=1)=\frac2{15}=\frac{24}{180}.
\]
The complementary probabilities are \(151/180\) and \(13/15=156/180\). All antichain, edge, join and other outcomes are counted; there is no postselection.

For any common stochastic readout and outcome event \(B\), put \(\delta=L_0-L_*\). Since \(0\le R(B\mid\gamma)\le1\) and the positive and negative masses of \(\delta\) agree,
\[
 \left|\sum_\gamma R(B\mid\gamma)\delta(\gamma)\right|
 \le\sum_{\gamma:\delta(\gamma)>0}\delta(\gamma)=\frac1{36}.
\]
Taking the supremum over output events proves the same upper bound for every readout. The displayed binary event attains it, proving optimality without a discrete-output restriction.

If equal hypothesis priors and ordinary correct/incorrect single-realization loss are externally declared, choose \(L_0\) when \(Y=1\) and \(L_*\) otherwise. Its optimal accuracy is
\[
 \tfrac12[P_0(E)+P_*(E^c)]
 =\frac{1+d_{\rm TV}}2=\frac{37}{72}.
\]
This is a decision convention, not a DET-derived prior, trial budget, repeated-trial independence claim or experimental performance result.

### 4. Orientation and one declared error model

The readout breaks global bitflip invariance: \(F(E)\) exchanges the two root-mark conditions and is disjoint from \(E\). A common calibrated dictionary must identify what physical record category, if any, is called zero under both hypotheses. Simultaneously transporting the law and this dictionary is only a coordinate change; the proposed comparison keeps the calibrated readout fixed.

Breaking flip invariance alone is insufficient. For example, the total zero count has the same binomial law under both hypotheses. Here the distinguishing information is the correlation between order shape and an oriented root mark.

As one explicitly imported single-trial channel, suppose shape is classified correctly and the relevant fork/chain root bit is independently flipped with known probability \(0\le\epsilon\le1/2\), identically under both hypotheses. Record shape and the reported root bit for these two shapes; report the other shapes without postselection. This is a declared response model, not supplied apparatus.

Each positive/negative root-sector difference becomes
\(\pm(1-2\epsilon)/72\); all other sectors still agree. The same binary rule on reported marks gives
\[
 P_0(Y_\epsilon=1)=\frac{29-10\epsilon}{180},\qquad
 P_*(Y_\epsilon=1)=\frac2{15},
\]
and attains the complete declared noisy-channel distance
\[
 d_{\rm TV}^{(\epsilon)}=\frac{1-2\epsilon}{36}.
\]
The equal-prior accuracy becomes \(1/2+(1-2\epsilon)/72\). The distinction vanishes at \(\epsilon=1/2\).

An unknown orientation fixed across trials is not automatically this independent error channel. A common unknown convention, a deliberately randomized per-record convention and calibrated bit errors require different models; no repeated-trial inference is made here.

### 5. Remaining physical bridge and stop

A physical prediction would require a justified correspondence from native events and marks to distinguishable records, a preparation and collection procedure yielding complete three-birth records, a detector map identifying order/root, and an independently fixed mark dictionary with a calibrated common response. Missing/delayed records and acquisition costs would need their own evidence. None is supplied by this ideal information calculation.

The question is closed conditionally: invariant readouts and passive payload are blind; a calibrated oriented shape-root correlation attains the exact three-birth contrast. No physical observer, empirically selected law, hidden agency, metric, gravity or GWOSC forward map follows. Original fair-model results, CE advantage closure and all standing gates remain.

## C. Shared orientation and joint record discrimination

### 1. Two joint laws, not a longer growth history

Let \(P=L_0\), \(Q=L_1=F_*P\), and \(M=L_*=(P+Q)/2\) on one complete three-birth record. Define
\[
 d=P-M=(P-Q)/2,\qquad P=M+d,\quad Q=M-d.
\]
From accepted QR-LD008, \(\sum d=0\), \(d(Fx)=-d(x)\) and \(\|d\|_1=1/18\).

Declare two distinct preparation laws on an **ordered pair** of records:
\[
 C=\tfrac12(P\otimes P+Q\otimes Q),\qquad I=M\otimes M.
\]
For \(C\), the two records are conditionally independent given one fair shared component choice. For \(I\), independent component choices and conditional product preparation produce two independent \(M\) records. Neither product law, fair component choice nor a reset mechanism is derived from the single-record growth law. There is no six-birth connected-history construction.

Expanding the products gives the complete signed pair law
\[
 \boxed{C-I=d\otimes d.}
\]
Summing either argument removes this term, so both one-record marginals of \(C\) and \(I\) equal \(M\). Equality of marginals therefore does not identify the joint law.

### 2. Complete multiplicities and exact distance

Use an intrinsic sign \(s(x)\):
- \(+1\): chain with minimum mark zero, or fork with root mark one;
- \(-1\): chain with minimum mark one, or fork with root mark zero;
- \(0\): antichain, edge plus isolate or join.

The accepted single-record masses, independently checked from the supplied signed table, are:

| Sign sector | Histories | Canonical endpoints | \(M\) mass | \(d\) mass | \(P\) mass |
| --- | ---: | ---: | ---: | ---: | ---: |
| \(+\) | 8 | 7 | \(2/15\) | \(1/36\) | \(29/180\) |
| \(-\) | 8 | 7 | \(2/15\) | \(-1/36\) | \(19/180\) |
| \(0\) | 40 | 18 | \(11/15\) | 0 | \(11/15\) |

Each nonzero individual history has \(d=\pm1/288\); all others have zero signed mass. Canonical marked endpoint masses include their natural-encoding multiplicities. In particular, mixed-leaf forks contribute twice the per-history difference; no opposite signs merge within a marked endpoint.

The full ordered pair space has \(56^2=3136\) histories or \(32^2=1024\) endpoint pairs. A pair of endpoint fibres has multiplicity equal to the product of its two single-record multiplicities. No factor of two is removed when the records exchange positions.

The sector partition of \(C-I\) is the outer product:

| First \ Second | \(+\) | \(-\) | \(0\) |
| --- | ---: | ---: | ---: |
| \(+\) | \(1/1296\) | \(-1/1296\) | 0 |
| \(-\) | \(-1/1296\) | \(1/1296\) | 0 |
| \(0\) | 0 | 0 | 0 |

There are 128 positive and 128 negative history pairs, each of magnitude \(1/82944\), and 2880 zero-difference pairs. At endpoint level the corresponding counts are 98, 98 and 828, with multiplicity-weighted magnitudes. This retains all unused sectors; it does not condition on two informative shapes.

Therefore
\[
 d_{\rm TV}(C,I)
 =\tfrac12\|d\otimes d\|_1
 =\tfrac12\|d\|_1^2
 =\boxed{\frac1{648}}.
\]
The canonical-endpoint distance is identical because the sign is constant on every pair of fibres.

### 3. An invariant optimal event

Take
\[
 A=\{s(x)s(y)=1\}.
\]
In words, both records must be chains or forks. Their root/minimum marks must agree when their shapes agree, and differ when their shapes differ. Every other pair gives the complementary outcome.

This event respects vertex relabeling within either record and exchange of the record positions. Since \(s(Fx)=-s(x)\), it is invariant under the simultaneous flip \((x,y)\mapsto(Fx,Fy)\). It is not invariant under flipping only one record. It requires a common relative mark dictionary across the pair, but no absolute designation of zero.

The event contains exactly the positive signed pair masses. Consequently it attains total variation, and no common stochastic readout can exceed it: any output event weights each signed pair mass by a number between zero and one.

Its exact probabilities are
\[
 I(A)=2(2/15)^2=\frac8{225},\qquad
 C(A)=\left(\frac{29}{180}\right)^2+
       \left(\frac{19}{180}\right)^2=\frac{601}{16200}.
\]
Their difference is \(1/648\). The complements have probabilities \(217/225\) and \(15599/16200\), respectively. Pairs with at least one zero-sign record have common probability \(209/225\) and remain included.

For externally declared equal priors on \(C\) versus \(I\) and single-pair zero-one loss, declaring \(C\) on \(A\) gives optimal accuracy
\[
 \tfrac12+\tfrac1{1296}=\frac{649}{1296}.
\]
This is an ideal information bound, not an experimental success rate.

### 4. Fixed unknown orientation: a minimax proof without a nuisance prior

Separately consider the composite alternative
\[
 A_0=P\otimes P,\qquad A_1=Q\otimes Q
\]
against null \(I\). The orientation \(\theta\in\{0,1\}\) is fixed and unknown; no probability distribution over it is assumed. Conditional product preparation is still an explicit premise.

For any randomized test \(\phi\in[0,1]\) that declares the alternative with probability \(\phi\), define its equal-null/alternative-prior accuracy against orientation \(\theta\) by
\[
 a_\theta(\phi)=\tfrac12\bigl[E_{A_\theta}\phi+E_I(1-\phi)\bigr].
\]
For every test,
\[
 \min_\theta a_\theta(\phi)
 \le\tfrac12[a_0(\phi)+a_1(\phi)]
 =\tfrac12[E_C\phi+E_I(1-\phi)]
 \le\frac{649}{1296}.
\]
The arithmetic average is an upper-bound device, not an asserted prior for the actual nuisance.

For \(\phi=\mathbf1_A\), simultaneous-flip invariance and
\(A_1=(F\otimes F)_*A_0\) give
\(A_0(A)=A_1(A)=C(A)\). Thus both accuracies equal \(649/1296\), attaining the bound:
\[
 \sup_\phi\min_\theta a_\theta(\phi)=\frac{649}{1296}.
\]
Equal priors apply only to null versus alternative in this decision convention. No actual random orientation, repeated-trial independence or physical reset is inferred.

### 5. When single-record blindness extends

If a joint readout kernel \(K(B\mid x,y)\) is invariant under flipping either record separately, then
\[
 \sum_{x,y}d(x)d(y)K(B\mid x,y)=0:
\]
change variables \(x\mapsto Fx\), which reverses the signed sum while leaving the kernel unchanged. Invariance in that one argument already suffices for this comparison. Products of individually flip-invariant readouts, with independent response noise, are a sufficient example.

Simultaneous flip invariance is weaker and does not erase the correlation: \(A\) is the counterexample. Thus the accepted single-record blindness theorem is preserved. It cannot be applied to each coordinate while silently retaining a joint comparison of the two orientations.

Two independent \(M\) preparations give \(I\); one shared component plus conditional independence gives \(C\). A detector response cannot establish which preparation/reset law was actually supplied. Joint preparation and dictionary alignment must be specified independently of the observation statistic.

### 6. One optional imported error channel

Assume correct shape classification and the same calibrated root-bit error probability \(0\le\epsilon\le1/2\) on each record, as in QR-LD008. **Additionally assume the two measurement errors are independent**, conditional on their records and component, and independent of the true bits. These are mathematical response assumptions.

Let \(T_\epsilon\) be that common one-record channel, \(M_\epsilon=T_\epsilon M\), and \(d_\epsilon=T_\epsilon d\). The accepted single-record sector calculation gives
\[
 \|d_\epsilon\|_1=(1-2\epsilon)/18.
\]
Product response independence then yields
\[
 C_\epsilon-I_\epsilon=d_\epsilon\otimes d_\epsilon,\qquad
 d_{\rm TV}(C_\epsilon,I_\epsilon)=\frac{(1-2\epsilon)^2}{648}.
\]
The same sign-agreement event on reported bits attains the bound:
\[
 I_\epsilon(A)=8/225,\qquad
 C_\epsilon(A)=8/225+(1-2\epsilon)^2/648.
\]
The channel commutes with the global flip, so the two fixed-orientation output laws remain related by simultaneous transport. The corresponding equal-prior accuracy is \(1/2+(1-2\epsilon)^2/1296\); the same symmetry argument proves the composite minimax value for this declared channel. Contrast vanishes at \(\epsilon=1/2\).

A perfectly shared mark-name flip would leave \(A\) unchanged, so it is not this independent-error channel. No statement about unknown or correlated apparatus errors is imported.

### 7. Missing operational input and stop

The smallest missing operational input is a specified joint preparation/readout contract: the pair's preparation/reset law, a stable shared versus independently randomized mark dictionary, retention of both complete records, and a common response calibration including cross-record error dependence. No such physical contract or evidence is supplied.

This closes the finite information question conditionally. Shared orientation can leave a simultaneously invariant pair correlation; independent symmetrization removes it. No physical iid repetitions, acquisition costs, metric/gravity, clocks, energy/work stores, hidden agency or empirical law selection follow. CE efficiency closure and all standing gates remain.
