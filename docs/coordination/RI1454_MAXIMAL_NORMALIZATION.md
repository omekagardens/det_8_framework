# RI1454: Maximal normalization and the scalar diamond

The independently reviewed, root-accepted RI1453 result tests a proposed conversion of an exchangeable completed-order law into maximal-birth growth: discard nonmaximal insertions from its ordinary extension kernel and normalize. Under full support the resulting rows are positive and normalized, but two incomparable-birth routes need not agree.

For a positive common endpoint, the two routes agree exactly when the maximal-extension masses at their intermediate parents agree. A strictly full-support comparison at lambda=999/1000 violates this condition. The pure two-level boundary has unequal masses but two zero route products, so that boundary alone is not the counterexample. The result rejects this prescription under the stated scalar-diamond requirement; it does not rule out every native implementation.

## 1. Comparison family and precise premises

Let P_n be an exchangeable law on labeled completed strict posets on [n]={1,...,n}, for every finite n. Exchangeability means that permuting sample labels preserves the law. Fixed-label restriction consistency means that restricting P_(n+1) to the old labels [n] gives P_n. Assume full labeled support except in the explicitly separated boundary calculation below. The unique empty order has probability one at n=0. These are comparison-law premises, not physical or native-growth conclusions.

The accepted family from [RI1452](RI1452_FULL_SUPPORT_COMPARISON.md) supplies a concrete background without evaluating an infinite series. Choose nonempty finite strict templates T_j, j>=1, including a representative of every finite nonempty anonymous poset. Put w_j=2^(-j). In Q_n^T, assign each sample vertex an independent uniform type tau_i in T and declare i<j exactly when tau_i<_T tau_j. Equal types stay distinct and incomparable. Template transitivity ensures that every outcome is a strict poset.

Choose one template and one orientation for the whole sample, with law

    H_n = sum_(j>=1) (w_j/2) [Q_n^(T_j)+Q_n^(T_j^op)].

The fixed nonnegative weights sum to one. The chosen component is shared across all vertices; it is not redrawn per vertex or after restriction. Conditional iid types retain their distribution under every fixed-subset restriction, and this identity commutes with the mixture. Thus H is exchangeable and exactly restriction-consistent. An independent uniform-subset average has the same restriction law. Conditional iid does not imply unconditional independence of overlapping observations.

For any particular labeled k-vertex order F, k>=1, choose T_j isomorphic to F. One fixed bijective type assignment gives

    H_k(F) >= 2^(-j-1) k^(-k) > 0.

For its anonymous type, all k! bijective assignments are disjoint type events, giving the bound 2^(-j-1)k!/k^k. These are target-dependent lower bounds, not exact values or uniform-in-size guarantees.

Let L_n be the two-level comparison: each vertex is independently lower with probability 1/3 and upper with probability 2/3; every lower is below every upper, with no within-level comparison. Fix 0<lambda<1 across sizes and define

    P_n^lambda = lambda L_n + (1-lambda) H_n.                (1)

One component is chosen for the whole order. Both components are consistent and exchangeable, so (1) is too. Its H weight is positive, giving full labeled support. The series and its template enumeration are formal definitions; no generator, numerical series evaluation or physical sampler is asserted.

For anonymous triples use A for the antichain, E for one edge plus an isolate, V for a fork with one bottom, W for a join with one top, and C for a chain. The dual-balanced H triple law is

    h=(a0,e0,u0,u0,c0),   a0+e0+2u0+c0=1,

with all four displayed parameters positive by full support. They are the exact induced triple probabilities of the declared H; their values remain unevaluated. L has triple law

    ell=(1/3,0,4/9,2/9,0).

Consequently the mixture triple law (a,e,v,w,c) is

    a=lambda/3+(1-lambda)a0,   e=(1-lambda)e0,
    v=4lambda/9+(1-lambda)u0, w=2lambda/9+(1-lambda)u0,
    c=(1-lambda)c0.                                        (2)

All entries are positive for 0<lambda<1. Only H is dual-balanced. No numerical lower bound on e0 is assumed.

## 2. Ordinary extension versus maximal normalization

For a labeled parent F on [n] and a one-vertex extension F' on [n+1] whose restriction is F, define

    K(F,F') = P_(n+1)(F')/P_n(F).

The denominator is positive under full support. The extension events partition the event of seeing F on the old labels, so fixed-label consistency gives

    sum_(F' restricting to F) K(F,F') = 1.                  (3)

This sum includes every insertion position, including nonmaximal insertions. Let M(F) be exactly the extensions in which the new vertex is maximal, and put

    s(F) = sum_(F' in M(F)) K(F,F'),
    qhat(F,F') = K(F,F')/s(F),       F' in M(F).             (4)

Every maximal extension is obtained from an ideal S of F: place the newborn above exactly S, with no successors. An ideal is downward closed, and this condition is exactly what preserves transitivity. The empty ideal, proper nonempty ideals, and the full ideal all count separately.

Full support gives s(F)>0 and positive qhat entries for every ideal. Their row sum is one. For a nonempty F, putting the newborn below every old vertex gives a valid nonmaximal extension with positive probability, hence s(F)<1. At the empty parent s=1; the strict deficit statement excludes it.

These facts make qhat a positive normalized finite Markov row prescription on maximal births. They do not yet prove preservation of the completed-order law or native admission.

## 3. Complete incomparable-birth route formula

Take any ideals S,T of F. Add x above S and y above T, with x and y incomparable. Write

    F_x=F+x_S,     F_y=F+y_T,     G=F+x_S+y_T.

Either first precursor may be the whole original parent. After adding x, T remains an ideal: a maximal newborn cannot lie below an old member of T. It excludes x and is therefore proper in F_x. The same reasoning applies to S in F_y. Thus full-first/proper-second cases belong to this diamond family and cannot be discarded.

Each route uses chronological newborn labels. Identify the endpoints by swapping those two labels. Exchangeability then supplies the same labeled endpoint mass P_(n+2)(G). For positive base and intermediate probabilities and positive normalizers, the two complete products are

    R_xy = qhat(F,F_x) qhat(F_x,G)
         = P_(n+2)(G)/[P_n(F) s(F) s(F_x)],

    R_yx = qhat(F,F_y) qhat(F_y,G)
         = P_(n+2)(G)/[P_n(F) s(F) s(F_y)].                 (5)

The intermediate P factors cancel. The unconditioned K products both equal P_(n+2)(G)/P_n(F); the extra parent-dependent normalizers cause the issue.

On precisely this positive-denominator domain,

    R_xy=R_yx
    if and only if P_(n+2)(G)=0 or s(F_x)=s(F_y).            (6)

At a positive endpoint, equality is equivalent to equality of the two intermediate maximal masses. Under full support the zero-endpoint alternative disappears, so all these scalar diamonds hold exactly when every such pair of intermediate masses agrees.

This criterion is not sufficient native admission. Without exchangeability the endpoint numerators may differ; without restriction consistency (3) is unjustified. Zero parent probability leaves the quotient undefined. “Incomparable births” means order incomparability, not probabilistic independence.

## 4. The singleton witness and actual labeled counts

Let the base be the singleton o. Add x with empty precursor and y with full precursor {o}, keeping x and y incomparable. The intermediate parents are A2 and the specified oriented chain C2:o<y. Their common endpoint is a specified E3, with o<y and isolated x.

For an exchangeable anonymous triple law (a,e,v,w,c), consistency gives pair comparability

    p=(e+2v+2w+3c)/3.

The labeled type counts of A,E,V,W,C are respectively 1,6,3,3,6, with equal mass within each type. Assume 0<p<1. A specified pair antichain has mass 1-p, and a specified chain orientation has mass p/2, not p.

The full ideal lists for the two intermediate parents are:

| Specified parent | Ideal of old parent | Maximal endpoint | Labeled mass |
|---|---|---|---:|
| A2:1 parallel 2 | empty | A3 | a |
| A2 | {1} | one edge into newborn | e/6 |
| A2 | {2} | the other labeled one edge | e/6 |
| A2 | {1,2} | W3, newborn is top | w/3 |
| C2:1<2 | empty | E3, newborn isolated | e/6 |
| C2 | {1} | V3, old vertex 1 is bottom | v/3 |
| C2 | {1,2} | chain 1<2<3 | c/6 |

These are ideal occurrences: the A2 full extension uses W, whereas the C2 bottom-only extension uses V. Therefore

    s(A2) = (a+e/3+w/3)/(1-p),
    s(C2) = (e/6+v/3+c/6)/(p/2)
          = (e+2v+c)/(3p).                                 (7)

At the singleton, maximal additions permit an incomparable pair and old<new, giving

    s1=1-p/2,
    qhat(o,A2)=(1-p)/s1,   qhat(o,C2)=(p/2)/s1.             (8)

After matching the newborn labels, the specified E3 endpoint has mass e/6. The complete route products are consequently

    R_A = e/[6 s1 s(A2)],
    R_C = e/[6 s1 s(C2)].                                  (9)

For e>0 they agree exactly when the two values in (7) agree.

## 5. The pure two-level boundary gives zero products

For L alone, p=4/9 and the triple law is ell above. The A2 numerator in (7) is 11/27 and its denominator is 5/9. The specified C2 numerator before division by its parent mass is 4/27, with parent mass 2/9. Hence

    s_L(A2)=11/15,   s_L(C2)=2/3,
    s_L(A2)-s_L(C2)=1/15.                                  (10)

Also s1,L=7/9, and the first normalized birth probabilities are 5/7 and 2/7. But e_L=0. Each required second transition into E3 has zero probability, so

    R_A,L=(5/7) times 0=0,
    R_C,L=(2/7) times 0=0.

Unequal normalizers alone do not violate this diamond. Cancelling its zero common endpoint would be invalid. This verifies only the displayed boundary diamond; it neither gives full support nor proves that every boundary diamond holds.

## 6. A positive counterexample at lambda=999/1000

Use (1) with any allowed background H and write epsilon=1-lambda. For either specified parent F=A2,C2, let D_J(F) be its pair probability and M_J(F) the probability that the old labels give F and the newborn is maximal, for J=L,H. Event containment and consistency imply

    0 <= M_H(F) <= D_H(F) <= 1.

Mixture linearity gives D_epsilon=lambda D_L+epsilon D_H and M_epsilon=lambda M_L+epsilon M_H. Since M_L=s_L D_L,

    s_epsilon-s_L
      = epsilon (M_H-s_L D_H)/(lambda D_L+epsilon D_H).

Both M_H and s_L D_H lie in [0,D_H]. For 0<lambda<1 and either positive D_L, it follows that

    |s_epsilon-s_L| <= epsilon/(lambda D_L),

    |s_epsilon(A2)-11/15| <= 9epsilon/(5lambda),
    |s_epsilon(C2)-2/3|  <= 9epsilon/(2lambda).              (11)

No background series value or numerical continuity experiment enters this bound. At the exact rational choice lambda=999/1000, epsilon=1/1000, the two errors are at most 1/555 and 1/222. Their sum is 7/1110, whereas 1/15=74/1110. Equations (10)-(11) therefore imply, uniformly over every allowed H,

    s_epsilon(A2)-s_epsilon(C2) >= 67/1110 > 0.             (12)

The bound need not be sharp. The positive H weight gives full support, including

    e_epsilon=e0/1000>0.

Thus all parent, intermediate, endpoint and normalizer factors in (9) are positive. The actual difference is

    R_C-R_A
      = e_epsilon [s_epsilon(A2)-s_epsilon(C2)]
        /[6 s1,epsilon s_epsilon(A2) s_epsilon(C2)]
      > 0.                                                (13)

Both route products are nonzero. This is the positive-endpoint counterexample; the boundary's zero-product defect is absent. The uniform normalizer gap is not a uniform positive numerical lower bound on e0 or on the route gap. Only e0>0 was needed. The rational mixture is a comparison law, not a newly adopted native law.

## 7. Changed pair law and the scope of the failure

Even before testing the diamond, the normalized prescription changes the completed-order distribution. Starting at the singleton, its anonymous chain probability is

    phat=(p/2)/(1-p/2)=p/(2-p).

For 0<p<1,

    p-phat=p(1-p)/(2-p)>0.

This changes anonymous pair probabilities, not just chronological labels; the conditioning is not law-preserving.

Positive normalized rows can define finite chronological growth laws by multiplying their entries. That elementary construction is weaker than the native requirement being tested here: (13) fails a required incomparable-birth scalar diamond, including a full first precursor.

For the declared fair-bit scalar-passive lift, the two-step payload maps carry their respective scalar products multiplied by the same factor 1/4. On a common nonzero positive semidefinite payload, unequal scalars still give unequal outputs. Those common factors cannot repair (13). This statement concerns that specific lift; no different marked or payload construction is analyzed or excluded.

The counterexample refutes an automatic passage from full-support comparison laws to scalar-diamond-compatible native laws by this particular maximal-only normalization. It does not classify every lambda, every full-support law or every alternative realization. Equality of all relevant intermediate normalizers remains the exact scalar criterion, not a proof of locality, mark equivariance, whole-payload compatibility or every native obligation. Shared latent templates can carry information about the whole parent; they do not establish precursor-record locality. Separately sorting terminal orders supplies no missing compatible coupling across sizes.

The original accepted seed, pair/triple target and t-family remain unchanged. This does not repair or strengthen the RI1447 N>=51 obstruction, establish a smaller obstruction or minimality, or supply a new all-horizon native theorem. Any further natural-label coherence or anonymous-law realization question is open here; no successor result is included.

## 8. Scientific and evidence boundaries

No physical preparation, observer, clock/readout, calibration, action/reset-cost mapping, empirical validation or execution permission follows. E retains the actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE retains source/reset/control/readout transfer, history-wise certificates in both candidate worlds and full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains packing/general serialization, source/build/ABI/binding, resource/control/qualification and observed-execution holds. The fixed nominal calculation remains separate from physical or production assurances; this publication adds no calibration or trace prerequisite to that nominal calculation.

RI1453 has a distinct author, independent review and root acceptance at the conditional mathematical scope above. The supplied review and root audits record checks of the actual ideal counts, endpoint-label cancellation, zero boundary, analytic perturbation and common fair-bit factor. Their positive historical identity counts are distinct from this publication's own literal input count and current byte checks.

Author substantive completion is recorded at 08:00:01 UTC, before its 08:07:35 cutoff. The 08:01:41 freeze declaration is not completion. Final completion at 08:02:14, before its 08:13:35 deadline, remains attributed because the original final all-four-file receipt is absent from this grant. The expected absent-directory reservation check and empty edit receipt do not independently prove earlier contents. The review's reported prose and complete-file readbacks are followed by 08:47:50 and 08:49:38, before its 08:53:16 and 08:59:16 deadlines. Present pins do not reconstruct those historical observations.

Prior over-cap drafts, clipped displays, administrative schema/patch qualifications, missing RI1389 evidence and late RI1401/RI1419 work remain history. Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% usage guard and RET-only pause remain. Publication is not execution; no commit, push or release receipt is invented.
