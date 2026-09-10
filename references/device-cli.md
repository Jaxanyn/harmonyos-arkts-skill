# Optional Ark Device CLI

Use only for an authorized device operation. This reference describes the `ark-device` 0.1 interface; inspect the available executable's help before use. Its optional source is in [tools/ark-device](../tools/ark-device/README.md), maintained in this repository but installed separately. Resolve the source path relative to this reference when using the repository copy; for an installed executable inspect its actual path/version. Do not install or download it automatically.

## Discovery And Scope

Discover `ark-device --help` or a user-supplied source invocation, then run `doctor` and `devices` as appropriate. The CLI requires Python 3.10+ and a configured HDC; it does not require a running IDE interface. A doctor pass without devices proves only host discovery. Select the intended device explicitly when several are connected.

`install` and `run` update an application; `launch` starts it; `logs capture` reads a running application's logs. Keep these within existing authorization. Signed-package execution does not authorize builds, dependency installation, permission grants, signing changes, uninstall or data reset. Do not claim the IDE was closed unless independently observed.

## Interface

| Operation | Required arguments |
| --- | --- |
| `doctor`, `devices` | None; optional `--hdc` and `--device` |
| `install` | `--hap` pointing to the authorized signed HAP |
| `launch` | `--bundle`, `--ability`, `--module` |
| `logs capture` | `--bundle`; app must already be running |
| `run` | `--hap`, `--bundle`, `--ability`, `--module` |

Arguments follow the operation, or `capture` for logs. `--output` must name a new directory; otherwise evidence goes to a system temporary directory. Log sessions accept `--seconds` (default 30, maximum 600) and `--max-bytes` (default 10 MiB, maximum 50 MiB). Install operations accept `--install-timeout` (default 180, maximum 600 seconds).

Use `run` to install, start capture before launch, observe the process and collect evidence. It accepts one HAP and checks its embedded target metadata; do not pass guessed Ability names or claim a filename proves signing. Keep the input artifact stable during execution. The CLI records its hash, not a claim that it was built from current source. Multi-HAP/HSP deployment is outside this version.

## Evidence And Failure Routing

Read `report.json` and the scoped `target.log` where present. Exit codes are 0 for operation success, 1 for failure, 2 for invalid arguments and 130 for cancellation. A passing operation does not imply `business_acceptance`; that remains `not-run` until separate assertions are performed.

Logs are selected by observed main-process PID and a device-clock cutoff with one-second precision. Same-second history may remain; child processes and log loss are not covered. Zero target logs, collector interruption, size limits, missing processes or changed PIDs cannot establish a complete successful run. PID snapshots do not prove continuous liveness. Error-severity excerpts are diagnostic candidates, not automatic bug verdicts.

Route tool/path/connection failures to environment diagnosis; install/signature or platform failures to the appropriate configuration/Kit owner; rendering and business behavior to their existing Ark owners. Reproduce and confirm before changing production code. Never uninstall or clear data merely to obtain a pass.

The tool stops its own collector and leaves the app installed/running. Local reports include private identifiers and paths; raw target logs may contain credentials. Review before sharing or placing in model context. CLI redaction is best effort, not a privacy guarantee. Do not copy local device details or test-project identity into this reusable skill.

## Read Reports By Evidence Type

Keep four conclusions separate: execution (build/install/launch and process snapshots), log capture, SDK/log signals, and business assertions. The top-level tool status is only the operation result. Missing stages remain not-run; missing diagnostic fields are unknown, not zero errors.

When the optional CLI exposes `logs.coverage`, interpret `bounded-window` as a completed bounded observation without detected loss, `partial` as failed/cancelled/truncated capture or observed device drops, `unknown` as insufficient coverage metadata, and `not-run` as no capture. A collector can succeed while device warnings disclose dropped lines. Counts include recognized warnings only in the selected target stream; zero detected drops does not prove all events were logged. Older reports lacking this field require inspection of the original evidence, not retroactive certification.

Keep SDK authorization and error-level counts as signals with their observed scope. Do not promote deployment success, absence of error logs, or positive authorization into a business pass. Put scenario-level expectations, actual results, evidence, cleanup and remaining gaps in a companion acceptance report, preserving raw CLI reports. Reports do not themselves diagnose arbitrary SDK failures or execute UI assertions.

## Installed-App Retest Details

When supported by local help, `launch --capture --bundle ... --ability ... --module ... --seconds 30` captures around launch without installing. It does not force-stop an already running app; no new initialization log means authorization is not observed, not passed.

Read `diagnostics.map_authorization` separately from operation status: `passed`, `failed`, `mixed`, or `not-observed` describe explicit Map Kit log evidence within this capture only. Never interpret internal reply `code:6` alone as failure; it was observed in both outcomes. A successful collector is not successful authorization, and authorization is not business acceptance. Network permission failures and page callback errors require their own diagnosis.

Map Kit is an open capability, not a guessed map ACL permission. An empty ACL list does not establish missing Map Kit authorization. Confirm application/team identity and current official capability requirements before configuration changes. After a Profile update, verify the signed artifact was regenerated; compare its hash and embedded signing evidence without exposing credentials. `INSTALL_SIGNATURE_MISMATCH` requires matching signing identity or a user-authorized data-loss decision; never automatically uninstall. Keep build/signing operations under their own authorization.

## Offline Map Business Context

Before diagnosing map logs, identify the data source (bundled files, local archives, cached online tiles or live services), renderer/controller, and features actually under test. User-owned offline tiles can render through a Map Kit component that still emits SDK authorization diagnostics. Preserve those diagnostics, but do not automatically turn them into a blocker for verified offline behavior or request cloud/signing changes.

Report authorization evidence and business impact separately: confirmed feature failure, no failure observed in the tested scenario, or impact unverified. Local data does not prove all SDK features work without authorization. Visible tiles do not prove a network-disconnected cold start. Establish WLAN/mobile-data state, stop only the authorized app, capture around relaunch, and verify local-resource initialization plus the actual viewport. Do not clear caches or user data to simulate first installation.

Offline acceptance should cover cold start, pan/zoom across known local coverage, markers and property queries, route queries and local custom-airport persistence. Record each scenario and its assertions independently. Missing coverage, unavailable input data, device lock or unconfirmed network state blocks only the affected assertion. SDK log severity alone neither passes nor fails the whole business suite. Restore any network setting changed by the agent; ask the operator to restore operator-controlled changes when finished.
