# Six exact recoil positions have zero uniform mass resolution under the energy cap

For the fixed total masses $2m_*$ and $3m_*/2$, the infimum of the maximum difference between their six casing positions is **zero**, even with incoming target energy capped at $2m_*v_0^2$. Both targets can have the same casing position and velocity at release while their centres of mass acquire different drifts. A sufficiently soft positive spring lets those drifts remain arbitrarily hard to see at the casing during the five observed gaps. The exact records remain distinct.

## Two elastic histories within one budget

Use CL083’s one-dimensional Newtonian system in the registered inertial frame. The reference cart of mass $m_*$ has signed velocities $u=-v_0$ and $v=-2v_0$, so the target receives positive impulse $J=m_*v_0$. Let $h$ be the casing mass, $g$ the hidden carriage mass, and $M=h+g$. Give both casings the mass $h=m_*/3$, the same initial position $x_*$, and speeds $w_-=-3v_0$ immediately before impact and $w_+=0$ immediately after it. Put the carriage initially at $y_*=x_*+d$, so the supplied spring offset $d$ gives zero initial strain. Give it speed $J/g$, continuous at impact.

| Quantity | Target 1 | Target 2 |
|---|---|---|
| Total mass $M$ | $2m_*$ | $3m_*/2$ |
| Hidden mass $g$ | $5m_*/3$ | $7m_*/6$ |
| Carriage speed at impact $J/g$ | $3v_0/5$ | $6v_0/7$ |
| Outgoing centre-of-mass speed $V=J/M$ | $v_0/2$ | $2v_0/3$ |
| Incoming target energy in units of $m_*v_0^2$ | $9/5$ | $27/14$ |
| Outgoing target energy in the same units | $3/10$ | $3/7$ |

The incoming target momentum is $hw_-+g(J/g)=-J+J=0$. At contact $h(w_+-w_-)=J$ and both positions are continuous. For the cart approaching from the left, $u-w_-=2v_0>0$ and $w_+-v=2v_0>0$. The relative velocity reverses with equal magnitude. The incoming spring and carriage state has a free backward continuation for a preparation just before approach. The stipulated port disengages with no further longitudinal impulse or work.

Since the incoming centre of mass is at rest, all incoming target energy is internal. Its value is $E_-=J^2/(2h)+J^2/(2g)$, with no spring contribution at contact. This gives the two entries below the cap in the table. At release $E_+=J^2/(2g)$. The loss $J^2/(2h)=3m_*v_0^2/2$ equals the cart’s kinetic energy gain from $m_*v_0^2/2$ to $2m_*v_0^2$. The cart energy is excluded from the stipulated incoming target budget. There is no additional energy supply at impact. [CL083 signed impact and measurement premises](six_casing_positions_and_total_inertial_mass.md)

## The same six times, with arbitrarily close readings

For each positive angular frequency $\omega$, set the spring stiffness in each target to $k=(hg/M)\omega^2>0$. For either mass, the exact free positions after contact are
$$
 x(t)=x_*+V\left(t-\frac{\sin(\omega t)}{\omega}\right),\qquad
 y(t)=x_*+d+V\left(t+\frac{h}{g}\frac{\sin(\omega t)}{\omega}\right).
$$
The strain is $z=y-x-d=(J/g)\sin(\omega t)/\omega$. It satisfies $\ddot z=-\omega^2z$, while the centre of mass drifts at $V$. Evaluation at zero recovers $x_*,y_*$, zero casing speed and the specified carriage speed. Each target genuinely vibrates. Its free internal harmonic energy is $(hg/2M)(J/g)^2$, independent of $\omega$. The remaining outgoing energy is $MV^2/2$. Every chosen positive stiffness, displacement and energy is finite.

Take $T=5\Delta$, the original five-gap horizon. Put $\delta V=V_2-V_1=v_0/6$. At *every* $0\le t\le T$ the signed position difference satisfies
$$
 0\le x_2(t)-x_1(t)
 =\delta V\int_0^t[1-\cos(\omega s)]\,ds
 \le\frac{\delta V\,\omega^2t^3}{6}.
$$
The upper bound follows from $1-\cos z\le z^2/2$. It has units of length, and the difference is strictly positive for $t>0$ at every $\omega>0$. In particular, for any prescribed coordinate error $\eta>0$, choosing $0<\omega^2<12\eta/(\delta V T^3)$ puts the true records less than $2\eta$ apart in the maximum norm at $t_j=j\Delta$, $j=0,\ldots,5$. Their coordinatewise midpoint is a single possible measured record within $\eta$ of either history, with the exact same signed cart velocities. This proves the zero infimum without imposing a noise distribution or taking $k=0$.

CL083’s exact uniqueness still applies after restricting to the energy cap. In the five consecutive position increments a compatible casing contributes a constant drift $V\Delta$ and at most two nonconstant harmonic sequences. When two histories are compared, grouping equal frequency factors leaves at most five distinct exponential sequences including the constant. Equality of all six tags gives five zero entries in the difference of their increment sequences. The first as many rows as there are distinct factors form a square Vandermonde system with trivial kernel. A harmonic sampled at a constant phase disappears upon differencing. Thus an exact six-position collision would require equal drifts, which the two masses cannot have. The separation is positive for each individual pair and has no positive lower bound over the allowed histories. [Six-position mass comparison](six_casing_positions_and_total_inertial_mass.md)

## A sufficient stroke and position-error bound

Suppose a separate physical calibration gives $|H(t)|\le S$ for the casing displacement $H$ about its own translating equilibrium, $x(t)=a+Vt+H(t)$. Here $S$ is a one-sided length bound. For observed positions $\tilde x_j$ with $|\tilde x_j-x(j\Delta)|\le\eta$, the measured end-to-end displacement $D=\tilde x_5-\tilde x_0$ obeys
$$
 |D-VT|\le 2S+2\eta .
$$
The two true endpoint harmonic values can differ by $2S$, and the two reading errors can differ by $2\eta$. Hence a sufficient uniform discrimination criterion on the existing tags is
$$
 (V_2-V_1)T>4(S+\eta)
 \quad\Longleftrightarrow\quad S+\eta<\frac{5v_0\Delta}{24}.
$$
Under this strict inequality the two allowed intervals for $D$ are disjoint. A record consistent with one mass excludes the other. At contact between the closed intervals this endpoint argument supplies no guarantee. The criterion is sufficient and uses no extra position, measured velocity of the casing, or exact casing-position origin.

In the constructed histories the casing’s harmonic amplitude is $V/\omega$. It can grow without bound as the spring softens while the internal energy and the signed impact data stay fixed. A bound on energy alone therefore supplies no such uniform stroke calibration. The inference concerns the ratio to the calibrated reference mass in the supplied inertial frame and over this one finite flight.
