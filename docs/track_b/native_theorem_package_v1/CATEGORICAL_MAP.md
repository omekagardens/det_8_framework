# Deterministic categorical map with exact proxy error

Status: independently reviewed deterministic component with exact map-to-proxy error certification. The optional approximate-width diagnostic remains **ABSTAIN / NOT RUN operationally**. The frozen exact D4-A diagnostic is unchanged.

## Component contract

The [source module](../../../det8/models/certified_categorical_map.py) exposes `CategoricalMap(proxy_weights, bit_width)`. Let the input contain m exact rational proxy probabilities q_i >= 0 with sum q_i = 1 and let N = 2^b. The implementation produces integer cell counts c_i, cumulative boundaries, and

    gamma = (1/2) sum_i |c_i / N - q_i|

as an exact `Fraction`, named `rounding_tv`. It maps one caller-supplied integer w in [0,N) to its outcome index. The module obtains no bits, performs no retry, and has no random source, network, scientific coefficients, data input, width computation, or benchmark runner.

Input weights must be a plain list or tuple of plain `int` or `Fraction` values. Booleans, floats, strings, Decimal values, numeric subclasses and implicit adapters are rejected. Nonnegative weights must sum exactly to one; the constructor never renormalizes them. The constructor accepts 1..256 outcomes, 0..256 bits, and reduced weight numerators/denominators of at most 256 bits each. A numerator or denominator outside that limit is rejected before rational aggregation. Invalid inputs raise `TypeError` or `ValueError`, including under Python optimization: validation does not use `assert`.

The original outcome ordering is retained, including zero-count outcomes. The weights are copied to an immutable tuple, and all derived fields are computed by the frozen dataclass constructor rather than accepted as caller-supplied certificates. These are ordinary Python interface guarantees, not a security boundary against deliberate object tampering.

## Exact partition and error proof

Write N q_i = f_i + r_i, where f_i is the floor and 0 <= r_i < 1. Exact normalization gives the integer

    R = N - sum_i f_i = sum_i r_i, with 0 <= R < m.

Order indices by descending r_i, breaking ties by ascending original index, and set c_i = f_i + 1 for the first R indices and c_i = f_i otherwise. Thus c_i >= 0 and sum c_i = N. If R > 0, the number of positive remainders exceeds R because each is strictly below one. Consequently no zero remainder is rounded up. In particular an exactly zero proxy weight keeps zero cells.

The cumulative boundaries t_0 = 0 and t_{i+1} = t_i + c_i are nondecreasing and end at N. Their half-open intervals [t_i,t_{i+1}) are disjoint and cover every admissible integer exactly once. Right bisection selects that unique interval, skipping empty intervals even when several boundaries coincide. Every outcome remains represented in the certificate, while a zero-count outcome is never returned. For b = 0 the single possible word is zero; ties still follow the same rule.

For an ideal uniform word, the exact output probability p_i is c_i/N. Each coordinate obeys |p_i - q_i| < 1/N: it is zero for an integer Nq_i, r_i/N when rounded down, and (1-r_i)/N when rounded up. Hence gamma <= min(1, m/(2N)), with the untruncated m/(2N) bound in fact strict. The exact reported gamma, rather than this looser bound, is the usable rounding certificate.

Since sum(p_i-q_i)=0, the total positive difference equals the total negative difference in magnitude. An event's probability difference is bounded by their common sum, and the event consisting of the positive coordinates attains it. Therefore

    TV(p,q) = sup_A |p(A)-q(A)| = (1/2) sum_i |p_i-q_i| = gamma.

The implementation uses integer arithmetic and reduced rational arithmetic throughout. There is no floating-point rounding premise. This proof and the tests do not assert a general Python runtime verification theorem or certify execution on an arbitrary platform.

A small positive proxy probability can receive zero cells. That error is included in gamma. The map is an approximation component; it does not establish strict positivity or admissibility of a new DET growth law.

## Connection to the optional width design

The intended width experiment has a complete ideal/newborn-bit outcome row. This generic map does not supply that row, its rational proxy, or the correspondence from its outcome indices to the declared complete alphabet. These must be fixed and reviewed independently; no conditioning or post-selection of that row is licensed.

For a fixed true target row P and a fixed rational proxy q, suppose an independent valid certificate gives TV(q,P) <= eta. Let p be this map's output law under uniform b-bit words, so the source certificate gives TV(p,q) = gamma. If the supplied b-bit block has conditional law R with TV(R,Uniform_b) <= epsilon under the full required history and valid-return conditioning, deterministic mapping and the triangle inequality give

    TV(map_* R, P) <= min(1, epsilon + gamma + eta).

This supplies a possible value of the optional protocol's complete-row error e_a, given all those certificates; gamma alone is not e_a. Any separate width-channel error c_a remains to be included exactly as the optional protocol requires. Under the alternative whole-experiment certificate route, this single-block result likewise does not prove the required joint experiment certificate.

No marginal bit balance, PRNG name, approximate random-bit heuristic, or successful software test supplies the conditional epsilon certificate. Arbitrary inter-draw dependencies remain outside this component's certificate. Rejection, retry, selective omission, changing the map during held-out execution, or an outcome-dependent valid-return rule requires its own applicable law/certificate; the component does not justify those practices.

The optional protocol's effect lower bound d, margin g = d - 2B > 0, alpha = beta = 1/20 budgets, frozen channel/baselines, stopping and failure rules, and distinction between unconditional wrong terminal decisions and detection power counting ABSTAIN all remain unchanged. Certificates with a nonzero chance of invalidity must retain the protocol's explicit certification-failure budgets. This implementation neither provides a failure-rate bound nor proves an end-to-end no-abstention guarantee.

## Costs and checks

Construction performs O(m log m) exact remainder comparisons plus O(m) rational operations and stores O(m) numbers. Mapping uses O(log m) integer boundary comparisons. No length-N cell table is created, even at b = 256. Those are arithmetic-operation counts; bit-operation costs depend on the rational operand sizes. The declared input limits bound the operands and any aggregate denominator by a size growing at most linearly with m times the input denominator-bit bound, plus b. They are resource limits for this implementation, not scientific thresholds or a runtime-performance claim. The caller must supply the b-bit word and any associated costs and certificates.

The [component test suite](../../../det8/tests/test_certified_categorical_map.py) uses stdlib unittest, collectable by pytest, and deterministic synthetic vectors only. Ten test methods passed. The exhaustive test covers all 21 triples with denominator five at each width 0..5: 126 maps, 1,323 cells, and all 1,008 outcome events. Direct cell frequencies match the stored counts; interval membership covers exactly the supplied cells; the event-supremum definition independently matches the exact TV certificate. Additional cases check dyadic exactness, deterministic ties and nearly tied rationals, repeated boundaries, zero-bit blocks, positive weights assigned zero cells, immutability, exact input rejection, and accepted/rejected resource boundaries without enumerating a large word space.

Actual isolated test commands and receipts are retained privately under the [publication evidence boundary](PUBLICATION_NOTE.md). No test drew randomness or ran the diagnostic. These checks establish bounded software evidence for this component, not the missing scientific premises.

## Prospective proxy-envelope certificate

The separate [probability-envelope design](PROXY_ENVELOPE.md) constructs a
normalized rational proxy and a TV bound valid for every normalized row inside
externally certified complete probability intervals. It specifies feasibility,
exact arithmetic and budget/resource abstention, including refusal when the
derived proxy exceeds this map's weight-precision limit. It supplies no actual
intervals or implemented envelope API. The true-law, source/channel, effect and
held-out prerequisites below remain open.

## Remaining instantiation work

An actual declared-law complete outcome row and its index dictionary, independently certified rational proxy error eta, independently certified numeric d, conditional bit-source error epsilon (or a valid whole-experiment bound), width-channel/error certificate, budgets, operational failure treatment, and a held-out freeze are still required before an appropriate benchmark could run. None is provided here. The generic quantizer and its exact map-to-proxy TV certificate close one implementable component only. No actual-law sampling, measured failure rate, held-out advantage, observed-data result, physical prediction, universal theorem, or production qualification follows.

Scope sources: the [fixed exact width diagnostic](WIDTH_DIAGNOSTIC.md) and [optional approximate protocol](APPROXIMATE_WIDTH_DIAGNOSTIC.md). The proof above is a direct finite arithmetic derivation, with no expansion into historical, protected, or native-coefficient sources.
