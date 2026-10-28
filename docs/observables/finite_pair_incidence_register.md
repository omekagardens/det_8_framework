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
