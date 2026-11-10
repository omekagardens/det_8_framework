# Action per occupation from sector inertias and phase advances

Independently reviewed conditional result, 9 November 2026 HST.

Under the supplied rest-energy and phase law, three sector inertias and three phase advances give an exact interval or singleton for the action per occupation in units of $M_0c^2T$. The interval can also be empty. One complete record gives the open interval $(1,2)$. Removing convexity alone allows every positive value on that same record, even with the physical masses and tick held fixed.

## 1. What joins the two experiments

In the GDM063 phase lift of GDM047, let $(\theta_r,I_r),(\theta_e,I_e)$ be canonical angle/action pairs. On the four registered occupation tori, $J=I_r+I_e=J_0Q$ with $J_0>0$ and $Q=r+e$. The labels $00,10,01,11$ have $Q=0,1,1,2$. The separate reference-memory label carries no extra unit of this action. The accepted generator $J$ rotates both angles at unit speed in its dimensionless group parameter. With the same canonical bracket, dividing $J$ by $J_0$ divides that speed by $J_0$. Its flow and a fixed angular detector supply an angular convention. They supply neither a physical time per rotation nor a measured energy per occupation. Jointly changing coordinates of states and effects preserves the detector probabilities, so the physical phase registration must be specified.

E53 supplies a physical autonomous dwell of duration $T>0$, shared with the mechanical tick, and one smooth ambient energy function $h(J)$ through $0\le J\le2J_0$. Hamilton's equations give $\dot I_r=\dot I_e=0$ and $\dot\theta_r=\dot\theta_e=h'(J)>0$. Convexity requires $h''(J)\ge0$. The independently measured sector masses enter as $h(qJ_0)=C_0+M_qc^2$ for **one** energy offset $C_0$. The common carrier registration across GDM040 and GDM047, the time transfer, and the identification of these values and derivatives with the same physical function are all premises. In GDM040 a conserved row has form $(A,B,B,D')$. Additivity over the two bits would further require $A+D'=2B$. Conservation alone imposes no such equation on the measured masses.

For one lifted birth branch let $S$ be its angle transport, identity or swap. A common rotation $R_{\phi_q}$ through $\phi_q=T h'(qJ_0)$ commutes with the swap. Every supported native/reference transition preserves $Q$, so $S R_{\phi_q}=R_{\phi_{q'}}S$ on a branch from $q$ to $q'$. Its native/reference kernel weight is independent of the angles. Pushing forward any initial measure and summing the branches therefore gives the same joint law in either order, including the original support zeros and native marginals. At equal initial angles the swap leaves their common value fixed. The phase experiment below has a single dwell. No interleaved birth, assigned birth duration or earlier single-birth detector table enters its probabilities.

## 2. Complete observation law

Choose the top-level arm by an independent fair draw. The mechanical arm retains the accepted fifteen settings, including its fair choice of original or calibration arm and uniform choice among nine or six settings respectively. Its preparations for sectors $0,1,2$ are $\delta_{00},\delta_{10},\delta_{11}$. Both labels of sector 1 have the same coefficients. For a retained history $H=(a,b_1,b_2)$, with $a=E,F$ and each of the four ordered bit pairs retained,
$$
p_i(H)=\frac{q_a}{4}\bigl(1+\epsilon_a{\bf1}_{i=1}/2\bigr),\quad
(q_E,q_F)=(2/3,1/3),\quad(\epsilon_E,\epsilon_F)=(1/8448,-1/4224).
$$
These weights sum to one. The table gives unconditional probabilities, already including the top-level draw. Each mechanical reading is a finite point value shared by all histories at that setting. For a reading event, multiply its weight by the indicator that the point belongs to the event.

| Tagged setting | Retained record | Unconditional weight per cell |
| --- | --- | --- |
| Spring pairs $01,02,12$ | Independent $H,H'$ and signed extension ratio $y_{ik}$ | $p_i(H)p_k(H')/36$ |
| Loaded lift (field 1 with 0 or 1, field 2 with 1 or 2) | $H,z_j,w^+_{ij},w^-_{ij}$ | $p_i(H)/36$ |
| Blank lift in each field | Empty token and its own $z_j,w^+_{\emptyset j},w^-_{\emptyset j}$ | $1/36$ |
| Stroke at $jL$, $j=1,2$, blank or engaged | Apparatus label and ordered $v^+_{rj},v^-_{rj}$ | $1/24$ |
| Echo at $jL$, $j=1,2$ | Apparatus label and delay $d_j$ | $1/24$ |
| Phase preparation $q=0,1,2$, quadrature $X$ or $Y$ | Actual $q$, quadrature, and sign $+$ or $-$ | $(1\pm z)/48$ |
| Same phase settings | Actual $q$, quadrature, and failure | $1/24$ |

The mechanical arm has $192+32+2+4+2=232$ labelled cells, all with failure flag zero. Conditional on the phase arm, draw $q$ uniformly, prepare the corresponding GDM047 source $00,10,11$, reference-memory label 0 and both angles zero. Perform the dwell and read one independent fair quadrature with $z=\cos\phi_q$ or $\sin\phi_q$. Each tagged phase setting has unconditional weight $1/12$. Its three outcomes give 18 labelled cells across the six settings, with any detector-implied zero weight retained. Total phase failure probability over the experiment is $1/4$. Each arm has total weight $1/2$. Their tagged outcomes are disjoint, and every other outcome has zero weight. Actual preparation labels identify the sectors, including mechanically indistinguishable history laws $p_0=p_2$. No mechanical history probability is assigned to a phase trial.

To invert, use the conditional probabilities on each **entire setting**, including its failures. Check $P({\rm fail})=1/2$ and $P(\pm)=(1\pm z)/4$ with $z=2[P(+)-P(-)]$. For each $q$, let $C_q,S_q$ be the reconstructed $X,Y$ responses. Require $C_q^2+S_q^2=1$ and $S_q>0$. The externally assured strict band $0<\phi_q<\pi$ then gives $\phi_q=\operatorname{atan2}(S_q,C_q)$ uniquely. This is inversion of the stipulated population law. Finite samples need not give the exact probabilities. Without independent assurance of the band, whole windings would be invisible.

## 3. Mechanical feasibility inherited by the inverse

Use the common stable Hooke stiffness $K>0$, simultaneous rest release with positive extension below equilibrium length, a signed ratio at the common tick, and the assured first lobe. For $-1<y_{ik}<1$, let $t_{ik}=(\arccos y_{ik})^2$. For distinct $i,k,l$ require
$$
u_i=(t_{ik}+t_{il}-t_{kl})/2>0.
$$
Then $u_i=KT^2/M_i$ and the three phases $\sqrt{u_i+u_k}$ reproduce the spring readings. In each lift field require a common positive $z_j=g_c\Delta\Phi_j/c^2$ with known $g_c>0$ and actual paths within the supplied weak-field regime. Use a common signed work gain $g_w>0$ and verified zero. Let $\ell_{ij}=-w^-_{ij}$, $H_{ij}=w^+_{ij}$ and require $\ell_{ij}\le H_{ij}$, including the blank. For $S_1=\{\emptyset,0,1\}$, $S_2=\{\emptyset,1,2\}$, test existence of positive $x_i=g_wc^2P_i/g_c$ with $x_\emptyset=0$ such that
$$
z_j(x_b-x_a)\le H_{bj}-\ell_{aj}\qquad(a,b\in S_j).
$$
This allows a common holder rise per field, chosen as $\max_{a\in S_j}(\ell_{aj}-z_jx_a)$ in display units. The same $x_1$ applies in both fields. Passive coefficients $P_i$ are otherwise unrestricted.

For strokes put $\ell^c_{rj}=-v^-_{rj}$, $H^c_{rj}=v^+_{rj}$, with $\ell^c_{rj}\le H^c_{rj}$. The shared stiffness, delivered-work gain, common fixture reference at each length and initially unstretched spring give the following feasible set for $E=g_wKL^2/2$.
$$
\mathcal E=(0,\infty)\cap\bigcap_{j=1}^2
\left[(\ell^c_{1j}-H^c_{0j})/j^2,\ (H^c_{1j}-\ell^c_{0j})/j^2\right].
$$
Indeed the blank and the engaged brackets shifted by $-j^2E$ must intersect for their holder. In tick units require $\lambda=(d_2-d_1)/2>0$ and $d_0=2d_1-d_2\ge0$. Then $d_j=d_0+2j\lambda$, $L=cT\lambda$, and the shared displayed scale is
$$
D=g_wKT^2c^2\ \in\ \mathcal D=(2/\lambda^2)\mathcal E .
$$
Positive shared endpoints are included, including singletons. A zero value of $D$ is excluded. An empty calibration set or failure of an arm's observation or operating conditions rejects that arm before an energy/phase comparison.

For any feasible $D$, choose compatible positive $T,g_w$ and take $K=D/(g_wT^2c^2)$, $M_i=D/(g_wc^2u_i)$. Use any feasible unrestricted lift solution. For each lift or stroke choose its common holder from the corresponding intersection. If $V$ is a row's resulting displayed conservative rise in $[\ell,H]$, its outward and return physical losses are $(H-V)/g_w$ and $(V-\ell)/g_w$. With rigid endpoints at rest and no hidden moving-leg supply, the sink receives these losses. For either signed pair $(w^+,w^-)$ the store must cover initial, turning and final levels $B,\ B-w^+,\ B-w^+-w^-$ in display units. Preparation and replenishment between independent trials use separate resources.

## 4. Exact set of action scales

Write $m_q=M_q/M_0=u_0/u_q$, $b_i=m_{i+1}-m_i$ for $i=0,1$, and $\eta=J_0/(M_0c^2T)$. The dimensionless rate profile $v(y)=T h'(J_0y)$ on $[0,2]$ has $v(q)=\phi_q$. Integrating between successive tori eliminates $C_0$ and gives
$$
b_i=\eta\int_i^{i+1}v(y)\,dy .
$$
Thus the data determine the energy differences and endpoint rates in their respective reference units. Convexity makes $v$ nondecreasing. Reject a nonpositive gap $b_i$ or a descending rate pair. Otherwise define
$$
I_i=
\begin{cases}
(b_i/\phi_{i+1},\,b_i/\phi_i),&\phi_i<\phi_{i+1},\\[2pt]
\{b_i/\phi_i\},&\phi_i=\phi_{i+1}.
\end{cases}
\qquad \mathcal I= I_0\cap I_1 .
$$
With distinct endpoints the mean of a continuous nondecreasing profile lies strictly between them. Continuity gives positive length near each endpoint on which the opposite endpoint value cannot hold. With equal endpoints monotonicity forces a constant throughout that segment. These statements give both endpoint rules. Two open intervals give a nonempty interval precisely when the larger lower bound is strictly smaller than the smaller upper bound. Contact alone is empty. A singleton survives exactly when its value belongs to the other set, strictly inside if the other set is open. Two flat segments give a singleton exactly when their inferred values agree. Every nonempty result is bounded away from both zero and infinity.

**Attainability by one smooth Hamiltonian.** Fix $\eta\in\mathcal I$ and a segment with endpoint rates $p,q$ and target mean $m=b_i/\eta$. If $p=q$, take $v=p$. If $p<q$, let $\xi=1-(m-p)/(q-p)\in(0,1)$. Choose a nonnegative smooth bump $w$ of unit integral, symmetric about $\xi$ and supported strictly inside $(0,1)$. Set
$$
v(i+s)=p+(q-p)\int_0^s w(t)\,dt,\qquad 0\le s\le1 .
$$
Its mean is $p+(q-p)\int_0^1(1-t)w(t)\,dt=p+(q-p)(1-\xi)=m$. It is nondecreasing and constant near both ends. The two profiles therefore glue smoothly at the shared rate $\phi_1$ and extend constantly across the outer endpoints. At any feasible mechanical realization choose $J_0=\eta M_0c^2T$ and set
$$
h(J)=C_0+M_0c^2+\frac{J_0}{T}\int_0^{J/J_0}v(y)\,dy .
$$
This gives all three stipulated values, all three dwell rates, $h'=v/T>0$, and $h''=v'/(TJ_0)\ge0$. The construction proves sufficiency globally and gives the same labelled arm probabilities for every permitted choice. When both arms pass separately but $\mathcal I$ is empty, their joint records exclude the stipulated common convex energy/action law under the supplied registration and calibrations.

The exact displayed action-per-tick assignment is $A=g_wJ_0/T=\eta D/u_0$. The joint set is all $(D,\eta,A)$ with $D\in\mathcal D$, $\eta\in\mathcal I$, and that single relation for $A$. A chosen $D$ is shared by all three sectors. The reportable projection uses the actual open, closed or singleton sets above.

## 5. A complete record and a one-premise control

Take positive $M_*,T,c,g_w,g_c$. Use $(M_0,M_1,M_2)=M_*(1,2,4)$, $K=M_*/T^2$, $L=cT$ and $W=g_wM_*c^2$. Specify every point reading in the table in §2 as follows.

- The spring readings in order $01,02,12$ are $\cos\sqrt{3/2},\cos\sqrt{5/4},\cos\sqrt{3/4}$. They have $u=(1,1/2,1/4)$. Use the common rest release within the declared extension range.
- Take $P_i=M_*$ for each loaded sector. Use stationary linear potentials from zero at the lower endpoints with gaps $j\epsilon c^2$, where $2\epsilon>0$ is below the supplied weak-field tolerance along the paths. At all rows $z_j=g_cj\epsilon$. Each loaded work pair is $(j\epsilon W,-j\epsilon W)$. Both blanks have $(0,0)$.
- At length $jL$, the blank stroke has $(0,0)$ and the engaged stroke has $(j^2W/2,-j^2W/2)$. Record $d_1=3,d_2=5$. This gives $d_0=1,\lambda=1,\mathcal E=\{W/2\},\mathcal D=\{W\}$. All holders and losses can be zero. A displayed initial store level $(3+2\epsilon)W$, with capacity at least that large, covers the largest outward stroke $2W$ and lift $2\epsilon W$. Each return restores that initial level.
- Take $\phi_0=1/2,\phi_1=1,\phi_2=2$ radians. The two quadrature responses are exactly $\cos\phi_q,\sin\phi_q$ at each preparation. The signs, failures, histories, arm weights and support zeros are those in §2.

Both gaps $(b_0,b_1)=(1,2)$ give $I_0=I_1=(1,2)$. The compatible actions are exactly $1<\eta<2$, or $W<A<2W$. For an explicit interior realization take $h(J)=C_0+M_*c^2\,2^{J/J_0}$ and $\eta=2\ln 2$. At the registered tori $T h'(qJ_0)=2^q/2$. The smooth construction in §4 attains every other interior value. The mechanical and phase laws do not distinguish these values even with the example's masses, gains and tick held fixed.

**Remove only $h''\ge0$.** Keep $h$ smooth, $h'>0$, the same three masses, the same clock and quadrature band at the three observed tori, and every operating and observation premise. Pick any $\eta>0$. On a segment with positive endpoint rates $p,q$ and target mean $m=b_i/\eta>0$, choose smooth cutoffs $U,V$ between zero and one, each equal to one near its respective endpoint and zero outside disjoint narrow endpoint neighborhoods. Their integrals $\alpha,\beta$ can be made so small that $\alpha+\beta<1$ and $p\alpha+q\beta<m$. Put
$$
k=\frac{m-p\alpha-q\beta}{1-\alpha-\beta}>0,\qquad
v(i+s)=pU(s)+qV(s)+k[1-U(s)-V(s)] .
$$
This positive profile has exactly the required mean and is constant near either endpoint. Glue the two segments and integrate as in §4. All sampled values and rates, including every failure probability, are identical. No bound on rates between the sampled tori was supplied in this control. Thus the matched record permits arbitrarily small and arbitrarily large $\eta$ under positive rate alone. More generally positive mass gaps are still necessary, and the construction suffices for any such gaps and positive endpoint rates in the stipulated band.

## 6. Physical calibration and resources

The integer occupation is a native sector label. Across the two physical attachments the independently inferred mass ratios and phase readings become constraints on $J_0$ in units of $M_0c^2T$. The free energy offset cancels throughout. Even a singleton in those units leaves a physical calibration question. For example, where time and length have no independent dimensional standard, $T\mapsto sT$, $L\mapsto sL$, $K\mapsto K/s^2$, $J_0\mapsto sJ_0$, $h(J)\mapsto h(J/s)$ at fixed masses and gains preserves all the point readings and $\eta$ for any $s>0$. The echo intercept is retained in tick units. The spring extension ratio and static stroke energies are unchanged. Converting a displayed $A$ to physical action requires the physical factor $T/g_w$ or an independently calibrated equivalent. The conditional boost result has separate boost-generator premises and a supplied physical action scale. Identifying $J_0$ with $\hbar$ would require independent evidence.

Carrier preparation, a stable time transfer, initial angle reference, switch and quadrature calibration, the detector failure channel, storage and restoration are physical inputs. The table includes the failures but supplies no work measurement for running or restoring that detector or its controller. The source, reference, readout and store must be prepared again for fresh trials. Establishing an empirical action bound from this protocol would require independent evidence that the sector inertias and the measured phase rates belong to the same registered $h$ and that its convexity holds between the sampled occupations.

## Reviewed sources

The [native phase and action construction](native_phase_action_interface.md) supplies the occupation labels and canonical phase interface. The [finite conservation law](finite_conservation_and_record_access.md), [spring inertia ratios](sector_inertial_mass_ratios.md) and [work-scale calibration](spring_mass_scale_in_displayed_work.md) specify the separate mechanical premises. The [conditional boost relation](conditional_boost_mass_relation.md) has independent physical assumptions. DET Energy Research derived the interpolation bounds. DET Quantum Relativity independently verified their endpoints, both observation arms and the same-record construction after relaxing convexity.
