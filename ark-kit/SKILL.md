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
- **Availability:** Separate unsupported SDK/device/system capability, temporarily disabled hardware/service, missing grant, and operational failure. For flows calling multiple APIs, retain the failing API identity at its error boundary or in per-request state, without a shared mutable stage across concurrent requests. Scope an API-specific unsupported error, state, and user message to that API or a feature that depends on it; do not infer that unrelated APIs or the entire device capability are unsupported. When a documented error changes which calls are allowed, follow the target-version action in control flow and user guidance; if recovery criteria are undocumented, report the uncertainty instead of inventing retry or permanent prohibition. If versioned guidance says to stop calling a particular API, apply that action and do not suggest retrying later unless a recovery condition is documented; separate this capability handling from stale page UI delivery. For each error whose documented handling limits future calls, check the actual failure branch, subsequent call guard, and user message together; a generic error fallback is not that handling. A current request must deliver its own outcome instead of substituting stale page-facing error state; keep independently required capability actions separate and do not infer recovery from a later success. For continuous samples, use supported metadata and the existing feature contract to determine validity and freshness, handle stale or invalid values, and recover on valid data. Do not invent fields or universal thresholds, or present old values as current. Provide a truthful feature-level fallback or unavailable state; never return fabricated sensor or service data as a successful result.
- **Background behavior:** Check the actual API, Ability/context, task eligibility, and lifecycle restrictions. Ordinary timers are not a guarantee of background execution. If the work must outlive a page, establish an authorized supported owner; do not introduce keep-alive workarounds or new background privileges silently.
- **Resources:** Record acquisition, owner, active scope, stop/unsubscribe, and final release for listeners, sessions, streams, file handles, and controllers. Cover partial initialization, repeated entry, loss of grant/service, and late callbacks. Store/context handles must not accidentally extend a destroyed UI owner's lifetime. For a page-owned capability flow whose result matters only while visible, invalidate eligibility to deliver page-scoped results on actual visibility loss as well as disposal using lifecycle events verified against the target SDK's official documentation; preserve flows required to outlive that visibility change according to their contract. For that flow, recheck ownership after each asynchronous stage before starting downstream work or updating success, error, or loading state; allow user-initiated retry on re-entry only when consistent with the capability's documented error and recovery contract, without obsolete completion clearing newer state. Keep required resource cleanup independent; ignoring results does not cancel work or change a caller's Promise contract.
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
