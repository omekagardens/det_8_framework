# RI1438: Positive four-birth sampling and finite native freedom

This publication consolidates the direct finite admission of the eleven-scale mark-independent family and an exact strictly positive extension preserving the uniform completed-order pair and triple marginals. The fixed prefix has pair-chain probability one half. The witness belongs to an explicit nonunique interval; one common scale cannot satisfy the same triple constraints. These are finite results through four committed births, not a sampling-consistent law at every horizon.

## Declared native model and admission

A state consists of a finite completed partial order P, immutable binary marks r, and an arbitrary complex positive-semidefinite payload on a fixed carrier. A birth selects any ideal S, appends a maximal vertex with exactly that strict past, and appends an independently fair bit b. The whole unnormalized payload map is B_(S,b)(D) = (q(P,r,S)/2) D, with the canonical scalar-passive transport to the common terminal carrier. This model and its carrier, bits and transport are stipulated; they are not derived from bare open becoming.

The required finite conditions are strictly positive complete probability rows, precursor-only mark locality with access to the whole unmarked parent, transported equivariance, every marked incomparable-birth diamond, and one committed birth per bookkeeping step. The numerical seed and normalization recipes of a particular earlier construction are not extra model axioms. For the present family the exact seed is the empty row 1, singleton row (1/2,1/2), two-chain row (1/3,1/3,1/3), and two-antichain row (1/6,1/3,1/3,1/6), with its two singleton ideals counted separately.

All proper probabilities in the table below ignore marks. They therefore satisfy precursor-only mark locality, while their dependence on the whole unmarked parent is allowed. Equivariance follows from the parent/ideal cases and occurrence multiplicities. The 23 proper ideal occurrences form 17 orbits and eleven scale blocks under the finite diamond equations. Positive scales and positive full complements give all positive normalized rows in this fully mark-independent scalar-passive finite subfamily with this fixed seed.

For each size-two base B and each ordered pair of old ideals S,T, the new boundary requires

    q(B,S) q(B+S,T) = q(B,T) q(B+T,S).

The accepted classification covers all nine chain-base and sixteen antichain-base ordered pairs, including equal and full choices. Every proper size-three slot is covered by deleting a maximal vertex outside its ideal. Each new second precursor excludes the other newborn and is proper; new full complements enter the next boundary, while old full first factors are retained at this one. The six nontrivial scaled ties and all loops hold throughout the displayed family. Both marked paths multiply the same transported arbitrary PSD payload by the same scalar product divided by four. This proves whole-map equality, including off-diagonal and zero payloads, rather than merely equality after trace normalization. Comparable births do not admit the reversed incomparable-birth route.

Strict positive scalar multiplication preserves PSD payloads; summing both bits and all ideals preserves total trace. The classical kernel is defined even at zero payload. Old records and completed relations are retained. These checks establish direct admission through parent size three, hence four births. They discharge the needed finite admission premise without classifying unrestricted marked ratio components. In particular, the earlier open H condition in the historical RI1434 report is resolved at this finite mark-independent scope, not at the scope of all marked laws.

Changing a scale changes a positive transition and a supported history law. A simultaneous change of potential coordinates and inverse scales leaving all probabilities fixed is a coordinate change; the alternatives here are not such a change. Full classification of the unrestricted marked family remains open. Continuing later native layers requires the separate extension theorem and recomputed potentials, including the changed full complements. It does not by itself preserve sampling identities.

## Observation and finite question

Uniform anonymous sampling selects a subset of the completed vertices, restricts the completed relation and forgets labels and marks. Comparisons already completed through discarded vertices remain. Deleting generating edges and recomputing reachability defines a different observation. T_(n,k) denotes this uniform induced-subset kernel. The additional requirement mu_n T_(n,k) = mu_k is an optional mathematical consistency condition, not an adopted DET or physical axiom.

The following complete table and arithmetic establish exactly which finite sampling claim is made. Fair marks remain underneath the calculation; no marked sampling theorem is asserted.

## 1. Actual prefix weights and retained family

Use \(A\) for the three-antichain, \(E\) for \(x<y\) with isolated \(z\), \(V\) for \(x<y,x<z\), \(W\) for \(x<z,y<z\), and \(C\) for \(x<y<z\). These labels also name the five reported triple types.

RI1423 fixes the singleton row \(1/2,1/2\), the two-chain row \(1/3,1/3,1/3\), and the two-antichain row \(1/6,1/3,1/3,1/6\). Thus the actual parent weights, not uniform type weights, are:

| Three-parent | Prefix contributions | \(\mu_3\) |
|---|---|---:|
| \(A\) | two-antichain, empty: \((1/2)(1/6)\) | \(1/12\) |
| \(E\) | chain, empty plus either antichain singleton: \((1/2)(1/3)+2(1/2)(1/3)\) | \(1/2\) |
| \(V\) | chain, bottom singleton: \((1/2)(1/3)\) | \(1/6\) |
| \(W\) | antichain, full: \((1/2)(1/6)\) | \(1/12\) |
| \(C\) | chain, full: \((1/2)(1/3)\) | \(1/6\) |

Put \(r=(1,6,2,1,2)=12\mu_3\). Fair bits sum out because the scalar rows and reported order types ignore marks. Actual marked histories are retained underneath; no automorphism factor or uniform-parent replacement is introduced. The seed fixes \(p=\mu_2(C_2)=1/2\) and already has all sampling identities through size three.

Keep RI1433/35's eleven coordinates and complete loads
\[
\begin{aligned}
K_A&=a_1/27+2a_2/3+a_3/2,\\
K_E&=a_2/9+2a_4/9+a_5/3+a_6/3+a_7/6,\\
K_V&=2a_4/9+2a_8/9+2a_9/3,\\
K_W&=a_3/6+2a_7/3+a_{10}/6,\\
K_C&=(a_6+a_9+a_{11})/3.
\end{aligned}
\]
Write \(F_P=1-K_P\). The exact native positive domain is \(a_c>0\) and \(F_P>0\) for every parent. Full complements remain in all sampling equations.

## 2. Complete newborn-triple count certificate

Choose an actual ideal \(S\) for the fourth birth \(v\), then one of the three old unordered pairs uniformly. Let \(N(P,S)\) count the resulting types among those three choices, in order \((A,E,V,W,C)\). Each displayed vector sums to three. The conditional triple law is \(N/3\).

The manual counting rule is exhaustive. If the old pair is comparable, intersecting \(S\) with it in zero, bottom-only or both vertices gives respectively \(E,V,C\). If the old pair is incomparable, zero, one or two selected vertices gives \(A,E,W\). An ideal cannot contain only the upper vertex of a comparable pair. Restrict the completed relation; do not delete generating edges and recompute reachability.

| Parent | Ideal \(S\) | Occurrences \(m\) | Probability per occurrence \(q\) | \(N=(A,E,V,W,C)\) |
|---|---|---:|---|---|
| \(A\) | empty | 1 | \(a_1/27\) | \((3,0,0,0,0)\) |
| \(A\) | singleton | 3 | \(2a_2/9\) | \((1,2,0,0,0)\) |
| \(A\) | pair | 3 | \(a_3/6\) | \((0,2,0,1,0)\) |
| \(A\) | full | 1 | \(F_A\) | \((0,0,0,3,0)\) |
| \(E\) | empty | 1 | \(a_2/9\) | \((2,1,0,0,0)\) |
| \(E\) | \(x\) | 1 | \(2a_4/9\) | \((1,1,1,0,0)\) |
| \(E\) | \(z\) | 1 | \(a_5/3\) | \((0,3,0,0,0)\) |
| \(E\) | \(xy\) | 1 | \(a_6/3\) | \((0,2,0,0,1)\) |
| \(E\) | \(xz\) | 1 | \(a_7/6\) | \((0,1,1,1,0)\) |
| \(E\) | full | 1 | \(F_E\) | \((0,0,0,2,1)\) |
| \(V\) | empty | 1 | \(2a_4/9\) | \((1,2,0,0,0)\) |
| \(V\) | \(x\) | 1 | \(2a_8/9\) | \((1,0,2,0,0)\) |
| \(V\) | root-plus-leaf | 2 | \(a_9/3\) | \((0,1,1,0,1)\) |
| \(V\) | full | 1 | \(F_V\) | \((0,0,0,1,2)\) |
| \(W\) | empty | 1 | \(a_3/6\) | \((1,2,0,0,0)\) |
| \(W\) | bottom singleton | 2 | \(a_7/3\) | \((0,2,1,0,0)\) |
| \(W\) | bottom pair | 1 | \(a_{10}/6\) | \((0,0,2,1,0)\) |
| \(W\) | full | 1 | \(F_W\) | \((0,0,0,1,2)\) |
| \(C\) | empty | 1 | \(a_6/3\) | \((0,3,0,0,0)\) |
| \(C\) | \(x\) | 1 | \(a_9/3\) | \((0,1,2,0,0)\) |
| \(C\) | \(xy\) | 1 | \(a_{11}/3\) | \((0,0,2,0,1)\) |
| \(C\) | full | 1 | \(F_C\) | \((0,0,0,0,3)\) |

For instance \(E,xz\) gives \(V\) on old pair \(xy\), \(W\) on \(xz\), and \(E\) on \(yz\). For \(C,xy\), old pair \(xy\) gives \(C\), whereas \(xz\) and \(yz\) give \(V\). These checks retain transitive old comparisons and distinguish fork from join.

Each multiple-occurrence row represents that many equally weighted but distinct ideals. Both newborn bits give the same unmarked result and have weights \(q/2\), so their sum is exactly \(q\), not \(2q\).

## 3. Exact affine equations, including pairs

Define
\[
U_t=\sum_{P}r_P\sum_{\text{table rows at }P}m\,q\,N_t.
\]
Then the actual newborn-containing triple law is \(\nu_{3,3}(t)=U_t/36\). The necessary and sufficient triple target is
\[
\boxed{(U_A,U_E,U_V,U_W,U_C)=(3,18,6,3,6).}\tag{T}
\]
Directly collecting the count table gives
\[
\begin{aligned}
U_A={}&a_1/9+2a_2+a_3/6+16a_4/9+4a_8/9,\\
U_E={}&2a_2+4a_3/3+20a_4/9+6a_5+6a_6+7a_7/3+2a_9,\\
U_V={}&4a_4/3+5a_7/3+8a_8/9+8a_9/3+a_{10}/3+4a_{11}/3,\\
U_W={}&a_3/2+a_7+a_{10}/6+3F_A+12F_E+2F_V+F_W,\\
U_C={}&2a_6+4a_9/3+2a_{11}/3+6F_E+4F_V+2F_W+6F_C.
\end{aligned}\tag{1}
\]
Since \(F_P=1-K_P\), these are exact affine equations in the eleven scales. Keeping the complements visible makes their subtraction effects explicit. Complete normalization gives \(\sum_tU_t=36\), so the five displayed targets are not five independent equations.

For a newborn-containing pair the chain probability is \(|S|/3\). The pair target is therefore
\[
\sum_Pr_P\sum_Sq(P,S)|S|=18.
\]
Equivalently the weighted proper deficit is
\[
\boxed{
a_1/9+10a_2/3+a_3+4a_4+4a_5+4a_6+
7a_7/3+8a_8/9+8a_9/3+a_{10}/6+2a_{11}/3=18.}\tag{P}
\]
Full branches contribute three to \(|S|\), zero to its deficit; occurrences are counted as in the table. This is an unconditional actual-law balance, not a separate constraint on each parent.

Here (P) is redundant once all of (T) holds. If \(J(P)\) is the old comparable-pair count, counting across all three old pairs gives
\[
U_E+2U_V+2U_W+3U_C
=\sum_Pr_PJ(P)+2\sum_Pr_P\sum_Sq(P,S)|S|.
\]
The fixed prefix has \(\sum_Pr_PJ(P)=18\); (T) makes the left side 54, forcing the rightmost sum to be 18. This is also the consistency of successive uniform induced-subset sampling. It does not make a single pair equation sufficient for the triple targets.

RI1429's exact mixture identity now gives
\[
\mu_4T_{4,3}=\tfrac14\mu_3+\tfrac34\nu_{3,3},
\qquad
\mu_4T_{4,2}=\tfrac12\mu_3T_{3,2}+\tfrac12\nu_{3,2}.
\]
The inherited identities through size three and (T),(P) imply both desired size-four marginals. Singleton/full-size identities are automatic. Thus (1),(P), positivity and the five loads form the exact finite criterion; no later horizon enters.

## 4. Rational witness and exact verification

The exact eleven-coordinate witness is
\[
a^*=(2/3,\ 2/3,\ 2/3,\ 2/3,\ 38/27,\ 2/3,\ 2/9,\ 2/3,\ 2/3,\ 2/3,\ 29/18).
\]

Substitute the announced \(a^*\). The complete new rows are:

| Parent | Proper probabilities in section 2 occurrence order | Full probability |
|---|---|---:|
| \(A\) | empty \(2/81\); each singleton \(4/27\); each pair \(1/9\) | \(16/81\) |
| \(E\) | \(2/27,\ 4/27,\ 38/81,\ 2/9,\ 1/27\) | \(4/81\) |
| \(V\) | empty \(4/27\); root \(4/27\); each root-plus-leaf \(2/9\) | \(7/27\) |
| \(W\) | empty \(1/9\); each bottom singleton \(2/27\); bottom pair \(1/9\) | \(17/27\) |
| \(C\) | \(2/9,\ 2/9,\ 29/54\) | \(1/54\) |

Every occurrence and both marked branches are strictly positive. Counting multiplicities gives
\[
(K_A,K_E,K_V,K_W,K_C)
=(65/81,77/81,20/27,10/27,53/54)<1,
\]
so all rows normalize with the displayed positive complements.

The five substitutions into (1), on denominator 27, are
\[
\begin{aligned}
U_A&=(2+36+3+32+8)/27=3,\\
U_E&=(36+24+40+228+108+14+36)/27=18,\\
U_V&=(24+10+16+48+6+58)/27=6,\\
U_W&=(9+6+3+16+16+14+17)/27=3,\\
U_C&=(36+24+29+8+28+34+3)/27=6.
\end{aligned}
\]
These sums check every target, not only their normalization.

An independent pair check uses the row-conditional means
\[
\mathbb E(|S|\mid A,E,V,W,C)
=(46/27,104/81,49/27,61/27,73/54).
\]
Weighting by the actual \(\mu_3\) gives
\[
\mathbb E|S|
=(46+208+98+61+73)/324=3/2.
\]
Thus \(\nu_{3,2}(C_2)=1/2\), as required. No programmed arithmetic, solver, search or mathematical enumeration was used; these are manual rational substitutions.

RI1435's accepted finite admission applies because this is a point in its complete positive family. The fair bits, proper-mark locality, all inherited/new marked diamonds and whole-PSD scalar-passive maps remain intact. Only the additional sampling statements are unmarked; no separate marked sampling theorem is claimed.

## 5. Nonuniqueness, rejected common line, and stop

There is an explicit feasible interval. Starting at \(a^*\), replace
\[
a_5\mapsto a_5+t,\qquad a_6\mapsto a_6-t,
\qquad -1/18<t<2/3.
\]
All other scales stay fixed. \(U_A,U_V\) are unchanged; \(U_E\) uses only \(6(a_5+a_6)\); \(F_E\) is unchanged, so \(U_W\) is unchanged. In \(U_C\), the change \(-2t\) from \(2a_6\) cancels \(+2t\) from \(6F_C\). Equation (P) also uses \(4(a_5+a_6)\).

Only \(K_C\) changes, by \(-t/3\). Hence \(F_C=1/54+t/3>0\) at the lower endpoint restriction, while \(a_6=2/3-t>0\) gives the upper restriction. \(a_5=38/27+t\) remains positive throughout. Other loads and scales are unchanged. The endpoints themselves fail strict positivity. This proves nonuniqueness without an equation-count or uncomputed-rank argument; it does not classify the entire feasible set.

Conversely on the optional common line \(a_c=\alpha\), the \(A\)-target is \((9/2)\alpha=3\), forcing \(\alpha=2/3\). But the \(E\)-target there is \((197/9)\alpha=394/27\ne18\). Thus no common-line point satisfies all triple equations for this unchanged prefix. Failure of that optional restriction does not imply failure of the admitted eleven-scale family.

The completed result is finite positive pair/triple feasibility, with a witness, a nonunique interval and a rejected common-scale summary of the law choices. It does not select a physical parameter, identify unrestricted marked components, prove a fifth-birth extension or any all-horizon sampling law. No physical clock/readout, informative QM, metric, mass/gravity or empirical qualification follows.


## Evidence, limits and next question

The scientific basis is RI1435's accepted direct admission theorem and RI1437's exact sampling calculation, each with a distinct independent review and coordinator disposition. Exact source and review identities are retained with this publication preparation. The displayed rational substitutions and exhaustive newborn-triple cases are mathematical checks, not observed scientific data or a programmed simulation. Packaging checks concern current bytes and do not authenticate unavailable historical tool bodies.

Historical custody and timing limitations, missing RI1389 evidence, RI1401 late freeze, RI1419 late readback, and prior cap, display, schema and wrapper failures remain recorded. Current hashes and present mathematical acceptance do not repair them. Protected validation, freeze/custody prerequisites, Option B/Status M, ABSTAIN, zero qualification, the shared 10% usage guard and the RET-only pause remain in force.

The next native question is whether complete anonymous four-order observation distinguishes members of the displayed interval despite their equal pair and triple summaries. No answer to that question is adopted here. Neither an uncomputed matrix rank nor a classification of the entire feasible set is claimed. No fifth-birth extension, all-horizon sampling law, physical clock or detector map, informative quantum dynamics, metric, mass, gravity or empirical validation follows.

The original measurement work and the E, NE and CE tracks remain separate. Measurement's nominal H1 functional and conditional rank/perturbation mathematics supply no observed significance or native forward map; source/build, bounded record representation, qualification and execution remain unadmitted. E still requires actual operator/actuator behavior and source-to-reset closure/cost evidence. NE still requires actual source/reset/control/readout certification in both candidate worlds. CE retains implementation, runtime and hard-resource admission gates, with no DET-distinct mechanism or M1 execution admitted. No result in one track validates another's premises.

Free Thinker contributes clearly marked philosophical proposals through the coordinator only. No philosophical proposal, private journal entry or unreviewed successor is part of this scientific publication. Its personal journal remains autonomous and is not a research evidence source.

This is a documentation checkpoint. Four coordinator fronts retain their full prior suffixes, and the standalone public report and nonself manifest are new paths. Main integration is merge-only. Publication requires independent review, coordinator acceptance and exact live repository/index/ancestry and remote checks.

## Exact source identities

These are the literal report versions used, not claims of independent authentication of original provider sessions.

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| RI1435 author report | 12238 | `17943c883b07b8d5fc360474d94ff097a46cc853734ca259bd4a78f8065335e0` |
| RI1435 independent review | 12210 | `ba18728d903ef644305e3ee2191077fcb1c1b84c759015da39e3d4d6d0a5ba62` |
| RI1437 author report | 11214 | `9ecd6e78e17d39b20efe3dc4499e7894c1fbb80b9124ea724ba67fac2725d299` |
| RI1437 independent review | 12039 | `dca2febb545b815afd72025be24e4cafa9ce602bd7962ec47633886c8db16cfe` |

The admitted-model sources are THEOREM_PACKAGE.md (52,030 bytes; SHA256 `b2dd69a951102d84023c690d5aaafdcef802cd27251ee4f2c6f4a4aa04362218`) and LAW_DEPENDENCE.md (17,936 bytes; SHA256 `68c38eeb7232f7fd471c6a6bbf74316350408031cbdbd849495ff890a534444a`), the recovered 18 October editorial versions, not substituted current drafts. RI1423, RI1429, RI1431 and RI1433 supply the fixed seed, sampling induction and finite coordinate premises as stated above.
