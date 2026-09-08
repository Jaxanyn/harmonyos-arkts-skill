# ArkUI And Architecture

## State Ownership

Choose the smallest owner that represents the user-visible fact.

| State | Owner | Pass Down As |
| --- | --- | --- |
| Local input, animation, temporary panel state | Component | `@State` or existing local pattern |
| Page coordination or navigation state | Page or its ViewModel | Explicit input, callback, or existing shared model |
| Cross-page preference | Existing application storage or preference wrapper | A single named key and access boundary |
| Remote or persisted domain data | Service/repository plus the existing state owner | Result model, not duplicated mutable copies |

Use the project's established decorator and state-management pattern. Do not introduce a second state system solely for one feature.

## Lifecycle

Register listeners, timers, location callbacks, controllers, and observers at the owner that can reliably remove them. Make initialization idempotent when a page or component can reappear. Distinguish visibility from destruction: pause visibility-scoped work on hiding and dispose owner-scoped registrations when their owner ends, using the applicable documented lifecycle. Ignore obsolete UI completions without abandoning cleanup of still-running work.

## Component Boundaries

Keep rendering and direct user interaction in components. Put coordination, non-UI state transitions, and business decisions in the existing ViewModel or manager layer. Put storage, parsing, and platform I/O behind services or adapters. Follow a local pattern when one exists; do not perform a broad reorganization as part of a feature request.

## Async Flow

For work visible to the user, make the flow legible:

1. Start from one owner and set the pending state.
2. Call the existing service or adapter.
3. Apply success only if the request is still current.
4. Surface failure through the project's existing message or error state.
5. Clear pending state on every terminal outcome only if that operation still owns the pending state.

Avoid hiding errors in logs when the user needs an action, and avoid showing raw platform error details in the UI when the project already has a safer message convention.

## State And Editing Contracts

For each changed fact identify its authoritative owner, consumers, update direction, and derived values. Verify whether mutations to nested objects or array items are observed by the actual decorators. Do not add a second mutable copy merely to force a refresh. Editable drafts are legitimate when cancel/revert and external-update conflicts have an explicit rule; saving must update the real owner once.

Avoid application-global storage for temporary component or per-window state. When windows or navigation stacks coexist, scope their selected item, controller, and pending request appropriately. Reuse established resource tokens, localized strings, and theme behavior rather than hardcoding a new visual system for a local feature.

## Navigation And Results

Inspect the current router or Navigation implementation, route registration and stack owner. Record input shape/defaults, invalid input behavior, result receiver, result delivery conditions, cancellation, and back interception where relevant. Keep route state authoritative in the existing navigation mechanism; do not infer a second route stack from lifecycle callbacks.

Prevent duplicate navigation from rapid taps and late completions after a caller has exited. Returning a selection should update the live requesting owner, not an unrelated global singleton. For dialogs, nested stacks, split layouts, or retained destinations, check visibility, ownership, and result delivery independently. Preserve drafts or unsaved work according to the existing product behavior rather than automatically discarding them on every back action.

## Responsive Layout And Accessibility

Use the available window/container space, established breakpoints, and actual supported devices. Orientation alone is insufficient for split-screen and resizable windows. Check the changed layout's minimum usable width, scrolling, safe areas, keyboard overlap, and focus visibility; do not let a page change silently alter app-wide window policy.

For interactive controls preserve meaningful labels, roles, focus order, disabled/selected states, and screen-reader information using SDK-supported APIs. Provide an accessible action when the changed behavior depends on a gesture. Account for enlarged text and localization in affected controls; avoid fixed heights that clip content and color-only status cues. Record which conditions remain unobserved when visual verification is excluded.

## Lists And Rendering Work

Choose item identity from stable data keys, not the changing list position, when reorder/filter/pagination can occur. Inspect the actual lazy/reuse mechanism before modifying it. Reused cells must reset transient state and reject late async results for their previous item. Cache derived data only with an explicit invalidation rule; do not add unbounded caches to reduce repeated rendering work.

Keep parsing, I/O, decoding, and expensive transformations outside rendering callbacks. Merely wrapping synchronous work in a Promise does not prove it moved off the UI thread. When performance is the requested outcome, state the measurement and target conditions; without an authorized measurement describe the change as a hypothesis, not an observed speedup.

## References And Handoffs

Use [official-document evidence](official-document-evidence.md) for specific lifecycle and component semantics. Huawei's [Navigation routing guide](https://developer.huawei.com/consumer/cn/doc/doccenter-capabilities/arkts-navigation-jump) is a lookup entry point, not a rule to migrate existing routing. Use [async data consistency](async-data-consistency.md) when loading, mutation, or caching crosses the component boundary.
