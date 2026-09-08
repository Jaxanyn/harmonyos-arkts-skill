---
name: ark-check
description: Plan or run risk-proportionate verification for pure-native HarmonyOS Stage-model changes, including tests, builds, packages, installation, device checks, logs, permissions, Native/NDK loading, failure triage, and review evidence.
---

# Ark Check

Build a verification manifest from the changed surface and the project's available tooling. DevEco CLI is evidence collection, not a default side effect.

Read [verification.md](../references/verification.md) to select evidence and result states. First choose plan-only, run-checks, or failure-triage from the user's request. Record revision/dirty diff, affected module, product/target, build mode, and relevant toolchain version. A report about another revision or target is not current evidence.

## Plan or Run

1. Record every applicable evidence obligation: `local`, `doc-bound`, `config-bound`, and `runtime-bound` are cumulative, not substitutes.
2. Discover supported test, lint, type, LSP, build, package, install, device, and log commands from project configuration and CLI help; do not copy fixed command lines or SDK paths into the skill.
3. Select the smallest sufficient evidence: focused inspection/test, behavior test with failure path, read-only project audit, static native audit, authorized build, or authorized runtime/device check with observable acceptance criteria.
4. Run builds, packages, installs, emulators, device commands, log streams, or native loading checks only within authorized verification scope. Existing explicit authorization is sufficient; do not ask again for the same action. Discover commands first and inspect their side effects. No dependency installation, SDK upgrade, signing replacement, uninstall, or device-data reset merely to make a check pass.
5. State every intentional gap as an unverified runtime risk.

## Failure Routing

When evidence fails, do not patch blindly. Route the failure to the command that owns the broken contract:

| Failure signal | Route to | Reason |
| --- | --- | --- |
| ArkTS syntax, typing, generic, import-form, or language-version diagnostic | `$ark-language` | Identify the applicable compiler constraint and source boundary before adapting code. |
| Render, navigation, decorator, lifecycle, listener, timer, controller, or stale UI completion | `$ark-ui` | The state/lifecycle ledger is incomplete or wrong. |
| Loading, cache, parser, DTO, repository, service, persistence, stale request, or error-state issue | `$ark-flow` | The async contract is incomplete or wrong. |
| Permission, API level, Kit behavior, module declaration, dependency, or device capability | `$ark-kit` | The capability contract or official constraint is incomplete or wrong. |
| C/C++, Node-API, `.d.ts`, CMake, ABI, shared-library loading, native thread, memory, or third-party native dependency | `$ark-native` | The native contract is incomplete or wrong. |
| Unknown owner, unexpected file boundary, public library boundary, or unsafe config implication | `$ark-scan` | The project change map is incomplete or wrong. |

## Deliver: Verification Manifest

| Changed surface | Evidence profile | Acceptance criterion | Discovered project command/check | Authorization needed | Result or remaining risk |
| --- | --- | --- | --- | --- | --- |

For each executed check, record sanitized command, working directory, target, exit code, actual assertion/test result, and evidence location. Use `passed`, `failed`, `blocked`, `not-run`, or `not-applicable`; qualify a pass when its environment is limited. An empty test selection, grepped symbol, successful package, or browser approximation is not a runtime behavior pass.

For failures, keep the first actionable diagnostic and route by the table above. Distinguish an existing baseline failure from a regression; if the baseline cannot be checked, say attribution is unknown. Fix only within the authorized implementation scope. After a fix, rerun the failing check and affected regression checks; stop when evidence is sufficient. Do not repeatedly rebuild an unchanged failure or make unrelated configuration edits.

Completion requires every changed surface to have evidence or a named unverified boundary. If required acceptance remains blocked, report the change as implemented but not fully verified, with the smallest concrete next check. Bound log capture by time and filter; stop processes started for this check and redact credentials, private paths, and device identifiers from shared output.

The optional [project scanner](../scripts/audit_harmony_project.py) inventories boundaries but cannot certify a build. For native verification read [native-napi-cmake.md](../references/native-napi-cmake.md). When publishing changes to Ark itself, run the [privacy scanner](../scripts/check_skill_privacy.py) and the package checks described in [skill-scenarios.md](../tests/skill-scenarios.md). Resolve helper paths relative to the installed skill, never the application working directory.

For documentation-backed claims use [official-document-evidence.md](../references/official-document-evidence.md) and preserve the distinction between documented, compiler-observed, and runtime-observed evidence. Respect an explicit exclusion of testing or acceptance: do not run those checks, and mark the affected results `not-run` rather than passed.
