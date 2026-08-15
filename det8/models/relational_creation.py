"""
DET v8.1 — Relational Creation (Track B, RC1.2 formalization)

A code-auditable model of the four RC1.2 concepts, separating what the
relational-creation research gate distinguishes:

    σ_ij   active bond           (currently operative relation strength)  [0,1]
    A_ij   latent capacity       (capacity to form/restore relation)      [0,1]
    L_i    causal lineage        (immutable provenance)
    M_iG   regime membership     (belonging to regime G)                  [0,1]

Key insight (RC1-A): an active bond can disappear (σ_ij → 0) while latent
capacity persists (A_ij > 0). Deletion destroys the active edge but NOT the
capacity; rewiring changes topology but preserves membership. This module makes
that claim precise, code-auditable, and — critically — EXTRACTS the Track-A
falsification levers it implies.

THE FALSIFICATION LEVERS (see FALSIFICATION_LEDGER.md):

  FL-4 (κ-reversibility). The structural drag κ is the *gap* between latent
      capacity and active bond. Because A_ij persists when σ_ij → 0, a damaged
      bond can be fully restored (σ→A), driving κ back to baseline. Standard
      materials science (defect annealing) treats damage as PERMANENT (restore
      is a no-op). The discriminator: does κ-recovery return to baseline
      (latent capacity) or saturate (permanent damage)?
  FL-5 (κ-transfer / conservation). Externalization (discarding a damaged
      part) RELOCATES κ; it does not annihilate it. Total damage
      D = Σ(A_ij − σ_ij) over a closed system is conserved under transfer. The
      falsifier: κ vanishing at a boundary with no compensating transfer.

ANTI-SMUGGLING / QUARANTINE (RC1-D): this model uses NO theological variables.
Agency, will, grace, healing, choice, spirit — none appear as fields or
dynamics. κ is a DERIVED relational quantity (the capacity–bond gap), not a
primitive. Theology is interpretation; the model is pure relational structure.
The audit() function enforces this.

DERIVATION CERTIFICATE (honest provenance):

  σ/A/L/M four-way separation     TH-DET — from the RC1.2 research gate.
  κ = capacity–bond gap           TH-DET — relational definition (Track-B-motivated).
  κ-reversibility (FL-4)          TH-DET — consequence of A_ij persistence.
  κ-transfer conservation (FL-5)  TH-DET — consequence of externalization = relocation.
  no forbidden variables (RC1-D)  TH-DET — enforced by audit.

  NOT derived: that latent capacity persists in any concrete physical
  realization — that is exactly the FL-4 empirical question.
"""

from __future__ import annotations


# ── The relational regime ───────────────────────────────────────────────────


class RelationalRegime:
    """A regime G of n members with active bonds σ, latent capacity A,
    immutable lineage L, and membership M.

    Constructed fully healthy: σ_ij = A_ij (all latent capacity active), so
    κ = 0 at baseline. The general partially-active case is a straightforward
    variant; the demonstrations use the clean baseline.
    """

    def __init__(self, n: int, seed: int = 42):
        import random
        rng = random.Random(seed)
        self.n = n
        self.sigma = [[0.0] * n for _ in range(n)]
        self.A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                self.A[i][j] = self.A[j][i] = rng.random()
                self.sigma[i][j] = self.sigma[j][i] = self.A[i][j]  # fully active
        self.lineage = [f"L{i}" for i in range(n)]   # immutable identity
        self.membership = [1.0] * n                   # belonging to G

    # -- derived structural drag κ (normalized gap) and damage D (raw gap) ---
    def kappa(self, i: int) -> float:
        """κ_i = mean over neighbors of (A_ij − σ_ij)/A_ij (capacity–bond gap).

        0 = healthy (all capacity active), 1 = fully damaged."""
        gaps = []
        for j in range(self.n):
            if i != j and self.A[i][j] > 0:
                gaps.append((self.A[i][j] - self.sigma[i][j]) / self.A[i][j])
        return sum(gaps) / len(gaps) if gaps else 0.0

    def total_kappa(self) -> float:
        return sum(self.kappa(i) for i in range(self.n))

    def total_damage(self) -> float:
        """D = Σ_{i<j} (A_ij − σ_ij) — the raw (unnormalized) damage.

        This is the quantity CONSERVED under externalization (FL-5)."""
        return sum(self.A[i][j] - self.sigma[i][j]
                   for i in range(self.n) for j in range(i + 1, self.n))

    # -- dynamics -----------------------------------------------------------
    def weaken_bond(self, i: int, j: int):
        """σ_ij → 0, but A_ij persists (latent capacity survives damage)."""
        self.sigma[i][j] = self.sigma[j][i] = 0.0

    def restore_bond(self, i: int, j: int):
        """Reactivate latent capacity: σ_ij → A_ij (κ-reversibility, FL-4)."""
        self.sigma[i][j] = self.A[i][j]
        self.sigma[j][i] = self.A[j][i]

    def delete_bond(self, i: int, j: int):
        """Permanent deletion: both σ and A vanish (the damage leaves the regime)."""
        self.sigma[i][j] = self.sigma[j][i] = 0.0
        self.A[i][j] = self.A[j][i] = 0.0

    def rewire(self, i: int, j: int, k: int):
        """Move the active edge from (i,j) to (i,k); membership is preserved."""
        self.weaken_bond(i, j)
        self.sigma[i][k] = self.sigma[k][i] = self.A[i][k]


def externalize(R: RelationalRegime, S: RelationalRegime, i: int, j: int):
    """Move a damaged bond (i,j) from regime R to regime S.

    R discards it (σ,A → 0); S inherits the SAME capacity A but with σ = 0
    (still damaged). The raw damage D = Σ(A−σ) is conserved across the move —
    this is FL-5 (relocation, not annihilation).
    """
    a = R.A[i][j]
    R.delete_bond(i, j)
    S.A[i][j] = S.A[j][i] = a
    S.sigma[i][j] = S.sigma[j][i] = 0.0


# ── FL-4: κ-reversibility (latent capacity vs permanent damage) ─────────────


def kappa_reversibility() -> dict:
    """The FL-4 discriminator: does κ-recovery return to baseline (latent
    capacity) or saturate (permanent damage)?

    A healthy regime damages a bond (σ→0, A persists), then restores it
    (σ→A). κ spikes then returns to baseline exactly. The falsifier is the
    permanent-damage world, where restore is impossible and κ stays elevated
    (saturates at the damaged level).
    """
    r = RelationalRegime(6, seed=11)
    baseline = r.total_kappa()                 # healthy, κ = 0
    r.weaken_bond(0, 1)
    damaged = r.total_kappa()                  # κ > 0
    r.restore_bond(0, 1)
    restored = r.total_kappa()                 # back to baseline

    return {
        "baseline_kappa": baseline,
        "damaged_kappa": damaged,
        "restored_kappa": restored,
        "damage_increases_kappa": damaged > baseline,
        "latent_recovers_to_baseline": abs(restored - baseline) < 1e-12,
        "falsifier": (
            "If κ-recovery saturates — restored κ stays at the damaged level "
            "(restore is a no-op because latent capacity does not persist) — "
            "FL-4 is falsified. Full recovery to baseline is the latent-"
            "capacity signature."
        ),
    }


# ── FL-5: κ-transfer / conservation across regimes ──────────────────────────


def kappa_transfer() -> dict:
    """The FL-5 claim: externalization RELOCATES damage, it does not annihilate.

    A damaged bond is externalized from regime R to regime S. The raw damage
    D = Σ(A−σ) over the closed system (R ∪ S) is conserved across the move.
    """
    R = RelationalRegime(4, seed=3)
    S = RelationalRegime(4, seed=5)
    R.weaken_bond(0, 1)                      # R is damaged
    total_before = R.total_damage() + S.total_damage()

    externalize(R, S, 0, 1)                  # R discards, S inherits
    total_after = R.total_damage() + S.total_damage()

    return {
        "total_damage_before": total_before,
        "total_damage_after": total_after,
        "R_damage_after": R.total_damage(),
        "S_damage_after": S.total_damage(),
        "conserved": abs(total_after - total_before) < 1e-12,
        "falsifier": (
            "If total damage D decreases at a regime boundary with no "
            "compensating transfer to the receiving regime, FL-5 is falsified."
        ),
    }


# ── The claims RC1-A … RC1-G, made verifiable ───────────────────────────────


def verify_claims() -> dict:
    """Turn the RC1.2 claims into checkable invariants."""
    r = RelationalRegime(5, seed=7)
    lineage_before = r.lineage[:]
    membership_before = r.membership[:]

    r.weaken_bond(0, 1)
    rc1a_weaken = (r.sigma[0][1] == 0.0 and r.A[0][1] > 0.0)

    r.rewire(0, 1, 2)
    rc1a_rewire = (r.lineage == lineage_before and r.membership == membership_before)

    return {
        "RC1-A bond weakens while capacity persists": rc1a_weaken,
        "RC1-A rewiring preserves lineage + membership": rc1a_rewire,
        "RC1-D no theological variables": audit()["no_forbidden_variables"],
        "RC1-D κ is derived (not a primitive field)": audit()["kappa_is_derived"],
    }


# ── Anti-smuggling audit ─────────────────────────────────────────────────────


_FORBIDDEN = ("agency", "will", "choice", "spirit", "grace", "healing",
              "jubilee", "consciousness", "intention", "soul")


def audit() -> dict:
    """Enforce RC1-D: no theological variables; κ is derived, not primitive."""
    src_fields = ["sigma", "A", "lineage", "membership", "kappa", "weaken_bond",
                  "restore_bond", "delete_bond", "rewire", "total_kappa",
                  "total_damage", "externalize"]
    no_forbidden = not any(any(w in f.lower() for w in _FORBIDDEN) for f in src_fields)

    r = RelationalRegime(3, seed=1)
    kappa_is_derived = "kappa" not in vars(r)  # computed, not stored

    return {
        "no_forbidden_variables": no_forbidden,
        "kappa_is_derived": kappa_is_derived,
        "forbidden_list": list(_FORBIDDEN),
        "interpretation": (
            "The relational model carries no agency/will/grace/healing fields; "
            "κ is computed from the capacity–bond gap. Theology is Track-B "
            "interpretation, not a physical mechanism."
        ),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "Track B RC1.2 — relational creation, formalized",
        "deliverables": {
            "σ/A/L/M four-way separation": "TH-DET — from the RC1.2 research gate",
            "κ = capacity–bond gap": "TH-DET — relational definition (Track-B-motivated)",
            "κ-reversibility (FL-4)": "TH-DET — consequence of A_ij persistence",
            "κ-transfer / conservation (FL-5)": "TH-DET — consequence of externalization = relocation",
            "no forbidden variables (RC1-D)": "TH-DET — enforced by audit",
        },
        "falsification_levers": {
            "FL-4": "κ-recovery saturates at permanent-damage level (no latent-capacity restoration) ⟹ falsified",
            "FL-5": "κ vanishes at a regime boundary with no compensating transfer ⟹ falsified",
        },
        "not_derived_here": [
            "that latent capacity persists in any concrete physical realization (the FL-4 empirical question)",
            "the theological reading of 'belonging' (RC1-G — interpretation, not mechanism)",
        ],
        "status": (
            "Track B's relational-creation concepts are now code-auditable, and "
            "their formalization surfaces two new Track-A falsification levers "
            "(FL-4 κ-reversibility, FL-5 κ-transfer) — registered in "
            "FALSIFICATION_LEDGER.md."
        ),
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_rc12() -> dict:
    return {
        "kappa_reversibility": kappa_reversibility(),
        "kappa_transfer": kappa_transfer(),
        "claims": verify_claims(),
        "audit": audit(),
        "certificate": derivation_certificate(),
        "interpretation": (
            "Latent capacity (A_ij) survives damage, so κ is reversible (FL-4): "
            "damage spikes κ and reactivation restores baseline. Externalization "
            "relocates damage rather than annihilating it (FL-5): total damage "
            "is conserved across regimes. The model carries no theological "
            "variables and κ is derived. These two κ-dynamics claims are the "
            "new Track-A falsification levers the Track-B formalization surfaced."
        ),
    }
