# Ark

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</p>

<p align="center">
  <strong>HarmonyOS Stage / ArkTS skills for development, migration, testing, and authorized device verification.</strong><br>
  HarmonyOS Stage / ArkTS 开发、迁移、测试与授权设备验证技能包。
</p>

<p align="center">
  <a href="#zh-cn">中文</a> · <a href="#english">English</a>
</p>

---

<details open>
<summary id="zh-cn"><strong>中文</strong></summary>

## 快速开始

Ark 面向原生 HarmonyOS Stage / ArkTS 工程，提供一个总入口和九个专项技能。

它复用项目现有架构，以官方文档、当前 SDK 和实际检查结果为依据。Ark 不绑定行业或业务项目，也不替代官方文档、SDK 或 DevEco 工具。

### 1. 选择入口

| 你的目标 | 建议入口 |
| --- | --- |
| 先理解工程或确定改动范围 | `ark` 或 `ark-scan` |
| 把 Android 功能迁移到鸿蒙 | `ark-migrate` |
| 补测试或发现缺陷 | `ark-test` |
| 在已连接真机上运行已签名工程并分析日志 | `ark` → `ark-check`，按需使用 `ark-project` |

### 2. 安装完整包

将以下要求交给支持本地 Skill 的 Agent：

```text
请从 https://github.com/Jaxanyn/harmonyos-arkts-skill 安装完整 Ark 技能包。
保留根 SKILL.md、全部 ark-* 子目录、references、scripts 和 tests 的相对布局。
安装到当前宿主支持的技能目录。保留已有修改，不覆盖其他技能。
```

### 3. 发起第一次请求

安装后，在目标项目中发起一次只读分析：

```text
用 ark 分析当前鸿蒙项目，识别模块、SDK 和本次需求的影响范围，建议下一步使用的技能。
先只读分析，不修改文件、不运行测试或构建。
```

结果应包含项目结构、影响范围和建议技能。这些名称是 Skill 入口，不是终端命令。支持显式调用的宿主可使用 `$ark`；其他宿主可读取根 [SKILL.md](SKILL.md)，再按链接加载专项指导。

<details>
<summary>设备验证：快速路径</summary>

### 在已连接真机上运行工程

此流程适用于标准、已配置签名的单 HAP Stage 工程。前置条件为已解锁且开启调试的 USB 真机，以及项目现有的 DevEco SDK、Hvigor 和依赖。流程会构建工程、覆盖安装 HAP 并启动应用，执行前确认这些操作已获授权。

Ark 技能包负责 Agent 的任务路由；`ark-device` / `ark-project` 是单独安装或从源码调用的本地 CLI，不会在加载技能时自动安装或运行。

从完整技能包的 `tools/ark-device/src` 目录执行：

```powershell
python -B -m ark_device doctor
python -B -m ark_device.project prepare --project "<工程绝对路径>"
python -B -m ark_device.project run --project "<工程绝对路径>" --seconds 30
```

`prepare` 只读取工程配置并显示识别出的模块和 Ability；`run` 生成计划后执行构建、安装、启动和限时采集。未指定 `--output` 时，工程运行证据默认写入工程父目录的 `.ark-evidence`，避免将大 HAP 复制到系统临时盘。已安装 CLI 时可把前两条模块命令替换为 `ark-device doctor` 和 `ark-project prepare/run`。详细安装方式见 [ark-device 工具说明](tools/ark-device/README.md#本地安装包)。

也可以直接向 Agent 发起请求：

```text
使用 Ark 构建并运行当前鸿蒙工程到已连接真机。
采集 30 秒与本应用相关的日志，分别报告构建、安装、启动、日志完整性、SDK 信号和业务验收；不要卸载应用或清除应用数据。
```

先阅读首次运行生成的 `report.md`，再按需检查 `report.json`、`build.log` 和 `target.log`。工具操作成功只表示本次构建、安装、启动或采集成功，不代表全部业务已通过。

<details>
<summary>完整包布局、更新与旧名称</summary>

安装目录名可以不同，但应保留以下相对布局：

```text
ark/
  SKILL.md
  ark-migrate/SKILL.md
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
  tools/ark-device/  # optional CLI source; install separately
```

子技能依赖共享资源，不支持只复制一个子目录。缺失资源应从同一版本的完整包恢复，不生成到业务项目中。宿主只发现根入口时，可以通过 `ark` 加载子技能；跨安装器行为尚未完整验证。

更新时保留本地修改，取得同一修订的完整包。安装目录为干净的 Git 克隆时，可运行 `git pull --ff-only`；存在改动或分叉时先处理差异，不强制覆盖。更新后刷新技能发现或重启宿主。

旧名称包括 `harmonyos-arkts-skill`、`arkts-scan`、`arkts-ui`、`arkts-flow`、`arkts-capability`、`arkts-verify`。更新后使用下表中的名称。

</details>

</details>

## 技能地图

不确定从哪里开始时用 `ark`。边界已清楚时，可直接使用专项技能，不必依次调用全部入口。

| 技能 | 何时使用 |
| --- | --- |
| [ark](SKILL.md) | 选择任务路径和需要的专项技能 |
| [ark-migrate](ark-migrate/SKILL.md) | 分析原生 Android 功能并协调鸿蒙迁移 |
| [ark-scan](ark-scan/SKILL.md) | 识别项目结构、调用链和安全修改范围 |
| [ark-language](ark-language/SKILL.md) | 处理 ArkTS 类型、导入、编译诊断和局部 TS 适配 |
| [ark-ui](ark-ui/SKILL.md) | 修改页面、状态、导航和生命周期 |
| [ark-flow](ark-flow/SKILL.md) | 处理业务规则、请求、缓存、取消和重试 |
| [ark-kit](ark-kit/SKILL.md) | 接入权限、存储、网络、定位等平台能力 |
| [ark-native](ark-native/SKILL.md) | 处理 Node-API、C/C++、CMake、ABI 和库加载 |
| [ark-test](ark-test/SKILL.md) | 规划、编写、诊断测试，开展全项目缺陷发现 |
| [ark-check](ark-check/SKILL.md) | 规划或执行已有检查，汇总构建与运行证据 |

常用流程：

- **开发**：`ark-scan` → 按需实现 → `ark-test` / `ark-check`。
- **迁移**：`ark-migrate` → 目标扫描与实现 → 测试验证 → 汇总迁移状态。
- **测试**：`ark-test` → 按授权交给实现技能修复 → 回归验证。

测试可穿插实施；`ark-check` 复用仍有效的结果。只执行已有检查时直接用 `ark-check`，边界不清时先扫描。

可选的 [ark-device 接入](references/device-cli.md) 可安装和启动已签名 HAP，并采集限时日志；`ark-check` 汇总相关证据。源码位于 [tools/ark-device](tools/ark-device/README.md)，需单独安装。未配置时，继续使用项目已有命令。

## 高级工作流

<details>
<summary>设备验证：完整流程</summary>

### 让 Agent 运行工程并分析日志

准备完整 Ark 技能包、项目现有 DevEco 命令行工具链及依赖、有效签名，并连接已开启调试且已解锁的设备。无需打开 DevEco Studio 界面，但仍需要它提供的 SDK、构建和设备工具。`ark-device` / `ark-project` 是可选工具，不是新增 Skill；仓库提供源码，不会随技能加载自动安装。

```text
使用 Ark，将当前鸿蒙工程构建并运行到已连接真机，采集 30 秒日志并分析启动问题。
先确认模块、Ability 和签名配置；保留已有改动，不卸载或清除应用数据。
将执行结果、日志完整性、SDK 信号和业务验收分别报告。
```

1. **识别目标**：`ark` → `ark-scan`，确认工程、模块、product/target、Ability 和现有工具链。
2. **运行采集**：`ark-check` 复用命令行构建、签名安装、启动和限时采集；已有安装包时可只启动采集。
3. **分析修复**：按证据交给对应实现技能；日志报错不直接等于根因，修复后复测同一场景。
4. **业务验收**：`ark-test` 定义预期，`ark-check` 汇总实际结果；进程存在或没有错误日志不等于业务通过。

结果包括阶段报告、构建日志和目标进程日志（按实际执行生成）。报告含本地路径和标识，分享前检查。`ark-project run` 默认将证据写入工程父目录的 `.ark-evidence`；需要其他位置时，以 `--output` 指向一个新的、空间充足的目录。详见[工程到真机流程](references/project-device-workflow.md)、[报告判读](references/device-cli.md)和[离线业务验收](references/offline-business-acceptance.md)。

### 日志过滤与无界面验收

高频工程可使用 `--level E,W`、`--tag <标签列表>` 或 `--regex <正则>` 缩小设备端采集范围，减少丢行。过滤掉的日志不属于本次观察范围，不能据此判断不存在问题。

`--acceptance <文件.json>` 可声明本次窗口内的稳定进程、必须出现的日志和禁止出现的日志。日志完整且全部条件满足时为 `passed`；出现禁止项、缺少必需项或进程不稳定时为 `failed`；采集丢行、截断或不完整时为 `blocked`。它不操作 UI，`passed` 不代表页面、地图渲染或完整业务流程已经验收。完整配置见 [ark-device 工具说明](tools/ark-device/README.md#无界面验收)。

</details>

<details>
<summary>Android 到鸿蒙迁移</summary>

### Android 到鸿蒙迁移

`ark-migrate` 支持 Kotlin/Java、XML/Compose 原生 Android 源码分析，目标为原生 HarmonyOS Stage 项目。分析模式只读、不运行构建；实施模式只修改获授权的目标功能，保留现有架构与改动。

1. **提供输入**：源与目标目录、源变体、目标 SDK、首批功能和允许执行的范围。目标尚不存在时，先明确位置、应用身份和初始化方法。
2. **分析功能**：记录来源证据、依赖和验收条件，决定复用、重写、替代或阻塞，不猜测平台 API 的对应关系。
3. **实施一个完整流程**：例如列表搜索，覆盖输入、请求、结果、空态和错误，复用现有 Ark 专项技能。
4. **补测试**：使用独立预期验证业务规则和边界。源项目构建与测试需要单独执行授权。
5. **逐项验收**：记录差异、检查结果和阻塞；所需运行时证据缺失时保持待验证，设备接入后按授权补齐。

```text
用 ark-migrate 分析指定 Android 源项目到指定鸿蒙目标项目的迁移。
先输出功能清单、依赖替代与验收条件。只读，不修改文件、不运行构建。
```

这套流程旨在减少调用链梳理、平台调研和回归规划的重复工作，节省程度尚未量化。它不提供一键语法翻译、APK 反编译或 Flutter/RN 迁移。历史用户数据搬迁需要单独方案，不等于实现相同存储功能。

详细规则：[迁移分析与依赖决策](references/android-migration.md) · [状态定义与两端验收](references/migration-acceptance.md)。

</details>

<details>
<summary>测试与缺陷发现</summary>

### 测试与缺陷发现

`ark-test` 支持测试规划、编写回归测试、测试诊断和全项目缺陷发现。复用已有测试设施，以独立预期和受控异步顺序检查行为。

全项目模式先建立模块与流程清单，再按风险选择补测范围，报告已复现 Bug、疑似问题和未覆盖部分。测试可帮助发现缺陷，不能保证找全所有 Bug。只读规划不修改或执行；测试编写和全项目请求可在授权范围内补测试并运行聚焦用例，不默认修复生产代码。

```text
用 ark-test 对整个项目进行缺陷发现，先扫描并建立测试基线，再按风险补测试。
只修改测试文件，不修复生产代码；报告已复现 Bug、疑似问题和未覆盖范围。
```

详细规则：[测试设计](references/testing-design.md) · [鸿蒙测试环境](references/testing-harmony.md) · [全项目测试](references/testing-project-sweep.md)。

</details>

## 支持范围与验证状态

| 范围 | 约定 |
| --- | --- |
| 项目与版本 | 面向原生 Stage / ArkTS，以目标 SDK 为准；ArkUI V1/V2 不等于 ArkTS 语言版本。不自动转换 FA、Web 或后端项目 |
| 离线或无设备 | 可分析源码、配置和本地 SDK，执行环境支持且获授权的检查；缺失的文档或运行证据标为未知或未执行 |
| 宿主 | 需要读取本地 Markdown 的 Agent，不强制特定 MCP；脚本使用 Python 3.10+ 标准库。跨平台、跨宿主和安装器兼容性未完整实测 |
| 包检查记录 | 根技能包 17 项通过，1 项因主机无法创建符号链接而跳过；设备工具 59 项模拟测试通过；隐私与差异空白检查通过 |
| 真机记录 | 可选设备工具已在同一 Windows 工具链和一台 USB 真机上完成两个 Stage 工程的构建、安装、启动及采集；YinMap 的低噪声、无界面稳定进程断言通过，不代表地图渲染或全部业务通过 |
| 尚未验证 | 模型行为评估、真实 Android 迁移、其他操作系统、多物理设备、复杂多 HAP/HSP 部署及全部 SDK 版本；模型评估须按 [行为验收场景](tests/skill-scenarios.md) 在隔离新上下文中记录。第二个工程通过不等于普遍兼容 |

Ark 不要求额外账号或密钥，不将项目签名、证书、客户数据和生产配置存入技能包。仅读取任务相关内容，配置、依赖、数据、构建、安装及设备操作遵循实际授权范围，已有明确授权不重复确认。

平台约束优先查询已配置的官方文档工具，缺失时使用官方网页并核对本地 SDK；离线或来源冲突时保留未知，不自动升级 SDK 或替换签名。详见 [官方文档证据](references/official-document-evidence.md) 和 [修改边界](references/harmony-risk-boundaries.md)。

## 详细文档与维护

| 主题 | 参考 |
| --- | --- |
| 语言与 UI | [ArkTS 适配](references/arkts-language-adaptation.md) · [状态、导航与架构](references/arkui-and-architecture.md) |
| 业务与平台 | [异步数据一致性](references/async-data-consistency.md) · [权限与平台能力](references/platform-capabilities.md) |
| 构建排障 | [环境诊断](references/build-environment.md) · [工程案例](references/engineering-examples.md) |
| 验证 | [验证规范](references/verification.md) · [Agent 行为验收场景](tests/skill-scenarios.md) |

<details>
<summary>可选扫描脚本与包检查</summary>

只读扫描用于盘点 Stage 模块、配置、权限、Kit 导入、测试和 Native 边界：

```bash
python scripts/audit_harmony_project.py /path/to/harmony/project --json
```

在完整技能包根目录执行包检查，测试使用临时合成工程，无需鸿蒙 SDK：

```bash
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B scripts/check_skill_privacy.py .
git diff --check
```

隐私扫描只报告类别与位置，不回显敏感值；可用 `--term` 指定私有业务词，不内置行业黑名单。扫描工具提供线索，不代替构建和实际运行验证。

</details>

## 许可证

[MIT](LICENSE)

</details>

---

<details>
<summary id="english"><strong>English</strong></summary>

## Quick Start

Ark is an Agent skill package for native HarmonyOS Stage / ArkTS projects. It includes one router and nine focused skills.

Ark reuses the project's architecture and grounds decisions in official documentation, the selected SDK and observed checks. It is domain-neutral and does not replace official docs, SDKs or DevEco tools.

### 1. Choose An Entrypoint

| Your goal | Suggested entrypoint |
| --- | --- |
| Understand a project or define a safe change boundary | `ark` or `ark-scan` |
| Migrate an Android feature | `ark-migrate` |
| Add tests or find defects | `ark-test` |
| Run a signed project on a connected device and diagnose logs | `ark` → `ark-check`, use `ark-project` when needed |

### 2. Install The Complete Package

Give the following requirements to a local Skill-capable agent:

```text
Install the complete Ark skill package from https://github.com/Jaxanyn/harmonyos-arkts-skill.
Preserve the relative layout of SKILL.md, all ark-* directories, references, scripts and tests.
Install to a skill directory supported by this host. Preserve existing changes and unrelated skills.
```

### 3. Send The First Request

Then request a read-only analysis in your target project:

```text
Use ark to identify this HarmonyOS project's modules, SDK and the impact of my task.
Recommend the next skills. Read-only: do not edit files or run tests or builds.
```

The result should include a project map, impact boundary and suggested skills. These are Skill entrypoints, not terminal commands. Hosts with explicit invocation can use `$ark`; others can read the root [SKILL.md](SKILL.md) and follow its links.

<details>
<summary>Device verification: quick path</summary>

### Run A Project On A Connected Device

This route is for a standard, signed single-HAP Stage project. It requires an unlocked USB debugging device plus the project's existing DevEco SDK, Hvigor and dependencies. The workflow builds the project, replaces the installed HAP and launches the app. Confirm that these actions are authorized before running.

The Ark skill package routes Agent work. `ark-device` and `ark-project` are local CLIs installed separately or invoked from source; loading a skill never installs or runs them automatically.

From `tools/ark-device/src` in the complete skill package, run:

```powershell
python -B -m ark_device doctor
python -B -m ark_device.project prepare --project "<absolute-project-path>"
python -B -m ark_device.project run --project "<absolute-project-path>" --seconds 30
```

`prepare` only reads configuration and shows the selected module and Ability. `run` creates a plan, then builds, installs, launches and captures bounded logs. Without `--output`, project-run evidence goes in `.ark-evidence` beside the project, avoiding a large HAP copy to the system temporary drive. With an installed CLI, use `ark-device doctor` and `ark-project prepare/run` instead. See [local installation](tools/ark-device/README.md#本地安装包) for package details.

You can also give an Agent this request:

```text
Use Ark to build and run the current HarmonyOS project on the connected device.
Capture 30 seconds of app-relevant logs. Report build, install, launch, log coverage,
SDK signals and business acceptance separately. Do not uninstall or clear app data.
```

Read the first-run `report.md` before inspecting `report.json`, `build.log` and `target.log` as needed. A successful tool operation does not establish that all application behavior passed.

<details>
<summary>Package layout, updates and legacy names</summary>

The installation directory name may differ; preserve this relative layout:

```text
ark/
  SKILL.md
  ark-migrate/SKILL.md
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
  tools/ark-device/  # optional CLI source; install separately
```

Child skills require shared resources; copying a child directory alone is unsupported. Restore missing resources from the same complete revision, not into the application project. Hosts exposing only the root can load children through `ark`. Cross-installer behavior is not fully verified.

Update the complete package at one revision while preserving local edits. A clean Git-based install can use `git pull --ff-only`; reconcile dirty files or divergence before updating, without forcing overwrites. Refresh skill discovery or restart the host afterward.

Legacy names include `harmonyos-arkts-skill`, `arkts-scan`, `arkts-ui`, `arkts-flow`, `arkts-capability` and `arkts-verify`. Use the names below after updating.

</details>

</details>

## Skill Map

Start with `ark` when unsure. Use a focused skill directly when the boundary is clear; not every task needs every entrypoint.

| Skill | When to use it |
| --- | --- |
| [ark](SKILL.md) | Select the task route and focused skills |
| [ark-migrate](ark-migrate/SKILL.md) | Analyze native Android features and coordinate migration |
| [ark-scan](ark-scan/SKILL.md) | Identify structure, call paths and safe edit scope |
| [ark-language](ark-language/SKILL.md) | Handle ArkTS types, imports, compiler diagnostics and scoped TS adaptation |
| [ark-ui](ark-ui/SKILL.md) | Change pages, state, navigation and lifecycle behavior |
| [ark-flow](ark-flow/SKILL.md) | Handle business rules, requests, caching, cancellation and retries |
| [ark-kit](ark-kit/SKILL.md) | Integrate permissions, storage, networking, location and platform services |
| [ark-native](ark-native/SKILL.md) | Work on Node-API, C/C++, CMake, ABI and library loading |
| [ark-test](ark-test/SKILL.md) | Plan, write and diagnose tests or find defects across a project |
| [ark-check](ark-check/SKILL.md) | Plan or run existing checks and summarize build/runtime evidence |

Common workflows:

- **Development**: `ark-scan` → relevant implementation → `ark-test` / `ark-check`.
- **Migration**: `ark-migrate` → target discovery and implementation → testing → migration status.
- **Testing**: `ark-test` → authorized fix through the implementation owner → regression verification.

Tests can accompany implementation; `ark-check` reuses valid results. For existing checks only, use `ark-check` directly, scanning first if scope is unclear.

The optional [ark-device integration](references/device-cli.md) installs and launches signed HAPs and captures bounded logs; `ark-check` summarizes the evidence. Source lives in [tools/ark-device](tools/ark-device/README.md) and must be installed separately. Existing project commands remain the fallback.

## Advanced Workflows

<details>
<summary>Device verification: full workflow</summary>

### Run A Project And Diagnose Logs

Prepare the complete skill package, the project's existing DevEco command-line toolchain and dependencies, valid signing, and an unlocked debugging-enabled device. The IDE window need not be open; its SDK/build/device tools are still required. Optional `ark-device` / `ark-project` source is included in this repository; installation is separate and never automatic when loading skills.

```text
Use Ark to build the current HarmonyOS project, run it on the connected device,
capture 30 seconds of logs and diagnose startup issues. Verify the target first,
preserve existing changes, and do not uninstall or clear app data.
Report execution, capture coverage, SDK signals and business acceptance separately.
```

Use `ark` → `ark-scan` to establish the target, `ark-check` to execute approved commands, the relevant implementation skill for an evidenced fix, and `ark-test` / `ark-check` for scenario acceptance. Installed-app retests can skip installation. A live process or zero error logs is not a business pass. `ark-project run` stores evidence under `.ark-evidence` beside the project by default; use `--output` with a new directory on a drive with sufficient space when needed. Review local identifiers before sharing reports.

### Log Filtering And No-UI Acceptance

For high-volume apps, use `--level E,W`, `--tag <tag-list>` or `--regex <pattern>` to narrow device-side capture and reduce dropped lines. Filtered-out logs are outside the observation window and cannot establish that an issue is absent.

`--acceptance <file.json>` can declare a stable process, required log patterns and forbidden log patterns for this capture window. Complete evidence with all conditions met is `passed`; a forbidden pattern, a missing required pattern or an unstable process is `failed`; dropped, truncated or incomplete capture is `blocked`. It does not operate the UI, so `passed` is not acceptance of rendering or the complete business flow. See [no-UI acceptance](tools/ark-device/README.md#无界面验收).

See [project-to-device workflow](references/project-device-workflow.md), [report interpretation](references/device-cli.md) and [offline acceptance](references/offline-business-acceptance.md).


</details>

<details>
<summary>Android to HarmonyOS migration</summary>

### Android To HarmonyOS Migration

`ark-migrate` analyzes Kotlin/Java and XML/Compose source for a native HarmonyOS Stage target. Analysis is read-only with no builds. Implementation edits only authorized target features while preserving existing architecture and changes.

1. **Supply inputs**: both roots, source variant, target SDK, initial features and execution scope. For a missing target, first establish its location, identity and initialization method.
2. **Analyze features**: record source evidence, dependencies and acceptance criteria; decide reuse, rewrite, replacement or blockers without guessing API equivalence.
3. **Implement one complete flow**: for example, search with input, request, results, empty and error states, using existing Ark skills.
4. **Add tests**: use independent expectations for business rules and boundaries. Source builds and tests require separate execution scope.
5. **Accept each feature**: record differences, results and blockers. Missing required runtime evidence leaves the feature unverified; complete authorized checks when a device is available.

```text
Use ark-migrate to analyze the specified Android source and HarmonyOS target.
Produce a feature ledger, dependency replacements and acceptance criteria.
Read-only: do not edit files or run builds.
```

This aims to reduce repeated call-path discovery, platform research and regression planning; savings have not been measured. It does not offer one-click translation, APK decompilation or Flutter/RN migration. Historical user-data transfer needs its own plan and is distinct from equivalent storage functionality.

Details: [migration analysis and dependencies](references/android-migration.md) · [status and parity acceptance](references/migration-acceptance.md).

</details>

<details>
<summary>Testing and bug discovery</summary>

### Testing And Bug Discovery

`ark-test` supports planning, regression authoring, diagnosis and whole-project discovery. It reuses existing tooling, independent expectations and controlled async ordering.

A project sweep maps modules and flows, then selects tests by risk and reports reproduced bugs, suspicions and untested areas. Testing can uncover defects but cannot guarantee finding every bug. Read-only planning does not edit or execute. Authoring and sweep requests allow scoped test changes and focused runs, not automatic production fixes.

```text
Use ark-test to find bugs across this project: map modules, establish the baseline,
then add risk-ranked tests. Edit tests only, not production code.
Report reproduced bugs, suspicions and untested boundaries.
```

Details: [test design](references/testing-design.md) · [HarmonyOS test environment](references/testing-harmony.md) · [project sweeps](references/testing-project-sweep.md).

</details>

## Scope And Verification Status

| Area | Boundary |
| --- | --- |
| Projects and versions | Native Stage / ArkTS, following the target SDK. ArkUI V1/V2 is not the ArkTS language version. No automatic conversion of FA, web or backend projects |
| Offline or no device | Analyze source, config and local SDK declarations; run supported, authorized checks. Missing documentation or runtime evidence remains unknown or not-run |
| Host | An agent that reads local Markdown; no mandatory MCP. Scripts use the Python 3.10+ standard library. Cross-platform, host and installer compatibility is not fully tested |
| Package check record | 17 root-package tests passed; one skipped because the host cannot create symlinks. The device tool has 59 passing simulated tests. Privacy and diff whitespace checks passed |
| Device evidence | The optional tool completed build/install/launch/capture for two Stage projects on one Windows toolchain and USB device. YinMap passed a low-noise no-UI stable-process assertion; this is not acceptance of map rendering or all application behavior |
| Not yet verified | Model evaluations, real Android migrations, other operating systems, multiple physical devices, complex multi-HAP/HSP deployment and all SDK versions. Record model evaluations in isolated fresh contexts using the [behavioral acceptance scenarios](tests/skill-scenarios.md); two projects do not establish universal compatibility |

Ark requires no extra account or secret and does not store project signing, certificates, customer data or production configuration in the skill package. Read only task-relevant content. Configuration, dependencies, data, builds, installation and device operations follow the actual authorization scope; existing explicit authorization remains valid.

Use configured official documentation tools first, then official web sources and local SDK cross-checks. Offline or conflicting evidence stays unknown; do not automatically upgrade SDKs or replace signing. See [official evidence](references/official-document-evidence.md) and [edit boundaries](references/harmony-risk-boundaries.md).

## Detailed Guides And Maintenance

| Topic | References |
| --- | --- |
| Language and UI | [ArkTS adaptation](references/arkts-language-adaptation.md) · [State, navigation and architecture](references/arkui-and-architecture.md) |
| Business and platform | [Async consistency](references/async-data-consistency.md) · [Permissions and platform capabilities](references/platform-capabilities.md) |
| Build diagnosis | [Environment diagnosis](references/build-environment.md) · [Engineering examples](references/engineering-examples.md) |
| Verification | [Verification rules](references/verification.md) · [Agent acceptance scenarios](tests/skill-scenarios.md) |

<details>
<summary>Optional scanner and package checks</summary>

The read-only scanner inventories Stage modules, config, permissions, Kit imports, tests and native boundaries:

```bash
python scripts/audit_harmony_project.py /path/to/harmony/project --json
```

Run package checks from the complete package root. Tests use temporary synthetic projects without a HarmonyOS SDK:

```bash
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B scripts/check_skill_privacy.py .
git diff --check
```

Privacy output reports categories and locations, not sensitive values. Supply private business terms with `--term`; there is no built-in industry blacklist. Scanning provides signals, not build or runtime verification.

</details>

## License

[MIT](LICENSE)

</details>
