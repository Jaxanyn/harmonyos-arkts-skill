# ark-device

供 Ark Agent 调用的本地鸿蒙工具：识别工程目标，复用现有工具链构建，再安装签名 HAP、启动应用并限时采集日志。设备 CLI 使用 Python 3.10+ 标准库与 HDC；工程自动准备还需要现有 DevEco Node/Hvigor/JSON5 工具。

本目录是 Ark 仓库中的工具源码维护位置，遵循仓库根目录的 [MIT 许可证](../../LICENSE)。技能加载不会安装或执行工具。旧业务工程中的副本仅保留本地历史；后续修改以本目录为准。

## 准备与推荐顺序

准备有效签名、已配置的 SDK/构建依赖和已解锁、已开启调试的 USB 设备。可以不打开 DevEco Studio 界面，但不能省去工具链。多设备需明确选择目标；报告输出目录必须是新目录，且有空间保存一份 HAP 和日志。

1. **检查环境**：从本工具 `src` 目录执行 `python -B -m ark_device doctor`。
2. **确认目标**：执行 `python -B -m ark_device.project prepare --project "<工程目录>"`，核对识别出的模块和 Ability；生成的计划留在本机。
3. **运行采集**：执行 `python -B -m ark_device.project run --project "<工程目录>" --seconds 30 --output "<新的证据目录>"`。构建失败时不安装旧 HAP；已安装应用可改用下文 `launch --capture`。
4. **判读与验收**：先看 `report.md`，再按需读 `report.json`、`build.log` 和 `target.log`。执行、采集、SDK 信号和业务结论分开；具体业务断言另写验收附录。

**当前交付状态**：已验证两个工程在同一 Windows 工具链和真机上的运行链路；不是所有工程兼容承诺。`0.1.1` wheel 已重建并在隔离环境离线安装，两个入口及安装后 53 项测试通过；旧 `0.1.0` 不包含最新修复。尚未发布或安装到常用环境。完整范围见[当前验证清单](VALIDATION.md#current-acceptance-summary)。

## 本地安装包

wheel 和校验文件作为单独分发产物，不随源码提交。构建时产物为 `dist/ark_device-0.1.1-py3-none-any.whl`，校验文件为 `dist/ark_device-0.1.1.sha256`；仅克隆仓库不会获得这些本地产物。验证包含包内源码一致性、`prepare.cjs` 资源、命令入口、53 项安装后测试、依赖检查和真实工程只读准备；本轮未再次运行真机。

在你选定的虚拟环境中安装，不需要下载依赖：

```powershell
python -m pip install --no-index --no-deps "<工具目录>/dist/ark_device-0.1.1-py3-none-any.whl"
ark-device --version
ark-project --help
```

`ark-device --version` 应显示 `0.1.1`。安装包只是设备工具，完整 Ark 技能包仍需单独提供；签名、SDK 和工程依赖不会随 wheel 分发。

## 使用

无需安装包即可从本工具的 `src` 目录运行：

```powershell
python -B -m ark_device doctor
python -B -m ark_device devices
```

需要命令行入口时，可在自己的虚拟环境中从工具根目录执行 `python -m pip install .`，然后使用 `ark-device`。构建包使用 setuptools；已在临时虚拟环境验证离线安装；未安装到用户常用环境，未发布。

| 命令 | 用途 |
| --- | --- |
| `doctor` | 检查 HDC 版本、设备和 aa/HiLog 必需参数；没有设备时明确标记设备检查未执行 |
| `devices` | 返回可选择的设备连接标识；列出零台设备不代表连接通过 |
| `install --hap <file>` | 检查 HAP 元数据并覆盖安装，不卸载或清数据 |
| `launch --bundle <name> --ability <name> --module <name>` | 启动已安装应用并查询主进程 |
| `logs capture --bundle <name>` | 对已运行应用采集限时日志，不启动应用 |
| `run --hap <file> --bundle <name> --ability <name> --module <name>` | 安装、先启动采集、再启动应用、观察进程并输出报告 |

所有操作支持 `--hdc`、`--device`、`--output`。参数放在具体命令后；`logs` 放在 `capture` 后。HDC 默认从 PATH 发现。多设备必须指定 `--device`，单设备可自动选择并记录。`--output` 必须是新的证据目录，避免覆盖旧报告；默认使用系统临时目录。

```powershell
python -B -m ark_device run --hap /path/to/signed.hap --bundle com.example.app --ability EntryAbility --module entry --seconds 30
python -B -m ark_device logs capture --bundle com.example.app --seconds 10
```

日志默认 30 秒，可用 `--seconds` 设置为 0 到 600 秒之间的正数。`--max-bytes` 限制采集缓冲，默认 10 MiB，最大 50 MiB；超限会停止并报告失败。安装默认超时 180 秒，可用 `--install-timeout` 调整，最大 600 秒。Ctrl+C 取消后清理本次 HDC 客户端，不关闭全局 HDC 服务。

## 结果与边界

每次操作输出 JSON，并保存 `report.json`。日志操作另保存 `target.log`。成功退出码为 0，失败为 1，参数错误为 2，取消为 130。`status` 只说明本次工具操作；`business_acceptance` 始终为 `not-run`。错误级别日志只作为诊断线索，不自动等同于已确认 Bug。

`run` 核对 HAP 内包名、模块与 Ability，记录 SHA-256，然后安装该文件。哈希用于标识读取时的产物，执行期间请勿替换该文件。签名真实性由设备安装器判定，文件名含 signed 不作为签名证据。当前只支持单 HAP；依赖其他模块的安装需要另行安排。

采集前读取设备时间，按观察到的主进程 PID 和设备时间过滤日志。时间边界精度为一秒；同一秒内旧日志可能保留。启动时的其他应用日志只暂存于有容量限制的内存，不持久化；日志文件仅保存筛选结果。未覆盖子进程、自动重启后的完整日志或日志配额丢失。主进程在起点和终点存在不代表持续存活或页面正确；PID 改变会报告失败。零目标日志不会判为采集通过。

本地报告包含实际命令、设备与路径，目标原始日志可能含敏感业务数据。标准输出省略命令原始输出，并对部分凭据模式脱敏；脱敏并不完备，分享前仍需检查。工具无网络服务或遥测；Agent 宿主可能将返回内容发送给模型。

不构建、不更改签名、权限或 SDK，不卸载、不清日志或应用数据。覆盖安装仍会更新应用，启动也可能触发应用自身网络与数据行为。失败后保留设备现状，不承诺回滚。安装超时或取消只终止本次客户端，设备端安装可能仍会完成，重试前应先确认状态。日志采集结束后应用仍运行。断点调试、UI 自动化、构建和 MCP 不在首版范围内。

## Ark 接入

在调用宿主可用的已安装 `ark-device`，或本地源码的 `python -m ark_device` 前，先读取其 `--help` 并检查版本与命令。设备操作须在用户授权范围内。`ark-check` 汇总操作证据，`ark-test` 负责测试设计，错误由现有 Ark 专项技能处理。

没有安装本工具时，Ark 继续使用项目实际 HDC 命令；此工具不是使用技能包的必备依赖。构建与 MCP 后续应复用现有执行函数，不复制一套设备实现。

## 验证

从本工具根目录运行模拟测试，不访问设备：

```powershell
python -B -m unittest discover -s tests -v
```

模拟测试覆盖目标选择、HAP 标识冲突、安装和启动的成功证据、超时、输出限额、断连、取消、旧日志过滤及零日志。真机记录见 [验证记录](VALIDATION.md)。

官方依据：[HDC](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc)。命令适配以本机 HDC 和设备帮助输出交叉核对，不承诺所有系统版本兼容。

## 已安装应用复测与地图鉴权

用户已安装新包时，无需再次覆盖安装：

```powershell
ark-device launch --capture --bundle com.example.app --ability EntryAbility --module entry --seconds 30
```

此命令先启动采集再发送启动请求；不强制停止应用，已运行时不保证重新触发地图初始化。没有新鉴权日志时结果为 `not-observed`，不能当作通过。

`diagnostics.map_authorization` 区分 `passed`、`failed`、`mixed` 和 `not-observed`，仅识别目标进程本次窗口内 Map Kit 的明确日志。内部回复 `code:6` 同时出现在授权成功和失败记录中，不参与判定。采集操作的 `status` 与鉴权状态独立；业务验收仍需单独执行。网络状态读取 `201 Permission denied`、页面回调误报等需要另行诊断，不能统称地图授权失败。

更新 Profile 后应重新构建签名 HAP；旧 HAP 不会随配置更新。对比产物哈希和包内 Profile，不能仅看文件名。`INSTALL_SIGNATURE_MISMATCH` 表示覆盖安装的签名身份不一致：恢复兼容签名，或在明确授权并处理数据保留后卸载，工具不会自动卸载。命令行构建如遇旧 JDK 无法读取新密钥库，应核对实际 Java 路径；只在构建进程中使用匹配的 Java，不重建证书来掩盖工具链错误。

## 工程构建并运行

新增 `ark-project` 编排入口，设备执行继续复用 `ark-device`。Agent 读取工程配置和现有构建命令后，生成经过审阅的本地 JSON 计划；不依赖固定 DevEco 安装路径，不自动安装 SDK 或修改签名。

```powershell
python -B -m ark_device.project inspect --project <工程绝对路径>
python -B -m ark_device.project run --plan <本地计划.json> --seconds 30
```

安装工具后可用 `ark-project inspect`、`ark-project run`。计划字段：

| 字段 | 内容 |
| --- | --- |
| `project` | 工程绝对路径 |
| `argv` | 已确认的构建参数数组，首项为实际可执行文件绝对路径；不使用命令拼接 |
| `hap` | 相对工程的签名 HAP 输出路径 |
| `bundle`、`module`、`ability` | 实际应用启动目标 |
| `product`、`target`、`build_mode` | 与构建参数一致的目标记录 |
| `env`（可选） | 仅支持 JAVA_HOME、DEVECO_SDK_HOME、PATH；只影响构建进程 |

计划是可执行输入，必须检查命令及工程钩子，不自动信任仓库中的计划。不允许放入签名密码。`inspect` 仅列出模块候选，不自动解析并选择复杂产品配置；Agent 负责读取配置消除歧义。

工具先检查设备，再构建；失败、超时或输出超限时不安装。构建成功后核对 HAP 元数据，复制并校验产物后安装。增量构建可以复用相同产物，报告会显示 `artifact_changed=false`；这不是源码到二进制的可复现性证明。构建超时只停止直接客户端，子进程可能仍在运行，重试前需确认。支持单 HAP，复杂 HSP 部署需单独安排。

报告新增 `report.md` 阶段表；`report.json` 保留详细证据。工程执行另存 `build.log` 和 `application.hap`，设备执行保存 `target.log`。这些本地文件可能含签名材料、业务日志和私有路径，不能直接提交或公开。工具不执行自动源码修复；Agent 依据证据调用 Ark 专项技能，修复后重复同一场景验证。

## 失败与取消验收

采集进程提前退出时，即使底层 HDC 返回 0，CLI 也会报告 `LOG_STREAM_ENDED` 并保留已采集日志。它证明采集未完整完成，不自动判定拔线、应用崩溃或业务失败。重新连接后应再次执行 doctor，单独开始新的验证轮次。

构建或安装取消时，已读取的命令输出会进入本地证据，阶段状态记为 cancelled，CLI 返回 130。构建输出保存在 build.log，安装命令输出在 report.json 的 commands 中。不要用关闭窗口或强杀 Agent 代替正常 Ctrl+C 验收；进程遭强制终止可能无法写报告。构建子进程、设备端安装完成情况仍需核对，不能将客户端退出当作全部执行已回滚。

当前首版范围：Python 3.10+ 标准库、单 HAP、经过审阅的项目构建计划、有限时长日志。实测环境是 Windows 和一台 USB 真机；不承诺其他系统、多个物理设备、复杂 HSP 部署及所有 SDK 版本兼容。模拟用例通过与物理验收记录分别维护。

## 只提供工程目录

标准 Windows DevEco 工程可以直接运行：

```powershell
ark-project prepare --project <工程目录>
ark-project run --project <工程目录> --seconds 30
```

`prepare` 只读取配置，生成本地计划，不构建、不安装；`run --project` 生成计划后执行构建和设备流程。Agent 应先读取工程指令，检查构建钩子并确认执行范围。用户不用手写 JSON。多个目标时通过 `--product`、`--module`、`--target`、`--ability` 明确选择，工具不会默认取第一个。

工具从 PATH 中 HDC 的上级目录发现标准 DevEco 安装，也可以使用 `--deveco` 指定安装根目录。配置读取复用该安装内的 Hvigor JSON5 解析器，不执行项目 JS，不输出签名材料。自动模式只支持已声明签名与 debug 模式、已注册的 Stage entry 模块和标准 HAP 输出路径。自定义输出用 `--hap`，其他工具布局和自定义构建命令可提供经审阅的 `--plan`，仍受当前目标与产物校验约束。安装流程仅处理单个 HAP，不支持多 HAP 协调部署；显式计划不能绕过这一限制。不保证所有工程零配置。

生成计划包含必要的本地路径和应用目标，应保留在本地。生成失败时修正具体歧义或提供显式计划，不自动修改 product、签名、SDK 或模块配置。Python 运行时仍无第三方依赖；自动准备模式额外复用本机 Node/Hvigor 自带 JSON5 包。

### Large artifacts and evidence storage

A project run copies the verified HAP into its evidence directory before installation. Ensure that drive has room for the HAP plus logs; for large packages use `ark-project run --project <root> --output <new-directory-on-a-drive-with-space>`. A failed evidence copy must not be reported as an installation failure. Preserve build evidence; a subsequent explicit artifact run can validate the successfully built HAP, but link both reports and compare the artifact hash. Do not silently install an older package or delete unrelated temporary files.

### 报告结论的四个层次

report.md 分为执行阶段、日志采集、SDK/日志信号、业务验收。顶层 status 与退出码仍表示工具操作结果，不表示业务通过；原有 JSON 字段保持兼容。

新增日志字段：device_dropped_lines_observed 汇总选中目标日志中识别到的 HiLog 丢行提示；coverage 为 bounded-window（限定窗口完成且未检测到丢失）、partial（失败、取消、截断或观察到丢行）、unknown（缺少覆盖元数据）、not-run（未采集）。采集器成功但设备丢行时，工具可成功而 coverage=partial；零丢行提示不保证所有事件都已记录。旧报告缺少字段时不能当作零丢行。

CLI 不执行业务断言，business_acceptance 保持 not-run；人工验收请另写附录，列出场景、预期、实际、证据和清理结果，不修改原始报告来制造业务通过。
