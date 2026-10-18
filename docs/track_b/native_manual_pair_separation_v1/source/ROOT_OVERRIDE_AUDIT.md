# RI197 manual original root and override audit

30 September 2026. This is a handwritten inspection ledger for the one
certificate admitted by RI197. It is not a parsed table, generated fixture,
resolved coefficient vector, graph reconstruction or executable test.

The complete 2,845-byte original certificate was displayed without truncation
in terminal receipt `882888`, exit 0, after exact whole-byte authentication.
An independent second read in that same command authenticated the same bytes
after the display. Both SHA256 values were
`3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.
No scientific JSON parser or arithmetic program was used.

## Domain and literal structure

The eight top-level names are distinct. Their exact declared meanings are:

| Name | Literal value or structure |
| --- | --- |
| schema | `ri41-height-primal-v1` |
| seed | `interior_a` |
| parent_size | integer `4` |
| potential | `RI-38 maximal-deletion` |
| component_order | `increasing minimum canonical-local-key` |
| default_alpha | string `1/8` |
| overrides | one object, inspected below |
| roots | one ordered array, inspected below |

The displayed document has ordinary balanced JSON delimiters and quoted
names/rational strings. No repeated top-level or override name, Boolean in
a root, decimal/exponential numeric token, null, floating/nonfinite token,
escape-dependent spelling or additional field appears. This is a literal
inspection finding, not observed acceptance by any JSON or coefficient parser.

## All root positions

Every index below is zero-based, as in the original loader. Each row gives
the common first coordinate E and every indexed pair (S,R) in that group;
thus `101:(7,0)` on the E=2254 row denotes the complete root (2254,7,0).
The entries were counted and transcribed by hand from the complete display.

| E | Exact indexed pairs (S,R) | Count |
| ---: | --- | ---: |
| 0 | 0:(0,0); 1:(1,0); 2:(3,0); 3:(7,0) | 4 |
| 2 | 4:(1,0); 5:(3,0); 6:(4,0); 7:(5,0); 8:(7,0); 9:(12,0); 10:(13,0); 11:(13,1) | 8 |
| 6 | 12:(1,0); 13:(3,0); 14:(7,0); 15:(8,0); 16:(9,0); 17:(9,1); 18:(11,0); 19:(11,1) | 8 |
| 14 | 20:(1,0); 21:(1,1); 22:(3,0); 23:(3,1); 24:(7,0); 25:(7,1) | 6 |
| 68 | 26:(3,0); 27:(7,0); 28:(9,0); 29:(9,1); 30:(11,0); 31:(11,1); 32:(11,3) | 7 |
| 70 | 33:(3,0); 34:(7,0); 35:(8,0); 36:(9,0); 37:(9,1); 38:(11,0); 39:(11,1); 40:(11,2); 41:(11,3) | 9 |
| 72 | 42:(3,0); 43:(7,0); 44:(7,1) | 3 |
| 76 | 45:(3,0); 46:(3,1); 47:(7,0); 48:(7,1); 49:(11,0); 50:(11,1); 51:(11,2); 52:(11,3) | 8 |
| 78 | 53:(3,0); 54:(3,1); 55:(7,0); 56:(7,1); 57:(9,0); 58:(9,1); 59:(11,0); 60:(11,1); 61:(11,2); 62:(11,3) | 10 |
| 204 | 63:(3,0); 64:(3,1); 65:(3,3); 66:(7,0); 67:(7,1); 68:(7,3) | 6 |
| 206 | 69:(3,0); 70:(3,1); 71:(3,2); 72:(3,3); 73:(7,0); 74:(7,1); 75:(7,2); 76:(7,3) | 8 |
| 2184 | 77:(7,0); 78:(7,1); 79:(7,3); 80:(7,7) | 4 |
| 2186 | 81:(7,0); 82:(7,1); 83:(7,2); 84:(7,3); 85:(7,4); 86:(7,5); 87:(7,6); 88:(7,7) | 8 |
| 2190 | 89:(7,0); 90:(7,1); 91:(7,2); 92:(7,3); 93:(7,6); 94:(7,7) | 6 |
| 2252 | 95:(7,0); 96:(7,1); 97:(7,3); 98:(7,4); 99:(7,5); 100:(7,7) | 6 |
| 2254 | 101:(7,0); 102:(7,1); 103:(7,2); 104:(7,3); 105:(7,4); 106:(7,5); 107:(7,6); 108:(7,7) | 8 |

The cumulative totals at the ends of these rows are

    4, 12, 20, 26, 33, 42, 45, 53,
    63, 69, 77, 81, 89, 95, 101, 109.

There is no missing or repeated ordinal from 0 through 108. The first
coordinates strictly increase between groups. Within each group S increases,
then R strictly increases for fixed S. Therefore all 109 triples are distinct
and strictly lexicographically ordered. All coordinates are unsigned literal
integers, not strings or Booleans. Every E is between 0 and 2254, hence within
the four-vertex relation-mask envelope 0 through 65535.

The full list of S values that occurs is 0,1,3,4,5,7,8,9,11,12,13. All are
proper four-vertex masks: none is 15. Their set-bit meanings and the R values
actually appearing with them exhaust the mask checks:

| S | Set-bit positions of S | R values actually present anywhere with this S |
| ---: | --- | --- |
| 0 | empty | 0 |
| 1 | {0} | 0,1 |
| 3 | {0,1} | 0,1,2,3 |
| 4 | {2} | 0 |
| 5 | {0,2} | 0 |
| 7 | {0,1,2} | 0,1,2,3,4,5,6,7 |
| 8 | {3} | 0 |
| 9 | {0,3} | 0,1 |
| 11 | {0,1,3} | 0,1,2,3 |
| 12 | {2,3} | 0 |
| 13 | {0,2,3} | 0,1 |

Every listed R has set bits contained in its S. This establishes the declared
typed-root/mask/order properties by inspection. It does not establish that
these are all actual graph components. The accepted original finite graph
reconstruction and RI189 routing remain explicit premises.

## Default and every override

The default is the positive rational string `1/8`. Every override name below
is an explicit canonical unsigned decimal index string, with no leading zero
except the name `0` itself. All are in 0 through 108 and occur once. Each
value has positive ASCII integer numerator and positive integer denominator;
there is no sign, space, decimal, exponent, zero term or extra slash.

The table groups only identical literal override values. Comma-separated
indices name every actual key individually, not an inferred range.

| Exact override keys | Literal rational string |
| --- | --- |
| 0 | 486413/200 |
| 7 | 27949/1000 |
| 12 | 268323/500 |
| 17 | 1851/500 |
| 18 | 101/500 |
| 22 | 31/10 |
| 25 | 3/20 |
| 30,31,32 | 171/200 |
| 33 | 203153/1000 |
| 38,39,40,41 | 361/1000 |
| 42 | 12729/500 |
| 45 | 64901/1000 |
| 46 | 29417/500 |
| 47 | 331/1000 |
| 48 | 333/1000 |
| 53 | 54747/1000 |
| 59,61 | 429/1000 |
| 60,62 | 181/200 |
| 66 | 141/1000 |
| 67 | 79/500 |
| 68 | 7/40 |
| 74,76 | 27/125 |
| 77,78,79,80 | 99/100 |
| 81,83,85,87 | 237/200 |
| 82,84,86,88 | 1193/1000 |
| 89,91,93 | 1083/1000 |
| 90,92,94 | 121/125 |
| 95,98 | 249/250 |
| 96,97,99,100 | 199/200 |
| 101,103,105,107 | 197/200 |
| 102,104,106,108 | 983/1000 |

For a second manual count, there are 7 keys through 25; 4 in 30 through 33;
5 in 38 through 42; 4 in 45 through 48; the single key 53; 4 in 59 through
62; 3 in 66 through 68; the two keys 74 and 76; and all 32 keys from 77
through 108. Thus there are 62 distinct overrides. The other 47 positions
would retain the default under the loader. No full resolved 109-vector is
constructed or transcribed here.

The complete original `check.py` was authenticated and literally read in
`8f6846`, exit 0. Its `load_certificate` first compares the declared roots
with the computed ordered root list, initializes all positions to the
default, then replaces each explicitly indexed override. The loader uses
zero-based indices. Consequently equality of some values elsewhere does
not identify components or change override origin.

The complete-list and all-override inspection precedes the selected-pair
conclusion: root (2254,7,0) is at index 101 and takes explicit override
`197/200`; root (2254,7,1) is at index 102 and takes explicit override
`983/1000`. Neither value comes from the default or an ordinal guess.

## Scope of the inspection

All literal roots and override strings have been inspected, including those
irrelevant to the selected pair. Only the two selected coefficients are
resolved for the hand calculation in [PAIR_PROOF.md](PAIR_PROOF.md).
This does not claim executable-parser compatibility, runtime success,
original graph recomputation, full-vector feasibility verification or any
qualification credit. The historical RI191 opaque-only record remains
unchanged; the separate RI197 admission supplies this one expanded read.
