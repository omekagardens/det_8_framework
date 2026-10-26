# Positive subset weights fail simultaneous uniform-deletion consistency

Accepted finite conditional result, 26 October 2026 (QR-LD034). Distinct independent review and coordinator disposition are complete. This result concerns the explicitly defined family below; uniform actual-vertex deletion is an optional observation convention, not an adopted physical axiom.

**Result.** No fixed positive \(t_1,t_2,t_3\), with \(t_0=1\), in the subset-weight family can satisfy uniform actual-vertex deletion both from three to two births and from four to three. Three-to-two consistency forces \(t_2=t_1^2/2\). A necessary antichain equation at four-to-three then forces \(t_3=t_1^3/3\), but the join equation has a strictly positive residual. This is a finite obstruction in this family, not an all-admitted-law theorem.

## 1. Family and observation convention

Write
\[
a=t_1>0,\quad b=t_2>0,\quad c=t_3>0,\qquad
u=1+a,\quad v=1+2a+b,\quad w=1+3a+3b+c,\quad H=uv.
\]
These are fixed weights; no horizon-dependent retuning is used. Each actual subset A of an n-vertex parent is chosen with probability \(t_{|A|}/Z_n\), where \(Z_1=u,Z_2=v,Z_3=w\). The newborn's strict past is the downward closure of A.

For an ideal S with s vertices and r maxima, the branch probability is
\[
q(P,S)=\frac{G(s,r)}{Z_n},\qquad
G(s,r)=\sum_{k=r}^{s}\binom{s-r}{k-r}t_k.
\tag{1}
\]
Closure equals S iff \(\operatorname{Max}(S)\subseteq A\subseteq S\). Thus positivity and the partition of actual subsets prove complete normalization, including empty/full slots. Mark independence and intrinsic counts give locality/equivariance. Both incomparable-birth routes have structural product \(G(S)G(T)/(Z_nZ_{n+1})\), including equal/empty/full precursors; independent fair bits give the same factor \(1/4\) on arbitrary transported PSD payloads. These checks apply to the finite rows and diamonds used here, following the supplied subset-weight proof.

Let \(\mu_N\) be the unlabelled marked endpoint law and D_N the kernel that chooses one actual vertex with probability \(1/N\), restricts the existing transitive order and marks, then forgets labels. The optional property is
\[
\mu_ND_N=\mu_{N-1}.
\tag{2}
\]
Restriction retains relations through omitted intermediate vertices. Neither orbit representatives nor deletion of generating edges replace actual-vertex restriction.

## 2. Necessary and sufficient three-to-two condition

Direct two births give chain probability \(a/u\). The complete unmarked three-vertex law is:

| Shape P | Numerator \(h_P\), probability \(h_P/H\) | Comparable pairs |
| --- | ---: | ---: |
| Antichain A | \(1\) | 0 |
| One relation plus isolate E | \(3a\) | 1 |
| Fork F: one minimum, two maxima | \(a^2\) | 2 |
| Join J: two minima, one maximum | \(b\) | 2 |
| Chain C | \(a(a+b)\) | 3 |

The three single-relation histories contribute a each. A fork comes from a chain parent and its root ideal; a join comes from an antichain parent and its full ideal. A chain uses the chain parent's full-ideal numerator a+b. The numerators sum to H.

Each deletion leaves one of three actual pairs, so
\[
\Pr_{\mu_3D_3}(C_2)
=\frac{3a+5a^2+2b+3ab}{3H}.
\]
Subtracting the direct probability yields
\[
\Pr_{\mu_3D_3}(C_2)-a/u
=\frac{2b-a^2}{3H}.
\tag{3}
\]
Therefore three-to-two consistency requires and, at this size, is equivalent to
\[
b=a^2/2.
\tag{4}
\]

This equivalence includes all marks and scalar payload coefficients. Given chain mass z, each of four lower/upper bit patterns has mass z/4; antichain 00 and 11 each have mass (1-z)/4, and mixed marks have mass (1-z)/2. Uniform deletion leaves independent fair bits because both structural growth and vertex choice are mark-independent. The seven marked endpoints are therefore fixed by the chain mass.

## 3. Four-to-three equations without a four-vertex classification

For B equal to the three-antichain or three-join, define
\[
T_B(P)=\sum_{A'\subseteq P}t_{|A'|}
\,n_B(P,A'),
\tag{5}
\]
where \(n_B(P,A')\) counts old pairs that, together with the new fourth vertex whose past is \(\downarrow A'\), induce B. This sum uses all eight actual subsets of P.

There are four induced triples after four births: the unchanged old triple and three containing the newborn. Uniform deletion selects each of them with probability \(1/4\). Consequently
\[
(\mu_4D_4)(B)
=\frac{h_Bw+\sum_P h_PT_B(P)}{4Hw}.
\tag{6}
\]
Equality to the direct mass \(h_B/H\) requires
\[
\sum_P h_PT_B(P)=3h_Bw.
\tag{7}
\]

The required weighted pair counts are:

| Parent P | \(h_P\) | \(T_A(P)\) | \(T_J(P)\) |
| --- | ---: | ---: | ---: |
| A | 1 | \(3(1+a)\) | \(3(b+c)\) |
| E | \(3a\) | \(2+a\) | \(3b+2c\) |
| F | \(a^2\) | \(1+a\) | \(b+c\) |
| J | b | 1 | \(a+3b+c\) |
| C | \(a(a+b)\) | 0 | 0 |

For the antichain column, an old incomparable pair must lie outside the newborn's past. Empty selection contributes the number of old incomparable pairs. Singleton selection adds three contributions a for parent A, one for E, one for F and none for J. Larger selections add none.

For the join column, an old incomparable pair must both lie in the newborn's past. Each pair in parent A contributes b+c. In E, the pair consisting of the lower vertex and isolate contributes 2b+c; the upper vertex and isolate contribute b+c. Fork leaves contribute b+c. For parent J, selecting its old maximum alone contributes a, every two-subset contributes b, and the full subset contributes c.

The last a term retains transitive relations: selecting the old join's maximum puts both roots below the newborn, even if that maximum is subsequently deleted. Counting only retained generating edges would lose it. Pair and subset multiplicities are literal counts, not uniform weights on automorphism orbits.

## 4. Two necessary equations contradict positivity

For the antichain, h_A=1. The table gives
\[
K_A:=\sum_P h_PT_A(P)
=3+9a+4a^2+a^3+b.
\]
Equation (7) is \(K_A=3w\), equivalently
\[
3c=4a^2+a^3-8b.
\tag{8}
\]
Combining with (4) forces
\[
c=a^3/3.
\tag{9}
\]

For the join, h_J=b. Its equation has residual
\[
\begin{aligned}
K_J-3bw
&=3(b+c)+3a(3b+2c)+a^2(b+c)\\
&\quad+b(a+3b+c)-3b(1+3a+3b+c)\\
&=(3+6a+a^2-2b)c+ab+a^2b-6b^2.
\end{aligned}
\tag{10}
\]
Substitution of (4) and (9) gives
\[
K_J-3bw=\frac{a^3(3+2a)}2>0.
\tag{11}
\]
Thus the actual join-probability discrepancy is
\[
(\mu_4D_4)(J)-\mu_3(J)
=\frac{a^3(3+2a)}{8Hw}>0.
\tag{12}
\]
All denominators are positive. No positive a can satisfy these three necessary equations.

Manual check: \(a=1,b=1/2,c=1/3\) gives \(H=7,w=35/6\). Three-to-two consistency and the four-to-three antichain equation pass. Direct join mass is \(1/14=14/196\); deleted join mass is \(17/196\). Their difference \(3/196\) agrees with (12). Passing the antichain equation is not sufficient for endpoint consistency.

## 5. Marks, control and exact limit of the result

At four-to-three, equality of complete marked laws would imply equality of the unmarked antichain and join events by summing marks. Their contradiction already disproves full marked feasibility; checking every remaining endpoint equation is unnecessary for this negative certificate. No sufficiency claim is based on two coarse events. Independent fair retained marks and scalar payloads cannot repair unequal unmarked event masses.

Chronological last-birth truncation remains a positive control for every positive choice of weights: old relations/marks persist and summing every last ideal/bit branch gives \(\sum_{S,\beta}q(P,S)/2=1\). Uniform two-to-one deletion also retains a fair bit.

QR-LD033 excluded the interior fixed-p subfamily, whose weights satisfy b=a^2. Here b=a^2/2 can repair the three-to-two test, but no positive c repairs both necessary four-to-three events. This extends the finite exclusion within the subset-weight family; it does not exclude all kernels admitted by DET's broader marked contract.

Zero weights lie outside this positive-weight question. The vanishing boundary a=0 would force b=c=0 under the displayed constraints, so it is not a positive solution. No higher-size continuation, physical law selector, prescribed-seed extension, geometry/gravity, quantum reconstruction, computational advantage or novelty follows. The optional observation property is not adopted.

## Provenance and boundaries

This presentation preserves the mathematical body of the accepted QR-LD034 author report (SHA256 `92ee5107da2c9eeea4d4757ac0e04b8c7d1a3325f565de9aa5396793a7de5a0e`), reviewed independently and dispositioned by the coordinator. The exact disposition SHA256 is `db22c4ec87776043f9026c9163ef79c0189b581d5d4cd85496ace1c939c3dd7f`. Its finite subset-weight law is stated here; the earlier [fixed-p counterexample](uniform_deletion_counterexample.md) and [finite-prefix distinction](finite_prefix_nonidentification.md) supply context.

No higher-size continuation, all-law classification, physical prediction, implementation speed or experimental validation is claimed. Historical custody failures, including LD023's 65-second noncompliance, remain unwaived; current source identity does not repair them. Independent review, protected validation, calibration, resource and execution requirements remain in force. RET development is resumed under its separate scoped contracts.
