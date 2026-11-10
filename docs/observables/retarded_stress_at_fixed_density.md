# A retarded tidal channel from stress at fixed energy density

**Decision: the specified stress freedom survives as a nonzero outgoing radiative curvature coefficient.** Two smooth spatially compact conserved sources share the same pointwise energy density and zero momentum density at every time, yet have opposite signals in one fixed transverse tidal channel. The leading density-quadrupole truncation returns zero. Keeping the source's spatial retardation phase gives a nonzero term starting at second order in that phase, and a curvature coefficient of fourth order in frequency.

This is a conventional first-order prescribed-source calculation. The modulation, geometry, gravitational equation and physical standards are supplied. No material realization, native tensor map, preparation protocol or nonlinear energy-balance closure is established.

## 1. One frozen modulation, direction and channel

Use signature $(-+++)$, $x^0=ct$, and supplied $G,c,u,R>0$, where $u$ is an energy density and $R$ a length. Reuse the accepted [static stress source](stress_quadrupole_at_equal_energy.md) functions, with no change to their spatial shapes:

$$
b(z)=\begin{cases}e^{-1/z},&z>0,\\0,&z\le0,\end{cases}\qquad
s=|x|/R,\qquad
\chi(s)=\frac{b(4-s^2)}{b(4-s^2)+b(s^2-1)},
$$
$$
\varepsilon(x)=u\chi(s),\quad
f(x)=uR^2 b(1-s^2),\quad
S=\operatorname{diag}(-1/2,-1/2,1),
$$
$$
D_{ij}=\epsilon_{ikm}\epsilon_{jln}S_{mn}\partial_k\partial_l f,
\qquad \epsilon_{123}=+1.
\tag{1}
$$

The energy density equals $u$ on the stress support $r\le R$, and vanishes beyond $2R$. The bump $f$, the stress and all their derivatives vanish at their support boundary. The accepted source proof, distinct review and disposition establish symmetry of $D$, $\partial_iD_{ij}=0$, and the explicit bound

$$
\|D\|\le2uM,\qquad
M=8e^{-2}+216e^{-3}+1024e^{-4}.
\tag{2}
$$

Freeze

$$
\lambda=\frac1{8M},\qquad
\omega=\frac{c}{2R},\qquad k=\omega/c=\frac1{2R},\qquad
g(t)=\cos(\omega t).
\tag{3}
$$

There is one modulation, with a common registered phase origin. The two source alternatives differ only in the sign of their stress:

$$
T^{00}_\pm(t,x)=\varepsilon(x),\qquad
T^{0i}_\pm=T^{i0}_\pm=0,\qquad
T^{ij}_\pm(t,x)=\pm\lambda\cos(\omega t)D_{ij}(x).
\tag{4}
$$

Freeze the observation ray $n=e_1$, transverse to the symmetry axis of $S$. Its transverse axes are $e_2,e_3$. Use only the plus electric-curvature channel

$$
\mathcal E_\pm(t,r)=\frac12
\left(R^{(1),\pm}_{0202}-R^{(1),\pm}_{0303}\right)(t,re_1).
\tag{5}
$$

The radiative observable is its $1/r$ coefficient at fixed retarded time $U=t-r/c$. A single phase-resolved comparison at $U=0$ will supply the nonzero result. Receivers in the exterior interpretation lie at r>2R, outside the complete matter support. This is an ideal asymptotic channel; no finite-radius detector is assumed. The small-frequency expansion below classifies this same analytic expression, not an additional modulation, direction or source scan.

## 2. Conservation, support and retained registration

All four flat-background conservation equations hold for all times. The energy equation is

$$
\partial_0T^{00}+\partial_iT^{i0}=0+0=0.
$$

For each spatial index $j$,

$$
\partial_0T^{0j}+\partial_iT^{ij}
=0\pm\lambda\cos(\omega t)\partial_iD_{ij}=0.
\tag{6}
$$

A time derivative of $T^{ij}$ does not occur in these divergence equations. Thus the time-dependent stress is not excluded by these conservation constraints. Smooth compact support makes the identities valid across the boundaries without a surface source. Symmetry and $|\cos|\le1$ give the uniform margin

$$
\|T^{ij}_\pm(t,x)\|\le\varepsilon(x)/4.
\tag{7}
$$

The shared integrated matter energy is $E=\int\varepsilon\,d^3x>0$; the shared momentum is $P^i=c^{-1}\int T^{0i}d^3x=0$. The complete density and all its spatial moments are identical and constant in time. Integration by parts gives, at every time,

$$
\int T^{ij}_\pm\,d^3x=0,\qquad
\int y_aD_{ij}(y)\,d^3y=0.
\tag{8}
$$

These statements concern the entire prescribed matter tensor. The static source boosted-slice calculation is not being reapplied to a nonstationary source, and no new acceleration-mass assay is asserted.

The source is compact in space at each time and bounded for all time, not compact in spacetime. The single harmonic is an eternal steady-state ansatz. Its retarded convolution is well-defined because only a bounded spatial region contributes to each field point. We choose the retarded solution without adding a free incoming wave. We do not claim a finite-time switch-on, finite total emitted wave energy over an infinite past, or a causal material mechanism generating the prescribed synchronous stress.

## 3. Retarded field with the full spatial phase

Supply the linearized harmonic-gauge equations

$$
\Box\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu},\qquad
\Box=\nabla^2-c^{-2}\partial_t^2,
$$
$$
\bar h_{\mu\nu}(t,x)=\frac{4G}{c^4}\int
\frac{T_{\mu\nu}(t-|x-y|/c,y)}{|x-y|}\,d^3y,
\qquad
h_{\mu\nu}=\bar h_{\mu\nu}
-\frac12\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta}.
\tag{9}
$$

These are the retarded conventional equations, with $c$ restored and $T$ in energy-density units. Carroll's versioned equation (6.74) precedes the additional replacement of the spatial source phase in (6.78); that replacement is not made here. [Carroll, *Lecture Notes on General Relativity*, gr-qc/9712019v1, §6](https://arxiv.org/pdf/gr-qc/9712019v1).

Define one outgoing scalar convolution and its radial Fourier factor:

$$
I_k(x)=\int f(y)\frac{e^{ik|x-y|}}{|x-y|}\,d^3y,
\qquad
\widehat f(k)=4\pi\int_0^R a^2 f(a)\operatorname{sinc}(ka)\,da,
\quad\operatorname{sinc}z=\frac{\sin z}{z}.
\tag{10}
$$

Here $f(a)$ denotes the radial value of the bump. For $r=|x|>R$, the angular integral over a shell of radius $a$ is exactly

$$
\int_{S^2}\frac{e^{ik|x-a\hat y|}}{|x-a\hat y|}\,d\Omega
=\frac{2\pi}{ra}\int_{r-a}^{r+a}e^{ikd}\,dd
=\frac{4\pi e^{ikr}}r\operatorname{sinc}(ka).
$$

Consequently

$$
I_k(x)=\widehat f(k)\frac{e^{ikr}}r,\qquad r>R.
\tag{11}
$$

This is an exact exterior retarded-phase identity. Twice integrating (1) by parts against the outgoing kernel gives the time-dependent stress field, also exactly:

$$
\bar h^{\pm,\mathrm{stress}}_{ij}(t,x)
=\pm\frac{4G\lambda}{c^4}\operatorname{Re}\left[
 e^{-i\omega t}\epsilon_{ikm}\epsilon_{jln}S_{mn}
 \partial_k\partial_l I_k(x)\right].
\tag{12}
$$

Both derivative signs from changing source to target coordinates cancel. Compact flat support removes the boundary terms. The time-dependent part has $\bar h_{00}=\bar h_{0i}=0$; the common static energy field remains separately present. Its spatial divergence vanishes exactly by the epsilon contraction, while the common $\bar h_{00}$ is static. Thus harmonic-gauge compatibility holds, consistent with (6).

Equivalently, taking $r\to\infty$ at fixed $U=t-r/c$ in (9) retains the phase

$$
\cos[\omega U+k n\cdot y],
$$

not merely $\cos(\omega U)$. The Fourier convention

$$
\widehat D_{ij}(kn)=\int D_{ij}(y)e^{-ikn\cdot y}\,d^3y
=-k^2\widehat f(k)\epsilon_{iam}n_a\epsilon_{jbq}n_b S_{mq}
\tag{13}
$$

uses real even tensors, so the sine integral vanishes and either sign of the spatial Fourier phase gives the same real coefficient. This formula also shows exact transversality of the radiative coefficient. Differentiating (11) gives (13) as its leading $1/r$ term, with subleading inverse-radius terms retained by (12).

## 4. The fixed transverse tidal contrast

For $n=e_1$, direct epsilon contraction gives

$$
\widehat D_{11}=\widehat D_{12}=\widehat D_{13}=0,\qquad
\widehat D_{22}=-k^2\widehat f(k),\qquad
\widehat D_{33}=\tfrac12 k^2\widehat f(k),\qquad
\widehat D_{23}=0.
\tag{14}
$$

Let $P_{ij}=\delta_{ij}-n_in_j$. The transverse tracefree projection of a symmetric tensor is
$D^{TT}_{ij}=P_{ia}P_{jb}D_{ab}-P_{ij}P_{ab}D_{ab}/2$.
It gives

$$
\widehat D^{TT}_{22}=-\frac34k^2\widehat f(k),\qquad
\widehat D^{TT}_{33}=+\frac34k^2\widehat f(k).
\tag{15}
$$

Trace reversal does not change this projection. With $h_+=(h^{TT}_{22}-h^{TT}_{33})/2$, the outgoing metric coefficient is

$$
h^{\pm}_+(t,re_1)
=\mp\frac{3G\lambda k^2\widehat f(k)}{c^4r}
\cos(\omega U)+O(r^{-2}).
\tag{16}
$$

Only the asymptotic coefficient is called TT here; an exact finite-radius transverse-gauge identification is not required.

Use the same curvature convention as the static source,

$$
R^\rho{}_{\sigma\mu\nu}
=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\alpha}\Gamma^\alpha_{\nu\sigma}
-\Gamma^\rho_{\nu\alpha}\Gamma^\alpha_{\mu\sigma}.
$$

For the stress contrast $h_{0i}=0$, and the exact linearized channel is

$$
\mathcal E=-\frac14\left[
(\partial_2^2-\partial_3^2)h_{00}
+\partial_0^2(h_{22}-h_{33})\right].
\tag{17}
$$

Along the fixed ray, transverse derivatives of an outgoing $e^{ikr}/r$ coefficient contribute no $1/r$ term. Thus the $h_{00}$ term in (17) is subleading. The common static energy contribution cancels in the source contrast. The radiative term is $-\partial_t^2h_+/(2c^2)$, so, with $\Delta=+\text{ source}-(-\text{ source})$,

$$
\Delta\mathcal E(t,r)
=-\frac{3G\lambda k^4\widehat f(k)}{c^4r}
\cos(\omega U)+O(r^{-2}).
\tag{18}
$$

In particular the frozen, single-phase observable is

$$
\boxed{
\mathcal C:=\lim_{r\to\infty}r\,
\Delta\mathcal E(r/c,r)
=-\frac{3G\lambda k^4\widehat f(k)}{c^4}<0,
\quad k=\frac1{2R}.}
\tag{19}
$$

To prove strictness without numerical quadrature, put $F=\int f\,d^3y>0$. Since $\operatorname{sinc}z=\int_0^1\cos(tz)dt$,

$$
F\left(1-\frac{(kR)^2}{6}\right)\le\widehat f(k)\le F
\quad (0\le kR\le1/2).
\tag{20}
$$

At the frozen frequency this gives $\widehat f\ge23F/24>0$. Hence

$$
\frac{23}{24}\frac{3G\lambda F}{16c^4R^4}
\le |\mathcal C|\le
\frac{3G\lambda F}{16c^4R^4}.
\tag{21}
$$

The source signs, ray, polarization and phase origin are fixed throughout. Linearized Riemann about flat spacetime is gauge invariant, so the contrast is not removable by a gauge transformation. A receiver tetrad aligned with the supplied background axes gives the same first-order channel; perturbative frame corrections enter beyond the retained order. The corresponding relative-acceleration contrast is $-c^2\Delta\mathcal E$ in the stated polarization convention.

Equations (16) and (18) are large-distance expansions at fixed nonzero $k$, fixed retarded time and direction. The exact exterior expression (12) determines their finite-distance corrections. For this smooth compact harmonic source its differentiated inverse-radius expansion has remainder $O(r^{-2})$ at fixed $k$. A finite-distance interpretation requires the wave-zone limit as well as exterior support, conventionally $r\gg R$ and $kr\gg1$; exteriority alone is not a radiative approximation. No finite-radius error certificate or detector noise budget is claimed. The small-frequency expansion below is applied to the radiative coefficient after this far-field limit, not by sending $k\to0$ at fixed receiver radius.

## 5. Why the density-quadrupole truncation gives zero

The zeroth spatial-phase term replaces the retarded stress coefficient by $\int T^{ij}(U,y)d^3y$, which vanishes exactly. The first phase term also vanishes by (8). The quadratic spatial-phase term is the first survivor and gives the $-k^2\widehat f$ structure in (13).

Under the additional long-wavelength replacement, compact conservation relates the stress integral to half the second time derivative of the energy second moment divided by $c^2$. That moment is fixed here, so the leading density-quadrupole radiation term is zero. Carroll derives that density form only after (6.78), in (6.80)–(6.85); it is not an exact statement with all spatial retardation retained. [Carroll, gr-qc/9712019v1, §6, equations (6.78)–(6.85)](https://arxiv.org/pdf/gr-qc/9712019v1).

For a quantitative order statement define $F_2=\int |y|^2f(y)d^3y$ and $F_4=\int |y|^4f(y)d^3y$. Taylor's bound for sinc yields

$$
\widehat f(k)=F-\frac{k^2F_2}{6}+\rho_k,
\qquad |\rho_k|\le\frac{k^4F_4}{120}
\le\frac{F(kR)^4}{120}.
\tag{22}
$$

Thus the difference of metric radiation coefficients starts at
$-6G\lambda Fk^2/c^4$, and the electric-curvature coefficient at
$-3G\lambda Fk^4/c^4$, each with relative correction $O((kR)^2)$. The nonzero leading constants and the bound are explicit. The supplied matter model has no independent slow-material-motion expansion or constitutive relation that would remove these stress terms. Keeping only the vanished density-quadrupole order therefore misses a higher spatial-retardation contribution. This is a truncation boundary, not a failure of conservation and not a contradiction of the leading quadrupole formula in its approximation regime.

## 6. Meaning and limits of the result

The retained equality is pointwise $T^{00}$ and $T^{0i}$ in one common background frame, for all times, together with all density moments and integrated matter energy. The two admissible stresses nevertheless give the distinct outgoing curvature (19). In this prescribed conserved-tensor class, registering that density and matter energy cannot determine the selected radiative signal. A predictive source attachment must additionally determine the time-dependent stress, or justify a constitutive restriction excluding this pair. The calculation does not derive such an attachment from DET or rule out all possible native constructions.

All components of $T$ have energy-density units; $f$ has energy per length units; $F$ and $\widehat f$ have energy times length squared units. The metric is dimensionless, $\mathcal E$ has inverse-length-squared units, $\mathcal C=r\Delta\mathcal E$ has inverse-length units, and $-c^2\mathcal E$ has inverse-time-squared units. Geometry, source phase/frequency, $G,c,u,R$, clock standards and transverse readout axes are supplied. The weak-field scale $GuR^2/c^4\ll1$ keeps this a first-order metric/curvature calculation with a prescribed zeroth-order source.

Outgoing curvature is established at the retained linear order. Wave-energy flux is quadratic in the metric perturbation; when its conventional normalization is included it requires a corresponding higher-order source/reaction accounting. Flat-background conservation of the prescribed matter tensor alone is not that accounting. We do not infer an energy-free radiating material, self-sustained oscillation, a closed source-plus-wave energy ledger, or a nonlinear solution with exactly unchanged density. No physical constitutive equation, source preparation, sustaining mechanism, work transfer, reset or empirical detector has been supplied. The retarded field law establishes propagation from the specified source; it does not establish how the modulation can be physically generated.

## Scientific review

Quantum Relativity derived this finite retarded source calculation. Relational State independently checked conservation, exact outgoing convolution, full spatial phase, transverse projection, curvature sign, strict transform bound, frequency order and limits. Author report SHA-256 68527f817236423707092205a7c27e74972bdc1017a9066ee26b0b763f90ffbc; independent review 6cb23299b951087c37cd2d0ae642877e01fdd10084dd59f9a49ebe4b6ff2c823.
