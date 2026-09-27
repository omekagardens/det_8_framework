# RI120 independent review of the F2 and prefix lemmas

26 September 2026. Reviewer: `/root/ri117_t1_lemma`.

**Verdict: PASS_CONDITIONAL_ANALYTIC_IDENTITIES_ONLY.** No blocking
mathematical finding in either exact document identified below. The
notes prove symbolic actual-prefix identities and record duplicates;
they do not prove either required sensitivity or a fixed-support
rejection. Root adjudication and any execution remain separate.

## 1. Independence, full read and exact identities

I did not author F2_ANALYTIC_CHECK.md or ANALYTIC_PREFIX_LEMMAS.md.
Both were read completely, respectively lines 1--258 and 1--155.
I authored the separate F3_ANALYTIC_CHECK.md and the producer check.py;
this document is not an independent review of either of those works.
The overlap is disclosed rather than counted as an additional
independent source/implementation review.

All three note paths are under
/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/.

| Note | Bytes | SHA-256 |
| --- | ---: | --- |
| F2_ANALYTIC_CHECK.md | 10742 | 81c0e90759acb6835a3a64b05088a9222bb19ba2e2c6a5acefb157110f996833 |
| ANALYTIC_PREFIX_LEMMAS.md | 7886 | 7e07f55a24aa6feb2859bc594786b8748ebc7eb73dce210e70eee0e25c3bb247 |
| F3_ANALYTIC_CHECK.md, disclosed authored cross-reference only | 8244 | d2b68390ad81f176bc2ff6a36290a9c18877459b985ad736f06d80d7c35785f2 |

Fresh opaque hashes are tool chunk 943890; line/byte counts are 56e0bb.
No scientific data were parsed by those checks.

## 2. Exact borrowed premises

The proof depends on the accepted actual RI63 size-five law, not just
on general DET or order locality. Its component coefficient is

    alpha_actual=(35/36)alpha_boundary+t,  t=c5/36>0.

RI63's accepted finite result says every positive canonical boundary
component is everywhere defect-neutral. Thus a component containing
one raising role has boundary coefficient zero. The conclusion applies
even when the particular role under discussion is neutral, provided a
complete ratio edge connects it to a raising role. Neither note
assumes every neutral role has zero or positive boundary coefficient.

Further load-bearing premises are the exact RI38 maximal-deletion
potential and its complete marked-diamond identities, positivity,
proper-precursor locality, transported equivariance, complete record
cubes and normalization. The RI85 unique/twin-top identities and
RI117's complete T2/T3 proper-ideal sums are retained. The size-four
prefix has its actual component scales; the common half-scales start
only at the accepted later levels.

I previously read the complete RI63 COMPLETION.md, RI102 AMPLITUDE.md
and RI117 connected lemma during this assignment chain, and checked
their pertinent statements again against the notes. Their fresh pins:

| Supporting source | Bytes | SHA-256 |
| --- | ---: | --- |
| RI63 COMPLETION.md | 17102 | e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122 |
| RI102 AMPLITUDE.md | 17366 | bef68897a4d91e24deab41b9bcd3b9fd03edcc55e41b12fd9e4be31ea38081ba |
| RI117 CONNECTED_CONSTRAINTS_LEMMA.md | 11893 | ede2d82067a4259266d61988e0897756507e06b28040d8d5bd324991aa79dad0 |

RI63 and RI102 are under the repository's docs/track_b/ directories
native_growth_expected_defect_completion_v1/ and
native_growth_fixed_amplitude_lift_v1/, respectively. The connected
lemma is under external ri117-coupled-positive-family-QrAaK5YQ/.
The complete root RI117 adjudication and RI120 assignment were also
read; their identities are retained in F3_ANALYTIC_CHECK.md.

## 3. Intrinsic Ferrers arguments checked individually

A Ferrers down-set cell's principal ideal is a complete rectangle.
It is a chain only on an axis. Two incomparable cells with chain
principal ideals must occupy different axes, so their principal
ideals intersect only in the unique minimum. The prefix note's
shared-two-vertices obstruction is therefore valid as a necessary
test, without claiming a complete classification.

For C5, masks 0,3,7,15 are raising. Empty birth produces multiple
minima; the three nonempty cases are nonchain with a single atom,
or equivalently have two incomparable chain-principal ideals sharing
at least two vertices. Deleting the newborn restores C5, so their
defect is exactly one. Mask1 is instead the explicitly realizable
Ferrers hook (5,1) and is neutral. Every proper C5 ideal is covered;
the full ideal remains a complement.

For H5 mask3, the prefix note considers every one-vertex deletion.
After deleting any of the three stem vertices, the old cap principal
ideals remain chains sharing at least two retained vertices. After
deleting a cap, the remaining cap and newborn share the two-vertex
prefix in their chain principal ideals. Deleting the newborn leaves
the non-Ferrers H5. The terminal itself has the same obstruction,
and deleting the newborn plus one cap leaves a chain. Hence the
defect is exactly two, not merely bounded below by a selected
deletion test.

For H5 mask1, the terminal is non-Ferrers from its old twin caps;
deleting a cap leaves the Ferrers hook (4,1), so defect is one.
Its other incoming hook-parent birth is raising from zero to one.
The ordinary diamond based on C4, with precursors C3 and root,
links these actual two second-leg roles. Positive first-leg factors
and the same identity for RI38 potentials equate their component
coefficients for every transported marking. This justifies t for
the neutral H5 root slot without a false neutral-implies-zero rule.

## 4. Full algebra and record transport checked

C5's unique-maximal deletion potential is the corresponding C4
probability. Applying t only to its four proved raising slots gives
the stated D(0),D(3),D(7),e identities. The remaining difference
N=D(1)-t B(1) is nonnegative by the actual mixture and depends only
on the root bit by proper locality. Complete normalization yields
ell=1-t-N exactly. Thus the internal C5 bit sigma drops from the
whole row by proof, not by treating it as a maximal mark.

The accepted twin-top diamond then gives h=t c and m=t h=t^2 c.
The H5 coefficient proof gives G(T)=t B(T)^2/A(T) separately for
each of its four stem ideals. Full normalization retains both
individual cap slots and gives j=1-t sum B^2/A-2t c.

Substitution into the F2 expressions was checked term by term:

    sum D G/B=t(1-2h-j)+N r,
    E2=1+(1-t)(h+j)+N(r-1),
    C2=t(E-2m-3j)+N H.

The resulting A2,B2,C2 formulas and all signs agree with the
complete RI117 fourteen-ideal T2 formula. Every term ignores sigma,
so Q2_8 is identically zero and Q2_(xi+8)=Q2_xi holds polynomially.
This does not establish constancy over the other stem records.

Substitution into V=E-m-2j=F+2m+j, with F=sum A G^3/B^3, gives

    V=1+t^3 sum B^3/A^2-t sum B^2/A+2(t^2-t)c,

exactly the prefix note's A5. All denominators are strictly positive.
Neither t nor any native probability or coefficient is evaluated.

## 5. Gaps and acceptance limit

Neither note proves a nonzero V contrast or a nonzero Q2 value at
the actual rho. Nonconstant intermediate terms do not exclude
cancellation. A nonzero polynomial may vanish at that unknown
scale, and cap-bit independence is not complete record constancy.
The notes explicitly preserve all these gaps.

Retaining all forty held rows, all eight V profiles and all sixteen
Q2 profiles in the separate source contract is correct. The derived
duplicates are prospective checks or consequences, not permission
to discard assigned records. No extra D1 rows or native probability
queries are needed or authorized by these lemmas.

Only manual proof review, source-text reads and opaque hashes/counts
were performed. No scientific certificate decoding, Python import,
AST, parse, compilation, probe, execution, fixture, H/z arithmetic,
new native coefficient evaluation or scale selection occurred.
No reviewed note, old RI117, repository/index/git, input copy,
candidate or active execution document was modified.

Signed for this bounded independent analytic review:
`/root/ri117_t1_lemma`, 26 September 2026.
