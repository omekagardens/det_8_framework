# First-commit elimination and lawful predictive quotients

13 September 2026. **FINITE_TYPED_COMPACT_BASE_THEOREM;
CONDITIONAL_QUOTIENT_DESCENT; PERIODIC_SILENT_COUNTEREXAMPLE.**

This is the bounded RI-07/P3/O2/O3 assignment from the
[independent review](../../../indep%20ndent_review.md), following the accepted
[controlled-context result](../t8-q-controlled-context-2026-09-13/CONTROLLED_CONTEXT.md).
The accepted bundle is unchanged. The new [model](model.py) and independent
[checks](check.py) implement exact rational examples, not a general process
SDK, an empirical experiment or a DET-derived physical law.

**Result.** Under the finite typed compact-base premises below, summing all
unobserved silent steps before a first commitment yields convergent
operator-valued committing maps, with complementary never-commit probability.
Silent residuals need not converge. A predictive quotient preserves this
construction when every allowed continuation and terminal observation descends.
Under the stated faithful-mass premises its positive cone is well behaved;
arbitrary cone projections do not inherit those properties.

## 1. Premise/result ledger

| Premise or choice | Status and consequence |
| --- | --- |
| A fixed committed prefix \(C\), finite controller and stationary finite map catalogue at that prefix | Scope of the theorem; an arbitrary history-dependent or time-dependent law is not automatically captured |
| Finite-dimensional closed, pointed, generating positive cones; strictly positive mass units, including on committing outputs | Sufficient compact-base assumptions, not necessary conditions or quantum selection |
| One declared complete experiment or fixed controller policy, with positive linear branch maps | Additional operational-law premise; do not sum incompatible actions as if they were outcomes |
| Every full committing label, precursor and output residual/controller type retained | Information-preserving output contract; no payload-only or outcome-discarding replacement |
| Silent paths/counts unobserved or deliberately excluded from the target questions; later tests linear on retained unnormalized residuals | Required observation contract for elimination, not a claim about physical access |
| Quotient invariant under every allowed continuation; every terminal effect, including mass, descends | Additional quotient obligation, not implied by one matching eventual-outcome distribution |
| Physical preparation, control, record formation and access availability | Still open; no DET-native \(F/L\), QM, geometry, mass or gravity derived |

The accepted QR-MAP quantum payload is not replaced by the classical examples
here. The theorem concerns positive record processes; a proposed quantum
image cone must separately supply its domain, mass and lawful operations.
Positivity does not imply complete positivity for unstated ancillary systems.
No reconstruction axiom, empirical threshold, Option B or Status-M boundary
is promoted.

## 2. Finite typed first-commit theorem

“Cone” throughout means a convex cone, closed under sums and nonnegative
scaling; additional topological closedness is stated explicitly.

At one fixed \(C\), let \(I\) be a finite set of internal controller types.
For each \(i\), let \(V_i\) be a nonzero finite-dimensional real vector space,
\(K_i\subset V_i\) a closed, pointed, generating cone, and \(u_i\) linear
with \(u_i(x)>0\) for every nonzero \(x\in K_i\). Take the direct sums

\[
V=\bigoplus_i V_i,\quad K=\bigoplus_i K_i,\quad
U(x)=\sum_i u_i(x_i).
\]

The direct sum retains the controller components; it does not assume they
are externally readable. If an apparatus type is externally known, that
known type remains part of the observation/control interface.

Let \(S:V\to V\) be the sum of the **mutually exclusive silent branches**
of one fixed declared experiment. Its typed blocks may change the internal
controller while leaving \(C\) untouched. Alternative commanded actions
cannot simply be added to form \(S\); their selection must already be
specified by a normalized fixed policy or an explicit finite controller.

For each of finitely many full committing labels \(r\), retain a positive
linear map \(B_r:V\to Y_r\), output cone \(J_r\) and mass \(v_r\), with the
same finite-dimensional closed, pointed, generating and strict-positivity
hypotheses. If one label has several retained output types, keep their
direct sum instead of averaging incompatible types. Assume complete mass:

\[
US+\sum_r v_r B_r=U. \tag{1}
\]

All maps act on **unnormalized** states. A normalized input has \(U(x)=1\).
Define

\[
H_{r,N}=\sum_{n=0}^{N-1}B_r S^n,\qquad s_N=US^N,\qquad H_{r,0}=0. \tag{2}
\]

**Theorem.** For every \(r\), \(H_{r,N}\) converges in operator norm to a
positive linear \(H_r\). The survival functionals \(s_N\) converge in dual
norm to a positive \(\ell\), and

\[
\sum_r v_rH_r+\ell=U,\qquad \ell S=\ell. \tag{3}
\]

For normalized positive \(x\), \(\ell(x)\) is the probability of no commitment
ever occurring under this fixed experiment. Neither \(S^N\to0\) nor
convergence of \(S^N\) is required.

### Proof

First, a finite-dimensional closed cone with a strictly positive mass \(v\)
has a compact normalized base. On its compact intersection with the unit
sphere, \(v\) has a positive minimum \(\delta\). Thus

\[
\|z\|\le \delta^{-1}v(z)\quad(z\ge0). \tag{4}
\]

The slice \(v(z)=1\) is closed and bounded. Apply this argument to every
input and output cone; in particular write \(c_r\) for an output bound.

For \(x\in K\), (1) telescopes:

\[
US^n x-US^{n+1}x=\sum_r v_r B_r S^n x\ge0,\qquad
\sum_r v_rH_{r,N}x=U(x)-US^Nx. \tag{5}
\]

Survival decreases to a nonnegative limit. For each \(r\), the scalar
sequence \(v_rH_{r,N}x\) increases and is bounded by \(U(x)\). If \(M>N\),
the increment \((H_{r,M}-H_{r,N})x\) lies in \(J_r\), so (4) gives

\[
\|(H_{r,M}-H_{r,N})x\|
\le c_r\bigl(v_rH_{r,M}x-v_rH_{r,N}x\bigr)\longrightarrow0. \tag{6}
\]

This proves vector convergence for every positive input. Because \(K\)
generates \(V\), choose a vector-space basis \(e_1,\ldots,e_d\) from \(K\).
Convergence on this finite basis defines a linear limit on \(V\). If
\(x=\sum_j a_j(x)e_j\), the finite-dimensional coordinate functionals are
bounded; hence
\(\|(H_{r,N}-H_r)x\|\le\sum_j |a_j(x)|\,\|(H_{r,N}-H_r)e_j\|\)
proves operator-norm convergence. Closedness of \(J_r\) preserves positivity.
The same basis argument gives dual-norm convergence of \(US^N\).
Pass to the limit in (5), using finitely many labels, to obtain (3).
Finally \(s_NS=s_{N+1}\), which yields \(\ell S=\ell\). ∎

For the probabilistic interpretation, complete branch accounting defines a
consistent finite outcome tree. In its induced countably additive path law,
the events “no commitment in the first \(N\) steps” decrease to “no commitment
ever”; continuity from above gives probability \(\ell(x)\). This does not
supply a physical occurrence mechanism or a finite observation of “never.”

For each fixed model the convergence is uniform over a bounded input set,
including its compact normalized base. This is not a uniform rate across
different models, prefixes, controller sizes or limiting families.

### Least positive solution, not an arbitrary inverse

The limits obey

\[
H_r=B_r+H_rS. \tag{7}
\]

Indeed \(H_{r,N}S=H_{r,N+1}-B_r\) and operator-norm limits commute with
multiplication by a fixed finite matrix. Moreover \(H_r\) is the **least
positive solution** of (7). Any positive solution \(T\) satisfies
\(T=H_{r,N}+TS^N\ge H_{r,N}\); closed cone order gives \(T\ge H_r\).

Equation (7) alone need not select \(H_r\). A conservative dark mode makes
\(I-S\) singular, and may permit positive solutions that assign spurious
commitments to that mode. Blind inversion or choosing an arbitrary solution
of (7) is rejected. Even a subnormalized positive solution need not be the
first-commit map.

## 3. What elimination preserves, and what it forgets

Expand \(S^n\) as the sum over legal silent branch paths. Each term
\(B_rS^n\) gives the unnormalized output after exactly \(n\) silent steps and
the first commitment with full label \(r\). The finite sums in (2), followed
by the proven limit, therefore retain the entire aggregated output residual,
not just its scalar probability.

For any declared later terminal effect \(f\) on \(Y_r\), or any finite lawful
continuation whose resulting effect is \(f\),

\[
\sum_{n\ge0} f B_rS^n x=fH_rx. \tag{8}
\]

Bounded finite-dimensional linearity and the operator-norm limit justify
this equality. Later controls may depend on the retained record and output
type under their declared rules; they cannot depend on a discarded
silent-path oracle. Nonlinear transformations of unnormalized mixtures,
unmodeled memory or additional observations require a new argument.

Elimination forgets silent step count, internal silent branch labels,
intermediate controller visits and silent residual trajectories. It does
**not** preserve bounded-wait probabilities, timing observations, or
interventions conditioned on discarded observations. If a committed record
actually includes a wait count or path tag, that information belongs in
\(r\) and cannot be marginalized while claiming to retain the full record.
An unbounded count in that payload generally leaves this finite-label
theorem's scope.

The scalar \(\ell(x)\) is a limiting path probability, not a newly committed
null event or a finite-time diagnosis of nontermination. It supplies **no
terminal residual state** on the never-commit event. A process with this
outcome cannot automatically be resumed from a scalar probability: later
finite-time intervention would need the retained microscopic process.

For a selected \(r\), normalize \(H_rx\) only if \(p_r=v_rH_rx>0\).
If \(p_r=0\), positivity and strict output mass imply \(H_rx=0\); there is
no conditional residual or append. The full law still includes the zero
branch. A structural append helper cannot check probability without a
residual; the state-aware selection must check it first.

Every committing \(r\) includes its actual setting/action/outcome and allowed
precursor ideal in \(C\). Append one fresh maximal event; all previous
records and order relations remain unchanged. A silent step appends nothing.
The executable example uses the entire current prefix as precursor, a
deliberately chosen chain rule, not a geometry generator. Its history
validation checks that grammar, not global reachability of an arbitrary
supplied history/residual pair.

These claims are at each **stated prefix and fixed controller law**. Applying
them after successive commitments requires the corresponding hypotheses at
each successor prefix. No unbounded-history closure or exchange of
continuum, controller-size and long-wait limits is inferred.

## 4. Lawful predictive quotient theorem

For every relevant external state type/prefix, let \(W_i\subseteq V_i^*\)
contain the mass unit and all declared terminal effects. Require pullback
closure under **every lawful continuation** \(T:V_i\to V_j\):
\(fT\in W_i\) for every \(f\in W_j\). Silent, committing, context-transition
and any separately available branch maps are included. Use corresponding
spaces for committing outputs and all later interfaces being claimed.
Here a lawful continuation is an available protocol branch or an aggregate
unobserved channel, not an arbitrary individually postselected refinement of
a hidden channel unless that refinement is separately available.

Set \(N_i=W_i^\perp\), \(q_i:V_i\to\bar V_i=V_i/N_i\), and
\(\bar K_i=q_i(K_i)\). Committed prefixes, full labels and externally known
apparatus types are **not** identified by this residual quotient.

**Descent theorem.** Every declared map and terminal effect has a unique
induced linear map/effect satisfying

\[
\bar Tq_i=q_jT,\qquad \bar f q_i=f,\qquad \bar u_i q_i=u_i. \tag{9}
\]

The induced maps are positive on \(\bar K_i\); complete mass accounting and
probability bounds descend. Under the compact-base premises of section 2,
\(\bar K_i\) is closed, pointed and generating, with strictly positive
\(\bar u_i\). The first-commit theorem therefore applies on these quotient
cones too, and

\[
q_rH_r=\bar H_rq,\qquad \bar\ell q=\ell. \tag{10}
\]

**Proof.** If \(z\in N_i\), then \(f(Tz)=(fT)z=0\) for every \(f\in W_j\),
so \(TN_i\subseteq N_j\). Terminal effects annihilate \(N_i\). These facts
are exactly the linear well-definedness conditions in (9). For \(x\in K_i\),
\(\bar T(q_ix)=q_jTx\in\bar K_j\), proving positivity. Surjectivity and (9)
give the descended mass identities. If \(0\le f\le u_i\) on \(K_i\),
then \(0\le\bar f\le\bar u_i\) on its image cone.

Closedness is **proved**, not presumed. Since \(u_i\in W_i\), it descends,
and the compact original normalized base \(D_i\) maps to precisely
\(\bar D_i=\{y\in\bar K_i:\bar u_i(y)=1\}=q_iD_i\), a compact set.
For nonzero \(y=q_ix\in\bar K_i\), \(x\ne0\) gives
\(\bar u_i(y)=u_i(x)>0\). Thus \(\bar D_i\) avoids zero. If
\(y_n=t_nb_n\in\bar K_i\) converges, with \(t_n=\bar u_i(y_n)\) and
\(b_n\in\bar D_i\) for nonzero \(y_n\), boundedness of \(\bar D_i\) makes
the limit zero when \(t_n\to0\). Otherwise a convergent subsequence in
\(\bar D_i\) represents the limit in \(\bar K_i\). This proves closedness.
Strict positivity proves pointedness; surjectivity and the generating
property prove generation of \(\bar V_i\).

Termwise intertwining gives
\(q_rH_{r,N}=\bar H_{r,N}q\). Continuity of the quotient maps and the
operator-norm limits give (10), with the analogous argument for survival
effects. Equal positive branch masses imply well-defined normalized
conditioning of equivalent positive representatives; zero branches have
no conditional state. ∎

One can state the descent obligation directly as
\(TN_i\subseteq N_j\) and \(f(N_i)=0\), without an algorithm for \(W_i\).
Finite future-effect closure from P2 constructs such a space only when the
whole claimed catalogue is captured by its finite typed interface.
Arbitrarily changing maps with an unbounded history are not automatically
covered. The theorems do not claim a general necessary-and-sufficient
classification of nonfaithful domains.

## 5. Exact periodic dark-controller example

The example has one external experiment, attempt, and two **internal**
controller modes with bright/dark coordinates
\(x=(b_0,d_0,b_1,d_1)^T\in\mathbb R_+^4\), mass \(U(x)=\sum x_i\).
All preparation/control rules here are supplied classical choices.

\[
S=\begin{pmatrix}
1/2&0&0&0\\0&0&0&1\\0&0&1/2&0\\0&1&0&0
\end{pmatrix},\qquad
B_0=\tfrac12 E_{b_0},\quad B_1=\tfrac12 E_{b_1}. \tag{11}
\]

Here \(E_j\) is the coordinate projection retaining coordinate \(j\) in the
four-dimensional output residual, not a scalar effect. The two full
committing labels retain source mode, action, outcome, target mode and
actual precursor. The internal typed decomposition consists of, at each
mode, a half-bright silent self-loop, a dark transfer to the other mode,
and a half-bright commitment. These are mutually exclusive possibilities
of the one attempt law. An individual silent edge is not an available
command or separately observed outcome in this interface.

For every nonnegative input, directly from (11),

\[
B_rS^n=2^{-(n+1)}E_{b_r},\quad
H_{r,N}=(1-2^{-N})E_{b_r},\quad H_r=E_{b_r},
\]
\[
US^Nx=2^{-N}(b_0+b_1)+d_0+d_1,\qquad \ell(x)=d_0+d_1. \tag{12}
\]

Thus \(\|H_r-H_{r,N}\|_{1\to1}=2^{-N}\), but
\(S^{2n}e_{d_0}=e_{d_0}\) and
\(S^{2n+1}e_{d_0}=e_{d_1}\). The silent residual does not converge.
Also \((I-S)(e_{d_0}+e_{d_1})=0\): the inverse is unavailable.
Let \(D\) send total dark mass to \(e_{b_0}\). Since \(DS=D\),
\(H_0+\alpha D\) solves (7) for every \(\alpha\ge0\). Even
\(\alpha=1/3\) keeps total first-commit output mass at most one on normalized
inputs while inventing dark commitments. The actual series selects
\(\alpha=0\), its least positive solution.

The quotient

\[
q(x)=(b_0,b_1,d_0+d_1)^T,\quad
\bar S=\operatorname{diag}(1/2,1/2,1)
\]

is lawful for the observed aggregate catalogue \(\{S,B_0,B_1,U\}\).
Its image cone is \(\mathbb R_+^3\), and the induced committing maps are
half-projections onto their corresponding bright coordinates. The future
effects span \(b_0,b_1,d_0+d_1\); the discarded direction is
\(e_{d_0}-e_{d_1}\). A positive representative of every quotient state is
obtained by putting all its dark mass in one internal mode.

This is a genuine nontrivial quotient of an **unobserved internal phase**,
not an identification of different known external settings. If a controller
readout distinguishes \(d_0\) from \(d_1\), or a singled-out dark edge becomes
an available postselected continuation, it fails the descent test. Adding
that observation invalidates the old quotient; it is not a claim that such
an observation is physically forbidden. Records and full committing labels
are unchanged throughout.

## 6. Obstructions and exact limits of the stronger claims

**A. Arbitrary projected cones need not be closed.** Project a positive
semidefinite real matrix
\(\begin{psmallmatrix}a&b\\b&c\end{psmallmatrix}\) to \((a,b)\).
Its image is \(\{(a,b):a>0\}\cup\{(0,0)\}\), not closed:
\(\begin{psmallmatrix}1/n&1\\1&n\end{psmallmatrix}\) is positive semidefinite,
while its image tends to the excluded \((0,1)\). Trace is a faithful source
mass but does not descend under this projection. Choosing mass \(a\)
instead makes mass descend but violates source strict positivity.
Neither setup satisfies the compact-base quotient hypotheses. Source
closedness alone is insufficient; closing the image by hand would add
states and is not performed here.

**B. Strict positivity is sufficient, not necessary; absence can matter.**
On \(K=\mathbb R_+^2\) with nonfaithful input/output mass \(u=v=(1,0)\),
the choice \(S=B=\tfrac12I\) gives
\(H_N=(1-2^{-N})I\to I\). Thus strict positivity is not necessary for
this particular series to converge.

With the same cones and units, instead choose
\(S=\operatorname{diag}(1/2,2)\), \(B=\operatorname{diag}(1/2,1)\).
Complete scalar mass still holds, but

\[
H_N=\operatorname{diag}(1-2^{-N},\,2^N-1)
\]

diverges. Scalar first-commit probabilities converge while invisible
residual coordinates diverge. For the declared catalogue \(\{S,B,u\}\),
the quotient \(q(x,y)=x\) is invariant, its cone is faithfully normalized
\(\mathbb R_+\), and its series converges to the identity. Thus elimination
can succeed **after quotienting** even though the unquotiented limit does
not exist. Equation (10) is not asserted with a nonexistent original \(H\).
This does not license erasing that coordinate if a later allowed restricted
readout can distinguish it.

**C. Eventual equality is weaker than full-process descent.** On
\(\mathbb R_+^2\), take
\(S=\operatorname{diag}(1/2,1/3)\) and scalar-output
\(B=(1/2,2/3)\). Then \(\sum_{n\ge0}BS^n=(1,1)\) and \(\ell=0\).
The eventual label and scalar output descend through \(q(x)=x_1+x_2\).
But neither \(S\) nor the one-step committing map \(B\) descends:
the two normalized basis inputs commit on the first attempt with
probabilities \(1/2\) and \(2/3\). The quotient is valid for that deliberately
coarse eventual question, not for the complete continuation interface.
An aggregate limit descending does not prove that every branch descends.

**D. No uniform model-family rate.** Scalar \(S=q,\ B=1-q\), \(0\le q<1\),
has tail \(q^N\). For each \(N\ge1\), choose rational
\(q_N=1-1/(2N)\). Bernoulli's inequality gives \(q_N^N\ge1/2\).
Every fixed model converges, but the premises alone give no decay bound
uniform across that family. This is not a new coverage or threshold gate.

## 7. Evidence, remaining obligation and stop

The proofs cover all inputs under their hypotheses. The exact checks
independently certify the typed branch decomposition, geometric formulas,
periodic obstruction, full record/precursor handling, quotient identities
and counterexamples. They do not prove the general theorem by testing a
finite sample, and are not evidence of physical availability.

Source hashes, reproduction commands and independent proof review are in the
[coordination handoff](../../coordination/QR_HANDOFF.md). The new source is
standard-library rational arithmetic, with no dependency on rewriting the
accepted P1/P2 bundle. No numerical inversion, empirical tolerance or
acceptance threshold is used.

**Remaining obligation:** select and justify a concrete operational
preparation/control/observation interface if the abstract result is to become
a physical or applied model. Any claim to discard a residual coordinate
must retain a continuation-invariance proof; any global history or family
limit needs its own hypotheses. A calibrated application or further domain
classification requires a separate bounded assignment. None is started here.

This sitting ends with the conditional theorems, exact counterexamples and
handoff for coordinator acceptance. No RET, clock, book, retired
\(\kappa\)-gravity, new QR-05 lettered work or physical promotion follows.
