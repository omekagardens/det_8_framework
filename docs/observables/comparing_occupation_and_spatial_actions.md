# Can two beat-phase readings identify a common occupation and spatial action?

On one registered baseline carrier, the two beat increments leave exactly two possible spatial actions in units of $M_0c^2T$. Equality with the occupation action is possible precisely when at least one of those two values belongs to the occupation record’s sharp set. If neither belongs, equality is excluded. Under the supplied freedom to prepare the mode arm independently, no feasible joint record in the stated winding band forces equality.

## Expressing both actions in the same units

Use the admitted E53 record, with the same positive baseline inertial mass $M_0$, tick $T$, stroke $L$ and optical speed $c$ in both arms. The signed echo difference fixes $\lambda=L/(cT)>0$. Write $\eta_o=J_{\rm occ}/(M_0c^2T)$ and $\eta_s=J_{\rm sp}/(M_0c^2T)$. Here $J_{\rm occ}$ is the unit of action per occupation, including when the baseline occupation index itself is zero.

For clarity, E53 uses the preparations $00,10,11$ at indices $q=0,1,2$. Its positive rates $\phi_q=T h'(qJ_{\rm occ})$ come from its registered quadrature law, and $m_q=M_q/M_0$ from its mechanics. Put $b_i=m_{i+1}-m_i$ for $i=0,1$. Under its smooth, increasing, convex energy law, $\eta_o$ ranges over $I=I_0\cap I_1$, where
$$
 I_i=(b_i/\phi_{i+1},\,b_i/\phi_i)\quad\text{if }\phi_i<\phi_{i+1},
 \qquad I_i=\{b_i/\phi_i\}\quad\text{if }\phi_i=\phi_{i+1}.
$$
The input is already admitted and $I$ is nonempty. Each value of $I$ is attainable at fixed feasible mechanical parameters by a smooth convex interpolation with the same sampled energies and rates. This preserves the original signed mechanical readings, indexed quadratures, histories, detector failures and setting probabilities. [E53, §§2–5](<./action_per_occupation_from_sector_masses.md>)

In the separate sector-zero mode preparation let $a_1>a_2>\cdots$ be the negative Airy zeros. For the top two nodes of the lower mode and the top node of the higher mode, form
$$
 A=\frac{X_{L1}-X_{L2}}{a_1-a_2},\qquad B=X_{H1}-X_{L1}.
$$
On the admitted E64 domain, $A=s\ell$ and $B=s\,\Delta E/F$ with $\ell^3=J_{\rm sp}^2/(2M_0F)$ and $\Delta E=J_{\rm sp}\omega$. All heights must be finite, with $A,B>0$. The common origin cancels. Decay selects the upper Airy solution, and the two top nodes correspond to the same Airy zero. The common lower reflector selects the actual pair of energies. The algebra presupposes those modes and their registered interior nodes. The positivity checks alone cannot certify a lower-wall spectrum. [E64, spatial inverse](<./gravity_bound_modes_action_and_acceleration.md>)

The same ruler gives the positive finite difference $D_L=sL$. Thus $\ell/(cT)=\lambda A/D_L$ and $(\Delta E/F)/(cT)=\lambda B/D_L$. Substituting $J_{\rm sp}/M_0=2\ell^3\omega/(\Delta E/F)$ yields
$$
 x=\omega T,\qquad K=\frac{2\lambda^2 A^3}{D_L^2 B}>0,\qquad
 \boxed{\eta_s=Kx}. \tag{1}
$$
Equivalently, $K=2\lambda^2(A/D_L)^2(A/B)$ uses only dimensionless ratios. An absolute ruler gain, tick in seconds and mass in kilograms all cancel.

## The winding and equality tests

Let $u$ be the complex increment at $T$, and $v$ the increment at $3T/2$. Require finite unit-modulus readings and $v^2=u^3$. Define $w=v/u$. If the phases fit, $w=e^{ix/2}$. Conversely, the consistency equation gives $w^2=u$ and $w^3=v$, so matching $w$ reproduces both signed complex increments. Choose the unique $\theta\in(0,2\pi]$ with $e^{i\theta}=w$. Within the supplied band the complete, duplicate-free set is
$$
 \mathcal X=\{2\theta,\ 2\theta+4\pi\},\qquad 0<x\le8\pi. \tag{2}
$$
Indeed the joint phase period is $4\pi$. For $u=v=1$ the two solutions are $4\pi$ and $8\pi$. Zero is excluded and the upper endpoint is attained. Inconsistent phases have no branch.

On a feasible joint record the full ordered action set in the common units is
$$
  (\eta_o,\eta_s)\in I\times S,\qquad S=\{Kx:x\in\mathcal X\}. \tag{3}
$$
The intersection $I\cap S$ lists exactly the possible **common** values. Check both distinct members of $S$. For an open interval use strict membership at both ends. For a singleton require exact equality. An empty intersection excludes equality in every fit. A nonempty intersection permits equality and permits inequality. Even if both candidates are in $I$, hold one occupation value fixed and take the other spatial branch. In general the product would force equality only for matching singletons. Here $K>0$ and the two windings always differ by $4\pi$, so this case never occurs. Failure of an input or phase feasibility condition rejects the model for the record before any equality decision.

**Why the product is sharp.** Start from an admitted joint preparation. Keep the same $M_0,T,L,s$, origin, mode labels and E53 mechanics. E53’s interpolation realizes any $\eta_o\in I$ with those parameters. To move from one admitted winding $x$ to another $x'$, put $k=x'/x$. At fixed mass and geometry take $J_{\rm sp}'=kJ_{\rm sp}$ and $F'=k^2F$. The kinetic and linear-potential terms both scale by $k^2$. A hard boundary stays fixed. If the admitted lower interaction has an uncalibrated potential energy, scale that term by the same factor for both modes. The full spatial Hamiltonian then scales by $k^2$ up to a common energy offset. Its eigenfunctions and all node heights persist, while $\Delta E'=k^2\Delta E$ and $\omega'=k\omega$. Equations (1) and (2) reproduce $D_L$, all three raw heights and both increments.

This attainment uses independent mode preparation, an unmeasured adjustable mode force outside the E53 lift settings, and a lower interaction compatible with this energy rescaling. It holds on the admitted domain with that freedom. An independently calibrated finite lower potential, a fixed relation between the mode field and the lift fields, or a constitutive link between the two actions would require checking joint support again.

## One complete record with opposite answers

Use E53 §5’s full registered law and choose one physical realization once. Take $M_q=M_*(1,2,4)_q$, $M_*,T,c>0$, spring stiffness $M_*/T^2$, $L=cT$, and the source’s signed lifts, strokes, store and detector law. Its echoes are $(3,5)$ in tick units, so $\lambda=1$. Its three phase advances are $(1/2,1,2)$ radians, giving $I=(1,2)$. Fix $\eta_* =2\log 2$ (natural logarithm), $J_{\rm occ}=J_*=\eta_*M_*c^2T$, and the same $h(J)=C_0+M_*c^2\,2^{J/J_*}$ in both worlds. Every earlier raw reading and outcome probability, including failures, is thus unchanged.

In the mode arm use a hard wall at $z=0$, energy zero there, and the third and fourth Airy modes as $L,H$. Write $d=a_3-a_4>0$ and choose
$$
 \ell=cT\sqrt{\frac{\eta_* d}{2\pi}},\qquad
 J_{\rm sp}=J_*,\qquad F=\frac{J_*^2}{2M_*\ell^3}.
$$
The energies are $E_n=-F\ell a_n$. The three registered heights before display conversion are $\ell(a_1-a_3),\ell(a_2-a_3),\ell(a_1-a_4)$, all strictly above the wall. Choose one $s>0$ and one origin $b$, apply $X=sz+b$ to all three, and record $D_L=s cT$. Use the tagged eigenmode preparations for the separate node readings. For both beat dwells take independent preparations of the equal coherent superposition with the same initial relative phase. Its mean excitation above the lower mode is $\Delta E/2=\pi J_*/(2T)$. The beat gives $x=TF\ell d/J_*=\pi$, so $(u,v)=(-1,-i)$. This world has equal actions.

In the second world set $J_{\rm sp}'=5J_*$ and $F'=25F$. Keep the same absolute mass, clock, stroke, ruler, wall, modes and occupation action. With the same baseline passive mass $P_0=M_*$ as in the E53 example, the independent mode field may have magnitudes $F/M_*$ and $25F/M_*$ respectively, with both earlier lift fields fixed. For each stationary tagged mode the mean upward wall reaction balances the applied downward force, so it too increases by a factor of 25. The retained record contains no force reading. The mode length and every displayed height agree. Every spatial eigenenergy and the required excitation gap are multiplied by 25, so $x'=5\pi$ gives the very same $(-1,-i)$. The two spatial candidates are $\eta_*$ and $5\eta_*$, only the former in $(1,2)$. The second world has unequal actions even though its full retained record agrees with the first.

## What the registration supplies

The comparison uses the same baseline carrier mass, the same stroke on the spatial ruler, and the same optical tick for the mechanical and occupation records and both beat dwells. Each complex phase is an increment relative to preparation of the same stable mode pair. Two snapshots with separate unknown starting phases would not supply (2). The independently justified winding band is essential. E53’s sharp set uses its exact population law including failures, while the spatial phases here are ideal registered readings. Finite quadrature counts or uncertain node locations would require a measurement-error model before applying exact equalities to data.

Preparing the coherent pair, supplying its excitation energy, maintaining the mode field and reflector, resolving the nodes, referencing the phases and resetting the readout are physical inputs. The coherent preparation in the second world has 25 times the first world’s mean excitation above its own lower mode. The actual work of preparing and reading either state also depends on apparatus and losses. E53’s calibrated spring, signed optical ranging, signed work store and restoration retain their own prerequisites and costs. To express either action in joule-seconds one needs a dimensional calibration of $M_0c^2T$ or an equivalent conversion. The dimensionless comparison supplies neither a physical clock nor a work store. Any identification with a universal action, Planck’s constant or a DET-native unit requires independent physical evidence.
