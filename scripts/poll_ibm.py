#!/usr/bin/env python3
"""Scheduled IBM Quantum calibration poll (run daily by launchd).

Appends one BackendProperties snapshot to the drift-series store, so the
decoherence-drift test accumulates data over time. The IBM token is read from
~/.ibm_quantum_token (or IBM_QUANTUM_TOKEN) by load_token() — never hardcoded.

Invoked by ~/Library/LaunchAgents/com.det.ibm-poll.plist using the project's
.venv Python (which has qiskit-ibm-runtime installed).
"""

import sys

ROOT = "/Volumes/AI_DATA/development/det_8_qwen"
sys.path.insert(0, ROOT)

from det8.applied_physics.ibm_ingest import poll_and_append  # noqa: E402

INSTANCE = (
    "crn:v1:bluemix:public:quantum-computing:us-east:"
    "a/814d555cd09d4953abb06cba094a604e:3bfa1c87-7663-40e8-bf28-d10695719926::"
)
BACKEND = "ibm_fez"
STORE = f"{ROOT}/det8/data/ibm_snapshots.json"


def main() -> int:
    try:
        r = poll_and_append(BACKEND, instance=INSTANCE, store_path=STORE)
        status = "skipped (no new calibration)" if r["skipped"] else "appended"
        print(f"[{status}] {r['n_snapshots']} snapshots total; "
              f"last_update={r['last_update']}")
        return 0
    except Exception as e:  # log-and-continue so a bad day doesn't break the job
        print(f"[error] {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
