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

Nothing has landed here yet -- this project is still at the
scaffolding stage. The first entries are expected to cover:

| Planned file | Will cover |
| --- | --- |
| `ARCHITECTURE.md` | How the ARKlight-compiled frontend and the Flask backend fit together: what ARKlight owns (the editor UI, compiled to static HTML/CSS/JS), what Flask owns (file I/O, search, anything needing a live process), and how the two talk to each other. |
| `GETTING-STARTED.md` | Install and local dev workflow for both halves of the stack. |

Add a row here -- with a real link -- as soon as a file actually
exists. Until then, treat the table above as a plan, not an index.
