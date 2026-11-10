# Mass radiated through two spheres from four uncalibrated readings

Two sphere-integrated local energy readings and two endpoint clock transfers determine the initial and final Bondi mass in units of the inner areal radius. The two channels can have different unknown positive gains. Each gain must be common to its own pair. The result identifies the fraction of gravitational mass radiated through the exterior, including complete mass loss. It needs neither the pulse profile nor a model for how an inertial load contributes to the source mass.

## What each fixed-radius station measures

Use geometrized lengths $x$ (retarded time), $r$ (areal radius) and $m(x)=GM_B(x)/c^2$. In the stipulated outgoing Vaidya exterior,
$$
 ds^2=-f\,dx^2-2\,dx\,dr+r^2d\Omega^2,\qquad
 f=1-\frac{2m(x)}r,\qquad T_{xx}=-\frac{m'(x)}{4\pi r^2}.
$$
This is the only nonzero covariant stress component. The smooth mass function is nonincreasing, constant in the two endpoint epochs, and $0\le 2m_f/R<2m_i/R<1$. Both stations remain timelike. This uses the pure outward spherical radiation law. [Mann, Nagle and Terno, v1, exterior metric convention](https://arxiv.org/pdf/1801.01981v1)

At constant $r$, a future unit tangent and the outward spacelike unit normal in the local rest frame have components
$$
 U=(f^{-1/2},0),\qquad n=(-f^{-1/2},\sqrt f)
$$
in $(x,r)$. Their norms are $-1,+1$, their inner product vanishes, and $n^r>0$. The positive outward local energy flux is $-T_{\mu\nu}U^\mu n^\nu=-m'/(4\pi r^2 f)$. The sphere has area $4\pi r^2$ and the station's proper time in length units is $c\,d\tau=\sqrt f\,dx$. Thus its complete sphere-integrated energy in joules is
$$
 \mathcal E_r=\frac{c^4}{G}\int\frac{-m'(x)}{\sqrt{1-2m(x)/r}}\,dx
 =\frac{c^4}{G}\,r\,\big[\sqrt{1-2m_f/r}-\sqrt{1-2m_i/r}\big]. \tag{1}
$$
The integral is an exact endpoint difference since $d(r\sqrt f)/dx=-m'/\sqrt f$. A pause in emission contributes zero. The displayed readings are $H_R=g_E\mathcal E_R,\ H_{2R}=g_E\mathcal E_{2R}$, for a common unknown $g_E>0$. The area factor is essential because each reading counts energy over its whole sphere.

At infinity the emitted energy is $\mathcal E_\infty=(c^4/G)(m_i-m_f)$. Rationalizing (1) yields
$$
 \frac{\mathcal E_\infty}{\mathcal E_r}
 =\frac{\sqrt{1-2m_i/r}+\sqrt{1-2m_f/r}}{2}.
$$
For a genuine burst at finite $r$ this conversion is strictly between the two endpoint lapse factors. Multiplying the whole received energy by either single endpoint redshift gives an incorrect total. The two meters register the same outgoing transfer in different local frames; their readings must not be added as separate losses.

## What the two clock transfers measure

Write $X_j=2m_j/R$ for $j=i,f$, and let $D_j$ be the displayed frequency ratio received at $2R$ divided by emitted at $R$ for a signal wholly inside static epoch $j$. The endpoint Schwarzschild lapse gives
$$
 D_j=g_C\sqrt{\frac{1-X_j}{1-X_j/2}},\qquad g_C>0 .
$$
No time-translation invariance across the burst enters this step. The clock gain is shared between epochs and independent of the calorimeter gain. [Schwarzschild, English translation v1, Eq. (14)](https://arxiv.org/pdf/physics/9905030v1)

## Exact inverse and sharp record domain

Start with four finite, strictly positive raw readings. Form
$$
 B=H_R/H_{2R},\qquad C=D_i/D_f .
$$
Introduce dimensionless positive parameters $s,t$ by
$$
 \sqrt{1-X_i}=\sinh s,\qquad \sqrt{1-X_f}=\sinh t,\qquad
 0<s<t\le L:=\operatorname{arsinh}1 .
$$
The outer-sphere lapse roots are then $\cosh s/\sqrt2,\cosh t/\sqrt2$. Put $h=(s+t)/2,\ k=(t-s)/2$. Equation (1) and the two clock transfers give
$$
 B=\frac{\sinh t-\sinh s}{\sqrt2(\cosh t-\cosh s)}
   =\frac{\coth h}{\sqrt2},\qquad
 C=\frac{\tanh s}{\tanh t},\qquad
 \frac{1-C}{1+C}=\frac{\sinh(2k)}{\sinh(2h)} .
$$
Thus the fluences fix the mean $h$; the clocks fix the separation $k$.

1. Require $B>1$ and $0<C<1$. Compute
   $$
   h=\operatorname{arccoth}(\sqrt2 B),\qquad
   k=\tfrac12\operatorname{arsinh}\!\left(\sinh(2h)\frac{1-C}{1+C}\right),
   $$
   taking the positive real inverse branches.
2. Require $h+k\le L$. These are the complete ratio constraints. Indeed $B>1$ gives $0<h<L$, while $0<C<1$ gives $0<k<h$. Consequently $s=h-k>0$ and $t=h+k$ meet the entire endpoint domain. Equality $h+k=L$ is allowed and means zero final mass. An initial horizon and a zero burst are excluded.
3. Return the unique endpoints and loss fraction
   $$
   X_i=1-\sinh^2(h-k),\qquad X_f=1-\sinh^2(h+k),\qquad
   \boxed{\frac{M_{B,i}-M_{B,f}}{M_{B,i}}=1-\frac{X_f}{X_i}} .
   $$
   Equivalently $GM_{B,j}/(Rc^2)=X_j/2$. The fraction is in $(0,1]$ and has positive denominator even when the final mass is zero.

To verify sufficiency for the *raw* record, choose any $R>0$ consistent with the relative radius registration, and set $m_i=RX_i/2,\ m_f=RX_f/2$. For example, integrate a smooth nonnegative bump of unit integral in $x$ from the past up to $x$; multiplying its cumulative integral by $m_i-m_f$ and subtracting from $m_i$ yields a smooth admissible history with static endpoint epochs. Choose $g_E=H_R/\mathcal E_R$ and $g_C=D_i\sqrt{(1-X_i/2)/(1-X_i)}$. Both are finite and positive. The two ratio equations then reproduce the remaining two raw readings. Thus a failed check has no compatible world, and no profile or gain branch can change the inferred dimensionless endpoints on a passing record.

## What either channel misses

**Fluences alone.** Fix any admissible $B>1$. It fixes $h$, while $k$ can vary over $0<k<h$ with $h+k\le L$. Taking $k\downarrow0$ sends the loss fraction to zero; each allowed positive $k$ has strictly positive loss. Hence even the fraction varies for the same $B$. For every such choice a positive gain fits the first raw fluence and the ratio fits the second.

**Static clocks alone.** Fix $0<C<1$. For any $0<t\le L$ take $s=\operatorname{artanh}(C\tanh t)$, so $0<s<t$. Adjust the positive gain to one raw clock reading; the other is unchanged. The loss fraction tends to zero as $t\downarrow0$ and equals one at $t=L$. By continuity every fraction in $(0,1]$ is possible for the same two raw clock readings.

## Scale, frame and observation requirements

With $R$ in physical length units and the physical conversion constants, $M_{B,j}=c^2R X_j/(2G)$ in kilograms and $\mathcal E_\infty=c^4R(X_i-X_f)/(2G)$ in joules. Alternatively, an absolute energy calibration at either station gives $\mathcal E_\infty$ from (1) and the mean lapse factor; the measured fraction and $c^2$ then give both endpoint masses. With neither standard, the clock gain follows from the dimensionless fit, but the fluence scale contains the product $g_E c^4R/G$. Scaling $R,m_i,m_f$ together by any positive factor and dividing $g_E$ by it preserves all four readings and changes both dimensional masses and the emitted energy.

A physical implementation requires supported fixed-area stations, registered local frames, full angular and temporal coverage of the outward flux, stable gains, and test signals that propagate entirely within the settled endpoint epochs. Nondepleting meters or separately registered identical repetitions are required for two readings of the same emission. Incoming energy, missed radiation or angular structure would change the inference. The observations do not reconstruct the burst duration, luminosity profile, mechanism or support work. This calculation concerns asymptotic gravitational mass loss in a supplied radiating exterior. It uses neither a microscopic energy sink, a material shell-crossing law, a closed cavity stress ledger nor a DET-derived mass unit.
