# RI125 primary white kernel first-refusal inventory — unexecuted

This revision freezes 38 concrete isolated controls for the implemented pure white
kernel only. It is **not** the complete packet's future qualifier inventory.
Wrapper/parser/custody, periodic, join and independently authored validator
controls remain source work; no missing branch is claimed covered here.

Start with a freshly built valid W01 operand and its correctly derived Shift
unless a row names W03. Mutate only the named input; retain the rest. Every row
specifies exactly one call and its required first ApplicationError.code.
The qualifier will own construction and actually invoke these calls later.
No fixture was built or call performed during source preparation.

| Id | Exact isolated operation | First code |
|---|---|---|
| WK01 | derive_shift rows converted from list to tuple | SHAPE |
| WK02 | derive_shift length=True, otherwise W01 | DOMAIN |
| WK03 | derive_shift with three W01-shaped row records, length=3,stride=2 | DOMAIN |
| WK04 | add key extra=null to W01 strip row | SCHEMA |
| WK05 | replace W01 row label 0 with True | ROW |
| WK06 | replace W01 head with empty list | SHAPE |
| WK07 | replace head interval's first scalar pair by True | SHAPE |
| WK08 | replace numerator string of that pair by True | EXACT |
| WK09 | replace numerator by empty string | EXACT |
| WK10 | replace numerator 1 by string "01" | EXACT |
| WK11 | replace denominator by string "0" | EXACT |
| WK12 | replace pair ["1","1"] by ["2","2"] | EXACT |
| WK13 | replace numerator with "1" followed by 65537 zero characters | RESOURCE |
| WK14 | replace numerator with "1" followed by 65536 zero characters | RESOURCE |
| WK15 | replace singleton head interval with [S(2),S(1)] | INTERVAL |
| WK16 | derive_response with Shift orientation="head_times_tail_transpose" | ORIENTATION |
| WK17 | add extra=null to Shift passed to derive_response | SCHEMA |
| WK18 | replace Shift center matrix with empty list | SHAPE |
| WK19 | replace Shift.error[0][0] with S(-1) | BOUND |
| WK20 | replace Shift.midpoint_polarization[0][0] with S(0) | POLARIZATION |
| WK21 | replace Shift.direct[0][0] with [S(3),S(4)] | DIRECT |
| WK22 | replace Shift.trace_center with S(0) | TRACE |
| WK23 | derive_response n=True | DOMAIN |
| WK24 | replace Gram key H by H_G, keeping its value | SCHEMA |
| WK25 | W03: Gram G[0][1]=S(2), leave inverse and other entries | GRAM |
| WK26 | Gram H[0][0]=S(-1) | GRAM |
| WK27 | Gram inverse[0][0]=S(1) | GRAM |
| WK28 | Gram G[0][0]=S(0), keep old inverse | GRAM |
| WK29 | Gram delta=S(1) but H=0 | GRAM |
| WK30 | Gram gamma=S(1) but inverse=[[S(1/2)]] | GRAM |
| WK31 | Gram rho=S(1/10^12) but H=delta=0 | GRAM |
| WK32 | Gram H=[[S(4/10^12)]],delta=S(4/10^12),gamma=S(1/2),rho=S(2/10^12) | GRAM |
| WK33 | usefulness(F(0),F(0)) | BOUND |
| WK34 | usefulness(F(-1),F(1)) | BOUND |
| WK35 | div(F(1),F(0)) | ZERO_DIVISOR |
| WK36 | mul(F(2^262143),F(4)): legal operands, oversized completed result | RESOURCE |
| WK37 | Gram G=[[-2]],inverse=[[-1/2]],H=0,delta=rho=0,gamma=1/2: inverse identities hold but positive LDL fails | GRAM |
| WK38 | Keep W01's valid Gram; replace Shift.center, midpoint_polarization and trace_center by 3, direct by [3,3], and retain E=trace_error=0. Call derive_response(...,n=2). All earlier checks pass, but its trace -1/2 misses structural [1/2,3/2]. This intentionally inconsistent operator pairing is refused; it is not an admitted physical operand. | STRUCTURAL |

Here S(q) denotes the stipulated reduced hexadecimal encoding of exact rational
q, and F denotes a future exact Fraction construction, not an executed call.
No controls claim that a ratio above the *new* eps threshold refuses: it returns
accuracy_failed with valid enclosures. WK32 concerns the unchanged inherited rho
premise and therefore does refuse. Direct-box and polarization mutations target
their distinct checks before the later trace/Gram checks. Resource text tests
distinguish the character cap from the parsed integer-bit cap.

The later complete packet must additionally freeze concrete controls for every
actual-input pin/phase/header guard before scientific decode; duplicate JSON,
complete capture framing and ninth-row/end-of-body rules; all output field
comparison paths; PSD/source identities, parity and endpoint conventions;
complete historical M-key projection and nuisance statuses; exclusive outputs,
unchanged full source/input postchecks, and resource/failure tails. Those are
explicitly unfinished and cannot be replaced by these 38 source-defined names.
WHITE_REFUSALS.md and white_controls.py now supply the bounded white-wrapper
controls. WK38 is also a concrete call in that source; the future separate
validator must execute its own corresponding mutation independently.
