#!/usr/bin/env python3
"""Read-only HarmonyOS Stage project scanner for Ark skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TEXT_EXTENSIONS = {".json5", ".json", ".ts", ".ets", ".d.ts", ".txt", ".md", ".yaml", ".yml"}
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


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def find_files(root: Path) -> list[Path]:
    ignored = {".git", ".hvigor", ".cxx", ".preview", "oh_modules", "node_modules", "build", ".idea"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


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

    modules = sorted({p.relative_to(root).parts[0] for p in module_jsons if len(p.relative_to(root).parts) > 1})
    har_hsp_markers = []
    for p in files:
        r = rel(root, p)
        if p.name == "module.json5":
            text = read_text(p)
            if re.search(r'"type"\s*:\s*"(?:har|hsp|shared|entry|feature)"', text):
                har_hsp_markers.append(r)

    return {
        "configFiles": sorted(r for r in rels if r in CONFIG_FILES or Path(r).name in MODULE_CONFIG_NAMES),
        "modules": modules,
        "moduleJson5": sorted(rel(root, p) for p in module_jsons),
        "etsFiles": len(ets_files),
        "pages": sorted(rel(root, p) for p in page_files[:25]),
        "components": sorted(rel(root, p) for p in component_files[:25]),
        "tests": sorted(rel(root, p) for p in test_files[:25]),
        "native": {
            "cmake": sorted(rel(root, p) for p in cmake_files),
            "declarations": sorted(rel(root, p) for p in dts_files),
            "cppFiles": sorted(rel(root, p) for p in files if p.suffix in {".c", ".cc", ".cpp", ".h", ".hpp"})[:50],
        },
        "libraryBoundaryCandidates": sorted(har_hsp_markers),
    }


def collect_signals(root: Path, files: list[Path]) -> dict[str, Any]:
    scanned_text = "\n".join(read_text(p) for p in files if p.suffix in TEXT_EXTENSIONS and p.stat().st_size < 512_000)
    permissions = grep_values(r'"name"\s*:\s*"(ohos\.permission\.[^"]+)"', scanned_text)
    imports = grep_values(r"from\s+['\"](@kit\.[^'\"]+)['\"]", scanned_text)
    sdk_versions = grep_values(r'"(?:targetSdkVersion|compatibleSdkVersion|compileSdkVersion)"\s*:\s*"([^"]+)"', scanned_text)

    protected: dict[str, list[str]] = {}
    for label, patterns in PROTECTED_PATTERNS.items():
        hits = []
        for p in files:
            if p.suffix not in TEXT_EXTENSIONS and p.name != "CMakeLists.txt":
                continue
            try:
                if p.stat().st_size > 512_000:
                    continue
            except OSError:
                continue
            text = read_text(p)
            if any(re.search(pattern, text) for pattern in patterns):
                hits.append(rel(root, p))
        if hits:
            protected[label] = sorted(set(hits))[:20]

    routes: list[str] = ["$ark-scan"]
    if re.search(r"@Component|@Entry|@State|@Link|@StorageLink|/components/|/pages/", scanned_text):
        routes.append("$ark-ui")
    if re.search(r"ViewModel|Service|Repository|async |Promise<|cache|parser|preferences|relationalStore", scanned_text):
        routes.append("$ark-flow")
    if permissions or imports:
        routes.append("$ark-kit")
    if re.search(r"napi_|CMakeLists\.txt|externalNativeOptions|\.so|add_library|target_link_libraries", scanned_text):
        routes.append("$ark-native")
    routes.append("$ark-check")

    return {
        "permissions": permissions,
        "kitImports": imports,
        "sdkVersions": sdk_versions,
        "protectedSurfaces": protected,
        "suggestedRoutes": list(dict.fromkeys(routes)),
    }


def build_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")
    files = find_files(root)
    return {
        "projectRoot": str(root),
        "summary": classify_project(root, files),
        "signals": collect_signals(root, files),
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
