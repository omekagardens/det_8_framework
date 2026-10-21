# Dense Ferrers incomparability screen

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: the existing fixed dense bounded-aspect Ferrers target and the
accepted optional factorial-subset law. Neither target nor law is changed.

## 1. Bounded theorem and exact dependencies

Fix real constants \(0<\nu\le1\) and \(1\le A<\infty\), independently of
size and history. For the target \(\mathcal T_{\nu,A}\) defined in section 2,
the explicit constants

\[
 \boxed{\epsilon(\nu,A)=\frac{\nu^4}{128}>0,\qquad
 m_0(\nu,A)=\left\lceil\frac{16A}{\nu^2}\right\rceil}
 \tag{1}
\]

have the following property: every target member \(Q\) of size \(m\ge m_0\)
has at least \(\epsilon\binom m2\) incomparable unordered pairs.
The constant \(\epsilon\) happens to depend only on \(\nu\); \(A\) enters
the size threshold. Neither constant is asserted optimal.

For the fixed accepted factorial-subset law \(P_N\), this establishes

\[
 \boxed{\frac{R_{\nu,A}(P_N)}N\longrightarrow0,\qquad
        \frac{D_{\nu,A}(P_N)}N\longrightarrow1
        \quad\text{almost surely},}
 \tag{2}
\]

where \(R_{\nu,A}\) is largest induced retained size in this exact target
and \(D_{\nu,A}=|P|-R_{\nu,A}\). The empty-order convention and finite
retained-size bound are given below.

There are three exact mathematical dependencies:

1. Section 7 of the supplied INTRINSIC_GEOMETRY_TARGET_SCREEN.md fixes the
   target definition. Section 2 reproduces that definition without adding
   representation uniqueness or a rectangle/shape condition.
2. The accepted FACTORIAL_SUBSET_HEIGHT_LAW.md supplies the fixed from-empty
   marked-order process. Its law is restated in section 5; it is not derived
   or redesigned here.
3. The exactly accepted ORDERING_FRACTION_OF_FACTORIAL_LAW.md proves
   \(I(P_N)/\binom N2\to0\) almost surely for that law and supplies the
   conditional induced-target retained-size bound. Sections 3–4 prove
   the missing target premise directly; section 5 verifies the deterministic
   specialization and applies the accepted stochastic conclusion.

The proof of the new target premise is self-contained finite combinatorics.
The stochastic input is expressly the accepted law-specific theorem, not
an inference from its separate sublinear-height result. The conclusion
is a target-specific approximation obstruction, not physical geometry.

## 2. The unchanged target and observable

For a nonempty integer partition

\[
 \lambda_1=w\ge\lambda_2\ge\cdots\ge\lambda_r\ge1,
\]

let

\[
 Q_\lambda=\{(i,j):1\le i\le r,\ 1\le j\le\lambda_i\},
\]

with coordinatewise order

\[
 (i,j)\preceq(i',j')
 \quad\Longleftrightarrow\quad i\le i'\ \text{and}\ j\le j'.
\]

The bounding rectangle uses the \(r\) nonzero rows and the largest row
length \(w\). Write \(k=|Q_\lambda|=\sum_i\lambda_i\). The existing target
conditions are exactly

\[
 k\ge\nu rw,\qquad A^{-1}\le r/w\le A.
 \tag{3}
\]

Here \(\nu\) is **diagram occupancy**, not event availability.
The target \(\mathcal T_{\nu,A}\) consists of the empty order, included
separately, and all finite orders isomorphic to some \(Q_\lambda\) with
a representation satisfying (3). No aspect ratio is assigned to empty.

Membership is existential over representations. The proof will work for
every qualifying representation, so no uniqueness of Ferrers representation
is required. No claim is made that a qualifying representation exists at
every cardinality.

For a finite order \(P\), let \(I(P)\) count unordered pairs of distinct
incomparable vertices. Set

\[
 \eta(P)=
 \begin{cases}
 0,&|P|\le1,\\
 I(P)/\binom{|P|}{2},&|P|\ge2.
 \end{cases}
 \tag{4}
\]

Cardinality and \(I(P)\) are isomorphism invariants. The theorem asserts
a positive lower bound on (4) only for sizes at least \(m_0\), not for
empty, singleton or all smaller shapes.

## 3. Occupancy forces a rectangular subdiagram

For any nonempty representation satisfying (3), define the integers

\[
 a=\left\lceil\frac{\nu r}{2}\right\rceil,\qquad
 b=\left\lceil\frac{\nu w}{2}\right\rceil.
 \tag{5}
\]

Since \(0<\nu\le1\) and \(r,w\) are positive integers,
\(1\le a\le r\) and \(1\le b\le w\).
We claim that \(\lambda_a\ge b\).

If instead \(\lambda_a<b\), integrality and the ceiling convention give

\[
 \lambda_a\le b-1<\frac{\nu w}{2},
 \qquad
 a-1<\frac{\nu r}{2}.
\]

By monotonicity of the row lengths, the first \(a-1\) rows have length
at most \(w\), and every later row has length at most \(\lambda_a\).
There is at least one later row because \(a\le r\). Thus

\[
 \begin{aligned}
 k
 &\le(a-1)w+(r-a+1)\lambda_a\\
 &<(a-1)w+r\frac{\nu w}{2}
 <\nu rw,
 \end{aligned}
\]

contrary to (3). This proves \(\lambda_a\ge b\). Consequently every cell
in

\[
 \{1,\ldots,a\}\times\{1,\ldots,b\}
 \tag{6}
\]

belongs to the original diagram.

This is a derived contained rectangle, not an assumption that the whole
diagram is rectangular, nor a new restriction on allowed shapes.
The argument uses occupancy and monotonicity of row lengths; it does not
yet need bounded aspect and remains valid for small diagrams.

## 4. A uniform incomparable-pair density

The aspect inequalities in (3) imply \(w\le Ar\) and \(r\le Aw\).
Since every diagram lies in its bounding rectangle,

\[
 k\le rw\le Ar^2,\qquad k\le rw\le Aw^2.
\]

It follows that

\[
 r,w\ge\sqrt{k/A}.
 \tag{7}
\]

For an integer \(k\ge m_0=\lceil16A/\nu^2\rceil\), (7) yields
\(r,w\ge4/\nu\), and hence the rectangle (6) has \(a,b\ge2\).
This is where the fixed aspect bound is used: both contained dimensions
are nondegenerate once the total size exceeds the stated threshold.

For each row pair \(i_1<i_2\) and column pair \(j_1<j_2\) in (6), the two
cells

\[
 (i_1,j_2),\qquad(i_2,j_1)
\]

are incomparable. Each coordinate increases in a different direction, so
neither cell is coordinatewise below the other. These incomparable pairs
are in bijection with the choices of two rows and two columns. Thus the
rectangle has exactly \(\binom a2\binom b2\) incomparable unordered pairs.
They remain incomparable in the ambient coordinatewise order; outside
cells cannot change the relation between them.

For every integer \(a\ge2\),
\(\binom a2=a(a-1)/2\ge a^2/4\), and similarly for \(b\).
Using (5), \(k\le rw\), and \(k(k-1)\le k^2\), we obtain

\[
 \begin{aligned}
 I(Q_\lambda)
 &\ge\binom a2\binom b2
 \ge\frac{a^2b^2}{16}\\
 &\ge\frac{\nu^4r^2w^2}{256}
 \ge\frac{\nu^4k^2}{256}\\
 &\ge\frac{\nu^4}{128}\binom k2.
 \end{aligned}
 \tag{8}
\]

This proves the density premise with (1). Since \(k\) and \(I\) are
isomorphism invariant, (8) holds for every order in \(\mathcal T_{\nu,A}\)
of the required size, regardless of which qualifying representation is
chosen.

### Finite, degenerate and boundary cases

The threshold in (1) is an integer at least sixteen, hence at least two.
It is finite for every fixed permitted \(\nu,A\). The ceiling ensures
\(k\ge m_0\) implies the real inequality \(k\ge16A/\nu^2\); no omitted
rounding convention is needed.

The empty order is handled separately and has \(I=0\). The one-cell diagram
has \(r=w=k=1\), satisfies (3) for every permitted \(\nu,A\), and also has
\(I=0\). Both lie below the density threshold. Other small shapes need no
positive density assertion in this theorem.

If \(r=1\) or \(w=1\), the aspect bound forces the other dimension, and
therefore the size, to be at most \(A<m_0\). Such thin chain
representations cannot violate the large-size conclusion.

At \(\nu=1\), occupancy and \(k\le rw\) force \(k=rw\), so every row has
length \(w\); the argument covers this case. At \(A=1\), the aspect bound
gives \(r=w\); the diagram need not be full unless \(\nu=1\), and the same
proof still applies.

These are sufficient conditions and conservative constants, not a
necessity or optimality theorem. In particular, the balanced thin hook
used in the target source is a counterexample to a height argument without
occupancy, not automatically to an incomparable-density claim. For
\(\lambda=(t,1^{t-1})\), \(t\ge2\), the two non-origin arms are chains but
every pair with one vertex on each arm is incomparable. Hence
\(I=(t-1)^2\) and \(\eta=(t-1)/(2t-1)\), which tends to \(1/2\).
Large hooks fail the fixed occupancy condition, and this observation is
not used to strengthen or alter the target.

## 5. Exact retained-size bound and factorial-law consequence

For any finite order \(P\), define

\[
 \begin{aligned}
 R_{\nu,A}(P)
 &=\max\{|W|:W\subseteq V(P),\ P[W]\in\mathcal T_{\nu,A}\},\\
 D_{\nu,A}(P)&=|P|-R_{\nu,A}(P).
 \end{aligned}
 \tag{9}
\]

The empty target makes the maximization feasible. On empty \(P\), set
\(R_{\nu,A}=D_{\nu,A}=0\), and set the normalized deletion fraction to
zero. A one-point order belongs to the target for every permitted parameter
pair, so its retained size is one and deletion distance/fraction are zero.
For nonempty \(P\), the normalized deletion fraction is
\(D_{\nu,A}(P)/|P|\).

Crucially, \(P[W]\) is the restriction of the completed order to \(W\).
Relations between retained vertices are unchanged, even if a generating
DAG path originally passed through deleted vertices. Deleting DAG vertices
and recomputing reachability is a different operation, not the distance
in (9). Under induced order restriction,

\[
 I(P[W])\le I(P).
 \tag{10}
\]

If an eligible retained set has size \(m\ge m_0\), the newly proved density
bound implies

\[
 \frac{\nu^4}{128}\frac{m(m-1)}2
 \le I(P[W])\le I(P).
\]

Solving the quadratic gives

\[
 m\le
 \left\lfloor\frac{1+\sqrt{1+1024I(P)/\nu^4}}2\right\rfloor.
\]

For \(m<m_0\), instead \(m\le m_0-1\). Hence, with

\[
 B_{\nu,A}(I)
 =\max\left\{m_0-1,\;
 \left\lfloor\frac{1+\sqrt{1+1024I/\nu^4}}2\right\rfloor\right\},
\]

we have the exact deterministic bounds

\[
 \boxed{
 R_{\nu,A}(P)\le\min\{|P|,B_{\nu,A}(I(P))\},\qquad
 D_{\nu,A}(P)\ge\max\{0,|P|-B_{\nu,A}(I(P))\}.
 }
 \tag{11}
\]

This is the accepted generic retained-size bound specialized to the
now-proved constants, with its short deterministic argument supplied.
It is a bound, not a claim of attainability. The \(m_0-1\) term keeps all
small qualifying diagrams allowed. No induced-suborder closure of the
target is assumed.

The fixed stochastic law used here draws, independently across births,

\[
 \Pr(U_n=U)=\frac1{|U|!\,Z_n},\qquad
 Z_n=\sum_{k=0}^n\frac{\binom nk}{k!},
 \qquad U\subseteq[n],
 \tag{12}
\]

and assigns newborn \(n+1\) strict past \(\downarrow_{P_n}U_n\), an
independent fair immutable bit, and the declared passive PSD payload map.
It starts from empty and remains unchanged at every size. Selection
indicators within one subset are not independent.

The accepted ordering-fraction theorem for precisely (12) states

\[
 \eta(P_N)=\frac{I(P_N)}{\binom N2}\longrightarrow0
 \quad\text{almost surely},
 \tag{13}
\]

with the zero/one-size convention (4). Its proof and admissibility
dependencies are not rerun or expanded here. Equation (13) entails
\(I(P_N)=o(N^2)\) almost surely.

Since \(\nu,A,m_0\) are fixed, (11) then gives
\(B_{\nu,A}(I(P_N))/N\to0\): the constant term vanishes after division by
\(N\), and the square-root term does also. Consequently

\[
 \frac{R_{\nu,A}(P_N)}N\longrightarrow0,\qquad
 \frac{D_{\nu,A}(P_N)}N
 =1-\frac{R_{\nu,A}(P_N)}N\longrightarrow1
 \quad\text{almost surely}.
 \tag{14}
\]

Thus, for this law and this exact fixed target, no positive asymptotic
fraction of vertices can be retained in a qualifying induced order.
In particular, approximation by deleting \(o(N)\) vertices is excluded.
This closes the target-specific question; it does not contradict the
same law's separate sublinear-height theorem. Sublinear height was only
one necessary structural test, not a sufficient approximation theorem.

## 6. Boundaries of the conclusion

The fixed-parameter assumption matters. This note does not replace
\(\nu,A\) with history-dependent or size-dependent values, weaken occupancy,
allow growing aspect bounds, or assert a uniform result for such changing
classes. It does not classify the weakest sufficient assumptions.

The unrestricted Ferrers class contains chains of every size, represented
by a single row. Those chains have no incomparable pairs, so that larger
class does not satisfy the uniform positive-density premise used here.
If \(D_{\rm Ferrers}\) denotes deletion distance to the unrestricted class,
then

\[
 D_{\rm Ferrers}(P)\le D_{\nu,A}(P),
\]

because the target in this note is a subclass. A lower bound tending to
one for the restricted normalized distance therefore gives no such lower
bound for the unrestricted objective. No unrestricted approximation or
optimizer result is supplied.

The separate optimizer is not identified with the law (12), and no
minimization, optimizer convergence or coefficient-selection claim follows.
Other optional laws need not have the ordering-fraction limit (13);
the law-specific stochastic conclusion is not transferred to them.
Likewise, the target conditions are declared mathematical shape conditions,
not DET-derived principles.

No manifold, metric, dimension, Lorentzian reconstruction, gravity/mass
law or physical observation is established or excluded. The record-order
diagnostic does not assert that records exhaust live relational activity,
nor that order alone is the full quantum-record mapping. Binary marks and
the passive quantum payload remain part of the declared process; this
calculation does not reconstruct their dynamics.

All new reasoning is manual symbolic proof. There is no scientific
executor, numerical probability/tail/interval evaluation, simulation,
optimizer run, sample history, experiment, dataset acquisition, protected
validation or network research. No successor, new gate, protocol change,
RET, clock, book or retired-gravity work is opened.

## 7. Source and evidence scope

The public exposition dependencies and their scientific roles are:

| Public source | Scientific role |
| --- | --- |
| [ORDERING_FRACTION_OF_FACTORIAL_LAW.md](ORDERING_FRACTION_OF_FACTORIAL_LAW.md) | Accepted law-specific incomparable-fraction limit and generic conditional retained-size bound; native predecessor in the original source set. |
| [FACTORIAL_SUBSET_HEIGHT_LAW.md](FACTORIAL_SUBSET_HEIGHT_LAW.md) | Fixed optional from-empty marked-order process and its separate sublinear-height result; height alone does not supply the stochastic density input. |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Section 7 defines the unchanged fixed dense bounded-aspect Ferrers target, with existential qualifying representations. |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Declared marked-order model, immutable bits, passive PSD payload and complete structural constraints. |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Optional law choices and fixed-prefix boundaries; no conclusion is transferred to other laws or a separate optimizer. |
| [HEIGHT_DRIFT_LAW_SELECTION.md](HEIGHT_DRIFT_LAW_SELECTION.md) | Height and actual-history drift obligations; sublinear height alone is not sufficient target approximation. |

The six authorized literal manuscript copies and two literal provenance
records were the source-author's complete source set. Their full native
read captures, exact hash/byte observations and pin joins remain in the
private source record. No original path, linked archive, source program,
additional adjudication member or protected material was followed in that
process. These are source-author evidence statements, not a fresh audit
of linked originals by the public derivative preparer.

The native ordering-fraction manuscript retains its historical pending
header. Its exact later adjudication, joined to the matching subject hash
and byte count, accepts the factorial-law ordering fraction and conditional
target obstruction. That predecessor acceptance is an input to this note,
not acceptance of this note. The link above is its public derivative; it
does not claim that the native original was among the five historical
public exposition snapshots.

The supplied pin record attributes the five public exposition copies to a
public source commit. This is metadata, not an independent Git/network
verification. The changed public factorial-law body was fully displayed
and consumed; unchanged complete bodies and exact prefixes were joined
to previously consumed bodies. New appended package/law sections were
displayed and consumed. The exact target's section 7 was additionally
displayed in full. The source-author record reports no truncated displays
in those reads. Current public navigation can include later appended
history, distinct from the original source snapshots.

The original manual-worker account is retained:

Two independent manual workers checked the supplied rectangle/density
argument, finite cases, representation issue and target consequence.
They performed no source/file access or scientific execution. Their
worker-reported supported usage observations are distinct from root-direct
observations. Their agreement is a mathematical cross-check, not a source
audit, proof-assistant certificate or native acceptance.

Those worker summaries and usage transcriptions remain supplied-context
reports, distinct from direct coordinator observations and independent
source audits. Source-author manual construction, worker cross-checks,
administrative readbacks and later independent review are different
activities and supply different evidence.

The original evidence limitation is retained:

Full native source/manuscript captures and metadata-only summaries of
own-receipt readbacks are labelled separately. Separate read/hash
observations are not atomic original-custody proofs. Prior failed captures,
custody limitations and actual protected validation are not erased,
reconstructed or recertified. The RET-only pause and separation of physical
readout/preparation and application benchmarks remain intact.

All six scientific sections above retain the source-author's manual symbolic
proof and exact scope. The source-author's bounded activity statements do
not determine any later coordinator selection after separate native
acceptance. No result for a further obligation is supplied here. A final
publication review record is conditional on the separate native, editorial
and root acceptance gates; preparation of this derivative is not theorem
adjudication or proof-assistant verification.

Private identifiers, exact paths, hashes, timestamps, receipt filenames,
tool/account metadata and private adjudication records are withheld.
The original four-artifact source packet and exact correspondence remain
local. Public links identify mathematical dependencies, not executable
private-source custody. No numerical probability or tail evaluation,
scientific execution, data acquisition, experiment, protected validation
or physical readout is supplied or authorized. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public evidence boundary.
