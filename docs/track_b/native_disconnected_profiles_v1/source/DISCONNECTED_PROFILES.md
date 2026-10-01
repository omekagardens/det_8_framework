# Complete disconnected full profiles for the shared mobility equations

30 September 2026, Honolulu. RI225 manual conditional derivation for
independent review. This note derives all five full profiles needed in
RI223 N16 from the complete fixed-support deletion identities. It does
not provide a solution or an inconsistency identity for N16-N17.

The result is an explicit reduction to the already admitted connected
held rows and two smaller disconnected orders. Neither a new probability
table nor independent row variables are introduced. All coefficients
below belong to the unchanged actual baseline, with its fixed rho and s.

## 1. Notation and the two smaller disconnected orders

Write I=C3, H=I ordinal-sum A2, and let o be an isolated vertex. The
five connected six-parent catalogue entries remain P1,...,P5 in RI85
order; D_i=P_i disjoint {o}. In particular P3=F(H), P5=F(C5), where
F appends a unique vertex above the whole order.

For a stem ideal S in the four-element list

    J={empty, initial singleton, initial pair, I},

write A_S=q(I,S), B_S=q(C4,S), G_S=q(H,S), D_S=q(C5,S).
The inherited held full/upper slots are

    a=A_I, b=B_I, c=q(C4,C4),
    g=G_I, h=q(H,I plus either cap),
    j=q(H,H), e=q(C5,C4), ell=q(C5,C5),
    m=h^2/c, nu=h^3/c^2.

D_S is a held probability, not a parent D_i. Records are suppressed in
notation only: each factor has the induced order, precursor and marking.
Retain every original marking, including C5's nonmaximal marks unless
a previously proved identity removes its dependence.

The two new symbolic lower orders are

    K=I disjoint {o},            Y=C4 disjoint {o}.

These are K4 and K5 by size, not new allowed scientific data reads.
For S in J define

    k_S=q(K,S),              y_S=q(Y,S),
    k_S^+=q(K,S union {o}),  y_S^+=q(Y,S union {o}),
    F_Y=q(Y,Y).

All are actual strictly positive probabilities. In particular k_I^+
is a full K probability. A full factor retains its complete induced
record before the maximal-record invariance theorem is applied.

One further lower equality is needed:

    q(Y,C4)=h.                                               (P1)

Indeed the complete empty/full diamond based at C4 gives
q(Y,C4)=c*e_C5/e_C4. The accepted empty identity e_C5=theta*e_C4
and h=theta*c prove (P1). It holds for every transported record
and both fair newborn bits. It is not an assumption that unrelated
full profiles coincide.

Use the following formal sums, each with its four individual S terms:

    M2 = sum_S (y_S^+)^2/k_S^+,
    M3 = sum_S (y_S^+)^3/(k_S^+)^2,

    V_H = sum_S A_S*G_S*y_S^2/(B_S^2*k_S) + 2m+j,
    V_C = sum_S D_S*y_S/B_S + e*h/c+ell,

    R1 = sum_S A_S^3*G_S^3*y_S^3/(B_S^6*k_S^2),
    R2 = sum_S A_S*D_S*G_S*y_S^2/(B_S^3*k_S)
                                       +e*h^2/c^2,
    R4 = sum_S D_S^2*y_S/B_S^2 + e^2*h/c^2,

    P_Y = 1-sum_S y_S-h,
    X = V_H+2F_Y+M2,
    Z = V_C+P_Y.                                             (P2)

P_Y is positive: it is the sum of all five Y probabilities whose
precursors contain o, including F_Y. X and Z will be the complete
proper-potential sums of H disjoint {o} and C5 disjoint {o}.
They are not free parameters.

The existing connected six-parent sums are

    E1=sum_S A_S*G_S^3/B_S^3+3m+3j,
    E2=sum_S D_S*G_S/B_S+e*h/c+h+j+ell,
    E4=sum_S D_S^2/B_S+e^2/c+2ell.                            (P3)

Thus q(P_i,P_i)=1-rho*E_i for i=1,2,4. The full probabilities
of P3 and P5 are 1-rho, by unique-maximum deletion and complete
normalization. All denominators used here are positive.

## 2. The five full profile identities

Let B_i be the complete proper-potential sum at D_i. The proposed
new identities are

    B1=4-rho*(E1+3X)+3rho^2*(j+F_Y)
                          +rho^3*(3nu+M3)+rho^4*R1,

    B2=3-rho*(E2+X+Z-F_Y)
                +rho^2*(m+j+ell+F_Y+M2)+rho^3*R2,

    B3=2-rho-rho*(1-rho)*V_H,

    B4=3-rho*(E4+2Z)+rho^2*(2ell+P_Y)+rho^3*R4,

    B5=2-rho-rho*(1-rho)*V_C,

    g_i(r)=1-s*B_i(r),             i=1,...,5.                (P4)

Here B_i is not the held C4 probability B_S. The subscripts and
arguments distinguish them. Equations (P4) use the baseline's common
size-seven scale only on proper ideals, then its normalized full
complement; no such scale property is imposed on a repaired law.

Sections 3-6 derive all proper terms. The lists comprise respectively
21,17,15,15,13 proper ideals. Together with five full ideals there are
86 individual ideals, twice the accepted 43 six-parent ideals.

## 3. Complete lower normalization and the unique-maximum pair

Put X6=H disjoint {o}, Z6=C5 disjoint {o}. For X6, the ideals excluding
o have the following proper potentials:

    S in J:      A_S*G_S*y_S^2/(B_S^2*k_S),
    I plus a:    m,
    I plus b:    m,
    H:           j.                                        (P5)

For the first line the omitted maxima are the two H caps and o.
The three singleton-deletion factors are G_S,y_S,y_S;
the double factors are B_S,B_S,k_S; the triple factor is A_S.
Their alternating product is exactly (P5). At a one-cap ideal the
two singleton factors are h,h and the double factor c, by (P1).
At H only o is omitted.

The ideals containing o, except the full X6, are

    S union {o}, S in J:    (y_S^+)^2/k_S^+,
    I plus a plus o:        F_Y,
    I plus b plus o:        F_Y.                             (P6)

The first line has two omitted caps; the two Y factors and one K
factor retain S and o. Each remaining line omits one cap and leaves
the full Y factor. These seven plus six proper ideals are complete.
Multiplying their sum by rho gives the complete proper mass of X6,
so its full probability is 1-rho*X with X from (P2).

For Z6, deleting its two maxima (the C5 tip and o) gives:

    S in J, excluding o:    D_S*y_S/B_S,
    C4, excluding o:        e*h/c,
    C5, excluding o:        ell,
    S union {o}, S in J:    y_S^+,
    C4 union {o}:           F_Y.                             (P7)

The last five terms sum to P_Y by the complete Y row, not by erasing
those terms. The first six sum to V_C. Hence the complete proper
potential is Z=V_C+P_Y, and the full probability is 1-rho*Z.
There is no unexpanded Z6 full-profile input left.

More generally take A=H or C5 and C=F(A). In C, each ideal S of A has
probability rho*q(A,S), and its full probability is 1-rho. The maxima
of C disjoint {o} are the new top of C and o. Its proper potentials are

    S subset A:        rho*q(A disjoint {o},S),
    C:                 1-rho,
    S union {o}:       q(A disjoint {o},S union {o}),
                                          S any ideal of A. (P8)

The two-maxima product cancels q(A,S) in the first line; the other
lines omit only one maximum. Both copies of every ideal of A are
retained, except the final full C disjoint {o}.

Let N_A=sum_{S ideal A}q(A disjoint {o},S). Complete normalization
makes the last-line sum 1-N_A. Thus the total proper potential is

    2-rho-(1-rho)*N_A.

Equations (P5),(P7) give N_H=rho*V_H and N_C5=rho*V_C.
This proves B3 and B5 in (P4), without requiring either disconnected
six-parent full probability as an independent source.

## 4. Every proper ideal at D1

Label the three P1 caps a,b,c. Every one is above I; o is incomparable
to the whole connected component. Proper ideals excluding o are:

| Precursor | Separate occurrences | Potential per occurrence |
| --- | --- | --- |
| Each S in J | empty, initial singleton, initial pair, I | rho^4*A_S^3*G_S^3*y_S^3/(B_S^6*k_S^2) |
| I plus one cap | a; b; c | rho^3*nu |
| I plus two caps | ab; ac; bc | rho^2*j |
| P1 | abc | 1-rho*E1 |

For a stem S all four maxima are omitted. The singleton factors are
q(P1,S) and three q(X6,S); double factors are three G_S and three y_S;
triple factors are three B_S and one k_S; the fourfold factor is A_S.
Substitute q(P1,S)=rho*A_S*G_S^3/B_S^3 and (P5). Their full alternating
product is the first table entry.

For a one-cap ideal, the three singleton factors are rho*m three times,
the three double factors are h three times, and the triple factor is c.
Thus the product is rho^3*m^3*c/h^3=rho^3*nu. A two-cap ideal has two
rho*j singleton factors and the full H factor j, giving rho^2*j.
The last row omits only o.

The proper ideals containing o are:

| Precursor | Separate occurrences | Potential per occurrence |
| --- | --- | --- |
| S union {o}, each S in J | all four S | rho^3*(y_S^+)^3/(k_S^+)^2 |
| I plus one cap plus o | a; b; c | rho^2*F_Y |
| I plus two caps plus o | ab; ac; bc | 1-rho*X |

For S union {o}, the three singleton factors are
rho*(y_S^+)^2/k_S^+, the three double factors are y_S^+, and the
triple factor is k_S^+. A one-cap ideal has two rho*F_Y factors
and one F_Y denominator; a two-cap ideal is a full X6 factor.

There are eleven no-o and ten with-o terms. Summing these two tables,
not their orbit representatives, gives exactly B1 in (P4).
In particular the no-o two-cap contribution is 3rho^2*j, NOT 3rho*j.

## 5. Every proper ideal at D2

Label the P2 cap a,b,c with a<c and b incomparable to a,c.
The maxima of D2 are b,c,o. Deleting b leaves Z6, deleting c
leaves X6 and deleting o leaves P2. The double deletions leave
Y, C5 and H; the triple deletion leaves C4.

The complete no-o list is:

| Precursor | Separate occurrences | Potential |
| --- | --- | --- |
| Each S in J | all four S | rho^3*A_S*D_S*G_S*y_S^2/(B_S^3*k_S) |
| I+a | one | rho^3*e*h^2/c^2 |
| I+b | one | rho^2*m |
| I+a+b | one | rho^2*j |
| I+a+c | one | rho^2*ell |
| P2 | one | 1-rho*E2 |

For S in J, the singleton factors are rho*D_S*G_S/B_S,
rho*D_S*y_S/B_S and rho*A_S*G_S*y_S^2/(B_S^2*k_S);
the double factors are D_S,G_S,y_S and the triple factor B_S.
For I+a the singleton factors are rho*e*h/c twice and rho*m;
the doubles are e,h,h and the triple is c. These give the stated
two three-maxima products. Each next line omits two maxima and
cancels one full H or C5 factor. The last omits only o.

The complete with-o list is:

| Precursor | Separate occurrences | Potential |
| --- | --- | --- |
| S union {o}, each S in J | all four S | rho^2*(y_S^+)^2/k_S^+ |
| I+a+o | one | rho^2*F_Y |
| I+b+o | one | rho*F_Y |
| I+a+b+o | one | 1-rho*X |
| I+a+c+o | one | 1-rho*Z |

In the first line the Z6 factor rho*y_S^+ and X6 factor
rho*(y_S^+)^2/k_S^+ are divided by y_S^+. For I+a+o,
two rho*F_Y factors are divided by F_Y. The I+b+o ideal omits
only c and its X6 probability is rho*F_Y. The final two rows
are full X6 and Z6 factors, respectively.

Nine no-o plus eight with-o terms give B2 in (P4). The unequal
rho powers on I+a+o and I+b+o must not be merged.

## 6. Every proper ideal at D4 and the exact labelled domain

P4=C4 ordinal-sum A2, with cap maxima b,c above the four-chain.
For its D4, every ideal S of that C4 (five separate S) excluding o
has potential

    rho^3*q(C5,S)^2*q(Y,S)/q(C4,S)^2.

This follows from singleton factors rho*q(C5,S)^2/q(C4,S),
rho*q(C5,S)*q(Y,S)/q(C4,S) twice, double factors
q(C5,S) twice and q(Y,S), and triple factor q(C4,S).
For S=C4, the term is rho^3*e^2*h/c^2 by (P1).

The two no-o one-cap ideals each give rho^2*ell; P4 gives
1-rho*E4. For the five S union {o} ideals the two Z6 factors
rho*q(Y,S union {o}) are divided by q(Y,S union {o}), leaving
rho^2*q(Y,S union {o}). Their sum is rho^2*P_Y. The two
C4-plus-one-cap-plus-o ideals give 1-rho*Z each. These eight
no-o and seven with-o terms prove B4.

For a literal original-label check, the complete six-parent ideal
mask lists are unchanged:

    P1: 0,1,3,7,15,23,31,39,47,55,63
    P2: 0,1,3,7,15,23,31,47,63
    P3: 0,1,3,7,15,23,31,63
    P4: 0,1,3,7,15,31,47,63
    P5: 0,1,3,7,15,31,63.

Give o label6. For each line the D_i no-o ideals are exactly that
list, INCLUDING63. Its with-o proper ideals are exactly each listed
mask plus64 EXCEPT127. The only full ideal is127. This specifies
each original ideal occurrence without a new graph enumeration.
It also checks the pair counts for (P8), where P3 and P5 have
respectively eight and seven no-o ideals.

## 7. Full record transport and use in the mobility equations

Each deletion restricts the original order, precursor and marking
together. Any relabeling transports all three by the same map;
an abstract o does not remain at a fixed numerical bit position in
K,Y,X6 or Z6. Repeated caps correspond to separate ideals and
separate restriction maps, even when probabilities then coincide.

Maximal-record invariance justifies independence from the bit on o
and from appropriate maxima of each smaller factor. It does not
remove nonmaximal marks. For full factors normalization is applied
to the complete induced row. The sums in (P2) must not be evaluated
at separately selected markings. These arguments establish (P4)
on all five original 128-mark cubes and their equivariant copies;
whole scalar payload maps inherit the equality for each fair
newborn bit, not after averaging.

Write l_i=L_i/rho, retaining the five linear forms of RI127 RESULT
equation12. For a reference r0, every original disconnected
homogeneous equation is now exactly

    (1-s*B_i(r0))*Delta_r l_i(W)
                  +s*Delta_r B_i*l_i(r0;W)=0,  i=1,...,5.   (P9)

The sign of the second term follows from g_i=1-s*B_i.
No division by a contrast, a correction, or an unproved pivot occurs.

If a_ij is the coefficient of W_j in l_i, the actual coefficient
in RI223 N15 is

    H_ij(r)=rho*[(1-s*B_i(r0))*Delta_r a_ij
                                +s*a_ij(r0)*Delta_r B_i].   (P10)

Thus (P4) is a native symbolic full-profile reduction of the
required relative coefficients, not a replacement by independent
H_ij variables. The unchanged connected contrasts N17 and the
recovery of every correction N11-N12 remain mandatory.

For D3 and D5 in particular, put V_i=V_H,V_C respectively. Then

    g_i=1-s*(2-rho)+s*rho*(1-rho)*V_i,
    g_i(r0)*Delta l_i
            -s*rho*(1-rho)*Delta V_i*l_i(r0;W)=0.            (P11)

The complete common factors and constant intercept remain in (P11).
A variation of g_i alone still does not force its correction to zero.

## 8. Source and result boundary

The derivation uses the admitted RI85 maximal-deletion product and
full individual ideal catalogue, RI103 complete empty diamonds and
maximal-record theorem, RI117 connected complete-normalization
identities, RI127 held transport identities, and the accepted
RI223 empty identity e_C5=theta*e_C4. The separately admitted
RI111 REPAIR restates the complete shared disconnected system but
does NOT supply the lower K/Y profiles or a normalized witness.
Its old 28-column restrictions are not applied to the current H30.

No scientific body, table, coefficient vector or certificate was
read, parsed or evaluated. All formulas above were derived manually.
K/Y variables name actual fixed probabilities; they are not new
chosen inputs, independent fitting parameters, or an assertion that
those values are determined by normalization alone.

The companion [LOWER_PROFILE_GAP.md](LOWER_PROFILE_GAP.md) reduces
this remaining lower dependence further and states the precise gap.
Actual normalized mobility, ceiling improvement and optimality are
still undecided. Original amplitude1/4 rejection and the accepted
small-amplitude family remain unchanged. No successor is opened.
