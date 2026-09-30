# Implementation

## Overview

Staged implementation plans for proposals that have already been
**accepted** -- turned from "should we?" into "here's the landing
order." A file here is a trackable stage ladder for work that's going
to happen (or has just happened), so accepted work has a home instead
of living informally in commit messages or an issue thread.

Mirrors the role of
[ARKlight's `docs/Implementation/`](https://github.com/ARKlight-Ecosystem/ARKlight/blob/main/docs/Implementation/README.md).

## Where this sits between an idea and a settled record

Three different states of a piece of design work, three different
places:

- **An open proposal** ([`docs/proposal/`](../proposal/README.md)) --
  *unsettled*. Nobody has decided yet. Proposals are a working
  reference, not permanent documentation.
- **`docs/implementation/`** (here) -- *accepted, not yet (fully)
  built*. A maintainer has looked at the proposal and said "yes, in
  this order" -- what's left is turning each staged rung into actual
  commits.
- **[`docs/foundational/`](../foundational/README.md)** -- *settled
  and shipped*. Once every stage in a ladder here is actually done,
  whatever is a permanent design decision (not just a shipped
  feature) graduates into `docs/foundational/`, and the file here is
  trimmed or removed.

## What belongs here

- A staged, rung-by-rung implementation ladder for a proposal that's
  been accepted, for work that's shipped or is about to.

## What doesn't

- An idea nobody has committed to yet -- that's
  [`docs/proposal/`](../proposal/README.md).
- A permanent design decision that's already shipped -- that's
  [`docs/foundational/`](../foundational/README.md).

## Index

Nothing has been accepted into a staged plan yet -- there's no app
code to stage work against. This index stays empty until the first
proposal is accepted.

| File | Covers |
| --- | --- |
| _(none yet)_ | |

## Contributing

When a proposal is accepted, write its stage ladder here rather than
jumping straight to code -- add a row to the Index table above when
you do. Once every stage in a ladder here has actually shipped, roll
its permanent decisions into `docs/foundational/` and trim or remove
the file here.
