# RI178 — increasing complete reference complements

30 September 2026. Manual coauthor proof for independent root review.
The two reference complements at the upper formal y boundary are strictly
increasing on the whole unchanged-law interval. This proof retains the
actual canonical singleton correction and all held ideal occurrences.
It requires neither a slope-regime comparison nor the sign of q'.

## 1. Same-law definitions and complete coefficients

Write the upper-boundary factors as

    F_2(x)=1-U20(x)/d(x),       F_3(x)=1-U30(x)/d(x),
    d(x)=6-4x+2x^2,
    0<x<=R<12/95<1/4.                                  (1)

F_2,F_3 here are reference-complement functions, not the earlier canonical
cap quantities F_i. This notation also avoids confusing the cubic
coefficient below with the local margin C2 or a reference complement.
The variable x is formal; the actual scale rho remains unchanged.

Use the complete four-stem sums over S=0,1,3,7, including the empty ideal:

    K_i=sum_S B_i(S)^2/A(S)+2c_i,
    T_i=sum_S B_i(S)^3/A(S)^2,
    h_i=theta*c_i,       m_i=theta^2*c_i=theta*h_i,
    j_i=1-theta*K_i,
    E_i=theta^3*T_i+3m_i+3j_i,
    V_i=theta^3*T_i+2m_i+j_i.                           (2)

The factor 2 in K_i retains the two distinct H5 one-cap ideals. They
have equal probabilities but remain two occurrences. Complete H5
normalization gives h_i+j_i<1, with all entries strictly positive.
No proper-slot locality shortcut is applied to a full complement.

The exact RI151 canonical correction, already substituted in RI173, is

    gamma=35/1476,
    N_i=gamma*[41p_i-f_i/2-min(g_(i,0),g_(i,1))]_+/c_i,
    omega_i=44theta*p_i,
    ell_i=1-theta-N_i>0.                               (3)

All entries in (3) are from the same fixed law. The minimum retains ties;
the positive part retains zero and its equality boundary. Neither N_0
nor N_1 is set to zero or chosen independently. The quantities f_i and
g_(i,u) are actual lower-prefix probabilities, not adjustable coefficients.

For the reference record, abbreviate h=h_0, m=m_0, j=j_0, N=N_0,
omega=omega_0 and V=V_0. The complete held-sum identities give

    U20(x)=3-A*x+B*x^2+C*x^3,
    A=E_0+2+2(1-theta)h+(1-2theta)j+2N(omega-1),
    B=2m+2j+ell_0,
    C=theta*(E_0-2m-3j)+N*theta*omega^2,
    U30(x)=2-x-x(1-x)V.                                (4)

These are RI145's complete coefficients with the canonical expression
(3) retained. In particular N contributes to all three coefficients in
(4), and its cubic contribution is a product rather than the square of
a contrast. There is no alternate zero-correction reference law.

## 2. A uniform envelope for the actual coefficients

The inherited complete-parent and canonical-cap proofs supply

    0<theta<1/144,       0<omega_i<1,
    71/24<E_i<3,        71/72<V_i<1,
    p_i<1/100,          c_i>1/14.                       (5)

The last two inequalities are uniform theorems about the accepted
prefix, not newly selected or evaluated probabilities. Their finite
certificate basis is explicit in RI157's cap proof. The stronger bounds
there are not needed for this derivative estimate.

Since f_i and both g_(i,u) are strictly positive, the positive part in
(3) is strictly less than 41p_i. This includes its zero branch because
p_i>0. Consequently

    0<=N_i<(35/36)*p_i/c_i<14p_i<7/50<1/4.            (6)

This inequality does not remove N from (4); it bounds its complete actual
contribution while preserving its correlations. On its zero branch the
strict upper comparisons remain valid. No actual positive-part branch or
record ordering is selected.

We now establish the deliberately coarse but sufficient bounds

    4<A<7,       0<B<4,       0<C<1.                  (7)

For the lower bound on A, the h and j terms in (4) are positive because
theta<1/144, and 2Nomega is nonnegative. Thus

    A>E_0+2-2N>71/24+3/2=107/24>4.                   (8)

For its upper bound, N>=0 and omega<1 make 2N(omega-1)<=0. Also
2h+j<2 follows from h+j<1 and positivity. Hence

    A<E_0+2+2h+j<7.                                   (9)

For B, all three terms in (4) are positive. Since m=theta*h<h,
ell_0<1 and h+j<1,

    0<B<2(h+j)+1<3<4.                                (10)

The sharper intermediate comparison B<3 is used only to justify the
chosen envelope, not as a changed coefficient. Finally (2) gives

    E_0-2m-3j=theta^3*T_0+m>0.

It is also smaller than E_0<3. With N<1/4 and omega<1,

    0<C<theta*(3+1/4)<13/576<1.                       (11)

Every strict lower bound remains valid at N=0 because the held stem sum
and m stay positive. Equations (7) are simultaneous bounds on the actual
coefficients, not an arbitrary-polynomial replacement for the fixed law.

## 3. Exact quotient derivatives and strictly positive numerators

For either j=2,3, differentiating the varying denominator is essential:

    F_j'(x)=[Uj0(x)*d'(x)-Uj0'(x)*d(x)]/d(x)^2,
    d'(x)=-4+4x.                                     (12)

The denominator is strictly positive. Direct expansion of the complete
cubic in (4), without dropping any canonical term, yields

    P_2(x):=U20*d'-U20'*d
       =6A-12+(12-12B)x+(-2A+4B-18C)x^2
          +8C*x^3-2C*x^4.                            (13)

For 0<x<=1/4, use A>4 in the constant term, B<4 in the linear term,
A<7 and C<1 in the quadratic term, and retain 4B*x^2 and 8C*x^3
as nonnegative contributions. These bounds give

    P_2(x)>12-36x-32x^2-2x^4
           >=12-9-2-1/128=127/128>0.                 (14)

The weak middle comparison only bounds powers of x by their positive
quarter-interval endpoints. Strictness already comes from (7); the
actual upper endpoint R<1/4 does not introduce an equality loophole.
The estimate is valid on the larger quarter interval for these fixed
coefficients, although only the assigned actual-containing interval is
used in the conclusion.

For the complete quadratic reference profile in (4), the separate exact
calculation is

    P_3(x):=U30*d'-U30'*d
       =-2+6V+(8-12V)x+(-2+2V)x^2.                  (15)

Because 71/72<V<1, its constant term exceeds 47/12, the linear
coefficient exceeds -4, and the quadratic coefficient exceeds -2.
Therefore

    P_3(x)>47/12-4x-2x^2
           >=47/12-1-1/8=67/24>0.                   (16)

Equations (12)--(16) prove both desired strict derivative signs.
In particular no claim that U20 or U30 decreases was substituted for
the quotient calculation: that alone would not control U/d when d
also decreases.

Since 0<d(x)<=6 on the assigned interval, the same proof gives explicit
uniform derivative lower bounds

    F_2'(x)>127/4608>0,
    F_3'(x)>67/864>0.                                 (17)

## 4. Boundary values and scope of the conclusion

The polynomials and positive denominator extend continuously to zero.
Their exact values there are U20(0)=3, U30(0)=2 and d(0)=6, so

    F_2(0)=1/2,       F_3(0)=2/3.

Integrating (17), or applying strict monotonicity from these continuous
limits, proves on the assigned positive-x interval

    F_2(x)>1/2+(127/4608)x>1/2,
    F_3(x)>2/3+(67/864)x>2/3.                          (18)

The zero comparison is a formal limiting endpoint, not an available
actual scale. The earlier complete reference bounds U20>7/4 and
U30>3/2 also retain F_2,F_3<1. Thus these strictly increasing factors
are positive and bounded; they are not new independent probabilities.

This proves a derivative property of the full upper-boundary factors.
It does not select the sign of the y-slope, compare v with any threshold,
or remove the signed canonical products in q. The companion proof may
combine it with RI175's separately accepted q>0 and q'<0 for the same
law to study the complete upper-y endpoint. The endpoint values, actual
W(rho,s), individual local margins, and shared-system feasibility do not
follow merely from increasing factors.

The inequalities (18) refer to the formal upper-y boundary y=1/d(x).
They are not a relabeling of RI127's distinct actual-baseline f_j0>1/2
premise, nor permission to choose the actual scales or alter support.
All records, the four distinct stem ideals and both H5 cap occurrences
remain in the construction.

## 5. Literal reading and diagnostic record

The exact RI178 assignment and RI175 predecessor decision in
`/Volumes/AI_DATA/development/det-review-evidence/ri177-root-intercept-review-va0vbeed`
were authenticated by `e4a847`,`a3313d` and read completely as `f8ff1a`,
all exit 0. Current literal mathematical reads were:

- `/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci/ENDPOINT_REDUCTION.md`, 16141 bytes, SHA256 `9b548f8a0cc912682c85f73f5a5f49a58d8a63d9daacbbb7156ffb1a65976a0d`: complete `086241`,`964a44`; equations (2),(3),(7)--(18) supply complete held sums, singleton terms, exact profiles and prior complement bounds.
- `/Volumes/AI_DATA/development/det-review-evidence/ri155-strict-capacity-proof-jv0xliup/CAPACITY_STRUCTURE.md`, 15579 bytes, SHA256 `54fa9b1e421520527a2403e20d0e243f257bdc8ef244e945200e4a652ab3d936`: complete `8dfac0`,`7e440a`; sections 5--6 supply complete normalization and E,V bounds.
- `/Volumes/AI_DATA/development/det-review-evidence/ri157-correlated-capacity-proof-tusjyk77/CANONICAL_CAP_BOUND.md`, 12849 bytes, SHA256 `abff2d8a473634532dc8690556a2ce828f80cde0ff1704068ec2445778462125`: complete `c596fb`; sections 2--4 give the explicitly inherited all-row finite margins, p,c bounds and full canonical correction, and section 5 fixes the cap branch without selecting rho.
- `/Volumes/AI_DATA/development/det-review-evidence/ri173-same-law-endpoint-slope-ckec5j02/CANONICAL_SLOPE.md`, 15263 bytes, SHA256 `81821c78fd0407db6d8d0523aa78641dfde6e34fd49aa7613295953c72ba9ac2`: complete `955d16`,`1d7d61`; equations (2),(6)--(8) collect the unchanged complete canonical profiles and all record distinctions.

Fresh four-file length/hash checks were `314c05`,`33a9c6`, both exit 0.
Every current read exited 0 without clipping; deliberate consecutive
ranges reached each file's end. Historical diagnostics printed inside
those manuscripts were read as history, not rerun or counted as current
failures. No new historical path or alias was needed.

Only this assigned Markdown is authored. No scientific body, coefficient
vector, actual probability, maximum or scale was decoded or evaluated.
No engine, subject/helper import, compile, AST, probe, fixture, runtime,
new agent, repository/index/Git operation or predecessor edit occurred.
This is coauthor work, not independent acceptance. Root owns adjudication.
RET stays paused; measurement and RI176 remain separate. Preserve P2/P3,
Y=1/4, all31/139/20/42, shared T1, other eight parents, all five Di,
strict endpoints and every labeled ideal occurrence.
