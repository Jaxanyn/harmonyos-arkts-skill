# ArkTS Language Adaptation

Use this reference with `$ark-language` for generation, compiler-error diagnosis, or a scoped TS-to-ArkTS change. It is a decision guide, not a version-independent list of prohibited TypeScript syntax. For exact restrictions follow [official-document evidence](official-document-evidence.md).

## Separate The Axes

| Axis | Evidence to inspect | Avoid assuming |
| --- | --- | --- |
| Application model | Affected module declarations and build configuration. | Every repository containing `.ets` is entirely Stage. |
| Language/toolchain | Actual diagnostics, SDK selection, build configuration and source extension. | ArkUI V2 means ArkTS language version 2. |
| State management | Affected component/model decorators, ownership and caller usage. | One V2 example makes all V1 files obsolete. |
| Source role | Application code, SDK/package declaration, TS/JS adapter, build script. | Restrictions for `.ets` apply unchanged to build-tool TypeScript. |
| Runtime capability | Device/system capability, permission and lifecycle conditions. | A symbol compiling means it is usable on every supported device. |

## Types And External Data

When the compiler rejects `any`, `unknown`, an object literal, an index signature, a generic, or another dynamic construct, locate its real data shape and the applicable diagnostic before choosing a replacement. Prefer an existing domain type or explicit interface/class; choose a map/record representation only when keys are genuinely dynamic and supported by the selected compiler. Do not invent a class for every object without a semantic reason.

At JSON, network, file, storage, or interoperability boundaries, preserve missing fields, nulls, invalid values, and errors intentionally. Validate external data in the existing adapter and map it to the internal shape. A type annotation after parsing is not validation, and an unchecked cast can hide a failure rather than fix it. Do not assume arbitrary helper syntax from standard TypeScript is accepted by the target ArkTS compiler.

When replacing spread, destructuring, dynamic indexing, constructor shorthand, or metaprogramming that the target rejects, account for evaluation order, defaults, mutation, copying, getters, prototype assumptions, and property enumeration. A syntactically acceptable rewrite that changes those behaviors is not equivalent adaptation. Limit changes to the requested call path.

## Imports And Public Boundaries

Resolve an import to the project's actual module/package export and declaration. Check the allowed import form for the current source kind and toolchain; avoid blanket conversions of type imports, re-exports, or extensions. Existing use of `@kit` and legacy module imports is a compatibility fact to inspect, not permission to normalize the whole project.

For TS/JS interop, distinguish what the bridge permits from what application `.ets` code permits. Do not move arbitrary application logic into a JavaScript escape hatch to satisfy the compiler. For a HAR/HSP export, preserve consumer-visible names, optionality, serialized shapes, and async/error behavior; route the affected consumers through the existing library boundary review. For Native declarations, verify exports with `$ark-native`.

## Decorators And Declarative UI

Inspect each decorator's allowed owner, value type, initialization, update direction, and lifetime against the affected component's state-management generation. A type-correct object does not by itself prove nested changes will be observed. Record the update path when adapting a model or array used by UI.

Separate ordinary ArkTS statements from declarative `build`/builder content when diagnosing a UI DSL error. Avoid moving side effects into rendering to make a construct fit. Delegate navigation, rendering behavior, listener cleanup, and cross-component state decisions to `$ark-ui`; language-only changes should not trigger a state-system migration.

## Diagnostic Loop

Capture the first relevant diagnostic and its location without including sensitive data. Distinguish language syntax/type errors from missing imports, platform API incompatibility, generated-code errors, and Native declaration mismatches. Trace consumers if a type change explains multiple errors. Preserve the project's error contract and external input behavior in the proposed change.

When compilation is authorized, use the discovered ArkTS diagnostic/build command for the affected target. When tests or builds are excluded, stop after the authorized source edit and state the unresolved compilation/runtime evidence. Do not fabricate compiler output, silence checks, or update SDK/dependencies as an implicit workaround.
