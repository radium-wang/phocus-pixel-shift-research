# Windows: local adapter development and acceptance

This mode teaches a local agent how to investigate the user's installed Windows Phocus. It is a development workflow, not a working Windows merger. The repository currently ships no Windows merge adapter, and the Mac source cannot be compiled into a functioning Windows adapter by renaming files.

For concrete module identities and API anchors from the official Windows 4.1.1 package, read [windows-4.1.1-static-findings.md](windows-4.1.1-static-findings.md). Confirm local hashes; a matching version label alone is insufficient.

## Inspect the actual installation

1. Run `discover_phocus_windows.py --no-probe -o <new-report.json>`. Confirm which executable belongs to the user's installation. Inventory adjacent PE files and their versions, machine architectures and SHA-256. Do not infer an algorithm from a filename alone.
2. Read locally installed documentation/configuration for a documented batch, automation, plugin or image-processing interface. Use it if it covers merge and native TIFF export. GUI command-line options are not assumed; unknown help flags can launch a GUI instead.
3. If no documented interface covers the task, inspect the local PE import/export tables using an available tool (for example Visual Studio `dumpbin /headers /exports /imports`). Local static analysis of the user's authorized installation can establish which modules carry multi-shot code. Record the exact files/hashes and the evidence behind each candidate. No vendor binaries go into this repository.
4. Where the installation contains managed wrappers, inspect the local managed assembly metadata and P/Invoke declarations before writing raw function-pointer calls. Windows 4.1.1 has a `PhocusApi64.dll` CSharp/SWIG export surface that is more useful than plugin filename guesses. The processing exports do not by themselves expose the complete capture/merge lifecycle.
5. Compare semantic stages, not addresses, with `native/macos`: raw decoding, correction/levels, shot position/order metadata, multi-shot accumulation/completion, native raw serialization/reopen and TIFF export. Windows C++ ABI, STL, exception handling, object layout and calling conventions must be established independently. Mach-O symbols, ARM64 offsets and object sizes are not Windows evidence.

## Write and compile original adapter source

Once a concrete interface is identified, write original source in the user's local workspace. Use explicit prototypes supported by headers or local analysis, explicit ownership and cleanup, and dependency hashes/architecture checks before calling the interface. Do not guess function addresses or execute candidates with unknown argument layouts.

Compile using the appropriate architecture and runtime toolchain (MSVC for an MSVC C++ ABI). Capture the exact build command, compiler version, source hashes and errors. Do not install a toolchain silently. Do not substitute a dummy bridge, image resize or unrelated merger for the Phocus route. A compiled executable is not an accepted implementation until sample processing passes.

The adapter should accept:

```text
native-fff-bridge.exe <frames> <output> <ordered-frame-1.3FR> ...
```

It should offer a dependency-only compatibility check without touching photos. Record supported environment/output settings explicitly; never inherit experimental Mac switches as Windows capabilities.

## Validate and integrate

On the Windows host, first use a known 4-frame group, then separately validate 6 and 16 only if the implementation supports them. Preserve originals and use a new output directory. Verify exit status, TIFF dimensions/bits/channels, nonconstant decoded pixels, complete merge/export logs and source integrity. Record each mode separately; one supported frame count does not establish the others. Remove test photos only when the user requested disposable outputs, retaining numerical results and logs.

The current `run_local_bridge.py` is Mac-specific (including process-group termination and Phocus bundle checks). A Windows implementation must additionally add and test native EXE/version validation, Windows process-tree termination on timeout/Ctrl-C, DLL dependency hashes and adapter-specific artifact checks before this runner can advertise Windows execution. Do not remove the platform check merely to make an example run.

If required entry points, ABI evidence, a Windows compiler/runtime or sample validation are unavailable, save a development report with the concrete missing items and stop before claiming a functional bridge. Do not repeatedly probe guessed signatures. The user may provide an official installer for static work, but Windows runtime acceptance still requires a Windows host.
