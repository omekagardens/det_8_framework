# Exact local amplitude range for a distinct H30 family

30 September 2026, Honolulu. Conditional manual theorem for independent review.

The original amplitude 1/4 candidate remains rejected by accepted RI216.
This note studies a separately labelled prospective amplitude family with the
same baseline law B, normalized seed direction z and thirty-child support.
It does not change or reaccept the original candidate.

For the new family's two local T2/T3 blocks, the exact common positive
amplitude range is

    0 < a < a_star,
    a_star = B2/(4h) = K*B2/(4*A_seed) > 0.                 (A1)

Here a is the bias amplitude, not the held C3 full probability. All lower
coefficients, actual rho/s, canonical q/N_i terms and seed direction stay
fixed. The endpoint a_star is excluded. These local intervals alone do not
decide shared affine compatibility or full H30 feasibility; the companion
checks a complete shared solution on a smaller positive interval.

## 1. Fixed premises and the amplitude change

Use the complete record transport and original equations in RI127
LOCAL_POSITIVITY and RECORD_TRANSPORT. The normalized child directions
remain y; their proposed multipliers are now 1+a*y instead of 1+y/4.
The seven-parent multipliers are 1+a*z_j, with z1=1 and |z_j|<=1.
For a>0, dividing the harmonic equation by a leaves its signed direction
equations unchanged. Only the strict positivity bounds change.

Keep, for j=2,3,

    e_j = q_B(T_j,empty) > 0,
    f_j(r) = q_B(T_j,r,T_j),    k_j(r) = q_B(T_j,r,C3),
    t_j = y_Yj,    v_j = y_F(Tj),    w_j = e_j*y_Jj,
    beta_j = -Delta k_j / Delta f_j > 0,
    Gamma_j = k_j(0)+f_j(0)*beta_j > 0.                     (A2)

The pivots Delta f_j are strictly positive, and f_j(0)>1/2.
The complete compensation minors vanish for every retained record, with
their original complete-cube and relabeling transport. Their proof is a
premise, not a new two-record fit.

Accepted RI216 and its RI212 seed identities give

    r>0, m0>0, j0>0, K>1/5500>0,
    h=A_seed/K>59/12000,
    z2=-r*h/(3m0),
    z3=r*(h-1)/(3j0).                                       (A3)

The last identity follows from r+3m0*z2+3j0*z3=0. Define the
complete positive reference sums

    E_j = e_j+Gamma_j,
    B2 = 12m0*E_2/r > 0,
    B3 = 12j0*E_3/r > 1+delta_W,
    delta_W = 4000000000/926000000001.                       (A4)

These B2/B3 are the original normalized margin contributions, not the
similarly named coefficients inside U20. Both original empty/core terms
are retained. Accepted RI216 gives B2<1/1000 and C2(1/4)=z2+4E_2<0.
No coefficient or scale is newly evaluated.

## 2. Full local reconstruction for any positive amplitude

The complete signed local equations remain

    w_j+k_j(r)*t_j+f_j(r)*v_j=z_j  for every record r.        (A5)

Subtracting reference and pivot rows, and then using every accepted
zero minor, gives exactly

    v_j=beta_j*t_j,    w_j=z_j-Gamma_j*t_j.                  (A6)

There is no division by t_j, and zero t_j is retained when feasible.
For a>0 the three strict child bounds are

    t_j>-1/a,    v_j>-1/a,    w_j>-e_j/a.                    (A7)

Let mu_j=min(1,1/beta_j), a positive fixed number. Substitution gives the
necessary and sufficient open interval

    L_j(a)=-mu_j/a,
    U_j(a)=(z_j+e_j/a)/Gamma_j,
    t_j in (L_j(a), U_j(a)).                                (A8)

Recover the original variables by (A6) and y_Jj=w_j/e_j. Equivalently,

    w_j in (-e_j/a, z_j+Gamma_j*mu_j/a),
    t_j=(z_j-w_j)/Gamma_j,    v_j=beta_j*t_j.                (A9)

All denominators a,e_j,Gamma_j and the original pivots are positive.
The reversal of endpoints in (A9) follows from Gamma_j>0.

The exact local feasibility condition for arbitrary a>0 is therefore

    a*z_j+e_j+Gamma_j*mu_j > 0.                             (A10)

One must not replace mu_j by 1 for arbitrary amplitudes without proving
the appropriate native branch. The simplification used at amplitude 1/4
in RI127 relied on its magnitude bounds, not only on beta_j>0.

For beta_j<1, the lower endpoint makes the Y_j multiplier zero.
For beta_j>1, it makes the F(T_j) multiplier zero. If beta_j=1,
both vanish. At the upper endpoint the J_j multiplier is zero.
All equalities fail strict positivity. If U_j<=L_j, the interval is empty.

When U_j>L_j, any fixed u_j in (0,1) gives the full symbolic parametrization

    t_j=(1-u_j)*L_j+u_j*U_j,                                (A11)

with (A6). This covers the entire local family; it is not a selected
shared solution. The same t_j and w_j must later be used by other parents.

## 3. The actual T2 branch and exact ceiling

The immutable accepted C2(1/4)<0 implies

    0<E_2<-z2/4<=1/4,

using |z2|<=1. Since E_2>Gamma_2>f_2(0)*beta_2>beta_2/2,

    0<beta_2<1/2<1.                                        (A12)

Thus mu_2=1 is proved, not assumed. Also z2<0 by (A3).
For every a>0, (A10) for T2 is exactly

    a*(-z2)<E_2,
    a<E_2/(-z2)
      =[12m0*E_2/r]/[4h]
      =B2/(4h)=K*B2/(4*A_seed)=a_star.                     (A13)

Every factor in a_star is strictly positive and finite. From the
already accepted bounds,

    a_star < (1/1000)/(4*59/12000)
           =3/59<1/4.                                    (A14)

This is a strict bound on a symbolic threshold, not a numerical scale
evaluation or the choice of a new accepted amplitude.

At a=a_star, A10 is zero and U_2=L_2=-1/a_star. The Y2 and
J2 multipliers both vanish there; the F(T2) multiplier remains
1-beta_2>0. Hence there is no strictly positive endpoint solution.
For every a>a_star, the necessary T2 interval is empty. In particular
the already rejected amplitude 1/4 remains outside the new range.

## 4. The exact T3 condition and why it does not reduce the range

For all a>0 define

    B3_tilde = 12j0*(e_3+Gamma_3*mu_3)/r > 0.

The exact T3 test (A10), after multiplication by the positive 3j0/r, is

    a*(h-1)+B3_tilde/4 > 0.                                (A15)

If h>=1 it holds for every a>0. If h<1 it holds exactly when

    0<a<a_3,    a_3=B3_tilde/[4*(1-h)],                     (A16)

with equality excluded. This is the full condition, whether beta_3 is
below, at or above one.

If beta_3<=1 then mu_3=1 and B3_tilde=B3. When h<1,
B3>1+delta_W and h>0 imply a_3>1/4. When h>=1 there
is no T3 ceiling at all.

If beta_3>1, then

    e_3+Gamma_3/beta_3
      =e_3+k_3(0)/beta_3+f_3(0)>1/2.

For any 0<a<=1/4, |z3|<=1 consequently gives

    a*z3+e_3+Gamma_3/beta_3 > -1/4+1/2 > 0.                (A17)

In the h<1 case this also shows a_3>1/2, since
a_3=(e_3+Gamma_3/beta_3)/(-z3) and 0<-z3<=1.
The beta_3=1 endpoint is already included in the first branch.

Thus T3 is strictly feasible throughout (0,a_star), whereas T2 fails
at and above a_star. The exact intersection of the two local admissible
positive-amplitude sets is (A1). The interval is nonempty; a_star/2 is
a symbolic member, not a global H30 candidate selected or accepted here.

For comparison with the historical C3 notation, on 0<a<=1/4 the
unminimized margin C3(a)=z3+E_3/a has normalized expression

    (3j0/r)*C3(a)=h-1+B3/(4a).

Its sign is sufficient and equivalent to local feasibility on that
restricted native range by the branch argument above. The exact
all-positive-amplitude condition remains (A15), not this simplified
formula when beta_3>1.

## 5. Parent positivity and the unresolved shared system

Every a in (A1) lies below 1/4, so the unchanged finite seed direction
satisfies 1+a*z_j>=1-a>3/4 for all eleven supported seven-parents.
The accepted lower harmonic zero relations scale by a without changing
their coefficients. This checks the already specified lower seed
multipliers, not the new eight-child harmonic extension.

At a=0 the multipliers are the unperturbed baseline. The normalized
direction equations arose by division by a and do not select a unique
direction at zero. This trivial baseline is not a positive-amplitude
member of the prospective nontrivial family.

The local intervals retain the original shared t2,t3,w2,w3 values.
They do not choose w_j=0, duplicate shared children across parents or
erase any individual ideal. Shared T1, the other eight connected parents
and all five disconnected systems remain binding. Their affine equalities
are independent of a; making the positivity bounds less restrictive
cannot remove an affine inconsistency.

[SHARED_COMPATIBILITY.md](SHARED_COMPATIBILITY.md) verifies the full
signed system by substituting the accepted seed, and proves a positive
extension on a strictly smaller symbolic amplitude interval. That global
claim depends on checking every shared equation, not on local feasibility
alone. The exact maximal full amplitude, runtime qualification, new
physics and any successor remain unestablished.
