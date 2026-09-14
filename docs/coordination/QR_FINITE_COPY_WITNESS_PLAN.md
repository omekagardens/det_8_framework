# RI-21 — one fixed seed and finite-copy principal-minor witnesses

14 September 2026 UTC. **CONDITIONAL_FINITE_COPY_WITNESS_THEOREM;
PREPARATION_AND_COMPOSITION_PREMISES_SUPPLIED; INDEPENDENTLY_REVIEWED.**
Coordinator conditional-proof acceptance is complete.
This is a bounded proof/design note, not an executor, new axiom, registered
suite or physical measurement proposal. Its predecessor
[RI-20](QR_COMPOSITION_PREMISE_PLAN.md) is accepted and published at
`0bd4d4677bf0c0664c52e05fe6fb87c586383a3a`, tree
`cd17aeec4d23b0f8df5ed8517fa867721f371f8b`, with accepted note SHA256
`389d1ff809a921f5af832ca197e6bca4e3810ef1d0c7943193c5b6b9c9d95971`.
Publication was verified by the coordinator. This owner performs no git/index
operation and reserves only this new note and the three QR summaries.

**Result.** For a fixed n-alternative Hermitian normalized candidate D,
one fixed three-alternative signed PSD seed B and at most n identical
independent candidate copies suffice for a finite Boolean-event catalogue
characterizing D>=0. The event for each nonempty principal subset I has
weight |I|! det(D_I). There are 2^n-1 catalogue entries, independent of the
values of D. This reduces the specified ancillary resource family; it does
not derive that resource's admission or a physical ability to perform the
tests. No minimality, dimension-independent copy bound or efficiency is claimed.

## 1. Attribution and relationship to known composition results

The determinant/antisymmetrizer identity is standard linear algebra, not a
DET novelty. [Dowker–Wilkes v2](https://arxiv.org/html/2011.06120v2),
Lemma 9 and equations (4.19)–(4.24), use its even/odd permutation form;
Lemma 10 treats reality for Hermitian matrices. Lemma 11 supplies phase
powers, and Lemma 12 combines a negative principal determinant with
interference to obtain a negative self-composite event. Its event unions
explicitly use disjoint permutation histories. Here we independently derive
a bounded corollary with one **specified** signed seed; we do not claim the
corollary is absent from prior literature or that a generic interference
resource has this same bound.

[Boës–Navascués v3](https://arxiv.org/html/1609.09723v3), Lemma 3, instead
uses a tailored quantum-functional probe against one non-SP candidate.
Lemma 2 shows that no fixed self-copy cutoff certifies unrestricted
composability. The present test supplies an extra signed resource and a bound
depending on the candidate carrier size; it is not a self-copy-only cutoff.
Neither paper establishes these resource premises from DET.

The proof below uses direct permutation reindexing and an elementary
principal-minor argument. No paper's executor, quantum instrument, phase
amplification construction or physical interpretation is imported as a DET law.

## 2. Starting data, seed and exact resource contract

Let Omega={1,...,n}, n>=1, with its full Boolean event algebra. D is an
n×n **complex Hermitian** matrix, biadditively extended to event pairs by
D(A,C)=chi_A† D chi_C. Initially assume

\[
M(D):=\mathbf1^\dagger D\mathbf1=1,
\qquad \mu_D(A):=\chi_A^\dagger D\chi_A\ge0\quad(A\subseteq\Omega).
\tag{1}
\]

Strong positivity on this finite full algebra is equivalent to D>=0.
The scalar field and Hermitian event calculus are supplied inputs; this note
does not select them. M is total-entry normalization mass, **not** trace or
physical rest mass. The algebraic identity below does not require initial
weak positivity, but (1) is the assigned pre-PSD candidate domain.

The only ancillary kernel is on S={0,1,2}:

\[
b=(1,-1,1)^T,\qquad
B=bb^\dagger=
\begin{pmatrix}1&-1&1\\-1&1&-1\\1&-1&1\end{pmatrix}.
\tag{2}
\]

B is PSD, M(B)=|1-1+1|²=1 and Tr(B)=3. It is fixed independently of n,
D and I. Its first two coordinates supply signs; the third remains in the
carrier and supplies the normalization even though it is not selected in the
witness events. The two-marker subblock alone has total-entry mass zero and
cannot be normalized by scaling. Excluding a coordinate from an event does
not prepare a truncated seed, condition a state or implement postselection.

We specify identical independent copies and the tensor law

\[
C_n(D)=D^{\otimes n}\otimes B
\quad\hbox{on }\Omega^n\times S.
\tag{3}
\]

It is Hermitian and total-entry-normalized; it is not assumed weakly positive
before the test. At this stage it is only a candidate composite functional.
The copy factors have ordered, separately retained origins. Identical D
means equal functionals in the declared local frame, not merged histories.
Independent preparation is an additional premise, not a consequence of equal
matrices or distinct origin labels. There is no operation cloning an unknown
snapshot or reusing a terminal record as a residual.

For the necessity argument, it suffices to require nonnegative weights for
the finite catalogue defined below. Requiring weak positivity on the full
Boolean algebra of (3) is a stronger sufficient premise. Neither requirement
asserts that all these events are available sharp measurements.

## 3. Explicit Boolean event and determinant identity

For each nonempty I={i_1<...<i_m}⊆Omega, use the fixed increasing order and
write D_I=(D_{i_j i_k})_{j,k=1}^m. For sigma∈S_m set

\[
h_\sigma=(i_{\sigma(1)},\ldots,i_{\sigma(m)}),\qquad
a_\sigma=\begin{cases}0&\sigma\text{ even},\\1&\sigma\text{ odd}.
\end{cases}
\]

Define the **ordinary Boolean event**

\[
E_I=\{(h_\sigma,a_\sigma):\sigma\in S_m\}
\subseteq\Omega^m\times S.
\tag{4}
\]

All h_sigma are distinct because the elements of I are distinct. Therefore
the m! event atoms are distinct even though many use the same ancillary
marker. No signed multiplicities, repeated atoms or m!-dimensional ancilla
are hidden in (4). In particular b_{a_sigma}=sgn(sigma).

**Determinant identity.** For every complex matrix D and every I,

\[
\mu_{D^{\otimes m}\otimes B}(E_I)=m!\det(D_I).
\tag{5}
\]

**Proof.** Expand the Boolean quadratic form using the tensor entries and
the real parity signs from B:

\[
\begin{aligned}
\mu(E_I)
&=\sum_{\sigma,\tau\in S_m}
 b_{a_\sigma}\overline{b_{a_\tau}}
 \prod_{k=1}^m D_{i_{\sigma(k)},i_{\tau(k)}}\\
&=\sum_{\sigma,\tau\in S_m}
 \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)
 \prod_{k=1}^m D_{i_{\sigma(k)},i_{\tau(k)}}.
\end{aligned}
\]

For fixed sigma put pi=tau∘sigma^(-1) and j=sigma(k). The product becomes
product_j D_{i_j,i_{pi(j)}}, while sgn(sigma)sgn(tau)=sgn(pi).
As tau varies, pi runs over all permutations. The inner sum is precisely
the Leibniz determinant of D_I for each of the m! choices of sigma, proving
(5). There is no extra conjugation of D, modulus square of the determinant
or replacement by its real part. For Hermitian D the determinant is real. ∎

Equivalently, the formal real-coefficient antisymmetric coordinate vector
w_I=sum_sigma sgn(sigma)e_{h_sigma} satisfies
w_I† D^tensor(m) w_I=m!det(D_I). This is bookkeeping for the standard
identity, not a supplied antisymmetrizing instrument, fermionic preparation
or physical Hilbert-space postulate. The Boolean event uses the already
specified coherent seed to supply the signs.

### Padding to one common composite carrier

Keep the seed as the final factor and define

\[
\widetilde E_I=
\{(h_\sigma,z,a_\sigma):\sigma\in S_m,
       z\in\Omega^{n-m}\}\subseteq\Omega^n\times S.
\tag{6}
\]

The unused candidate factors contribute their whole-carrier events, not
selected histories. Directly summing their paired indices gives

\[
\mu_{C_n(D)}(\widetilde E_I)
=m!\det(D_I)\,M(D)^{n-m}
=m!\det(D_I).
\tag{7}
\]

The final equality uses (1). For m=n the empty tensor product has weight one;
there is no padding. For m=1 only the identity permutation is present and
the event weight is D_ii. No two-parity argument is needed in that case.

The catalogue has 2^n-1 entries, indexed by **all** nonempty principal
subsets; both seed and event definitions are independent of D's entries.
An unpadded witness of order m uses m candidate copies and one seed.
The common padded construction uses n candidate copies and one seed, with
m! n^(n-m) event atoms on a carrier of size 3 n^n. These are mathematical
resource counts, not sample counts, runtime guarantees or a minimality claim.
The events can overlap and do not form one recorded probability partition.

## 4. Complete principal-minor criterion and finite catalogue equivalence

**Principal-minor lemma.** A finite Hermitian D is PSD if and only if
det(D_I)>=0 for every nonempty principal subset I.

**Proof.** If D>=0, every principal compression is PSD and its determinant
is the product of nonnegative eigenvalues. Conversely assume all principal
determinants are nonnegative. Expanding det(tI_n+D) by its diagonal t choices
and remaining D entries gives

\[
\det(tI_n+D)
=\sum_{I\subseteq\Omega}t^{n-|I|}\det(D_I),
\qquad \det(D_\varnothing)=1.
\tag{8}
\]

To see the expansion, in each Leibniz term choose the indices contributing
t rather than D. They must be fixed permutation indices; on the remaining
principal subset the signed sum is its determinant. Equation (8) is strictly
positive for every t>0 because all its coefficients are nonnegative and its
leading term is t^n. A negative eigenvalue lambda of Hermitian D would give
det((-lambda)I_n+D)=0 at t=-lambda>0, a contradiction. All eigenvalues are
therefore nonnegative. This proves the lemma, including singular D. ∎

**Finite-copy theorem.** For D in the domain (1), with the specified seed,
copies and tensor law,

\[
\boxed{
D\succeq0
\ \Longleftrightarrow\
\mu_{C_n(D)}(\widetilde E_I)\ge0
\quad\text{for every nonempty }I\subseteq\Omega.
}
\tag{9}
\]

In particular, a non-PSD D has a negative principal determinant of some
order m<=n and hence the concrete negative event (4) or (6).
Weak positivity rules out a negative singleton minor, so such a witness in
the assigned domain has m>=2. The catalogue nevertheless includes singletons.

**Proof.** Equation (7) identifies the catalogue inequalities with all the
principal-minor inequalities; the lemma gives necessity. For the converse,
PSD D and B imply that D^tensor(n) tensor B is PSD: factor D=VV† and use
(V^tensor(n) tensor b)(V^tensor(n) tensor b)†. Consequently **every** Boolean
composite event has nonnegative weight, not only the catalogue. ∎

For n=1, normalization fixes D=[1] and the sole catalogue event has weight
one. Zero minors and zero event weights are allowed; replacing >=0 by >0
would wrongly reject singular PSD kernels. The empty principal minor is the
constant one in the lemma and requires no catalogue test. Testing only the
full determinant, only leading minors, or only minors of order at most two
does not implement (9).

## 5. Exact examples and supplementary arithmetic

All kernels in the table are Hermitian, total-entry-normalized and weakly
positive on their full local Boolean algebras. Identity (7) gives the same
value for direct and padded witnesses.

| Candidate | Principal minors | Catalogue conclusion |
|---|---|---|
| Original F3 D3=(J3-I3)/6 | Singletons 0; each order-two determinant -1/36; full determinant +1/108 | Each pair event is -1/18, despite the order-three catalogue event being +1/18. All candidate-only self-powers remain entrywise nonnegative. |
| Diagonal PSD diag(1/2,1/3,1/6) | All nonempty principal determinants positive | Every catalogue event is positive; order-three catalogue event 1/6. |
| H=[[1,1,1],[1,1,-1],[1,-1,1]]/5 | Singletons 1/5; all order-two minors 0; full determinant -4/125 | Only the third-order catalogue entry is negative: -24/125. Order-two checks alone miss it. |
| Complex Di=[[1/2,i],[-i,1/2]] | Singletons 1/2; determinant -3/4 | The two-copy-plus-seed event is -3/2, despite one-copy blindness to all real PSD probes. |
| Singular PSD J3/9 | Singletons 1/9; every higher-order principal determinant 0 | Higher-order event weights are exactly zero and must pass. |
| D_lead=0 direct-sum D3, n=4 | All leading principal minors vanish; lower-block pair determinants are -1/36 | Nonleading pair events are -1/18. Leading-minor-only testing fails even within the weak-positive domain. |
| n=1, D=[1] | Sole minor 1 | Sole event weight 1. |

For H, local event weights are 0 for the empty set, 1/5 for each singleton,
4/5,4/5,0 for the pairs {1,2},{1,3},{2,3}, and 1 for Omega. Thus its
third-order negative determinant is not a failure of local event positivity.
For D_lead, every event weight equals that of its intersection with the
D3 block; the zero first row/column makes every leading determinant zero.

For complex Di, the witness (4) consists of ((1,2),0) and ((2,1),1).
Its diagonal contribution is 1/2 and the seed-signed off-diagonal contribution
is -2, totaling -3/2. This event is **not** the unseeded self-square diagonal
event in RI-20, even though their weights coincide. Candidate copies now
carry the complex factors which a fixed real probe against one copy missed.

A temporary standard-library Gaussian-Fraction calculation formed these
literal Boolean events and summed their tensor entries. Independently computed
determinants used elimination, not the same double-permutation formula as the
event sum. Across the seven table cases it checked **54 local base events
and 94 direct/padded identities** for 47 principal subsets; all passed.
Seed normalization/trace, distinct event atoms, the third-order determinant,
complex value and vanishing leading minors were also checked. The calculation
ran from temporary input without writing a source file or importing DET's
existing executors. It is supplementary arithmetic, not a new suite, registry
witness, pinned execution or proof of the all-n theorem.

## 6. Why this does not contradict RI-20

[RI-20, section 4](QR_COMPOSITION_PREMISE_PLAN.md#4-exact-fixed-probe-adequacy-theorem)
concerns tests linear in an unrestricted original D using fixed independently
specified PSD ancillary matrices. Here C_n(D) depends on D in every candidate
factor. Before normalization (7) is homogeneous of degree n in D; on M(D)=1
it equals a degree-|I| principal determinant. For |I|>=2 these are nonlinear
tests of D. If the full composite is treated as the unknown matrix, it is
restricted to the tensor-power image (3), not an unrestricted Hermitian cone.
Neither reading satisfies the hypotheses of RI-20's polyhedral obstruction.

Similarly, the other candidate copies are not fixed real PSD ancillary
probes: they depend on D, can be non-PSD before selection, and retain its
complex entries. A real signed seed detecting Di through multiple copies
therefore does not defeat the one-copy real-probe blindness result.

D3 remains a countermodel to all-self-power positivity **without** the seed.
The resource (2) has negative entries, so adding it changes that hypothesis.
The construction strengthens the concrete resource account relative to a
tailored all-vector probe family: one fixed seed works, with a copy bound
depending on n. It does not strengthen the starting assumptions for free.
One exact signed seed is more specified admission data than an arbitrary
member outside R+; no conversion of every such resource into (2) is proved.

## 7. Premises-to-result ledger and the remaining DET gap

| Premise or result | Status in this note | Repository/source boundary |
|---|---|---|
| Finite Hermitian complex biadditive D, total-entry mass one, weak event positivity | Supplied pre-PSD candidate calculus | [RI-20 sections 1 and 7](QR_COMPOSITION_PREMISE_PLAN.md#7-det-wide-premise-ledger-assumed-proved-still-missing); complex completion is not derived from scalar weights |
| B from (2) admitted as one resource | Supplied; its PSD and normalization are proved algebraically | [RI-20 section 2](QR_COMPOSITION_PREMISE_PLAN.md#2-exact-primary-literature-route-and-its-hypotheses) permits a particular PSD seed without assuming class-wide PSD; preparation access remains missing |
| Up to n identically described but independently prepared candidates and one independent seed | Supplied admission/independence premise | [RI-08d premises](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md), section 1: distinct origins do not prove independence; a snapshot is not a copying operation |
| Composite factorization (3) and its Boolean event algebra | Supplied product law | [Pair-kernel composition](../../det8/models/pair_kernel.py), lines 309–319, computes a tensor matrix; existing PSD closure proves sufficiency, not availability for the pre-PSD class |
| Nonnegative weights for every catalogue event | Additional admissibility requirement; implied by full composite weak positivity | Mathematical event positivity, not an available sharp instrument, common recorded partition or observed frequency law |
| Identities (5), (7), principal-minor lemma and equivalence (9) | Proved conditional finite mathematics | No imported metric, fitted inverse or test-suite count substitutes for this proof |
| DET-native adoption/derivation of the preceding admission and product premises | **Not established** | Existing pair-kernel and finite reference/coupler routes assume PSD and supplied interfaces, as audited in RI-20 |

The improvement is a finite, precisely specified target for that missing
admission argument: for each n-candidate, establish the preparation/product
premises and catalogue positivity of this one resource construction. This
does not need an all-vector family of preparations or unbounded closure to
deduce PSD at that fixed n. A theory covering unbounded carrier sizes would
still need the corresponding premises for every size. No dimension-independent
copy bound follows, and no minimal resource theorem is asserted.

The seed's PSD verification does not make the reasoning circular: one
particular resource may be admitted independently. What is not yet supplied
by DET is that admission, independent replication and the composite positivity
law. Without them, the result remains conditional. No new global axiom is
adopted here.

The (R,Z) distinction is preserved. Residual activity can precede commitment,
but that does not make all residual event weights accessible records. Exact
recordability can fail for PSD states at an existing supplied interface;
event positivity is a different property. Neither parity markers nor event
membership supply an antisymmetrizing operation or a new instrument.

## 8. Boundaries, review and source-quiet handoff

No efficiency, sharp physical measurement, finite-sample confidence, uniform
noise margin, preparation tomography or resource-reuse protocol is proved.
Exact zero minors are legitimate; strict negative weights near the boundary
need not be bounded away from zero. A catalogue of algebraic tests is not an
experiment with that many shots, and may involve overlapping nonrecordable
events. Further apparatus and calibration premises would need separate work.

The complex scalar field, full-QM state/instrument richness, purification,
local tomography and native F/L remain separate. There is no physical time,
rest mass, Lorentzian geometry or gravity conclusion. The primitive-input
test, Option B and metric-as-record Status M remain unchanged. No supplied
mesh, Minkowski coordinates, Johnston kernel or borrowed growth law has
been recovered or promoted by this determinant calculation.

Three independent complete reviews passed: the mathematics and all examples;
primary-source attribution and resource bounds; and repository premises and
RI-20 compatibility. The reviewed table now explicitly names the order-three
catalogue event, avoiding confusion with the whole-carrier event of weight one.
No substantive blocker remains.

All 68 accepted predecessor/design/synthesis identities matched on entry and
at the final check. All 134 local link targets in the four scoped documents
resolve; whitespace/conflict-marker checks have zero findings. The exact four
document identities accompany the [source-quiet handoff](QR_HANDOFF.md).
Only this note and the three QR summaries changed; no predecessor executable,
registry, dependency, RET/core/application/bank file or protected review is
changed. No suite is replayed. Coordinator conditional-proof acceptance is complete; the
coordinator retains every git/index operation and publication authority.

This assignment stops at reviewed source-quiet handoff. It does not start an
executor, another operation family, QR-05BW–DO/coverage/noncollapse sequel,
clocks, book, retired kappa-gravity or an automatic successor. The missing
admission premise is not silently discharged by the copy bound.
