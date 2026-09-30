# Notepad++ for Linux Documentation

This folder is the documentation index for the project. Start here,
then follow the links below into the subfolders for the kind of
document you need.

This structure -- and the lifecycle rule each folder follows -- is
adopted directly from
[ARKlight's own `docs/` layout](https://github.com/ARKlight-Ecosystem/ARKlight/blob/main/docs/README.md),
since ARKlight is this project's frontend dependency and we're
following its documentation conventions rather than inventing our
own.

## Folder Guide

### [`docs/foundational/`](foundational/README.md) -- permanent

The core reading for understanding how this project works and why
it's built the way it is: architecture, design rationale, the
ARKlight/Flask split, and anything else that's a settled decision
rather than in-flight work. **Not deletable** -- this is the permanent
design record for the project, updated in place rather than removed.

### [`docs/implementation/`](implementation/README.md) -- working reference

Staged, rung-by-rung landing orders for work that has been
**accepted** but isn't fully built yet. A file here is a trackable
plan for something that's going to happen, not an idea someone is
still debating.

### [`docs/proposal/`](proposal/README.md) -- working reference

Open, unsettled ideas -- "should we?", not yet "here's how." A
proposal graduates into `docs/implementation/` once accepted, or is
simply dropped if it isn't. Proposals are not permanent documentation
and shouldn't be treated as a decision record.

## The lifecycle, in one line

An idea starts in `docs/proposal/` (unsettled) -> gets accepted and
moves to `docs/implementation/` as a staged plan (accepted, in
progress) -> once every stage ships, whatever is a permanent design
decision graduates into `docs/foundational/` (settled) and the
implementation file is trimmed or removed. Nothing in
`docs/foundational/` is ever just deleted once its "purpose" is
fulfilled -- there's no expiry condition for foundational design
knowledge.

## Contributing to the Docs

If you add a new doc file, add a row for it to the relevant subfolder
`README.md`'s index so this structure stays accurate. If a folder's
index doesn't have an Index table yet, that just means nothing has
been written there yet -- add the table when you add the first file.
