# RI-08h — connected reversible generators on the interior return cone

13 September 2026. **CONDITIONAL_INTERIOR_REVERSIBLE_GENERATOR_CLASSIFICATION;
CUT_ONLY_GENERATOR_NONIDENTIFICATION; EXPLICIT_PREMISE_BOUNDARIES.**
This is a theorem under additional reversible-law premises, not a
DET-derived Hamiltonian, physical time law, energy scale or full QM.

## 1. Fixed object and added premises

Use the explicit enlarged return cone from
[RI-08g](../t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md).
For a fixed known interior parameter \(|t|<1\), let
\[
B_t=(I+tZ)/4,\qquad
M_t(\rho)=U((\rho^T/2)\otimes B_t)U^\dagger,\qquad
U=(I\otimes H_{\rm Had})\mathrm{CNOT}.
\]
Here \(X,Y,Z\) are the standard Pauli matrices and \(H_{\rm Had}\) is the
Hadamard matrix. These matrix conventions, independent reference and
coupler remain supplied interface structure, not derived DET primitives.
The native labels are \((a,i,b,j)\), indexed by \(8a+4i+2b+j\).
The fixed signed permutation is
\[
P_{8a+4b+2i+j,\;8a+4i+2b+j}=(-1)^{ai+bj}.
\]
Writing \(\alpha=(a,b)\) for a cell, define
\[
\mathcal I_t((\rho_\alpha))
=P^\dagger\operatorname{diag}(M_t(\rho_{00}),M_t(\rho_{01}),
M_t(\rho_{10}),M_t(\rho_{11}))P,\qquad
L_t=\mathcal I_t\!\left(\bigoplus_\alpha{\rm PSD}_2\right).
\]
All four positive blocks are independent. This is not the older
equal-block return cone \(K_t\). The native kernel and all sixteen labels
remain present. On its actual sixteen-dimensional real span,
\[
q_\alpha=\operatorname{Tr}(E_\alpha\rho_\alpha),\qquad
E_{ab}=(I+(-1)^btZ)/4,\qquad
m=\sum_\alpha q_\alpha,\qquad
\tau=\operatorname{Tr}N=\tfrac14\sum_\alpha\operatorname{Tr}\rho_\alpha.
\]
Normalization mass m is not physical rest mass and generally is not raw
trace \(\tau\). Each \(E_\alpha\) is positive definite in this sitting.
The literal cut \(\mathsf C_\alpha\) keeps just its native cell block.

The new hypotheses are real-linear maps \(T_s\) on this actual span,
indexed by every \(s\in\mathbb R\), with

1. \(T_0=I\) and \(T_{s+u}=T_sT_u\);
2. \(T_s(L_t)=L_t\), with both \(T_s\) and \(T_{-s}\) positive;
3. \(mT_s=m\);
4. strong continuity: \(T_sN\) is continuous in s for every N.

In finite dimension the last condition implies matrix continuity in
any fixed basis. The parameter s is an abstract group parameter, not an
elapsed physical time. None of these availability, group, reversibility,
mass-law or continuity premises is proved from DET here.

## 2. Classification theorem

**Theorem.** Exactly the families satisfying these hypotheses have, on
each cell independently, the form
\[
\boxed{
T_s(\rho_\alpha)=E_\alpha^{-1/2}e^{-isH_\alpha}E_\alpha^{1/2}
\rho_\alpha E_\alpha^{1/2}e^{isH_\alpha}E_\alpha^{-1/2},
\qquad H_\alpha=H_\alpha^\dagger .
}
\]
The native action means conjugating this blockwise map by \(\mathcal I_t\).
Each \(H_\alpha\) is unique modulo addition of a real scalar multiple of
I. There are twelve nontrivial real generator parameters, three per
block, relative to the fixed known frame. Their values and physical
meaning have not been identified.

### 2.1 Each cell and its mass are preserved

The extreme points of the normalized positive base are rank-one matrices
in exactly one cell, normalized by its faithful \(E_\alpha\) mass.
Faithful filtering identifies each such component with the usual
rank-one trace-one Bloch sphere. The entire extreme-point set is thus
four disjoint compact spheres.

A mass-preserving cone automorphism maps the normalized base bijectively
to itself and preserves extreme points. For an extreme point in one
component, the continuous path \(s\mapsto T_sN\), starting at N, cannot
enter another connected component. Every positive matrix in that block
is a positive sum of rank-one matrices, so the entire block cone is
preserved, and the same holds for its real span. Apply mass preservation
to an isolated block: its individual \(q_\alpha\) is preserved. By
linearity this holds on every full input. In particular all cuts commute
with \(T_s\).

### 2.2 Faithful filtering gives rotations, not an assumed unitary law

For one block put \(\sigma=E^{1/2}\rho E^{1/2}\). The induced map on
\({\rm Herm}_2\) is positive with positive inverse and preserves
\(\operatorname{Tr}\sigma\). Its trace-one base is
\[
\sigma=(I+r\cdot(X,Y,Z))/2,\qquad \|r\|\le1.
\]
An affine bijection of this ball has the form \(r\mapsto A_sr+b_s\).
It fixes the center: the image ball would otherwise have distinct
centers of symmetry 0 and \(b_s\); composing their point reflections
would make a bounded ball invariant under a nonzero translation.
Thus \(b_s=0\). A linear ball bijection preserves the Euclidean norm
(apply the map and its inverse), hence is orthogonal by polarization.
Continuity from the identity gives \(A_s\in{\rm SO}(3)\).

### 2.3 Continuity plus the group law yields a constant generator

This step does not assume differentiability. For small \(a>0\), the
matrix \(J=\int_0^a A_u\,du\) is invertible because \(J/a\to I\).
The group law gives
\[
A_sJ=\int_s^{s+a}A_v\,dv .
\]
Continuity makes the right side differentiable, so
\[
A'_s=(A_{s+a}-A_s)J^{-1}
=A_sK,\qquad K=(A_a-I)J^{-1}.
\]
Differentiating \(A_s^TA_s=I\) gives \(K^T=-K\).
Differentiating \(A_se^{-sK}\) now gives zero, hence \(A_s=e^{sK}\).
Every real skew 3-by-3 matrix has the unique form
\(Kr=\omega\times r\). With
\[
H=\tfrac12(\omega_xX+\omega_yY+\omega_zZ),
\]
the Pauli multiplication identities give
\(-i[H,\sigma]=(\omega\times r)\cdot(X,Y,Z)/2\).
The same linear differential equation and initial value therefore give
\(\sigma_s=e^{-isH}\sigma e^{isH}\). Undoing the filter proves the
displayed classification.

### 2.4 Converse, generator form and scalar gauge

Conversely every Hermitian H gives a continuous group of invertible
congruences, positive with positive inverses and trace preserving in
filtered coordinates. It therefore preserves the original E mass.
Taking four independent such groups proves the full converse.

Equivalently,
\[
\dot\rho=G\rho+\rho G^\dagger,\qquad
G=-iE^{-1/2}HE^{1/2},\qquad
\boxed{G^\dagger E+EG=0}.
\]
Conversely this boxed equation makes
\(H=iE^{1/2}GE^{-1/2}\) Hermitian and gives the same flow.
Two Hermitian generators give the same full matrix evolution iff their
difference commutes with every Hermitian matrix, hence is scalar I.
The equivalent G gauge is an imaginary scalar I; these four scalar
directions act trivially. This proves the twelve-parameter count.

Unitarity is in the filtered coordinates. The raw congruence
\(E^{-1/2}e^{-isH}E^{1/2}\) need not be an ordinary unitary, and raw
trace need not be conserved when t is nonzero. At t=0 the filter is
scalar and the distinction disappears.

## 3. Exact observational limit and record contract

For every classified flow,
\[
q_\alpha T_s=q_\alpha,\qquad
\mathsf C_\alpha T_s=T_s\mathsf C_\alpha.
\]
The same holds for any finite word of separately declared such flows,
even when their generators differ. Interleaving those words with literal
cuts has the same cell-weight action as the cut word alone. A full
read has probabilities \(q_\alpha/m\); a positive selected cut makes
its full cell outcome repeat with probability one.

**Finite-policy theorem.** Fix the same known context, full committed
prefix, initial pending command word and retained nominal-command history,
and a finite common policy mapping that retained history to a command,
cut or stop. For normalized sources with equal four weights,
the conditional future cut-outcome laws agree. They also agree when
different candidate Hamiltonians implement the same nominal commands,
provided every implementation satisfies the premises. Proof is induction
on the finite policy tree: commands preserve all weights, cuts have
the same probabilities and selected weights, and the common policy
makes the same choice at every common retained history.

This does not identify different known commands. The actual command
labels, their order and all settings remain part of the record contract:

- a command changes the raw residual, keeps existing records intact,
  and appends its nominal label to an ordered pending word;
- a positive cut records the full cell outcome and actual pending
  word with the full precursor, then clears only that pending word;
- stop keeps the residual, complete history and any pending word.

Changing or omitting a known command changes this metadata. Equal cut
probabilities under different words do **not** mean equal full record
laws. For unknown-generator comparisons, equality of full observable
history laws is asserted only under the same retained nominal command
policy and identical initial command metadata. A policy inspecting unequal
pending words could choose different cut/stop actions, so even that
comparison is outside the theorem. No residual identity follows. No physical clock or unrecorded
duration is silently attached to a command label.

Thus this cut-only catalogue cannot determine the internal generators.
RI-08g permits other mathematical interior effects that can distinguish
equal-weight internal states, but their availability is not part of this
catalogue. Neither such additional effects nor an experiment identifying
H is supplied here.

## 4. What fails when premises change

### 4.1 Singular endpoint: positive reversible dark growth

At \(|t|=1\), \(E=\tfrac12Q_{\rm bright}\) has a dark direction. Set
\[
V_s=Q_{\rm bright}+e^sQ_{\rm dark},\qquad
\rho_s=V_s\rho V_s^\dagger.
\]
This is a continuous positive reversible group for all real s with
\(V_s^\dagger EV_s=E\). A dark diagonal scales by \(e^{2s}\).
For example the isolated block
\(\rho=2Q_{\rm bright}+Q_{\rm dark}\) has mass one, while its native
raw trace becomes \(1/2+e^{2s}/4\), unbounded as s increases.
The faithful filter is unavailable. This is a counterexample to
extending the interior compact/filtered-rotation conclusion to endpoints,
not an endpoint dynamics selected by DET.

### 4.2 Transpose, divisibility and the precise continuity boundary

Static transpose \(\rho\mapsto\rho^T\) is positive, invertible and
E-mass preserving because E is real diagonal. It flips the Y Bloch
coordinate and reverses orientation. It is an individual automorphism,
not a value of a group satisfying the hypotheses.

It would be incorrect to obtain transpose merely by dropping continuity
while retaining a group indexed by all of \(\mathbb R\). Indeed every
individual finite-dimensional linear automorphism is continuous in its
state argument and permutes the four extreme components. The induced
permutation homomorphism obeys
\(\pi(s)=\pi(s/24)^{24}=I\), since every permutation of four objects has
order dividing 24. Blocks therefore remain fixed even without parameter
continuity. Similarly
\(\det A_s=(\det A_{s/2})^2=1\). Orientation reversal is still excluded.

Continuity is load-bearing for differentiability and the constant
generator description. A genuine discontinuous example is mathematical
and nonconstructive: extend \(\{1,\sqrt2\}\) to a Hamel basis of
\(\mathbb R\) over \(\mathbb Q\), using choice, and define an additive f
with \(f(1)=0,\ f(\sqrt2)=1\), zero on the other basis elements.
Use \(e^{-if(s)Z/2}\) in one filtered block. Group law, positivity,
positive inverse and mass preservation all hold. For rationals
\(r_n\to\sqrt2\), \(s_n=\sqrt2-r_n\to0\) but \(f(s_n)=1\), so the
Bloch rotation does not tend to the identity. This is not an executable
or physically available law. Finite rational tests cannot establish
or refute the required all-real continuity premise.

### 4.3 A positive one-sided semigroup need not be reversible

In filtered coordinates define, for s≥0 and \(r=e^{-s}\),
\[
\mathcal D_r(\sigma)
=\tfrac{1+r}{2}\sigma+\tfrac{1-r}{2}Z\sigma Z.
\]
It is positive, trace preserving and obeys
\(\mathcal D_r\mathcal D_u=\mathcal D_{ru}\).
For \(0<r<1\), its linear inverse \(\mathcal D_{1/r}\) is not positive:
on \(Q_{X+}\) its eigenvalues are \((1\pm1/r)/2\), one negative.
Pulling back by the faithful filter gives the same boundary for L_t.
This is not a counterexample to the two-sided positive-inverse theorem.

## 5. Exact witness scope, not a sampled continuity proof

The isolated [model](model.py) and independent [checks](check.py) use
Gaussian-rational entries and the full sixteen-label native kernel.
The primary typed command fixture explicitly fixes \(t=3/5\) and the
enlarged L domain. At b=0 and b=1 respectively,
\[
E_0=\operatorname{diag}(4,1)/10=D_0^2/10,\quad D_0=\operatorname{diag}(2,1),
\qquad
E_1=\operatorname{diag}(1,4)/10=D_1^2/10,\quad D_1=\operatorname{diag}(1,2).
\]
The scalar cancels from \(D_b^{-1}UD_b\), avoiding irrational arithmetic.
The named exact elements
\[
U(c,d)=cI-idX,\quad
(c,d)=(3/5,4/5),\ (5/13,12/13)
\]
are unitary, have inverses \((c,-d)\), and multiply to
\[
(c,d)=(-33/65,56/65).
\]
These are labels for group elements, not numerical additive times.
Endpoint scales 2, 1/2 and 4 likewise label multiplicative
\(r=e^s\), not additive s. Endpoint scaling, static transpose and
dephasing/inverse are separate algebraic diagnostics, not admitted
primary reversible commands.

Witnesses check native reconstruction and signed-span actions; mass,
raw trace and inverse behavior; scalar gauge and the twelve nontrivial
generator directions; commutation with literal cuts; complex Y and
transpose; complete probabilities; and typed preservation of full
provenance, actual records and ordered pending words. Algebraic span
checks do not turn signed matrices into operational preparations.
Continuity, the all-real group classification and the finite-policy
theorem are established by the proofs above, not by finite samples.

Reproduction from the repository root:

~~~sh
.venv/bin/python -B docs/validation/t8-q-reversible-generator-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-reversible-generator-2026-09-13/check.py
~~~

## 6. Adjudication and stop boundary

The proposed conditional classification passes. The hypotheses constrain
the form of reversible evolution but do not select a generator, rate,
physical energy, clock, preparation catalogue or internal observation.
Record cuts alone cannot identify those generators. Present raw activity
without a new record remains mathematically possible; this is not a
proof that nature realizes the added flow family.

Accepted RI-08g and earlier sources remain unchanged. This isolated
obligation adds no cross-bundle adapter, physical dynamics, full QM,
mass/gravity claim, RET integration, registry/claim/operational-ledger
edit or automatic successor. Geometry and the primitive-input horizon
are not advanced by inserting these matrix-law premises. This result is
submitted for independent acceptance, then this sitting stops.
