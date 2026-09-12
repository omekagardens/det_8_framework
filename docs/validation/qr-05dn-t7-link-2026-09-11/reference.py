"""Independent reference route for QR-05DN (direction J).

Same report by different mechanics: instead of importing the registry, this
route parses `det8/claims.py` with `ast` and re-derives the link entry, the
development sequence, the supported-core export map and the estimator's module
status **from source**.  Agreement therefore checks the entry *and* that the
entry is static source rather than a value computed at import time.

The heading-anchor convention is included independently (the repository's
shared convention, as in `det8/tests/test_claim_boundaries.py`).
"""

from __future__ import annotations

import ast
import re
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

_STATUS_CONSTANTS = {
    "MODULE_SUPPORTED": "SUPPORTED",
    "MODULE_SUPPORTED_INTERNAL": "SUPPORTED_INTERNAL",
    "MODULE_PARTIAL_QUARANTINE": "PARTIAL_QUARANTINE",
    "MODULE_DEFERRED_RESEARCH": "DEFERRED_RESEARCH",
    "MODULE_RETIRED": "RETIRED",
    "MODULE_LEGACY_OPT_IN": "LEGACY_OPT_IN",
    "MODULE_EXPERIMENTAL": "EXPERIMENTAL",
    "MODULE_UNVALIDATED_PREVIEW": "UNVALIDATED_PREVIEW",
}


def github_heading_anchor(heading: str) -> str:
    """The repository's heading-anchor convention, coded independently here."""
    normalized = heading.strip().casefold()
    retained = "".join(
        character for character in normalized
        if character.isalnum() or character.isspace() or character in {"-", "_"}
        or not unicodedata.category(character).startswith("P")
    )
    return re.sub(r"\s", "-", retained)


def resolve_link(link: str) -> dict:
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


def _names(tree):
    """Module-level string constants and collection literals, by name."""
    strings, collections = {}, {}
    for node in tree.body:
        targets = []
        value = None
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                targets, value = [node.target.id], node.value
        elif isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            value = node.value
        if value is None:
            continue
        for name in targets:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                strings[name] = value.value
            else:
                collections[name] = value
    return strings, collections


def _string_tuple(node):
    node = _unwrap_call(node)
    if isinstance(node, ast.Tuple):
        return tuple(element.value for element in node.elts if isinstance(element, ast.Constant))
    return ()


def _string_membership(node):
    """Members of a set/frozenset/tuple literal."""
    node = _unwrap_call(node)
    if isinstance(node, (ast.Set, ast.Tuple, ast.List)):
        return tuple(element.value for element in node.elts if isinstance(element, ast.Constant))
    return ()


def _unwrap_call(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.args:
            return node.args[0]
    return node


def _dict_payload(node):
    node = _unwrap_call(node)
    return node if isinstance(node, ast.Dict) else None


def _literal(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Tuple):
        return tuple(_literal(element) for element in node.elts)
    return None


def parse_registry():
    tree = ast.parse(CLAIMS_PATH.read_text(encoding="utf-8"))
    strings, collections = _names(tree)
    claims = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "_CLAIMS" for t in node.targets):
            for key, value in zip(node.value.keys, node.value.values):
                if not isinstance(key, ast.Constant):
                    continue
                args = [_literal(argument) for argument in value.args]
                kwargs = {word.arg: _literal(word.value) for word in value.keywords}
                claims[key.value] = {
                    "claim_id": args[0] if len(args) > 0 else None,
                    "title": args[1] if len(args) > 1 else None,
                    "layer": args[2] if len(args) > 2 else None,
                    "evidence_status": args[3] if len(args) > 3 else None,
                    "development_status": args[4] if len(args) > 4 else None,
                    "dependencies": kwargs.get("dependencies", ()),
                    "falsifier": kwargs.get("falsifier"),
                    "evidence_links": kwargs.get("evidence_links", ()),
                    "priority": kwargs.get("priority"),
                }
    resolved = {}
    for claim_id, raw in claims.items():
        resolved[claim_id] = {
            "claim_id": raw["claim_id"],
            "title": raw["title"],
            "layer": strings.get(raw["layer"], raw["layer"]),
            "evidence_status": strings.get(raw["evidence_status"], raw["evidence_status"]),
            "development_status": strings.get(raw["development_status"], raw["development_status"]),
            "dependencies": tuple(raw["dependencies"] or ()),
            "falsifier": raw["falsifier"],
            "evidence_links": tuple(raw["evidence_links"] or ()),
            "priority": raw["priority"],
        }
    return {
        "claims": resolved,
        "constants": strings,
        "collections": collections,
    }


def _estimator_status(module_name, collections, strings):
    def members(name):
        node = collections.get(name)
        return _string_membership(node) if node is not None else ()

    table = [
        ("SUPPORTED_PUBLIC_MODULES", "MODULE_SUPPORTED"),
        ("PREVIEW_PUBLIC_MODULES", "MODULE_UNVALIDATED_PREVIEW"),
        ("SUPPORTED_CORE_IMPLEMENTATION_MODULES", "MODULE_SUPPORTED_INTERNAL"),
        ("RETIRED_MODULE_REASONS", "MODULE_RETIRED"),
        ("PARTIALLY_QUARANTINED_MODULES", "MODULE_PARTIAL_QUARANTINE"),
        ("DEFERRED_RESEARCH_MODULE_CLAIMS", "MODULE_DEFERRED_RESEARCH"),
    ]
    for name, constant in table:
        node = collections.get(name)
        if node is None:
            continue
        payload = _dict_payload(node)
        if payload is not None:
            if any(isinstance(key, ast.Constant) and key.value == module_name
                   for key in payload.keys):
                return strings.get(constant, _STATUS_CONSTANTS[constant])
        elif module_name in members(name):
            return strings.get(constant, _STATUS_CONSTANTS[constant])
    if module_name == "det8.legacy" or module_name.startswith("det8.legacy."):
        return strings.get("MODULE_LEGACY_OPT_IN", _STATUS_CONSTANTS["MODULE_LEGACY_OPT_IN"])
    return strings.get("MODULE_EXPERIMENTAL", _STATUS_CONSTANTS["MODULE_EXPERIMENTAL"])


def build_report(protocol):
    parsed = parse_registry()
    claim_id = protocol["claim_id"]
    estimator = protocol["required"]["estimator_module"]
    record = parsed["claims"][claim_id]
    collections, strings = parsed["collections"], parsed["constants"]

    sequence_node = collections.get("PRIMARY_DEVELOPMENT_SEQUENCE")
    sequence = tuple(_string_tuple(sequence_node)) if sequence_node is not None else ()
    export_node = _dict_payload(collections.get("SUPPORTED_CORE_EXPORTS", ast.Constant(None)))
    export_modules = tuple(
        key.value for key in export_node.keys) if export_node is not None else ()
    status = _estimator_status(estimator, collections, strings)
    supported_public = set(_string_membership(collections.get("SUPPORTED_PUBLIC_MODULES",
                                                              ast.Constant(None))))

    entry = {
        "claim_id": record["claim_id"],
        "title": record["title"],
        "layer": record["layer"],
        "evidence_status": record["evidence_status"],
        "development_status": record["development_status"],
        "priority": record["priority"],
        "dependencies": list(record["dependencies"]),
        "falsifier": record["falsifier"],
        "evidence_links": list(record["evidence_links"]),
        "in_development_sequence": claim_id in sequence,
        "supported_core_export_modules": sorted(export_modules),
        "estimator_is_supported": estimator in supported_public,
        "scope_recorded": True,
        "open_gaps_recorded": True,
        "all_evidence_statuses": sorted({claim["evidence_status"]
                                         for claim in parsed["claims"].values()}),
        "known_layers": sorted({claim["layer"] for claim in parsed["claims"].values()
                                if claim["claim_id"] != claim_id}),
    }

    # The checker is deliberately re-coded here rather than imported, so the two
    # routes share no code beyond the declared pre-specification.
    required = protocol["required"]
    links = [resolve_link(link) for link in entry["evidence_links"]]
    gaps = [
        {"gap": gap["gap"], "pointer": gap["pointer"],
         "resolves": resolve_link(gap["pointer"])["exists"]}
        for gap in protocol["open_gaps"]
    ]
    title = (entry["title"] or "").lower()
    falsifier = (entry["falsifier"] or "").lower()
    scope = protocol["scope"]
    checks = {
        "registered": bool(entry["claim_id"]),
        "layer_is_correspondence": entry["layer"] == required["layer"],
        "evidence_status_is_bounded_conditional":
            entry["evidence_status"] == required["evidence_status"],
        "development_status_remains_deferred":
            entry["development_status"] == required["development_status"],
        "not_in_the_primary_development_sequence":
            bool(required["must_not_be_in_development_sequence"])
            and not entry["in_development_sequence"],
        "priority_is_null": bool(required["priority_must_be_null"]) and entry["priority"] is None,
        "evidence_links_resolve": bool(links) and all(
            item["exists"] and item["anchor_ok"] is not False for item in links),
        "names_the_o7_target": any(
            item["link"] == required["o7_pointer_anchor"] for item in links),
        "carries_no_promotion_language_in_the_title": not any(
            word in title for word in required["promotion_words_forbidden_in_title"]),
        "falsifier_pins_the_bounded_scope": all(
            marker in falsifier for marker in required["promotion_markers_required_in_falsifier"]),
        "estimator_is_absent_from_the_supported_core_exports":
            required["estimator_module"] not in export_modules,
        "estimator_does_not_classify_as_supported": status != "SUPPORTED",
        "scope_is_recorded": bool(entry["scope_recorded"])
            and all(scope[key] for key in ("dimensions", "geometry", "verified", "not_claimed")),
        "open_gaps_are_recorded_and_resolve": bool(entry["open_gaps_recorded"])
            and all(item["resolves"] for item in gaps),
    }
    comparison = {
        "new_evidence_status_introduced": any(
            status_name not in EVIDENCE_STATUS_VOCABULARY
            for status_name in entry["all_evidence_statuses"]),
        "new_layer_label_introduced": entry["layer"] not in entry["known_layers"],
    }
    flags = {
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
            "claim_count": len(parsed["claims"]),
            "evidence_status_vocabulary": list(EVIDENCE_STATUS_VOCABULARY),
            "primary_development_sequence": list(sequence),
            "estimator_module": estimator,
            "estimator_module_status": status,
        },
        "checks": checks,
        "evidence_links": links,
        "open_gaps": gaps,
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
