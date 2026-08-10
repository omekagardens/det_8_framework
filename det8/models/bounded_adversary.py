"""
Bounded-Adversary Model-Complexity Tool (S2b)

Implements a bounded-memory retrodiction/prediction analysis for MAM-0
and MAM-Q output sequences. This is a model-class discrimination tool,
NOT an ontological-openness discriminator.

Per D4 (discriminator feasibility): S2/S2b can discriminate between
bounded model classes but cannot establish ontological openness. It
answers: "can a bounded-memory emulator reproduce this sequence?" —
not "was the future genuinely open?"

The tool fits bounded-memory Markov predictors to committed record
sequences and measures prediction error. It compares sequences from:
- DET open regime (non-singleton support)
- Deterministic regime (singleton support)
- Pseudorandom null model
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


# ── Sequence Generator (from MAM-0) ────────────────────────────────────────


def generate_open_sequence(
    n_events: int,
    seed: int = 42,
    initial_a: int = 5,
    initial_b: int = 5,
) -> list[int]:
    """Generate a sequence of committed outcomes from MAM-0 in open regime.

    Each event transfers -1, 0, or +1 from A to B (subject to nonnegativity).
    Returns the sequence of A-values (or B-values) as the record trace.

    Uses MAM-0's law map and actualizer directly.
    """
    from det8.models.mam0 import Actualizer, CommitMap, LawMap, Record, Regime

    rng = random.Random(seed)
    r_a = Record(value=initial_a)
    r_b = Record(value=initial_b)
    trace: list[int] = []

    for _ in range(n_events):
        # Generate possibility from current record.
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        # Select outcome (uniform over Ω).
        idx = rng.randint(0, len(w.omega) - 1)
        successor = w.omega[idx]

        # Commit.
        CommitMap.commit(r_a, r_b, successor)

        # Record the trace: store the current value of A.
        trace.append(r_a.value)

    return trace


def generate_deterministic_sequence(
    n_events: int,
    initial_a: int = 5,
    initial_b: int = 5,
) -> list[int]:
    """Generate a deterministic sequence from MAM-0."""
    from det8.models.mam0 import Actualizer, CommitMap, LawMap, Record, Regime

    r_a = Record(value=initial_a)
    r_b = Record(value=initial_b)
    trace: list[int] = []

    for _ in range(n_events):
        w = LawMap.generate(r_a, r_b, Regime.DETERMINISTIC)
        successor = w.omega[0]  # Only one option.
        CommitMap.commit(r_a, r_b, successor)
        trace.append(r_a.value)

    return trace


def generate_pseudorandom_sequence(
    n_events: int,
    seed: int = 42,
    min_val: int = 0,
    max_val: int = 10,
) -> list[int]:
    """Generate a pseudorandom sequence from a uniform distribution.

    This is the null model: a pseudorandom sequence is deterministically
    generated from a short seed but appears incompressible without the seed.
    """
    rng = random.Random(seed)
    return [rng.randint(min_val, max_val) for _ in range(n_events)]


# ── Bounded-Memory Markov Predictor ─────────────────────────────────────────


@dataclass
class BoundedPredictor:
    """A bounded-memory Markov predictor.

    Given a memory depth M, predicts the next value based on the
    previous M values. If the (M+1)-gram has been seen in training,
    predicts the most common successor. Otherwise falls back to M-1,
    then M-2, etc.
    """

    memory_depth: int
    transitions: dict[tuple, dict[int, int]] = None  # type: ignore

    def __post_init__(self):
        if self.transitions is None:
            self.transitions = defaultdict(lambda: defaultdict(int))

    def train(self, sequence: list[int]) -> None:
        """Train on a sequence: count (prefix → next) transitions."""
        for i in range(self.memory_depth, len(sequence)):
            prefix = tuple(sequence[i - self.memory_depth : i])
            next_val = sequence[i]
            self.transitions[prefix][next_val] += 1

    def predict(self, prefix: tuple[int, ...]) -> Optional[int]:
        """Predict the most likely next value given a prefix.

        Falls back to shorter prefixes if the full prefix is unseen.
        """
        for m in range(self.memory_depth, 0, -1):
            key = prefix[-m:] if m <= len(prefix) else prefix
            if key in self.transitions:
                counts = self.transitions[key]
                if counts:
                    return max(counts, key=lambda k: counts[k])
        return None

    def evaluate(self, sequence: list[int]) -> dict:
        """Evaluate prediction accuracy on a sequence.

        Returns error rate: fraction of positions where the predictor
        either couldn't predict or predicted wrong.
        """
        errors = 0
        predictions_made = 0
        total = len(sequence) - self.memory_depth

        if total <= 0:
            return {"error_rate": 1.0, "predictions_made": 0, "total_predictable": 0}

        for i in range(self.memory_depth, len(sequence)):
            prefix = tuple(sequence[i - self.memory_depth : i])
            actual = sequence[i]
            predicted = self.predict(prefix)

            if predicted is not None:
                predictions_made += 1
                if predicted != actual:
                    errors += 1
            else:
                errors += 1  # Count inability to predict as error.

        error_rate = errors / total if total > 0 else 1.0

        return {
            "error_rate": error_rate,
            "predictions_made": predictions_made,
            "total_predictable": total,
            "errors": errors,
        }


# ── Model-Complexity Analysis ───────────────────────────────────────────────


def bounded_adversary_analysis(
    n_events: int = 1000,
    memory_depth: int = 3,
    seed: int = 42,
) -> dict:
    """Compare bounded-memory prediction performance across sequence types.

    Trains on first 80% of each sequence, tests on last 20%.

    Returns a comparison table showing:
    - DET open regime error rate
    - Deterministic regime error rate
    - Pseudorandom error rate
    """
    split = int(n_events * 0.8)

    # Generate sequences.
    open_seq = generate_open_sequence(n_events, seed=seed)
    det_seq = generate_deterministic_sequence(n_events)
    rand_seq = generate_pseudorandom_sequence(n_events, seed=seed + 1)

    results = {}

    for name, seq in [
        ("open (DET)", open_seq),
        ("deterministic", det_seq),
        ("pseudorandom", rand_seq),
    ]:
        train_seq = seq[:split]
        test_seq = seq[split:]

        predictor = BoundedPredictor(memory_depth=memory_depth)
        predictor.train(train_seq)
        eval_result = predictor.evaluate(test_seq)

        # Also compute unique (M+1)-gram count in training data.
        unique_ngrams = len(predictor.transitions)

        results[name] = {
            "error_rate": eval_result["error_rate"],
            "predictions_made": eval_result["predictions_made"],
            "total_predictable": eval_result["total_predictable"],
            "unique_training_ngrams": unique_ngrams,
            "sequence_preview": seq[:10],
        }

    return {
        "n_events": n_events,
        "memory_depth": memory_depth,
        "train_split": split,
        "results": results,
        "interpretation": (
            "Lower error rate → more predictable by bounded-memory adversary. "
            "Higher error rate → less predictable, more 'complex'. "
            "This measures model-class discrimination, NOT ontological openness. "
            "A deterministic chaotic system can also produce high error rates. "
            "A pseudorandom sequence from a short seed is deterministic but "
            "appears incompressible without the seed."
        ),
    }


# ── Compression Ratio Analysis ──────────────────────────────────────────────


def compression_ratio_analysis(
    n_events: int = 1000,
    max_memory: int = 5,
    seed: int = 42,
) -> dict:
    """Analyze how compression ratio varies with memory depth.

    For each sequence type and each memory depth, compute the prediction
    error rate. Plot the "learning curve" — error rate vs memory depth.

    A sequence that requires more memory to predict is "more complex"
    from the bounded-adversary perspective.
    """
    split = int(n_events * 0.8)

    open_seq = generate_open_sequence(n_events, seed=seed)
    det_seq = generate_deterministic_sequence(n_events)
    rand_seq = generate_pseudorandom_sequence(n_events, seed=seed + 1)

    curves = {"open": [], "deterministic": [], "pseudorandom": []}

    for m in range(1, max_memory + 1):
        for name, seq in [
            ("open", open_seq),
            ("deterministic", det_seq),
            ("pseudorandom", rand_seq),
        ]:
            train_seq = seq[:split]
            test_seq = seq[split:]

            predictor = BoundedPredictor(memory_depth=m)
            predictor.train(train_seq)
            eval_result = predictor.evaluate(test_seq)
            curves[name].append(
                {"memory": m, "error_rate": eval_result["error_rate"]}
            )

    return {
        "n_events": n_events,
        "max_memory": max_memory,
        "curves": curves,
    }
