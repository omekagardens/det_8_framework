# RI1452: Full-support comparison

The independently reviewed, root-accepted RI1451 construction gives asymmetric random-poset laws that are exactly consistent under induced restriction and assign positive probability to every finite completed order. Its explicit mixture removes the zero-support limitation of the earlier two-level comparison. It does not supply a native DET growth law: the positive normalized ordinary extension kernel includes nonmaximal insertions, so its maximal-only subrow is not normalized.

The original marginal target and RI1447 obstruction remain unchanged.

## 1. Declare one family across sizes

Choose a sequence T_1,T_2,... of nonempty finite strict posets containing a representative of every nonempty finite anonymous poset. Let m_j be the number of vertices of T_j. There are only finitely many binary relations at each finite size, so their countable union permits this formal choice. No enumeration is performed.

Set w_j=2^(-j), for j>=1. Every weight is positive and their sum is one. For a finite template T, define Q_N^T on the N distinct labeled sample vertices [N]={1,...,N}: independently assign each vertex a uniform type tau_i in T, then declare

    i precedes j  if and only if  tau_i <_T tau_j.

Equal types remain distinct, incomparable sample vertices. They are not identified. Define the dual-balanced mixture

    H_N = sum_(j>=1) (w_j/2) [Q_N^(T_j)+Q_N^(T_j^op)].           (1)

Here T^op reverses every comparison. Choose one template and one orientation for the whole sample. Do not choose a fresh component separately for each vertex or after restriction. Duplicate representatives or self-dual templates are allowed; their component weights still sum to one.

Let L_N be the two-level law obtained by giving each sample vertex an independent lower type with probability 1/3 and an upper type with probability 2/3, with every lower below every upper and no within-type comparison. Fix 0<lambda<1 and put

    P_N = (1-lambda) H_N + lambda L_N.                         (2)

The same sequence, weights and lambda are used at every size. A mixture chooses one poset-valued component; it does not average order relations. At size zero use the unique empty law. All of these are declared comparison-law data, not DET primitives, an executed generator or a physical sampling experiment.

## 2. Partial orders and exact restriction

For Q_N^T, irreflexivity and asymmetry follow directly from the template. If i precedes j and j precedes k, then tau_i <_T tau_j <_T tau_k, hence tau_i <_T tau_k. Thus the relation is transitive. Repeated endpoint types cannot defeat this argument: they would require a strict cycle in T. Adding sample-vertex equality gives its non-strict partial order; it does not equate distinct vertices of the same type.

The two-level relation is also a strict poset. A two-step chain would require its middle vertex to be both upper and lower, so no such chain exists and transitivity holds. Therefore every realized component and every realized mixture outcome is a poset.

For any fixed k-subset of N sample labels, 1<=k<=N, the retained types are still iid with the same template distribution. Their completed induced relation uses only these retained types. Restriction preserves existing comparisons; it does not recompute generating edges after deletion. Relabel the retained sample vertices onto [k]. Conditional on the chosen component, this gives precisely its k-vertex law.

Consequently, if U_(N,k) independently selects a uniform k-subset and reports its induced order on [k],

    Q_N^T U_(N,k) = Q_k^T,       L_N U_(N,k) = L_k,
    H_N U_(N,k) = H_k,           P_N U_(N,k) = P_k.             (3)

The fixed-subset identity holds before the uniform average. Countable mixing commutes with restriction because its nonnegative probability sums have total weight one. Each component is invariant under sample-label permutations, so the mixture is exchangeable. The shared component remains shared after restriction; redrawing it would define another experiment. Conditional iid types do not assert unconditional independence between vertices or overlapping observations.

This proves exact consistency at every finite size without an infinite representation theorem, natural birth ordering or physical observer.

## 3. Explicit full-support bounds

Let F be any anonymous k-vertex poset with k>=1. Choose an index j(F) such that T_j is isomorphic to F; then m_j=k. Within that displayed template orientation, each assignment from [k] to its k types has probability k^(-k). All k! bijective assignments yield the anonymous order F.

Those assignment events are disjoint, even when automorphisms give the same resulting labeled relation. Thus retaining just this component in (2) gives

    P_k([F]) >= (1-lambda) 2^(-j(F)-1) k!/k^k > 0.            (4)

No automorphism division or extra automorphism factor is appropriate. For any particular labeled version F_lab, one fixed isomorphism assignment already gives

    P_k(F_lab) >= (1-lambda) 2^(-j(F)-1) k^(-k) > 0.          (5)

Other assignments and components may add mass, so these are lower bounds, not exact probabilities. The empty order has mass one at size zero. Dropping the factor 1-lambda in the same argument proves that H itself has full support.

The quantifier is: for every finite target, the ensemble law at that size gives it positive probability. The bound depends on the chosen target's index and size; no uniform-in-size coverage estimate is asserted. It does not say every latent component or every sampled world contains every pattern. For example, a single finite template cannot produce a chain longer than its height.

## 4. Complete symbolic triple law

Write A for the antichain, E for one edge plus an isolate, V for a fork with one bottom, W for a join with one top, and C for a three-chain. For a template T of size m define

    n_X(T) = number of maps f:{1,2,3}->T whose pullback
             completed order has anonymous type X,
    theta_X(T) = n_X(T)/m^3,                X in {A,E,V,W,C}. (6)

All maps count, including repeated types. The five types partition the m^3 assignments, so each theta_X is nonnegative and their sum is one. These are exact definitions, not evaluated tables.

Template duality fixes A,E,C and interchanges V,W. This remains true for the incomparabilities introduced by repeated types. Therefore H has triple law h=(a0,e0,u0,u0,c0), with

    a0 = sum_j w_j theta_A(T_j),
    e0 = sum_j w_j theta_E(T_j),
    c0 = sum_j w_j theta_C(T_j),
    u0 = (1/2) sum_j w_j [theta_V(T_j)+theta_W(T_j)].          (7)

All series converge absolutely, since their nonnegative terms are bounded by summable weights. Their normalization is a0+e0+2u0+c0=1. The full-support witness for H applied to the five triple types proves a0,e0,u0,c0>0. Their exact values depend on the chosen template sequence and have not been computed.

For L, three equal types give A, precisely one lower gives V, and precisely two lowers give W. At lower probability 1/3 its triple law is

    ell = (1/3, 0, 4/9, 2/9, 0).

Thus P has the entire triple law

    a = (1-lambda)a0 + lambda/3,
    e = (1-lambda)e0,
    v = (1-lambda)u0 + 4lambda/9,
    w = (1-lambda)u0 + 2lambda/9,
    c = (1-lambda)c0.                                       (8)

It sums to one and every coordinate is strictly positive. Its asymmetry survives exactly:

    v-w = 2lambda/9 > 0.                                    (9)

Only H is dual-balanced. Pairing L equally with its dual would cancel this difference and would change the declared construction.

## 5. Root moments and strict covariance slack

For a uniform root 1 and neighbor j, let X_j indicate comparability and let Y_j be +1 for a successor, -1 for a predecessor and zero otherwise. For distinct neighbors j,k define

    p=E[X_j], eta=E[X_jX_k], gamma=E[X_jY_k], beta=E[Y_jY_k].

Counting comparable pairs and averaging the three root roles in each triple gives

    p = (e+2v+2w+3c)/3,
    eta = (v+w)/3+c,  gamma = (v-w)/3,  beta = (v+w+c)/3.

For example, V and W each contribute 1/3 to eta and beta, but opposite signs to gamma. The chain contributes 1 to eta, zero to gamma and 1/3 to beta: its middle root has signed neighbor product -1 and its endpoints each have +1. A and E contribute zero to these distinct-neighbor cross moments.

Define the corresponding quantities for H:

    p0=(e0+4u0+3c0)/3,
    eta0=2u0/3+c0,  beta0=(2u0+c0)/3,  delta0=eta0-p0^2.

Linearity of the raw moments in (8) gives

    p=(1-lambda)p0+4lambda/9,
    eta=(1-lambda)eta0+2lambda/9,
    gamma=2lambda/27,
    beta=(1-lambda)beta0+2lambda/9.                           (10)

Their meaning can be checked without evaluating a template series. Condition on the component, orientation and root type. Let d be the probability that another iid type is comparable to the root, and b its successor probability minus predecessor probability. Conditional independence of two further types gives

    p=E[d], eta=E[d^2], gamma=E[db], beta=E[b^2].

For each component, averaging over root and neighbor types gives E[b]=0: exchanging the two iid types reverses each oriented comparison with equal probability. This does not require a dual-balanced component. Hence delta=eta-p^2=Var(d), gamma=Cov(d,b), and beta=Var(b). Cauchy-Schwarz gives delta*beta>=gamma^2. In particular delta0>=0, and beta0>0 follows from u0,c0>0.

For L, p_L=4/9, eta_L=beta_L=2/9 and delta_L=2/81. Expanding the squared mixture mean in (10) yields the stronger exact identity

    delta = (1-lambda)delta0 + 2lambda/81
            + lambda(1-lambda)(p0-4/9)^2
          >= 2lambda/81 > 0.                               (11)

Also beta>2lambda/9 because 1-lambda>0 and beta0>0. Therefore

    delta*beta > 4lambda^2/729 = gamma^2.                    (12)

Both strictness and the parameter domain matter. No numerical value of p0 was assumed. This is a check on the constructed law, not a sufficiency theorem for arbitrary prescribed marginals.

For completeness, at finite N>=3 set D=sum X_j/(N-1) and B=sum Y_j/(N-1). Pair orientation balance gives E[D]=p and E[B]=0. Same-neighbor moments are E[X_j^2]=E[Y_j^2]=p and E[X_jY_j]=0. There are N-1 such terms and (N-1)(N-2) ordered distinct-neighbor terms. Thus

    Var(D) = [p(1-p)+(N-2)delta]/(N-1),
    Cov(D,B) = (N-2)gamma/(N-1),
    Var(B) = [p+(N-2)beta]/(N-1).

These are actual finite moments of P_N; their covariance matrix is positive semidefinite. Existence came from the component construction and restriction proof, not from covariance alone.

The original admitted target has p=1/2 and eta=1/4, so delta=0. Equation (11) proves that this comparison cannot preserve that joint pair/triple target. It does not establish a numerical p or rule out p=1/2 by itself. RI1447's original N>=51 obstruction remains; 51 is not proved minimal. The accepted t variation fixes the old pair/triple laws; relabeling and paired probability-preserving potential gauges preserve them, while duality only reverses gamma's sign. None turns this comparison into a coordinate repair. The preceding general marginal-law test is given in [RI1450](RI1450_MARGINAL_LAW_DEPENDENCE.md).

## 6. Positive extension kernel and the missing maximal mass

Full labeled support and fixed-subset consistency imply more than terminal positivity alone. For every labeled parent F on [n], P_n(F)>0. For every labeled one-vertex extension F' on [n+1] whose restriction to [n] is F, set

    K(F,F') = P_(n+1)(F')/P_n(F).

Each entry is positive. The finite set of all such extensions partitions the event of observing F on [n], so

    sum_(F' restricting to F) P_(n+1)(F')=P_n(F),
    sum_(F' restricting to F) K(F,F')=1.                     (13)

This is a normalized ordinary label-extension kernel. It includes positive entries for maximal additions, but it also includes nonmaximal insertions.

For any nonempty F, placing the new vertex below every old vertex gives a valid nonmaximal extension. Full support makes its probability positive. Omitting it, together with any other nonmaximal extensions, leaves the maximal-only subrow with sum strictly less than one. Positive maximal extensions exist too, such as placing the new vertex above every old vertex. The empty parent is excluded from this strict-deficit statement.

For a singleton parent the deficit is especially explicit. Exchangeability makes the two chain orientations each have probability p/2. Maximal addition permits the incomparable pair and the orientation old<new, so the maximal-only sum is 1-p/2. Since p=(1-lambda)p0+4lambda/9>=4lambda/9>0, its omitted mass p/2 is at least 2lambda/9.

Conditioning on maximal additions or renormalizing their subrow changes K and requires a new consistency argument. None is supplied here. A separate topological sorting of each completed order does not construct a compatible native growth process across sizes. Failure of this particular kernel to be a normalized maximal-birth row does not rule out every possible native implementation.

## 7. Native and physical boundaries

Final-order support is an ensemble probability statement. Native strict positivity requires positive probabilities for every eligible ideal in a normalized row at each actual marked parent, together with locality, equivariance and complete incomparable-birth diamonds acting on the payload. Those obligations do not follow from (4), (5) or (13).

The template is shared latent information. Its posterior weights may depend on the whole observed parent, so iid types conditional on that template do not prove precursor-record locality. Sample labels are not natural birth labels. No fair immutable marks, whole-PSD maps, complete marked diamonds or normalized native row family is provided. The zero E/C support limitation of the earlier two-level example is removed, while native admission remains unproved. Neither a native replacement nor universal native impossibility is asserted.

No physical preparation, joint observation kernel, nondisturbance, clock/readout, calibration or action/reset-cost mapping follows. E still needs the actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE still needs source/reset/control/readout transfer and history-wise certificates in both candidate worlds, including full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains packing/general serialization, source/build/ABI/binding, resource/control/qualification and observed-execution holds. No new measurement theorem or calibration/trace prerequisite for the fixed nominal statistic is added.

## 8. Evidence and retained history

RI1451 has distinct author, independent review and root acceptance at the scope proved here. Retained final author report/premises bodies and the review body match current bytes. The review separately records twelve original body joins, including the manifest body; that historical count is distinct from this publication's literal input scope. Present body identities do not reconstruct chronology or replace absent original completion receipts.

The author recovered 12,637-byte and 12,339-byte drafts above its 12,288-byte cap; its final report is 12,193 bytes. It records substantive completion at 06:47:01 UTC before the 06:54:37 cutoff. The 06:48:10 freeze declaration precedes the separately attributed 06:48:32 final completion before the 07:00:37 deadline. The original final all-file receipt is not supplied; empty edit receipts remain limited evidence of earlier changes.

The reviewer recovered a clipped combined display and a 13,064-byte draft above its 12,288-byte cap, producing a final 12,255-byte review. Its recorded full prose is followed by 07:49:23; its reported all-file completion by 07:50:43 precedes its 08:03:56 deadline. These attributions remain separate from current verification. Missing RI1389 evidence, late RI1401/RI1419 work and inherited cap/display/schema/wrapper/patch/TextEncoder and custody qualifications persist.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% usage guard and RET-only pause remain. Publication is not execution. No unreviewed successor result, empirical validation or release receipt is supplied.
