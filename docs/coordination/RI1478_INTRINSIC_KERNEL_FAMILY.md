# RI1478 — Intrinsic mark kernels and the two-birth mixture boundary

24 October 2026. Conditional mathematics over a declared family. The original independently fair newborn-mark law remains the admitted model. The family below changes that clause; it is neither a coordinate change nor a selected physical law.

The [native theorem package](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md) retains the admitted law, support, coordinate reconciliation and scoped exclusions. The [fixed-instrument record-mixture result](RI1474_RECORD_MIXTURE.md) concerns one common commuting instrument. The present contextual scalar family has a different premise and does not contradict it.

## Exact premises and support

Keep the supplied finite positive structural law q(P,r,S), for each eligible ideal S of a finite marked parent (P,r), at its existing horizon N>=2. Assume complete normalized ideal rows, equivariance under marked-order transport, proper-slot old-mark locality and the complete marked scalar diamond identity. Proper locality holds with the unmarked parent and the selected ideal's restricted marks fixed; it does not forbid q from reading the whole unmarked parent. All actual old-mark dependence of q is retained.

A newborn vertex is maximal, has strict past S, and receives an immutable binary mark. The admitted fair scalar law is B_(S,b)(X)=q(P,r,S)X/2 on the supplied matrix carrier. No new q coefficients, native continuation, carrier construction or physical instrument are provided here.

## A sufficient family, not a complete classification

Let K(S,r|S) be the isomorphism class of the induced marked precursor. Choose any function p0(K) strictly between zero and one, and put p1(K)=1-p0(K). It reads only K: no ambient size, stage, numerical labels, unselected marks, payload or external setting. Define

    B_(S,b)(X) = q(P,r,S) p_b(K(S,r|S)) X.

Each branch is a positive scalar identity map and therefore completely positive. Nonzero positive-semidefinite inputs have positive trace weight; zero remains zero. Summing b gives q(P,r,S)X, and summing S gives X. Successive normalized rows normalize histories. Conditional normalized payloads are unchanged. Both marks remain possible at every eligible slot; the original structural support is unchanged within the supplied horizon.

For a proper S, both q and p are independent of marks outside S. Isomorphisms preserve K and transport q, proving whole-branch locality and equivariance.

Take two incomparable newborns x over S with mark b and y over T with mark c, above an arbitrary marked base C. Neither newborn belongs to the other's precursor. The two composition coefficients are

    q(C,r,S) q(C+S,r+b,T) p_b(K_S) p_c(K_T),
    q(C,r,T) q(C+T,r+c,S) p_c(K_T) p_b(K_S).

The actual q products agree by the all-mark diamond premise. The intrinsic precursors are unchanged, so their p products agree. Thus the full unnormalized maps agree on every matrix, including off-diagonal inputs. This covers all inherited marks, all four b,c choices, S=T, and a full base precursor that becomes proper after the unrelated birth. Comparable parent/descendant swaps are outside the claim.

For a complete admitted history h the scalar is

    w_q(h) product_j p_(b_j)(K_j),
    w_q(h) = product_j q(P_(j-1),r_(j-1),S_j).

Every q factor remains. A vertex's marked strict past is unchanged by later maximal births, so the p product is intrinsic to the terminal marked order. Adjacent incomparable swaps leave identical transported marked parents and suffix contexts, including suffix ideals containing swapped vertices. Equivariance then gives equal suffix maps. Since finite linear extensions connect by these swaps, full natural-label transport follows. This is not arbitrary mark-word exchangeability.

The theorem is sufficient for this declared scalar family. It does not classify all admissible contextual operators, force the kernel choice, or supply a law beyond the admitted q horizon.

## The exact unselected two-birth table

Write a=p0(empty), and u_b=p0(singleton marked b), all strictly in (0,1). The first q equals one. Let gamma be the actual empty-slot q on a singleton parent. Proper empty-slot locality makes gamma independent of the old mark, while positivity and row normalization give 0<gamma<1 and full-slot weight 1-gamma. Gamma is an existing symbolic input, not a fitted or chosen number.

Rows denote first mark b, columns second mark c. The complete structural tables are

    J_empty = gamma * [[a*a,       a*(1-a)],
                       [a*(1-a),  (1-a)*(1-a)]],

    J_full = (1-gamma) * [[a*u0,       a*(1-u0)],
                         [(1-a)*u1,   (1-a)*(1-u1)]].

Their totals are gamma and 1-gamma. Neither has been separately renormalized after selecting a structure. Put v_b=gamma*a+(1-gamma)*u_b. Their sum is

    J = [[a*v0,       a*(1-v0)],
         [(1-a)*v1,  (1-a)*(1-v1)]].

All entries are positive. The first zero-mark marginal is a and the second is

    m = gamma*a + (1-gamma)*(a*u0+(1-a)*u1).

For Z_j equal to the indicator of mark zero, its actual covariance before assuming equal marginals is

    C = J00 - a*m
      = (1-gamma)*a*(1-a)*(u0-u1).

J00-a*a is covariance only when m=a. Equal time marginals hold exactly when a*u0+(1-a)*u1=a; in this binary table that also gives J01=J10.

## Necessary and sufficient two-birth mixture criterion

There is a probability measure mu on [0,1] whose iid Bernoulli mixture equals this entire two-birth table if and only if

    a*u0 + (1-a)*u1 = a,     and     u0 >= u1.

Here theta is the latent probability of mark zero. Necessity follows because both one-time marginals must equal integral(theta), and covariance must be Var(theta)>=0. Marginal mismatch rejects the representation regardless of covariance sign. With equal marginals, u0<u1 rejects it by negative covariance. For example, u0=u1=d different from a gives zero covariance but unequal marginals: independent differently biased marks are not an iid mixture.

For sufficiency, assume both conditions and set t=J00=a*v0. Then a*a<=t<a. Define z=t/a=v0, w=a*a/t=a/v0 and

    mu = (1-w)*delta_0 + w*delta_z.

Strict parameters give 0<z<1 and 0<w<=1. The measure has mass one, first moment w*z=a and second moment w*z*z=t. Equal marginals make J exactly

    [[t, a-t], [a-t, 1-2*a+t]],

which is the table from those moments. This is an elementary constructive two-moment argument, not a new general moment theorem or optimal-support classification. At C=0 with equal marginals, z=a and w=1, giving delta_a and u0=u1=a. Kernels on larger precursor classes remain unrestricted by this calculation.

## What is optional, and what remains local

The original fair law sets p0(K)=1/2 for every K. It passes the criterion with a=u0=u1=1/2 and witness delta_(1/2). Setting only those three values to one half does not impose fairness on larger precursors.

RI1475 supplies a construction-specific example inside the family: the empty precursor is fair; on each nonempty precursor, give probability epsilon to matching the parity of its old marks and 1-epsilon to the opposite mark, with 0<epsilon<1/2. Thus a=1/2, u0=epsilon, u1=1-epsilon. Its time marginals agree, while

    C = (1-gamma)*(2*epsilon-1)/4 < 0.

It has no iid mixture even at two births. Parity and epsilon are optional choices. The anticorrelation is ordinary classical causal response on the full-precursor branch with passive payloads; it is not quantum contextuality, Bell nonlocality or physical evidence.

For every family member, the actual empty-second-branch probabilities conditional on either first mark are gamma*a and gamma*(1-a). Proper whole-branch locality therefore survives even when the unselected conditional contrast (1-gamma)*(u0-u1) is nonzero. The earlier fixed-instrument RL equivalence required one common outcome pair and its specific empty-branch factorization. Contextual kernels do not supply that premise. A point-mass witness at two births does not restore it.

## Evidence, limits and next boundary

The authored RI1475 counterexample and RI1477 family theorem received distinct independent manual review. Current text, pins, captured source bodies, positive inventories and caps were checked separately; no scientific program, enumeration or simulation was used to establish this proof. Source context comes from coordinator-pinned model/precedent excerpts; unvisited original-source identities remain attributed. Credit for precursor-context construction belongs to the earlier QR05A work; the variance and two-moment reasoning are elementary probability.

Two-birth moment matching does not show that later contextual histories equal the abstract mixture continuation. No necessary classification of all contextual operators, native all-length exchangeability or q extension follows. A native physical prediction still needs a selected law and an explicit observation/readout, calibration and rival contract. No QM, gravity, agency, empirical advantage or RI1451 escape is established.

Comp-Sci's separate CE-F012 parser/reference source has passed independent source review and remains unexecuted. Its scope is the exact fixed V03 workload and an independently recomputed conventional oracle, not the optimized F1/I0 actors, a verified baseline or a DET-specific mechanism. Runtime/native identities, hard resource enforcement, custody and separate verification/M1 admission remain open. Measurement and E/NE still require their recorded actual operational inputs; no cross-track success supplies them.

Retain historical missing-directory recovery, unwritten draft-cap failures, clipped-display recoveries, source-version and custody limitations. Current identities cannot reconstruct historical completion; final author/reviewer completion is attributed through separately supported handoffs. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, the shared 10% stop/reset guard and the RET-only pause remain. No philosophical journal or selected Free Thinker packet is published here.
