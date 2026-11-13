# Positive stationary wavefield dynamics across all four-birth branches

**Decision.** Sampling a single spatial probe cannot extend the stationary four-chain oscillator construction to any of the remaining 14 four-birth structural orders: distinct sampling times fail every incomparable pair, and even permitting equal sampling times at one point fails incomparability non-transitivity on 11 rows, fails online adaptedness across the entire fork prefix $I_x=\{a\}$, and collapses distinct-birth observables on all remaining non-chain rows. Introducing one compact anti-periodic spatial coordinate on $\mathbb R\times S_L^1$ ($L=4c\tau$) resolves the obstruction completely. An explicit minimal-denominator adapted causal embedding in $\frac13\mathbb Z^2$, paired with a single 12-mode positive-Hamiltonian traveling-wave scalar field in its unique centered stationary Gaussian ground state on $L^2(\mathbb R^{12})$, realizes the exact target-first Johnston causal commutator, strictly positive-definite complex and real branch covariances, positive-variance stagewise commutator zero modes, and exact branchwise and unread old-field Weyl-algebra preservation across all 15 structural rows (all 60 marked histories per prepared source, weight $1320/1320$) with zero feedback or reweighting of the native growth law. This is a conditional spacetime and positive-generator attachment, not a derivation of native geometry, physical calibration, or non-chain $3+1$D gravitational sourcing.

---

## 1. Context, inputs, and single-point obstruction

In the accepted [stationary four-chain dynamics](stationary_dynamics_for_four_chain_fields.md) and its [local $3+1$D scalar source lift](local_scalar_source_for_four_chain_field.md), a positive quadratic oscillator generator and stationary Gaussian ground state were attached exclusively to the total-chain structural row $a\prec b\prec x\prec y$ ($I_x=\{a,b\},\ I_y=\{a,b,x\}$), which carries source-conditioned probabilities $779/1320$ and $574/1320$ ($779/5280$ and $574/5280$ per fair suffix-mark pair). The remaining 14 structural rows (56 of the 60 marked histories per prepared source) were left `"unavailable"`. Conversely, the accepted [kinematic Gaussian field-transport note](gaussian_field_transport_on_native_histories.md) realized the target-first causal commutator across all 15 structural rows while preserving unread old-field marginals—avoiding the stagewise spectral obstruction established in [spectral covariance under native growth](spectral_covariance_under_native_growth.md)—but used history-dependent linear combinations of three abstract canonical pairs without a stationary positive generator, wave equation, or causal cone. The complete native continuation weights and mark rules are fixed throughout by the [finite interval and source specification](finite_interval_action_and_source_preparation.md) and the [prepared source ledger](native_source_readout_response.md).

Retain the target-first causal convention of [Gaussian field transport](gaussian_field_transport_on_native_histories.md). On any realized strict partial order $\prec$ with vertex set $\{a,b,x,y\}$, write $c_{rs}=\mathbf 1_{\{s\prec r\}}$ (target row $r$, source column $s$) and $D_{rs}=\beta(c_{rs}-c_{sr})$ for one supplied $\beta>0$. Two distinct vertices satisfy $r\parallel s$ when neither $r\prec s$ nor $s\prec r$ holds. The prescribed field commutator is
$$
[\phi_r,\phi_s]=iD_{rs}I=i\beta(c_{rs}-c_{sr})I=
\begin{cases}
+i\beta I,& s\prec r,\\
-i\beta I,& r\prec s,\\
0,& r\parallel s\ \text{or}\ r=s.
\end{cases}
\tag{1}
$$
In particular, the prepared prefix $a\prec b$ fixes $[\phi_a,\phi_b]=-i\beta I$ and $[\phi_b,\phi_a]=+i\beta I$. As noted in [Gaussian field transport](gaussian_field_transport_on_native_histories.md) and [spectral covariance under native growth](spectral_covariance_under_native_growth.md), target-first indexing transposes the source-first convention of [Johnston, arXiv:0909.0944v2, §II Eqs. (18)–(23)](https://arxiv.org/pdf/0909.0944v2).

Among the 15 structural continuations above $a\prec b$, row $I_x=\{a,b\},\ I_y=\{a,b,x\}$ is the unique total chain: when $I_x=\varnothing$ we have $x\parallel a$ and $x\parallel b$; when $I_x=\{a\}$ we have $b\parallel x$; and when $I_x=\{a,b\}$ with $I_y\subsetneq\{a,b,x\}$, maximal birth of $y$ leaves $y\parallel u$ for every $u\in\{a,b,x\}\setminus I_y$. Hence every one of the 14 non-chain structural rows contains at least one incomparable pair $r\parallel s$.

**Theorem 1 (Single-point obstruction on all 14 non-chain rows).** *Let $\phi(t)=\Psi(t,x_*)$ be a linear field on a nontrivial Hilbert space $\mathcal H\ne\{0\}$ ($I\ne0$) sampled at a single spatial point $x_*$ such that assigned sampling times satisfy*
$$
[\phi(t_r),\phi(t_s)]=i\beta\,\operatorname{sign}(t_r-t_s)I,\qquad \beta>0,
\tag{2}
$$
*with $\operatorname{sign}(u)=+1$ for $u>0$, $-1$ for $u<0$, and $0$ for $u=0$. Write $\phi_r=\phi(t_r)$ for $r\in\{a,b,x,y\}$.*

1. *(Distinct ticks).* *If $t_r\ne t_s$ whenever $r\ne s$, no non-chain row can satisfy (1).*
2. *(Coincident ticks permitted).* *Even if equal ticks $t_r=t_s$ are permitted:*
   - *Non-transitivity of $\parallel$ excludes offline (branch-by-branch) all 11 rows containing three vertices $u,v,w$ with $u\prec v$, $w\parallel u$, and $w\parallel v$.*
   - *Online adaptedness—requiring $t_x=t_x(I_x)$ to be fixed at the third birth before $I_y$ is drawn—excludes the entire fork block $I_x=\{a\}$ (all 5 rows, including both weak-order rows in that block).*
   - *Linear independence of distinct-birth observables (equivalently nondegeneracy of the real symmetrized covariance $V(H)=\operatorname{Re}W(H)$) excludes the sole remaining non-chain row $I_x=\{a,b\},\ I_y=\{a,b\}$, as well as all three weak-order non-chain rows offline.*

*Proof.*
(1) Choose $r\parallel s$ ($r\ne s$) on a given non-chain row. Equation (1) requires $[\phi_r,\phi_s]=0$, whereas $t_r\ne t_s$ in (2) gives $[\phi(t_r),\phi(t_s)]=\pm i\beta I\ne0$ because $\beta>0$ and $I\ne0$ on $\mathcal H\ne\{0\}$.

(2) Suppose equal ticks are permitted. Comparing (1) and (2) on every pair $(r,s)$ requires
$$
s\prec r\iff t_s<t_r,\qquad r\prec s\iff t_r<t_s,\qquad r\parallel s\iff t_r=t_s.
\tag{3}
$$
Because equality on $\mathbb R$ is transitive, $w\parallel u$ and $w\parallel v$ imply $t_w=t_u$ and $t_w=t_v$, hence $t_u=t_v$, which contradicts $t_u<t_v$ whenever $u\prec v$. Checking the 14 non-chain rows explicitly exhibits such a $\mathbf 2+\mathbf 1$ triple $(u,v,w)$ on 11 rows:
- **All 6 rows with $I_x=\varnothing$** ($I_y=\varnothing,\{x\},\{a\},\{a,b\},\{a,x\},\{a,b,x\}$): $a\prec b$ with $x\parallel a$ and $x\parallel b$, so $(u,v,w)=(a,b,x)$.
- **3 of the 5 rows with $I_x=\{a\}$**: for $I_y=\varnothing$, $a\prec b$ with $y\parallel a,y\parallel b$ gives $(u,v,w)=(a,b,y)$; for $I_y=\{a,b\}$, $b\prec y$ with $x\parallel b,x\parallel y$ gives $(u,v,w)=(b,y,x)$; for $I_y=\{a,x\}$, $x\prec y$ with $b\parallel x,b\parallel y$ gives $(u,v,w)=(x,y,b)$.
- **2 of the 3 non-chain rows with $I_x=\{a,b\}$**: for $I_y=\varnothing$, $a\prec b$ with $y\parallel a,y\parallel b$ gives $(u,v,w)=(a,b,y)$; for $I_y=\{a\}$, $b\prec x$ with $y\parallel b,y\parallel x$ gives $(u,v,w)=(b,x,y)$.

Only 3 non-chain rows are strict weak orders (transitive $\parallel$): row $I_x=\{a\},\ I_y=\{a\}$ ($b,x,y$ pairwise incomparable above $a$), row $I_x=\{a\},\ I_y=\{a,b,x\}$ (the diamond with $b\parallel x$), and row $I_x=\{a,b\},\ I_y=\{a,b\}$ (the upper fork with $x\parallel y$).

Now impose online adaptedness at the third birth $I_x=\{a\}$. At stage 3, $b\parallel x$, so (3) forces $t_x(\{a\})=t_b$ before $I_y$ is revealed. Because both observables evaluate the same single-point family $\phi(t)=\Psi(t,x_*)$ at the same time $t_b$, this forces the stage-3 operator identity
$$
\phi_x=\Psi(t_b,x_*)=\phi_b.
$$
Conditional on $I_x=\{a\}$, the fourth-birth continuation $I_y=\{a,x\}$ has strictly positive native probability ($19/220$ under $P_0$ and $7/220$ under $P_1$; full weights $19/1320$ and $14/1320$). On $I_y=\{a,x\}$, we have $x\prec y$ and $b\parallel y$, so (1) requires simultaneously
$$
[\phi_y,\phi_x]=+i\beta I\ne0\qquad\text{and}\qquad[\phi_y,\phi_b]=0,
$$
which is impossible for any operator $\phi_y$ when $\phi_x=\phi_b$ (and at tick level $t_y>t_x=t_b$ contradicts $t_y=t_b$). Hence no online single-point rule exists on $I_x=\{a\}$, eliminating both $I_x=\{a\},\ I_y=\{a\}$ and $I_x=\{a\},\ I_y=\{a,b,x\}$ as well.

Finally, on any of the three strict weak-order non-chain rows—specifically the sole remaining row $I_x=\{a,b\},\ I_y=\{a,b\}$ online (with $x\parallel y$) as well as both weak-order rows $I_x=\{a\},\ I_y=\{a\}$ and $I_x=\{a\},\ I_y=\{a,b,x\}$ offline (each having $b\parallel x$)—transitivity of $\parallel$ implies $u\prec r\iff u\prec s$ and $r\prec u\iff s\prec u$ for every vertex $u$ whenever $r\parallel s$, so $g:=e_r-e_s\in\ker D(H)$ (specifically $g=e_x-e_y$ on $I_x=\{a,b\},\ I_y=\{a,b\}$, and $g=e_b-e_x$ on both $I_x=\{a\},\ I_y=\{a\}$ and $I_x=\{a\},\ I_y=\{a,b,x\}$). Assigning $t_r=t_s$ to $r\parallel s$ yields the identical operator $\phi_r=\Psi(t_r,x_*)=\phi_s$, so $\Phi(g)=\phi_r-\phi_s=0$, forcing zero fluctuation variance $g^T V(H)g=0$, singular covariance matrices $\det V(H)=\det W(H)=0$, and failure of distinct-birth operator nondegeneracy. $\square$

Theorem 1 proves that the `"unavailable"` tag on the 14 non-chain rows in the previous stationary constructions is an exact consequence of restricting spatial sampling to one point $x_*$.

---

## 2. Minimal-denominator adapted $1+1$D causal embedding

Supply flat $1+1$D dimensionless coordinates $z_r=(\tau_r,\xi_r)\in\mathbb R^2$, related to physical coordinates $(t_r,x_r)=(\tau_r\tau,\xi_r c\tau)$ whenever a tick duration $\tau>0$ and propagation speed $c>0$ are declared. A strict $1+1$D Minkowski causal embedding of a poset $(\{a,b,x,y\},\prec)$ is a map $r\mapsto z_r$ such that for all distinct $r,s\in\{a,b,x,y\}$,
$$
s\prec r\iff \tau_r-\tau_s>|\xi_r-\xi_s|,\qquad
r\parallel s\iff |\tau_r-\tau_s|<|\xi_r-\xi_s|.
\tag{4}
$$
Null separations $|\tau_r-\tau_s|=|\xi_r-\xi_s|$ are excluded. Fix the prepared two-event prefix at
$$
z_a=(0,0),\qquad z_b=(1,0).
\tag{5}
$$

**Proposition 1 (Minimal lattice denominator $q\ge3$).** *Let $q\in\mathbb Z_{\ge1}$. Any strict causal embedding (even offline) of the single structural row $I_x=\{a\},\ I_y=\{a,x\}$ into $\frac1q\mathbb Z^2$ satisfying (4)–(5) requires $q\ge3$.*

*Proof.* Write $z_r=\frac1q(T_r,X_r)$ with $(T_r,X_r)\in\mathbb Z^2$, so $(T_a,X_a)=(0,0)$ and $(T_b,X_b)=(q,0)$. On row $I_x=\{a\},\ I_y=\{a,x\}$ we have $a\prec x$, $x\prec y$, and $b\parallel y$. By (4) and integrality of $T_r,X_r$:
1. $a\prec x\implies T_x>|X_x|\implies T_x-|X_x|\ge1$.
2. $x\prec y\implies T_y-T_x>|X_y-X_x|\implies T_y-T_x-|X_y-X_x|\ge1$.

Adding these two inequalities and applying the triangle inequality $|X_x|+|X_y-X_x|\ge|X_y|$ gives
$$
T_y-|X_y|\ge(T_x-|X_x|)+(T_y-T_x-|X_y-X_x|)\ge2,\qquad\text{so}\qquad |X_y|\le T_y-2.
$$
On the other hand, $b\parallel y$ gives $|T_y-q|<|X_y|$, which by integrality implies
$$
|X_y|\ge|T_y-q|+1\ge T_y-q+1.
$$
Combining the two bounds yields $T_y-q+1\le|X_y|\le T_y-2$, hence $q\ge3$. $\square$

We now verify that $q=3$ suffices simultaneously for an **adapted (online)** causal embedding of all 15 structural rows in $\frac13\mathbb Z^2$, where $z_x=z_x(I_x)$ depends solely on $I_x$ and $z_y=z_y(I_x,I_y)$ depends solely on $(I_x,I_y)$. For any $z=(\tau_*,\xi_*)\in\frac13\mathbb Z^2$, define the two integer lightcone coordinates
$$
\nu_+(z):=3(\tau_*-\xi_*)\in\mathbb Z,\qquad
\nu_-(z):=3(\tau_*+\xi_*)\in\mathbb Z,
\tag{6}
$$
and for any pair $(r,s)$ write $\nu_\pm(z_r-z_s)=\nu_\pm(z_r)-\nu_\pm(z_s)=3\bigl((\tau_r-\tau_s)\mp(\xi_r-\xi_s)\bigr)\in\mathbb Z$. Because $\tau_r-\tau_s>|\xi_r-\xi_s|$ holds if and only if both $(\tau_r-\tau_s)\mp(\xi_r-\xi_s)>0$, while $(\tau_r-\tau_s)^2-(\xi_r-\xi_s)^2=\frac19\nu_+(z_r-z_s)\nu_-(z_r-z_s)$, integrality gives the exact equivalences
$$
\begin{aligned}
s\prec r&\iff \nu_+(z_r-z_s)\ge1\ \text{and}\ \nu_-(z_r-z_s)\ge1,\\
r\prec s&\iff \nu_+(z_r-z_s)\le-1\ \text{and}\ \nu_-(z_r-z_s)\le-1,\\
r\parallel s&\iff \nu_+(z_r-z_s)\,\nu_-(z_r-z_s)<0.
\end{aligned}
\tag{7}
$$

With $z_a=(0,0)$ and $z_b=(1,0)$, we have $(\nu_+(z_a),\nu_-(z_a))=(0,0)$, $(\nu_+(z_b),\nu_-(z_b))=(3,3)$, and $\nu_\pm(z_b-z_a)=(+3,+3)$ ($a\prec b$) across all 15 rows. At stage 3, define $z_x(I_x)$ on the three eligible ideals $I_x\subseteq\{a,b\}$ as follows:

| $I_x$ | $z_x(I_x)$ | $(\nu_+(z_x),\nu_-(z_x))$ | $\nu_\pm(z_x-z_a)$ | $\nu_\pm(z_x-z_b)$ | Realized stage-3 order |
|---|---|---|---|---|---|
| $\varnothing$ | $(1/3,\,4/3)$ | $(-3,\,+5)$ | $(-3,\,+5)$ | $(-6,\,+2)$ | $a\prec b,\ x\parallel a,\ x\parallel b$ |
| $\{a\}$ | $(1,\,2/3)$ | $(+1,\,+5)$ | $(+1,\,+5)$ | $(-2,\,+2)$ | $a\prec b,\ a\prec x,\ x\parallel b$ |
| $\{a,b\}$ | $(2,\,0)$ | $(+6,\,+6)$ | $(+6,\,+6)$ | $(+3,\,+3)$ | $a\prec b\prec x$ |

Every stage-3 difference $\nu_\pm(z_r-z_s)$ lies in $\{\pm1,\ldots,\pm6\}$ and satisfies (7). At stage 4, define $z_y(I_x,I_y)$ as in the complete 15-row ledger below; concatenation denotes a set ($ab=\{a,b\}$), and the final columns retain the exact structural probability numerators over $1320$ from the [finite interval and source specification](finite_interval_action_and_source_preparation.md).

| Row | $I_x$ | $I_y$ | $z_x(I_x)$ | $z_y(I_x,I_y)$ | $\nu_\pm(z_y)$ | $\nu_\pm(z_y-z_a)$ | $\nu_\pm(z_y-z_b)$ | $\nu_\pm(z_y-z_x)$ | $1320P_0$ | $1320P_1$ |
|---:|---|---|---|---|---|---|---|---|---:|---:|
| 1 | $\varnothing$ | $\varnothing$ | $(1/3,4/3)$ | $(1/3,-1)$ | $(+4,-2)$ | $(+4,-2)$ | $(+1,-5)$ | $(+7,-7)$ | 6 | 6 |
| 2 | $\varnothing$ | $x$ | $(1/3,4/3)$ | $(2/3,4/3)$ | $(-2,+6)$ | $(-2,+6)$ | $(-5,+3)$ | $(+1,+1)$ | 6 | 6 |
| 3 | $\varnothing$ | $a$ | $(1/3,4/3)$ | $(1,-1/3)$ | $(+4,+2)$ | $(+4,+2)$ | $(+1,-1)$ | $(+7,-3)$ | 5 | 10 |
| 4 | $\varnothing$ | $ab$ | $(1/3,4/3)$ | $(4/3,0)$ | $(+4,+4)$ | $(+4,+4)$ | $(+1,+1)$ | $(+7,-1)$ | 19 | 14 |
| 5 | $\varnothing$ | $ax$ | $(1/3,4/3)$ | $(4/3,1)$ | $(+1,+7)$ | $(+1,+7)$ | $(-2,+4)$ | $(+4,+2)$ | 33 | 33 |
| 6 | $\varnothing$ | $abx$ | $(1/3,4/3)$ | $(2,1/3)$ | $(+5,+7)$ | $(+5,+7)$ | $(+2,+4)$ | $(+8,+2)$ | 195 | 195 |
| 7 | $a$ | $\varnothing$ | $(1,2/3)$ | $(1/3,-1)$ | $(+4,-2)$ | $(+4,-2)$ | $(+1,-5)$ | $(+3,-7)$ | 5 | 10 |
| 8 | $a$ | $a$ | $(1,2/3)$ | $(1,-2/3)$ | $(+5,+1)$ | $(+5,+1)$ | $(+2,-2)$ | $(+4,-4)$ | 5 | 10 |
| 9 | $a$ | $ab$ | $(1,2/3)$ | $(4/3,0)$ | $(+4,+4)$ | $(+4,+4)$ | $(+1,+1)$ | $(+3,-1)$ | 19 | 14 |
| 10 | $a$ | $ax$ | $(1,2/3)$ | $(5/3,1)$ | $(+2,+8)$ | $(+2,+8)$ | $(-1,+5)$ | $(+1,+3)$ | 19 | 14 |
| 11 | $a$ | $abx$ | $(1,2/3)$ | $(2,0)$ | $(+6,+6)$ | $(+6,+6)$ | $(+3,+3)$ | $(+5,+1)$ | 172 | 392 |
| 12 | $ab$ | $\varnothing$ | $(2,0)$ | $(1,5/3)$ | $(-2,+8)$ | $(-2,+8)$ | $(-5,+5)$ | $(-8,+2)$ | 19 | 14 |
| 13 | $ab$ | $a$ | $(2,0)$ | $(4/3,1)$ | $(+1,+7)$ | $(+1,+7)$ | $(-2,+4)$ | $(-5,+1)$ | 19 | 14 |
| 14 | $ab$ | $ab$ | $(2,0)$ | $(2,1/3)$ | $(+5,+7)$ | $(+5,+7)$ | $(+2,+4)$ | $(-1,+1)$ | 19 | 14 |
| 15 | $ab$ | $abx$ | $(2,0)$ | $(3,0)$ | $(+9,+9)$ | $(+9,+9)$ | $(+6,+6)$ | $(+3,+3)$ | 779 | 574 |
| **Total** | | | | | | | | | **1320** | **1320** |

Each structural row splits into four fair suffix-mark continuations $(b_3,b_4)\in\{0,1\}^2$, each carrying weight $P_i(I_x,I_y)/4$ over denominator $5280=4\times1320$ (for example $779/5280$ and $574/5280$ on each marked 4-chain history, and $6/5280=1/880$ on each marked instance of Rows 1 and 2). Summing by stage-3 blocks checks complete normalization: $(6+6+5+19+33+195)+(5+5+19+19+172)+(19+19+19+779)=264+220+836=1320$ for $P_0$, and $(6+6+10+14+33+195)+(10+10+14+14+392)+(14+14+14+574)=264+440+616=1320$ for $P_1$.

Inspection of the stage-3 table together with the three $\nu_\pm(z_y-z_s)$ columns across all 15 rows verifies directly for all $15\times6=90$ unordered pairs (and by antisymmetry $\nu_\pm(z_s-z_r)=-\nu_\pm(z_r-z_s)$ for all 180 ordered pairs $r\ne s$):
1. Every lightcone integer is strictly nonzero and satisfies
   $$
   \nu_\pm(z_r-z_s)\in\{\pm1,\pm2,\pm3,\pm4,\pm5,\pm6,\pm7,\pm8,\pm9\},\qquad 1\le|\nu_\pm(z_r-z_s)|\le9.
   \tag{8}
   $$
2. For each row and each $u\in\{a,b,x\}$, $\nu_+(z_y-z_u)\ge1$ and $\nu_-(z_y-z_u)\ge1$ hold if and only if $u\in I_y$, while $\nu_+(z_y-z_u)\nu_-(z_y-z_u)<0$ holds if and only if $u\notin I_y$. Thus (7) and (4) hold identically on all 15 structural rows.
3. On the 4-chain row $I_x=\{a,b\},\ I_y=\{a,b,x\}$ (Row 15), the embedding reduces to $((0,0),(1,0),(2,0),(3,0))$, recovering the exact single-probe integer ticks $n=0,1,2,3$ at $\xi=0$.

---

## 3. Exact discrete odd-harmonic square-wave identity

Let $N=2M$ be an even positive integer ($M\in\mathbb Z_{\ge1}$). Define the $M$ discrete odd-harmonic angles and cotangent weights
$$
\varphi_m:=\frac{(2m+1)\pi}{N}=\frac{(2m+1)\pi}{2M},\qquad
c_m:=\frac{1}{M}\cot\!\left(\frac{\varphi_m}{2}\right)=\frac{1}{M}\cot\!\left(\frac{(2m+1)\pi}{4M}\right),\qquad m=0,\ldots,M-1,
\tag{9}
$$
and the finite trigonometric sum
$$
S_N(\nu):=\sum_{m=0}^{M-1}c_m\sin(\nu\varphi_m),\qquad \nu\in\mathbb Z.
\tag{10}
$$
Because $1\le 2m+1\le 2M-1$, every half-angle satisfies $0<\varphi_m/2<\pi/2$, where both $\sin$ and $\cos$ are strictly positive; hence $c_m>0$ for all $m=0,\ldots,M-1$.

**Proposition 2 (Exact discrete odd-harmonic square wave on $\mathbb Z/2N\mathbb Z$).** *For every even $N=2M\ge2$, the sum (10) satisfies $S_N(\nu+2N)=S_N(\nu)$ and*
$$
S_N(\nu)=
\begin{cases}
+1,& \nu\in\{1,2,\ldots,N-1\},\\
0,& \nu\in\{0,N\},\\
-1,& \nu\in\{-(N-1),\ldots,-2,-1\}.
\end{cases}
\tag{11}
$$
*In particular, for $N=12,\ M=6$ ($\varphi_m=\frac{(2m+1)\pi}{12}$, $c_m=\frac16\cot\bigl(\frac{(2m+1)\pi}{24}\bigr)>0$, $m=0,\ldots,5$), $S(\nu):=S_{12}(\nu)$ equals $+1$ for all $\nu\in\{1,\ldots,11\}$, $0$ for $\nu\in\{0,12\}$, and $-1$ for all $\nu\in\{-11,\ldots,-1\}$.*

We give two independent first-principles proofs: an elementary telescoping proof and the finite Fourier orthogonality proof on $\mathbb Z/2N\mathbb Z$ ($\mathbb Z/24\mathbb Z$ for $N=12$).

*Proof 1 (Elementary telescoping sums).* Periodicity $S_N(\nu+2N)=S_N(\nu)$ and oddness $S_N(-\nu)=-S_N(\nu)$ follow immediately from $(\nu+2N)\varphi_m=\nu\varphi_m+2(2m+1)\pi$, while $S_N(0)=0$ and $S_N(N)=\sum_{m=0}^{M-1}c_m\sin((2m+1)\pi)=0$. Let $\nu\in\{1,\ldots,N-1\}$. For any $\varphi\in(0,2\pi)$, summing the product-to-sum identity $2\sin(\varphi/2)\cos(k\varphi)=\sin\bigl((k+\tfrac12)\varphi\bigr)-\sin\bigl((k-\tfrac12)\varphi\bigr)$ over $k=1,\ldots,\nu-1$ telescopes to
$$
\begin{aligned}
\sin\!\left(\frac{\varphi}{2}\right)\left[1+2\sum_{k=1}^{\nu-1}\cos(k\varphi)+\cos(\nu\varphi)\right]
&=\sin\!\left(\Bigl(\nu-\frac12\Bigr)\varphi\right)+\sin\!\left(\frac{\varphi}{2}\right)\cos(\nu\varphi)\\
&=\sin(\nu\varphi)\cos\!\left(\frac{\varphi}{2}\right)-\cos(\nu\varphi)\sin\!\left(\frac{\varphi}{2}\right)+\sin\!\left(\frac{\varphi}{2}\right)\cos(\nu\varphi)\\
&=\sin(\nu\varphi)\cos\!\left(\frac{\varphi}{2}\right).
\end{aligned}
$$
Dividing by $\sin(\varphi/2)\ne0$ yields the exact pointwise identity
$$
\cot\!\left(\frac{\varphi}{2}\right)\sin(\nu\varphi)=1+2\sum_{k=1}^{\nu-1}\cos(k\varphi)+\cos(\nu\varphi).
$$
Next, for every integer $k\in\{1,\ldots,N-1\}$, we have $0<\frac{k\pi}{2M}<\pi$, so $\sin\bigl(\frac{k\pi}{2M}\bigr)>0$. Multiplying $\sum_{m=0}^{M-1}\cos(k\varphi_m)$ by $2\sin\bigl(\frac{k\pi}{2M}\bigr)$ telescopes in $m$:
$$
2\sin\!\left(\frac{k\pi}{2M}\right)\sum_{m=0}^{M-1}\cos\!\left(\frac{k(2m+1)\pi}{2M}\right)
=\sum_{m=0}^{M-1}\left[\sin\!\left(\frac{k(2m+2)\pi}{2M}\right)-\sin\!\left(\frac{k(2m)\pi}{2M}\right)\right]
=\sin(k\pi)-\sin(0)=0.
$$
Dividing by $2\sin\bigl(\frac{k\pi}{2M}\bigr)>0$ gives $\sum_{m=0}^{M-1}\cos(k\varphi_m)=0$ for every $k\in\{1,\ldots,N-1\}$. Because $1\le\nu\le N-1$, every index $k\in\{1,\ldots,\nu\}$ lies in $\{1,\ldots,N-1\}$, so summing the pointwise cotangent identity over $m=0,\ldots,M-1$ gives
$$
S_N(\nu)=\frac{1}{M}\sum_{m=0}^{M-1}1+\frac{2}{M}\sum_{k=1}^{\nu-1}\sum_{m=0}^{M-1}\cos(k\varphi_m)+\frac{1}{M}\sum_{m=0}^{M-1}\cos(\nu\varphi_m)=\frac{M}{M}=1,
$$
and oddness gives $S_N(-\nu)=-1$ for $\nu\in\{1,\ldots,N-1\}$. $\square$

*Proof 2 (Finite Fourier orthogonality on $\mathbb Z/2N\mathbb Z$, specifically $\mathbb Z/24\mathbb Z$ at $N=12$).* Let $f:\mathbb Z/2N\mathbb Z\to\{-1,0,+1\}$ denote the right-hand side of (11), extended $2N$-periodically. The discrete Fourier characters $\chi_\ell(\nu)=e^{i\pi\ell\nu/N}$ ($\ell\in\{0,\ldots,2N-1\}$) satisfy exact orthogonality on $\mathbb Z/2N\mathbb Z$:
$$
\frac{1}{2N}\sum_{\ell=0}^{2N-1}e^{i\pi\ell(\nu-\nu')/N}=\mathbf 1_{\{\nu\equiv\nu'\pmod{2N}\}},
\qquad
f(\nu)=\sum_{\ell=0}^{2N-1}\widehat f(\ell)\,e^{i\pi\ell\nu/N},
$$
where $\widehat f(\ell):=\frac{1}{2N}\sum_{\nu=0}^{2N-1}f(\nu)e^{-i\pi\ell\nu/N}$. Observe that $f$ satisfies both oddness $f(-\nu)=-f(\nu)$ and exact half-period anti-periodicity $f(\nu+N)=-f(\nu)$ for every $\nu\in\mathbb Z/2N\mathbb Z$ (at $\nu=0,N$, $0=-0$; for $1\le\nu\le N-1$, $\nu+N\equiv-(N-\nu)\pmod{2N}$ gives $f(\nu+N)=-1=-f(\nu)$). Shifting $\nu\mapsto\nu+N$ in $\widehat f(\ell)$ yields
$$
\widehat f(\ell)=\frac{1}{2N}\sum_{\nu\in\mathbb Z/2N\mathbb Z}f(\nu+N)e^{-i\pi\ell(\nu+N)/N}=-(-1)^\ell\widehat f(\ell).
$$
Hence $\widehat f(\ell)=0$ for **every even** $\ell\in\{0,2,\ldots,2N-2\}$. For **odd** $\ell$, put $q_\ell=e^{-i\pi\ell/N}\ne1$; then $q_\ell^N=e^{-i\pi\ell}=-1$, and summing the finite geometric series gives
$$
\sum_{\nu=0}^{N-1}q_\ell^\nu=\frac{1-q_\ell^N}{1-q_\ell}=\frac{2}{1-e^{-i\pi\ell/N}}=\frac{e^{i\pi\ell/(2N)}}{i\sin\bigl(\frac{\pi\ell}{2N}\bigr)}=1-i\cot\!\left(\frac{\pi\ell}{2N}\right).
$$
Using $f(0)=f(N)=0$ and $f(-\nu)=-f(\nu)$ for $1\le\nu\le N-1$,
$$
\widehat f(\ell)=\frac{1}{2N}\sum_{\nu=1}^{N-1}\bigl(q_\ell^\nu-q_\ell^{-\nu}\bigr)=\frac{1}{2N}\left[\Bigl(1-i\cot\frac{\pi\ell}{2N}\Bigr)-\Bigl(1+i\cot\frac{\pi\ell}{2N}\Bigr)\right]=-\frac{i}{N}\cot\!\left(\frac{\pi\ell}{2N}\right).
$$
Since $N=2M$ is even, the $N=2M$ odd residues in $\{0,\ldots,2N-1\}$ pair into $\ell=2m+1$ and $2N-(2m+1)$ for $m=0,\ldots,M-1$, with $\widehat f(2N-\ell)=-\widehat f(\ell)=+\frac{i}{N}\cot\bigl(\frac{\varphi_m}{2}\bigr)$ and $e^{i\pi(2N-\ell)\nu/N}=e^{-i\nu\varphi_m}$. Exact Fourier inversion on $\mathbb Z/2N\mathbb Z$ (specifically $\mathbb Z/24\mathbb Z$ when $N=12,\ M=6$) therefore gives
$$
f(\nu)=\sum_{m=0}^{M-1}\left(-\frac{i}{N}\cot\frac{\varphi_m}{2}\right)\bigl(e^{i\nu\varphi_m}-e^{-i\nu\varphi_m}\bigr)=\sum_{m=0}^{M-1}\frac{2}{N}\cot\!\left(\frac{\varphi_m}{2}\right)\sin(\nu\varphi_m)=S_N(\nu)
$$
for every $\nu\in\mathbb Z$, since $2/N=1/M$. $\square$

**Recovery of the accepted two-mode four-chain weights at $N=4,\ M=2$.** Setting $N=4,\ M=2$ gives $\varphi_0=\pi/4,\ \varphi_1=3\pi/4$ and
$$
c_0=\frac12\cot\!\left(\frac{\pi}{8}\right)=\frac{\sqrt2+1}{2},\qquad
c_1=\frac12\cot\!\left(\frac{3\pi}{8}\right)=\frac{\sqrt2-1}{2},
$$
using $\cot(\alpha/2)=(1+\cos\alpha)/\sin\alpha$. Under the reflection $\tilde\varphi_m=2\pi-\varphi_m$, the two frequencies become $\tilde\varphi_1=5\pi/4$ and $\tilde\varphi_0=7\pi/4$ with squared amplitudes $\beta c_1=\frac\beta2(\sqrt2-1)$ and $\beta c_0=\frac\beta2(\sqrt2+1)$, reproducing Eq. (3) of [stationary dynamics for four-chain fields](stationary_dynamics_for_four_chain_fields.md) identically on the integer lags $\nu\in\{1,2,3\}$. Because our all-branch embedding in $\frac13\mathbb Z^2$ reaches $|\nu_\pm|\le9$, we require $N-1\ge9$ with $N=2M$ even; $N=10$ would already cover $\{1,\ldots,9\}$, while $N=12,\ M=6$ aligns $\theta_m=3\tilde\varphi_m=\frac{(23-2m)\pi}{4}$ cleanly with quarter-turn chain phases on circumference $L=4c\tau$.

---

## 4. Reflected 12-mode anti-periodic $1+1$D scalar wavefield and positive generator

Fix $N=12,\ M=6$, $\varphi_m=\frac{(2m+1)\pi}{12}$, and $c_m=\frac16\cot\bigl(\frac{(2m+1)\pi}{24}\bigr)>0$ ($m=0,\ldots,5$). Define the reflected angles and strictly positive dimensionless per-tick frequencies
$$
\tilde\varphi_m:=2\pi-\varphi_m=\frac{(23-2m)\pi}{12}\in(\pi,2\pi),\qquad
\theta_m:=3\tilde\varphi_m=\frac{(23-2m)\pi}{4}>0,\qquad m=0,\ldots,5.
\tag{12}
$$
When physical standards $\tau>0$ (duration per dimensionless tick) and $c>0$ (propagation speed) are supplied, define the spatial circle $S_L^1=\mathbb R/L\mathbb Z$ of circumference
$$
\boxed{L:=4c\tau,}
\tag{13}
$$
together with angular frequencies and right/left-moving wavevectors ($\sigma\in\{+1,-1\}$)
$$
\omega_m:=\frac{\theta_m}{\tau}=\frac{(23-2m)\pi}{4\tau}>0,\qquad
k_{m,\sigma}:=\sigma\frac{(23-2m)\pi}{L}=\sigma\frac{\omega_m}{c}.
\tag{14}
$$

Take 12 canonical pairs $(Q_{m,\sigma},P_{m,\sigma})$ ($m\in\{0,\ldots,5\},\ \sigma\in\{+,-\}$) in their standard Schrödinger representation on $\mathcal H=L^2(\mathbb R^{12})$, $(Q_{m,\sigma}\psi)(q)=q_{m,\sigma}\psi(q)$ and $(P_{m,\sigma}\psi)(q)=-i\partial_{q_{m,\sigma}}\psi(q)$, with common invariant Schwartz domain $\mathcal S(\mathbb R^{12})$. On $\mathcal S(\mathbb R^{12})$,
$$
[Q_{m,\sigma},P_{m',\sigma'}]=i\delta_{mm'}\delta_{\sigma\sigma'}I,\qquad
[Q_{m,\sigma},Q_{m',\sigma'}]=[P_{m,\sigma},P_{m',\sigma'}]=0.
$$
Define the dimensionless positive quadratic generator
$$
K:=\frac12\sum_{m=0}^5\sum_{\sigma=\pm}\theta_m\bigl(Q_{m,\sigma}^2+P_{m,\sigma}^2\bigr).
\tag{15}
$$
Because $\theta_m>0$ for each $m$, $K$ is symmetric, strictly positive, and essentially self-adjoint on $\mathcal S(\mathbb R^{12})$ (whose Hermite tensor-product basis diagonalizes $K$ with pure point eigenvalues $\sum_{m,\sigma}\theta_m(n_{m,\sigma}+\tfrac12)$, $n_{m,\sigma}\in\mathbb Z_{\ge0}$). Its unique normalized ground state $\Omega_0\in\mathcal S(\mathbb R^{12})$ is the centered product Gaussian
$$
\Omega_0(q):=\pi^{-3}\exp\!\left(-\frac12\sum_{m=0}^5\sum_{\sigma=\pm}q_{m,\sigma}^2\right),\qquad
K\Omega_0=27\pi\,\Omega_0,
$$
since $\sum_{m=0}^5\theta_m=\frac{\pi}{4}(23+21+19+17+15+13)=27\pi>0$, and the lowest excitation gap above $\Omega_0$ is $\theta_5=\frac{13\pi}{4}>0$. Write $\omega_{\rm vac}(A):=\langle\Omega_0,A\Omega_0\rangle$; then $\omega_{\rm vac}$ is stationary ($e^{-isK}\Omega_0=e^{-i27\pi s}\Omega_0$) with single-pair moments $\omega_{\rm vac}(Q_{m,\sigma}^2)=\omega_{\rm vac}(P_{m,\sigma}^2)=\frac12$, $\omega_{\rm vac}(Q_{m,\sigma}P_{m,\sigma})=+\frac{i}{2}$, $\omega_{\rm vac}(P_{m,\sigma}Q_{m,\sigma})=-\frac{i}{2}$, and vanishing cross-pair contractions. The unitary group $U(s)=e^{-isK}$ ($s\in\mathbb R$) leaves $\mathcal S(\mathbb R^{12})$ invariant.

In dimensionless spacetime coordinates $z=(s,\xi)\in\mathbb R^2$ (corresponding to $(t,x)=(s\tau,\xi c\tau)$), define the dimensionless 12-mode traveling-wave scalar field on $\mathcal S(\mathbb R^{12})$ by
$$
\Psi(z)=\Psi(s,\xi):=\sum_{m=0}^5\sum_{\sigma=\pm}\sqrt{\frac{\beta c_m}{2}}\,
\Bigl[Q_{m,\sigma}\cos\bigl(\theta_m(s-\sigma\xi)\bigr)+P_{m,\sigma}\sin\bigl(\theta_m(s-\sigma\xi)\bigr)\Bigr],
\tag{16}
$$
and write $\Psi(t,x):=\Psi(t/\tau,x/(c\tau))$ when physical coordinates $(t,x)$ are used, so $\theta_m(t/\tau-\sigma x/(c\tau))=\omega_m t-k_{m,\sigma}x$.

Let us verify the exact wave, boundary, Heisenberg, and Hamiltonian identities on $\mathcal S(\mathbb R^{12})$:

1. **Exact $1+1$D wave equation and spatial anti-periodicity.** For every $(m,\sigma)$, $\omega_m^2-c^2k_{m,\sigma}^2=0$, so differentiating (16) twice on $\mathcal S(\mathbb R^{12})$ yields the exact operator identity
   $$
   \left(\frac{1}{c^2}\frac{\partial^2}{\partial t^2}-\frac{\partial^2}{\partial x^2}\right)\Psi(t,x)=0
   \qquad\Longleftrightarrow\qquad
   \left(\frac{\partial^2}{\partial s^2}-\frac{\partial^2}{\partial\xi^2}\right)\Psi(s,\xi)=0.
   \tag{17}
   $$
   Under $x\mapsto x+L$ (equivalently $\xi\mapsto\xi+4$), $k_{m,\sigma}(x+L)=k_{m,\sigma}x+\sigma(23-2m)\pi$. Because $23-2m\in\{13,15,17,19,21,23\}$ is an odd integer for every $m\in\{0,\ldots,5\}$, $\cos(\alpha-\sigma(23-2m)\pi)=-\cos\alpha$ and $\sin(\alpha-\sigma(23-2m)\pi)=-\sin\alpha$, establishing exact spatial anti-periodicity with no constant zero mode:
   $$
   \Psi(t,x+L)=-\Psi(t,x)\qquad\bigl(\Psi(s,\xi+4)=-\Psi(s,\xi)\bigr).
   \tag{18}
   $$

2. **Exact Heisenberg evolution.** On $\mathcal S(\mathbb R^{12})$, $[iK,Q_{m,\sigma}]=\theta_m P_{m,\sigma}$ and $[iK,P_{m,\sigma}]=-\theta_m Q_{m,\sigma}$ integrate to
   $$
   e^{isK}Q_{m,\sigma}e^{-isK}=Q_{m,\sigma}\cos(s\theta_m)+P_{m,\sigma}\sin(s\theta_m),\qquad
   e^{isK}P_{m,\sigma}e^{-isK}=P_{m,\sigma}\cos(s\theta_m)-Q_{m,\sigma}\sin(s\theta_m).
   $$
   Applying $e^{i(t/\tau)K}(\cdot)e^{-i(t/\tau)K}$ to $\Psi(0,x)=\sum_{m,\sigma}\sqrt{\frac{\beta c_m}{2}}\bigl[Q_{m,\sigma}\cos(k_{m,\sigma}x)-P_{m,\sigma}\sin(k_{m,\sigma}x)\bigr]$ and expanding $\cos(\omega_m t-k_{m,\sigma}x)=\cos(\omega_m t)\cos(k_{m,\sigma}x)+\sin(\omega_m t)\sin(k_{m,\sigma}x)$ and $\sin(\omega_m t-k_{m,\sigma}x)=\sin(\omega_m t)\cos(k_{m,\sigma}x)-\cos(\omega_m t)\sin(k_{m,\sigma}x)$ gives the exact operator identity
   $$
   \Psi(t,x)=e^{i(t/\tau)K}\Psi(0,x)e^{-i(t/\tau)K}.
   \tag{19}
   $$

3. **Optional action-derived $1+1$D scalar Hamiltonian and field-scale ledger.** Following the normalization discipline of the [local scalar source lift](local_scalar_source_for_four_chain_field.md), if one additionally supplies an action reference $A_*>0$ and $1+1$D scalar kinetic normalization $\kappa_1>0$ alongside $c,\tau>0$, consider the local $1+1$D scalar action on anti-periodic fields $\Phi_{\rm sc}(t,x+L)=-\Phi_{\rm sc}(t,x)$,
   $$
   \mathcal S_{1+1}[\Phi_{\rm sc}]=\frac{\kappa_1}{2}\int dt\int_0^L\left[\frac{\dot\Phi_{\rm sc}^2}{c^2}-(\partial_x\Phi_{\rm sc})^2\right]dx.
   $$
   With $\kappa_m:=|k_{m,\sigma}|=\frac{(23-2m)\pi}{L}=\frac{\omega_m}{c}$, the 12 real anti-periodic standing profiles $u_{m,1}(x)=\cos(\kappa_m x)$ and $u_{m,2}(x)=\sin(\kappa_m x)$ satisfy exact orthogonality on $[0,L]$: because $(\kappa_m\pm\kappa_{m'})L=[(23-2m)\pm(23-2m')]\pi$ is an even integer multiple of $\pi$ (zero only for $\kappa_m-\kappa_m$),
   $$
   \int_0^L u_{m,a}(x)u_{m',b}(x)\,dx=\frac{L}{2}\delta_{mm'}\delta_{ab},\qquad
   \int_0^L \partial_x u_{m,a}(x)\,\partial_x u_{m',b}(x)\,dx=\frac{L}{2}\kappa_m^2\delta_{mm'}\delta_{ab}.
   $$
   Define on the **same** 12 canonical pairs $(Q_{m,\sigma},P_{m,\sigma})$ the action-normalized anti-periodic wavefield
   $$
   \Phi_{\rm sc}(t,x):=\sum_{m=0}^5\sum_{\sigma=\pm}B_m\bigl[Q_{m,\sigma}\cos(\omega_m t-k_{m,\sigma}x)+P_{m,\sigma}\sin(\omega_m t-k_{m,\sigma}x)\bigr],
   \qquad B_m:=\sqrt{\frac{A_*c^2}{\kappa_1 L\omega_m}}>0.
   \tag{20}
   $$
   Then $\Phi_{\rm sc}(t,x)$ obeys $(c^{-2}\partial_t^2-\partial_x^2)\Phi_{\rm sc}=0$, $\Phi_{\rm sc}(t,x+L)=-\Phi_{\rm sc}(t,x)$, and $\Phi_{\rm sc}(t,x)=e^{i(t/\tau)K}\Phi_{\rm sc}(0,x)e^{-i(t/\tau)K}$. Writing $R_{m,\sigma}(t,x):=-Q_{m,\sigma}\sin(\omega_m t-k_{m,\sigma}x)+P_{m,\sigma}\cos(\omega_m t-k_{m,\sigma}x)$, we have $c^{-1}\dot\Phi_{\rm sc}=\sum_{m,\sigma}B_m\kappa_m R_{m,\sigma}$ and $\partial_x\Phi_{\rm sc}=-\sum_{m,\sigma}\sigma B_m\kappa_m R_{m,\sigma}$, so the $\sigma=\pm1$ cross terms cancel pointwise in $(c^{-1}\dot\Phi_{\rm sc})^2+(\partial_x\Phi_{\rm sc})^2=2\sum_{\sigma=\pm}\bigl(\sum_{m=0}^5 B_m\kappa_m R_{m,\sigma}\bigr)^2$. Integrating over $[0,L]$ removes all $m\ne m'$ and $\sin\cdot\cos$ terms by periodic orthogonality of $2\kappa_m L=2(23-2m)\pi$ and $(\kappa_m\pm\kappa_{m'})L$, yielding on $\mathcal S(\mathbb R^{12})$
   $$
   H_{1+1}:=\frac{\kappa_1}{2}\int_0^L\left[\frac{\dot\Phi_{\rm sc}^2}{c^2}+(\partial_x\Phi_{\rm sc})^2\right]dx
   =\frac{\kappa_1 L}{2c^2}\sum_{m=0}^5\sum_{\sigma=\pm}B_m^2\omega_m^2\bigl(Q_{m,\sigma}^2+P_{m,\sigma}^2\bigr)
   =\boxed{\frac{A_*}{\tau}K.}
   \tag{21}
   $$
   Equivalently, in the standing-mode coordinates $q_{m,1}=B_m(X_{m,+}+X_{m,-})$ and $q_{m,2}=B_m(-Y_{m,+}+Y_{m,-})$ with mode inertia $\mu_1=\kappa_1 L/(2c^2)$ and conjugate momenta $p_{m,a}=\mu_1\dot q_{m,a}$, the reduced action gives $[q_{m,a},p_{m',b}]=iA_*\delta_{mm'}\delta_{ab}I$ and the same $H_{1+1}=(A_*/\tau)K$. Anti-periodicity of $\Phi_{\rm sc}$ makes every quadratic density $L$-periodic: with energy density $\mathcal H_{1+1}(t,x):=\frac{\kappa_1}{2}\bigl[c^{-2}\dot\Phi_{\rm sc}^2+(\partial_x\Phi_{\rm sc})^2\bigr]$, the energy flux $\mathcal P_{1+1}:=-\frac{\kappa_1}{2}\{\dot\Phi_{\rm sc},\partial_x\Phi_{\rm sc}\}$ satisfies $\mathcal P_{1+1}(t,L)=\mathcal P_{1+1}(t,0)$, so local conservation $\partial_t\mathcal H_{1+1}+\partial_x\mathcal P_{1+1}=0$ integrates to $\frac{d}{dt}H_{1+1}=0$ with exact cancellation of boundary terms.

   Note an explicit structural distinction from the single-point $3+1$D construction in the [local scalar source lift](local_scalar_source_for_four_chain_field.md). At one fixed point $x_*=0$ in $3+1$D, standing-wave spatial phase offsets $\delta_j$ absorbed the ratio between the action-normalized amplitudes $B_j\propto\omega_j^{-1/2}$ and the commutator amplitudes $a_j\propto\sqrt{c_j}$. In pure $1+1$D across spatially separated points $x_r$, traveling-wave ground-state weights are translation-invariant, and $c_m\theta_m$ is not independent of $m$ (for instance $c_1\theta_1=\frac{7\pi}{8}(\sqrt2+1)\ne\frac{5\pi}{8}(\sqrt2-1)=c_4\theta_4$). Consequently $\Phi_{\rm sc}$ and $\Psi$ are not proportional by a single constant; rather, introducing the calibrated field unit $F_*:=B_0/\sqrt{\beta c_0/2}>0$ and dimensionless positive mode ratios $\eta_m:=\sqrt{(c_m\theta_m)/(c_0\theta_0)}>0$, the calibrated sampled field $\Psi_{\rm cal}(t,x):=F_*\Psi(t/\tau,x/(c\tau))$ is related to $\Phi_{\rm sc}(t,x)$ by the exact translation-invariant anti-periodic convolution on $S_L^1$,
   $$
   \Psi_{\rm cal}(t,x)=\int_0^L\Gamma_{\rm read}(x-y)\,\Phi_{\rm sc}(t,y)\,dy,\qquad
   \Gamma_{\rm read}(y):=\frac{2}{L}\sum_{m=0}^5\eta_m\cos\!\left(\frac{(23-2m)\pi y}{L}\right),
   $$
   since $\int_0^L\cos\bigl(\kappa_m(x-y)\bigr)e^{-i\sigma\kappa_{m'}y}\,dy=\frac{L}{2}\delta_{mm'}e^{-i\sigma\kappa_m x}$ for both $\sigma=\pm1$. Both $\Phi_{\rm sc}$ and $\Psi_{\rm cal}$ evolve by $e^{itH_{1+1}/A_*}(\cdot)e^{-itH_{1+1}/A_*}=e^{i(t/\tau)K}(\cdot)e^{-i(t/\tau)K}$ under the single local Hamiltonian (21). (Equivalently, if one restricts $H_{1+1}$ to a mode-weighted quadratic form directly on $\Psi_{\rm cal}$ via $\Phi_{\rm sc}=\Gamma_{\rm read}^{-1}*\Psi_{\rm cal}$ with $\Gamma_{\rm read}^{-1}(y)=\frac{2}{L}\sum_{m=0}^5\eta_m^{-1}\cos(\kappa_m y)$, the same operator $\frac{A_*}{\tau}K$ is recovered.) In the accepted observables corpus prior to any separate compact-cavity registration, local $3+1$D stress-energy attachment is formulated only on the 4-chain in the [local $3+1$D scalar source lift](local_scalar_source_for_four_chain_field.md), where periodic $\mathbb T_L^3$ encounters the spatial-mean Poisson obstruction.

---

## 5. Exact all-branch commutator, Vandermonde positivity, four-chain radicals, and marginal preservation

For every marked history $H$ (belonging to structural row $(I_x,I_y)$), define the four stage-adapted field operators on $\mathcal S(\mathbb R^{12})$ by evaluating the single dimensionless wavefield (16) along the adapted $\frac13\mathbb Z^2$ coordinates of Section 2:
$$
\phi_a:=\Psi(0,0),\qquad \phi_b:=\Psi(1,0),\qquad
\phi_x(H):=\Psi\bigl(z_x(I_x)\bigr),\qquad \phi_y(H):=\Psi\bigl(z_y(I_x,I_y)\bigr).
\tag{22}
$$

### 5.1 Exact target-first Johnston commutator on all 15 rows

At $z_r=(\tau_r,\xi_r)$, the mode phase in (16) equals
$$
\theta_m(\tau_r-\sigma\xi_r)=3\tilde\varphi_m(\tau_r-\sigma\xi_r)=\tilde\varphi_m\,\nu_\sigma(z_r),\qquad \sigma\in\{+,-\}.
$$
Using the ground-state contraction $\omega_{\rm vac}\bigl([Q\cos\alpha_r+P\sin\alpha_r][Q\cos\alpha_s+P\sin\alpha_s]\bigr)=\frac12e^{-i(\alpha_r-\alpha_s)}$ for each independent canonical pair $(Q_{m,\sigma},P_{m,\sigma})$, the unsymmetrized two-point matrix $W_{rs}(H):=\omega_{\rm vac}\bigl(\phi_r(H)\phi_s(H)\bigr)$ is
$$
W_{rs}(H)=\frac{\beta}{4}\sum_{m=0}^5c_m\Bigl(e^{-i\tilde\varphi_m\nu_+(z_r-z_s)}+e^{-i\tilde\varphi_m\nu_-(z_r-z_s)}\Bigr).
$$
Because $\nu_\sigma:=\nu_\sigma(z_r-z_s)\in\mathbb Z$ is an **integer** on every pair of every row, the reflection $\tilde\varphi_m=2\pi-\varphi_m$ gives
$$
e^{-i\tilde\varphi_m\nu_\sigma}=e^{-i(2\pi\nu_\sigma-\nu_\sigma\varphi_m)}=e^{+i\nu_\sigma\varphi_m},\qquad
-\sin(\tilde\varphi_m\nu_\sigma)=+\sin(\nu_\sigma\varphi_m).
$$
Hence for all $r,s\in\{a,b,x,y\}$ on all 15 rows,
$$
W_{rs}(H)=\frac{\beta}{4}\sum_{m=0}^5c_m\Bigl(e^{i\nu_+(z_r-z_s)\varphi_m}+e^{i\nu_-(z_r-z_s)\varphi_m}\Bigr),
\tag{23}
$$
and because $[\phi_r(H),\phi_s(H)]=\bigl(W_{rs}(H)-W_{sr}(H)\bigr)I$ as scalar-valued canonical commutators on $\mathcal S(\mathbb R^{12})$,
$$
[\phi_r(H),\phi_s(H)]=\frac{i\beta}{2}\Bigl(S_{12}\bigl(\nu_+(z_r-z_s)\bigr)+S_{12}\bigl(\nu_-(z_r-z_s)\bigr)\Bigr)I.
\tag{24}
$$
Combining the verified lattice bounds $1\le|\nu_\pm(z_r-z_s)|\le9\le11$ in (8), the causal cone characterization (7), and Proposition 2 ($S_{12}(\nu)=\operatorname{sign}(\nu)$ for $|\nu|\le11$):
- If $s\prec r$, then $\nu_+\in\{1,\ldots,9\}$ and $\nu_-\in\{1,\ldots,9\}$, so $S_{12}(\nu_+)+S_{12}(\nu_-)=1+1=+2$, giving $[\phi_r(H),\phi_s(H)]=+i\beta I$.
- If $r\prec s$, then $\nu_+\in\{-9,\ldots,-1\}$ and $\nu_-\in\{-9,\ldots,-1\}$, so $S_{12}(\nu_+)+S_{12}(\nu_-)=-1-1=-2$, giving $[\phi_r(H),\phi_s(H)]=-i\beta I$.
- If $r\parallel s$, then $\nu_+\nu_-<0$ with $1\le|\nu_\pm|\le9$, so $\{S_{12}(\nu_+),S_{12}(\nu_-)\}=\{+1,-1\}$ and $S_{12}(\nu_+)+S_{12}(\nu_-)=0$, giving $[\phi_r(H),\phi_s(H)]=0$.
- If $r=s$, then $\nu_+=\nu_-=0$ and $[\phi_r(H),\phi_r(H)]=0$.

Thus $[\phi_r(H),\phi_s(H)]=i\beta\bigl(c_{rs}(H)-c_{sr}(H)\bigr)I$ holds **with the exact target-first $+i\beta$ sign for $s\prec r$ on all 15 structural rows (all 60 marked histories)**.

### 5.2 Vandermonde proof of strict positive definiteness and commutator zero-mode fluctuations

**Theorem 2 (Strict positive definiteness on all 15 rows).** *For every one of the 15 structural rows (all 60 marked histories $H$), both the $4\times4$ complex second-moment matrix $W(H)$ on $\mathbb C^4$ and the $4\times4$ real symmetrized covariance $V(H):=\operatorname{Re}W(H)$ on $\mathbb R^4$ (and $\mathbb C^4$) are strictly positive definite. Consequently, at every growth stage $k\in\{2,3,4\}$, every nonzero commutator zero mode $g\in\ker D_k(H)\setminus\{0\}$ defines a central linear observable $\Phi_H(g)=\sum_r g_r\phi_r(H)$ with strictly positive ground-state fluctuation variance $\omega_{\rm vac}(\Phi_H(g)^2)=g^T V_k(H)g>0$.*

*Proof.* By (23), $W(H)=W_+(H)+W_-(H)$, where for each $\sigma\in\{+,-\}$ and $u=(u_a,u_b,u_x,u_y)^T\in\mathbb C^4$,
$$
u^\dagger W_\sigma(H)u=\frac{\beta}{4}\sum_{m=0}^5c_m\left|\sum_{r\in\{a,b,x,y\}}\overline{u_r}\,e^{i\nu_\sigma(z_r)\varphi_m}\right|^2\ge0,
$$
since $\beta>0$ and $c_m>0$ for all $m=0,\ldots,5$. Define on the chirality $\sigma=+$ the unit-modulus factors
$$
\zeta_r:=e^{i\pi\nu_+(z_r)/12},\qquad \lambda_r:=e^{i\pi\nu_+(z_r)/6}=\zeta_r^2,\qquad r\in\{a,b,x,y\}.
$$
Because $\varphi_m=\frac{(2m+1)\pi}{12}$, we have the exact monomial factorization
$$
e^{i\nu_+(z_r)\varphi_m}=\zeta_r\,\lambda_r^m,\qquad m=0,1,2,3,4,5.
$$
Suppose $u\in\mathbb C^4$ satisfies $u^\dagger W(H)u=0$. Nonnegativity of $W_\pm(H)$ and strict positivity of $c_m$ force $u^\dagger W_+(H)u=0$ and hence $\sum_r(\overline{u_r}\zeta_r)\lambda_r^m=0$ for every $m=0,\ldots,5$. Retaining the first four harmonics $m=0,1,2,3$ gives the $4\times4$ Vandermonde system
$$
\begin{pmatrix}
1&1&1&1\\
\lambda_a&\lambda_b&\lambda_x&\lambda_y\\
\lambda_a^2&\lambda_b^2&\lambda_x^2&\lambda_y^2\\
\lambda_a^3&\lambda_b^3&\lambda_x^3&\lambda_y^3
\end{pmatrix}
\begin{pmatrix}
\overline{u_a}\zeta_a\\
\overline{u_b}\zeta_b\\
\overline{u_x}\zeta_x\\
\overline{u_y}\zeta_y
\end{pmatrix}=0.
$$
For any two distinct vertices $r\ne s$, $\lambda_r=\lambda_s$ holds if and only if $\frac{\pi}{6}\nu_+(z_r-z_s)\in2\pi\mathbb Z$, i.e. $\nu_+(z_r-z_s)\in12\mathbb Z$. By (8), $1\le|\nu_+(z_r-z_s)|\le9<12$ for every distinct pair on all 15 rows, so $\nu_+(z_r-z_s)\notin12\mathbb Z$ and the four unit-circle nodes $\lambda_a,\lambda_b,\lambda_x,\lambda_y$ are pairwise distinct. The Vandermonde determinant $\prod_{r<s}(\lambda_s-\lambda_r)$ is therefore nonzero, forcing $\overline{u_r}\zeta_r=0$ and (since $|\zeta_r|=1$) $u_r=0$ for all $r$. Thus $W_+(H)\succ0$ (and identically $W_-(H)\succ0$ using $\mu_r=e^{i\pi\nu_-(z_r)/6}$), proving $W(H)\succ0$ on $\mathbb C^4$.

Next, decompose $W(H)=V(H)+\frac{i}{2}D(H)$, where $V(H)=\operatorname{Re}W(H)$ is real symmetric and $D(H)=\beta(C-C^T)$ is real skew-symmetric. For every nonzero real vector $g\in\mathbb R^4\setminus\{0\}$, skew-symmetry gives $g^T D(H)g=0$, whence
$$
g^T V(H)g=g^T V(H)g+\frac{i}{2}g^T D(H)g=g^\dagger W(H)g>0.
$$
Thus $V(H)\succ0$ on $\mathbb R^4$ (and on $\mathbb C^4$ since all eigenvalues of $V(H)$ are strictly positive). Every stage-$k$ covariance $V_k(H)$ ($k=2,3$) is a principal submatrix of $V(H)$ and is therefore strictly positive definite as well; in particular $g^T V_k(H)g>0$ for all $g\in\ker D_k(H)\setminus\{0\}$. $\square$

**Resolution of Johnston's Eq. (23) zero-mode quotient obstruction inside one stationary wavefield.** Consider Row 2 ($I_x=\varnothing,\ I_y=\{x\}$, probability $6/1320=1/220$ under both $P_0$ and $P_1$, or $1/880$ per marked history), the witness row analyzed in [Gaussian field transport](gaussian_field_transport_on_native_histories.md). At stage 3 ($I_x=\varnothing$), $a\prec b$ while $x$ is isolated ($x\parallel a,\ x\parallel b$), so $e_x=(0,0,1)^T\in\ker D_3$. Imposing Johnston's stagewise kernel-as-zero quotient (Eq. (23) of [arXiv:0909.0944v2](https://arxiv.org/pdf/0909.0944v2)) at stage 3 would identify $\phi_x=0$, making it impossible for the stage-4 extension $I_y=\{x\}$ ($x\prec y$) to satisfy $[\phi_y,\phi_x]=+i\beta I\ne0$ without discarding or altering the old operator. Here $\phi_x=\Psi(1/3,4/3)$ commutes with $\phi_a=\Psi(0,0)$ and $\phi_b=\Psi(1,0)$ at stage 3 while retaining strictly positive ground-state variance $\omega_{\rm vac}(\phi_x^2)=W_0=\frac{\beta}{6}(2\sqrt6+\sqrt2)>0$; when $y$ is born at $z_y=(2/3,4/3)$ ($\nu_\pm(z_y-z_x)=(+1,+1)$), the unchanged stage-3 operator $\phi_x$ satisfies $[\phi_y,\phi_x]=+i\beta I$ and $[\phi_y,\phi_a]=[\phi_y,\phi_b]=0$ automatically.

### 5.3 Closed-form radicals on the four-chain and release of the saturated prefix

Using $\sin(\pi/12)=(\sqrt6-\sqrt2)/4$, $\cos(\pi/12)=(\sqrt6+\sqrt2)/4$, and $\cot(\alpha/2)=(1+\cos\alpha)/\sin\alpha$, the six positive cotangents $\gamma_m:=\cot\bigl(\frac{(2m+1)\pi}{24}\bigr)=6c_m$ evaluate in exact radical form to
$$
\begin{aligned}
\gamma_0&=2+\sqrt2+\sqrt3+\sqrt6,&\qquad \gamma_5&=-2+\sqrt2-\sqrt3+\sqrt6,\\
\gamma_1&=1+\sqrt2,&\qquad \gamma_4&=-1+\sqrt2,\\
\gamma_2&=2-\sqrt2-\sqrt3+\sqrt6,&\qquad \gamma_3&=-2-\sqrt2+\sqrt3+\sqrt6,
\end{aligned}
$$
with reciprocal pairings $\gamma_m\gamma_{5-m}=1$, symmetric sums $\gamma_0+\gamma_5=2\sqrt6+2\sqrt2$, $\gamma_1+\gamma_4=2\sqrt2$, $\gamma_2+\gamma_3=2\sqrt6-2\sqrt2$, and antisymmetric differences $\gamma_0-\gamma_5=4+2\sqrt3$, $\gamma_1-\gamma_4=2$, $\gamma_2-\gamma_3=4-2\sqrt3$.

On the 4-chain row $I_x=\{a,b\},\ I_y=\{a,b,x\}$ (Row 15), $z_n=(n,0)$ for $n\in\{0,1,2,3\}$ gives $\nu_\pm(z_n-z_{n'})=3(n-n')$. Hence $W^{\rm chain}_{n,n'}=W_{n-n'}$ is Toeplitz with positive-lag entries ($\ell=n-n'\in\{0,1,2,3\}$, $\psi_m:=3\varphi_m=\frac{(2m+1)\pi}{4}$)
$$
W_\ell=\frac{\beta}{2}\sum_{m=0}^5c_m e^{i\ell\psi_m}=\frac{\beta}{12}\sum_{m=0}^5\gamma_m\cos(\ell\psi_m)+\frac{i\beta}{2}S_{12}(3\ell),
$$
and $W_{-\ell}=\overline{W_\ell}$. Since $\psi_{5-m}=3\pi-\psi_m$, we have $\cos(\ell\psi_{5-m})=(-1)^\ell\cos(\ell\psi_m)$:
- At $\ell=0$: $\sum_{m=0}^5\gamma_m=(2\sqrt6+2\sqrt2)+2\sqrt2+(2\sqrt6-2\sqrt2)=4\sqrt6+2\sqrt2$, giving $W_0=\frac{\beta}{6}(2\sqrt6+\sqrt2)$.
- At $\ell=1$: $\cos\psi_0=+\frac{1}{\sqrt2}$ and $\cos\psi_1=\cos\psi_2=-\frac{1}{\sqrt2}$, so $\sum_{m=0}^2(\gamma_m-\gamma_{5-m})\cos\psi_m=\frac{(4+2\sqrt3)-2-(4-2\sqrt3)}{\sqrt2}=\frac{4\sqrt3-2}{\sqrt2}=2\sqrt6-\sqrt2$, while $S_{12}(3)=1$.
- At $\ell=2$: $\cos(2\psi_m)=\cos\bigl(\frac{(2m+1)\pi}{2}\bigr)=0$ for every $m=0,\ldots,5$, while $S_{12}(6)=1$.
- At $\ell=3$: $\cos(3\psi_m)+\cos(\psi_m)=2\cos(2\psi_m)\cos(\psi_m)=0\implies\cos(3\psi_m)=-\cos(\psi_m)$, while $S_{12}(9)=1$.

Thus the four Toeplitz lags on the 4-chain are in exact radical form:
$$
\begin{aligned}
W_0&=\frac{\beta}{6}(2\sqrt6+\sqrt2),&\qquad
W_1&=\frac{\beta}{12}(2\sqrt6-\sqrt2)+\frac{i\beta}{2},\\
W_2^{\rm lag}&=\frac{i\beta}{2},&\qquad
W_3&=-\frac{\beta}{12}(2\sqrt6-\sqrt2)+\frac{i\beta}{2}.
\end{aligned}
\tag{25}
$$
Moreover, since $e^{in\psi_4}=e^{in\psi_0}$ and $e^{in\psi_5}=e^{in\psi_1}$ for $n\in\{0,1,2,3\}$, the four orthogonal Fourier vectors $u^{(k)}_n=e^{in(2k+1)\pi/4}$ ($k=0,1,2,3$, $\|u^{(k)}\|^2=4$) diagonalize $W^{\rm chain}$ explicitly with four strictly positive eigenvalues $\frac{\beta}{3}(\gamma_0+\gamma_4)$, $\frac{\beta}{3}(\gamma_1+\gamma_5)$, $\frac{\beta}{3}\gamma_2$, and $\frac{\beta}{3}\gamma_3$ summing to $4W_0$ (upgrading the rank-2 positive-semidefinite 4-chain matrix of [stationary dynamics for four-chain fields](stationary_dynamics_for_four_chain_fields.md) to full rank 4).

Across **all** 15 rows, the fixed prefix coordinates $z_a=(0,0),\ z_b=(1,0)$ induce the common two-event second-moment matrix
$$
W_2^{\rm ext}:=\begin{pmatrix}W_0&\overline{W_1}\\ W_1&W_0\end{pmatrix},
\qquad
\det W_2^{\rm ext}=W_0^2-|W_1|^2
=\frac{\beta^2}{144}\bigl[(104+32\sqrt3)-(26-8\sqrt3)-36\bigr]
=\frac{\beta^2}{72}(21+20\sqrt3)>0.
\tag{26}
$$
Releasing the singular prefix $W_2=\frac\beta2\left(\begin{smallmatrix}1&-i\\ i&1\end{smallmatrix}\right)$ ($\det W_2=0$) of [Gaussian field transport](gaussian_field_transport_on_native_histories.md) to $W_2^{\rm ext}$ is mathematically forced: as shown in Eq. (2) of [stationary dynamics for four-chain fields](stationary_dynamics_for_four_chain_fields.md), any finite positive-frequency ground state realizing $W_2$ on $(z_a,z_b)=((0,0),(1,0))$ saturates the unit-circle triangle inequality, forcing every occupied mode phase at $\xi=0$ to satisfy $e^{-i\theta_j}=i$ and collapsing $[\phi_x,\phi_a]=0$ on every $I_x=\{a,b\}$ continuation (native mass $836/1320$ for $P_0$ and $616/1320$ for $P_1$).

### 5.4 Exact branchwise and unread old-field Weyl-algebra preservation

On $\mathcal S(\mathbb R^{12})$, every real linear combination $\Phi_H(u)=\sum_{r\in\{a,b,x,y\}}u_r\phi_r(H)$ ($u\in\mathbb R^4$) is essentially self-adjoint (by Nelson's analytic-vector theorem on the Hermite basis), generating bounded Weyl unitaries $\mathcal W_H(u):=\exp\bigl(i\overline{\Phi_H(u)}\bigr)$ on $L^2(\mathbb R^{12})$ that satisfy
$$
\mathcal W_H(u)\mathcal W_H(u')=e^{-\frac{i}{2}u^T D(H)u'}\mathcal W_H(u+u'),\qquad
\omega_{\rm vac}\bigl(\mathcal W_H(u)\bigr)=\exp\!\left(-\frac12 u^T V(H)u\right).
\tag{27}
$$
Because $\mathcal H=L^2(\mathbb R^{12})$, $K$, $\Psi$, and $\omega_{\rm vac}$ are prepared once prior to both suffix births and are independent of $(i,I_x,I_y,b_3,b_4)$:
1. **Stage $2\to3$ and $2\to4$ preservation.** The operators $\phi_a=\Psi(0,0)$ and $\phi_b=\Psi(1,0)$ are identical on all 60 marked histories. For every $u=(u_a,u_b)^T\in\mathbb R^2$ with stage-4 inclusion $\iota_2 u=(u_a,u_b,0,0)^T$, $\mathcal W_H(\iota_2 u)=\mathcal W_2(u):=\exp\bigl(i\overline{u_a\phi_a+u_b\phi_b}\bigr)$ and $W_4(H)[a,b;a,b]=W_2^{\rm ext}$ hold branch by branch. Summing over all 60 marked histories under either prepared source $i\in\{0,1\}$ gives exact unread covariance and Weyl-expectation preservation:
   $$
   \sum_{H=1}^{60}P_i(H)\,W_4(H)[a,b;a,b]=W_2^{\rm ext}\sum_{H=1}^{60}P_i(H)=W_2^{\rm ext},\qquad
   \sum_{H=1}^{60}P_i(H)\,\omega_{\rm vac}(A)=\omega_{\rm vac}(A)
   \tag{28}
   $$
   for every bounded observable $A$ in the stage-2 Weyl $C^*$-algebra (or von Neumann algebra) generated by $\{\mathcal W_2(u):u\in\mathbb R^2\}$.
2. **Stage $3\to4$ conditional preservation.** Conditional on any realized stage-3 prefix $(I_x,b_3)$, the triple $(\phi_a,\phi_b,\phi_x(I_x))$ is identical across all allowed stage-4 continuations $(I_y,b_4)$. For every $u=(u_a,u_b,u_x)^T\in\mathbb R^3$ with $\iota_3 u=(u_a,u_b,u_x,0)^T$, $\mathcal W_H(\iota_3 u)=\mathcal W_{3,I_x}(u)$ and $W_4(I_x,I_y)[a,b,x;a,b,x]=W_3(I_x)$ are independent of $(I_y,b_4)$, so averaging against the normalized conditional fourth-birth law $\frac14 q_4(I_y\mid I_x,i)$ preserves $W_3(I_x)$ and $\omega_{\rm vac}(B)$ identically for every bounded stage-3 observable $B$.

No field moment, phase, or readout feeds back into the native transition weights $P_0,P_1$, fair newborn bits, or optional counters. If an attachment-availability tag is recorded alongside the 15-row ledger, its status is upgraded from `"unavailable"` on 14 rows to **available on all 15 structural rows ($1320/1320$, all 60 marked histories per prepared source)**.

---

## 6. Dimensional ledger, anti-smuggling audit, and scope limits

When the optional physical standards $c,\tau,A_*,\kappa_1>0$ and field unit $\mathcal F$ are declared for the local $1+1$D action field $\Phi_{\rm sc}$ in (20)–(21), define the ground-state energy $E_0^{(1+1)}:=\omega_{\rm vac}(H_{1+1})=\langle\Omega_0,H_{1+1}\Omega_0\rangle=\frac{27\pi A_*}{\tau}>0$. Because $\omega_{\rm vac}\bigl(R_{m,\sigma}(t,x)R_{m',\sigma'}(t,x)\bigr)=\frac12\delta_{mm'}\delta_{\sigma\sigma'}$ (in particular $\omega_{\rm vac}(R_{m,\sigma}(t,x)^2)=\frac12$ pointwise), $\omega_{\rm vac}\bigl(\mathcal H_{1+1}(t,x)\bigr)=\kappa_1\sum_{m=0}^5 B_m^2\kappa_m^2=\frac{E_0^{(1+1)}}{L}$ is spatially uniform, and with $\omega_0=\theta_0/\tau=23\pi/(4\tau)$ denoting the $m=0$ angular frequency in (14), every dimensional and dimensionless relation is explicit:
$$
\frac{L}{c\tau}=4,\qquad
\frac{E_0^{(1+1)}\tau}{A_*}=27\pi,\qquad
\omega_{\rm vac}\bigl(\mathcal H_{1+1}(t,x)\bigr)=\frac{E_0^{(1+1)}}{L}=\frac{27\pi A_*}{4c\tau^2},
$$
$$
F_*^2=\frac{2A_*c^2}{\kappa_1 L\omega_0\,\beta c_0}
=\frac{12A_*c}{23\pi\kappa_1\beta(\sqrt3+\sqrt2)(\sqrt2+1)}.
\tag{29}
$$
Here $[t]=[\tau]=\text{time}$, $[x]=[L]=\text{length}$, $[c]=\text{length}/\text{time}$, $[A_*]=\text{energy}\cdot\text{time}$, $[\Phi_{\rm sc}]=[\Psi_{\rm cal}]=[B_m]=[F_*]=\mathcal F$, $[\kappa_1]=\text{energy}\cdot\text{length}/\mathcal F^2$, $[\mu_1]=\text{energy}\cdot\text{time}^2/\mathcal F^2$, $[q_{m,a}]=\mathcal F$, $[p_{m,a}]=\text{action}/\mathcal F$, $[\Gamma_{\rm read}]=\text{length}^{-1}$, $[\mathcal P_{1+1}]=\text{energy}/\text{time}$ ($1+1$D energy flux), and $[\mathcal H_{1+1}]=[\mathcal P_{1+1}/c]=\text{energy}/\text{length}$ ($1+1$D energy density). Rescaling $\Phi_{\rm sc}\mapsto s\Phi_{\rm sc}$ and $\kappa_1\mapsto\kappa_1/s^2$ ($s>0$) rescales $B_m,F_*$ by $s$ while leaving $H_{1+1}$, $\mathcal H_{1+1}$, $\eta_m$, and $\Gamma_{\rm read}$ invariant. Adding $CI$ to $H_{1+1}$ or normal-ordering away $E_0^{(1+1)}$ would leave Heisenberg evolution (19) unchanged while modifying the unshifted action integral (21); neither offset is claimed to represent a continuum vacuum energy.

**Strict separation of native vs. externally supplied ingredients:**
- **Supplied by the native growth law:** Only the 15 four-birth posets above $a\prec b$, the fair newborn-mark factor $1/4$ per structural row, and the exact conditional probability laws $P_0,P_1$ over the 60 marked histories ($1320$ structural denominator, $5280$ marked denominator).
- **Externally supplied mathematical and physical choices:** The $1+1$D Minkowski cylinder $\mathbb R\times S_L^1$ and metric signature, the adapted coordinate map $(z_a,z_b,z_x(I_x),z_y(I_x,I_y))\in\frac13\mathbb Z^2$, the target-first Johnston commutator normalization $\beta>0$, the 12 canonical oscillator pairs on $L^2(\mathbb R^{12})$ and stationary Gaussian ground state $\omega_{\rm vac}$, the odd-harmonic discrete square-wave mode set $N=12$ and frequency reflection $\tilde\varphi_m=2\pi-\varphi_m$, the readout filter $\Gamma_{\rm read}$ when paired with a local kinetic action, and any optional physical standards $c,\tau,A_*,\kappa_1,\mathcal F$.

**Explicit non-claims and boundaries:**
1. *Non-uniqueness of geometry and spectrum.* While $q=3$ is the minimal lattice denominator for row $I_x=\{a\},\ I_y=\{a,x\}$ with $(z_a,z_b)=((0,0),(1,0))$, infinitely many continuous or finer-lattice adapted embeddings in $\mathbb R^{1,1}$ realize the same 15 discrete orders. Likewise, any even harmonic count $N=2M\ge10$ and any positive integer aliases $\tilde\varphi_m+2\pi k_m$ ($k_m\in\mathbb Z_{\ge0}$) preserve all sampled commutators (24) while altering $W_0$, off-cone correlations, and the excitation gaps of $K$. Neither spacetime dimensionality nor generator gaps are uniquely reconstructed from the four-birth order law.
2. *Finite-mode projector vs. continuum microcausality.* With only 12 anti-periodic oscillator modes on $L^2(\mathbb R^{12})$ (infinite-dimensional Hilbert space, finite mode count), the equal-time canonical commutator $[\Phi_{\rm sc}(t,x),\kappa_1 c^{-2}\dot\Phi_{\rm sc}(t,y)]$ equals $iA_*$ times the 12-mode anti-periodic projector kernel $\frac{2}{L}\sum_{m=0}^5\cos\bigl(\kappa_m(x-y)\bigr)$ rather than $iA_*\delta(x-y)$, and off-lattice continuum commutators $[\Psi(z),\Psi(z')]$ vanish or equal $\pm i\beta I$ on the $\frac13\mathbb Z^2$ lattice up to $|\nu_\pm|\le11$ rather than vanishing everywhere outside the continuum lightcone.
3. *No $3+1$D non-chain gravitational source, carrier mass, or Status-M promotion.* Extending positive stationary field dynamics to all 15 rows on $\mathbb R\times S_L^1$ is a kinematic and positive-Hamiltonian spacetime realization, not a $3+1$D stress-energy source or linearized Einstein solution on non-chain branches (in the accepted observables corpus prior to any separate compact-cavity registration, local $3+1$D stress-energy attachment is formulated only on the 4-chain in the [local $3+1$D scalar source lift](local_scalar_source_for_four_chain_field.md), where periodic $\mathbb T_L^3$ encounters the spatial-mean Poisson obstruction). Positive oscillator gaps $\theta_m$ do not establish carrier rest mass or inertia, no sequential joint-measurement apparatus or energetic preparation/reset budget is supplied, software execution remains paused, and all Track-B / Status-M ontological commitments remain strictly quarantined.

## Scientific review

All-Branch Spacelike Field Author derived the single-point non-chain obstruction theorem, minimal-denominator adapted $\frac13\mathbb Z^2$ causal embedding, reflected odd-harmonic discrete square-wave kernel, 12-mode anti-periodic $1+1$D wavefield and positive generator, Vandermonde covariance positivity, closed-form four-chain radical lags, and 60-history Weyl-algebra marginal preservation. Independent All-Branch Field Reviewer independently verified all 90 lightcone integer pairs, both square-wave proofs, commutator signs, Vandermonde invertibility, cotangent radicals, action/readout calibration, native probability sums, dimensional relations, and scope boundaries. Prospective protocol SHA-256 1d902eb847031ffbb353ee784b66843729d7e17e527523a8d41d8d9a9f50103b; accepted author report SHA-256 012ac7fdee69d0168fd6293d432b5e29d5918d8cb4c61071d9cb07203acf2443; independent scientific review SHA-256 d6bd3af934ff0a7441aa4c7890caa6771f2ad02f669ad7cf8e0186477397ec26.
