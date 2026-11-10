# Mass and signed spin from two rotating optical rings

**Result.** Four first-return proper durations at two registered equatorial Kerr radii uniquely determine the mass length $m$, signed spin length $a$ and common apparatus angular rate $\Omega$ on every compatible record except one. When both source and receivers are nonrotating, the readings are $T_{i+}=T_{i-}=2\pi r_i$. Those data force $a=\Omega=0$ but admit every $0<m<r_1/2$.

## What the two directions measure

Use the supplied neutral Kerr exterior with $0<2m<r_1<r_2$, $|a|\le m$, and $t$ in length units. The two guided null pulses leave the same local emitter and return to that moving receiver after one relative winding in their labelled directions. At either radius put
$$
H=g_{\phi\phi}=r^2+a^2+2ma^2/r,\quad B=g_{t\phi}=-2ma/r,\quad
D=B^2-g_{tt}H=r^2-2mr+a^2,\quad C=B+H\Omega .
$$
The receiver's proper-length rate is $N=d\tau/dt=\sqrt{(D-C^2)/H}$. Timelikeness is exactly $|C|<\sqrt D$. The null slopes $w_\pm=(-B\pm\sqrt D)/H$ solve the quadratic for constant-radius propagation. Since $r>2m$, $w_-<0<w_+$, and the timelike receiver has $w_-<\Omega<w_+$. The pulses first gain one full turn relative to the receiver at coordinate intervals $2\pi/(w_+-\Omega)$ and $2\pi/(\Omega-w_-)$, respectively. Multiplication by $N$ gives the measured proper durations
$$
T_\pm=\frac{2\pi HN}{\sqrt D\mp C}.
$$
The labels are the registered azimuthal senses, regardless of which pulse arrives first. Guided counterpropagation in a rotating metric motivates the observable. [Tartaglia & Ruggiero](https://arxiv.org/abs/2103.03763v1)

The positive durations at each site are equivalently represented by
$$
H_i=\frac{T_{i+}T_{i-}}{4\pi^2},\qquad
s_i=\frac{T_{i+}-T_{i-}}{T_{i+}+T_{i-}}=\frac{C_i}{\sqrt{D_i}} .
$$
Indeed the two denominators in the product multiply to $D-C^2=HN^2$. Thus $\sqrt{T_{i+}T_{i-}}=2\pi\sqrt{H_i}$ measures the geometric circumference **on a constant Boyer–Lindquist $t$ slice**. The arithmetic mean is larger by the factor $1/\sqrt{1-s_i^2}$ whenever $s_i\ne0$. The directional imbalance measures $B_i+H_i\Omega$ relative to $\sqrt{D_i}$, so source spin and receiver rotation both enter it.

## Complete inverse for four labelled readings

Require finite, strictly positive $T_{i\pm}$, the two known radii in the stated order and the specified orientation. These checks give $H_i>0,\ |s_i|<1$. Write $S_i=H_i-r_i^2$ and calculate
$$
U=\frac{r_2 S_2-r_1 S_1}{r_2-r_1},\qquad
V=\frac{r_1r_2(S_1-S_2)}{r_2-r_1}.
$$
The products require $S_i=U+V/r_i$, with $U=a^2,\ V=2ma^2$. The allowed cases are as follows.

**Spinning source, $U>0$.** Set $m=V/(2U)$. Require $0<m<r_1/2$ and $U\le m^2$, allowing extremal spin. From the measured differences form
$$
D_i=r_i^2-2mr_i+U,\qquad C_i=s_i\sqrt{D_i}.
$$
Multiplying $C_i=H_i\Omega-2ma/r_i$ by $r_i$ and subtracting the two equations gives the only candidate
$$
\Omega=\frac{r_2C_2-r_1C_1}{r_2H_2-r_1H_1},\qquad
a=\frac{r_1(H_1\Omega-C_1)}{2m}.
$$
The denominator is $r_2^3-r_1^3+U(r_2-r_1)>0$. Require $a^2=U$ exactly. Failure rejects the record; success fixes the signed $a$ as well as $m,\Omega$. For static receivers $C_i=-2ma/r_i$, so the spin sign follows from the opposite sign of either measured imbalance. A single symmetric pair of times is possible on a spinning source when the receiver motion cancels the local $B_i$. Simultaneous cancellation at both radii would force $\Omega=0$ by the difference equation and then $a=0$.

**Nonrotating source, $U=V=0$.** The product data now give $H_i=r_i^2$. Define $k_i=s_i/r_i$. The signed equations reduce to $k_i=\Omega/\sqrt{1-2m/r_i}$.

- If both $k_i$ vanish, $\Omega=0$. Every $m\in(0,r_1/2)$ gives the four stated durations and timelike static receivers. The coordinate light-travel time and clock rate vary with $m$; their product in each proper return time is $2\pi r_i$.
- For nonzero motion require both $k_i$ nonzero, with the same sign and $|k_1|>|k_2|$. The strict ordering follows from $m>0,\ r_1<r_2$. Equating $k_i^2(1-2m/r_i)=\Omega^2$ yields
  $$
  m=\frac{k_1^2-k_2^2}{2(k_1^2/r_1-k_2^2/r_2)},\qquad
  \Omega=k_1\sqrt{1-2m/r_1}.
  $$
  The strict inequalities make the denominator positive and $0<m<r_1/2$. The common sign restores the second unsquared equation. Thus receiver rotation can identify mass even with zero source spin. One zero imbalance, opposite signs or failure of the strict ordering gives no solution in this branch.

All remaining product cases, including $U<0$ or $U=0,\ V\ne0$, are incompatible. For every accepted candidate, both $D_i>0$ and $N_i^2=D_i(1-s_i^2)/H_i>0$; this checks each receiver against the corresponding null slopes. Substitution reproduces $H_i,s_i$, which determine the durations individually by $T_{i\pm}=2\pi\sqrt{H_i}\sqrt{(1\pm s_i)/(1\mp s_i)}$. This proves sufficiency as well as excluding additional sign branches.

## Calibration of the mass reference

The inverse uses independently registered **Boyer–Lindquist** radii and the same $\Omega=d\phi/dt$ relative to the asymptotically normalized time and oriented azimuth at both sites. The circumference is an output; replacing $r_i$ by $\sqrt{H_i}$ would erase the product information about spin. Each local clock must have a calibrated rate, and its two measured proper durations in seconds are converted to the common length unit by $c$. No shared clock phase zero is required. The first-winding tags, null nondispersive guides, absence of extra propagation delays, and negligible backreaction are physical premises.

With known $G,c$, the dimensional source mass and signed angular momentum are $M=c^2m/G$ and $J=Mac=c^3ma/G$; the apparatus rate in radians per second is $c\Omega$. Assigning these parameters to a physical or DET source requires the stated exterior metric and source, radius, orientation and clock correspondences. The result is an exact inverse within that supplied model.

## Scientific review

DET Quantum Relativity supplied the derivation. A distinct scientific reviewer verified the tagged return paths, the signed inverse and the static mass ambiguity. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `1da6af8b186121768b108acb88bc05c3818a3cc0884cdcbf4d82f422cbd822c1`.
- Author report SHA-256: `bdff77e7f64a76fb27e610f764bb7f932bf2bd7dae9312b3195cc8d70a8b30df`.
- Freeze SHA-256: `a2e981bfbe6472fabf565e256ec81787cc01bd5e33c1f5325ba0659c4f74b6fa`.
- Independent scientific review SHA-256: `fb7b6a81c29c682a1749e0b43f3ac96a4e09ae6fc06ae8cad46887078c79d6c1`.
