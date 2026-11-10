# A tidal pulse and its reverse have the same phase-balanced energy spectrum

At every calibrated probe frequency, a tidal pulse and its exact time reverse produce the same mean terminal energy from two orthogonal, equal-energy preparations. Scanning the frequency cannot distinguish these two histories. Retaining the preparation label can distinguish them. In the two-step example below, a probe released from maximum displacement finishes with $16E_0$ in one order and $E_0/16$ in the other.

## The observable and its physical preparation

Use the prescribed local Newtonian potential $\Phi(X,Y,Z,t)=-K(t)(X^2-Y^2)/2$. Its spatial Laplacian vanishes and its axial acceleration gradient is $K(t)$, with units of inverse time squared. Take a signed axial harmonic coordinate $q$ with zero equilibrium displacement relative to a freely falling reference. The probe and reference receive the same gravitational acceleration at the same position, and their axial gravitational acceleration difference at separation $q$ is $Kq$. With bare restoring force $-m\nu^2q$, the ideal differential mode obeys
$$
 \ddot q+(\nu^2-K(t))q=0,\qquad \nu>0.
$$
The reference, alignment, linear restoring law and negligible backreaction are supplied. A spring with nonzero resting separation $L$ would have a driving term $K(t)L$ in the equation for its extension. CL084 used that different preparation and a signed terminal velocity. [Two-template spring-velocity comparison](signed_spring_response_to_tidal_histories.md)

At each $\nu$ use energy coordinates $x=(q,\dot q/\nu)^{\mathsf T}$. Both components have length units, and the bare energy with the tide off is $E=m\nu^2\|x\|^2/2$. Prepare two separate runs with $x_j(0)=r e_j$, where $e_1,e_2$ are orthonormal and $r^2=2E_0/(m\nu^2)$ for known $E_0>0$. Repeat the same pulse for both. Read the bare mechanical energy immediately after switch-off at $T$. The phase-balanced result is the arithmetic mean of these two readings. The comparison of pulse orders uses the same $m,\nu,E_0$, phase convention and clock in both orders.

## Why reversal preserves the mean at every frequency

Let $U$ map $x(0)$ to $x(T)$. Its real generator is
$$
 \begin{pmatrix}0&\nu\\ K(t)/\nu-\nu&0\end{pmatrix}.
$$
Its zero trace preserves the determinant of the fundamental matrix, so $\det U=1$. This holds for every bounded piecewise continuous $K$ on the finite interval, even if the instantaneous restoring coefficient vanishes or becomes negative. Finite jumps of $K$ leave $q,\dot q$ continuous.

Write $S=\operatorname{diag}(1,-1)$ for velocity reversal. If $x(t)$ follows $K(t)$, then $Sx(T-t)$ follows $K_{\rm rev}(t)=K(T-t)$. It starts at $Sx(T)$ and ends at $Sx(0)$, giving
$$
 U_{\rm rev}=S U^{-1}S
  =\begin{pmatrix}d&b\\c&a\end{pmatrix},
 \qquad U=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
$$
For any orthonormal pair of preparations,
$$
 \frac{\bar E_K(\nu)}{E_0}
 =\frac{\|Ue_1\|^2+\|Ue_2\|^2}{2}
 =\tfrac12(a^2+b^2+c^2+d^2)
 =\frac{\bar E_{K_{\rm rev}}(\nu)}{E_0}. \tag{1}
$$
This is an exact identity for the same dimensional pulse and its reverse over the entire range $\nu>0$. If $\sigma\ge1$ is the larger singular value of $U$, the mean measures $(\sigma^2+\sigma^{-2})/2$. It records the amount of stretching in energy coordinates and discards the orientation of the input phases that gain or lose energy. Its frequency dependence may still distinguish other pulse shapes.

With displacement and velocity preparations $e_1=(1,0)^{\mathsf T}$ and $e_2=(0,1)^{\mathsf T}$, the displacement-labelled energy changes by $E_0(a^2-d^2)$ between forward and reverse. The velocity-labelled change has the opposite sign. Thus $a^2\ne d^2$ is necessary and sufficient for this particular pair of labels to distinguish the reversal at that frequency.

## A label that identifies the order, with a finite error margin

Fix a fiducial angular frequency $\nu_*>0$ once. Use the following consecutive constant segments, with zero tide before and after. In the reversed pulse the duration travels with its gradient.

| Segment | Dimensional gradient $K_j$ | Duration $\tau_j$ | Driven frequency $\Omega_j$ at $\nu=\nu_*$ |
|---|---|---|---|
| 1 | $-3\nu_*^2$ | $\pi/(4\nu_*)$ | $2\nu_*$ |
| 2 | $3\nu_*^2/4$ | $\pi/\nu_*$ | $\nu_*/2$ |

The common endpoint is $T=5\pi/(4\nu_*)$. Keep these actual gradients and durations fixed when changing the probe frequency. At the fiducial frequency both segments last a quarter period in their respective driven oscillators. The exact transfer of a quarter period is $P_j=\left(\begin{smallmatrix}0&\nu_*/\Omega_j\\-\Omega_j/\nu_*&0\end{smallmatrix}\right)$. Consequently
$$
 U_{1\to2}=P_2P_1=\operatorname{diag}(-4,-1/4),\qquad
 U_{2\to1}=P_1P_2=\operatorname{diag}(-1/4,-4).
$$

| Preparation and readout | $1\to2$ | $2\to1$ |
|---|---:|---:|
| Displacement preparation, terminal energy | $16E_0$ | $E_0/16$ |
| Velocity preparation, terminal energy | $E_0/16$ | $16E_0$ |
| Phase-balanced mean | $257E_0/32$ | $257E_0/32$ |

Even the unordered pair of readings coincides in this example. For a terminal energy tagged as the displacement preparation, compare the reading with $257E_0/32$, the midpoint of the two predictions. Above the threshold selects $1\to2$ and below it selects $2\to1$, for the two promised pulses. A deterministic absolute energy error bounded by $\varepsilon_E<255E_0/32$ guarantees the decision with the specified preparations, gradients and timing. At the half-gap itself the two allowed intervals touch.

## Work and limits of the inference

During the pulse the bare energy satisfies $\dot E=mKq\dot q$. Its terminal change is the work done by the prescribed tide on the mode. Equivalently, in either constant segment the energy including tidal potential is $E-mKq^2/2$ and is conserved. At a switch this quantity changes by $-m\,\Delta K\,q^2/2$ while the bare energy stays continuous. The tide does negative net work in the low-energy labelled run. The probe readout measures only the change on the probe side of that exchange. The example’s positive mean energy gain is $225E_0/32$.

The comparison requires preparation of both quadratures, repeatable fields over the probe’s excursion, a common time origin, and a calibrated terminal energy reading. That reading can in principle be defined by calibrated displacement and velocity or by a calibrated energy transfer. Preparing, reading, switching and resetting the probes require physical resources whose costs are outside the terminal mechanical energy. Retaining the phase label identifies the order of this promised pair. The calculation supplies no gravitational field energy, empirical detector qualification or DET-native energy or clock unit.
