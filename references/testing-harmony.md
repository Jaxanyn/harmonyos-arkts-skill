# HarmonyOS Testing

Load for environment selection and platform-dependent tests. This is discovery guidance, not a fixed SDK or testing API catalog. Reuse [official-document evidence](official-document-evidence.md) for the selected framework and version.

## Discover Before Choosing

Inspect the target module's active SDK/product configuration, package dependencies, test sources, registration entrypoints, runner configuration and supported CLI help. Identify whether the project uses Hypium, Hamock, UI testing, host scripts, native tests, or another existing facility. A directory named `src/test` does not establish host executability; `src/ohosTest` alone does not prove registration or device availability.

Trace the selected runner to the actual production code and test entry. Distinguish test modules from production modules, sample assertions from business coverage, and installed tooling from a working test environment. Do not print signing values or device identifiers.

| Available environment | Action | Limit |
| --- | --- | --- |
| Existing compatible runner | Reuse source layout, registration and project command; confirm target cases execute. | A passing unrelated suite does not cover the changed contract. |
| Host scripts loading production logic | Inspect substitutions and transformations; test the real supported logic boundary. | Host success is not ArkTS compilation, decorator behavior or platform runtime evidence. |
| Platform/device tests | Discover target and runtime prerequisites; run within authorized scope. | Emulator results do not establish physical sensor or device-specific support. |
| No runnable test facility | Produce the smallest concrete setup proposal and useful cases; continue independent analysis. | Do not silently install a framework, upgrade SDKs, or create a universal ArkTS transpiler. |

## Select By Behavior

- **Pure logic:** parsers, conversion and validation use independent fixtures at an existing boundary. Do not replace the production function with a copied implementation for host execution.
- **Flows:** keep the real ViewModel/service under test; substitute I/O and time where supported. Cover stale completion, cancellation, errors and teardown according to the changed contract.
- **Kits:** distinguish declarations, runtime grants, denied/revoked permissions, unsupported capability and service failures. Mocked denial tests verify application handling, not the system permission dialog or actual device availability.
- **ArkUI:** verify interactions, navigation and relevant state across hiding, disposal and re-entry. Inspect the actual rendered surface or test-accessible component tree before choosing stable selectors; do not invent identifiers. Use bounded readiness conditions, not guessed delays or default coordinates. Screenshots support visual evidence but do not prove callback behavior.
- **Native:** exercise parameter/error contracts and async ownership through the real wrapper where feasible. Declaration review, host unit tests, target build/link, packaged ABI and device loading are distinct evidence; refer to [native guidance](native-napi-cmake.md).

Keep temporary files and records disposable. Clean up only resources created for the test; permission changes, installs, uninstalls and data resets require the applicable scope. Reuse [verification](verification.md) for provenance, gaps and result states.

For comparison, [Anthropic's web testing skill](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) uses observation before interaction and resource cleanup. Its browser selectors, Python runner and network-idle assumptions are not HarmonyOS instructions.
