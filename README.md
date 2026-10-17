# Phocus Pixel Shift Research Skill

用于研究哈苏 X 系统像素位移序列的本地 Codex skill。它通过用户自己授权的 Phocus 安装和用户提供的本地 bridge，扫描、记录并运行 3FR 序列处理实验。

A local Codex skill for researching Hasselblad X-System pixel-shift sequences through the user's own licensed Phocus installation and a user-supplied local bridge.

## 功能 / Features

- 扫描目录中的 `.3FR` 文件，并识别精确的 4、6、16 张序列。
- 为每组输入生成可复现实验 manifest、文件哈希和运行日志。
- 调用用户本机的 native bridge，执行本地 Phocus 处理路径。
- 输出目录由用户指定，默认不上传照片或实验数据。

- Scans `.3FR` files and recognizes exact 4-, 6-, and 16-frame groups.
- Writes reproducible manifests, file hashes, and run logs.
- Invokes a user-local native bridge for the local Phocus processing route.
- Writes to a user-selected output directory and does not upload images by default.

## 在 Codex 中使用 / Use in Codex

将本 skill 安装或加载到 Codex 后，直接告诉 agent 原始照片目录：

After loading this skill in Codex, give the agent the directory containing the raw frames:

```text
Use $phocus-pixel-shift-research on /path/to/my/raw-directory
```

skill 会扫描目录，并在 bridge 可用时处理 4/6/16 张序列，同时记录命令、环境开关、文件哈希和 bridge 身份。

The skill scans the directory and, when a bridge is available, processes the 4/6/16-frame groups while recording commands, environment flags, file hashes, and bridge identity.

## 独立运行脚本 / Standalone scripts

```bash
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/manifest.json

python3 scripts/run_local_bridge.py /path/to/manifest.json \
  --output-root /path/to/output \
  --bridge /path/to/native-fff-bridge \
  --native-tiff
```

bridge 必须是用户自己提供的本地可执行文件或脚本，能够接收 manifest 分组并写出结果。macOS 上 runner 会检查 `/Applications/Phocus.app`，不会下载或内置厂商软件。

The bridge must be a user-supplied local executable or script that accepts a manifest group and writes the requested output. On macOS, the runner checks for `/Applications/Phocus.app`; it never downloads or embeds vendor software.

## 范围与合法边界 / Scope and legal boundary

本仓库只包含原创的编排脚本和文档，不包含 Phocus 二进制、私有框架、提取出的厂商代码、固件补丁、许可证密钥、相机写入代码或云端上传代码。Phocus 及任何 native bridge 均由其各自厂商单独拥有并受其许可约束。请只使用你有权使用的软件和文件。

This repository contains only original orchestration scripts and documentation. It does not contain Phocus binaries, private frameworks, extracted vendor code, firmware patches, license keys, camera-write code, or cloud upload code. Phocus and any native bridge remain separately owned and licensed by their respective vendors. Use this skill only with software and files you are authorized to use.

接受 16 张输入并不等于证明相机存在独立的 16 次拍摄内核或触发协议；manifest 和输出应被视为实验记录。

Acceptance of a 16-frame input group does not by itself prove that a distinct 16-shot camera kernel or capture trigger exists. Treat the manifest and output as an experiment record.

完整流程见 [`SKILL.md`](SKILL.md) 和 [`references/implementation-contract.md`](references/implementation-contract.md)。

See [`SKILL.md`](SKILL.md) and [`references/implementation-contract.md`](references/implementation-contract.md) for the full workflow and bridge contract.
