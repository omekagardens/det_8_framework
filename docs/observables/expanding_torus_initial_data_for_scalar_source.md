# Expanding flat-torus initial data for the scalar source

The positive scalar expectation source admits the specified flat three-torus initial slice with constant isotropic nonzero extrinsic curvature. The constraints determine the magnitude of its initial proper-volume rate. The expanding sign is used for the attachment. This is conditional initial-data compatibility with the supplied Einstein constraints.

## Initial source and geometric inputs

Take $\Sigma=\mathbb R^3/(L\mathbb Z)^3$, $L=8c\tau$, with the inherited flat spatial metric $\gamma_{ij}=\delta_{ij}$ and $V_0=L^3$. The supplied constants are $G,c,\tau,A_*>0$, with $A_*$ the action reference and $\tau$ the duration per tick in the reference model. Use signature $(-+++)$, future unit normal $n$, and the kinetic stress with the previously accepted symmetric ordering. Keep the accepted scalar field and its initial normal derivative as initial operators on the same two-mode product ground state. Identify the reference $\dot\Psi/c$ at the initial slice with the new $\nabla_n\Psi$ there. This is a supplied correspondence of initial data.

The mode angles are $\alpha_j=k_j\cdot x+\delta_j$ with $k_1=10\pi e_1/L$, $k_2=14\pi e_2/L$, and $\omega_1\tau=5\pi/4,\ \omega_2\tau=7\pi/4$. Let $d_j=k_j/|k_j|$, $E_j=A_*\omega_j/2$, and $\rho_j=E_j/V_0$. In mode $j$, the two derivative-square contributions to the normal energy expectation are $\rho_j\cos^2\alpha_j$ and $\rho_j\sin^2\alpha_j$. These follow from the accepted mode normalization $B_j^2=2A_*c^2/(\kappa V_0\omega_j)$ and the two quadrature variances $1/2$, where $\kappa$ is the supplied scalar kinetic normalization. Cross-mode ground contractions and the symmetrized same-mode position/momentum contraction vanish. The latter gives zero normal flux.

Write $\mathsf T=\langle T\rangle$ for the initial classical source specified to the Einstein constraints. The contractions give
$$
 \rho_E=\mathsf T(n,n)=\rho_1+\rho_2
   =\frac{E_0}{V_0}=\frac{3\pi A_*}{1024 c^3\tau^4},\qquad
 E_0=\frac{3\pi A_*}{2\tau},\qquad J_i=-\mathsf T(n,e_i)=0.
$$
The full spatial expectation is
$$
 S_{ab}=\sum_{j=1}^2\rho_j\left[d_j^a d_j^b+
     (\delta^{ab}-d_j^a d_j^b)\cos(2\alpha_j)\right].
$$
For example $S_{11}-S_{33}=\rho_1(1-\cos 2\alpha_1)$ is nonzero at some points and $S_{22}$ varies along $e_1$. The stress retains its periodic spatial structure. Its divergence in the reference slice vanishes since each varying transverse component depends on its own mode's longitudinal coordinate. The zero flux and uniform energy here are ground-state expectation statements. The operator tensor and its expectation are distinct, including the fact that a zero field mean still has nonzero quadratic moments. The unshifted action Hamiltonian supplies $E_0$. An identity energy offset or removal of the ground energy would change the source convention, so the accepted convention is used throughout. [The local scalar source and its stress](local_scalar_source_for_four_chain_field.md)

## Pointwise constraints and sign

Supply the Einstein constraint equations at zero cosmological term, with $\mathsf T$ as their initial source. This expectation-to-gravity coupling is an added model premise. Adopt $K_{ij}=-\mathcal L_n\gamma_{ij}/2$, where the normal derivative has inverse-length units. In the normal momentum convention above the equations with units restored are
$$
 {}^{(3)}\!{\cal R}+K^2-K_{ij}K^{ij}=\frac{16\pi G}{c^4}\rho_E,\qquad
 D_j K^j{}_i-D_iK=\frac{8\pi G}{c^4}J_i .
$$
Here $D$ is the spatial covariant derivative and $K$ the trace. The full spatial stress is absent from these two projections. [Gourgoulhon, gr-qc/0703035v1, §4, Eqs. (4.63)–(4.66) and (4.93)–(4.94)](https://arxiv.org/pdf/gr-qc/0703035v1)

For $K_{ij}=b\gamma_{ij}$ with constant $b$, all three momentum equations hold pointwise because $D\gamma=0$, $K=3b$ is constant and $J_i=0$. The flat metric gives ${}^{(3)}\!{\cal R}=0$. The Hamiltonian left side is $9b^2-3b^2=6b^2$. Thus the allowed values in this ansatz are
$$
 b=\pm\sqrt{\frac{8\pi G\rho_E}{3c^4}}.
$$
Both signs solve the same initial constraint equation. Take $b<0$ for the expanding representative in this convention. Positivity of $\rho_E$ excludes zero $b$ in this fixed flat ansatz. No constant part of the source is removed.

## Initial proper-volume rate and scale

Use $x^0=ct$, unit lapse and zero shift on the initial slice to register proper time there. The normal metric derivative gives $\partial_t\gamma_{ij}|_0=-2cK_{ij}$, hence
$$
 \frac{\dot V_0}{V_0}=-cK=-3cb,\qquad
 {\cal H}_0:=\frac{\dot V_0}{3V_0}=-cb .
$$
This follows by differentiating the metric volume density and integrating over the torus. It is an instantaneous rate of the specified normal slice, independent of coordinates on that slice. In particular
$$
 {\cal H}_0^2=\frac{8\pi G\rho_E}{3c^2}
  =\frac{8\pi G E_0}{3c^2 V_0},\qquad
 ({\cal H}_0\tau)^2=\frac{\pi^2}{128}\,\frac{G A_*}{c^5\tau^2}.
$$
Thus $b$ has inverse-length units, ${\cal H}_0$ inverse-time units, and $G A_* /(c^5\tau^2)$ is dimensionless. For the expanding representative $\tau\dot V_0/V_0=(3\pi/(8\sqrt2))\sqrt{G A_* /(c^5\tau^2)}$. The positive branch rate follows from the independently supplied scales and sign choice. The scalar field-unit normalization cancels in $\rho_E$ through $B_j$. Neither that cancellation nor the initial rate determines the physical values of $G,c,\tau,A_*$ or a native clock or mass standard. The relation $L=8c\tau$ is inherited mode compatibility.

## Relation to the static obstruction and future scope

For a static weak-field perturbation on a flat periodic background, the Poisson equation for the time-time trace-reversed metric has a spatial Laplacian with zero integral and a nonzero mean source. The earlier obstruction remains valid in that model. Here flat intrinsic curvature accompanies $K_{ij}\ne0$. With fixed positive $\rho_E$ and the other physical scales held fixed, $b$ scales as $\sqrt G$ and its quadratic constraint term is of order $G$. In an ordinary expansion with metric and extrinsic curvature perturbations of order $G$ about a flat static slice, the extrinsic term is of order $G^2$. Even allowing a smooth periodic first-order intrinsic metric correction $h_{ij}$, the first variation of ${}^{(3)}\!{\cal R}$ at the flat metric is the spatial divergence $\partial_i\partial_j h_{ij}-\nabla^2\operatorname{tr}h$, with zero spatial integral. That expansion cannot supply the positive mean at order $G$. The specified attachment uses the full quadratic extrinsic-curvature term. The obstruction concerns that perturbation class, not unrestricted nonlinear initial data.

The spatial Einstein equations depend on $S_{ij}$, including its inhomogeneous tracefree part. Flat $\gamma$ and isotropic $K$ on one slice therefore supply no homogeneous future-spacetime ansatz. The missing evolution premise is a geometry-dependent scalar state and stress prescription on the evolving metric, with $\nabla_\mu\mathsf T^{\mu\nu}=0$ in that metric, coupled to the spatial Einstein evolution equations. The accepted flat-background operator conservation law applies to its reference wave equation. The initial constraints alone provide no construction or existence or uniqueness result for such a coupled model. They also provide no continuation of the original generator, mode spectrum, or four probe samples on the new geometry. The accepted four-tick covariance match remains a reference-background calculation. A physical preparation, clock transfer, readout and reset would need their own registration.

The conditional scalar and gravitational attachments concern the same supported $a<b<x<y$ branch. Its original structural weights are $779/1320$ and $574/1320$, with four fair mark assignments at one quarter each. All other histories retain their original weights, with this attachment unavailable there. The initial constraint result supplies no change to the native law. This specific initial slice is a conditional attachment of the [scalar source](local_scalar_source_for_four_chain_field.md).

## Reviewed basis

DET Relational State Research constructed the initial-data attachment; DET Quantum Relativity independently checked the source projections, four constraints, signs, units and evolution limits. The scalar-source proof is reused. No empirical claim or native gravitational law follows.
