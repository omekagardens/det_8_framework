"""Deterministic synthetic checks only; no randomness or held-out samples."""

from collections import Counter
from dataclasses import FrozenInstanceError
from decimal import Decimal
from fractions import Fraction
import unittest

from det8.models.certified_categorical_map import (
    CategoricalMap,
    MAX_BIT_WIDTH,
    MAX_OUTCOMES,
    MAX_WEIGHT_BITS,
)


class TestCategoricalMap(unittest.TestCase):
    def test_exact_dyadic_proxy(self):
        mapping = CategoricalMap([Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)], 4)
        self.assertEqual(mapping.cell_counts, (8, 4, 4))
        self.assertEqual(mapping.boundaries, (0, 8, 12, 16))
        self.assertEqual(mapping.rounding_tv, 0)

    def test_exact_remainders_and_tie_order(self):
        mapping = CategoricalMap((Fraction(1, 3),) * 3, 2)
        self.assertEqual(mapping.cell_counts, (2, 1, 1))
        self.assertEqual(mapping.rounding_tv, Fraction(1, 6))
        non_tie = CategoricalMap((Fraction(1, 10), Fraction(3, 10), Fraction(3, 5)), 3)
        self.assertEqual(non_tie.cell_counts, (1, 2, 5))
        # Exact remainders distinguish these weights despite their closeness.
        close = CategoricalMap((Fraction(1, 2) - Fraction(1, 2**100),
                                Fraction(1, 2) + Fraction(1, 2**100)), 0)
        self.assertEqual(close.cell_counts, (0, 1))

    def test_zero_intervals_and_half_open_endpoints(self):
        mapping = CategoricalMap((0, Fraction(1, 2), 0, Fraction(1, 2), 0), 2)
        self.assertEqual(mapping.boundaries, (0, 0, 2, 2, 4, 4))
        self.assertEqual([mapping.map_word(x) for x in range(4)], [1, 1, 3, 3])
        self.assertEqual(len(mapping.cell_counts), 5)

    def test_zero_bits_and_positive_proxy_with_no_cell(self):
        singleton = CategoricalMap((1,), 0)
        self.assertEqual(singleton.total_cells, 1)
        self.assertEqual(singleton.map_word(0), 0)
        self.assertEqual(singleton.rounding_tv, 0)
        mapping = CategoricalMap((Fraction(1, 100), Fraction(99, 100)), 0)
        self.assertEqual(mapping.cell_counts, (0, 1))
        self.assertEqual(mapping.rounding_tv, Fraction(1, 100))
        self.assertEqual(mapping.map_word(0), 1)
        tie = CategoricalMap((Fraction(1, 3),) * 3, 0)
        self.assertEqual(tie.cell_counts, (1, 0, 0))

    def test_exhaustive_small_maps_and_event_supremum(self):
        # All 21 rational triples with denominator five, and widths 0..5.
        # Cell enumeration is independent of the constructor's rounding logic;
        # all eight events realize the defining supremum for finite-space TV.
        for first in range(6):
            for second in range(6 - first):
                weights = tuple(Fraction(x, 5) for x in
                                (first, second, 5 - first - second))
                for width in range(6):
                    with self.subTest(weights=weights, width=width):
                        mapping = CategoricalMap(weights, width)
                        total = 2**width
                        observed = Counter(mapping.map_word(x) for x in range(total))
                        self.assertTrue(set(observed).issubset({0, 1, 2}))
                        frequencies = tuple(Fraction(observed[i], total) for i in range(3))
                        self.assertEqual(tuple(observed[i] for i in range(3)), mapping.cell_counts)
                        self.assertEqual(mapping.boundaries[0], 0)
                        self.assertEqual(mapping.boundaries[-1], total)
                        self.assertEqual(sum(mapping.cell_counts), total)
                        self.assertEqual(tuple(mapping.boundaries[i + 1] - mapping.boundaries[i]
                                               for i in range(3)), mapping.cell_counts)
                        for i in range(3):
                            self.assertLess(abs(frequencies[i] - weights[i]), Fraction(1, total))
                            for word in range(total):
                                in_interval = mapping.boundaries[i] <= word < mapping.boundaries[i + 1]
                                self.assertEqual(mapping.map_word(word) == i, in_interval)
                        event_errors = []
                        for mask in range(8):
                            actual = sum((frequencies[i] for i in range(3) if mask & (1 << i)), Fraction(0))
                            proxy = sum((weights[i] for i in range(3) if mask & (1 << i)), Fraction(0))
                            event_errors.append(abs(actual - proxy))
                        self.assertEqual(max(event_errors), mapping.rounding_tv)

    def test_input_copy_and_frozen_derived_fields(self):
        source = [Fraction(1, 2), Fraction(1, 2)]
        mapping = CategoricalMap(source, 1)
        source[0] = 0
        self.assertEqual(mapping.proxy_weights, (Fraction(1, 2), Fraction(1, 2)))
        with self.assertRaises(FrozenInstanceError):
            mapping.rounding_tv = Fraction(1)
        with self.assertRaises(TypeError):
            CategoricalMap((1,), 0, rounding_tv=Fraction(0))

    def test_invalid_weights(self):
        for value in (0.5, Decimal("0.5"), "1/2", True, None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                CategoricalMap((value, Fraction(1, 2)), 1)
        for weights in ((), (0,), (1, 1), (Fraction(1, 3), Fraction(1, 3)),
                        (Fraction(-1, 2), Fraction(3, 2))):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                CategoricalMap(weights, 1)
        for container in (None, "1", iter((1,))):
            with self.subTest(container=container), self.assertRaises(TypeError):
                CategoricalMap(container, 1)

    def test_invalid_bit_widths_and_words(self):
        for width in (True, 2.0, Fraction(2), "2"):
            with self.subTest(width=width), self.assertRaises(TypeError):
                CategoricalMap((1,), width)
        for width in (-1, MAX_BIT_WIDTH + 1):
            with self.subTest(width=width), self.assertRaises(ValueError):
                CategoricalMap((1,), width)
        mapping = CategoricalMap((1,), 2)
        for word in (True, 1.0, Fraction(1), "1"):
            with self.subTest(word=word), self.assertRaises(TypeError):
                mapping.map_word(word)
        for word in (-1, 4, 2**1000):
            with self.subTest(word=word), self.assertRaises(ValueError):
                mapping.map_word(word)

    def test_resource_bounds_without_cell_table(self):
        mapping = CategoricalMap((Fraction(1, 3), Fraction(2, 3)), MAX_BIT_WIDTH)
        self.assertEqual(mapping.total_cells, 2**MAX_BIT_WIDTH)
        self.assertEqual(len(mapping.boundaries), 3)
        self.assertEqual(mapping.map_word(mapping.total_cells - 1), 1)
        at_limit = CategoricalMap((Fraction(1, MAX_OUTCOMES),) * MAX_OUTCOMES, 8)
        self.assertEqual(sum(at_limit.cell_counts), 256)
        with self.assertRaises(ValueError):
            CategoricalMap((0,) * MAX_OUTCOMES + (1,), 0)
        tiny = Fraction(1, 2**(MAX_WEIGHT_BITS - 1))
        CategoricalMap((tiny, 1 - tiny), 0)
        too_precise = Fraction(1, 2**MAX_WEIGHT_BITS)
        with self.assertRaises(ValueError):
            CategoricalMap((too_precise, 1 - too_precise), 0)
        with self.assertRaises(ValueError):
            CategoricalMap((2**MAX_WEIGHT_BITS,), 0)

    def test_numeric_subclasses_are_not_implicit_adapters(self):
        class IntLike(int):
            pass
        class FractionLike(Fraction):
            pass
        class ListLike(list):
            pass
        for weights in ((IntLike(1),), (FractionLike(1),), ListLike([1])):
            with self.subTest(weights=weights), self.assertRaises(TypeError):
                CategoricalMap(weights, 0)
        with self.assertRaises(TypeError):
            CategoricalMap((1,), IntLike(0))
        with self.assertRaises(TypeError):
            CategoricalMap((1,), 0).map_word(IntLike(0))


if __name__ == "__main__":
    unittest.main()
