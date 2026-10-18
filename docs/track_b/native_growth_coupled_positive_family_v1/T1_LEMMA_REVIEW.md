# RI-117 — exact conditional T1 positive family

26 September 2026. Independent manual analytic contribution by the T1-lemma
reviewer. This note proves the local consequence of the accepted RI-115 result;
it does not adjudicate the complete 28-child extension.

## 1. Premises and scope

Keep the RI-111 fixed actual baseline B, the same eleven-class seed, epsilon
= 1/4, the same 28 child classes, the complete record cubes, and all sixteen
incoming parents. The actual scales rho and s are strictly positive and fixed,
with 0 < rho <= R. No scale is chosen or evaluated here.

Write f_xi = f_1(xi) and k_xi as in RI-111 (4), for all eight stem markings
xi = 0,...,7. The proof uses the following accepted facts:

1. Every coefficient of each of the six polynomials M_xi is zero (RI-115).
2. The saved signs are Delta_1 p < 0 and P_1(0) < 0. These are the
   saved-data review's signs, reported and endorsed in the accepted result
   review; this note does not recompute them.
3. P_1 is continuous and has no zero on (0,R], and is the same pivot
   identified in RI-111 (15).
4. Actual baseline probabilities k_0, f_0 and e = e_T1 are strictly positive.
5. With K = C3 ordinal-sum A3, D1 = K disjoint A1, and I = C3,
   R_xi = q_B(K,xi,I)/e_K > 41, for every complete stem marking.
   The baseline D1 row is strictly positive and normalized.
6. The exact RI-111 identities and empty-birth whole-map diamond hold, with
   each ideal counted individually and all inherited marks transported.

The result is conditional on those baseline/model premises. It is neither a
derivation of the premises from DET nor a statement about arbitrary artificial
choices of scales in an outer interval.

## 2. Sign lemma at the actual baseline

P_1(0) < 0, continuity and absence of a root on (0,R] imply P_1(x) < 0
throughout [0,R]. Indeed a nonnegative value anywhere in (0,R] would give a
zero there, either at that point or by the intermediate value theorem.
Consequently

    beta = rho^3 Delta_1 p / P_1(rho) > 0.

The denominator is nonzero by the accepted pivot result. Actual baseline
positivity then gives

    Gamma = k_0 + beta f_0 > 0.

Only the pivot's sign is asserted throughout the outer interval. Positivity
of k_0, f_0 and Gamma is used at the actual baseline; no claim is made that
every artificially substituted (rho,s) defines a positive baseline.

## 3. Complete all-record affine family, both directions

The T1 equations are

    w + k_xi t + f_xi v = 1,       xi = 0,...,7.

RI-111 gives

    k_xi - k_0 = s rho^4 Delta_xi p,
    f_xi - f_0 = -s rho P_xi(rho).

Subtracting row zero and dividing only by the positive s rho yields

    rho^3 Delta_xi p t - P_xi(rho) v = 0.

The xi = 1 pivot forces v = beta t. Row zero then forces w = 1 - Gamma t.
These implications also hold when t = 0; no division by t has occurred.

Conversely, all six accepted zero minors give, for xi = 2,...,7,

    Delta_xi p P_1(rho) = Delta_1 p P_xi(rho),

and hence rho^3 Delta_xi p = beta P_xi(rho). The same identity holds
for xi = 1 by beta's definition and for xi = 0 trivially. Thus

    k_xi + beta f_xi = k_0 + beta f_0 = Gamma

for every one of the eight records. Substitution proves that every member

    (w,t,v) = (1 - Gamma t, t, beta t)

satisfies all eight original equations. This is the entire affine solution
line, not a fit to two selected rows and not a replacement of eight records
by an assumed parity quotient.

Since Gamma > 0, w is an equivalent free coordinate:

    t = (1-w)/Gamma,       v = beta(1-w)/Gamma.

## 4. Exact local positivity and D1 slot family

For each complete D1 stem marking let q_xi = q_B(D1,xi,I). The baseline
has more than one eligible ideal and every slot is strictly positive, so
0 < q_xi < 1. Therefore

    W_xi = 4(1-q_xi)/R_xi > 0,
    W_* = min_{xi=0,...,7} W_xi > 0.

Since R_xi > 41 and q_xi > 0, every W_xi < 4/41; hence W_* < 4/41 < 1.
This uses the finite complete eight-record set, not an unproved minimum over
an omitted or infinite record domain. Maximal-bit invariance and locality
transport the stated slots to all complete D1 records.

**Theorem.** The following two statements are equivalent:

(a) All eight T1 equations hold, the three affected child corrections satisfy
    w > -4e, t > -4, v > -4, and every RI-111 D1 slot upper bound
    w < W_xi holds.

(b) For one freely chosen real w,

    -4e < w < W_*,
    t = (1-w)/Gamma,
    v = beta(1-w)/Gamma.

**Proof of necessity.** Section 3 forces the two formulas. The J1 positivity
condition is precisely the lower bound, because e > 0. The finite conjunction
of all slot bounds is precisely w < W_*.

**Proof of sufficiency.** Section 3 establishes every T1 row. The lower bound
is exactly J1 positivity. Since w < W_* < 1 and beta,Gamma > 0, the displayed
formulas actually give t > 0 and v > 0, stronger than the two required
inequalities t > -4 and v > -4. Finally w < W_* implies every slot bound.
There are no endpoint exceptions: all inequalities are strict.

The interval contains zero because e and W_* are positive. Thus w = 0 gives
the valid local member t = 1/Gamma, v = beta/Gamma. This member witnesses
nonemptiness of exactly subsystem (a); it is not imposed on the coupled
extension problem.

The positivity of v proved here is a new conditional consequence of the
accepted signs, zero minors and slot bound. It is not the old 27-child
argument v > 0 from 1-w > 0 alone. Without these additional facts the new
Y0 term prevents that argument, exactly as RI-111 section 5 states.

## 5. Optional exact simplification of the slot endpoint

The empty/ordinary-birth diamond from K and I gives

    q_B(K,xi,I) e_T1 = e_K q_B(D1,xi,I),

because the ordinary child K+I is T1. Therefore q_xi = R_xi e. It follows
without any new evaluation that

    W_xi = 4/R_xi - 4e,
    W_* = 4/R_max - 4e,
    R_max = max_{xi=0,...,7} R_xi.

In particular the local interval has exact positive length 4/R_max, and
its alternative coordinate lambda = w + 4e obeys

    0 < lambda < 4/R_max.

The transformed D1 I-slot is R_xi lambda/4, so the lower bound makes it
positive and the upper bound makes every such slot less than one. The
baseline inequalities R_xi e < 1 ensure W_* > 0. These identities neither
evaluate R_max nor enforce the sum of all D1 slots.

## 6. Coupling is not removed

The local family leaves w_1 free. At the next parent D1, t and v_1 do not
enter the correction row directly; the same w_1 does, together with the
shared J-column variables w_2 and w_3 in L_1. Their coefficients must count
every supported individual ideal. The exact D1 requirement remains

    g_10 L_1(r;w) - g_1(r)L_1(r0;w) = 0   for every complete record,
    L_1(r0;w) < 4 e_C1 g_10,
    d_1 = -L_1(r0;w)/(e_C1 g_10).

Those are additional coupled conditions, not consequences of the bounds in
section 4. For each j = 2,3 the connected-parent condition remains

    (z_j-w_j)(f_j(r)-f_j0) = 0   for every record,
    -4e_Tj < w_j < z_j + 4f_j0,
    v_j = (z_j-w_j)/f_j0.

If one proves a nonzero record contrast of f_j, these conditions force
w_j = z_j and v_j = 0. If f_j is constant, they retain a genuine open
interval of w_j. Neither alternative may be chosen without proof. In
particular nonconstant g_1 alone does not force d_1 = 0, because L_1 can
vary with records as well. No old necessity for v_1 is substituted for
this analysis, and w_1 = 0 may not be imposed to simplify it.

Even a complete D1 solution would leave T2,...,T11 and D2,...,D5 compulsory,
except to the exact extent that some of their equations have independently
been proved and used. The sixteen-parent obligation is unchanged. No full
repair, support rejection, all-size extension, QM derivation, geometry,
gravity or empirical conclusion is established by this local lemma.

## 7. Read coverage and operations

The reviewer read the following four sources completely:

| Source | Lines | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| RI111 external REPAIR.md | 525 | 20656 | ca07943f8d2f9d9c396b4484193dc5797900f6c7a18c5f8c2a5b8333759ccf53 |
| RI115 root final mathematical adjudication | 132 | 6678 | a23c0ac1208c78cc28590727675869968e2f579c863857aad67a9ea08b1d2480 |
| Published one-column-rank RESULT_REVIEW.md | 112 | 6498 | 0489c1cea77f8cc6cf0b93ee15b0423181fb274a963e8d9fbbffedf4c38d0a01 |
| Independent ANALYTIC_NEXT_STEP.md | 123 | 6518 | 1bb2b0bbcc46c27c83b150b1f6601149358c4a645e54cb0998585c0ac5547803 |

Exact paths:

- /Volumes/AI_DATA/development/det-review-evidence/ri111-one-column-repair-HRfi3z/REPAIR.md
- /Volumes/AI_DATA/development/det-review-evidence/ri115-116-root-review-tyo8kzjn/RI115_ROOT_FINAL_MATHEMATICAL_ADJUDICATION.json
- /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_one_column_rank_check_v1/RESULT_REVIEW.md
- /Volumes/AI_DATA/development/det-review-evidence/ri112-independent-positive-family-2_hgjqki/ANALYTIC_NEXT_STEP.md

RI111 was read in ranges 1--260 and 261--EOF; the other three were read
1--EOF. The source byte identities were independently refreshed by an opaque
SHA-256 read (tool chunk 067683), and line/byte counts by chunk abf283.
The independent next-step note's description of then-pending audit is historical;
the later RI115 root decision supplies the accepted zero-minor disposition.

Only source reading, opaque identity/count checks, and manual symbolic proof
were performed. No target import, AST, compilation, runtime probe, replay,
fixture, solver, new probability or polynomial coefficient evaluation,
H/z arithmetic, q6/q7 table, or scale selection occurred. Only this external
note was written; no repository, index, git, prior evidence, admission or
execution artifact was changed. This note is a proof contribution for
independent whole-packet review and root adjudication, not self-acceptance.
