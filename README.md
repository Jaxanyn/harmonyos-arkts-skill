# Ark

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="HarmonyOS" src="https://img.shields.io/badge/HarmonyOS-Stage%20Model-red.svg">
  <img alt="ArkTS" src="https://img.shields.io/badge/ArkTS-Agent%20Workflow-2f80ed.svg">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827.svg">
</p>

<p align="center">
  <strong>Turn pure-native HarmonyOS app changes into scoped, documented, and verified agent workflows.</strong>
</p>

<p align="center">
  <a href="#zh-cn">中文</a> · <a href="#english">English</a>
</p>

---

<details open>
<summary id="zh-cn"><strong>中文</strong></summary>

## 一句话

Ark 把纯血鸿蒙 Stage 模型项目的改代码工作变成有边界、有证据、可验证的 Agent 工作流。它不复述官方 API，也不替代 DevEco CLI，而是把项目事实、官方约束、Native/NDK 边界、构建/设备证据放进同一条安全变更链路。

```text
Discover -> Change -> Verify
ark-scan -> ark-ui / ark-flow / ark-kit / ark-native -> ark-check
```

## Why Ark?

| 工具 | 回答的问题 |
| --- | --- |
| 官方文档 MCP | 平台规则、API 约束、权限、生命周期、Native/NDK 和兼容性是什么？ |
| DevEco CLI / 项目命令 | 构建、安装、日志和设备上实际发生了什么？ |
| Ark | 在这个具体项目里，应该怎么安全修改、验证和归因失败？ |

## 它有什么不同？

多数鸿蒙工具回答“API 怎么用”。Ark 回答“这个项目里应该怎么安全地改”。它把 Agent 最容易忽略的项目边界、配置风险、异步状态、平台约束、Native 边界和验证证据放进同一套工作流里。

| 没有 Ark | 使用 Ark |
| --- | --- |
| Agent 直接改文件 | 先扫描项目边界和调用链 |
| API 靠记忆或搜索片段判断 | 平台约束走官方文档或当前 SDK |
| 权限、SDK、签名、依赖等配置风险被顺手改掉 | 配置风险单独标记并先请求确认 |
| Native、CMake、so 加载问题和 ArkTS 类型问题混在一起 | 按跨语言契约定位导出、声明、构建和运行时 |
| 构建和真机结果混在描述里 | 验证证据、剩余风险单独说明 |
| 失败后继续试错式改代码 | 按失败信号回到对应命令 |

## 适合用在

- 接手陌生 HarmonyOS NEXT / 纯血鸿蒙 Stage 项目，先识别模块、调用链和安全边界。
- 修改 ArkUI 页面、状态、导航、生命周期和异步 UI 更新。
- 梳理 ViewModel、service、repository、缓存、加载、失败和重试链路。
- 接入权限、存储、网络、WebView、定位、通知、MapKit、蓝牙、媒体等 HarmonyOS Kit 能力。
- 处理 Node-API、C/C++、CMake、ABI、so 加载和三方 Native 库。
- 为构建、安装、日志、真机验证和失败归因建立最小充分验证路线。

## 核心价值

| 价值 | 说明 |
| --- | --- |
| Project-first | 先看项目结构和变更边界，再决定怎么改。 |
| Evidence-aware | 区分本地事实、官方文档约束、配置风险和运行时证据。 |
| Contract-driven | UI、业务流、平台能力和 Native 工作都以明确契约交付。 |
| Verification-led | 每次非平凡改动都能说明验证过什么、还剩什么风险。 |
| General-purpose | 服务公司、单位和个人的通用纯血鸿蒙 App，不绑定某个行业或项目。 |

## 命令矩阵

| 命令 | 核心作用 | 开发者收益 |
| --- | --- | --- |
| `ark` | 总入口，选择扫描、UI、业务流、Kit、Native 或验证路径。 | 模糊需求快速落到正确执行面。 |
| `ark-scan` | 扫描结构、调用链、受保护配置、库边界和改动边界。 | 接手项目先拿到可改地图。 |
| `ark-ui` | 处理 ArkUI 状态、导航、生命周期和渲染副作用。 | 减少状态漂移、泄漏和旧请求覆盖。 |
| `ark-flow` | 梳理 ViewModel、service、repository 和异步状态。 | 让加载、失败、取消、重试可追踪。 |
| `ark-kit` | 接入权限、存储、网络、WebView、定位、通知等能力。 | 同步处理官方约束、权限配置和设备行为。 |
| `ark-native` | 处理 Node-API、C++、CMake、ABI、so 和三方 Native 库。 | 让跨语言调用、构建、加载和崩溃归因更清楚。 |
| `ark-check` | 规划或执行构建、打包、安装、日志和设备验证。 | 明确验证证据、剩余风险和失败归因。 |

## 使用示例

| 场景 | 使用 |
| --- | --- |
| 不知道需求该从哪里下手 | `ark` |
| 接手陌生项目，先找边界 | `ark-scan` |
| 页面状态、导航或生命周期有风险 | `ark-ui` |
| 请求、缓存、失败流混乱 | `ark-flow` |
| 接入定位、网络、权限等平台能力 | `ark-kit` + `ark-check` |
| 修复 NAPI、CMake 或 so 加载问题 | `ark-native` + `ark-check` |

```text
用 ark 判断这个需求应该先扫描项目、改 UI、接 Kit、改 Native，还是先补验证。
```

```text
用 ark-ui 修改这个页面，并说明状态归属、生命周期清理和旧请求处理方式。
```

```text
用 ark-kit 和 ark-check 接入定位能力，并确认权限、配置、真机验证和剩余风险。
```

```text
用 ark-native 排查这个 libxxx.so 加载失败，并核对 ArkTS 声明、C++ 注册和 CMake 配置。
```

## 安装

```bash
npx skills@latest add Jaxanyn/harmonyos-arkts-skill
```

安装到 Codex 全局范围：

```bash
npx skills@latest add Jaxanyn/harmonyos-arkts-skill -a codex -g
```

更新后请刷新 skill 发现或重启 Codex。当前命令名是 `ark`、`ark-scan`、`ark-ui`、`ark-flow`、`ark-kit`、`ark-native`、`ark-check`。

如果你之前安装过旧版本，可能会看到旧命令名：`harmonyos-arkts-skill`、`arkts-scan`、`arkts-ui`、`arkts-flow`、`arkts-capability`、`arkts-verify`。建议更新后统一使用新的短命令。

## 不做什么

- 不缓存官方 API 表，平台事实以官方文档或当前 SDK 为准。
- 不写死 DevEco、本地 SDK、设备 ID 或证书路径。
- 不保存签名配置、账号、密钥、客户数据或生产常量。
- 不替代目标项目自己的业务规则和架构约定。
- 不把某个行业、公司或个人项目的私有规则做成默认模板。
- 不把未运行的真机或构建验证描述成已经验证。

## 许可证

MIT

</details>

---

<details>
<summary id="english"><strong>English</strong></summary>

## One-liner

Ark turns pure-native HarmonyOS Stage-model app changes into scoped, documented, and verified agent workflows. It does not copy official API docs or replace DevEco CLI; it puts project facts, official constraints, Native/NDK boundaries, and build/device evidence into one safe change loop.

```text
Discover -> Change -> Verify
ark-scan -> ark-ui / ark-flow / ark-kit / ark-native -> ark-check
```

## Why Ark?

| Tool | Answers |
| --- | --- |
| Official docs MCP | What are the platform rules, API constraints, permissions, lifecycle, Native/NDK, and compatibility limits? |
| DevEco CLI / project commands | What actually happened during build, install, logs, and device execution? |
| Ark | How should this specific project be changed, verified, and failure-triaged safely? |

## What makes it different?

Most HarmonyOS helpers answer "what is the API?" Ark answers "how should this project be changed safely?" It keeps the project boundary, config risk, async state, platform constraint, native boundary, and verification evidence in one workflow.

| Without Ark | With Ark |
| --- | --- |
| The agent edits files directly | It scans project boundaries and call paths first |
| APIs are judged from memory or snippets | Platform constraints come from official docs or the current SDK |
| Permission, SDK, signing, dependency, or config risk gets changed casually | Config risk is flagged and confirmed first |
| Native, CMake, shared-library loading, and ArkTS type issues blur together | Cross-language contracts guide export, declaration, build, and runtime checks |
| Build and device results are buried in prose | Evidence and remaining risk are reported explicitly |
| Failures lead to trial-and-error edits | Failures route back to the owning command |

## Best for

- Mapping an unfamiliar HarmonyOS NEXT / pure-native Stage project before editing.
- Changing ArkUI pages, state, navigation, lifecycle, and async UI updates.
- Shaping ViewModel, service, repository, cache, loading, failure, and retry flows.
- Integrating HarmonyOS Kit capabilities such as permissions, storage, networking, WebView, location, notifications, MapKit, Bluetooth, and media.
- Handling Node-API, C/C++, CMake, ABI, shared-library loading, and third-party native libraries.
- Planning the smallest sufficient build, install, log, device, and failure-triage verification path.

## Core Value

| Value | Meaning |
| --- | --- |
| Project-first | Inspect structure and edit boundaries before changing code. |
| Evidence-aware | Separate local facts, official constraints, config risk, and runtime evidence. |
| Contract-driven | Deliver UI, async flow, platform capability, and native work as explicit contracts. |
| Verification-led | State what was verified, what remains risky, and who owns failures. |
| General-purpose | Support company, organization, and individual pure-native HarmonyOS apps without binding to one domain. |

## Command Matrix

| Command | Core role | Developer benefit |
| --- | --- | --- |
| `ark` | Route work to scan, UI, flow, Kit, Native, or verification. | Turn broad requests into the right execution path. |
| `ark-scan` | Inspect structure, call paths, protected config, library boundaries, and edit boundaries. | Map safe changes before editing. |
| `ark-ui` | Handle ArkUI state, navigation, lifecycle, and render side effects. | Reduce state drift, leaks, and stale updates. |
| `ark-flow` | Shape ViewModel, service, repository, and async states. | Keep loading, failure, cancel, and retry paths traceable. |
| `ark-kit` | Integrate permissions, storage, networking, WebView, location, notifications, and platform APIs. | Align official constraints, permissions, config, and device behavior. |
| `ark-native` | Handle Node-API, C++, CMake, ABI, shared libraries, and third-party native code. | Clarify cross-language calls, builds, loading, and crash triage. |
| `ark-check` | Plan or run build, package, install, log, and device verification. | Show evidence, remaining risk, and failure ownership. |

## Usage Examples

| Scenario | Use |
| --- | --- |
| You do not know where the task should start | `ark` |
| You inherited an unfamiliar project | `ark-scan` |
| Page state, navigation, or lifecycle is risky | `ark-ui` |
| Request, cache, and failure flow is messy | `ark-flow` |
| You are integrating location, network, permissions, or another platform capability | `ark-kit` + `ark-check` |
| You are fixing Node-API, CMake, or shared-library loading | `ark-native` + `ark-check` |

```text
Use ark to decide whether this task should start with project scanning, UI work, Kit integration, Native work, or verification.
```

```text
Use ark-ui to change this page and report state ownership, lifecycle cleanup, and stale request handling.
```

```text
Use ark-kit and ark-check to integrate location, then verify permissions, config, device behavior, and remaining risk.
```

```text
Use ark-native to triage this libxxx.so loading failure and check ArkTS declarations, C++ registration, and CMake config.
```

## Installation

```bash
npx skills@latest add Jaxanyn/harmonyos-arkts-skill
```

Install globally for Codex:

```bash
npx skills@latest add Jaxanyn/harmonyos-arkts-skill -a codex -g
```

After updating, refresh skill discovery or restart Codex. The current command names are `ark`, `ark-scan`, `ark-ui`, `ark-flow`, `ark-kit`, `ark-native`, and `ark-check`.

Older installs may still show the previous names: `harmonyos-arkts-skill`, `arkts-scan`, `arkts-ui`, `arkts-flow`, `arkts-capability`, and `arkts-verify`. Prefer the new shorter names after updating.

## Non-goals

- Do not cache official API tables; platform facts should come from official docs or the current SDK.
- Do not hard-code DevEco, local SDK, device ID, or certificate paths.
- Do not store signing configuration, accounts, secrets, customer data, or production constants.
- Do not replace the target project's own business rules and architecture conventions.
- Do not turn one industry, company, or personal project into a default template.
- Do not report unrun build or device checks as verified.

## License

MIT

</details>
