# Phocus Pixel Shift Research Skill

A local Codex skill for researching Hasselblad X-System pixel-shift sequences through the user's own licensed Phocus installation and a user-supplied local bridge.

It scans a directory of `.3FR` frames, recognizes exact 4-, 6-, and 16-frame groups, writes a reproducible manifest with hashes, and can invoke a local bridge for the native processing route. Outputs and logs are written to a user-selected directory.

## Scope and legal boundary

This repository contains only original orchestration scripts and documentation. It does not contain Phocus binaries, private frameworks, extracted vendor code, firmware patches, license keys, camera-write code, or cloud upload code. Phocus and any native bridge remain separately owned and licensed by their respective vendors. Use this skill only with software and files you are authorized to use.

Acceptance of a 16-frame input group does not by itself prove that a distinct 16-shot camera kernel or capture trigger exists. Treat the manifest and output as an experiment record.

## Use in Codex

Install or load this skill from the repository, then tell the agent the local directory containing the `.3FR` frames, for example:

```text
Use $phocus-pixel-shift-research on /path/to/my/raw-directory
```

The skill will scan the directory and, when a bridge is available, run the selected 4/6/16-frame groups locally. It records command lines, environment flags, file hashes, and bridge identity.

## Standalone scripts

```bash
python3 scripts/scan_3fr_sequences.py /path/to/raw \
  --manifest /path/to/manifest.json

python3 scripts/run_local_bridge.py /path/to/manifest.json \
  --output-root /path/to/output \
  --bridge /path/to/native-fff-bridge \
  --native-tiff
```

The bridge must be a user-local executable or script that accepts a manifest group and writes the requested output. The runner checks for `/Applications/Phocus.app` on macOS and never downloads or embeds vendor software.

See [`SKILL.md`](SKILL.md) and [`references/implementation-contract.md`](references/implementation-contract.md) for the full workflow and bridge contract.
