# An intrinsic target screen from linear native height

21 October 2026. Manual conditional native-order theorem.
No data evaluation, coefficient reduction or experiment.
Independent review is recorded separately from this source manuscript.

## 1. Result and exact claim

**Yes.** The accepted all-layer half-scale height theorem obstructs
approximation by any fixed target class with a sublinear height bound,
even when arbitrary vertices may be deleted from the observed order.

Let \(\mathcal T\) be a declared isomorphism-invariant class of finite
orders, containing the empty order, such that
\[
              h(Q)\le g(|Q|)\quad(Q\in\mathcal T),\qquad
              g(k)=o(k).
\]
Height \(h\) counts vertices in a longest chain. Define
\(D_{\mathcal T}(P)\) to be the fewest vertices whose deletion leaves
an **induced** suborder in \(\mathcal T\).
Under the accepted half-scale baseline history law,
\[
 \boxed{\qquad
 \liminf_{N\to\infty}\frac{D_{\mathcal T}(P_N)}N\ge\frac12
 \quad\text{almost surely}.
 \qquad}                                                       \tag{1}
\]
No exact limiting distance or equality with \(1/2\) is asserted.

A concrete target covered by (1) consists of Ferrers cell orders with
fixed positive bounding-rectangle occupancy and fixed bounded aspect
ratio, together with the empty order. Its explicit height bound is
\(O(\sqrt{k})\). Bounded aspect **alone** fails: balanced thin hooks
have linear height. The unrestricted Ferrers class also contains
arbitrarily long one-row chains, so the screen does not apply to
that larger class.

These are compatibility statements for a selected native stochastic
order model and optional declared target classes. Deletion is a
combinatorial diagnostic, not physical record erasure or a detector
noise model. No physical dimension, metric, clock, embedding,
geometry bridge, QM/gravity or empirical conclusion follows.

## 2. Accepted native input and scope of its use

The height input is the accepted
[HALF_SCALE_HEIGHT_GROWTH](HALF_SCALE_HEIGHT_GROWTH.md) theorem.
Its source manuscript is distinct from the separately recorded review
status; historical manuscript-header metadata does not determine that
status.

The accepted input concerns the baseline which retains the admitted
finite prefix and uses the specified whole-marked-layer half-scale
prescription at every parent size \(n\ge6\). Its complete full-birth
probability exceeds \(1/2\) for every marked history. Full births
extend a chain. The accepted proof uses conditional-history
concentration, not iid growing-history assumptions.

Write \(P_N\) for the order at cardinality \(N\), \(H_N=h(P_N)\),
and \(\mathcal F_n\) for the complete marked-history filtration.
For every fixed \(n_0\ge6\), \(m=N-n_0\ge1\), and \(x\ge0\),
the accepted result is
\[
 P\!\left(H_N\le H_{n_0}+\frac m2-x
                   \mid\mathcal F_{n_0}\right)
       \le e^{-2x^2/m},                                    \tag{2}
\]
and
\[
                 \liminf_{N\to\infty}H_N/N\ge1/2
                 \quad\text{almost surely}.                \tag{3}
\]
Conditional statements are almost-sure statements, or statements
on positive-probability finite initial histories.
The random initial prefix and all its marks are retained.

This packet uses (2)–(3), not a new calculation of native probabilities.
Their admitted valid-prefix, ratio-potential, complete all-layer
baseline and infinite classical history-measure premises remain.
No \(\Xi\) decision or actual coefficient branch is needed.
The theorem does not transfer to the separately prescribed
expected-defect optimizer or to a finite harmonic deformation
without its own all-size argument.

## 3. Declared target and deletion distance

Fix \(\mathcal T\) independently of \(N\), the realized order and the
data. Membership is invariant under order isomorphism; labels and
marks play no role. Assume explicitly that \(\varnothing\in\mathcal T\).
Let
\[
 g:\mathbb N_0\longrightarrow[0,\infty),\qquad
 g(0)=0,
\]
be finite-valued and satisfy
\[
                         h(Q)\le g(|Q|)
                         \quad(Q\in\mathcal T).             \tag{4}
\]
No monotonicity of \(g\) or closure of \(\mathcal T\) under further
vertex deletion is assumed.

For a finite order \(P\) on vertex set \(V\), let \(P[V\setminus A]\)
retain exactly the induced order relation on the undeleted vertices.
Define
\[
 D_{\mathcal T}(P)
  =\min\{|A|:A\subseteq V,\ P[V\setminus A]\in\mathcal T\}.    \tag{5}
\]
Deleting all vertices is feasible, so the minimum is attained among
finitely many subsets and
\[
            0\le D_{\mathcal T}(P)\le |P|,\qquad
            D_{\mathcal T}(\varnothing)=0 .
\]
No relation editing, contraction or replacement order is permitted.
Isomorphism invariance of \(\mathcal T\) makes (5) intrinsic as well.

The empty-order convention is part of the declared target, not a
silent assumption that some positive retained size is achievable.
If a different target excludes empty and has no induced representative
in a particular \(P\), its corresponding distance must instead be
declared \(+\infty\). The finite-valued theorem here uses (5) with
empty included; it does not assert attainment for such other targets.

This distance permits deletion sets chosen after inspecting \(P\).
The target class and its bound remain fixed. No efficient membership
or distance algorithm follows from isomorphism invariance alone.

## 4. Deterministic deletion inequalities and the correct envelopes

Choose a longest chain of \(P\), of size \(h(P)\).
Deleting \(a=|A|\) vertices removes at most \(a\) members of that
chain, and the remaining members stay comparable in the induced
suborder. Hence
\[
 h(P[V\setminus A])\ge\max\{0,h(P)-a\},\qquad
 h(P)\le a+h(P[V\setminus A]).                              \tag{6}
\]
This is a statement about **every** subset \(A\), not an average
over deletion patterns.

Put \(N=|P|\), and apply (6) to a minimizing deletion of size
\(D=D_{\mathcal T}(P)\). Equation (4) gives the implicit necessary
condition
\[
                        h(P)\le D+g(N-D).                   \tag{7}
\]
For a direct bound valid even when \(g\) is nonmonotone, define
\[
                      G(N)=\max_{0\le k\le N}g(k).           \tag{8}
\]
Then
\[
 \boxed{\qquad
 D_{\mathcal T}(P)\ge h(P)-g(N-D_{\mathcal T}(P))
                    \ge h(P)-G(N),
 \qquad}                                                    \tag{9}
\]
with the final lower bound clipped at zero when desired.
Only if \(g\) is nondecreasing may one replace \(G(N)\) by \(g(N)\).

There is a sharper bound for a specified deletion budget.
For an integer \(0\le d\le N\), define
\[
                B_N(d)=\max_{0\le a\le d}\{a+g(N-a)\}.       \tag{10}
\]
All maxima in (8)–(10) are over integers. If \(D_{\mathcal T}(P)\le d\),
use its actual minimizing size \(a=D_{\mathcal T}(P)\) in (7).
This proves the exact event inclusion
\[
 \boxed{\quad
 \{D_{\mathcal T}(P)\le d\}
       \subseteq\{h(P)\le B_N(d)\}.
 \quad}                                                     \tag{11}
\]
Some retained sizes in these envelopes may be unattainable targets;
including them is conservative, not an existence claim.

One cannot simply replace \(B_N(d)\) by \(d+g(N-d)\):
the successful deletion may use fewer than \(d\) vertices, and
further deletion need not preserve target membership.
Monotonicity of \(g\) alone is not a substitute for the needed
comparison of \(a+g(N-a)\) over the entire budget range.

A small counterexample makes both warnings explicit.
Let \(\mathcal T=\{\varnothing,C_2\}\), with \(g(2)=2\) and
\(g(k)=0\) at every other size. For \(P=C_3\),
\(D_{\mathcal T}(P)=1\), \(h(P)=3\), and \(G(3)=2\).
Using \(g(3)=0\) instead of \(G(3)\) would incorrectly give \(D\ge3\).
Also \(D\le2\) does not imply a retained one-vertex target:
\(2+g(1)=2<3\), whereas \(B_3(2)=3\) is correct.
This is a finite-order counterexample to incorrect envelope
simplifications, not a proposed native growth law.

## 5. Finite-time native target-distance prediction

Let \(D_N=D_{\mathcal T}(P_N)\).
For fixed \(n_0\ge6\), \(m=N-n_0\ge1\), and integer
\(0\le d\le N\), put
\[
 t_N(d)=H_{n_0}+\frac m2-B_N(d),\qquad
 t_N(d)_+=\max\{t_N(d),0\}.
\]
Combining the exact inclusion (11) with the accepted height tail (2)
gives
\[
 \boxed{\quad
 P(D_N\le d\mid\mathcal F_{n_0})
       \le\exp\!\left[-\frac{2\,t_N(d)_+^2}{m}\right].
 \quad}                                                     \tag{12}
\]
When \(t_N(d)\le0\), (12) is only the trivial bound one.
When it is positive, condition on the initial finite history and
apply (2) with that value of \(x\).
Its dependence on \(H_{n_0}\) is legitimate because the initial
height is known under this conditioning. No null-history division
is used.

For the simpler envelope, (9) gives, for every real \(z\),
\[
              \{D_N\le z\}\subseteq\{H_N\le z+G(N)\}.
\]
Consequently, for \(x\ge0\),
\[
 \boxed{\quad
 P\!\left(D_N\le H_{n_0}+\frac m2-G(N)-x
                       \mid\mathcal F_{n_0}\right)
                    \le e^{-2x^2/m}.
 \quad}                                                     \tag{13}
\]
An impossible negative distance threshold has probability zero;
there is no hidden integer rounding requirement.
For a declared \(0<\delta<1\), a convenient consequence is
\[
 D_N\ge
 H_{n_0}+\frac m2-G(N)
       -\sqrt{\frac m2\log(1/\delta)}
                                                               \tag{14}
\]
with conditional probability at least \(1-\delta\).
Neither tails nor numerical intervals are evaluated here.

For \(m=0\), use the deterministic inequalities; do not divide by
\(m\). Unconditional versions follow by averaging the displayed
conditional statements over the random initial history. No iid
assumption on the growing orders or on deletion choices is introduced.

## 6. Sublinear target height forces a linear deletion fraction

Suppose now that \(g(k)/k\to0\) as integers \(k\to\infty\).
This does **not** require \(g\) to be monotone.

For any \(\epsilon>0\), choose a finite \(K\) such that
\(g(k)\le\epsilon k\) for all \(k\ge K\).
Let \(C_K=\max_{0\le k<K}g(k)<\infty\).
For \(N\ge K\), (8) then gives
\[
                 G(N)\le\max\{C_K,\epsilon N\}.
\]
Divide by \(N\), take a limsup, and let \(\epsilon\downarrow0\).
Thus
\[
                              G(N)=o(N).                    \tag{15}
\]
Finite exceptional small orders cannot invalidate this conclusion.

On the probability-one event in (3), the pathwise inequality (9)
holds for every \(N\). Therefore
\[
 \liminf_{N\to\infty}\frac{D_N}{N}
 \ge\liminf_{N\to\infty}\frac{H_N}{N}
       -\limsup_{N\to\infty}\frac{G(N)}N
 \ge\frac12 ,
\]
proving (1).

In particular, for every fixed \(0\le\eta<1/2\), almost surely
\(D_N\le\eta N\) occurs only finitely often.
A sublinear deletion sequence cannot produce targets in
\(\mathcal T\) for all sufficiently large \(N\), or for an infinite
unbounded subsequence eventually using a vanishing deletion fraction.
This includes deletion sets selected after seeing the realized order:
(5) already minimizes over **all** such subsets.

The conclusion is a liminf lower bound, not a limit or equality.
For example, the empty-only target has distance exactly \(N\);
the theorem does not assert that half the vertices always suffice.
It does not give a constructive approximation or any upper bound
better than the declared feasibility bound \(D_N\le N\).

The target and the common function \(g\) were fixed in advance.
An outcome-selected or \(N\)-dependent target family is not covered
merely by naming a different sublinear-looking bound at each size.
A new uniform-envelope argument would be required; no such
enlargement is made here.

## 7. A precise dense bounded-aspect Ferrers target

Fix constants
\[
                           0<\nu\le1,\qquad A\ge1,
\]
independently of \(N\) and the observed order.
Here \(\nu\) means **diagram occupancy**, not native event availability.

For a nonempty integer partition
\(\lambda_1=w\ge\lambda_2\ge\cdots\ge\lambda_r\ge1\),
define its Ferrers cell order
\[
 Q_\lambda=\{(i,j):1\le i\le r,\ 1\le j\le\lambda_i\},
\]
with
\[
 (i,j)\preceq(i',j')\quad\Longleftrightarrow\quad
 i\le i'\ \text{and}\ j\le j'.
\]
Let \(k=|Q_\lambda|=\sum_i\lambda_i\), and impose
\[
                   k\ge\nu rw,\qquad
                   A^{-1}\le r/w\le A.                     \tag{16}
\]
The \(r\)-by-\(w\) rectangle is the diagram's bounding rectangle,
using its nonzero rows and largest row.

Define \(\mathcal T_{\nu,A}\) to contain the empty order and all
finite orders **isomorphic to a diagram with a representation
satisfying (16)**. This existential representation definition is
isomorphism-invariant without assuming a uniqueness theorem for
Ferrers representations. Empty is included separately; no undefined
\(0/0\) aspect ratio is assigned to it.

### Exact Ferrers height; not always r+w-1

Along a strict chain, \(i+j\) increases by at least one.
A chain ending at cell \((i,j)\) therefore has at most \(i+j-1\)
vertices, since every cell has coordinate sum at least two.
Conversely, the path down the first column to row \(i\), then across
row \(i\), is present in the diagram and is a chain of length
\(i+\lambda_i-1\). Hence
\[
 \boxed{\quad
 h(Q_\lambda)=\max_{1\le i\le r}(i+\lambda_i-1)
                         \le r+w-1 .
 \quad}                                                     \tag{17}
\]
Equality with the bounding-rectangle value is not assumed for
a general partition.

### Explicit sublinear bound

Put \(x=r/w\in[A^{-1},A]\).
The inequality \((x-A)(x-A^{-1})\le0\), divided by \(x>0\),
gives \(x+x^{-1}\le A+A^{-1}\). Therefore
\[
 r+w
 =\sqrt{rw}\left(\sqrt{x}+\frac1{\sqrt{x}}\right)
 \le\left(\sqrt A+\frac1{\sqrt A}\right)\sqrt{rw}
 \le\left(\sqrt A+\frac1{\sqrt A}\right)\sqrt{k/\nu}.
\]
With the fixed constant
\[
                   K_{\nu,A}=\frac{\sqrt A+1/\sqrt A}{\sqrt\nu},
\]
equation (17) yields
\[
                  h(Q_\lambda)\le K_{\nu,A}\sqrt{k}-1.
                                                               \tag{18}
\]
In particular \(K_{\nu,A}\ge2\). A valid target height envelope is
\[
 g_{\nu,A}(0)=0,\qquad
 g_{\nu,A}(k)=K_{\nu,A}\sqrt{k}-1\quad(k\ge1).                \tag{19}
\]
It is nonnegative, nondecreasing and \(o(k)\); its jump from
\(k=0\) to \(k=1\) is harmless. The singleton diagram satisfies
(16) for all declared \(\nu,A\), and (18) is valid there as well.
There need not be a qualifying diagram at every larger size;
deleting to empty remains feasible.

For \(N\ge1\), \(G_{\nu,A}(N)=g_{\nu,A}(N)\).
Writing \(D_{\nu,A}=D_{\mathcal T_{\nu,A}}\), (9) becomes
\[
 \boxed{\quad
 D_{\nu,A}(P_N)\ge
      \max\{0,\ H_N-K_{\nu,A}\sqrt N+1\}.
 \quad}                                                     \tag{20}
\]
Thus
\[
 \boxed{\qquad
 \liminf_{N\to\infty}D_{\nu,A}(P_N)/N\ge1/2
 \quad\text{almost surely}
 \qquad}                                                     \tag{21}
\]
for the accepted baseline.

Its explicit finite-time version, for \(m=N-n_0\ge1,\ x\ge0\), is
\[
 P\!\left(
 D_{\nu,A}(P_N)\le
 H_{n_0}+\frac m2-K_{\nu,A}\sqrt N+1-x
 \mid\mathcal F_{n_0}\right)\le e^{-2x^2/m}.                  \tag{22}
\]
The inclusion proving (22) is precisely the height inclusion in
§5, not a claim that vertex deletions are random or iid.

### Why aspect alone is insufficient: the balanced thin hook

For integers \(t\ge2\), take the partition
\[
                         \lambda=(t,1^{\,t-1}).
\]
Then
\[
 r=w=t,\qquad k=2t-1,\qquad
 h(Q_\lambda)=t=\frac{k+1}{2},\qquad
 \frac{k}{rw}=\frac{2t-1}{t^2}\longrightarrow0.              \tag{23}
\]
Its aspect ratio is exactly one but its height is linear in cardinality.
For \(t\ge2\), its height also differs from \(r+w-1=2t-1\).
This rejects the attempted sublinear-height premise for
bounded-aspect Ferrers orders **without** occupancy control.
For any fixed \(\nu>0\), sufficiently large hooks fail the occupancy
condition in (16).

Occupancy alone is insufficient as well: a one-row chain has occupancy
one and height \(k\), but unbounded aspect as \(k\) grows.
Both conditions in this specific target definition are load-bearing.
If \(A\) is allowed to grow with \(N\), or \(\nu\) to decrease toward
zero, the fixed-\(K_{\nu,A}\) screen no longer follows unchanged.

These are declared shape restrictions, not DET principles,
derived law-selection conditions or physical manifold criteria.
The hooks are finite combinatorial examples, not constructed
alternative native histories.

## 8. Why this does not settle unrestricted Ferrers defect

Let \(\mathcal F\) be the unrestricted Ferrers cell-order class,
including empty. Every one-row chain \(C_N\) lies in \(\mathcal F\), and
\[
                     h(C_N)=N,\qquad D_{\mathcal F}(C_N)=0.
                                                               \tag{24}
\]
Thus a linear lower bound on height alone cannot imply positive
normalized deletion distance to \(\mathcal F\).
Equation (24) is a counterexample to that deterministic inference,
not a claim that the accepted stochastic baseline is an infinite chain.

Because \(\mathcal T_{\nu,A}\subseteq\mathcal F\), the distance
comparison has direction
\[
                    D_{\mathcal F}(P)\le D_{\nu,A}(P).
\]
A lower bound on the **larger** restricted-target distance does not
give the same lower bound on the unrestricted distance.

[THEOREM_PACKAGE](THEOREM_PACKAGE.md), §9, defines its existing expected-Ferrers-defect
objective using arbitrary vertex deletion to leave an unrestricted
induced Ferrers order. This packet does not silently replace that
objective by (16). Its separately prescribed optimizer and strict
restoration are also a different law from the all-layer common
half-scale baseline to which (2)–(3) apply.
Neither the optimizer's unproved Cesaro claims nor an actual
asymptotic unrestricted defect for the baseline is resolved here.

[LAW_DEPENDENCE](LAW_DEPENDENCE.md) distinguishes optional normalizations/objectives from
coordinate gauges. The present screen conditions on the already
specified baseline and separately declares a narrower target class.
It does not make either choice forced by DET.
A finite harmonic extension likewise does not inherit a proven
all-size history or this screen merely by being admissible at its
finite boundary.

## 9. Native prediction and mathematical observation channel

For a declared target, the intrinsic mathematical observation is
\[
                [P]\longmapsto
                \mathcal O_{\mathcal T}([P])
                  =\bigl(|P|,\ h(P),\ D_{\mathcal T}(P)\bigr),
                                                               \tag{25}
\]
where \([P]\) is the unlabelled finite order isomorphism class.
All three quantities ignore marks and external coordinates.
Exact complete-order access determines them mathematically.
No efficient algorithm, implemented classifier or tractable exact
distance computation is asserted.

The native prediction is concrete: under the selected baseline,
small values of the third component obey (12)–(13); for fixed dense
bounded-aspect Ferrers targets they obey (22), and their normalized
liminf obeys (21).
The height component alone already certifies the deterministic
distance lower bounds (9) or (20).
No target distance, height statistic or probability has been evaluated
on a dataset in this packet.

This channel does not supply physical access to the order, a
preparation/measurement procedure or calibration. Arbitrary vertex
deletion defines closeness of induced suborders; it neither authorizes
erasing committed records nor describes missing-record noise.
No observation-loss distribution or noisy-order correction is assumed.

The cardinality \(N\) is a bookkeeping event count, not physical time.
There is no spacetime-dimension inference, metric or clock,
Lorentzian/Poisson embedding or comparison, mass/gravity/QM conclusion
or empirical discriminator here.
An obstruction to this precise target does not exclude every possible
geometry, every Ferrers order, or every native growth law.

## 10. Completion, provenance and evidence boundaries

The completed yield consists of:

- The deterministic height-deletion inequality with valid nonmonotone
  and deletion-budget envelopes.
- Finite-time native distance bounds and the almost-sure
  \(\liminf D_{\mathcal T}(P_N)/N\ge1/2\) theorem for fixed
  sublinear-height targets.
- The explicit dense bounded-aspect Ferrers height bound and its
  resulting screen.
- The balanced thin-hook counterexample to the aspect-only premise,
  and the chain counterexample to an unrestricted-Ferrers inference.

No premise in the declared screen failed. The broader aspect-only
sublinear-height premise does fail, and (23) gives its exact obstruction.
The target was not enlarged or altered to conceal that failure.

The public exposition dependencies and their load-bearing uses are:

| File | Provenance and use |
| --- | --- |
| [HALF_SCALE_HEIGHT_GROWTH.md](HALF_SCALE_HEIGHT_GROWTH.md) | Accepted height theorem; source of (2)–(3), with source-manuscript construction and separate review status distinguished |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Accepted public exposition; baseline/optimizer distinction and unrestricted Ferrers objective |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Accepted public exposition; law/target choices are not coordinate gauges or principle-forced conclusions |

The height link is a public derivative of the accepted native source
manuscript. It does not imply that this private native manuscript was
already published with the other original exposition snapshots.
Source construction and separate review status remain distinct.

The source-author's literal snapshot and acceptance joins are retained
privately. Public links identify mathematical premises and preserve their
scientific uses; they do not supply the private pin or adjudication files,
or grant access to linked archives, audit members or protected sources.
The source-author's actual checks were present-byte/source correspondence
checks, not scientific execution or independent custody reconstruction.

The original evidence limitation is retained exactly:

Separate read/hash observations are not atomic identity certificates.
Accepted exposition and administrative joins do not reconstruct
original coefficient certificates or repair historical custody,
execution, source-check or receipt-matching failures. Those limitations
remain preserved.

For construction of the source manuscript, the retained statement is:

All proofs and displayed algebra are manual.

That statement describes source-author construction and supplied-context
manual challenges. Later independent review and its separate checks are
recorded separately. This derivative does not assert a machine proof,
executable source custody or scientific acceptance by its preparer.

The target and its common height envelope remain fixed in advance and
intrinsic. The nonmonotone and deletion-budget envelopes, finite-time
conditional tails and sublinear-envelope restriction are retained.
The dense bounded-aspect Ferrers target requires both occupancy and aspect
controls; the thin-hook failure of aspect-only height control remains.
Neither unrestricted Ferrers defect nor the separately prescribed optimizer
is resolved. The selected native probability law and narrower target are
optional choices, not forced by DET or obtained through a coordinate gauge.
Arbitrary deletion is a mathematical diagnostic, not record erasure,
missing-record noise or physical readout.

Private review identifiers, exact source paths, hashes, receipt filenames,
timestamps and tool/account metadata are withheld. The original evidence
and exact private-to-public correspondence remain local. No distance or
height statistic was evaluated on data, and no native probability,
coefficient, tail/interval, sampler, benchmark, calibration or experiment
was executed or is authorized here. No physical metric, dimension, clock,
geometry bridge or empirical validation is supplied. Frozen protocols and
protected validation inputs remain unchanged. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the public publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public/private boundary.
