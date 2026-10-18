# QR-05D evidence revision 2: native JSON control containers

5 September 2026. The original mathematical results and every original source
are preserved. Version one must not be represented as having passed its own
strict read-only replay command.

## Detected failure and exact scope

All 133 original tests passed in normal and optimized Python. The create-only
capture succeeded, but the first optimized replay failed at suite equality.
The runner's `controls.collision.interior_orders` was a Python tuple. JSON
encoded it as a list; the freshly reconstructed tuple then compared unequal
to that list. Individual executor outputs had round-trip tests, but the
aggregate suite did not. The lifecycle tests used a simple stub suite.

A recursive comparison found exactly one difference, that container type at
`/controls/collision/interior_orders`. Canonical JSON bytes of the reconstructed
and saved mathematical suites were identical. No coordinate, count, coefficient,
control value, prior witness or mathematical acceptance condition changed.

The retained version-one artifact is `results.json`, 2,523,350 bytes, SHA-256:

```text
ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238
```

Its protocol and six-file source ledger remain unchanged. `study.py --verify`
is deliberately not patched and retains its known container-type failure.

## Version-two correction and safeguards

`study_v2.py` changes the collision container to a list. It also rejects any
non-native mathematical JSON tree before capture and during replay: tuples,
floats and non-string dictionary keys are not permitted. This guard is stricter
than merely calling json.dumps, which can silently convert some Python values.
Runtime metadata remains separately allowed to contain measured floating-point
durations, outside the exact mathematical suite.

Exact suite and dual-executor comparisons use canonical JSON bytes after the
native-type guard, not ordinary Python equality. This preserves the distinction
between Boolean and integer values (`True == 1` in Python), with a dedicated
nested-type substitution regression. The independent review identified this
additional comparison issue before version two was captured.

Every version-two run must reproduce exactly the mathematical JSON suite already
saved in version one, in addition to rerunning the two independent executors
and all original controls. Version two uses new create-only `results-v2.json`
and schema `det8-qr05d-results-v2`. It pins version one's artifact as an eighth
prior, and binds nine source identities: the original six plus this revision,
study_v2.py and test_capture_v2.py. No frozen source or artifact is overwritten.

Regression tests now cover the complete real suite's JSON round trip, equality
to the preserved v1 mathematical data, the recursive exact-wire guard and the
new driver lifecycle. This is an evidence-packaging correction, not an excuse
for the geometric discrepancies: the mesh bias, density error, local warp
ambiguity and endpoint collision all remain retained.

## Corrected reproduction commands

Run all tests normally and optimized using the README's fresh-cache commands.
For the current capture/replay driver, use these commands instead of the v1
capture/replay commands:

```sh
qr05d_capture_v2_cache=$(mktemp -d /tmp/det8-qr05d-capture-v2.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05d_capture_v2_cache" docs/validation/qr-05d-geometric-correspondence-2026-09-05/study_v2.py
```

Only capture if results-v2.json does not exist. Then replay read-only:

```sh
qr05d_replay_v2_cache=$(mktemp -d /tmp/det8-qr05d-replay-v2.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05d_replay_v2_cache" docs/validation/qr-05d-geometric-correspondence-2026-09-05/study_v2.py --verify
```

Version-two source files freeze at its capture. Interpretation and audit outcomes
belong in RESULTS.md, outside either source ledger. This revision does not alter
the protocol's scientific scope or establish any new physical result.
