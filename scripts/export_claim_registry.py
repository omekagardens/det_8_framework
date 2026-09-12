"""Render the authoritative registry as Markdown, or check its checked-in summary.

Run from an installed checkout. The renderer only emits text or compares files;
it never promotes evidence, edits the registry, or performs publication.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from det8.claims import registry_document


def render_markdown() -> str:
    registry = registry_document()
    lines = [
        "# DET8 public-program claim registry", "",
        "Generated from `det8.claims`; do not maintain a separate status table by hand.",
        "Run `python scripts/export_claim_registry.py --check` to verify synchronization.", "",
        "This is the bounded supported/public-program registry, not validation of every",
        "historical research claim. Software evidence does not promote physical claims.",
        "Unlisted research APIs are experimental by default. Gate completion requires",
        "its own dated report under `docs/validation/`.", "",
        "| ID | Layer | Evidence status | Development status |",
        "|---|---|---|---|",
    ]
    for claim in registry["claims"]:
        lines.append(f"| {claim['claim_id']} | {claim['layer']} | {claim['evidence_status']} | {claim['development_status']} |")
    for claim in registry["claims"]:
        lines.extend([
            "", f"## {claim['claim_id']} — {claim['title']}", "",
            "Dependencies: " + (", ".join(claim["dependencies"]) or "none") + ".", "",
            "Failure or withdrawal condition: " + claim["falsifier"], "",
            "Evidence / scope links:", "",
        ])
        lines.extend(f"- [{link}](../{link})" for link in claim["evidence_links"])
    lines.extend([
        "", "## Supported public modules", "",
        *[f"- `{name}`" for name in registry["supported_public_modules"]],
        "", "## Unvalidated development-preview namespaces", "",
        *[f"- `{name}` — G2 is not closed; see [RET_SDK.md](RET_SDK.md)." for name in registry["preview_public_modules"]],
        "", "Exact exports, partial quarantine, and the retired-module ledger are available",
        "through `det8.claims.registry_document()`. See [CORE_API.md](CORE_API.md) for",
        "compatibility notes and explicit historical opt-in behavior.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = render_markdown()
    if args.check:
        path = Path(__file__).resolve().parents[1] / "docs" / "CLAIM_REGISTRY.md"
        if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
            print("claim registry summary is missing or out of date")
            return 1
        print("claim registry summary matches det8.claims")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
