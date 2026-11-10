# What a single upper load cell weighs in an accelerating laboratory

Let $F$ be the local force magnitude at the top, $g$ the proper acceleration at the payload, $L$ the tether's proper length, and $h=1+gL/c^2$. The acceleration of the upper contact is $a_{\rm top}=g/h$. Its reading determines the total proper energy of the supported payload and tether:
$$
\boxed{\frac{F}{a_{\rm top}}=\frac{hF}{g}
       =m+\frac{E_{\rm t}}{c^2}},\qquad
E_{\rm t}=\int_0^L\varepsilon(z)\,dz .
$$
Here $m$ is payload rest mass and $E_{\rm t}$ is the tether energy on a stationary proper-length slice. At fixed $F,g,L>0$, the sharp payload range is $0<m\le F/g$. Even the largest admissible payload requires tether energy $FL$.

## Force balance and frame registration

Use the prescribed flat Rindler metric with $N(z)=1+gz/c^2$, $N(0)=1$. A stationary clock has $d\tau=N\,dt$, and a stationary observer has proper acceleration $a(z)=c^2 N'/N=g/N$, directed toward increasing $z$. The top pulls upward on the tether with local force $F$; the tether pulls downward on the contact with equal magnitude. The point payload has only its bottom-end traction to supply the required upward acceleration, so $T(0)=mg$. The other endpoint condition is $T(L)=F$.

In coordinates $(ct,z)$ the mixed line stress-energy components are $S^\mu{}_\nu=\operatorname{diag}(-\varepsilon,-T)$. This uses the local longitudinal pressure $p=-T$ and zero energy flux. In the open tether the longitudinal conservation equation, using $\Gamma^0{}_{0z}=N'/N$, reads
$$
0=\nabla_\mu S^\mu{}_z=-T'+\frac{N'}N(\varepsilon-T),
\qquad
\boxed{(NT)'=N'\varepsilon}.
$$
The time equation holds by stationarity and zero flux. The tension has force units, the same as the proper energy per length ($\mathrm{J/m}=\mathrm{N}$); $N'$ has inverse-length units. Thus both terms in the longitudinal balance have units of force per length.

Since $N'=g/c^2$ is constant, integration and endpoint matching give $hF-mg=(g/c^2)E_{\rm t}$. The lapse-weighted traction $hF$ is the top force referred to the base normalization, with base lapse one. Equivalently the cell uses its local $F$ and local $a_{\rm top}$ in the boxed mass reading. $F/g$ pairs the top reading with the bottom acceleration and is the payload's upper bound.

On a stationary slice $dz$ is proper length. The base-normalized time-translation (Killing) energy of the supported matter is instead
$$
E_K=mc^2+\int_0^L N(z)\varepsilon(z)\,dz .
$$
The contact identity integrates $\varepsilon$ with unit proper-length weight. For instance, in the constant-density family below, $E_K-(mc^2+E_{\rm t})=(h-1)E_{\rm t}/2$; different payloads at the same $F$ give different Killing energies. The load cell and the external agency accelerating it lie outside the supported energy ledger.

## Sharp bounds and all attainable payloads

The energy condition $0\le T\le\varepsilon$ and $N'>0$ give $T'\ge0$. Hence $mg\le T(z)\le F$ and $\varepsilon(z)\ge mg$ throughout. For a given payload,
$$
E_{\rm t}\ge mgL=mc^2(h-1).
$$
Equality requires $\varepsilon=T=mg$ everywhere: the continuous nonnegative excess $\varepsilon-mg$ has zero integral and $mg\le T\le\varepsilon$. That constant profile satisfies conservation and the endpoint conditions with $F=mg$. It is the unique minimizing profile under the stipulated line model, which expressly allows equality of energy density and tension.

To realize each candidate $0<m\le F/g$ for a fixed measured $F$, take a spatially constant line energy and the tension
$$
\varepsilon_0=\frac{hF-mg}{h-1},\qquad
T(z)=\varepsilon_0+\frac{mg-\varepsilon_0}{N(z)} .
$$
Here $\varepsilon_0-mg=h(F-mg)/(h-1)\ge0$, so $T\ge mg>0$ and $\varepsilon_0-T=(\varepsilon_0-mg)/N\ge0$. Since $NT=N\varepsilon_0+mg-\varepsilon_0$, conservation holds exactly. At $N=1$ the tension is $mg$; at $N=h$ it is $F$. Both profiles are finite and smooth on the closed segment. At $m=F/g$ they reduce to the saturated constant solution. Taking positive $m$ arbitrarily close to zero preserves all conditions, so there is no positive lower mass bound. This establishes sufficiency for the whole interval.

For fixed $F,g,L$, the full joint feasible set and its tether-energy projection are
$$
0<m\le F/g,\qquad E_{\rm t}=c^2(hF/g-m),\qquad
E_{\rm t}\in[FL,\ c^2hF/g).
$$
The largest payload and smallest tether energy occur together. The upper tether-energy endpoint would use $m=0$, excluded by the payload premise. At fixed $m$ alone, the same construction allows every energy at or above $mgL$ by taking $F=(g/h)(m+E_{\rm t}/c^2)$.

## What a budget or tare adds

The tether must supply at least $(h-1)/h$ of the total supported proper energy. A certified upper budget $E_{\rm t}\le B$ is compatible with a fixed contact reading only if $B\ge FL$. If it is compatible, it further requires $m\ge hF/g-B/c^2$ together with $0<m\le F/g$; the profiles above make that restriction sharp. When $gL/c^2$ is small the *minimum* tether energy is small relative to the payload rest energy. A small ratio $gL/c^2$ alone supplies no upper bound on the tether's fraction below one.

Inferring the payload requires the tether's proper energy in its loaded state, or an independently verified way of accounting for its change under load. With the same $g,L$, subtracting an empty reading gives
$$
\frac{F_{\rm loaded}-F_{\rm empty}}{a_{\rm top}}
=m+\frac{E_{{\rm t,loaded}}-E_{{\rm t,empty}}}{c^2}.
$$
A tare therefore isolates $m$ if the tether energy is unchanged or the difference is independently corrected. A material implementation must establish the loaded length, strain and stored energy, stable equilibrium, attachment forces and calibrated local force and acceleration scales. An equation of state and a preparation that realize a proposed profile would supply evidence beyond conservation and the energy inequality. Exact saturation is an allowed mathematical limit of the stated material class. Strength relative to line energy is the public background for the assumed inequality. [Brown, *Tensile Strength and the Mining of Black Holes*, v1](https://arxiv.org/abs/1207.3342v1)

## Comparison with the cavity and the closed shell

CL087 sums collision impulses from a pulse at two externally maintained mirrors, with rates defined by local or base clocks. Those impulses occur at different events and are recorded in different instantaneous rest frames. The pulse exchanges momentum and lab-frame energy with the supports. The earlier short-cavity factors of two and one characterize those particular rate sums. Here one stationary contact transmits the continuous stress of a specified tether plus payload, and the tether's own energy enters through local conservation. The observable requires one local steady force measurement and the registered Rindler acceleration.

The closed-shell result instead boosts a complete isolated stationary stress-energy tensor, including its wall stress, to extract inertia from momentum. This tether calculation assumes an externally accelerated boundary in flat spacetime and neglects self-gravity. It establishes a conditional support-force calibration. Active gravitational mass, a DET-native mass scale, elastic dynamics and empirical material performance require additional inputs. [Supported light cavity](two_clocks_on_a_supported_light_cavity.md) · [Complete radiation-shell inertia](closed_radiation_shell_inertia.md)
