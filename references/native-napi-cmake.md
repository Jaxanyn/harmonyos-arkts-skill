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

## Partial Failure And Teardown

For each allocation or registration, record the success owner and the failure cleanup path. Check argument extraction, buffer creation, promise creation, async-work creation, and queue submission before using outputs. Review the actual SDK status/exception contract instead of assuming calls cannot fail. Do not resolve a deferred twice or continue building a result after an unhandled pending exception.

| Path | Required reasoning |
| --- | --- |
| Input rejected | No work queued; caller receives the established error shape. |
| Work creation or queueing fails | Dispose only resources that were created, settle the caller if the environment permits, and retain no orphan work context. |
| Worker fails | Carry native error data to completion; do not use JS objects from the worker. |
| Cancellation or page exit | Distinguish requested cancellation, actual worker termination, and stale-result suppression. Resources remain owned until work really ends. |
| Environment teardown | Identify cleanup hook/callback lifetime and prohibit callbacks into a dead environment; verify the API available in the selected SDK. |

Input sizes and allocation arithmetic need explicit bounds at untrusted boundaries. State string encoding and byte length, buffer copy/borrow/transfer semantics, and integer precision. Never return pointers into temporary storage. Keep cross-thread ownership explicit, and use the project's synchronization strategy for shared mutable data.

## Native Rendering (Only When Affected)

Locate the XComponent/surface callbacks and their owner. Follow create, resize, hide/show where applicable, destroy, and recreate; account for queued frames arriving after destruction. Record the thread owning the graphics context/window, cancellation of render work, callback detachment, and release order. A source-only lifecycle review cannot prove GPU/context behavior. Measure frame time and memory on an authorized target before claiming performance improvement.

## Verification Ladder

Check caller/declaration/export agreement first. Build and link the selected module/product/ABI with the discovered toolchain next when authorized. Inspect the generated package's actual libraries and dependencies, then test loading and a valid/invalid call on the intended runtime. Include repeated calls or teardown while work is pending when ownership changed. A library filename or successful host C++ compilation does not prove target ABI or runtime compatibility.

Record third-party provenance and license evidence from the dependency itself. If redistribution terms are unclear, flag the missing decision before adding or shipping that dependency; do not infer legal compatibility from a repository being public.

## Official Evidence

Use Huawei's [Node-API asynchronous task guide](https://developer.huawei.com/consumer/cn/doc/doccenter-capabilities/use-napi-asynchronous-task) as a lookup entry point. Select the documentation matching the project's SDK and check the installed declarations for each used symbol. This reference describes workflow obligations rather than a fixed API-version catalog.
