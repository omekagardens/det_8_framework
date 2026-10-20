"""A deterministic finite categorical map with an exact proxy-TV certificate.

``CategoricalMap(q, b)`` partitions the integers in ``[0, 2**b)`` into
contiguous outcome intervals.  Under a *uniform* input word its outcome
probabilities are exactly ``cell_counts[i] / total_cells``.  ``rounding_tv``
is their exact total-variation distance from the supplied rational proxy q.

This module does not obtain random bits, sample a physical or growth law,
certify q against another law, or certify the distribution of supplied words.
Those obligations remain external, including any required conditional-on-
history and valid-return certificates in an approximate-sampler protocol.
"""

from bisect import bisect_right
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence, Tuple, Union


# Storage depends on these bounds, never on an array of 2**bit_width cells.
MAX_BIT_WIDTH = 256
MAX_OUTCOMES = 256
MAX_WEIGHT_BITS = 256


@dataclass(frozen=True)
class CategoricalMap:
    """Validated, immutable floor/largest-remainder categorical partition.

    ``proxy_weights`` must be a nonempty plain list or tuple of plain ``int``
    or ``Fraction`` values.  They must be nonnegative and sum *exactly* to one;
    no normalization or conversion from floating point is performed.  Each
    reduced numerator and denominator may have at most MAX_WEIGHT_BITS bits.
    Outcome indices are the original positions, including zero-count outcomes.

    ``bit_width`` must be a plain integer in [0, MAX_BIT_WIDTH].  At width zero
    the sole admissible word is zero.  Tied fractional remainders are resolved
    in ascending outcome-index order.  Public derived fields cannot be supplied
    to the constructor.  Normal construction always computes its certificate.
    """

    proxy_weights: Sequence[Union[int, Fraction]]
    bit_width: int
    total_cells: int = field(init=False)
    cell_counts: Tuple[int, ...] = field(init=False)
    boundaries: Tuple[int, ...] = field(init=False)
    rounding_tv: Fraction = field(init=False)

    def __post_init__(self) -> None:
        if type(self.bit_width) is not int:
            raise TypeError("bit_width must be a plain integer")
        if not 0 <= self.bit_width <= MAX_BIT_WIDTH:
            raise ValueError("bit_width is outside the supported resource bound")
        if type(self.proxy_weights) not in (list, tuple):
            raise TypeError("proxy_weights must be a plain list or tuple")
        if not 1 <= len(self.proxy_weights) <= MAX_OUTCOMES:
            raise ValueError("proxy_weights must contain 1..MAX_OUTCOMES entries")

        weights = []
        for value in self.proxy_weights:
            if type(value) not in (int, Fraction):
                raise TypeError("each weight must be a plain int or Fraction")
            if value < 0:
                raise ValueError("weights must be nonnegative")
            numerator = value if type(value) is int else value.numerator
            denominator = 1 if type(value) is int else value.denominator
            if (numerator.bit_length() > MAX_WEIGHT_BITS or
                    denominator.bit_length() > MAX_WEIGHT_BITS):
                raise ValueError("weight numerator or denominator exceeds resource bound")
            weights.append(Fraction(numerator, denominator))
        weights = tuple(weights)
        if sum(weights, Fraction(0)) != 1:
            raise ValueError("weights must sum exactly to one")

        total = 1 << self.bit_width
        counts = []
        remainders = []
        for weight in weights:
            count, remainder = divmod(total * weight.numerator, weight.denominator)
            counts.append(count)
            remainders.append(Fraction(remainder, weight.denominator))
        extra = total - sum(counts)
        # Exact normalization makes extra an integer in [0, len(weights)).
        order = sorted(range(len(weights)), key=lambda i: (-remainders[i], i))
        for index in order[:extra]:
            counts[index] += 1

        boundaries = [0]
        for count in counts:
            boundaries.append(boundaries[-1] + count)
        rounding_tv = sum(
            (abs(Fraction(count, total) - weight)
             for count, weight in zip(counts, weights)), Fraction(0)
        ) / 2

        object.__setattr__(self, "proxy_weights", weights)
        object.__setattr__(self, "total_cells", total)
        object.__setattr__(self, "cell_counts", tuple(counts))
        object.__setattr__(self, "boundaries", tuple(boundaries))
        object.__setattr__(self, "rounding_tv", rounding_tv)

    def map_word(self, word: int) -> int:
        """Map one supplied b-bit integer to its outcome; never draw or retry.

        Intervals are [boundaries[i], boundaries[i+1]).  Empty intervals are
        skipped by right bisection.  The return value is an outcome index,
        not a randomly generated value.  Booleans and integer subclasses are
        rejected, as are words outside [0, total_cells).
        """
        if type(word) is not int:
            raise TypeError("word must be a plain integer")
        if not 0 <= word < self.total_cells:
            raise ValueError("word must lie in [0, total_cells)")
        return bisect_right(self.boundaries, word) - 1
