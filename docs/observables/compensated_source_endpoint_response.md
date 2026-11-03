# Compensated source endpoints: paired clock and free-fall response

GDM051, accepted 3 November 2026. This fixed conditional construction adds a gravitating auxiliary mass to the accepted [localized-source response](localized_source_clock_freefall.md), while preserving the complete [GDM047 native law](finite_source_order_return_and_visibility.md). It tests whether the paired response survives this particular endpoint compensation. It does; no claim of an isolated transition, native gravity, native mass unit or empirical discrimination follows.

## Fixed source boundary

For terminal source state j=(r,e), with r,e in {0,1}, put masses mr at +a and me at -a, and one auxiliary mass 2m at X_A=-(a/2)(r-e), along the x-axis. The listed total mass is m(Q+2), Q=r+e, and its first moment is zero in all four states. The actual Q=1 preparation has total mass 3m in both alternatives. No transition between different Q sectors is asserted.

This is a supplied three-dimensional, static inverse-distance source map with externally supplied m,a,G,c, equality of inertial and gravitational mass, and a common affine potential A+Bx. Zero endpoint COM is a necessary condition for an isolated rearrangement in the specified COM-rest frame of the fixed listed masses. It does not prove a path, isolation, momentum/angular-momentum/work closure or a complete actuator boundary. Holding forces, reference and record masses, stresses and controllers are not accounted for by the endpoint identity. The accepted native charge is unchanged; the auxiliary is not an additional native degree of freedom.

Writing kappa=Gm, on x>a the two actual potentials are

    Phi10(x) = -kappa[1/(x-a) + 2/(x+a/2)] + A+Bx,
    Phi01(x) = -kappa[1/(x+a) + 2/(x-a/2)] + A+Bx.

Their exact difference is

    Phi10-Phi01 = -(3/2) kappa a^3 / [(x^2-a^2)(x^2-a^2/4)].

After cancelling the common affine term, the first nonzero positive-axis exterior term is -(3/2) kappa a^3/x^4, with remainder O(kappa a^5/x^6). This static asymptotic statement is not radiation or a transition dynamics calculation. The following finite measurements do not use that expansion.

## Exact finite paired response

Use the same fixed R=3a, d=a/2 and operational convention as the accepted localized-source result: z_±=[Phi(R±d)-Phi(R)]/c^2 to retained weak-field order, g_±=-Phi'(R±d), C=c^2(z_++z_-)/d^2 and T=-(g_+-g_-)/(2d). Define theta=kappa/a^3>0. The auxiliary contributes to both channels:

| Endpoint | C/theta | T/theta |
| --- | --- | --- |
| 10 | -38/105 | -229/600 |
| 01 | -94/315 | -2461/7938 |

The complete native source contrast remains +3/64 at10 and -3/64 at01. Therefore

    Delta C = -theta/336,
    Delta T = -56867 theta/16934400,
    50400 Delta T - 56867 Delta C = 0.

Both contrasts are nonzero. The finite-baseline coefficients differ and share one scale; they are not independently fitted. C,T,theta have dimensions of inverse time squared. These observations constrain only the supplied combination Gm/a^3 under external geometry, clocks and calibration; they do not determine native units or separate G,m,a.

## Operational and error premises

The accepted same-frame construction uses the central held observer's proper time, normalized spatial axis, static simultaneity and finite proper distance. At simultaneous release from rest its exact initial relative position acceleration in the assumed metric is

    d^2 ell / d tau0^2 = -Phi'(x)/[(1+2 Phi(R)/c^2) sqrt(1-2 Phi(x)/c^2)].

A freely falling probe's own proper acceleration is zero. The initial relative acceleration here is not an invariant curvature definition or a finite trajectory prediction.

All source-dependent bounds must include the auxiliary. For 0<=sigma_x<a/2, let x_L=5a/2-sigma_x, x_U=7a/2+sigma_x, D_+=x_L-a, D_-=x_L+a, D_A=x_L-a/2. Uniformly over all four j and the exterior interval [x_L,x_U], sufficient bounds are

    U0 = kappa(1/D_+ + 1/D_- + 2/D_A) + |A| + |B|x_U,
    U1 = kappa(1/D_+^2 + 1/D_-^2 + 2/D_A^2) + |B|,
    U2 = 2kappa(1/D_+^3 + 1/D_-^3 + 2/D_A^3).

With eta=U0/c^2<=1/8, sufficient per-reading budgets are

    epsilon_z >= 7 eta^2 + 2 U1 sigma_x/c^2 + E_z,
    epsilon_g >= 6 eta U1 + U2 sigma_x + E_g.

Finite body size, nonoverlap, weak compactness, omitted metric derivatives, stresses, release/transfer and instrument effects require valid finite E_z,E_g or equivalent bounds. Small potential alone does not bound the connection. Baseline/frame conversion must also be calibrated. None of these physical bounds is established by the endpoint algebra.

The original 224-cell law retains every setting, preparation outcome, actual ideal, bit, terminal source/reference state, zero and complement. Apply a normalized source-dependent readout kernel to every cell, with the auxiliary position a deterministic function of j. Terminal source/reference access must be supplied equally to comparators. Actual failures need explicit retained outcomes and a stated mean convention; success-only conditioning is excluded.

For a common source-only conditional kernel, attainable contrast error half-widths are h_C=3c^2 epsilon_z/(4a^2) and h_T=3epsilon_g/(16a). Merely common support with setting/record-dependent responses requires H_C=16c^2 epsilon_z/a^2 and H_T=4epsilon_g/a. Equal bounds do not imply matched response. Let w denote the explicitly justified pair and alpha=(1/336,56867/16934400). The mean rectangle centered at -theta alpha excludes zero iff alpha_C theta>w_C or alpha_T theta>w_T; comparison with an equally uncertain null requires the stronger 2w thresholds. Equality is boundary contact. Widths used across a theta interval must be valid uniformly on it, or retain their theta dependence. These are population-mean statements, not finite-sample power.

A common positive theta requires the intersection of [(-u-w_C)/alpha_C,(-u+w_C)/alpha_C], [(-v-w_T)/alpha_T,(-v+w_T)/alpha_T] and (0,infinity) to be nonempty. The necessary residual bound

    |50400 v - 56867 u| <= 50400 w_T + 56867 w_C

is not sufficient for that positive intersection or physical attribution.

## Controls and scope

The complete lawful source cut has equal terminal-source marginals across settings. Through the same source-only readout it therefore has equal readout marginal laws, not necessarily equal complete retained records. A setting-dependent response can destroy that null.

The co-located control includes total assigned mass m(Q+2), hence3m for the actual probe, giving C=-8theta/35 and T=-288theta/1225 in both settings. Its contrast is zero only under ideal or genuinely total-mass-only response; conditional biases retain the appropriate uncertain null. Affine terms cancel at retained order. In an exactly flat accelerated chart the raw motion statistic can still be T=g0^2/c^2 while C=0; this higher-order inertial contribution must be corrected or bounded and is not curvature. Conventional GR with the identical complete source, apparatus, readout, failure, access and cost assumptions gives the same observations term by term.

This closes only the fixed ratio-two endpoint question. It leaves physical transition, holding and complete resource accounting unresolved. No geometry, ratio or native coefficient was retuned. No software, empirical acquisition or new physical calibration is reported.

## Provenance and procedural qualification

Author: existing DET Quantum Relativity chat. Frozen GDM051 REPORT: SHA256 b8ff4fefe48896a56ce37a430f82e27f2a2bc0c2ef90ed4835ecfb76eb85fcb0. Separate prospective scientific review by broad_native_select: SHA256 7603f08fa8da2a192a81e3a6f6a5b12726ad18c2fcd1f4abf73eaf8925594f44; saved full read06:57:46 UTC, before07:00:05 cutoff, final custody06:58:49 before07:04:05 hard end. Coordinator disposition is in followthrough-0641-20261103/GDM051_DISPOSITION.json in the research evidence store.

The first review missed its required saved-report full-read cutoff06:52:10 and remains PROCEDURE_INCOMPLETE. The new review did not use that draft and does not retroactively certify it. Earlier recorded procedural qualifications also remain permanent. The scientific source is the full frozen report with its accepted GDM047/GDM049 dependencies; this note is a scoped publication summary.
