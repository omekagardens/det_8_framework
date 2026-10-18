# RI-76 — fixed-parameter defect decay and a height obstruction

24 September 2026 UTC. **Conditional research proof; independently accepted after coordinator adjudication.**
This note analyzes the specific unadopted RI-75 law, for one fixed rational
\(0<\epsilon\leq1\). It changes no probability row and creates no executor.
Both conclusions below are required: almost-sure normalized defect decay,
and a positive-probability obstruction to sublinear height. The latter
prevents the former from being mistaken for nondegenerate geometry.

## 1. Conditional law, definitions and result

Keep every premise of [RI-75](../native_growth_plancherel_approximation_v1/APPROXIMATION.md):
the exact held actual marked prefix at parent sizes below six, complete
structural marked components, all ideals eligible, precursor-record
locality, equivariance, fair immutable newborn bits and scalar-passive maps
\(\mathcal B_{S,b}(D)=q^\epsilon_{P,r}(S)D/2\).
The Ferrers/Plancherel target is chosen mathematical structure, not dynamics
derived uniquely from DET. The entire residual remains passive.
All rows of this particular candidate are strictly positive.

Let \(P_N\) be the naturally labeled committed order after N births,
and \(\mathscr F_N\) the complete marked-history information at that size.
The already normalized kernels define consistent cylinder probabilities
and their ordinary probability measure on the finitely branching path tree.
All probabilities and expectations below are under this **fixed** law,
written \(\mathbb P_\epsilon,\mathbb E_\epsilon\). Epsilon does not vary with N.

For \(N\geq7\), define the intrinsic family
\[
 \mathcal F=\{K\oplus F:\ |K|=6,\quad F\ne\varnothing
                  \text{ a Ferrers order}\}.
 \tag{1}
\]
The core is the unique six-element ideal, as in
[RI-74, §6](../native_growth_plancherel_graft_v1/PLANCHEREL_GRAFT.md);
it is not chosen by birth labels. Let
\[
 \tau=\inf\{N\geq7:P_N\notin\mathcal F\},\qquad
 A=\{\tau<\infty\}.
 \tag{2}
\]
Use \(\tau=\infty\) if the set is empty. No claim about
\(\mathbb P_\epsilon(A)=1\), or about a positive probability of \(A^c\),
is assumed or concluded.

A **full birth** has precursor equal to the whole parent, so its newborn
is above every existing vertex. A **proper birth** has any other ideal
as its precursor. Define height \(H(P)\) as the largest chain cardinality
and width \(W(P)\) as the largest antichain cardinality. Write
\[
 \delta(P)=\min\{|B|:P[V(P)\setminus B]\text{ is Ferrers}\}.
 \tag{3}
\]
This is arbitrary-vertex deletion, not only ideal or maximal deletion.
The empty order, every singleton and every chain are Ferrers.
For every nonempty N-vertex order, \(0\leq\delta(P)\leq N-1\).
Normalized quantities are considered only for \(N\geq1\).

**Theorem, for this fixed RI-75 candidate.**

1. There is an almost-surely finite random bound on \(\delta(P_N)\) for all N.
   Consequently \(\delta(P_N)/N\to0\) almost surely and in every
   \(L^p,\ 1\leq p<\infty\).
2. With probability at least \(\alpha_\epsilon=\epsilon c>0\),
   where c is a fixed prefix-dependent rational number in \((0,1/98)\),
   the order develops a permanent full-birth tail. On A,
   \(H(P_N)/N\to1\) and \(W(P_N)/N\to0\) almost surely.
   In particular height divided by N does not tend to zero in probability
   or almost surely.
3. The defect convergence is not \(L^\infty\) convergence:
   \[
    \left\|\delta(P_N)/N\right\|_\infty=1-\frac1N .
    \tag{4}
   \]
   No finite, size-independent deterministic defect bound, integrable random
   bound or quantitative size-decay rate is supplied.

The proof is source-specific. It uses RI-75's off-family row formula and
RI-74's structural no-return property, not finite-cylinder continuity as
epsilon tends to zero.

## 2. Structural exit is irreversible

Suppose P has size n≥7 and is outside \(\mathcal F\). If any eligible birth
gave a family child \(Q=K\oplus Z\), that child's suffix would have
\(|Z|=n+1-6\geq2\). The newborn x is maximal in Q. All maximal vertices
of a family order belong to its suffix, so x lies in Z.

Deleting x leaves \(K\oplus(Z-x)\). Under any diagram isomorphism,
Z−x is the Ferrers ideal obtained by deleting a maximal cell; it is
nonempty because \(|Z|\geq2\). Thus the parent P would belong to
\(\mathcal F\), a contradiction.

Therefore **every** child of an off-family parent of size at least seven
is off-family. This uses only the order construction, not a support
restriction or a zero transition weight. It applies equally to proper
and full births under the strictly positive approximant. On A,
\(P_N\notin\mathcal F\) for all \(N\geq\tau\).

## 3. Only finitely many proper births after exit

Recall the exact RI-75 proper-row formula at n≥6:
\[
 q_i^\epsilon=\lambda_n h_i^\epsilon+\sigma_n u_i^\epsilon,\qquad
 h_i^\epsilon=a_c^0u_i^\epsilon,\qquad
 \sigma_n=\frac{t_n}{2(1+M_n^\epsilon)},\qquad
 t_n=\frac{\epsilon}{(n+1)^2}.
 \tag{5}
\]
Here \(u_i^\epsilon>0\) is the RI-38 maximal-deletion potential,
\(M_n^\epsilon\) is the maximum complete marked proper-row sum of u,
and \(a_c^0=0\) on inactive components. The symbol \(\sigma_n\) is exactly
RI-75's floor coefficient \(\tau_n\); it is renamed here solely to avoid
confusion with the exit time \(\tau\). Nothing is reselected.

For an off-family parent with n≥7, no proper terminal can be active:
an active terminal would be a family child, contrary to §2. Thus h=0
on its **entire** proper row, for every marking, and
\[
 \mathbb P_\epsilon(\text{birth }n+1\text{ proper}\mid\mathscr F_n)
   =\sigma_n\sum_{S\subsetneq P_n}u_{P_n,r_n}^\epsilon(S)
   \leq\frac{t_nM_n^\epsilon}{2(1+M_n^\epsilon)}
   <\frac{\epsilon}{2(n+1)^2}
 \quad\text{when }P_n\notin\mathcal F.
 \tag{6}
\]
Each sum includes individual labeled ideals. The probability sums over both
newborn marks, so their two factors of \(1/2\) add to one; no extra factor
of two is inserted into (6).

For n≥7 let
\[
 A_n=\{P_n\notin\mathcal F,\ \text{birth }n+1\text{ proper}\},\qquad
 C=\sum_{n=7}^{\infty}\mathbf1_{A_n}.
 \tag{7}
\]
The exit-causing birth is not counted in C: its parent was still inside the
family, or had size six. All later proper births are counted because
exit is irreversible. Inside the family the conditional probability of
\(A_n\) is zero; outside it (6) applies. Taking expectations gives
\[
 \mathbb P_\epsilon(A_n)\leq\frac{\epsilon}{2(n+1)^2}.
\]
Finite partial sums therefore have uniformly bounded expectations.
Increasing those nonnegative partial sums gives
\[
 \mathbb E_\epsilon C
   =\sum_{n=7}^{\infty}\mathbb P_\epsilon(A_n)
   \leq\frac{\epsilon}{2}\sum_{m=8}^{\infty}\frac1{m^2}
   <\frac{\epsilon}{14}.
 \tag{8}
\]
The strict numerical inequality follows by comparing each \(m^{-2}\)
with the integral of \(x^{-2}\) on \([m-1,m]\), whose sum is \(1/7\).
The interchange is only increasing nonnegative sums, not a conditional
independence or stationarity assumption.

For an explicit almost-sure argument, the union bound gives
\[
 \mathbb P_\epsilon\!\left(\bigcup_{n\geq m}A_n\right)
 \leq\frac{\epsilon}{2}\sum_{n\geq m}(n+1)^{-2}\longrightarrow0.
\]
The event of infinitely many \(A_n\) is the decreasing intersection of
these unions. It has probability zero, so C is finite almost surely.
Equivalently, partial-count Markov bounds give
\(\mathbb P_\epsilon(C\geq j)\leq\epsilon/(14j)\).
Neither argument needs independence, an integrable exit time,
or control of the total probability of leaving the family.

## 4. Pathwise defect bound and finite-\(L^p\) convergence

On \(A^c\), every size-N order with N≥7 is in \(\mathcal F\).
Deleting its six core vertices leaves a Ferrers suffix, so
\(\delta(P_N)\leq6\); sizes below seven satisfy that bound trivially.

On A, fix a path with C finite. For any \(N\geq\tau\), delete the entire
exit-state prefix of \(\tau\) vertices and every later proper-birth vertex
present by N. Let \(C_N=\sum_{n=7}^{N-1}\mathbf1_{A_n}\leq C\).
Every retained vertex was born at a full birth after exit, and therefore
lies above every earlier retained vertex. The remaining induced order
is a chain, possibly empty. Hence
\[
 \delta(P_N)\leq\tau+C_N\leq\tau+C \quad(N\geq\tau).
 \tag{9}
\]
Before exit, the family bound applies for N≥7; for N≤6 use
\(\delta(P_N)\leq N-1\). Since \(\tau\geq7\), define
\[
 R=\begin{cases}
  6,&A^c,\\
  \tau+C,&A.
 \end{cases}
 \tag{10}
\]
On the probability-one event C<∞, R is finite and
\(\delta(P_N)\leq R\) for **every** N≥1. This proves
\(\delta(P_N)/N\to0\) almost surely.

For completeness, the finite-\(L^p\) argument does not require
\(\mathbb E R<\infty\). Set \(Y_N=\delta(P_N)/N\), so \(0\leq Y_N\leq1\).
For \(a>0\) and \(1\leq p<\infty\),
\[
 \mathbb E_\epsilon Y_N^p
 \leq a^p+\mathbb P_\epsilon(Y_N>a)
 \leq a^p+\mathbb P_\epsilon(R>aN).
 \tag{11}
\]
Since R is finite almost surely, the last probability tends to zero.
Taking a limsup and then \(a\downarrow0\) proves \(L^p\) convergence.

No estimate on \(\mathbb E_\epsilon[\tau\mid A]\), on
\(\mathbb E_\epsilon[R]\), or on the tail of the finite exit time is used
or supplied. Equation (8) controls C, not the exit-prefix size.
In particular (9) is not a uniform numerical rate in N.

## 5. Exit produces an eventually linear-height branch

On A with C finite, define T to be the **child size** of the last proper
birth after exit; if there is none, set \(T=\tau\).
Then T is finite and every birth after size T is full. The whole order
need not be a chain: it is the finite order \(P_T\) followed by a chain
of new universal tops.
T is used only pathwise; it need not be a stopping time, and no optional
stopping argument is used.

Appending one universal top increases height by exactly one and preserves
width for a nonempty parent. By induction, for all N≥T,
\[
 H(P_N)=H(P_T)+N-T,\qquad W(P_N)=W(P_T).
 \tag{12}
\]
Thus, on A almost surely,
\[
 \frac{H(P_N)}{N}\longrightarrow1,\qquad
 \frac{W(P_N)}{N}\longrightarrow0.
 \tag{13}
\]
Nothing here specifies the height or width behavior on \(A^c\).

### The exit event has strictly positive probability

At parent size six there are no active proper components: a family terminal
would be \(K\oplus1\), with a unique maximum, whereas a proper birth leaves
at least two maxima. To justify the latter, a proper ideal omits at least
one old maximal vertex (an ideal containing all maxima is the whole finite
order). That old maximum and the newborn remain incomparable maxima.

Conversely, a full birth from any size-six parent gives exactly \(K\oplus1\).
Thus the first test of family membership at size seven gives
\[
 \{\tau=7\}=\{\text{birth seven is proper}\}.
 \tag{14}
\]
This is an equivalence of order events, independent of the mark values.

All size-six potentials depend only on the held prefix and hence do not
depend on epsilon. Write them as \(u_{6,P,r}(S)\), and set
\[
 U_6(P,r)=\sum_{S\subsetneq P}u_{6,P,r}(S),\qquad
 M_6=\max_{P,r}U_6(P,r).
\]
These are finite positive rational numbers at every complete marked parent.
Let \(\mu_6\) denote the fixed distribution of the entire marked history
through six births. It too is rational, fixed by the held prefix, and
independent of epsilon. Since h=0 at this layer, (5) gives exactly
\[
 \alpha_\epsilon:=\mathbb P_\epsilon(\tau=7)
   =\frac{\epsilon\,\mathbb E_{\mu_6}U_6}{98(1+M_6)}
   =\epsilon c,\qquad
 c:=\frac{\mathbb E_{\mu_6}U_6}{98(1+M_6)}.
 \tag{15}
\]
Every row has a positive proper slot, including the empty ideal.
Since \(0<U_6\leq M_6<\infty\) on a finite normalized probability table,
\[
 0<c\leq\frac{M_6}{98(1+M_6)}<\frac1{98},\qquad
 0<\alpha_\epsilon<\frac{\epsilon}{98}.
 \tag{16}
\]
This is an exact symbolic identity and inequality; no actual parent-six
inventory or numerical evaluation of c has been performed or is required.
The upper bound is for immediate exit, **not** for eventual exit.
We know only \(\mathbb P_\epsilon(A)\geq\alpha_\epsilon>0\) here.

### Probability and expectation obstruction

For any \(0<\eta<1\), define, on the probability-one finite-C set,
\[
 A^{(\eta)}_m
   =A\cap\{H(P_N)/N>\eta\text{ for every }N\geq m\}.
\]
By (13), these events increase to A up to a null set. For all N≥m,
\(\mathbb P_\epsilon(H(P_N)/N>\eta)\geq
  \mathbb P_\epsilon(A^{(\eta)}_m)\).
Taking the lower limit in N and then increasing m yields
\[
 \liminf_{N\to\infty}
   \mathbb P_\epsilon(H(P_N)/N>\eta)
   \geq\mathbb P_\epsilon(A)\geq\alpha_\epsilon>0.
 \tag{17}
\]
Also
\(\mathbb E_\epsilon[H(P_N)/N]\geq
\eta\,\mathbb P_\epsilon(H(P_N)/N>\eta)\).
Letting \(\eta\uparrow1\) after taking the lower limit gives
\[
 \liminf_{N\to\infty}\mathbb E_\epsilon[H(P_N)/N]
   \geq\mathbb P_\epsilon(A)\geq\alpha_\epsilon>0.
 \tag{18}
\]
These arguments use only eventual pathwise behavior and continuity of
probability for increasing events. Equation (17) rules out
\(H(P_N)/N\to0\) in probability; (13) on the positive-probability event A
also directly rules out almost-sure convergence to zero.
No global height limit or almost-sure exit is claimed.

## 6. Why almost-sure defect decay is not a uniform guarantee

For every fixed N, constructing the N-antichain uses only empty-ideal births.
Every such finite sequence, with any specified record bits, has strictly
positive probability under the held strict prefix and RI-75 strict
continuation. This is a **finite cylinder**, not a claim that an infinite
antichain path has positive probability.

An antichain with at least two vertices has no unique minimum and cannot
be Ferrers. Every induced suborder of an antichain is an antichain, so its
largest Ferrers induced suborder has one vertex. Thus its defect is N−1.
Together with the general singleton upper bound in §1, this proves the
exact essential-supremum equality (4). It tends to one, not zero.

Accordingly there is no finite, size-independent deterministic bound on defect
valid almost surely at every size, and no \(L^\infty\) normalized-defect
convergence. These facts are consistent with the finite random R and all
finite-\(L^p\) convergence:
rare finite histories may require arbitrarily large deletions.
An infinite mean for R is **not** proved; its integrability is simply not
established here.

## 7. Interpretation and limits

This result supplies a fixed-epsilon conclusion not established in RI-75,
but does so by a different proof. RI-75's small proper-transition floor
does not bound total family leakage: a full complement can cause exit.
Here no such bound is needed. After any exit, irreversibility and the
off-family floor make all but finitely many later births full, which is
enough for the defect bound and also creates the height obstruction.

The two outcomes must be reported together:

- For this chosen law, small normalized deletion defect is achieved
  almost surely, even at a fixed positive epsilon.
- That criterion alone is insufficient for nondegenerate geometry:
  with positive probability it is satisfied by a finite irregular
  prefix followed by an indefinitely growing chain of universal tops.

The fixed epsilon result is not obtained by interchanging epsilon and size
limits. The identity \(\alpha_\epsilon=\epsilon c\) does not bound the
probability of eventual exit or provide an epsilon-uniform defect rate.
No claim of positive nonexit probability, balanced Ferrers shape,
dimension, manifold structure, Lorentzian metric, matter/source response
or gravity follows. In particular this is not a native derivation of
Plancherel dynamics, an informative quantum coupling, an empirical
discriminator or a change to metric-as-record Status M or Option B.

No alternative law or selector, adoption decision, new gate or successor
is designed here. Accepted sources, coordinator records, RET, measurement
and git/index remain untouched by this worker.

## 8. Proof review and handoff

This is a one-note proof packet. There is no new executor or machine
certificate, no numerical sampling or optimizer, no bounded illustration
presented as an asymptotic proof, and no actual parent-six enumeration.

Three independent mathematical reviewers read the complete proof draft and
its conditional premises. Each found no blocker in structural no-return,
the all-mark conditional bound, summability without independence, the
all-size random defect bound, finite-\(L^p\) versus \(L^\infty\) distinctions,
the symbolic immediate-exit probability, or the height obstruction.
Their suggested wording clarification is incorporated: the excluded
deterministic defect bound is a **finite size-independent constant**, not
the valid size-dependent bound N−1. The last-proper-birth index is explicitly
pathwise, with no stopping-time assumption.

These are analytical proof reviews, not machine-formalized proofs or
numerical tests of an asymptotic assertion. No Lean verification is claimed.
The only final mechanical checks concern source identity, equation-tag
inventory, local links, whitespace and exactly one EOF newline. Durable
source/review provenance is retained under
`/Volumes/AI_DATA/development/det-review-evidence/ri76-qr/worker-jLxs2C/`.
No repository file outside this single new note was edited by this worker.

**Disposition:** conditional fixed-parameter defect decay **and** a
positive-probability linear-height obstruction for the specific RI-75 law.
Neither conclusion is withheld when evaluating this candidate. This
one-note packet is ready for coordinator adjudication; publication and
any further assignment remain with the coordinator.

## 9. Independent coordinator adjudication

Root and a separate coordinator reviewer read the complete final proof and
found no mathematical or claim-scope blocker. The accepted result pairs the
fixed-parameter almost-sure and finite-Lp normalized-defect limit with the
positive-probability linear-height obstruction. The proof uses the actual
held prefix symbolically; no parent-six enumeration, numerical approximation
to c, asymptotic simulation or formal proof execution was performed.

The worker handoff note was 17418 bytes, SHA-256
`dc4f55af509520714f0ba0e0c29c735ee8fed511538f5f8afe4edabe00c8b3d1`.
Root reopened the four external scope/review records and all four published
RI-74/75 context files against the handoff identities. The comprehensive
handoff manifest is 2880 bytes, SHA-256
`dc963fe5cbc2e3b92a42f3f61b80568bacad2dbce49cf316611cd3429a70f75a`.
This opening-status update and provenance addendum do not change the proof.
The three worker reviews and the independent coordinator review are analytical
reviews; source hygiene and identity checks are separate from mathematical
verification. The source reservation is released to root publication.
