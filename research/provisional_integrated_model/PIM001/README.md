# PIM001 finite integrated baseline

This Python standard-library research model integrates the registered native
growth probabilities, immutable marks, prepared classical incidence counters,
chronological Gaussian attachment, and D/Y/cover-link readouts. Its finite
enumeration reproduces the specified accepted results. The full endpoint field
state **fails schedule independence**, as the named swap explicitly demonstrates.
Option B and Status M remain unchanged.

## Run

From this directory, using Python 3.10 or later:

```sh
python3 -B runnable_model.py
python3 -B -m unittest -v test_model.py
python3 -B runnable_model.py --histories
```

The first command prints an exact JSON summary. The last prints all 120 marked
histories, including order, marks, counters, probabilities, D/Y, field matrices
and the cover-link mean. Fractions are strings, including integers such as `"1"`;
no floating-point approximations or sampling are used. Output goes to stdout.
`-B` prevents Python cache files.

## Finite domain and interfaces

`prepare(i)` conditions on `a<b`, marks `(i,0)`, counters `(1,0)`, with mass one,
for `i=0,1`. It does not multiply in the earlier probability of that preparation.
Exactly two further births are admitted. The original full growth law is used
only on this registered restriction; no other prefix or fifth-birth transition
is supplied. There are 15 structural sequences and four fair suffix-mark pairs
per preparation, all with positive weight. Every actual labeled ideal is retained;
isomorphic endpoints are never merged or divided by an automorphism count.

`State` is frozen and retains chronological identity handles, the full strict
relation `(source,target)`, immutable marks, counters, structural and marked
history masses, and each suffix birth's actual ideal, bit and structural q.
`actual_ideals(state)` enumerates all eligible downward-closed subsets.
`transition_row(state)` uses the supplied proper-slot prescription and exact full
normalization complement. `step(state, ideal, mark, label)` appends a fresh
maximal vertex, multiplies marked mass by `q/2`, increments each addressed old
counter modulo five, and appends zero. The preparation ensures no wrap here.
Counter data and fields do not feed back into q.

`readouts(state)` returns formal total-chain D and terminal counter-equals-two Y.
Y is not an “ever equalled two” flag. D uses complete order information; the
mathematical joint law is not a claim about a jointly available physical apparatus.
This implements the prepared classical register distribution, not the general
quantum instrument on arbitrary coherent inputs or references.

`attach_field(state, endpoint_labels=None)` applies the fixed three-pair formula
in chronological roles before transporting rows to any requested endpoint label
order. Its exact outputs are L, target-first C, K=LJLᵀ, V/β=LLᵀ/2, and the real
and imaginary parts of W/β=(LLᵀ+iK)/2. Thus φ=√β LR and [φᵣ,φₛ]=iβKᵣₛ.
The supplied β>0 remains factored symbolically; β is not a fitted or physically
calibrated unit. The real part of W/β equals the displayed V/β. The three canonical pairs
and their centered Gaussian with quadrature covariance I₆/2 are inherited choices.
These exact matrices characterize that finite field list; the underlying Hilbert
space is infinite dimensional and is not numerically truncated.

`Field.weyl_exponent_over_beta(t)` returns the rational coefficient A in
ω(exp(i t·φ))=exp(βA), for rational real t. `cover_link_mean(state, field=None)`
returns the mean of Σ_covers(φᵥ−φᵤ)²/(2β). Covers are computed from the actual
strict order, omitting transitive non-covers. `named_swap()` supplies the accepted
u/v witness with both original masses; it does not replace the full ensemble.
Birth order is implementation bookkeeping, never a physical global present.

## Results and checks

| Preparation | Histories | Mass | Joint (D,Y) cells 00,01,10,11, denominator 1320 |
| --- | ---: | ---: | --- |
| i=0 | 60 | 1 | 246, 295, 0, 779 |
| i=1 | 60 | 1 | 456, 290, 0, 574 |

P₁−P₀ gives ΔD=−41/264 and ΔY=−7/44, with ΔY−ΔD=−1/264.
The eight test groups check the complete literal accepted ledger and counters,
all original row masses and ideal occurrences, immutability and descendant
counts, both joint laws, every causal commutator, every old-field restriction,
the retained central fluctuation, the named swap, renaming and domain rejection.
There are no skipped or expected-failure tests. A successful test of the known
counterexample confirms a **scientific property failure**; it does not remove it.

For every one of 120 marked histories, K=C−Cᵀ and the prepared ordered moment
block is W₂/β=½[[1,−i],[i,1]]. Every three-event old block also persists under
each fourth birth. Real covariance positive definiteness is checked with exact
principal determinants. Ordered W positivity follows from the unchanged supplied
Gaussian factorization L(I₆+iJ)Lᵀ/2, whose canonical blocks have eigenvalues 0,2.
The instantaneous commutator kernel retains fluctuations: for Iₓ=∅, Iᵧ={x},
the formerly central x has Vₓₓ/β=1/2 and later Kᵧₓ=1.

For the accepted i=0 named swap, both structural weights are 19/1320 and each
specified marked branch has weight 19/5280. Transport to `(a,b,u,v)` gives the
same order, marks and counters `(3,1,0,0)`, and the same K. Nevertheless,
V₊−V₋=(β/2)diag(0,0,−1,1). The bounded eᵤ Weyl expectations are exp(−β/2) and
exp(−3β/4), unequal for every β>0. The fixed cover-link mean is exactly 2 in both
histories for all four matched marks. The same program also executes the swap
within preparation i=1, retaining its original structural weights 14/1320 each.
That additional finite check is not a new empirically tested model.

The cover-link mean is computed for all histories; its range on each complete
preparation is [1/2,5/2]. No general equality under other schedule swaps, equality
of full diagnostic laws, or minimal-schedule-register theorem is inferred.

## Boundaries and sources

“Runs” records actual successful command execution. “Reproduces” records exact
known-answer checks, not fresh evidence. No new derivation of the growth law,
Gaussian choices or scale from DET ontology is claimed. Agreement with
observations is **NOT TESTED**: there are no empirical calibration or holdout data.
Native growth premises, chosen register access and imported Gaussian resources
remain distinct in [ASSUMPTIONS.json](ASSUMPTIONS.json).

The prior fresh-spectral covariance obstruction is retained as an accepted source
limitation; this packet does not reimplement that discarded rule. The current
attachment's endpoint-state failure is directly demonstrated here. No repair,
continuum/all-size proof, physical clock/action/mass/energy/stress/gravity source,
coupling, measurement apparatus, conservation law or hardware claim follows.

[RESULT.md](RESULT.md) records achieved versus unresolved outcomes and the actual
author execution intervals on 16 November 2026. Internal fixture/code assistance
was author-side checking, separate from the distinct DET Energy Research review.
**Integrated scientific review: ACCEPT_WITH_SCOPE.** Energy independently ran all
eight test groups and checked every serialized history against the accepted
source tables and field formulas. The coordinator accepted this finite baseline
with no implementation correction. Acceptance covers the registered
prepare-then-step domain and tested renamings; it does not qualify arbitrary
fabricated State/Field objects or a general-purpose validation API.

The [PIM charter](../../../docs/coordination/PROVISIONAL_INTEGRATED_MODEL.md)
sets the research remit. The code's short source names refer to these complete
public statements:

- [Prepared source/readout ledger](../../../docs/observables/native_source_readout_response.md): both preparations, all 15 structural rows and exact D/Y laws.
- [Interval/preparation table](../../../docs/observables/finite_interval_action_and_source_preparation.md): the structural probability fixtures; no interval-action module is added here.
- [Optional incidence register](../../../docs/observables/finite_incidence_register.md): counter access, preparation and classical-realization limits.
- [Gaussian field transport](../../../docs/observables/gaussian_field_transport_on_native_histories.md): the unchanged chronological field formula, retained center and W₂ restrictions.
- [Native field state across a causal diamond](../../../docs/observables/native_field_state_across_a_causal_diamond.md): the accepted state-dependence counterexample and the separately agreeing fixed mean.

The two Python files are exact copies of the stable author implementation and
tests. Public source byte/hash identities are in [ASSUMPTIONS.json](ASSUMPTIONS.json).
