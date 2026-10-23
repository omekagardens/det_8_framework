# RI1406: Calibration, transfer and conditional admission

23 October 2026. This documentation checkpoint consolidates the root-adjudicated RI1405 height-to-clock bridge, E-C013 invariant-box rate certificate and NE-C013 common-source transfer/risk composition. CE's strict resident-memory execution hold and the measurement binding gap are carried forward. These are conditional mathematical and documentary results; no scientific execution, physical success, operational admission or new successor result is claimed.

## QR: intrinsic height needs an external clock premise

For the selected RI1299 baseline under its admitted construction and classical history measure, take the inherited bounds as premises:

\[
H_N\le N,\qquad\liminf_{N\to\infty}H_N/N\ge1/2\quad\text{almost surely}.
\]

Here height counts vertices and the integer event index is dimensionless. This checkpoint does not rederive that stochastic theorem or transfer it to another optimizer or an infinite harmonic continuation. For any fixed \(0<\epsilon<1/2\), eventually \((1/2-\epsilon)N\le H_N\le N\) on the height event. Dividing logarithms by \(\log N\) proves \(\log H_N/\log N\to1\).

Separately require a positive increasing divergent clock \(\tau_N\), a positive reference duration \(\tau_{\rm ref}\) in the same unit, and

\[
\frac{\log(\tau_N/\tau_{\rm ref})}{\log N}\to\beta,
\qquad0<\beta<\infty.
\]

Then the quotient of the two limits gives

\[
\frac{\log H_N}{\log(\tau_N/\tau_{\rm ref})}\to1/\beta.
\]

The clock logarithm is dimensionless and eventually positive. With a random or history-dependent clock, the result holds on the intersection of the height and clock events. Both must have probability one for an almost-sure conclusion; independence is unnecessary. A random positive finite exponent gives its path-dependent reciprocal. The height theorem does not establish the clock event.

The stronger, independently justified calibration \(aN\le\tau_N\le bN\) eventually, with deterministic finite time-valued \(0<a\le b\), yields clock exponent one and only

\[
\liminf H_N/\tau_N\ge1/(2b),\qquad\limsup H_N/\tau_N\le1/a.
\]

An exact rate does not follow. Power clocks \(\tau_N=\tau_{\rm ref}N^\beta\) preserve all order and height data while changing the clock exponent. As a countermodel to an exact-rate deduction, chain orders have \(H_N=N\), while the increasing clock \(\tau_N=\tau_{\rm ref}N[2+\tfrac12\sin(\log N)]\) is of linear order but gives liminf \(2/(5\tau_{\rm ref})\) and limsup \(2/(3\tau_{\rm ref})\). This chain example is not asserted to be a typical trajectory of the selected native law.

The missing physical premise is an operational clock/readout-to-event correspondence with independently justified calibration and event coverage. A definition \(\tau_N=N\tau_{\rm ref}\) supplies a convention. A fixed unit conversion cannot select the exponent. Count per time is not spatial velocity; a spatial-length interpretation, metric dimension and empirical validation remain absent. If two models have the same full joint order/clock law, common measurable summaries have the same law. The previously accepted fixed four-query classical equivalence does not establish that full-process match or arbitrary intervention equivalence.

## E: obtain the enclosure before computing the rate

E-C013 separately postulates the continuous two-zone law, almost everywhere in real time:

\[
q=g(T_1-T_2)+b,\qquad
C_1T'_1=\eta_1P_1-h_1(T_1-T_a)-q+w_1,\qquad
C_2T'_2=\eta_2P_2-h_2(T_2-T_a)+q+w_2.
\]

Require constant \(C_i,h_i>0\), \(\eta_i\ge0\), measurable essentially bounded realized inputs, and independent finite bounds

\[
0\le P_i\le\bar P_i,\quad0\le g\le\bar G,\quad
A_-\le T_a\le A_+,\quad |b|\le b_*,\quad|w_i|\le\omega_i.
\]

The bias bound \(b_*\) is unrelated to the QR clock exponent. An independently established finite initial enclosure is also required. Exogenous bounded inputs give a measurable affine vector field with bounded Lipschitz coefficient and hence a unique absolutely continuous solution on each finite interval while the bounds hold. A physical feedback/switching implementation needs its own well-posedness and realized-input premises.

Choose \(L<U\) containing that initial enclosure and satisfying, for both zones,

\[
L\le A_--(b_*+\omega_i)/h_i,\qquad
U\ge A_++(\eta_i\bar P_i+b_*+\omega_i)/h_i.
\]

This common rectangle \(R=[L,U]^2\) is chosen without assuming the desired service or safety band. At each lower face, nonnegative coupling points inward and the lowest ambient/heater/disturbance combination gives a nonnegative temperature derivative. At each upper face the coupling again points inward and the largest heater/ambient/disturbance combination gives a nonpositive derivative. More formally, clip the state to \(R\) and sum its positive coordinate violations to obtain \(V\). With \(K=\max_i(h_i+2\bar G)/C_i\), the positive-part chain rule yields \(V'\le2KV\) almost everywhere. Initial containment gives \(V(t_0)=0\); Gronwall proves invariance.

Only after this enclosure is established define

\[
D_R=U-L,\quad A_R=\max\{|L-A_-|,|L-A_+|,|U-A_-|,|U-A_+|\},
\]
\[
B_i=\frac{\eta_i\bar P_i+h_iA_R+\bar G D_R+b_*+\omega_i}{C_i}.
\]

The triangle inequality now gives \(\operatorname*{ess\,sup}|T_i'|\le B_i\), in K/s. The earlier two-endpoint intersample implication may use \(M_i=B_i\), a proved larger value, or a separately proved tighter bound. This certificate does not justify an arbitrary smaller \(M_i\). Its excursion margin is reading uncertainty plus \(M_iL_k^+/2\), where \(L_k^+\) is a certified upper physical gap. Crediting uninterrupted dwell requires a lower elapsed-time bound. Nominal twenty 60-second intervals have no positive clock-error slack.

The construction fails without initial containment or the required finite/sign/regularity assumptions. With zero heat loss, uncoupled positive heating can be unbounded; this does not say every zero-loss system is unbounded. The rectangle can be so broad that the tightened service band is empty. The sampled Euler update supplies neither continuous physical interpolation nor calibrated parameters. Actual plant/input bounds, readout error and lag, physical clocks, causal future endpoint enclosures, controller feasibility, dwell, terminal reset and source-to-reset energy remain missing. D60, the 64-step cap, W20, conditional full-window entry by step 44 and later-entry continuation are unchanged. The competent matched 32-packet MHE comparison, equal causal channels/resources, failure/reset costs, independent held-out iid evaluation and reliability/quality/time/energy gates remain obligations, not outcomes.

## NE: a common source certificate needs target transfer

The fixed catalogue uses a positive trace-one filtered direct sum \(\Sigma^*=\bigoplus_\beta\sigma^*_\beta\) with four cell masses \(q=1/4\), target block \(\sigma^*_{00}=(q/2)(I+X/2)\), and other blocks \(qI/2\). The strong contract requires the same actual pre-command input \(\widetilde\Sigma\) for every candidate, setting and target trial throughout a declared validity interval, including resets and transfer after calibration/selection. An independently justified uniform per-trial bound is another possible sufficient structure. A shared preparation label alone establishes neither.

If an independent source certificate supplies

\[
d_{\rm src}=\tfrac12\|\widetilde\Sigma-\Sigma^*\|_1
=\tfrac12\sum_\beta\|\widetilde\sigma_\beta-\sigma^*_\beta\|_1\le\eta_P,
\]

then the same exact block unitary \(V_{j,c}\) acting on actual and ideal inputs preserves this distance for each candidate \(j\) and setting \(c\). The already admitted complete-POVM contraction and complementary effect-error bound give row total variation at most \(\eta_P+\eta_Q\), at their proved scope. This reuses those results; it does not absorb physical command error, clock error, response-support failure, unmodeled loss or readout drift.

A weaker stable candidate-indexed input \(\widetilde\Sigma_j\), with one candidate-blind source admission rule sound under each law, suffices for the one-world risk theorem. It does not prove equality of counterfactual sources. The strong simultaneous input premise, or an independent all-candidate bound, is needed to promote one deterministic source number to the simultaneous family claim.

The transfer counterexample is finite and explicit: an earlier certified preparation equals \(\Sigma^*\), but a later target preparation replaces its target block by \(qI/2\). The certified distance is zero, while the target distance is \(q/4=1/16\). All four target blocks are maximally mixed, so the ideal eight cell/sign outcomes each have probability \(1/8\) under either candidate at every retained setting. A certificate on the earlier preparation cannot control this target without transfer. Equality of rows alone requires a common sampler/metadata law to become equality of full record laws.

Let \(B\) be the externally supplied candidate-blind source admission and \(A\) the effect admission. Require false-admission bounds on the actual joint selected process, for each true candidate \(j\):

\[
P_j(B\cap\mathrm{source\ bad})\le\delta_{\rm src},\qquad
P_j(A\cap\mathrm{effect\ bad})\le\delta_{\rm cal}.
\]

Budgets and rules are fixed before source, effect or target data and are not fitted to tested target outcomes. On good admitted states, require the inherited target guarantee conditional on the full pretarget information, including both certificates and true source/effect/command nuisance. In its stated scope, \(e=\eta_P+\eta_*<3/1280\), \(h=3/320-4e>0\), threshold \(t=9/64\), and \(N=\lceil8/(\delta_{\rm tgt}h^2)\rceil\) samples per setting are used. Here \(\eta_*\) bounds the admitted actual effect error. The two conditional setting means must have a signed-sum mean at least \(t+h\) under the first candidate and at most \(t-h\) under the second; each sample mean must have conditional variance at most \(1/N\). Conditional Chebyshev and a union over the two settings then give target error at most \(\delta_{\rm tgt}\). An unconditional tail bound does not automatically survive selection.

Split accepted-and-wrong outcomes into bad-source, bad-effect and jointly good parts; integrate the conditional target bound on the last. Then

\[
P_j(B\cap A\cap\mathrm{wrong})\le
\delta_{\rm src}+\delta_{\rm cal}+\delta_{\rm tgt}.
\]

Independence of \(A\) and \(B\) is unnecessary, and mutually exclusive candidate worlds do not introduce a factor two. This is an unconditional accepted-and-wrong bound. It gives neither the same error conditional on acceptance, an acceptance rate nor physical identification. Source certification, reset/command transfer, control/readout, conditional target sampling and physical clock/time/action/energy inputs remain absent. Source preparations/readouts, resets and transfer checks must be charged in addition to the inherited \(32n_{\rm cal}+2N\) preparations/readouts; no source cost or numerical source risk is established.

## CE and measurement: retained blockers

CE's documented footprint-triggered fatal-memory policy and launch configuration remain a candidate. Footprint and resident memory are different metrics. A callback after crossing a threshold does not establish an instantaneous RSS bound of at most 256 MiB before import, no overshoot, installed-system applicability, adequate entitlements or a durable post-kill receipt. Mutable main-branch source locations are not immutable installed-version pins. The bounded search is not universal impossibility. The original CPU 10 s, wall 30 s, one-process/no-children, output 140 KiB, no-network, cleanup and failure-evidence limits remain; no trusted-controller process-count amendment is adopted. The next prerequisite is an exact runner contract or an explicitly adopted reviewed alternative. Benchmark, native, hardware, GPU, AI and distributed execution remain unadmitted.

Measurement retains the conditional relation design: actual selected role/address, its containing mapped image, same-image UUID, authoritative current-cache membership, coherent lifetime/epoch, target applicability and complete manifest matching compose under their stated hypotheses. This is not necessity for every possible alternative design. An outer interval 1000..2000 can contain a hole 1200..1800 and a non-cache target 1500, so extent alone cannot bind the selected image/UUID to the current cache. Paths, category flags and independently obtained UUID endpoints also need correspondence premises. The missing input remains an applicable versioned selected-image/current-cache membership and safe-composition contract. Mutable private-header declarations, before/after matches or historical availability do not establish installed applicability, pointer safety, lifetime or absence of ABA rebinding. Conditional residual hypotheses do not replace actual same-invocation B1. Selected-role, source/build/R1, record/image/process/resource and failure-before-contrast requirements remain. No acquisition, integration, compile, native call, test or observed calculation is admitted.

## Process, custody and current directions

Root dispositions accept QR, E and NE at the conditional scopes above. Current pinned bytes establish present identity; they do not reconstruct historical custody, repair missing evidence or prove physical validity. The full historical suffix of each of the four private and four public coordinator fronts is preserved byte-for-byte beneath a current-status prefix. The public manifest records the report and four public fronts and excludes itself. New checkpoint prose contains no private source paths, account identifiers or raw administrative receipts.

The retained limits are material: QR's five author guard brackets and declared freeze are consistent with its budget but do not exhaustively prove all write times; RI1401's late freeze, missing original RI1389 evidence and the legacy helper's zero-count schema limitation remain. E's earlier review clocks at 11:28:55–11:28:56 UTC bracket the usage observation, not subsequent hashing or file-write completion; the root clarification supersedes the stronger historical wording. Earlier E author guard bodies outside the packet remain attributed transcript evidence. NE's six raw author observations and recorded approximately 241.7 seconds describe retained evidence, not every unseen act; its review's first concurrent clock is not a strict start/end bracket, and NE-C010/011 gaps remain. CE retains the failed patch/freeze-repair history, mutable-version limitation and five raw guards lacking paired clocks. Measurement's reported 7m17 elapsed lacks a separate active-time record: six-active-minute compliance is not certified; neither invented idle deductions nor a measured active overrun is inferred. Later review and available capacity do not retroactively extend author budgets.

Next directions are bounded questions, not new accepted results: QR may examine a summable law allocation; E may examine service-region invariance; measurement may optionally examine fixed-17-window rank interpretation and a post-selection counterexample. Any resulting packet needs its own review and root disposition. NE remains closed at this conditional design until an independently reviewable physical source/calibration/transfer and resource input exists. CE remains blocked on strict RSS admission. No generic norm-reduction successor, blind restricted-source retry or repeated scientific replay is implied.

Option B/Status M, operational ABSTAIN, zero production qualification, protected validation, held-out requirements, all resource controls, the shared 10% remaining-usage stop and RET-only pause remain. Documentation publication does not lift the operational pause. No threshold waiver, physical calibration, execution result or new successor finding is part of RI1406.
