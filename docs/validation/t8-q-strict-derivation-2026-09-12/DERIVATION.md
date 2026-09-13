# QR-MAP: stricter derivation from the admitted pair-kernel

12 September 2026. **DERIVED_FROM_ADMITTED_D; FULL_QM_NOT_DERIVED.**
The owner requests a stricter DET-derived quantum account. This sitting
removes the preceding candidate's assumed noncommutative multiplication
table and compression law from the derivation inputs. It does not rename
those assumptions as theorems or change the Track-A primitive list.

**Positive result:** the admitted pair-kernel already supplies a canonical
finite Hilbert representation, norm-squared record weights, and an explicit
same-diagonal / different-readout example. **Obstruction:** it does not
determine a physical measurement algebra, residual update or future law.
The two statements are proved separately below; no new QR-05 gate opens.

## 1. What "derived" means here

The current [primitive declaration](../../../MODEL_CARD.md#2-primitives)
labels D a **candidate**. The
[pair-kernel proposal](../../record_kernel_physics.md#31-proposed-pair-kernel)
specifies its axioms; its [open reconstruction items](../../record_kernel_physics.md#34-what-it-does-not-yet-derive)
already distinguish Gram representation from general quantum theory.

| Item | Status in this derivation |
| --- | --- |
| Finite possibility set Ω and its Boolean event algebra | Declared data; alternatives, not uncommitted event vertices |
| Complex-valued D, Hermiticity, biadditivity, strong positivity and D(Ω,Ω)=1 | Admitted candidate premises; not derived from ontology/order alone |
| A complete exactly decoherent partition P={A_r} and record readout K(r)=D(A_r,A_r) | Declared recordability/readout rule; its normalization is derived, its physical selection is not |
| Committed C=(V,≺,R), counting and stable abstract L | Retained architecture; these do not specify the missing local quantum law |
| Hilbert space, amplitudes, dimension, event operators | Not supplied; distinguish derived mathematical representations from realizable operations |
| Pair-groupoid algebra, compression, two-port grammar and fixed action weights | Not premises here; previous assumed candidates remain isolated |
| Metric, coordinates, propagator, Hamiltonian, physical tensor split | Not inputs and not recovered claims |

There are two different derivation demands. **Relative to admitted D**, the
theorems below follow. **From the older record/order ontology without D's
axioms**, a forcing theorem is still missing. In particular, using D with
codomain C cannot also count as deriving why nature selects complex scalars.
Approximate decoherence is not substituted for the exact premise: in general
Σ_r μ(A_r)=1−Σ_(r≠s)D(A_r,A_s), which need not equal one.

## 2. Canonical finite representation — an actual derivation

Write d_ij=D({i},{j}). Strong positivity is equivalent, in this finite
setting, to d being Hermitian positive semidefinite. On the free formal
complex vector space F_Ω define

\[
\langle x,y\rangle_D=\sum_{i,j}\overline{x_i}d_{ij}y_j,
\quad N_D=\{x:\langle x,x\rangle_D=0\}=\ker d,
\quad H_D=F_\Omega/N_D.
\]

Cauchy–Schwarz makes every null vector orthogonal to every vector, so the
inner product descends and is positive definite on the quotient. Finite
dimension gives completeness. Thus H_D is a Hilbert space **constructed
from d**, with dimension rank d; no fixed qubit or physical Hilbert space
was inserted. Define |A⟩=[1_A] and ψ=|Ω⟩. Then

\[
D(A,B)=\langle A|B\rangle_D,\quad
|A\sqcup B\rangle=|A\rangle+|B\rangle,\quad
\mu(A)=\|A\|_D^2,\quad\|\psi\|_D=1.
\]

Consequently |D(A,B)|²≤μ(A)μ(B), pair interference is 2 Re D(A,B),
and I₃=0 for mutually disjoint triples, by cancellation of pair terms.
For any other spanning Gram realization with the same d, the map
[x]↦Σ_i x_i v_i is well-defined, inner-product preserving and onto.
It is the unique unitary intertwining the labeled event vectors. This is
representation uniqueness, not uniqueness of a physical state space or law.

This restates the existing T2/T2b consequence as a finite, explicit proof;
it is established quantum-measure mathematics, not a new DET discovery.
See Dowker, Johnston and Sorkin,
[Hilbert Spaces from Path Integrals, §2.3](https://arxiv.org/html/1002.0589v3#S2.SS3).
Their subsequent ordinary-QM identifications also use specified quantum
dynamics; we do not import those dynamics to construct d here.

For the declared exactly decoherent record partition, |A_r⟩ are orthogonal
and sum to ψ. On H_record=span{|A_r⟩}, define P_r as the projection onto
the ray of |A_r⟩, or zero when that vector is null. These derived projections
sum to the identity **on H_record**, and

\[
K(r)=\mu(A_r)=\|P_r\psi\|_D^2,\qquad\sum_rK(r)=1.
\]

This is an exact Born-form representation of the declared record rule.
It does not derive a probability assignment on all conceivable measurements.
Nor is the full kernel interchangeable with these scalar weights or rays.

## 3. Coherence-sensitive readout without the added qubit algebra

Use four primitive alternatives, Ω={0,1,2,3}, and record cells
A={0,1}, B={2,3}. Take the two explicitly supplied input kernels

\[
d(c)=\begin{pmatrix}
1/4&c&0&0\\c&1/4&0&0\\
0&0&1/4&-c\\0&0&-c&1/4
\end{pmatrix},\qquad c=+1/8\text{ or }-1/8.
\]

Their eigenvalues are 1/4+c and 1/4−c, each twice; both are positive
definite. Both have the same atomic diagonal (1/4,1/4,1/4,1/4), total-entry
mass one and D(A,B)=0. At the same C, event alphabet and record question,

\[
K_c(A)=\tfrac12+2c=\begin{cases}3/4&c=1/8,\\1/4&c=-1/8,\end{cases}
\qquad K_c(B)=1-K_c(A).
\]

No Hilbert space, amplitude, projector, noncommutative product, compression
or action-weight rule generates these numbers. They follow directly from
the two primitive kernels and the already-declared record rule. This rejects
the diagonal-only summary for this record question with fewer assumptions
than the earlier coherent-readout candidate.

The kernels and partition are **input examples**, not a derived initial
state, a partition chosen by L or an identified apparatus. Unlike the prior
joint action/outcome example, 3/4 and 1/4 here are the actual record-cell
probabilities: there is no extra action factor of 1/3. H_D is reconstructed
from each d; a common preparation-independent physical Hilbert realization
is not silently assumed.

## 4. Exactly where event vectors stop being measurement operators

**Prepared-state projection criterion.** For a binary event A, an orthogonal
projection P on H_D with Pψ=|A⟩ exists iff D(A,Aᶜ)=0. Necessity follows
from orthogonality of Pψ and (I−P)ψ. For sufficiency project onto the ray
|A⟩, using P=0 for a null |A⟩. This realizes a branch of the specified ψ,
not an operation on all alternative histories.

**All-history sharp-cut criterion.** On F_Ω let E_A x=1_A x. It induces
a quotient map iff E_A ker d⊆ker d. If it does, it is an orthogonal
projection on H_D iff

\[
E_A d=dE_A\quad\Longleftrightarrow\quad
d_{ij}=0\text{ whenever }i\in A,\ j\notin A.
\]

Proof: self-adjointness on all quotient vectors is exactly
x†E_A d y=x†dE_A y for every x,y. Conversely that equality preserves
ker d and gives a self-adjoint idempotent. Requiring it for **every
singleton** makes d diagonal. Thus interpreting every Boolean cut as a
sharp quantum operation would erase the off-diagonal structure we retained.
This rejects that particular construction, not all quantum reconstruction.

Two exact witnesses locate the distinction:

- d=J₂/4 (J₂ has every entry one) is normalized and positive. The null
  vector (1,−1) is taken by the first-atom cut to (1,0), with norm²=1/4.
  That cut does not even descend to H_D.
- d=(1/3)[[1,0,1/2],[0,1,−1/2],[1/2,−1/2,1]] is positive definite.
  For A={0,1}, B={2}, D(A,B)=0 and the weights are 2/3 and 1/3,
  but atomic cross entries ±1/6 make E_A non-self-adjoint. Here quotient
  descent holds; the stronger sharpness condition fails.

In the second example u_A=(1,1,0), u_B=(0,0,1) and w=(1,−1,−1)
are pairwise D-orthogonal, with squared norms 2/3,1/3,1/3. The record
rays span only two of the three dimensions. Assigning the w-complement
to either outcome gives two full projective decompositions with the same
P_r ψ=|A_r⟩ but different action on w. Hence even a full projective
extension is not selected by the current record probabilities.

One can always form End(H_D) mathematically. Declaring all its operators
physically realizable, assigning them to apparatus settings, or choosing a
tensor factorization is **additional physical structure**, not a consequence
of being able to construct that algebra.

## 5. Conditional histories are derived; physical updates are not unique

For μ(A)>0, the same-history conditional kernel

\[
D\vert_A(U,W)=D(U\cap A,W\cap A)/\mu(A)
\]

is Hermitian, strongly positive, biadditive and normalized on the original
carrier (or its restriction to A). Conditioning subsequently on B agrees
with direct conditioning on A∩B whenever **both required masses are
positive**. Positivity of μ(A∩B) alone does not imply positivity of μ(A):
quantum measures need not be monotone.

An impossible raw block must not be normalized or replaced by an invented
state. For d=[[1,−1,0],[−1,1,0],[0,0,1]], the complete record partition
{0,1}|{2} is decoherent and has weights 0,1. The first raw block is nonzero
positive with total mass zero. This is consistent with |{0,1}⟩=0; its
individual subevent vectors have not vanished. A zero record probability
does not generally make the entire restricted kernel zero.

**Residual-update underdetermination.** This can be proved without supplied
quantum operators. On a fixed recordable partition A_r={r0,r1}, let
σ_(r,b) be the unit diagonal kernel at rb, b=0 or 1. The two branch families

\[
T^{(b)}_r(d)=\mu_d(A_r)\,\sigma_{(r,b)}\qquad(b=0,1)
\]

are positive linear maps, preserve summed record mass on this recordable
domain, yield the same K(r) for every input, and repeat the recorded cell
with certainty. Their zero-weight outputs are identically zero. They can
keep the identical committed past and append identical coarse records.
Nevertheless, on d=I₄/4 their positive conditional residuals select
different atoms. A later finer record distinguishes them with probabilities
one versus zero. Thus normalization, positivity, recordability and
repeatability do not select a unique quantum residual update.

These are countermodels to uniqueness, not replacement physical laws.
The same-history restriction above is a valid conditional description;
declaring it, either reset rule, or the earlier compression to be an
actual postmeasurement transition still needs a justified L.

**Future-law underdetermination.** Even an exact old-kernel marginal does
not choose the next record law. For any probability vector q, define

\[
d^q_{(i,x),(j,y)}=d_{ij}\delta_{xy}q_x.
\]

Each extension is positive, normalized and exactly decoherent between
different x; summing x,y recovers d. The two fixed rules q=(1,0) and
q=(1/2,1/2) preserve the same old d but give different next-record laws.
Each uses one stable rule, not an ambient-stage change. This is the explicit
bare-extendability limitation, also identified in
[the existing local analysis](../../../det8/models/record_extendability.py).
The x labels are possibilities, not vertices allocated before commit.
No such extension is adopted here as a DET-derived birth law.

## 6. Field and premise checks: do not inherit stronger local claims

Real pair-kernels need not be classical: d=(1/6)[[2,1],[1,2]] is normalized
and positive, with pair interference 1/3. Interference is 2 Re D(A,B),
not restricted to the imaginary part. The contrary sentence in the older
assessment in `docs/record_kernel_physics.md` is not used as a premise.

Likewise, a complex structure is not generally G⁻¹Ω for d=G+iΩ. Let
J₀=[[0,−1],[1,0]] and d_t=(I+i tJ₀)/2, 0<t<1. The eigenvalues are
(1±t)/2 and the total mass is one, but

\[
(G^{-1}\Omega)^2=-t^2I\ne-I.
\]

Ordinary planar rotations preserve both G and Ω. For t=1/2 even these
reversible transformations coexist with the failed identity. The specially
compatible G=I, Ω=J₀ construction in `det8/models/why_complex.py` cannot
be promoted to a theorem for every admitted d. Rescaling/polar-normalizing
the skew map may define a compatible structure under further conditions;
that is not the asserted identity or a physical field-selection theorem.
No global source or governance file is changed in this research sitting.

## 7. Strict outcome and stopping boundary

**Derived from admitted D:** canonical labeled Hilbert representation;
grade-two interference; exact record probabilities in Born form; the
four-atom fixed-diagonal readout separation; the conditional-history
identity; and the stated operator/update obstruction theorems.

**Still not derived:** D's axioms from record/order alone; complex field
selection; a physical partition selector; a preparation-independent
measurement/operation algebra; unique residual and future dynamics;
subsystem composition or quantum-sensitive causal growth. The abstract
name L cannot substitute for those specifications. The old explicitly
assumed coherent-readout F remains a conditional model and fails promotion
to a strictly forced DET-native quantum law at its algebra/update premises.

This is stricter than the previous model because fewer mathematical
structures are inputs—not because full QM has been declared recovered.
No physical predictions are changed or tested. No geometry, empirical
discriminator, new QR-05 letter, coverage/noncollapse/identifiability sequel,
RET, clocks, book, κ-gravity, shared API or primitive-list edit is included.
Option B, Status M and zero new gravity Novelty Ledger rows are unchanged.

## 8. Small exact checks

`check.py` is a self-contained, standard-library arithmetic check of the
displayed finite witnesses, not a growth executor, simulation sweep or
create-only certificate. It imports neither the old candidates nor DET/RET
model code. Universal statements rest on the proofs above, not the number
of examples that pass. All **eight named witness tests pass in normal and
optimized Python 3.11.6**, each in about 0.004 seconds. Ruff passes. An
independent read-only mathematical review found no blocking discrepancy.
The check covers the readout pair, positive and impossible conditioning,
the two operator obstructions, real interference, the reversible-form
counterexample, reset ambiguity and bare-extension ambiguity.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/validation/t8-q-strict-derivation-2026-09-12/check.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O docs/validation/t8-q-strict-derivation-2026-09-12/check.py
.venv/bin/python -m ruff check docs/validation/t8-q-strict-derivation-2026-09-12/check.py
```

Checked source SHA-256 (`check.py`):
`a506f424cebd9edb976bb2b001da833663098cc6264889cb8fc2343c3aac73ab`.
This is a source record, not an independently frozen theorem certificate.
Earlier candidate sources, checked-source records and captures are unchanged.
