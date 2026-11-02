# Fixed four-birth law versus a flat two-dimensional interval profile

The admitted native four-birth model cannot have the same complete interval-profile distribution as four independent uniform interior points in a flat 1+1-dimensional Alexandrov interval, for any admitted two-state source mixture. A single event proves this finite mismatch. It is not a physical gravity test, a general exclusion of native geometry, or a statement about a continuum limit.

## Models and observable

The native model is exactly the [active residual law](../track_b/native_active_residual_v1.md), with the fair marks and four-birth structural prefix in [Part A of the marked-law specification](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). Retain every actual ideal, immutable binary mark and naturally encoded history once. Its complete history and mixed-source laws are stated in the [complete-trial observation reference](native_complete_trial_readout.md). No coefficient, support or horizon changes here.

For a terminal strict order E on four vertices, define

```text
N_m(E) = #{(a,b): a precedes b and exactly m vertices lie strictly between a and b},
m = 0, 1, 2.
```

The profile is (N_0,N_1,N_2). It is zero exactly when E is an antichain: every comparable pair has zero, one or two strict interior vertices and contributes to one entry. This event does not depend on vertex labels.

The comparison model is supplied independently. Sample four iid uniform points (u_i,v_i) in the unit null-coordinate rectangle of a flat 1+1-dimensional Alexandrov interval, and order them by both coordinates increasing. The two boundary events defining the interval are not among the four sampled vertices. This is the conditional-four-point sampling ensemble, not uniform weighting of unlabelled order classes. The distinction between these ensembles is explicit in [Brightwell, Henson and Surya, version 3](https://arxiv.org/html/0706.0375v3). No large-cardinality equivalence is used at four points.

Interval abundances motivate comparisons with supplied spacetime ensembles; see [Glaser and Surya, version 2](https://arxiv.org/html/1309.3403v2). Their continuum/locality setting is not a four-vertex dimension or curvature certificate. Here the comparison model supplies the geometry; the native generation does not inherit it.

## Exact separating event

Write Z(E)=1 for an antichain and zero otherwise. The accepted native complete-history mass for pure source i is

```text
L_i(h) = w_h [1 + (-1)^i theta (Z(E_h)-a)],
a = 1/264, theta = 1/32.
```

Here w_h is the reference history probability, including the original fair marks. The reference antichain weight is 1*(2/3)*(1/4)*(1/44)=1/264; summing the four fair marks supplies total factor one. Thus

```text
P_0(Z=1) = 8711/2230272,
P_1(Z=1) = 8185/2230272.
```

For any actual source mixture rho(x)=(x,1-x), with 0<=x<=1, linearity gives

```text
P_native(zero profile) = (8185 + 526x)/2230272 <= 8711/2230272.
```

There is no prior distribution over x. No extra permutation factor or automorphism divisor is inserted into the complete native history sum.

On the comparison side, sort the four points by u. Coordinate ties have probability zero. The v ranks are uniformly distributed over the 24 permutations, independently of this u ranking. The order is an antichain exactly for the single decreasing v permutation. Consequently

```text
P_flat(zero profile) = 1/24 = 92928/2230272,
P_flat(zero profile) - P_native(zero profile) >= 84217/2230272 > 0.
```

The full profile distributions therefore differ for every admitted native mixture. The native history accounting and the comparison permutation counting serve different roles and are not interchangeable.

## Decision and limits

Close exact equality to this specified four-point benchmark. A complete profile enumeration cannot change this decision, so it is not needed. Do not retune the native law or comparison ensemble after this result to present the same test as passed.

This does not decide equality of selected profile means, an independently declared approximate comparison, another sampling law or dimension, or a continuum limit. A different correspondence requires its own motivation, explicit assumptions and independent review. Count-to-volume interpretation, mass-bearing dynamics, backreaction and physical readout remain unestablished by this comparison.

## Review and provenance

GDM028's author packet and distinct mathematical review completed on November 2, 2026. The review independently checked the history accounting, source-mixture orientation, rank argument and exact rational gap. Coordinator adoption was made afresh at 18:27 UTC after capacity eligibility returned. An earlier disposition written after the 3% stop was invalid and remains preserved as an incident record; this adoption does not retroactively certify it. No empirical acquisition, simulation or benchmark is used in this proof.

Exact reviewed source identities (SHA-256):

- Author REPORT.md: `92c3bf854e7a0b77f88a1ad74e4fb15d55e5b253379930aa7175c3322f1c9bf7`.
- Distinct REVIEW.md: `13a283df6442bdad139331175430352be0398174997d528a2f45c032ca0ca355`.
- Distinct FREEZE.json: `bccefdce09a93c5d80ad3d8e8e750a346e22e0ac65a09f78e1802192ddea777c`.

Hashes identify these versions; the stated argument and completed review support the result.
