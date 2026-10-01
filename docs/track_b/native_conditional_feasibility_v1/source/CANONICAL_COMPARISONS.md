# RI238 — canonical comparison and complete conditional recovery

30 September 2026, Honolulu. Source-only author result, pending independent
review. The actual normalized system now has the exact two-case criterion
in section 3, with an explicit shared solution on either feasible branch.
The actual canonical branch has not been located. No actual witness,
signed inconsistency, improvement or optimality is claimed.

## 1. Sharpen the retained D2 canonical comparison

Begin with the unchanged complete canonical capacity, not freely fitted
root allocations. At P=r<a<b,r<x,o<x,

    kappa_i=(352/41)(1-M_i),
    M_i=max_(all root-i records)
        [t(row)mu_(i,l)+v(row)tau_i+n(row)nu_(i,j)].

Every companion constraint, all 32 records, the original canonical
objective and all nonnegative competing coordinates remain binding.
Define chi_i=(35/36)kappa_i and Q(x)=x^2-(1-2theta)x.

RI235 proved the exact separation

    C_b=C_2(b^2)=g2(0)b1^2-g2(1)b0^2=C_hat+lambda Xi,
    C_hat<-1/12000, lambda=s rho(1-rho)/64,
    Xi=Q(chi0)b1^2-Q(chi1)b0^2.                           (B1)

The allocation-free part still includes the actual C5 correction N.
The full g2, and not that part alone, is used in every equation below.

Use now the accepted RI128 correlated scale bound

    s<=1/(6-4rho+2rho^2), 0<rho<1/8.

The function r(1-r)/(6-4r+2r^2) is strictly increasing on
0<r<1/8: its derivative has positive numerator 6-12r+2r^2.
At r=1/8 its value is 7/354. Consequently

    lambda<7/22656,
    Xi<=236/875  implies  C_b<0,
    C_b=0  implies  Xi>236/875>1/4.                      (B2)

The endpoint calculation is
(7/22656)(236/875)=1/12000; the strict lambda bound and the
strict C_hat bound retain equality in the sufficient Xi test.
If Xi<=0 the conclusion is immediate without multiplying an upper
bound by a negative number. This improves the former threshold 64/375.

There is also a comparison stated directly in the actual competition
masses. Let a_theta=1-2theta, so 0<a_theta<1 and
Q(x)>=-a_theta^2/4>-1/4 for x>=0. Suppose chi0<=chi1.

If chi0+chi1>=a_theta, then

    Q(chi0)-Q(chi1)
       =(chi0-chi1)(chi0+chi1-a_theta)<=0,
    Xi=b1^2[Q(chi0)-Q(chi1)]-(b0^2-b1^2)Q(chi1)<1/4.

If chi0+chi1<a_theta, both Q values are nonpositive and

    Xi<=-b0^2 Q(chi1)<1/4.

Here 0<b1<b0<1. Thus either case and B2 give

    kappa0<=kappa1, equivalently M0>=M1, implies C_b<0.   (B3)

In particular a zero actual core coefficient requires simultaneously

    M0<M1, kappa0>kappa1, Xi>236/875.                    (B4)

This does not establish that M0>=M1 in the canonical optimum. No
componentwise comparison of mu,tau,nu is available merely from the
individual row caps. They stay coupled; choosing them independently
would not settle B3 for the actual law.

For reference the other still unresolved canonical difference is

    d=(35/1476) {
       [41p-f_hook,1/2-min(g_hook,(1,0),g_hook,(1,1))]_+/c1
      -[41p-f_hook,0/2-min(g_hook,(0,0),g_hook,(0,1))]_+/c0
      }.

Every minimum tie and zero positive part remains admitted. The relevant
exceptional value is d7=-theta^2 K/(1-t). The T4 value d4 no longer
needs to be separated from d: ACTUAL_BRANCH_REDUCTION.md proves U4=0
even if that equality holds.

## 2. Carry the T7 exception through D2 and D5

Write C_p(x)=g_p(0)x1-g_p(1)x0 with the actual full profiles.
The companion proves U4=U5=U6=0 in every solution. Therefore D2 is

    (theta^2 Gamma2/a)C_b+C_2(ell)U7=0, Gamma2>0.         (B5)

If d!=d7, the connected T7 equation forces U7=0, so B5 is
equivalent to C_b=0.

If d=d7, then Delta ell=-d7>0 and the companion proves U9=U10=0.
The zero alternative for the remaining D2 coefficient can now be
settled rather than divided away. If C_2(ell)=0, positivity gives

    g2(1)/g2(0)=ell1/ell0>1,
    C_b=g2(0)[b1^2-(ell1/ell0)b0^2]<0.

Equation B5 would then have a strictly negative nonzero left side,
because its U7 coefficient is zero. Thus

    d=d7 and C_2(ell)=0 is inconsistent.                 (B6)

This is a conditional finite signed inconsistency, not an assertion
that the actual fixed coefficients occupy that branch.

On the remaining exceptional branch C_2(ell)!=0, B5 uniquely sets

    U7=-theta^2 Gamma2 C_b/[a C_2(ell)].                  (B7)

The companion proves C_5(ell)>0 on d=d7. The complete D5 equation,
with U10=0, therefore has the valid shared recovery

    U11=-theta C_5(b)U7/C_5(ell).                        (B8)

Thus this exception is not rejected merely because it was an
exception. D5 genuinely admits the value B8 at the same coefficients;
no separate record-sector adjustment is introduced.

## 3. Exact full-system criterion and conditional witness

Conditional on the unchanged accepted finite-law premises, the original
normalized ten-coordinate system has a solution exactly as follows:

| Actual branch | Necessary and sufficient condition |
| --- | --- |
| d!=d7 | C_b=0 |
| d=d7 | C_2(ell)!=0 |

Necessity follows from the actual U4 elimination and section 2.
Here is a constructive sufficiency proof that retains all other parents.

Choose U4=U5=U6=U9=U10=0. These are shared choices for the
original coordinates, not removal of columns or changes of support.

On the first feasible branch set U7=U11=0.
On the second feasible branch use B7 and B8.
Keep the same accepted Gamma and beta coefficients and define

    W1=-Gamma_10 u0+Gamma_12-Gamma_13 u3,
    W2=Gamma2, W3=-Gamma3 u3, Wj=Uj for j>=4.

To solve D1, using its unchanged actual g1 including all canonical
offsets, set

    X=(theta^3/a^2)C_1(b^3),
    Y=3C_1(j),
    Z=3theta^2 Gamma2 C_1(c).

The complete equation is X W1+Y W3+Z=0.
The companion proves Gamma_10>0; Gamma3>0 is inherited.
Moreover X and Y cannot both vanish: C_1(b^3)=0 would require
g1(1)/g1(0)=b1^3/b0^3<1, whereas C_1(j)=0 would require
that same ratio to be j1/j0>1.

Consequently the following original-coordinate choices are well-defined:

    If X!=0:
        u3=0, u0=(X Gamma_12+Z)/(X Gamma_10).
    If X=0:
        u0=0, u3=Z/(Y Gamma3).                           (B9)

No sign or nonzero assumption is made about C_1(c), Gamma_12,
Gamma_13 or the unresolved canonical terms in g1. They remain actual.

The companion's unconditional C_3(j)>0 now solves D3:

    U8=-(theta/a) C_3(b^2) W3/C_3(j).                    (B10)

D4 is zero with the chosen U4,U9,U10. D2 and D5 were solved above.
For the connected rows, every nonzero chosen U is among U7,U8,U11;
U7 is used only on its proved zero-contrast branch, and f8,f11
are the inherited constant profiles. Hence all eight connected
equations hold, including the T9/T10 equations without needing a
blanket nonconstancy assertion. This completes sufficiency.

For clarity, the full original shared forms checked in this argument are

    l1=(theta^3 b^3/a^2)W1+3theta^2 c W2+3j W3,
    l2=(theta^2 b^2/a)W2+theta^2 c W4
                                  +theta c W5+j W6+ell W7,
    l3=(theta b^2/a)W3+2theta c W6+j W8,
    l4=theta^2 b W4+theta^2 c W9+2ell W10,
    l5=theta b W7+theta c W10+ell W11,

    g_p(0)l_p(1;W)-g_p(1)l_p(0;W)=0, p=1,...,5,
    U_j[f_j(1)-f_j(0)]=0, j=4,...,11.                    (B11)

All ten original unknowns u0,u3,U4,...,U11 are specified by the
construction whenever its stated branch holds. No assertion of the
rank of a matrix has replaced a row check.

The complete original recovery remains

    u2=-1,
    delta v1=beta_10 u0-beta_12+beta_13 u3,
    delta v2=-beta2, delta v3=beta3 u3,
    delta vj=-Uj/f_j(0), j>=4,
    delta d_p=-rho*l_p(0;W)/(e_Cp*g_p(0)),
    delta y_Jj=Wj/e_j.                                  (B12)

The denominators in B12 are the original positive references.
The normalized proper-child variations are u0,u2,u3 themselves.
T1/T2/T3 compensation, full-slot corrections, all individual ideals
and factors two and three, and the original endpoint exclusions are
retained. RI233 transports these equations to all original records,
labels and both newborn maps; these are not two selected records
substituted for the complete law.

No new numerical amplitude is selected. Conditional signed recovery
does not authorize an endpoint, a positivity claim outside the
inherited local theorem, or an actual witness before the coefficient
branch is proved.

## 4. What is settled and what is not

New fixed-law content is the unconditional U4 elimination, complete
exceptional T9/T10 signs, C_3(j)>0, exceptional C_5(ell)>0,
Gamma_10>0, and the full conditional feasibility classification.
The actual core cancellation has a sharper necessary threshold B4.

These results reduce the previous three D2 branches to two complete
full-parent cases. They go beyond a restatement of a necessary D2
criterion: the former T4 freedom is eliminated by D4, the T7
zero-coefficient branch is inconsistent, and every remaining feasible
case has an explicit solution to all thirteen equations.

The actual decision is still missing. Specifically, this packet has
not established whether the canonical hook expression equals d7,
whether the actual C_b vanishes, or (if d=d7) whether C_2(ell)
vanishes. It also has not proved the canonical competition order in
B3. B2–B4 are constraints on actual fixed quantities, not permission
to refit them.

An actual full normalized witness or actual signed inconsistency
therefore remains unclaimed. Strict improvement, ceiling optimality,
maximal amplitude, all-size existence, full QM and geometry or
mass/gravity conclusions remain unclaimed as well.

## 5. Boundary and stop

Only already admitted analytic texts and administrative provenance
were used. The fifteen inherited boundary objects and the 423-source
manifest remain unchanged by reference. Historical scientific-body
and literal exceptions are not renewed.

No automatic scientific arithmetic, calculator/Fraction engine,
scientific JSON/coordinate extraction, H/z, graph/LP, subject/runtime,
capture, fixture/card, measurement, RET, repository/Git/index or
successor work occurs. Return this bounded sealed packet to the
coordinator for independent review; successor selection and any
publication remain coordinator-owned.

