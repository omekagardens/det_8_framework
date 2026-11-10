# Testing dispersion with moving phase and tracked velocity

Three distinct positive speed settings distinguish the two supplied exact Hamiltonians under a common speed gain and a common dwell ratio. For square-root dispersion the squared moving-to-rest phase ratio is affine in the squared speed display. For quadratic dispersion the phase ratio itself is affine. The two feasible three-point domains are disjoint. Two settings can fit both laws, and unequal dwell ratios can make the quadratic law reproduce an otherwise distinguishing three-point square-root record.

Fix one registered sector $J=J_*$ with $E=E(J_*)>0$ and $E'=E'(J_*)>0$. Its stationary advance is $\phi=TE'$. The physical candidate laws are
$$
 H_R=C_{\rm out}+\sqrt{E(J)^2+c^2p^2},\qquad
 H_Q=C_{\rm out}+E(J)+\frac{c^2p^2}{2E(J)} .
$$
Both are used as exact laws for this comparison. The independent local boost theorem determines a quadratic coefficient under its own assumptions and supplies no unique finite-momentum continuation. The previous moving-phase inverse assumed $H_R$ while comparing sectors at common momentum. Here the sector is fixed and momentum may vary between settings. [Local boost result](conditional_boost_mass_relation.md) · [Accepted moving-phase inverse](moving_phase_test_of_spring_inertia.md)

Use Hamilton's phase equation $\dot\theta=\partial_JH$ at fixed physical canonical momentum, and independently track the position velocity $v=\partial_pH$ at fixed $J$. For $u=cp/E>0$ these equations give
$$
 \begin{array}{c|c|c}
 &v/c&\dot\theta/E'\\ \hline
 R&u/\sqrt{1+u^2}&1/\sqrt{1+u^2}\\
 Q&u&1-u^2/2
 \end{array}
$$
The energy derivative in the second row includes the derivative of $1/E(J)$ in the kinetic term. Omitting it would change the test.

Write $\beta=v/c$, with $0<\beta<1$ in each admitted candidate. During a constant-momentum dwell of duration $\lambda T$ the measured ratio is therefore
$$
 r=\psi/\phi=
 \begin{cases}
 \lambda\sqrt{1-\beta^2},&R,\\
 \lambda(1-\beta^2/2),&Q.
 \end{cases}                                                    \tag{1}
$$
The displayed speed is $s=gv$ with one finite positive gain and zero offset, so $\beta=s/(gc)$. The positive phase condition follows from the stipulated velocity range, including the quadratic case where $\lambda/2<r<\lambda$. The square-root case has $0<r<\lambda$. The shared $\lambda$ is a ratio of physical lab durations and is independent of the unknown speed gain in the supplied contract.

The exact input domain requires finite $0<s_1<s_2<s_3$, finite $r_j>0$, and qualified stationary and moving phase readouts. Set $x_j=s_j^2$. Define slopes and intercepts separately for each candidate as follows.

| Test | Square-root candidate $R$ | Quadratic candidate $Q$ |
|---|---|---|
| Transformed phase | $y_j=r_j^2$ | $y_j=r_j$ |
| Fit first two settings | $B=(y_1-y_2)/(x_2-x_1)$ and $A=y_1+Bx_1$ | Same definitions using this column's $y_j$ |
| Strict parameter check | $B>0,\ A>0$ | $B>0,\ A>0$ |
| Third setting | $y_3=A-Bx_3$ | $y_3=A-Bx_3$ |
| Strict speed domain | $Bx_3<A$ | $2Bx_3<A$ |
| Conditional reconstruction | $\lambda=\sqrt A,\quad gc=\sqrt{A/B}$ | $\lambda=A,\quad gc=\sqrt{A/(2B)}$ |

These tests are necessary and sufficient. In $R$, the positive observed $r_3$ and the third-point identity already ensure the speed bound, which is stated explicitly to preserve its meaning. In $Q$, positivity of $r_3$ alone is insufficient; the stronger condition is $r_3>A/2$. A zero slope would require an excluded limiting gain or indistinguishable speeds. Negative or zero fitted parameters fail the positive physical domain. At $Bx_3=A$ in $R$, the final phase is zero and the speed equals $c$. At $2Bx_3=A$ in $Q$, the final speed equals $c$ despite a positive phase. Both boundaries are excluded. Coincident speeds violate the stated three-setting preparation.

To establish sufficiency on a passing record, keep any permitted stationary $E,E',T$ and choose the reconstructed $\lambda,g$. For each setting use
$$
 \frac{cp_j}{E}=
 \begin{cases}
 \beta_j/\sqrt{1-\beta_j^2},&R,\\
 \beta_j,&Q,
 \end{cases}
 \qquad \beta_j=\frac{s_j}{gc}.
$$
Each momentum is finite and positive. These parameters recover both the measured speed and the phase ratio at all three settings. They also recover the complete phase outcome probabilities for each prospectively labelled setting. The unique fitted pair $(A,B)$ fixes $\lambda$ and $gc$ conditional on the law; with a calibrated physical $c$, it fixes the speed gain $g$. It also fixes all $\beta_j$, $cp_j/E$ and the momentum ratios.

For separation, suppose the same three observations passed $Q$, so $r_j=a-bx_j$ with $b>0$. Its square would be $a^2-2abx+b^2x^2$. Passing $R$ as well would require this quadratic to equal an affine function at three distinct $x_j$. Their difference would be a quadratic with nonzero leading coefficient and three distinct roots, which is impossible. A triple can consequently pass $R$, pass $Q$, or fail both. The conclusion is conditional on the two laws and their registered observation model.

With just two settings, any $0<x_1<x_2$ and $r_1>r_2>0$ give a valid $R$ fit. For $Q$ the additional subluminal condition reduces to
$$
 \frac{r_2}{r_1}>\frac{x_2}{2x_2-x_1}.
$$
Thus the entire admissible two-setting $Q$ domain overlaps the $R$ domain. As an exact example, choose any positive speed-display scale $S$ and read
$$
 (s_1,s_2)=(S,2S),\qquad (r_1,r_2)=(9/10,3/5).
$$
The quadratic fit has $\lambda_Q=1$ and $(g_Qc)^2=5S^2$. The square-root fit has $\lambda_R^2=24/25$ and $(g_Rc)^2=32S^2/5$. Both velocities are strictly between zero and $c$ in both interpretations. The same stationary function $E(J)$ and the appropriate candidate momenta realize each interpretation. Their different gains and dwell ratios are free calibrations in this two-setting record.

A complete synthetic three-setting record can be attached to the stationary example in the accepted action study. Choose $M_q=M_*(1,2,4)$, $K=M_*/T^2$, $L=cT$, $J_0=2\log(2)M_*c^2T$, and $E(J)=M_*c^2\,2^{J/J_0}$. The stationary phases are $(1/2,1,2)$ radians with action interval $(1,2)$ in units of $M_*c^2T$. Select $q=1$, so $J_*=J_0$, $E=2M_*c^2$ and $\phi=1$ radian. Use all spring, signed lift/blank, stroke, echo and store readings of that source's §5, including its weak-field restrictions. This supplies a feasible stationary preparation. [Stationary example and complete tagged law, §§2–5](action_per_occupation_from_sector_masses.md)

For the moving preparations take $H_R$, $\lambda=1$, $gc=S$ and
$$
 \beta=(3/5,\,4/5,\,12/13),\qquad
 s=S(3/5,\,4/5,\,12/13),\qquad
 r=\psi=(4/5,\,3/5,\,5/13).
$$
The normalized momenta are $(3/4,4/3,12/5)$. The data satisfy $r_j^2=1-s_j^2/S^2$. For a quadratic fit, the negative secant slopes of $r$ against $x=s^2$ would have to agree. Their magnitudes are $5/(7S^2)$ and $65/(64S^2)$, so this triple fails $Q$.

The native preparations remain $00,10,11$ at reference-memory label zero with initially equal zero angles in the inherited phase arm. The native mechanical histories retain the exact weights
$$
 p_i(H)=\frac{q_a}{4}\left(1+\frac{\epsilon_a}{2}{\bf1}_{i=1}\right),
 \quad (q_E,q_F)=(2/3,1/3),\quad
 (\epsilon_E,\epsilon_F)=(1/8448,-1/4224),
$$
and the spring trials retain their independent history-product law. The existing stationary experiment can be kept as one prospectively tagged block with every internal randomization and unconditional cell weight in its published §2. For a separately tagged moving block, choose $j$ uniformly among the three settings and the cosine or sine quadrature fairly. The conditional probability per tagged sign cell is $(1\pm Z_j)/24$ and per failure cell is $1/12$, with $Z_j=\cos\psi_j$ or $\sin\psi_j$. Append its separately tracked speed $s_j$ to every cell, including phase failures. These 18 cells sum to one within the moving block and retain failure probability $1/2$. An independent fair choice between the existing block and this added block specifies a complete combined record by multiplying both block laws by $1/2$. All source histories, zeros and failures within the original block keep their relative and conditional weights. No mechanical history is assigned to a phase trial. The phase interface and reference convention are supplied physical attachments. [Native phase interface](native_phase_action_interface.md)

A shared timing registration is essential. Keep the synthetic triple's stationary preparation and the same gain $gc=S$. Under $H_Q$, choose the same three physical velocities but use
$$
 \lambda_j=\frac{r_j}{1-\beta_j^2/2}
           =(40/41,\ 15/17,\ 65/97).
$$
All are positive. The three quadratic momenta are now $cp_j/E=\beta_j$, and every recorded phase, speed and detector probability agrees with the square-root record. This changes only the premise that the moving dwells share one duration ratio. Thus timing equality must be independently established. Allowing unregistered changes of speed gain, phase reference or sector between settings would likewise change the model being tested.

Both candidates have the same kinetic Hessian at zero momentum, $\partial_p^2H|_0=c^2/E$. Distinguishing their finite-momentum behavior therefore tests an assumption needed by the earlier mass-offset interpretation. It does not determine $E$ itself. At fixed $E'$ and stationary level differences, the internal energy origin can be shifted within its positive domain and the momenta scaled to keep all $cp_j/E$ fixed. The phases and velocities above then persist. The externally additive $C_{\rm out}$ is also absent from both derivatives. The inherited stationary action constraints still apply, but the new fixed-sector ratios supply no absolute $J_0$ or mass scale. Absolute momentum requires $E/c$, an absolute moving duration requires $T$, and dimensional velocity calibration uses the supplied physical length/time convention and $c$.

Phase extraction must use the whole tagged setting, including failures, with the calibrated quadrature law. Known turn counts or a justified unwrapping band are required for both stationary and moving advances. Each moving advance is measured over its constant-momentum dwell; any phase accumulated during acceleration must be independently subtracted or excluded by the reference protocol. A failure or unresolved phase cannot be discarded to change the setting denominator. The tracked velocity must be the physical Hamiltonian velocity in the same lab convention, with one multiplicative gain and a verified zero. Finite-sample probabilities, drift, gain errors and uncertainty in phase unwrapping were not supplied. With such uncertainty, compatibility would require one shared set of admissible parameters for all three settings before excluding either law.

The ideal translational energy supplied at fixed sector is $E[(1-\beta^2)^{-1/2}-1]$ for $R$ and $E\beta^2/2$ for $Q$. The record determines each cost relative to its candidate $E$. Preparation, acceleration, maintaining the sector and reference, tracking position, timing, phase detection and restoration have additional unmeasured costs. The stationary store calibration covers its registered mechanical operations; a moving experiment requires its own preparation and restoration accounting. This is a finite conditional theory test with a synthetic record. It derives no new dispersion law, physical detector, gravity calibration or native unit.
