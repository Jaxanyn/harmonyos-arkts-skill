---
name: ark-flow
description: Implement HarmonyOS ArkTS layered async flows across ViewModels, services, repositories, DTOs, cache, parsing, loading, errors, navigation coordination, request identity, and stale-result handling.
---

# Ark Flow

Make each user-visible operation traceable from its trigger to its data source and terminal state.

Use [official-document-evidence.md](../references/official-document-evidence.md) when platform concurrency, persistence, or API semantics constrain the flow. Use `$ark-language` for type/import adaptation, preserving external input validation and the existing async/error contract. Do not treat a cast or DTO annotation as validation of network, storage, or Native data.

Determine whether the user requested implementation, diagnosis, or review. Preserve existing data stores, public contracts, and module boundaries. Read [async-data-consistency.md](../references/async-data-consistency.md) for the affected concurrency, cache, pagination, or persistence branch rather than applying every mechanism to every operation.

## Implement

1. Follow the project's established component -> ViewModel/manager -> service/adapter/repository boundary; introduce a new layer only when an existing boundary cannot own the responsibility.
2. Give every user-visible operation one state owner. It sets pending, initiates work, applies only the current result, surfaces a project-consistent failure, and clears pending on every terminal path that still owns that state. An older operation's finally block must not clear a newer operation's loading state.
3. Preserve DTO, domain model, cache key, logging, and error conventions. Validate external input at the adapter boundary.
4. Use request identity, cancellation, or the project's equivalent when repeated actions, navigation, refresh, searches, downloads, or tile loads can complete out of order.
5. Verify official API behavior when a platform API or compatibility rule changes the flow.

## Consistency Decisions

- **Operation state:** Separate initial load, refresh, pagination, mutation, empty success, recoverable failure, and cancellation when users need different behavior. Preserve visible data during refresh if that matches the product; do not introduce a universal state-machine framework for a local operation.
- **Concurrency and timeouts:** Choose latest-result, serialization, deduplication, or bounded parallelism according to the operation. A timeout or ignored response does not prove the underlying task stopped. Track operation identity through success, failure, and cleanup; a shared request should not be cancelled because only one subscriber disappeared.
- **Retries and writes:** Bound attempts and delay using the existing policy. Retry only eligible failures; never automatically retry a non-idempotent write unless the service provides an established deduplication/reconciliation contract. An ambiguous response can mean the server committed; represent uncertainty and reconcile rather than duplicating the mutation.
- **Cache and pagination:** Scope cache keys by all relevant query, account, permission, and schema inputs. Define freshness, invalidation, eviction, and logout behavior. Tie page cursors to a query generation; a refresh invalidates old page completions. Merge by stable identity and advance the cursor only after the page is accepted.
- **Durability:** Identify the invariant spanning writes and whether the selected store supports the required transaction. Keep external work outside a database transaction where possible. For schema/file migration define restart, partial failure, version switching, recovery, and data preservation. Do not clear user data, change storage technology, or add offline write queues as a side effect of a flow fix.

## Behavior To Specify

For an async or layered flow, define:

- Trigger and state owner.
- Pending, success, failure, and cancellation states.
- Stale-result rule for repeated or navigated-away requests.
- Data boundary: adapter, repository, service, cache, or parser.
- Public verification point closest to the changed behavior.

## Deliver: Async Contract

Report trigger, state owner, downstream call path, evidence profile, pending behavior, success behavior, failure behavior, stale-result behavior, and verification point. Completion requires every terminal path to be observable to the user or deliberately represented by the project's existing state model.

Include only applicable timeout/cancellation, retry/idempotency, cache/cursor, transaction/migration, and recovery decisions. Separate business results from sanitized diagnostics; cancellation should not automatically become an alarming user error. Hand platform restrictions to `$ark-kit`, Native worker ownership to `$ark-native`, and authorized verification to `$ark-check`. If checks are excluded, report the unobserved behavior without running them.
