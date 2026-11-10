# Inertia calibration from three marked-base angles

Two unballasted endpoints fix the ratios among the bare base moment, rotor moment and slider mass times the squared reference length. The positive parameters consistent with a feasible pair form one open ray. A repeat of the first loop with a known additional base moment selects exactly one point on that ray if and only if its signed endpoint lies strictly between zero and the first endpoint.

## Complete angular momentum and the observed angles

Each run begins at rest, separately prepared with its specified low radius and with both angles zero. In a run with extra base moment D_h, the cyclic momentum is

    p_θ = (I₀ + D_h) θ̇ + 2mr² θ̇ + J(θ̇ + φ̇).

The last term uses the rotor's absolute angular speed. The symmetric sliders contribute their common rotational motion, while their purely radial relative motion contributes zero moment about the shared axis. The supplied kinetic Lagrangian is independent of θ and its generalized external torque vanishes, so p_θ stays at its initial zero. Thus

    θ̇ = −k_h(r) φ̇,       k_h(r) = J/(I₀ + D_h + J + 2mr²).

For all admitted positive parameters k_h is strictly between zero and one and strictly decreasing at r>0. The given quintic has endpoint values 0,1 and derivative 30u²(1−u)². It is monotone with first and second derivatives zero at the joins. The finite four-leg protocol therefore returns to (r_low,0) with both shape rates zero at 4τ, and the momentum equation returns θ̇ to zero as well. The marked base may change orientation although all rates close. The ballasted run uses a fresh zero-momentum preparation after attachment. These arguments hold for every finite τ>0.

With α=π/2 and positive sense as specified, the successive base-angle increments are 0, −α k_h(r_high), 0 and +α k_h(r_low). During the angular legs the motion is monotone. From its start at zero the lifted orientation lies between −α k_h(r_high) and α[k_h(r_low)−k_h(r_high)], hence strictly inside (−π/2,π/2). Its positive endpoint already equals the recorded principal value in (−π,π]. No turn count or intermediate sample is needed.

Write T=2ma², x=(I₀+J)/T, y=J/T and d=D/T. Here T has units of moment of inertia, and x,y,d are dimensionless. Positivity gives x>y>0 and d>0. Conversely each T>0 and x>y>0 yields I₀=(x−y)T, J=yT and m=T/(2a²). At radius na the coefficient equals y/(x+D_h/T+n²). For normalized observations b_i=β_i/α, subtraction at the two radii gives

    b₁ = 3y / [(x+1)(x+4)],
    b₂ = 5y / [(x+4)(x+9)],
    b₃ = 3y / [(x+d+1)(x+d+4)].

Here the squared-radius pairs are (1,4), (4,9) and (1,4), respectively. Ballast modifies only the base contribution in run 3.

## Feasibility and the full inverse for the raw pair

Treat each raw β as a signed real principal angle. A value outside (−π,π] fails the record definition. Apply the following tests in order.

1. Require b₁>0 and b₂>0. Form R=3b₂/(5b₁) and require 1/9<R<1.
2. Put x=(9R−1)/(1−R). Require 0<b₁<3x/[(x+1)(x+4)]. Set y=b₁(x+1)(x+4)/3.

For necessity, cancellation of y and x+4 in the forward pair gives R=(x+1)/(x+9). This function increases strictly from 1/9 to 1 for x in (0,∞), with derivative 8/(x+9)². Solving for x gives the displayed expression. The remaining strict bound is exactly 0<y<x. Thus zero or negative endpoints fail, either equality for R fails, and equality at the positive upper bound for b₁ would require I₀=0. None of these boundary values is attained by the positive family.

For sufficiency the reconstructed x,y have x>y>0. For every T>0 the triple

    (I₀,J,m) = ((x−y)T, yT, T/(2a²))

reproduces b₁ by the definition of y. It reproduces b₂ because its ratio R and its b₁ agree with the record. The winding proof ensures that both calculated values equal the raw readings. Necessity recovers the same x,y from any solution, so this formula exhausts the inverse. The two independent dimensionless quantities can equivalently be taken as I₀/(ma²)=2(x−y) and J/(ma²)=2y. The unmeasured common scale T is arbitrary.

## The third raw reading and the inertia standard

First pass the pair tests. For the ballasted repeat require the raw principal angle to obey 0<β₃<β₁. An infeasible pair has empty triple inverse for every third reading. For a feasible pair, all readings outside the open interval, including β₃=0 and β₃=β₁, have empty inverse. Indeed b₃ is a strictly decreasing continuous function of d>0. Its limits at zero and at infinity are b₁ and zero. For each fixed known D>0 the positive common scales T sweep exactly all d=D/T>0.

For any reading inside that interval, solve for z=x+d. The equation (z+1)(z+4)=3y/b₃ has roots (−5±√(9+12y/b₃))/2. Since 3y/b₃>(x+1)(x+4), the square root exceeds 2x+5. Its positive-sign root is greater than x, while the other is negative. The full inverse is the singleton obtained from

    d = [√(9+12y/b₃)−5]/2 − x,
    T = D/d,      I₀=(x−y)T,      J=yT,      m=T/(2a²).

All quantities under the root are dimensionless, the computed d is strictly positive and T,I₀,J have mass·length² units. With calibrated length a, m has mass units and refers to each of the two sliders. Substitution in the three endpoint equations proves sufficiency. The pair fixes x,y and the third fixes the unique positive d, proving uniqueness for known D. At β₃=β₁ a finite scale would need d=0, incompatible with D>0. At β₃=0 no finite positive d can make the numerator vanish.

If only a positive unknown ballast moment is promised, the same feasibility test and inferred d apply. The full joint family then has arbitrary T>0 with D=dT and the same formulas for I₀,J,m. The new angle fixes a ratio to the ballast. A numerical moment D calibrated in stated units supplies the independent scale needed for the absolute inverse.

## Matched fixture and scope

Set I₀=J=D and m=D/a². Then T=2D, x=1, y=1/2 and d=1/2. The first run coefficients at a and 2a are 1/4 and 1/10. Their difference gives b₁=3/20 and β₁=3π/40, the fixed CL051 endpoint. The second run has coefficients 1/10 and 1/20, giving b₂=1/20 and β₂=π/40. The ballasted repeat has coefficients 1/5 and 1/11, giving b₃=6/55 and β₃=3π/55. Inverting those readings gives R=1/5, x=1, y=1/2 and 9+12y/b₃=64. Hence d=(8−5)/2−1=1/2, T=2D and the starting moments and each slider mass are recovered.

A native or empirical use would have to register the same bare base, centered rotor and two equal sliders across all three preparations, the calibrated radii and relative excursion in the specified order, each rest reset and the zero complete angular momentum in the absence of external torque. It would also need the common signed inertial angle reference for the marked base, a length reference for a, and the independently calibrated centered base moment D with all other moving components unchanged. The derivation conditions on the supplied mechanical model and ideal internal controls. It establishes the inverse for the three exact endpoints and makes no empirical or native calibration claim.

## QR use and scientific review

QR adopted the rotor as a way to transfer a separately calibrated moment of inertia to the measured apparatus. Two angles determine the proportions of the base moment, rotor moment and the two sliders’ combined moment at radius $a$. For a feasible unballasted pair, a calibrated added moment $D$ and a third endpoint satisfying $0<β_3<β_1$ determine the two moments. The length $a$ must also be calibrated to infer the inertial mass of each slider. Using it as a sector mass requires independently registering that slider to the sector carrier. Comparing it with gravitational mass requires a separate gravitational observation.

Classical supplied and independently reviewed CL077/v1. DET Quantum Relativity assessed the receiving assumptions. The coordinator adopted the transfer on 9 November 2026 HST.

- Classical result SHA-256: `8f0ac0e6703690ef283b9a2ab1fe38d5813a68afd1a74375373ec2c33274ecbb`.
- Classical scientific review SHA-256: `a5e8d298b933a8310ce7c322a9e3dfcef095bde332a6d45b8095e9865acd59b3`.
- Classical disposition SHA-256: `8a2c5716dd3b4f9edb4f7be0d0a2366f0836d0134ee1344885e668d3c841f497`.
- QR recipient assessment SHA-256: `736f43726a9f194fa9a34de054713167fecbc4c0c68982dec8ecb0d35b31cb78`.
