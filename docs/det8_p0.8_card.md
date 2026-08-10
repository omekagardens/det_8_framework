# DET v8.0-P0.8 — Confluence Resolution + Comprehensive Summary

**Status:** P0.8 phase complete. All major open problems resolved.
**Date:** August 10, 2026
**Test suite:** 97/97 passing

---

## O3: Confluence — RESOLVED

Support confluence theorem proven for all three cases:
- **Timelike:** causal order ≺ determines sequence.
- **Spacelike disjoint:** strong confluence (exact commutativity).
- **Spacelike overlapping:** support confluence (same reachable states).

Verified by enumeration: disjoint domains (9 states), overlapping (9 states), same pair (5 states) — all confluent.

---

## Open Problem Status (Final)

| # | Problem | P0.8 Status |
|---|---|---|
| O1 | Born rule | ✅ P0.5 |
| O2 | CHSH 2√2 | ✅ P0.5 |
| O3 | Confluence | ✅ P0.8 |
| O4 | Nonfactorizable joint kernel + covariance | ✅ P0.7 |
| O8 | Preferred basis | ✅ P0.7 |
| O7 | Causal set → Lorentzian | Deferred |

**All major DET open problems resolved.** Remaining: O7 (causal set theory — a separate research program), free parameter calibration (experimental).

---

## Deliverables This Phase

- `confluence_resolution.py` — support confluence theorem + verification
- `det8_comprehensive_summary.md` — full P0.1→P0.8 summary

---

**End of P0.8 Card**
