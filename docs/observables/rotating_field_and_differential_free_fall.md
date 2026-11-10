# When tracking a rotating field identifies differential free fall

**Decision.** Four exact eccentricity vectors determine whether the two passive-to-inertial mass ratios agree, with one exception. A pure rotation at the field frequency with a nonzero amplitude in phase or antiphase with the field admits both equal and unequal ratios. The two explanations can give identical continuous trajectories throughout the observation. An independent measurement of the actual apsidal rate resolves every compatible case, including resonance, with the same four readings and an unknown detector zero.

## Model and record

The plane and both axes are registered and nonrotating. At $t=0$ the external field points along the positive real axis. Read the tagged vectors $y_n=b+e(nh)$ at $n=0,1,2,3$. The additive bias $b$ is one arbitrary complex constant. The supplied dynamics and parameter domain are
$$
\dot e=i\omega e+i a\delta e^{i\nu t},\qquad
\delta=P_1/I_1-P_2/I_2\in[-D,D]\subset\mathbb R,\qquad
\omega\in\Omega=[\omega_{\min},\omega_{\max}],
$$
with $0<\omega_{\min}<\nu<\omega_{\max}<\pi/h$, known $a,h,E,D>0$ and $|e_0|\le E$. The assumption $E+3haD\le e_{\rm small}$ controls the **true** eccentricity: the integrating-factor solution gives $|e(t)|\le |e_0|+a|\delta|t$ even at resonance. There is no bound on $|b|$ or $|y_0|$. The readout requires all four finite two-component vectors, the fixed phase of the external field and the same body ordering throughout. A pulsar triple provides motivation for considering a changing external direction. The equation and four vector readings are the stipulated experiment here. [Archibald et al. (2018)](https://arxiv.org/abs/1807.02059)

Put $R=e^{i\nu h}$ and $Q=e^{i\omega h}$. On the closed admissible arc $Q$ uniquely identifies $\omega=\arg(Q)/h$, with $0<\arg(Q)<\pi$. In particular $Q,R\ne1$. The two exact sampled solutions are
$$
\begin{array}{ll}
\omega\ne\nu: & y_n=b+FQ^n+L R^n,\quad L=a\delta/(\nu-\omega)\in\mathbb R,\quad F=e_0-L,\\[2mm]
\omega=\nu: & y_n=b+(e_0+nS)R^n,\quad S=i h a\delta\in i\mathbb R .
\end{array}
$$
For the first line, substitution into the differential equation gives the real forced coefficient $L$. For the second, $e^{-i\nu t}e(t)=e_0+i a\delta t$. This latter solution includes the term growing linearly in time on the finite window.

## Four-read inverse

First form $d_n=y_{n+1}-y_n$ for $n=0,1,2$. This removes the detector bias. Next form $w_n=d_{n+1}-R d_n$ for $n=0,1$. Substitution gives
$$
w_n=
\begin{cases}
(Q-R)(Q-1)F Q^n,&\omega\ne\nu,\\
(R-1)S R^{n+1},&\omega=\nu .
\end{cases}
$$
The following cases exhaust the data, including coincidences among individual readings. Every retained parameter set must obey the launch and forcing bounds above.

**1. $w_0\ne0$.** Form $Q=w_1/w_0$. Require unit modulus and an angle in the closed interval $[\omega_{\min}h,\omega_{\max}h]$. Failure gives no compatible world. Otherwise the rate is unique.

- If $Q\ne R$, recover
  $$
  F=\frac{w_0}{(Q-R)(Q-1)},\qquad
  L=\frac{d_0-(Q-1)F}{R-1},\qquad
  \delta=\frac{(\nu-\omega)L}{a},\qquad e_0=F+L,\qquad b=y_0-e_0 .
  $$
  Require $L$ real, $|\delta|\le D$ and $|e_0|\le E$. This single tuple is the full inverse if admissible. Equality is forced at $L=0$ and excluded otherwise.
- If $Q=R$, recover
  $$
  S=\frac{w_0}{R(R-1)},\qquad
  \delta=\frac{S}{iha},\qquad
  e_0=\frac{d_0-RS}{R-1},\qquad b=y_0-e_0 .
  $$
  Require $S$ purely imaginary, $|\delta|\le D$ and $|e_0|\le E$. This is the unique resonant tuple if admissible. Here $S\ne0$, so equality is excluded.

In either branch a failed reality or magnitude check rejects the record. To see sufficiency, the reconstruction matches $y_0,d_0,w_0,w_1$. These determine $d_1=R d_0+w_0$, then $d_2=R d_1+w_1$, hence all four original tags. No individual first difference needs to be nonzero.

**2. $w_0=0,\ w_1\ne0$.** Neither solution can realize this record, since in both $w_1=Qw_0$.

**3. $w_0=w_1=0$.** Define $T=d_0/(R-1)$. The data are exactly $y_n=b+T R^n$, with $b=y_0-T$. At every off-resonant rate the vanishing $w_0$ forces $F=0$; at resonance it forces $S=0$. Thus every solution has $e_0=T$, with the same bias. Reject $|T|>E$. For $|T|\le E$ the complete rate and response sets are

| Tracking amplitude at the registered initial phase | All admissible $(\omega,\delta)$ | Equality |
| --- | --- | --- |
| $T=0$ | Every $\omega\in\Omega$, $\delta=0$ | Forced |
| $\operatorname{Im}T\ne0$ | Only $(\nu,0)$ | Forced |
| $T\in\mathbb R\setminus\{0\}$ | Every $\omega\in\Omega$ with $\lvert\nu-\omega\rvert\le aD/\lvert T\rvert$, and $\delta=(\nu-\omega)T/a$ | Ambiguous |

For a constant record the true eccentricity is zero and the displayed constant is the bias. For nonreal $T$, a real $\delta$ cannot supply that phase off resonance. For real nonzero $T$, tuning $\omega=\nu$ gives zero difference; moving slightly to either side gives opposite, nonzero signs within the bound because $\nu$ is interior and $D>0$. Both endpoints are attained, whether set by the frequency band or by the bound on $|\delta|$. Each permitted tuple reproduces all four tags by the sampled solutions above. In the rotating frame the pure tracking solutions are equilibria.

## Matched trajectories and the independent rate check

Take $A=\tfrac12\min\{E,aD/(\nu-\omega_{\min})\}>0$, use $e_0=A$ and the same arbitrary $b$ in both worlds.

| World | Actual precession rate | Differential response | True eccentricity for $0\le t\le3h$ |
| --- | --- | --- | --- |
| Free precession at resonance | $\nu$ | $0$ | $A e^{i\nu t}$ |
| Forced tracking | $\omega_{\min}$ | $(\nu-\omega_{\min})A/a>0$ | $A e^{i\nu t}$ |

Both satisfy the launch and response bounds. They give the same $y(t)=b+A e^{i\nu t}$ at every instant of the window. Even calibrating the detector zero would leave this particular pair indistinguishable.

An independently calibrated $\omega_c$ restricts the inverse to that rate. In case 1 it must match the reconstructed value. For pure tracking with real $T$, the sole possible response is $(\nu-\omega_c)T/a$, including zero at exact resonance. Nonreal tracking requires $\omega_c=\nu,\delta=0$; a constant record requires $\delta=0$ at any admitted $\omega_c$. Thus a compatible independent rate fixes $\delta,e_0,b$ in every case. Incompatibility with that rate rejects the joint interpretation. Seeing the field frequency in the same eccentricity data is precisely the observation shared by the two worlds and supplies no such independent calibration.

The numerical $\delta$ uses $a,\nu,\omega$ in matching inverse-time units, $h$ in the calibrated clock, the registered two-component eccentricity scale and phase, and the signed order of the bodies. The equality tested is agreement of their passive-to-inertial responses in this convention. Their common absolute ratio is a separate measurement. The conclusions concern exact vector readouts over the supplied validity window.

The [constant-field cadence test](binary_free_fall_observation_cadence.md) uses a registered zero and a fixed external direction. Both tests assume a calibrated binary response law.

## Scientific provenance

DET Quantum Relativity derived the rotating-field inverse in E58. A distinct mass-registration reviewer checked the full four-read solution including exact resonance. Frozen QR report SHA-256 425c7c0b78e9d677299a27d63c82e82ca77d3950da56f4ba2d7a2440ab50f32f. Independent review SHA-256 db47455d7ed929156a959ef0bcbd006a4cf7d483752e2e0eeb5c9eaa1606dc03.
