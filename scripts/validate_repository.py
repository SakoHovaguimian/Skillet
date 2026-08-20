#!/usr/bin/env python3
"""Validate Skillet's repository-level skill authoring contract."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
README = ROOT / "README.md"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CALLEE_RE = re.compile(r"\$([a-z][a-z0-9-]*)")
DECLARED_CALLEE_RE = re.compile(r"^\|\s*`\$([a-z][a-z0-9-]*)`\s*\|", re.MULTILINE)
README_SKILL_RE = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|", re.MULTILINE)
SCRIPT_REFERENCE_RE = re.compile(r"<skill-dir>/scripts/([A-Za-z0-9_.-]+\.py)")
BARE_SCRIPT_RE = re.compile(r"(?<!<skill-dir>/)(?<![A-Za-z0-9_.-])scripts/[A-Za-z0-9_.-]+\.py")
LOCAL_LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
ABSOLUTE_USER_PATH_RE = re.compile(r"(?:/Users/[^/<\s]+|/home/[^/<\s]+|[A-Za-z]:\\Users\\[^\\\s]+)")

SECTION_ORDER = [
    "Outcome",
    "Inputs and preconditions",
    "Workflow",
    "Constraints",
    "Composition",
    "Failure handling",
    "Output contract",
]
REQUIRED_SECTIONS = {
    "Outcome",
    "Inputs and preconditions",
    "Workflow",
    "Constraints",
    "Output contract",
}

CANONICAL_HYGIENE = """
Invoke `$unslop` once on the complete user-facing artifact after its technical
content is final, unless a parent workflow owns the final artifact, in which
case the outermost workflow makes the single pass. `$unslop` may improve prose
but must not change technical meaning: preserve code, paths, symbols, commands,
measurements, quoted decisions, evidence anchors, classification labels, and
document structure. If `$unslop` is unavailable, deliver the artifact unchanged
and note the skipped pass.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate all Skillet skills and helpers.")
    parser.add_argument(
        "--skip-helpers",
        action="store_true",
        help="Skip executing each Python helper with --help.",
    )
    return parser.parse_args()


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def outside_fences(markdown: str) -> str:
    kept: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append(line)
    return "\n".join(kept)


def split_frontmatter(text: str, path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{path}: missing opening YAML frontmatter delimiter")
        return {}, text
    try:
        closing = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path}: missing closing YAML frontmatter delimiter")
        return {}, text

    values: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values, "\n".join(lines[closing + 1 :])


def validate_skill(skill_dir: Path, all_names: set[str], errors: list[str]) -> None:
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    metadata_file = skill_dir / "agents" / "openai.yaml"
    label = skill_file.relative_to(ROOT)

    if not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"{label}: folder name must be kebab-case and at most 64 characters")
    if not skill_file.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
        return
    if not metadata_file.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing agents/openai.yaml")

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text, label, errors)
    if frontmatter.get("name") != name:
        errors.append(f"{label}: frontmatter name must match folder name {name!r}")
    if frontmatter.get("disable-model-invocation") != "true":
        errors.append(f"{label}: disable-model-invocation must be true")

    description = frontmatter.get("description", "")
    if not description:
        errors.append(f"{label}: missing description")
    elif "Use when " not in description:
        errors.append(f"{label}: description must include concrete 'Use when ...' routing cues")
    if re.search(r"\b(?:Codex|Claude)\b", description):
        errors.append(f"{label}: description must be agent-neutral")

    visible_body = outside_fences(body)
    h1s = re.findall(r"^# (.+)$", visible_body, re.MULTILINE)
    if len(h1s) != 1:
        errors.append(f"{label}: expected exactly one H1, found {len(h1s)}")

    sections = re.findall(r"^## (.+)$", visible_body, re.MULTILINE)
    unknown_sections = [section for section in sections if section not in SECTION_ORDER]
    if unknown_sections:
        errors.append(f"{label}: renamed or unknown H2 sections: {', '.join(unknown_sections)}")
    missing = sorted(REQUIRED_SECTIONS - set(sections))
    if missing:
        errors.append(f"{label}: missing required sections: {', '.join(missing)}")
    order_positions = [SECTION_ORDER.index(section) for section in sections if section in SECTION_ORDER]
    if order_positions != sorted(order_positions):
        errors.append(f"{label}: H2 sections do not follow the canonical section order")

    mentioned = set(CALLEE_RE.findall(visible_body))
    declared = set(DECLARED_CALLEE_RE.findall(visible_body))
    undeclared = sorted(mentioned - declared)
    if undeclared:
        errors.append(f"{label}: callees missing Composition rows: {', '.join('$' + item for item in undeclared)}")
    missing_callees = sorted(mentioned - all_names)
    if missing_callees:
        errors.append(f"{label}: referenced skills are absent from skills/: {', '.join('$' + item for item in missing_callees)}")

    for row in re.findall(r"^\|\s*`\$[a-z][a-z0-9-]*`.*$", visible_body, re.MULTILINE):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != 5 or not all(cells):
            errors.append(f"{label}: each Composition row needs five non-empty cells")

    normalized_body = normalize_whitespace(visible_body)
    if "Invoke `$unslop` once on the complete user-facing artifact" in visible_body:
        if normalize_whitespace(CANONICAL_HYGIENE) not in normalized_body:
            errors.append(f"{label}: writing-hygiene block differs from the canonical verbatim text")

    for match in BARE_SCRIPT_RE.finditer(visible_body):
        errors.append(f"{label}: bare script path is not portable: {match.group(0)}")
    for portable_file in sorted(skill_dir.rglob("*")):
        if not portable_file.is_file() or portable_file.suffix not in {".md", ".py", ".yaml", ".yml"}:
            continue
        portable_text = portable_file.read_text(encoding="utf-8")
        if ABSOLUTE_USER_PATH_RE.search(portable_text):
            errors.append(f"{portable_file.relative_to(ROOT)}: contains an absolute user path")
    if "/path/to/" in text:
        errors.append(f"{label}: contains a forbidden /path/to/... placeholder")

    for script_name in SCRIPT_REFERENCE_RE.findall(text):
        if not (skill_dir / "scripts" / script_name).is_file():
            errors.append(f"{label}: referenced helper does not exist: scripts/{script_name}")
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for helper in sorted(scripts_dir.glob("*.py")):
            expected = f"<skill-dir>/scripts/{helper.name}"
            if expected not in text:
                errors.append(f"{label}: bundled helper is not invoked with the portable path: {expected}")

    if metadata_file.is_file():
        metadata = metadata_file.read_text(encoding="utf-8")
        if not re.search(r"(?m)^\s{2}allow_implicit_invocation:\s*false\s*$", metadata):
            errors.append(f"{metadata_file.relative_to(ROOT)}: allow_implicit_invocation must be false")
        prompt_match = re.search(r'(?m)^\s{2}default_prompt:\s*"([^"]*)"\s*$', metadata)
        if not prompt_match:
            errors.append(f"{metadata_file.relative_to(ROOT)}: missing quoted interface.default_prompt")
        elif f"${name}" not in prompt_match.group(1):
            errors.append(f"{metadata_file.relative_to(ROOT)}: default_prompt must mention ${name}")


def validate_readme(skill_names: set[str], errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    inventory = set(README_SKILL_RE.findall(text))
    missing = sorted(skill_names - inventory)
    stale = sorted(inventory - skill_names)
    if missing:
        errors.append(f"README.md: skills missing from inventory: {', '.join(missing)}")
    if stale:
        errors.append(f"README.md: inventory names without skill folders: {', '.join(stale)}")


def validate_links(errors: list[str]) -> None:
    for markdown_file in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown_file.parts:
            continue
        text = markdown_file.read_text(encoding="utf-8")
        for raw_target in LOCAL_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target):
                continue
            resolved = (markdown_file.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{markdown_file.relative_to(ROOT)}: broken local link: {raw_target}")


def validate_helpers(skill_dirs: Sequence[Path], errors: list[str]) -> None:
    for skill_dir in skill_dirs:
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.is_dir():
            continue
        for helper in sorted(scripts_dir.glob("*.py")):
            try:
                result = subprocess.run(
                    [sys.executable, str(helper), "--help"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"{helper.relative_to(ROOT)}: --help timed out")
                continue
            if result.returncode != 0:
                details = (result.stderr or result.stdout).strip().splitlines()
                suffix = f" ({details[-1]})" if details else ""
                errors.append(f"{helper.relative_to(ROOT)}: --help exited {result.returncode}{suffix}")

    dead_code_helper = SKILLS_ROOT / "dead-code-scanner" / "scripts" / "dead_code_scanner.py"
    if dead_code_helper.is_file():
        with tempfile.TemporaryDirectory(prefix="skillet-validator-") as temp_dir:
            missing_root = Path(temp_dir) / "missing"
            result = subprocess.run(
                [sys.executable, str(dead_code_helper), str(missing_root), "--json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            if result.returncode == 0 or "Root does not exist" not in result.stderr:
                errors.append(
                    "skills/dead-code-scanner/scripts/dead_code_scanner.py: nonexistent roots must fail clearly"
                )


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, skill_names, errors)
    validate_readme(skill_names, errors)
    validate_links(errors)
    if not args.skip_helpers:
        validate_helpers(skill_dirs, errors)

    if errors:
        print(f"Repository validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    helper_count = sum(1 for skill_dir in skill_dirs for _ in (skill_dir / "scripts").glob("*.py"))
    helper_note = "helper execution skipped" if args.skip_helpers else f"{helper_count} helpers loaded"
    print(f"Repository validation passed: {len(skill_dirs)} skills, {helper_note}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
