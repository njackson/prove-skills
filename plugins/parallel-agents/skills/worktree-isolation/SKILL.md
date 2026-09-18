---
name: worktree-isolation
description: Opens, closes and tidies git worktrees so that no two streams of work ever share a checkout: one tree per stream, branched from the remote tip, closed by rebase and never by force. Use when a second piece of work has to start before the first one lands, before handing an agent a branch, or when asked to open, close, list or tidy worktrees.
allowed-tools: [Bash, Read]
---

# Worktree isolation

The discipline, not one project's implementation. Where a repository provides its own helper
scripts, prefer them — this describes what they are for and what to do when there are none.

## The one rule everything else protects

**Two agents must never share a working tree.** A checkout that moves under a running build makes
its results fiction — in both directions, so the passing run is as untrustworthy as the failing
one, and you will not know which kind you got. Every parallel stream gets its own tree, and the main workdir stays single-threaded.

## Opening one

1. **Refuse to open a worktree from inside a worktree.** Check `git rev-parse --git-dir`; if it
   contains `worktrees/`, say so and stop. Nesting them makes cleanup a guessing game.
2. **Branch from the remote tip, not the local one.** `git fetch origin <trunk>` first, then create
   from `origin/<trunk>`. A tree branched from a stale local ref starts life behind and discovers
   it during the merge, which is the worst moment.
3. **Keep them all under one parent** — a single directory the repository already ignores. Scattered
   worktrees make `git worktree list` the only inventory, and cleanup guesswork.
4. **One branch name per tree**, the slug verbatim. If it exists already, ask rather than guessing a
   suffix — a reused branch name is how two streams end up on one branch.

## Before opening, if the project has a preflight

Worktrees are cheap in git and expensive on a machine: each is a full checkout, usually with its
own `node_modules`, its own file watches and its own temp files. A project that has learned this
the hard way will have a script for it — run it, and stop if it says stop. Where there is none, at
least check free space on the filesystem holding the repo and on `/tmp` before adding another —
the failure mode is not a slow build, it is several agents dying at once with no obvious cause.

## Closing one

From inside the tree, in order:

1. The working tree is clean, or stop and say what is dirty.
2. CI is green on the branch's head. If the project gates on CI, this is the gate — not a read of
   the diff.
3. `git fetch` and rebase onto the trunk. **On conflict, stop.** Surface the markers; never
   `--skip` or `--abort` on the agent's own judgment.
4. Push the branch's commits to the trunk.
5. Leave the tree, remove it, delete the branch.

**Never force-push a trunk.** A rejected push means somebody landed while you worked: pull with
rebase and try again. Force is how their work disappears, silently, with the push
reported as a success.

## The shared stash stack

`git stash` is per REPOSITORY, not per worktree — every tree pushes onto the same stack. A bare
`git stash` in one tree and a `git stash pop` in another silently applies the wrong changes to the
wrong checkout, and git reports both commands as having worked. Never use bare stash in a worktree. If the project provides a safe-stash helper,
use it; otherwise commit to a scratch branch instead, which is recoverable and unambiguous.

## Tidying

A tree whose commits are all present on the trunk is closeable. List them, show the driver what
would go, and remove only after one confirmation — then prune. Removing without asking is how work
that had not landed yet disappears.
