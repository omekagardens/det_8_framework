# Initial circulation: an omitted-state comparator under one Euler law

CL117/v1. Conditional conventional result with distinct scientific review and recipient scope review. The continuum law, equation of state, preparations, material flow, regularity, exact field access and dimensional scales are supplied.

Two preparations have identical initial density, velocity, constants, oriented material loop and circulation, but different initial circulation rates:

\[
\boxed{\Gamma_A(0)=\Gamma_B(0)=0,\qquad
\dot\Gamma_A(0)=\frac{p_0}{20\rho_0}>0,\qquad
\dot\Gamma_B(0)=0.}
\]

The retained record omits pressure and the advected entropy label. The complete states differ under the same deterministic law. This is an exact two-preparation counterexample to predicting this initial rate from that reduced record; it is not evidence of different laws, stochasticity or quantum/classical divergence.

## 1. Supplied law, preparations and observation

Let \(L,\rho_0,p_0,g>0\), \(\gamma=5/3\), and \(K=p_0/\rho_0^\gamma\). Both preparations obey

\[
D_t=\partial_t+v\cdot\nabla,\qquad
D_t\rho=-\rho\nabla\cdot v,\qquad
D_tv=-\rho^{-1}\nabla p-g e_y,\qquad D_t\sigma=0,
\]
\[
p=K e^\sigma\rho^\gamma,\qquad \Phi=gy.
\]

Here \(\sigma\) is a dimensionless advected entropy label, not a measured heat or entropy-production record. On the surrounding three-dimensional patch

\[
P=(-L/2,3L/2)\times(-L/2,3L/2)\times(-L/2,L/2),
\qquad X=1+\frac{x}{4L},\quad Y=1+\frac{y}{4L},
\]

both preparations have \(\rho(0)=\rho_0X\) and \(v(0)=0\). The remaining initial fields are

| Preparation | Entropy label | Pressure |
|---|---|---|
| A | \(\log(Y/X^\gamma)\) | \(p_0Y\) |
| B | \(0\) | \(p_0X^\gamma\) |

Throughout the patch, \(7/8<X,Y<11/8\), so the density and pressure are positive and the displayed fields are smooth. Substitution verifies the same equation of state for both preparations; neither its constants nor its law change. The entropy and pressure fields do change.

A local solution that is \(C^1\) in time and \(C^2\) in space, together with a differentiable material flow, is a supplied premise. The initial equations give \(\partial_t\rho=\partial_t\sigma=\partial_t p=0\) and

\[
a_A:=D_tv\big|_0=-\left(\frac{p_0}{4L\rho_0X}+g\right)e_y,
\qquad
a_B:=D_tv\big|_0=-\frac{\gamma p_0}{4L\rho_0}X^{\gamma-2}e_x-g e_y.
\]

Initial-law compatibility does not prove positive-time existence or a lifetime. In particular, zero initial velocity is not equilibrium or zero acceleration. No wall, extra force or solved boundary-value problem is introduced.

The initial loop has the ordered vertices

\[
(0,0,0),\ (L,0,0),\ (L,L,0),\ (0,L,0),\ (0,0,0),
\]

counterclockwise viewed from \(+e_z\). In each preparation, that preparation's material flow transports the loop and its shared corner particles. The quantity is

\[
\Gamma(t)=\oint_{C(t)}v\cdot d\ell,
\]

evaluated only at \(t=0\) and its material time derivative there. Exact field, spatial-derivative and material-label access are supplied; no physical acquisition protocol is established.

## 2. Material transport and the initial rate

Parameterize each initial edge by \(q_j(s)\), \(0\le s\le1\), and write \(\chi_j(t,s)=F_t(q_j(s))\), where \(\partial_t\chi_j=v(t,\chi_j)\). Differentiate the sum of four edge integrals:

\[
\frac{d\Gamma}{dt}
=\sum_j\int_0^1\left[(D_tv)\cdot\partial_s\chi_j
 +v\cdot\partial_s v\right]ds.
\]

The moving-line-element term is

\[
\sum_j\left[\frac{|v(t,\chi_j)|^2}{2}\right]_{s=0}^{s=1}=0.
\]

Shared endpoints and the continuous velocity field make these corner contributions telescope. A change of tangent at a corner supplies no extra force term. At the initial event,

\[
\dot\Gamma(0)=-\oint_{C_0}\frac{\nabla p(0)}{\rho(0)}\cdot d\ell
 -\oint_{C_0}\nabla\Phi\cdot d\ell.
\]

The conservative-gravity term vanishes separately because the potential differences telescope around the closed loop. The varying density weight in the pressure term must remain inside the integral.

For A, \(\nabla p_A=p_0e_y/(4L)\). The horizontal edges contribute zero. The upward right edge has \(\rho=5\rho_0/4\) and contributes \(-p_0/(5\rho_0)\); the downward left edge has \(\rho=\rho_0\) and contributes \(+p_0/(4\rho_0)\). Their sum is \(p_0/(20\rho_0)\).

For B the pressure acceleration is \(-\gamma p_0X^{\gamma-2}e_x/(4L\rho_0)\). Define the positive endpoint difference

\[
H=\frac{\gamma}{\gamma-1}\frac{p_0}{\rho_0}
 \left[(5/4)^{\gamma-1}-1\right].
\]

The bottom and top pressure integrals are respectively \(-H\) and \(+H\); the vertical pressure integrals vanish. The complete edge ledger is

| Oriented edge | A pressure term | B pressure term | Gravity term, either preparation |
|---|---:|---:|---:|
| Bottom, rightward | 0 | \(-H\) | 0 |
| Right, upward | \(-p_0/(5\rho_0)\) | 0 | \(-gL\) |
| Top, leftward | 0 | \(+H\) | 0 |
| Left, downward | \(+p_0/(4\rho_0)\) | 0 | \(+gL\) |
| Sum | \(p_0/(20\rho_0)\) | 0 | 0 |

Both initial circulations are zero because the initial velocity vanishes. Reversing this same loop's orientation reverses A's signed rate and preserves B's zero; it is a sign-convention check, not another preparation.

## 3. Independent initial-surface check

On the same initial square surface \(S_0=[0,L]\times[0,L]\times\{0\}\), with normal \(+e_z\), the product rule gives

\[
\nabla\times(-\rho^{-1}\nabla p)
=\frac{\nabla\rho\times\nabla p}{\rho^2}.
\]

Uniform gravity has zero curl. For A,

\[
\nabla\times a_A=\frac{p_0}{16L^2\rho_0}X^{-2}e_z,
\]
\[
\int_{S_0}(\nabla\times a_A)\cdot e_z\,dx\,dy
=\frac{p_0}{16L^2\rho_0}\,L\,4L(1-4/5)
=\frac{p_0}{20\rho_0}.
\]

For B, the density and pressure gradients are both along \(e_x\), so the cross product is zero. Stokes' theorem therefore reproduces both direct edge sums, with the same surface, orientation and initial event. No evolved surface or positive-time result is used.

## 4. What the reduced record fails to identify

The common record retains the entire initial density and velocity fields on \(P\), \(g,L,\rho_0,p_0,\gamma,K\), the loop and orientation, and \(\Gamma(0)\). It omits \(\sigma\) and \(p\). Any single-valued predictor of \(\dot\Gamma(0)\) based only on these retained entries would give the same answer for A and B. The unequal derived rates show that such a predictor cannot be correct for both preparations.

This record includes continuum fields: it is not a finite-bit or finitely sampled record merely because the counterexample contains two preparations. Restoring the full entropy field, or equivalently here the positive pressure field with the retained density and common equation of state, removes this particular ambiguity under the stipulated exact derivative access. That is neither a minimal-readout theorem nor a physical measurement design or generic state-closure result.

A has a nonzero instantaneous circulation rate. B has a zero initial rate only. Nothing here establishes later conservation, stationarity, a shock-free interval, integrated circulation growth or a positive-time Euler solution.

## 5. Units, premise ledger and permitted use

Density retains three-dimensional units \([\rho]=M/L^3\), even though the loop and initial check surface are planar. Pressure has \([p]=M/(LT^2)\); hence

\[
[\Gamma]=L^2/T,\qquad [\dot\Gamma]=[p_0/\rho_0]=[gL]=L^2/T^2,
\qquad [K]=[p]/[\rho]^\gamma.
\]

The cancellation of the square size \(L\) in A's rate follows from these specified gradients and loop; it derives no native length or time unit. Gravity is present in each acceleration and cancels independently in each closed-loop rate. This neither estimates \(g\) nor derives gravity, mass or a native coupling.

Supplied premises are the state space, compressible Euler update, equation of state, entropy advection, uniform conservative gravity, patch, preparations, material loop, clocks, conventional scales, local regularity and exact field/derivative/material-label access. Derived consequences are the transported-loop relation, the signed initial rates, agreement of the two calculations and this reduced-record failure.

The permitted use is a conventional same-law comparator with its omitted state identified. A native application would need a separately supplied and justified state, update, material-loop/readout, regularity and unit correspondence. This construction supplies no native DET-to-continuum map, empirical data, apparatus qualification, heat or entropy-production measurement, different-regime dynamics, quantum/classical divergence or ontology validation. Retired kappa-gravity remains retired. No active QR/PIM result is imported as a premise, and this publication assigns no dependency or successor.

The original author result, distinct scientific review and distinct recipient scope review were accepted at this exact scope. This article is a public assembly of that result, not a new proof review or an empirical validation. Original machine/runtime/custody records and the private correspondence map are withheld under the [publication policy](../coordination/REDACTED_PUBLICATION.md); the public payload is identified in the [publication manifest](../publications/initial-circulation-omitted-state/PUBLICATION_MANIFEST.json).
