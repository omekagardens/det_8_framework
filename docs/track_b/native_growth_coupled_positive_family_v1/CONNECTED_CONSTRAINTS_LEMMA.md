# RI117 connected-parent reduction: T2 and T3

26 September 2026. Manual analytic source work only; no new native coefficient,
H/z, q6/q7, scale, solver, fixture or runtime evaluation.

## 1. Scope and accepted premises

This note retains RI111's fixed actual baseline B, the accepted eleven-class
seed z with z1=1, amplitude 1/4, and precisely its 28-child support. It
does not fix w1 to its local witness zero. All sixteen parent obligations
remain required.

Sources read for this reduction:

- RI111 complete REPAIR.md, especially (22) and (23), at
  /Volumes/AI_DATA/development/det-review-evidence/ri111-one-column-repair-HRfi3z/REPAIR.md.
- RI103 complete REPAIR.md at
  /Volumes/AI_DATA/development/det-review-evidence/ri103-full-birth-repair-QakuEg/REPAIR.md.
- RI85 DESIGN.md, sections 1–5, at
  /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_four_vertex_cap_v1/DESIGN.md.
- RI102 AMPLITUDE.md, sections 1–5, at
  /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_fixed_amplitude_lift_v1/AMPLITUDE.md.
- The RI109, RI95 and RI94 result/proof notes and relevant RI41/RI63
  definitions were consulted, but no certificate bodies were decoded.

The following are accepted model premises, not new DET axioms: strict
positivity, normalized complete rows, full binary record cubes, fair
independent newborn marks, strict precursor-record locality, marked
equivariance, and complete scalar-passive whole-map diamonds. Let rho=a6
and s=a7 be the actual unchanged global half-scales. In particular
0<rho<1/2 and s>0; neither is calculated or selected.

The maximal-record invariance lemma of RI103 is used only where its
hypotheses hold. A factor order, its precursor and all retained records
are transported together on deletion. No existing record is physically
removed by this mathematical operation.

## 2. Held notation

For xi=0,...,7 and eta=xi+8 sigma, sigma in {0,1}, write

    A_xi(S)=q_B(C3,xi,S),
    B_xi(S)=q_B(C4,xi,S),
    G_xi(S)=q_B(H5,xi,S),
    D_eta(S)=q_B(C5,eta,S),

where H5=C3 ordinal-sum A2 and S ranges over the four stem ideals
0,1,3,7. The top mark of each chain and both H5 cap marks are set to
zero in these representatives by the already proved transport lemmas.
C5's lower added-chain mark sigma is retained.

Write

    c_xi=q_B(C4,xi,15),
    h_xi=q_B(H5,xi,15)=q_B(H5,xi,23),
    j_xi=q_B(H5,xi,31),
    e_eta=q_B(C5,eta,15),
    ell_eta=q_B(C5,eta,31),
    m_xi=h_xi^2/c_xi.

The notation ell distinguishes a held C5 full probability from the
seven-parent profiles f2 and f3 below. Every denominator is positive.

Define held symbolic expressions

    E_xi = sum_S A_xi(S) G_xi(S)^3 / B_xi(S)^3 + 3 m_xi + 3 j_xi,
    V_xi = sum_S A_xi(S) G_xi(S)^3 / B_xi(S)^3 + 2 m_xi + j_xi
         = E_xi - m_xi - 2 j_xi,

    E2_eta = sum_S D_eta(S) G_xi(S) / B_xi(S)
             + e_eta h_xi/c_xi + h_xi + j_xi + ell_eta,

    C2_eta = sum_S A_xi(S) G_xi(S)^3 D_eta(S) / B_xi(S)^4
             + e_eta h_xi^2/c_xi^2.

The sum always includes all four stem ideals individually.
E is the complete proper-potential sum of K=C3 ordinal-sum A3.
E2 is the complete proper-potential sum of
C2=C3 ordinal-sum (C2 disjoint A1), where indexed C2 is RI85's
six-parent catalogue entry and unindexed C2 denotes a two-chain.
C2_eta in the final line is only a named expression, not an order.

Indeed the four stem potentials at that six-parent are D G/B.
Its other four proper ideals have potentials e h/c, h, j, ell,
respectively. The excluded full ideal has complement 1-rho E2.
At K the four stem potentials are A G^3/B^3, its three one-cap
potentials are m, and its three two-cap potentials are j. The full
complement is 1-rho E.

## 3. Exact T3 full profile and complete sensitivity criterion

Label the four cap vertices of T3 by a,b,c,d, with a<d and b<d,
and c isolated within the cap. All four lie above the C3 stem I.
The maxima are c,d. Deleting c yields V6=F(H5), a six-parent with a
unique maximum. Deleting d yields K. Deleting both yields H5.

For every ideal S of H5, its proper probability in V6 is
rho q_B(H5,S): deleting the unique maximum leaves exactly that factor.
The complete H5 row sums to one, so V6's full complement is 1-rho.
The two-maxima deletion identity at T3 therefore gives

    u_T3(S) = q_K(S) q_V6(S) / q_H5(S) = rho q_K(S)

for all seven ideals S contained in H5. For an ideal of K containing c,
the only omitted maximum is d, hence u_T3(S)=q_K(S). The remaining
proper ideal is V6 itself, of potential 1-rho.

For explicit completeness the twelve individual proper ideals have:

| Precursor | Multiplicity | Potential per ideal |
|---|---:|---|
| Stem ideals 0,1,3,7 | four individual ideals | rho^2 A G^3/B^3 |
| I+a; I+b | 2 | rho^2 m |
| I+a+b | 1 | rho^2 j |
| I+c | 1 | rho m |
| I+a+c; I+b+c | 2 | rho j |
| K=I+a+b+c | 1 | 1-rho E |
| V6=I+a+b+d | 1 | 1-rho |

No orbit division occurs. The full ideal of T3 is not in this table.
Summing gives the exact identity

    U3(xi;rho) = 2-rho-rho(1-rho)V_xi,
    f3(xi) = 1-s U3(xi;rho).

Only the stem records remain: the retained K rows ignore their cap
maxima, and V6's proper row is inherited from the complete H5 row,
which ignores both cap marks. This proves transport to the complete
128-mark T3 cube, not only equality on a chosen record pair.

For any xi,xi0,

    f3(xi)-f3(xi0) = s rho(1-rho)(V_xi-V_xi0).

Because the prefactor is strictly positive, f3 is record-constant
if and only if V_xi=V_0 for every xi=0,...,7. A single proved
nonzero contrast of V suffices to force, by RI111(22),

    w3=z3 and v3=0.

Neither nonconstant j nor nonconstant E alone proves a contrast of
V=E-m-2j. The new cancellation condition must be checked or proved;
this note does not declare it nonzero from those unrelated contrasts.

## 4. Exact T2 full profile and complete sensitivity criterion

Label T2's cap a,b,c,d with a<d and b,c isolated within the cap.
Its maxima are b,c,d. Its ideal count is 3*2*2+3=15 including the full
ideal: three stem-prefix ideals, then twelve cap ideals containing I.
There are fourteen proper ideals.

Deleting d yields K. Deleting b or c yields the six-parent C2.
Deleting d together with b or c yields H5. Deleting b,c yields C5.
Deleting all three maxima yields C4. Those are all the deletion
factors needed, with their inherited records transported.

| Precursor | Multiplicity | Potential per ideal |
|---|---:|---|
| Stem ideals 0,1,3,7 | four individual ideals | rho^3 A G^3 D/B^4 |
| I+a | 1 | rho^3 e h^2/c^2 |
| I+b; I+c | 2 | rho^2 m |
| I+a+b; I+a+c | 2 | rho^2 j |
| I+b+c | 1 | rho j |
| K=I+a+b+c | 1 | 1-rho E |
| C5=I+a+d | 1 | rho^2 ell |
| I+a+d+b; I+a+d+c | 2 | 1-rho E2 |

Here e,ell,D use eta and all remaining held terms use xi.
For example, the first table line is the three-maxima product

    (rho A G^3/B^3) (rho D G/B)^2 B / (D G^2)
      = rho^3 A G^3 D/B^4.

For I+a, the same product is

    (rho h^2/c) (rho e h/c)^2 c / (e h^2)
      = rho^3 e h^2/c^2.

For I+b one omits d,c. Their singleton factors are rho m and rho h,
and their double-deletion factor is h, giving rho^2 m.
For I+a+b those factors are rho j, rho j and j, giving rho^2 j.
For I+a+d they are rho ell, rho ell and ell, giving rho^2 ell.
The one-omitted-maximum entries are the stated six-parent probabilities.
This verifies all fourteen ideals, including the three full-six-parent
factors. Marked equivariance interchanges b,c but does not erase a's mark.

The complete proper sum is consequently

    U2(eta;rho)
      = 3-rho(E_xi+2 E2_eta-j_xi)
          +rho^2(2 m_xi+2 j_xi+ell_eta)+rho^3 C2_eta,
    f2(eta) = 1-s U2(eta;rho).

Only the three stem marks and sigma on a remain. This follows term
by term from the transported held rows and maximal-record invariance;
all sixteen eta and hence the complete 128-mark T2 cube are covered.

Put

    A2_eta=E_xi+2 E2_eta-j_xi,
    B2_eta=2 m_xi+2 j_xi+ell_eta,
    Q2_eta(x)=-(A2_eta-A2_0)
                 +x(B2_eta-B2_0)+x^2(C2_eta-C2_0).

Then

    f2(eta)-f2(0) = -s rho Q2_eta(rho).

Thus f2 is record-constant if and only if all fifteen Q2_eta vanish
at the actual rho. Proving one Q2_eta(rho) nonzero forces

    w2=z2 and v2=0.

An identically nonzero polynomial is not by itself proof of that
nonzero value: it may vanish at the actual unknown rational scale.
No root is substituted as a selected baseline scale.

For an optional internal simplification, comparing sigma=0,1 at
fixed xi gives Delta ell=-Delta e by the complete C5 row and locality
of its four stem slots. Hence

    Delta U2
      = rho [2-rho-2 h/c+rho^2 h^2/c^2] Delta e.

This exact identity proves no actual sensitivity without a justified
nonzero Delta e and nonzero bracket. In particular record-read
permission is not evidence that Delta e differs from zero.

## 5. A short sufficient rejection, but no unjustified promotion

RI102(23) supplies the strict, fixed-seed disjunction

    e_T2+z2/4<0 OR e_T3+z3/4<0.

It concerns the signed lift's unchanged J2/J3 multipliers and was
proved from a complete normalized row; no H/z arithmetic is needed
to reuse it. It is independent of a new choice of w1.

If both nonconstancy criteria above are proved, RI111(22) forces
w2=z2 and w3=z3. The strict child requirements wj>-4e_Tj then
contradict that accepted disjunction. This would reject the entire
fixed 28-child support, regardless of all other variables.

The contrapositive is already a rigorous necessary condition for a
positive repair:

    f2 constant OR f3 constant.

A sharper statement is that every index j in {2,3} satisfying the
accepted strict inequality e_Tj+zj/4<0 must have a constant f_j.
The disjunction does not identify which index fails, so proving
nonconstancy of only one unselected index is insufficient.

No accepted statement read for this note proves either new
nonconstancy condition. The signs Delta p<0 and Delta E>0 and the
root-free T1 pivot concern different expressions. A new numerical
evaluation of V or Q2 has not been performed here.

## 6. Exact unresolved domain, not execution authority

The full connected T2/T3 criteria use only the already retained
RI88 domain: eight complete C3 rows (32 slots), eight complete C4
rows (40 slots), sixteen complete C5 rows (96 slots), and eight
complete H5 rows (56 slots): forty rows and 224 slots. No new
unmarked shape or q6/q7 table is needed.

For a fixed sufficient *pair* rejection attempt using records 0,1
on both T2 and T3, the exact complete held domain is eight rows and
44 slots: two complete rows of each of C3,C4,C5,H5. This adds only
the two C5 rows (twelve slots) to the preceding six-row/32-slot
T1 pivot domain. It is sufficient only if it proves both

    V1-V0 != 0,
    Q2_1(rho) != 0 at the actual unchanged rho.

A root exclusion on the already justified outer interval (0,R]
would suffice for the second assertion; a surviving root would not
choose rho or settle the full family. These are precise conditional
obstructions, not proposals to execute a new certificate in this sitting.
This pair domain is a justified sufficient domain, not a global
information-theoretic minimum. A zero pair is not a proof of constancy.

If neither rejection is established, the exact connected conditions remain

    (z2-w2) Q2_eta(rho)=0 for every eta,
    (z3-w3) (V_xi-V_0)=0 for every xi,
    -4 e_Tj < wj < zj+4 f_j(0)  (j=2,3),
    vj=(zj-wj)/f_j(0).

They must be intersected with the complete D1 system in shared
w1,w2,w3, not fitted independently at one record. The T1 local
interval retains free w1. T4,...,T11 and D2,...,D5 are twelve other
parent obligations and remain exactly RI111(22),(23). No full
positive extension is inferred from this reduction.

The constant-profile counterexamples T8 and T11 remain unchanged.
No blanket full-profile sensitivity, old v1-positive premise,
all-size growth theorem, native geometry or physical correspondence
is claimed.

