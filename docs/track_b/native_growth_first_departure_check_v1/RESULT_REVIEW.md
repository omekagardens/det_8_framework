# RI-84 — exact obstruction on the first three-shape support

25 September 2026 UTC. **Independently accepted for scoped publication.**
The frozen finite question has a negative answer:
there is no nonzero record-blind perturbation supported on the three declared
seven-event classes. This is a candidate-specific result. Other supports,
record-dependent candidates, later departures and all-size extensions remain open.

The unchanged [design](../native_growth_first_departure_v1/DESIGN.md) and
[checker](check.py) fix h=1 through size six and outside
T1=C4⊕A3, T2=C5⊕A2, T3=C4⊕(C2 disjoint A1) at size seven.
Their complete maximal-deletion closure is the two six-parent classes
P_A=C4⊕A2 and P_B=C6. Full-birth children have a unique maximum and are
outside this support. Thus the common positive proper-birth scale a6 cancels
from the harmonic equations; no numerical a6, M6, q6 or q7 is required.

## Exact reason the candidate fails

For each four-bit record ξ, the held actual prefix supplies positive
qξ=q4(C4,ξ;15), pξ=q5(C5,ξ;15), vξ=q5(C5,ξ;31), with αξ=pξ²/qξ.
The fifth C5 bit is fixed to zero in these representatives; its irrelevance
and the induced-record transport follow from the accepted locality argument.
The complete affected-row equations reduce to

\[
 A_\xi z=\alpha_\xi z_1+2v_\xi z_3=0,\qquad
 B_\xi z=v_\xi z_2+p_\xi z_3=0.
\]

The actual saved rational values obey, between records 0 and 1,

\[
 q_1/q_0=p_1/p_0=\alpha_1/\alpha_0=359/360,
 \qquad v_1=v_0>0.
\]

For example q0=81/1100 and q1=3231/44000. Consequently
(A1−A0)z=−α0 z1/360=0 forces z1=0. The A0 equation then forces
z3=0, and B0 forces z2=0. Equivalently, the determinant of the three
rows A0, B0, A1 is α0 v0²/180>0. The matrix has rank three; the first
failed compact balance is index 2 (record 1, parent A). No positive-amplitude
or width-gain admission follows. The saved normalized reference direction
is only the kernel of A0 and B0, not a solution of the full system.

## Finite verification and provenance

The exact [certificate](CERTIFICATE.json) is 422785 bytes, SHA-256
`e8ef1434784d36f9174ead89588edf46176409c6b6609525670a59d965bba9a7`.
It retains 32 held rows /176 positive probability slots, 128 complete
marked parent rows, 960 individual ideal occurrences, 448 deletion factors,
320 supported and 640 zero-correction occurrences (including all 128 full
births), 32 compact equations and 1472 transported marked-ideal cases.
Seven backward maximal-deletion roles and 15 forward ideals remain distinct;
backward counts are not transition multiplicities.

The genuine witness, normal replay and fresh optimized replay all exited
zero under the unchanged 120-second /512-MiB sampled-RSS envelope.
The witness took 9.255609 seconds /126681088 sampled peak bytes; normal
9.290595 seconds /128057344 bytes; optimized 9.231852 seconds /128434176
bytes. Normal and optimized full stdout and expected diagnostic stderr are
byte-identical. Both replays retain 69 canonical inherited-prefix stages,
15 inherited and 71 new intended-reason controls. The certificate's logical
JSON digest printed by the checker excludes its terminal newline; the file
SHA above includes it.

The independently reviewed stdlib-only certificate consumer uses separate
order enumeration and rational arithmetic to check the saved complete finite
structure, held normalization, deletion factors, transport, all compact
rows and the determinant. It imports no producer module. The actual audit exited zero in 0.189241 seconds with 28655616 sampled peak
RSS bytes; all three raw monitoring attempts and two live observations were
reconciled, and the final owned process group was absent. The report matches
the complete certificate coverage, equivariance and rank-three decision.
It does not independently rederive the optimizer's inherited prefix or
replace the analytic arbitrary-label/locality arguments; these retain their
published proof and actual replay evidence.

Durable external evidence lives under
`/Volumes/AI_DATA/development/det-review-evidence/`:

- `ri84-qr-env-repair-LioNdK/`: accepted qualification, witness, normal replay,
  compact arithmetic and independent witness-custody reviews.
- `ri84-optimized-recovery-cNvcKp/`: separately admitted successful optimized
  attempt and its predecessor provenance; the copied witness receipt is
  explicitly a copy of the genuine first witness.
- `ri84-certificate-audit-execution-bommbwhm/`: independent consumer execution,
  final report and root adjudication.

The first qualification refused before child launch because Darwin added an
unbound environment field. A fresh reviewed environment binding then passed
73 synthetic supervisor checks. A later root orchestration error dispatched
the first optimized launcher without its authorization; that attempt also
refused before any child. Both failures, original drafts and their explanations
remain preserved. The successful optimized recovery changed only the evidence
root in its qualified supervisor and used a new freeze. Scientific inputs,
acceptance thresholds and historical results were unchanged.

Sampled process-group RSS is not a hard OS memory cap. The result is a finite
obstruction under the held strictly positive prefix and this exact support.
It neither rejects native growth in general nor supplies an all-size harmonic
law, macroscopic geometry, gravity dynamics or a measurement forward map.

## Final acceptance records and continuation

Relative to the external evidence root above, the decisive records are:

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| ri84-qr-env-repair-LioNdK/witness-01/receipt.json | 15407 | `4a87135a63582c85825de90294fc9748a7842a100eefa4f8b84849257e0bfe3d` |
| ri84-qr-env-repair-LioNdK/normal-01/receipt.json | 17752 | `ea90d27001bd7991d968889f7abbca96744d6e5a13295da4333763433147e1b7` |
| ri84-optimized-recovery-cNvcKp/optimized-01/receipt.json | 18093 | `5cc1bbbac49a1cdf6e87d0eac0a7062142761d7fbd8192cfb32368b0309dac07` |
| ri84-certificate-audit-execution-bommbwhm/audit-01/REPORT.json | 4809 | `affe0c2f2a05bf794382eb8c836417baf6ddd549dffe11ed2b5b8dd0c35ea73b` |
| ri84-certificate-audit-execution-bommbwhm/ROOT_RESULT_ADJUDICATION.json | 7954 | `9a2e7b00738239f87d87e40ac2bce1c1527ab710d5709292db3dc80379de73fc` |
| ri84-independent-completed-audit-review-4umrbm4c/INDEPENDENT_COMPLETED_REVIEW.json | 17592 | `b30ee2f1780b7e22a178041bf06a171138432bcb4b246af557c0b9529380e395` |

The root adjudication pins the complete qualification, source-review,
replay, independent arithmetic and custody evidence, including the retained
failed admissions. It reports actual outer process exits separately from
success flags in child-produced files.

RI-85 now examines the complete four-vertex cap family C3⊕Q with at least
two maxima. Its first deliverable is the analytic closure and exact finite
harmonic/width decision design, reviewed before coefficients are evaluated.
This successor is an explicit enlargement following the obstruction, not a
retroactive change of the rejected RI-82/84 candidate. RET remains paused.
