---
name: ark-migrate
description: Plan or implement native Android Kotlin/Java application migration into a native HarmonyOS Stage / ArkTS project. Use for Android source analysis, feature mapping, platform dependency replacement and cross-platform acceptance. Android is a read-only source by default; this is not general Android development, APK decompilation, Flutter/React Native migration, or automatic source translation.
---

# Ark Migrate

Coordinate a migration by user-visible behavior. Keep implementation ownership in the existing Ark skills and maintain one migration ledger, not a second development framework.

## Mode And Boundaries

Choose analysis/plan or implementation from the request. Analysis produces a feature map, migration decisions and acceptance criteria without edits or builds. Implementation changes only the authorized HarmonyOS target and selected feature slices. Android source remains read-only unless separately authorized; source builds/tests may generate files and require execution scope, even when application source is unchanged.

Record source and target roots, revisions/dirty files, source build variant, target module/product/SDK, requested features and permitted execution. Reuse supplied information. Resolve missing or overlapping roots before any write; in a monorepo identify separate owned subtrees. Do not run target edits from the source working directory. Preserve existing source and target changes.

If no target exists, establish its location, SDK, application identity and supported initialization method before creating it. Do not invent project configuration, sign an app or overwrite a target. Reuse [shared boundaries](../references/harmony-risk-boundaries.md) for configuration, dependencies, data and execution; existing concrete authorization remains valid.

## Five-Step Workflow

1. Read applicable rules and decisions for both projects. Use [Android migration](../references/android-migration.md) to trace a selected user journey through Android UI, business logic, data and platform dependencies. Distinguish source inference, existing test evidence and observed runtime behavior. An unavailable Android runtime does not block independent source analysis.
2. Build the migration ledger from feature contracts and evidence. Classify reuse, rewrite, replacement, needs-confirmation or blocked. Validate version-sensitive replacement claims with [official evidence](../references/official-document-evidence.md); Android rules need matching official Android sources, and HarmonyOS rules need matching target documentation. Do not assume one-to-one API equivalence.
3. Select a bounded, independently verifiable feature slice spanning UI, logic, data and errors. Prefer clear contracts and few unresolved platform dependencies. Record intentional behavior differences; do not reproduce a suspected source bug as the target requirement or silently redesign the product.
4. Inspect the target with [ark-scan](../ark-scan/SKILL.md), then hand off to the owners below. Supply target files, source evidence, contract, authorized scope and acceptance cases. Reuse the target architecture; no wholesale folder translation, compatibility layer or speculative framework.
5. Use [migration acceptance](../references/migration-acceptance.md) with ark-test and ark-check. Update status from evidence, preserve blockers, and report the next feature boundary. Implemented code is not an accepted migration; a build is not behavioral parity.

## Implementation Owners

| Work | Owner |
| --- | --- |
| Target structure and safe edit scope | [ark-scan](../ark-scan/SKILL.md) |
| ArkTS types, imports and compiler constraints | [ark-language](../ark-language/SKILL.md) |
| UI, navigation, state and lifecycle | [ark-ui](../ark-ui/SKILL.md) |
| Business rules, APIs, persistence and async coordination | [ark-flow](../ark-flow/SKILL.md) |
| Permissions, platform services and third-party alternatives | [ark-kit](../ark-kit/SKILL.md) |
| C/C++, JNI dependencies and target cross-language adaptation | [ark-native](../ark-native/SKILL.md) |
| Regression cases and aggregate evidence | [ark-test](../ark-test/SKILL.md), [ark-check](../ark-check/SKILL.md) |

Keep this skill's Android exception limited to source analysis for migration. Other skills operate on the HarmonyOS target. No APK reverse engineering, automatic publishing, or claim that existing user data can be read from the Android sandbox.

## Deliver

Report source/target baselines, selected feature map, ledger, approved differences, implemented target files, evidence and remaining blockers. Reuse an existing project document when durable tracking is requested; otherwise respond inline. Refresh affected ledger items after source/target drift rather than restarting the entire analysis. Never promote project credentials, service addresses, certificates or proprietary behavior into this reusable skill.
