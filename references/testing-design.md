# Test Design

Load when writing or reviewing tests. Start with the behavior and the defect a test should detect, not a count of functions to cover.

## Contracts And Assertions

Use requirements, public interface documentation, protocol examples, or manually verified fixtures as the oracle. Never call the implementation or duplicate its algorithm to calculate its own expected result. A characterization test can document existing behavior without declaring it correct; distinguish intentional compatibility from a suspected bug.

Observe public outputs, state transitions, persisted effects, or resource contracts. Private helpers, source text, constants, and framework internals do not need tests merely because they exist. Internal refactoring that preserves the contract should not break the tests. Use a table of independently derived inputs and expected results when cases share a contract.

Select the intended outcome, relevant failure, and contract-specific edge conditions. Do not manufacture tests for trivial wording changes, chase an arbitrary coverage number, or weaken an assertion to hide a failure.

## Dependencies And Isolation

Execute the real production unit. Replace the unavailable or nondeterministic boundary, not the behavior being tested. Understand the dependency's side effects before faking it; a fake must not silently omit state needed by the test. Do not copy the production algorithm into a test double.

Calls and arguments are valid assertions when they are the contract: a subscription occurs once, a write uses the correct key, or cleanup removes the exact listener. Checking only that a mock exists or returns its configured value proves nothing about production behavior. Pair interaction assertions with outcomes where those outcomes matter.

Use disposable data and existing injection points. Reset singleton state, listeners, timers and temporary resources after each case, including failure paths. Keep test helpers in test sources; do not expose private state or add production reset methods solely for tests. If isolation requires a production change, identify the smallest boundary and obtain scope for that change first.

## Async And Lifecycle

Control clocks, events, and Promise completion order through project-supported facilities. Assert transitions after explicit completion signals; use bounded condition waits for real runtime behavior. Fixed sleeps, unlimited polling, and retries until green hide defects.

| Contract | Controlled sequence | Observable assertion |
| --- | --- | --- |
| Latest request wins | Start A, start B, complete B, complete A | B remains visible; A's cleanup cannot clear B's pending state. |
| Disposal ends ownership | Start work, dispose owner, complete work | No state revival or new subscription; owned resources remain released. |
| Partial initialization cleans up | Acquire first resource, fail the next acquisition | First resource released once; retry does not duplicate ownership. |
| Retry is bounded | Supply eligible failures under a controlled clock | Attempts stop at the contract limit; ineligible failures are not retried. |

For flaky tests, retain the failing sequence, environment and any random seed. Distinguish shared state, timing assumptions, external-service instability and a product race. Repeated execution is justified to reproduce a timing defect, not to erase a failure from the report.

## Prove Sensitivity

For regressions, observe the expected assertion fail on the faulty behavior and pass after the authorized fix when feasible. A compile/import failure is not reproduction of the behavior defect. Never reset or overwrite user changes to obtain a baseline; use an isolated copy or record unavailable baseline evidence.

When useful, introduce one contract-breaking mutation in a disposable copy to check the assertion. Never mutate the user's working production file for this experiment. If the mutant survives, inspect the assertion; an equivalent mutation is not evidence of a weak test. Full mutation campaigns are not the default.

Property tests are optional when a meaningful rule exists: normalization is idempotent, serialization roundtrips preserve specified fields, or a transformation preserves an invariant. Define the valid input domain and any tolerance first. Reuse a compatible existing library; do not assume TypeScript libraries run in ArkTS. Without one, prefer ordinary boundary cases and propose a dependency only if the specific benefit warrants it. Preserve seed and minimized counterexample; classify a failure as code defect, wrong property, or unclear contract. Filtering away all inputs is not success, and fixed examples are not a generator-based campaign.

## Design References

Further reading, not required skills or runtime dependencies: [Superpowers test quality](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/writing-good-tests.md), [Matt Pocock TDD](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md), and [Trail of Bits property testing](https://github.com/trailofbits/skills/tree/main/plugins/property-based-testing). Apply this package's authorization and platform boundaries rather than importing another workflow's mandatory approvals or toolchain.
