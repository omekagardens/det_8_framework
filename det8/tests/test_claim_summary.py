"""The public Markdown summary must derive from the authoritative registry."""

from pathlib import Path

from scripts.export_claim_registry import render_markdown


def test_generated_claim_summary_matches_registry():
    root = Path(__file__).resolve().parents[2]
    assert (root / "docs" / "CLAIM_REGISTRY.md").read_text(encoding="utf-8") == render_markdown()
