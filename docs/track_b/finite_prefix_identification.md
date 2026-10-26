# Finite-prefix identification within the positive subset-weight family

**Reviewed conditional result.** An exact direct endpoint population distribution at H births identifies precisely the normalized weights through index H−1 within the declared positive scalar subset-weight family. This is neither selection of that family nor inference from one sampled endpoint.

## Declared family and distribution

Fix H≥1 and positive finite weights t_k through k=H−1, normalized by t_0=1. At a parent order P with n vertices, use

    Z_n = Σ_(k=0..n) binom(n,k)t_k,
    G(s,m) = Σ_(k=m..s) binom(s−m,k−m)t_k,
    q(P,S) = G(|S|,|Max S|)/Z_n.

S ranges over actual ideals, including empty and full. Independent immutable fair-bit marks split each scalar branch into q(P,S)/2 on a common arbitrary complex positive-semidefinite payload. Partitioning all selected subsets by their ideal closure proves normalization. No separately prescribed mark-dependent seed or arbitrary admitted DET kernel is included.

Let μ_n be the direct n-birth marked-endpoint population law with birth labels forgotten. The accepted [intrinsic restriction theorem](intrinsic_subset_restriction.md) supplies the parameter-independent deletion kernel K_n: delete an actual maximal vertex v with weight L(P−v)/L(P), where L counts linear extensions on distinct vertices, restrict order and marks, then merge output types. For this family, μ_n K_n=μ_(n−1). The kernel recovers marginal laws, not realized birth chronology.

## Inverse and its exact horizon

Let a_n be the probability that the underlying order is the n-antichain, with a_0=a_1=1. Any nonempty ideal creates a relation that persists. Thus an antichain requires and is produced by the unique all-empty sequence of structural choices:

    a_n = ∏_(j=0..n−1) 1/Z_j > 0,
    Z_n = a_n/a_(n+1),
    t_n = Σ_(k=0..n) (−1)^(n−k) binom(n,k)Z_k.

There is no extra n! factor for the canonical naturally labelled antichain. The marked type with k one-bits has mass a_n binom(n,k)/2^n; summing marks returns a_n.

Binomial inversion follows by substituting the expression for Z_k: the coefficient of t_j becomes binom(n,j)Σ_(l=0..n−j)(−1)^(n−j−l)binom(n−j,l), which is zero for j<n and one for j=n. The diagonal is one, so the inverse is unique. Without fixing t_0, the same ratios recover t_k/t_0, since common positive scaling cancels in every G/Z row.

Starting with the full μ_H and iterating the accepted K kernels obtains μ_n and hence a_n at every lower horizon. K depends only on order, so the full unmarked endpoint distribution also suffices. It follows that, for two members of this family,

    μ_H^(t) = μ_H^(u)
      if and only if t_k/t_0 = u_k/u_0 for 0≤k≤H−1.

The reverse implication holds because all H-birth rows use only those coefficients. No coefficient of index H or later enters them. Positive tails may vary without changing μ_H; t_n/t_0 is first identifiable at horizon n+1 when coefficients are otherwise unrestricted. H=1 identifies no nontrivial coefficient. A single sampled order, or just the single scalar a_H, does not generally supply the full distribution needed here. Computing K requires exact extension counts; no efficient algorithm is established.

## Exact example and precision

For (t_0,t_1,t_2)=(1,2,3), Z=(1,3,8) and (a_1,a_2,a_3)=(1,1/3,1/24). At three births the unmarked probabilities for antichain, edge-plus-isolate, fork, join and chain are respectively (1,6,4,3,10)/24. Under K their chances of yielding a two-antichain are (1,2/3,0,1,0), so a_2=(1+4+3)/24=1/3. Inversion returns t_1=3−1=2 and t_2=8−2·3+1=3.

If each of a_n and a_(n+1) has absolute error at most ε<a_(n+1), subtracting ratios yields

    |Zhat_n−Z_n| ≤ ε(1+Z_n)/(a_(n+1)−ε).

If |Zhat_k−Z_k|≤d_k, inversion gives |that_n−t_n|≤Σ_(k=0..n)binom(n,k)d_k. These are deterministic bounds conditional on supplied probability-error bounds. There is no uniform absolute-error stability on the unrestricted positive family: already t_1=1/a_2−1 becomes arbitrarily sensitive near a_2=0. For fixed-p growth, a_H=(1−p)^[H(H−1)/2], so the diagnostic event can be rare.

## Claim boundary

This result complements [finite-prefix nonidentification](finite_prefix_nonidentification.md): a finite prefix may be identified while its unrestricted future remains undetermined. [Law-selection limits](intrinsic_law_selection_limits.md) remain: endpoint distributions and intrinsic restriction do not certify family membership or determine history weights outside the promised family. An unknown observation/deletion channel can confound the direct-law inference.

The result has distinct mathematical review and coordinator adoption. It supplies no observed population law, calibrated channel, finite-sample guarantee, preferred law, computational advantage or physical mass/gravity prediction. Exact private review and identity evidence remain local under the metadata-obscured publication policy; publication does not reconstruct historical custody.
