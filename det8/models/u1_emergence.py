"""DET — unproved suggestions concerning a phase and reversible dynamics.

A complex Hermitian matrix has a symmetric real part and one antisymmetric
imaginary part by definition. This calculation does not derive the complex
field from one causal order, exclude quaternionic operational theories, or
identify imaginary units with arrows of time. Compatible complex forms in
why_complex.py are supplied assumptions, not a completed field selection.

Likewise, preserving an unbiased distribution does not imply reversible
or unitary dynamics: a uniform-reset channel is an elementary counterexample.
Irreversible record growth can coexist with particular reversible residual
models, but does not force them. These interpretive suggestions and a
constructive U(1)-from-discrete derivation remain open.
"""

from __future__ import annotations


def one_arrow_implies_one_phase() -> dict:
    """Historical name: decompose an already complex Hermitian example."""

    # Concrete: a Hermitian 𝔇 decomposes into exactly one antisymmetric part.
    D = [[0.5, 0.2 + 0.1j], [0.2 - 0.1j, 0.5]]
    n = len(D)
    G = [[D[i][j].real for j in range(n)] for i in range(n)]
    Om = [[D[i][j].imag for j in range(n)] for i in range(n)]
    antisymmetric = all(
        abs(Om[i][j] + Om[j][i]) < 1e-12 for i in range(n) for j in range(n)
    )
    symmetric = all(
        abs(G[i][j] - G[j][i]) < 1e-12 for i in range(n) for j in range(n)
    )
    return {
        "hermitian_decomposition": "𝔇 = G + iΩ (G symmetric, Ω antisymmetric)",
        "handwritten_2x2_is_hermitian": antisymmetric and symmetric,
        "one_arrow_gives_one_phase": (
            "One causal order does not establish the number of physical phase "
            "degrees of freedom or choose a scalar field."

        ),
        "computed_vs_asserted": (
            "the numeric check only verifies the hand-written 2×2 matrix is "
            "Hermitian. Connecting this to causal arrows is an unproved shape ARGUMENT, "
            "not an implication of the calculation."
        ),
        "conclusion": "The decomposition assumes complex scalars and does not select them.",
        "complex_field_selected": False,
        "causal_order_implies_one_phase": False,
    }


def irreversible_record_reversible_possibility() -> dict:
    """Distinguish compatible interpretations from a reversible-dynamics theorem."""
    channel = [[0.5, 0.5], [0.5, 0.5]]
    outputs = [[sum(channel[i][j] * state[j] for j in range(2)) for i in range(2)]
               for state in ([1.0, 0.0], [0.0, 1.0])]
    return {
        "record_is_irreversible": "Committed record growth is directed; it does not determine residual reversibility",
        "possibility_is_open": "Open possibility is an interpretation, not a specified transition law",
        "unbiased_navigation_is_reversible": "Preservation of a uniform distribution does not imply reversibility or unitarity",
        "complementarity": "Irreversible records and chosen reversible residual models may coexist, but coexistence does not derive either law",
        "counterexample": {"uniform_preserving_channel": channel, "distinct_input_outputs": outputs,
                           "injective": outputs[0] != outputs[1]},
        "reversibility_derived": False,
    }


def u1_emergence_resolution() -> dict:
    return {
        "residue_addressed": "unproved links between causal order, phase and reversible residual dynamics",
        "one_phase": one_arrow_implies_one_phase(),
        "reversibility": irreversible_record_reversible_possibility(),
        "provenance": {
            "complex Hermitian decomposition": "MATH — conditional on the supplied complex matrix",
            "one causal order selects one physical phase": "UNPROVED interpretive suggestion",
            "uniform preservation implies reversibility": "FALSE — uniform-reset counterexample",
        },
        "honest_boundary": "The shape arguments do not close the conceptual or constructive selection problem; U(1) emergence remains unproved.",
        "scope": {"complex_field_selected": False, "reversibility_derived": False,
                  "u1_emergence_proved": False},
    }
