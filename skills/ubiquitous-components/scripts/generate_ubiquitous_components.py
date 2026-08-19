#!/usr/bin/env python3
"""Generate a categorized API catalog for Rune + app UI building blocks."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

CATEGORY_ORDER: List[Tuple[str, str]] = [
    ("components", "Components"),
    ("view_modifiers", "ViewModifiers"),
    ("services", "Services"),
    ("views", "Views"),
    ("extensions", "Extensions"),
]

APP_CATEGORY_DIRS: Dict[str, Sequence[str]] = {
    "components": ("Components",),
    "view_modifiers": ("ViewModifiers",),
    "services": ("Services",),
    "views": ("Views", "Screens"),
    "extensions": ("Extensions",),
}

RUNE_CATEGORY_DIRS: Dict[str, Sequence[str]] = {
    "components": ("Components",),
    "view_modifiers": ("ViewModifiers",),
    "services": ("Services",),
    "views": ("Views",),
    "extensions": ("Extensions",),
}

TOP_LEVEL_DECL_RE = re.compile(
    r"^\s*(?:(?:public|internal|private|fileprivate|open)\s+)?"
    r"(?:(?:final|indirect|nonisolated|@MainActor|@preconcurrency|convenience|required|override|mutating|dynamic|lazy|static|class|actor)\s+)*"
    r"(?P<kind>class|struct|enum|actor|protocol|extension)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_\.]*)"
)

MEMBER_START_RE = re.compile(
    r"^(?:(?:@\w+(?:\([^)]*\))?\s+)*)"
    r"(?:(?:public|internal|private|fileprivate|open)\s+)?"
    r"(?:(?:nonisolated|override|mutating|static|class|final|convenience|required|async|reasync|prefix|postfix|infix)\s+)*"
    r"(?:init[?!]?\s*\(|func\s+[A-Za-z_`][A-Za-z0-9_`]*\s*(?:<[^>{}]*>)?\s*\()"
)

FUNC_NAME_RE = re.compile(r"\bfunc\s+([A-Za-z_`][A-Za-z0-9_`]*)")
ACCESS_RE = re.compile(r"\b(public|open|internal|fileprivate|private)\b")
OFFERED_ACCESS = {"public", "open", "internal"}


@dataclasses.dataclass
class SourceRoot:
    source_name: str
    source_kind: str  # rune | app
    root: Path
    category_dirs: Dict[str, List[Path]]


@dataclasses.dataclass
class Parameter:
    external_label: str
    internal_name: str
    type_name: str
    default_value: str


@dataclasses.dataclass
class ApiSignature:
    kind: str
    name: str
    access: str
    signature: str
    params: List[Parameter]
    return_type: str
    line: int

    @property
    def display_name(self) -> str:
        base = "init" if self.kind == "init" else self.name
        if not self.params:
            return f"{base}()"

        labels: List[str] = []
        for param in self.params:
            label = param.external_label or param.internal_name or "_"
            labels.append(label)
        return f"{base}({''.join(f'{label}:' for label in labels)})"


@dataclasses.dataclass
class Declaration:
    name: str
    kind: str
    access: str
    declaration_line: str
    summary: str
    how_it_works: str
    source_name: str
    source_kind: str
    category: str
    file_path: Path
    file_display: str
    line: int
    apis: List[ApiSignature]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate docs/UBIQUITOUS_COMPONENTS.md from Rune + app source."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root to scan (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/UBIQUITOUS_COMPONENTS.md"),
        help="Output markdown path (relative paths are resolved from --workspace).",
    )
    parser.add_argument(
        "--rune-root",
        action="append",
        default=[],
        help="Optional path to Rune root or Sources/Rune (repeatable).",
    )
    parser.add_argument(
        "--app-root",
        action="append",
        default=[],
        help="Optional app root containing Components/Services/ViewModifiers (repeatable).",
    )
    parser.add_argument(
        "--allow-missing-rune",
        action="store_true",
        help="Allow generation when Rune source cannot be discovered.",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private/fileprivate declarations and APIs (off by default).",
    )
    parser.add_argument(
        "--no-global-sync",
        action="store_true",
        help="Disable writing Rune catalog to global shared storage.",
    )
    parser.add_argument(
        "--global-rune-output",
        type=Path,
        default=None,
        help=(
            "Optional override path for globally shared Rune catalog "
            "(default: <shared-home>/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md, "
            "where <shared-home> is $SKILLET_SHARED_HOME, else $CODEX_HOME, else ~/.codex)."
        ),
    )
    return parser.parse_args()


def to_absolute(path: Path, workspace: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (workspace / path).resolve()


def shared_home() -> Path:
    for env_var in ("SKILLET_SHARED_HOME", "CODEX_HOME"):
        raw = os.environ.get(env_var, "").strip()
        if raw:
            return Path(raw).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def default_global_rune_output() -> Path:
    return shared_home() / "shared" / "ubiquitous-components" / "rune" / "UBIQUITOUS_COMPONENTS.md"


def dedupe_paths(paths: Iterable[Path]) -> List[Path]:
    seen: set[str] = set()
    ordered: List[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path.resolve())
    return ordered


def discover_rune_from_package_resolved(workspace: Path) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    resolved_files = workspace.glob("**/Package.resolved")

    for resolved_file in resolved_files:
        if "node_modules" in resolved_file.parts:
            continue

        try:
            payload = json.loads(resolved_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        pins: List[dict] = []
        if isinstance(payload, dict):
            if isinstance(payload.get("pins"), list):
                pins = payload["pins"]
            elif isinstance(payload.get("object"), dict) and isinstance(payload["object"].get("pins"), list):
                pins = payload["object"]["pins"]

        for pin in pins:
            if not isinstance(pin, dict):
                continue
            identity = str(pin.get("identity", "")).lower()
            location = str(pin.get("location", ""))
            if identity != "rune" and "rune" not in location.lower():
                continue
            state = pin.get("state", {}) if isinstance(pin.get("state"), dict) else {}
            results.append(
                {
                    "package_resolved": str(resolved_file),
                    "location": location,
                    "revision": str(state.get("revision", "")),
                    "branch": str(state.get("branch", "")),
                    "version": str(state.get("version", "")),
                }
            )

    return results


def normalize_rune_input(path: Path) -> Optional[Path]:
    resolved = path.resolve()
    if not resolved.exists():
        return None

    if resolved.name == "Rune" and resolved.parent.name == "Sources":
        return resolved

    candidate = resolved / "Sources" / "Rune"
    if candidate.exists():
        return candidate.resolve()

    return None


def discover_rune_roots(workspace: Path, explicit_rune_roots: Sequence[str]) -> List[Path]:
    roots: List[Path] = []

    for raw_path in explicit_rune_roots:
        normalized = normalize_rune_input(to_absolute(Path(raw_path), workspace))
        if normalized is not None:
            roots.append(normalized)

    # Explicit roots should fully control scan scope.
    if roots:
        return dedupe_paths(roots)

    candidates = [
        workspace / "Rune" / "Sources" / "Rune",
        workspace / ".build" / "checkouts" / "Rune" / "Sources" / "Rune",
        workspace / "SourcePackages" / "checkouts" / "Rune" / "Sources" / "Rune",
    ]

    for candidate in candidates:
        if candidate.exists():
            roots.append(candidate.resolve())

    derived_data_glob = os.path.expanduser(
        "~/Library/Developer/Xcode/DerivedData/*/SourcePackages/checkouts/Rune/Sources/Rune"
    )
    for match in glob.glob(derived_data_glob):
        path = Path(match)
        if path.exists():
            roots.append(path.resolve())

    return dedupe_paths(roots)


def rune_repo_root(source_root: Path) -> Path:
    # .../Rune/Sources/Rune -> .../Rune
    return source_root.parent.parent


def read_git_revision(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return ""
    return result.stdout.strip()


def select_preferred_rune_roots(
    rune_roots: Sequence[Path],
    workspace: Path,
    rune_pins: Sequence[Dict[str, str]],
) -> List[Path]:
    roots = dedupe_paths(rune_roots)
    if len(roots) <= 1:
        return roots

    workspace_token = workspace.name.lower()
    workspace_matches = [root for root in roots if workspace_token in str(root).lower()]
    candidate_roots = workspace_matches or roots

    pin_revisions = {pin.get("revision", "").strip() for pin in rune_pins if pin.get("revision")}
    if pin_revisions:
        revision_matches: List[Path] = []
        for root in candidate_roots:
            revision = read_git_revision(rune_repo_root(root))
            if revision in pin_revisions:
                revision_matches.append(root)
        if revision_matches:
            candidate_roots = revision_matches

    # Keep deterministic order and avoid duplicate checkouts at the same revision.
    by_revision: Dict[str, Path] = {}
    ordered: List[Path] = []
    for root in candidate_roots:
        revision = read_git_revision(rune_repo_root(root)) or f"path:{root}"
        if revision in by_revision:
            continue
        by_revision[revision] = root
        ordered.append(root)

    return ordered


def has_app_shape(path: Path) -> bool:
    checks = [
        path / "Components",
        path / "Services",
        path / "ViewModifiers",
        path / "Views",
        path / "Screens",
    ]
    score = sum(1 for check in checks if check.exists() and check.is_dir())
    return score >= 2


def discover_app_roots(workspace: Path, explicit_app_roots: Sequence[str]) -> List[Path]:
    roots: List[Path] = []

    for raw_path in explicit_app_roots:
        path = to_absolute(Path(raw_path), workspace)
        if path.exists() and path.is_dir() and has_app_shape(path):
            roots.append(path)

    candidates = [workspace]
    for child in workspace.iterdir():
        if child.is_dir() and child.name not in {".git", "node_modules", ".build"}:
            candidates.append(child)

    for candidate in candidates:
        if has_app_shape(candidate):
            roots.append(candidate.resolve())

    return dedupe_paths(roots)


def build_source_roots(workspace: Path, rune_roots: Sequence[Path], app_roots: Sequence[Path]) -> List[SourceRoot]:
    sources: List[SourceRoot] = []

    for rune_root in rune_roots:
        category_dirs: Dict[str, List[Path]] = {}
        for category, dirs in RUNE_CATEGORY_DIRS.items():
            category_dirs[category] = [directory for directory in (rune_root / d for d in dirs) if directory.exists()]

        derived_data_hint = ""
        if "DerivedData" in rune_root.parts:
            idx = rune_root.parts.index("DerivedData")
            if idx + 1 < len(rune_root.parts):
                derived_data_hint = rune_root.parts[idx + 1]

        name = "Rune"
        if derived_data_hint:
            name = f"Rune ({derived_data_hint})"

        sources.append(
            SourceRoot(
                source_name=name,
                source_kind="rune",
                root=rune_root,
                category_dirs=category_dirs,
            )
        )

    for app_root in app_roots:
        category_dirs = {}
        for category, dirs in APP_CATEGORY_DIRS.items():
            category_dirs[category] = [directory for directory in (app_root / d for d in dirs) if directory.exists()]

        sources.append(
            SourceRoot(
                source_name=app_root.name,
                source_kind="app",
                root=app_root,
                category_dirs=category_dirs,
            )
        )

    deduped: List[SourceRoot] = []
    seen: set[Tuple[str, str]] = set()
    for source in sources:
        key = (source.source_kind, str(source.root))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(source)

    deduped.sort(key=lambda source: (0 if source.source_kind == "rune" else 1, source.source_name.lower(), str(source.root)))
    return deduped


def iter_swift_files(directory: Path) -> Iterable[Path]:
    for path in sorted(directory.rglob("*.swift")):
        if any(part in {".git", "node_modules", "Tests"} for part in path.parts):
            continue
        yield path


def clean_decl_line(line: str) -> str:
    normalized = re.sub(r"^\s*(?:@\w+(?:\([^)]*\))?\s+)+", "", line)
    return normalized


def strip_inline_comment(line: str) -> str:
    if "//" not in line:
        return line
    return line.split("//", 1)[0]


def leading_spaces(line: str) -> int:
    count = 0
    for char in line:
        if char == " ":
            count += 1
        elif char == "\t":
            count += 4
        else:
            break
    return count


def find_block_end(lines: Sequence[str], start_idx: int) -> Optional[int]:
    brace_depth = 0
    opened = False

    for index in range(start_idx, len(lines)):
        raw = strip_inline_comment(lines[index])
        for char in raw:
            if char == "{":
                brace_depth += 1
                opened = True
            elif char == "}" and opened:
                brace_depth -= 1
                if brace_depth == 0:
                    return index

    return None


def collect_doc_comment(lines: Sequence[str], start_idx: int) -> str:
    comments: List[str] = []
    index = start_idx - 1

    while index >= 0:
        stripped = lines[index].strip()
        if stripped.startswith("///"):
            comments.append(stripped[3:].strip())
            index -= 1
            continue
        if not stripped and not comments:
            index -= 1
            continue
        break

    comments.reverse()
    return " ".join(comment for comment in comments if comment).strip()


def split_top_level(text: str, delimiter: str) -> List[str]:
    chunks: List[str] = []
    current: List[str] = []

    paren = 0
    bracket = 0
    brace = 0
    angle = 0

    for char in text:
        if char == "(":
            paren += 1
        elif char == ")":
            paren = max(0, paren - 1)
        elif char == "[":
            bracket += 1
        elif char == "]":
            bracket = max(0, bracket - 1)
        elif char == "{":
            brace += 1
        elif char == "}":
            brace = max(0, brace - 1)
        elif char == "<":
            angle += 1
        elif char == ">":
            angle = max(0, angle - 1)

        if char == delimiter and paren == 0 and bracket == 0 and brace == 0 and angle == 0:
            chunks.append("".join(current))
            current = []
            continue

        current.append(char)

    if current:
        chunks.append("".join(current))

    return chunks


def find_top_level_char(text: str, target: str) -> int:
    paren = 0
    bracket = 0
    brace = 0
    angle = 0

    for idx, char in enumerate(text):
        if char == "(":
            paren += 1
        elif char == ")":
            paren = max(0, paren - 1)
        elif char == "[":
            bracket += 1
        elif char == "]":
            bracket = max(0, bracket - 1)
        elif char == "{":
            brace += 1
        elif char == "}":
            brace = max(0, brace - 1)
        elif char == "<":
            angle += 1
        elif char == ">":
            angle = max(0, angle - 1)

        if char == target and paren == 0 and bracket == 0 and brace == 0 and angle == 0:
            return idx

    return -1


def extract_first_parenthesized(signature: str) -> Tuple[str, int]:
    start = signature.find("(")
    if start < 0:
        return "", -1

    depth = 0
    for index in range(start, len(signature)):
        char = signature[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return signature[start + 1 : index], index

    return "", -1


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_parameter(raw: str) -> Optional[Parameter]:
    token = raw.strip()
    if not token:
        return None

    colon_index = find_top_level_char(token, ":")
    if colon_index < 0:
        return None

    name_part = token[:colon_index].strip()
    type_part = token[colon_index + 1 :].strip()

    eq_index = find_top_level_char(type_part, "=")
    default_value = ""
    if eq_index >= 0:
        default_value = type_part[eq_index + 1 :].strip()
        type_part = type_part[:eq_index].strip()

    name_tokens = [piece for piece in re.split(r"\s+", name_part) if piece and not piece.startswith("@")]
    if not name_tokens:
        external = "-"
        internal = "-"
    elif len(name_tokens) == 1:
        external = name_tokens[0]
        internal = name_tokens[0]
    else:
        external = name_tokens[-2]
        internal = name_tokens[-1]

    return Parameter(
        external_label=external,
        internal_name=internal,
        type_name=type_part or "-",
        default_value=default_value,
    )


def parse_parameters(parameter_list: str) -> List[Parameter]:
    if not parameter_list.strip():
        return []

    parts = split_top_level(parameter_list, ",")
    parsed: List[Parameter] = []
    for part in parts:
        parameter = parse_parameter(part)
        if parameter is not None:
            parsed.append(parameter)

    return parsed


def parse_access(line: str) -> str:
    match = ACCESS_RE.search(line)
    if match:
        return match.group(1)
    return "internal"


def parse_signature(lines: Sequence[str], start_idx: int, end_idx: int) -> Tuple[str, int]:
    signature_lines: List[str] = []
    paren_depth = 0
    opened = False
    last_idx = start_idx

    for index in range(start_idx, end_idx + 1):
        raw = strip_inline_comment(lines[index]).strip()
        if not raw and not signature_lines:
            continue

        signature_lines.append(raw)

        for char in raw:
            if char == "(":
                paren_depth += 1
                opened = True
            elif char == ")" and opened:
                paren_depth -= 1

        if opened and paren_depth == 0:
            last_idx = index
            break

    signature = normalize_whitespace(" ".join(piece for piece in signature_lines if piece))
    if "{" in signature:
        signature = signature.split("{", 1)[0].strip()

    return signature, last_idx


def parse_api_signature(lines: Sequence[str], start_idx: int, end_idx: int) -> Optional[Tuple[ApiSignature, int]]:
    first_line = lines[start_idx].strip()
    signature, consumed_idx = parse_signature(lines, start_idx, end_idx)
    if not signature:
        return None

    params_raw, closing_idx = extract_first_parenthesized(signature)
    params = parse_parameters(params_raw)

    access = parse_access(first_line)
    is_init = bool(re.search(r"\binit[?!]?\s*\(", signature))

    if is_init:
        api_name = "init"
        api_kind = "init"
        return_type = "-"
    else:
        func_match = FUNC_NAME_RE.search(signature)
        if not func_match:
            return None
        api_name = func_match.group(1).strip("`")
        api_kind = "func"

        return_type = "-"
        if closing_idx >= 0:
            after = signature[closing_idx + 1 :].strip()
            arrow_index = after.find("->")
            if arrow_index >= 0:
                return_type = after[arrow_index + 2 :].strip()
                return_type = return_type.split(" where ", 1)[0].strip()
                if not return_type:
                    return_type = "-"

    api = ApiSignature(
        kind=api_kind,
        name=api_name,
        access=access,
        signature=signature,
        params=params,
        return_type=return_type,
        line=start_idx + 1,
    )
    return api, consumed_idx


def words_from_identifier(identifier: str) -> str:
    split = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", identifier)
    split = split.replace("_", " ").strip()
    return split.lower() if split else identifier.lower()


def fallback_summary(category: str, name: str, kind: str) -> str:
    subject = words_from_identifier(name)
    if category == "components":
        return f"Reusable UI component for {subject}."
    if category == "view_modifiers":
        return f"View-modifier API related to {subject}."
    if category == "services":
        return f"Service-layer API handling {subject}."
    if category == "views":
        return f"Standalone view for {subject}."
    if category == "extensions":
        return f"Extension API for {subject}."
    return f"{kind.capitalize()} for {subject}."


def derive_how_it_works(declaration_line: str, apis: Sequence[ApiSignature], category: str) -> str:
    parts: List[str] = []

    if ":" in declaration_line:
        conformances = declaration_line.split(":", 1)[1].split("{", 1)[0].strip()
        if conformances:
            parts.append(f"Conforms to `{conformances}`")

    if apis:
        sample = ", ".join(f"`{api.display_name}`" for api in apis[:3])
        if len(apis) > 3:
            sample += f" (+{len(apis) - 3} more)"
        parts.append(f"Primary entry points: {sample}")
    else:
        if category == "views":
            parts.append("No explicit init/func signature extracted at top-level member depth")
        else:
            parts.append("No top-level init/func signature extracted")

    return ". ".join(parts).strip() + "."


def category_title(category: str) -> str:
    for key, value in CATEGORY_ORDER:
        if key == category:
            return value
    return category


def relative_file_display(path: Path, source_root: SourceRoot) -> str:
    try:
        relative = path.relative_to(source_root.root)
        return str(relative)
    except ValueError:
        return str(path)


def parse_declarations(
    file_path: Path,
    source_root: SourceRoot,
    category: str,
) -> List[Declaration]:
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file_path.read_text(encoding="utf-8", errors="ignore")

    lines = content.splitlines()
    declarations: List[Declaration] = []

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if not stripped or stripped.startswith("//"):
            idx += 1
            continue

        match = TOP_LEVEL_DECL_RE.match(clean_decl_line(line))
        if not match:
            idx += 1
            continue

        kind = match.group("kind")
        name = match.group("name").split(".")[0]
        block_end = find_block_end(lines, idx)
        if block_end is None:
            idx += 1
            continue

        declaration_line = normalize_whitespace(stripped)
        access = parse_access(declaration_line)
        member_indent = leading_spaces(line) + 4

        apis: List[ApiSignature] = []
        cursor = idx + 1
        while cursor <= block_end:
            candidate = lines[cursor]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                cursor += 1
                continue

            if leading_spaces(candidate) != member_indent:
                cursor += 1
                continue

            if not MEMBER_START_RE.match(candidate_stripped):
                cursor += 1
                continue

            parsed = parse_api_signature(lines, cursor, block_end)
            if parsed is None:
                cursor += 1
                continue

            api, consumed = parsed
            apis.append(api)
            cursor = consumed + 1

        doc_summary = collect_doc_comment(lines, idx)
        summary = doc_summary if doc_summary else fallback_summary(category, name, kind)
        how = derive_how_it_works(declaration_line, apis, category)

        declarations.append(
            Declaration(
                name=name,
                kind=kind,
                access=access,
                declaration_line=declaration_line,
                summary=summary,
                how_it_works=how,
                source_name=source_root.source_name,
                source_kind=source_root.source_kind,
                category=category,
                file_path=file_path,
                file_display=relative_file_display(file_path, source_root),
                line=idx + 1,
                apis=apis,
            )
        )

        idx = block_end + 1

    return declarations


def markdown_escape(text: str, max_len: int = 220) -> str:
    normalized = text.replace("\n", " ").strip()
    normalized = re.sub(r"\s+", " ", normalized)
    if len(normalized) > max_len:
        normalized = normalized[: max_len - 3].rstrip() + "..."
    normalized = normalized.replace("|", "\\|")
    return normalized or "-"


def summarize_entry_points(apis: Sequence[ApiSignature], limit: int = 3) -> str:
    if not apis:
        return "-"
    samples = [f"`{api.display_name}`" for api in apis[:limit]]
    if len(apis) > limit:
        samples.append(f"(+{len(apis) - limit} more)")
    return ", ".join(samples)


def offered_apis(apis: Sequence[ApiSignature], include_private: bool) -> List[ApiSignature]:
    if include_private:
        return list(apis)
    return [api for api in apis if api.access in OFFERED_ACCESS]


def generate_markdown(
    workspace: Path,
    output_path: Path,
    sources: Sequence[SourceRoot],
    declarations: Sequence[Declaration],
    rune_pins: Sequence[Dict[str, str]],
    include_private: bool,
    global_rune_output: Optional[Path] = None,
) -> str:
    by_category_source: Dict[Tuple[str, str], List[Declaration]] = {}
    for declaration in declarations:
        key = (declaration.category, declaration.source_name)
        by_category_source.setdefault(key, []).append(declaration)

    for records in by_category_source.values():
        records.sort(key=lambda record: (record.name.lower(), str(record.file_path), record.line))

    generated_at = dt.datetime.now().astimezone().isoformat(timespec="seconds")

    lines: List[str] = []
    lines.append("# Ubiquitous Components")
    lines.append("")
    lines.append(f"_Generated: {generated_at}_")
    lines.append("")

    lines.append("## Scope")
    lines.append("")
    lines.append("- **Workspace:** `{}`".format(workspace))
    lines.append("- **Output:** `{}`".format(output_path))
    if global_rune_output is not None:
        lines.append("- **Global Rune Output:** `{}`".format(global_rune_output))
    lines.append("")

    lines.append("### Source Roots")
    lines.append("")
    lines.append("| Source | Kind | Root |")
    lines.append("| --- | --- | --- |")
    for source in sources:
        lines.append(
            f"| {markdown_escape(source.source_name)} | {source.source_kind} | `{markdown_escape(str(source.root), max_len=512)}` |"
        )
    lines.append("")

    lines.append("### Coverage Summary")
    lines.append("")
    lines.append("| Source | Category | Declarations | APIs | Parameters |")
    lines.append("| --- | --- | --- | --- | --- |")

    for source in sources:
        for category, category_display in CATEGORY_ORDER:
            records = by_category_source.get((category, source.source_name), [])
            api_count = sum(len(offered_apis(record.apis, include_private)) for record in records)
            parameter_count = sum(
                len(api.params)
                for record in records
                for api in offered_apis(record.apis, include_private)
            )
            lines.append(
                f"| {markdown_escape(source.source_name)} | {category_display} | {len(records)} | {api_count} | {parameter_count} |"
            )
    lines.append("")

    lines.append("### Context Strategy")
    lines.append("")
    lines.append("- This file is intentionally compact: one row per declaration with summarized entry points.")
    if include_private:
        lines.append("- Private/fileprivate declarations are included for deep implementation audits.")
    else:
        lines.append("- Private/fileprivate declarations are excluded to focus on offered surface area.")
    lines.append("- Use source file links (`File`) to inspect implementation details only where needed.")
    lines.append("- For deep audits, regenerate with a custom script variant that emits full per-API parameter tables.")
    lines.append("")

    if rune_pins:
        lines.append("### Rune Package Pins")
        lines.append("")
        lines.append("| Package.resolved | Location | Revision | Branch | Version |")
        lines.append("| --- | --- | --- | --- | --- |")
        for pin in rune_pins:
            lines.append(
                "| `{}` | `{}` | `{}` | `{}` | `{}` |".format(
                    markdown_escape(pin.get("package_resolved", ""), max_len=256),
                    markdown_escape(pin.get("location", ""), max_len=256),
                    markdown_escape(pin.get("revision", ""), max_len=80),
                    markdown_escape(pin.get("branch", ""), max_len=80),
                    markdown_escape(pin.get("version", ""), max_len=80),
                )
            )
        lines.append("")

    for category, category_display in CATEGORY_ORDER:
        lines.append(f"## Category: {category_display}")
        lines.append("")

        for source in sources:
            records = by_category_source.get((category, source.source_name), [])
            if not records:
                continue

            lines.append(f"### Source: {source.source_name}")
            lines.append("")
            lines.append("| Symbol | Kind | Access | File | APIs | Params | Entry Points | What |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
            for record in records:
                visible_apis = offered_apis(record.apis, include_private)
                api_count = len(visible_apis)
                parameter_count = sum(len(api.params) for api in visible_apis)
                file_ref = f"`{markdown_escape(record.file_display, max_len=512)}`:{record.line}"
                lines.append(
                    "| `{}` | `{}` | `{}` | {} | {} | {} | {} | {} |".format(
                        markdown_escape(record.name, max_len=120),
                        markdown_escape(record.kind, max_len=40),
                        markdown_escape(record.access, max_len=40),
                        file_ref,
                        api_count,
                        parameter_count,
                        markdown_escape(summarize_entry_points(visible_apis), max_len=360),
                        markdown_escape(record.summary, max_len=220),
                    )
                )
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append("- Confirmed all discovered `Components`, `ViewModifiers`, `Services`, `Views`/`Screens`, and `Extensions` folders were scanned.")
    lines.append("- Confirmed each declaration row includes access, file+line, API counts, parameter counts, and summarized entry points.")
    if include_private:
        lines.append("- Output includes private/fileprivate declarations for implementation-level inventory coverage.")
    else:
        lines.append("- Output excludes private/fileprivate declarations to keep focus on offered APIs.")
    lines.append("- Review rows with `0` APIs to decide whether additional hand-written notes are needed.")

    return "\n".join(lines).rstrip() + "\n"


def run() -> int:
    args = parse_args()

    workspace = args.workspace.resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"[ERROR] Workspace not found: {workspace}", file=sys.stderr)
        return 1

    output_path = args.output
    if not output_path.is_absolute():
        output_path = (workspace / output_path).resolve()

    global_rune_output: Optional[Path]
    if args.global_rune_output is None:
        global_rune_output = default_global_rune_output()
    else:
        global_rune_output = args.global_rune_output.expanduser()
        if not global_rune_output.is_absolute():
            global_rune_output = (workspace / global_rune_output).resolve()

    rune_pins = discover_rune_from_package_resolved(workspace)
    rune_roots = discover_rune_roots(workspace, args.rune_root)
    rune_roots = select_preferred_rune_roots(rune_roots, workspace, rune_pins)
    app_roots = discover_app_roots(workspace, args.app_root)

    if not rune_roots and not args.allow_missing_rune:
        print("[ERROR] Rune source was not discovered.", file=sys.stderr)
        print("        Provide --rune-root or ensure DerivedData has SourcePackages/checkouts/Rune.", file=sys.stderr)
        if rune_pins:
            print("        Rune pin(s) found in Package.resolved:", file=sys.stderr)
            for pin in rune_pins:
                location = pin.get("location", "")
                revision = pin.get("revision", "")
                print(f"        - {location} @ {revision}", file=sys.stderr)
        return 2

    if not app_roots and not rune_roots:
        print("[ERROR] No source roots discovered for scanning.", file=sys.stderr)
        return 3

    sources = build_source_roots(workspace, rune_roots, app_roots)

    all_declarations: List[Declaration] = []
    for source in sources:
        for category, _display in CATEGORY_ORDER:
            for category_dir in source.category_dirs.get(category, []):
                for swift_file in iter_swift_files(category_dir):
                    parsed = parse_declarations(
                        file_path=swift_file,
                        source_root=source,
                        category=category,
                    )
                    if args.include_private:
                        all_declarations.extend(parsed)
                    else:
                        all_declarations.extend(
                            declaration for declaration in parsed if declaration.access in OFFERED_ACCESS
                        )

    markdown = generate_markdown(
        workspace=workspace,
        output_path=output_path,
        sources=sources,
        declarations=all_declarations,
        rune_pins=rune_pins,
        include_private=args.include_private,
        global_rune_output=global_rune_output,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    if not args.no_global_sync and global_rune_output is not None:
        rune_sources = [source for source in sources if source.source_kind == "rune"]
        if rune_sources:
            rune_declarations = [declaration for declaration in all_declarations if declaration.source_kind == "rune"]
            global_markdown = generate_markdown(
                workspace=workspace,
                output_path=global_rune_output,
                sources=rune_sources,
                declarations=rune_declarations,
                rune_pins=rune_pins,
                include_private=args.include_private,
                global_rune_output=global_rune_output,
            )
            global_rune_output.parent.mkdir(parents=True, exist_ok=True)
            global_rune_output.write_text(global_markdown, encoding="utf-8")
            metadata_path = global_rune_output.with_name("UBIQUITOUS_COMPONENTS.metadata.json")
            metadata_payload = {
                "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "workspace": str(workspace),
                "global_output": str(global_rune_output),
                "source_roots": [str(source.root) for source in rune_sources],
                "declarations": len(rune_declarations),
                "include_private": bool(args.include_private),
                "rune_package_pins": list(rune_pins),
            }
            metadata_path.write_text(
                json.dumps(metadata_payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            print(f"[OK] Global Rune catalog: {global_rune_output}")
            print(f"[OK] Global Rune metadata: {metadata_path}")
        else:
            print("[WARN] Global sync skipped: no Rune sources discovered.")

    print(f"[OK] Wrote {output_path}")
    print(f"[OK] Sources: {len(sources)} | Declarations: {len(all_declarations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
