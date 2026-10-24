# RI1448: Directional sampling obstruction

The independently reviewed, root-accepted RI1447 theorem gives a finite obstruction: no random completed N-poset with N>=51 can have uniform induced triple law (1,6,2,1,2)/12 on the five types defined below. Every member of the admitted four-order family shares this triple law, so none has that exact uniform induced-suborder extension at those sizes. The proof concerns an optional sampling-consistency requirement. It leaves native causal growth without that requirement and physical observation as separate questions.

## 1. Exact hypothesis and finite-family consequence

An induced suborder retains the completed order relation between its selected vertices, including comparisons whose generating paths used deleted vertices. Choose the vertex subset uniformly, independently of the realized order conditional on that order. The five anonymous three-vertex orders are:

- A: the antichain.
- E: one comparable pair and one isolated vertex.
- V: a fork with one bottom below two incomparable tops.
- W: a join with two incomparable bottoms below one top.
- C: the three-vertex chain, including its transitive bottom-to-top comparison.

The theorem assumes an arbitrary random completed N-poset, with integer N>=3, whose uniform induced triple has probabilities

    m(A,E,V,W,C) = (1,6,2,1,2)/12.

No growth law or independence between comparisons is needed for the obstruction. The hypothesis itself will be contradicted for N>=51.

For its application, let P_t denote the previously admitted anonymous four-order law for -1/18<t<2/3. Its finite admission is conditional on the fixed-seed, mark-independent, scalar-passive family, positive complete birth rows, proper-precursor mark locality with whole-unmarked-parent access, equivariance, fair immutable bits and complete marked incomparable-birth diamonds. Every admitted t has the displayed triple law and pair comparability probability 1/2. These are finite growth premises, not an all-horizon construction. The earlier [variance report](RI1446_VARIANCE_AND_NUMERICAL_RESIDUALS.md) records the family and scalar test; the inputs and proof for the present obstruction are all given here.

The triple theorem is stronger than an exclusion of a selected parameter: any hypothetical N-order with this exact triple marginal fails at N>=51. No four-order probability, disjoint-pair moment or choice of t can change that conclusion while retaining m.

## 2. Uniform root and direction convention

Conditionally on each realized N-order, assign a uniform random bijection of its vertices to labels 1,...,N. These auxiliary labels are unrestricted by birth time or topological order. Vertex 1 is therefore a uniform root. For each neighbor label j!=1 put

    X_j = 1{1 precedes j or j precedes 1},
    Y_j = 1{1 precedes j} - 1{j precedes 1}.

A successor contributes +1 and a predecessor -1. Let n=N-1 and define the normalized comparability and directional degrees

    D = (sum_(j!=1) X_j)/n,
    B = (sum_(j!=1) Y_j)/n.

Since 0<=D<=1 and |B|<=1, all moments used below exist. Uniform relabeling permits common moments for distinct neighbor labels but does not make their indicators independent.

The five triple types contain respectively 0,1,2,2,3 comparable pairs. Their weighted mean is (0+6+4+2+6)/12=3/2. A uniform pair in a uniform triple is a uniform pair in the N-order, so its comparability probability is p=(3/2)/3=1/2. Swapping the two labels of a comparable pair exchanges its directions; each direction has probability 1/4. Thus E[X_j]=1/2 and E[Y_j]=0. This orientation balance follows from uniform labeling and requires no order-dual symmetry: V and W have unequal weights.

The randomization here is a finite mathematical device. It asserts neither an available physical selector nor a nondisturbing readout procedure.

## 3. All rooted triple roles

For a triple with chosen center, let d be its number of comparable neighbors and b its successor-minus-predecessor count. The center is uniform among the three vertices, and the two other labels have two equally likely assignments. For distinct neighbors j,k,

    X_j X_k = d(d-1)/2,
    average_(j,k) X_j Y_k = (d-1)b/2,
    Y_j Y_k = (b^2-d)/2.

To obtain the last two identities, expand db and b^2 and remove the same-neighbor terms X_jY_j=Y_j and Y_j^2=X_j. The mixed expression is the average over the two ordered assignments, not an assertion that their individual values agree.

| Triple | All three center roles (d,b) | E[X_jX_k] | E[X_jY_k] | E[Y_jY_k] |
| --- | --- | ---: | ---: | ---: |
| A | (0,0), (0,0), (0,0) | 0 | 0 | 0 |
| E | (1,1), (1,-1), (0,0) | 0 | 0 | 0 |
| V | (2,2), (1,-1), (1,-1) | 1/3 | 1/3 | 1/3 |
| W | (2,-2), (1,1), (1,1) | 1/3 | -1/3 | 1/3 |
| C | (2,2), (2,0), (2,-2) | 1 | 0 | 1/3 |

The chain's middle center has one predecessor and one successor, giving Y_jY_k=-1. Its bottom and top each give +1, so its average is 1/3. All comparisons refer to the completed relation.

Weighting every row by m gives the three distinct-neighbor moments

    eta   = E[X_jX_k] = (2/12+1/12)/3 + 2/12 = 1/4,
    gamma = E[X_jY_k] = (2/12-1/12)/3 = 1/36,
    beta  = E[Y_jY_k] = (2/12+1/12+2/12)/3 = 5/36.

The mixed moment gamma is nonzero because the fork and join weights differ. Zero cross-products for A and E are retained zero contributions, not omitted probability mass. These types still affect the single-neighbor moments.

## 4. Finite corrections and covariance

For a single neighbor, the identities X_j^2=X_j, Y_j^2=X_j and X_jY_j=Y_j give

    E[X_j^2] = E[Y_j^2] = 1/2,
    E[X_jY_j] = 0.

Each product of sums has n same-neighbor terms and n(n-1) ordered distinct-neighbor terms. There is no extra factor two after using this ordered count. Consequently,

    E[D] = 1/2,                    E[B] = 0,
    E[D^2] = [n/2+n(n-1)/4]/n^2 = N/[4(N-1)],
    Var(D) = 1/[4(N-1)],
    Cov(D,B) = E[(D-1/2)B]
             = [n*0+n(n-1)/36]/n^2 = (N-2)/[36(N-1)],
    E[B^2] = [n/2+5n(n-1)/36]/n^2 = (5N+8)/[36(N-1)].

Using triple moments for the same-neighbor terms would lose these finite-size corrections. Reversing the convention for B changes the covariance sign but not its square or the obstruction.

At N=3 a direct check uses D=d/2 and B=b/2 in the table. Averaging gives E[d^2]=3/2, E[db]=1/18 and E[b^2]=23/18. Hence E[D^2]=3/8, Var(D)=1/8, E[DB]=1/72 and E[B^2]=23/72, agreeing with the formulas. The covariance determinant there is 206/5184>0; the known three-order distribution is not excluded.

## 5. A finite nonnegative-square contradiction

Cauchy-Schwarz applied to D-1/2 and B requires

    ((N-2)/[36(N-1)])^2
        <= (1/[4(N-1)]) * ((5N+8)/[36(N-1)]).

All denominators are positive on N>=3. Clearing them yields

    (N-2)^2 <= 9(5N+8),
    equivalently f(N) := N^2-49N-68 <= 0.

The covariance determinant is -f(N)/[1296(N-1)^2]. More explicitly, Var(D)>0 allows a=Cov(D,B)/Var(D)=(N-2)/9. Expanding a real square gives

    E[(B-a(D-1/2))^2]
      = E[B^2] - Cov(D,B)^2/Var(D)
      = (-N^2+49N+68)/[324(N-1)].

This required expectation must be nonnegative. The integer boundary is exact for this test:

| N | f(N) | Required square expectation | Covariance test |
| ---: | ---: | ---: | --- |
| 50 | -18 | 1/882 | passes |
| 51 | 34 | -17/8100 | impossible |

For N>=51, f(N+1)-f(N)=2N-48>0, so failure persists at every larger integer. For 3<=N<=49, f(N)=N(N-49)-68<0; N=50 also passes. Thus 51 is the first failing integer of this covariance condition. It is not established as the smallest impossible extension size. Passing at smaller sizes proves neither existence of an extension nor that all other necessary constraints hold.

The negative value at N=51 is already a finite contradiction. No asymptotic limit, infinite exchangeability representation, numerical search or later growth-layer construction is used.

## 6. Exact transfer from four vertices to three

Suppose N>=4 and a uniform four-subset of an N-order has induced law P_t. Select one of that four-set's four triples uniformly. Any fixed triple of the N vertices belongs to exactly N-3 four-sets. Its probability under the two-step selection is

    (N-3)/[4 C(N,4)] = 1/C(N,3).

Therefore the selected triple is exactly uniform in the N-order. Restricting the completed relation in two steps is the same as restricting directly to the triple. Since each P_t has marginal m, the hypothetical N-order would satisfy the theorem's triple hypothesis. For every admitted -1/18<t<2/3, such an extension is impossible at every N>=51.

The common triple marginal, not any changing four-order weight, drives this result. Selecting t differently even at each size cannot repair a target that still imposes this same m at a size N>=51. Changing the triple target or the sampling kernel is a different requirement and needs separate justification; no replacement is adopted here.

## 7. What is excluded and what remains open

The inconsistent conjunction is the exact finite triple target m, exact uniform induced-suborder consistency with that target, and extension to any N>=51 (in particular, unbounded sizes). Retaining the finite target requires weakening or abandoning that optional all-size uniform-sampling demand, or limiting the requested horizon. A limited horizon is not itself proved feasible.

Native incomparable-birth diamonds compare alternative routes of growth. They do not impose arbitrary uniform vertex-deletion consistency. The theorem therefore leaves intact the accepted finite four-birth construction; it neither forbids all native continuation without the optional sampling demand nor constructs such continuation. No fifth-birth law, full-horizon law, classification, optimal obstruction threshold, physical prediction or empirical claim follows.

This is consistent with RI1445. Its necessary scalar total-comparability variance condition, using theta(t)=259/972+t/9, passes throughout the admitted interval and excludes no parameter. It discards directional information. Here Var(D) decreases as 1/[4(N-1)], while the nonzero mixed covariance eventually exceeds what E[B^2] permits. A passing scalar variance was never a sufficiency theorem for the full covariance or distribution constraints.

## 8. Evidence qualification and unchanged gates

RI1447 has distinct author, independent mathematical review and root conditional acceptance. That present acceptance does not repair historical custody. The retained author record includes original control/disposition bodies, but five predecessor report/premise bodies are not embedded. Final prose/source-readback records contain metadata and boolean capture assertions rather than the original full output strings; the notation-clarification receipt is empty. Reported display clipping and recovery remain attributed. Fresh semantic reads support the present mathematics, not a claim that missing historical bodies were recovered.

The author's recorded substantive clock is 04:50:31 UTC, before its 04:57:47 cutoff. Its 04:52:33 freeze declaration precedes completion; the separately attributed 04:52:57 final completion is before the 05:03:47 deadline, but its original all-file response is not embedded. The independent review separately reports full prose followed by 04:59:24 and all-file completion followed by 05:01:11, before its 05:13:51 deadline. These attributions remain distinct from present-byte verification. Missing RI1389 evidence, late RI1401/RI1419 readbacks and retained cap, display, schema, wrapper, patch and TextEncoder failures are not waived.

This checkpoint publishes no new measurement theorem. Its actual execution, custody and resource holds remain. No calibration or trace prerequisite is added to the fixed nominal statistic.

E still requires the actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE still requires source/reset/control/readout transfer and history-wise certificates in both candidate worlds, including full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains packing/general serialization, source/build/ABI/binding, resource/control/qualification and observed-execution holds. Native joint observation, physical preparation/readout, nondisturbance, calibration and action/reset costs remain separate missing inputs.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% usage guard and RET-only pause persist. Publication is not execution. No unreviewed successor result, release receipt or physical validation is supplied.
