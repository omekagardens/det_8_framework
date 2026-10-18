# Public branch integration

`main` is the public entry point. Published `ret` checkpoints should reach
`main` regularly, with current reader-facing documentation and scoped software
checks. Review branch drift weekly and after a substantial reviewed release.
If the published tips are already integrated, no merge is needed.

## Which history may be merged

Use the freshly fetched **`origin/ret` public lineage** as the source. The local
research branch named `ret` can contain private checkpoint history, machine
metadata, active reservations and unfinished edits. Its name is not evidence
that it is the published branch. Never merge or push that private history into
`main`, and never stage unrelated work merely to make a checkout clean.

The [metadata-obscured publication policy](coordination/REDACTED_PUBLICATION.md)
continues to govern new research publications. An integration carries forward
already published evidence and its limits; it does not publish local-only
results, reconstruct historical custody or certify the science again.

## Integration procedure

1. Fetch `origin/main` and `origin/ret`. Record their exact commits and inspect
   both directions of divergence. If `origin/ret` is already an ancestor of
   `origin/main`, stop without creating an empty merge.
2. Work in a clean isolated checkout based on `origin/main`, on a
   `codex/` integration branch. Preserve the research checkout, its index,
   untracked files and active reservations.
3. Merge the public `origin/ret` tip without committing. Resolve routine
   conflicts against both histories; stop for a substantive scientific or
   publication-policy conflict that cannot be resolved from accepted evidence.
4. Update README, Next Steps, Roadmap and the Model Card where the merged
   checkpoint changes their public summary. Keep historical results historical.
   Link the consolidated statements and distinguish unreviewed or local-only work.
5. Run the relevant maintenance checks below, inspect the final tree and review
   all new integration edits. Existing upstream defects must be recorded and
   distinguished from merge regressions; never weaken a scientific threshold.
6. Commit the reviewed merge and documentation. Re-fetch before publication;
   if either source tip moved, incorporate and recheck the new scope. Use a
   normal fast-forward update of `main`, or a reviewed PR when branch protection
   requires it. Never force-push or bypass required checks.
7. Verify the remote commit and that it contains the selected public `ret` tip.
   Check that the original research checkout is unchanged. Record the integrated
   source commit, maintenance edits, actual checks and any remaining limitations.

Root coordinates Git and index operations centrally; parallel reviewers work
on disjoint documents or perform read-only software review. Archive temporary
integration worktrees once the result is safely published and no longer needed.

## Validation boundary

Integration checks cover Git ancestry/conflicts, the reviewed source delta,
documentation links and applicable offline software contracts. Select tests by
their actual source and side effects; do not run every research directory to
obtain an impressive aggregate count. Python 3.11 or later is required by the
explicit research-registry tools; individual applications can have additional
dependencies.

The following offline maintenance gate uses Python 3.11+ and `pytest`. Install
the test runner in an isolated environment, activate it, and run from the
repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python3 -B -m pytest -q -p no:cacheprovider \
  det8/tests/test_ingestion.py \
  det8/tests/test_clock_chronology_contracts.py \
  det8/tests/test_operational_scripts.py \
  det8/tests/test_review_snapshot.py
```

These tests exercise parsing, chronology, refusal behavior, command-line
handling and byte-integrity checks with synthetic inputs. They do not replay
the actual scientific snapshot. Reinspect their scope when their source changes.
The 18 October 2026 integration ran this command with Python 3.12.14 and
pytest 9.1.1: **145 passed**. This is an integration record, not an expected count
for later revisions or a whole-repository certification.

`python3 run_tests.py` is a broad numerical and research aggregator. The
`scripts/run_research_checks.py` registry and frozen experimental bundles have
their own scope and execution prerequisites. They are not automatic maintenance
gates, and a research pause is not permission to rerun them as merge checks.
Protected validation, preregistered holdouts, actual-data acquisition and RET
research require their existing authorization and controls.

Passing ordinary software tests does not prove the conditional mathematics,
qualify a production environment, establish a native physical forward map or
validate DET empirically. Record counts only for the exact command and revision
that produced them.

## Recurring maintenance

A weekly integration check should merge newly reviewed public `ret` work,
refresh these entry-point documents and verify the remote result. It should
remain quiet when there is no branch drift, and report completed integration,
test failures, publication conflicts or a required decision. Do not start a
research investigation to unblock an unattended merge.

Research usage guards and the RET pause remain unchanged. Separately authorized
repository maintenance may proceed during a research pause; it must not start
research workers, publish unreviewed evidence or bypass platform limits.
