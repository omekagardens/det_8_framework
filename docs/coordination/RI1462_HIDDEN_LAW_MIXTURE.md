# RI1462: A covariant five-birth mixture without record sufficiency

Accepted RI1461 constructs a conditional five-birth witness with full probability-preserving history transport but unequal next-record laws at identical committed records when the retained selector is known. Forgetting the selector gives the admitted marked t=3/4 prefix; forgetting marks requires a separate posterior average.

L1 scaling, general record sufficiency and augmentation descent are prior results. This particular witness supplies neither a DET-derived baseline/physical selector nor a sixth-birth law.

## 1. Exact model and horizon

Write C=(F,r): F is a completed order with predecessors earlier in birth order, and r gives immutable vertex bits. An actual ideal S is downward-closed; F+S appends a maximal vertex above exactly S, retaining old comparisons.

Fix an admitted scalar-passive prefix q(C,S) with rows at parent sizes 0 through 4, hence five births. Every actual ideal has positive probability; rows normalize. Proper-ideal locality permits whole-unmarked-parent access but restricts mark dependence to the precursor record. The full complement may depend on all marks.

Assume transported marked equivariance, all contained incomparable-birth diamonds, fair newborn bits, and complete-state Markov dependence on C, without unrepresented memory or payload-dependent probabilities. These are model premises, not consequences of immutability or Status-M ontology.

[Law Dependence, historical §2](../track_b/native_theorem_package_v1/LAW_DEPENDENCE.md), proves L1: at a fixed last layer, common 0<t<=1 scales proper entries by t and replaces full a by 1-t+ta. It preserves the admitted prefix, including full-first diamonds, without retaining old later rows.

## 2. The two components and their complete histories

Retain an uncommitted immutable selector z in {0,1}, initially half/half and independent of fair mark draws. Set t_0=1, t_1=1/2 and fix the same arbitrary payload D in both components. Random choices are z and birth branches; z is neither agency nor a stored outcome.

For parent size k<4, let q_z(C,S)=q(C,S). At k=4 define

    q_z(C,S) = t_z q(C,S),                  S proper in F,
    q_z(C,F) = 1-t_z+t_z q(C,F).             S=F.

Append above S and attach bit b in {0,1}, with branch probability q_z(C,S)/2. The augmented predictive state is (C,z); conditional on z, C is complete. There are no parent-five transitions.

For every complete augmented history h=(z,S_1,b_1,...,S_n,b_n), 0<=n<=5, put

    rho_n(h) = (1/2) product_(j=1..n) [q_z(C_(j-1),S_j)/2].

Include all ideals and both marks without postselection. At the changed layer, proper mass t_z(1-a) plus full mass 1-t_z+t_z a is one. Summing both bits preserves this sum. Each parent's children therefore sum to its mass; induction from the initial half/half law proves normalization and prefix consistency.

All factors are positive. At a nonempty parent, 0<a<1, and each full/proper alternative remains below one. At the empty parent the only ideal has probability one; its two marked branches each have probability 1/2. Projection to old birth labels commutes with truncation because births retain relations and marks.

Under the model's terminal payload identifications, the whole branch map is

    M^z_(C,S,b)(D) = [q_z(C,S)/2] D

for every complex positive-semidefinite payload D. Each map preserves positivity and the complete branch sum is identity on the passive payload. This is a conditional scalar calculus, not a physically derived quantum instrument.

## 3. Every contained diamond

A contained diamond has base size at most three. Below size three, both factors are unchanged. At a marked base C of size three, take independent precursors S,T in its unmarked parent, with arbitrary fixed old/newborn marks. Each second precursor excludes the other newborn and is therefore proper in its size-four parent. Both routes gain exactly one t_z:

    q(C,S) t_z q(C+x_S,T)
      = q(C,T) t_z q(C+y_T,S).

The mark arguments are suppressed only in this display; the baseline equality holds for every marking. It includes S=F, T=F and S=T. A full first birth occurs at size three and remains unchanged; its second precursor is still proper at size four.

Both newborn factors give D/4 times the route products, equal for every payload. Constant parent/mark-independent scaling preserves proper locality and equivariance; the full complement retains its permitted mark dependence. This proves each component's finite admission by L1.

## 4. Same records, different selector-conditioned laws

For n<=4, restrictions of C_n determine its marked history. Its unchanged rows give the same positive conditional likelihood in both components, hence

    P(z=0 | C_n) = P(z=1 | C_n) = 1/2.

This posterior is proved from prefix agreement. It is not an assumption that a hidden selector stays independent after arbitrary observations.

Fix any marked C_4. Write a=q(C_4,F), so 0<a<1, and choose a proper ideal S with d=q(C_4,S)>0. The next-ideal laws are

| Ideal | z=0 | z=1 |
|---|---:|---:|
| Proper S | d | d/2 |
| Full F | a | (1+a)/2 |

A specified newborn bit halves each entry. Both equal-C states are reachable under one augmented rule and common protocol, but their next-precursor laws differ. Thus record-only sufficiency fails by the existing criterion summarized in [RI1460](RI1460_PRIMARY_ASSUMPTIONS.md). The selector is explicit, not an omitted controller change.

After observing the fifth ideal, Bayes gives

| Observation, conditional on C_4 | P(z=0) | P(z=1) |
|---|---:|---:|
| A specified proper ideal | 2/3 | 1/3 |
| The full ideal | 2a/(1+3a) | (1+a)/(1+3a) |

Likelihood ratios are d:(d/2) or a:(1+a)/2; a specified fair bit cancels. Denominators are positive and rows normalize. Since a<1, the full branch favors z=1.

The full natural marked fifth record retains its parent and ideal, so the formulas apply there too. Anonymous/mark-erased conditioning requires averaging. Neither selector fixes the outcome, and posteriors supply no later kernel.

## 5. Actual full-history transport, including every tail

Fix n<=5 and adjacent labels i,i+1 incomparable in a final natural order F. Here (z,F,r) uniquely determines the augmented history: restrictions reconstruct every earlier marked state and ideal.

Define T by swapping those two vertices, carrying their marks with them, leaving z fixed, and reconstructing the full history from (z,sigma F,sigma r). Incomparability makes the swapped birth order natural. Strict positivity makes every resulting history admissible.

The prefix agrees; the complete marked diamond equates the pair's factors, including full first precursors. The resulting full marked states are isomorphic with the same z. At every later birth, sigma carries the ideal and newborn mark to its counterpart. Complete-state Markov dependence and equivariance equate each suffix probability and scalar map.

This explicitly includes the changed parent-four factor when the swap occurred earlier: proper scaling and the full-complement rule are equivariant at that size. A swap of births four and five instead uses the base-three diamond and has no suffix.

The reverse swap is inverse and covers every marking and both selector atoms. Initial weights and all rho_n factors are preserved, as are the composed payload maps. This proves atomwise FT on complete fibers through the horizon; mixture-mass equality alone would not supply the map and tails.

## 6. Forget the selector while retaining marks

Let g_n(C)=sum_z rho_n(z,C). At parent four the conditional selector weights are exactly half/half, giving

    bar_q(C,S) = (3/4) q(C,S),                 S proper,
    bar_q(C,F) = 1/4+(3/4) q(C,F).

Earlier rows remain q, and marked branches have probability bar_q/2.

For n<=4 the marked histories already agree. Each fifth-birth history has four common factors and one changed factor; averaging the latter gives bar_q/2. Thus its entire product equals q^(3/4), not only an endpoint marginal.

L1 gives this marginal positivity, normalization, proper locality, equivariance and all contained marked diamonds, with bar_q in the payload maps. This uses the common prefix and single changed layer, not an admission theorem for arbitrary mixtures.

The autonomous marginal predicts after averaging the prescribed prior. It does not equate the two selector-conditioned laws above. An admitted marked marginal and failure of full-state record sufficiency coexist.

## 7. Then forget marks: a different conditional average

Write g_n(F,r) for the marked mass and define

    W_n(F) = sum_r g_n(F,r),
    eta_n(r | F) = g_n(F,r)/W_n(F).

Every natural order and marking through five has positive mass. At parent size n<=4, summing the child mass over old marks r and both newborn bits yields

    W_(n+1)(F+S) = sum_r g_n(F,r) bar_q(F,r,S),
    q_eff(F,S) = W_(n+1)(F+S)/W_n(F)
               = sum_r eta_n(r | F) bar_q(F,r,S).

The newborn-bit sum removes its factor 1/2. Fair newborn draws do not make old marks uniform conditional on the observed order. Mark-dependent q remains inside the sum.

At parent four this becomes (3/4) sum_r eta_4 q(F,r,S) for a proper S, and 1/4+(3/4) sum_r eta_4 q(F,r,F) for the full ideal.

Complete transport of the (z,r) fibers gives natural covariance after summation. Prefix consistency gives labeled coherence

    W_n(F) = sum_(S in I(F)) W_(n+1)(F+S).

The natural relation retains its projected past by restrictions. Thus q_eff is its actual positive normalized conditional row. Covariance gives transported equivariance; two contained routes telescope to the same terminal/parent mass, giving the contained unmarked scalar diamonds, as in [RI1458](RI1458_AUGMENTATION_DESCENT.md).

No microscopic strong lumpability over z/r or automatic transfer of every marked locality restriction is asserted. Nor is uniform induced sampling or an RI1451 target law supplied.

## 8. Why this is not a sixth-birth law

No transition from parent five was defined. To see why old rows cannot simply be retained, suppose an old admitted continuation existed. At a changed parent of size four, take a mixed full/proper diamond with old factors

    a=q(F,F), b=q(F,S),
    c=q(F+x_F,S), d=q(F+y_S,F),     ac=bd.

Both second precursors are proper in their intermediate parents. If only the size-four layer is changed by 0<t<1 while the old next layer is retained, the route difference is

    [(1-t)+ta]c - tbd = (1-t)c > 0.

Multiplying both proper next-layer factors by a common t'>0 leaves t'(1-t)c>0. This applies to the changed component and to a naive continuation of the t=3/4 marginal. It does not prove that every separately rebuilt extension is impossible.

This conditional covariant witness supplies no physical selector, all-horizon law, informative QM, agency, geometry/readout, application advantage or RI1451 solution. Accepted fixed-law and obstruction results remain. The Bayesian-mixture locality continuation is open.

## 9. Source and process boundaries

The literal source grant was read without following linked implementations or theorem packages. Historical LAW_DEPENDENCE is a 17,936-byte body, SHA256
`68c38eeb7232f7fd471c6a6bbf74316350408031cbdbd849495ff890a534444a`.
It remains intact once at zero-based byte 5,597, line 40, in the supplied expanded public LAW_DEPENDENCE. Its §2 is the L1 source; FINITE_LAW_DEPENDENCE is a different work.

RI1461 author prose completion is recorded at 12:03:31 UTC before 12:09:43. Preparation at 12:05:08 is not final completion: 12:05:25 before 12:15:43 remains attributed because the original final all-four receipt is absent. Reviewer prose is recorded at 12:48:40 before 12:59:24; final all-nine 12:50:05 before 13:05:24 is attributed to its supported handoff, without the original external receipt here. Declaration at 12:49:51 is not completion.

The author recovered a nonzero existence test by verifying its reservation was empty, and retained a superseded report/random-choice clarification. No current author cap or reviewer check failure is reported. Root's display recovery and inherited cap/patch/display/schema/manifest-pin-basis, attributed-completion, missing RI1389 and late RI1401/RI1419 limits persist. Current hashes do not reconstruct history.

E retains actual failure behavior and complete cost, latency and source-to-reset closure. NE retains source/reset/control/readout certification in both worlds and history-wise costs. CE retains interface ownership, implementation, runtime/allocator/enforcer and hard-resource gates, with M1 held. Measurement retains bounded representation/serialization, source/build/ABI/binding, resources, controls, qualification and observed-execution holds. Nominal calculation remains separate from calibration/production assurance.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% stop/reset guard and RET-only pause remain. No execution permission or release receipt follows.
