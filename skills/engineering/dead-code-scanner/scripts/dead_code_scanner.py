#!/usr/bin/env python3
"""Index language-neutral dead-code signals without assigning removal verdicts."""

from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    import tomllib
except ImportError:  # Python 3.10 still runs the scanner without TOML dependency hints.
    tomllib = None


EXCLUDED_DIRS = {
    ".build",
    ".git",
    ".gradle",
    ".idea",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".swiftpm",
    ".tox",
    ".venv",
    ".vscode",
    "Build",
    "Carthage",
    "DerivedData",
    "Pods",
    "SourcePackages",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

SOURCE_LANGUAGES = {
    ".c": "C",
    ".cc": "C++",
    ".cjs": "JavaScript",
    ".cpp": "C++",
    ".cs": "C#",
    ".cts": "TypeScript",
    ".cxx": "C++",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".go": "Go",
    ".h": "C/C++ header",
    ".hpp": "C++ header",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".mjs": "JavaScript",
    ".mts": "TypeScript",
    ".php": "PHP",
    ".py": "Python",
    ".pyi": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
}

TEXT_EXTENSIONS = set(SOURCE_LANGUAGES) | {
    ".cfg",
    ".conf",
    ".css",
    ".graphql",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".plist",
    ".properties",
    ".proto",
    ".sh",
    ".sql",
    ".storyboard",
    ".strings",
    ".toml",
    ".txt",
    ".xib",
    ".xml",
    ".yaml",
    ".yml",
}

TEXT_FILENAMES = {
    "BUILD",
    "Gemfile",
    "Makefile",
    "Package.resolved",
    "Package.swift",
    "Podfile",
    "WORKSPACE",
    "go.mod",
    "package.json",
    "pyproject.toml",
}

SOURCE_EXCLUDED_FILENAMES = {"Package.swift"}

ASSET_EXTENSIONS = {
    ".avif",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".lottie",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".riv",
    ".svg",
    ".webm",
    ".webp",
    ".wav",
    ".woff",
    ".woff2",
}

SUPPORT_PARTS = {
    "__tests__",
    "benchmark",
    "benchmarks",
    "demo",
    "demos",
    "example",
    "examples",
    "fixture",
    "fixtures",
    "preview",
    "previews",
    "sample",
    "samples",
    "snapshot",
    "snapshots",
    "spec",
    "specs",
    "stories",
    "storybook",
    "test",
    "tests",
}

ENTRY_FILENAMES = {
    "__main__.py",
    "app.py",
    "cli.py",
    "index.js",
    "index.jsx",
    "index.cjs",
    "index.mjs",
    "index.cts",
    "index.mts",
    "index.ts",
    "index.tsx",
    "main.c",
    "main.cc",
    "main.cpp",
    "main.cs",
    "main.dart",
    "main.go",
    "main.java",
    "main.js",
    "main.kt",
    "main.py",
    "main.rs",
    "main.swift",
    "main.ts",
    "manage.py",
    "program.cs",
    "server.js",
    "server.py",
    "server.ts",
}

ENTRY_PATTERNS = (
    (re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]"), "Python main guard"),
    (re.compile(r"\brequire\.main\s*===\s*module\b"), "Node main guard"),
    (re.compile(r"^\s*@main\b", re.MULTILINE), "annotated main entry"),
    (re.compile(r"\bpublic\s+static\s+void\s+main\s*\("), "JVM main method"),
    (re.compile(r"^\s*func\s+main\s*\(", re.MULTILINE), "Go main function"),
    (re.compile(r"^\s*fn\s+main\s*\(", re.MULTILINE), "Rust main function"),
    (re.compile(r"^\s*fun\s+main\s*\(", re.MULTILINE), "Kotlin main function"),
)

WORD_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
MAX_TEXT_BYTES = 4 * 1024 * 1024


@dataclass(frozen=True)
class Declaration:
    language: str
    kind: str
    name: str
    path: Path
    line: int
    prefix: str = ""
    tail: str = ""

    @property
    def external_risk(self) -> bool:
        combined = f"{self.prefix} {self.tail}"
        markers = (
            "public",
            "open",
            "export",
            "pub",
            "@objc",
            "dynamic",
            "extern",
            "Codable",
            "Decodable",
            "Serializable",
        )
        protocol_kinds = {"interface", "protocol", "trait"}
        c_family_function = self.language in {"C", "C++", "C/C++ header"} and self.kind == "function"
        go_export = self.language == "Go" and self.name[:1].isupper()
        return (
            self.kind in protocol_kinds
            or any(marker in combined for marker in markers)
            or (c_family_function and "static" not in self.prefix)
            or go_export
        )


DECLARATION_PATTERNS: dict[str, Sequence[re.Pattern[str]]] = {
    "Python": (
        re.compile(r"^\s*(?P<prefix>async\s+)?(?P<kind>def|class)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "JavaScript": (
        re.compile(r"^\s*(?P<prefix>(?:export\s+(?:default\s+)?)?(?:async\s+)?)?(?P<kind>class|function)\s+(?P<name>[A-Za-z_$][\w$]*)", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)?(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)?(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?function\b", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=", re.MULTILINE),
    ),
    "TypeScript": (
        re.compile(r"^\s*(?P<prefix>(?:export\s+(?:default\s+)?)?(?:declare\s+)?(?:async\s+)?)?(?P<kind>class|function|interface|type|enum|namespace)\s+(?P<name>[A-Za-z_$][\w$]*)", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)?(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)?(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*(?:async\s+)?function\b", re.MULTILINE),
        re.compile(r"^\s*(?P<prefix>export\s+)(?P<kind>const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*(?::[^=]+)?=", re.MULTILINE),
    ),
    "Swift": (
        re.compile(r"^\s*(?P<prefix>(?:(?:public|open|internal|private|fileprivate|final|dynamic|@\w+(?:\([^)]*\))?)\s+)*)?(?P<kind>class|struct|enum|protocol|actor|func)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Kotlin": (
        re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|internal|open|data|sealed|abstract|export)\s+)*)?(?P<kind>class|interface|enum|object|fun|typealias)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Java": (
        re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|static|final|abstract|sealed)\s+)*)?(?P<kind>class|interface|enum|record)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Go": (
        re.compile(r"^\s*(?P<kind>func|type)\s+(?:\([^)]*\)\s+)?(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Rust": (
        re.compile(r"^\s*(?P<prefix>pub(?:\([^)]*\))?\s+)?(?P<kind>fn|struct|enum|trait|type|mod)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Ruby": (
        re.compile(r"^\s*(?P<kind>def|class|module)\s+(?P<name>[A-Za-z_]\w*[!?=]?)", re.MULTILINE),
    ),
    "PHP": (
        re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|final|abstract|static)\s+)*)?(?P<kind>class|interface|trait|function)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "C#": (
        re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|internal|static|sealed|abstract|partial)\s+)*)?(?P<kind>class|interface|struct|enum|record)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Dart": (
        re.compile(r"^\s*(?P<prefix>abstract\s+)?(?P<kind>class|enum|mixin|extension|typedef)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Scala": (
        re.compile(r"^\s*(?P<prefix>(?:(?:private|protected|sealed|abstract|final|case)\s+)*)?(?P<kind>class|trait|object|enum|def)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Elixir": (
        re.compile(r"^\s*(?P<kind>defmodule|defp|def)\s+(?P<name>[A-Za-z_][\w.!?]*)", re.MULTILINE),
    ),
    "C": (
        re.compile(r"^\s*(?P<prefix>extern\s+)?(?P<kind>struct|enum|union)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "C++": (
        re.compile(r"^\s*(?P<prefix>export\s+)?(?P<kind>class|struct|enum|union|namespace)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "C/C++ header": (
        re.compile(r"^\s*(?P<prefix>extern\s+|export\s+)?(?P<kind>class|struct|enum|union|namespace)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Objective-C": (
        re.compile(r"^\s*@(?P<kind>interface|protocol|implementation)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
    "Objective-C++": (
        re.compile(r"^\s*@(?P<kind>interface|protocol|implementation)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE),
    ),
}

C_FAMILY_FUNCTION_PATTERNS: dict[str, re.Pattern[str]] = {
    language: re.compile(
        r"^(?!\s*(?:if|for|while|switch|return|sizeof)\b)"
        r"\s*(?P<prefix>(?:(?:extern|static|inline|constexpr|const|volatile|unsigned|signed|long|short)\s+)*)"
        r"(?:[A-Za-z_]\w*(?:::[A-Za-z_]\w*)?(?:\s*[*&]+)?\s+)+"
        r"(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:\{|;)",
        re.MULTILINE,
    )
    for language in ("C", "C++", "C/C++ header")
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index cross-platform dead-code and low-value-reference candidates."
    )
    parser.add_argument("root", type=Path, help="Repository or source root to scan.")
    parser.add_argument(
        "--focus",
        action="append",
        type=Path,
        help="Relative file or directory inside the root to scan (repeatable).",
    )
    parser.add_argument(
        "--include-assets",
        action="store_true",
        help="Report assets with no path, filename, quoted-stem, or generated-identifier reference.",
    )
    parser.add_argument(
        "--include-dependencies",
        action="store_true",
        help="Report declared dependencies with no import-like lexical hit.",
    )
    parser.add_argument(
        "--max-reference-examples",
        type=int,
        default=4,
        metavar="COUNT",
        help="Maximum reference locations shown per symbol (default: 4).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def iter_files(roots: Iterable[Path]) -> Iterable[Path]:
    seen: set[Path] = set()
    for root in roots:
        if root.is_file():
            resolved = root.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield resolved
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
            for filename in sorted(filenames):
                path = (Path(dirpath) / filename).resolve()
                if path not in seen:
                    seen.add(path)
                    yield path


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def is_support_path(path: Path, root: Path) -> bool:
    rel = relative(path, root).lower()
    parts = set(Path(rel).parts)
    name = path.name.lower()
    return bool(parts & SUPPORT_PARTS) or any(
        marker in name
        for marker in ("_test.", ".test.", ".spec.", "test_", "tests.", "preview", "fixture")
    )


def validate_roots(root_arg: Path, focus_args: Sequence[Path] | None) -> tuple[Path, list[Path]]:
    root = root_arg.expanduser().resolve()
    if not root.exists():
        raise ValueError(f"Root does not exist: {root}")
    if not root.is_dir() and not root.is_file():
        raise ValueError(f"Root is not a regular file or directory: {root}")

    if not focus_args:
        return root, [root]
    if root.is_file():
        raise ValueError("--focus cannot be used when root is a file")

    scan_roots: list[Path] = []
    for focus in focus_args:
        resolved = focus.expanduser().resolve() if focus.is_absolute() else (root / focus).resolve()
        if not resolved.exists():
            raise ValueError(f"Focus path does not exist: {resolved}")
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise ValueError(f"Focus path must remain inside root: {resolved}") from error
        scan_roots.append(resolved)
    return root, scan_roots


def declarations_for(path: Path, text: str) -> list[Declaration]:
    language = SOURCE_LANGUAGES.get(path.suffix.lower())
    if language is None:
        return []

    line_offsets = [0] + [match.end() for match in re.finditer("\n", text)]

    def get_line(offset: int) -> int:
        return bisect.bisect_right(line_offsets, offset)

    def get_tail(match: re.Match[str]) -> str:
        line_end = text.find("\n", match.end("name"))
        if line_end == -1:
            line_end = len(text)
        return text[match.end("name") : line_end].strip()

    declarations: list[Declaration] = []
    for pattern in DECLARATION_PATTERNS.get(language, ()):
        for match in pattern.finditer(text):
            declarations.append(
                Declaration(
                    language=language,
                    kind=match.group("kind"),
                    name=match.group("name"),
                    path=path,
                    line=get_line(match.start("name")),
                    prefix=(match.groupdict().get("prefix") or "").strip(),
                    tail=get_tail(match),
                )
            )

    function_pattern = C_FAMILY_FUNCTION_PATTERNS.get(language)
    if function_pattern is not None:
        for match in function_pattern.finditer(text):
            declarations.append(
                Declaration(
                    language=language,
                    kind="function",
                    name=match.group("name"),
                    path=path,
                    line=get_line(match.start("name")),
                    prefix=(match.group("prefix") or "").strip(),
                    tail=get_tail(match),
                )
            )

    unique: dict[tuple[int, str], Declaration] = {}
    for declaration in declarations:
        key = (declaration.line, declaration.name)
        existing = unique.get(key)
        if existing is None or ("export" in declaration.prefix and "export" not in existing.prefix):
            unique[key] = declaration
    return list(unique.values())


def reference_index(
    source_text: dict[Path, str], declarations: Sequence[Declaration]
) -> dict[str, list[tuple[Path, int]]]:
    """Map declaration names to unique source-line reference locations."""
    definition_locations = {(item.path, item.line, item.name) for item in declarations}
    locations: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    names = {item.name for item in declarations}
    for path, text in source_text.items():
        for number, line in enumerate(text.splitlines(), start=1):
            for name in set(WORD_RE.findall(line)):
                if name not in names or (path, number, name) in definition_locations:
                    continue
                locations[name].append((path, number))
    return locations


def entry_point_hints(text_by_path: dict[Path, str], root: Path) -> list[dict[str, object]]:
    hints: list[dict[str, object]] = []
    manifest_names = {"package.json", "pyproject.toml", "Package.swift", "Cargo.toml", "go.mod"}
    for path, content in text_by_path.items():
        reasons: list[str] = []
        if path.name.lower() in ENTRY_FILENAMES:
            reasons.append("conventional entry filename")
        for pattern, label in ENTRY_PATTERNS:
            if pattern.search(content):
                reasons.append(label)
        if path.name in manifest_names:
            if any(marker in content for marker in ("scripts", "bin", "entry", "executable", "main")):
                reasons.append("manifest entry declaration")
        if reasons:
            hints.append({"path": relative(path, root), "reasons": sorted(set(reasons))})
    return hints


def reference_examples(
    locations: Sequence[tuple[Path, int]], root: Path, maximum: int
) -> list[str]:
    return [f"{relative(path, root)}:{line}" for path, line in locations[:maximum]]


def symbol_candidates(
    declarations: Sequence[Declaration],
    locations: dict[str, list[tuple[Path, int]]],
    source_text: dict[Path, str],
    root: Path,
    maximum: int,
) -> dict[str, list[dict[str, object]]]:
    groups: dict[str, list[dict[str, object]]] = {
        "unreferenced": [],
        "support_only": [],
        "narrowly_referenced": [],
    }
    for declaration in declarations:
        refs = locations.get(declaration.name, [])
        production_refs = [item for item in refs if not is_support_path(item[0], root)]
        support_refs = [item for item in refs if is_support_path(item[0], root)]
        production_files = {path for path, _ in production_refs}
        same_file_only = bool(production_refs) and production_files == {declaration.path}
        dynamic_pattern = re.compile(rf"['\"]{re.escape(declaration.name)}['\"]")
        dynamic_hint = any(dynamic_pattern.search(text) for text in source_text.values())

        item = {
            "path": relative(declaration.path, root),
            "line": declaration.line,
            "language": declaration.language,
            "kind": declaration.kind,
            "name": declaration.name,
            "production_reference_lines": len(production_refs),
            "support_reference_lines": len(support_refs),
            "production_reference_files": len(production_files),
            "same_file_only": same_file_only,
            "external_or_dynamic_risk": declaration.external_risk or dynamic_hint,
            "reference_examples": reference_examples(refs, root, maximum),
        }

        if not production_refs and not support_refs:
            groups["unreferenced"].append(item)
        elif not production_refs:
            groups["support_only"].append(item)
        elif len(production_files) <= 1:
            groups["narrowly_referenced"].append(item)

    for values in groups.values():
        values.sort(key=lambda item: (str(item["path"]), int(item["line"]), str(item["name"])))
    return groups


def asset_candidates(
    all_paths: Sequence[Path], text_blob: str, root: Path
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for path in all_paths:
        if path.suffix.lower() not in ASSET_EXTENSIONS:
            continue
        relative_path = relative(path, root)
        direct_references = {path.name, relative_path, f"./{relative_path}"}
        if any(reference in text_blob for reference in direct_references):
            continue
        stem = path.stem
        if len(stem) > 3:
            quoted_stem = re.compile(rf"(?P<quote>['\"]){re.escape(stem)}(?P=quote)")
            generated_identifier = (
                re.compile(rf"(?<![A-Za-z0-9_])\.{re.escape(stem)}\b")
                if re.fullmatch(r"[A-Za-z_]\w*", stem)
                else None
            )
            if quoted_stem.search(text_blob) or (
                generated_identifier is not None and generated_identifier.search(text_blob)
            ):
                continue
        try:
            byte_count = path.stat().st_size
        except OSError:
            byte_count = 0
        candidates.append(
            {
                "path": relative(path, root),
                "bytes": byte_count,
                "support_only": is_support_path(path, root),
            }
        )
    return sorted(candidates, key=lambda item: str(item["path"]))


def dependency_declarations(text_by_path: dict[Path, str], root: Path) -> list[dict[str, str]]:
    dependencies: list[dict[str, str]] = []
    for path, content in text_by_path.items():
        rel_path = relative(path, root)
        if path.name == "package.json":
            try:
                payload = json.loads(content)
            except json.JSONDecodeError:
                continue
            for table, scope in (("dependencies", "runtime"), ("optionalDependencies", "optional"), ("devDependencies", "development")):
                values = payload.get(table, {})
                if isinstance(values, dict):
                    for name in values:
                        dependencies.append({"name": name, "ecosystem": "npm", "scope": scope, "manifest": rel_path})
        elif path.name == "pyproject.toml":
            if tomllib is None:
                continue
            try:
                payload = tomllib.loads(content)
            except tomllib.TOMLDecodeError:
                continue
            project = payload.get("project", {})
            if isinstance(project, dict):
                project_dependencies = project.get("dependencies", [])
                if isinstance(project_dependencies, list):
                    for raw in project_dependencies:
                        match = re.match(r"([A-Za-z0-9_.-]+)", str(raw))
                        if match:
                            dependencies.append({"name": match.group(1), "ecosystem": "Python", "scope": "runtime", "manifest": rel_path})
                optional = project.get("optional-dependencies", {})
                if isinstance(optional, dict):
                    for values in optional.values():
                        if not isinstance(values, list):
                            continue
                        for raw in values:
                            match = re.match(r"([A-Za-z0-9_.-]+)", str(raw))
                            if match:
                                dependencies.append({"name": match.group(1), "ecosystem": "Python", "scope": "optional", "manifest": rel_path})
            poetry = payload.get("tool", {}).get("poetry", {}) if isinstance(payload.get("tool", {}), dict) else {}
            if isinstance(poetry, dict):
                for table, scope in (("dependencies", "runtime"), ("dev-dependencies", "development")):
                    values = poetry.get(table, {})
                    if isinstance(values, dict):
                        for name in values:
                            if name.lower() != "python":
                                dependencies.append({"name": name, "ecosystem": "Python", "scope": scope, "manifest": rel_path})
        elif path.name == "Cargo.toml":
            if tomllib is not None:
                try:
                    payload = tomllib.loads(content)
                except tomllib.TOMLDecodeError:
                    payload = {}

                cargo_tables: list[tuple[object, str]] = [
                    (payload.get("dependencies", {}), "runtime"),
                    (payload.get("dev-dependencies", {}), "development"),
                    (payload.get("build-dependencies", {}), "build"),
                ]
                workspace = payload.get("workspace", {})
                if isinstance(workspace, dict):
                    cargo_tables.append((workspace.get("dependencies", {}), "workspace"))
                targets = payload.get("target", {})
                if isinstance(targets, dict):
                    for target in targets.values():
                        if not isinstance(target, dict):
                            continue
                        cargo_tables.extend(
                            (
                                (target.get("dependencies", {}), "target"),
                                (target.get("dev-dependencies", {}), "target-development"),
                                (target.get("build-dependencies", {}), "target-build"),
                            )
                        )
                for table, scope in cargo_tables:
                    if isinstance(table, dict):
                        for name in table:
                            dependencies.append({"name": name, "ecosystem": "Cargo", "scope": scope, "manifest": rel_path})
            else:
                in_dependencies = False
                for line in content.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("["):
                        in_dependencies = stripped.endswith("dependencies]")
                        continue
                    if in_dependencies:
                        match = re.match(r"([A-Za-z0-9_-]+)\s*=", stripped)
                        if match:
                            dependencies.append({"name": match.group(1), "ecosystem": "Cargo", "scope": "review", "manifest": rel_path})
        elif path.name == "go.mod":
            for match in re.finditer(r"(?m)^\s*([A-Za-z0-9_.~/-]+)\s+v\d", content):
                dependencies.append({"name": match.group(1), "ecosystem": "Go", "scope": "review", "manifest": rel_path})
        elif path.name == "Gemfile":
            for match in re.finditer(r"(?m)^\s*gem\s+['\"]([^'\"]+)['\"]", content):
                dependencies.append({"name": match.group(1), "ecosystem": "Ruby", "scope": "review", "manifest": rel_path})
        elif path.name == "Podfile":
            for match in re.finditer(r"(?m)^\s*pod\s+['\"]([^'\"]+)['\"]", content):
                dependencies.append({"name": match.group(1), "ecosystem": "CocoaPods", "scope": "review", "manifest": rel_path})
        elif path.name == "Package.swift":
            for match in re.finditer(r"\.product\s*\(\s*name\s*:\s*['\"]([^'\"]+)['\"]", content):
                dependencies.append({"name": match.group(1), "ecosystem": "SwiftPM", "scope": "review", "manifest": rel_path})

    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for item in dependencies:
        unique[(item["ecosystem"], item["name"], item["manifest"])] = item
    return sorted(unique.values(), key=lambda item: (item["ecosystem"], item["name"], item["manifest"]))


def dependency_candidates(
    declarations: Sequence[dict[str, str]], source_blob: str
) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    lowered_source = source_blob.lower()
    for item in declarations:
        name = item["name"]
        variants = {name, name.split("/")[-1], name.replace("-", "_"), name.replace("-", "")}
        if name.lower() in lowered_source or any(
            re.search(rf"\b{re.escape(variant)}\b", source_blob, re.IGNORECASE)
            for variant in variants
            if variant
        ):
            continue
        candidates.append(item)
    return candidates


def emit_markdown(result: dict[str, object]) -> None:
    print("# Dead Code Static Scan")
    print()
    print(f"Root: `{result['root']}`")
    print(f"Source files scanned: {result['source_files_scanned']}")
    languages = result["languages"]
    print(f"Languages: {', '.join(f'{name} ({count})' for name, count in languages.items()) or 'none'}")
    print()

    print("## Entry Point Hints")
    hints = result["entry_point_hints"]
    if hints:
        for item in hints:
            print(f"- `{item['path']}`: {', '.join(item['reasons'])}")
    else:
        print("- No conventional entry point hints found. Establish live roots manually.")
    print()

    headings = (
        ("unreferenced", "Unreferenced Declarations"),
        ("support_only", "Support-Only Declarations"),
        ("narrowly_referenced", "Narrowly Referenced Declarations Requiring Value Audit"),
    )
    symbol_groups = result["symbol_candidates"]
    for key, heading in headings:
        print(f"## {heading}")
        items = symbol_groups[key]
        if not items:
            print("- None found by lexical scan.")
        for item in items:
            risk = "review dynamic/external use" if item["external_or_dynamic_risk"] else "no dynamic hint"
            print(
                f"- `{item['path']}:{item['line']}` `{item['kind']} {item['name']}`; "
                f"production reference lines: {item['production_reference_lines']}; "
                f"support reference lines: {item['support_reference_lines']}; {risk}"
            )
            if item["reference_examples"]:
                print(f"  References: {', '.join(f'`{location}`' for location in item['reference_examples'])}")
        print()

    if "asset_candidates" in result:
        print("## Asset Candidates")
        items = result["asset_candidates"]
        if items:
            for item in items:
                print(f"- `{item['path']}` ({item['bytes']} bytes)")
        else:
            print("- No assets without a path, filename, quoted-stem, or generated-identifier reference found.")
        print()

    if "dependency_candidates" in result:
        print("## Dependency Candidates")
        items = result["dependency_candidates"]
        if items:
            for item in items:
                print(f"- `{item['name']}` ({item['ecosystem']}, {item['scope']}) in `{item['manifest']}`")
        else:
            print("- No declared dependencies without an import-like lexical hit found.")
        print()

    print("Note: These are lexical signals, not removal verdicts. Trace each candidate to live roots and audit whether every reference contributes required behavior.")


def run() -> int:
    args = parse_args()
    if args.max_reference_examples < 0:
        print("[ERROR] --max-reference-examples must be zero or greater", file=sys.stderr)
        return 2

    try:
        root, scan_roots = validate_roots(args.root, args.focus)
    except ValueError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    all_paths = list(iter_files(scan_roots))
    source_paths = [
        path
        for path in all_paths
        if path.suffix.lower() in SOURCE_LANGUAGES and path.name not in SOURCE_EXCLUDED_FILENAMES
    ]
    if not source_paths:
        print(f"[ERROR] No supported source files found under: {', '.join(str(path) for path in scan_roots)}", file=sys.stderr)
        return 3

    text_paths = [
        path
        for path in all_paths
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in TEXT_FILENAMES
    ]
    text_by_path = {path: content for path in text_paths if (content := read_text(path)) is not None}
    source_text = {path: text_by_path[path] for path in source_paths if path in text_by_path}
    declarations = [
        declaration
        for path, text in source_text.items()
        for declaration in declarations_for(path, text)
    ]
    locations = reference_index(source_text, declarations)
    languages = Counter(SOURCE_LANGUAGES[path.suffix.lower()] for path in source_paths)
    all_text_blob = "\n".join(text_by_path.values())
    source_blob = "\n".join(source_text.values())

    result: dict[str, object] = {
        "root": str(root),
        "scan_roots": [relative(path, root) or "." for path in scan_roots],
        "source_files_scanned": len(source_paths),
        "text_files_scanned": len(text_by_path),
        "languages": dict(sorted(languages.items())),
        "entry_point_hints": entry_point_hints(text_by_path, root),
        "symbol_candidates": symbol_candidates(
            declarations,
            locations,
            source_text,
            root,
            args.max_reference_examples,
        ),
    }
    if args.include_assets:
        result["asset_candidates"] = asset_candidates(all_paths, all_text_blob, root)
    if args.include_dependencies:
        dependencies = dependency_declarations(text_by_path, root)
        result["dependency_candidates"] = dependency_candidates(dependencies, source_blob)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        emit_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
