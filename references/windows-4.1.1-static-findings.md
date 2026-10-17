# Windows Phocus 4.1.1: static findings

Checked on 2026-10-17 from the installer identified by the [official Phocus software catalog](https://api.hasselblad.com/products/downloads/133/software). The installer was downloaded and unpacked locally; it was not installed or executed. Vendor payloads remain outside this repository.

- Official installer: `https://cdn.hasselblad.com/software/Phocus_for_PC/4.1.1/Phocus-4.1.1-x64.exe`
- Installer bytes: 174164600
- Installer SHA-256: `996db33b736cdc4332c2a2af9f6e998ea260ff0236e147f11424c10aa25fc844`
- WiX bundle contains a Phocus MSI; MSI SHA-1 matched the bundle manifest (`668B6D01FB1B4D807AC014515F0A16D7802C7AC6`). This is an internal integrity cross-check, not independent publisher-signature verification.
- Install layout: `[ProgramFiles6432Folder]Hasselblad\Phocus 4.1.1`, launching `Phocus64.exe`. Discovery must cover versioned directories and the `Phocus64.exe` name.
- Main processing module: `PhocusApi64.dll`, AMD64 (`0x8664`), 8192 named PE exports.
- Module SHA-256: `70b697d839378c58de086cb82b81ecefd2b1d723ea7361bcdaef0c8a04a6211a`.

Relevant export names include:

```text
CSharp_PhocusfNative_CCameraImage_AddMultishotRawFilters___
CSharp_PhocusfNative_CCamera_GetSixShotImg___
CSharp_PhocusfNative_CCamera_SetSixShotImg___
CSharp_PhocusfNative_CCamera_SetMultiShotPosList___
CSharp_PhocusfNative_CRawImageFile_GetMultiShotPosList___
CSharp_PhocusfNative_sRawDescription_IsPreprocessed3ChannelMultiShot___
```

The module also contains diagnostic strings naming `CMultiShotCapture::AddShot()` and six-shot interpolation moving into the filter chain, plus the `CTiffSaveHandler` RTTI name. This is evidence of relevant internal processing code, not proof of an externally callable merge API or a working 16-frame route. No direct named `CMultiShotCapture::AddShot` / `CMultiShotCapture` constructor export or `SaveTIFF` export was identified in the named export table. Their absence there does not mean the implementation is absent internally.

The next investigation should inspect managed `Phocus.dll` metadata and the `CSharp_PhocusfNative_*` wrapper declarations/call sites to establish types, ownership and initialization. For merge operations not exposed by those wrappers, independently establish the Windows internal ABI from this exact module. Do not transplant Mac offsets or guess signatures. No Windows source-build bridge, runtime sample merge or GUI equivalence has been accepted in this work.
