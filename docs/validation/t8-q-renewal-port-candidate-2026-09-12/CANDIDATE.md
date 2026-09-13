# T8-Q candidate: fixed renewal ports with quantum-payload transport

12 September 2026. **An explicit conditional candidate L is specified.**
This is candidate construction authorized by the owner, not a new QR-05
letter, a uniquely DET-derived law, or a geometry result. The preceding
[F_NOT_SPECIFIED finding](../t8-q-licensed-growth-2026-09-12/BIRTH_F.md)
remains the historical finding before these additional assumptions.

The candidate generates forks and joins, retains the entire quantum
pair-kernel, and has exact birth-label covariance. Its main limitation is
equally explicit: **birth/outcome probabilities do not depend on the quantum
payload**. It supplies coherent-payload transport through growing records,
not quantum-controlled order growth or general quantum measurement.

## 1. Assumptions, state and locality

Choose the following finite structure as part of one fixed law L:

- Two persistent port types P = {a,b}, and the action menu
  M = {{a},{b},{a,b}}. Ports are control types, not events, spatial axes,
  observer worldlines or uncommitted future vertices.
- The residual possibility set Ω = Z₃ × Z₃ and its full event algebra.
  This is a chosen finite possibility alphabet, not an assumed Hilbert space.
- Six positive action/outcome branches (A,x), A ∈ M, x ∈ {0,1}, each
  assigned weight 1/6 by L. A formal outcome ⊥ for each A has weight zero.
  These constants are explicit law assumptions, not percolation p or
  probabilities derived uniquely from DET.
- The record-block preparation and finite set permutations below. These
  specify quantum and record transformations together; no separately
  supplied quantum instrument is an input.

The mathematical state is **X = (C,𝔇)**, with C = (V,≺,R) the complete
committed marked poset. R(e) retains the action A_e, outcome x_e and setting
s_e. Each port's committed events form a chain. Start with V empty; neither
a seed event nor any later event is preallocated.

The residual 𝔇 is a Hermitian, biadditive, strongly positive pair-kernel on
Ω with 𝔇(Ω,Ω)=1. Equivalently its atomic matrix d is positive semidefinite
and the sum of **all** entries is one. That normalization is not generally
Tr d = 1. Complex off-diagonal entries are retained, not reconstructed from
a probability vector. A choice of initial 𝔇 is declared input data.

**Locality interpretation is load-bearing.** The law may inspect committed
port incidence and heads as structural metadata to determine a precursor.
Its record-dependent setting reads outcome values only in that precursor.
Heads are derived from C, not new primitive variables; cached heads would
have to agree with the committed marked order. This is not a claim that
every absolute precursor probability is independent of all surrounding
structure. Under that stronger interpretation the candidate is not admitted.
No global birth index or value of |V| enters any probability or setting rule.

## 2. The explicit birth law

Let h_p be the latest committed event touching port p, or absent if the port
is unused. Write ↓h for the inclusive past of h. For A ∈ M set

\[
S_A=\bigcup_{p\in A,\ h_p\text{ exists}}\downarrow h_p,
\qquad
r_A=\sum_{v\in S_A}x_v\pmod2.
\]

S_A is an order ideal, with repeated ancestors counted once. Reachable
records have binary outcomes; ⊥ is never sampled or committed. For a positive
branch β=(A,x), set s=x⊕r_A and use the following bijection of Ω; all
arithmetic is modulo three:

| A | π_(A,0)(i,j) | π_(A,1)(i,j) |
| --- | --- | --- |
| {a} | (i+1,j) | (−i,j) |
| {b} | (i,j+1) | (i,−j) |
| {a,b} | (j,i) | (i,j+i) |

The cycle inverses decrement; the last shear has inverse (i,j−i).
The law acts on **sets of possibilities**, with no quantum operator or
amplitude supplied upstream. Its unnormalized branch transformation is

\[
\mathcal B^L_{C;\beta}[\mathfrak D](U,W)
=w_\beta\,\mathfrak D(\pi_{A,s}^{-1}U,\pi_{A,s}^{-1}W),
\quad w_{(A,0)}=w_{(A,1)}=\tfrac16.
\]

For β=(A,⊥), define B_β identically zero and its formal setting tag as ⊥,
retaining that label without normalizing or committing it. Define the whole
precommit functional, on the disjoint union
of branch-tagged copies of Ω, by

\[
\mathfrak D^{\rm pre}_C((\beta,z),(\gamma,w))
=\delta_{\beta\gamma}\,
\mathcal B^L_{C;\beta}[\mathfrak D](\{z\},\{w\}).
\]

It is a direct sum of positive kernels; its branch blocks are exactly
decoherent. This orthogonal record-block preparation is an **assumption of
L**, not a derived decoherence mechanism. Its total mass is Σ_β w_β = 1,
so the joint kernel and positive-branch residual follow:

\[
K_C(A,x)=\mathcal B^L_{C;(A,x)}[\mathfrak D](\Omega,\Omega)=w_{(A,x)},
\qquad
\mathfrak D^+={\mathcal B^L_{C;(A,x)}[\mathfrak D]\over K_C(A,x)}.
\]

Sample β from this joint kernel, and **only then** append a fresh event e:

\[
V^+=V\cup\{e\},\qquad
\prec^+=\prec\cup\{(v,e):v\in S_A\},\qquad
R^+|_V=R,\quad R^+(e)=(A,x,s).
\]

The new event is maximal; its past is exactly S_A. Update the participating
heads to e, leaving other heads unchanged. This defines the stochastic
transition F_L:(C,𝔇)→(C⁺,𝔇⁺). Branch tags in Dpre describe possibilities,
not vertices already allocated in V. Alternative order births form a
classical mixture, not a coherent sum over orders.

An ideal can arise from several actions. Its probability is the sum of the
corresponding action/outcome weights, with action records retained. Initially
all three actions have empty past, so the aggregate empty-ideal probability
is one. After one {a} birth, only {b} has empty past, with aggregate probability
1/3. This is explicit changing structural support, not hidden dependence on
ambient n. The fixed menu is never replaced by uniform sampling over ideals
or a changing frontier.

## 3. Conditional consistency theorem

For every normalized strongly positive input 𝔇 and every reachable marked
snapshot of this fixed law:

1. **Normalization and positivity.** Pullback by a bijection preserves
   Hermiticity, biadditivity, strong positivity and total mass. Positive
   scaling and direct sum preserve positivity. The preceding formulas
   establish all nine branch weights, including three identically zero maps.
2. **Append consistency.** Union of inclusive down-sets is an ideal.
   Adding only arrows from that ideal to a fresh e preserves transitivity
   and acyclicity. Existing order and record entries are not rewritten.
3. **Complete incomparable-birth equality.** Births sharing a port become
   comparable: the later birth contains the earlier one in that port's
   past. Incomparable births therefore use disjoint actions {a} and {b}.
   Such births leave each other's heads, ideals and record parities unchanged.
   Their coordinate-wise permutations commute for every pair of settings.
   Consequently their complete unnormalized pair-kernel compositions agree,
   each with weight 1/36, after transporting event IDs and record slots.
   Zero-map compositions remain zero and their formal labels are retained.
4. **Birth-label covariance.** Linear extensions of a fixed generated
   marked poset are connected by swaps of adjacent incomparable events.
   Applying the previous identity at each swap proves equality of the full
   terminal branch map and transported record, not just scalar weights or
   one initial state's probabilities. Relabeling event IDs preserves the
   order-defined heads and settings. Port types stay fixed; no port-exchange
   symmetry is asserted.

This is an analytical theorem conditional on the displayed law and domain.
It is not an executed finite certificate or relativistic covariance result.
Same-port cycle and reflection need not commute: on a coordinate initially
zero, cycle-after-reflection gives one, while reflection-after-cycle gives
two. Those operations are comparable in this model, so covariance does not
require their exchange. Past-local record access is not being used as a
general proof of quantum commutation.

## 4. Nontrivial order and retained quantum information

From empty C, action sequence ({a,b},{a},{b}) creates a fork; sequence
({a},{b},{a,b}) creates a join. A synchronizing birth after the fork produces
a diamond. Every three-step positive action/outcome history has probability
1/216, independently of the input pair-kernel.

With all outcomes zero, all settings are zero. Both the fork and join have
the same composed permutation (swap the two coordinates and advance both)
and hence the same complete unnormalized payload map. Their retained posets
are still nonisomorphic. Thus this candidate preserves, rather than erases,
the payload-only failure already established by QR-05A.

An explicit nonclassical admissible input illustrates what is retained.
Let u=(0,0), v=(1,0), and let E_uv denote an atomic matrix unit. Set

\[
d_*={I_9+\tfrac{1+i}{2}E_{uv}+\tfrac{1-i}{2}E_{vu}\over10}.
\]

The affected two-by-two block has positive diagonal and determinant 1/2
before scaling; the remaining diagonal entries are positive. Thus d_* is
positive definite. Its total-entry sum is one. In particular,
μ({u,v})−μ({u})−μ({v})=1/10: it is not a diagonal classical kernel.
Each positive branch preserves this full complex pair information under its
declared relabeling. This input is a chosen primitive fixture, not a derived
state, amplitude prescription or experimental observation.

For an **after-the-fact QM comparison only**, each finite bijection has a
permutation matrix P_β. The already-defined branch becomes
w_β P_β d P_β†. Since Tr d>0 and permutations preserve it, the auxiliary
density matrix ρ=d/Tr d undergoes an ordinary random-unitary instrument with
the same weights. This representation does not generate the law; the
finite alphabet and set maps were specified first. It establishes neither
a uniquely selected physical Hilbert space nor general measurement/Born
reconstruction. Full record-resolved transformations, not discarded channels,
are the comparison object.

## 5. The quantum-feedback limit is structural

All branch probabilities here are state-independent. There is a short
general explanation within this particular operation class. On the full
cone of finite positive atomic matrices, let m(d)=1†d1. Suppose positive
linear branch maps Φ_β conserve total mass on that entire cone. Each positive
functional m∘Φ_β has a positive matrix E_β, with

\[
\sum_\beta E_\beta=\mathbf1\mathbf1^\dagger.
\]

The right side has rank one. Positivity forces every E_β to be a
nonnegative multiple c_β of that same matrix: on its orthogonal complement
each nonnegative quadratic form must vanish. Therefore
m(Φ_β(d))=c_β m(d), and probabilities on normalized inputs are constant.

This is **not** a no-go theorem for pair-kernel quantum models. It depends
on the full positive-matrix domain, linear positive operations and this
total-mass convention. It explains why this candidate cannot also promise
state-sensitive quantum readout. A nonlinear reweighting is not silently
inserted to defeat the result: it would change the operation class and lose
the established linear-instrument comparison.

## 6. Obligations and stopping boundary

| Licensed-G obligation | Candidate disposition |
| --- | --- |
| (a) Past-local | Settings use only R restricted to S_A; admissibility uses the explicitly assumed committed port structure. No claim to the stronger context-free absolute-probability condition. |
| (b) Birth-label covariance | Proved for complete maps of this generated marked-poset family by adjacent incomparable swaps. |
| (c) Incomparable quantum maps | Disjoint-coordinate pullbacks commute on the full declared kernel domain; no physical spacelike claim. |
| (d) Weights from L/𝔇 commit | One explicit L constructs Dpre; its diagonal record blocks give K. The six equal weights are declared model choices, not hidden percolation or uniquely derived constants. |
| (e) Order and records retained | Full marked C survives; explicit fork/join payload collision remains distinct in C. |
| (f) No agency variable | Action and outcome are sampled jointly; no additional chooser of S exists. |
| (g) Stable L | Alphabet, menu, permutations, record rule and weights are fixed; only their committed inputs change. |

The port/action grammar, fixed weights, chosen alternative algebra and
orthogonal record preparation are **additional candidate assumptions**.
The generated orders have width at most two and exclude many finite posets.
There is no manifoldlikeness, local metric, quantum-to-order feedback,
physical apparatus or empirical discriminator established here.

Metric, Minkowski coordinates, Johnston kernels, Rideout–Sorkin p, Hilbert
spaces, amplitudes, future vertices, foliation and a global birth counter
are not construction inputs. No MODEL_CARD/GOVERNANCE/shared API or
RET/T8 source is edited or imported. Option B, Status M and zero new gravity
Novelty Ledger rows remain unchanged.

**Status: candidate specified and analytically checked, not certificate-run.**
Independent read-only checks agreed on the growth and full-map covariance
arguments. No executor, simulation or create-only capture was run for this
candidate search. No new QR-05 letter or coverage/noncollapse sequel is
opened; this document is the candidate, not a plan substituting for one.
