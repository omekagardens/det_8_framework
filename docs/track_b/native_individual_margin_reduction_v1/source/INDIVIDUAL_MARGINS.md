# Individual margin reduction with a native positive slack

30 September 2026, Honolulu. Manual conditional theorem for independent review.

The accepted global bound supplies more than a positive weighted sum.
At the unchanged actual pair, the positive contribution belonging to
C3 alone exceeds the complete normalized harmonic seed deficit:

    B3 > 1 + delta,
    delta = 4,000,000,000 / 926,000,000,001 > 0.                 (I1)

The original two strict margins reduce exactly to one fixed seed split h:

    C2 > 0 and C3 > 0    iff    1-B3 < h < B2,
    h = -3m*z2/r.                                             (I2)

Here B2>0 and B3 are the original contributions, not fitted coefficients.
In particular the whole closed strip -delta<=h<=0 is a sufficient
condition for both strict margins. No membership of the unchanged seed
in that strip is asserted. Outside it, one particular margin is settled
and exactly one same-law scalar comparison remains. The latter is
specified in [SEED_COMPARISON.md](SEED_COMPARISON.md).

That companion uses two newly admitted original analytic texts to
eliminate h exactly: h=A/K, with A>0 and K!=0 proved. Thus no
independent numerical seed-coordinate input is needed. The remaining
native determinant sign and branch inequality are stated explicitly;
neither has been silently treated as proved.

This is not yet a proof or refutation of the actual pair of margins.
It does not reconstruct H or the seed, substitute another law, or
promote W>0 to simultaneous positivity.

## 1. Accepted same law premises

Use the complete original connected formulas, held coefficients and
record transport in the six analytic texts admitted by the RI212
assignment. Their exact identities and earlier inherited matches are
in [SOURCE_REFERENCES.json](SOURCE_REFERENCES.json). Write

    r = r3_0 > 0,       j = j0 > 0,       m = m0 > 0,
    theta > 0,         c = c0 > 0,       g = theta^3*c = theta*m,
    lambda = D3/r > 0,  eta = epsilon3/r > 0.

The g here is the positive aggregate in the accepted weighted proof,
not a held row G_i or core probability g_i. The seed split h below
is not the prefix one-cap probability h_i in the canonical polynomial.

RI145 gives the exact identities

    D2=theta*D3,       r2_0=theta*r,
    epsilon2=theta*epsilon3,       m=theta^2*c,
    r+3m*z2+3j*z3=0,       z1=1.                               (I3)

The epsilon identity uses the actual empty slot. It does not erase
the singleton canonical correction at other C5 slots. The original
amplitude is 1/4; |z_i|<=1 and all seed coordinates remain fixed.

At the actual correlated pair define

    f2=1-s*U20(rho),       f3=1-s*U30(rho).

The accepted domain and signs give q(rho)>0, 1-rho>0, f2>0,
and in fact f3>2/3. The last fact follows from the accepted
U30>0, 0<s<=1/d(rho) and 1-U30/d>2/3, with
d(x)=6-4x+2x^2. Actual s is not replaced by zero or by the
upper boundary; the inequality holds at its unchanged value.

The accepted global result is

    M6 < B=463,000,000,000 < A=465,000,000,000 < T,
    T=4lambda*j/v-1/2,       v>0,
    rho=1/[2(1+M6)].                                         (I4)

Thus rho>1/[2(1+B)]. Its existing upper bounds and its coupling to s
are retained. None of M6, M7, rho or s is evaluated here. All of
(I3)-(I4) are premises from the accepted same-law chain, not freshly
run numerical certificates or values chosen for this proof.

## 2. Exact split into seed and positive contributions

Keep the original margins without dropping a term:

    C2=z2+4[rho^2*D2/q(rho)]*f2
         +4s*rho^3*(epsilon2+r2_0),

    C3=z3+4[rho*D3/((1-rho)*v)]*f3
         +4s*rho^2*(epsilon3+r3_0).                           (I5)

Normalize their positive parts by the positive harmonic weights:

    B2=12lambda*g*rho^2*f2/q(rho)
          +12g*s*rho^3*(1+eta),

    B3=12lambda*j*rho*f3/((1-rho)*v)
          +12j*s*rho^2*(1+eta).                              (I6)

Every factor and denominator determining the signs in (I6) is
strictly positive. In particular B2>0. These B2,B3 symbols name
normalized positive contributions, not the held polynomial coefficient
B2_0 appearing in U20.

Set h=-3m*z2/r. This is a fixed scalar of the ORIGINAL seed, not
a new degree of freedom. The harmonic identity gives
3j*z3/r=h-1. Multiplying the complete margins (I5) by their
positive weights and using g=theta*m proves

    (3m/r)*C2=B2-h,
    (3j/r)*C3=B3-1+h.                                        (I7)

For example, the first positive core term becomes
(3m/r)*4rho^2*(theta*lambda*r)*f2/q
=12lambda*g*rho^2*f2/q. Its empty-plus-core term becomes
12g*s*rho^3*(1+eta). No already scaled empty probability has
been substituted for a held epsilon.

Summing (I7) recovers the original identity exactly:

    W/r = (3m*C2+3j*C3)/r = B2+B3-1.                          (I8)

The seed has not disappeared from each individual sign. Equation
(I8) eliminates its split only from their weighted sum.

## 3. Quantitative lower bound for the C3 contribution alone

Use f3>2/3 and retain the strict positivity of the second term
in B3. Multiplication by positive factors gives

    B3 > 8lambda*j*rho/((1-rho)*v)
        = 8lambda*j/[v*(1+2M6)]
        = (2T+1)/(1+2M6).                                    (I9)

The middle equality follows directly from the actual definition of
rho; the last follows from the original definition of T. This step
has kept the positive contribution from C3 alone. It has not borrowed
the C2 contribution to establish the bound.

As T>A and M6<B, all denominators are positive, and

    (2T+1)/(1+2M6)
      > (2A+1)/(1+2B)
      = 1+2(A-B)/(1+2B)
      = 1+4,000,000,000/926,000,000,001.                       (I10)

Equations (I9)-(I10) prove (I1) by manual algebra. No automatic
scientific arithmetic is used. The displayed rational is exact,
not a rounded tolerance. At the more general sufficient endpoint
M6=T, (I9) already gives B3>1 strictly; the actual accepted
strict separation in (I4) supplies the explicit delta.

Consequently, at the SAME unchanged pair,

    (3j/r)*C3 > h+delta,
    C3 > -(m/j)*z2 + r*delta/(3j),
    W/r > B2+delta > delta.                                  (I11)

The first two statements are individual-margin bounds. They are
strict even when h=-delta, or when z2=r*delta/(3m).
The final statement is a strengthened weighted consequence, not
a substitute for testing the individual margins.

## 4. Exact strict criterion and the settled seed cases

Because r, m and j are strictly positive, (I7) proves the exact
criterion (I2). Its endpoints are excluded:

    h=B2       gives C2=0;
    h=1-B3     gives C3=0.

Either equality therefore fails the original strict local interval
test. Since B3>1+delta and B2>0, the lower endpoint is strictly
below -delta and the upper endpoint is strictly above zero.
Thus the closed strip -delta<=h<=0 is contained in the strict
success interval. Including the strip endpoints does not relax
either original strict inequality.

The remaining cases separate without choosing a seed-bad index:

| Fixed seed case | Already settled | Exact remaining test |
| --- | --- | --- |
| h>0, equivalently z2<0 | C3>0 | h<B2 |
| -delta<=h<=0 | C2>0 and C3>0 | No further local sign test |
| h<-delta, equivalently z2>r*delta/(3m) | C2>0 | 1-h<B3 |

These are statements about where the one unchanged h actually lies,
not permission to pick h from the middle row. In the first row
equality h=B2 or h>B2 yields an actual nonpositive C2 if established
for that fixed seed. In the last row equality 1-h=B3 or a larger
left side yields an actual nonpositive C3.

The zero seed case is included in this intermediate criterion for
mathematical completeness. The companion proves h!=0 for the original
seed, so the actual seed cannot use that boundary. The sufficient
strip and exact criterion remain sound.

## 5. Relation to the original positively cleared targets

Retain the original polynomials, with H2=epsilon2+r2_0 and
H3=epsilon3+r3_0:

    P2(x,y)=q(x)*z2+4x^2*D2
        +4y*(q(x)*x^3*H2-U20(x)*x^2*D2),

    P3(x,y)=(1-x)*v*z3+4x*D3
        +4y*((1-x)*v*x^2*H3-U30(x)*x*D3).                     (I12)

At the actual pair the new reduction agrees with them:

    P2(rho,s)=[q(rho)*r/(3m)]*(B2-h),
    P3(rho,s)=[(1-rho)*v*r/(3j)]*(B3-1+h).                    (I13)

Both multipliers are strictly positive. This is an exact
reparameterization of the original two signs, not a changed target,
amplitude, box, endpoint convention or record quotient. The old
fixed numerical certificate Y=1/4 is not redesigned or executed.

## 6. Canonical corrections and shared constraints stay binding

The original q is still

    q(x)=(1-theta*x^2)*v
       +(2-theta-2theta*x+theta^2*x^2)*Delta h_i
       +(3-2theta-2x+theta*x^2)*Delta j_i
       +(x-2)*Delta N+2Delta(N*omega)
       -theta*x^2*Delta(N*omega^2),

    N_i=(35/1476)*[41p_i-f_i/2-min{g_(i,0),g_(i,1)}]_+/c_i,
    omega_i=44theta*p_i.                                     (I14)

In this display Delta h_i denotes h_1-h_0 of the held prefix
probabilities, not the seed split h. The other Deltas retain their
original record1-minus-record0 convention, including whole-product
contrasts. Zero positive-part branches, tied minima and actual
normalizations have not been changed. No N_i or q coefficient has
been extracted, fitted, numerically bounded or evaluated here.

Complete record transport and individual-ideal multiplicities remain
accepted premises. Even a later proof of both signs would establish
only the two connected local intervals. The same recovered t2,t3
must still enter shared T1; w2,w3 must still enter every applicable
Di row. The other eight connected parents, all five Di and the
whole H30 system have not been solved.

The exact remaining native comparison is stated in the companion note.
This work gives neither a countermodel to the fixed law nor a
theorem that the missing comparison is underivable. It is a bounded
analytic reduction awaiting independent adjudication.

The original 92/34/35 and 31/139/20/42 executable obligations remain
unchanged and uncredited. No scientific body, vector or certificate
is parsed; no graph, LP, scientific executor, runtime, fixture or
card is run or changed. No H/z reconstruction, favorable scale
selection, new law, new agent/thread, repository or Git/index change
occurs. RET remains paused. Full QM, manifold emergence, gravity,
empirical correspondence and ontology are not conclusions. Root
owns independent acceptance, publication and any successor.
