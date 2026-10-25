# Precursor-local payloads: recovered contrast and shared-ancestor limits

This note combines a conditional construction and its finite information limit. A local update can recover a marked-chain probability difference that newborn-mark-only coupling loses. The same access can still miss whether two events share an ancestor. These are statements about an explicitly optional mathematical family; the original passive native law is unchanged.

The actual structural law and complete ideal support are specified in [the admitted model](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model). The [newborn-mark coupling result](native_mark_payloads_v1.md) supplies the earlier count-only comparison. The labels QR-LD003, QR-LD004 and QR-LD005 below identify that earlier comparison, Part I and Part II respectively. All witness kernels, endpoint events and additional preparation/readout assumptions needed for the present calculations are stated below.

## Part I. A precursor-local coupling recovers a probability contrast

### Proposed family and sufficient diamond condition

Keep the actual admitted \(q(P,r,S)>0\), all eligible ideals, finite horizon, immutable marks and positive intrinsic kernels \(p_b(K)\), with \(K=K(S,r|_S)\). On the same supplied common qubit carrier, with fixed basis and trivial order-relabeling action, propose
\[
\mathcal B^{P,r}_{S,b}(X)=q(P,r,S)p_b(K)\,\mathcal C_{K,b}(X),
\qquad \mathcal C_{K,b}=\operatorname{Ad}_{U_{K,b}},
\]
where the unitary family is fixed independently of the unknown kernel. Dependence is only on the intrinsic marked precursor and newborn bit, not outside marks, arbitrary labels, or a terminal endpoint.

A sufficient condition is pairwise commutation of all these conjugation channels. More narrowly, commutation is needed only for pairs of indices appearing together in a supported incomparable-birth diamond. Indeed their precursor classes \(K_S,K_T\) remain unchanged when the births are exchanged: neither new vertex belongs to the other's strict past. The intrinsic mark factors are the same in either order, and the actual complete \(q\) diamond gives a common positive scalar \(a\). The full maps are
\[
a\,\mathcal C_{K_T,c}\mathcal C_{K_S,b},
\qquad
a\,\mathcal C_{K_S,b}\mathcal C_{K_T,c}.
\]
Thus the stated sufficient condition equates unnormalized maps for every old marking, all bit choices and equal precursors. Positivity enforces commutation on an actually co-realizable pair; it does not prove global pairwise necessity for arbitrary indices at a bounded horizon. No general classification is asserted.

After the swap, the marked parents agree under transport. Every later marked precursor, newborn bit and scalar coefficient is transported identically, including suffix ideals containing either swapped vertex. The same transported suffix preserves full-map equality. This also covers a precursor that was full before the other birth and proper afterwards: its induced class is unchanged. Tensoring with the identity on a retained reference preserves these equalities on entangled inputs.

### A complete local rule

Let \(K_0\) be the class consisting of one vertex marked zero. For every admitted precursor class and newborn bit, set
\[
U_{K,b}=
\begin{cases}
Z=\operatorname{diag}(1,-1),&K=K_0\text{ and }b=0,\\
I,&\text{otherwise}.
\end{cases}
\]
This specifies both bits at empty, singleton and all larger precursor classes. It never tests the size or shape of the whole parent. All chosen channels are either identity or \(\operatorname{Ad}_Z\), so they commute globally and satisfy the sufficient condition.

Each branch is completely positive with Kraus operator \(\sqrt{qp_b}\,U_{K,b}\), and has trace \(qp_b\operatorname{Tr}X\). Since \(\sum_Sq=1\) and \(\sum_bp_b(K)=1\), every complete row preserves trace. For any admitted history,
\[
\mathcal B_h(X)=L_p(h)V_hXV_h^\dagger
\]
for a product of selected unitaries \(V_h\). Hence every classical marked-history probability, and every classical endpoint law, remains exactly that of the same supplied kernel and actual \(q\), for every normalized payload/reference input.

Trace normalization is not identity-channel normalization. In a singleton-zero parent, writing \(u=p_0(K_0)\), the actual row is
\[
(1-u/3)\operatorname{id}+(u/3)\operatorname{Ad}_Z,
\]
because the full-precursor probability is \(1/3\). With \(u>0\), this is not identity. Independently requiring identity nonselective maps would force every positive-weight active branch to fix each pure input: positive outputs summing to that pure input have its one-dimensional support, and their fixed traces fix their coefficients. Linearity then forces identity conjugation on every reachable branch. The proposed nontrivial rule would be excluded.

### Same two kernels, local encoding, fixed final readout

Use exactly the QR-LD003 horizon \(N=2\), actual singleton ideal row \(2/3,1/3\), and kernels
\[
p_0^F(K)=1/2\text{ for every }K;
\]
\[
p_0^G(\varnothing)=9/20,\quad
p_0^G(K_0)=23/30,\quad
p_0^G(K_1)=81/110,
\]
with \(p_0^G=1/2\) at every other admitted class and \(p_1=1-p_0\). Here \(K_1\) is the singleton marked one. Both kernels are strictly positive. The coupling above is identical under \(F\) and \(G\).

Prepare the same \(\rho_+=|+\rangle\langle+|\), where
\(|\pm\rangle=(|0\rangle\pm|1\rangle)/\sqrt2\).
After exactly two births, use the fixed payload-only effects
\(E_1=|-\rangle\langle-|\) and \(E_0=I-E_1\), with the stipulated trace rule.

At the first birth the precursor is empty, so the update is always \(I\). At the second birth it is \(Z\) exactly when the precursor is the zero-marked singleton and the newborn bit is zero. Thus the trigger is exactly the endpoint event \(C_{00}\): a two-vertex chain with both marks zero. It arises during the local update, not from a final oracle. The final effect acts only on the qubit; there is no record-conditioned readout or postselection.

The accepted endpoint probabilities are included explicitly. Each numerical entry is a numerator over \(600\); \(A_{ij}\) denotes an antichain and \(C_{ij}\) a chain with lower/upper marks \(i,j\).

| Endpoint | \(F\) | \(G\) | Total payload action |
| --- | ---: | ---: | --- |
| \(A_{00}\) | 100 | 81 | \(I\) |
| \(C_{00}\) | 50 | 69 | \(Z\) |
| \(A_{01}\) | 200 | 198 | \(I\) |
| \(C_{01}\) | 50 | 21 | \(I\) |
| \(C_{10}\) | 50 | 81 | \(I\) |
| \(A_{11}\) | 100 | 121 | \(I\) |
| \(C_{11}\) | 50 | 29 | \(I\) |

The mixed antichain includes both natural histories \(01\) and \(10\); equal-mark antichains are not doubled. Chains have their directed mark assignment. For example,
\[
P_p(C_{00})=\tfrac13p_0(\varnothing)p_0(K_0),
\]
giving \(1/12=50/600\) under \(F\) and \(23/200=69/600\) under \(G\). Each complete column sums to \(600\); all actual structural possibilities are included.

Writing \(r_p=P_p(C_{00})\), the full unselected final channel and state are
\[
\mathcal E_p=(1-r_p)\operatorname{id}+r_p\operatorname{Ad}_Z,
\qquad
\rho_p=(1-r_p)|+\rangle\langle+|+r_p|-\rangle\langle-|.
\]
Since \(Z|+\rangle=|-\rangle\),
\[
P_F(Y=1)=50/600,\qquad P_G(Y=1)=69/600.
\]
The complementary probabilities are \(550/600\) and \(531/600\); the binary total-variation contrast is \(19/600\). This is exact-law separation, not perfect one-outcome discrimination or a finite-sample guarantee.

### What changed and what did not

QR-LD003 remains correct for fixed newborn-bit-only channels. Here zero-marked births over empty and singleton-zero precursors have different actions; the normalized history channel no longer factors through newborn counts alone. At \(N=2\), \(A_{00}\) and \(C_{00}\) have the same count but different payload actions. Precursor access, rather than noncommuting updates, recovers this distinction.

The supplied rule records only the parity of its local triggers over longer already admitted prefixes; it is not a general order encoder. Its local access, qubit carrier, basis/relabeling convention, selected phase operation, preparation, final two-birth access and trace readout are additional premises. Their physical realization and calibration remain missing; coordinate changes must transform preparation and readout too. No clock/action scale, Born-rule derivation, physical detector, selected dynamics, gravity prediction or Boundary influence follows. The original passive model remains unchanged.

## Part II. Precursor profiles forget shared ancestry

### 1. Profile and factorization

Retain the actual positive structural probabilities \(q\), every eligible ideal, immutable marks, the admitted horizon and a positive intrinsic mark kernel \(p_b(K)\). The optional branch family is
\[
 \mathcal B^{P,r}_{S,b}
 =q(P,r,S)p_b(K(S,r|_S))\,\mathcal C_{K(S,r|_S),b},
 \qquad \mathcal C_{K,b}=\operatorname{Ad}_{U_{K,b}}.
\]
The common carrier, trivial relabeling action and indexed unitaries remain supplied premises; fix the family independently of the unknown kernel.

For a marked endpoint \(E=(V,\prec,r)\), let \(K_v\) be the isomorphism class of the marked induced strict past of \(v\), and define
\[
 m_E(K,b)=\#\{v\in V:(K_v,r(v))=(K,b)\}.
\]
This profile has finite support and total \(|V|\). It is intrinsic, without persistent vertex names.

**Theorem.** If the indexed conjugation channels commute pairwise, every history ending at \(E\) has normalized channel
\[
 T_{m_E}=\prod_{(K,b)}\mathcal C_{K,b}^{\,m_E(K,b)}.
\]
A maximal birth never changes an older vertex's strict past. Thus the update index at that vertex's birth is exactly its endpoint index. The history contains each vertex once; commuting the factors groups precisely the displayed multiplicities. This proves independence from natural labeling and history. It is algebraic reordering, not an asserted physical chronology. Commutation concerns channels; their chosen unitary representatives need not commute as matrices.

Keep the scalar weights separate:
\[
 \mathcal B_h=L_p(h)T_{m_E},\qquad
 \mathcal B_E=Q_p(E)T_{m_E},\qquad
 Q_p(E)=\sum_{h\to E}L_p(h).
\]
The sum is over distinct naturally encoded marked histories. Positivity ensures \(Q_p(E)>0\) for a reachable endpoint. Dividing by this scalar gives the conditional endpoint channel. Neither \(L_p(h)\) nor \(Q_p(E)\) is asserted to factor through the profile. Nor must the profile be recoverable from the payload: a particular channel family can discard further information.

### 2. The admitted four-birth collision

All four vertices have mark zero. On vertices \(a,b,c,d\), take:

- \(P\): \(a\prec c\), \(a\prec d\); \(b\) isolated, with no further strict comparabilities.
- \(Q\): \(a\prec c\), \(b\prec d\), with no further strict comparabilities.

Each has two minimal vertices and two nonminimal maximal vertices. They are nonisomorphic: \(P\) has an isolated vertex and \(Q\) has none. Let \(K_0\) denote the singleton marked zero. In both cases,
\[
 m(\varnothing,0)=2,\qquad m(K_0,0)=2,
\]
with all other entries zero. The profile forgets whether the two singleton pasts share their actual ancestor.

Natural labels \(a=1,b=2,c=3,d=4\) give ideal sequences
\[
 P:(\varnothing,\varnothing,\{1\},\{1\}),\qquad
 Q:(\varnothing,\varnothing,\{1\},\{2\}).
\]
Each selected subset is an ideal of its current parent. Both are on the actual positive support. The first three structural factors are \(1,2/3,1/10\). At the fourth birth the parent is an edge plus an isolate. The printed model gives
\[
 q(\{\text{edge root}\})
 =\frac{e f_{\rm seed}(0)}{c_{\rm seed}}=\frac5{264},
 \qquad q(\{\text{isolate}\})=e=\frac1{44}.
\]
Consequently these histories have structural weights \(1/792\) and \(1/660\). No new structural law, supplied mesh or wider horizon is used.

For completeness, all distinct natural encodings can be listed manually. Put \(\alpha=p_0(\varnothing)>0\), \(\beta=p_0(K_0)>0\). Every row below has the same mark factor \(\alpha^2\beta^2\).

| Endpoint | Ideal sequence | Structural weight |
| --- | --- | --- |
| \(P\) | \(\varnothing,\varnothing,\{2\},\{2\}\) | \(1/792\) |
| \(P\) | \(\varnothing,\varnothing,\{1\},\{1\}\) | \(1/792\) |
| \(P\) | \(\varnothing,\{1\},\varnothing,\{1\}\) | \((1/3)(1/5)(5/264)=1/792\) |
| \(P\) | \(\varnothing,\{1\},\{1\},\varnothing\) | \((1/3)(1/6)(1/44)=1/792\) |
| \(Q\) | \(\varnothing,\{1\},\varnothing,\{3\}\) | \((1/3)(1/5)(1/44)=1/660\) |
| \(Q\) | \(\varnothing,\varnothing,\{1\},\{2\}\) | \(1/660\) |
| \(Q\) | \(\varnothing,\varnothing,\{2\},\{1\}\) | \(1/660\) |

For \(P\), the isolated vertex's birth label fixes one of four encodings. For \(Q\), the three partitions of four labels into two unordered pairs fix the two chains, with the smaller label below the larger. This counts encoded orders, not permutations of interchangeable vertices. Summing gives
\[
 Q_p(P)=\frac{\alpha^2\beta^2}{198},\qquad
 Q_p(Q)=\frac{\alpha^2\beta^2}{220}.
\]
Their positive difference is \(\alpha^2\beta^2/1980\). Identical normalized payload channels therefore coexist with unequal endpoint probabilities in this very model.

### 3. What final access can distinguish

Write \(A=\mathcal C_{\varnothing,0}\), \(B=\mathcal C_{K_0,0}\). Under the theorem both endpoints have channel \(B^2A^2\). For every common initial payload/reference state \(\rho_{AR}\), their conditional states are identically
\[
 (B^2A^2\otimes\operatorname{id}_R)(\rho_{AR}).
\]
Every fixed final measurement on that state consequently has the same conditional distribution. The preparation and measurement cannot depend on which endpoint occurred. Access to the classical endpoint itself is a different information source. Mathematical conditioning here does not assert an implemented postselection experiment.

For an unselected experiment at the same fixed horizon under kernel \(p\),
\[
 \mathcal E_p=\sum_m\nu_p(m)T_m,\qquad
 \nu_p(m)=\sum_{E:m_E=m}Q_p(E).
\]
Equal profile distributions under two kernels suffice for equal channels, but a fixed family can collapse further differences between mixtures. This single endpoint collision does not establish equality of profile distributions or unselected channels under different kernels. The accepted QR-LD004 separation of its two particular kernels remains intact. No physical no-go or general order reconstruction result follows.

### 4. Only the relevant supported diamond is needed

The collision does not depend on imposing global commutation on unrelated indices. Begin with a singleton marked zero. Compare two incomparable new zero-marked births: an independent root with empty precursor (index \(A\)), and a leaf over the old root (index \(B\)). Both orders are admitted. Their structural products are
\[
 (2/3)(1/10)=(1/3)(1/5)=1/15.
\]
Their complete branch products are \((\alpha\beta/15)BA\) and \((\alpha\beta/15)AB\). The actual complete marked-diamond condition and positive coefficient force \(AB=BA\). This diamond uses only three births. All seven histories above therefore have channel \(B^2A^2\) even when only actual supported-diamond commutation is required. No broader co-realizability classification is claimed.

### 5. The explicit missing information

A distinguishing extension must access information beyond this profile. Here the missing datum is joint incidence: whether the two singleton leaf pasts refer to the same ancestor. Their intersection has size one in \(P\) and zero in \(Q\), although each separate induced past has the same class.

This identifies a design gap, not an implemented overlap test. No persistent identities, endpoint oracle, new memory/transport law, physical observer or selected dynamics are introduced. A different allowed architecture would need its own justified access premise; more precise final measurement of these identical conditional states cannot supply the missing information.

The result is an optional mathematical limitation of the stated update family. It derives neither native DET quantum dynamics nor physical measurement, Born probabilities, clock/action scales, geometry, gravity or Boundary influence.
