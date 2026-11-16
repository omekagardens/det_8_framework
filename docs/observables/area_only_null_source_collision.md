# Area-only records and distinct null sources

The two prescribed metrics have the same three normalized area readings and the same complete positive area history on 0<=u<=U=pi L/4, but different Ricci/null-source contractions for every u>0 in that interval. The vacuum pencil carries shear; the isotropic pencil carries a positive Ricci term instead. One unordered endpoint semiaxis ratio distinguishes this fixed pair. All results below are conditional on supplied conventional geometry, affine registration, infinitesimal geometric optics and Einstein source conversion; they are not native gravity or empirical results.

## 1. Source conventions and exact scope

Earlier vacuum field-input and field-history comparisons delimit the question: a common zero matter tensor need not fix distinct vacuum tidal readings, and common final curvature need not fix retained motion after different field histories. Their metrics and numerical results are not premises here.

The conventional plane-wave framework follows [Abraham I. Harte, arXiv:1210.1449v2, section 2](https://arxiv.org/html/1210.1449v2), using the metric/curvature/Jacobi conventions of equations 1, 3, 4 and 9–11. The exact pair, full checks and finite observation decision below are directly derived. No full-paper claim or literature-novelty claim is made, and no unrelated interaction-energy or scalar-source/initial-constraint result is used.

Coordinates (u,v,x,y) have length units, L,G,c are positive supplied constants, and the metric signature is (-+++). Let xbold=(x,y), K(u,xbold)=xbold^T H(u) xbold, and

```text
ds²=-2du dv+K du²+dx²+dy².
```

Exactly two profiles are used:

```text
H_A=L^(-2) diag(-1,+1),
H_B=-q(u) I_2,
q(u)=[tan(u/L)+tanh(u/L)]²/(4L²).
```

The open patch is -pi L/8<u<3pi L/8, |x|,|y|<L and |v|<L. Both profiles are smooth on it; its closure in u stays away from the tangent pole. The observation segment [0,U] lies strictly inside. Nothing is spliced or switched on at 0 or U, so no junction or distributional curvature is introduced. No global extension is asserted.

## 2. Complete local geometry and source

In coordinate order (u,v,x,y), the metric and inverse have the blocks

```text
g_uv-block=[[K,-1],[-1,0]],
g_inverse_uv-block=[[0,-1],[-1,-K]],
g_ij=g_inverse_ij=delta_ij,
```

with all other components zero. The determinant is -1. The two eigenvalues of the first block are (K±sqrt(K²+4))/2, one negative and one positive, and both transverse eigenvalues are +1. The signature is therefore Lorentzian throughout the patch, without a small-K approximation.

Use

```text
R^rho_(sigma mu nu)=partial_mu Gamma^rho_(nu sigma)-partial_nu Gamma^rho_(mu sigma)
 +Gamma^rho_(mu lambda) Gamma^lambda_(nu sigma)-Gamma^rho_(nu lambda) Gamma^lambda_(mu sigma),
R_(sigma nu)=R^rho_(sigma rho nu).
```

Direct substitution in the Levi-Civita formula gives the complete potentially nonzero connection pattern, with i=x,y:

```text
Gamma^i_(uu)=-(H xbold)_i,
Gamma^v_(ui)=Gamma^v_(iu)=-(H xbold)_i,
Gamma^v_(uu)=-(1/2) xbold^T H_prime xbold.
```

Every connection with upper u or a lower v vanishes. All remaining unlisted connections vanish. Here and below a prime means d/du, not d/d(u/L).

For example, partial_j Gamma^i_(uu)=-H_ij gives R^i_(u j u)=-H_ij. In the sectors with a u derivative, partial_u Gamma^v_(ui) and partial_i Gamma^v_(uu) cancel their H_prime terms. The connection products introduce no extra covariant sectors because all lower-v and upper-u connections vanish. The complete covariant Riemann pattern is

```text
R_(u i u j)=-H_ij,
```

and those obtained from antisymmetry within either index pair and exchange of the two pairs; all other components vanish. In these diagonal profiles the independent entries are R_uxux and R_uyuy, and R_uxuy=0. Hence:

| Model | R_uxux | R_uyuy | R_uu |
|---|---:|---:|---:|
| A | +1/L² | -1/L² | 0 |
| B | q(u) | q(u) | 2q(u) |

More generally R_uu=-tr H, while R_uv,R_vv,R_ui,R_vi and R_ij are all zero. Because g^uu=0, the scalar R is zero in both models. Scalar flatness is not mistaken for vacuum: A has the full Ricci tensor zero, whereas B has R_uu=2q. For 0<u<=U, tan(u/L)+tanh(u/L)>0, so q>0; q(0)=0. A has nonzero Riemann curvature even though it is vacuum.

The four-dimensional Weyl decomposition gives C_(u i u j)=-H_ij+(tr H/2)delta_ij, with the same zero-sector pattern. Thus A's displayed curvature is Weyl curvature, while B has zero Weyl tensor and the displayed Ricci curvature. This statement concerns these local supplied metrics only.

Under the added Einstein equation with Lambda=0, the Einstein tensor equals the Ricci tensor since R=0. Let n^a=(partial_v)^a. It is null everywhere and n_a=-(du)_a. Its covariant derivative vanishes because every Gamma^a_(mu v)=0. The required source is

```text
T_ab=mathcalT(u) n_a n_b=mathcalT(u) (du)_a(du)_b,
mathcalT(u)=-(c^4/(8pi G))tr H.
```

In A, T_ab=0. In B, mathcalT=c^4 q/(4pi G)>=0. For any null w, T_ab w^a w^b=mathcalT(w^u)²>=0; the same square is nonnegative for timelike vectors. This is a conserved nonnegative null stress, not a rest-mass density. Indeed

```text
n^a partial_a mathcalT=partial_v mathcalT=0,
nabla_a n^b=0,
```

so nabla_a T^(ab)=0 throughout the patch. All its other covariant coordinate components vanish. Conservation is checked locally rather than assumed from an unspecified material realization. No microscopic radiation field, emitter or compact isolated source is supplied.

## 3. Reference ray, screen and an actual neighboring null family

The reference ray is gamma(u)=(u,0,0,0), with k=partial_u. On it K=0, so g(k,k)=0 and g(k,n)=-1. Every connection in section 2 vanishes at x=y=0, so nabla_k k=0 and u is affine. The screen vectors e1=partial_x and e2=partial_y satisfy g(e_i,e_j)=delta_ij, are orthogonal to k,n, and obey nabla_k e_i=0. This verifies the physical screen metric and parallel transport rather than assuming coordinate distances suffice away from the ray.

The pair normalization g(k,n)=-1 by itself allows reciprocal rescaling of k and n. The stipulated coordinates, k=partial_u, n=partial_v and calibrated L/affine registration select the common scale; it is not intrinsically derived from the null ray.

Consider a small constant transverse launch offset a in R² and a matrix J satisfying J_doubleprime=H J, J(0)=I_2, J_prime(0)=0. Define the exact curves

```text
xbold(u,a)=J(u)a,
v(u,a)=(1/2) xbold(u,a) dot xbold_prime(u,a),
u(u,a)=u.
```

The last line means u itself is used as affine parameter, not a new coordinate function. Their initial coordinates are xbold(0,a)=a and v(0,a)=0. They have xbold_prime(0,a)=0 and

```text
v_prime=(1/2)(|xbold_prime|²+xbold^T H xbold).
```

Consequently -2v_prime+|xbold_prime|²+K=0: every curve is null. Its transverse geodesic equation is xbold_doubleprime-H xbold=0. Differentiating v_prime gives

```text
v_doubleprime=2 xbold_prime^T H xbold+(1/2)xbold^T H_prime xbold,
```

which is exactly the remaining v-geodesic equation from the complete connections. The u equation is u_doubleprime=0. Thus this is an actual null-geodesic family, not merely a solution of an unrelated transverse ODE.

At a=0, variation with respect to a gives the screen deviation J(u)a; v and its variation are quadratic and linear in a respectively, so the first variation of v vanishes at the central ray. The initial screen deviation is a and its covariant derivative is zero. The full neighboring initial v_prime(0,a) is of order |a|² and can differ between metrics; identical full gravitational or finite-neighbor initial data are not claimed.

The Jacobi sign agrees independently with curvature: R^i_(u u j)=+H_ij in the stated convention, so the geodesic-deviation equation yields xi_doubleprime=H xi. Along the parallel screen this is exactly J_doubleprime=H J. The chosen initial map is nonzero; this is a prepared initially circular pencil, not the point-source angular-diameter-distance initial condition J(0)=0.

For either exact solution below, J and J_prime are bounded on the compact segment. With M=max||J|| and N=max||J_prime|| over both models, choose a common delta>0 with M delta<L and MN delta²/2<L (the second condition is void if N=0). Then |a|<delta keeps every neighboring curve within |x|,|y|<L and |v|<L throughout [0,U]. Such a delta exists. This establishes a complete finite-interval local family within the stated patch; it supplies no physical finite-beam accuracy guarantee.

## 4. Exact Jacobi solutions, positive area and all retained cells

Set s=u/L. For A the two decoupled scalar equations have the unique solutions with the registered initial data

```text
J_A(u)=diag(cos s,cosh s).
```

For B define D(s)=cos s cosh s and r(s)=sqrt(D(s)), taking the positive branch on the segment. Let a_s=tan s and b_s=tanh s. Then

```text
r_prime/r=(b_s-a_s)/(2L),
r_doubleprime/r=[sech²s-sec²s]/(2L²)+(b_s-a_s)²/(4L²)
 =-(a_s+b_s)²/(4L²)=-q(u).
```

Thus J_B(u)=r(s) I_2 satisfies J_B_doubleprime=H_B J_B, J_B(0)=I_2 and J_B_prime(0)=0. Smoothness and uniqueness of the linear initial-value problem apply because the coefficients are smooth on the open patch. These matrices have been verified, not taken as accepted inputs from the design hypotheses.

On 0<=s<=pi/4, cos s>=1/sqrt(2)>0 and cosh s>=1. Both maps are therefore nonsingular and orientation-preserving, and all their singular values are positive. In particular there is no area-caustic of this prepared pencil anywhere in the registered interval. For s>0, tan s>tanh s, as follows from the positive derivative sec²s-sech²s and equality at zero. Hence

```text
D_prime/D=(tanh s-tan s)/L<0,
D(U)<=D(u)<=D(0)=1,
D(U)=cos(pi/4)cosh(pi/4)>0.
```

Both determinants are exactly D(u)=cos(u/L)cosh(u/L). The complete retained normalized area record is therefore:

| Model | D(0) | D(U/2) | D(U) |
|---|---:|---:|---:|
| A | 1 | cos(pi/8)cosh(pi/8) | cos(pi/4)cosh(pi/4) |
| B | 1 | cos(pi/8)cosh(pi/8) | cos(pi/4)cosh(pi/4) |

Equality holds at every intermediate u as well. A small initial circular screen section of area A_initial has infinitesimal area A_initial det J. The normalized determinant is dimensionless; no absolute optical brightness or distance claim is used. At fixed u, the induced inner product on the family variations is J^T J, since du=0 and all dv contributions to the transverse induced metric vanish. This connects the retained area and shape to the verified family/screen geometry.

## 5. Full optical focusing ledger

Define the optical deformation matrix Bopt=J_prime J_inverse, expansion theta=tr Bopt, traceless symmetric shear S=Bopt-theta I_2/2, and twist as the antisymmetric part of Bopt. Both Bopt matrices here are diagonal and have zero twist. Differentiating gives Bopt_prime+Bopt²=H. Taking the trace gives, with R_kk=-tr H,

```text
theta_prime=-theta²/2-tr(S²)-R_kk.
```

This fixes the shear normalization explicitly; tr(S²) is the sum of squared screen-matrix eigenvalues. No convention-dependent extra factor is suppressed.

For A,

```text
Bopt_A=L^(-1)diag(-a_s,b_s),
theta_A=(b_s-a_s)/L,
S_A=(a_s+b_s)/(2L) diag(-1,+1),
tr(S_A²)=(a_s+b_s)²/(2L²)=2q,
R_kk,A=0.
```

For B,

```text
Bopt_B=(b_s-a_s)/(2L) I_2,
theta_B=(b_s-a_s)/L,
S_B=0,
R_kk,B=2q.
```

Thus both have exactly the same expansion, as their area histories require, but different shear/Ricci allocations. Direct differentiation independently gives

```text
theta_prime=[sech²s-sec²s]/L²=-(a_s²+b_s²)/L²,
-theta_prime-theta²/2=(a_s+b_s)²/(2L²)=2q.
```

The complete ledger is:

| Model | theta | twist | tr(S²) | R_kk | tr(S²)+R_kk |
|---|---|---:|---:|---:|---:|
| A | (b_s-a_s)/L | 0 | 2q | 0 | 2q |
| B | (b_s-a_s)/L | 0 | 0 | 2q | 2q |

Every term vanishes at u=0 except A's underlying Weyl curvature. For u>0 the last column is positive. The area-derived combination -theta_prime-theta²/2 therefore does not equal the Ricci contraction in A, although it does in B. The noncaustic full area history cannot by itself select between these two source contractions. This is the exact omitted-shear ambiguity, not a failure of the Raychaudhuri equation.

The verified source contractions are T_kk,A=0 and T_kk,B=c^4 q/(4pi G), with the stipulated k normalization. They are null stress components. Neither a dust rest density nor a global source mass is inferred from them.

## 6. One endpoint shape reading

The singular values of J_A(U) are cos(pi/4) and cosh(pi/4), whereas both singular values of J_B(U) equal sqrt(cos(pi/4)cosh(pi/4)). Therefore the unordered larger/smaller semiaxis ratios are

```text
Rshape_A=cosh(pi/4)/cos(pi/4)=sqrt(2)cosh(pi/4)>1,
Rshape_B=1.
```

They are invariant under orthogonal choices of initial/final screen axes and do not require preserving the sign of an axis label. The proposed one endpoint scalar distinguishes the two prescribed metrics and hence their Ricci/null-source histories within this two-member family. No general local Ricci reconstruction from a single shape measurement follows. The exact separation is a mathematical record statement; finite instrument errors and acquisition feasibility are not supplied.

## 7. Interpretation, units and scope

The retained area triples, and even their full histories, agree while R_kk differs at every u in (0,U]. Both models share the stipulated screen/affine launch and initial optical map; they do not share full metric curvature or gravitational initial/boundary data. Adding endpoint shape resolves this exact pair. The earlier vacuum comparison instead used different vacuum curvature with the same zero matter input; the field-history comparison used retained motion after different histories with the same final curvature. This packet tests the conversion from optical area to a null-source contraction. It does not claim a new general relativity law or exhaustive optical inverse theorem.

With length-valued coordinates, [L]=length, [H]=[q]=[R_kk]=length^(-2), [Bopt]=[theta]=[S]=length^(-1), while J,D and Rshape are dimensionless. J_prime has inverse-length units; physical deviation vectors multiply J by an initial length. With [G]=length³/(mass*time²) and [c]=length/time, [T_kk]=energy/volume for the registered dimensionless tangent components. The source conversion requires the independently supplied G,c and affine normalization.

If the same ray is reparameterized by ubar=a u with a>0, its tangent becomes kbar=k/a. Expansion and shear referred to that parameter scale by a^(-1), while R_kbar_kbar and T_kbar_kbar scale by a^(-2). The geometric section area and shape at a specified event do not change, but their argument and derivatives do. A null normalization or length standard is therefore not derived merely by recording an area ratio. The present comparison fixes that registration explicitly in both models.

The continuum metrics, classical field equation, geometric-optics and infinitesimal-pencil description, ideal readout, preparations and standards are all supplied. No native DET geometry, count-to-volume rule, mass or unit, empirical gravity validation, actual source generation, compact isolation, gravitational-wave energy ledger, point-source distance/flux, detector precision or finite-baseline calibration follows. There is no physical-execution permission, law-genesis result or ontology validation. Retired kappa-gravity remains retired; L is only a supplied length scale.

The result covers exactly two profiles, one common launch per profile, one fixed finite segment, three area cells, one endpoint shape per model, complete curvature/null-source conservation, compatible rays and optical balance. It supplies no further waveform or parameter-family classification.

The exact equality of whole area histories strengthens the three-cell comparison. It does not authorize differentiating three measured samples to obtain the expansion derivative. With independently known shear and twist, and adequate registered area-derivative information, the optical equation can determine the null Ricci contraction. A zero-shear premise excludes model A away from launch; this pair does not invalidate estimators that explicitly retain those premises. The endpoint shape ratio separates the fixed pair without measuring an arbitrary shear history or establishing a general Ricci or rest-density inverse.

This observation limitation is not a violation of Einstein's equation or determinism: the two geometries do not share complete gravitational initial/boundary data. A native application still requires a justified state-to-geometry/source map, observable registration, dynamics and dimensional standards. A physical application still requires source generation, pencil preparation, finite-resolution readout and appropriate apparatus/energy accounting. The conserved local null tensor alone supplies neither a microscopic source realization nor compact isolation or a gravitational-wave energy ledger.

## Reviewed basis

DET Classical supplied the exact finite derivation and a distinct nonblind scientific review. The reviewer's prospective profile-design exposure was disclosed. That review checked the complete geometry/source, compatible null family and parallel screen, Jacobi solutions, area and focusing ledgers, shape discrimination and affine calibration. DET Quantum Relativity separately reviewed the restricted recipient use, including the known-shear estimator and physical/native boundaries.
