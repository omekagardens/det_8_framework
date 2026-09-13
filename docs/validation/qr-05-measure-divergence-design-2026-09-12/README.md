# QR-05: supplied measure, divergence and exact moments

12 September 2026 (Pacific/Honolulu). **Analytical design only.** No new
mathematical executor, fixture enumeration, test suite, simulation or acquired
data is produced by this gate. Section 8 specifies a prospective verification,
not an executed result. See the [decision record](RESULTS.md).

This standalone finite calculus requires no DET ontology. It follows the
[causal-operator verification](../qr-05-causal-operator-verification-2026-09-12/RESULTS.md)
and addresses the selected-operator moment error in the
[concurrent-branch geometry audit](../qr-05-bridge-reconciliation-2026-09-12/AUDIT_GEOMETRY.md).
The object here is a supplied undirected weighted graph, NOT the previous
strict causal order. Neither construction selects a physical wave operator.

## 1. Supplied objects and sign conventions

Let V={0,...,n−1}, n≥1, be labelled nodes of a finite simple undirected graph.
For bookkeeping choose a tail and head for each edge; no self-loops or repeated
undirected edges are admitted. Zero-conductance edges are allowed and retained.
The incidence matrix B has one row per edge, with −1 at its tail and +1 at
its head. This orientation is not temporal or causal orientation.

Supply node measures μ_i>0, edge conductances k_e≥0, and coordinate marks
x_i∈R^p. The coordinates are inputs, not an embedding recovered from the graph.
Set

```text
W = diag(μ_i),       K = diag(k_e),
ℒ = Bᵀ K B,         Q = −W⁻¹ ℒ.
```

For unjoined distinct nodes write k_ij=0; otherwise k_ij=k_ji is their edge
conductance. Thus

```text
Q_ij = k_ij/μ_i  (i≠j),     Q_ii = −sum(j≠i) k_ij/μ_i,
(Qf)_i = (1/μ_i) sum(j≠i) k_ij(f_j−f_i).
```

All quantities in the bounded verification will be dimensionless rationals.
Calling μ a measure does not identify it with measured proper volume, a
sampling density, a probability, or the scalar diagonal d of the previous
causal-operator contract. No geometry-to-conductance rule is assumed.

Define the node inner product ⟨u,v⟩_W=u*Wv. Here * denotes conjugate transpose;
for the real matrices in this design it agrees with transpose. Its adjoint
is Q†_W=W⁻¹Q*W, not generally Qᵀ. The edge expression (Bu)*K(Bv) is a
nonnegative semidefinite form when u=v; K need not be invertible.

For a real field f, define oriented flux J=−KBf. Positive J_e flows from
the declared tail to head. With this sign convention BᵀJ is net node influx.
The closed diffusion choice is W fdot=BᵀJ, equivalently fdot=Qf.
This choice of evolution is an additional stipulation, not a consequence
of having written down a matrix.

## 2. Weighted Green identity, conservation and kernel

Since B1=0 and ℒ is symmetric,

```text
Q1 = 0,             1ᵀWQ = 0,             WQ = Q*W = −ℒ,
⟨u,Qv⟩_W = −(Bu)*K(Bv).
```

The last identity follows directly by substituting Q. It proves weighted
self-adjointness and nonpositivity, without a spectral approximation. It
does NOT imply 1ᵀQ=0 for counting measure or Q=Qᵀ in ordinary coordinates.

For closed real diffusion, the weighted mass M=1ᵀWf and energy
E=½fᵀWf obey

```text
Mdot = 0,
Edot = −sum(edges e) k_e(f_head−f_tail)² ≤ 0.
```

Each undirected edge is summed once. Constants are stationary. More precisely,
ker Q consists of fields constant on each connected component of the graph
containing only strictly positive-conductance edges. Indeed Qf=0 implies the
nonnegative sum of weighted squared differences vanishes; conversely such
componentwise constants have KBf=0. A zero edge does not join components.
Isolated nodes therefore retain their own constant mode. Strict dissipation
or a single equilibrium constant cannot be asserted without qualification.

For any subset S⊆V, cancellation of internal edge contributions gives

`sum(i∈S) μ_i(Qf)_i = sum(i∈S,j∉S) k_ij(f_j−f_i)`.

This is a finite flux balance. Restricting attention to S need not conserve
its mass; inflow from its complement remains visible.

An exact two-node witness separates the two measures. For μ=(1,2), k_01=1,
and f=(0,1),

```text
Q = [−1    1  ],       Qf = (1,−1/2),
    [ 1/2 −1/2]

1ᵀWQf=0,              1ᵀQf=1/2,              Edot=−1.
```

Thus the same operator conserves its supplied weighted mass while changing
the unweighted sum. Conservation claims must name their measure.

## 3. Boundary contracts: closed, prescribed flux, held reservoirs

These are different models. Never infer one from an endpoint's coordinate.
The finite path examples have no periodic wrap or implicit exterior edge.

### 3.1 Closed graph

All nodes are dynamic and fdot=Qf. Section 2 applies. An endpoint with one
edge simply has a one-neighbor row; no additional boundary approximation
or continuum Neumann accuracy is asserted.

### 3.2 Prescribed outward node flux

Supply a real vector q(t), positive when material leaves a node to the
exterior. It is separate from the internal oriented edge flux J. Set

```text
W fdot = BᵀJ − q,       fdot = Qf − W⁻¹q,
Mdot = −1ᵀq,
Edot = −(Bf)ᵀK(Bf) − fᵀq.
```

The homogeneous Q still annihilates constants, but the full affine field
at c1 is −W⁻¹q and need not vanish. Zero NET exterior flux can preserve
mass while forcing local changes or increasing energy. For the two-node
graph above, f=(1,2), q=(2,−2) gives fdot=(−1,1/2), Mdot=0 and Edot=+1.
No positivity-preserving evolution is claimed for arbitrary prescribed q.

### 3.3 Dirichlet reservoirs

Partition V into dynamic nodes I and held nodes D; hold f_D=g. Let ℒ_II and
ℒ_ID denote blocks in explicitly declared node orders. Then

```text
W_I fdot_I = −ℒ_II f_I − ℒ_ID g,
Q_D = −W_I⁻¹ℒ_II,       b_g = −W_I⁻¹ℒ_ID g,
fdot_I = Q_D f_I + b_g.
```

The outward reservoir flux from interior node i is
q_i^res=sum(a∈D) k_ia(f_i−g_a). With M_I=1ᵀW_I f_I and
E_I=½f_IᵀW_I f_I,

```text
Mdot_I = −sum(i∈I,a∈D) k_ia(f_i−g_a),
Edot_I = −sum(internal edges {i,j}⊆I) k_ij(f_i−f_j)²
         −sum(i∈I,a∈D) k_ia f_i(f_i−g_a).
```

The homogeneous block remains W_I-self-adjoint and nonpositive, but

`(Q_D1)_i = −sum(a∈D) k_ia/μ_i`

is generally nonzero. Grounding g=0 dissipates energy while permitting mass
loss. Nonzero g can drive energy into the interior. Consistent full constant
data f_I=c1 and g=c1 are stationary, including c≠0; this is an affine balance,
not a claim that Q_D1=0.

The grounded block is strictly negative/invertible iff each connected
component of the positive-conductance interior graph has a positive edge to
D. To prove it, extend an interior field by zero on D and apply the energy
identity: a zero mode must be constant on interior components and vanish on
each attached component. An unattached component supplies a nonzero kernel
vector. Edges within D do not alter the interior equation; held values and
their external maintenance are not part of conserved interior mass.

## 4. Exact moments of the actual matrix

For supplied scalar coordinates x_i define, INCLUDING the diagonal,

```text
m0_i = sum(j) Q_ij,
m1_i = sum(j) Q_ij(x_j−x_i),
m2_i = ½ sum(j) Q_ij(x_j−x_i)².
```

Throughout this document m2 is the **half-second moment**, not the raw
second moment. Direct expansion yields for any matrix Q

```text
Q1 = m0,
(Qx)_i = x_i m0_i + m1_i,
(Qx²)_i = x_i² m0_i + 2x_i m1_i + 2m2_i.
```

For a quadratic p(x)=a+bx+cx², this is equivalently

`(Qp)_i = m0_i p(x_i) + m1_i(b+2cx_i) + 2c m2_i`.

The full closed Q has m0=0. A reduced Dirichlet Q_D generally does not, so
dropping the m0 term is an error. Its moments use only interior columns;
reservoir forcing b_g must be retained separately. Report full-stencil and
reduced-block moments as distinct objects, not interchangeable coefficients.

In p coordinate dimensions, define

```text
b_i = sum(j≠i) Q_ij(x_j−x_i),
D_i = ½ sum(j≠i) Q_ij(x_j−x_i)(x_j−x_i)ᵀ.
```

For this closed Q, Qx^α=b^α and
Q(x^α x^β)=x^α b^β+x^β b^α+2D^αβ, pointwise. For a symmetric matrix H
and quadratic p(x)=a+v·x+½xᵀHx,

`(Qp)_i = b_i·(v+Hx_i) + tr(D_i H)`.

D_i is positive semidefinite because each summand has nonnegative weight.
It may be singular and is not automatically a spacetime metric, an inverse
metric, or a calibrated diffusion tensor. These identities are exact on the
finite marks. Continuum consistency, limiting coefficients and uniform error
bounds require an additional family of graphs and assumptions.

### 4.1 Repair the actual divergence coefficient

At an interior point of a supplied uniform one-dimensional grid, use x_{i±1}
=x_i±h, h>0, μ_i=1 and arithmetic-face conductances
k_±=(η_i+η_{i±1})/(2h²), for a supplied positive profile η. Then

```text
m1_i = (η_{i+1}−η_{i−1})/(2h),
m2_i = (2η_i+η_{i+1}+η_{i−1})/4,
m2_i−η_i = (η_{i+1}−2η_i+η_{i−1})/4.
```

The alternative finite-volume normalization μ_i=h,
k_±=(η_i+η_{i±1})/(2h) gives the same row Q, not the same absolute measure.
The pointwise operator η_i(f_{i+1}−2f_i+f_{i−1})/h² instead has
m1_i=0 and m2_i=η_i. Checking that operator does not check the selected
arithmetic-face operator. A smooth-grid interpretation can make their
second-moment difference small; it does not make the exact finite identity
true. No convergence rate is claimed without regularity/grid premises.

The prior audit's periodic local stencil η=(1,2,1) at node 0 gave m2=5/4
instead of η_0=1. Wrapped offsets in that calculation are local offsets,
not automatically differences of a global real coordinate vector. Preserve
that historical witness; use an open path to test global Qx identities here.

On the three-node path with all nodes dynamic, x=(−1,0,1), μ=(1,1,1),
η=(2,1,1), and conductances (3/2,1),

```text
Q = [−3/2  3/2   0 ]
    [ 3/2 −5/2   1 ]
    [ 0     1   −1 ],

m1 = (3/2,−1/2,−1),       m2 = (3/4,5/4,1/2).
```

The center coefficient is 5/4, not 1; its first moment is −1/2, not 0.
The endpoint rows are one-sided closed rows. They are not interior stencils
with missing terms silently filled in.

### 4.2 Pointwise multiplication is not universally nonconservative

Let Q_0 be the unit-conductance graph operator with counting measure, and
take η_i>0. The pointwise operator Q_pt=diag(η)Q_0 generally has
1ᵀQ_pt≠0. But it has the admitted representation

`W_pt=diag(1/η_i), K_pt=I, Q_pt=−W_pt⁻¹BᵀK_ptB`.

It therefore conserves the reciprocal-profile weighted mass and is
self-adjoint in that measure. This is a different supplied measure/operator
pair, not a silent repair of the counting-measure comparison. On the same
three-node path with η=(2,1,1),

```text
Q_pt = [−2  2  0],        1ᵀQ_pt = (−1,1,0),
       [ 1 −2  1]
       [ 0  1 −1]

m1 = (2,0,−1),           m2 = (1,1,1/2).
```

The useful distinction is the actual row and its declared measure, not a
blanket claim that one algebraic form can never conserve anything.

## 5. What an ideal full operator identifies

Within this admitted undirected reversible class, full Q in a specified
node basis determines the positive-edge support and, along each such edge,

`μ_j/μ_i = Q_ij/Q_ji`, because `μ_i Q_ij=μ_j Q_ji=k_ij`.

Following a path determines relative measures within a positive-conductance
component. The result is path-independent under the admitted-class premise.
Fixing one positive reference measure in each component then determines all
μ in that component and k_ij=μ_iQ_ij. Isolated nodes retain a free scale.
An arbitrary matrix with nonnegative off-diagonal entries and zero row sums
need not satisfy this reversible premise; cycle-ratio consistency cannot be
silently assumed for such a matrix.

Conversely, for any c>0, (W,K)→(cW,cK) leaves Q unchanged. Independent positive
scales on positive-conductance components have the same property. Thus full
Q identifies W,K up to exactly one scale per such component in this class,
not up to a single universal scale on a disconnected graph. Presence of an
extra zero-weight edge is also invisible if the graph itself is unknown.
This proof does not provide stable inversion of noisy, nearly zero entries.

This is more informative than saying that Q contains no measure information:
it can contain RELATIVE measure information. Yet an absolute measure or
physical unit still requires additional input. Under common scaling, mass,
energy and flux values scale by c even though Q and all its coordinate moments
remain identical. The chosen basis and supplied coordinate marks also remain
part of the interface; Q alone does not recover x.

The previous joint-geometry channels O,P,T do not already provide this full
Q. If Q=F(O,P,T) is only a common deterministic construction, identical inputs
still give identical outputs and retain the previous geometric collision.
An actually measured additional operator channel could change identification;
it would require its own response, measure/basis and uncertainty contract.
Supplying W or k from a hidden geometric target is not recovering them from
the old observations. See the
[joint-channel result](../qr-05-joint-geometry-verification-2026-09-12/RESULTS.md).

## 6. A precise optional QM connection, not a dynamics selection

In the finite weighted complex Hilbert space, H=−Q is self-adjoint and
nonnegative. **If** one stipulates the dimensionless evolution

`i ψdot=Hψ`, equivalently `ψdot=iQψ`,

then d(ψ*Wψ)/dt=iψ*(WQ−Q*W)ψ=0. Equivalently
−W^(1/2)QW^(−1/2)=W^(−1/2)ℒW^(−1/2) is an ordinary Hermitian
nonnegative matrix. This permits an ordinary finite unitary model in a
weighted basis. It does not determine a physical Hamiltonian, time unit,
state preparation, position observable, measurement instrument or Born
probabilities merely from Q.

The equally explicit diffusion choice fdot=Qf instead decreases the weighted
squared norm at rate −2(Bf)*K(Bf). Norm preservation and dissipation are not
two descriptions of the same chosen evolution. No Wick rotation or physical
equivalence between them is asserted. The design supplies a reusable
adjoint/norm check for a future chosen quantum model, not a derivation of QM.

Nor is Q the preceding nilpotent causal A: a positive edge gives bidirectional
off-diagonal support, Q has constant zero modes, and nonzero Q is not nilpotent
(it is similar to a nonzero symmetric nonpositive matrix). The finite strict-
poset path-inverse theorem cannot be transplanted to Q. No Lorentzian metric,
retarded/advanced Green function, gravity equation or ontology follows here.

## 7. Transformations and what they preserve

For a node permutation P, transport the entire input: W'=PWPᵀ, B'=BPᵀ,
x'=Px, f'=Pf, q'=Pq, and the boundary partition and held values accordingly.
Keep edge order fixed. Then Q'=PQPᵀ. Relabeling is not a change of physics
or a source of information.

For any diagonal edge-sign matrix S with entries ±1, replace B by SB and
keep K fixed. Then ℒ,Q are unchanged, J'=SJ, and B'ᵀJ'=BᵀJ. This is purely
orientation bookkeeping; it is not the previous causal order reversal.

For joint scaling c>0, let μ'=cμ, k'=ck and q'=cq, holding x,f,g fixed.
Then Q and the full affine fdot are unchanged, while W, ℒ, J, reservoir
fluxes, mass, energy and their derivatives scale by c. If prescribed q
were instead held fixed, W⁻¹q would scale by 1/c and the full affine dynamics
would NOT be invariant. Fixed Dirichlet values need no such scaling; their
reaction fluxes scale with k. Do not call a fixed-q experiment the same gauge.

## 8. Prospective bounded verification

Use exactly these nine base fixtures, with node order 0,...,n−1. Two-node
graphs have edge 0→1; three-node graphs have edges 0→1 and 1→2 in that order.
The singleton has no edges. The arrows specify B only. Vectors in the table
are in full-node order except f_I and g in Dirichlet rows.

| ID | μ; k; x | Boundary and field |
|---|---|---|
| singleton_closed | (1); (); (0) | Closed, f=(2) |
| unequal_closed | (1,2); (1); (0,1) | Closed, f=(0,1) |
| zero_edge_closed | (1,2,1); (1,0); (0,1,2) | Closed, f=(0,1,2) |
| arithmetic_face_closed | (1,1,1); (3/2,1); (−1,0,1) | Closed, f=(0,1,0) |
| pointwise_reweighted | (1/2,1,1); (1,1); (−1,0,1) | Closed, f=(0,1,0) |
| prescribed_flux | (1,2); (1); (0,1) | All dynamic, f=(1,2), outward q=(2,−2) |
| dirichlet_grounded | (1,1,1); (3/2,1); (−1,0,1) | I=(1), D=(0,2), f_I=(1), g=(0,0) |
| dirichlet_driven | (1,1,1); (3/2,1); (−1,0,1) | I=(1), D=(0,2), f_I=(1/2), g=(1,1) |
| dirichlet_unanchored | (1,2,1); (1,0); (0,1,2) | I=(1,2), D=(0), f_I=(1,2), g=(0) |

In closed rows q=0. No prescribed q is added to a Dirichlet row. The η profile
in section 4 explains two fixtures, not a hidden extra input to the evaluator.

Apply four SEPARATE variants to every base, in order: identity; cyclic
relabel old i→(i+1) mod n; reverse every edge orientation; joint scaling
μ,k,q by c=3/2. Do not compose them, deduplicate symmetric rows, add parameter
sweeps or fit fixtures. Relabelled I and D preserve their transported list
order, as do f_I and g; they are not silently sorted. Thus full matrices
conjugate by P while reduced matrices retain coordinates in the transported
active-node list. Full-node vectors use the new node labels as usual.

The analytical prospective census is 36 labelled rows, 92 full-node
occurrences, 56 edge occurrences, 252 cells per full square node matrix,
72 dynamic-node occurrences and 168 cells per effective dynamic matrix.
Duplicates are deliberate checks, not independent statistical trials.

The following values are analytical expectations, NOT an executed report.
M and E here refer to the dynamic nodes with their supplied measure.

| Base | Full affine fdot on dynamic nodes | Mdot | Edot |
|---|---|---:|---:|
| singleton_closed | (0) | 0 | 0 |
| unequal_closed | (1,−1/2) | 0 | −1 |
| zero_edge_closed | (1,−1/2,0) | 0 | −1 |
| arithmetic_face_closed | (3/2,−5/2,1) | 0 | −5/2 |
| pointwise_reweighted | (2,−2,1) | 0 | −2 |
| prescribed_flux | (−1,1/2) | 0 | 1 |
| dirichlet_grounded | (−5/2) | −5/2 | −5/2 |
| dirichlet_driven | (5/4) | 5/4 | 5/8 |
| dirichlet_unanchored | (−1/2,0) | −1 | −1 |

For the two anchored Dirichlet bases Q_D=[−5/2], with b_g respectively
0 and 5/2. The unanchored block is diag(−1/2,0), with b_g=0. Retain the
unanchored zero mode rather than asserting that every Dirichlet block is
invertible. Consistent nonzero constant interior/reservoir data are a
separate algebraic check, not another study row.

### Full report and independent routes

The primary route should assemble BᵀKB and the reference route independently
assemble neighbor exchange and boundary fluxes; they must not share a
mathematical helper or import one another. Compare complete native rational
objects, not just common pass flags or rounded summaries. At minimum retain:

- Entire supplied world, ordered boundary lists, B,W,K,ℒ,Q, weighted and
  ordinary conservation residuals, Q1, WQ−QᵀW and the weighted energy form.
- Full field (including held values), edge differences, signed flux J,
  node influx BᵀJ, positive-edge components and their indicator kernel basis.
- Full m0,m1,m2 and Q1,Qx,Qx², plus all corresponding reduced-block objects
  with nonzero m0 retained. Compute moments from actual rows and check them
  independently against the polynomial identities.
- Effective matrix and affine source, actual fdot, outward reservoir fluxes,
  mass/energy values and both sides of their derivative identities. Keep
  homogeneous constant-row tests distinct from full constant-data balance.
- Per-component relative measure reconstruction normalized to one at that
  component's smallest label, with detailed-balance and normalized-conductance
  residuals. Under relabeling this anchor can change: compare ratios, not an
  unjustified raw permutation of the normalized weight vector. If the new
  anchor is old node b, divide both transported normalized measures and
  normalized conductances in that component by the old normalized μ_b.
- Complete identity-versus-scale same-Q/different-measure witnesses, and
  all relabel/orientation/scaling relations, including affine boundary terms.

The optional QM statement needs an adjoint/norm-derivative identity, not a
matrix-exponential simulation or numerical spectral decomposition. The proof
for arbitrary finite graphs remains analytical; these small cases alone do
not verify a universal theorem.

Before execution, freeze the full machine-readable protocol, API and exact
report schema. Use plain native dict/list/int/Fraction inputs, 1≤n≤3,
positive μ, nonnegative k, and inclusive 128-bit rational input bounds.
Reject malformed shapes/types, bool-as-int, coercions, duplicate undirected
edges, self-loops, invalid partitions or inconsistent boundary vectors.
Accept zero edges, isolates and arbitrary node labels. Do not mutate inputs
or alias mutable output to them; otherwise-valid shared containers may be
copied. The pure engine has no I/O, random state or hidden target channel.

Freeze these named proof/API boundary controls as tests, outside the 36-row
study census: a closed three-node triangle with μ=(1,1,1), k=(1,1,1), ordered
edges (0→1,1→2,2→0), x=(0,1,2), f=(0,1,0), q=0 (Q has diagonal −2 and all
off-diagonals 1); consistent Dirichlet f_I=g=1 on the arithmetic-face graph
with I=(1), D=(0,2); and the prescribed-flux two-node graph with f=(1,2),
q=(1,0), giving
fdot=(0,−1/2), Mdot=−1, Edot=−2. The last checks nonzero net outflow as well
as the study's zero-net-flux energy-increase witness. These are fixed
analytical controls, not permission for an adaptive fixture bank.

### Evidence and later scope

Bind both design documents, the executable contract/protocol, independent
engines, tests, driver and any literal-SHA-pinned evidence-only helper before
the first mathematical run. Authenticate source bytes before loading; compare
native types before canonical serialization, recheck source/input identities
after execution and publish captures exclusively with readback. Earlier
frozen sources and captures remain unchanged. Do not import branch engines.

Use 30 seconds per full analysis, 60 seconds per suite, 262,144 bytes per
source, 16,777,216 per artifact, and one alternate-runtime full replay.
Sequence: static review, freeze, first capture, normal/optimized suites and
full replays, then exactly one Python 3.11 full replay. Preserve any failure
and use a named repair revision instead of tuning frozen sources afterward.

The next gate is this bounded exact verification. Physical operator
coefficients, geometry/measure acquisition, general correspondence distortion
and noncollapse, uniform bounds, stochastic growth/null calibration and
empirical interfaces remain separate. RET integration, materials monitoring
and anomaly triage readiness are not promoted. Book work stays archival;
deferred clocks, retired couplings and new gravitational laws are not reopened.
