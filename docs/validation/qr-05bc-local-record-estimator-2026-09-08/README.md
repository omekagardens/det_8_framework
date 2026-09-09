# QR-05BC: local quantum records to a supplied geometric-response estimator

8 September 2026 (Pacific/Honolulu). Bounded exact synthetic verification.
This protocol is written before implementation or fixed numerical evaluation.
The preceding [BB model](../qr-05bb-operational-bridge-design-2026-09-08/README.md)
supplies the complete mathematical interpretation and analytical boundary.

## Frozen question and domain

Can registered local Z outcomes estimate the supplied bilinear response
functional in the precise population-law sense, while an interior bubble
remains invisible to the same four sites? Neither the metric nor the target
integral is given to the observer as an unknown answer to rediscover.

The machine-readable [protocol](protocol.json) fixes one unit null-coordinate
rectangle, dμ = du dv/2, V = μ(Q), F = V²f, σ = V⁴ and
R_Q = (1−u)(1−v)/2. The target is T(F) = ∫F R_Q dμ/σ. Four stations use
order (00,10,01,11). Their bilinear basis is (1−u)(1−v), u(1−v), (1−u)v, uv.
Weights wₐ = V²∫φₐR_Q dμ/σ are compiled from geometry before profiles.

At each station ρₐ = (I₂+fₐZ)/2, Πₓ = (I₂+xZ)/2 and the retained
unnormalized branch is ΠₓρₐΠₓ. Independent fresh preparations yield the
product Born law. All 16 outcome vectors are retained for each of six
prespecified profiles: zero, all plus, all minus, asymmetric rational means,
and the two deterministic one-plus profiles at corners 00 and 11.
The estimator uses only labeled outcomes and geometry weights. Its expected
value, not each finite record, is compared with the bilinear target.

The continuous-profile negative control is f = u(1−u)v(1−v) versus f = 0.
Its sampled states are identical, but its true interior target need not be.
The interpolation model is deliberately held fixed; this is a larger-domain
identifiability test, not a failure inside the bilinear family.

## Independent routes and limits

- `quantum.py`: explicit sparse tensor-product density matrices and local
  projectors, branch operators/states and monomial polynomial integration.
- `reference.py`: independent classical Bernoulli products and factorized
  beta-moment integration, with independently constructed branch operators.
  It must not import the quantum implementation or its computed weights.
- `study.py`: source/protocol-bound orchestration, exact report comparison,
  a record-only estimator, refusal controls and create-only capture/replay.
- `test_qr05bc.py`: independent adversarial and contract checks, including
  malformed records/artifacts and optimized-Python behavior. A third geometric
  route uses tensor Simpson integration, exact for the prescribed degree-at-
  most-three product integrands. These are private fixture/oracle evaluations,
  not additional measurements available to the public observer.

No numerical tolerance, Monte Carlo seed, decoder fit or target lookup table
is used. Fractions remain exact. Positive passage requires agreement of the
complete reports, not only their aggregate means. The primary source and
reference share the frozen inputs, not mathematical helpers or outputs.

Full branch Kraus operators are compared across all 24 station permutations.
Diagonal storage is exact for these Z projectors, not a deletion of unknown
off-diagonal entries. Operator equality certifies equality of the associated
outcome maps on this four-qubit operator space; it is not physical covariance.
Selected postmeasurement states remain unnormalized, including zero branches.

## Prespecified controls

1. Keep the entire corner record law for the zero/bubble pair and independently
   integrate its unequal true targets. Extra repeats at these same sites
   cannot repair the analytical information loss.
2. Retain labeled estimates, a wrong 00↔11 label swap, correct joint
   record/weight relabeling, and histograms that forget station identity.
   The two one-plus profiles provide a full histogram-law collision.
3. At station 00 with zero polarization, compare all four two-shot histories
   for fresh copies versus repeated Z measurement without reset. This is the
   sole repeat extension; no larger repeated-trial enumeration is authorized
   by the protocol. Matching one-shot marginals does not establish independence.
4. Enumerate all four true/registered ±1 assignments for the four frozen
   calibration rows. Compare direct assignment probabilities with the affine
   response formula. Retain the unknown-calibration confound and zero-contrast
   refusal; inversion needs known offset and known nonzero contrast.
5. Compare the stated geometric integral with a naive corner trapezoid of
   its product integrand. This does not condemn exact interpolation of R_Q;
   the mistake is replacing product integration with that nodal quadrature.
6. Verify one conditional error-composition example, using the bubble and
   the declared corner errors. Its supplied ε = 1/16 follows from the
   elementary bound u(1−u), v(1−v) ≤ 1/4. This is not an inferred uncertainty
   budget, sharpness theorem or transfer of BA's receiver certificate.
7. Require complete ideal records with known quotas. Reject missing, duplicate,
   unavailable, nonattempted, malformed or mismatched records, postselection,
   hidden/private fields and calibration/frame/setting mismatch. Missing
   records are not outcome zero or detector nondetection. Physical loss is
   outside the ideal binary POVM and would require an expanded model.

## Observer and evidence contract

The public estimator accepts exactly four one-shot records and four compiled
weights keyed by station. It receives no private profile ID, f, density
matrix, probability, target or fixture seed. Every record key and public
context value is frozen in the protocol; registration references are opaque
ideal-packet identifiers, not extra outcome channels. All records must be
available at the collector. File/list order may change; event/shot labels may
not disappear. This schema is a research contract, not an SDK or detector.

The evidence driver records hashes of the protocol, current implementation
and tests, and both preceding BB documents. It does not recursively import
or rerun old BA engines and does not inherit their mathematical certificates.
Capture is create-only; replay checks strict JSON types, complete identities
and the entire recalculated report. Duplicates, unexpected fields and
type-changing replacements are errors, not equal-looking evidence.
The native engine reports are compared before rational-string encoding.
Engines execute freshly from their checked source bytes, not cached imports.
Input immutability, capped reads, exclusive writes, readback and final
source/freeze/artifact identity checks protect this bounded local workflow;
they are not authentication of a laboratory experiment or a hostile host.

Source identity is frozen at the first fixed evaluation. Any subsequent
implementation/protocol correction must be documented, and a failed first
capture must not be overwritten or concealed. Development corrections before
that first evaluation may be recorded separately. Source revisions require
a new capture, never an in-place edit of old evidence.

No timing-sensitive RET rehearsal may overlap these small research runs.
No RET/core imports, dependency changes, heavy inherited suites, hardware
operations, clock tests or application-release claims belong to this gate.

## Acceptance and interpretation

The independent exact routes must agree on geometry, complete branch laws and
states, estimator moments, all retained controls and error identities. The
public decoder must reproduce estimates without private inputs and refuse
malformed/access-incomplete inputs in normal and optimized Python. Negative
controls must retain the expected discrepancies; universal agreement across
deliberately invalid alternatives would itself be a failure.

Record all failures. An exact disagreement needs an implementation repair or
narrower premise, not attribution to apparatus noise. A passing result is
restricted model correspondence plus an information-loss witness, not quantum
advantage, empirical compatibility, arbitrary-profile recovery, inferred
geometry or gravity. Later calibration, new measurement access and RET
integration require their own protocols.

Implementation status and measured execution results will be recorded in
[RESULTS.md](RESULTS.md) after the frozen study is run; none is reported by this initial
protocol text. Ordinary QM and the conventional retarded-kernel comparison
are adopted from the primary sources cited in BB, without ontological premises.

## Reproduction commands

From this study directory, once the retained capture exists:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bc.py
python3 -I -O -B test_qr05bc.py
```

The initial source freeze is created with `study.py --freeze source-freeze.json`
and the initial capture with `study.py --capture results.json`. These are
create-only operations; do not remove or overwrite the retained artifacts to
repeat them. Runtime identity describes the source-freeze environment; replay
deliberately permits a different optimization mode while retaining exactly
the same mathematical evidence and checked source identities.
