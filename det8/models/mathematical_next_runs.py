"""Combined entry point for the validated Riemann and Collatz frontier runs."""

from __future__ import annotations

import json

from det8.models.examples.collatz_frontier_extension import (
    run_collatz_frontier_extension,
)
from det8.models.examples.riemann_validated_extension import (
    run_validated_riemann_extension,
)


NEXT_RUN_PROOF_BOUNDARY = (
    "The Riemann result is a two-resolution numerical count audit rather than "
    "interval proof, and the Collatz result ends at its explicit integer frontier."
)


def run_mathematical_next_runs() -> dict[str, object]:
    return {
        "method": "validated bounded mathematical next runs",
        "proof_boundary": NEXT_RUN_PROOF_BOUNDARY,
        "runs": {
            "riemann_validated_extension": run_validated_riemann_extension(),
            "collatz_frontier_extension": run_collatz_frontier_extension(),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_mathematical_next_runs(), indent=2))
