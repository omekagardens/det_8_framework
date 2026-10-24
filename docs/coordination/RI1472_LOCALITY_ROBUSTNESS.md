# RI1472: Robustness of a proposed branch-locality rule

Accepted RI1471 gives conditional error bounds for a supplied fixed instrument. A small two-mark joint defect controls the difference between first-mark probabilities at tested preparations and their mixture. A uniform defect bound over the whole state space makes the instrument's effects close to scalar effects, with a square-root error bound. Neither conclusion makes the state updates passive or the marks fair.

The distinctions between a joint defect, a conditional contrast and a growth-weighted branch defect are essential. Rare branches can have a small joint defect and a substantial conditional contrast. These are mathematical bounds under explicit preparation coverage, not confidence statements about observed data.

## 1. Family, locality rule and complete two-birth law

Keep an admitted positive marked scalar law q(C,S), where C=(P,r) is a finite naturally labeled order with immutable binary marks and S is a downward-closed ideal. Every ideal, including empty and full, is eligible; the complete row sums to one. For proper S, q may depend on the whole unmarked parent but only the selected marks. It is transported-equivariant and satisfies complete marked scalar diamonds through an existing finite horizon N>=2.

The original branch q(C,S)D/2, with a passive PSD payload D and independently fair bit, is unchanged. The [Native theorem package](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), supplied lines 64–104 and 141, provides this model and its admitted coefficient boundary. No numerical table or larger horizon is constructed here.

The alternative family supplies a finite complex matrix algebra, common carrier identifications, two fixed complex-linear completely positive maps I_0,I_1, and the trace probability rule. The maps are independent of parent, precursor and marks. Their sum Phi is trace preserving, with

    B_(S,b)^C(D) = q(C,S) I_b(D),
    Pr(S,b | C,rho) = q(C,S) Tr[I_b(rho)]

for normalized PSD rho. Universal complete marked diamonds on arbitrary PSD inputs, applied to equal empty precursors at the empty base, have the same positive scalar factor on both routes. Cancellation, PSD span and complex linearity imply I_0 I_1=I_1 I_0. Commutation supplies the corresponding complete map diamonds within the existing horizon. This is an algebraic shared-carrier assumption, not spatial separation.

Write 1 for the matrix identity. The effect E=I_0^*(1) satisfies 0<=E<=1, and the other effect is 1-E. Define

    a(rho) = Tr[I_0(rho)] = Tr[E rho],
    J(rho) = Tr[I_0 I_0(rho)],
    W(rho) = J(rho)-a(rho)^2.

For J_bc=Tr[I_c I_b(rho)], CP gives nonnegative entries, commutation gives symmetry, and trace preservation gives row sums (a,1-a). Symmetry gives the same column sums. No stationarity Phi(rho)=rho, or identity channel Phi=id, is needed. The entire joint law is

| First bit / second bit | 0 | 1 |
| --- | --- | --- |
| 0 | a²+W | a(1-a)-W |
| 1 | a(1-a)-W | (1-a)²+W |

For 0<a<1 the signed conditional contrast is

    D(rho) = Pr(0 | first 0,rho)-Pr(0 | first 1,rho)
           = J/a-(a-J)/(1-a)
           = W/[a(1-a)].

In particular |D|<=1. The total variation distance from the product of the two marginals, using TV=(1/2) sum of absolute entry differences, is 2|W|. No sign restriction on W is used in these bounds.

At a=0, the PSD matrix I_0(rho) has trace zero and is zero. Its joint row and, by symmetry, its column vanish; only the 11 atom remains. At a=1 the corresponding statement leaves only the 00 atom. Thus W=0 at both endpoints. D is undefined there: an impossible first branch has no conditional, and no value is inserted by continuity.

The proposed stronger rule RL requires the second mark distribution to be independent of the first bit, on all positive first branches for each tested preparation. For interior a it is D=0, equivalently W=0. With only one positive first branch the comparison is vacuous and W=0 still follows. RL is an additional proposed premise, not the original q-only restriction. Its exact all-preparation equivalence with scalar effects is established in [RI1470](RI1470_BRANCH_LOCALITY.md), presenting accepted RI1469.

Every growth slot remains explicit. The first birth has only the empty ideal and q=1. At the one-vertex parent,

    gamma = q(P_1,r_b,empty),       0<gamma<1,

is independent of b because the proper precursor selects no marks. The full-ideal factor is 1-gamma. The complete second-birth probabilities are gamma J_bc for the empty ideal and (1-gamma)J_bc for the full ideal, summing over both ideals and both bits to one. The empty-branch conditional contrast is gamma D; its weighted joint-cell defect is gamma W. The unweighted joint TV is 2|W|, not |W|. Positivity of gamma supplies no numerical lower bound. The full ideal selects the first mark and is not the forbidden-mark comparison.

## 2. Converting error statements

For nonnegative caps delta and epsilon, at an interior preparation,

    |D|<=delta  implies  |W|<=delta a(1-a)<=delta/4,
    |W|<=epsilon implies |D|<=min(1,epsilon/[a(1-a)]).

A separately justified floor kappa<=a<=1-kappa, with 0<kappa<=1/2, gives the denominator lower bound kappa(1-kappa). Without such a floor, small absolute W alone need not make D small.

Likewise, |gamma D|<=beta gives |D|<=beta/gamma, and |gamma W|<=epsilon_branch gives |W|<=epsilon_branch/gamma. Combine these with probability caps where applicable. A lower bound on gamma and a lower bound on a(1-a) solve different denominator problems. Neither follows quantitatively from strict positivity alone.

These caps concern exact mathematical probabilities under one specified instrument. Translating finite observations into them would require a justified observation model, sampling design, uncertainty analysis and preparation contract, none supplied here.

## 3. The three-preparation identity

Let rho and sigma be two preparations and tau=t rho+(1-t)sigma, with 0<t<1, under the same fixed instrument. Both a and J are affine. Expanding the square in W=J-a² gives the exact identity

    W(tau)-t W(rho)-(1-t)W(sigma)
      = t(1-t)[a(rho)-a(sigma)]².

If all three absolute defects are bounded by epsilon_tau, epsilon_rho and epsilon_sigma respectively, then

    |a(rho)-a(sigma)|
      <= min(1, sqrt(
           [epsilon_tau+t epsilon_rho+(1-t)epsilon_sigma]
           /[t(1-t)] )).

For an equal mixture and a common cap epsilon this becomes min(1,sqrt(8 epsilon)). The triangle bound is sufficient; no assertion of optimal constants is made. Conditional caps can be converted separately to epsilon_i=delta_i a_i(1-a_i) at interior states. Endpoint W=0 is exact and needs no undefined D.

The identity requires the mixture's defect bound as well as the endpoint bounds. It cannot be obtained from endpoint observations alone. Ignoring a mixture's component label describes a different experiment from conditioning on that retained label.

This is initially a finite-pair statement. A convex tested domain supports the same pairwise conclusion within that domain. A domain lying in a smaller affine span does not identify an effect on the whole matrix state space. Even a finite spanning family with nonzero errors needs quantitative reconstruction geometry and conditioning before a global bound can be claimed. No finite-source global certificate is asserted.

## 4. Uniform full-state bound and its limits

Assume the stronger hypothesis |W(rho)|<=epsilon for every normalized PSD rho. Let m and M be the least and greatest eigenvalues of the Hermitian effect E. Corresponding pure eigenstates and their equal mixture are covered, so the preceding identity gives

    M-m <= min(1,sqrt(8 epsilon)).

For lambda_*=(m+M)/2, spectral calculus gives the best scalar approximation in operator norm:

    min_lambda ||E-lambda 1|| = ||E-lambda_* 1||
      = (M-m)/2 <= min(1/2,sqrt(2 epsilon)).

Here m,M and lambda_* lie in [0,1]. The complementary effect has the same distance with scalar 1-lambda_*. This proves the claimed uniform conclusion without requiring a sign theorem for W.

If instead |D(rho)|<=delta uniformly at every state where 0<a(rho)<1, the endpoint result W=0 completes the uniform bound |W|<=delta/4. Therefore

    min_lambda ||E-lambda 1|| <= min(1/2,sqrt(delta/2)).

These are sufficient bounds, not a sharp-constant theorem. The premise ranges over the entire state space, not merely the preparations available in a proposed experiment.

Scalar effects fix probabilities, not state updates. For supplied Z=diag(1,-1), the maps I_0=lambda_0 id and I_1(D)=lambda_1 ZDZ commute and have scalar effects for any nonnegative weights summing to one. They can disturb a state; unequal weights give biased marks. Thus even W=0 everywhere does not certify passive maps or fairness. Approximate scalar effects do not establish map closeness or a length-uniform approximation of complete histories. No auxiliary all-length process or exchangeability representation is proved here.

## 5. Weak filters: full-state maxima and square-root order

For supplied 0<eta<1 set

    u=(1+eta)/2,       v=(1-eta)/2,
    K_0=diag(sqrt(u),sqrt(v)),
    K_1=diag(sqrt(v),sqrt(u)),
    I_b(D)=K_b D K_b^dagger.

These CP maps commute and their sum is trace preserving. Both Kraus operators are invertible, so every finite structurally allowed history has positive quantum weight on nonzero PSD input. All scalar growth factors remain the existing q.

For any qubit density matrix with first population x in [0,1], all allowed coherences drop out of these trace expressions:

    a=v+eta x,
    J=v²+eta x,
    W=eta² x(1-x),
    a(1-a)=(1-eta²)/4+eta² x(1-x),
    D=4 eta² x(1-x)/[1-eta²+4 eta² x(1-x)].

The expression for J uses u²-v²=eta. With y=x(1-x) in [0,1/4], W and D increase with y for strict eta. Hence their exact full-state maxima, attained at x=1/2, are

    sup_rho |W|=eta²/4,       sup_rho |D|=eta².

The weighted empty-branch maxima are gamma eta²/4 and gamma eta² respectively. Full-ideal weights still use 1-gamma.

The effect is diag(u,v), so its best scalar is 1/2 and its operator-norm distance is eta/2. Exactly,

    distance = sqrt(sup |W|) = (1/2)sqrt(sup |D|).

As eta decreases to zero, distance/(sup |W|)=2/eta and distance/(sup |D|)=1/(2 eta) diverge. Thus no uniform linear error bound with a fixed finite constant can replace square-root order across this family. This establishes an order obstruction, not optimality of the constants in Section 4.

At eta=0 both maps are id/2, with a=1/2 and W=D=0. At eta=1 they are projectors: a=x, J=x, W=x(1-x), and D=1 for 0<x<1. At x=0 or 1 the corresponding first branch is impossible and D remains undefined. Quantum zero branches are compatible with positive q.

## 6. Rare branches and missing mixtures

A strictly positive rare-branch sequence makes the denominator issue explicit. Let eta=1-2s and x=s, with 0<s<1/2. The weak filters remain invertible, but

    a=2s(1-s),
    W=(1-2s)² s(1-s),
    D=(1-2s)²/[2(1-2s(1-s))].

As s decreases to zero, a and W tend to zero while D tends to 1/2. Every member has positive effects, whose least eigenvalue is s, but there is no common positive floor. This is a pointwise small-defect sequence at chosen preparations. Its full-state supremum is (1-2s)²/4, tending to 1/4; it is not a vanishing uniform defect and does not contradict Section 4.

For fixed strict eta, the pure population endpoints x=0 and x=1 each have W=D=0 and positive first branches. Their first-bit probabilities are v and u, respectively. Their equal mixture has W=eta²/4>0 and D=eta²>0. Both endpoints can therefore pass a source-specific test while the missing mixture fails. A singleton is already convex, showing why convexity without sufficient span cannot certify global scalar effects.

## 7. Credit, observation boundary and custody

RI1469 supplies the exact branch-locality equivalence; RI1467 supplies the conditional fixed-instrument alternative. The [QR-05A source excerpt](../validation/qr-05a-quantum-births-2026-09-05/README.md), lines 7–105, already includes q-times-instrument fixtures, arbitrary-input map comparisons and finite history transport on a borrowed shared qubit. The [QR_MAP RI-08c excerpt](../track_b/QR_MAP.md), lines 413–431, instead uses prescribed effects, source-cone range and repeatability, with restricted preparation reachability. The excerpt links identify their originals; only the supplied spans were read. None supplies the missing physical preparation and observation contract. The affine identity, probability algebra and spectral arguments use standard mathematics.

This closes a conditional robustness calculation. It does not adopt RL or derive the carrier, common identifications, instrument, trace rule, preparation or mixture availability, physical readout, accessible labels, calibration or rival/uncertainty contract. No new q table, horizon, seventh birth, native clock, physical locality, full QM, geometry/gravity, agency, RI1451 escape or empirical/application advantage follows. The original scalar model remains unchanged.

Historical custody retains the author's missing-directory recovery, unwritten 12,600-byte report-cap failure and final 12,150-byte report/5,701-byte premises, recovered author display clipping, reviewer metadata-split/display recovery, and root combined-write display recovery. Author all-four completion at 17:12:30 UTC and reviewer all-nine completion at 17:55:28 are supported chat/message attributions where original external final receipts are absent from this grant. Preparation declarations are not completion. Inherited cap, patch, display, schema, missing, late, manifest-pin-basis and completion-attribution qualifications remain; current hashes do not reconstruct historical custody.

Measurement, E, NE and CE operational/execution gates remain unchanged. CE source reconciliation is active and unaccepted; no settled textual-encoding absence is asserted here. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, the shared 10% stop/reset rule, RET-only pause and all physical/execution holds persist. The separate question of a classical mixture representation for the binary committed-record law, distinguished from residual quantum updates and the finite native q horizon, has no accepted answer here.
