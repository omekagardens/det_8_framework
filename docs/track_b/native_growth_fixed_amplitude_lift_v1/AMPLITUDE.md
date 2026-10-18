# RI-102 — the fixed empty-birth lift fails at amplitude one quarter

25 September 2026. External analytic proof proposal for coordinator
adjudication. Actual baseline B, its half-scale rules, the RI-88 direction
and the prescribed amplitude are unchanged.

**Result.** The accepted RI-101 empty-birth signed lift is not positive at
epsilon=1/4. A named disconnected parent row has a formal proper-birth
probability greater than 41/4 while its full-birth probability exceeds
1/2. The signed row still sums to one, so another entry is strictly
negative. The violating multiplier is among the two specified classes
J2,J3. In fact this lift's positive-amplitude threshold is strictly below
1/82. This rejects this lift at the requested amplitude, not every
positive shared-child extension.

## 1. Fixed premises and notation

Keep [RI-101's accepted signed construction](../native_growth_signed_extension_v1/SIGNED.md):

\[
 T_j=C_3\oplus Q_j,\quad J_j=T_j\sqcup A_1,\quad
 Z(T_j)=z_j,\quad Z(P)=0\text{ otherwise},
\]
\[
 e_P=q_B(P,r,\varnothing)>0,\qquad
 y(J_j)=z_j/e_{T_j},\qquad y(H)=0\text{ otherwise}.
 \tag{1}
\]

The eleven cap classes and their complete individual-slot inventory are
those of [RI-85](../native_growth_four_vertex_cap_v1/DESIGN.md);
z is the actual [accepted RI-88 direction](../native_growth_four_vertex_cap_check_v1/RESULT_REVIEW.md),
with z1=1 and all coordinates nonzero. Empty probabilities e_P are
record-blind by strict precursor-record locality, not freely chosen.

Use a notation distinct from the three-chain C3:

\[
 K=C_3\oplus A_3,\qquad R=K\sqcup A_1,\qquad I=C_3\subset K.
 \tag{2}
\]

K is RI-85's six-parent P1. The isolated vertex of R is denoted w.
A natural representative is

\[
 K=(0,1,3,7,7,7),\qquad R=(0,1,3,7,7,7,0).
 \tag{3}
\]

The final zero in R is the appended isolated vertex, not a new minimum
chosen to replace the inherited labels. I is ideal mask7 in these
representatives. The all-zero marking of R is one explicit witness
row; the argument below actually holds for every marking.

The actual B through parent size five includes the accepted
[RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
and actual
[RI-63 strict mixture](../native_growth_expected_defect_completion_v1/COMPLETION.md).
At parent sizes six and seven it uses the common RI-38 half-scales
rho=a6 and s=a7, as in RI-85/RI-99. They are not numerically known or
replaced. In particular every seven-parent row has

\[
 q_B(P,r,P)>\tfrac12,\qquad
 \sum_{S\subsetneq P}q_B(P,r,S)<\tfrac12.
 \tag{4}
\]

Indeed s=1/[2(1+M7)] and each proper potential sum U(P,r)<=M7, so its
proper mass is at most M7/[2(1+M7)]<1/2. No selected-row maximum is
substituted for M7.

All complete record cubes, immutable fair newborn bits, strict
precursor-record locality, marked equivariance, eligible ideals and
whole scalar-passive maps qD/2 remain premises. The full payload is not
replaced by a scalar observation, but no informative quantum dynamics
is introduced. The proof below concerns this fixed conditional law.

## 2. An exact ratio bound from the accepted size-four height constraint

Let H5=C3 ordinal-sum A2. For any marking xi of C3 define the following
actual held quantities, transporting the same stem records throughout:

\[
 A=q_B(C_3,\varnothing)=\tfrac1{44},\qquad
 a=q_B(C_3,C_3)=\tfrac{41}{44},\qquad a/A=41,
\]
\[
 B=q_B(C_4,\varnothing)>0,\qquad
 b_\xi=q_B(C_4,\xi,C_3)>0.
 \tag{5}
\]

The first line follows from RI-41's explicitly fixed three-chain row:
its three proper ideals empty, singleton root and initial pair all have
probability 1/44. The full complement is 41/44. These values are
independent of marks. B is also record-blind; b_xi may depend on all
three stem bits. The C4 top bit is not in its proper precursor.

The other accepted RI-41 premise is the uniform bound

\[
 \tau_4(P,r)=
 \sum_{\substack{S\ {\rm ideal\ of}\ P\\
        H(P+S)=H(P)+1}}q_B(P,r,S)<\tfrac{19}{40}
 \quad\text{for every four-parent and every marking}.
 \tag{6}
\]

Here H counts vertices of a longest chain. Both fair newborn marks are
summed in q; this is the complete height-increment probability, not
only the full-birth mass on an arbitrary parent.

For each strict ideal S of C3 (masks0,1,3), form P_S=C3+y_S. It has
height three. A subsequent birth with past the old C3 raises its height
to four. Compare it with the opposite birth order, first a full birth
from C3 to C4, then a birth with past S. The inherited marked diamond,
with every newborn bit retained, gives

\[
 a\,q_B(C_4,\xi\mathbin{\|}\beta,S)
    =q_B(C_3,\xi,S)\,q_B(P_S,\xi\mathbin{\|}\gamma,C_3)
    =A\,q_B(P_S,\xi\mathbin{\|}\gamma,C_3).
 \tag{7}
\]

Here xi is the full C3 marking; beta marks the full-past newborn
and gamma marks the S-past newborn. Both are arbitrary, and named
terminal coordinates are transported together. The last factor is
one height-raising slot of P_S, so (6) yields

\[
 q_B(C_4,r,S)<\frac{19}{40\cdot41}
             =\frac{19}{1640}
        \qquad(S=0,1,3).
 \tag{8}
\]

This holds for every C4 marking: it follows from the full marked
diamond and an all-record bound, not an all-zero substitution.

For the chain C4 only its full ideal raises height to five. Therefore
q_B(C4,r,C4)<19/40. Its complete five-ideal row consists of masks
0,1,3,7,15. Subtracting the four just-bounded slots gives

\[
 b_\xi>
 1-\frac{19}{40}-3\frac{19}{1640}
 =\frac{201}{410}.
 \tag{9}
\]

Since 0<B<19/1640,

\[
 \boxed{\displaystyle
 \frac{b_\xi}{B}>\frac{804}{19}>41
       \quad\text{for every stem marking }\xi.}
 \tag{10}
\]

These are rational bounds derived from already printed accepted
constants. No actual C4 coefficient has been queried or recalculated.

## 3. Why two H5 slots have the same actual strict-restoration scale

Use the exact [RI-56 Ferrers defect](../native_growth_ferrers_defect_v1/DEFECT.md):

\[
 \delta(P)=\min\{|D|:\ P\setminus D
                  \text{ is an induced Ferrers order}\}.
 \tag{11}
\]

Here D is an arbitrary diagnostic vertex set, not necessarily an ideal.
No committed record is actually removed. A Ferrers order is any finite
down-set of the product order on N^2, not just a rectangle.

### Elementary intrinsic classification

Every nonempty Ferrers order has a unique minimum. If it is not a
chain, it has both axis-neighbor cells (1,0) and (0,1) above (0,0);
these are two distinct atoms, meaning vertices covering the minimum.
Indeed, absence of either axis neighbor forces the whole down-set
onto the other axis, hence a chain.

For k>=2 and m>=2, C_k ordinal-sum A_m is nonchain but has only one
atom, the second chain vertex. It is therefore not Ferrers.

Consequently H5=C3 ordinal-sum A2 is not Ferrers, while deleting one
cap gives the chain C4. Thus delta(H5)=1. The core birth H5+I is
C3 ordinal-sum A3. Deleting one of its three caps leaves H5;
deleting any of its three stem vertices leaves C2 ordinal-sum A3.
Both are nonchain with one atom, so none is Ferrers. The whole
six-order is also non-Ferrers. Deleting two caps leaves C4. Hence

\[
 \delta(H_5)=1,\qquad \delta(H_5+I)=2.
 \tag{12}
\]

RI-56 section 2 also proves that every empty birth at a nonempty parent
raises this defect by exactly one: an induced Ferrers suborder cannot
contain both the new isolated vertex and an old vertex. Thus

\[
 \delta(H_5+\varnothing)=2.
 \tag{13}
\]

The two proper H5 slots empty and I are therefore defect-raising for
every marking. This proof uses arbitrary Ferrers down-sets and arbitrary
induced deletions, not a classification restricted to rectangles.

### Apply the accepted actual RI-63 mixture

RI-63 section 1 establishes that all 69 active components of its
canonical **boundary** law are everywhere defect-neutral. If a
component contains even one raising slot, its canonical boundary
coefficient must therefore vanish. This is a specific accepted
finite-layer result, not a general assertion about every optimizer.

Both H5 slots above have zero boundary coefficient. The actual
strict law, however, is not that boundary law: RI-63 section 4 fixes

\[
 \widetilde\alpha_c=\frac{35}{36}\alpha_c^{\min}
                       +\frac{c_5}{36},\qquad c_5>0.
 \tag{14}
\]

It follows that both slots have the same strictly positive coefficient

\[
 t=c_5/36,
 \tag{15}
\]

even if they are in different ratio components. No new equality of
components is asserted and no probability is set to zero.

Write G=q_B(H5,empty)>0 and g_xi=q_B(H5,xi,I)>0. The RI-38
maximal-deletion potential has two singleton deletions leaving C4
and one double deletion leaving C3. Using their common coefficient
t from (15) gives

\[
 G=t\,\frac{B^2}{A},\qquad
 g_\xi=t\,\frac{b_\xi^2}{a},\qquad
 \frac{g_\xi}{G}
   =\frac1{41}\left(\frac{b_\xi}{B}\right)^2.
 \tag{16}
\]

For the core slot each restriction keeps the same complete stem
marking. The surviving cap top is outside the precursor and its bit
is not read. For the empty slot no marks are read. The denominator
in the core potential is the complete C3 full slot a, not its empty
probability. All factors and t are strictly positive.

This cancellation uses the actual strict mixture, not the zero
boundary law, a half-scale replacement for q5, or an altered prefix.

## 4. The scale-free six-parent ratio exceeds forty-one

In K=C3 ordinal-sum A3, the empty and core ideals each omit all
three cap maxima. The maximal-deletion formula has three singleton
deletions leaving H5, three double deletions leaving C4 and one
triple deletion leaving C3. The actual common positive rho is the
same in both size-six probabilities:

\[
 q_B(K,r,I)=\rho\,\frac{a g_\xi^3}{b_\xi^3},\qquad
 e_K=q_B(K,\varnothing)=\rho\,\frac{A G^3}{B^3}.
 \tag{17}
\]

These are direct proper-potential formulas on the retained prefix,
also consistent with RI-85's P1 core coefficient. No cap mark is
read in either precursor. Dividing and using (5),(16),

\[
 \mathcal R_\xi:=
 \frac{q_B(K,r,I)}{e_K}
 =\frac aA
   \left(\frac{g_\xi}{G}\right)^3
   \left(\frac B{b_\xi}\right)^3
 =\frac1{41^2}\left(\frac{b_\xi}{B}\right)^3
 >41.
 \tag{18}
\]

Both the actual unknown rho and the actual strict-restoration t have
cancelled. No global M6, M7, chosen half-scale or numeric q6 row is
needed for this strict bound. It holds for all complete markings of K,
including every choice of the three cap bits.

## 5. A complete named row rejects the one-quarter lift

The parent R=K disjoint A1 lies outside the eleven connected support
classes, so h7(R)=1. A birth with past I produces J1, because
K+I=T1=C3 ordinal-sum A4. For every complete marked row of R,
the baseline empty/I diamond gives

\[
 q_B(K,r,I)e_{T_1}=e_K q_B(R,\widetilde r,I).
 \tag{19}
\]

This identity follows from equality of the complete D/4 maps for
the two birth orders, with all records transported and both newborn
bits retained. The empty probabilities ignore those bits. There is
no division by a state or a selected payload trace.

The RI-101 affine formula on this parent is

\[
 \widehat q_\epsilon(R,\widetilde r,S)
   =q_B(R,\widetilde r,S)
          \bigl(1+\epsilon y_{[R+S]}\bigr).
 \tag{20}
\]

A hat emphasizes that these are **formal signed** row entries until
nonnegativity is proved. RI-101's exact Ay=Z gives a sum of one for
this complete row for every epsilon, whether or not its entries are
positive. From y(J1)=1/e_T1 and (18),(19),

\[
 \widehat q_\epsilon(R,\widetilde r,I)
 =q_B(R,\widetilde r,I)+\epsilon\mathcal R_\xi.
 \tag{21}
\]

At the unchanged prescribed amplitude,

\[
 \boxed{\displaystyle
 \widehat q_{1/4}(R,\widetilde r,I)>\frac{41}{4}>1.}
 \tag{22}
\]

This already contradicts nonnegativity of a normalized complete row.
Moreover the full-birth child has a unique maximum, so its correction
y is zero and its unchanged baseline probability exceeds 1/2 by (4).

For explicit coverage, each ideal of R either is an ideal of K or
is that ideal together with w. Hence there are 22 individual ideals,
not an averaged or support-conditioned row. The only nonzero child
correction slots are exactly:

| Individual precursor masks in R | Child | Multiplicity |
| --- | --- | ---: |
| 7 | J1 | 1 |
| 15,23,39 | J2 | 3 |
| 31,47,55 | J3 | 3 |

They are RI-85's supported K slots, with w excluded. Every remaining
one of the 15 ideals has y=0 and a strictly positive baseline entry,
including the full ideal mask127. Old isolated bit6 and all other
records remain independently allowed.

Thus normalization of the signed row and (22) force at least one
strictly negative entry among the six J2/J3 slots. Since their baseline
coefficients are strictly positive, this is the rigorous two-class
violating witness

\[
 \boxed{\displaystyle
 e_{T_2}+z_2/4<0\quad\text{or}\quad e_{T_3}+z_3/4<0.}
 \tag{23}
\]

In particular the failure is not merely equality at a forbidden zero
endpoint. We do not identify which alternative holds by unperformed
coefficient evaluation; the complete named row proves the disjunction.

Every inequality above holds for every marking; the all-zero row of
(3) is a sufficient single witness. Newborn-bit-resolved entries are
half the displayed ideal entries; (22) would still exceed one even
after that factor. The argument itself uses the complete ideal row,
summing both fair newborn outcomes consistently.

## 6. An upper bound on the positive-amplitude threshold

This additional bound is analytic; it does not select a smaller
amplitude or authorize a new seed. Define the nonempty set

\[
 N=\{j\in\{2,3\}:z_j<0\},\qquad
 \eta_{23}=\min_{j\in N}\frac{e_{T_j}}{-z_j}>0.
 \tag{24}
\]

N is nonempty because K's accepted harmonic row contains only
z1,z2,z3 with positive baseline slot coefficients and z1=1.

Let Nslots be all individual supported K ideals whose child index is
in N. Define their negative harmonic mass

\[
 L=\sum_{S\in Nslots}q_B(K,r,S)(-Z(K+S)).
 \tag{25}
\]

Complete harmonicity says that L equals the sum of all positive
correction terms. That sum includes q_B(K,r,I)z1, so L>=q_B(K,r,I).
For every negative slot e_(K+S)>=eta23*(-Z(K+S)). Applying the
baseline empty/S diamond individually and retaining all repeated
ideals yields

\[
 \eta_{23}L
 \leq\sum_{S\in Nslots}q_B(K,r,S)e_{K+S}
 =e_K\sum_{S\in Nslots}q_B(R,\widetilde r,S)
 <\frac{e_K}{2}.
 \tag{26}
\]

The strict last inequality follows because these are proper R slots
and its total baseline proper mass is less than 1/2. Consequently,

\[
 \eta_{23}<\frac1{2\mathcal R_\xi}<\frac1{82}.
 \tag{27}
\]

The accepted RI-101 lift threshold is the minimum over **all**
negative z_j. Therefore

\[
 0<\epsilon_{\rm lift}\leq\eta_{23}<\frac1{82}<\frac14.
 \tag{28}
\]

This is an upper bound on that lift's interval, not a numerical
evaluation of its exact endpoint or a certified choice of an interior
amplitude. RI-101's existence of some sufficiently small positive
interval is preserved. No single amplitude valid at all later sizes
is established.

## 7. Adjudication boundary and provenance

The prescribed-amplitude decision is complete as a manual analytic
proof: **reject the RI-101 empty-birth lift at epsilon=1/4**. The
failure is witnessed by R=(C3 ordinal-sum A3) disjoint A1 with
precursor I=C3; one of J2,J3 has a strictly negative multiplier.
There is no missing full-layer scale domain for this decision:
the relevant scales cancel or enter only through the inherited
strict half-mass bound.

This does not reject every positive solution of the RI-99 shared-child
system at epsilon=1/4. It does not undo signed feasibility, smaller
amplitude existence or the accepted RI-95 common-level obstruction.
No new support, new direction, changed prefix, replacement scale,
optimizer or executor is proposed by this note.

The additional load-bearing accepted sources are RI-41's printed
three-chain row and complete size-four height bound; RI-56's actual
Ferrers-defect definition and empty-birth lemma; and RI-63's
everywhere-neutral active boundary support and actual strict mixture.
All were read completely for this work. The older RI-38/85/88/101
premises remain fixed; their exact identities and root acceptance
are retained in the external PREMISES.json.

All derivations here are manual finite proofs and symbolic bounds.
No native coefficient was evaluated, no global table or numerical
search was run, no helper/checker was imported or compiled, and no
scientific certificate was parsed for arithmetic. One reviewer's
accidental broad text search exposed a truncated certificate match;
it was stopped, excluded from every inference and reported to the
coordinator. An initially suggested rectangle-only defect argument
was also withdrawn and replaced by section 3's arbitrary-Ferrers
proof. Both events and their corrections are retained in the external
review record, rather than hidden by a clean-execution claim.

This remains a conditional finite record/growth result, not a new
QM derivation, measurement forward map, geometry, mass or gravity
result. Option B, metric-as-record Status M and RET's pause are
unchanged.

The sole proposed repository artifact is this AMPLITUDE.md for
docs/track_b/native_growth_fixed_amplitude_lift_v1/. External
provenance and review metadata are not executors. No accepted source,
repository file, index or git state is changed by this worker.
Coordinator adjudication, publication and any further scoped
assignment remain separate. The bounded handoff does not pause or
end the wider programme.
