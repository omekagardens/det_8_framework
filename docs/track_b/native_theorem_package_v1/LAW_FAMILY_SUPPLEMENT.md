# Law-dependence supplement: fixed and moving harmonic seeds

20 October 2026 public edition of the 18 October proof. Companion to the
[conditional finite-growth theorem package](THEOREM_PACKAGE.md).

The growth principles permit more than one law. A normalized harmonic seed
valid for one law need not remain harmonic after the law changes. Nevertheless,
for the explicit family below, a replacement seed can be written symbolically.
The [singular-law kernel and width theorem](SINGULAR_LAW_WIDTH.md) completes its
classification: the eleven-column harmonic system has rank ten and a
one-dimensional kernel throughout the declared family. Away from \(\chi=0\),
the normalized seed is unique and changes the target width. At any \(\chi=0\)
law, every harmonic direction is target-width-blind; the admitted bound on
\(\theta\) excludes the formal compatible alternative printed below.

Only occurrence remains unselected: with
\(\Xi=\theta+360\mu_1-359\mu_0\ne1\), there is one exceptional law exactly
when \(\Xi>1\), and none when \(\Xi<1\). No coefficient search is needed
for the kernel and width classification.

These results concern positive prefixes through seven births and a one-birth
width gain. They do not transfer the later h8 constructions or exclusions,
and do not establish informative quantum dynamics or physical geometry.

The [admitted model](THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model)
and [fixed seed and support](THEOREM_PACKAGE.md#2-the-finite-harmonic-question)
are stated in the theorem package.
The [finite-prefix scaling proof](LAW_DEPENDENCE.md#proposition-1-complete-finite-prefix-admissibility)
and [distinction between law and coordinate choices](LAW_DEPENDENCE.md#4-optional-law-choices-are-not-coordinate-gauges)
provide the common premises.

**Notation across the package.** Here `e=q(C5,C4)` is the theorem package's
`e′` in §2, not its smaller-seed `e=1/44` in §1. Here `f_i` is the
package's `ell_i` in its held-row identities, not its later full-slot `f_j`.
These are notation correspondences; no probability is changed.

## 1. The optional choice and the complete-law premises

Work within the admitted conditional model: every ideal is eligible and has
positive probability; complete rows normalize; newborn record bits are fair
and immutable; proper transitions obey precursor-record locality; relabelings
transport order, precursor and marking together; and every incomparable-birth
diamond agrees on the whole unnormalized scalar-passive payload map q1*q2/4.
The underlying law and these premises are not derived here from bare DET.

For any valid prefix ending at parent size n>=1, the following last-layer change
is valid for 0<lambda<=1:

    q_lambda(P,r,S)=lambda*q(P,r,S)              for S proper
    q_lambda(P,r,P)=1-lambda+lambda*q(P,r,P)      for S full.

Smaller-parent rows remain unchanged. Complete normalization and positivity
are immediate. Each diamond contained in the prefix has either no changed
factor or one changed proper second factor on each route. This includes
full first births at the preceding layer. Both routes therefore acquire
the same factor: one on unchanged diamonds, lambda on changed diamonds.

This prescription does NOT specify later layers. Leaving them unchanged,
or simply applying the same proper-only scaling at every layer, generally
breaks a mixed full/proper diamond. Later potentials and normalization
choices must be rebuilt from the changed prefix.

The family studied below applies this operation at parent FIVE, preserving
the original prefix through parent four. Parent six is then rebuilt with
the admitted positive common-scale continuation. Its scale rho_lambda is
recomputed, not held equal to the old scale.

For comparison, a change at parent four is a different problem. If
b=q(C4,C3), c=q(C4,C4), then b_t=t*b and c_t=1-t+t*c. Any compatible
parent-five continuation must satisfy

    h_t/d_t=c_t/b_t=c/b+(1-t)/(t*b),

where h is an H5 one-cap probability and d=q(C5,C3).
For t<1, the old h and d cannot both remain fixed. This identity does not
select that continuation. The replacement theorem below does not silently
supply a q5 law for a changed parent-four prefix.

## 2. The seed and the full family of harmonic equations

Retain the theorem package's eleven unmarked seven-order classes
T_j=C3 ordinal-sum Q_j, where Q_j runs over all four-element orders with
at least two maxima, in the original fixed order.
One record-blind value z_j is shared across every occurrence of T_j.
Set h_n=1 for n<=6 and

    h7(T_j)=1+epsilon*z_j; h7=1 elsewhere; z1=1.

The admitted original seed has every z_j nonzero and |z_j|<=1.
All supported births are proper. The complete incidence inventory has
five affected six-parent classes and all 320 marked rows.
For a common parent-six scale, harmonicity is M*z=0; that positive scale
cancels. Changing the scale alone leaves the kernel unchanged.

Let a,b,c denote the original C3/C4 held probabilities; g,h,j the original
H5=C3 ordinal-sum A2 probabilities; and d,e,f the original C5 probabilities.
Here g,h,d,e are proper, while j,f are full.
For the parent-five scaling define

    J=1-lambda+lambda*j, F=1-lambda+lambda*f
    U=a*g^3/b^3, B=h^2/c, C=d*g/b, E=e*h/c
    V=d^2/b, W=e^2/c.

The entire supported matrix, with its individual forward multiplicities, is

    P1: lambda^3*U*z1+3lambda^2*B*z2+3J*z3=0
    P2: lambda^2*C*z2+lambda^2*E*z4+lambda*h*z5+J*z6+F*z7=0
    P3: lambda*g*z3+2lambda*h*z6+J*z8=0
    P4: lambda^2*V*z4+lambda^2*W*z9+2F*z10=0
    P5: lambda*d*z7+lambda*e*z10+F*z11=0.               (1)

Unsupported ideals have zero correction, not zero probability.
Parents outside the five cannot receive a supported child.

The admitted original held law has complete root-only C4/H5/C5 rows,
including full complements and the C5 singleton correction. Scaling preserves
this property. Every row in (1) therefore equals its root-sector row i=0 or 1,
with all order/record restrictions transported. The resulting ten equations
cover the full marked domain; they are not ten sampled observations.

The exact fixed-law identities used are

    a=41/44; g_i=theta*b_i^2/a; d_i=theta*b_i
    e_i=h_i=theta*c_i; f_i=1-theta-mu_i; theta>0
    b0=8077/8800; b1=40303/44000
    c0=81/1100; c1=3231/44000; j1>j0>0.                 (2)

These are additional admitted instance facts, not universal growth principles.
The mu_i remain symbolic. In particular, the changed full probabilities are
J and F, not the unchanged complements in (2). The admitted bounds
\(0<\theta<10^{-10}\) and \(0\le\mu_i<1/26\), together with the complete
held-row identities, also imply that the singular compatibility condition
below cannot hold. The [standalone proof](SINGULAR_LAW_WIDTH.md) states these
additional premises explicitly and proves the required sign.

## 3. Why the fixed seed fails

For the original seed, P3's new residual is exactly

    lambda*(g*z3+2h*z6+j*z8)+(1-lambda)*z8
       =(1-lambda)*z8 != 0 for lambda<1.                (3)

At lambda=1/2 its complete proposed harmonic row sums to
1+epsilon*rho_lambda*z8/2, not one.
The changed baseline is admissible; its perturbation by the unchanged old
seed is not. A common scale change or nonzero rescaling of the old vector
cannot remove this residual.

More generally, any fixed vector with z1=1 has the P1 residual

    U*lambda^3+3B*z2*lambda^2+3(j-1)*z3*lambda+3z3.

Its leading coefficient U is positive, so no single normalized vector can
work on an interval. This is not a prohibition on different seeds z(lambda).

## 4. Explicit moving seeds and the possible exceptional point

Use two-component columns over the two root sectors:

    G=(g0,g1)^T, H=(h0,h1)^T, D=(d0,d1)^T
    U=(a*g0^3/b0^3,a*g1^3/b1^3)^T
    J=(J0,J1)^T, F=(F0,F1)^T.

Write [X,Y]=X0*Y1-X1*Y0 and set

    K=[H,J], Delta=[D,H], chi=[H,F].

The first two pivots are always nonzero:

    K=(1-lambda)*(h0-h1)+lambda*(h0*j1-h1*j0)>0
    Delta=theta^2*(b0*c1-b1*c0)<0.                      (4)

For the second sign, b0*c1-b1*c0=(82*c0-9*b0)/44000;
c0<3/40 and b0>9/10 give 82*c0-9*b0<-39/20.

The remaining pivot is affine:

    chi(lambda)=(1-lambda)*(h0-h1)+lambda*chi(1).        (5)

Moreover chi(1)!=0. Otherwise f would be proportional to H, and the original
P5 row, together with Delta!=0, would force z7_old=0, contradicting the
admitted seed. Thus chi has at most one zero in (0,1], never at 1.
If chi(1)>0 there is none; if chi(1)<0 the unique exception is

    lambda_star=(h0-h1)/((h0-h1)-chi(1)) in (0,1).        (6)

Equivalently, \(\chi(\lambda)=\theta c_0(1-\lambda\Xi)/360\), where
\(\Xi=\theta+360\mu_1-359\mu_0\ne1\). The comparison of the actual
fixed \(\Xi\) with one remains unselected. It controls occurrence only;
the singular kernel and its width image are classified below.

Define the ordinary two-by-two formula

    Pair(X,Y;R)=([R,Y]/[X,Y], [X,R]/[X,Y]).

It returns the unique (u,v) satisfying X*u+Y*v=R when [X,Y]!=0.
For chi!=0, set z1=1 and compute symbolically

    (z2,z3)=Pair(3lambda^2*theta*H,3J;-lambda^3*U)
    (z6,z8)=Pair(2lambda*H,J;-lambda*G*z3)

    X=lambda*D; Y=lambda*H
    Q=-lambda^2*theta*G*z2-J*z6

    (k,z7)=Pair(Y,F;Q)
    (z10,z11)=Pair(Y,F;-X*z7)
    (z4,z9)=Pair(X,Y;-2F*z10/(lambda*theta))
    z5=k-lambda*theta*z4.                               (7)

All denominators are nonzero by (4)–(5). These expressions are rational
functions of lambda with the original fixed coefficients; no numerical
matrix or coefficient allocation has been computed.

To verify completeness, (2) gives B=theta*h, C=theta*g, E=theta*h,
V=theta*d and W=theta*h. The first two lines solve P1/P3, and the rest solve

    Y*(lambda*theta*z4+z5)+F*z7=Q
    X*z7+Y*z10+F*z11=0
    lambda*theta*(X*z4+Y*z9)+2F*z10=0,

which are exactly P2/P5/P4. Conversely these equations force (7).
The normalized seed is therefore unique. The full eleven-column seed matrix
has rank ten and a one-dimensional kernel on this branch.

At the possible exception chi=0, the first two lines of (7) still determine
the four front coordinates and Q. Put kappa=F0/Y0=F1/Y1>0.
The following is the formal algebraic alternative before applying the
additional admitted bounds: a normalized seed exists exactly when

    [Y,Q]=0.                                             (8)

If this fails, no z1=1 seed exists there, although a width-blind direction
remains. If it holds, all normalized solutions are

    z11=w; z10=-kappa*w; z9=2*kappa^2*w/(lambda*theta)
    z7=z4=0; z5=Q0/Y0, with w any finite real number,     (9)

together with z1=1 and the fixed front coordinates.

The [singular-law proof](SINGULAR_LAW_WIDTH.md) now establishes \([Y,Q]<0\)
throughout this declared family using the admitted \(\theta\) bound. Thus
(8) cannot hold here: (9) remains a formal compatible solution formula, not
an available family branch. At any \(\chi=0\) law the full unnormalized
kernel is exactly the span of
\[
 (0,0,0,0,0,0,0,0,\ 2\kappa^2/(\lambda\theta),-\kappa,1).
\]
The kernel has dimension one and the system has rank ten. Every direction
has zero target-width correction. This does not decide whether an exceptional law occurs.

## 5. What persists, and what does not

At lambda=1, (7) equals the original seed by uniqueness.
Because chi(1)!=0, its rational formulas are continuous in a sufficiently
small one-sided neighborhood of 1. The original margins
1+z_j(1)/4 are at least 3/4. Consequently amplitude epsilon=1/4 remains
strictly positive locally, and the old nonzero coordinate signs persist.
No numerical neighborhood radius is claimed.

For any nonexceptional lambda, the choice

    epsilon=1/[2*(1+max_j |z_j|)]>0

makes all h7 multipliers greater than 1/2.
Complete harmonicity, positivity and the original shared-terminal telescoping
argument then give an admissible prefix through seven births.

At the complete width target row, subtracting three times the P1 harmonic
equation from its width functional leaves lambda^3*U0*z1. Hence

    one-birth width gain=epsilon*rho_lambda*lambda^3*U0>0.

This is not conditioning on a selected birth or newborn record.
It proves a one-birth gain, not persistent width, asymptotic geometry,
or an all-size record-blind continuation.

The fixed seed is law-dependent. A moving normalized seed and positive
finite-prefix target-width gain survive at every nonexceptional law.
At an exceptional law the displayed width-blind kernel vector still gives
strictly positive multipliers at sufficiently small amplitude and an admissible
prefix through seven births. All harmonic directions there have zero target
width gain. Rank ten and kernel dimension one hold throughout the declared
family; only the occurrence comparison for Xi remains unselected.

The [exceptional-law width witness](SINGULAR_OBSERVABLE_WITNESS.md) concerns
a different admitted parent, \(P_4=C_4\oplus A_2\). Conditional on \(\Xi>1\),
write the exceptional kernel multiplier as \(1+\eta w\). Its exact positive
interval is \(-\lambda_*\theta/(2\kappa^2)<\eta<1/\kappa\); the full-row
\(P_4\) width contrast is nonzero iff \(\eta\ne0\), in both root sectors.
All eight ideals and sixteen marked outcomes are retained. This requires
complete child-order access and the known parent embedding, not a physical
detector or an implemented sampler; the \(P_1\) blindness above is unchanged.

The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) normalizes a
kernel section by \(v_{11}=1\) without dividing by \(\chi\). Conditional on
\(\Xi>1\), a single fixed amplitude gives a multiplier floor \(1/4\) and
positive \(P_4\) width contrast throughout an existence-defined neighborhood.
The uniform bound \(\delta_{4,i}/\rho_\lambda>1/4\) is scale-normalized;
it supplies no uniform absolute signal guarantee without an additional
lower bound on \(\rho_\lambda\). No continuity of the baseline scale is assumed.

The [positive-contrast limit](POSITIVE_CONTRAST_LIMIT.md) also treats approach
to a possible exception. If \(\Xi>1\), the absolute target-width contrast of
every strictly positive harmonic perturbation on this support has a local
uniform \(O(|\lambda-\lambda_*|^2)\) upper bound. Normalization and amplitude
may vary arbitrarily with the law parameter. This needs no continuity or
uniform positive lower bound of \(\rho_\lambda\), and claims neither a sharp
rate nor convergence of raw expected widths or entire laws.

No uniform amplitude over the whole interval, positivity of an h8 lift,
transfer of the fixed 30/33/38 exclusions, canonical active-set preservation,
informative quantum dynamics, Lorentzian structure, mass/gravity derivation,
or empirical correspondence follows. The eleven-coordinate seed kernel is
not the later thirty-class kernel. Metric-as-record remains unvalidated;
the retired gravity proposal and separate software/measurement projects
are unaffected.

## Provenance and status

This supplement consolidates two independently accepted manual proofs:
*Harmonic-seed dependence on the optional growth law* and
*Replacement harmonic seeds for the parent-five scaling family*.
Their exact source identities and acceptance records are retained privately;
[public provenance and evidence limits](PUBLICATION_NOTE.md) state what this
edition supplies and what it withholds.
The complete held-law and original seed premises remain load-bearing.
No scientific executor, new coefficients or production dependencies were used.
The fixed/moving seed statements retain their independent manual acceptance.
The companion [singular-law proof](SINGULAR_LAW_WIDTH.md) resolves the formal
compatibility alternative under the declared bounds and identifies the exact
remaining occurrence premise. This publication supplies mathematical exposition,
not a new numerical execution or a reconstructed finite certificate.
