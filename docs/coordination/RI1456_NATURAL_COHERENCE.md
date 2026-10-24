# RI1456: Natural-label coherence

The independently reviewed, root-accepted RI1455 theorem characterizes positive anonymous laws in a declared scalar maximal-birth Markov class. Complete diamonds force equal natural-history weights. These determine every row uniquely, and their actual-ideal sums must match parent weights.

Already at three births, simultaneous natural-history coherence and uniform induced pair sampling require v=2w, where v and w are the fork and join probabilities. Every interior RI1451 full-support mixture violates that equation. This excludes realization of those laws in the stated class, not arbitrary marked, hidden-state or payload-dependent mechanisms.

## 1. Class, horizon and positive domain

An anonymous order is an isomorphism type of a finite completed strict poset. Start at the empty order. At a parent F, choose an actual ideal S, meaning a downward-closed subset of its vertices, and append the next-labeled maximal vertex with exactly S as its strict past. Write F+S for the resulting child.

The scalar transition probability q(F,S) depends on the unmarked parent and ideal, with access to the whole unmarked parent allowed. It is Markovian and independent of marks and any additional hidden state. The requirements are:

- every actual ideal has positive probability and the complete row sums to one;
- probabilities are preserved by transporting parent/ideal presentations through order isomorphisms;
- every scalar diamond for two incomparable newborns holds after identifying endpoints, including full first precursors.

For horizon N, these requirements concern rows at sizes 0,...,N-1 and diamonds ending by N. Later rows are unspecified. These are stipulated mathematical premises, not a derivation from bare DET.

Let mu_n(F) be the intended probability of anonymous type F. Assume mu_0(empty)=1 and, at every size n<=N, a normalized law with positive mass on every anonymous type. This strict positivity is the domain of the equivalence theorem. A separate nonnegative boundary prefix will be checked directly, without extending that domain.

## 2. Natural labels and forced history weights

A natural labeling of an abstract n-vertex F is an order-preserving bijection to [n]={1,...,n}: predecessors receive smaller birth labels. An arbitrary sample labeling need not have this property.

Let ell(F) count linear extensions on a fixed vertex set, and alpha(F)=|Aut(F)| count order automorphisms. There are ell(F) natural-label bijections. Two produce the same relation on [n] exactly when they differ by an automorphism. The action is free, since an automorphism fixing a bijection fixes every vertex. Thus the number of distinct naturally labeled relations is

    b(F)=ell(F)/alpha(F).                                  (1)

Each natural relation has exactly one chronological actual-ideal history: at step k, choose the strict predecessors of k in its restriction to [k-1]. Conversely every maximal-birth history yields a natural relation.

Linear extensions connect by adjacent incomparable swaps: move the target extension's first vertex leftward in the other extension. A crossed predecessor contradicts the target ordering; a crossed successor contradicts the original. Repeat on the suffix.

At each swap the newborns have ideals in a common preceding parent. The complete diamond equates the two local products. Equivariance transports the subsequent history and equates its factors; earlier factors are unchanged. Full first precursors are included. The second precursor excludes the other newborn and is proper in its intermediate parent. Connectivity therefore proves equal probabilities for every natural realization of a fixed anonymous F.

Its anonymous mass forces each individual history weight to be

    w_n(F)=mu_n(F)/b(F)=alpha(F) mu_n(F)/ell(F).              (2)

Here w_n is a history weight, distinct from the lower-case triple probability w used below. For comparison, the exchangeable arbitrary-label version P_n of mu_n gives a specified labeled relation mass

    P_n(F_tilde)=alpha(F) mu_n(F)/n!,
    w_n(F)=[n!/ell(F)] P_n(F_tilde).                        (3)

There are n!/alpha(F) arbitrary labeled realizations. In particular, a natural two-chain has weight p, while each specified arbitrary chain orientation has probability p/2. Replacing one normalization by the other changes the problem. No terminal-sorting coupling is assumed in this counting proof.

## 3. Necessary and sufficient actual-ideal coherence

On the positive domain through horizon N, realization in the declared class is equivalent to

    w_n(F) = sum_(S in I(F)) w_(n+1)(F+S),
                       for every parent F, 0<=n<N.        (4)

The sum is over actual ideals of a specified natural parent. Different ideals give different labeled children, even if their anonymous types coincide. When (4) holds, the rows are uniquely

    q(F,S)=w_(n+1)(F+S)/w_n(F).                            (5)

For necessity, a specified child's unique history is its parent's history followed by that ideal. Its probability is w_n(F)q(F,S), and (2) fixes both the parent and child weights. This forces (5); complete row normalization then forces (4). Allowing the whole unmarked parent does not evade the equation.

For sufficiency, define (5). Positivity supplies positive entries and nonzero denominators; (4) gives row sums one. The weights depend only on order type, so parent/ideal transport gives equivariance. For either incomparable-birth route from F to a matched endpoint G, the two factors telescope to

    w_(n+2)(G)/w_n(F).

Thus every required diamond holds, including full-first/proper-second cases. A history from the empty state telescopes to w_n(F), since w_0=1. Summing over the b(F) distinct natural realizations recovers exactly mu_n(F).

This proves equivalence and uniqueness for the stated class and horizon. If a fixed positive family satisfies (4) at every size, the ratios give compatible finite chronological laws; no proposed solution of that infinite system follows. Zero parents and unrestricted marked/payload mechanisms are excluded from this sufficiency claim.

These weights differ from arbitrary-label maximal conditioning; see [RI1454](RI1454_MAXIMAL_NORMALIZATION.md).

## 4. The backward deletion kernel

Conditional on an anonymous terminal G, the natural law is uniform over its b(G) natural relations. It can be represented by a uniform linear extension of a fixed abstract G, because all automorphism classes have equal size.

For a specified maximal vertex z, appending z bijects extensions of G-z with extensions of G ending at z. Therefore

    Pr(z is last)=ell(G-z)/ell(G).

Nonmaximal vertices cannot be last. These probabilities sum to one. The anonymous backward kernel is

    D(G,F)=sum_(z maximal in G, G-z isomorphic to F)
                       ell(G-z)/ell(G).                   (6)

It deletes the last natural birth. To retain multiplicities, let m(F,G) count actual ideals of one specified natural F producing child type G. Counting natural labeled parent-child pairs in two ways gives

    b(F) m(F,G)=b(G) D(G,F).                               (7)

The left side counts all b(F) parent realizations and their m(F,G) ideal occurrences. The right side counts the fraction D(G,F) of the b(G) natural child relations whose last-label deletion has parent type F. Isomorphism transport makes m independent of the chosen parent presentation.

Multiplying (4) by b(F), grouping children by type and using (7) yields

    mu_n(F)=sum_G mu_(n+1)(G) D(G,F).                      (8)

Conversely, substitute (7) into (8) and divide by positive b(F) to recover (4). This is an exact equivalence.

D is not uniform arbitrary-vertex deletion. A fork V with one bottom and two leaves loses a leaf under D and always leaves a chain. Uniform vertex deletion instead leaves an antichain with probability 1/3. A join W with two bottoms and one top loses its top under D and always leaves an antichain; uniform deletion leaves a chain with probability 2/3. Consequently natural terminal coherence and uniform induced sampling are different requirements.

## 5. Complete pair/triple counts

Use A,E,V,W,C for antichain, one edge plus an isolate, one-bottom fork, one-top join and chain. Their anonymous triple masses are (a,e,v,w,c), summing to one. The letter a denotes probability, not alpha. Let p be anonymous pair comparability.

| Type | ell | alpha | Natural count b | Arbitrary-label count | Natural weight |
|---|---:|---:|---:|---:|---:|
| A2 | 2 | 2 | 1 | 1 | 1-p |
| C2 | 1 | 1 | 1 | 2 | p |
| A3 | 6 | 6 | 1 | 1 | a |
| E3 | 3 | 1 | 3 | 6 | e/3 |
| V3 | 2 | 2 | 1 | 3 | v |
| W3 | 2 | 2 | 1 | 3 | w |
| C3 | 1 | 1 | 1 | 6 | c |

Natural E has sole edge 1<2, 1<3 or 2<3. Natural V has bottom 1; W has top 3; C is 1<2<3; A has no edges.

Every actual ideal at the two pair parents contributes:

| Parent | Actual ideal | Child type | Child weight |
|---|---|---|---:|
| A2 | empty | A3 | a |
| A2 | {1} | E3 | e/3 |
| A2 | {2} | E3 | e/3 |
| A2 | full | W3 | w |
| C2:1<2 | empty | E3 | e/3 |
| C2 | {1} | V3 | v |
| C2 | full | C3 | c |

Both A2 singleton occurrences count. Full precursors remain in the equations, and V/W orientations must not be exchanged. The singleton row is (1-p,p). Coherence at the pair parents is precisely

    1-p=a+2e/3+w,
      p=e/3+v+c.                                          (9)

Given normalized triple masses these equations are equivalent. Independently, uniformly selecting two vertices from the completed triple counts respectively 0,1,2,2,3 comparable pairs in A,E,V,W,C. The induced pair requirement is

    p=(e+2v+2w+3c)/3.                                    (10)

Combining the second equation of (9) with (10) gives

    v=2w.                                                 (11)

Thus (11) is necessary for both coherences. For strictly positive pair/triple targets, with normalized masses and p supplied by (10), it is also sufficient through three births: (9) holds and the ratios in (5), including the singleton row, satisfy the theorem. It is not sufficient at later horizons or a characterization of all native sampling laws.

## 6. All interior RI1451 mixtures fail in this class

The comparison uses finite nonempty templates T_j covering every finite nonempty order. In Q_n^T, iid uniform types induce the template order; repeated types stay distinct and incomparable. Its whole-world background is

    H_n=sum_(j>=1) 2^(-j-1) [Q_n^(T_j)+Q_n^(T_j^op)].

Fixed-subset restriction retains the iid types and fixed component weights, proving exchangeability and consistency. A bijective assignment in a matching template gives each target positive mass. No series is evaluated.

Its triple law is h=(a0,e0,u0,u0,c0), with all four entries positive and a0+e0+2u0+c0=1. The equal V/W masses follow from pairing each template with its dual. Let L be the iid two-level law with lower probability 1/3 and all lowers below all uppers. Its triple law is (1/3,0,4/9,2/9,0). For the fixed interior mixture

    P_n^lambda=(1-lambda)H_n+lambda L_n,   0<lambda<1,

full support, exchangeability and uniform induced restriction remain valid. Its fork/join masses are exactly

    v=(1-lambda)u0+4lambda/9,
    w=(1-lambda)u0+2lambda/9.

Hence

    v-2w=-(1-lambda)u0<0                                  (12)

for every interior lambda. Only strict u0>0 is needed; no uniform numerical floor is asserted. The necessary condition (11) fails throughout this range.

The forced row defect is explicit. Put d=(1-lambda)u0/3>0. Using (10),

    sum_(S in I(C2)) w_3(C2+S)=p-d,
    sum_(S in I(A2)) w_3(A2+S)=1-p+d.

Full support gives 0<p<1. Dividing by parent weights, the forced chain row sums to 1-d/p<1, while the antichain row sums to 1+d/(1-p)>1. Altering these ratios cannot retain both the target laws and the declared complete covariance, because (2)-(5) uniquely force them.

This excludes every prescription in the declared class for these targets, not only RI1454's maximal conditioning. Any all-horizon realization in this class would require the impossible three-birth prefix. The comparison laws and their restriction identities remain valid. Other asymmetric targets, marked dependence, informative payloads and hidden-state mechanisms remain unclassified.

## 7. Separate boundary prefix and finite positive contrast

At lambda=1, the pure L target has

    (a,e,v,w,c)=(1/3,0,4/9,2/9,0),   p=4/9,

and satisfies v=2w. It lies outside the strict-positive theorem. A direct nonnegative construction only through three births is:

| Parent | Ideals in order | Probabilities |
|---|---|---|
| empty | empty | 1 |
| singleton | empty, full | 5/9, 4/9 |
| A2 | empty, {1}, {2}, full | 3/5, 0, 0, 2/5 |
| C2:1<2 | empty, {1}, full | 0, 1, 0 |

All rows normalize. The masses are A=(5/9)(3/5)=1/3, W=(5/9)(2/5)=2/9 and V=(4/9)1=4/9; E and C have zero mass. Parents through size two have positive weights, so the ratios telescope directly for every diamond ending by three. Both routes to E are zero. This verifies equivariance and those finite scalar diamonds without dividing by zero parents, asserting strict positivity, or providing later rows. These are not RI1454's K/s rows.

A different accepted finite target supplies a positive contrast. [RI1438](RI1438_FOUR_BIRTH_ADJUDICATION.md) has

    p=1/2,   (a,e,v,w,c)=(1,6,2,1,2)/12.

It satisfies v=2w and (9). The forced A2 row is (1/6,1/3,1/3,1/6), counting both singleton ideals; the C2 row is (1/3,1/3,1/3). RI1438 also admits a positive sampling-consistent extension through four births in its stated mark-independent scalar-passive model. That finite result remains unchanged and is not re-proved as an all-horizon claim here. Its nonunique fourth-birth choices share pair/triple summaries, but need not share the complete fourth-order law. Uniqueness for fixed complete laws therefore creates no contradiction.

## 8. Lift, operational gates and retained evidence limits

A common independent fair-bit scalar-passive lift multiplies each specified marked history by 2^(-n) and each two-step diamond by 1/4. Summing the bits returns the same unmarked rows and target law. It cannot remove (12) while remaining mark-independent. No conclusion about unrestricted marked, hidden-state or payload-dependent mechanisms follows. No successor answer is included.

This is conditional mathematics, without physical preparation, clock/readout, calibration, cost/reset mapping, experimental evidence or execution permission. E still needs actual operator/actuator failure behavior and full cost, latency and source-to-reset closure. NE retains source/reset/control/readout certification in both candidate worlds and full history-wise costs. CE retains interface ownership, implementation, runtime/allocator/enforcer and hard-resource gates, with M1 held. Measurement retains bounded record packing/general serialization, source/build/ABI/binding, resources, controls, qualification and observed-execution holds. Its nominal calculation stays separate from calibration and production assurances; no new calibration or trace prerequisite is imposed on that calculation.

The source has distinct authorship, review and root acceptance. Author drafts of 13,476 and 12,425 bytes exceeded its 12,288-byte cap; a patch was rejected. The final report is 12,142 bytes. The rejected-patch readback's claimed equality to an earlier draft remains an author comparison. The review recovered 12,781 bytes to 12,211. These failures remain recorded.

Recorded author prose completion at 08:59:26 UTC preceded its 09:06:40 cutoff. Declaration at 09:01:22 is not the attributed completion at 09:01:57 before 09:12:40; the original final all-four-file receipt is absent. Reported reviewer prose/all-file clocks 09:49:41/09:51:41 precede 09:58:31/10:04:31. Current hashes do not reconstruct history.

The root's initial audit rejected a timestamp within the authorized one-second reset pair; the corrected audit retains that failure and applies only the existing exception. Earlier cap/display/schema/patch and missing/late custody qualifications persist, including missing RI1389 and late RI1401/RI1419 evidence. Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% guard and RET-only pause remain. Publication does not supply a release receipt or authorize execution.
