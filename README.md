# Ark

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="HarmonyOS" src="https://img.shields.io/badge/HarmonyOS-Stage%20Model-red.svg">
  <img alt="ArkTS" src="https://img.shields.io/badge/ArkTS-Agent%20Workflow-2f80ed.svg">
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent-Skill-111827.svg">
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

Ark 把纯血鸿蒙 Stage 模型项目的改代码工作变成有边界、有证据、可验证的通用 Agent 工作流。它不复述官方 API，也不替代 DevEco CLI，而是把项目事实、官方约束、Native/NDK 边界、构建/设备证据放进同一条安全变更链路。

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

## 只读扫描脚本

Ark 附带一个可选只读脚本，用于快速盘点 Stage 项目的模块、配置、权限、Kit import、测试和 Native 边界：

```bash
python scripts/audit_harmony_project.py /path/to/harmony/project
python scripts/audit_harmony_project.py /path/to/harmony/project --json
```
脚本只提供项目形状和风险面线索，不替代官方文档、构建、安装或真机验证。

`ark-scan` 现在区分嵌套生产模块与测试源集，分别记录 SDK 字段和组件状态管理线索；`ark-native` 补齐部分初始化失败、异步取消、资源释放和渲染表面重建；`ark-check` 将构建、测试、打包与运行时行为分别报告为通过、失败、阻塞、未执行或不适用。证据维度可同时适用，不用一个“最高等级”覆盖其他义务。

技能包的回归检查：`python -B -m unittest discover -s tests -p "test_*.py" -v`。测试采用临时合成工程，不需要鸿蒙 SDK；[行为验收场景](tests/skill-scenarios.md) 单独验证 Agent 决策。脚本测试通过不等于完成模型评测或真机验证。

发布公开 skill 前，可以运行隐私扫描，避免把本机路径、证书字段、密码字段或私有项目词写进通用 skill：

```bash
python scripts/check_skill_privacy.py .
python scripts/check_skill_privacy.py . --term 客户项目名
```

## 配置、数据和权限边界

Ark 本身无需额外配置、账号或密钥。它只读取目标项目中与当前任务有关的源文件、配置文件和公开文档线索；不会保存签名文件、证书、账号、密钥、客户数据、设备 ID 或生产常量。

构建、安装、真机/模拟器、日志、外部服务、依赖变更、权限变更、签名变更和 Native 构建面都属于高风险或外部状态边界。Agent 必须先说明最小影响范围并获得用户授权，再执行这些动作。

已有明确授权继续有效，不重复确认同一动作。只读发现与有界日志读取、构建产物生成、安装或卸载是不同的操作范围。扫描输出只报告敏感字段类别和位置，不回显命中的值；私有业务词由 `--term` 指定，不内置行业黑名单。

脚本兼容性以 Python 3.10+ 标准库为目标；已在当前 Windows 开发环境执行过静态校验和脚本帮助命令。macOS、Linux、不同 Agent 宿主、无 GUI 环境、无设备环境和离线环境属于未完整实测范围，应按实际宿主能力降级为只读扫描、静态检查或人工执行命令。

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

把仓库地址交给支持本地 Skill 的 Agent：

```text
请帮我安装这个 Skill：https://github.com/Jaxanyn/harmonyos-arkts-skill
```

也可以使用兼容的 Skill CLI：

```bash
npx skills add Jaxanyn/harmonyos-arkts-skill
```

更新后请刷新 Agent 宿主的 Skill 发现，或重启对应宿主。当前命令名是 `ark`、`ark-scan`、`ark-ui`、`ark-flow`、`ark-kit`、`ark-native`、`ark-check`。

安装时保留完整仓库布局：子 Skill 依赖上一级共享的 `references/`、`scripts/` 和 `tests/skill-scenarios.md`。若安装器只复制单个子目录，需要恢复同一版本的共享资源后再使用。不要将缺失资源生成到业务项目中。

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

Ark turns pure-native HarmonyOS Stage-model app changes into scoped, documented, and verified general Agent workflows. It does not copy official API docs or replace DevEco CLI; it puts project facts, official constraints, Native/NDK boundaries, and build/device evidence into one safe change loop.

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

## Read-Only Audit Script

Ark includes an optional read-only scanner for a quick inventory of Stage modules, config, permissions, Kit imports, tests, and native boundaries:

```bash
python scripts/audit_harmony_project.py /path/to/harmony/project
python scripts/audit_harmony_project.py /path/to/harmony/project --json
```
The script provides project-shape and risk-surface signals only. It does not replace official docs, builds, installs, or device verification.

`ark-scan` distinguishes nested production modules from test source sets and records separate SDK fields and component state markers. `ark-native` covers partial initialization failure, async cancellation, resource release, and surface recreation. `ark-check` separates build, test, package, and runtime claims into passed, failed, blocked, not-run, or not-applicable results. Evidence obligations can coexist.

Run package regression checks with `python -B -m unittest discover -s tests -p "test_*.py" -v`. Tests use temporary synthetic projects without a HarmonyOS SDK. [Behavioral acceptance scenarios](tests/skill-scenarios.md) evaluate agent decisions separately; passing script tests does not imply model or device validation.

Before publishing a public skill update, run the privacy scanner to catch local paths, signing fields, password fields, or private project terms:

```bash
python scripts/check_skill_privacy.py .
python scripts/check_skill_privacy.py . --term customer-project-name
```

## Configuration, Data, And Permissions

Ark itself requires no extra configuration, account, or secret. It reads only the target project's task-relevant source files, configuration files, and public documentation signals; it does not store signing files, certificates, accounts, secrets, customer data, device IDs, or production constants.

Builds, installs, device or emulator checks, logs, external services, dependency changes, permission changes, signing changes, and Native build surfaces are high-risk or external-state boundaries. The Agent must state the smallest impact and get user authorization before running those actions.

Existing explicit authorization remains valid. Read-only discovery, bounded log reads, generated build output, and installation/uninstallation are distinct scopes. Privacy findings show categories and locations only; private business terms are supplied with `--term`, with no built-in industry blacklist.

The bundled scripts target Python 3.10+ standard-library compatibility. Static validation and script help commands have been run on the current Windows development environment. macOS, Linux, other Agent hosts, no-GUI environments, no-device environments, and offline environments are not fully runtime-tested; use read-only scanning, static checks, or human-run commands when host capabilities are missing.

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

Give the repository URL to any local Skill-capable Agent:

```text
Please install this Skill: https://github.com/Jaxanyn/harmonyos-arkts-skill
```

Or use a compatible Skill CLI:

```bash
npx skills add Jaxanyn/harmonyos-arkts-skill
```

After updating, refresh skill discovery in the Agent host or restart that host. The current command names are `ark`, `ark-scan`, `ark-ui`, `ark-flow`, `ark-kit`, `ark-native`, and `ark-check`.

Preserve the complete repository layout: child skills depend on shared `references/`, `scripts/`, and `tests/skill-scenarios.md` one level above. If an installer copies only a child folder, restore shared resources from the same revision before use. Do not generate missing helpers inside the application project.

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
