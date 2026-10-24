# RI1434: Finite scale freedom and conditional sampling feasibility

This report consolidates two accepted mathematical results: RI1431's conditional one-layer affine sampling criterion and RI1433's explicit size-three boundary classification. The finite classification has 17 proper-slot orbits, 23 ideal occurrences and 11 scale blocks. That count belongs to the stated diamond, equivariance and mark-independence equations. It is **not** a proof that the full native law admits eleven independent parameters. Nor has a sampling-feasible point, a sampling-matrix rank or an all-size sampling-consistent law been established.

The useful separation is precise. First identify what the finite equations force. Then state the additional native-component premise needed to interpret those coordinates as a permitted native family. Only within a permitted family does the affine criterion decide sampling feasibility. Choosing one common scale is an additional restriction of the displayed finite equations; it is not a consequence of their classification.

## 1. Objects, fixed prefix and observation

A parent is a finite completed partial order \(P\), carrying marks \(r\). A birth with precursor ideal \(S\subseteq P\) adds a new vertex above exactly \(S\); all old completed comparisons remain. A full ideal is \(P\) itself. Distinct ideal occurrences remain distinct even when symmetry identifies their scalar values.

The scalar rows considered here are mark independent. Newborn bits are independently fair. The canonical scalar-passive transports on whole positive-semidefinite payloads are inherited premises. Neither mark independence nor those transports is derived by the unmarked sampling calculation.

Anonymous sampling means choosing a uniform vertex subset of the completed order, restricting its completed relation, and forgetting labels and marks. Comparisons already completed through deleted vertices persist. Deleting generating edges and recomputing reachability would define a different experiment. Write \(\mu_k\) for the size-\(k\) unmarked law and \(T_{n,k}\) for this uniform subset kernel. Sampling consistency means \(\mu_nT_{n,k}=\mu_k\). It is an optional mathematical constraint, not an adopted physical postulate.

The numerical classification uses exactly the accepted RI1423 prefix:
\[
q(O,O)=1,\qquad q(E_1,\varnothing)=q(E_1,E_1)=1/2,
\]
\[
q(C_2,\varnothing)=q(C_2,\{x\})=q(C_2,C_2)=1/3,
\]
\[
q(A_2,\varnothing)=q(A_2,A_2)=1/6,\qquad
q(A_2,\{x\})=q(A_2,\{y\})=1/3.
\]
Here \(O\) is empty, \(E_1\) is a singleton, \(C_2=\{x<y\}\), and \(A_2=\{x\parallel y\}\). The prefix has positive support on its marked ideal histories and the previously accepted unmarked sampling identities through size three. It fixes \(p=\mu_2(C_2)=1/2\). No arbitrary-\(p\) replacement of these numerical rows is supplied.

## 2. Complete finite boundary classification

At parent size three write the new scalar row as \(Q(P,T)\). The finite equations being classified are transported order equivariance, the declared mark independence, and every commuting two-birth diamond with size-two base \(B\):
\[
q(B,S)Q(B+S,T)=q(B,T)Q(B+T,S). \tag{D}
\]
Both \(S\) and \(T\) run over all old ideal occurrences, including equal and full ideals. Second precursors exclude the other newborn and are therefore proper in the size-three parent. New full entries do not occur as second factors; old full first factors do occur and must retain their displayed values. Comparable newborns have no legal reversed order and do not add commuting diamonds.

Every proper slot appears in this boundary. For proper ideal \(T\) of a size-three order \(P\), choose a maximal vertex \(z\) outside \(T\). Such a vertex exists because an upward chain starting outside an ideal cannot end inside it. Then \(B=P\setminus\{z\}\), \(S=\operatorname{Past}_P(z)\), and \(P=B+S\), while \(T\) is still an ideal of \(B\).

Use the five parent types
\[
A:\text{three-antichain};\quad
E:x<y,\ z\text{ isolated};\quad
V:x<y,\ x<z;\quad W:x<z,\ y<z;\quad C:x<y<z.
\]
These exhaust the three-element order types: zero, one, two or three completed comparisons give the listed possibilities, with the two-comparison cases distinguished by orientation.

For each proper slot use the positive maximal-deletion coordinate
\[
u(P,T)=
\prod_{\varnothing\ne H\subseteq\operatorname{Max}(P)\setminus T}
q(P\setminus H,T)^{(-1)^{|H|+1}}. \tag{U}
\]
Restricted marks are retained, although these prefix scalars ignore them. Every repeated deletion factor and smaller full-ideal value is included. Write \(Q(P,T)=u(P,T)a_c\) on block \(c\).

| Parent | Proper ideal representative | Occurrences | \(u\) | Block |
|---|---|---:|---:|---:|
| \(A\) | \(\varnothing\) | 1 | \(1/27\) | 1 |
| \(A\) | one vertex | 3 | \(2/9\) | 2 |
| \(A\) | two vertices | 3 | \(1/6\) | 3 |
| \(E\) | \(\varnothing\) | 1 | \(1/9\) | 2 |
| \(E\) | \(\{x\}\) | 1 | \(2/9\) | 4 |
| \(E\) | \(\{z\}\) | 1 | \(1/3\) | 5 |
| \(E\) | \(\{x,y\}\) | 1 | \(1/3\) | 6 |
| \(E\) | \(\{x,z\}\) | 1 | \(1/6\) | 7 |
| \(V\) | \(\varnothing\) | 1 | \(2/9\) | 4 |
| \(V\) | \(\{x\}\) | 1 | \(2/9\) | 8 |
| \(V\) | \(\{x,y\}\) | 2 | \(1/3\) | 9 |
| \(W\) | \(\varnothing\) | 1 | \(1/6\) | 3 |
| \(W\) | \(\{x\}\) | 2 | \(1/3\) | 7 |
| \(W\) | \(\{x,y\}\) | 1 | \(1/6\) | 10 |
| \(C\) | \(\varnothing\) | 1 | \(1/3\) | 6 |
| \(C\) | \(\{x\}\) | 1 | \(1/3\) | 9 |
| \(C\) | \(\{x,y\}\) | 1 | \(1/3\) | 11 |

Multiplicity counts actual ideals in one parent, not an extra factor on an individual transition. The occurrence counts \(7,5,4,4,3\) total 23; the orbit counts \(3,5,3,3,3\) total 17.

For completeness, the potentials follow directly from the complete prefix. In \(A\), the empty slot gives \((1/6)^3/(1/2)^3=1/27\), with the triple-deletion empty-parent factor equal to one. A singleton gives \((1/3)^2/(1/2)=2/9\); a pair gives the smaller full value \(1/6\). In \(E\), empty gives \((1/6)(1/3)/(1/2)=1/9\), and bottom gives \((1/3)^2/(1/2)=2/9\). Its other slots have one allowed maximal deletion. In \(V\), empty and bottom each give \(2/9\), and either two-vertex ideal gives \(1/3\). In \(W\) and \(C\), deleting the unique top gives the complete \(A_2\) and \(C_2\) rows, including their full entries.

Here is the entire edge certificate. Reversing an off-diagonal pair gives the same equation, while diagonal pairs are retained. For chain base \(B=C_2\), denote its ideals by \(0=\varnothing,a=\{x\},f=B\). All first factors are \(1/3\).

| Unordered pair | Equation after canceling the common first factor |
|---|---|
| \(0,0\) | \(Q_{E,\varnothing}=Q_{E,\varnothing}\) |
| \(0,a\) | \(Q_{E,\{x\}}=Q_{V,\varnothing}\) |
| \(0,f\) | \(Q_{E,\{x,y\}}=Q_{C,\varnothing}\) |
| \(a,a\) | \(Q_{V,\{x\}}=Q_{V,\{x\}}\) |
| \(a,f\) | \(Q_{V,\{x,y\}}=Q_{C,\{x\}}\) |
| \(f,f\) | \(Q_{C,\{x,y\}}=Q_{C,\{x,y\}}\) |

These six unordered cases represent all nine ordered cases. For antichain base \(A_2\), the ideals \(0,x,y,f\) have first factors \(1/6,1/3,1/3,1/6\).

| Unordered pair | Equation with its actual first-factor ratio |
|---|---|
| \(0,0\) | \(Q_{A,\varnothing}=Q_{A,\varnothing}\) |
| \(0,x\), \(0,y\) | \(Q_{A,\mathrm{one}}=2Q_{E,\varnothing}\) |
| \(0,f\) | \(Q_{A,\mathrm{two}}=Q_{W,\varnothing}\) |
| \(x,x\), \(y,y\) | \(Q_{E,\{x\}}=Q_{E,\{x\}}\) |
| \(x,y\) | \(Q_{E,\{z\}}=Q_{E,\{z\}}\), after transported swap |
| \(x,f\), \(y,f\) | \(Q_{W,\mathrm{one\ bottom}}=2Q_{E,\{x,z\}}\) |
| \(f,f\) | \(Q_{W,\{x,y\}}=Q_{W,\{x,y\}}\) |

The grouped rows represent ten unordered and all sixteen ordered cases. For example,
\((1/6)Q_{A,\mathrm{one}}=(1/3)Q_{E,\varnothing}\), whereas
\((1/3)Q_{E,\{x,z\}}=(1/6)Q_{W,\mathrm{one\ bottom}}\).
Equating the unscaled entries in these cases would be incorrect.

After dividing by \(u\), the six distinct non-loop edges are
\[
(A,\mathrm{one})-(E,\varnothing),\quad
(A,\mathrm{two})-(W,\varnothing),\quad
(E,\{x\})-(V,\varnothing),
\]
\[
(E,\{x,y\})-(C,\varnothing),\quad
(E,\{x,z\})-(W,\mathrm{one\ bottom}),\quad
(V,\mathrm{two})-(C,\{x\}).
\]
They are six disjoint pairs. The five isolated vertices are
\((A,\varnothing),(E,\{z\}),(V,\{x\}),(W,\{x,y\}),(C,\{x,y\})\).
Thus the explicit graph has eleven connected blocks. This conclusion uses the complete edge list, not a subtraction of equation counts or an unperformed rank computation.

For each fixed old marking and newborn bits \(b,c\), both sides of a diamond receive the same \(1/4\) factor. Declared mark independence handles unequal marks as well as equal ones; it is not inferred from an automorphism of a marked order. Under the retained canonical scalar-passive transport premise, equal scalar coefficients multiply the whole transported PSD payload. The conclusion is therefore not merely a trace equality.

Necessity follows from the edges. Conversely, assigning one scale to each displayed block satisfies every edge, loop and transported copy; boundary coverage supplies all new diamonds in this finite class. Complete positivity is exactly \(a_c>0\) and
\[
\begin{aligned}
K_A(a)&=a_1/27+2a_2/3+a_3/2<1,\\
K_E(a)&=a_2/9+2a_4/9+a_5/3+a_6/3+a_7/6<1,\\
K_V(a)&=2a_4/9+2a_8/9+2a_9/3<1,\\
K_W(a)&=a_3/6+2a_7/3+a_{10}/6<1,\\
K_C(a)&=(a_6+a_9+a_{11})/3<1.
\end{aligned} \tag{P}
\]
Set \(Q(P,P)=1-K_P(a)\). These full complements normalize the rows and impose inequalities, not extra equality edges. They enter a later boundary that has not been classified here.

The finite positivity domain is nonempty and open: set all scales to a sufficiently small common positive value. Perturbing only \(a_1\) slightly preserves these strict inequalities and all displayed ties while breaking common scaling. It changes a supported complete-history transition, but need not change a particular unmarked observable. This is a finite-equation witness only; it proves neither native admission nor sampling consistency.

## 3. The native identification that is still missing

The unresolved bridge is:

> H: At this fixed prefix and size-three layer, the native ratio components are precisely the eleven displayed blocks, with no additional scale restriction beyond complete positivity and the retained payload premises.

The inherited ratio-component sufficiency statements do not supply the native generators or prove that the displayed diamond, equivariance and mark ties exhaust them. If actual native relations merge blocks, those merges must be imposed. If further restrictions remain, they must be stated and checked; they cannot simply be assumed absent or linear.

Consequently eleven independent scales have been classified for the explicit finite conditions, not established as eleven permitted native dimensions. The common-layer recipe remains an inherited construction under its own admission and transport premises. Its common-scale restriction is optional relative to the displayed finite equations; this does not establish native freedom to make every non-common perturbation.

Under H, the table supplies a permitted eleven-coordinate family for the following theorem. Without H, the affine algebra can still describe a declared finite transition family, but cannot certify it as native.

## 4. Conditional affine sampling theorem

Fix \(n\ge2\), a strictly positive admitted prefix through parent size \(n-1\), its actual marked-parent distribution \(\eta_n(x)\), \(x=(P,r)\), and all unmarked sampling identities through size \(n\). Let \(p=\mu_2(C_2)\in(0,1)\). This notation allows a separately fixed prefix in the general theorem; the explicit numerical prefix above still has only \(p=1/2\).

For each proper ideal occurrence \(i=(x,S)\), retain its fixed finite potential \(u_i>0\). Suppose a **permitted** partition \(c(i)\in\{1,\ldots,d\}\) into nonempty blocks respects all required equivariance and mark ties. Independent positive block scales with positive full complements must be allowed by the inherited native sufficiency premise; this is a hypothesis, not the conclusion of linear algebra.

Define
\[
K_{x,c}=\sum_{\substack{S\subsetneq P\\c(x,S)=c}}u_{x,S},\qquad
q_a(x,S)=u_{x,S}a_{c(x,S)},\qquad q_a(x,P)=1-K_xa.
\]
Every complete row is strictly positive precisely on
\[
\mathcal D=\{a:a_c>0\text{ for every }c,\ K_xa<1\text{ for every }x\}. \tag{4}
\]
Parents not encountered in one realization are included. A block can be absent from one row, but is nonempty somewhere in the complete layer.

For \(2\le k\le n\), unmarked \(k\)-type \(t\), and every ideal including full, define the fixed branch kernel
\[
R_{x,S}^{k,t}=
\frac{1}{2\binom n{k-1}}
\sum_{b\in\{0,1\}}\sum_{\substack{U\subseteq P\\|U|=k-1}}
\mathbf1\{[(P+_Sv)[U\cup\{v\}]]=t\}.
\]
The fair-bit sum is harmless after marks are forgotten but retains the correct normalization. The newborn is above \(S\cap U\) in the restricted completed order. Each branch kernel is a probability vector.

Set
\[
v^0_{k,t}=\sum_x\eta_n(x)R_{x,P}^{k,t},\qquad
A_{(k,t),c}=\sum_x\eta_n(x)
\sum_{\substack{S\subsetneq P\\c(x,S)=c}}
u_{x,S}(R_{x,S}^{k,t}-R_{x,P}^{k,t}).
\]
Here the matrix \(A\) is unrelated to the parent symbol \(A\) for the three-antichain. Actual history probabilities \(\eta_n\), not uniform order-type weights, define its entries. Substituting the full complement proves the exact identity
\[
\begin{aligned}
\nu_{n,k}(t)
&=\sum_x\eta_n(x)\left[(1-K_xa)R_{x,P}^{k,t}
+\sum_{S\subsetneq P}u_{x,S}a_{c(x,S)}R_{x,S}^{k,t}\right]\\
&=v^0_{k,t}+(Aa)_{k,t}. \tag{5}
\end{aligned}
\]
The full-branch subtraction in each coefficient is essential. The algebraic baseline \(a=0\) is normalized full birth, but is not a strictly positive candidate. For each \(k\), the coordinates of \(v^0\) sum to one and each column of \(A\) sums to zero.

A uniform \(k\)-subset of the \(n+1\) completed vertices excludes the newborn with probability \((n+1-k)/(n+1)\). Hence
\[
\mu_{n+1}T_{n+1,k}
=\frac{n+1-k}{n+1}\mu_nT_{n,k}
+\frac{k}{n+1}\nu_{n,k}.
\]
Under prior consistency, extension to size \(n+1\) is equivalent to \(\nu_{n,k}=\mu_k\) for every \(2\le k\le n\). Singleton and full-size identities are automatic. With \(b_{k,t}=\mu_k(t)-v^0_{k,t}\), the exact criterion is
\[
\boxed{Aa=b,\qquad a_c>0,\qquad K_xa<1\quad\text{for every }x.} \tag{6}
\]
Necessity follows by substitution. Conversely, a solution gives complete positive normalized rows, every required newborn identity, and therefore the next sampling identities. Native admission additionally needs the permitted-partition and transport premises. Without prior consistency, old and newborn discrepancies could offset, so the same induction claim would not follow.

All coefficients are fixed by the prefix. Earlier rows cannot be varied while treating \(\eta_n,u,\mu_k\) as constants. Equation (6) is a finite conditional feasibility criterion, not a proof of nonemptiness.

## 5. Strict positivity, floors and uniqueness

Without prescribed floors, suppose \(a^*\in\mathcal D\) satisfies \(Aa=b\). The equality solutions are \(a^*+\ker A\). Finitely many strict positive slacks permit sufficiently small motion of either sign along any nonzero vector in \(\ker A\). Therefore, **after feasibility is established**,
\[
a^*\text{ is unique}\ \Longleftrightarrow\ \ker A=\{0\}
\ \Longleftrightarrow\ \operatorname{rank}A=d. \tag{7}
\]
Full column rank does not establish existence or positivity. Listed motif equations include normalization redundancies, so their count is not a rank result.

For fixed positive coordinate floors add
\[
u_i a_{c(i)}\ge\ell_i,\qquad 1-K_xa\ge\ell_{x,P}.
\]
The floors are prescribed data and are not lowered to obtain feasibility. Write them as \(Ga\ge g\), with active row set \(J\) at a feasible \(a^*\). The exact uniqueness condition becomes
\[
\boxed{\ker A\cap\{v:G_jv\ge0\text{ for every }j\in J\}=\{0\}.} \tag{8}
\]
Another feasible point supplies a nonzero difference in that intersection. Conversely, a nonzero such vector permits a sufficiently small positive step: active inequalities do not decrease and all inactive floor and strict positivity slacks persist. This is a one-sided test. At an interior floor point it reduces to (7); at a boundary, rank deficiency alone does not imply alternatives. For instance \(x+y=2,\ x,y\ge1\) has only one point despite a nontrivial equality nullspace; this is an abstract illustration, not a native example.

Since every block has a proper slot with \(u_i>0\), distinct scale vectors change a transition entry. With positive finite-history coverage they change a complete-history law. They need not change the constrained motifs or the unmarked terminal law. No actual native rank, nullspace or alternative sampling solution is asserted here.

## 6. What a common scale does and does not decide

A newborn-containing pair is a chain with conditional probability \(|S|/n\); full birth gives one. Put
\[
D_c=\sum_x\eta_n(x)\sum_{\substack{S\subsetneq P\\c(x,S)=c}}
(n-|S|)u_{x,S},\qquad D=\sum_cD_c>0.
\]
Each \(D_c\ge0\), and the positive empty ideal in a positive parent makes \(D>0\). The pair-chain row of \(A\) is \(-D_c/n\). Its exact unconditional equation is
\[
\sum_cD_ca_c=n(1-p). \tag{9}
\]
It is not a separate requirement for each parent, and it is only one of the motif equations.

On the optional common line \(a=\alpha\mathbf1\), the pair equation forces
\[
\alpha^*=\frac{n(1-p)}D>0.
\]
Writing \(h=A\mathbf1\), every remaining row must satisfy \(b_{k,t}=\alpha^*h_{k,t}\). A zero entry of \(h\) requires zero target; nonzero entries require the same forced ratio. Strict positivity requires
\[
\alpha^*\max_x\sum_cK_{x,c}<1,
\]
and any fixed floors must also hold. There is no spare common parameter to repair an incompatible higher motif. This proves at most one candidate on that line, not general native uniqueness.

At the explicit size-three layer, prior consistency is available and both \(k=2\) and \(k=3\) matter. Under H, use the eleven coordinates and five loads above; otherwise first establish the actual permitted family. No sampling matrix for that layer, its rank, a positive sampling-feasible point or a non-common sampling solution has been computed. In particular the open finite diamond domain in section 2 is not a sampling-feasibility witness.

## 7. Pinned intake status of the other tracks

The following are the accepted intake dispositions supplied for this documentation checkpoint. They are not a claim about later evolving research, and no pending F006 or QR successor result enters this report.

- **E-F005:** a conditional compositional range template is accepted. The retained core time and cost, augmented by independently justified finite event/count/cost/latency caps, can give gross nonnegative whole-request energy/time ranges, including failures and cleanup. The event grammar and service amendments remain prospective. Numerical caps, a closed controller and ledger profile, adoption, continuous service, comparator competence, numerical validation, custody and execution admission remain absent.
- **NE-F005:** a conditional uniform exponential error certificate is accepted for externally certified complete-row total-variation budgets, fixed oriented control and fixed iid sampling. With \(t=e_- -e_+\) and \(h=0.1-e_+-e_->0\), maximum conditional error is at most \(\exp(-Nh^2/2)\); inherited radii are clipped at one. Common marginal rows alone do not establish iid. Target-independent orientation, calibration, complete record registration, reset/sampler certification, physical cost and execution contracts remain missing.
- **CE-F005:** the conditional four-menu comparison is accepted: \(I_0\) weakly dominates \(I_1\) on a matched trace, while \(F_0,F_1,I_0\) each have unique-optimum nonnegative-weight witnesses. Correlated outcomes remain in the exact regions. No implementation/runtime/RSS enforcer, justified primitive prices or DET-distinct third mechanism is admitted; M1 remains unadmitted. There is no physical winner or benchmark claim.
- **M-F005:** newly retained source contexts are accepted for limited documentary correspondence only. Both structure-header requests remain missing. Source/build/ABI/helper/caller/parser/image binding, qualification, controls and observed execution remain on HOLD. Missing original M-F004 response bodies remain a historical custody gap; new retrieval does not reconstruct them or qualify a platform.

## 8. Evidence and remaining programme

The scientific content here is the two accepted manual results and their distinct reviews. The complete finite tables are reproduced so that the classification can be assessed without chronological packet summaries. Fresh packaging checks establish exact source identities, safe archive structure and full byte preservation of the copied baseline fronts. Such checks do not independently authenticate old provider receipts or repair historical inspection order.

Earlier custody, guard, helper, schema, display and size-cap failures remain recorded. Missing RI1389 evidence, RI1401 late freeze and RI1419 late readback remain unresolved historical qualifications. Attributed author completion times remain distinct from original tool bodies and present identity checks. Current mathematical acceptance is not retrospective process certification. Protected validation, freeze/custody prerequisites, Option B/Status M, ABSTAIN, zero qualification and the RET-only pause remain in force.

The next native issue is source-supported identification and completeness of the actual ratio/locality generators, especially H. It is open; no successor answer is adopted here. One-layer feasibility is not all-horizon feasibility or an all-size law. Neither theorem selects a physical \(p\), derives informative quantum dynamics or geometry, gravity or mass, supplies an empirical forward map, or authorizes execution.

This checkpoint adds documentation only. The four coordinator fronts retain their entire old suffixes; the report and its nonself manifest are new public paths. Publication still requires distinct review, root acceptance and root checks of the live repository, exact index scope, ancestry and remote result. Main integration is merge-only.
