# Weighing a freely vibrating target from six casing positions

**Result.** Every compatible complete record gives one positive total mass. In the prescribed five-position prefix the same passive reference-cart readings and target positions admit total masses $2m_*$ and $3m_*/2$. Their sixth positions are $\ell$ and $2\ell$, respectively, with $\ell=v_0\Delta$.

## Observation and mechanics

The full record has eight labeled scalars, the two signed reference velocities $u,v$ and six signed casing positions $x_0,\ldots,x_5$. The prefix has seven, dropping only $x_5$. The tag $x_0$ is the single continuous position at impact. Reject missing, extra, duplicate, mistimed or misassigned labels, nonfinite or nonreal values, and readings outside the registered controls. In particular $u=-v_0,\ v=-2v_0$, with supplied finite $m_*,v_0,\Delta>0$, finite equilibrium offset $d$, and tags at $j\Delta$. All signed velocities, positions, times and the zero incoming target momentum refer to one inertial frame and the stipulated common ruler and clock.

Write $x,y$ for casing and carriage position, $h,g$ for their positive masses, $M=h+g$, $\mu=hg/M$, $R=(hx+gy)/M$, and $z=y-x-d$. The potential is $kz^2/2$. The casing receives $+J=m_*(u-v)=m_*v_0$. The carriage velocity and both positions are continuous. After the impulse the internal forces $+kz,-kz$ give
$$
 R(t)=R(0)+Vt,\quad V=J/M,\qquad
 \ddot z+\omega^2 z=0,\quad \omega^2=k/\mu .
$$
Since $x=R-(g/M)(d+z)$, the free casing motion has the form
$$
 x(t)=a+Vt+A\cos(\omega t)+B\sin(\omega t).
$$
Here $a$ is the intercept of the translating equilibrium casing position. The phase and amplitude include any internal motion already present at impact.

## Exact membership test and drift

Write $p_j=x_{j+1}-x_j$ for $0\leq j\leq4$, $q_j=p_{j+1}-p_j$ for $0\leq j\leq3$, $b=V\Delta$ and $c=\cos(\omega\Delta)$. The following test uses only exact arithmetic and trigonometric identities.

1. If every $q_j=0$, set $b=p_0$. Reject unless $b>0$. A translating solution realizes these tags. A sampled constant mode ($\omega\Delta=2n\pi,\ n\geq1$), a vanished mode or a vibration invisible at the tags can also give a straight record. For $c=1$ the sampled harmonic is constant, hence the measured increment is $b$. For every $c\ne1$ the drift identity below also yields $b=p_0$. This includes a two-phase oscillation whose visible alternating coefficient vanishes.
2. Otherwise a physical mode must obey $q_{j+2}+q_j=2c q_{j+1}$ for $j=0,1$, by taking twice the forward difference of the sampled position. If $q_1=q_2=0$, the two equations force $q_0=q_3=0$, so reject this nonaffine branch. Use either available nonzero middle value $q_{j+1}$ to form $c=(q_{j+2}+q_j)/(2q_{j+1})$. Check both equations and require $-1\le c<1$. A nonaffine record cannot come from $c=1$, even if a formal repeated-root recurrence accepts its second differences.
3. For the surviving $c$, set
$$
 b=\frac{p_2-2c p_1+p_0}{2(1-c)},\qquad
 a=\frac{x_2-2c x_1+x_0}{2(1-c)}-b,\qquad A=x_0-a .
$$
Reject unless $b>0$. The filter $f_{j+2}-2cf_{j+1}+f_j$ annihilates the harmonic and maps $a+bj$ to $2(1-c)(a+b(j+1))$. Applied to $p_j$ it gives $2(1-c)b$, independent of index by the two checked $q$-equations. A compatible nonaffine record thus has only this $c$ and this drift.
4. For $-1<c<1$ take $\theta=\arccos c$ and $B=(x_1-a-b-Ac)/\sin\theta$. Check all six equalities $x_j=a+bj+A\cos(j\theta)+B\sin(j\theta)$. For $c=-1$ take $\theta=\pi,\ B=0$, and check all six $x_j=a+bj+A(-1)^j$. Reject on any failure. The last check excludes the generalized solution $j(-1)^j$ permitted by a double-root formal recurrence. For $c=1$ the affine branch already excludes spurious polynomial trends.

On every accepted record $V=b/\Delta$ and
$$
 \frac{M}{m_*}=\frac{(u-v)\Delta}{b}=\frac{v_0\Delta}{b}.
$$
Positive finite $b,\Delta,J$ give positive finite $M$. The derivation proves necessity and uniqueness of the drift. The construction below proves that all accepted records, including the affine and alternating ones, are achievable with the specified elastic impact.

## Constructing the impact and target

In the affine case set $a=x_0,\ A=B=0,\ \theta=2\pi$. In the interior-frequency case, if $B<0$ replace $(\theta,B)$ by $(2\pi-\theta,-B)$. At the integer tags that replacement preserves both harmonic terms. With these choices, including the $c=-1$ choice above, $\omega=\theta/\Delta>0$ and the outgoing casing speed $w_+=V+\omega B$ is at least $V$. This choice uses the allowed frequency aliases. It imposes no frequency band on the target.

Restitution requires $w_++w_-=u+v=-3v_0$ and impulse balance requires $h(w_+-w_-)=J$. Choose
$$
 h=\frac{J}{2w_++3v_0},\quad g=M-h,\quad
 w_-=-3v_0-w_+,\quad k=\mu\omega^2 .
$$
Since $2w_++3v_0>V=J/M>0$, $0<h<M$ and $g,k>0$. Take $H(t)=A\cos(\omega t)+B\sin(\omega t)$ and set
$$
 x=a+Vt+H,\qquad y=a+Vt+d-(h/g)H.
$$
These positions yield $R=a+Vt+(g/M)d$, $z=-(M/g)H$, and solve the two free equations of motion. Keep $\dot y$ and both positions continuous at impact and use casing speed $w_-$ immediately before. The outgoing target momentum is $MV=J$. Removing $h(w_+-w_-)=J$ gives incoming target momentum zero. Free backward evolution locally from that incoming state gives finite initial data for both bodies.

For a cart on the left the signed relative approach speed is $u-w_-=(1+m_*/h)v_0/2>0$; the separation speed $w_+-v$ equals it. Reference momentum loss equals $J$. The casing kinetic-energy change is $J(w_++w_-)/2=-3m_*v_0^2/2$, exactly opposite the reference gain $m_*(v^2-u^2)/2$. Carriage kinetic and spring potential energies are continuous through the impulse. All energies are finite. The reference can acquire energy from internal target motion even with zero incoming target momentum. The stipulated port disengages after impact with zero longitudinal impulse and energy transfer, leaving one free target trajectory and exactly one contact. Relative separation at the event and that supplied disengagement are both used.

## Two complete histories for the five-tag prefix

Use units $(\ell,\Delta,m_*)=(1,1,1)$, so $u=-1,\ v=-2,\ J=1$. Let $s=t/\Delta-2$ and $X=x/\ell=b s+D\sin(\theta s)$, where here $b,D$ are dimensionless. The odd form gives the middle tag zero. The two positive-side tags require $b+D\sin\theta=1$ and $2b+D\sin(2\theta)=1$, hence $b=(1-2\cos\theta)/(2(1-\cos\theta))$. Evaluation gives the following exact histories.

| Quantity | History I | History II |
|---|---:|---:|
| $\theta$ | $\pi/2$ | $2\pi/3$ |
| $b,\ D$ | $1/2,\ 1/2$ | $2/3,\ 2/(3\sqrt3)$ |
| $X(-2),X(-1),X(0),X(1),X(2)$ on the $s$ clock | $(-1,-1,0,1,1)$ | $(-1,-1,0,1,1)$ |
| Sixth tag $X(3)$ | $1$ | $2$ |
| $M=1/b$ | $2$ | $3/2$ |
| $w=b+D\theta\cos(2\theta)$ just after impact | $1/2-\pi/4$ | $2/3-2\pi/(9\sqrt3)$ |
| $h=1/(2w+3)$ | $1/(4-\pi/2)$ | $1/(13/3-4\pi/(9\sqrt3))$ |
| $g=M-h$ | $2-1/(4-\pi/2)$ | $3/2-1/(13/3-4\pi/(9\sqrt3))$ |

The two denominators $2w+3$ exceed $1/M=b$. Indeed $\pi<4$ gives a lower bound of $2$ in I and, using $\sqrt3>1$, $23/9$ in II. Thus both mass splits are physical. Each history uses $Y=y/\ell=b s+d/\ell-(h/g)D\sin(\theta s)$, reduced mass $\mu=hg/M$, and spring stiffness $k=\mu\theta^2$ in the chosen units. This fixes the hidden positions and velocities on the entire post-impact interval. With $Z=Y-X-d/\ell$, the two contact strains at $s=-2$ are $0$ in I and $-M/(3g)$ in II; spring force and energy are finite in both.

For each column use incoming casing speed $w_-=-3-w$, retain carriage speed $p=(1-hw)/g$ at the contact, and extend the unforced incoming target motion to the left of that time. The explicit column values of $w,h$ give $h(w-w_-)=h(2w+3)=1$, $hw+gp=1$, and $hw_-+gp=0$. The reference momentum changes from $-1$ to $-2$. Incoming relative speed $-1-w_-=2+w$ equals outgoing relative speed $w-(-2)=2+w=(1+1/h)/2>0$ in both columns. The cart starts on the left locally and the supplied test-port removal isolates the target thereafter.

In these units the target energy immediately after contact is
$$
 E_+=\tfrac12 M b^2+\frac{hM}{2g}D^2\theta^2 .
$$
This follows by summing the two kinetic energies and $\mu\theta^2 Z^2/2$; it remains constant throughout the six tags. It equals $1/4+hM\pi^2/(32g)$ in I and $1/3+8hM\pi^2/(243g)$ in II, using the respective masses. The pre-impact spring and carriage energies are the same as at $0^+$. The casing energy difference is $h(w^2-w_-^2)/2=(w+w_-)/2=-3/2$ in both worlds. Thus the initially stationary centre of mass coexists with internal incoming energy $E_-=E_++3/2$; the complete pre/post totals including the reference are $E_-+1/2=E_++2$. The signed approach and separation, elastic law, and energy transfer hold for the actual phases in the table without changing either trajectory.

## Interpretation and provenance

The two histories establish failure of universal five-tag identification for this nested schedule and observable. Six tags on that same event identify the total inertia under the supplied premises. The inverse neither requires nor generally recovers a unique constituent inertia, frequency, or internal energy. For example an affine record permits an invisible $B\sin(2\pi t/\Delta)$ with arbitrary positive $B$ and a corresponding change in $h$. For the same registered ruler/clock, $v_0\Delta/b$ is dimensionless. An absolute total mass uses the external calibration of $m_*$; a common positive scaling of both target masses, $m_*$, and $k$ preserves these kinematics and the elastic collision. Exact, noiseless identifiability here supplies no practical resolution threshold or native physical mass unit.

The verified dispositions CL015 (calibrated recoil ratios), CL028 (hidden pair energy), CL037 (retained homogeneous motion), and CL071 (sampled harmonic ambiguity and calibration) inform the question. The selection and control specified the five-tag prefix and candidate phases before this proof. The example is a source-informed construction. The mathematics uses one supplied Newtonian channel and a hand-derived feasibility test. No empirical or numerical runs enter the result.

## Use in QR mass comparisons

The QR receiving review adopted this result as a test of whether motion of one visible part identifies the inertia of the whole target. Applying it to a particular carrier requires identifying the same closed package throughout the flight. Applying the ratio to an occupation sector also requires independent sector registration. A gravitational comparison needs its own gravitational observable on the registered carrier. [Same-carrier registration](same_carrier_mass_registration.md) · [Sector inertial-mass ratios](sector_inertial_mass_ratios.md)
