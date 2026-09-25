# RI-94 — amplitude persistence along the accepted harmonic direction

25 September 2026 UTC. **Source-only proof and fixed certificate design.**
This note extends the accepted [RI-91 obstruction](../native_growth_relative_obstruction_v1/RESULT_REVIEW.md)
in its amplitude parameter, not its support, parent/record catalogue or
continuation class. No new native polynomial coefficients are evaluated.

Two analytic conclusions already follow: the obstruction is not isolated
at epsilon=1/4, and its divided polynomials have the required analytic
bidegree bounds. Obstruction for **every** 0<epsilon<=1/4 is not established
here. One exact, nonadaptive bivariate sign test is specified for that
remaining question; neither its success nor a surviving native slice is
claimed.

## 1. Frozen family and inherited premises

Let H_j be the accepted RI-88 multiplier at amplitude 1/4, in the unchanged
eleven-class order of [RI-85](../native_growth_four_vertex_cap_v1/DESIGN.md).
Fix, without rescaling or choosing another null vector,

\[
 E=\tfrac14,\qquad z_j=4(H_j-1),\qquad
 h^\epsilon_7(T_j)=1+\epsilon z_j,\quad 0<\epsilon\leq E.
 \tag{1}
\]

Outside those eleven classes h7=1; through six births h=1. There is no
prescribed h8 and no reset of the multiplier above seven. The canonical
direction has z1=1, all eleven coordinates nonzero, and |z_j|<=1, by the
accepted H_j in [3/4,5/4]. Thus

\[
 h^\epsilon_7=(1-4\epsilon)\,1+4\epsilon\,h^E_7,\qquad
 3/4\leq h^\epsilon_7\leq5/4.
 \tag{2}
\]

The baseline B and its positive held prefix, including the actual mixed
q5, are fixed. Write rho=a6 for its unknown global half-scale. Change only
the six-parent seed rows by q6_epsilon=q6_B*h7_epsilon(child).
RI-88's complete harmonic equations are homogeneous and linear in z;
they therefore normalize every complete marked row for every amplitude
in (1), not just the six rows used below. Unsupported births, including
every full six-parent birth, remain unchanged.

Positive class-invariant multipliers preserve strict proper-precursor
record locality and marked equivariance. Both paths of each new
five-parent diamond acquire the same terminal h7_epsilon, so the entire
unnormalized scalar-passive payload map D/4 agrees, with inherited marks,
both fair newborn bits and equal precursors retained. These remain
conditional fair-record, scalar-passive model premises, not a derivation
of informative quantum growth from DET. The scalar D_r used below is
not the payload D.

On the same complete zero-record P1=C3 ordinal-sum A3 row as RI-88,

\[
 \mathbb E_\epsilon[w\mid P_1,0]-\mathbb E_B[w\mid P_1,0]
 =\epsilon\rho\,u_0>0,\qquad u_0=a_0g_0^3/b_0^3>0.
 \tag{3}
\]

This follows from the accepted width functional L(z)=u0. It sums all
eleven ideals and both newborn bits; it is not conditioned on proper
birth or support membership. The finite-width gain survives throughout
(1). It says nothing about sustained width or a geometric limit.

### The same continuation class, not all growth laws

For each amplitude use the complete positive common-level-scale RI-38
continuations of the two seeds. Their seven-parent proper probabilities
are s*u_B and t_epsilon*u_epsilon. The fixed baseline s=a7 is its unknown
global half-scale. The candidate t_epsilon is common to the entire level,
chosen before a current record; it may depend on the amplitude but not
on parent, record, ideal or payload. Both full complements must remain
strictly positive on the **complete** marked layer.

RI-89's untouched RI-79 contrast has two minimal vertices. Deleting any
maximum and adjoining the next maximal birth preserves those minima,
whereas every supported T_j has one. Hence its modified proper-potential
sum equals its baseline sum for every epsilon. The accepted nonzero
record contrast on that parent reduces the full-complement condition
to (s-t_epsilon)*Delta U=0. Therefore

\[
 t_\epsilon=s
 \tag{4}
\]

is necessary for a record-independent relative h8 at every amplitude.
Neither normalization alone nor equality of selected maxima proves (4);
the accepted RI-79 contrast and its uniform rho bound are load-bearing.
For two half-scale selectors, (4) would require equality of their complete
maxima; this note neither computes nor assumes that equality.

## 2. Parameterized full-complement criterion

Retain the [RI-89 theorem](../native_growth_relative_continuation_v1/CONTINUATION.md):
proper-birth relative weights are forced terminal products over maximal
deletions. Unique-maximal eight-event terminals instead have ratio

\[
 h^\epsilon_7(P)\,
 \frac{1-t_\epsilon V^\epsilon(P,r)}{1-sU(P,r)}.
 \tag{5}
\]

The numerator and denominator are positive under the complete-law
premises. A positive unmarked h8 exists in this continuation class iff
these full-complement ratios are record-independent for every parent
and record pair. Proper and full terminals are disjoint; neither
proper-birth factorization nor scalar normalization replaces (5).

After the necessary equality (4), put D_r=V_r^\epsilon-U_r. For any
selected pair r=0,1 the necessary condition is exactly

\[
 F(\rho,s,\epsilon)=D_1-D_0
       -s(D_1U_0-D_0U_1)=0.
 \tag{6}
\]

One pair with F nonzero rejects record-blindness. A zero of this pair
does not establish the full theorem, nor does it identify the actual
unknown baseline scales.

### No new numerical inputs

Freeze the same seven-parent and records:

\[
 P_\star=C_3\oplus A_4=(0,1,3,7,7,7,7),\qquad r=0,1.
 \tag{7}
\]

Only vertex 0 changes; all four cap marks remain zero. New polynomial
construction may use only the six complete RI-88 held rows below and
z1,z2,z3 from (1). The remaining eight h coordinates enter the inherited
whole-seed proof and provenance, not an enlarged coefficient calculation.

| Held order | Records | Individual ideal masks | Slots |
| --- | --- | --- | ---: |
| C3=(0,1,3) | 0,1 | 0,1,3,7 | 8 |
| C4=(0,1,3,7) | 0,1 | 0,1,3,7,15 | 10 |
| H5=(0,1,3,7,7) | 0,1 | 0,1,3,7,15,23,31 | 14 |

Use A_r(S), B_r(S), G_r(S) for these held probabilities on the four C3
ideals. Set a_r=A_r(7), b_r=B_r(7), g_r=G_r(7),
c_r=q_C4,r(15), h_r=q_H5,r(15)=q_H5,r(23), j_r=q_H5,r(31).
The lower-case held h_r is not a multiplier. Retain positive denominators,
complete row normalization, and RI-85's unique-top/twin-top transport
lemmas; no additional record erasure is assumed.

Define, symbolically from those entries,

\[
 E_r=\sum_{S=0,1,3,7}\frac{A_r(S)G_r(S)^3}{B_r(S)^3}
            +3h_r^2/c_r+3j_r,\qquad
 K_r=\sum_{S=0,1,3,7}\frac{A_r(S)^3G_r(S)^6}{B_r(S)^8},
 \tag{8}
\]
\[
 p_r=a_r^3g_r^6/b_r^8,\qquad v_r=h_r^3/c_r^2,
\]
\[
 U_r(\rho)=4-4\rho E_r+6\rho^2j_r+4\rho^3v_r+\rho^4K_r.
 \tag{9}
\]

E without a record subscript is the amplitude ceiling 1/4, not E_r.

The eighteen proper ideals have the unchanged RI-89 multiplicities:
four stem ideals, four one-cap ideals, six two-cap ideals and four
three-cap ideals. Their multipliers are respectively 1 except
(1+epsilon*z1)^4 at stem ideal 7, then (1+epsilon*z2)^3,
(1+epsilon*z3)^2, and 1. Thus

\[
 \begin{split}
 D_r(\rho,\epsilon)={}&
 \rho^4p_r[(1+\epsilon z_1)^4-1]\\
 &+4\rho^3v_r[(1+\epsilon z_2)^3-1]
 +6\rho^2j_r[(1+\epsilon z_3)^2-1].
 \end{split}
 \tag{10}
\]

These are symbolic substitutions in an accepted identity, not evaluations
of new native coefficients. Individual labeled ideals and repeated
isomorphic deletion factors retain their multiplicities.

## 3. Exact division and analytic bidegrees

For m=2,3,4 define the polynomial

\[
 L_m(z,\epsilon)=
 \sum_{k=1}^{m}\binom{m}{k}z^k\epsilon^{k-1}.
 \tag{11}
\]

The polynomial identity epsilon*L_m=(1+epsilon*z)^m-1 follows directly
from the binomial theorem, including at zero. No rational function with
an unhandled epsilon=0 pole is introduced. In particular,

\[
 L_2=2z+\epsilon z^2,\quad
 L_3=3z+3\epsilon z^2+\epsilon^2z^3,\quad
 L_4=4z+6\epsilon z^2+4\epsilon^2z^3+\epsilon^3z^4.
\]
\[
 D_r=\epsilon\rho^2d_r,\qquad
 d_r=\rho^2p_rL_4(z_1,\epsilon)
           +4\rho v_rL_3(z_2,\epsilon)+6j_rL_2(z_3,\epsilon).
 \tag{12}
\]

Define the divided quantities, distinct from RI-91's undivided A,C,G:

\[
 A=d_1-d_0,\quad C=d_1U_0-d_0U_1,\quad
 G_i=2(1+U_i)A-C\quad(i=0,1).
 \tag{13}
\]
\[
 F=\epsilon\rho^2(A-sC).
 \tag{14}
\]

All are polynomials over the rational field generated by the fixed held
entries and z; those entries are rational and their denominators positive.
Equation (12) proves divisibility by the **fixed** epsilon*rho^2.
A later verifier must also confirm every forbidden raw coefficient is
exactly zero before dividing; it must not infer a valuation from sampled
values or discard other factors.

| Expression | Analytic upper bidegree (rho,epsilon) |
| --- | --- |
| U_i | (4,0) |
| D_i | (4,4), with fixed factor epsilon*rho^2 |
| d_i and A | (2,3) |
| C and both G_i | (6,3) |

These follow by addition and multiplication in (9), (12), (13), not by
fitting signs, inspecting highest nonzero evaluated coefficients, or
assuming cancellations. Pad missing coefficients by exact zeros.

On the admitted domain epsilon*rho^2>0, so (14) preserves both signs and
zeros. At epsilon=0 the seed is baseline and F is identically zero;
with t=s the continuation is baseline too. At rho=0 the raw F also
vanishes. Values of the divided polynomials on either excluded axis
are algebraic extensions, not nonzero physical obstructions at that
axis. There is no claim of a positive raw margin through epsilon=0.

## 4. The baseline domain and full endpoint reduction

The rigorous outer domain is unchanged:

\[
 R=\frac1{2(1+\max(E_0,E_1))},\quad
 b_i(\rho)=\frac1{2(1+U_i(\rho))},\quad b=\min(b_0,b_1),
\]
\[
 0<\rho\leq R,\qquad 0<\epsilon\leq E,\qquad 0<s\leq b(\rho).
 \tag{15}
\]

R and U_i depend only on the fixed baseline, not epsilon. Selected E_i
and U_i are bounded by their respective complete baseline row maxima;
therefore (15) contains the actual unknown half-scales. It does not set
a6, a7, M6 or M7 equal to selected-row bounds. Since rho*E_i<1/2,
all selected baseline proper factors are positive, including
1-rho*E_i>1/2. Hence U_i>0 and 1-sU_i>1/2 throughout (15).

The modified law still has to satisfy its complete positivity premises.
The larger outer domain need not enforce all those premises. Rejecting
F on the outer domain suffices for every actual admissible candidate;
an outer-domain zero would not establish an admissible continuation.

For a binding i with b=b_i, let lambda=s/b in (0,1]. Then

\[
 A-sC=(1-\lambda)A
             +\lambda\,\frac{G_i}{2(1+U_i)}.
 \tag{16}
\]

Consequently A>=0 and **both** G_i>0 throughout the half-open
(rho,epsilon) rectangle imply F>0 throughout (15).
A is allowed to vanish because s=0 is excluded. Endpoint strictness
is required because the binding upper s endpoint is included. Checking
both G_i is the fixed conservative sufficient rule, not a necessary
condition for F to have a sign. No amplitude-dependent switching,
subdivision or alternative endpoint criterion follows from failure.

## 5. What can already be proved without new coefficients

### Obstruction is not an isolated epsilon=1/4 effect

Let the seventeen rho-Bernstein coordinate functions of (13) use the
same interval [0,R] and degrees 2,6,6 as RI-91, while keeping epsilon
formal. Each is a rational polynomial in epsilon of degree at most three.
At epsilon=E, E*z_j+1=H_j, so each function equals four times its
corresponding accepted RI-91 coordinate.

RI-91's complete independent reconstruction proved **all seventeen**
coordinates strictly positive. Continuity of finitely many polynomials
therefore supplies some delta with 0<delta<E such that they are all
positive for E-delta<=epsilon<=E. The same Bernstein and affine arguments
prove F>0 on (15) throughout this amplitude interval. Together with
(4), this rejects every admissible common-level-scale record-blind
continuation there.

This is an existence theorem for a nontrivial amplitude interval, not
an evaluated delta or a full-interval result. It uses a positive margin
among finitely many normalized Bernstein coordinates; the raw F need
not have a positive uniform lower bound as rho, epsilon or s approach
their excluded boundaries.

### A uniform small-rho consequence, not a scale choice

Put kappa=(j1-j0)*z3. From (12) and U0(0)=U1(0)=4,

\[
 A(0,\epsilon)=6\kappa(2+\epsilon z_3),\qquad
 G_0(0,\epsilon)=G_1(0,\epsilon)=6A(0,\epsilon).
 \tag{17}
\]

The strictly positive first RI-91 A/rho^2 Bernstein coordinate is its
value at rho=0. The slice identity above and
2+E*z3>=7/4 imply kappa>0, without calculating kappa.
Since |z3|<=1, all three polynomials in (17) are strictly positive
uniformly for epsilon in [0,E]. Uniform continuity on the compact
rectangle [0,R] times [0,E] gives some eta>0, eta<=R, for which they
remain positive on [0,eta] times [0,E]. Thus F>0 for every positive
amplitude in this **small-rho subdomain** and every admitted positive s.

The actual unknown rho has not been shown to lie below eta. Neither
eta nor a new scale is computed or selected. This result does not
settle the rest of the fixed rectangle or assign a sign to the raw
F at epsilon=0 or rho=0.

### Remaining question

Endpoint positivity, the small-rho conclusion and normalization do
not decide all coefficient signs over the full rectangle. No native
amplitude slice surviving the complete record-independence criterion
has been identified. The following fixed test addresses this remaining
question; failure of that sufficient test would not identify such a slice.

## 6. One frozen exact bivariate Bernstein test

Set x=rho/R and y=epsilon/E, so the admitted rectangle is (0,1]^2.
Use tensor degree (m,n)=(2,3) for A and (6,3) for each G_i.
For a polynomial Q with padded ordinary coefficients c_ab, define

\[
 Q(\rho,\epsilon)=\sum_{a=0}^{m}\sum_{b=0}^{3}
                         c_{ab}\rho^a\epsilon^b,
\]
\[
 \beta_{ij}=\sum_{a=0}^{i}\sum_{b=0}^{j}
 c_{ab}R^aE^b
 \frac{\binom{i}{a}}{\binom{m}{a}}
 \frac{\binom{j}{b}}{\binom{3}{b}},
 \quad 0\leq i\leq m,\quad0\leq j\leq3.
 \tag{18}
\]

Then Q(Rx,Ey)=sum beta_ij B_i^m(x) B_j^3(y), where
B_i^m(x)=binom(m,i)*x^i*(1-x)^(m-i).
The exact identity follows by applying the univariate monomial-to-
Bernstein identity in each variable. There are exactly 12+28+28=68
coordinates across the three fixed grids. No degree elevation, fitting,
adaptive valuation, interval split or tolerance is authorized.

**Independent reverse identity.** Expand the binomial basis factors
directly, without inverting or calling the forward conversion. For every
a=0,...,m and b=0,...,3, require

\[
 c_{ab}R^aE^b=
 \sum_{i=0}^{a}\sum_{j=0}^{b}
 \beta_{ij}\binom{m}{i}\binom{m-i}{a-i}
             \binom{3}{j}\binom{3-j}{b-j}
             (-1)^{a-i+b-j}.
 \tag{19}
\]

Compare the full scaled power grid first, then divide by R^a E^b to
recover and compare the original grid. These are different arrays;
do not repeat a scaled/unscaled reverse-comparison mistake.
R,E are fixed positive rationals, so this division is legitimate.
Zero padding, axis order and every entry are part of the certificate.

### Weak A, strict included G corner

The positive certificate requires all 68 coordinates nonnegative,
and for each G_i its corner coordinate beta_(6,3) strictly positive.
No strict condition is required on A's coordinates.

All basis products are nonnegative on [0,1]^2. The single corner term
gives G_i(Rx,Ey)>=beta_(6,3)*x^6*y^3>0 whenever x,y>0.
This includes both upper edges and their corner; the excluded lower
and left edges may vanish. Conversely, within the nonnegative-coefficient
class, strict positivity at the included corner requires beta_(6,3)>0,
since it is the value there. Requiring every coefficient or every
excluded-axis value to be strictly positive would be unnecessary.
The criterion is sufficient, not necessary among arbitrary positive
polynomials.

### Mandatory RI-91 slice reconciliation and native outcomes

At y=1 only the last Bernstein column remains. The seventeen entries
beta_(i,3) must agree coefficientwise with four times the accepted
RI-91 univariate coordinates, with the same R and degrees. The identity
comes from E*z_j+1=H_j and (10)--(13); it must also be retained as an
exact reconstruction check in any future certificate. RI-88 remains
the construction input. RI-91's authenticated saved witness is the
fixed boundary-regression reference, not a replacement for rebuilding
the parameterized polynomials from RI-88.

All seventeen last-column entries must be strictly positive. A conflict
with this accepted boundary, a nonzero discarded coefficient, or a
failed reverse identity is a reconstruction/input refusal, **not** a
new mathematical disposition. In particular, a negative-sign whole
family or an identically zero whole pair would contradict the anchor.
The native test therefore fixes positive orientation only, with exactly
two mathematical outcomes after all identity checks pass:

1. **certified-positive-amplitude-obstruction:** every weak/strict
   requirement above passes. With (4), the entire interval in (1) is
   excluded for this record-blind common-level-scale continuation class.
2. **unresolved-fixed-bivariate-bernstein:** at least one required
   coefficient is negative. Retain every failing index and exact value
   in fixed order A,G0,G1, then increasing rho index, then epsilon index.
   No root, sign change, surviving amplitude or invalid growth law follows.

With the mandatory strict last-column anchor, there is no admissible
native corner-zero branch. Generic corner-zero, negative and blind
synthetic cases below exercise the algebraic test separately; they
cannot be reported as outcomes for the authenticated anchored family.

For interpretation only, at a specified (rho,epsilon) the divided pair
equation is s=A/C if C is nonzero; A=C=0 makes this pair blind, and
C=0 with A nonzero admits no root. Any candidate additionally needs
0<s<=b, actual complete-law positivity and all other parent/record
conditions. This is a symbolic criterion, not authorization for a
root solver, amplitude search, endpoint scan or numerical scale choice.

## 7. Minimal justified certificate and adversarial design

A later implementation requires separate coordinator review and admission.
This note supplies no executor, execution manifest or certificate body.
The bounded evidence must retain:

1. Authenticated, unchanged RI-88 bytes and the exact six-row/32-slot
   inventory, H1,H2,H3 and z_j=4(H_j-1), with source/theorem provenance.
   Authenticate the accepted RI-91 boundary witness and rebuild the
   epsilon=E slice; do not substitute its signs for parametric arithmetic.
2. Both exact polynomial routes: (8)--(13), and the independent RI-91
   individual-deletion construction with formal epsilon multipliers.
   Preserve 20 lower slots/80 factors and 36 upper slots/220 factors,
   all signs, labeled multiplicities and order/ideal/record transports.
   Reconstruct the lower E_r independently before using 1-rho*E_r.
3. All raw U,V,D and cross-difference coefficients, forbidden-coefficient
   zero checks, fixed-factor quotients and analytic-degree checks.
   Only accepted positive held constants appear in denominators;
   no negative epsilon or rho powers may survive reconstruction.
4. Exact R definition, fixed half-open domains, all 68 ordinary/scaled/
   Bernstein/reverse coefficients, both endpoint identities, all seventeen
   slice comparisons, and the complete deterministic outcome evidence.
5. Strict schemas/types, reduced rational encodings, immutable source/input
   pins, saved complete-byte reconstruction and an independently written
   exact consumer. Replaying one producer is not independent arithmetic.

A 68-entry sign flag is not sufficient without these identity and
provenance checks. Independent deletion/transport and reverse algebra,
not merely a different polynomial storage representation, are required.

### Synthetic tests, not native computations or laws

Freeze x=rho/R, y=epsilon/E with synthetic R=1, E=1/4. For the first
eight fixtures use U0=1,U1=3 and set

\[
 d_0=(A-C)/2,\qquad d_1=(3A-C)/2.
 \tag{20}
\]

Then (13) holds exactly, G0=4A-C and G1=8A-C, and the binding s bound
is 1/8. The listed toy polynomials respect the bidegree bounds; they
are algebra fixtures, not an alternative DET seed or native evidence.

| Fixture | A,C | Required interpretation |
| --- | --- | --- |
| Positive | 1,0 | Positive sign test passes |
| Negative orientation | -1,0 | Positive test refuses; generic reversed sign passes, never a native anchored result |
| Weak A / excluded s=0 | 0,-1 | Pass: A-sC=s>0 for positive s |
| Blind pair | 0,0 | Generic blind identity, not global continuation or a native anchored result |
| Included binding s endpoint | 1,8 | Refuse strictness: a root occurs at s=1/8 |
| Conservative two-endpoint refusal | 1,6 | Unresolved although A-sC>0 for all allowed s; G0 is negative |
| Positive but mixed basis | (y-1/2)^2+1/16,0 | Unresolved despite everywhere-positive A; amplitude coordinates are 5/16,-1/48,-1/48,5/16 |
| Endpoint positive, interior zero | (2y-1)^2,0 | Refuse; positive y=1 slice alone cannot exclude the y=1/2 zero |

A ninth, algebraically compatible strict-support fixture uses
U0=1, U1=1+x^4 and d0=d1=x^2*y^3. It gives
A=0, C=-x^6*y^3 and G0=G1=x^6*y^3.
Only the (6,3) corner coefficient is positive; all other G coefficients
are zero, yet both G are strictly positive on (0,1]^2. It exercises the
excluded-axis boundaries without requiring false strictness there.

Polynomial-only reverse/boundary fixtures also include G=1-x and G=1-y
(each zero on an included edge and therefore refused), and distinct
rho/epsilon monomials of unequal exponents to detect swapped axes,
incorrect R/E powers, dropped padded entries and incorrect reverse
division. These are not claims of whole growth-law realizability.

Intended-reason mutations must reject omitted epsilon or rho factors,
nonzero raw coefficients below the fixed valuation, degrees exceeding
(2,3)/(6,3), changed amplitude ceiling or interval endpoints, noncanonical
rationals or boolean indices, incorrect z extraction or support order,
missing held/full slots, merged ideal multiplicities, wrong transports,
unjustified record erasure, incorrect R from selected rows, missing
G endpoint or full-complement term, a zero included corner passed as
strict, incorrect slice factor four, incomplete saved grids and forged
outcomes. An input/code/resource failure is not an unresolved mathematical
result. No fixtures or refusal controls are executed in this packet.

## 8. Provenance, conclusions and stop boundary

Load-bearing accepted identities are:

- RI-88 CERTIFICATE.json: 1,828,149 bytes,
  SHA-256 ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b.
- RI-89 CONTINUATION.md: 21,769 bytes,
  SHA-256 56c45bb5aba5e9fa0ab1f09ff959a73235939cc850e6fdde91a4cc39180b5cd1.
- RI-91 accepted witness: 364,312 bytes,
  SHA-256 9e48c437e90cbeef6284ddbcdf5ec915aa520217172f580ef900e5c2bccd37ed.
- RI-91 independent report: 131,331 bytes,
  SHA-256 e5521806e4b8cde0e206962b6cb3d5468835278542e6caedba77a87995d1c5a7.
- RI-91 root result adjudication: 3,604 bytes,
  SHA-256 97e92a700198c1640107ba08d8062e7090c2075d169d72179a6c8e1d65963350.

The first three are retained in the corresponding research directories.
The independent report is at
/Volumes/AI_DATA/development/det-review-evidence/ri91-certificate-audit-order-repair-hhd7z0qb/audit-01/REPORT.json;
the adjudication is at
/Volumes/AI_DATA/development/det-review-evidence/ri91-result-checkpoint-1jhq26yx/RI91_ROOT_RESULT_ADJUDICATION.json.
RI-79's contrast, RI-85's transport and support closure, and RI-38's
conditional growth theorem remain inherited proof premises, not rerun
calculations or new DET axioms.

Established here: the amplitude family retains its positive normalized
finite prefix and finite width gain; record-blind continuation still
requires t=s; fixed epsilon*rho^2 division and bidegrees are justified;
and the accepted obstruction persists near epsilon=1/4. The separate
small-rho conclusion does not locate the actual scale. The full positive
amplitude interval remains unresolved pending the fixed exact test.

Failure of that future sufficient test would not refute RI-91, produce
a surviving complete h8, or invalidate the individual RI-38 laws.
Success would reject this amplitude family only in the specified
relative record-blind common-level-scale class. Neither outcome supplies
an all-size harmonic weight, persistent width improvement, informative
quantum coupling, Lorentzian geometry, mass or gravity. The known
half-scale height-density obstruction, Option B, Status M and RET pause
are unchanged.

The sole reserved change is this AMPLITUDE.md. No actual new native
polynomial coefficients, global maxima, scales or probability tables
were computed; no supplied target source was imported, compiled or
executed. Accepted sources, historical failed evidence, RI-93 measurement
work and coordinator records remain untouched. Git/index, publication,
admission and next-step assignment remain coordinator-owned. Completing
this bounded proof/design handoff does not end the overall programme.
