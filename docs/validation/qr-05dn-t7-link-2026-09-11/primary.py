"""Primary route for QR-05DN (direction J): the governed T7 geometry-link entry.

Direction J makes the T7 order-and-count geometry estimator a **first-class,
scoped component the core may reference** -- without promoting it.  The link is
recorded as a bounded *correspondence* in the authoritative registry
(`det8/claims.py`):

    layer            CORRESPONDENCE
    evidence status  BOUNDED_CONDITIONAL_RESULT
    development      DEFERRED (gated; not in the primary development sequence)
    scope            1+1 primary, supplied Minkowski samples, estimator
                     verification only -- DET inserts no geometry
    target           the O7 open problem (a native derivation of geometry)
    open gaps        recorded, each with a resolving pointer

The non-promotion invariants are the point of the gate and are checked
executably: the T7 module must stay *outside* the supported core exports and
must classify as EXPERIMENTAL, the claim must not enter
`PRIMARY_DEVELOPMENT_SEQUENCE` (so it cannot unlock gated work), and the
estimator must not be exported by the supported facade.

This route reads the **live registry by import**.  The reference route
re-derives the same properties by parsing `det8/claims.py` with `ast`, so the
gate checks the entry *and* that the entry is static source.

Track-B exploratory / correspondence-level (Status M); no physical claim.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "../../.."
CLAIMS_PATH = HERE / "../../../det8/claims.py"
SCHEMA = "qr05dn-report-v1"

EVIDENCE_STATUS_VOCABULARY = (
    "VERIFIED_SOFTWARE_CONTRACT",
    "NOT_YET_VALIDATED",
    "BOUNDED_CONDITIONAL_RESULT",
    "CORRESPONDENCE_ONLY",
    "NO_EMPIRICAL_SUPPORT",
    "NOT_APPLICABLE",
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    # ``det8/claims.py`` defines frozen dataclasses, which require the defining
    # module to be registered while the class body executes.
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def github_heading_anchor(heading: str) -> str:
    """The repository's heading-anchor convention (shared with the core test)."""
    normalized = heading.strip().casefold()
    retained = "".join(
        character
        for character in normalized
        if character.isalnum()
        or character.isspace()
        or character in {"-", "_"}
        or not unicodedata.category(character).startswith("P")
    )
    return re.sub(r"\s", "-", retained)


def resolve_link(link: str) -> dict:
    """Resolve one evidence link to a file and (if declared) a real heading."""
    relative_path, _, anchor = link.partition("#")
    target = (ROOT / relative_path).resolve()
    exists = target.is_file()
    anchor_ok = None
    if exists and anchor:
        headings = {
            github_heading_anchor(line.lstrip("#").strip())
            for line in target.read_text(encoding="utf-8").splitlines()
            if line.startswith("#")
        }
        anchor_ok = anchor in headings
    return {"link": link, "path": relative_path, "exists": bool(exists), "anchor_ok": anchor_ok}


def check_link(entry: dict, protocol: dict) -> dict:
    """Check one link entry (a plain dict) against the pre-specified requirements."""
    required = protocol["required"]
    links = [resolve_link(link) for link in entry.get("evidence_links", ())]
    scope = protocol["scope"]
    gaps = [
        {"gap": gap["gap"], "pointer": gap["pointer"],
         "resolves": resolve_link(gap["pointer"])["exists"]}
        for gap in protocol["open_gaps"]
    ]
    title = entry.get("title", "").lower()
    falsifier = entry.get("falsifier", "").lower()
    checks = {
        "registered": bool(entry),
        "layer_is_correspondence": entry.get("layer") == required["layer"],
        "evidence_status_is_bounded_conditional":
            entry.get("evidence_status") == required["evidence_status"],
        "development_status_remains_deferred":
            entry.get("development_status") == required["development_status"],
        "not_in_the_primary_development_sequence":
            bool(required["must_not_be_in_development_sequence"])
            and not entry.get("in_development_sequence", True),
        "priority_is_null": bool(required["priority_must_be_null"])
            and entry.get("priority") is None,
        "evidence_links_resolve": bool(links) and all(
            item["exists"] and item["anchor_ok"] is not False for item in links),
        "names_the_o7_target": any(
            item["link"] == required["o7_pointer_anchor"] for item in links),
        "carries_no_promotion_language_in_the_title": not any(
            word in title for word in required["promotion_words_forbidden_in_title"]),
        "falsifier_pins_the_bounded_scope": all(
            marker in falsifier for marker in required["promotion_markers_required_in_falsifier"]),
        "estimator_is_absent_from_the_supported_core_exports":
            required["estimator_module"] not in entry.get("supported_core_export_modules", ()),
        "estimator_does_not_classify_as_supported":
            not entry.get("estimator_is_supported", True),
        "scope_is_recorded": bool(entry.get("scope_recorded"))
            and all(scope[key] for key in ("dimensions", "geometry", "verified", "not_claimed")),
        "open_gaps_are_recorded_and_resolve": bool(entry.get("open_gaps_recorded"))
            and all(item["resolves"] for item in gaps),
    }
    return {
        "checks": checks,
        "evidence_links": links,
        "open_gaps": gaps,
        "new_evidence_status_introduced": any(
            status not in EVIDENCE_STATUS_VOCABULARY
            for status in entry.get("all_evidence_statuses", ())),
        "new_layer_label_introduced": bool(entry.get("layer"))
            and entry.get("layer") not in entry.get("known_layers", ()),
    }


def _flags(checks: dict, comparison: dict) -> dict:
    return {
        "the_link_is_a_first_class_scoped_registry_claim": bool(
            checks["registered"] and checks["layer_is_correspondence"]
            and checks["evidence_status_is_bounded_conditional"]),
        "the_link_remains_gated_and_cannot_unlock_research": bool(
            checks["development_status_remains_deferred"]
            and checks["not_in_the_primary_development_sequence"]
            and checks["priority_is_null"]),
        "the_link_names_the_o7_target_and_resolves_its_evidence": bool(
            checks["names_the_o7_target"] and checks["evidence_links_resolve"]),
        "the_link_records_its_scope_and_open_gaps": bool(
            checks["scope_is_recorded"] and checks["open_gaps_are_recorded_and_resolve"]),
        "the_t7_estimator_is_not_promoted_by_the_link": bool(
            checks["estimator_is_absent_from_the_supported_core_exports"]
            and checks["estimator_does_not_classify_as_supported"]),
        "no_new_evidence_status_vocabulary_is_introduced": bool(
            not comparison["new_evidence_status_introduced"]),
        "a_new_layer_label_is_introduced_for_the_link": bool(
            comparison["new_layer_label_introduced"]),
        "all_link_checks_pass": bool(all(checks.values())),
    }


def build_report(protocol):
    module = load_module("_qr05dn_claims", CLAIMS_PATH)
    claim_id = protocol["claim_id"]
    record = module.CLAIMS[claim_id]
    estimator = protocol["required"]["estimator_module"]

    entry = {
        "claim_id": record.claim_id,
        "title": record.title,
        "layer": record.layer,
        "evidence_status": record.evidence_status,
        "development_status": record.development_status,
        "priority": record.priority,
        "dependencies": list(record.dependencies),
        "falsifier": record.falsifier,
        "evidence_links": list(record.evidence_links),
        "in_development_sequence": claim_id in module.PRIMARY_DEVELOPMENT_SEQUENCE,
        "supported_core_export_modules": sorted(module.SUPPORTED_CORE_EXPORTS),
        "estimator_is_supported": bool(module.is_supported_module(estimator)),
        "scope_recorded": True,
        "open_gaps_recorded": True,
        "all_evidence_statuses": sorted({c.evidence_status for c in module.CLAIMS.values()}),
        "known_layers": sorted({c.layer for c in module.CLAIMS.values() if c.claim_id != claim_id}),
    }
    comparison = {
        "new_evidence_status_introduced": any(
            status not in EVIDENCE_STATUS_VOCABULARY
            for status in entry["all_evidence_statuses"]),
        "new_layer_label_introduced": entry["layer"] not in entry["known_layers"],
    }
    result = check_link(entry, protocol)
    flags = _flags(result["checks"], comparison)

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Is the T7 order-and-count geometry estimator registered as a "
                         "first-class, scoped correspondence the core may reference, "
                         "without promoting it?"),
            "claim_id": claim_id,
            "scope": protocol["scope"],
            "status": "Track-B exploratory / correspondence (Status M); no physical claim",
        },
        "link": {key: value for key, value in entry.items()
                 if key not in {"all_evidence_statuses", "known_layers"}},
        "registry": {
            "claim_count": len(module.CLAIMS),
            "evidence_status_vocabulary": list(EVIDENCE_STATUS_VOCABULARY),
            "primary_development_sequence": list(module.PRIMARY_DEVELOPMENT_SEQUENCE),
            "estimator_module": estimator,
            "estimator_module_status": module.module_status(estimator),
        },
        "checks": result["checks"],
        "evidence_links": result["evidence_links"],
        "open_gaps": result["open_gaps"],
        "comparison": comparison,
        "flags": flags,
        "verdict": (
            "QR-05DN (direction J, the governed link): the T7 order-and-count geometry "
            "estimator is registered as a first-class **correspondence** claim "
            "(`DET8-T7-LINK`, layer `CORRESPONDENCE`, evidence "
            "`BOUNDED_CONDITIONAL_RESULT`, development `DEFERRED`) with its **scope** "
            "(1+1 primary; supplied Minkowski samples; estimator verification only; no "
            "manifoldlike emergence, no native derivation, no metric/continuum/curvature/"
            "dynamics, no gravity), its **O7 target pointer**, and its **open gaps** "
            "recorded with resolving pointers. The non-promotion invariants hold "
            "executably: the estimator stays outside the supported core exports and "
            "classifies EXPERIMENTAL, and the claim does not enter the primary "
            "development sequence, so it cannot unlock gated work. Only the existing "
            "evidence-status vocabulary is used (one new *layer* label is introduced, "
            "which is the link's own classification). Correspondence-level; no physical "
            "claim."),
    }
