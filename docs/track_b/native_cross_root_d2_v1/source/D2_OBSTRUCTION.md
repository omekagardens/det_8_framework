# D2 allocation separation and the full normalized system

30 September 2026, Honolulu. RI235 manual conditional result for independent
review. The allocation-free part of the actual D2 core contrast is strictly
negative, with a proved gap. The remaining canonical contribution is isolated
exactly. Combined with the new connected signs, this gives a bounded
three-branch decision problem, not a full witness or a signed inconsistency.

## 1. Separate the actual canonical offset without replacing the law

Use the accepted RI231 six-root values and RI233 offset collection.
Let chi_z=(35/36)kappa_z be the unchanged actual canonical allocations,
and let T0=138697/387200. Define, using all four separate stem ideals,

    Acal[X]=(5/352)(X_empty+X_singleton)
                           +(203153/8800)X_pair+(1/8)X_I,
    U=Acal[B]+c,              V=Acal[B^2/A],
    F0=1-theta(U+T0),         M20=theta^2 T0,
    P_Y=1-theta U,
    V_H=theta^3 V+2theta^2 c+j,
    V_C=theta^2 U+theta(5/352)N+ell,
    R2=theta^4 V+theta^3(1/8)(5/352)N+theta^3 c.

The R2 identity follows by substituting the complete C5 row
D=theta B+N at its singleton into RI231 W4. The full term e=theta c
is retained. Every displayed quantity is a fixed function of the same
law and same root sector.

Set

    Bhat2=3-rho(E2+V_H+V_C+P_Y+F0+M20)
                 +rho^2(theta^2 c+j+ell+F0+M20)+rho^3 R2,
    Q(chi)=chi^2+(2theta-1)chi,
    ghat2=1-s Bhat2,
    lambda=s rho(1-rho)/64>0.

The original profile then satisfies exactly

    B2=Bhat2-rho(1-rho)Q(chi)/64,
    g2=ghat2+lambda Q(chi).                                (D1)

This is algebraic term collection, not a law with kappa set to zero.
In particular the actual C5 correction N and all other coupled
canonical quantities remain in Bhat2. No independent choice of chi
or of a growth scale is made.

## 2. A strict sign for the allocation-free core coefficient

The companion establishes the actual bounds
N_0<1/200, N_1<1/800, |Delta N|<1/200, together with
p=1/352, L<44, theta<2^-38, rho<1/8 and s<1/4.
Since each Acal weight is below 24 and the complete proper C4
mass is 1-c, positivity gives U<25 and V<24L<1056.

There is an exact decomposition

    Bhat2,z=3(1-rho)^2+rho(2-rho)N_z+epsilon_z,
    |epsilon_z|<160 rho theta.                             (D2)

For a transparent manual bound, compare the terms defining Bhat2
with their zeroth-order expressions, retaining theta throughout:

| Term | Comparison expression | Absolute error bound |
| --- | --- | --- |
| E2 | 2-N | 47 theta |
| V_H | 1 | 47 theta |
| V_C | 1-N | 2 theta |
| P_Y | 1 | 25 theta |
| F0 | 1 | 26 theta |
| M20 | 0 | theta |
| theta^2 c+j+ell+F0+M20 | 3-N | 75 theta |
| R2 | 0 | theta |

For example E2=2-N-theta[1+(1-theta)(L+c)-(1/8)N],
and V_H-1=-theta(L+2c)+2theta^2 c+theta^3 V.
Their bounds use theta<1/10000 and the complete positive sums.
For R2, its displayed formula is below 1058 theta^3<theta.
The first six errors total 148 theta. Therefore the total error is
less than rho theta[148+75rho+rho^2]<160 rho theta, proving (D2).
The comparison expressions are used only for a bound, not evaluated
as a substitute zero-theta or zero-canonical law.

It follows that

    Bhat2<3-rho[6-3rho-(2-rho)N-160theta]<3,
    ghat2>1/4.                                             (D3)

The bracket is positive under the retained bounds. Also

    |Delta Bhat2|
      <rho(2-rho)/200+320rho theta
      <1/800+40theta<1/750.                                (D4)

The last step uses 40theta<1/12000, which follows from
theta<2^-38 and 480000<2^38. Thus
|Delta ghat2|<1/3000.

The admitted beta pair gives b0-b1=41/22000>1/600.
Both b sectors exceed 1/2, so b0^2-b1^2>1/600; also b0^2<1.
Consequently the unchanged allocation-free contrast obeys

    C_hat=ghat2(0)b1^2-ghat2(1)b0^2
         =-ghat2(0)(b0^2-b1^2)-Delta ghat2*b0^2
         <-1/2400+1/3000
         =-1/12000.                                        (D5)

This is a strict actual-law bound on a defined algebraic part of the
coefficient. It is not the assertion that the full coefficient has
that sign when its canonical offset is restored.

## 3. The precise remaining canonical comparison

Define the original D2 core coefficient and its retained offset by

    C_b=g2(0)b1^2-g2(1)b0^2,
    Xi=Q(chi_0)b1^2-Q(chi_1)b0^2.

Equation (D1) gives the exact identity

    C_b=C_hat+lambda Xi.                                   (D6)

Since lambda<1/2048, (D5) implies the sound sufficient conclusion

    Xi<=64/375  implies  C_b<0.                            (D7)

For positive Xi the upper product is strictly below
(1/2048)(64/375)=1/12000; for Xi<=0 its contribution is
nonpositive. Therefore an actual zero coefficient must satisfy

    C_b=0  implies
    Xi=-C_hat/lambda>1/(12000lambda)>64/375.                 (D8)

The inequalities are strict. Neither equality in the sufficient test
nor a zero canonical coefficient is discarded. The actual kappa values
have not been resolved, so (D7) is a conditional test, not an actual
choice of branch.

The accepted complete canonical P capacity identity and
0<=kappa_z<=352/41 remain binding. Their nonnegative competing
mu,tau,nu terms are not omitted and the two sectors are not fitted
independently. This proof does not claim that those bounds settle Xi,
nor construct a relaxed-allocation counterexample to the fixed law.
In particular the negative sign in (D5) is not promoted to the sign
of (D6) without the remaining canonical comparison.

## 4. The three exact D2 branches

Retain W2=Gamma2>0 and the original normalized u2=-1.
Let, for any held scalar x,

    C_x=g2(0)x1-g2(1)x0.

The companion proves U5=U6=0. The actual D2 equation is therefore

    (theta^2 Gamma2/a) C_b
                  +theta^2 C_c U4+C_ell U7=0,             (D9)

where a=41/44>0. This reduction does not require either j9 or j10
to have a nonzero contrast.

The actual connected equations admit exactly these cases.

1. If d is neither d4 nor d7, both U4 and U7 are zero. D2 then
   requires C_b=0. In this branch a proof of (D7), or any other
   proof of C_b!=0, would be a finite necessary-subsystem
   inconsistency. Without that premise there is no rejection.

2. If d=d4, then Delta f4=0 and Delta f7<0, hence U7=0.
   If C_c!=0, D2 requires
   U4=-Gamma2*C_b/(a*C_c).
   If C_c=0, D2 instead requires C_b=0 and leaves U4 free.
   Neither alternative alone solves the other parents.

3. If d=d7, then Delta f7=0 and Delta f4>0, hence U4=0.
   If C_ell!=0, D2 requires
   U7=-theta^2*Gamma2*C_b/(a*C_ell).
   If C_ell=0, D2 instead requires C_b=0 and leaves U7 free.

The two exceptional cases cannot coexist because d4>0>d7.
All divisions above are conditional on their explicitly stated
nonzero coefficient. A zero D2 coefficient is not permission to
drop its reference equation or create private root-sector corrections.

For completeness, on the first branch the formal finite row
combination is explicit. Write E_D2 for the original cross-root
D2 row, F_j=Delta f_j and E_j=F_j U_j. When all four F4–F7
are nonzero, subtract from E_D2

    (theta^2 C_c/F4)E4+(theta C_c/F5)E5
                    +(C_j/F6)E6+(C_ell/F7)E7.

Its left side is exactly (theta^2 Gamma2/a)C_b; all unknown
coefficients vanish. This becomes a signed inconsistency only
after the actual remaining nonzero premises are proved.
It is not claimed as a completed obstruction in this packet.

## 5. Full system and recovery are unchanged

All ten original unknowns u0,u3,U4,...,U11 remain the coordinates
of the problem; U5=U6=0 are new proved consequences, not a new
support or a replacement problem. Define

    W1=-Gamma_10*u0+Gamma_12-Gamma_13*u3,
    W2=Gamma2>0,       W3=-Gamma3*u3,       Wj=Uj (j>=4).

Keep all original shared forms

    l1=(theta^3 b^3/a^2)W1+3theta^2 c W2+3j W3,
    l2=(theta^2 b^2/a)W2+theta^2 c W4
                                     +theta c W5+j W6+ell W7,
    l3=(theta b^2/a)W3+2theta c W6+j W8,
    l4=theta^2 b W4+theta^2 c W9+2ell W10,
    l5=theta b W7+theta c W10+ell W11.

Every original equation is still required:

    g_p(0)l_p(1;W)-g_p(1)l_p(0;W)=0,  p=1,...,5,
    U_j[f_j(1)-f_j(0)]=0,              j=4,...,11.          (D10)

Only j8 and j11 are the inherited identically zero connected cases.
The actual g1 and g2 offsets remain in these equations. The same
Gamma and beta coefficients, not independently adjusted reference
values, give the original complete recovery

    u2=-1,
    delta v1=beta_10*u0-beta_12+beta_13*u3,
    delta v2=-beta2,             delta v3=beta3*u3,
    delta vj=-Uj/f_j(0),         j>=4,
    delta d_p=-rho*l_p(0;W)/(e_Cp*g_p(0)),
    delta y_Jj=Wj/e_j.                                     (D11)

Every denominator is its inherited strictly positive actual reference.
T1/T2/T3 compensation, all labeled factors two and three, original
records, full-slot corrections, endpoint exclusions and fixed-law
coupling remain. No averaged row or row-specific fit is substituted.

Equations (D9) and its three cases are only a sharper necessary
part of (D10)–(D11). They do not establish rank, a full normalized
solution, strict improvement, ceiling optimality or maximal amplitude.

## 6. Exact gap and bounded stop

This sitting proves additional actual-law signs and cancellations,
not merely the previous conditional D2 criterion:

- Both actual canonical C5 corrections have the new strict bounds (C4).
- Delta f5 and Delta f6 are strictly positive.
- Delta f4 and Delta f7 have disjoint zero branches.
- The allocation-free D2 core coefficient is below -1/12000.
- The exact remaining canonical contribution is (D6), with
  the necessary threshold (D8) for cancellation.

The smallest remaining branch facts on this route are whether the
actual d equals d4 or d7, and the actual comparison in (D6).
On either exceptional branch, the relevant C_c or C_ell zero case
and all remaining (D10) equations must still be solved. This is a
precise unresolved premise, not a claim that further source reasoning
is impossible or that a named coefficient alone settles the full problem.

Stop at this bounded packet for independent review. No successor is
self-assigned and no new lettered gate, source exception, executor,
runtime, scientific-body read, automatic scientific arithmetic, H/z,
new amplitude, graph/LP, repository/Git/index, measurement or RET work
is authorized or performed. Original rejected-candidate history and
the accepted positive family remain unchanged. There is no physical
QM, geometry, mass/gravity, empirical or all-size claim.

