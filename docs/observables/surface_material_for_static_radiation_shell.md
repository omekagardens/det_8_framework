# A surface material assignment for the static radiation shell

The fixed positive law passes the registered equilibrium, energy and local characteristic tests. It supplies one material specialization of the accepted [complete radiation-shell source](closed_radiation_shell_mass.md), with surface energy e_s(n0)=3τ0 and mass per area σ_GDM=3τ0/c². Throughout z=n/n0∈[1/2,3/2], the three physical polarization classes have squared speeds

$$
 c_L^2=c^2\frac{z}{1+z},\qquad c_V^2=0,\qquad
 c_N^2=c^2\frac{3-z^2}{z^2+2z+3}.
$$

The longitudinal and normal sectors have strictly positive kinetic and restoring quadratic coefficients. The transverse in-plane sector is a neutral vortical flow with positive kinetic coefficient and no shear restoring term. These are properties of the stipulated homogeneous planar material principal equations. They do not establish stability or dynamics of a radiation-filled sphere.

## 1. Fixed question, premises and scientific domain

The constants and density interval below are fixed. The background is supplied 3+1 Minkowski spacetime with signature (−+++), coordinates x⁰=ct, and c,R0,u0,n0>0. The radiation energy density u0 has energy/volume units and τ0=u0R0/6 is the accepted reference tension. Material amount N is conserved; n=N/A is its proper surface density. Neither n nor its unit is derived from DET.

The energy law and its constants are exactly

$$
 e(n)=a n+K n^2+b,\qquad
 a n_0=\tau_0,\quad K n_0^2=\frac{\tau_0}{2},\quad
 b=\frac{3\tau_0}{2}.
$$

Here e abbreviates e_s, an ENERGY per area. It is not the source's σ, which is MASS per area. Isentropic perfect-fluid surface matter is assumed: there is no shear or bending rigidity, viscosity, dissipation or independent thermal variable. With induced worldvolume metric h_ab and h_ab U^a U^b=−1, the supplied material model assumes

$$
 S^{ab}=(e+p)U^aU^b+p h^{ab},\qquad
 D_a(nU^a)=0,\qquad D_a S^{ab}=0
$$

in the absence of tangential load. It also supplies the unloaded normal equation S^{ab}K_ab=0. These are conventional additional update laws, not consequences of record ontology. No general action derivation is claimed or needed for this conditional calculation.

The reference sphere is checked only at (R0,n0), where stationary interior radiation supplies the equilibrium normal pressure u0/3. The perturbation test instead concerns homogeneous unloaded planar rest states at every fixed z in the specified compact interval. It is an instantaneous linear principal-symbol calculation; there is no finite evolution horizon, wavelength error estimate, apparatus observation or radiation perturbation model. Values away from n0 are material test states, not a family of asserted radiation-shell equilibria.

## 2. Area work, dimensions and the reference shell

At fixed material amount N, E_s(A,N)=A e(N/A) and dn/dA=−n/A. Therefore

$$
 \left.\frac{\partial E_s}{\partial A}\right|_N=e-ne',
 \qquad p=-\left.\frac{\partial E_s}{\partial A}\right|_N=ne'-e
 =K n^2-b.
$$

Negative p is tension. Define w=e+p. The useful identities are

$$
 e'=a+2Kn>0,\quad e''=2K>0,\quad
 p'=2Kn=n e'',\quad w=ne'=a n+2K n^2.
$$

Writing the dimensionless density explicitly gives

$$
 \frac e{\tau_0}=z+\frac{z^2}{2}+\frac32,
 \qquad \frac p{\tau_0}=\frac{z^2}{2}-\frac32,
 \qquad \frac w{\tau_0}=z+z^2.
$$

At n0 this is e0=3τ0, p0=−τ0, w0=2τ0. Thus

$$
 \sigma_{\rm GDM}=\frac{e_0}{c^2}
 =\frac{3\tau_0}{c^2}=\frac{u_0R_0}{2c^2}>0.
$$

For the outward unit normal ν on r=R0 and spatial tangent projector P_ij=δ_ij−ν_iν_j, the static wall specialization is exactly

$$
 T^{\rm wall}_{00}=3\tau_0\delta(r-R_0)
 =\sigma_{\rm GDM}c^2\delta(r-R_0),\quad
 T^{\rm wall}_{0i}=0,\quad
 T^{\rm wall}_{ij}=-\tau_0 P_{ij}\delta(r-R_0).
$$

Together with the unchanged interior entries T00=u0 and Tij=(u0/3)δij, these are the complete accepted GDM032 source entries for this σ choice. Its accepted traction identity 2τ0/R0=u0/3 is satisfied. The surface material amount is N=4πR0²n0. No new active-mass, field or boost calculation is made.

For sign consistency in the normal equation, use K_ab=e_a·∂_bν=−ν·∂_a e_b in flat space. It is positive 1/R0 in each orthonormal spatial tangent direction on the outward-oriented static sphere. An outward normal force density f has the convention S^{ab}K_ab=−f, since the normal projection of the stress divergence is −S^{ab}K_ab. Hence the sphere gives 2p0/R0=−u0/3 as required. The planar unloaded calculation below uses f=0. Reversing the orientation flips both K and the signed force and changes no result.

If material amount has its own bookkeeping unit Q, then [n]=Q/area, [a]=energy/Q, [K]=energy·area/Q², and [b]=[p]=[e]=energy/area. Taking Q dimensionless yields the inverse-area convention used here. The radial delta has inverse-length units, so every embedded T entry has energy/volume units. No physical scale or conversion c is inferred by choosing these normalizations.

GDM032 deliberately allowed σ and τ to be independent; this result selects one admissible constitutive specialization and does not restrict every accepted σ. The [same-source boost result](closed_radiation_shell_inertia.md) remains a separate reference, not an acceleration or material theorem. The [two Newtonian volume-fluid crossing comparison](matched_self_gravitating_fluid_crossing.md) is a separate result.

## 3. Energy conditions on the complete registered patch

Every inequality below holds for the fixed constants and every z∈[1/2,3/2]. Both e and w increase with z>0, and

$$
 \frac{17}{8}\tau_0\le e\le\frac{33}{8}\tau_0,\quad
 -\frac{11}{8}\tau_0\le p\le-\frac38\tau_0<0,\quad
 \frac34\tau_0\le w\le\frac{15}{4}\tau_0.
$$

Moreover

$$
 e+p=\tau_0(z+z^2)>0,\qquad
 e-p=\tau_0(z+3)>0.
$$

Thus e>|p| and e>0 on the whole patch, including both endpoints. In an orthonormal rest frame the embedded wall stress coefficients have type-I eigenvalues (e,p,p,0): the normal stress is zero, so the fourth inequality e≥|0| is also satisfied. This verifies the dominant energy condition for the stipulated wall surface stress, understood as its coefficient against the nonnegative surface delta measure. It does not prove a microscopic model of the material. The reference radiation separately has the supplied positive density u0 and pressure u0/3; its perturbative response is outside this test. No strong energy condition or self-gravity conclusion is asserted.

The thermodynamic curvature e''=2K and the local compression coefficient n p'=2Kn² are strictly positive. These alone would be insufficient for all membrane modes; the physical inertia and the normal equation must also be checked.

## 4. Tangential conservation and the two in-plane classes

Fix an arbitrary background density n̄ in the patch and put ē=e(n̄), p̄=p(n̄), w̄=ē+p̄, p̄'=p'(n̄). Use physical planar coordinates (t,x,y). To first order in a tangential velocity v=(v_x,v_y), U^a=(1,v_x/c,v_y/c); normalization changes U⁰ only at second order. The linear stress entries are

$$
 \delta S^{00}=e'(\bar n)\delta n,\quad
 \delta S^{0i}=\bar w v_i/c,\quad
 \delta S^{ij}=\bar p'\delta n\,\delta_{ij}.
$$

The number and spatial stress equations therefore give

$$
 \partial_t\delta n+\bar n\,\nabla\!\cdot v=0,\qquad
 \frac{\bar w}{c^2}\partial_t v+\bar p'\nabla\delta n=0.\tag{1}
$$

The temporal stress equation is ∂tδe+w̄∇·v=0. It agrees with number conservation because n̄ e'(n̄)=w̄; it adds no spurious scalar mode. Thus the tangential inertia is w̄/c², not ē/c².

For a nonzero physical wave covector k, isotropy permits k along x. The Fourier system for (δn,v_x,v_y) has characteristic matrix

$$
 A_x=\begin{pmatrix}0&\bar n&0\\ c^2\bar p'/\bar w&0&0\\0&0&0\end{pmatrix},
 \qquad \det(\lambda I-A_x)=\lambda(\lambda^2-c_L^2),
 \quad c_L^2=c^2\frac{\bar n\bar p'}{\bar w}.
$$

Its two compression eigenvectors can be chosen (n̄/λ,1,0), for λ=±c_L; the neutral eigenvector is (0,0,1). All are physical density/velocity variables. Since n̄,w̄,p̄'>0, the eigenvectors are complete and c_L>0. For general k, replace v_x,v_y by the components parallel and perpendicular to k. This rotation changes no eigenvalue.

Substitution of the fixed law yields

$$
 \frac{c_L^2}{c^2}=\frac{2K\bar n}{a+2K\bar n}
 =\frac z{1+z},\qquad \frac13\le\frac{c_L^2}{c^2}\le\frac35.
$$

Equivalently c_L²=c² dp/de, but here that relation follows from (1); it was not used as a substitute for the other polarizations.

The in-plane transverse velocity satisfies ∂t v_⊥=0 with δn=0 for this Fourier polarization. Its frequency and propagation speed are zero. It is a physical neutral vorticity mode, not an elastic shear wave: there is no shear modulus. In a material-displacement description ξ_⊥, one may write ξ_⊥=ξ_⊥(0)+t v_⊥(0). Consequently bounded velocity does not imply bounded material displacement. A time-independent divergence-free relabeling can leave the fluid density and stress unchanged; counting that label freedom as an additional propagating or negative-energy mode would be incorrect. The Eulerian transverse velocity itself is not removed as gauge.

The conserved quadratic energy density for (1) is

$$
 Q_{\parallel}=\frac12\left[
 \frac{\bar w}{c^2}|v|^2+
 \frac{\bar p'}{\bar n}(\delta n)^2\right],\qquad
 \partial_t Q_{\parallel}+\nabla\!\cdot(\delta p\,v)=0.\tag{2}
$$

Indeed multiply the momentum equation by v, the number equation by (p̄'/n̄)δn, and add. Both coefficients are strictly positive, with p̄'/n̄=2K. For isolated Fourier modes, periodic domains or compact support this also gives conservation of the integrated quadratic form. It is the positive local quadratic perturbation energy, not the assertion that the un-subtracted linear variation of total energy vanishes. More explicitly, subtract the background chemical potential μ=e'(n̄) times the conserved lab-frame material density from S00 and expand to second order; the resulting density is (2), up to its constant, using J⁰=n+n̄|v|²/(2c²)+O(perturbation³) and w̄=n̄μ.

In physical first-order variables the symmetrizer is diag(p̄'/n̄,w̄/c²,w̄/c²). It is positive and uniformly bounded above and away from zero for this fixed compact patch and supplied parameters. Its product with each directional A is symmetric. This establishes the constant-coefficient linear tangential principal system's symmetric hyperbolicity, including its semisimple zero-speed vortical mode. It is not a full nonlinear existence theorem.

## 5. Normal displacement, its sign and physical characteristic variables

Embed a perturbed planar surface as X^μ=(ct,x,y,ζ(t,x,y)). To linear order the induced metric is still diag(−1,1,1): its geometric correction is ∂aζ∂bζ, which starts at second order. The declared extrinsic-curvature convention gives

$$
 K_{ab}=-\partial_a\partial_b\zeta+O(\text{perturbation}^2).
$$

Since the background K vanishes, δS·K_background is zero. The background stress entries are S00=ē and Sxx=Syy=p̄, with zero mixed entries. The normal equation hence becomes, after multiplication by −1,

$$
 \frac{\bar e}{c^2}\partial_t^2\zeta+
 \bar p\,\Delta\zeta=0,\qquad
 \omega^2=c_N^2|k|^2,\qquad
 c_N^2=-c^2\frac{\bar p}{\bar e}.\tag{3}
$$

This sign makes negative pressure a positive tension restoring term. The normal inertia is ē/c², distinct from the tangential coefficient w̄/c². At linear order normal displacement and the intrinsic fluid variables decouple on the planar homogeneous background. No such exact decoupling for the finite curved, radiation-loaded sphere is asserted.

Equation (3) has quadratic energy and flux

$$
 Q_N=\frac12\left[
 \frac{\bar e}{c^2}(\partial_t\zeta)^2
 -\bar p|\nabla\zeta|^2\right],\qquad
 \partial_t Q_N+\nabla\!\cdot
 (\bar p\,\partial_t\zeta\,\nabla\zeta)=0.\tag{4}
$$

This follows directly by multiplication of (3) by ∂tζ. Its kinetic coefficient is strictly positive; −p̄≥3τ0/8>0 supplies the positive gradient coefficient. Translation of the whole plane changes no gradient energy, so this is not a norm controlling the absolute offset ζ.

For a physical first-order check, set V=∂tζ and q=∇ζ. Then

$$
 \partial_t V+\frac{c^2\bar p}{\bar e}\nabla\!\cdot q=0,
 \qquad \partial_t q-\nabla V=0,\qquad \nabla\!\times q=0.
$$

For nonzero k the integrability constraint removes q_⊥, leaving (V,q_∥) with directional matrix [[0,c²p̄/ē],[−1,0]], eigenvalues ±c_N and eigenvectors (−λ,1). Both are real, nonzero and complete. On the unreduced gradient system the transverse q zero mode is a constraint variable, not a second physical normal polarization. The positive symmetrizer diag(ē/c²,−p̄,−p̄) makes the principal matrices symmetric and propagates the curl constraint. Including ζ as an integrated position adds a lower-order reconstruction, not another propagating characteristic. These statements are confined to the linear material principal system.

For the fixed law,

$$
 f(z)=\frac{c_N^2}{c^2}=\frac{3-z^2}{z^2+2z+3}.
$$

The numerator is positive since z≤3/2<√3. The denominator is positive, and its excess over the numerator is 2z²+2z>0. Thus 0<f<1. To locate the exact interval bounds,

$$
 f'(z)=-\frac{2(z^2+6z+3)}{(z^2+2z+3)^2}<0,
 \quad f(1/2)=\frac{11}{17},\quad f(3/2)=\frac1{11}.
$$

Therefore 1/11≤c_N²/c²≤11/17. At n0 the speed is c/√3. No sign change, degeneracy or superluminal characteristic is hidden at either endpoint of the declared density interval.

## 6. Finite check table and scope of admission

| Registered check | Result on z∈[1/2,3/2] | At z=1 |
| --- | --- | --- |
| Surface energy e/τ0 | [17/8,33/8] | 3 |
| Pressure p/τ0 | [−11/8,−3/8] | −1 |
| Enthalpy w/τ0 | [3/4,15/4] | 2 |
| Dominant energy condition | e>\|p\| and e>0; zero normal stress allowed | 3τ0>τ0 |
| Compression speed squared /c² | [1/3,3/5] | 1/2 |
| In-plane vortical speed squared /c² | 0, physical neutral velocity | 0 |
| Normal speed squared /c² | [1/11,11/17] | 1/3 |
| Tangent kinetic and compression coefficients | w/c²>0, p'/n=2K>0 | 2τ0/c², τ0/n0² |
| Normal kinetic and gradient coefficients | e/c²>0, −p>0 | 3τ0/c², τ0 |

All three physical classes are now accounted for: two signed longitudinal roots, one neutral vortical root, and two signed normal roots after removal of gradient-constraint artifacts. Isotropy handles every nonzero planar wave direction. The positive block energies also remain valid if speeds from different blocks happen to coincide; no division by their difference was used. No claim that every displacement has a restoring force or remains bounded is made.

The conditional admission is exactly this: the fixed surface-fluid law yields the required static wall stress and positive wall energy at n0, obeys the stated energy condition across the density patch, and has positive quadratic physical material energies with real subluminal local principal speeds there. This is a constructive constitutive/local-principal completion of one previously supplied source assignment. It adds assumptions; it does not uniquely derive matter from DET or from the static tensor.

It supplies no finite-wavelength approximation theorem for a sphere, perturbed radiation traction, reflection law, moving-source dynamics, radial/nonspherical/global stability, nonlinear well-posedness, microscopic realization, fabrication or empirical permission. Curvature and load terms were excluded, not estimated to be harmless. Restoring signs in the planar principal part can coexist with lower-order instabilities in a different coupled problem. No gravitational field, active-mass correction, boost/acceleration coefficient, native unit, physical heat, absolute calibration, efficiency or historical law genesis is inferred. Retired kappa-gravity remains retired.

Static gravitational reuse retains the accepted zeroth-order matter tensor and linearized field ordering. A loaded or moving source additionally requires an evolving wall embedding with curvature and load terms, a radiation transport and reflection or interaction law, matched perturbed traction, and the full conserved tensor with its boundary conditions. Those additional premises are not supplied by this local material test.

## 7. Sources and independent review

This article preserves Classical result CL107: one fixed constitutive assignment for the adopted complete static radiation-shell source and its separate unloaded planar material test. The source convention and tension relation are those of the linked complete-source article. The same-source boost and Newtonian fluid-crossing results delimit separate questions; they provide no new numerical premise here.

The public primary reference is [Mourão, Natário and Vicente, arXiv:2409.10602v1](https://arxiv.org/html/2409.10602v1), sections 2.1–2.3 and 2.5 through equation 62. The donor inspected this exact HTML version for the conventional worldvolume and polarization framework. No full-paper review, Dyson-sphere stability result, literature novelty or transfer of its particular elastic law is claimed. The equations and inequalities above were derived from the supplied laws; no source speed formula replaced the physical derivations. This assembly reuses the recorded source inspection and adds no new literature-read claim.

The author inherited source-informed design hypotheses, including the candidate reference-density speeds, and independently derived the equations, signs, energy forms and interval bounds. A distinct Classical reviewer then challenged the stable result. That review was nonblind: the reviewer designed the control and had prospective exposure to the pressure and mode hypotheses. A separate Relational State recipient review assessed the static source correspondence and limits while reusing the completed proof. The coordinator admitted the exact material assignment and full three-class planar test at the scope stated above.
