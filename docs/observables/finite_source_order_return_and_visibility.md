# Finite source, order, return and visibility

Two distinct finite classical constructions establish different parts of a source–geometry comparison. GDM044 makes an unmarked order statistic depend on a conserved charge under a common prepared reference. GDM045 makes a later source-allocation update depend on a prepared parent order while preserving total charge. E042 determines exactly which observations expose that second difference. These results do not combine the two constructions into one autonomous feedback law, or establish physical mass, curvature or units.

## Conserved charge changes committed order: GDM044

Use source coordinates i=(00,10,01,11), r=(0,1,0,1), e=(0,0,1,1), and Q=r+e=(0,1,1,2). Add a reference bit m. States are columns on the entire Delta8, including correlated and boundary states. Target preparations are rho tensor delta0; the distinct reference control is rho tensor u, u=(1/2,1/2). Both product families are narrower than the validity domain.

Set

    M0=[[3/4,1/4],[1/4,3/4]], K=diag(1,M0,1),
    J=u(1,1), L=I4 tensor (1,1).

The first birth, with bit b, has map F_b=(K tensor I2)/2. At either marked singleton, the second birth chooses actual ideal s=E (empty) or F (full) and bit b. Its maps are

    C_s^(q)=u f_s^(q),
    A_(s,b)=diag(C_s^0,M0 tensor C_s^1,C_s^2)/2.

Here q is the conserved source sector. The complete effect table is:

| q | f_F^(q), reference inputs 0,1 | f_E^(q), reference inputs 0,1 |
| --- | --- | --- |
| 0 | (1/2,1/6) | (1/2,5/6) |
| 1 | (1/3,1/3) | (2/3,2/3) |
| 2 | (1/6,1/2) | (5/6,1/2) |

Equivalently, A_(s,b)[j,n;i,m]=K[j,i] f_s^(Q_i)[m]/4 for each final n. The full instrument sums are K tensor I2 and K tensor J; each is column stochastic. Their source marginals separately satisfy L sum F=K L and L sum A=K L. Every positive source transition preserves Q; the exchanges 10->01 and 01->10 have signed (Delta r,Delta e)=(-1,+1) and(+1,-1). All reference transitions are retained but assigned zero Q charge. This is a bookkeeping assumption, not zero physical reference energy.

Each F_b has 12 positive entries and 52 zeros; each A_(s,b) has 24 positive entries and 40 cross-sector zeros. Structural outcomes have positive mass throughout Delta8, so closure uses their full probability; microscopic zero events have no conditional state. With w8=(1,1,1,1)/4 tensor u, the branch anchors are F_b w8=w8/2, A_(E,b)w8=w8/3 and A_(F,b)w8=w8/6.

Fix natural birth labels. The complete observed history is h=(s,b1,b2): eight cells, with no latent source/reference labels. For any initial joint nu,

    H_h[j,n;i,m]=(K^2)[j,i] f_s^(Q_i)[m]/8,
    P_nu(h)=sum_(i,m) nu[i,m] f_s^(Q_i)[m]/4.

The sum over all histories and final coordinates is one. For the same prepared reference delta0 at every source,

    P(chain)=rho00/2+(rho10+rho01)/3+rho11/6.

Sources delta10 and delta01 have identical complete eight-cell laws. The endpoint sources delta00 and delta11 have chain probabilities 1/2 and 1/6. Chain versus antichain is an unmarked order projection of the committed two-event graph, not a latent-coordinate readout. Independently, for EVERY rho tensor u, each E bit-pair cell has probability 1/6 and each F cell 1/12. A uniform marginal with initial correlations is not this independent reference control.

The only incomparable two-birth base is empty. Both transported compositions equal

    A_E F=diag(C_E^0,M0^2 tensor C_E^1,C_E^2)/4

for every pair of newborn bits, as full unnormalized matrices. Common terminal projections preserve the equality. There is no third-birth suffix in this model. Maps are independent of old marks, transport under marked isomorphisms, and append one maximal event over the selected ideal without changing old records. These checks concern this finite support, not arbitrary horizons.

After the second birth the reference is uniform and uncorrelated with the conditioned source on every branch, including initially correlated inputs. The supplied delta0 reference is not restored. Repetition requires preparation/reset resources. Source conservation compares before and after conditioned on the SAME event; a selected mixed-sector posterior need not equal the unconditional prior.

## Prepared parent order changes allocation: GDM045

This is a DIFFERENT law on Delta4, with three births and no reference bit. It does not inherit GDM044's selective maps. Define

    M(x,t)=[[1+x+t,1-x-t],[1+x-t,1-x+t]]/2,
    D(x,t)=diag(1,M(x,t),1),
    B_(C,S,b)=q_C(S) D(x_C,S,t_C,S)/2,
    a=1/8448.

Both native bits remain distinct outcomes. The complete branch table is:

| Parent and actual ideal | q | x | t, witness | t, cut |
| --- | ---: | ---: | ---: | ---: |
| empty, sole ideal | 1 | 0 | 1/2 | 1/2 |
| singleton, empty | 2/3 | a | 1/2 | 1/2 |
| singleton, full | 1/3 | -2a | 1/2 | 1/2 |
| two-event antichain, EACH of its four ideals | 1/4 | 0 | 1/2 | 1/2 |
| two-event chain, empty | 1/2 | 6a | 1/2 | 1/2 |
| two-event chain, root singleton | 1/4 | 0 | 1/2 | 1/2 |
| two-event chain, full | 1/4 | -12a | 3/4 | 1/2 |

Every parent has sum q=1 and sum qx=0. Branch effects are (q/2)(1,1+x,1-x,1), independent of t. All maps are nonnegative with six positive source entries and ten cross-Q zeros; each preserves the uniform anchor up to q/2. The complete sums normalize on the full simplex. Q is preserved on each microscopic transition, with the same signed source/reservoir exchange ledger. Both witness and cut satisfy the finite support, closure, covariance, append, conservation and full unnormalized marked-diamond requirements.

At the singleton-base diamonds, transporting an old full ideal after an incomparable birth makes it the proper root ideal of the chain. The changed chain/full map cannot be the second map of such a diamond. The mixed-ideal identity uses M's triangular representation [[1,x],[0,t]] and -2a+3a=a; both-empty and both-full cases use unchanged matching maps. All common allowed terminal suffixes preserve equality. The empty-base diamond is unchanged. Size three is terminal. This explains why changing the specified full-past branch gives a lawful comparison at this scope, without claiming unlimited freedom to modify growth laws.

The return experiment is externally controlled. Begin with the same marked singleton and source rho. An explicit source-identity preparation appends an incomparable or a chain event, with retained preparation bit k and map I4/2 for EACH k. The setting s is externally selected with lambda_s=1/2. This is a supplied preparation operation, not an autonomous native transition or a physical apparatus. For the next native birth and terminal source basis j, the complete augmented law is

    P(s,k,S,b,j|rho)=(lambda_s/2)(B_(C_s,S,b) rho)_j.

All ideals, bits, final coordinates, zeros and complements remain. The summed antichain source map is D(0,1/2). The chain map is D(0,9/16) in the witness and D(0,1/2) in the cut. For rho=delta10, source r has final expectation 3/4 at antichain, 25/32 at witness chain, and 3/4 at cut chain. The matched-parent return contrast is therefore 1/32, with zero in the complete lawful comparison. Total Q has not changed. The first two autonomous native births are identical between witness and cut.

## Which records expose that return: E042

For the same known rho in both laws, put d=rho10-rho01 and v=(0,1,-1,0)^T. The ONLY changed branch, chain/full for each b, obeys

    Delta B=(v v^T)/64, Delta B rho=(d/64)v,
    1^T Delta B=0.

Forget j. The complete controlled native record D=(s,k,S,b) has probability q(1+xd)/8 in both families. For each actual k,b its rows are:

| Parent/ideal | Probability | Number of k,b pairs per actual ideal |
| --- | --- | ---: |
| antichain, each of four ideals | 1/32 | 4 |
| chain, empty | (1+6ad)/16 | 4 |
| chain, root | 1/32 | 4 |
| chain, full | (1-12ad)/32 | 4 |

These are all 28 cells and sum to one. This compares witness with cut at the same setting and preparation, not chain with antichain settings.

For the autonomous three-birth experiment there is no external preparation. If the second ideal u has (q_u,x_u)=(2/3,a) or (1/3,-2a), and the third actual ideal V has the table's (q_V,x_V), every labelled bit triple has probability

    (q_u q_V/8)[1+(x_u/2+x_V/4)d].

There are 32 antichain-prefix and 24 chain-prefix histories. All 56 probabilities agree between witness and cut after terminal j is forgotten. Their sum is one by sum_V q_V x_V=0 and sum_u q_u x_u=0. This family-specific equality does not imply that all native records are independent of the source or that all possible laws are observationally equivalent.

Now SUPPLY a common terminal binary effect ell, with each entry in [0,1], e1=ell and e0=1-ell. In the controlled experiment the full law becomes

    P_F(s,k,S,b,y|rho)=(lambda_s/2)e_y B_F rho.

Summing both y restores the 28-cell law; all 56 augmented cells and zero outcomes are retained. Only the chain/full cells differ. For each k,b,

    Delta P(c,k,full,b,1)=d(ell10-ell01)/256,
    Delta P(c,k,full,b,0)=-d(ell10-ell01)/256.

Thus the full augmented laws differ if and only if d(ell10-ell01) is nonzero. Q-only effects have ell10=ell01 and cannot distinguish them. Even an allocation-sensitive effect fails when d=0. A known distribution rho does not give access to its realized initial decomposition label; adding that label changes the experiment.

For delta10, ell=r is a supplied separating example. After conditioning only on the declared chain setting, y=1 has probabilities 25/32 and 3/4, with complements 7/32 and 1/4. With the setting weight retained, the chain/y=1 joint difference is 1/64. The complete cell law above establishes distinction without selecting a successful outcome.

## What remains a premise

The binary terminal effect is a mathematical channel, not a constructed native receipt, passive access to hidden j, or a calibrated detector. A committed allocation-sensitive readout needs its own outcome-resolved interaction and record-access design, native consistency checks and physical preparation/readout cost account. The [observer and preparation note](finite_observer_records_and_preparation.md) concerns a different declared receipt model; it cannot be silently appended here.

The numerical laws, finite supports, factorization/reference conventions and external preparations are supplied assumptions. Conservation and the displayed response laws are derived conditional relations. Naming Q a mass, counting births as duration or supplying a scale multiplier does not derive physical units. No metric, acceleration, inertia, physical energy, action scale, calibration, empirical evidence, efficiency, autonomous feedback or whole-route qualification is claimed. A conventional comparator must receive the same information, setting labels and preparation/access resources.

The two constructions leave a concrete joint-model question: can conserved-source influence on committed order and order-conditioned source return coexist under one exact preparation, law and observation contract? Their separate acceptance does not answer it. No additional model or extension is authorized by this note.

## Source custody

GDM044 report SHA256 47522873f2e397a6803f30fd45108b019c56bbe4f198eb8285541014debcccda; coordinator disposition 407ed24e0903ad99e399899c641703715cb98ff5115260e3b12a4c3cd1d31178.

GDM045 report SHA256 8d29be8ac7b57a9c161d0ced1ee2af7af89edf896efdcd03d6212f6e5318261e; coordinator disposition b7cb4f0736f9d8c036389b4850d9f87c8611853408b480817c31a2aa9fa7ff06.

E042 report SHA256 754ab2a66236e5eef3dfe8b69c2d05141a2feab675704bc593c630ac41810860. Its original review missed its saved-readback cutoff; that procedural failure remains permanent. E33 separately adopted the unchanged theorem after a fresh distinct content review (SHA256 264362811f4cd791fbe5afabaf90101570082d119cac26bee70fa987b0926114); coordinator disposition SHA256 4204f54755ab80a4f8f4080f5d4f067ee684e65bb8616d974e989e1a4fad5321. This does not retroactively qualify the original failed review. Hashes establish source identity, not scientific truth.
