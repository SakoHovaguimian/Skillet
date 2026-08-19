#!/usr/bin/env python3
"""Validate Skillet's dependency-free skill structure contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(
    r"^(name|description|disable-model-invocation):\s*(.+?)\s*$"
)


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    if not lines or lines[0] != "---":
        return {}, ["SKILL.md must start with --- on the first line"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["SKILL.md frontmatter must end with a line containing only ---"]

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = FIELD_PATTERN.match(line)
        if match:
            fields[match.group(1)] = unquote(match.group(2).strip())

    for required in ("name", "description"):
        if not fields.get(required):
            errors.append(f"frontmatter is missing a non-empty {required}")

    return fields, errors


def has_explicit_only_policy(path: Path) -> bool:
    in_policy = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "policy:":
            in_policy = True
            continue
        if in_policy and line and not line[0].isspace():
            return False
        if in_policy and line.strip() == "allow_implicit_invocation: false":
            return True
    return False


def main() -> int:
    errors: list[str] = []

    if not SKILLS_DIR.is_dir():
        print("ERROR: skills/ does not exist", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("skills/ contains no skill directories")

    declared_names: set[str] = set()
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        label = skill_dir.relative_to(ROOT)

        if not skill_file.is_file():
            errors.append(f"{label}: missing SKILL.md")
            continue

        fields, file_errors = frontmatter(skill_file)
        errors.extend(f"{label}: {message}" for message in file_errors)

        name = fields.get("name")
        if not name:
            continue
        if name != skill_dir.name:
            errors.append(f"{label}: frontmatter name {name!r} must match the folder name")
        if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
            errors.append(f"{label}: name must be at most 64 lowercase letters, digits, or hyphens")
        if name in declared_names:
            errors.append(f"{label}: duplicate skill name {name!r}")
        declared_names.add(name)

        if fields.get("disable-model-invocation") != "true":
            errors.append(
                f"{label}: SKILL.md must set disable-model-invocation to true"
            )

        openai_file = skill_dir / "agents" / "openai.yaml"
        if not openai_file.is_file():
            errors.append(f"{label}: missing required agents/openai.yaml")
        elif not has_explicit_only_policy(openai_file):
            errors.append(
                f"{label}: agents/openai.yaml must set "
                "policy.allow_implicit_invocation to false"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
