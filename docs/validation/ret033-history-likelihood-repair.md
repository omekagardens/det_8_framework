# Two-sample history likelihood repair

The history-distinction helper used both samples to fit a common probability law but included only the first sample in its likelihood-ratio statistic. It now includes both contributions. For the fixed binary-count example A=(16,4), B=(50,50), exchanging both groups and their sample sizes preserves the statistic and diagnostic verdict.

The sample-size-weighted pooled law, function signature, return keys, degrees-of-freedom calculation and reference cutoff are unchanged. All source bytes outside `test_history_distinction` are preserved. The local documentation now distinguishes a reference-cutoff diagnostic from calibrated inference: non-exceedance establishes neither equality nor predictive sufficiency. Generated kernels with nominal counts remain distinct from sampled observations.

## Observed checks

One admitted run on November 1, 2026 at 21:06:02 UTC passed two fixed unittest methods, containing four helper calls:

- The unequal-sample table and its complete group swap agree with `32 log(16/11) + 8 log(4/9) + 100 log(100/99)` to absolute tolerance `1e-12`, and both exceed the unchanged binary reference cutoff.
- Equal laws with totals 20 and 100 give exactly zero and matching false diagnostics in both group orders.

The expected expression comes directly from the count table, without calling the implementation's row-statistic helper. The source and test design passed separate review; the controller and external observer also passed distinct review before execution. The release additionally requires independent review of the actual evidence and assembly before coordinator adoption and publication.

The executed test loaded the frozen adjacent candidate. The published model is byte-identical to that candidate. The published test changes only its first docstring sentence to remove prospective wording; its loader and test bodies are unchanged. Its repository-relative fallback layout and the complete `run_t1` driver were not executed. The [machine-readable check record](ret033-history-likelihood-check.json) supplies exact identities and observations.

The complete controller invocation took 0.106653708 seconds. Completed-child retrospective peak RSS was 19,660,800 bytes on Darwin. These observations do not establish a hard memory limit, whole-job accounting, speed advantage or M38 runtime qualification. The rounded unittest duration excludes setup and must not replace the complete interval.

## Scope

These are fixed synthetic count-table regressions. Malformed inputs, zero totals, arbitrary dimensions, shared-zero category handling, custom bin choices and general cutoff behavior remain unqualified. No finite error-rate calibration, p-value, power, empirical history effect, scalar-state sufficiency or native physical claim follows. The existing transport/rank/generator functions are unchanged; this repair does not endorse all module-level claims.
