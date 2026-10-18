# Exact linear identifiability contract

RI-12, 13 September 2026. This module implements a bounded structural check for
the proposed comparator application in
[APPLICATION_WORK_PLAN.md](APPLICATION_WORK_PLAN.md). It is ordinary linear
algebra, not a novelty, quantum, experimental-success or RET-integration claim.
The implementation is [identifiability.py](../../det8/applied_physics/identifiability.py).

## Domain and question

Let the parameter vector `theta` range over **all of R^n**, with `n >= 1`.
The supplied exact rational matrix `H` has `m >= 0` rows, and the supplied exact
rational row `q` specifies the question `q theta`. Coordinates use the same
positional parameter order `theta[0], ..., theta[n-1]` in every row, target and
candidate. The certificate retains these coefficients and their order.

The entries of `H`, `q` and candidate rows are **known model coefficients**, not
noisy observed responses, estimated coefficients or inferred apparatus laws.
The structural question is whether `H theta = H theta'` always implies
`q theta = q theta'`. It does not require an observed response vector.
In a noisy model with known parameter-independent noise, equal mean maps give
equal observation laws; this check still does not give finite-sample certainty,
an estimator, confidence interval, posterior precision or a model-family choice.

## Theorem and finite witnesses

For unrestricted real parameters, these statements are equivalent:

1. The question has the same value on each fiber of the mean map `theta -> H theta`.
2. `q delta = 0` for every `delta` in `ker H`.
3. `q` lies in the real row space of `H`.
4. There is a rational row-weight vector `lambda` with `lambda^T H = q`.

For (1) versus (2), take `delta = theta' - theta`; conversely any null direction
gives indistinguishable mean maps. A row combination annihilates the nullspace.
Rational RREF proves the converse and supplies the exact witnesses below,
so rational coefficients do not restrict the parameter domain to rational
vectors. Full column rank is sufficient but is **not necessary** for identifying
a particular question.

The implementation tracks row operations `R = E H`, retaining the nonzero RREF
rows and their pivot columns. Eliminate pivot coordinates from `q` with these
rows while accumulating their weights in `E`. If the remaining row is zero,
the accumulated `lambda` proves identification by direct multiplication.

Otherwise choose a free coordinate `j` with nonzero remaining coefficient
`r_j`. Set `delta_j = 1/r_j`, set other free coordinates to zero, and set each
pivot coordinate `p_i` to `-R_ij/r_j`. Then `H delta = 0` and `q delta = 1`.
This proves failure of identification by the concrete pair `theta = 0` and
`theta' = delta`; more generally `theta` and `theta + delta` have the same mean
map and different answers for every `theta`. Unrestricted parameters are
essential for treating every such pair as allowed.

The zero target is identified even when `H` is empty, using zero row weights
(the empty tuple for an empty design). A nonzero target with an empty design
has a normalized null witness. No floating-point tolerance or prior enters
the calculation. Rank is computed by exact rational elimination.

The two witness identities can be independently checked by exact substitution.
They certify the requested question's status; by themselves they are not
separate certificates of the reported matrix rank. Rank follows the RREF
calculation and can be independently recomputed.

## Public interface and refusal limits

```python
from fractions import Fraction
from det8.applied_physics.identifiability import analyze_identifiability

result = analyze_identifiability(
    design=[(2, 1)],                  # theta = (gain, offset)
    target=(0, 1),                    # offset
    candidates=[("zero reference", (0, 1))],
)
```

`IdentifiabilityAnalysis` extends `LinearCertificate`. Both are frozen, slotted
dataclasses. Their fields are `design`, `target`, `n_rows`, `n_parameters`,
`rank`, `identified`, `row_weights` and `null_direction`. Exactly one of
`row_weights` and `null_direction` is present. Every rational output entry is
a `Fraction`; designs, rows and weights are tuples detached from mutable input
containers. The analysis adds the immutable tuple `candidates`.

Each `CandidateAnalysis` has `label`, `row`, `separation`,
`separates_displayed_pair` and `certificate`. Candidate input is an iterable of
`(label, single_row)` pairs. Labels are supplied availability names, not evidence
of physical feasibility. They must be distinct, nonblank built-in strings and
are retained verbatim. Candidate order is retained without ranking or cost.

The bounded input contract is:

| Limit | Value |
|---|---:|
| Nonempty parameter dimension / target length | 1 through 8 |
| Base design rows | 0 through 32 |
| Individually analyzed candidate rows | 0 through 16 |
| Candidate label length | 1 through 128 characters, nonblank |
| Bit length of each reduced input numerator and positive denominator | at most 64 each |

Coefficient types are exactly built-in `int` or `fractions.Fraction`; floats,
booleans, numeric strings, other numeric types and subclasses are refused.
An explicitly supplied `Fraction` is taken as an assertion of an exact model
coefficient; the module cannot establish how it was obtained. Every row must
match the target dimension. Text and mappings are not row/container formats.
Type violations raise `TypeError`; malformed shapes, duplicate/invalid labels
and size limits raise `ValueError`. There is no partial successful result after
an invalid candidate.

Each supplied container is materialized once, reading at most its applicable
limit plus one entries, so an overlong generator is refused without exhausting
it. The row limit applies to the base design: each augmented certificate may
have 33 rows. Exact derived fractions may exceed 64 bits; that is an input
limit, not a truncation or output rounding rule. Finite input-bit and dimension
limits bound rational arithmetic growth, but are not a constant-time or fixed
latency guarantee. No floating-point conversion, optional numerical dependency
or hidden tolerance is used.

## Candidate separation is not complete identification

For an unidentified base target, `separation = row dot delta` tests whether the
candidate separates the **displayed** mean-map pair. Its sign and magnitude
are algebraic values in the supplied units, not a noisy detection probability
or a utility score. Separately, the candidate's `certificate` analyzes the
full augmented design `[H; row]` and includes its own row weights or normalized
null direction. Thus it can still exhibit unresolved ambiguity even when the
old displayed pair is separated. If the base target is identified, no pair is
displayed and both separation fields are `None`; the augmented certificate
still proves identification.

For example, take three unrestricted parameters, `H = [(1,0,0)]` and
`q = (0,1,0)`. The displayed direction can be `delta = (0,1,0)`. The candidate
`a = (0,1,1)` separates this pair, but the augmented design still has the
null direction `(0,1,-1)` with target value one. Another candidate
`b = (0,0,1)` does not separate the original displayed pair and does not alone
identify `q`. Together, `a-b = q`; analyze a new design containing both rows
to certify joint identification. This single-row API does not implicitly
combine or rank candidate actions.

## Comparator interpretation

The example is explicitly a **single-channel** comparator with mean
`y = g x + b` and parameter order `(g,b)`. It is not a diagnosis of the existing
RET apparatus adapter: that adapter supplies two axes at `x` and `x+0.25`,
which can already give two independent rows in one fully observed action.

One reading level `x0` supplies row `(x0,1)`. Repeating this row does not change
the structural rank, although repeated noisy measurements can improve
precision. The prediction at the same level has target `(x0,1)` and is
identified. Gain, offset (unless `x0=0`), and prediction at another level are
not identified from this one level alone. The invisible direction
`(1,-x0)` leaves the observed mean fixed; prediction at `x*` changes by
`x*-x0`. The module scales a suitable direction so the requested target changes
by exactly one. Adding a second distinct level `(x1,1)` gives determinant
`x0-x1 != 0` and identifies both parameters and every linear target. A zero
reference at `x0=0` already identifies offset, but not gain.

Exact identification is also distinct from practical conditioning: two
arbitrarily close but distinct levels give exact rank two, while the resulting
noisy gain/offset estimates may have unusable precision. This module reports no
conditioning or precision guarantee.

A proper prior can produce finite posterior precision in an unobserved
direction. That prior-based certainty is distinct from identification by the
mean map. No confidence or uncertainty number is inferred from rank or witness
separation here. Supplied candidate rows establish availability only in the
algebraic input; noise, cost, reset, stability and reference accuracy require
separate apparatus evidence.

Future integration must assemble `H` from actually assimilated observed
training axes in the declared parameter order. Validation/held-out responses,
missing axes or merely proposed measurements must not be counted as existing
information. An action with multiple axes needs its whole added row block and
a fresh analysis; this API analyzes single-row candidates separately.

## Outside this contract

Parameter constraints or restricted domains can change identifiability; a
null pair may then be inadmissible. Nonlinear models, unknown or noisy
reference coefficients, parameter-dependent noise, causal mechanism selection,
model-family comparison and finite-sample estimation are outside this theorem
and implementation. This is not evidence that a particular observation bank,
prior, covariance, action or physical comparator satisfies the model. No RET
source or registry integration, pilot execution or benefit claim is included.
