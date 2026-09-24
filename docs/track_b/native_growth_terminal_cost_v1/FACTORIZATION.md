# RI-66 — intrinsic terminal-child costs

24 September 2026 UTC. **Conditional all-size factorization and stress-family
proof; independently accepted after coordinator adjudication.**
The proposed identities hold for the same [RI-59 candidate](../native_growth_expected_defect_v1/EXPECTED_DEFECT.md).
They separate intrinsic terminal-order costs from history/record-dependent
magnitudes. They do not collapse marked components, determine allocations,
or establish the remaining defect-decay condition.

## 1. Definitions and factorization theorem

Fix a free parent size n with the actual strictly positive prefix through
parent size n-1. Keep the complete model of
[RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md): all ideals,
full independent binary record cubes, precursor-record locality, marked-parent
equivariance, one birth, fair newborn bits, and complete scalar-passive maps
`q(S) D/2` on the entire unnormalized payload. No seed, potential normalization,
canonical minimization or mixing constant is changed.

Let j index full marked-parent classes, with actual prefix probability pi_j.
For a proper component c use the fixed positive potentials u and define

\[
 U_c=\sum_j\pi_j\sum_{S:c(j,S)=c}u_j(S)>0,
\]
\[
 R_c=\sum_j\pi_j\sum_{S:c(j,S)=c}u_j(S)
                 [\delta(P_j+x_S)-\delta(P_j)],
\]
\[
 \beta_c=\sum_j\pi_j\sum_{S:c(j,S)=c}u_j(S)
 [\delta(P_j+x_S)-\delta(P_j+\mathrm{top})]. \tag{1}
\]

The final expression equals RI-59's `sum pi*(d_j(S)-f_j)*u_j(S)`; the two
parent-defect terms cancel. A top is a new vertex above every parent vertex,
not a physical coordinate. Every labeled ideal occurrence remains a summand.
Delta is the unchanged arbitrary-vertex Ferrers defect of
[RI-56](../native_growth_ferrers_defect_v1/DEFECT.md).

Every component has a well-defined terminal **unmarked** order Q of size
N=n+1 with at least two maxima. Write e(Q) for the number of linear extensions
on a fixed abstract vertex set, with e(empty)=1. For each maximal v put
`P_v=Q-v` and `P_v^up=P_v+top`. Define

\[
 D(Q)=\sum_{v\in\operatorname{Max}(Q)}e(P_v)
                          [\delta(Q)-\delta(P_v^{\uparrow})],
\]
\[
 H_{\rm num}(Q)=\sum_{v\in\operatorname{Max}(Q)}e(P_v)
                          [\delta(Q)-\delta(P_v)],
 \qquad H(Q)=H_{\rm num}(Q)/e(Q). \tag{2}
\]

**Theorem.** For each proper component c there is a positive constant K_c,
which generally depends on the prefix and its marked component, such that

\[
 \boxed{U_c=K_ce(Q),\quad\beta_c=K_cD(Q),\quad R_c=K_cH_{\rm num}(Q).}
 \tag{3}
\]

Consequently `beta_c/U_c=D(Q)/e(Q)` and `R_c/U_c=H(Q)`. This is an
all-size conditional proof, not an extrapolation from the finite checker.
D(Q) is a diagnostic cost numerator, not the retained quantum payload D.

## 2. Why terminal order is well-defined but does not identify the component

A node is `[P,S,r|S]`, retaining the whole unmarked parent and only precursor
marks. Its possible terminal is `P+x_S`. Isomorphic local nodes have
isomorphic unmarked terminals. Each raw diamond compares two births with
the same unmarked terminal after swapping newborn labels. Therefore all nodes
in a connected component have one terminal type Q. The converse is **not**
assumed: different marked components may share Q and must retain their
separate coordinates and row caps.

Fix an abstract copy of Q and a full mark assignment rho on all N vertices.
For each maximal v form

\[
 i_v(\rho)=[Q-v,\operatorname{past}_Q(v),
                         \rho|_{\operatorname{past}_Q(v)}].
\]

These are proper nodes because another maximal vertex is outside the past.
For distinct maxima v,w, use the old parent `Q-{v,w}` and the two ideals
`past(v),past(w)`. Both newborn marks and every old record are admitted.
The complete diamond directly joins `i_v(rho)` and `i_w(rho)`, including
when the two pasts are equal. Thus all maximal-deletion roles for this
**same full marked terminal** belong to a common component `c_Q(rho)`.

This proves the needed connectivity without assuming that erasing records
makes the entire unmarked Q fiber connected. For a given component c set

\[
 \Omega_c(Q)=\{\rho\in\{0,1\}^{Q}:c_Q(\rho)=c\}. \tag{4}
\]

This nonempty set is invariant under Aut(Q), but need not be the whole cube
or a single marked-isomorphism orbit. A given node may be compatible with
many assignments outside its readable precursor; all such assignments remain
in the sum. They are not silently replaced by one representative. Newborn
and maximal-event marks are not illicitly read to define the local kernel.

## 3. Common weight, fair bits, and automorphism multiplicities

Let W(A,r) be one natural construction's product of ideal probabilities,
without fair-bit factors. Complete inherited diamonds and equivariance make
W independent of the chosen linear extension: adjacent swaps of incomparable
births connect any two such extensions. Actual marked history probability
is `2^(-|A|)W(A,r)`, not W and not a uniform class weight.

For the proof only, RI-38's positive auxiliary terminal weight is

\[
 \Phi(Q,\rho)=
 \prod_{\varnothing\ne T\subseteq\operatorname{Max}(Q)}
 W(Q-T,\rho|_{Q-T})^{(-1)^{|T|+1}}.
 \tag{5}
\]

Every W argument has at most n vertices and is supplied by the fixed prefix.
Pair the deletion factors T and `T union {v}` in this product. Appending v
last in the former gives the known smaller-row factor q; the parent W factors
cancel, leaving precisely RI-38's fixed maximal-deletion potential. Hence

\[
 \Phi(Q,\rho)=W(P_v,\rho|_{P_v})\,
                 u_{P_v,\rho}(\operatorname{past}_Q(v))>0
 \quad\text{for every maximal }v. \tag{6}
\]

This is a comparison weight, not a supplied future law. It retains all
allowed prefix/record dependence. The equality follows on the full scalar
maps, whose two-birth factors are `D/4`, not from a diagonal payload summary.

Expand each pi_j in (1) into its distinct naturally labeled marked histories.
A proper parent history plus a labeled ideal becomes a full terminal history
once a newborn bit is chosen. The correct lift of its contribution is

\[
 2^{-n}W(P_v)u_v
 =\sum_{b=0}^1 2^{-N}\Phi(Q,\rho_b). \tag{7}
\]

The two values agree because the local potential and parent history do not
read the newborn bit. The explicit fair-bit factor is essential. For an
actual selected strict layer the probability of each such terminal history
is `2^(-N) Phi(Q,rho) * tilde_alpha_c`; for an auxiliary boundary it has
coefficient alpha_c instead. We use (7) before allocating either coefficient,
so no division by a possibly zero boundary alpha is made.

Let L(Q) be all linear extensions as ordered lists of the abstract vertices.
Aut(Q) acts simultaneously on pairs `(rho,ell)` in `Omega_c(Q) x L(Q)`.
This action is free: an automorphism fixing an ordered list fixes every
vertex. Its orbits are exactly distinct naturally labeled marked terminal
histories; an identification between two such lists yielding the same
history is the unique corresponding order/mark automorphism. Thus division
by `|Aut(Q)|` is justified on the **pairs**, even when stabilizers of individual
mark assignments vary. No assumption of constant marked automorphism group
or blind multiplication by e(Q) is used.

Define

\[
 K_c=\frac{2^{-N}}{|\operatorname{Aut}(Q)|}
                 \sum_{\rho\in\Omega_c(Q)}\Phi(Q,\rho)>0. \tag{8}
\]

There are e(P_v) extensions ending at v, and `e(Q)=sum_v e(P_v)`. Therefore
for any unmarked, isomorphism-invariant deletion-role statistic g(Q,v),

\[
 \sum_j\pi_j\sum_{S:c}u_j(S)g(Q,\text{newborn})
 =K_c\sum_{v\in\operatorname{Max}(Q)}e(P_v)g(Q,v). \tag{9}
\]

The sum is over all concrete maximal vertices, including isomorphic deletion
roles. There is no additional division by their orbit sizes. Take g equal
to 1, `delta(Q)-delta(P_v^up)`, and `delta(Q)-delta(P_v)` to obtain (3).

Strict positivity of the actual prefix makes K_c and U_c positive. Arbitrary
zero-probability prefixes are not covered by these divisions. Prefix and
mark dependence cancels from the two **ratios**, not from K_c, the row caps,
actual occupation, or the selected alpha values.

## 4. Parent-sector restrictions and the RI-65 residual

For an unmarked parent predicate A insert `1_A(P_v)` into every role sum:

\[
 E_A(Q)=\sum_v e(P_v)\mathbf1_A(P_v),
\quad H_A^{\rm num}(Q)=\sum_v e(P_v)\mathbf1_A(P_v)
                                      [\delta(Q)-\delta(P_v)],
\]
\[
 D_A(Q)=\sum_v e(P_v)\mathbf1_A(P_v)
                                      [\delta(Q)-\delta(P_v^{\uparrow})].
\]

Then the restricted quantities obey

\[
 U_{c,A}=K_cE_A,\quad R_{c,A}=K_cH_A^{\rm num},\quad
 \beta_{c,A}=K_cD_A. \tag{10}
\]

Relative to **whole-component** U_c, the denominators are e(Q). Relative
to **restricted** U_c,A, the denominators are E_A(Q) when E_A>0; otherwise
the restricted quantities are zero and those conditional ratios are undefined.
A record-dependent sector would require retaining the marked Phi-weighted
sum in (9), not these unmarked formulas. A restricted D_A need not have
the sign of the whole D.

Take `A={P:delta(P)>0 and P notin C}`, the residual sector from
[RI-65](../native_growth_residual_reentry_v1/OBSTRUCTION.md). Put
`p_c^0=alpha_c^min U_c`, the actual-history-weighted auxiliary boundary
proper-birth mass of component c. The exact residual is

\[
 T_n^+=\underbrace{\sum_c p_c^0\frac{H_A^{\rm num}(Q_c)}{e(Q_c)}}_{A_n^+}
 +\underbrace{\sum_{j\in A}\pi_jf_j
       \left[1-\sum_{S\subsetneq P_j}u_j(S)\alpha_{c(j,S)}^{\min}\right]}_{F_n^+}.
 \tag{11}
\]

Equivalently `T_n^+=B_n,A+sum_c p_c^0 D_A(Q_c)/e(Q_c)`, with
`B_n,A=sum_(j in A)pi_j f_j`. This reindexing does not omit the full-complement
mass, change the actual history law, or make global canonical minimization
into a separate sector optimization.

RI-61's canonical elimination now has an intrinsic sign interpretation:
`D(Q)>0` forces zero boundary allocation in every primary optimum, whereas
`D(Q)=0` has zero allocation in the canonical lexicographic optimum. Thus
canonical support lies in `D(Q)<0`. Strict mixing restores positive mass
on all components; the assertion is not about every strict law or every
zero-cost primary optimum. Components with the same Q still cannot be merged.

## 5. All-size stress family: a negative cost with raising share near one

Let F be the five-vertex hook `(4,1)` and define
`Q_t=F disjoint-union Ant_t`, for every integer t>=1. Use G=`(3,1)` and
C4 for a four-chain. All exceptional sets below are arbitrary induced
subsets, not only ideals or maximal deletions.

Every nonempty Ferrers order has a unique minimum. A retained Ferrers subset
of disjoint old components can therefore use only one component. Even if a
new universal top is retained, selecting nonempty subsets of two old components
still leaves two minima. The largest retained Ferrers suborder of Q_t is F,
so `delta(Q_t)=t`. The same argument applies to every parent below.

A finite Ferrers order with a greatest element is a rectangle. F+top is
nonchain, of size six and height five; the only nonchain six-cell rectangle
has height four. Hence F+top is not Ferrers, but retaining F attains size
five. G+top is nonchain of prime size five, so cannot be a rectangle; its
largest retained Ferrers subset has size four, attained by G. C4+top is C5.
With isolates present, no larger cross-component Ferrers subset is possible;
a single isolate plus top has only two vertices. These upper bounds and
attaining subsets prove the full-top defects, including internal deletions.

Since e(F)=4, e(G)=3 and e(C4)=1, interleaving their vertices with distinguishable
isolates gives the following **per-deleted-vertex** counts:

| Deleted maximal role | Multiplicity | Parent P_v | e(P_v) | delta(P_v) | delta(P_v+top) | Proper increment | Reduced cost |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| Isolate | t | F plus Ant_(t-1) | `(t+4)!/30` | t-1 | t | 1 | 0 |
| Long-arm tip | 1 | G plus Ant_t | `(t+4)!/8` | t | t+1 | 0 | -1 |
| Short-arm tip | 1 | C4 plus Ant_t | `(t+4)!/24` | t | t | 0 | 0 |

Summing the last-element counts proves

\[
 e(Q_t)=\frac{(t+5)!}{30},\qquad
 H(Q_t)=\frac{t}{t+5},\qquad
 \boxed{\frac{D(Q_t)}{e(Q_t)}=-\frac{15}{4(t+5)}<0.} \tag{12}
\]

For this family only, one can also prove that all full-mark assignments
belong to one component: deleting any isolated maximum exposes the local
empty-precursor node, which reads no marks. Every maximal-deletion role for
any full assignment connects to that same node. This uses precursor erasure
explicitly; it is not an assumption about general terminal types.

Every relevant parent is noncritical: deleting the long-arm tip of F/G, or
the chain tip of C4, preserves its defect. For t>=2 every parent also has
positive defect, so sector A retains all roles and both ratios in (12).
For t=1 the isolate-deletion parent F has defect zero and is excluded.
Here `e(Q_1)=24`, `E_A=20`, `H_A^num=0`, `D_A=-15`. Thus
`U_c,A/U_c=5/6`, `R_c,A/U_c=0`, `beta_c,A/U_c=-5/8`, but
`beta_c,A/U_c,A=-3/4`. Using the unreduced denominator in that last ratio
would be an error.

The t=1 instance is RI-63 component 98, whose boundary alpha is zero. A
negative cost therefore does not force allocation even in the actual finite
candidate. The family theorem proves neither nonzero allocation for larger
t nor recurrent occupation or asymptotic failure.

## 6. Consequence for a drift envelope: cost sign is not a uniform charge

The stress family gives, for t>=2 entirely within the positive-defect,
noncritical sector,

\[
 \frac{H(Q_t)}{-D(Q_t)/e(Q_t)}=\frac{4t}{15}\longrightarrow\infty. \tag{13}
\]

Therefore no size-independent constant C can establish the componentwise
inequality `R_c,A <= C*(-beta_c)` on all negative-cost components of this
model. This rejects a **uniform cost-only charging inequality**, not an
inequality that also uses actual allocations, competing row caps or history
occupation. The t equal maximal-deletion roles are counted in the terminal
history sum; they are not t empty-ideal slots in any one parent row.

For canonical boundary allocations define `d_Q=D(Q)/e(Q)<0` on their support
and `h_A(Q)=H_A^num(Q)/e(Q)`. With `Delta_n=B_n-m_n`, (3) yields

\[
 \Delta_n=\sum_{c:d_{Q_c}<0}p_c^0(-d_{Q_c}),\qquad
 A_n^+=\sum_{c:d_{Q_c}<0}p_c^0h_A(Q_c). \tag{14}
\]

For any threshold K>0, a valid but not yet decaying bound is

\[
 T_n^+\le K\Delta_n+
 \sum_{c:\ h_A(Q_c)>K(-d_{Q_c})}p_c^0+F_n^+ . \tag{15}
\]

This follows by splitting the proper sum in (14) and using `0<=h_A<=1`.
It identifies the missing ingredient concretely: a bound on actual allocated
mass in the high-raising/low-improvement terminal tail (or another argument
using the row caps), together with control of F_n^+. The hook family prevents
removing that tail with a universal constant. Neither Delta_n nor either
remaining term is proved small here; (15) is not a sublinearity theorem.
No successor bound or next-layer optimization is started in this packet.

## 7. Bounded exact finite corroboration and scope

The envelope was declared before computation: 900 seconds and 2 GiB resident
memory per attempt, using sampled/checkpoint enforcement rather than a hard
OS allocator limit. Instantaneous unobserved overshoot is not excluded.
Failures are not grounds to weaken a claimed threshold. There is no optimizer,
new dependency, probability table beyond RI-63, or blanket seven-event atlas.

The [checker](check.py) explicitly reuses byte-pinned accepted RI-63 sources
and the actual RI-41 certificate. It reconstructs the complete parent-five
problem and canonical certificate. New checks concern only intrinsic terminal
six-event diagnostics, marked fibers, maximal-deletion roles and their weighted
sums. The all-size proof is sections 2–3; finite agreement does not replace it.

A main independent audit used forward ideal-prefix dynamic programming to
count linear extensions, rather than the new checker's maximal-deletion
recursion. It aggregated all 15,702 canonical marked-row labeled proper-slot
occurrences and verified all 798 components, their whole and sector ratios,
and their existing beta coefficients exactly. It covered 703 natural terminal
profiles and 885 DP orders, taking 5.116 seconds with sampled peak RSS
105,299,968 bytes. Negative/zero/positive counts were 125/262/411.
For component 98 it independently found

\[
 U=41/87228416,\quad R=41/523370496,\quad
 \beta=-205/697827328,\quad U_A=205/523370496,\quad R_A=0.
\]

The saved [certificate](CERTIFICATE.json) contains all 798 component records
and all 255 proper unmarked terminal types. Its exact reconstruction covers:

- 357 natural parents, 11,424 raw marked rows and 1,490 marked row classes;
  142,944 labeled proper slots and 2,961 proper local nodes;
- 4,467 naturally labeled proper terminal orders, 671 maximal-deletion roles
  and 1,381 component/parent-type role weights;
- every one of the 16,320 complete terminal mark assignments and all 42,944
  marked maximal-deletion roles, including common component membership,
  common Phi, and the `e(Q)/(64*|Aut(Q)|)` fiber-mass normalization;
- 4,788 whole/sector factor equalities: the U/U normalization and five
  nontrivial ratios per component. There are 703 positive sector masses and
  457 positive sector raising masses. For the other 95 components, conditional
  sector ratios are null, not invented zero-denominator values.

The accepted complete RI-63 primary/canonical and actual strict-law replay,
including its 15 certificate controls, is checked again. The new checker
rejects changed dependency bytes, a wrong marked-history weight, dropped
natural-label multiplicity, wrong extension count, wrong full-top defect,
wrong global cost, wrong sector mass, wrong automorphism divisor, omitted
newborn fair-bit factor, a missing full terminal mark, merged nonisomorphic
terminals, duplicate JSON keys and a terminal above the six-event cap.
Ordinary saved-certificate execution also rejects a missing component:
13 controls in witness mode, 14 in saved-certificate mode. Certificate checking
compares the complete reconstructed object, not only selected fields or hashes.

Reproduction, from the repository root, requires only Python's standard library:

```sh
python3 -I -S -B docs/track_b/native_growth_terminal_cost_v1/check.py
python3 -I -S -B -O docs/track_b/native_growth_terminal_cost_v1/check.py
```

The main worker actually ran both saved-certificate commands with Python 3.14.0
and the declared sampled parent watchdog. Both exited zero: 12.142/12.156
seconds, sampled peak RSS 123,633,664/124,403,712 bytes. Their 1,401-byte stdout
was identical, SHA-256
`6064f6abe8397e79d0dc2bf03b390c2f5546970cdd76e055f578452b5842ebba`.
The checker author's earlier normal/optimized witness runs also exited zero
in 11.989/11.909 seconds, with byte-identical 450,950-byte stdout.

Stable byte pins:

- `check.py`: `cf54313465da754345406f58a1a60622e51c034d954f8147332c1578cd62fdab`;
- `CERTIFICATE.json` (451,015 bytes):
  `67d6b6706da3100afa89f8c99c6a72b88a6b39c7a1bc628fa69a02e46eca9d01`;
- canonical certificate object:
  `e667fbade262c694bceb1d40628391b6f3b4acfb2357381c662b31068332680a`.

The certificate records all three accepted dependency byte pins; the checker
verifies those bytes before loading helpers and again after reconstruction.
Two independent reviewers read the complete proof and 524-line source without
finding blockers. A separate complete parsed-data audit checked every terminal,
role, component, sector denominator, mark-fiber partition and group, including
`K=U/e` and the stored defect increments. These checks corroborate, rather than
replace, the all-size arguments above.

Exactly `FACTORIZATION.md`, `check.py` and `CERTIFICATE.json` are authored in
this directory. No q6 probability or seven-event order is evaluated. Accepted
sources, ledgers, RET, measurement and git/index operations remain untouched
by the worker.

**Disposition:** the terminal-cost factorization is proved conditionally
within the frozen scalar-passive model, and the uniform cost-only charging
candidate is rejected by an all-size intrinsic family. Prefix/record-dependent
magnitudes, allocations and full-birth residuals remain indispensable. No
all-size decay, informative QM, geometry, mass, gravity or physical discriminator
is derived. Option B and metric-as-record Status M remain unchanged. Stop
at stable handoff for coordinator adjudication and successor selection.
