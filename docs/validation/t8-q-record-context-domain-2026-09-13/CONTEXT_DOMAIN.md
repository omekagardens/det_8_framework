# QR-MAP: conditional record domains and the context-transition gap

13 September 2026. **CONDITIONAL_DOMAIN_CONSTRUCTION;
SERIAL_CLOSURE_COUNTEREXAMPLE; PHYSICAL_CONTEXT_LAW_NOT_SELECTED.**

This continues the [operation-domain obligation](../t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md).
The unrestricted positive-kernel linear instrument candidate was rejected.
We now construct domains directly from the already-declared exact-recordability
criterion, without inserting a physical Hilbert space or a quantum instrument.

**Positive result:** each supplied record partition determines a closed convex
kernel domain with normalized readout and mathematically admissible conditional
cuts. These domains retain the earlier coherence-sensitive \(3/4\) versus
\(1/4\) example. **Limits:** this does not select physical preparations, a
partition, a unique update, or the next context. Common initial recordability
does not imply serial closure. A separate symmetry counterexample rules out
one proposed automatic deterministic context selector.

These are theorems and rejected constructions, not a full QM derivation.
No new lettered gate, growth executor, geometry fixture, global axiom or
physical experiment is introduced.

## 1. Input ledger: a record question is still supplied

The admitted [finite fragment B_D](../t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md#1-fix-the-source-theory-before-making-an-implication-claim)
contains a finite residual possibility carrier \(\Omega\), a strongly positive
pair-kernel, and readout on a **declared exactly decoherent partition**.
It does not assert that every mathematically admissible kernel is a physically
available preparation, or that every recordable question is an available
apparatus operation.

Fix a partition \(P=\{A_1,\ldots,A_k\}\) into nonempty cells. Here a
nontrivial partition has more than one cell; the indiscrete partition has one.
Its cells are
possibility alternatives, not preallocated future vertices. Put
\[
b_r=\mathbf1_{A_r},\qquad E_r=\operatorname{diag}(b_r),\qquad
e=\mathbf1_\Omega,\qquad m(d)=e^\dagger d e.
\]

The domain construction below follows from this supplied \(P\) and the admitted
matrix conditions. Treating its whole normalized slice as a physical system
type is a further candidate interpretation, **not** a newly proved premise.
Any control or apparatus data selecting \(P\) must be accounted for explicitly.
The [activity/commit/access contract](../../track_b/RECORD_PROCESS_CONTRACT.md)
remains the implementation boundary.

## 2. Exact-domain theorem and conditional commit maps

Define
\[
\mathcal K_P=
\{d\succeq0:\ b_r^\dagger d b_s=0\text{ for }r\ne s\}.
\tag{1}
\]

**Theorem.** \(\mathcal K_P\) is a closed convex cone. It is exactly the
largest set of positive kernels satisfying the admitted exact-recordability
criterion for this **fixed partition**, and on it
\[
\mu_r(d)=b_r^\dagger d b_r\ge0,\qquad
\sum_r\mu_r(d)=m(d).
\tag{2}
\]

**Proof.** The constraints in (1) are homogeneous real-linear equations in
the Hermitian entries, with real and imaginary parts both zero. Intersecting
their closed linear solution space with the PSD cone gives the stated cone.
Expanding \(e=\sum_rb_r\) makes the mass identity immediate; positivity gives
each nonnegative weight. Maximality here means precisely satisfaction of
this criterion, not maximality of a physically available preparation domain.
\(\square\)

Mere normalization of raw weights is weaker. For example
\[
d=\begin{pmatrix}1/2&i/4\\-i/4&1/2\end{pmatrix}
\]
is positive and normalized, and its singleton weights sum to one, but it is
not exactly decoherent. Accidental cancellation of cross terms does not
license the stronger recordability assertion.

For the supplied \(P\), define unnormalized cuts
\[
T_r(d)=E_rdE_r.
\tag{3}
\]
These maps are linear and positive on the ambient cone. Their outputs are
supported on \(A_r\), hence lie in \(\mathcal K_P\); on that domain
\[
m(T_r(d))=\mu_r(d),\qquad \sum_rm(T_r(d))=m(d).
\]
If \(\mu_r(d)>0\), \(d_r=T_r(d)/\mu_r(d)\) is a normalized kernel and a repeated
\(P\) readout returns \(r\) with certainty. This is the existing
[same-history conditioning rule](../t8-q-strict-derivation-2026-09-12/DERIVATION.md#5-conditional-histories-are-derived-physical-updates-are-not-unique)
written as an explicit conditional-domain map. Promoting it to an actual
postinteraction update is still an additional law choice.

The full-cone no-information theorem is not bypassed by notation. The cut
effects sum to
\[
H_P=\sum_rb_rb_r^\dagger,
\]
For a nontrivial partition, \(H_P\ne\Gamma=ee^\dagger\) on the ambient
matrix space. Nevertheless \(\operatorname{Tr}[(H_P-\Gamma)d]=0\) is
guaranteed on \(\mathcal K_P\); the converse need not hold. For the
indiscrete partition, \(H_P=\Gamma\) and the sole outcome is uninformative.
Completeness of a nontrivial readout has been restricted honestly, rather
than asserted on every positive kernel.

These maps do not select a precursor ideal or a fresh-event law. To obtain
a QR-MAP commit, a complete \(L\) must also supply the allowed ideal, context
and record tags, outcome sampling and output residual rule. A positive
conditional branch can then append a fresh maximal event. None of that is
replaced by scalar readout weights alone.

### Zero-mass and classical boundaries remain

For \(P=\{01\mid2\}\),
\[
d=\begin{pmatrix}1&-1&0\\-1&1&0\\0&0&1\end{pmatrix}
\tag{4}
\]
is positive, normalized and in \(\mathcal K_P\). Its weights are \(0,1\),
but \(T_0(d)\ne0\). That zero-weight branch is never normalized or committed.

More generally, for \(d\in\mathcal K_P\), \(m(d)=0\) implies
each \(b_r^\dagger d b_r=0\). Positivity then gives \(db_r=0\). Thus the
zero-mass part of this cone consists exactly of PSD matrices supported on
\(\operatorname{span}\{b_r\}^{\perp}\). It is nontrivial whenever some cell
contains more than one atom. The earlier residual-convergence warning is
therefore not removed merely by adopting a recordable domain.

Every classical distribution over the cells can also occur: choose one atom
in each \(A_r\) and give those diagonal entries arbitrary weights summing
to one. Fixed-context normalization and repeatability do not select QM.

## 3. What composes, and what does not

**Convex mixtures and coarse questions.** Equation (1) is preserved under
positive mixtures. If \(Q\) coarsens \(P\), sums of its zero cross terms show
\(\mathcal K_P\subseteq\mathcal K_Q\); its coarse weights are sums of the
fine weights. This is mathematical convexity, not a proof of physical
randomization or preparation closure.

But coarse weights do not determine a residual update:
\[
E_{\cup_{r\in I}A_r}dE_{\cup_{r\in I}A_r}
\quad\text{need not equal}\quad
\sum_{r\in I}E_rdE_r.
\tag{5}
\]
Exact aggregate decoherence does not zero every atomic cross-block entry.
For example
\[
d=\frac13
\begin{pmatrix}1&0&1/2\\0&1&-1/2\\1/2&-1/2&1\end{pmatrix},
\qquad P=\{01\mid2\}
\tag{6}
\]
is positive, normalized and exactly \(P\)-recordable. The whole-carrier cut
is the identity operation, whereas the sum of the two fine cuts deletes its
nonzero cross-block entries. Both have total output mass one.

Coarse-graining the labels of a specified instrument sums its actual branch
maps; it does not authorize replacing them with a different coarse-cut map.
If fine records have already committed, a later coarse access view also
does not erase them from committed history.

**Declared products.** For supplied product carriers, \(d\in\mathcal K_P\)
and \(h\in\mathcal K_Q\) imply
\[
d\otimes h\in\mathcal K_{P\times Q}.
\]
Positivity, cross terms, masses and cuts factor in the usual finite matrix
product construction. This does not prove which physical subsystems or
correlated joint preparations exist.

**An admissible silent family.** Set \(S=\operatorname{span}\{b_r\}\).
In coefficient coordinates its orthogonal projection is
\[
\Pi_S=\sum_r\frac{b_rb_r^\dagger}{|A_r|}.
\]
The matrices \(M_\lambda=\Pi_S+\lambda(I-\Pi_S)\), \(\lambda>0\), fix
every \(b_r\). Therefore \(d\mapsto M_\lambda dM_\lambda^\dagger\) preserves
\(\mathcal K_P\), its mass and every \(P\)-weight; the inverse uses
\(1/\lambda\). Unless \(S\) is the whole space or \(\lambda=1\), these are
nonunitary transformations. This is coefficient-space linear algebra, not
a physical Hilbert-space premise, selected dynamics or clock parameter.

In particular, the restriction (1) does not itself eliminate arbitrary
growth of positive zero-mass components or force unitary quantum dynamics.

## 4. Exact counterexample: two current contexts need not compose

Retain the earlier coherence-sensitive kernels
\[
d(c)=
\begin{pmatrix}
1/4&c&0&0\\c&1/4&0&0\\
0&0&1/4&-c\\0&0&-c&1/4
\end{pmatrix},\qquad c=\pm1/8.
\tag{7}
\]
Their eigenvalues are \(1/4\pm c\), each twice, so they are positive definite
with mass one. Let
\[
P=\{01\mid23\},\qquad Q=\{02\mid13\}.
\]
Both are exactly recordable on each input:
\[
K_P=(1/2+2c,1/2-2c),\qquad K_Q=(1/2,1/2).
\tag{8}
\]
Thus the domain construction retains the \(3/4\) versus \(1/4\) distinction.
No qubit or amplitude model is inserted to obtain it.

Now take the positive \(P_0\) cut and normalize by \(\mu=1/2+2c\). On the
resulting \(d'\), the \(Q\) cross term is \(c/\mu\ne0\). Its two raw weights
are each \(1/(4\mu)\), summing to
\[
\frac1{2\mu}=
\begin{cases}2/3,&c=1/8,\\2,&c=-1/8.\end{cases}
\tag{9}
\]
Consequently \(d'\notin\mathcal K_Q\). These are **not** a licensed second
probability distribution. Dividing them by their sum would add a new rule;
it is not a correction of roundoff or detector noise.

**Rejected summary:** “both questions are currently recordable” is not a
certificate of jointly or sequentially available operations. The common
refinement here is the singleton partition and is not recordable either;
there is no exactly recordable partition refining both \(P\) and \(Q\).
Hence “choose the unique finest recordable partition” also fails as a
general construction.

For cut-based \(P\) followed by \(Q=\{B_s\}\), the exact branch condition is
\[
D(A_r\cap B_s,A_r\cap B_t)=0
\quad(s\ne t)
\tag{10}
\]
for every branch with \(\mu_r>0\). This follows directly by substituting the
conditional kernel; initial \(D(B_s,B_t)=0\) is insufficient. Equation (10)
is a conditional admission test, not a physical process that makes it hold.
A separately justified interaction might establish the next context, but
such an interaction has not been derived here.

Nor do (2), positivity and repeatability choose the cut update uniquely.
For any normalized positive \(h_r\) supported in \(A_r\),
\[
R_r(d)=\mu_r(d)h_r
\tag{11}
\]
has the same weights and \(P\)-repeatability, but can prepare a different
residual atom and hence different later records. This preserves the earlier
update-underdetermination result; it is not a proposed replacement law.

## 5. Exact obstruction to an automatic symmetric context selector

One might instead try to infer a privileged context directly from \(d\).
Consider a selector required to:

1. Depend deterministically on the kernel alone, without extra apparatus,
   ordered-label or symmetry-breaking record input.
2. Be covariant under relabeling the possibility atoms.
3. Return a nontrivial exactly recordable partition whenever one exists.

These are candidate requirements, not axioms already proved from B_D.
In particular, possibility-label covariance is distinct from the program's
incomparable-birth covariance.

On five atoms take
\[
d_*=\frac1{40}
\begin{pmatrix}
8&1&-1&-1&1\\
1&8&1&-1&-1\\
-1&1&8&1&-1\\
-1&-1&1&8&1\\
1&-1&-1&1&8
\end{pmatrix}.
\tag{12}
\]
Its diagonal exceeds the sum of absolute off-diagonal entries by \(1/10\)
in every row, so \(d_*\succeq(1/10)I\). Every off-diagonal row sum is zero,
giving \(m(d_*)=1\). Cyclic rotation of the five atoms leaves it unchanged.
Each singleton/complement partition is exactly recordable with weights
\(1/5,4/5\).

**Theorem.** No selector satisfies all three requirements on every kernel.

**Proof.** At \(d_*\), covariance and determinism require the selected
partition to be invariant under the cyclic group \(C_5\). That group is
transitive on the five atoms, so every block of an invariant partition has
the same size. Since five is prime, such a partition is either indiscrete
or discrete. The discrete partition is not exactly recordable because all
its atomic off-diagonal entries are nonzero. Only the indiscrete partition
remains, contradicting the third requirement. \(\square\)

This does **not** forbid a record-controlled or stochastic selector.
Meaningful control data can break the symmetry. A law could also randomize
among admissible contexts; choosing such a distribution is additional law
data. The finite set-valued map
\[
\operatorname{Adm}(d)=\{P:d\in\mathcal K_P\}
\]
is canonical and relabeling-covariant, but a set of admissible questions is
not their physical availability, an occurrence law or a unique choice.

## 6. Adjudication and next obligation

**Established conditionally:** exact record domains, informative normalized
readouts, cut and reset candidates, coarse-weight/product identities and
domain-preserving silent congruences. They use the admitted kernel calculus
and a supplied partition, not the full quantum reconstruction package.

**Rejected:** common domain membership as sufficient for sequential
availability; a unique finest recordable context; and a deterministic,
kernel-only, relabeling-covariant selector that always makes a nontrivial
choice. These are specific constructions, not a shutdown of QR-MAP.

**Not established:** a physical preparation domain or a DET-forced context,
update or generator. These conditions still admit classical cell
distributions and nonunitary silent maps. Retaining the exhibited coherent
preparations physically is an explicit research target, not a consequence
of writing their matrices.

The next concrete obligation is a **record/apparatus-conditioned context
transition law**: identify which declared physical principle makes a test
available, specify how its interaction puts the residual into the next
licensed domain, and retain the full record, residual update and precursor
choice. A stochastic selector or additional availability axiom may be
investigated, but must be labeled as such and tested against (9)–(12).
The existing conditional quantum completion is an openly assumed benchmark,
not a proof that this law has been derived from DET.

Mass and gravity remain authorized targets. No geometric or matter-coupling
result follows here, the two-port width obstruction remains, and neither
Option B nor Status M changes. RET, clocks, book work and retired κ-gravity
are untouched.

## 7. Verification

The accompanying [check.py](check.py) uses standalone exact rational arithmetic
for the finite witnesses, not a growth executor or a numerical physical model.
Universal claims rest on the proofs above. Its finite enumeration of the 52
five-atom partitions checks the specific symmetry counterexample; it is not
a coverage claim about physical processes or a new research gate.

**Verification:** all 10 new witness tests pass, and the existing 73 scoped
checks pass: **83 distinct tests, all passing normally and under optimized
Python (`-O`)**. Ruff checking and formatting pass. Independent mathematical
and source-scope reviews checked the proofs; their corrections concerning
accidental normalization and the one-cell partition are incorporated. No Lean
or empirical verification is claimed.

From the repository root:

```sh
.venv/bin/python docs/validation/t8-q-record-context-domain-2026-09-13/check.py
.venv/bin/python -O docs/validation/t8-q-record-context-domain-2026-09-13/check.py
.venv/bin/ruff check docs/validation/t8-q-record-context-domain-2026-09-13/check.py
```

Checked source SHA-256 (`check.py`):
`0a273d2c16f9e9a69178c494170f7b15294c7e2faf0fa82f94e23c233131da86`.
This identifies the tested source; it is not an independently frozen theorem
certificate.
