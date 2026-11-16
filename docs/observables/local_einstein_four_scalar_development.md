# Local Einstein–four-scalar development of a fixed expectation source

Conditional analytic result

The specified fixed-state source reduces exactly to four real, positive-kinetic, massless classical scalars. Their accepted expanding-torus data satisfy the Einstein constraints with the same energy, zero normal flux and full inhomogeneous spatial stress. With the supplied Einstein and scalar wave equations, standard smooth quasilinear-wave local existence, and the constraint-propagation argument below, these data admit a local coupled development, geometrically unique as a local germ up to diffeomorphism. The result gives no quantitative lifespan, no guarantee through $4\tau$, and no continuation of the earlier stationary four-tick probe identity or generator.

This is a conditional mathematical model, not a native DET derivation or a required quantum ontology. The scalar reduction is an equality of the prescribed stress expectation, not an identification of all operator observables with four classical fields. No new state, quantum modes, source averaging, energy shift or mean subtraction is introduced.

The [local scalar source](local_scalar_source_for_four_chain_field.md) supplies the fixed algebra, state, mode normalization and source convention. The [expanding flat-torus initial-data construction](expanding_torus_initial_data_for_scalar_source.md) establishes initial constraint compatibility only. The present construction addresses its remaining evolution premise by supplying the coupled equations stated below.

## Fixed-state source and exact four-scalar reduction

Let $(M,g)$ have signature $(-+++)$, with time coordinates expressed in length units when writing spacetime components. Keep the same fixed canonical operators
$$
 R_A=(Q_1,P_1,Q_2,P_2),\qquad [Q_j,P_k]=i\delta_{jk}I,
$$
on $L^2(\mathbb R^2)$, and the same centered Gaussian functional $\omega$. Its symmetrized covariance is
$$
 \frac12\omega(\{R_A,R_B\})=\frac12\delta_{AB}.
 \tag{1}
$$
The supplied evolving field prescription is
$$
 \Psi(x)=\sum_{A=1}^4 R_A F_A(x),\qquad
 (F_1,F_2,F_3,F_4)=(f_1,g_1,f_2,g_2),
 \qquad \Box_gF_A=0. \tag{2}
$$
Here the $F_A$ are real smooth scalar functions, and $g$ is a classical metric determined by the coupled equations. The symbols $g_j$ for coefficients are distinct from the metric $g$. The operators and the functional $\omega$ remain fixed; the coefficients carry the spacetime dependence. No instantaneous ground-state selection is made as the geometry changes.

Use the same symmetric kinetic tensor, now on that metric:
$$
 T_{\mu\nu}=\kappa\left[
 \frac12\{\nabla_\mu\Psi,\nabla_\nu\Psi\}
 -\frac14g_{\mu\nu}g^{\alpha\beta}
       \{\nabla_\alpha\Psi,\nabla_\beta\Psi\}\right],
 \qquad \mathsf T_{\mu\nu}=\omega(T_{\mu\nu}).
 \tag{3}
$$
There is no improvement, potential or cosmological term. Because the coefficients are ordinary real functions, (1) implies
$$
 \mathsf T_{\mu\nu}
 =\frac{\kappa}{2}\sum_A
 \left[\nabla_\mu F_A\nabla_\nu F_A
 -\frac12g_{\mu\nu}\nabla_\alpha F_A\nabla^\alpha F_A\right].
$$
The candidate normalization is therefore proved:
$$
 \boxed{\chi_A=\sqrt{\kappa/2}\,F_A,\qquad
 \mathsf T_{\mu\nu}=\sum_{A=1}^4
 \left[\nabla_\mu\chi_A\nabla_\nu\chi_A
 -\frac12g_{\mu\nu}(\nabla\chi_A)^2\right].} \tag{4}
$$
Antisymmetric commutator terms do not survive the symmetric ordering. This is exact on the same oscillator Schwartz domain: fields and their derivatives are finite linear combinations of $R_A$, and the stresses are quadratic polynomials there. No ultraviolet limit or renormalization is involved.

With all four wave equations in (2) imposed on the same metric,
$$
 \nabla^\mu\mathsf T_{\mu\nu}
 =\sum_A(\Box_g\chi_A)\nabla_\nu\chi_A=0. \tag{5}
$$
The four separate wave equations are supplied matter equations. Conservation by itself does not imply them individually, since the sum on the right can vanish without every wave residual vanishing.

Write $\lambda_G=8\pi G/c^4>0$. The proposed expectation-coupled equations become exactly
$$
 G_{\mu\nu}(g)=\lambda_G\mathsf T_{\mu\nu},\qquad
 \Box_g\chi_A=0,
$$
or, by trace reversal in four spacetime dimensions,
$$
 \boxed{R_{\mu\nu}(g)=\lambda_G
          \sum_A\nabla_\mu\chi_A\nabla_\nu\chi_A,\qquad
        \Box_g\chi_A=0.} \tag{6}
$$
Rescaling once more by $\varphi_A=\sqrt{\lambda_G}\chi_A$ gives the unit-coupling convention $G=\sum_A t[\varphi_A]$. This accounts for the physical factor $8\pi G/c^4$ rather than suppressing it through notation.

For any future unit normal $n$, let $\Pi_A=n^\mu\nabla_\mu\chi_A$ and $D$ be the induced spatial derivative. The full normal decomposition of (4) is
$$
 \rho=\frac12\sum_A(\Pi_A^2+|D\chi_A|^2),\qquad
 J_i=-\sum_A\Pi_A D_i\chi_A,
$$
$$
 S_{ij}=\sum_A\left[D_i\chi_A D_j\chi_A
 +\frac12\gamma_{ij}(\Pi_A^2-|D\chi_A|^2)\right]. \tag{7}
$$
The energy density is nonnegative in any such smooth development. No perfect-fluid or homogeneous-stress replacement has been used.

## Accepted torus Cauchy data

The accepted initial slice is $\Sigma=\mathbb T_L^3$, with
$$
 L=8c\tau,\quad V_0=L^3,\quad \gamma_{ij}=\delta_{ij},\qquad
 K_{ij}=b\gamma_{ij},\qquad
 K_{ij}=-\tfrac12{\cal L}_n\gamma_{ij},
$$
$$
 b=-\sqrt{\frac{8\pi G\rho_E}{3c^4}}<0.
 \tag{8}
$$
Retain the original profiles and scales:
$$
 u_j(x)=\cos\alpha_j,\quad \alpha_j=k_j\cdot x+\delta_j,\quad
 k_1=\frac{10\pi}{L}e_1,\quad k_2=\frac{14\pi}{L}e_2,\quad
 \omega_j=c|k_j|,
$$
$$
 \omega_1\tau=\frac{5\pi}{4},\quad \omega_2\tau=\frac{7\pi}{4},\quad
 \delta_2=0,\quad
 \cos\delta_1=(\sqrt2-1)\sqrt{5/7},\quad
 B_j^2=\frac{2A_*c^2}{\kappa V_0\omega_j}.
$$
The issued data in coefficient form are
$$
 f_j|_\Sigma=B_ju_j,\quad g_j|_\Sigma=0,\qquad
 nf_j|_\Sigma=0,\quad ng_j|_\Sigma=\frac{B_j\omega_j}{c}u_j.
 \tag{9}
$$
The $1/c$ is required because $n$ differentiates with respect to proper length. Let $C_j=\sqrt{\kappa/2}B_j$. The four classical scalar Cauchy pairs are consequently
$$
 (\chi_{f_j},\Pi_{f_j})|_\Sigma=(C_ju_j,0),\qquad
 (\chi_{g_j},\Pi_{g_j})|_\Sigma=(0,C_j\omega_ju_j/c).
 \tag{10}
$$
Every datum is smooth and periodic, including at torus chart identifications.

For each mode, the nonzero normal-square and spatial-gradient-square pieces in (7) contribute respectively
$$
 \rho_j\cos^2\alpha_j,\qquad \rho_j\sin^2\alpha_j,\qquad
 \rho_j=\frac{\kappa B_j^2|k_j|^2}{4}
       =\frac{A_*\omega_j}{2V_0}.
$$
Thus (7) gives, pointwise,
$$
 \rho|_\Sigma=\rho_1+\rho_2=\rho_E
 =\frac{3\pi A_*}{1024c^3\tau^4}>0,\qquad J_i|_\Sigma=0,
$$
$$
 S_{ab}|_\Sigma=\sum_j\rho_j
 \left[d_j^ad_j^b+(\delta_{ab}-d_j^ad_j^b)\cos2\alpha_j\right],
 \qquad d_j=k_j/|k_j|. \tag{11}
$$
The vanishing flux follows because each nonzero spatial gradient and each nonzero normal derivative belong to different scalar coefficients in (10). The full spatial stress, not just $\rho,J$, agrees with the accepted fixed-state tensor. In particular it is anisotropic and spatially varying. Its initial integral is
$\int_\Sigma S_{ab}\,dV_0=\operatorname{diag}(E_1,E_2,0)$, with
$E_j=A_*\omega_j/2$; no compact-source stress cancellation is imposed on the torus.

The initial Einstein constraints in the accepted conventions are
$$
 {}^{(3)}R+K^2-K_{ij}K^{ij}=2\lambda_G\rho,\qquad
 D_jK^j{}_i-D_iK=\lambda_GJ_i.
 \tag{12}
$$
For (8), their left sides are $6b^2$ and zero, respectively, exactly matching (11). All four constraints hold without a source correction. The initial expanding proper-volume rate remains
$$
 {\cal H}_0=-cb>0,\qquad
 ({\cal H}_0\tau)^2=\frac{\pi^2}{128}\frac{GA_*}{c^5\tau^2}.
 \tag{13}
$$
This is an initial statement. The spatial stress in (11) remains a source for the future Einstein evolution; flat $\gamma$ and isotropic $K$ on one slice do not imply a homogeneous future metric.

## Imported local Cauchy theorem and its scope

The PDE input must be stated accurately. The pinned primary source is Choquet-Bruhat, Isenberg and Pollack, *Applications of theorems of Jean Leray to the Einstein-scalar field equations*, arXiv gr-qc/0611009v1, [versioned primary text](https://arxiv.org/pdf/gr-qc/0611009v1).
Its §§2–3, printed pages 3–6, specify the scalar kinetic stress, wave equation and Cauchy decomposition. Section 4, page 7, explicitly separates evolution hyperbolicity from the Bianchi argument needed to obtain a full constrained solution. Theorem 4.1 on page 10 states hyperbolicity of its particular lapse-conditioned evolution system. It is not, by itself, a theorem of four-field geometric uniqueness. The arbitrary-lapse discussion in §4.1 is Leray–Ohya/Gevrey; one must not silently substitute a general smooth-data conclusion for that formulation.

We use the standard local Cauchy theorem for finite smooth quasilinear wave systems on a spacelike initial hypersurface, within the hyperbolic framework described in §4. Its mathematical content here is: a normally hyperbolic, smoothly coupled finite system with Lorentzian principal metric and sufficiently regular compatible Cauchy data has a unique local reduced solution in its chosen gauge, with continuous dependence. We use smooth data, lying in every sufficiently high Sobolev class on this compact torus; for example an integer $s\ge6$ is a safe non-sharp regularity choice for the usual wave-system estimates. No low-regularity threshold or quantitative existence-time estimate is claimed. This theorem is imported mathematics, not inferred from the native field or proved anew from estimates in this packet.

## Wave-map reduction and gauge data

Here is the explicit reduction that makes its use legitimate for four fields. Choose a smooth reference product connection and wave-map gauge vector
$$
 {\cal C}^\mu=g^{\alpha\beta}
 \bigl(\Gamma^\mu_{\alpha\beta}(g)-\widehat\Gamma^\mu_{\alpha\beta}\bigr).
$$
Use the reduced system
$$
 R_{\mu\nu}-\nabla_{(\mu}{\cal C}_{\nu)}
   =\sum_{A=1}^4\partial_\mu\varphi_A\partial_\nu\varphi_A,
 \qquad \Box_g\varphi_A=0. \tag{14}
$$
In the flat reference charts its metric principal part is
$-\tfrac12g^{\alpha\beta}\partial_\alpha\partial_\beta g_{\mu\nu}$.
It is accompanied by four diagonal scalar wave blocks
$g^{\alpha\beta}\partial_\alpha\partial_\beta\varphi_A$.
All additional couplings contain only first derivatives of the unknown metric and scalars, with smooth coefficients while $g$ is Lorentzian. Replacing one scalar by four copies therefore adds finite scalar wave blocks and finite sums of lower-order terms; it does not change the principal causal cone or introduce derivative loss. This explicit principal-part argument, not merely the name “Einstein–scalar,” is the finite-four extension used here.

The initial metric is Lorentzian with spacelike $\Sigma$; choose initial lapse one and shift zero. Gauge-compatible normal derivatives of lapse and shift can be assigned to set ${\cal C}|_\Sigma=0$. In local affine periodic charts with $x^0$ in length units and flat reference connection, one concrete choice is
$$
 g_{00}|_\Sigma=-1,\quad g_{0i}|_\Sigma=0,\quad
 \partial_0g_{ij}|_\Sigma=-2b\delta_{ij},\quad
 \partial_0g_{00}|_\Sigma=6b,\quad
 \partial_0g_{0i}|_\Sigma=0. \tag{15}
$$
Indeed initially $\Gamma^0=\tfrac12\partial_0g_{00}-3b$ and
$\Gamma^i=-\partial_0g_{0i}$. These choices affect gauge data, not $\gamma,K$ or (10). Lapse and shift need not remain constant in the future. The scalar coordinate derivatives in this initial gauge equal the normal derivatives in (10), with the additional constant rescaling for $\varphi$.

The smooth wave-system theorem now gives a reduced solution on a nonzero collar of the initial slice. Compactness permits a common positive collar by a finite patch cover and uniqueness on overlaps; periodic chart transitions are compatible. The conclusion is an existence interval $(-\epsilon,\epsilon)$ in a suitable time coordinate for some $\epsilon>0$ depending on the data and gauge. It supplies no numerical bound in seconds or in multiples of the reference tick.

## Constraint propagation

Constraint propagation is a separate step. Define the Einstein residual of the reduced solution by
$$
 {\cal E}_{\mu\nu}=G_{\mu\nu}
 -\sum_A\left(\partial_\mu\varphi_A\partial_\nu\varphi_A
 -\tfrac12g_{\mu\nu}(\partial\varphi_A)^2\right).
$$
Taking the trace of (14) gives
$$
 {\cal E}_{\mu\nu}
 =\nabla_{(\mu}{\cal C}_{\nu)}
  -\tfrac12g_{\mu\nu}\nabla_\alpha{\cal C}^\alpha. \tag{16}
$$
The four imposed wave equations imply matter conservation by (5). The contracted Bianchi identity then yields the homogeneous subsidiary wave equation
$$
 \Box_g{\cal C}_\nu+R_{\nu\mu}{\cal C}^\mu=0. \tag{17}
$$
The sign is fixed by the gauge-vector definition and the standard Ricci convention in (14). The satisfied constraints are exactly the initial normal projections ${\cal E}(n,\cdot)=0$. Since ${\cal C}|_\Sigma=0$, its tangential derivatives vanish there; (16) and these four projections force $n{\cal C}|_\Sigma=0$. In an initially orthonormal adapted frame these residual components reduce to one half of the corresponding normal derivatives of ${\cal C}$. Uniqueness for the homogeneous wave problem (17) gives ${\cal C}=0$ on a possibly smaller collar. Thus (14) solves the full Einstein equations (6), and the Hamiltonian and momentum constraints remain satisfied. This supplies the step the primary source explicitly requires in addition to evolution hyperbolicity.

## Local geometric uniqueness

Local geometric uniqueness is also a separate conclusion. Put any two smooth developments of these same metric, extrinsic-curvature and four scalar Cauchy data into common wave-map coordinates with the same initial coordinate and normal data. The coordinate wave problems have local solutions with nonsingular initial Jacobians, so they define local diffeomorphisms after shrinking the collar. The two metric–scalar systems then have identical reduced Cauchy data and coincide by reduced uniqueness. Hence the developments agree locally up to a diffeomorphism fixing the initial-data identification. This is uniqueness of the local germ, not uniqueness of arbitrary coordinates, a maximal-development construction, or a global existence theorem.

## Reconstructed source and limits

Recovering $F_A=\sqrt{2/\kappa}\chi_A$ on that development reconstructs (2) on the same two-pair algebra and gives exactly the same expectation source (4). This closes the proposed metric–source equations; no independently evolved state covariance is needed because the fixed functional is the stipulated prescription. The word “ground” describes the inherited reference Gaussian, not a claim that it stays the instantaneous vacuum of the evolving geometry.

The reduction does not assert that the four functions remain the original two standing profiles multiplied by time-dependent amplitudes. On an inhomogeneous evolving metric their spatial dependence can change. It is a finite number of scalar fields, each a spacetime function, not a finite-dimensional ordinary differential system or a new addition of quantum oscillator pairs.

The operator commutator remains
$$
 [\Psi(x),\Psi(y)]
 =i\sum_{j=1}^2
   \bigl[f_j(x)g_j(y)-g_j(x)f_j(y)\bigr]I. \tag{18}
$$
Its separable kernel has rank at most four. This is not the full local field delta algebra, a general quantum field theory, or a proof of microcausality. The four classical fields reproduce this model's stress expectation; they need not reproduce its noncommuting observables as classical random measurements. No claim about physical quantum ontology is necessary for (4)–(17).

The fixed initial source has energy $E_0=3\pi A_*/(2\tau)$, and the same local initial probe data as the accepted scalar packet. Subsequent covariant conservation does not guarantee that a spatial energy integral stays equal to $E_0$ on a time-dependent geometry, or furnish the old stationary Hamiltonian. The old constant-frequency evolution, four-tick covariance matrix and operator sample identity are reference-background results. They do not transfer to this coupled solution. Even the existence of the events at a future elapsed time $4\tau$ is not certified by the local theorem.

The previous static-periodic Poisson obstruction remains valid. The present solution starts with nonzero extrinsic curvature, whose quadratic constraint contribution balances the positive mean energy. It does not obtain a static solution by subtracting that mean. This packet proves a local dynamical development of the accepted nonlinear initial data, not a globally stationary source, an asymptotic exterior, a homogeneous cosmology or a global nonlinear solution.

The attachment still conditions on the same supported chain $a<b<x<y$, whose source-conditioned structural weights are $779/1320$ and $574/1320$. Its four fair suffix-mark assignments retain weights $779/5280$ and $574/5280$, respectively. Every other native history retains its original weight, with this scalar–gravity attachment unavailable there. No all-branch construction or native reweighting follows from evolving the selected branch's supplied field data.

With field units ${\cal F}$, the coefficient functions have units ${\cal F}$, $\kappa$ has units energy/(${\cal F}^2$ length), and $\chi_A$ has units $\sqrt{\text{energy}/\text{length}}$. Thus $(\nabla\chi_A)^2$ has energy-density units; $\lambda_G$ has units length/energy; $\varphi_A$ is dimensionless and the right side of the trace-reversed equation has inverse-length squared units. The fixed normalized initial amplitude satisfies
$$
 C_j^2=\frac{A_*c^2}{V_0\omega_j}.
$$
Cancellation of $\kappa$ reflects the same field-unit normalization freedom as before. It does not determine $G,c,\tau,A_*$, a native length, a physical time standard or a mass calibration. Relation (13) is still a conditional initial scale relation.

Physical source preparation, coherent or otherwise, clock registration, local readout, reset and a closed work-store boundary remain unsupplied. Local PDE existence is not a preparation algorithm, a complete energy budget or empirical validation. These distinctions remain requirements for downstream use.

## Reviewed basis

DET Energy Research supplied the finite analytic derivation. DET Relational State Research independently verified the covariance contraction and normalization, complete initial source projections and four constraints, covariant conservation, finite hyperbolic principal-block extension, gauge initialization and subsidiary propagation, and local geometric uniqueness. That review checked the source paper's narrower theorem against the separately imported smooth Cauchy mathematics and found no scientific correction required.

The result admits this supplied fixed-state prescription as a conditional four-real-scalar Einstein model with a justified local development. Its next use may rely on exact source closure and local existence only. Any future-time probe, quantitative lifespan, global property or physical implementation requires a separate justification.
