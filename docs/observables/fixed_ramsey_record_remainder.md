# A uniform error bound for a Ramsey clock record

A first-order Ramsey calculation predicts the probability of a clock reading in a specified external field. How accurately does it predict the entire distribution when each trial also records the preparation, field and pulse phase? In the quadratic model below, a single explicit bound covers all 16 possible records. At the physical substitution $\lambda=c^{-2}$, the stated sufficient test bounds their total-variation error by $1/200$, inside the prescribed one-percent budget. Its application to a particular parameter set requires the values of those parameters.

## Model and complete record

Use a center of mass on $L^2(\mathbb R)$ with $[X,P]=i\hbar$, a supplied mass $M>0$, and internal ground and excited states with gap $\Delta E=\hbar\omega>0$. The uniform field takes either value $\chi\in\{g,0\}$ with fixed $g\ne0$. The ground-block Hamiltonian and the excited-block Hamiltonian are respectively

$$
H_0^\chi=\frac{P^2}{2M}+M\chi X,\qquad
H_e^\chi(\lambda)=H_0^\chi+\Delta E+\lambda\Delta E\,V_\chi,
\qquad V_\chi=\chi X-\frac{P^2}{2M^2}.
$$

Set the correction common to both levels to zero. Hold all other parameters fixed while varying $\lambda$, which has units of inverse velocity squared, over $0\le\lambda\le M/(2\Delta E)$. Use the same spatial origin, time coordinate and pulse-phase reference in both field settings. The earlier clock calculation supplies the first-order prediction and its matched field comparison. [Conditional internal-clock Ramsey readout](conditional_internal_clock_readout.md)

Preparation A is a pure Gaussian with position mean $x_0$, variance $s^2>0$, momentum mean $p_0$, and zero symmetrized position–momentum covariance. Preparation B applies a Gaussian random momentum displacement of mean zero and variance $\eta>0$ to A. Their momentum variances are $v_A=\hbar^2/(4s^2)$ and $v_B=v_A+\eta$. Each trial begins in the internal superposition $(|g\rangle+|e\rangle)/\sqrt2$. After free evolution for $T>0$, measure the projector onto $(|g\rangle+e^{-i\theta}|e\rangle)/\sqrt2$ and its complement.

An independent randomizer assigns probability $1/8$ to each setting $(j,\chi,\theta)$ with $j\in\{A,B\}$ and $\theta\in\{0,\pi/2\}$. Write $U_\lambda(t)$ for the evolution of $H_0^\chi+\lambda\Delta E V_\chi$ at the chosen field. For center-of-mass state $\rho_j$, the exact coherence and conditional positive-outcome probability are

$$
C_j^\chi=e^{-i\omega T}\operatorname{Tr}\!\left(U_\lambda(T)\rho_j U_0(T)^\dagger\right),
\qquad
p=\frac{1+\operatorname{Re}(e^{i\theta}C_j^\chi)}{2}.
$$

The exact distribution $P_\lambda$ assigns weights $p/8$ and $(1-p)/8$ to the two outcomes at that setting. The approximation uses

$$
C_{1,j}^\chi=e^{-i\omega T}(1-i\omega\lambda a_j^\chi),\qquad
a_j^\chi=\chi Tx_0-\frac{T(p_0^2+v_j)}{2M^2}
          +\frac{\chi p_0T^2}{M}-\frac{\chi^2T^3}{3}.
$$

Keep the carrier phase $e^{-i\omega T}$ exact. Clip $(1+\operatorname{Re}(e^{i\theta}C_{1,j}^\chi))/2$ to $[0,1]$ to obtain $q$. The approximate distribution $Q_\lambda$ assigns weights $q/8$ and $(1-q)/8$. Both laws retain all setting labels and both outcomes, including cells of zero weight.

## Bound and sufficient test

Set $G=|g|$, $v=v_B$, $m_2=p_0^2+v$ and $m_4=p_0^4+6p_0^2v+3v^2$. These second and fourth momentum moments bound the corresponding moments of both preparations. Define

$$
B=\frac{\omega^2}{2}
\left(GT\sqrt{x_0^2+s^2}
+\frac{T\sqrt{m_4}}{2M^2}
+\frac{GT^2}{M}\sqrt{m_2}
+\frac{G^2T^3}{3}\right)^2 .
$$

Uniformly on the declared interval,

$$
\max_{j,\chi}|C_j^\chi-C_{1,j}^\chi|\le B\lambda^2,\qquad
\operatorname{TV}(P_\lambda,Q_\lambda)\le \frac{B\lambda^2}{2}.
$$

The constant $B$ has units of velocity to the fourth power and is independent of $\lambda$ and $c$. For $\lambda=c^{-2}$ the registered test requires **both** $c^{-2}\le M/(2\Delta E)$ and $B/c^4\le1/100$. It then bounds coherence error by $1/100$ and total-variation error by $1/200$. If the test fails, the actual error remains undecided.

## Why a fourth momentum moment suffices

The generator after removing the internal carrier has the form $\alpha P^2+\beta X$, with $\alpha=(1-\lambda\Delta E/M)/(2M)$ and $\beta=(M+\lambda\Delta E)\chi$. In momentum space its unitary evolution translates $k$ by $\beta t$ and multiplies the translated wavefunction by $\exp[-i\alpha\int_0^t(k+\beta r)^2\,dr/\hbar]$. This strongly continuous group preserves Schwartz functions. Smooth compactly supported time averages approximate vectors in the generator domain in graph norm and can themselves be approximated there by Schwartz averages. Thus the Schwartz functions form a core and support the following product derivatives.

Write $\psi_\xi=e^{i\xi X/\hbar}\psi_A$, taking $\xi=0$ for A and the specified Gaussian displacement for B. In the ground interaction picture,

$$
U_0(t)^\dagger V_\chi U_0(t)
=\chi X-\frac{P^2}{2M^2}+\frac{2\chi t}{M}P-\chi^2t^2 .
$$

Its expectation integrated from zero to $T$ gives $a_j^\chi$. Apply Duhamel’s formula twice, first with the ground propagator on the left, then with the perturbed propagator on the left inside the first integral. For a single displaced vector the overlap remainder, with the common carrier stripped off, is exactly

$$
-(\omega\lambda)^2\int_0^T\!\int_0^t
\left\langle V_\chi U_0(t)\psi_\xi,\,
U_\lambda(t-u)V_\chi U_0(u)\psi_\xi\right\rangle\,du\,dt .
$$

This order places one unbounded perturbation on each ground-evolved Gaussian. The propagator between them has unit norm. At time $t$, the root mean square of $\|V_\chi U_0(t)\psi_\xi\|$ over the displacement obeys the triangle bound

$$
L(t)=G\sqrt{x_0^2+s^2}+\frac{\sqrt{m_4}}{2M^2}
       +\frac{2Gt}{M}\sqrt{m_2}+G^2t^2 .
$$

Cauchy–Schwarz on the vectors and on their common displacement distribution bounds the averaged absolute integrand by $L(t)L(u)$. These finite moments justify the scalar integrals over the full Gaussian tails. The ordered time integral gives $\tfrac12(\int_0^T L(t)\,dt)^2$, yielding $B\lambda^2$ for the coherence. Clipping fixes the exact $p\in[0,1]$ and contracts absolute differences, hence $|p-q|\le |C_j^\chi-C_{1,j}^\chi|/2$. Summing both complementary cells at each of the eight retained settings gives $\operatorname{TV}(P_\lambda,Q_\lambda)=\tfrac18\sum_{j,\chi,\theta}|p-q|$.

The design specified the coefficient and anticipated the Duhamel argument. An independent review checked the evolution domain, the ordering, the Gaussian moments and the complete record bound. The certificate applies to the supplied Hamiltonians, ideal preparations and projectors in this provisional model. The matched first-order field contrast retains its variance cancellation. The sign of any higher-order signal, the effects of omitted Hamiltonian terms, detector calibration, preparation and reset costs, empirical accuracy and any derivation of physical units from DET remain open.
