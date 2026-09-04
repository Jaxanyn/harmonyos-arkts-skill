---
name: ark-scan
description: Inspect a pure-native HarmonyOS Stage-model project before modifying it. Use when task scope, file ownership, project shape, evidence profile, configuration impact, safe boundaries, Native/NDK involvement, or the next Ark command is unclear.
---

# Ark Scan

Map the live project before editing. End with the smallest safe next action.

## Inspect

1. Identify modules, entry abilities, page routing, source and resource layout, test locations, library modules, and the feature owner.
2. Trace the current request from UI or entry point through state, ViewModel or manager, service, adapter, repository, storage, native, and platform boundary before proposing a new manager, event channel, storage key, dependency, module, or cross-module abstraction.
3. Read only configuration relevant to the request: SDK level, module declaration, permissions, dependencies, build tooling, HAR/HSP/HAP boundaries, native/CMake, signing, and lockfiles.
4. Mark protected surfaces: signing, certificates, package identity, SDK compatibility, local device configuration, credentials, production constants, generated output, dependencies, lockfiles, native build files, and public library interfaces.
5. Assign an evidence profile: `local`, `doc-bound`, `config-bound`, or `runtime-bound`. Retrieve official documentation only when platform facts constrain the change.

Read [project-shape.md](../references/project-shape.md) when scanning an unfamiliar Stage-model project or library boundary. Read [harmony-risk-boundaries.md](../references/harmony-risk-boundaries.md) when a protected surface may be affected.

## Tool Preflight

When verification or platform evidence may be needed, discover what is available instead of assuming it:

- Official-document lookup or MCP available for API, Kit, permission, API-level, lifecycle, and Native/NDK facts.
- Project build/test scripts, DevEco CLI, Hvigor, ohpm, IDE-generated command surfaces, or local task runners.
- ETS language diagnostics, static checks, device, emulator, hdc, and log access when runtime evidence is in scope.
- Optional read-only project scanner: scripts/audit_harmony_project.py <project-root> [--json] when a quick project-shape inventory would reduce rediscovery.

Record missing tools as constraints, not as failures, unless the user explicitly requested that evidence.

## Deliver: Project Change Map

Report all of the following:

- Affected module and ownership path.
- Entry point and current call path.
- Evidence profile and why it applies.
- Files likely to change and protected surfaces that need approval.
- Official platform constraint, if one affects the request.
- The next command (`$ark-ui`, `$ark-flow`, `$ark-kit`, `$ark-native`, or `$ark-check`) and the reason.

The scan is complete only when another agent can locate the change boundary without rediscovering it.
