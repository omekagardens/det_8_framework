# Smooth Newtonian source reduction and the effective branch-operator boundary

**Accepted conditional mathematics.** This fixed smooth-source result passed its first distinct scientific review and coordinator admission. The geometry, gravitational coupling, mass and length scales, imposed sources and later quantum operator rule are supplied assumptions. Empirical status is **NOT TESTED**.

For the exact smooth bump, define the dimensionless positive profile integral \(\mathcal I_b\) below. With \(k=Gm^2/d\), the four complete minimized energies are
\[
 (U_{00},U_{01},U_{10},U_{11})
 =-k\left(4\mathcal I_b+\frac13,\;
           4\mathcal I_b+\frac14,\;
           4\mathcal I_b+\frac12,\;
           4\mathcal I_b+\frac13\right).                 \tag{1}
\]
Both finite self-energies are retained in every entry. Under the separately stipulated diagonal quantum assignment, the full operator is
\[
 H_{\rm red}=-k\left[4\mathcal I_b I_4+
                 \operatorname{diag}\left(\frac13,\frac14,\frac12,\frac13\right)\right]. \tag{2}
\]
Its alternating energy difference is
\[
 D=U_{00}-U_{01}-U_{10}+U_{11}=\frac{Gm^2}{12d}>0.       \tag{3}
\]
It therefore has no representation \(A\otimes I+I\otimes B+\gamma I\), even when A,B range over all Hermitian qubit operators. Static reduction and this added operator assignment do not furnish the mediator/history/instrument premises of the accepted four-round theorem. No quantum evolution or entanglement is calculated here.

The conclusion concerns one fixed conditional model. Euclidean geometry, G,m,d, prescribed sources and quantum promotion are supplied, not DET-derived or physically calibrated.

## 1. Exact inputs and regularity

Retain supplied Euclidean \(\mathbb R^3\), \(G,m,d>0\), \(\eta=d/4\), and \(e_1=(1,0,0)\). Introduce only notation for the already fixed bump:
\[
 b(t)=\exp[-1/(1-t^2)]\quad(0\le t<1),\qquad
 Z_b=4\pi\int_0^1t^2 b(t)\,dt.
\]
The integrand is positive in the interior and bounded, so \(0<Z_b<\infty\). The specified normalization constant is \(C_\eta=(\eta^3 Z_b)^{-1}\), and
\[
 f_\eta(x)=\frac{b(|x|/\eta)}{\eta^3Z_b}\quad(|x|<\eta),
 \qquad f_\eta(x)=0\quad(|x|\ge\eta).
\]
It is nonnegative and integrates to one. The exponential and all its derivatives vanish at the support boundary; near the origin it is a smooth function of \(|x|^2\). Thus \(f_\eta\in C_c^\infty(\mathbb R^3)\).

For exactly \(a,b\in\{0,1\}\), let
\[
 x_A(a)=ad e_1,\qquad x_B(b)=(3+b)d e_1,
\]
\[
 f_A(x)=f_\eta(x-x_A(a)),\quad f_B(x)=f_\eta(x-x_B(b)),
 \qquad \rho_{ab}=m(f_A+f_B).
\]
Each \(\rho_{ab}\) is smooth and compactly supported, belongs to \(L^p\) for all \(1\le p\le\infty\), and has total mass \(2m\). The four centre separations are
\[
 R_{00}=3d,\quad R_{01}=4d,\quad R_{10}=2d,\quad R_{11}=3d.
\]
All exceed \(2\eta=d/2\), so the two supports in each configuration are disjoint. No source is replaced by a point distribution and no zero-radius limit is taken.

The real potential space is the declared gradient-norm completion \(\dot H^1(\mathbb R^3)\), with its canonical \(L^6\) representative. For compactly supported smooth u, the Sobolev inequality
\(\|u\|_6\le C_S\|\nabla u\|_2\) holds; an elementary sufficient constant and proof are supplied in Appendix A. It extends to this completion. Hence
\[
 \left|\int\rho_{ab}\Phi\right|
 \le \|\rho_{ab}\|_{6/5}\|\Phi\|_6
 \le C_S\|\rho_{ab}\|_{6/5}\|\nabla\Phi\|_2.           \tag{4}
\]
The functional
\[
 \mathcal E_{ab}[\Phi]
 =\frac{1}{8\pi G}\|\nabla\Phi\|_2^2+\int\rho_{ab}\Phi \tag{5}
\]
is therefore well-defined on the whole space. Its positive quadratic part and (4) make its infimum finite. Constants other than zero are not canonical \(L^6\) representatives; no free potential offset or pointwise boundary condition on arbitrary domain elements is inserted.

## 2. Constructing the smooth minimizer

For a unit bump at the origin write
\[
 w_\eta(x)=\int\frac{f_\eta(y)}{|x-y|}\,dy,
 \qquad M_\eta(r)=4\pi\int_0^r s^2 f_\eta(s)\,ds\quad(0\le r\le\eta).
\]
Here \(f_\eta(s)\) denotes its radial value. The angular integral needed to evaluate w is derived directly. For \(r,s>0\),
\[
 \int_{S^2}\frac{d\Omega}{|r e_1-s n|}
 =2\pi\int_{-1}^{1}\frac{dt}{\sqrt{r^2+s^2-2rst}}
 =\frac{2\pi[(r+s)-|r-s|]}{rs}
 =\frac{4\pi}{\max(r,s)}.                             \tag{6}
\]
The limits at zero and the integrable coincident-radius angular singularity agree with this expression. It follows that
\[
 w_\eta(r)=
 \begin{cases}
 \displaystyle\frac{M_\eta(r)}r+4\pi\int_r^\eta s f_\eta(s)\,ds,&0<r<\eta,\\
 1/r,&r\ge\eta,
 \end{cases}                                         \tag{7}
\]
with finite value \(w_\eta(0)=4\pi\int_0^\eta s f_\eta(s)\,ds\).

Differentiating the interior expression gives
\[
 w_\eta'(r)=-\frac{M_\eta(r)}{r^2},\qquad
 (r^2w_\eta')'=-4\pi r^2 f_\eta(r).                   \tag{8}
\]
Since \(M_\eta(r)=O(r^3)\) at zero, the derivative is \(O(r)\) there. Smooth radial regularity at zero and the flat bump boundary make \(w_\eta\) smooth across zero and \(r=\eta\). Equations (7)–(8) yield everywhere, also distributionally,
\[
 \Delta w_\eta=-4\pi f_\eta.                          \tag{9}
\]
Thus a candidate for each branch is the explicitly constructed smooth function
\[
 \Phi_{ab}(x)=-Gm\,[w_\eta(x-x_A(a))+w_\eta(x-x_B(b))]. \tag{10}
\]
It satisfies
\[
 \Delta\Phi_{ab}=4\pi G\rho_{ab}.                     \tag{11}
\]
The sign and coefficient agree with varying (5), rather than being stipulated as an evaluated solution.

The function is bounded on bounded sets. At large \(r=|x|\), (7) gives
\[
 \Phi_{ab}(x)=-\frac{2Gm}{r}+O(r^{-2}),\qquad
 \nabla\Phi_{ab}(x)=O(r^{-2}).                        \tag{12}
\]
Consequently \(\Phi_{ab}\in L^6\) and \(\nabla\Phi_{ab}\in L^2\). To prove membership in the specified completion, take smooth cutoffs \(\chi_R=1\) on the radius-R ball, zero outside radius 2R, with \(|\nabla\chi_R|\le C/R\). Then \(\chi_R\Phi_{ab}\in C_c^\infty\), and
\[
 \|\nabla(\chi_R\Phi_{ab}-\Phi_{ab})\|_2
 \le \|(1-\chi_R)\nabla\Phi_{ab}\|_2
      +\|\Phi_{ab}\nabla\chi_R\|_2\longrightarrow0.   \tag{13}
\]
The first term tends to zero by the finite gradient norm. The square of the second is bounded by \(C R^{-2}\int_{R<|x|<2R}|\Phi_{ab}|^2=O(R^{-1})\). The \(L^6\) tails vanish as well, identifying the same canonical representative. These are properties of the constructed minimizer, not an extra restriction on all trial potentials.

## 3. Weak equation, global minimization and boundary release

For compactly supported smooth v, (11) gives
\[
 \int\nabla\Phi_{ab}\cdot\nabla v=-4\pi G\int\rho_{ab}v. \tag{14}
\]
Both sides are continuous in the gradient norm by (4), so (14) extends to every \(v\in\dot H^1\). Expanding (5) now yields the exact identity
\[
 \mathcal E_{ab}[\Phi_{ab}+v]
 =\mathcal E_{ab}[\Phi_{ab}]+\frac1{8\pi G}\|\nabla v\|_2^2. \tag{15}
\]
It proves existence, attainment and uniqueness of the minimizer on the full declared domain. Equality implies zero gradient norm, hence the zero element of the completion and the zero \(L^6\) representative. Conversely any stationary point satisfies (14), so no other stationary solution in this domain is missed.

Taking \(v=\Phi_{ab}\) in the extended weak equation is legitimate and gives
\[
 \|\nabla\Phi_{ab}\|_2^2=-4\pi G\int\rho_{ab}\Phi_{ab},
\]
\[
 U_{ab}=\mathcal E_{ab}[\Phi_{ab}]
       =\frac12\int\rho_{ab}\Phi_{ab}
       =-\frac1{8\pi G}\|\nabla\Phi_{ab}\|_2^2.        \tag{16}
\]
This is a finite attained energy, not an omitted boundary convention.

For an explicit surface check on a large sphere, the usual smooth integration-by-parts identity has surface term
\(\int_{|x|=R}\Phi_{ab}\partial_n\Phi_{ab}\,dS\).
Equation (12) bounds it by \(O(R^{-1})\), so it vanishes. The same estimate applies to each translated component's self surface term and mixed component surface term: each potential is \(O(R^{-1})\) and each normal derivative \(O(R^{-2})\). Thus there is no hidden finite surface contribution to (16) or its self/cross splitting. The weak-domain argument independently establishes the identity without assigning boundary values to arbitrary trials.

## 4. Full finite self and cross energies

Define the exact unit-profile self integral
\[
 J_\eta=\iint\frac{f_\eta(x)f_\eta(y)}{|x-y|}\,dx\,dy. \tag{17}
\]
It is positive and finite. On the bounded support the kernel \(|x-y|^{-1}\) is locally integrable in three dimensions and the bump is bounded. Translation leaves this integral unchanged.

A one-dimensional expression makes its dependence on the fixed smooth profile explicit. Set
\[
 \mu(t)=\frac{4\pi}{Z_b}\int_0^t s^2 b(s)\,ds\quad(0\le t\le1),
 \qquad
 \mathcal I_b=1+\int_0^1\frac{\mu(t)^2}{t^2}\,dt.       \tag{18}
\]
Here \(\mu(0)=0,\mu(1)=1\), and \(\mu(t)=O(t^3)\) near zero, so the integral is finite and \(\mathcal I_b>1\). This is an exact convergent integral for the registered bump, not a fitted or numerical constant.

To obtain (18) from (17), use (7) and \(M_\eta'(r)=4\pi r^2 f_\eta(r)\). Interchanging the finite nonnegative radial integrals gives
\[
 J_\eta=2\int_0^\eta\frac{M_\eta(r)M_\eta'(r)}r\,dr.
\]
Integration by parts in the identity
\((M_\eta^2/r)'=2M_\eta M_\eta'/r-M_\eta^2/r^2\)
has zero lower endpoint because \(M_\eta(r)=O(r^3)\). Its upper endpoint is \(1/\eta\). Therefore
\[
 J_\eta=\frac1\eta+\int_0^\eta\frac{M_\eta(r)^2}{r^2}\,dr
       =\frac{\mathcal I_b}{\eta}.                    \tag{19}
\]
Each body's full self energy in (16) is \(-Gm^2J_\eta/2\); both together contribute \(-Gm^2J_\eta\). They remain in every branch.

For the cross integral
\[
 K_{ab}=\iint\frac{f_\eta(x-x_A(a))f_\eta(y-x_B(b))}{|x-y|}\,dx\,dy,
\]
every x in the A support is outside the B support, since \(R_{ab}>2\eta\). The first angular integration (6)–(7) therefore gives
\[
 K_{ab}=\int\frac{f_\eta(x-x_A(a))}{|x-x_B(b)|}\,dx
        =w_\eta(x_B(b)-x_A(a))=\frac1{R_{ab}}.         \tag{20}
\]
The second equality uses radial symmetry and the same derived exterior formula. This is an exact result for the finite smooth disjoint sources. No point-source energy, asymptotic separation expansion or zero-radius approximation is adopted.

Expanding (16) with both sources gives the full accounting
\[
 U_{ab}=-\frac{Gm^2}{2}\,[J_\eta+J_\eta+2K_{ab}]
       =-Gm^2\frac{\mathcal I_b}{\eta}-\frac{Gm^2}{R_{ab}}. \tag{21}
\]
Substitution of \(\eta=d/4\) and the four exact separations proves (1). In particular, cancellation of common self terms in a later diagnostic is not a subtraction from the original energy functional.

## 5. Added operator assignment and all-Hermitian locality test

The classical minimization does not introduce a Hilbert space or coherent dynamics. Now, and only as the separately supplied model rule, use \(\mathcal K_A=\mathcal K_B=\mathbb C^2\), basis 00,01,10,11, and
\(H_{\rm red}=\sum U_{ab}|ab\rangle\langle ab|\).
Equation (21) then gives (2), a bounded self-adjoint 4x4 operator on its entire finite carrier. No infinite operator-domain issue is imported from the potential space.

Suppose it has a local-additive representation with arbitrary Hermitian A,B and real \(\gamma\). For either b,
\[
 \langle0b|H_{\rm red}|1b\rangle=A_{01}=0,
\]
and for either a,
\[
 \langle a0|H_{\rm red}|a1\rangle=B_{01}=0.
\]
The other off-diagonal entries vanish by Hermiticity. Thus A and B must be diagonal; their diagonal entries would have to satisfy
\(U_{ab}=A_{aa}+B_{bb}+\gamma\). The alternating sum is necessarily zero.

This condition is also sufficient for a diagonal four-entry operator: if D=0, take
\[
 A=\operatorname{diag}(U_{00},U_{10}),\qquad
 B=\operatorname{diag}(0,U_{01}-U_{00}),\qquad\gamma=0.
\]
The last entry is correct precisely when D=0. This proves the criterion over the complete Hermitian class, rather than assuming diagonal local terms.

Using the energies already derived from the smooth minimizers, the self term cancels with coefficient \(1-1-1+1=0\), while
\[
 D=\frac{Gm^2}{d}\left(-\frac13+\frac14+\frac12-\frac13\right)
  =\frac{Gm^2}{12d}>0.
\]
The local-additive representation is therefore excluded. This is an effective two-factor operator statement only, not an entanglement or channel-class calculation.

## 6. What transfers to the mediation question

| Earlier mediation ingredient | What this reduced model supplies |
|---|---|
| Two specified quantum factors | C2 tensor C2 branch-label space, by the added assignment only; no physical subsystem identification is derived. |
| Initial product preparation | No quantum state or preparation is part of this static question. |
| A local probe–mediator interaction or a classical recorded alternative | Neither a mediator factor nor an interaction schedule is specified. |
| Complete classical history register and local CP instruments | None are supplied by minimizing the scalar functional. |
| No direct AB operation in the declared comparator | The assigned reduced Hamiltonian is not a sum of AB-local terms. This does not determine whether an unreduced local-mediator completion exists or whether its channels belong to the earlier class. |
| A final unconditional state/record diagnostic | Only energies and an assigned operator are computed; no evolution or observation law is added. |
| Physical gravitational correspondence | G, sources, geometry, coupling and operator promotion remain supplied mathematical assumptions. |

Consequently static elimination alone does not instantiate the hypotheses needed to transfer the accepted local-record mediation exclusion. The implication from this reduction alone to such a physical exclusion is rejected. There is no counterexample to the earlier theorem: its declared operational process is not constructed here.

Nor does a joint effective operator prove fundamental direct action, rule out every local-mediator completion, or decide whether physical gravitational degrees of freedom are classical or quantum. Eliminating an explicit variable is not an ontological conclusion. In particular this report does not say that a classical field entangles matter; the quantum operator was separately assigned and was not evolved.

The source distributions are imposed configurations. No force balance, material support, confinement, recoil, autonomous motion or stability follows. There is no causal radiation model, gauge-invariant physical factorization, nonlinear GR completion, controlled weak-field error, physical apparatus or measurement budget. These missing premises are not silently repaired by the finite energy calculation.

If conventional dimensions are assigned, \(J_\eta\) has inverse-length units and \(Gm^2/d\) has energy units. That is consistency of the supplied convention, not a native mass, action, clock or unit derivation. No result from another active research lane is a premise of this calculation.

## 7. Review status and process qualifications

This fixed result passed its first distinct scientific review by DET Relational State Research and coordinator admission on 26 November 2026, without a substantive correction or unresolved admitted mathematical obligation. The review covered the full potential domain, constructive minimizer, boundary terms, retained self and cross energies, arbitrary-Hermitian locality criterion and operational-interface limits. The present document assembles that accepted result; it introduces no additional profile, centre, parameter choice or scientific claim. Empirical status is **NOT TESTED**.

Scientific acceptance does not erase process departures. During earlier candidate selection, a point-source mixed-energy diagnostic was calculated before selected-proof authorization and anticipated the coefficient appearing in (3). That calculation remains an unrepaired authorization-order departure; it was not a premise of the smooth-source derivation. Agreement with it is neither retrospective authorization nor a blind prediction. An earlier failed capacity-reading attempt was followed by four dependent discovery reads before inspection and stopping; that material guard-inspection error also remains unrepaired. Later eligible work and independent review do not certify clean prospectivity or all-algebra-after-activation. Nonblind exposure and recorded source-read/order limitations remain attached to the accepted result.

The exact author report, first scientific review and coordinator disposition are retained in the coordinator’s assembly provenance, with their cryptographic digests. Those digests establish documentary identity, not scientific truth. Mathematical reasoning was performed on paper; file and hash operations were custody work, not numerical experiments. The publication assembly has a separate fidelity-review boundary and does not repeat the scientific review or authorize a quantum-evolution, entanglement, source-profile or centre variant.

## Appendix A. Analytic inequality used for the declared completion

For real compactly supported smooth v, the fundamental theorem of calculus in each coordinate gives
\(|v(x)|\le F_i(x_{\widehat i})\), where \(F_i\) is the integral of \(|\partial_i v|\) along the i-th coordinate. Hence
\[
 |v(x)|^{3/2}\le[F_1(x_2,x_3)F_2(x_1,x_3)F_3(x_1,x_2)]^{1/2}.
\]
Integrate first in x1 and apply Cauchy–Schwarz; the inner integral is bounded by
\([\int F_2(x_1,x_3)dx_1\int F_3(x_1,x_2)dx_1]^{1/2}\).
A second Cauchy–Schwarz in (x2,x3) and Fubini then give
\[
 \int|v|^{3/2}\le
 \prod_{i=1}^3\|\partial_i v\|_1^{1/2},\qquad
 \|v\|_{3/2}\le\prod_{i=1}^3\|\partial_i v\|_1^{1/3}.
\]
Apply this to \(v=u^4\). Hölder gives
\(\|\partial_i(u^4)\|_1\le4\|u\|_6^3\|\partial_i u\|_2\), so
\[
 \|u\|_6^4\le4\|u\|_6^3
       \prod_i\|\partial_i u\|_2^{1/3}
 \le4\|u\|_6^3\|\nabla u\|_2.
\]
For nonzero u, divide by \(\|u\|_6^3\); the zero case is immediate. Thus \(C_S=4\) suffices. A gradient-Cauchy sequence is consequently Cauchy in L6. Its L6 limit has the gradient limit distributionally, furnishing the canonical representative used in (4). This elementary domain lemma adds no physical input or alternative source model.
