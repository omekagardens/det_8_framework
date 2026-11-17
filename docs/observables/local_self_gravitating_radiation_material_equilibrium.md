# Local self-gravitating radiation/material equilibrium

**A smooth, locally unique regular static branch exists near the flat reference.**
The fixed material law, material amount and radiation content admit the supplied
self-gravitating radiation/membrane equilibrium for $0\leq\epsilon<\epsilon_*$
for some $\epsilon_*>0$. No numerical interval or arbitrary physical compactness
is certified. The regular-center integral construction, both shell junction
equations and the constrained Jacobian establish equilibrium preparation, not
dynamical formation or stability.

This is a conditional conventional source and static readout model. Its Einstein
gravity, material and radiation laws, conserved current, matching conventions and
infinity-normalized clock are supplied. It is not a quantum-coherent preparation,
a native gravitational source or a calibrated physical apparatus.

## 1. Inputs and supplied structure

The [surface material assignment](surface_material_for_static_radiation_shell.md)
provides the exact constitutive law and strict material inequalities. Its unloaded
planar modes are not transferred to a curved shell. The
[radial radiation/material energy result](radial_energy_of_a_radiation_loaded_membrane.md)
provides the flat reference and content normalization only; its flat energy bound
is not a gravitational stability theorem. The
[static mass/proper-energy comparison](static_radial_length_and_proper_matter_energy.md)
distinguishes exterior mass from local matter energy; neither of its imposed
source profiles is transplanted here.

The primary context is Katz and Okuta, *What Cavities?*,
[gr-qc/9409021v1](https://arxiv.org/html/gr-qc/9409021v1), 12 September 1994.
The accepted author and scientific reviewer read sections 2–3 through equations
(2)–(22), concerning static radiation and massive-shell matching. The selected
constitutive and fixed-content branch is not imported from that paper. Its
signature, units and parameters differ, so the equations below use the explicitly
stated conventions. No later stability, maximum-mass or percentage threshold
is used. The exact frozen context snapshot is 226,314 bytes, SHA-256
`e9805ab459c9824ac0a97cb6522c91c6af819c1521f50556fd051c5ad63acc16`.

Supply Einstein gravity with zero cosmological constant, signature (−+++), positive reference scales R₀,u₀,n₀,c, and the ordinary interior/exterior orientation. The interior contains an isotropic hydrodynamic radiation fluid with energy density u>0 and p=u/3. Its static metric is

    ds²=−e^(2ν(r))c²dt²+f(r)^(-1)dr²+r²dΩ²,
    f(r)=1−2Gm(r)/(c²r).

m(r) is a mass, not an energy. The exterior is Schwarzschild with mass M and unit lapse at infinity. There is no central point mass, external support, throat, heat bath or additional reservoir. The membrane is an ideal surface fluid with fixed law

    e(n)=a_m n+K n²+b_m,       p_s=K n²−b_m,
    a_m n₀=τ₀, K n₀²=τ₀/2, b_m=3τ₀/2, τ₀=u₀R₀/6.

The symbol b_m is the constitutive constant called b in the material law; it is kept distinct from the dimensionless radius b below. Fixed N=4πR²n=N₀=4πR₀²n₀ fixes n=n₀(R₀/R)². The radiation content is exactly the supplied static charge

    C=4π∫₀ᴿ (u/u₀)^(3/4) r² f^(-1/2)dr=C₀=4πR₀³/3.       (1)

For the supplied adiabatic radiation model, the energy equation along U is U·∇u+(u+p)∇·U=0, so ∇·[(u/u₀)^(3/4)U]=0. On a static slice U is its unit future normal; contracting this current with that normal leaves the proper-volume density in (1). Thus no extra lapse factor occurs. C is a mathematical volume-dimensioned charge, not a measured entropy, photon count or native count.

The registered coupling is ε=Gu₀R₀²/c⁴. The local family varies this mathematical parameter with all reference material scales fixed. Each positive member is a solution of the supplied Einstein system at that member's coupling. It is not a proposal to change a measured constant, nor a guarantee that a given observed coupling belongs to the proved neighborhood. The ε=0 point is a desingularized flat reference.

## 2. Interior Einstein equations and regular center

For the displayed metric, the two independent mixed Einstein components are

    G^t_t=(f−1)/r²+f′/r=−2Gm′/(c²r²),
    G^r_r=(f−1)/r²+2fν′/r.

Equating these to −8πGu/c⁴ and 8πGp/c⁴, respectively, and using radial stress conservation gives

    m′=4πr²u/c²,
    ν′=G[m+4πr³p/c²]/(c²r²f),
    p′=−(u+p)ν′,       u′=−4uν′.                    (2)

The remaining angular Einstein equation follows from the contracted Bianchi identity and conservation away from the center; the regular construction below extends it there. In particular (2) is the radiation TOV equation with correct mass/energy factors. A homogeneous u at positive G has not been assumed.

Put

    b=R/R₀,   q=u_c/u₀,   s=r/R∈[0,1],
    w(s)=u(Rs)/u₀,   j(s)=m(Rs)c²/(4πu₀R³),
    κ=4πεb²,   f(s)=1−2κj(s)/s.

The common radial interval is fixed even while R varies. Equations (2) become

    j′=s²w,   j(0)=0,   w(0)=q,
    ν_s=κ[j+s³w/3]/(s²f),
    w_s=−4κw[j+s³w/3]/(s²f).                        (3)

The apparently singular coefficients at s=0 cannot be dismissed. To construct the regular solution, set z=s² and w(s)=W(z). Define the bounded linear operator

    (LW)(z)=∫₀¹ t²W(zt²)dt.

Then j(s)=s³(LW)(s²), and the complete regular-center problem is the single integral equation on X=C([0,1]):

    W(z)=q−2κ∫₀ᶻ W(v)[(LW)(v)+W(v)/3]
                         /[1−2κv(LW)(v)] dv.         (4)

Here ||L||≤1/3 in the uniform norm. For q in a sufficiently small open neighborhood of 1, take a fixed positive uniform-norm ball for W around 1, for example with all its values between 1/2 and 3/2. On a slightly smaller closed ball around the constant q, and for |κ| sufficiently small, the denominator is uniformly bounded away from zero. The rational integrand and its W derivative have uniform finite bounds there, because L is bounded and W remains in a fixed compact positive range. Thus the right-hand map Φ(q,κ,W) has

    ||Φ(q,κ,W)−q||≤C₁|κ|,
    ||D_WΦ(q,κ,W)||≤C₂|κ|,

with finite constants independent of q,κ,W in those neighborhoods. Shrinking |κ| makes the first bound smaller than the chosen ball radius and the second strictly less than one. The contraction theorem therefore supplies one W, unique in that ball, for each nearby (q,κ). This is a finite-interval existence construction, not a formal center series.

The map Φ is continuously differentiable (indeed smooth) as a map of (q,κ,W) into X on the open set with the denominator separated from zero. The inverse of I−D_WΦ exists by its convergent Neumann series. The Banach-space implicit-function theorem consequently gives smooth dependence W(q,κ) in X; these are its explicit domain, differentiability and invertibility hypotheses. This suffices for all terminal evaluations and integrals used in the finite-dimensional equations below.

There is also spatial regularity, not merely continuity. Equation (4) first gives W∈C¹. The operator L maps C^k to C^k, with derivatives obtained by inserting t^(2k) in its integral. Differentiating the smooth right-hand differential equation from (4) bootstraps W to C^∞ in z. Therefore w(s)=W(s²) is smooth and even at the center, w_s(0)=0, and j=s³LW has the required regular mass behavior. The identity 3LW+2z(LW)_z=W verifies j′=s²w directly. f and ν are regular even functions of s, with f(0)=1 and ν_s(0)=0. Conversely, every regular solution close to the reference, with m(0)=0, satisfies (4); no central point-mass integration constant is lost.

For κ=0, the exact solution is W=q, w=q, j=qs³/3. The formal use of negative κ to obtain an open parameter neighborhood for the theorem is mathematical only. Physical conclusions below are restricted to ε≥0.

## 3. Both Israel equations with fixed signs

At the shell let

    μ_−=Gm(R)/(c²R),   μ_+=GM/(c²R),
    S_−=sqrt(1−2μ_−),   S_+=sqrt(1−2μ_+).

Both square roots are positive in the ordinary-side neighborhood. The common normal points from interior to exterior on each side. Brackets denote exterior-minus-interior jumps, and K is the trace K^a_a. The supplied Israel convention is

    [K^a_b]−δ^a_b[K]=−8πG S^a_b/c⁴.

With K_ab=e_a^μe_b^ν∇_μn_ν, the nonzero mixed extrinsic curvatures of a static shell are

    K^τ_τ=sqrt(f)ν′,     K^θ_θ=K^φ_φ=sqrt(f)/R.

For example K_tt=−sqrt(f)e^(2ν)c²ν′; raising its timelike index supplies the positive mixed K^τ_τ. With S^a_b=diag(−e,p_s,p_s), the τ component of the specified Israel equation gives [K^θ_θ]=−4πGe/c⁴. Its angular component gives [K^τ_τ]+[K^θ_θ]=8πGp_s/c⁴. Consequently

    S_−−S_+=4πGRe/c⁴,                               (5)

    8πGRp_s/c⁴=(1−μ_+)/S_+
                  −[1−μ_−+4πGR²p(R)/c⁴]/S_−.        (6)

These are separate surface-energy and tangential-pressure conditions. The exterior ν′ in this derivation is GM/(c²R²f_+); the interior one is (2). The induced metric is continuous when e^ν(R)=S_+, with the same infinity-normalized t. A jump in radial metric coefficient is allowed at the shell. The static tangential surface balance has no tangential load or flux and is consistent with fixed N; no external support supplies an omitted force.

Equation (5) can also be solved in dimensional mass form. With the proper material shell mass M_s=4πR²e/c²,

    M=m(R)+M_s S_−−G M_s²/(2Rc²),                    (7)

provided S_+=S_−−GM_s/(Rc²)>0. Thus the total exterior mass includes the shell and its gravitational relation; it is not an unweighted fluid integral, nor generally the sum of local proper matter energies.

## 4. Nonsingular residuals at zero coupling

Let the dimensionless material functions be

    E(b)=e/(u₀R₀)=b^(−2)/6+b^(−4)/12+1/4,
    P(b)=p_s/(u₀R₀)=b^(−4)/12−1/4.                   (8)

They follow exactly from n/n₀=b^(−2); no material parameter is adjusted as gravity is turned on. Define

    j₁=j(1),  w₁=w(1),  S=sqrt(1−2κj₁),
    d=4πεbE(b),  S_+=S−d,
    M₀=4πu₀R₀³/c²,  Z=M/M₀.

The shell energy equation is equivalently

    Z=b³j₁+b²E(b)S−2πεb³E(b)².                      (9)

This is smooth at ε=0 and is (7) in fixed units. Substitution shows 1−8πεZ/b=(S−d)²; requiring S−d>0 retains exactly the ordinary branch and avoids a spurious solution introduced by squaring.

The remaining two finite-dimensional equations for (q,b) are

    F_C(q,b,ε)=3b³∫₀¹ w(s)^(3/4)s²/sqrt(f(s)) ds−1=0,

    F_P(q,b,ε)=2P(b)+b w₁/(3S)
                 −E(b)/2 [1/(S(S−d))−1]=0.          (10)

The first is precisely fixed C, not a fixed coordinate-volume approximation. To verify the second without dividing by an unexamined zero, use

    (1−μ)/sqrt(1−2μ)=(S+S^(-1))/2.

The difference of those terms in (6) is d[1/(S(S−d))−1]/2. The interior radiation term is κw₁/(3S). For ε≠0, division of (6) by 4πεb gives exactly F_P=0. Formula (10) itself is smooth at zero and defines its removable limit there. Thus every positive-coupling solution of (9)–(10) with positive square roots satisfies both original junction equations. We have not treated the equation at G=0 as Einstein matching divided by zero.

At ε=0, w=q, S=1, d=0. The residuals reduce to

    F_C=b³q^(3/4)−1,
    F_P=2P(b)+bq/3.                                 (11)

The flat pressure equation is p(R)=−2p_s/R, the correct Laplace balance with tensile p_s<0. Both equations vanish at (q,b)=(1,1); E(1)=1/2 and P(1)=−1/6. Equation (9) gives the flat reference Z=1/3+1/2=5/6, including its material shell. This reference value is needed to specify the branch, not a first-order gravitational coefficient.

## 5. Checked local branch theorem

The regular-center construction makes w,j smooth functions of (q,κ) as continuous functions on the fixed interval. Since κ=4πεb² is smooth, and f,S,S−d remain positive near (q,b,ε)=(1,1,0), both residuals in (10) are C¹ there. Fractional powers and square roots cause no singularity in this positive neighborhood; their Fréchet derivatives and integration/evaluation are continuous.

Using (11), the constrained Jacobian with rows (F_C,F_P) and columns (q,b) at the reference is

    D_(q,b)F |_(1,1,0) = [ 3/4     3   ]
                          [ 1/3   −1/3 ],
    det = −5/4 ≠ 0.                                  (12)

In particular P′(1)=−1/3, so ∂_bF_P=2P′(1)+1/3=−1/3; fixed material amount is essential to this derivative. The content derivative includes the changing volume, ∂_bF_C=3. None of the O(ε) metric terms contributes to these q,b derivatives at ε=0. If M is retained as a third unknown, the residual Z minus the right side of (9) has unit derivative in Z. The corresponding three-equation Jacobian is block triangular with the same nonzero determinant. Eliminating M therefore conceals no extra constraint or rank defect.

The finite-dimensional implicit-function theorem applies: there are an open interval about ε=0 and an open neighborhood of (q,b)=(1,1) in which (10) has unique smooth functions q(ε),b(ε). Equation (9) gives a unique smooth Z(ε), and (4) and the lapse match give the unique nearby regular interior and static matching. This is local uniqueness among regular solutions whose central density, radius and field lie in the constructed neighborhood, not uniqueness of all equilibria for that material.

Choose the neighborhood small enough that q,b∈(9/10,11/10), then shrink the ε interval further if necessary. Uniform continuity of w and f on the compact fixed radial interval ensures w>0 and f>0 throughout the interior; S>0 and S−d>0 also persist. Z(0)=5/6>0 and E(1)=1/2>0 give positive exterior mass and shell energy nearby. With R positive and less than 2R₀, the stated exterior annulus exists. For ε>0 and M>0, its Schwarzschild f increases with r, so positivity at the shell implies no exterior horizon anywhere in that annulus (or in its ordinary outward extension).

Since n/n₀=b^(−2) stays inside (1/2,3/2), the supplied material law’s accepted strict inequalities e>0, e+p_s>0, e>|p_s| hold. They can also be seen directly from (8) near the strict reference values. The radiation fluid has u>0 and p=u/3, hence strict dominant-energy inequality as well. Positivity of the matched lapse and interior lapse is proved explicitly below. The regular center has no point mass, throat or trapped sphere. All these inequalities can be enforced together by shrinking one neighborhood and choosing some ε_* >0. The admitted physical branch is 0≤ε<ε_*.

No numerical value of ε_* is asserted. The enclosing q,b box is not a claim of a solution for every point of that box. No first derivative of q,b,Z with respect to ε, mass correction, mode frequency or stability coefficient is needed for or appended to this existence decision.

## 6. Registered static readouts

The following implicit maps completely specify the registered record for each admitted ε:

    R/R₀=b(ε),       u_c/u₀=q(ε),
    M=M₀[b³j₁+b²E(b)S−2πεb³E(b)²],
    e=u₀R₀E(b),     p_s=u₀R₀P(b),
    e^ν(R)=S−d,
    e^ν(0)=(S−d)[w₁/q]^(1/4).                       (13)

They are determined by (4), (9) and (10), whose local solution has been proved. In the interior, integration of u′=−4uν′ gives

    e^ν(r)=(S−d)[w₁/w(r/R)]^(1/4).                  (14)

Thus all lapses are positive; their time coordinate is the fixed exterior one. At the reference both lapses equal one. For positive coupling, (2) also gives decreasing u away from the center, consistent with the central lapse lying below the shell lapse; no new quantitative redshift bound is claimed. The finite exterior annulus has lapse sqrt(1−2GM/(c²r)) and its supplied Schwarzschild normalization. The extension to infinity fixes the clock convention; it is not an extra measured observable or evolution interval.

Dimensions are explicit: u,p are energy/volume; e,p_s energy/area; m,M,M_s,M₀ masses; R,R₀ lengths; C has volume units; N is a count when n has number/area units. ε,κ,b,q,w,j,E,P,Z,S,d and the lapse are dimensionless. All physical units, G,c and reference scales are supplied. In particular no geometric mass is converted into a native count or calibrated rest-mass standard by this theorem.

## 7. What the branch establishes

The prescribed Einstein/radiation/material system has no local equilibrium
obstruction at the flat reference: the regular interior is well defined, both
shell equations are compatible after desingularization, and the constrained
Jacobian is invertible. This gives one smooth, locally unique static branch at
fixed $N,C$, with the implicit readout maps above. Failure of a different method
or Jacobian would not itself prove nonexistence; here the required hypotheses
are checked.

The charge $C$, proper matter energy, exterior mass and lapse are distinct objects.
The exterior mass is not just the fluid contribution, and the clock convention
is not a native clock construction. A physical member has not been certified to
lie below the unspecified $\epsilon_*$. A native or QR application still needs
its own source-state, stress/geometry, scalar, transition and observation
correspondence with a stated domain and controlled errors. The
[native mapping inventory](../coordination/NATIVE_MASS_MAPPING.md) keeps those
obligations distinct from conditional conventional comparisons.

No flat perturbation-energy theorem is transferred to curved spacetime. The
result supplies no radial, nonspherical, nonlinear, dynamical or global stability,
spectrum, gravitational correction coefficient, global equilibrium classification,
microscopic photon reflection/material realization, empirical execution, physical
calibration, native units, heat/efficiency or ontology validation. The fluid and
ideal shell remain stipulated continuum descriptions. Retired kappa-gravity
remains retired.

## Scientific and recipient provenance

A separate Classical author constructed CL112/v1. Classical root completed the
distinct nonblind scientific proof review, and the lane admitted the local static
branch on 17 November 2026 (UTC). The reviewer had prospectively proposed the
weak-gravity implicit-function strategy and examined flat feasibility; that
exposure was disclosed. The reviewer did not author or edit the completed result.
The independent recipient transfer review then admitted only the conventional
conditional source preparation and static readout scope, with no donor repair
or repeat proof review required. The present assembler performed that recipient
review; it is distinct from the donor scientific author and reviewer.

The scientific review checked regular-center contraction and smooth parameter
dependence, spatial regularity, both Israel signs, the fixed-$N,C$ derivatives,
removal of the zero-coupling factors, local uniqueness and the simultaneous
positivity neighborhood. The recipient review kept the native bridge and
physical qualification separate. This article reuses those completed reviews;
publication assembly adds no new proof or calculation.

| Accepted source | Bytes | SHA-256 |
| --- | ---: | --- |
| CL112/v1 author result | 19,164 | `f62be1eca48f3de45e4fc968646e7dfd841dddb61032db0f7814ee46b7e8763e` |
| Distinct Classical scientific review | 12,198 | `4417d24585e15bb20ebff97e1fe37bc70fdb1a290caef2e1eb8159fd49ab515c` |
| Recipient transfer review | 12,569 | `ba4bea16e9d1e0158c4645aa1fd4f50c7d98e95db0ff17433945e4870d8cae51` |

These identities identify the accepted evidence without presenting private archive
paths as public reproduction links. The work is manual analytic mathematics;
there was no scientific executable, numerical ODE solution, simulation, parameter
scan, empirical dataset or holdout. Accepted conventional inputs were reused,
and the branch theorem is derived conditionally under them. No derivation of the
supplied gravity, material, clock or scales from DET is claimed. Agreement with
observations is **NOT TESTED**. This publication adds no executable.
