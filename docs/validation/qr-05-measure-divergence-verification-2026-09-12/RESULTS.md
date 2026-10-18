# Measure/divergence verification: exact results and decision

12 September 2026 (Pacific/Honolulu). **This bounded verification gate is
complete.** The first capture passed without source repair. Independent
incidence-matrix and neighbor-exchange implementations agree on all 36 fixed
rows. All 30 tests pass in both normal and optimized modes. Three complete
replays, including exactly one Python 3.11 replay, match the first capture.

The [executable contract](README.md) implements the
[prior analytical design](../qr-05-measure-divergence-design-2026-09-12/README.md).
This is supplied finite mathematics, not physical measure acquisition,
Hamiltonian selection, a continuum theorem, gravitational dynamics or
RET/application readiness.

## What was verified

| Retained quantity | Verified total |
|---|---:|
| Base cases / labelled variant rows | 9 / 36 |
| Full-node occurrences / edge occurrences | 92 / 56 |
| Cells per full square node matrix | 252 |
| Dynamic-node occurrences / effective matrix cells | 72 / 168 |
| Same-Q, different-measure scale witnesses | 9 |
| Mathematical/API tests per mode | 20 |
| Evidence-integrity tests per mode | 10 |

Each row retains the supplied graph, measures, conductances, coordinate marks,
field and boundary data; incidence and operator matrices; actual full and
reduced moments; edge fluxes; weighted and ordinary balances; component
kernels; reconstructed relative measures; and full affine boundary equations.
The four variants are identity, cyclic relabeling, edge-orientation reversal
and joint scaling of measure/conductance/outward flux. Symmetric duplicates
are retained, not counted as independent statistical trials.

The independent test oracle begins with an explicit analytical base-Q table
and reconstructs the entire native report. It does not merely accept agreement
between two engines. A separate exact-elimination rank check verifies the
reported full and reduced kernel dimensions and invertibility flags. Native
Fraction/int/bool distinctions are preserved before serialization.

## Constructive identities and boundary counterexamples

For Q=−W⁻¹BᵀKB, every full row satisfies the declared identities

```text
Q1=0,       1ᵀWQ=0,       WQ=QᵀW,
⟨u,Qv⟩_W=−(Bu)*K(Bv).
```

The tests compare the full weighted energy form with the edgewise outer-
product sum, not a guessed coefficient. The two-node unequal-measure case
has weighted mass derivative zero while the ordinary sum changes at 1/2.
The zero-conductance edge remains in the report but does not connect positive-
weight components or carry flux.

Boundary outcomes are deliberately different:

- Closed diffusion conserves weighted mass and dissipates weighted energy.
- Prescribed outward q=(2,−2) on the unequal-measure pair has zero net mass
  change but energy derivative +1. Constant annihilation by homogeneous Q
  is not stationarity under the full prescribed forcing.
- Grounded arithmetic-face Dirichlet data give mass and energy derivatives
  −5/2. The driven case gives mass derivative 5/4 and energy derivative 5/8.
  Reservoir exchange is not hidden behind a closed-system conservation flag.
- The unanchored Dirichlet block is diag(−1/2,0). Its isolated interior mode
  survives; Dirichlet naming alone does not imply invertibility.

The three named controls outside the 36-row census also pass: a closed unit
triangle, consistent nonzero constant interior/reservoir data, and prescribed
net outward q=(1,0). The last gives fdot=(0,−1/2), mass derivative −1 and
energy derivative −2. This checks nonzero net mass loss as well as the study's
zero-net-flux energy-increase example.

## The audited moment error is now repaired and tested

The actual arithmetic-face operator on the open three-node path gives

```text
m1 = (3/2,−1/2,−1),      m2 = (3/4,5/4,1/2).
```

m2 is the HALF-second moment. In particular the center coefficient is 5/4,
not the profile value 1, and its first moment is −1/2, not zero. The differently
weighted pointwise operator instead has center moments (0,1). It conserves
its reciprocal-profile weighted mass, not the original counting-measure sum.
The two supplied measure/operator pairs remain distinct.

Full and reduced Q1,Qx,Qx² actions are checked against their actual row moments
and an independent quadratic probe. The reduced Dirichlet block retains its
nonzero zeroth moment and separate boundary source. No periodic local-offset
calculation is silently substituted for a global coordinate difference.
These checks repair the finite implication identified in the
[CR audit](../qr-05-bridge-reconciliation-2026-09-12/AUDIT_GEOMETRY.md);
they do not modify the historical branch or prove continuum convergence.

## Relative-measure information survives; absolute scale does not

Both implementations recover component-relative measure using Q ratios
before comparing it against supplied μ. All detailed-balance and supplied-
input residuals vanish. The tests check μ_j/μ_i=Q_ij/Q_ji on positive edges,
component anchors and conductance reconstruction. Under relabeling, changed
smallest-label anchors correctly renormalize BOTH measure and conductance.

All nine identity/rescale pairs have identical full Q and different positive
measures. Full affine dynamics also agree because prescribed outward q is
scaled with μ and k; held Dirichlet values remain fixed while reservoir
fluxes scale. Thus relative measure can be identified within the admitted
reversible class, but an absolute reference per positive-edge component is
still needed. The general proof is analytical; this bounded report verifies
its specified witnesses, not stable inversion under arbitrary measurement noise.

The weighted-adjoint matrix identity also supports the design's conditional
QM connection: IF H=−Q and iψdot=Hψ are chosen, the weighted norm is preserved.
No time evolution or matrix exponential was simulated here, and no physical
Hamiltonian or measurement instrument was selected. A full reversible graph
operator is additional information, not already supplied by the old O,P,T
channels. Computing a common function of those old channels cannot remove
their retained geometric ambiguity.

## API, evidence and source identities

The 20 mathematical/API tests cover complete native reports, all fixture and
transformation identities, actual moments, boundary balances, exact kernel
rank, invalid native types/shapes, invalid edges/partitions, signed field
values, nonpositive measure, negative conductance, inclusive 128-bit rational
inputs and refusal beyond that bound. Valid exact outputs may exceed the
input bit bound. Shared valid input containers are accepted and copied;
fresh outputs do not alias caller inputs or later calls.

The ten evidence tests cover authenticated helper loading, nine-source pins,
strict native codec/JSON, freeze schema/runtime/canonical refusals, exclusive
publication, readback, changed source/freeze inputs, capture tampering and
route mismatches. Temporary synthetic corruption tests do not change any
retained source, freeze or capture. The authenticated BM driver supplies
evidence helpers only; its mathematical study is not executed.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Canonical mathematical report | 154,123 | `c9662f57a99b137a5ae5da67c5c2cff6f2f76e37db4d5361e47164a90820e1b0` |
| Source freeze | 1,243 | `621705217af3aa9ee547b8a0e7e533f1afbf9076ec0fe7bc9fbda2f18c999cce` |
| Complete capture | 155,377 | `f6b20794672b26bedef6b033fe13e6cba537a4fedfa4ed497fede319efabced0` |

Normal and optimized suites completed in 0.433 and 0.435 seconds respectively.
All three replays match the report hash above. The retained
[verification log](verification.json) records commands and outputs;
[source-freeze.json](source-freeze.json) and [results.json](results.json)
bind the prospective bytes to the captured report. No prospective source
was edited after first execution, and no extra alternate-runtime replay
or adaptive fixture search was performed.

Final metadata-only review matches all 46 source bindings across this and
the four preceding bundles, with all five capture/freeze bindings unchanged.
The new directory has exactly the ten expected files, including hidden/
ignored inventory; all 108 local Markdown file targets in the new bundle,
preceding design and roadmap resolve. These checks import no study module.

## Next gate and publication boundary

**Next: correspondence-distance and noncollapse contract, design-only.**
Define the actual directed-separation comparison and normalization before
another geometry simulation. Separate unrestricted correspondences from
bijections, supremum distortion from trimmed summaries, and all-pair
max-plus closure from the invalid link-only characterization. Retain the
audited three-chain counterexample and scale-collapse/normalization controls.
Finite diagnostic trends are not uniform convergence theorems.

Stochastic growth/null calibration, justified uniform bounds, acquired
measure/response calibration and physical operator selection remain separate
later work. RET integration and materials/anomaly applications are not
promoted. Book work remains archival; clocks and retired couplings stay
deferred. No new dependencies or `temp_qr.md` edits were made.

Publication is scoped to this ten-file verification bundle, its two-file
preceding design and the research-roadmap update. The prior published head
is `a0326139dbe1a026392738b3c1397eced48ec66c`; the remote matched it before
publication work. The 231 unrelated core/RET/application status entries are
excluded. Historical uncommitted-state statements in source-bound design
records retain their original checkpoint meaning; publishing those bytes
does not authorize changing them. Commit and remote-head confirmation are
reported at publication, not inserted into their own hashed source inputs.
