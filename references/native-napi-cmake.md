# Native Node-API And CMake

Use this reference with `$ark-native` when a HarmonyOS Stage project crosses ArkTS and C++.

## Contract Checklist

| Contract point | Check |
| --- | --- |
| ArkTS import | The module name matches the dependency and packaged native library. |
| Declaration file | `.d.ts` describes the actual exported names, parameters, return shape, and promise behavior. |
| C++ registration | The registered property names match ArkTS callers exactly. |
| CMake target | The target name, source list, include paths, and linked libraries are intentional. |
| Error shape | Native failures are observable to the ArkTS caller. |
| Buffers and strings | Encoding, length, ownership, and ArrayBuffer lifetime are explicit. |
| Async work | Worker and completion phases clean up resources exactly once. |
| License | Third-party source, version, notice, and redistribution terms are recorded. |

## Node-API Async Work

For promise-based native work, account for:

1. Argument validation on the JS thread.
2. Native-owned copies of inputs needed by the worker.
3. Worker-thread restrictions: no UI work and no unsafe access to JS values.
4. Completion behavior for success and failure.
5. Cleanup of async work, deferred state, native buffers, and file handles.
6. Caller-visible behavior when cancellation is impossible.

## CMake And Packaging

Prefer minimal CMake changes. When adding or moving native files, verify the target includes the source file, exported headers, required libraries, and any compiler definitions.

Do not add a third-party native dependency without checking license and redistribution impact. Do not edit generated build output as a substitute for source or build-profile changes.
