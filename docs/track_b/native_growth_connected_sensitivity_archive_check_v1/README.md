# Check the published RI-122 archive

From this directory, run:

```sh
python3 -B verify_archive.py
```

Python 3.9 or later and its standard library are sufficient. A fresh checkout
contains both this checker and its sibling result archive. To check another
copy, pass `--archive /path/to/native_growth_connected_sensitivity_result_v1`.
The command reads files and prints a JSON result; it writes no reports or
archive files. It never imports or executes the archived scientific sources.

The pinned manifest records all 117 files published in commit
`3027dc6813b95cc57e8637c6598a6b07325074f0`. Every archived file must be present
with exactly its original bytes; unexpected files and symlinks are refused.
The checker also compares all nineteen reconstructed certificate sections,
complete canonical certificate bytes, both producer summaries and the saved
root decision with type-sensitive equality. Historical trailing blank lines
remain authenticated bytes. No external absolute path in the provenance
records is opened.

Success establishes agreement with this published snapshot and consistency of
its saved objects. It does not independently reconstruct the mathematics,
rerun the experiments, authenticate the publisher, verify the external runtime
or historical closure, or grant permission for another scientific execution.
The [result review](../native_growth_connected_sensitivity_result_v1/RESULT_REVIEW.md)
states the accepted proof, genuine execution evidence and remaining premises.
The published commit and its review remain the basis for trusting the snapshot.

File observations detect ordinary concurrent changes during reads. This is an
offline reproducibility aid, not an adversarial filesystem-custody mechanism.
Use a stable checkout. Scientific, calibration and protected-validation gates
are unchanged.
