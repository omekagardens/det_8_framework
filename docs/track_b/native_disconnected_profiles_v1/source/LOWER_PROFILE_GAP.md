# Lower profile reduction and the unresolved normalized mobility witness

30 September 2026, Honolulu. RI225 author deduction, conditional on the
same accepted finite native law. This note reduces the lower dependence
of all five disconnected profiles to fixed empty-birth ratios and two
root-record functions. It does not decide the normalized H30 system.

The accepted RI223 singleton theorem is an input, not a result repeated
here. Strict improvement is still equivalent to the exact full solution
with u2=-1. An actual inconsistency identity would instead prove the
ceiling is optimal. Neither witness has been obtained.

## 1. Empty diamonds turn the no-isolate profiles into fixed weights

Retain all notation from
[DISCONNECTED_PROFILES.md](DISCONNECTED_PROFILES.md).
For each of the four individual stem ideals S in J, define

    alpha_S=e_(I+S)/e_I,
    beta_S=e_(C4+S)/e_C4.                                   (G1)

Here P+S appends one new event with precursor S, and e_Q is the
actual empty-birth probability at Q. The ratios are positive and
record blind by the inherited empty-locality theorem. They are
not independent parameters and no actual value is extracted.

The complete empty/ordinary-birth diamonds give, including S=I,

    k_S=alpha_S*A_S,       y_S=beta_S*B_S.                   (G2)

The precursor excluding the isolate is proper in K or Y even when
its original precursor was full in I or C4. Both routes of each
whole-map diamond retain their inherited records and newborn bits.
Positivity permits the displayed division.

Write A_E=e_I and w=e_C4, as in accepted RI223. The already accepted
empty identities yield

    alpha_I=w/A_E,
    beta_I=theta*w/A_E,
    q(Y,C4)=theta*c=h.                                     (G3)

If beta is extended to the fifth C4 ideal C4 itself, beta_C4=theta.
No additional empty-child or seed coordinate is resolved in (G3).

Consequently every no-isolate expression in (P2) is now

    V_H=sum_S (beta_S^2/alpha_S)*G_S +2m+j,
    V_C=sum_S beta_S*D_S +theta*e+ell,

    R1=sum_S (beta_S^3/alpha_S^2)*A_S*G_S^3/B_S^3,
    R2=sum_S (beta_S^2/alpha_S)*D_S*G_S/B_S +e*h^2/c^2,
    R4=sum_S beta_S*D_S^2/B_S +e^2*h/c^2,

    P_Y=1-sum_S beta_S*B_S-h.                              (G4)

In particular V_H and V_C are fixed weighted sums of existing
connected held rows, not independent disconnected profile inputs.
All four terms, including the empty term, remain in every sum.

Only alpha_S,beta_S for S empty, initial singleton, initial pair
remain additional empty ratios in this representation; the two
I entries are already reduced in (G3). Calling them six named
ratios does not assert their independence, numerical values or
information-theoretic minimality.

## 2. Three of four isolate-containing Y slots are raising

Let the C4 chain be r<a<b<c. K consists of r<a<b and o isolated;
Y includes c as well. For S in J, the precursor S union {o}
omits exactly the chain maximum c of Y. Its maximal-deletion
potential is therefore k_S^+, without any record quotient shortcut.

Y has Ferrers-cell deletion defect one: it has two minima and is
not a nonempty Ferrers cell order; deleting o leaves C4.

For S equal to empty, {r,a}, or I, the terminal after the indicated
birth x has defect exactly two. This can be checked without a graph
enumeration:

- If S is empty, the terminal is C4 disjoint C2. Every single
  deletion leaves two nonempty components. Deleting o and x
  leaves C4.
- If S={r,a} or I, r and o are two minima. A deletion other than
  r or o preserves both. Deleting r still leaves a and o as two
  minima. Deleting o leaves a four-chain with an extra branch
  above a or b. The two incomparable tops have chain principal
  ideals sharing respectively two or three stem vertices, which
  is impossible in a Ferrers cell order. Deleting o and x again
  leaves C4.

The common-cell obstruction is precisely the one in admitted RI127
RECORD_TRANSPORT: incomparable chain principal ideals in a Ferrers
cell order can share only its least cell. It is not a classification
of arbitrary objects with the name Ferrers.

These are therefore raising slots from defect one to two. The
accepted size-five rule says every active canonical component is
everywhere defect-neutral, so each such slot has zero canonical
coefficient and actual restoration coefficient theta. Hence

    y_S^+=theta*k_S^+,
                      S=empty, initial pair, I.             (G5)

This invokes the original rule at the same parent size five as its
prior accepted uses; it does not extrapolate that coefficient to a
new size or replace the actual prefix with a common-scale law.

The remaining S={r} slot is not set equal to (G5). Its terminal
has defect one: it has two minima, but deleting o leaves the
Ferrers hook r<a<b<c with r<x. Thus the raising argument cannot
force its canonical coefficient to zero.

Define only the actual difference

    gamma(r)=k_{ {r} }^+>0,
    zeta(r)=y_{ {r} }^+-theta*gamma(r).                       (G6)

No sign, value or independence of zeta is assumed. In particular
this note does not replace it by zero or by a chosen canonical term.

## 3. Complete normalization reduces the two higher moments

Put

    T=sum_{S in J} k_S^+
       =1-sum_{S in J} alpha_S*A_S.                         (G7)

This is the complete K row: four ideals exclude o and four include
it, the latter including the full K. The accepted C3 law has three
record-constant proper probabilities and its record-constant full
complement. Thus T is one positive record-independent constant.

The complete Y row has five no-o ideals and five with-o ideals.
The latter are the four y_S^+ terms plus F_Y. From (G5)-(G7),

    F_Y=P_Y-theta*T-zeta,
    M2=theta^2*T+2theta*zeta+zeta^2/gamma,
    M3=theta^3*T+3theta^2*zeta
                       +3theta*zeta^2/gamma+zeta^3/gamma^2. (G8)

These are exact binomial expansions of the one exceptional term
plus the other three terms, not an automatic symbolic calculation.
Even if zeta vanishes, (G8) is valid and no division by zeta occurs.
Only gamma, an actual positive probability, is in the denominator.

Inserting (G4),(G8) in all five (P4) profiles removes every
unexpanded K/Y probability except the six fixed empty ratios and
the two actual functions gamma,zeta. The baseline keeps all of
them coupled. Their allowed values also preserve positive F_Y,
all full complements and every original row; this note does not
claim any chosen values would define an admissible baseline.

## 4. The two new functions depend only on the root record

The precursor defining gamma or y_{ {r} }^+ is {r,o}.
Strict precursor locality removes every other record. The bit on
o is maximal in both K and Y, so the separately proved maximal-
record invariance removes dependence on that bit as well.

Thus gamma and zeta each have just two actual values,

    gamma_0,gamma_1>0,    zeta_0,zeta_1,                      (G9)

indexed by the mark on the intrinsically ordered chain root r.
This is a proved equality across all records, not selection of a
convenient pair or erasure of a physically committed record.

There is also a justified consequence for D1 and D3. The complete
C4 row depends only on its root record: b,c have that accepted
actual-value property; its singleton slot does by locality; its
empty slot is record blind; its initial-pair slot follows from
complete normalization. This is retained explicitly in admitted
RI189 COMPONENT_ROUTING and COUPLED_CONTRAST.

For H, the empty slot is record blind, the singleton slot depends
only on the root by locality, and the core and two one-cap slots
are g=theta*b^2/a and h=theta*c. The full j has the accepted
RI127 root-only pattern. Complete normalization then makes its
initial-pair slot root-only too. Thus the complete G row has
that property, not just its core coefficient.

It follows from (G4),(G8) and (P3)-(P4) that g1 and g3 depend only
on the root bit. Their l1,l3 coefficient profiles have the same
property. All D1/D3 compatibility rows with the same root bit are
therefore identical; at most their one root-sector contrast is
nontrivial. The equations still hold on the full record cubes,
with their original multiplicities and labels.

No analogous blanket reduction is asserted here for D2,D4,D5 or
the remaining connected full profiles. Their existing complete
record domains remain explicitly required. In particular the new
D1/D3 result supplies no discarded D2 contrast.

## 5. What the native normalized question now requires

The accepted complete homogeneous recovery remains

    W1=-Gamma_10*u0-Gamma_12*u2-Gamma_13*u3,
    W2=-Gamma2*u2, W3=-Gamma3*u3, Wj=Uj for j>=4,

    delta v1=beta_10*u0+beta_12*u2+beta_13*u3,
    delta v2=beta2*u2, delta v3=beta3*u3,
    delta vj=-Uj/f_j(0), j>=4,
    delta d_i=-L_i(0;W)/(e_Ci*g_i(0)).                      (G10)

Keep u2=-1 and all ten unknowns u0,u3,U4,...,U11. For every record,
the five disconnected equations are (P9), now with the actual
profile formulas (P4),(G4),(G8). The eight connected conditions
remain

    Uj*(f_j(r)-f_j(0))=0,                  j=4,...,11.         (G11)

Constant f8,f11 retain their freedom, subject to all five (P9).
No other Uj is set to zero without a proof of a nonzero contrast.
No d_i is independently adjustable after (G10).

The exact missing witness is still either:

- A concrete exact solution of these rows with u2=-1, followed
  by recovery and verification of every original connected and
  disconnected row in (G10).
- A finite signed combination of the actual normalized rows
  cancelling all ten unknown columns while leaving a nonzero
  right side, or an equivalent native identity forcing W2=0
  on the complete homogeneous space.

No such solution or row combination is in this packet. The new
profile formulas do not themselves decide which alternative holds.
We do not divide by a hoped-for contrast or assume a determinant
is nonzero because it is formally nonzero.

For the explicit profile route, the newly exposed lower inputs
are precisely the combinations in (G4),(G8), and not full new
six/seven-parent tables. A sufficient same-source analytic lemma
could determine or bound those combinations tightly enough to
settle the native row identity; literal values are not necessarily
required. The normalization conditions alone have not supplied
that lemma here. This is not a theorem of nonderivability.

The newly admitted RI111 REPAIR, read completely, retains g_i as
full probabilities in its equations23; it does not calculate
these K/Y combinations. Reading it checked the source boundary
but did not fill this remaining coefficient premise. Its old
28-column w2=z2/w3=z3 restrictions are not imported into H30.

## 6. Exact lower-source boundary for the unresolved combinations

The four additional record-sector quantities in (G9) are directly
defined by the following literal parent/precursor roles:

    K: parent C3 disjoint A1, precursor {chain root,isolate},
       gamma_i=q_B(K,root bit i,{root,isolate});

    Y: parent C4 disjoint A1, same precursor,
       zeta_i=q_B(Y,root bit i,{root,isolate})-theta*gamma_i.

Maximal and outside-precursor bits are suppressed only by the
proof in section4. The six additional empty ratios are exactly
(G1) for the three strict stem prefixes, not arbitrary new
coordinates of a full vector.

The existing construction texts associated with these actual
size-four and size-five roles have exact inherited metadata:

- RI41 NORMALIZATION.md, published path
  /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md,
  16243 bytes, SHA256
  567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8,
  inherited analytic metadata row dep_0419.
- RI63 COMPLETION.md, published path
  /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md,
  17102 bytes, SHA256
  e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122,
  inherited analytic metadata row dep_0412.

Only the existing metadata rows were read in this sitting, not
these two source bodies or their descendants. Naming them does
not admit them. Their construction roles are already described
in the admitted RI189 analytic text; it does not follow that
either note contains the missing quantitative witness.

A separately authorized source route would have to establish
the actual coefficient relations at exactly the roles above,
including the unchanged size-five canonical correction. It
must not infer values from component-key order, discard the
canonical term, assign a convenient empty ratio, decode a
scientific certificate by association, or treat a discovery
history as a theorem. No such source expansion or successor
has been started here.

## 7. Bounded disposition

New native deductions are all five complete disconnected full
profiles, the normalization cancellation for D3/D5, their exact
relative-row substitution, the three raising-slot identities,
the two-moment reduction (G8), and the proved root-sector
dependence for gamma,zeta and D1/D3.

This is a substantive profile deduction with an exact remaining
native witness gap, not acceptance of an improved family or a
proof of optimality. It remains conditional on the finite
baseline, H30 equivalence and inherited analytic premises.
It is not a full QM, geometric, gravitational or physical result.

No coefficient was evaluated, no amplitude selected, and no
scientific body/vector/certificate, H/z reconstruction, graph,
LP, automatic proof arithmetic, subject runtime, fixture/card,
repository/Git/index, measurement or RET work occurred. The
original quarter-amplitude rejection and the accepted positive
small-amplitude family are preserved. Stop for independent
review of this bounded result; root owns all further decisions.
