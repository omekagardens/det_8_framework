# Full-layer half-scale continuity and an absolute P4 contrast bound

20 October 2026. Conditional manual finite-prefix theorem.

**Answer: yes for the explicitly prescribed half-scale continuation; no
for an arbitrary positive common-scale continuation.** Rebuilding the
complete six-parent layer by the published half-scale rule makes
\(\rho_\lambda\) continuous and bounded below on a compact neighborhood
of the conditional exceptional law. Consequently the [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) has a uniform
absolute \(P_4\) contrast there, for this selected construction.
The scale rule is an optional law prescription, not a consequence of bare
DET or of positivity, locality and diamond compatibility alone.

The result is symbolic and conditional. It does not select whether
\(\Xi>1\), supply a numerical neighborhood or effect size, or assert
physical observability.

## 1. Exact construction and full-domain premises

Fix the admitted positive, normalized, equivariant, record-local prefix
\(q^0\) through parent size five. Its smaller-parent probabilities, including
all full complements, are fixed mathematical inputs; the parent-four witness
and parent-five canonical construction are not rerun as \(\lambda\) varies.
For \(0<\lambda\le1\), leave every parent of size at most four unchanged
and set, for every marked five-parent and every individual ideal,
\[
 q_\lambda(P,r,S)=
 \begin{cases}
  \lambda q^0(P,r,S),&S\subsetneq P,\\
  1-\lambda+\lambda q^0(P,r,P),&S=P.
 \end{cases}                                                   \tag{1}
\]
These complete rows remain positive, normalized and continuous.
In particular a full probability in (1) is the complete complement,
not the old full probability or a complement of a selected support.

For a six-parent proper slot let
\(E(P,S)=\operatorname{Max}(P)\setminus S\). It is nonempty: the complement
of a proper ideal in a finite order contains a maximal element.
The published maximal-deletion potential is
\[
 u_\lambda(P,r,S)=
 \prod_{\varnothing\ne A\subseteq E(P,S)}
 q_\lambda(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}}.
                                                               \tag{2}
\]
Since \(A\cap S=\varnothing\), every indicated ideal is retained.
The smaller slot may be full, with its full induced marking.
These are evaluations of smaller mathematical inputs, not physical
deletion of committed records.

Define
\[
 T_{P,r}(\lambda)=\sum_{\substack{S\text{ ideal of }P\\ S\subsetneq P}}
                        u_\lambda(P,r,S),\qquad
 \mathcal M_6(\lambda)=\max_{\substack{|P|=6\\r:P\to\{0,1\}}}
                        T_{P,r}(\lambda).                       \tag{3}
\]
Every individual proper ideal occurrence is counted, including the empty
ideal. The maximum is over **all** marked six-parents, not the five affected
parents, the eleven supported children, two root sectors, or a selected
canonical component set. One may use all orders on a fixed six-element
label set and all binary markings: this is finite, and equivariance
identifies other label sets without dropping any mathematical row.

Select the published rule anew on this changed prefix:
\[
 \rho^H_\lambda=\frac1{2(1+\mathcal M_6(\lambda))},\qquad
 q^H_\lambda(P,r,S)=\rho^H_\lambda u_\lambda(P,r,S)\quad(S\subsetneq P),
 \qquad
 q^H_\lambda(P,r,P)=1-\rho^H_\lambda T_{P,r}(\lambda).              \tag{4}
\]
The superscript \(H\) distinguishes this choice from an unspecified common
scale. The theorem package prescribes (4) for its baseline; the law-family
supplement permits a compatible common-scale continuation of the changed
prefix without forcing this particular choice. Here (4) is stated explicitly.

The admitted ratio-component theorem makes a sufficiently small common
positive scale compatible with the full proper-slot equations. Together
with full complements it supplies the accepted record-local construction
and complete unnormalized diamond identities. This remains a premise,
not a newly proved derivation from DET. Binary records and both fair newborn
outcomes remain, with scalar-passive maps \(q^H_\lambda\mathfrak D/2\) for
arbitrary admitted PSD payload \(\mathfrak D\).

## 2. Continuity, positive complements and the compact lower bound

All factors in (2) are positive continuous functions of \(\lambda\).
A finite product and the reciprocal of a nowhere-zero continuous function
are continuous. Thus every potential is finite, positive and continuous
on \(0<\lambda\le1\). This reasoning includes smaller full slots;
their positivity, not an unsupported cancellation, legitimizes reciprocals.

The sums (3) are finite continuous functions on a fixed finite index set.
A finite maximum is continuous, regardless of changes in which row attains it:
\[
 \left|\max_j f_j(\lambda)-\max_j f_j(\lambda')\right|
 \le\max_j|f_j(\lambda)-f_j(\lambda')|.                          \tag{5}
\]
No differentiability, unique maximizing parent, or active-set persistence
is needed. In particular, this is not a continuity claim about a rerun
lexicographic optimization procedure.

Equation (4) has denominator \(2(1+\mathcal M_6)\ge2\), so
\(\rho^H_\lambda>0\) is continuous. Every proper probability is positive
continuous, and its **complete** full complement satisfies
\[
 q^H_\lambda(P,r,P)
 \ge1-\frac{\mathcal M_6}{2(1+\mathcal M_6)}
 =\frac12+\rho^H_\lambda>\frac12.                              \tag{6}
\]
Consequently the full six-parent layer is a positive continuous family.

For any compact interval \(\mathcal I\subset(0,1)\), put
\[
 B_{\mathcal I}=\max_{\lambda\in\mathcal I}\mathcal M_6(\lambda)<\infty,
 \qquad
 \underline\rho_{\mathcal I}
       =\frac1{2(1+B_{\mathcal I})}>0.                         \tag{7}
\]
Then \(\rho^H_\lambda\ge\underline\rho_{\mathcal I}\) throughout
\(\mathcal I\). This is a symbolic, construction-dependent bound.
Finiteness of the layer alone would not suffice if the input probabilities
were arbitrary discontinuous positive functions; continuity of (1) and
the fixed positive smaller prefix are essential.

## 3. A coarse bound without computing a maximizing row

The present family admits a stronger elementary estimate. Negative
exponents in (2) correspond exactly to nonempty even subsets \(A\).
Thus \(|A|\ge2\), and every denominator probability belongs to a parent
of size at most four. Those probabilities are independent of \(\lambda\).

Let
\[
 m_4=\min_{\substack{|Q|\le4,\ r:Q\to\{0,1\}\\
                         S\text{ any ideal of }Q}}q^0(Q,r,S)>0. \tag{8}
\]
The minimum is over the complete fixed prefix, including full ideals and
the empty parent, whose sole ideal has probability one. It is finite by
using fixed finite label sets at each size, and \(m_4\le1\).
No held-row or root-only substitution for this full minimum is made.

If \(k=|E(P,S)|\le6\), there are exactly \(2^{k-1}-1\le31\) denominator
occurrences in (2). Repeated coordinates still count as repeated factors.
Every numerator factor is a normalized probability at most one, whereas
each denominator is at least \(m_4\). A six-element parent has at most
\(2^6-1=63\) individual proper ideals. Therefore, for every marked row,
\[
 u_\lambda(P,r,S)\le m_4^{-31},\qquad
 \mathcal M_6(\lambda)\le63m_4^{-31},\qquad
 \boxed{\ \rho^H_\lambda\ge
    c_4:=\frac1{2(1+63m_4^{-31})}>0.\ }                       \tag{9}
\]
This is a bound on the original full-layer maximum, not its replacement
by a restricted maximum. It needs no numerical coefficient allocation,
maximizer identification, or experiment.

Only singleton deletions in (2) can reach parent size five.
Their factors are affine in \(\lambda\) by (1); all remaining factors
are fixed positive constants or their reciprocals. Hence each \(u_\lambda\)
is a polynomial in \(\lambda\) of degree at most \(k\le6\), with fixed
real coefficients. The affine full-slot factor need not be proportional
to \(\lambda\), and polynomial coefficients need not all be positive.
The finite maximum of these row-sum polynomials remains continuous even
when its maximizing row changes.

The scale bound (9) holds on \(0<\lambda\le1\); it does **not** enlarge
the regular family's perturbation-positivity neighborhood, admit \(\lambda=0\),
or establish any later-layer or all-size result.

## 4. Upgrade of the regular observable family for the selected law

Continue to condition on the unselected comparison
\[
 \Xi=\theta+360\mu_1-359\mu_0>1,\qquad \lambda_*=\Xi^{-1}\in(0,1).
\]
The regular-family theorem supplies the continuous eleven-coordinate section \(v(\lambda)\),
normalized by \(v_{11}=1\), one fixed amplitude
\(\eta_*=1/(2\kappa_*)>0\), and a compact neighborhood
\(\mathcal I_*\subset(0,1)\) of \(\lambda_*\) on which every multiplier
is at least \(1/4\). Its section and neighborhood use the fixed
parent-five family, not any regularity of the parent-six common scale.
The complete harmonic system has that positive scale as a cancellable
common factor, so the same section, amplitude and neighborhood apply to (4).

At \(P_4=C_4\oplus A_2\), the accepted complete-row contrast for each
root sector \(i=0,1\) is
\[
 \delta^H_{4,i}(\lambda)
  =-2\eta_*\rho^H_\lambda F_i(\lambda)v_{10}(\lambda),
 \qquad F_i(\lambda)=1-\lambda(\theta+\mu_i),                    \tag{10}
\]
including the \(T_4\), \(T_9\) and both \(T_{10}\) occurrences, all eight
individual ideals and both newborn bits. The same amplitude applies in
both sectors. On \(\mathcal I_*\), the regular-family theorem proves
\[
 \frac{F_i(\lambda)}2
 \le\frac{\delta^H_{4,i}(\lambda)}{\rho^H_\lambda}
 \le\frac{3F_i(\lambda)}2,\qquad
 \frac{\delta^H_{4,i}(\lambda)}{\rho^H_\lambda}>\frac14.         \tag{11}
\]
The previously missing scale premise is now proved from the explicit rule.
Combining (7) and (11) gives
\[
 \delta^H_{4,i}(\lambda)>
 \frac1{8(1+B_{\mathcal I_*})}>0
 \quad(\lambda\in\mathcal I_*,\ i=0,1).                        \tag{12}
\]
Alternatively the fully symbolic coarse bound (9) gives
\[
 \boxed{\quad
 \delta^H_{4,i}(\lambda)>d_4:=
   \frac1{8(1+63m_4^{-31})}>0
 \quad(\lambda\in\mathcal I_*,\ i=0,1).
 \quad}                                                       \tag{13}
\]
In particular \(\inf_{\mathcal I_*}\delta^H_{4,i}\ge d_4\).
No numerical value for \(d_4\) is asserted. All factors in (10) are now
continuous, so the absolute contrast, not just its quotient by the scale,
is continuous for this construction.

The \(P_1\) quadratic upper bound is unaffected: its contrast contains
\(\chi(\lambda)^2\) and remains zero at the exception. Nothing here
establishes a sharp \(P_1\) rate or a matching lower bound there.
The observation underlying (10) still requires exact complete child-order
access and the known parent embedding. An absolute mathematical
probability-contrast bound does not supply a physical detector or sampler.

## 5. Why positivity and compatibility alone do not force this result

An arbitrary admissible positive common-scale continuation can use a
different scale function at each parameter. The principles impose
pointwise capacity conditions, not continuity in this external law parameter.

For an explicit obstruction on the same \(\mathcal I_*\), set
\[
 b(\lambda)=
 \begin{cases}
  |\lambda-\lambda_*|,&\lambda\ne\lambda_*,\\
  1,&\lambda=\lambda_*,
 \end{cases}
 \qquad
 \rho^{\rm bad}_\lambda=b(\lambda)\rho^H_\lambda.                \tag{14}
\]
Because \(\mathcal I_*\subset(0,1)\), \(0<b\le1\). Use
\(\rho^{\rm bad}_\lambda u_\lambda\) on all proper slots and their
complete full complements. Each fixed-parameter row remains positive,
normalized and compatible under the admitted common-scale theorem;
its full complement is at least the half-scale complement.
No new claim of continuity is needed for its validity as separate laws.

Nevertheless \(\rho^{\rm bad}_\lambda\to0\) on a punctured approach to
\(\lambda_*\), while its value there is positive. Its neighborhood infimum
is zero. The same multiplier family remains valid because the common scale
cancels from harmonicity; its contrast is
\(\delta^{\rm bad}_{4,i}=b\,\delta^H_{4,i}\).
The half-scale contrast is bounded and continuous, so this alternative
contrast approaches zero along that punctured approach and has no uniform
positive lower bound. This is a counterexample to a principle-only
regularity inference, not a statement about the selected rule (4).

Other regular selections are possible. For example, a separately chosen
constant \(0<c<1\) gives
\[
 \rho^{(c)}_\lambda=\frac{c}{1+\mathcal M_6(\lambda)},\qquad
 q^{(c)}_\lambda(P,r,P)>1-c.
\]
It is continuous and bounded below on compact intervals by the same
argument. It is another optional law choice, not a forced replacement,
a coordinate gauge, or a new selection made for this deliverable.

| Continuation | Conclusion | Source of the conclusion |
| --- | --- | --- |
| Unspecified positive common scale | Pointwise positive laws; regularity and absolute uniform contrast need not hold | Admitted growth principles plus pointwise capacities only |
| Full-layer half-scale (4) | Continuous scale and positive lower bounds (7), (9); absolute contrast (12), (13) | Fixed continuous prefix **and** explicit optional normalization rule |
| Separately prescribed regular scale, e.g. constant \(c\) above | Similar bounds when its stated regularity and capacity conditions hold | Additional law prescription, not uniqueness from DET |

## 6. What is established and what is not numerically available

For (7), \(B_{\mathcal I_*}\) depends on the entire admitted prefix and
the chosen compact interval. For (9) and (13), \(m_4\) depends on the
complete fixed prefix through parent four. The interval and amplitude
still depend on the original coefficients and the conditional exception;
their existence comes from the regular-family theorem. No actual \(\Xi\) comparison is selected.

These are existential and symbolic quantitative bounds, not evaluated
numbers. The public premises do not supply the full parent-four and
parent-five coefficient tables, a certified numerical value of the full
minimum (8), or a certified neighborhood radius.
Consequently no numerical lower signal bound is certified here.

If complete exact rational lower-prefix data, or a certified positive
lower bound \(\widehat m_4\le m_4\), were supplied, substituting
\(\widehat m_4\) in (9), (13) would give an evaluable conservative bound.
Computing a sharper \(B_{\mathcal I_*}\) would additionally require all
full-layer potentials and an identified interval with certified bounds.
Neither an effective numerical computation from unspecified positive
real inputs nor any coefficient acquisition is claimed.

There is no missing regularity premise for the **explicitly selected**
half-scale family: it has been proved from the finite continuous prefix.
There remains no principle forcing that selection, and numerical
evaluation is a distinct, unperformed task.

## Public premises and scope

The [theorem package](THEOREM_PACKAGE.md) supplies the admitted
deletion potential, complete full-layer half-scale definition and the
distinction between continuation existence and prescribed optimization.
The [law-family supplement](LAW_FAMILY_SUPPLEMENT.md) supplies the
parent-five scaling family and the need to rebuild later layers.
The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) supplies the
continuous kernel section, fixed positive amplitude, existence-defined
neighborhood and complete two-sector \(P_4\) contrast.

The positive compatible lower prefix, ratio-component construction,
complete marked-row harmonic reduction and scalar-passive shared-terminal
payload identities remain admitted premises. The continuity and bounds
printed here are manual conditional finite mathematics for the explicitly
prescribed half-scale family. The full-domain maxima, all denominator
occurrences and complete normalization complements are retained; no
selected-support maximum substitutes for them.

The actual \(\Xi\) comparison, numerical coefficient values, numerical
neighborhood and numerical effect bound remain unselected or unevaluated.
No coefficient acquisition, sampling implementation, observed simulation,
h8/30/33/38 transfer, all-size harmonic extension, informative quantum
dynamics, geometry, mass/gravity or physical-observability result is supplied.
This theorem does not change application protocols or establish benchmark
success, historical custody or production qualification. See the
[publication note](PUBLICATION_NOTE.md) for evidence boundaries and the
[metadata-obscured publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the separation of public exposition from private source correspondence.
