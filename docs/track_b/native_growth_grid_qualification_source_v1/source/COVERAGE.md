# RI161 planned qualification coverage

This is a source-inspected expansion of all 63 inherited families. It records
recipes and independent expectations, not generated fixtures or test results.
Cases constructed: zero. Cases executed: zero. Operational admissions: zero.
Every row below is prospective. The sources define exact IDs and isolated
first-refusal expectations; CONTRACT.md defines their scope and record format.

## Certificate controls

Every Q variant is applied independently to checker and auditor. Thus 237
variant recipes imply 474 planned records per mode, not 237 shared-oracle tests.

| Family | Variants | Independent expected check |
| --- | ---: | --- |
| Q01 | 1 | Complete baseline 109-entry reconstruction |
| Q02–Q04 | 3 | Single off-grid override at first, middle and last index |
| Q05 | 109 | Separate single-override case at every index 0 through 108 |
| Q06–Q09 | 4 | All overrides on/off grid, removed override, same-value override origin |
| Q10 | 2 | Unreduced and zero-padded rational representations |
| Q11–Q13 | 3 | Reduced eighth, reduced third and positive half-grid scaled value |
| Q14 | 2 | Grid unit and integer coefficient |
| Q15 | 1 | Exactly 64-digit positive numerator, exact digit retention |
| Q16 | 4 | 65-digit numerator/denominator, including leading-zero padding |
| Q17 | 5 | Zero numerator/denominator and padded zero spellings |
| Q18 | 3 | Invalid inactive default: zero, undefined denominator, wrong type |
| Q19 | 9 | Signed, spaced, decimal, exponent, Unicode and multiple-slash rejection |
| Q20 | 6 | Integer, both Booleans, null, array and object rejection |
| Q21 | 8 | Five domain labels plus Boolean, float and string parent size |
| Q22 | 9 | Each of eight required fields missing, or one extra field |
| Q23 | 9 | Each top-level duplicate and duplicate override key |
| Q24 | 2 | Escape-equivalent duplicate top-level/override labels |
| Q25 | 2 | 108 and 110 roots |
| Q26 | 2 | Duplicate roots and swapped roots |
| Q27 | 6 | Wrong root length/container/member type |
| Q28 | 9 | Bounds/subset failures, valid relation and mask endpoints |
| Q29 | 11 | Noncanonical or out-of-domain override labels |
| Q30 | 5 | Non-object override containers |
| Q31 | 8 | UTF-8/syntax/trailing/incomplete/delimiter/empty/input-type failures |
| Q32 | 6 | Float/nonfinite/integer-token rejection and exact integer limit |
| Q33 | 5 | Certificate byte/depth limits and separate semantic depth refusal |
| Q34 | 2 | Quoted delimiters/escapes at parser and rational boundaries |
| Q35 | 1 | Alternate shape-valid roots remain direct and unauthenticated |

Literal answers include 1/8 → 125/1, 1/3 → 1000/3, 1/2000 → 1/2,
1/1000 → 1/1 and 2/1 → 2000/1 after scaling by 1000. A literal power-of-ten
case supplies the 64-digit endpoint. Every complete reconstruction includes
indices, roots, origins, all rational fields, default, lists and counts.
No subject calculation is used to construct its own expected answer.

## Saved result controls

R controls act on the auditor and an independently specified saved result.
There are 1994 planned records per mode.

| Family | Variants | Independent expected check |
| --- | ---: | --- |
| R01–R02 | 2 | Complete correct GRID_PASS and GRID_FAIL objects match |
| R03 | 4 | Schema, status, root-order basis and scope mutations refuse |
| R04 | 25 | Seven domain fields and all three fields of each of six identities |
| R05 | 8 | Four default fields with active and inactive default |
| R06 | 4 | Component removal/addition/duplication/reordering |
| R07 | 545 | All 109 entries × index, origin and three root coordinates |
| R08 | 436 | All 109 entries × alpha, scaled numerator, scaled denominator and flag |
| R09 | 3 | Numerically equal noncanonical rational/integer representations |
| R10 | 11 | Five counts; removal/addition/reversal of each index list |
| R11 | 5 | Boolean/integer/string type confusion including index/root types |
| R12 | 1 | Coherent multi-field false result rejected against the certificate |
| R13 | 934 | 814 missing-field mutations and 120 extra-key mutations at every dictionary |
| R14 | 9 | Duplicate/escape-equivalent keys, float/nonfinite, UTF-8, trailing and malformed JSON |
| R15 | 5 | Saved-result byte/depth bounds and separate semantic depth refusal |
| R16 | 2 | Object-key order and insignificant whitespace remain equivalent |

R13 reaches the top object, domain, inputs map, every input identity, default,
counts and all 109 component dictionaries. The 120 dictionaries and 814
declared fields are counted from source structure, not by executing an oracle.
R07 and R08 cover all indices, not only the first, middle and last.

## Operational and actual caller controls

| Family | Records per mode | Boundary and retained observation |
| --- | ---: | --- |
| P01 | 24 | Six fixed roles × length/hash × both implementations; target reader remains real under an in-memory OS double |
| P02 | 14 | Missing/directory/FIFO/device/leaf link/ancestor link/realpath alias × both implementations |
| P03 | 8 | Before-open drift, in-read drift, close-only and primary-plus-close × both implementations |
| P04 | 8 | One/multiple late failures and primary-plus-one/multiple postcheck failures × both implementations |
| P05 | 2 | Wrong arity, exact nonzero main result and diagnostic |
| P06 | 8 | Relative, nonnormalized, leaf-link and ancestor-link paths × both implementations |
| P07 | 2 | Auditor no-result-baseline and saved-result drift; all later attempts retained |
| P08 | 1 | Different certificate rejected despite an internally consistent baseline result |
| P09 | 6 | Short stdout write, failed stdout flush and failed diagnostic write × both implementations |
| P10 | 2 | Genuine authenticated child imports: bounded stdout/stderr, guarded operations and actual main entry observation |
| P11 | 2 | Actual child interpreter flags for both imported implementations |
| P12 | 2 | Direct synthetic reconstruction/audit cannot establish actual-input authority |

P01–P09/P12 contribute 75 records; caller-owned P10/P11 add four. Operational
expected objects include exact class/code/message, all secondary errors,
ordered read/recheck calls and write/flush traces. P04 demands all six final
fixed-role attempts; auditor cases also demand the final saved-result attempt.
P07's first-read failure cannot be converted into a fabricated baseline.
P09 accepts no result merely because some output was written.

P06 probes the respective direct path readers; only the auditor has a
saved-result interface. P10 is source loading, not execution of subject main.
P11 is meaningful only in two genuinely distinct normal/optimized children;
a mocked flag or source label is insufficient. The parent compares every
other case record across those children and requires genuine completion.

## Qualification prerequisites and unchanged obligations

| Prerequisite | Source supplied here | Still required |
| --- | --- | --- |
| QP01 | Concrete bounded caller, exact prospective request, immutable subject pins and exclusive capture/completion rules | Fresh independent source/control review and root runtime admission |
| QP02 | All family expansions, independent complete expected objects, exact exception semantics and index sweeps | Execute admitted controls and independently review their complete outcomes |
| QP03 | Close, primary/later failures, absent baseline, partial writes/flush and diagnostic failure cases | Verify actual controls and preserve any partial/failed evidence |
| QP04 | No actual-input executor run or result | Separate later fixed-certificate producer/auditor admission after qualification |

The planned total is 474 + 1994 + 75 + 4 = 2547 per mode, or 5094 for both.
Source counts do not satisfy any executed-control obligation. All original
P2/P3, numerical Y=1/4, seed/amplitude/support/witness, shared T1, other eight
connected parents, five Di, ideal multiplicities and strict endpoints remain
unchanged. The inherited 31 focused variants, 139 policy cases and 20 native/
42 audit deeper obligations are neither reduced nor newly executed here.
