# HarmonyOS Project Shape

Use this reference when scanning an unfamiliar pure-native HarmonyOS Stage-model project.

## Stage Model Landmarks

| Surface | What to inspect | Why it matters |
| --- | --- | --- |
| Application scope | `AppScope/app.json5`, app resources, icons, labels | Identifies app-level metadata without changing module behavior. |
| Module scope | `entry/`, feature modules, HAR/HSP modules | Determines the smallest module that owns the change. |
| Ability declaration | `module.json5`, abilities, pages, permissions, metadata | Controls entry points, routing, permissions, and install/runtime behavior. |
| Build profile | root and module `build-profile.json5` | Controls SDK compatibility, targets, signing selection, native build, and packaging. |
| Dependencies | `oh-package.json5`, lockfiles, local file dependencies | Controls public library use and reproducibility. |
| Resources | `resources/base`, `resources/rawfile`, profiles, media | Separates UI resources, bundled assets, profiles, and user data. |
| Source layout | `ets/pages`, `ets/components`, `ets/viewmodel`, `ets/model`, `ets/utils` or local equivalents | Reveals the local architecture rather than imposing a template. |
| Tests | `src/test`, `src/ohosTest`, project scripts | Determines the closest evidence that can verify a change. |
| Native | `src/main/cpp`, `CMakeLists.txt`, `types/*/index.d.ts` | Reveals cross-language contracts and build risk. |

## Scan Guidance

Start from the file or user-visible behavior named in the request. If none is named, identify the module, ability, page route, and nearest owner before proposing edits.

Use existing names for layers and folders. A project may use ViewModel, manager, service, repository, adapter, or utility naming differently; follow the local convention unless the request is explicitly a restructuring task.

## HAR, HSP, and HAP Boundaries

- HAP application modules own abilities, app-facing permissions, install behavior, and runtime entry points.
- HAR libraries should expose stable ArkTS APIs and avoid owning app identity, signing, or user-specific configuration.
- HSP/shared native surfaces add packaging and ABI risk; verify the consuming module and target devices.

Do not move code across module boundaries merely to make a single change look cleaner. Name the target module and public interface before changing a library boundary.

## Version And Module Evidence

Record configured compile/target/compatible SDK values separately, per product when present. Do not replace them with a remembered latest release. Detect Stage/FA from application/module declarations and build configuration, then verify the affected module. A `src/ohosTest/module.json5` is test metadata, not another production module. Module roots can be nested or renamed through `srcPath`; the first directory segment is not a reliable module identity.

Inspect state patterns per affected file: V1, V2, mixed, or unknown. ArkUI state management and the ArkTS language/toolchain version are independent facts. Existing V1 code is not a request to migrate to V2. Inspect SDK diagnostics and official documentation before changing decorator semantics.

For HAR/HSP work trace package entry/export declarations, local dependencies, public resources, and consumers. A `.d.ts` file alone is not proof of Native involvement. A standalone library may have no EntryAbility or pages; do not fabricate them. Ignore build/dependency output and embedded third-party examples when selecting the production owner.

## Scanner Limits

The bundled scanner is a read-only heuristic inventory, not a JSON5 parser, compiler, dependency graph, or security audit. It strips comments without stripping quoted strings and reports production module roots, state markers, SDK field names, and relevant paths. Unquoted JSON5 keys and single-quoted strings are supported for simple signal extraction; computed configuration and nested objects still require inspection. Missing, oversized, or unreadable content is reported as a limitation. Symlinks/junctions are skipped and generated/dependency directories are pruned. No matches means unknown, not absent or safe.

Only known metadata values (module type, SDK version, permission, Kit name) should appear in the inventory. Do not copy configuration bodies or credentials into reports. Keep local absolute roots and any customer-identifying filenames out of public examples.
