#!/usr/bin/env python3
"""PIM001: exact, conditional four-birth research model; Python standard library.

Run: python3 -B runnable_model.py [--histories]
Matrices factor out the supplied beta>0: phi=sqrt(beta)L R,
[phi_r,phi_s]=i beta K_rs, V=beta V_over_beta, W=beta(W_real+i W_imag).
No sampling, fitting, physical units, kernel quotient or endpoint-state repair.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
import argparse
import json


@dataclass(frozen=True)
class Birth:
    label: str
    ideal: frozenset
    mark: int
    q: F                         # Structural probability, before the fair bit.


@dataclass(frozen=True)
class State:
    labels: tuple                # Chronological identity handles, never a clock.
    order: frozenset              # Full strict relation: (source, target).
    marks: tuple                 # Immutable by step().
    counters: tuple              # Prepared classical incidence register, mod 5.
    probability: F               # Conditional marked-history mass.
    structural_probability: F
    history: tuple = ()          # Suffix births; prefix is already conditioned on.

    def validate(self):
        n = len(self.labels)
        if not 2 <= n <= 4 or len(set(self.labels)) != n:
            raise ValueError("Only distinct identities at prepared sizes 2..4")
        if len(self.marks) != n or any(b not in (0, 1) for b in self.marks):
            raise ValueError("One binary immutable mark per vertex required")
        if len(self.counters) != n or any(c not in range(5) for c in self.counters):
            raise ValueError("One five-valued counter per vertex required")
        index = {v: k for k, v in enumerate(self.labels)}
        if any(u not in index or v not in index or index[u] >= index[v]
               for u, v in self.order):
            raise ValueError("Order must be strict and follow the birth schedule")
        if any((u, w) not in self.order for u, v in self.order
               for vv, w in self.order if v == vv):
            raise ValueError("Full transitive relation required")
        if (self.labels[0], self.labels[1]) not in self.order or self.marks[1] != 0:
            raise ValueError("PIM001 requires the registered a<b prefix, marks(i,0)")
        if self.counters != tuple(sum(u == v for u, _ in self.order)
                                  for v in self.labels):
            raise ValueError("Counters must be consistent with the fixed preparation")
        if self.probability <= 0 or self.structural_probability <= 0:
            raise ValueError("History weights must be positive")


def prepare(i, labels=("a", "b")):
    if i not in (0, 1) or len(labels) != 2:
        raise ValueError("Choose prepared bit 0 or 1 and two distinct labels")
    state = State(tuple(labels), frozenset({tuple(labels)}), (i, 0), (1, 0), F(1), F(1))
    state.validate()
    return state


def actual_ideals(state):
    """Enumerate every actual downward-closed labeled subset once."""
    state.validate()
    return tuple(frozenset(s) for n in range(len(state.labels) + 1)
                 for s in combinations(state.labels, n)
                 if all(v not in s or u in s for u, v in state.order))


def transition_row(state):
    """Original q restricted to the registered two-prefix continuation domain.

    Proper slots follow finite_incidence_register.md; full slot is their exact
    normalization complement. No shape class replaces actual ideal occurrences.
    """
    state.validate()
    ideals = actual_ideals(state)
    full = frozenset(state.labels)
    i = state.marks[0]
    c, e = F(1, 5), F(1, 44)
    f, h = (F(1, 6), F(19, 30)) if i == 0 else (F(1, 3), F(7, 15))
    a, b = state.labels[:2]
    if len(state.labels) == 2:
        row = {frozenset(): c, frozenset({a}): f, full: h}
    elif len(state.labels) == 3:
        x = state.labels[2]
        proper = {}
        for s in ideals:
            if s == full:
                continue
            if len(state.order) == 1:           # Edge a<b, isolate x.
                q = {frozenset(): e, frozenset({x}): e,
                     frozenset({a}): e*f/c, frozenset({a, b}): e*h/c,
                     frozenset({a, x}): e*F(11, 20)/F(1, 10)}[s]
            elif len(state.order) == 2:         # Fork rooted at a.
                q = e if len(s) <= 1 else e*h/f
            elif len(state.order) == 3:         # Total chain a<b<x.
                q = e
            else:
                raise ValueError("Parent outside registered continuation domain")
            proper[s] = q
        row = {**proper, full: F(1) - sum(proper.values(), F(0))}
    else:
        raise ValueError("Four-birth horizon reached; no fifth-birth law supplied")
    if set(row) != set(ideals) or sum(row.values(), F(0)) != 1 or min(row.values()) <= 0:
        raise ValueError("Incomplete, unnormalized or nonpositive original q row")
    return row


def step(state, ideal, mark, label):
    """Append one maximal birth, q/2 mass and exact addressed counter update."""
    ideal = frozenset(ideal)
    row = transition_row(state)
    if ideal not in row or mark not in (0, 1) or label in state.labels:
        raise ValueError("Requires an actual ideal, fair binary mark and fresh identity")
    q = row[ideal]
    result = State(
        state.labels + (label,), state.order | frozenset((u, label) for u in ideal),
        state.marks + (mark,),
        tuple((n + (u in ideal)) % 5 for u, n in zip(state.labels, state.counters)) + (0,),
        state.probability*q/2, state.structural_probability*q,
        state.history + (Birth(label, ideal, mark, q),))
    result.validate()
    return result


def enumerate_histories(i):
    states = (prepare(i),)
    for label in ("x", "y"):
        states = tuple(step(s, ideal, bit, label) for s in states
                       for ideal in actual_ideals(s) for bit in (0, 1))
    return states


def readouts(state):
    """Formal total-chain D and prepared counter-equals-two Y."""
    n = len(state.labels)
    return int(len(state.order) == n*(n-1)//2), int(2 in state.counters)


def covers(state):
    return tuple((u, v) for u in state.labels for v in state.labels
                 if (u, v) in state.order and not any(
                     (u, w) in state.order and (w, v) in state.order for w in state.labels))


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    return tuple(tuple(sum(x*y for x, y in zip(row, col)) for col in transpose(b)) for row in a)


J = tuple(tuple((1 if r % 2 == 0 else -1) if c == (r ^ 1) else 0
                for c in range(6)) for r in range(6))


@dataclass(frozen=True)
class Field:
    labels: tuple
    L: tuple
    C: tuple                     # Target row, source column.
    K: tuple                     # Commutator divided by i*beta.
    V_over_beta: tuple
    W_real_over_beta: tuple
    W_imag_over_beta: tuple

    def weyl_exponent_over_beta(self, t):
        """Exact exponent coefficient: omega(exp(i t.phi))=exp(beta * result)."""
        if len(t) != len(self.labels):
            raise ValueError("One real rational smearing per field required")
        t = tuple(F(x) for x in t)
        return -sum(t[r]*self.V_over_beta[r][s]*t[s]
                    for r in range(len(t)) for s in range(len(t)))/2


def attach_field(state, endpoint_labels=None):
    """Apply supplied chronological map, THEN transport observable row labels.

    Endpoint transport does not reassign oscillator birth roles or remove schedule.
    Matrices represent the Gaussian exactly; no Hilbert-space truncation is used.
    """
    state.validate()
    c = lambda r, s: int((state.labels[s], state.labels[r]) in state.order)
    rows = [(1, 0, 0, 0, 0, 0), (0, -1, 0, 0, 0, 0)]
    if len(state.labels) >= 3:
        rows.append((-c(2, 1), -c(2, 0), 1, 0, 0, 0))
    if len(state.labels) == 4:
        rho = c(3, 2) - c(3, 1)*c(2, 0) + c(3, 0)*c(2, 1)
        rows.append((-c(3, 1), -c(3, 0), 0, -rho, 1, 0))
    labels = state.labels if endpoint_labels is None else tuple(endpoint_labels)
    if len(labels) != len(state.labels) or set(labels) != set(state.labels):
        raise ValueError("Endpoint labels must be a permutation of all identities")
    L = tuple(rows[state.labels.index(v)] for v in labels)
    C = tuple(tuple(int((s, r) in state.order) for s in labels) for r in labels)
    K = matmul(matmul(L, J), transpose(L))
    V = tuple(tuple(F(x, 2) for x in row) for row in matmul(L, transpose(L)))
    Wi = tuple(tuple(F(x, 2) for x in row) for row in K)
    return Field(labels, L, C, K, V, V, Wi)


def cover_link_mean(state, field=None):
    """Mean of sum_covers (phi_v-phi_u)^2/(2 beta), on ANY domain history."""
    field = attach_field(state) if field is None else field
    if set(field.labels) != set(state.labels):
        raise ValueError("Field and order identities must match")
    V = field.V_over_beta
    return sum((V[field.labels.index(u)][field.labels.index(u)]
                + V[field.labels.index(v)][field.labels.index(v)]
                - 2*V[field.labels.index(u)][field.labels.index(v)])/2
               for u, v in covers(state))


def named_swap(i=0, marks=(0, 0)):
    """Two original supported histories with common endpoint (a,b,u,v)."""
    p = prepare(i)
    plus = step(step(p, {"a"}, marks[0], "u"), {"a", "b"}, marks[1], "v")
    minus = step(step(p, {"a", "b"}, marks[1], "v"), {"a"}, marks[0], "u")
    return plus, minus


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    return value


def report(include_histories=False):
    preparations = []
    for i in (0, 1):
        histories = enumerate_histories(i)
        joint = {cell: F(0) for cell in ((0, 0), (0, 1), (1, 0), (1, 1))}
        causal = old = 0
        for s in histories:
            joint[readouts(s)] += s.probability
            f = attach_field(s)
            causal += f.K == tuple(tuple(f.C[r][c]-f.C[c][r] for c in range(4)) for r in range(4))
            old += (tuple(tuple(row[:2]) for row in f.W_real_over_beta[:2]) == ((F(1, 2), 0), (0, F(1, 2)))
                    and tuple(tuple(row[:2]) for row in f.W_imag_over_beta[:2]) == ((0, F(-1, 2)), (F(1, 2), 0)))
        entry = {"prepared_bit": i, "marked_histories": len(histories),
                 "mass": sum(s.probability for s in histories), "joint_00_01_10_11": list(joint.values()),
                 "D_mean": joint[(1, 0)] + joint[(1, 1)], "Y_mean": joint[(0, 1)] + joint[(1, 1)],
                 "causal_commutator_checks": causal, "W2_restriction_checks": old,
                 "cover_link_mean_range": [min(cover_link_mean(s) for s in histories), max(cover_link_mean(s) for s in histories)]}
        if include_histories:
            entry["histories"] = [{"labels": s.labels, "ideals": [sorted(b.ideal) for b in s.history],
                                   "order": sorted(s.order), "marks": s.marks, "counters": s.counters,
                                   "probability": s.probability, "structural_probability": s.structural_probability,
                                   "DY": readouts(s), "L": attach_field(s).L, "C": attach_field(s).C,
                                   "K": attach_field(s).K, "V_over_beta": attach_field(s).V_over_beta,
                                   "W_imag_over_beta": attach_field(s).W_imag_over_beta,
                                   "cover_link_mean": cover_link_mean(s)} for s in histories]
        preparations.append(entry)
    plus, minus = named_swap()
    fp, fm = (attach_field(s, ("a", "b", "u", "v")) for s in (plus, minus))
    delta = tuple(tuple(fp.V_over_beta[r][c]-fm.V_over_beta[r][c] for c in range(4)) for r in range(4))
    return encode({"model": "PIM001", "preparations": preparations,
                   "contrasts_P1_minus_P0": {k: preparations[1][k]-preparations[0][k] for k in ("D_mean", "Y_mean")},
                   "named_swap": {"structural_weights": [plus.structural_probability, minus.structural_probability],
                       "K_equal": fp.K == fm.K, "V_plus_minus_over_beta": delta,
                       "endpoint_field_state_covariance": "FAIL: demonstrated schedule dependence",
                       "Weyl_e_u_exponents_over_beta": [fp.weyl_exponent_over_beta((0, 0, 1, 0)), fm.weyl_exponent_over_beta((0, 0, 1, 0))],
                       "cover_link_means": [cover_link_mean(plus, fp), cover_link_mean(minus, fm)]},
                   "empirical_agreement": "NOT TESTED; no calibration or holdout data",
                   "scope": "Conditional finite operational baseline; Option B / Status M unchanged"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--histories", action="store_true", help="Include all 120 histories and exact field matrices")
    args = parser.parse_args()
    print(json.dumps(report(args.histories), indent=2))
