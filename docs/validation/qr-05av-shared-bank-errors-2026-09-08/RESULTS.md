# QR-05AV results: shared-bank error propagation

8 September 2026. Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AU commit `dfbd1f7208bd3ba5659012c96b5839eb917f2760`.

## Main result

Keeping the common bank-error structure gives strictly tighter response bounds
than its independently variable receiver-coordinate enclosure for seven of
64 targets in EACH geometry. The other 57 bounds tie: 33 are zero and 24 are
positive. The same seven target indices have strict gaps in both families.

The enclosure also changes which target appears most sensitive. Under the
shared-error model, the unique largest bound is at target (9,9) in both cases;
the enclosing receiver box instead selects (3,3) for grid and (3,10) for warp.

| Numerical unit-box certificate | Grid | Warp |
|---|---:|---:|
| Raw bank / receiver / target coordinates | 48 / 37 / 64 | 48 / 37 / 64 |
| Strictly smaller shared bounds / ties | 7 / 57 | 7 / 57 |
| Maximum sharp shared gain | 10/3 | 26/9 |
| Its unique target, zero-based row | (9,9), 54 | (9,9), 54 |
| Maximum receiver-enclosure gain | 27/8 | 185/56 |
| Its unique target, zero-based row | (3,3), 18 | (3,10), 23 |
| Largest rowwise enclosure-minus-shared gap | 9/4 | 65/21 |
| Its unique target, zero-based row | (3,3), 18 | (3,10), 23 |

The largest rowwise gap is NOT the difference between the two global maxima.
Counts are not probabilities. Neither the raw grid/warp values nor their
ordering establish intrinsic geometric robustness or calibrated sensor precision.

## Declared error model and exact identity

The complete AU coefficient maps B, G and D remain unchanged and satisfy
D B=G. No source fitting, new readout, filter reselection or normalization row
is introduced. The selected whole-bank identity is explicitly rechecked;
old AU ranks, source restrictions, witnesses and other mathematics are not replayed.

The generic error contract is

```text
e = W xi,                   |xi_j| <= epsilon,
x_measured = B(z+e),
D x_measured - G z = G e.

H = B W,                    J = G W = D H,
A_ij = J_ij / sigma_i,
beta_l = sum_j |H_lj|,
alpha_i = sum_j |A_ij|,
gamma_i = sum_l |D_il| beta_l / sigma_i.
```

The normalized target error lies in [-epsilon*alpha_i,+epsilon*alpha_i].
Both endpoints are attainable on the prescribed primitive box. Bounding each
receiver coordinate separately gives |eta_l|<=epsilon*beta_l and the larger
sharp interval [-epsilon*gamma_i,+epsilon*gamma_i] for that DIFFERENT domain.
The triangle inequality proves alpha_i<=gamma_i.

The fixed benchmark preregistered W=I48 and sigma=ones64. These are the stored
RAW NUMERICAL coordinate units, not a dimensionless apparatus model or a
probability distribution. A Cartesian box means separately variable coordinates,
not stochastic independence. Target scales are reference constants, not possibly
zero observed responses. Negative corrupted moments or outputs are not clipped.

Full D B=G is checked before restriction by W. The weaker D B W=G W would
allow a deficient primitive map to hide an incorrect decoder. All full-bank,
restricted-error and normalized coefficient maps and residuals are retained.

## Every strict row

All indices below are zero-based original target rows. Every unlisted row
has exactly equal shared and enclosure bounds.

| Row / target | Grid shared | Grid enclosure | Grid gap | Warp shared | Warp enclosure | Warp gap |
|---|---:|---:|---:|---:|---:|---:|
| 2 / (1,3) | 7/48 | 17/48 | 5/24 | 115/1152 | 95/384 | 85/576 |
| 15 / (2,10) | 1/12 | 19/12 | 3/2 | 5/24 | 485/168 | 75/28 |
| 18 / (3,3) | 9/8 | 27/8 | 9/4 | 25/32 | 75/32 | 25/16 |
| 19 / (3,4) | 1/8 | 3/8 | 1/4 | 35/288 | 35/96 | 35/144 |
| 21 / (3,7) | 1/4 | 3/4 | 1/2 | 25/72 | 25/24 | 25/36 |
| 22 / (3,9) | 5/12 | 5/4 | 5/6 | 13/24 | 13/8 | 13/12 |
| 23 / (3,10) | 1/12 | 7/4 | 5/3 | 5/24 | 185/56 | 65/21 |

All strict rows here have positive shared gains. The alpha=0<gamma case occurs
in the generic controls, not these fixed cases. Previously discussed target
row63=(10,10) has a tied gain of 2 in both families.

## Signed witnesses and important countercontrols

Every target retains both signed shared endpoints and both signed enclosure
endpoints, with complete cross-target error vectors. There are 128 shared and
128 enclosure endpoints per family, including repeats and all-zero endpoints.

Each shared endpoint actually evaluates xi -> W xi -> B(W xi) -> D(B(W xi)),
with a separate direct G(W xi) evaluation. All complete direct/decoded errors
agree, every target obeys its own bound, and the designated target attains its
positive or negative endpoint. The enclosure endpoints pass through the same
restricted receiver but have no manufactured primitive or bank antecedent.

For the largest shared bound, row54=(9,9), the canonical positive primitive
witness is (+1,-1,-1,+1) on bank coordinates36..39 and again on40..43,
with every other coordinate zero, in BOTH geometries. Its negative attains
the lower endpoint. This is an error vector, not a prepared physical source.

All tied maximizing TARGET indices are retained. A canonical sign witness
does not enumerate the entire maximizing face, and individual row witnesses
need not maximize every response simultaneously.

Two small controls make the domain distinction explicit:

- B=[1;1], D=[1,-1], G=[0], W=[1] gives shared gain0 but enclosure gain2.
  A common perturbation cancels exactly; the receiver box discards that relation.
- B=[1;1], D=[1,0], G=[1], W=[1] gives equal gains1, but the canonical enclosure
  vector (1,0) is not a shared vector (xi,xi). A tied bound does not prove
  equality of error domains or reachability of that canonical vector.

No general fixed inverse-image/feasibility solver is part of this gate.
The enclosure is not assumed to describe possible shared-bank measurements.
Synthetic empty/deficient error maps, zero receiver radii, repeated targets
and opposite signed maximizing directions retain their distinct semantics.

## Application meaning and limits

If the coarse and supplemental values really are computed from one noisy bank,
the appropriate error map is G W, not an arbitrary independent perturbation of
the receiver inputs. Preserving that dependence can avoid overly conservative
budgets and misleading rankings of sensitive response rows. If the measurements
instead have separate acquisition errors, a common-bank model needs justification;
the arithmetic here does not establish that apparatus architecture.

These are exact deterministic bounds conditional on the declared maps and error
set. A finite gain alone is not operational robustness: actual error magnitudes,
tolerances, reference units and acquisition mechanisms remain unspecified.
Local moment errors need not be realizable perturbations of a physical field.

Synthetic coordinate transport moves B,G,D,W and sigma together and preserves
the normalized shared map and its sharp bounds. General mixing of RECEIVER
coordinates can change the axis-aligned enclosure and its bounds. Resetting W=I
after a bank basis change would define a new error set, not the same model.

No empirical noise calibration, field reconstruction, minimality recomputation,
RET integration, physical sensor validation, quantum-channel construction,
unknown-geometry inference, gravity derivation or Lean verification was performed.

## Representation and tests

Across both families, 19,168 input rational occurrences and 45,152 map entries
are retained. The 464 gain entries include receiver radii, both row-gain lists,
all gaps and three maxima per family. The 256 shared endpoints retain 83,456
rational occurrences and 6,144 signs; the 256 enclosure endpoints retain 42,496
rational occurrences and 4,736 signs. Zeros and repetitions count.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Input problem | 59,677 | 59,735 |
| Complete coefficient maps | 136,971 | 137,149 |
| Shared bounds and witnesses | 276,464 | 277,759 |
| Enclosure bounds and witnesses | 145,903 | 146,874 |
| Complete comparison | 648 | 665 |
| Complete native family | 620,386 | 622,905 |

The canonical suite is 1,245,154 bytes. These overlapping projections are not
additive unique storage or measured-value transmission packets.

All 62 tests pass normally and optimized: 92.54 s / 92.95 s in the recorded
concurrent runs. Before freeze, 52 generic tests passed in both modes
(4.94 s / 4.84 s), with all ten fixed tests deselected.

Primary constructs dense products and absolute row sums. Reference reconstructs
the maps through actual column probes and coordinate interval endpoints.
The third oracle uses independently indexed scalar contractions and exhaustive
vertices of SMALL synthetic primitive/receiver cubes. Fixed 48-dimensional
vertices are not exhaustively enumerated; complete coefficient identities and
explicit attaining signs certify the fixed linear bounds.

Each isolated normal/-O guard subprocess performs 316 explicit ValueError
rejections across the two engines: 139 malformed fixtures, ten overflow/cycle/
deficient-map rejects and nine early-admission checks per engine. Nine additional
synthetic selected-history projection rejections check the bridge boundary.

All 475 non-noop mutation checks pass: 306 generic family, 154 fixed family,
eight suite and seven selected historical-producer changes. Six deliberately
unselected historical changes remain admitted by selective bridge helpers;
complete actual prior captures remain byte-pinned.

Synthetic checks cover signed/rectangular/rank-deficient W, p=0 and s=0,
non-unit target scales, epsilon scaling, full same-domain transport, primitive
signed permutations, receiver mixing versus monomial rescaling, actual endpoint
call inventories, tiny values, retained overflow versus canceled intermediates,
early admission, cycles versus shared inputs and detached outputs.

The expected optimized pytest warning concerns assertions outside test modules.
Engine guards use explicit exceptions and separate normal/-O subprocess checks.
This is not exhaustive hostile-input, work, memory or production API hardening.
Timing measures verification, not an application benchmark.

## Freeze and evidence lifecycle

Five AV sources were frozen at 2026-09-08 23:40:17 UTC before any fixed AV
projection, error map, gain or witness calculation. All 136 distinct identities
were bracketed: five AV sources, 52 prior captures and 79 ancestor sources.

1. First external primary/reference comparison: 14.5126 s.
2. Exactly ONE independent normal reference-only read-only audit: 10.1245 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 14.5068 s.
5. Exclusive final comparison capture: 14.5712 s.
6. Fresh primary-normal / reference--O read-only replays: 5.6906 s / 9.5879 s.

The audit and full tests ran concurrently after the first comparison; both
finished before preflight. All non-runtime first/preflight/final fields agree,
with every source identity and capture byte unchanged. Capture and serialized
working caps are not process-memory or computation bounds.

Before freeze, an author's unpublished cancellation hand was correctly
rejected because it overflowed a RETAINED full endpoint; that hand fixture was
changed to exercise genuine unretained cancellation. No engine mathematics or
protocol correction was required. There were NO post-first source, protocol,
fixture or mathematical corrections.

Final capture: 1,265,211 bytes, SHA256
`db498dfae4d1659f0fe35eef72efc916c6d9c8fedbd375830145e78a680c4ef5`.
Suite: 1,245,154 bytes, SHA256
`08e12a2ef6a452a61d52e822aa8a35a58b8ac2263e806174c71d216814458ae9`.

## Next proposed gate

QR-05AW should define a supplied-geometry LOCAL bank error-domain contract.
Authenticate the actual repair-bank tile order, raw monomial coordinate labels,
probe bounds and original fine target regions. Preregister local bank-coordinate
synthesis, reference amplitude/volume scales and target normalization; derive
blocks from those actual regions, not AP's old coarse tiles.

This declares a NEW local-coordinate error box, not a mere renaming of AV's raw
unit box and not improved precision at equal physical noise. Preserve AV as-is.
Separately verify that the new domain transports consistently under coordinate
changes, keeping the AU response maps frozen and retaining shared-error versus
receiver-enclosure distinctions. Zero target scales require explicit undefined
semantics, not a fabricated unit scale or normalized zero.

Geometry can provide reference units, not measured uncertainty magnitudes.
Physical calibration and field-realizable error classes remain later questions.
No fixed AW synthesis, scale, gain or witness calculation has run.
