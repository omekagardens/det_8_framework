# RI1430: Closed growth constraints and exact sampling balance

This documentation checkpoint consolidates the accepted RI1427 common-layer constraints and RI1429 newborn-subset criterion. It supplies a self-contained account of those conditional results, not a new theorem, an existence certificate, a numerical experiment, or a physical prediction. The common-layer family is an optional restriction of the admitted native family. For a fixed pair probability it has at most one inductively feasible pair-consistent candidate; that assertion does not supply a candidate, higher-order sampling consistency, or a physical choice of the probability.

## 1. Objects and scope

A finite labelled parent order P carries a marking r. An actual ideal occurrence S of P, including the full ideal, specifies a transition: add a new maximal element above exactly S, retaining every completed old relation. Occurrences, relabellings and deletion multiplicities are counted, even when several give isomorphic types. The scalar class below has mark-independent normalized rows q(P,r,S), equivariance under transported relabelling, and independent fair newborn marking. Thus the marked branch weight is q/2. The admitted native interpretation additionally assumes the specified compatible scalar-passive whole-PSD transports and its inherited full marked ratio-sufficiency theorem. Scalar algebra alone does not establish an arbitrary transport's admissibility.

For a stopped size-N law mu_N, T_(N,k) means uniformly choose k vertices of the completed order, take its induced order, then forget labels and markings. This is sampling the completed relation, not deleting generating edges or choosing isomorphism types uniformly. Projective sampling consistency means mu_N T_(N,k)=mu_k. The newborn criterion in section 4 needs only normalized retained growth; it does not require the optional common-layer restriction or mark independence.

## 2. Explicit closed common-layer constraints

Index all finite marked parent/ideal slots by i. Fix once and for all a horizon-independent positive floor ell_i in (0,1] for every slot and work in X_ell=product_i[ell_i,1]. Every complete row is normalized. The empty-parent full slot is 1. No feasibility of a proposed floor collection is assumed. A horizon H contains parent rows of sizes 0 through H-1; any explicitly imposed diamonds have bases of size at most H-2. There is no proper-slot scale at size zero.

For a proper slot i=(P,r,S) with n=|P|>=1, let M_i=Max(P) minus S. This set is nonempty: an element outside an ideal has a maximal extension outside it. For each nonempty D subset of M_i, put

    d_(i,D) = q(P minus D, r restricted to P minus D, S),
    A_i = product over odd |D| of d_(i,D),
    B_i = product over positive even |D| of d_(i,D),
    u_i = A_i / B_i.

Use the stipulated carrier relabelling after deletion. Empty products are 1. All factors concern strictly smaller parents; full slots of those smaller parents are their actual probabilities, not 1, except for the empty row. Repeated factors remain repeated. Each finite product has a strictly positive lower bound supplied by its particular floors. Consequently u_i is positive and continuous on X_ell, and clearing B_i is valid there. This argument says nothing about zero-floor boundary points.

The common-layer recipe deliberately selects one alpha_n for every proper slot of every marked size-n parent, including different ratio components:

    q(P,r,S) = alpha_n u_(P,r,S)  for S proper,
    K_n(P) = sum over proper S of u_(P,r,S),
    q(P,r,P) = 1 - alpha_n K_n(P).

All full complements must be positive. There is no additional summable scale schedule in this definition. This is a specified subclass, not a classification of every native continuation.

Let C_n be the labelled n-chain with zero marking and z_n=q(C_n,0,C_n). The proper potentials of C_n correspond to the complete row of C_(n-1), including its full slot, because C_n has a unique maximal element. Their sum is 1, also for n=1 using the empty row. Therefore alpha_n=1-z_n. The scale can be eliminated by the explicit polynomial equations

    q_i B_i - (1-z_n) A_i = 0                    (CL_n)

for every proper size-n slot. Conversely, positive normalized rows satisfying these equations have alpha_n=1-z_n equal to the positive sum of the chain's proper probabilities. Hence 0<alpha_n<1. Division by positive B_i recovers the recipe, and normalization supplies each full complement. The equivalence uses positivity and full row normalization; neither may be dropped.

If a_n is the sum of the floors of the proper C_n slots and f_n is its full-slot floor, then

    0 < a_n <= alpha_n <= 1-f_n < 1.

An inconsistent interval simply makes that layer infeasible. These are layer-specific bounds, not a single uniform lower bound for all scales.

At a finite horizon the complete list consists of all row normalizations and floors, the mark-independence and transported-equivariance identifications, every CL_n for 1<=n<=H-1, and the fixed admitted RI1423 prefix as its rows enter. This is a finite closed linear/polynomial description in the selected scalar class. It does not hide an additional undefined locality condition. Native admissibility is supplied only under the inherited ratio-sufficiency and whole-PSD transport premises: the positive proper ratios must match the admitted prefix and the compatible component scales, and full complements remain positive. A common layer is a permitted special choice of those scales. Without that inherited theorem and transport premise, the equations describe only the scalar family.

One may explicitly add all marked diamond equations. For every parent D, old marking r, ideals S,T (equal ideals and a full first ideal included), and newborn marks b,c, they read schematically

    q(D,r,S) q(D+S,r+b,T)
      = q(D,r,T) q(D+T,r+c,S).

Here the second ideal denotes the corresponding old occurrence in the enlarged parent; it excludes the other newborn and is therefore proper. Full first branches cannot be discarded. New full complements enter subsequent boundary potentials even though these immediate second ideals are proper. The marked factors contribute 1/4 on each side; under the stated transport compatibility the assertion is about the whole PSD transport, not merely its trace. These equations are redundant under the inherited full marked ratio-sufficiency premise, but they are finite closed equations when included explicitly.

### The stopped seed and the compactness qualification

The admitted RI1423 seed has empty full weight 1. The singleton has proper potential 1 and scale 1/2, giving proper/full weights 1/2,1/2. At size two, the chain's proper potentials are (1/2,1/2), and the antichain's are (1/4,1/2,1/2). Scale 2/3 gives chain weights (1/3,1/3; full 1/3) and antichain weights (1/6,1/3,1/3; full 1/6). The empty-base diamond product is 1/2; the four ordered singleton-base products are 1/12,1/6,1/6,1/6 before the common marking factor 1/4.

After three births the unmarked law is

    (mu_3(A3), mu_3(E3), mu_3(V3), mu_3(Lambda3), mu_3(C3))
      = (1/12, 1/2, 1/6, 1/12, 1/6),

where A3 has no comparisons, E3 one comparison, V3 two comparisons sharing the lower element, Lambda3 two sharing the upper element, and C3 is the chain. Its sampled pair-chain probability is 1/2. This is a stopped three-birth check; it supplies neither a parent-size-three row nor four-birth coefficients.

For optional sampling constraints, a labelled marked history through N has weight 2^(-N) times the product of its scalar branch weights. Summing actual histories and actual sampled subsets makes each finite identity mu_N T_(N,k)=mu_k a polynomial equality. Add the desired identities to the finite constraints if full sampling consistency is the chosen restriction.

Under the same fixed floors and seed, the finite constraint sets are closed and nested under restriction: every equation uses only its own layer and earlier layers. Restriction preservation is not surjectivity of extension and does not prove any set nonempty. If every finite horizon is feasible under those same floors and seed, compactness of X_ell (equivalently a diagonal argument for these countably many coordinates) supplies a positive all-size array satisfying all finite constraints and hence its normalized history measure. Native interpretation still requires the inherited admission premises. Feasibility at every horizon, including simultaneous optional sampling constraints, remains unproved; changing the floors separately with the horizon would not establish this assertion.

## 3. Why the next result is an exact induction test

Sampling consistency is about completed unmarked orders under the actual growth law. The row geometry does not by itself force it. RI1429 separates the universal newborn sampling identity from the special common-layer scale restriction. It gives a necessary and sufficient next-step test only after specifying the corresponding prior consistency identity. It then proves that the pair part leaves no scale choice within the common-layer family.

## 4. Newborn-subset mixture, with its hypotheses

Fix n>=2 and 2<=k<=n. Draw the actual marked parent history through n, the actual next ideal/mark, and an independent uniform (k-1)-subset U of the n old vertices. Let nu_(n,k) be the unmarked law of the completed induced order on U together with the newborn: the newborn is above exactly S intersect U. This averages the actual parent and transition probabilities, including all full branches, marks and occurrence multiplicities. It is not a uniform average over order types or over potentials.

A uniform k-subset of n+1 vertices omits the newborn with probability (n+1-k)/(n+1) and includes it with probability k/(n+1). Conditional on omission its old subset is uniform; summing normalized future branches restores the actual size-n law. Conditional on inclusion its old (k-1)-subset is uniform. Since old relations were retained,

    mu_(n+1) T_(n+1,k)
      = ((n+1-k)/(n+1)) mu_n T_(n,k)
        + (k/(n+1)) nu_(n,k).                 (M)

For this particular k, assume the prior identity mu_n T_(n,k)=mu_k. Subtracting mu_k in (M) then gives

    mu_(n+1) T_(n+1,k) - mu_k
      = (k/(n+1)) [nu_(n,k)-mu_k].            (I_k)

Thus the new identity holds if and only if nu_(n,k)=mu_k. A fully sampling-consistent prefix through n extends through n+1 if and only if these newborn identities hold for every k=2,...,n. Past identities remain unchanged by retained growth. Without the corresponding prior identity for a given k, (M) still holds but (I_k) and its equivalence do not: old and newborn discrepancies can cancel.

The singleton case k=1 is automatic. The case k=n+1 samples the entire new order and is an identity, not an extra constraint; one may identify its newborn law with mu_(n+1). Consistency through size two is automatic, so n=2 is the first nontrivial next-step test. The normalized empty row merely starts the first singleton.

## 5. The pair condition and the forced common-layer scale

Write p=mu_2(C2), the probability of a comparable pair. In the strictly positive scalar class, 0<p<1. Conditional on the next actual ideal S_n, a uniformly chosen old vertex lies below the newborn with probability |S_n|/n. There are just two unmarked pair types, so

    nu_(n,2)(C2) = E[|S_n|]/n.

For n>=2, assuming prior pair consistency mu_n T_(n,2)=mu_2, the new pair identity is equivalent to E[|S_n|]=n p. No prior higher-motif identity is needed for this pair-only assertion. Applying it at every n>=2 yields all-size pair consistency from the size-two law. The comparable-pair count J_n gives the same check: J_(n+1)=J_n+|S_n|, and under prior pair consistency E[J_n]=binom(n,2)p. At n=1 the equation E[|S_1|]=p defines the initial pair parameter; it does not select p.

Now restrict to the common-layer family. Given positive normalized rows through parent size n-1, the actual size-n parent law and all size-n potentials are already determined independently of the new alpha_n. Set

    K_n(P) = sum_(S proper) u_(P,S),
    L_n(P) = sum_(S proper) (n-|S|) u_(P,S),
    D_n = E_(mu_n)[L_n(P)].

The expectation includes the actual marked histories, with the prescribed mark-independent/equivariant scalar identification where applicable. The full branch has probability 1-alpha_n K_n(P) and contributes n selected old vertices. Including that branch gives

    E[|S_n| given P]
      = n(1-alpha_n K_n(P))
        + alpha_n sum_(S proper) |S|u_(P,S)
      = n-alpha_n L_n(P),
    E[|S_n|] = n-alpha_n D_n.

For n>=1 the proper empty-ideal term n u_(P,empty) is strictly positive. There are finitely many parent states and slots at a fixed size, so 0<D_n<infinity. No limiting integrability assumption is being used. The pair balance therefore forces the unique candidate

    alpha_n* = n(1-p)/D_n.                    (F)

For n>=2, prior pair consistency and valid positive normalized new rows make (F) necessary and sufficient for the next pair identity. At n=1 it gives the row corresponding to the chosen p.

Let M_n=max_P K_n(P), over every admitted size-n parent, not just a selected type or a displayed portion of the support. This maximum is finite and positive. Since p is strictly between zero and one, alpha_n*>0. Strict positivity of every full complement is exactly

    alpha_n* M_n < 1,
    equivalently n(1-p) M_n < D_n.             (P)

Equality creates a zero full branch and fails strict positivity; a larger left side makes at least one full branch negative. The candidate must then be rejected, not renormalized or repaired by another scale while retaining pair balance and the prior rows. The chain has K_n(C_n)=1, so M_n>=1 and a feasible candidate necessarily has alpha_n*<1.

The chosen floors impose further requirements at this layer:

    alpha_n* u_i >= ell_i                 for every proper slot,
    1-alpha_n* K_n(P) >= ell_(P,full)      for every full slot.

Strict positivity (P) is not itself a certificate for the preassigned floors, much less for one horizon-independent feasible floor system.

### At most one, with no existence promotion

Fix p and start from the normalized empty row. The singleton proper/full row must be (1-p,p). If two candidates in this common-layer family have identical earlier rows, then their actual parent law, potentials and D_n coincide; (F) forces their next scale, and the complete next rows coincide. Induction proves at most one inductively feasible pair-consistent common-layer candidate for each fixed p, and consequently at most one fully sampling-consistent such candidate. This also gives at most one next common-layer extension for a specified positive pair-consistent prefix.

It does not prove existence through all sizes, uniqueness for unrelated native families or arbitrary prefixes merely sharing p, a physical selection of p, or any native universality. For 3<=k<=n, the separate tests nu_(n,k)=mu_k still have to hold under their own prior identities. They can obstruct the forced pair candidate; no additional common scale remains to repair them while preserving its pair identity and previous rows. Pair consistency does not establish higher-motif consistency.

The already accepted p=1/2 seed checks (F) without new coefficients. At n=1, D_1=1 and alpha_1=1/2. At n=2 the chain and antichain parent probabilities are each 1/2. Their (K,L) values are (1,3/2) and (5/4,3/2), so D_2=3/2 and alpha_2=2/3. The full complements are 1/3 and 1/6 and E[|S_2|]=1=2p, reproducing section 2. This finite check leaves later feasibility open.

## 6. Carried gates and evidence boundaries

The other lanes retain their actual gates. E has conditional confidence coverage, with a joint-gate correction and whole-cycle cost, time and executable-profile closure still required; no physical advantage or execution is certified. NE retains a conditional robust complete-row gap, with actual calibration, clock, resource and error certification missing. CE retains accepted repaired atomic cost projections, while explicit cycle-search scratch and transition accounting remain required; there is no host-RSS or measured-winner claim. Measurement has an adopted conditional documentary Linux criterion, with its original numerical bands and budgets unchanged; source, ABI, units, error handling, mapping, binding, qualification, controls and actual observed execution remain separate obligations. No later F004 result enters this checkpoint.

The previously accepted fixed 17-value rank interpretation remains a rank interpretation, not observed significance or a measurement qualification. Protected validation, Option B/Status M, ABSTAIN, zero qualification, scientific/custody requirements and the RET-only pause remain binding. Nothing here authorizes scientific execution, external validation, a physical prediction or a successor result.

Current source hashes establish identities at inspection, not historical possession or timely completion. Earlier timing, custody, helper, guard, draft-cap and readback failures remain part of the record, including the earlier missing-evidence, late-freeze and late-readback limitations. Current acceptance does not repair them. A declared write-start is not a completed freeze or readback; attributed completion observations remain attributed. The shared usage guard still stops work at 10% or less in any applicable window, with supported same-account reset evidence required to resume after a threshold stop. The explicit human resolution of a one-second reset discrepancy is the only such exception; it does not waive deadlines, evidence gaps or the threshold.

This preparation is for independent exact publication review and final root acceptance. The only prospective repository scope is eight prepended fronts, the public report and its public manifest; all eight historical front bodies remain byte-for-byte suffixes. Publication preserves open mathematical and empirical questions and grants no successor or execution authority.
