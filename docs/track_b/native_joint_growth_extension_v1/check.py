#!/usr/bin/env python3
"""Exact, bounded corroboration of RI-36; not a generator or all-size proof.

Run directly with the standard library, normally and with ``python -O``.
The rational fixtures exercise a symbolic construction proved in EXTENSION.md;
passing these fixtures does not prove that construction on its parameter domain.
No project code is imported and no output files or bytecode are written here.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, permutations, product


class CheckFailure(Exception):
    """A check that remains active in optimized Python."""


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


@dataclass(frozen=True)
class Parameters:
    name: str
    a: F
    c: F
    d: F
    f0: F
    f1: F

    def __post_init__(self):
        require(all(type(value) is F for value in
                    (self.a, self.c, self.d, self.f0, self.f1)),
                "parameters must be exact fractions")
        require(0 < self.a < 1 and self.c > 0 and self.d > 0,
                "strict parameter domain")
        require(all(0 < value < 1 - self.c for value in (self.f0, self.f1)),
                "strict chain domain")
        require(self.d + 2 * self.g < 1, "strict antichain domain")

    def f(self, bit):
        return (self.f0, self.f1)[bit]

    def h(self, bit):
        return 1 - self.c - self.f(bit)

    @property
    def g(self):
        return (1 - self.a) * self.c / self.a

    @property
    def k(self):
        return 1 - self.d - 2 * self.g

    @property
    def epsilon(self):
        # Computed only from fixed law parameters, not current parent records.
        largest = max(F(1), self.g / self.d, self.k / self.d,
                      self.f0 / self.c, self.f1 / self.c,
                      self.h(0) / self.c, self.h(1) / self.c,
                      self.k / self.g, self.h(0) / self.f0,
                      self.h(1) / self.f1)
        return 1 / (8 * largest)


def subsets(n):
    return tuple(frozenset(v for v in range(n) if mask & (1 << v))
                 for mask in range(1 << n))


def marks(n):
    return tuple(product((0, 1), repeat=n))


def closure(n, edges):
    result = set(edges)
    for middle in range(n):
        for left in range(n):
            for right in range(n):
                if (left, middle) in result and (middle, right) in result:
                    result.add((left, right))
    return frozenset(result)


def natural_posets(n):
    # Independent of the candidate rows: close every subset of forward edges,
    # then deduplicate the resulting complete strict relations, not histories.
    possible = tuple(combinations(range(n), 2))
    relations = {closure(n, (possible[i] for i in range(len(possible))
                            if mask & (1 << i)))
                 for mask in range(1 << len(possible))}
    return tuple(sorted(relations, key=lambda edges: tuple(sorted(edges))))


def ideals(n, edges):
    return tuple(part for part in subsets(n)
                 if all(right not in part or left in part for left, right in edges))


def shape(n, edges):
    if n == 0:
        return "empty"
    if n == 1:
        return "singleton"
    if n == 2:
        return "chain2" if edges else "antichain2"
    require(n == 3, "rows are defined only through three-event parents")
    if len(edges) == 0:
        return "antichain3"
    if len(edges) == 1:
        return "edge_isolated"
    if len(edges) == 3:
        return "chain3"
    require(len(edges) == 2, "unexpected three-parent relation")
    if any(sum(left == v for left, _ in edges) == 2 for v in range(n)):
        return "fork"
    require(any(sum(right == v for _, right in edges) == 2 for v in range(n)),
            "unexpected three-parent shape")
    return "join"


def row(parameters, n, edges, record, mutation=None):
    """Exact ideal marginals; fair-bit branch coefficient is q / 2."""
    require(len(record) == n and all(bit in (0, 1) for bit in record),
            "invalid full record")
    slots = ideals(n, edges)
    full = frozenset(range(n))
    empty = frozenset()
    kind = shape(n, edges)
    if n == 0:
        return {empty: F(1)}
    if n == 1:
        return {empty: parameters.a, full: 1 - parameters.a}
    if kind == "chain2":
        root = next(iter(edges))[0]
        return {empty: parameters.c,
                frozenset((root,)): parameters.f(record[root]),
                full: parameters.h(record[root])}
    if kind == "antichain2":
        return {empty: parameters.d, frozenset((0,)): parameters.g,
                frozenset((1,)): parameters.g, full: parameters.k}

    epsilon = parameters.epsilon
    # Negative control: discard inherited marks only in new three-parent rows.
    # This still yields local, equivariant, strictly positive normalized rows.
    read_record = (0,) * n if mutation == "drop_inherited_mark" else record
    result = {part: epsilon for part in slots if part != full}
    if kind == "antichain3":
        for part in result:
            if len(part) == 1:
                result[part] = epsilon * parameters.g / parameters.d
            elif len(part) == 2:
                result[part] = epsilon * parameters.k / parameters.d
    elif kind == "edge_isolated":
        root, tip = next(iter(edges))
        isolated = next(v for v in range(n) if v not in (root, tip))
        result[frozenset((root,))] = (
            epsilon * parameters.f(read_record[root]) / parameters.c)
        result[frozenset((root, tip))] = (
            epsilon * parameters.h(read_record[root]) / parameters.c)
        result[frozenset((root, isolated))] = epsilon * parameters.k / parameters.g
        if mutation == "halve_root_ratio":
            result[frozenset((root,))] /= 2
    elif kind == "fork":
        root = next(v for v in range(n)
                    if sum(left == v for left, _ in edges) == 2)
        for part in result:
            if len(part) == 2:
                result[part] = (epsilon * parameters.h(read_record[root])
                                / parameters.f(read_record[root]))
    # chain3 and join retain epsilon on each proper ideal.
    result[full] = 1 - sum(result.values(), F(0))
    require(set(result) == set(slots), "row changed the ideal-slot envelope")
    return result


def transport(n, edges, record, part, permutation):
    require(sorted(permutation) == list(range(n)), "invalid coordinate transport")
    transported_record = [None] * n
    for old, new in enumerate(permutation):
        transported_record[new] = record[old]
    return (frozenset((permutation[left], permutation[right])
                      for left, right in edges),
            tuple(transported_record),
            frozenset(permutation[v] for v in part))


def check_rows(parameters, parents, mutation=None):
    row_count = slot_count = locality_count = equivariance_count = zero_rows = 0
    for n, relations in enumerate(parents):
        records = marks(n)
        for edges in relations:
            cached = {record: row(parameters, n, edges, record, mutation)
                      for record in records}
            for record, probabilities in cached.items():
                row_count += 1
                zero_rows += int(not any(record))
                require(sum(probabilities.values(), F(0)) == 1,
                        "exact row normalization failed")
                for part, probability in probabilities.items():
                    slot_count += 1
                    require(type(probability) is F and probability > 0,
                            "strict positivity failed")
                    if n == 3:
                        if len(part) < n:
                            require(probability <= F(1, 8), "proper-slot bound failed")
                        else:
                            require(probability >= F(1, 8), "full-slot bound failed")
                    for alternative in records:
                        if all(record[v] == alternative[v] for v in part):
                            locality_count += 1
                            require(probability == cached[alternative][part],
                                    "strict precursor-record locality failed")
                for permutation in permutations(range(n)):
                    for part, probability in probabilities.items():
                        moved_edges, moved_record, moved_part = transport(
                            n, edges, record, part, permutation)
                        equivariance_count += 1
                        require(probability == row(parameters, n, moved_edges,
                                                   moved_record, mutation)[moved_part],
                                "marked-parent equivariance failed")
    return row_count, slot_count, locality_count, equivariance_count, zero_rows


def append(n, edges, record, part, bit):
    require(part in ideals(n, edges), "birth precursor is not an old-parent ideal")
    return (edges | frozenset((old, n) for old in part), record + (bit,))


# A normalized positive-definite Hermitian pair kernel with nonzero imaginary
# off-diagonals: diagonal entries 1/2, off-diagonals +/- i/4; eigenvalues 1/4,3/4.
# Each complex entry is (real Fraction, imaginary Fraction); no float arithmetic.
PAYLOAD = ((F(1, 2), F(0)), (F(0), F(1, 4)),
           (F(0), F(-1, 4)), (F(1, 2), F(0)))


def scaled(coefficient, payload):
    return tuple((coefficient * real, coefficient * imaginary)
                 for real, imaginary in payload)


def check_diamonds(parameters, parents, mutation=None, expect_failure=False):
    total = two_base = equal_precursor = all_zero = full_payload = failures = 0
    first_failure = None
    for n in range(3):
        for edges in parents[n]:
            old_ideals = ideals(n, edges)
            for record in marks(n):
                base = row(parameters, n, edges, record, mutation)
                # Ordered pairs, including S=T, preserve all labeled slots.
                for first, second in product(old_ideals, repeat=2):
                    for first_bit, second_bit in product((0, 1), repeat=2):
                        total += 1
                        two_base += int(n == 2)
                        equal_precursor += int(first == second)
                        all_zero += int(not any(record) and first_bit == second_bit == 0)
                        left_edges, left_record = append(n, edges, record, first, first_bit)
                        right_edges, right_record = append(n, edges, record, second, second_bit)
                        left_second = row(parameters, n + 1, left_edges, left_record,
                                          mutation)[second] / 2
                        right_second = row(parameters, n + 1, right_edges, right_record,
                                           mutation)[first] / 2
                        left_first = base[first] / 2
                        right_first = base[second] / 2
                        left_terminal = append(n + 1, left_edges, left_record,
                                               second, second_bit)
                        right_terminal = append(n + 1, right_edges, right_record,
                                                first, first_bit)
                        exchange = tuple(range(n)) + (n + 1, n)
                        transported = transport(n + 2, *right_terminal, frozenset(), exchange)
                        require(left_terminal == transported[:2],
                                "whole terminal order/record transport failed")
                        left_coefficient = left_first * left_second
                        right_coefficient = right_first * right_second
                        # Scalar-map identity is the general obligation. The full
                        # complex witness additionally guards against conditional
                        # renormalization concealing a scalar-weight mismatch.
                        left_payload = scaled(left_second, scaled(left_first, PAYLOAD))
                        right_payload = scaled(right_second, scaled(right_first, PAYLOAD))
                        require(left_payload == scaled(left_coefficient, PAYLOAD)
                                and right_payload == scaled(right_coefficient, PAYLOAD),
                                "sequential full-payload scaling failed")
                        full_payload += 1
                        if left_coefficient != right_coefficient:
                            failures += 1
                            require(left_payload != right_payload,
                                    "nonzero full payload concealed a weight mismatch")
                            if first_failure is None:
                                first_failure = (n, tuple(sorted(edges)), record,
                                                 tuple(sorted(first)), tuple(sorted(second)),
                                                 first_bit, second_bit)
                        else:
                            require(left_payload == right_payload,
                                    "equal scalar maps changed the full payload")
    require(total == 436 and two_base == 400,
            "diamond-domain coverage differs from the declared 436/400 cases")
    require(equal_precursor == 132 and all_zero == 30,
            "equal-precursor or all-zero-sector coverage is incomplete")
    if expect_failure:
        require(failures > 0 and first_failure[0] == 2,
                "negative control did not expose a size-two-base diamond failure")
    else:
        require(failures == 0, f"diamond failures: {failures}; first={first_failure}")
    return total, two_base, equal_precursor, all_zero, full_payload, failures


def main():
    parents = tuple(natural_posets(n) for n in range(4))
    require(tuple(map(len, parents)) == (1, 1, 2, 7), "parent enumeration failed")
    require({shape(3, edges) for edges in parents[3]} ==
            {"antichain3", "edge_isolated", "chain3", "fork", "join"},
            "missing three-parent order type")
    require(len(set(parents[3])) == 7, "duplicate parent relations")
    fixtures = (
        Parameters("interior_a", F(2, 3), F(1, 5), F(1, 4), F(1, 6), F(1, 3)),
        Parameters("interior_b", F(1, 2), F(1, 5), F(1, 5), F(1, 5), F(2, 5)),
        Parameters("small_a_f0", F(1, 10), F(1, 100), F(1, 100), F(1, 1000), F(49, 50)),
        Parameters("large_a_small_h1", F(99, 100), F(1, 4), F(1, 3), F(1, 100), F(37, 50)),
    )
    for parameters in fixtures:
        require(parameters.f0 != parameters.f1, "fixture lacks root-mark feedback")
        rows = check_rows(parameters, parents)
        require(rows[0] == 67 and rows[1] == 353 and rows[3] == 1981 and rows[4] == 11,
                "row/equivariance/zero-sector coverage changed")
        diamonds = check_diamonds(parameters, parents)
        # Distinct unlabeled outcomes from a two-chain: root-only precursor
        # yields a fork, full precursor a chain. Their probabilities are f(r),h(r).
        chain = frozenset(((0, 1),))
        root_only = frozenset((0,))
        zero = row(parameters, 2, chain, (0, 0))[root_only]
        one = row(parameters, 2, chain, (1, 0))[root_only]
        require(zero != one, "unlabeled fork probability lost record feedback")
        print(f"{parameters.name}: rows={rows[0]} slots={rows[1]} "
              f"locality={rows[2]} equivariance={rows[3]} zero_rows={rows[4]}; "
              f"diamonds={diamonds[0]} two_base={diamonds[1]} "
              f"equal_precursor={diamonds[2]} all_zero={diamonds[3]} "
              f"full_payload={diamonds[4]}; PASS")
    for mutation in ("halve_root_ratio", "drop_inherited_mark"):
        # These still pass every row check, making the diamond failure specific.
        check_rows(fixtures[0], parents, mutation)
        result = check_diamonds(fixtures[0], parents, mutation, expect_failure=True)
        print(f"negative_control={mutation}: row_checks=PASS "
              f"detected_diamond_failures={result[5]}; PASS")
    print("PASS: exact finite-prefix corroboration only; no all-size or physical claim")


if __name__ == "__main__":
    main()
