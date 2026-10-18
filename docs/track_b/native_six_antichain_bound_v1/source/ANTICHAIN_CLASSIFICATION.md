# RI185 — complete marked antichain row and restoration proof

30 September 2026. Manual coauthor proof, submitted for independent review.
All 63 proper ideals and all 64 binary records of A6 are covered below.
The required A5 law is proved restoration-only at every proper slot;
its six Hamming-weight classes of full complements are retained by complete
normalization.
No numerical law table, component value or scientific body is inspected.

## 1. All ideal and record occurrences

Let A(B) be the antichain on a labeled set B. Every subset S of B is an
ideal. For |B|=6 the proper cardinality classes are

| k=card(S) | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Distinct proper ideals | 1 | 6 | 15 | 20 | 15 | 6 |

Their sum is 63; the one excluded ideal is B itself. The 5-element
ideals are six distinct subsets, not one orbit-weighted occurrence.
For A5, the proper counts are 1,5,10,10,5 at k=0,...,4, totaling 31.
Empty ideals occur once in both rows.

The full permutation group of the antichain transports parent, ideal and
all records simultaneously. Its binary-record orbits for A6 are the
seven Hamming weights m=0,...,6, with multiplicities

    1,6,15,20,15,6,1,                                (1)

which sum to 64. For A5 the corresponding six orbit sizes are
1,5,10,10,5,1, summing to 32. These are exact permutation orbits, not
an assumption of record-flip symmetry or equality across weights.

In an m-one-bit row, the number of k-element selected ideals containing
j one-bits is

    N_(n,m;k,j)=binom(m,j)*binom(n-m,k-j).              (2)

Only indices with max(0,k-(n-m))<=j<=min(k,m) are used. Summing (2)
over j gives binom(n,k), so all labeled occurrences remain in the row.
No averaging over parent or precursor marks replaces these counts.

## 2. Precisely retained smaller-law quantities

For 0<=k<=n and 0<=j<=k write

    p_(n;k,j)=q_{A_n,r}(S),       |S|=k, |r|_S=j.      (3)

When n>k, this is well defined because strict proper locality removes
only marks outside S, and equivariance identifies antichain presentations
with the same selected marked subset type. When n=k it is a full-parent
probability: j is then the entire parent's Hamming weight. Equivariance
still justifies (3), but no full-slot record independence is assumed.
In particular p_(k;k,j) may vary with j.

Every p in (3) is the unchanged positive law. The size-four entries retain
their actual component coefficients, not a common replacement. The empty
parent has just its full empty ideal and total scalar probability one:

    p_(0;0,0)=1.                                     (4)

This boundary value is not an extension of a proper-slot formula to n=0.
The separate fair newborn-mark factor is not included in p; the accepted
whole-map diamonds have matching such factors on both routes.

For a proper S of A_n with k=|S|, the omitted maxima are exactly B\S.
The accepted maximal-deletion formula, with every restricted record, is

    u_(n;k,j)= product_{h=1}^{n-k}
         p_(n-h;k,j)^[(-1)^(h+1)*binom(n-k,h)].        (5)

Before grouping, (5) is a product over every nonempty deleted subset H
of B\S. Equal factors at the same |H| follow from proper locality and
simultaneous permutation transport, not from ignoring selected marks.
The final factor n-h=k is full on S and retains all j selected one-bits.
All denominators are strictly positive. In particular the empty-parent
factor at k=0 is retained before (4) simplifies it.

## 3. Arbitrary-deletion defects and every A5 proper component

A nonempty Ferrers cell order has a unique least cell. Therefore the
largest Ferrers induced suborder of A_n has one vertex, and

    defect(A5)=4,       defect(A6)=5.                 (6)

Consider A_n plus an apex z whose predecessors are a nonempty subset S
of the old antichain. Any induced suborder with at least three vertices
contains at least two old vertices. Both are minimal and incomparable:
no old vertex has a predecessor, and the only new relations point from
old vertices to z. That suborder has no least vertex and cannot be
Ferrers. Conversely one selected old vertex together with z is a
two-chain, hence Ferrers. The largest Ferrers subset is exactly two.
This reasoning quantifies over arbitrary retained subsets, not just
maximal or ideal deletions. It proves

    defect(A5+z_S)=4,
    defect(A4+z_S)=3       whenever S is nonempty.     (7)

An empty birth at A5 produces A6, so by (6) its proper role raises defect.
For every nonempty proper S of A5, choose an omitted old vertex d outside
S. Deleting d leaves the four-antichain base A4. Its two precursors are
S and the empty ideal. On one route, the empty birth d gives A5 and
then the S birth gives A5+z_S. On the other, the S birth gives
Q=A4+z_S, and the empty birth d gives the identical terminal order.
By (6)--(7),

    A5 -> A5+z_S is neutral: 4 -> 4,
    Q  -> Q+isolated d is raising: 3 -> 4.            (8)

This is an ordinary ratio-graph diamond, not merely a shared unmarked
terminal. All four old base bits and both newborn bits are independently
variable, and the two routes transport d's and z's separate records to
the same final carrier. Thus every one of the 32 A5 records, every
nonempty proper S, and both newborn bits is covered. When |S|=4 the
first S is full in the base A4; the inherited complete diamond domain
includes that case. Its two new-layer roles remain proper. For S empty
the direct raising argument already applies, including all-zero records.

RI63's accepted finite theorem says every positive canonical component
is everywhere defect-neutral. Each component incident to an A5 proper
slot has just been shown to contain a raising role, either directly or
through (8). Its canonical boundary coefficient is therefore zero.
The actual unchanged mixture gives, for every proper antichain slot,

    p_(5;k,j)=theta*u_(5;k,j),       0<=k<=4,
    theta=c5/36=1/[72(1+M5)]>0.                      (9)

This proves restoration-only rather than assuming neutral roles have no
correction. The theorem is specific to these incident components. It does
not delete the canonical singleton correction N from other parent-five
laws or alter the size-four component vector.

## 4. Complete 31-slot A5 normalization

For a fixed selected type (k,j), abbreviate p_(n;k,j) by p_n within
each row of the next table. Indices k,j are not changed within a product.
Equation (5) gives every proper A5 potential as follows:

| k | Number in each A5 row | Complete potential u_(5;k,j) |
| --- | ---: | --- |
| 0 | 1 | p4^5 p2^10 p0 / (p3^10 p1^5) |
| 1 | 5 | p4^4 p2^4 / (p3^6 p1) |
| 2 | 10 | p4^3 p2 / p3^3 |
| 3 | 10 | p4^2 / p3 |
| 4 | 5 | p4 (full) |

The last lower-law factor p_k in each row is full, even when it appears
in a denominator. The k=0 row alone includes p0=1. No proper/full
identification is inferred from sharing the symbol p.

For an A5 record with m one-bits define its complete sum and full complement

    K_5(m)=sum_{k=0}^{4} sum over admissible j
              N_(5,m;k,j)*u_(5;k,j),
    j_5(m)=p_(5;5,m)=1-theta*K_5(m).                 (10)

Thus all 31 proper occurrences determine the full probability. We do not
assert that different j_5(m) are equal. Full-record dependence is retained
through the actual lower probabilities and the complete multiplicities.
The inputs needed by (10) are the antichain laws at sizes zero through
four, including their full slots. No size-five scientific body is needed.

## 5. All 63 A6 parity products and exact cancellation

Continue the same per-row abbreviation p_n=p_(n;k,j). Before using (9),
the full six-parent deletion table is

| k | Number | Raw parity product u_(6;k,j) |
| --- | ---: | --- |
| 0 | 1 | p5^6 p3^20 p1^6 / (p4^15 p2^15 p0) |
| 1 | 6 | p5^5 p3^10 p1 / (p4^10 p2^5) |
| 2 | 15 | p5^4 p3^4 / (p4^6 p2) |
| 3 | 20 | p5^3 p3 / p4^3 |
| 4 | 15 | p5^2 / p4 |
| 5 | 6 | p5 (full) |

For k<=4 let t=6-k>=2. Each p5 factor is then proper and can be
replaced by theta*u5. A lower factor p_(6-h), h=2,...,t, receives its
original parity exponent and the contribution from all t replaced p5
factors. Its total exponent is exactly

    (-1)^h*[t*binom(t-1,h-1)-binom(t,h)]
      =(-1)^h*(h-1)*binom(t,h),                      (11)

using t*binom(t-1,h-1)=h*binom(t,h). Consequently

    u_(6;k,j)=theta^t product_{h=2}^{t}
       p_(6-h;k,j)^[(-1)^h*(h-1)*binom(t,h)]          (12)

for k<=4. No p5 full factor is replaced by this formula. Written out,
the exact reduced table is

| k | Reduced potential |
| --- | --- |
| 0 | theta^6 p4^15 p2^45 p0^5 / (p3^40 p1^24) |
| 1 | theta^5 p4^10 p2^15 / (p3^20 p1^4) |
| 2 | theta^4 p4^6 p2^3 / p3^8 |
| 3 | theta^3 p4^3 / p3^2 |
| 4 | theta^2 p4 (full) |
| 5 | j_5(j), the full complement from (10) |

In the k=0 row p0^5=1 only by the empty-parent boundary (4).
For k=1,2,3,4 the bottom p_k remains the full smaller probability
with all selected marks. These formulas do not pretend that proper
locality removes a full-parent record.

The complete marked six-parent sum is therefore

    U_6(m)=sum_{k=0}^{5} sum over admissible j
                 N_(6,m;k,j)*u_(6;k,j).              (13)

Equations (1)--(3),(10),(12)--(13) cover every original record and every
proper ideal by proved transport and exact integer multiplicity. The
six full-complement terms can also be displayed separately:

    m=0:     6*j_5(0),
    1<=m<=5: (6-m)*j_5(m)+m*j_5(m-1),
    m=6:     6*j_5(5).                               (14)

The endpoint cases avoid undefined j_5(-1) or j_5(6); they are not
written as zero times an undefined value. The other 57 potentials in
(13) are all strictly positive and all remain in the exact sum.

## 6. Uniform consequence, without an attaining-record claim

Every K_5(m) is a complete unscaled marked parent-five sum in the actual
definition of M5, hence K_5(m)<=M5. The unchanged dependence of theta
on M5 gives

    j_5(m)>=1-theta*M5=71/72+theta.                  (15)

Combining all six occurrences in (14) with the 57 positive terms proves

    U_6(m)>71/12+6theta       for every m=0,...,6.    (16)

The inequality is strict even if every used K_5(m) equals M5. It neither
asserts equal full complements nor identifies the maximizing A6 record
or the global maximizing six-parent. The companion cap proof compares
this guaranteed bound with RI181 and carries only the proved cap into
the unchanged weighted endpoint test. No actual endpoint sign follows
from (16) alone. Nor does the stronger guaranteed bound prove that the
actual complete A6 sum exceeds every actual four-cap sum.

## 7. Sources, diagnostics and stopping boundary

The RI185 assignment was authenticated as `82f7c1`,`b5a0c0` and read
completely as `023c93`. The RI181 decision was authenticated with the
source identities in `5e59b8`,`3714ee`, then fully read as `0b0fee`.
All exited 0.

The only fresh historical mathematical reads were the already selected:

- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`, 16243 bytes, SHA256 `567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8`; complete `f2cc00`,`f5db45`. It fixes strict proper locality, full-record allowance, equivariance, every marked diamond and the maximal-deletion formula, with individual labeled slots retained.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`, 17102 bytes, SHA256 `e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122`; complete `605e4b`,`b6fb3a`,`0b508b`. It supplies the exhaustive everywhere-neutral active-component theorem, arbitrary-vertex defect, complete base-four diamond domain, strict mixture and actual M5 definition.

Fresh byte/hash checks `5e59b8`,`3714ee` matched the inherited exact pins.
All current calls succeeded with complete, unclipped displays. No failed
read or new historical path/alias was needed. Printed historical executions
and certificate values were read as historical text, not rerun, decoded
or substituted as evaluated scientific operands.

Only this assigned Markdown is authored. No scientific JSON/vector/body,
actual coefficient or scale evaluation, engine, source/helper import,
compile, AST, probe, run, fixture, runtime/card/admission, new agent,
repository/index/Git operation or predecessor edit occurred. This is
coauthor work, not independent acceptance. RET remains paused; measurement
and RI184 remain separate. Preserve P2/P3,Y=1/4,all31/139/20/42,shared T1,
other eight parents,five Di,strict endpoints and every labeled ideal.
Root owns independent adjudication and any successor.
