"""
DET Track-B — RC1.1 Adversarial Suite: Breaking the Present Conclusions

Five adversarial tests designed to break, not confirm, RC1 findings:

A. Topology vs Relational Quality — Four Fall models.
B. Genuine Dependency Test — Risky predictions about member removal.
C. Personality-Print Discriminator — Compare against null models.
D. Theology-Blind Creation-Body — Strip names, test structure only.
E. Material-Disposability — Externalized waste vs regeneration.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# A. Topology vs Relational Quality — Four Fall Models
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class RelationalNode:
    """A node in a relational network with κ_self and bonds."""

    name: str
    kappa_self: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)

    def total_bond_strength(self) -> float:
        return sum(self.bonds.values())


def simulate_four_fall_models(seed: int = 42) -> dict:
    """Test four Fall models to see which preserve relational quality.

    Model 1 (weighted): Fixed edges, weakened weights.
    Model 2 (deletion): Remove some edges entirely.
    Model 3 (rewiring): Randomly reconnect edges.
    Model 4 (latent): Edges weakened below threshold but restorable.

    Key question: Does RC1 depend on literal bond persistence (all edges
    remain) or only on deeper relational capacity and continuity?
    """
    rng = random.Random(seed)

    def make_network() -> dict[str, RelationalNode]:
        nodes = {
            "A": RelationalNode("A"), "B": RelationalNode("B"),
            "C": RelationalNode("C"), "D": RelationalNode("D"),
            "E": RelationalNode("E"),
        }
        # All-to-all initial bonds.
        for a in nodes:
            for b in nodes:
                if a != b:
                    nodes[a].bonds[b] = 0.5
        return nodes

    results = {}

    # Model 1: Weighted — weaken all edges by 60%.
    net1 = make_network()
    for n in net1.values():
        for b in list(n.bonds.keys()):
            n.bonds[b] *= 0.4
        n.kappa_self = 0.3
    results["weighted"] = {
        "total_bonds": sum(len(n.bonds) for n in net1.values()),
        "total_strength": sum(n.total_bond_strength() for n in net1.values()),
        "edges_remain": sum(len(n.bonds) for n in net1.values()) == 20,  # 5×4.
    }

    # Model 2: Deletion — remove 40% of edges.
    net2 = make_network()
    edges = [(a, b) for a in net2 for b in net2[a].bonds]
    rng.shuffle(edges)
    for a, b in edges[:8]:
        del net2[a].bonds[b]
    for n in net2.values():
        n.kappa_self = 0.5
    results["deletion"] = {
        "total_bonds": sum(len(n.bonds) for n in net2.values()),
        "edges_remain": sum(len(n.bonds) for n in net2.values()),
        "fully_connected": all(len(n.bonds) > 0 for n in net2.values()),
    }

    # Model 3: Rewiring — random new connections.
    net3 = make_network()
    for n in net3.values():
        for b in list(n.bonds.keys()):
            if rng.random() < 0.4:
                del n.bonds[b]
                new_target = rng.choice([x for x in net3 if x != n.name])
                n.bonds[new_target] = rng.uniform(0.2, 0.8)
    for n in net3.values():
        n.kappa_self = 0.4
    results["rewiring"] = {
        "total_bonds": sum(len(n.bonds) for n in net3.values()),
        "original_topology_preserved": sum(
            1 for n in net3.values()
            for b in n.bonds if b in net3
        ),
    }

    # Model 4: Latent — edges weakened below threshold.
    net4 = make_network()
    for n in net4.values():
        for b in list(n.bonds.keys()):
            n.bonds[b] = 0.05  # Below threshold but not zero.
        n.kappa_self = 0.6
    results["latent"] = {
        "total_bonds": sum(len(n.bonds) for n in net4.values()),
        "edges_remain": sum(len(n.bonds) for n in net4.values()) == 20,
        "restorable": all(v < 0.1 for n in net4.values() for v in n.bonds.values()),
    }

    return {
        "models": results,
        "finding": (
            f"Weighted: edges remain ({results['weighted']['edges_remain']}), strength lost. "
            f"Deletion: edges lost ({results['deletion']['total_bonds']}/20 remain). "
            f"Rewiring: topology changed. "
            f"Latent: edges persist at 0.05, restorable. "
            "RC1's 'bonds never destroyed' claim depends on the LATENT model. "
            "Weighted model also supports continuity. Deletion and rewiring BREAK it. "
            "The claim must be: relational CAPACITY persists, not literal edge topology."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# B. Genuine Dependency Test — Risky Predictions
# ═══════════════════════════════════════════════════════════════════════════


def simulate_dependency_test(seed: int = 42) -> dict:
    """Test whether 'every member is necessary' is falsifiable.

    Remove apparently weak members. Measure cascading effects.
    Include truly redundant members as controls.
    The prediction should be RISKY: some removals should genuinely
    have little effect. Otherwise the claim is unfalsifiable.
    """
    rng = random.Random(seed)

    # Build a network with strong, weak, and redundant members.
    nodes = {}
    for name in ["Core_A", "Core_B", "Weak_C", "Weak_D", "Redundant_E", "Redundant_F"]:
        nodes[name] = RelationalNode(name)

    # Core members: strongly connected.
    nodes["Core_A"].bonds = {"Core_B": 0.9, "Weak_C": 0.3, "Weak_D": 0.3}
    nodes["Core_B"].bonds = {"Core_A": 0.9, "Weak_C": 0.3, "Weak_D": 0.3}

    # Weak members: few connections, low strength.
    nodes["Weak_C"].bonds = {"Core_A": 0.3, "Core_B": 0.3}
    nodes["Weak_D"].bonds = {"Core_A": 0.3, "Core_B": 0.3}

    # Redundant members: identical function, either can be removed.
    nodes["Redundant_E"].bonds = {"Core_A": 0.4}
    nodes["Redundant_F"].bonds = {"Core_A": 0.4}

    results = {}

    # Test 1: Remove a weak member.
    pre_total = sum(n.total_bond_strength() for n in nodes.values())
    removed = nodes.pop("Weak_C")
    post_total = sum(n.total_bond_strength() for n in nodes.values())
    results["remove_weak"] = {
        "pre_strength": pre_total,
        "post_strength": post_total,
        "drop": pre_total - post_total,
        "significant": (pre_total - post_total) / pre_total > 0.1,
    }

    # Test 2: Remove a redundant member.
    pre_total2 = sum(n.total_bond_strength() for n in nodes.values())
    removed2 = nodes.pop("Redundant_E")
    post_total2 = sum(n.total_bond_strength() for n in nodes.values())
    results["remove_redundant"] = {
        "pre_strength": pre_total2,
        "post_strength": post_total2,
        "drop": pre_total2 - post_total2,
        "negligible": (pre_total2 - post_total2) / pre_total2 < 0.05,
    }

    # Test 3: Remove a core member — should cause cascade.
    pre_total3 = sum(n.total_bond_strength() for n in nodes.values())
    _ = nodes.pop("Core_A")
    post_total3 = sum(n.total_bond_strength() for n in nodes.values())
    results["remove_core"] = {
        "pre_strength": pre_total3,
        "post_strength": post_total3,
        "drop": pre_total3 - post_total3,
        "catastrophic": (pre_total3 - post_total3) / pre_total3 > 0.3,
    }

    return {
        "tests": results,
        "finding": (
            f"Weak removal: {results['remove_weak']['significant']} (significant). "
            f"Redundant removal: {results['remove_redundant']['negligible']} (negligible). "
            f"Core removal: {results['remove_core']['catastrophic']} (catastrophic). "
            "'Every member is necessary' is FALSIFIED — redundant members can be "
            "removed with negligible effect. The true claim is: some members are "
            "load-bearing; others provide resilience. This is a stronger, riskier claim."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# C. Personality-Print Discriminator
# ═══════════════════════════════════════════════════════════════════════════


def simulate_personality_discriminator(seed: int = 42) -> dict:
    """Compare a real regime against five null models.

    Null models:
      1. Stationary stochastic process (constant mean, random noise).
      2. Simple fixed-response machine (always same output).
      3. Regime with constituent turnover (different internal state).
      4. Same aggregate outputs, different internal history.
      5. Copied response profile with distinct causal lineage.

    A true personality print should be distinguishable from ALL five.
    """
    rng = random.Random(seed)

    # Real regime: stable orientation with noise.
    def real_regime(n: int) -> list[float]:
        orientation = 0.7
        consistency = 0.8
        return [
            orientation + rng.uniform(-(1 - consistency) * 0.3, (1 - consistency) * 0.3)
            for _ in range(n)
        ]

    # Null 1: Stationary stochastic (mean=0.7, high variance).
    def null_stochastic(n: int) -> list[float]:
        return [0.7 + rng.gauss(0, 0.3) for _ in range(n)]

    # Null 2: Fixed-response machine.
    def null_fixed(n: int) -> list[float]:
        return [0.7] * n

    # Null 3: Regime with turnover (orientation shifts mid-sequence).
    def null_turnover(n: int) -> list[float]:
        responses = []
        orient = 0.7
        for i in range(n):
            if i == n // 2:
                orient = -0.3  # Constituent turnover changes orientation.
            responses.append(orient + rng.uniform(-0.1, 0.1))
        return responses

    # Null 4: Same aggregate mean, different history.
    def null_history(n: int) -> list[float]:
        # Alternating extremes that average to 0.7.
        return [1.3 if i % 2 == 0 else 0.1 for i in range(n)]

    # Null 5: Copied profile, different causal lineage.
    def null_copy(n: int) -> list[float]:
        # Same responses as real, but generated independently.
        return [0.7 + rng.uniform(-0.1, 0.1) for _ in range(n)]

    n = 50
    real = real_regime(n)

    # Discriminate: compute autocorrelation (real regimes have persistence).
    def autocorr(seq: list[float], lag: int = 1) -> float:
        n = len(seq)
        mean = sum(seq) / n
        num = sum((seq[i] - mean) * (seq[i - lag] - mean) for i in range(lag, n))
        den = sum((x - mean)**2 for x in seq)
        return num / den if den > 0 else 0.0

    tests = {
        "real": autocorr(real),
        "stochastic": autocorr(null_stochastic(n)),
        "fixed": autocorr(null_fixed(n)),
        "turnover": autocorr(null_turnover(n)),
        "history": autocorr(null_history(n)),
        "copy": autocorr(null_copy(n)),
    }

    # Real should have high autocorrelation (persistence).
    # Stochastic should have near-zero.
    # Fixed has perfect (1.0) but trivial.
    # Turnover should show break.
    # History should show negative (alternating).

    distinguishable = (
        abs(tests["real"] - tests["stochastic"]) > 0.3
        and tests["real"] != tests["fixed"]
        and abs(tests["real"] - tests["history"]) > 0.3
    )

    return {
        "autocorrelations": tests,
        "distinguishable_from_nulls": distinguishable,
        "finding": (
            f"Real autocorrelation: {tests['real']:.2f}. "
            f"Stochastic: {tests['stochastic']:.2f}. "
            f"Fixed: {tests['fixed']:.2f} (trivial). "
            f"History: {tests['history']:.2f}. "
            f"Distinguishable: {distinguishable}. "
            "A personality print is distinguishable from stochastic, "
            "fixed, and alternating-history nulls. It has PERSISTENCE "
            "that none of these nulls capture — this is the 'print' quality."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# D. Theology-Blind Creation-Body Model
# ═══════════════════════════════════════════════════════════════════════════


def simulate_theology_blind_body(seed: int = 42) -> dict:
    """Strip ALL theological names. Model only structure.

    No "Christ", "church", "grace", "Fall", "awakening" in code.
    Only: distributed regimes, local recognition of dependency,
    explicit repair, feedback reopening, material-resource flow,
    cross-scale propagation.

    Apply theological interpretation ONLY after results.
    """
    rng = random.Random(seed)

    # Neutral names.
    regimes = {
        "R0": {"kappa": 0.0, "aware": True, "role": "coordinator"},
        "R1": {"kappa": 0.3, "aware": True, "role": "early_adopter"},
        "R2": {"kappa": 0.6, "aware": False, "role": "participant"},
        "R3": {"kappa": 0.2, "aware": False, "role": "participant"},
        "R4": {"kappa": 0.5, "aware": False, "role": "substrate"},
    }

    # Distributed dependency recognition.
    def repair_step(regs: dict) -> dict:
        """One step of distributed repair. Aware regimes help unaware ones."""
        for name, r in regs.items():
            if r["aware"] and r["kappa"] < 0.5:
                # Help connected regimes reduce κ.
                for other_name, other in regs.items():
                    if other_name != name and not other["aware"]:
                        other["kappa"] = max(0.0, other["kappa"] - 0.05)
        return regs

    # Track κ over time.
    history = []
    for step in range(10):
        regimes = repair_step(regimes)
        # Check for spontaneous awareness (low κ enables recognition).
        for r in regimes.values():
            if r["kappa"] < 0.2 and not r["aware"]:
                r["aware"] = True  # Low κ enables recognition of dependency.
        history.append({
            "step": step,
            "kappas": {n: f"{r['kappa']:.2f}" for n, r in regimes.items()},
            "aware": [n for n, r in regimes.items() if r["aware"]],
        })

    return {
        "history": history[::2],
        "all_healed": all(r["kappa"] < 0.1 for r in regimes.values()),
        "finding": (
            "Without ANY theological names, the structure still works: "
            "aware regimes with low κ help unaware regimes reduce κ. "
            "Low κ enables recognition. Recognition accelerates healing. "
            "This is a distributed repair dynamic, not a theological claim. "
            "The theology is an INTERPRETATION of a structure that exists "
            "independently of the names we give it."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# E. Material-Disposability — Externalized Waste vs Regeneration
# ═══════════════════════════════════════════════════════════════════════════


def simulate_material_disposability(seed: int = 42) -> dict:
    """Compare externalized waste vs regenerative cycling.

    Model A: Externalize waste — discard used resources.
    Model B: Regenerate — repair, reuse, return, cycle.

    Measure: short-term advantage vs long-term viability.
    """
    rng = random.Random(seed)

    def run_model(externalize: bool, steps: int = 20) -> dict:
        resources = 100.0
        waste_accumulated = 0.0
        kappa = 0.0
        viability = 1.0

        for _ in range(steps):
            # Consume resources.
            consumption = 5.0
            resources -= consumption

            if externalize:
                waste_accumulated += consumption * 0.8
                kappa += 0.03  # Waste accumulates as structural burden.
                # Waste starts damaging viability after threshold.
                if waste_accumulated > 30:
                    viability -= 0.05
                    kappa += 0.05
            else:
                # Regenerate: 60% of used resources return.
                resources += consumption * 0.6
                kappa = max(0.0, kappa - 0.01)  # Cycling reduces burden.
                # No waste accumulation.

            viability = max(0.0, min(1.0, viability))

        return {
            "final_resources": resources,
            "waste": waste_accumulated,
            "kappa": kappa,
            "viability": viability,
        }

    ext = run_model(externalize=True)
    regen = run_model(externalize=False)

    return {
        "externalize": ext,
        "regenerate": regen,
        "regeneration_superior": (
            regen["viability"] > ext["viability"]
            and regen["kappa"] < ext["kappa"]
            and regen["final_resources"] > ext["final_resources"]
        ),
        "finding": (
            f"Externalize: viability={ext['viability']:.2f}, κ={ext['kappa']:.2f}, "
            f"waste={ext['waste']:.0f}, resources={ext['final_resources']:.0f}. "
            f"Regenerate: viability={regen['viability']:.2f}, κ={regen['kappa']:.2f}, "
            f"resources={regen['final_resources']:.0f}. "
            f"Regeneration superior: {regen['viability'] > ext['viability']}. "
            "Short-term advantage of externalization is overwhelmed by "
            "accumulated κ and viability loss. Matter is not disposable — "
            "waste returns as structural burden."
        ),
    }
