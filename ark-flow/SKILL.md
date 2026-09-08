---
name: ark-flow
description: Implement HarmonyOS ArkTS layered async flows across ViewModels, services, repositories, DTOs, cache, parsing, loading, errors, navigation coordination, request identity, and stale-result handling.
---

# Ark Flow

Make each user-visible operation traceable from its trigger to its data source and terminal state.

Use [official-document-evidence.md](../references/official-document-evidence.md) when platform concurrency, persistence, or API semantics constrain the flow. Use `$ark-language` for type/import adaptation, preserving external input validation and the existing async/error contract. Do not treat a cast or DTO annotation as validation of network, storage, or Native data.

## Implement

1. Follow the project's established component -> ViewModel/manager -> service/adapter/repository boundary; introduce a new layer only when an existing boundary cannot own the responsibility.
2. Give every user-visible operation one state owner. It sets pending, initiates work, applies only the current result, surfaces a project-consistent failure, and clears pending on every terminal path.
3. Preserve DTO, domain model, cache key, logging, and error conventions. Validate external input at the adapter boundary.
4. Use request identity, cancellation, or the project's equivalent when repeated actions, navigation, refresh, searches, downloads, or tile loads can complete out of order.
5. Verify official API behavior when a platform API or compatibility rule changes the flow.

## Acceptance

For an async or layered flow, define:

- Trigger and state owner.
- Pending, success, failure, and cancellation states.
- Stale-result rule for repeated or navigated-away requests.
- Data boundary: adapter, repository, service, cache, or parser.
- Public verification point closest to the changed behavior.

## Deliver: Async Contract

Report trigger, state owner, downstream call path, evidence profile, pending behavior, success behavior, failure behavior, stale-result behavior, and verification point. Completion requires every terminal path to be observable to the user or deliberately represented by the project's existing state model.
