#!/usr/bin/env python3
"""Update documentation with provider/action counts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_FILE = "CATALOG.md"
PROVIDER_DOC = ROOT / PROVIDER_FILE
README_DOC = ROOT / "README.md"
PROVIDERS_DIR = ROOT / "src" / "integrations" / "providers"
STATS_PREFIX = "> **Stats**:"
README_CALLOUT_PREFIX = "> **Provider catalog:**"


def count_providers_and_actions(providers_dir: Path) -> tuple[int, int]:
    providers = []
    total_actions = 0

    for child in sorted(providers_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("__"):
            continue

        providers.append(child)
        actions_dir = child / "actions"
        if not actions_dir.exists():
            continue

        for action_file in actions_dir.rglob("*.py"):
            if action_file.name == "__init__.py":
                continue
            total_actions += 1

    return len(providers), total_actions


def update_provider_doc(doc_path: Path, provider_count: int, action_count: int) -> None:
    if not doc_path.exists():
        raise FileNotFoundError(f"Missing provider catalog: {doc_path}")

    stats_line = (
        f"{STATS_PREFIX} {provider_count} providers, {action_count} actions."
        if action_count != 1
        else f"{STATS_PREFIX} {provider_count} providers, {action_count} action."
    )

    lines = doc_path.read_text(encoding="utf-8").splitlines()

    if len(lines) < 1 or not lines[0].startswith("# Providers Catalog"):
        raise RuntimeError(f"Unexpected {PROVIDER_FILE} format: missing heading")

    if len(lines) > 1 and lines[1].startswith(STATS_PREFIX):
        lines[1] = stats_line
    else:
        lines.insert(1, stats_line)

    # Keep a blank line after the stats block for readability.
    if len(lines) < 3 or lines[2] != "":
        lines.insert(2, "")

    doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_readme(readme_path: Path, provider_count: int, action_count: int) -> None:
    if not readme_path.exists():
        raise FileNotFoundError(f"Missing README: {readme_path}")

    providers_label = "provider" if provider_count == 1 else "providers"
    actions_label = "action" if action_count == 1 else "actions"
    callout_line = (
        f"{README_CALLOUT_PREFIX} {provider_count} {providers_label}, "
        f"{action_count} {actions_label} — see [{PROVIDER_FILE}]({PROVIDER_FILE})."
    )

    lines = readme_path.read_text(encoding="utf-8").splitlines()

    if not lines or not lines[0].startswith("# "):
        raise RuntimeError("Unexpected README.md format: missing top-level heading")

    callout_index: int | None = None
    search_window = min(len(lines), 8)
    for idx in range(1, search_window):
        if lines[idx].startswith(README_CALLOUT_PREFIX):
            callout_index = idx
            break

    if callout_index is None:
        insert_at = 1
        if len(lines) > insert_at and lines[insert_at] == "":
            lines[insert_at] = callout_line
        else:
            lines.insert(insert_at, callout_line)
            insert_at = min(insert_at, len(lines) - 1)

        after_index = insert_at + 1
        if after_index >= len(lines) or lines[after_index] != "":
            lines.insert(after_index, "")
        else:
            while after_index + 1 < len(lines) and lines[after_index + 1] == "":
                del lines[after_index + 1]
    else:
        lines[callout_index] = callout_line
        after_index = callout_index + 1
        if after_index >= len(lines) or lines[after_index] != "":
            lines.insert(after_index, "")
        else:
            while after_index + 1 < len(lines) and lines[after_index + 1] == "":
                del lines[after_index + 1]

    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    provider_count, action_count = count_providers_and_actions(PROVIDERS_DIR)
    update_provider_doc(PROVIDER_DOC, provider_count, action_count)
    update_readme(README_DOC, provider_count, action_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
