# Official Document Evidence

Read this reference when a platform API, language restriction, decorator, permission, lifecycle, threading rule, error code, or compatibility fact changes a decision. Pure project-local edits with no changed platform assumption do not need a new documentation search.

## Frame The Question

Record the affected module, product/target, configured compile/target/compatible SDK fields, platform distribution, source kind, and exact symbol or diagnostic. Treat state-management generation separately from language/toolchain version. Ask a narrow question such as whether a specific overload is supported on the project's minimum supported target, rather than requesting a generic API tutorial.

For queries sent outside the machine, use public API names, diagnostic codes, and a reduced synthetic example. Do not upload proprietary source, whole logs, signing configuration, device identifiers, or customer data merely to retrieve documentation.

## Lookup And Cross-Check

1. Discover an already configured official-document connector or MCP. Use it when available; record the actual document identity, not just the tool name. Do not assume a named MCP exists or silently install/configure one.
2. Otherwise use Huawei's official developer documentation for HarmonyOS. Select the product, language, release/API context, and application type appropriate to the project. OpenHarmony documentation may clarify shared foundations, but does not establish availability of Huawei-specific Kits or services.
3. Inspect the installed SDK declarations and relevant release/migration notes when signatures, deprecation, annotations, or compiler behavior matter. Declarations show what the selected toolchain exposes; they do not alone prove runtime availability, permission grants, or lifecycle semantics.
4. Use third-party examples only as implementation leads. Verify decisive restrictions against official references. Search snippets, a community post hosted on an official domain, a local documentation mirror without version metadata, and an AI summary are not equivalent to the official API reference.
5. Reuse verified evidence during the same task while its version, symbol, and affected boundary remain unchanged. Refresh it after an SDK/product change, a conflicting diagnostic, or a move to another API variant. Avoid storing a large unversioned API catalog in this package.

## Evidence Record

Keep a compact record in the task response or existing project decision record when requested; do not create a new permanent file for every lookup.

| Field | What to capture |
| --- | --- |
| Question | Exact symbol, overload, decorator, or diagnostic being resolved. |
| Project context | Relevant SDK fields, target and source kind; unknown fields remain unknown. |
| Source | Official title/URL or connector document ID; local SDK relative file and symbol when used. |
| Applicability | Release/API context and relevant app/device/system capability or permission conditions. |
| Decision | The specific code/configuration choice affected; separate quotation/fact from inference. |
| Freshness and limits | Retrieval date, conflicts, inaccessible sections, and unobserved runtime behavior. |

For capability work distinguish API introduction, compatibility floor, compile-time presence, runtime device support, permission declaration, and actual authorization. A documented replacement may have a higher minimum API level; do not adopt it without checking supported targets.

## Conflict And Failure Handling

If docs and the actual compiler disagree, preserve the exact diagnostic and compare SDK selection, overload, app type, imports, and documentation version first. Do not increase the SDK, rewrite public interfaces, suppress diagnostics, or invent a compatibility API to reconcile the disagreement.

If a connector fails, fall back to official web documentation and available local SDK evidence. If the network is unavailable, use local evidence with its limits and leave unverifiable semantics open. Continue independent local work, but do not implement a change whose correctness depends on an unresolved platform premise. Report the exact missing fact and the smallest way to obtain it. Existing user authorization governs configuration or runtime actions; lookup availability does not broaden that authority.

## Official Entry Points

These are discovery links, not fixed compatibility guarantees. Follow the version relevant to the target project and record the source actually used.

- [ArkTS adaptation background](https://developer.huawei.com/consumer/cn/doc/doccenter-getting-started/arkts-migration-background): why TypeScript compatibility requires explicit language-rule checks.
- [ArkTS adaptation cases](https://developer.huawei.com/consumer/cn/doc/doccenter-getting-started/arkts-more-cases): diagnostic-led examples; verify their SDK applicability before applying them.
- [ArkUI state management](https://developer.huawei.com/consumer/cn/doc/doccenter-capabilities/arkts-state-management): V1/V2 concepts and migration guidance.
- [Native async tasks](https://developer.huawei.com/consumer/cn/doc/doccenter-capabilities/use-napi-asynchronous-task): async API lifecycle and thread constraints.
- [Testing overview](https://developer.huawei.com/consumer/cn/doc/doccenter-testing/app-testing-overview): available validation surfaces, selected according to authorized scope.
