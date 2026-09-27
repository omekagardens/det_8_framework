# RI119 preparation and review record

This is a source-writing record, not numerical evidence. Target source has not
been imported, compiled, AST-processed, probed or run. No scientific JSON result
or execution receipt was created. Source text was read in full; metadata tools
only read/write text, JSON provenance metadata or hashes. All changes are inside
this external RI119 reservation. Repository/index/git remain root-owned.

The parent authored primary.py, qualify.py and the contract. A distinct agent
`ri119_independent_validator` authored validator.py before reading primary.py,
using only the literal contract and accepted RI118 design. Its initial source
handoff was23,192 bytes/SHA256a85873ccbc9b5cf8227bebb9badcdef947489530eacac779ed196a90f1ec4510.
After parent text review, that author harmonized strict nonnumeric-string types
and global shape-before-dimension guard ordering; that independently authored
state was23,301 bytes/SHA256600b80ceabb417df065b0d1009764ff11d5baacd8e28dc138fb3e3ef052023cd.
Both handoffs were source-only.

Separate complete reviewer `ri119_full_source_review` then read all source.
It found no fixed-case mathematical discrepancy and identified two general
resource guard differences, both corrected before freeze:

1. Parent moved primary's decimal component-length checks before regex,
   matching validator's oversized-malformed-input first refusal. Added M33
   with2468 nonnumeric characters and expected RESOURCE.
2. Validator initially checked only the reduced PSD determinant difference.
   Parent changed the single expression from `_bounded(a*c-b*b)` to
   `_bounded(_bounded(a*c)-_bounded(b*b))`, keeping the same mathematical
   determinant and short-circuit checks. This precise non-scientific guard
   edit was made after the independent author's follow-up was unavailable
   because the agent thread limit was reached; root authorized parent repair.
   Added G03 with all four entries2^4096, whose individual products exceed the
   arithmetic bound before cancellation. This mathematically PSD input is
   refused for RESOURCE, not falsely classified as non-PSD. Independent
   scientific authorship is retained; the guard-only parent edit is explicit.

A further parent coverage question noted that sign-flip outputs cannot be
verified solely from second moments. Separate review agreed to require explicit
per-sign checks. Parent added actual A row-sum and same-sign zero-mean output
checks for Q06, and signed scale times same-sign baseline output checks for both
Q08 cases. These execute before the vector is counted if the source is later
admitted; no sign cube has been enumerated now. Full result schema is unchanged.

The separate final text review is recorded in SOURCE_REVIEW.md; its status and
SOURCE_PINS.json identify the actual reviewed final bytes; the earlier numbers in this record are
historical checkpoints, not active source pins. The final41 controls per
implementation are declarations of intended results until genuine qualification.
No claims of runtime fit, zero exit, normal/optimized equality or downstream
physical validity are made by this record.
