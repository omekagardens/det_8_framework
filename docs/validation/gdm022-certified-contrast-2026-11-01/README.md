# Fixed quantum–classical contrast: exact enclosures

The selected formal quantum contrast does not equal the selected classical contrast as a function of the same retained orientation. This is a result about the fixed supplied model and first-order coefficient, not a measured discrepancy or a native DET prediction.

The [model](../gdm020-quantum-contrast-2026-11-01/MODEL.md) fixes conventional Weyl quantization, the full Coulomb Hilbert space, the globally normalized circular-state packet n=140,...,160, its preparation phases, a finite-width Gaussian center, spectator spin, controls, readout and clock. The [finite derivation](../gdm020-quantum-contrast-2026-11-01/CALCULATION.md) gives

    quantum contrast coefficient = K_cl [d_c cos(2φ) + d_s sin(2φ)]
    classical contrast coefficient = K_cl [cos(2φ) + sin(2φ)]
    K_cl = 24 C / (π² a) > 0
    D = sqrt((d_c - 1)² + (d_s - 1)²).

These are coefficients of ε in the normalized B-minus-A response contrast. Both coefficients would have to equal 1 for exact agreement at the same orientation. The accepted [rational enclosure method](../gdm020-quantum-contrast-2026-11-01/ARITHMETIC.md) specifies the normalization, nineteen terms, tails and outward rounding.

## Certified values

Every endpoint below is its hexadecimal numerator divided by **Q=2^128**. The intervals are closed.

| Quantity | Lower numerator | Upper numerator | Width |
| --- | --- | --- | --- |
| d_c | `0xefc3626310e2703a960fe306361cb6c3` | `0xefc3626310e2703a960fe306361cb6c8` | 5/Q |
| d_s | `0xef6fdae25349dbdba5a8d491edc1a11a` | `0xef6fdae25349dbdba5a8d491edc1a11f` | 5/Q |
| D | `0x1731b33ea36a407bb577edf3938345fb` | `0x1731b33ea36a407bb577edf393834705` | 266/Q |

Both d_c and d_s lie strictly between 0 and 1. D has a strictly positive lower endpoint. The uniform absolute discrepancy is exactly K_cl D. This is a supremum over orientation; it does not assert separation at every angle. All three enclosure widths are below 10^-6. The bounds concern arithmetic error under the model, not physical or truncation error.

## Independent evidence

[witness.json](witness.json) is the exact frozen producer artifact. [independent_checker_source.py](independent_checker_source.py) is the exact source used by the separate checker author, after independent source review. [independent_result.json](independent_result.json) is its complete captured stdout. The checker used homogeneous Horner constructions instead of the producer's power tables and term sums, independently reconstructed all 40 exponentials, 19 coefficient/phase pairs and 38 trigonometric terms, and checked exact outward-rounding residuals before clipping. A direct nonnegative square-bracket certificate verifies the root without replaying the producer's bisection history.

The checker completed once on November 1, 2026 at 20:07:39 UTC. Separate arithmetic adjudication completed at 20:13:45 UTC with no required repairs, followed by coordinator numerical adoption. The actual stdout retains its original pending-adjudication marker; this paragraph records the subsequent disposition. Source hashes establish identity, while the model, mathematical checks, actual completed run and distinct review establish the stated conditional result.

The source is an archived exact execution record. Its original candidate header and absolute artifact-location constant are retained to preserve identity; it is not a newly adapted portable command. Changing that location produces a different source version. No additional checker or evaluator run was performed for this publication.

The complete controller invocation took 0.630922292 seconds in this one observation; the completed checker child's retrospective peak RSS was 23,511,040 bytes. These are neither an efficiency comparison nor hard memory enforcement, full-job accounting or measurement-runtime qualification.

## Remaining premises and stopping decision

The supplied operators, contact convention, preparation and formal perturbative order remain assumptions. Machin's identity, Taylor/alternating remainder estimates, derivative bounds, interval arithmetic and the norm inequality remain the accepted analytic premises of the enclosure method. There is no finite-ε remainder or omitted-physics completeness bound.

Individual response laws and unpaired marginals are undetermined by a contrast. Physical preparation/repeatability, matched controls, force calibration, a detector/readout map and empirical observation correspondence remain open. No physical 0-versus-2/3 event transfer, gravity measurement or programme-wide gate release follows.

This exact two-number comparison is closed, and its fixed same-orientation equality candidate is excluded. A new model, packet, clock or observation question needs its own prospective justification and review; repeating this calculation or retuning its inputs is not the next task. Independent research and the separate software repair continue under their own scopes.
