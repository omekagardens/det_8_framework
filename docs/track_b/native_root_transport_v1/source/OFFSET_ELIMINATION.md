# Same root offset cancellation and exact compatibility conditions

30 September 2026, Honolulu. RI233 manual conditional result for independent
review. The explicit canonical allocation terms cancel from same-root
profile differences. Division-free minors follow, but reference and
cross-root equations remain indispensable. The companion proof shows
that the actual same-root equations in this support are all identities.

## 1. Fixed law and the five offsets

Retain the accepted RI231 notation, actual fixed rho,s,theta and all
original records and ideal occurrences. Write z for the bit on the
intrinsically ordered C3 stem root, and

    chi_z=(35/36)*kappa_z,    gamma_z=1/64,
    T=t0=138697/387200,
    U=Acal[B]+c,             P_Y=1-theta*U.

Acal retains its four fixed weights5/352,5/352,203153/8800,1/8.
These are inherited accepted facts; no original scientific body is
reopened and no coordinate is resolved in this sitting.

For purposes of collecting terms define the following algebraic
offset-free expressions, with every held row kept at its actual value:

    F0=1-theta*(U+t0),
    M20=theta^2*t0,       M30=theta^3*t0,
    X0=V_H+2F0+M20,       Z=V_C+P_Y.

Then exactly

    F_Y=F0-chi_z/64,
    M2=M20+(2theta*chi_z+chi_z^2)/64,
    M3=M30+(3theta^2*chi_z+3theta*chi_z^2+chi_z^3)/64,
    X=X0+((2theta-2)*chi_z+chi_z^2)/64.                     (O1)

Let Bhat_p be the accepted W5 expression for B_p with F0,M20,
M30,X0 in place of F_Y,M2,M3,X, respectively. No replacement
probability law or feasible zero-allocation law is asserted by this
algebraic notation. Other held quantities may be coupled to kappa
through the fixed global selection; they are not freely variable.

Direct collection in all five W5 rows gives

    B_p(r)=Bhat_p(r)+Phi_p(chi_z),                           (O2)

    Phi1(x)=[-3rho*((2theta-2)*x+x^2)-3rho^2*x
                    +rho^3*(3theta^2*x+3theta*x^2+x^3)]/64,

    Phi2(x)=(rho^2-rho)*((2theta-1)*x+x^2)/64,

    Phi3=Phi4=Phi5=0.                                      (O3)

For B1 the three contributing terms are -3rho*X,
3rho^2*F_Y and rho^3*M3. For B2 they are
-rho*(X-F_Y) and rho^2*(F_Y+M2). Both have the same
quadratic combination ((2theta-1)*x+x^2)/64. B3 and B5
contain only V_H,V_C; B4 contains only E4,Z,ell,P_Y,R4,
none of which has an explicit chi term. This checks each of
the five rows rather than assuming a common offset structure.

For any two records r,t with the same root bit,

    B_p(r)-B_p(t)=Bhat_p(r)-Bhat_p(t).                       (O4)

The corresponding full profile is still g_p=1-s*B_p>0.
Its sector reference value contains the actual offset; cancellation
in(O4) does not remove that reference from the original equation.
No equality of chi_0 and chi_1 is assumed.

## 2. Division-free same-root minors and their zero branches

Fix a parent family p and a root sector z. Choose a reference
record o_z in that sector, preserving every other record r.
For this section alone abbreviate

    D_r=Bhat_p(r)-Bhat_p(o_z),
    J_r=l_p(r;W)-l_p(o_z;W),
    G_z=g_p(o_z)>0,       L_z=l_p(o_z;W).

Using(O4), the complete within-sector compatibility equation is

    E_r=G_z*J_r+s*D_r*L_z=0.                               (O5)

For every pair r,t define the division-free linear minor in W

    M_rt=D_t*J_r-D_r*J_t.                                  (O6)

The exact identity

    D_t*E_r-D_r*E_t=G_z*M_rt                               (O7)

proves necessity of every M_rt=0. Only the strictly positive
reference G_z is used to infer this; no possibly zero D,J,
correction or canonical allocation is divided out.

The missing sufficiency conditions can be stated exactly:

- If every D_r=0, all minors vanish automatically. The actual
  equations require every J_r=0, since G_z>0. Minor vanishing
  alone is not enough.
- If some D_t is nonzero, the full within-sector equations are
  equivalent to all M_rt=0 together with the retained E_t=0.
  Indeed(O7) then gives D_t*E_r=0 for every r, hence E_r=0.
  This implication uses the declared nonzero branch; it does
  not introduce a quotient formula singular on D_t=0.

This preserves J=0 branches as well. For example, if every J_r=0
but some D_t is nonzero, the pivot equation forces L_z=0,
not a chosen full-child correction. If D and J both vanish,
within-sector compatibility is automatic, but the reference
intercept L_z and cross-sector equation are still live.

Equation(O6) is necessary after substituting the normalized W
recovery too. A putative nonzero symbolic determinant is not a
proof that an actual minor or actual rank is nonzero.

## 3. Restore the shared cross-sector and reference equations

For each p retain the actual references o_0,o_1 and the single
cross-sector equation

    C_p=g_p(o_0)*l_p(o_1;W)-g_p(o_1)*l_p(o_0;W)=0.          (O8)

There is one full-child correction per parent, not one per root
sector. It is recovered at o_0 using the original positive
denominators. Root-sector fits cannot choose two private corrections.

The within-sector equations(O5) in both sectors plus(O8) are
equivalent to the original complete disconnected record family.
For r in sector z, the division-free transport identity is

    g_p(o_z)*[g_p(o_0)*l_p(r)-g_p(r)*l_p(o_0)]
      =g_p(o_0)*[g_p(o_z)*l_p(r)-g_p(r)*l_p(o_z)]
         +g_p(r)*[g_p(o_0)*l_p(o_z)
                                  -g_p(o_z)*l_p(o_0)].     (O9)

Both bracketed terms on the right vanish by the stated equations;
positive g_p(o_z) gives the original left bracket. Conversely
the original equations give all pairwise compatibilities by the
same identity. This proves equivalence without discarding zero
contrasts, reference information or cross-sector coupling.

## 4. The actual same-root branch is entirely zero

[ROOT_TRANSPORT.md](ROOT_TRANSPORT.md) proves a stronger native
held-row fact: the complete actual C5 row depends only on its
root record, including

    D_empty=theta*B_empty,
    D_pair=theta*B_pair,
    d=theta*b,           e=theta*c.                        (O10)

The singleton reads only the root by locality; normalization
then gives the same property for ell. Together with the accepted
complete C3,C4,H5 root pattern, this proves all five actual B_p,
all their l_p coefficients and all eleven supported connected
full profiles f_j have only root dependence.

Consequently, for every actual same-root pair in this support,

    D_r=0,   J_r=0,   E_r=0,   M_rt=0                      (O11)

for every W, including every substitution with u2=-1. These
equalities are proved on the original record cubes, not obtained
by averaging or selecting two convenient records.

This is a concrete negative yield for the proposed same-root
elimination test: its minors contribute no constraints on the
actual normalized direction. It is not a proof that the full
system is feasible, inconsistent or rank deficient. In particular
it does not relax the fixed kappa values to arbitrary choices.

The cross-root equations(O8), connected contrasts and common
reference recovery remain the exact decision problem. The
following companion gives explicit held-row consequences and
the complete two-sector form of that problem.

## 5. Source and scope

The fixed W4-W8 formulas and six resolved values are inherited
from independently accepted RI231, with its canonical-only
capacity qualification unchanged. RI225 supplies complete ideal
counts and full-profile formulas; RI127 supplies the actual
shared l_p forms and root patterns. The new C5 argument uses
the already admitted RI63 neutral-active-component and strict-mixture
rules, the fixed maximal-deletion definition and precursor locality.

[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json) binds the exact
sources and preserves all prior boundaries by reference. Old
literal certificate exceptions are historical, not reused here.
No scientific body/vector, coordinate, numerical amplitude,
automatic proof arithmetic, graph/LP/runtime, H/z reconstruction,
repository/Git/index, measurement or RET work occurred. This is
a conditional finite theorem, not a full QM, geometry, gravity or
all-size result. Stop at the bounded packet for independent review.
