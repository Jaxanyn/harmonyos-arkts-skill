# Verification

Use this reference when a change touches more than one surface or when the required evidence is unclear.

## Evidence Selection

| Evidence profile | Changed surface | Minimum evidence | Escalate when |
| --- | --- | --- | --- |
| `local` | Local ArkTS, ArkUI, resource, or contained library code inside known boundaries. | Focused inspection and closest existing test/check. | Rendering, navigation, lifecycle, or user-visible behavior changes. |
| `doc-bound` | Platform API behavior, permission semantics, API level, lifecycle semantics, Native/NDK semantics, or compatibility. | Official-document constraint plus local inspection/test. | The documented behavior changes config, error handling, runtime availability, or native ownership. |
| `config-bound` | Permission declaration, dependency, SDK, module config, native build, package identity, signing, lockfile, or public HAR/HSP/HAP interface. | Explicit approval plus relevant test and authorized build. | The config change affects packaging, signing, installation, native output, or consuming apps. |
| `runtime-bound` | Device capability, rendering, location, external service, install, logs, shared-library loading, or hardware-dependent behavior. | Authorized runtime/device check with acceptance criteria. | Static tests or simulator checks cannot observe the intended outcome. |

## Verification Manifest

Use this table in the final report. Discover commands from the target project and available CLI help; treat copied commands as stale until rediscovered.

| Changed surface | Evidence profile | Acceptance criterion | Project command/check | Authorization | Result / remaining risk |
| --- | --- | --- | --- | --- | --- |

Test behavior at the public boundary of a component, ViewModel, service, repository, adapter, or native wrapper. Cover intended outcome, meaningful failure, and one edge condition created by the changed contract.

Build, package, install, emulator, device, native loading, and log work require the user's requested verification scope. If skipped, name the remaining runtime risk rather than implying a full pass.
