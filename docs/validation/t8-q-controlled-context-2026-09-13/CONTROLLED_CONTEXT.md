# Controlled record-context transitions and constructive future tests

13 September 2026. **CONDITIONAL_CONTROLLED_MODEL; CONSTRUCTIVE_EQUIVALENCE_THEOREM.**

This closes a bounded mathematical version of P1 in the
[independent review](../../../indep%20ndent_review.md) and instantiates its
P2/O1 proposal. Two explicitly chosen preparation domains admit lawful,
informative, residual-preserving transitions. A finite exact procedure returns
a distinguishing future experiment whenever the declared residual predictions
differ. Neither the domains nor their apparatus interactions are derived
from DET. The model is classically representable, despite off-diagonal
pair-kernel entries; it does **not** select quantum mechanics.

The source is [model.py](model.py), with independent exact checks in
[check.py](check.py). These are isolated research sources, not supported core
or RET interfaces. This is not a QR-05 gate, a geometry construction, or an
empirical experiment.

## 1. Obligation and premise ledger

The [preceding result](../t8-q-record-context-domain-2026-09-13/CONTEXT_DOMAIN.md)
constructed the exact-recordability cone \(K_P\) for a supplied partition.
Its four-atom example shows that initial membership in both \(K_P\) and \(K_Q\)
does not license a \(Q\)-read after a selective \(P\)-cut. That counterexample
stands. Here an explicit active interaction supplies a new, narrower
conditional transition; an illegal direct read is not repaired by
renormalization.

| Ingredient | Status here |
| --- | --- |
| Immutable committed history; possibility kernel with total-entry mass; exact recordability of the declared partition | Retained mathematical semantics, not a fresh physical validation |
| Two four-dimensional simplicial preparation cones below; all their normalized mixtures available in this model | Additional selected-domain premise; not all of \(K_P\) or \(K_Q\) |
| Read, switch and \(Q\)-only attempt, with the specified residual maps | Additional apparatus/control law; not inferred from recordability |
| Whole-current-history precursor on every commitment | Chosen serial append rule, not a native spacetime generator |
| Finite prescribed interaction boundaries at which append/no-append can be distinguished | Declared observation interface; not a physical clock or a committed null |
| Minimal product cone and local operations in section 5 | Additional composition convention; not arbitrary quantum ancillas |
| Physical preparation, control, formation and access availability | Open; no experimental realization asserted |

The frozen QR-MAP architecture is retained. This is one controlled model
inside it, not a uniquely forced \(F\), \(L\), Hilbert space, amplitude law,
or field choice. No threshold or existing acceptance criterion is changed.
The algebra below holds over real coordinates; the executable implements
its exact rational fragment and rejects floating-point inputs.

## 2. Selected domains, retaining pair-kernel information

Let \(c\in\{P,Q\}\) be the explicit apparatus mode, with partitions
\(P=\{01\mid23\}\) and \(Q=\{02\mid13\}\). Coordinates are unnormalized
columns \(x=(x_{00},x_{01},x_{10},x_{11})^T\ge0\), with
\(u(x)=\sum_{r,s}x_{rs}\). Use two real pair-kernel blocks

\[
a=\begin{pmatrix}1/3&1/6\\1/6&1/3\end{pmatrix},
\qquad
b=\begin{pmatrix}1&-1/2\\-1/2&1\end{pmatrix}.
\]

Each is positive definite and has total-entry mass one. Their eigenvalues
are \(1/2,1/6\) and \(3/2,1/2\), respectively. Write \(g^c_{r0}\) for
\(a\) embedded in cell \(r\) of \(c\), and \(g^c_{r1}\) for \(b\) similarly.
Define

\[
\iota_c(x)=\sum_{r,s}x_{rs}g^c_{rs},\qquad
\widehat K_c=\iota_c(\mathbb R_+^4)\subset K_c.
\]

Different cells have zero cross-kernel entries. Within cell \(r\) the equal
diagonal and off-diagonal entries are

\[
t_r=x_{r0}/3+x_{r1},\qquad h_r=x_{r0}/6-x_{r1}/2.
\]

The inverse on the image is
\(x_{r0}=3t_r/2+3h_r,\ x_{r1}=t_r/2-h_r\). Hence the four
generators are linearly independent, the embedding is injective, the image
cone is closed, convex, pointed and generating in its four-dimensional
linear span, and

\[
m(\iota_c(x))=\mathbf1^T\iota_c(x)\mathbf1
             =u(x),\qquad
\mu_r=x_{r0}+x_{r1}.
\]

The normalized base is a simplex, therefore compact. Its mass is strictly
positive on every nonzero positive element. There are no nonzero zero-mass
elements **in these selected cones**. This is not a repair of the unrestricted
cone, where that property fails.

The older coherence witness \(d(\pm1/8)\) belongs to \(\widehat K_P\):
its coordinates are \((3/4,0,0,1/4)\) and \((0,1/4,3/4,0)\).
Conversely, the normalized \(P\)-recordable positive block
\(\begin{psmallmatrix}1/4&1/4\\1/4&1/4\end{psmallmatrix}\), with a zero
second block, is excluded: its inverse coordinates include \(-1/8\).
The restriction is genuine and must not be hidden.

Off-diagonal pair-kernel entries remain in the state and affect its allowed
predictions. Nevertheless this cone is isomorphic to a classical four-state
cone. Off-diagonal entries alone are not a certificate of nonclassical
operational behavior.

## 3. Complete controlled transition law

Matrices act on unnormalized coordinate columns. Given a normalized input,
a branch \(T\) has probability \(p=u(Tx)\) and, only if \(p>0\), conditional
residual \(Tx/p\) in its target mode. Zero branches have probability zero
and no selected conditional state or event. They remain in the complete
test; an attempt to condition on one is refused.

**Read, in either mode.** The two committing branches are

\[
(R_r x)_{ts}=\delta_{tr}x_{ts},\qquad r=0,1.
\]

They stay in the same mode. In pair-kernel coordinates these are precisely
the cell cuts \(E_r\iota_c(x)E_r\). Their masses sum to \(u(x)\);
repeating the same read gives the same result with probability one.

**Switch, in either mode.** The single branch is silent and deterministic:
it changes the mode to the other mode and applies the involution

\[
(r,s)\longmapsto(r\mathbin{\mathrm{xor}}s,s),\qquad
S(x_{00},x_{01},x_{10},x_{11})^T
 =(x_{00},x_{11},x_{10},x_{01})^T.
\]

In kernel notation it is
\(\iota_{\bar c} S\iota_c^{-1}\), only on the specified image cone.
It is positive there, mass-preserving and involutive across the two types.
It is **not** merely a passive renaming of atoms: passive transport of the
embedding would leave \(x\) unchanged. This interaction changes the cell
carrying the shape-\(1\) contribution, so later recorded predictions can change.

The selected switch has **no positive linear extension to all \(K_P\)**
that agrees on the selected cone. For example, the normalized positive
\(P\)-recordable kernel consisting of
\(\begin{psmallmatrix}1&-1\\-1&1\end{psmallmatrix}\) in cell 0 and \(a\)
in cell 1 has span coordinates \((-3/2,3/2,1,0)\). Agreement on the
four linearly independent generators forces any linear extension to send
these to \((-3/2,0,1,3/2)\). Its first \(Q\)-block is \(-3a/2\),
which is not positive semidefinite. Thus the domain restriction is
load-bearing, not an unverified claim of global positivity.

**Attempt, only in mode \(Q\).** There are three branches:

\[
N=\operatorname{diag}(1/2,1,1/2,1),\quad
B_0=\operatorname{diag}(1/2,0,0,0),\quad
B_1=\operatorname{diag}(0,0,1/2,0).
\]

\(N\) is silent; \(B_0,B_1\) commit their respective outcomes. All stay in
\(Q\), and \(uN+uB_0+uB_1=u\). Attempt in \(P\) is unavailable,
not a zero-probability experiment. “Bright” \(s=0\) and “dark” \(s=1\)
are names for this selected attempt law, not claims about photons or detectors.

**Closure proposition.** Every legal branch maps its source cone into its
declared target cone. Every action is complete. Every finite typed sequence
therefore defines a normalized controlled outcome tree with legitimate
positive-branch conditioning.

**Proof.** Coordinate matrices have nonnegative entries and the stated
column-mass sums. The embeddings are cone isomorphisms onto the selected
domains. A general positive input is a nonnegative linear combination of
the four generators, so their target membership and mass identities extend
by linearity and positivity. Induction over the sequence gives normalization;
division by a positive branch mass stays on the normalized base. No change
of cone without a registered map is permitted. ∎

### Commitment, precursor and choice of action

The state is \((C,c,x)\). In the executable candidate \(C\) is an immutable
chain of records with contiguous event IDs. A commit appends one fresh event,
with the **entire current history** as its precursor ideal, recording source
mode, action and outcome. Past labels and relations remain identical.
Silent branches, including switches and failed attempts, leave the same
history tuple unchanged. The residual and current mode remain in the state,
not discarded in favor of the history.

The branch law is controlled: the commanded action is an explicit argument.
To obtain a complete action-and-outcome kernel \(L^\pi\), additionally supply
a fixed normalized policy \(\pi(a\mid C,c)\) supported on available actions.
Set

\[
L^\pi(a,o\mid C,c,x)=\pi(a\mid C,c)\,u(T^c_{a,o}x).
\]

The policy cannot inspect an undeclared residual oracle. The precursor rule
is a deterministic, hence degenerate-kernel, choice. Outcome probabilities
and the conditional transition \(F_{a,o}\) are then fully specified. Prescribed
controls are an explicit experimental interface; a finite program can carry
its own declared instruction state. The executable does exact branch
enumeration/conditioning, not random sampling or a physical scheduler.
It does not select a unique autonomous policy, validate an arbitrary
purported initial history as reachable, or derive the chain rule from DET.
The built-in apparatus maps do not implement a nontrivial rule selecting
contexts from records. Record-conditioned policies remain a supplied choice.
This serial growth choice is not a proposed manifold-producing law.
The source's append_record helper checks only append structure; its caller
must already have selected a positive-probability branch. It has no residual
and cannot check that premise itself. The state-aware apply_branch transition
enforces positivity before invoking the helper.

## 4. Observation interface and a constructive equivalence theorem

A **test word** specifies a legal sequence of actions and branch outcomes.
Its probability is \(uT_k\cdots T_1x\). An epsilon symbol denotes absence
of an append at a prescribed finite protocol boundary, not a stored null
event. This boundary/formation-access interface is an additional premise.
Interaction count supplies mathematical composition order, not duration or
a universal physical clock.

This is a procedure-indexed test family. In general it is richer than a view
retaining only an unindexed final committed history and forgetting how it
was obtained. Tests in this section compare states at the **same** mode and
committed prefix. Different prefixes are not silently identified.

**Typed future-effect theorem.** For finitely many state types with finite
dimensional real vector spaces, finitely many registered linear branch maps
belonging to complete legal tests, finitely many declared terminal effects
that are outcomes of available terminal tests, and lawful type transitions,
define \(W_c\) by
starting with the terminal effects at type \(c\) and repeatedly adjoining
pullbacks \(fT\), for every \(T:c\to d\) and \(f\in W_d\).
The process stabilizes after finitely many independent additions.
Two states of the same type agree on every declared finite word followed
by a declared terminal observation exactly when their difference annihilates
the final \(W_c\).
With rational maps, terminal effects and compared states, the construction is
an executable exact decision procedure. Store a legal suffix word and
terminal observation with each added basis effect; a failed equivalence
comparison returns a lawful test and its unequal probabilities.
The candidate implemented here has only
the terminal mass effect, so its stored witness is just the branch word.
The source implements this particular two-mode catalogue, not a generic
arbitrary-dimension process-equivalence library.
This instantiates review O1; it is not a novelty claim for finite-dimensional
linear-process effect closure.

**Proof.** Each added independent row increases a finite dimension. After a
full sweep with no addition, every registered pullback preserves the relevant
spaces. Induction on word length puts every word effect in the final span.
Conversely each stored basis row is the effect of its stored legal word
followed by the corresponding terminal observation:
prepending a branch to a target-type witness constructs its source-type
pullback. Annihilating the basis is therefore sufficient and necessary for
equality of every word probability. If it fails, one basis witness separates
the inputs. Off-witness branches may simply stop to make a complete adaptive
test. Exact rational elimination decides independence without a numerical
tolerance. ∎

Here the initial effect is \(u=(1,1,1,1)\) at each of two types; there can
be at most eight independent stored rows in total. The checker obtains
dimension four at each type. This can also be proved **without the algorithm**:

\[
\Pr[\operatorname{read}(r),\operatorname{switch},
        \operatorname{read}(r\mathbin{\mathrm{xor}}s)\mid c,x]=x_{rs}.
\]

The first read retains cell \(r\), the switch routes its two shapes to
different cells, and the last read selects shape \(s\). These four lawful
word effects are the coordinate functionals. Moreover this is one fixed
read–switch–read program with **two committed outcomes**; its joint recorded
law is \(\Pr(r,t)=x_{r,r\mathbin{\mathrm{xor}}t}\). Separation in this
candidate does not depend on measuring the timing of silent attempts.
Both the full cylinder test family and the available committed-record
procedures therefore distinguish all unequal states here. This does not
identify those observation quotients for a general process.

The algorithm demonstrates no nontrivial state compression in this candidate:
linear predictive rank is four, with three independent normalized parameters.
That rank is not a minimum physical Hilbert dimension or a bit-storage bound.

For example \(x=e_{00}\) and \(y=e_{01}\), in mode \(P\) at the same \(C\),
have the same immediate read outcome \(0\). After a silent switch, a \(Q\)-read
returns \(0\) for \(x\) and \(1\) for \(y\). Even the immediate full
read-probability vector is an insufficient summary of future predictions.
The intervening switch need not append a record to change those predictions.

Finite adaptive procedures assembled from this fixed catalogue inherit the
result by summing their branch words; the same declared policy must be used
for both states. Arbitrary history-dependent *new maps*, unrestricted
ancillary experiments, inaccessible outcomes, or changed observation channels
are not covered by this finite interface.

## 5. Mixing and a deliberately limited composite

Mixing is coordinate convex combination; \(\iota_c\) is linear, so this
commutes with kernel mixing and with every unnormalized branch map.
The operational availability of those mixtures is a premise in section 1,
not a consequence of the original DET axiom set.

For a minimal declared composite of types \(c,d\), take \(z_{ij}\ge0\) on
sixteen coordinates and embed it as
\(\sum_{i,j}z_{ij}g_i^c\otimes g_j^d\). Its mass is \(\sum z_{ij}\).
The product record partition is exactly recordable: a cross-cell factor
vanishes in each generator whenever one subsystem's cell differs.
Local maps \(T\otimes I\) and \(I\otimes U\) preserve these selected cones,
normalize each complete local test, and commute on unnormalized states.
The complete outcomes must remain labeled.

This is an explicitly classical composite, including classically correlated
coordinate distributions; it contains no entangled preparations beyond that
chosen cone. It supplies no universal tensor-product postulate, purification,
physical spatial separation or relativistic locality. No append-order
independence of complete global histories is claimed: a joint precursor/merge
policy would be another obligation. The stated composition theorem is about
residual maps and full local outcome probabilities.

## 6. Silent elimination and the quotient boundary

For repeated attempts in \(Q\), the first commitment of outcome \(r\), after
exactly \(n\ge0\) silent attempts, has unnormalized residual
\(B_rN^nx=2^{-(n+1)}x_{r0}e_{r0}\). Therefore

\[
\Pr(n,r)=2^{-(n+1)}x_{r0},\qquad
\Pr(\text{never commits under repeated attempt})=x_{01}+x_{11}.
\]

The first-commit partial map is
\(H_{r,k}=(1-2^{-k})E_{r0}\); its limit is \(H_r=E_{r0}\).
In coordinate \(\ell^1\) operator norm,
\(\|H_r-H_{r,k}\|=2^{-k}\). The silent residual map \(N^k\)
converges to the dark-coordinate projection, **not zero**. Survival after
\(k\) attempts equals
\(2^{-k}(x_{00}+x_{10})+x_{01}+x_{11}\).
The “never” event is a limiting path event, not a finite record or an
observable finite-time diagnosis. A later change of control can reveal or
commit a surviving dark residual; “never” is relative to the repeated-attempt
policy.

This model instantiates the compact-base mechanism proposed in review O2.
For example the entrywise absolute kernel norm satisfies
\(\|\iota_c(x)\|_{\mathrm{entry},1}\le3u(x)\) on the positive cone.
It is not a necessary-and-sufficient characterization for general domains,
and it does not fix the earlier full-cone residual divergence. The general
compact-base theorem remains a separately scoped proof obligation.

For O3, let \(N_c^{\rm pred}\) denote the annihilator of the final future-effect
space, not the silent matrix \(N\). Every registered \(T:c\to d\) obeys
\(T N_c^{\rm pred}\subseteq N_d^{\rm pred}\), since
\(f(Tz)=(fT)z=0\). Thus its linear map descends to the predictive quotient.
Terminal mass also descends. Positive-probability normalized branches then
respect equivalence; zero branches still have no conditional state.

The requirement to include **every allowed continuation** is load-bearing.
Under an attempt-only interface at \(Q\), \(e_{01}\) and \(e_{11}\) both
produce no commits forever. The full interface distinguishes them by an
immediate read. An attempt-only quotient cannot be transported unchanged to
that enlarged experiment family. With the full catalogue here,
\(N_c^{\rm pred}=\{0\}\), so no residual coordinate can be discarded.

## 7. Evidence, result classification and successor

The written arguments prove the claims on the specified cones and complete
catalogue; finite checks catch implementation errors but do not prove physical
availability. Exact arithmetic, immutability/refusal tests, independent
coordinate-word witnesses and a separate proof review are recorded in the
[coordination handoff](../../coordination/QR_HANDOFF.md).

**Yield:** a frozen conditional controlled definition, its closure and
constructive equivalence theorems, and counterexamples to immediate-read
sufficiency, to global positivity of the selected switch, and to reusing an
attempt-only quotient after adding read access. This connects record-context
research to predictive sufficiency without reopening an identifiability atlas.

**Next obligation:** consolidate the compact-base first-commit theorem and
its transition-compatible quotient conditions (P3/O2/O3), with never-commit
mass explicit. In parallel, physical/DET selection of preparation cones and
apparatus transformations remains an unsolved foundational premise question.
This classical candidate does not exclude the earlier countermodels, force
complex QM, or justify promotion of any proposed reconstruction axiom.
No empirical discriminator, native geometry, mass mechanism, Einstein limit,
RET change, clock work, book work or retired \(\kappa\)-gravity is started.
Option B and Status M are unchanged.
