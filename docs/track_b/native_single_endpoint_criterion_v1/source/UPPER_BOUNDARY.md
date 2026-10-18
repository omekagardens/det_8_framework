# RI178 upper boundary and the single endpoint criterion

30 September 2026. Manual author proof, pending independent root review.
All quantities belong to the unchanged accepted prefix.

## Result and scope

The normalized upper boundary J(x)=W(x,1/d(x))/r is strictly increasing
on0<x<=R, without the RI173 hypothesis v<=T_R. Together with RI175's
accepted intercept monotonicity, this gives the requested two-endpoint
criterion at R. A further same-domain domination argument proves more:

    W(x,y)<=0 for all 0<x<=R, 0<y<=1/d(x)
       iff I(R)<=0,                                    (1)

where I=a/Q is the lower-y limiting intercept. No slope-regime assumption
is needed. When(1) holds, W is in fact strictly negative at every allowed
positive-y point, including when I(R)=0. The excluded y=0 can still have
limiting value zero; it is never treated as an allowed scale.

The actual comparison I(R)<=0 is not decided. Consequently no actual
W(rho,s), C2/C3, shared H30 or continuation conclusion is asserted.
The result reduces a formal-domain question; it does not solve its remaining
same-law endpoint inequality or supply new physical or ontological evidence.

## Unchanged functions and canonical dependence

Retain the accepted actual-containing domain and positive quantities

    0<x<=R,       1/8<R<12/95<1/4,
    d(x)=2(3-2x+x^2),       0<y<=1/d(x),
    r>0, lambda>0, G_*>0, j_0>0, v>0,
    q(x)>0, q'(x)<0, q(0)>0,
    Q(x)=q(x)(1-x)v>0.                                 (2)

The signs of q' and q(0), and strict increase of I, are now accepted RI175
theorems. Their historical finite RI122 sign premise remains explicit;
neither is being rederived here from general DET axioms or fresh coefficient
evaluation. The new assignment permits their direct use. No RI122 decision
reread, scientific decoding or operational expansion is needed in this proof.

Delta means record1 minus record0. The polynomial in(2) is exactly

    q(x)=(1-theta*x^2)*v
       +(2-theta-2theta*x+theta^2*x^2)*Delta h
       +(3-2theta-2x+theta*x^2)*Delta j
       +(x-2)*Delta N+2Delta(N*omega)
       -theta*x^2*Delta(N*omega^2),                     (3)

with the full actual canonical correction

    N_i=(35/1476)*[41p_i-f_i/2-min(g_(i,0),g_(i,1))]_+/c_i,
    omega_i=44theta*p_i,
    theta=1/[72(1+M5)] in(0,1/144),
    h_i=theta*c_i, m_i=theta^2*c_i,
    ell_i=1-theta-N_i>0.                               (4)

Both zero and positive branches, tied minima and every signed product in(3)
remain. The contrast of a product is not a product of contrasts. No parameter,
global maximum, actual scale or correction is independently adjustable here.

The actual complete reference polynomials are

    U20(x)=3-A*x+B*x^2+C*x^3,
    A=E_0+2+2(1-theta)h_0+(1-2theta)j_0
         +2N_0(omega_0-1),
    B=2m_0+2j_0+ell_0,
    C=theta(E_0-2m_0-3j_0)+theta*N_0*omega_0^2,
    U30(x)=2-x-x(1-x)V_0.                              (5)

A,B,C in(5) are polynomial coefficients, not the weighted a,b or the
local margin C2. All stem sums behind E_0,V_0 include S=0,1,3,7; H5
retains its two separate one-cap ideals. In particular
E_0-3m_0-3j_0 is a strictly positive complete stem sum. We retain

    7/4<U20<3,       3/2<U30<2,
    71/72<j_0<V_0<1,
    0<eta=41^2*(w/b_0)^3<1/32,
    0<j_0+G_*x<1.                                    (6)

The last inequality follows from complete H5 normalization, not independent
coefficient bounds: if K_0=sum_S B_0(S)^2/A(S)+2c_0>2c_0, then
j_0+G_*x=1-theta*K_0+theta^3*c_0*x<1 on(2).
The formal x,y variables do not replace the unchanged actual rho,s.

## Reference complements really increase

Set

    C20(x)=1-U20(x)/d(x),
    C30(x)=1-U30(x)/d(x).                              (7)

These are upper-boundary reference factors, not the actual-baseline
f_j0 premise or the local C2/C3 margins. The companion
[REFERENCE_COMPLEMENTS.md](REFERENCE_COMPLEMENTS.md) proves their strict
increase using the full coefficients(5), not positivity of complements
alone. Its complete argument is summarized here for the product-rule use.

RI157's accepted p_i<1/100 and c_i>1/14, together with(4), give
0<=N_i<14p_i<7/50<1/4, retaining the zero branch. The complete row bounds
then imply

    4<A<7,       0<B<4,       0<C<1.                   (8)

For example the negative N contribution in A is bounded below by -2N,
not deleted: A>E_0+2-2N>71/24+3/2>4. Its upper bound uses omega_0<1
and h_0+j_0<1. The positivity of C follows from its complete sum;
its upper bound uses theta<1/144 and N<1/4. Thus(8) concerns the same
canonical polynomial throughout, not a freely selected coefficient box.

For either U, quotient differentiation gives

    (1-U/d)'=(U*d'-U'*d)/d^2,
    d'=-4+4x.                                        (9)

Direct collection yields

    U20*d'-U20'*d
      =6A-12+(12-12B)x+(-2A+4B-18C)x^2
          +8C*x^3-2C*x^4
      >12-36x-32x^2-2x^4
      >=127/128>0,                                   (10)

and

    U30*d'-U30'*d
      =-2+6V_0+(8-12V_0)x+(-2+2V_0)x^2
      >47/12-4x-2x^2
      >=67/24>0.                                     (11)

The last inequalities hold on the larger interval0<x<=1/4; therefore
they apply on(2). The varying denominator d has not been held constant.
Since d<=6, these also give C20'>127/4608 and C30'>67/864.
The exact continuous extensions at zero are C20(0)=1/2,C30(0)=2/3.
Thus, throughout the actual formal domain,

    1/2<C20(x)<1,       2/3<C30(x)<1.                  (12)

The upper bounds use U20,U30>0. The sharper lower bounds are formal
upper-boundary facts; they do not alter a separately scoped baseline premise.

## Exact upper boundary and every derivative contribution

Substituting y=1/d(x) into RI145 equation21 gives exactly

    J(x)=-1
      +12lambda*[G_*x^2*C20(x)/q(x)
                 +j_0*x*C30(x)/((1-x)*v)]
      +12(1+eta)*x^2*(G_*x+j_0)/d(x).                 (13)

This verifies the assignment's proposed starting identity independently
against the original weighted formula. Neither the y reference correction
nor the last positive term is omitted or counted twice.

Both x^2/q and x/(1-x) are positive and strictly increasing:

    (x^2/q)'=x*(2q-x*q')/q^2>0,
    (x/(1-x))'=1/(1-x)^2>0.                           (14)

The first sign uses the accepted complete q'<0, not a sign assigned to
one canonical product. For the last numerator n=x^2*(G_*x+j_0),
n'=x*(3G_*x+2j_0)>0. Since d>0 and d'<0,

    (n/d)'=[x*(3G_*x+2j_0)*d-n*d']/d^2>0.             (15)

In full, the product and quotient rules give

    J'(x)/12
      =lambda*G_*[(x^2/q)'*C20+(x^2/q)*C20']
       +lambda*j_0/v*[C30/(1-x)^2+x*C30'/(1-x)]
       +(1+eta)*[x*(3G_*x+2j_0)*d-n*d']/d^2 > 0.      (16)

Every displayed bracket is positive by(9)--(15). All derivatives of the
reference factors and denominator are present. This proves strict increase
of J on the whole unchanged interval with no v<=T_R or b-sign hypothesis.

## Two endpoints and the excluded lower limit

RI175 gives

    I(x)=-1+12lambda*[G_*x^2/q(x)+j_0*x/((1-x)*v)],
    I'(x)>0,       I(0+)=-1.                          (17)

Since q(0)>0 and the reference polynomials are finite at zero, (13) also
has J(0+)=-1. This uses the actual accepted nondegenerate q, not an
unjustified generic limit for q_0=q_1=0. RI175 retains that separate audit.

For tau=d(x)y in(0,1], the exact affine-y identity is

    W(x,y)/r=(1-tau)*I(x)+tau*J(x).                    (18)

Consequently RI145's whole curved-domain criterion becomes

    W<=0 throughout the domain
       iff I(R)<=0 and J(R)<=0.                       (19)

Sufficiency follows from both strictly increasing functions being bounded
by their endpoint values and from(18). Necessity for J(R) uses the included
point x=R,y=1/d(R). Necessity for I(R) uses continuity as allowed positive y
tends to zero at x=R. It does not include y=0 or identify it with s.

More generally the exact supremum of W/r over the domain is max{I(R),J(R)};
the supremum of W is r times that maximum.
If I(R)>J(R), this supremum is only the lower-y limit; if J(R)>I(R), it is
attained at x=R,y=1/d(R); if they are equal, every allowed y at x=R has
that value. For x<R, strict increase of both endpoints makes every convex
combination strictly below the maximum endpoint value. These are algebraic
equality rules; the next section excludes some zero cases for this law.

## A stronger domination lemma removes the second comparison

This step uses the accepted size bounds in(6), in addition to the endpoint
monotonicity. It is not an inference that increasing functions share a sign.
At each fixed x define positive same-law aliases

    u=12lambda*G_*x^2/q(x),
    t=12lambda*j_0*x/((1-x)*v),
    E_add=12(1+eta)*x^2*(G_*x+j_0).                    (20)

E_add is the numerator of the last additive contribution in(13), not either
complete-parent E_i. The aliases are fixed functions, not tunable weights.
Then I=-1+u+t and J=-1+u*C20+t*C30+E_add/d.

If I(x)<=0, positivity gives u+t<=1. By(12), the larger reference factor
is positive. Therefore, with U_min=min(U20,U30),

    u*C20+t*C30 <= (u+t)*max(C20,C30)
                  <= max(C20,C30)=1-U_min/d,
    J(x) <= (E_add-U_min)/d.                           (21)

The inequality direction here requires positive reference factors; it
does not follow from u+t<=1 for arbitrary signed factors. In this same law,
(2),(6) give the strict bound

    E_add<12*(33/32)*(1/4)^2=99/128<1,
    U_min>3/2.                                       (22)

Thus the pointwise domination lemma is

    I(x)<=0  implies  J(x)<-1/(2d(x))<=-1/12<0.        (23)

It does not assume or conclude a sign of b. A positive b at an x with a
sufficiently negative intercept would not invalidate this argument.
No correction in q or the reference functions has been dropped.

Now I(R)<=0 implies I(x)<=0 everywhere by RI175, so(23) implies J(x)<0
everywhere. Conversely full-domain W<=0 necessarily gives I(R)<=0 by the
lower-limit argument. This proves the single-endpoint equivalence(1)
without the RI173 slope regime. The requested upper-boundary theorem(16)
and two-endpoint equivalence(19) remain valid; (23) shows that the second
comparison is redundant for full-domain nonpositivity in this fixed law.

## Equality and the remaining actual comparison

All nonpositive endpoint cases are now exact:

- If I(R)<0, both endpoint values are strictly negative and W<0 everywhere.
- If I(R)=0, J(R)<-1/12. For x<R both values are negative; at x=R,
  (18) gives W/r=tau*J(R)<0 for every allowed tau>0. The supremum is0
  and is not attained, because y=0 is excluded.
- If I(R)>0, sufficiently small allowed positive y at x=R gives W>0.
  This invalidates full-domain nonpositivity but does not locate actual rho,s
  or decide their W. No sign of J(R) is asserted in this case.

In particular, I(R)<=0,J(R)=0 and the double-zero endpoint case are
excluded by(23); they are not silently allowed as native equality cases.
If J(R)=0 in the actual law, then necessarily I(R)>0. This is a conditional
logical consequence, not a report that either endpoint vanishes.

Using RI175's positive clearing, the unresolved single comparison is

    I(R)=-1+12lambda*G_*R^2/q(R)+B_cap/v <=0,
    B_cap=12lambda*j_0*R/(1-R),

    equivalently:
    v>B_cap and q(R)>=12lambda*G_*R^2*v/(v-B_cap).     (24)

B_cap is the earlier B capacity threshold, not coefficient B in(5).
The strict v>B_cap branch must be fixed before division; equality there
cannot pass because the q term is positive. Equality in the q comparison
is retained and gives the unattained-zero case above.

Equation(24) is not a new coefficient evaluation, a sign determination,
or a witness that the actual prefix satisfies either inequality. It is now
the complete formal-domain weighted-sign criterion without a slope-regime
premise. The separate RI173 slope theorem remains valid for its own question.

## Evidence and stopping boundary

The assignment, RI175 adjudication and direct independent root proof were
authenticated and read fully. Fresh complete mathematical reads include
RI145 ENDPOINT_REDUCTION, RI157 CANONICAL_CAP_BOUND and RI173 SLOPE_REGION;
the complete current companion derivative proof is checked as author-peer
work. RI175's accepted historical finite-sign consequence is used directly,
not reexecuted or recertified. Exact paths and pins are in the source
manifests; author checks and any genuine diagnostics remain separately
attributed. No independent acceptance of this new proof is self-declared.

All predecessor evidence is immutable. No scientific JSON/vector/coefficient
decode, numerical/symbolic engine, source/helper import, compile, AST, probe,
run, fixture, runtime capture, new agent or repository/index/Git mutation
occurred. RET stays paused; measurement and RI176 remain separate. Preserve
P2/P3,Y=1/4,31/139/20/42,shared T1,other eight parents,five Di,strict
endpoints and every labeled occurrence. No physical QM, geometry, gravity,
mass or ontology claim follows. Root owns independent review, publication
and any successor. Stop at the sealed bounded handoff.
