# Calibrating acceleration gain with three signed position readings

Conditional measurement design accepted on 9 November 2026

For readings $p_-,p_0,p_+$ at times $-h,0,h$, the central second difference determines an interval for the instantaneous acceleration at zero. Its exact half-width is $4\sigma/h^2+Jh/3$, where $\sigma$ bounds each position error and $J$ bounds the rate at which acceleration can change. A simultaneous signed display reading then gives a sharp interval for the gain shared by the reference and the GDM065 motion channels. In the absence of a prescribed jerk bound, the same four exact readings can accommodate every gain in the prior.

## The reference measurement

Fix $h>0$. Let $t$ be the held central observer’s proper time and $x(t)$ the reference’s signed axial distance on the GDM049 simultaneity slice. The time origin, both spacings and the signed length scale are independently metered. Their conversion to these coordinates is exact in the model. The separate reference can be driven. Its initial position and velocity are free.

The entire record is $(p_-,p_0,p_+,d)$, including the display reading $d$ at the middle instant. For $t_i=-h,0,h$ the admitted errors satisfy
$$
 |p_i-x(t_i)|\leq\sigma,\qquad |d-kx''(0)|\leq\eta ,
 \qquad \tfrac12\leq k\leq\tfrac32 .
$$
Here $\sigma\geq0$ is in length units and $\eta\geq0$ in displayed acceleration units. All points in the simultaneous error box are permitted. The path is twice continuously differentiable on $[-h,h]$ and satisfies $|x''(t)-x''(s)|\leq J|t-s|$ for a supplied finite $J\geq0$ in length per time cubed. The same positive dimensionless $k$ multiplies the entire signed position acceleration on the driven reference and at each of the two science releases. The length and time standards are independent of that display and of the probe force law.

## The instantaneous acceleration interval

Define
$$
 D_p=\frac{p_+-2p_0+p_-}{h^2},\qquad
 W=\frac{4\sigma}{h^2}+\frac{Jh}{3},\qquad
 [a_-,a_+]=[D_p-W,D_p+W].                                             \tag{1}
$$
The set of attainable $x''(0)$ for the three raw readings is exactly $[a_-,a_+]$.

To prove the bound, first use true positions in the second difference and call the result $D_x$. Integrating the acceleration from zero on each side and adding cancels the initial velocity, giving
$$
 D_x=\int_{-h}^{h}\frac{h-|t|}{h^2}\,x''(t)\,dt .
$$
The weight has integral one. Its weighted mean of $|t|$ is $2h^{-2}\int_0^h(h-t)t\,dt=h/3$. The Lipschitz condition gives $|D_x-x''(0)|\leq Jh/3$. The three coefficients of the raw positions give $|D_x-D_p|\leq4\sigma/h^2$.

**Attainability for all three readings.** Choose $e\in[-\sigma,\sigma]$ and $s\in[-J,J]$. Set $z_-=p_-+e$, $z_0=p_0-e$, $z_+=p_++e$. Write
$$
 A=D_p+\frac{4e}{h^2}-\frac{sh}{3},\qquad
 V=\frac{z_+-z_-}{2h},\qquad
 x(t)=z_0+Vt+\frac{A}{2}t^2+\frac{s}{6}|t|^3 .                       \tag{2}
$$
This path has $x''(t)=A+s|t|$, which is continuous with Lipschitz constant $|s|$. Its middle position is $z_0$, its endpoint difference is $2hV$, and its true second difference is $A+sh/3=(z_+-2z_0+z_-)/h^2$. Thus its two endpoint positions are individually $z_-,z_+$. As $e,s$ range independently over the stated closed intervals, $A=x''(0)$ covers (1), including the endpoints. The construction also works when either tolerance is zero or $J=0$. An extremal path may have different one-sided jerks at zero, as allowed by the regularity assumption.

## Gain from the simultaneous display

Put $d_-=d-\eta$ and $d_+=d+\eta$. The exact feasible gain set is
$$
 \mathcal K=\{k\in[1/2,3/2]\mid k a_-\leq d_+\ \text{and}\ k a_+\geq d_-\}. \tag{3}
$$
For positive $k$, the attainable true displays fill $[ka_-,ka_+]$. The two inequalities are exactly its intersection condition with $[d_-,d_+]$. For any feasible $k$, choose a true display in the intersection, divide it by the positive $k$, and use (2) to realize the resulting acceleration and all positions. The recorded $d$ then has an admitted error.

The following rules give the endpoints of (3) for signed data. Start with lower and upper gain limits $1/2$ and $3/2$. Tightening a lower limit means taking a maximum, and tightening an upper limit means taking a minimum.

| Constraint | Positive acceleration endpoint | Negative acceleration endpoint | Zero acceleration endpoint |
| --- | --- | --- | --- |
| $k a_-\leq d_+$ | Tighten upper limit to $d_+/a_-$ | Tighten lower limit to $d_+/a_-$ | Require $0\leq d_+$ |
| $k a_+\geq d_-$ | Tighten lower limit to $d_-/a_+$ | Tighten upper limit to $d_-/a_+$ | Require $0\geq d_-$ |

A failed zero test or reversed limits give an empty calibration class. Equal surviving limits give an attained singleton. Distinct surviving limits give a proper interval if either end of the prior was removed. The full prior survives exactly when both inequalities in (3) hold at both prior endpoints, by linearity. In particular, if both the acceleration and display intervals contain zero, every gain fits. If the intervals are strictly of opposite signs, no positive gain fits. If $[a_-,a_+]=\{0\}$, the display alone tests whether $|d|\leq\eta$. For a tangency example, if $a_+>0$ and $d_-=(3/2)a_+$, the two intervals meet only at the prior endpoint $k=3/2$. Reversing the signs of all four readings reflects both intervals and yields the same gain set.

## Combining calibration with the clock and motion observations

In GDM065 the witness clock contrast $u$ measures the positive source scale $\theta$, and the motion contrast $v$ depends on that scale and the product $k\beta$. Here $\beta\in[1/2,3/2]$ is the common probe response and $0<\theta\leq\theta_{\max}$. The fixed compensated-source coefficients are $\alpha=1/336$ and $\gamma=56867/16934400$. The matched population contrast half-widths are $h_C=3c^2\epsilon_z/(4a^2)$ and $h_T=3\epsilon_g/(16a)$, with $a,c$ the calibrated science scales and $\epsilon_g$ expressed after display gain. The symbol $h$ in the reference trial is a sampling time, independent of these two half-widths.

The sharp combined parameter set consists of the triples satisfying
$$
 k\in\mathcal K,\qquad \tfrac12\leq\beta\leq\tfrac32,\qquad
 0<\theta\leq\theta_{\max},\qquad
 |u+\alpha\theta|\leq h_C,\qquad |v+\gamma\theta k\beta|\leq h_T .        \tag{4}
$$
Necessity comes from the two observation contracts. For sufficiency, a given feasible triple has a calibration trajectory and display error by (2)–(3). GDM065 supplies a normalized source-only kernel attaining the desired pair of science means at **that same gain and source scale**. The contracts allow the reference errors and science kernels to be chosen independently at fixed gain and shared frame/scale constants, so both constructions can hold together. The lawful source cut retains its own native law and its zero readout setting contrasts. Equation (4) tests science population means. Compatibility with any separately specified joint distribution or finite sample requires its corresponding observation model.

For an explicit decision, first require a nonempty $\mathcal K=[k_L,k_U]$. For a positive trial product interval $[q_L,q_U]$ define
$$
 \begin{split}
 C_\pm&=(-u\pm h_C)/\alpha,\qquad M_\pm=(-v\pm h_T)/\gamma,\\
 L&=\max(0,C_-,M_-/q_U),\\
 U&=\min(\theta_{\max},C_+,M_+/q_L).
 \end{split}
$$
The product interval fits exactly when $U>0$ and $L\leq U$. Indeed, a positive $\theta\in[C_-,C_+]$ must also have $[\theta q_L,\theta q_U]$ meet $[M_-,M_+]$. These inequalities give precisely the stated bounds after imposing the source cap. A positive contact point $L=U$ is attained. Contact only at zero is infeasible.

Use $[q_L,q_U]=[k_L/2,3k_U/2]$ for the full model and $[\beta_0 k_L,\beta_0 k_U]$ for a specified $\beta_0\in[1/2,3/2]$. Each listed product interval is filled by its permitted factors. Let $\mathcal B$ contain exactly the values of $\beta_0$ passing that test. An empty calibration or empty $\mathcal B$ rejects the combined model for the records. For nonempty $\mathcal B$, membership decides the unit-response question.

| Feasible responses | Population conclusion under the stated bounds |
| --- | --- |
| $1\notin\mathcal B$ | Unit probe response is excluded. |
| $\mathcal B=\{1\}$ | Only unit probe response fits. |
| $1\in\mathcal B$ and another value fits | Unit and nonunit responses are both compatible. |

### A strict contraction that changes a science inference

Fix any $h>0$ and an acceleration unit $A_*>0$. Take the mathematical reference record
$$
 (p_-,p_0,p_+,d)=(A_*h^2/2,\,0,\,A_*h^2/2,\,A_*),\qquad
 \sigma=A_*h^2/64,\quad J=3A_*/(16h),\quad \eta=A_*/16 .
$$
Here $D_p=A_*$. The distance and jerk contributions to (1) are each $A_*/16$, giving the acceleration interval $[7/8,9/8]A_*$. The display interval is $[15/16,17/16]A_*$. Their positive endpoints in (3) give
$$
              \mathcal K=[5/6,17/14]\ \subsetneq\ [1/2,3/2].
$$
Both contracted endpoints are attainable. For example, the lower endpoint pairs true acceleration $9A_*/8$ with true display $15A_*/16$. Taking $e=\sigma,s=-J$ in (2) supplies all three corresponding true positions. Reversing those choices gives $7A_*/8$ at the upper gain endpoint with true display $17A_*/16$.

Consider ideal science means with $\theta=\theta_{\max}/2$ and $k\beta=4/3$, so $u=-\alpha\theta$ and $v=-(4/3)\gamma\theta$ with zero science error widths. The original gain prior allowed unit response with $k=4/3$. The reference record restricts the feasible responses to $[56/51,3/2]$ by dividing this positive product by the attained gain bounds and intersecting the response prior. The combined model fits, for example at $(\beta,k)=(4/3,1)$, and excludes unit response. This is a conditional example with positive calibration tolerances.

## Smooth paths without a prescribed common jerk bound

Keep the same three times and the same middle-instant display. For arbitrary exact raw positions, let $Q(t)$ be their quadratic interpolant, so $Q''(0)=D_p$. For any proposed gain $k$ in the positive prior, the smooth path
$$
 x_k(t)=Q(t)+\frac{d/k-D_p}{2}\,t^2(1-t^2/h^2)                          \tag{5}
$$
has the same three raw positions. The added term vanishes at $-h,0,h$ and its second derivative at zero is $d/k-D_p$, so $k x_k''(0)=d$. Consequently the exact four-tuple alone retains the entire gain prior in this comparator. Each polynomial has finite jerk on the compact sampling interval. The metrological premise needed for (1) is a specified upper bound that applies before inference.

For an explicit pair, take exact readings $(A_*h^2/2,0,A_*h^2/2,A_*)$. Gain $k_1=1$ admits $x_1(t)=A_*t^2/2$. Gain $k_2=4/5$ admits
$$
 x_2(t)=A_*t^2/2+(A_*/8)t^2(1-t^2/h^2).
$$
Its middle acceleration is $5A_*/4$, giving the same nonzero display $A_*$. The second path has maximum absolute jerk $3A_*/h$. That exceeds the specific $3A_*/(16h)$ supplied in the contraction example. The three sampled positions conceal this difference between paths.

Join these calibration worlds to the GDM065 ideal science pair $(\beta_1,k_1)=(1,1)$ and $(\beta_2,k_2)=(5/4,4/5)$. Use the same positive $\theta=\theta_{\max}/2$, geometry, affine coefficients, frame and record access in both worlds. Both products are one. For every native cell $r=(s,\ell,S,b,j,n)$, the ideal science kernel places its mass at the same four-vector $Y_j$ in both worlds. For either native family $F$, any reference-record event $E$ and science-readout event $H$, the probability at that labelled cell in each world is
$$
 \mathbf 1_E(p_-,p_0,p_+,d)\ P_N^F(r)\ \mathbf 1_H(Y_j).
$$
This identity holds over all 224 science cells, their zeros and complements, and the full reference tuple with its common fixed sampling times. It compares the two worlds within the witness and, separately, within the lawful cut. The ambiguity concerns the complete observations specified here.

Physical use would require independently established time, length, sign, frame and simultaneity conversions, a justified bound on the fiducial’s acceleration variation, and a reference display at the middle instant. Interpreting the gain interval in the science trial also requires evidence that the same channel measures held-frame position acceleration under driven motion and both release conditions. A drive command and a carried proper accelerometer measure different quantities. The probe force law, source model, physical remainders and displayed-error bounds retain their stated status as premises.

## Sources and review

The held-frame coordinate and time convention comes from the [localized-source calculation](localized_source_clock_freefall.md). The accepted [probe-response and acceleration-gain result](paired_probe_response_and_acceleration_gain.md) gives the full observation law and population contrast test used here.

Frozen QR proof SHA-256 `60aaff788196d3622692ce75b2c0a7d11a6b0dc1a97b786ff8af29cbfc584dbe`. Independent scientific review SHA-256 `abba94ca16959bd81262b94a8b45f48f80e206a4b70f6f71acfd8001ab9ca09a`.
