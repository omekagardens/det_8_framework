# RI-90 — saved public-spectrum covariance-proxy result

25 September 2026 UTC. The unchanged qualified RI-87 consumer has actually
processed the fixed RI-83 spectra and RI-73 operator certificate. Both execution
modes agree exactly. A separately written and source-reviewed arithmetic audit
also reconstructs the entire result exactly. Completed-audit custody adjudication
is recorded in the final acceptance section below.

This is a finite covariance-model calculation from already published data. It
does not establish physical noise covariance, calibration, stationarity,
significance or a native gravity prediction. The four spectra, the postulated
circulant covariance and calibrated physical covariance remain distinct.

## Scientific result and usefulness

The [full result](RESULT.json) has 6,994,965 bytes, SHA-256
`c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf`.
It applies the accepted [RI-86 design](../gwosc_colored_covariance_proxy_v1/DESIGN.md)
to precisely H1:left, H1:right, L1:left and L1:right. Each has 8193 saved
binary64 PSD bins; all are converted to exact dyadics. Endpoint eigenvalues use
fs=4096, interior eigenvalues fs/2, and the frequency spacing is 1/4 Hz.
DC is excluded from the output-action extrema under the separately accepted
operator theorem A1=0. No bins are discarded to improve the bounds.

For the same eight operator rows, the result retains every entry of

`ell*(1-rho)*G <= Omega_proxy <= u*(1+rho)*G`

in Loewner order, every tied spectral extremum, rank conclusion, diagonal and
trace endpoint, and exact difference between integrated dyadic PSD and the
previously rounded saved q. Off-diagonal matrix entries are not scalar variance
intervals. The projected certificate has eight positive exact LDL pivots, an
independently solved inverse and zero residuals on both sides. Its exact rho
passes the unchanged 10^-12 gate; rho is approximately 5.552e-56.

All four declared proxies have positive lower eigenvalues and rank-eight output
covariance. That is a statement about the postulated model. The enclosing
matrices are extremely far apart:

| Scenario | Minimum-bin index | Maximum-bin index | Approximate upper/lower scalar factor |
|---|---:|---:|---:|
| H1:left | 8111 | 25 | 4.223e12 |
| H1:right | 8129 | 26 | 4.462e12 |
| L1:left | 8129 | 26 | 2.906e12 |
| L1:right | 8161 | 25 | 7.443e12 |

The displayed factors round `u*(1+rho)/(ell*(1-rho))`; exact rationals are in
the result. They apply to every positive diagonal/trace pair because the two
endpoint matrices are scalar multiples of the same G. The extrema at bins
25/26 correspond to 6.25/6.5 Hz, below 10 Hz, where the inherited calibration
evidence does not justify a calibrated physical interpretation. These bins remain part
of the declared finite proxy. The enormous factor is a practical limitation of
the global spectral envelope, not an arithmetic failure or permission to alter
its accepted thresholds. The result alone cannot provide a useful covariance
adequacy test.

An appropriate next mathematical question is whether the same model can use
certified operator frequency-response information to obtain tighter envelopes.
An empirical model-adequacy test additionally needs independent data and its
own design. The current left/right spectra already reuse the declared public
32-second inputs; they must not silently become independent held-out evidence.

## Genuine executions and independent calculation

Both producer modes used the fixed [qualified implementation](../gwosc_colored_covariance_proxy_implementation_v1/IMPLEMENTATION.md)
and complete validator. The genuine runtime is recovered CPython 3.11.6,
NumPy 2.1.3, SciPy 1.14.1, h5py 3.12.1 and HDF5 1.12.2. The same admitted
interpreter chain, 3925 runtime files, input bytes and complete runtime
fingerprint are bound before and after. The prior RI-87 fabricated qualification
is an explicit prerequisite; it is not represented as observed-data validation.

| Actual execution | Child time (seconds) | Sampled peak (KiB) | Raw RSS samples | Genuine outer completion |
|---|---:|---:|---:|---|
| Normal application | 2.343191 | 273760 | 62 | `607ce3`, exit 0 |
| Optimized application | 2.381167 | 278880 | 65 | `cc9aa7`, exit 0 |
| Independent saved-result audit | 2.779598 | 291552 | 85 | `bbbda4`, exit 0 |

The unchanged envelope is 180 seconds and 524288 KiB sampled child RSS,
with 0.025-second target polling, 0.1-second maximum/final gaps and a
0.05-second ps timeout. This is not an allocator hard cap; parent custody
work is outside the child envelope. All scientific stdout is retained, all
stderr is empty, and both full application outputs are byte-identical.

The published [independent auditor](audit_saved_result.py) is the exact source
used by the actual audit: 41587 bytes, SHA-256
`2f3252d28acde27cdd74adc38e4cb9d068fd65a6f912f120840419f0a6d6f193`.
It imports neither producer nor validator. It uses exact Schur updates for LDL,
Gauss-Jordan elimination for the inverse, and reconstructs every scientific
result field with strict type-sensitive comparison. All three immutable input
identities precede any scientific decoding. The [audit contract](AUDIT_CONTRACT.md)
is preserved verbatim from source preparation; its prospective status describes
that historical stage. This note records the later actual execution.

The complete [audit report](AUDIT_REPORT.json) has 219279 bytes, SHA-256
`cfe2e80862078da49613ec852e81b9b92766755fadc94ac4eab865f1877cb223`.
It rederives 32772 PSD values, 32768 non-DC one-sided spectral representatives,
512 matrix endpoint
entries, 64 diagonal endpoint values, eight trace values and four q differences.
Its reconstructed complete result identity is exactly the original result pin.
The historical coefficient reconstruction, H error enclosure and A1=0 proof
remain pinned predecessor premises; this audit does not rerun those algorithms.

## Inputs and durable execution evidence

| Accepted input | Bytes | SHA-256 |
|---|---:|---|
| [RI-83 result](../gwosc_off_event_spectra_result_v1/RESULT.json) | 38952074 | e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f |
| [RI-73 result](../gwosc_noise_operator_covariance_v1/RESULT.json) | 11180937 | 3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe |

Full scientific and acceptance identities appear in the result provenance.
Durable external records retain the actual machine-specific source/runtime
closure, exact commands, authorizations, exclusive outputs and raw monitoring:

- Application: `/Volumes/AI_DATA/development/det-review-evidence/ri90-execution/preparation-kgakmp9d/`.
  Its authorization is 31158 bytes,
  `18f1acc1878253df2d6360b33ec731afcebafcfbfc21f662c826cabe0d85e370`.
  Normal/optimized receipts are 63666/64434 bytes,
  `e1b8ba903cb93c96f2745e4ef7fa6643f149edaa211c12167de95f86ebb1a8cb`
  and `89620046de53875fa1da9a276086da926169cb02158d4f2e006717a9030ac667`.
- Independent actual application custody review:
  `/Volumes/AI_DATA/development/det-review-evidence/ri90-completed-custody-independent-review-20260925/INDEPENDENT_ACTUAL_CUSTODY_REVIEW.json`,
  9896 bytes, `f04eb6756d4542eb64471114ff8c1c4bfc88801cc5292d9e4f01b936053d0314`.
  It independently rederived all 127 samples and reopened the full byte closure.
- Arithmetic audit: `/Volumes/AI_DATA/development/det-review-evidence/ri90-saved-audit-execution/preparation-a29digd_/`.
  Authorization is 26795 bytes,
  `6954fa07ad86cb0efde4c68c9f6c3214283cf04af8100a070d685e8367fe4a45`;
  actual receipt is 111047 bytes,
  `926fe0a280bbbe58906a20ad5de0f932c105fccf1561cbd0b7047a0253f062df`.
  `ROOT_ACTUAL_COMPLETION.json` retains the genuine outer tool exit.
- Root coordinator evidence:
  `/Volumes/AI_DATA/development/det-review-evidence/ri89-ri90-checkpoint-pf3q_wuy/`.
  The separate actual caller-custody decision is 2432 bytes,
  `f661f7596e9cbfd3193c63c6c2d5ca9362c3216601dc8f5d44a054ca7a5c5707`.

No scientific attempt failed or was retried. Metadata-review corrections are
retained: a reviewer initially treated the prospective null authorization as
an absent key, and a root runtime-inventory check initially omitted existing
pinned bytecode files. Corrected complete comparisons passed with all source,
runtime and scientific bytes unchanged. Neither correction relaxed a gate.

## Remaining premises

The four-second circulant covariance and its long-lag wraparound remain explicit
model choices. Empirical PSD estimates are not a known population covariance.
Noise estimation uncertainty, stationarity, Gaussianity, detector independence,
mean/template adequacy, detector response, timing and calibration remain
separate obligations. Nominal V2/C02 provenance, blank literal Yunits, public
prior access and the clear L1 NO_CW_HW_INJ flag are preserved. No covariance
inverse, whitening, residual score, SNR, p-value, chi-square law, physical
gravity test or native forward map is supplied. RET remains paused.

## Final acceptance

Root accepts this fixed saved-result calculation and its independent exact audit.
The final independent completed-audit review is
`/Volumes/AI_DATA/development/det-review-evidence/ri90-independent-completed-audit-review-8u85hpxm/INDEPENDENT_COMPLETED_REVIEW.json`,
9861 bytes, `11ce24c059ac93d0fd32e3dd1f4c63c73a49a6cea8f45c27e48080a63d8939a3`.
It independently reconciles all 27 audit source pairs, three helpers, thirteen
predecessor acceptance records, 3925 runtime files, 85 raw monitoring responses,
the genuine outer exit, every actual output binding and the complete report
scope. Together with the producer review, all 212 actual samples are reconciled.
This evidence review did not rerun the scientific calculation or claim a third
independent arithmetic implementation.

The root decision is
`/Volumes/AI_DATA/development/det-review-evidence/ri89-ri90-checkpoint-pf3q_wuy/RI90_ROOT_RESULT_ADJUDICATION.json`,
5773 bytes, `ac1cc18491dfd9a9f1bd1bf546f0d0ecea3427eb287238f6c4783f6a3b34cd50`.
The numerical sources/results are published byte-for-byte. The result-note
scope review led to clearer calibration and one-sided-mode wording; no
scientific value changed. RI-92 now separately investigates frequency-resolved
operator bounds under the same proxy premises. No implementation or new
scientific execution for that successor is included in this result.
