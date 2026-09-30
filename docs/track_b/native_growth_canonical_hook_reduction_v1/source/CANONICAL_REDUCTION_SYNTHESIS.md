# Canonical hook coefficient reduction

The complete singleton-hook incidence yields a stronger conclusion than a
sign or scale bound: each of the two target boundary coefficients is exactly
the least normalized residual capacity of its incident rows, with every
other coefficient held at its actual value. The whole primary problem can
therefore eliminate these two coordinates exactly. The original canonical
lexicographic order must still be applied to the reconstructed full vector.

This is a manual conditional theorem about the accepted finite optimization,
not an evaluation of its canonical solution. It does not yet determine the
sign of the root coefficient contrast or discharge the RI147 sensitivity
budget. The new remaining premise is a relation on a specific reduced
canonical face, stated below. Author review is not independent acceptance.

## Complete incidence and the negative objective coefficients

HOOK_INCIDENCE.md proves that terminal hook (5,1) has precisely two ratio
components, one for each root bit i. Each consists of one C5 singleton
local node and eight marked long-arm nodes of Q=(4,1). The ordinary C4
full/singleton diamond connects all eight nodes to that singleton; every
terminal presentation is one of these two maximal-deletion roles. No
additional marked subdivision or connection to another terminal is omitted.

Write p_i=B_i(1)>0 for the actual C4 singleton probability, and c_xi>0 for
its complete full probability with four-chain marking xi. The target
component occurs once in every C5 row with root i, with potential p_i,
and once in every Q row with root i, with potential c_xi. There are sixteen
marked row classes of each shape per root bit. The Q classes have four
natural histories and the chain classes one. Distinct ideal occurrences
and both newborn marks remain counted. No row contains both target columns.

Let pi_C and pi_Q be the accepted history masses of those complete marked
row classes. In a transported comparison with long-arm marking xi and
last-born mark epsilon, the full diamond and fair-mark factors give

    pi_C(xi,epsilon) = H4_xi c_xi/2,
    pi_Q(xi,epsilon) = 2 H4_xi p_i,
    pi_Q(xi,epsilon)c_xi = 4 pi_C(xi,epsilon)p_i.

H4_xi is the fixed four-birth marked history product, not a uniform class
weight. The Q path multiplicity four is indispensable. It is derived by
interleaving the short leaf with the three ordered nonroot long-arm events;
all transported paths have equal weight by the inherited marked diamonds.

Both target births are defect-neutral. Full C5 birth is neutral, whereas
full Q birth raises the defect by one. Thus the target objective columns
are strictly negative, with exact unevaluated weights

    beta_obj,target_i = -w_i,
    w_i = sum_(Q rows root i) pi_Q c_xi
        = 4 p_i sum_(C5 rows root i) pi_C
        = 4 p_i sum_(eight xi with root i) H4_xi c_xi > 0.   (1)

The companion incidence and face notes justify the terminal classification,
all row coefficients and these complete sums. Neither a coefficient value
nor a history mass has been calculated.

## Exact elimination with every other coordinate retained

Use RI63's original finite boundary problem

    minimize B5 + beta_obj^T alpha
    subject to alpha>=0 and A alpha<=1.

The target coordinates have their actual original component indices
mathfrak_c_0 and mathfrak_c_1. Call their values a_0,a_1, and call the
remaining vector z. This notation does not change or sort the indices.
For every original row j, define

    L_j(z)=sum_(k not in {mathfrak_c_0,mathfrak_c_1}) A_jk z_k,
    D_rest={z>=0: L_j(z)<=1 for every original row j}.

Let I_i be the complete incident row set of target i and u_ji its positive
coefficient, p_i or c_xi according to the parent shape. Define

    T_i(z)=min_(j in I_i) [1-L_j(z)]/u_ji.                  (2)

These are nonempty finite minima. Their denominators are positive, and
T_i>=0 on D_rest. Every proper component occurs in some row with a positive
coefficient, so row caps bound every remaining coordinate. D_rest is a
nonempty compact polytope; z=0 is feasible. No table or vertex enumeration
is needed for these statements.

Because I_0 and I_1 are disjoint and the target columns vanish outside them,
the complete feasible slice at any fixed z is exactly

    0<=a_0<=T_0(z),  0<=a_1<=T_1(z).                     (3)

Rows outside I_0 union I_1 remain present in D_rest. Conversely any z in
D_rest has a feasible extension by taking both target coordinates zero.
Thus D_rest is the exact projection, not a relaxation that drops other rows.

Equation (1) makes the objective strictly decrease in either target
coordinate when all others are fixed. Its unique minimizing pair on (3) is

    a_i=T_i(z), i=0,1.                                   (4)

This is also a direct exchange proof. If a_i<T_i at a primary optimum,
increase only that coordinate by a sufficiently small positive amount.
Every incident cap remains satisfied, all nonincident rows and the other
target coordinate are unchanged, and the objective strictly decreases.
That contradiction proves (4). The proof includes a_i=T_i=0 and tied
minimizing rows. No division by a_i, by a slack, or by a contrast is used.

Consequently the full primary problem is exactly equivalent to

    minimize F(z)=B5+sum_remaining beta_obj,k z_k
                         -w_0 T_0(z)-w_1 T_1(z)
    over z in D_rest.                                    (5)

Each T_i is the minimum of finitely many affine functions, hence concave;
F is convex and piecewise affine. The equivalence is more important than
this regularity statement: every original primary minimizer satisfies (4),
and every minimizer of (5) lifts to an original primary minimizer. This is
a symbolic elimination theorem, not a new numerical solver or executor.

## The canonical tie-break is not removed

Let Phi(z) be the original full coefficient vector with a_i=T_i(z)
inserted at the original indices mathfrak_c_i and every other entry equal
to its original coordinate in z. The actual canonical solution is exactly

    Phi(z_star), where z_star minimizes F on D_rest
    and Phi(z_star) is lexicographically least among these full vectors. (6)

The proof is the bijection between primary minimizers just established,
followed by the unchanged definition of the canonical tie-break. It would
be incorrect to replace (6) by a lexicographic minimization of z alone.
An eliminated target coordinate can occur earlier than a retained one;
its value T_i(z) is then part of an earlier canonical equality. Every
earlier-coordinate restriction and all primary forced-tight rows remain.

At this actual canonical point, RI63's accepted everywhere-neutral active
component theorem permits simplification of the incident row caps. C5 has
only its singleton neutral proper birth. Q has exactly three neutral proper
births, at masks15,17,19, with terminals (5,1), (4,1,1), and (4,2).
All other proper contributions in these rows have zero canonical
coefficient. Thus (2) specializes at z_star to

    T_i(z_star)=min{
      1/p_i,
      min_(all Q markings with root i)
        [1-u17 alpha_component17-u19 alpha_component19]/c_xi }.
                                                               (7)

The other two component coordinates in (7) are still their actual fixed
canonical coordinates with all permitted mark dependence retained. The
full uncollapsed definition (2) remains in force away from the canonical
point. In particular this note does not set raising coordinates to zero
at every arbitrary primary optimum or every z in D_rest.

## A dual-face constraint and its zero case

For any feasible primary dual y>=0, the two reduced costs are

    s_i=-w_i+sum_(j in I_i) y_j u_ji >=0.                  (8)

At a primal-dual optimum, complementarity gives a_i s_i=0 and
y_j[1-L_j(z)-u_ji a_i]=0 for incident rows. Since w_i>0, (8) implies
at least one positive y_j in I_i, even if a_i=0. Every such row attains
the minimum in (2). If a_i>0, the weighted dual sum equals w_i; if a_i=0,
it can exceed w_i. These are exact constraints, not evaluated dual values.

They explain why a bare exchange of one root coefficient for the other
does not establish their ordering: releasing capacity in I_1 does not
release a row in the disjoint I_0. A coupled exchange would have to move
other coordinates and preserve all their incident caps, primary-face
equalities, and earlier canonical restrictions. The explicit remaining
coordinates in (7), not a component index or neutrality alone, control
that possibility. No counterexample with freely assigned coefficients is
substituted for the actual fixed canonical problem.

## What this resolves in the weighted-margin question

The actual strict-mixture corrections are now exactly

    kappa_i=(35/36)T_i(z_star),
    N_i=(35/36)p_i T_i(z_star),
    delta_kappa=(35/36)[T_0(z_star)-T_1(z_star)].            (9)

Retain RI147's complete C4 contrast polynomial T_core(x) and positive
singleton factors k_i(x). Its exact q identity becomes

    q(x)=T_core(x)+(35/36)[p_0 T_0(z_star) k_0(x)
                                     -p_1 T_1(z_star) k_1(x)].   (10)

This substitution preserves the beta/N/omega correlations; p_i here is
RI147's held beta_i, not an objective coefficient. For any proposed
positive ratio floor b, the precise remaining q comparison is

    (35/36)[p_0 T_0(z_star) k_0(x)-p_1 T_1(z_star) k_1(x)]
      >= b D3-T_core(x) for every x in [0,Z].              (11)

Z, the reference sums, and the weighted envelope must remain the actual
correlated expressions after the same substitution (9). They cannot be
held at unrelated favorable values. The separate C4 comparison supplying
an adequate lower bound for v/D3 is still required, as are both endpoint
budgets in RI147. A bound only on the unweighted difference T_0-T_1 would
not automatically suffice for (11).

The incidence, negative objective columns, exact saturation and canonical
elimination have been derived. The values and relative residual capacities
at z_star, or an inequality on its original primary/lexicographic face
strong enough for (11) and the joint budget, have not. This is a precise
remaining actual canonical-face relation, not a claim of impossibility.
No actual sign, rho membership, local margin or full H30 result is promoted.

## Scope and source boundary

Load-bearing literal definitions are RI63 COMPLETION.md sections2–4 and
check.py history_probability, build_problem, and check_certificate_core;
RI38 supplies the complete marked diamonds and deletion potentials. Current
companion notes prove the complete incidence and optimization steps; accepted
RI147 supplies the q identity and weighted-budget definitions. Exact paths,
identities and review boundaries are in the source manifests.

All algebra and graph reasoning were manual. No scientific body, canonical
coefficient, maximum, scale, H or z was evaluated; no engine, graph enumerator,
subject/helper import/compile/AST/probe/run, executor, controller or admission
was used. No predecessor or repository/index/Git edit occurred. The numerical
P2/P3 and Y=1/4, all31/139/20/42 obligations, shared T1 recovery, other eight
connected parents and all five Di systems remain unchanged. RET stays paused;
measurement and isolated work remain separate. No full QM, geometry, gravity,
all-size or empirical conclusion follows. Stop for nonauthor review and root
adjudication; this note assigns no successor.
