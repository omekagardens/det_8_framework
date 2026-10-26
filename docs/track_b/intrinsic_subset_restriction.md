# Intrinsic restriction for positive subset growth

QR-LD036, independently reviewed and accepted on 2026-10-26. This self-contained proof states its exact law family and horizon. It describes a proposed stochastic observation, not a physical apparatus or recovery of the realized past.

## 1. Exact law and horizon

Write \(L(P)\) for the number of linear extensions of P on its distinct actual vertices, ignoring marks as ordering constraints, and set \(L(\varnothing)=1\).

Fix an admitted law whose rows on the horizon considered have the supplied subset-weight form
\[
Z_n=\sum_{k=0}^{n}\binom nk t_k,\qquad
G(s,m)=\sum_{k=m}^{s}\binom{s-m}{k-m}t_k,\qquad
q(P,r,S)=G(|S|,|\operatorname{Max}(S)|)/Z_{|P|}.
\tag{1}
\]
The weights are fixed finite positive numbers, with \(t_0=1\); marks are independent fair immutable bits, and each branch sends \(X\mapsto q(P,r,S)X/2\) on a common arbitrary complex PSD payload.

These are the supplied scalar-passive subset-weight rows, not a characterization of all DET-admitted kernels. Closure of an actual selected subset A equals S iff \(\operatorname{Max}(S)\subseteq A\subseteq S\). Partitioning all actual subsets proves normalization and positivity of (1), including empty/full ideals. No new selection axiom is imposed.

For a horizon N, only \(t_0,\ldots,t_{N-1}\) and the corresponding normalized birth rows are needed. The proof applies at every finite N to the already accepted all-size fixed-p laws of QR-LD027 and fixed positive sequences of QR-LD032. For QR-LD034's finite prefix alone, it applies only through its supplied four births. A finite prefix does not certify an unspecified continuation, and the separately prescribed mark-dependent seed is not silently included.

## 2. Equal history weights, derived directly

For a vertex v of the terminal order P, let \(S_v=P_{<v}\), \(s_v=|S_v|\) and \(m_v=|\operatorname{Max}(S_v)|\). In any linear extension, when v is born its strict past is exactly \(S_v\). Earlier incomparable vertices change the parent cardinality but not this numerator.

A complete canonical ideal/bit history uses successive birth labels \(1,\ldots,N\). It is uniquely determined by its naturally labelled marked endpoint: its prefixes are the induced orders on the first n labels. Auxiliary subset choices have already been summed in (1); they are not extra recorded history.

Every such history encoding the same marked isomorphism type \([P,r]\) therefore has probability
\[
W_N(P,r)=
2^{-N}\,
\frac{\prod_{v\in P}G(s_v,m_v)}
     {\prod_{n=0}^{N-1}Z_n}.
\tag{2}
\]
The numerator depends only on terminal pasts, while each parent size occurs once in the denominator. This proves equality of complete history weights directly from (1), without a later commutation theorem. The composed unnormalized payload map is exactly \(X\mapsto W_N(P,r)X\).

## 3. Natural encodings and marked automorphisms

Let \(a(P,r)=|\operatorname{Aut}(P,r)|\), where automorphisms preserve both order and marks. Each linear extension of the distinct vertices gives one natural encoding on \([N]\). Two extensions give the same encoded marked endpoint exactly when a marked automorphism sends one ordered vertex list to the other.

This action is free: an automorphism fixing a full vertex list fixes every vertex. Hence every encoding has exactly \(a(P,r)\) extension representatives, and the number of distinct canonical histories is
\[
L(P)/a(P,r),\qquad
\mu_N([P,r])=\frac{L(P)}{a(P,r)}W_N(P,r).
\tag{3}
\]
One must not count all L extensions as distinct encoded histories and then ignore this divisor. Conversely, one must not divide the deletion probabilities by the automorphism count again.

By positivity and (2), conditional on \([P,r]\), the distinct encoded histories are equally likely. A uniform extension on actual vertices induces precisely that uniform law on encodings, since all fibers have the same size. Marks can split automorphism orbits; the marked group in (3) accounts for this without changing L.

## 4. The kernel and marginal identity

The extensions of P partition according to their last vertex. That vertex must be maximal, and extensions ending at v are in bijection with extensions of \(P\setminus v\). Thus
\[
L(P)=\sum_{v\in\operatorname{Max}(P)}L(P\setminus v).
\tag{4}
\]
The candidate weights are nonnegative and sum to one, including the one-vertex case.

For an output marked type \([Q,s]\), define
\[
K_N([P,r],[Q,s])
=\frac1{L(P)}
\sum_{v\in\operatorname{Max}(P)}
L(P\setminus v)\,
\mathbf1\{(P\setminus v,r|_{P\setminus v})\cong(Q,s)\}.
\tag{5}
\]
An order/mark isomorphism transports maxima, restricted markings and extension lists bijectively, so (5) is independent of representative. It sums actual vertices, even when several deletions give the same output or lie in one orbit.

For a uniform extension, (5) is exactly the distribution of its endpoint after removing its last vertex. That output type is constant on each marked-automorphism orbit of extensions. Section 3 therefore identifies (5) with the conditional distribution of the preceding marked endpoint under the admitted birth law.

Averaging this conditional distribution over the terminal endpoint gives
\[
\boxed{\mu_NK_N=\mu_{N-1}}.
\tag{6}
\]
The right side is the actual preceding marginal because summing every final ideal/bit branch gives one. This is a finite counting and conditioning proof for every available N, not extrapolation from a three-vertex test.

Replacing each scalar probability by its coefficient multiplying X proves the same equality of coarse-grained unnormalized payload maps for every common X. No trace normalization, diagonal restriction or payload-subsystem deletion is used. The random observation does not erase committed history.

## 5. Explicit three-vertex control

Put \(a=t_1>0,\ b=t_2>0,\ H=(1+a)(1+2a+b)\). The accepted three-vertex masses and the candidate's behavior are:

| Shape | Probability | \(L(P)\) | Chain probability after K | After uniform actual-vertex deletion |
| --- | ---: | ---: | ---: | ---: |
| Antichain | \(1/H\) | 6 | 0 | 0 |
| Edge \(u<v\), isolate w | \(3a/H\) | 3 | \(1/3\) | \(1/3\) |
| Fork: one minimum, two maxima | \(a^2/H\) | 2 | 1 | \(2/3\) |
| Join: two minima, one maximum | \(b/H\) | 2 | 0 | \(2/3\) |
| Chain | \(a(a+b)/H\) | 1 | 1 | 1 |

In the edge-plus-isolate case, deleting v has weight \(2/3\), and deleting w has weight \(1/3\). Uniform choice among its two maxima would be incorrect. In a fork each maximal leaf has weight \(1/2\). In a join only the top vertex is eligible, with weight one. The antichain gives each actual vertex weight \(1/3\). Marking two leaves differently changes marked output classes, not these actual-vertex weights.

Consequently the K chain mass is
\[
\frac{a+a^2+a(a+b)}H=\frac{a}{1+a},
\]
exactly the direct two-birth mass. Uniform deletion instead has chain mass
\[
\frac{3a+5a^2+2b+3ab}{3H},
\]
with discrepancy \((2b-a^2)/(3H)\). Thus the two kernels are different even where a particular coarse test happens to agree.

For the fixed-p family, \(a=p/(1-p), b=a^2\). K gives chain mass p, while uniform deletion gives \(p+p^2(1-p)/3\). At \(p=1/2\), these are \(1/2\) and \(13/24\).

The complete marked two-vertex law with chain mass z has \(C_{00},C_{01},C_{10},C_{11}\) each of mass \(z/4\), \(A_{00},A_{11}\) each of mass \((1-z)/4\), and mixed antichain mass \((1-z)/2\). Selection by K is mark-independent, so this retains fair marks and the mixed-antichain multiplicity two. These coefficients also specify every scalar output map.

## 6. Interpretation and stop

The kernel is parameter-independent within the stated family because the common W in (2) cancels upon conditioning. It uses intrinsic order counts and preserves the marks in its output. It does not identify which maximal vertex was actually born last. In the edge-plus-isolate example, multiple chronological histories remain possible.

The all-finite-N conclusion is conditional on the stated kernel form and supported law horizon. No conclusion is made for arbitrary mark-dependent, parent-dependent or informative-payload laws outside that form.

This is a proposed mathematical stochastic readout, with exact linear-extension counts as required quantities. No physical device, calibration, efficient counting procedure, implementation, speed or novelty is supplied. It neither imposes uniform deletion nor contradicts QR-LD033/034, which concern that different kernel. QR-LD035's channel ambiguity remains valid.


## Source and review identity

The mathematical body above is reproduced unchanged from the accepted QR-LD036 report, from Section 1 through its interpretation boundary. The title, status and this provenance wrapper are editorial. The private author report SHA256 is `d20986190f4ffa9ebdfe26025fd8639d627854641be8dc538dbe01cf4af5b25f`; the distinct review SHA256 is `35b92f91451894ea06b4e5c278a03dd0f4f10db8c13ebd3bd1d53fbcc60d0e3d`; coordinator disposition SHA256 is `2061579ee6ce7ed1ab213638b8bdc2040b87464c2e4f1edc1a737f23917d0f58`. Current identities do not reconstruct historical custody.

See the [positive-subset uniform-deletion obstruction](positive_subset_deletion_obstruction.md) for the different uniform-vertex rule, and [finite-prefix nonidentification](finite_prefix_nonidentification.md) for admitted family scope. No scientific execution, calibration, physical prediction or efficiency claim accompanies this proof.
