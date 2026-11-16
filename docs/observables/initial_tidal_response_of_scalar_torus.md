# Initial tidal response of the scalar torus

**The initial tidal interpretation is generically anisotropic, including at the existing probe.** Uniform energy density and flat/isotropic intrinsic and extrinsic initial geometry do not imply isotropic spacetime tidal acceleration. For this exact accepted candidate, the proper-time trace-free Jacobi tensor is
$$
\boxed{\mathcal A^{\rm TF}_{ij}=\frac{8\pi G}{c^2}
\left(S_{ij}-\frac S3\gamma_{ij}\right).}
\tag{1}
$$
A dimensionless scalar of this tensor is computed below, with its exact isotropy locus. Electric Weyl curvature alone would give half of (1) for these initial data. This is a conditional initial-curvature result on any smooth Einstein development agreeing with the supplied initial source, not an existence or evolution theorem.

## 1. The one accepted source and initial slice

Reuse the accepted flat torus $\Sigma=\mathbb R^3/(L\mathbb Z)^3$, $L=8c\tau$, with $\gamma_{ij}=\delta_{ij}$, $K_{ij}=b\gamma_{ij}$, and expanding $b<0$. Write $\rho=\mathsf T(n,n)$, $J_i=-\mathsf T(n,e_i)=0$, $S_{ij}=\mathsf T(e_i,e_j)$, and $S=\gamma^{ij}S_{ij}$. The source is the accepted expectation tensor, with its full spatial stress, not a perfect-fluid replacement. Define $\lambda=8\pi G/c^4$. The accepted constraint result is
$$
\rho=\frac{3\pi A_*}{1024c^3\tau^4}>0,
\qquad b^2=\frac{\lambda\rho}{3},
\qquad \mathcal H_0=-cb>0,
\qquad \mathcal H_0^2=\frac{\lambda c^2\rho}{3}.
\tag{2}
$$
Here $\mathcal H_0$ denotes initial proper-volume expansion divided by three, not a Hamiltonian. All scales, torus geometry, observer registration, unshifted source convention and expectation-to-Einstein coupling remain supplied. No source mean or ground energy is removed. [Expanding flat-torus initial data](expanding_torus_initial_data_for_scalar_source.md)

The only matter profiles inserted are
$$
\alpha_1=\frac{10\pi x^1}{L}+\delta_1,\qquad
\alpha_2=\frac{14\pi x^2}{L},\qquad
\delta_1=\arccos\!\left[(\sqrt2-1)\sqrt{5/7}\right],
$$
$$
\frac{\rho_1}{\rho}=\frac5{12},\quad
\frac{\rho_2}{\rho}=\frac7{12},\quad
S_{ij}=\operatorname{diag}\left(
\rho_1+\rho_2\cos2\alpha_2,
\rho_2+\rho_1\cos2\alpha_1,
\rho_1\cos2\alpha_1+\rho_2\cos2\alpha_2\right).
\tag{3}
$$
They retain the accepted phase choice and existing probe $x_*=0$; no retuning or added mode is used. [Local scalar-source attachment](local_scalar_source_for_four_chain_field.md)

## 2. Curvature convention and proper-time acceleration

Use signature $(-+++)$, future unit normal $g(n,n)=-1$,
$$
[\nabla_\mu,\nabla_\nu]v^\alpha
=R^\alpha{}_{\beta\mu\nu}v^\beta,
\qquad R_{\beta\nu}=R^\alpha{}_{\beta\alpha\nu},
\qquad K_{ij}=-\tfrac12\mathcal L_n\gamma_{ij}.
\tag{4}
$$
The curvature, Ricci contraction, Gauss and Weyl conventions are those of Gourgoulhon v1, equations (2.13), (2.17), (2.18), (2.92)–(2.93); the trace-reversed Einstein equation is (4.2). Units are restored explicitly here. [Primary GR source](https://arxiv.org/pdf/gr-qc/0703035v1)

At any initial point, choose the freely falling timelike geodesic whose initial four-velocity is $U=cn$, and a parallel-propagated orthonormal spatial frame initially equal to the registered torus axes. Proper time $t_{\rm pr}$ is measured in seconds. For a Jacobi separation field with $[U,\xi]=0$, torsion freedom and the geodesic equation give
$$
\nabla_U^2\xi=R(U,\xi)U.
$$
In this frame the spatial components are
$$
\frac{d^2\xi^i}{dt_{\rm pr}^2}
=c^2R^i{}_{nnj}\xi^j
=-c^2R^i{}_{njn}\xi^j
=\mathcal A^i{}_j\xi^j.
\tag{5}
$$
Thus define the electric **Riemann** tensor $\mathcal E^R_{ij}=R_{injn}$ and $\mathcal A_{ij}=-c^2\mathcal E^R_{ij}$. Equation (5) is infinitesimal geodesic deviation, not a finite detector protocol. It fixes the minus sign and the conversion from inverse-length-squared curvature to inverse-time-squared acceleration coefficient.

## 3. Derive the full initial tensor before removing its trace

The spatial Gauss relation gives
$$
R_{kilj}={}^{(3)}R_{kilj}+K_{kl}K_{ij}-K_{kj}K_{il}.
$$
For the flat slice with $K=b\gamma$, its contraction is
$$
\gamma^{kl}R_{kilj}=2b^2\gamma_{ij}.
$$
The timelike term in the four-dimensional Ricci contraction has a minus sign, hence
$$
{}^{(4)}R_{ij}=2b^2\gamma_{ij}-\mathcal E^R_{ij}.
\tag{6}
$$
Equivalently this is the contracted Gauss identity
${}^{(4)}R_{ij}+\mathcal E^R_{ij}={}^{(3)}R_{ij}+KK_{ij}-K_{ik}K^k{}_j$.

The stress trace is $\mathsf T^\mu{}_\mu=-\rho+S$. With zero cosmological term, Einstein's equation yields
$$
{}^{(4)}R_{ij}=\lambda\left[S_{ij}+\frac{\rho-S}{2}\gamma_{ij}\right],
\quad R_{nn}=\frac\lambda2(\rho+S),
\quad {}^{(4)}R=\lambda(\rho-S).
\tag{7}
$$
Substituting (2) and (7) in (6), rather than guessing a stress factor, gives
$$
\boxed{\mathcal E^R_{ij}
=\lambda\left[\left(\frac\rho6+\frac S2\right)\gamma_{ij}-S_{ij}\right],}
\tag{8}
$$
$$
\boxed{\mathcal A_{ij}
=\lambda c^2\left[S_{ij}-\left(\frac\rho6+\frac S2\right)\gamma_{ij}\right].}
\tag{9}
$$
The trace checks against (7):
$$
\operatorname{tr}\mathcal E^R=R_{nn}=\frac\lambda2(\rho+S),
\qquad \operatorname{tr}\mathcal A=-\frac{\lambda c^2}{2}(\rho+S).
$$
Writing $\Pi_{ij}=S_{ij}-S\gamma_{ij}/3$, equation (9) is
$\mathcal A=\lambda c^2[\Pi-(\rho+S)\gamma/6]$, establishing (1). Only initial $\gamma,K,\mathsf T$ and the Einstein relation entered. There is no unknown time derivative of matter in this initial determination.

The distinction from Weyl is essential. Define $\mathcal E^W_{ij}=C_{injn}$. The four-dimensional Ricci/Weyl decomposition, evaluated on these indices, gives
$$
\mathcal E^R_{ij}=\mathcal E^W_{ij}-\tfrac12{}^{(4)}R_{ij}
+\left(\tfrac12R_{nn}+\tfrac16{}^{(4)}R\right)\gamma_{ij}.
\tag{10}
$$
Because $\mathcal E^W$ is spatially trace-free, taking the trace-free part of (10) and using (7)–(8) gives
$$
(\mathcal E^R)^{\rm TF}=-\lambda\Pi,
\qquad \boxed{\mathcal E^W=-\tfrac\lambda2\Pi.}
\tag{11}
$$
Consequently $-c^2\mathcal E^W$ contributes only half of $\mathcal A^{\rm TF}$ here; the other half is the trace-free Ricci contribution. Weyl electric curvature and trace-free Riemann electric curvature are not interchangeable in this matter-filled slice. This factor is specific to the stated flat/isotropic initial data.

## 4. Fixed profiles and the one normalized invariant

Define the dimensionless profile values
$$
r_1=\frac{\rho_1}{\rho}(1-\cos2\alpha_1)=\frac56\sin^2\alpha_1,
\qquad
r_2=\frac{\rho_2}{\rho}(1-\cos2\alpha_2)=\frac76\sin^2\alpha_2.
\tag{12}
$$
Then (3) can be written
$$
S_{ij}=\rho\left[(1-r_1-r_2)\delta_{ij}
+\operatorname{diag}(r_1,r_2,0)\right],
\qquad S=\rho[3-2(r_1+r_2)].
$$
Insertion into (9), with $\mathcal H_0^2=\lambda c^2\rho/3$, produces the full and trace-free matrices
$$
\boxed{\frac{\mathcal A}{\mathcal H_0^2}
=\operatorname{diag}(3r_1-2,\,3r_2-2,\,-2),}
\tag{13}
$$
$$
\boxed{\frac{\mathcal A^{\rm TF}}{\mathcal H_0^2}
=\operatorname{diag}(2r_1-r_2,\,2r_2-r_1,\,-r_1-r_2).}
\tag{14}
$$
Thus the requested scalar, with spatial indices contracted by $\gamma$, is
$$
\begin{aligned}
\mathcal I(x)&:=\frac{\operatorname{tr}[(\mathcal A^{\rm TF})^2]}{\mathcal H_0^4}
=\frac{9\Pi_{ij}\Pi^{ij}}{\rho^2}\\
&=(2r_1-r_2)^2+(2r_2-r_1)^2+(r_1+r_2)^2\\
&=\boxed{6(r_1^2+r_2^2-r_1r_2)}\\
&=\boxed{\frac{25\sin^4\alpha_1+49\sin^4\alpha_2
-35\sin^2\alpha_1\sin^2\alpha_2}{6}}.
\end{aligned}
\tag{15}
$$
No second source or coefficient family is compared. This is one scalar field on the existing initial torus. It is invariant under rotations of the observer's spatial orthonormal frame, not an observer-independent four-dimensional curvature invariant.

Since $r_1^2+r_2^2-r_1r_2=(r_1-r_2/2)^2+3r_2^2/4$,
$$
\mathcal I=0\quad\Longleftrightarrow\quad
\alpha_1\in\pi\mathbb Z\ \text{and}\ \alpha_2\in\pi\mathbb Z.
\tag{16}
$$
This is exactly the pointwise isotropy locus of $\mathcal A$: the corresponding periodic lines parallel to $e_3$. There $\mathcal A=-2\mathcal H_0^2\mathrm{Id}$, so isotropy does not mean zero tides. These lines contain no open region of the slice. Elsewhere the tensor is anisotropic. Spatial variation is explicit on the existing section $x^2=0$, where $\mathcal I=(25/6)\sin^4\alpha_1$.

At the already registered probe $x_*=0$, $\sin^2\alpha_2=0$ and
$$
p_*:=\sin^2\delta_1=1-\frac57(\sqrt2-1)^2
=\frac{10\sqrt2-8}{7}>0,
$$
so the same invariant has the fixed value
$$
\boxed{\mathcal I(x_*)=\frac{25}{6}
\left(\frac{10\sqrt2-8}{7}\right)^2>0.}
\tag{17}
$$
This rules out isotropic initial Jacobi acceleration at that probe, within the conditional model.

## 5. What the normalized result fixes

The dimensional quantities satisfy
$$
[\mathcal E^R]=[\mathcal E^W]=\mathrm{length}^{-2},\qquad
[\mathcal A]=\mathrm{time}^{-2},\qquad [\mathcal I]=1.
$$
The factor $G$ and common source amplitude $\rho$ cancel in (15); field normalization $\kappa$ and sample normalization had already cancelled from the accepted stress. At a fixed dimensionless position $x/L$, only the supplied mode ratio, axes and phases remain in (15). The dimensional length $L=8c\tau$ is still required to locate those phases at a physical point. Normalization has not derived geometry or eliminated its registration.

The absolute rate scale remains
$$
\mathcal H_0^2=\frac{\pi^2}{128}\frac{GA_*}{c^5\tau^4}.
\tag{18}
$$
Neither (15) nor its probe value separates or calibrates $G,c,A_*,\tau$, a native clock, physical length or energy. If registered, the normalized scalar fixes the squared magnitude of trace-free stress relative to $\rho$ for this observer. A nonzero value excludes isotropic tides at that point; the scalar alone does not reconstruct the eigenframe, both phases, or a unique spatial position. At the fixed probe (17) is a conditional consistency target, not an actual observation or detector design.

## 6. Scope and distinct result

This calculation is conditional on **any smooth local Einstein development** that agrees with all the accepted initial components. It fixes necessary initial curvature if such a development exists. It neither proves that development exists nor assumes a specific matter continuation. The separate four-scalar continuation result is not an input to this calculation and is not needed to obtain (6)–(17). No future time interval, homogeneous future metric, preservation of the old four samples or nonlinear detector forecast is claimed.

The initial slice remains intrinsically flat with spatially constant isotropic extrinsic curvature and uniform density. Its normal-observer spacetime tidal invariant nevertheless varies across the slice. The general isotropic/homogeneous tidal interpretation is therefore rejected; the exact pointwise exception (16) is retained. No conclusion about spatial geometry emerging from records follows.

The earlier [equal-energy stress quadrupole](stress_quadrupole_at_equal_energy.md) and [retarded stress](retarded_stress_at_fixed_density.md) results already establish stress-sensitive tidal channels for different prescribed weak-field compact sources. This result does not reannounce that principle as new. Its distinct yield is the full nonlinear initial Jacobi tensor and expansion-normalized invariant of the already accepted compact torus, without an exterior or weak-field expansion. The [two-epoch Ricci-scalar result](rest_density_from_two_expansion_epoch_curvatures.md) assumes a homogeneous isotropic transported gas and addresses rest-density inference; those assumptions and inferences are not imported here.

All native history weights, attachment availability and the excluded saturated-prefix boundary remain intact. The supported chain weights stay $779/1320$ and $574/1320$, with four fair suffix-mark pairs at one quarter of each row; other histories keep their original weights without this attachment. The excluded saturated prefix is not restored. There is no field feedback, native law, gravity calibration, physical preparation/readout, apparatus closure, empirical execution or retired kappa-gravity claim.

**Result:** (8)–(17) give the conditional initial-curvature result. General isotropic tides are excluded for this source and, specifically, at the existing probe. The calculation adds no new source cases or modes, future evolution, detector protocol or experiment.

## Reviewed basis

DET Quantum Relativity supplied the finite initial-curvature derivation. DET Energy Research independently checked the curvature conventions, full Riemann/Jacobi and Weyl distinction, fixed-profile matrices and invariant, exact isotropy locus, original-probe value, observer registration and dimensional limits. The accepted proof remains conditional on a compatible smooth Einstein development and uses no separate continuation theorem.
