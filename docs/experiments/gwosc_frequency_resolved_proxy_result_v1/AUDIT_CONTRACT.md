# RI96 independent saved-result arithmetic audit — source preparation

This external packet prepares one independent review of **both completed actual
RI96 modes**. It is not an execution, a qualification result or authorization.
No actual interval, PSD, RI90 numerical body or RI96 result has been decoded in
preparation. The sole implementation is `audit_saved_result.py`; it imports
only Python standard-library modules and never imports or calls the producer,
validator, qualifier, FFT, runtime probe, caller or supervisor.

## Closed scientific scope

The fixed application packet is
`/Volumes/AI_DATA/development/det-review-evidence/ri96-execution/application-preparation-wvp1hizx`.
Its unchanged prospective freeze is 43,585 bytes, SHA-256
`d12228df7dcd73aefb1d3c72da55ca2ea6b5aa2f68754bc011281fc005a0fc46`.
The actual freeze must differ **only** by changing its status to
`authorized_fixed_saved_application`. The application method, environment,
commands, source closure, runtime, input pins, fixed rows/bands, limitations and
acceptance records are therefore inherited from exactly this reviewed packet.
A future source or admission change requires separate review, not permissive
fallback logic in this auditor.

Before scientific decoding, the audit authenticates both complete mode results,
both operand original/copy paths, all original/copied scientific sources,
helpers, qualification/acceptance records, all 3,925 runtime files (including
pinned pycs) and the named interpreter's bound symlinks/target. Every accessed
file is regular, nonsymlink and held by byte identity plus device/inode/size/
mtime/ctime. Inputs are rehashed at the end. Both complete results must have
identical bytes, not merely matching selected values.

The only original numerical operands decoded are the accepted RI73 interval
snapshot (51,891,508 bytes,
`fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba`)
and accepted RI90 report (6,994,965 bytes,
`c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf`).
RI83 and RI73 prior reports remain pinned provenance members; their numerical
bodies are not independently parsed or recomputed. No raw HDF input is opened.

The compact RI73 snapshot is streamed one row at a time. A separately written
fixed-delimiter reader, followed by canonical/closed-schema/hex checks, binds
all eight original rows and all short/long interval endpoints without retaining
a full 51.9 MB JSON tree. It reconstructs the centered long-minus-short interval,
midpoint, radius, exact outward Q256 floor/ceiling coordinates, alpha equal to
the sum of coefficient radii divided by 128, constant-annihilation compatibility
and both endpoint imaginary-zero requirements. All 87,688 initial coordinates
and 65,544 saved one-sided complex rectangles are checked, with exact array
identity and signed canonical hexadecimal/bit-ceiling validation.

## Independently reconstructed arithmetic

For each real or imaginary component, the audit uses the direct identity

`(|center_i| + error_i)(|center_j| + error_j) - |center_i center_j|`

to bound product error. Each total error includes the saved transform radius
and independently derived coefficient alpha. The calculation uses exact common
denominators and integer sums, followed by reduced Fractions. It does not reuse
the primary implementation's transform-only sum plus linear-alpha terms and
alpha-count factorization. Center products are accumulated separately.
Nyquist and DC imaginary centers **and all imaginary error components** are
analytically zero. Nonendpoint real modes have weight two; endpoints have
weight one.

Every entry of the fourteen full 8x8 C/H matrix pairs is reconstructed. Midpoint
Parseval uses the separate transform-only remainder, includes the real DC
component and independently checks all 64 entries against held G. True-A DC
omission in covariance is distinct from this midpoint Parseval check.

For all four PSD scenarios, decode all 8,193 canonical finite nonnegative
binary64 values, verify the complete little-endian byte hash and convert to
exact rational values. The eigenvalue map is fs*P at DC/Nyquist and fs*P/2 at
interior bins. Check all fourteen band minima/maxima and every tied index;
weighted C-minus/C-plus/H-minus/H-plus matrices; exact maximum-row-sum margins;
full lower/upper Loewner endpoint matrices; diagonal/trace intervals; held
non-DC global bounds; every scalar intersection and each conditional ratio.
Check the exact prior projection, positive Gram by an independently coded LDL
recurrence, unchanged `0 <= rho <= 10^-12`, all provenance, closed fields, ten
gates and all ten limitations. No improvement threshold is added. Negative
lower endpoints, zero spectral bins, nonpositive ratio denominators and null
ratios retain the accepted semantics. Scalar intersections are not a new
matrix intersection theorem or an off-diagonal variance bound.

The report gives exact per-scenario scalar results and field identities, full
check counts and complete-result identity. It does not describe all result
fields as independently derived: the transform dependency below is explicit.

## Precise inherited mathematical checks

This audit **does not execute an independent FFT**. It checks every retained
mode rectangle's shape, ordered endpoints, exact byte identity and endpoint
conditions, and then independently rebuilds all response and scenario
arithmetic from those enclosures. It structurally checks all fourteen twiddle
stages but does not recompute square-root isolation, base roots, powers or
interval butterflies. Those validity checks are inherited from the accepted
RI93 qualification and the **genuine completed full `validate_saved` replay in
each actual RI96 mode**, pinned to the reviewed validator source. The replay
independently reads the original snapshot and reconstructs the recursive
transform; the primary uses the other traversal. The audit requires each
worker and parent receipt, actual output custody and exact returned validation
record (8 rows, 65,544 modes, 14 bands, 4 scenarios). A `passed` field on the
scientific result alone never supplies this premise.

Other explicit premises are accepted RI73 interval validity and capture,
accepted RI90 Gram/rho and PSD provenance, constant annihilation and the RI92
Loewner/Gram theorem. Independently checking arithmetic does not prove detector
noise adequacy, stationarity, a physical calibration or a native forward map.
It supplies no new uncertainty law, SNR, p-value, inverse, whitening or RET
result. The four empirical spectra remain separate postulated finite circulant
proxy scenarios.

## Concrete descriptor and root-held admission

The CLI is exactly:

`<held-python> -I -B audit_saved_result.py <AUDIT_INPUT.json> <bytes> <sha256>`

One normal audit invocation checks both application modes. There is no second
audit mode, direct target call, alternate domain, adaptive parameter or retry.
The descriptor is canonical JSON, pinned in the future audit authorization,
and has exactly these fields:

- schema: `ri96-independent-saved-audit-input-v1`;
- status: `root_bound_completed_application_evidence`;
- auditor, contract and authorized_freeze: exact path/bytes/sha256 records;
- root_admission: an exact root-written custody bridge record;
- root_admission_status:
  `accepted_actual_custody_pending_independent_saved_arithmetic`;
- modes: exactly normal and optimized, each with result, receipt,
  worker_receipt, custody, attempt and outer_completion path/bytes/sha256
  records, plus outer_exit_pointer and outer_tool_pointer (JSON member/index
  paths to the genuine separate completion's exit and nonempty tool reference).

The root bridge is intentionally small and precisely specified. Its schema is
`ri96-independent-audit-custody-admission-v1`; its exact keys are schema, status,
authorized_freeze, modes, auditor and contract. Status is the pending-arithmetic
status above; other fields equal the descriptor. Root must issue it only after
reviewing the authentic tool completion evidence, all-mode source/runtime/input
custody and observed output identities. It is not final mathematical acceptance.
The reviewer must read the referenced genuine completion fields; a fabricated
zero or a newly asserted external exit is not adequate. Root may instead choose
a different actual admission format, but that requires a reviewed adapter
change before execution. The accompanying template has null pins and a
prospective status and **cannot pass admission**.

## Actual execution custody checked by the auditor

The auditor reconciles exact parent/worker commands, environment and fixed
limits from the held freeze. It verifies both exclusive attempt records,
source-before/after and complete runtime-before/after records, actual probed
runtime fingerprints, all accepted prerequisites, original/copied input stat
bindings, immutable captured RI90 body identity, canonical saved-result
validation completion, result/custody identities, empty successful stderr,
worker exit and parent child exit zero, success/no-stop and genuine separately
retained outer exits zero. The root-written bridge cannot be created by this
consumer or upgraded to an arithmetic acceptance.

Every raw `/bin/ps` attempt is inspected. Each live valid RSS observation must
have exactly one matching sample; only the terminal observation may lack a live
RSS. Every sample elapsed/RSS and gap, the peak, final sample-to-reap gap and
child elapsed are reconciled. A conservative eight-ulp allowance concerns only
subtraction of retained binary64 timestamp metadata; the declared sample gap
of 0.1 s, final gap of 0.1 s, 180 s wall and 524,288 KiB sampled RSS limits are
checked directly, with **no tolerance or threshold relaxation**. Sampling is of
the single reviewed worker; it is not an OS cap or aggregate group-RSS claim.
Genuine child creation/reaping provenance remains the reviewed actual caller
plus root's authentic outer tool evidence; receipts are not cryptographic proof
that an operating system ran.

The accepted qualification metadata, both original qualification receipts and
all fourteen actual artifact pins in both modes are reopened. Their historical
mathematical and resource adjudication is inherited; this audit does not rerun
qualification, silently repair it, or claim an additional audit-control suite.
All earlier failed attempts remain historical evidence and must not be deleted.

## Future supervision and acceptance gates

Before execution, root and another reviewer must read this complete source and
contract, bind final source pins, inspect the real completed descriptor and root
bridge, and review a minimal caller adapted from the already qualified exact
monitor/cleanup mechanism. Keep the complete unchanged runtime, exact argv/env,
exclusive output paths, source/input pins before and after, and the same
180-second/512-MiB/.025/.1/.05 envelope. The caller must capture exact auditor
source bytes before executing it and collect complete canonical stdout as the
actual audit report. It must preserve failures, raw monitors, exit status,
worker/caller receipts and exclusive output identities. No actual caller,
freeze or authorization is created by this source-only packet.

After the one admitted invocation, an independent completed-evidence reviewer
must reconcile the **audit's own** authentic outer exit, raw sampled resources,
source/runtime/descriptor inputs and report identity. Root must read the actual
arithmetic report and inherited-premise boundaries before final RI96 acceptance.
An audit report alone never proves the audit ran within the admitted resources.
Source review, qualification, actual application, saved arithmetic and physical
interpretation remain separate decisions throughout.
