# RI172 complete finite layer nonimplication theorem

30 September 2026. Source-only author proof, pending independent root review.
This note resolves the assigned comparison-class question. It does not decide
the desired inequality at the unchanged actual coefficient vector.

## Result and exact comparison class

The complete size-four row, ratio, coefficient-floor, complement-floor and
height conditions **do not imply** the reverse bound

    D_minus <= 213d,                                      (1)

even when every global component outside the eight core B components is
held at its original accepted value, every marked parent is retained, and
the original root-only value patterns are preserved. Indeed D_minus/d is
unbounded within that declared finite-layer class with d>0.

This is stronger than RI166's two-row relaxation example. The present
construction preserves every row and ratio at the entire size-four layer,
because RI168 exhaustively established the eight changed components' global
incidence. It is still **not a counterexample to the actual fixed law**:
the constructed coefficient vectors differ from that law. Nor is it a
counterexample within a class additionally requiring all its later
canonical, polynomial, maximum-derived or H30 constraints.

Here is the precise class to which the theorem applies. Keep the accepted
RI36/RI41 prefix through parent size three, its asymmetric seed, and its
maximal-deletion potentials. For every size-four proper slot, use the same
global ratio-component convention and probabilities

    q_j(S)=alpha_component(j,S)*u_j(S).

Require all of the following simultaneously:

- every global alpha is at least1/8;
- every complete marked row is normalized, with its full complement at
  least beta=33901019/474368400;
- every complete marked row has total height-raising probability strictly
  below H=19/40;
- every raw marked diamond, locality and marked equivariance condition is
  retained, with all distinct labeled ideal occurrences and newborn marks.

Thus all branch probabilities are strictly positive. The full complement is
the complete row's residual, not an additional independent parameter. The
floor conditions do not require their minima to be attained at the same
coordinates as in the actual vector; the height condition does not require
the original exact maximum value. Exact-vector membership, a particular
coefficient lattice and higher-layer equations are not premises of this
comparison class. No such condition is silently advertised as preserved.

## Original data used to select the path

Use superscript orig, when needed, for quantities of the original unchanged
accepted law. Its complete C4 rows are

    (w,p_i,s_i,b_i,c_i),       w+p_i+s_i+b_i+c_i=1,
    i=0,1,                  d=b_0-b_1>0.                 (2)

RI168 inherits b/c root-only values from RI127 and then derives root-only
s by complete normalization. These actual value equalities do not merge
the two singleton, four pair or eight triple graph components. All other
marks remain in their corresponding full rows.

Define

    x=p_1-p_0,        y=s_1-s_0,
    D_minus=x_+ + y_+,
    U_i=w+p_i+s_i,
    L=H-beta>0,       A=41/44,       m=A/8.                (3)

Positivity of L follows already from any original C4 complement satisfying
beta<=c_i<H. The m here is the core-probability floor A/8, not the smaller
proper-slot floor e/8, where e=1/44.

The complete alternative V/T rows and their height bounds, proved in RI168,
give

    0<p_i<L/41,       0<s_i<L/82.                        (4)

No relative order of p_0,p_1 or s_0,s_1 is assumed. No root-bit flip is a
symmetry of the asymmetric smaller prefix.

## Positive numerator from the original sensitivity theorem

The path requires D_minus>0, not just nonnegative probabilities. This follows
from the **original accepted sensitivity premises**, not from a guessed
ordering of component indices or seed values.

RI147's complete actual-law factorization and RI157's original-law sign
bounds supply

    v_orig = theta_orig * (d_1 H_1 + d_3 H_3 + d H_7) > 0,
    theta_orig>0,       H_1<0, H_3<0, H_7<0,
    d_1=p_0-p_1=-x,    d_3=s_0-s_1=-y,    d>0.           (5)

These are RI147 COMPONENT_CONTRASTS section4 equation(6) and RI157
CORRELATED_CONTRAST_BOUND sections3--4. The latter proves all three secant
signs and explicitly obtains the positive numerator consequence. The empty
contrast is zero by strict empty locality; its slot has not been removed
from the underlying complete rows.

For a direct manual proof, suppose D_minus=0. Both x and y are then at
most zero, so d_1,d_3 are nonnegative. The first two summands in(5) are
nonpositive and the last is strictly negative. Multiplying by positive
theta_orig gives v_orig<0, a contradiction. Therefore

    D_minus>0.                                           (6)

This argument allows either x or y to vanish and selects neither positive
disjunct individually. It never divides by x, y or a possibly zero contrast.

Crucially, (5) is used **only at the original starting point** to establish
the fixed fact(6). We do not assume v, theta, the secants, canonical
selection or the RI115--122 identities are unchanged or even defined as
the original higher-law objects at the altered vectors. Since p_i and s_i
are left unchanged by the finite-layer path, (6) then remains true by
elementary equality of those four numbers, not by a new sensitivity theorem.

## Diagonal endpoint and complete global preservation

The companion [FULL_LAYER_PATH.md](FULL_LAYER_PATH.md) proves every step
of the path. Its core construction is summarized here to make the theorem
self-contained.

For fixed other coefficients, each C4 core probability is admissible exactly
under the size-four floor/complement/height conditions

    b_i>=m,       1-U_i-H < b_i <= 1-U_i-beta.             (7)

C4's only height-raising slot is its full ideal. Its proper initial triple
birth preserves height, so its full height mass equals c_i=1-U_i-b_i.
These facts account for both the strict lower and weak upper endpoint in(7).

Because w is common and each p_i+s_i lies strictly between0 and3L/82,

    |U_1-U_0|<3L/82<L.                                  (8)

Let U_max=max(U_0,U_1) and set

    b_star = min_i(1-U_i-beta) = 1-U_max-beta,
    c_i_star = 1-U_i-b_star = beta+U_max-U_i.              (9)

Original feasibility gives 1-U_i-beta>=b_i>=m for both roots, hence
b_star>=m. Equations(8)--(9) give beta<=c_i_star<H for both roots.
Thus b_star is a common admissible diagonal endpoint, including any equality
at its coefficient floor or complement floor. Its height upper bound is
strict. No numerical choice of a frozen coefficient was made.

For every real t in[0,1] define, in every one of the four core components
with root i,

    b_i(t)=(1-t)b_star+t b_i,
    alpha_B(i,u,v)(t)=b_i(t)/A,       u,v in{0,1}.          (10)

Keep every other global component coefficient fixed, and determine every
full complement by its complete row sum. RI168 proves that each changed
component appears only in C4's initial-triple slot with those retained stem
marks. Across the eight components, there are exactly16 naturally labeled
marked C4 rows, one changed ideal per row, and32 equal-precursor raw diamonds.
No non-C4 row has a changed component. Arbitrary isomorphic labelings are
handled by the same marked quotient, not additional coefficient choices.

The C4 complements are consequently

    c_i(t)=(1-t)c_i_star+t c_i.                           (11)

Both endpoints satisfy beta<=c_i<H, so every convex combination does too.
Likewise alpha_B(t)>=1/8. All other coefficient floors, row sums,
complement floors and height bounds are unchanged. In every affected raw
diamond the same core probability occurs on both sides of the retained
equal-precursor loop; the lower prefix is fixed. All other ratio equations
are untouched. Global component sharing, locality, equivariance, both
newborn bits and all labeled ideal multiplicities are preserved. The full
passive maps still multiply the entire retained unnormalized kernel by q/2.

This is a proof covering **all** size-four occurrences, not an independent
choice of the two displayed C4 rows. In particular the alternative V/T rows,
their shared z column and the other global coefficients remain exactly
unchanged. No later-layer potential is being claimed unchanged.

## Explicit violating parameter and unbounded ratio

Equations(10) give

    d(t)=b_0(t)-b_1(t)=t d,
    D_minus(t)=D_minus>0.                                (12)

For t>0 the strict core order survives. The diagonal endpoint t=0 is used
only to construct the path; it is not a counterexample requiring d>0.
Choose the exact symbolic parameter

    t_star = min(1/2, D_minus/(426d)).                    (13)

Every denominator is positive by(2),(6), and 0<t_star<=1/2. Therefore

    213d(t_star) = 213t_star d
                 <= D_minus/2 < D_minus.                (14)

This is a member of the entire declared finite-layer class that strictly
violates(1), while retaining the unchanged values of every other component.
It is an analytic existence witness, not a decoded numerical vector, a new
fixture, an edit to the actual certificate, or an executed countermodel.

More generally, for each fixed finite M>0, the parameter
min(1/2,D_minus/(2Md)) gives D_minus/d(t)>M. Equivalently this ratio tends
to positive infinity as t decreases to0 through positive values. Thus no
finite uniform relative-contrast constant is imposed by these finite-layer
conditions alone, even with the other component coordinates fixed here.
This corollary uses the same path, not an additional programme or gate.

The RI168 resource identities still hold along the path. Their K is constant
because the V/T rows and all their summands are unchanged. If C(t) denotes
c_1(t)-c_0(t), complete normalization gives

    x+y=d(t)-C(t),       41x-82y=K.                      (15)

The chain-complement contrast adjusts consistently; it was never held
independently fixed. At t_star at least one of RI168's three corridor
inequalities fails, by its exact equivalence with(1). No claim is needed
about which inequality fails or the sign of C(t).

## What the theorem does and does not exclude

The finite-layer implication route is now rejected in the precise class
defined above. This is a theorem about the declared mathematics. It does
not reject the actual reverse bound; that statement still concerns one
fixed vector, not every member of the comparison class.

| Premise or quantity | Role in this proof | Preservation claim |
|---|---|---|
| Actual finite-law existence and all complete row margins | Provides the starting point | The declared inequalities hold along the entire path |
| RI168 full B-component incidence | Justifies every global occurrence affected | All raw occurrences and graph identities retained |
| Original RI127 b/c patterns and normalization-derived s pattern | Selects root-only starting data | Those value patterns are preserved by construction, without component merging |
| Original v>0, secant signs and theta>0 | Establishes D_minus>0 once | No higher-law identity or v sign claimed at altered vectors |
| Frozen actual109-vector | Selects the original law | Not preserved for t<1; no certificate bytes changed |
| Exact attained coefficient/complement minima or exact maximum height value | Not required by the declared class | Not claimed; only its specified floors and strict ceiling are preserved |
| Parent-five canonical selection, RI115--122 identities, same-law M5/M6/rho | Additional actual-law structure | Not preserved or evaluated |
| Actual capacity, joint q/v, W/C2/C3 and shared H30 | Separate continuation questions | Not settled |

Any proof of the actual reverse bound now needs a premise that constrains
the *selection* of the actual core coefficients beyond these complete
finite-layer conditions. The frozen vector itself, or a proved selection
property from additional same-law structure, could supply such information;
this note proves neither. An unverified grid rule cannot be inserted as
that premise. A proposed later-law restriction must actually be shown to
exclude the constructed path, not merely named as though it already does.

Changing a size-four row changes inputs to later deletion potentials and
their canonical problems. Reusing the old later tables or theta unchanged
would define no proved same-law continuation. Conversely, satisfying all
size-four conditions does not establish that these alternative prefixes
retain the original higher-layer laws or satisfy H30. Failure of the
reverse bound, which was only a way to reject a sufficient envelope,
does not prove that envelope or the original continuation problem feasible.

## Sources and stopping boundary

The authenticated RI172 assignment selects this comparison-class question;
RI168's root decision accepts its complete incidence and exact corridor but
not this new candidate. The full RI168 proof and the primary RI36/RI41,
RI127, RI147 and RI157 mathematical sources are selected in the current
source manifests. The original sensitivity source was read literally and
its argument above reconstructed manually; no scientific body was decoded.

[DEPENDENCY_NOTES.md](DEPENDENCY_NOTES.md) records exact inherited identities
and explicit provenance stopping boundaries. Administrative byte checks
are not numerical or mathematical acceptance. This proof and its companion
remain author work until root's independent adjudication.

All31/139/20/42 obligations, P2/P3, numerical Y=1/4, shared T1, other eight
parents, all five Di, strict endpoints and labeled multiplicities remain
unchanged in the actual programme. The actual vector, prior manuscripts,
reviews and failures were not modified. RI170 measurement and RI171 native
qualification stay separately owned. RET alone remains paused. No quantum,
geometry, mass/gravity or empirical promotion follows. Root owns independent
review, the next justified assignment, repository/index/Git and publication.
This packet stops at its sealed proof handoff.
