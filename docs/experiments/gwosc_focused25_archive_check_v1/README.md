# Check the published RI139 focused-control archive

From this directory in a checkout, run:

```sh
python3 -B verify_archive.py
```

Python 3.9 or later and its standard library are sufficient. To check a relocated
copy, pass `--archive /path/to/gwosc_focused25_result_v1`. The command writes only
its JSON result to standard output, or a refusal to standard error with exit 1.
It does not modify the archive or produce cache files when invoked with `-B`.

The checker pins the complete publication manifest from commit
`878ef6041d937abd4ecdc7b0d4fa9adbc81a5005`, verifies all 135 archive files and 132
original-copy identities, and reconciles all 89 operation files against the saved
complete namespace. Missing, changed, unexpected or nonregular files and symlinks
are refused. Historical empty directories survive as saved namespace records;
they need not exist in a fresh Git checkout. Unexpected empty directories inside
the portable archive are refused.

It checks the saved root decision, 25-case order/counts and outcome assertions,
complete child-completion agreement, all 30 raw monitoring samples and unchanged
recorded bounds, and byte equality of the saved bootstrap observations. It preserves
zero-byte streams and deliberately partial JSON as authenticated bytes rather than
trying to decode every file. Files are capped at 8 MiB, total payload at 32 MiB,
and the portable archive namespace at 512 names.

No original absolute path or dependency-map external/Git operand is opened. The
checker imports or executes no archived source and does not repeat a control,
observe the current scientific runtime or admit an experiment. Its saved agreement
checks are not a new full semantic reconstruction of all control envelopes; those
are covered by the archived independent actual review. Success does not authenticate
the original tool session or publisher, establish an external dependency closure,
prove a scientific claim, or qualify physical calibration or a native forward map.
The published commit and [accepted review](../gwosc_focused25_result_v1/actual_review/INDEPENDENT_ACTUAL_REVIEW.md)
remain the basis for trusting the snapshot.

Use a stable local checkout. Ordinary file changes during reads and namespace
changes are detected; this is an offline reproducibility aid, not an adversarial
filesystem containment or custody mechanism. The interpreter and standard library
used to run this utility remain the reader's own environment.
