# HarmonyOS Risk Boundaries

Use this reference when a change may affect configuration, packaging, devices, or user data.

## Protected Surfaces

Require explicit user approval before editing or generating changes for:

| Surface | Risk |
| --- | --- |
| Signing files and signing config | Can break install, update, release, or leak secrets. |
| Bundle name, app ID, client ID, metadata | Can change identity, service binding, or upgrade behavior. |
| SDK compatibility and API level | Can break devices or hide unavailable APIs. |
| Permissions in `module.json5` | Can affect review, privacy prompts, and runtime access. |
| Dependencies and lockfiles | Can change reproducibility, licensing, and build output. |
| Native build files and packaged libraries | Can break ABI, loading, or release artifacts. |
| Generated build output | Should normally be recreated, not manually edited. |
| Device, emulator, install, log, or service state | Mutates or observes runtime state outside source files. |
| Production constants and credentials | Can leak secrets or change real-world behavior. |

## Data Boundary

Classify every file or storage change before editing:

- Bundled resources: packaged with the app and read through resource APIs.
- Sandbox files: app-owned runtime files that can usually be recreated or migrated.
- User-visible exports: files the user or another app may depend on.
- Cache: rebuildable data with a cleanup policy.
- Durable user data: needs migration, recovery, and rollback thought.
- External storage or downloads: requires permission and clear failure behavior.

## Approval Note

When approval is needed, show the smallest intended config or command impact. Do not bundle sensitive config changes into unrelated UI or business-logic edits.

## Rollback

For source-only changes, rollback is a git revert. For permissions, dependencies, native packaging, user data migration, installation, or external service state, state the rollback path before changing it.
