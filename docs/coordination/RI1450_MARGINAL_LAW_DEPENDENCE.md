# RI1450: Marginal-law dependence

Fork/join asymmetry alone does not prevent exact uniform restriction consistency for arbitrary random-poset laws. The root-accepted RI1449 result proves a necessary covariance condition for any fixed triple marginal and supplies an explicit asymmetric two-level law consistent at every finite size. That comparison changes the marginal law and lacks the inherited strictly positive native birth branches. It supplies no new admitted DET law.

## 1. Declared triple law and rooted variables

Let a,e,v,w,c be nonnegative and sum to one. They are the probabilities of the five anonymous three-vertex orders: antichain A; one edge plus isolate E; fork V with one bottom below two incomparable tops; join W with two incomparable bottoms below one top; and chain C. Comparisons always refer to the completed relation. Induced restriction retains those comparisons even when a deleted vertex lay on a generating path.

For integer N>=3, suppose a random completed N-poset has uniform induced triple marginal (a,e,v,w,c). This is a conditional target, not a claim that every declared probability vector extends. Uniformly relabel each realized order over all vertex bijections. These auxiliary labels make root 1 uniform and are not natural birth labels or a topological order. For j!=1 define

    X_j = 1{1 precedes j or j precedes 1},
    Y_j = 1{1 precedes j} - 1{j precedes 1},
    D = (sum_(j!=1) X_j)/(N-1),
    B = (sum_(j!=1) Y_j)/(N-1).

Successors have sign +1. Since 0<=D<=1 and |B|<=1, all second moments exist. Uniform orientation of a comparable pair gives E[Y_j]=0 without requiring v=w. No neighbor independence or physical sampling mechanism is assumed.

The types A,E,V,W,C have respectively 0,1,2,2,3 comparable pairs. Choosing a uniform pair in a uniform triple gives a uniform pair of the N vertices: each pair belongs to N-2 triples, and (N-2)/[3 C(N,3)]=1/C(N,2). Thus

    p := E[X_j] = (e+2v+2w+3c)/3,       E[D]=p, E[B]=0.

## 2. Complete rooted-triple calculation

For a center in a triple let d count its comparable neighbors and let b count successors minus predecessors. There are three equally likely centers and two equally likely ordered assignments of the other labels. For distinct neighbors j,k,

    X_jX_k = d(d-1)/2,
    average_(j,k) X_jY_k = (d-1)b/2,
    Y_jY_k = (b^2-d)/2.

These follow from d=X_j+X_k, b=Y_j+Y_k, X_jY_j=Y_j and Y_j^2=X_j. Subtract the same-neighbor terms from db and b^2 before dividing the ordered cross sums by two. The mixed identity averages the two assignments; it does not equate their separate values.

| Type | All three center roles (d,b) | E[X_jX_k] | E[X_jY_k] | E[Y_jY_k] |
| --- | --- | ---: | ---: | ---: |
| A | (0,0), (0,0), (0,0) | 0 | 0 | 0 |
| E | (1,1), (1,-1), (0,0) | 0 | 0 | 0 |
| V | (2,2), (1,-1), (1,-1) | 1/3 | 1/3 | 1/3 |
| W | (2,-2), (1,1), (1,1) | 1/3 | -1/3 | 1/3 |
| C | (2,2), (2,0), (2,-2) | 1 | 0 | 1/3 |

The middle of a chain contributes -1 to the signed product, while each endpoint contributes +1. Weighting all rows gives

    eta   := E[X_jX_k] = (v+w)/3+c,
    gamma := E[X_jY_k] = (v-w)/3,
    beta  := E[Y_jY_k] = (v+w+c)/3,          j!=k.

Zero contributions from A and E are included; they still affect the pair and same-neighbor moments. In particular, fork/join asymmetry is exactly gamma!=0 under the stated direction convention.

## 3. Finite covariance necessities

Set n=N-1, k=N-2=n-1 and delta=eta-p^2. The same-neighbor terms obey

    E[X_j^2]=E[Y_j^2]=p,       E[X_jY_j]=0.

Each product of sums contains n same-neighbor terms and n(n-1) ordered distinct-neighbor terms. There is no further factor two. Expansion therefore gives

    Var(D) = [p+k eta]/(k+1)-p^2
           = [p(1-p)+k delta]/(k+1),
    Cov(D,B) = k gamma/(k+1),
    Var(B) = [p+k beta]/(k+1).

This actual covariance matrix must be positive semidefinite, so both diagonal numerators and its determinant must be nonnegative:

    p(1-p)+k delta >= 0,
    p+k beta >= 0,
    k^2 gamma^2 <= [p(1-p)+k delta][p+k beta].             (1)

The second diagonal condition is automatic for a declared probability vector, because p,beta>=0. The first remains explicit: checking a determinant without its diagonal conditions is not a general positive-semidefiniteness test. No division by a variance, delta or beta was used, so zero cases remain covered.

These are necessary conditions for the hypothetical extension, not sufficient conditions for a probability law or a growth process. A passing covariance matrix does not establish any extension.

## 4. Fixed-law unbounded-size implication

Suppose the same vector (a,e,v,w,c) occurs as a uniform triple marginal at arbitrarily large finite sizes. Divide the first inequality in (1) by k and the determinant inequality by k^2. Along those sizes, taking numerical limits gives

    delta=eta-p^2 >= 0,             gamma^2 <= delta beta.             (2)

No coupling between the orders at different sizes or infinite representation theorem is required for this implication. The marginal is fixed while N grows. One cannot apply (2) as a uniform conclusion for unspecified N-dependent marginals.

If delta<0, the first variance eventually becomes negative. If delta=0 but gamma!=0, the determinant condition becomes

    k^2 gamma^2 <= p(1-p)(p+k beta),

with a positive quadratic left side and an at-most-linear right side, so it eventually fails. Thus fork/join asymmetry obstructs unbounded exact sampling on the slice eta=p^2. If delta=gamma=0, this test passes but proves no extension. Even delta>0 cannot permit unbounded sizes when gamma^2>delta beta.

The degenerate cases are consistent with this formulation. At p=0 only A has positive mass and all moments vanish. At p=1 only C has positive mass; delta=gamma=0 and beta=1/3, so D is deterministic. If beta=0, then v=w=c=0, gamma=eta=0 and delta=-p^2; (2) forces p=0. No zero denominator or canceled constraint hides these cases.

For the previously accepted target

    (a,e,v,w,c)=(1,6,2,1,2)/12,
    p=1/2, eta=1/4, delta=0, gamma=1/36, beta=5/36,

condition (1) gives (N-2)^2<=9(5N+8), or N^2-49N-68<=0. It recovers RI1447: the polynomial is -18 at N=50 and 34 at N=51, increasing thereafter. No N>=51 extension has that exact triple target. This does not tighten the threshold, establish minimality or prove smaller-size existence. The complete finite contradiction is in [RI1448](RI1448_DIRECTIONAL_SAMPLING_OBSTRUCTION.md). RI1445's scalar variance no-exclusion result remains correct; passing that scalar test never certified all covariance constraints.

## 5. A complete asymmetric comparison at every finite size

Fix q in the open interval (0,1), using this same q for the entire comparison family. For any finite number of labeled vertices, give each vertex an independent lower type with probability q and an upper type with probability 1-q. Declare i to precede j exactly when i is lower and j is upper. There are no within-type comparisons.

The relation is irreflexive and asymmetric. A two-step chain would require its middle vertex to be both upper and lower, so none exists; transitivity holds. Adding equality gives a non-strict partial order.

For any deterministic subset of vertices, the retained types remain independent with the same probabilities, and their induced relation depends only on those retained types. Restriction therefore gives exactly the smaller construction. An independent uniform subset averages identical fixed-subset laws, so it gives that law too. This proves exact uniform restriction consistency at every finite size directly. Existence comes from the construction, not from a passing covariance test.

A triple is A when all types agree, V when precisely one vertex is lower, and W when precisely two are lower. E and C never occur. The complete marginal is

    (a,e,v,w,c)
      = (q^3+(1-q)^3, 0, 3q(1-q)^2, 3q^2(1-q), 0).               (3)

Every entry is nonnegative. Their sum is the binomial expansion (q+(1-q))^3=1. Put r=q(1-q)>0 and s=1-2q, so s^2=1-4r. Then

    v-w=3rs,
    p=2r, eta=beta=r, gamma=rs, delta=r-4r^2=rs^2.

The law is asymmetric exactly when q!=1/2. For these asymmetric choices delta>0, and gamma^2=delta beta: the unbounded necessary inequality is saturated rather than violated. These examples lie outside the zero-delta slice responsible for RI1447.

## 6. Finite covariance and an explicit example

For the comparison, substitution into the general finite formulas gives, for N>=3,

    Var(D) = r[s^2+1/(N-1)],
    Cov(D,B) = rs(N-2)/(N-1),
    Var(B) = rN/(N-1).

These also follow by conditioning on the root. With n=N-1, a lower root has a binomial number K of comparable neighbors with n trials and success probability 1-q, and D=B=K/n. An upper root has success probability q, with D=K/n and B=-K/n. Averaging the binomial first and second moments gives E[D]=2r, E[B]=0, E[D^2]=E[B^2]=r+r/n and E[DB]=rs(1-1/n), recovering the displayed covariance.

The determinant is

    Var(D)Var(B)-Cov(D,B)^2
      = r^2 [N+(3N-4)s^2]/(N-1)^2 > 0,       N>=3.              (4)

To check the numerator, its s^2 coefficient with n=N-1 is n(n+1)-(n-1)^2=3n-1=3N-4, and its constant is n+1=N. Both variances are positive. The excluded endpoints q=0,1 are not used to justify strict positivity. The construction is defined at smaller sizes too; normalized-degree and triple formulas above are asserted only on their stated domains.

At q=1/3 the exact values are

    (a,e,v,w,c)=(1/3,0,4/9,2/9,0),
    (p,eta,gamma,beta,delta)=(4/9,2/9,2/27,2/9,2/81).

This is an explicit asymmetric law with exact restriction consistency at every finite size. At q=1/2 the law is (1/4,0,3/8,3/8,0), with p=1/2 and gamma=delta=0. It is symmetric but still differs from the previously admitted triple target.

## 7. Why the comparison is not native admission

The comparison changes the specified probabilities. Its e=c=0 disagree with the admitted e=1/2 and c=1/6. Its a=1-3r>=1/4 disagrees with a=1/12. For asymmetric q, p=2r<1/2, so even the pair marginal changes. At q=1/2 the pair probability matches but the triple law does not.

The inherited native family requires strictly positive probability for every eligible ideal and its full-complement case. Its prefix already assigns positive mass to all five triple types. The comparison has two-chain probability 2r>0. A strictly positive full-ideal maximal birth from that chain would produce a three-chain with positive probability, contradicting c=0. A strictly positive empty birth from the chain would produce E, contradicting e=0. Summing positive marked branches cannot cancel these positive unmarked masses.

Moreover, iid vertex indices are not maximal-birth labels: a later indexed lower vertex may lie below an earlier upper vertex. No native marked rows, record locality, whole-PSD maps or complete marked incomparable-birth diamonds are supplied by the construction. Its arbitrary-poset existence result is not a counterexample within the complete strictly positive native class, and no replacement law is adopted.

The accepted four-order parameter t varies over -1/18<t<2/3 while leaving the seed and pair/triple marginals fixed. No t realizes the comparison law (3). Vertex relabeling leaves anonymous probabilities unchanged. A paired potential gauge u'=lambda u, alpha'=alpha/lambda with lambda>0 also preserves branch probabilities. Neither operation changes the target marginal.

Order duality exchanges v,w, reverses gamma and preserves p,eta,beta. Reversing only the convention for B reverses the covariance sign. Both preserve gamma^2 and leave the obstruction unchanged. A probability-changing choice of law therefore cannot be presented as a coordinate relabeling, a probability-preserving gauge or a harmless change of direction convention. The conditional finite-prefix law-choice distinction supplies no bare-DET law-selection principle or all-horizon native replacement.

## 8. Evidence and boundaries retained

RI1449 has distinct author and independent review, followed by root acceptance of the conditional necessity and explicit comparison. Actual retained final report and premises bodies match their current bytes; the reviewer also retains its complete final prose body. This present evidence does not reconstruct original chronology. The author recovered a 10,653-byte draft that exceeded its 10,240-byte cap; the final author report is 10,167 bytes. Empty patch results and an editorial clarification receipt remain limited evidence of the earlier edits. The review's duplicate-path editorial patch was rejected and recovered with a single update.

The author recorded substantive completion at 05:46:38 UTC before its 05:56:13 cutoff. Its 05:48:23 freeze declaration precedes final completion; the separately attributed 05:48:49 completion is before the 06:02:13 deadline, but the original final all-file response is absent. The review separately records full prose followed by 05:57:00 and reports all-file completion followed by 05:58:32 before its 06:10:10 deadline. Current hashes and acceptance do not supply missing historical receipts. Missing RI1389 evidence, late RI1401/RI1419 work and inherited cap/display/schema/wrapper/patch/TextEncoder and custody qualifications remain.

No physical preparation, joint observation kernel, nondisturbance, clock/readout, calibration or action/reset-cost mapping is supplied. E still needs the actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE still needs source/reset/control/readout transfer and history-wise certificates in both candidate worlds, including full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains packing/general serialization, source/build/ABI/binding, resource/control/qualification and observed-execution holds. No new measurement theorem or calibration/trace prerequisite for the fixed nominal statistic is added.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% usage guard and RET-only pause persist. This is a conditional mathematical publication, not execution or empirical validation. It asserts neither covariance sufficiency nor a new native all-size law. No unreviewed successor result or release receipt is included.
