# T8-Q: coherence-sensitive recorded readout

12 September 2026. **A conditional finite candidate, not a new QR-05 gate.**
This extends the explicitly assumed-law search, separately from the
[renewal-port transport candidate](../t8-q-renewal-port-candidate-2026-09-12/CANDIDATE.md)
and its bounded verification. It specifies a readout law whose probabilities
depend on off-diagonal pair information at fixed classical record and fixed
atomic diagonal. It does not supply quantum-dependent order selection.

The additional hypotheses are substantive: a finite noncommutative
composition table, its compatible history-kernel domain, a compression
update and orthogonal record-block preparation. They encode conventional
finite quantum measurement structure algebraically. They are **not derived
uniquely from DET**, nor made less of an assumption by avoiding matrix
notation. This is a candidate under the owner's explicitly broadened
assumed-L authorization; a stricter demand for that algebra to follow from
the existing DET axioms remains an unclosed gap.

## 1. An explicit algebra, with the pair-kernel still primitive

Take two abstract local symbols, 0 and 1. Their directed pairs span a complex
unital *-algebra with the following fixed composition rules:

\[
e_{ij}e_{kl}=\delta_{jk}e_{il},\qquad
e_{ij}^{*}=e_{ji},\qquad 1=e_{00}+e_{11}.
\]

This table is an assumption of L. The symbols are possibility/control
labels, not future vertices or spatial coordinates. Put

\[
z_i=e_{ii},\quad u=e_{01}+e_{10},\quad v=z_0-z_1,
\quad q_s=(1+su)/2,\quad h_{i,s}=q_sz_i\quad(s=+1,-1).
\]

The table implies u*=u, v*=v, u²=v²=1. Thus q_s are self-adjoint
idempotents with q_++q_-=1 and q_+q_-=0. The four h's form a basis:
h_(i,+)+h_(i,-)=e_ii and h_(i,+)-h_(i,-)=e_(1-i,i). Their sum is 1.
No projector or amplitude is independently supplied to obtain these facts.

Keep the Hermitian pair-kernel D as state data. If
a=Σ_z c_z(a)h_z, define the **derived**, not extra, functional

\[
\phi_D(a)=\sum_z c_z(a)\sum_yD(y,z).
\]

The admitted unnormalized domain is the proper cone

\[
\mathcal K=\{D\succeq0:\ D(z,w)=\phi_D(h_z^*h_w)\text{ for every }z,w\}.
\]

These are fixed linear compatibility identities, not state-dependent
renormalization. Because h spans the algebra, D is strongly positive iff
the reconstructed functional is positive: for a=Σc_z h_z,
φ_D(a*a)=Σ conjugate(c_z)D(z,w)c_w≥0. Conversely any positive functional
φ determines an admitted D by that formula and is recovered from its
column sums. Hence no quantum state is silently discarded or added.

The original mass convention remains

\[
m(D)=D(\Omega,\Omega)=\sum_{z,w}D(z,w)=\phi_D(1).
\]

Also Σ_z h_z* h_z=1, so **Tr D=m(D) on this compatible cone only**.
This identity is proved from the chosen histories; it is not a switch to
trace normalization on the earlier candidate's unrestricted cone.

For two ports take the tensor product of two copies of this algebra. There
are 16 product-history labels z=(i,s,j,t), a basis of the resulting algebra.
All definitions above extend using these histories. Positive functionals
need not factor across the ports; correlated and entangled cases are admitted.
The state remains X=(C,D), C=(V,≺,R), with m(D)=1 before a birth.

## 2. The complete law, including growth and residual payload

Keep the renewal-port action menu A∈{{a},{b},{a,b}} and its committed-head
rule. For each participating port p let H_p be its latest committed event.
Set S_A=∪_(p∈A,H_p exists)↓H_p, counting a repeated ancestor only once, and
r_A=Σ_(e∈S_A)x_e mod 2. The structural locality qualification of the earlier
candidate is unchanged: support reads committed port incidence; the setting
reads outcomes only in S_A. No ambient birth index enters L.

**This new law's setting is r_A, selected before the outcome.** It is not
the transport candidate's setting x XOR r_A. Record R(e)=(A,x,r_A).
Write u_p,v_p for the algebra elements on the relevant tensor factor and
derive

\[
t_{A,0}=\prod_{p\in A}u_p,\quad
t_{A,1}=\prod_{p\in A}v_p,\qquad
p_{A,x,r}=\frac{1+(-1)^x t_{A,r}}2\quad(x=0,1).
\]

Each t is a self-adjoint involution; the two p's for a given A,r are
orthogonal idempotents summing to 1. The synchronizing action {a,b} reads
a binary parity; it is not two separately recorded local outcomes.

Declare the entire unnormalized branch, on the same 16-history carrier:

\[
\mathcal B_{C;A,x}[D](z,w)
=\frac13\phi_D(p_{A,x,r_A}h_z^*h_wp_{A,x,r_A}),\qquad
K_C(A,x)=m(\mathcal B_{C;A,x}[D])
=\frac13\phi_D(p_{A,x,r_A}).
\]

The factor 1/3 is an explicit fixed action weight in this candidate L, not
a DET-derived constant or a Rideout–Sorkin parameter. Add one formal ⊥
outcome per action with an identically zero map and formal ⊥ setting; it
is never normalized or committed. Actual binary outcomes can also have
zero weight, without removing their declared maps or labels.

Form Dpre as the direct sum of these nine branch-tagged kernels, with zero
cross-branch entries. This record-block preparation is a law assumption,
not a derived decoherence mechanism. Sample (A,x) from its branch masses.
For K>0, D⁺=B[D]/K; only then append a fresh maximal e with past exactly
S_A and record (A,x,r_A). Retain every prior record and order relation and
update the participating heads. Possibilities are not preallocated events.
This specifies F_L; a scheduler or agent does not separately choose S.

## 3. Conditional theorem on the whole declared domain

**Positivity, linearity and closure.** For the derived functional
ψ(a)=φ_D(pap)/3, ψ(a*a)=φ_D((ap)*(ap))/3≥0. Thus its rebuilt history
kernel lies in K. Reconstruction, compression and rebuilding are linear,
so unnormalized branches respect convex mixtures. Conditional normalized
states use the usual branch-probability-weighted mixture, not equal mixture
weights. These claims concern the whole cone K, not selected fixtures.

**Normalization and zero branches.** For each action,
Σ_x K(A,x)=φ_D(1)/3; summing actions gives m(D). If K(A,x)=0, positivity
and Cauchy–Schwarz imply ψ(a)=0 for every a. Its rebuilt branch kernel is
therefore identically zero. No division by zero is performed. This implication
holds here; a generic strongly positive kernel can be nonzero with zero
total-entry mass.

**Append and birth-label covariance.** The precursor is an ideal, so maximal
append preserves the old marked poset. Two births sharing a port are
comparable. Incomparable births must be singleton actions on different
ports; neither changes the other's ideal or setting. Their idempotents
commute on the tensor algebra, even for correlated input functionals.
The complete two-step functional in either order is

\[
\psi_{ab}(a)=\tfrac19\phi_D(p_a p_b a p_b p_a).
\]

Rebuilding gives equality of the full unnormalized residual pair-kernels,
with transported event records, including impossible branches. Adjacent
incomparable swaps connect linear extensions, proving birth-label covariance
for the generated marked histories. Same-port context changes need not
commute and are not covered by this exchange claim. Neither label covariance
nor the port tensor structure establishes physical spacelike locality.

## 4. A genuine fixed-diagonal readout separation

For one port choose the two positive normalized functionals

\[
\phi_\pm(e_{00})=\phi_\pm(e_{11})=\tfrac12,
\qquad \phi_\pm(e_{01})=\phi_\pm(e_{10})=\pm\tfrac14.
\]

Their positivity follows from diagonal 1/2 and determinant 3/16 in their
two-symbol coefficient form. For s,t∈{+1,-1}, their kernels obey

\[
D((i,s),(j,t))=\delta_{st}
\begin{cases}\phi(e_{ii})/2&i=j,\\s\phi(e_{ij})/2&i\ne j.\end{cases}
\]

Both local kernels have all four atomic diagonals 1/4, but their
off-diagonals differ. Tensor either with the other port's uniform diagonal
functional. Both 16-atom kernels then have every diagonal **1/16**.
At the **same empty C**, with the **same law and pre-outcome setting r=0**,

\[
K_+(\{a\},0)=\tfrac14,\qquad K_-(\{a\},0)=\tfrac1{12}.
\]

Conditional on action {a}, these are **3/4 versus 1/4**. This is a rejected
diagonal-only summary for the declared readout question, not simply a change
of classical preparation labels. The whole D, not those labels, is input.

**A necessary zero-branch control.** Use instead local off-diagonals -1/2.
The input's q_+ history block is (1/4)[[1,-1],[-1,1]]: nonzero positive
matrix, total mass zero. The compression branch φ(q_+ a q_+) is identically
zero. Therefore a raw restriction to a source history block is **not** this
law's residual update and cannot be normalized in its place. The law rebuilds
the full compatible history kernel after compression. Record preparation
is an explicit operation, not passive conditioning on an already existing
classical partition of Ω.

## 5. What changed, and what did not

The earlier rank-one obstruction assumes positive linear operations on the
**full** positive atomic-matrix cone with total-entry mass. Here the domain
is a proper algebra-compatible subcone and positivity of the branch maps is
asserted on that domain only. The obstruction is preserved, not disproved.
No nonlinear reweighting or hidden normalization change is used.

For an after-the-fact comparison, represent e_ij as ordinary matrix units.
The assumed algebra is isomorphic to M₂(C), and its two-port version to
M₄(C). The reconstructed φ has a density representation φ(a)=Tr(ρa),
with φ(e_ij)=ρ_ji. The derived branch is the conventional update
ρ↦pρp/3. This correspondence describes precisely how much familiar quantum
structure has been assumed; it is not a new derivation of that structure.
The upstream construction has no supplied Hilbert space, amplitudes or
matrix instrument, but adopting this noncommutative algebra and compression
rule is a substantive quantum-kinematic postulate nonetheless.

Action marginals remain exactly 1/3 for every normalized D. Since precursor
selection depends on those actions and committed incidence, the unmarked
order law remains quantum-independent. Outcomes can alter later measurement
contexts through past records; they do **not** alter this candidate's port
grammar or action marginal. The width-at-most-two limitation also remains.

**Yield:** an explicit conditional definition and consistency theorem,
plus a diagonal-summary counterexample. No quantum-to-order feedback,
manifoldlikeness, Lorentzian structure, physical apparatus, empirical
discriminator or metric-as-record promotion has been established. The
DET-native origin/selection of this algebra and law remains a named gap.
Option B, Status M and zero new gravity Novelty Ledger rows are unchanged.
No new QR-05 letter, geometry/coverage/noncollapse/identifiability sequel,
RET, clocks, book, κ-gravity or shared API work is opened.

## 6. Bounded arithmetic checks

The accompanying isolated checker compares symbolic pair composition with
an independently written **downstream** conventional matrix representation.
It checks all 16 functional-coordinate basis inputs for all 12 action /
context / binary-outcome maps; basis inputs are algebraic probes, not claimed
positive preparations. History reconstruction, full maps, complex coherence,
mixtures, zero branches and all disjoint context/outcome exchanges are
checked exactly. No second growth census, parameter sweep or geometry is run.
These implementation checks support, but do not replace, the theorem above.

Run `python3 check.py` and `python3 -O check.py` in this directory. All
arithmetic is rational (including rational real and imaginary components);
only the Python standard library is used. `CHECKS.md` records the executed
outcome. This readout construction is not another numbered or lettered gate.
