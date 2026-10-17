---
name: phocus-pixel-shift-research
description: Run local Hasselblad X2D 3FR pixel-shift research workflows through the user's own Phocus installation.
---

# Phocus Pixel-Shift Research

Use this skill when the user gives a local directory of Hasselblad X2D `.3FR` files and asks to merge or inspect 4-, 6-, or 16-frame pixel-shift sequences.

The user only needs to provide the photo directory in the conversation. Treat the directory as the source of truth, scan it recursively, and preserve the originals. Do not ask for frame counts when the scan identifies an unambiguous 4-, 6-, or 16-frame group.

## Required workflow

1. Run `scripts/scan_3fr_sequences.py` on the user directory. Write a manifest beside the outputs and report every discovered `.3FR`, its timestamp source, size, and SHA-256. Accept only groups with exactly 4, 6, or 16 frames unless the user explicitly asks for another grouping.
2. Resolve a local native bridge from `PHOCUS_NATIVE_BRIDGE`, a project-local `native-fff-bridge`, or an explicitly supplied path. The bridge must use the user's own licensed Phocus installation. If no bridge is available, stop with the exact configuration needed; do not download, copy, or reconstruct Phocus binaries.
3. Run `scripts/run_local_bridge.py` with the manifest and an output directory. Use a new run directory such as `<photo-dir>/phocus-pixel-shift-run-YYYYMMDD-HHMMSS`; never overwrite source files or an existing result.
4. Before execution, verify that `/Applications/Phocus.app` exists, record its version if available, and record the bridge SHA-256. Refuse to run when a configured bridge hash or Phocus framework hash check fails.
5. For each group, retain the native output, a per-group JSON record, stdout/stderr logs, input hashes, and a cleanup record for temporary files. Use the native full TIFF export only when the local bridge supports `PHOCUS_NATIVE_TIFF_FILE`; otherwise label the result as an intermediate FFF/RGB buffer rather than a finished image.
6. After completion, independently inspect output dimensions, bit depth, channel count, and file size. Report whether the result is a native TIFF, FFF, or intermediate buffer. Do not call a 16-frame result a separate 16-shot kernel unless the local evidence proves that.
7. Keep the summary short: groups found, output paths, completion/failure, and any limitation. Only create visual comparisons or JSR comparisons when the user requests them.

## Safety and distribution boundary

- This skill is an orchestration layer; it must not contain Phocus binaries, private frameworks, extracted vendor code, proprietary resources, license keys, or firmware patches.
- Do not bypass Phocus licensing, integrity checks, authentication, or camera firmware safeguards. Do not write to a camera.
- The user must have a lawful, licensed local Phocus installation and their own source files.
- Describe the result as local research and interoperability testing. Do not claim that the camera-side capture trigger, a public 6/16-frame UI, or a distinct 16-shot algorithm has been discovered unless independently verified.
- Do not upload photos or send results to external services unless the user explicitly requests a named destination.

## Bridge contract

The bridge is a user-local executable, not shipped by this skill. It accepts:

```text
native-fff-bridge <frames> <output> <frame-1.3FR> ... <frame-N.3FR>
```

`frames` must be 4, 6, or 16. For full native export, the bridge may honor these optional environment variables:

```text
PHOCUS_ROUNDTRIP_FILE=<temporary native round-trip file>
PHOCUS_NATIVE_TIFF_FILE=<finished TIFF destination>
PHOCUS_RETAIN_NATIVE_TIFF=1
PHOCUS_CALIBRATED_PROBE=1
PHOCUS_USE_NATIVE_FILE_WRITER=1
PHOCUS_ALLOW_NATIVE_64BIT_REOPEN=1
```

Only set these variables when the bridge documents that it supports them. The wrapper never assumes that an FFF or RGB buffer is a finished color-managed TIFF.

For the legal and technical rationale behind this boundary, read [references/implementation-contract.md](references/implementation-contract.md).
