# QR-05BH results: certified global-admission refinement

8 September 2026 (Pacific/Honolulu). The bounded gate passes.
The fixed subdivision certifies **36 of 42 candidate profiles**, including
eight excluded by BG's older sufficient rule. Actual polynomial values
refute the other six. No fixed candidate remains unresolved.
Inner and outer sets consequently coincide in all 35 menus.

This settles global validity for these particular candidate polynomials,
not for arbitrary profiles or experiments. It also reveals two target
ambiguities hidden by the older restrictive class: stronger validity
certification can admit more alternatives and thereby remove apparent
uniqueness. No means, sampling positions or quantum laws were changed.

See the [standalone model and frozen checking rules](README.md),
[input](protocol.json) and [complete capture](results.json).
BG's entire mathematical report is preserved separately as bg_model.

## What was checked

The supplied square, profile basis and target remain
V=1/2, σ=1/16 and q=(1/9,1/18,1/18,1/36,1/144).
Full corner means fix c; each candidate position gives
θ=(m_cc−φ(z)·c)/b(z). The 42 resulting polynomials are unchanged.

For every candidate the report retains the full-square Bernstein net
and four covering half-square nets: **210 patches, 1,890 coefficients
and 1,890 zero reconstruction residuals**. Nonnegative degree-(2,2)
basis functions partition unity, so each patch's coefficient interval
encloses its whole polynomial range. Exact equality on the local
unisolvent grid verifies the represented polynomial, within this degree
bound. All leaf coefficients lie inside their root coefficient enclosure.

Root nets certify 21 profiles. Subdivision certifies 36, including
all 28 older admissions and eight additional profiles. The other
six fail the subdivision certificate and have actual violations;
failure of a coefficient bound alone was never used as refutation.
The fixed nine-point physical grid contributes **378 values**, of
which six are strictly outside [−1,1], one for each refuted profile.
There are no certificate/refutation conflicts.

These counts come from a prespecified control menu, not an estimate
of how often experimental profiles are valid. Enclosing coefficient
bounds are not automatically attained extrema or a range optimizer.

## Eight valid profiles recovered from conservative exclusion

Six recovered candidates belong to constant_corners_zero_interior,
and two to asymmetric:

| Public case / candidate position | Root coefficient enclosure | Subdivision enclosure | Target |
|---|---|---|---:|
| constant corners / center | [−3,1] | [0,1] | 5/36 |
| constant corners / equality_u and equality_v | [−19/5,1] | [−1/5,1] | 7/60 |
| constant corners / shift_low and shift_high | [−7/2,1] | [−1/8,1] | 1/8 |
| constant corners / near_corner | [−55/9,1] | [−7/9,1] | 17/324 |
| asymmetric / equality_v | [−1/2,37/20] | [−1/2,191/240] | 59/540 |
| asymmetric / shift_high | [−1/2,47/24] | [−1/2,79/96] | 97/864 |

All eight fail the old sufficient bound and the root coefficient check,
but pass every covering leaf. For the center control f=1−16b, the
root lower coefficient −3 is not an actual field minimum. Its refined
enclosure is [0,1], consistent with BG's separate attained-range proof.
Root failure must not veto a valid refined certificate.

BG's old class-infeasible constant-corner reports remain intact in
bg_model and the old set layer. BH does not rewrite their history:
it supplies stronger evidence under the broader globally valid family.

## Six actual violations, despite valid sampled qubits

Every refuted candidate has a strict violation at the physical point
(1/2,1/2):

| Public case | Candidate position(s) | Actual f(1/2,1/2) |
|---|---|---:|
| unit_interior | equality_u, equality_v | 6/5 |
| unit_interior | shift_low, shift_high | 9/8 |
| unit_interior | near_corner | 16/9 |
| asymmetric | near_corner | 109/108 |

Each polynomial still matches all five supplied population means at
its candidate sampling coordinates and hence gives valid local qubit
states there. That does not extend to every point of the square.
In particular, the asymmetric violation is only 1/108 above one;
exact rational arithmetic distinguishes it from a valid boundary value.
No tolerance or fitted noise explanation was used.

These are mathematical counterexamples to global validity within
the stipulated response model, not observed experimental anomalies.
The witness grid is a calculation, not additional acquired measurements.
The six local-only branch laws and diagnostic targets remain recorded.

## Exact finite target sets, including newly exposed ambiguity

For this fixed run, every candidate is decided. Thus
H_inner=H_valid=H_outer for each supplied menu, and their target
projections also coincide. This equality follows from certificates
and actual counterexamples, not from assuming that a failed bound
implies invalidity.

The largest menu gives:

| Public case | Globally valid positions | Exact target set | Target status |
|---|---:|---|---|
| zero | 6 | {0} | identified |
| plus | 6 | {1/4} | identified |
| minus | 6 | {−1/4} | identified |
| quarter_interior | 6 | {1/36,1/32,1/30,4/81} | ambiguous |
| unit_interior | 1 | {1/9} | identified |
| constant_corners_zero_interior | 6 | {17/324,7/60,1/8,5/36} | ambiguous |
| asymmetric | 5 | {19/270,61/864,19/216,59/540,97/864} | ambiguous |

Across all 35 menus, existence is certified for **33**, and **two**
are infeasible within the declared family/menu. Target status is
**26 identified, 7 ambiguous and 2 infeasible**. All 35 hypothesis
sets and all 35 target sets have exact inner/outer agreement.
No fixed unresolved report occurs; generic tests still exercise it.

The two infeasible menus are unit_interior's equality_pair and
shifted_pair. Here all candidate polynomials have actual violations,
so BH proves more than BG's sufficient-class refusal. It still does
not establish inconsistency of the locally valid quantum experiment
or exclude profiles outside the declared family.

The five constant-corner menus move from old class-infeasibility to
certified existence. center_only identifies 5/36, equality_pair 7/60
and shifted_pair 1/8. all and center_near are target-ambiguous;
their hull width is 7/81. Neither hull replaces the exact finite set.

For asymmetric, the newly certified equality_v and shift_high
alternatives remove two earlier class-relative identifications:

| Menu | BG sufficient-class target set | BH globally valid target set |
|---|---|---|
| equality_pair | {19/270} | {19/270,59/540} |
| shifted_pair | {61/864} | {61/864,97/864} |

Their target separations are 7/180 and 1/24. The all-position hull
widens from 19/1080 to 181/4320 because valid alternatives were
previously excluded. This is an admission-model effect, not changed
measurement data. All candidates in each case still share the
complete five-role law and internal quantum outputs.

The old quarter-interior full-law collision remains unchanged:
4b at the center and (64/9)b at near_corner have target difference
7/324. Better global certification does not repair missing position
information. Nor does target identification imply position identification;
with exact corners and nonzero q_b it does fix the coefficient vector
in this particular family.

## Unresolved remains a legitimate result

The fixed menu happens to be fully decided. Neither the checking
budget nor acceptance was changed to obtain that outcome. The generic
combiner tests retain unresolved cases using explicitly abstract
classification inputs, not claims of additional realized profiles.

An empty inner set with a singleton outer target leaves existence
and target identification unresolved. Nonempty inner plus a singleton
outer target certifies identification. Two distinct inner targets
already certify ambiguity, even if the full target set is not known.
Duplicate target values can give exact target information despite
unresolved hypotheses. These logical cases are tested separately.

There is no inference from “no grid violation” to global validity,
no probability distribution over positions, and no confidence coverage
claim for the supplied exact means.

## Verification and source history

The first source freeze and first capture succeeded. The primary
affine-monomial/power conversion and independent interpolation/
de Casteljau implementation agree on the complete native report.
The third test route reconstructs every net through exact
Bernstein-Gram moments, tensor-Boole integration and cofactor inversion.
Extra interior evaluation checks are mathematical oracles, not stations.

All **48 tests passed** in isolated Python 3.14.0 normally and optimized
(22.779 s and 22.822 s). There are zero Python assert statements;
checks remain active under optimization. Both complete driver replays
passed with all eleven frozen identities and the same capture bytes.

Exactly one reference-only audit in isolated Python 3.11.6 made one
analyze call (0.51974 s) and matched the full mathematical report:
**466,036 canonical bytes**, SHA256
`b39ba5768d21b421bbef2747138263eccb93ffba250dc25434079e06e487f882`.
It used a fresh external cache and verified unchanged input, all eleven
sources, freeze and capture before/after. Only the verified current
reference ran, including its statically carried BG route; no primary,
driver, tests or historical executor was imported or executed in that
audit. This is not a full-suite Python 3.11 compatibility claim.
Recorded timings are not benchmarks.

The entire freshly recomputed BG report matches retained BG mathematics:
six positions, seven cases, 42 candidates, 35 old menus, both witnesses,
the domain control and all 1,568 branches (812 positive, 756 zero).
BH adds 35 refinement menus without changing the experiment.
Historical executors and BG's separate BF restriction, lifecycle tests
and prior audit/publication process were not rerun.

Source-bound tests cover native types and typed nulls, complete/late
coefficient and branch mutations, dropped leaves or witnesses, omitted
violations, input mutation, source/cache changes, strict bounded JSON,
create-only outputs and publication/replay byte brackets. The two
authenticated protocol snapshots are hashed and parsed from their
respective same bytes; altered certificate budgets and nested model
inputs reach their own rejection guards. Fault injections are temporary
or in memory, not alterations of the retained evidence.

Prefreeze static cleanup included formatting, a set-comprehension
lint adjustment and an explicit loop-variable binding in a test spy.
**No post-first source, protocol, mathematical or test correction was
required.** The partition, witness grid and all population inputs
were fixed before evaluation; no failed first capture is hidden.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| source-freeze.json | 2,337 | `14ec10d9ea284e08788faac230de79f482d53e83bce0d4a74742e4d8e87d8661` |
| results.json | 2,613,666 | `a5e1387c4de81d35641ea8b9f333d4530c66e729a3e60df2ca6e5f80e251d9f5` |

Use the [model sheet's replay/test commands](README.md#source-bound-execution-and-acceptance);
do not overwrite the retained capture. This publication starts from
pushed BG commit `55fc87cd5b50cb4d3ef6a61f13a4a785a7e8b658`.
Separate core, RET, applications and other dirty work remain outside
scope. Local pre-run process checks found no RET timing rehearsal.

## Next proposed gate: QR-05BI, interval-valued interior response

Keep exact supplied corners, the finite position menus and the same
profile family. Prospectively replace the exact interior population
mean with small fixed rational intervals, including zero-width controls
that must reproduce BH. This is supplied uncertainty, not a statistically
calibrated finite-shot interval or a model of apparatus faults.

For fixed corners, each Bernstein coefficient and each witness value
is affine in θ. Solve their scalar linear inequalities exactly to
obtain certified inner and necessary outer θ sets. Preserve the old
sufficient certificate as an inner route. Intersect with the θ interval
obtained by inverting each candidate position's response interval, then
project to per-position target intervals and their finite union.

Retain position metadata, endpoints, gaps and empty sets; an interval
hull must not replace a disconnected union. Narrowing the response
interval or position menu must shrink both bounds. Distinguish
existence, target uniqueness and exact inner/outer agreement as in BH.
The global θ constraints depend on the fixed corner vector, not on
candidate position, and can be derived once per case. Handle zero-slope
constraints and closed endpoints explicitly. Merge overlapping or touching
intervals for the target union while retaining separate position records.
An uncertain mean specifies a family of quantum-record laws, not a single
midpoint law; do not assign posterior weights to that family.

BI is conceptual only and has not been run. No continuous-position
inference, noisy-corner treatment, finite-shot coverage, RET adapter,
apparatus calibration, metric inference or gravity dynamics is included.
