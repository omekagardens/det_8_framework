# RI-08g — minimal literal-cut-closed completion

13 September 2026. **MINIMAL_CONVEX_CUT_CLOSED_EXTENSION;
POLARIZATION_DEPENDENT_MASS_AND_EFFECT_BOUNDARY;
CUT_CATALOGUE_WEIGHT_EQUIVALENCE.** Conditional mathematics for an
explicitly enlarged return cone. Convex closure and algebraic operations
do not establish physical preparation or operation availability.

## 1. Fixed native interface, explicitly different return type

Retain the fixed reference, Z orientation, independent initial composition,
coupler \(U=(I\otimes H)\mathrm{CNOT}\), and signed native permutation T
of [RI-08f](../t8-q-joint-repeatability-2026-09-13/JOINT_REPEATABILITY.md).
For a Hermitian 2-by-2 matrix \(\rho\), set
\[
B_t=(I+tZ)/4,\quad
M_t(\rho)=U\bigl((\rho^T/2)\otimes B_t\bigr)U^\dagger,\quad
-1\le t\le1 .
\]
The fixed t is a known interface parameter, not a changing hidden setting.
All sixteen native labels \((a,i,b,j)\), with index \(8a+4i+2b+j\),
remain. Grouped order is \((a,b,i,j)\), index \(8a+4b+2i+j\), and
\[
T_{8a+4b+2i+j,\;8a+4i+2b+j}=(-1)^{ai+bj}.
\]

For \(\alpha=(a,b)\) in the four-cell set \(\mathcal A\), define
\[
\mathcal I_t((\rho_\alpha)_\alpha)
=T^\dagger\operatorname{diag}
   (M_t(\rho_{00}),M_t(\rho_{01}),M_t(\rho_{10}),M_t(\rho_{11}))T ,
\]
\[
\boxed{L_t=\{\mathcal I_t((\rho_\alpha)):\rho_\alpha\succeq0
\text{ independently for all }\alpha\}.}
\]
Unlike the old \(K_t\), the four blocks need not be equal. The old image
embeds by \(\rho_\alpha=\rho\) for every cell. This is a changed declared
domain and range, not reuse of the old K_t return contract. At t=0 both
definitions choose c=0 image blocks; no unpolarized-reference exclusion
of the earlier local c parameter is inferred.

The native literal cut is
\(\mathsf C_\alpha(N)=P_\alpha NP_\alpha\), where \(P_\alpha\) retains
the four native labels in cell \(\alpha\). It keeps all entries in that
cell, not merely a scalar probability.

## 2. Minimality and positive inverse on the full span

**Minimality theorem.** L_t is the smallest convex cone containing K_t
and closed under every \(\mathsf C_\alpha\).

**Proof.** L_t is a convex cone, contains K_t by equal-block embedding,
and each cut zeros three blocks without changing the fourth. Conversely,
any convex cone H containing K_t and closed under the four cuts contains
\(\mathsf C_\alpha\mathcal J_t(\rho_\alpha)\) for every positive
\(\rho_\alpha\), where \(\mathcal J_t\) is the accepted equal-block map.
It therefore contains their sum
\[
\sum_\alpha\mathsf C_\alpha\mathcal J_t(\rho_\alpha)
=\mathcal I_t((\rho_\alpha)).
\]
Thus \(L_t\subseteq H\). No infinite or topological completion was used. ∎

This is minimality among **mathematical convex cones** with those closure
properties. It neither supplies all independent preparations nor assumes
that distinct known preparation histories may be averaged and forgotten.
Starting at one physically available K_t source and performing only cuts
does not by itself generate every independent four-block preparation.

Undo T and inspect all four diagonal blocks \(M_\alpha\). Each inverse is
\[
\rho_\alpha=
4\left[\operatorname{Tr}_{\mathrm{ref}}
 (U^\dagger M_\alpha U)\right]^T .
\]
The factor follows from \(\operatorname{Tr}B_t=1/2\). It does not divide
by \(1+t\) or \(1-t\), and works at t=0 and both rank-one reference
endpoints. Membership requires that these reconstructed matrices reproduce
**every native entry**, including off-block zeros. A partial trace alone
must not silently project an outsider into L_t.

This makes \(\mathcal I_t\) a real-linear isomorphism of the actual
sixteen-dimensional span with \(\bigoplus_{\alpha}\operatorname{Herm}_2\).
It and its inverse are positive on their respective cones: positivity
of a native block implies positivity of the displayed partial trace;
positive \(\rho_\alpha\) give positive tensor/congruence blocks.
Consequently L_t is isomorphic to a direct sum of four PSD2 cones.
It is closed, pointed and generating in its own span for every t,
including the endpoints. It is not the entire PSD cone on sixteen labels.

The blockwise after-the-fact convention remains
\[
4M_\alpha^T
=\bar U(\rho_\alpha\otimes\rho_t)U^T,\qquad
\rho_t=(I+tZ)/2 .
\]
Complex transposes are not dropped just because the specified U is real.

## 3. Cell weights, mass and raw trace are different functionals

The accepted full-cell effect pulls back separately in each block:
\[
q_\alpha(N)=\operatorname{Tr}(E_\alpha\rho_\alpha),\qquad
E_{ab}=(I+(-1)^btZ)/4 .
\]
Every complex off-cell form vanishes. Total-entry mass is therefore
\[
\boxed{m(N)=\sum_\alpha q_\alpha(N)
=\sum_\alpha\operatorname{Tr}(E_\alpha\rho_\alpha).}
\]
The ordinary sixteen-label trace is instead
\[
\boxed{\tau(N)=\operatorname{Tr}N
=\tfrac14\sum_\alpha\operatorname{Tr}\rho_\alpha.}
\]
These agree at t=0 and on the equal-block K_t subset, but generally
**not on L_t**. Normalization and branch probabilities use m, not τ.
For positive N its Hermitian trace norm is τ(N). Here mass means
normalization mass, not physical rest mass.

The eigenvalues of every E_alpha are
\(\lambda_\pm=(1\pm|t|)/4\). Hence, for positive N,
\[
(1-|t|)\tau(N)\le m(N)\le(1+|t|)\tau(N).
\]
For each fixed \(|t|<1\), m is faithful. The normalized positive base is
closed and trace-norm bounded by \(1/(1-|t|)\), hence compact in the
finite-dimensional actual span.

## 4. Literal cuts are complete and repeatable on the new type

Every \(\mathsf C_\alpha\) is real-linear on the full span and positive
L_t→L_t. The exact identities are
\[
m(\mathsf C_\alpha N)=q_\alpha(N),\qquad
\sum_\alpha\mathsf C_\alpha N=N,\qquad
\mathsf C_\beta\mathsf C_\alpha
=\delta_{\alpha\beta}\mathsf C_\alpha .
\]
Thus both raw completeness and mass completeness hold. For a positive
weight \(p=q_\alpha(N)>0\), the selected state
\[
N_\alpha=\mathsf C_\alpha N/p
\]
is normalized in L_t and has \(q_\alpha(N_\alpha)=1\), with every other
cell weight zero. It perfectly repeats the **full** outcome.
Earlier and new records still retain both a and b.

There is no contradiction with RI-08f: its obstruction required return
to K_t, with four equal blocks. A nonzero literal cut leaves K_t but
belongs to L_t, where the same full-cell effect has normalized maximum
one. No physical reference reset or repeated coupler was derived.
Reusable literal cuts are supplied operations on this newly declared
domain, not an automatic retagging of accepted objects or a new SDK.

At an endpoint a zero weight need not mean a zero raw cut. It is never
normalized or appended as a possible record. The raw completeness identity
still includes every such cut. In particular,
\[
\sum_{q_\alpha(N)>0}q_\alpha(N)N_\alpha
=N-\sum_{q_\alpha(N)=0}\mathsf C_\alpha N
\]
can differ from N by nonzero positive raw payload. The scalar probabilities
still sum to m(N); that fact does not authorize discarding the remainder
while claiming exact raw reconstruction.

## 5. Polarized endpoints and three different kernels

At \(|t|=1\), write
\[
E_\alpha=\tfrac12 Q_\alpha^{\mathrm{bright}},\qquad
Q_\alpha^{\mathrm{dark}}=I-Q_\alpha^{\mathrm{bright}},
\]
where the bright Z sign is \((-1)^b\operatorname{sign}(t)\).
Because all cell weights are nonnegative, a positive N has zero mass
exactly when each \(\rho_\alpha=s_\alpha Q_\alpha^{\mathrm{dark}}\),
\(s_\alpha\ge0\). Positivity rules out a remaining off-diagonal row/column
when the bright diagonal is zero. Thus the positive zero-mass subcone is
isomorphic to \(\mathbb R_+^4\), and its real span has dimension four.
It is not the whole linear kernel of m.

Every real-linear effect on the actual span has a unique representation
\[
e(N)=\sum_\alpha\operatorname{Tr}(F_\alpha\rho_\alpha),
\qquad F_\alpha=F_\alpha^\dagger .
\]
The **whole-cone mass-domination** requirements \(0\le e\le m\) are
equivalent, by PSD2 self-duality in each independent block, to
\[
0\preceq F_\alpha\preceq E_\alpha .
\]
At an endpoint E_alpha has rank one. The two inequalities force F_alpha
to have the same support, so
\[
F_\alpha=c_\alpha E_\alpha,\quad0\le c_\alpha\le1,\qquad
\boxed{e(N)=\sum_\alpha c_\alpha q_\alpha(N).}
\]
This classifies all such mathematical effects, not an asserted available
physical observation catalogue.

The four q_alpha are independent. Therefore the relevant dimensions are:

| Object on the sixteen-dimensional real span | Dimension |
| --- | --- |
| Span of the positive zero-mass subcone, at an endpoint | 4 |
| Common kernel of every whole-cone effect \(0\le e\le m\), at an endpoint | 12 |
| Kernel of the single total-mass functional m | 15 |

The twelve-dimensional common kernel includes eight real coherence
directions as well as four dark diagonal directions. The further three
directions in ker(m) redistribute signed visible weights between cells.
These are different objects; a signed invisible direction is not itself
a positive zero-mass state.

Ordinary norm-bounded linear functionals are not the same as
mass-dominated effects. In finite dimension every linear functional is
norm bounded, including ones seeing dark payload. For example τ is
positive and norm bounded but cannot obey τ≤m on an endpoint positive
zero-mass state. The endpoint collapse does not concern all linear probes.

For \(|t|<1\), each E_alpha is positive definite. The interval
\([0,E_\alpha]\) spans all Hermitian 2-by-2 directions (a sufficiently
small perturbation of E_alpha/2 stays in it), so these mathematical
effects span all sixteen dual dimensions. Internal effects beyond cell
weights are then permitted by positivity/mass domination, with their
physical availability still separate.

For a concrete interior example on one cell, set
\(F=\lambda_-Q_{X+}=\lambda_-(I+X)/2\) and all other F blocks to zero.
Then \(0\le F\le\lambda_-I\le E_\alpha\).
The positive one-cell states with
\(\rho_\alpha=2(I+sX)\) and \(2(I-sX)\), \(0<s\le1\), both have mass
and that cell weight one, but e differs by \(4\lambda_-s\).
These are mathematical distinguishability witnesses, not new available
controls or preparations. At an endpoint this F is zero.

## 6. Singular limit and the absence of a uniform compact-base bound

For any fixed cell and \(0<|t|<1\), let \(Q_-(\alpha,t)\) be its
**lower-effect** Z eigenprojector. It is not universally the literal
Z-negative projector: the choice depends on b and the sign of t.
Set only
\[
\rho_\alpha=Q_-(\alpha,t)/\lambda_-,\qquad
\lambda_-=(1-|t|)/4 ,
\]
with every other block zero. Then
\[
m(N)=1,\qquad
\boxed{\tau(N)=\|N\|_1=\frac1{1-|t|}.}
\]
This saturates the interior base bound and diverges toward either
polarized endpoint. It is a family of finite mathematical normalized
states, not evidence of an experimentally realizable unbounded resource.

At an endpoint, add any multiple of a nonzero positive dark block to a
fixed normalized bright state. Mass stays one while τ grows without
bound. Thus the endpoint normalized base is not compact. Neither the
compact-base constant nor any argument depending on it is uniform in t.
No infinite-history or continuum-limit interchange is inferred.

## 7. Exact future equivalence for the stated cut-only catalogue

Now restrict available tests to the **fixed full-cell question**, its
literal cuts, and stopping, with finite serial or known-history adaptive
use. No internal effect from §5, additional control, changed reference,
new context or silent dynamics is silently included.
Compare normalized states at the same retained full prefix and known context.

Define the weight map
\[
q:L_t\to\mathbb R_+^4,\qquad q(N)=(q_\alpha(N))_\alpha .
\]
It is surjective: put
\(\rho_\alpha=x_\alpha Q_\alpha^*/p_{\mathrm f}\),
where \(p_{\mathrm f}=(1+|t|)/4\) and Q_alpha* is any maximizing
normalized local state. This gives an explicit positive linear section
and q=x; it does not make that section a physically available reset.
The quotient mass is \(\sum_\alpha x_\alpha\), which is faithful for
every t, including the endpoints.

If \(P_\alpha^{\mathrm{wt}}\) projects onto one weight coordinate, then
\[
q\,\mathsf C_\alpha=P_\alpha^{\mathrm{wt}}q .
\]
Every finite cut word therefore factors through q. A nonempty word has
the first cell's weight if every outcome is that same cell, and zero
if two successive requested outcomes differ. Immediate full-cell
probabilities distinguish unequal q. Thus
\[
\boxed{\text{equal cut-only finite future-record laws}
\iff\text{equal four cell weights}}
\]
on the declared same-prefix/context interface.
For general unnormalized positive inputs, the analogous statement concerns
equality of finite outcome-weight measures, including total mass, not laws
conditioned on normalizing the source. N and 2N need not have equal q even
though normalization would make their record laws agree.
History-dependent stopping and choices among those same operations
preserve this conclusion by finite-tree induction; policies must not
depend on an undeclared residual oracle. A stop before any cut adds no
cell knowledge. Actual records, their settings and precursors are not
identified by this residual equivalence.

At interior t, this equivalence is weaker than equivalence under all
mathematically mass-dominated effects, as §5 shows. At endpoints every
such effect factors through q, but ordinary norm-bounded probes need not.
In either case, q is a predictive summary for its declared questions,
not a replacement for the retained full raw residual or record history.

## 8. Precisely bounded use of RI-07

For each fixed interior \(|t|<1\), L_t supplies the closed, pointed,
generating finite-dimensional cone and faithful compact mass base used by
[RI-07](../t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md).
A cut-face may also be used in its own actual span. This does **not**
supply the remaining first-commit premises. One must still declare:

1. One fixed committed prefix and a stationary experiment or fixed finite
   internal controller/policy, not a sum of alternative commanded actions.
2. Positive linear mutually exclusive silent and committing branches
   satisfying complete mass, with finitely many **full** committing labels
   and retained output types.
3. Faithful masses on every committing-output cone, not only the input,
   and the other finite-dimensional closed-cone hypotheses there.
4. An observation contract that does not later use the eliminated silent
   path, wait count or controller visits. Actually retained words/counts
   must remain in labels; unbounded payloads can defeat finite-label scope.

Under those separate hypotheses RI-07 gives its raw first-commit operator
limits at that fixed model/prefix. It gives neither convergence of silent
residuals nor a uniform family rate or unbounded-history closure.
The present cut-only executor has no newly supplied silent law; an
immediate cut has a trivial first-commit calculation.

At \(|t|=1\), the raw L_t input and cut-output cones fail faithfulness.
The RI-07 raw compact-base theorem cannot simply be applied. The explicit
weight cone is instead \(\mathbb R_+^4\), independently proved closed and
faithful above; its properties are not borrowed from the faithful-source
quotient theorem whose source premise fails here. RI-07 can apply to that
quotient after **all** of its other hypotheses hold and every claimed
continuation and terminal effect descends. The cut catalogue has the
displayed descent; a changed type or added law requires its own check.

Finite partial-sum intertwining does not prove convergence of raw
committing operators. Do not write an equality involving a raw limiting
map unless that limit exists by a separate argument. The nonfaithful
counterexamples in RI-07 show why scalar convergence alone is insufficient.
This warning does not claim that the present idempotent cut maps diverge.
No record, raw dark payload or unbounded word is erased to force a theorem
to apply.

## 9. Executable, evidence and stop boundary

[model.py](model.py) uses exact Gaussian-rational arithmetic, all native
blocks and the explicit changed L_t domain tag. Independent block inversion
and reconstruction distinguish signed span membership from positive
source membership. Normalization and commitment use total-entry mass.
Known t/orientation, original local/reference provenance, frame/coupler,
actual cut setting, full fine outcomes and origin-tagged complete
precursors remain in immutable typed records. Source snapshots certify
grammar/domain, not global preparation reachability.

Only the fixed literal cuts are reusable typed operations. General
four-block construction and convex minimality do not infer physical
mixture availability or erase its possible selectors. Zero-weight cuts
remain inspectable full raw objects and cannot be normalized or committed.
The weights are a query summary, never an instruction to replace sources.

[check.py](check.py) independently checks native identities, span/rank
certificates, endpoint and interior witnesses, singular sequences and
finite record-bearing protocols. Finite tests supplement the universal
proofs; they do not prove them by sampling or supply empirical calibration.

This sitting yields the minimality, return-map and effect theorems plus
explicit boundary/counterexamples. It derives no physical availability,
new controls, arbitrary ancillary/composite theory, full QM, geometry,
rest mass or gravity. Option B and Status M stay unchanged.
Only this new bundle and reserved QR maps/handoff are changed. Accepted
sources and RET/application/registry/claims/operational-ledger files remain
untouched. No successor is designed or started; stop for independent
acceptance.

~~~sh
.venv/bin/python -B docs/validation/t8-q-cut-closed-completion-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-cut-closed-completion-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-cut-closed-completion-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-cut-closed-completion-2026-09-13
~~~

Final source pins and internal review/replay are in the
[handoff](../../coordination/QR_HANDOFF.md). No external peer review,
proof-assistant certificate or empirical validation is claimed.
