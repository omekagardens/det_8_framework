# Timing an additive-mass measurement without a frequency calibration



For exact force and time data, 81 readings at $iD+jE$, $0\le i,j\le8$, $D>0,\ E/D=\sqrt2$, identify the total positive mass in one continuous common-acceleration run. Two applications of the nine-point inverse suffice, even if different modes appear constant on different timing intervals. **At any positive force tolerance, no fixed finite list of exact times can uniformly distinguish total masses $3m$ and $6m$** in the admitted family. Here $m>0$ can be fixed before choosing the times or the tolerance.

## Force and timing model

The two positive-mass terminals of a connected, ungrounded one-dimensional network follow the same displacement $X(t)$ with known signed acceleration $X''=a\ne0$. The network has at most two internal positive point masses, positive ideal Hooke springs, unforced interiors, no losses and no other external forces. For the exact test, acceleration is maintained through $8(D+E)$; all times refer to a single inertial clock and a common opening epoch. The force tag is the sum of the signed forces exerted by the two actuators on the network.

Let $M$ be total constituent mass. In displacement coordinates relative to the common translation, the interior obeys $M_I y''+K_{II}y=-aM_I\mathbf1$, with positive diagonal $M_I$. The restricted stiffness is positive definite by connectedness to the prescribed terminals. Removing the constant particular solution leaves a mass-normalized real symmetric oscillator. Repeated eigenvalues give ordinary sinusoids. Internal forces cancel in the sum, giving $F(t)=aM+\mathbf1^{\mathsf T}M_I y''$. The accepted result therefore represents every compatible force as
$$
 F(t)=aM+\sum_{\sigma\in S} c_\sigma e^{i\sigma t},
$$
where $S$ has at most four nonzero signed frequencies (two positive frequencies with their conjugates). Initial positions and velocities are arbitrary finite values. Coincident terms combine; an unexcited or force-invisible mode contributes zero. With no internal contribution $F=aM$.

## A finite inverse for the 81 tags

Use the following real nine-point operation $\mathcal C$ on a sequence $Y_0,\ldots,Y_8$ known to be a constant plus at most four distinct nonunit complex exponentials, paired to give real data. Set $d_n=Y_{n+1}-Y_n$. Solve for any real weights $p_0,\ldots,p_4$ satisfying
$$
 \sum_{j=0}^4p_j=1,\qquad \sum_{j=0}^4 p_j d_{s+j}=0
 \quad(0\le s\le3),\qquad
 \mathcal C(Y)=\sum_{j=0}^4p_jY_j .
$$
If $Z$ is the set of distinct active nonunit roots, the normalized polynomial $\prod_{z\in Z}(v-z)/(1-z)$ is a real solution after padding its coefficients. For any solution polynomial $P(v)=\sum p_jv^j$, the four difference equations annihilate the moments at orders $s=0,\ldots,3$ of the weights $b_z(z-1)P(z)$, where $b_z$ is the amplitude of $z^n$. The first $|Z|$ rows form a nonsingular Vandermonde matrix, so every active $P(z)=0$. Since $P(1)=1$, the answer is exactly the constant. For an all-constant input $p_0=1$ works. This operation also works for a negative or zero constant and for singular weight systems with multiple solutions.

Write $F_{ij}=F(iD+jE)$. For **each fixed $j$** apply $\mathcal C$ along the nine $i$ entries. Nonunit $D$-roots are eliminated regardless of aliasing or cancellation at this $j$. Every term with $e^{i\sigma D}=1$ joins the column constant. The nine extracted values are therefore
$$
 b_j=\mathcal C(F_{0j},\ldots,F_{8j})
     =aM+\sum_{\sigma:\ e^{i\sigma D}=1} c_\sigma e^{i\sigma Ej}.
$$
For any surviving $\sigma\ne0$, $\sigma D=2\pi n$ for a nonzero integer $n$. Then $\sigma E=2\pi n\sqrt2$ is not a multiple of $2\pi$. Thus $b_0,\ldots,b_8$ have at most four distinct nonunit $E$-roots after merging plus the single constant $aM$. The final answer is
$$
 \boxed{M=\mathcal C(b_0,\ldots,b_8)/a}.
$$
Any mode constant only in $E$ was already removed in the first stage. Alternating roots, missing modes and mutual aliases need no frequency estimates or rank choices. All 81 epochs are distinct by irrationality. The shared continuous trajectory is essential to the displayed dependence on $j$; independently restarting each column with new phases would remove that guarantee.

## Any positive force tolerance permits a fixed mass ambiguity

Fix $m>0,\ a\ne0$, an arbitrary finite list of $N\ge1$ nonnegative sampling times $t_s$, and $\epsilon>0$ in force units. Put mass $m$ at each terminal and use two identical springs, each of stiffness $k=2m\Omega^2>0$, flanking a central mass $\mu$. Compare $\mu=m$ with $\mu=4m$, keeping the same springs in both networks. Start from rest at equilibrium and impose $X=at^2/2$. For $\omega^2=2k/\mu$, the centre’s displacement relative to the terminals and the boundary force sum are
$$
 y(t)=\frac{a}{\omega^2}(\cos\omega t-1),\qquad
 F(t)=2ma-2ky(t)=2ma+\mu a(1-\cos\omega t).
$$
The two frequencies are $2\Omega$ and $\Omega$, respectively. Each actuator supplies $ma-ky=F/2$ by symmetry. The mass gap $3m$ is independent of the force tolerance and of the timing list.

Choose $\Omega$ so every $\Omega t_s$ is within $\eta$ radians of a multiple of $2\pi$. Here is a finite existence argument that respects the units. Fix a reference duration $\tau>0$, integers $n_0\ge1$ and $Q>2\pi/\eta$. Take the fractional-part vectors of $j n_0(t_1,\ldots,t_N)/\tau$ for $j=0,\ldots,Q^N$. Two lie in the same one of $Q^N$ equal boxes of the unit cube. Their positive index difference $q$ yields $\Omega=2\pi q n_0/\tau$, which meets every phase tolerance simultaneously. The frequency is finite and can be made arbitrarily large by increasing $n_0$.

Using $1-\cos\theta\le\theta^2/2$, the lighter centre’s force differs from $2ma$ by at most $m|a|(2\eta)^2/2$ at each tag; the heavier centre’s bound is $4m|a|\eta^2/2$. Take $\eta\le\sqrt{\epsilon/(2m|a|)}$. The constant displayed record $2ma$ is then within $\epsilon$ of **each** physical record at **every** exact time, including the 81 proposed times if selected. On the irrational grid the ideal records differ, as the exact inverse requires. Bounded measurement errors can obscure that difference. This excludes a uniform finite-tag guarantee over the admitted family, even for initially unstrained springs and known opening velocities.

## Stroke, work and clock standards

For the collision let $T=\max_s t_s$. The prescribed terminal stroke from rest is $|a|T^2/2$, and $|y|\le2|a|/\omega^2,\ |y'|\le|a|/\omega$. Equilibrium spacings larger than the relative excursion keep the sites ordered. The maximum magnitude of either actuator force is bounded by $(m+\mu)|a|$. Each example uses finite stiffness, although the family allows increasing stiffness and faster force variation as the requested tolerance shrinks.

The two terminal kinetic energies sum to $m(at)^2$, the central kinetic energy is $\mu(at+y')^2/2$, and the two springs store $k y^2\le2\mu a^2/\omega^2$. The entire ledger is finite on $[0,T]$; the change from initial rest equals $\int_0^T F(t)\dot X(t)\,dt$. Equal signed terminal velocities allow this sum of powers. Thus the ambiguity does not rely on large opposed actuator forces, a diverging terminal displacement, or an omitted energy source. Supplying the acceleration and registering the rapidly varying forces requires an external apparatus. Discrete force tags do not measure the continuous work integral.

The exact protocol replaces the separate spectral exclusion by exact placement of two incommensurate intervals on one clock. A rational approximation to $\sqrt2$ does not certify that premise: if $E/D=p/q$, the positive frequency $2\pi q/D$ has unit phase in both directions. A timing error $\Delta t$ produces a phase error $\omega\Delta t$, which has no uniform bound from clock precision alone over unbounded frequencies. The finite-error obstruction already holds with timing error zero. A practical discrimination guarantee would need independent restrictions that separate allowed mechanical responses at the apparatus’s resolution, or additional preparation or measurement information. No such restriction is supplied. Mass units still come from calibrated signed force divided by calibrated acceleration; no native or gravitational scale follows.

[Underlying nine-force mass measurement](total_mass_from_nine_boundary_forces.md)
