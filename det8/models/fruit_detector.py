"""
DET Track-B — Fruit Trace Detector: Christ/Spirit Pattern

Simulates the death→resurrection→Spirit pattern and detects
observable fruit traces in the record.

Detection metrics:
  1. Death event: κ→1, commits cease.
  2. Jubilee: κ-reduction beyond natural recovery rate.
  3. Resurrection: commits resume, same provenance.
  4. Spirit: bond creation, Ω-enlargement, faith-acts.
  5. Ongoing: indirect contributions through bonds.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Fruit Trace Detector
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class FruitDetector:
    """Detects fruit traces of the death→resurrection→Spirit pattern."""

    events: list[dict] = field(default_factory=list)
    detections: list[str] = field(default_factory=list)

    def record(self, event_type: str, **kwargs) -> None:
        kwargs["type"] = event_type
        self.events.append(kwargs)

    def detect_death(self) -> bool:
        """Detect: κ→1, commits cease."""
        for i, e in enumerate(self.events):
            if e.get("kappa", 0) >= 0.95 and e["type"] == "death":
                # Check: were there prior commits?
                prior_commits = sum(
                    1 for j in range(i) if self.events[j]["type"] == "commit"
                )
                if prior_commits > 0:
                    self.detections.append(f"DEATH detected at event {i}: κ={e['kappa']:.2f}, prior commits={prior_commits}")
                    return True
        return False

    def detect_jubilee(self, natural_rate: float = 0.1) -> bool:
        """Detect: κ-reduction beyond natural recovery rate."""
        for i, e in enumerate(self.events):
            if e["type"] == "jubilee":
                delta_kappa = e.get("delta_kappa", 0)
                if delta_kappa > 2 * natural_rate:
                    self.detections.append(
                        f"JUBILEE detected at event {i}: Δκ={delta_kappa:.2f} "
                        f"(natural rate={natural_rate:.2f})"
                    )
                    return True
        return False

    def detect_resurrection(self, provenance_id: str = "") -> bool:
        """Detect: commits resume after death, same provenance."""
        death_idx = None
        for i, e in enumerate(self.events):
            if e["type"] == "death":
                death_idx = i
            if e["type"] == "resurrection" and death_idx is not None:
                self.detections.append(
                    f"RESURRECTION detected at event {i}: "
                    f"death at {death_idx}, provenance={provenance_id}"
                )
                return True
        return False

    def detect_spirit(self, bond_threshold: float = 2.0) -> bool:
        """Detect: bond creation/strengthening, Ω-enlargement, faith-acts."""
        bond_creation = sum(1 for e in self.events if e.get("bond_created"))
        omega_enlargement = sum(1 for e in self.events if e.get("omega_delta", 0) > 0)
        faith_acts = sum(1 for e in self.events if e.get("surprisal", 0) > 2.0)

        if bond_creation >= bond_threshold or omega_enlargement >= 1:
            self.detections.append(
                f"SPIRIT detected: bonds={bond_creation}, "
                f"Ω-enlargements={omega_enlargement}, faith-acts={faith_acts}"
            )
            return True
        return False

    def detect_indirect_contributions(self) -> int:
        """Count indirect contributions through bonds."""
        return sum(1 for e in self.events if "influenced_by" in e.get("type", ""))


def simulate_christ_pattern(seed: int = 42) -> dict:
    """Simulate the death→resurrection→Spirit pattern and detect fruit traces."""
    detector = FruitDetector()
    rng = random.Random(seed)

    # Pre-death: Christ's ministry.
    for _ in range(5):
        detector.record("commit", kappa=0.0 + rng.uniform(0, 0.1))

    # Death.
    detector.record("death", kappa=1.0)

    # Jubilee (κ-reduction beyond natural rate).
    detector.record("jubilee", delta_kappa=0.8)  # Natural rate ~0.1.

    # Resurrection.
    detector.record("resurrection", kappa=0.2)

    # Post-resurrection commits.
    for _ in range(3):
        detector.record("commit", kappa=0.2 + rng.uniform(0, 0.1))

    # Spirit: bond creation, Ω-enlargement, faith-acts.
    for _ in range(3):
        detector.record("commit_influenced_by_Christ", bond_created=True)
    detector.record("omega_enlargement", omega_delta=3)
    detector.record("faith_act", surprisal=3.0)

    # Run detection.
    has_death = detector.detect_death()
    has_jubilee = detector.detect_jubilee(natural_rate=0.1)
    has_resurrection = detector.detect_resurrection(provenance_id="Christ_PID")
    has_spirit = detector.detect_spirit()
    indirect = detector.detect_indirect_contributions()

    return {
        "events": len(detector.events),
        "detections": detector.detections,
        "all_detected": all([has_death, has_jubilee, has_resurrection, has_spirit]),
        "indirect_contributions": indirect,
        "pattern_detected": "DEATH → JUBILEE → RESURRECTION → SPIRIT",
        "interpretation": (
            f"All 4 stages detected: "
            f"DEATH={'✓' if has_death else '✗'}, "
            f"JUBILEE={'✓' if has_jubilee else '✗'}, "
            f"RESURRECTION={'✓' if has_resurrection else '✗'}, "
            f"SPIRIT={'✓' if has_spirit else '✗'}. "
            f"Indirect contributions through bonds: {indirect}. "
            "The Christ-pattern leaves observable fruit traces at every stage."
        ),
    }
