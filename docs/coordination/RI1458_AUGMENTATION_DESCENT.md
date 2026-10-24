# RI1458: Covariance after forgetting additional state

The independently reviewed, root-accepted RI1457 theorem derives natural-label coherence from probability-preserving transport of complete augmented-history fibers under adjacent incomparable swaps. It carries the RI1451 target obstruction to that class without assuming a coarse Markov law or independent hidden choices.

This sufficient condition is not necessary. The immutable-mark scalar model satisfies it with mark-dependent probabilities under its complete-state and diamond premises. Arbitrary hidden, payload and continuous models remain unclassified.

## 1. Complete histories and labeled coherence

Fix a finite horizon N. Let H_n, 0<=n<=N, be finite or countable spaces of complete augmented histories, including all marks and hidden choices. Truncation r_n:H_(n+1)->H_n removes the last segment. Initial hidden choices are allowed, but every initial history projects to the empty unmarked order.

The weights rho_n(h)>=0 are normalized probabilities and satisfy

    sum_(h in H_0) rho_0(h)=1,
    rho_n(h)=sum_(g:r_n(g)=h) rho_(n+1)(g),   n<N.          (1)

They are not amplitudes or postselected weights. All positive branches are included. Let pi_n map histories to natural completed relations on birth labels [n]. A natural relation puts every predecessor before its successor in birth order. Require

    pi_n(r_n(g))=pi_(n+1)(g)|_[n].                         (2)

Each birth retains old vertices and completed relations and adds a maximal vertex above an actual ideal, a downward-closed subset of the parent. The projection forgets augmentation, not comparisons.

For a specified natural relation F define its complete fiber and mass:

    H_n(F)={h:pi_n(h)=F},
    W_n(F)=sum_(h in H_n(F)) rho_n(h).

Expanding (1)-(2), child fibers partition by their unique last-birth ideal S. Nonnegative countable summation gives

    W_n(F)=sum_(S in I(F)) W_(n+1)(F+S).                   (3)

Here F+S appends label n+1 above exactly S. This labeled prefix coherence needs no covariance or Markov projection. A zero history cannot have a positive extension under (1).

## 2. Full-fiber transport and descent

If adjacent labels i,i+1 are incomparable in F, swapping them gives another natural relation sigma F.

**Condition FT:** for every n<=N and each such swap, there is a bijection

    T:H_n(F)^+ -> H_n(sigma F)^+,
    rho_n(T(h))=rho_n(h),                                 (4)

where the superscript + means positive-weight histories. The inverse implements the reverse transport. Empty positive fibers must occur on both sides. Zero atoms may be ignored; positive branches may not.

Reindexing the complete nonnegative sum proves W_n(sigma F)=W_n(F). Linear extensions connect by adjacent incomparable swaps: move the desired first vertex leftward, crossing only incomparable vertices, then repeat on the suffix. A crossed predecessor would contradict the target extension; a crossed successor would contradict the original. Thus every natural realization of an anonymous order has equal mass.

For anonymous A let ell(A) count linear extensions and alpha(A) count automorphisms. Automorphisms act freely on natural-label bijections, so the distinct natural relations number b(A)=ell(A)/alpha(A). With mu_n(A) their total anonymous mass, descent forces

    W_n(F)=mu_n(A)/b(A)=alpha(A) mu_n(A)/ell(A),
                                                   F isomorphic to A. (5)

Individual swap equalities suffice; no microscopic group action is needed. Equations (3) and (5) give natural-label coherence.

## 3. Effective ratios without hidden strong lumpability

A natural relation F_n determines its whole unmarked chronological past: F_k=F_n|_[k], and the predecessors of label k determine its earlier actual ideal. Conditioning on that complete projected past is therefore conditioning on F_n itself.

At W_n(F)>0 the actual conditional law is

    q_eff(F,S)=W_(n+1)(F+S)/W_n(F).                        (6)

The child event implies the parent event; (3) normalizes the row. Products along supported projected histories telescope from W_0=1 to their terminal W. This works before FT, though the resulting probabilities may then depend on the natural-label presentation and fail diamonds.

With FT and positive anonymous mass on every type through N, (5) makes every natural parent and child positive. Ratios (6) have complete positive rows and transported parent/ideal equivariance. Two incomparable-birth routes to matched G both have product W_(n+2)(G)/W_n(F). Hence all scalar diamonds hold, including full first precursors: the second precursor excludes the other newborn and is proper in its intermediate parent.

These are the uniquely forced ratios in the positive scalar class described in [RI1456](RI1456_NATURAL_COHERENCE.md), through this horizon only. Hidden histories over the same F may have different next probabilities; (6) averages their posterior weights. It does not assert strong lumpability. Anonymous or lossy summaries need not encode their entire past. Ratios at zero parents are undefined.

## 4. A complete local certificate for FT

Write history weights as an initial weight times normalized conditional branch probabilities. Kernels may depend on the whole augmented past. For each adjacent coarse swap and each common augmented prefix, require both:

1. A bijection of all supported two-step branches in the two birth orders. It retains the prefix, projects to the swap, pairs every augmentation choice and preserves the product of the two conditional probabilities. Include every multiplicity and full first precursor.
2. Reversible continuation transport for each paired endpoint through the remaining horizon. At each later step, admissible branches correspond bijectively, have equal conditional probabilities, and project under the same vertex relabeling. The new endpoints again satisfy this condition.

Apply the two-step map after the common prefix, then transport the tail successively. Inverses recover each source history; complete coverage gives the destination fiber. The prefix weight, two-step product and every tail factor agree. Over all common prefixes this proves FT.

A complete augmented Markov state and transition-intertwining endpoint isomorphism suffice for continuation. Unmarked endpoint equality does not: future-relevant memory must be included or transported. Selected outcomes, unmatched lifts and local equality without tail control are insufficient.

## 5. Immutable marks may affect the birth probabilities

Consider the stipulated scalar model whose complete probability-relevant state is (F,r): the completed order and immutable vertex bits. Each branch has probability q(F,r,S)/2 for each newborn bit. Rows normalize, the rules are Markov in this full marked state and transported-equivariant, and every marked incomparable-birth diamond holds. There is no additional unrepresented memory or payload-dependent branch law in this corollary.

For fixed natural F, final bits specify a unique marked history. Swapping adjacent incomparable vertices with their bits invertibly pairs assignments. Earlier factors stay fixed; the complete marked diamond equates the two affected products, including factor 1/4 and full first precursors. The resulting full marked states are isomorphic, so Markov dependence and equivariance equate every later factor. The reverse swap recovers the history.

This constructs FT, including equality of positive supports when zero weights occur. It never factors q out of the mark sum or assumes q is mark-independent. Conditioning on an observed order may bias its marks; their actual history weights are transported.

Thus this normalized scalar marked model cannot realize the interior target below. The statement is conditional on the complete-state and full marked-diamond premises, not a derivation of those premises from DET. Arbitrary payload evolution is outside it.

## 6. Pair/triple obstruction and exact comparison target

Let anonymous triple masses (a,e,v,w,c) correspond to A:antichain, E:one edge plus isolate, V:one-bottom fork, W:one-top join, and C:chain. Let p be pair comparability. The natural counts of these triples are 1,3,1,1,1, giving natural weights a,e/3,v,w,c. In particular E has sole edge 1<2, 1<3 or 2<3.

The actual ideals of A2 contribute a,e/3,e/3,w: empty, each singleton separately, and full. Those of C2:1<2 contribute e/3,v,c: empty, bottom-only and full. Equations (3)-(5) require

    1-p=a+2e/3+w,       p=e/3+v+c.                         (7)

Uniformly selecting a pair from a completed triple separately gives

    p=(e+2v+2w+3c)/3,

by counting 0,1,2,2,3 comparable pairs in A,E,V,W,C. Combining this with (7) yields v=2w. Uniform induced sampling is an additional target condition, not natural last-birth deletion.

RI1451 uses finite nonempty templates T_j covering every finite nonempty order. Q_n^T pulls back their strict order along iid uniform types; repeated types stay distinct and incomparable. Its whole-world mixture is

    H_n=sum_(j>=1) 2^(-j-1) [Q_n^(T_j)+Q_n^(T_j^op)].

Fixed-subset iid restriction gives consistency and exchangeability; a matching template's bijective assignment proves full support. Dual pairing gives triple law (a0,e0,u0,u0,c0), positive with a0+e0+2u0+c0=1. No series is evaluated.

Let L_n use iid lower/upper types with lower probability 1/3, all lowers below all uppers and no within-level comparisons. Its triple law is (1/3,0,4/9,2/9,0). For the same fixed 0<lambda<1 across sizes, put

    P_n^lambda=(1-lambda)H_n+lambda L_n.
    v=(1-lambda)u0+4lambda/9,
    w=(1-lambda)u0+2lambda/9,
    v-2w=-(1-lambda)u0<0.                                 (8)

These laws retain full support and exact uniform induced restriction. For any N>=3, they cannot be realized by augmented histories satisfying (1)-(2) and FT: (7) contradicts (8). Positive microscopic weights everywhere are unnecessary; target positivity and descent supply coarse positivity.

More strongly, fixing the history/projection premises and those exact targets forces some aggregate adjacent-swap masses to differ. Otherwise equal natural weights would give the same contradiction. FT must fail somewhere, but its failure alone does not construct an escape. Calling a process non-Markov does not change the argument. Other augmented mechanisms remain unclassified. Accepted finite positive and nonnegative boundary results retain their scopes; no later-horizon boundary construction follows.

## 7. Two separating examples and a weaker coupling test

**Equal coarse masses without FT.** At horizon three put mass 1/3 on each natural one-edge history 1<2, 1<3, 2<3 and zero on other triples. Give prefixes their summed masses. Split exactly one terminal history into two hidden outcomes of weight 1/6 each. Its coarse mass is unchanged.

The natural law remains covariant. Its pair masses are C2=1/3 and A2=2/3; C2 chooses empty, while A2 chooses each singleton ideal with probability 1/2. Both mixed singleton route products equal 1/3. Yet a swap connecting the split and unsplit fibers would require a bijection between two positive atoms and one. FT therefore is not necessary for coarse covariance. This finite nonnegative example is not a strictly positive native candidate.

For two countable fibers with weights rho(h),rho(g), a weaker aggregate test is a nonnegative array C(h,g) whose row and column sums are those weights. Such a coupling forces equal total mass. Conversely, at common mass M>0,

    C(h,g)=rho(h)rho(g)/M

has the required marginals. At M=0 every nonnegative atom vanishes, and the zero array works, including empty fibers. Thus equal mass is equivalent to existence of this coupling. It supplies neither an atom bijection nor a local or physical transport mechanism.

**Anonymous endpoint information without covariance.** Give the same sole-edge histories weights 1/2,1/4,1/4 and all other triples zero, with consistent prefixes. The anonymous terminal is always E3, but the natural histories have unequal weights. The singleton row is (1/2,1/2); A2 chooses either singleton ideal with probability 1/2; C2 chooses empty with probability one. The mixed diamond products are

    (1/2)(1/2)=1/4,        (1/2)1=1/2.

Rows normalize while covariance fails. Birth-pair comparability is 1/2, whereas a uniformly induced pair from E3 is comparable with probability 1/3. This example does not also satisfy uniform pair-sampling consistency. It is a finite nonnegative logical separation, not a replacement law or full-support claim.

## 8. Scope, operational holds and evidence limits

FT is a sufficient microscopic transport condition; equal aggregate swap masses are the relevant necessary covariance condition for descent. Neither anonymous endpoint information nor isolated local equalities establish either one. Continuous fibers require specified measures and measurable transport, with disintegration assumptions where needed. Interfering amplitudes are not the nonnegative classical history weights used here. No unrestricted hidden/payload classification, all-horizon construction, physical derivation or successor answer follows.

E retains actual operator/actuator failure behavior and complete cost, latency and source-to-reset closure. NE retains source/reset/control/readout certification in both candidate worlds and history-wise full costs. CE retains interface ownership, implementation, runtime/allocator/enforcer and hard-resource gates, with M1 held. Measurement retains bounded record representation/serialization, source/build/ABI/binding, resources, controls, qualification and observed-execution holds. Its nominal calculation remains separate from calibration or production assurance; no new calibration or trace prerequisite is imposed on it.

The source has distinct authorship, review and root acceptance. Author drafts of 14,062/12,411 bytes exceeded its 12,288-byte cap; final size is 12,211. Reviewer drafts of 13,583/12,383 recovered to 12,219. Failed cap assertions are not prose readbacks. The author's original manifest digest came from current native checks, not a supplied external digest.

Author substantive completion is recorded at 10:05:43 UTC before 10:08:47. Declaration at 10:07:30 is not the attributed final completion at 10:08:12 before 10:14:47; its original all-four-file receipt is absent. Reviewer handoff reports prose/final clocks 10:49:38/10:51:10 before 10:58:16/11:04:16. Current pins do not reconstruct history.

Prior attributed completions, cap/rejected-patch and corrected reset-audit failures, missing RI1389 and late RI1401/RI1419 custody remain qualified. Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% stop/reset guard and RET-only pause remain. Publication supplies no physical prediction, execution permission or release receipt.
