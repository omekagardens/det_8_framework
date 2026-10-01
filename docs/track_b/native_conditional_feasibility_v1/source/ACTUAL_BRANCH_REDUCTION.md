# RI238 — full-parent elimination of the T4 exception

30 September 2026, Honolulu. Manual source-only author proof, pending
independent review. The fixed finite law and complete RI233 record transport
are unchanged. Every normalized solution has U4=U5=U6=0, even on the
previously unresolved T4 zero-contrast branch. The surviving T7 exception
is carried through D2 and D5 in CANONICAL_COMPARISONS.md.

This is an additional actual-law elimination, not an assertion that the
actual canonical comparisons or the full normalized problem are decided.

## 1. Start from the actual canonical law

Use the accepted RI235 notation, not independent allocations. The C5
singleton correction is exactly its equation C3:

    N_z=(35/1476)
        [41p-f_hook,z/2-min(g_hook,(z,0),g_hook,(z,1))]_+/c_z.

Here the four-event hook is r<a<b,r<x, f_hook is its {r,x} slot,
and g_hook is its {r,a,x} slot. The minimum keeps both selected-atom
marks, including ties; the positive part keeps its zero branch.

At the exceptional canonical P=r<a<b,r<x,o<x, retain every one of
the 32 records and every competing nonnegative canonical coordinate:

    (41/352) kappa_i
       +t(row) mu_(i,l)+v(row) tau_i+n(row) nu_(i,j)<=1,
    M_i=max_(all rows with root i)
             [t(row) mu_(i,l)+v(row) tau_i+n(row) nu_(i,j)],
    kappa_i=(352/41)(1-M_i).

The complete companion constraints and the canonical objective remain
the ones in RI231 CANONICAL_CAPACITY.md. No cost-only optimization or
separate choice of either root sector is made. This note does not
determine which hook minimum is active or which P row attains M_i.

The accepted actual consequences, with Delta X=X_1-X_0, are

    a=41/44, p=1/352, t=theta/8,
    0<theta<2^-38<1/10000, 0<rho<1/8, 0<s<1/4,
    b0-b1=41/22000>1/600, b0,b1>1/2,
    C=Delta c=-9/44000,
    Delta j=theta J, J=148345/(44*1000000),
    K=C+J=139345/(44*1000000), 1/400<K<J<1/250,
    0<=N0<1/200, 0<=N1<1/800,
    d=Delta N, S_N=N0+N1,
    ell=1-theta-N, D_S=theta B_S+N 1_(singleton).

The last row includes the whole proper C5 row; B is the whole C4 row
when its full slot c is included. All size-seven full complements used
below exceed 1/2. These are the unchanged positive reference coefficients.

The RI235 complete connected identities imply U5=U6=0 and

    Delta f4=s rho[theta A4 K+B4 d],
    1<A4<2, -4<B4<-1,
    d4=-theta A4 K/B4,  theta K/4<d4<2theta K,

    Delta f7=s rho(1-rho)[-theta^2 K-(1-t)d],
    d7=-theta^2 K/(1-t)<0.

Thus T4 can leave U4 free only at d=d4>0; T7 can leave U7
free only at d=d7<0. Their zero branches are disjoint. Neither
actual equality is assumed or ruled out by the displayed formula alone.

## 2. Complete T9 and T10 profiles

The RI85 cap shapes are T9=C4 ordinal-sum A3 and
T10=C4 ordinal-sum (C2 disjoint A1). Let

    E4=theta^2+2theta N+352N^2+2ell,
    J9=theta^3+3theta^2 N+3theta N^2/p+N^3/p^2.

For T9, deleting any one of its three maxima leaves P4=C4
ordinal-sum A2. Double deletions leave C5 and the triple deletion
leaves C4. Its complete proper-ideal inventory is:

- Five separate ideals S contained in C4, each with potential
  rho^3 D_S^3/B_S^2, including S=C4.
- Three ideals C4 plus one maximum, each with potential rho^2 ell.
- Three ideals C4 plus two maxima, each with potential 1-rho E4.

These are all eleven individual proper ideals. Expanding the singleton
excess in the first sum gives J9, since the complete C4 probabilities
sum to one. Hence

    V9=3-3rho E4+3rho^2 ell+rho^3 J9, f9=1-s V9.       (A1)

For T10, write its cap a<c and isolated b, all above C4.
Deleting c gives P4; deleting b gives P5=F(C5); their common
deletion is C5=C4+a. Each of the six ideals contained in C5
has potential rho times its corresponding P4 probability, and their
total is rho^2(E4-ell). The other three proper ideals are C4+b,
C4+a+b and C4+a+c, with potentials rho ell, 1-rho E4
and 1-rho, respectively. Thus all nine proper ideals give

    V10=2-rho-rho(1-rho)(E4-ell), f10=1-s V10.          (A2)

No orbit-average replaces these individual slots. The unique-maximum
identity used in A2 includes the old full slot.

Subtraction, before division by any possible zero d, yields

    Delta f10=s rho(1-rho)d[2theta-1+352S_N],           (A3)

    Delta f9=s rho d {
      3[-2(1-theta)+352S_N]+3rho
      -rho^2[3theta^2+1056theta S_N
                      +123904(N1^2+N1N0+N0^2)] }.      (A4)

These identities are valid also at d=0 and at ties or zero positive
parts in the original canonical expression.

## 3. T9/T10 are nonconstant on either exceptional branch

On d=d4, N0<N1<1/800, so S_N<1/400.

On d=d7, use t<1/2 and K<1/250 to obtain

    |d|<theta^2/125,
    S_N=2N1+|d|<1/400+theta^2/125<1/375.

The last inequality follows from theta<1/10000 and
1/375-1/400=1/6000. Therefore S_N<1/375 on either branch.

The bracket in A3 is below -1/20: indeed
352/375<47/50 and 2theta<1/100. The brace in A4 is below -2:
its last term is nonpositive, and
3[-2+1/100+1]+3/8<-2.

Both exceptional d values are nonzero. Consequently

    d in {d4,d7}  implies  Delta f9!=0, Delta f10!=0,
    and every normalized solution then has U9=U10=0.    (A5)

Their signs are opposite to d. This is not a blanket assumption that
T9 or T10 is nonconstant away from the two specified branches.

## 4. The D4 contrast closes the apparent T4 freedom

First obtain an exact complete-stem contrast already implicit in the
accepted six-root row. With

    alpha_s=5/352, alpha_pair=203153/8800,
    Acal[X]=alpha_s(X_empty+X_singleton)
                                  +alpha_pair X_pair+(1/8)X_I,
    U=Acal[B]+c,

the unchanged root values give

    Delta U=[91 alpha_pair-77/4]/44000,  0<Delta U<1/20. (A6)

Indeed the empty and singleton contrasts are zero, the pair contrast
is 91/44000, the I contrast is -41/22000, and Delta c=-9/44000.
The two bounds follow from 23<alpha_pair<24. This is manual
substitution in the already admitted complete row, not new extraction.

The accepted complete disconnected D4 profile is

    Z=2-theta-theta(1-theta)U-(1-theta alpha_s)N,
    P_Y=1-theta U,
    R4=theta^3 U+2theta^2 alpha_s N+theta alpha_s N^2/p,
    Bdisc4=3-rho(E4+2Z)+rho^2(2ell+P_Y)+rho^3 R4,
    g4=1-s Bdisc4.                                      (A7)

Every canonical term in this expression remains actual. Consider
d=d4. Then 0<d<theta/125, S_N<1/400, and direct subtraction gives

    Delta E4=[-2(1-theta)+352S_N]d<0,
                                      |Delta E4|<2theta/125,
    Delta Z=-theta(1-theta)Delta U-(1-theta alpha_s)d<0,
                                      |Delta Z|<theta/10,
    Delta(2ell+P_Y)=-2d-theta Delta U,
                                      |Delta(2ell+P_Y)|<theta/10,
    Delta R4=theta^3 Delta U
               +[2theta^2 alpha_s+theta alpha_s S_N/p]d,
                                      0<Delta R4<theta. (A8)

For the last bound use alpha_s<1, S_N/p<22/25 and
d<theta/125: its upper bound is
theta^3/20+(2theta^2+theta)theta/125<theta.
All bounds retain theta; no zero-theta replacement law is used.

Equations A7–A8 imply

    |Delta Bdisc4|
      <rho(2theta/125+2theta/10)+rho^2 theta/10+rho^3 theta
      <theta,
    |Delta g4|<theta/4.

It follows that the actual D4 b contrast satisfies

    C_4(b):=g4(0)b1-g4(1)b0
      =-g4(0)(b0-b1)-Delta g4*b0
      <-1/1200+theta/4<-1/2400<0.                       (A9)

We used g4(0)>1/2 and b0<1, not an allocation-free substitute.

On d=d4, T7 forces U7=0 and A5 forces U9=U10=0.
The original D4 shared form therefore becomes l4=theta^2 b U4.
Its cross-root equation is theta^2 C_4(b)U4=0. By A9,
U4=0. Off d=d4 the original T4 connected equation already forces
U4=0. Combining both branches proves the unconditional fixed-law result

    Every full normalized solution has U4=U5=U6=0.     (A10)

This proof does not divide by the D2 contrast C_2(c). If that contrast
vanishes, is nonzero, or has either sign, A10 is unchanged. The old
C_c zero alternative is therefore closed by another retained parent,
not silently discarded. Separating actual d from d4 is no longer
necessary for the normalized feasibility decision.

## 5. Two remaining-parent coefficients and a T1 pivot

The following strict coefficients allow complete conditional recovery;
they do not by themselves select the remaining canonical branch.
Define for each disconnected parent

    C_p(x)=g_p(0)x1-g_p(1)x0,
    Astar=1-s(2-rho)>1/2, lambda5=s rho(1-rho)<1/32.

The complete accepted profiles are

    g3=Astar+lambda5 V_H, V_H=j+theta^2 R_H,
    R_H=2c+theta V, 0<V<1056, 0<R_H<3,
    g5=Astar+lambda5 V_C, V_C=ell+theta^2 U+theta alpha_s N.

Hence

    C_3(j)=[Astar+lambda5 theta^2 R_H0]theta J
                                     -lambda5 theta^2 j0 Delta R_H
           >theta/800-3theta^2/32>theta/1600>0.         (A11)

Here |Delta R_H|<3, 0<j0<1 and J>1/400. This strict sign
holds throughout the actual admitted law, independently of d.

On d=d7, Delta ell=theta^2 K/(1-t)>theta^2 K, and

    C_5(ell)=[Astar+lambda5 theta alpha_s(1-theta)
                        +lambda5 theta^2 U0]Delta ell
                            -lambda5 theta^2 ell0 Delta U
             >theta^2[K/2-lambda5 Delta U]>0.           (A12)

For the final strict comparison, K>1/320 because
139345*320=44590400>44000000; lambda5<1/32 and
Delta U<1/20, so the subtracted product is below 1/640.
The coefficient multiplying Delta ell is strictly above 1/2.
No C_5(ell) sign is asserted for arbitrary d.

For completeness the T1 affine pivot needed below is also strictly
positive. In the RI103 full formula, write the complete proper C4
stem sums as

    T3=sum B_S^3/A_S^2, T4sum=sum B_S^4/A_S^3,
    0<T3<1936, 0<T4sum<85184,
    E=theta^3 T3+3theta^2 c+3j,
    nu=theta^3 c, Kheld=theta^6 T4sum,
    f1=1-s[4-4rho E+6rho^2 j+4rho^3 nu+rho^4 Kheld].

The names T3,T4sum in this display are sums, not parent labels.
Subtraction gives exactly

    Delta f1=s rho {
      (12-6rho)theta J+12theta^2 C+4theta^3 Delta T3
                  -4rho^2 theta^3 C-rho^3 theta^6 Delta T4sum }.

Since C<0, |C|<1 and rho<1/8, this is greater than

    s rho theta[11/400-12theta-7744theta^2-85184theta^5]
      >s rho theta/40>0.                                (A13)

To check the last conservative bound manually, theta<1/10000 makes
the three error terms respectively below 1/500, 1/10000 and
1/10000; their sum is below 1/400.

The actual k_1,0=s rho^4 theta^6 b^4/a^3 is positive and has
strictly negative contrast. Thus the inherited coefficients satisfy

    beta_10=-Delta k_1,0/Delta f1>0,
    Gamma_10=k_1,0(0)+f1(0)beta_10>0.                    (A14)

The accepted Gamma2,Gamma3>0 and all other Gamma/beta definitions
remain unchanged. No coefficient value has been numerically computed.

## 6. Scope

A10 and A11 are new unconditional consequences of the fixed finite law.
A5, A9 and A12 explicitly state their branch premises. The companion
retains the full ten-coordinate system and constructs conditional
solutions, without claiming the actual branch is known.

This proof uses only admitted analytic texts and manual algebra.
It creates no executor, source exception, scientific-body read, new
coordinate, numerical amplitude, H/z reconstruction, graph/LP,
measurement, RET, repository/Git/index operation or successor.
It is not a derivation of QM, geometry, mass/gravity or an all-size law.

