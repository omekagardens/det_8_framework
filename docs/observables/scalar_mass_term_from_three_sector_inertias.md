# Testing a scalar mass term against three sector inertias

Three labelled, strictly increasing inertial mass ratios and three scalar settings identify at most one positive power exponent. Let $m_i=M_i/M_0$, with $1=m_0<m_1<m_2$, and let $A_i>0$ be the mean scalar response from $a$ to $b$ in setting $i$. Put $Y_i=1/\sqrt{A_i}$. On a compatible record the quadratic hypothesis has the exact observational test
$$
\frac{Y_2-Y_0}{Y_1-Y_0}=\frac{m_2^2-1}{m_1^2-1}.
$$
A pass also requires the common apparatus to reproduce **all nine** scalar means. Under the proposed positive quadratic conversion $k=(M_0 c/J_s)^2$, that full record fixes $J_s/(M_0 c\ell)=\sqrt{(h/k)/2}$. Neither an absolute increment dial nor an absolute inertial mass is part of the record.

## Two preparations linked by a registered sector setting

**Spring.** Use the accepted common stiffness $K>0$, common tick $T>0$, registered signed extension ratio $y_{ij}$, and independently assured phase $0<\omega_{ij}T<\pi$. The pair setting $(i,j)$ is uniform on $01,02,12$; the two carrier copies have independent native histories conditional on their preparations $00,10,11$ for sectors $0,1,2$. For each history $\mathfrak h=(a,b_1,b_2)$, with $a=E,F$ and each labelled bit pair, its original probability is
$$
p_i(\mathfrak h)=\tfrac{q_a}{4}[1+\tfrac{\eta_a}{2}\mathbf1_{i=1}],
\quad (q_E,\eta_E)=(2/3,1/8448),\quad(q_F,\eta_F)=(1/3,-1/4224).
$$
Each of the 192 labelled setting/history cells keeps weight $p_i(\mathfrak h_1)p_j(\mathfrak h_2)/3$ and its mechanical point reading $y_{ij}$. From $-1<y_{ij}<1$, set $s_{ij}=(\arccos y_{ij})^2$. For $\{i,j,l\}=\{0,1,2\}$, define $w_i=(s_{ij}+s_{il}-s_{jl})/2$ using the unordered pairs. The spring law gives $w_i=KT^2/M_i$. Require all $w_i>0$, set $m_i=w_0/w_i$, and check the stipulated strict mass order. These conditions with the stated cell law preserve the complete spring preparation. They do not impose additivity of its three masses.

**Scalar.** Use the two supported four-event orders, the diamond $a\prec b,x\prec y$ with $b,x$ incomparable (both lie between $a,y$), and the chain $a\prec b\prec x\prec y$. The inaccessible $x$ participates in propagation. The common chain fraction is $\pi\in[0,1]$, with diamond fraction $1-\pi$; conditional marks retain their preparation law. This selected mixture is independent of the two spring histories. Its weights are not the native unconditional probabilities of the two structural rows. The apparatus must reproducibly associate the labelled sector $i$ with the scalar setting $u_i=k m_i^\nu$, $k>0,\ \nu>0$, while keeping $d\ge0,\ h=2/\ell^2>0,\ g>0,\pi$ common across settings.

At each setting the three blank-subtracted means $A_i,B_i,C_i$ use the registered unit impulses and target/source addresses $(b,a),(y,b),(y,a)$. Introduce normalized quantities
$$
v_i=m_i^\nu,\quad H=h/k,\quad D=d/k,\quad \Gamma=g/k,\quad
\alpha=D+H,\quad t_i=v_i+\alpha,\quad r_i=H/t_i .
$$
The actual mass term is $d+kv_i$. Applying the accepted finite inverse on each **full** order before mixing gives
$$
A_i=\frac{2\Gamma H}{t_i^2},\qquad
\frac{B_i}{A_i}=1-3\pi+2\pi r_i,\qquad
\frac{C_i}{A_i}=1+4(1-3\pi)r_i+4\pi r_i^2. \tag{1}
$$
For this particular pair of orders the corrected averaged full-operator calculation gives the same means. Rebuilding the layer law on the visible three-chain would discard the hidden paths. Negative values of $B_i$ or $C_i$ are allowed.

## Exact exponent test

Require finite real readings, $A_i>0$ and $Y_0<Y_1<Y_2$. Equation (1) gives $Y_i=(m_i^\nu+\alpha)/\sqrt{2\Gamma H}$. Taking two differences eliminates both nuisance combinations:
$$
R_Y:=\frac{Y_2-Y_0}{Y_1-Y_0}=\frac{m_2^\nu-1}{m_1^\nu-1}.
$$
Let $b=\log m_2/\log m_1>1$ and $z=m_1^\nu>1$. The right side becomes $(z^b-1)/(z-1)$, the mean of $bt^{\,b-1}$ on $1\le t\le z$. The integrand is strictly increasing, so extending the interval strictly increases this mean. Its limits are $b$ as $z\downarrow1$ and infinity as $z\to\infty$. Thus the contrast equation has a positive solution **exactly when $R_Y>b$**. Equality is excluded. When this test passes there is one root $z>1$, giving $\nu=\log z/\log m_1$. This establishes global uniqueness within the proposed positive-power family. Full feasibility also needs the following checks.

## Restoring the nuisance parameters and checking all nine means

Use that unique exponent to compute $v_i=m_i^\nu$. The first two settings now provide known distinct dimensionless increments $v_0=1<v_1$ for the accepted two-setting inverse.

1. Set $S=\sqrt{A_0/A_1}$. Require $1<S<v_1/v_0$, then set $\alpha=(v_1-Sv_0)/(S-1)$ and $t_i=v_i+\alpha$ for all three settings. This gives $\alpha>0$.
2. Write $b_i=B_i/A_i,\ c_i=C_i/A_i$, and compute
   $$
   Z=\frac{b_0-b_1}{2(1/t_0-1/t_1)},\qquad
   \pi=\frac{1-b_0+2Z/t_0}{3}.
   $$
   The divisor is positive. Require $0\le\pi\le1$. For $0<\pi\le1$, require $Z>0$ and put $H=Z/\pi$, since $Z=\pi H$. This includes pure chain. For $\pi=0$, require $Z=0,\ b_0=b_1=1$, and set $H=(c_0-1)t_0/4$, requiring $H=(c_1-1)t_1/4$ as well. This uses the outer response in pure diamond.
3. Require $0<H\le\alpha$; set $D=\alpha-H$ and $\Gamma=A_0 t_0^2/(2H)>0$. Check all three equalities (1) at **each** of $i=0,1,2$, including the third pair and outer responses. Any failure rejects the proposed joint model. Equality $H=\alpha$ admits zero offset.

Necessity follows from (1). Conversely, a passing record is realized by choosing any $k>0$, setting $h=kH,\ d=kD,\ g=k\Gamma,\ \ell=\sqrt{2/(kH)}$, and using the two specified scalar orders with the recovered $\pi$. The three channels give all nine observed means. For any $M_0,T>0$, choose $M_i=m_i M_0,\ K=w_0M_0/T^2$; the spring then reproduces every signed reading and its original joint history law. This constructs the common labelled setting correspondence stipulated by the control without identifying histories in different apparatuses. The result separates an incompatible record, a compatible unique quadratic exponent, and a compatible unique nonquadratic exponent.

## Two scalar settings can give identical laws

Keep the entire three-pair spring arm in both worlds. Take $M_i=M_0(1,2,3)_i,\ K=M_0/T^2$, with identical $T$ and initial release conditions. The three squared phases $3/2,4/3,5/6$ all lie in $(0,\pi^2)$; the three mechanical point readings and all 192 cell probabilities agree. Retain only the scalar settings $m=1,2$. Fix $U>0$ in inverse-length-squared units, $h=U,\ g=g_0>0,\ \pi=1/2$ in both worlds.

| Supplied coupling | $k$ | $d$ | $d+k m^\nu$ at $m=1,2$ | At the omitted $m=3$ |
|---|---:|---:|---|---:|
| Quadratic, $\nu=2$ | $U$ | $2U$ | $3U,\ 6U$ | $11U$ |
| Linear, $\nu=1$ | $3U$ | $0$ | $3U,\ 6U$ | $9U$ |

At the retained settings the same $h$ makes the dimensional denominators $4U,7U$ in both worlds. Even the full-order conditional propagators agree on each topology before applying the same mixture and gain, so all six labelled means agree. There is no dial reading for $u_i$ in this record. The two worlds differ at the third setting, including in $A_2$. This is a reduced-record ambiguity between admissible powers with every retained preparation preserved.

## What the quadratic calibration means

For $\nu=2$ only, a positive action scale in $k=(M_0c/J_s)^2$ gives
$$
\ell\sqrt{k}=\sqrt{2/H},\qquad
\boxed{\frac{J_s}{M_0c\ell}=\sqrt{H/2}} .
$$
A signed coefficient allowed inside the square would fix only its magnitude. The record fixes $H,D,\Gamma,\pi,\nu$ and the spring’s $w_i$. Its scalar freedom is exactly one common factor: multiplying $k,h,d,g$ by $\lambda>0$ divides $\ell$ by $\sqrt\lambda$. The remaining spring freedoms are $M_0>0,T>0$, with $K=w_0M_0/T^2$. In the quadratic interpretation a further change $M_0\mapsto\mu M_0$ with this scalar rescaling gives $J_s\mapsto\mu J_s/\sqrt\lambda$ at fixed supplied $c$. A physical mass and scalar length calibration, or an equivalent dimensional reference, would be needed to give $J_s$ in joule-seconds.

To compare against an occupation action reported in units $M_0c^2T$, the baseline carrier and tick would have to be registered in both experiments. One must also measure $\ell/(cT)$ independently; then $J_s/(M_0c^2T)=\sqrt{H/2}\,\ell/(cT)$ can be compared with the separately admitted occupation-action set. The earlier spatial-mode comparison used a registered ruler and a different physical coupling. Here the finite observations test quadratic dependence at the three prepared masses under the proposed power family. Many other functions agree at those three points. No universal functional law, common occupation action, native length unit or empirical sector-to-field coupling follows from these records.

[Inertial mass ratios](sector_inertial_mass_ratios.md) · [Scalar length with one hidden event](scalar_length_with_one_hidden_event.md) · [Occupation and spatial actions](comparing_occupation_and_spatial_actions.md)
