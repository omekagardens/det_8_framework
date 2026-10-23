# RI1426: Finite compatibility and a conditional global criterion

A complete strictly positive growth prefix can satisfy the admitted marked native conditions and anonymous sampling consistency through three completed births. The exact witness below is the accepted RI1423 result. A separate accepted theorem, RI1425, gives a sufficient route from finite compatibility to an all-size positive law: one fixed positive floor for each transition coordinate, an exhaustive closed finite-coordinate native specification, and feasibility at every horizon under those same floors and constraints.

The second result is a conditional existence implication. Its feasibility and native-closure hypotheses remain unproved; the three-birth witness does not establish them. Sampling consistency remains an optional mathematical constraint, not an adopted DET or physical law. Neither result supplies physical selection, empirical validation or an operational permission.

## 1. Growth, marks and the sampling question

A parent is a finite retained partial order P with immutable binary marks r. A birth chooses an ideal occurrence S of P and appends a new vertex whose old predecessors are exactly S. Distinct ideal occurrences are distinct alternatives, even if isomorphic. The full ideal S=P is included; the empty parent has one ideal, simultaneously empty and full.

Write q(P,r,S) for the ideal probability. In the finite witness the rows ignore r. Each newborn bit b is independently fair, so its marked branch weight is q(P,r,S)/2. Use the admitted scalar-passive, trace-preserving finite-stage transports, with canonical identification of targets along a native diamond. In transported coordinates a branch multiplies the entire positive-semidefinite (PSD) payload by q/2. Those transports and the native admission premise below are inputs, not derived physical dynamics.

Let mu_N be the distribution of the unmarked order type after N completed births. For 1<=k<=N, T_{N,k} chooses one uniform k-subset independently of growth and restricts the **completed order relation** to it, reporting only its unmarked type. It does not retain birth labels, marks or payload, and it does not delete generating edges and recompute reachability. The optional sampling identities are

\[
 \mu_NT_{N,k}=\mu_k.\tag{SC}
\]

The subset kernels compose: T_{N,m}T_{m,k}=T_{N,k}. For a particular k-subset, the two-stage probability is binom(N-k,m-k)/[binom(N,m)binom(m,k)]=1/binom(N,k); restriction of relations is associative. Thus requiring every adjacent-size deletion identity is equivalent to requiring all SC identities. Requiring only finitely many sizes is weaker. Temporal consistency retains the distinguished first births; equivariance changes names. Neither operation is anonymous uniform deletion.

## 2. The complete positive three-birth prefix

Births 1, 2 and 3 use parent sizes 0, 1 and 2. Let O be the empty parent, E={x} a singleton, C={x<y} a two-chain and A={x,y} a two-antichain. For every old marking, use these complete rows:

| Parent | Ideal occurrence | q |
|---|---|---:|
| O | empty=O, full | 1 |
| E | empty | 1/2 |
| E | {x}=E, full | 1/2 |
| C | empty | 1/3 |
| C | {x} | 1/3 |
| C | {x,y}=C, full | 1/3 |
| A | empty | 1/6 |
| A | {x} | 1/3 |
| A | {y} | 1/3 |
| A | {x,y}=A, full | 1/6 |

These exhaust every ideal occurrence on every parent at this scope. The two antichain singleton slots remain separate even when the old marks differ. Row sums are 1, 1/2+1/2, 3(1/3), and 1/6+1/3+1/3+1/6, respectively: all equal one and all entries are positive. Summing both newborn bits returns each q. Every legal marked history of at most three births therefore has positive probability.

For conditional native locality, use the inherited full marked maximal-deletion ratio-sufficiency premise, applied layerwise from an admitted positive prefix with the normalized empty row as base. For a proper ideal S, the deletion potential is

\[
 u_n(P,S)=
 \prod_{\varnothing\ne B\subseteq\operatorname{Max}(P)\setminus S}
 q(P\setminus B,S)^{(-1)^{|B|+1}}.
\]

Marks restrict with each deletion and are suppressed here because these rows ignore marks. Only smaller-parent rows enter. At the singleton, the sole proper potential is q(O,O)=1; scale 1/2 gives proper and full probabilities 1/2. At size two, deleting the chain's sole maximum gives potentials 1/2 for both proper slots. In the antichain, its empty-slot potential is (1/2)(1/2)/1=1/4, while either singleton-slot potential is 1/2. A common proper-slot scale 2/3 therefore gives proper loads 2/3 for C and 5/6 for A. Their positive full complements are 1/3 and 1/6, exactly the table.

The common scale is an allowed construction choice, not a necessary or unique coefficient. Relabeling transports ideal occurrences and deletion products, and the rows are mark-independent. Under the stated layerwise sufficiency and transport premises this supplies conditional native admission in the declared subclass. Normalization alone does not prove locality; no stronger unspecified locality axiom is certified. No later continuation or coefficient is used.

## 3. Every marked diamond at the finite scope

For two commuting incomparable births over base B with old precursor ideals S,T, the scalar diamond equation is

\[
 q(B,S)q(B+S,T)=q(B,T)q(B+T,S).
\]

Each second precursor is the indicated old subset and excludes the first newborn. A full first precursor is therefore proper in the intermediate parent. With terminal size at most three the base has size zero or one, giving the following exhaustive cases:

| Base | Ordered precursor pair (S,T) | Scalar product on either route |
|---|---|---:|
| empty | (empty,empty) | 1 times 1/2 = 1/2 |
| {x} | (empty,empty) | (1/2)(1/6) = 1/12 |
| {x} | (empty,{x}) | (1/2)(1/3) = 1/6 |
| {x} | ({x},empty) | (1/2)(1/3) = 1/6 |
| {x} | ({x},{x}) | (1/2)(1/3) = 1/6 |

In a mixed case the empty-first intermediate is an antichain and the second ideal is the particular old singleton, not a sum over both singleton slots. The full-first intermediate is a chain and the second ideal is empty. For full/full, the second ideal is the chain's bottom singleton; both newborns lie above x and are incomparable. For empty/empty, the second ideal is empty in the intermediate antichain. Equal precursors and full first factors have thus been included. Comparable successive births cannot be swapped legally and give no additional commuting diamond.

For any fixed pair of newborn bits, every scalar product acquires the same factor 1/4 on both routes, regardless of old marks. The whole-PSD composite factors are consequently 1/8 for the empty base, 1/48 for singleton empty/empty, and 1/24 for the other three singleton cases. Canonical transport compatibility makes these equalities hold on the entire transported payload, including off-diagonal entries, not only its trace. Summing branch traces preserves the input trace because the transports preserve trace and the complete marked row sums are one.

Parent-size-two full probabilities are needed for normalization but cannot be second factors in these diamonds. Their appearance in later diamonds is beyond this finite prefix. No infinite payload limit or informative quantum transformation is asserted.

## 4. Exact stopped laws and sampling through three births

The singleton has mass one, and mu_2(C_2)=mu_2(A_2)=1/2. Fair independent marks sum out of each ideal history. At size three, define A_3 as the antichain, E_3 as one comparable pair plus an isolated vertex, V_3 as one bottom below two incomparable tops, Lambda_3 as two incomparable bottoms below one top, and C_3 as the chain.

| Terminal type | Mutually exclusive contributions | mu_3 | Comparable pairs |
|---|---|---:|---:|
| A_3 | A_2, empty: (1/2)(1/6) | 1/12 | 0 |
| E_3 | C_2, empty: (1/2)(1/3); A_2, either singleton: 2(1/2)(1/3) | 1/2 | 1 |
| V_3 | C_2, bottom singleton: (1/2)(1/3) | 1/6 | 2 |
| Lambda_3 | A_2, full: (1/2)(1/6) | 1/12 | 2 |
| C_3 | C_2, full: (1/2)(1/3) | 1/6 | 3 |

These masses sum to one. They count actual ideal-history alternatives; no extra symmetry factorial or automorphism division is applied. A uniform pair is a chain with probability

\[
 (\mu_3T_{3,2})(C_2)
 =\frac{0(1/12)+1(1/2)+2(1/6)+2(1/12)+3(1/6)}3
 =\frac{3/2}{3}=\frac12=\mu_2(C_2).
\]

The only other pair type is the antichain, so it agrees too. All remaining identities with 1<=k<=N<=3 are identity kernels (k=N) or the unique singleton output (k=1). This proves every optional unmarked SC identity through three completed births. The native marked/PSD statement is separate; no additional marked sampling theorem is claimed.

## 5. Why the earlier exclusions still apply

RI1421 excludes two specified admitted families from all-size SC, not every native law. For the from-empty Bernoulli product-edge law at a fixed p in (0,1), the first and last of three birth labels can be comparable either directly or through the middle vertex. Its uniform pair-chain probability is p+(1-p)p^2/3, whereas its stopped-size-two chain mass is p. The positive discrepancy (1-p)p^2/3 persists in the completed relation when the middle vertex is omitted from the sample. The witness above has pair-chain mass 1/2 but differs from the Bernoulli p=1/2 prefix at size three.

For each fixed admitted strictly positive delayed-summable law, only finitely many proper births occur almost surely; later full births preserve the finite incomparable-pair count. Conditional on a completed order, a union bound makes the probability that a fixed-k uniform sample is not a chain at most min{1, binom(k,2)I(P_N)/binom(N,2)}. Bounded convergence gives a chain limit for every fixed k, without integrability of the eventual count. All-size SC would then force the stopped two-vertex distribution to be a point mass on the chain, contradicting its strictly positive antichain mass. This is a fixed-law conclusion; it supplies neither a uniform horizon across the family nor an all-native impossibility.

A finite compatible prefix therefore coexists with those exclusions. Native-only extension does not automatically preserve sampling equations. No replacement all-size law has been constructed.

## 6. Coordinates and closed constraints for a global criterion

On every finite carrier [n], include every partial order P, binary marking r, and ideal occurrence S, full ideals included. Let i=(n,P,r,S) and q_i=q(P,r,S). Each layer is finite, so the complete index set is countable. Include all presentations for equivariance; actual growth histories use natural birth presentations. Retain fair newborn bits, and impose mark independence by closed equalities if keeping the precise subclass of the finite witness.

A horizon H means H completed births. It uses full rows at parents 0,...,H-1 and diamonds with base size at most H-2. Fix a positive number ell_i<=1 for each coordinate and use the common product box

\[
 X_\ell=\prod_i[\ell_i,1].
\]

Each floor is fixed across all horizons containing its coordinate. The floors are not one common constant across sizes. Necessarily their sum in each row is at most one; an n-antichain has 2^n ideal occurrences, precluding one common positive floor at all sizes. No feasible floor system is supplied here.

Complete normalization, the empty-row value, equivariance and declared mark independence are finite linear equalities. Complete marked scalar diamonds are quadratic equalities, with every marking, equal precursor and full first factor included. With the fixed admitted canonical transports these coefficients give whole-PSD diamond equality after the common bit factor. Non-strict inequalities of continuous finite-coordinate functions are also closed. Strict positivity by itself is open; fixed floors replace it with closed positive bounds.

Finite deletion products and reciprocals are continuous on X_ell because each of their finitely many denominators has a fixed positive lower bound. Clearing denominators is justified on that domain, not automatically at zero. A sufficient ratio construction can define a restricted subclass without exhausting native laws.

**Closed native specification premise.** Supply an exhaustive cumulative, restriction-compatible finite-level formulation of every desired native condition, especially any remaining record-locality requirement. At horizon H, each condition must be closed and involve only rows through H-1; the formulation must include finitely many such conditions at each level and capture the claimed all-size admission in its union. An unspecified locality claim, extension slogan or existential representation does not establish this premise. Without it, the conclusion below concerns only the closed constraints actually specified.

The transports and Hilbert spaces are fixed finite-stage inputs, not variables whose compactness is proved. No infinite-dimensional payload space is introduced.

## 7. Sampling equations in the same transition array

A legal marked history h_N records successive ideal choices and bits, determining its retained orders and marks. Its mass is

\[
 w_q(h_N)=2^{-N}\prod_{n=0}^{N-1}q(P_n,r_n,S_n).
\]

For fixed N there are finitely many such histories. Summing these monomials over histories ending at an unmarked type t gives mu_N(t), a finite polynomial. No automorphism factor is inserted. The kernel entry T_{N,k}(t,u) is a fixed rational subset count divided by binom(N,k), independent of q. Each required identity

\[
 \sum_t\mu_N(t)T_{N,k}(t,u)-\mu_k(u)=0
\]

is consequently a closed finite-coordinate polynomial equation. At horizon H impose all output types and 1<=k<=N<=H. These use the same transition array as the native constraints and refer only to unmarked completed relations.

## 8. Conditional compactness theorem and proof

Let F_H be the subset of X_ell satisfying the complete row, mark/equivariance, native and diamond conditions through horizon H and all the sampling equations through H. If the finite witness is pinned, impose its exact coordinates as their rows enter and keep the same pin forever. Assume that these finite-prefix cylinders are closed, nested (F_{H+1} subset F_H), and nonempty for every H. Unused coordinates may be filled by their floors. All floors, earlier constraints and any chosen prefix pin stay unchanged across horizons.

**Theorem.** Under these assumptions, the intersection of all F_H is nonempty. Each member is a strictly positive normalized all-size array satisfying all specified sampling and closed native conditions. Full native admission follows only with the exhaustive native-specification premise.

Choose q^(H) in F_H and enumerate the countably many coordinates. Compactness of the first coordinate's closed interval gives a convergent subsequence. Extract from it a subsequence converging in the second coordinate and continue. A diagonal subsequence whose horizon indices tend to infinity converges coordinatewise to q* in X_ell. Fix a level m. The selected sequence is eventually in F_m by nesting, and every finite-coordinate constraint defining that level passes to the limit by continuity and closedness. Hence q* lies in F_m. Since m was arbitrary, it lies in the intersection. Each q*_i>=ell_i>0.

The separate finite witnesses need not agree in advance: their subsequential limit is the coherent witness. The proof gives no effective search, unique limit or constructive selection algorithm. Most importantly, nonemptiness for every H under the same floors is an assumption, not a consequence of the three-birth table.

## 9. History measure and the positivity boundary

Set the empty-history mass to one. Normalization gives

\[
 \sum_{S,b}w_{q^*}(h_n,S,b)
 =w_{q^*}(h_n)\sum_{S,b}q^*(P_n,r_n,S)/2
 =w_{q^*}(h_n).
\]

The resulting consistent finite distributions on the finitely branching history tree define a unique infinite-history probability measure on its cylinder sigma-algebra. Each legal finite cylinder has lower bound 2^-N times the product of its positive coordinate floors. Its stopped unmarked pushforwards are exactly the mu_N in the equations, so all SC identities hold under this one measure. Positive finite histories do not imply positive mass for every entire infinite path. Finite-stage payload compositions do not supply an infinite payload limit.

One alternative is to impose a fixed positive floor eta_h on every legal finite marked-history mass. These are closed polynomial inequalities on the coordinate cube. To deduce positive rows, they must cover every coordinate up to equivariance. A linear extension presents any finite marked parent as a legal natural history; its selected next ideal and bit cover the desired coordinate. For that child,

\[
 0<\eta_{h,S,b}\le w_q(h)q_i/2\le q_i/2,
 \qquad q_i\ge2\eta_{h,S,b}>0.
\]

Uncovered rows are not controlled. Rational native formulas still require their justified positive-domain closed formulation; they cannot be extended arbitrarily to zero.

Horizonwise positivity alone is weaker. The abstract sets (0,1/H] are individually nonempty and positive but have empty intersection; the closed relaxations [0,1/H] intersect only at zero. This is a minimal compactness boundary example, not a DET countermodel. A genuinely coherent family of positive prefixes already fixes every coordinate positively and gives floors a posteriori, for example half each coordinate. Unrelated positive witnesses at successive horizons provide neither coherence nor a fixed feasible floor system.

## 10. Remaining mathematics and retained gates

The three-birth witness establishes one finite compatibility checkpoint. Positive floors can be placed below those finitely many entries. It establishes neither all-size floors, every-horizon feasibility, nor exhaustive closed native locality. Even with that prefix pinned, all later feasibility obligations remain. There is no four-birth construction, global classification or proof that a sampling-consistent native law actually exists.

The next question is OPEN: can the narrower common-layer deletion-potential subclass be given an explicit exhaustive closed finite-constraint formulation on a justified positive domain? No answer to that question is incorporated here, and answering it alone would not establish every-horizon feasibility.

The separate E, NE, CE and measurement tracks retain their physical and execution gates; this consolidation does not adjudicate their current work or announce their older blockers as new findings. E still requires actual plant/rate calibration, timing and dwell, pre-entry and reset/storage conditions, complete costs and matched-resource validation. NE retains actual common-source and transfer premises with its source/control/readout/reset costs. CE retains an applicable enforceable resource contract, including the exact resident-memory ceiling and durable failure/cleanup evidence. Measurement retains applicable selected-image/cache and safe-composition authority, fixed statistic/arithmetic and data-quality gates, and justified rank/null interpretation. No acquisition, replay, selected-image execution or replacement calculation is authorized by these mathematical results.

Conditional admission remains separate from empirical qualification. The results establish no physical sampling postulate, informative quantum dynamics, geometry, gravity, mass, native forward prediction or application advantage. Protected validation, freeze/custody requirements, Option B/Status M, operational ABSTAIN, zero qualification and the RET-only pause remain.

The underlying results were accepted after distinct manual review at their stated evidence scope. Current identities do not reconstruct historical inspection. Missing earlier evidence, late historical freezes and manuscript readbacks, earlier custody/guard/helper errors, the expired unfrozen publication attempt, and repaired author/reviewer draft-size failures remain recorded. Mathematical acceptance does not waive or backdate them. The human exception for one reset-timestamp discrepancy is limited; the shared usage stop/reset guard remains.

This documentation preparation uses manual reasoning and fresh inert byte, JSON and archive checks, without scientific or frozen-program execution. Publication requires distinct review, exact root acceptance and current repository/remote verification. Every prior front suffix is preserved.
