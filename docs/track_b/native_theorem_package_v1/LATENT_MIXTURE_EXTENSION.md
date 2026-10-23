# Latent mixtures as optional admitted growth laws

Accepted conditional mathematical result: an explicit shared-latent extension, its exact feasible parameter region, and its admission as an optional all-size scalar-passive marked law under the declared model. The extension proof is the source author's work; the model-comparison proof is the independent reviewer's work, adopted by coordinator adjudication. This public document is a selective composite, not a literal copy of either whole source.

The [finite law-dependence witness](FINITE_LAW_DEPENDENCE.md) is the source's historical RI1383. The operative admission rules are [the declared model, §1](THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model), with [law dependence](LAW_DEPENDENCE.md) separating optional choices from gauges. The [full-order likelihood](BERNOULLI_ORDER_LIKELIHOOD.md), [within-family parameter-identifiability theorem](PARAMETER_IDENTIFIABILITY.md), [finite thinning likelihood](THINNED_ORDER_LIKELIHOOD.md) and [auxiliary-seed equality](AUXILIARY_SEED_IDENTIFIABILITY.md) retain their distinct scopes.

The first four sections reproduce the author's extension proof literally. Its candidate-stage qualifications describe what those sections establish on their own. The separately attributed comparison below supplies the declared-model admission proof; the author's superseded admission HOLD is not the current disposition. Review-stage references to separate coordinator acceptance are satisfied by the subsequent scoped adjudication recorded here. Historical line numbers in the comparison refer to the review's captured public version; the model link above locates the operative section directly.

All claims remain conditional on that mathematical model and the stated observation premises. No physical prediction, readout, experiment, calibration or execution is supplied.

## 1. Exact moment decision over the original finite-witness domain

Retain \(q=1-p\) and the accepted domain \(0<p<1,\ 0<\delta<pq^2\).
The question is whether a probability measure \(\mu\) on \([0,1]\) can satisfy
\[
 m_1=\mathbb E_\mu\theta=p,\qquad
 m_2=\mathbb E_\mu\theta^2=p^2+\delta,\qquad
 m_3=\mathbb E_\mu\theta^3=p^3+\delta.                                  \tag{1}
\]
There is such a measure if and only if
\[
                    \boxed{0<p<\tfrac12,\quad
                           0<\delta\le p(1-2p).}                     \tag{2}
\]
The upper endpoint is included. It lies strictly below the original
upper bound \(pq^2\), since \(pq^2-p(1-2p)=p^3>0\).
For all other parameters in the original domain, this particular
conditional-iid latent representation is impossible. That is not
impossibility of every other projective extension.

### Necessity, without an imported moment theorem

Because \(\theta\ge0\),
\[
0\le\mathbb E_\mu\!\left[\theta
  \left(\theta-\frac{m_2}{p}\right)^2\right]
=m_3-\frac{m_2^2}{p}.
\]
Multiplication by \(p>0\) and substitution of (1) give
\[
             p m_3-m_2^2
               =\delta\,[p(1-2p)-\delta]\ge0.                         \tag{3}
\]
Since \(\delta>0\), this forces (2). Thus even a nonnegative latent
variable could not satisfy these moments outside that region.

### Explicit sufficiency on the whole feasible region

Put
\[
 r=pq-\delta,\quad s=pq^2-\delta,\quad a=\frac{p^2q}{r},
\]
and define a three-point measure on \(\{0,a,1\}\) with weights
\[
\boxed{
 w_0=\frac{\delta(2pq-\delta)}{p^2q},\qquad
 w_a=\frac{r^3}{p^2q\,s},\qquad
 w_1=\frac{\delta[p(1-2p)-\delta]}{s}.
}                                                                     \tag{4}
\]
On (2), \(r>0,\ s>0\) and \(r-p^2q=s\), so \(0<a<1\).
All weights are nonnegative; \(w_a>0\), and \(w_0>0\).
The endpoint weight \(w_1\) is positive in the strict interior and zero
when \(\delta=p(1-2p)\).

To check both normalization and moments transparently, the formulas imply
\[
 w_a a(1-a)=r,\qquad
 w_0=q-w_a(1-a),\qquad w_1=p-w_a a.                                   \tag{5}
\]
For the last identity, its numerator after putting over denominator \(s\)
is \(\delta[p(1-2p)-\delta]\); the middle identity gives
\([p^2q^2-r^2]/(p^2q)=\delta(2pq-\delta)/(p^2q)\).
Adding (5) gives \(w_0+w_a+w_1=1\), and
\(w_a a+w_1=p\). Further,
\[
 \mathbb E[\theta-\theta^2]=w_a a(1-a)=r=pq-\delta,
\]
so \(\mathbb E\theta^2=p-r=p^2+\delta\). Finally
\[
 \mathbb E[\theta^2-\theta^3]=w_a a^2(1-a)=ar=p^2q,
\]
so \(\mathbb E\theta^3=p^2+\delta-p^2q=p^3+\delta\).
This proves (1) by manual algebra, without numerical evaluation.

At the feasible upper endpoint, \(a=q\), \(w_1=0\),
\(w_a=p/q\), and \(w_0=(1-2p)/q\). Thus the boundary is a valid
two-point law on \(\{0,q\}\), not a limit silently omitted from existence.
The reference \(\delta=0\), outside the positive-correlation domain,
would reduce to the point mass at \(p\).

## 2. The construction recovers every accepted three-edge atom

Draw \(\theta\) once for the entire array. Conditional on that draw,
take all forward-edge coordinates mutually independent Bernoulli(\(\theta\)).
For three edges, each specified configuration with \(k\) ones has mass
\(\mathbb E[\theta^k(1-\theta)^{3-k}]\). Using (1), these are
\[
\begin{array}{c|c}
k&\text{mass of each specified configuration}\\ \hline
0&1-3m_1+3m_2-m_3=q^3+2\delta\\
1&m_1-2m_2+m_3=pq^2-\delta\\
2&m_2-m_3=p^2q\\
3&m_3=p^3+\delta .
\end{array}                                                          \tag{6}
\]
Thus this is exactly the RI1383 eight-atom witness, not merely a
different distribution with the same first marginal. Its \(N=3,m=2\)
alias, changed intrinsic full law and nonzero edge covariance remain
the accepted finite results.

Different edge coordinates have covariance
\(\mathbb E\theta^2-(\mathbb E\theta)^2=\delta\).
The single global draw must not be replaced by independent new draws at
each edge or birth; that would define a different array.

## 3. Projective forward arrays and natural-label covariance

One explicit common construction uses one \(\theta\sim\mu\) and a countable
independent family of uniform variables \(U_{ij}\), independent of \(\theta\),
and sets \(E_{ij}=\mathbf1_{\{U_{ij}\le\theta\}}\).
For each finite \(N\) this gives the stated conditional product law.
Restricting to the first \(N\) vertices of any larger array returns
exactly the same finite array law. This is a projective array extension.

Forward paths among the first \(N\) vertices cannot visit a vertex with
larger birth label and return. Therefore transitive closure also commutes
with restriction to this birth prefix. This does not assert that a
uniformly thinned completed order is a fresh smaller draw.

For a naturally labeled finite completed order \(P\), let \(c(P)\) count
covers and \(i(P)\) incomparable unordered pairs. Conditional on any
\(0<\theta<1\), requiring cover edges present, incomparable edges absent,
and summing every comparable noncover edge freely gives its mass
\(\theta^{c(P)}(1-\theta)^{i(P)}\).
The same polynomial identity is valid at endpoints by continuity
(or directly by the deterministic empty/complete edge arrays).
Use \(0^0=1\) for these polynomial factors. Define
\[
                    F(P)=\int_0^1
                     t^{c(P)}(1-t)^{i(P)}\,\mu(dt).                   \tag{7}
\]
This is the probability of one naturally labeled completed order,
not its unlabeled-class probability. The latter is
\(e(P)F(P)/|\operatorname{Aut}(P)|\).

Since the invariants \(c,i\) are unchanged by isomorphism, all naturally
labeled copies of the same completed order have equal mass at every
finite size. This proves all-size natural-label covariance for this
particular mixture. It is stronger than the horizon-three check, but
it is not by itself complete native admission.

Because \(w_a>0\) at a point \(a\in(0,1)\), every finite \(F(P)>0\).
The atoms at \(\theta=0,1\) therefore do not remove full finite order
support. Those degenerate conditional components are not being called
separately admitted open-parameter Bernoulli laws.

## 4. Explicit every-parent candidate and identities it actually satisfies

The following is an algebraically specified order-growth candidate,
not certification against an unavailable current native contract.
For every finite parent \(P\) and every ideal \(S\subseteq P\),
let \(P^S\) append one maximal vertex with strict past \(S\). Set
\[
                         \Pi(P,S)=F(P^S)/F(P).                        \tag{8}
\]
Both numerator and denominator are positive. Appending a maximal vertex
preserves old covers; its new covers come from \(\operatorname{Max}(S)\).
New incomparable pairs are precisely the \(n-|S|\) vertices outside \(S\).
Thus, for \(n=|P|\),
\[
 c(P^S)=c(P)+|\operatorname{Max}(S)|,\qquad
 i(P^S)=i(P)+n-|S|.                                                   \tag{9}
\]
The posterior measure proportional to
\(t^{c(P)}(1-t)^{i(P)}\mu(dt)\) consequently gives
\[
 \Pi(P,S)=\int t^{|\operatorname{Max}(S)|}(1-t)^{n-|S|}
                       \,\mu(dt\mid P).                              \tag{10}
\]
Conditional on \(t\), the closure fibers
\(\operatorname{Max}(S)\subseteq U\subseteq S\) partition all subsets.
Summing their product-Bernoulli masses shows that the integrand's sum
over every ideal is one, also at \(t=0,1\).
Integrating proves \(\sum_S\Pi(P,S)=1\).
Empty and full ideals are included and positive after mixing.

The history ending at a naturally birth-labeled \(P\) determines its
birth prefixes by restriction. Its likelihood at \(t\) is exactly
the factor in (7); marks, if added as independent fair bits, do not
change that posterior. Thus (8) is the conditional next-ideal law of
the mixture, not a heuristic replacement of the latent parameter by
its posterior mean. It uses the whole unmarked parent.

Ratios telescope: for any two allowable birth routes from a parent
\(P\) to isomorphic terminal orders \(R\),
\[
                 \Pi(P,S)\Pi(P^S,T)=F(R)/F(P).
\]
In particular, swapping two incomparable births gives the same product.
This is a concrete order-level diamond identity, including cases where
a precursor is the whole original parent or the two precursors coincide.

One can specify a further scalar-passive marked candidate on an arbitrary
fixed complex matrix carrier:
\[
                \mathcal B_{S,b}^{P,r}(X)=\tfrac12\Pi(P,S)X,
                \qquad b\in\{0,1\}.                                  \tag{11}
\]
Each map is completely positive, since it is nonnegative scalar
multiplication, and the sum of all these maps is the identity map.
It preserves the full arbitrary PSD payload, including zero; no
trace-normalization is used to define the classical probabilities.
Two marked birth compositions multiply to
\(F(R)X/[4F(P)]\) in either order, so the corresponding full scalar-map
diamond equality is proved, not inferred solely from an unmarked mean.
The coefficients ignore all old marks and are equivariant under
relabeling of parent and ideal.

These are explicit candidate properties: projectivity, all-size
natural-label covariance, every-ideal positivity/normalization,
equivariance, old-mark independence and the stated scalar marked
diamond identities. They do not derive non-passive quantum dynamics.

The following independently authored comparison supplies the admission step for the extension just proved. Its quoted scientific text is retained literally, including its original review-stage attribution; current coordinator acceptance is stated above.

## Direct comparison with the current declared native model

The earlier author's missing-source-location statements are superseded by its own completion addendum. The public files were then captured by the author, but it expressly did not complete this comparison. I freshly read the decisive literal definitions, independently of that capture claim.

THEOREM_PACKAGE.md lines 48–72 declare the state, scalar branch map and complete admission list. LAW_DEPENDENCE.md lines 38–40 explicitly restates that same conditional model. The candidate meets it as follows:

| Declared requirement | Verification |
| --- | --- |
| Every ideal, including empty/full, eligible with positive normalized probability | The F-ratio row and closure-fiber partition prove this for every finite parent. |
| Proper slots may read whole unmarked P but only marks inside S; full slots may read all marks | Pi reads the whole unmarked order and no marks. Whole-parent posterior dependence is expressly permitted at theorem line 59; it is not a locality violation. |
| Transported marked equivariance | c,i and the ideal-extension construction are isomorphism invariant, while probabilities ignore all marks. |
| Independent fair immutable newborn bit | The stipulated factor 1/2 is independent of the ideal, latent draw and old marks; old marks remain fixed. |
| Complete unnormalized marked diamond on arbitrary fixed-carrier PSD payload | Both two-step scalar compositions equal F(R)X/[4F(P)] for the same transported terminal marked order. This is equality for every X, including zero, not a trace-normalized or diagonal-only check. |
| All inherited marks, both new bits, equal precursors, and full first precursors included | No factor depends on any bit. In a diamond the second precursor excludes the other newborn, even when its underlying ideal was full at the base. The two terminal orders are isomorphic, so telescoping covers these cases without an exception. |
| One committed maximal birth per step | The explicitly defined P+S transition does exactly this; it supplies no physical clock. |

More explicitly, for ideals S,T of base C, each route product is F(R)/F(C). Scalar maps are completely positive, because they multiply by positive reals, and their sum over ideals and both marks is the identity map. The carrier is fixed and passive; there is no implicit changing-dimensional map or non-passive quantum claim.

The fixed seed, parent-four witness, optimizer and baseline continuation appearing after the model definition are particular law choices, not extra axioms forced on every optional law. The public text labels them as such; LAW_DEPENDENCE distinguishes actual law changes from gauges. This candidate is an optional from-empty law and need not preserve that prescribed numerical prefix. Its altered three-vertex intrinsic probabilities already prove a change of law, not a paired coordinate gauge.

Thus there is **no missing or violated identity among the stated conditional admission requirements**. The author stopped conservatively before this source comparison; this review completes the comparison without modifying the frozen manuscript or pretending it had done so. No independent proof of the admitted ratio-component theorem, reproduction of prescribed coefficients, canonical optimization, all-law classification or larger ontology is supplied. Coordinator adjudication of this explicit conditional model check remains separate.

## Accepted scope and remaining boundaries

Within the exact feasible parameter region, the candidate gives a concrete optional all-size scalar-passive marked law meeting the declared axioms and recovering the finite correlated witness. The resulting N=3,m=2 alias can therefore be compared with the existing optional independent Bernoulli law at this conditional-model level, subject to root's acceptance. The alias is not claimed for every larger N or every observation channel.

Outside the feasible region, only this shared-latent conditional-iid representation is ruled out. There is no universal no-extension theorem. The endpoint components do not imply a uniform finite-history lower bound, ergodicity or an asymptotic geometry. Known true size, uniform independent subset selection and faithful completed comparisons remain the inherited observation premises. No physical implementation, quantum reconstruction, clock, gravity, RET, estimator performance, numerical execution or publication permission follows.

## Additional scientific limits from the extension source

The original finite witness is recovered only in the feasible region (2).
Outside it, (3) excludes this latent-iid representation only.
No exhaustive extension classification, coefficient ladder or new
finite law is opened. Within-family parameter identification and
the distinct auxiliary-seed equality result remain unchanged.
The \(N=3\) alias is not asserted for all larger two-survivor experiments.

Known true size, uniform independent survivor selection and faithful
completed restriction remain observation premises; physical preparation,
readout, unknown-size/biased/noisy channels, calibration, quantum
reconstruction, gravity, geometry, clocks, RET and application claims
remain outside this result.

## Publication scope and exact correspondence

The composite retains four exact source chunks: author sections 1–4, the independent review's direct declared-model comparison, its accepted-scope boundaries, and the two scientific-limit paragraphs from author section 6. All mathematical expressions in those chunks are unchanged. The publication manifest identifies each chunk and its public byte hash. Exact original-file pins, byte ranges, omitted administration and private correspondence are retained in the separately withheld SOURCE_SECTION_MAP.json record.

The author's original status/header, source-location/admission section 5, administrative provenance and bounded-completion addendum are not republished as current conclusions. Their failures, later clarification and incomplete author comparison remain in the private originals. The review's full source-exposure, concurrent-publication, receipt and custody limitations likewise remain private; public excerpting does not cure them. Present text/hash checks are administrative correspondence, not machine proof or reconstructed historical custody.

The admitted optional law recovers the finite witness only in the feasible region. Outside it, this particular latent representation is excluded, not every extension. The inherited three-vertex/two-survivor alias is not an all-size observation-alias claim. The assigned finite-horizon mixing-law identifiability question remains pending independent admission and excluded. Publication preparation and a later independent editorial/release gate remain separate from mathematical acceptance.

Previously stated 30/33/38 exclusions retain their original construction or family restrictions; this publication does not extend them to every latent-mixture or admitted law.
