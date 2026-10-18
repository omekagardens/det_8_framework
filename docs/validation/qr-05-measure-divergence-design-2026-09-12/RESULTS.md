# Supplied measure and divergence: analytical decision

12 September 2026 (Pacific/Honolulu). **The design gate is complete.** The
[standalone contract](README.md) derives weighted conservation and adjoints,
separates three boundary models, and computes the moments of the actual
chosen finite operator. No new mathematical executor, fixture enumeration,
test suite, quantum simulation or acquisition was run for this design.
The 36-row exact verification is prospective, not already passed.

## Constructive result and exact correction

For a supplied undirected graph, incidence B, positive node measure W and
nonnegative edge conductance K, set Q=−W⁻¹BᵀKB. Then

```text
Q1=0,        1ᵀWQ=0,        WQ=QᵀW,
⟨u,Qv⟩_W=−(Bu)*K(Bv).
```

This gives a reusable conservation/energy contract and a componentwise
kernel description. Ordinary counting mass is not generally conserved.
Closed diffusion dissipates weighted energy; prescribed exterior flux and
held reservoirs have explicit affine balance terms. A grounded reservoir
can lose mass, driven boundary data can increase energy, and an unanchored
interior component keeps a zero mode. These are separate expected outcomes,
not exceptions hidden behind one success flag.

The arithmetic-face divergence stencil has half-second moment
(2η_i+η_{i+1}+η_{i−1})/4, not exactly η_i. Its first moment is
(η_{i+1}−η_{i−1})/(2h). The open three-node regression with η=(2,1,1)
gives center moments (−1/2,5/4), while pointwise multiplication would give
(0,1). This analytically repairs the audited CR coefficient implication;
it does not rewrite the historical branch or establish a continuum limit.
Global coordinate identities are kept separate from periodic local offsets,
and reduced Dirichlet blocks retain their nonzero zeroth moments.

The conservation comparison is also sharpened: pointwise η_iΔ can conserve
the reciprocal-profile measure W=diag(1/η_i), even when it fails counting-
measure conservation. The chosen measure/operator pair must be declared;
one cannot silently switch it to rescue the earlier comparison.

## A useful identification boundary

Full Q, in a supplied node basis and within this reversible class, determines
relative measures by μ_j/μ_i=Q_ij/Q_ji along positive edges. One positive
reference value per connected component then determines W and K. Without
those references, independent common scaling of W,K in each component leaves
Q unchanged. Zero-weight graph edges are also invisible if graph support is
unknown. This is exact identification up to component scales, not a claim
that full Q contains no relative-measure information or a noise-stable inverse.

This result supplies a concrete future question: can an independently
calibrated response channel provide the requisite reversible operator and
normalization? The old O,P,T records do not already contain that additional
channel. A common operator computed solely from those records retains their
verified geometric ambiguity. Supplied weights or coordinates are not newly
measured geometry.

There is also a clean QM-compatible option. H=−Q is self-adjoint in the
W inner product; IF iψdot=Hψ is chosen, ψ*Wψ is conserved. Choosing diffusion
fdot=Qf instead dissipates that norm. Neither evolution follows from the
static matrix alone. This is an algebraic interface for future model checks,
not a selected physical Hamiltonian, an ontology argument or a gravity law.
The earlier strict-poset/nilpotent inverse theorem does not apply to this
bidirectional, singular full graph generator. Reduced Dirichlet blocks may
be invertible under the stated attachment condition.

## Bounded next gate

The fixed plan has nine bases and four separate variants: identity, cyclic
relabeling, edge-orientation reversal and joint measure/conductance/outward-
flux scaling by 3/2. It includes unequal measures, a singleton, a zero edge,
the actual arithmetic-face coefficient, the differently weighted pointwise
operator, prescribed flux, grounded/driven reservoirs and an unanchored
interior component. The prospective census is 36 rows, 92 full-node and
56 edge occurrences, 252 full square matrix cells, 72 dynamic-node occurrences
and 168 effective matrix cells. These are analytical counts, not observations.

Independent incidence-matrix and neighbor-flux constructions must agree on
full rational matrices, moments, component modes, boundary reductions,
mass/energy balances and identification/scaling witnesses. Named triangle,
consistent-constant and nonzero-net-flux API/proof controls are separate from
the 36-row census. Freeze the full protocol and sources before first execution;
no new study was launched while drafting this contract.

After verification, correspondence-distance/noncollapse and uniform-bound/
growth-null repairs retain separate gates. Actual metrology, noisy response
inversion, physical operator selection and empirical correspondence remain
open. No RET/application or gravitational-dynamics readiness is promoted.
Book work is archival; clocks and retired couplings remain deferred.

## Publication checkpoint and evidence separation

Before this design began, the completed joint-geometry and causal-operator
design/verification bundles plus their research-roadmap update were committed
and pushed to `origin/ret` as
`a0326139dbe1a026392738b3c1397eced48ec66c`
(`Verify joint geometry and signed causal-operator calculus`). The 25 staged
paths were checked explicitly; the 231 unrelated dirty core/RET/application
status entries were excluded. A direct remote-head check matched the full
commit hash. No wholesale branch merge or core/RET promotion was performed.

Publication preflight reran the ALREADY EXISTING normal suites and captures:

| Existing bundle | Normal suite | Exact full replay |
|---|---:|---|
| Joint geometry | 23 tests pass, 0.914 s | 64 worlds / 32 menus; original report unchanged |
| Causal operator | 27 tests pass, 0.522 s | 52 rows / 304 paths; original report unchanged |

Commands were `python3 -B` applied respectively to `test_joint_geometry.py`
and `test_causal_operator.py`, and each bundle's `study.py --replay results.json`
with explicit repository-relative paths. The joint report remains 310,259
bytes, SHA-256 `3fbbba9716e5d64cdeb18b04d973e4393533e088a6f62f108a26a62eb54d2a61`;
the causal report remains 165,114 bytes,
`1fdeebb292c84bd8a4617f9515082a8b06b199f1c87ff4816f75b65de36d9bca`.
These 50 passing preflight tests are not a new measure/divergence suite or an
additional alternate-runtime replay. Earlier frozen reports remain unchanged.

Prepublication metadata checks matched all 37 source bindings across the
causal, joint-geometry, reconciliation and BV bundles, plus their capture/
freeze bindings. The staged diff passed whitespace checks. Historical prose
inside frozen designs records their then-uncommitted state and is preserved;
this publication checkpoint supersedes it without changing frozen bytes.

Independent analytical reviews checked the weighted identities, actual
moments, boundary signs, relative-measure theorem and prospective controls.
They prompted explicit componentwise scale freedom, the pointwise reciprocal-
measure clarification, and full-versus-reduced boundary moments. No new
dependency, physical acquisition, core/RET edit or `temp_qr.md` edit was made.
This new design and its roadmap update remain local and uncommitted after
the requested publication checkpoint.

Final metadata-only checks again matched all 37 frozen source bindings and
the four capture/freeze identities; no mathematical module was imported.
All 99 checked local Markdown links in the new documents and roadmap resolve.
The new directory contains only README and RESULTS; the tracked whitespace
check passes and the index is empty. All 231 preexisting status entries are
still present, with only this design directory and the roadmap update added.
