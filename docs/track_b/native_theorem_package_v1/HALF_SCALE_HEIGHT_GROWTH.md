# Linear intrinsic height under the all-layer half-scale baseline

21 October 2026. Manual conditional native-order theorem.
No implementation, coefficient calculation or empirical experiment.
Independent review is recorded separately from this source manuscript.

## 1. Result

**The selected all-layer half-scale baseline forces linear intrinsic
longest-chain height almost surely.** This is a theorem about one
native growing history under its admitted classical history measure,
not about iid repeated preparations.

Let \(P_N\) be its order after \(N\) births and let \(H_N\) be the
maximum **number of vertices** in a chain of \(P_N\).
Conditional on the admitted valid finite prefix, ratio-potential
theorem and specified all-layer baseline,
\[
 \boxed{\qquad
 \liminf_{N\to\infty}\frac{H_N}{N}\ge\frac12
 \quad\text{almost surely}.
 \qquad}                                                     \tag{1}
\]
For every fixed starting size \(n_0\ge6\), put \(m=N-n_0\).
If \(C_m\) counts full births among the next \(m\) births, then,
for \(m\ge1,\ x\ge0\),
\[
 \begin{split}
 P\!\left(C_m\le\tfrac m2-x\mid\mathcal F_{n_0}\right)
       &\le e^{-2x^2/m},\\
 P\!\left(H_N\le H_{n_0}+\tfrac m2-x
                      \mid\mathcal F_{n_0}\right)
       &\le e^{-2x^2/m}.                                    \tag{2}
 \end{split}
\]
Here \(\mathcal F_n\) is the complete marked-history filtration.
Conditional assertions hold almost surely, and in particular on every
admissible finite history of positive probability.

Since \(H_N\le N\), the precise height-versus-cardinality consequence is
\[
 \boxed{\qquad
 \lim_{N\to\infty}\frac{\log H_N}{\log N}=1
 \quad\text{almost surely}.
 \qquad}                                                     \tag{3}
\]
No convergence of \(H_N/N\) to \(1/2\), exact limiting speed, or
size-uniform improvement above \(1/2\) is established.

This result does not require \(\Xi>1\), an actual coefficient-branch
decision, an additional finite harmonic deformation, or a computed
coefficient table. It does require the optional half-scale prescription
at **every** parent size \(n\ge6\), not merely at one layer.
It is an intrinsic order statistic, not a spacetime dimension,
physical clock, geometry bridge, QM/gravity result or empirical validation.

## 2. Exactly which law and history measure are used

[THEOREM_PACKAGE](THEOREM_PACKAGE.md), §1, defines a state as a finite order \(P\), immutable
binary marks \(r\), and an arbitrary complex PSD payload \(\mathfrak D\).
A birth chooses an ideal \(S\subseteq P\) and appends one new maximal
vertex whose strict past is exactly \(S\). The old induced order and
marks are retained. Every ideal, including empty and full, has
strictly positive probability, and
\[
 \sum_{S\ {\rm ideal\ of}\ P}q(P,r,S)=1,\qquad
 \mathcal B_{S,b}^{P,r}(\mathfrak D)
             =\frac{q(P,r,S)}2\mathfrak D,\quad b\in\{0,1\}. \tag{4}
\]
The newborn bit is fair; both outcomes belong to the complete row.

Preserve the source package's admitted prefix through parent size five.
Thus its transitions through six births are fixed, including the
prescribed parent-four witness and restored parent-five instance.
No earlier witness, objective, selector or coefficient is changed.

For every later parent size \(n\ge6\), use the source's baseline B.
In its **specified maximal-deletion-potential convention**,
\[
 u(P,r,S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}},
 \quad S\subsetneq P.                                      \tag{5}
\]
Every smaller full slot retains its full induced marking.
The complement of a proper ideal contains a maximal element, so the
index set is nonempty. These are evaluations of smaller-law inputs,
not deletion of committed events.

Define
\[
 T_{P,r}=\sum_{\substack{S\ {\rm ideal\ of}\ P\\S\subsetneq P}}
                           u(P,r,S),\qquad
 M_n=\max_{\substack{|P|=n\\r:P\to\{0,1\}}}T_{P,r},\qquad
 a_n=\frac1{2(1+M_n)}.                                     \tag{6}
\]
The maximum covers the **whole marked layer**, and the sum counts
every individual proper ideal occurrence. A fixed finite label set
with all orders and markings gives a finite representative domain;
equivariance transports the construction. No selected-support or
root-only maximum substitutes for (6).

All smaller probabilities are positive finite inputs. Hence every
potential is positive and finite, and \(0<M_n<\infty\) at each
\(n\ge6\). No bound uniform in \(n\) or numerical value is needed.
The complete baseline row is
\[
 q_B(P,r,S)=a_nu(P,r,S)\quad(S\subsetneq P),\qquad
 q_B(P,r,P)=1-a_nT_{P,r}.                                   \tag{7}
\]
The admitted ratio-potential construction supplies compatibility,
locality and equivariance; the full slot is the complement of the
**entire** proper row. This proof does not rederive that admitted
construction from DET primitives or authenticate its original certificates.

[THEOREM_PACKAGE](THEOREM_PACKAGE.md), §9, explicitly distinguishes the all-size continuation
from the expected-defect optimization recursion. Its compatible finite
history probabilities give an infinite classical history measure.
That admitted existence is the probability-space premise used here.
On each finite history the next marked branch has probability
\(q_B(P_n,r_n,S)/2\); the complete next-branch sum is one.
The finite prefix need not itself obey the later half-scale bound.

This theorem is about B alone. It is not a theorem about the separately
optimized expected-defect recursion, nor an all-size extension of a
finite harmonic perturbation. The source expressly leaves that latter
extension unproved.

### Payload and zero normalization

The classical kernel \(q_B/2\) is specified independently of the
payload and is normalized by the complete ideal/bit sum.
For a PSD payload with finite positive trace, a branch trace ratio
also equals \(q_B/2\), but the theorem does not need that interpretation.

If \(\mathfrak D=0\), every branch map in (4) is zero. No probability
can be obtained by a \(0/0\) trace normalization; none is attempted.
The linear map and diamond identities still hold, and the separately
declared classical history kernel remains defined.
Payload passivity is an admitted model feature, not a derivation of
informative quantum dynamics.

## 3. Conditional full-birth floor, including every mark and both bits

For every marked parent of size \(n\ge6\), \(T_{P,r}\le M_n\).
Its complete full-birth probability therefore satisfies
\[
 \begin{split}
 q_B(P,r,P)
 &\ge1-\frac{M_n}{2(1+M_n)}\\
 &=\frac12+\frac1{2(1+M_n)}
   =\frac12+a_n>\frac12 .                                  \tag{8}
 \end{split}
\]
This is uniform over every parent and old marking at that size.
It supplies the common floor \(1/2\) at all sizes, even if the
additional \(a_n\) is not bounded away from zero as \(n\) varies.
No assertion that it actually tends to zero is needed or made.

Let \(X_{n+1}\) be one if the birth from \(P_n\) selects \(S=P_n\),
and zero otherwise. Conditional on the full realized history,
\[
 \begin{split}
 p_{n+1}
 :=E[X_{n+1}\mid\mathcal F_n]
 &=\sum_{b=0}^1\frac{q_B(P_n,r_n,P_n)}2\\
 &=q_B(P_n,r_n,P_n)
 \ge\frac12+a_n>\frac12 .                                  \tag{9}
 \end{split}
\]
There is no extra factor \(1/2\) after summing the two newborn bits.
Marks can affect the next law, and the shape and size certainly
change along the history; (9) remains true after conditioning on
all those past facts. Neither the \(X_{n+1}\) nor the native births
are asserted to be independent or identically distributed.

All following conditional estimates may be integrated over the random
initial history, because their constants are uniform over its
admissible marked realizations. No conditioning on an individual
zero-probability infinite history is used.

## 4. Deterministic chain and height facts

A full birth appends a vertex strictly above **every** earlier vertex.
If two births are full and the first precedes the second, the second
therefore lies above the first. All full-birth vertices form a chain
in their chronological order.

A longest old chain can be extended by the new full-birth vertex.
Conversely, deleting the new vertex from any chain containing it
leaves an old chain, so a single birth can increase height by at most
one. Old chains are never lost. Thus
\[
 H_{n+1}-H_n\in\{0,1\},\qquad
 X_{n+1}=1\ \Longrightarrow\ H_{n+1}-H_n=1.                  \tag{10}
\]
Non-full births may also increase height; full births are a sufficient
witness, not an exhaustive characterization of all height increments.

For a fixed starting size \(n_0\ge6\) and \(m\ge0\), put
\[
 C_m=\sum_{j=1}^mX_{n_0+j},\qquad N=n_0+m.
\]
An initial longest chain followed by all subsequent full-birth
vertices is a chain. Equivalently, summing (10) gives the pathwise bounds
\[
            H_{n_0}+C_m\le H_N\le H_{n_0}+m\le N .           \tag{11}
\]
For \(m=0\), \(C_0=0\) and no concentration formula with division
by \(m\) is used.

A full-birth vertex need not be comparable to every **future** vertex:
a later empty birth is incomparable with all existing vertices.
Thus this proof does not call full-birth vertices permanent posts
or assume a property of their future.

Natural labels index births and define the filtration; they do not
define chain height. \(H_N\) depends only on the induced partial order,
is invariant under order isomorphism, and ignores all marks.
The auxiliary count \(C_m\) uses the realized history. No reconstruction
of that count from a final unlabelled order is claimed.
If height were counted in edges instead of vertices, the nonempty
finite height would differ by one; the asymptotic conclusions would
be unchanged, but (11) uses the vertex convention throughout.

## 5. A conditional-history concentration lemma, proved here

**Lemma.** Let \(Y_j\in\{0,1\}\) be adapted to a filtration
\((\mathcal G_j)\), and assume
\[
 E[Y_j\mid\mathcal G_{j-1}]\ge\gamma
 \quad\text{almost surely},\qquad 0<\gamma\le1,
\]
for every \(j\). For \(S_m=\sum_{j=1}^mY_j\), \(m\ge1\), \(x\ge0\),
\[
 P(S_m\le\gamma m-x\mid\mathcal G_0)
                  \le \exp(-2x^2/m)\quad\text{almost surely}. \tag{12}
\]
No independence, stationary law or Markov assumption is required.

**Proof.** For \(t\ge0\), writing
\(p_j=E[Y_j\mid\mathcal G_{j-1}]\),
\[
 E[e^{-tY_j}\mid\mathcal G_{j-1}]
  =1-p_j+p_je^{-t}
  \le1-\gamma+\gamma e^{-t}.                                \tag{13}
\]
The inequality has this direction because \(e^{-t}-1\le0\).
Since \(S_{j-1}\) is measurable with respect to \(\mathcal G_{j-1}\),
successive conditional expectation gives
\[
 E[e^{-tS_m}\mid\mathcal G_0]
                    \le(1-\gamma+\gamma e^{-t})^m.           \tag{14}
\]
This product is a bound obtained by conditioning, not a factorization
claim for the dependent \(Y_j\)'s.

For an auxiliary single Bernoulli variable \(Z\) of mean \(\gamma\),
define the elementary function
\[
 f(s)=\log E[e^{s(Z-\gamma)}]
     =\log(1-\gamma+\gamma e^s)-\gamma s.
\]
It has \(f(0)=f'(0)=0\). For \(0<\gamma<1\), its second derivative
is \(w_s(1-w_s)\le1/4\), where
\(w_s=\gamma e^s/(1-\gamma+\gamma e^s)\in(0,1)\).
For \(\gamma=1\), \(f\) is identically zero.
For any real \(s\), integration yields
\[
 f(s)=s^2\int_0^1(1-v)f''(vs)\,dv\le s^2/8 .
\]
Applying this at \(s=-t\) in (14) proves
\[
 E[e^{-t(S_m-\gamma m)}\mid\mathcal G_0]\le e^{mt^2/8}.
\]
For \(x>0\), conditional Markov bounds the event
\(S_m-\gamma m\le-x\) by \(\exp(-tx+mt^2/8)\).
Take \(t=4x/m\) to obtain (12).
For \(x=0\), the trivial probability bound one suffices.
Thresholds may be real; an impossible negative count event simply has
probability zero. All exponential moments exist because the variables
are bounded. \(\square\)

The auxiliary Bernoulli variable in this scalar-function proof is
not a claim that the history is iid, a sampled comparison process,
or an executed random construction.

## 6. Finite-time consequences for the selected native history

Apply the lemma to \(Y_j=X_{n_0+j}\),
\(\mathcal G_j=\mathcal F_{n_0+j}\), and \(\gamma=1/2\).
Equation (9) verifies its conditional-mean hypothesis on every
marked history. It gives the first estimate in (2).
By (11),
\[
 \{H_N\le H_{n_0}+m/2-x\}\subseteq\{C_m\le m/2-x\},
\]
which proves the second.

For \(0<\varepsilon<1/2\), this includes
\[
 P\!\left(H_N\le H_{n_0}+(1/2-\varepsilon)m
                       \mid\mathcal F_{n_0}\right)
                    \le e^{-2\varepsilon^2m}.               \tag{15}
\]
Equivalently, for a declared \(0<\delta<1\), with conditional probability
at least \(1-\delta\),
\[
 H_N\ge H_{n_0}+\frac m2
                  -\sqrt{\frac m2\log(1/\delta)} .           \tag{16}
\]
These are symbolic finite-time bounds under the native history measure,
not observed frequencies or a proposed physical test.

Linearity and the tower property also give the expectation bound
\[
 E[H_N\mid\mathcal F_{n_0}]
 \ge H_{n_0}+E[C_m\mid\mathcal F_{n_0}]
 \ge H_{n_0}+\frac m2+\sum_{n=n_0}^{N-1}a_n .               \tag{17}
\]
The \(a_n\) are fixed by the law's complete layers, not fitted from
the observed history. No value or asymptotic average of them is evaluated.

The finite prefix is handled exactly by \(n_0=6\), not by assuming
the half-scale rule at earlier births. Any fixed later starting
history works as well. Random marks in the first six births are
already included in \(\mathcal F_6\), so averaging introduces no
independence assumption.

There is no deterministic guarantee on **every** finite history.
For example, after any fixed prefix, a finite sequence of empty
births has positive probability under the complete positive model.
It appends isolated vertices and leaves the old nonempty height
unchanged. Such exceptional finite histories do not contradict
the exponentially small lower-tail bound or the almost-sure result.
No positive probability is claimed for an infinite all-empty history.

## 7. Almost-sure linear height and its precise exponent

Fix \(0<\varepsilon<1/2\), and let
\(E_m=\{C_m\le(1/2-\varepsilon)m\}\).
Integrating (12) over the initial history gives
\[
 P(E_m)\le e^{-2\varepsilon^2m},\qquad
 \sum_{m\ge1}P(E_m)<\infty .
\]
For every integer \(K\),
\[
 P\!\left(\bigcup_{m\ge K}E_m\right)
 \le\sum_{m\ge K}e^{-2\varepsilon^2m}\longrightarrow0
 \quad(K\to\infty).
\]
The event that \(E_m\) occurs infinitely often is contained in every
such union, so it has probability zero. This elementary summable-tail
argument uses no independence between the events.

Intersect the resulting probability-one events over a countable
sequence of positive rational \(\varepsilon\) tending to zero.
Then
\[
                  \liminf_{m\to\infty}C_m/m\ge1/2
                  \quad\text{almost surely}.               \tag{18}
\]
For fixed finite \(n_0\), \(m/N\to1\) and \(H_{n_0}/N\to0\).
Equation (11) therefore proves (1).
The same argument, with \(1/2\) replaced by \(\gamma\), gives
\(\liminf H_N/N\ge\gamma\) whenever a growing-order law has the
lemma's uniform conditional full-birth floor from a fixed size onward.

On the probability-one event in (1), eventually
\[
                            N/4\le H_N\le N .
\]
Thus, for \(N>1\) sufficiently large,
\[
 1+\frac{\log(1/4)}{\log N}
            \le\frac{\log H_N}{\log N}\le1,
\]
and squeezing proves (3).
In this precise sense \(H_N=\Theta(N)\) almost surely; the onset
of the eventual bound may depend on the realized history.
The variable \(N\) is event cardinality. Calling (3) a
height-volume exponent uses “volume” only to mean that cardinality.

Pointwise strictness in (8) does not establish a fixed surplus
\(\gamma>1/2\) valid at all sizes. Neither a positive limiting
average of the \(a_n\), nor convergence of \(H_N/N\), is proved.
The assertion is a liminf lower bound and exponent, not an exact
linear coefficient. No subleading scaling law or width/shape
asymptotic follows from this proof.

## 8. What is prescribed, and what arbitrary positive scales do not force

The load-bearing fact is an **absolute probability prescription**:
(6) leaves more than half of every complete row for the full birth.
Positivity and normalization alone say only that its full complement
is positive. The inherited ratio identities determine compatible
proper-slot ratios, not this particular absolute allocation.

This distinction can be made exact at a single next layer.
Fix any admitted lower prefix and its potentials in convention (5).
For nonempty parent size \(n\), \(0<M_n<\infty\).
For any \(0<\epsilon<1\), choose a common component coefficient
\[
                \alpha=\frac{1-\epsilon}{M_n}
\]
on this last layer, and take **complete** full complements.
All proper slots are positive, and every full probability is
\[
        1-\alpha T_{P,r}\ge\epsilon ,
\]
with equality at a maximizing row. The admitted ratio-potential
characterization preserves the inherited proper-slot ratio equations
under that common coefficient. In every diamond internal to this
extended prefix, the second precursor is proper in its intermediate
parent; its two route factors have the same permitted common scaling.
Locality and equivariance are retained.

Thus arbitrarily small full probability at a complete last-layer row
is compatible with the declared principles. There is no universal
positive full-birth floor over **all** such law prescriptions, and
in particular those principles do not force the selected \(>1/2\)
inequality. This argument does not alter the baseline used in §§2–7.

Later layers of that alternative would have to be rebuilt from its
changed prefix. [LAW_DEPENDENCE](LAW_DEPENDENCE.md), §§2–4, explicitly warns that retaining
the old later layers—or naively applying proper-only scalings across
them—can fail a mixed full/proper diamond.
No such invalid extension is used here.

The finite-layer observation is **not** a proof of an infinite
alternative with sublinear height. Nor does it rule out linear height
by other mechanisms, including height increases at non-full births.
It shows exactly why the present sufficient-floor argument is
law-dependent. We do not infer a universal height no-go from the
absence of this particular floor.

A coordinate gauge is different. Replacing a component potential by
\(u'_{\mathcal C}=t_{\mathcal C}u_{\mathcal C}\) and its coefficient
by \(\alpha'_{\mathcal C}=\alpha_{\mathcal C}/t_{\mathcal C}\)
leaves all products, complete complements and path probabilities
unchanged. Merely transporting labels also leaves intrinsic height
unchanged. In contrast, changing actual proper-slot allocation while
recomputing its full complement changes the stochastic law.
The common half-scale rule must therefore be identified in its
specified potential convention; it is not a gauge-free consequence
of the ratio equations.

The source package also contains a prescribed expected-defect optimizer
with strict restoration. Its coefficients are not the all-layer
common half-scale coefficients used here. The present proof neither
settles that optimizer's unproved Cesaro/defect claims nor transfers
the height conclusion to it.
Likewise a finite harmonic extension does not acquire an infinite
history satisfying (8) merely because it was admissible for one
additional layer.

## 9. Mathematical observation and interpretation limits

Height is an intrinsic order observable: exact knowledge of the
finite unlabelled order suffices to define its longest-chain
cardinality, without marks, external coordinates or a birth clock.
This is a mathematical observation channel. No physical procedure
for recovering the complete order, handling missed records or
calibrating a readout is supplied.

The proof exploits one committed vertex per bookkeeping step, as
declared in the model. It does not identify that step with physical
time or claim that all present relational activity produces a record.

No dimension or geometry follows from the single exponent (3).
In particular there is no lower-dimensional spacetime interpretation,
Poisson or Minkowski comparison, metric reconstruction, manifoldlike
limit, Lorentzian correspondence, physical clock or geometry bridge
in this packet. Nor is there informative QM, mass/gravity, empirical
correspondence or validation of DET or its ontology.
The growing order remains a selected conditional mathematical model.

No \(\Xi\) or canonical coefficient branch is selected or required.
No further coefficient reduction, finite harmonic gate, benchmark or
physical experiment is opened.
The completed yield is a theorem: the admitted all-layer half-scale
baseline has the conditional full-birth floor, finite-time tails,
almost-sure linear height and precise cardinality exponent above.

## Public premises and evidence scope

The public exposition dependencies and their original load-bearing uses are:

| Snapshot | Load-bearing use |
| --- | --- |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md), §§1, 9 | Birth/mark/payload definitions, full complements, fixed-potential half-scale at all \(n\ge6\), admitted infinite classical history measure |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md), §§2, 4, 6–8 | Law-choice versus coordinate gauge, complete last-layer changes, mixed-diamond boundary and inherited evidence limits |

The source-author's correspondence checks concerned authorized public
exposition snapshots. These links identify mathematical premises, not
reconstruction of historical certificate or custody identity. Separate
current reads and hashes are not atomic identity certificates. No original
archive, coefficient manifest or protected input is supplied or followed
by these public links.

The following source evidence boundary is retained exactly:

The accepted prefix and ratio-potential theorem remain admitted.
Historical missing execution/custody records, failed source/receipt
checks and provisional corrections recorded by the source package
are not erased or repaired by present-byte matches.
The manual challenges are supplied-context reviews, not independent
source-custody audits or coordinator adjudication.

For construction of the source manuscript, the retained statement is:

All mathematical work is manual and bounded to the proof above.

That statement and the supplied-context challenges describe source-author
construction. Later independent review and its separate checks are recorded
separately. This derivative does not claim a machine proof, an executable
custody audit or scientific acceptance by its preparer.

The result remains conditional on the admitted finite prefix,
ratio-potential construction and infinite classical history measure under
the specified optional whole-layer half-scale law at every later parent
size. The law changes actual probabilities; it is not a coordinate gauge.
The theorem concerns intrinsic longest-chain height in one growing history,
without assuming independent or identically distributed births. The classical
kernel is declared separately from the PSD payload; zero payload does not
provide a trace-normalized probability.

No exact limiting speed, size-uniform surplus over the stated floor,
canonical coefficient branch, spacetime dimension, physical clock or
empirical validation is supplied. No height conclusion is transferred to
the distinct optimization recursion or to an unproved infinite harmonic
extension. The last-layer alternative does not establish an infinite
sublinear-height counterexample.

Private review identifiers, external paths, hashes, source-capture files,
tool receipts and account/reset metadata are withheld; the exact original
evidence and correspondence remain separate. No coefficient computation,
native numerical probability evaluation, sampler, benchmark, dataset,
calibration, experiment or physical readout is reported or authorized by
this derivative. Frozen protocols and protected validation inputs remain
unchanged. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the public publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public/private boundary.
