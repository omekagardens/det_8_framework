# RI168 — complete incident rows and the remaining contrast corridor

30 September 2026. Source-only manual mathematics under the RI168 assignment.
This is an author result awaiting independent root adjudication. No graph,
solver, scientific JSON, fixed109-vector or target/helper was executed or
decoded. All probabilities refer to the unchanged actual law, not a new
choice of its coefficients.

## Result

The companion [INCIDENCE.md](INCIDENCE.md) exhausts the parent-row appearances
of the six selected C4 components. The singleton appears in C4 and V4; the
initial pair appears in C4 and both distinct arms of T4; the initial triple
appears only in C4. The full marked families contain 2, 4 and 8 graph
components, respectively. This is a complete local incidence theorem, not
a full enumeration or numerical reconstruction of the 109-component law.

The alternative rows give a shared probability z_i, exact resource identities
and a necessary-and-sufficient three-inequality corridor for the desired
reverse bound. The values in that corridor have not been bounded relative
to d7. The outcome is therefore **complete target incidence and an exact
residual cross-row constraint**, not a proved reverse bound, a full-law
counterexample, or a new numerical qualification.

## 1. Premises and the distinction between components and values

Use the RI36/RI41 fixed prefix, with

    e = 1/44,       a = 41/44,
    c_seed = 1/5,
    f_seed(0) = 1/6,       f_seed(1) = 1/3,
    h_0 = 19/30,          h_1 = 7/15.

Here a denotes the full C3 probability, not the older singleton seed2/3.
Put phi_i=e*h_i/f_seed(i) and psi_i=1-2e-2phi_i. These are respectively
one root-plus-leaf probability and the full probability of the three-fork.
Both distinct fork leaf ideals are included in psi_i. All are positive.

For every proper slot use the **same global RI41 coefficient**

    q_P(S) = alpha_[P,S,records|S] * u_P(S),

where the bracket means its entire ratio-graph component, not a row-local
coordinate. Each alpha is at least1/8 in the accepted fixed finite law.
The positive maximal-deletion potential u is RI41 equation(4). No symbol
below permits the same component to take different values at different
row occurrences. Its probability can differ only by its prescribed potential.

Write C4 as r<a1<a2<a3. Its complete marked row initially has the form

    w + p_i + s_(i,u) + b_(i,u,v) + c_(i,u,v,t) = 1,          (1)

with i,u,v,t the four marks. Component locality proves w record-blind and
p_i root-only, but by itself does not discard u from s or u,v from b.
All four marks remain part of the marked parent.

There is, however, an additional accepted actual-law premise: RI127
RECORD_TRANSPORT section3 equation(9) proves b_(i,u,v)=b_i. Equations(4),
(6),(8) there give c_(i,u,v,t)=c_i, using theta>0 and the accepted maximal-bit
transport, without dividing by a possibly zero complement contrast. These
are consequences of the previously accepted RI115/RI122 patterns, not
fresh incidence consequences. RI151 section6 explicitly preserves the
complement implication. Inserting these facts and p_i into(1) forces

    s_(i,u) = s_i,      w+p_i+s_i+b_i+c_i = 1.                (2)

Thus distinct marked graph components can have equal values in the actual
fixed law. They are not merged, and their labeled row occurrences are not
removed. No equality between the two root sectors is inferred. In particular,
f_seed(0)!=f_seed(1); no bit-flip symmetry is available.

Retain the accepted RI41 bounds

    beta = 33901019/474368400,
    full complement >= beta > 1/14,
    total height-raising probability < H = 19/40.            (3)

These are inherited printed finite-law bounds, not this sitting's evaluation
of the frozen certificate. RI166's d=b_0-b_1>0 and all other accepted scale
and contrast premises are unchanged.

## 2. Complete incident rows, with the shared column retained

Use V4 with relations r<a1<a2 and r<x, and T4 with relations r<a1<a2,
a1<x. Their masks use the vertex order (r,a1,a2,x). The complete potentials
and component proofs are in INCIDENCE. Name their actual proper probabilities
as follows; these names are aliases of global components, not free variables.

| Parent | Mask | Probability | Potential |
|---|---:|---|---|
| C4 | 0 | w | e |
| C4 | 1 | p_i | e |
| C4 | 3 | s_i | e |
| C4 | 7 | b_i | a |
| V4 | 0 | w_V | e^2/c_seed |
| V4 | 1 | ell_i | e^2/f_seed(i) |
| V4 | 3 | z_i | e^2/f_seed(i) |
| V4 | 7 | 41p_i | a |
| V4 | 9 | f_i | phi_i |
| V4 | 11 | g_(i,u) | psi_i |
| T4 | 0 | w_T | e^2/c_seed |
| T4 | 1 | z_i | e^2/f_seed(i) |
| T4 | 3 | t_(i,u) | e^2/h_i |
| T4 | 7 | 41s_i | a |
| T4 | 11 | 41s_i | a |

The f_i in this table is V4's short-arm probability, not f_seed(i).
Likewise t_(i,u) is a probability, not a mark or an adjustable correction.
V4's long-arm factor41 and T4's two factors41 follow from the C3
full/proper ratio a/e, not from a new coefficient choice. The two T4 arms
are distinct labeled ideals even when their marks coincide.

The V4-mask3/T4-mask1 C3 diamond has precursor pair(1,3). Its two old
probabilities are e, so it equates the new probabilities. Varying the
nonroot inherited and newborn bits proves exactly the shared z_i shown
above. The potentials also agree. This column must not be duplicated into
independent V/T variables. It is not one of the six selected components.

RI151 section6 proves V4's f_i is root-only and g_(i,u) may retain its
distinguished atom bit. That section also identifies another occurrence:

    q_D4(selected C2 with root i, atom u)
        = phi_i*g_(i,u)/psi_i.                              (4)

Equation(4) remains binding wherever that other parent enters the global
law. No independent D4 coefficient is introduced here. All other aliases
likewise retain their original global component wherever it reappears;
this incident-sector reduction is not a claim to close all their other rows.

Full complements are denoted v_(i,u) for V4 and h_(i,u) for T4. These
letters do not denote the older contrast V1-V0 or the seed h_i. The complete
rows, for every u and every forgotten-tip assignment, are exactly

    V: w_V + ell_i + z_i + 41p_i + f_i + g_(i,u) + v_(i,u) = 1,
    T: w_T + z_i + t_(i,u) + 82s_i + h_(i,u) = 1.            (5)

They include six and five proper occurrences, respectively, and one full
occurrence each. Positivity of all summands, bounds(3), and their global
coefficient definitions remain required. No full complement is a separately
selectable coefficient. No record averaging is used.

## 3. Height budgets and same-column interval coupling

V4 and T4 both have height3. Only V4's long C3 proper ideal and its full
ideal raise that height. Both complete C3 arms of T4, plus its full ideal,
raise height. Consequently, for every i,u,

    41p_i + v_(i,u) < H,
    82s_i + h_(i,u) < H.                                   (6)

These are total raising probabilities, not just full-birth probabilities.
Together with(3), they give the actual incident-sector bounds

    e/8 <= p_i < (H-beta)/41,
    e/8 <= s_i < (H-beta)/82.                               (7)

The upper bounds use the full accepted beta rather than replacing it by
1/14. They are absolute bounds; d has not been bounded away from zero by
them. They must not be described as a d-relative estimate.

For an exact expression of the shared-column constraint, put

    A_(i,u) = w_V + ell_i + f_i + g_(i,u),
    B_(i,u) = w_T + t_(i,u).

Then equations(5) read

    z_i = 1-41p_i-A_(i,u)-v_(i,u)
        = 1-82s_i-B_(i,u)-h_(i,u).                          (8)

In particular the same z_i, for both values of u, satisfies

    z_i >= e^2/[8 f_seed(i)],
    z_i > 21/40 - A_(i,u),
    z_i > 21/40 - B_(i,u),
    z_i <= 1-beta-41p_i-A_(i,u),
    z_i <= 1-beta-82s_i-B_(i,u).                            (9)

All four u-indexed bounds hold simultaneously. The first lower bound is
root-asymmetric; it does not equate the two z values. Other proper-slot
floors are their table potentials divided by8, with the same global
coefficients in every occurrence. Equations(8), not merely separate row
inequalities, retain the cross-row equality.

## 4. Exact contrast corridor supplied by the alternative rows

Subtract the two equal expressions in(8). Define

    R_(i,u) = B_(i,u)-A_(i,u)+h_(i,u)-v_(i,u).

Then

    R_(i,u) = 41p_i-82s_i.                                 (10)

Thus R_(i,0)=R_(i,1). More explicitly, (5) gives g_(i,u)+v_(i,u)
independent of u, and t_(i,u)+h_(i,u) independent of u. No individual
equality of the two g, t or full-complement values is asserted.

Write Delta for root1 minus root0 with the same u, and define

    K = Delta R_(i,u)
      = Delta[t_(i,u)-ell_i-f_i-g_(i,u)+h_(i,u)-v_(i,u)],
    C = c_1-c_0,
    x = p_1-p_0,       y = s_1-s_0,       d = b_0-b_1 > 0.  (11)

K is independent of the chosen u. The record-blind w_V,w_T disappear
from its contrast; z_i was eliminated because it is a shared column,
not because its root contrast was set to zero. Equations(2),(10) give

    x+y = d-C,       41x-82y = K,
    x = 2(d-C)/3 + K/123,
    y =   (d-C)/3 - K/123.                                (12)

This second, differently weighted equation is the new cross-row content
beyond RI166's C4 normalization. It expresses the missing comparison in
terms of the *other global components and the actual alternative full
complements*, rather than introducing independently chosen p/s rows.

For real x,y, x_++y_+=max(0,x,y,x+y). Since213d>0, the desired reverse
bound is therefore equivalent to the following three inequalities:

    x_+ + y_+ <= 213d
      iff
    C >= -212d,
    -26158d - 41C <= K <= 26117d + 82C.                    (13)

Indeed x+y<=213d is the first inequality. Multiplying x<=213d by123
gives K<=26117d+82C; multiplying y<=213d gives the lower bound. No
sign is assigned to K or C, and no potentially vanishing contrast is
divided out. All endpoints in(13) are weak, while the inherited height
and final comparison margins remain strict. This is an exact equivalence
for the actual incident rows, not a sufficient envelope accidentally
promoted to the original all-parent continuation criterion.

## 5. The precise unresolved obstruction

The full target-component incidence contributes no alternative-parent
occurrence of b_i. For a mask7 component the terminal is a C3 stem with
two incomparable caps; deleting either cap leaves C4, and there is no
third maximum. Its diamonds are the retained equal-precursor loops. Thus
no additional row containing that *same core component* has been omitted
which could furnish a second direct resource comparison with d.

The exact remaining task is to establish, for the unchanged actual global
coefficient vector and its full complements, the corridor(13), or an
independently sufficient bound implying it. The additional rows presently
supply(7)--(10) and the definitions of K; they do not in this proof supply
a d-relative estimate of C or K. The dependencies of ell,f,g,t and their
full complements on their other global rows must not be replaced by free
choices. Nor does the absence of a core occurrence elsewhere prove those
remaining global constraints cannot imply the corridor.

This is a **localized proof gap**, not a nonimplication theorem for the full
RI41 law. No modified coefficient vector, reduced numerical witness or
all-mark perturbation is offered. In particular RI166's reduced family is
not certified to satisfy(5), all other parent-four rows, the actual frozen
109 coefficients, or the later same-law canonical/global-scale constraints.
It remains exactly the reduced counterexample previously adjudicated.

If(13) were proved, RI157's accepted strict comparison would reject only
its sufficient envelope. Failure of(13), or failure to prove it, would not
establish feasibility of the original coupled programme. This packet proves
neither outcome. It supplies a complete finite incidence theorem and the
explicit residual relation on which this particular reverse-bound route
depends; it stops for root review.

## 6. Unchanged scope and provenance

The actual109-vector and final-witness grid remain unread/unverified in
this sitting. No grid divisibility, common-scale replacement, new witness,
mark-flip symmetry, physical claim or execution permission is inferred.
Actual capacity, the joint q/v budget, global M6/rho, the same-law M5 and
canonical construction, W/C2/C3, shared H30 and the full coupled correction
system remain separate. Preserve P2/P3, Y=1/4, all31/139/20/42 obligations,
the identical shared T1 quantities, other eight parents, all five Di,
strict endpoints and all labeled multiplicities. No scientific check ran.

The full quantum kernel and unnormalized maps qD/2 from RI36/RI41 remain
unchanged; this scalar incidence theorem is not an informative quantum
evolution or a DET-native reconstruction of geometry, mass or gravity.
Option B, Status M and RET's pause are unchanged. RI167 and measurement
qualification remain separately owned. Root owns execution admission,
independent acceptance, repository/index/Git and publication.

The exact RI36, RI41, RI127, RI147, RI151, RI155, RI157 and RI166 source
identities and governance selection are in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json)
and [SOURCE_DEPENDENCIES.json](SOURCE_DEPENDENCIES.json), with the explicit
historical stopping rules in [DEPENDENCY_NOTES.md](DEPENDENCY_NOTES.md).
Literal proof reading and administrative byte validation are not target
execution or independent mathematical acceptance.
