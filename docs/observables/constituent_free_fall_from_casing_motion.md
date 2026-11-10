# Can one casing test equal free fall of two spring-bound constituents?

Yes, on compatible exact records. Subtract the field-off casing displacement from the field-on displacement to obtain $D(t)$. Form $D(2t)-4D(t)$ at $t=h_0$ and at $t=\sqrt2\,h_0$. Both differences vanish exactly when the two constituents have equal passive-to-inertial mass ratios. Either timing pair alone can miss an unequal response. Even the four exact tags have no positive uniform error margin when the spring stiffness is unrestricted.

## What survives the matched subtraction

Let $x$ be the casing position, $y$ the carriage position, and $z=y-x-d$ the spring extension from its fixed equilibrium offset $d$. Write $M=h+g$, $\mu=hg/M$, and $\omega^2=k/\mu>0$. In an applied field $a$ the equations are
$$
 h\ddot x=kz+ah\beta_h,\qquad g\ddot y=-kz+ag\beta_g .
$$
The two preparations have the same $h,g,k,d$ and identical initial positions and velocities in a common inertial frame. One has $a=a_0\ne0$ for $t\ge0$, the other $a=0$. There is no switching impulse. Denote field-on minus field-off differences by brackets $[\,\cdot\,]$. Since $[x(0)]=0$, the observed displacement contrast $D(t)$ also equals $[x(t)]$.

Set $R=(hx+gy)/M$, $\bar\beta=(h\beta_h+g\beta_g)/M$ and $\delta=\beta_h-\beta_g$. Adding and subtracting the equations of motion gives
$$
 [\ddot R]=a_0\bar\beta,\qquad
 [\ddot z]+\omega^2[z]=-a_0\delta.
$$
Both contrasts and their first derivatives start at zero. Thus $[R]=a_0\bar\beta\,t^2/2$ and $[z]=-a_0\delta(1-\cos\omega t)/\omega^2$. Using $x=R-(g/M)(z+d)$ gives the observable
$$
 D(t)=\tfrac12 a_0\bar\beta\,t^2+C(1-\cos\omega t),\qquad
 C=\frac{a_0g\,\delta}{M\omega^2}. \tag{1}
$$
The centre-of-mass acceleration is present even for equal ratios. The second term is the casing’s share of the relative motion driven by unequal ratios. Matched subtraction cancels any pre-existing free vibration, including its unknown phase. As a sign check, (1) gives $D''(0)=a_0\beta_h$.

## One timing pair has blind frequencies. The two pairs share none.

For a positive dwell $t$, the doubling of time multiplies the bulk displacement by four. The signed residual is
$$
 Q(t)=D(2t)-4D(t)
     =-2C(1-\cos\omega t)^2. \tag{2}
$$
If $\delta\ne0$, then $C\ne0$, and $Q(t)=0$ exactly at $\omega t=2\pi n$ for positive integers $n$. At such times both original readings in the pair agree with the purely quadratic response, so the cancellation hides all evidence of the composition difference in that pair.

For a concrete collision on the shorter record, choose $h=g=m>0$ and $k=(m/2)(2\pi/h_0)^2$. Start both arms at rest with $z=0$ and use the same casing origin, offset, field and time standard. Compare $(\beta_h,\beta_g)=(1,1)$ with $(3/2,1/2)$. Both worlds have $\bar\beta=1$ and the same positive stiffness. At $h_0,2h_0$ both give the full signed contrast pair $(a_0h_0^2/2,\,2a_0h_0^2)$. In the second world the relative mode is excited between the tags and returns to its initial extension and velocity at each tag.

Put $t_1=h_0$ and $t_2=\sqrt2\,h_0$. If unequal ratios hid at both pairs, one would have $\omega t_1=2\pi n$ and $\omega t_2=2\pi m'$ for positive integers $n,m'$. This would give $\sqrt2=m'/n$. Hence, on the model domain,
$$
 \boxed{\ \beta_h=\beta_g\quad\Longleftrightarrow\quad Q(t_1)=Q(t_2)=0.\ } \tag{3}
$$
One nonzero residual establishes inequality. Its sign also gives the sign of $-a_0\delta$. For raw data of unknown compatibility, an equal-ratio explanation requires all four values $2D(t)/(a_0t^2)$ to equal the same positive constant. That condition is also sufficient for an equal-ratio explanation by (1). In particular, two zero residuals accompanied by inconsistent quadratic amplitudes between pairs reject the stipulated model. They do not establish equality on such data.

## A fixed composition difference can produce arbitrarily close records

Fix $h,g$ and a positive $\bar\beta$. Fix any nonzero $\delta$ for which $\beta_h=\bar\beta+(g/M)\delta$ and $\beta_g=\bar\beta-(h/M)\delta$ are both positive. Compare that world with one having both ratios equal to $\bar\beta$. For each choice of $\omega$, give both worlds the same stiffness $\mu\omega^2$ and the same unstrained, stationary initial preparation. The difference of their true casing contrasts satisfies
$$
 \left|D_{\ne}(t)-D_{=}(t)\right|
 \le \frac{2|a_0|g|\delta|}{M\omega^2}
 \quad\text{for every }t\ge0. \tag{4}
$$
For example, take $\omega_n=2\pi n/h_0$. At every finite $n$ the first pair agrees exactly, and the second pair distinguishes the worlds by (3). Nevertheless their maximum difference over all four tags tends to zero as $n$ increases. All stiffnesses used are finite and positive. This comparison holds the actual constituent inertias, mean ratio and nonzero ratio difference fixed.

For any absolute contrast-error allowance $\eta>0$, choose $\omega$ so that the right side of (4) is less than $2\eta$. The coordinatewise midpoint of the two four-tag records is then admissible under either world. If errors are assigned per raw casing position, the off-field trajectory in this construction is identical in both worlds, so the same midpoint argument applies to the on-field readings alone. Thus the infimum separation is zero although an exact four-tag collision between equal and unequal ratios is impossible. For an individual observed record with contrast errors bounded by $\eta$, a measured $|Q(t)|>5\eta$ still certifies inequality, because the two contrast errors enter (2) with coefficients $1,-4$. This supplies no uniform guarantee of detecting the fixed difference.

## Energy, units and scope

The spring forces and the field act on both constituents in the equations used above. For the field-on arm, define mechanical energy as the two kinetic energies plus $kz^2/2$. Its change over the dwell is the external work
$$
 E_{\rm mech}(t)-E_{\rm mech}(0)
 =a_0\!\left[h\beta_h(x(t)-x(0))+g\beta_g(y(t)-y(0))\right].
$$
The field-off arm conserves mechanical energy. For the initially unstrained, stationary example, the on-field relative kinetic plus spring energy is $\mu(a_0\delta)^2(1-\cos\omega t)/\omega^2$. It is positive between returns when the mode is moving or strained. The work and initial-state matching are physical premises. Switching without an impulse preserves the initial velocities.

The quantities $D,Q,C,\eta$ have units of length, $h_0$ is a time, $\omega$ is an angular frequency and $a_0$ is a signed acceleration. Exact nulls need a shared displacement scale, registered direction and frame, matched releases, a uniform constant drive, and the two exact time ratios. Interpreting (3) as a statement about material masses requires the supplied force law, one stable linear spring mode, and freedom from tides, supports, damping or other differential forces. A numerical common ratio in the equal case also uses the calibrated magnitude of $a_0$, time and length. The test concerns these two constituents. Their common ratio need not be one, and the readings supply no independent absolute inertial mass or DET-native acceleration standard.
