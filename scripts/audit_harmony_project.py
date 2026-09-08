#!/usr/bin/env python3
"""Read-only HarmonyOS Stage project scanner for Ark skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TEXT_EXTENSIONS = {".json5", ".json", ".ts", ".ets", ".cpp", ".cc", ".c", ".h", ".hpp", ".cmake"}
MAX_TEXT_BYTES = 512_000
CONFIG_FILES = [
    "AppScope/app.json5",
    "build-profile.json5",
    "oh-package.json5",
    "oh-package-lock.json5",
]
MODULE_CONFIG_NAMES = {"module.json5", "build-profile.json5", "oh-package.json5", "oh-package-lock.json5"}
PROTECTED_PATTERNS = {
    "signing config": [r"signingConfigs", r"certpath", r"storeFile", r"keyPassword", r"storePassword"],
    "package identity": [r"bundleName", r"appIdentifier", r"client_id", r"appId"],
    "sdk compatibility": [r"targetSdkVersion", r"compatibleSdkVersion", r"compileSdkVersion"],
    "permissions": [r"requestPermissions", r"ohos\.permission\."],
    "dependencies": [r"\"dependencies\"", r"\"devDependencies\"", r"file:.*\.so"],
    "native build": [r"externalNativeOptions", r"CMakeLists\.txt", r"add_library", r"target_link_libraries"],
}


def read_text(path: Path, warnings: list[dict[str, str]] | None = None, root: Path | None = None) -> str:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            raise ValueError("oversized content skipped")
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError, ValueError) as error:
        if warnings is not None:
            warnings.append({"path": rel(root, path) if root else path.name,
                             "reason": type(error).__name__})
        return ""


def is_link(path: Path) -> bool:
    try:
        return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & 0x400)
    except OSError:
        return True


def find_files(root: Path, warnings: list[dict[str, str]] | None = None) -> list[Path]:
    ignored = {".git", ".hvigor", ".cxx", ".preview", "oh_modules", "node_modules", "build", ".idea", "__pycache__"}
    files: list[Path] = []
    def onerror(error: OSError) -> None:
        if warnings is not None:
            warnings.append({"path": "(directory)", "reason": type(error).__name__})
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=onerror):
        base = Path(directory)
        dirs[:] = sorted(d for d in dirs if d not in ignored and not is_link(base / d))
        files.extend(base / name for name in sorted(names) if not is_link(base / name))
    return sorted(files)


def strip_comments(text: str) -> str:
    # Preserve quoted URLs/strings. This is lexical filtering, not a JSON5 parser.
    token = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
    return re.sub(token, lambda m: " " if m[0].startswith(("//", "/*")) else m[0], text)


def field_values(text: str, field: str) -> list[str]:
    pattern = rf'''(?<![\w$])(?:"{field}"|'{field}'|{field})\s*:\s*(?:"([^"\n]*)"|'([^'\n]*)'|(\d+(?:\.\d+)?))'''
    return sorted({next(v for v in match.groups() if v is not None)
                   for match in re.finditer(pattern, strip_comments(text))})


def module_root(root: Path, manifest: Path) -> str:
    parts = manifest.relative_to(root).parts
    if len(parts) >= 4 and parts[-3:-1] == ("src", "main"):
        return Path(*parts[:-3]).as_posix() if parts[:-3] else "."
    return manifest.parent.relative_to(root).as_posix()


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def grep_values(pattern: str, text: str) -> list[str]:
    return sorted(set(match.group(1) for match in re.finditer(pattern, text)))


def classify_project(root: Path, files: list[Path]) -> dict[str, Any]:
    rels = {rel(root, p) for p in files}
    module_jsons = [p for p in files if p.name == "module.json5"]
    cmake_files = [p for p in files if p.name == "CMakeLists.txt"]
    dts_files = [p for p in files if p.suffix == ".ts" and p.name.endswith(".d.ts")]
    ets_files = [p for p in files if p.suffix == ".ets"]
    page_files = [p for p in ets_files if "/pages/" in rel(root, p)]
    component_files = [p for p in ets_files if "/components/" in rel(root, p)]
    test_files = [p for p in ets_files if "/test/" in rel(root, p).lower() or "/ohostest/" in rel(root, p).lower()]

    production = [p for p in module_jsons if "ohostest" not in {s.lower() for s in p.relative_to(root).parts}]
    modules = sorted({module_root(root, p) for p in production})
    har_hsp_markers = []
    for p in files:
        r = rel(root, p)
        if p in production:
            text = read_text(p)
            if set(field_values(text, "type")) & {"har", "hsp", "shared"}:
                har_hsp_markers.append(r)

    return {
        "configFiles": sorted(r for r in rels if r in CONFIG_FILES or Path(r).name in MODULE_CONFIG_NAMES),
        "modules": modules,
        "moduleJson5": sorted(rel(root, p) for p in module_jsons),
        "moduleTypes": [{"root": module_root(root, p), "manifest": rel(root, p),
                         "types": field_values(read_text(p), "type")} for p in production],
        "etsFiles": len(ets_files),
        "pages": sorted(rel(root, p) for p in page_files),
        "components": sorted(rel(root, p) for p in component_files),
        "tests": sorted(rel(root, p) for p in test_files),
        "native": {
            "cmake": sorted(rel(root, p) for p in cmake_files),
            "declarations": sorted(rel(root, p) for p in dts_files),
            "cppFiles": sorted(rel(root, p) for p in files if p.suffix in {".c", ".cc", ".cpp", ".h", ".hpp"}),
        },
        "libraryBoundaryCandidates": sorted(har_hsp_markers),
    }


def collect_signals(root: Path, files: list[Path], warnings: list[dict[str, str]] | None = None) -> dict[str, Any]:
    texts = {p: strip_comments(read_text(p, warnings, root)) for p in files
             if p.suffix in TEXT_EXTENSIONS or p.name == "CMakeLists.txt"}
    scanned_text = "\n".join(texts.values())
    permissions = sorted({value for p, text in texts.items() if p.name == "module.json5"
                          for value in field_values(text, "name") if value.startswith("ohos.permission.")})
    imports = grep_values(r"from\s+['\"](@kit\.[^'\"]+)['\"]", scanned_text)
    sdk_fields = [{"path": rel(root, p), "field": key, "values": values}
                  for p, text in texts.items() if p.name == "build-profile.json5"
                  for key in ("targetSdkVersion", "compatibleSdkVersion", "compileSdkVersion")
                  if (values := field_values(text, key))]
    sdk_versions = sorted({value for item in sdk_fields for value in item["values"]})

    protected: dict[str, list[str]] = {}
    for label, patterns in PROTECTED_PATTERNS.items():
        hits = []
        for p, text in texts.items():
            if any(re.search(pattern, text) for pattern in patterns):
                hits.append(rel(root, p))
        if hits:
            protected[label] = sorted(set(hits))

    routes: list[str] = ["$ark-scan"]
    if re.search(r"@Component|@Entry|@State|@Link|@StorageLink|/components/|/pages/", scanned_text):
        routes.append("$ark-ui")
    if re.search(r"ViewModel|Service|Repository|async |Promise<|cache|parser|preferences|relationalStore", scanned_text):
        routes.append("$ark-flow")
    if permissions or imports:
        routes.append("$ark-kit")
    if any(p.name == "CMakeLists.txt" or p.suffix in {".c", ".cc", ".cpp"} for p in files) or re.search(r"napi_|externalNativeOptions|\.so['\"]", scanned_text):
        routes.append("$ark-native")
    routes.append("$ark-check")

    return {
        "permissions": permissions,
        "kitImports": imports,
        "sdkVersions": sdk_versions,
        "sdkFields": sdk_fields,
        "modelEvidence": {
            "stage": sorted(rel(root, p) for p in files if p.name == "module.json5"),
            "faCandidates": sorted(rel(root, p) for p, text in texts.items()
                                   if p.name == "config.json" and re.search(r'[\"\']abilities[\"\']\s*:', text)),
        },
        "stateManagement": [{"path": rel(root, p), "markers": markers}
                            for p, text in texts.items() if p.suffix == ".ets"
                            if (markers := sorted(set(re.findall(r"@(ComponentV2|ObservedV2|Trace|Local|Param|Component|Observed|State|Link|Prop)\b", text))))],
        "protectedSurfaces": protected,
        "suggestedRoutes": list(dict.fromkeys(routes)),
    }


def build_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")
    warnings: list[dict[str, str]] = []
    files = find_files(root, warnings)
    return {
        "projectRoot": str(root),
        "summary": classify_project(root, files),
        "signals": collect_signals(root, files, warnings),
        "warnings": warnings,
        "limitations": ["Heuristic inventory, not a JSON5 parser or compatibility verdict.",
                        "Generated/dependency directories and symlinks/junctions are skipped.",
                        "Text above 512000 bytes or unreadable text is skipped and listed in warnings.",
                        "Module roots outside the supplied directory and computed configuration require manual inspection."],
    }


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    signals = report["signals"]
    print(f"Project: {report['projectRoot']}")
    print(f"Modules: {', '.join(summary['modules']) or '(none detected)'}")
    print(f"ETS files: {summary['etsFiles']}")
    print(f"Config files: {', '.join(summary['configFiles']) or '(none detected)'}")
    print(f"SDK versions: {', '.join(signals['sdkVersions']) or '(none detected)'}")
    print(f"Permissions: {', '.join(signals['permissions']) or '(none detected)'}")
    print(f"Kit imports: {', '.join(signals['kitImports']) or '(none detected)'}")
    print(f"Native CMake: {', '.join(summary['native']['cmake']) or '(none detected)'}")
    print(f"Native declarations: {', '.join(summary['native']['declarations']) or '(none detected)'}")
    print(f"Suggested routes: {' -> '.join(signals['suggestedRoutes'])}")
    for warning in report["warnings"]:
        print(f"Warning: {warning['path']}: {warning['reason']}")
    for limitation in report["limitations"]:
        print(f"Limit: {limitation}")
    if signals["protectedSurfaces"]:
        print("Protected surfaces:")
        for label, paths in signals["protectedSurfaces"].items():
            print(f"- {label}: {', '.join(paths)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only HarmonyOS Stage project scanner for Ark skills.")
    parser.add_argument("project", help="HarmonyOS project root to scan")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    report = build_report(Path(args.project))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
