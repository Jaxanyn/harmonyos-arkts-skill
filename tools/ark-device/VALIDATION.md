# Validation record

Date: 2026-09-10. This is a scoped observation, not an all-device compatibility claim.

## Current acceptance summary

This table supersedes historical counts and pending items below. Evidence is scoped to the current source, one Windows host/toolchain and one USB device. Optional tooling is separate from the Ark skill package.

| Evidence level | Scope | Current result / limit |
| --- | --- | --- |
| Automated | Standard-library tool suite | 53 tests passed; synthetic commands/fixtures, not hardware. Automatic-plan fixtures use the installed JSON5 parser and may skip where unavailable |
| Automated | Skill package | 16 passed, 1 symlink-capability skip; privacy and diff checks passed |
| Device | Two Stage projects, different entry/Ability names, one with local HAR dependencies | Automatic target discovery, incremental build, signed installation, launch and bounded logs passed without project-specific runner edits; not clean-build reproducibility |
| Device | Failure and recovery reports | Log byte cap, controlled process exit, changed PID, relaunch passed; early byte-cap and changed-PID status defects fixed |
| Earlier device evidence | Offline stream/reconnect, log SIGINT cancellation, signature rejection | Observed in earlier runs, not all repeated on the latest revision; no claim of physical build/install interruption |
| Bounded business evidence | First project: selected offline queries, persistence/cleanup, map samples; second project: local geometries and filter counts | Limited scenarios only; SDK and sample-data warnings remain independent. Raw CLI business_acceptance stays not-run; companion reports hold manual assertions |
| Synthetic only / gaps | Build/install cancellation retention, multi-device selection ambiguity, recognized device-drop warnings | No simultaneous physical devices or forced real install cancellation; detected zero loss does not prove every event was logged |
| Not verified | Spontaneous startup crash/stack diagnosis, other OS/SDK combinations, multi-HAP/HSP deployment, complete business suites, real Android migration, model behavior evaluations | Remain separate acceptance tasks |
| Packaging | 0.1.1 wheel built offline and installed in an isolated environment | Nine runtime files match source bytes, including prepare.cjs; both entrypoints, all 53 installed-package tests, pip check and real-project read-only preparation passed. No publication or common-environment installation; old 0.1.0 retained |

Reproduce tool checks from this tool's root: `python -B -m unittest discover -s tests -p "test_*.py" -v`. Skill checks run separately from the complete skill package root. Local device evidence remains private under the ignored build directory; it is not bundled with the skill or promised as a portable artifact.

## Repository placement verification

Source now lives at tools/ark-device in the Ark repository; installation remains optional. The nine runtime files still match the tested 0.1.1 wheel source. The synthetic signing fixture was rewritten without changing its data or assertion to avoid a privacy-scanner false positive. All 53 tool tests passed from this new directory; skill package/link checks passed 16 with one symlink skip. Build output, wheels, environments and real-device evidence remain ignored. Original application-directory copies are retained as local history, not a second maintenance location.

## Package acceptance: 0.1.1

Built with already installed setuptools/wheel, without dependency downloads. Installed with `--no-index --no-deps` into a new isolated virtual environment. Copied the existing test suite into a directory without a source package and confirmed imports resolve to that environment's site-packages; all 53 tests passed. `ark-device --version` reports 0.1.1; `ark-project --help`, `pip check`, and read-only preparation of the second project passed using the bundled JavaScript helper.

Wheel SHA256: `5971d02cfc57294a59a7421a641a95ade660d5fb4338b11ed8acbd335b07d2c4` (17,911 bytes). Archive inspection found exactly the nine expected runtime files plus distribution metadata, with all runtime bytes equal to source; no raw device evidence is bundled. Local artifacts: `dist/ark_device-0.1.1-py3-none-any.whl` and its checksum file. Private test evidence is under `build/wheel-check-0.1.1`.

This packaging run did not invoke a device, rebuild a business application, modify a common Python environment, publish or commit. It does not add cross-platform or minimum-Python-version evidence beyond the tested Windows environment.

<details>
<summary>Historical observations (chronological; earlier counts and gaps are not current status)</summary>

## Automated checks

The 46-test standard-library unittest suite passes and uses synthetic commands and temporary HAP metadata. It never calls HDC. Coverage includes missing/ambiguous devices, explicit target binding, malformed targets, HAP/launch mismatch before device operations, success-message checks independent of exit code, timeouts, output flooding, log filtering, empty captures and cancellation cleanup.

## Physical-device observations

Host: Windows, Python 3.13, HDC 3.2.0b, one USB-connected authorized device. Exact connection identifiers, paths, HAP hash and application identifiers stay in local reports, outside the reusable package.

| Check | Observation |
| --- | --- |
| `doctor` | HDC discovery, device selection and required aa/HiLog switches passed |
| `run` with an existing signed HAP | Replacement installation and launch accepted; same main PID at initial/final checks; 30-second capture produced 739 target lines without truncation |
| Standalone `launch` | Valid target accepted and PID observed |
| Invalid Ability | CLI returned exit 1 and `LAUNCH_UNCONFIRMED`, rather than treating the underlying zero exit code as success |
| Standalone `logs capture` on a quiet app | No new target lines; correctly returned exit 1 and `NO_TARGET_LOGS`, even though the process remained present |

Error-level map-service messages were retained as diagnostics. App functionality, map correctness and offline behavior were not accepted. The run used command-line tools; whether the IDE was closed was not observed. No source, signature, permission or SDK configuration was changed. No uninstall or data reset was issued. The application remains installed/running; collectors started for these checks were stopped.

## Remaining acceptance

Physical cable removal, physical-device cancellation, multiple simultaneous devices, other HDC/OS versions, signed-package rejection and a fresh dependency/toolchain installation remain untested on hardware. Their covered synthetic cases do not establish hardware compatibility. Package installation/distribution, builds, MCP, UI assertions and other operating systems have not been validated.

## Follow-up device evidence

On the same test environment, an updated local Profile initially left the existing HAP unchanged. Rebuilding with the matching Java runtime produced a new signed artifact; replacement installation was rejected with `9568332 / install sign info inconsistent`. The user removed the old app and installed the new package. The agent did not uninstall it.

A subsequent installed-app launch/capture observed `checkMapPermission:true`, no map-authorization-failure message, and 617 target lines over 30 seconds with the same initial/final PID. An earlier observation ended with a missing process and remains a failed run. Internal reply `code:6` appeared with both true and false authorization verdicts and is not a failure classifier. Other error-level messages remained; map/business acceptance is still incomplete.

The new `launch --capture` command was then exercised on the already running app: a 10-second capture produced two target lines with unchanged initial/final PID and no installation command. No new map initialization occurred, so authorization correctly remained `not-observed`. The path is also covered by a synthetic no-install regression. Physical signature rejection has now been observed; other remaining acceptance items above still apply.

## Project orchestration and packaging

The project runner composed the existing adapter with a reviewed Hvigor command, matching process-scoped Java and existing signing. A real incremental build, copied-HAP installation, launch and 30-second capture passed. There were 617 target lines, a stable initial/final PID and an explicit positive Map Kit authorization verdict. Other diagnostics remained; no business acceptance or automatic repair was claimed. The build reused identical artifact bytes and reported this explicitly.

The standard-library suite now includes project discovery, build failure with an old HAP present, timeout, target mismatch, artifact copy isolation, process environment and no-device behavior. CLI packaging was built offline with existing build dependencies. An isolated virtual environment is used for entrypoint validation, not a global installation. New project-run hardware coverage is limited to this one project/environment; native multi-HAP/HSP deployments, other platforms, physical disconnect/cancel and multiple real devices remain future acceptance work. MCP remains deferred.

## Permission repair experiment

A consuming demo module omitted network-state permission declarations. The selected SDK and official Network Kit reference require GET_NETWORK_INFO for network connection registration. Adding only that declaration removed the registration denial and network-scene callback error in the next startup capture, while explicit Map Kit authorization stayed positive. A separate startUrlRequest network-status denial remained. Adding INTERNET in a controlled second run did not remove that event; the extra permission was reverted. This confirms a scoped registration fix, not resolution of every network or SDK diagnostic. No SDK internal implementation or all-business success is claimed.

## Reliability follow-up

During an authorized 180-second device capture, HiLog exited early after about 48 seconds with underlying exit code 0. The CLI correctly returned exit 1 / LOG_STREAM_ENDED, preserved the partial target log and report, and stopped its collector. Immediate HDC enumeration showed no device. This establishes handling of an observed device-offline event; the precise physical unplug time and cause require operator confirmation. Recovery and multi-device physical acceptance must be recorded separately.

Cancellation regressions found that partial build/install command output could be lost and a build stage could remain running. The shared process runner now attaches collected output to cancellation, HDC keeps that evidence, and build/install stages terminate as cancelled. Tests use a real local child for interruption/cleanup and synthetic build/install adapters; they do not claim a real installation was interrupted. Device-side installation may continue after client cancellation.


After the operator reported reconnection, doctor again found the device and verified aa/HiLog switches. A real-device launch/capture was interrupted with a programmatically delivered SIGINT (normal Python interrupt handler, not a forced process kill). The supervising subprocess observed exit code 130; both operation and logs were cancelled, report.json/report.md were saved, and the owned collector stopped. The quiet app emitted zero selected lines before cancellation; no log-content or map-authorization pass was inferred. This validates the SIGINT path, not a physical keyboard keystroke or an Agent force-abort.

Current reliability acceptance: observed offline stream handling and reconnect passed; real-device log SIGINT cancellation passed; build/install cancellation output retention and device-selection ambiguity passed synthetic regressions. Physical install interruption, physical build interruption with descendant cleanup, simultaneous multiple devices and non-Windows systems remain unverified. No app data was cleared and no real install was interrupted during these checks.

## Automatic preparation checks

Seven additional fixture tests exercise the real locally installed Hvigor JSON5 parser, without running HDC or builds: registered entry selection, signing-secret exclusion, product ambiguity and explicit selection, unregistered example exclusion, unsigned-product rejection, target/product mapping and escaping-module rejection, plus parse-error redaction. (Some checks share a test.) These tests skip as a group when the supported DevEco installation is unavailable; the remaining Python suite is independent of it. Temporary parser fixtures are kept in the ignored build directory to avoid host sandbox path traversal restrictions.


Automatic preparation selected the expected targets from two local projects. The new `run --project` entrypoint then completed a real incremental build, installation, launch and 30-second capture on the smaller demo: 619 target lines, unchanged initial/final PID and a positive map-authorization verdict. Network/SDK diagnostics remain unresolved independently. The second project's preparation was checked only; no new full build or device acceptance is claimed for it. This run required no hand-written plan, dependency download, signing replacement or business-source edit.

## Preparation boundary regression

Automatic-plan tests now cover multiple registered entry modules, multiple targets and custom signed-HAP output selection in addition to product ambiguity, signing presence, target/product mapping, unregistered examples and path containment. These are synthetic configuration checks using the installed JSON5 parser; they do not constitute multi-device or multi-HAP installation validation.

## Report separation update (2026-09-10)

Source report rendering now separates execution, capture, SDK/log signals and business assertions. Target HiLog drop warnings are counted; logs.coverage distinguishes bounded-window, partial, unknown and not-run without changing operation exit codes or upgrading business acceptance.

Validation: 52 synthetic tool tests passed, including loss-aware coverage, legacy missing metadata and SDK-failure/business-status separation. Skill package: 16 passed, 1 symlink capability skip; privacy and diff checks passed. Example under build/report-format-example is synthetic. No device invocation, wheel rebuild, installation or publication was performed for this report-only update; use the updated source to obtain the new format.

## Failure-report hardware regression (2026-09-10)

Current source passed 53 synthetic tests. Hardware checks confirmed normal bounded capture, a deliberate 1024-byte log limit, missing process after controlled force-stop, successful relaunch, and changed PID after controlled restart. Fixes: recognize a byte cap before the first collector poll; mark changed-PID process observation failed. Both fixes were rechecked on hardware. Expected error reports retain partial evidence and business_acceptance=not-run. The application was left running; no uninstall, data reset or package reinstall was performed.

Controlled process exit is not a spontaneous startup crash. Physical cable removal/cancellation use earlier evidence, not a new hardware claim for this revision. Multiple devices/projects, actual crash-stack diagnosis and forced device log loss remain separate acceptance. Private evidence is in local build/failure-regression-acceptance.md. No wheel rebuild or publication.

## Second-project portability check (2026-09-10)

The unchanged project runner auto-selected a differently named entry module and Ability in a second project with three local HAR dependencies. Incremental build, signed-HAP installation, launch and a 20-second 638-line capture passed; the artifact was unchanged by the incremental build. Coverage was bounded-window with no recognized drops. Initial UI showed three local GeoJSON geometries; a four-step filter cycle showed one point, one line, one polygon and all three, restoring the original filter.

Tracked source/configuration hashes matched the pre-run baseline, including existing user modifications. SDK/error signals and missing sample-tile warnings remain separate from this bounded UI pass. No project-specific names were added to the tool. This validates a second project on the same host/toolchain/device, not all projects, a clean build, multiple-HAP deployment or complete offline behavior. Private evidence: build/yinmap-cross-project-run/acceptance.md.

</details>
