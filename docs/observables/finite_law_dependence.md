# A finite law family with an invariant readout distinction

**Accepted conditional theorem.** The common-scale prescription below has strictly positive full support, normalized rows, marked equivariance and every marked scalar diamond through four births exactly for
\[
0<\lambda<88/23.
\]
With the unchanged supplied pair register and its fixed empty preparation, the complete unselected output law is
\[
\boxed{p_\lambda(Y=0)=71\lambda/2640,\qquad
p_\lambda(Y=1)=1-71\lambda/2640.}
\]
Distinct admitted parameters give different probabilities for the same representation-invariant event. This establishes optional finite law dependence under the declared common interpretation. It does not select a physical law or extend the family beyond four births. The family theorem and output calculation received separate blind reconstructions and coordinator reconciliation.

## Domain, unchanged rows and the prescription

A birth adjoins a maximal vertex with full strict past equal to a chosen ideal of the current finite order. Every actual ideal occurrence is retained; existing binary marks are immutable, and each newborn bit has probability one half. The accepted reference law \(q_*\), including its complete marked diamonds and equivariance, is a dependency of this theorem.

Use the reference constants
\[
a=2/3,\ c=1/5,\ d=1/4,\ g=1/10,\ k=11/20,\ e=1/44,
\quad f_0=1/6,\ f_1=1/3,\ h_0=19/30,\ h_1=7/15.
\]
In particular \(f_i+h_i=4/5\). Leave all earlier rows unchanged:

| Parent | All ideal weights |
| --- | --- |
| Empty | Empty: 1 |
| Singleton | Empty: \(a\); full: \(1-a\) |
| Two-chain, root mark \(i\) | Empty: \(c\); root: \(f_i\); full: \(h_i\) |
| Two-antichain | Empty: \(d\); each singleton: \(g\); full: \(k\) |

For every marked three-vertex parent \((A,r)\), let \(R(A,r)\) be the sum of its proper reference slots. Define
\[
q_\lambda(A,r,S)=\lambda q_*(A,r,S)\quad(S\subsetneq A),
\qquad q_\lambda(A,r,A)=1-\lambda R(A,r).
\]
The same positive dimensionless parameter is used for all shapes and markings. Full slots are complete normalization complements, not scaled reference full slots.

In the next table, D is an edge \(u<v\) with isolate \(w\), F a fork with root \(u\) and leaves \(v,w\), J a join with minima \(u,v\) and top \(w\), and C a chain. A denotes the antichain here. Every proper coefficient shown is multiplied by \(\lambda\).

| Parent | All proper reference slots, including multiplicities | \(R\) | Full \(q_\lambda\) |
| --- | --- | --- | --- |
| A | Empty: \(1/44\); three singletons: \(1/110\) each; three pairs: \(1/20\) each | \(1/5\) | \(1-\lambda/5\) |
| D, root mark \(i\) | Empty, {w}: \(1/44\) each; {u}: \(5f_i/44\); {u,v}: \(5h_i/44\); {u,w}: \(1/8\) | \(23/88\) | \(1-23\lambda/88\) |
| F, root 0 | Empty, root: \(1/44\) each; two root-plus-leaf ideals: \(19/220\) each | \(12/55\) | \(1-12\lambda/55\) |
| F, root 1 | Empty, root: \(1/44\) each; two root-plus-leaf ideals: \(7/220\) each | \(6/55\) | \(1-6\lambda/55\) |
| J | Empty, each minimum singleton, minimum pair: \(1/44\) each | \(1/11\) | \(1-\lambda/11\) |
| C | Empty, root, initial pair: \(1/44\) each | \(3/44\) | \(1-3\lambda/44\) |

These cover every three-vertex shape and marking: only the indicated root bits affect unequal coefficients. The largest proper sum is \(23/88\). Therefore all proper and full slots are positive exactly on the stated interval, and each complete marked row sums to \(\lambda R+1-\lambda R=1\). At zero, proper support disappears. At \(88/23\), a reachable edge-plus-isolate parent's full slot vanishes; above it that slot is negative. Reachability follows by forming a chain and then using its positive empty slot. Neither boundary is admitted. At \(\lambda=1\) every row recovers the reference law.

## Marked transport and all diamonds

A marked order isomorphism bijects actual proper ideals and preserves their reference weights. It therefore preserves \(R\), the scaled slots and their full complement. No unmarked quotient is used.

Every incomparable-birth diamond ending within four births has a common base \(C\) of size zero, one or two. If its precursor ideals are \(S,T\), the second ideal \(T\) inside \(C+x_S\) excludes the new \(x\), hence is proper even when \(T=C\). The reverse path has the same property.

For base size at most one, both factors are unchanged. For base size two, exactly the second factor is a proper size-three slot, so both products acquire the same factor \(\lambda\). The accepted reference identity thus gives, for every inherited marking and both newborn bits,
\[
q_\lambda(C,r,S)q_\lambda(C+x_S,r+b,T)/4
=q_\lambda(C,r,T)q_\lambda(C+y_T,r+c,S)/4.
\]
This includes empty, full-in-base, equal, overlapping and disjoint precursors. A full size-three slot cannot be that second factor: containing the first newborn would make the two births comparable. Its normalization was nevertheless checked, and it remains available in suffixes after earlier diamonds.

## Unchanged register, references and preparation

Use the supplied [pair-incidence register](finite_pair_incidence_register.md): one five-valued cell per vertex and unordered vertex pair, with actual ideal handles and pair addressing. A birth increments each old vertex cell in its ideal and each old pair cell contained in that ideal, modulo five, then appends zero newborn coordinates. Let \(J|z\rangle=|Tz\rangle\). Inverting the retained shifts gives \(J^\dagger J=I\).

The branch Kraus operator is \(\sqrt{q_\lambda/2}J\). It is completely positive; complete rows satisfy \(\sum K^\dagger K=I\). Replacing \(J\) by \(J\otimes I_R\) preserves these statements for arbitrary finite references, including entangled intermediate inputs. This is complete-row trace preservation, not an identity-channel claim.

Actual-identity transport commutes with the updates. On an incomparable diamond, old vertex and pair increments commute, while all newborn coordinates finish at zero on either path. The isometries therefore agree exactly. Combining this with the scalar identity proves equality of the full unnormalized complex-operator maps. Covariance transports every admitted suffix through four births, including ideals containing either or both swapped newborns, before summation or normalization.

From empty preparation, vertex and pair cells count strict descendants and common strict descendants. Their maxima are three and two, so no wrapping occurs. The fixed readout is \(Y=1\) when any pair cell is nonzero; equivalently, some birth has at least two strict predecessors, which need not be incomparable. Structural tags, individual cells, histories and marks remain unavailable to the final observer.

For every natural marked history \(h\), write \(w_\lambda(h)=\prod(q_\lambda/2)\). The matched classical and quantum preparations give
\[
\mu_h=w_\lambda(h)\delta_{z_h},\qquad
\rho_h=w_\lambda(h)|z_h\rangle\langle z_h|\otimes\rho_R,
\]
with independent normalized \(\rho_R\). Their joint history/output probabilities coincide. Histories are probability blocks, not coherently summed amplitudes. This prepared equality does not simulate arbitrary quantum channels.

## Complete probability ledger

The first three births use unchanged rows. Birth one has mark masses \(1/2\); birth two has antichain and chain totals \(2/3,1/3\), with per ordered bit-pair masses \(1/6,1/12\). Below, the first ideal is empty and numbers denote birth positions. Each encoding admits all eight ordered three-bit strings.

| Three-parent | Second and third ideals | Mass per string per encoding | Total |
| --- | --- | --- | --- |
| A | empty, empty | \(ad/8=1/48\) | \(1/6\) |
| D | empty, {1}; empty, {2}; {1}, empty | \(ag/8=(1-a)c/8=1/120\) each | \(1/5\) |
| F, root \(i\) | {1}, {1} | \(f_i/24\) | \(1/12\) |
| J | empty, {1,2} | \(ak/8=11/240\) | \(11/30\) |
| C, root \(i\) | {1}, {1,2} | \(h_i/24\) | \(11/60\) |

These seven encodings exhaust the four antichain and three chain ideals. D has mass \(1/40\) per root/leaf/isolate marking, hence \(1/10\) per root bit. F root masses are \(1/36,1/18\); C root masses are \(19/180,7/90\). Total mass is one; A,D,F are untriggered with mass \(9/20\), and J,C already triggered with mass \(11/20\).

Multiplicity remains marked: for antichain mark counts \(n_0,n_1\), singleton orbit sizes are \(n_0,n_1\), and pair sizes are \(\binom{n_0}{2},n_0n_1,\binom{n_1}{2}\), totaling three each. Fork leaves or join minima form one size-two orbit when equally marked, otherwise two singleton orbits. D/C roles are distinct. Incoming encodings are already counted; no further automorphism or linear-extension factor enters.

The untriggered fourth-step survivor sums, retaining only empty/singleton ideals, are
\[
s_A=\lambda/20,\quad s_{D,0}=17\lambda/264,
\quad s_{D,1}=22\lambda/264,\quad s_F=\lambda/22.
\]
At the terminal step both newborn bits sum to the displayed slot weight. Thus D's zero contribution is \((1/10)(17+22)\lambda/264=13\lambda/880\); F's is \((1/36+1/18)\lambda/22=\lambda/264\). No mark-dependent ratio is separately averaged.

| Parent | Incoming mass | \(Y=0\) contribution | \(Y=1\) contribution |
| --- | --- | --- | --- |
| A | \(1/6\) | \(\lambda/120\) | \((20-\lambda)/120\) |
| D | \(1/5\) | \(13\lambda/880\) | \((176-13\lambda)/880\) |
| F | \(1/12\) | \(\lambda/264\) | \((22-\lambda)/264\) |
| J | \(11/30\) | 0 | \(11/30\) |
| C | \(11/60\) | 0 | \(11/60\) |

The triggering A/D/F rows include their full affine complements; already-triggered J/C retain all terminal slots. Each row conserves its incoming mass. Summing the columns gives
\[
p_0=(22+39+10)\lambda/2640,
\]
\[
p_1=[(440-22\lambda)+(528-39\lambda)+(220-10\lambda)+968+484]/2640.
\]
Their sum is one, with complete mass conserved at every depth.

An independent blind complement reconstruction pruned all precursors of size at least two without renormalizing. Its surviving-path expression agrees:
\[
C_4=ad\frac\lambda{20}+[2ag+(1-a)c]\frac{13\lambda}{176}
+\frac{1-a}{2}\sum_i f_i\frac\lambda{22}
=\frac\lambda{120}+\frac{13\lambda}{880}+\frac\lambda{264}
=\frac{71\lambda}{2640}.
\]
Each surviving fourth transition is proper and scales once. This does not scale every triggered path, whose full terminal slots are affine. Coordinator reconciliation confirmed agreement of the independent and author ledgers.

## Meaning, limits and retained qualification

At \(\lambda=1\), the reference output is \((71/2640,2569/2640)\). On the admitted interval, \(0<p_0<71/690\) and \(619/690<p_1<1\); boundary values are limits only.

Order-and-mark transport preserves precursor size, pair incidence, effects and probabilities. Thus the event is representation invariant. Different parameters give different values of \(71\lambda/2640\), so a probability-preserving coordinate change preserving this same event cannot identify those different laws. Renaming a parameter while retaining the same actual law adds no member. The conclusion supplies neither empirical identification nor a preferred parameter.

The family proof's premises file was saved after preliminary reasoning, although its exact protocol had already been separately frozen and admitted. A distinct blind reconstruction independently established the bounded theorem. Acceptance does not certify a premises-first process or repair historical custody; earlier interruption and recovery qualifications remain.

Structural supply, physical memory, routing, reset, calibration and their costs remain additional premises. No all-size extension, native physical observer, quantum advantage, efficiency, geometry or gravity follows. Scientific, review, protected-validation, custody, resource, execution and publication gates remain.
