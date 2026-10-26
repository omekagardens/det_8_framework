# Uniform deletion is not implied by birth consistency

Status: independently reviewed and accepted as conditional finite mathematics on 26 October 2026. No scientific execution was used.

**Result.** Every fixed interior-p member of the accepted family fails uniform-vertex-deletion consistency already from three vertices to two:
\[
\Pr(\text{chain after uniform deletion})
=p+\frac{p^2(1-p)}3>p
=\Pr(\text{chain after two births}).
\]
Chronological last-birth truncation remains consistent. No additional law-selection principle is adopted.

## 1. The proposed observation property

Let \(\mu_N\) be the law of the unlabelled marked endpoint after N births. For a marked order \((P,r)\) with N actual vertices, define
\[
D_N([P,r],[Q,s])
=\frac1N\#\{v\in P:
(P|_{P\setminus\{v\}},r|_{P\setminus\{v\}})
\cong(Q,s)\}.
\tag{1}
\]
Restriction retains every order relation between surviving vertices, including transitive relations formerly witnessed through v. Isomorphism preserves marks. The actual-vertex sum makes (1) independent of representative.

The proposed property is
\[
\mu_ND_N=\mu_{N-1}\qquad(N\ge2).
\tag{2}
\]
This is a mathematical observation kernel, not reversal of a committed birth or a new physical process. It is not an axiom of the supplied marked-diamond contract.

## 2. Exact finite representation and pair calculation

Fix \(p\in(0,1)\), and write \(q=1-p\). Accepted QR-LD027 supplies
\[
q_p(P,r,S)=p^{|\operatorname{Max}(S)|}q^{|P|-|S|},
\]
fair independent immutable bits and scalar payload maps.

For three births, take independent Bernoulli(p) edges \(E_{12},E_{13},E_{23}\), then their transitive closure. At each birth, closure of selected old vertices is S precisely when its maxima are selected and outside vertices are not; other selections within S are free. Its probability is exactly the accepted kernel. Fresh incoming choices and the new fair bit are independent of the old history. Thus this finite representation realizes complete marked histories, rather than assuming an unrelated edge model.

In the resulting order,
\[
\Pr(1\prec2)=\Pr(2\prec3)=p,
\]
\[
\Pr(1\prec3)
=\Pr(E_{13}=1\ \text{or}\ E_{12}=E_{23}=1)
=p+qp^2.
\tag{3}
\]
Uniformly deleting vertex 1, 2 or 3 leaves each actual pair with probability \(1/3\). Averaging (3) therefore gives
\[
c:=\Pr_{\mu_3D_3}(\text{chain})
=\frac{p+(p+qp^2)+p}{3}
=p+\frac{p^2q}{3}.
\tag{4}
\]
The antichain probability is \(1-c=q(1-p^2/3)\). Direct two-birth probabilities are p and q.

On the event \(E_{12}=E_{23}=1,E_{13}=0\), of probability \(p^2q\), deleting vertex 2 still leaves \(1\prec3\). Deleting edges first and recomputing reachability would instead erase this relation. That different operation would miss precisely the extra \(p^2q/3\) in (4).

## 3. Actual multiplicities and complete endpoint laws

A second manual derivation uses every three-vertex unmarked shape:

| Shape | Endpoint probability | Actual deletions leaving a chain |
| --- | ---: | ---: |
| Three-antichain | \(q^3\) | \(0/3\) |
| One relation and an isolated vertex | \(3pq^2\) | \(1/3\) |
| Fork: one minimum, two maxima | \(p^2q\) | \(2/3\) |
| Join: two minima, one maximum | \(p^2q\) | \(2/3\) |
| Three-chain | \(p^2\) | \(3/3\) |

The single-relation row counts three possible sole edges. The chain requires \(E_{12}=E_{23}=1\), with \(E_{13}\) free. The other rows specify the remaining edge configurations. Their probabilities sum to
\(q^3+3pq^2+2p^2q+p^2=(p+q)^3=1\).
Weighting the last column gives
\[
pq^2+\frac43p^2q+p^2=p+\frac13p^2q,
\]
agreeing with (4).

Given each unmarked shape, all eight assignments of its three bits are equally likely. A marked isomorphism class containing b such assignments has probability b times the shape probability divided by eight. Explicitly, b is one for the chain and single-relation shape; \(\binom3j\) for the antichain with j ones; and \(\binom2j\) for a fork/join with fixed central bit and j ones on the interchangeable pair. This specifies the complete marked three-vertex law.

Deleting a vertex uniformly uses actual vertices, not uniformly chosen automorphism orbits. In an unmarked fork, deleting the root has weight \(1/3\); deleting one of the two leaves has combined weight \(2/3\). Uniformly weighting its two vertex orbits would incorrectly give \(1/2\) each. If marks split an orbit, each actual vertex still has weight \(1/3\).

Selection is independent of the fair bits, so the two retained bits remain independent and fair. The complete unlabelled marked two-vertex law is:

| Marked endpoint | Probability with chain mass z |
| --- | ---: |
| Chain, lower/upper marks 00 | \(z/4\) |
| Chain, lower/upper marks 01 | \(z/4\) |
| Chain, lower/upper marks 10 | \(z/4\) |
| Chain, lower/upper marks 11 | \(z/4\) |
| Antichain, marks 00 | \((1-z)/4\) |
| Antichain, marks 11 | \((1-z)/4\) |
| Antichain, one mark of each kind | \((1-z)/2\) |

Use \(z=c\) after deletion and \(z=p\) for direct two births. The mixed antichain combines two actual bit assignments; the two mixed chains remain distinct because order distinguishes lower from upper. Each table sums to one. Coarse-graining the scalar-passive branches gives the displayed coefficient times any common initial payload X; no normalized-state shortcut or payload-subsystem deletion is involved.

At \(p=1/2\), deletion gives chain/antichain probabilities \(13/24,11/24\), versus \(1/2,1/2\) directly.

## 4. Chronological control and finite exceptions

Deleting the actual last-born vertex from the complete birth history preserves the previous order and its marks. A later maximal vertex cannot introduce a path between older vertices. Summing its complete branches gives
\[
\sum_{S,b}q(P,r,S)/2=1.
\]
Hence chronological truncation returns the full preceding marked-history law, and therefore its endpoint law, at every N. For three to two births, removing label 3 leaves pair 12 with chain probability p and exactly the table above with \(z=p\). This control retains birth identity; it is not uniform deletion or uniform choice among maxima.

Uniform deletion from two vertices to one does pass for this family: the survivor has a single fair bit, matching the first birth. One to zero is trivial. Nevertheless (4) fails at three to two for every interior p.

Within \(0\le p\le1\), the defect \(p^2(1-p)/3\) vanishes only at p=0 or p=1. Their degenerate edge constructions give all-antichain or all-chain endpoints with fair bits and satisfy uniform deletion at every N. They are outside the admitted strict-support family: the singleton full or empty slot, respectively, has probability zero.

## 5. Exact conclusion and connection to QR-LD032

Admission and complete marked diamonds do not imply (2): the accepted interior-p family supplies counterexamples. The proposed property excludes every interior member at this finite test. This does not classify other admitted laws or establish whether any full-support law satisfies (2) at all sizes. No kernel is changed to enforce it.

Accepted QR-LD032 gives alternatives matching \(L_p\) through any specified finite horizon. For cutoff \(m\ge2\), both two- and three-birth marked laws coincide, so applying the same deletion kernel gives the same defect (4), despite their different asymptotic density results. Prefix agreement alone says nothing about this three-birth test when \(m=1\).

Thus finite record agreement and consistency under an additional observation operation are different requirements. Neither result makes finite observations universally uninformative. Uniform deletion would be an additional proposed restriction, not a consequence derived here or a newly authorized physical law.

All results concern the unrestricted comparison family, not the separately prescribed seed. No physical time, readout, dimension, gravity, quantum reconstruction, computational advantage or novelty is inferred. The optional observation property is not adopted as a law-selection principle. Historical custody limitations and failures remain explicit; this mathematical acceptance clears no experimental or operational gate.

## Dependencies and review scope

The admitted model and fixed-p family are stated in [the native-law compendium, Part T](native_symmetric_law_nonuniqueness_v1.md#t-constant-parameter-transitive-percolation-in-the-marked-contract). The separate [finite-prefix nonidentification theorem](finite_prefix_nonidentification.md) supplies the precisely scoped transfer in Section 5. These results concern formal marked growth laws; an observation kernel on their mathematical endpoints is not a supplied physical detector.

The author and independent reviewer separately checked the finite representation, both probability calculations, actual-vertex and mark multiplicities, chronological control and boundary cases. The coordinator read the complete proof and review, checked that algebra, and reverified the exact source identities. A separate evidence audit checked current inputs, retained captures and actual acceptance joins. Some original post-freeze completion records are externally attributed rather than retained in the literal packets; present hashes do not reconstruct continuous custody. Coordinator disposition: QR-LD033, SHA256 `161de464db26e7b75766a3a27a0d6c1ba98154ced420362b005b4ebe4dba4631`.
