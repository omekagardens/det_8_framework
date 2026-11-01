# GDM009 scientific review record

The accepted manuscript received a distinct manual scientific result review. The recorded verdict was **PASS_RECOMMEND_SCOPED_CONDITIONAL_MATHEMATICAL_ACCEPTANCE**, with no findings. The reviewer began on 2026-11-01 at 03:22:28 UTC, completed premise readback at 03:22:50 UTC and stopped analysis at 03:23:39 UTC. The coordinator records final review completion at 03:24:39 UTC and adopted the result at 03:26:15.617065 UTC.

This document summarizes those actual recorded checks. Preparing this public candidate is editorial work; it is not a new independent scientific review. The reviewer was distinct from the manuscript author. The review explicitly disclosed that parent context included preliminary reasoning, which was not used as scientific evidence; the reviewer manually derived each equation, inequality and expansion from the recorded assumptions. No scientific code, solver or test was used.

## Recorded manual checks

### 1. Canonical equations and new preparation — PASS

Direct differentiation of -F(X1+X2) gives +F on EACH constituent, so Pdot1=chi*k*q+F, Pdot2=-chi*k*q+F and total momentum derivative 2F. With tau=ct/ell, a=c(P1+P2)/(2e), b=c(P2-P1)/(2e), lambda=Fell/e, obtain a_prime=lambda, b_prime=-chi*y, y_prime=f(a+b)-f(a-b), r_prime=[f(a+b)+f(a-b)]/2. The new zero-common-kick preparation has a=y=r=0,b=1/10, distinct from accepted GDM007 a=±1/20.

### 2. Continuation and support at h — PASS

Bounded constituent velocities |K_prime|<c bound positions and q on any finite interval, while the linear force bounds momenta. Smooth canonical flow continues and depends smoothly on F uniformly over the compact readout. At F=0, a=r=0, y_prime=2f(b),b_prime=-chi*y. In the free case b=1/10 and y=2f(1/10)tau<tau/5. In the linked case initial y_prime>0 initiates y>0 and b<1/10; before any first exit, y<=tau/5 and b>=1/10-tau²/10>=3/32 on [0,1/4]. This rules out first zero; y>0 prevents return to upper boundary. Thus 0<b<1/10 for all positive readout times and y<1/20. Strict compact support margin and smooth parameter dependence give a common open force neighborhood with |q|<ell. No T result is transferred.

### 3. Physical force variational IVP — PASS

K_second(P)=c²e²/(e²+c²P²)^(3/2), hence along antisymmetric baseline D=(c²/e)(1+b²)^(-3/2)>0 and both constituent Hessians coincide. With zero initial variations, xi_i_dot=D*pi_i and pi1_dot=chi*k*(xi2-xi1)+1, pi2_dot=-chi*k*(xi2-xi1)+1. The difference pair eta=xi2-xi1,rho=pi2-pi1 satisfies eta_dot=D*rho,rho_dot=-2chi*k*eta with zero data, hence identically zero. Each pi_i=t and xi1=xi2=integral_0^t sD(s)ds. Thus S_chi(h)=(ell²/e)integral_0^(1/4) tau*f_prime(b_chi(tau))d tau. This is an exact implicit finite-time value, not an instantaneous or endpoint replacement.

### 4. Strict finite-readout comparison — PASS

For positive b, f_prime(b)=(1+b²)^(-3/2) decreases strictly. Linked 0<b1<1/10 and free b0=1/10 therefore imply f_prime(1/10)<f_prime(b1)<1 at every positive tau<=1/4. Positive integration weight gives 0<S0=(ell²/(32e))(1+(1/10)²)^(-3/2)<S1<ell²/(32e). The strict finite-h ordering is independent of the series cross-check.

### 5. Quartic cross-check — PASS

At zero force the linked baseline satisfies b_second=-2f(b),b_prime(0)=0. Smooth time-reversal symmetry gives b=b_star-f(b_star)tau²+O(tau⁴). Then f_prime(b)-f_prime(b_star)=-f_second(b_star)f(b_star)tau²+O(tau⁴)=3b_star²(1+b_star²)^(-3)tau²+O(tau⁴). Integrating with weight tau gives S1-S0=(ell²/e)[3b_star²/(4(1+b_star²)³)tau⁴+O(tau⁶)]. Positive coefficient, no quadratic difference, and t⁴ coefficient 3c⁴b_star²/[4e ell²(1+b_star²)³] are correct.

### 6. Units, physical meaning and inherited scope — PASS_WITH_EXPLICIT_LIMITS

S has units length/force because ell²/e has those units; the external parameter is constituent force, not total force. A conditional substitution F=m_g*g gives partial_g R=m_g*S only with an additional coupling premise. Same charge across laws is stipulated, not derived; mechanical response cannot identify it, a native gravitational law, interaction-energy charge, physical energy center or equivalence-principle violation. The ratio may cancel a common nonzero charge without estimating it. GDM007 remains its separate finite-impulse mechanical theorem; GDM008 rejected mapping remains rejected; GDM_F001 remains parked.

## Coordinator checks and accepted limits

The coordinator read the full proof and distinct result review, and separately checked the canonical force sign and total force 2F, equal constituent momentum variations t, zero relative variation, exact response integral, first-exit lower bound 3/32, strict fixed-h ordering, units and positive quartic coefficient. Acceptance retained the conditional binding-sensitive continuous-force observable and withheld physical mass and gravity identification.

The recorded result review checked fifteen unique inputs, all eleven author source/control pins and three non-freeze output pins; the four-file author inventory and its byte cap passed. Those are the historical review's checks. The present publication preparation checked only the exact source set identified in SOURCE_MANIFEST.json and does not claim to have reopened nested source targets or reconstructed continuous historical custody.

The review found no unresolved finite mathematical calculation within its packet. That is a bounded mathematical conclusion, not a general absence claim. GDM007 retains its original procedural qualification, and GDM008's tested mapping remains rejected. Independent field characterization, a justified constituent coupling, interaction-energy treatment and calibration remain necessary for a physical gravity claim.

The accepted scientific status is established by the coordinator disposition. The separate publication-equivalence review completed on 2026-11-01 at 04:11:30 UTC. It confirmed scientific equivalence and identified assembly corrections concerning the public inventory, publication-status wording and administrative source coverage. It also disclosed preliminary editorial thinking before persisted premises. That review was not an unconditional publication approval. The original candidate and review remain frozen; exact final-assembly verification and coordinator publication disposition are separate records.
