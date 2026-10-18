# RI119 independent complete source review

26 September 2026. Reviewer: separate `ri119_full_source_review` agent.
Disposition: **no remaining source-review blocker found for this fixed
synthetic packet after the resource-guard corrections and pointwise coverage
completion below**. This is
not execution admission, successful qualification, or a runtime/custody review.

I read the complete primary, independent validator and qualifier as text,
the full contract and implementation/author notes, and the accepted RI118
design. I manually followed the mathematical formulas, all saved fields and
every frozen negative control. Only text reads, source metadata hashing and
this review-file write were performed. No target import, execution, compilation,
AST analysis, probe, sign enumeration, simulation, scientific output generation,
repository edit, git/index operation or runtime admission occurred.

## Exact reviewed bytes

The six packet files below were stable at final text review. This review does
not pin itself and does not purport to review a later caller or source manifest.

| File | Bytes | SHA256 |
|---|---:|---|
| primary.py | 20346 | aea35e5840d96e0aee1bacf258d94a735171e201ac1c02fee23a2151feed7d10 |
| validator.py | 23321 | b915ae587e9193c51a66c79f0dd987adb9f1e114a285503297521729ab987707 |
| qualify.py | 14435 | 23ccba3faff451894fbfbd35024b5575e25fc42f1d6d4616e052d8a89ddb58c3 |
| CONTRACT.md | 17291 | 13d54fc6af96ca22b793cd47aee7588257ce3b3c1f1e246eaf07e580bee010ab |
| IMPLEMENTATION.md | 7499 | 76f5e84c4ab00aa7c31d9a822e45fdf505323ef80e6423fc718499abdd249ac3 |
| VALIDATOR_NOTES.md | 6697 | f147ae3b8633225bd1d8c06ca995439c538e6db2caf428843fe0abab6eccfc27 |

Accepted-design reference in the project is
`docs/experiments/gwosc_joint_window_covariance_v1/DESIGN.md`, 15602 bytes,
SHA256 `d128bcab94f453bb9aa506595cd76a6b3907533924f5d1b3ed3df202706d03a4`.

## Scientific review

The scientific input is closed: nine small literal models and three dimensioned
nuisance fixtures. The primary uses full independent sign cubes with the
declared latent factors, applies scale to both raw mean and factor, applies A
to the first T entries of shared raw windows, and directly accumulates complete
first/second moments and pointwise energies. Its pointwise U=V+mean-energy
check and its separately accumulated centered moment identity are exact.
The source-defined nine-case support sizes sum to 912; the Q12 scalar-factor
supports add eight. These are manual source counts, not observed execution.

The validator has a materially different arithmetic route: literal selectors,
projected factors, complete covariance matrices, an explicit centering matrix,
and the U-minus-mean-energy identity. It neither imports/calls the primary nor
enumerates its sign cubes. The declared independent authorship is consistent
with that source structure; later parent harmonization was limited to protocol
and resource guards. The complete scientific model, selectors, maps, raw/window/
stacked/cross/mean-output/centered covariances, means, scalar energies and counts
are all compared. There is no scalar-trace-only substitute for full matrices.

Manual calculation confirms the following prospective energy table. It is an
analytic review of declarations, not a fabricated machine result:

| Case | E[V] | E[U] | E[||mean output||^2] |
|---|---|---|---|
| Q02_white_two | 3/2 | 2 | 1/2 |
| Q03_periodic_two | 2 | 2 | 0 |
| Q05_white_three | 16/9 | 2 | 2/9 |
| Q06_constant_mean | 3/2 | 2 | 1/2 |
| Q07_quadratic_mean | 400/9 | 566/3 | 1298/9 |
| Q08_scale_minus_one | 3/2 | 2 | 1/2 |
| Q08_scale_two | 6 | 8 | 2 |
| Q09_oriented_matrix | 5/2 | 4 | 3/2 |
| Q10_zero_map | 0 | 0 | 0 |

Q02 and Q03 retain equal I4 within-window marginals but different coherent
cross-window laws. The declared Q02 cross covariance is -1 and the periodic
one is -2. Q05 preserves both adjacent -1 terms and the nonadjacent zero.
Q07 has output means (-4,-12,-20), mean dispersion 128/3 and centered covariance
contribution 16/9. Constant nominal mean cancellation is realized by A applied
to that actual constant input; no generic centering rule is substituted.
Before counting each Q06 sign vector, the primary explicitly checks its actual
A row sums and equality of outputs to the same-sign zero-mean baseline. Before
counting each Q08 vector, it checks outputs against the signed scale times
the same-sign unit-scale baseline. This matters because aggregate second
moments alone cannot distinguish scale -1 from +1. Both guards are correctly
inside their complete sign loops and change no result schema.

For Q09 the orientation is correct: C=[[-1,0],[-1,0]], the reverse block is C^T,
and the centered average is [[3/2,3/4],[3/4,1]]. Transposing only cross_blocks[0][1]
changes an actual asymmetric matrix and is caught even though a scalar trace
could miss it. Zero A and the singular periodic covariance require no ridge,
inverse, tolerance or eigensolver.

Q12 remains one output per window in the standalone n=2 factor bounds. The
calibrated constant produces -1. With D=(1,-1)^T and Pi D=D, the covariance
contributions 1 and 2 attain absolute-error bound 1; the calibration factors
produce contributions 1 and 4 and attain bound 3. The validator explicitly
checks the fixed equal-factor premise before replacing a product of Frobenius
norms by their squared norm. These fixtures supply no physical eta or
calibration envelope and are not an eight-output capture calculation.

## Complete interface and control review

Closed roots and inventories precede scientific comparisons. Recursive shape,
plain-type and rational checks cover all cases and bounds before case-specific
value checks. Within each case, fixed dimension values precede the Q02/Q03 PSD
guard and ordered model/selector/map/mean/covariance/energy comparisons. Bound
dimensions precede calibrated-constant and bound checks. Type-sensitive equality
does not conflate booleans with integers. Canonical byte parsing refuses duplicate
keys, nonfinite values and noncanonical entire bodies; rational syntax and
reduction are checked by the complete result comparators.

I traced every one of the 33 single-fault report mutations, five parser
controls and three PSD controls through both implementations. In the reviewed
source each reaches the exact first-refusal code frozen in CONTRACT.md;
33+5+3=41 controls per implementation. The altered fields actually differ
from the fixed baseline, including M12's asymmetric block and M32's nonzero
centered off-diagonal. Unexpected success or an unexpected exception is a
qualification failure. This is a source-path assessment, not a claim that any
control has run or that the finite inventory exhausts all malformed inputs.

The qualifier creates its own fresh primary reference and a separate parsed
scientific record, requires both full baseline successes, preserves canonical
baseline/reference snapshots and compares malformed inputs before/after each
full result guard. Parser controls use immutable bytes/strings. PSD-control
arguments are compared before/after the guard pair; the reviewed guard bodies
do not mutate them. A final baseline/reference check precedes the report.
The saved report contains the complete scientific body, exact refusal records,
coverage, counts, scope and limitations. Its whole canonical serialize/parse
path and full audit are part of run().

The audit correctly distinguishes saved-field reconstruction from historical
execution: it compares every saved field, calls the independent scientific
validator again and requires an independently owned fresh primary reference,
but explicitly says it does not reexecute or witness the historical controls.
Actual captured-child execution and external custody must establish that part.
No supplied report is allowed to choose the fresh reference. The source uses
no assert-only acceptance gate and no mode-dependent scientific branch.

## Findings corrected during this review

1. Primary scalar parsing initially ran its grammar check before the individual
   decimal-component bound, while the validator applied that bound first.
   Oversized nonnumeric components could therefore have different first labels.
   The parent moved the primary component bound before grammar matching. I read
   that edit and verified the final source order matches the validator.
2. The validator's PSD determinant initially bounded a*c-b*b only after the two
   products could cancel. The primary bounded each product. A large rank-one
   covariance could therefore evade the validator's stated per-operation
   resource guard. The parent now bounds both products before their difference.
   I read the edit; short-circuit symmetry and nonnegative-diagonal checks remain
   intact, and singular PSD acceptance is preserved for admissible magnitudes.

Two explicit prospective regressions now cover these corrections. M33 supplies
2468 nonnumeric characters in a rational field and must refuse RESOURCE before
grammar inspection. G03 supplies a rank-one PSD matrix whose four entries are
2^4096: each parsed entry fits, but its products have 8193 bits and must refuse
RESOURCE before cancellation. The source constructs that decimal value only
inside the future run; it has not been evaluated here. A RESOURCE refusal of
this mathematically PSD matrix is not a finding of non-PSD mathematics.

The parent also identified the need to test Q06/Q08 output properties pointwise.
I agreed with and reviewed the minimal loop guards described above; they make
the signed-output obligation explicit rather than inferring it from moments.

Both corrections were source-only. They were not verified by executing any
boundary fixture, and they do not alter the fixed scientific model or results.

## Remaining prerequisites and limits

The bounded dimensions, decimal/rational/body limits, 41-control inventory,
closed schemas and full expected-field equations are fixed before execution.
The documents preserve the existing candidate runtime and sampled-resource
thresholds as requirements, explicitly without claiming current identity,
admission, resource fit or a hard operating-system allocation cap. The modules
do not read data, spawn children, provide a CLI or inspect a runtime on import;
they import only the named standard-library dependencies. Actual transitive
runtime capture and source loading remain the future caller's responsibility.

The next reviewable step is root's concrete caller/application of existing
supervision, with exact source and complete runtime closure, independent caller
review and explicit execution admission. Genuine normal and optimized runs in
fresh roots, retained failure/custody evidence, full result validation and whole
canonical byte identity remain necessary. No such event is established here.
No RI73 coefficient capture, RI116 numerical body, empirical PSD or observed
HDF5 enters this packet. A malformed report's refusal is relative to the fixed
declared model, not a prohibition on all coherent joint laws. Physical modeling,
calibration, significance, protected validation and native prediction remain
separate; RET remains paused.
