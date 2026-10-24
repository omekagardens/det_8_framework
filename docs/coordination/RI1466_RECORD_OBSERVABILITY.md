# RI1466: What a finite record can distinguish

Accepted RI1465 separates component classification, statistical sufficiency and description-origin testing. The five-birth full/proper flag preserves total variation and equal-prior forced error but is not sufficient. The likelihood ratio is sufficient without revealing the selector exactly. The augmented mixture and its own marginal have identical record laws.

All conclusions are conditional finite mathematics. A specified mathematical observation channel is not a physical detector.

## 1. The complete record experiment

Use [RI1462](RI1462_HIDDEN_LAW_MIXTURE.md)'s admitted pair. A natural marked record retains birth labels, order and immutable bits; restrictions reconstruct its full history. Births append maximal vertices above actual downward-closed ideals with independent fair bits. Every ideal is positive, rows normalize, and complete maps are q(C,S)D/2 for arbitrary complex positive-semidefinite D on a common passive carrier.

Fix uncommitted z in {0,1}, initially half/half and independent of fair mark draws. Conditional laws exclude that prior. Components agree through four births. At parent four, t_0=1 and t_1=1/2 send proper q to t_z q and full a to 1-t_z+t_z a. This model and prefix are premises, not ontology-derived laws or physical preparations.

Let C be a complete natural marked four-birth record, F its unmarked parent, and mu_4(C)>0 its common probability. Put

    a(C) = q(C,F),          A = sum_C mu_4(C) a(C).

Positivity of the full and proper alternatives gives 0<a(C)<1 and 0<A<1. No numerical A is inferred from undisplayed tables.

A complete fifth record is equivalently h=(C,S,b), retaining its actual ideal and newborn bit. On this finite sample space the conditional likelihoods are

    P_0(h) = mu_4(C) q(C,S)/2,
    P_1(h) = mu_4(C) q(C,S)/4,                 S proper,
    P_1(h) = mu_4(C) [1+a(C)]/4,               S=F.

Summing both bits and every ideal gives a normalized row: P_1's proper/full totals are (1-a)/2 and (1+a)/2. Summing mu_4 normalizes both laws. They share finite positive support; anonymous or mark-erased endpoints are different experiments.

Their likelihood ratio is

    L(h) = P_0(h)/P_1(h)
         = 2,                                 S proper,
         = 2a(C)/(1+a(C)),                     S=F.

The full ratio lies strictly between zero and one. The common prefix likelihood and fair-bit factor cancel. The fixed passive payload supplies no extra component information.

## 2. Total variation and forced equal-prior error

Use TV(P_0,P_1)=(1/2) sum_h |P_0(h)-P_1(h)|. For fixed C, the proper positive differences sum over both bits and all proper ideals to mu_4(C)(1-a(C))/2. The full negative difference has the same magnitude. Therefore

    TV(P_0,P_1) = (1-A)/2.

For a randomized forced decision, let delta(h) be the probability of declaring z=0. Its equal-prior error is

    R(delta) = (1/2) sum_h
               [P_0(h)(1-delta(h)) + P_1(h)delta(h)].

Pointwise minimization declares zero on proper ideals and one on full ideals. Its two conditional errors are A and (1-A)/2, so

    R_* = (1/2) sum_h min(P_0(h),P_1(h))
        = (1-TV)/2 = (1+A)/4,
    1/4 < R_* < 1/2.

This exact fixed-pair expression is not a numerical universal rate. Positive common support prevents zero-error recovery from one record: the same atom requires opposite correct decisions. Randomization cannot remove the overlap; abstention is not identification.

Let B retain only whether the fifth ideal is proper or full:

| Law | B=proper | B=full |
|---|---:|---:|
| P_0 | 1-A | A |
| P_1 | (1-A)/2 | (1+A)/2 |

Its TV is also (1-A)/2, and B implements the same equal-prior optimum. This works because the sign of P_0-P_1 is constant in each cell. It does not establish statistical sufficiency or retention for every prior.

## 3. Why the flag is not sufficient

A deterministic statistic is sufficient when its conditional full-history law is component-independent. On finite positive common support this holds iff L is constant in each cell: divide equal conditional probabilities for necessity; cancel the constant ratio for sufficiency.

The supplied primary excerpts identify c=q(C4,C4) as the full four-chain probability and give

    c_0 = 81/1100 = 3240/44000,
    c_1 = 3231/44000.

Here i is the root bit, not z. Held rows are root-only by admitted all-mark proofs, not a reconstructed table. Fix other marks alike, the full fifth ideal and the same new bit; positivity makes both histories reachable under both components.

Within the single full flag cell their ratios are

    L_0 = 162/1181,          L_1 = 6462/47231,
    L_1-L_0 = 2(c_1-c_0)/[(1+c_1)(1+c_0)]
            = -19800/(1181*47231) < 0.

These likelihood ratios differ from the earlier locality witness's posteriors. B pools positive atoms with unequal ratios, so is not sufficient for this root-dependent pair. No failure for every constant-a baseline is claimed.

There is strict decision loss for some unequal prior. If pi is the prior probability of z=0, the optimal forced rule compares L with t=(1-pi)/pi. Choose L_1<t<L_0 and pi=1/(1+t). The two positive histories in the full cell now require opposite decisions.

More explicitly, let U and V be the positive and negative total magnitudes of pi P_0-(1-pi)P_1 within that cell. Both are positive. A full-record rule chooses separately on each sign. A flag-only rule must use a common randomized decision, whose best excess risk is min(U,V)>0. Thus equal-prior preservation must not be generalized to every prior.

## 4. A sufficient likelihood-ratio statistic

Set T(h)=L(h). For each attained t define

    K(t,h) = 1_{L(h)=t} P_1(h)/P_1(T=t).

Every denominator is positive and K is a normalized conditional distribution. On that cell P_0(h)=t P_1(h) and P_0(T=t)=t P_1(T=t). Hence K is the conditional history law under either component, and

    sum_t P_z(T=t) K(t,h) = P_z(h),             z=0,1.

This common reconstruction proves sufficiency. Since 2a/(1+a) increases strictly on (0,1), T equivalently keeps a proper tag, or a full tag with a(C). Evaluation presupposes q and access to natural labels/marks.

Sufficiency retains the record's component information; it does not recover z. Nor does it restore predictive record-fiber sufficiency, which compares identical committed records with different reachable residual states under the same future protocol. RI1462 has identical C4 and unequal z-conditioned next laws; the particular sixth-birth extension in [RI1464](RI1464_MIXTURE_LOCALITY.md) has identical C5 and empty probabilities d versus d/2, with d>0. A statistic of that same record cannot separate those residual states.

## 5. Augmented and marginal descriptions have the same record law

Now test description origin, a different question from which component generated a record. At five births the fixed augmented mixture projects to

    M_5(h) = [P_0(h)+P_1(h)]/2.

Averaging the fifth factor after four common factors gives proper 3q/4 and full 1/4+3q/4, with the same fair bit. The entire marked history law and its prefixes equal the admitted t=3/4 marginal. This does not say P_0=P_1.

At six births fix the particular conditional RI1464 construction, with its admitted positive extensions and all-mark chain premises. Write rho_n(z,C) for its augmented history mass and

    g_n(C) = sum_z rho_n(z,C).

Define child transition g_(n+1)(C')/g_n(C). Positive denominators and child-mass sums give normalized rows. Products telescope to g_n(C), exactly the projected augmented mass. Natural marked C retains its chronological past, so this is an autonomous full-record rule. Equality holds through six only; no seventh-birth transition follows.

Admission and equality of observations are separate. The five-birth marginal is admitted. At six births the conditional components remain admitted, but the marginal violates original proper-precursor mark locality. In RI1464 its empty-slot root-bit contrast is -9900d/(1343*53693)<0 for the same unmarked five-chain and empty selected marks. The augmented state includes z. The two descriptions are not both certified members of the same original unaugmented class. Excluding a rival through a locality axiom restricts the model class; it does not add an observation.

## 6. Common postprocessing and prefix stopping

For either fixed horizon H=5 or H=6, let M_H be the common complete record law. A common randomized record-only channel J gives, for every output event E,

    Pr_augmented(Y in E) = sum_h M_H(h) J(h,E)
                        = Pr_marginal(Y in E).

J must have the same rule under both descriptions and cannot inspect z or a description label. This includes sequential summaries and stopping only when they genuinely read prefixes of the fixed record, within H, without changing generation, using identically distributed independent auxiliary randomness. Include stopping time and all outputs, censoring, no-stop and abstention outcomes. A law-changing intervention or silent postselection is not this unconditional channel.

The output TV is zero. If a forced origin test declares the augmented description with probability gamma(Y), its opposite errors are 1-E[gamma] and E[gamma]. Their sum is one, so every forced rule has equal-prior average error exactly 1/2. This is distinct from the component error (1+A)/4.

No physical record access, arbitrary interventions, all-quantum-observable claim or fresh repetitions follow. Holding z across preparations and redrawing it define different joint experiments requiring separate contracts.

## 7. Attribution and limits

The supplied [RI1404 observational-boundary excerpt](RI1404_OBSERVATIONAL_BOUNDARIES_ADJUDICATION.md), lines 1–51, already proves matching observed laws and no discriminator for a different fixed four-query experiment. Its preparation and detector contract is not imported. The supplied [P4 observation-sufficiency excerpt](../track_b/native_theorem_package_v1/P4_OBSERVATION_SUFFICIENCY.md), lines 1–17, already distinguishes TV retention from statistical sufficiency; its unprovided section 6 was not read. The present contribution is the finite-selector calculation and reachable-chain obstruction, not either general theorem.

The model/coefficient/extension premises come from five supplied excerpts of the [Native theorem package](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), lines 64–104, 141, 189–190, 312–337 and 760–764. Original identities are attribution; full originals were not retrieved. No numerical A or continuation table was computed.

Native preparation/readout, justified label/mark access, grounded rival restrictions and intervention/selector-access contracts remain absent. Mathematical access supplies no physical interaction or empirical evidence, ontology selection, agency, informative QM, geometry, application advantage or RI1451 escape.

Source audits retain unwritten 6,331-byte and written 6,226-byte premises exceeding the 6,144-byte cap, including writing after a failed prewrite gate. Final premises 6,130/report 11,689 and display recovery do not erase failures. Author final 14:02:59 UTC is attributed: preparation 14:02:32 was not completion, and the original all-four receipt plus subsequent clock is absent here. Reviewer/root display recoveries and inherited cap/patch/schema/manifest-pin-basis, missing/late and completion-attribution limits remain. Current pins do not reconstruct history.

Actual E/NE/CE and measurement cost, resource, source/reset, interface, custody, qualification and observed-execution inputs remain blockers. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, shared 10% stop/reset and RET-only pause remain. The pending scalar-passivity/fairmark/nonselective-channel law-boundary question, with earlier instrument work credited, supplies no accepted answer or operational/native-QM admission.
