# Conditional rest and kinetic mass matching from a local boost relation

**Independently reviewed conditional theorem (2 November 2026):** under the exact supplied local canonical/boost assumptions, the required coefficient relation holds if and only if

\[
\{H_0,A\}=2c^2 I,
\qquad\text{equivalently}\qquad A=c^2H_0^{-1}.
\]

Strict positivity of H0 then gives positive, invertible A and

\[
M_{\rm kinetic}:=A^{-1}=H_0/c^2=:M_{\rm rest}.
\]

This is a conditional theorem about the supplied formal dynamical model. It does not derive the boost prescription, canonical carrier, physical scales or gravity from DET. It supplies a precise mass-consistency relationship for a later native model to reproduce. No global representation, empirical observation or new physical law is established.

## 1. Premises and meaning of the coefficient comparison

Let U be a momentum neighborhood of zero and take a common test domain of smooth, compactly supported functions U→C². Momentum P multiplies by the real scalar p; X=iℏ∂p, with supplied ℏ,c>0. The Hermitian matrix-valued multiplication operator is

\[
H(p)=H_0+\tfrac12 Ap^2+R(p),\quad H_0>0,\quad A=A^*,
\quad R(p)=O(p^4),\quad R'(p)=O(p^3).
\]

H and R are even and sufficiently smooth for these differential expressions. Matrix remainder bounds are local finite-dimensional norm statements. No relation between H0 and A is assumed. The symmetric boost expression at t=0 is supplied:

\[
K=(XH+HX)/(2c^2).
\]

Require [H,P]=0 and [K,P]=iℏH/c², together with [K,H]=iℏP through the coefficient linear in p. The latter means the coefficients of the resulting differential expressions agree at the specified order on arbitrary common test functions. This is not a uniform operator-norm estimate on all test functions, nor a claim about self-adjoint closures or exponentiated boosts. In the calculation below all derivatives of the test function cancel exactly from the commutators, leaving multiplication expressions whose matrix Taylor coefficients can be compared.

Physical preparation, readout and calibration remain separate from this formal coefficient comparison. No measured recoil ratio is identified with these masses by assumption.

## 2. Retain the derivative terms before taking coefficients

For every common test function ψ, the product rule gives

\[
K\psi=\frac{i\hbar}{c^2}\left(H\psi'+\tfrac12 H'\psi\right).
\]

Since p is scalar, [H,P]ψ=0 exactly. Also

\[
K(P\psi)=\frac{i\hbar}{c^2}
 \left(H\psi+pH\psi'+\tfrac p2H'\psi\right),
\qquad
P(K\psi)=\frac{i\hbar}{c^2}
 \left(pH\psi'+\tfrac p2H'\psi\right).
\]

Thus [K,P]ψ=iℏHψ/c² exactly on the local domain. This commutator adds no constraint on A.

For the remaining commutator, keep the matrix order:

\[
\begin{aligned}
K(H\psi)&=\frac{i\hbar}{c^2}
 \left(HH'\psi+H^2\psi'+\tfrac12H'H\psi\right),\\
H(K\psi)&=\frac{i\hbar}{c^2}
 \left(H^2\psi'+\tfrac12HH'\psi\right).
\end{aligned}
\]

The derivative terms H²ψ′ cancel. Neither HH′=H′H nor [H0,A]=0 has been used. Consequently

\[
[K,H]\psi=\frac{i\hbar}{2c^2}(HH'+H'H)\psi.
\]

Since H′=Ap+O(p³), the multiplication coefficient is

\[
HH'+H'H=(H_0A+AH_0)p+O(p^3).
\]

The exact leading defect is therefore

\[
([K,H]-i\hbar P)\psi
 =\frac{i\hbar}{2c^2}
 \left[(\{H_0,A\}-2c^2I)p+O(p^3)\right]\psi.
\]

It vanishes through the linear coefficient if and only if {H0,A}=2c²I. The remainder hypotheses ensure that R cannot change this coefficient. Equality at cubic or higher order is not required or inferred; those coefficients can depend on the remainder.

## 3. Solve without simultaneous diagonalization

Diagonalize only the initially supplied Hermitian H0. In its orthonormal eigenbasis, H0=diag(ε1,ε2), with ε1,ε2>0. Write the still arbitrary Hermitian A in that basis. Its entrywise equations are

\[
(\varepsilon_i+\varepsilon_j)A_{ij}=2c^2\delta_{ij}.
\]

Every sum εi+εj is strictly positive. Therefore

\[
A_{11}=c^2/\varepsilon_1,\qquad
A_{22}=c^2/\varepsilon_2,\qquad A_{12}=A_{21}=0.
\]

Conjugating back gives the unique A=c²H0⁻¹. In particular, [H0,A]=0 is a conclusion. If ε1=ε2=ε>0, the same equation gives A=(c²/ε)I; basis freedom in the degenerate eigenspace produces no extra coefficient freedom. Positivity and invertibility of A follow from its two positive eigenvalues, rather than being inserted.

Conversely, A=c²H0⁻¹ satisfies the anticommutator equation and hence all required commutator coefficients, for every admitted remainder R. This establishes necessity and sufficiency at the stated order. There is no obstruction inside the strict-positive H0 domain. No claim is made for singular or indefinite H0, or for a larger internal carrier.

In each rest-energy eigenbranch the local kinetic term is p²/(2m_i), where m_i=ε_i/c²>0. This justifies calling A⁻¹ the inertial coefficient mass in this stipulated low-momentum model, and establishes its equality with the stipulated rest-energy mass. It does not establish a physical preparation, stable particle species, a full dispersion relation at all p, or gravitational mass.

## 4. Dimensionless relationships, normalization and calibration

Take supplied positive reference scales E_star for energy and P_star for momentum. Define

\[
h=H_0/E_\star,\qquad a=A P_\star^2/E_\star,
\qquad \beta=cP_\star/E_\star,
\qquad M_\star=P_\star^2/E_\star.
\]

Here h,a,β are dimensionless and M_star has mass units. The same theorem becomes

\[
\{h,a\}=2\beta^2I,\qquad a=\beta^2h^{-1},
\qquad \mu:=M_{\rm kinetic}/M_\star=a^{-1}=h/\beta^2.
\]

The spectral mass ratio is m1/m2=ε1/ε2. An energy-level difference implies a mass difference (ε2−ε1)/c² within this model. Neither equality predicts the eigenvalues of H0 or an absolute physical mass.

For a change of reference scales E_star→λE_star, P_star→νP_star, with λ,ν>0 and physical operators and c held fixed,

\[
h\mapsto h/\lambda,\quad
 a\mapsto (\nu^2/\lambda)a,\quad
 \beta\mapsto(\nu/\lambda)\beta,\quad
 M_\star\mapsto(\nu^2/\lambda)M_\star,\quad
 \mu\mapsto(\lambda/\nu^2)\mu.
\]

Both dimensionless matrix equations transform consistently, M_star*μ remains the same mass operator and spectral mass ratios remain unchanged. Choosing β=1, when reference scales are chosen accordingly, is a normalization choice, not a derivation of a signal speed or mass scale. ℏ cancels from this coefficient relation because it is the same supplied nonzero constant in both commutators; its physical action calibration is not derived.

The model supplies the meanings of energy, momentum, c and ℏ. A native application still needs a dynamical identification of these quantities and the corresponding time/translation interpretation, together with preparation and observation access. Units can be chosen before empirical calibration, but changing units does not supply those physical correspondences.

## 5. Decomposition freedom is not a change of total rest energy

If one writes H0=m_base*c²I+H_internal, the paired bookkeeping change

\[
H_{\rm internal}\mapsto H_{\rm internal}+sI,
\qquad m_{\rm base}\mapsto m_{\rm base}-s/c^2
\]

leaves H0 fixed. It therefore leaves the derived A, total mass operator and boost expression unchanged. No independently physical meaning for m_base is gained merely from this decomposition. Setting the lowest internal energy to zero is one possible convention.

By contrast, change the total H(p) to H(p)+sI while keeping A,c fixed and rebuilding K using the same prescribed expression. The coefficient condition becomes

\[
\{H_0+sI,A\}=2c^2I+2sA.
\]

Since A is invertible, the original linear boost condition survives only for s=0. If instead K itself were held fixed, [K,P]=iℏ(H+sI)/c² already fails for nonzero s. Thus the usual global-phase irrelevance of an isolated additive energy constant cannot be imported unchanged into this joint energy-and-boost specification.

A shifted positive H0+sI could obey the same coefficient theorem with the different coefficient A_s=c²(H0+sI)⁻¹; that changes the kinetic response and the total mass operator. This is algebraic bookkeeping of the specified normalization issue, not an added physical scenario or executed model. A fixed excitation gap alone leaves the common energy offset undetermined; the gap by itself does not fix a base rest mass. An independently fixed kinetic coefficient would add information under these conditional premises.

## 6. Exact yield and boundary

The yield is one conditional coefficient theorem with a unit/decomposition ledger. It identifies the load-bearing extra structure: a positive rest-energy carrier, canonical momentum/position, and the specific boost algebra and generator. These premises jointly constrain the kinetic coefficient; record growth, a generic residual spectral gap or a scalar mass label alone does not supply the proof.

This result can serve as a conventional comparison target for the QR plan's mass-bearing dynamics obligation. It supplies no native law selection, quantum reconstruction, geometric limit, gravitational source law, equivalence of inertial and gravitational mass, experimental test or empirical validation. No mass shell was used as an input, and no all-orders mass shell or global boost representation was derived. Higher-order remainder coefficients and physical realization remain outside the question.

A native application still requires a justified energy/momentum/translation identification, an admitted state domain and a physical scale interpretation. This reference supplies a comparison criterion for that task; it supplies neither those premises nor a gravity prediction.

The proof is self-contained. Its assumptions are supplied rather than established by an external citation. The accepted source package is GDM030; independent scientific review and coordinator disposition preceded this publication assembly.
