#!/usr/bin/env python3
"""First-pass static indexer for hybrid UIKit/SwiftUI iOS dead-code audits.

This script intentionally reports candidates, not final deletion verdicts.
Codex should still trace reachability from live app entry points before
classifying anything as safe to remove.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".build",
    ".git",
    ".swiftpm",
    "Build",
    "Carthage",
    "DerivedData",
    "Pods",
    "SourcePackages",
    "build",
}

TEXT_EXTENSIONS = {
    ".h",
    ".m",
    ".mm",
    ".plist",
    ".storyboard",
    ".strings",
    ".swift",
    ".xib",
    ".xcconfig",
    ".pbxproj",
}

TYPE_RE = re.compile(
    r"(?P<prefix>(?:@\w+(?:\([^)]*\))?\s*)*(?:(?:public|open|internal|private|fileprivate|final)\s+)*)"
    r"(?P<kind>class|struct|enum|protocol|actor)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
    r"(?P<tail>[^{\n]*)"
)
FUNC_RE = re.compile(
    r"(?P<prefix>(?:(?:public|open|internal|private|fileprivate|static|class|final|@objc|dynamic)\s+)*)"
    r"func\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\("
)
PROPERTY_RE = re.compile(
    r"(?P<prefix>(?:(?:public|open|internal|private|fileprivate|static|@Published|@IBOutlet)\s+)*)"
    r"(?P<kind>let|var)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
)
IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
STRING_KEY_RE = re.compile(r'"([^"\n]+)"\s*=')
POD_RE = re.compile(r"^\s*pod\s+['\"]([^'\"]+)['\"]", re.MULTILINE)
PACKAGE_RE = re.compile(r"\.package\s*\([^)]*(?:url|path)\s*:\s*\"([^\"]+)\"")
PRODUCT_RE = re.compile(r"\.product\s*\(\s*name\s*:\s*\"([^\"]+)\"")
WORD_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


@dataclass
class Declaration:
    kind: str
    name: str
    path: Path
    line: int
    prefix: str
    tail: str

    @property
    def risky(self) -> bool:
        text = f"{self.prefix} {self.tail}"
        return any(marker in text for marker in ("public", "open", "@objc", "dynamic", "Codable", "Decodable"))

    @property
    def bridge_kind(self) -> str | None:
        if "UIViewRepresentable" in self.tail:
            return "UIViewRepresentable"
        if "UIViewControllerRepresentable" in self.tail:
            return "UIViewControllerRepresentable"
        if "UIHostingController" in self.tail:
            return "UIHostingController subclass"
        return None


def iter_files(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if root.is_file():
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
            for filename in filenames:
                yield Path(dirpath) / filename


def iter_asset_sets(roots: Iterable[Path]) -> Iterable[Path]:
    suffixes = (".imageset", ".colorset", ".symbolset")
    for root in roots:
        if root.is_file():
            continue
        for dirpath, dirnames, _ in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
            path = Path(dirpath)
            if path.name.endswith(suffixes):
                yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def asset_name(path: Path) -> str:
    return path.name.rsplit(".", 1)[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index iOS dead-code candidates.")
    parser.add_argument("root", type=Path, help="Project root or feature path to scan.")
    parser.add_argument("--focus", action="append", type=Path, help="Additional path to scan instead of the whole root.")
    parser.add_argument("--focus-bridging", action="store_true", help="Only show bridge-oriented candidate sections.")
    parser.add_argument("--include-assets", action="store_true", help="Report likely unused Assets.xcassets image sets.")
    parser.add_argument("--include-dependencies", action="store_true", help="Report import, SPM, and Pod usage hints.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    scan_roots = [p.resolve() if p.is_absolute() else (root / p).resolve() for p in args.focus] if args.focus else [root]

    all_paths = list(iter_files(scan_roots))
    text_paths = [p for p in all_paths if p.suffix in TEXT_EXTENSIONS or p.name in {"Package.swift", "Podfile"}]
    swift_paths = [p for p in text_paths if p.suffix == ".swift"]
    text_by_path = {p: read_text(p) for p in text_paths}
    swift_texts = [text_by_path[p] for p in swift_paths]
    all_texts = list(text_by_path.values())
    all_text_blob = "\n".join(all_texts)
    all_word_counts = Counter(WORD_RE.findall(all_text_blob))
    swift_word_counts = Counter(WORD_RE.findall("\n".join(swift_texts)))

    declarations: list[Declaration] = []
    functions = []
    properties = []
    imports = Counter()

    for path in swift_paths:
        text = text_by_path[path]
        imports.update(IMPORT_RE.findall(text))
        for match in TYPE_RE.finditer(text):
            declarations.append(
                Declaration(
                    kind=match.group("kind"),
                    name=match.group("name"),
                    path=path,
                    line=line_number(text, match.start()),
                    prefix=match.group("prefix") or "",
                    tail=match.group("tail") or "",
                )
            )
        for match in FUNC_RE.finditer(text):
            if args.focus_bridging:
                continue
            name = match.group("name")
            prefix = match.group("prefix") or ""
            references = swift_word_counts[name]
            if ("private" in prefix or "fileprivate" in prefix) and references <= 1:
                functions.append({"name": name, "path": path, "line": line_number(text, match.start()), "references": references})
        for match in PROPERTY_RE.finditer(text):
            if args.focus_bridging:
                continue
            name = match.group("name")
            prefix = match.group("prefix") or ""
            references = swift_word_counts[name]
            if ("private" in prefix or "fileprivate" in prefix or "@Published" in prefix) and references <= 1:
                properties.append(
                    {
                        "name": name,
                        "path": path,
                        "line": line_number(text, match.start()),
                        "references": references,
                        "prefix": prefix.strip(),
                    }
                )

    type_candidates = []
    bridge_candidates = []
    for decl in declarations:
        references = all_word_counts[decl.name]
        item = {
            "kind": decl.kind,
            "name": decl.name,
            "path": decl.path,
            "line": decl.line,
            "references": references,
            "risk": "review" if decl.risky else "candidate",
            "bridge_kind": decl.bridge_kind,
        }
        if decl.bridge_kind:
            bridge_candidates.append(item)
        if references <= 1:
            type_candidates.append(item)

    entry_patterns = ["@main", "@UIApplicationMain", "UIApplicationMain", "class AppDelegate", "class SceneDelegate", "WindowGroup"]
    entry_points = []
    for path, text in text_by_path.items():
        hits = [pattern for pattern in entry_patterns if pattern in text]
        if hits:
            entry_points.append({"path": path, "hits": hits})

    assets = []
    if args.include_assets:
        for path in iter_asset_sets(scan_roots):
            name = asset_name(path)
            references = all_text_blob.count(name)
            if references == 0:
                size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
                assets.append({"name": name, "path": path, "bytes": size})

    strings = []
    for path in text_paths:
        if path.name == "Localizable.strings":
            text = text_by_path[path]
            for match in STRING_KEY_RE.finditer(text):
                key = match.group(1)
                references = all_text_blob.count(key) - text.count(key)
                if references == 0:
                    strings.append({"key": key, "path": path, "line": line_number(text, match.start())})

    dependencies = []
    if args.include_dependencies:
        package_text = "\n".join(text_by_path[p] for p in text_paths if p.name == "Package.swift")
        pod_text = "\n".join(text_by_path[p] for p in text_paths if p.name == "Podfile")
        declared = []
        declared.extend(PRODUCT_RE.findall(package_text))
        declared.extend(PACKAGE_RE.findall(package_text))
        declared.extend(POD_RE.findall(pod_text))
        for dep in sorted(set(declared)):
            module_hint = Path(dep).stem.replace("-", "_")
            used = any(module_hint in module or dep in module for module in imports)
            dependencies.append({"name": dep, "used_by_import_hint": used})

    result = {
        "root": str(root),
        "entry_points": [{"path": rel(i["path"], root), "hits": i["hits"]} for i in entry_points],
        "bridge_candidates": [{**i, "path": rel(i["path"], root)} for i in bridge_candidates],
        "likely_unreferenced_types": [{**i, "path": rel(i["path"], root)} for i in type_candidates],
        "private_members_with_few_references": [{**i, "path": rel(i["path"], root)} for i in functions + properties],
        "unused_assets": [{**i, "path": rel(i["path"], root)} for i in assets],
        "unused_localization_keys": [{**i, "path": rel(i["path"], root)} for i in strings],
        "imports": dict(sorted(imports.items())),
        "dependencies": dependencies,
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("# iOS Dead Code Static Scan")
    print()
    print(f"Root: `{result['root']}`")
    print(f"Swift files scanned: {len(swift_paths)}")
    print()

    print("## Entry Point Hints")
    if result["entry_points"]:
        for item in result["entry_points"]:
            print(f"- `{item['path']}`: {', '.join(item['hits'])}")
    else:
        print("- No obvious entry point hints found in scan scope.")
    print()

    if result["bridge_candidates"]:
        print("## Bridge Candidates")
        for item in result["bridge_candidates"]:
            print(f"- `{item['path']}:{item['line']}` `{item['name']}` ({item['bridge_kind']}), references: {item['references']}, risk: {item['risk']}")
        print()

    if not args.focus_bridging:
        print("## Likely Unreferenced Types")
        if result["likely_unreferenced_types"]:
            for item in result["likely_unreferenced_types"]:
                print(f"- `{item['path']}:{item['line']}` `{item['kind']} {item['name']}`, risk: {item['risk']}")
        else:
            print("- No type declarations with a single lexical reference found.")
        print()

        print("## Private Members With Few References")
        if result["private_members_with_few_references"]:
            for item in result["private_members_with_few_references"]:
                print(f"- `{item['path']}:{item['line']}` `{item['name']}`, references: {item['references']}")
        else:
            print("- No private/fileprivate members with a single lexical reference found.")
        print()

        if args.include_assets:
            print("## Likely Unused Assets")
            if result["unused_assets"]:
                for item in result["unused_assets"]:
                    print(f"- `{item['path']}` ({item['bytes']} bytes)")
            else:
                print("- No unreferenced image/color/symbol sets found by exact-name search.")
            print()

        print("## Likely Unused Localization Keys")
        if result["unused_localization_keys"]:
            for item in result["unused_localization_keys"]:
                print(f"- `{item['path']}:{item['line']}` `{item['key']}`")
        else:
            print("- No Localizable.strings keys with zero exact references found.")
        print()

        if args.include_dependencies:
            print("## Dependency Import Hints")
            if result["dependencies"]:
                for item in result["dependencies"]:
                    status = "has import-like hit" if item["used_by_import_hint"] else "no import-like hit"
                    print(f"- `{item['name']}`: {status}")
            else:
                print("- No SPM products/packages or pods found in scan scope.")
            print()

    print("Note: This scan is lexical. Trace reachability from live entry points before assigning Safe to Remove.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
