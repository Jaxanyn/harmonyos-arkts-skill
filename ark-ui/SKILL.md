---
name: ark-ui
description: Implement or modify ArkUI pages and components, including state, layout, navigation, lifecycle, controllers, listeners, timers, stale-result handling, and cleanup, with explicit state and lifecycle evidence.
---

# Ark UI

Keep user-visible state local, lifecycle work removable, and rendering aligned with the project's existing ArkUI pattern.

For decorator or lifecycle semantics use [official-document-evidence.md](../references/official-document-evidence.md). Determine V1/V2 per affected component/model separately from the ArkTS language version. Use `$ark-language` for compiler-only syntax or type adaptation; keep state propagation, ownership, and runtime UI behavior in this skill. A same-named or similar V2 decorator is not automatically a behavior-equivalent replacement.

## Implement

1. Inspect the page/component's existing decorators, state owner, navigation path, controllers, listeners, and error presentation before adding another mechanism.
2. Choose the smallest owner for each new user-visible fact: component for transient UI, page or existing ViewModel for coordination, existing preference boundary for cross-page preference, and service/repository plus the existing state owner for remote or durable data.
3. Keep rendering and direct interaction in components; put coordination and non-UI transitions in the existing ViewModel or manager.
4. Register listeners, timers, callbacks, controllers, and observers at the owner that can remove them. Make re-entry initialization idempotent and ignore completions belonging to an obsolete page or request.
5. When decorator semantics, lifecycle behavior, API compatibility, or platform widgets are material, verify them through the official documentation lookup before changing the code.

## Acceptance

For a UI change, define the observable runtime behavior before verification:

- Initial screen state.
- User action or lifecycle event.
- Expected visible result.
- Failure or empty state if applicable.
- Re-entry, disposal, or stale-completion behavior when async work exists.

## Deliver: State/Lifecycle Ledger

For each added or changed user-visible state, report:

| Fact | Owner and existing decorator/pattern | Initialized by | Cleared or disposed by | Stale-result handling |
| --- | --- | --- | --- | --- |

Also report changed UI files, evidence profile, any official constraint used, and whether `$ark-check` is required. Read [arkui-and-architecture.md](../references/arkui-and-architecture.md) when ownership crosses component, page, and service boundaries. Completion requires every new registration and asynchronous completion to have an owner and an exit path.
