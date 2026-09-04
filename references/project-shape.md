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
