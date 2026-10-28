# A finite pair-incidence register theorem

Independently reviewed and coordinator-accepted at the conditional scope stated here. A separate protocol preceded the proof. This statement adds a supplied pair register to the finite incidence construction; it establishes neither a native physical observation channel nor quantum advantage.

**Result.** Through four births, the prescribed vertex-and-pair register satisfies complete positivity, complete-row trace preservation, relabeling covariance, every supported marked diamond, arbitrary-reference extension and transported suffix consistency. From empty preparation, its pair counters record common strict descendants. One fixed binary readout separates the join-plus-isolate endpoint from two disjoint chains, although their vertex-counter states coincide. An ordinary classical register has exactly the same prepared joint history/output law.

## Fixed law, support and additional premises

Use exactly the positive marked growth law and parent-size-zero-through-three rows printed in Section 1 of the [finite incidence-register theorem](finite_incidence_register.md). Its normalization, full ideal support, equivariance and complete marked scalar diamonds are inherited admitted premises. Each newborn bit is fair; existing marks are immutable. Every labeled ideal occurrence and both bits remain in the successor row. No seed, coefficient, support or horizon is changed.

For a parent order A, write P(A) for its unordered pairs of distinct vertices and set
\[
H_A=\bigotimes_{v\in A}\mathbb C^5_v\otimes
\bigotimes_{p\in P(A)}\mathbb C^5_p,
\qquad H_\varnothing=\mathbb C.
\]
Vertex and pair coordinates are separately typed. The controller is supplied actual ideal handles S, the complete old-handle roster and unique pair-key addressing. For z=(c_v,d_p), the update T_(S,x) increments c_v modulo five when v belongs to S, increments d_p when both endpoints belong to S, then appends a zero newborn vertex and zero pairs joining x to every old vertex. Updates are lossless, with no intermediate measurement, reset or feedback into the growth law.

Define J_(S,x)|z>=|T_(S,x)z>. For newborn bit b, the branch map is
\[
\mathcal B_{S,b}(X)=\frac{q(A,r,S)}2J_{S,x}XJ_{S,x}^{\dagger}.
\]
The complete instrument uses orthogonal structural-successor sectors. Those tags, individual cells, histories, marks and informative names are unavailable to the final observer. The operational preparation is empty memory with an independent normalized reference state. Only the prescribed final bit is exposed. These memory, routing, preparation and readout capabilities are supplied assumptions.

## Maps, complete rows and reference systems

Subtracting the fixed modular increments from the retained old coordinates recovers the input configuration. Appending zeros therefore makes T injective and J an isometry. Each branch has Kraus operator K_(S,b)=sqrt(q/2)J, so it is completely positive and
\[
\operatorname{Tr}\mathcal B_{S,b}(X)=\frac q2\operatorname{Tr}X,
\qquad
\sum_{S,b}K_{S,b}^{\dagger}K_{S,b}
=\sum_Sq(A,r,S)I=I.
\]
Orthogonal successor inclusions preserve this completeness relation. The complete row is trace preserving; it is not an identity channel on a fixed carrier. Replacing J by J tensor I_R proves the same statements for every finite reference, including arbitrary entangled intermediate inputs. A history h retains the unaltered weight w(h)=product(q/2).

## Transport, marked diamonds and suffixes

An order-and-mark isomorphism phi transports v to phi(v) and {u,v} to {phi(u),phi(v)}. Membership, pair containment and zero allocation commute with that transport. Thus
\[
U_{\phi+x}J_{S,x}=J_{\phi S,\phi x}U_\phi.
\]
Together with q equivariance this proves branch covariance.

For incomparable births x,y over a common base C with precursor ideals S,T, neither newborn belongs to the other's precursor. After matching actual terminal identities, both birth orders give:

| Coordinate | Result from arbitrary old configuration |
| --- | --- |
| Old vertex v | c_v + 1_(v in S) + 1_(v in T), modulo five |
| Old pair p | d_p + 1_(p contained in S) + 1_(p contained in T), modulo five |
| New vertices x,y | zero |
| Pairs {v,x}, {v,y}, v in C | zero |
| Pair {x,y} | zero |

An old/new pair allocated first cannot be incremented by the second birth because the first newborn is outside that precursor. In the reverse order it is appended zero on the second step. The newborn pair is appended zero in either order. Old-coordinate additions commute, including equal or overlapping ideals. The composed isometries therefore agree exactly, without a phase ambiguity. Equality extends to all matrix units, complex operators and reference systems.

The inherited marked scalar identity is
\[
q(C,r,S)q(C+x_S,r+b,T)/4
=q(C,r,T)q(C+y_T,r+c,S)/4.
\]
Hence the full unnormalized branch maps agree for every old marking and both newborn bits. Empty, full, equal and overlapping precursors are included. Repeated covariance transports every subsequent ideal and coordinate, including suffix ideals containing either or both newborns. Equality persists branchwise and under complete suffix sums within the horizon.

## Prepared counts and the fixed readout

At terminal order B, empty preparation gives
\[
c_B(v)=\#\{w:v\prec w\}\pmod5,
\qquad
d_B(\{u,v\})=\#\{w:u\prec w,\ v\prec w\}\pmod5.
\]
Each vertex increments exactly at its later strict descendants. A pair is allocated when its second endpoint is born; every common strict descendant must be later, so none is lost. The pair increments exactly at those common descendants. At four births the respective maxima are three and two, so neither count wraps. Every history ending at B yields the same transported normalized basis state |z_B><z_B| tensor rho_R.

The fixed effects are
\[
E_0=I_{\mathrm{vertices}}\otimes
\bigotimes_{p\in P(B)}|0\rangle\langle0|_p,
\qquad E_1=I-E_0,
\]
with identity action on the reference. They are positive complementary projections. Pair permutations preserve their product. Coarse-graining local pair-zero tests into the bit “any pair is nonzero” gives these effect probabilities without exposing individual results.

Let E have a<c and b<c, with d isolated; let F have a'<c' and b'<d', with no other strict relations. Give all vertices mark zero. Both endpoints have positive support under the unchanged admitted law. Their vertex counts are (1,1,0,0), so the vertex-only prepared states coincide under a factor matching. The orders differ: E has a vertex with two strict predecessors and F does not.

In E, precisely {a,b} has the common strict descendant c. No pair in F has a common strict descendant. Therefore
\[
\Pr(Y=1\mid E)=1,\qquad\Pr(Y=1\mid F)=0.
\]
The vertex-only collision remains; the distinction uses the added pair memory. The readout is the same for both endpoints. Mathematical conditioning supplies no operational postselection apparatus. No equality of endpoint masses or value of the unselected output probability is asserted.

## Classical equality and exact abstract charges

Give the classical comparator the same five-valued cells, handles, updates, branch weights and readout. Induction on every natural marked history gives
\[
\mu_h=w(h)\delta_{z_h},\qquad
\rho_h=w(h)|z_h\rangle\langle z_h|\otimes\rho_R.
\]
If f(z) is the pair-nonzero bit, then
\[
p_C(h,y)=w(h)\mathbf1_{\{y=f(z_h)\}}=p_Q(h,y).
\]
The complete classical row normalizes because every branch has one successor configuration and the full q row sums to one. Histories are instrument records, summed as probabilities or blocks, not coherently as vectors. Relabeling transports the updates and leaves f invariant. Any common grouping of histories preserves equality with every natural multiplicity. This does not simulate arbitrary-input quantum channels.

At size n the register has n+binomial(n,2) cells, n handles and binomial(n,2) pair keys, each containing two handle references. At four births that is ten five-level cells, four handles, six keys and twelve references. Quantum dimension and classical formal configuration count are both 5^10; this is neither equal usable information capacity nor a reachable-state count.

A birth with n old vertices and m ideal members charges one new handle, 1+n allocations/zero initializations, n pair-key creations, m vertex increments and binomial(m,2) pair increments. Each pair increment also charges one pair generation and one key lookup. Across four births the totals are ten allocations, six key creations, four handles, at most six vertex increments and at most four pair increments/generations/lookups. E uses two vertex and one pair increment; F uses two vertex and none. Both pay all allocations and the final six pair-zero tests and five binary OR operations.

These matched abstract charges establish no measured time, memory advantage, energy saving or optimality. Supplying q, ideals and the roster, physical routing/storage, synchronization, calibration, reset and fault control remain uncosted, not free.

No minimality, universal order reconstruction, quantum necessity, native quantum mechanics, physical observer, geometry or gravity follows. Calibration, protected validation, custody, independent review, resource and execution gates remain. Historical interruption, incomplete original wrap and earlier process qualifications are retained in the private evidence; the later recovery and review do not reconstruct that history. This public derivative supplies the mathematical statement, not an executable or custody-replay package.

## Accepted unselected four-birth output probability

A subsequent calculation, independently reconstructed and reconciled by the coordinator, establishes
\[
\boxed{\Pr(Y=0)=\frac{71}{2640},\qquad
\Pr(Y=1)=\frac{2569}{2640}.}
\]
This section supersedes the earlier statement that no unselected output probability is asserted, solely for the fixed law, four births, empty preparation and supplied pair readout above. All ideal occurrences and both newborn marks are retained. The original conditional theorem and its implementation limitations remain unchanged.

Here \(Y=1\) precisely when some birth's full strict past contains at least two vertices: that birth increments a pair counter, and no counter wraps at this horizon. Those predecessors need not be incomparable. No endpoint selection or renormalization is used.

### Fixed rows and complete prefix ledger

For convenience, restate the coefficients of the [fixed incidence law](finite_incidence_register.md):
\[
a=2/3,\ c=1/5,\ d=1/4,\ g=1/10,\ k=11/20,\ e=1/44,
\]
\[
f_0=1/6,\ f_1=1/3,\ h_0=19/30,\ h_1=7/15;
\qquad f_i+h_i=4/5.
\]
The empty row is one; singleton empty/full weights are \(a,1-a\). Two-chain empty/root/full weights are \(c,f_i,h_i\), with root mark \(i\); two-antichain empty/singleton/singleton/full weights are \(d,g,g,k\). Every birth bit has probability \(1/2\), so each natural marked history has weight \(\prod(q/2)\).

Let A, D, F, J and C denote the three-vertex antichain, edge plus isolate, fork, join and chain. These ledger letters do not rename the four-vertex endpoint contrast above. Birth positions label the ideals below; the first ideal is empty. Every displayed encoding admits all eight ordered three-bit strings.

| Parent | Second and third ideals | Weight per bit string per encoding | Total mass |
| --- | --- | --- | --- |
| A | empty, empty | \(ad/8=1/48\) | \(1/6\) |
| D | empty, {1}; empty, {2}; {1}, empty | \(ag/8=(1-a)c/8=1/120\), each | \(1/5\) |
| F, root mark \(i\) | {1}, {1} | \(f_i/24\) | \(1/12\) |
| J | empty, {1,2} | \(ak/8=11/240\) | \(11/30\) |
| C, root mark \(i\) | {1}, {1,2} | \(h_i/24\) | \(11/60\) |

This exhausts the empty, singleton and full alternatives in the two-parent rows. At depth two, each ordered bit pair has antichain mass \(1/6\) and chain mass \(1/12\), totaling \(2/3\) and \(1/3\).

For D, each fixed root/leaf/isolate marking has three natural encodings of mass \(1/120\), hence mass \(1/40\). Four such assignments per root mark give \(1/10\) each. For F, root-mark masses are \(f_i/6\), namely \(1/36,1/18\); for C they are \(h_i/6\), namely \(19/180,7/90\). Incoming mark dependence is retained.

The five parent masses sum to one. A, D and F are untriggered, totaling \(9/20\); J and C are already triggered, totaling \(11/20\). Complete mass is one at every depth through three.

### Complete fourth rows and marked multiplicities

In D write \(u<v\) with isolate \(w\); in F, root \(u\) has leaves \(v,w\); in J, minima \(u,v\) lie below \(w\).

| Parent | Every proper ideal and its weight | Full ideal weight |
| --- | --- | --- |
| A | empty: \(1/44\); each of three singletons: \(1/110\); each of three pairs: \(1/20\) | \(4/5\) |
| D, root mark \(i\) | empty, {w}: \(1/44\) each; {u}: \(5f_i/44\); {u,v}: \(5h_i/44\); {u,w}: \(1/8\) | \(65/88\) |
| F, root mark \(i\) | empty, {u}: \(1/44\) each; {u,v}, {u,w}: \(h_i/(44f_i)\) each | \(43/55\) for 0; \(49/55\) for 1 |
| J | empty, {u}, {v}, {u,v}: \(1/44\) each | \(10/11\) |
| C | empty, root, initial pair: \(1/44\) each | \(41/44\) |

The fork pair slots are \(19/220,7/220\) for root marks 0,1. Proper-slot sums are respectively \(1/5,23/88,12/55\) or \(6/55,1/11,3/44\). Thus every entry is positive and every complete row sums to one. At this terminal step the unused newborn bit sums as \(q/2+q/2=q\).

These are actual ideal occurrences, not an unmarked quotient. For an A parent with mark counts \(n_0,n_1\), singleton orbit sizes are \(n_0,n_1\), while pair orbit sizes are \(\binom{n_0}{2},n_0n_1,\binom{n_1}{2}\): each total is three. Exchangeable fork leaves or join minima form one size-two orbit when their marks agree, and two size-one orbits otherwise; their corresponding slot weights agree. D and C have distinct roles. Incoming mass already includes all natural-history multiplicities, so no extra automorphism, labeling or linear-extension factor is applied.

### Terminal probabilities and independent complement

For untriggered parents, summing exactly the empty and singleton ideals gives
\[
R_A=1/20,\quad R_{D,0}=17/264,\quad
R_{D,1}=22/264=1/12,\quad R_F=1/22.
\]
Thus D contributes \((1/10)(17/264)+(1/10)(22/264)=13/880\) to zero, and F contributes \((1/36+1/18)/22=1/264\). No mark-dependent ratio is averaged separately from its incoming weight.

| Parent | Incoming mass | Contribution to \(Y=0\) | Contribution to \(Y=1\) |
| --- | --- | --- | --- |
| A | \(1/6\) | \(1/120\) | \(19/120\) |
| D | \(1/5\) | \(13/880\) | \(163/880\) |
| F | \(1/12\) | \(1/264\) | \(7/88\) |
| J | \(11/30\) | 0 | \(11/30\) |
| C | \(11/60\) | 0 | \(11/60\) |

Each row conserves its incoming mass. The two column sums are
\[
p_0=(22+39+10)/2640=71/2640,
\]
\[
p_1=(418+489+210+968+484)/2640=2569/2640.
\]
They are nonnegative and sum to one, completing depth-four normalization.

A distinct reviewer independently reconstructed the complement without accessing the author ledger. Removing every transition with an ideal of size at least two, without renormalizing, retains only the A, D and F routes. With \(\overline R_D=(17/264+22/264)/2=13/176\), the surviving-path expression is
\[
C_4=adR_A+[2ag+(1-a)c]\overline R_D
+\frac{1-a}{2}\sum_{i=0}^1 f_iR_F
=\frac1{120}+\frac{13}{880}+\frac1{264}=\frac{71}{2640}.
\]
The independent reconstruction also retained the triggered third-birth mass \(11/20\) and the new fourth-birth contributions, recovering \(2569/2640\). Coordinator reconciliation found agreement with the full ledger, including marked multiplicities and complete-row conservation.

These fractions transfer to the prescribed classical and quantum preparations by the joint-law equality already proved above. They identify neither a physical observation probability nor a growth law, and establish no quantum advantage, efficiency, geometry or gravity result. Supplying the structural law, ideal handles, routing, memory, reset and calibrated readout remains an additional requirement; all review, custody, calibration, resource and execution gates remain.
