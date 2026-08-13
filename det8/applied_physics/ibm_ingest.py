"""
DET v8.0 — Applied Physics: IBM Quantum Calibration Ingest

Fetches qubit T1/T2 calibration data from IBM Quantum and maps it to DET κ
inputs for the decoherence-drift test (Test 2).

SECURITY — the API token is NEVER pasted into code or chat. It is read from:

  1. the environment variable  IBM_QUANTUM_TOKEN,  or
  2. the file  ~/.ibm_quantum_token   (one line, the token only; chmod 600).

Set it up yourself (once):

    export IBM_QUANTUM_TOKEN='your-token-here'     # or
    printf '%s' 'your-token-here' > ~/.ibm_quantum_token && chmod 600 ~/.ibm_quantum_token

Two fetch backends:

  1. qiskit-ibm-runtime (preferred, official SDK):  pip install qiskit-ibm-runtime
  2. REST (stdlib urllib, no dependency): direct API call.

The decoherence-drift test needs the TIME SERIES of T1/T2 per qubit. IBM
publishes the current snapshot; the drift series is built by polling over time
(or from the calibration-history export). `generate_ibm_qubit` (in ingest.py)
provides a format-identical synthetic surrogate for offline development.
"""

from __future__ import annotations

import json
import os
import urllib.request


TOKEN_ENV = "IBM_QUANTUM_TOKEN"
TOKEN_FILE = os.path.expanduser("~/.ibm_quantum_token")
DEFAULT_BACKEND = "ibm_brisbane"


def load_token() -> str | None:
    """Read the IBM Quantum token from the env var, then the token file."""
    tok = os.environ.get(TOKEN_ENV)
    if tok:
        return tok
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, encoding="utf-8") as f:
            tok = f.read().strip()
        if tok:
            return tok
    return None


def fetch_properties_qiskit(
    backend_name: str = DEFAULT_BACKEND,
    token: str | None = None,
    instance: str | None = None,
) -> dict:
    """Fetch BackendProperties via the qiskit-ibm-runtime SDK.

    `instance` is the account's instance CRN or name (the modern IBM Quantum
    Platform replaced hub/group/project with CRNs). If None, the account's
    default/free instance is used.

    Returns a JSON-like dict {backend_name, last_update_date, qubits: [[...]]}.
    """
    from qiskit_ibm_runtime import QiskitRuntimeService  # optional dependency

    tok = token or load_token()
    if not tok:
        raise RuntimeError("no IBM token (set IBM_QUANTUM_TOKEN or ~/.ibm_quantum_token)")
    kwargs = {"channel": "ibm_quantum_platform", "token": tok}
    if instance:
        kwargs["instance"] = instance
    service = QiskitRuntimeService(**kwargs)
    backend = service.backend(backend_name)
    props = backend.properties()
    qubits = []
    for q in props.qubits:
        qubits.append([
            {"name": "T1", "value": q.t1, "unit": "us", "date": getattr(q, "date", "")},
            {"name": "T2", "value": q.t2, "unit": "us", "date": getattr(q, "date", "")},
            {"name": "frequency", "value": q.frequency, "unit": "GHz",
             "date": getattr(q, "date", "")},
        ])
    return {
        "backend_name": backend_name,
        "last_update_date": str(getattr(props, "last_update_date", "")),
        "qubits": qubits,
    }


def fetch_properties_rest(backend_name: str = DEFAULT_BACKEND, token: str | None = None) -> dict:
    """Fetch BackendProperties via the REST API (stdlib, no dependency).

    Uses the legacy IBM Quantum API endpoint; the token goes in the
    x-access-token header. (Endpoint may need updating as IBM migrates.)
    """
    tok = token or load_token()
    if not tok:
        raise RuntimeError("no IBM token (set IBM_QUANTUM_TOKEN or ~/.ibm_quantum_token)")
    url = f"https://api.quantum-computing.ibm.com/api/Backends/{backend_name}/properties"
    req = urllib.request.Request(url, headers={"x-access-token": tok})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return _normalize_properties(data)


def _normalize_properties(raw: dict) -> dict:
    """Normalize a raw IBM properties payload to the {qubits: [...]} shape."""
    qubits = raw.get("qubits", [])
    if qubits and isinstance(qubits[0], dict):
        # Legacy shape: qubits = [{name, value, unit, date}, ...] for one qubit.
        return {
            "backend_name": raw.get("backend_name", ""),
            "last_update_date": raw.get("last_update_date", ""),
            "qubits": [qubits],  # single-qubit payload → list of one.
        }
    return {
        "backend_name": raw.get("backend_name", ""),
        "last_update_date": raw.get("last_update_date", ""),
        "qubits": qubits,
    }


def fetch_properties(
    backend_name: str = DEFAULT_BACKEND,
    token: str | None = None,
    instance: str | None = None,
) -> dict:
    """Fetch properties via qiskit-ibm-runtime, falling back to REST."""
    try:
        return fetch_properties_qiskit(backend_name, token, instance)
    except (ImportError, ModuleNotFoundError):
        return fetch_properties_rest(backend_name, token)


def ibm_to_kappa_inputs(properties: dict) -> dict:
    """Map IBM BackendProperties to DET κ inputs.

    observable = T1 per qubit (µs; higher κ → more TLS drag → shorter T1).
    T_t = chip temperature (15 mK, constant). flux_t = 0 (no radiation; the
    "damage" is TLS spectral diffusion, not radiation).
    """
    qubits = properties.get("qubits", [])
    t, T_t, flux_t, observable = [], [], [], []
    for i, qprops in enumerate(qubits):
        rec = {}
        for p in qprops:
            if isinstance(p, dict) and p.get("name") in ("T1", "T2"):
                try:
                    rec[p["name"]] = float(p["value"])
                except (TypeError, ValueError):
                    pass
        if "T1" in rec:
            t.append(i)
            T_t.append(0.015)   # 15 mK.
            flux_t.append(0.0)
            observable.append(rec["T1"])
    return {"t": t, "T_t": T_t, "flux_t": flux_t, "observable": observable}


def qubit_drift_series(snapshots: list[dict], qubit_index: int = 0) -> list[dict]:
    """Build a qubit's T1 drift series from a LIST of time-ordered snapshots.

    Each snapshot is a properties dict (from fetch_properties at a different
    time). Returns [{date, T1, T2}] for the given qubit, sorted by date.
    """
    series = []
    for snap in snapshots:
        qubits = snap.get("qubits", [])
        if qubit_index < len(qubits):
            rec = {p["name"]: float(p["value"]) for p in qubits[qubit_index]
                   if isinstance(p, dict) and p.get("name") in ("T1", "T2")}
            rec["date"] = snap.get("last_update_date", "")
            series.append(rec)
    series.sort(key=lambda r: r.get("date", ""))
    return series


def run_ibm_ingest(
    backend_name: str = DEFAULT_BACKEND,
    token: str | None = None,
    instance: str | None = None,
) -> dict:
    """End-to-end: fetch properties and map to DET κ inputs."""
    props = fetch_properties(backend_name, token, instance)
    inputs = ibm_to_kappa_inputs(props)
    n_qubits = len(inputs["t"])
    return {
        "backend": backend_name,
        "last_update": props.get("last_update_date", ""),
        "n_qubits_with_t1": n_qubits,
        "inputs": inputs,
        "interpretation": (
            f"{n_qubits} qubits with T1 calibration. T1 is the observable for the "
            f"decoherence-drift test; the drift series needs repeated snapshots "
            f"(poll daily/weekly, or use the calibration-history export)."
        ),
    }
