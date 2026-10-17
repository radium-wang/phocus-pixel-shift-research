# Implementation contract

## Dependencies and limits

Python 3.10+ is required. Scanning works across platforms; optional `exiftool` provides capture timestamps. Native execution requires macOS, the user's own Phocus installation (default `/Applications/Phocus.app`), and a separately supplied bridge. The skill may call Phocus components that the user has installed and is authorized to use. The repository does not package, distribute or automatically obtain those components; the user is responsible for confirming the applicable license and permissions. Installing the skill alone does not provide merging. On Windows, `discover_phocus_windows.py` produces a read-only inventory report and bounded help/version probes; it does not prove a merge path.

## Grouping and manifest

The scanner writes schema `phocus-pixel-shift/2` with every discovered frame's path, size, SHA-256, sort coordinate and timestamp source. It refuses to overwrite an existing manifest. Output/source directories and confirmed file order must remain stable between review and execution.

EXIF is used only when all frames have parseable timestamps on the same time basis. `OffsetTimeOriginal` and `SubSecTimeOriginal` are read. Without an offset, EXIF is a shared wall-clock coordinate, not an asserted UTC capture time. Mixed offset/no-offset or incomplete EXIF makes the entire scan use mtime with a warning. Results from individual files survive nonzero exiftool exit; lookup uses a stdin argument file and a 120-second timeout. Copied mtimes and camera clock changes can make inferred grouping unreliable.

Time-based groups never span separate immediate parent directories. Counts other than exactly 4/6/16 are retained but not selected. Even valid counts are unconfirmed by default. `--confirm-group ID` confirms a candidate on a fresh scan. `--expected-count N` filters, without confirming. No automatic integer-multiple splitting is performed.

For known capture order, provide `--groups-file` with a JSON array of arrays of relative paths:

```json
[["shot01.3FR", "shot02.3FR", "shot03.3FR", "shot04.3FR"]]
```

This is an explicit grouping confirmation. Paths must stay inside the scanned directory; duplicates are rejected. Omitted frames are reported. To change confirmed grouping, create and review a fresh manifest, rather than merely flipping `selected` in an old v1 file.

## Bridge identity and invocation

Only `--bridge` (highest priority) or `PHOCUS_NATIVE_BRIDGE` is used. No directory search is performed. `--bridge-sha256` is required and compared before execution and before each group. Pin an expected digest from a trusted build record; a digest identifies bytes, not their safety or licensing status.

```text
native-fff-bridge <frames> <output> <frame-1.3FR> ... <frame-N.3FR>
```

4/6-frame destinations use `.fff`; 16-frame destinations use `.rgb16`. These are intermediates, not finished color-managed images. A successful exit must produce a nonempty intermediate. An explicit native TIFF request must also produce an inspectable TIFF.

The runner rejects non-macOS execution and records Phocus version/build from `Contents/Info.plist`. It supports `--phocus-app` for a user-installed alternate location. It does not assert that the bundle is vendor-authentic merely because Info.plist exists.

## Optional bridge profile

Supply `--bridge-profile /path/to/reviewed-profile.json`. This declares capabilities known from the bridge's documentation; it does not auto-probe or certify them. Example shape (replace placeholder hashes with trusted 64-character digests):

```json
{
  "supportedEnvironment": [
    "PHOCUS_PROBE_LABEL",
    "PHOCUS_ROUNDTRIP_FILE",
    "PHOCUS_NATIVE_TIFF_FILE",
    "PHOCUS_RETAIN_NATIVE_TIFF"
  ],
  "frameworkSha256": {}
}
```

`frameworkSha256` optionally maps paths relative to Phocus.app to expected SHA-256 digests. All configured hashes must match; no automatic acceptance on software update. An empty map explicitly means no framework hashes were checked.

Inherited `PHOCUS_*` variables are removed from the child environment. `PHOCUS_PROBE_LABEL` is set only if declared. With `--native-tiff`, both `PHOCUS_ROUNDTRIP_FILE` and `PHOCUS_NATIVE_TIFF_FILE` must be declared. Only declared flags from the following list are set to `1`:

- `PHOCUS_RETAIN_NATIVE_TIFF`
- `PHOCUS_CALIBRATED_PROBE`
- `PHOCUS_USE_NATIVE_FILE_WRITER`
- `PHOCUS_ALLOW_NATIVE_64BIT_REOPEN`

No native export flags or paths are set without `--native-tiff`. Undocumented variables are rejected. The exact profile and effective environment are recorded.

## Records and failures

Use a new output directory. Manifest validation rejects unsafe group IDs, unconfirmed selected groups, wrong frame counts, duplicated selected inputs and paths outside the source directory. Each group's input size and SHA-256 are checked against the manifest before bridge launch. Inputs and configured binaries must remain unchanged for the duration of execution; concurrent replacement is unsupported.

The runner writes top-level `run.json` before processing and updates it atomically after each group. Each attempted group has status, timestamps, elapsed time, checked inputs, effective environment, command when launched, error/exit code and retained-file cleanup record. Launched groups have raw-byte stdout/stderr logs. Normal failures continue to the next group; Ctrl-C terminates the active process group, records interruption and lists unattempted groups. Timeout defaults to 3600 seconds per group and kills the process group. SIGKILL, power loss or disk failure can prevent finalization; the latest saved record may remain `running`.

Partial outputs are retained. No temporary artifacts are deleted automatically. Successful and normally failed bridge exits record discovered intermediate/TIFF/roundtrip files, sizes and hashes. A failure before launch has no bridge logs. Preflight failures return without creating an output directory.

`inspect_output.py` reads classic TIFF/BigTIFF first-IFD metadata without third-party packages. It reports dimensions, bits per sample, channel count, sample format and byte size. It does not decode pixel data, inspect all pages, verify HNCS/color accuracy or prove that the complete native processing route was used. FFF/RGB intermediates receive only size/hash/type records; dimensions remain unknown. Acceptance of 16-frame input does not establish a distinct 16-shot capture kernel.

## Offline validation

Run `python3 -m unittest discover -s tests -v`. Tests use synthetic `.3FR` bytes, fake application metadata and a fixture bridge. They validate orchestration only, not Phocus compatibility, photographic quality or hardware behavior. No camera, vendor framework or real image merge is invoked.

## Windows discovery

Run `python scripts/discover_phocus_windows.py -o phocus-windows-discovery.json` on Windows. Use `--phocus C:\Path\to\Phocus.exe` for an explicit executable or repeat `--root` for an offline fixture. The default search checks common Program Files and Local AppData layouts and uses a bounded recursive search of each supplied root.

The report contains the executable path, SHA-256, bounded `--version` and `--help` output, adjacent layout directories, and filename hints containing terms such as `multishot`, `pixel`, `shift`, `merge`, `export`, `batch`, `cli`, or `headless`. These are discovery clues only. The script never copies, modifies, decompiles or patches Phocus files and never creates merged image output. A user must verify a candidate workflow visibly in their licensed Phocus installation before configuring a Windows bridge.
