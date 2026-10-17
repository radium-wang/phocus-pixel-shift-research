# Phocus Pixel Shift Research Skill

## 中文版

用于本地哈苏 X2D 100C 像素位移实验的 Codex skill：扫描原片、确认分组、检查本机 Phocus、编译原创适配桥、验证依赖，再调用原厂处理和 TIFF 导出路径。默认保留原片，不上传照片。

### 平台状态

| 平台 | 当前能力 |
| --- | --- |
| Apple Silicon Mac + 本仓库锁定的 Phocus 4.1.1 | 包含原创桥源码；支持本地编译、依赖验证、4／6／16 张原厂 TIFF 路径实验 |
| Intel Mac 或其他 Phocus 构建 | 尚未适配；版本或组件哈希不匹配会停止 |
| Windows | 可扫描、发现本地安装，并按 skill 指导研究接口及开发桥；**尚无已实现、验收通过的 Windows 合成桥** |

Python 3.10+；Mac 编译需要 Apple Command Line Tools 的 `clang++`。本仓库不安装 Phocus 或编译器，不附带预编译的桥。

### 在对话中使用

安装或加载 skill 后，告诉 agent：

```text
使用 $phocus-pixel-shift-research，检查本机 Phocus，编译兼容的桥，处理 /path/to/raw 中的照片。
```

支持的 Mac 环境不再要求用户自己寻找现成 bridge 或输入哈希；agent 从本地构建记录读取这些配置。张数与时间只能确定候选分组，需要按实际拍摄序列确认顺序。Windows 会进入本地适配开发流程，缺少接口证据时明确报告阻塞，不能把发现成功说成合成成功。

### Mac 本地编译和运行

```bash
# 每次使用新目录；只检查依赖和编译，不处理照片。
python3 scripts/prepare_native_bridge.py -o /path/to/new-build

# 查看候选，核对实际拍摄顺序。
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/candidates.json

# 核对后确认；多组可重复 --confirm-group，或提供有序 --groups-file。
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/confirmed.json --confirm-group group-001
```

`new-build/build.json` 记录 bridge 路径、SHA-256、编译命令、源码哈希及兼容性结果。将其中的值传给 runner：

```bash
python3 scripts/run_local_bridge.py /path/to/confirmed.json \
  --output-root /path/to/new-output \
  --bridge /path/to/new-build/native-fff-bridge \
  --bridge-sha256 SHA256_FROM_LOCAL_BUILD_JSON \
  --bridge-profile /path/to/new-build/bridge-profile.json \
  --native-tiff
```

当前桥固定使用 `/Applications/Phocus.app`。编译前和运行时检查指定组件哈希；不匹配应研究新版本接口，不能把当前哈希填入旧配置强行运行。构建成功只是依赖验收，最终以样片实际处理结果为准。

### Windows 本地适配流程

```powershell
python scripts/prepare_native_bridge.py -o C:\work\new-phocus-build
```

当前 Windows 分支只生成发现和待开发报告，退出码为 3。它不会编译一个假桥。agent 随后按 [Windows 开发与验收流程](references/windows-native-development.md) 检查本机 PE 模块、接口和 ABI，在证据充分时编写并编译原创适配代码，再用样片验证。**目前不能承诺 Windows 用户仅提供照片目录就能自动合成。**

已静态检查官方 Windows 4.1.1 安装包，发现 `PhocusApi64.dll` 的 multi-shot API 线索；详见 [Windows 静态检查](references/windows-4.1.1-static-findings.md)。这不等于合成验收。

只做安装发现：

```powershell
python scripts/discover_phocus_windows.py --no-probe -o phocus-windows-discovery.json
```

### 验证、输出与限制

- 原片在启动每组前核对 SHA-256；失败组保留记录并继续，中断会停止，默认每组超时 3600 秒。
- 本地记录包括版本、组件／桥哈希、有效环境变量、命令、原始字节日志、部分输出及清理记录。
- 完整 TIFF 请求不要求额外的 positional 中间文件；桥可能只生成 roundtrip FFF 与 TIFF。
- TIFF 首 IFD 元数据检查不证明所有像素正确，也不证明 GUI 等价或 HNCS 色彩参考一致。
- RAW 中间文件预览借用首张原片；16 张输入不证明存在独立 16-shot 内核；缺失的坏点信息等研究限制仍保留。
- 临时文件默认保留。若只需验收不留成片，agent 在专用临时目录处理、检查并清理，只保存日志和数值。

离线测试：`python3 -m unittest discover -s tests -v`。真实验收范围见 [validation.md](references/validation.md)。完整契约见 [implementation-contract.md](references/implementation-contract.md)。

### 组件使用

Skill 可以调用用户自己安装且有权使用的 Phocus 组件；仓库不打包、分发或自动获取这些组件，用户需自行确认其许可和使用权限。本仓库提供原创编排与适配源码，不包含相机写入或云端上传代码。

---

## English version

A local Codex skill for Hasselblad X2D 100C pixel-shift experiments: scan frames, confirm grouping, inspect local Phocus, compile an original adapter, verify dependencies, then invoke native processing and TIFF export. Originals are preserved and photos are not uploaded by default.

### Platform status

| Platform | Current capability |
| --- | --- |
| Apple Silicon Mac + the exact pinned Phocus 4.1.1 build | Original adapter source, local compilation, dependency checks, experimental native TIFF processing for 4/6/16-frame sequences |
| Intel Mac or other Phocus builds | Not adapted; version or component hash mismatches stop execution |
| Windows | Local scanning/discovery and guided interface/adapter development; **no implemented, accepted Windows merge adapter yet** |

Python 3.10+ is required. Mac compilation uses Apple's Command Line Tools `clang++`. This repository does not install Phocus/compiler tools or ship a prebuilt adapter.

### Conversational use

After installing or loading the skill:

```text
Use $phocus-pixel-shift-research to check local Phocus, compile a compatible bridge and process /path/to/raw.
```

The supported Mac route no longer requires users to locate a prebuilt bridge or supply its hash manually; the agent reads local build records. Frame counts and timestamps provide candidates, not capture-order proof. Windows enters local adapter development and must report missing evidence honestly.

### Compile and run on Mac

```bash
# Use new directories. Preparation checks/builds without processing photos.
python3 scripts/prepare_native_bridge.py -o /path/to/new-build

python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/candidates.json

# Confirm only after reviewing capture order; repeat for additional groups.
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/confirmed.json --confirm-group group-001

python3 scripts/run_local_bridge.py /path/to/confirmed.json \
  --output-root /path/to/new-output \
  --bridge /path/to/new-build/native-fff-bridge \
  --bridge-sha256 SHA256_FROM_LOCAL_BUILD_JSON \
  --bridge-profile /path/to/new-build/bridge-profile.json \
  --native-tiff
```

Read the actual bridge path/hash from `new-build/build.json`. That record also includes source hashes, command and dependency results. The current adapter requires `/Applications/Phocus.app`. Do not replace pinned hashes to force unsupported private ABI layouts through. Compilation/dependency checks do not replace sample-processing acceptance.

### Windows local adaptation

```powershell
python scripts/prepare_native_bridge.py -o C:\work\new-phocus-build
```

The Windows branch currently writes discovery/development records and exits 3; it does not compile a placeholder bridge. The agent follows [Windows development and acceptance](references/windows-native-development.md) to inspect local PE interfaces/ABI, implement original code when evidence supports it, compile and validate samples. **A photo-directory-only Windows merge workflow is not yet available.**

The official Windows 4.1.1 package has been statically inspected; multi-shot API clues in `PhocusApi64.dll` are recorded in [Windows static findings](references/windows-4.1.1-static-findings.md). This is not merge acceptance.

Inventory without launching Phocus:

```powershell
python scripts/discover_phocus_windows.py --no-probe -o phocus-windows-discovery.json
```

### Validation, artifacts and limits

- Inputs are hash-checked before each group. Normal failures retain records and continue; interruption stops. Default timeout is 3600 seconds per group.
- Records include versions, dependency/bridge hashes, effective environment, commands, raw byte logs, partial artifacts and cleanup policy.
- Native TIFF export can succeed with a roundtrip FFF and TIFF only, without the positional intermediate artifact.
- First-IFD metadata inspection does not prove pixel correctness, GUI equivalence or HNCS color-reference agreement.
- Intermediate RAW previews inherit the first source preview. Sixteen inputs do not establish a distinct 16-shot kernel; other research limitations remain explicit.
- Temporary files are retained by default. For disposable validation, the agent uses an isolated temporary directory, verifies and removes image artifacts, retaining numerical evidence/logs only.

Offline tests: `python3 -m unittest discover -s tests -v`. See [validation.md](references/validation.md) for actual acceptance scope and [implementation-contract.md](references/implementation-contract.md) for the contract.

### Component use

The skill may call Phocus components that the user has installed and is authorized to use. The repository does not package, distribute or automatically obtain those components; the user is responsible for confirming the applicable license and permissions. This repository provides original orchestration/adapter source, without camera-write or cloud-upload code.
