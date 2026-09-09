# Migration Acceptance

Load when specifying or checking Android-to-HarmonyOS parity. Use [verification](verification.md) for command provenance and check states; migration progress is separate from a check result.

## Establish An Independent Oracle

Derive expected results from confirmed requirements, service/protocol contracts, manually checked fixtures or validated Android examples. Record which source supports each expectation. Android output is not automatically correct: label characterization separately from intended behavior and flag suspected historical bugs. Never compute expected results using the target implementation itself.

Use the same logical input and controlled conditions on both sides where feasible. Account for normalization, units, encoding, ordering, null/empty values, error codes and agreed numerical tolerances. Native UI need not be pixel-identical; record approved differences in navigation, presentation or platform behavior and verify the preserved user outcome.

## Select Evidence Per Feature

| Surface | Acceptance | Limit |
| --- | --- | --- |
| Business logic / protocol | Independent fixtures cover intended results, relevant failures and boundaries. | Passing examples do not prove all inputs or copied source bugs are correct. |
| UI / async | User flow, pending/error/empty states, repeated actions, stale completion and disposal match the confirmed contract. | Host state tests do not prove rendering or platform lifecycle callbacks. |
| Storage / historical transfer | Formats and durable effects meet the contract; transfer tests cover duplicates, partial failure and recovery when in scope. | Equivalent target schema is not evidence that existing users' data was transferred. |
| Kits / third-party / Native | Actual supported target capability, permissions, loading and failure behavior are observed when required. | Mocks, declarations and a successful package cannot establish device behavior. |

ark-test owns target regression tests; Android execution is separately scoped and not implied by reading source. If the Android build cannot run, continue with available contracts while explicitly naming the missing comparative evidence. If device/runtime acceptance is required but unavailable or excluded, leave the relevant migration item unverified or blocked. Do not install tools or reset devices merely to fill the gap.

## Progress And Completion

| Status | Meaning |
| --- | --- |
| awaiting-analysis | Source behavior, target mapping or prerequisites are not established. |
| awaiting-implementation | The selected contract and target boundary are ready, but code is not complete. |
| implemented-unverified | Implementation exists, but required acceptance evidence is missing or failing. |
| verified | All required criteria for this feature passed against the recorded baseline/environment; approved differences and limitations are explicit. |
| blocked | A concrete missing prerequisite or decision prevents the next required step; retain any implementation evidence already obtained. |

A changed contract/revision invalidates affected verification until checked again. Report feature status alongside the ordinary passed/failed/blocked/not-run/not-applicable check results. Zero tests, wrong variant/target and stale artifacts never establish parity. A feature approved for limited platform support may be verified only within that explicit scope; do not silently shrink acceptance after a failure.

## Report And Recovery

Report source/target revisions and variants, feature IDs, expected/actual outcomes, evidence locations, approved differences, failures, status and the smallest next check. Attribute failures to source behavior, target implementation, tests, environment or unresolved requirements; do not assume every difference is a target defect. Whole-migration completion requires every agreed feature to be verified or explicitly removed from scope by the user, not merely every file translated.

Rerun affected regressions after authorized fixes. Preserve source code and existing target edits. For target source changes use a scoped revert if needed; storage transfer and external actions follow their predeclared recovery plan. No automatic data deletion, production rollout or publication is part of acceptance.
