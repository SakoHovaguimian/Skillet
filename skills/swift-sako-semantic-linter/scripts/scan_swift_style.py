#!/usr/bin/env python3
"""Fast heuristic checks for focused Swift Sako semantic-lint passes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    identifier: str
    severity: str
    message: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    column: int
    rule: str
    severity: str
    message: str
    source: str


RULES = (
    Rule(
        identifier="body-colon-spacing",
        severity="error",
        message="Use `var body: some View` without a space before the colon.",
        pattern=re.compile(r"\bvar\s+body\s+:\s*some\s+View\b"),
    ),
    Rule(
        identifier="void-tuple-return",
        severity="error",
        message="Use `() -> Void` instead of `() -> ()`.",
        pattern=re.compile(r"\(\)\s*->\s*\(\)"),
    ),
    Rule(
        identifier="spaced-member-token",
        severity="error",
        message="Remove whitespace between `.` and the member name.",
        pattern=re.compile(r"\.\s+[A-Za-z_]\w*"),
    ),
    Rule(
        identifier="explicit-self-method-call",
        severity="review",
        message="Omit `self.` for method calls unless capture or disambiguation requires it; confirm this is not a callable property.",
        pattern=re.compile(r"\bself\.[A-Za-z_]\w*\s*\("),
    ),
    Rule(
        identifier="bare-multiline-initializer",
        severity="error",
        message="Keep the first initializer parameter on the `init` line and align subsequent parameters beneath it.",
        pattern=re.compile(
            r"^\s*(?:(?:public|internal|private|fileprivate|package|required|convenience|override|nonisolated)\s+)*init\s*\(\s*$"
        ),
    ),
    Rule(
        identifier="unscoped-animation",
        severity="review",
        message="Prefer value-scoped `.animation(_:value:)` when this is SwiftUI animation state.",
        pattern=re.compile(r"\.animation\([^\n,()]+\)"),
    ),
    Rule(
        identifier="raw-system-image",
        severity="review",
        message="Prefer ImageSource or the established project image wrapper; keep raw Image only for a documented interop exception.",
        pattern=re.compile(r"\bImage\s*\(\s*systemName\s*:"),
    ),
    Rule(
        identifier="raw-async-image",
        severity="review",
        message="Prefer the established remote-image wrapper instead of AsyncImage or custom remote loading.",
        pattern=re.compile(r"\bAsyncImage\s*\("),
    ),
)

EXCLUDED_PARTS = {".build", "DerivedData", ".git", "Pods", "Carthage"}


def swift_files(paths: list[str]) -> list[Path]:
    files: set[Path] = set()

    for raw_path in paths:
        path = Path(raw_path).expanduser()

        if path.is_file() and path.suffix == ".swift":
            files.add(path.resolve())
        elif path.is_dir():
            for candidate in path.rglob("*.swift"):
                if not EXCLUDED_PARTS.intersection(candidate.parts):
                    files.add(candidate.resolve())

    return sorted(files)


def changed_lines(path: Path, base: str) -> set[int] | None:
    root_result = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=False,
        text=True,
    )

    if root_result.returncode != 0:
        return None

    root = Path(root_result.stdout.strip())
    relative_path = path.relative_to(root)
    tracked_result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", str(relative_path)],
        capture_output=True,
        check=False,
        text=True,
    )

    if tracked_result.returncode != 0:
        return None

    diff_result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "diff",
            "--unified=0",
            "--no-ext-diff",
            base,
            "--",
            str(relative_path),
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    if diff_result.returncode != 0:
        return None

    lines: set[int] = set()
    hunk_pattern = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

    for source in diff_result.stdout.splitlines():
        match = hunk_pattern.match(source)

        if not match:
            continue

        start = int(match.group(1))
        count = int(match.group(2) or "1")
        lines.update(range(start, start + count))

    return lines


def mask_non_code(lines: list[str]) -> list[str]:
    """Mask comments and string literals while preserving line/column positions."""

    masked: list[str] = []
    block_depth = 0
    in_multiline_string = False

    for source in lines:
        result = list(source)
        index = 0

        while index < len(source):
            if in_multiline_string:
                end = source.find('"""', index)

                if end == -1:
                    for position in range(index, len(source)):
                        result[position] = " "
                    index = len(source)
                    continue

                for position in range(index, end + 3):
                    result[position] = " "
                in_multiline_string = False
                index = end + 3
                continue

            if block_depth:
                if source.startswith("/*", index):
                    result[index:index + 2] = [" ", " "]
                    block_depth += 1
                    index += 2
                elif source.startswith("*/", index):
                    result[index:index + 2] = [" ", " "]
                    block_depth -= 1
                    index += 2
                else:
                    result[index] = " "
                    index += 1
                continue

            if source.startswith("//", index):
                for position in range(index, len(source)):
                    result[position] = " "
                break

            if source.startswith("/*", index):
                result[index:index + 2] = [" ", " "]
                block_depth = 1
                index += 2
                continue

            if source.startswith('"""', index):
                result[index:index + 3] = [" ", " ", " "]
                in_multiline_string = True
                index += 3
                continue

            if source[index] == '"':
                result[index] = " "
                index += 1

                while index < len(source):
                    result[index] = " "

                    if source[index] == "\\":
                        index += 1
                        if index < len(source):
                            result[index] = " "
                    elif source[index] == '"':
                        index += 1
                        break

                    index += 1

                continue

            index += 1

        masked.append("".join(result))

    return masked


def line_for_pattern(lines: list[str], pattern: str, default: int = 1) -> int:
    compiled = re.compile(pattern)

    for line_number, source in enumerate(lines, start=1):
        if compiled.search(source):
            return line_number

    return default


def semantic_finding(
    path: Path,
    lines: list[str],
    line: int,
    rule: str,
    severity: str,
    message: str,
) -> Finding:
    source = lines[line - 1].strip() if lines and line <= len(lines) else ""
    return Finding(
        path=str(path),
        line=line,
        column=1,
        rule=rule,
        severity=severity,
        message=message,
        source=source,
    )


def screen_member_entries(code_lines: list[str]) -> list[tuple[int, int, str]]:
    """Return (line, rank, section) for likely top-level screen members."""

    entries: list[tuple[int, int, str]] = []
    depth = 0
    inside_screen = False
    pending_view_builder = False
    ranks = {
        "@Environment": 1,
        "@Binding": 2,
        "@State": 3,
        "@FocusState": 4,
        "stored properties": 5,
        "computed properties": 6,
        "methods": 7,
        "view logic": 8,
    }

    for index, source in enumerate(code_lines):
        stripped = source.strip()
        line_number = index + 1

        if not inside_screen and re.search(r"\bstruct\s+\w+(?:Screen|Sheet)\b", source):
            inside_screen = True

        if inside_screen and depth == 1:
            section: str | None = None

            if stripped.startswith("@ViewBuilder"):
                pending_view_builder = True
            elif re.match(r"@Environment\b", stripped):
                section = "@Environment"
            elif re.match(r"@Binding\b", stripped):
                section = "@Binding"
            elif re.match(r"@State(?:Object)?\b", stripped):
                section = "@State"
            elif re.match(r"@FocusState\b", stripped):
                section = "@FocusState"
            elif re.match(r"(?:(?:public|internal|private|fileprivate|package)\s+)?init\s*\(", stripped):
                section = "methods"
            elif re.match(r"(?:(?:public|internal|private|fileprivate|package|static|class)\s+)*func\b", stripped):
                signature = " ".join(code_lines[index:min(index + 8, len(code_lines))])
                section = "view logic" if pending_view_builder or re.search(r"->\s*some\s+View\b", signature) else "methods"
                pending_view_builder = False
            elif re.match(r"(?:(?:public|internal|private|fileprivate|package|static|class)\s+)*(?:let|var)\b", stripped):
                if re.search(r"\bvar\s+body\s*:\s*some\s+View\b", stripped) or re.search(
                    r":\s*some\s+View\b", stripped
                ):
                    section = "view logic"
                elif "{" in stripped.split("=", 1)[0]:
                    section = "computed properties"
                else:
                    section = "stored properties"

            if section:
                entries.append((line_number, ranks[section], section))

        depth += source.count("{") - source.count("}")

        if inside_screen and depth <= 0 and entries:
            break

    return entries


def semantic_scan(
    path: Path,
    lines: list[str],
    code_lines: list[str],
    allowed_lines: set[int] | None,
) -> list[Finding]:
    if allowed_lines is not None and not allowed_lines:
        return []

    findings: list[Finding] = []
    code = "\n".join(code_lines)
    is_screen_source = "Screens" in path.parts
    is_view_model = is_screen_source and path.name.endswith("ViewModel.swift")
    is_screen = is_screen_source and path.name.endswith(("Screen.swift", "Sheet.swift"))

    if is_view_model:
        class_match = re.search(r"\b(?:(final)\s+)?class\s+(\w+ViewModel)\b", code)

        if class_match:
            type_name = class_match.group(2)
            class_line = line_for_pattern(code_lines, rf"\bclass\s+{re.escape(type_name)}\b")

            if not class_match.group(1):
                findings.append(semantic_finding(
                    path, lines, class_line, "viewmodel-final-class", "error",
                    "Declare standard screen ViewModels as final classes.",
                ))

            for member in ("loggerName", "loggerEmoji"):
                if not re.search(rf"\b{member}\b", code):
                    findings.append(semantic_finding(
                        path, lines, class_line, "viewmodel-logger-pair", "error",
                        "Include loggerName and loggerEmoji as a complete ViewModel logging contract.",
                    ))
                    break

            for method in ("logInit", "logDeinit"):
                if not re.search(rf"\b{method}\s*\(", code):
                    findings.append(semantic_finding(
                        path, lines, class_line, "viewmodel-log-lifecycle-pair", "error",
                        "Call logInit() and logDeinit() as a complete ViewModel lifecycle pair.",
                    ))
                    break

            track_match = re.search(r"\bfunc\s+track\s*\(\s*\)", code)
            extension_match = re.search(
                rf"\bextension\s+{re.escape(type_name)}\s*\{{[\s\S]*?\bfunc\s+track\s*\(\s*\)",
                code,
            )

            if not track_match:
                findings.append(semantic_finding(
                    path, lines, class_line, "viewmodel-track-extension", "error",
                    "Implement track() for every standard screen ViewModel.",
                ))
            elif not extension_match:
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"\bfunc\s+track\s*\("),
                    "viewmodel-track-extension", "error",
                    "Move track() into the final same-type ViewModel extension.",
                ))

            first_appear = re.search(
                r"\bfunc\s+handleFirstAppear\s*\(\s*\)\s*\{([\s\S]*?)\n\s*\}",
                code,
            )

            if first_appear:
                body = first_appear.group(1)
                track_position = body.find("track(")
                bind_positions = [
                    position
                    for position in (match.start() for match in re.finditer(r"\bbind\w*\s*\(", body))
                ]

                if track_position == -1:
                    findings.append(semantic_finding(
                        path, lines, line_for_pattern(code_lines, r"func\s+handleFirstAppear"),
                        "viewmodel-first-appear-tracks", "error",
                        "Call track() exactly once from handleFirstAppear().",
                    ))
                elif bind_positions and track_position > min(bind_positions):
                    findings.append(semantic_finding(
                        path, lines, line_for_pattern(code_lines, r"func\s+handleFirstAppear"),
                        "viewmodel-first-appear-order", "error",
                        "Call track() before subscriber binding in handleFirstAppear().",
                    ))
            elif track_match:
                findings.append(semantic_finding(
                    path, lines, class_line, "viewmodel-missing-first-appear", "review",
                    "Add handleFirstAppear() or document why this ViewModel uses a special lifecycle.",
                ))

            init_match = re.search(r"\binit\s*\([^)]*\)\s*\{([\s\S]*?)\n\s*\}", code)
            if init_match and re.search(r"\bbind\w*\s*\(", init_match.group(1)):
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"\binit\s*\("),
                    "viewmodel-no-init-binding", "error",
                    "Do not bind screen publishers from init; bind from first appearance.",
                ))

            if re.search(r"\bvar\s+navigationService\s*:\s*NavigationService\??", code) and not re.search(
                r"\bweak\s+var\s+navigationService\b", code
            ):
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"navigationService"),
                    "viewmodel-weak-navigation", "error",
                    "Hold a screen-injected NavigationService weakly.",
                ))

            for setup_match in re.finditer(r"\bfunc\s+setup\s*\(", code):
                prefix = code[max(0, setup_match.start() - 80):setup_match.start()]
                suffix = code[setup_match.start():setup_match.start() + 600]
                signature = suffix.split("{", 1)[0]
                is_route_context_setup = bool(re.search(
                    r"\b(?:\w+ID|token|context|mode|selectedTab|initialRoute)\s*:",
                    signature,
                ))
                if is_route_context_setup and (
                    "@discardableResult" not in prefix
                    or not re.search(r"\)\s*->\s*Self\b", signature)
                ):
                    findings.append(semantic_finding(
                        path, lines, line_for_pattern(code_lines, r"\bfunc\s+setup\s*\("),
                        "viewmodel-setup-returns-self", "review",
                        "Route/context setup should be @discardableResult and return Self; exempt dependency-only setup explicitly.",
                    ))
                    break

            task_names = re.findall(r"\bprivate\s+var\s+(\w+Task)\s*:\s*Task<", code)
            deinit_match = re.search(r"\b(?:isolated\s+)?deinit\s*\{([\s\S]*?)\n\s*\}", code)
            for task_name in task_names:
                cancel_pattern = rf"\bself\.{re.escape(task_name)}\?\.cancel\s*\("
                if not deinit_match or not re.search(cancel_pattern, deinit_match.group(1)):
                    findings.append(semantic_finding(
                        path, lines, line_for_pattern(code_lines, rf"\b{re.escape(task_name)}\b"),
                        "stored-task-cancelled-in-deinit", "error",
                        f"Cancel {task_name} during deinitialization.",
                    ))

                assignment_count = len(re.findall(rf"\bself\.{re.escape(task_name)}\s*=\s*Task\b", code))
                non_deinit_code = code[:deinit_match.start()] + code[deinit_match.end():] if deinit_match else code
                if assignment_count > 1 and not re.search(cancel_pattern, non_deinit_code):
                    findings.append(semantic_finding(
                        path, lines, line_for_pattern(code_lines, rf"\b{re.escape(task_name)}\b"),
                        "stored-task-cancelled-before-replacement", "review",
                        f"Cancel replaceable {task_name} before assigning its replacement, or document the mutual-exclusion guard.",
                    ))

            if task_names and not deinit_match:
                findings.append(semantic_finding(
                    path, lines, class_line, "stored-task-deinit", "error",
                    "Cancel every stored task during deinitialization.",
                ))

            if re.search(r"\bisLoading\s*=\s*true", code) and re.search(r"\bTask\s*\{", code) and not re.search(
                r"\bdefer\s*\{", code
            ):
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"isLoading\s*=\s*true"),
                    "task-missing-defer", "error",
                    "Use defer for paired presentation cleanup and loading-state completion.",
                ))

            if "shouldShowEmptyState" in code:
                for required in ("hasCompletedInitialLoad", "isLoading", "hasContent"):
                    if required not in code:
                        findings.append(semantic_finding(
                            path, lines, line_for_pattern(code_lines, r"shouldShowEmptyState"),
                            "empty-state-gating", "error",
                            "Gate empty state with hasCompletedInitialLoad, isLoading, and hasContent.",
                        ))
                        break

    if is_screen:
        declaration_line = line_for_pattern(code_lines, r"\bstruct\s+\w+(?:Screen|Sheet)\b")

        if re.search(r"\b\w+ViewModel\b", code) and "@StateObject" not in code:
            findings.append(semantic_finding(
                path, lines, declaration_line, "screen-stateobject-ownership", "review",
                "Let the standard screen own its injected ViewModel with @StateObject.",
            ))

        if ".onFirstAppear" in code and not re.search(r"\.onFirstAppear\s*\{\s*\[weak\s+viewModel\]", code):
            findings.append(semantic_finding(
                path, lines, line_for_pattern(code_lines, r"\.onFirstAppear"),
                "screen-first-appear-weak-capture", "error",
                "Capture the ViewModel weakly in onFirstAppear.",
            ))

        if re.search(r"(?:self\.)?viewModel\??\.track\s*\(", code):
            findings.append(semantic_finding(
                path, lines, line_for_pattern(code_lines, r"viewModel.*\.track\s*\("),
                "screen-no-direct-track", "error",
                "Route standard screen analytics through viewModel.handleFirstAppear(), not a direct track() call.",
            ))

        if "AppHeaderScrollView" in code:
            if not re.search(r"AppHeaderScrollView[^\{]*\{\s*navHeader\s*\(\s*\)", code):
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"AppHeaderScrollView"),
                    "screen-nav-header-helper", "error",
                    "Call navHeader() directly from the AppHeaderScrollView header closure.",
                ))
            if not re.search(r"\bfunc\s+navHeader\s*\([^)]*\)\s*->\s*some\s+View", code):
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"AppHeaderScrollView"),
                    "screen-nav-header-helper", "error",
                    "Define navHeader() as a focused some View helper.",
                ))

        wrapper_groups = (
            ("@Environment", r"@Environment\b"),
            ("@Binding", r"@Binding\b"),
            ("@State", r"@State(?:Object)?\b"),
            ("@FocusState", r"@FocusState\b"),
        )
        present_groups: list[tuple[str, int, int]] = []

        for name, pattern in wrapper_groups:
            positions = [
                number
                for number, source in enumerate(code_lines, start=1)
                if re.search(pattern, source)
            ]
            if positions:
                present_groups.append((name, min(positions), max(positions)))

        starts = [group[1] for group in present_groups]
        if starts != sorted(starts):
            findings.append(semantic_finding(
                path, lines, min(starts), "screen-member-order", "error",
                "Order property-wrapper sections as @Environment, @Binding, @State/@StateObject, then @FocusState.",
            ))

        for previous, current in zip(present_groups, present_groups[1:]):
            between = lines[previous[2]:current[1] - 1]
            if between and not any(not line.strip() for line in between):
                findings.append(semantic_finding(
                    path, lines, current[1], "screen-section-spacing", "error",
                    f"Keep a blank line between the {previous[0]} and {current[0]} sections.",
                ))

        member_entries = screen_member_entries(code_lines)
        highest_rank = 0
        previous_section: tuple[int, int, str] | None = None

        for entry in member_entries:
            line_number, rank, section = entry
            if rank < highest_rank:
                findings.append(semantic_finding(
                    path, lines, line_number, "screen-member-order", "error",
                    "Order screen sections as environment, binding, state, focus, stored properties, computed properties, methods, then view logic.",
                ))
                break
            highest_rank = max(highest_rank, rank)

            if previous_section and previous_section[2] != section:
                previous_line = lines[line_number - 2] if line_number >= 2 else ""
                if previous_line.strip():
                    findings.append(semantic_finding(
                        path, lines, line_number, "screen-section-spacing", "error",
                        f"Keep a blank line before the {section} section.",
                    ))
                    break

            previous_section = entry

        if "@Environment(\\.style)" in code and "Style.shared" in code:
            findings.append(semantic_finding(
                path, lines, line_for_pattern(code_lines, r"Style\.shared"),
                "screen-active-style", "review",
                "Prefer self.style in an environment-styled production screen; reserve Style.shared for static/default contexts.",
            ))

        if "#Preview" in code:
            if "mockResolve(" not in code:
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"#Preview"),
                    "preview-mock-resolve", "review",
                    "Resolve standard preview ViewModels with mockResolve(...).",
                ))
            if ".withMockServices(" not in code and ".withMockServices()" not in code:
                findings.append(semantic_finding(
                    path, lines, line_for_pattern(code_lines, r"#Preview"),
                    "preview-with-mock-services", "review",
                    "Apply the project mock service/style wrapper to standard screen previews.",
                ))

    return findings


def scan(path: Path, allowed_lines: set[int] | None = None) -> list[Finding]:
    findings: list[Finding] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [
            Finding(
                path=str(path),
                line=1,
                column=1,
                rule="unreadable-file",
                severity="error",
                message=str(error),
                source="",
            )
        ]

    code_lines = mask_non_code(lines)

    for line_number, (source, code_source) in enumerate(zip(lines, code_lines), start=1):
        if allowed_lines is not None and line_number not in allowed_lines:
            continue

        for rule in RULES:
            for match in rule.pattern.finditer(code_source):
                findings.append(
                    Finding(
                        path=str(path),
                        line=line_number,
                        column=match.start() + 1,
                        rule=rule.identifier,
                        severity=rule.severity,
                        message=rule.message,
                        source=source.strip(),
                    )
                )

        if source.rstrip() != source:
            findings.append(
                Finding(
                    path=str(path),
                    line=line_number,
                    column=len(source.rstrip()) + 1,
                    rule="trailing-whitespace",
                    severity="error",
                    message="Remove trailing whitespace.",
                    source=source.rstrip(),
                )
            )

    findings.extend(semantic_scan(path, lines, code_lines, allowed_lines))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan Swift files for deterministic Sako-style violations and review hints."
    )
    parser.add_argument("paths", nargs="+", help="Swift files or directories to scan")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a non-zero status for review findings as well as errors",
    )
    parser.add_argument(
        "--diff-base",
        metavar="REF",
        help="Report only added or modified lines relative to a Git ref, such as HEAD",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Group findings by rule and show only representative locations",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=3,
        metavar="COUNT",
        help="Maximum representative locations per summary group (default: 3)",
    )
    args = parser.parse_args()

    if args.summary and args.format != "text":
        parser.error("--summary cannot be combined with --format json")
    if args.max_examples < 1:
        parser.error("--max-examples must be at least 1")

    return args


def print_summary(findings: list[Finding], file_count: int, max_examples: int) -> None:
    error_count = sum(finding.severity == "error" for finding in findings)
    review_count = len(findings) - error_count
    print(
        f"Scanned {file_count} Swift file(s): {len(findings)} finding(s) "
        f"({error_count} error, {review_count} review)."
    )

    grouped: dict[tuple[str, str], list[Finding]] = {}
    for finding in findings:
        grouped.setdefault((finding.rule, finding.message), []).append(finding)

    ordered_groups = sorted(
        grouped.items(),
        key=lambda item: (
            0 if any(finding.severity == "error" for finding in item[1]) else 1,
            -len(item[1]),
            item[0][0],
            item[0][1],
        ),
    )

    for (rule, message), rule_findings in ordered_groups:
        severity = "error" if any(
            finding.severity == "error" for finding in rule_findings
        ) else "review"
        affected_files = len({finding.path for finding in rule_findings})
        examples = ", ".join(
            f"{finding.path}:{finding.line}"
            for finding in rule_findings[:max_examples]
        )
        remaining = len(rule_findings) - max_examples
        suffix = f" (+{remaining} more)" if remaining > 0 else ""
        print(
            f"- {severity}: {rule}: {len(rule_findings)} finding(s) in "
            f"{affected_files} file(s) — {message}"
        )
        print(f"  examples: {examples}{suffix}")


def main() -> int:
    args = parse_args()
    files = swift_files(args.paths)

    if not files:
        print("No Swift files found.", file=sys.stderr)
        return 2

    findings = [
        finding
        for path in files
        for finding in scan(
            path,
            changed_lines(path, args.diff_base) if args.diff_base else None,
        )
    ]

    if args.summary and findings:
        print_summary(findings, len(files), args.max_examples)
    elif args.format == "json":
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(
                f"{finding.path}:{finding.line}:{finding.column}: "
                f"{finding.severity}: {finding.message} [{finding.rule}]"
            )
    else:
        print(f"No findings in {len(files)} Swift file(s).")

    has_error = any(finding.severity == "error" for finding in findings)
    has_strict_finding = args.strict and bool(findings)
    return 1 if has_error or has_strict_finding else 0


if __name__ == "__main__":
    raise SystemExit(main())
