---
name: ark-native
description: Implement or debug HarmonyOS Native/NDK boundaries for Stage-model projects, including Node-API exports, ArkTS type declarations, CMake, ABI, shared libraries, native async work, memory ownership, and third-party library licensing.
---

# Ark Native

Treat Native/NDK work as a cross-language contract. The ArkTS caller, type declaration, native export, build file, packaged library, and runtime loader must agree.

## Inspect

1. Locate the ArkTS import and its `.d.ts` declaration before editing C++ or CMake.
2. Locate `CMakeLists.txt`, native source files, generated library name, module dependency, and package configuration that loads the library.
3. Check whether the change affects ABI, exported symbols, Node-API registration, async work, threads, memory ownership, file handles, native resources, or third-party licenses.
4. Verify official Native/NDK or Node-API behavior when API level, registration, threading, or packaging semantics constrain the change.
5. Mark build configuration, dependencies, lockfiles, generated outputs, signing, and packaged native artifacts as protected surfaces that need explicit user approval before mutation.

## Implement

1. Keep the public ArkTS API narrow and typed. Return stable objects or promises rather than leaking native implementation details.
2. Keep `.d.ts` declarations, ArkTS imports, exported property names, and C++ registration names synchronized.
3. For `napi_create_async_work` or equivalent async native work, define input capture, worker execution, completion, promise resolution or rejection, cleanup, and cancellation limitations.
4. Return project-consistent error objects or rejected promises. Do not hide native failures behind empty catch blocks when the caller needs to recover.
5. Isolate third-party native code behind a small adapter and record license, source, version, and redistribution constraints when relevant.

## Failure Routing

| Failure signal | First check |
| --- | --- |
| ArkTS import or type error | Module dependency, `.d.ts`, exported names, and import path |
| Build or link failure | `CMakeLists.txt`, source list, include path, library name, ABI, and toolchain output |
| Runtime load failure | Packaged library name, module dependency, registration function, and device ABI |
| Native crash or hang | Threading, async completion, buffer lifetime, file handles, and ownership transfer |
| Wrong result crossing boundary | Serialization, encoding, numeric range, ArrayBuffer lifetime, and error contract |
| License concern | Third-party notice, redistribution terms, source obligations, and product license fit |

## Acceptance

For a native change, define:

- ArkTS caller and public type contract.
- Native export, registration, and build target.
- Threading and resource ownership rule.
- Error and unavailable-library behavior.
- Build or runtime evidence required for the changed surface.

## Deliver: Native Contract

Report ArkTS entry point, declaration file, native implementation file, build file, evidence profile, public contract, ownership and cleanup rule, failure behavior, protected surfaces, and required verification. Completion requires every cross-language name and data shape to be accounted for.
