# Inert qualification cases for the grid audit

These are future case specifications, not fixtures, executed tests, a runnable
harness or scientific results. Zero qualification cases have been executed in
this packet. Separate root authorization is required before constructing any
synthetic input, importing either source, testing it, or decoding the actual
certificate. The actual witness must never be modified for a control.

## Boundaries and the hypothetical baseline

Q cases address the direct pure certificate parser and complete reconstruction
in each independently written source. A future harness must test both
implementations separately, not accept agreement as an expected answer. Those
direct functions do not authenticate the original scientific witness.

R cases address the auditor's direct saved-result comparison. The independently
specified expected result must be derived from the synthetic input and this
contract, never copied uncritically from producer output. Actual production
acceptance still requires the six original pins and a separate admission.

P cases address fixed-input identity, file handling and production-envelope
boundaries. Use isolated, separately admitted test doubles or temporary files
at a direct I/O boundary, never edits to an original file or changes to the
production pin constants. A production CLI result with the wrong pinned bytes
must fail before any scientific decode. A direct synthetic parser result must
not be reported as an admitted actual-law result.

For the baseline recipe, use the eight domain fields specified in CONTRACT,
a hypothetical sorted root list (i,0,0) for i from 0 through 108, default_alpha
equal to the rational string 1/8, and no overrides. This shape-only synthetic
list is not a claim about actual canonical roots or a valid growth law. Were
this case separately admitted, its exact expected vector would contain 109
default-origin entries with alpha 1/8, scaled value 125/1, no off-grid indices,
and GRID_PASS. This paragraph does not create that fixture.

## Full coverage and exact rational cases

| Case | Hypothetical change or condition | Required direct-boundary outcome |
|---|---|---|
| Q01 | Baseline with no overrides | All 109 default entries, correct roots and indices, GRID_PASS |
| Q02 | One override at index 0, value 1/3 | Exactly index 0 off-grid, scaled 1000/3, GRID_FAIL |
| Q03 | One override at index 54, value 1/3 | Exactly index 54 off-grid; neither prefix nor tail omitted |
| Q04 | One override at index 108, value 1/3 | Exactly index 108 off-grid; complete last-index coverage |
| Q05 | Repeat the single 1/3 override separately at every index from 0 through 108 | Each of the 109 distinct hypothetical variants has exactly its selected off-grid index; no shortcut based on fixed locations |
| Q06 | All 109 indices overridden with 1/8; default 1/3 | GRID_PASS for the final vector, default separately reported off-grid; defaulted count zero |
| Q07 | All 109 overridden with 1/3; default 1/8 | GRID_FAIL with all 109 indices, overridden count 109 |
| Q08 | Remove an override from a mixed case | That index uses the default and is still present; missing override is not a missing component |
| Q09 | Override an index with the same value as the default | Numeric value unchanged but origin remains override and counts change correctly |
| Q10 | Use 2/16 or 0002/0016 | Reduce to 1/8, scaled 125/1, on-grid; no spelling-based denominator rejection |
| Q11 | Use 3/24 | Reduce to 1/8 even though the unreduced denominator 24 does not divide 1000 |
| Q12 | Use 2/6 | Reduce to 1/3, scaled 1000/3, off-grid |
| Q13 | Use 1/2000 | Positive but off-grid; scaled 1/2, not rounded to a grid point |
| Q14 | Use 1/1000 and integer string 2 | Respectively scaled 1/1 and 2000/1; alpha always includes its reduced denominator |
| Q15 | Use a positive 64-digit numerator over denominator 1 | Accept within the bound and preserve every digit exactly; no float conversion |
| Q16 | Use a 65-digit term, including a term padded with leading zeros | Refuse the lexical bound before arbitrary-size arithmetic |
| Q17 | Zero numerator or zero denominator, in any allowed digit spelling | Refuse; neither zero coefficients nor undefined fractions are admitted |
| Q18 | Invalid unused default with every index overridden | Refuse even though that default supplies no final entry |
| Q19 | Negative, plus-signed, spaced, decimal, exponent, Unicode-digit or multiple-slash rational | Refuse each representation; do not coerce |
| Q20 | Coefficient as JSON integer, Boolean, null, array or object rather than string | Refuse each wrong type |

Q05 is an explicit family of 109 future variants, not a claim that any were
generated or executed. No aggregate pass count is assigned to this document.

## JSON labels and component domain cases

| Case | Hypothetical change or condition | Required outcome |
|---|---|---|
| Q21 | Change each of the five domain labels independently | Refuse every mismatch, including parent_size 4.0 or true |
| Q22 | Remove each required top-level field, or add an unknown one | Refuse exact-field mismatch |
| Q23 | Repeat a top-level key or override key with identical value | Refuse the duplicate; equality of values does not excuse it |
| Q24 | Duplicate a key with a JSON escape-equivalent spelling | Refuse after decoding key strings, not merely raw-token comparison |
| Q25 | Root list of length 108 or 110 | Refuse incomplete or extra component domain |
| Q26 | Duplicate or swap two root triples | Refuse lack of strict lexicographic order or uniqueness |
| Q27 | Root tuple has wrong length, wrong container, Boolean or noninteger member | Refuse every malformed root |
| Q28 | First root coordinate outside 0..65535, mask outside 0..15, or mark bit not in precursor mask | Refuse the shape constraint |
| Q29 | Override keys -1, 109, 00, 01, +1, empty, spaced or Unicode digits | Refuse every noncanonical or out-of-domain index |
| Q30 | overrides is an array, null or scalar | Refuse; only a keyed object is allowed |
| Q31 | Invalid UTF-8, malformed JSON or trailing second JSON value | Refuse without a partial scientific result |
| Q32 | JSON float, NaN, Infinity or oversized integer token anywhere | Refuse before scientific reconstruction |
| Q33 | Certificate exceeds 64 KiB or container depth eight | Refuse at the declared resource boundary |
| Q34 | Brackets and escaped quotes inside strings, including a rational later rejected lexically | Depth handling must ignore string contents; subsequent refusal reason must remain appropriate |
| Q35 | A different shape-valid root list under a direct synthetic call | Shape parser may accept, but result has no authenticated original-law status; production must refuse changed original bytes |

The boundary cases must include exactly-at-limit and one-over-limit inputs.
The lexical depth limit counts containers, not braces inside quoted strings.
Invalid structures may violate multiple constraints; qualification should use
single-fault cases when asserting a particular diagnostic.
Where an otherwise valid certificate or result cannot reach the maximum depth,
test acceptance by the bounded JSON decoder separately from the required later
semantic refusal. A within-limit unknown field does not become a valid witness.

## Every saved result field must be checked

| Case | Hypothetical saved-result change | Required auditor outcome |
|---|---|---|
| R01 | Correct complete baseline result independently specified from Q01 | Direct audit match, explicitly unauthenticated synthetic boundary |
| R02 | Correct complete GRID_FAIL result independently specified from Q04 | Match; valid off-grid result is not a process error |
| R03 | Change schema, status, root_order_basis or scope separately | Refuse each disagreement |
| R04 | Change each domain field or a fixed input identity path, bytes or hash | Refuse every altered field |
| R05 | Change each default field, even where all components are overridden | Refuse; inactive default is still a reported field |
| R06 | Remove, add, duplicate or reorder a component entry | Refuse exact 109-entry indexed result mismatch |
| R07 | Change a component index, root coordinate or origin | Refuse even if all numerical values are unchanged |
| R08 | Change reduced alpha, scaled numerator, scaled denominator or on_grid independently | Refuse each field; no Boolean-only or digest-only audit |
| R09 | Use a numerically equal but noncanonical alpha or scaled integer spelling | Refuse representation mismatch with the exact intended result |
| R10 | Change each count, override index list or off-grid index list | Refuse each inconsistency or reorder |
| R11 | Replace true with 1, false with 0, or an integer with a numeric string | Refuse type drift even where Python equality would compare equal |
| R12 | Coherently falsify component values, status, flags, counts and lists together | Refuse against independent reconstruction from the certificate, not just internal consistency |
| R13 | Remove any declared field or add an undeclared field at any result depth | Refuse exact key-set mismatch |
| R14 | Duplicate a result key, use nonfinite/float tokens, malformed UTF-8 or trailing JSON | Refuse result parsing |
| R15 | Saved result above 256 KiB or depth twelve | Refuse resource bound; include exact-limit counterparts |
| R16 | Reorder JSON object keys or alter insignificant whitespace only | Match after strict parsing; scientific list ordering remains significant |

R07 and R08 must cover first, middle and final entries and the full index sweep
where permitted by the later qualification admission. They cannot be satisfied
by comparing only one sample entry.

## Identity custody and operational cases

| Case | Future isolated condition | Required outcome |
|---|---|---|
| P01 | Change one byte or length of any of the six fixed inputs | Refuse whole identity before scientific decode; repeat for every role |
| P02 | Missing, directory, device, FIFO, symlink leaf or symlink ancestor | Refuse unsafe/nonregular input without an unbounded blocking read |
| P03 | Replace or mutate an input between its before/after snapshots | Refuse detected instability; no stale success receipt |
| P04 | Change a pinned input after analysis but before final recheck | Refuse final identity drift |
| P05 | Supply arguments to checker, or wrong argument count to auditor | Refuse usage; no implicit alternate mode |
| P06 | Relative, nonnormalized or symlinked saved-result path | Refuse the path contract |
| P07 | Replace or mutate saved-result bytes before final auditor recheck | Refuse drift rather than attest to an earlier body under a later path |
| P08 | Saved GRID_PASS from different certificate bytes, despite a self-consistent result | Refuse original pin or reconstructed-field mismatch |
| P09 | Output write or flush fails | Nonzero process outcome; any partial capture must be rejected, never consumed as a valid receipt |
| P10 | Source text imported under a later explicit qualification admission with interpreter bytecode writes disabled | No automatic main call, certificate access, scientific reconstruction or subject-initiated writes solely from import; test only when admitted |
| P11 | Normal and optimized interpreter modes under a later admission | Same explicit checks; no reliance on removable assert statements |
| P12 | Direct pure reconstruction or direct audit used without production authentication | Remains qualification-only and cannot establish an actual certificate result |

No P case authorizes mutation of a protected original or modification of the
source pins. The eventual harness and its temporary test environment must be
reviewed separately. Resource exhaustion beyond the declared inputs, a hostile
filesystem race that occurs wholly between finite snapshots, or a future change
after a successful receipt is not claimed impossible by these source checks.

## Review and later execution evidence

Fresh reviewers should inspect both complete sources independently before
authorizing qualification. They must verify that producer and auditor do not
share a parser or reconstruction implementation, that every direct expected
answer above is checked rather than inferred from agreement, and that production
cannot substitute synthetic input for the fixed certificate.

Any later record must distinguish cases defined, cases actually constructed,
cases executed, failures and repaired reruns. Preserve real stderr and nonzero
outcomes; do not relabel refusal as a grid failure or source preparation as
execution. The final actual grid audit remains a separate bounded admission
after qualification. This packet claims none of those future outcomes.
