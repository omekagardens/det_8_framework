# Bounded exact renewal-port verification

12 September 2026. This certificate checks the existing
[candidate](../t8-q-renewal-port-candidate-2026-09-12/CANDIDATE.md), unchanged.
It is not a new QR-05 gate, a geometry result, a test of physical quantum
predictions, or an extension of the candidate law.

## Fixed scope, written before execution

Enumerate all six-positive-branch histories of lengths zero through three:
1 + 6 + 36 + 216 = 259 histories. Add exactly one named four-birth history,
the all-zero diamond `ab,a,b,ab`. Do not sample, search parameters or extend
this census. There are 260 retained base rows.

For every row retain the complete strict order, event-indexed action,
outcome and setting records, precursor sets, exact history weight and all
81 atomic matrix-unit images. A common exact coefficient with 81 explicit
destination cells specifies the entire linear payload map, not just its
action on a selected state. Also retain all nine next-branch possibilities:
six positive branches and the three separately labelled identically zero
branches. Zero maps retain all 81 zero images, are not normalized and cannot
be committed. The four-birth row's next menu is inspected only; no fifth
birth is committed.

Two independent implementations are compared. `primary.py` maintains port
heads and inclusive downsets and composes forward possibility permutations.
`reference.py` reconstructs precedence from the full committed port history,
closes that relation, and transports all matrix units using independently
written inverse-pullback coordinate rules. They share no mathematical helper
or source import. Each is loaded from the source bytes bound into the study.

For each retained marked order, replay every linear extension with stable
event identities and compare the full terminal row, including next menus.
Also check the fixed label replacement `i -> 10 + 7*(n-1-i)`; labels are not
time inputs. Histories are bounded at four and extension enumeration at 4!.

Named controls, not further study sweeps:

- All-zero fork/join have equal full payload maps but nonisomorphic orders;
  the diamond has the specified five strict comparable pairs.
- All six coordinate bijections and their true inverses; a wrong forward
  rule substituted for inverse pullback is detected for a cycle and shear.
- Same-port cycle/reflection do not commute. Disjoint-port settings do;
  past-locality alone is not asserted to imply general commutation.
- Changing an incomparable event's outcome leaves a fixed local branch's
  precursor, setting and full map unchanged. An explicitly incorrect
  global-stage setting rule fails the adjacent-swap check.
- Exact normalization, retained zero branches, unchanged committed inputs
  and append-only order/records.
- The candidate's exact complex positive-definite `d*`, its conjugate with
  the same atomic diagonal, and a nonzero positive zero-total-mass kernel.
  The first two have identical record weights; zero total mass does not
  imply an identically zero pair-kernel. Direct singleton restrictions of
  `d*` have total weight 9/10, not one.
- The rank-one mass-functional argument is checked only through its finite
  effect identity and the preceding scope witnesses; these computations do
  not constitute an exhaustive numerical proof of the general theorem.
- Strict malformed input refusals, finite resource limits, tampered source
  and capture refusal, and create-only evidence lifecycle checks.

## Exactness and evidence lifecycle

Only the Python standard library is used. Rational quantities are
`fractions.Fraction`; complex kernel entries are pairs of exact rationals.
No QR-05, RET, T8, Hilbert-space or external mathematical implementation is
imported. This is a developer certificate with an intentionally small API,
not a new shared public API.

The supported commands, from this directory, are:

```
python3 study.py --tests
python3 -O study.py --tests
python3 study.py --capture
python3 study.py --verify
python3 -O study.py --verify
```

The driver applies a 60-second deadline. Sources may be tested and reviewed
before capture. Capture is permitted only after the final source review; it
creates `source-freeze.json` and `results.json` exclusively, never overwriting
either. The freeze includes this README, both independent routes, driver,
tests and the unchanged candidate document. Results embed that exact freeze
and the full report. Subsequent `--verify` authenticates every source and
recomputes the complete report without writing anything. Sources are not
edited after capture. A changed source requires a new explicitly authorized
study, not an overwritten capture.

Passing this finite census supports the implementation of this candidate
on these cases. Universal positivity and covariance remain conditional
mathematical arguments based on positive scaled permutations and adjacent
incomparable swaps. The added port grammar, finite algebra, fixed weights
and orthogonal record preparation remain assumptions. No state-dependent
readout, quantum-to-order feedback, empirical validation or geometric
conclusion follows from this certificate.
