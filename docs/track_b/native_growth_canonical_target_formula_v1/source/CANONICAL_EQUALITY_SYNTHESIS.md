# Canonical root coefficient from the coupled Ferrers rows

The accepted all-Q-row equality, together with the other incident neutral
components and the original canonical ordering, determines the two target
boundary coefficients symbolically. There is no remaining parent-five
optimization coordinate in their formula. This is a manual theorem about
the unchanged accepted finite law. It does not evaluate that formula or
establish the quantitative weighted budget.

The companion NEUTRAL_COMPONENT_INCIDENCE.md proves the complete marked
incidences, including the symmetric parent's two distinct ideal occurrences.
COUPLED_EQUALITY_REDUCTION.md proves the exact closed face, its two cases,
and the minimum used below. This synthesis proves that the original
canonical order selects that minimum and substitutes it into the actual
weighted contrast. The author team is not an independent acceptance body.

## Fixed probabilities and boundary coordinates

For root bit i, keep the unchanged positive size-four probabilities

    p_i = q(C4,root singleton),
    c_i = q(C4,full),
    f_i = q(Q4,short two-chain),
    g_iu = q(Q4,root plus both atoms),  u in {0,1},
    v_i = q(V3,full),
    L_i = 41 p_i,   g_i^- = min(g_i0,g_i1).

Here Q4=(3,1), V3=(2,1), and u is the bit at Q4's distinguished
long-arm atom. Full records are still present in every row. The c_i
root-only identity follows from accepted RI127 RECORD_TRANSPORT equations
(4),(6),(8): nu_xi=theta^3 c_xi and
Delta_xi nu=chi(xi)Delta_1 nu. Positive theta, not a possibly zero contrast,
is divided out. The C4 tip is outside every proper precursor, so its full
complement is independent of that tip bit as well. The companion proves
the f_i and g_iu reductions through the actual marked size-four diamonds.
These are identities of the fixed prefix, not independently tunable inputs.

Name the actual size-five boundary component coordinates

    a_i       terminal (5,1),
    b_i       terminal (4,1,1),
    d_iu      terminal (4,2),
    h_i       terminal (3,2,1).

These names do not renumber the original component vector. Different
components may have equal values or zero values. The two root sectors
have no common coordinate or row in this Ferrers-parent block.

At the actual canonical point, the complete reduced constraints are

    C5: p_i a_i <= 1,
    Q:  c_i a_i + f_i b_i + g_iu d_iu = 1,
    P:  2 L_i b_i + (g_iu g_is/v_i) h_i = 1,
    U:  L_i d_iu + (f_i g_is/v_i) h_i <= 1,
                                                        (1)

for every u,s in {0,1}, with all coordinates nonnegative. P=(3,1,1)
has two full-arm proper ideals, both in b_i; their individual potentials
are L_i. They are added, not identified as one occurrence. U=(3,2) has
neutral full birth, so its row is not asserted tight. Q and P have
raising full births and are noncritical Ferrers parents. Accepted zero
canonical drift and everywhere-neutral activity force their equalities.

This is a boundary statement. In the actual strict law the coefficient is
theta+(35/36) times the relevant boundary coordinate. Every actual proper
and full probability remains positive; no zero boundary complement is
substituted for an actual full probability.

## Why this is a closed primary-face block

Every six-cell terminal named above is Ferrers. Its maximal deletions are
exactly the parent roles in the companion incidence proof. Conversely,
the five-cell Ferrers orders, up to order isomorphism and transposition,
are C5, Q, P, U. Their neutral proper births are exactly the a,b,d,h
roles; their remaining proper births are raising and have canonical
coefficient zero. Full C5 and U births are neutral; full Q and P births
are raising. The companions establish these statements by fixed shapes,
not by a new global graph or defect enumeration.

Start from the actual canonical solution and hold every coordinate
outside this block fixed. Vary only a,b,d,h, preserving (1). Every original
row outside these four parent shapes is unchanged, since none of these
columns has an incidence there. Every row within the block is feasible.
Its boundary expected defect increment remains zero: Q and P have zero
full complement, and C5/U have neutral full births. Thus the complete
history-weighted primary objective is unchanged. No uniform history
weights or unweighted proxy objective are being used.

Consequently every such variation is a genuine variation within the same
global primary optimal face, with all external coordinates fixed. This
is stronger than displaying a nullspace of selected equations. It does
not say that arbitrary primary optima have raising columns zero. The
zero columns are fixed at their already accepted canonical values during
this particular exchange. The complete original lexicographic ordering
is still decisive.

## Original component order within the block

RI63 layout encodes a parent relation by the integer with a bit at
5 label(x)+label(y) for every x<y. It minimizes that relation first,
then the selected-ideal mask, then the transported inside-record mask.
Components are ordered by their least local key. We compare those
literal keys; we do not assume root order, shape size or an invented
ordering of the reduced variables.

First, a minimum relation encoding must be topologically labelled.
Suppose otherwise. Choose the largest label k at an element x having a
descendant y of smaller label h. No vertex with label above k has a
relation into either x or y: such a source would be a higher-labelled
inversion. Swap the labels of x and y. All source rows above k remain
unchanged. In source row k the new outgoing set is the old outgoing set
of y, a proper subset of x's outgoing set; in particular the old x-to-y
bit at target h disappears. No bit is added to that row. Changes in
smaller source rows cannot offset its decrease. The integer therefore
strictly decreases, contradicting minimality. This proves the assertion
without searching permutations or executing layout.

For the four fixed shapes it remains to compare their topological orders.
The following displayed sets give the positions of nonzero relation bits
in their minimum encoding. They are manually derived from the orders,
not decoded canonical indices or evaluated scientific coefficients.

| Parent | Minimum relation bit positions | A minimum vertex order |
|---|---|---|
| Q=(4,1) | 1,2,3,4,7,8,13 | r,a1,a2,a3,b |
| P=(3,1,1) | 1,2,3,4,9,13 | r,a1,b1,b2,a2 |
| U=(3,2) | 1,2,3,4,8,9,13 | r,a1,b,c,a2 |
| C5 | contains bit19 | its unique chain order |

For Q, the isolated short arm can occupy any of the four positions after
the root. Putting it first or second leaves a nonmaximal chain vertex at
label3, hence bit19. Putting it third gives bit14; putting it last gives
the listed maximum bit13 and the unique minimum. For P, modulo its arm
swap, the three interleavings are AABB, ABAB, ABBA. Their highest bits
are respectively19,14,13; ABBA gives the listed minimum. For U, after
the root the five orders are a1,a2,b,c; a1,b,a2,c; a1,b,c,a2;
b,a1,a2,c; b,a1,c,a2. Their highest bits are19,14,13,14,14,
respectively. This exhausts the fixed-shape comparisons. No parent-six
or global component inventory is enumerated.

Comparison from the highest differing bit gives

    E_Q < E_P < E_U < E_C5.                              (2)

The a components have Q and C5 roles, the b components Q and P roles,
the d components Q and U roles, and the h components P and U roles.
Thus their least parent encodings are Q for a,b,d, and P for h.
Q has trivial automorphism and its minimum labels are exactly
(r,a1,a2,a3,b). In these labels the respective ideal masks are

    a:15,  b:17,  d:19.                                 (3)

The marked minima within each component retain root i, and for d retain
the distinguished atom bit u. Additional retained marks can be chosen
zero when finding the least member. Most importantly, (2)-(3) prove
that BOTH a coordinates precede EVERY b,d,h coordinate of this block
in the original vector. Other components may occur between them; all
such coordinates are held fixed in the exchange above. No assertion
about their absolute indices is needed.

## Exact canonical target formula

The companion equality proof gives the minimum feasible a_i on (1):

    a_i,min = [L_i-f_i/2-g_i^-]_+ / (L_i c_i),
    [x]_+ := max(x,0).                                  (4)

This is not a minimum over unknown canonical residual capacities. It is
a closed expression involving only already fixed size-at-most-four rows.
For clarity, its zero and unequal-g cases matter. Set
t_i=g_iu d_iu=1-c_i a_i-f_i b_i. The P equations give
(g_i0-g_i1)h_i=0. If the two g values differ, h_i=0 and
b_i=1/(2L_i); then U bounds t_i by g_i^-/L_i. If they agree,
eliminate h_i using P and the U cap becomes

    L_i c_i a_i+3L_i f_i b_i >= L_i+f_i-g_i,
    0 <= b_i <= min(1/(2L_i),(1-c_i a_i)/f_i).

For f_i<=2L_i, the value (4) is attained with b_i=1/(2L_i).
For equal g and f_i>2L_i, known nonemptiness of the actual block forces
f_i<=2L_i+g_i; a_i=0,b_i=1/f_i is then feasible. The chain cap is
respected because the candidate is no larger than any existing feasible
a_i. The unequal-g case also uses the known nonempty interval, never a
division by g_i0-g_i1. All probabilities divided by are strictly positive.

If an actual canonical a_i were larger than (4), replace its root sector
by a feasible sector attaining (4), keeping every outside coordinate and
the other root sector unchanged. The closed-block proof preserves every
primal constraint and the global primary objective. Equations (2)-(3)
make the first altered coordinate the smaller a_i. The reconstructed
original full vector would be lexicographically smaller, a contradiction.
Therefore the actual canonical coordinates satisfy

    a_i^* = [L_i-f_i/2-g_i^-]_+ / (L_i c_i).              (5)

No alternate primary optimum is substituted for the canonical point.
Formula (5) follows precisely because the original full-vector tie-break
rules out a larger target there. It includes zero targets and equalities
at the positive-part threshold. Remaining freedom in b,d,h need not be
resolved to determine a; its own actual values still obey the later
original lexicographic stages.

## Weighted contrast without unresolved boundary coordinates

Define fixed-prefix expressions

    H_i = L_i-f_i/2-g_i^-,   sigma_i = [H_i]_+/c_i >= 0.

The actual strict-mixture corrections are now exactly

    kappa_i = (35/36) sigma_i/L_i,
    N_i = p_i kappa_i = (35/1476) sigma_i,
    delta_kappa = (35/36)(sigma_0/L_0-sigma_1/L_1).       (6)

All factors, including the restoring theta used elsewhere, remain those
of the same actual law. The integer1476 is36 times41, not a fitted scale.
In particular a_i is zero exactly when H_i<=0 and positive exactly when
H_i>0; this does not decide which branch the unevaluated actual prefix
occupies. Nor does ordering sigma alone order kappa without the L factors.

Substitution into the accepted RI147 identity gives

    q(x) = T_core(x)
              +(35/1476)[sigma_0 k_0(x)-sigma_1 k_1(x)]. (7)

For a proposed adequate b>0, its exact remaining uniform floor test is

    (35/1476)[sigma_0 k_0(x)-sigma_1 k_1(x)]
           >= b D3-T_core(x)  for all x in [0,Z].        (8)

Unlike RI149's version, no unknown parent-five canonical coordinate or
optimization over its face appears in (8). This is the concrete new
elimination result. It is not yet a proof of that quantitative comparison.
The accepted 41/36<k_i(x)<2 supplies the valid, possibly negative bound

    q(x) >= T_core(x)
                +(35/1476)[(41/36)sigma_0-2sigma_1].     (9)

The minus sign on the second root requires its UPPER factor bound.
Zero sigma values cause no exception. Claiming positivity or sufficiency
from (9) without establishing its complete right side would be wrong.

Use (6) consistently in the same correlated Z, chain full complements,
reference sums and envelope factors. The separate adequate v/D3 floor
and BOTH RI147 joint endpoint budgets remain to be proved, or the exact
cleared endpoint polynomials must be established directly. There is no
new assertion about actual rho membership, W, C2/C3 or full H30.

## Scope and review boundary

The new yield is a theorem giving the actual canonical target coefficients
in closed symbolic form and eliminating them from the weighted contrast.
Its load-bearing assumptions are the accepted finite RI63 canonical law,
O01 as separately accepted by the RI149 root adjudication, RI127's complete
record-transport identities, and the literal marked-node, potential and
canonical-key definitions. Exact paths and identities are in the manifests.

No scientific body was decoded; no actual numerical coefficient,
probability, history, maximum, scale, H or z was evaluated; no engine,
global graph enumerator, source/helper import/compile/AST/probe/run,
runtime/controller/card/admission, repository/index/Git or predecessor
mutation occurred. Fixed-shape manual relation-key comparison is not an
execution of the global layout or component constructor.

P2/P3, numerical Y=1/4, all31/139/20/42 obligations, the shared T1 recovery,
the other eight connected parents, all five Di systems and each ideal
multiplicity remain unchanged. RET is paused; measurement stays separate.
No quantum reconstruction, geometry, mass/gravity, all-size or empirical
claim is promoted. This packet stops for nonauthor review and root
adjudication; it does not assign or authorize another obligation.
