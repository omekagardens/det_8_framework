# RI-57 — selected-row finite-context operator

24 September 2026 UTC. **Failed numerical qualification, preserved for reproduction.
The actual sensitivity calculation was not admitted.**
This packet implements the [accepted RI-55 design](../gwosc_context_sensitivity_v1/DESIGN.md).
The eight rows, context lengths, precision and acceptance gates stay fixed.
A rigorous enclosure may still fail the separate usefulness requirement.

## Target and claim boundary

The target is the exact rational linear operator F_m obtained by interpreting
all accepted binary64 SOS coefficients as exact rationals. It includes each
stage's own odd extension, initialized ordered forward cascade, reversal,
fresh initialized cascade, reversal and unpadding. It is not a replacement
filter recipe. The published binary64 production filter and Decimal80 reference
are rounded numerical evaluations; neither is exactly linear.

For central length N=2769, side length L=4096, and T=N+2L=10961, let E insert
a central vector into zero context, U insert left/right context around zero
central values, and C crop the central N positions. The selected rows are
0, 1, 27, 805, 1384, 2741, 2767 and 2768. Their exact coefficients are

- a_i = E^T F_T^T C^T e_i - F_N^T e_i;
- b_i = U^T F_T^T C^T e_i;
- d_i = a_i^T x and g_i = sum_j |b_ij|.

For an explicitly supplied finite M>=0,
`sup_{||z||inf<=M} |d_i + b_i z| = |d_i| + M*g_i`.
This is a sharp rowwise algebraic statement. Different rows may require different
attaining contexts. No physical M is selected by this packet. A proved nonzero
context coefficient prevents a finite bound over unrestricted real contexts;
a coefficient enclosure containing zero is not proof of nonzero or exact zero.
The finite context window and eight rows do not represent an infinite physical
continuation or a complete samplewise uncertainty profile.

An exact-operator interval alone does not cover every rounded production run.
That would additionally require a bound for the baseline rounding error and a
uniform extended-input rounding bound. No such physical or production-wide
promotion follows from numerical comparisons with the reference.

## Independent oracle and exact transpose

`oracle.py` was authored without reading the new engine. It implements exact
Fraction direct form I with constant prehistory and forward basis columns for
small systems. `operator.py` separately implements exact small direct form II
and its startup-aware transpose. Later cross-review is distinct from independent
oracle authorship. The already published RI-44 Decimal80 reference is explicitly
reused for admitted-length numerical diagnostics, not claimed as a new oracle.

For one SOS section write
`H=[[-a1,1],[-a2,0]]`, `c=(1,0)`,
`J=(b1-a1*b0,b2-a2*b0)`,
`g=(b0+b1+b2)/(1+a1+a2)`, and `h=(g-b0,b2-a2*g)`.
Its initialized state is h times the original pass-input first value times the
product of all preceding section DC gains. The transpose starts at lambda_ell=0
and runs backward:

`bar_x[k] = b0*v[k] + J^T*lambda[k+1]`

`lambda[k] = c^T*v[k] + H^T*lambda[k+1]`.

Each section contributes `h^T*lambda[0]` times its preceding DC-gain product
to the original pass-input coordinate zero. All such contributions are summed
there after reversing the cascade. There is no division by an earlier DC gain,
which may be zero. A stage is transposed in reverse operator order; its odd
extension transpose folds the two endpoint weights and subtracts reflected
entries. Full stages also reverse order. H inverse is never used.

## Validated arithmetic and residual proof

The point recurrence uses 256 significant binary digits with nearest/even
rounding. Small matrix intervals round outward at 256 bits. Every local equation
residual, interval endpoint, final sum and dot product is computed as an exact
Fraction, subject to explicit resource limits. No ambient Decimal or binary64
arithmetic enters a certified interval. Coefficient conversion remains exact.

The adjoint point recurrence rounds only the first state coordinate; the second
is an exact copy of the preceding first coordinate. Let r enclose incoming
coordinate error, eL be the largest first-coordinate state residual, eX the
largest output residual, and eP the startup-scalar residual. If K_v bounds
`sum_{k>=0} |c H^k v|`, a section has valid bounds

`r_out = |b0|*r + K_J*(r+eL) + eX`,

`r_start = K_h*(r+eL) + eP`.

These follow by summing the signed Green function against the scalar state
forcing error. Startup errors are multiplied by absolute preceding DC products,
then added with their exact accumulation residuals. Reversal and zero insertion
are exact; the odd-extension transpose multiplies the incoming error by its row
absolute-weight sum and includes each final rounding residual. Applying these
bounds through all reversed stages yields a conservative uniform row radius.
Its conservatism cannot be hidden by relaxing a width threshold.

For complex poles, `a2>0` and `D=a2-a1^2/4>0`, the rational matrix
`P=[[a2,-a1/2],[-a1/2,1]]` is positive definite and satisfies
`H^T P H = a2 P`. Exact Jury inequalities also imply `a2<1`.
Cauchy-Schwarz gives

`sum_{k>=0}|c H^k v| <= sqrt((v^T P v)/D)/(1-sqrt(a2))`.

The implementation forms J and h exactly before bounding them, preserving
numerator cancellations. It rounds the square roots upward, verifies that
`1-rho_upper>0`, and rounds the final quotient upward. An unsupported or
unresolved denominator returns no certificate. For `a2=0`, the exact alternative
is `|v0| + |(-a1)*v0+v1|/(1-|a1|)`, which covers the prescribed first-order/FIR
toys without bypassing the validated path.

The frozen signed-power search remains mandatory: K=2^j, j=0,...,20, using
outward repeated squaring and the first proved infinity-norm contraction for
H and H^T separately. A transposed enclosure of H^K encloses (H^T)^K.
Finite remainder powers have quadratic-form entry bounds or the exact a2=0
bounds. The contraction witnesses are admission checks; the scalar Green bounds
supply the residual estimate. Stable coefficients alone do not guarantee that
this declared method succeeds.

The implementation caps lengths, padding, stages, SOS count, input integer size,
intermediate integer size, point-rounding exponent, proof serialization and
state-update count. The machine-readable `arithmetic_contract()` is authoritative
for these finite limits. Exceeding a cap or failing a certificate is unresolved,
not a qualified result. Precision is not raised adaptively.

## Qualification and protected input ordering

Before admitted-coefficient execution, root freezes the reviewed arithmetic
source and the verifier/driver source closure. The qualification driver verifies
published dependency bytes before parsing or executing them. The engine pin
must be real; rejecting authoring placeholders cannot qualify anything.

Both normal and optimized execution must pass the accepted gates: all 32 exact
toy configurations; complete N/T outputs for seven synthetic vectors; nine
adjoint seeds against all seven vectors at both lengths; all eight row width
checks; exact/contained constant-input cancellation; and malformed provenance,
configuration, arithmetic, status and receipt refusals. Tiny toy checks compare
all forward basis columns and adjoint rows, affine decomposition, box corners
and attaining witnesses. The same validated engine must enclose their exact
answers. All floating-reference dots use exact arithmetic on retained values.
Zero-vector production and reference outputs must both be exactly zero.

The actual driver requires a caller-pinned, successful qualification receipt.
It verifies runtime, source and dependency identities, recomputes the selected
coefficient rows, and compares their interval identities before accessing the
accepted RI-53 input export. It then uses the unchanged 2769 `input_hex` values;
there is no interpolation, subset, filtering of an already filtered vector,
new acquisition or retiming of the printed-time metadata. The actual context
width gate is `1e-12*max(abs(x))`, without a unit floor. No accepted partial
sensitivity report is permitted after any failure.

An optional M must be an explicitly labeled canonical nonnegative rational,
with positive denominator and the frozen integer-size bound. Without it, only
conditional ingredients and zero/nonzero/unresolved classifications are emitted.
All output must be external and exclusive before reviewed publication.

## Evidence and next action

RI-55's external exact algebra/adjoint checks support the design, but do not
qualify this new implementation. Root and a separate complete source/method
review accept the prospective engine at 24,882 bytes, SHA-256
`3a7b847bd8bec752a48af2c339a5cebd6d923c3b307c2c54910abddbf51703b4`.
The independent oracle is 9,484 bytes, SHA-256
`37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651`.

The engine author's external exact-synthetic checks pass normally and under
optimization: 48 toy models, 360 adjoint rows and 2,936 entries, 192 forward
vectors, 40 extra dense seeds, 62 power-enclosure checks and arithmetic/refusal
controls. Both 650-byte reports have SHA-256
`90c62806fe61f02418bb2ef336c4354f158f320754299da3e0ba0ac7b91dfdbd`.
The separate reviewer independently ran 192 forward vectors, 448 exact and
448 validated rows, 3,456 coordinate containments, 22 finite Green-sum sanity
checks and arithmetic/refusal controls. Both normal/optimized 391-byte reports
have SHA-256
`33cd9c90b657ca9f89185228b3058d7b654be3cda40a5fcac2397c4fe8f8e44b`.
These are exact small-system evidence and analytic method review; finite
Green sums do not prove the infinite bounds, which have the analytic argument
above. No admitted coefficients or scientific sample values were executed.

The qualifier and driver passed root and separate complete source reviews.
Independent normal/optimized arithmetic and custody checks passed 41 controls
per mode; author helper/mock checks passed 89 per mode. These tests were
explicitly separated from qualification. The first author mock omitted a stub
for the final coefficient guard; the mock was corrected before its passing run,
without changing production source or suppressing a failure.

At 2026-09-24 07:01:28 UTC root froze an isolated eleven-file source/dependency
closure, including the prospective method guide, before running admitted
coefficients. Numerical execution used the existing RI-44 CPython 3.11.6,
NumPy 2.1.3, SciPy 1.14.1 and h5py 3.12.1 runtime with its full pinned platform
identity. The sources executed here remain unchanged; this guide's closing
status/evidence was updated after the result. Commands from the isolated root:

```sh
/path/to/pinned-ri44-python -I -B docs/experiments/gwosc_context_operator_v1/check.py
/path/to/pinned-ri44-python -I -B -O docs/experiments/gwosc_context_operator_v1/check.py
```

The absolute interpreter used was
`/var/folders/47/s7fm88bn5ql2tw7j103kbyzr0000gn/T/det-ri44-processing-apas30qu/env/bin/python`.
The accepted RI-44 requirements/runtime receipt specify its environment; the
temporary directory name alone is not a portable environment guarantee.

Both runs exited **1** with empty stderr and byte-identical 161,816-byte JSON,
SHA-256 `7dfbc8cac7e631a9c3663bca2b288b134d6cea03f1d0ca14c8334746761a808a`.
The exact output is [QUALIFICATION_REPORT.json](QUALIFICATION_REPORT.json).
**187 of 196 gates passed; 9 failed.** All 32 exact toy cases, 14 complete
production/reference vector comparisons, 126 adjoint diagnostics and 15 refusal
categories passed. Every one of the eight gain-enclosure width gates failed.
Their dependent structural-constant report could not complete because the eight
rows had not been certified with the required widths. It is not evidence that
the analytic constant-annihilation identity is false. Synthetic central-context
width checks inside those failed enclosure gates were not reached.

The full driver also refused this failed receipt under both interpreter modes,
before its actual-input read, and created no output directory. The test supplied
a nonexistent synthetic sentinel path, not the scientific input. There is no
`SENSITIVITY_REPORT.json` in this packet: actual input processing was not admitted.

A subsequent diagnostic reran only the frozen T-length row-zero unit seed.
It found a valid uniform coordinate radius about 1.2555514907816582e-10 and gain
interval approximately [1.95270195782976, 1.9527040149253223]. The width exceeded
its unchanged gate by about 1,053,460 times. The conservative radius grew from
about 6.8e-75 after reversed stage 16 to 1.26e-10 after stage 0. This diagnoses
loss of useful precision in the uniform error propagation, not a discrepancy
with the exact toy transpose or a measured physical uncertainty. The external
810,641-byte proof trace has SHA-256
`f3653e1f5f123b84fd1af13c129f280492b6bc7494fea40c1fbd7bcd10e198df`.

This failed source and receipt remain fixed. RI-60 separately reviews a method
using per-coordinate error radii, retaining 256-bit arithmetic, all row/context
choices and every threshold. It must receive its own source freeze and full
qualification; the present failure is not reclassified as success.

This is conventional public-data numerical work. A native detector forward map,
physical continuation envelope, calibrated agreement and gravity prediction
remain separate obligations. RET remains paused.
