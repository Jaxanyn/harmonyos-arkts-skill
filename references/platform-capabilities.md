# Platform Capabilities

## Capability First

Before calling a HarmonyOS system API, inspect the target project's existing imports, module declarations, permissions, and SDK level. Prefer the official Kit already used by the project. Treat the current project configuration and official documentation as authoritative over remembered APIs.

## Permissions

Separate declaration, runtime authorization, and feature behavior:

1. Confirm whether the capability requires a declared permission.
2. Request runtime authorization at the user action or feature entry point when required.
3. Handle grant, denial, cancellation, and unavailable capability separately.
4. Change `module.json5` only after the user has explicitly authorized the permission change.

## Data And Files

Keep bundled resources, sandbox files, user-visible exports, caches, and durable user data separate. Validate external input before parsing. Reuse the project's storage abstraction and its error handling. A cache must be recreatable; user data must have an intentional persistence and recovery path.

## Network And Concurrent Work

Use cancellation or request identity when results can arrive out of order. Bound repeated work such as downloads, scans, map tile loads, batch imports, uploads, or sync jobs. Keep network, I/O, and parsing off the UI-critical path when the platform API supports asynchronous execution.

## Specialized Boundaries

For MapKit, GNSS, Bluetooth, media, sensors, WebView, notifications, file access, or other hardware-facing work, search for an existing manager, adapter, or service first. Preserve the public interface and isolate platform-specific types at that boundary.

For C/C++, Node-API, CMake, ABI, or shared-library loading, use `$ark-native`. Do not add a native library, dependency, permission, or build configuration merely because another project used one.

## Permission Recovery And Revocation

Determine whether the selected permission/API requires runtime authorization at all. Check current state at the appropriate feature boundary; a saved boolean is not an authority for today's grant. Map returned results to individual requested permissions and define partial-grant behavior. Do not invent a distinct cancellation result when the API reports it as denial or another outcome.

Do not assume a denied request can always show another prompt. Offer the documented, version-compatible recovery path from an explicit user action, without forcing settings navigation or repeated prompts. On return, re-check the grant and feature prerequisites. Handle grant revocation during an active session using supported observation or checks, then stop or degrade the affected operation and release resources.

## Availability And Background Work

| Condition | Feature response |
| --- | --- |
| API absent or unsupported target | Use a verified compatible path or mark the feature unavailable; do not import an invented replacement. |
| Device/system capability missing | Disable or degrade only the affected feature with a clear reason. |
| Hardware/service temporarily disabled | Explain the relevant user action and support a bounded retry when appropriate. |
| Permission denied or revoked | Respect the decision, release affected work, and offer an explicit recovery path. |
| Operational failure after initialization | Preserve useful existing state where appropriate and report actionable failure without fabricating success. |

Foreground visibility, process lifetime, supported background tasks, and device availability are distinct. Check the actual API's context/Ability and task eligibility before moving work beyond a page. Do not assume timers, polling, or an async function can keep the process alive. Use an existing authorized platform mechanism if continuous work is required; otherwise define pause, interrupted completion, and resume/reconciliation behavior.

## Resource Ledger

For each changed registration/session/stream record acquisition, owner, active lifetime, pause/stop, release, and reacquisition. Retain the registration identity needed for unsubscription where the API requires it. Release only resources that were successfully acquired on partial initialization failure. Make repeated setup/teardown safe and prevent callbacks for an obsolete owner from updating UI.

Use the appropriate context for the capability and scope. Do not retain a UI context indefinitely in a process-global singleton. When another live consumer shares a resource, one page exiting must not stop the shared session unexpectedly. Distinguish removing a subscriber from closing the underlying capability.

## Storage, Export, And Cleanup

Track bundled input, app-owned working data, caches, durable records, and user-visible exports separately. A picker selection or URI grants a specific access scope, not arbitrary filesystem ownership. Follow documented URI/descriptor APIs and access duration; validate names, sizes, and destinations at untrusted boundaries before writing.

For an export, handle cancellation, partial write, disk-full/error, and final success. Clean up only partial artifacts owned by this operation; do not delete an existing user file to recover from failure. Confirm the actual write/close result before claiming the export succeeded. Document retention and cleanup for captured or downloaded sensitive data and keep it out of logs. Storage migration/transaction coordination belongs to [async-data-consistency.md](async-data-consistency.md).

## Official Lookup Entry Points

Use [official-document-evidence.md](official-document-evidence.md) to resolve version and application-type applicability. Huawei's [permission request guidance](https://developer.huawei.com/consumer/cn/doc/doccenter-capabilities/request-app-permissions) and [permission recovery FAQ](https://developer.huawei.com/consumer/cn/doc/doccenter-dev-faq/faqs-access-control-15) provide starting points. Confirm exact API signatures and constraints for the target SDK instead of copying a fixed settings URI, permission group, or release-specific snippet.
