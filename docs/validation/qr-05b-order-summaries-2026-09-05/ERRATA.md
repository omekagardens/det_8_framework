# QR-05B protocol erratum

Recorded 5 September 2026 after capture, before the milestone commit.

The captured README's opening model section incorrectly refers to
"QR-05A's four-event covariance certificate." QR-05A's retained exhaustive
covariance checks cover **at most three births**, not four.

The intended sentence is: **This study does not extend QR-05A's covariance
checks to four births; only the specified one-step continuation questions
are examined here.** QR-05B starts from retained three-birth histories and
computes one subsequent birth. It does not enumerate all four-birth covariance
comparisons.

This is a scope-description error, not a change to the implementation, input
domain, computed results, or acceptance checks. The capture explicitly records
source_births=3 and future_births=1. The source-ledger README is preserved so
the create-only artifact continues to replay against its original exact bytes.
This erratum and RESULTS.md are interpretation documents outside that ledger.
