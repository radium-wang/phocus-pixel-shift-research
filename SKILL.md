---
name: phocus-pixel-shift-research
description: Build the included Phocus 4.1.1 ARM64 Mac bridge for local X2D pixel-shift merging, or guide Windows adapter development on the user's installation; Windows merging is not yet implemented.
---

# Phocus Pixel-Shift Research

Use for local `.3FR` sequence inspection, original adapter compilation and 4/6/16-frame research runs. The repository includes original Mac adapter source, not Phocus components. The skill may call Phocus components that the user has installed and is authorized to use. The repository does not package, distribute or automatically obtain those components; the user is responsible for confirming the applicable license and permissions. Do not install this skill locally unless requested.

## Platform preparation

- On Apple Silicon macOS, run `python3 scripts/prepare_native_bridge.py -o <new-local-build-dir>`. This checks the installed Phocus version and pinned dependency hashes, compiles `native/macos` with Apple's `clang++`, checks the built adapter and writes `build.json` plus `bridge-profile.json`. No prebuilt adapter or user-supplied bridge is needed for this supported build. If the compiler is absent, explain the Apple Command Line Tools requirement; do not install it silently.
- Current Mac support is exactly the pinned Phocus 4.1.1 ARM64 installation at `/Applications/Phocus.app`, tested with X2D 100C sequences. Intel Macs and other Phocus builds need separate compatibility work. Do not alter expected hashes to force a mismatch through. Successful dependency checks are not sample-processing acceptance.
- On Windows, read [references/windows-native-development.md](references/windows-native-development.md). Start from the actual installation and continue local interface analysis, original adapter development and compilation when evidence permits. `prepare_native_bridge.py` currently records discovery and returns `windows-adapter-required` (exit 3). No working Windows merger is shipped or verified. Do not present this state as complete Windows support.

## Workflow

1. Run `scripts/scan_3fr_sequences.py <photo-dir> -o <new-candidates.json>`. Preserve originals. Read every group's files, timestamp source and warnings. Exact frame count and a time gap are only grouping candidates, not proof of a capture sequence. Do not guess frame order or split 8/12/16 frames into smaller sequences by arithmetic.
2. Confirm groups against capture records, sequence metadata or user-provided grouping. If that evidence is unavailable, ask for grouping confirmation. Write a new manifest with `--confirm-group group-001` (repeat as needed), or `--groups-file <groups.json>` containing ordered relative-path arrays. `--expected-count` only filters; it does not confirm a sequence. A changing source directory requires a fresh review of candidate IDs.
3. For the supported Mac build, read the bridge path, SHA-256 and profile from the locally generated `build.json`. Pass those explicitly to the runner. An externally supplied bridge can still be selected through `--bridge` or `PHOCUS_NATIVE_BRIDGE`, with its trusted expected hash. Do not recursively discover executables or substitute an unverified bridge.
4. Run `scripts/run_local_bridge.py <confirmed-manifest> -o <new-run-dir> --bridge <path> --bridge-sha256 <expected-digest>`. The runner supports `--phocus-app <path>` and configurable `--timeout-seconds` (default 3600 per group). It checks input hashes before each group, pins the bridge hash, reads the Phocus version, and verifies framework hashes if configured in a bridge profile.
5. With the included Mac source, request `--native-tiff --bridge-profile <build-dir>/bridge-profile.json`; this enables the calibrated native raw roundtrip and TIFF export route. TIFF may be produced without a separate positional intermediate output. Only request `--native-tiff` with a reviewed `--bridge-profile` declaring the supported variables. The runner clears inherited `PHOCUS_*` variables and sets only supported ones. See [references/implementation-contract.md](references/implementation-contract.md) for the profile and CLI contract.
6. Read top-level and per-group `run.json` files. Normal group failures continue; interruption stops the run. Preserve partial outputs, byte logs and cleanup records. The runner retains temporary files for audit; it does not automatically delete them. All-failed or partial-failed runs return nonzero.
7. TIFF output gets independent first-IFD dimensions, bit depth, channels and size inspection; this is not full pixel decoding or proof of HNCS/native color accuracy. FFF/RGB outputs remain unverified intermediates with unknown dimensions unless separately inspected. Do not label them as finished images. Do not call 16-frame input a distinct 16-shot kernel without independent evidence.

On Windows, discovery is read-only inventory plus bounded `--version`/`--help` probes. It does not copy application files or infer that a plugin name is a working merge route. A bridge still needs explicit implementation or user configuration. Report groups, success/failure, outputs and limitations briefly. Make visual/JSR comparisons only when requested.

## Distribution boundary

The skill may call Phocus components that the user has installed and is authorized to use. Do not package, distribute or automatically obtain those components in this repository. The user is responsible for confirming the applicable license and permissions. Use the authorized local installation without bypassing licensing or integrity checks. Do not write to a camera or upload photographs without explicit authorization. This workflow does not implement camera-side capture or provide a public 6/16-frame camera trigger.
