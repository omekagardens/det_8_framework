# RI168 — complete incidence of the six selected C4 components

30 September 2026, Hawaii. Manual fixed-shape proof; source-only author work,
not an independent review or an execution admission. The accepted RI41
component vector and all its global rows remain fixed and unread as scientific
data. No graph program, coefficient evaluation, new fixture or alternative law
is used below.

## 1. Result, conventions and two distinct kinds of equality

The C4 proper slots with masks 1, 3 and 7 belong respectively to **two,
four and eight** ratio-graph components. Their complete local labels are

    P_i,       S_(i,u),       B_(i,u,v),       i,u,v in {0,1}.

The six components selected in the preceding contrast proof are

    P_0, P_1, S_(0,0), S_(1,0), B_(0,0,0), B_(1,0,0).

The interior bits in the latter two families cannot be erased from the
component graph. Nevertheless, the separately inherited RI127 transport
theorem implies that the **actual accepted probabilities** in every root
sector satisfy

    q_C4(1)=p_i,   q_C4(3)=s_i,   q_C4(7)=b_i,
    q_C4(full)=c_i.                                      (1)

For masks 3 and 7, these actual value equalities hold across distinct graph
components. They are not new local-node identifications. Section 8 proves the
precise implication from the inherited transport result, including the full
complement, rather than obtaining it by dropping records from a full row.

Let C4 have vertices r<a<b<c, in that order, with natural representative
(0,1,3,7). A representative lists the strict predecessor masks of successive
vertices. An ideal mask uses the same vertex order. A local node retains the
whole unmarked parent, the selected ideal, and exactly the marks in that
ideal; a complete marked row retains **all four marks**. Simultaneous marked
isomorphisms are allowed, not independent record flips.

The common three-chain base is C3 on r<a<b. Its accepted complete row is

    q_C3(0)=q_C3(1)=q_C3(3)=e=1/44,
    q_C3(7)=A=41/44,       A/e=41.                       (2)

No actual size-four coefficient or probability is evaluated. Formula (2)
is an explicitly stated accepted prefix theorem, not a new reading of the
RI41 scientific certificate. Every proper probability has the form

    q_P(S)=alpha_[P,S,r|S] * u_P(S),

where the alpha subscript denotes its **global** ratio component. The
maximal-deletion potential is

    u_P(S) = product over nonempty T subset Max(P)\S
             q_(P\T)(S) ^ ((-1)^(|T|+1)).                (3)

Thus one omitted maximum gives one smaller-parent probability. Two omitted
maxima give the product of the two one-deletion probabilities divided by
the two-deletion probability. Positivity permits the divisions below.

## 2. All terminal types and maximal-deletion roles

Append a new maximal event x to C4 above the selected initial segment. The
three resulting five-event terminals have the following cover relations:

    mask 1:                  mask 3:                  mask 7:

        c    x                   c    x                   c    x
        |    |                   |    |                    \  /
        b    |                   b    |                      b
        |    |                    \  /                       |
        a    |                     a                         a
         \  /                      |                         |
           r                       r                         r

The diagrams are mnemonic; the exact relations are respectively

    T1: r<a<b<c and r<x;
    T3: r<a<b<c and a<x (hence also r<x);
    T7: r<a<b<c and b<x (hence also r<x and a<x).           (4)

In each terminal the two maxima are c,x. The unique vertex with two
outgoing cover relations is respectively r,a,b. Its distance in cover
edges from the unique minimum is 0,1,2. Consequently the three terminal
types are pairwise nonisomorphic, including after forgetting every mark.

The alternative four-event parent shapes needed here are

    V: r<a<b and r<x,       order (r,a,b,x), (0,1,3,1);
    T: r<a<b and a<x,       order (r,a,b,x), (0,1,3,3).

V has no nontrivial automorphism. T exchanges its two tips b,x, while
fixing r,a. Here T denotes the four-event stem-fork, not any seven-event
parent from the H30 support.

| Terminal | Deleted/newborn maximum | Remaining parent | Selected precursor in that parent |
|---|---|---|---|
| T1 | x | C4 | {r}, mask 1 |
| T1 | c | V | its full long arm {r,a,b}, mask 7 |
| T3 | x | C4 | {r,a}, mask 3 |
| T3 | c | T | one full arm {r,a,b}, mask 7 |
| T7 | x | C4 | initial triple {r,a,b}, mask 7 |
| T7 | c | C4 | initial triple {r,a,b}, mask 7 |

For T3, choosing T's other arm gives the same unmarked local role under
tip exchange but a second **individual ideal occurrence**, mask 11, in
the full T row. For T7 both deletion roles give the same C4 local node
after the terminal tip exchange; no V or T parent occurs.

These are complete role lists. An event appended in the stated birth rule
is maximal. Conversely deleting any possible newborn maximum recovers its
parent and its strict-past precursor. The displayed two maxima therefore
exhaust the possible presentations. A raw diamond deletes both of its
newborn maxima; its old base here is always the displayed C3. Ratio edges
preserve the whole terminal order, so no path can lead to a different
terminal type or a hidden extra parent. This argument concerns incidence,
not independent feasibility of different columns in the global matrix.

## 3. Complete marked diamonds and local component graphs

Give the C3 base marks (i,u,v) at (r,a,b), and give the two newborn events
arbitrary marks t,w. All five bits are independently variable. The second
precursor never includes the first newborn, but that newborn's mark remains
in the complete final marked order. Both routes multiply the entire
unchanged payload by the corresponding scalar product divided by four.
Nothing below averages newborn or inherited bits.

### 3.1 Singleton family P_i: ordered pairs (1,7) and (7,1)

A root birth first creates V; the subsequent C3-full birth reads its
long-arm local marking (i,u,v). A C3-full birth first creates C4; the
subsequent root birth reads only i. Hence every marked diamond gives

    e * q_V(7;i,u,v) = A * q_C4(1;i),
    q_V(7;i,u,v) = 41 p_i.                               (5)

For fixed i, the four V local nodes indexed by (u,v) each connect directly
to the single C4 singleton node. The underlying simple incidence graph is
the star K_(1,4), with five nodes; the raw parallel edges are retained in
section 4. V's selected ideal locally retains u,v; its
value ceases to depend on them because of (5), not because they were
forgotten before applying the diamond. C4's top mark and its two interior
marks lie outside its selected singleton.

The terminal's unique minimum belongs to every precursor, so i is retained
by every node and edge. No isomorphism changes its value. Thus there are
exactly two components P_i. Their C4 and V potentials are e and A,
respectively, and their common global scale alpha_Pi obeys

    p_i=e alpha_Pi,       q_V(7)=A alpha_Pi.

### 3.2 Initial-pair family S_(i,u): ordered (3,7) and (7,3)

An initial-pair birth first creates T; the subsequent full-base birth
selects one full arm, retaining (i,u,v). A full-base birth first creates
C4; the subsequent initial-pair birth retains (i,u). Therefore

    e * q_T(arm;i,u,v) = A * q_C4(3;i,u),
    q_T(7)=q_T(11)=41 s_(i,u)                            (6)

in a full T row whose stem marks are (i,u). The last expression uses
s_(i,u) to denote the component-level C4 probability before applying the
separate inherited equality (1).

For fixed (i,u), the two T selected-arm local nodes, indexed by their tip
bit v, connect to one C4 selected-pair node. Its underlying simple graph
is K_(1,2), with three nodes, retaining all the raw parallel edges below.
The root and next stem vertex lie in every precursor and are
intrinsically distinguished by order. Neither i nor u can be erased or
exchanged. T's tip automorphism exchanges the choice of arm, not the
ordered stem bits. It follows that there are exactly four components
S_(i,u), with potentials e on C4 and A on each T arm.

The two individual T ideals contribute twice to normalization even when
their local nodes, component labels or probabilities coincide. Equation
(6) is not permission to replace their sum by a single orbit weight.

### 3.3 Initial-triple family B_(i,u,v): equal pair (7,7), once

Both births are above the whole C3. Both parents are C4, both selected
local markings are the same (i,u,v), and the edge equation is

    A * q_C4(7;i,u,v) = A * q_C4(7;i,u,v).                (7)

These are retained loops, not omitted constraints. Tip exchange relates
the two birth presentations but fixes the entire ordered three-stem.
Every component is one local node, indexed by (i,u,v); there are eight.
Its potential is A, and b_(i,u,v)=A alpha_B(i,u,v).

The equal precursor pair is one ordered pair, not two artificially
different orientations. The four assignments of (t,w) remain distinct
raw diamond instances, including (0,0). No edge joins different stem
mark triples. The actual inherited equality b_(i,u,v)=b_i is therefore
not a consequence of this loop graph.

## 4. Canonical rows, raw rows and labeled-ideal multiplicities

The counts here are proved from these fixed shapes and bit cubes; they
are not output from an enumeration or qualification of the full graph.
Canonical marked rows are full marked-parent isomorphism classes. Raw
rows are the accepted naturally labeled unmarked orders with all their
independent mark assignments.

C4 has one natural order and no nontrivial automorphism. V has three
natural orders: after r, interleave its short leaf among the two ordered
long-arm events. It has no automorphism, so each canonical marked V row
has three raw representatives. T has two linear extensions differing by
its tip swap and just one natural unmarked order. For fixed stem marks,
its three canonical tip patterns 00,01,11 have raw multiplicities 1,2,1.

| Component | Local nodes | Canonical incident rows | Raw incident rows | Canonical target-ideal occurrences | Raw target-ideal occurrences |
|---|---:|---:|---:|---:|---:|
| P_i | 1 C4 + 4 V = 5 | 8 C4 + 8 V = 16 | 8 C4 + 24 V = 32 | 16 | 32 |
| S_(i,u) | 1 C4 + 2 T = 3 | 4 C4 + 3 T = 7 | 4 C4 + 4 T = 8 | 4 C4 + 6 T = 10 | 4 C4 + 8 T = 12 |
| B_(i,u,v) | 1 C4 | 2 C4 | 2 C4 | 2 | 2 |

For T's canonical 00 row, both arms have the tip-0 local marking; for
01 one arm has each tip marking; for 11 both have tip 1. Each canonical
row still contains two arm occurrences. The mixed row's raw multiplicity
is two, independently of those two ideal occurrences.

The ordered raw diamond multiplicities per component are exactly

| Component | Old C3 mark cube at fixed component label | Newborn pairs | Precursor orders | Raw diamonds |
|---|---:|---:|---:|---:|
| P_i | 4 choices of (u,v) | 4 | (1,7),(7,1): 2 | 32 |
| S_(i,u) | 2 choices of v | 4 | (3,7),(7,3): 2 | 16 |
| B_(i,u,v) | 1 | 4 | (7,7): 1 | 4 |

All P and S diamonds connect different parent shapes; all B diamonds are
local-node loops. The C3 base has one natural order. No terminal tip
automorphism divides these raw counts, and no extra factor is inserted
for its isomorphic maximal-deletion presentations.

The selected six components have 104 raw diamond instances: two times
each of 32,16,4. Their incident-row counts must **not** simply be added:
C4 rows occur in more than one family. Their distinct union consists of
all 16 C4 raw rows, all 48 V raw rows, and the eight T raw rows with
stem bit u=0, hence 72 raw rows. The corresponding canonical union has
16 C4 + 16 V + 6 T = 38 rows. Counting individual selected target ideals,
not distinct rows, gives 92 raw occurrences and 56 canonical occurrences.
These overlap-aware totals make no statement about the remainder of the
109-component system.

## 5. Complete smaller-parent potentials and complete V/T rows

To display every row slot, keep the accepted two-chain parameters symbolic:

    q_C2(empty)=c_seed,
    q_C2(root bit i,root)=phi_i,
    q_C2(root bit i,full)=chi_i=1-c_seed-phi_i.

All are strictly positive. Do not confuse c_seed with the actual C4 full
complement c_i. The three-chain row is (2). The accepted three-fork F3,
with root r and two incomparable leaves, has

    q_F3(empty)=q_F3(root)=e,
    q_F3(each root-plus-leaf)=ell_i=e chi_i/phi_i,
    q_F3(full)=nu_i=1-2e-2ell_i>0.                        (8)

The two leaf choices both occur; their probabilities do not read the
selected leaf's mark by the accepted RI36 row formula. The symbol nu_i
in (8) is a three-fork complement, not RI127's H5 coefficient nu_xi.

Notation translation to the companion COUPLED_BOUND.md: this note's
phi_i, chi_i, ell_i, nu_i are respectively that note's f_seed(i), h_i,
phi_i, psi_i. Its ell_i instead names the V-mask1 probability. These
are notation aliases only, not additional identifications of components.

V has exactly the proper masks 0,1,3,7,9,11, followed by its full mask15.
For marks (i,u,v,w) at (r,a,b,x), the complete row is as follows. Every
alpha in the last column denotes the original global component of the
indicated local node; equal values of potentials alone do not identify
different alphas.

| V ideal | Locally retained bits | Positive potential u_V | Probability / global component statement |
|---|---|---|---|
| 0, empty | none | e^2/c_seed | alpha_[V,0] e^2/c_seed |
| 1, {r} | i | e^2/phi_i | alpha_[V,1,i] e^2/phi_i |
| 3, {r,a} | i,u | e ell_i/chi_i = e^2/phi_i | z_i, same global component as T mask1 |
| 7, {r,a,b} | i,u,v | A | 41p_i, component P_i |
| 9, {r,x} | i,w | ell_i | alpha_[V,9,i,w] ell_i; inherited value f_i |
| 11, {r,a,x} | i,u,w | nu_i | alpha_[V,11,i,u,w] nu_i; inherited value g_(i,u) |
| 15, full | all i,u,v,w | not a new proper potential | 1 minus the six displayed proper probabilities |

For example, masks 0,1,3 omit both V maxima b,x. Their two single
deletions are F3 and C3; the double deletion is C2. For mask3 the two
numerators are ell_i and e and the denominator is chi_i, giving the
displayed cancellation. Mask7 omits only x, giving C3-full A. Masks9
and11 omit only b, giving respectively the F3 pair and full probabilities.

T has exactly the proper masks 0,1,3,7,11 and full mask15. For marks
(i,u,v,w) at (r,a,b,x):

| T ideal | Locally retained bits | Positive potential u_T | Probability / global component statement |
|---|---|---|---|
| 0, empty | none | e^2/c_seed | alpha_[T,0] e^2/c_seed |
| 1, {r} | i | e^2/phi_i | z_i, same global component as V mask3 |
| 3, {r,a} | i,u | e^2/chi_i | alpha_[T,3,i,u] e^2/chi_i |
| 7, {r,a,b} | i,u,v | A | 41s_(i,u), component S_(i,u) |
| 11, {r,a,x} | i,u,w | A | 41s_(i,u), the same component again |
| 15, full | all i,u,v,w | not a new proper potential | 1 minus the five displayed proper probabilities |

Here both one-maximum deletions are C3 and the double deletion is C2;
the initial pair therefore has potential e^2/chi_i. Each complete arm
omits the other tip and has potential A. These formulas exhaust every
ideal: an ideal containing either tip contains r,a, while V's short leaf
can be included independently of an initial segment of its long arm.

RI151 section 6 separately proves the V value compressions q_V(9)=f_i
and q_V(11)=g_(i,u) using their complete marked component diamonds. The
former uses the symmetric two-arm terminal; the latter retains the
distinguished long-atom bit through a V/D4 diamond. They do not assert
g_(i,0)=g_(i,1). Their use here changes neither the row's full record cube
nor the list of its individual ideals.

The V/T tables are global-coordinate row expressions, not a Cartesian
product of separately selectable probabilities. In particular alpha_[V,0]
and alpha_[T,0] have not been identified merely because their potentials
match; any real component identification anywhere in the full law must
still be enforced. Other rows containing any listed global coordinate
remain binding. No unseen coordinate is silently assigned a new value.

## 6. The shared V-initial-pair / T-root component z_i

Use C3 again, now with the ordered precursor pairs (1,3) and (3,1).
A root birth first creates V, whose next birth above the old initial
pair reads local bits (i,u). An initial-pair birth first creates T, whose
next root birth reads i. Both old probabilities equal e, so

    e q_V(3;i,u) = e q_T(1;i),
    q_V(3;i,u) = q_T(1;i) = z_i>0.                       (9)

This is a component identification, not merely a row-normalization
coincidence. Its two potentials are both e^2/phi_i. If zeta_i denotes
the global coefficient, then

    z_i=zeta_i e^2/phi_i.

At fixed i, the two V selected-pair nodes indexed by u connect to the
single T singleton node. The old top bit v and both newborn bits vary
freely in these direct diamonds. Root i cannot change along any edge.

For completeness, this terminal has a stem r<a, two incomparable tips
above a, and a separate leaf above r. Deleting its separate leaf gives
T with a selected root; deleting either upper tip gives V with a selected
initial pair. These exhaust the maxima. The remaining pair of upper
tips leaves an F3 base and equal root-plus-leaf precursors, yielding
V-to-V instances and local-node loops. They neither add a different
parent role nor split the connected star already proved. They preserve
the same root bit. Thus (9) is one shared global variable per root in
every displayed V and T row, not a separate adjustable value per row.

The extra z-component proof does not add its diamonds to the 104 count
in section 4, which was explicitly confined to the six selected target
components.

## 7. Full-cube row transport without dropping marks

For each C4 selected slot, marks outside its precursor do not affect its
proper probability by strict locality. They still label the full row and
its actual full complement. For V and T, the identities (5),(6),(9) remove
specified *value* dependence only after retaining and comparing every
marked diamond. T's arm exchange transports the whole parent and marked
selected ideal simultaneously, including both individual arm occurrences.

Every natural labeling of V and T transports to the representatives used
above. The selected ideal masks change under that transport, and so do
their record coordinates; a numeric mask is not held fixed while its
parent is relabeled. Since the displayed roles exhaust all terminal
maxima and the diamonds retain all old/newborn bits, the results cover
all raw marked presentations, not just the all-zero representatives.

The root-bit sectors are structurally separated in every target family:
the terminal minimum is intrinsic and is in each selected precursor.
No record-flip symmetry is assumed for either the probabilities or their
global component coefficients.

## 8. Separately inherited actual root-only values

RI127 RECORD_TRANSPORT.md uses xi for the three ordered C3 stem bits
and proves, in section 3 equation (9),

    b_xi=b_0 if the root bit is 0,
    b_xi=b_1 if the root bit is 1.                       (10)

The proof uses accepted RI115 polynomial identities and RI122 complete
contrast patterns, together with positivity and the unchanged actual
strict-mixture identity p_xi=theta^6 b_xi^4/a^3. It is not a theorem
deduced solely from the three local graphs in this note. In particular,
we do not import (10) into arbitrary alternative component vectors.

The same source equations (6),(8), with nu_xi=theta^3 c_xi and theta>0,
prove root-only c_xi. RI151 section 6 records the accepted transport of
the remaining maximal chain bit for this full complement. These are
actual fixed-prefix identities valid even when the relevant full contrast
vanishes; no division by that contrast is introduced.

C4's complete normalization is

    w+p_i+s_(i,u)+b_(i,u,v)+c_i=1,                       (11)

where w=q_C4(empty) is record-independent by precursor locality.
Substitution of (10) into (11) gives

    s_(i,u)=1-w-p_i-b_i-c_i=:s_i                        (12)

for both values of u. Therefore every actual V/T arm expression in the
tables can be written as 41p_i or 41s_i, respectively, without asserting
that S_(i,0) and S_(i,1) are one graph component. Since C4's slot3 and
slot7 potentials are the fixed positive e and A, the corresponding
actual component coefficients likewise agree within each root sector;
their original global identities are nevertheless retained.

Equations (10)--(12) strengthen the bookkeeping compared with a projection
containing only the six selected representative rows. They do not establish
the requested cross-root contrast inequality, independent feasibility of
a changed vector, the unchanged actual maximum/scale comparison, W or H30.
The complete native matrix, all other marked rows, the pinned 109-vector,
and every later-layer canonical and maximum-derived constraint remain
outside any claim of new feasibility here.

## 9. Source boundary, literal reads and provenance

This manuscript applies the authenticated RI168 assignment and preserves
the RI166 conclusion that the earlier rational family was only a reduced
system counterexample. Its structural incidence is a new manual proof;
its stated actual-value equalities are explicitly inherited. Author-peer
checking is not independent acceptance.

The administrative authority read completely was:

- `/Volumes/AI_DATA/development/det-review-evidence/ri166-root-proof-outcomes-u3c1eicb/RI168_NATIVE_ASSIGNMENT.json`, 2875 bytes, SHA256 `a49d7c62a8a5c312a648b9962186dc6bc0af112b0ea4e1965ba7fd3268ff7710`.
- The same directory's `RI166_ROOT_ADJUDICATION.json`, 1261 bytes, SHA256 `635d33bda65c3aec4c75293694741b652977750d009575b5559793d863bb8dd7`.

Load-bearing literal mathematical sources, without following links into
their scientific certificate bodies:

- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_joint_growth_extension_v1/EXTENSION.md`, sections 2--4: complete labeled row sums, marked diamonds, positive two-chain and three-parent formulas; 18800 bytes, SHA256 `61423e355f508021f05cd941e5a0dbed62661c76ba750766583fd4b8c619e716`.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`, sections 1--3 and 5: held C3 row, maximal-deletion potential, exact local quotient, loops/parallel edges, individual ideal sums and global components; 16243 bytes, SHA256 `567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8`.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`, section 2: retained complete marked local-component convention; 17102 bytes, SHA256 `e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/COMPONENT_CONTRASTS.md`, terminal/root invariants; 19001 bytes, SHA256 `b982477d162bce2210aabaffe91cc68e52315734c186d2895e67da4736c9a49f`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri155-strict-capacity-proof-jv0xliup/CAPACITY_STRUCTURE.md`, sections 3--4: marked factor-41 transports and the two separate T arms; 15579 bytes, SHA256 `54fa9b1e421520527a2403e20d0e243f257bdc8ef244e945200e4a652ab3d936`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/RECORD_TRANSPORT.md`, sections 2--3 and 5: inherited b/c transport and its exact premises; 15418 bytes, SHA256 `ee55be354336e7262fa1cf6efccec270f46a8276ea63dd04fef7ead2606a259e`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri151-canonical-q-equalities-_546ie2h/NEUTRAL_COMPONENT_INCIDENCE.md`, section 6: the V9/V11 component identities and inherited full-complement transport; 22869 bytes, SHA256 `dccd56286e012010fd4775eff5b1bb355312e4af12975e73bb8361bb85873495`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri166-native-contrast-gap-2j9ykuoq/CONTRAST_COUPLING.md`, terminal separation and precise unrecovered global coupling; 11920 bytes, SHA256 `cfb1c64f3e9d8caa28427cf9a6acb993d85d52bec5e4d7f8458c4da43273fd51`.

The RI36/41/63, RI147 and RI155 texts were read completely in the immediately
preceding author work and their stated sections were retained here. Fresh
complete RI168 reads include the assignment/decision (`96931f`), RI166
coupling (`d138ce`), RI151 incidence (`d730df`,`e5144d`), and RI127 record
transport (`399bc0`,`a4afa1`), all command exit 0. Additional literal
rereads were `7da0e7`, `29bc95`, `f94bab`; they are text reads, not source
execution. Authority byte/hash checks were `facc9e`,`ac4548`; the final
three-manuscript metadata checks were `8deb5a`,`9e02fe`, all exit 0.

No scientific JSON body, actual coefficient vector or new numerical
probability was decoded or evaluated. No subject/helper import, compilation,
AST construction, probe, engine, graph enumeration, runtime capture, fixture,
active card, repository/index/Git operation or predecessor edit occurred.
Only this new external Markdown manuscript is written. RET remains paused;
no geometry/gravity or physical acceptance follows.
