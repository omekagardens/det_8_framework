# RI246 Six hook coefficients from the original source

1 October 2026, Honolulu. Manual author result for independent review.
The separately admitted original source resolves exactly the six hook
coefficients identified in RI243:

    x0=x1=1/8,
    y00=y01=429/1000,
    y10=y11=181/200.                                      (W1)

Their common denominator 1000 meets RI243's sufficient bound. Direct
substitution also makes both actual hook deficits zero. These are results
for the unchanged prescribed finite law, not a DET derivation of its
coefficient selection or a full normalized witness.

## 1 Source authority and genuine custody

The separately ISSUED admission is

    /Volumes/AI_DATA/development/det-review-evidence/ri245-root-hook-review-ichvs643/RI246_SIX_HOOK_LITERAL_ADMISSION.json
    5803 bytes
    SHA256 ef7a03e9290e76694f4265504376ca9fa3211a061fc41ec8f06da44babae6b12

The admission and RI243 root adjudication were completely read and
authenticated in 68e452 exit0. The accepted role map and proposed
contract were reauthenticated, and the complete root/nonauthor reviews
read, in c8f30e exit0 before source access. The admission authorizes
exactly these six roles; historical exceptions are not renewed.

The sole original scientific body is

    /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json
    2845 bytes
    SHA256 3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969

Its complete, untruncated literal display and before/after custody are
in genuine receipt ac4078 exit0. Every path segment was checked against
symlinks; the normalized absolute path was the real path and the final
object a regular file. O_NOFOLLOW descriptor state, whole length and
SHA256 were checked before display, then checked again after display.
The seven observed state fields were identical throughout:

| Field | Before and after |
| --- | --- |
| dev | 16777244 |
| ino | 373218 |
| mode | 33188 |
| nlink | 1 |
| size | 2845 |
| mtimeNs | 1790219166674919262 |
| ctimeNs | 1790219166674919262 |

These are this acquisition's observed states, not comparisons with
historical timestamps. The literal body was not JSON-decoded, filtered,
sorted, reindexed, copied to a new source file or executed. Administrative
admission JSON and filesystem/crypto operations are distinct from scientific
data parsing. No mathematical engine was used.

## 2 Original ordinal counting

The source declares an increasing minimum canonical-local-key root list
with original zero-based indices. Manual counting from its first root
gives these contiguous blocks before the hook:

| First entry of the root triple | Original indices | Number of roots |
| --- | --- | --- |
| 0 | 0 through 3 | 4 |
| 2 | 4 through 11 | 8 |
| 6 | 12 through 19 | 8 |
| 14 | 20 through 25 | 6 |
| 68 | 26 through 32 | 7 |
| 70 | 33 through 41 | 9 |
| 72 | 42 through 44 | 3 |
| 76 | 45 through 52 | 8 |

The hand count is 4+8+8+6+7+9+3+8=53, so the original hook
block begins at 53. Its exact consecutive entries are

    53 (78,3,0)       54 (78,3,1)
    55 (78,7,0)       56 (78,7,1)
    57 (78,9,0)       58 (78,9,1)
    59 (78,11,0)      60 (78,11,1)
    61 (78,11,2)      62 (78,11,3).

The next root begins the code 204 block at 63. The complete displayed
list contains each requested triple exactly once; it contains no other
code 78 block. Nonrequested keys above are ordinal landmarks only.
Their coefficient values have not been resolved or used.

RI243 proved that g's retained non-root bit is the LONG-ARM atom a
in r<a<b,r<x. Thus role order y00,y01,y10,y11 corresponds to
selected masks 0,2,1,3 and original indices 59,61,60,62. Keeping source
order instead of role order without this transport would be an error.

## 3 Complete default and override provenance

The complete literal source prescribes default_alpha="1/8".
Manual inspection of the entire override object shows no entry at 57
or 58; its entry at 53 is followed by 59, and no 57/58 entry occurs
elsewhere. These two roles therefore use the literal default.

The four other target entries are explicitly present:

    "59": "429/1000",    "60": "181/200",
    "61": "429/1000",    "62": "181/200".

Explicit entries supersede the default at their original indices.
No default was inferred from an excerpt or a numerical coincidence.
No discovery rounding is used as a denominator premise.

| Role | Exact component root | Original index | Provenance | Literal string | Positive denominator |
| --- | --- | --- | --- | --- | --- |
| x0 | (78,9,0) | 57 | no override; literal default | "1/8" | 8 |
| x1 | (78,9,1) | 58 | no override; literal default | "1/8" | 8 |
| y00 | (78,11,0) | 59 | explicit override at 59 | "429/1000" | 1000 |
| y01 | (78,11,2) | 61 | explicit override at 61 | "429/1000" | 1000 |
| y10 | (78,11,1) | 60 | explicit override at 60 | "181/200" | 200 |
| y11 | (78,11,3) | 62 | explicit override at 62 | "181/200" | 200 |

The exact potential multipliers and resulting IDEAL probabilities are

    f_hook,0=(19/220)(1/8)=19/1760,
    f_hook,1=(7/220)(1/8)=7/1760,

    g_hook,(0,0)=g_hook,(0,1)
       =(43/55)(429/1000)=1677/5000,

    g_hook,(1,0)=g_hook,(1,1)
       =(49/55)(181/200)=8869/11000.                      (W2)

For the manual simplification, 429=11*39 cancels the factor 11
in 55, and 43*39=1677; also 49*181=8869. These probabilities
are not individual newborn-bit probabilities, which have the inherited
additional factor 1/2.

The whole-parent records, selected precursors, component transport and
potentials are those independently accepted in RI243. Both selected bits
and both newborn bits remain. Equality of the two g coefficients within
each root sector is a source result, not a new locality assumption.

## 4 Same-source denominator certificate

All six newly resolved strings have positive integer denominators in
{8,1000,200}. The following manual identities provide a common
denominator D=1000:

    1000=8*125=1000*1=200*5,
    1/8=125/1000,    181/200=905/1000.

Thus each of the six actual coefficients, with its own original
default-or-override provenance above, is an integer divided by 1000.
The bound is immediate from

    0<1000<1024=2^10<2^50.                               (W3)

RI243's accepted branch-safe theorem therefore excludes d=d7 for
THIS actual finite law. No full vector, global coefficient lattice,
floating discovery grid, new growth scale or amplitude was instantiated.

The companion HOOK_BRANCH_CONSEQUENCE.md proves the stronger exact
same-six result P0=P1=0 and d=0, and states precisely what remains
of the original normalized decision.

## 5 Scope and independent acceptance

Only these six source values were newly resolved. No extra C4, theta,
rho, s, kappa, H/z, amplitude or other coefficient was looked up. The
C4 complements used by the accepted theorem are prior derived results.

This is the author's manual acquisition and proof packet. Independent
nonauthor verification of the full literal/custody receipt, original
ordinals, default absence, overrides and mathematical consequence is
still required; metadata integrity alone is not proof acceptance.

All 15 inherited boundary objects remain unchanged, with the 423-source
manifest by reference. The new issued RI246 exception is recorded
separately and does not reclassify historical opaque source entries.
The complete ten-coordinate/thirteen-equation system and recovery remain.
No executable qualification, RET/measurement, repository/Git/index,
publication or self-assigned successor work occurs. Stop at handoff.
