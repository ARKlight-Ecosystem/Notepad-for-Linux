# Foundational

## Overview

The core reading for understanding how Notepad++ for Linux works and
why it's built the way it is: architecture, the ARKlight/Flask split,
and the design rationale behind them. This is reference material for
the project as a whole, not a record of a single in-flight task.

**These docs are not deletable.** Unlike the working-reference docs in
[`docs/implementation/`](../implementation/README.md) and
[`docs/proposal/`](../proposal/README.md), files in this folder are
the permanent design record for the project. They get updated as the
project evolves, but a file here should never simply be deleted once
its "purpose" is fulfilled -- there is no expiry condition for
foundational design knowledge.

This folder mirrors the role of
[ARKlight's `docs/Foundational/`](https://github.com/ARKlight-Ecosystem/ARKlight/blob/main/docs/Foundational/README.md),
one level down: ARKlight's own foundational docs cover the compiler;
this folder covers how this project uses ARKlight as a frontend
alongside a Flask backend.

## Index

| File | Covers |
| --- | --- |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the ARKlight-compiled frontend and the Flask backend fit together, what each owns, the pywebview interim-native-window amendment, where hard-coded content lives, and the testing strategy. |
| [`DESIGN-NOTES.md`](DESIGN-NOTES.md) | Per-decision design records: why pywebview, why the OS title bar stays on for now, why Escape-to-close is deferred rather than faked, why File-menu items close the dropdown with nothing else wired. |

Still planned, not yet written:

| Planned file | Will cover |
| --- | --- |
| `GETTING-STARTED.md` | Install and local dev workflow for both halves of the stack. |

Add a row to the Index table above -- with a real link -- as soon as
a planned file actually exists.
