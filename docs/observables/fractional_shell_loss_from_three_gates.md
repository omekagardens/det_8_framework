# Fractional shell-encounter loss from three passive gates



The six exact readings identify the fraction of incoming radial kinetic energy transferred to the internal register. The spatial difference of two pre-crossing field readings calibrates the first gate’s jump in units of departing shell mass. A ratio of adjacent flight times measures how the outgoing shell slows. Together they determine the update and loss fraction using shared affine instruments with unknown offsets and positive gains.

## Encounter and first-crossing window

Use the [single-gate shell preparation](shell_encounter_from_field_step_and_time.md) with a central point mass $m$, shell A of mass $2m$ initially moving outward at $V$, and shell B of mass $m$ initially moving inward at $2V$. At coincidence the radius is $R$ and $V^2=Gm/R$. The approach has radial kinetic energy $K^-=3mV^2$. Transparent passage preserves each labelled velocity and A becomes outer. In a material contact the equal-and-opposite impulses per solid angle and the restitution rule give $2v_A^++v_B^+=0,\ v_B^+-v_A^+=3eV$, with $1/2\le e\le1$. Thus $v_A^+=-eV,\ v_B^+=2eV$, and B becomes outer. The gravitational potential energy is continuous at contact; both limits give $-15mV^2/2$. With no external work, define $\Delta E$ positive for the gain of the internal register. Then
$$
 \frac{\Delta E}{3mV^2}=
 \begin{cases}
 0 & \text{transparent passage},\\
 1-e^2 & \text{material contact}.
 \end{cases}
$$

Set $x=r/R,\ \tau=tV/R$, choosing physical $t=0$ at coincidence solely for the derivation. The three gate radii, in units of $R$, are $x_1=129/128,\ x_2=130/128,\ x_3=132/128=33/32$. CL090’s outer motion obeys $x''=-q/x^2,\ x'(0)=s,\ x(0)=1$, where primes use $\tau$. Enclosed mass plus half the shell’s own mass give $(s,q)=(1,3)$ for passage and $(2e,7/2)$ for contact. The positive outward speed satisfies $x'^2=s^2-2q(1-1/x)\ge26/33$ up to $x_3$. The donor’s inner-shell bound keeps it at positive radius moving inward throughout this first outward flight. The additional gates are passive and sample this same ordered arc; the physical horizon is the first crossing of $33R/32$.

## The two observable ratios

**Field.** Let $B_i^-$ be the displayed inward field immediately before the departing shell crosses gate $i=1,2$, and let $J_B=B_1^- -B_1^+$ be the displayed one-sided drop at gate 1. Put $g_*=Gm/R^2$. Each pre-crossing gate still encloses $4m$; the crossing removes only the departing mass from the enclosed total. For $\chi=m_{\rm out}/m$, the common field law gives
$$
 B_i^-=b_0+b_1\,4g_*x_i^{-2},\qquad
 J_B=b_1\,\chi g_*x_1^{-2},\quad b_1>0 .
$$
Here $b_0,b_1$ are the offset and gain. Form
$$
 \boxed{\chi_{\rm obs}
 =4\big[1-(129/130)^2\big]\frac{J_B}{B_1^- -B_2^-}} .
$$
The common additive zero cancels first and the common positive gain cancels in the ratio. The only allowed values are 2 for passage and 1 for contact. The individual displayed fields can have either sign because the offset is free.

**Time.** Let $C_i=c_0+c_1 t_i,\ c_1>0$, with unknown $c_0$; no encounter stamp is used. Write $H(x)=1-1/x,\ \lambda=2q/s^2$, and define
$$
 L_{ij}(\lambda)=\int_{x_i}^{x_j}\frac{dx}{\sqrt{1-\lambda H(x)}} ,
 \qquad x_0=1,\qquad
 \mathcal R(\lambda)=\frac{L_{23}(\lambda)}{L_{12}(\lambda)} .
$$
The physical time to any $x$ is $(R/(sV))\int_1^x [1-\lambda H(u)]^{-1/2}du$. Consequently
$$
 \boxed{S_{\rm obs}=\frac{C_3-C_2}{C_2-C_1}=\mathcal R(\lambda)},\qquad
 \lambda_{\rm passage}=6,\quad
 \lambda_{\rm contact}=\frac{7}{4e^2}\in[7/4,7].
$$

The span ratio is strictly increasing on the full allowed interval. Indeed $0\le H(x)\le1/33$, so the integrands and their parameter derivatives are bounded there. The log derivative of $L_{ij}$ is a weighted average of $H(x)/[2(1-\lambda H(x))]$ with strictly positive weight $(1-\lambda H(x))^{-1/2}$. The averaged function increases strictly with $x$. Its average over the later span is strictly greater than its average over the earlier span, whose interior lies entirely below $x_2$. Thus $d\log\mathcal R/d\lambda>0$, also establishing uniqueness despite the unequal distances of the two spans.

## Complete compatibility and recovery

Require six finite real readings, $C_1<C_2<C_3$ for the three **gate stamps**, $B_1^->B_2^-$, and $J_B>0$. Compute the two boxed observables above. The following are exact tests.

| Field result | Required span ratio | Recovered loss fraction |
|---|---|---|
| $\chi_{\rm obs}=2$ | $S_{\rm obs}=\mathcal R(6)$ | $0$, transparent passage |
| $\chi_{\rm obs}=1$ | $\mathcal R(7/4)\le S_{\rm obs}\le\mathcal R(7)$ | $1-7/(4\lambda)$, with $\lambda=\mathcal R^{-1}(S_{\rm obs})$ and $e=\sqrt{7/(4\lambda)}$ |
| Any other value or failed test | — | Incompatible |

Both contact endpoints are attained: $e=1$ gives zero loss and $e=1/2$ gives $3/4$. In particular a span ratio $\mathcal R(6)$ is valid in both rows; the field result resolves it.

For sufficiency take any positive compatible physical scales $G,m,R$ and the chosen CL090 update. Compute the three physical flight times. Choose the positive time gain from the first observed time difference divided by the first physical time difference; choose the offset to match the first stamp. The span-ratio check then matches the third stamp as well. Choose the field gain from the observed pre-crossing difference divided by $4g_*(x_1^{-2}-x_2^{-2})$, and the field offset to match the first pre-crossing value. The two pre-readings and the signed jump are now exactly the supplied readings. This realizes each passing record with one clock and one field convention. It leaves no further absolute-offset condition.

## What is lost when a channel is removed

**Complete outward trace, with or without a single uncalibrated jump.** Choose contact with $e^2=7/24$, strictly within the admitted interval. Then $\lambda=6$ in both models, while $s_{\rm contact}=\sqrt{7/6}$ and $s_{\rm passage}=1$. For the same $R,m,G$, the contact arrival time at **every** outer radius from $R$ through $33R/32$ is the transparent arrival time divided by $\sqrt{7/6}$. Giving the contact clock a gain $\sqrt{7/6}$ times the passage clock gain and the same encounter intercept produces the same entire displayed outer radius–time trace. Passage loses zero and contact loses $17/24$ of $K^-$. At gate 1 the contact field step is half the transparent step. Doubling the unknown field gain in the contact world matches the complete single-jump reading as well. One individual field level, if kept alongside the jump, can also be matched with the free offset. The two pre-crossing levels in the full record prevent this simultaneous rescaling.

**Only two gate stamps, even retaining the full field data.** On the contact branch, the two pre-crossing fields and the jump depend on shell masses and radii alone. For any two distinct ordered gates, every $e\in[1/2,1]$ has a positive physical flight span. Choose the clock gain to map that span to the given positive displayed gap and the offset to match the first stamp. Thus contacts with $e=1/2$ and $e=1$, for example, match both time stamps and every retained field value while losing $3/4$ and zero. All intermediate contact fractions are feasible. If the field data select passage, that update alone fixes the loss at zero.

## Standards and energy ledger

The readout requires registered gate-radius ratios, known mass ratios and incoming preparation, correctly ordered one-sided field tags, one stable affine field response across both radii and the jump, and one stable affine clock across all three passages. It also imports spherical Newtonian gravity, self-gravity with the half-shell convention, the two material updates and negligible gate backreaction. Independent clock origins per gate, drifting gains or an unsigned ambiguity in the field convention lie outside the model. These are exact observations with no instrument-resolution bound.

For a nonzero fraction, a loss in joules requires the incoming kinetic-energy scale $3mV^2=3Gm^2/R$, or an equivalent independent energy calibration. A calibrated mass and speed would suffice, as would mass and radius with known $G$. For example at fixed $G$, scaling $m$ and $R$ by the same positive factor leaves $V$ unchanged and multiplies $mV^2$ by that factor. The clock and field gains can absorb the corresponding changes in physical time and field, leaving all six displayed values fixed. The internal register balances the change in shell mechanical energy at coincidence; neither its starting level nor a microscopic destination such as heating is measured. No later evolution or detector work is inferred.
