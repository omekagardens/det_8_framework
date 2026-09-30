# RI149 — exact capacities and canonical-face relation for the singleton hooks

Author-side manual proof, 30 September 2026. This derives the complete
symbolic row-cap and history-weighted objective contributions of the two
target components, then an exact saturation relation at the unchanged
canonical optimum. It does not evaluate either coefficient, prove an
ordering of them, or decide the RI147 weighted-margin budget. It is not
independent acceptance or execution authority.

## 1. Coordinates, incident rows, and retained other variables

Let `k_0,k_1` be the **existing** canonical component indices containing
the C5 singleton-root roles with root bits `0,1`. Write their boundary
coordinates as `a_i=alpha_(k_i)`, not as actual strictly mixed coefficients.
The actual correction and its difference are

\[
 \kappa_i=\frac{35}{36}a_i^*,\qquad
 \delta_\kappa=\frac{35}{36}(a_0^*-a_1^*),
 \tag{1}
\]

where the star denotes the fixed RI63 primary-plus-lexicographic canonical
optimum. The common strict-restoration term cancels in this difference;
it is not removed from the underlying probability law.

The target terminal is the six-element Ferrers hook `(5,1)`. Its two
maximal deletions give precisely C5 and the five-element hook
`Q=(4,1)=(0,1,3,7,1)`. The roles are respectively the C5 root singleton
and Q's long four-chain precursor. An ordinary diamond based at that C4,
with first precursors root and full C4, connects them with all inherited
and both newborn marks transported. Changing any nonroot marking does
not change the C5 singleton local node. Hence it connects all eight Q
long-arm local nodes for each fixed root bit. The two root bits remain
distinct. A diamond preserves the terminal order, so no additional parent
shape can enter this component. These are the complete two target
components, as detailed in the companion intrinsic-incidence proof.

Both parent shapes have trivial unmarked automorphism group. Per target
component there are sixteen complete marked C5 rows and sixteen complete
marked Q rows. Each complete row contains exactly one target ideal; no
row contains both target coordinates. C5 has one natural history and Q
has four. Thus these are eighty raw marked natural-parent rows per target,
not thirty-two equally weighted histories. Complete marked-row counts and
history multiplicities are not interchanged.

Every remaining component coordinate stays in the fixed full problem.
In particular the components reached by other Q ideals are shared global
coordinates at their actual indices, not new independent row-specific
variables. No component ordering is inferred from the labels `0,1`.

## 2. Complete symbolic incident row caps

Use Q labels `0` for the root, `1<2<3` for the long arm, and `4` for
the short leaf. Its complete ideal list is

\[
 0,1,3,7,15,17,19,23,31.
\]

Let its inherited marking be `(r0,r1,r2,r3,r4)` and root bit `i=r0`.
Define only symbolic entries of the existing actual prefix:

- `B_xi(S)` is the complete C4 row after deleting leaf 4, with marking
  `xi=(r0,r1,r2,r3)`; `c_xi=B_xi(15)` and `beta_i=B_xi(1)>0`.
- `J_zeta(T)` is the complete row at the four-element hook `(3,1)` after
  deleting vertex 3, canonically labeled `(0,1,3,1)` with marking
  `zeta=(r0,r1,r2,r4)`.
- `A_chi(S)` is the complete C3 row after deleting both maxima, with
  marking `chi=(r0,r1,r2)`.

These are notation for fixed source-law functions, not requested row
queries or additional evaluated probabilities. No bit of a full J row
is erased without a separate source lemma. The maximal-deletion formula
gives the entire Q proper-potential table:

| Q ideal | Exact potential | Canonical-boundary status of its component |
|---|---|---|
| `0,1,3,7` individually | `B_xi(S) J_zeta(S)/A_chi(S)` | raising role, hence zero at the accepted canonical optimum |
| `15` | `c_xi` | target `k_i`, terminal `(5,1)` |
| `17` | `J_zeta(9)` | neutral role, terminal `(4,1,1)` |
| `19` | `J_zeta(11)` | neutral role, terminal `(4,2)` |
| `23` | `J_zeta(15)` | raising role, hence zero at the accepted canonical optimum |

The first four ideals omit both maxima. Ideals 17,19,23 omit only the
long-arm maximum and become masks 9,11,15 after its deletion. Ideal 15
omits only the leaf and uses the C4 **full** probability. Full ideal 31
is not a proper-potential term; it contributes the full-birth complement.
All eight proper ideals occur once.

For completeness, the defect classification follows directly from Ferrers
cell geometry. Q is Ferrers. Empty birth creates two minima; root birth
creates three atoms; births at 3 and 7 create incomparable chain principal
ideals sharing at least two vertices. None is Ferrers. A birth at 23 has
a five-element nonchain principal ideal, impossible for a rectangle with
five cells. Each has defect exactly one because deleting the newborn
restores Q. The three remaining proper births give exactly the three
Ferrers partitions in the table and have defect zero. Full birth at Q
has a unique maximum and height five; a six-cell Ferrers rectangle is a
chain of height six or a 2-by-3 rectangle of height four. It is therefore
non-Ferrers, and deleting the newborn proves its defect is exactly one.

The complete Q cap is initially

\[
 c_\xi a_i+
 \sum_{S\in\{0,1,3,7,17,19,23\}}
 u_Q(S)\alpha_{c(Q,r,S)}\le1.
 \tag{2}
\]

At the accepted canonical optimum every active component is everywhere
defect-neutral. The five raising roles consequently vanish there. Put
`p_r=J_zeta(9)>0`, `t_r=J_zeta(11)>0`, and retain the original component
lookups `c17(r),c19(r)`. Then the canonical Q cap is exactly

\[
 c_\xi a_i^*+p_r\alpha_{c17(r)}^*
                    +t_r\alpha_{c19(r)}^*\le1.
 \tag{3}
\]

At C5 the five proper ideals are `0,1,3,7,15`. Their potentials are the
five complete C4 entries `B_xi(S)`. Only the singleton birth gives a
Ferrers child; the other four proper roles are raising. The full birth
gives C6 and remains Ferrers. Thus the full unreduced cap retains all
five terms, while its canonical specialization is

\[
 \beta_i a_i^*\le1.
 \tag{4}
\]

Equations (3)–(4) are statements at the accepted canonical point. They
are **not** claims that every primary optimum, or every feasible trial
vector, has zero raising coordinates. The full rows (2) and their C5
counterparts remain the constraints when other coordinates are varied.

## 3. Exact history weights and objective coefficients

Use the RI63 objective convention
`beta_c=sum_j pi_j sum_(S:c(j,S)=c)(d_j(S)-f_j)u_j(S)`.
To avoid confusing that objective vector with the positive singleton
probability `beta_i`, denote the target objective coefficients by
`mathfrak b_i`.

At the C5 target role both proper and full births have zero defect
increment, so its contribution is zero. At the Q target role the proper
increment is zero and the full increment is one, so its contribution is
`-pi_Q(r)c_xi`. Therefore

\[
 \mathfrak b_i=-w_i,\qquad
 w_i=\sum_{r:\,r0=i}\pi_Q(r)c_\xi>0.
 \tag{5}
\]

This sum includes all sixteen complete Q markings for that root bit,
with their actual history masses. It is not a uniform row average.

More explicitly, let `H4_xi>0` be the unchanged marked C4 chain-history
weight. Symbolically it is `2^(-4)` times the product of the four full
chain-prefix births at parent sizes zero through three, with all prefix
marks restricted from xi. For each last-bit value `epsilon`, the C5
history and the leaf-last Q history share this marked C4 prefix. Q has
four linear extensions, corresponding to the short leaf's four possible
positions among the three nonroot long-arm vertices. Adjacent
incomparable swaps are complete accepted marked diamonds, so each
transported history has the same weight, including its newborn factors.
Consequently, for matched complete markings `(xi,epsilon)`,

\[
 \pi_{C5}(\xi,\epsilon)=H4_\xi c_\xi/2,\qquad
 \pi_Q(\xi,\epsilon)=4H4_\xi\beta_i/2,
 \qquad \pi_Qc_\xi=4\pi_{C5}\beta_i.
 \tag{6}
\]

There are eight xi values and two last bits for each root bit. Summing
(6) gives the exact equivalent formulas

\[
 w_i=4\beta_i\sum_{\text{16 C5 markings with root }i}\pi_{C5}
     =4\beta_i\sum_{\text{8 C4 markings with root }i}H4_\xi c_\xi>0.
 \tag{7}
\]

No root-only compression of `H4_xi` or `c_xi` is needed. The history
weights use the unchanged prefix, not the boundary alpha being optimized
at parent size five. They are fixed coefficients of the objective.

## 4. Exact saturation with all other coordinates fixed

Let `I_i` be the complete incident marked-row set for target `k_i`, and
`u_ji=A_(j,k_i)>0` its coefficient. Fix **every** other coordinate at
its actual canonical value. Define its residual row capacity by

\[
 R_j^*=1-\sum_{c\notin\{k_0,k_1\}}A_{jc}\alpha_c^*.
\]

Canonical feasibility makes these residuals nonnegative. Since `I_0`
and `I_1` are disjoint and no other row contains either target, the
remaining feasible pair is precisely the rectangle

\[
 0\le a_i\le L_i,\qquad
 L_i=\min_{j\in I_i}\frac{R_j^*}{u_{ji}}\quad(i=0,1).
 \tag{8}
\]

The target part of the objective is `-w0 a0-w1 a1` with both weights
strictly positive. If `a_i^*<L_i`, increasing just that coordinate by
a sufficiently small positive amount preserves every row cap and every
other coordinate, but strictly improves the primary objective. This
contradicts primary optimality. Hence

\[
 \boxed{\quad a_i^*=L_i,\qquad
 \delta_\kappa=\frac{35}{36}(L_0-L_1).\quad}
 \tag{9}
\]

This proof retains `L_i=0` and `a_i^*=0`; positivity of the objective
weight does not force a positive canonical coordinate. Every minimum
is over a nonempty finite incident set with strictly positive
denominators. At least one incident cap attains each minimum.

Using the canonical specializations (3)–(4), (8) becomes the concrete
fixed-face relation

\[
 L_i=\min\left\{\frac1{\beta_i},\quad
 \min_{r:\,r0=i}
 \frac{1-p_r\alpha_{c17(r)}^*-t_r\alpha_{c19(r)}^*}{c_\xi}
 \right\}.
 \tag{10}
\]

All sixteen Q markings are retained; repeated values may be consequences,
not permission to omit marked subdivisions. The coordinates appearing
in the numerators remain their shared canonical values throughout the
full problem. Formula (10) is not a new optimization over those values.

## 5. Dual and lexicographic consistency

The accepted primary dual has `y>=0` and `s=beta+A^T y>=0`. Its two
target-column conditions are exactly

\[
 s_{k_i}=-w_i+
 \beta_i\sum_{\text{C5 rows with root }i}y_j
 +\sum_{\text{Q rows with root }i}c_\xi y_j\ge0,
 \qquad a_i^*s_{k_i}=0.
 \tag{11}
\]

Every positive dual row is tight. If `a_i^*>0`, the incident dual sum
equals `w_i`; if `a_i^*=0`, only its lower bound by `w_i` is required.
Since `w_i>0`, some incident dual row has positive weight even in the
zero-coordinate case. These are implications of the unchanged full
dual, not newly evaluated dual coefficients or a constructed certificate.

The RI63 canonical vector is the lexicographic minimizer on the primary
optimal face in the original component order. Each positive-coordinate
stage fixes all earlier coordinates and retains the remaining cap matrix,
primary forced-tight rows, and its certified lower-bound dual. No such
stage is dropped or reordered here. Equation (9) follows already from
primary optimality with the other **canonical** coordinates fixed; it
does not replace the sequential tie-break or show how those other
coordinates were selected.

For arbitrary other feasible coordinates, the analogous residual minima
give a conditional optimal pair. They do not guarantee global primary
optimality. If the target coordinates are algebraically eliminated, the
original lexicographic comparison must be applied after reinserting both
minima at their actual indices, not by lexicographically sorting only
the remaining coordinates. The companion synthesis states this exact
full-face reduction without creating an executor.

## 6. The remaining canonical-face comparison

For any proposed bound `delta_kappa>=D_*`, (9) makes the exact remaining
condition

\[
 L_0-L_1\ge\frac{36}{35}D_*.
 \tag{12}
\]

Thus the target contrast is not a free DeltaN or an unspecified graph
edge. It is the difference of two minimum residual capacities of the
fixed canonical face, explicitly (10). In particular a lower bound on
`L0` must control **every** root-zero incident cap; one favorable row
cannot lower-bound a minimum. The root-one minimum still depends on its
own canonical residual capacities.

The derived signs `w_i>0`, `u_ji>0`, and `alpha_c^*>=0` do not compare
those minima. Component index order and defect neutrality do not supply
the comparison either. The neutral components reached by ideals 17 and
19 can consume the Q capacities and are globally coupled to their other
incident rows and the original canonical tie-break. No ordering,
equality, saturation choice, or quantitative value for them is assumed.

Consequently this manuscript proves the complete symbolic capacity and
objective reduction, but not (12) for the RI147 required right-hand side,
nor its joint sensitivity compensation budget. It is not a countermodel
to the fixed law or a theorem that no further analytic comparison can
be proved. All other coordinates and constraints remain in scope; no
alternative primary optimum is substituted for the canonical one.

## 7. Actual source-reading and work boundary

The complete RI149 assignment was read at
`/Volumes/AI_DATA/development/det-review-evidence/ri147-root-scale-review-9dwcmsz2/NATIVE_SUCCESSOR_RESERVATION.json`.
RI63's literal accepted result, local-node/diamond/history definitions,
full objective, primary dual, lexicographic stages, and strict-mixture
definition were reread from sections 1–4 of
`/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`.
The displayed large scientific constants were not extracted, recomputed,
or used in this proof. The current companion incidence proof was jointly
developed by manual reasoning and author-peer message checks; that is
not independent acceptance of either contribution.

Only this fresh assigned Markdown is authored. No scientific certificate
body was decoded, source/helper imported, compiled, parsed as an AST,
probed or run, or numerical/symbolic engine used. No actual component
coefficient, history mass, probability, maximum, scale, H/z or dual value
was evaluated. There was no global graph enumeration, controller,
runtime inventory, card, admission, repository/index/Git change, or
predecessor mutation. The 31/139/20/42 obligations, shared T1 recovery,
other eight connected parents, all five Di conditions, strict endpoints,
old numerical targets and Y=1/4 remain unchanged. RET and measurement
remain separate. No QM, geometry, gravity, empirical or ontological
conclusion follows from this finite canonical-face identity.
