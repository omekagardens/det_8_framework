# Native birth kernels with a supplied canonical phase action

GDM063 supplies a conditional phase/action interface for the exact three-birth GDM047 common law. Its full positive-measure kernels preserve the native branch probabilities and consistency identities, and commute with a supplied simultaneous phase translation. A fixed complete readout has action contrast 1/4 and transport contrast 1/16, retaining detector failures.

The interpretation has an exact limitation: the transported and passive phase models are conjugate by one fixed, source-dependent change of angle coordinates. Transforming states and effects together preserves every probability. The nonzero transport contrast holds the detector's angle convention fixed. It does not establish a representation-independent new coupling, physical energy, mass, gravity or a derived unit.

## Exact native input and enlarged domain

Use the WITNESS, not the source-return cut, from the GDM047 section of [Finite source, order, return and visibility](finite_source_order_return_and_visibility.md). That source gives the complete first, second and third branch matrices, reference-memory coefficients and native-domain proof. Here B_alpha(x'|x) denotes precisely those unnormalized matrices for each actual ideal and newborn bit, with all marks, reference transitions and transported histories retained through three births. No coefficient or horizon changes.

The eight native labels are x=(i,m), i in {00,10,01,11}, m in {0,1}. Source and reservoir rows are r=(0,1,0,1), e=(0,0,1,1), Q=r+e=(0,1,1,2). Supported source transitions are self-transitions or 10↔01. Accepted native inputs include nonnegativity, strict branch eligibility, full effect normalization, uniform branch anchors, allowed record reads, marked covariance, every full unnormalized diamond and admissible suffix. These facts do not follow merely from conserving Q.

Supply T=R/(2pi Z) and two angles (theta_r,theta_e). A state nu is a vector of eight finite positive Borel measures on T², with mass sum_x nu_x(T²). Arbitrary correlated, atomic, singular and continuous measures are admitted. The probability cone is infinite-dimensional; the finite claims concern the native horizon and recorded outcomes.

Let S exchange the two angles, and let T_(i',i)=S for 10↔01, identity for source self-transitions. Define transported A and passive P branches by

    [A_alpha nu]_x' = sum_x B_alpha(x'|x) (T_(i',i))_* nu_x,
    [P_alpha nu]_x' = sum_x B_alpha(x'|x) nu_x.

Unsupported transitions have zero coefficients. Both instruments preserve old records and append the same native event over the same actual ideal. The extra angle rule reads only the supported source pair; it has no dependence on vertex names, forbidden old marks or external settings.

## Supplied generator and normalization

Supply the four-dimensional ambient cotangent space T*(T²), canonical pairs (theta_a,I_a), and bracket

    {f,g} = sum_(a=r,e) [(partial_theta_a f)(partial_I_a g)
                        -(partial_I_a f)(partial_theta_a g)].

With supplied J0>0, embed native labels at I_r=J0 r_i, I_e=J0 e_i. The individual occupation tori are not asserted to be intrinsically symplectic. The ambient action R_lambda adds the same lambda to both angles and fixes both actions. For G=I_r+I_e,

    {f,G}=partial_theta_r f+partial_theta_e f,
    d(f composed with R_lambda)/d lambda={f,G} composed with R_lambda.

This uses smooth periodic observables, so local angle notation does not require a global real-valued angle coordinate. On the occupation tori, G/J0=Q. Replacing G by G/J0 under the unchanged bracket divides the generator by J0; Q is not silently made a unit-speed generator. A function constant on each torus can still have nonzero ambient action derivatives.

If I has action units, the bracket has the corresponding inverse-action convention and lambda is dimensionless. Supplying physical time t and Omega would give lambda=Omega t and H=Omega G. This optional interpretation derives neither J0, Omega nor time per birth. The declared angular speed is identical at every native label, not proportional to Q.

Exchanging both complete canonical pairs preserves the bracket and canonical two-form, maps the 10 torus to 01 and restricts to S. Identity represents a source self-transition. These deterministic representatives preserve G; their stochastic mixture is not a deterministic symplectomorphism.

## Full measure-kernel consistency

For every Borel set E, the branch kernel is

    K_alpha^A((x,theta),{x'} times E)
      =B_alpha(x'|x) 1_E(T_(i',i)theta).

The maps are continuous Borel bijections, so these are measurable, countably additive positive kernels on the entire declared domain. Finite sums preserve finiteness. For the marginal pi(nu)_x=nu_x(T²),

    pi(A_alpha nu)=B_alpha pi(nu)=pi(P_alpha nu).

Thus all native history probabilities are retained even with native/angle correlations. Writing c_alpha(x)=sum_x' B_alpha(x'|x), strict native eligibility gives positive branch mass for every nonzero input. Since sum_alpha c_alpha(x)=1, summing every branch conserves total probability mass. Division by a positive branch probability gives an admitted posterior. Unsupported native transitions remain zero.

Normalized product Haar measure h is invariant under S. For the native uniform anchor w8, if B_alpha w8=a_alpha w8, then A_alpha(w8 tensor h)=P_alpha(w8 tensor h)=a_alpha(w8 tensor h), with the original weights 1/2, q_s/2 or p_C(S)/2. This anchor does not replace the all-input kernel proof.

Set eta_01=1 and eta_00=eta_10=eta_11=0. Every supported pair obeys T_(i',i)=S^(eta_i'+eta_i), with exponents modulo two. Define the fixed involution

    [D nu]_x=(S^eta_i)_* nu_x,   D²=I.

For the passive lift P(B) of a native matrix,

    A_alpha=D P(B_alpha) D,
    A_gamma=D P(B_gamma) D

for every chronological native history gamma. The interior D² factors cancel. Explicitly,

    [A_gamma nu]_x'(E)
      =sum_x B_gamma(x'|x) nu_x((S^(eta_i'+eta_i))^-1 E).

This is equality of finite measures for every E, including repeated exchanges and arbitrary reference updates. Every accepted native matrix diamond therefore lifts to a full unnormalized kernel diamond. D is independent of the parent and branch and commutes with native relabeling, so identified endpoints use the same D. Every allowed common suffix preserves equality. The original native theorem covers every empty or singleton base, all marked equal/unequal ideal cases and full-to-proper transport within the three-birth horizon. No scalar-only, product-state or Haar-average replacement is used.

Since S commutes with R_lambda for all real lambda, each A and P branch commutes with R_lambda pushforward on every finite measure. On smooth observable vectors, L=partial_theta_r+partial_theta_e also commutes with the adjoint branches. Bounded smooth derivatives on the compact torus justify differentiating their integrals against finite measures. No differentiable density or total-variation derivative is assumed for an arbitrary input measure.

## Complete fixed one-birth observation

Prepare x0=(10,0), angles (0,pi/2). For either retained bit b the first native branch (K tensor I2)/2 gives x1=(10,0) with weight k1/2=3/8 and x2=(01,0) with weight k2/2=1/8. All six other native endpoints, including all reference-one labels, have zero weight.

Independently randomize lambda in {0,pi/2} and j in {X,Y}, each uniformly. X and Y mean cosine and sine of the source angle, not quantum operators. For z=f_j(theta), the supplied complete detector is

    K_z(+1)=(1+z)/4, K_z(-1)=(1-z)/4, K_z(failure)=1/2.

The following table supplies every response parameter; each entry is (z_X,z_Y).

| Family | lambda | x1 | x2 |
| --- | --- | --- | --- |
| A | 0 | (1,0) | (0,1) |
| A | pi/2 | (0,1) | (-1,0) |
| P | 0 | (1,0) | (1,0) |
| P | pi/2 | (0,1) | (0,1) |

For each family F=A or P, each placement of the translation before or after the birth, both b and every setting pair, the complete joint law is

    P_F(lambda,j,b,x_i,o)=(k_i/8)K_z(o), i=1,2,
    P_F(lambda,j,b,x',o)=0 for the six other endpoints.

At x1 the + and - cells are 3(1±z)/128 and the failure cell is 3/64. At x2 they are (1±z)/128 and 1/64. The table and formula specify all 2*2*2*8*3=192 cells per family and placement, including zero detector cells. Their sum is one; the total failure mass is 1/2. Before/after laws agree cell by cell, and full-kernel intertwining proves that equality for arbitrary inputs as well.

Conditioning only on the prospectively randomized lambda gives p_(F,lambda)=2P_F, with weights k_i/4 for each endpoint, quadrature and bit. With total variation defined as one half the full sum of absolute cell differences,

    TV(K_z,K_z')=|z-z'|/4.

The A responses differ by one between lambda settings at both endpoints and quadratures, so

    D_action=TV(p_(A,0),p_(A,pi/2))=1/4.

At lambda=0 the A and P responses differ only at x2, by one at each quadrature. Hence

    D_transport=TV(p_(A,0),p_(P,0))=k2/4=1/16.

All bits, endpoints, settings, zero cells and failures remain in these laws. Failure differences vanish; failure trials are not discarded or renormalized. These are population contrasts under supplied preparation, phase reference, basis access and detector rules, not calibrated observations or sampling guarantees.

## Exact interpretation boundary

The same D conjugates every A branch into P. Transforming initial measures and terminal effects consistently preserves every probability. At the selected initial 10 label D is identity; at a possible 01 endpoint it changes which angle a source-angle effect reads. The fixed detector is deliberately unchanged between the two families. Thus the positive fixed-interface contrast does not demonstrate an invariant new coupling or select these phase conventions from DET.

The trial stays in Q=1. It measures neither a charge-dependent phase frequency nor J0. The canonical geometry, off-torus extension, action scale, preparation and readout are supplied. Physical clocks, work stores, momentum, inertial response, gravitational fields, calibration, reset costs and empirical evidence remain unprovided. The result is not an all-horizon law or closed autonomous Hamiltonian dynamics. It establishes an exact conditional interface and its limitation, without retuning a failed candidate or changing the accepted native law.

The earlier GDM062 question review missed its full-read confirmation cutoff by 16 seconds and remains procedurally incomplete. A separate prospective fresh review admitted the unchanged question with explicit conventions; it does not retroactively certify the earlier process. All other recorded qualifications remain intact.

## Reviewed source identity

GDM063 report SHA256 a453e873010f33d3ee29d9d54ca47023a3a49f671e7d71a6b7d78261aa6eb41c; independent result review c72af4dc68cc986fdd8c9f43dcca75c2c0b6ac3e996498bc1eb4f007d0f50be1; coordinator disposition a2960a9b795735e26856f4a72893138bd3f46c059116dd7ac6d04d8b6de06aff. These identify exact reviewed sources, not physical evidence. Author and result reviewer met their own declared saved-read and completion deadlines. The separate publication assessment applies only to this assembly.
