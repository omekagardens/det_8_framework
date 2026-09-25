# RI90 independent saved-result arithmetic audit — source-only contract

25 September 2026 UTC. No audit, target, numerical fixture, actual RI83/RI73
value read, or saved application has been executed by this preparation. This
packet does not authorize its own invocation. Root must independently review
the source, bind a completed result and its custody, freeze the exact invocation,
and admit the bounded execution. The repository is unchanged.

## Exact scope and independence

`audit_saved_result.py` is a standalone standard-library implementation. It never
imports the producer, published validator, qualifier, supervisor or another
local module. It neither reconstructs filter coefficients nor runs a PSD,
FFT, HDF5 parser, simulation, score or physical-noise model. The arithmetic is
exact `Fraction` arithmetic with the accepted 262144-bit bound on every parsed
and derived rational operation. The output domain is precisely the four held
H1/L1 left/right scenarios, M=16384, fs=4096, eight retained operator rows and
rho <= 10^-12. There is no fallback, adaptive subset, ridge or threshold change.

Closed metadata constants were transcribed from literal AST assignments in the
accepted consumer, without importing it. `REFERENCE_CONSTANTS.json` records the
exact source pin and the full transcribed data. These include schema labels,
fixed input/source identities, 92 held gate identifiers, method/metadata
requirements and claim limitations. Copying these contract literals is not an
independent calculation. All numerical reconstruction below is newly authored
in the auditor. References are the accepted RI86 design, RI87 consumer and
validator, and the completed independent RI87 saved-fixture review. Source and
reference identities are retained in the handoff.

The auditor independently:

- Decodes every one of the four original 8193-bin mean PSD records from canonical
  finite binary64 hex, preserves signed-zero byte identity, reconstructs the
  complete little-endian SHA, and converts each value to an exact dyadic.
- Maps DC/Nyquist by fs and interior bins by fs/2, keeps every one-sided non-DC
  eigenvalue, and verifies the independently weighted full spectral trace gives
  the same q_proxy=(1/4)sum(p). It excludes DC only from the output-action extrema,
  under the accepted A1=0 premise.
- Derives all exact minimum/maximum values and every tied index, paired-interior
  positive/zero counts, full/non-DC spectral ranks, output rank upper bound,
  positive/zero/unresolved status and singularity conclusion.
- Computes every entry of ell(1-rho)G and u(1+rho)G, all diagonal pairs and trace
  pairs, and each exact difference from the saved rounded binary64 q. It does
  not compute Omega itself or turn off-diagonal entries into scalar intervals.
- Selects the unique held `integration:gram` certificate, checks every ordered
  predecessor gate label/pass flag and the held fixed model/source identities,
  then independently calculates a unit-lower LDL factorization by exact Schur
  updates and solves the full Gram inverse by exact Gauss-Jordan elimination.
  These calculations do not use the supplied factor or inverse as an oracle.
- Compares the independently solved factor/pivots/inverse to the saved ones,
  directly reconstructs G, computes both GV and VG residuals exactly, and derives
  delta=max row-sum(H), gamma=max absolute row-sum(V), and rho=delta*gamma. It
  checks the fixed rho gate, nonnegative symmetric H, positive pivots, the saved
  inverse-error bound and both saved inverse-envelope matrices.
- Reconstructs the complete closed scientific result from the actual pinned
  predecessor objects and expected provenance. A recursive type-sensitive
  comparison rejects missing/extra fields, differing array entries, integer/bool
  substitutions, noncanonical rationals, phase/schema drift, wrong contexts,
  changed gates or weakened limitations. It compares all four scenarios, the
  projected certificate, every header, seven application gates and all ten
  limitations. Canonical result-byte identity is checked independently.

The full result is rederived, not merely compared with producer booleans.
The audit report retains the reconstructed result identity, source/input and
provenance bindings, exact certificate scalars, all extrema/tie lists, rank
conclusions, diagonal/trace intervals and power differences. It records checks
of 32772 PSD bins, 32768 non-DC eigenvalues, 512 matrix endpoint entries, 64
diagonal endpoint values, eight trace values and four saved-q differences. The
retained original result remains the full array/matrix evidence.

## Fixed bodies and provenance

The pure API is:

```text
audit_saved_result(result_body, ri83_body, ri73_body,
                   result_identity, expected_provenance) -> audit_report
```

The three bodies must be immutable `bytes`. The root-frozen new result identity
and both complete published predecessor identities are verified **before any
of the three scientific bodies is decoded**:

| Input | Bytes | SHA-256 |
|---|---:|---|
| RI83 saved spectra | 38952074 | e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f |
| RI73 held operator certificate report | 11180937 | 3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe |
| RI90 result | To be fixed only after actual completion | To be fixed only after actual completion |

The result parser refuses duplicate keys, decimal scientific literals and
nonfinite tokens. The immutable predecessor bodies admit their published JSON
syntax but reject duplicate/nonfinite/overflowing tokens. Exact held byte
identities remain mandatory. All three bodies are rechecked after arithmetic.

Expected provenance has exactly `sources`, `inputs`, `acceptance`, and `runtime`.
The five scientific source pins are fixed literally to the accepted RI86 design
and four RI87 files. Input pins must be the two fixed actual identities above.
All four predecessor/qualification acceptance pins must be present and non-null;
the phase is only `fixed_saved_application`. Runtime inventory, interpreter and
full fingerprint pins must have their closed positive-size/SHA format, match the
root-frozen expected provenance, and the fingerprint must equal the canonical
identity of the complete held RI73 runtime dictionary. The root's separately
reviewed caller and supervisor establish genuine current runtime equality and
file custody. The auditor does not substitute source metadata for that check.

The complete RI37 metadata report is reconstructed from the retained RI83 input
metadata and checked to its fixed published hash. All method/grid, fixed side
indices, segment flags and original input identities remain bound. L1 injection
mask 23 and clear NO_CW_HW_INJ, blank literal Yunits, prior public access, unequal
seven/six segment counts and the unused right tail are retained. Selected values
come only from `mean_psd`, never ASD, reference PSD or an adaptive replacement.

## Minimal prospective invocation

There is one small CLI, with no general runner or authorization mode:

```text
<qualified-python> -I -B <frozen-audit_saved_result.py>
    <frozen-AUDIT_INPUT.json> <exact-descriptor-bytes> <exact-descriptor-sha256>
```

This is an argument template, not a runnable authorized command. A later
separately admitted wrapper must bind the exact absolute paths, environment,
interpreter chain, complete source/runtime identities and exclusive outputs.
It should reuse the accepted supervision for one worker with wall180s,
sampledRSS524288KiB, poll0.025s, maximum/final sample gap0.1s and ps timeout0.05s.
No execution qualification or resource success for this new audit is claimed.
Root determines the concrete bounded invocation and any serial optimized replay
only after source review; no automatic run or retry is requested here.

`AUDIT_INPUT.json` is a closed canonical descriptor with exactly:

```text
schema: "ri90-independent-saved-audit-input-v1"
phase: "fixed_saved_application"
files:
  result: {path, bytes, sha256}
  ri83:   {path, bytes, sha256}
  ri73:   {path, bytes, sha256}
expected_provenance: {sources, inputs, acceptance, runtime}
custody_premise: {bytes, sha256}
```

All descriptor and file paths must be absolute, resolve literally without a
symlink substitution, and be distinct. Each file is opened as a regular pinned
snapshot with inode/device/size/mtime continuity and complete byte hashing.
Descriptor identity is supplied in the frozen argv; it cannot be silently
rewritten to fit a different result. CLI output is one canonical ASCII JSON
scientific audit report on stdout, flushed/fsynced only after all checks; failures
raise and must be retained by the external supervisor with raw stderr and real
OS/tool exit. The CLI rereads every input and the descriptor after the audit.
Mode/path/time/process receipts stay external to the scientific report.

`custody_premise` names the separately accepted completed caller/input custody
record. It is an explicit external premise: the audit only retains this identity;
the supervisor/root must open, verify and bind the record itself. Neither this
field, descriptor nor a mathematical pass constitutes root authorization. No
actual descriptor is written now, because the RI90 result and completed custody
identity do not yet exist at this preparation stage.

Before issuing that descriptor, root must reconcile both completed RI90 normal
and optimized modes: genuine outer exits, every raw monitoring attempt and
resource gate, complete source/runtime/input bindings before and after, saved
output/custody identities, and exact full scientific byte equality. The outer
audit caller must verify the actual accepted custody record and retain its
identity. A producer status string or one successful mode cannot replace this
prerequisite.

## What a pass does and does not establish

A pass would prove exact agreement of all saved result fields with the stated
finite PSD-to-circulant-envelope calculation under the accepted held operator
and custody premises. Independently recomputed LDL, inverse and rho concern the
projected numerical certificate. They do not reconstruct the coefficient
interval enclosure H, rerun the historical 92-gate computation or establish
that the accepted error matrix bounds the physical world. The exact A1=0 theorem
and the historical coefficient/source proof remain pinned prior premises.

The four empirical spectra, the separately postulated finite circulant
covariances, and calibrated physical-noise covariance remain distinct. No
stationarity, signal-free interval, Gaussianity, detector independence,
confidence interval, physical gravity test or native forward prediction is
established. RET stays paused. A zero lower bound and an unresolved rank remain
valid reported outcomes, not reasons to change the domain.

Current verification is AST syntax/static source reasoning and literal identity
checks only. No helper/target/auditor import, numerical control, observed result
parse or runtime probe has run. Root and a separate reviewer must review the
actual source before freezing or executing this auditor. Publication requires
actual completed audit evidence and independent adjudication, not this note.
