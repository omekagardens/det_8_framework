# RI120: bounded symbolic prefix simplifications

26 September 2026. Analytic source preparation only. No held row, native
coefficient, polynomial coefficient, actual scale or H/z value is evaluated.
The actual RI41 prefix and RI63 strict mixture are retained. These lemmas
do not settle the complete connected-sensitivity question.

## 1. Accepted premise and a Ferrers test

RI63 COMPLETION.md sections 1 and 4 establish that every active canonical
boundary component is everywhere defect-neutral and that the actual strict
coefficient is

    alpha_tilde_c = (35/36) alpha_min_c + t,       t=c5/36>0.

Consequently any component containing a defect-raising slot has canonical
coefficient zero and actual coefficient exactly t. The same conclusion
holds for a neutral slot joined to a raising one by a ratio-component edge.
No universal assertion about optimizers is being substituted for this
accepted finite-layer fact.

In a Ferrers downset in N^2, the principal ideal of a cell (i,j) is the
entire rectangle [0,i] times [0,j]. It is a chain only when i=0 or j=0.
If two incomparable cells have chain principal ideals, they lie on different
axes, and their principal ideals intersect only at the unique minimum.
Thus a finite order with two incomparable elements whose principal ideals
are chains sharing two or more vertices cannot be Ferrers. This is a
necessary obstruction, not a purported complete characterization.

## 2. The C5 next-to-full slot is sigma-independent

Let C5 be the five-chain. Adding a newborn above a proper chain prefix of
length k>=2 gives two incomparable maxima with chain principal ideals
sharing that k-vertex prefix. The test above makes the terminal non-Ferrers.
Deleting the newborn leaves C5, so its defect is exactly one, whereas
C5 has defect zero. Empty birth also raises defect by one. Therefore all
C5 slots at masks 0,3,7,15 have actual component coefficient t.

The RI38 maximal-deletion potential at a unique-maximal parent C5 is the
corresponding probability at C4. In RI117 notation, for every transported
record assignment,

    D_eta(S)=t B_xi(S),               S=0,3,7,
    e_eta=q_B(C5,eta,15)=t c_xi.                              (A1)

Here eta=xi+8 sigma. The C4 full probability c_xi ignores its top mark
sigma by the proved unique-top/maximal-record lemma. Thus e_eta is
independent of sigma. This is a derived equality, not a smallness or
read-permission argument.

The remaining proper C5 ideal is mask 1. Its terminal is the Ferrers hook
with row lengths (5,1), so this particular defect argument does not remove
its canonical coefficient. Write that strict coefficient as tau_(r0)>0;
locality makes its probability depend only on the root bit. Its potential
is B_xi(1), hence

    D_eta(1)=tau_(r0) B_xi(1),        tau_(r0)>=t.               (A2)

Neither tau value is evaluated or asserted nonzero above t. Every stem
slot already excludes sigma by locality, and (A1) handles the only other
proper slot. Normalization therefore proves that the entire C5 row,
including its full complement ell_eta, is sigma-independent.

It follows that RI117's E2,A2,B2,C2 profiles are sigma-independent as well.
The source-only certificate must nevertheless retain the assigned sixteen
profiles and all fifteen reference quadratics; their duplicate equalities
are consequences to verify, not permission to omit half the record domain.
In particular Q2_8 is identically zero, not evidence for constancy of f2.

## 3. Every H5 stem slot has the restoration coefficient t

Write H5=C3 ordinal-sum A2, with chain vertices 0<1<2 and cap vertices
3,4. Its defect is one. The accepted RI102 proof already establishes that
the empty and full-stem precursor masks 0 and 7 raise defect to two.

For mask 3, the newborn 5 has past {0,1}. The terminal is non-Ferrers.
After deleting vertex 0, 1 or 2, its two old cap principal ideals are
still chains sharing at least two vertices. After deleting either cap,
the remaining old cap and newborn have chain principal ideals sharing
{0,1}. After deleting the newborn one recovers H5. The Ferrers test thus
excludes every one-vertex deletion, separately. Deleting the newborn and
one cap leaves C4. The terminal has defect exactly two, so mask 3 is
raising and has actual coefficient t.

For mask 1 the terminal H5 plus a root leaf still has the two incomparable
old caps with chain principal ideals sharing C3, so it is not Ferrers.
Deleting one cap leaves C4 plus a root leaf, the Ferrers hook with row
lengths (4,1). Thus this terminal has defect one. The H5 root slot itself
is neutral, but the birth from that hook parent above the old C3 is
raising from defect zero to one.

The two roles are the two second legs of the complete ordinary diamond
based at C4, with first precursors C3 and the singleton root. They have
positive first-leg factors. RI38's potentials satisfy the same diamond;
division gives equality of their component coefficients. The raising
hook-parent slot therefore forces the canonical coefficient of H5's
root slot to zero as well. This argument transports all inherited and
newborn marks, not just the zero-mark case.

Both singleton deletions of H5 leave C4; their double deletion leaves C3.
All four stem ideals T=0,1,3,7 consequently satisfy

    G_xi(T)=t B_xi(T)^2/A_xi(T).                              (A3)

For the one-cap H5 ideal, the already accepted diamond gives
h_xi=c_xi d_xi/b_xi. Equation (A1) at mask 7 says d_xi=t b_xi,
so

    h_xi=t c_xi,       m_xi=h_xi^2/c_xi=t^2 c_xi,
    j_xi=1-t sum_T B_xi(T)^2/A_xi(T)-2t c_xi.                 (A4)

All individual ideals remain in that full complement: four stem slots
and two distinct one-cap slots. No numerical q5 replacement is made.

## 4. Simplified sensitivity expression and the remaining gap

Insert (A3)-(A4) into RI117's complete V profile. It becomes

    V_xi=1+t^3 sum_T B_xi(T)^3/A_xi(T)^2
             -t sum_T B_xi(T)^2/A_xi(T)
             +2(t^2-t)c_xi.                                 (A5)

This is an exact symbolic reduction to actual C4 rows and the fixed
positive restoration coefficient. It is not a sign determination for
V_xi-V_0. The RI41 prefix uses record-sensitive component scales at size
four; these are not the common half-scales used at size six and above.
Replacing B by a common-scale law here would change the fixed baseline.

Similarly e_eta has now been proved independent of sigma, so RI117's
optional same-xi sigma comparison of f2 has zero Delta e. That shortcut
cannot prove connected sensitivity. Nothing in these lemmas forces all
other f2 contrasts to vanish, and nothing derives the required V contrast
from a contrast of E alone.

The bounded analytic examination therefore yields additional identities
but not an accepted conclusion that both f2 and f3 are nonconstant.
The complete assigned saved-row algebraic decision remains a legitimate
source-only fallback on the already held 40 rows/224 slots. These lemmas
authorize no evaluation, execution, root selection or new input domain.

## 5. Read scope and incident

The complete RI117 root adjudication and RI120 assignment were read
(tool chunk 259e78). The complete CONNECTED_CONSTRAINTS_LEMMA.md was read
(a91a70). RI63 COMPLETION.md sections 1-4 supply the strict-mixture and
active-component premises (8ba21b). RI102 AMPLITUDE.md sections 1-4 were
read for its defect and H5 coefficient arguments (a91a70). RI41's fixed
prefix and component-scale definitions were read from NORMALIZATION.md
sections 1-3 (49e783). No scientific certificate body was decoded.

A guessed read-only path CONNECTED_SENSITIVITY_LEMMA.md did not exist
(8ba21b); the actual directory was then listed and the correct
CONNECTED_CONSTRAINTS_LEMMA.md was read. The same initial command read
RI63's document successfully and returned zero overall; this does not
erase the failed first read. No source or existing evidence was modified.
