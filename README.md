# Phocus Pixel Shift Research Skill

## 中文版

运行环境：Python 3.10+；扫描可跨平台，原厂路径执行限 macOS。

这是一个用于研究哈苏 X 系统像素位移序列的本地 Codex skill。它通过用户自己授权的 Phocus 安装和用户提供的本地 bridge，扫描、记录并运行 3FR 序列处理实验。

**前提：本仓库不附带 native bridge。只有 skill 和照片目录可以完成扫描；合成还需要另行配置的 bridge、可信构建记录中的 SHA-256、macOS 和本机 Phocus。它不是开箱即用的独立合成软件。**

### 功能

- 扫描目录中的 `.3FR` 文件，列出 4、6、16 张的候选分组，执行前需要确认实际拍摄分组。
- 为每组输入生成可复现实验 manifest、文件哈希和运行日志。
- 调用用户本机的 native bridge，执行本地 Phocus 处理路径。
- 输出目录由用户指定，默认不上传照片或实验数据。

### 在 Codex 中使用

加载本 skill 后，直接告诉 agent 原始照片目录：

```text
Use $phocus-pixel-shift-research on /path/to/my/raw-directory
```

skill 会先扫描目录。时间间隔和张数只构成候选，需要根据拍摄记录确认分组；确认后，配置好 bridge 才能处理。脚本记录命令、环境开关、文件哈希、Phocus 版本和 bridge 身份。

### 独立运行脚本

```bash
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/candidates.json

# 核对实际拍摄序列后再确认 group-001。
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/confirmed.json --confirm-group group-001

python3 scripts/run_local_bridge.py /path/to/confirmed.json \
  --output-root /path/to/new-output \
  --bridge /path/to/native-fff-bridge \
  --bridge-sha256 TRUSTED_64_CHARACTER_SHA256
```

bridge 必须是用户自己提供的本地可执行文件或脚本。请将示例哈希占位符替换为可信构建记录中的实际值；runner 不再自动搜索执行程序。默认每组超时 3600 秒，可用 `--timeout-seconds` 调整。

上述命令保留 FFF/RGB 中间结果。完整 TIFF 请求还需添加 `--native-tiff --bridge-profile /path/to/profile.json`，profile 必须声明支持的环境变量；格式见下方参考文档。TIFF 检查仅验证首个 IFD 的尺寸、位深和通道等元数据，不证明 HNCS 或完整原厂显色。失败组会保留记录并继续下一组；中断会停止，临时文件默认保留。

离线回归检查：`python3 -m unittest discover -s tests -v`。测试使用模拟文件和 bridge，不代表已验证真实 Phocus 合成。

### 范围与合法边界

Skill 可以调用用户自己安装且有权使用的 Phocus 组件；仓库不打包、分发或自动获取这些组件，用户需自行确认其许可和使用权限。本仓库只包含原创的编排脚本和文档，不包含相机写入代码或云端上传代码。

接受 16 张输入并不等于证明相机存在独立的 16 次拍摄内核或触发协议；manifest 和输出应被视为实验记录。

完整流程见 [`SKILL.md`](SKILL.md) 和 [`references/implementation-contract.md`](references/implementation-contract.md)。

---

## English version

Requirements: Python 3.10+. Scanning is cross-platform; native execution requires macOS.

A local Codex skill for researching Hasselblad X-System pixel-shift sequences through the user's own licensed Phocus installation and a user-supplied local bridge.

**Prerequisite: this repository does not include a native bridge. The skill and photo directory alone support scanning. Merging additionally requires a separately configured bridge, a trusted expected SHA-256, macOS and local Phocus. This is not a standalone, ready-to-run merger.**

### Features

- Scans `.3FR` files and proposes 4-, 6-, and 16-frame groups that require capture-group confirmation.
- Writes reproducible manifests, file hashes, and run logs.
- Invokes a user-local native bridge for the local Phocus processing route.
- Writes to a user-selected output directory and does not upload images by default.

### Use in Codex

After loading this skill in Codex, give the agent the directory containing the raw frames:

```text
Use $phocus-pixel-shift-research on /path/to/my/raw-directory
```

The skill first proposes groups. Frame counts and time gaps alone do not prove a capture sequence; confirm grouping against capture records before processing with a configured bridge. Commands, effective environment flags, file hashes, Phocus version and bridge identity are recorded.

### Standalone scripts

```bash
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/candidates.json

# Confirm group-001 only after reviewing the capture sequence.
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/confirmed.json --confirm-group group-001

python3 scripts/run_local_bridge.py /path/to/confirmed.json \
  --output-root /path/to/new-output \
  --bridge /path/to/native-fff-bridge \
  --bridge-sha256 TRUSTED_64_CHARACTER_SHA256
```

Supply your own local bridge and replace the hash placeholder with a trusted build digest. The runner no longer discovers executables automatically. The per-group timeout defaults to 3600 seconds; configure it with `--timeout-seconds`.

These commands retain intermediate FFF/RGB results. For TIFF export, also pass `--native-tiff --bridge-profile /path/to/profile.json` with declared environment capabilities; see the contract below. TIFF inspection validates first-IFD metadata only, not HNCS or complete native color processing. Failed groups retain records and continue; interruption stops the run. Temporary files are retained by default.

Offline regression check: `python3 -m unittest discover -s tests -v`. Tests use fixture files and bridges, not real Phocus merges.

### Scope and legal boundary

The skill may call Phocus components that the user has installed and is authorized to use. The repository does not package, distribute or automatically obtain those components; the user is responsible for confirming the applicable license and permissions. This repository contains original orchestration scripts and documentation, with no camera-write code or cloud upload code.

Acceptance of a 16-frame input group does not by itself prove that a distinct 16-shot camera kernel or capture trigger exists. Treat the manifest and output as an experiment record.

See [`SKILL.md`](SKILL.md) and [`references/implementation-contract.md`](references/implementation-contract.md) for the full workflow and bridge contract.
