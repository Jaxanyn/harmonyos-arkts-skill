---
name: ark-language
description: Write or adapt ArkTS in HarmonyOS Stage projects and diagnose ArkTS syntax, typing, import, or decorator compilation errors. Use for TypeScript-to-ArkTS adaptation and SDK-dependent language constraints. Route runtime UI behavior to ark-ui and native export or ABI issues to ark-native.
---

# Ark Language

Make the requested source change compatible with the project's actual ArkTS toolchain while preserving its behavior and public contracts. This skill handles language adaptation, not a whole Android migration or a forced SDK upgrade.

## Establish The Applicable Rules

1. Identify the affected module and source kind: application `.ets`, TS/JS interoperability, declarations, or build-tool TypeScript. Do not apply application ArkTS restrictions to every `.ts` file, including Hvigor configuration.
2. Read configured SDK fields and the actual compiler/IDE diagnostic if supplied. Keep HarmonyOS versus OpenHarmony, Stage versus FA, ArkTS language/toolchain version, and ArkUI state-management V1/V2 as distinct facts. Use `$ark-scan` only when these boundaries are unknown.
3. Choose diagnosis, source generation, or adaptation from the user's request. For diagnosis, explain the smallest evidenced cause before proposing a fix; do not implement unless authorized. For adaptation, identify callers, external inputs, and observable behavior that must remain compatible.
4. Read [official-document evidence](../references/official-document-evidence.md) for version-sensitive claims. Read [language adaptation](../references/arkts-language-adaptation.md) for types, imports, external data, and decorator boundaries. Use the project's compatible existing pattern where one exists.
5. If compiler output or version evidence is missing, label the suspected restriction as unverified. Do not invent a diagnostic, assume the latest SDK, or turn an example from one release into a universal syntax ban.

## Make The Smallest Correct Adaptation

- Fix the first relevant diagnostic and its underlying type or module boundary before chasing likely cascading errors. Preserve nullability, return/error behavior, property names used in serialization, object identity, and public callers.
- Replace unsupported dynamic constructs with explicit types and a compatible data representation when required by the target compiler. Do not hide a mismatch using suppression comments, broad casts, unchecked assertions, or a move to `.ts` merely to escape checking.
- Treat deserialization, JS interoperability, native results, and storage reads as data boundaries. A declared type or cast does not validate input at runtime. Use the existing adapter to check required fields and represent missing or invalid data deliberately.
- Check imports against the actual package exports and SDK declarations. Do not globally rewrite import syntax or add a dependency based on a rule from another language/SDK version. Native declaration/export mismatches belong to `$ark-native`; platform availability and permissions belong to `$ark-kit`.
- For decorator errors, identify the affected component/model's generation, owner, and update path. A compiler fix must preserve state propagation; route behavioral or lifecycle changes to `$ark-ui`. Do not mechanically replace V1 decorators with similarly named V2 decorators.

## Deliver

Report the source kind and toolchain evidence, diagnostic or unsupported construct, official constraint and version, changed boundary, preserved behavior, and remaining uncertainty. Use [verification](../references/verification.md) through `$ark-check` when verification is authorized: ordinary TypeScript checks are not proof of ArkTS compilation. If the user excludes tests/builds, deliver the source changes and explicitly state that compilation and behavior remain unverified. Keep verification exclusions intact; do not make a successful build a claim based on inspection.

Resolve sibling skills and references from the installed package. No extra account, fixed SDK path, or new language runtime is required by this skill.
