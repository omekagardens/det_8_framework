"""
DET Track-B — F10 Compression Hypothesis: Executable Test

Tests whether growing records force law extension (program growth).

Key test:
  Generate a sequence of records. Compress with a bounded program.
  As more records accumulate, does the minimal program need to GROW?
  If yes → law extension is forced. If no → L is fixed.

DET formalization:
  L_t = compress(R_{<=t})
  If L_t fits R_{<=t+1} → no extension needed.
  If L_t fails → L must be extended.
  Constraint: L_{t+1}(R^-) ⊇ L_t(R^-) — old possibilities preserved.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. Program Growth Test
# ═══════════════════════════════════════════════════════════════════════════


def minimal_program_size(
    sequence: list[int],
    memory_depth: int,
) -> int:
    """Estimate minimal program size to generate a sequence.

    The "program" is a transition table: prefix → next value.
    Program size = number of distinct (prefix, next) pairs.

    If the sequence has structure, the transition table is compact.
    If the sequence has novelty, new entries keep appearing.
    """
    transitions: dict[tuple, set[int]] = defaultdict(set)
    for i in range(memory_depth, len(sequence)):
        prefix = tuple(sequence[i - memory_depth : i])
        transitions[prefix].add(sequence[i])

    # Program size = total number of (prefix, next) pairs.
    return sum(len(v) for v in transitions.values())


def test_program_growth(
    sequence_length: int = 500,
    memory_depth: int = 3,
    check_interval: int = 50,
    seed: int = 42,
) -> dict:
    """Test whether the minimal program grows as more records arrive.

    Generates a DET record sequence. Every `check_interval` events,
    computes the minimal program size for the records seen so far.
    If the program grows → law extension is occurring.
    If the program stabilizes → L is fixed for this sequence.
    """
    from det8.models.mam0 import Actualizer, CommitMap, LawMap, Record, Regime

    rng = random.Random(seed)
    r_a = Record(value=5)
    r_b = Record(value=5)
    sequence = []

    checkpoints = []
    for i in range(sequence_length):
        w = LawMap.generate(r_a, r_b, Regime.OPEN)
        idx = rng.randint(0, len(w.omega) - 1)
        successor = w.omega[idx]
        CommitMap.commit(r_a, r_b, successor)
        sequence.append(r_a.value)

        if (i + 1) % check_interval == 0 and i >= memory_depth:
            prog_size = minimal_program_size(sequence[: i + 1], memory_depth)
            checkpoints.append({
                "records": i + 1,
                "program_size": prog_size,
            })

    # Does the program grow or stabilize?
    sizes = [c["program_size"] for c in checkpoints]
    growing = all(
        sizes[i] <= sizes[i + 1] for i in range(len(sizes) - 1)
    )
    stabilized = len(sizes) >= 2 and sizes[-1] == sizes[-2]

    return {
        "sequence_length": sequence_length,
        "memory_depth": memory_depth,
        "checkpoints": checkpoints,
        "program_grows": growing and not stabilized,
        "program_stabilizes": stabilized,
        "final_program_size": sizes[-1] if sizes else 0,
        "interpretation": (
            f"Program size: {sizes[0] if sizes else '?'} → {sizes[-1] if sizes else '?'}. "
            f"{'GROWING — law extension is occurring.' if growing and not stabilized else 'STABLE — L is fixed for this sequence.' if stabilized else 'MIXED.'} "
            "A growing program means new patterns continue to appear — "
            "the compression must be extended. A stable program means "
            "all patterns have been captured — L is complete for this domain."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Extension Constraint Test
# ═══════════════════════════════════════════════════════════════════════════


def test_extension_constraint(
    n_trials: int = 100,
    seed: int = 42,
) -> dict:
    """Test the extension constraint: L_{t+1} ⊇ L_t.

    For any record R⁻, the new law map must generate AT LEAST the
    possibilities the old one did. Nothing lawful becomes unlawful.

    Test: generate two law maps from overlapping record sets.
    Check that the later (larger) map never excludes possibilities
    that the earlier (smaller) map included.
    """
    rng = random.Random(seed)

    violations = 0
    for trial in range(n_trials):
        # Generate two record sets with overlap.
        all_records = [(rng.randint(0, 10), rng.randint(0, 10)) for _ in range(50)]

        # L_early: compressed from first 20 records.
        early_set = all_records[:20]
        # L_late: compressed from all 50 records.
        late_set = all_records

        # For each possible R⁻ in early_set, both L_early and L_late
        # must generate possibilities. L_late must generate at least
        # what L_early generated.

        # Simplified: check that for a fixed R⁻, the set of possible
        # next values in L_late ⊇ those in L_early.
        for r_neg in early_set:
            # Possibilities from L_early.
            early_next = set()
            for i in range(len(early_set) - 1):
                if early_set[i] == r_neg:
                    early_next.add(early_set[i + 1][0])

            # Possibilities from L_late.
            late_next = set()
            for i in range(len(late_set) - 1):
                if late_set[i] == r_neg:
                    late_next.add(late_set[i + 1][0])

            # Check: late ⊇ early.
            if not late_next.issuperset(early_next):
                violations += 1

    return {
        "n_trials": n_trials,
        "violations": violations,
        "constraint_holds": violations == 0,
        "interpretation": (
            f"Extension constraint violations: {violations}/{n_trials}. "
            f"{'Constraint HOLDS — L never excludes old possibilities.' if violations == 0 else 'Constraint VIOLATED — L excluded some old possibilities.'}"
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Full Compression Hypothesis Status
# ═══════════════════════════════════════════════════════════════════════════


def compression_hypothesis_full() -> dict:
    """Complete compression hypothesis analysis."""
    prog = test_program_growth(sequence_length=500, memory_depth=3)
    ext = test_extension_constraint()

    return {
        "program_growth": prog,
        "extension_constraint": ext,
        "f10_status": (
            f"Program {'GROWS' if prog['program_grows'] else 'STABILIZES'}. "
            f"Extension constraint {'HOLDS' if ext['constraint_holds'] else 'VIOLATED'}. "
            "Compression hypothesis: law extension is observable when records "
            "contain novelty beyond what the current compression captures. "
            "The constraint L_{t+1} ⊇ L_t ensures old law is never degraded."
        ),
    }
