# RI-123 — applying the qualified joint-window identities to the retained real operator

27 September 2026 UTC. **Prospective application design for independent review.**
No target, coefficient contraction, new PSD calculation, empirical-data processing,
qualification campaign or runtime admission has been executed. This note builds on
accepted RI-118 and actual RI-119/121 synthetic qualification. Its two calculations
are conditional conventional moment calculations, not selected physical noise laws.

The next useful result is a complete eight-coordinate overlap certificate for the
actual retained operator, accompanied by a deliberately labeled periodic-completion
stress comparison using already saved public-development spectra. Both avoid a raw
covariance matrix and preserve all four RI-116 rows without refitting or selection.
The white calculation supplies a response per specified unit input variance; the
periodic calculation supplies a concrete illustration of the extra joint-law premise
at the scale of the fixed empirical proxy. Neither supplies a calibrated prediction.

## 1. Fixed domain and exact support

Retain the complete RI-104/116 method without alteration:

```
fs=4096; raw length=131072; M=16384; stride d=8192
N=2769; L=4096; T=N+2L=10961; output dimension r=8
I=(0,1,27,805,1384,2741,2767,2768)
left starts=(0,8192,16384,24576,32768,40960,49152), n=7
right starts=(69632,77824,86016,94208,102400,110592), n=6
scenario order=(H1:left,H1:right,L1:left,L1:right)
```

Every window uses the first T samples of its retained M segment, not a centered T
crop. The short center is [4096,6865) relative to its start. The exact rational
finite-filter definition, 17 stage order, odd extensions, states, reversal,
unpadding and selected rows remain those of RI-55/60/73. Write

    P=J F_N C, Q=J C F_T, A=Q-P, B=[A,0_(8 by 5423)].

A is 8 by 10961 and annihilates constants by the accepted true-operator premise.
Interval midpoints need not annihilate constants and must never be projected.
This is the finite exact operator, not a newly rounded filter or FFT approximation.

For a side, W_a selects its T coordinates from the common raw vector; L_a=A W_a.
Only neighboring T windows overlap, in exactly T-d=2769 coordinates. M windows
overlap in 8192 coordinates; those two overlaps must not be confused. The T unions
are [0,60113) and [69632,121553), with respective lengths 60113 and 51921.
The M unions remain [0,65536) and [69632,126976). No endpoint is inclusive.
The different sides' T unions are disjoint, but physical cross-side independence
is not assumed: these are separate expectations with no pooled statistic.

## 2. The inherited identity and the proposed two model records

Put D=stack(L_a), H_n=I-11^T/n, Pi=H_n tensor I_8. For a stipulated raw mean mu
and covariance Sigma with finite second moments,

    Gamma_ab=L_a Sigma L_b^T,
    Xi=(1/n) sum_a Cov(d_a-bar_d),
    E[V]=tr(Xi)+b_mu,
    Xi=(1/n) sum_a Gamma_aa - (1/n^2) sum_(a,b) Gamma_ab,
    b_mu=||Pi D mu||^2/n.                                      (1)

This is RI-104 equation (5)/RI-118 equation (1), reused without dropping the mean
or cross terms. The observed V still has divisor n. Its observed coordinatewise
sample centering neither estimates mu nor proves b_mu=0.

The first output has model id `shared_raw_white_unit_response`: Sigma=sigma2 I,
mu unspecified, and a dimensionless response at sigma2=1. The real detector's
sigma2 and b_mu remain null/unresolved. A symbolic conditional expression is
reported; an arbitrary unit variance must not be displayed as a strain prediction.

The second has model id `periodic_completion_of_retained_proxy`: for each fixed
scenario take the already accepted finite circulant K_s and one M-vector Z with
Cov(Z)=K_s, then set X_j=Z_(j mod M) relative to that side's first start. In its
stated zero-mean stress subcase E[Z]=0. This is a coherent shared-sample completion,
but exact M-periodic repetitions are an extra strong assumption. It is not chosen
as the detector noise hypothesis, nor fitted to the RI-116 table. Its use in a
stress comparison is frozen here before any new result is evaluated.

There is no Gaussian, likelihood, ergodicity or stationarity-of-the-actual-data
premise. Cross-detector covariance is unnecessary for these individual records;
that does not establish detector independence.

## 3. White response: contract only two small coefficient strips

Define the two 8 by 2769 strips

    H_ij=A_(i,j), U_ij=A_(i,j+d), 0<=j<2769,
    Omega=A A^T, C_shift=U H^T.                               (2)

Orientation is fixed: Gamma_(a,a+1)=sigma2 C_shift, since coordinate j+d of the
earlier window equals coordinate j of the next. The opposite block is its
transpose. All blocks at distance two or more are exactly zero under this model.
Do not symmetrize C_shift before recording it.

**Useful support reduction.** Both [0,2769) and [8192,10961) lie wholly outside
P's [4096,6865) support. Therefore H=Q[:,0:2769] and U=Q[:,8192:10961] exactly.
No short-operator coefficient appears in this shifted product. The full captured
short/long rows must nevertheless be admitted and their grammar/order exhausted;
the reduction is not permission to accept an incomplete capture or alternate A.

For n=6 and n=7 let a=(n-1)/n and b=(n-1)/n^2. Then

    Xi_n=sigma2 Xi_n^(1), Xi_n^(1)=a Omega-b(C_shift+C_shift^T),
    kappa_n=tr(Xi_n^(1))=a g-2 b c,
    g=tr(Omega), c=tr(C_shift), E[V]=sigma2 kappa_n+b_mu.       (3)

Only one real-operator C_shift is required for both detectors and sides. Two
matrix/trace response records (n=7,6) then serve all four observed scenario rows.
Xi_n^(1) means the unit-variance response, so no division by an unknown or zero
sigma2 is performed.
C_shift is new work; the original one-window Gram is not recomputed gratuitously.

For any vector v, the disjoint head/tail support gives

    -Omega <= C_shift+C_shift^T <= Omega,
    ((n-1)^2/n^2) Omega <= Xi_n^(1)
                         <= ((n^2-1)/n^2) Omega,
    |c|<=g/2.                                                (4)

This is RI-118's bound. The factors are [36/49,48/49] for seven windows and
[25/36,35/36] for six. They remain conditional matrix/trace bounds; they are not
claims about ratios of the recorded V values. No independent-window substitution
or n/(n-1) adjustment is allowed.

### Exact interval certificate

Read the retained complete RI-73 capture, 51,891,508 bytes/SHA
`fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba`.
Use the accepted 8 MiB-per-row/64 MiB-whole streaming grammar and ninth-item
exhaustion guard. Decode all 109840 intervals, but retain only the two strips
needed for (2), plus the small per-row identities. Hash the complete consumed
snapshot and recheck descriptor/path identity. Capture validity and original
adjoint correctness are inherited premises, not newly proved by contraction.

For H=H0+E_H, U=U0+E_U, with component radii R_H,R_U, compute exactly

    K=U0 H0^T,
    E_ik=sum_j (|U0_ij| R_H(k,j)+R_U(i,j)|H0_kj|
                +R_U(i,j)R_H(k,j)),                         (5)

Equivalently
E=|U0| R_H^T + R_U |H0|^T + R_U R_H^T. Thus
|C_shift-K|<=E entrywise. Here K and E are 8 by 8, generally nonsymmetric.
All j sums in this strip formula range over 0,...,2768.

Separately retain direct four-endpoint-product sums for all 64 entries. Require
each direct interval to intersect [K_ik-E_ik,K_ik+E_ik], without replacing the
primary interval by an adaptively chosen intersection. Correlated coefficient
errors are not random or independent; these are deterministic enclosures of the
same actual operator. For midpoint verification only, the independent identity
4 K_ik=||U0_i+H0_k||^2-||U0_i-H0_k||^2 supplies an exact alternate formula.

Reuse the complete accepted RI-73 `integration:gram` certificate (G,H_G,delta,
gamma,rho and all inherited gates), where G is the coefficient-midpoint Gram,
|Omega-G|<=H_G, ||G^-1||_2<=gamma and rho<=10^-12. Do not take a same-shaped
unbound G or call it the true Omega. Admit the full RI-73 result and acceptance
chain; inspect schema, all 92 gate identities, status, dimensions and exact
`integration:gram`/`integration:accuracy` records, not only a success label.
Then form

    Z_n=a G-b(K+K^T), F_n=a H_G+b(E+E^T),
    Xi_n^(1) entrywise in [Z_n-F_n,Z_n+F_n].                (6)

Record all 64 entries for each n, their exact trace interval, and the trace
obtained separately from g/c. These must agree as algebraic primary formulas.
Require intersection with the explicit structural trace interval
[((n-1)^2/n^2)(1-rho)tr(G), ((n^2-1)/n^2)(1+rho)tr(G)] from (4), not
entrywise Loewner tests on interval endpoints. A matrix whose entries lie in an
interval box need not be PSD. Structural PSD is supplied by the joint factor
construction and (1); there is no eigenvalue clipping, ridge or inversion here.

A prospective, scale-free numerical usefulness test is explicit rather than
hidden in a small decimal display. Set

    delta_n=max_i sum_k F_n(i,k),
    ell_n=((n-1)^2/n^2)*(1-rho)/gamma,
    eps_n=delta_n/ell_n.                                     (7)

The accepted positive G/rho premises make ell_n>0 and Xi_n^(1)>=ell_n I.
Hence -eps_n Xi_n^(1) <= Z_n-Xi_n^(1) <= eps_n Xi_n^(1).
Require eps_n<=10^-12 for the new `usefulness_passed` state, while retaining the
separate enclosure/theorem state. This is a **new prospective check** on the
new shift contraction, using the existing precision convention; it is not a
previously passed RI-73 gate. If it fails, preserve the valid broad enclosures
and report `accuracy_failed`; do not change rows, precision, formula, threshold
or data. The original RI-73 rho gate and RI-116 width gates stay unchanged.

## 4. A cheap, explicit periodic-completion stress calculation

A half-M shift has Fourier phase exp(2 pi i k d/M)=(-1)^k. Let t_s be the
retained total marginal trace and h_s=tr Cov(BZ,B shift_d Z). Under the stated
circulant completion,

    t_s=sum_k lambda_sk p_k,
    h_s=sum_k (-1)^k lambda_sk p_k,
    t_s-h_s=2 sum_(k odd) lambda_sk p_k.                       (8)

Conjugate frequency pairs share parity because M is even. p_k uses exactly the
RI-100 one-sided weights: 2 on k=1,...,8191 and 1 on Nyquist k=8192. DC remains
under the original true-annihilation premise. Independently, both DC and
Nyquist are even and cancel from the centered periodic expression. Neither
fact permits altering the historical DC, Nyquist or Parseval records.

There are p repeated even-phase outputs and q repeated odd-phase outputs.
The exact finite centering identity gives

    V=pq/n^2 ||d_even-d_odd||^2,
    E[V]_periodic,zero-mean=(4pq/n^2) t_s,odd.                 (9)

Thus the factors are 48/49 on the left (p,q)=(4,3) and 1 on the right (3,3).
The latent law may be non-Gaussian. This derivation uses only its covariance.
The centered stacked covariance has rank at most eight because there are only
two repeating eight-vectors; it must not be treated as n independent outputs.

**The actual retained schema matters.** RI-100 saves 8192 common `mode_terms`
with k,pair_weight,c,h_tau,h_alpha. It does *not* save the PSD or scenario-specific
lambda array in its result. Its four `source_identity` fields bind the original
PSD source records. Consequently the operand set must also include the exact
RI-96 result, 41,673,703 bytes/SHA
`5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580`,
whose four scenarios contain the complete `source_record` with dtype, shape,
values_hex and raw-array SHA. Do not infer weights from the scalar trace.

Admit both complete bodies before parsing; require their fixed headers/gate
inventories and each exact source-record identity. Decode all 8193 original
binary64 PSD values per scenario by the retained exact convention. Keep
lambda=4096 PSD at DC/Nyquist and 2048 PSD at interior bins. Require finite,
nonnegative values and complete original little-endian-array identity. No PSD
re-estimation, FFT, demeaning, taper or altered calibration is performed.

If c_k,h_tau,k,h_alpha,k are the already accepted RI-100 center/error terms,
calculate, separately for even and odd nonzero k,

    C_par=sum lambda_sk c_k,
    E_tau,par=sum lambda_sk h_tau,k,
    E_alpha,par=sum lambda_sk h_alpha,k.                      (10)

Retain all six sums. Even+odd must reproduce the entire accepted RI-100 center,
error_tau and error_alpha exactly for each scenario. This consumes *raw* terms,
not the previously intersected `final` interval as if it were mode-additive.
The raw signed cross-trace enclosure is
[C_even-C_odd-(E_even+E_odd), C_even-C_odd+(E_even+E_odd)].
The primary new centered prediction is

    (4pq/n^2) [C_odd-E_odd,C_odd+E_odd].                       (11)

Keep it exactly as constructed, including any negative lower endpoint. The true
quantity is nonnegative structurally, but no clipping or tuned intersection is
part of this contract. Independently check containment in the wider naive
2pq/n^2*(t_raw-h_raw) interval and preserve both routes. The primary parity
formula cancels the even modes *before* interval arithmetic; subtracting two
independent intervals destroys that dependency and is not the primary method.
Since E_odd<=E_all, the new width is at most 4pq/n^2 times the RI-100 raw width.
This is deterministic width accounting, not empirical uncertainty or adequacy.

For an unspecified periodic mean m_Z, add
b_mu=pq/n^2 ||B(m_Z-shift_d m_Z)||^2. This is not generally zero. The zero-mean
stress record is clearly distinguished from this unresolved general expression.
A common nominal constant is annihilated by the true A; an arbitrary population
mean, signal or injection is not.

## 5. Joining to RI-116 without rereading or tuning the observations

Consume the complete accepted 2,296,321-byte RI-116 result (SHA
`ca9405768281584afcf7ddba9644e262d81e6c59f4291ca387367c5c013f1c9b`)
and root/independent acceptance. Preserve all four scenario ids, starts, row
order, n, exact U/Mbar/V intervals, and original RI-100 trace intervals. New
application records bind these unchanged fields by exact canonical projection
identity. There is no new HDF5 extraction, raw filter evaluation or centering.
The existing six RI-116 artifact identities remain provenance references; their
bytes need not become numerical operands for this saved-result comparison.
No numeric output here establishes that the old extraction was independently
repeated. The completed RI-116 endpoint-validator/custody chain supplies that
premise. If a later target wishes to reread raw samples, it needs its own full
input admission and cannot silently expand this operand set.

Display four records, always in the original order:

* retained observed V (nominal strain squared), unchanged;
* retained single-window marginal proxy trace t_s, unchanged and labeled;
* the unit-white operator coefficient kappa_n, dimensionless, with the symbolic
  `sigma2*kappa_n+b_mu`, sigma2=null and b_mu=null for physical interpretation;
* the periodic-zero-mean proxy-completion interval (11), in nominal strain
  squared, labeled `hypothetical_joint_completion_not_physical_prediction`;
* explicit model/covariance/mean/calibration adequacy status `not_established`.

Do not report a fitted white sigma2=V/kappa_n, a residual z-score, standardized
ratio ranking, p-value, chi-square, SNR, empirical pass/fail or a chosen preferred
side/model. A displayed difference or resemblance must not become acceptance.
The first release can contain exact intervals only; any decimal display needs
an independently checked outward-rounding record, not ordinary formatting.

## 6. What can and cannot bound the remaining terms

The numerical coefficient and transform enclosures are available. A physical
covariance error bound, population-mean bound and calibrated observation operator
are not supplied by these predecessors. Record them as unavailable rather than
putting a zero, estimating them from these same four V values, or treating the
RI-100 enclosure width as one of those uncertainties.

For either declared nominal model, a separately justified bound
||Sigma_true-Sigma_model||_2<=eta on the relevant common raw support yields

    |covariance contribution error|<=eta kappa_n,              (12)

because ||Pi D||_F^2/n=kappa_n from the shared-white operator calculation.
Use its exact upper enclosure when eta>=0 is later supplied with its units and
scope. There is no eta value in this design. Likewise a supplied mean norm can
be propagated through the actual map; absent such a premise b_mu is unresolved.
A scalar temporal-mean subtraction is not a substitute.

For a future factor model and calibration C_0+Delta_C, let
Y0=Pi D C_0 F and YDelta=Pi D Delta_C F. Then

    |calibrated covariance contribution change|
       <=(2 ||Y0||_F ||YDelta||_F+||YDelta||_F^2)/n.            (13)

Only factor actions need evaluation; the raw covariance need not be formed.
Independent measurement noise and cross terms are not implicit assumptions.
No actual calibration factors or finite eta/mean envelope are chosen here.

Retain nominal V2/C02 provenance, blank literal Yunits, the known clear L1
NO_CW_HW_INJ flag, possible injection effects and unresolved calibration below
10 Hz. The existing empirical PSDs and V values use the same already inspected
public windows: they are development/calibration evidence, never fresh protected
validation. A validated noise model would additionally need a prespecified
estimation/evaluation protocol and justified nuisance bounds. A native geometry
or gravity test still requires a quantitative source/observer forward map.
RET alone remains paused.

## 7. Size and feasibility accounting

These counts are exact consequences of source dimensions, not timings or newly
computed coefficient values:

| Object/work | Fixed size |
|---|---:|
| Full raw covariance, deliberately never formed | 131072^2 = 17179869184 entries (128 GiB even at 8 bytes/entry) |
| White output covariance sizes, if explicitly materialized | 56 by 56 left; 48 by 48 right |
| Nonzero block slots before actual numerical zeros | 1216 left; 1024 right |
| Original captured intervals requiring grammar validation | 109840 |
| Retained head+tail interval strips | 8*2*2769 = 44304 |
| Midpoint multiplication summands for full directed shift | 64*2769 = 177216 |
| Primary midpoint plus three error-product summands | 4*177216 = 708864 |
| Direct four-endpoint-product candidates | 4*177216 = 708864 |
| Midpoint polarization square terms | 2*177216 = 354432 |
| Diagonal-only midpoint summands, a subset | 8*2769 = 22152 |
| New output matrices | C_shift center/error/direct box plus two 8 by 8 response center/error matrices |
| Retained nonzero one-sided modes | 8192, with 4096 odd and 4096 even (including Nyquist) |
| Complete source PSD bins | 4*8193 = 32772 |
| Three scalar mode-weight products, all parities/scenarios | 4*8192*3 = 98304 |
| Independent mode oracle source rectangles | 8*8193 = 65544 |
| Active real components in the nonzero mode oracle | 131064 |

The above work counts identify algebraic summands, not integer-machine
instructions, reductions, parsing overhead or totals for both implementations.
No 56 by 131072 dense selector, sample covariance estimate or Monte Carlo
campaign is needed. Store starts/selectors as integer ranges, the white block
covariance as Omega/C_shift/C_shift^T plus the exact zero pattern, and the two
periodic phase multiplicities as integers. Full 8 by 8 C_shift is compulsory;
a scalar c cannot substitute for the directional-matrix checks.

Primary exact contractions may lift each retained strip row's endpoints to a
common positive denominator, accumulate checked integer products, and reduce
completed rational operations. This is the reviewed RI-116 acceleration pattern,
not a floating shortcut. Retain at most one full decoded capture row plus the
small strips; release parsing trees before reading the next row. The full
RI-96 JSON tree and capture row arrays need not coexist: extract/check/hash the
required PSD/rectangle records, release their parent, then work on the next
fixed stage. A separately authored validator can process row pairs or saved
small strip projections under freshly bound custody rather than copy all eight
full A matrices. Any projection used numerically must be derived and rebound
from the admitted full capture; a standalone projection hash is not proof of
its parentage.

The inherited 262144-bit explicit integer/reduced-rational guard, 8 MiB row and
64 MiB capture caps remain. A bound on completed rational objects does not cap
all internal temporary multiplication allocations. These operation counts show
structural feasibility, not a guaranteed runtime/memory result. Actual calls
retain 180 s numerical child, 524288 KiB sampled sole-child RSS, 25 ms target
poll, 100 ms maximum/final gap and 50 ms ps timeout. If full qualification or
actual C_shift does not fit, preserve failure; no automatic scalar-only fallback,
row drop, precision escalation or weaker gate is authorized.

## 8. Exact output and independent oracle contracts

Use three separately identified outputs so one missing premise cannot be hidden
inside a partial-success application report:

1. `WHITE_COUPLING.json`: closed top sections `schema,phase,status,method,
   provenance,operator,shift,white_responses,checks,limitations`. Operator binds
   full RI-73 result/capture, G/H_G/gamma/rho, eight row identities and shape.
   Shift records all 64 K/E/direct intervals with head/tail orientation and c.
   `white_responses` contains n=7 then n=6, full Z/F/entry intervals, trace routes,
   structural bounds, delta_n/ell_n/eps_n and distinct enclosure/usefulness states.
   The unit variance is mathematical only. No detector noise amplitude field is
   silently filled. Actual phase differs from conspicuously fabricated fixtures.
2. `PERIODIC_COMPLETION.json`: closed top sections `schema,phase,status,method,
   provenance,mode_domain,scenarios,checks,limitations`. Four exact scenarios
   each retain source-record identity, both parity counts/centers/error splits,
   full-trace reconciliation, signed h interval, phase multiplicities, primary
   centered interval and wider t-h check. Zero mean and exact periodic repeats
   are literal model premises; no physical adequacy status can be true.
3. `APPLICATION_COMPARISON.json`: closed top sections `schema,phase,status,
   method,provenance,scenarios,nuisance_premises,checks,limitations`. It binds
   *accepted complete* first/second outputs and RI-116; copies the specified
   exact historical projection; joins all four rows as in section 5; declares
   every missing physical nuisance input. It never fabricates success when a
   dependency failed. A valid white enclosure with failed usefulness can be
   separately reported as inconclusive and does not trigger another run.

The implementation packet must freeze literal schema strings, every subrecord
key, canonical exact hex rational encoding, full check/refusal inventories and
all failure states before execution. This design is not that future executable
contract. Scientific results are deterministic across normal/optimized modes;
mode-specific process facts belong in separate custody receipts. Never accept
an invented historical field in a source-only template.

Independent validation must use separately authored arithmetic and independently
admitted input parsing; no primary import or reuse of its computed dictionaries.
For white coupling it reconstructs all strip endpoints and all 64 exact midpoint
products/error bounds, verifies the four-endpoint box and polarization route,
then all entries and scalars of both responses. Its error calculation may use
(|u|+r_u)(|h|+r_h)-|u||h| instead of the primary three-term expansion, with exact
integer-pair arithmetic; independent complete field comparison remains required.

For the periodic record, an independent oracle rebuilds c/h_tau/h_alpha from the
RI-96 Q256 rectangles and alpha bounds, using the retained RI-100 integer-pair
product identity. It verifies all mode order/weights and all PSD values, then
computes the centered spectral weights directly as
2pq/n^2*(1-(-1)^k), before accumulation. This equals zero on even modes and
4pq/n^2 on odd modes. It reconstructs every output field, including full-trace
reconciliation, rather than comparing a few totals. No new FFT, adjoint or
original covariance-model validation is claimed. The earlier complete RI-100
mode audit is an inherited premise, not relabeled as this new oracle's execution.

For the joined report, independently reconstruct all four mappings and copied
historical fields, dimensions/starts/units/statuses, not only report hashes.
Root separately reviews actual execution/custody and complete saved mathematics.

## 9. Bounded implementation and meaningful qualification sequence

**Next concrete assignment after independent design acceptance:** prepare one
source-only implementation packet containing the new exact white-strip consumer,
periodic saved-mode consumer, deterministic join, separately authored validator,
and fixed fabricated qualifier. Reuse immutable predecessor source patterns only
through reviewed deltas; do not edit RI-116, RI-118, RI-119, RI-121 or their data.
No actual operator or saved public-data target runs during source preparation.

Keep the two arithmetic stages independently admissible. First qualify the whole
new packet on fixed fabricated operands in genuine normal and optimized modes.
After full acceptance, root can admit the white real-operator stage and the
periodic saved-input stage separately, each followed by full validation/custody
review. The final join uses accepted results, with no new numerical campaign.
A failure in one stage remains visible while unrelated native work continues.

Prospective qualification groups must include at least these exact obligations;
the implementation freezes the complete concrete cases and reason codes before
execution, not a count invented by this design:

* Boundary selectors and source framing: first-T/M/short maps, final endpoints,
  exact shared head/tail coordinates, nonneighbor zero blocks, all eight rows,
  wrong crop/stride, missing/ninth row, altered complete body and retained footer.
* Exact white/asymmetric cases: reuse the mathematical RI-119 Q02/Q05/Q09
  expectations as source premises and independently re-evaluate the new kernel
  on these tiny declared domains. Q09 C=[[-1,0],[-1,0]] and Xi_2=
  [[3/2,3/4],[3/4,1]] must pass entrywise; a lone transpose, omitted cross block or
  silent symmetrization must fail. Production shape has a sparse rational fixture
  with nonzero first/last overlap coordinates, plus all-zero primitive cases.
* Interval dependence: exact endpoint enumeration on small head/tail boxes,
  mixed signs/zero radii, asymmetric off-diagonals, midpoint polarization, and
  error product-versus-expanded equality. Distinguish valid containment from
  the separate new usefulness gate; wide toy boxes must not masquerade as passing
  actual precision checks. Test eps just below, at and above 10^-12 using explicit
  fabricated certificates; never replace old coefficient gates.
* Periodic exact law: M=4, A=(1,0,-1), white K=I_4 gives periodic E[V]=2 for
  n=2, distinct from shared-white 3/2. Enumerate all sixteen latent sign vectors
  in the tiny fixture only. For three alternating windows p=2,q=1, the same
  model gives 16/9. Check n=6 and n=7 multiplicity factors 1 and 48/49 directly.
  A full-M pure even/Nyquist toy mode has zero centered periodic contribution,
  despite nonzero marginal trace; it is not substituted for the production
  first-T operator. Include odd-only, mixed-parity, DC-only and zero PSD fixtures.
* Spectral conventions: wrong interior/Nyquist factors, changed PSD bytes/hash,
  negative/nonfinite values, odd/even misindex, extra Nyquist doubling, missing
  source-record identity, using final scalar interval as additive mode terms,
  dropping uncertainty cross terms and false equality of wide/tight endpoints.
  A fully labeled production-shaped zero spectral fixture tests complete schema
  and 8192-mode/32772-bin exhaustion without pretending to be a real predecessor.
* Mean/calibration boundary: constant nominal mean cancellation only with its
  true-A premise; a nonconstant mean and the retained Q12 calibrated-constant
  counterexample must prevent b_mu=0 by default. Missing eta/calibration inputs
  remain null; no calibration envelope is synthesized from numerical error.
* Full report/refusal controls: every nested result field and limitation,
  strict integer-versus-bool typing, reduced rationals, all existing size/bit
  limits, canonical JSON/duplicate-key rules, full scenario order, each historic
  U/Mbar/V copy and exact input provenance. Changed output and wrong first refusal
  fail. Actual-input entry guards must reject fabricated pins before numerical
  decode; no synthetic identity impersonates accepted public evidence.

All of RI-121's 41-per-implementation controls remain preserved historical
qualification of their exact source. They do not automatically qualify this
new streaming/interval/saved-mode integration. Conversely, no new FFT or HDF5
branch is present, so unrelated historical numerical campaigns are not repeated
under a new label.

## 10. Custody, provenance and stopping rules

`PREDECESSOR_PINS.json` names source/design/accepted-result identities inspected
or hashed while authoring. It is a source/premise manifest, not an active freeze
or a substitute for transitive admission. Coordinating plan pins are historical
context snapshots. Future root admission must freeze exact original/copied
source, all consumed full input bodies, original execution/capture/acceptance
history, named interpreter/aliases, complete current runtime and command/env,
exclusive outputs, actual monitor and failure-tail source, and separate stages.

RI-121 supplies current actual profile and repaired helper evidence. A changed
caller still requires reviewed applicability and any meaningful new guards; it
cannot inherit permission from copied success files. Full stdlib/site/source/
cache/interpreter and non-OS loader/config closure, required external namespace/
selection/observed-dyld sidecars, and trusted stable Apple-host premises remain
explicit. A runtime-only change does not allow changing the scientific operator.
Preserve RI-110's original failed caller evidence, RI-108's narrowly inherited
numerical applicability and RI-114's distinct interface qualification; none is
renamed as qualification of this new application.
Use only the root-admitted caller. Normal completion and independent review must
precede a separate optimized admission. Retain every failure and partial output,
raw monitor attempt and genuine outer exit, all before/after identities and exact
whole-output equality. No automatic retry on a changed threshold or operand.

The actual coefficient capture has only been opaque-hashed during this design,
not decoded. Published prior JSON bodies were inspected for schema/key/count
locations only, not newly contracted into numerical results. No raw HDF5,
float64 strain artifact or protected body was read. No file in the repository,
active runtime, existing evidence packet, admission or Git index was modified.
The author previously independently reviewed RI-118/119/121 source and custody;
this new design is their own proposal, so independent mathematical review and
root adjudication are still required. The native programme continues separately.
