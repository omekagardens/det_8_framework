# GDM010 independent scientific review

Scientific review: **PASS, subsequently adopted by the coordinator**. This document attributes the completed independent review; it is not a new review by the publication editor. A separate root review confirmed publication equivalence; the frozen preparation candidate remains historical.

The reviewer, distinct from the QR author, independently checked the recorded assumptions and proof by manual mathematics. The review completed on2026-11-01 at04:09:31UTC (October31,18:09:31HST). Its verdict was PASS_RECOMMEND_SCOPED_CONDITIONAL_MATHEMATICAL_ACCEPTANCE, with no findings. Coordinator adoption followed at04:10:28.026108UTC. The following substantive checks reproduce the completed review's assessments.

## Force normalization and baseline

PASS

Differentiating eU((X2-X1-d)/ell)-F(X1+X2) gives Pdot1=(e/ell)U'(y)+F and Pdot2=-(e/ell)U'(y)+F. Thus Ptotal_dot=2F, a'=lambda and b'=-U'(y). With constituent momenta e(a-b)/c,e(a+b)/c and K'=cf, obtain y'=f(a+b)-f(a-b),r'=[f(a+b)+f(a-b)]/2. At F=0, a=0 and oddness of f gives r'=0,y'=2f(b), starting y=0,b=1/10. No evenness assumption on U is required. The arithmetic center, no-common-kick preparation and h=ell/(4c) remain fixed.

## C2 potential, continuation and common support

PASS

U globally C2 makes U' C1 and the canonical vector field C1 in state and F; this suffices for unique local flow and C1 parameter dependence, without U''' or a smoothness claim stronger than C1. On any finite time interval, |Xdot_i|<c bounds positions and q. Continuous U' is bounded on that compact q/ell range, bounding Pdot_i and hence momenta; a finite-time escape is excluded. This argument holds uniformly for F in any bounded parameter interval. Since y(0)=0 and |y'|<2, |y(tau)|<2tau<=1/2 through tau=1/4 for every finite constant F. Consequently |q|<ell holds through the same h for every specified potential, in particular an open common force neighborhood. Neither stability nor long-window organization follows.

## Zero relative variation and exact integral

PASS

K''(P)=(c²/e)[1+(cP/e)²]^(-3/2) is even. The antisymmetric zero-force momenta therefore give equal constituent Hessians D=(c²/e)f'(b). Set J=(e/ell²)U''(y), continuous under C2. Direct linearization gives xidot_i=D*pi_i,pi1dot=J(xi2-xi1)+1,pi2dot=-J(xi2-xi1)+1. Hence eta_dot=D*rho,rho_dot=-2J*eta with zero initial data, whose unique solution is eta=rho=0. Adding momentum variations gives pi1=pi2=t. Therefore S_U(h)=integral_0^h tD(t)dt=(ell²/e)integral_0^(1/4)tau f'(b_U(tau))dtau. This is a fixed-preparation fixed-time force derivative; its units are length/force. S0=(ell²/(32e))f'(1/10)>0. No factor2 from total force belongs in this constituent-force susceptibility.

## Restoring-envelope finite-time bounds

PASS

On the first-exit region 0<=y<1/20,0<b<=b_star=1/10, the assumed 0<=U'(y)<=y gives b'<=0 and y'=2f(b)<=2f(b_star)<1/5. Integrating gives y<tau/5 and b>=b_star-tau²/10>=3/32 through tau=1/4. Initial y'>0 enters positive y; positive b makes y strictly increasing. These strict y and positive b bounds exclude both possible lower/outer exits; b'<=0 excludes an upper-b exit. Thus 3/32<=b<=b_star throughout readout. Since f'(b)=(1+b²)^(-3/2) strictly decreases on b>0, the exact integral gives S_U>=S0 and S_U<ell²/(32e). The latter is strict because b stays positive.

## Equality iff criterion including endpoints

PASS

The weighted integrand tau[f'(b(tau))-f'(b_star)] is continuous and nonnegative. A zero integral forces equality at every tau>0; strict monotonicity of f' on positive b gives b=b_star, also at zero by continuity. Its equation then forces U'(y(tau))=0 and y=2f(b_star)tau, sampling exactly [0,Y0], Y0=1/(2sqrt(101))<1/20. Conversely, U'=0 throughout [0,Y0] makes that free path a solution of the full IVP, and uniqueness gives S_U=S0. Under nonnegative continuous U', failure of vanishing on this closed interval is equivalent to positivity at an interior point: U'(0)=0 and a positive endpoint value persists just inside. Thus the report's strictness criterion is exact within the declared family. Force that acts only beyond Y0 cannot change this equality.

## Explicit nonharmonic member

PASS

U_plus=y^4/4 is globally smooth, bounded below by0 and satisfies U(0)=U'(0)=0. Its derivative y^3 lies between0 and y on[0,1/20], and is positive at every positive sampled y. The already established criterion proves S_plus>S0 without a harmonic term or coefficient expansion.

## Opposite-sign bounded-below negative control

PASS

U_minus=y^4/4-y²/2=(y²-1)²/4-1/4 is globally smooth and bounded below by-1/4, with zero value and derivative at0. It violates the restoring envelope: U'=y³-y<0 on(0,1). Its baseline is y'=2f(b),b'=y-y³. General support gives |y|<1/2 through readout. Starting b=b_star>0 and y=0, y'>0; on y>0,b>=b_star both y' and b' are positive, so their lower boundaries cannot be crossed. Therefore y>0,b>b_star at every positive readout time. Also b'=y-y³<=y<2tau gives b<=b_star+tau²<=13/80. Thus f'(b)<f'(b_star), and positive weighted integration yields 0<S_minus<S0<S_plus at exactly h. Both potentials obey the same finite support criterion and are bounded below. These two counterposed signs disprove determination of the contrast sign by that support criterion or by adding boundedness below. This is not a stability assertion about U_minus.

## Claim boundaries and inherited scope

PASS_WITH_EXPLICIT_LIMITS

The envelope is sufficient, with an exact equality criterion inside it; the report neither proves its necessity over all potentials nor derives it from DET. Kinetic law, canonical structure, preparation and driving term remain supplied. The observable is a conditional mechanical force susceptibility, not physical mass or gravitational charge. GDM009's missing independent field/coupling/interaction-energy/calibration premises remain. GDM007's accepted finite-kick theorem and original finalization incident, and GDM008's rejected mapping family, are preserved. No energy-center/worldline completion, equivalence-principle violation, experiment readiness, runtime or automatic successor is supported.

## Verification and boundaries

The completed review checked twelve literal input identities, the seven author source/control descriptors, three non-freeze output descriptors, exact four-file author inventory and size cap. Its initial truncated display was completed before review analysis. Current hashes identify files; they do not reconstruct continuous historical custody. The original author final checks at04:04:34UTC preceded its effective deadline and this review.

No scientific program, import, test, solver, experiment or benchmark was run. C2 regularity supports the stated C1 flow and parameter dependence, not an unproved stronger smoothness class. The review does not authorize physical mass/gravity identification, stability from finite support, native potential selection, a complete classification, execution or an automatic successor. GDM007's historical finalization qualification, GDM008's mapping rejection and GDM009's coupling/calibration limits remain.

The exact private review is11722bytes, SHA-2564164307e597efb47f2a2cf54053d3da6c533db10d4460ce2d3d61cced476ffe7. SOURCE_MANIFEST.json records the manuscript and disposition identities. Mathematical acceptance, editorial equivalence and remote Git confirmation are separate records.
