# RI243 — Six hook roles and an exact separation target

1 October 2026, Honolulu. Manual source-only derivation for independent
review. The actual hook has six unresolved prescribed component coefficients,
not six unidentified probabilities. This note identifies their original
component keys and derives both required C4 full complements from already
admitted coefficients. It does not read or resolve a new source coordinate.

## 1. Same law, whole parent, selected records

Keep the RI41 finite law, its maximal-deletion potential, its complete
marked-parent quotient and its original component-root ordering. For a
proper ideal S of P,

    q_(P,r)(S)=alpha_[P,S,r|S] * u_(P,r)(S).

Here alpha is constant on the original ratio component, not on a newly
chosen partition. The component root is the minimum original triple
(E, precursor mask, selected-record mask). Only marks outside the selected
precursor are forgotten by locality; marks inside it may be shown irrelevant
only by an actual diamond identity.

Write the hook J as r<a<b and r<x, with natural order (r,a,b,x).
Its order masks are (0,1,3,1). Its minimum relation code is 78 under that
order: the transitive strict relations contribute 2+4+8+64. The other
topological orders have codes 142 and 2062. The admitted RI189
topological-minimum argument excludes a smaller nontopological code.

For the lower three-event fork B: r<a,r<x, put

    a_0=19/220,    a_1=7/220,
    F_0=43/55,    F_1=49/55.                              (R1)

Here a_i is either root-plus-one-leaf probability, and F_i is the
FULL fork probability. The RI41 complete fork row has empty and root
probabilities 1/44 and both leaf-pair occurrences a_i. Thus
F_i=1-2/44-2a_i; the two distinct ideals have not been merged.

The symbol a_i in this note is not the three-chain full probability
a=41/44 used in the original normalized system. Subscripts make the
distinction explicit.

## 2. The f family: selected {r,x}

Initially retain root mark i and short-leaf mark v. The omitted maximum
is b, so maximal deletion gives

    u_J({r,x};i,v)=q_B({r,x};i,v)=a_i.                    (R2)

Appending a new event y above {r,x} gives the terminal order

    r<a<b,    r<x<y.

Its only maxima are b,y. Deleting either maximum gives a hook; their
common base is B. Retain an arbitrary marking (i,u,v) of (r,a,x) and
both possible bits for each newborn event. Equality of the two birth
orders, with their common newborn factors 1/2 cancelled, is

    a_i q_J({r,x};i,v)
        =a_i q_J'({r,a};i,u).                            (R3)

J' has long arm r<x<y and short arm r<a. Whole-parent relabeling
therefore transports its selected short arm to the same f role.
Since a_i>0 and u,v vary independently, all short-leaf bits are in
one component for each fixed i. This is a diamond consequence, not
permission to omit a selected record at the outset.

The two maximal-deletion presentations exhaust this terminal type.
Every ratio edge preserves the unmarked terminal type. Their common
compulsory past is {r}; it is present in each selected precursor, so
its record i cannot be changed along any edge or relabeling. The
arm exchange also fixes r. Hence there are exactly two f components,
one per root mark. The terminal has no presentation of another parent
shape.

At code 78 the selected precursor has mask 9; its selected-record
mask is i+8v. The proven component contains both v values, so its
minimum is (78,9,i). Define the still-unresolved actual coefficients

    x_i=alpha_(78,9,i),    i=0,1.

The complete f expressions are

    f_hook,0=(19/220)x_0,
    f_hook,1=(7/220)x_1.                                  (R4)

Each expression covers all eight whole-hook record assignments with
that root bit. Unselected a,b marks remain present in the whole record;
the selected x bit remains present and is transported through R3.

## 3. The g family: selected {r,a,x}

Here i is the root mark and u is the mark of a, the atom on the
DISTINGUISHED LONG ARM. It is not the mark of the short leaf x.
Initially retain that short-leaf mark v too. Again only b is an
omitted maximum, now leaving the FULL lower fork:

    u_J({r,a,x};i,u,v)=F_i.                               (R5)

Appending y above {r,a,x} gives

    r<a<b,    r<x,    a<y,    x<y.

Its only maxima are b,y. Delete y to get J. Delete b to get the
diamond D: r<a,r<x,a<y,x<y. Both presentations have common base B.
The ordered precursors at that base are {r,a} and all of B, giving

    a_i q_J({r,a,x};i,u,v)
        =F_i q_D({r,a};i,u).                             (R6)

The diamond selected pair has only y as omitted maximum, so its
potential is a_i. Dividing R6 by a_i F_i identifies the component
coefficient on both presentations. It also proves independence
of v on the hook side, without dropping the selected x record.

The compulsory intersection of the maximal pasts is the chain {r,a}.
The terminal distinguishes a from x: a lies below both b,y whereas
x lies below only y. Thus terminal automorphisms and every presentation
preserve the two ordered compulsory marks i,u. All presentations are
the two just named. In a canonical diamond presentation either arm can
be the selected pair; equivariance transports the selected mark with
that arm, never to the unselected one.

For each fixed i,u, the two hook nodes v=0,1 connect to the diamond
selected-pair node. This exhausts the component. All old markings,
both newborn bits, ordered reversals and equivariant arm-swapped
copies are retained. No raw-equation count is asserted.

The diamond's minimum relation code is 2190: either topological arm
order contributes 2+4+8+128+2048. The same admitted minimum lemma
excludes a smaller nontopological code. Since 78<2190, the component
root is a hook key. There the precursor mask is 11 and the selected
record mask is i+2u+8v. Minimizing over the proven v transport gives

    root(g_(i,u))=(78,11,i+2u).

Define y_(i,u)=alpha_(78,11,i+2u). Then

    g_hook,(0,u)=(43/55)y_(0,u),
    g_hook,(1,u)=(49/55)y_(1,u).                          (R7)

Each expression covers all four whole-hook markings with those fixed
r,a bits; b,x are not physically erased. The f terminal and g terminal
are different unmarked orders (the latter has a joined past), so no
ratio path joins their components.

The exact acquisition roles, before any source-index lookup, are:

| Probability role | Original component-root key | Potential multiplier |
| --- | --- | --- |
| f_hook,0 | (78,9,0) | 19/220 |
| f_hook,1 | (78,9,1) | 7/220 |
| g_hook,(0,0) | (78,11,0) | 43/55 |
| g_hook,(0,1) | (78,11,2) | 43/55 |
| g_hook,(1,0) | (78,11,1) | 49/55 |
| g_hook,(1,1) | (78,11,3) | 49/55 |

In particular, the displayed ROLE order is not the source root order:
g_(0,1) has mask 2 while g_(1,0) has mask 1. No original zero-based
index, default status, override status or coefficient value is guessed.

## 4. The C4 complements require no additional source lookup

The admitted RI231 W1 states alpha_I=w/e_I=1/8, where w is the
C4 empty probability and e_I=1/44 is the complete three-chain empty
probability. This relation also follows from the empty/full diamond
between C4 and K=C3 disjoint isolate:

    e_I q_K(I)=a w,    q_K(I)=alpha_I a,    a=41/44.

Positivity permits cancellation of a, yielding

    w=e_I alpha_I=1/352.                                (R8)

The admitted pi_i=1/8 and sigma_0=1/8,sigma_1=27/125 give the
C4 root and initial-pair probabilities

    p_0=p_1=1/352,
    s_0=1/352,    s_1=27/5500.

Use the already accepted b_0=8077/8800 and contrast
c_1-c_0=-9/44000. The COMPLETE C4 normalization, including all
four proper ideals empty/root/pair/triple, gives

    c_0=1-w-p_0-s_0-b_0
       =1-3/352-8077/8800
       =648/8800=81/1100=3240/44000,
    c_1=c_0-9/44000=3231/44000.                         (R9)

These are manual deductions from admitted coefficient identities, not
new values read from the original certificate. No extra C4 role is
included in the proposed acquisition.

## 5. Six symbolic coefficients suffice for the actual exception test

Keep RI240's minima, their ties and both zero-positive-part branches.
Let [t]_+=max(t,0), and define

    m_0=min(y_(0,0),y_(0,1)),
    m_1=min(y_(1,0),y_(1,1)),
    A_0=[205-76x_0-1376m_0]_+,
    A_1=[205-28x_1-1568m_1]_+.

The complete actual deficits and cleared contrast are

    P_i=[41/352-f_hook,i/2
                   -min(g_hook,(i,0),g_hook,(i,1))]_+,
    P_0=A_0/1760,    P_1=A_1/1760,
    Z_hook=3240A_1-3231A_0,
    F=c_0 P_1-c_1 P_0=Z_hook/77440000,
    d=(35/1476)F/(c_0 c_1)
      =25(35/1476)Z_hook/(3240*3231).                    (R10)

The multipliers are manually checked with the common denominator 1760:
41/352=205/1760, 19/440=76/1760, 7/440=28/1760,
43/55=1376/1760 and 49/55=1568/1760. Also
44000*1760=77440000 and 44000/1760=25.

Nothing here chooses a minimum, removes a tie, or assumes a positive
deficit. All x,y remain the actual prescribed same-source coefficients,
not free variables to be fitted or rounded.

## 6. A precise, branch-safe denominator certificate

RI240 proves for the unchanged actual scale that

    d=d7  =>  -2^-77<F<0,
    d7=-theta^2 K/(1-theta/8)<0.                         (R11)

Suppose the SIX original coefficient strings can separately be proved
to admit a common positive integer denominator D with D<=2^50.
Write x_i=n_xi/D and y_(i,u)=n_yiu/D with integer numerators.
No reduced-fraction assumption is needed. Define the integers

    B_0=max(205D-76n_x0
                      -1376min(n_y00,n_y01),0),
    B_1=max(205D-28n_x1
                      -1568min(n_y10,n_y11),0).

Then A_i=B_i/D, including all ties and zero cases, so

    F=(3240B_1-3231B_0)/(77440000 D).                    (R12)

Because 77440000<2^27, its displayed positive denominator is
strictly less than 2^77. If the numerator is nonnegative, F>=0;
if negative, integer spacing gives F<-2^-77. Either contradicts
R11. Therefore the precise conditional theorem is

    six-key SAME-SOURCE common denominator 0<D<=2^50
        => d!=d7.                                       (R13)

A product or common multiple of the six literal denominators can serve
as D; it need not be their least common multiple. The divisibility
witness and the bound must be checked manually. This note does not
assert that the actual strings meet R13. The discovery-rounding story
is not evidence for it. Rationality alone supplies no size bound.

An independently established F>=0 or F<=-2^-77 also separates d7
without R13. F in the intervening open strip, or failure of the
sufficient denominator bound, leaves the branch unresolved; neither
proves equality d=d7.

## 7. Bounded result, not a new native law or physical bridge

The result is a manual six-role component proof, a derivation of the
two C4 complements, and a precise conditional integer-spacing test.
The original six coefficient strings/default-or-override selections
remain unacquired. The companion acquisition document is only a
design submitted for independent review and separate root admission.

Excluding d7 would still leave the accepted canonical C_b comparison
for the complete normalized decision. If d7 remains possible, the
RI240 exceptional Delta Q obligation remains exactly as accepted.
No witness, signed inconsistency, optimum, improvement or new amplitude
is asserted here. The ten-coordinate, thirteen-equation system and
complete recovery printed in the contract remain binding for every
original record and ideal.

The finite law's coefficients are supplied accepted premises. Identifying
them is not deriving their selection from DET. No full-QM, all-size,
geometry, mass or gravity result follows. Option B and Status M are
unchanged. All 15 boundary objects and the 423-source manifest remain by
reference. Stop after source-only handoff; root owns review, admission,
publication and successor selection.
