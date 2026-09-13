# QR-05: bounded exact joint-geometry verification contract

12 September 2026. Prospective contract: freeze all sources before the first
mathematical execution. This is the executable follow-up to the
[joint design](../qr-05-joint-geometry-design-2026-09-12/README.md), not a new
physical law, calibrated acquisition, ontology or gravity-dynamics claim.

## Fixed mathematical scope

Use exactly the [protocol](protocol.json) and all 64 worlds in Cartesian
product order κ=[1,2], ε=[−1,1], a=[0,1], b=[0,1], L=[1,3/2], r=[1,2/3].
IDs w000 through w063 are verifier labels, never channel inputs.

The supplied model on Q=(0,1)^2 is g=L(1+ax)diag(−1,κ²), with sampling
intensity per proper area r(1+bx). Proper-area polynomial coefficients are
[κL,κLa]; coordinate intensity coefficients are
κLr[1,a+b,ab]. For Z=1+(a+b)/2+ab/3, normalized point-density coefficients
are [1,a+b,ab]/Z. Probe A=(1/8,1/8), B=(7/8,1/8), C=(7/8,5/8) give
O=[χ(A,B),χ(A,C)]. Strict chronological equality is excluded.

Channels are O (two signed comparisons), P (normalized probability x<1/2),
T (total-count Poisson mean only), D=b and R=r. They are distinct information
types, not five guaranteed instruments. The full marked count law supplies
both P and T and is NOT the T-only channel. The target is the complete
geometric dictionary {O,relative_volume,volume}, with
relative_volume=(1/2+a/8)/(1+a/2), volume=κL(1+a/2).

The continuous-class proof remains in the design. This computation verifies
only the fixed rational subclass. Expected global census: 16 targets, 32
menus, exactly one identifying menu (all five channels), and 1,920
different-target unordered pairs. Nonidentifying menus can still contain
some target-constant fibers.

No Poisson samples, count-tail enumeration, field/operator integration,
empirical calibration, arbitrary metric inference or old branch engines run.
The Fisher matrix is checked algebraically as T[[1,1],[1,1]], conditional on
κ,a,b, before the density reference; it is not spacetime curvature.

## Independent routes

Primary: integrate explicit coefficient polynomials; use signed slope
inequalities for chronology; group native observations into fibers.
Reference: integrate the quadratic product by exact Simpson values and the
affine proper measure by endpoint trapezoids; use the quadratic metric sign
and time orientation; decide identification using every differing-target
pair's channel separators and build fibers from an equivalence relation.

Both independently enumerate worlds and produce the complete native report.
They must not import one another or a shared mathematical helper. The study
driver provides source-bound orchestration only. Tests additionally compare
the finite partition report with the previously frozen generic quotient
utility using explicitly injective per-channel/per-target finite alphabets.
Original rational values are always retained and compared before encoding;
verifier IDs and target data cannot be used as observation encodings.

## Pure engine API and exact native report

Both primary.py and reference.py expose:

- evaluate(world): validate and return a row WITHOUT id for one world.
- recover(channels): validate the five-channel tuple and return its recovered
  world, or raise ValueError if outside the model image.
- chronological(kappa,orientation,left,right): signed strict comparison,
  with each point a two-Fraction plain list inside the closed unit square.
- analyze(): enumerate only the fixed 64-world protocol domain and return
  the complete report. No arguments, I/O, random state or caches.

world is exactly a plain dict with keys kappa,orientation,a,b,L,r.
The first four are plain ints in the stated binary sets; L,r are positive
plain Fraction values, with numerator/denominator bit lengths at most 128.
evaluate and recover allow positive rational L,r beyond the finite catalogue;
this permits the named compensation control, not a new fixture sweep.
Point coordinates are plain Fractions in [0,1] with the same bit bound.
Booleans, floats, integer-for-Fraction substitutions, subclasses, extra or
missing fields and malformed dimensions raise ValueError. No coercion is
allowed. Functions do not mutate inputs or return aliased mutable input data.
evaluate also refuses if its derived channel tuple or recovered world exceeds
the 128-bit bound. Individually bounded L and r can have an oversized product;
the public utility is not promised to return a row for every such input.

channels is exactly a plain dict O,P,T,D,R. O is a two-plain-int list
of one of the four valid signed probe outputs; P,T,R are plain Fractions,
P∈{1/2,5/12,19/56}, T,R>0 with the same input bit bound; D is plain int0/1.
A P,D combination requiring a outside {0,1} is refused. A valid image can
recover any positive rational L; recovery must recheck the world bound and
round-trip the supplied channels, or refuse if that output exceeds the
128-bit API bound.

An evaluate row has EXACT keys:

- world: a fresh copy of the validated six-coordinate world.
- channels: the native five-channel dict.
- target: {O:[int,int],relative_volume:Fraction,volume:Fraction}.
- geometry_coefficients: two Fractions, increasing polynomial degree.
- intensity_coefficients: three Fractions, increasing polynomial degree.
- point_density_coefficients: three Fractions, increasing degree.
- Z: Fraction.
- recovered: recover(channels), containing all six coordinates.
- fisher: 2×2 plain list of Fraction entries, each equal to T.

The report has EXACT keys schema,channels,worlds,partitions,
minimal_identifying_sets,minimum_size,minimum_identifying_sets,
obstructions,omission_witnesses,collision_groups.
schema is qr05-joint-geometry-report-v1; channels is [O,P,T,D,R].
Each worlds entry adds id to the evaluate row above, in fixed product order.

partitions enumerates all subsets in increasing cardinality then input-channel
index order. Each row is {selected,blocks,targets,identifying}. blocks are
world-ID lists in first-world order and within-block world order. targets
is a list, one entry per block, of distinct complete target dictionaries
in first-world order. identifying is true iff every block has exactly one
target. No target ambiguity information is suppressed.

minimal_identifying_sets lists all inclusion-minimal globally identifying
subsets in menu order; minimum_size is [] if impossible else [k]; and
minimum_identifying_sets lists all globally identifying sets of least size.

obstructions contains EVERY different-target unordered pair in input-world
pair order, as {worlds:[id1,id2],separators:[channel names in input order]}.
Empty separator lists must be retained if present.

omission_witnesses are in channel order, each {omitted,worlds:[leftID,rightID]}.
Fix κ=1, ε=+1 except the O flip; tuples below are (a,b,L,r):
O: same(0,0,1,1), orientations +1 then−1;
P: (0,0,3/2,1) then(1,0,1,1);
T: (0,0,1,1) then(0,0,3/2,1);
D: (1,0,1,1) then(0,1,1,1);
R: (0,0,1,1) then(0,0,3/2,2/3).

collision_groups is one row per κ,ε in product order, with keys
kappa,orientation,worlds. In each group enumerate shape pairs (a,b)=(1,0),
then(0,1); within each choose (L,r)=(1,1),then(3/2,2/3).
All four worlds must have identical intensity coefficients, point-density
coefficients and O,P,T while their complete geometric targets differ.

## Tests and evidence discipline

Tests cover complete primary/reference/native/quotient agreement, fixed
domain/target/pair census, all menu refinements and fiber target sets,
five omitted-channel witnesses, four simultaneous collision groups, known
integrals, probe signs, reversal/incomparable/equal/null controls, recovered
worlds, scale compensation c=3/2, Fisher null and repetitions m=1,3,
inclusive 128-bit acceptance and overflow refusals, native type/mutation/
aliasing controls, and full freeze/capture lifecycle.

The null probe pair is (1/4,1/4),(3/4,3/4): κ=1 yields a null tie;
κ=2 yields spacelike separation. Neither is strict chronology. Tests may
use named malformed inputs and proof controls, but not a parameter search.
The scale control applies to the fixed 64 worlds; multiplying L by c and
dividing r by c must preserve record intensity and O,P,T,D while volume
multiplies by c. No quantum executor is needed for the design's linearity
argument, and no numerical CQ verification is claimed in this gate.

Freeze TEN sources: this README, protocol.json, primary.py, reference.py,
study.py, test_joint_geometry.py, the two prior design documents, the literal
BM evidence-utility source and the literal frozen reconciliation calculus.py.
The previous source freezes/captures remain unchanged. Publication RESULTS
and verification logs are not prospective mathematical inputs.

The utility bytes must be bounded/regular and literal-SHA verified before
execution; only evidence helpers may be used. Protocol/design/quotient pins
are checked before new engine execution. Captures and replays authenticate
source identities and freeze bytes before analysis, recheck them afterward,
and publish by exclusive create with readback. Full native Fraction/list/int/
bool distinctions are checked before and after canonical serialization.

Limits: 30 seconds per full analysis, 60 seconds per test suite, 262,144 bytes
per source, 16,777,216 per artifact, one alternate-runtime full replay.
Sequence: static review and formatting; source freeze; FIRST capture; normal
and optimized suites; both full replays; one Python3.11 full replay.
No post-first-run source tuning: preserve failures and use a separately named
revision if an implementation repair becomes necessary.
