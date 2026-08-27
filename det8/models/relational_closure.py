"""Experiment-agnostic conserved-transfer closure for RET regimes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence, Tuple


Vector = Tuple[float, ...]


@dataclass(frozen=True)
class ConservedTransfer:
    endpoint_a: str
    endpoint_b: str
    on_a: Vector
    label: str = "transfer"

    @property
    def on_b(self) -> Vector:
        return tuple(-value for value in self.on_a)


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(sum(value * value for value in vector))


def regime_residual(
    transfers: Sequence[ConservedTransfer],
    included_endpoints: Sequence[str],
) -> Vector:
    included = set(included_endpoints)
    if not transfers:
        return ()
    dimension = len(transfers[0].on_a)
    residual = [0.0] * dimension
    for transfer in transfers:
        if len(transfer.on_a) != dimension:
            raise ValueError("all transfers must share one vector dimension")
        if transfer.endpoint_a in included:
            for axis in range(dimension):
                residual[axis] += transfer.on_a[axis]
        if transfer.endpoint_b in included:
            for axis in range(dimension):
                residual[axis] += transfer.on_b[axis]
    return tuple(residual)


def closure_ladder(
    transfers: Sequence[ConservedTransfer],
    candidate_cuts: Sequence[Sequence[str]],
    *,
    tolerance: float = 1.0e-9,
) -> dict[str, object]:
    if tolerance < 0.0:
        raise ValueError("closure tolerance cannot be negative")
    rows = []
    first_closed = None
    for index, cut in enumerate(candidate_cuts):
        residual = regime_residual(transfers, cut)
        norm = _norm(residual)
        closed = norm <= tolerance
        if closed and first_closed is None:
            first_closed = index
        rows.append(
            {
                "cut_index": index,
                "included_endpoints": tuple(cut),
                "residual": residual,
                "residual_norm": norm,
                "closed": closed,
            }
        )
    return {
        "tolerance": tolerance,
        "first_closed_cut_index": first_closed,
        "model_failure": first_closed is None,
        "cuts": rows,
    }
