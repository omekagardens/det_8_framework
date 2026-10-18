# QR-05: bounded exact measure/divergence verification

12 September 2026. Prospective executable contract implementing the
[analytical design](../qr-05-measure-divergence-design-2026-09-12/README.md).
Freeze all sources before first mathematical execution. No physical operator,
geometry acquisition, continuum theorem, quantum dynamics or RET readiness is
selected or established by this finite supplied-graph study.

## Fixed domain and independent routes

Use exactly the nine base cases and four separate variants in
[protocol.json](protocol.json), case-major then variant order. The 36 rows
retain 92 full-node occurrences, 56 edges, 252 cells per full square node
matrix, 72 dynamic-node occurrences and 168 effective square matrix cells.
Keep symmetric duplicates. No fixture sweep, adaptation or compositions.

Primary assembles L=BᵀKB with explicit matrix multiplication; reference
assembles L,Q and balances by independent neighbor exchange. Neither reads
or imports the other, or shares a mathematical helper. Each independently
constructs the literal fixed cases. A third test oracle uses analytical base
Q matrices. Compare complete native Fraction/int/bool reports before encoding.
The proof for arbitrary finite graphs remains analytical, not established by
these 36 rows alone. This executable subclass has one scalar coordinate per
node; the design's multidimensional theorem is not numerically exercised here.

## Pure API and transformations

Each engine provides evaluate(world) and analyze(), with no I/O, randomness
or input mutation. evaluate accepts exactly a plain dict with keys
mu,edges,k,x,mode,I,D,f,g,q. All vectors are plain lists. mu has length n,
1≤n≤3; mu,k,x,f,g,q entries are plain Fractions with absolute numerator and
denominator bit lengths≤128. mu>0, k≥0; other rational values may be signed.
No output-rational cutoff. Reject malformed inputs with ValueError; never
coerce or repair. Reject subclasses, bool-as-int, floats and nonnative types.

edges is a plain list of plain two-element lists [tail,head], with distinct
plain-int labels in range(n). No self-loops or repeated undirected edges,
even opposite orientations. k has one value per edge, and x,q length n.
Zero-conductance edges and empty edge lists are valid and retained.
mode is exactly a plain str: closed, flux or dirichlet.

I and D are ordered lists of unique plain-int labels and partition all nodes.
f has length len(I), g length len(D). In closed/flux mode I=range(n) in that
order, D=g=[]; closed additionally requires q=0. In dirichlet mode I and D
are both nonempty, their order is arbitrary, and q=0. f is in I order, g in
D order. No aliases to caller-owned mutable containers may appear in output;
otherwise-valid shared input containers are accepted and copied.

Variants: identity; cyclic old i→(i+1) mod n; reversal of every edge's tail
and head; rescale mu,k,q by c=3/2 with x,f,g held fixed. Keep edge order.
Cyclic relabeling permutes full vectors mu,x,q. For closed/flux keep canonical
I and permute f as a full-node vector. For Dirichlet transport the ordered I,D
lists and keep f,g in those transported orders. Do not sort them afterward.
These conventions implement the prior design's full-versus-active ordering.

## Exact evaluate schema

The row has EXACTLY these keys:
world,B,W,K,L,Q,full,flux,components,kernel_basis,kernel_images,reconstruction,
reduced,balances. world is a fresh copy of the admitted input. Every numeric
matrix/vector/scalar below is Fraction-valued, including B and indicator
bases; labels and component lists are plain ints; flags are plain bools.
Empty K is [] and empty B is [] for a zero-edge graph; L,Q,W remain n×n.

- B: edge×node incidence, −1 tail/+1 head. W=diag(mu), K=diag(k),
  L=BᵀKB, Q=−W⁻¹L.
- full: exactly m0,m1,m2,Q1,Qx,Qx2,counting_columns,weighted_columns,
  adjoint_residual,energy_form. m0_i=sum_j Qij,
  m1_i=sum_j Qij(xj−xi), m2_i=½sum_j Qij(xj−xi)². Q1,Qx,Qx2 are actual
  matrix actions on 1,x,x². counting_columns=1ᵀQ, weighted_columns=1ᵀWQ,
  adjoint_residual=WQ−QᵀW, energy_form=−WQ. Do not substitute pointwise η.
- flux: exactly field,gradient,J,influx,Qf,dirichlet_outward. field is full
  f with g installed on D; gradient=B field, J=−K gradient, influx=BᵀJ,
  Qf=Q field. dirichlet_outward is in I order, with entry
  sum_a∈D k_ia(field_i−g_a); zero for non-Dirichlet modes.
- components: sorted positive-conductance connected components, each with
  increasing labels; order components by smallest label. kernel_basis is
  their full-node indicator vectors, kernel_images their Q products.
- reconstruction: exactly mu_normalized,k_normalized,detailed_balance,
  mu_residual,k_residual. Recover mu_normalized using only Q ratios along
  positive edges, anchoring each component's smallest label to 1. Recover
  k_normalized in input edge order as mu_normalized_tail Q_tail,head.
  detailed_balance_ij=mu_normalized_i Qij−mu_normalized_j Qji. mu_residual
  compares recovery with supplied mu_i/mu_anchor. k_residual compares each
  edge with supplied k_e/mu_anchor_of_tail (zero edges still yield zero even
  across components). Reconstruct first; supplied mu only verifies residuals.
- reduced: exactly nodes,W,Q,adjoint_residual,m0,m1,m2,Q1,Qx,Qx2,source,fdot,
  constant_balance,components,anchored,kernel_basis,kernel_images,invertible.
  nodes is I. W,Q are principal blocks in I order. Moments and actions use
  x restricted to I; retain nonzero m0. adjoint_residual=W_I Q_I−Q_IᵀW_I.
  source_i=sum_a∈D Q_ia g_a−q_i/mu_i; fdot=Q_I f+source.
  constant_balance_i=sum_j∈I Qij+sum_a∈D Qia−q_i/mu_i uses interior AND held
  values equal to 1 while retaining prescribed q. It is not Q_I1 alone.
  components are positive-edge components of the induced I graph, sorted
  by full label; anchored has one bool per component, true iff it has a
  positive edge to D. kernel_basis contains indicators of UNANCHORED
  components in I-coordinate order; kernel_images are their Q_I actions.
  invertible is true iff there are no unanchored components.
- balances: exactly mass,energy,mass_rate,energy_rate,mass_rhs,energy_rhs,
  internal_dissipation,external_work,reservoir_work,ordinary_rate.
  mass=sum_i∈I mu_i f_i; energy=½sum_i∈I mu_i f_i²;
  mass_rate=sum_i∈I mu_i fdot_i; energy_rate=sum_i∈I mu_i f_i fdot_i;
  ordinary_rate=sum_i∈I fdot_i. internal_dissipation sums k_ij(fi−fj)²
  over edges entirely in I, once each. external_work=sum_i∈I fi q_i;
  reservoir_work=sum_i∈I fi dirichlet_outward_i.
  mass_rhs=−sum_i∈I q_i−sum_i∈I dirichlet_outward_i;
  energy_rhs=−internal_dissipation−external_work−reservoir_work.

The adjoint residual also checks the formal weighted quantum norm-derivative
identity; no matrix exponential, sampled quantum evolution or spectral solver
is required. The full Q has constant modes and is not a causal nilpotent A.

## Exact analyze schema and proof controls

analyze() has no arguments, I/O or caches. Its exact top-level keys are
schema,rows,witnesses; schema is qr05-measure-divergence-report-v1. Each row
adds id,base,variant to evaluate's exact output, with id=base+':'+variant.
witnesses has nine records in base order, each exactly base,rows,Q,measures,
conductances. rows=[base+':identity',base+':rescale']; Q is their common full
matrix, measures and conductances each contain the two differing-scale input
vectors. Measures must differ even for the singleton; zero conductances may
agree. Inputs/target measures are verifier data, not part of the Q channel.

Tests must reconstruct the full report from an independent analytical base-Q
table, not merely compare engines. Check the nine derivative rows and actual
moments from the prior design, full and reduced identities, all transformation
laws including transported boundary order and anchor renormalization, kernel
and grounding conditions, all native validation/refusal boundaries and lack
of input/output aliasing. Under a changed component anchor, both normalized
mu and normalized k must be renormalized, not simply permuted.

Named API/proof controls outside the 36-row census are exactly the prior
design's closed unit triangle (edges 0→1,1→2,2→0; x=(0,1,2), f=(0,1,0)),
arithmetic-face Dirichlet f_I=g=1, and two-node outward q=(1,0), f=(1,2).
The last gives fdot=(0,−1/2), mass_rate=−1, energy_rate=−2. Also test inclusive
128-bit inputs and refusal beyond the bound without an adaptive fixture bank.
Finite bit-bound output may exceed 128 bits and remains valid exact arithmetic.

## Evidence discipline

Freeze NINE sources: this README, protocol.json, primary.py, reference.py,
study.py, test_measure_divergence.py, both preceding design documents and
the literal-SHA-pinned BM evidence utility. RESULTS and verification logs
are publication records, not prospective sources. Existing freezes/captures
must not change. The authenticated BM driver source is loaded for its
evidence-only helpers; its mathematical study functions are never called.
No prior mathematical engine or rejected branch engine is loaded.

Authenticate bounded regular utility bytes before loading; enforce literal
dependency/protocol pins before engine execution. Capture/replay bind all
source identities and freeze bytes, recheck afterward, compare native types
before serialization, exclusively create outputs and read them back. Test
source mutation, malformed metadata/codec, route mismatch, capture tampering,
publication refusals and freeze lifecycle. One cached full analysis per suite.

Limits: 30 seconds per analysis, 60 seconds per suite, 262,144 bytes per source,
16,777,216 per artifact. Sequence: static review/formatting, freeze, first
capture, normal/optimized suites and replays, exactly one Python 3.11 full
replay. Preserve failures and use a named repair revision; never tune frozen
sources after first execution. Later correspondence/noncollapse, uniform
bounds, growth/null calibration and empirical interfaces retain separate
gates. RET/applications, book/clock deferrals and gravity boundaries are unchanged.
