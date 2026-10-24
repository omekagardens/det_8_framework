# RI1474: A classical mixture for one fixed record channel

Accepted RI1473 proves that the binary record probabilities of a supplied fixed commuting instrument have a classical mixture representation. For each normalized positive-semidefinite initial matrix rho, there is a probability measure mu_rho on [0,1] such that an individual word w of length n, containing k zeros, has probability

    P_rho(w) = integral theta^k (1-theta)^(n-k) d mu_rho(theta).

There is no binomial coefficient: this is one specified word, not the sum over all words with k zeros. The measure may depend on the preparation. The theorem matches this record channel's probabilities, including their growth-weighted histories. It does not replace the conditioned residual matrices or describe experiments with changed settings.

The proof below constructs auxiliary word laws at every mathematical length from the fixed maps. Native growth remains restricted to its existing admitted horizon. No additional birth or physical repetition is authorized.

## 1. Supplied family and its native boundary

A complete record C=(P,r) consists of a naturally labeled finite order and immutable binary marks. A birth appends a maximal vertex above a downward-closed ideal S. Keep the admitted scalar law q(C,S): every ideal, including empty and full, has positive weight; the complete ideal row sums to one; relabeling transports all record data; and complete marked scalar diamonds hold through an existing finite horizon N>=2. Proper-slot weights may read the whole unmarked parent but only the marks in S.

The original branch q(C,S)D/2 has a passive PSD payload D and independently fair newborn bit. It remains unchanged. These model premises and the admitted coefficient boundary are supplied in the [Native theorem package excerpt](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), lines 64–104 and 141.

The alternative supplies a finite complex matrix algebra, common payload identifications, and fixed complex-linear completely positive endomorphisms I_0,I_1. They do not depend on the parent, precursor or marks. Their sum Phi=I_0+I_1 is trace preserving. The branch and probability rule are

    B_(S,b)^C(D) = q(C,S) I_b(D),
    Pr(S,b | C,rho) = q(C,S) Tr[I_b(rho)].

Universal complete marked diamonds on arbitrary PSD inputs, at the empty base with equal empty precursors, equate two compositions with the same positive scalar factor. Cancellation, PSD span and complex linearity yield I_0 I_1=I_1 I_0 on the full algebra. This accepted commutation premise is algebra on a shared carrier, not a statement of physical separation.

The stronger two-birth branch-locality rule RL will be defined in Section 6. It remains a proposed additional condition, not an adopted native postulate.

## 2. Auxiliary word laws

Fix any normalized PSD rho. For every auxiliary integer n>=0 define

    I_w = I_(b_n) ... I_(b_1),
    P_n(w) = Tr[I_w(rho)],       P_0(empty)=1.

These compositions exist at every finite length because the maps are fixed endomorphisms of the same algebra. Complete positivity gives nonnegative weights. Summing all words gives Tr[Phi^n(rho)]=1. Summing a final outcome gives

    sum_(c=0,1) P_(n+1)(wc) = Tr[Phi I_w(rho)] = P_n(w).

Thus these are normalized, prefix-consistent finite laws. Commutation makes them invariant under every permutation of positions. Any ordered list of m distinct positions in a length-n word consequently has law P_m: permute those positions to the first m in the chosen order, then sum the remaining suffix.

No stationarity Phi(rho)=rho, identity channel Phi=id or infinite sample space was assumed. Mere finite exchangeability at one horizon would not suffice for the argument that follows. The extension here is supplied by the fixed maps; stage-dependent, partially defined or changing-setting maps would need a different premise. No q beyond its admitted horizon is evaluated or constructed.

## 3. Finite count measures and the exact multiplicity

Let K_n count zeros under the mathematical law P_n, and for n>=1 define the probability measure

    mu_n = sum_(z=0..n) P_n(K_n=z) delta_(z/n).

These are measures defined from finite laws, not acquired frequencies or executed enumerations.

Fix a particular word w of length m with k zeros. For n>=max(1,m), use the falling factorial

    (z)_j=z(z-1)...(z-j+1),       (z)_0=1,

which vanishes for nonnegative integer z<j. In a fixed length-n population with z zeros, the probability of this pattern on uniformly sampled ordered distinct positions is

    H_(n,w)(z) = (z)_k (n-z)_(m-k)/(n)_m.

There are (n)_m possible ordered distinct-position tuples. The zero-designated positions have (z)_k assignments and the one-designated positions have (n-z)_(m-k) assignments. There is no choice of which pattern positions are zero: w already specifies them. Averaging over the law P_n and using the ordered-position marginal yields exactly

    E_(P_n)[H_(n,w)(K_n)] = P_m(w).

This unconditional identity never divides by the mass of a zero-probability count stratum. For the empty word it is the constant-one identity.

Now sample m independent uniform position indices with replacement. For the same population the pattern probability is

    f_w(z/n),       f_w(theta)=theta^k(1-theta)^(m-k).

Conditional on no repeated index, the indices are uniform among ordered distinct tuples, giving H_(n,w). Decomposing over the collision event therefore bounds |f_w(z/n)-H_(n,w)(z)| by its probability. Each pair of indices coincides with probability 1/n, so the union bound gives

    |f_w(z/n)-H_(n,w)(z)| <= m(m-1)/(2n),
    |integral f_w d mu_n - P_m(w)| <= m(m-1)/(2n).

The bound is uniform over z, is exact at m=0 or 1, and remains valid if its right side exceeds one. The limit is n tending to infinity for each fixed m. No uniform claim for growing word length or statistical confidence statement is made. Powers with exponent zero equal one, including at the endpoints, so every f_w is a bounded continuous polynomial on [0,1].

## 4. One common limiting measure

For completeness, construct the needed compactness step rather than assuming a word-dependent limit. Let F_n be the distribution function of mu_n, extended by zero below 0 and one at or above 1. Enumerate the rational numbers. Successive bounded-sequence subsequence selection and a diagonal subsequence n_j give convergence of F_(n_j)(r) at every rational r to a nondecreasing function g(r). Define

    F(x) = inf { g(r) : r rational, r>x }.

This function is nondecreasing. To see right continuity, choose a rational r>x whose g(r) is within any prescribed positive error of F(x). For y decreasing to x and eventually less than r,

    F(x) <= F(y) <= g(r).

Thus the right limit is F(x). The prescribed outside values give F=0 below 0 and F=1 at or above 1, with limits zero and one at the two infinities. The standard distribution-function/Stieltjes correspondence supplies a Borel probability mu supported on [0,1].

At a continuity point x, rational lower and upper sandwiches give

    F(x-) <= liminf_j F_(n_j)(x)
           <= limsup_j F_(n_j)(x) <= F(x).

The endpoints agree there. A monotone function has at most countably many jumps, so partitions may choose continuity-point endpoints. Extend a continuous function on [0,1] constantly a little beyond the interval, and bound its integrals by upper and lower partition sums. Uniform continuity makes their gap arbitrarily small; convergence of distribution functions at the partition endpoints gives convergence of the sums. This proves weak convergence of mu_(n_j) to mu. Endpoints outside [0,1] retain any atoms at 0 or 1; endpoint continuity is not imposed.

Apply this construction to the count measures and name its limit mu_rho. For every fixed finite word, weak convergence and the collision bound give

    integral f_w d mu_rho
      = lim_j integral f_w d mu_(n_j)
      = P_m(w).

The subsequence was selected for the measures, once. It serves all bounded continuous functions and hence every finite word, rather than producing unrelated measures for different words.

Bounded-sequence selection, countable diagonal selection, the Stieltjes correspondence and uniform-continuity partition approximation are standard probability and analysis. They are credited mathematical ingredients, not DET or physical assumptions. There is no exchange involving an unbounded integrand or an empirical limit. Existence is enough here; no uniqueness, support-size classification or optimal finite-atomic statement is claimed.

## 5. Every native growth weight survives

For a complete natural marked history h=(S_1,b_1,...,S_n,b_n), n<=N, keep its actual record prefixes and define

    w_q(h) = product_(j=1..n) q(P_(j-1),r_(j-1),S_j).

Composing the branch maps and taking their trace gives

    Pr_rho(h) = w_q(h) P_n(b_1...b_n)
      = w_q(h) integral theta^k(1-theta)^(n-k) d mu_rho(theta).

The product can depend on earlier marks and the structural history. It is not replaced by a mark-blind coefficient or discarded.

An equivalent finite classical probability construction selects theta with law mu_rho and, conditional on theta and the complete current record, assigns the next joint branch weight

    q(P,r,S) theta^(1-b)(1-theta)^b.

The ideal row and the binary factor each sum to one, including theta=0 or 1. Multiplying these weights along a history and integrating gives the same complete marked-history probability. All zero histories remain present without normalizing impossible branches. This is a representation of a finite probability law, not an implemented sampler or an assertion that nature contains a hidden bias.

For a fixed mark word, summing over all structural histories removes the q product by successive normalized rows, starting with the last structural choice. Earlier-mark feedback is retained in each prefix and does not obstruct that summation. The unselected fixed-length mark marginal is therefore P_n.

Conditioning on a structural class, applying selective stopping, or changing the coarse record can reweight the history factors. Such selected variables need not retain the exchangeable or iid form. A specified pushforward or selection based on records is matched by applying the same operation to the full represented law. Selection involving an additional payload measurement is outside the equality.

## 6. Variance, RL and preparation coverage

Put a=P_1(0), J=P_2(00) and W=J-a². The representation gives

    a=integral theta d mu_rho,
    J=integral theta² d mu_rho,
    W=integral (theta-a)² d mu_rho >= 0.

The sign is now a consequence within this fixed family. The earlier sign-free sufficient bounds in [RI1472](RI1472_LOCALITY_ROBUSTNESS.md), presenting accepted RI1471, remain valid; no optimal-constant claim is added.

For clarity, commutation makes J_bc=Tr[I_c I_b(rho)] symmetric, and trace preservation gives row sums (a,1-a). Symmetry supplies the same column sums without stationarity. The two-bit law is

| First / second bit | 0 | 1 |
| --- | --- | --- |
| 0 | J | a-J |
| 1 | a-J | 1-2a+J |

For 0<a<1 its signed conditional contrast is

    D = J/a-(a-J)/(1-a) = W/[a(1-a)] >= 0.

At the one-vertex parent the existing empty-ideal factor gamma=q(P_1,r_b,empty) lies in (0,1) and is independent of b by proper-mark locality. The full ideal has factor 1-gamma. Their joint weights are gamma J_bc and (1-gamma)J_bc. The actual empty-branch conditional contrast is gamma D. Positive q alone gives no calibrated numerical branch floor.

Proposed RL requires the second mark distribution to be independent of the first bit on every possible first branch, at the tested source. If both rows are positive, RL gives a common conditional vector; summing the rows identifies it as (a,1-a). Thus RL is equivalent to the product two-bit law, or W=0. Conversely that product law gives RL. If a row has zero probability, its PSD output has zero trace and vanishes; symmetry and normalization give the same product statement without division.

A nonnegative square has zero integral precisely when theta=a almost everywhere. Therefore, for this fixed source and unchanged instrument,

    RL iff W=0 iff mu_rho is concentrated at a
       iff all mark words have probability a^k(1-a)^(n-k).

The last formula is the iid mark law, including every admitted native length and the auxiliary word lengths. At a=0 or 1 the measure is concentrated at that endpoint already. The missing first branch remains impossible, and D is undefined rather than assigned a fictitious zero value.

Different sources may have different point masses. Fixed-source RL does not make E_0=I_0^*(1) scalar globally. On a convex preparation domain, a and J are affine; for tau=t rho+(1-t)sigma with 0<t<1,

    W(tau)-t W(rho)-(1-t)W(sigma)
      = t(1-t)[a(rho)-a(sigma)]².

If RL holds throughout that domain, the left side vanishes and a is constant there. Global scalar effects additionally require full affine-span/effect-separating access, or RL on all normalized PSD states. A convex singleton is insufficient. Mathematical preparation coverage is not proof of physical access to sources or their mixtures.

## 7. Residual states, source credit and limits

On a positive word the conditioned matrix is I_w(rho)/P_n(w). Its value is not determined by the represented trace probabilities. For supplied Z=diag(1,-1), take

    I_0(D)=D/2,       I_1(D)=ZDZ/2.

The maps commute and give P_n(w)=2^(-n), represented by a point mass at 1/2. A selected outcome-one still sends rho to ZrhoZ and can disturb it. The ignored-outcome channel need not be the identity. This classical record representation does not predict changed or noncommuting settings, interventions or further payload readouts, and is not a noncontextual model for arbitrary quantum experiments.

RI1469 supplies exact RL and RI1471 its robustness boundary; RI1473 supplies this accepted representation and variance consequence. The supplied [QR-05A excerpt](../validation/qr-05a-quantum-births-2026-09-05/README.md), lines 7–105, already has q-times-instrument fixtures and universal-map/history comparisons on a borrowed carrier. The [QR_MAP RI-08c excerpt](../track_b/QR_MAP.md), lines 413–431, has different prescribed-effect, source-cone and repeatability premises with restricted preparation reachability. Only the supplied excerpt spans were read; links identify their originals without claiming a complete original-source review.

The carrier, fixed CP instrument, common identifications and trace rule are supplied, not derived from DET. Native F/L selection, physical preparation, observation/readout, calibration and rival/uncertainty contracts remain missing. No new q table or continuation, native horizon, seventh birth, full QM, geometry/gravity, agency, RI1451 escape, empirical advantage or physical ontology follows.

Custody retains the author missing-directory recovery and inherited cap, patch, schema, display, missing/late and manifest-pin-basis qualifications. Author all-four completion at 18:08:49 UTC and reviewer all-nine completion at 18:59:31 are supported-message attributions where original external final receipts are absent from this grant. The retained reviewer prose readback precedes 18:58:34; preparation declarations are distinct from completion. Root historical display clipping and a reviewer-input schema assumption were recovered before disposition. Current hashes do not reconstruct historical timing.

Measurement/E/NE actual-input gates and CE implementation, runtime, hard-resource, M1 and DET-distinct-arm gates remain. CE canonical source reconciliation has passed; the F010 actor-input contract has not been adopted. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, shared 10% stop/reset, RET-only pause and physical/execution holds persist. The prospective question about intrinsic-past-dependent instruments retaining diamonds while escaping this fixed-instrument conclusion is a candidate direction only, with no answer adopted here.
