# Causal order and scalar length after radial projection

Discarding angular coordinates can turn a causal diamond into a chain. On one open set of projected four-event records, both true orders have positive conditional probability, and the two orders give different scalar responses. A constant transverse area makes radial counts homogeneous while leaving this ambiguity.

Use the spherical light exposure between areal radii $R$ and $2R$, with a homogeneous Poisson intensity $\rho$ per invariant four-volume, unit efficiency and registered radial gates. Write $u=2GM/(Rc^2)$ and $D_u(x)=\int_x^2 t/(t-u)\,dt$. A fixed central direction defines the angular aperture of the sampling region. The optical width and the scalar length concern separate preparations. [Reflected-light exposure](radially_split_reflected_light_counts.md) · [Scalar propagation on four events](scalar_length_with_one_hidden_event.md)

## Projection of the count intensity

Write $X=ct$ and $F(r)=1-uR/r$, $0\le u<1$, in the adopted exterior:
$$
 ds_4^2=-F\,dX^2+F^{-1}dr^2+r^2d\Omega^2,\qquad
 ds_2^2=-F\,dX^2+F^{-1}dr^2.
$$
The four-volume element is $r^2d\Omega\,dX\,dr$, and the radial two-metric has determinant $-1$, hence positive proper-area element $dX\,dr$.

At each $r$ retain the specified angular cap of solid angle $\Omega(r)>0$. For any projected region $E$, its accepted preimage has Poisson mean
$$
 \Lambda_2(E)=\int_E\rho\,r^2\Omega(r)\,dX\,dr.
$$
Disjoint projected regions have disjoint four-dimensional preimages, so the projected counts are independent Poisson on disjoint sets. The coordinate intensity is absolutely continuous; exact coincidences of two projected points have probability zero. Thus the image is a simple Poisson point process with intensity
$$
 \boxed{\lambda_2(r)=\rho r^2\Omega(r)}
$$
per proper area of the orbit metric. No causal-order assertion follows from this mapping.

Since the original $\rho$ is constant, radial homogeneity is equivalent to $r^2\Omega(r)$ being constant almost everywhere in the observed annulus. A fixed solid angle instead produces an $r^2$ intensity profile. For the design in this experiment, let
$$
 {\cal A}_\perp=r^2\Omega(r)=A,\quad
 0<A<4\pi R^2.
$$
It follows that
$$
 \boxed{\rho_2=\rho A>0,\qquad
 [\rho]=L^{-4},\quad[A]=L^2,\quad[\rho_2]=L^{-2}.}         \tag{1}
$$
The aperture restriction ensures a valid non-full cap throughout $R\le r\le2R$. Its physical cross-section is an additional registered transverse quantity, not derived from radial event counts.

The local light fronts remain the gates of the projected exposure. Their radial two-area is $2R^2\int_1^2D_u(x)\,dx$, so its cap count mean is $2\rho A R^2\int_1^2D_u(x)\,dx$. This differs from the full-sphere $8\pi\rho R^4\int x^2D_u(x)\,dx$. One must not reuse the full-angle shell means after silently changing the retained population.

## Actual event causality versus orbit/quotient causality

For any causal curve in the stipulated static exterior,
$$
 ds_2^2=ds_4^2-r^2d\Omega^2\le0.
$$
Future orientation also projects. Hence actual four-dimensional causal precedence implies causal precedence of the projected orbit points.

The converse is not true for the actual event pair. A radial causal path has a same-angle lift, so orbit causality describes the **existence** of causally related representatives on the two spheres (and the centred caps contain a common axis). It does not say that the two randomly sampled angular representatives are related. Projection can add comparisons and change interval interiors. It is not an order embedding.

The following obstruction uses the exact $M=0$ member in the model. It disproves universal order preservation for this family. No stronger all-compactness obstruction is needed or claimed; the intensity formula and one-way causal implication above apply throughout the adopted exterior.

## Exact four-event chain/diamond construction inside the flat exposure

Fix arbitrary $R>0,\rho>0$ and any admitted $A>0$. In Minkowski space the reflected-shell region is
$$
 R<r<2R,\qquad r-R<X<3R-r.
$$
At $r_0=3R/2$ the open time interval is $R/2<X<3R/2$. Let $\vartheta_0>0$ be the angular cap half-width at $r_0$. Choose
$$
 0<\alpha<\min(\vartheta_0/4,1/100),\qquad
 \delta=r_0\sin\alpha>0.
$$
In particular $\delta<3R/200<R/32$. Use the same four projected points in both lifts:
$$
\begin{array}{c|cccc}
 \text{label}&a&b&x&y\\ \hline
 r&r_0&r_0&r_0&r_0\\
 X&3R/4&R-\delta/2&R+\delta/2&5R/4 .
\end{array}                                             \tag{2}
$$
All are strictly inside the optical exposure, and the projected radial order is $a<b<x<y$.

Let ${\bf n}(\theta)=(\sin\theta,0,\cos\theta)$, with ${\bf n}(0)$ the cap axis.

**Chain lift.** Put all four angular positions at ${\bf n}(0)$. Their spatial vectors are equal, while all displayed time differences are positive. Thus all prescribed chain comparisons are strictly timelike.

**Diamond lift.** Put $a,y$ at ${\bf n}(0)$, $b$ at ${\bf n}(\alpha)$, and $x$ at ${\bf n}(-\alpha)$. These directions are strictly inside the cap. The actual Euclidean chord between the middle two events has length
$$
 |r_0{\bf n}(\alpha)-r_0{\bf n}(-\alpha)|
       =2r_0\sin\alpha=2\delta,
$$
whereas their time-coordinate difference is $\delta$. They are strictly spacelike in the full Minkowski spacetime. This uses the actual shortest spatial separation, not a spherical arc or a path constrained to a detector.

Each axis-to-middle distance is
$$
 2r_0\sin(\alpha/2)=\delta/\cos(\alpha/2)<2\delta<R/16.
$$
The smallest endpoint-to-middle time difference is
$R/4-\delta/2>15R/64$. Hence $a$ is strictly timelike before both middle events and both are strictly timelike before $y$; $a<y$ also holds. The actual order is exactly the diamond, with $b,x$ incomparable. The relevant straight segments stay in the annulus for these small angles, but the spacelike middle-pair conclusion holds even when arbitrary physical paths are allowed.

The radial record (2), geometry, aperture, density and known standards are identical. The lifts already exhibit two different actual orders behind the same projected chain. Their common projected chain cannot be declared the actual relation of the diamond events.

## Positive conditional support on a common open record set

The exact values and exact axis directions in (2) are construction centres, not positive-probability point events. The obstruction is strengthened as follows.

All timelike/spacelike inequalities above are strict. Choose sufficiently small open angular neighbourhoods around the four chain-lift directions, and separately around the four diamond-lift directions. The cap is open around each centre, so each angular product neighbourhood has positive product solid angle. Continuity preserves all required pairwise signs.

There is also one common open neighbourhood ${\cal U}$ of the four projected pairs in (2), with four disjoint time-ordered projected boxes, such that:

- every projected tuple remains inside the optical gates and has strict radial chain order;
- the chain angular neighbourhood yields the actual chain for every projected tuple in ${\cal U}$;
- the diamond angular neighbourhood yields the actual diamond for every projected tuple in ${\cal U}$;
- both angular neighbourhoods remain strictly inside the caps as the radii vary slightly.

The last statement follows from the continuous positive cap width for $\Omega(r)=A/r^2$. The simultaneous neighbourhood exists because only finitely many strict inequalities and interior conditions must be retained.

Conditional on distinct projected points, angular marks of the stipulated process are independent with normalized measure $d\Omega/\Omega(r_i)$ in each cap. Thus for almost every projected tuple in ${\cal U}$, both actual-order possibilities have positive conditional probability. There is no appeal to the probability of one exact real-vector record.

For an unconditional check, the flat projected exposure has finite area $R^2$ and count mean $\rho A R^2>0$. Requiring one point in each of the four small boxes and no other retained point in the exposure has strictly positive Poisson probability. Conditional angular neighbourhoods of either type then also have positive probability. In fact the entire remaining projected record is empty in this positive-probability control, so observing more projected events cannot resolve it. One may additionally require no sampled points in the complementary angular region of the finite full-shell exposure: that disjoint Poisson region has a positive empty probability. Thus the witness can have exactly four sampled events in the whole exposure, not merely four accepted projections.

Consequently no function of the complete projected point record can return the actual four-event chain/diamond relation with probability one throughout the model. On the common positive-measure record set its conditional order is not deterministic. Private randomness cannot make both alternatives correct with certainty. Narrowing a positive cap can reduce some errors but does not provide exact universal order recovery: the construction chooses a smaller positive $\delta$ for every positive cap.

This is an ambiguity within one fixed sampler/geometry, not a change of the native preparation probabilities. The two abstract order types coincide with the scalar's candidates; that coincidence does not make the projected Poisson population their independently specified finite source preparation.

## The actual scalar propagator changes when projection adds a relation

The accepted scalar acts on the full four-event order, including hidden $x$, with
$$
 N=2L_1-4L_2+2L_3,\quad h=2/\ell^2>0,\quad
 G(s_m)=[t_mI-hN]^{-1},\quad
 t_m=s_m+d+h,\quad s_m>0,\ d\ge0.
$$
In target-row/source-column convention the outer response is
$$
 (G_D)_{ya}=2h/t_m^2+8h^2/t_m^3,
$$
$$
 (G_C)_{ya}=2h/t_m^2-16h^2/t_m^3+8h^3/t_m^4.
$$
Therefore at the same scalar parameters and unit impulse,
$$
 \boxed{(G_D-G_C)_{ya}
       =\frac{8h^2(3t_m-h)}{t_m^4}>0.}                   \tag{3}
$$
A common positive gain preserves this difference. Treating the projected chain as the actual order of the diamond lift thus changes a specified observable, not merely its labels. Hidden $x$ cannot be deleted when counting the intervals.

This does not invalidate the accepted scalar inverse on its correctly registered preparation. It shows that radial projection does not supply that preparation or its full-order operator. The corrected averaging identities for the special chain/diamond family also do not replace each actual order by the projected chain: such averaging requires the actual mixture and retains its full operator information.

One could deliberately define a new radial quotient order and a field law on that order. That is a distinct reduced model requiring its own physical propagation/access argument. It cannot inherit actual point-event causality or the scalar apparatus calibration merely by relabelling projected records.

## Zero-width fibre and possible order-access premises

A single exact angular direction has zero solid angle. In any finite exposure of the continuous four-volume Poisson sampler, its intensity measure is zero, so almost surely no sampled events lie on that exact radial fibre. Conditioning on exact alignment is not a positive-support preparation of four events.

At fixed density/exposure, shrinking the cap to zero also sends the mean retained count to zero. Repeated exposures, increased density or a separately created line detector/source would supply new preparation/rate/cost assumptions; they are not a positive-intensity exact radial marginal of this given sampler. No quantitative approximation or cost bound is established here.

Actual-order access could instead be supplied independently: retain sufficient angular/point information with a justified full-spacetime causal calculation, directly register the pairwise causal relation, or prepare an independently specified genuinely radial process. In the flat construction, the angles together with times and radii determine the chord distances. For a nonflat extension, the full exterior causal model and relevant path/domain information would have to justify the analogous inference. Physical paths cannot silently be constrained to a cap or one ray.

Even with actual chain/diamond order supplied, the scalar source's mixture/marks, labelled drives/readout, gain/offset convention, hidden-event participation and propagation law remain independent premises. A positive-support Poisson pattern is not a derivation of the native numerical mark law or the accepted selected scalar ensemble.

## Density ratios, transverse area and the remaining scalar standard

The two density-length conventions obey
$$
 \ell_4=\rho^{-1/4},\qquad
 \ell_2=\rho_2^{-1/2}=(\rho A)^{-1/2}
                 =\ell_4^2/\sqrt A.
$$
Neither is automatically the scalar parameter $\ell$. Homogeneous counting establishes (1), not $h=2\rho_2$ or $\ell=\ell_2$.

For a potential bridge define two dimensionless calibrations
$$
 \beta=\rho_2\ell^2,\qquad a_\perp=A/\ell^2.
$$
Then
$$
 \boxed{\chi=\rho\ell^4=\beta/a_\perp.}                  \tag{4}
$$
If both quantities are independently justified for the same population, exposure efficiency and scalar preparation, the accepted shell $S=\rho R^4$ gives
$$
 R/\ell=(S\,a_\perp/\beta)^{1/4}.
$$
They need not be two independent new calibrations when the aperture already registers $q_\perp=A/R^2=\Omega(R)$. In that case
$$
 \beta=\frac{S q_\perp}{(R/\ell)^2},\qquad
 \boxed{R/\ell=\sqrt{S q_\perp/\beta},\qquad
 \chi=\frac{\beta^2}{S q_\perp^2}.}                 \tag{5}
$$
Thus one independently calibrated scalar-density normalization $\beta$, together with the registered angular aperture and matched shell record, suffices for the length conversion; an additional independent $A/\ell^2$ is not required in that case. Simply asserting $\ell=\rho_2^{-1/2}$ sets $\beta=1$ as a new physical normalization premise, not a consequence of homogeneous counts. If the transverse ratio is unregistered, it or an equivalent common area/length standard must also be supplied. A known dimensional $A$ is an external transverse reference only to the extent calibrated; it does not by itself identify scalar propagation or the parameter $\ell$. Choosing $A=\ell^2$ would itself spend a scalar-to-area calibration.

With a matched unknown constant efficiency $\epsilon$, the same formulas use $\rho_{\rm eff}=\epsilon\rho$, $\rho_{2,\rm eff}=\epsilon\rho A$, and $\beta_{\rm eff}$. Matching efficiencies/populations between full-shell, aperture and scalar calibrations is required; arbitrary different thinning cannot be cancelled by assuming the same symbol.

There is an explicit remaining scalar scale freedom even if actual order information were restored. Hold the entire sampler, optical geometry, cap $A$, projected record and spring preparations fixed. In the accepted relative scalar model,
$$
 \ell\mapsto\lambda\ell,\qquad
 (h,k,d,g)\mapsto(h,k,d,g)/\lambda^2,\quad\lambda>0
$$
preserves all nine scalar means and the complete spring record. Under the adopted quadratic interpretation $J_s\mapsto\lambda J_s$, keeping $J_s/(M_0c\ell)$ fixed. Neither radial counts nor their causal projection responds to this independent scalar rescaling. Yet $R/\ell$ changes by $1/\lambda$ and $\rho\ell^4$ by $\lambda^4$. An external density/area-to-scalar relation would exclude this freedom; none is given.

The exterior-clock result also retains its independent source-response calibration and configuration registration. This projection result does not remove that separate limitation even if a radius in scalar units is eventually supplied.

[Scalar response in the three registered sectors](scalar_mass_term_from_three_sector_inertias.md) · [Exterior clock and mass registration](exterior_clocks_and_scalar_gravity_coupling.md)
