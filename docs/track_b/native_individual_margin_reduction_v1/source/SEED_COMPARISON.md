# Exact seed elimination and the remaining native margin test

30 September 2026, Honolulu. Manual conditional theorem accompanying
[INDIVIDUAL_MARGINS.md](INDIVIDUAL_MARGINS.md).

The original fixed seed split is eliminated symbolically:

    K*h=A,       K!=0,       A>59c0/12000>0,
    K=c0*j1-j0*c1,
    A=c0*(lambda*j0+j1-j0),
    h=A/K=-3m*z2/r.                                          (S1)

No numerical seed coordinate or harmonic matrix is reconstructed.
The two original strict margins now reduce to ONE remaining native
inequality after determining the sign of the explicit determinant K:

    K>0:  C3>0 already; both pass iff K*B2>A.
    K<0:  C2>0 already; both pass iff (-K)*(B3-1)>A.           (S2)

All quantities in (S1)-(S2) belong to the unchanged same law and actual
correlated pair. Neither branch's remaining inequality is asserted.
This is a substantive exact reduction, not a proof of both signs,
a refutation of the selected law or a statement of nonderivability.

The A here is the seed numerator in (S1), not the 465-billion
comparison constant in the main note. K is this determinant, not
the complete prefix sums K_i defined below or the historical
77+72theta endpoint abbreviation in the admitted source.

## 1. Original marked harmonic rows determine the relation

The specifically admitted original four-vertex-cap DESIGN equation10
requires the P1 harmonic identity for every retained record. At its
record0 and record1 rows, with z1=1, this gives

    r3_i+3m_i*z2+3j_i*z3=0,       i=0,1.                      (S3)

All three repeated individual ideal occurrences in each coefficient
remain. The already admitted prefix identities give

    r3_1=(1-lambda)*r,       r=r3_0>0,
    m_i=theta^2*c_i,         m=m0>0,
    h=-3m*z2/r,             3j0*z3/r=h-1.

Divide the record1 equation by r>0 and substitute:

    (1-lambda)-(c1/c0)*h+(j1/j0)*(h-1)=0.

Multiplication by c0*j0>0 and collection of the h terms gives
K*h=A exactly. No sign of a contrast or determinant is assumed.

These are necessary identities of the already accepted complete
harmonic seed. They do not replace its other marked rows, canonical
direction rule, z1=1, |z_i|<=1 or amplitude1/4. A vector satisfying
just these two rows is not being proposed as another seed. The
newly admitted DESIGN text does not authorize its historical RREF
procedure, linked executors, certificates or numerical seed fields.

## 2. The complete complements give a positive numerator

Use the additionally admitted RI187 ENDPOINT_CERTIFICATE equation3,
which retains the complete C4 and C3 rows:

    B_i(S)=(w,p_i,s_i,b_i),       S=0,1,3,7,
    sum_S B_i(S)=1-c_i,       0<c_i<1,
    A_C3(0)=A_C3(1)=A_C3(3)=1/44,
    A_C3(7)=41/44,

    K_i=sum_S B_i(S)^2/A_C3(S)+2c_i,
    j_i=1-theta*K_i.                                        (S4)

The symbol A_C3 distinguishes the C3 row from the seed numerator A.
The 2c_i term represents both separate H5 one-cap occurrences.
No proper slot, empty slot or full complement is removed.

Since A_C3(S)>=1/44 and every B_i(S)>0,

    0<K_i
      <=44*sum_S B_i(S)^2+2c_i
      <=44*(1-c_i)^2+2c_i
      =44-c_i*(86-44c_i)
      <44.                                                  (S5)

The second inequality uses the nonnegative cross terms in the
square of the complete proper-row sum. For 0<c_i<1,
c_i*(86-44c_i)>0, proving strictness of the final bound.
Therefore the original two complete complements obey

    1-44theta<j_i<1,       |j1-j0|<44theta.                   (S6)

The accepted native M5 witness supplies theta<2^-38.
In particular 44theta<1/1000: 2^38>2^16=65536>44000.
The previously admitted RI199 analytic proof supplies, for this
same fixed lower law, lambda>3/500 and j0>71/72. Thus

    lambda*j0+(j1-j0)
      > (3/500)*(71/72)-1/1000
      =213/36000-36/36000
      =59/12000>0.                                          (S7)

Multiplying by c0>0 proves A>59c0/12000. These are hand
inequalities on the admitted complete rows, not numerical extraction
of p_i, s_i, b_i, c_i or j_i. The estimate preserves all their
correlations and does not replace the original law by a free box.

## 3. The zero determinant branch is excluded by the existing seed

Before (S7), K=0 could not safely be divided out. Now if K=0,
the original harmonic relation K*h=A would force A=0, contradicting
(S7). The original accepted finite seed exists and h is finite
because r>0. Consequently the actual determinant satisfies

    K!=0,       h=A/K,       sign(h)=sign(K).                 (S8)

This exclusion is conditional on the already accepted existence of
the original complete harmonic seed. It does not prove that every
freely chosen set of positive row values admits such a seed, and
does not construct a new one. No sign of K itself follows from
(S7); its positive and negative branches both remain explicit.

## 4. Exact remaining native inequalities

The main note proves, at the unchanged actual pair,

    C2=(r/(3m))*(B2-h),
    C3=(r/(3j0))*(B3-1+h),
    B2>0,       B3>1+delta,
    delta=4,000,000,000/926,000,000,001.                       (S9)

Substituting (S8), define the fixed expressions

    F2=K*B2-A,       F3=K*(B3-1)+A.
    (3m/r)*C2=F2/K,       (3j0/r)*C3=F3/K.                  (S10)

If K>0, A>0 and B3-1>0 make F3>0, hence C3>0. The
remaining C2 inequality is exactly F2>0, or K*B2>A.
If K<0, B2>0 and A>0 make F2<0, hence C2>0.
The remaining C3 inequality is F3<0, equivalently
(-K)*(B3-1)>A. These prove (S2).

Equality in either branch's remaining test makes that original
margin exactly zero and fails strict local feasibility. The strict
opposite gives an actual negative margin if proved at the fixed law.
Failure of a sufficient bound alone is not such a sign proof.

The two positive contributions are still the complete expressions

    B2=12lambda*theta^3*c0*rho^2*(1-s*U20(rho))/q(rho)
          +12theta^3*c0*s*rho^3*(1+eta),

    B3=12lambda*j0*rho*(1-s*U30(rho))/((1-rho)*v)
          +12j0*s*rho^2*(1+eta).                             (S11)

All q/N_i terms, positive parts, tied branches and full complements
inside them remain. Rho and s have not been set to comparison
endpoints. P2/P3 are unchanged and their positive clearings are
checked in the main note.

## 5. A scale free sufficient strip and a sharper conditional test

The explicit slack gives one sufficient negative-determinant condition:

    K<0 and (-K)*delta>=A    implies C2>0 and C3>0.            (S12)

Indeed this says -delta<=h<0. At equality, B3-1>delta
still gives the strict second inequality in (S2). No such
determinant magnitude bound has been established here.

For any actual h<0, a sharper sufficient comparison is

    M6 <= (T+h/2)/(1-h).                                    (S13)

Here T=4lambda*j0/v-1/2 is the original target. Since 1-h>0,
(S13) is equivalent to (1+2M6)*(1-h)<=2T+1. The main note's
strict B3>(2T+1)/(1+2M6) then gives C3>0 even at equality.
C2 is already positive on this branch.

Using K<0 and A>0, the same sufficient comparison has no seed
coordinate in it:

    8lambda*j0*(-K) >= v*(1+2M6)*(A-K),
    A-K=j0*[c1-(1-lambda)*c0]>0.                             (S14)

The displayed identity follows by expanding (S1); positivity also
follows directly from A>0 and K<0. Every clearing is therefore
justified. This is not a proposed new maximum computation or
containing-domain search. It simply states what the retained
individual-contribution lower bound would need on the original
negative-determinant branch. Neither (S13) nor (S14) is asserted.

## 6. Precise remaining dependency and stopping boundary

The bounded question has been reduced to the actual sign of

    c0*j1-j0*c1

and the corresponding SINGLE inequality in (S2), with j_i and every
other term explicitly defined by (S4), (S11) and the original canonical
law. An independent scalar h input is no longer needed: it has been
eliminated symbolically. This does not evaluate the determinant or
prove the branch's required quantitative comparison.

The accepted upper/lower rho bounds, strict B3 slack, positive A
and nonzero determinant do not by themselves settle that comparison
in this derivation. No independently varied coefficient countermodel
is offered, and no impossibility of further native proof is claimed.

All original records, individual ideal multiplicities and proper/full
distinctions are retained. Even a proof of both local signs would
not solve shared T1, the other eight connected parents, all five Di
or H30 as a whole. The original 92/34/35 and 31/139/20/42 executable
obligations remain unchanged and uncredited. RET remains paused.

Only the two exact additional analytic texts and their narrow
admissions are used. Their descendants and older operational
boundaries stay unexpanded. No scientific body/vector/certificate
parse, automatic proof arithmetic, H/z reconstruction, graph/RREF/LP
execution, runtime/fixture/card, repository or Git/index change occurs.
No new law, amplitude, scale choice, support, agent/thread, physical
discriminator or successor is introduced. Stop at sealed handoff for
independent root adjudication, publication and successor selection.
