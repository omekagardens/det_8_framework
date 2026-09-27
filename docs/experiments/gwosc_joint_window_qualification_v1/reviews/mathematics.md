# RI121 independent saved-moment mathematical review

26 September 2026. Reviewer is a separate, nonauthor agent. Status: **ACCEPT_FIXED_MODEL_MOMENT_RECONSTRUCTION_WITH_SCOPE_LIMITS**. No algebraic defect or missing case/bound field was found in the reviewed reconstruction. This is a source and saved-evidence mathematical review, not a new target execution, qualification campaign or admission.

## Exact reviewed evidence

All paths below are under `/Volumes/AI_DATA/development/det-review-evidence`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| ri121-root-runtime-qualification-jsf0o3_x/review_saved_science.py | 6498 | 7afcbc25cf9a5c1bdd574096270de63248adeff477837a71d780e1fd65000daf |
| ri121-root-runtime-qualification-jsf0o3_x/ROOT_SAVED_SCIENTIFIC_RECONSTRUCTION.json | 2602 | dc9af83ae372cfc7cc2cba345edb6a9160ce7462bd9edba0c2017ccb99d46428 |
| ri121-root-runtime-qualification-jsf0o3_x/metadata.py | 3144 | d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7 |
| ri121-synthetic-caller-repair-7ys8vsc3/controls/normal/RESULT.json | 81253 | 395f217fda2939d096822f9446d01216db4ac54f1d53fe4275830ddd2d05f70a |
| ri119-joint-window-source-119uwunz/CONTRACT.md | 17291 | 13d54fc6af96ca22b793cd47aee7588257ce3b3c1f1e246eaf07e580bee010ab |

The reconstruction source, its small metadata dependency and RI119 contract were read in full as text. The saved reconstruction and scientific result were read as JSON. A separate administrative pass rejected duplicate/nonfinite JSON and confirmed the complete saved report's canonical bytes. Review tools were generic `/usr/bin/python3 -I -B` reads, JSON operations and opaque hashes; no reviewed module was imported, compiled, parsed as Python, or run. No sign enumeration or scientific campaign was performed by this reviewer. Evidence appears in tool outputs `2227d5`, `887c60`, and `4c55a0`.

## Algebra and complete field coverage

The nine literal models in reconstruction lines 33–41 match the fixed contract: M=4, T=3, stride=2; three windows only for Q05/Q07; periodic factor only for Q03; the declared two-row Q09 map; zero Q10 map; constant and quadratic means; signed scales -1 and 2. These expected models do not obtain dimensions, selectors, matrices or scalar answers from the saved cases.

For independent symmetric latent signs z, E[z]=0 and E[zz^T]=I. With raw X=s(mu+Fz), the code correctly forms m=s*mu and Sigma=s^2 F F^T. The unscaled factor and mean remain in `model`; scale is not absorbed into A or output_map. D stacks the declared A-window selectors. Consequently output mean is Dm, covariance K=D Sigma D^T, and the averaging map L=(1/n)[I ... I] gives mean covariance L K L^T. Lines 42–50 implement exactly these identities.

For a block covariance K, the average covariance of centered outputs is
`(1/n) sum_a K_aa - L K L^T`.
This equals the average diagonal blocks of P K P with P=I-(11^T/n) tensor I. No stationarity or symmetric individual cross-block assumption is needed. Thus line 51 is valid also for Q09's asymmetric directed cross-block. Lines 52–55 retain deterministic mean dispersion separately, with
`E[V] = trace(centered covariance) + (1/n) sum_a ||m_a-bar_m||^2`,
`E[U] = (trace(K)+||Dm||^2)/n`, and
`E||bar_d||^2 = trace(L K L^T)+||L Dm||^2`.
The checked decomposition E[U]=E[V]+E||bar_d||^2 follows exactly.

The expected case dictionary has **20 fields**, exactly the contract and saved schema. Initial assignment prose said 21; root acknowledged the prose miscount, with no source/result change required. The line-64 comparison covers the entire case object including model, all selector and map entries, full raw/window/stacked covariances, every directed cross-block, means, all energy fields and sign_count. Canonical JSON comparison against rational-string expectations distinguishes booleans, floats, missing/extra fields, malformed matrices and alternative rational spellings. Although the elementary multiplication helper uses zip, all its operand dimensions come from the fixed construction; saved matrix shapes do not control a calculation and are compared in full.

## Independent discriminating calculations

| Case | E[V] | E[U] | E||bar_d||^2 |
| --- | --- | --- | --- |
| Q02 white two | 3/2 | 2 | 1/2 |
| Q03 periodic two | 2 | 2 | 0 |
| Q05 white three | 16/9 | 2 | 2/9 |
| Q06 constant mean | 3/2 | 2 | 1/2 |
| Q07 quadratic mean | 400/9 | 566/3 | 1298/9 |
| Q08 scale -1 | 3/2 | 2 | 1/2 |
| Q08 scale 2 | 6 | 8 | 2 |
| Q09 oriented matrix | 5/2 | 4 | 3/2 |
| Q10 zero map | 0 | 0 | 0 |

For white scalar windows, diagonal variances are 2 and adjacent covariance -1. For three windows the far covariance is zero, so mean variance is (6-4)/9=2/9 and centered contribution 16/9. For periodic Q03 the second output is the negative of the first: off-diagonal covariance -2, mean variance zero, E[V]=2. These use different actual joint laws despite equal marginal variances.

Q07's output mean is [-4,-12,-20], with mean -12 and mean dispersion (64+0+64)/3=128/3. Adding the covariance contribution 16/9 yields 400/9; mean-output energy is 144+2/9=1298/9. Constant Q06 mean is annihilated by the actual row sum of A.

Q09 has same-window Omega=[[2,1],[1,2]], forward block C=[[-1,0],[-1,0]], and reverse C^T=[[-1,-1],[0,0]]. Hence mean covariance is (2*Omega+C+C^T)/4=[[1/2,1/4],[1/4,1]], and centered covariance is Omega minus this, namely [[3/2,3/4],[3/4,1]]. Both orientations and all off-diagonal entries are present in the saved result and the full comparison. The trace alone is not used as a substitute.

Signed scale enters the raw mean linearly and covariance quadratically. For the declared linear map, output(s,z)=s*output(1,z) for each z. However the zero-mean Q08 second moments are invariant under s=-1 versus s=1: agreement of those moments does **not** establish that the primary actually executed its signed pointwise checks. Sign_count likewise is a compared expected count, not an execution trace.

## Q12 bounds

All three complete bound dictionaries are compared in the required order at line 75. They retain output dimension one and the full fixture matrices.

- Calibrated constant: A diag(1,1,2) [1,1,1]^T = 1-2 = -1. Universal constant annihilation is therefore correctly false.
- Covariance error: Pi D=D for D=[1,-1]^T, so `trace(Pi D D^T Pi)/2=1`. Scalar covariances 1 and 2 give contributions 1 and 2; difference and eta=1 bound both equal 1.
- Calibration error: C0=DeltaC=F=1 gives model factor 1 and perturbed factor 2, hence contributions 1 and 4. Difference 3 equals the declared quadratic bound `(2*|C0|*|DeltaC|+|DeltaC|^2)*1=3`.

The scalar multipliers and calibrated output literal in the reconstruction are fixed fixture declarations whose arithmetic is independently verified here. They are not estimated nuisance bounds, empirical calibration, or general calibration-error validation.

## Acceptance scope and remaining evidence

The saved reconstruction's status `ALL_9_CASES_AND_3_BOUNDS_MATCH_IN_FULL` is supported by its complete fixed-model construction and comparisons; its summary scalars agree with the independent reasoning above. I did not rerun that source or independently repeat every numerical matrix multiplication through a second executable. This review adjudicates its algebra, implementation and saved result consistency; root's genuine invocation/custody evidence is separate.

Lines 77–79 check refusal counts and equality of the saved primary/validator/expected labels, but do not independently bind every control ID or expected label to the frozen inventory. The reconstruction also does not independently compare all qualification-envelope fields. Therefore it is not a standalone full qualification-report guard. Root reports that the separate custody review binds those envelope fields and frozen labels through pinned REPORT_DOMAIN; this review does not substitute for that separate check.

Actual Q06/Q08 pointwise guards, negative-control execution, complete target execution, normal/optimized equality, resource fit and source/runtime custody must be established by the actual captured caller/worker evidence and its independent custody adjudication. Setting direct_average_V to the independently derived moment value verifies the saved number, but does not itself reproduce the primary's pointwise averaging. The source explicitly preserves these distinctions.

No physical joint-window law, protected validation, empirical significance, native forward map, or geometry/gravity result follows from this exact finite synthetic arithmetic. No change to the reviewed source or saved result is required by this bounded mathematical review.
