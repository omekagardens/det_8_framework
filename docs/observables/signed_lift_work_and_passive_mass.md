# When signed lifting work excludes a common passive-to-inertial mass ratio

Independently reviewed conditional result, 9 November 2026.

**Result.** Each signed outward and return reading gives a closed interval for the conservative work on that load and holder. The blank and both loaded rows in a field must use the same holder. With this constraint, the two fields give an exact test for arbitrary positive passive coefficients and a second exact test for one proportionality slope. There are realizable records for which the proportionality test passes in each field separately and fails when the fields are combined. Allowing field-specific clock gain permits a proportional world with exactly the same complete record.

## 1. Nine settings and their physical premises

Use the registered whole-carrier sectors $i=0,1,2$ prepared at $\delta_{00},\delta_{10},\delta_{11}$, respectively. Registration fixes the load identity and its coefficients across settings, including the two internal states of sector 1. Write $h=(a,b_1,b_2)$ for the ideal $a\in\{E,F\}$ and the two retained bits. Its eight probabilities are
$$
 p_i(h)=\frac{q_a}{4}\left(1+\frac{\eta_a}{2}{\bf1}_{i=1}\right),
 \qquad(q_E,\eta_E)=(2/3,1/8448),\quad(q_F,\eta_F)=(1/3,-1/4224).
$$
They sum to one because $\sum_a q_a=1$ and $\sum_a q_a\eta_a=0$. Put $S_1=\{\emptyset,0,1\}$, $S_2=\{\emptyset,1,2\}$. Require the following full population law, with point masses on the readings. Each of the nine individual settings has weight $1/9$.

| Setting | Retained history | Joint mass including the setting | Reading at every such history |
| --- | --- | --- | --- |
| Spring $i\ell=01,02,12$ | $h,h'$ of independently prepared copies | $p_i(h)p_\ell(h')/9$ | Signed ratio $y_{i\ell}$ |
| Lift in $j$, $i\in S_j\setminus\{\emptyset\}$ | $h$ | $p_i(h)/9$ | $(z_j,w^+_{ij},w^-_{ij})$, in this order |
| Lift in $j$, empty | Distinguished empty token | $1/9$ | $(z_j,w^+_{\emptyset j},w^-_{\emptyset j})$ |

All readings are finite. For any Borel reading event multiply the given mass by the indicator that the entire indicated tuple belongs to it. All 192 spring, 32 loaded and two blank cells have failure flag zero. All other outcomes, including failures, have zero probability. No success conditioning enters. The field clock reading must repeat on every load and blank at that field with $z_j>0$.

Use the common rest-release spring, stiffness $K>0$, tick $T>0$, extension $0<D<L$, and assured open first lobe. Require $-1<y_{i\ell}<1$, put $d_{i\ell}=(\arccos y_{i\ell})^2=d_{\ell i}$, and for distinct $i,\ell,m$ require
$$
 u_i=(d_{i\ell}+d_{im}-d_{\ell m})/2>0.
$$
These checks recover all three dimensionless $u_i$. Their pair sums are exactly the observed squared phases, so $M_i=C/u_i$, $C=KT^2$, realizes all the spring readings using one scale.

In each stable, weak external field the lower-to-upper leg and the held-clock transfer have matched endpoints. The supplied clock law is $z_j=g_c\Delta\Phi_j/c^2$, with $\Delta\Phi_j>0$, known $c>0$, one finite positive clock gain and established zeros. The supplied load force $-P_i\nabla\Phi_j$ gives a rise $P_i\Delta\Phi_j$ with $P_i>0$ and $P_\emptyset=0$. A conservative holder rise $H_j$ of either sign is common to all its loads and its blank. The energy ledger assumes rest at each endpoint, recovery of the assembly's mechanical and internal state after the return, negligible backreaction, stationary supports and zero displacement during dwells. Preparation, installation and controller boundaries supply no hidden moving-leg work. The only unrecovered moving-leg energy goes into a passive sink with independent finite nonnegative losses on each leg. One separately zeroed work store with gain $g_w>0$ records energy **delivered** with its sign, including energy returned to the store. The supplied initial level covers the turning and final levels. The lift schedule supplies no calibrated duration. These assumptions and the weak-field clock law define the conditional tests below.

## 2. Eliminate the losses and the two holders

Define measured endpoints and scaled unknowns
$$
 L_{ij}=-w^-_{ij},\quad U_{ij}=w^+_{ij},\quad
 b_j=g_w H_j,\quad \alpha=\frac{g_wc^2}{g_c},\quad x_i=\alpha P_i,\quad x_\emptyset=0 .
$$
The conservative rise in displayed work units is $V_{ij}=b_j+z_j x_i$. The two signed balances are equivalent to the closed bracket
$$
 L_{ij}\le V_{ij}\le U_{ij},\qquad
 g_w D^+_{ij}=U_{ij}-V_{ij},\qquad g_w D^-_{ij}=V_{ij}-L_{ij}.             \tag{1}
$$
Require $L_{ij}\le U_{ij}$ on all six rows including both blanks. Its width $w^+_{ij}+w^-_{ij}$ identifies the total displayed loss. At zero width both losses vanish and the conservative rise is fixed. At just one endpoint the corresponding loss vanishes. With initial physical store energy $E_0$, the turning and final levels are $E_0-w^+_{ij}/g_w$ and $E_0-(w^+_{ij}+w^-_{ij})/g_w$. These must be supported by the supplied store. The sink retains the cycle loss, while the net conservative change of the assembly is zero. A positive cycle sum alone says nothing about its allocation between the legs.

**Unrestricted positive coefficients.** Denote the terminal sector in each field by $r_1=0,\ r_2=2$, and write $t=x_1$ for the coefficient shared between fields. In each field demand $L_{\emptyset j}<U_{r_j j}$. Compute the following entirely observed interval for $t$, intersecting both field constraints:
$$
 {\cal T}=(0,\infty)\ \cap\
 \bigcap_{j=1}^2\left(
 \left[\frac{L_{1j}-U_{\emptyset j}}{z_j},
       \frac{U_{1j}-L_{\emptyset j}}{z_j}\right]
 \cap\left(\frac{L_{1j}-U_{r_j j}}{z_j},\infty\right)\right).              \tag{2}
$$
The unrestricted model fits exactly when the preliminary checks pass, the two strict blank-to-terminal inequalities hold and (2) is nonempty. This is a finite scalar test. Take the smaller of the two finite upper endpoints. It must meet both closed lower bounds, exceed both open lower bounds and be strictly positive. In that case this upper endpoint itself is one possible $t$.

To see the elimination, for fixed $t$ the blank and bridge require one common $b_j$ in
$[L_{\emptyset j},U_{\emptyset j}]\cap[L_{1j}-z_jt,U_{1j}-z_jt]$.
Given the nonnegative bracket widths, its nonemptiness is precisely the closed bracket in (2). The terminal row permits a positive $x_{r_j}$ exactly when an allowed $b_j$ lies strictly below $U_{r_j j}$. Choose the smallest possible holder $b_j=\max(L_{\emptyset j},L_{1j}-z_jt)$. The strict blank-to-terminal inequality and the open lower bound in (2) say exactly that this choice works. Now $x_{r_j}=(U_{r_j j}-b_j)/z_j>0$ realizes the upper endpoint of the terminal bracket. These two terminal coefficients are independent because each occurs in only one field. This proves necessity, constructs a witness, and covers positive singletons in (2) as well as the excluded zero.

For either test in this report, the reconstructed displayed shifts and coefficients lift to physical parameters. Use common positive gains, $\Delta\Phi_j=c^2 z_j/g_c,\ H_j=b_j/g_w,\ P_i=x_i/\alpha$ and (1). Choose $C>0$ consistent with the spring scale. With unspecified clock gain one can take a sufficiently large common finite $g_c$ to make both gaps weak, using stationary linear potentials over the two finite lift paths. Supplied calibrations or store limits must be respected wherever fixed. With the registered carriers and probabilities of §1 this reconstructs each signed leg, both repeated clocks, blanks and all spring and native records.

## 3. Exact positive proportionality slope

Set $a_i=1/u_i$ for loaded sectors, $a_\emptyset=0$. If $P_i=kM_i$, then $x_i=s a_i$ with one $s=\alpha k C>0$. For each field and every ordered pair $i,\ell\in S_j$ form
$$
 A_{i\ell j}=z_j(a_\ell-a_i),\qquad B_{i\ell j}=U_{\ell j}-L_{ij}.
$$
Pairs with $A=0$ require $B\ge0$, including distinct sectors with equal inertia. Let $s_{\rm lo}=\max_{A<0}(B/A)$ and $s_{\rm hi}=\min_{A>0}(B/A)$ across both fields. Blanks and positive loads ensure both types of pair occur. Subject to the preliminary checks and every zero-coefficient check, the exact set is
$$
                     [s_{\rm lo},s_{\rm hi}]\ \cap\ (0,\infty).             \tag{3}
$$
Thus require $s_{\rm hi}>0$ and $s_{\rm lo}\le s_{\rm hi}$. A positive singleton is attained, even on reversible rows. An upper endpoint zero fails. For a single field the same calculation restricted to its rows gives its local set. With a common transfer the joint set is their intersection.

Indeed a holder for a proposed $s$ must lie in every $[L_{ij}-z_j a_i s,U_{ij}-z_j a_i s]$ in its field. Such an intersection is nonempty exactly when each lower endpoint is at most every upper endpoint, or $A_{i\ell j}s\le B_{i\ell j}$. Splitting by the sign of $A$ gives (3). Conversely take $b_j=\max_{i\in S_j}(L_{ij}-z_j a_i s)$, reconstruct the losses by (1) and set $k=s/(\alpha C)$. This uses one holder per field, including the blank, and reproduces the entire law. If (2) fits while (3) is empty, the unrestricted model supplies a world for which every proportional interpretation with shared gains is excluded. An impossible unrestricted record instead challenges the whole experiment model.

## 4. A crossed rejection and an identical-record clock control

Fix positive finite $C,P_*,g_w,g_c$. Take $M_i=C$ so $u_i=1$, and choose $K=C/T^2$ for the common tick. All three spring readings are $\cos\sqrt2$ on the first lobe. Choose a positive potential gap $\phi$, and use units $W=g_wP_*\phi$ for displayed work and $Z=g_c\phi/c^2$ for displayed clock transfer. The complete six lift rows are

| Field | Load | $z_j/Z$ | $w^+/W$ | $w^-/W$ | $[L,U]/W$ |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | empty | 1 | 1 | −1 | [1,1] |
| 1 | 0 | 1 | 2 | −2 | [2,2] |
| 1 | 1 | 1 | 3 | −2 | [2,3] |
| 2 | empty | 1 | −1 | 1 | [−1,−1] |
| 2 | 1 | 1 | 1 | 0 | [0,1] |
| 2 | 2 | 1 | 1 | −1 | [1,1] |

Use the histories, setting probabilities, empties and failure cells of §1 in both worlds. The blanks fix $b_1=W,\ b_2=-W$. The terminal reversible rows then force $x_0=W/Z,\ x_2=2W/Z$ under shared gains. Both bridge brackets admit $x_1\in[W/Z,2W/Z]$. Field 1 alone allows exactly the proportional slope $W/Z$, attained at the lower bridge endpoint. Field 2 alone allows exactly $2W/Z$, attained at the upper bridge endpoint. Since the two numbers differ, no common slope fits all nine settings.

**World with shared clock gain.** Use $\Delta\Phi_1=\Delta\Phi_2=\phi$ and passive masses $P=(P_*,3P_*/2,2P_*)$. The displayed conservative rises are the unique blank and terminal entries and $5W/2,W/2$ on the two bridge rows. All four sharp rows have no loss. Each bridge deposits $W/(2g_w)$ on each leg. Substitution in (1) gives every raw entry in the table. These equal inertias and unequal passive coefficients realize the full record in the unrestricted model.

**World with proportional masses.** Keep all inertias, histories, spring readings, initial store, work gain, holders, clock endpoints and row labels. Let $P=(P_*,P_*,P_*)$ so $k=P_*/C$. Take the latent gaps $(\phi,2\phi)$ and clock gains $(g_c,g_c/2)$. Every lift, including the second blank, again records $Z$. The terminal conservative rises and both blank rises are exactly as before. The bridge rises become $2W,W$. On the field-1 bridge the outward and return losses are $(W/g_w,0)$. On the field-2 bridge they are $(0,W/g_w)$. All four sharp rows still have zero loss. These substitutions give the same **signed** entries, including the negative outward reading on the second blank and the zero return reading on the second bridge. The latent split of the loss may differ as allowed by the original ledger. The displayed level after each leg and the total heat per cycle agree in the two worlds. The failure flag and every conditional point mass in §1 therefore agree.

For example use a common starting store energy $4W/g_w$. Every turning and final level is positive. At the turning point the conservative system and the sink can retain different shares between worlds. After return the recoverable assembly is restored, the store has lost exactly the sink gain, and a reversible blank has zero net transfer. For any $\varepsilon>0$ choose $0<\phi<\varepsilon c^2/2$, using stationary linear potentials starting at zero on each registered path. Both worlds then have $|\Phi|/c^2<\varepsilon$ along the lifted paths, with positive clock readings, finite signed work readings and the same strict joint exclusion in the shared-gain model. In each world the work gain is common to both fields and all three cycles within a field use the same clock gain.

## 5. What has a scale

The full ideal records identify $u_i$, $M_i/M_\ell=u_\ell/u_i$, $z_2/z_1=\Delta\Phi_2/\Delta\Phi_1$ under common clock transfer, and each displayed cycle loss. The signed brackets constrain holder and load contributions jointly. Equation (2) gives the exact projection for the shared sector coefficient and (3) gives the exact conditional proportionality slope set. Individual conservative rises, one-leg losses and passive masses can have intervals of solutions. Sharp rows and positive singleton slopes can collapse particular intervals.

Changing the common display units $w\mapsto \beta w,\ z\mapsto\gamma z$, with $\beta,\gamma>0$, multiplies holder shifts by $\beta$ and every fitted $x_i,s$ by $\beta/\gamma$. Feasibility and rejection are invariant. At fixed raw data one can also change latent calibrations where they are free. Replacing $(g_w,g_c,C)$ by $(\beta g_w,\gamma g_c,\lambda C)$, dividing $H,D^\pm$ by $\beta$ and the gaps by $\gamma$, multiplying $P_i$ by $\gamma/\beta$ and $M_i,K$ by $\lambda$ preserves the readings within the stated physical domain and capacity of the store. The value of $k$ in a proportional realization changes by $\gamma/(\beta\lambda)$. This freedom already exists through $C$ alone if the gains are independently fixed.

For an attained slope $s$, a numerical $k=s\,g_c/(g_w c^2 C)$ requires external calibration of the combined scale $g_wc^2 C/g_c$ or its factors. Even exact calibration leaves any width in (3). Comparing a displayed work $w$ to $M_i c^2$ uses $u_i w/(g_w C c^2)$ and hence the work-to-inertial scale $g_w C c^2$. Such a comparison supplies no rest-energy conversion law. The argument uses a stipulated passive force, calibrated signed energy access and matched held clocks. The native histories supply the probability weights. These records alone determine neither an active source mass, a freefall observation, nor a DET-native energy unit.

## Reviewed sources

- [Testing proportionality of active and inertial mass across three carrier sectors](registered_active_and_inertial_mass.md)
- [What paired clock and motion records identify about probe response](paired_probe_response_and_acceleration_gain.md)
- [Finite conservation, additive quantities and record access](finite_conservation_and_record_access.md)
- [Native birth kernels with a supplied canonical phase action](native_phase_action_interface.md)
- [Can a finite exterior clock array determine total active mass?](finite_exterior_clocks_and_total_mass.md)

The scientific report (SHA-256 98061f7881095ec37e54bc3250855ad8c70b34be6e6544580884a20a018227d8) passed independent review (SHA-256 a2ae7e8c785a4319d0dd438e0f1b6b303ec7500a48db15f115df619a93259588) on 9 November 2026.
