"""Runnable entry point for the Relational Experimental Calculus (REC).

REC combines experiment-agnostic relational tomography, adaptive scheduling,
and conservation closure.  Exodus is retained as one demanding vector-response
fixture; a thermal-drift fixture demonstrates that the calculus is reusable.
"""

from __future__ import annotations

import json

from det8.models.examples.exodus_tomography import run_exodus_ret_fixture
from det8.models.examples.neutron_lifetime import run_neutron_lifetime_fixture
from det8.models.examples.thermal_drift_tomography import run_thermal_ret_fixture
from det8.models.relational_closure import ConservedTransfer, closure_ladder
from det8.models.relational_scheduler import RG1
from det8.models.relational_tomography import POSTERIOR_IS_NOT_ONTOLOGY


def run_relational_experimental_calculus() -> dict[str, object]:
    transfers = [
        ConservedTransfer(
            "instrument",
            "environment",
            (18.242e-6, 0.0, -454.0e-6),
            "instrument-environment transfer",
        )
    ]
    closure = closure_ladder(
        transfers,
        (("instrument",), ("instrument", "environment")),
        tolerance=1.0e-12,
    )
    return {
        "method": "Relational Experimental Calculus",
        "rg1": RG1,
        "posterior_warning": POSTERIOR_IS_NOT_ONTOLOGY,
        "architecture": (
            "family identification",
            "endpoint-existence testing",
            "parameter characterization",
            "conservation closure",
        ),
        "generic_closure_demo": closure,
        "fixtures": {
            "exodus": run_exodus_ret_fixture(),
            "neutron_lifetime": run_neutron_lifetime_fixture(),
            "thermal_drift": run_thermal_ret_fixture(),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_relational_experimental_calculus(), indent=2))
