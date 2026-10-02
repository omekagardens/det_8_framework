> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Kappa is first in the original joint sector order

1 October 2026, OBSCURED-LOCATION. RI268 manual author result pending independent
adjudication. Kappa_i is earlier in the ORIGINAL component sequence than
all ten other coordinates permitted to vary in RI266's joint sector block.

The previously missing Q bound is proved by an exhaustive manual table:
its minimum relation code is 8988. The candidate example attains this
value, but the example alone was only an upper bound. Every other
topological order, every parent presentation and every record marking
is covered below. No graph enumeration engine or original index lookup
is used.

## Actual key and complete parent presentations

The unchanged five-carrier key is the triple

    (E_5(parent,pi), selected_ideal_mask, selected_record_mask),

    E_5(parent,pi)=sum_(u<v in the strict order)
                                  2^(5*pi(u)+pi(v)),    (O1)

where pi labels vertices by 0,1,2,3,4. The sum uses ALL strict
relations, including transitive ones, not only covers. Component
roots minimize this triple over every node/presentation in the
component and every carrier permutation. The original coordinate
sequence sorts these complete triples lexicographically.

The accepted RI248 CANONICAL_BINDING section 2 uses the
topological-minimum lemma: the minimum first coordinate over all
permutations is attained at a topological labeling. Its inversion
argument chooses the greatest-labeled source with a backward relation,
swaps it with a lower descendant and strictly lowers the highest
changed outgoing-bit block; lower blocks cannot compensate.
We retain that admitted lemma and convention, not a new key.

Thus an exhaustive topological minimum is a lower bound for EVERY
permutation. Marking and selected-ideal masks can decide a tie in
E_5, but cannot overcome a strict difference in its first coordinate.

The accepted exhaustive component inventory in RI266 is

| Original coordinates | Every carrying parent |
| --- | --- |
| kappa_i | Y and P |
| tau_i | P_tau and P |
| nu_(i,0), nu_(i,1) | P and P_nu |
| eta_(i,0), eta_(i,1) | P_tau and Q |
| four xi_(i,l,m) | P_tau and P_nu |
| sigma_i | P_tau and V5 |

These are exhaustive because each component terminal has exactly
two maxima, every parent presentation deletes one of them, and
component paths preserve that terminal. Compulsory marked vertices
distinguish the coordinates. No third presentation, hidden
identification or record flip is being inferred away.

## Complete manual Q calculation

The parent Q has covers r<a<z, o<z, r<x and o<x. Its complete
strict relation set is

    {(r,a),(r,z),(a,z),(o,z),(r,x),(o,x)}.               (O2)

Initially only r and o are minimal. If r is first, its next vertex
is a or o. After r,a, the next vertex must be o, followed by x,z
in either order. After r,o, the remaining vertices a,x,z have only
a<z, so there are exactly three orders. If o is first, r is forced
second, followed by the same three a,x,z orders. This exhausts
five r-first and three o-first topological orders.

The following table lists ALL eight. Labels are their positions
0 through 4. The sum column uses the six relations in O2.

| Vertex order | Relation-bit sum or rigorous lower bound | E_5 |
| --- | --- | ---: |
| r,a,o,x,z | 2+16+512+16384+8+8192 | 25114 |
| r,a,o,z,x | 2+8+256+8192+16+16384 | 24858 |
| r,o,a,x,z | 4+16+16384+512+8+256 | 17180 |
| r,o,a,z,x | 4+8+8192+256+16+512 | 8988 |
| r,o,x,a,z | a at 3 precedes z at 4, giving 2^19 alone | >=2^19 |
| o,r,a,x,z | 128+512+16384+16+256+8 | 17304 |
| o,r,a,z,x | 128+256+8192+8+512+16 | 9112 |
| o,r,x,a,z | a at 3 precedes z at 4, giving 2^19 alone | >=2^19 |

Every entry other than 8988 is strictly larger. In particular
2^19>8988. The order r,o,a,z,x attains 8988, so, using the
topological-minimum lemma,

    min_(ALL carrier permutations) E_5(Q)=8988>8590.   (O3)

No test of a single convenient representative establishes O3:
both the exhaustive branching argument and the table are needed.
Q's whole record, selected ideal and both newborn histories remain.
The minimized relation code is an unmarked parent invariant; whatever
those retained masks are, every Q presentation has first key coordinate
at least 8988.

## Trace every other parent bound

RI248 CANONICAL_BINDING proves the original kappa roots

    root(kappa_i)=(8590,17,i),                         (O4)

using Y=C4 disjoint an isolate: its minimum is 8590 with the
isolate last, 17046 with the isolate immediately before the chain's
last vertex, and at least 2^19 in the other three positions.
The P presentation has larger minimum 8730, so cannot lower O4.
All optional Y records are connected at fixed compulsory i,
giving the displayed minimum selected-record mask. No canonical
coefficient value follows from that key.

The same accepted source exhausts P's nine topological orders
and P_tau's seven, proving their exact minima 8730 and 8604.
These are whole-parent permutation minima, not minima for an
unproved selected-record representative.

For P_nu and V5, the unique top lies above ALL four other vertices.
In every topological labeling it has label 4, while label 3
precedes it. That single relation contributes 2^(5*3+4)=2^19.
The topological-minimum lemma extends the lower bound to the
minimum over all permutations. Both parents therefore have
minimum first coordinate at least 2^19>8590. This uses no
chosen old record, selected ideal or original component index.

Combining every presentation in each component gives

| Coordinate group other than kappa | Lower bounds from ALL presentations | Component first coordinate is at least |
| --- | --- | ---: |
| tau_i | P_tau:8604; P:8730 | 8604 |
| both nu_(i,j) | P:8730; P_nu:2^19 | 8730 |
| both eta_(i,l) | P_tau:8604; Q:8988 | 8604 |
| all four xi_(i,l,m) | P_tau:8604; P_nu:2^19 | 8604 |
| sigma_i | P_tau:8604; V5:2^19 | 8604 |

A component's restricted set of selected nodes can only INCREASE
a parent lower bound. It cannot produce a lower relation code than
the minimum over all labelings of that parent. Thus the table is
valid for every compulsory i,j,l,m assignment, every optional mark,
every selected-ideal mask and every original parent presentation.
It does not assume that each component attains its listed bound.

Every one of these ten coordinates has first key coordinate
strictly greater than 8590. Hence

    kappa_i precedes tau_i, both nu, both eta,
                     all four xi and sigma_i.          (O5)

This proves only the necessary first-coordinate ordering. The
relative order of the remaining ten is neither guessed nor needed.
Coordinates elsewhere in the ORIGINAL full vector, including
other-sector kappa or mu, may occur earlier or between them but
are fixed in the same-rest block.

## Exact meaning of earliest changing coordinate

O5 says kappa is the earliest coordinate ALLOWED to vary in this
eleven-coordinate block. If two feasible block vectors have different
kappas, all earlier original entries are fixed and equal. Their
first actual difference is therefore kappa, and the smaller kappa
is lexicographically smaller, regardless of every later change.

If two vectors have equal kappas, their first actual difference
may be one of the later ten. O5 does not impose a new order on
that tie. The full original sequential selector must continue.
This distinction includes a zero or constant kappa across an
entire feasible/optimal face.

The companion note applies this complete order to RI266's already
accepted compact primary-optimal image. No actual rank, coefficient,
cap, support, vector, H or dual z has been acquired or reconstructed.
