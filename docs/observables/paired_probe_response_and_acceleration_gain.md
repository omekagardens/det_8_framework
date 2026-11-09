# What paired clock and motion records identify about probe response

GDM065 · Independently reviewed and accepted on 9 November 2026

The ideal clock contrast determines the active source scale $\theta$. The ideal motion contrast then determines $q=k\beta$, the product of acceleration gain and probe response. With unit calibrated gain this identifies $\beta$. With an unknown common gain, even the complete recorded probability law admits distinct values of $\beta$ at the same source strength. The bounds on gain still allow some observations to exclude $\beta=1$.

## Observation model

Fix calibrated $a,c>0$, the source geometry, the held central frame and finite common affine coefficients $A,B$. Choose any finite $\theta_{\max}>0$ admissible for the assumed weak-field domain and keep it fixed. The active source coefficients are $m_g$ and $2m_g$, with $Gm_g=\theta a^3$ and $0<\theta\leq\theta_{\max}$. In the proposed force model, the passive gravitational coefficient divided by the inertial coefficient is $m_p/m_i=\beta$. The probes share the dimensionless response $\beta\in[1/2,3/2]$ at the two release locations. The dimensionless display gain $k$ is either known to be one or is fixed but unknown in $[1/2,3/2]$. These two parameters apply to all sources, settings and records.

For source label $j=(r,e)\in\{00,10,01,11\}$, the static compensated map places the occupied sources at $+a,-a$ and the auxiliary at $X_A=-(a/2)(r-e)$. At the exterior readout positions its potential is
$$
 \Phi_j(x)=-\theta a^3\left(\frac r{x-a}+\frac e{x+a}+\frac2{x-X_A}\right)+A+Bx.
$$
Only $10,01$ have positive probability in this preparation. The geometry, source map and held-readout phase are supplied. The source inertial masses play no role in these equations.

Write $R=3a,\ d=a/2,\ x_\pm=R\pm d$. The calibrated clock readings are $z_\pm=[\Phi_j(x_\pm)-\Phi_j(R)]/c^2$. At the retained order we stipulate the probe's initial central-frame position acceleration at release to be $-\beta\Phi'_j(x)$. Including display gain, the ideal recorded vector is
$$
 Y_j(\theta,\beta,k)=
 \big(z_+,z_-,-k\beta\Phi'_j(x_+),-k\beta\Phi'_j(x_-)\big).             \tag{1}
$$
The product multiplies the entire derivative, including $B$. The clock convention is independent of that gain. For $\beta\ne1$ the response is a new phenomenological force law. Its scope is the initial relative position acceleration in the specified frame. The geodesic calculation at $\beta=1$ supplies neither its higher-order extension nor a prediction for the probe's proper accelerometer at other values of $\beta$.

## Complete record and the matched source cut

Let $F=W$ denote the GDM047 witness and $F=D$ its complete lawful source cut. For each family, write $h=(s,\ell,S,b,j,n)$ for the native record. It contains the equally likely chain or antichain setting, preparation bit, actual ideal, newborn bit, terminal source and reference bit. For initial state $\nu=\delta_{10}\otimes\delta_0$, the supplied native probabilities are $P_N^F(h)=(\lambda_s/2)[B^F_{C_{s,\ell},S,b}\nu]_{j,n}$, where $\lambda_s=1/2$. The native maps enter the proof through their normalized probabilities and the source marginals below. Every comparator receives the same record access.

For each Borel set $E\subseteq\mathbb R^4$, the complete observation law is
$$
 \Pr_F(h,Y\in E)=P_N^F(h)K(E\mid j).                                      \tag{2}
$$
One normalized source-only kernel is shared across settings and both families. In the ideal case $K=\delta_{Y_j}$. Equation (2) retains all 224 native cells, including their zeros and complements. Taking $E=\mathbb R^4$ and summing over the cells gives one. Expectations use the full setting denominator. The four-coordinate readout adds no detector loss. An application that records failures needs their retained probabilities and a prospectively defined contribution to the means.

In source order $(00,10,01,11)$, the witness probabilities are $(0,51/64,13/64,0)$ at chain and $(0,3/4,1/4,0)$ at antichain. Their difference is $(0,\delta,-\delta,0)$, $\delta=3/64$. The cut has the latter marginal in both settings. It therefore has equal setting-conditional readout marginals for any shared $K$, and both of its setting-mean contrasts vanish. Equation (2) keeps each family's own native record probabilities.

## Ideal identification and a full-record counterexample

For $Y=(z_+,z_-,g_+,g_-)$ use
$$
 C=c^2(z_++z_-)/d^2,\qquad T=-(g_+-g_-)/(2d).
$$
Let $(u,v)=(\Delta C,\Delta T)$ be the witness chain-minus-antichain population contrasts. Put $\alpha=1/336$ and $\gamma=56867/16934400$, the accepted compensated-source coefficients. The symmetric clock sum and the motion difference cancel their respective affine contributions. Linearity in the displayed acceleration and (1) give the ideal equations
$$
     u=-\alpha\theta,\qquad v=-\gamma\theta q,\qquad q=k\beta.              \tag{3}
$$
Both contrasts and $\theta$ have units of inverse time squared.

On the ideal model, recover $\theta=-u/\alpha$ and check $0<\theta\leq\theta_{\max}$. Then recover $q=-v/(\gamma\theta)$ and check its admitted range. Thus the two witness contrasts alone determine $(\theta,q)$. Equality of full ideal witness laws entails equality of these contrasts. Conversely, fixed common geometry, affine coefficients and frame make every vector (1) a function only of $(\theta,q)$, so equality of this pair gives equality of the full laws in (2), separately for witness and cut. Even the labelled ideal cut can recover the pair from its supported $j=10$ readings through the accepted values $C_{10}=-(38/105)\theta$, $T_{10}=-(229/600)\theta q$. Its *setting contrasts* alone contain no such information.

For known $k=1$, $\beta=q\in[1/2,3/2]$. For unknown $k$, the products range over $[1/4,9/4]$. At fixed ideal $\theta,q$ the exact equivalent parameter pairs are
$$
  \max(1/2,2q/3)\ \leq\ \beta\ \leq\ \min(3/2,2q),\qquad k=q/\beta.       \tag{4}
$$
These inequalities impose both original parameter bounds. The interval has positive length for every interior product. At $q=1/4$ both factors must be $1/2$, and at $q=9/4$ both must be $3/2$.

For an explicit ambiguity involving unit response, take $\theta=\theta_{\max}/2$ in both worlds. Use $(\beta,k)=(1,1)$ in one and $(5/4,4/5)$ in the other. Each has $q=1$. With the same $A,B,a,c$, frame, native probabilities and record access, their four coordinates agree at **every** $j$. For every $h,E$, the probability in each world equals $P_N^F(h)\mathbf 1_E(Y_j)$. This proves equality of complete normalized ideal laws, including the two acceleration readings before differencing. In ideal data, the unknown-gain class admits unit response exactly for $q\in[1/2,3/2]$. Other admissible products exclude it through the specified gain limits.

## Bounded errors and the sharp population region

Assume finite uniform bounds $\epsilon_z,\epsilon_g\geq0$. For every $j$, allow every probability kernel supported on
$$
 Y_j+[-\epsilon_z,\epsilon_z]^2\times[-\epsilon_g,\epsilon_g]^2.
$$
Here $\epsilon_g$ is in displayed acceleration units *after* gain. Arbitrary biases and correlations within this box are allowed. The same conditional kernel for a given source must serve both settings and the cut.

A single source can acquire a conditional mean bias of at most $B_C=2c^2\epsilon_z/d^2$ in $C$ and $B_T=\epsilon_g/d$ in $T$. Each witness contrast bias is $\delta$ times the difference of the biases at $10$ and $01$. This gives the matched half-widths of GDM051,
$$
 h_C=2\delta B_C=\frac{3c^2\epsilon_z}{4a^2},\qquad
 h_T=2\delta B_T=\frac{3\epsilon_g}{16a}.                                  \tag{5}
$$
Both bounds are simultaneously sharp, including all interior biases. To see this, prescribe any contrast bias $(e_C,e_T)$ in the closed rectangle with these half-widths. Give source $10$ conditional biases $(b_C,b_T)=(e_C,e_T)/(2\delta)$ and give $01$ their negatives. At each source take a point mass shifted from its ideal reading by
$$
 \left(\frac{b_Cd^2}{2c^2},\frac{b_Cd^2}{2c^2},-db_T,+db_T\right).
$$
This stays in the support box and gives exactly the required biases in $C,T$. Use zero shifts at the other labels. The resulting normalized source-only kernel also serves the cut, whose readout setting contrast stays zero. The construction includes zero-width boxes.

Write $[k_-,k_+]=[1,1]$ or $[1/2,3/2]$ for the chosen class. For observed **population** contrasts $(u,v)$, the sharp joint parameter set is
$$
 \left\{(\theta,\beta,k):
 \begin{array}{l}
 0<\theta\leq\theta_{\max},\quad 1/2\leq\beta\leq3/2,\quad k_-\leq k\leq k_+,\\
 |u+\alpha\theta|\leq h_C,\qquad |v+\gamma\theta k\beta|\leq h_T
 \end{array}\right\}.                                                        \tag{6}
$$
Necessity follows from (1)–(5). For sufficiency take $e_C=u+\alpha\theta$, $e_T=v+\gamma\theta k\beta$ in the construction above. It realizes exactly the observed pair with one shared source scale and one matched kernel. If cut setting contrasts are also supplied under this model, both must be zero. Further aspects of a specified joint law impose additional requirements, including its native cell masses, conditional readout distributions and support. Equation (6) answers the two-mean question.

### An explicit test for any proposed response

Form four numbers from the readings,
$$
 c_- =\frac{-u-h_C}{\alpha},\quad c_+=\frac{-u+h_C}{\alpha},\qquad
 t_- =\frac{-v-h_T}{\gamma},\quad t_+=\frac{-v+h_T}{\gamma}.
$$
For any allowed product interval $[p_-,p_+]$ with $0<p_-\leq p_+$, define
$$
 L=\max\{0,c_-,t_-/p_+\},\qquad
 U=\min\{\theta_{\max},c_+,t_+/p_-\}.                                    \tag{7}
$$
Call this interval **feasible** exactly when $U>0$ and $L\leq U$. The allowed source strengths are then $[L,U]\cap(0,\infty)$. Indeed, a positive $\theta$ has to belong to $[c_-,c_+]$. Its possible values of $\theta q$ span $[\theta p_-,\theta p_+]$. That interval meets $[t_-,t_+]$ exactly when $\theta p_+\geq t_-$ and $\theta p_-\leq t_+$, which proves (7). No division by an observed contrast occurs.

| Population question | Product interval to use in (7) |
| --- | --- |
| Does any member of the calibration class fit? | $[k_-/2,\,3k_+/2]$ |
| Is a specified $\beta_0\in[1/2,3/2]$ possible? | $[\beta_0k_-,\,\beta_0k_+]$ |
| Is unit response possible? | $[k_-,k_+]$ |

Every product in each listed interval is attainable by admissible factors. The middle row gives the exact projection of (6) onto $\beta$ in both classes. For a feasible $\beta_0,\theta$, the allowed gains are exactly
$$
 [k_-,k_+]\ \cap\ [t_-/(\theta\beta_0),\ t_+/(\theta\beta_0)].
$$
In particular the calibrated membership test uses $p_-=p_+=\beta_0$. A positive point of contact $U=L$ is attained, including at $\theta_{\max}$. If $U=0$, there is no admissible source. For example $u=h_C$ would require $\theta\leq0$, even if the motion interval touches the zero-source limit.

If the first row fails, the observed pair rejects the combined response and error model, leaving attribution to $\beta$ unresolved. If the class fits, failure of the unit-response row excludes $\beta=1$ under the chosen gain and error bounds. If that row fits, unit response is compatible. When another response also fits, the means leave the equality question unresolved. If only unit response fits, the means specify that value within the model.

At every positive source strength the ideal identification in (3) holds. As $\theta\downarrow0$, both ideal contrasts approach zero and the motion separation of two fixed products is $\gamma\theta|q_1-q_2|$. For any fixed $h_T>0$ their motion intervals overlap at sufficiently small positive $\theta$ even at the same known source strength. If both half-widths are positive, the observation $(0,0)$ is attainable for every admissible $\beta$ by a sufficiently small *positive* source. With both widths zero, $(0,0)$ is unattainable. These cases explain the strict positivity test in (7) and the loss of uniform resolving power in the weak-source limit.

## Calibration and physical interpretation

For a point determination of an interior probe response, (3) requires an independent calibration of the gain from physical held-frame position acceleration to its displayed value, relative to the clock and length standards entering $C$ and $T$. A calibration obtained by assuming the same probe has $\beta=1$ would identify only the product again. Independently justified gain bounds can already exclude unit response through (7). Reading $\beta$ as a passive-to-inertial mass ratio additionally requires justification of the prescribed probe force law and its interpretation in the chosen frame.

A physical application requires uniform bounds on the finite source and its stresses, field and relevant derivatives, initial release, nongeodesic force response, frame, clock transfer and instrument calibration over the declared $\theta,\beta,k$ ranges. The geodesic remainders evaluated at unit response do not establish these bounds for the modified force law. The result concerns population means under supplied support bounds. Sampling uncertainty requires its own observation and inference model. The static records supply neither an interpolating source trajectory nor a measurement of the inertial masses of the sources.

## Sources and review

The fixed geometry and response coefficients come from [compensated source endpoints](compensated_source_endpoint_response.md). The [localized source calculation](localized_source_clock_freefall.md) supplies the original held-frame convention. The [finite native record law](finite_source_order_return_and_visibility.md) supplies the witness and its separately defined cut.

Frozen QR proof SHA-256 `ae936aabb14a681a1319b7ec8da14251cda1774b05db47de44cb50c3a82df428`. Independent scientific review SHA-256 `0e77981b650f8b406c57366aa8c93b8557b717699dc5db0c3cc9d430c9410c44`.
