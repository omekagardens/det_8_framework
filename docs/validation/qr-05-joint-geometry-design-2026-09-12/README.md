# QR-05: common-world geometric target and channel design

12 September 2026 (Pacific/Honolulu). **Design and analytical review only.**
No new numerical study, fixture enumeration, mathematical executor, simulator,
unit-test suite or apparatus experiment runs in this gate. The preceding
branch audit and finite calculus were committed and pushed first as
`47262b616296c632189d4e8b3e2582ed2016a6d8`.

This sheet is standalone. It specifies a conditional geometric/sampling model,
not DET ontology, a new physical law, a derivation of gravity or an available
instrument. Its contribution is a joint identification question with exact
positive and negative answers, following the [reconciliation](../qr-05-bridge-reconciliation-2026-09-12/README.md).

## 1. Question and common world class

Which declared information distinguishes marked causal structure, time
orientation, relative proper volume and absolute proper volume when sampling
shape and normalization are unknown at the same time?

Use the one common class

`W = { (κ,ε,a,b,L,r): κ∈{1,2}, ε∈{−1,+1}, a,b∈{0,1}, L>0, r>0 }`.

All channels and targets below are functions on THIS W. There is no separate
one-parameter-family test substituted for a joint statement. L and r are
continuous positive parameters in the analytical claim. A 64-world rational
subclass will be specified only as a prospective executable witness set.

The hidden coordinates have these roles:

| Coordinate | Role |
|---|---|
| κ | Cone parameter relative to the fixed marked chart |
| ε | Time orientation relative to the fixed event labels |
| a | Conformal-factor profile, hence relative volume shape |
| L | Metric multiplier carrying squared-length units |
| b | Sampling-intensity shape relative to proper volume |
| r | Sampling-intensity normalization in inverse proper-area units |

No realized coordinate of W, volume, density parameter or generator label is
placed in an observer packet unless an explicitly named reference channel
below supplies it.

## 2. Geometry and marks

Take Q=(0,1)×(0,1), with dimensionless coordinates (t,x), and the metric

`g_w = L(1+a x)(−dt² + κ² dx²)`.

The metric extends smoothly to a neighborhood of the closed rectangle;
1+a x is positive there after a sufficiently small extension. Its matrix
determinant is `−κ² L²(1+a x)²`, giving positive proper-area measure

`dμ_w = κ L(1+a x) dt dx`.

These are two-dimensional spacetime areas, not spatial three-volumes.
The total area and the left-strip relative area, with
H={(t,x)∈Q:x<1/2}, are

```text
V_w = μ_w(Q) = κ L(1+a/2),
R_a = μ_w(H)/μ_w(Q) = (1/2+a/8)/(1+a/2),

R_0=1/2,       R_1=5/12.
```

The positive conformal multiplier does not change the cones. With the selected
orientation, strict chronology in the convex rectangle satisfies

`z≺_w z' iff ε(t'−t) > κ |x'−x|`.

Sufficiency follows from the straight timelike segment, which remains in Q.
Necessity follows by integrating the future timelike slope inequality along
any such curve. Null equality is excluded.

Use three fixed, individually identified interior probe events:

```text
A=(1/8,1/8), B=(7/8,1/8), C=(7/8,5/8).
```

For two distinct probes define χ(P,Q)=+1 when P≺Q, −1 when Q≺P, and 0
when neither is strictly before the other. The ideal causal channel is

`O_w = (χ(A,B),χ(A,C)) = (ε, ε if κ=1 else 0)`.

Indeed the second pair has Δt=3/4 and |Δx|=1/2. It is timelike for κ=1 and
spacelike for κ=2, with no null boundary. O identifies κ and ε within this
specified family; it does not reconstruct an arbitrary cone field.

### Marking, conformal terminology and units

The chart, region, probes and strip are fixed *model/interface definitions*,
not a claim that their coordinates have been measured. Registering the same
marks and asking the same strip or causal question in an actual apparatus
requires its own evidence.

Changing a or L changes the conformal representative, not the conformal class
of a fixed κ metric. Changing κ changes cones relative to these fixed marks.
Do not call all three changes “conformal structure.” The target below is a
marked-model target, not an invariant classification of every unmarked
spacetime. In particular, a coordinate rescaling may relate metric formulas
while moving the region and marks; it is not the active alternative used here.

A passive coordinate change transports g, the domain, probes, strip and
sampling measure together. The directed probe relations, V and R_a are
unchanged. Fixed-label orientation reversal is a different active alternative;
this contract does not quotient it out.

A common external unit convention is fixed across worlds. L has area units,
√L has length units, and r has inverse-area units. Active changes of L at
fixed marks and units are not passive changes of unit notation. No physical
clock channel, k-clock dynamics or retired coupling is introduced.

## 3. Sampling measure is not geometric measure

Declare intensity per proper area

`λ_w(t,x)=r(1+b x)`.

The coordinate intensity measure is therefore

```text
dM_w = λ_w dμ_w = κ L r (1+a x)(1+b x) dt dx,
Z_ab = ∫_0^1 (1+a x)(1+b x) dx
     = 1+(a+b)/2+ab/3,
Λ_w = M_w(Q) = κ L r Z_ab.
```

Λ is an expected count under the law specified below, not a count observed
with certainty. Geometry and density enter M multiplicatively. The normalized
point law is

`dν_w = [(1+a x)(1+b x)/Z_ab] dt dx`.

It is independent of κ, ε, L and r. Its left-strip probability is

```text
p_ab = ν_w(H)
     = [1/2+(a+b)/8+ab/24]/Z_ab.

(a,b)=(0,0): Z=1,    p=1/2.
(a,b)=(0,1) or (1,0): Z=3/2, p=5/12.
(a,b)=(1,1): Z=7/3,  p=19/56.
```

Thus p identifies the unordered pair {a,b}, not which factor is geometry.
Within this binary family it also identifies the full normalized point law.
That last statement depends on this menu; one strip probability does not
identify an arbitrary spatial density.

### Two acquisition laws, kept separate

**Fixed quota:** for a prospectively fixed n≥1, draw n independent points
from ν and retain only membership bits Y_j=1{X_j∈H}. For an ordered word y,

`Pr_w(y)=p_ab^k(1−p_ab)^(n−k)`, where k is its number of ones.

The quota is not a sample of Λ and gives no count-rate information. Unknown
loss, drift, selection or dependence would require another law.

**Poisson regional count:** as a separate stipulated acquisition model,
draw N with Poisson mean Λ, then conditional on N draw N independent points
from ν. For the unordered counts N_0,N_1 outside/inside H the law is

`Pr_w(N_0=i,N_1=j)=exp(−Λ) [Λ(1−p)]^i [Λp]^j/(i!j!)`.

This follows by multiplying the Poisson count mass and conditional binomial
mass. It also defines the full finite-region Poisson point process through
N and the conditional locations. The region/exposure and perfect detection
are fixed premises; this is not a causal growth law or a consequence of
Lorentzian geometry alone.

The complete count law identifies Λ and p: Λ=E[N_0+N_1]>0 and
p=E[N_1]/Λ. One finite realization does not reveal these expectations exactly.
Intensity alone determines the full process law only because this particular
Poisson construction is stipulated. A general correlated point process is
not determined by its intensity.

## 4. Joint target and five declared information channels

Use the geometric target

`τ(w) = (O_w, R_a, V_w)`.

Within W it is equivalent to (κ,ε,a,L): O recovers κ,ε; R_a recovers a; and
L=V/[κ(1+a/2)]. The sampling parameters b,r are nuisance coordinates. Returning
an expected observation must not be confused with returning a known target.

| Channel | Mathematical output | Actual information requirement |
|---|---|---|
| O | Two signed causal comparisons above | Ideal identified probes and correct chronological-comparison interface |
| P | p_ab | Full normalized membership law; a finite sample supplies bits, not exact P |
| T | Λ_w | Total-count N marginal law; not the fixed quota, marked-location law or one count |
| D | b | Explicit ideal density-shape reference, not a fitted label from P |
| R | r | Explicit ideal density-normalization reference in common proper-area units |

D and R are perfect reference outputs for this design, not newly validated
apparatus. In particular R already imports dimensional information per proper
area. Deriving it from the unknown V being inferred would be circular; an
actual route must justify independent metrology/transfer or retain the
reference as an unsupplied premise. Here “independent” concerns the source
of justification, not an independence requirement for a union bound.

All channels are defined on the same W. P and T are population-law summaries,
whereas D,R are stipulated reference information and O is an ideal comparison.
Counting five such information types is not a claim that five physical
devices are needed. T can also carry shape information; P and T are not
assumed statistically independent.
In particular, the complete two-region count law in Section 3 supplies BOTH
P and T. It must not be called the T-only channel in the minimality theorem.
Combining information types into one acquisition does not change the theorem's
specified observation maps, but does change a count of physical instruments.

## 5. Exact joint identification and minimality

### Sufficiency

The full set {O,P,T,D,R} identifies the joint target, and even all six hidden
coordinates, everywhere on W:

1. Recover κ and ε from O.
2. Set b=D.
3. P has one of three distinct values above, determining a+b; subtract b
   to recover a.
4. Set r=R.
5. Recover `L=T/(κ r Z_ab)`, with strictly positive denominator.

These are exact algebraic inverses of declared channels, not an inference
from a numerical fit or a separately calibrated instrument.
The inverse is asserted for channel tuples in the model image. An inconsistent
combination (for example P=1/2 with D=1) is model-infeasible, not a license to
coerce the recovered a outside {0,1} or silently replace a channel value.

### Necessity among the five declared channels

For each deleted channel, the following pair agrees on **every other channel**
but differs in τ. Fix κ=1 and ε=+1 except in the orientation row; omitted
coordinates in the table agree between the worlds.

| Omitted channel | Different worlds, with tuple coordinates (a,b,L,r) | Why retained channels agree |
|---|---|---|
| O | Keep (0,0,1,1), flip ε | All four scalar channels ignore ε |
| P | (0,0,3/2,1) versus (1,0,1,1) | D=0, R=1, T=3/2 and O agree |
| T | (0,0,1,1) versus (0,0,3/2,1) | O,P,D,R do not depend on L |
| D | (1,0,1,1) versus (0,1,1,1) | Same unordered factors, P=5/12, T=3/2, R=1 and O |
| R | (0,0,1,1) versus (0,0,3/2,2/3) | Lr=1, with the same O,P,D,T |

In the missing-P row V happens to agree, but R_a differs. This is why the
target must include relative volume as well as absolute volume. In the
missing-D row both proper-volume quantities change. These are failures of
joint target identification, not arbitrary parameter-label distinctions.

Any proper subset omits at least one channel, so that row is an obstruction.
Consequently the full five-channel set is the unique globally identifying
subset among these five channels on W. This does not mean every observation
fiber of every smaller subset is ambiguous; some partial observations can
identify a particular world target. It also does not rule out a different
instrument encoding several of these information types at once.

## 6. A simultaneous four-world collision of the complete record law

Fix κ,ε. Independently choose

`(a,b)∈{(1,0),(0,1)}` and `(L,r)∈{(1,1),(3/2,2/3)}`.

All four worlds have

`dM_w=κ(1+x)dt dx, P=5/12, T=3κ/2`

and the same directed chronology and probe O. They therefore have identical
full Poisson point-process laws, and identical fixed-quota iid point laws.
Even supplying latent sample coordinates and all sampled causal relations
would not distinguish them under this model: the intensity and chronology
already coincide. The actual basic packet supplies less information.

Nevertheless their geometric (R_a,V) pairs are

```text
a=1,L=1:   (5/12, 3κ/2)
a=1,L=3/2: (5/12, 9κ/4)
a=0,L=1:   (1/2,  κ)
a=0,L=3/2: (1/2,  3κ/2).
```

This is one common-class ambiguity involving shape and scale together. It is
not a comparison of unrelated seeded panels. The remedies are conditional:
D distinguishes which shape factor belongs to sampling, and R breaks the
scale/intensity-normalization ambiguity.

More generally the transformation

`(L,r) ↦ (cL,r/c)`, c>0,

preserves the entire record intensity, normalized law and chronology, while
multiplying V by c. It also preserves D. No deterministic postprocessing of
these identical data laws can recover V over W without additional information.

## 7. Information-geometric form of the scale ambiguity

Condition on fixed κ,a,b for this calculation. Choose fixed reference units
L_0,r_0 and define dimensionless log parameters u=log(L/L_0), v=log(r/r_0).
Then Λ=κL_0r_0 Z_ab exp(u+v). In the total-count Poisson experiment,

`∂_u log Pr(N) = ∂_v log Pr(N) = N−Λ`.

Since Var(N)=Λ, the Fisher information matrix is

```text
I(u,v) = Λ [ 1  1 ]
           [ 1  1 ].
```

It has rank one and null direction (1,−1), exactly the infinitesimal version
of (L,r)↦(cL,r/c). Normalized locations have no u,v dependence, so they add no
information in that direction. Any fixed number m≥1 of independent identical
regional replicates multiplies I by m without removing the null direction.
Fixed-quota normalized observations alone have a zero (u,v) information block.
This is record-channel information before supplying the ideal r reference;
it does not contradict identification once the additional channel R is given.

This is information geometry of a stipulated statistical family, not a
spacetime metric or gravitational curvature. It gives a useful future
diagnostic: a scale/density ambiguity is structural nonidentification, not
merely a small sample or a numerical covariance-conditioning problem. The
calculation conditions on the shape coordinates; it does not resolve their
separate exchange ambiguity. No Fisher-information software or RET inference
was run here.

## 8. Quantum-record boundary

For any fixed finite-quota word y, append a fixed, world-independent quantum
state σ_y, which may depend on the retained word. The resulting finite CQ state is

`Ω_w=Σ_y Pr_w(y)|y⟩⟨y|⊗σ_y`.

It is positive and trace one. Equal word laws give equal Ω. Every common
quantum channel or measurement maps equal input states to equal output laws;
randomized classical postprocessing has the same limitation. Thus merely
rewriting this sampler in quantum-record notation cannot break the collisions.

This is not a theorem that all possible quantum probes are uninformative.
A world-dependent field state, propagation channel or quantum measurement
would be an additional physical observation map needing its own justified
model and observational checks. No such coupling is proposed or excluded here.

All p values lie strictly between zero and one and Λ is finite and positive.
Every fixed finite membership word, and every finite pair of Poisson counts,
has positive probability under every relevant scalar-law alternative.
Population identification therefore does not imply certain scalar-parameter
recovery from one finite packet. Separate confidence, loss and selection
contracts are required before a RET adapter or measured-data claim.

## 9. Prospective bounded verification gate

The next executable gate is deliberately separate. Before its first run:

- Freeze this design's mathematical content, an exact protocol, independent
  primary/reference implementations, tests and a source-bound evidence driver.
  Do not edit the prior reconciliation's frozen calculus or capture.
- Use the rational witness subclass with L∈{1,3/2}, r∈{1,2/3} and all four
  binary coordinates free: 64 worlds, not axis slices. No random seeds,
  empirical data, fitted thresholds or hidden-label observation inputs.
- Analyze all 32 subsets of the five channels. Derive all observation
  partitions, target-constant fibers, minimal/minimum identifying sets and
  all differing-target pair separators. The global answer predicted here is
  one identifying menu and 31 nonidentifying menus.
- The 16 target values each have four nuisance worlds. Hence there are
  C(64,2)−16 C(4,2)=1,920 differing-target unordered pairs. Preserve every
  separator witness; do not reduce agreement to verdict flags.
- Compute the complete rational O,P,T,D,R and geometric target from the
  defining integrals/formulas by independent routes. If the prior integer
  quotient utility is reused, use explicit injective finite-alphabet encodings
  based ONLY on each observable value; retain and compare the original
  rational values too. World IDs and target labels are not channel inputs.
- Include the five omission witnesses, the four-world full-law collision,
  strict probe/boundary checks, scale compensation, representative-versus-class
  terminology and malformed inputs. Do not enumerate Poisson count tails or
  simulate point processes merely to verify these algebraic identities.
- Preserve first capture and failures; run normal/optimized tests and complete
  replays with one alternate-runtime replay under bounded work limits.

The witness grid is chosen transparently to contain exact degeneracies. A
different finite grid can introduce accidental identification: for example,
L∈{1,4} makes T with O,D,R distinguish a and L without P, because for each b
the four products L Z_ab are distinct. That narrower-grid shortcut is not
valid on continuous W. Neither grid is observed evidence or a discovery of
a physical parameter spectrum.

The analytical gate ends at this contract and its reviewed proofs. The
64-world enumeration, measured references, general metric reconstruction,
operator repairs, uniform convergence, manifoldlike dynamics, RET integration,
materials/anomaly applications and deferred clock work are not completed here.
