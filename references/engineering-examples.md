# Engineering Examples

These synthetic walkthroughs illustrate decisions, not executed tests, proven fixes, or ready-to-run ArkTS templates. Discover commands and API constraints in the target project. Read only the relevant case; no private project data or machine-specific setup is required.

## Terminal Cannot Find Java

- **Symptom:** The developer reports that the IDE builds successfully; the terminal fails before compilation because Java cannot be started.
- **Evidence:** Compare the actual IDE invocation/log with the terminal wrapper, executable resolution and process settings. Without IDE evidence, label that side of the comparison unknown.
- **Route:** ark-scan maps tooling; ark-check uses [build environment diagnosis](build-environment.md).
- **Action:** Prefer the existing compatible launcher or an authorized process-scoped setting after confirming the cause. Do not edit application code or install another JDK merely because the terminal cannot locate one.
- **Acceptance:** The original command for the intended target starts the required tool. Build success needs its own observed exit/result; a subsequent compiler failure remains a separate finding.

## IDE And Terminal Build Different Targets

- **Symptom:** One invocation succeeds and another reports a missing module or resource.
- **Evidence:** The IDE selects a supported product and module target; the terminal selects a different combination. Compare revision, working directory and build mode too.
- **Route:** ark-check compares invocations; ark-kit owns any necessary platform configuration change.
- **Action:** If the terminal target was unintended, select the intended existing target using the discovered project command. If the failing target is required, investigate it rather than switching to a passing target to hide the failure.
- **Acceptance:** Compare results only for matching intended inputs. Record any still-required failing target; do not delete modules or change SDK levels to manufacture agreement.

## Re-entry Duplicates A Subscription

- **Symptom:** After repeated page entry, a single event causes multiple updates.
- **Evidence:** Observe ownership, callback identity, registration and cleanup across entry, hiding, disposal and re-entry. Hiding is not automatically disposal; follow the actual lifecycle contract.
- **Route:** ark-ui owns lifecycle behavior; ark-test builds the regression; ark-check reports runtime limits.
- **Action:** Reproduce with a controlled event source. Correct registration/cleanup only when production fixes are authorized; otherwise leave a failing regression and finding. Do not replace the owner under test with a mock.
- **Acceptance:** One event produces the contractually expected update count, at most one owned subscription is active, and disposal removes the exact callback. A fake proves application logic, not real platform callbacks.

## Earlier Request Overwrites Newer Results

- **Symptom:** A user changes a query, but the earlier response later replaces the new results.
- **Evidence:** Start A then B, complete B then A, and observe state. Derive expected ownership from the product contract; latest-wins is not universal for all operations.
- **Route:** ark-flow owns request/state coordination; ark-test controls completion order; ark-check summarizes evidence.
- **Action:** Test the real state owner with controllable I/O. Under fix authorization, use the project's existing request-identity or cancellation mechanism. Do not claim ignoring a response stops the underlying operation.
- **Acceptance:** For a latest-wins contract, B remains visible after A completes. Separately complete A while B is pending to confirm A cannot clear B's loading state; dispose before completion to confirm no revival. No fixed sleeps are needed for these controlled cases.
