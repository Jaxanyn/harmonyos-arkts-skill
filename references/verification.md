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

## Select Checks By Changed Contract

| Change | Evidence to select when available and authorized | Do not infer |
| --- | --- | --- |
| ArkTS logic/parser | Project-supported diagnostics and focused tests with failure/edge inputs; confirm test registration and nonzero executed count. | `tsc` or textual matching proves ArkTS compilation. |
| UI/state/lifecycle | Relevant component or UI tests, actual rendered states, re-entry/disposal checks; adapt orientation/device/accessibility checks to the change. | Browser emulation or a screenshot proves platform callbacks. |
| HAR/HSP/public interface | Build changed module and affected consumers; inspect exports/resources/packaging and relevant runtime loading. | A standalone library build proves consumers still work. |
| Permission/Kit | Match official API constraints, declarations, grant/denial/unavailable paths and actual target capability. | Declared permission proves runtime authorization. |
| Native | Declaration/export review, target build/link, actual packaged libraries and ABI, runtime load/calls; teardown and memory checks if ownership changes. | A host build proves device behavior. |

Discover whether the project uses Hypium, mocks, `src/test`, `src/ohosTest`, or another runner and inspect its registration mechanism. Do not install a second test framework or assume every test source is executable on a host machine. Keep test data disposable. Prefer pure logic tests for deterministic logic and runtime tests for platform-dependent behavior.

Use [ark-test](../ark-test/SKILL.md) for test design, authoring and diagnosis. Record actual selected/executed cases and whether they exercise the target behavior; template-only success is not business coverage. For project-wide discovery, keep [finding categories and coverage gaps](testing-project-sweep.md) separate from check result states.

## Results And Provenance

Record revision or dirty diff, module/product/target, SDK/tool versions, command/check, timestamp, exit code and assertion outcome. Keep log/artifact paths locally and report sanitized excerpts. Distinguish:

- `passed`: the stated criterion was observed on the named environment; list limitations.
- `failed`: the check ran and contradicted the criterion; preserve the actionable diagnostic.
- `blocked`: a required check cannot run because of a concrete missing tool, authorization, dependency, or device.
- `not-run`: intentionally outside this verification scope; name the residual risk.
- `not-applicable`: explain why the changed surface does not require the check.

The overall result is limited by required acceptance, not by the number of successful commands. An exit code of zero with no tests selected is not a test pass. A stale artifact must not be reported as a new build. Compare a failing baseline only when this can be done without disturbing user changes; otherwise report unknown attribution.

## Tool And Authorization Boundaries

Use previously granted explicit scope; repeat approval only for an uncovered action. Read-only CLI discovery is distinct from build/package, and build/package is distinct from install/uninstall or device reset. Bounded log reads do not authorize log clearing. Choose one explicit target before installing when multiple devices exist. Do not uninstall to bypass an update/signature mismatch without authorization, since app data may be lost.

On a failed check, route to its owner, make only authorized fixes, and rerun the affected check. Do not retry unchanged failures indefinitely or upgrade SDK/dependencies to suppress errors. If blocked, provide the discovered command and concrete acceptance check with missing prerequisites, not a fabricated success.

For the platform testing landscape consult Huawei's [testing overview](https://developer.huawei.com/consumer/cn/doc/doccenter-testing/app-testing-overview), then use documentation matching the project's tools. This skill does not require every testing service for every change.
