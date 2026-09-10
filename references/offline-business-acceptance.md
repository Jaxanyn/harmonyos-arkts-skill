# Offline Business Acceptance

Use with ark-test to define assertions and ark-check to execute the selected scope. Reuse project UI, tests and device tools; do not add production test backdoors. Offline is a scenario precondition, not an inference from a local-looking map.

## Establish Evidence

Record operator-confirmed or tool-observed WLAN/mobile-data state and its time, application target, installed artifact provenance, local dataset identity when available, and the test boundary (service, UI or both). A previous online pass is not an offline pass. A force-stop/relaunch checks process restart with existing data; it does not prove first installation or absence of caches. Preserve user network preferences and leave restoration instructions when the operator changed them.

## Select Bounded Scenarios

| Scenario | Independent expectation | Evidence and cleanup |
| --- | --- | --- |
| Query recovery | A known valid query matches an agreed fixture, an absent value yields an explicit empty state, and the valid query restores the same result | Save first/empty/restored outputs; confirm actual input text after automation, since input injection can append rather than replace |
| Persistence | One unique test record can be inserted, read, updated, read after process restart, deleted, and remains absent after another restart | Save the record identity and cleanup steps before mutation; compare visible historical fields or database snapshots within the declared scope |
| Map coverage | Known covered samples render at selected scales; documented missing coverage is distinguished from decoding, I/O or renderer failure | Save region, scale, tile identifiers, local-read/missing/error signals and screenshots; restore a usable viewport |

Do not hardcode one project's route name, expected segment count, file path, device key or existing user records into the reusable skill. The application owner defines which external database must remain authoritative; preserve that storage contract. Do not silently copy it into a sandbox and call external-file compatibility passed. Account for resource closing and database locking; concurrent external writers are a separate test.

## Interpret Results

- SDK authorization messages are independent evidence. They are not an automatic offline-business blocker and successful offline samples do not prove all SDK functions are authorization-independent.
- Code-defined camera limits are not an inventory of actual tiles. Reaching UI zoom limits or panning through a few regions does not establish complete geographic coverage. Mark exact dataset edges blocked/unverified when no trusted manifest/index is available.
- Query UI output and service output are separate assertions. A row count or successful handler does not verify rendering; screenshots do not establish data accuracy without an expected source.
- Record pass, failure, blocked prerequisites and unexecuted scope per scenario. Failed collectors, unconfirmed inputs or uncertain cleanup cannot be marked passed. Preserve partial evidence and prioritize removing only agent-created test records.
- Test cleanup can leave SQLite sequence increments or ordinary application preference changes. Do not reset counters or overwrite entire databases to manufacture byte-identical cleanup.
- A byte-limited capture and device-side dropped lines leave an incomplete observation window. Record both; use shorter bounded captures for reproduction rather than removing limits or treating absent errors as proof. A white map screenshot alone cannot distinguish missing tiles from renderer failure.
- Inspect the actual fallback payload and all callers rather than trusting comments such as "transparent". Check whether request/read logs stop after an initial quota and whether missing data, I/O errors and invalid coordinates share a silent fallback. A complete capture with no errors still cannot prove those branches were not taken. Request a matching dataset index before concluding that coverage or zoom limits caused the image.
- Separate archive index presence, successful extraction and actual image content. Valid high-zoom tiles can themselves be white or sparse. Inspect bounded original samples and match them to observed viewport requests before assigning a root cause; an arbitrary sample does not explain an entire screen. A portable-device path shown by the desktop file manager is not necessarily an HDC shell path; use an available read-only transfer interface and preserve the originals.
- When initial logs cannot identify the viewport, add only authorized bounded diagnostics at the existing tile entry point. Sample by zoom so startup requests cannot exhaust all later evidence; record coordinates, return size and data/fallback outcome without changing rendering. Verify the on-device log format before trusting camera values. Match original samples to the observed requests, distinguish equal byte length from content identity, and keep unsampled tiles explicit.

## Local Report

Record target and network evidence, expected/actual observations, evidence links, test-record cleanup, historical-data comparison scope, SDK diagnostics with business impact, and remaining gaps. Keep project-specific reports private and outside the distributed skill. Maintain the raw device report unchanged; put manually verified business assertions in a companion report rather than upgrading every CLI stage to passed.
