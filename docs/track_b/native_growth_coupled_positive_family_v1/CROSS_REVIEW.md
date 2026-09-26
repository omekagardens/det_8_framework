# RI117 independent cross-review

26 September 2026. Review by the connected-constraints contributor.
This reviewer did not author the T1 or D1 notes reviewed below.
The review is manual mathematical/source review, not numerical execution,
proof-assistant verification, whole-packet acceptance or root adjudication.

## Reviewed exact sources

Both notes were read completely in tool chunks 2e060a and 4747cf;
opaque identities and line/byte counts were checked in 934e4b and ae0612.

| File in this external RI117 directory | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| T1_LEMMA_REVIEW.md | 221 | 9777 | 1769f8afacc65dff5262cf539a747fa447c8a1c8aad1a651aaa9bb24a8eb2b2e |
| D1_CATALOGUE_LEMMA.md | 257 | 11691 | 89aa520ad0d24407254d588f0de814bf5a674228270dcfdb75d8b8f6af3da1cc |

The complete RI111 and RI103 proofs had previously been read during this
assignment, along with the relevant RI85 catalogue and RI102 proof.
This reviewer additionally read the complete current RI115 root final
mathematical adjudication and published result note in chunks 266ea9
and 894261. They support the current zero-minor disposition and the
separately reviewed saved signs; no old pending-audit wording is treated
as current status.

## T1 review

No blocker found.

1. The continuous root-free pivot with negative value at zero stays
   negative on the whole admitted interval. The quotient defining beta
   is therefore positive at the actual positive rho.
2. Gamma positivity correctly uses actual k0 and f0, not arbitrary
   trial-scale baseline positivity.
3. The row-difference elimination uses the nonzero pivot and divides
   by s rho, never by t. It includes t=0 in the affine line before
   later positivity/slot constraints exclude it.
4. The zero minors give every remaining record equation; there is no
   unproved parity reduction.
5. The local equivalence is exactly to the interval
   -4e < w1 < W*. Its sufficiency includes t>0 and v1>0 because
   W*<1. This is not the older 27-child v1-positive premise.
6. The D1 slot bounds use positivity of every baseline slot and the
   exact finite eight-record minimum. The empty-birth diamond gives
   q_D1(I)=R_xi e_T1, so W*=4/Rmax-4e_T1 and the interval length is
   exactly 4/Rmax. No Rmax is calculated.
7. The zero member is only a local witness. The complete D1 equations
   and other parents remain independent obligations.

## D1 review

No blocker found.

1. The seven supported individual ideals are exactly the core, the
   three single-cap ideals and the three double-cap ideals; their
   correction columns are J1,J2,J3. All other complete ideals remain
   baseline except the private full correction.
2. The accepted harmonic relation removes precisely the seed direction:
   x=w2-z2w1 and y=w3-z3w1 yield
   L1=3rho(Bcore x+Ccore y). Reference-row elimination gives all
   seven homogeneous compatibility equations and the strict d1>-4
   inequality with its correct direction.
3. The K6 ideal partition has thirteen proper slots: 4+2+1 excluding
   o and 4+2 including o. Every deletion factor was checked manually.
   In particular the first potential is
   G A Bminus^2/(B^2 Aminus), and the o-containing one-cap
   potential is the full K5 probability fbar, not cbar.
4. The D1 partition has twenty-one proper slots: 4+3+3+1 excluding
   o and 4+3+3 including o. Its first four-maxima product reduces to
   rho^4 A^3 G^3 Bminus^3/(B^6 Aminus^2).
   The one-cap/no-o product is rho^3 h^2 cbar/c^2, the two-cap/no-o
   product is rho^2 j, and the one-cap/o product is rho^2 fbar.
   The full-six-parent factors remain 1-rho E and 1-rho Ebar.
5. Summing all repeated ideals gives exactly the displayed quartic
   UD, including constant 4, linear term -rho(E+3Ebar) and
   quadratic term 3rho^2(j+fbar). Thus g1=1-s UD is a complete
   full complement, not a selected supported-slot complement.
6. K4=C3 disjoint A1 has eight ideals and two irrelevant maximal
   bits, so four complete representative rows remain.
   K5=C4 disjoint A1 has ten ideals and two irrelevant maximal bits,
   so eight complete representative rows remain. The resulting
   12 rows/112 slots are a complete domain for the two additional
   held shapes under those invariances. They are not claimed globally
   minimal. D1 itself still has all eight stem records.
7. The note correctly refuses to infer these disconnected held
   probabilities from the names of the previously retained connected
   shapes. It presents an explicit unevaluated closure, not a new
   campaign or a full feasibility decision.

## Scope, independence and operations

No blocking finding or uncorrected mathematical error was found in either
exact source. This reviewer authored CONNECTED_CONSTRAINTS_LEMMA.md;
that note is therefore not independently self-reviewed by this artifact.
It receives a separate review from the T1 contributor.

No numerical probability or polynomial coefficient, H/z value, q6/q7
table, actual scale, fixture, target import, AST/compilation, runtime probe,
replay or solver was evaluated. No repository/index/git action occurred.
This external review is not an execution authorization or claim that the
complete fixed-support extension is feasible. Root retains acceptance and
publication authority.

## Complete main-manuscript review addendum

The subsequently completed ANALYTIC_REDUCTION.md was read in full, lines
1--300 in chunk cd28fc and 301--EOF in chunk 0da0a4. Its exact identity
was independently checked: 350 lines, 15,564 bytes, SHA-256
9726383aabb01cfa922b90f64bd572ac0a04a390111f57e722ed29d896289194
(count chunk 7ce057, digest chunk e39427).

No mathematical blocker found. The reviewer did not author this manuscript,
although its connected-profile formulas incorporate this reviewer's separate
contribution; those formulas additionally have the T1 contributor's independent
review. This review independently checks the manuscript's new conditional
classification and its use of the other authors' lemmas.

1. Equations (3)--(4) have the correct normalized D1 coefficients:
   delta=e_K d1/(3rho), theta=m/j and eta=g1/j. Eliminating y
   loses no solution because its coefficient is exactly one.
2. The four theta/eta cases are exhaustive and zero-safe. A proved
   nonzero theta contrast fixes x=-kappa delta; failure of any remaining
   affine condition forces delta=x=y=0. Constant theta correctly
   leaves either two freedoms or delta=0 according to eta's variation.
3. The RI102 strict negative-multiplier disjunction, combined with
   nonconstancy of both connected profiles, rigorously rejects that
   branch without testing D1 ratios or fixing w1. The sharpened equality
   case zj=-4e_j is also correctly excluded by strict positivity.
4. In the both-constant branch, the displayed open constraints and
   recovery formulas are necessary and sufficient for exactly the four
   parents. The zero witness obeys all constraints: zj/fj(0)>-2>-4
   follows from |zj|<=1 and fj(0)>1/2. It is not a whole-system witness
   or a restriction on the general free parameter.
5. In the exactly-one-nonconstant branch, wa=za requires the separately
   stated strict za>-4e_a. Since u=1-lambda>0, dividing the D1 row
   by c_b u is valid. Reference subtraction gives exactly (10), and
   reference recovery gives wb=zb-u(zb+C). The three alternatives
   for the set M cover all zero-contrast possibilities and use za!=0
   only where needed.
6. The final pair of strict bounds in (11) is correctly oriented:
   vb>-4 is u(zb+C)>-4fb(0), whereas wb>-4e_b is
   u(zb+C)<zb+4e_b. No division by mu or zb+C occurs, so their
   zero or negative cases are included. The remaining bounds are
   exactly T1's interval and d1>-4. Substitution of (12) restores
   every original D1 and connected equation, establishing sufficiency
   as well as necessity.
7. The twelve other parents are precisely T4,...,T11 and D2,...,D5.
   Their literal supported mask multiplicities match the accepted
   catalogue. Their equations use the same shared w2,w3 rather than
   independent copies. Constant T8/T11 freedoms are retained.
8. The complete-support iff is conditional on satisfying all these
   remaining equations; no actual branch, numerical coefficient,
   complete positive extension or root choice is asserted. The named
   finite input gaps and execution boundary remain explicit.

Result: PASS_MANUAL_COMPLETE_ANALYTIC_REVIEW, with no blocking findings.
The operations and authority limitations above remain unchanged. This
addendum is independent source review, not root acceptance or permission
for any numerical campaign.
