# The observable quotient of maximal exact-recordability domains

13 September 2026. **FULL_DOMAIN_EFFECT_CLASSIFICATION;
SUBSTOCHASTIC_QUOTIENT_THEOREM; OPERATIONAL_SELECTION_PREMISE_OPEN.**

RI-08a classifies the **entire** exact-recordability domains from the
[domain construction](../t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md),
not another chosen smaller preparation cone. The proposed classification
holds: every bounded real-linear effect depends only on cell weights;
every full-domain positive mass-nonincreasing map induces a substochastic
map of those weights.

This is conditional mathematics about the stated domains and operation
class. It does not show that DET or nature is classical, select a quantum
subdomain, establish physical availability, or claim literature novelty.
Exact examples are in [model.py](model.py) and [check.py](check.py).
All previously accepted research source snapshots remain unchanged.

## 1. Domain and premise ledger

Fix a nonempty finite carrier \(\Omega\) of size \(n\), with a partition
\(P=\{A_1,\ldots,A_k\}\) into nonempty cells. Let
\(s_r=|A_r|\), \(b_r=\mathbf1_{A_r}\), \(v_r=b_r/s_r\), and
\(h_r=v_rv_r^\dagger\). Work in the **real** vector space of complex
Hermitian \(n\)-by-\(n\) matrices. Define

\[
E_P=\{X=X^\dagger:b_r^\dagger Xb_s=0\ (r\ne s)\},\qquad
K_P=E_P\cap\{d\succeq0\},
\]
\[
q_{P,r}(X)=b_r^\dagger Xb_r,\qquad
m_P(X)=\sum_rq_{P,r}(X)=e^\dagger Xe\quad(X\in E_P). \tag{1}
\]

Both real and imaginary parts of each off-cell constraint vanish. The mass
identity is on \(E_P\); it is not asserted for arbitrary Hermitian matrices.

| Ingredient | Status in this result |
| --- | --- |
| Supplied finite partition and exact-recordability criterion | Earlier admitted mathematical construction |
| An effect real-linear on \(E_P\), with \(0\le f(d)\le m_P(d)\) for every \(d\in K_P\) | Load-bearing full-domain assumption |
| A fixed real-linear map on the whole span, positive and mass-nonincreasing on the entire input cone | Additional operational candidate; not implied by event biadditivity |
| Availability fixed by declared record/type/controller, not hidden residual inspection | Required fixed-interface premise |
| All mathematical preparations, cell measurements or substochastic realizations physically available | Not inferred; needed separately for the corresponding operational richness |
| Full committed labels, precursors, records and known external apparatus types | Retained outside the residual quotient |

Maximality means largest domain satisfying this fixed partition's exact
criterion. It is not maximal physical preparability. All theorems are
at the same stated committed prefix and external interface when comparing
states. No ancillary/composite or unbounded-history extension is assumed.

## 2. Actual span, decomposition and positive quotient

**Span lemma.** \(E_P=\operatorname{span}_{\mathbb R}K_P\).
Indeed \(I\in E_P\), and for any \(X\in E_P\), choosing sufficiently large
real \(t\ge0\) makes \(X+tI\succeq0\). Thus
\(X=(X+tI)-tI\) is a difference of two members of \(K_P\).

Let \(U_P=\operatorname{span}_{\mathbb C}\{b_r\}\), let
\(W_P=U_P^\perp\), and let \(\Pi,\Delta=I-\Pi\) be their orthogonal
projections. In particular

\[
\Pi=\sum_r\frac{b_rb_r^\dagger}{s_r}.
\]

The orthogonality of disjoint indicators and the constraints in (1) give
the unique block decomposition

\[
X=\sum_rq_{P,r}(X)h_r+
       (\Pi X\Delta+\Delta X\Pi)+\Delta X\Delta,\qquad X\in E_P. \tag{2}
\]

The visible block has only \(k\) real diagonal coordinates; the visible-dark
cross block is arbitrary complex; the dark block is arbitrary Hermitian.
Writing \(h=n-k=\dim_{\mathbb C}W_P\), this yields

\[
\dim_{\mathbb R}E_P=k+2kh+h^2=n^2-k(k-1),\quad
\dim_{\mathbb R}\ker q_P=2kh+h^2=n^2-k^2. \tag{3}
\]

The word “dark” denotes indicator-orthogonal kernel coordinates, not a
claim about a physical hidden sector.

Define a positive linear section

\[
j_P(x)=\sum_r x_rh_r,\qquad x\in\mathbb R^k. \tag{4}
\]

Since \(b_s^\dagger v_r=\delta_{sr}\),
\(q_Pj_P=I_k\), \(j_P(\mathbb R_+^k)\subset K_P\), and
\(q_P(K_P)=\mathbb R_+^k\). Therefore the quotient \(E_P/\ker q_P\)
is exactly \(\mathbb R^k\) with positive cone \(\mathbb R_+^k\) and
faithful mass \(\mathbf1^\top x\). Its normalized base is the classical
simplex. Closedness and faithfulness follow from this explicit image and
section, not from a claim about arbitrary cone projections.

For \(d\in K_P\), \(m_P(d)=0\) iff \(db_r=0\) for all \(r\), since
\(b_r^\dagger db_r=\|d^{1/2}b_r\|^2\). Thus the positive zero-mass face
is exactly the PSD matrices supported on \(W_P\). Its real span has
dimension \(h^2\), which is generally **smaller** than \(\ker q_P\).
The cross terms in (2) must also be addressed; removing the zero-mass
positive face alone does not prove the effect theorem.

## 3. Bounded-effect classification

**Theorem.** A real-linear \(f:E_P\to\mathbb R\) satisfies
\(0\le f\le m_P\) on the entire \(K_P\) iff

\[
f(X)=\sum_{r=1}^k c_rq_{P,r}(X),\qquad 0\le c_r\le1. \tag{5}
\]

The coefficients are unique, \(c_r=f(h_r)\).

**Proof.** For every \(w\in W_P\), \(ww^\dagger\in K_P\) and has zero
mass, hence \(f(ww^\dagger)=0\). Such rank-one matrices span the Hermitian
dark block over the reals, by real and imaginary polarization. Therefore
\(f(\Delta X\Delta)=0\) for every \(X\in E_P\).

Fix a cell \(r\) and \(w\in W_P\). For **every** complex \(z\),

\[
d_z=(v_r+zw)(v_r+zw)^\dagger\in K_P,\quad
q_P(d_z)=e_r,\quad m_P(d_z)=1. \tag{6}
\]

For real \(z=t\), linearity and the already vanishing dark term give
\[
f(d_t)=f(h_r)+t f(v_rw^\dagger+wv_r^\dagger).
\]
It lies in \([0,1]\) for all \(t\in\mathbb R\); its slope must vanish.
Taking \(z=it\) likewise forces
\(f(iwv_r^\dagger-iv_rw^\dagger)=0\). As the \(v_r\) span the visible
space and \(w\) ranges over the dark space, these are all Hermitian
visible-dark cross directions. Equation (2) now gives (5). Each
\(h_r\in K_P\) has mass one, so \(c_r\in[0,1]\), and evaluating on
the \(h_r\) proves uniqueness. Conversely, nonnegative cell weights and
\(\sum_rq_{P,r}=m_P\) make every coefficient vector in \([0,1]^k\)
a bounded effect. ∎

This is a statement about functionals on \(E_P\), not unique ambient
matrix representatives. If an ambient Hermitian \(F\) represents
\(f(X)=\operatorname{Tr}(FX)\), then

\[
F=\sum_r c_rb_rb_r^\dagger+Y,\qquad Y\in E_P^\perp \tag{7}
\]

is the relevant equivalence class. Visible off-cell real/imaginary terms
in \(Y\) vanish on \(E_P\). A representative outside the displayed cell
matrix span is not a counterexample unless its **restricted functional**
fails (5).

## 4. Full-domain transformations and conditional records

Let \(Q\) be another finite partition, possibly on another finite carrier.
Let \(T:E_P\to E_Q\) be fixed and real-linear, with
\(T(K_P)\subseteq K_Q\) and \(m_QT\le m_P\) on all of \(K_P\).
No positive extension to the whole ambient Hermitian cone is required.

**Map theorem.** There is a unique nonnegative column-substochastic matrix
\(A_T\) such that

\[
q_QT=A_Tq_P\quad\text{on }E_P,\qquad
(A_T)_{sr}=q_{Q,s}(Th_r),\quad
\sum_s(A_T)_{sr}\le1. \tag{8}
\]

**Proof.** Each \(q_{Q,s}T\) is nonnegative and bounded by \(m_QT\le m_P\).
The effect theorem gives its row of \(A_T\). Positivity gives nonnegative
entries, and the mass bound evaluated on \(h_r\) gives each column sum.
Equality holds on \(E_P\), not only on normalized preparations. ∎

Thus \(T(\ker q_P)\subseteq\ker q_Q\). Every lawful continuation factors,
and composition gives \(A_{T_2T_1}=A_{T_2}A_{T_1}\). This does **not**
mean \(T=j_QA_Tq_P\): many full residual maps induce the same \(A_T\),
including different growth of operationally invisible coordinates.

For a complete instrument with full labels \(\alpha\), distinct output
types \(Q_\alpha\) and branch maps \(T_\alpha\), keep each
\(A_\alpha\) separately. Completeness implies
\(\sum_\alpha\mathbf1^\top A_\alpha=\mathbf1^\top\). Coarsening a
requested view does not erase already committed fine labels.

For normalized \(d\), a selected branch has
\[
p_\alpha=\mathbf1^\top A_\alpha q_P(d),\qquad
q_{Q_\alpha}(T_\alpha d/p_\alpha)
  =A_\alpha q_P(d)/p_\alpha\quad(p_\alpha>0). \tag{9}
\]

When \(p_\alpha=0\), the quotient output is zero, but \(T_\alpha d\)
can still be a **nonzero** positive dark kernel. Do not normalize it or
append an event. For example a cell cut applied to
\(h_s+ww^\dagger\), with \(s\ne r\) and nonzero \(w\) supported dark
inside cell \(r\), leaves \(ww^\dagger\) with zero mass.

A commit retains the full setting/action/outcome, allowed precursor ideal,
output type and chosen residual update, then appends one fresh maximal
event without changing the existing record/order. This theorem quotients
residual predictions only; it neither identifies different committed
prefixes nor discards event order. The precursor and apparatus rule remain
part of the declared law, not a consequence of (8).

## 5. At most classical versus an available classical theory

Equation (8) bounds the information in any catalogue meeting the full-domain
premises: terminal bounded effects and finite sequences of positive
mass-nonincreasing branches factor through cell weights. Extra declared
record/controller types remain as types, with corresponding block matrices.
They are not an oracle for hidden residual-dependent operation availability.

Three levels must remain distinct:

- **At most this informative:** a restricted available catalogue may
  distinguish fewer states than \(q_P\). The classification bounds it
  above; it does not supply the missing measurements.
- **Exact residual equivalence:** if the cell readout with effects
  \(q_{P,r}\) is available, unequal cell weights are distinguishable.
  Within the same prefix/type, equality of all declared finite future
  predictions is then exactly equality of \(q_P\). Only the actually
  available preparations are compared.
- **The full finite classical operational catalogue:** availability of
  every simplex preparation, cell readout/classical postprocessing and
  the required transition instruments is an additional premise. Mathematical
  existence of their representations is not physical availability.

For the last level, every substochastic \(A\) has the explicit mathematical
realization

\[
T_A=j_QAq_P,\qquad
T_A(d)=\sum_s(Aq_P(d))_s h_s^{Q}. \tag{10}
\]

This is positive on all \(K_P\), lands in \(K_Q\), and is mass-nonincreasing.
Collections of such maps with joint column sums one realize complete
classical instruments. The section (4) realizes every preparation weight.
Calling these **available** measure-prepare operations would be a separate
catalogue admission, not a DET deduction.

If the operation is allowed only on a proper preparation subdomain,
the unbounded rank-one families (6) need not remain available in that domain,
and its effects may evade (5). Likewise a catalogue chosen after inspecting
the unknown residual is not a fixed full-domain interface. If an availability
decision is itself a physical bounded full-domain test, its effect is subject
to the same theorem; it cannot silently reveal extra coordinates.

A concrete partial-domain exception is the two-shape cone generated by
\[
a=\begin{pmatrix}1/3&1/6\\1/6&1/3\end{pmatrix},\qquad
b=\begin{pmatrix}1&-1/2\\-1/2&1\end{pmatrix}.
\]
Both have one-cell weight one. On \(xa+yb\), \(x,y\ge0\), the effect
\(f(xa+yb)=x\) is bounded by \(m=x+y\), but it distinguishes \(a\)
from \(b\). It is **not** bounded on the entire one-cell PSD cone:
for the normalized rank-one block with all entries \(1/4\), its same
linear formula \(f=3d_{00}/2+3\operatorname{Re}d_{01}\) gives \(9/8\).
That block is \((9a-b)/8\), so the offending value is already forced on
the two-shape real span, not chosen through an arbitrary ambient extension.
This is a smaller-domain exception, not a refutation.

The [accepted selected-context switch](../t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md)
operationalizes this kind of distinction under supplied controls:
its two shapes share source cell weights but can produce different target
weights. Equation (8) explains why such a switch cannot be a lawful
full-domain map; the previous explicit nonextension counterexample remains
valid. No smaller quantum domain is selected in this sitting.

## 6. First commitments: quotient convergence only

For a fixed prefix and finite declared controller, mutually exclusive silent
and committing branches induce finite substochastic block matrices on the
cell-weight quotients. Their orthant cones have faithful mass and compact
normalized bases. The accepted
[RI-07 theorem](../t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md)
therefore applies to their first-commit sums, retaining every full committing
label, output quotient residual and complementary never-commit probability.
Availability and coefficients must be fixed as stipulated, not chosen by a
hidden residual oracle. RI-07 requires finitely many full labels and one
fixed policy/controller experiment. It forgets silent counts/paths only when
the declared observation interface permits it; a path tag in an actual
record must remain in its label. Never-commit probability supplies no
limiting residual state or finite-time diagnosis.

This does **not** establish convergence of the original nonfaithful kernel
maps. Whenever \(W_P\ne0\), a counterexample lives on the whole \(K_P\):

\[
M=\tfrac12\Pi+2\Delta,\qquad S(d)=MdM^\dagger,\qquad
B(d)=\tfrac34d. \tag{11}
\]

Both maps are positive and preserve \(K_P\), with
\(q_PS=q_P/4\), \(q_PB=3q_P/4\). Thus
\(m_PS+m_PB=m_P\); completeness is a mass identity, not \(S+B=I\).
For \(d=h_r+ww^\dagger\), \(0\ne w\in W_P\), the input has mass one
and

\[
\sum_{n=0}^{N-1}BS^n(d)
=(1-4^{-N})h_r+\frac{4^N-1}{4}\,ww^\dagger. \tag{12}
\]

The dark component diverges. In contrast its quotient is
\((1-4^{-N})e_r\to e_r\), with never-commit mass zero. No original
infinite residual is inserted into an identity requiring its existence.
Full kernels may still be retained for questions outside this catalogue;
the quotient is justified only for its declared continuations.

## 7. Boundaries, evidence and remaining premise

For one cell, \(E_P=\mathrm{Herm}_n\), \(K_P\) is the full PSD cone,
and \(q_P=m_P\): (5) reduces to the earlier
[full-cone no-information obstruction](../t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md).
For all singleton cells, \(W_P=0\) and \(K_P\) is exactly the nonnegative
diagonal cone, already faithfully normalized. Unequal cell sizes change the
section normalization \(v_r=b_r/s_r\), not the classification.

What this adds is a classification for **every finite partition**, including
all complex dark/cross directions, every bounded effect on the actual span,
and every full-domain positive mass-nonincreasing continuation. It explains
why a fixed context can retain the earlier \(3/4\) versus \(1/4\) coherent
readout while still having only cell weights as its full-domain operational
quotient: those two inputs already have different cell weights.

The independent checks cover span identities and dimensions, unequal cells,
real/imaginary rank-one families, one-cell/singleton boundaries, effect and
map realizations, positive-branch and zero-mass limits, and the original
kernel divergence. The proof, not finitely sampled inequalities, establishes
the all-domain statement. Source hashes, internal independent reviews and
reproduction are in the [handoff](../../coordination/QR_HANDOFF.md).

**Precise remaining premise:** the admitted DET fragment has not selected
which mathematically recordable kernels are physical preparations or which
transformations/tests are available. A richer-than-cell-weight operational
result must depart from at least one of the theorem's full-domain,
fixed-catalogue, real-linear positivity/mass-boundedness assumptions.
Which departure DET justifies, and how its allowed domains compose and
support subsequent records, remains open. No particular departure or
quantum reconstruction axiom is adopted here.

This is a completed conditional classification and counterexample, not a
conclusion that nature is classical. No ancillary/composite extension,
geometry/mass/gravity result, literature novelty, RET change, QR-05 lettered
gate, clock/book work or physical promotion follows. The sitting stops for
coordinator acceptance before any successor assignment.
