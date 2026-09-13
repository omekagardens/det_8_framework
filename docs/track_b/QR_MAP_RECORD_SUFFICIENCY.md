# QR-MAP: record sufficiency and the conditional first-commit law

13 September 2026. **THEOREM_AND_COUNTEREXAMPLE; CONDITIONAL_PROCESS_LAW.**

This starts the QR-MAP plan after implementation of the
[activity/commit/access contract](RECORD_PROCESS_CONTRACT.md). It establishes
when a committed record is predictively sufficient and how a supplied silent
process can be eliminated from a first-commit description. It does not derive
the physical availability of that process, select quantum theory, or supply a
DET-native growth law. No new executor or lettered QR-05 gate is introduced.

## 1. State, scope and complete future experiments

Write \(x=(C,\mathcal Z)\in X_{\rm reach}\), with committed snapshot

\[
C=(V,\prec,R_{\rm comm}).
\]

Reachability is relative to declared preparations and available processes.
The first QR-MAP candidate for \(\mathcal Z\) is its existing residual kernel
\(\mathfrak D_C\), together with its operational interface. An accessible
record projection is a different object; the theorem below concerns the
specified committed input, not an implicitly complete observer's log.

Fix law parameters, model scope and a common residual-system interface.
For every compared snapshot \(C\), declare a family \(\mathscr T_C\) of
continuation experiments applicable to **every** compared state above \(C\).
Each experiment fixes the same intervention policy, observation mechanism and
accounted-for control context. Where complete process comparisons are claimed,
include all allowed ancillary references and their continuation tests.

An apparatus or controller distinction that changes predictions must be in
the state or declared input context; it cannot be omitted to manufacture
"identical inputs." Different available test domains likewise cannot be
identified without an explicit common-interface restriction.

For \(t\in\mathscr T_C\), let \(P_t(\cdot\mid x)\) be its probability measure
on a specified complete outcome space \(Y_t\). A test that can wait forever
without another commit must account for that possibility. Conditioning on a
later detection instead defines a different experiment and requires its own
positive-probability condition. Receipt delay and absence of formation must
not share an undifferentiated outcome label.

## 2. Record-fiber sufficiency theorem

**Theorem.** At the level of probability distributions, record-only predictors
\(\widehat P_t(\cdot\mid C)\) satisfying

\[
P_t(\cdot\mid x)=\widehat P_t(\cdot\mid C(x))
\tag{1}
\]

exist for all declared continuations if and only if

\[
C(x)=C(y)\quad\Longrightarrow\quad
P_t(\cdot\mid x)=P_t(\cdot\mid y)
\quad\text{for every }t\in\mathscr T_C,
\qquad x,y\in X_{\rm reach}.
\tag{2}
\]

**Proof.** If (1) holds, both sides of a comparison in (2) evaluate the same
predictor at the same input. Conversely, for every reachable \(C\), define
\(\widehat P_t\) from any state above \(C\). Condition (2) makes this definition
independent of the representative and supplies (1). No prediction is assigned
to an unreachable snapshot by this argument. \(\square\)

For a measurable stochastic kernel on the record space, not just this
set-level factorization, measurability must also be established. It is
automatic for finite/countable record spaces with the discrete sigma-algebra.
General spaces require suitable measurable-quotient assumptions; this theorem
does not infer them from operational equivalence.

Within each \(C\)-fiber, define future-test equivalence by equality of all
distributions for \(\mathscr T_C\). Record-only sufficiency holds exactly when
each reachable fiber has only one class: equivalently, the disjoint-union
quotient \(x\mapsto(C,[x]_{\mathscr T_C})\) factors through \(C\). Different test domains
are not implicitly identified across snapshots. Literal recovery of every entry of
\(\mathfrak D_C\) is **sufficient, not necessary**: descriptions can differ by
gauge or by distinctions unavailable to the declared tests.

The theorem does not identify operational equivalence with ontological
identity. It also does not construct a unique autonomous Markov law. Equality
of one next-record marginal is weaker than equality of all continuation laws;
an untested residual difference may affect a later record. Neither software
immutability nor a fixed transition rule proves (2).

## 3. Exact classical counterexample at fixed committed history

Take a two-alternative carrier and the admitted diagonal kernels

\[
d_0=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
d_1=\begin{pmatrix}0&0\\0&1\end{pmatrix},\qquad
P=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\tag{3}
\]

They are positive semidefinite and have total-entry mass one. The permutation
map \(S(d)=PdP^T\) preserves both properties, since \(P^T\mathbf1=\mathbf1\).

**Explicit availability assumption:** admit \(S\) as a silent residual
operation in this candidate extension, leaving the specified \(C\) unchanged.
From \((C,d_0)\) it reaches \((C,d_1)\). Both compared states have the same
residual type and are allowed preparations/continuation states at one fixed
readout interface and current protocol. This abstract candidate has no separate
retained controller variable revealing which state was prepared; any such
variable in an implementation must be included, not silently omitted. The
common future singleton-partition readout is exactly decoherent on both and gives

\[
P(r=0\mid C,d_0)=1,\qquad P(r=0\mid C,d_1)=0.
\tag{4}
\]

Consequently (2) fails. This is a rejected record-only summary in a declared
silent-operation extension. The extra operation is not derived from the
original kernel axioms. Its composition depth is not a physical clock, and
the comparison does not erase a controller record outside the chosen scope.
The implemented contract can represent this example; it does not prove its
physical realization. No Hilbert space, amplitude or geometry is needed for
this witness, and its classical character prevents a uniquely quantum claim.

## 4. Conditional finite-QM comparison

Inside the separately assumed
[finite operational completion](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md),
let

\[
\rho_\pm=\tfrac12\begin{pmatrix}1&\pm1\\\pm1&1\end{pmatrix},\qquad
U=\operatorname{diag}(1,-1),\qquad E_+=\rho_+.
\tag{5}
\]

Then \(U\rho_+U^*=\rho_-\). The two computational-basis distributions agree,
whereas \(\operatorname{Tr}(E_+\rho_+)=1\) and
\(\operatorname{Tr}(E_+\rho_-)=0\). Admitting this operation silently at fixed
\(C\) therefore violates record sufficiency for a family containing that
later readout. It changes a relative phase, not an unobservable global phase.

On the reconstruction's specified compatible kernel cone, use its injective
encoding \(J_2\) and the transported map

\[
\mathfrak D\longmapsto
J_2\!\left(UJ_2^{-1}(\mathfrak D)U^*\right).
\tag{6}
\]

This is not arbitrary unitary conjugation of an unrestricted kernel matrix:
the original normalization is total-entry mass, not trace. The quantum system,
operations and encoding are explicitly conditional inputs. This comparison
does not prove a native silent scheduler or autonomously extend \(L_{XYZ}\).

## 5. First-commit elimination for a supplied finite instrument

Fix \(C\) and an accounted-for control context. Consider a **chosen** repeated
interaction protocol on the full finite complex matrix spaces
\(A=\mathcal B(H_A)\), \(A_r=\mathcal B(H_r)\), with
\(d_A=\dim H_A\). These quantum spaces are conditional inputs. Let
\(Q:A\to A\) be a CP no-append map, with finitely many CP commit branches
\(B_r:A\to A_r\). Their completeness condition is

\[
u_AQ+\sum_r u_{A_r}B_r=u_A,
\tag{7}
\]

where \(u_A=\operatorname{Tr}\) in this conditional quantum representation.
The label \(r\) contains the **full** append branch: allowed predecessor ideal
\(S\), outcome/payload, fresh-event bookkeeping and output residual type.
Each branch must satisfy the implemented immutable maximal-append contract.
Scalar outcome probabilities alone do not specify the order-producing law.

The silent branch leaves \(C\) unchanged; its mathematical tag is not a
logged null outcome. Repetition of one \(Q\) assumes the same declared
protocol between commits. A changing policy may require controller state in
\(A\), or an explicitly specified sequence of different maps. Neither is
supplied by the notation. The integer below counts composition steps, not
derived duration or a preferred global tick.

For normalized \(\rho\), the probability of first commitment to branch \(r\)
after exactly \(n\) silent transitions is

\[
p(n,r)=u_{A_r}B_rQ^n(\rho),\qquad n\geq0.
\tag{8}
\]

Let \(s_N=u_AQ^N(\rho)\). Equation (7) telescopes to

\[
\sum_{n=0}^{N-1}\sum_r p(n,r)=1-s_N,\qquad
p_{\rm never}=\lim_{N\to\infty}s_N,\qquad
\sum_{n\geq0,r}p(n,r)=1-p_{\rm never}.
\tag{9}
\]

The limit exists because \(s_N\) decreases in \([0,1]\). It is the mass of
infinite silent continuation in this discrete protocol, not a derived claim
about an infinite physical duration. No eventual-commit assumption is used.

**Finite-dimensional convergence proof.** Define
\(H_{r,N}=\sum_{n=0}^{N-1}B_rQ^n\). These maps are CP, and their unnormalized
Choi matrices increase in positive-semidefinite order. Applying (9)'s
unnormalized telescoping identity to \(I_A\) bounds
\(\operatorname{Tr}\operatorname{Choi}(H_{r,N})
=\operatorname{Tr}H_{r,N}(I_A)\leq d_A\).
The positive increments have trace norm equal to their trace; bounded monotone
traces therefore make the Choi sequence Cauchy. Its finite-dimensional limit
is positive and defines the CP map

\[
\widehat B_r=\sum_{n\geq0}B_rQ^n.
\tag{10}
\]

Trace-nonincreasing inequalities pass to the limit. Moreover
\(E_N=(Q^*)^N(I_A)\) decreases to an effect \(E_\infty\), giving

\[
p_{\rm never}=\operatorname{Tr}(E_\infty\rho),\qquad
\sum_r\widehat B_r^*(I_{A_r})=I_A-E_\infty.
\tag{11}
\]

Thus (10) need not be a normalized commit instrument. A cemetery outcome
with effect \(E_\infty\) completes its outcome probabilities. It is mathematical
bookkeeping, not a newly committed "never" record or a limiting residual state;
the sequence \(Q^n(\rho)\) need not converge. Conditioning
on commitment requires \(1-p_{\rm never}>0\); the resulting normalization
can depend on the input and is not generally an affine channel. Almost-sure
commitment on all preparations requires \(E_\infty=0\). A bound
\(Q^*(I_A)\leq(1-\epsilon)I_A\), \(\epsilon>0\), is sufficient, but must not
be assumed without justification. An inverse \((I-Q)^{-1}\) is not used.

For example, on a classical cone take \(Q(a,b)=(a/2,b)\) and \(B(a,b)=a/2\).
On \((a,1-a)\), \(p(n)=a/2^{n+1}\) and \(p_{\rm never}=1-a\). Preparations
\(a=1/3\) and \(a=2/3\) have identical conditional detected labels but different
never-commit probabilities. Discarding that outcome loses a genuine distinction.

## 6. Result and remaining obligations

The completed results are a factorization theorem, an exact rejected
record-only summary, and a conditional first-commit lemma. They supply no
native choice of \(Q\), \(B_r\), measurement algebra or order-growth rule.

The concrete remaining obligations are: justify a lawful silent/commit family
and its physically available operations; account for controller state and
sequencing without a universal tick; prove eventual commitment or retain its
cemetery mass; generate precursor ideals and complete branches within the law;
and specify a separate formation/access mechanism before geometry inference.
Selecting an already-assumed branch in software is not first-outcome formation.

**Verification:** the written arguments received an independent mathematical
review. Exact fraction arithmetic also checked the last example's finite-prefix
mass balance at \(N=0,1,2,8,32\) for both preparations. Those checks illustrate
the general proof; this is not a Lean-verified theorem or a physical validation.

The classical and real-quantum countermodels to reconstruction remain live.
The [selection principles](../validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md)
are not adopted by these results. Authorized mass/geometry/gravity research
remains open, but no metric, manifold, matter coupling or gravitational claim
is promoted here. RET, clocks, book work and retired \(\kappa\)-gravity are
untouched; no lettered gate or new executor follows from this note.
