# RI-58 — twin-top obstruction to uniform zero defect drift

24 September 2026 UTC. **Conditional structural obstruction and exact bounded
certificate; independent coordinator adjudication accepted.** For the unchanged
RI-41 prefix, every strict size-five extension has a defect-raising probability
greater than `13552/14457` on at least one of three specified marked rows.
Consequently the fixed-layer uniform zero-drift admission criterion fails.
This is a certified lower bound, not a proved optimum.

The result does **not** refute sublinear Cesaro defect for a history-weighted
all-size law. A worst-row obstruction at one fixed size supplies neither
typical occupation estimates nor a size-uniform asymptotic bound. No actual
records are deleted, no later-layer law is chosen, and no geometry follows.

## 1. Fixed model and defect diagnostic

Keep the complete [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through parent size four, with every mark assignment and probability unchanged.
Use the [RI-38 model](../native_joint_growth_extension_criterion_v1/CRITERION.md):
all ideal/bit branches are strictly positive, precursor records are read only
inside the ideal, whole unmarked parent order is available, full marked-parent
equivariance holds, and newborn binary marks are fair. Complete passive maps
remain `B_(S,b)(D)=q(S)D/2`; compositions retain the entire unnormalized D.

The [RI-56 diagnostic](../native_growth_ferrers_defect_v1/DEFECT.md) is

\[
 \delta(P)=\min\{|K|:P[V(P)\setminus K]\text{ is Ferrers}\},
 \tag{1}
\]

where K is arbitrary, the retained order is induced, and the empty retained
order is allowed. This is a mathematical comparison, not a history operation.
For every maximal birth its increment lies in `{0,1}`. Thus the conditional
expected increment in a marked parent row is also its probability of a
defect-raising birth. A nonempty parent's empty-ideal birth always raises.

The general structural lemmas below apply to any fixed complete strict prefix
providing the stated rectangle row. The exact numerical certificate uses only
the actual four-event prefix and selected five/six-event comparison orders.

## 2. The twin-top parent has exactly two neutral ideals

Let R be a product of chains of lengths `a,b>=2`, of size `N=ab>=4`, with
unique maximum m. Write `B=R\{m}` and add a clone y with strict past B:

\[
 P=R+y_B=B\oplus\operatorname{Ant}_2.
 \tag{2}
\]

RI-56 proves `delta(P)=1`. Its intrinsic twin-maxima lemma states that two
distinct Ferrers maxima with identical strict past force the entire order
to be the three-element V.

**Largest retained orders in P.** An induced N-vertex Ferrers suborder of P
must omit exactly one old top, m or y. Omitting any other vertex leaves both
maximal tops with equal strict past in an N-vertex order, where `N>=4`, so
the twin-maxima lemma excludes Ferrers membership. Omitting either top does
leave a rectangle. These are therefore the only largest retained subsets.

Now make an arbitrary maximal birth `T=P+x_S`. If it is neutral then
`delta(T)=1`, so an induced `(N+1)`-vertex Ferrers order G is obtained by
removing one vertex. Removing x leaves non-Ferrers P. Removing an old
non-top v is also impossible: since P is an ideal of T, `P\{v}` is an
ideal of G. Ferrers ideal closure would make `P\{v}` Ferrers, contrary
to the previous paragraph. This step uses ideal closure, not an assumption
that the old twins remain maximal after an arbitrary newborn is added.

It follows that G removes one of the old twins, call it e, and contains x
and the retained rectangle `R'=P\{e}`. By the intrinsic rectangle-corner
classification in [RI-54](../native_growth_ferrers_bottleneck_v1/BOTTLENECK.md),
the only Ferrers extensions of this non-chain rectangle have one of its
two distinct axis ideals `I_0,I_1` as the newborn past. There is no good
full extension. The two ideals lie in B and are unchanged when the twins
are exchanged.

If `e in S`, downward closure forces all of B into S, so `S intersect R'`
contains at least `N-1` vertices. But an axis ideal has only a or b vertices,
and `ab-1>max(a,b)` for `a,b>=2`. Therefore e cannot be in S. Hence
`S=S intersect R'=I_i`. Conversely, either axis birth is neutral: removing
one old twin leaves the corresponding Ferrers corner extension of R.

We have proved the exact classification

\[
 \delta(P+x_S)-\delta(P)=
 \begin{cases}0,&S=I_0\text{ or }I_1,\\1,&\text{every other ideal }S.
 \end{cases}
 \tag{3}
\]

In particular the full birth raises. In a square the axes are exchanged by
an automorphism but remain two distinct labeled ideal slots, each counted
once in normalization. Diagram coordinates in this proof are combinatorial
representatives, not physical coordinates supplied to a growth law.

## 3. Each neutral slot shares a component with a raising slot

Let `F_i=R+x_(I_i)`. This is Ferrers, with defect zero. Its proper ideal B
excludes both the old rectangle maximum and the corner newborn. Restoring
a top with past B gives

\[
 F_i+y_B\cong P+x_{I_i}.
 \tag{4}
\]

This terminal has defect one by (3). Thus the incoming P slot is neutral,
but the incoming F_i slot B raises defect. They are directly linked by the
actual R-based diamond; no merely isomorphic-payload identification is used.

Consequently both neutral P slots belong to proper ratio components with a
raising occurrence. In RI-56's equivalent boundary criterion these components
must be assigned zero scale. P has no remaining everywhere-neutral proper
component, while its full birth raises and would require neutral proper mass
one. This gives an intrinsic structural obstruction to the zero-drift boundary
system at this fixed layer. The quantitative proof next retains the actual
positive prefix weights instead of just their support.

## 4. Marked diamonds and the drift inequality

Fix a complete record r on R. Write

\[
 p=q_{R,r}(B)>0,\qquad a_i=q_{R,r}(I_i)>0.
 \tag{5}
\]

For the branch `P=R+y_B` give y bit u; for `F_i=R+x_(I_i)` give x bit v.
The two terminal histories identify the named x,y while swapping their last
two natural labels. They also transport their bits; the old record r is
unchanged. Equality of the two full branch maps is

\[
 p\,q_{P,r+u}(I_i)D/4
 =a_i\,q_{F_i,r+v}(B)D/4.
 \tag{6}
\]

For arbitrary D this gives the scalar identity

\[
 p\,x_i=a_i\,z_i,
 \quad x_i=q_{P,r+u}(I_i),\quad z_i=q_{F_i,r+v}(B).
 \tag{7}
\]

The first second-step probability reads only I_i and excludes y's mark u;
the other reads only B and excludes x's mark v. Thus these factors do not
depend on the respective first newborn bit. This does not erase other marks
from the local keys or from the complete parent states. The two fair-bit
factors are already included in `D/4`; there is no additional multiplicity
factor to insert into (7).

Choose any u and, for each F_i, any v. Let their actual defect drifts be
`mu_P,mu_(F_0),mu_(F_1)`, and let gamma be the maximum of these three marked
row drifts. Summing the fair newborn mark in a single row gives the usual
ideal probabilities q. Equation (3) and the raising F_i slot give

\[
 \mu_P=1-x_0-x_1,\qquad \mu_{F_i}\geq z_i.
 \tag{8}
\]

Therefore

\[
 p(1-\gamma)\leq p(1-\mu_P)
 =a_0z_0+a_1z_1\leq(a_0+a_1)\gamma,
\]
\[
 \boxed{\gamma\geq\frac{p}{p+a_0+a_1}>0.}
 \tag{9}
\]

For an admitted strict law the inequality is strict: each F_i has a distinct
empty-ideal raising slot of positive weight, so `mu_(F_i)>z_i`. Since each
a_i is positive, the last bound before (9) is then strict. This observation
does not establish the infimum or a matching law attaining the limiting
bound. Other marked rows and normalization constraints may strengthen it.

All probabilities and drifts here are conditional on their specified parent
states. The statement is that at least one of these rows has high drift;
it is not an unconditional probability of visiting them, and it is not a
claim that P alone must attain gamma. Maximizing over all rows of the layer
can only increase gamma.

## 5. Actual-prefix certificate at the first free layer

Use natural labels and strict predecessor masks as follows:

| Role | Order masks | Selected record mask | Distinguished slots |
|---|---|---:|---|
| R, four-event rectangle | `(0,1,1,7)` | 1 | Clone precursor 7; axes 3 and 5 |
| P, twin-top parent | `(0,1,1,7,7)` | 1 | Neutral slots 3 and 5 |
| F_3, first corner parent | `(0,1,1,7,3)` | 1 | Raising restored-top slot 7 |
| F_5, second corner parent | `(0,1,1,7,5)` | 1 | Raising restored-top slot 7 |

Record 1 means the unique root has bit one and all other listed vertices
have bit zero. It is **not** the all-zero record assignment. The chosen
newborns in these three comparison rows have bit zero; (6) remains valid
for all four u,v combinations, verified below for each axis.

The eight labeled P ideals are
`0,1,3,5,7,15,23,31`. Their child defects, in that order, are
`2,2,1,1,2,2,2,2`, whereas `delta(P)=1`. Both F_i have defect zero,
and their restored-top children have defect one. These finite defect values
are independently checked by searching arbitrary induced retained subsets,
not by presuming the structural proof or restricting exceptions to ideals.

The accepted prefix gives exactly

\[
 p=\frac{539}{625},\qquad
 a_0=a_1=\frac{1267}{44000},\qquad
 \frac{p}{p+a_0+a_1}=\frac{13552}{14457}.
 \tag{10}
\]

Thus every strict size-five completion of the unchanged prefix has

\[
 \max(\mu_{P,1},\mu_{F_3,1},\mu_{F_5,1})
 >\frac{13552}{14457}\approx0.9374005672.
 \tag{11}
\]

For this square and these marks, F_3 and F_5 are isomorphic marked rows.
Their two labeled branch occurrences are nevertheless both retained, giving
the two terms in (10); neither is divided out by symmetry.

Equivalently, (8) gives a positive weighted inequality
`(13552/14457) mu_P+(905/28914)(mu_(F_3)+mu_(F_5))>=13552/14457`.
The three coefficients sum to one, so the maximum row drift is at least
that lower bound. This is a certificate inequality, not a replacement of
the marked-row requirements by an averaged feasibility assumption.

### Direct local keys and potentials

The actual RI-38 local keys are whole-parent/ideal/inside-record canonical
triples. For each axis, with either first-newborn bit, they are

| Slot | Canonical local key | Positive potential |
|---|---|---:|
| Neutral P axis | `(25374,3,1)` | `229327/8800000` |
| Raising F_i restored-top slot | `(8990,7,1)` | `97559/125000` |

The exact potential identity is `p*u_P(I_i)=a_i*u_(F_i)(B)`.
The slots therefore are endpoints of a genuine positive ratio edge, not
assumed to share a component because their scalar values happen to coincide.
The component scale is an unknown new-law choice; no new row probability
has been evaluated. Both structural labeling and fixed-prefix factors are
part of the certificate.

### Bounded choice of marking

Read-only inspection of all sixteen markings of this one fixed R row gave
two classes. Root-bit-zero records have
`p=46569/55000`, `a_0=a_1=741/20000`, and bound `1634/1777`.
Root-bit-one records have (10). The latter is stronger, so the complete
record mask 1 was selected for the final obstruction. No solver, fit,
new size-five row table or averaged marked relaxation was used. A single
complete record assignment already suffices to disprove a uniform zero-drift
claim; the old-row comparison only improves this same bounded certificate.

## 6. Exact bounded verification and provenance

The [certificate](CERTIFICATE.json) identifies the selected orders, markings,
slots, all finite defects, actual old factors, local edges and rational bound.
The [checker](check.py) uses only the standard library. It explicitly reuses
the accepted RI-52 prefix helper after checking its byte hash before execution;
the helper is loaded with a non-main name. Its main and Ferrers target-matrix
routine are not invoked. This is pinned helper reuse, not an independently
reimplemented growth prefix.

The pinned dependencies are:

| Dependency | SHA-256 |
|---|---|
| Accepted RI-52 `check.py` | `822d49b766a2ef2862f289f9e4abb4a262cfafcf58ac3ff4c34c044e75f6c654` |
| Accepted RI-41 `CERTIFICATE.json` | `3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969` |

Both hashes are checked before the helper is executed. The actual RI-41
certificate's 109 roots, default scale and 62 overrides are also compared
directly with the helper's embedded data. Its unchanged prefix reconstruction
checks 707 marked rows, 6065 labeled slots, 436 lower scalar diamonds and
7616 RI-41 ratios. The new runtime's local research-file dependency closure
is its checker/certificate plus these two pinned files.

The new finite-order routine searches induced subsets of only the selected
orders of at most six vertices, comparing complete order relations against
Ferrers partition representatives. It is separate from the reused prefix
helper's shape routines. No full size-five or size-six growth-order layer,
global component graph, global linear program or later-layer probability
table is evaluated.

Actual coverage is 14 selected naturally labeled orders and all 752 of their
induced-subset occurrences, including empty subsets. Complete transitive pasts
and precursor ideals are validated. The diagnostic catalogue covers every
integer partition at sizes zero through six, with counts `1,1,2,3,5,7,11`,
and classifies them by complete order permutations into `1,1,1,2,3,4,6`
intrinsic Ferrers types. This catalogue tests the diagnostic definition; it
is not a supplied growth generator or physical mesh.

All eight P ideals and their child defects are checked. P's only optimal
retained masks are 15 and 23, removing one twin in each case. The comparison
keeps three raw marked rows and two marked isomorphism classes. All sixteen
old R record assignments are inspected only through the unchanged prefix.

The checker verifies the natural-label swap of vertices 4 and 5 together
with their marks for both axes and all four newborn-bit pairs. The resulting
eight raw diamonds retain both labeled ideal occurrences. Their scalar
identities are identities of potentials times fixed prefix probabilities,
so the implication for arbitrary D is algebraic. No numerical payload test
or informative quantum coupling is claimed.

The certificate's exact normalized drift coefficients are checked to sum to
one and to equal the old weights divided by `p+a_0+a_1`. Three in-memory
malformed controls must fail for their precise intended reasons: replacing
axis 5 by 7, increasing the declared bound by `1/1000`, and supplying base
record 16 outside the four-bit cube. None changes a source or certificate file.

Main execution used CPython 3.14.0 from the repository root:

```sh
/opt/homebrew/bin/python3 -I -S -B docs/track_b/native_growth_defect_bottleneck_v1/check.py
/opt/homebrew/bin/python3 -I -S -B -O docs/track_b/native_growth_defect_bottleneck_v1/check.py
```

Both runs exited zero with empty stderr in approximately 0.222 seconds each.
Their stdout was byte-identical: 1182 bytes, SHA-256
`9d74a7b2ebfb7ac195bd6c0173563c5a1167cdbb6e036e9abe7b02525d061e1a`.
The author independently reproduced the same outputs in both modes.

Separate analytic reviews read the complete proof, reconstructed the actual
prefix factors and local potentials, and checked the strict drift bound and
its scope. Main read every checker and certificate line. A separate reviewer
also read every line of the checker, certificate and complete note, then
replayed both modes with the same interpreter and isolation flags. Both
runs exited zero with empty stderr in approximately 0.228 and 0.230 seconds,
and reproduced the identical 1182-byte stdout and hash above. That review
confirmed the independent induced-subset classification, marked transport,
prefix reconciliation and all refusal controls. The checker author also
cross-checked note/certificate alignment. No mathematical or source blocker
remained. Coordinator adjudication is separate and recorded in the opening.

## 7. Disposition and limits

The RI-56 uniform zero-defect-drift boundary gate fails at this fixed layer
under the actual prefix. The structural reason is an empty everywhere-neutral
component support row at a full-raising twin-top parent. The quantitative
certificate supplies the positive lower bound (10) over three marked rows.
It does not establish an optimal worst-row value.
Strict compatible completions still exist by RI-38; what fails is the
additional uniform zero-drift requirement, not consistency of the prefix.

The prefix-dependent bound for one layer supplies no lower bound on the
occupation frequencies of these parent states along later histories. It does
not show that Cesaro conditional drift stays positive, that delta_N/N cannot
tend to zero, or that future layers cannot have smaller worst-row bounds.
The general rectangle proof also does not keep the probability ratio (9)
uniformly away from zero as rectangle size and inherited law vary.

No alternative seed, history repair, defect-control selection, all-size
feasibility decision, near-square limit, informative quantum coupling,
metric, clock, source or gravity is supplied. Option B and metric-as-record
Status M are unchanged; RET stays paused.

Only `OBSTRUCTION.md`, `check.py` and `CERTIFICATE.json` in this new directory
are authored. Accepted sources, measurement work and coordinator records
remain untouched. The coordinator owns git/index/publication. Stop at this
source-stable handoff for independent adjudication; no successor is started.
