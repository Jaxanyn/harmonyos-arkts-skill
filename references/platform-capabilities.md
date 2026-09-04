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
