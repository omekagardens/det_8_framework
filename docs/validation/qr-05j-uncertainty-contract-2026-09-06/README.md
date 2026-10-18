# QR-05J — constructive uncertainty-summary contract

Protocol recorded before implementation, 2026-09-06.
Research base: `da75a0ea9cb7e61277004abf698b0d0eb82b3a92`.
That checkpoint and six preceding pending commits were pushed to origin/ret
at the user's request before this gate began. This new gate is isolated
mathematical research: no RET/core imports or edits, dependency installation,
new physical laws, ontological commitment, empirical data or Lean installation.
Prior evidence is immutable.

## Question and acceptance

QR-05I's complete joint count-law polynomial already determines every static
count moment. This gate does not strengthen that full-law prediction claim.
Instead, derive a constructive summary for means and covariances directly
from eligible-support unions of ordered chain pairs, without constructing the
full law in the primary route. Measure which existing summaries preserve it
and whether its supported partition is strictly smaller than the full-law
partition in this bounded universe. No strict compression or partition count
is prescribed. A retained failure is a valid investigative result.

Acceptance: independent exact ordered-pair and full-law-moment routes agree
on the entire native output; all previous source/frame/history identities and
12 candidate partitions match the pinned I artifact; polynomial, covariance,
mixture, PSD and collision controls pass; independent tests, normal/-O runs,
create-only capture, unchanged replay and all source/prior hashes pass.
Proof arguments below are mathematical, not conclusions from finite tests.
No Lean proof or arbitrary-law coverage is claimed.

## Standalone finite mathematics

A supplied finite order has fixed bottom0 and top7. Observation S contains
all fixed vertices and a subset of eligible vertices. A repeat observation U
contains all fixed vertices and independently retains each eligible odd-ID
vertex with rate x and each eligible even-ID vertex with rate y in [0,1].
Parity is named acquisition metadata, not a physical property inferred from
labels. Fixed interior vertices are never randomized or colored.

For q=0..3 let C_q(S) be the set of q-internal-vertex chains between the probes,
counted once per vertex set; C_0 has the single empty internal chain.
Let A* be the eligible support of chain A. Its indicator I_A(U) is one iff
A* is contained in U. Then N_q(U)=sum_{A in C_q} I_A(U), with N_0=1.
Let D[q,o,e] count chains whose eligible supports have o odd and e even
members. If S has O odd and E even eligible vertices,

```text
M_q(x,y) = E N_q = sum_{o,e} D[q,o,e] x^o y^e.
B[q,r,o,e] = # ordered pairs (A,B) in C_q x C_r
              whose eligible union A* union B* has o odd and e even members.
R_qr(x,y) = E[N_q N_r] = sum_{o,e} B[q,r,o,e] x^o y^e.
K_qr(x,y) = Cov(N_q,N_r) = R_qr(x,y) - M_q(x,y) M_r(x,y).
```

The raw moment formula follows by distributing N_q N_r and using
I_A I_B=I_(A* union B*). A shared eligible vertex appears once in the union,
not twice. When q=r, self-pairs occur once and every distinct off-diagonal
pair occurs in both orientations. Sharing fixed vertices alone creates no
random overlap. Disjoint eligible supports give independent chain indicators
under the declared IID law, even if chains share probes or a fixed interior.

B is a nonnegative integer tensor, symmetric in q,r. B[0,r]=D[r].
The sum of all color cells in B[q,r] equals N_q(S)N_r(S). Fixed chains
can contribute constant terms. These relations retain chain multiplicity,
not just a set of distinct eligible supports.

### Polynomial degrees and equality

The eligible-union raw moment has bidegree at most (O,E), at most (3,3)
here, and total degree at most q+r. Its table is padded4x4.
Mean products can have bidegree up to (6,6), with total degree at most
q+r<=6; covariance tables must be padded7x7. In particular a triple of
odd eligible vertices on a chain has R_33=x^3 but K_33=x^3-x^6.
Truncating K to4x4 would silently change variance.

B is exactly the raw-moment polynomial coefficient tensor. Equality of B
is equivalent to equality of every R_qr on the square: a polynomial zero on
an open rectangle is identically zero. Because B includes D in its q=0 row,
it also is equivalent to equality of the means together with all covariances.
No claim is made that covariance alone determines the means.

Full joint-law equality implies B equality, not conversely in general.
The primary computes B by pair unions; the independent reference reconstructs
the full law from source-chain indicators and exact4x4 tensor interpolation,
then computes R by weighting its count-atom polynomials with z_q z_r.
It never counts chain pairs. Covariance coefficients are then obtained by
full convolution, without interpolating a degree-six object on a four-node grid.
The reference degree-bounded interpolation contract is the explicit I contract,
reproduced locally in the reference route, not an import of earlier executors.

### Positivity and singularity

For every real vector v and every declared finite probability law,

```text
v^T K v = sum_U p(U) [v dot (N(U)-E N)]^2 >= 0.
```

Thus the evaluated covariance matrix is positive semidefinite (PSD), not
necessarily positive definite. Its q=0 row and column are identically zero.
This is the standard variance-of-a-linear-combination argument; see the
[University of Iowa STAT7400 notes](https://homepage.stat.uiowa.edu/~luke/classes/STAT7400-2021/_book/numerical-linear-algebra.html#cholesky-factorization).
Signed coefficient matrices need not themselves be PSD; the statement concerns
evaluations on the domain. No Gaussian distribution, matrix inversion,
regularization, eigenvalue tolerance or covariance fitting is introduced.
For raw chain counts under this IID law, each pair covariance contribution
is nonnegative: the survival monomial of a union is at least the product
of the two support-survival monomials on the closed square. This does not
require all covariance coefficients to be nonnegative.

For any fixed linear coefficients alpha_q, the corresponding transformed
count vector has covariance alpha_q alpha_r K_qr; any scalar combination
has variance computed by the quadratic form. This is a prediction from a
supplied law, not a calibrated error bar for unknown data.

### Correlated block mixture

Keep the H policy menu for evaluated diagnostics: iid_half=(1/2,1/2),
iid_color=(1/3,2/3), and block_coin, one fair shared coin for each eligible
parity block, with independent coins across blocks. Empty blocks coalesce.
For block_coin, let z_c be the deterministic count vector at each corner
c in {(0,0),(1,0),(0,1),(1,1)}. Then

```text
m_block = (sum_c z_c)/4
R_block = (sum_c z_c z_c^T)/4
K_block = R_block - m_block m_block^T
        = (sum_c (z_c-m_block)(z_c-m_block)^T)/4.
```

Equivalently average the corner raw moments and then center. Averaging the
corner covariances alone gives zero and omits between-corner variation.
The general mixture identity follows by adding/subtracting conditional mean
products in E[NN^T]-E[N]E[N]^T; here the within-corner term is zero.
This block law is not evaluation at the IID half-rate point.
All four corners have zero conditional covariance, but noncorner boundary
edges need not: a color may remain random on an edge.

### Explicit general-limit diagnostic

On abstract count vectors (1,n,0,0), compare these constant probability laws:
A gives n=0,2 masses1/2,1/2; B gives n=0,1,3 masses1/3,1/2,1/6.
Both have E N1=1, E N1^2=2 and Var N1=1, and the same complete four-vector
first and second moments. Their laws differ and E N1^3 is4 versus5.
They are valid abstract distributions, NOT claimed to be induced-order IID
laws in this gate. Retain this diagnostic regardless of any bounded
second-moment/full-law partition coincidence.

## Frozen source and history universe

Exactly the I universe: IDs0..7, density metadata12, bottom0 below and top7
above all interiors. Write a_i=i+1,b_j=j+4 for i,j=0..2.
ferrers6 has a_i<b_j iff i<=j; standard_example3 iff i!=j;
chain6 is the total order. ferrers6_fixed uses the Ferrers relation but fixes
[0,3,7]. All other profiles fix [0,7]. Eligible vertices are increasing IDs
1..6 excluding fixed interiors. Source relations are transitively closed.

Cases in this order:
ferrers6/independent, ferrers6/parity_adaptive, ferrers6/common_coin,
ferrers6/parity_hole, ferrers6/first_pair, standard_example3/independent,
chain6/parity_adaptive, chain6/parity_hole, chain6/first_pair,
ferrers6_fixed/independent.

Mask bitj means eligible[j]. S runs in increasing numeric order. The first
law is uniform over all masks, except first_pair uniform over size-two masks
and zero elsewhere. For current final mask T subset S, independent/first_pair
uses independent rate1/2, parity_adaptive uses1/3 for even|S| and2/3 for odd,
parity_hole uses1 for even|S| and0 for odd, common_coin uses fair all/none.
At empty S the common-coin outcomes coalesce. The current token is that rate,
or1/2 for common_coin. Diagnostic conditional laws remain defined at zero
first-probability states.

Retain608 states (510 first-positive),6,804 histories (3,534 positive joint,
3,270 zero joint), and6,804 potential repeat observations(case,S,U).
History IDs follow case,S,T ascending full enumeration including zeros.
Only positive joint histories form predictive partitions. No(S,T,U) expansion.
Each per-case mass sums to1; pooled class masses sum to10, not a source prior.

The public base is [context,T kept,T local past], where
context=[current design,"12",fixed IDs,eligible IDs]. Hidden source/profile
names are audit metadata, never key fields. Local past entries index sorted
kept IDs, while source past uses original IDs.

## Summaries and target partitions

Retain all12 I/H candidates in their original order and with exactly their
original keys/classes: final_only,policy_token,tagged_policy,counts_policy,
graded_policy,tagged_graded,unmarked_order,marked_order,full_record,
color_graded,block_order,color_order. Their suffixes appended to public base
are respectively [],[r],[r,tag],[r,N(S)],[r,C],[r,C,tag],[r,unmarked],
[r,marked],[S kept,S past],[r,D],[r,block],[r,color].
tag is whether eligible[0] is in S and C[q,k]=sum_{o+e=k}D[q,o,e].

The order codes anchor fixed vertices individually in increasing order then
permute remaining vertices. Relation code sums2^(i*n+j) over v_i<v_j in the
order. Unmarked code anchors only0,7, deliberately forgetting fixed interior
marks. Plain code is[n,min relation]. Colored code minimizes(relation,color)
lexicographically, color=sum2^i over eligible odd positions, output[n,relation,color].
Anonymous block decoration sums2^(i*n+j) over i<j of equal eligible parity;
block names may exchange. Fixed vertices are never color/block decorated.

Append a13th candidate pair_graded with suffix[r,B]. It is an explicit
pair-union summary, not a claim of minimal bytes. Two targets, in order:
analytic_means signature=D (the retained mean_polynomials);
analytic_second signature=B. Targets refine the public base.
B's q=0 row recovers D, hence|S| from q=1 and the current token from the
public design. Therefore pair_graded and analytic_second should have the
same members. Verify this structurally expected equality rather than assume it.

Retain all13x13 candidate and2x2 target refinement booleans,26 assessments,
first positive-occurrence class IDs, sorted member IDs, reduced rational
class masses, and first failed-fiber collisions against the first class
representative in ascending history order. Row A,column B means A finer.
Compare both targets with I's analytic_means and analytic_counts in both
directions by actual member maps, retaining collision witnesses and common
refinement sizes. Do not infer any equality from class counts alone.

## Executor interface and exact schema

analyze(problem) accepts only the exact native dict
{"schema_version":"det8-qr05j-problem-v1","family":"qr05i_chain_pairs"}.
Reject unknown keys/values, native-type substitutions and subclasses normally
and with-O. Standard library only. Executors do no file I/O, do not import
one another or any earlier executor, and do not consume captured artifacts.

Use I's complete analysis schema, case metadata, and history fields.
Candidate maps gain pair_graded; target maps are analytic_means,analytic_second.
State fields retain all I fields EXCEPT count_polynomials, which is removed.
Retain mean_polynomials and color_sizes. Add exactly:

```text
pair_graded: B[q][r][o][e]              # 4x4x4x4 native nonnegative integers
covariance_polynomials: K[q][r][i][j]  # 4x4x7x7 native signed integers
predictions: {
  iid_half: {
    count_mean: [4 Fraction strings],
    count_second_moment: [4x4 Fraction strings],
    count_covariance: [4x4 Fraction strings],
    coefficient_mean: [4 Fraction strings],
    coefficient_covariance: [4x4 Fraction strings]
  },
  iid_color: {same fields},
  block_coin: {same fields}
}
```

The fixed coefficient scaling is alpha_q=(-1)^q/(2^(q+1)*12^q),
applied to the count vector componentwise. Do not treat this scaling as a
new propagation experiment or promote the density metadata to measured units.
The analytic_second signature is pair_graded directly; do not duplicate B
under another state field or retain full-law polynomials in the primary output.

Analysis counts have exactly14 fields:
cases,states,positive_states,observations,histories,positive_histories,
zero_histories,candidates,targets,pair_instances,pair_coefficient_cells,
covariance_coefficient_cells,mean_coefficient_cells,predictions.
pair_instances is sum_states sum_q,r N_q(S)N_r(S), including q0 and self-pairs.
Coefficient cell totals are256,784,64 per state respectively; predictions3
per state. All native dict/list with native string keys; no float, tuple,
Fraction objects or implicit bool/int coercion in retained math.
All rationals are reduced strings, including"0" and"1"; exact component cap4096bits.
Zero-history class IDs stay null.

## Runner checks and controls

The runner independently verifies B[0,r]=D[r], symmetry, sums, exact mean
convolution into all49 covariance cells, degree bounds, constant covariance
row/column zero, and evaluated moments against direct subset outcomes.
Use I's22 distinct rational audit points: the16 points on
{0,1/3,2/3,1}²; (1/2,1/2); and held-out(2/5,3/7),(1/5,4/5),
(1/2,1/3),(0,2/5),(3/7,1). The colorIIDpoint is already in the16 grid.
These evaluations cross-check; coefficient identities and finite-law arguments
establish the mathematical contract, not a degree-six interpolation assumption.

Audit each evaluated count covariance and each block covariance for PSD using
exact nonnegative principal minors of the q1..3 submatrix (all7 nonempty
principal subsets), together with symmetry and the exact zero q0 row/column.
Singular matrices are valid. Also verify fixed coefficient transformations.
Cross-check all three policy predictions using the supplied labeled laws,
not an inferred law from moments. Compare all B coefficients with raw moments
of the pinned I count-polynomial coefficients. Pin all14 earlier artifacts;
compare relevant I source/state/observation/history and all12 candidate identities.

Retain these controls, all at positive current histories with final mask0:
case0 odd singleton mask1; two odd antichain mask5; star57/path27; shared-root
star mask41={1,4,6}; fixed case9 mask0 and mask16={6}; case6 chain6 mask21
={1,3,5} and42={2,4,6}. Controls respectively test self-pairs, ordered cross-pair
multiplicity, equal-mean unequal-covariance structure, shared eligible root,
fixed versus sampled overlap and the degree-six covariance cells.
Retain the block-mixture nonzero variance despite zero corner covariances,
the nonzero boundary-edge variance in case0mask41 at(0,1/2), and the
abstract equal-first/second-moments but unequal-law diagnostic above.

## Evidence lifecycle and limitations

Freeze README,uncertainty.py,reference_qr05j.py,study.py,test_qr05j.py and
test_capture.py by exact byte/hash ledger only after tests/review/formatting.
Use isolated Python and fresh external bytecode caches. Capture results.json
once with exclusive creation, canonical exact JSON and readback; replay must
preserve bytes and compare the whole suite. Verify sources/priors before and
after every capture/replay. Lifecycle tests mutate temporary stub evidence only.
Runtime floats are descriptive metadata outside the exact-math suite.
RESULTS.md and the roadmap are reports outside the frozen source ledger.

No empirical covariance calibration, unknown acquisition law, Gaussian model,
performance improvement, recursive closure, quantum channel, metric, gravity,
continuum limit or universal moment sufficiency is established here.
Later dynamic closure needs a declared transition/access contract. A physical
bridge still requires measured observables, units and an acquisition model.
