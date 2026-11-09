# Can the same three carriers have proportional passive and active gravitational coefficients?

Independently reviewed conditional result, 9 November 2026.

**Result.** On the equal-axis subclass of the twelve-clock experiment, the complete registered clock and lift laws admit a common positive $P_i/A_i$ exactly when the finite linear inequalities in §3 have a solution. Their strict inequalities matter because source mass on the boundary of the ball is excluded. In the example, the lift records force $P_2/P_0=2$. One realizable clock record excludes $A_2/A_0=2$ for every allowed source shape. A second admits that ratio even though the records independently exclude both active and passive proportionality to the measured inertias.

## 1. Physical meaning of the ratio

Let $A_i$ be the total active source mass of carrier $i$, $P_i$ its passive response to a uniform external potential gradient, and $M_i$ its spring inertia. To give the first two coefficients a pair-force interpretation, supply all of the following. The same physical carrier types retain their coefficients when moved from the registered rigs to the pair configuration. Their supports are small relative to their separation $R$. Use a common spatial frame and positive Newton coupling $G$ in both directions. The leading field from each separated source is its active monopole. Across the other body this field may be treated to leading order as a uniform external gradient with the response $-P\nabla\Phi$ measured by the lift attachment. The leading pair terms can be isolated from external forces and higher-order effects.

With $n$ pointing from $i$ to $j$, the leading force on $j$ from $i$ is $-G A_i P_j n/R^2$. The force on $i$ from $j$ is $+G A_j P_i n/R^2$. Equal and opposite **leading coefficients** for each pair are therefore equivalent to $A_iP_j=A_jP_i$ for all pairs. Positivity makes this equivalent to one common $P_i/A_i>0$. The two experiments measure neither pair recoil nor the momentum of an isolated system. They supply no exact finite-separation force law for arbitrary profiles. The decision below tests the coefficient relation under the stated transfer of the active field and passive force laws.

## 2. Which records may be combined

Choose protocol independently with probability $1/2$ each. On fresh equivalently prepared copies retain its label, setting, full native history or histories, signed point readings and failure flag. Use sectors $0,1,2$ prepared at $\delta_{00},\delta_{10},\delta_{11}$, with both internal states of sector 1 carrying its same coefficients. For $h=(a_h,b_1,b_2)$ with two recorded bits, use
$$
 p_i(h)=\frac{q_{a_h}}4(1+\eta_{a_h}{\bf1}_{i=1}/2),\qquad
 (q_E,\eta_E)=(2/3,1/8448),\quad(q_F,\eta_F)=(1/3,-1/4224).
$$
The eight cells for each load sum to one. The table gives **unconditional** masses, including protocol choice. Physical readings are deterministic within a setting across its histories. For a Borel event multiply the mass by the indicator that the whole stated reading belongs to it.

| Protocol and setting | Complete native record | Joint mass | Reading |
| --- | --- | --- | --- |
| Twelve clocks, spring $i\ell=01,02,12$ | Independent $h,h'$ | $p_i(h)p_\ell(h')/12$ | $y_{i\ell}$ |
| Twelve clocks, source $i=0,1,2$ | $h$ | $p_i(h)/12$ | Ordered six-vector $\Delta_i$ |
| Signed lift, spring $i\ell=01,02,12$ | Independent $h,h'$ | $p_i(h)p_\ell(h')/18$ | Same $y_{i\ell}$ |
| Signed lift, field 1 with 0 or 1, field 2 with 1 or 2 | $h$ | $p_i(h)/18$ | $(z_j,w^+_{ij},w^-_{ij})$ |
| Signed lift, empty holder once in each field | Empty token | $1/18$ | $(z_j,w^+_{\emptyset j},w^-_{\emptyset j})$ |

There are $192+24$ cells in the first protocol and $192+32+2$ in the second. All readings must be finite. All listed cells have failure flag zero. All other outcomes have zero probability. The protocols retain their respective conditional setting weights $1/6$ and $1/9$. This disjoint mixture requires no joint value for two histories on unperformed alternative trials.

The common spring, stiffness $K>0$, tick $T>0$, registered release from rest at $0<D<L$, and strict first lobe must transfer between protocols. Require all three corresponding raw readings to agree, $-1<y_{i\ell}<1$, and form $d_{i\ell}=(\arccos y_{i\ell})^2$. For each distinct triple $i,\ell,m$ require $u_i=(d_{i\ell}+d_{im}-d_{\ell m})/2>0$ with symmetric pair indices. Then $M_i=C/u_i$, $C=KT^2>0$, reproduces both spring branches. Ratios of these inertias will serve as a separate comparison.

**Active source.** Keep the calibrated $a,G,c,g_s>0$, common axes and origin, held positions $2an,4an$ for the six signed axis directions, registered signs and instrumental zeros. Each source is positive, finite atomic, inversion-symmetric and strictly inside $|y|<a$. Each $\Delta_i(n)$ is outer minus inner, with normalized mass-unit reading $d_i(n)=ac^2\Delta_i(n)/(g_sG)$. Require the three opposed half-differences to agree across sectors, giving $o_j$ and the single affine background gradient $B_j=Go_j/(2a^2)$. Within each sector the three half-sums must all equal some $s_i>0$. An unequal-axis record falls outside this exact test. The constant potential cancels. With the accepted kernel extrema $0<\kappa_-<1/4<\kappa_+<2\kappa_-$, the exact active set for the fixed six-vector is
$$
             l_i<A_i<h_i,\qquad l_i=s_i/\kappa_+,\quad h_i=s_i/\kappa_- .   \tag{1}
$$
Here $\kappa_\pm$ are the dimensionless extrema given in §3 of the accepted twelve-clock theorem. Its §4 constructs the profile for every interior total using finite sign-and-permutation orbits inside the ball. Each of the six raw components is preserved at the observed background. The three sector choices are independent under the registered model.

Retain the active theorem's local weak-field and calibration premises. For instance at $U_0=0$ along the sampled exterior segments, a sufficient uniform bound on $|\Phi_i|/c^2$ is $[4a|B|+G\max_i h_i/a]/c^2$, since every source point is at distance at least $a$. Equation (1) is exact for the retained-order coefficient law. A separately imposed tighter physical tolerance on admissible profiles would need its own verification before applying the full interval. Both examples below satisfy any prescribed positive local amplitude tolerance by common scaling.

**Passive load.** In field $j=1,2$ write $S_1=\{\emptyset,0,1\}$, $S_2=\{\emptyset,1,2\}$. All three rows of field $j$ must give the same $z_j=g_c\Delta\Phi_j/c^2>0$, measured at the lift endpoints. Require the same positive $g_c,g_w$ across the two lift fields for their respective clock and work displays, known signs and verified zeros. Uniform weak stationary external fields, rest at all endpoints, stable fixtures, negligible backreaction, preparation and controller boundaries, and the absence of hidden moving-leg work are supplied. The assembly returns to its original configuration and recoverable internal state. There is one conservative holder rise $H_j$ per field and independent losses $D^\pm_{ij}\ge0$ into a one-way sink. The signed work store and sink retain their final changes. No lift-duration calibration is required by the work equation.

Use the accepted lift report's displayed coefficients $x_i=\alpha P_i$, $\alpha=g_w c^2/g_c>0$, $x_\emptyset=0$, and $L_{ij}=-w^-_{ij},\ U_{ij}=w^+_{ij}$. Require $L_{ij}\le U_{ij}$ including blanks. A conservative displayed rise $b_j+z_jx_i$, $b_j=g_w H_j$, must lie in that closed bracket. Check the supplied initial store can support its turning and final levels $E_0-w^+_{ij}/g_w$ and $E_0-(w^+_{ij}+w^-_{ij})/g_w$. A zero-width bracket is reversible. The external lift fields need not come from the three source profiles. Cross-protocol transfer requires a common identity, persistence of the whole package and compatibility of its three coefficients. Repeated preparation labels alone cannot establish this. Nothing here requires the exterior clock gain $g_s$ to equal the lift clock gain $g_c$.

## 3. A finite test on the observed records

Use (1) and the lift brackets to build a linear system in just $x_0,x_1,x_2$. For unrestricted joint feasibility require $x_i>0$ and
$$
        z_j(x_\ell-x_i)\ \le\ U_{\ell j}-L_{ij}
          \qquad(j=1,2,\quad i,\ell\in S_j),\qquad x_\emptyset=0.            \tag{2}
$$
For a common positive $P/A$ add the nine **strict** linear inequalities
$$
                          l_\ell x_i<h_i x_\ell
                     \qquad (i,\ell\in\{0,1,2\}).                           \tag{3}
$$
All coefficients come from the data and fixed calibrations. Equations (2)–(3) together with the preliminary record checks are necessary and sufficient in the stated domain. Failure of the unrestricted checks means the combined observation model fails. If those pass and the strict system fails, the joint law rules out a reciprocal leading coefficient assignment.

To derive (2), eliminate $b_j$ by comparing every lower endpoint $L_{ij}-z_jx_i$ with every upper endpoint $U_{\ell j}-z_jx_\ell$ in its field. These pairwise comparisons are exactly (2). They include blanks and require one holder for all rows. To derive (3), let $r=\alpha(P_i/A_i)$ be common. Then $A_i=x_i/r$, so (1) is equivalent to
$$
               \max_i x_i/h_i < r < \min_i x_i/l_i .                        \tag{4}
$$
Positive $x_i,l_i,h_i$ permit cross multiplication. Existence of $r$ is precisely (3). Replacing strict comparisons with closed ones would count sources at limiting masses which no permitted interior profile can realize.

For a finite arithmetic decision one may eliminate the three variables in turn. Keep zero-coefficient rows. Divide each remaining row into a lower or upper bound on the variable by its signed coefficient. Compare every lower bound with every upper bound, strictly whenever either bound was strict. Retain the resulting rows in the other variables. A singleton with two closed ends is permitted. A singleton with an open end fails. One-sided families require no opposing comparison. After the last variable, check the resulting constant inequalities. On back-substitution choose a point between distinct finite bounds, the common value for a permitted singleton, or a finite point strictly inside a one-sided range. Each step is exact because every retained family is finite. This gives a decision and witness without a search over source shapes or a numerical tolerance.

**Realization.** For a solution $x$ take $b_j=\max_{i\in S_j}(L_{ij}-z_jx_i)$, $\Delta\Phi_j=c^2z_j/g_c$, $P_i=x_i/\alpha$, $H_j=b_j/g_w$. For $V_{ij}=b_j+z_jx_i$ set $D^+_{ij}=(U_{ij}-V_{ij})/g_w,\ D^-_{ij}=(V_{ij}-L_{ij})/g_w$. Equation (2) makes both nonnegative and reconstructs the two signed readings on every row. The sink gains the energy lost by the store over the cycle. Use the given weak, uniform fields or, in a coefficient-model realization, stationary linear potentials across the paths with gains compatible with the declared domain. For unrestricted feasibility choose any $A_i$ strictly within (1). For reciprocity choose the midpoint of (4) and set $A_i=x_i/r$. Apply the accepted interior-orbit construction once per sector to give a fixed source profile for its complete observed vector. Keep that same profile, $P_i$ and $M_i$ for every copy of that sector in the realized world. The spring and native law, the fixed six-vector, and all signed lifts and blanks now give every cell in §2. This construction uses the freedom of the stated coefficient model to attach $A_i,P_i,M_i$ to a common carrier. An additional constitutive law linking its internal shape, passive response or inertia would require a new compatibility check.

If each channel separately admits proportionality to the *same* $M_i$ in combinable worlds, choose those two realizations and their shared registration. With $A_i=k_A M_i$ and $P_i=k_P M_i$, they already give $P_i/A_i=k_P/k_A$. The joint test cannot reject such data. Conversely, neither inertia comparison is necessary for reciprocity of the leading pair coefficients.

## 4. One rejecting record and a compatible comparison

Keep the same springs and the same complete lift table for both records. Set $M=C(1,2,4)$, $u=(1,1/2,1/4)$ so the shared readings are cosines of the square roots of $3/2,5/4,3/4$ at settings $01,02,12$. These squared phases are on the strict first lobe. Let both lift gaps be $\phi>0$. Use $P=P_*(1,3/2,2)$, $W=g_wP_*\phi>0$ and $Z=g_c\phi/c^2>0$. Give all six lift rows clock reading $Z$. In field 1, with order blank, 0, 1, the signed $(w^+,w^-)/W$ pairs are $(1,-1),(2,-2),(3,-2)$. In field 2, with order blank, 1, 2, they are $(-1,1),(1,0),(1,-1)$.

The blanks fix the displayed holders $+W,-W$. The terminal rows fix $x_0=W/Z$ and $x_2=2W/Z$. The bridge permits $x_1\in[W/Z,2W/Z]$. The given passive vector realizes $x_1=3W/(2Z)$. Each bridge leg loses $W/(2g_w)$. All blank and terminal legs are lossless. Initial store energy $4W/g_w$ in a store supporting levels $W/g_w$ through $5W/g_w$ covers every signed leg. Thus any joint fit has $P_2/P_0=2$, independent of the absolute gains.

For both active records take true point sources at the common origin with totals $A=m(1,3/2,v)$, $m>0$, and $U_0=B=0$. Each of the six directions in sector $i$ reads $\Delta_i(n)=g_s G A_i/(4ac^2)$, so all half-sums equal $s_i=A_i/4$. This prescribes complete raw source readings. In the inverse test the source shape still ranges over the entire admitted class. Define $\rho=\kappa_+/\kappa_-$. The accepted bound gives $1<\rho<2$. Equation (1) implies the strict bounds $v/\rho<A_2/A_0<v\rho$ for every fit to those raw readings.

- **Reject, $v=1$.** Every allowed active ratio is below $\rho<2$, while the lift requires a ratio of 2. The point sources, passive vector, losses and springs above realize both experiments without proportional $P/A$. No admissible nonspherical profile can remove the gap.
- **Compatible, $v=2$.** The stated sources and passive masses give $P_i/A_i=P_*/m$ in every sector. Yet $M_2/M_0=4$, and the data force $P_2/P_0=2$ and $A_2/A_0<2\rho<4$. Thus even the *records* exclude both separate inertia proportionalities. The same compatible record admits a nonreciprocal world with those same sources and inertias. Take $x_1=W/Z$ and use (1) of the signed-lift theorem to adjust the two bridge loss splits. All four bridge leg readings are preserved. In detail their conservative rises are then $2W,0$ in fields 1 and 2, with outward and return losses $(W/g_w,0)$ in each field. The middle ratio now differs from the other two.

The endpoint issue can also be read directly in this family. At $v=2/\rho$ the upper bound $v\rho=2$ is only a supremum. If active endpoints were incorrectly included one could take $A_0=l_0,\ A_1=3l_0/2=l_1,\ A_2=2l_0=h_2$ with the midpoint passive vector. The actual positive interior sources exclude that fit, although the recorded law is realizable without a common ratio.

For the two specified records choose $\phi<\varepsilon c^2$ with zero potential at the lower lift stations and $0<m<\varepsilon ac^2/G$. Then both lift gaps and all central-source exterior potentials on the sampled paths satisfy the prescribed positive amplitude tolerance $\varepsilon$ in units of $c^2$. Their scaling preserves the ratio comparisons. Independent protocol selection, the common labelled histories and the readings above give both complete laws including their zero cells.

## 5. Scale and interpretation

The mass intervals use the source array's calibration. The lift constrains $x_i=(g_wc^2/g_c)P_i$. A common $r$ in (4) corresponds to $P/A=r\,g_c/(g_wc^2)$ using active mass units. A common positive rescaling of active mass units scales $l_i,h_i$ together. Changing the common lift displays $w\mapsto\beta w,\ z\mapsto\gamma z$ scales $x_i$ by $\beta/\gamma$. Both operations preserve the existence test. A numerical ratio requires the respective calibrations and even then (4) is open whenever it is nonempty. The arbitrary common mechanical scale $C$ cancels from this comparison. A field-dependent clock gain or sector-dependent work or source gain can instead alter relative coefficients. The accepted lift control illustrates why common transfer between its two fields is a substantive premise.

The decision concerns compatibility with reciprocity at the leading monopole order under the independent physical attachments. Finite clock and lift data in this ideal model can exclude that coefficient assignment or permit it. Neither outcome measures forces between the bodies, establishes momentum conservation, tests the full equivalence principle, or derives a physical mass unit from the native records.

## Reviewed sources

- [How twelve exterior clocks can exclude active-to-inertial mass proportionality](twelve_clock_active_mass_bounds.md)
- [When signed lifting work excludes a common passive-to-inertial mass ratio](signed_lift_work_and_passive_mass.md)
- [Testing proportionality of active and inertial mass across three carrier sectors](registered_active_and_inertial_mass.md)
- [What paired clock and motion records identify about probe response](paired_probe_response_and_acceleration_gain.md)

Scientific report SHA-256 ce04ed13a8c8cb81e8b193af212eb5132779917d97708da5a936f57102a69680. Independent review SHA-256 f16a4f96ed535d337bdacf883cf5f0d9c3c059e3db2386f4b42c517375113fd4.
