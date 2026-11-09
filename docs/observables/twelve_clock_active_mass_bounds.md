# How twelve exterior clocks can exclude active-to-inertial mass proportionality

Conditional theorem accepted after independent scientific review on 9 November 2026.

**Result.** Six signed outer-minus-inner clock differences give an open interval of possible total active masses, with endpoints determined by the extremes of a single Newtonian kernel. When the three gradient-cancelled axis readings agree within each sector, this interval is exact for the entire recorded vector. In that subclass an ideal three-sector law admits a common positive active-to-inertial ratio exactly when its three inertia-scaled intervals have a common point and the registration, history, mechanical and background conditions below hold. A realizable example has identical spring readings in all three sectors, twice the clock signal in the middle sector, and disjoint scaled intervals. All these statements concern the stipulated observation law at retained order.

## 1. What counts as an ideal record

Sectors $i=0,1,2$ prepare $\delta_{00},\delta_{10},\delta_{11}$. Inversion of the mechanics and interpretation of the clocks require registered equivalent copies of the whole sector package in both modes. The two internal states of sector 1 share its coefficients. Allow each sector its own fixed finite positive atomic measure $\mu_i$, of total $A_i>0$, invariant under inversion about the common origin, supported strictly inside $|y|<a$. Keep the same axes, references, gain, signs, instrumental zeros and geometry in all sectors.

Each copy records $h=(j,b_1,b_2)$, $j\in\{E,F\}$, with two bits. Its eight probabilities are
$$
 p_i(h)=\frac{q_j}{4}\left(1+\frac{\eta_j}{2}{\bf1}_{i=1}\right),
 \qquad (q_E,\eta_E)=(2/3,1/8448),\quad(q_F,\eta_F)=(1/3,-1/4224).
$$
Their sum is one since $\sum q_j\eta_j=0$. For every labelled cell and Borel reading event of the appropriate type, require
$$
\begin{aligned}
 P(I,ij,h_1,h_2,Y\in S,F_{\rm fail}=0)
   &=p_i(h_1)p_j(h_2){\bf1}_{S}(y_{ij})/6,\qquad ij=01,02,12,\\
 P(A,i,h,\Delta\in E,F_{\rm fail}=0)
   &=p_i(h){\bf1}_{E}(\Delta_i)/6,\qquad i=0,1,2 .
\end{aligned}
$$
Here $y_{ij}$ is a finite signed spring ratio and $\Delta_i$ is one finite ordered **six-vector** in direction order $+e_1,-e_1,+e_2,-e_2,+e_3,-e_3$. Each setting has the same point reading across its native histories. There are 192 mechanical and 24 static cells, each mode has probability $1/2$, and every other cell, including each failure cell, has probability zero. The observation contract includes the joint record at each static setting. Marginal summaries alone do not establish that contract.

On the stipulated strict first lobe, require $-1<y_{ij}<1$. Put $D_{ij}=(\arccos y_{ij})^2=D_{ji}$. For distinct sector indices $i,j,\ell$, set
$$
 u_i=(D_{ij}+D_{i\ell}-D_{j\ell})/2
$$
and require all three $u_i>0$. Then $u_i+u_j=D_{ij}\in(0,\pi^2)$. The registered rest release at $0<D<L$, common stiffness $K_{\rm sp}>0$ and tick $T>0$ give $M_i=C/u_i$, $C=K_{\rm sp}T^2>0$, and exactly $y_{ij}=\cos\sqrt{u_i+u_j}$. One choice of the common scale suffices for all settings. The spring observation identifies all three $u_i$.

## 2. What the six clock differences measure

There are twelve clock positions $2an,4an$, $n\in\{\pm e_1,\pm e_2,\pm e_3\}$. In the static coefficient model
$$
 \Phi_i(x)=U_0+B\cdot x-G\int |x-y|^{-1}\,d\mu_i(y),\qquad
 \Delta_i(n)=g[\Phi_i(4an)-\Phi_i(2an)]/c^2 .
$$
The normalized raw reading $d_i(n)=ac^2\Delta_i(n)/(gG)$ has units of mass for the supplied positive $a,c,g,G$ (the display gain is removed by division). With $v=y/a$, define $k_n(v)=|2n-v|^{-1}-|4n-v|^{-1}$. The negative potential and outer-minus-inner convention give
$$
 d_i(n)=\int k_n(y/a)\,d\mu_i(y)+\frac{2a^2}{G}B\cdot n .
$$
The kernel is dimensionless, $B$ is an acceleration and $a^2 B/G$ has units of mass. The offset $U_0$ cancels. The squared outer distance minus the squared inner distance in these coordinates is $12-4n\cdot v>0$ even on the closed unit ball, so each $k_n>0$.

Form the half-difference $o_{ij}=[d_i(+e_j)-d_i(-e_j)]/2$ and the half-sum $e_{ij}=[d_i(+e_j)+d_i(-e_j)]/2$, where here $j=1,2,3$ labels an axis. Inversion symmetry and $k_{-n}(v)=k_n(-v)$ cancel the source from the odd part. Require $o_{0j}=o_{1j}=o_{2j}=o_j$ component by component. This is exactly the common-gradient condition, with $B_j=Go_j/(2a^2)$. Each even part must be strictly positive by positivity of the kernel and total mass. Raw individual differences can have either sign. Retain all three even parts and write
$$
 s_i=\tfrac13\sum_j e_{ij}=\int K(y/a)\,d\mu_i(y),
 \qquad K(v)=\tfrac16\sum_n k_n(v).
$$

## 3. Exact directional extrema and strict mass bounds

Each inverse distance is harmonic in $v$ on a neighborhood of the closed unit ball because its sensor is at radius 2 or 4. Their difference and finite mean are harmonic there. On the boundary write $t_j=v_j^2$, so $t_j\ge0$, $\sum t_j=1$. Opposing directions contribute the pair mean
$$
 P_R(t)=\tfrac12\big[(R^2+1-2R\sqrt t)^{-1/2}+
                         (R^2+1+2R\sqrt t)^{-1/2}\big],\qquad
 H(t)=P_2(t)-P_4(t).
$$
Thus $K(v)=\sum_jH(t_j)/3$ on that boundary. Convexity of this particular **difference** follows by the convergent even binomial expansion
$$
 H(t)=\sum_{m\ge0}\frac{\binom{4m}{2m}}{4^{2m}}
 \left[\frac{(4/5)^{2m}}{\sqrt5}-\frac{(8/17)^{2m}}{\sqrt{17}}\right]t^m .
$$
Both expansion arguments have modulus at most $4/5<1$, and each coefficient is strictly positive. In particular the linear term makes $H$ strictly increasing and the quadratic term gives strict convexity on $[0,1]$. Jensen's inequality gives the minimum when all $t_j=1/3$. The chord bound $H(t)\le(1-t)H(0)+tH(1)$ gives the maximum when the squared components are a permutation of $(1,0,0)$, with strict inequality elsewhere. The exact constants are
$$
 \begin{aligned}
 \kappa_- &=\tfrac12\left[(5-4/\sqrt3)^{-1/2}+(5+4/\sqrt3)^{-1/2}
                  -(17-8/\sqrt3)^{-1/2}-(17+8/\sqrt3)^{-1/2}\right],\\
 \kappa_+ &=\tfrac13\left[\tfrac25+2(1/\sqrt5-1/\sqrt{17})\right].
 \end{aligned}
$$
Indeed $H(1)=2/3-4/15=2/5$. The eight unit body diagonals minimize and the six unit axis points maximize. Strict convexity gives distinct extrema and hence a nonconstant harmonic function. The strong maximum and minimum principles give $\kappa_-<K(v)<\kappa_+$ throughout the open ball. Positivity on the comparison ball gives $\kappa_->0$. The center provides the check $K(0)=1/4$.

Every allowed source therefore satisfies
$$
                   A_i\in I_i=(s_i/\kappa_+,\ s_i/\kappa_-).                \tag{1}
$$
Neither endpoint is attained by positive mass on strict interior atoms. A boundary atom would change the source class.

## 4. Sharpness while holding every reading fixed

Fix a sector with $e_{i1}=e_{i2}=e_{i3}=s_i>0$ and a compatible odd vector $o$. For each interior $v$, let $Q_v$ be the probability measure giving equal weight to the sign-and-permutation images of $av$ (equivalently average over the finite group with multiplicities). Its atoms are interior. It is centered, inversion symmetric and has unit mass. Its six source responses are equal because the group acts transitively on the six directions. Their common value is $K(v)$, since their mean is the group average of the invariant function $K$.

Given any $A\in I_i$, one has $\kappa_-<s_i/A<\kappa_+$. Take $v_-=\rho(1,1,1)/\sqrt3$ and $v_+=\rho e_1$, with $0<\rho<1$ close enough to 1 that $h_-=K(v_-)<s_i/A<h_+=K(v_+)$. Continuity at the two boundary extrema guarantees such a radius. With $\theta=(s_i/A-h_-)/(h_+-h_-)\in(0,1)$, set
$$
                   \mu_i=A[(1-\theta)Q_{v_-}+\theta Q_{v_+}].
$$
This source has total $A$ and gives $A[(1-\theta)h_-+\theta h_+]=s_i$ in **each** of the six directions. With the same $B$ it gives each raw reading $s_i\pm o_j$ in mass units. Conversion back to $\Delta_i$ uses the same calibration. For either extremizing direction $v_*$ of unit length, the sources $[s_i/K(\rho v_*)]Q_{\rho v_*}$ reproduce that very same six-vector for every $0<\rho<1$, and approach the respective limiting total as $\rho\uparrow1$. This proves a genuine interval of positive width at a fixed joint observation.

Profiles may be chosen independently between sectors. Within a realized world each sector's profile and inertia belong to the same registered package in both modes. Changing a profile between candidate worlds preserves the native law and spring coefficients under the supplied model. Using one $C$, one $B$, the original instrument settings and the full observation law in §1 reproduces all 216 cells and every support zero. Thus for equal-even records meeting §§1–2 the unrestricted coefficient model is realizable and (1) is the exact mass set sector by sector.

## 5. Proportionality and a realizable rejection

A common $A_i=kM_i$, $k>0$, requires a common value $q=kC=u_iA_i$. For equal-even data satisfying the other checks the exact test is
$$
 \max_i\frac{u_i s_i}{\kappa_+}
       \;<\; \min_i\frac{u_i s_i}{\kappa_-}.                               \tag{2}
$$
If it holds, choose any $q$ strictly between the two sides and realize $A_i=q/u_i$ by §4 in every sector. This constructs a proportional world. Other compatible worlds can have different mass ratios, as changing only one interior mass preserves the law. If equality holds in (2)'s two sides the open intervals have no common point, even though their closures touch.

For unequal even components the common gradient, component positivity, history, mechanical, and mass bounds remain necessary. Failure of the strict inequality excludes a proportional realization. Passing (2) alone leaves feasibility unresolved because the orbit construction enforces equal responses and can change the measured vector. Failure of a basic record condition rejects the stipulated observation model itself. A proportionality rejection has physical interpretive content within this model when the unrestricted record can be realized.

For an explicit example fix $m>0$, $C>0$, $M=(C,C,C)$, $K_{\rm sp}=C/T^2$ and the common rest release. Then $u=(1,1,1)$ and all three readings are $\cos\sqrt{2}$ on the open first lobe. Set $U_0=0,\ B=0$, and take the registered central atomic measures $(m\delta_0,2m\delta_0,m\delta_0)$. The six raw readings **in every direction** for sector $i$ equal
$$
            \Delta_i(n)=\frac{gG}{4ac^2}A_i,\qquad A=(m,2m,m).
$$
These values with the weights and support in §1 specify the whole ideal law. To see the strict separation without numerical rounding, $1/6<H(0)=1/\sqrt5-1/\sqrt{17}<3/10$ follows from $5/12<1/\sqrt5<1/2$ and $1/5<1/\sqrt{17}<1/4$. Hence $\kappa_-=H(1/3)>1/6$ and $\kappa_+=[2/5+2H(0)]/3<1/3$. Since $\kappa_+<2\kappa_-$, the lower mass bound of sector 1, $2m/(4\kappa_+)$, exceeds the upper bound $m/(4\kappa_-)$ of sector 0. An unrestricted realization exists, yet even allowing arbitrary admitted sector shapes cannot restore proportionality. For any prescribed local amplitude tolerance $\varepsilon>0$, choose $0<m<\varepsilon ac^2/G$. Over all sampled exterior radial segments $|x|\ge2a$, the strongest source then has $|\Phi|/c^2\le Gm/(ac^2)<\varepsilon$. The strict separation survives that rescaling at fixed gain and geometry.

Equivalently (2) compares the dimensionless ratio $\max_i(u_i s_i)/\min_i(u_i s_i)$ to $\kappa_+/\kappa_-$. The masses in (1) and the common $q$ are in calibrated mass units. Converting $q$ to a numerical $k$ requires the mechanical scale $C$ as well. The sharp sets describe the exact retained-order coefficient law. At fixed gain a separately specified field-amplitude or higher-order error budget could further restrict arbitrary input data. Actual use would require measured source support, registration, clock positioning, transfer and calibration, and a controlled weak-field approximation. The witness establishes a mathematical rejection under the supplied Newtonian attachment.

The operative inputs are the E46 selection, its independent admission review, and the published registered carrier law. The finite-array nonidentifiability theorem concerns universal exact recovery and is consistent with (1). The CL068 binding-work result is a separate measurement.

## Reviewed dependencies

The [registered carrier experiment](registered_active_and_inertial_mass.md) supplies the mechanical and native history laws. The [finite exterior-array theorem](finite_exterior_clocks_and_total_mass.md) establishes the limit on exact total-mass recovery. These finite bounds use the twelve calibrated positions and strictly interior source support specified above.

Frozen proof SHA-256 `8f43982a59535bd1682975f0644b84670a08d091eec3ea29f733e9ecec235de9`. Independent scientific review SHA-256 `faf8818263d18ad75461dc912f265c4f5fbaa4e535c8b46be31f55de9c7800f4`.
