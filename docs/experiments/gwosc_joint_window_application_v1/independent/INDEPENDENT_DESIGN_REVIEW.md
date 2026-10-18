# Independent review of RI-123 prospective application design

27 September 2026 UTC. Verdict: **ACCEPT CONDITIONAL APPLICATION DESIGN ONLY**.
No blocking mathematical or source-interface discrepancy was found. This accepts
preparation of the explicitly bounded source-only implementation packet. It does
not accept a new executable, grant runtime admission, certify actual operator
coefficients or PSD-weighted arithmetic, or select a physical joint noise law.
Root adjudication remains separate.

Reviewed proposal: `DESIGN.md`, 31,586 bytes, SHA256
`4e725c42d77097e66b5b5cf5c3cc014f97b2a42663b0ef0ee3f78d8b4161699b`.
The source-only handoff is 4,667 bytes, SHA256
`37c6611aa6db3a0b04e6e243bd3b1519ce387ef1b5ba779b372ddcc03ef858d9`.

## Review independence and actual coverage

This reviewer did not author the proposal, its scientific implementation, or
its saved numerical predecessors. I read the complete proposed design,
authoring record, dimension accounting, handoff and 45-record premise manifest;
I independently derived the identities below. I also read the complete RI-118
design and root adjudication, complete RI-98 API, RI-116 result review and
RI-121 qualification README. Source reads covered RI-98 `derive_modes`,
`decode_psd`, `derive_scenario`, `project_saved` and `run_saved`; RI-100's independent
integer-numerator `mode_reconstruction`; RI-73's covariance certificate,
integration grammar and result construction; and RI-113/116's entire capture
reader plus its operator reconstruction and returned scenario structure.
Relevant RI-121 caller resource, mode and runtime paragraphs were checked.
This is not a fresh complete audit of every predecessor executable.

An independently written metadata inspection checked actual retained bodies for
closed-field locations, headers, inventories, source-record identities, counts
and order. It did not decode their encoded scientific rationals or binary64 PSD
values into a new calculation. The complete 51,891,508-byte coefficient capture
was opaque-hashed only and was never JSON-decoded. No target was imported,
compiled, run or rewritten. No scientific contraction, new transform, sign
campaign, raw strain/HDF5 access, empirical processing or protected-data access
occurred. Manual toy identities below are proof checks, not executed future
qualification cases. Only this new external review directory was written;
repository/index/Git, active caller/runtime/admission and prior evidence were
untouched. RET remains paused.

`PIN_REVIEW.json` records all 45 predecessor identities and all five proposal
files, including the handoff, with current byte counts, SHA256, resolved paths,
file state and path-chain observations. All 50 pins matched. The three
coordination documents are explicitly historical context snapshots, not future
scientific operands. The manifest does not purport to be the full transitive
execution closure; future root admission must still construct that closure.

## 1. Support, orientation and dimensions

The fixed intervals are consistent: T=10961, d=8192 and T-d=2769=N, while
2d>T. Earlier-window coordinate d+j and later-window coordinate j name the same
raw sample for exactly j=0,...,2768. With rows i,k, their directed covariance is
sum_j A[i,d+j] A[k,j], hence **C=U H^T**, not H U^T. The reverse window block is
C^T. Nonneighbors have disjoint first-T support under the stipulated white raw
covariance; disjointness alone does not make physical detector noise independent.

The embedded short operator P is supported only on [4096,6865). Both proposed
strips [0,2769) and [8192,10961) miss it. Thus their A coefficients equal the
long operator Q coefficients exactly. This is a valid and useful reduction;
all eight complete short/long rows must nevertheless be framed, decoded,
exhausted and bound to the original operator and Gram certificate. In particular,
there is no permission to replace the complete input by unauthenticated strips.

The first-T and full-M unions and final endpoints all check. On the left the
last T interval ends at 49152+10961=60113 and the last M interval at 65536;
on the right they end at 110592+10961=121553 and 126976. The used T-union lengths
are 60113 and 51921. The zero extension of A to M has 5423 columns. The selected
rows are the exact eight retained indices, with both endpoints 0 and 2768.

The dimension counts are consistent: eight pairs of short/long rows contain
8(2769+10961)=109840 intervals; two retained strips contain 44304. There are
64*2769=177216 midpoint summands, four times as many primary center/error
product terms and endpoint candidates, and twice as many polarization squares.
For n windows, n diagonal and 2(n-1) adjacent block slots each carry 64 entries:
(3n-2)*64 gives 1216 and 1024. These are structural work counts, not performance
measurements or guarantees. A covariance on 131072 raw coordinates would contain
17179869184 entries and occupy 128 GiB at eight bytes per entry.

## 2. White centered covariance and its deterministic enclosures

The average centered covariance is
Xi=(sum_a Gamma_aa)/n-(sum_ab Gamma_ab)/n^2. There are n identical diagonal
blocks and n-1 copies of each directed adjacent block. Therefore at unit input
variance

    Xi = ((n-1)/n) Omega - ((n-1)/n^2)(C+C^T).

Taking its trace gives the stated kappa=a*g-2b*c, with no Bessel correction.
Unknown sigma2 and mean dispersion remain separate; the nominal unit response
is not a detector strain prediction.

For any v, let u=U^T v and h=H^T v. They use disjoint columns of A, so
||u||^2+||h||^2<=v^T Omega v. Since |2u^T h|<=||u||^2+||h||^2,
-Omega<=C+C^T<=Omega. Combining with a,b>0 yields lower factor a-b=(n-1)^2/n^2
and upper factor a+b=(n^2-1)/n^2. The advertised [36/49,48/49] and [25/36,35/36]
factors and |tr C|<=tr Omega/2 follow. None needs Gaussianity or a diagonal C.
The asymmetric Q09 check is essential because some transpose mistakes disappear
under a scalar trace or a final symmetrization.

Writing U=U0+E_U and H=H0+E_H expands U H^T-K into three terms. Componentwise
triangle inequalities give exactly |U0|R_H^T+R_U|H0|^T+R_U R_H^T; the
radius-radius term is required. Deterministic coefficient errors need not be
independent. Each sum of four-endpoint product intervals also encloses the
same true entry. Requiring the two intervals to intersect is a consistency
check, not a proof that either arithmetic implementation is correct. Complete
independent reconstruction and the source proof provide the latter obligation.
The midpoint polarization identity is exact for every ordered row pair.

With the inherited |Omega-G|<=H_G, the symmetric response center and error are
Z=aG-b(K+K^T) and F=aH_G+b(E+E^T). This proves all 64 component enclosures.
The sum of diagonal lower/upper bounds equals exactly the independently written
trace formula from trG, trH_G, trK and trE. Recording every entry, both directions
of C, and both trace routes is appropriate. The Loewner bound gives a separate
structural trace interval through (1-rho)G<=Omega<=(1+rho)G. It does not license
entrywise Loewner comparisons or PSD claims about every matrix in an interval
box. Leaving the primary interval unchanged preserves the fixed computation.

The new usefulness gate also follows. Accepted G is positive definite and
||G^-1||_2<=gamma, with 0<=rho<1. Thus Omega>=(1-rho)I/gamma and
Xi>=ell I for ell=((n-1)^2/n^2)(1-rho)/gamma>0. Since F is symmetric and
nonnegative entrywise, ||Z-Xi||_2<=max_i sum_k F[i,k]=delta. Hence
- delta I<=Z-Xi<=delta I and, because delta I<= (delta/ell)Xi,

    -(delta/ell)Xi <= Z-Xi <= (delta/ell)Xi.

The sufficient eps<=10^-12 test is valid. It is a new prospective numerical
usefulness check, not an inherited passed gate, and it must not erase an
otherwise valid enclosure when it fails. The original RI-73 precision gate
and RI-116 width checks remain intact. No actual eps was computed in this review.

## 3. Periodic completion and parity arithmetic

For the explicit finite completion X_j=Z_(j mod M), shifting a window by d=M/2
multiplies Fourier mode k by(-1)^k. Circulant covariance makes the shifted
marginal covariance identical. For M even the conjugate partner M-k has the
same parity. This makes the real cross trace t_even-t_odd and t-h=2t_odd.
The orientation ambiguity of a general shift has no effect here because this
half-period permutation is its own inverse; this does not excuse orientation
loss in the white C record.

For any two output vectors y,z repeated p,q times, direct subtraction of their
common average gives V=pq||y-z||^2/n^2. With zero mean and equal marginal trace t,
E||y-z||^2=2t-2h=4t_odd. Thus the stated factor is 4pq/n^2, namely 48/49 for (4,3)
and 1 for (3,3). The stacked centered output equals a fixed scalar contrast vector
tensored with y-z, so its covariance rank is at most eight. No independence,
Gaussian law or likelihood is implicit. An arbitrary latent mean contributes
the separately displayed pq/n^2 times the squared shifted mean difference.

The toy B=(1,0,-1,0) has a half shift equal to-B, so marginal t=2, h=-2 and
periodic E[V]=2 for n=2. With three alternating windows the factor 8/9 gives 16/9.
By contrast, the genuinely shared-white three-sample operator has adjacent
cross covariance -1 and two-window expectation 3/2. These manual identities
support the proposed fixtures without purporting to have enumerated them.

The one-sided mode convention is crucial. Interior conjugate pairs already
carry weight 2 in each saved c,h_tau,h_alpha; Nyquist carries 1. Multiplying by
lambda=2048*PSD at interior bins and4096*PSD at the endpoints applies the PSD
convention exactly once. No further pair doubling is valid. DC is absent from
the saved nonzero terms under the inherited true-annihilation premise; DC and
Nyquist are even and their centered periodic contributions cancel independently.
Original DC/Nyquist/Parseval evidence is retained, not rewritten.

All PSDs are required finite and nonnegative, so the even/odd error sums are
nonnegative. Their sum must reproduce each entire accepted center/error_tau/
error_alpha exactly. The raw cross interval has center C_even-C_odd and radius
E_even+E_odd. The interval difference t_raw-h_raw, scaled by2pq/n^2, has the same
center as the primary centered interval but radius (4pq/n^2)E_all. The primary
radius is(4pq/n^2)E_odd<=that radius. This proves the proposed containment and
width comparison, including potentially negative lower endpoints. Subtracting
already intersected final intervals is not mode-additive and is prohibited.

## 4. Actual retained source schema and independent oracle

The metadata check confirms RI-100 schema `ri98-mode-weighted-trace-v1`, actual
phase, 8192 ordered nonzero mode records, their exact pair weights, and four
scenario records in H1:left,H1:right,L1:left,L1:right order. Its scenario records
have `source_identity`, not PSD values. RI-96 has all four exact `source_record`
objects with dtype '<f8', shape [8193], 8193 `values_hex` strings and raw-array SHA;
each whole canonical source-record identity matches the corresponding RI-100
identity. Its eight `row_proofs` contain 8193 Q256 rectangles each. Thus the
proposed extra RI-96 input is necessary, and the oracle's source rectangles and
alpha bounds exist where the design expects them. These are schema/identity
checks, not a new reconstruction or acceptance of the numeric values.

The 64*2769 white contractions require the original full capture, and the
proposed separately authored validator must independently parse it and derive
its strips. The alternative error identity
(|u|+r_u)(|h|+r_h)-|u||h| equals all three error terms and is suitable for a
separate arithmetic route. Freshly rebound projections may limit memory, but
must retain their proven parentage to the full admitted capture.

The retained RI-100 independent reconstruction really uses the integer-pair
identity: for endpoint sum m, width w and denominator d=2Q, the component terms
are m^2/d^2, w(2|m|+w)/d^2, and alpha((2|m|+2w)/d+alpha). Only the real component
is active at Nyquist. This matches the requested new oracle design and explains
its 131064 active real-component count. A new implementation must separately
reconstruct all these terms and every reported parity/cross/centering field;
importing the primary or comparing selected totals would not satisfy it.

RI-73 actually has 92 gate records in its declared order, all retained `passed`
values true, with the Gram certificate under the `integration:gram` detail.
The source names its bound matrix `H`; the proposed mathematical notation H_G
is an alias, not a new historical field. RI-116 has four actual scenarios,
six artifacts and all required starts/energies/trace records. Its historical
energy key is `M`, not `Mbar`. Future projection code must bind these literal
existing fields rather than invent similarly named predecessor keys. These are
implementation clarifications, not missing design premises.

## 5. Meaning of the application and remaining prerequisites

The same fixed RI-116 values and same four public-development spectra may be
shown next to these two conditional calculations. That comparison does not
estimate sigma2, select a law, establish model adequacy or create fresh protected
validation. Preserving all four scenarios and exact historical intervals avoids
hidden selection. Exact-only first output is reasonable; any displayed decimals
need their own verified outward rounding. The literal blank Yunits, nominal
V2/C02 status, clear L1 NO_CW_HW_INJ flag, possible injection effects and unresolved
below 10-Hz calibration remain visible. No native prediction is supplied.

For any justified ||Delta Sigma||_2<=eta, the positive matrix D^T Pi D/n gives
|tr(Delta Sigma D^T Pi D/n)|<=eta tr(D^T Pi D/n)=eta*kappa. This holds on the
specified common raw support for either declared comparison model. The new
unit-white coefficient can therefore support a later supplied discrepancy
bound, but supplies no eta itself. A mean bound likewise remains external.
Expanding ||Y0+YDelta||_F^2-||Y0||_F^2 and applying Cauchy-Schwarz gives the exact
calibration bound in equation 13. It concerns the stated factor contribution;
other noise and cross terms do not disappear without additional assumptions.

The implementation assignment is appropriately limited to new exact white-strip
and saved-mode consumers, deterministic joining, separately authored full-field
validation, and a fixed fabricated qualifier. The prospective groups address
boundary framing, directionality, interval dependence and uncertainty products,
new usefulness boundaries, parity and PSD conventions, mean/calibration mistakes,
complete report fields and first refusals. The production-shaped zero fixture
checks exhaustion rather than pretending to be real accepted predecessor bytes.
The exact concrete cases, schemas and refusal codes must still be frozen and
independently source-reviewed; prose obligations are not executed tests.

RI-121's 41 controls per implementation qualify their exact prior sources only.
Changed streaming, interval and saved-mode integration needs its own genuine
qualification. After accepted complete normal execution/custody, optimized
admission is separate. Each real-input stage then needs its own fresh original/
copy/source/runtime/input closure, actual monitor evidence and full independent
mathematics. Accepted dependency outputs are required before the final join.
A failed usefulness or resource check remains evidence; it is not permission to
change precision, rows, data, thresholds, or to fall back to a scalar calculation.
The 180-second and 524288-KiB sampled child limits, 25-ms target poll, 100-ms maximum/
final gap and 50-ms monitor timeout are preserved. The 262144-bit completed-object
bound is not a guarantee about every hidden temporary allocation or performance.
Current runtime/config/loader/namespace and trusted host/cache premises still
require review; a retained qualification report is not an active admission.

## Verdict and next step

No repair to the sealed design is required before root considers design-only
acceptance. Record the literal historical field-name clarification and preserve
all stated prerequisites when writing the source contract. The justified next
step is the source-only implementation/independent validator packet described in
section 9, with no actual input calculation during authoring. Native proof work
continues separately. This review establishes neither successful new execution,
physical noise adequacy, protected validation, calibration nor a geometry/gravity
forward map, and the wider programme remains incomplete.
