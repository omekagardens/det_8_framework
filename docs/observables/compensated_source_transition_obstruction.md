# Compensated endpoints: a central two-body transition obstruction

GDM064, 3 November 2026. The [compensated-source construction](compensated_source_endpoint_response.md) has equal listed mass and zero first moment at its two Q=1 endpoints. Those endpoint identities do not establish a connecting isolated motion. This result excludes one precisely supplied mechanical completion: two labelled bodies starting at rest, interacting through an autonomous central potential, and remaining separated throughout. The accepted static clock/free-fall response remains unchanged.

## Exact question

Fix arbitrary m,a,T>0 and a unit vector e_x in three-dimensional Euclidean space. The bodies have inertial masses m and 2m and canonical Hamiltonian

    H = |p1|^2/(2m) + |p2|^2/(4m) + U(|x1-x2|),
    U in C^2((0,infinity)), real and autonomous.

Their labelled endpoints are

    x1(0)=+a e_x,       x2(0)=-(a/2)e_x,
    x1(T)=-a e_x,       x2(T)=+(a/2)e_x,
    p1(0)=p2(0)=p1(T)=p2(T)=0.

Positions are C^2, momenta satisfy p1=m x1dot and p2=2m x2dot, and Hamilton's equations hold pointwise, with one-sided endpoint interpretation. Require finite energies and |x1-x2|>=a/4 at every t in [0,T]. No other body, field-momentum carrier, spin, external forcing, guide, impulse, contact continuation or label swap is included.

The triple (m,a,T) is fixed before asking for existence. U may be chosen for those parameters, jointly with a proposed trajectory; it need not be attractive, monotone, bounded below or Newtonian. This is a full three-dimensional question. Instantaneous endpoint rest is an added assumption, not equilibrium or a held-readout interval. The mass, time and interaction premises are supplied classical structure, not native quantities derived from DET.

## Full-class obstruction

Suppose such a solution exists. Put r=x1-x2, rho=|r|, n=r/rho and mu=2m/3. The positive separation floor makes n well defined throughout. Hamilton's equations give

    p1dot = -U'(rho)n,       p2dot = +U'(rho)n,
    mu rddot = -U'(rho)n.

The relative angular momentum ell=mu(r cross rdot) therefore obeys

    elldot = mu(rdot cross rdot + r cross rddot) = 0.

Initial rest gives ell(0)=0. Thus r cross rdot=0 at every time. Since r is never zero, rdot is parallel to r, and

    ndot = [rdot - n(n . rdot)]/rho = 0.

The oriented unit direction is constant on the connected interval. This conclusion is derived from the vector equations; no one-dimensional trajectory was assumed. A three-dimensional detour cannot evade it. The prescribed endpoints instead require

    n(0)=+e_x,       n(T)=-e_x,

a contradiction. **No admitted solution exists for any fixed positive m,a,T or any allowed U.** Reversing the relative vector along its deduced fixed ray would require collision, which the positive floor excludes. Final rest is not needed for the contradiction, though it remains part of the tested question. Initial rest also need not be an equilibrium: a nonzero radial acceleration at t=0 does not permit rotation of n.

All encountered separations lie in a compact subinterval of (0,infinity), since rho is continuous on [0,T] and bounded away from zero. U and its derivatives are bounded on that image. No singular positive-distance force or discontinuous continuation is admitted by the regularity assumptions.

## Why endpoint balance was insufficient

The same equations give constant total momentum P=p1+p2 and centre of mass X=(x1+2x2)/3. Initial data imply P=X=0 throughout, hence x1=2r/3 and x2=-r/3. Both proposed endpoints meet this requirement.

Energy is also conserved:

    E = (mu/2)|rdot|^2 + U(rho) = U(3a/2).

Both resting endpoints have separation 3a/2 and the same energy. Thus total mass, centre of mass and endpoint energy agreement all survive this screen, but do not establish the transition. The obstruction is zero angular momentum together with noncontact and reversed labelled relative direction.

## Scope and provenance

Reject only this closed central two-body completion. This theorem is not a general impossibility result for isolated rearrangements. It supplies no actuator, alternative mechanism, empirical test, physical mass/time/action unit or gravity derivation. The accepted native maps, dimensionless charge, separately supplied preparation/readout and static observation kernels remain intact. A native birth is not identified with the continuous time used here. No static response coefficient or excluded correspondence was retuned; no GDM063 or CL061 result was transferred.

The scientific author is the existing DET Quantum Relativity chat. Frozen GDM064 REPORT SHA256: 783fad14168005cf7395b0118df3daadbd2e014fe5e0143833b984dfa6bda380. Its final saved report full read was confirmed at 13:47:14 UTC, before 13:52:10; final custody completed 13:48:24, before 13:56:10. The distinct scientific review and coordinator disposition are retained in followthrough-1338-20261103 in the research evidence store; the publication assembly has a separate review.

The earlier question selector's 25-second overrun and E42 coordinator's 22-second overrun remain permanent procedural qualifications. The separate timely prospective question review, fresh coordinator admission and this new proof do not retroactively certify those procedures. No software or empirical execution was performed.
