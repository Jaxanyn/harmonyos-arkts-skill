# Ark

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="HarmonyOS" src="https://img.shields.io/badge/HarmonyOS-Stage%20Model-red.svg">
  <img alt="ArkTS" src="https://img.shields.io/badge/ArkTS-Agent%20Workflow-2f80ed.svg">
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent-Skill-111827.svg">
</p>

<p align="center">
  <strong>General-purpose HarmonyOS Stage / ArkTS skills for project discovery, implementation, and evidence-based verification.</strong>
</p>

<p align="center">
  <a href="#zh-cn">中文</a> · <a href="#english">English</a>
</p>

---

<details open>
<summary id="zh-cn"><strong>中文</strong></summary>

## 一句话

Ark 是面向鸿蒙开发工程师的通用 HarmonyOS Stage / ArkTS Agent Skill 包，包含一个总入口和八个专项技能，覆盖项目扫描、语言适配、ArkUI、异步数据流、系统能力、Native/NDK、测试与缺陷发现和验证规划。不绑定特定行业、公司或业务项目，也不替代官方文档、SDK 或 DevEco 工具。

## 快速开始

完整安装后，将目标项目与具体需求交给 Agent；不确定选哪个技能时使用 `ark`：

```text
用 ark 分析当前鸿蒙项目，识别模块、SDK 和本次需求的影响范围，给出需要使用的专项技能。先只读分析，不修改文件、不运行测试或构建。
```

这些名称是 Skill 入口，不是终端命令。支持显式技能调用的宿主可使用 `$ark`；其他宿主可直接读取本包的 `SKILL.md`，再按其中链接加载专项指导。

```text
Discover -> Implement and test as needed -> Verify
ark-scan -> ark-language / ark-ui / ark-flow / ark-kit / ark-native <-> ark-test -> ark-check
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
| `ark` | 总入口，选择扫描、语言、UI、业务流、Kit、Native、测试或验证路径。 | 模糊需求快速落到正确执行面。 |
| `ark-scan` | 扫描结构、调用链、受保护配置、库边界和改动边界。 | 接手项目先拿到可改地图。 |
| `ark-language` | 处理 ArkTS 语法、类型、导入、装饰器编译问题与 TS 适配。 | 按实际 SDK 修复语言约束，保留业务行为和公共接口。 |
| `ark-ui` | 处理 ArkUI 状态、导航、生命周期和渲染副作用。 | 减少状态漂移、泄漏和旧请求覆盖。 |
| `ark-flow` | 梳理 ViewModel、service、repository 和异步状态。 | 让加载、失败、取消、重试可追踪。 |
| `ark-kit` | 接入权限、存储、网络、WebView、定位、通知等能力。 | 同步处理官方约束、权限配置和设备行为。 |
| `ark-native` | 处理 Node-API、C++、CMake、ABI、so 和三方 Native 库。 | 让跨语言调用、构建、加载和崩溃归因更清楚。 |
| `ark-test` | 规划、编写、诊断测试，按风险开展全项目缺陷发现。 | 形成有效回归测试，区分已复现 Bug、疑似问题与未验证风险。 |
| `ark-check` | 规划或执行构建、打包、安装、日志和设备验证。 | 明确验证证据、剩余风险和失败归因。 |

## 测试与全项目缺陷发现

[ark-test](ark-test/SKILL.md) 支持测试规划、编写回归测试、测试诊断和全项目缺陷发现四种模式。复用现有测试设施，控制异步顺序，使用独立预期值；规划和只读审查不修改或执行。测试编写或全项目模式可在现有环境中补测试并执行聚焦检查，不默认修复生产代码或改变依赖、配置和设备状态。

全项目模式先建立模块和流程地图，再运行适用的已有测试，按风险选择有限范围补测。报告已复现 Bug、疑似问题和未验证风险；零用例、模板测试或主机模拟通过都不能证明整个项目或真实设备没有 Bug。范围和预算限制覆盖广度，不改变证据标准。

ark-test 可在修复前复现 Bug，也可在已有功能上补测试，并直接运行获授权的聚焦用例；ark-check 汇总整体验证，复用当前结果。只运行已有检查时直接使用 ark-check，不需要依次调用所有技能。

```text
用 ark-test 给当前模块补回归测试，复用现有设施，覆盖相关失败和异步边界；只修改测试并运行聚焦用例。
用 ark-test 对整个项目进行缺陷发现，先扫描并建立测试基线，再按风险补测试。只修改测试文件，不修复生产代码；报告已复现 Bug、疑似问题和未覆盖范围。
```

参考：[测试设计](references/testing-design.md)、[鸿蒙环境适配](references/testing-harmony.md)、[全项目测试](references/testing-project-sweep.md)。新增测试模式的 Agent 行为验收与真实项目试跑尚未执行，包结构检查不代表这些能力已经实测。

## UI、数据流与系统能力

`ark-ui` 增强导航输入与返回、状态传递、隐藏与销毁的区别、窗口适配、无障碍和列表复用规则；`ark-flow` 增强过期请求收尾、重试幂等性、缓存分页、事务与迁移恢复；`ark-kit` 增强权限拒绝/撤销、设备不支持、后台任务、资源归属和导出清理。规则按改动范围加载，不要求每个任务引入新缓存、队列或管理器。

对应参考：[UI 与架构](references/arkui-and-architecture.md)、[异步数据一致性](references/async-data-consistency.md)、[平台能力](references/platform-capabilities.md)。

## 语言与文档查询

新增的 `ark-language` 负责 ArkTS 源码生成、编译诊断和局部 TypeScript 适配。它分别识别应用 `.ets`、TS/JS 互操作、声明文件与构建脚本，不把应用代码规则强加给整个仓库；也不将 ArkUI V1/V2 等同于 ArkTS 语言版本。

所有分支复用 [官方文档证据规范](references/official-document-evidence.md)：优先使用已配置的官方文档工具，缺失时查询官方网页，并与项目 SDK 声明交叉核对。记录版本、符号、出处与影响决策的约束；离线或来源冲突时明确未知，不猜 API、不自动升级 SDK。该规范不新增 `ark-docs` 命令，也不要求安装特定 MCP。

```text
用 ark-language 分析这个 ArkTS 编译错误，按当前项目 SDK 修复类型和导入问题，保留原有行为。
```

## 构建排障与工程案例

当 IDE 能构建但终端失败时，ark-scan 先比较命令来源、实际工具和构建目标，ark-check 再按授权执行检查。按环境、配置、依赖、源码和测试区分首个有效错误，避免误改业务代码。优先复用项目启动方式，不自动修改全局环境、升级 SDK 或替换签名。

官方文档查询按 API 用法、编译诊断、旧 API 迁移和离线冲突四条路径展开；结论仍使用同一份来源与版本记录。需要补回归或全项目测试时，ark-scan 可转到 ark-test；只执行已有检查时转到 ark-check。

参考：[构建环境诊断](references/build-environment.md)、[四个中性工程案例](references/engineering-examples.md)。案例涵盖 Java 启动失败、目标不一致、重复订阅和异步乱序，是流程说明，不是已执行验证。

```text
用 ark 分析 IDE 能构建、终端失败的原因，比较实际工具和目标。只诊断，不运行构建或修改环境。
用 ark-scan 定位重复订阅的责任边界，给出交给 ark-test 的回归测试建议。先只读分析。
```

## 支持范围与验证状态

| 范围 | 当前约定 |
| --- | --- |
| 项目模型 | 面向原生 HarmonyOS Stage / ArkTS 项目；不把 FA、Flutter、React Native、Web 或后端项目自动迁移到此流程。 |
| SDK 与 API | 以目标项目实际 SDK、工具链和官方文档为准，不承诺覆盖所有版本；ArkUI V1/V2 不等于 ArkTS 语言版本。 |
| 离线或无设备 | 可以分析已有源码、配置和本地 SDK 声明；缺失的官方依据、设备行为和运行结果必须标为未知或未执行。 |
| 宿主与脚本 | 需要能读取本地 Markdown 的 Agent；可选脚本以 Python 3.10+ 标准库为目标，不强制特定 MCP。 |
| 当前验证状态 | 最近的语言、UI、数据流和系统能力内容更新未执行验收、测试或构建。已有测试文件不代表当前版本通过，历史脚本结果也不证明模型或设备行为。 |

## 扫描工具

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
| ArkTS 类型、导入或编译诊断需要处理 | `ark-language` |
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

建议按完整包安装。把以下要求交给支持本地 Skill 的 Agent：

```text
请从 https://github.com/Jaxanyn/harmonyos-arkts-skill 安装完整 Ark 技能包。
保留根 SKILL.md、全部 ark-* 子目录、references、scripts 和 tests 的相对布局。
按当前宿主支持的技能目录安装；如已有安装，先保留本地修改和备份，不覆盖其他技能。
```

完整包布局如下；目录名 `ark/` 表示安装后的包根目录：

```text
ark/
  SKILL.md
  ark-scan/SKILL.md
  ark-language/SKILL.md
  ark-ui/SKILL.md
  ark-flow/SKILL.md
  ark-kit/SKILL.md
  ark-native/SKILL.md
  ark-test/SKILL.md
  ark-check/SKILL.md
  references/
  scripts/
  tests/
```

第三方安装器是否保留共享资源、是否发现嵌套技能，取决于其实现，本包未完成跨安装器验证。若宿主只发现根入口，可通过 `ark` 读取子技能，不要求九个入口都独立显示。

更新时从远程仓库取得同一修订的完整包，先处理本地自定义改动，再整体更新；不要混用不同版本的子技能和共享参考。若安装目录本身是 Git 克隆且工作区干净，可在该目录执行 `git pull --ff-only`；有本地修改或分支分叉时先停止并处理差异，不强制覆盖。

更新后请刷新 Agent 宿主的 Skill 发现，或重启对应宿主。当前命令名是 `ark`、`ark-scan`、`ark-language`、`ark-ui`、`ark-flow`、`ark-kit`、`ark-native`、`ark-test`、`ark-check`。

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

Ark is a general-purpose HarmonyOS Stage / ArkTS Agent Skill package for developers. One router and eight focused skills cover project discovery, language adaptation, ArkUI, async data flows, system capabilities, Native/NDK work, test authoring and bug discovery, and verification planning. It is not tied to an industry, company, or application and does not replace official documentation, SDKs, or DevEco tools.

## Quick Start

After installing the complete package, give the agent a target project and a concrete task. Start with `ark` when the appropriate branch is unclear:

```text
Use ark to inspect this HarmonyOS project, identify modules, SDK, and the scope of this task, and select the relevant skills. Read-only analysis first; do not edit files or run tests or builds.
```

These names are skill entrypoints, not shell commands. Use `$ark` where the host supports explicit skill invocation; otherwise read the bundled `SKILL.md` and follow its links to focused guidance.

```text
Discover -> Implement and test as needed -> Verify
ark-scan -> ark-language / ark-ui / ark-flow / ark-kit / ark-native <-> ark-test -> ark-check
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
| `ark` | Route work to scan, language, UI, flow, Kit, Native, testing, or verification. | Turn broad requests into the right execution path. |
| `ark-scan` | Inspect structure, call paths, protected config, library boundaries, and edit boundaries. | Map safe changes before editing. |
| `ark-language` | Handle ArkTS syntax, types, imports, decorator diagnostics, and scoped TS adaptation. | Follow the selected SDK while preserving behavior and public contracts. |
| `ark-ui` | Handle ArkUI state, navigation, lifecycle, and render side effects. | Reduce state drift, leaks, and stale updates. |
| `ark-flow` | Shape ViewModel, service, repository, and async states. | Keep loading, failure, cancel, and retry paths traceable. |
| `ark-kit` | Integrate permissions, storage, networking, WebView, location, notifications, and platform APIs. | Align official constraints, permissions, config, and device behavior. |
| `ark-native` | Handle Node-API, C++, CMake, ABI, shared libraries, and third-party native code. | Clarify cross-language calls, builds, loading, and crash triage. |
| `ark-test` | Plan, write and diagnose tests; organize risk-ranked project sweeps. | Catch regressions and distinguish reproduced bugs, suspicions and unverified risks. |
| `ark-check` | Plan or run build, package, install, log, and device verification. | Show evidence, remaining risk, and failure ownership. |

## Testing And Whole-Project Discovery

[ark-test](ark-test/SKILL.md) supports planning, test writing, test diagnosis and project sweeps. Reuse existing runners, independent expectations and controlled async ordering. Planning and read-only review do not edit or execute. Writing/sweep requests allow relevant test additions and focused runs in the existing environment, not automatic production fixes, dependency/config changes or device mutations.

A sweep inventories modules/flows, establishes applicable test baselines and selects a finite risk-ranked pass. Report reproduced bugs, suspected issues and unverified risks separately. Zero cases, template-only success or host simulation cannot prove a bug-free project or real-device behavior.

Test authoring may precede a fix or follow existing implementation. ark-test runs authorized focused tests; ark-check reuses current results for overall verification. Use ark-check directly when only running existing checks; not every task needs every skill.

```text
Use ark-test to add regression tests for this module using existing tooling. Cover relevant failures and async boundaries; edit tests only and run focused cases.
Use ark-test to find bugs across this project: map modules, establish the baseline, then add risk-ranked tests. Do not fix production code; report reproduced bugs, suspicions and untested boundaries.
```

References: [test design](references/testing-design.md), [HarmonyOS environment](references/testing-harmony.md), and [project sweeps](references/testing-project-sweep.md). Agent behavioral evaluation and real-project trials for these new modes have not been run; package checks do not establish that evidence.

## UI, Data Flows, And System Capabilities

`ark-ui` now covers navigation inputs/results, state propagation, visibility versus disposal, window adaptation, accessibility, and list reuse. `ark-flow` covers obsolete-request cleanup, retry idempotency, cache/paging consistency, transactions, and migration recovery. `ark-kit` covers denied/revoked grants, unsupported devices, background ownership, resource lifetimes, and export cleanup. Load only the affected guidance; these rules do not require new caches, queues, or managers for every change.

References: [UI and architecture](references/arkui-and-architecture.md), [async data consistency](references/async-data-consistency.md), and [platform capabilities](references/platform-capabilities.md).

## Language And Documentation Lookup

`ark-language` handles source generation, compiler diagnostics, and scoped TypeScript adaptation. It distinguishes application `.ets`, TS/JS interop, declarations, and build-tool TypeScript, and keeps ArkUI state-management generation separate from ArkTS language version.

All branches share [official-document evidence](references/official-document-evidence.md): discover a configured official documentation tool, fall back to official web references, and cross-check the selected SDK declarations. Record version, symbol, source, and the constraint affecting the decision. Offline or conflicting evidence stays explicitly unresolved; do not invent APIs or upgrade SDKs to reconcile it. No separate `ark-docs` command or mandatory MCP is added.

```text
Use ark-language to fix this ArkTS type/import diagnostic for the project's current SDK while preserving behavior.
```

## Build Diagnosis And Engineering Examples

When IDE and terminal builds disagree, ark-scan compares command provenance, actual tooling and intended targets; ark-check runs checks within authorization. Classify the first actionable error as environment, configuration, dependency resolution, source or test failure before editing. Prefer existing project launchers; do not automatically change global settings, upgrade SDKs or replace signing.

Documentation lookup now has paths for API usage, compiler diagnostics, deprecated API migration and offline conflicts, all using the same source/version evidence record. ark-scan routes regression authoring and project sweeps to ark-test, and existing-check execution to ark-check.

References: [build environment diagnosis](references/build-environment.md) and [four synthetic engineering examples](references/engineering-examples.md). Java startup failure, target mismatch, duplicate subscription and stale request examples illustrate workflows; they are not executed verification.

```text
Use ark to diagnose why the IDE builds but the terminal fails. Compare actual tools and targets; do not build or change the environment.
Use ark-scan to locate ownership of duplicate subscriptions and propose a regression handoff to ark-test. Read-only analysis first.
```

## Scope And Verification Status

| Area | Current boundary |
| --- | --- |
| Project model | Native HarmonyOS Stage / ArkTS projects; no automatic migration of FA, Flutter, React Native, web, or backend projects. |
| SDK and APIs | Follow the target project's SDK, toolchain, and official documentation; no all-version compatibility claim. ArkUI V1/V2 is not the ArkTS language version. |
| Offline or no device | Inspect available sources, config, and local SDK declarations. Missing official evidence, device behavior, and execution results remain unknown or not-run. |
| Host and scripts | An agent that can read local Markdown; optional scripts target the Python 3.10+ standard library. No specific MCP is required. |
| Verification status | Recent language, UI, data-flow, and capability updates have not undergone acceptance, tests, or builds. Existing tests do not establish a passing current revision; historical script results do not validate model or device behavior. |

## Audit Tools

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
| ArkTS types, imports, or compiler diagnostics need attention | `ark-language` |
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

Install the complete package. Give a local Skill-capable agent these requirements:

```text
Install the complete Ark skill package from https://github.com/Jaxanyn/harmonyos-arkts-skill.
Preserve the root SKILL.md, all ark-* directories, references, scripts, and tests in their relative layout.
Use a skill location supported by this host. Preserve local edits and back up an existing installation without overwriting unrelated skills.
```

The installed package should retain this layout:

```text
ark/
  SKILL.md
  ark-scan/SKILL.md
  ark-language/SKILL.md
  ark-ui/SKILL.md
  ark-flow/SKILL.md
  ark-kit/SKILL.md
  ark-native/SKILL.md
  ark-test/SKILL.md
  ark-check/SKILL.md
  references/
  scripts/
  tests/
```

Shared-resource preservation and nested-skill discovery depend on the installer and host; cross-installer behavior has not been verified. A host exposing only the root skill can follow child instructions through `ark`; nine independently listed commands are not required.

For updates, obtain the complete package at one revision, preserve local customizations, and update it together. Do not mix child skills and shared references from different revisions. For a clean Git-based installation, run `git pull --ff-only` in its directory. Stop and reconcile local changes or divergent branches instead of forcing an overwrite.

After updating, refresh skill discovery in the Agent host or restart that host. The current command names are `ark`, `ark-scan`, `ark-language`, `ark-ui`, `ark-flow`, `ark-kit`, `ark-native`, `ark-test`, and `ark-check`.

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
