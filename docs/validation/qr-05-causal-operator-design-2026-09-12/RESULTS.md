# Finite causal operators: analytical decision record

12 September 2026. **The design gate is complete.** The
[standalone contract](README.md) proves the exact inverse/path relation,
separates direct support from reachability, and gives explicit information-
loss witnesses. This gate ran no mathematical executor, unit-test suite,
fixture enumeration, simulation or apparatus study. The proposed 52-row
verification is the next gate, not a result already obtained.

## Main constructive result

For a finite strict order, use receiving rows: C_ij=1 when j≺i. Let A be any
signed rational matrix supported on C and d>0. With M=dI−A,

```text
G=M^(-1)=sum(k=0,...,n−1) A^k/d^(k+1),
TC(nonzero off-diagonal G)=TC(nonzero A).
```

The inverse exists because A is nilpotent. The first identity is a finite
telescoping sum, not a convergence approximation. The second follows by
expanding both G in A and A in G−I/d.

On each cover relation, G_ij=A_ij/d². Therefore the directed transitive
closure of G's nonzero entries equals the entire supplied order **if and
only if every cover weight is nonzero**. Signs are allowed. This is the
useful refinement beyond the branch audit: cancellation may erase an
individual noncover entry without destroying recoverable reachability.

It is not information creation. A's support already carries that same
reachability. Nor can observing G establish that an unknown latent order has
no extra zero-weight relations; the nonzero-cover condition restricts the
admitted world class.

## Three distinctions now resolved analytically

1. **Causal containment versus pointwise equality.** An inverse entry can be
   nonzero only on an allowed directed relation, but not every allowed entry
   must survive. Entrywise A≥0 plus positive weights on every cover gives
   the stronger exact support/sign theorem. Positive covers by themselves
   do not suffice when negative noncover weights remain allowed.

2. **Matrix recovery versus latent-order recovery.** Full G in a specified
   basis and normalization gives d from its diagonal and A from its inverse.
   The three-chain and an order with one edge plus an isolated event can
   nevertheless give the same full G when the chain assigns a cover zero
   weight. Recovering A does not automatically recover such invisible
   relations.

3. **Directed response versus antisymmetric response.** Even with every
   cover nonzero, signed weights permit a fork and a nonisomorphic chain
   to give identical Δ=G−G^T. Full G distinguishes them. Δ alone, or a common
   deterministic function of Δ, does not. A supplied compatible topological
   ordering changes this information question and must be declared, not
   silently assumed.

The signs are fixed consistently: positive Δ_ij means j≺i on the restricted
nonnegative class. The old audited toy uses the opposite whole inverse sign,
so the new contract records M=−H and G=−H^(-1) explicitly.

## Exact negative controls retained

The three-chain toy has A_10=A_21=3, A_20=−3 and d=a. Its endpoint response
is −3/a²+9/a³. It cancels exactly at a=3; at a=5 it has the opposite sign
from the adjacent responses. Both examples retain full chain reachability.

A signed diamond cancels two cover-path contributions without using a
noncover edge. A two-event pair isolates loss of orientation from Δ; the
fork/chain pair strengthens this to genuinely different unlabelled order
types. These are mathematical counterexamples, not noise or setup defects.

The operator retains its actual finite toy name. No sourced physical wave
operator, quantum state, gravitational dynamics or continuum correspondence
has been selected or repaired by these identities.

## Why this helps the QR/Track-B program

The contract provides a way to distinguish three causes of a zero response:
no directed path, a zero coupling, or cancellation among signed paths. It
also states when an ideal full response preserves enough information to
recover a directed order. These distinctions can guide future response and
graph diagnostics, but no noisy measurement or application has been validated.

A chosen operator built only from existing O,P,T observations cannot split
their previously verified four-world geometric collision. Introducing a
metric factor, proper-volume measure or physical amplitude normalization
adds model/reference input. It is not information recovered from the same
records. Likewise, the previous O channel supplies two probe comparisons,
not the arbitrary full causal matrix used as an input in this design.

Ordinary transpose is an algebraic convention here. A physical inner product,
measure, advanced/retarded interpretation, boundary conditions, operator
coefficients and stable inversion require separate contracts. Exact nonzero
support supplies no uniform noise-detection margin.

## Prospective next gate

One bounded exact verification will cover 13 named base cases, each with
identity, cyclic relabeling, order reversal and joint positive rescaling:
52 labelled rows, with duplicate symmetric cases deliberately retained.
The expected census is 452 cells per reported matrix and 304 full path
records, including trivial paths and zero-weight contributions.

Expected direct-support equality holds in 36 rows; reachability equality in
48. These are analytically derived expectations, not numerical observations.
The distinction prevents a single generic success flag from hiding a false
stronger claim. All same-G/same-Δ witness pairs retain their different target
orders explicitly.

Independent finite-power and exact-elimination/path routes must compare
full native rational matrices, powers, both inverse products, all path
contributions, covers, support masks, closures and failure witnesses.
Input validation must accept arbitrary labels while rejecting nontransitive
relations, forbidden weights and malformed native types. Freeze the complete
protocol and sources before first execution; retain any failure without
tuning the frozen sources. No branch geometry engine is transplanted.

Physical operator selection, actual divergence-operator moments,
correspondence-distance/noncollapse, justified uniform bounds, stochastic
growth/null calibration and empirical interfaces remain subsequent separate
work. RET integration and materials/anomaly application readiness are not
promoted. Book work remains archival; deferred clocks and retired couplings
are not reopened.

## Review and checkout boundary

Independent analytical reviews checked the nilpotent inverse, all-path and
reachability proofs, the positive-support condition, exact sign mapping,
full-G versus Δ ambiguities, all fixed fixtures and their prospective census.
The stronger signed reachability result and the nonisomorphic fork/chain
witness were incorporated during design, before any executable study.

Final metadata-only checks matched all ten joint-geometry, six reconciliation
and 12 BV frozen source identities and their captures' source/freeze bindings.
No study module was imported or replayed for these checks. All 104 checked
local Markdown links resolve and the tracked diff passes whitespace checks.
All 234 preexisting status entries remain present, including the 231 unrelated
entries; only the new design directory was added to the status inventory.

The authoritative branch remains `ret`; the last published checkpoint is
`47262b616296c632189d4e8b3e2582ed2016a6d8`. This design, the preceding
joint-geometry work and the roadmap update remain local and uncommitted.
No commit, push, dependency installation, core/RET edit or `temp_qr.md` edit
was made in this gate. Earlier frozen mathematics remains unchanged.
