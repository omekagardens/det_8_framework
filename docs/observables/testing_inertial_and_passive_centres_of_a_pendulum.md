# Testing whether a pendulum’s passive and inertial centres coincide

In an inertial laboratory with a uniform field, two equal axial angular impulses measure an inertia ratio without using gravitational torque. Together with two horizontal-pivot periods, this gives the distance to the passive centre. The third period then separates the inertial centre, radius of gyration and effective gravity. All four quantities are unique for every admissible record. The three periods alone can agree exactly for a pendulum with coincident centres and one with displaced centres.

## Five readings on one body

Let $M>0$ be total inertial mass, $P>0$ total passive mass, $g>0$ the prescribed uniform field strength in the inertial lab, and $G_p=(P/M)g$. Positions along the given common ray are measured from pivot 0. Pivots 1 and 2 lie at $-d,-2d$ for $d>0$. Define
$$
 x=s_I/d>0,\qquad p=s_P/d>0,\qquad v=k^2/d^2>0,\qquad N_j=(x+j)^2+v.
$$
Here $Mk^2$ is the central moment about the axis parallel to the bearings through the inertial centre. For an unchanged body, the parallel-axis theorem gives $I_j=Md^2N_j$. In a uniform field the resultant force $Pg$ acts at the passive centre with lever arm $d(p+j)$. The pendulum hangs with this arm pointing down. The rotor inertia depends on $x$, while the restoring torque depends on $p$. The common-centre CL094 result corresponds to $p=x$. [Three-pivot acceleration reference](effective_acceleration_from_three_pivot_periods.md)

At each horizontal pivot release the body from rest at the same angle $0<\theta_*<\pi$ from stable equilibrium. The angular-momentum balance about the bearing gives the equation of motion. Integrating from the release point gives the second relation below.
$$
 I_j\ddot\theta=-Pg\,d(p+j)\sin\theta,\qquad
 \tfrac12 I_j\dot\theta^2=Pg\,d(p+j)(\cos\theta-\cos\theta_*).
$$
The first full return to the release extremum at rest has four equal quarter cycles. Substituting $\sin(\theta/2)=q\sin\phi$ with $q=\sin(\theta_*/2)$ in the time integral gives
$$
 F=4\int_0^{\pi/2}\frac{d\phi}{\sqrt{1-q^2\sin^2\phi}},\qquad
 y_j=\left(\frac{T_j}{F}\right)^2
     =\tau\,\frac{N_j}{p+j},\qquad \tau=\frac{d}{G_p}>0. \tag{1}
$$
This is the finite-amplitude full period for a rigid body with two distinct centre coordinates.

For the two impulse measurements, reorient the body and selected bearing together so the rotation axis is vertical. The uniform field has zero torque component about that axis throughout the trial. The fixed bearing may exert transverse reactions and transmits zero axial torque. With the body initially at rest, an applied pure axial torque of signed finite nonzero impulse $L=\int\Gamma\,dt$ gives $I_j\omega_j=L$, exactly for a finite pulse. Choose consistent signed axes. The two final speed readings are $w_j=b\,L/I_j$ at $j=0,1$ with one positive gain $b$ and a calibrated zero. Thus
$$
 r=\frac{w_0}{w_1}=\frac{I_1}{I_0}=\frac{N_1}{N_0}>1. \tag{2}
$$
The strict inequality follows from $N_1-N_0=2x+1>0$. Equality of the signed impulses and the common speed gain are independent physical registrations.

## Sharp data test and inverse

Require the three labelled $T_j$ to be finite and strictly positive and the two $w_j$ to be finite, nonzero and of the registered impulse sign. Use the following strict tests and formulas.

1. Compute $r$ from (2). Require $r>1$ and $r y_0>y_1$. In (1) the ratio of the first two squared periods is $y_1/y_0=r p/(p+1)$. Therefore the only candidate passive offset is
   $$
   p=\frac{y_1}{r y_0-y_1}.
   $$
2. Form $U_j=(p+j)y_j$. They satisfy $U_j=\tau[(x+j)^2+v]$. The second difference fixes $\tau$, the first fixes $x$, and the first reading fixes $v$.
   $$
   \tau=\tfrac12(U_2-2U_1+U_0),\qquad
   x=\tfrac12\left(\frac{U_1-U_0}{\tau}-1\right),\qquad
   v=\frac{U_0}{\tau}-x^2.
   $$
   Require $\tau>0$ before dividing, then $x>0$ and $v>0$.
3. On a passing record return
   $$
   s_I=dx,\qquad s_P=dp,\qquad k=d\sqrt v,\qquad G_p=d/\tau .
   $$
   **The centres coincide exactly when $x=p$.** Equivalently, $U_1-U_0=\tau(2p+1)$. In a passing displaced-centre record the signed separation is $d(p-x)$, and the same inverse still returns $G_p$.

All tests use the raw labelled trials without requiring monotone or distinct periods. A failed test has no realization under the full premises. To verify sufficiency, the quadratic reconstructed from $U_0$, its first increment and its second difference gives all three $U_j$ exactly. Dividing by $p+j$ reproduces every $y_j$ and its positive period. The fitted ratio $U_1/U_0=r$ reproduces the two speed readings. Choose any $M>0$ and $b>0$, set $L=w_0 Md^2N_0/b$, and use this same signed impulse in the second trial. Choose any $g>0$ and set $P=MG_p/g$. No other positive parameter branch can change a centre, the central squared radius or the effective acceleration.

## Realization with positive constituent masses

For any passing record put $\Delta=s_P-s_I$. Place two sites at $s_I-\ell$ and $s_I+h$, where $\ell,h>0$, $\ell h=k^2$ and $-\ell<\Delta<h$. Such sites always exist. If $\Delta\ge0$, take $h>\Delta$ and $\ell=k^2/h$. If $\Delta<0$, take $\ell>-\Delta$ and $h=k^2/\ell$. The permitted light frame can span the chosen sites and all three bearings.

The left and right inertial mass fractions are $h/(\ell+h)$ and $\ell/(\ell+h)$. They give centre $s_I$ and central second moment per unit mass $\ell h=k^2$. Give the same sites passive fractions $(h-\Delta)/(\ell+h)$ and $(\ell+\Delta)/(\ell+h)$. They are strictly positive and sum to one. Their first moment gives $s_P$. Fix these weights throughout all five preparations. Rotation about a reoriented bearing uses the same body-fixed axial inertia. This realizes the common geometry, both positive mass distributions, the periods and the paired impulses on a single body. Equality of the two centres constrains a first moment; sitewise proportionality in a general composite requires further observations. [Passive mass at registered material sites](site_passive_masses_from_tidal_torque.md)

## Why three periods alone cannot certify coincidence

Hold $d$, the physical field $g$, release angle and clock fixed. Use the same three material sites at coordinates $0,d,4d$ on the same bearing layout and the same total inertial mass in both worlds. The table uses mass fractions at those sites in that order.

| World | Inertial fractions | Passive fractions | $P/M$ | $(x,p,v)$ | $(y_0,y_1,y_2)/(d/g)$ | $w_0/w_1$ |
|---|---|---|---:|---|---|---:|
| A | $(1/4,\,2/3,\,1/12)$ | $(1/4,\,2/3,\,1/12)$ | $1$ | $(1,1,1)$ | $(2,5/2,10/3)$ | $5/2$ |
| B | $(51/84,\,16/84,\,17/84)$ | $(1/8,\,1/2,\,3/8)$ | $6/7$ | $(1,2,17/7)$ | $(2,5/2,10/3)$ | $15/8$ |

For example, in B the inertial mean is $(16+4\cdot17)/84=1$ in units of $d$, and the variance is $(51+9\cdot17)/84=17/7$. The passive mean is $1/2+4(3/8)=2$. In B, $N_j=(24,45,80)/7$ and $\tau=7d/(6g)$. Equation (1) therefore gives the same three full periods as in A despite the different passive centre and effective gravity. The distinct speed ratios in the last column resolve the ambiguity.

## Units, work and limits

The geometry ratios $s_I/d$, $s_P/d$, $k/d$ and all $I_j/(Md^2)=N_j$ use only squared-period ratios and the speed ratio. Multiplying all $y_j$ by a common factor multiplies $\tau$ by that factor and preserves the geometry. With the common angle one also gets the dimensionless acceleration $G_pT_0^2/d=F^2N_0/p$. The registered spacing and clock convert lengths and $G_p$ to physical units. Even on a coincident-centre record the field $g$ and the coupling $P/M$ enter only as the product $G_p$. The full family $M>0$, $g>0$, $P=MG_p/g$, $I_{\rm centre}=Mk^2$ preserves the five readings when $bL/M$ is held fixed. A reference coupling or independently calibrated field is needed to separate them.

Relative to hanging equilibrium, a horizontal trial starts with stored energy $E_j=Pg\,d(p+j)(1-\cos\theta_*)$. The ideal fixed bearing does no work and at the bottom all of $E_j$ is rotational kinetic energy. The specific swing energy $E_j/M=G_p d(p+j)(1-\cos\theta_*)$ is determined with registered length, clock and angle. Absolute swing energy still scales with $M$. Each vertical pulse delivers $W_j=L^2/(2I_j)$ from rest; gravity does zero axial work. Thus $W_0/W_1=r$. The unknown absolute impulse and speed gain leave the individual pulse energies per unit mass undetermined as well. Changing the speed gain and inversely changing the impulse at fixed body reproduces both speed displays.

The calculation requires unchanged bearing locations and mass distributions, a registered inertial lab and uniform field, frictionless axes, the same finite release angle, first-return timing, fresh rest preparations, true axial impulse equality, and common signed speed readout. Remounting and reorienting the fixture, preparing each release, delivering and recovering the impulse energy, damping or reversing residual motion, timing, readout and restoration all need physical resources. The measurements contain no complete work ledger for those operations. The result is a conditional mechanical test on this body. It supplies neither a universal passive coupling nor an absolute mass, action or native DET clock.
