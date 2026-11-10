# Equal energy and inertia with different exterior stress quadrupoles

Conditional analytic source construction

Yes. In the supplied static linearized gravitational model, two smooth compact conserved tensors can have exactly the same pointwise nonnegative energy density and the same integrated boost-defined inertia, while producing different exterior tidal curvature. The pair below has opposite internal stresses, each bounded in operator norm by half the common energy density. Its stress integrals vanish, but its stress-weighted quadrupole moments do not. Energy-density and total-inertia registration therefore leave an independent spatial stress datum undetermined.

This is one conventional source pair and one finite exterior contrast. It supplies no DET-native tensor attachment, equation of state, material realization, nonlinear equilibrium or empirical certification. The double-curl ansatz in the assignment was a hypothesis; the conservation, admissibility and nonzero curvature calculations below establish its stated conditional use.

The [closed-source active-mass note](closed_radiation_shell_mass.md) supplies the linearized field convention. Its [same-source boost companion](closed_radiation_shell_inertia.md) supplies the simultaneous-slice inertia calculation. Their equations and approximation boundaries are retained; this construction is a different smooth compact source.

Use Cartesian background coordinates with signature $(-+++)$, $x^0=ct$, supplied $G,c>0$, and static tensors on all space. Let $u>0$ have energy-density units and $R>0$ have length units. Define the smooth flat bump
$$
 b(t)=\begin{cases}e^{-1/t},&t>0,\\0,&t\le0,\end{cases}
\quad s=\frac{|x|}{R},\qquad
 \chi(s)=\frac{b(4-s^2)}{b(4-s^2)+b(s^2-1)}.
$$
The denominator is never zero: both arguments cannot be nonpositive. This is a smooth function of $|x|^2/R^2$, equal to one for $s\le1$, positive for $s<2$, and zero for $s\ge2$. All derivatives match at its boundaries. Put
$$
 \varepsilon(x)=u\chi(s),\qquad
 f(x)=uR^2 b(1-s^2),\qquad
 S=\operatorname{diag}(-1/2,-1/2,1).
 \tag{1}
$$
Here $S$ is fixed, symmetric and tracefree, with operator norm one. The bump $f$ and all its derivatives vanish at and beyond $r=R$. The common energy density extends to $2R$. Set
$$
 D_{ij}=\epsilon_{ikm}\epsilon_{jln}S_{mn}\partial_k\partial_l f,
 \qquad \epsilon_{123}=+1,
 \tag{2}
$$
and define the pair
$$
 T^{00}_+=T^{00}_-=\varepsilon,\qquad
 T^{0i}_\pm=T^{i0}_\pm=0,\qquad
 T^{ij}_\pm=\pm\lambda D_{ij}. \tag{3}
$$
Spatial lowering changes no sign, and $T_{00}=T^{00}$. The dimensionless positive $\lambda$ is fixed below. Both complete tensors are static and smooth with compact support in the closed ball of radius $2R$, with no surface distribution or omitted boundary support.

To check symmetry, exchange $i,j$ in (2) and then exchange $k,l$ and $m,n$; the Hessian and $S$ are symmetric. Thus $D_{ij}=D_{ji}$. Divergence vanishes identically:
$$
 \partial_iD_{ij}
 =\epsilon_{ikm}\epsilon_{jln}S_{mn}\partial_i\partial_k\partial_l f=0,
 \tag{4}
$$
because the third derivative is symmetric in $i,k$. Static $\varepsilon$ and zero energy flux give the remaining component of $\partial_\mu T^{\mu\nu}=0$. These identities hold on all space, including both support boundaries, since the defining functions are smooth and flat where necessary. No external force density or tether is left out of the tensor equation.

The trace follows from contracting the two epsilon tensors:
$$
 \operatorname{tr}D=(\operatorname{tr}S)\nabla^2f-S_{kl}f_{,kl}
 =-S_{kl}f_{,kl}. \tag{5}
$$
Each unweighted integral $\int D_{ij}\,d^3x$ vanishes by integration by parts, as does $\int\operatorname{tr}D\,d^3x$. Equivalently, compact conservation gives
$\int \partial_i(x_k T^{ij})\,d^3x=\int T^{kj}\,d^3x=0$.
The boundary term is genuinely zero for the complete tensor. The first spatial moments of the double derivatives also vanish. None of these unweighted or linear-weight identities says that quadratic-weight moments vanish.

There is an explicit nonzero admissible interval. For $r<R$, write $y=x/R$, $t=1-|y|^2$. Direct differentiation of (1) gives
$$
 \frac{f_{,kl}}u
 =e^{-1/t}\left[-\frac{2\delta_{kl}}{t^2}
 +\left(\frac4{t^4}-\frac8{t^3}\right)y_ky_l\right].
$$
Since $0<t\le1$, $t^{-k}e^{-1/t}\le k^ke^{-k}$ for $k=2,3,4$. Therefore
$$
 \|\operatorname{Hess}f\|\le uM,\qquad
 M=\frac8{e^2}+\frac{216}{e^3}+\frac{1024}{e^4}>0. \tag{6}
$$
This is a finite explicit upper bound, not a numerical estimate. For any unit vector $v$, the matrix $A_{km}=v_i\epsilon_{ikm}$ has rank at most two and norm at most one. With $H=\operatorname{Hess}f$,
$$
 v_iD_{ij}v_j=\operatorname{tr}(HASA^{\mathsf T}),\qquad
 |v_iD_{ij}v_j|\le 2\|H\|\|S\|.
$$
The last inequality uses the nuclear norm of the rank-at-most-two matrix $ASA^{\mathsf T}$. Symmetry of $D$ now gives
$$
 \|D\|\le2uM.
$$
On its support $\varepsilon=u$; outside that support the stress is zero. Thus the entire interval
$$
 0<\lambda\le\frac1{4M} \tag{7}
$$
satisfies, everywhere for both sources,
$$
 \|T^{ij}_\pm(x)\|\le\frac{\varepsilon(x)}2
 \le T^{00}_\pm(x).
 \tag{8}
$$
For a single fixed example, choose $\lambda=1/(8M)$. All subsequent formulas describe that pair, with $\lambda$ left visible to show the constructive admissible interval and scaling. This bound establishes the stated tensor admissibility condition; it is not a certification of an actual material, its stability or its preparation.

Define the positive finite constants
$$
 E=\int\varepsilon\,d^3x
   =uR^3 C_\varepsilon,\qquad
 C_\varepsilon=4\pi\int_0^2s^2\chi(s)\,ds,
$$
$$
 F=\int f\,d^3x=uR^5 C_f,\qquad
 C_f=4\pi\int_0^1s^2e^{-1/(1-s^2)}\,ds>0. \tag{9}
$$
In particular $4\pi/3<C_\varepsilon<32\pi/3$. These integrals specify exact shape constants; numerical quadrature is unnecessary. The two sources share not only $E$ but the entire function $\varepsilon(x)$, its centroid and all its spatial energy moments.

Let $\Sigma^\pm_{ij}=\int T^{ij}_\pm\,d^3x=0$. For a supplied active plus Lorentz boost along the first axis, with $\beta_v=v/c$ and $\gamma=(1-\beta_v^2)^{-1/2}$, the accepted simultaneous-slice formula is
$$
 E'_\pm=\gamma(E+\beta_v^2\Sigma^\pm_{11}),\quad
 P'_{\pm,1}=\frac{\gamma\beta_v}{c}(E+\Sigma^\pm_{11}),\quad
 P'_{\pm,a}=\frac{\beta_v}{c}\Sigma^\pm_{1a}\quad(a=2,3).
$$
It follows, for both tensors, that
$$
 E'_\pm=\gamma E,\qquad P'_{\pm,1}=\gamma vE/c^2,\qquad
 M_{\rm in,\pm}:=\lim_{v\to0}\frac{P'_{\pm,1}}v=\frac E{c^2}.
 \tag{10}
$$
Rotation of the boost axis gives the same coefficient in every direction; the linear inertia tensor is $(E/c^2)\delta_{ij}$. This is an integrated boost-momentum definition within the flat stationary source model, not a derived acceleration protocol. The accepted active-monopole expression likewise gives
$$
 M_{\rm active,\pm}
 =\frac1{c^2}\int(\varepsilon+\operatorname{tr}T_\pm)\,d^3x
 =\frac E{c^2}. \tag{11}
$$
Equations (10) and (11) compare the same complete tensors. Gravitational binding energy and self-gravity corrections are outside the retained approximation.

Now evaluate the tracefree active quadrupole, with its normalization explicitly fixed:
$$
 Q^\pm_{ab}=\frac1{c^2}\int
 (3x_ax_b-r^2\delta_{ab})(\varepsilon+\operatorname{tr}T_\pm)\,d^3x.
 \tag{12}
$$
The radial energy density contributes zero. Twice integrating (5) by parts gives
$$
 \int(3x_ax_b-r^2\delta_{ab})\operatorname{tr}D\,d^3x
 =-S_{kl}\int f\,\partial_k\partial_l
       (3x_ax_b-r^2\delta_{ab})\,d^3x
 =-6F S_{ab}.
$$
Here the differentiated polynomial is
$3(\delta_{ka}\delta_{lb}+\delta_{kb}\delta_{la})-2\delta_{kl}\delta_{ab}$;
its contraction uses $\operatorname{tr}S=0$. Consequently
$$
 Q^\pm_{ab}=\mp\frac{6\lambda F}{c^2}S_{ab},\qquad
 \Delta Q_{ab}:=Q^+_{ab}-Q^-_{ab}
 =-\frac{12\lambda F}{c^2}S_{ab}\ne0. \tag{13}
$$
In the alternative STF normalization with $x_ax_b-\delta_{ab}r^2/3$, these tensors are divided by three. This distinguishes a nonzero quadratic-weight stress moment from the vanishing $\Sigma_{ij}$.

Use exactly the supplied whole-space decaying field equations
$$
 \nabla^2\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu},\qquad
 \bar h_{\mu\nu}(x)=\frac{4G}{c^4}\int\frac{T_{\mu\nu}(y)}{|x-y|}\,d^3y,
$$
$$
 h_{\mu\nu}=\bar h_{\mu\nu}
 -\tfrac12\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta},\qquad
 \bar h_{\mu\nu}\longrightarrow0\ \text{at infinity}. \tag{14}
$$
Compact conservation supplies the de Donder compatibility by differentiating this convolution and integrating by parts. The smooth compact source has a regular whole-space potential. A difference of allowed solutions is harmonic on all space and decays, hence is zero; an added singular multipole would be an additional source and is excluded.

Define the negative Newtonian lapse potential by
$$
 g_{00}=-1+h_{00}=-1-\frac{2\Phi}{c^2},\qquad
 \Phi(x)=-\frac G{c^2}\int
       \frac{\varepsilon(y)+\operatorname{tr}T(y)}{|x-y|}\,d^3y.
 \tag{15}
$$
For $r>2R$, radiality gives the energy convolution $E/r$ and the bump convolution $F/r$. To see the latter without an expansion assumption, its exterior potential is radial, harmonic and decaying, so it is a constant divided by $r$; its far coefficient is $\int f=F$. The same argument applies to $\varepsilon$.

With two integrations by parts and $\partial_{y_k}|x-y|^{-1}=-\partial_{x_k}|x-y|^{-1}$,
$$
 \int\frac{\operatorname{tr}D(y)}{|x-y|}\,d^3y
 =-S_{kl}\partial_k\partial_l(F/r)
 =-\frac{3F\,S_{kl}n_kn_l}{r^3},\quad n=x/r.
$$
Thus the full exterior lapse potentials are exactly, within the linearized model,
$$
 \Phi_\pm(x)=-\frac{GE}{c^2r}
 \ \pm\frac{3G\lambda F}{c^2r^3}S_{kl}n_kn_l,\qquad r>2R.
 \tag{16}
$$
Their difference is a pure quadrupole. This is not just its asymptotic leading term: no additional exterior lapse multipoles occur for these radial defining functions. Equation (16) also agrees with the convention
$\Phi_{\rm quad}=-GQ_{kl}n_kn_l/(2r^3)$ using (13).

A potential difference alone is insufficient, so fix one curvature contrast. Use the curvature convention
$$
 R^\rho{}_{\sigma\mu\nu}
 =\partial_\mu\Gamma^\rho_{\nu\sigma}
  -\partial_\nu\Gamma^\rho_{\mu\sigma}
  +\Gamma^\rho_{\mu\alpha}\Gamma^\alpha_{\nu\sigma}
  -\Gamma^\rho_{\nu\alpha}\Gamma^\alpha_{\mu\sigma}.
$$
For these static perturbations,
$$
 R^{(1)}_{0i0j}=-\tfrac12\partial_i\partial_jh_{00}
              =\frac1{c^2}\partial_i\partial_j\Phi. \tag{17}
$$
Supply the common exterior receiver location $p=(0,0,L)$, $L=3R$, and the third axis $e_3$. It is outside the support of both complete tensors. Along the positive third axis, $S_{kl}n_kn_l=1$; differentiating with $x_1=x_2=0$ gives
$$
 R^{(1),\pm}_{0303}(p)
 =-\frac{2GE}{c^4L^3}\ \pm\frac{36G\lambda F}{c^4L^5}.
$$
The single finite source-to-source curvature contrast is therefore
$$
 \boxed{\Delta R^{(1)}_{0303}(p)=
       \frac{72G\lambda F}{c^4(3R)^5}>0.} \tag{18}
$$
With the specified fixed $\lambda=1/(8M)$, its numerator coefficient is $9GF/M$.

At this retained order the component is the corresponding orthonormal electric-curvature component for a rest receiver with those supplied axes; corrections to the frame multiply an already first-order curvature and are beyond that order. Equivalently the leading relative-acceleration coefficient for nearby freely falling test bodies initially at rest is
$$
 {\cal K}_\pm=-c^2R^{(1),\pm}_{0303}(p),\qquad
 \Delta{\cal K}=-\frac{72G\lambda F}{c^2(3R)^5}<0,
 \tag{19}
$$
where the radial relative acceleration is ${\cal K}_\pm\xi^3$ to first order in their separation. This is one ideal tidal channel, not an executed apparatus protocol. Linearized Riemann curvature about a flat background is invariant under infinitesimal gauge changes, so the nonzero contrast cannot be removed as a potential-coordinate artifact. The location, orientation, time and separation standards must be held common in comparing the two sources.

Every $T_{\mu\nu}$ has energy-density units, $f$ has energy per length units, $F$ has energy times length squared units, and $\lambda,S,M,C_\varepsilon,C_f$ are dimensionless. Then $E/c^2$ has mass units, $Q$ has mass times length squared units, $\Phi$ has velocity squared units, (18) has inverse-length squared units and (19) has inverse-time squared units. The weak-field ordering is supplied by
$$
 g=\frac{GuR^2}{c^4}\ll1.
$$
All shape constants and the stress-to-density ratio are bounded independently of $g$, so choosing $u,R$ in this regime makes the source fields weak at the retained order. Matter is held at zeroth order, as in the accepted notes. We have not constructed a nonlinear self-gravitating equilibrium, estimated a nonlinear remainder, or established uniform weak-field behavior for arbitrarily large boosts.

The equality of energy density is pointwise in the same supplied background rest coordinates. It is stronger than equality of an energy integral. The remaining information is the tracefree quadratic spatial moment of the stress trace. Compact conservation fixes its unweighted integral but leaves (13) free. A prospective native-to-gravity map that registers only energy density and total boost inertia cannot distinguish this pair and therefore cannot fix the tidal reading (19) in the admitted tensor class. It must supply independent stress/spatial information, or an additional justified constitutive restriction that excludes this ambiguity. This is a scoped nonuniqueness result, not a proof that every native map fails.

Coordinates and support geometry, the energy-density scale $u$, the meaning of time and $c$, the gravitational coupling $G$, and receiver calibration are conventional inputs. No action scale enters this static classical construction; one would need to supply and justify such a scale if connecting it to an oscillator energy assignment. No mapping from the earlier chain fields, no native metric location and no preparation or detector model is derived. State's coherent-inertia task and Classical's mass assays supply no premise to this proof and remain disjoint.

Preparing opposite stress patterns at equal energy density, maintaining a physical source, switching between them, measuring a weak tidal channel and restoring all resources need separate support, work, readout and reset ledgers. Equal static endpoint energy does not imply a costless reversible preparation cycle. The admissibility bound does not prove a material can realize either endpoint, nor does zero flat-background divergence solve its self-gravitating dynamics. No empirical or production claim follows.

The result is a conditional conventional counterexample to sufficiency of energy density plus integrated inertia for this spatial gravitational prediction. The next-use decision is to retain an explicit stress/spatial attachment obligation in any proposed native field-to-source bridge. No further source pair, growth law, material study or experiment is started by this report.

## Scientific review

Energy derived this finite source pair. Relational State independently verified smooth conservation, the explicit stress margin, equal integrated masses, exterior quadrupole and gauge-invariant tidal contrast. Author report SHA-256 9192bbe415f06aa2343f652aa65ca03445786b27d1e682f1e5fade4c4769f809; independent review 839d5cd662cd709119a015fd7151ba23241dea6139702a49608044b2407e9a0d.
