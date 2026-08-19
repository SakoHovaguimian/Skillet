#!/usr/bin/env python3
"""Fetch globally shared Rune ubiquitous components catalog into a workspace."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch globally shared Rune UBIQUITOUS_COMPONENTS catalog."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/UBIQUITOUS_COMPONENTS_GLOBAL.md"),
        help="Output path for local copy (relative to --workspace unless absolute).",
    )
    parser.add_argument(
        "--global-input",
        type=Path,
        default=None,
        help=(
            "Optional override path to global source catalog "
            "(default: <shared-home>/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md, "
            "where <shared-home> is $SKILLET_SHARED_HOME, else $CODEX_HOME, else ~/.codex)."
        ),
    )
    parser.add_argument(
        "--read-only",
        action="store_true",
        help="Do not write local copy; only report source path and size.",
    )
    return parser.parse_args()


def shared_home() -> Path:
    for env_var in ("SKILLET_SHARED_HOME", "CODEX_HOME"):
        raw = os.environ.get(env_var, "").strip()
        if raw:
            return Path(raw).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def default_global_input() -> Path:
    return shared_home() / "shared" / "ubiquitous-components" / "rune" / "UBIQUITOUS_COMPONENTS.md"


def run() -> int:
    args = parse_args()

    workspace = args.workspace.resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"[ERROR] Workspace not found: {workspace}", file=sys.stderr)
        return 1

    if args.global_input is None:
        global_input = default_global_input()
    else:
        global_input = args.global_input.expanduser()
        if not global_input.is_absolute():
            global_input = (workspace / global_input).resolve()

    if not global_input.exists() or not global_input.is_file():
        print(f"[ERROR] Global catalog not found: {global_input}", file=sys.stderr)
        print("        Run $ubiquitous-components in any Rune project to publish it first.", file=sys.stderr)
        return 2

    content = global_input.read_text(encoding="utf-8")
    line_count = content.count("\n")
    byte_count = len(content.encode("utf-8"))
    metadata_path = global_input.with_name("UBIQUITOUS_COMPONENTS.metadata.json")
    metadata_generated_at = ""
    if metadata_path.exists() and metadata_path.is_file():
        try:
            metadata_payload = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata_generated_at = str(metadata_payload.get("generated_at", "")).strip()
        except Exception:
            metadata_generated_at = ""

    if args.read_only:
        print(f"[OK] Global source: {global_input}")
        if metadata_generated_at:
            print(f"[OK] Global generated_at: {metadata_generated_at}")
        print(f"[OK] Lines: {line_count} | Bytes: {byte_count}")
        return 0

    output_path = args.output
    if not output_path.is_absolute():
        output_path = (workspace / output_path).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Global source: {global_input}")
    if metadata_generated_at:
        print(f"[OK] Global generated_at: {metadata_generated_at}")
    print(f"[OK] Wrote local copy: {output_path}")
    print(f"[OK] Lines: {line_count} | Bytes: {byte_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
