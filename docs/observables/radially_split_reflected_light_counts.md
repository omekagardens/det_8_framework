# Compactness and radius from a radially split reflected-light exposure

The ratio of the two population mean counts uniquely determines $u=2GM/(Rc^2)$ throughout $0\le u<1$. Their common normalization then gives $\rho R^4$, hence the areal radius in units of the density length $\rho^{-1/4}$. Transferring this result to the scalar length $\ell$ requires one more dimensionless number, $\rho\ell^4$, for the registered apparatus. With unknown common counting efficiency the required number is the corresponding effective density times $\ell^4$.

## The region between the light fronts

Use $X=ct$, $x=r/R$ and $F(r)=1-uR/r$. The stipulated exterior, in areal-radius coordinates and signature $(-+++)$, has
$$
 ds^2=-F(r)\,dX^2+F(r)^{-1}\,dr^2+r^2\,d\Omega^2 .
$$
The angular term fixes the meaning of radial ratios. The lapse and radial coefficient cancel in the determinant, giving $dV_4=r^2\sin\vartheta\,dX\,dr\,d\vartheta\,d\varphi$. Along a radial null ray $dX=\pm dr/F(r)$. This uses the Schwarzschild exterior as an input. [Schwarzschild, English translation, Eq. (14)](https://arxiv.org/pdf/physics/9905030v1)

Set the emission coordinate to zero and let $T(r_1,r_2)=\int_{r_1}^{r_2}dr/F(r)$ for $r_1\le r_2$. At the *same* shell $r$, the outgoing front arrives at $X_{\rm out}=T(R,r)$ and the reflected front at $X_{\rm ret}=T(R,2R)+T(r,2R)$. Their separation is
$$
 X_{\rm ret}-X_{\rm out}=2T(r,2R)=2R\,D_u(x),\qquad
 D_u(x)=\int_x^2\frac{t}{t-u}\,dt
       =(2-x)+u\log\frac{2-u}{x-u}.
$$
The factor of two counts both legs from that shell to the reflector. The exposure thickness decreases to zero at $2R$. The count gates are the local front passages. No coordinate time slice or clock reading enters the record.

Put $I_{\rm in}(u)=\int_1^{3/2}x^2D_u(x)\,dx$ and $I_{\rm out}(u)=\int_{3/2}^2x^2D_u(x)\,dx$. Full solid-angle coverage gives independent Poisson counts with means
$$
 (\mu_{\rm in},\mu_{\rm out})
       =8\pi\,\rho R^4\,(I_{\rm in}(u),I_{\rm out}(u)).
 \tag{1}
$$
Indeed the two regions are disjoint up to a zero-four-volume boundary. Both means are strictly positive and finite. The density has dimensions length$^{-4}$ with the coordinate $ct$. An instantaneous three-volume or the launch-to-return duration multiplied by a whole shell volume would describe a different exposure.

## Why one ratio selects a unique compactness

Write $Q(u)=I_{\rm in}(u)/I_{\rm out}(u)$. For $0\le u_1<u_2<1$ the ratio $D_{u_2}(x)/D_{u_1}(x)$, $x<2$, is the weighted mean on $[x,2]$ of
$$
 g(t)=\frac{t-u_1}{t-u_2},\qquad \text{weight } \frac{t}{t-u_1}>0 .
$$
Since $g'(t)=(u_1-u_2)/(t-u_2)^2<0$, raising $x$ deletes values strictly larger than the mean of the remaining interval. Thus the ratio of light-front separations strictly decreases with $x$. Its averages over the inner and outer zones with positive weight $x^2D_{u_1}(x)$ equal $I_{\rm in}(u_2)/I_{\rm in}(u_1)$ and $I_{\rm out}(u_2)/I_{\rm out}(u_1)$. The first is strictly larger. Cross-multiplication proves $Q(u_2)>Q(u_1)$, including at the flat lower endpoint.

Both integrals are continuous for $u<1$. At zero, $D_0=2-x$ and $2x^3/3-x^4/4$ is a primitive of the weighted integrand. As $u\uparrow1$, $D_u(x)$ increases to $2-x-\log(x-1)$ for $x>1$. The endpoint logarithm is integrable despite the divergent inner-station round-trip coordinate time. Monotone convergence gives the following limits.

| Compactness | $I_{\rm in}$ | $I_{\rm out}$ |
| --- | ---: | ---: |
| $u=0$ | $109/192$ | $67/192$ |
| $u\uparrow1$ | $(695+456\log 2)/576$ | $(761-456\log 2)/576$ |

For the last row put $y=x-1$ and integrate the additional term $-(1+y)^2\log y$. A primitive is $-(y+y^2+y^3/3)\log y+y+y^2/2+y^3/9$, with limiting value zero at $y=0$. The two integrals sum to $11/12$ in the flat case and $91/36$ in the limit.

Consequently the sharp population-mean test is positivity and finiteness of both means and
$$
 \boxed{\displaystyle \frac{109}{67}
     \ \le\ \frac{\mu_{\rm in}}{\mu_{\rm out}}
     \ <\ \frac{695+456\log 2}{761-456\log 2}.}
 \tag{2}
$$
The upper endpoint would place the static emitting station on its horizon and is excluded. Under (2), continuity and strict monotonicity give one root $u$. Then
$$
 S=\frac{\mu_{\rm in}+\mu_{\rm out}}
              {8\pi[I_{\rm in}(u)+I_{\rm out}(u)]}
   =\rho R^4,\qquad \frac{R}{\rho^{-1/4}}=S^{1/4}.
 \tag{3}
$$
Sufficiency is constructive. Choose any $R>0$, $\rho=S/R^4$, $M=uRc^2/(2G)$, and put the three stations at the specified radii. These parameters realize both means and their full product Poisson law. A proposed *full law* must also have that independent Poisson form. A single observed integer pair, including one with a zero count, cannot pass or fail (2) as a test on known means. Every nonnegative integer pair has positive probability under every admissible finite parameter pair.

## What deleting the split loses

If the only observation is the total count, its complete law is Poisson with mean $m>0$. For **every** $u\in[0,1)$ choose $S(u)=m/\{8\pi[I_{\rm in}(u)+I_{\rm out}(u)]\}$ and use the construction above. The total law, including the empty-exposure probability, is identical. Both integrals increase strictly with $u$, so these geometries have genuinely different $R\rho^{1/4}$ as well as different compactness. The degeneracy persists even at fixed positive $\rho$ if the absolute radius and mass are allowed to vary together as required by (1).

## Transfer to the scalar and gravity apparatus

With unit efficiency let $\chi=\rho\ell^4$. Given the optical record, the exact transfer is
$$
 \boxed{\displaystyle R/\ell=(S/\chi)^{1/4}.} \tag{4}
$$
The scalar response defines $h=2/\ell^2$. Its accepted relative calibration can determine $j=J_s/(M_0c\ell)$ under the quadratic hypothesis. It supplies no four-volume sampling rate in those units. For an explicit ambiguity, hold the entire optical geometry and point process fixed. For any $\lambda>0$ rescale $\ell\mapsto\lambda\ell$ and $h,k,d,g\mapsto(h,k,d,g)/\lambda^2$ in the accepted scalar model. Its nine means and its spring data agree. With $M_0$ fixed the quadratic conversion gives $J_s\mapsto\lambda J_s$, preserving $j$. The same optical $S$ is compatible with $R/\ell$ divided by $\lambda$. Conversely, (4) gives a unique $R/\ell$ for any one independent calibration of $\chi$. A direct length standard registered in both arms could supply the equivalent information.

For independent, constant thinning with probability $0<\epsilon\le1$ shared across zones, (1) holds with $\rho_{\rm eff}=\epsilon\rho$. The ratio and compactness survive. The identifiable scale is $S_{\rm obs}=\epsilon\rho R^4$. The *true* density radius requires a known efficiency or equivalent latent-rate calibration. For the scalar transfer it suffices to calibrate the single product $\chi_{\rm eff}=\epsilon\rho\ell^4$ under identical conditions. Then $R/\ell=(S_{\rm obs}/\chi_{\rm eff})^{1/4}$. Unknown efficiencies that differ between the two zones enter the ratio itself. An unknown radial intensity profile also changes the weighting in (1). The two-dimensional optical and two-counter results use different sampling assumptions and do not supply these calibrations.

For the gravity-coupling design, identify the optical $R$ with the same areal inner station and $2R$ with the same outer station, in a matched, settled exterior for the specified object/fixture and source setting. Transfer across settings requires independent evidence that the radii remain fixed. The middle split, full solid angle, reflection without delay, empty trials, complete local front gates, negligible station/backreaction and common intensity/efficiency must be registered. The density calibration must refer to the same sampled population and to the scalar preparation defining $\ell$. The recovered $u$ belongs to the measured **total exterior mass in that setting**. The exposure by itself does not separate fixture and source or test their proportionality.

The scalar length, homogeneous invariant Poisson sampler and exterior null propagation each enter from their respective models. No physical identification of DET events with that sampler, empirical precision, or dimensional coupling follows from this calculation.

[Exterior clocks and gravitational coupling](exterior_clocks_and_scalar_gravity_coupling.md) · [Scalar mass term from three sector inertias](scalar_mass_term_from_three_sector_inertias.md)
