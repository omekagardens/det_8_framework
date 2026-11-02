# Finite branching response and normalization ambiguity

Two independently reviewed conditional results, GDM037 and NE041, separate a finite response-shape distinction from an absolute-scale inference. Neither kernel, source or readout is derived from DET ontology. No physical mass or native unit is established.

## Fixed chain/diamond comparison

Use the three-chain s<a<t and four-diamond s<a<t, s<b<t, with a,b incomparable. Define the receiver-row matrix C by C_ij=1 exactly when j strictly precedes i. It is the full strict relation, not the cover matrix. To distinguish the hop coefficient from the vertex a, write the positive scalar coefficient as alpha.

The proposed signed linear response is

    K_mu = alpha C (I + mu alpha C)^(-1),
    eta = mu alpha in [0, 1/2].

Compare it with exactly the depth-attenuation family

    (K_att)_ij = alpha r^(d(j,i)-1)  if j strictly precedes i,
    (K_att)_ij = 0                  otherwise,
    r in [0,1],

where d is the greatest number of cover edges in a chain from j to i. The polynomial convention r^0=1 includes r=0. Within each model its parameters are common across the two fixtures.

The sole source is J=A e_s with the same known A>0 on both fixtures. Retain the fixture, source address/value and every signed output coordinate Y=gKJ. Gain g>0 is common across vertices and fixtures within a model. The rival models have independently variable positive nuisance products G_mu and G_att, each equal to g A alpha in its own model. They are not required to agree in advance. These are ideal response values, not event probabilities; every zero remains in the record.

Both causal matrices have C^3=0. Their only nonzero C^2 entry is (t,s): it equals1 for the chain and2 for the diamond. Thus

    (I+eta C)^(-1) = I-eta C+eta^2 C^2,
    K_mu = alpha(C-eta C^2).

Multiplication by I+eta C verifies the finite inverse directly, without an infinite-series assumption. Only the source-s column is observed; this calculation does not supply physical tomography. In coordinate orders (s,a,t) and (s,a,b,t), the complete observed families are

    F_mu:  (G_mu(0,1,1-eta), G_mu(0,1,1,1-2eta)),
    F_att: (G_att(0,1,r),    G_att(0,1,1,r)).

For any positive nuisance product the permitted gains realize these families. Equality of complete records first forces G_mu=G_att from a retained middle coordinate. Terminal equality then requires simultaneously r=1-eta and r=1-2eta, hence eta=0 and r=1. Conversely those values and equal observed scales give identical complete records. The exact intersection is therefore

    { ((0,G,G),(0,G,G,G)) : G>0 }.

Let R_C be chain terminal divided by chain middle, and R_D be diamond terminal divided by the mean of its two middles. Each denominator equals its model's positive G throughout the domain. The branching contrast Delta=R_D-R_C is

    (R_C,R_D,Delta)_mu  = (1-eta,1-2eta,-eta),
    (R_C,R_D,Delta)_att = (r,r,0).

| Endpoint | Chain terminal / G | Diamond terminal / G | Delta |
|---|---:|---:|---:|
| eta=0 | 1 | 1 | 0 |
| eta=1/2 | 1/2 | 0 | -1/2 |
| r=0 | 0 | 0 | 0 |
| r=1 | 1 | 1 | 0 |

At r=0 the cover responses remain alpha because r^0=1. The retained terminal zeros are legitimate responses, not removed failures. A zero contrast alone does not prove full-record equality: only r=1 intersects the eta=0 family. No strictly positive uniform separation margin exists as eta approaches zero, so the exact distinction supplies no finite-noise or finite-sample guarantee.

Transporting the order, source address and every output coordinate by one permutation conjugates C and both kernels. Cover depth is preserved, as are the middle average and the scalar ratios with their roles transported. The kernels vanish on the diagonal and outside strict precedence; cancellation at the diamond terminal when eta=1/2 is compatible with this formal retarded support. Neither that support nor relabeling covariance establishes physical spacetime.

The distinction comes from counting intermediate vertices in C^2 versus using only maximal cover depth in the comparator. A conventional real classical field with the same proposed K_mu yields the same data and survives this comparison. No exclusion of all classical propagation, quantum necessity, conserved energy, source recoil or gravity mechanism follows.

## Complete-map normalization ambiguity

Now explicitly strengthen the mathematical access contract: on every finite strict order P, allow every signed real source J and observe the entire noiseless vector

    Y = g alpha C (I + mu alpha C)^(-1) J,
    alpha,g>0, mu>=0,

with parameters common across all P and J. This is a separate ideal model assessment, not additional physical access established by the preceding single-source theorem.

For an N-vertex strict order, C^N=0: a nonzero entry of C^N would require N+1 strictly ordered distinct vertices. The inverse is the finite sum of (-mu alpha C)^k for k=0,...,N-1. The empty order has its unique empty map. Thus there are no poles or convergence conditions in the admitted finite domain.

For every lambda>0, the parameter transformation

    (alpha,mu,g) -> (lambda alpha, mu/lambda, g/lambda)

preserves every complete reported map while keeping C, the numerical J and Y coordinates fixed. Indeed beta=mu alpha is unchanged, K is multiplied by lambda and the gain compensates by1/lambda. With gamma=g alpha,

    Y = gamma C (I+beta C)^(-1) J.

This proves an exact ambiguity even under all the stipulated ideal maps. It does not assert that beta and gamma are always identifiable from a particular record, or that these exhaust every ambiguity. For mu>0, mu varies within the indistinguishable family; mu=0 stays zero. Antichains, zero sources and cancellation zeros are all retained, with no division by them.

One additional independently supplied gain value g=g_star>0, in the same source/output normalization, breaks this displayed action: g_star/lambda=g_star forces lambda=1. That statement is a normalization premise, not an acquired calibration or proof of complete identification. If the internal field has no separately fixed physical normalization, phi'=lambda phi with g'=g/lambda is a possible coordinate interpretation; physical permission for that re-expression is not assumed.

## Native quantities, units and use

The derived quantities here are conditional response shapes and invariant products. The fixtures, kernels, source preparation, addressing and readout are supplied assumptions. Further response shapes under the unchanged complete-map contract cannot remove the displayed normalization ambiguity. A physical interpretation needs additional correspondence and normalization evidence.

In particular, mu=m^2/rho would be an extra unvalidated relation with independently specified meanings and units for m and rho; it is not used in either proof. The [closed-source radiation/shell inertia result](closed_radiation_shell_inertia.md) supplies a conventional same-source E_total/c^2 target, but no identification of its energy or c with these response parameters. No physical length, time, density, action, work store, mass or native unit is derived here. The [native mapping inventory](../coordination/NATIVE_MASS_MAPPING.md) keeps those correspondence questions distinct from finite conditional mathematics.

Any physical trial would need a complete preparation/readout/failure model, calibration and execution admission. Missing access is unavailable evidence, not an observed zero. No apparatus, empirical trial, resource advantage or software execution is authorized by these results. The exact attenuation comparison and this normalization action are closed finite questions; unrelated native source and conservation work remains independent.

## Reviewed source identity

GDM037 author report SHA256 d41b0a195aaed83f97099086d928751e56b0254da47258c1e0a612adac352135; distinct proof review SHA256 23794bd2d4d631d1e4ee8e68c3f5e0feb7eb866319b109098fa160cd4bdd7ec9. Coordinator disposition SHA256 20b5b7dd8decbf5552fdbceb2c0f99a23714ac9716e8a22ba1cbea521dc7ed0e; completed-review timing clarification SHA256 353657a92bed669c4a5666e14c5cc2fb99e239150a90fc0af19f88b0843f19ce.

NE041 author report SHA256 7922eeb70637514b48a95dfe5eb1c25f8696920674010ff78f74b9314a91b536; distinct proof review SHA256 a493c5bae836a77507d30906cd19ddafe137cad108484b954fcd5d6a2dbcedb6; coordinator disposition SHA256 30a257c0518db273e2b30225994f31de96675c1b6535012e2fb91de00de33d16. These identities track accepted versions; they do not establish scientific truth or retroactively certify earlier incomplete procedures.
