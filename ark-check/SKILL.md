---
name: ark-check
description: Plan or run risk-proportionate verification for pure-native HarmonyOS Stage-model changes, including tests, builds, packages, installation, device checks, logs, permissions, Native/NDK loading, failure triage, and review evidence.
---

# Ark Check

Build a verification manifest from the changed surface and the project's available tooling. DevEco CLI is evidence collection, not a default side effect.

Read [verification.md](../references/verification.md) to select evidence and result states. First choose plan-only, run-checks, or failure-triage from the user's request. Record revision/dirty diff, affected module, product/target, build mode, and relevant toolchain version. A report about another revision or target is not current evidence.

Use [ark-test](../ark-test/SKILL.md) to design or add tests, diagnose test defects, or organize a whole-project test sweep. Keep existing-check execution here. Reuse current focused results from ark-test when revision, target and environment still match.

## Plan or Run

1. Record every applicable evidence obligation: `local`, `doc-bound`, `config-bound`, and `runtime-bound` are cumulative, not substitutes.
2. Discover supported test, lint, type, LSP, build, package, install, device, and log commands from project configuration and CLI help; do not copy fixed command lines or SDK paths into the skill.
3. Select the smallest sufficient evidence: focused inspection/test, behavior test with failure path, read-only project audit, static native audit, authorized build, or authorized runtime/device check with observable acceptance criteria.
4. Run builds, packages, installs, emulators, device commands, log streams, or native loading checks only within authorized verification scope. Existing explicit authorization is sufficient; do not ask again for the same action. Discover commands first and inspect their side effects. No dependency installation, SDK upgrade, signing replacement, uninstall, or device-data reset merely to make a check pass.
5. State every intentional gap as an unverified runtime risk.

## Optional Device CLI

When `ark-device` is available, follow [device CLI integration](../references/device-cli.md) for signed-HAP installation, launch and bounded logs. It is optional: use discovered project/HDC commands when absent. Do not install it automatically or treat tool-operation success as application acceptance. Reuse the user's existing execution authorization.

## Failure Routing

When tools fail to start or IDE and terminal results differ, read [build-environment.md](../references/build-environment.md) before attributing the failure to source code. Compare command provenance, actual tools and intended targets; distinguish environment, configuration, dependency resolution, source and test failures.

When evidence fails, do not patch blindly. Route the failure to the command that owns the broken contract:

| Failure signal | Route to | Reason |
| --- | --- | --- |
| Tool startup failure, IDE/terminal mismatch, or dependency resolution error before compilation | Environment diagnosis in this skill; ark-scan if ownership is unknown | Establish the actual executable, intended target and first cause before routing a configuration or source fix. |
| Missing/unregistered cases, ineffective assertions, test doubles, isolation, or test timing defects | `$ark-test` | Repair test evidence; do not assume a failing test proves a production defect. |
| ArkTS syntax, typing, generic, import-form, or language-version diagnostic | `$ark-language` | Identify the applicable compiler constraint and source boundary before adapting code. |
| Render, navigation, decorator, lifecycle, listener, timer, controller, or stale UI completion | `$ark-ui` | The state/lifecycle ledger is incomplete or wrong. |
| Loading, cache, parser, DTO, repository, service, persistence, stale request, or error-state issue | `$ark-flow` | The async contract is incomplete or wrong. |
| Permission, API level, Kit behavior, module declaration, dependency, or device capability | `$ark-kit` | The capability contract or official constraint is incomplete or wrong. |
| C/C++, Node-API, `.d.ts`, CMake, ABI, shared-library loading, native thread, memory, or third-party native dependency | `$ark-native` | The native contract is incomplete or wrong. |
| Unknown owner, unexpected file boundary, public library boundary, or unsafe config implication | `$ark-scan` | The project change map is incomplete or wrong. |

For migration, use [migration acceptance](../references/migration-acceptance.md) and return feature-level evidence to [ark-migrate](../ark-migrate/SKILL.md). Record both baselines and variants/targets, approved differences and missing comparative evidence. Target build success alone does not make a migrated feature verified.

## Deliver: Verification Manifest

| Changed surface | Evidence profile | Acceptance criterion | Discovered project command/check | Authorization needed | Result or remaining risk |
| --- | --- | --- | --- | --- | --- |

For each executed check, record sanitized command, working directory, target, exit code, actual assertion/test result, and evidence location. Use `passed`, `failed`, `blocked`, `not-run`, or `not-applicable`; qualify a pass when its environment is limited. An empty test selection, grepped symbol, successful package, or browser approximation is not a runtime behavior pass.

For failures, keep the first actionable diagnostic and route by the table above. Distinguish an existing baseline failure from a regression; if the baseline cannot be checked, say attribution is unknown. Fix only within the authorized implementation scope. After a fix, rerun the failing check and affected regression checks; stop when evidence is sufficient. Do not repeatedly rebuild an unchanged failure or make unrelated configuration edits.

Completion requires every changed surface to have evidence or a named unverified boundary. If required acceptance remains blocked, report the change as implemented but not fully verified, with the smallest concrete next check. Bound log capture by time and filter; stop processes started for this check and redact credentials, private paths, and device identifiers from shared output.

The optional [project scanner](../scripts/audit_harmony_project.py) inventories boundaries but cannot certify a build. For native verification read [native-napi-cmake.md](../references/native-napi-cmake.md). When publishing changes to Ark itself, run the [privacy scanner](../scripts/check_skill_privacy.py) and the package checks described in [skill-scenarios.md](../tests/skill-scenarios.md). Resolve helper paths relative to the installed skill, never the application working directory.

For documentation-backed claims use [official-document-evidence.md](../references/official-document-evidence.md) and preserve the distinction between documented, compiler-observed, and runtime-observed evidence. Respect an explicit exclusion of testing or acceptance: do not run those checks, and mark the affected results `not-run` rather than passed.

## Run A Project On A Device

For an Agent-driven project build, device launch and log diagnosis, follow [project-to-device workflow](../references/project-device-workflow.md). Choose current-source build, supplied HAP, or installed-app retest explicitly; reuse ark-scan, ark-check and the optional CLI instead of inventing another device implementation.

For offline business execution, follow [offline business acceptance](../references/offline-business-acceptance.md). Preserve network-state provenance and report each business assertion separately from deployment and SDK log verdicts.
