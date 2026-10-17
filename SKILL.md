---
name: phocus-pixel-shift-research
description: Scan local Hasselblad X2D 3FR sequences and run a user-configured Phocus bridge for pixel-shift research; requires a separate bridge for merging.
---

# Phocus Pixel-Shift Research

Use for local `.3FR` sequence inspection or 4/6/16-frame research runs. This repository supplies orchestration, not the native bridge. A photo directory alone is sufficient for scanning; merging also requires a separately configured bridge, a trusted expected SHA-256, macOS and the user's licensed Phocus installation. The skill may call Phocus components that the user has installed and is authorized to use. The repository does not package, distribute or automatically obtain those components; the user is responsible for confirming the applicable license and permissions. State this dependency before promising a merge. Do not install this skill locally unless requested.

## Workflow

1. Run `scripts/scan_3fr_sequences.py <photo-dir> -o <new-candidates.json>`. Preserve originals. Read every group's files, timestamp source and warnings. Exact frame count and a time gap are only grouping candidates, not proof of a capture sequence. Do not guess frame order or split 8/12/16 frames into smaller sequences by arithmetic.
2. Confirm groups against capture records, sequence metadata or user-provided grouping. If that evidence is unavailable, ask for grouping confirmation. Write a new manifest with `--confirm-group group-001` (repeat as needed), or `--groups-file <groups.json>` containing ordered relative-path arrays. `--expected-count` only filters; it does not confirm a sequence. A changing source directory requires a fresh review of candidate IDs.
3. Resolve the bridge only from `--bridge` or `PHOCUS_NATIVE_BRIDGE`. Obtain its expected hash from a trusted build/configuration record; calculating a hash of an unknown executable does not establish trust. Stop with configuration instructions when the bridge is absent. Do not search personal directories or automatically obtain Phocus components; use only components the user has installed and is authorized to use.
4. Run `scripts/run_local_bridge.py <confirmed-manifest> -o <new-run-dir> --bridge <path> --bridge-sha256 <expected-digest>`. The runner supports `--phocus-app <path>` and configurable `--timeout-seconds` (default 3600 per group). It checks input hashes before each group, pins the bridge hash, reads the Phocus version, and verifies framework hashes if configured in a bridge profile.
5. Only request `--native-tiff` with a reviewed `--bridge-profile` declaring the supported variables. The runner clears inherited `PHOCUS_*` variables and sets only supported ones. See [references/implementation-contract.md](references/implementation-contract.md) for the profile and CLI contract.
6. Read top-level and per-group `run.json` files. Normal group failures continue; interruption stops the run. Preserve partial outputs, byte logs and cleanup records. The runner retains temporary files for audit; it does not automatically delete them. All-failed or partial-failed runs return nonzero.
7. TIFF output gets independent first-IFD dimensions, bit depth, channels and size inspection; this is not full pixel decoding or proof of HNCS/native color accuracy. FFF/RGB outputs remain unverified intermediates with unknown dimensions unless separately inspected. Do not label them as finished images. Do not call 16-frame input a distinct 16-shot kernel without independent evidence.

Report groups, success/failure, outputs and limitations briefly. Make visual/JSR comparisons only when requested.

## Distribution boundary

The skill may call Phocus components that the user has installed and is authorized to use. Do not package, distribute or automatically obtain those components in this repository. The user is responsible for confirming the applicable license and permissions. Use the authorized local installation without bypassing licensing or integrity checks. Do not write to a camera or upload photographs without explicit authorization. This workflow does not implement camera-side capture or provide a public 6/16-frame camera trigger.
