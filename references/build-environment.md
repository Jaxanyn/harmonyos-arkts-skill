# Build Environment Diagnosis

Load when a build tool cannot start, the IDE and terminal disagree, or the failure owner is unclear. Discovery is read-only. Follow [verification](verification.md) for execution scope and result states; a diagnosis request alone does not authorize a build or persistent environment changes.

## Evidence Before Fixes

1. Establish the command source: project script, wrapper, supported CLI help, or an observed IDE invocation. Record the working directory, revision/dirty changes and first actionable diagnostic. Do not guess a DevEco command or dump a complete environment or signing configuration.
2. Compare actual tool resolution in the failing terminal and the working IDE: Node, Java, SDK, Hvigor and ohpm as relevant. Inspect project configuration and observed executable/version evidence. An installed executable is not necessarily the one used by the process; a claimed IDE success without logs is an unverified comparison.
3. Compare module, product, target, build mode and source revision before treating the two results as equivalent. Keep compile/target/compatible SDK fields separate. Resolve wrapper/local dependency paths and task-relevant process settings without printing credentials.
4. Classify the earliest actionable cause using the table below. Later diagnostics may be consequences; retain unresolved independent errors rather than assuming one cause explains everything.
5. Propose the smallest evidence-backed correction. Prefer the project's existing launcher or a process-scoped setting when sufficient. Apply only within authorization, then rerun the original failed check with the same intended target. Report what changed and what remains unverified.

## Failure Ownership

| Signal | First investigation | Next owner |
| --- | --- | --- |
| Executable missing or tool fails before compilation | Actual command resolution, wrapper, process environment, supported runtime version | Stay in environment diagnosis under ark-check; ark-scan maps unknown paths. |
| Product, target or SDK configuration mismatch | Active configuration and IDE/terminal invocation differences | ark-kit for platform/config implications; ark-native for native build configuration. |
| Dependency cannot be located or fetched | Declared package/local path, lockfile, first resolver error and service availability | Diagnose resolution first; identify config owner before changes. Do not replace dependencies or delete lockfiles. |
| Compiler or linker reaches application sources | Exact file/symbol and selected toolchain | ark-language for ArkTS diagnostics; ark-native for native compile/link/loading. |
| Test runner or assertion fails | Registration, executed cases and actual assertion evidence | ark-test for test defects; use ark-check's ownership table for confirmed product defects. |

Do not infer a product bug from a missing tool, a successful build from a version check, or a source regression from different targets. If the initial cause is fixed and another remains, report the new observed boundary instead of repeating unchanged builds.

## Correction Boundaries And Delivery

Existing explicit authorization remains valid. Show the minimal proposed change before crossing an uncovered config/dependency/public-interface boundary. Do not automatically install tools, upgrade SDKs, change global environment variables, clear caches, replace signing, or reset device data. A process-scoped adjustment must not persist in user/machine settings; end or restore the process context used for the check.

Deliver command provenance, relevant IDE/terminal differences, intended target, first diagnostic, classification, proposed/applied correction and next check. Reuse the verification manifest rather than creating a new report format. When evidence is missing, name the specific missing observation and continue independent work. For concrete illustrations read [engineering examples](engineering-examples.md).
