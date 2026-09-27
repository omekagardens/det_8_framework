# RI125 bounded primary white controls — unexecuted source inventory

Executable source: white_controls.py. This is primary test infrastructure,
not an independent validator or an executed report. Its entry is
`run_controls(directory)` with a new absent literal external directory supplied
by a separately admitted caller. It creates only explicit fabricated control
files, retains changes/partial output as evidence and performs no actual input
read. This source has never been imported, compiled, probed or run.

The exact order is WK38; WC01–WC26; WG01–WG92; WC27–WC46; WT01–WT03.
There are **142 declared controls**: 139 isolated first-refusal checks and
three positive failure-tail checks. This is not the complete 32-case application
qualifier, nor a new runtime/caller campaign. Prior WK01–WK37 remain stipulated
kernel controls requiring the eventual complete primary/independent qualifier.
Each first-refusal checks both exact code and exact message, so a later refusal
with the same broad code cannot accidentally qualify the intended guard.

| Id | Concrete isolated operation in source | Required first code/message |
|---|---|---|
| WK38 | Full W01 Gram with self-consistent mutated Shift K=3,E=0,pol=3,direct=[3,3],trace=3,n=2 | STRUCTURAL / trace structural interval intersection |
| WC01 | Only actual request phase changed to fabricated | PHASE / actual phase before body decoding |
| WC02 | Empty request | SCHEMA / closed object keys |
| WC03 | `run_white(b'{}',wrong whole-request pin)` | returned INPUT / externally frozen request bytes |
| WC04 | Change literal capture digest in metadata-only request | INPUT / fixed historical pin capture |
| WC05 | Omit validator source role | SOURCE / closed object keys |
| WC06 | Wrong loaded primary path | SOURCE / loaded primary path |
| WC07 | Wrong loaded kernel path | SOURCE / loaded kernel path |
| WC08 | Empty admission candidate | ADMISSION / exact root-bound card |
| WC09 | Pin byte count is bool | INPUT / positive bounded pin length |
| WC10 | Uppercase digest | INPUT / lowercase sha256 |
| WC11 | Relative path | INPUT / literal absolute nonsymlink path |
| WC12 | Duplicate JSON key | SCHEMA / duplicate JSON key |
| WC13 | Decimal-number token | EXACT / decimal or nonfinite JSON token |
| WC14 | NaN token | EXACT / decimal or nonfinite JSON token |
| WC15 | Incomplete JSON | SCHEMA / invalid bounded JSON |
| WC16 | Integer token of 65538 digits | RESOURCE / JSON integer text ceiling |
| WC17 | Owned one-byte file against wrong digest | INPUT / whole body pin |
| WC18 | Owned file changed after initial state | CUSTODY / path state changed |
| WC19 | Owned symlink instead of literal regular path | INPUT / literal absolute nonsymlink path |
| WC20 | Owned file with a second hard link | INPUT / regular single-link source or input |
| WC21 | Historical metadata mode fixtures_only | RI73 / full inherited header mode |
| WC22 | Historical metadata wrong source identity | RI73 / full inherited header source_identity |
| WC23 | Reverse literal gate inventory | RI73 / full inherited header gate_inventory |
| WC24 | Metadata passed count 91 | RI73 / full inherited header gate_counts |
| WC25 | Remove last gate record | SHAPE / exact list length |
| WC26 | Replace first gate id | RI73 / literal 92-gate order |
| WG01–WG92 | For each exact historical id in RI73_GATES order, change only its passed flag to false | RI73 / all inherited gates passed with details |
| WC27 | Attempt actual capture pin through fabricated route; nonexistent path | PHASE / actual capture forbidden in fabrication, before file access |
| WC28 | Fabricated capture header N=2768 | ROW / literal capture header |
| WC29 | First row label True | ROW / fixed row order |
| WC30 | Extra row key | ROW / closed object keys |
| WC31 | Empty short array | SHAPE / exact list length |
| WC32 | Extra whitespace in row serialization | CANONICAL / compact row encoding |
| WC33 | Duplicate row key | SCHEMA / duplicate JSON key |
| WC34 | Reversed first long interval | INTERVAL / ordered endpoints |
| WC35 | Leading-zero scalar | EXACT / canonical signed hex |
| WC36 | Only one complete row | ROW / row separator |
| WC37 | Ninth complete row after eight | ROW / capture footer and ninth-row exhaustion |
| WC38 | Trailing newline after exact compact capture | ROW / trailing capture bytes |
| WC39 | Same-length wrong footer schema v0 | ROW / capture footer and ninth-row exhaustion |
| WC40 | Unclosed row exceeding 8 MiB | RESOURCE / capture row byte ceiling |
| WC41 | Deliberately different metadata vector identities at bind_row | BINDING / capture vector identity tied to accepted RI73 result |
| WC42 | Vector metadata equal but row-sum metadata differs | BINDING / complete row sum tied to accepted RI73 result |
| WC43 | Existing owned output | OUTPUT / output absent before exclusive open |
| WC44 | Serialized object exceeds 64 MiB | RESOURCE / serialized byte ceiling |
| WC45 | Wrong fabricated context | PHASE / fabricated context |
| WC46 | Invented fabricated case id | DOMAIN / fixed fabricated assembly case |

The historical metadata scaffold contains no coefficients, no numeric Gram and
no complete reconstruction. It cannot be accepted as a historical report, is
never serialized as one, and is never supplied to run_white. Its conspicuous
MALFORMED_CONTROL_ONLY markers distinguish guard-unit inputs from evidence.
Every WG mutation must hit its own gate check **before** the intentionally
empty reconstruction fails. Request scaffolds likewise contain unused paths
and are never written as active requests/admissions. Only WC03 calls the actual
entry, and its wrong external request pin refuses before request parsing.

WT01 registers two owned inputs, reads both, changes only the first, and calls
the same Ledger.finish used by the actual wrapper: the first result must fail
and the second must still pass. WT02 passes those results with an earlier EXACT
error through the actual finish_attempt function and requires that first code
to survive. WT03 supplies apparent success and the same failed postcheck list;
the same actual tail must null the result and report CUSTODY. The complete
postcheck/refusal records are retained. They do not manufacture scientific
acceptance or run numerical fixtures.

The control result schema is exactly {schema:"ri125-primary-white-controls-v1",
phase:"fabricated_qualification",context:literal,
actual_scientific_input_opened:false,independent_validator_run:false,
controls:ordered records,counts:{total,passed,failed},status:literal}.
First-refusal records have id,expected_code,expected_message,observed_code,
observed_message,passed. WT01 has id,passed,postchecks; WT02/WT03 have
id,passed,refusal. Status is all_declared_controls_passed iff every record
passed; otherwise control_failure. This module returns the complete result to
its future caller; it does not write an acceptance card or overwrite a report.

The independently authored validator must have its own header/parser/operand/
arithmetic comparisons and corresponding controls. These primary calls cannot
stand in for that independent execution. Full fabricated cases, positive source
and input admission, actual complete runtime/closure/watchdog/outer completion,
periodic and join paths, and fresh saved-result comparisons remain additional
obligations. No control is evidence of actual captured coefficient evaluation.
