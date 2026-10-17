# Implementation contract

This skill deliberately separates reusable orchestration from vendor-owned components.

The reusable part scans user-owned `.3FR` files, groups frames, hashes inputs, invokes a user-local bridge, and verifies outputs. The bridge and the Phocus frameworks remain on the user's machine.

A local bridge may be built or configured by the user under their own Phocus license. The skill must not download or redistribute Phocus frameworks, extracted symbols, proprietary model files, or license material. It also must not patch a binary to defeat authorization or integrity checks.

A 4- or 6-frame FFF is an intermediate native result unless a native export step writes a verified color-managed TIFF. A 16-frame result may use a native multi-shot input path without proving that the binary contains a separate 16-shot kernel. Preserve that distinction in reports.

The wrapper records source directory, manifest, file hashes, Phocus path/version, bridge hash, command, environment flags, logs, output type, dimensions, and cleanup events. The workflow is read-only with respect to the camera and does not upload photographs by default.
