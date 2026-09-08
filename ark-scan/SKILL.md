---
name: ark-scan
description: Inspect a pure-native HarmonyOS Stage-model project before modifying it. Use when task scope, file ownership, project shape, evidence profile, configuration impact, safe boundaries, Native/NDK involvement, or the next Ark command is unclear.
---

# Ark Scan

Map the live project before editing. End with the smallest safe next action. A scan is read-only; it does not authorize dependency installation, builds, device changes, or implementation.

## Applicability And Baseline

Read applicable project instructions and existing decisions first. Establish the repository root, branch/revision, dirty files, requested behavior, and affected area. Preserve unrelated edits. Inspect Stage/FA indicators, product/target, configured SDK fields, and the affected components' state-management generation. ArkUI V1/V2 is separate from the ArkTS language version; do not infer either from a marketing version or one decorator elsewhere in the repository.

Use this workflow for the Stage portion of an application or library. For FA-only, framework-only, or ambiguous projects, report the evidence and route to the matching workflow; do not silently migrate the project. Mixed repositories need per-module decisions. Unknown is a valid finding, not permission to assume a new-project default.

## Inspect

1. Identify modules, entry abilities, page routing, source and resource layout, test locations, library modules, and the feature owner.
2. Trace the current request from UI or entry point through state, ViewModel or manager, service, adapter, repository, storage, native, and platform boundary before proposing a new manager, event channel, storage key, dependency, module, or cross-module abstraction.
3. Read only configuration relevant to the request: SDK level, module declaration, permissions, dependencies, build tooling, HAR/HSP/HAP boundaries, native/CMake, signing, and lockfiles.
4. Mark protected surfaces: signing, certificates, package identity, SDK compatibility, local device configuration, credentials, production constants, generated output, dependencies, lockfiles, native build files, and public library interfaces.
5. Record all applicable evidence obligations: `local`, `doc-bound`, `config-bound`, and `runtime-bound` can coexist. Runtime checks never replace API evidence or configuration authorization. Retrieve official documentation only when platform facts constrain the change.

Identify production modules separately from test source sets, and distinguish declared module name from filesystem path. For a shared library, trace public exports and consuming modules before proposing an interface change. Follow profile/resource references rather than assuming pages live in a fixed folder. Check task-relevant local dependency paths and native declarations without reading credentials or dumping complete signing configuration.

Read [project-shape.md](../references/project-shape.md) when scanning an unfamiliar Stage-model project or library boundary. Read [harmony-risk-boundaries.md](../references/harmony-risk-boundaries.md) when a protected surface may be affected.

## Tool Preflight

When verification or platform evidence may be needed, discover what is available instead of assuming it:

- Official-document lookup or MCP available for API, Kit, permission, API-level, lifecycle, and Native/NDK facts.
- Project build/test scripts, DevEco CLI, Hvigor, ohpm, IDE-generated command surfaces, or local task runners.
- ETS language diagnostics, static checks, device, emulator, hdc, and log access when runtime evidence is in scope.
- Optional [read-only scanner](../scripts/audit_harmony_project.py): resolve its path from this skill file, then pass the target project root explicitly. It emits heuristic signals, relative paths, and scan limitations; it does not parse every JSON5 construct or prove project compatibility.

Record missing tools as constraints, not as failures, unless the user explicitly requested that evidence.

For API constraints record the official URL/document identity, applicable version, symbol, and decision it changes. Use a configured official-document tool or the official website; the installed SDK can confirm signatures but not all runtime semantics. If evidence is unavailable, leave the affected platform claim unverified. Do not configure tools or upgrade SDKs as a side effect of scanning.

Follow [official-document-evidence.md](../references/official-document-evidence.md) for lookup, version conflicts, source provenance, and offline fallback. After identifying source kind and toolchain, route ArkTS syntax, typing, or import diagnostics to `$ark-language`.

## Deliver: Project Change Map

Report all of the following:

- Affected module and ownership path.
- Entry point and current call path.
- Evidence profile and why it applies.
- Files likely to change and protected surfaces that need approval.
- Official platform constraint, if one affects the request.
- The next command (`$ark-language`, `$ark-ui`, `$ark-flow`, `$ark-kit`, `$ark-native`, or `$ark-check`) and the reason.

The scan is complete only when another agent can locate the change boundary without rediscovering it.

Include baseline, module applicability, configuration evidence paths, and tool limitations in that map. Report sensitive fields by category and location only, never by value. Reuse the map within the task; refresh only after relevant files, configuration, branch, or scope change. Read [behavior scenarios](../tests/skill-scenarios.md) when validating changes to this skill itself.
