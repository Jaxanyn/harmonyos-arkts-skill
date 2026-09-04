---
name: ark
description: Route pure-native HarmonyOS Stage-model app changes through project inspection, official-document evidence, safe implementation boundaries, Native/NDK handling, and risk-proportionate verification. Use when broad ArkTS tasks need scanning, ArkUI changes, async flow coordination, system Kit integration, native code changes, or verification. Do not use for Flutter, React Native, web, backend, non-HarmonyOS, or non-Stage-model projects.
---

# Ark

Route HarmonyOS / ArkTS work to the smallest command. This skill is the control layer: the target project supplies local facts, official documentation supplies platform facts, and discovered DevEco or project commands supply execution evidence.

Use this for general pure-native HarmonyOS app development. Do not specialize the workflow for one company, product, industry, local machine, dataset, certificate, or device.

## Evidence Profile

Assign each task the highest evidence level that affects the decision:

| Profile | Use when | Required action |
| --- | --- | --- |
| `local` | Pure ArkTS/UI/resource change inside known boundaries. | Inspect the current project path and produce the changed boundary. |
| `doc-bound` | Platform API, Kit, permission, API level, error code, lifecycle semantics, or compatibility matters. | Use the official-document lookup and record the constraint that changes the decision. |
| `config-bound` | `module.json5`, SDK, dependency, native build, signing, package identity, lockfile, build tooling, HAR/HSP/HAP boundary, or public library surface may change. | Show the smallest config or public-interface diff and ask for explicit approval before editing. |
| `runtime-bound` | Build, package, install, emulator/device, external service, logs, location, rendering, native loading, or hardware capability must be observed. | Discover the project command/check first; run only the user-authorized scope and report the exact result. |

Do not copy platform API catalogs, fixed SDK paths, device identifiers, certificates, customer data, product-domain rules, or static DevEco command lines into this skill. The project, official docs, and current environment are the sources of truth.

## Commands

| Command | Use when | Required deliverable |
| --- | --- | --- |
| `$ark-scan` | Scope, ownership, evidence profile, project shape, or safety boundary is unclear. | Project change map and safe next command. |
| `$ark-ui` | ArkUI page, component, state, navigation, lifecycle, controller, listener, or layout behavior changes. | State/lifecycle ledger and changed UI boundary. |
| `$ark-flow` | ViewModel, service, repository, DTO, cache, loading, parser, persistence, or async coordination changes. | Async contract from user action to data source. |
| `$ark-kit` | Permission, file, storage, network, WebView, MapKit, location, notification, Bluetooth, media, or other system capability changes. | Capability contract with official constraint and failure behavior. |
| `$ark-native` | Node-API, C/C++, CMake, ABI, shared library, `.d.ts`, native async work, native rendering, or third-party native library changes. | Native contract across ArkTS, declarations, C++, build, and runtime loading. |
| `$ark-check` | Tests, builds, packaging, installation, device checks, logs, review evidence, or failure triage is requested. | Verification manifest with evidence, failures, and remaining risk. |

## Reference Navigation

Child skills load shared references only when their branch needs them:

- `$ark-scan` reads [project-shape.md](references/project-shape.md) and [harmony-risk-boundaries.md](references/harmony-risk-boundaries.md) for unfamiliar project shape or protected surfaces.
- `$ark-ui` reads [arkui-and-architecture.md](references/arkui-and-architecture.md) when state ownership crosses component, page, and service boundaries.
- `$ark-kit` reads [platform-capabilities.md](references/platform-capabilities.md) when permissions, storage, I/O, or hardware-facing APIs matter.
- `$ark-native` reads [native-napi-cmake.md](references/native-napi-cmake.md) when ArkTS crosses into C/C++, Node-API, CMake, ABI, or shared-library loading.
- `$ark-check` reads [verification.md](references/verification.md) when evidence spans multiple surfaces or runtime boundaries.

## Routing Rules

1. Start with `$ark-scan` when affected files, module ownership, call path, evidence profile, project type, or protected configuration are unknown.
2. Use `$ark-ui` for local UI/state/lifecycle work; add `$ark-flow` when data or business coordination crosses the component boundary.
3. Use `$ark-kit` for platform capabilities, permissions, system APIs, and configuration implications.
4. Use `$ark-native` when any ArkTS change crosses into `.d.ts`, C/C++, CMake, ABI, shared-library loading, or native third-party code.
5. Finish every non-trivial authorized change with `$ark-check`.
6. When `$ark-check` fails, route by the failing evidence: UI/lifecycle to `$ark-ui`, async/data to `$ark-flow`, platform/config/device to `$ark-kit`, native/build/loading to `$ark-native`, unknown ownership to `$ark-scan`.

## Approval Boundaries

Require explicit user approval before editing signing, certificates, package identity, SDK compatibility, dependencies, lockfiles, permissions, native build surfaces, generated output, device state, production constants, or public HAR/HSP/HAP interfaces.

Read [harmony-risk-boundaries.md](references/harmony-risk-boundaries.md) when a change may cross configuration, packaging, external storage, device, native, or user-data boundaries.

## Shared Boundary

Preserve the project's existing module, page, ViewModel, service, adapter, repository, resource, logging, error-presentation, and test boundaries. Prefer the official API and the project's compatible existing pattern. Keep reusable workflow guidance here; keep credentials, certificates, local paths, device identifiers, customer data, and product-domain rules in the target project.
