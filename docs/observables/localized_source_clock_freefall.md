# A conditional localized-source clock and differential-freefall map

3 November 2026. Independently reviewed conditional mathematics, GDM049. Physical source, apparatus and calibration premises remain unresolved; this is not a native-gravity or empirical-discrimination result.

The native input is the exact GDM047 construction in [Finite source, order, return and visibility](finite_source_order_return_and_visibility.md), including its full lawful source cut. This note adds an explicitly supplied classical localization, mass and weak-field observation map. It preserves the accepted scientific derivation below; the native model and physical comparison assumptions have different evidential roles.

## 1. Decision and precise scope

The fixed GDM047 native law admits the stipulated, normalized source-to-observation pushforward. At the fixed finite spatial baseline its leading weak-field clock and differential-freefall contrasts are both nonzero and share ONE normalization:

    Delta C = -(37/3360) theta,
    Delta T = -(391/33075) theta,
    theta = G m_* / a^3 > 0.

Consequently 11655 Delta T - 12512 Delta C = 0. The finite-baseline quantities are unequal. Their coefficients are obtained from the complete native source law, without postselection or separate clock/motion fits.

This is a conditional mathematical correspondence, with an explicit operational frame and sufficient remainder bounds below. An actual apparatus with those bounds is NOT established. In particular the higher-order physical metric and its derivatives, held-source/controller stresses, transfer protocol, geometry calibration and initial conditions remain supplied premises. If their stated error budgets are unavailable, physical attribution is unresolved. A matched conventional weak-field GR model has exactly the same observation law. This result does not distinguish DET from GR, derive mass/units/geometry, promote metric-as-record, or authorize a successor.

## 2. Accepted native law and supplied physical map

The exact pinned GDM047 witness and its complete lawful source cut are retained: all six tau values, every branch map/effect, actual ideals, both preparation bits, both subsequent bits, zero cells, complements, boundary states and whole-cone obligations remain unchanged. Their native proofs are accepted inputs, not recomputed here. In particular no aggregate substitution is made for the cut.

Write s=c for chain and s=a for antichain, lambda_c=lambda_a=1/2. The fixed probe is nu=delta_10 tensor delta_0. Each retained preparation outcome k=0,1 has joint map I8/2. With GDM047's exact B maps, the complete law is

    P_N(s,k,S,b,j,n) = (lambda_s/2) [B_(C_s,k,S,b) nu]_(j,n).

Here S ranges over the actual ideals of its prepared parent, b is the subsequent retained bit, j in {00,10,01,11} is the source/reservoir occupation pair, and n in {0,1} is the reference bit. There are 2*(4+3)*2*8=224 controlled cells across settings and k. Zero cells remain cells. At every prepared parent the sum over S,b,j,n is one; summing both k with their 1/2 weights and both settings with lambda_s gives total mass one. All setting contrasts below are conditional means under their recorded setting, averaging BOTH k and all other native outcomes. They do not condition on a favorable S,b,j,n subset.

The accepted witness terminal laws are

    c: (0,51/64,13/64,0) tensor (9/16,7/16),
    a: (0,3/4,1/4,0) tensor (9/16,7/16).

Thus delta=3/64 is the chain-minus-antichain change of mean source occupation r; the reservoir occupation e changes by -delta. Q=r+e=1 for this probe. For the full lawful cut BOTH setting terminal laws have the antichain source marginal. This does not assert equality of the complete native graph/ideal record laws across settings.

Supply a>0, positive common mass m_* per occupation, kappa=G m_*, G,c, a Euclidean spatial embedding and a held, quasistatic readout phase. Put occupation r at +a e_x and occupation e at -a e_x. These are physical-model inputs, not DET consequences. The exterior three-dimensional potential and its axis restriction are

    Phi_j(X) = -kappa[r_j/|X-a e_x| + e_j/|X+a e_x|] + A + B x,
    Phi_j(x) = -kappa[r_j/(x-a) + e_j/(x+a)] + A + B x,  x>a,
    g_j(x) = -Phi'_j(x).

A and B are common affine nuisances at the retained order. Source support, reference carrier, controllers, clocks and probes have common/matched gravitation and stresses or bounded contributions. Zero assigned native Q for the reference does NOT imply physical masslessness. Common native cost access is retained; no physical energy/cost closure is derived from Q conservation. The source is assumed static over readout; no source-transfer trajectory, radiation or retardation theorem is supplied.

Use the supplied static weak-field metric, to first order in phi=Phi/c^2,

    ds^2 = -(1+2phi)c^2 dt^2 + (1-2phi)dX^2 + higher-order terms.

Higher-order terms and their needed derivatives require bounds; the displayed truncation is not an exact physical metric. Fix R=3a, d=a/2 and x_-=5a/2, x_0=3a, x_+=7a/2. No placement or coefficient is optimized.

## 3. Common operational frame, clocks, and initially comoving probes

For each held source state j, use the central static observer at x=R, with proper time tau_0=N_R t, where N(x)=sqrt(1+2phi(x)) and S(x)=sqrt(1-2phi(x)) in the displayed metric surrogate. Its x axis is the nonrotating, Fermi-Walker orthonormal direction S_R^(-1) partial_x. There is no shift or rotation. The static Killing slice t=t_0 is orthogonal to the static congruence. Calibrated symmetric radar synchronization in this static geometry selects that simultaneity; unmodeled transfer effects must enter the error budget.

Along the exterior axis define operational signed spatial distance on that slice by the full integral

    ell(x) = integral from R to x of S(u) du.

The axis curve is an orthogonal spatial geodesic by axial symmetry. This is a finite-distance coordinate convention anchored to the central observer, with no finite-order spatial Fermi expansion. The prescribed x_+ and x_- are symmetric in the supplied leading coordinate, not exactly symmetric in ell. Their leading physical separations are +d and -d, with a bound below. The reported quantities use the declared calibration d. A protocol using measured proper half-spacing must convert to that convention or include its calibration correction.

A static clock at x has instantaneous proper-rate ratio N(x)/N_R relative to the central proper clock. Calibrated transfer permits estimating that ratio. Its retained excess rate is

    z_j(x) = [Phi_j(x)-Phi_j(R)]/c^2.

For the freefall readout, release two probes initially at rest relative to the static congruence at x_+ and x_- on the common slice. Thus dx/dt=0 at release. In the displayed static metric the geodesic equation at that instant gives

    d^2x/dt^2 = -c^2 N N'/S^2 = -Phi'(x)/(1-2phi(x)).

The operational position acceleration measured using the central time and the specified distance is, at release,

    a_ell(x) = d^2ell/dtau_0^2
             = -Phi'(x) / [(1+2phi_R) sqrt(1-2phi(x))].

The S'(dx/dt)^2 term vanishes at release. Therefore a_ell(x)=-Phi'(x) at retained first order. Differencing the two probes removes the common leading inertial acceleration associated with the central static observer. A probe's own freely falling accelerometer reads zero; this protocol estimates relative position accelerations in the central observer's defined frame. Coordinate acceleration by itself is not an invariant tidal observable, nor is the finite difference asserted to be a pointwise curvature component.

Define the retained finite-baseline quantities

    C_j = c^2[z_j(x_+)+z_j(x_-)]/d^2,
    T_j = -[g_j(x_+)-g_j(x_-)]/(2d).

The motion protocol above measures the stipulated g differences at the retained order, with corrections bounded as follows. Full potential dependence across the baseline is retained; curvature gradients are not discarded by an infinitesimal approximation.

### Sufficient conversion and remainder bounds

Assume uniformly over the used states and calibration neighborhood

    |phi| <= eta <= 1/8,
    M1 >= sup |Phi'|,   M2 >= sup |Phi''|.

These are supplied finite bounds outside the sources. The elementary square-root bounds give

    |ell(x)-(x-R)| <= 2 eta |x-R|,
    |ell(x_+) - d| <= 2 eta d,
    |ell(x_-) + d| <= 2 eta d.

For the acceleration factor F=[(1+2phi_R)sqrt(1-2phi_x)]^(-1), use |(1+2phi_R)^(-1)-1| <= (8/3)eta, (1-2phi_x)^(-1/2) <= 4/3 and |(1-2phi_x)^(-1/2)-1| <= 2eta. Hence |F-1| <= (50/9)eta < 6eta and

    |a_ell(x)+Phi'(x)| <= 6 eta M1.

For the clock factor f(p,q)=sqrt((1+2p)/(1+2q)), its second derivatives on this box obey |f_pp|<2, |f_pq|<2, |f_qq|<7. Taylor's theorem about (0,0) therefore gives

    |N(x)/N_R - 1 - (phi_x-phi_R)| <= 7 eta^2.

These inequalities bound only conversion in the displayed surrogate. They do NOT bound arbitrary omitted physical metric terms. In particular small metric amplitude alone supplies no bound on its derivatives or on a freefall observable. Require a physical C1 metric/remainder bound sufficient for acceleration, plus the clock-transfer and apparatus bounds. Let E_z and E_g bound all remaining effects uniformly: higher-order physical lapse/metric/connection terms, imperfect initial comoving release, transfer/reconstruction, stress/background mismatch and instrumental error. E_z is dimensionless; E_g has acceleration units. These must be established externally rather than assigned zero because the native model omits them.

If all relevant endpoint and central coordinate calibration errors are at most sigma_x in the bounded neighborhood, a sufficient total support budget is

    epsilon_z >= 7 eta^2 + 2 M1 sigma_x/c^2 + E_z,
    epsilon_g >= 6 eta M1 + M2 sigma_x + E_g.

The first calibration term covers both endpoint and central potentials. M2 controls the acceleration change at a displaced endpoint. Uniform bounds must include any frame-origin or normalization calibration not already removed by known conversion. If a measured half-spacing d_m differs from d by at most sigma_d<d, either rescale the reported C and T explicitly to d, or include the denominator factors (d/d_m)^2 and d/d_m and their bounded effect. No equality of coordinate and proper separation is silently assumed. Unavailable finite E_z/E_g or calibration bounds leave actual physical attribution unresolved.

### Flat accelerated-frame control

The exact flat, nonrotating uniformly accelerated chart provides a necessary check beyond leading order:

    ds^2 = -(1+g_0 ell/c^2)^2 c^2 dtau^2 + dell^2 + dy^2 + dz^2,
    |g_0 d/c^2| < 1.

For static clocks at ell=+d,-d, the excess rates are exactly +g_0 d/c^2 and -g_0 d/c^2, so C=0. Initially comoving freely falling probes have central-time relative acceleration

    a_ell(ell) = -g_0(1+g_0 ell/c^2).

Their raw motion statistic is T_raw=g_0^2/c^2, even though curvature is zero. At retained first order T=0; the higher-order term must be subtracted using the calibrated inertial frame or bounded. Per endpoint its departure from -g_0 is at most g_0^2 d/c^2. Thus raw finite central-time relative acceleration is not an all-orders curvature test. This concrete correction also prevents interpreting the affine control's first-order cancellation as exact at every order.

The exact-version clock-compass source is used only for frame/approximation caution and the accelerated metric form, not for its reconstruction theorem. Its sign convention is opposite to the one used here. The finite-baseline derivation above uses the supplied potential directly.

## 4. Exact spatial arithmetic at the retained weak-field order

Put mu=kappa/(a c^2) and theta=kappa/a^3. For j=10 the inverse source distances at (x_-,R,x_+) are (2/3,1/2,2/5)/a. For j=01 they are (2/7,1/4,2/9)/a. The resulting rates and accelerations are:

| Occupation | z_+ | z_- | g_+ | g_- |
|---|---|---|---|---|
| 10 | mu/10 + Bd/c^2 | -mu/6 - Bd/c^2 | -(kappa/a^2)(4/25)-B | -(kappa/a^2)(4/9)-B |
| 01 | mu/36 + Bd/c^2 | -mu/28 - Bd/c^2 | -(kappa/a^2)(4/81)-B | -(kappa/a^2)(4/49)-B |

The constant A cancels in rates and derivatives. For general j, multiply the source contributions by r_j and the reservoir contributions by e_j, adding the common affine contribution once. This defines the same map on j=00 and j=11, even though those cells have zero probe probability.

With d=a/2 the finite contrasts for each terminal occupation are

| Occupation | C_j/theta | T_j/theta |
|---|---:|---:|
| 10 | -4/15 | -64/225 |
| 01 | -2/63 | -128/3969 |

For example C_10=4 theta(1/10-1/6)=-4 theta/15, and T_10=theta(4/25-4/9)=-64 theta/225. Similarly C_01=4 theta(1/36-1/28)=-2 theta/63 and T_01=theta(4/81-4/49)=-128 theta/3969. These are exact rational finite-distance evaluations, not a small-d Taylor series.

The population means under the two settings retain the full native mixture:

    E[C|c] = (51/64)C_10 + (13/64)C_01,
    E[C|a] = (3/4)C_10 + (1/4)C_01,

and the same expressions hold for T. Therefore

    Delta C = (3/64)(C_10-C_01),
    Delta T = (3/64)(T_10-T_01).

Now C_10-C_01=-(74/315)theta, while T_10-T_01=-(25024/99225)theta. Multiplying by 3/64 yields

    alpha_C = 37/3360,
    alpha_T = 391/33075,
    (Delta C,Delta T) = -theta(alpha_C,alpha_T).

Both coefficients are positive and neither can be separately retuned. Their ratio is alpha_T/alpha_C=12512/11655. A division-free common-scale relation is

    11655 Delta T - 12512 Delta C = 0.

In particular C and T are not equal: even at a single source occupation, T_10-C_10=-(4/225)theta and T_01-C_01=-(2/3969)theta. The finite spatial baseline matters. External geometry, units and protocol calibration make theta the identifiable parameter combination in these means. They do not separately infer native G, m_*, a or a time unit. If a and G are supplied externally one can of course translate theta into a conditional m_* estimate; that is not a native mass derivation.

## 5. Complete normalized observation channel

Let Y=(z_+,z_-,g_+,g_-) and let Y_j denote the four-component leading value above, defined for all j. The ideal observation kernel is K_0(dY|j)=Dirac_(Y_j)(dY). The complete pushforward, retaining the native record labels, is

    P_obs(s,k,S,b,dY)
      = sum_(j,n) P_N(s,k,S,b,j,n) K_0(dY|j).

Every setting, preparation bit, actual ideal and outcome bit remains. All j,n cells are summed, including zero cells and complements. If terminal j,n are also retained by the declared augmented native access, the unsummed law P_N K_0 is the corresponding refinement; the same access must be offered to every comparator. No outcome-dependent renormalization or postselection is used. For any probability kernel K with integral K(dY|j)=1, summing records and integrating Y returns exactly one, by native normalization.

A bounded-error observation family consists of EVERY probability kernel K_epsilon(dY|j) with total mass one and support in

    Y_j + [-epsilon_z,epsilon_z]^2 x [-epsilon_g,epsilon_g]^2,

uniformly over all native states and settings. This is a normalized channel family, not clipping, a subprobability measure or an unnormalized perturbation. Arbitrary correlations among the four errors are allowed; no Gaussian distribution, independent noise or zero-mean bias is assumed. The binding matched observation-map premise is that the SAME conditional kernel is used under both settings and the full cut. Setting-independent conditional response is a supplied apparatus property, not a native theorem. Equal marginal error bounds alone do not imply it.

The complete pushforward contains more information than the two means analyzed next. Passing their consistency test does not certify the full joint law.

## 6. Worst-case population regions and common normalization

Under one kernel, the expectation biases of each conditional C_j and T_j obey independently

    |b_C(j)| <= B_C = 2c^2 epsilon_z/d^2 = 8c^2 epsilon_z/a^2,
    |b_T(j)| <= B_T = epsilon_g/d = 2 epsilon_g/a.

The rectangular extremes are attainable by normalized deterministic error kernels; there is no hidden independence premise. The clock errors occupy different components from the acceleration errors, so their extreme conditional biases can be achieved together.

### Binding matched conditional channel

For the SAME K_epsilon(.|j) in both settings, the exact difference of terminal j probabilities is delta at 10 and -delta at 01. Thus the contrast error is delta[b(10)-b(01)], not a general difference of two unrelated apparatus biases. Its exact attainable mean-error rectangle has half-widths

    h_C = 2 delta B_C = (3/4)c^2 epsilon_z/a^2,
    h_T = 2 delta B_T = (3/16)epsilon_g/a.

This reduction is justified solely by the common conditional channel and the accepted native marginals. It does not assume statistical independence or average away noise. At a fixed theta, the witness contrast region is

    R_h(theta) = [-alpha_C theta-h_C,-alpha_C theta+h_C]
                 x [-alpha_T theta-h_T,-alpha_T theta+h_T].

The full source cut has identical terminal j distributions between settings for this probe; with its common conditional response it has exactly zero population setting contrast even if that response is biased. The full underlying record laws need not be identical. The co-located Q-only control has the same Q in both settings, but its native j distributions need not agree. Its zero-contrast statement requires an ideal response or a truly Q-only conditional kernel K_Q(.|Q). If a bounded readout is permitted to depend on the hidden split j despite the co-located source, its null contrast can occupy [-h_C,h_C] x [-h_T,h_T]; it is then not a pure Q-only response. Guaranteed separation from that larger matched null rectangle requires alpha_C theta>2h_C OR alpha_T theta>2h_T.

The witness region excludes the origin precisely when alpha_C theta>h_C OR alpha_T theta>h_T. Each channel separately excludes zero when its own strict inequality holds; both do so when both hold. Equality includes the boundary and does not establish exclusion. Without a positive externally justified lower bound on theta, there is no uniform separation over all theta>0, since the signal approaches zero.

### What remains if conditional apparatus matching is not established

If only the same uniform support bounds are established, a kernel K_s(.|j) may differ by setting. That is a relaxation, not the binding common-map premise. The conservative, attainable contrast rectangle then has half-widths

    H_C = 2 B_C = 16c^2 epsilon_z/a^2,
    H_T = 2 B_T = 4 epsilon_g/a.

The witness region is R_H(theta). A null source contrast can itself occupy [-H_C,H_C] x [-H_T,H_T]. Excluding the origin from the witness region uses alpha_C theta>H_C OR alpha_T theta>H_T, but guaranteed disjointness from the entire uncertain null rectangle requires the stronger condition alpha_C theta>2H_C OR alpha_T theta>2H_T. These are different statements. Unknown setting-dependent apparatus effects cannot be declared canceled merely because their bound is common. If even these uniform bounds are unavailable, the physical inference is unresolved.

### Common-scale falsification or inconclusive outcome

For either explicitly selected rectangle width w=(h_C,h_T) or the relaxed w=(H_C,H_T), let (u,v) be the observed population contrasts. The exact mean-level compatibility condition is a single common positive theta in

    Theta_C = [(-u-w_C)/alpha_C, (-u+w_C)/alpha_C],
    Theta_T = [(-v-w_T)/alpha_T, (-v+w_T)/alpha_T],
    Theta_C intersect Theta_T intersect (0,infinity) nonempty.

Empty intersection rejects the combined fixed correspondence and its claimed error bounds. A nonempty intersection makes those mean contrasts compatible; it does not prove the native source law, actual error bounds or geometry. It may remain compatible with zero/null alternatives at the stated resolution.

The useful necessary division-free check is

    |11655 v - 12512 u| <= 11655 w_T + 12512 w_C.

A violation falsifies common-scale compatibility. Satisfaction alone is insufficient: positivity and interval intersection still have to hold. This avoids a ratio of nearly zero quantities. All these statements concern exact population means and support-constrained channels. They provide no finite-sample power, sample-size claim, experimental sensitivity or physical readiness.

## 7. Controls at the same map and cost boundary

**Full lawful native source cut.** Use the pinned GDM047 whole branch family, including every unchanged tau/effect/reference branch and the authorized chain/full H replacement. Pass its entire normalized law through the same localization, masses, apparatus access and conditional observation kernel. Both setting source marginals are (3/4,1/4), giving Delta C=Delta T=0 under the ideal or matched conditional kernel. The conclusion is about these source-derived setting contrasts, not equality of all records. Common versus merely bounded apparatus errors have the different consequences in section 6.

**Co-located Q-only source.** Replace the localization rule by a single co-located mass m_* Q at the origin with the same cost/access convention. Because Q=1 under both settings, the ideal setting contrasts vanish; they also vanish for a common kernel depending only on Q. Allowing additional j-dependent readout biases instead gives the qualified null region in section 6. The readouts themselves do not vanish: at the fixed x_-,R,x_+ the inverse distances are (2/5,1/3,2/7)/a and

    C_Q = -(8/105)theta,
    T_Q = -(96/1225)theta.

Hence this control tests the setting-dependent localization response rather than pretending that fixed total Q generates no gravitational field. A single-source Q model without split information cannot reproduce a nonzero population setting contrast under a common response depending only on Q. Common support bounds alone do not enforce that restriction.

**Affine potential.** For Phi=A+Bx, z_+=Bd/c^2, z_-=-Bd/c^2 and g_+=g_-=-B, so C=T=0 at retained order. Higher-order lapse, frame and transfer terms must still satisfy the error budget. Section 3's exact flat accelerated chart demonstrates explicitly the nonzero second-order raw motion correction in flat space; it cannot be interpreted as native or physical curvature.

**Matched conventional weak-field GR.** Supply a conventional stochastic source whose probabilities over j and retained classical labels are exactly P_N and use the SAME masses, placements, held-source assumptions, apparatus and kernel. Its full P_obs is then term-by-term identical, including all complement/zero cells and noise correlations. This comparator is stronger than agreement of two means. Accordingly no DET-versus-GR discriminator exists in this calculation. Neither a gravity Novelty Ledger promotion nor an empirical discriminator is produced. Geometry here remains a known-answer supplied fixture, not emergence.

## 8. Premise accounting and stop

Established conditionally: a normalized complete native pushforward; exact rational finite-baseline clock and motion coefficients; one common-scale relation; an operational initial relative-motion derivation; explicit weak-field conversion bounds and the accelerated flat-space correction; exact matched-channel and conservative unmatched-channel population regions; all required controls.

Not established: native selection of the localization map, physical G/c/units/mass, a source/controller stress-energy completion, actual calibrated apparatus/remainder bounds, sustained finite-time freefall trajectories, full curvature reconstruction, Einstein dynamics, empirical discrimination or finite-sample detectability. The metric derivative/remainder and apparatus bounds are load-bearing physical premises, not consequences of a successful native normalization proof. The exact accepted native law is not made more physical by omitting its reference or its records.

This advances only the conditional paired weak-field source/clock response and its observer-map accounting. Option B and Status M are unchanged. No new geometry/probe, fourth native birth, placement retune, lettered QR gate, coverage/noncollapse sequel, software work, publication or automatic successor is proposed. The finite result has completed distinct proof review and coordinator adoption. Later work requires its own question and review.

## 9. Sources, review and preserved limits

The [clock-compass paper, arXiv:1805.10673v2, 25 July 2018](https://arxiv.org/html/1805.10673v2), was checked at its introduction and Sections II.3–III, equations16–24, for frame and approximation cautions. It does not derive this source localization, native probability law or finite-baseline response; no full compass reconstruction theorem is imported. [Roura, arXiv:1810.06744v1, 15 October 2018](https://arxiv.org/abs/1810.06744v1), supplies only abstract-level protocol/preparation context; no interferometer theorem or apparatus feasibility is used. These are limited source reads, not full-paper audits.

The full author report is26,466bytes, SHA256`3a2240309d9c3b0e249b55321077771e2cdb09cd4a053fb06634774f7bddeae6`. Its distinct scientific review is14,786bytes, SHA256`974db37f3d5e2896bce54ed6b36589421c43080f1794f7550067ded8f86a8a61`. The author completed within the original05:12:03 substantive and05:18:03 hard deadlines; the reviewer completed05:44:58 within05:45:52/05:49:52. Coordinator acceptance is at the exact conditional scope. A later publication review does not substitute for that scientific review.

The earlier E041/E042/CL042 procedural qualifications and GDM047's E33 dispatch-clock qualification remain unchanged. This new result does not retrospectively certify them. Option B and Status M remain unchanged. All software work is paused. This note does not adopt any later recoil, reversal, parameter or horizon proposal.
