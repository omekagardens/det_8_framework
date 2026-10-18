# QR-05BA results: field-plus-acquisition error composition

8 September 2026 (Honolulu). Completed bounded mathematical gate.
Protocol: [README.md](README.md). Final evidence: [results.json](results.json).
Base: pushed AZ commit
`fb8170842b5d3efca57908c4699f645babc1baf1`.

## Main result

The separately declared field and acquisition error budgets compose sharply,
row by row, on the declared Cartesian uncertainty set. Both supplied geometries
retain all 64 exact target gains through the existing 12-to-48-tile refinement
for every one of the four budget cases. The decoder, 37 receivers and target
normalizations are unchanged.

The field-only maximum remains 1. The receiver-coordinate unit box has a
much larger normalized effect and a different maximizing target:

| Budget (field, acquisition) | Grid exact maximum | Grid maximizing rows | Warp exact maximum | Warp maximizing rows |
|---|---:|---|---:|---|
| Zero (0,0) | 0 | All 64 | 0 | All 64 |
| Field (1,0) | 1 | 6,7,15,23,31 | 1 | 6,7,15,23,31 |
| Acquisition (0,1) | 28,800 | 18 | 5,308,416/25 | 9 |
| Joint (1,1) | 115,201/4 | 18 | 21,233,689/100 | 9 |

These exact maxima hold at both parent and child levels. Rows are zero-based
original target indices: row 18 is (3,3), row 9 is (2,2). At each joint maximizer,
the field term is **1/4**, not the global field maximum 1. Thus the sharp
maximum of the rowwise sum is smaller by 3/4 than the sum of the two separate
global maxima. Every tie and all off-target outputs are retained.

**The numerical receiver box is not an apparatus noise model.** Each radius 1
means one existing RAW receiver-coordinate unit, without measured scales,
uncertainty calibration or matched physical noise across the two geometries.
The unequal values above are therefore not a physical accuracy ranking.
Likewise, comparing the field-only and acquisition-only numbers does not
compare equal physical perturbations or establish that real noise dominates.

Each fixed family has 31 positive and 33 zero field gains, and acquisition
gains are positive on exactly the same 31 rows. All 64 normalizations are
defined; the zero rows here are not undefined rows. The generic tests retain
the distinct case of undefined normalized targets with nonzero raw noise.

## Why the terms add, and where that statement stops

Let dmu=du*dv/2, V be the probe volume, and sigma_i=V² h_C h_D.
The raw global-moment bank e(deltaF) integrates the signed field against the
tilewise basis (1,u,v,uv). The fixed zero-intercept maps satisfy D B=G over
the full raw bank. Observed error is

```text
y = B e(deltaF) + n
|deltaF| <= epsilon V² almost everywhere
n = diag(rho) z,   |z_j| <= eta,   rho_j >= 0
K = D diag(rho)
H_i = K_i / sigma_i               only if sigma_i > 0
gamma_i = sum_j |H_ij|
normalized total_i = field_response_i/sigma_i + H_i z
```

The field and acquisition choices range over a **Cartesian product of
deterministic uncertainty sets**. This is not statistical independence,
a sampling distribution, a confidence guarantee or a claim that real errors
are uncorrelated. Correlated realizations can lie inside the set, but a
smaller coupled set need not have the same sharp bound.

For a defined target with supplied piecewise bilinear kernel k_i, retain

```text
C_i = (V²/sigma_i) sum_t |integral_t k_i dmu|
L_i = sum_t,a |A_i,ta|             A_i,ta = V² integral_t k_i phi_ta / sigma_i
S_i = (V²/sigma_i) integral |k_i| dmu
U_i = (V²/sigma_i) sum_t h_t max_corner |k_i|

Cbar_i = epsilon C_i + eta gamma_i
Lbar_i = epsilon L_i + eta gamma_i
Sbar_i = epsilon S_i + eta gamma_i
Ubar_i = epsilon U_i + eta gamma_i
Cbar_i <= Lbar_i <= Sbar_i <= Ubar_i
```

The triangle inequality gives the upper bound for Sbar. The field
deltaF=epsilon V² sign(k_i) and independent coordinate choices
z_j=eta sign(K_ij) attain its positive endpoint; negate BOTH choices for
the negative endpoint. Cbar and Lbar are likewise sharp for their
tile-constant and corner-bilinear field subclasses. These are target-specific
witnesses, not a generic simultaneous maximizer of every target.

A numerical Sbar is retained only when all tiles of that row have field
sign certificates, or epsilon=0. In the latter case the total is exactly
eta*gamma without promoting a mixed field kernel to sign-certified.
An unavailable exact entry remains NULL. A maximum over the exact-available
subset is not a maximum of an uncertified full query.

If sigma_i=0, normalized maps, gains and outputs remain NULL even when
both budgets vanish. Raw K, n and Dn remain meaningful and can be nonzero.
The implementation retains them. Adding acquisition error does not count
B e(deltaF) twice: it is the separate n term only.

## Refinement result

The same physical field, same receiver error n, same decoder, probe and
target scales are compared across the two representations. Parent corner
values map to correlated child corners through the convex restriction E;
raw child moments add by lineage. The positive and negative paired pipelines
actually integrate both representations and use the SAME z and n.

This preserves every field, acquisition and total observation/output
component and all defined normalized responses. The independent child
bilinear cube is a larger finite subclass, not a new apparatus measurement.
At each fixed budget, the full measurable-field uncertainty set and receiver
uncertainty set are unchanged by refinement. Different budgets do define
different uncertainty sets.

The unchanged acquisition contribution cancels from every refinement gap:

```text
Cbar_child - Cbar_parent = epsilon (C_child - C_parent)
Lbar_child - Lbar_parent = epsilon (L_child - L_parent)
Ubar_parent - Ubar_child = epsilon (U_parent - U_child)
```

For all four fixed budgets, Cbar, Lbar and Sbar are identical between levels.
Field and joint budgets each have 26 strict upper decreases per geometry,
38 ties and maximum decrease 7/16 at rows 9,18,36,63. Their 26 loose rows remain
loose, with largest Ubar-Sbar excess falling 3/4 to 5/16. Zero and
acquisition-only budgets have 64 upper ties and zero gaps.

In the joint case, the parent-to-child envelope MAXIMUM changes from
28,801 to 460,809/16 on grid, and 5,308,441/25 to 84,934,881/400 on warp.
The exact joint maxima do not change. These envelope maxima stay on row 18
and row 9 respectively; tighter certification is not improved measurement
precision.

Across two geometries and four budgets, the capture has 512 inherited exact
budget-target occurrences, zero newly exact or unavailable occurrences,
and 104 strict upper decreases. They are repeated case counts, not 512
distinct observables or 104 distinct target rows. The generic domain still
permits newly exact and unavailable child rows.

## Controls and independent calculations

The new primary implementation uses global monomials and separable exact
integration. The independent reference uses physical polynomial interpolation,
exact tensor Simpson integration, endpoint-grid partition checks and actual
bank/receiver unit probes. The third full-wire test oracle uses polynomial
dictionaries, antiderivatives and scalar pipelines. Independent source and
oracle authoring preceded the common comparisons; all were held before the
source freeze. Neither engine imports another engine's mathematics or
executes an older gate's family builder.

The root separately checked seven literal synthetic cases against both
engines in normal and optimized Python. One example on a unit probe uses
k=2-u, B selecting mass/u moments, D=(2,-1), rho=(1/32,1/16),
epsilon=1/3 and eta=2/5. Here S=3, gamma=2 and the exact joint gain is 9/5.
The actual positive witness has field receiver errors(1/24,1/48),
acquisition errors(1/80,-1/40), decoded field 1/16, decoded acquisition 1/20
and total 9/80; division by sigma=1/16 gives 9/5. Midpoint refinement lowers
Ubar from 32/15 to 59/30 without changing the sharp gain.

Further root literals use k=u-1/4 with gamma=9,
epsilon=1/2 and eta=1/3. The parent has Cbar=Lbar=13/4 and no exact value.
A midpoint split gives child Lbar=79/24 and Ubar=7/2, still uncertified.
A split at the zero u=1/4 gives exact child 53/16 with Ubar=29/8; the
parent record stays NULL. Setting epsilon=0 instead gives exact total 3
at both levels while the mixed field certification remains unchanged.
Other literals retain raw null-target totals(-1,-2), zero radii,
identity refinement and empty receivers.

The common independent tests also cover:

- Product-set sharpness versus a smaller coupled set: on the unit probe,
  take B=(1/16,0,0,0), D=1, rho=1/16 and sigma=1/16. The normalized
  constant-field contribution is c/8 and the normalized acquisition term
  is z. With epsilon=1 and eta=1/8, the product set has sharp normalized
  gain 1/4 (raw bound 1/64). The smaller constant-field set with z=-c/8
  cancels exactly.
- Small Cartesian vertex enumeration, opposite target signs, defined zero
  rows, partial exact availability and subset-only maxima with complete ties.
- Nonconstant parent/child pairs, new child sign certificates, unresolved
  mixed kernels, zero budgets/radii, fractional budgets and budget order.
- Actual public integration/production/application argument multisets,
  raw component sums, off-target outputs and detached shared input objects.
- Positive diagonal/permuted receiver coordinates and affine geometry
  changes with their field/moment/decoder/radius transport. Independent
  reference controls additionally cover signed coordinate permutations.
- A mixed receiver transform: the transported unit square is a parallelogram.
  Replacing it with a new independent enclosing box changes a test gain 1
  into 2. No general zonotope API or fixed affine family is introduced.
- Complete late shape/value rejection before arithmetic, native types,
  dimensions, geometry, cycles, retained 4096-bit limits and cancellation.
  These are bounded generic guards, not a production-security claim.

## Retained inventory and byte accounting

Each family retains four budgets,40 actual parent/child witness pairs and
24 standalone child witnesses. Thus there are 104 actual field/noise
pipelines per family, each with one integration, three productions and
three applications; the reference additionally performs independent unit
probes. Every pipeline retains 16 fields and every pair 15 fields, including
complete raw errors and residuals. No discarded AZ witness, moment-block
bank, transport table or comparison was replayed as an input.

| Per-family inventory | Count |
|---|---:|
| Positive cells; target rows; receivers | 8;64;37 |
| Parent / child tiles | 12 /48 |
| Parent / child bank coordinates | 48 /192 |
| Input geometry / matrix / budget rational entries | 276 /7,216 /45 |
| Geometry / restriction rational entries | 133 /768 |
| Parent / child kernel rational entries | 9,216 /36,864 |
| Parent / child field-map rational entries | 12,288 /49,152 |
| Field-bound / acquisition rational entries | 520 /4,801 |
| Case-bound / exact-bridge / comparison rational entries | 2,080 /256 /780 |
| Retained witness rational entries | 145,592 |
| Signed field/acquisition choices | 2,328 |
| Named checks / count fields | 16 /35 |

Repeated rationals and zeros count; NULLs, signs, indices, names and native
count values are excluded from the rational-entry counts. Sign choices have
their separate count. The protocol gives every formula, and the test oracle
also traverses the stored rational fields independently.

| Canonical newline-terminated JSON bytes | Grid | Warp |
|---|---:|---:|
| Input projection | 50,202 | 50,378 |
| Field evidence | 851,401 | 858,630 |
| Acquisition evidence | 29,466 | 29,677 |
| Cases | 1,015,769 | 1,036,480 |
| Complete native family | 1,948,143 | 1,976,470 |

These are overlapping serialized projections, not unique additive storage
costs, an online packet specification or an application benchmark.

## Verification and provenance

All 70 gate tests pass in normal Python (915.84s) and optimized Python
(917.41s). The optimized run emits pytest's expected warning about ordinary
assertions outside rewritten tests. Public refusals are explicit ValueError
checks, not disabled assertions. The isolated normal and optimized guard
subprocesses each execute 738 explicit rejections: 369 per engine.

There are 1,161 non-noop exact-wire mutations: 665 across three generic
families, 472 across the two fixed families, eight suite mutations and
16 selected-history mutations. Ten additional changes to excluded AZ
calculations are deliberately admitted by the selected-history bridge;
the complete consumed artifact remains byte-authenticated separately.
Thirteen synthetic projection changes are rejected. These are bounded
comparison/admission tests, not adversarial authentication guarantees.

The first primary/reference comparison passed in 85.6368s. Exactly one
independent NORMAL reference-only read-only audit followed, passing in
65.0848s while the full tests ran. Before and after the tests/audit, all
166 identities and the first capture bytes were unchanged.

The subsequent fresh preflight comparison passed in 85.0349s, followed by
the exclusive final primary/reference capture in 85.5733s. Fresh read-only
replays of the final capture passed through normal primary (54.1001s) and
optimized reference (65.1695s). All three captures have identical complete
non-runtime content. Final byte/identity checks again preserve all 166
identities, the original first/preflight bytes and the final capture bytes.

| Capture | Bytes | SHA256 |
|---|---:|---|
| External first | 3,951,707 | 9098f6193439d97cb4f85999c02496cfd9ebd456d3648a1c44f5daf8d1ea52d8 |
| External preflight | 3,951,711 | 7babd814bfa0702176fb5fbbded9862f440fb028005ce2c3d1a3edc66b8ab9db |
| Retained final results.json | 3,951,707 | 171c2d522a001a0cf547385100b24582da24d1f2effa8e26fe64967a708d31fd |

The five sources were frozen at 2026-09-09T03:00:08.752073+00:00,
before any assembled fixed BA projection or mathematics. The ledger covers
five current sources, 57 prior captures and 104 ancestor sources: 166 identities.
The parent AZ artifact is 2,380,556 bytes, SHA256
`cbb04f7a4af49a5714ecf80652393933557f490f7e16dab0848b8d32cda27585`.

The first comparison's suite is 3,927,273 bytes, SHA256
`2ef4ac5bd8fd3ecdc2a653a4102424ae5dc66e442a51910dc5695d8b894da19d`.
The external freeze record is 23,985 bytes, SHA256
`e3f0fa0ea3c96b4588365585c619dea715c92c22d61c04f5e5de95c91fc93645`.

| Frozen source | Bytes | SHA256 |
|---|---:|---|
| README.md | 23,333 | 9b52c40901c17d7e3007549ecf73daa2a612551f8b70ac34036a41f87f5f2e55 |
| kernel.py | 51,616 | 5dc03f1a6806abcb3550d3b151e94d27f6cd4b61150a46697538ac8da7da0a47 |
| reference.py | 54,505 | 8615b3a377f34973b295d9b8263725f7ede582b43acccd75a98e5b48f8fab69b |
| study.py | 51,983 | 2affdeeba2e89e40f1f9181afede64ee441984181c95f592e6aea8be511a891a |
| test_qr05ba.py | 114,264 | 11467352299750eed4cc8bee7cee7cd7738f49ec61b4ceafb0e90ab9685ad786 |

Prefreeze generic tests passed 60 normally and 60 optimized, with 10 fixed
tests intentionally deferred. Earlier 59 generic tests passed before a
synthetic test's name was changed from fixed_shapes to declared_shapes so
that it also ran prefreeze. This was test selection, not a mathematical
failure or revised expected value. Other authoring cleanup was unused
bindings/stale inherited test documentation, all before freeze. No
post-first mathematical/source/protocol correction has been made.
One stored-output reporting command exceeded its tool display budget;
reducing its JSON whitespace fixed reporting only, without changing the
capture or executing an engine.

All runs use the existing Python 3.11.6 environment with isolated mode and
fresh external bytecode caches; no dependency installation or RET execution
is part of this gate. Timings and process high-water marks are verification
metadata, not application benchmarks. The 128MiB capture and 192MiB
serialized-working caps do not bound peak memory or arbitrary computation.
Ruff lint/format checks and scoped diff whitespace checks pass.

Example read-only reproduction from the repository root:

```sh
qr05ba_cache=$(mktemp -d /tmp/qr05ba-replay.XXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05ba_cache" \
  docs/validation/qr-05ba-field-acquisition-errors-2026-09-08/study.py \
  --route primary --verify
```

Use another fresh cache with `-O --route reference` for the independent
optimized route (`-O` belongs before the script name). The gate tests are
`test_qr05ba.py`, run via `-m pytest -q -x -p no:cacheprovider` in each mode.
Do not overwrite the retained capture; creation uses exclusive mode and
verification preserves its original bytes and runtime metadata.

Publication is restricted to the seven files in this gate directory and
the quantum–record/geometry roadmap. The pre-existing 231 unrelated status
entries remain unchanged; no RET source, calibration bank, application
artifact, book file or other checkout is part of this work.

## Roadmap consequence and scope

BA provides a useful additive deterministic error contract for future
readout models. It separates uncertainty in the physical field from
uncertainty added at acquisition, preserves them under representation
change and makes the unit/uncertainty-set assumptions explicit. It does
not supply the actual budgets, calibrate an instrument, authenticate a
measurement or identify geometry from observations.

Potential uses, conditional on a justified interface and budgets, include
target-specific worst-case acceptance bounds, error-budget allocation among
readouts, and deciding whether tighter field envelopes matter relative to
acquisition uncertainty. Exact reconstruction D B=G alone does not imply
a small acquisition gain. No decoder optimization, new readout design or
validated application is supplied by this gate.

The next proposed step is **QR-05BB: an operational bridge-design checkpoint**,
not an automatic new alphabetic numerical study. Select one event/readout
interface and conventional geometric comparison, document what information
the observer really has, separate uncertainty sources and specify a possible
failure criterion before freezing further calculations. Existing
supplied-geometry comparisons are not erased by this checkpoint; it asks
what would connect them to an operational record model.

The local roadmap still records RET as an unvalidated preview with G2 open.
This isolated mathematical gate neither verifies the latest separately
developing SDK source nor closes its calibration or application gates.
The QR-06 quantum adapter, materials monitoring, anomaly triage,
Lean verification and empirical work have their own prerequisites.
No quantum channel, unknown metric, gravitational dynamics, ontology,
new physical law, clock coupling or sensor improvement is established.
Book work remains archival.
