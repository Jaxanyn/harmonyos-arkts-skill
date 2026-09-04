---
name: ark-check
description: Plan or run risk-proportionate verification for pure-native HarmonyOS Stage-model changes, including tests, builds, packages, installation, device checks, logs, permissions, Native/NDK loading, failure triage, and review evidence.
---

# Ark Check

Build a verification manifest from the changed surface and the project's available tooling. DevEco CLI is evidence collection, not a default side effect.

## Plan or Run

1. Classify each changed surface by evidence profile: `local`, `doc-bound`, `config-bound`, or `runtime-bound`.
2. Discover supported test, lint, type, LSP, build, package, install, device, and log commands from project configuration and CLI help; do not copy fixed command lines or SDK paths into the skill.
3. Select the smallest sufficient evidence: focused inspection/test, behavior test with failure path, static native audit, authorized build, or authorized runtime/device check with observable acceptance criteria.
4. Run builds, packages, installs, emulators, device commands, log streams, or native loading checks only when the user requested that verification scope. Record the exact command/check and result.
5. State every intentional gap as an unverified runtime risk.

## Failure Routing

When evidence fails, do not patch blindly. Route the failure to the command that owns the broken contract:

| Failure signal | Route to | Reason |
| --- | --- | --- |
| Render, navigation, decorator, lifecycle, listener, timer, controller, or stale UI completion | `$ark-ui` | The state/lifecycle ledger is incomplete or wrong. |
| Loading, cache, parser, DTO, repository, service, persistence, stale request, or error-state issue | `$ark-flow` | The async contract is incomplete or wrong. |
| Permission, API level, Kit behavior, module declaration, dependency, or device capability | `$ark-kit` | The capability contract or official constraint is incomplete or wrong. |
| C/C++, Node-API, `.d.ts`, CMake, ABI, shared-library loading, native thread, memory, or third-party native dependency | `$ark-native` | The native contract is incomplete or wrong. |
| Unknown owner, unexpected file boundary, public library boundary, or unsafe config implication | `$ark-scan` | The project change map is incomplete or wrong. |

## Deliver: Verification Manifest

| Changed surface | Evidence profile | Acceptance criterion | Discovered project command/check | Authorization needed | Result or remaining risk |
| --- | --- | --- | --- | --- | --- |

Completion requires every changed surface to have evidence or a named unverified boundary. Read [verification.md](../references/verification.md) when selecting evidence for a mixed-surface change. Read [native-napi-cmake.md](../references/native-napi-cmake.md) when native verification is in scope.
