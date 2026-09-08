---
name: ark-kit
description: Integrate HarmonyOS ArkTS system capabilities, including permissions, files, storage, network, WebView, MapKit, GNSS, Bluetooth, media, and device APIs, using official constraints and explicit failure behavior. Use $ark-native instead when the primary change is C/C++, Node-API, CMake, ABI, or shared-library loading.
---

# Ark Kit

Treat each system API as a capability contract, not merely an import.

Use [official-document-evidence.md](../references/official-document-evidence.md) when retrieving API constraints. Distinguish compile-time API presence, minimum supported version, device/system capability, permission declaration, and runtime authorization. Record the applicable source; a search snippet or unversioned mirror is not sufficient platform evidence. Route language-only diagnostics to `$ark-language` without changing Kit configuration to suppress them.

## Implement

1. Inspect existing imports, adapters, module declarations, permissions, and SDK level. Reuse the project's compatible Kit and boundary.
2. Retrieve the official documentation for the proposed API and capture the facts that govern API level, permission declaration, runtime authorization, availability, error behavior, and required configuration.
3. Separate declaration, runtime authorization, and feature behavior. Place authorization at the user action or feature entry point, then represent grant, denial, cancellation, and unavailable capability distinctly.
4. Keep bundled resources, sandbox files, user-visible exports, caches, and durable data separate. Put I/O, parsing, and network work off the UI-critical path when the platform supports it.
5. Present the smallest `module.json5`, dependency, or build-configuration diff for explicit user approval before editing that surface. If the change crosses into C/C++, `.d.ts`, CMake, ABI, or shared-library loading, route that portion to `$ark-native`.

## Acceptance

For a capability change, define:

- API/Kit name and official constraint that affected implementation.
- Permission declaration and runtime authorization behavior, if any.
- SDK/API compatibility and unavailable-device behavior.
- Data location, retention, and cleanup rule when storage or export is involved.
- Runtime/device acceptance check when static verification cannot observe the capability.

## Deliver: Capability Contract

Report capability, existing boundary, evidence profile, official constraint, SDK/API compatibility, declaration change, authorization behavior, unavailable/denied/failure behavior, data location where relevant, any `$ark-native` handoff, and required runtime acceptance checks. Read [platform-capabilities.md](../references/platform-capabilities.md) for storage, I/O, and concurrent-work boundaries. Completion requires every configuration change to have its purpose and user approval recorded.
