# RI-88 — positive finite width perturbation

25 September 2026 UTC. The exact four-vertex cap decision has a positive
solution within the frozen RI-85 domain. Coordinator acceptance of this finite result is complete; publication status
is maintained in the root implementation plan and coordination records.
The source-only wording in IMPLEMENTATION.md is its preserved preparation
snapshot, not a statement that this later calculation remains unrun.

The complete [certificate](CERTIFICATE.json) is 1,828,149 bytes, SHA-256
`ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b`.
It is the unmodified successful witness stdout. The checker and implementation
note retain their published `d02b4b6` identities; the [RI-85 design](../native_growth_four_vertex_cap_v1/DESIGN.md)
and all accepted prefix inputs remain unchanged.

## Mathematical result and its exact domain

The 64-by-11 rational matrix has rank 10, pivots 0 through 9 and a
one-dimensional kernel. The canonical direction has z1=1 and every one of its
eleven coordinates is nonzero. All 320 expanded marked-row residuals vanish.
With epsilon=1/4, each supported multiplier h7=1+epsilon*z lies in [3/4,5/4];
all other seven-event orders have h7=1. This is strictly interior to the
positive domain. The amplitude is a safety convention, not a uniquely selected
DET parameter; other sufficiently small positive amplitudes are possible.

On the complete P1 row with all inherited marks zero, let
u0=a0*g0^3/b0^3>0. Summing all eleven ideals and both fair newborn marks gives
L(z)=u0 and the exact expected-width increase a6*u0/4>0. The unknown common
baseline scale a6 is positive; no numerical a6, q6, q7 or global M6 was evaluated.
The exact gain divided by a6 is retained in the certificate. This is a
conditional-on-parent expectation over the entire row, with no conditioning on
support membership or proper birth.

The nullity-one result also gives a short support-minimality corollary.
Every solution is a scalar multiple of z. Restricting to any strict subset of
these eleven classes sets at least one nonzero coordinate to zero and therefore
forces that scalar to zero. This is minimality only within this fixed pool,
held prefix and first-departure convention. It does not prove global minimality
among other supports or birth sizes. RI-84's narrower obstruction is preserved.

RI-85's maximal-deletion closure covers all five affected six-event parents;
other parent rows and all smaller rows remain unchanged. Complete harmonic
equations supply normalization, and the positive unmarked class multiplier
preserves precursor-record locality and marked equivariance. In every new
five-parent diamond, both scalar-passive D/4 paths acquire the same terminal
h7. Thus this is an admissible strict prefix through seven births under the
stated fair-bit, scalar-passive model premises.

## Actual checks and independent reproduction

The separately admitted witness, normal replay and optimized replay all exited
zero. Normal and optimized scientific summaries are byte-identical: 8,939 bytes,
SHA-256 `25210a0acf2fd78975a30c7003a68f3f8ac8e823bc3608e7d9eb1574a1a025ef`.
All 90 new intended-reason refusals, three algebra-only branch fixtures and the
15 inherited controls pass; the inherited exact prefix replay retains 69
canonical stages. The three synthetic ranks are 1, 2 and 11; they do not replace
the actual native rank-10 decision.

A separate standard-library consumer imports no producer or native-law helper.
It independently rebuilds the structure, 40 authenticated held rows/224 slots,
64 matrix rows, all 320 expanded rows/2,752 ideals/2,752 uncancelled factors,
complete RREF operations and kernel, width and positivity. It also reconstructs
all 8,448 marked-ideal transports and 10,752 transported factors, including
same-image automorphisms and all three P2 images. The transport digest is
`e94405882f4e76951b00b67dde9284cb4da952c683dc319c17f3f451252048ac`.
All 17 certificate sections reconcile exactly. Held probabilities' derivation
remains authenticated accepted-prefix evidence; the independent consumer does
not re-optimize that prefix or rerun the producer's negative controls.

| Actual operation | Child seconds | Peak sampled RSS bytes | Actual outer exit |
|---|---:|---:|---:|
| Witness | 12.367616 | 127795200 | 0 |
| Normal saved replay | 12.452696 | 129925120 | 0 |
| Optimized saved replay | 12.523282 | 129073152 | 0 |
| Independent arithmetic audit | 0.561571 | 54116352 | 0 |

Every operation used the unchanged 120-second/512-MiB envelope. Sampled RSS is
not an allocator hard cap. Expected progress stderr from the producer is
retained. The independent arithmetic report is 56,803 bytes, SHA-256
`cb6499aef376592c14d9e8e514899e50f4d0e135ab5506c5d3be40174b7a495d`.
Its complete source, plan, snapshots, raw monitor samples and actual receipt are
retained at `/Volumes/AI_DATA/development/det-review-evidence/ri88-certificate-audit-execution-fv4qc9xl/`.
Producer evidence is in `ri88-qr-source-6aRFc9/` under the same evidence parent.
The post-replay reporting command `79af1f` used a nonexistent receipt field and
failed; corrected check `70b2a3` preceded optimized authorization. No scientific
attempt failed or was retried. Historical RI-84 admission failures remain held.

## Remaining proof and physical premises

[RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md) permits some
strict all-size continuation preserving this finite seed. It does not provide
an all-size record-independent relative weight, persistent width improvement,
expected-width domination or suitable asymptotic geometry. In particular,
choosing its explicit half-scale continuation still invokes
[RI-39's finite-seed height obstruction](../native_growth_history_height_v1/HISTORY_HEIGHT.md):
liminf H(P_N)/N >= 1/2 almost surely. The finite width gain does not repair that
rejected vanishing-height-density target.

The next proof question is the full-complement condition for record-independent
relative weights at the first continuation. Proper-birth ratios may factor over
maximal deletions; unique-maximal/full-birth terminals still require a separate
record-independence test. A failure of one selector is not a universal no-go.
No metric, gravity, informative quantum payload, physical forward map or DET
uniqueness is established. RET remains paused.

Root acceptance is `RI88_ROOT_RESULT_ADJUDICATION.json` in
`/Volumes/AI_DATA/development/det-review-evidence/ri87-ri88-results-checkpoint-3_kuqmvi/`,
2,783 bytes, SHA-256 `15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6`.
The independent completed audit review is retained in
`/Volumes/AI_DATA/development/det-review-evidence/ri88-independent-completed-audit-review-7ln5xzqd/`,
35,072 bytes, SHA-256 `566ee7ad9589f89433c43ba97aabfeb1dec8f63e5d84f484d2851c114381cae9`.
It reconciles all 31 audit inputs, six outputs, nine raw monitor attempts and
17 reconstructed section identities. Earlier independent witness/replay
reviews reconcile all 533 producer monitor attempts. Minor reviewer metadata
key corrections remain in their records; no scientific result was changed.
