# GDM010: law dependence of a finite force response

Scientific status: **ACCEPTED_SCOPED_CONDITIONAL_MATHEMATICS**. See [review](REVIEW.md) and [adoption](ADOPTION.md).

The harmonic spring is unnecessary for the nonnegative contrast proved below. Within the declared restoring-force envelope, strictness has an exact criterion. A prescribed smooth bounded-below alternative has the opposite contrast while retaining the same finite separation support. These are conditional statements about supplied laws, not DET-derived force selection.

Canonical convention: {A,B}=sum_i[(partial_Xi A)(partial_Pi B)−(partial_Pi A)(partial_Xi B)], with Xdot_i=partial_Pi H and Pdot_i=−partial_Xi H. Finite support here means a unique uninterrupted trajectory, finite momenta, fixed positive e and |q(t)|<ell for every t in[0,h]. It does not mean stability. U is real-valued on the whole real line. Primes on trajectories below denote d/dtau; primes on U and f denote derivatives of their arguments. These conventions make the proof standalone.

## 1. Exact protocol, continuation and variational formula

Keep e,c,ell>0, d=4ell, q=X2−X1−d, R=(X1+X2)/2, K(P)=sqrt(e²+c²P²), and

H_U,F=K(P1)+K(P2)+e U(q/ell)−F(X1+X2).

U is globally C2 with U(0)=U'(0)=0. Initially X1=−d/2, X2=d/2, P1=−e/(10c), P2=e/(10c), independently of F. F is constant force on EACH constituent. The readout remains h=ell/(4c).

Use tau=ct/ell, y=q/ell, a=c(P1+P2)/(2e), b=c(P2−P1)/(2e), r=R/ell, lambda=Fell/e and f(u)=u/sqrt(1+u²). Direct canonical differentiation gives

a'=lambda, b'=−U'(y),
y'=f(a+b)−f(a−b),
r'=[f(a+b)+f(a−b)]/2,

with a=y=r=0, b=b_star=1/10 initially. At F=0, a=r=0, and the exact relative IVP is

y'=2f(b), b'=−U'(y), y(0)=0, b(0)=b_star.     (1)

For every such U and finite F, bounded constituent velocities bound positions and y on each finite interval. U' is bounded on the resulting compact y interval; hence momenta also remain finite. The C1 canonical vector field therefore gives unique uninterrupted continuation and C1 dependence on F. In particular |y'|<2 implies |y(tau)|<2tau≤1/2 for 0<tau≤1/4. Thus the common finite-h separation criterion holds, even for the negative control below, and an open force neighborhood exists. This finite-time speed bound asserts no dynamical stability or long-window persistence.

For the force variation at zero, let xi_i=partial_F X_i|0 and pi_i=partial_F P_i|0; all initial variations vanish. Along (1), put

D(t)=(c²/e)f'(b(ct/ell)),
J(t)=(e/ell²)U''(y(ct/ell)).

The complete variational IVP is

xidot1=D pi1, xidot2=D pi2,
pidot1=J(xi2−xi1)+1, pidot2=−J(xi2−xi1)+1.

The differences eta=xi2−xi1, rho=pi2−pi1 satisfy eta_dot=D rho, rho_dot=−2J eta with zero data. Continuous coefficients give eta=rho=0, irrespective of the sign of U''. Consequently pi1=pi2=t and

S_U(h)=partial_F R_U,F(h)|0
      =(ell²/e) integral_0^(1/4) tau f'(b_U(tau)) d tau,     (2)

where f'(b)=(1+b²)^(-3/2). This is the exact finite-readout integral, with length/force units. The comparison value is

S_0(h)=(ell²/(32e))f'(b_star)>0.                            (3)

No coefficient expansion or endpoint approximation is used.

## 2. Declared family: support, nonnegative contrast and exact strictness

Now impose 0≤U'(y)≤y for 0≤y≤1/20. This is a local force-envelope assumption; global convexity or a harmonic law is not assumed.

A first-exit argument in 0≤y<1/20 and 0<b≤b_star gives b'≤0 and y'=2f(b)≤2f(b_star)<1/5. While in that region,

0≤y(tau)<tau/5 for positive tau,
b(tau)=b_star−integral_0^tau U'(y(s))ds
       ≥b_star−tau²/10≥3/32

through tau=1/4. Therefore neither the y boundary nor b=0 can be reached. The upper b boundary cannot be crossed because b'≤0. Initial y'>0 starts motion into positive y. These bounds close the argument and give strictly increasing y throughout readout, with b positive and nonincreasing.

Since f' strictly decreases on positive b, (2) yields

S_U(h)≥S_0(h), with S_U(h)<ell²/(32e).                     (4)

To state the exact equality criterion, define the free endpoint

Y_0=2f(b_star)(1/4)=1/(2sqrt(101))<1/20.

Within this declared family,

S_U(h)=S_0(h)  iff  U'(y)=0 for every y in [0,Y_0].         (5)

Proof: the integrand difference in (2) is continuous and nonnegative. Equality of integrals forces b(tau)=b_star for every positive readout time, and then by continuity at zero as well. Equation (1) forces y=2f(b_star)tau and U'(y)=0 along the entire sampled interval [0,Y_0]. Conversely, if U' vanishes there, that free path solves the full IVP through readout; uniqueness establishes equality.

Thus strict inequality holds precisely when U' is not identically zero on [0,Y_0], equivalently when U'(y)>0 at some y in (0,Y_0). Continuity handles a possible nonzero endpoint value. A nonzero force only beyond the sampled interval does not suffice.

An explicit nonharmonic member is U_plus(y)=y⁴/4. It is globally smooth, satisfies U_plus'=y³ between zero and y on the stipulated interval, and is positive in derivative for every y>0. Hence S_plus(h)>S_0(h). No harmonic quadratic term is required.

## 3. Prescribed bounded-below control reverses the sign

Take exactly

U_minus(y)=y⁴/4−y²/2=(y²−1)²/4−1/4.

It is smooth and bounded below by−1/4, with the required zero value and derivative at zero. It is outside the restoring envelope: U_minus'(y)=y³−y<0 on 0<y<1.

Its zero-force IVP is

y'=2f(b), b'=y−y³.

The general speed bound already gives |y|<1/2 through readout. Initially y'>0. While y>0 and b≥b_star, both y' and b' are positive because y<1/2<1. They therefore cannot cross their lower boundaries. It follows that y>0 and b>b_star for every positive readout time. Finite momenta can also be bounded directly:

b(tau)≤b_star+integral_0^tau 2s ds
       =b_star+tau²≤13/80.

Consequently f'(b_minus(tau))<f'(b_star) at every positive readout time, and (2) proves

0<S_minus(h)<S_0(h)<S_plus(h).                            (6)

Both alternatives satisfy the identical finite separation criterion, at the same h and preparation; both potentials are bounded below. They yield opposite signs relative to the free susceptibility. Thus neither that support criterion alone nor boundedness below fixes the response sign.

## 4. Candidate decision and limits

Retain the finite-readout response as dependent on the declared force law. The harmonic result extends to this weaker envelope, with strict increase exactly when restoring force acts within the free sampled interval. Do not promote finite support into a sufficient explanation of the sign: the specified negative control refutes that inference.

This proves sufficiency and exact equality conditions inside one declared family, not necessity of that family among all possible potentials. The envelope, kinetic law, initial state, canonical structure and external drive remain supplied hypotheses; this work does not establish that DET forces them. The negative control is not restoring near zero, and finite survival over h is not stability.

No physical mass, gravitational charge, native gravity, energy-center identification, equivalence violation or GDM008 repair follows. The independently justified coupling and calibration obligations retained by GDM009 remain. No new small-time coefficient chain, numerical execution, extra candidate family or automatic successor is opened. The result has passed distinct scientific review and coordinator adoption. The separate root review confirms editorial equivalence; publication grants no execution authority.
