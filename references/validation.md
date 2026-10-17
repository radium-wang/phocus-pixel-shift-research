# Validation scope

On 2026-10-17 the original source in `native/macos` was locally compiled with Apple clang++ (C++17, ARM64, Foundation and the installed Phocus framework rpath), then tested through the repository scanner and runner on real X2D 100C sequences. Phocus 4.1.1 dependency hashes matched the committed compatibility record. Capture ordering came from prior recorded multi-shot indices, not filename/count guessing.

| Frames | Runner exit | TIFF dimensions | Channels | Bits/sample | TIFF bytes |
| --- | --- | --- | --- | --- | --- |
| 4 | 0 | 11656 × 8742 | 3 | [16, 16, 16] | 611389910 |
| 6 | 0 | 23312 × 17484 | 3 | [16, 16, 16] | 2445531446 |
| 16 | 0 | 23312 × 17484 | 3 | [16, 16, 16] | 2445531446 |

All three groups returned bridge exit 0 and runner success. FFF/TIFF artifacts were temporary and removed after checking; only logs and numerical records were retained locally. Post-run SHA-256 checks confirmed all 26 originals were unchanged. No user photographs, local absolute paths or vendor binaries are committed here.

This verifies the local source-build/native-TIFF integration on that exact installation. It does not establish Windows support, Intel support, compatibility with another Phocus build, GUI-export equivalence, complete color accuracy, or a distinct 16-shot capture kernel. The independent repository TIFF inspection reads first-IFD metadata only; this run is not a new resolution/optical-quality benchmark.

An initial build failed to resolve `@rpath` Phocus dependencies; the build command now includes the installed framework rpath. A real calibrated run also exposed an artifact-contract mismatch: native TIFF export can return without a positional intermediate. The runner now accepts a valid requested TIFF in that mode; intermediate-only mode still requires its output. Offline regression covers this case.

Run the offline suite with `python3 -m unittest discover -s tests -v`. Fixtures test orchestration and failure handling without loading Phocus; they do not replace real-image acceptance. The official Windows 4.1.1 installer was downloaded and statically unpacked; PE/interface findings are recorded in [windows-4.1.1-static-findings.md](windows-4.1.1-static-findings.md). Windows adapter compilation and native Windows sample validation remain unperformed.
