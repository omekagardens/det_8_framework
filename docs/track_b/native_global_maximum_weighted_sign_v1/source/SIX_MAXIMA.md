# Complete six maxima upper bound for the unchanged native law

30 September 2026, Honolulu. Manual theorem submitted for independent review.

Every marked six-event parent with six maxima is the six-antichain A6.
For all its 64 binary records and all 63 proper ideal occurrences,

    U6(A6,r_mark) < 2^36+7 = 68,719,476,743
                           < 69,000,000,000 < T.                (1)

The proof reuses RI185's accepted complete marked classification and
restoration-only proper A5 theorem. It bounds all six rows of the
accepted reduced potential table, retaining full complements and their
records. It does not restart that classification or evaluate a maximum,
canonical vector or actual scale.

The [global comparison and weighted consequence](GLOBAL_W.md) separately
combine this result with the accepted one-through-five-maxima classes.
Conditional on the same named inherited finite-prefix premises, they
give M6<463 billion<T and the exact RI199 consequence W(rho,s)>0.
Both individual margins, shared H30 and physical conclusions remain open.

## 1. Accepted inputs and the exact marked domain

A six-element order with six maxima has no comparabilities; hence it is
A6. RI185 has already proved that its proper ideals of sizes k=0,...,5
have multiplicities

    1,6,15,20,15,6,                  totaling 63.                (2)

Its seven record Hamming weights m=0,...,6 have multiplicities
1,6,15,20,15,6,1, totaling 64. This is simultaneous marked permutation
transport, not record-flip symmetry or a selected representative record.

For a selected k-element ideal containing j one-bits, write

    p_(n;k,j)=q_(A_n,r)(S),       |S|=k, |r|_S=j.

Proper locality forgets only marks outside S. At n=k the quantity is
FULL in its smaller parent, with the entire selected record retained.
For fixed m,k the number of labeled occurrences of selected weight j is

    N_(6,m;k,j)=binom(m,j)*binom(6-m,k-j),                        (3)

with max(0,k-(6-m))<=j<=min(k,m). Its sum over j is binom(6,k).
No record averaging replaces the complete row.

RI185 proved, using arbitrary-deletion defects and full marked ordinary
diamonds, that every proper A5 component has zero canonical boundary
coefficient. Thus for all k<=4 and all allowed j,

    p_(5;k,j)=theta*u_(5;k,j),
    theta=1/[72(1+M5)]>0.                                      (4)

This accepted theorem covers even k=3,4, where the terminal need not
have four maxima. The later four-terminal-maxima support lemma alone
would not justify those cases. We use the full RI185 A5 theorem, not
a weakened terminal-count argument.

All smaller probabilities remain those of the unchanged strictly positive
complete prefix. Actual size-four components, marks, full complements
and the empty-parent probability p_(0;0,0)=1 are retained.

## 2. Precise seed reconciliation and the small restoration scale

The literal accepted NORMALIZATION.md fixes the singleton row
(2/3,1/3), e=1/44, d=1/4, g=1/10, and k_seed=11/20.
Its three-antichain proper probabilities are

    p_(3;0,0)=e=1/44,
    p_(3;1,j)=e*g/d=1/110,
    p_(3;2,j)=e*k_seed/d=1/20.                                 (5)

These particular entries do not depend on j by the literal seed; that
does not make every other row record-independent. The complete proper
sum is

    1/44+3/110+3/20=(5+6+33)/220=1/5,

so the full three-antichain probability is p_(3;3,j)=4/5 for every j.
The singleton full entry is p_(1;1,j)=1/3, while its empty entry is 2/3.
These formulas are not a new scientific table lookup.

The earlier accepted native witness gives M5>5 billion, hence

    theta < 2^-38,                                             (6)

because 2^38=274,877,906,944<360,000,000,000=72*5 billion.
The unchanged same-law target is

    T=4lambda*j0/v-1/2
      >(468/5)(1+M5)-1/2>465,000,000,000.                       (7)

Neither the printed numerical M5 nor an evaluated theta is used.
All p_n numerator factors below are simply bounded by one, as entries
in genuine complete normalized rows.

## 3. Accepted complete reduced table

Within EACH row only, abbreviate p_(n;k,j) by p_n. Do not change
k or j within a product. The accepted RI185 reduced table is

| Selected size k | Labeled multiplicity | Exact reduced potential |
| --- | ---: | --- |
| 0 | 1 | theta^6 p4^15 p2^45 p0^5 / (p3^40 p1^24) |
| 1 | 6 | theta^5 p4^10 p2^15 / (p3^20 p1^4) |
| 2 | 15 | theta^4 p4^6 p2^3 / p3^8 |
| 3 | 20 | theta^3 p4^3 / p3^2 |
| 4 | 15 | theta^2 p4 full |
| 5 | 6 | j5(j), the full A5 complement |

Here p0^5=1 by the empty-parent boundary, not by an invented proper-slot
formula. At k=1,2,3,4 the bottom smaller-parent probability is full.
In particular p4 in the k=4 row is the actual full four-antichain entry,
not alpha*u4 at a full slot.

For clarity, this table is the accepted exact cancellation, not a new
row model. In the full maximal-deletion product a deletion of h omitted
maxima contributes exponent (-1)^(h+1)*binom(6-k,h). Substitution of
(4) into the proper p5 factors gives, for t=6-k>=2, the lower-factor
exponents

    (-1)^h (h-1) binom(t,h),      h=2,...,t,

and theta^t. No substitution of theta*u5 is made at k=5, where p5
is full. This identifies every factor being bounded while reusing
RI185's completed all-mark classification.

## 4. Bounds on all five proper-restoration rows

For k=0, (5) gives p3=1/44>1/64=2^-6 and p1=2/3>1/2.
Using (6), p0=1 and numerator probabilities at most one,

    u_(6;0,0) < 2^(-228) * 2^240 * 2^24 = 2^36.               (8)

The precise empty probability 1/44 is important. A generic 1/110
floor for every p3 would discard this available information and give
an unnecessarily weak empty-row bound.

For k=1, p3=1/110>1/128=2^-7 and the FULL singleton p1=1/3>1/4.
For every selected mark,

    u_(6;1,j) < 2^(-190) * 2^140 * 2^8 = 2^-42.               (9)

For k=2, p3=1/20>1/32=2^-5. The full p2 in the numerator remains
an actual probability at most one. Thus

    u_(6;2,j) < 2^(-152) * 2^40 = 2^-112.                     (10)

For k=3, the denominator is the FULL three-antichain probability
p3=4/5>1/2, not its empty probability. Consequently

    u_(6;3,j) < 2^(-114) * 2^2 = 2^-112.                      (11)

For k=4, p4 is FULL and is used only as a probability at most one:

    u_(6;4,j)=theta^2*p4 < 2^-76.                              (12)

All inequalities are strict because theta<2^-38. The bounds on the
fixed smaller denominators are also strict as displayed. Each original
record and every selected weight j remains in the domain; the size-four
numerators are not evaluated or made record-independent.

There are 6+15+20+15=56 occurrences in k=1,...,4. Each is below 2^-42.
Since 56<2^42, their COMPLETE contribution is strictly less than one.
This is a sum over all labeled ideals, not one term per orbit.

## 5. All six full complements retained

For an A5 record with weight m, RI185 defines the complete 31-term sum

    K5(m)=sum_(k=0,...,4) sum_j
             binom(m,j)binom(5-m,k-j) u_(5;k,j),
    j5(m)=1-theta*K5(m).                                      (13)

Every proper potential is positive. Complete strict normalization gives

    0<j5(m)<1,                 m=0,...,5.                       (14)

No equality between different j5(m) is assumed. In an A6 record of
weight m, the six full-complement occurrences contribute exactly

    6*j5(0)                         if m=0,
    (6-m)*j5(m)+m*j5(m-1)           if 1<=m<=5,
    6*j5(5)                         if m=6.                     (15)

The endpoints contain no undefined j5(-1) or j5(6). For every m,
(14)-(15) give a total strictly below six. There is NO additional
theta multiplier at these full slots.

## 6. Whole class conclusion and limits

The empty occurrence contributes less than 2^36 by (8), the other
56 non-full occurrences less than one by (9)-(12), and all six full
complements less than six. Thus the complete 63-term row satisfies

    U6(A6,r_mark)<2^36+7=68,719,476,743<69 billion<T              (16)

for every one of its 64 records. This proves the entire six-maxima
class. It is not an assertion that A6 attains the global M6 or that
a particular record maximizes its row.

RI185's earlier lower bound U6(A6,r_mark)>71/12+6theta remains valid.
The new upper bound does not alter that lower theorem, its strict
rho cap, its classification or any accepted source.

The new yield here is the uniform upper comparison (16), obtained
from the already accepted marked table. The [companion](GLOBAL_W.md)
performs the exhaustive global combination and separately checks the
weighted consequence. Both use the SAME selected law and named inherited
finite premises; neither is a new DET-native selection theorem, new
certificate verification, quantum reconstruction or physical prediction.

All proof arithmetic is manual. Exact sources and read scope are in
[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json); administrative checks
do not verify mathematics. No scientific body/vector/certificate,
automated proof arithmetic, subject/graph/LP/runtime/fixture/card work,
repository/Git/index or RET changes occur. Stop at the sealed handoff
for root independent review, publication and successor selection.
