"""Combined, proof-governed Riemann and Collatz search entry point."""

from __future__ import annotations

import json

from det8.models.examples.collatz_search import run_collatz_search
from det8.models.examples.riemann_zero_search import run_riemann_zero_search


MATHEMATICAL_SEARCH_BOUNDARY = (
    "These runs automate bounded computation and adaptive model comparison. "
    "They can find finite-record structure or a concrete anomaly, but a finite "
    "record is not promoted to a proof of a universal mathematical conjecture."
)


def run_mathematical_searches() -> dict[str, object]:
    return {
        "method": "proof-governed RET mathematical searches",
        "proof_boundary": MATHEMATICAL_SEARCH_BOUNDARY,
        "searches": {
            "riemann": run_riemann_zero_search(),
            "collatz": run_collatz_search(),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_mathematical_searches(), indent=2))
