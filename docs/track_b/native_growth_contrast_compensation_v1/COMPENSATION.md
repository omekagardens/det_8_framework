# RI124 — complete record-contrast compensation on a 30-child support

26 September 2026, Hawaii. Analytic/source-only manuscript.
The accepted seed, baseline B, amplitude 1/4 and earlier results are unchanged.
No new probability, H/z, actual scale, solver or numerical certificate is
evaluated here. This is an exact finite conditional criterion, not a claimed
positive continuation.

## 1. Accepted starting point and present result

RI122_ROOT_FINAL_ADJUDICATION.json accepts the obstruction for the entire
unchanged 28-child support: both connected profiles f2 and f3 are nonconstant,
so its equations force w2=z2 and w3=z3, contradicting strict positivity for at
least one index. It does not reject every proper-child support. The accepted
positive local T1 family remains valid on its stated subsystem.

This manuscript derives the joint contrast/intercept/positivity theorem,
then specializes it to two additional proper-child classes. SUPPORT.md
enumerates the complete closure and individual supported slots. The result
is a necessary-and-sufficient reduced system at the actual unchanged B.
Its feasibility has not been decided. COEFFICIENT_OBLIGATIONS.md distinguishes
symbolic coefficients already expressible in held data from remaining
premises and any separately admitted later calculation.

The two additional classes are

    Y2 = C3 ordinal-sum (C2 disjoint A3),
    Y3 = C3 ordinal-sum ((A2 ordinal-sum A1) disjoint A2).

Here Cn is an n-chain and An an n-antichain. Subscripts Y2,Y3 refer to their
T2/T3 incidence in this manuscript; they are not new seed coordinates.
Retain Y0=C3 ordinal-sum A5. The full support is

    H30 = {Jj=Tj disjoint A1: j=1,...,11}
          union {F(P): P in P16}
          union {Y0,Y2,Y3},
    P16 = {T1,...,T11,D1,...,D5}.

F(P) adds a unique new maximum above all of P. The catalogue and individual
mask conventions are fixed in SUPPORT.md. The totals are 30 child classes,
16 incoming parent classes, 66 individual maximal-deletion roles and
63 supported forward ideal slots. Backward counts are not forward weights.
No new incoming parent class is introduced. All five Di still have h7=1
and their full constraints remain binding.

## 2. Joint theorem before a support-specific elimination

For a finite declared support H and each incoming seven-parent P, define

    a[P,r,H] = sum of q_B(P,r,S) over every individual ideal S
               whose unmarked child is H.

One y_H is shared across every parent, marking, ideal, newborn bit and
labeling. It is not chosen separately by row. Put Z(Tj)=zj and Z=0 otherwise.
For the prescribed amplitude, h8(H)=1+y_H/4 on support and h8=1 outside it.

The complete system is

    sum_H a[P,r,H] y_H = Z(P)     for every incoming P and every record r,
    y_H > -4                     for every support class H.                (1)

Every incoming parent of the support must be included even if Z(P)=0.
A parent outside the closure has no corrected slot and Z(P)=0 in this
application. Its equation is then discharged, not omitted without proof.
Individual repeated ideals are always included in a[P,r,H].

Choose one reference r0(P). System (1) is equivalent to the simultaneous
conditions

    sum_H (a[P,r,H]-a[P,r0,H]) y_H = 0     for every P,r,
    sum_H a[P,r0,H] y_H = Z(P)            for every P,
    y_H > -4                             for every H.                      (2)

Necessity is subtraction; sufficiency is addition of each reference row.
Consequently the nullspace of all contrast rows must be intersected with
all reference affine equations and the open positivity region. Rank/span
compatibility alone is not a positive continuation. Zero contrasts and
zero columns remain part of the system; no division by them is justified.

In a connected row with the record-blind empty contribution w_j and a
private full child v_j, write the additional proper contribution as
sum_H k_jH(r)y_H. The exact equations become

    Delta f_j(r) v_j + sum_H Delta k_jH(r)y_H = 0,
    w_j + f_j(r0)v_j + sum_H k_jH(r0)y_H = z_j,                              (3)
    w_j > -4 e_Tj, v_j > -4, y_H > -4.

The same y_H in another parent row is the same unknown, not a new freedom.
A private full child is private only to its unmarked parent, not its records.

Why T1-only freedom cannot repair RI122: if every added column is zero in
all T2 and T3 rows, their contrast equations remain Delta f_j v_j=0.
The accepted nonconstancies then give v2=v3=0 and w2=z2,w3=z3. The accepted
strict disjunction z2<-4e_T2 OR z3<-4e_T3 remains contradictory. This proof
does not depend on the number or effectiveness of the T1-only columns.

## 3. Complete equations for the chosen support

Use the unchanged notation

    e_P = q_B(P,r,empty)>0,       w_j=e_Tj y_Jj,
    f_j(r)=q_B(Tj,r,Tj)>0,       v_j=y_F(Tj),
    g_i(r)=q_B(Di,r,Di)>0,       d_i=y_F(Di),
    t0=y_Y0, t2=y_Y2, t3=y_Y3.

All e_P are record-blind. Define the actual coefficient functions

    k0(xi)  = q_B(T1,xi,C3),
    k12(xi) = sum over the four one-cap ideals of T1 of q_B(T1,xi,S),
    k13(xi) = sum over the six two-cap ideals of T1 of q_B(T1,xi,S),
    k2(r)   = q_B(T2,r,C3),
    k3(r)   = q_B(T3,r,C3).

These are sums of individual probabilities, never averaged probabilities.
They are positive. The last two ignore nonstem records by precursor locality.
The justified complete f2 and f3 representative domains are respectively
eta=0,...,15 and xi=0,...,7, by RI117. The T1 domain is all eight xi.
The conservative 384-row quotient of all 2,048 parent-marked rows remains
available globally; no further reduction is presumed on other parents.

The connected equations are exactly

    w1 + f1(xi)v1 + k0(xi)t0 + k12(xi)t2 + k13(xi)t3 = 1,                  (4)
    w2 + f2(eta)v2 + k2(eta)t2 = z2,                                      (5)
    w3 + f3(xi)v3 + k3(xi)t3 = z3,                                        (6)
    wj + fj(r)vj = zj                 (j=4,...,11; every r).               (7)

For each Di=Ci disjoint A1, let

    Li(r;w) = sum_{individual S of Ci: [Ci+S]=Tj} q_B(Ci,r,S) wj.

Its 7,5,4,4,3 individual supported slots are all listed in SUPPORT.md.
The empty/ordinary whole-map diamond, separately at every record and both
newborn bits, gives the exact unchanged equations

    Li(r;w) + e_Ci gi(r) di = 0       (i=1,...,5; every r).                 (8)

No ti appears in (8), but the w1,w2,w3 obtained from (4)-(6) do. Thus the
Di constraints couple the connected subsystems and cannot be checked with
different w values. All positivity conditions are

    wj>-4e_Tj, vj>-4 (j=1,...,11), di>-4 (i=1,...,5),
    t0>-4, t2>-4, t3>-4.                                                  (9)

The necessary-and-sufficient statement includes every equation (4)-(9),
not just the two connected parents motivating the enlargement.

## 4. What exactly lets an added proper column escape the old forcing

For j=2,3 fix reference record zero and pivot record one. RI122 supplies
piv_j=Delta_1 f_j != 0 at the actual unchanged scale, not merely permission
for the profile to vary. Define symbolically

    beta_j = -Delta_1 k_j / piv_j,
    Gamma_j = k_j(0) + f_j(0) beta_j,
    N_j(r) = Delta_r k_j piv_j - Delta_r f_j Delta_1 k_j.                  (10)

Then (5) or (6) for all its records is equivalent to

    v_j = beta_j t_j,
    w_j = z_j - Gamma_j t_j,
    t_j N_j(r) = 0                    for every remaining record r.        (11)

Indeed the pivot contrast gives v_j, the reference gives w_j, and every
other contrast after substitution is t_j N_j(r)/piv_j=0. Division is only
by the accepted nonzero piv_j; there is no division by t_j or Delta k_j.
The pivot symbol is distinct from the private Di full corrections d_i.

Three distinct cases must not be conflated:

- If any N_j(r) is nonzero, t_j=0 and hence v_j=0,w_j=z_j: the old forcing
  survives on that parent, despite the added column.
- If all N_j vanish but Gamma_j=0, w_j=z_j still holds; contrast cancellation
  alone does not repair the intercept.
- If all N_j vanish and Gamma_j!=0, the signed all-record system allows
  w_j to move away from z_j. It is still restricted by strict positivity
  and every shared-parent equation.

Thus the support supplies genuine proper columns in both obstructed rows,
rather than another T1-only modification. Its escape capacity is precisely
conditional on (10)-(11), not certified by incidence alone. No claim of
support minimality or actual nonzero Gamma is made.

The exact local strict conditions are

    t_j>-4, beta_j t_j>-4, z_j-Gamma_j t_j>-4e_Tj,
    t_j N_j(r)=0 for every r.                                             (12)

At each seed-bad index with z_j<=-4e_Tj, these require t_j!=0,
Gamma_j!=0 and all N_j=0; moreover Gamma_j t_j<z_j+4e_Tj<=0.
RI122 guarantees at least one strictly bad index, but does not select it.
If no t_j meets (12) at any bad index, H30 is rejected. If such t_j exists
locally, it is not yet a simultaneous positive continuation.

## 5. Full elimination without losing the T1 coupling or other parents

Let m run over 0,2,3 with k_1,0=k0, k_1,2=k12, k_1,3=k13.
RI109's accepted f1(1)-f1(0)!=0 supplies the T1 pivot piv_1. Put

    beta_1m = -Delta_1 k_1m / piv_1,
    Gamma_1m = k_1m(0) + f1(0) beta_1m,
    B_m(r) = Delta_r k_1m + Delta_r f1 beta_1m.                             (13)

Then every T1 equation (4) is equivalent to

    v1 = sum_m beta_1m t_m,
    w1 = 1 - sum_m Gamma_1m t_m,
    sum_m B_m(r)t_m = 0                 (r=2,...,7).                        (14)

These are sums: independent vanishing of the three column minors is not
required in the general elimination. Assigning a separate independently
adjustable v1 to each column would break the shared system. Conversely a
solution at records zero and one alone leaves six equations untested,
unless the following accepted polynomial identities are explicitly used.

### Accepted RI115 identities discharge the T1 contrast rows

The six accepted identities hold as polynomials, not just at one scale:

    Delta_xi p P_1(x) - Delta_1 p P_xi(x) = 0,     xi=2,...,7,
    P_xi(x)=-4 Delta_xi E + 6x Delta_xi j
                  +4x^2 Delta_xi nu + x^3 Delta_xi K.

RI117 also accepts Delta_1 p<0, so division by it is justified. Equality
of the coefficients of x and x^2 gives respectively

    Delta_xi j = (Delta_xi p/Delta_1 p) Delta_1 j,
    Delta_xi nu = (Delta_xi p/Delta_1 p) Delta_1 nu.

The polynomial identity itself gives
P_xi=(Delta_xi p/Delta_1 p)P_1. The three T1 proper coefficients are
k0=s rho^4 p, k12=4s rho^3 nu and k13=6s rho^2 j, whereas
Delta_xi f1=-s rho P_xi(rho). All four contrast columns therefore have
the same proportionality factor Delta_xi p/Delta_1 p. Every B_m(r) in
(13) vanishes at the actual baseline. Records zero and one satisfy the
same statement by definition. This is a manual coefficient-identity proof
using the accepted polynomial result, not new numerical reconstruction.

Consequently (14)'s T1 contrast equations are automatic for arbitrary
t0,t2,t3. Its reference equation, all three shared-variable couplings
and every strict inequality still bind. This discharges a specific
previously expressible condition; it does not prove the T2/T3 minors,
positive feasibility or the Di equations.

For j=4,...,11, retain all actual records and set f_j0=f_j(0). The complete
remaining connected conditions are

    (zj-wj) Delta_r fj = 0              for every r,
    -4e_Tj < wj < zj+4f_j0,
    vj=(zj-wj)/f_j0.                                                       (15)

Constant profiles, including T8 and T11, retain their freedoms. No blanket
nonconstancy assumption is used.

With g_i0=gi(0), the complete Di conditions are

    g_i0 Li(r;w) - gi(r) Li(0;w) = 0    for every r,
    Li(0;w) < 4e_Ci g_i0,
    di=-Li(0;w)/(e_Ci g_i0).                                              (16)

All denominators here are positive. Nonconstant gi alone does not force
di=0 because Li may vary with the same records.

**Reduced feasibility theorem.** At the unchanged actual coefficients,
H30 admits the required positive through-eight-birth transform iff there
are finite real t0,t2,t3,w4,...,w11 satisfying:

1. Equations (11)-(12) for j=2,3, determining w2,w3,v2,v3.
2. The T1 equations in (14), whose contrast part is discharged above,
   with the displayed recovered w1,v1 and
   w1>-4e_T1, v1>-4, t0>-4.
3. Every condition (15), using the same w4,...,w11.
4. Every condition (16), using these same eleven w values.

The bounds on t2,t3 are already included in (12). Necessity follows by
the pivot/reference eliminations. Sufficiency recovers all thirty child
corrections and verifies (4)-(9), then uses the complete closure.

In particular the unchanged D1 core-slot bound w1<W_xi<4/41 still holds.
That slot produces J1, not Y2/Y3. It follows automatically from the complete
positive normalized D1 row in (16); it may be retained as an explicit
necessary diagnostic but does not replace that row. The earlier positive
local T1 witness cannot simply be combined with arbitrary connected repairs:
(14) and (16) must be solved with the same t2,t3,w2,w3.

## 6. Why the reduced theorem is a positive-law theorem, conditionally

Assume the reduced system actually has a solution. Define y_Jj=wj/e_Tj,
the sixteen private full corrections by (11),(14)-(16), the three t values
as above and all other eight-class corrections as zero. Then every h8 is
strictly positive by the open bounds; the accepted h7 is also positive.

For a seven-parent put q_Q(P,r,S)=q_B(P,r,S)h8(P+S)/h7(P).
Equations (4)-(8) are exactly complete normalization after subtracting the
baseline and dividing by amplitude 1/4. Every unaffected parent has h7=1
and all its child corrections zero by exhaustive incoming closure.
No unsupported ideal probability is removed from a row.

Because the multiplier is unmarked/class-invariant and the whole unmarked
parent is permitted input, strict precursor-record locality and marked
equivariance are preserved. In each whole-map diamond based at a six-parent,
the intermediate h7 cancels and both paths acquire the same terminal h8.
The two fair newborn factors and the scalar-passive payload D are retained.
Earlier diamonds remain the accepted seed prefix. Thus the implication
is through eight births only; it does not select an all-size continuation.

Conversely a positive transform confined to this support must normalize
all those rows and keep all multipliers positive, yielding (4)-(9) and
hence the reduced system. This proves both directions without claiming
that the actual coefficient instance passes them.

## 7. Current disposition and boundary

Yield: a finite definition, complete closure and a necessary-and-sufficient
record-contrast/intercept/strict-positivity theorem for H30, with its T1
contrast conditions discharged analytically by the accepted RI115 result.
The actual positive branch is unresolved. No new numerical coefficient or
compensation minor has been evaluated; no failure of the selected support
is claimed. A precise coefficient/remaining-premise inventory accompanies
this theorem, including the additional disconnected held-row domain.

No amplitude reduction, baseline reselection, new seed, supplied geometry,
borrowed growth law or more informative quantum payload has been introduced.
This remains internal analysis in the conditional scalar-passive model,
not a full DET-to-QM derivation or a geometry, mass/gravity or empirical result.
Option B and metric-as-record Status M are unchanged. RET remains paused;
the independent measurement lane is not part of this assignment.

All new files are confined to the declared external RI124 directory.
Predecessor evidence is preserved. Repository/index/Git/publication and
any later numerical admission remain with the research owner. After fresh
nonauthor review and exact-pinned handoff, this bounded assignment stops;
that is not a programme stop or a request for renewed user permission.
