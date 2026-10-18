# RI248 Canonical component binding and remaining decision

1 October 2026, Honolulu. Manual author proof and proposed source design,
pending independent review. This note binds the two kappa roles to the
original whole-parent components and canonical primary/lex selector.
It does not acquire their values or authorize a scientific-body read.

The companion note resolves the actual exchange comparison L_i=0<T_i,
derives the complete P_tau row, and proves the remaining tight-capacity
and dual-weight obstruction. A bound kappa0-kappa1<=1/70 has not
been proved. The corresponding C_b decision therefore remains open.

## 1 Complete original kappa component

Keep the accepted two parent presentations

    P: r<a<b, r<x, o<x,       selected {r,a,b},
    Y: r<a<b<c, o isolated,   selected {r,o}.

Their common six-event terminal is

    r<a<b<c, r<x, o<x,

with maxima c,x. Deleting either maximum gives exactly P or Y;
every component edge preserves that terminal, so no other parent
presentation can enter the component.

The compulsory intersection of maximal pasts is {r}. Its bit i is
retained. At each fixed i the accepted complete marked diamond connects
all four P optional (a,b) assignments to both Y optional o assignments.
Both newborn bits and all unselected whole records remain. The terminal
distinguishes r from o, so the two root-bit components are distinct.

The canonical coefficient of this existing component is kappa_i.
It is not its ideal probability or actual strict-mixture coefficient:

    q_can(P,{r,a,b})=(41/352)kappa_i,
    q_can(Y,{r,o})=(1/64)kappa_i.

The target is alpha^min itself. A strict-law probability would instead
include the unchanged (35/36) canonical weight and theta restoration;
it must not be substituted for kappa without that complete identity.

## 2 Five-carrier minimum relation keys

Use the unchanged transported relation-bit key on five vertices:

    E_5(P)=sum_(v<w in the order) 2^(5*pi(v)+pi(w)),
    S_m=sum_(v in S)2^pi(v),
    R_m=sum_(v in S with mark1)2^pi(v).

Here v<w means the strict order relation, not a presumed initial label
order. Component roots minimize the triple over all carrier permutations
and all nodes in the complete component.

RI189's topological-minimum argument applies with blocks of width 5:
if a source k has a backward relation, choose the greatest such k and
swap it with a lower-labeled descendant h. All rows above k have no
relation to either vertex. Row k becomes a strict subset of its old
outgoing row, losing at least one bit; all lower binary blocks cannot
compensate. Thus every minimizer is topological. No permutation engine
is used here.

For Y, place the isolate in each of the five positions relative to
its ordered chain. With the isolate last, order(r,a,b,c,o),

    E_5(Y)=2+4+8+128+256+8192=8590.

If the isolate is immediately before c, the sum is 17046. In each
earlier position, the chain's penultimate vertex has label 3 and
precedes label 4, contributing 2^19 by itself. All exceed 8590.
The minimizing Y selected ideal has mask 17 and selected-record mask
i+16*l. Both l values belong to the proved component, so its minimum
mark mask is i.

For P there are nine topological orders. The following six avoid a
source3-to-target4 contribution:

| Vertex order | E_5 |
| --- | ---: |
| r,a,o,x,b | 8730 |
| r,o,a,b,x | 8732 |
| o,r,a,b,x | 9104 |
| r,a,o,b,x | 16666 |
| r,o,a,x,b | 16668 |
| o,r,a,x,b | 17288 |

For example the first sum is 2+16+8+512+8192=8730. The remaining
orders(r,a,b,o,x), (r,o,x,a,b), (o,r,x,a,b) each contribute
2^19 or more. This exhausts the six r-first and three o-first orders.
Therefore P's minimum 8730 is above Y's 8590.

The exact component roots in this original relation-bit convention are

    root(kappa0)=(8590,17,0),
    root(kappa1)=(8590,17,1).                              (K1)

There is no integer triple strictly between these two, so their sorted
component ranks are consecutive. The first rank is NOT determined here.
Consecutive ranks do not imply any ordering of their numerical values.

For completeness the same argument fixes the tau order relevant to
the two-coordinate exchange. The other parent P_tau has seven
topological orders. Its minimum is at(r,o,x,y,a):

    E_5(P_tau)=4+8+16+128+256+8192=8604.

The other three orders without a source3-to-target4 bit give
9100,17052,17300; the other three have at least 2^19. The P
presentation has minimum 8730. The P_tau selected ideal {r,a}
has mask 17, and its optional a bit is transported by the accepted
tau diamond. Hence

    root(tau_i)=(8604,17,i).                              (K2)

Thus kappa_i precedes tau_i in the actual component order. This is a
manual structural key proof, not an original vector-index lookup.

## 3 Preserve the actual primary and sequential selector

RI63's accepted complete problem is

    minimize Phi=B5+beta^T alpha,
    alpha>=0,    A alpha<=1,

with every original ideal occurrence, actual history weights and complete
component matrix. Its canonical answer alpha^min is the sequential
lexicographic minimizer of that primary optimal face. The primary
optimum alone is not unique.

The primary certificates use z>=0, beta+A^T z>=0 and matching primal
and dual objectives. At each positive canonical coordinate, all earlier
coordinates are fixed at their already selected canonical values.
The accepted remaining-column inequalities and forced-tight equalities
then certify the next coordinate's lower bound. None of those earlier
bindings is replaced by a local choice here.

For RI240's two-coordinate direction, K1–K2 identify the earliest change
as a DECREASE of kappa_i. A feasible zero-primary-cost direction with
only those two coordinates would therefore be a lexicographic descent.
But the newly proved L_i=0<T_i makes its primary cost strictly negative
whenever the full companion row permits the move. There is no unresolved
primary-equality branch for that particular direction.

A compensation changing eta,xi,sigma or other coordinates is a DIFFERENT
direction. It must satisfy every affected P/Y/companion constraint, the
whole objective, and the actual earliest-change test on ALL its changed
coordinates. The ordering of only kappa and tau is not a certificate
for such a direction. No local refit or alternate primary optimum is
substituted for the canonical answer.

## 4 Exact remaining comparison and minimal two-value target

The accepted RI240 theorem gives the sufficient comparison

    kappa0-kappa1<=1/70  =>  C_b<0,

equivalently M1-M0<=41/24640, with the stronger simple bound
M1-M0<=1/625 also sufficient. Equality is retained in those bounds.
Together with accepted d=0!=d7, such a result would establish
inconsistency of this fixed normalized system.

The complete companion derivation has now removed unknown T_i/L_i
comparison from this route. It leaves the actual coupled cap

    kappa_i>0 =>
    tau_i=[1-max_(l,m)
       (h_(i,l)eta_(i,l)+n_(i,l)xi_(i,l,m)
                              +s_(i,l,m)sigma_i)]/p_i,

and a strictly positive required sum of primary dual weights on those
companion rows. Nothing in this packet determines the residual
allocations or proves that cap incompatible with positive kappa.

A minimal direct data target for the displayed sufficient comparison
is therefore the TWO existing canonical coordinates at K1, with their
original rank and selector binding. This is minimal in requested roles
for that test, not an information-theoretic minimality theorem or a claim
that those values always decide C_b. If their difference is larger than
1/70, that sufficient test fails; C_b=0 is not thereby established.

No further RI41 coefficient acquisition, full canonical vector, complete
companion residual table, new amplitude or global reoptimization is
needed merely to perform that two-value comparison once exact binding
has been supplied. None is authorized here.

## 5 Proposed source and explicit index-binding gap

The admitted RI63 COMPLETION.md identifies its original final certificate
at

    /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/CERTIFICATE.json
    expected SHA256 f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b

The expected hash is from the already admitted analytic source, not a
fresh scientific-body read. Metadata-only receipt 226790 exit0 observed
a regular, normalized, no-symlink original path of 19805 bytes, with
stable lstat fields. It neither opened the file nor computed its hash.
Those combined expected path/length/hash fields are a PROPOSED pin;
the body's current whole-byte identity has not been authenticated.

An authenticated read of the inherited administrative manifest in aa1f5c
did not locate a row at this exact certificate path. No manifest
descendant or any of its 423 referenced files was opened for that
lookup. The proposed pin therefore is explicitly not misrepresented
as an inherited authenticated body identity.

COMPLETION establishes that the certificate has a canonical primal,
primary dual, sequential optimal-face evidence and a distinct alternative
primary optimum. Its text does not supply the selected original ranks
or a literal root-to-primal-index table for K1. This note does NOT
assert that the original body prints such a table.

The precise unresolved source-binding gap is:

    (8590,17,i) as an original component
       -> its original rank in the full 798-component order
       -> that rank's entry in the canonical alpha^min,
          not the alternative primary solution or strict mixture.

The source's known example about coordinate 109 cannot be assigned to
kappa merely because it has a tempting numerical value. No index or
sparse-zero convention is guessed.

## 6 Proposed bounded acquisition design only

A new root-issued admission would have to name the proposed original
pin above, the two K1 keys, the canonical selector and permitted literal
binding evidence. The closed RI246 authority supplies none of this.

The proposed sequence is:

1. Root independently accepts the structural K1 binding and verifies
   the original five-carrier relation-key convention. Root then issues
   a separately pinned admission specifying exact readers and scope.
2. Under that NEW authority only, require normalized no-symlink path,
   regular file, exact whole length/hash and stable path/descriptor
   state before and after a complete bounded literal display. Use
   O_NOFOLLOW and preserve the genuine untruncated receipt. No source
   repair, alternate copy or regeneration is permitted.
3. Manually locate the original root-to-rank binding for both K1 keys,
   if it is supplied. Count ORIGINAL indices without filtering or
   sorting, prove uniqueness, and retain the consecutive-rank check.
   If the body provides only a root-list hash or otherwise lacks that
   binding, STOP with GAP-INDEX. Do not infer ranks from numerical
   vector order or execute a reconstruction.
4. Bind those exact ranks to the primal selected by the COMPLETE
   primary plus sequential lexicographic certificate. Do not select
   the separately supplied alternative primary optimum. If any sparse
   representation is used, absence means zero ONLY under an explicitly
   admitted original schema rule; otherwise STOP with GAP-SCHEMA.
5. Transcribe only the two canonical coefficient strings and their
   exact provenance. Manually compare kappa0-kappa1 with 1/70.
   A result <=1/70 supplies the accepted sufficient C_b<0 theorem.
   A larger result leaves C_b unresolved; it does not prove equality.
6. A nonauthor independently verifies custody, whole-parent/record keys,
   original indices, canonical-versus-alternative selection, rational
   transcription and the exact comparison before root adjudication.

If GAP-INDEX or GAP-SCHEMA occurs, root would need to identify and
separately admit existing binding evidence. This packet does not invent
its path, assert it exists, authorize an executor or broaden the two
scientific-value target. An acquisition design is not an issued admission
and its possible success is not a present result.

## 7 Original normalized system and recovery

Keep all ten unknowns u0,u3,U4,...,U11 and

    u2=-1,
    W1=-Gamma_10 u0+Gamma_12-Gamma_13 u3,
    W2=Gamma2>0,    W3=-Gamma3 u3,    Wj=Uj for j>=4.

The five original complete forms are

    l1=(theta^3 b^3/a^2)W1+3theta^2 c W2+3j W3,
    l2=(theta^2 b^2/a)W2+theta^2 c W4
                                  +theta c W5+j W6+ell W7,
    l3=(theta b^2/a)W3+2theta c W6+j W8,
    l4=theta^2 b W4+theta^2 c W9+2ell W10,
    l5=theta b W7+theta c W10+ell W11.

All thirteen equations remain

    g_p(0)l_p(1;W)-g_p(1)l_p(0;W)=0, p=1,...,5,
    U_j[f_j(1)-f_j(0)]=0, j=4,...,11.

Their complete original recovery remains

    delta v1=beta_10 u0-beta_12+beta_13 u3,
    delta v2=-beta2,    delta v3=beta3 u3,
    delta vj=-Uj/f_j(0), j>=4,
    delta d_p=-rho*l_p(0;W)/(e_Cp*g_p(0)),
    delta y_Jj=Wj/e_j.

Proper-child variations are u0,u2,u3 themselves. Every denominator is
an inherited positive reference. Gamma/beta/T1/T2/T3, actual canonical
g1/g2 offsets, full-slot corrections, all records and labeled ideals,
both newborn bits and original strict endpoints remain. RI233 supplies
complete transport. The accepted U4=U5=U6=0 consequence does not
remove original coordinates or equations.

RI246's N_i=0 is retained analytically, not reacquired, and does not
erase kappa or other canonical terms. No full normalized witness,
signed inconsistency, improvement, optimality or new amplitude is
claimed in this packet.

## 8 Scope and stop

The new results are the complete marked companion row, exact strictly
favorable weighted exchange, forced tightness and primary dual weight,
plus structural component/selector binding and a proposed two-value
source design with explicit index/schema failure conditions.

No original scientific body was opened or hashed; the one fresh
candidate-file operation was metadata-only lstat/path inspection.
No new coordinate, scientific JSON, vector, graph/LP, automatic
mathematics, subject runtime, measurement/RET, repo/Git/index or
publication work occurred. All 15 inherited boundary objects and the 423
manifest remain; the RI246 literal exception is preserved as CLOSED
historical provenance. Option B and Status M remain unchanged.
No all-size, full-QM, geometry, mass or gravity claim is made.
Stop at handoff for independent root review; no successor is assigned.
