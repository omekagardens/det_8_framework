# Finite source, order, return and visibility

Three finite classical constructions establish different parts of a source–geometry comparison. GDM044 makes an unmarked order statistic depend on a conserved charge under a common prepared reference. GDM045 makes a later source-allocation update depend on a prepared parent order, and E042 determines which observations expose that difference. GDM047 supplies one common law supporting both response directions, with changed reference-memory dynamics and explicit preparation/access premises. These are conditional finite results; they do not establish an autonomous feedback cycle, physical mass, curvature or units.

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

## One common law with retained reference information: GDM047

GDM047 answers a compatibility question left open by the separate GDM044 and GDM045 constructions. It keeps GDM044's full eight-coordinate domain, first maps and effect rows while changing the explicitly permitted second-step reference output. It then gives a complete third-birth witness and a lawful source-return comparison. The old reset instrument remains the separate GDM044 model; its latent dynamics are not asserted unchanged.

Put u=(1/2,1/2)^T and v=(1/2,-1/2)^T. With the f rows above, replace the second reference blocks by

    C_s^q = u f_s^q + tau_s^q v(1,-1),
    B_(s,b) = diag(C_s^0, M0 tensor C_s^1, C_s^2)/2.

The fixed tau values, in order (E0,F0,E1,F1,E2,F2), are (4/9,1/9,1/3,1/6,4/9,1/9). They obey |tau_s^q|<min(f_s^q). Each block has the original column effects and row sums q_E=2/3 or q_F=1/3. The complete nonselective reference maps are T0=T2=M(0,5/9), T1=M0. They retain information rather than reset to uniform.

For every joint input nu, including correlated and boundary states, each complete two-birth history has operator

    W_h = diag(C_s^0, M0^2 tensor C_s^1, C_s^2)/4,
    P_nu(s,b1,b2) = sum_(i,m) nu[i,m] f_s^(Q_i)[m]/4.

Thus the entire eight-cell observed prefix, the common-reference chain probabilities and the separate independent-uniform-reference control are exactly those of GDM044. The joint outputs differ. For example, sector0 input reference delta0 gives E-reference (17/18,1/18), F-reference (11/18,7/18), and nonselective reference (7/9,2/9). Restoring delta0 for another trial remains a supplied resource.

For every size-two parent C and actual ideal S, define

    A_(C,S) = p_C(S) diag(R^0, H tensor R^1, R^2),
    B_(C,S,b) = A_(C,S)/2,
    R^q = M(x_q,t_q).

Every actual ideal and both newborn bits are retained. The two antichain singletons are separate outcomes with the same row:

| Parent / ideal | p | (x0,t0) | (x1,t1) | (x2,t2) |
| --- | ---: | --- | --- | --- |
| antichain / empty | 3/8 | (-7/24,1/8) | (0,1/8) | (7/24,1/8) |
| antichain / each singleton | 1/8 | (7/8,1/16) | (0,1/8) | (-7/8,1/16) |
| antichain / full | 3/8 | (-7/24,1/8) | (0,1/8) | (7/24,1/8) |
| chain / empty | 1/4 | (-1/2,1/8) | (0,1/8) | (1/2,1/8) |
| chain / root | 3/8 | (1/6,1/8) | (0,1/8) | (-1/6,1/8) |
| chain / full | 3/8 | (1/6,1/8) | (0,1/8) | (-1/6,1/8) |

In the witness H=M(0,3/4) at chain/full and H=M0 elsewhere. In the complete cut H=M0 everywhere; every other parameter, including the entire reference-memory prefix, is identical. Each map has 24 positive entries and 40 cross-charge zeros. Branch effects are p[1+sigma_m x_q]/2, where sigma_0=1 and sigma_1=-1. Weighted x values sum to zero at each parent, so complete normalization holds on the entire joint cone. Row sums give uniform branch anchors p/2. The same source/reservoir exchange ledger and assigned zero reference charge preserve Q pathwise, conditional on the same event, and unconditionally; none of these statements assigns physical energy to the reference.

All full unnormalized marked diamonds through three births hold. In the nontrivial mixed singleton-base diamond, both scalar factors are (1/8)(2/3)/4=(1/4)(1/3)/4=1/48, and the common full matrix is

    diag(M(1/3,1/24), M0^2 tensor M(0,1/16), M(-1/3,1/24))/48.

Equal-ideal and empty-base pairs also agree; common allowed suffixes preserve their equality. Old full singleton ideals transport to the proper chain root. Chain/full cannot be the second event of such an incomparable pair because its past includes the preceding newborn. Coefficients depend on the current unmarked parent and actual ideal role, never old marks or external setting labels. Size three is terminal.

The controlled return test supplies the same marked singleton and arbitrary joint nu to both settings. Each retained preparation bit has map I8/2, preserving the entire joint input; this is an external append preparation, not the native second birth. With lambda_s=1/2, the full augmented law is

    P(s,k,S,b,j,n|nu) = (lambda_s/2)[B_(C_s,S,b)nu]_(j,n).

All 224 cells, including every zero and complement, are retained and sum to one. The terminal joint-basis access is supplied, not a constructed native detector. For nu=delta10 tensor delta0, summing every native outcome and preparation bit gives witness source probabilities (0,51/64,13/64,0) at chain and (0,3/4,1/4,0) at antichain. Both have reference output (9/16,7/16). The allocation return is 3/64, with the opposite reservoir response and unchanged total Q.

The complete cut obeys

    L G_chain^cut = L G_antichain^cut = K L

as four-by-eight operators on all joint inputs, including correlations and mixed charges. This removes source return for every input, although outer-sector reference outputs can still differ. Both families preserve the complete autonomous forward prefix after the third outcomes are forgotten. The two response directions therefore coexist in one declared finite law under two explicit experiment contracts. This does not close an autonomous feedback loop or derive an operational gravitational response. E042's observation theorem remains specific to GDM045; it has not been transferred to GDM047.

## What remains a premise

The binary terminal effect is a mathematical channel, not a constructed native receipt, passive access to hidden j, or a calibrated detector. A committed allocation-sensitive readout needs its own outcome-resolved interaction and record-access design, native consistency checks and physical preparation/readout cost account. The [observer and preparation note](finite_observer_records_and_preparation.md) concerns a different declared receipt model; it cannot be silently appended here.

The numerical laws, finite supports, factorization/reference conventions and external preparations are supplied assumptions. Conservation and the displayed response laws are derived conditional relations. Naming Q a mass, counting births as duration or supplying a scale multiplier does not derive physical units. No metric, acceleration, inertia, physical energy, action scale, calibration, empirical evidence, efficiency, autonomous feedback or whole-route qualification is claimed. A conventional comparator must receive the same information, setting labels and preparation/access resources.

The separate GDM044/GDM045 constructions left the coexistence question open. GDM047 now supplies one conditional common-law witness by changing the explicitly permitted reference output and declaring a joint preparation/access contract. A gravity or mass bridge still needs an operational target and justified additional premises. No further model, horizon extension or empirical execution is authorized by this note.

## Source custody

GDM044 report SHA256 47522873f2e397a6803f30fd45108b019c56bbe4f198eb8285541014debcccda; coordinator disposition 407ed24e0903ad99e399899c641703715cb98ff5115260e3b12a4c3cd1d31178.

GDM045 report SHA256 8d29be8ac7b57a9c161d0ced1ee2af7af89edf896efdcd03d6212f6e5318261e; coordinator disposition b7cb4f0736f9d8c036389b4850d9f87c8611853408b480817c31a2aa9fa7ff06.

E042 report SHA256 754ab2a66236e5eef3dfe8b69c2d05141a2feab675704bc593c630ac41810860. Its original review missed its saved-readback cutoff; that procedural failure remains permanent. E33 separately adopted the unchanged theorem after a fresh distinct content review (SHA256 264362811f4cd791fbe5afabaf90101570082d119cac26bee70fa987b0926114); coordinator disposition SHA256 4204f54755ab80a4f8f4080f5d4f067ee684e65bb8616d974e989e1a4fad5321. This does not retroactively qualify the original failed review. Hashes establish source identity, not scientific truth.

GDM047 report SHA256 f10b500a4972bf4800655828969175a848cb9ae95292e4b38a8d03b26573f66f; independent proof review SHA256 670caf84c867d804b713d5a6adf3debf3ba7f8e359faf688986cdc26c7bf3451; E34 coordinator disposition SHA256 77ad0e162a2745f2ed858300bee24fd8c2cbb2c99380c0ea0248ce0f9deddf6d. The E33 root dispatch clock bracket straddled its substantive cutoff, so its exact dispatch timing remains uncertified. The author and reviewer completed within their own prospective deadlines; E34 acceptance does not retroactively certify that root dispatch or any earlier failed procedure.
