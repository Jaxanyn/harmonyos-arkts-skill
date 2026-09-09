---
name: ark-test
description: Design, write, diagnose, or review tests for pure-native HarmonyOS Stage / ArkTS projects, including regression tests, deterministic async tests, and risk-ranked whole-project bug discovery. Use for missing tests, ineffective assertions, flaky tests, or project-wide test sweeps; use ark-check for running existing verification alone. Not for FA, Flutter, React Native, web, or backend projects.
---

# Ark Test

Turn a behavior contract into a test that can detect a specific failure. Reuse the project's runner and public boundaries; do not introduce a test platform.

## Choose The Mode

| Request | Mode | Deliverable |
| --- | --- | --- |
| How should this feature be tested? | Plan | Prioritized behaviors, test boundaries, prerequisites, and checks; no edits or execution. |
| Add tests or reproduce a bug | Write | Registered tests, independent expectations, and focused execution evidence. |
| Review tests or diagnose flaky/ineffective tests | Diagnose | Evidence of the test defect and a correction within the requested scope; review alone is read-only. |
| Test the whole project and find bugs | Project sweep | Coverage map, risk-ranked tests, and classified findings; load [project sweep](../references/testing-project-sweep.md). |

A test-writing or project-sweep request permits relevant test additions and focused execution within the existing environment unless the user limits it. It does not by itself authorize production fixes, dependency/config changes, installation, or device resets. Honor read-only and no-execution requests. Reuse existing authorization; do not ask again for an already authorized boundary.

## Workflow

1. Discover project rules, revision/dirty changes, modules, toolchain, test registration, and supported commands. Use [ark-scan](../ark-scan/SKILL.md) if ownership is unknown and [HarmonyOS testing](../references/testing-harmony.md) for environment decisions.
2. Derive the expected behavior from requirements, interface contracts, or independently checked examples. Name the failure each important test should catch. Read [test design](../references/testing-design.md) when writing or reviewing tests. Unclear requirements remain questions, not invented assertions.
3. Select the smallest public boundary that observes the failure. Reuse real production code and replace only necessary external dependencies. Prefer one useful regression over per-function coverage or a new abstraction.
4. Register and run the focused tests when authorized. Control time and completion order; release test resources. For bug fixes, reproduce before fixing when possible. For existing behavior, preserve the implementation and add independent tests; do not delete code to enforce TDD. New test-first work proceeds one behavior at a time.
5. Classify failures before changing anything: product bug, test defect, environment failure, or unclear contract. Route authorized production fixes through [ark-check's failure ownership](../ark-check/SKILL.md). Rerun the affected checks after a fix, then stop when the selected evidence is sufficient.

For migration regressions, take the source contract and selected feature from [ark-migrate](../ark-migrate/SKILL.md) and follow [migration acceptance](../references/migration-acceptance.md). Write tests in the authorized target using independent expectations; do not equate copied Android behavior with correctness or target host tests with cross-platform runtime parity. Source builds/tests require separate execution scope.

## Completion

Report behavior and contract source, chosen boundary, changed test files/registration, actual selected and executed counts, assertion result, and remaining risks. Reuse [verification](../references/verification.md) for commands, provenance and result states; do not maintain a second result vocabulary. Zero tests or template-only success does not verify the target behavior.

Run focused tests directly under this skill; use ark-check for overall verification without rerunning unchanged successful checks. A blocked environment may still allow useful test source or a plan, but report it as unexecuted. Do not claim all bugs are found or full device compatibility from host tests.

Before protected configuration or public-interface changes, follow [shared boundaries](../references/harmony-risk-boundaries.md). Resolve version-sensitive APIs through [official evidence](../references/official-document-evidence.md). No dependency installation, SDK upgrade, production-only test hooks, or broad refactoring merely to make tests easier.
