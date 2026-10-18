# RI-16 — first commitment with retained command words

14 September 2026 UTC. **CONDITIONAL_COUNTABLE_LABEL_FIRST_COMMIT_THEOREM;
PREFIX_SHIFT_LEAST_SOLUTION; UNIFORMLY_BOUNDED_CONTINUATION_INTERCHANGE.**
Proof and exact supplement accepted by the coordinator on 14 September
2026 UTC. This extends the named
finite-full-label boundary of
[RI-07 §§2–4](../t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md)
under explicit finite-input and output-norm premises. It does not select a
physical record-formation law, add an instrument, or identify physical time.

## 1. Fixed policy, retained words and hidden paths

Fix one committed prefix C and one complete stationary experiment or finite
controller policy. All action-selection probabilities are already included
in its mutually exclusive branch maps. A sum of independently available
commands is not a policy. This theorem does not authorize an arbitrary
full-word-dependent in-run policy unless it is represented by the declared
finite controller.

Let the finitely many input controller types have nonzero finite-dimensional
real spaces \(V_i\), closed pointed generating cones \(K_i\), and linear
mass units \(u_i\) strictly positive on \(K_i\setminus\{0\}\). Write
\[
V=\bigoplus_iV_i,\qquad K=\bigoplus_iK_i,\qquad
u(x)=\sum_i u_i(x_i).
\]
The internal direct sum preserves controller state without asserting that
it is observed. A known external controller/type remains part of the stated
interface, not a hidden-state oracle.

Let \(\mathcal A\) be a finite alphabet of actual retained command tokens.
Optionally include \(\varepsilon\), a silent step retaining no token.
For each \(a\in\mathcal A\cup\{\varepsilon\}\), supply a positive
linear \(S_a:V\to V\). It may aggregate hidden branches only when they
have the same retained token and compatible target typing. All hidden
controller components remain in the declared residual space. Set
\[
S=\sum_a S_a.
\]
Distinct hidden realizations are not recorded merely to distinguish terms
in this sum. If a path detail is actually retained, it must instead belong
to the declared alphabet, committing label or output type.

Let R be a finite set of committing base labels. Each label retains its
actual action, setting, outcome, allowed precursor in C and output type,
apart from the accumulated word recorded separately. Supply positive linear
\(B_r:V\to Y_r\), where each output cone \(J_r\subset Y_r\) is closed,
pointed and generating in a finite-dimensional real space, with strictly
positive mass \(v_r\). A type containing hidden controller alternatives
keeps them in its residual direct sum; that bookkeeping does not make
their selectors observable. Incompatible output types are never averaged.
The complete unnormalized mass law is
\[
\boxed{uS+\sum_{r\in R}v_rB_r=u.}\tag{1}
\]
All maps and equalities concern unnormalized residuals. Comparison of
normalized inputs requires the same C, context, known initial pending word
\(w_0\), controller declarations and nominal policy. A committing output
records \(w_0w\), not just its matrix action; \(w_0\) has already been
applied to the supplied snapshot and is not applied again here.

There are countably many possible finite words \(w\in\mathcal A^*\),
even with a finite alphabet and controller. The output label is the full
pair \((w,r)\). Hidden paths may be summed only inside a coordinate with
identical retained label and residual/output type. Availability, complete
policy selection and the history grammar remain premises, not consequences
of the following convergence theorem.

## 2. A complete residual output space

Equip V with its faithful base norm
\[
\|x\|_u=\inf\{u(p)+u(q):x=p-q,\ p,q\in K\}.
\tag{2}
\]
Use the analogous norm \(\|\cdot\|_{v_r}\) on each output space. The
closed, pointed, generating finite-dimensional hypotheses and faithful mass
make these genuine complete norms. For example, compactness of the positive
unit sphere bounds an ambient norm by a constant times mass on the cone;
this rules out a nonzero vector of zero base norm. Generating cones give
the required decompositions. In particular
\[
\|x\|_u=u(x)\ (x\ge0),\qquad
\|y\|_{v_r}=v_r(y)\ (y\ge0).
\tag{3}
\]
Define the countable output space and cone
\[
\mathcal W=\bigoplus_{(w,r)\in\mathcal A^*\times R}^{\ell^1}
(Y_r,\|\cdot\|_{v_r}),\qquad
\|z\|_{\mathcal W}=\sum_{w,r}\|z_{w,r}\|_{v_r},
\]
\[
\mathcal J=\{z\in\mathcal W:z_{w,r}\in J_r\},\qquad
v(z)=\sum_{w,r}v_r(z_{w,r}).
\tag{4}
\]
The series defining v is absolutely convergent, since
\(|v_r(y)|\le\|y\|_{v_r}\). The standard Cauchy-sequence argument for
an \(\ell^1\) sum of complete spaces makes \(\mathcal W\) Banach:
coordinates converge, the summed norm controls their tails, and the limiting
sequence has finite summed norm. Its positive cone is closed, because every
coordinate projection is continuous. Positive and negative base-norm
decompositions in each coordinate also make this cone generating. Most
importantly,
\[
\boxed{\|z\|_{\mathcal W}=v(z)\quad(z\in\mathcal J).}\tag{5}
\]
No word-dependent mass-to-norm constant is hidden in this identity. If
different coordinate norms are used instead, a uniform bound over all words
must be proved; individual finite-dimensional norm equivalence is not enough.

For any positive linear \(T:V\to\mathcal W\), base decompositions give
\[
\boxed{\|T\|_{u\to\mathcal W}
=\sup_{x\ge0,\,u(x)=1}v(Tx)
=\|vT\|_{u,*}.}\tag{6}
\]
Indeed, the supremum bounds \(\|Tp\|+\|Tq\|\) for every decomposition
\(x=p-q\); taking the infimum proves one inequality. Positive unit inputs
give the reverse. The same argument identifies the dual norm of a positive
functional with its supremum on the positive normalized base. Finite input
dimension ensures every linear map into this Banach output space is bounded.

## 3. Chronological truncations and prefix shifts

Let \(J_B:V\to\mathcal W\) put \(B_rx\) in \(((),r)\) and zero
elsewhere. Define the positive prefix-shift isometry \(L_a\) by moving
coordinate \((w,r)\) to \((aw,r)\), and set \(L_\varepsilon=I\).
Shifts retain every other label, residual entry and type. In particular
\(vL_a=v\).

Define
\[
H_0=0,\qquad
\boxed{H_{N+1}=J_B+\sum_a L_aH_NS_a.}\tag{7}
\]
Equivalently, H_N sums, for \(0\le n<N\), all paths
\(a_1,\ldots,a_n\) with output payload
\[
B_rS_{a_n}\cdots S_{a_1}x
\quad\text{at}\quad
(\operatorname{erase}_{\varepsilon}(a_1\cdots a_n),r).
\tag{8}
\]
The first applied command is the leftmost retained token. The first shift
is \(L_{a_1}\), acting outside all later shifts; reversing that convention
would reverse the recorded chronological word even if some matrices commute.

N bounds the **total number of silent steps** before commitment, not merely
retained-word length. Hidden \(\varepsilon\) steps can make many lengths
and paths contribute to one coordinate. H_N has finite support, is positive,
and \(H_{N+1}-H_N\) is positive. Aggregation uses sums of raw positive
residuals, never sums of individually normalized conditional states.

Applying v to (8), using (1), telescopes exactly:
\[
vH_N=\sum_{n=0}^{N-1}\sum_rv_rB_rS^n
=u-uS^N.\tag{9}
\]
This calculation sums masses across labels only to check completeness. It
does not replace the retained-word residual output by that scalar summary.

## 4. Full operator convergence and exact tail accounting

**Theorem.** Under §§1–2, H_N converges in operator norm to a positive
\(H:V\to\mathcal W\). The functionals \(s_N=uS^N\) converge in dual
norm to a positive \(\ell\), and
\[
\boxed{vH+\ell=u,\qquad \ell S=\ell,\qquad \|H\|\le1.}\tag{10}
\]
The complete countable first-commit law and exact tail relations are
\[
\sum_{w,r}v_r(Hx)_{w,r}+\ell(x)=u(x),\qquad x\ge0,
\tag{11}
\]
\[
\boxed{\|H-H_N\|_{u\to\mathcal W}
=\|uS^N-\ell\|_{u,*},}\qquad
\boxed{\|(H-H_N)x\|_{\mathcal W}=uS^Nx-\ell(x)\quad(x\ge0).}
\tag{12}
\]
There is no requirement that \(S^N\to0\) or that silent residuals converge.

**Proof.** For positive x, (1) implies
\(0\le s_{N+1}(x)\le s_N(x)\le u(x)\). Choose a vector-space basis
from the generating cone K. The finitely many decreasing bounded values
\(s_N\) on that basis have limits, defining a linear \(\ell\). Bounded
finite-dimensional coordinate functionals then give dual-norm convergence
\(s_N\to\ell\). Positivity and \(\ell\le u\) follow on every
positive input, and \(s_NS=s_{N+1}\) gives \(\ell S=\ell\).

For M>N, \(H_M-H_N\) is positive. Equations (6) and (9) give
\[
\|H_M-H_N\|=\|s_N-s_M\|_{u,*}\longrightarrow0.
\tag{13}
\]
Because \(\mathcal W\) is Banach, the bounded-operator space is complete,
so H_N has a limit H. The closed positive cone makes H and H−H_N positive.
Passing to the limit in (9) proves (10)–(11). Applying (6) and then (5)
to H−H_N proves both equalities in (12). This also proves absolute
summability of positive coordinate payloads, not merely convergence of
each label's scalar probability. ∎

For a normalized positive input, a consistent countably additive path law
for the declared complete policy interprets \(s_N(x)\) as survival through
N decisions and \(\ell(x)\) as never committing. Continuity from above
justifies this limiting probability. It is not an observed null record,
a finite-time diagnosis, or a supplied residual on the infinite silent path.
The tail in (12) subtracts never mass: \(s_N\) itself need not tend to zero.

Convergence is uniform over bounded inputs of each fixed finite-dimensional
model. The theorem gives no rate uniform across different policies, model
families, controller sizes, reference limits or growing prefixes.

## 5. The retained-word fixed point and leastness

The finite sum of bounded prefix shifts and input maps is continuous in
operator norm. Taking the limit in (7) gives
\[
\boxed{H=J_B+\sum_aL_aHS_a.}\tag{14}
\]
Writing only \(H=B+HS\) would generally discard words and use a different
output object. No inverse of \(I-S\) defines the retained-word map.

**Least-positive-solution theorem.** H is the least positive bounded
solution of (14). If a positive T solves that equation, positivity and
H_0=0 imply inductively T≥H_N. More explicitly,
\[
T=H_N+\sum_{a_1,\ldots,a_N}
L_{a_1}\cdots L_{a_N}\,T\,S_{a_N}\cdots S_{a_1}.
\tag{15}
\]
The remainder is positive. Closed cone order therefore gives T≥H after
taking the limit. The same monotone induction bounds H by every positive
supersolution \(T\ge J_B+\sum_aL_aTS_a\).

There is an important distinction. Without \(\varepsilon\), every silent
step retains a nonempty letter. The empty-word coordinate is then B_r, and
each longer coordinate is fixed recursively by its first letter; solutions
in this word-indexed space are unique. That special case does not invalidate
leastness, but it cannot use an unlabelled dark-added fixed point as a second
retained-word solution.

With genuine hidden empty steps, nonuniqueness is possible. On
\(V=\mathbb R^2\), \(K=\mathbb R_+^2\), \(u(b,d)=b+d\), take
\[
S_\varepsilon(b,d)=(b/2,d),\qquad B(b,d)=b/2\in\mathbb R_+.
\]
All commits have the empty retained word. The true limit is H(b,d)=b and
\(\ell(b,d)=d\). Nevertheless \(T_c(b,d)=b+cd\), supported at that same
empty word, solves (14) for every c≥0. For 0≤c≤1 it is even positive and
mass-nonincreasing. Only c=0 is the least solution and actual first-commit
law. An arbitrary fixed-point solution can fabricate a commitment of never
mass despite satisfying those other conditions.

## 6. Word-dependent continuations without erasing labels

For each retained coordinate \(j=(w,r)\), independently supply a linear
continuation \(C_j:Y_r\to Z_j\), where Z_j is a declared Banach residual
output space. Require a proved or explicitly assumed uniform bound
\[
\sup_j\|C_j\|\le M<\infty.\tag{16}
\]
Let \(\mathcal Z=\bigoplus_j^{\ell^1}Z_j\) and define the diagonal
map \((\mathcal Cz)_j=C_jz_j\). It retains j; new continuation records
may be attached inside the declared output, never in place of the original
word/label. Then
\[
\|\mathcal C\|\le M,\qquad
\boxed{\mathcal CH_N\to\mathcal CH\ \text{in operator norm},\quad
\|\mathcal C(H-H_N)\|\le M\|uS^N-\ell\|_{u,*}.}\tag{17}
\]
Indeed \(\sum_j\|C_jz_j\|\le M\sum_j\|z_j\|\); bounded linearity
permits interchange with the norm-convergent first-commit sum. This proves
the whole retained-output assertion, not just each coordinate separately.
The continuation may depend on the actual retained word, but not on a
discarded empty-step count or hidden path.

If each Z_j has its own faithful base norm and \(C_j\) is positive and
mass-nonincreasing, the base-decomposition argument gives \(\|C_j\|\le1\)
uniformly. This is the natural mathematical contraction contract. It does
not establish physical availability, nor permit operational continuation
after a terminal-only output. A map aggregating distinct j into one target
is a separate coarse question; its boundedness does not make that aggregation
record-preserving or sufficient for every later word-dependent question.

After summing all compatible hidden contributions to coordinate j, its
selected weight is \(p_j=v_r(Hx)_j\). Only p_j>0 permits the conditional
residual \((Hx)_j/p_j\) and an append with its full label and allowed
precursor, preserving all prior records. If p_j=0, faithfulness implies
\((Hx)_j=0\): no conditional state or record is invented. There is no
corresponding normalization or residual for the scalar never probability.

## 7. Terminal-read effects are not postread residual maps

The accepted [RI-08i §§2,7](../t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md)
and [RI-08j §5](../t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md)
terminal read supplies the positive unnormalized linear effects
\(e_{\alpha,\pm}(N)\), with full cell/sign labels and
\(\sum_{\alpha,\pm}e_{\alpha,\pm}=m\). It can enter B only with scalar
output cone \(\mathbb R_+\) and identity mass, retaining the complete
word/cell/sign record. Policy selection factors must be included. It does
not supply a linear postread residual.

In particular, an audit pre-read source cannot manufacture the map
\[
F(N)=e(N)\,N/m(N).\tag{18}
\]
Choose normalized sources N_+,N_- with e(N_+)=1 and e(N_-)=0, for example
opposite projectors of the fixed tilted effect in one filtered cell.
Then
\[
F((N_++N_-)/2)=(N_++N_-)/4
\ne\bigl(F(N_+)+F(N_-)\bigr)/2=N_+/2.
\]
The generally nonlinear audit construction fails the branch-map premise.
Keeping N in a sidecar does not repair linearity, certify previous preparation
probabilities, or grant an operational continuation. Scalar postread
statistics may be analyzed mathematically without pretending they are a
reusable quantum residual.

By contrast, the already declared literal-cut maps
\(N\mapsto P_\alpha NP_\alpha\) on fixed interior L_t are positive,
linear unnormalized residual maps with complete mass accounting
([RI-08g §§3–4](../t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md)).
They may use their declared residual output types in this theorem when a
complete stationary policy is supplied. This does not retag older terminal
cut objects, supply a reference reset, infer all physical preparations or
extend faithful base-norm claims through singular endpoint mass.

## 8. Counterexamples to omitted hypotheses

**Nonuniform coordinate norms.** On scalar input with mass x, let
S_a x=x/2 and Bx=x/2. Coordinate \((a^n,r)\) has weight
\(2^{-(n+1)}x\), and total committing mass is x. If its norm is instead
\(\|y\|_n=2^{n+1}|y|\), every coordinate is complete and individually
norm-equivalent to its faithful mass norm, but \(\|H_N(1)\|=N\).
The supposed infinite output does not lie in that weighted \(\ell^1\)
space. Uniform control cannot be replaced by coordinatewise norm equivalence.

**Unbounded continuations.** With the same geometric law in ordinary
\(\ell^1\), choose \(C_{a^n}(y)=2^{n+1}y\). Each map is individually
bounded and positive, but the uniform bound fails. Continued terms all have
mass one at input 1, so partial sums again have norm N. These maps are not
mass-nonincreasing; positivity alone does not justify (17).

**Word erasure.** On \(\mathbb R_+^3\) with basis e_0,e_1,e_2 and sum
mass, set \(S_a e_0=e_2\), \(S_b e_1=e_2\), \(Be_2=1\), and all
other branch values zero. This is one complete stationary policy. Inputs
e_0 and e_1 commit with identical scalar payload after one silent step but
at words a and b respectively. The bounded word-dependent effect
\(f_w(y)=\mathbf1_{\{w=a\}}y\) distinguishes them. Erasing the words
loses a legitimate retained question even though scalar totals match.

**Infinite-dimensional input.** Let input be \(\ell^1(\mathbb N_0)\)
with its positive cone and sum mass. Define
\[
S_a e_0=0,\quad S_a e_{n+1}=e_n,\qquad Bx=x_0.
\]
The full retained-word map is the isometry
\(Hx=(x_n)_{(a^n,r)}\), and H_N keeps coordinates n<N. Every input has
\(\ell(x)=0\) and H_Nx→Hx, but
\[
\|H-H_N\|=1\quad\text{for every }N,
\]
as seen on e_N. Faithful base norms and pointwise convergence alone do not
give operator-norm convergence without the finite-input argument. Here the
normalized positive base is not compact and \(uS^N\) does not converge
to zero in dual norm.

**No uniform model-family rate.** For scalar \(S_a=qI\), \(B=(1-q)I\),
0≤q<1, the exact tail norm is q^N. At every finite N its supremum over
q<1 is one, although each fixed model converges. A claim of uniform speed
across the family needs an additional quantitative assumption.

## 9. Exact supplement and scope of verification

The bounded [model](model.py) and independent [checks](check.py) are an exact
rational supplement, not an implementation of arbitrary infinite-output
operators. A symbolic word law and finite truncations illustrate the theorem;
the proof of its infinite limit is §§2–6, not enumeration to a chosen depth.

The primary declared toy policy has positive input \((x_0,x_1,d)\), mass
\(x_0+x_1+d\), retained letters A,B, and maps
\[
S_A(x_0,x_1,d)=(x_1/4,x_0/4,d/2),\quad
S_B(x_0,x_1,d)=(x_0/4,x_1/4,d/2),\quad
B(x_0,x_1,d)=(x_0/2,x_1/2).
\]
Committing outputs retain a positive two-coordinate residual. The A map
may be resolved into hidden subbranches with the same retained token;
their sum, not a public hidden-path label, defines the output coordinate.
For a word w of length n with A-count parity \(\pi(w)\),
\[
(Hx)_{w}=\frac{\operatorname{swap}^{\pi(w)}(x_0,x_1)}{2\,4^n},\qquad
\ell(x)=d,\qquad
\|(H-H_N)x\|=2^{-N}(x_0+x_1).
\]
There are \(2^n\) distinct words of length n. The total first-commit
mass is \(x_0+x_1\), not \(x_0+x_1+d\); the latter includes genuine
never mass. Original pending words and full prior records are retained.
No earlier preparation/reference-selection probabilities are inferred.
The illustrated continuation family depends on the last **newly** retained
letter, with a separate empty-new-suffix row even if the initial pending word
is nonempty. Its three coefficient rows lie in the unit box, proving a
uniform positive-contraction bound for all words. It is not an interface
that certifies arbitrary word-dependent functions by sampling them. Explicit
truncation is capped at twelve levels as an execution guard; the symbolic
coordinate and tail formulas, and the theorem, have no such cutoff.

The supplemental nonclassical case uses only an already declared interior
L_t cut-face at t=3/5 in faithful filtered coordinates: the existing common-X
A command and literal cut on occupied cell00, each selected with weight 1/2
by a fixed complete waiting/commit policy. A length-n output is
\(2^{-(n+1)}A^n\sigma A^{\dagger n}\), retaining its full word and
positive two-by-two residual. The native correspondence is the accepted
image with other blocks zero and
\(\rho_{00}=10D_{00}^{-1}\sigma D_{00}^{-1}\),
\(D_{00}=\operatorname{diag}(2,1)\). These residuals can fail to commute;
this is a representation of declared maps, not a new instrument, quantum
state-space classification or availability claim. The `TerminalScalar`
example evaluates the existing tilted scalar effect on a lawful literal-cut
coordinate, preserving its label and adding cell/sign. It is a mathematical
continuation statistic, not a replacement first-commit instrument or a
postread residual. Direct scalar committing effects have the separate
conditional status described in §7.

Focused normal and optimized checks, exact source pins and independent
full proof/source review are reported in the
[QR handoff](../../coordination/QR_HANDOFF.md). The accepted synthesis,
earlier bundles, registry/runner/schema, RI-15, claims, coordinator records,
core/RET/application source and protected evidence are not edited. Git/index
operations remain with the coordinator. No general SDK, physical-QM selection,
apparatus/bank work, automatic successor or new finite-cone refinement is
started. This bundle stops for independent coordinator review and acceptance.
