# GDM009 — the restoring link increases fixed-time weak-force susceptibility

**Accepted scoped conditional mathematics.** For the Hamiltonians, preparation and continuously applied constituent force specified below, at h=ell/(4c) the linked pair has strictly larger arithmetic-center displacement susceptibility than the unlinked pair. Both meet the separation criterion |q|<ell throughout this readout, including a common open neighborhood of zero force. This binding-sensitive mechanical observable alone identifies neither gravitational charge nor a gravity-specific law. The separate scientific review and acceptance are described in [REVIEW.md](REVIEW.md) and [ADOPTION.md](ADOPTION.md).

## 1. Protocol and exact baseline

Use the supplied Hamiltonian

H_chi,F=K(P1)+K(P2)+chi kq²/2−F(X1+X2),
K(P)=sqrt(e²+c²P²),

where e,c,ell>0, k=e/ell², d=4ell, q=X2−X1−d, R=(X1+X2)/2 and chi=0 (unlinked) or chi=1 (linked). The readout time is fixed at h=ell/(4c). The initial state is X1=−d/2, X2=d/2, P1=−e/(10c), P2=e/(10c), independent of F. There is no common kick.

With K_i=K(P_i), the complete equations have the prescribed force sign (dots denote differentiation with respect to t):

Xdot_i=c²P_i/K_i,
Pdot1=chi kq+F, Pdot2=−chi kq+F.

F is the force on EACH constituent; total momentum obeys Ptotal_dot=2F. This is a continuously driven protocol, not an isolated pair after a finite impulse.

Define tau=ct/ell, y=q/ell, r=R/ell, a=c(P1+P2)/(2e), b=c(P2−P1)/(2e), lambda=Fell/e, and f(u)=u/sqrt(1+u²). Primes on a, b, y and r denote differentiation with respect to tau; derivatives of f and K are with respect to their displayed arguments. The exact equations are

a'=lambda, b'=−chi y,
y'=f(a+b)−f(a−b),
r'=[f(a+b)+f(a−b)]/2,

with a=y=r=0 and b=b_star=1/10 initially. At zero force, a=r=0 and the relative baseline is

y_chi'=2f(b_chi), b_chi'=−chi y_chi,
y_chi(0)=0, b_chi(0)=b_star.

The unlinked baseline has b_0=b_star. These are newly established zero-common-kick baselines, not GDM007's signed-kick trajectories.

## 2. Support and differentiability through the fixed h

For either chi and any bounded force parameter interval, |Xdot_i|<c bounds positions and separation on finite times. Linear restoring forces plus constant F then bound momenta. The smooth canonical vector field therefore has a unique uninterrupted finite solution and smooth parameter dependence on [0,h].

At zero force the free case has y_0=2f(b_star)tau<tau/5 for positive tau. For the linked case, initially y'>0; until a possible first exit from 0<b<b_star, y>0, y'=2f(b)<2b_star=1/5, and b'≤0. Integration gives

y_1≤tau/5,
b_1≥b_star−tau²/10=b_star(1−tau²)≥3/32>0

through tau_h=1/4. This excludes a first zero of b; positive y excludes a return to b_star. Thus 0<b_1<b_star for every positive time through readout. In both cases 0≤y<1/20 throughout [0,h], so |q|<ell with a strict uniform margin. Fixed e stays positive.

Smooth dependence is uniform on this compact interval. Consequently some common delta>0 ensures |F|<delta keeps each perturbed separation within, for example, ell/4 of its zero-force separation. Both still satisfy |q|<ell. This neighborhood and the smooth flow justify the derivative at fixed preparation and h. No long-window T theorem is asserted.

## 3. Exact force-variational IVP and finite-time integral

Let xi_i(t)=partial_F X_i(t)|0 and pi_i(t)=partial_F P_i(t)|0. Since preparation is independent of F, all four variations start at zero. Along the zero-force baseline define

D_chi(t)=K''(P1^0(t))=K''(P2^0(t))
        =(c²/e)[1+b_chi(ct/ell)²]^(-3/2).

The exact linear IVP is

xidot1=D_chi pi1, xidot2=D_chi pi2,
pidot1=chi k(xi2−xi1)+1,
pidot2=−chi k(xi2−xi1)+1.

Subtracting gives the homogeneous relative-variation system, with zero initial data. Uniqueness gives xi2−xi1=pi2−pi1=0. It follows that pi1=pi2=t and hence

S_chi(h)=partial_F R_chi,F(h)|0
        =(c²/e) integral_0^h t [1+b_chi(ct/ell)²]^(-3/2) dt
        =(ell²/e) integral_0^(1/4) tau f'(b_chi(tau)) d tau.

The integral with the displayed baseline IVP is an exact implicit value. No instantaneous acceleration, small-time approximation or finite-kick coefficient replaces it. S has length/force units.

Since f'(b)=(1+b²)^(-3/2) strictly decreases for b>0, the proved 0<b_1(tau)<b_star implies, for every positive tau≤1/4,

f'(b_star)<f'(b_1(tau))<1.

Integration with positive weight tau establishes the fixed-h result

0<S_0(h)=(ell²/(32e))(1+b_star²)^(-3/2)
 <S_1(h)<ell²/(32e).

Thus the strict difference is established at the assigned finite time, rather than inferred from its early-time sign.

## 4. First nonzero small-time difference

As a separate local cross-check, write S_chi(t) for the same susceptibility evaluated at small t and tau=ct/ell. At zero force the linked relative equation is b_1''=−2f(b_1), with b_1'(0)=0. Its even smooth solution gives

b_1(tau)=b_star−f(b_star)tau²+O(tau⁴).

The unlinked b remains constant. Therefore

f'(b_1(tau))−f'(b_star)
 =−f''(b_star)f(b_star)tau²+O(tau⁴),

where f''(b)=−3b(1+b²)^(-5/2). Substituting into the exact response integral yields

S_1(t)−S_0(t)
 =(ell²/e){[3b_star²/(4(1+b_star²)³)]tau⁴+O(tau⁶)}.

The quartic coefficient is positive and nonzero. Equivalently its t⁴ coefficient is 3c⁴b_star²/[4e ell²(1+b_star²)³]. There is no quadratic difference: both start with c² f'(b_star)t²/(2e). This expansion is not used to extrapolate the fixed-h inequality.

## 5. Interpretation and gravity-identification limits

The link reduces outward relative momentum during readout. The nonlinear kinetic derivative K'' is then larger, increasing the first-order center response to the same continuous constituent force. Relative motion has zero first-order force variation, but its different unforced histories enter the center's susceptibility. Both candidates remain organized over this common h.

Retain S_chi(h) as a conditional binding-sensitive mechanical readout. GDM007 instead used a finite signed total impulse, nonzero common momentum and a displacement-per-time ratio. The protocols and observables differ; their response coefficients are not identified. GDM008's rejected position-only boost mapping is unchanged and is not repaired here.

Only with the additional stipulated identification F=m_g*g does the chain rule give

partial_g R_chi,m_g*g(h)|0 = m_g S_chi(h).

Using the same m_g in both models is an added premise. For positive m_g the displacement-per-g response has the same strict ordering; zero charge removes it and a negative charge reverses its sign. For any nonzero common charge the conditional response ratio cancels m_g, which does not determine its value.

The mechanical susceptibility is a derivative with respect to force, not an independent measurement of gravitational charge. A gravity interpretation needs an independently characterized field g and a justified, calibrated coupling mapping that field to each constituent force. It must also specify whether and how interaction energy contributes to the coupling; this assigned external potential adds no separate interaction-charge term. Equal constituent charge across the two laws is not derived from their energies. No value m_g=e/c² is installed.

A calibrated displacement-versus-g observation could infer a charge only conditional on an independently validated response/coupling model. No such calibration or data is supplied here. The arithmetic center is not a physical energy center by derivation, and the model has no established physical boost/worldline completion. The response contrast is consequently neither an equivalence-principle violation nor a native or gravity-specific prediction.

The accepted conclusion is the conditional continuous-force observable. Gravitational and physical-mass identification are withheld for the missing coupling and calibration premises above. The accepted result supplies no physical execution or experiment-readiness claim.
