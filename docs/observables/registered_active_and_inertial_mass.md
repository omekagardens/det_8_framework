# Testing proportionality of active and inertial mass across three carrier sectors

Conditional theorem accepted after independent scientific review on 9 November 2026.

**Theorem.** Under the registered ideal experiment below, the complete population law admits positive inertial masses $M_i$ and positive active coefficients $A_i$ exactly when it satisfies the record law (1), the mechanical domain (2) and the static domain (3). On that domain it admits a common $k>0$ with $A_i=kM_i$ exactly when
$$
                    u_0w_0=u_1w_1=u_2w_2.
$$
The six dimensionless quantities here come from three signed spring readings and three pairs of clock readings. Equality tests whether the two independently measured sector profiles have the same relative values. The magnitude of $k$ requires scale calibration. Section 5 gives a single labelled law whose interpretation changes if static preparation labels 0 and 2 can be exchanged without a record.

## 1. Which complete law is being tested

Sectors $i=0,1,2$ use preparations $\delta_{00},\delta_{10},\delta_{11}$ respectively. The two possible internal states $10,01$ in sector 1 share its coefficients. A spring trial uses two independently prepared copies of the **entire** carrier. A static trial uses an equivalently prepared copy. Registration certifies that sector $i$ refers to the same complete carrier type, attachments, composition and relevant preparation in both modes. The coefficients persist across settings. In particular the zero-charge sector has positive baseline inertia and positive active coefficient in this model.

Each copy retains the ordered history $h=(a_h,b_1,b_2)$ with ideal $a_h\in\{E,F\}$ and two bits. The known eight-cell history law is
$$
 p_i(h)=\frac{q_{a_h}}4\left(1+\frac{\eta_{a_h}}2\,\mathbf 1_{\{i=1\}}\right),
 \qquad (q_E,\eta_E)=(2/3,1/8448),\quad (q_F,\eta_F)=(1/3,-1/4224).
$$
It sums to one because $\sum q_a=1$ and $\sum q_a\eta_a=0$. In particular $p_0=p_2$. Preparation labels are recorded externally. Intermediate and terminal internal states are marginalized with their original support zeros.

Let $I$ be spring mode and $A$ static mode, each chosen with probability $1/2$. Conditional on mode, each of its three settings has probability $1/3$. Write $F$ for the failure flag. The first test requires that there exist finite real readings $y_{ij}$ and finite signed pairs $z_i=(Z_{i-},Z_{i+})$ such that for **every** listed cell and every Borel reading set of the appropriate type,
$$
\begin{aligned}
 P(I,ij,h_1,h_2,Y\in B,F=0)&=\tfrac16\,p_i(h_1)p_j(h_2)\,\mathbf 1_B(y_{ij}),
       &&ij\in\{01,02,12\},\\
 P(A,i,h,Z\in E,F=0)&=\tfrac16\,p_i(h)\,\mathbf 1_E(z_i),
       &&i\in\{0,1,2\}.
\end{aligned}                                                           \tag{1}
$$
All other support has zero mass, including $F=1$. There are $3\cdot8^2=192$ spring cells and $3\cdot8=24$ static cells. Each mode sums to $1/2$. At a fixed setting the indicated point mass must be the same at every history. The spring histories have the specified product weights. For example, correct setting-wise mean readings together with history-dependent fluctuations would fail (1). This checks the whole observed law with the supplied record access and negligible backreaction.

## 2. Domains and inverse measurements

**Mechanical.** A common ideal spring of stiffness $K>0$ and equilibrium length $L$ is released from rest at extension $D$ with $0<D<L$. The signed ratio $x(T)/D$ is read at one common tick $T>0$. On the supplied strict first lobe, the accepted sector-inertia law gives $y_{ij}=\cos\sqrt{u_i+u_j}$, $u_i=C/M_i$ and $C=KT^2$. Require $-1<y_{ij}<1$, form $d_{ij}=(\arccos y_{ij})^2$ and require
$$
 u_0=\tfrac12(d_{01}+d_{02}-d_{12})>0,\quad
 u_1=\tfrac12(d_{01}+d_{12}-d_{02})>0,\quad
 u_2=\tfrac12(d_{02}+d_{12}-d_{01})>0.                                  \tag{2}
$$
These are the unique inverse values. Their pair sums are the measured $d_{ij}\in(0,\pi^2)$. Negative extension readings are admissible within the open interval. Its endpoints and any zero inverse-mass parameter lie outside the assumed physical domain.

**Static.** Use the supplied spherical complete-source profile supported inside radius $a>0$, with held clocks at $2a,3a,4a$ on a common radial axis. Its retained potential is $\Phi_i(r)=-G A_i/r+U_0+U_1 r$. The external constants $G,c,a$ are positive. The clock differences are relative to $3a$, with a common positive display gain $g$, registered channel signs and independently established zero instrumental offsets. With $H=gG/(12ac^2)$ and $b=gU_1a/c^2$ the displayed pair is $(-2HA_i-b,HA_i+b)$. Invert both coordinates and require
$$
 w_i=-(Z_{i-}+Z_{i+})>0,\qquad
 b_i=Z_{i-}+2Z_{i+},\qquad b_0=b_1=b_2=b.                               \tag{3}
$$
The pair recovered from $w_i,b_i$ is exactly $(-2w_i-b_i,w_i+b_i)$. The common gradient may have either sign, and no separate sign restriction is imposed on either channel. A zero $w_i$ is a recorded boundary outside the strictly positive source domain. The potential offset $U_0$ cancels. Instrumental offsets have their own independently supplied zeros.

## 3. Construction, local weak field and scales

Necessity of (1)–(3) follows from the specified preparations, first-lobe mechanics and signed clock equations. For sufficiency choose one mass scale $C>0$. With the common tick $T$, set $K=C/T^2$ and $M_i=C/u_i$. These choices reproduce each spring ratio, including its sign, using one stiffness and the stipulated release.

Choose one common $g>0$, set $H=gG/(12ac^2)$, and take
$$
 A_i=w_i/H,\qquad U_1=bc^2/(ga).
$$
These finite positive active coefficients and the single real gradient return both observed clock coordinates in every sector. The six settings, preparation histories, physical point masses and failure probabilities now reproduce (1) cell by cell. The construction allows the $A_i$ and $M_i$ to vary independently at this stage.

Weak-field feasibility can be enforced on the whole sampled radial segment. Write $x=r/a\in[2,4]$ and $f_i(x)=bx-12w_i/x$. Then
$$
                  \frac{\Phi_i(ax)}{c^2}=\frac{U_0}{c^2}+\frac{f_i(x)}g .
$$
For any prescribed local amplitude tolerance $\varepsilon>0$, take $U_0=0$ and one common $g>(4|b|+6\max_i w_i)/\varepsilon$. This makes $|\Phi_i|/c^2<\varepsilon$ for every sector and all $x\in[2,4]$. The design permits arbitrarily large finite common gain. If a calibration instead fixes $g$ or bounds its range, the constructed parameters must pass the local condition at an allowed value. For example, with $U_0$ free and the non-strict tolerance $\varepsilon$, the exact amplitude condition at a specified $g$ is $\max_{i,x} f_i(x)-\min_{i,x} f_i(x)\leq 2g\varepsilon$. Centering the largest and smallest potentials with one $U_0$ proves sufficiency. The argument concerns this finite segment and the retained potential amplitude. An affine gradient can grow without bound on an infinite ray, and physical clock-transfer or metric-remainder estimates would require separate evidence.

## 4. The proportionality decision

On the unrestricted feasible domain, positivity permits the identity
$$
              \frac{A_i}{M_i}=\frac{u_iw_i}{CH}.
$$
Write $J_i=u_iw_i$. If all $A_i=kM_i$, all $J_i=CHk>0$. Conversely if the three $J_i$ equal a common $J$, the same constructed world satisfies the proportionality equations with $k=J/(CH)>0$. If they differ, every unrestricted realization of the given law has unequal active-to-inertial ratios. At fixed positive $u_i$, the two constraints $w_1=(u_0/u_1)w_0$ and $w_2=(u_0/u_2)w_0$ constrain different clock amplitudes, so both are needed.

The normalized profiles are directly identified:
$$
 \frac{M_i}{M_0}=\frac{u_0}{u_i},\qquad
 \frac{A_i}{A_0}=\frac{w_i}{w_0},\qquad
 \frac{A_i/M_i}{A_0/M_0}=\frac{J_i}{J_0}.
$$
Here $C$ carries mass, $H$ inverse mass, and $u_i,w_i,b,J_i$ are dimensionless. With the same mass convention for $A_i$ and $M_i$, $k$ is dimensionless as well. Scaling $C,K,M_i$ together by any positive factor at fixed $T$ leaves all observations invariant. Changing $g$ scales $H$ with it and scales $A_i,U_1$ inversely, subject to the stated local domain. Even a proportional law leaves $k$ undetermined through the free mechanical scale alone. The test asks whether the three ratios are constant across sectors. Their common value need not equal one.

## 5. A discriminating law and a hidden registration exchange

Fix any dimensionless $s>0$. Use (1) with spring readings $y_{ij}=\cos\sqrt{d_{ij}}$ for
$$
                 (d_{01},d_{02},d_{12})=(3/2,5/4,3/4).
$$
All phases lie strictly in $(0,\pi)$. The static records and their inverses are as follows.

| Logged sector $i$ | $u_i$ | $M_i/C$ | $(Z_{i-},Z_{i+})/s$ | $w_i/s$ | $J_i/s$ |
| --- | ---: | ---: | --- | ---: | ---: |
| 0 | $1$ | $1$ | $(-9,5)$ | $4$ | $4$ |
| 1 | $1/2$ | $2$ | $(-5,3)$ | $2$ | $1$ |
| 2 | $1/4$ | $4$ | $(-3,2)$ | $1$ | $1/4$ |

Each signed clock pair yields the same $b=s$. For any common $C>0$ and a $g$ satisfying the segment bound, choose $M=C(1,2,4)$, $A=(s/H)(4,2,1)$ and $U_1=sc^2/(ga)$. These parameters realize the entire table. With faithful labels it rejects proportionality because $J=(4s,s,s/4)$. In particular this rejection occurs inside the unrestricted positive class.

Now keep the *logged* labels, readings, native histories, mode weights and access fixed. Withdraw only the cross-mode registration guarantee. In a second world, let $\pi$ exchange 0 and 2 and fix 1. The mechanics still prepares the true sectors it logs. In static mode nominal $i$ loads true sector $\pi(i)$, and the true active triple is now
$$
                         A'=(s/H)(1,2,4).
$$
Keep the same mechanics, $C,g,U_0,U_1$ and geometry. Each true $A'_i$ equals $[s/(HC)]M_i$, so this world has exact positive proportionality. But $A'_{\pi(i)}=A_i$ for every nominal setting, so the newly loaded clock pair equals the originally logged $z_i$ coordinate by coordinate. Also $p_{\pi(i)}(h)=p_i(h)$ for every history because $p_0=p_2$. For each clock event $E$, the second world's labelled probability is therefore
$$
 \tfrac16 p_{\pi(i)}(h)\mathbf 1_E(z'_{\pi(i)})
       =\tfrac16 p_i(h)\mathbf 1_E(z_i).
$$
Both worlds have the identical mechanical kernel and failure support. This establishes equality of every cell in (1), while the two worlds disagree about proportionality of the true packages. An exchange of unequal clock data in the log itself would be observable. The ambiguity arises because the physical preparation behind a retained label can be wrong when registration is untrusted.

More generally, if the only uncertainties are identity or this particular hidden exchange, test the two product triples $(u_iw_i)_i$ and $(u_iw_{\pi(i)})_i$. If neither is constant, rejection survives either assignment. If just one is constant, the law leaves the physical association decisive. Both are constant exactly when $u_0=u_2$, $w_0=w_2$ and $u_0w_0=u_1w_1$. Sector 1 fixes the same common product under both assignments. Comparing the two products at sector 0 then gives $w_0=w_2$, and comparing sectors 0 and 2 gives $u_0=u_2$. The converse follows by substitution. For example $u=(1,1/2,1)$ and $w=s(1,2,1)$ give $J_i=s$ under both assignments. This successful test cannot independently certify registration.

## 6. Reading the decision

| Available evidence in the registered design | Decision |
| --- | --- |
| Complete ideal law contradicts (1), (2) or (3) | The unrestricted model is inconsistent. A common background mismatch, positive failure probability, or zero inferred active amplitude belongs here. |
| Complete law is admissible and at least two $J_i$ differ | Positive active coefficients and inertias fit, and every such fit excludes common proportionality. |
| Complete law is admissible and all three $J_i$ agree | Every registered realization has a common positive active-to-inertial ratio. |
| Required setting or reading is missing, or registration, first-lobe assurance or readout calibration is unavailable | The registered test lacks a premise. A finite collection omitting a setting differs from an exact population law assigning it zero probability. |

Physical interpretation requires faithful preparation of equivalent complete packages, persistence under loading, the independently justified spherical source and common background, stable spring and tick, and known frame, clock-transfer and instrumental-zero conventions. Residuals from stresses, supports, references and controllers must be included or controlled. Actual acquisition and failures require a specified observation law with their full denominator. Preparation, loading, holding, readout and resetting costs were not measured. The result is an ideal relative-coefficient theorem under these mechanical and static attachments.

## Reviewed dependencies

The [sector spring inverse](sector_inertial_mass_ratios.md) and [finite conserved carrier and history law](finite_conservation_and_record_access.md) provide the mechanical and native inputs. The active-source attachment and cross-mode registration are supplied here. Frozen proof SHA-256 `063d2591e650a78fac145c3b6ba2444f013830ed716c888a8855626a435c6e92`. Independent scientific review SHA-256 `f50f0e9ad4b5e234b94345559f3658a47dc52646c2c67ea2ac88468681df247b`.
