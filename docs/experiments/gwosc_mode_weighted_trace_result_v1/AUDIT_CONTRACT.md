# RI100 independent saved scalar arithmetic audit — source contract

This is preparation of a separate mathematical consumer. No actual RI96 or
RI100 scientific body has been decoded during authoring, and no auditor,
helper, primary, validator, qualifier, FFT or numerical fixture has run here.
The actual RI100 output, its completed custody bridge and a later audit
execution remain unissued inputs of this source-only preparation. Nulls in
the descriptor template are deliberately inadmissible.

The author did not write the RI98 primary, product-form validator or qualifier.
The author proposed the RI97 question, reviewed that design and the RI98
qualification caller, and authored the earlier RI96 saved arithmetic consumer.
Those related roles are disclosed; this is separately written scalar
arithmetic, not an independent proof of the inherited transform or physical
covariance. Other source reviewers must disclose their own roles too.

## 1. Fixed numerical question and independent route

The sole upstream numerical input is the complete accepted RI96 RESULT:
41,673,703 bytes, SHA256
`5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580`.
The other body is one genuine completed RI100 RESULT, whose identity must
come from both completed application modes and root's custody acceptance.
A new PSD, alternate processing row, different amplitude, chosen bin or
summary table is not an admissible substitute. Complete normal/optimized
output bytes must agree before either scientific body is parsed.

Keep M=16384, fs=4096, Q=2^256, eight rows
`0,1,27,805,1384,2741,2767,2768`, and the separate scenarios
`H1:left,H1:right,L1:left,L1:right`. The independent module imports only the
standard library, never a primary/validator/qualifier, native or runtime
helper. It has no new transform or coefficient reconstruction. Source-level
literal method, gate and limitation vocabulary is transcribed from the
accepted contract; numerical functions are separately implemented.

For a retained component with integer endpoints l,u, set
`m=l+u`, `n=u-l`, `d=2Q`. Exact center is m/d and transform radius n/d.
For each mode, the audit first accumulates **integer numerators** across
active row/components:

    c numerator     += m*m
    tau numerator   += n*(2*abs(m)+n)
    alpha error     += alpha*((2*abs(m)+2*n)/d + alpha)

Only afterward are the first two sums divided by d^2 and all three sums
multiplied by the mode pair weight. Thus tau is
`2*abs(center)*tau+tau^2`, and the separate alpha contribution is
`2*abs(center)*alpha+2*tau*alpha+alpha^2`. These equations follow by expanding
the deterministic square-error bound; they do not rely on implementation
agreement. The common integer denominator route differs from both the
primary per-component Fraction expansion and the product validator's
successive Fraction square differences, while sharing the accepted theorem.

Interior weight is two. Nyquist weight is one, and only its real component
is active: imaginary center, tau and alpha are all omitted analytically.
The saved DC and Nyquist imaginary rectangles must contain zero. DC evidence
is retained in row identities; only the true constant-annihilated operator
action is omitted. No midpoint DC or Parseval record is overwritten or
recalculated. Alpha is inherited from RI96, not regenerated from raw
coefficient intervals. Every original endpoint encoding is checked, including
the retained initial Q256 input intervals and their complete array identities.

All 8,192 mode records and all 24,576 scalar entries are compared with strict
JSON type equality. The source visits all 65,544 retained rectangles; there
are 131,064 active real components in the non-DC sum. It does not select
favorable modes or assume independent errors.

Each original binary64 PSD is authenticated from all 8,193 canonical
`float.hex` strings and their exact little-endian byte digest, including the
original signed-zero bit if present. Conversion by `as_integer_ratio` gives
an exact dyadic value. Eigenvalues are fs*p at DC/Nyquist and fs*p/2 at
interior representatives. All four full 8,193-entry eigenvalue arrays are
reconstructed; the separate pair multiplicity is not absorbed into them.
Only non-DC entries enter each of the exact dot products C,E_tau,E_alpha.

For every scenario the independent calculation reconstructs:

- E=E_tau+E_alpha and raw `[C-E,C+E]`, retaining any negative lower endpoint.
- All fourteen exact minima/maxima and **all** tied indices of the unchanged
  bands. Spectral spread is reconstructed from `sum_b(u_b-ell_b) sum_k c_k`
  and independently compared with `trace(C_plus-C_minus)`.
- The old raw trace from both complete symmetric 8-by-8 C matrices and the
  inherited nonnegative delta values; matrix margin is
  `8*(delta_plus+delta_minus)`. Spread+margin must equal its width.
- The required one-sided `direct_upper <= old_raw_band_upper` identity gate,
  the preserved prior scalar trace intersection, and exact intersection with
  the new raw interval. An empty intersection refuses; it never retunes bins,
  clips endpoints, substitutes a floor or changes a tolerance.
- Raw/prior/final widths, two exact equality flags and all five ratios.
  Zero width denominator means null/`zero_width_denominator`; nonpositive
  lower endpoint means null/`nonpositive_lower_endpoint`. A positive point
  interval has upper/lower one but still undefined width division.

No minimum improvement is required, and direct lower dominance is not a
gate. The prior matrices and intervals remain accepted enclosures; the audit
checks their used scalar arithmetic and spread identity, not a new Loewner
proof or original full matrix reconstruction. The full RI96 body authenticates
unselected fields, while its accepted transform/row/covariance premises
remain explicitly inherited.

The whole RI100 result is reconstructed: exact ten top-level fields, method,
provenance, 11-gate inventory and typed counts/results, complete mode and
scenario objects, inherited projection/provenance identities and literal
limitations. Its complete canonical identity must equal the actual body;
This RI100 schema has exactly **ten** top-level sections.

## 2. Exact types and serialization

No scientific JSON decimal floats, NaN/Infinity or duplicate keys are allowed.
Plain integer metadata excludes booleans. Rational pairs are canonical
lowercase signed-hex numerator/positive-hex denominator, reduced by gcd;
zero is `0`, not `-0`. All Q256 endpoints use the same canonical integer
encoding. The inherited integer ceiling is 262144 bits. Completed guarded
integer and Fraction operations check their result bounds; Python's internal
allocation or intermediate multiplication is not promised to have a hard
bit or memory cap.

Scientific canonical JSON is sort_keys=True, indent=2, ensure_ascii=True,
allow_nan=False and exactly one LF. Canonical identity uses streaming JSON
encoding to avoid an extra full encoded copy. Documentary metadata containing
actual timing floats uses its frozen canonical format; original outer tool
records are hashed opaquely, because their historical formatting is not a
scientific serialization gate.

## 3. APIs, actual descriptor and deliberately unbound template

`reconstruct(ri96_body, result_body, result_identity, expected_provenance)`
is the separately written scientific operation. Both complete immutable
bodies bind before either scientific parse. It returns an audit payload,
not an execution authorization or a substitute custody review. Actual callers
must use the complete `main()` admission, not call this function to bypass it.
There is no tiny-data mode, fabricated-result acceptance or standalone FFT.

The only CLI is one future supervised normal invocation:

    <qualified interpreter> -I -B audit_saved_result.py AUDIT_INPUT.json

Captured execution may preserve the exact original `__file__` and argv path
bound in the descriptor, as in prior reviewed callers. The adapter must pin
source and descriptor before loading/calling `main`; this module creates no
process, imports no capture helper and implements no supervision loop.
Optimization must be zero; no extra audit replay is implied.

The closed descriptor schema is `ri100-independent-scalar-audit-input-v1`.
Its exact fields are:

`schema,status,auditor,contract,source_reviews,completed_custody,ri96,ri100,ri100_optimized,expected_provenance,output`.

Concrete status is `issued_for_separately_authorized_saved_audit`. It is a
root-issued descriptor, not the separate execution authorization. File refs
are exactly `{path,bytes,sha256}` with an absolute canonical nonsymlink regular
path. `source_reviews` contains at least two actual complete review refs,
including root and separate review; source text does not invent their verdicts.
`auditor` is the exact executing source and `contract` this complete note.
`ri96` names the original RI100 caller's immutable input copy; `ri100` and
`ri100_optimized` name the original completed mode outputs. Output is a fresh
absolute path in an existing canonical directory, created exclusively.

`DESCRIPTOR.source-only-template.json` leaves actual output/bridge/review/
authorization-related slots null or empty. It cannot admit `main()`. Source
and contract pins can be materialized after stable review; future source
reviews and real result/bridge identities must be genuinely issued by root.
A copied output or digest without its completed original execution chain is
insufficient. All prior failures remain retained; no retry is implicit.

## 4. Completed producer custody bridge

Root must issue and pin a canonical bridge with schema
`ri100-root-completed-custody-bridge-v1`, status
`accepted_both_mode_custody_pending_independent_arithmetic`, and
`arithmetic_accepted:false`. Its closed fields are:

`schema,status,arithmetic_accepted,producer_freeze,source_acceptance,input_custody,qualification,normal_acceptance,independent_custody_review,raw_monitor_review,modes,full_result_equality,expected_provenance,inherited_premises`.

The three exact `inherited_premises` strings are exported as source constant
`BRIDGE_PREMISES`; they distinguish accepted genuine execution custody,
accepted RI96 mathematics and root-only later audit admission. The source
acceptance is the actual 3,102-byte RI100 root decision at
`ri99-root-review-osb8owly/RI100_ROOT_SOURCE_ADJUDICATION.json`, SHA256
`5695a96d24db24e17df032670cf175b6e848c34dc60883b73600250e9285464c`.
All paths here are under `/Volumes/AI_DATA/development/det-review-evidence/`.

For each of `normal,optimized`, `modes` contains exactly
`authorization,outer_completion,outer_exit_code,receipt,worker_receipt,custody,attempt,stdout,stderr`.
Everything except the typed outer exit zero is a full path/byte/SHA256 ref.
Root must independently authenticate genuine original outer-tool occurrence,
normal-before-optimized authorization and accepted normal prerequisite; the
consumer reopens their exact documentary bytes, but cannot prove a tool
actually ran by hashing a hand-written record. That occurrence and provenance
remain the bound root/independent completed-custody review premise.

`full_result_equality` is exactly `{byte_equal:true,common_identity:<pin>}`.
The consumer separately compares both complete actual output streams, not
just hashes. Its expected provenance equals the actual frozen caller's
provenance, including genuine runtime and the historical pre-execution input
custody pin. That input admission must still say
`actual_application_executed:false`; it is not retroactively rewritten into
the new completed bridge. Qualification acceptance remains the genuine RI98
4,283-byte decision at SHA256
`312e023d13618f3343cbbbdd042656cf56a329e44a9768ed278da0042080aee9`.

The accepted 65,470-byte RI100 source template is pinned at SHA256
`3f0ea0d4953c5e52564dbe8637e12759d58d487c037dcc890356eddd3730b3b0`.
The actual application freeze may differ **only** in the authorized status,
`evidence.input_custody` and `provenance_template.acceptance.custody`.
Historical preparation_boundary remains identical. This exact delta was
confirmed by root during preparation. Any other change requires preserved
source/contract review rather than a permissive runtime exception.

The consumer reopens all 49 original/copy source pairs, three helpers,
79 historical records and complete evidence refs. It independently walks
and matches the whole 3,925-file runtime inventory (152,961,716 bytes),
including pinned pycs, all named-interpreter links and its resolved target.
It repeats the complete closure after scalar arithmetic and checks stable
file dev/inode/size/mtime plus byte hashes through final completion. Upstream
scientific reports in this closure are read as opaque bytes; only the fixed
RI96 and actual RI100 scientific bodies are parsed.

For each actual mode it reconciles complete before/after source, runtime,
acceptance and input capture records; fixed argv/env/freeze/resource settings;
worker/child zero exits; full saved product-validator return; all saved output
bindings; empty stderr; and parent verified custody. Product-validator success
is a genuine executed prerequisite, never the independent scalar oracle.

Every saved raw ps observation is parsed again. RSS values, ordered timestamps,
all successful samples/gaps, sampled peak, final sample-to-reap gap and final
terminal observation are reconciled against the actual receipt. The limits
remain 180 active-child seconds, 524288 KiB sampled **sole-child** RSS,
0.025-second target polling, 0.1-second maximum/final gaps and 0.05-second ps
timeout. The timeout and sampled child identity are enforced by the exact
accepted caller and bound custody review; they are not separately measured by
this file. This is neither native owned-group monitoring nor a hard allocator
cap. The auditor introduces no alternate limits or supervisory process.

## 5. Required later execution preparation and retained output

Root must accept the complete independent source and contract before a
minimal separately reviewed supervision adapter is prepared. Reuse the actual
qualified 180s/512-MiB mechanism, with frozen sources/runtime/input closure,
exact argv/environment, exclusive attempt/report/stdout/stderr/runtime/receipt
paths, failed-attempt preservation and owned-child cleanup unchanged.
Source/contract review does not admit the actual scientific call. A real
root-issued descriptor, accepted completed producer bridge, explicit later
freeze/authorization and original outcome pins are all required.

The audit writes exactly one exclusive canonical report and streams identical
bytes to stdout. Source changes or partial writes are failures and retained;
there is no in-module retry or destructive cleanup. Successful return alone
does not establish own execution custody: the supervisor's raw samples,
actual parent/child and outer-tool exits, pre/post runtime/source/input pins,
exact report/stdout equality and independent completed review remain a later
required evidence step. Nothing in this source contract asserts those facts
already exist.

The report contains exact ten reconstructed result-section identities,
complete reconstructed scenarios, row/DC/Nyquist operand identities, all
coverage counts, scalar decomposition evidence, both actual mode custody
summaries, original descriptor/source/input/bridge pins and the final complete
reopened-file inventory identity. It does not duplicate every full mode body:
those 8,192 records are compared individually and bound again by the whole
reconstructed RESULT identity, while the original complete bodies remain held.

## 6. Source-review anchors and scientific limits

The RI97 analytic identities already explain tiny Q1–Q11. This auditor's
normalization gives Q1 C=14, Q2 C=12, interior-only C=4, Nyquist-only C=10
and DC-only exact zero. For Q6, center3/2,tau0,alpha1/2 gives c=9/4,
h_tau=0,h_alpha=7/4; lambda4 gives raw[2,16]. For Q7,tau1/4 gives
h_tau=13/16,h_alpha=2, raw[-9/4,81/4], with prior[4,16] unchanged.
Q8 separates band spread8 from zero direct width. Q9 gives matrix margin192
versus direct raw width24. Doubling all response/radius operands scales
quadratic quantities fourfold, preserving defined ratios and undefined
branches. These are hand-algebra source-review anchors, not claimed new
fixture executions or artificial actual-body reports. Existing genuine
RI98 qualification and independent retained-evidence review remain pinned
prerequisites; no new generic qualification campaign is proposed.

The result is conditional centered discrepancy energy summed over eight
selected coordinates of the same finite four-second circulant proxies.
It neither validates PSD-estimation uncertainty, detector-noise covariance,
stationarity, Gaussianity, independent detectors, physical calibration or
mean-zero adequacy, nor bounds all 2769 outputs. It retains the already used
32-second development/calibration status, nominal V2/C02, blank literal
Yunits, clear L1 NO_CW_HW_INJ flag, below-10-Hz and wraparound limitations.
No SNR, p-value, native forward map, geometry/gravity or RET result follows.
Protected validation and physical/experimental prerequisites are unchanged.
