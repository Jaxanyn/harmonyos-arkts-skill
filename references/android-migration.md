# Android Source To HarmonyOS Target

Load for source analysis and migration decisions. Read Android sources; write only to the authorized target. This guide does not declare platform APIs interchangeable.

## Source Discovery

Inspect applicable project rules and decisions, Gradle modules/variants and source sets, manifests, Kotlin/Java, XML/Compose, navigation and entrypoints. Trace the selected feature through Activity/Fragment or composable UI, state owners, services/repositories, DTOs, networking, storage, background work and Native calls. Follow actual dependencies rather than assuming a particular Android architecture. Generated code, demos and unused variants do not establish production behavior.

Record relevant permissions, resources, third-party SDKs, C/C++ sources and JNI/Android-specific dependencies. Inspect only task-relevant configuration and never dump secrets. Existing tests describe intended or historical behavior; inspect their assertions and execution provenance. Without runnable Android evidence, label behavioral conclusions as source/test-derived rather than runtime-observed.

## Migration Ledger

Use stable feature identifiers within the project so implementation and acceptance refer to the same contract. Keep strategy separate from progress status.

| Feature / source location | Contract and evidence | Strategy and rationale | Target owner / files | Dependencies, differences and acceptance | Status |
| --- | --- | --- | --- | --- | --- |

Strategies are reuse, rewrite, replacement, needs-confirmation, or blocked. Reuse requires checking portability and permission to reuse the resource or dependency; an existing binary or platform-bound library is not portable by name alone. Rewrite preserves confirmed behavior in native target patterns. Replacement requires evidence that an alternative meets the needed subset and compatibility constraints. Needs-confirmation means a product decision is missing; blocked means a concrete prerequisite prevents progress.

Statuses are awaiting-analysis, awaiting-implementation, implemented-unverified, verified, or blocked. Follow [acceptance](migration-acceptance.md) before marking verified. Unknown target paths or APIs remain explicit gaps; resolve them before handing that item off as implementation-ready.

## Contracts Before Mapping

For each slice specify trigger, inputs, outputs, state, error/empty behavior, navigation results and persistent effects. Inspect async ordering, cancellation, lifecycle ownership, threading, numeric ranges, null handling and serialization where they affect semantics; replacing Kotlin/Java syntax with ArkTS does not preserve these automatically.

Keep domain rules and service protocols where valid. Map UI and lifecycle by behavior rather than class names; do not equate Activity, Fragment or Compose constructs with target components. Separate portable native algorithms from JNI bindings and Android APIs before routing to ark-native. Verify permissions, background behavior and service availability against target SDK documentation.

Record each third-party dependency's required features, target support evidence, alternative, capability differences, configuration prerequisites and usage conditions. Unknown availability stays unknown. Never use a no-op, mock or sample service as a completed production replacement. Continue independent slices while a required capability is blocked.

## Data And Configuration

Implementing equivalent storage is different from transferring existing users' data. Historical data transfer is a separate authorized scope: establish export/import or sync channel, versioned format, field/encoding semantics, identity mapping, duplicates/conflicts, partial failure, restart and recovery. Do not assume direct access to the source app's sandbox. Use disposable fixtures for tests; never overwrite or clear durable data to make acceptance pass.

Do not copy source signing, credentials, production service settings or app identity into the target. Identify the required binding without exposing values. Target code changes can be reverted as a scoped patch; data or external-state changes need a recovery plan before execution. Preserve unrelated dirty files and do not reset either repository.

## Handoff And Drift

Pick one complete user flow with independently testable acceptance. Supply the source evidence, target baseline, exact target boundary, replacement decisions and authorization to the owning Ark skill. Existing target implementations take precedence over inventing parallel layers. If source evidence contradicts requirements, surface the conflict rather than copying a historical defect.

After either side changes, revisit only affected contracts, mappings and tests. A previous pass against another revision or build variant is historical evidence. Reuse existing project tracking or a requested target-side ledger; no mandatory migration database, generated report system or new runtime is needed.
