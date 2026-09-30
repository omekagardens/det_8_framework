# RI160 exact late-fixture control contract — source only

All22 new IDs append after the complete original84. No execution, syntax test,
fixture generation or claimed pass occurred. `final_fixture_case` calls real
`adapter.run_authenticated` once; prior authenticate and action are explicit
private substitutes. The I/O proxy records every actual runner observer/write and
injects a mutation only at `tree:owned-output`, after both individually registered
fixture observations. No request-selectable callbacks or module-global patches
are added to production.

The fixed inert trees each contain exactly a directory root, regular alpha.txt
with literal bytes `INERT fixture alpha\n`, symlink link targeting alpha.txt, and
empty directory nested. The control independently asserts all exact rows against
those literals and their byte hashes; it does not derive expected final rows from
the changed scan. Complete final rows are reconstructed by the stated literal
mutation recipe, sorted once and compared in full to both raw prefixed rows and
normalized receipt rows. No scientific object or historical credential is used.

Eight mutations are used independently on each root: bytes replaces alpha's
literal body with `INERT fixture beta\n`; add writes extra.txt with `INERT new
member\n`; delete renames alpha outside the owned output; missing_root renames
the whole root outside that output; file_type preserves alpha by rename then
makes an empty directory of that name; link preserves the old link by rename and
creates link targeting nested; root_file preserves the old root by rename and
writes `INERT root replacement\n`; root_link preserves the old root by rename
and creates the literal dangling target INERT_missing_target. Retained renames
stay inside the private per-case root, never an external source or original.
In-place byte mutations remain reconstructible from literal source/expected rows.

For all17 ordinary final-scan cases (positive plus16 isolated mutations), the
complete exact runner trace requires both individual fixture calls immediately
before the whole-tree call, exactly one action, one whole final scan and one final
COMPLETE write. Every earlier tail must have error=null and its complete expected
rows must survive unchanged. Changed final normalized/raw records, complete
member/output/fixture mismatch arrays and the exact final/primary error are all
asserted. Added/deleted membership, empty/missing root, hashes, types and link
targets are compared; no boolean pass label substitutes those assertions.

| ID | Mutation/root | Required first outcome |
| --- | --- | --- |
| L01_both_unchanged | Neither | code0, no error, both full final equalities true |
| L02_inert_bytes | inert-fixtures bytes | final namespace control fixture tree inert-fixtures |
| L03_inert_add | inert-fixtures add | final namespace control fixture tree inert-fixtures |
| L04_inert_delete | inert-fixtures delete | final namespace control fixture tree inert-fixtures |
| L05_inert_missing_root | inert-fixtures missing_root | final namespace control fixture tree inert-fixtures |
| L06_inert_file_type | inert-fixtures file_type | final namespace control fixture tree inert-fixtures |
| L07_inert_link | inert-fixtures link | final namespace control fixture tree inert-fixtures |
| L08_inert_root_file | inert-fixtures root_file | output member type; also complete fixture mismatch |
| L09_inert_root_link | inert-fixtures root_link | output member type; also complete fixture mismatch |
| L10_integration_bytes | integration-fixtures bytes | final namespace control fixture tree integration-fixtures |
| L11_integration_add | integration-fixtures add | final namespace control fixture tree integration-fixtures |
| L12_integration_delete | integration-fixtures delete | final namespace control fixture tree integration-fixtures |
| L13_integration_missing_root | integration-fixtures missing_root | final namespace control fixture tree integration-fixtures |
| L14_integration_file_type | integration-fixtures file_type | final namespace control fixture tree integration-fixtures |
| L15_integration_link | integration-fixtures link | final namespace control fixture tree integration-fixtures |
| L16_integration_root_file | integration-fixtures root_file | output member type; also complete fixture mismatch |
| L17_integration_root_link | integration-fixtures root_link | output member type; also complete fixture mismatch |
| L18_primary_both | returned primary error, then late inert bytes + integration link | INERT primary fixture action failure; both independent late mismatches |
| L19_ordinary_both | late RESULT bytes + inert bytes + integration link | final namespace produced pin RESULT.json; both fixture mismatches still collected |
| L20_primary_ordinary_both | returned primary error, then same three late changes | INERT primary fixture action failure; all three late mismatches retained |
| L21_partial_no_expectations | action makes both trees then raises before returning | INERT primary fixture action failure; only ATTEMPT pin, no RESULT or invented expected comparisons |
| L22_success_without_expectations | nominal success omits both expected trees | complete captured control fixture expectation inert-fixtures; both unavailability refusals, no success |

All messages except explicit INERT primary messages have literal `RI156_IO: `
prefix; their type is ValueError. Every nonpositive row requires code1 and
REFUSED_RETAIN_ALL_PARTIALS. L18/20 return the stated primary through the existing
first_error action field while keeping status ALL_DECLARED_PASSED; this exercises
the runner's real preservation of a returned earlier failure. L21 raises the same
error before returning, so no action expectation exists. L21/22 intentionally
have no independent fixture-tail calls; their complete raw/normalized partial
trees remain and availability is false/false/null for each root. L21 has no late
mismatch/namespace error, but its prior error and nonzero result must remain;
L22 refuses both missing expectations. These are distinct boundaries, not false
late-drift credit.

Root file/link cases retain the original structural first error but must also
record the later full fixture equality failure. L19/20 prove an earlier ordinary
mismatch cannot short-circuit either fixture comparison. All earlier applicable
source/card/request/dependency/output/fixture tails are checked, with complete
ordered trace and exact registered tail set. Both full earlier fixture rows are
asserted where applicable, not merely asserted as observer calls. The complete
receipt, trace, mutation list, fixed rows, final scan and whole private-case tree
are returned as evidence; failures retain their private filesystem in the outer
full integration tree. All original29 case/helper bodies remain exact. C02 may
now also have a final fixture error after its earlier fixture-tail failure; its
unchanged original assertion requires the same earlier first error and the
unaffected second individual fixture tail.

The future combined report is106 rows (55+29+22). Row shape remains
{id,passed,evidence,error}; every prospective call is fresh, no old result is
copied. Group counts/order and full expected fixture namespaces bind the complete
report. Current SOURCE_SET/106 IDs, fresh nonauthor review/root source decision,
genuine admission/actual monitored execution and independent complete outcomes
review are prerequisites. These controls do not cover authentic bootstrap/source
admission, operational normal/optimized execution, scientific arithmetic, RI131,
actual15 WHITE, full32, public data, calibration or native claims.
