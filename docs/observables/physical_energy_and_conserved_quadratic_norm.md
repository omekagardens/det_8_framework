# Physical energy and a conserved quadratic norm

In the fixed conventional charged-particle model below, indefinite physical energy is conserved under both declared magnetic controls. A positive conserved quadratic norm exists at b=3 and is impossible at b=0. Their single registered trajectories have the same energy and different terminal state norms. This distinguishes physical energy from a norm certificate; it does not construct a physical work store or derive native units.

The result has a distinct scientific proof review and Classical lane acceptance. Programme recipient admission and publication assembly review are recorded separately. This is conditional mathematics, not empirical evidence.

## Fixed question and supplied premises

The control supplies m>0, q>0, omega0>0 and L>0, a Cartesian inertial frame, clock, static fields, Lorentz update and ideal readout. The question is only the existence of one real symmetric P_b>0 with trace(P_b)=4 and F_b^T P_b+P_b F_b=0, separately for b=3 and b=0. There is exactly one registered initial trajectory, s_star=(1,0,0,0), per control. The initial unit ball is the domain of an analytic bound, not a set of additional trajectory probes. The physical window is 0<=t<=1/omega0, equivalently 0<=tau<=1.

## Result and decision

For b=3, an explicit dimensionless positive conserved quadratic C_3 exists with trace-four matrix and comparison constants 1/3 and 5/3. Consequently the full planar state obeys ||s(tau)||^2 <= 5||s(0)||^2 <= 5 throughout the prescribed window. For the registered initial state, C_3=1 gives the stronger certificate ||s(tau)||^2<=3.

For b=0, no real symmetric positive definite matrix satisfies the required conservation identity, regardless of trace normalization. Nevertheless that same finite linear system has finite-window bounds. Both registered trajectories conserve the same physical energy H=-m*omega0^2*L^2/2, while their terminal state norms differ explicitly below.

Thus the indefinite sign of the supplied physical energy alone does not decide whether this positive conserved norm comparator exists. A change in the specified magnetic control changes the comparator decision under the same Lorentz law. C_3 is not the physical H, a work store or a native energy unit.

## Check 1 — fields, signs, units, planar closure and update

The supplied potential and fields are

    Phi = m*omega0^2*(2*z^2-x^2-y^2)/(2*q),
    E = (m*omega0^2/q)*(x,y,-2*z),
    B_b = (b*m*omega0/q)*e_z,  b in {3,0}.

With rdot cross e_z=(ydot,-xdot,0), the supplied equation m*rddot=q*(E+rdot cross B_b) gives

    xddot = omega0^2*x + b*omega0*ydot,
    yddot = omega0^2*y - b*omega0*xdot,
    zddot = -2*omega0^2*z.

The last equation and zero initial z,zdot imply z=zdot=0 by uniqueness for the linear initial-value problem. This is a closure check, not an extra axial trajectory experiment.

Set tau=omega0*t and s=(X,Y,U,V)=(x/L,y/L,xdot/(omega0*L),ydot/(omega0*L)). A prime denotes d/dtau. Write r=(X,Y)^T, v=(U,V)^T and

    J = [ 0  1 ],  J^T=-J,  J^2=-I.
        [-1  0 ]

Then r'=v and v'=r+b*J*v. The generator, in the fixed s ordering, is

            [0 0  1 0]
    F_b  =  [0 0  0 1].
            [1 0  0 b]
            [0 1 -b 0]

For fixed positive supplied parameters this constant-coefficient finite-dimensional system has a unique finite solution on the specified finite window for every initial state in the unit ball. No nonlinear, variable-field or longer-horizon conclusion is needed.

The dimensions are: x,y,z,L length; t time; omega0 inverse time; m mass; q charge; Phi energy/charge; E force/charge; B mass/(charge*time) in the explicitly supplied Lorentz convention. The coordinates s, time tau, b and the matrices/comparators below are dimensionless. The prescribed fields contain the already supplied ratio m/q: this is not a mass-identification experiment.

## Check 2 — physical energy and zero magnetic work

Define the positive supplied energy scale E0=m*omega0^2*L^2/2. The physical energy in the invariant plane is

    H = E0*h(s),    h(s)=v^T*v-r^T*r,
    h(s)=s^T*diag(-1,-1,1,1)*s.

Directly,

    h' = 2*v^T*(r+b*J*v) - 2*r^T*v = 0,

because v^T*J*v=0. In dimensional form the same cancellation is q*rdot dot E plus q*dPhi/dt, with rdot dot (rdot cross B)=0. Both fields are static. This is conservation of particle kinetic plus specified electrostatic potential energy; it does not account for constructing or maintaining the external apparatus.

The displayed diagonal form has both signs on the stated initial unit ball and is not positive definite. This is an algebraic signature statement, not a pair of additional evolved preparations. Magnetic zero work does not mean the magnetic force leaves the trajectory or existence of other invariants unchanged.

## Check 3 — one positive conserved quadratic at b=3

Choose the single matrix

           [1    0     0   2/3]
    P_3 =  [0    1   -2/3   0 ].
           [0   -2/3   1    0 ]
           [2/3  0     0    1 ]

Equivalently P_3 has 2x2 blocks [I,(2/3)J;-(2/3)J,I]. It is real symmetric with trace 4. Its exact multiplication by the registered generator gives

    P_3*F_3 = [(2/3)J    -I    ].
              [   I    (7/3)J ]

This product is skew-symmetric. Hence F_3^T*P_3+P_3*F_3=0 exactly; no numerical residual or tolerance is used.

Let ell=r^T*J*v=XV-YU. The same quadratic is

    C_3 = r^T*r+v^T*v+(4/3)*ell.

Since |ell|<=||r||*||v||<=(||r||^2+||v||^2)/2,

    (1/3)*||s||^2 <= C_3(s) <= (5/3)*||s||^2.

These explicit constants establish positive definiteness. No search for the best comparator, optimization over constants or classification of all conserved quadratics is made. As a sign cross-check at this same control,

    ell' = v^T*J*v+r^T*J*(r+3*J*v) = -3*r^T*v,
    (r^T*r+v^T*v)'=4*r^T*v,

so C_3'=0. This verifies the cross-term sign in the matrix calculation.

## Check 4 — finite obstruction at b=0

For b=0 the generator is F_0=[0,I;I,0]. Consider the algebraic vector w=(1,0,1,0)^T. It obeys F_0*w=w. If a symmetric P>0 satisfied F_0^T*P+P*F_0=0, then

    0 = w^T*(F_0^T*P+P*F_0)*w = 2*w^T*P*w > 0,

a contradiction. This excludes every SPD candidate, including the trace-four candidates requested. The vector is solely a witness for the matrix obstruction; no extra trajectory is solved or observed.

This negative result is not absence of a finite-window solution or bound. For example at this same b=0,

    d(||s||^2)/dtau = 4*r^T*v <= 2*||s||^2,

so ||s(tau)||^2<=exp(2*tau)*||s(0)||^2<=exp(2) on 0<=tau<=1. This finite-window inequality uses the original preparation domain and does not construct a conserved positive quadratic.

## Check 5 — norm certificate and the registered terminal readings

For b=3, conservation and the constants proved above give, throughout the fixed window,

    ||s(tau)||^2 <= 3*C_3(s(0)) <= 5*||s(0)||^2 <= 5.

At the sole registered initial state s_star=(1,0,0,0), h=-1 and C_3=1. Its norm certificate is therefore ||s(tau)||^2<=3. Both controls below start at this same state. No other trajectory is evaluated.

For b=0, the solution of that registered initial-value problem is

    s_0(tau)=(cosh(tau),0,sinh(tau),0),
    s_0(1)=(cosh(1),0,sinh(1),0).

It satisfies the generator and initial conditions by differentiation. Its physical-energy and state-norm readings are

    h(s_0(tau))=sinh^2(tau)-cosh^2(tau)=-1,
    ||s_0(tau)||^2=cosh(2*tau),
    H_0(0)=H_0(T)=-E0,    ||s_0(1)||^2=cosh(2).

For b=3 use the complex planar coordinate Z=X+iY, only as a notation for this same real initial-value problem. The equations give

    Z''+3*i*Z'-Z=0,  Z(0)=1,  Z'(0)=0.

Set beta=3/2 and k=sqrt(5)/2. Substitution Z=exp(-i*beta*tau)*W gives W''+k^2*W=0, with W(0)=1 and W'(0)=i*beta. Thus

    Z(tau)=exp(-i*beta*tau)*[cos(k*tau)+i*(3/sqrt(5))*sin(k*tau)],
    Z'(tau)=exp(-i*beta*tau)*(2/sqrt(5))*sin(k*tau).

The second line follows by direct differentiation, using beta^2-k^2=1; it checks the initial velocity and magnetic sign. At tau=1 the exact terminal real state is

    X_3 = cos(beta)*cos(k)+(3/sqrt(5))*sin(beta)*sin(k),
    Y_3 = (3/sqrt(5))*cos(beta)*sin(k)-sin(beta)*cos(k),
    U_3 = (2/sqrt(5))*cos(beta)*sin(k),
    V_3 = -(2/sqrt(5))*sin(beta)*sin(k).

No decimal approximations are needed. The same solution gives on the prescribed window

    ||r_3||^2=1+(4/5)*sin^2(k*tau),
    ||v_3||^2=(4/5)*sin^2(k*tau),
    ell_3=-(6/5)*sin^2(k*tau).

Therefore h=-1 and C_3=1 exactly, in agreement with both conservation checks, and

    H_3(0)=H_3(T)=-E0,
    ||s_3(1)||^2=1+(8/5)*sin^2(sqrt(5)/2) <= 13/5 < 3.

The terminal comparison is strictly different in norm: cosh(2)=1+2*sinh^2(1)>3, because sinh(1)=integral_0^1 cosh(u)du>1. Consequently

    ||s_3(1)||^2 < 3 < ||s_0(1)||^2,
    H_3(T)=H_0(T)=-E0.

This is a comparison of the one registered trajectory under two declared controls, not a claim of optimized confinement, a parameter boundary or an unbounded finite-time divergence. The b=0 reading is finite. The certificate for arbitrary initial states and the explicit registered terminal readings are distinct claims. Both use the original initial-unit-ball preparation domain and fixed physical window; the later states are not required to remain inside that initial unit ball.

## Check 6 — scientific interpretation, limits and handoff

The full state used in the certificate and observation is (position,velocity) in the invariant plane. H alone is a scalar, indefinite, conserved observable; it is not being asserted to be a sufficient state or a positive norm. C_3 is another scalar observable computed from the same full state and known control. No closure of an H-only reduced dynamics is inferred. In particular, matching H at the two terminal cuts does not identify their full states.

The physical potential/kinetic decomposition and the auxiliary quadratic have different meanings. C_3 contains the cross term XV-YU with a coefficient fixed for b=3 and the chosen normalization. It measures a dimensionless quadratic combination. Multiplication by E0 would assign energy dimensions to a number without proving that it is physical work, heat, an apparatus energy store or rest mass. Both controls preserve H because the magnetic force does no work. Their different comparator decisions and terminal states occur under the same supplied force law with a changed declared control.

The conditional model supplies all dynamics, units, clock, ideal observations and m/q-dependent fields. It does not derive them from DET records or native updates. It is a conventional finite classical comparator potentially useful to QR when distinguishing a physical energy observable from an auxiliary norm certificate under explicit state/update/readout assumptions. There is no adoption or assignment of QR work, no scalar-field stress claim and no PIM recovery claim.

The physical horizon is exactly 0<=tau<=1. The algebraic identities do not authorize an all-time, nonlinear, variable-field or general-b stability conclusion. No extra magnetic ratio, trajectory probe, noise/damping model, Floquet analysis or empirical apparatus run was used. Empirical application would require evidence that this nonrelativistic test-particle model and neglect of radiation/backreaction remain valid over that window. No such evidence is supplied or inferred. There is no native-unit, gravity, ontology, law-genesis or efficiency claim; retired kappa-gravity is not reopened.

The proof is analytic. The declared model, physical window, two controls and one trajectory per control are the complete scope. Independent proof review found no required repair. Exact private controls, source identities, author/reviewer manifests and recipient disposition are retained under the [metadata-obscured publication policy](../coordination/REDACTED_PUBLICATION.md). They are not represented as an executable public custody archive.
