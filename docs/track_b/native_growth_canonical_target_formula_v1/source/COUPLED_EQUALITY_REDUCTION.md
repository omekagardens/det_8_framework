# RI151 — coupled Ferrers equalities and the canonical root coefficient

30 September 2026. Manual author-side proof; no scientific evaluation or
independent acceptance. The accepted tightness of every canonical Q row
can be combined with the other incident Ferrers parents. The resulting
block is an exact slice of the full primary optimal face, not merely a
local linear system. The original component ordering then determines
both target canonical coefficients symbolically.

The weighted q and W inequalities are not decided here. The result removes
the previously unspecified target canonical-coordinate contrast in favor
of an explicit expression in the unchanged size-four prefix probabilities.

## 1. Accepted tightness and the necessary component closure

The complete RI151 assignment and RI149 root adjudication accept O01:
every canonical marked row at Q=(4,1) is tight. All active canonical
components are everywhere defect-neutral; every noncritical canonical row
has zero boundary drift. A Ferrers parent has defect zero and cannot be
critical under the accepted criterion requiring a maximal deletion with
defect one less. None of these statements sets an actual strict-mixture
full probability to zero.

Use the following names only for boundary component coordinates at parent
size five:

| Terminal | Boundary coordinates | Complete parent roles |
|---|---|---|
| `(5,1)` | `a_i` | C5 singleton; Q long four-chain |
| `(4,1,1)` | `b_i` | Q short two-chain; P=(3,1,1) either full three-chain arm |
| `(4,2)` | `d_(i,u)` | Q inner V3 precursor; U=(3,2) long three-chain |
| `(3,2,1)` | `h_i` | P inner V3 precursor; U short two-chain |

Here `i` is the root bit and `u` the distinguished long-arm first-vertex
bit. These boundary `b_i,h_i` are not the held C4 core probabilities or
the held H5 one-cap probabilities used in older manuscripts.

The companion incidence proof establishes exactly two root components
for `(4,1,1)`, four `(i,u)` components for `(4,2)`, and two root components
for `(3,2,1)`. In the first case the Q short-arm local node connects by a
complete marked diamond to every selected-arm local node at the symmetric
P parent. The root survives, but the other selected marks can vary. In
the second case the common precursor of the two roles retains the root
and its distinguished long-arm atom, and both marks survive; the other
marks vary along the diamond. For the staircase, its three maximal
deletions give one P role and two isomorphic U roles. The P inner node
with unlike atom bits connects both short-arm U markings. Thus only the
root bit remains. The third pair of maxima supplies further U–U edges,
not another component. All inherited and newborn marks are transported.

The two P full-arm ideals are distinct occurrences with the same b_i.
They must be summed twice even when their marks agree. Each U row has
one staircase role, not two copies merely because the terminal has two
isomorphic maximal deletions.

## 2. Fixed lower-prefix probabilities, without new evaluation

Write the following positive entries of the unchanged actual size-four
and smaller prefix:

\[
 p_i=q_{C4,i}(\{\text{root}\}),\quad c_i=q_{C4,i}(C4),\quad
 f_i=J_i(9),\quad g_{iu}=J_{iu}(11),\quad
 v_i=q_{V3,i}(V3),\qquad L_i=41p_i.
 \tag{1}
\]

Here J is the four-element hook `(3,1)` with labels root0, long-arm1<2,
short-leaf3; V3 is the three-element fork. The symbol v_i is its full
probability, not the sensitivity contrast `v=V1-V0`.

The stage-four marked-component diamonds prove J9 depends only on the
root bit: its terminal is `(3,1,1)` and the two selected two-chain roles
erase the nonroot selected marks through their diamond. J11 depends on
`(i,u)`: its terminal `(3,2)` connects the hook's inner V3 role to a
square's selected two-chain role, retaining the root and that selected
atom. If `e_i` is the positive V3 selected-two-chain probability, the
same component relation gives

\[
 q_{D4,(i,u)}(\text{selected C2})=(e_i/v_i)g_{iu}.
 \tag{2}
\]

The stage-four `(4,1)` component relates J7 to the C4 singleton. Their
potentials are the C3 full and singleton probabilities respectively,
so `J7=(A7/A1)p_i=41p_i=L_i`. This uses the unchanged accepted C3 row,
not a new coefficient or probability calculation.

The full C4 probability really is root-only here. RI127 RECORD_TRANSPORT
equations (4), (6), (8) give `nu_xi=theta^3 c_xi` and
`Delta_xi nu=chi(xi) Delta_1 nu`, with `theta>0` fixed. Dividing only
by theta cubed proves `c_xi=c_i` for all assignments with root i.
No nonzero contrast of nu is assumed or needed. This removes no record
by fiat; it uses the accepted all-record transport proof.

## 3. The complete coupled canonical block

For each root bit, suppress i temporarily. The nonnegative boundary
coordinates are `a,b,d0,d1,h`; the fixed positive quantities are
`p,c,f,g0,g1,v,L=41p`. The coupled constraints are exactly

\[
 \begin{aligned}
 &pa\le1 &&\text{(C5)},\\
 &ca+fb+g_u d_u=1 &&\text{(Q, each }u=0,1\text{)},\\
 &2Lb+(g_u g_s/v)h=1 &&\text{(P, all }u,s\in\{0,1\}\text{)},\\
 &L d_u+(f g_s/v)h\le1 &&\text{(U, all }u,s\in\{0,1\}\text{)}.
 \end{aligned}
 \tag{3}
\]

All other inherited marks remain in the source row domain. The equations
repeat across them only by the stated locality, component, and transport
proofs. There is no averaging over a marked row or division by an arm
multiplicity.

Q's equation is O01 after the proved substitutions (1). P is also
Ferrers and noncritical. Its full cone has height four and a unique
maximum, but is not a 2-by-3 rectangle: its two intermediate arm-end
vertices each cover only one atom, whereas that rectangle has an
intermediate vertex above both atoms. Nor is it a chain. Its full birth
therefore raises defect by one. With canonical proper raising terms zero,
accepted zero boundary drift forces every P row tight. Its two neutral
arm births each have potential L. Its neutral inner birth has potential
`g_u g_s/v`, by the two-maximum deletion formula. These give the P line.

U's full birth is the six-element rectangle and is neutral, so zero drift
does **not** imply a tight cap. Its neutral long-arm birth has potential
L. Its short-arm potential is
`f*q_D4(selected C2)/e_i=f g_s/v`, using (2). Its complete remaining
canonical proper terms are zero, giving the U inequality. The full C5
birth is also neutral; its cap likewise remains an inequality.

The complete Ferrers shapes at five elements, up to transposition of
their cell diagrams, are C5,Q,P,U. At six elements, the nonrectangular
Ferrers shapes are exactly the four terminals in section 1. The chain
and the 2-by-3 rectangle have unique maxima and can arise from Ferrers
five-parents only by full birth, not a proper role. Thus (3) accounts
for every canonical neutral proper term in these four parent shapes.
Every maximal deletion of a Ferrers terminal is again a Ferrers downset,
so these four terminal components have no incident non-Ferrers parent.

## 4. Why feasible block variations are genuine primary-face variations

Hold all coordinates outside the ten-component, two-root block fixed at
their actual canonical values. In particular all other contributions to
Ferrers parent rows are their accepted zero raising coordinates. The two
root blocks are independent: every retained neutral precursor contains
the unique root, and its bit is invariant throughout these components.

Changing a block point subject to (3) and nonnegativity affects no other
parent row. C5 and U caps are preserved; every Q and P row remains tight.
For C5 and U, neutral proper births and the full birth have defect
increment zero, so their objective contribution from these coordinates
is zero. For Q and P the full increment is one and every retained proper
increment is zero. Their objective contribution is consequently minus
their history mass times their proper boundary row sum, which remains
one. Every individual occurrence and every actual history weight is
retained in this argument; no value of a history mass is needed.

Thus every nonnegative solution of (3), with all outside coordinates
fixed as above, is globally feasible and has the **same full primary
objective** as the actual canonical solution. It is an actual slice of
the original primary optimal face. Conversely the canonical solution
belongs to this slice, so the block is known to be nonempty.

This lifting proof is stronger than a nullspace count. It does not claim
that arbitrary local rank freedom changes the canonical solution, or
that every primary optimum has zero raising coordinates. Original
full-vector lexicographic minimization still selects the actual point.

## 5. Exact interval/polygon reduction, including zero cases

Define the common nonnegative residual

\[
 t=1-ca-fb=g_0d_0=g_1d_1\ge0.
 \tag{4}
\]

Subtract two P equations in (3). Since `g0,v>0`,

\[
 (g_0-g_1)h=0.
 \tag{5}
\]

This does not select either branch for the fixed prefix.

If `g0!=g1`, (5) gives

\[
 h=0,\quad b=1/(2L),\quad d_u=t/g_u,\quad
 a=(1-f/(2L)-t)/c,
\]

and the complete remaining interval is

\[
 \max\{0,1-f/(2L)-c/p\}\le t
 \le\min\{1-f/(2L),g_0/L,g_1/L\}.
 \tag{6}
\]

If `g0=g1=g`, the complete remaining polygon can be written

\[
 \begin{gathered}
 0\le b\le1/(2L),\\
 \max\{0,1-fb-c/p\}\le t\le1-fb,\\
 Lt+f(1-2Lb)\le g,\\
 a=(1-fb-t)/c,\quad d_0=d_1=t/g,\quad
 h=v(1-2Lb)/g^2.
 \end{gathered}
 \tag{7}
\]

Every division is by a named strictly positive prefix expression. Both
directions follow by substitution into (3); no constraint is merely
necessary and then silently used as sufficient. Zero coordinates, tied
interval endpoints, and degenerate polygons are retained. Their dimensions
are not presumed positive. Nonemptiness is inherited from the actual
canonical point, not demonstrated by choosing new prefix values.

## 6. The minimum target coordinate on the exact primary slice

For either branch of (5), put `G=min(g0,g1)`. The minimum a over the
nonempty block is

\[
 \boxed{\quad a_{\min}=
 \frac{[L-f/2-G]_+}{Lc},\qquad [z]_+=\max(z,0).\quad}
 \tag{8}
\]

For unequal g, maximizing t in (6) gives this formula directly. Known
nonemptiness ensures the resulting minimum also obeys the C5 upper cap.

For equal g, substitute the Q relation into the U cap to obtain
`Lca+3Lf b>=L+f-g`. Since `b<=1/(2L)`, every feasible point satisfies
`Lca>=L-f/2-g`, as well as `a>=0`. To verify attainment, not just the
lower bound, retain the following exhaustive cases:

- If `f<=2L` and `L-f/2-g>0`, choose `b=1/(2L)`, `h=0`, `t=g/L`
  and a from (8). All U caps and both Q equations hold. The C5 cap
  follows because this proven lower bound is at most the a-coordinate
  of the known nonempty block.
- If `f<=2L` and `L-f/2-g<=0`, choose `a=0`, `b=1/(2L)`, `h=0`,
  and `t=1-f/(2L)`. It is nonnegative and `Lt<=g`, so every cap holds.
- If `f>2L`, the unequal-g branch would contradict nonnegativity in Q
  and is impossible for a nonempty block. In the equal-g branch, Q
  gives `fb<=1-ca`. Combining this with the U inequality yields
  `L+f-g<=Lca+3Lfb<=3L-2Lca<=3L`, so `f<=2L+g`.
  Set `a=0`, `b=1/f`, `t=0`, and
  `h=v(1-2L/f)/g^2`. These are nonnegative and the U cap becomes
  `(f-2L)/g<=1`. Thus (8), which is zero here, is attained as well.

These constructions vary only boundary coefficients within the exact
primary slice at the **fixed** prefix. They are proof witnesses for a
symbolic extremum, not invented countermodels or actual coefficient
evaluations.

## 7. Why the actual canonical coordinate equals this minimum

The companion source-order proof retains RI63's original local-node key
and original component order. Its manual finite comparison proves that
the minimum parent keys satisfy `E_Q<E_P<E_U<E_C5`. At the unique minimum
Q labeling, the target a component has precursor mask15, whereas b has
mask17 and d has mask19. The staircase h component has its minimum
parent at P. Therefore both a target coordinates precede every b,d,h
coordinate in this closed Ferrers block. The comparison does not use
a numerical component-index lookup or infer ordering from a coefficient.

One can check the parent-key comparison directly with the relation-bit
sets in that proof: Q has `{1,2,3,4,7,8,13}`, P has
`{1,2,3,4,9,13}`, U has `{1,2,3,4,8,9,13}`, and the C5 minimum includes
bit19. Non-topological labelings cannot lower the minimum: swap the
highest labeled ancestor participating in an inversion with a lower
labeled descendant. Higher source rows are unchanged, and the former
ancestor's source row strictly decreases because the descendant's future
is a strict subset. The remaining topological placements of these fixed
shapes give the listed minima. The companion provides the full placement
argument; this is not a global graph enumeration.

Suppose the actual canonical a_i exceeded (8). Replace only its root
block by the attaining point in section 6 and retain all outside
coordinates, including the other root block. Section 4 proves feasibility
and equal primary objective. Every earlier original coordinate is
unchanged, because a_i is the first changed coordinate in that block.
The reconstructed full vector is lexicographically smaller, contradicting
canonicality. Hence, restoring root indices,

\[
 \boxed{\quad a_i^*=
 \mathcal A_i:=
 \frac{[L_i-f_i/2-\min(g_{i0},g_{i1})]_+}{L_i c_i},
 \qquad i=0,1.\quad}
 \tag{9}
\]

This uses the original full-vector order; it does not lexicographically
minimize a reordered list or the reduced variables b,t alone. Intervening
outside coordinates are held fixed. Formula (9) is an unevaluated identity
for the actual canonical coefficient, not just a necessary lower bound.

## 8. Consequence and still-unresolved quantitative comparison

The exact target correction and its contrast are now

\[
 \kappa_i=(35/36)\mathcal A_i,\quad
 N_i=(35/36)p_i\mathcal A_i,\quad
 \delta_\kappa=(35/36)(\mathcal A_0-\mathcal A_1).
 \tag{10}
\]

In RI147/RI149's notation, the exact q identity therefore reads

\[
 q(x)=T_{\rm core}(x)+\frac{35}{36}
 \{p_0\mathcal A_0 k_0(x)-p_1\mathcal A_1 k_1(x)\}.
 \tag{11}
\]

Its remaining lower-bound question is a comparison of these fixed
lower-prefix expressions, including their positive-part branches, with
the required multiple of D3. It no longer requires an unspecified
canonical residual-capacity ordering for a_i. No sign of (10), no
adequate quantitative q/D3 or v/D3 floor, and neither RI147 endpoint
budget is established here. The correlated scale cap and reference
sums must use the same substituted N_i; they cannot be held at unrelated
favorable values. Actual W, the individual connected margins, and the
whole shared H30 system remain undecided.

All equalities above concern the canonical **boundary** law. At a tight
Q or P row the actual strict mixed full probability is
`1/36-theta U_j`, not zero. Since
`theta=1/[72(1+M5)]` and `U_j<=M5`, it is strictly greater than `1/72`.
If a canonical component vanishes, its actual proper coefficient still
contains the positive restoration theta. No strict-law endpoint is
admitted or removed by this argument.

## 9. Literal premises and author work boundary

Read for this contribution:

- Complete assignment and root decision at `/Volumes/AI_DATA/development/det-review-evidence/ri149-root-canonical-review-25_k3ysa/NATIVE_SUCCESSOR_RESERVATION.json` and `RI149_ROOT_ADJUDICATION.json`; the O01 section of `ROOT_MANUAL_REVIEW.json` was searched as administrative text.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`, sections 1–3: fixed lower prefix, full fork probability, component quotient, deletion potential and complete-row multiplicities.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/RECORD_TRANSPORT.md`, section 3 reread with the already read equations (4), (6), (8): the derived full-record c compression. A text search of same-directory `LOCAL_POSITIVITY.md` did not supply an additional premise.
- Accepted RI63 primary/lexicographic and active-neutral premises from the unchanged `COMPLETION.md`, read in the preceding author contributions and preserved by the root decision.
- Current companion incidence and source-order proofs were developed and hand-crosschecked through author coordination. This is author-peer checking, not nonauthor acceptance.

Only this assigned Markdown is authored. No scientific body was decoded,
actual prefix value, canonical coefficient, history mass, maximum, scale,
H/z or final sign was evaluated, and no symbolic/numerical engine,
source/helper import, compilation, AST, probe, execution, global graph
enumeration, controller, card or runtime inventory was used. There is no
repository/index/Git or predecessor change. All31/139/20/42 obligations,
shared T1 recovery, other eight connected parents, all five Di systems,
strict endpoints, old numerical P2/P3 targets and Y=1/4 remain unchanged.
RET and measurement remain separate. This finite identity makes no full
QM, geometry, gravity, all-size, empirical or ontological claim.
