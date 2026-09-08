# QR-05AJ: additive cell-pair geometry across scales

7 September 2026. Research after pushed AI commit
`e77482fccb3d72ab21f1b50ebbb4aee632a7831d`.
The [prospective protocol](README.md) specifies the fixtures, exact output,
incorrect weighting candidates and verification before fixed AJ computation.

The gate is complete. Both independent engines agree exactly on all five
families, 3,725 directed level-pair rows and 3,025 parent-pair blocks. Every
complete child-block measure matches its parent; all 900 direct l0-to-l2
blocks also match the reconstructed route through l1. Geometrically weighted
conditional fractions agree wherever defined. Uniform and stale-mark weighting
do not generally preserve them.

## What is being represented

For a supplied rectangular probe Q, let h_A be the volume of cell A clipped
to Q and J_AB the measure of ordered causal point pairs in the two clipped
cells. This is a two-point geometric measure, not a Boolean relation between
cell representatives. It includes distinct points inside the same region.

Finite additivity gives an immediate general identity for disjoint measurable
child partitions, up to zero-measure boundaries:

    J_AB = sum_(a child of A,b child of B) J_ab.

The identity follows by splitting the integration domain into the Cartesian
child blocks. The executable gate checks that the specified rectangle calculus,
lineage implementation and complete retained data actually obey it; it does
not discover a new physical law or establish a continuum limit.

For positive h_A*h_B, define C_AB=J_AB/(h_A*h_B). Then

    C_AB = sum_ab [h_a*h_b/(h_A*h_B)] C_ab.

These are conditional fractions for independently drawn points in specified
regions. Product-volume weights follow from the measure. Zero-volume child
pairs have zero weight, while their conditional fractions remain undefined.
If the entire parent product vanishes, the parent fraction is also undefined.
Uniform averaging and annotation-derived weights are different constructions.

## Why exact pair aggregation is useful but not sufficient

AI showed that exact local volumes can coexist with an incorrect
representative-chain pair coefficient. Retaining J_AB supplies the additional
two-point information that a single representative omits. It can be aggregated
without inventing a causal order between region labels or authenticating
supplied volume annotations.

This provides a concrete scale-consistent geometric data structure. Its cost
is that the geometry and pair information must be supplied or separately
estimated; pair consistency does not reconstruct either from a bare record.
The implementation is a private diagnostic, not a hardened RET SDK interface.

With the AI coefficient convention, summing these supplied pair integrals and
dividing by8 gives V^2/32 exactly on the declared flat rectangular probes.
That follows from the complete integral, not from representative order or a
new derivation of the scalar propagation law. It does not certify composition
of the resulting pair table into higher coefficients.

## Fixed comparisons and failure witnesses

The selected data are the fifteen identity-design sources already retained
in AI: five families, three levels of6,7,8 cells, and five probes. No masks
are enumerated here. Parentage is derived from full-rectangle containment,
with disjointness and local coverage checks before clipping; event IDs are
explicitly local to their levels.

The 3,025 blocks contain 4,425 ordered child terms. Of those blocks, 1,030
have positive parent volume products and defined conditional fractions;
1,995 have zero products and retain null fractions. Among the 3,725 level
pair rows, 2,435 have undefined fractions. Raw integrals are still explicitly
zero on those zero-volume products. No null is filled with an invented zero
conditional probability.

| Family | Blocks | Uniform-weight disagreements | Annotation-weight disagreements |
| --- | ---: | ---: | ---: |
| Grid | 605 | 5 | 0 |
| Warp | 605 | 16 | 0 |
| Warp with stale marks | 605 | 16 | 16 |
| Boost | 605 | 5 | 0 |
| Dilation | 605 | 5 | 0 |
| Total | 3,025 | 47 | 16 |

These are repeated family/link/probe/block contexts, not independent trials
or empirical failure rates. Boost and dilation repeat the grid's conditional
fractions; stale warp repeats the warp's true geometry. The annotation
candidate uses s_a=w_a*h_a/g_a followed by normalized s_a*s_b weights. It is
this particular clipped-annotation heuristic that is tested, not every
possible use of marks.

### Within-child and same-parent cross-child pairs both matter

For the grid whole probe, l0-to-l1 parent block(2,2), the coarse measure is

    J_22 = 1/576 = 1/1152 within-child + 1/1152 cross-child.

The four child fractions are1/4,1/2,0,1/4 with equal product weights1/4.
Dropping either half of the integral gives the wrong parent value. For the
same parent through l2, the split becomes1/1536 within-child plus5/4608
cross-child; the total remains1/576. Both direct and via-middle conditionals
remain1/4. Region-diagonal measure is not a self-causal event.

Across all blocks, omitting child diagonals changes240 values. Omitting all
off-diagonal child terms changes375:45 are same-parent blocks and330 are
distinct-parent blocks. The latter count must not be described as375
within-parent failures. Every omitted-term candidate and unchanged value
remains in the complete retained wire.

### Clipped geometric weights cannot be replaced by uniform averaging

For grid lower_unaligned, l1-to-l2 block(1,2), the two child fractions are
5/16 and13/16. Their clipped product weights are5/8 and3/8, giving

    (5/8)(5/16) + (3/8)(13/16) = 1/2.

The arithmetic mean is9/16 instead. The raw child measure correctly sums to
the parent1/900. This is an exact deterministic weighting discrepancy, not
measurement noise or a changed physical observable.

### Stale marks can preserve support while changing the conditional answer

For warp whole, l0-to-l1 block(2,7), child fractions19/24 and7/24 have true
product weights5/12 and7/12. Their geometric combination is1/2, with raw
integral1/384. On the identical warp geometry with stale marks, the annotation
weights become1/2 and1/2, giving13/24. Both child terms remain supported;
positive weights alone do not make the weighting geometric.

The complete boost geometry/coarsening wire equals grid. Dilation multiplies
volumes by4 and pair measures by16, preserving conditional fractions and
normalized weights. Warp and stale warp have identical complete geometric
wires after excluding only the specified annotation weights, candidate values
and their mismatch count. These tests do not authenticate or repair marks.

## Shared intermediate points: the composition obstruction

Take independent uniform X,Y,Z in a unit rectangle with strict product order.
For each coordinate, the probability of an ordered pair is1/2, hence
P(X≺Y)=1/4. The one-entry conditional matrix therefore has row sum1/4,
not1. Row-normalization would change the statistic.

For three points sharing the same intermediate Y, each coordinate has six
equally likely strict orderings, giving P(X≺Y≺Z)=1/36. Equivalently, integrate
u(1-u)v(1-v) over the shared middle point. Multiplying two separately averaged
pair fractions instead gives1/16: it loses their dependence on that point.

With dmu=du dv/2, h=1/2 and J=1/16. The dimensionally matched comparison is

    J^2/h = 1/128,  true triple measure = h^3/36 = 1/288,
    signed product error = 5/1152.

This is an analytic control independently checked by exact integration, not a
new fixed-family triple experiment. It shows why exact pair block sums alone
cannot justify matrix powers, transition dynamics or higher-chain closure.

## Verification and retained evidence

Two independently written mathematical engines consume the same authenticated
source data. Primary integrates with positive-part antiderivatives; reference
uses affine overlap segments. Each derives lineage and complete pair/block
arithmetic independently. The runner compares complete native wires, all
consumed AI clipped-volume and pair-table rows, transformations and provenance.
No historical mathematical engine is imported. Shared input and orchestration
are explicit; the reference replay is not a third production engine.

Before fixed execution, root checked784 rational directed-interval pairs
through both engines, including zero-length intervals, direction complements
and affine scaling:1,568 route comparisons in each normal/optimized mode.
A separate unequal three-level, multi-probe family tested changed signed IDs,
detachment, zero products and direct/via-middle reconstruction. Polynomial
integration independently checked the analytic shared-middle control.
Both implementation authors also ran their own bounded synthetic checks.

All66 tests pass in normal Python(10.67s) and optimized Python(10.69s), run
concurrently with separate external caches. There are54 generic/lifecycle
tests and12 fixed tests: five real complete primary/reference/literal-oracle
family comparisons, a full-suite comparison, three cached route-orchestration
checks and three mutation groups. The34 non-noop corruptions comprise20
family-wire, eight suite and six historical-projection changes. The separate
literal test oracle is additional verification, not another production engine.
An explicit subprocess also checks36 invalid-input rejections in each mode.
The optimized suite has only the expected pytest assertion warning.

The final generic tests before freeze passed54 with12 deselected in normal
1.37s and optimized1.39s. Pre-freeze assembly corrections were limited to an
initial primary syntax typo/formatting and an obsolete malformed-fixture label
in the test subprocess: that label caused two guard harness errors while the
original52 tests passed, then both modes passed after correction. No fixed
fixture, mathematical rule, implementation or protocol correction followed
the first fixed comparison.

The first two-engine capture took2.222483s. A separate fresh reference-only
read-only audit took2.105319s and preserved the capture and all64 identities.
External create-only preflight took2.284163s. First capture and preflight have
identical mathematics and source/prior ledgers; only runtime metadata differ.
These timings are verification metadata, not application performance benchmarks.

The exclusive final capture took2.223598s on isolated Python3.11.6,
macOS arm64, optimization off, two-engine comparison route. Recorded process
RSS high-water was367,312,896bytes; timing/RSS exclude final serialization.
First, preflight and final suite bytes are identical. The complete envelopes
differ only in runtime metadata.

Final [results.json](results.json):1,825,670bytes, SHA256
`4be2fbc4a7f62322416fd2a2e256a529eb03f54fad3ca88674c060d31d94e8d1`.
Canonical mathematical suite:1,815,955bytes, SHA256
`5ceec50884b87bfd5fe08fb51695fa5f16858ed0fcb4f5d9f3daee1de05c7f92`.

Fresh read-only final replays passed: primary normal2.129683s and independent
reference optimized2.010945s. They ran concurrently in separate processes with
separate fresh external caches, so these are not controlled speed comparisons.
Both preserve the complete final bytes and verify all64 source/prior targets:
five frozen AJ sources,40 prior captures and19 ancestor sources. Historical
arithmetic beyond the fifteen consumed AI geometry projections is preserved
by identity, not claimed replayed. Ruff and formatting checks pass all four
Python files. No dependencies were installed or RET/core sources changed.

Read-only replay from the checkout root:

```sh
qr05aj_cache=$(mktemp -d /tmp/qr05aj-replay-XXXXXX)
.venv/bin/python -I -O -X "pycache_prefix=$qr05aj_cache" \
  docs/validation/qr-05aj-pair-coarsening-2026-09-07/study.py \
  --verify --route reference
```

Use primary without `-O` for the other retained route. Creation is exclusive;
the published artifact must never be overwritten. This is a bounded research
lifecycle check, not a claim of generic adversarial JSON/API hardening.

## Proposed next gate: QR-05AK

On these same supplied partitions, compare actual shared-intermediate triple
measures with the dimensionally matched pair product J_AB*J_BC/h_B when h_B
is positive. Integrate over one common middle point, retain all ordered region
triples, and distinguish triple-measure additivity from composition of projected
pair tables. A zero-volume middle region has zero raw triple measure but an
undefined normalized product; do not silently divide by zero.

The purpose is to measure the dependence lost by this pair-product construction.
This is not a universal impossibility claim about all pair summaries or the full
supplied geometry. No fixed AK calculation has been performed. Freeze its detailed
protocol before doing so; observation-mask enumeration and RET integration are
not prerequisites unless a separate new sampling or interface claim is added.
