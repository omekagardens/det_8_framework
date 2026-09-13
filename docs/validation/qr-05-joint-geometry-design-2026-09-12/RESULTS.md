# Joint geometric channels: analytical decision record

12 September 2026. **Analytical/design gate complete.** The
[standalone contract](README.md) puts marked causal structure, orientation,
relative proper volume, absolute proper volume and sampling nuisances on
one common world class. No new numerical executor, test suite, simulation,
64-world enumeration or acquisition ran in this design gate.

## Publication checkpoint

Before starting this gate, the 15-file branch audit/reconciliation was
committed as `47262b616296c632189d4e8b3e2582ed2016a6d8` and pushed to
`origin/ret`. A direct remote-ref check matched that full commit.

Publication preflight reran the existing reconciliation's 19 normal tests
and exact report replay successfully. Independent metadata review confirmed
its six frozen sources and all 12 BV frozen sources and both captures'
source/freeze bindings. Those checks belong to publication of the prior
result, not execution of the new geometric model.

The separate 231 dirty core/RET/application entries were excluded. No merge
from `qr-05-bridge`, core/registry edit, dependency installation or
`temp_qr.md` change was made.

## Main mathematical result

The supplied metric and sampling intensity are

```text
g = L(1+a x)(−dt²+κ²dx²),
λ = r(1+b x),
dM = κLr(1+a x)(1+b x) dt dx,
Λ = κLr[1+(a+b)/2+ab/3].
```

Here κ∈{1,2}, ε∈{−1,+1}, a,b∈{0,1}, while L,r range over ALL positive
values. The marked geometric target comprises two directed probe relations,
the left-strip proper-area fraction and total proper area. It is equivalent
to the four geometric coordinates (κ,ε,a,L) in this family.

The five declared information channels jointly identify that target:

- O: signed causal comparisons, identifying κ and ε within the supplied menu.
- P: normalized strip-membership law.
- T: total-count marginal mean Λ, not the full marked count law.
- D: ideal sampling-shape reference b.
- R: ideal density-normalization reference r.

P with D identifies a; T with R and the recovered shape/cone parameters
identifies L. Five exact omission witnesses show that every proper subset
fails global identification on the common world class. Some particular
fibers can still have a unique target. Nor does the result claim that five
separate physical devices are required.

The positive result is conditional. Causal comparison is supplied by O,
not derived from scalar counts. D,R are unsupplied ideal references; R
requires dimensional metrology before it can serve as a physical scale
anchor. Model-inconsistent channel tuples must be refused, not coerced.

## The decisive joint collision

With κ,ε fixed, choose independently

`(a,b)=(1,0) or (0,1)`, and `(L,r)=(1,1) or (3/2,2/3)`.

All four worlds have the same intensity `κ(1+x)dt dx`, chronology, normalized
point law, P=5/12 and T=3κ/2. Under the expressly stipulated Poisson model they
have the same complete point-process law; conditional iid fixed-quota point
laws coincide too. Supplying more summaries or even all the sampled causal
relations cannot break this particular collision.

Yet relative and/or absolute proper volume differ. D distinguishes the
geometry/sampling shape exchange, while R breaks the scale/rate compensation.
This exhibits simultaneous geometric ambiguities on a common class; it is
not an inference from separate axis slices or unrelated sampled panels.

Identical intensity would not determine the law of an arbitrary correlated
point process. The Poisson premise is essential to that stronger law claim.
A fixed quota contains no information about the total count intensity.

## Information and quantum-record implications

Conditioning on κ,a,b, use u=log(L/L_0), v=log(r/r_0). Both Poisson score
components equal N−Λ, so

`I(u,v)=Λ [[1,1],[1,1]]`.

The null direction (1,−1) is the scale/density compensation. Independent
repetition multiplies the information matrix but leaves its null direction.
This concerns the record channels before supplying the ideal r reference;
fixed-quota normalized observations alone have a zero block for these parameters.
This is a useful structural-identification diagnostic for future estimation
work, not a spacetime curvature tensor or evidence of RET readiness.

A finite classical–quantum encoding with fixed word-conditioned states has
the same state whenever the input word laws agree. Any common subsequent
quantum channel preserves that equality. A genuinely world-dependent quantum
probe would be additional information needing a separate physical contract;
it is neither supplied nor ruled out here.

Every finite scalar record has overlapping positive support in the relevant
alternatives. Population-law identification is not error-free finite-sample
recovery. Noise, loss, calibration and selection remain separate obligations.
Observed conflicts with a specified acquisition law would require diagnosing
or revising its premises; they cannot simply be renamed noise.

## Independent analytical review

Two independent reviews checked the full contract's geometry, volume and
probability integrals, fixed interior probes, active/passive distinctions,
joint inverse, five omission witnesses, four-world collision and finite
verification census. No mathematical code was executed by the reviewers.

Review clarified an important interface boundary: the joint inside/outside
count law contains both P and T, so it cannot be substituted for the T-only
channel in a minimality argument. The finalized contract states this and
rejects out-of-model channel combinations explicitly.
An additional independent analytical check confirmed the Poisson score and
rank-one information matrix, including the fixed-quota zero-information case.

The witness design is transparent. An earlier candidate scale grid {1,4}
made P redundant through discrete intensity separation. The analytical claim
instead uses continuous L,r and explicit collisions already contained in
the rational grid {1,3/2}×{1,2/3}. No data were fitted and no observed parameter
spectrum is claimed. This is a check against finite-catalogue artifacts.

Final documentation checks resolved 90 local links across the new documents
and roadmap, and the tracked diff passes whitespace checks. All six prior
reconciliation source identities and all 12 BV identities still match their
freezes, without rerunning their mathematics during this design gate. The
231 unrelated status entries remain unchanged. This new two-document design
and its roadmap update remain local and uncommitted after the earlier audit push.

## Next gate: bounded exact verification, not acquisition

The prospective rational subclass has 64 worlds, all six coordinates varied
jointly, and 32 channel subsets. There are 16 joint targets, four nuisance
worlds per target and 1,920 differing-target unordered pairs.

Freeze the exact protocol, independently derived raw rational channels and
targets, the observation-partition/pair-separator comparison, and the evidence
driver before execution. Preserve every partition and witness. Expected
global outcome: the full five-channel set identifies, the other 31 do not.
This census is analytically specified, not yet computationally verified.

The next gate should check these formulas and collisions without generating
Poisson samples, enumerating count tails or importing the branch's rejected
geometry engines. Later work remains separately scoped: operator contracts,
correspondence-distance normalization, uniform bounds, stochastic growth/null
calibration and eventually empirical interfaces. No gravity dynamics, ontology,
new law, material-monitoring deployment, anomaly classifier, book revival or
deferred clock coupling is established.
