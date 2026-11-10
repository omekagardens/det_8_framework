# What two spectral lines and one weighing establish about passive mass

On the three registered carrier sectors, a change in the ratio of the two spectral lines rules out a common positive passive-to-inertial mass ratio. An unchanged line ratio leaves proportionality ambiguous. With matched endpoint weighing, every feasible record has a definite answer. Proportionality holds exactly when the line ratio stays constant and the measured endpoint passive-mass ratio equals the known endpoint inertial-mass ratio. This decision assumes the specified held energy levels, including removal of sector-dependent support shifts.

## Inverting all six lines

Label the whole-carrier preparations $00,10,11$ by $j=0,1,2$. The inertial ratios $r_j=M_j/M_0$ obey $1=r_0<r_1<r_2$. Write $q_j=P_j/M_0>0$. Define
$$
 A=r_1-1,\qquad B=r_2-r_1,\qquad D=A+B=r_2-1,\qquad
 d=q_1-q_0,\qquad e=q_2-q_1 .
$$
In the supplied common energy convention the three held levels in units of $M_0c^2$ are $r_j+u q_j$, up to a common term. The calibrated potentials are $u=0,+v,-v$ with $0<v<1$. The tagged lines on each display have the form
$$
 x_s=k_s(A+u_s d),\qquad y_s=k_s(B+u_s e),\qquad k_s>0 .
$$
All six readings must be finite and strictly positive. Define the normalized within-station ratio $z_s=A y_s/(B x_s)$. The zero station requires $z_0=1$ and fixes $k_0=x_0/A$. Set $m=vd/A$ and $n=ve/B$. Positivity of the four shifted gaps is exactly $|m|<1$ and $|n|<1$. The other stations require
$$
 z_+(1+m)=1+n,\qquad z_-(1-m)=1-n. \tag{1}
$$

**Different ratios.** For $z_+\ne z_-$, adding the equations and substituting back gives
$$
 m=\frac{2-z_+-z_-}{z_+-z_-},\qquad
 n=z_+(1+m)-1,\qquad d=\frac{A m}{v},\qquad e=\frac{B n}{v}. \tag{2}
$$
Keep this solution exactly when both strict gap bounds hold. Equivalently, for the positive readings already required, $z_+$ and $z_-$ must lie strictly on opposite sides of 1. Indeed, $1+m=2(1-z_-)/(z_+-z_-)$ and $1-m=2(z_+-1)/(z_+-z_-)$. Once both are positive, (1) makes $1\pm n$ positive as well. A single shifted ratio equal to 1 with the other different cannot fit. This branch identifies both dimensionless passive gaps, including their signs.

**Equal ratios.** For $z_+=z_-=z$, adding (1) gives $z=1$. Any other common value fails. At $z=1$ the entire gap family is
$$
              (d,e)=\lambda(A,B),\qquad -1/v<\lambda<1/v . \tag{3}
$$
Thus the equality $d/A=e/B$ is identified. The magnitude and sign of the slope remain free, including zero. The excluded endpoints of (3) would extinguish both lines at one station.

For **either** branch the complete family of positive masses and gains follows from
$$
 \Delta=d+e,\qquad
 (q_0,q_1,q_2)=(t,t+d,t+\Delta),\qquad
 t>T=\max(0,-d,-\Delta),\qquad
 k_\pm=\frac{x_\pm}{A(1\pm m)}. \tag{4}
$$
All parameters are finite. Any spectral gap solution admits such a $t$. Conversely, (4) gives the two $x$ readings at the shifted stations and (1) then gives the two measured $y$ readings. The zero-station check reconstructs its two lines as well. This proves sufficiency for the raw displays despite independent station gains. The strict bound on $t$ enforces positivity of all three masses.

## Proportionality and the endpoint weighing

If $q_j=k r_j$ for some $k>0$, then $d=kA$ and $e=kB$, so (1) requires constant line ratios. Every feasible different-ratio record therefore excludes proportionality for all $t$. In the constant-ratio family the masses are $q_j=t+\lambda(r_j-1)$. They are proportional exactly when $t=\lambda>0$. Choosing any $0<\lambda<1/v$ and $t=\lambda$ realizes proportionality. Increasing $t$ at that same $\lambda$ gives unequal ratios with identical six lines and identical gains. More generally, any common shift of the $q_j$ that maintains positivity adds a common $u$-dependent term to the held levels and preserves both transitions. Spectroscopy alone can never establish proportionality.

When present, the finite matched weighing ratio $R=P_2/P_0$ must be strictly positive. It adds precisely $\Delta=(R-1)t$ to (4). The following are the complete additional checks.

| Spectral record | Extra feasibility condition | What the weighing identifies |
|---|---|---|
| Different ratios, $R\ne1$ | $t=\Delta/(R-1)>T$ | All three $q_j$ are unique. The gaps already exclude proportionality. |
| Different ratios, $R=1$ | $\Delta=0$ | Every $t>T$ fits. The two nonzero gaps cancel and still exclude proportionality. |
| Constant ratios, $R\ne1$ | Every finite $R>0$ in this row fits | $0<t<D/(v\,\lvert R-1\rvert)$ and $\lambda=(R-1)t/D$. All solutions are proportional exactly when $R=r_2$. Every other $R$ excludes it. |
| Constant ratios, $R=1$ | Every $t>0$ fits with $\lambda=0$ | The two passive gaps vanish. The three equal positive passive masses exclude proportionality because the inertias increase. |

For the constant case, substituting $\lambda=(R-1)t/D$ gives $q_2=Rt$ and $q_1=t[1+(R-1)A/D]$, strictly between the two distinct positive endpoints when $R\ne1$. The strict upper bound on $t$ comes solely from the line gaps. Weighing fixes the sign of the nonzero slope and the entire relative passive profile here, while its magnitude remains free. In particular $R=r_2$ yields every $k=t$ in $(0,1/v)$. For $R=1$, (3) forces both gaps to zero only on the constant branch. A failed feasibility check in any row means the stipulated model cannot realize the record.

## A separating record and its holder control

Take $r=(1,2,4)$, $v=1/100$, and $(k_0,k_+,k_-)=(2,100,200)$. The three displayed pairs $(x_s,y_s)$, in station order $0,+,-$, are **$(2,4)$, $(101,202)$, $(198,396)$** in each of the following worlds.

| World | Intrinsic $(q_0,q_1,q_2)$ | Middle-level holder term in units of $M_0c^2$ | $R$ | Intrinsic proportionality |
|---|---|---|---|---|
| A | $(1,2,4)$ | $0$ | $4$ | Yes |
| B | $(2,3,5)$ | $0$ | $5/2$ | No |
| C | $(1,3/2,4)$ | $u/2$ | $4$ | No |

Worlds A and B have passive gaps $(1,2)$ and differ by a common shift. Their endpoint weighings separate them. As a check on the different-ratio branch, take $q=(2,3,2)$ with the same inertias, potentials, gains and zero holder shift. The three display pairs are $(2,4),(101,199),(198,402)$. Equation (2) recovers $d=1$ and $e=-1$. Equal endpoint weights here admit all $t>0$ in $(t,t+1,t)$ and exclude proportionality.

For the holder control, allow only the extra dimensionless energy $u b$ on level 1. The displayed lines then depend on $d+b$ and $e-b$. In world C, $b=1/2$ changes the intrinsic gaps $(1/2,5/2)$ to the effective gaps $(1,2)$ at the level of the potential coefficients. Worlds A and C have identical end states, endpoint weighing, all gains and all six raw lines, with opposite intrinsic conclusions. Even one uncalibrated middle-level support response suffices to defeat the affirmative intrinsic test.

## Physical scope

The two spectral lines require prepared and identified whole-carrier sectors, persistence across all three stations and the balance, accessible tagged adjacent transitions, and independent inertial ratios for those same sectors. A shared baseline energy convention fixes the zero-potential gaps to $A,B$ in units of $M_0c^2$. The signed potential differences from that reference must be known in units of $c^2$. The inverse uses the stated affine level law exactly at those three settings. Clock rate, frequency conversion, reference scale and any common lapse enter once through the station gain. To form each ratio, the two tagged lines must share that gain and have their display zeros, recoil and level-dependent support shifts controlled. Matched endpoint weighing requires the same applied field and balance response for both endpoint preparations, with fixture loads removed.

Equations (2)–(4) concern ratios to $M_0$. Reporting passive masses in kilograms requires a dimensional determination of $M_0$ and, wherever the family remains nonunique, enough information to select its member. Absolute transition energies require an energy standard or $M_0c^2$ calibration and the corresponding frequency conversion for a physical display. Preparing and holding the carrier, exciting or interrogating the lines, generating the potential differences, weighing, reading and resetting all require external resources. Earlier spring, signed-lift, free-recoil, device-exchange and same-carrier results address distinct registrations. The occupation labels alone supply neither these transitions nor their energy and clock standards. The conclusion is a conditional comparison on three sectors of one carrier.

## Scientific review

DET Energy Research supplied the derivation. A distinct reviewer verified the two-line inverse, constant ratios, endpoint weighing and middle-level support ambiguity. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `5b21d7dba7950606aae9750ae9a42afb2cc2f1dc962cb681247a4d9fbeae2672`.
- Author report SHA-256: `fd664d93a0b8b714c6a982336fca1720ca5afe8c95b33f66fdc7976cba85bbe8`.
- Author freeze SHA-256: `e3af24637a08e182293fa0f705ded1e2957713bd91158e4a5dd3b024f598c517`.
- Independent scientific review SHA-256: `fb3f3a0d9602350cafc0cba09ba3632c091914a3dc2a48ec15687c1894529e1a`.
