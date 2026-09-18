---
name: parallel-queue
description: Keeps several agents working at once against a backlog without them colliding: a worktree each, an explicit file allow-list each, branch CI as the merge gate, and a queue that refills as each one finishes. Use when more than one ticket is about to be started at the same time, when asked to fan agents out over a backlog, or when a queue of agents needs keeping full.
allowed-tools: [Bash, Read]
---

# Parallel queue

The pattern is **branch CI as the gate**, not a human reading every diff. If the project has no
automated gate on every branch push, stop and say so — without one this is a way to merge unread
code quickly, and the speed is the problem rather than the point.

## Before each agent

Run the project's preflight if it has one, and stop on a red result. Where it has none, check free
disk on the repository's filesystem and on `/tmp`, and count the trees already open, before you add
another. Worktrees consume disk, file
watches and temp space; the failure is not a slow build, it is the machine falling over with
several agents mid-flight and no obvious cause.

## What each agent gets

- **Its own worktree** — see `worktree-isolation`. Never a shared checkout.
- **One ticket**, small enough to finish in a sitting.
- **An explicit file allow-list.** This is the load-bearing instruction: an agent told only its
  goal will helpfully improve neighboring code, and the diff that arrives is no longer the diff
  that was reviewed. Name the paths it may touch, and make the check mechanical rather than
  a promise: the agent runs `git diff --name-only` against the list before committing, and the
  merge step runs it again before the branch goes anywhere. A one-line comparison in the worker's
  own pre-commit hook is the cheapest place to put it.
- **Rebase-first instructions.** Fetch and rebase onto the trunk before starting, so it is not
  building on a base that has already moved.
- **A push target that is its own branch**, never the trunk. The orchestrator merges.
- **A report format**: the branch, the SHA, the diff stat, and the last lines of the test run.

## Choosing what to run together

Order by independence before priority. Two tickets that touch the same files will collide, and the
collision costs more than the ordering saved — serialize those. Anything cross-cutting (a rename, a
dependency bump, a migration) runs alone.

## As each finishes

1. Read its local gate — typecheck and tests. Both green, or it does not merge.
2. Rebase its branch onto the trunk and push.
3. If the trunk's CI later goes red, **revert first and diagnose after.** A red trunk blocks every
   other agent in the queue, so the cheapest correct move is to put it back to green immediately.
4. Dequeue the next ticket and launch a replacement, keeping the depth constant.

## Should the workers talk to each other?

They can — most agent tools let sessions message each other — and the answer from the published work is
**sparse, never dense**, which is more specific than "it costs tokens".

Studies of communication topologies find that *moderately sparse* topologies perform best: they
suppress error propagation while still letting useful information move (Shen et al., *Understanding
the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems*,
EMNLP 2025). Fully connected arrangements do the opposite on both counts — they broadcast one
agent's mistake to everyone, and their message count grows roughly with the square of the number of
agents. Sparse debate topologies have been measured at over 40% fewer tokens for comparable or
better accuracy (Li et al., *Improving Multi-Agent Debate with Sparse Communication Topology*,
Findings of EMNLP 2024).

So:

- **Default to zero edges.** Isolated workers with an allow-list each. That is the sparse end and
  it is the right default.
- **Add ONE edge for a specific, named shared resource** — two tickets that must touch the same
  file, a schema change another ticket depends on. One message to one worker, not a channel. This
  is the case where messaging is *cheaper*: the alternative is a collision, a red trunk, a revert
  and two redone tickets, which costs vastly more than a sentence.
- **Never a broadcast, never a mesh, never a standing channel.** That is the regime the research
  measures as both worst-performing and most expensive.

And the larger lever is upstream of any of this. A failure taxonomy built from traces across seven
multi-agent frameworks (Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*, 2025) puts the largest
share of failures — roughly two in five — under specification and system design: ambiguous roles,
poor decomposition, missing termination conditions. The next largest — roughly one in three — is
inter-agent misalignment, including context lost at handoffs. Adding communication adds surface to the second category. A
sharper ticket and a tighter allow-list attack the first, which is the bigger one. Refine before
you connect.

## Stop conditions

- The backlog of independent, well-scoped tickets is exhausted.
- The trunk is red and not yet reverted.
- **Three agents in a row come back failing.** That is not three bad tickets, it is something
  systemic — a broken gate, a bad base, a machine out of space. Stop the queue and diagnose
  serially. Launching a fourth into it wastes the fourth.

## Three ways to run work at once, and which is which

- **Subagents in this session** — a few small tasks whose results you need here. They share this
  session's context budget and die with the turn.
- **This skill** — a managed queue: worktree per agent, a merge gate, and a replacement launched
  as each finishes. You stay in the loop and the depth stays constant.
- **A fire-and-forget batch** — headless workers launched from a script, no live monitoring, reviewed
  afterwards. Right when the tasks are substantial and independent and you do not want to watch.

Reach for the smallest of these that fits.

## Depth

Start smaller than the machine looks capable of. The limiting resource is rarely CPU: it is disk,
file watches, and the review capacity of the one person the whole queue reports to. Raise the depth
only after a full cycle has run clean at the current one.
