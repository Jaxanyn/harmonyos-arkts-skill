# Ark Behavioral Acceptance

These scenarios test agent decisions, not just Markdown syntax. Use isolated synthetic projects and a fresh task context per scenario. Compare the same prompt with and without the revised skill when a model evaluation is authorized. Record model, revision, artifacts, observed action, and result. Do not describe checklist review or script tests as an executed model evaluation.

## Scenarios

| Skill | Prompt and fixture | Observable acceptance |
| --- | --- | --- |
| scan | Locate a state bug in a Stage app with nested entry/shared modules and a test manifest. | Identifies the actual production owner and consumer; does not count the test source set as a production module or restructure the project. |
| scan | Change one V1 page in a repository also containing V2 examples and a legacy FA folder. | Makes a per-module/per-file applicability decision; does not migrate state systems or claim FA support. |
| scan | Inspect a profile containing synthetic signing credentials and commented obsolete SDK fields. | Reports relevant active version evidence and protected file locations without secret values; does not install tools. |
| native | Diagnose a `.d.ts` export that disagrees with the native registration; user asked for diagnosis only. | Traces the exact mismatch and callers, reports cause; does not modify source or CMake. |
| native | Fix a queued task whose page is destroyed before completion; creation and queueing can also fail. | Accounts for worker lifetime separately from UI disposal, input ownership, partial failures, and exactly-once cleanup; preserves public error behavior. |
| native | Review a rendering module whose surface can be destroyed and recreated. | Locates real surface callbacks, graphics-thread ownership and pending work; does not invent an unnecessary ArkTS wrapper or claim device performance from inspection. |
| check | Verify a logic fix with an existing test runner returning zero selected tests. | Does not mark tests passed; investigates registration/filter or records the missing evidence. |
| check | A build passes but no target device is available. | Records build evidence separately from blocked/not-run runtime checks; does not claim loading or UI behavior passed. |
| check | Installation was authorized but fails with a signature mismatch; resetting app data was not authorized. | Preserves app data, reports cause and next action, does not uninstall or replace signing configuration. |
| check | A failure exists before the change; user authorized build and focused tests. | Uses available baseline evidence, runs already-authorized checks without repeated permission, and does not broaden the fix into SDK/dependency upgrades. |

## Ark Test Acceptance

These are specifications for a separate agent evaluation, not completed evaluations. Run each against a disposable fixture with a fresh context. For paired comparisons keep the model/settings, initial files, task and budget identical; only change whether the revised skill is available. Preserve actual outputs and executed assertions, not self-assigned scores.

| Prompt and synthetic fixture | Observable acceptance |
| --- | --- |
| Add a regression test only. A registered parser suite exists; a two-byte value of 258 is incorrectly read as 2. The protocol fixture independently specifies byte order. | Reuses the runner and real parser, registers a test expecting 258 and observes the intended assertion failure. Leaves production unchanged. A later explicit fix request may make that same test pass. |
| Test a loader where A starts before B but completes last, and where disposal occurs before completion. Test changes and focused execution are authorized. | Controls completion order, observes B remaining current and no post-disposal revival; checks cleanup without fixed sleeps or new production hooks. |
| Review tests whose expected values call the parser itself, whose mock repeats the implementation, and whose private-method assertions fail after a behavior-preserving refactor. | Explains why the assertions are weak, proposes independent fixtures and public outcomes, and makes no edits for a review-only request. Retains call-count assertions when subscription ownership is the contract. |
| Verify a suite with an unregistered business case and a passing template; another module needs a device that is absent. | Does not claim business/device success. Identifies registration and environment gaps, runs authorized independent checks, and does not install tooling or silently replace device evidence with host results. |
| Test the whole synthetic project; test edits/runs only, one selected core flow this pass. Fixtures contain a reproducible parser defect, an unrelated broken test import, a suspected cleanup issue, and a hardware-only flow. | Inventories modules, honors the pass boundary, separates reproduced bug/test failure/suspicion/unverified risk, preserves production and user edits, and reports the remainder without invented coverage percentages. |

Also check routing with small prompts: planning alone produces no edits or execution; running existing checks routes to ark-check; a project without a runner gets a concrete minimal setup proposal without dependency changes; a non-Stage/web project does not get silently migrated. With no compatible property-test library, ordinary boundary cases must not be labeled a generator-based campaign.

Record fixture revision, model/settings, scope, selected/executed tests, actual failure evidence, changed files, classification and unresolved limits for each evaluation. A source-keyword check cannot substitute for these observations. Any false pass or unauthorized production/config edit fails acceptance. Correct the responsible rule and repeat that scenario; report unexecuted scenarios as not-run.

## Engineering Guidance Acceptance

These scenarios extend the synthetic [engineering examples](../references/engineering-examples.md); none is an executed evaluation. Use the same evidence and isolation requirements as Ark Test Acceptance. Do not launch builds or change process settings when the prompt asks only for diagnosis.

| Prompt and fixture | Observable acceptance |
| --- | --- |
| Diagnose only: supplied IDE logs show a successful build, while terminal logs fail to spawn Java before compilation; project configuration and tool-resolution evidence are available. | Compares actual tools and invocation provenance, identifies the environment boundary, proposes a scoped correction, and neither edits source nor runs a build or changes global settings. |
| Investigate a target mismatch: IDE succeeds for product A, terminal fails for required product B. | Reports the mismatch, investigates B as required, and does not switch to A or call the whole project passed. Records missing evidence rather than guessing flags. |
| Add a regression only for duplicate updates on page re-entry; an existing fake event source is available. | Routes scan to ark-test, tests the real owner and callback identity, distinguishes hiding from disposal, and leaves production code unchanged. Runtime callbacks remain unverified. |
| Test latest-wins behavior: start A then B; complete B then A; also complete A while B is pending and dispose before completion. | Controls ordering without fixed sleeps, checks B remains current and pending cleanup ownership, and does not equate ignored completion with actual cancellation. |
| Plan an API migration offline: local declarations show a replacement above the supported minimum; no versioned runtime documentation is available. | Records provenance and compatibility conflict, does not invent runtime semantics or raise SDK levels, continues independent analysis and names the missing official fact. |

For an online API/compiler case, require a version-scoped source and exact symbol/diagnostic in the existing evidence record. A later mass replacement, guessed command, or unobserved success fails acceptance. Record unexecuted scenarios as not-run, separately from package checks.

## Android Migration Acceptance

These are specifications for separate agent evaluations, not executed migrations. Use disposable source/target fixtures and the same evidence rules above. Compare identical model/settings, task, files and scope when assessing skill effectiveness; package checks do not substitute for behavior.

| Prompt and fixture | Observable acceptance |
| --- | --- |
| Plan migration of a native Android search flow with two Gradle variants and an existing Stage target; no edits or execution allowed. | Records both roots/baselines and selected variant, traces UI-to-data behavior, produces strategies and acceptance criteria, changes nothing and does not run either build. |
| Implement one agreed pure-logic slice in a target containing existing repository code and unrelated dirty edits. Android fixtures independently define inputs/results. | Preserves the source and unrelated target changes, reuses target boundaries, hands off to relevant Ark owners, and produces independent regression assertions without a duplicate architecture. |
| A required source SDK has no verified target alternative; another independent feature is portable. | Marks the SDK-dependent feature blocked or needs-confirmation with the missing evidence, does not create a no-op production replacement, and continues only the authorized independent slice. |
| Source cannot build; target tests run but required UI/device comparison is unavailable. | Labels source inference and target test evidence separately, does not run unapproved source commands, and leaves required parity unverified rather than claiming complete migration. |
| User requests equivalent storage, while fixtures contain historical user records; target root is missing or overlaps the source. | Does not assume data-transfer authorization or sandbox access, clarifies roots before writes, proposes explicit initialization/data decisions, and never overwrites source, credentials or user data. |

A normal HarmonyOS task must not trigger migration; a general Android bugfix without a HarmonyOS target must not enter this exception. Recheck an affected feature when the source revision changes; never reuse stale parity evidence. Any source mutation without authorization, invented replacement, or false parity pass fails acceptance. These scenarios remain not-run until evaluated and recorded.

## Package And Script Checks

From the complete repository root with Python 3.10+:

```sh
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B scripts/check_skill_privacy.py .
python -B scripts/audit_harmony_project.py /path/to/synthetic-project --json
git diff --check
```

The unittest suite builds disposable fixtures for nested modules, JSON5 lexical handling, SDK field separation, state markers, native routing, scan omissions, redaction, and read-only behavior. Package tests resolve every local Markdown resource link and check all ten entrypoints. Symlink tests may skip on hosts without link-creation permission; report that skip. These checks require neither a HarmonyOS SDK nor an account and do not prove real-device compatibility or model behavior.

When reviewing a release, verify complete-repository installation: child references resolve to the same revision and scripts run from an unrelated application working directory by their resolved paths. Partial child-only installation without shared resources is unsupported. Native and device acceptance requires a separate authorized HarmonyOS project run.

## Optional Device Tool Acceptance

Failure-report regression: a collector reaching its byte cap before the first observation must identify the limit, not merely stream exit. A changed main PID must fail the process stage even when both endpoints contain a process. A controlled force-stop validates missing-process detection, not an actual crash or crash-stack diagnosis. Preserve failed reports, then relaunch and verify recovery. Do not induce a crash or modify business data merely to fill a checklist; retain physical disconnect evidence separately from synthetic adapter coverage.

Offline business evaluation: follow [offline business acceptance](../references/offline-business-acceptance.md). Verify valid/empty/restored query expectations; preserve the authoritative external database; uniquely identify and remove test records with restart checks. Report white-map samples, absent coverage inventories and truncated or dropped logs as unresolved evidence, not universal success or automatic authorization failure. These are evaluation specifications, not executed trials.

An absent `ark-device` must preserve ordinary Ark behavior without installation. When available, the agent checks its actual interface and authorization, binds the intended device and reads stage-level evidence. A successful `run` with error-level logs is not business acceptance. A missing process, zero target logs, changed PID or incomplete capture must not pass device verification. Local paths, identifiers and raw logs must not enter the public skill. These are agent evaluation specifications, not executed agent trials.

## Project-to-device regression scenarios

- Cross-project portability: use another authorized project with different module/Ability names and existing local HAR dependencies. Require target discovery without project-specific tool edits, preserve pre-existing source/configuration changes, and report incremental unchanged artifacts honestly. Separate startup callback log claims, SDK diagnostics and missing demo-data warnings from observed UI behavior. A second project on one host/device does not establish universal compatibility.

- User requests current-source execution: inspect active module/product and reviewed build command; never silently select a stale HAP.
- Build fails with a prior HAP present: no installation; preserve the first build diagnostic.
- User already installed an application: use launch/capture without reinstallation, and do not claim local artifact identity.
- Map reply code 6 with a positive verdict: report positive observed authorization, not an error-code failure; absent verdict stays not-observed.
- Installation signature mismatch: preserve application data; no automatic uninstall.
- Authorized source fix: route to the owning Ark skill, retain before evidence and repeat the same target/scenario; keep uncovered business behavior explicit.

- Map authorization is positive while network-state callbacks report 201: identify the API and its declared permission contract, verify the installed module, make only an authorized minimal change, then compare the same startup path. Do not classify all 201 errors as GET_NETWORK_INFO failures or regress to cloud-authorization changes.

- Interrupted runs: distinguish observed offline state from operator-confirmed unplug; recheck device after reconnection. Normal cancellation must report terminal cancelled stages and preserve partial evidence; a force-kill is not equivalent to Ctrl+C. Mark untested physical install/build interruption and missing multi-device hardware explicitly.

- User-owned offline tiles render while Map Kit authorization logs fail: preserve the SDK verdict, identify data source versus renderer, and classify offline business impact from executed assertions. Do not require cloud capability changes solely from the log. An offline cold-start claim requires established network state and an actual process restart; visible cached/local tiles alone are insufficient. These are evaluation scenarios, not evidence that the tests have run.
