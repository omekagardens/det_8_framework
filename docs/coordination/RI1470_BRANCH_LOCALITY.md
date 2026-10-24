# RI1470: What a stronger branch-locality rule would require

Accepted RI1469 proves a conditional equivalence. In a supplied fixed commuting instrument family, requiring the second empty-precursor branch probability to ignore the first bit for every preparation is equivalent to scalar effects. Complete finite records then carry no information about the initial payload. The result still permits biased marks and disturbing state updates.

This proposed rule is stronger than the original restriction on q. It is not adopted here as a DET postulate or a statement of physical locality.

## 1. Fixed model and the proposed rule

A record C=(P,r) is a naturally labeled finite order with immutable binary marks. A birth appends a maximal vertex above a downward-closed ideal S, including empty and full ideals. Keep an admitted positive scalar law q(P,r,S), normalized over every ideal, transported-equivariant and satisfying complete marked scalar diamonds through its existing finite horizon N>=2. For a proper S, q may read the entire unmarked parent but only the marks in S.

The original model has branch q(P,r,S)D/2: fair bits and a passive positive-semidefinite payload D. It remains unchanged. These premises are supplied in the [Native theorem package excerpt](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), lines 64–104, with admitted coefficient scope retained at line 141.

The alternative from accepted RI1467, presented in [RI1468](RI1468_PAYLOAD_LAW_BOUNDARY.md), supplies a finite complex matrix algebra, common payload identifications, and fixed complex-linear completely positive maps I_0,I_1. They do not depend on parent, precursor or marks. Their sum Phi is trace preserving, and

    B_(S,b)^C(D) = q(C,S) I_b(D),
    Pr(S,b | C,rho) = q(C,S) Tr[I_b(rho)]

for normalized PSD rho. The matrix carrier, instrument and trace rule are premises, not native derivations. Write 1 for the matrix identity and E_b=I_b^*(1) for the trace-dual effects. Then E_b>=0 and E_0+E_1=1.

Assume universal complete marked diamonds on arbitrary PSD inputs. At the empty base, equal empty precursors and N>=2 give two routes with the same positive scalar coefficient multiplying I_c I_b and I_b I_c. Cancellation, the PSD span and complex linearity give superoperator commutation. This uses full unnormalized maps, not a selected source or normalized outputs. Commutation conversely supplies complete diamonds, including equal/full first precursors and every transported suffix within N. It is algebra on one shared carrier, not spacetime separation.

The first birth has only the empty ideal, so its q factor is one. Define

    a_b(rho) = Tr[I_b(rho)],
    J_bc(rho) = Tr[I_c I_b(rho)],       b,c in {0,1}.

For a_b>0, the residual state after the first bit is rho_b=I_b(rho)/a_b. At the one-vertex parent, proper-mark locality gives an actual empty-ideal factor

    gamma = q(P_1,r_b,empty),       0<gamma<1,

independent of b because the selected precursor contains no marks. Positivity and normalization fix the full-ideal factor as 1-gamma. No numerical gamma is chosen. The complete conditional empty-precursor branch probability is

    Pr(S_2=empty,c | b,rho) = gamma J_bc(rho)/a_b(rho).

Original q-only locality constrains gamma. It does not constrain the different residual payloads in J_bc/a_b.

**Proposed rule RL:** for each tested initial rho and each c, J_bc/a_b is the same for all first bits b with a_b>0. The common value may initially depend on rho. No conditional is assigned to an impossible first branch.

Since gamma is common and positive, RL is exactly independence of that complete empty-precursor branch probability from the unselected first bit. It compares different residual states as well as marks. That comparison is an added premise.

## 2. A symmetric two-mark law, including zero rows

CP makes J nonnegative. Commutation gives J_bc=J_cb, while trace preservation gives

    sum_c J_bc = Tr[Phi I_b(rho)] = a_b,
    sum_b a_b = 1.

Symmetry therefore gives the other marginal, sum_b J_bc=a_c. Both mark marginals equal a, although Phi(rho) need not equal rho. Neither an invariant preparation nor Phi=id is assumed.

Under RL, choose a conditional vector g from any positive row; one exists because the first probabilities sum to one. Every positive row satisfies J_bc=a_b g_c. If a_b=0, the positive matrix I_b(rho) has zero trace and is zero, so that entire J row vanishes. Thus the same factorization holds on zero rows without division. Summing over b yields g_c=a_c, hence

    J_bc(rho) = a_b(rho) a_c(rho).

Conversely this product identity gives RL wherever its conditional is defined. With just one positive first branch RL is vacuous, but symmetry and normalization still imply the product identity. Strictly positive effects are not required.

## 3. The all-preparation equivalence

Suppose RL holds for every normalized PSD preparation. Set a=a_0. Both a(rho) and J_00(rho) are affine functions of rho; the preceding identity gives J_00=a^2.

Take any two preparations rho,sigma and an interior mixture tau=t rho+(1-t)sigma, 0<t<1. Applying that identity at both endpoints and the mixture gives

    t a(rho)^2 + (1-t) a(sigma)^2
      = [t a(rho)+(1-t)a(sigma)]^2,

so

    t(1-t)[a(rho)-a(sigma)]^2 = 0.

Thus a is a constant lambda_0 on the whole state space. Since a_1=1-a_0, the other expectation is lambda_1=1-lambda_0. Testing all pure states against the Hermitian difference E_b-lambda_b 1 shows

    E_b = lambda_b 1,
    lambda_b>=0,       lambda_0+lambda_1=1.

For sufficiency, globally scalar effects give Tr[I_b(D)]=lambda_b Tr(D) for every PSD D. Consequently J_bc=lambda_c a_b=lambda_b lambda_c on normalized inputs, including zero boundaries. RL follows on every positive first branch.

Therefore, within the stated fixed commuting, trace-preserving family at N>=2,

    RL on every normalized PSD preparation
        iff both effects are scalar multiples of 1.

The sufficiency trace calculation does not itself need commutation; commutation is retained as the family premise supplying complete growth diamonds. Necessity does not apply unchanged without the fixed-map, universal-input, commutation and preparation-domain hypotheses.

The mixture argument initially allowed the conditional g to depend on rho. Its constancy was derived, not inserted into RL.

## 4. Exactly what preparation coverage is needed

The affine-square step needs two tested endpoints and one tested interior mixture under the same instrument contract. On a convex tested domain it forces constant a_b on that domain. Global scalar effects additionally require full state-space coverage, a domain with full affine span of the trace-one Hermitian hyperplane, or equivalent effect-separating access.

For the affine-span claim, differences of tested states span the traceless Hermitian space. Constant expectation makes E_b orthogonal to each such direction, so it is a multiple of 1; the known constant fixes that multiple. Convexity alone gives no global conclusion on a smaller span.

Constant expectation on a restricted initial set is only a necessary consequence here. It is not asserted sufficient for the conditional law at residual states outside that set, and no arbitrary-family classification is claimed. Preparing a mixture or ignoring its component label is not physically derived. Conditioning on a retained component label is a different experiment.

## 5. Complete records versus payload updates

For any natural marked history h=(S_1,b_1,...,S_n,b_n), n<=N, retain its actual marked prefixes:

    w_q(h) = product_(j=1..n) q(P_(j-1),r_(j-1),S_j),
    B_h(D) = w_q(h) I_(b_n) ... I_(b_1)(D).

Scalar effects allow successive trace extraction, giving

    Pr_rho(h) = w_q(h) product_(j=1..n) lambda_(b_j).

All old-mark dependence stays inside w_q. Complete rows normalize and zero histories remain included. At each positive prefix the next branch probability is q(P,r,S)lambda_b, so forbidden mark dependence cannot re-enter through the payload at a proper precursor. The whole finite marked record law is independent of initial rho for fixed q, instrument and initial record. No continuation or larger horizon is added.

If lambda_b>0, T_b=I_b/lambda_b is completely positive and trace preserving (CPTP). It is the normalized conditional update and may disturb the state; the chosen maps must still obey the assumed commutation. If lambda_b=0, every positive output has zero trace and vanishes. PSD span and complex linearity then make I_b the zero map. Its branch has no normalized conditional state.

For supplied Z=diag(1,-1), consider

    I_0(D)=lambda_0 D,
    I_1(D)=lambda_1 ZDZ.

These commute and have scalar effects for any nonnegative weights summing to one. Half weights obey RL and are fair, but ignoring the bit gives dephasing and a selected bit-one branch applies Z. For example Z changes the plus-state projector to the minus-state projector. Weights 1/3 and 2/3 also obey RL, with biased marks.

Scalar effects fix probabilities; scalar maps lambda_b id fix the full payload action. Fairness adds lambda_b=1/2. RI1467's stronger CP premise Phi=id forces scalar maps by its rank-one Choi-support theorem; RL does not impose that premise.

## 6. Exact weak-filter failure and its endpoints

Use supplied 0<eta<1 and

    u=(1+eta)/2,       v=(1-eta)/2,
    K_0=diag(sqrt(u),sqrt(v)),
    K_1=diag(sqrt(v),sqrt(u)),
    I_b(D)=K_b D K_b^dagger.

The effects are diag(u,v) and diag(v,u), summing to 1. The diagonal Kraus operators commute, so the outcome maps commute. Original q-only locality, normalization and complete growth diamonds still hold, with nonscalar effects.

At rho_*=1/2, both first bits have probability 1/2 and the normalized residuals are diag(u,v) and diag(v,u). Direct multiplication gives

    J_00=J_11=(1+eta^2)/4,
    J_01=J_10=(1-eta^2)/4,
    Pr(c=0 | b=0,rho_*)=(1+eta^2)/2,
    Pr(c=0 | b=1,rho_*)=(1-eta^2)/2.

The conditional mark contrast is eta^2>0. The complete empty-precursor branch contrast is gamma eta^2>0.

Every growth factor is accounted for: the first is one, and complete second-birth probabilities are gamma J_bc for the empty ideal and (1-gamma)J_bc for the full ideal. Summing both ideals and both bits gives one. The full ideal selects the first mark, so its comparison is not the forbidden-mark test. Gamma is the existing q slot, not an adjustable new coefficient.

For strict eta the Kraus operators are invertible, so every finite structurally allowed history is positive on nonzero PSD input. At eta=0 the maps are id/2 and the contrast vanishes. At eta=1 they become projectors: on rho_* both first conditionals still exist, the mark contrast is one, and mixed-bit two-step histories have zero weight. On a pure eigenstate one first branch is impossible and has no conditional. Positive q does not remove quantum zero branches.

This example fails proposed RL while retaining the original q-only restriction and complete diamonds.

## 7. Why passing pure sources does not settle RL

For the same strict weak filters, let rho_0=|0><0|. Both branches are positive and leave its normalized state equal to rho_0. Every subsequent bit therefore has probabilities (u,v), independent of earlier bits, and full history weights are w_q(h)u^(n_0)v^(n_1). RL holds at this source despite nonscalar effects.

At rho_1=|1><1| the same argument gives probabilities (v,u). Each singleton and the nonconvex pair {rho_0,rho_1} pass source-specific RL, yet have different mark probabilities. Their equal mixture is rho_* and fails by the preceding contrast. Even a singleton is convex, illustrating why affine-span information matters.

A passing test at the two endpoints does not supply the mixture test. None of these mathematical states or mixtures is thereby established as physically available.

## 8. Credit, scope and custody

RI1467 supplies the alternative instrument family and its complete-map/history conclusions. The supplied [QR-05A excerpt](../validation/qr-05a-quantum-births-2026-09-05/README.md), lines 7–105, already contains q-times-instrument fixtures, arbitrary-input map comparisons and full-history transport on a borrowed shared qubit. The [QR_MAP RI-08c excerpt](../track_b/QR_MAP.md), lines 413–431, instead uses prescribed effects, source-cone range and repeatability with restricted preparation reachability. Those distinct premises remain unproved from DET. Standard affine and probability identities are mathematics, not new native physics. Links identify the supplied excerpt sources; their full originals were not retrieved.

What closes is a conditional equivalence and a counterexample, not a reason to adopt RL. Carrier/instrument/trace-rule selection, preparation and mixture access, physical readout, accessible labels/marks, and justified observation/rival contracts remain missing. No q table, new horizon, seventh birth, native clock, physical locality, full QM, geometry/gravity, agency, RI1451 escape or empirical/application advantage follows. The original scalar model remains unchanged.

Source custody retains the unwritten 13,284-byte report-cap failure and final 12,189-byte report/5,809-byte premises. Author completion 16:05:57 UTC is supported-chat attribution, distinct from preparation 16:05:32; reviewer completion 16:55:58 is supported-message attribution. Original final receipts absent from this grant are not reconstructed. Recovered root context clipping, reviewer outer display clips and TextEncoder preflight failure, inherited cap/patch/display/schema/missing/late/manifest-pin-basis and cursor-reset qualifications remain. Current identities do not certify historical completion.

Measurement/E/NE/CE actual operational inputs remain absent. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, shared 10% stop/reset, RET-only pause and all physical/execution gates remain. The next approximate-locality question has no accepted answer here.
