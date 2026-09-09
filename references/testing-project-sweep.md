# Whole-Project Test Sweep

Load only when the user asks to test a project broadly or find bugs across modules. Whole-project means inventory the project and select tests by risk, not exhaust every input, path, version or device.

## Scope And Budget

Reuse the [ark-scan](../ark-scan/SKILL.md) project map or build it once. Include production modules, key user journeys, public library consumers and existing tests. Exclude generated output and third-party internals as test targets, while considering the application's integration contracts with them.

State the selected scope and execution boundary. Honor a user-supplied time or case budget. Without one, choose a finite first pass over the highest-risk flows and report the remainder; do not require a budget discussion to begin or silently imply exhaustive coverage. New tests and focused runs in the existing environment are in scope unless excluded. Production fixes, dependency changes and device mutations need their own applicable authorization.

## Execute One Pass

1. Map each relevant module/flow to its contract, existing tests, feasible environment and gaps. Avoid rescanning known facts.
2. Establish a baseline with the applicable existing tests. Record actual selected/executed cases, not just exit status. Separate template-only results, baseline failures and environment blockers. Do not disturb user changes to recreate history.
3. Rank targets by user impact, failure likelihood and missing evidence: data loss, crashes and broken core flows first; then async ownership, caches, parsing, permissions and recovery as applicable. Explain priorities without inventing numerical risk scores.
4. Add and execute focused tests using [test design](testing-design.md) and [HarmonyOS testing](testing-harmony.md). Continue independent work if one environment is blocked. Deduplicate findings with the same root cause; do not broaden into production fixes unless authorized.
5. Stop after the declared pass/budget or when selected targets have evidence or named blockers. Report the most valuable next untested boundary rather than claiming the project is bug-free.

## Classify Findings

| Category | Required evidence | Report as |
| --- | --- | --- |
| Reproduced bug | Observed behavior contradicts a stated contract, with a failing assertion or repeatable runtime steps. | Impact/severity justified by the affected user flow; source location, prerequisites, expected/actual behavior, reproduction and evidence. |
| Suspected issue | Concrete code or observation suggests a defect, but reproduction or contract is unresolved. | Hypothesis, supporting evidence, missing fact and smallest confirming check. |
| Unverified risk | Relevant behavior lacks executable evidence because of scope, tools, data or device limits. | Boundary, reason, and concrete next check; not a discovered bug. |

A failing check must first be attributed to product behavior, test code, environment, or an unclear requirement. Test defects and environment failures are recorded separately from product bug counts. Preserve uncertainty when baseline attribution cannot be established. Use [verification result states](verification.md) for check results; finding categories are not substitutes for those states.

## Report

Lead with covered modules/flows, actual test counts, reproduced/suspected findings and blockers. Include a compact map:

| Module / flow | Contract and priority | Existing or added check | Environment and result | Gap / next check |
| --- | --- | --- | --- | --- |

For each reproduced bug include impact, source location, prerequisites, reproduction steps or test, independent expected result, actual result, evidence location, and fix status. Link regression tests when present. Say whether production code was changed; an unfixed bug found by a test remains unfixed.

Do not fabricate a coverage percentage without a defined denominator and measurement. Successful tests do not establish absence of bugs. Keep logs sanitized and store reports in the user's requested location or respond inline; do not create permanent report infrastructure.
