---
name: ark-kit
description: Integrate HarmonyOS ArkTS system capabilities, including permissions, files, storage, network, WebView, MapKit, GNSS, Bluetooth, media, and device APIs, using official constraints and explicit failure behavior. Use $ark-native instead when the primary change is C/C++, Node-API, CMake, ABI, or shared-library loading.
---

# Ark Kit

Treat each system API as a capability contract, not merely an import.

Use [official-document-evidence.md](../references/official-document-evidence.md) when retrieving API constraints. Distinguish compile-time API presence, minimum supported version, device/system capability, permission declaration, and runtime authorization. Record the applicable source; a search snippet or unversioned mirror is not sufficient platform evidence. Route language-only diagnostics to `$ark-language` without changing Kit configuration to suppress them.

Select implementation, diagnosis, or review from the request. Read [platform-capabilities.md](../references/platform-capabilities.md) for the affected permission, background, resource, or storage boundary. Choose the minimum capability needed for the user action and reuse the current adapter rather than introducing another manager.

## Implement

1. Inspect existing imports, adapters, module declarations, permissions, and SDK level. Reuse the project's compatible Kit and boundary.
2. Retrieve the official documentation for the proposed API and capture the facts that govern API level, permission declaration, runtime authorization, availability, error behavior, and required configuration.
3. Separate declaration, runtime authorization, and feature behavior. Place authorization at the user action or feature entry point, then represent grant, denial, cancellation, and unavailable capability distinctly.
4. Keep bundled resources, sandbox files, user-visible exports, caches, and durable data separate. Put I/O, parsing, and network work off the UI-critical path when the platform supports it.
5. Present the smallest `module.json5`, dependency, or build-configuration impact and use existing explicit authorization; ask only for changes outside that scope. If the change crosses into C/C++, native `.d.ts`, CMake, ABI, or shared-library loading, route that portion to `$ark-native`.

## Capability Lifecycle

- **Authorization:** Check the current grant at the feature boundary where required. Handle partial grants and denial, and distinguish cancellation only if the API actually exposes it. Use version-compatible, user-initiated recovery when another permission prompt is unavailable; do not loop prompts or treat a settings round-trip as proof of authorization.
- **Availability:** Separate unsupported SDK/device/system capability, temporarily disabled hardware/service, missing grant, and operational failure. Provide a truthful feature-level fallback or unavailable state; never return fabricated sensor or service data as a successful result.
- **Background behavior:** Check the actual API, Ability/context, task eligibility, and lifecycle restrictions. Ordinary timers are not a guarantee of background execution. If the work must outlive a page, establish an authorized supported owner; do not introduce keep-alive workarounds or new background privileges silently.
- **Resources:** Record acquisition, owner, active scope, stop/unsubscribe, and final release for listeners, sessions, streams, file handles, and controllers. Cover partial initialization, repeated entry, loss of grant/service, and late callbacks. Store/context handles must not accidentally extend a destroyed UI owner's lifetime.
- **Data:** Identify source, destination, access scope, retention, cleanup, and recovery for files and captured data. Respect picker/URI-based access where applicable; do not assume a URI is a writable filesystem path. Separate rebuildable caches from durable user data and user-visible exports.

## Behavior To Specify

For a capability change, define:

- API/Kit name and official constraint that affected implementation.
- Permission declaration and runtime authorization behavior, if any.
- SDK/API compatibility and unavailable-device behavior.
- Data location, retention, and cleanup rule when storage or export is involved.
- Runtime/device acceptance check when static verification cannot observe the capability.

## Deliver: Capability Contract

Report capability, existing boundary, evidence profile, official constraint, SDK/API compatibility, declaration change, authorization behavior, unavailable/denied/failure behavior, data location where relevant, any `$ark-native` handoff, and required runtime acceptance checks. Read [platform-capabilities.md](../references/platform-capabilities.md) for storage, I/O, and concurrent-work boundaries. Completion requires every configuration change to have its purpose and user approval recorded.

For changed lifetimes, include foreground/background, reacquisition, revocation, and disposal behavior; for stored data include retention and failure cleanup. Delegate request/cache coordination to `$ark-flow`. Route checks to `$ark-check` only within authorized scope. If the user excludes tests/builds/acceptance, keep runtime claims explicitly unverified and do not execute checks.
