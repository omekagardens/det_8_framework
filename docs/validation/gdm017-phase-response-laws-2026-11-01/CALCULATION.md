# GDM017 — unequal individual coefficient laws under uniform hidden phase

**Accepted scoped formal result after distinct review and coordinator disposition.** Uniform unobserved phase does not make the two individual formal coefficient laws identical. One normalized coefficient-space event has probabilities 0 in Model A and 2/3 in Model B. This is a statement about stipulated response coefficients, not an operational test or a controlled physical variance prediction.

## Accepted inputs and coefficient extraction

Use the unchanged [GDM015 Hamiltonians](../gdm015-gradient-response-2026-10-31/CALCULATION.md), ideal -fQ_x drive, local zero-offset potential -gR_x, canonical map, Q/R readouts and classical circular preparation. Keep M=2m, mu=M/4, C,a>0, omega^2=C/(mu*a^3), beta_PPN=gamma_PPN=1, no radiation interaction, and the same collision-free low-speed weak-local-field formal scope. Fix t=t_*=pi/(4omega), epsilon=c^-2. Phase varphi is uniform modulo2pi, fixed when differentiating in f,g, and unobserved. The models are alternative **unpaired** ensembles; a shared accessible hidden phase is not assumed.

The accepted [GDM016 report, equation (5)](PREPARATION.md) supplies the individual numerators. Its [distinct review](REVIEW.md) explicitly verifies them and the force identities. Prior GDM familiarity is disclosed; rejected GDM015-v1 is not an input. No new Hamiltonian term or approximation order is introduced here.

Write T_X^j=t_0+epsilon*tau_X^j at retained order, with t_0=t_*^2/2. Set
\[
u=2\varphi\pmod{2\pi},\quad
d=\frac{\mu a^2}{4M}>0,\quad k=\frac\pi2,\quad
s=\frac{t_*^2}{2M},\quad E_0=-\frac C{2a}.
\]
Uniform varphi makes u uniform: doubling wraps the circle twice with equal uniform weight. Specializing the accepted J gives J=d(cos u+sin u). The common raw readout correction is
\[
-\frac{t_*q_{0x}p_{0x}}M=dk\cos u.
\]
Consequently the **individual** coefficients are
\[
\begin{aligned}
\tau_Q^A&=-d(\cos u+\sin u),&
\tau_Q^B&=2d(\cos u+\sin u),\\
\tau_R^A&=d[(k-1)\cos u-\sin u],&
\tau_R^B&=d[(k+2)\cos u+2\sin u].
\end{aligned}\tag{1}
\]
These functions, rather than a paired B-minus-A difference, determine the unpaired marginals. Tau and d have units length squared; multiplying by epsilon gives a response with time-squared units.

## Matched individual formal ratios

Write S_X=s+epsilon*sigma_X and Z_X^j=T_X^j/S_X=M+epsilon*zeta_X^j. The accepted force identities give
\[
\sigma_Q=-sE_0/M,\qquad
\sigma_R=\sigma_Q+(dk/M)\cos u.
\]
The leading denominator s>0 is phase-independent. Formal division therefore gives zeta=(tau-M*sigma)/s. The R corrections cancel between numerator and denominator, so, **at this coefficient order**,
\[
\begin{aligned}
\zeta_Q^A=\zeta_R^A&=E_0-w(\cos u+\sin u),\\
\zeta_Q^B=\zeta_R^B&=E_0+2w(\cos u+\sin u),\qquad
w=\frac ds=\frac{8C}{\pi^2a}>0.
\end{aligned}\tag{2}
\]
Zeta, w and E_0 have energy units; epsilon*zeta has mass units. Equation (2) does not equate the individual raw Q/R responses or their force denominators. It is also not equality of exact finite-epsilon ratios beyond the retained order.

## Exact coefficient-space marginal laws

For uniform U, any variable h+A*cos U+B*sin U equals h+r*cos(U-delta) for an appropriate phase delta and r=sqrt(A^2+B^2)>0. Uniform angular measure gives the CDF
\[
F_{h,r}(x)=
\begin{cases}
0,&x\le h-r,\\
\tfrac12+\pi^{-1}\arcsin((x-h)/r),&h-r<x<h+r,\\
1,&x\ge h+r.
\end{cases}\tag{3}
\]
Indeed, for -1<y<1, the set cos U>y has angular length 2*arccos(y); its complement gives (3). Differentiation gives density 1/[pi*sqrt(r^2-(x-h)^2)] on the interior. There are no endpoint atoms, and the support is the full closed interval [h-r,h+r]. Thus all requested laws are specified by this table:

| Coefficient | Center h | Radius r |
| --- | --- | --- |
| tau_Q^A | 0 | sqrt(2)*d |
| tau_Q^B | 0 | 2*sqrt(2)*d |
| tau_R^A | 0 | d*sqrt((k-1)^2+1) |
| tau_R^B | 0 | d*sqrt((k+2)^2+4) |
| zeta_Q^A and zeta_R^A | E_0 | sqrt(2)*w |
| zeta_Q^B and zeta_R^B | E_0 | 2*sqrt(2)*w |

Raw Q and R laws are explicitly different: k=pi/2 lies between 0 and 2, giving r_RA<r_QA, while r_RB>r_QB. Within R, r_RB^2-r_RA^2=6*d^2*(k+1)>0. Within Q and in the normalized laws, Model B's radius is twice Model A's. Hence the A/B marginals differ for each requested readout.

For a measure-preserving negative control, shift varphi to varphi+pi/2. This reverses every centered sine/cosine coefficient above while preserving uniform phase, and therefore preserves its marginal law. A sign reversal or a nonzero paired difference alone is not evidence of a marginal distinction. The actual A/B radii differ, so no measure-preserving phase relabeling can equate their marginals: composing with such a relabeling preserves the pushforward law and its support.

## One distinguishing event

Retain exactly the following event in the normalized coefficient space, with r_A=sqrt(2)*w:
\[
\mathcal E=\{z:\ |z-E_0|>r_A\}.\tag{4}
\]
For either Q or R, Model A assigns probability zero, since its support ends at E_0 plus or minus r_A. In Model B, (4) is equivalent to |cos(u-pi/4)|>1/2. Its angular length is 4pi/3, so
\[
\boxed{P_A(\mathcal E)=0,\qquad P_B(\mathcal E)=\frac23.}\tag{5}
\]
No phase observation or pairing across models is used in this event. Its input is the ideal coefficient zeta; availability of that input is not established. These are population probabilities, not finite-sample risks or a claim that a response derivative is obtainable from one physical shot.

Both model coefficient means are E_0. The individual-ratio distribution therefore contains information absent from its mean. Consistently with GDM016, both the mean of individual formal ratios and the ratio of ensemble-mean responses equal M+epsilon*E_0 through the retained order, for both models and both readouts. The scalar ratio of ensemble means is not a draw from the nondegenerate laws (3).

## Physical boundary and decision

For the exactly truncated normalized random variable, event (4) would translate to
\[
|Z-(M+\epsilon E_0)|>\epsilon r_A.
\]
This is the same event expressed in response units, not a second proposed event. Its threshold and response spread shrink as c^-2. Exact coefficient probabilities do not supply resolution at that shrinking scale.

Any physical use still needs:

- A justified compatible physical composite/preparation and uniform phase distribution, with matched force/gravity controls, time, parameter calibration and Q or R readout. The native DET correspondence remains a separate obligation.
- Access to the individual response functional and its matched force denominator for the same preparation, or a justified direct readout with that joint pushforward law. Separately averaging uncontrolled-phase force and gravity runs does not produce the individual ratio distribution. This requirement is distinct from, and supplies no, cross-model hidden-phase pairing.
- Controlled omitted-model, response-derivative, ratio and calibration errors at the event's response scale. If an actual calibrated response were represented as M+epsilon*zeta+rho_epsilon, coefficient recovery would require quantitative control of rho_epsilon/epsilon, including measurement error. A justified small remainder or resolution bound relative to epsilon*r_A, together with control of probability mass near the threshold, is missing. Neither exact zero false-event probability nor the value2/3 transfers automatically under errors; a fixed nonvanishing noise scale is not negligible as epsilon tends to zero.

The accepted truncations omit physical contributions that may affect the retained coefficient itself. Their completeness cannot be assumed by naming an unknown correction a higher-order remainder. The squared spread of the truncated variable scales as epsilon^2, but promoting a coefficient second moment to a physical c^-4 variance prediction requires response-level moment/remainder and noise control not supplied here. No iid sampling, finite-sample guarantee or empirical execution is assumed.

**Decision:** retain this one conditional coefficient-space distributional event; uniform-phase signed-mean cancellation does not close it. Its physical response/readout/error and measurement dependencies remain open. The accepted signed-mean closure remains intact, and no broader physical gravity or ontology claim follows. This finite question is closed at the stated scope. See [adoption](ADOPTION.md) for the coordinator next-work decision; no optimization or new observable family is assumed.


Accepted phase-preparation dependency: [GDM016](PREPARATION.md). See [review](REVIEW.md), [adoption](ADOPTION.md) and [source manifest](SOURCE_MANIFEST.json).
