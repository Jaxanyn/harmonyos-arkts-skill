# Async Data Consistency

Read only the branch relevant to the changed flow. These are design decisions to make within the existing architecture, not a requirement to add queues, caches, state frameworks, or databases. Platform API behavior must follow [official-document evidence](official-document-evidence.md).

## Operation Identity And State

Attach results to the operation that owns them, including failures and cleanup. When request A finishes after request B starts, A must not replace B's data, surface an obsolete error, or clear B's loading state. Account for page exit, account change, query change, and refresh as separate invalidation events when they affect ownership.

Choose concurrency semantics deliberately:

| Operation | Candidate policy | Failure to avoid |
| --- | --- | --- |
| Search or preview | Latest applicable result; optional cancellation/debounce. | Slow earlier response replacing the current selection. |
| Shared read | Deduplicate equivalent requests with subscriber ownership. | One consumer cancelling work still needed by another. |
| Ordered mutation | Serialize when order matters; use established server idempotency/reconciliation. | Reordering or duplicating writes after retries. |
| Batch import/download | Bounded parallelism with per-item status and explicit aggregate outcome. | Unbounded memory/work or one error masking completed items. |
| Refresh plus pagination | Query generation and cursor ownership. | An old page appending into newly refreshed data. |

Use the product's existing pending/success/empty/error/cancel representation. Background refresh failure need not erase previously valid data; show freshness and recovery when the user needs them. Avoid turning intentional cancellation into a noisy error. Do not assume that abandoning a Promise stops underlying work.

## Timeout, Retry, And Ambiguous Writes

Define an operation deadline and who clears its timer; use existing timeout values unless changing them is requested. Distinguish a transport timeout, user cancellation, stale-result discard, and a server business rejection. Late completions after a timeout still need resource cleanup.

Use bounded retry only for failures classified as retryable by the actual service contract. Preserve retry budgets and server backoff guidance when provided. Do not retry authorization/validation failures indefinitely. A timed-out write may already have committed: reuse the service's idempotency key/status query or another established reconciliation mechanism before resubmission. Do not invent a server deduplication contract from client-only code.

If optimistic UI is used, define rollback or reconciliation against later mutations. A failed earlier write must not revert a newer successful edit. Keep the pending intent distinguishable from confirmed server or durable state. Adding offline writes requires explicit conflict, replay, identity, expiry, and recovery decisions; an offline read fallback does not imply an offline write queue.

## Cache And Pagination

Cache keys must distinguish inputs affecting the result: account/tenant where applicable, query/filter/sort, permissions, locale, and schema/version. Keep scope proportional; do not store private data in a shared cache. Define freshness, capacity, eviction, invalidation after writes, logout/account switching, and stale-on-error behavior. Avoid adding a cache when the existing data owner already provides the required reuse.

Tie cursor/offset, filter/sort, and request generation together. Advance paging state only after accepting and merging the response; failed pages retain a retryable cursor. Use stable identity for deduplication and preserve ordering from the source contract. On refresh or query change, invalidate old completions. Do not infer end-of-list solely from an empty page unless the API contract defines that meaning.

## Transactions And Migration

Identify which writes form one invariant and whether the selected persistence API actually makes them atomic. UI state containers and preferences are not automatically transactional databases. Close result sets, connections, and file handles according to their ownership even when parsing or commit fails. Avoid long network work inside transactions; a local database transaction cannot atomically commit an external service or unrelated file store.

For multiple stores, use an existing recovery protocol or define a minimal staged operation with reconciliation before implementing it. For file replacement or schema migration, record the old/new version, validation before activation, interruption points, restart/idempotency, recovery source, and supported downgrade behavior. Do not delete the previous durable data merely because migration started or mark the version advanced before the new representation is usable. Rename/replace and durability guarantees depend on the actual filesystem/API and must be checked.

Preserve user data when a migration fails. If safe recovery cannot be established, leave the prior version active or report the blocker according to the project contract rather than wiping the database. Do not log record contents or identifiers unnecessarily while diagnosing recovery.

## Handoff

Report the invariant, operation owner, terminal states, stale-result rule, applicable retry/cache/cursor/durability decisions, and unobserved risks. Route platform store or concurrent-work API constraints to `$ark-kit`, rendering/state propagation to `$ark-ui`, and Native worker lifetime to `$ark-native`. Runtime and failure-path execution belong to authorized `$ark-check` scope; an implementation review alone does not prove concurrency or durability behavior.
