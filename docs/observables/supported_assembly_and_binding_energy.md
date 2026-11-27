# What a force reading misses about gravitational binding energy

Two bodies move slowly apart against their mutual attraction. A preloaded spring helps push them apart. At the start and finish, every contact force has the same value in two settings of the support. Yet the actuator receives a different amount of energy in each setting. The difference comes from the force the spring exerts **between** the endpoints. One signed reading of the actuator’s energy store distinguishes the two cases.

## The pair and its support

Each body is a rigid sphere of mass $m$ with the same smooth radial density, supported within radius $\eta=d/4$. In a common inertial frame their centres lie at $\pm R e_1/2$, where $e_1$ points along the line joining them. The stroke opens from $R=3d$ to $R=4d$ and starts and ends at rest. With the Newtonian potential zero at infinity, the mutual energy is $U_x(R)=-Gm^2/R$ throughout. This formula is exact for the disjoint spherical profiles. Each body also has its own finite gravitational self energy, unchanged by translation.

The **weighed assembly** $A$ contains the bodies, collars, spring, guide, two cam tracks, selector and locks. Both tracks are installed in both settings. The selector engages one before the stroke and stays there. Its two positions have equal intrinsic energy. The **isolated apparatus** $C$ also includes the two-ended drive and its calibrated reversible energy store. Only the drive does work across the boundary of $A$. The store is inside $C$.

The endpoint record gives the body masses, profiles and poses, bare inventory, dimensional standards, initial spring energy and store fill. It includes the individual signed loads and areas of both support pads and both drive pads, the lock status, temperatures and rest velocities. It leaves the selected track, the intermediate loads, the terminal spring compression and the terminal store fill unobserved. The comparison matches the two settings at each corresponding endpoint.

## How equal endpoint forces give different work

Let $t=(R-3d)/d$ denote fractional opening, $H(R)=Gm^2/R^2$ the attraction magnitude, $H_0=H(3d)$ and $H_1=H(4d)$. Use the energy unit $E=H_0d=Gm^2/(9d)$. The cam in setting $s=0,1$ transmits outward force
$$
B_s(R)=(1-t)H_0+tH_1+sH_1t(1-t),\qquad H_1/H_0=9/16 .
$$
The last term vanishes at both endpoints. There, the left and right support forces are $-H_j e_1$ and $+H_j e_1$ at endpoint $j=0,1$. Each acts uniformly over a pad of area $\eta^2$, with zero transverse force and zero couple. Both drive pads are unloaded. The internal locks engage at fixed separation and zero preload, so they do no work.

Both force laws can be realized by the same ideal Hookean spring of stiffness $K=H_0/d$ and initial energy $2E$. Define its dimensionless work on opening by
$$
I_s(t)=\int_0^t\frac{B_s\bigl(d(3+u)\bigr)}{H_0}\,{\rm d}u
=t-\frac{7}{32}t^2+s\frac{9}{16}\left(\frac{t^2}{2}-\frac{t^3}{3}\right).
$$
Here $u$ is fractional opening. The spring’s remaining energy is $S_s=E(2-I_s)$ and its compression is $x_s=\sqrt{2S_s/K}$. The dimensionless integral increases from zero to $(25+3s)/32$, keeping $3d/2\le x_s\le2d$ throughout. A cam track can therefore constrain its follower to the smooth graph $y=x_s(R)$. Since $-Kx_s x_s'=B_s$, the track transmits the specified force with bounded slope. Its ideal reaction has zero total power on motions satisfying $\dot y=x_s'\dot R$. The final spring energies follow from the two paths and common preload.

In quasistatic balance the signed outward drive force on the right collar is $D_s=H-B_s$, and the left collar receives the opposite force. Both contacts move. The right contact moves by $+e_1\,{\rm d}R/2$, the left by $-e_1\,{\rm d}R/2$, so each contributes $D_s\,{\rm d}R/2$ to the work delivered to $A$. With positive $W_s$ denoting delivery from the store,
$$
W_s(t)=\int_{3d}^{R}D_s(r)\,{\rm d}r
=E\left[\frac{3t}{3+t}-I_s(t)\right].
$$
The first term in brackets is the increase in mutual energy in units of $E$. The inverse-square attraction lies below its endpoint chord $B_0$ in the interior, and $B_1\ge B_0$. The drive absorbs energy throughout opening. Its store rises monotonically from $10E$ to at most $(10+1/8)E$, within its $20E$ capacity.

## What one signed store reading determines

| Change from $3d$ to $4d$, in units of $E$ | Setting 0 | Setting 1 |
|---|---:|---:|
| Mutual energy of the bodies | $+3/4$ | $+3/4$ |
| Spring energy | $-25/32$ | $-7/8$ |
| Energy of the weighed assembly $A$ | $-1/32$ | $-1/8$ |
| Actuator store fill | $+1/32$ | $+1/8$ |
| Energy of the isolated apparatus $C$ | $0$ | $0$ |

The spring releases more energy than the bodies gain in separating. The actuator receives the excess. In $A$, all bare rest energies and fixed internal energies are counted once, as are the two body self energies, their mutual energy and the variable spring energy. Thus $\Delta E_A=\Delta U_x+\Delta S_s=W_s$. An independently calibrated reading of **initial minus final store fill** gives $W_s$ without reading the selector. With the known $\Delta U_x$, it also gives the spring correction $\Delta S_s=W_s-\Delta U_x$. The raw assembly change equals the mutual energy change alone precisely when the other retained internal energies have zero net change. Here that would require $\Delta S_s=0$, which neither setting satisfies.

The drive docks and undocks at rest and zero load, with no external anchor. The model assumes reversible unloaded retraction, recovery of the drive’s non-store state, and no heat, radiation or material exchange. The store retains its gain. Inside $C$ the two changes sum to $\Delta E_C=0$.

**The mass statement uses an additional premise.** Applying the supplied rest-frame rule $\Delta M=\Delta E/c^2$ to the detached endpoints gives $\Delta M_A=-E/(32c^2)$ or $-E/(8c^2)$, and $\Delta M_C=0$ at the retained order. $H,B,D$ have force units, $K$ has force per length, traction has force per area, and $W,E,S,U_x$ have energy units. The dimensional standards and $c$ are supplied.

## Profile and accuracy of the calculation

For the specified unit-integral profile take $b(q)=\exp[-1/(1-q^2)]$ for $0\le q<1$ and zero otherwise. Then $f_\eta(x)=b(|x|/\eta)/(\eta^3 Z)$ with $Z=4\pi\int_0^1 q^2 b(q)\,{\rm d}q$. Each translated density is $m f_\eta$. Spherical symmetry and disjoint support give the mutual term above. Each endpoint inventory includes two terms $-Gm^2J_\eta/2$, where $J_\eta=\iint f_\eta(u)f_\eta(v)/|u-v|\,{\rm d}^3u\,{\rm d}^3v$.

Set $\lambda=Gm/(dc^2)\ll1$. The energy and force comparisons retain terms of orders $\lambda mc^2$ and $\lambda mc^2/d$. Throughout the stroke, all auxiliary hardware, including its stored energy, has nonnegative mass-equivalent density $a$, total mass $O(\lambda m)$, density bounded by $O(\lambda m/d^3)$ and spatial extent $O(d)$. The constants are independent of $\lambda$. Splitting the Newtonian kernel integral at distance $d$ gives, for $p=1,2$,
$$
\int \frac{a(y)}{|x-y|^p}\,{\rm d}^3y
\le \frac{4\pi}{3-p}\|a\|_\infty d^{3-p}+\|a\|_1d^{-p}
=O(\lambda m/d^p).
$$
Body–hardware gravitational energies are consequently $O(\lambda^2mc^2)$ and hardware–hardware energies $O(\lambda^3mc^2)$, including interactions across the drive boundary. The absolute force bounds carry one more factor of $1/d$. With hardware travel of order $d$, the gravitational work from those forces is subleading. Redistribution of stored energy changes the auxiliary mass-equivalent source by $O(\lambda m)$ over the stroke, whose coupling to the body potential $O(Gm/d)$ is likewise subleading. The hardware’s bare rest energy and variable spring and store energies remain in their respective inventories. These bounds concern Newtonian hardware terms. Physical material dynamics, measured gravitational weight, relativistic error control and a derivation of mass or units from DET primitives remain open.

## Provenance

The original State reviewer independently checked the fixed calculation, and the research coordinator accepted it within the stated model. The support idea, design and proof strategy were known before the target calculation was authorized. Earlier work included an unauthorized point-source calculation and four dependent source reads after a failed usage check on 26 November 2026 at 09:04:31 UTC. Both departures remain on record. An earlier design-registration display exceeded the available context. The author subsequently recorded a full readback. The reviewer checked the visible order of command previews and completion, and attributed the extent of the registration and readback to the author’s record. Source identities and the sections actually read were recorded separately. The acceptance covers the analytic result within its stated assumptions.
