---
name: improve-agent
description: Makes an agent measurably better by changing only the text it reads (a prompt, a skill, a tool description, a context file) and keeping a change only when it clears the noise. Use when you changed one of those and want to know whether it helped, when asked to tune, optimize or improve an agent against fixtures, or when a rubric keeps missing the same way. Not for a known bug with a known fix, and not for a change you cannot measure yet.
# An orchestrator: the driver starts it by name. See README.md for the layering rule.
disable-model-invocation: true
allowed-tools: [Bash, Read, Write, Edit, Agent]
---

# Improve agent

You are the optimizer. You propose changes to what an agent reads, you measure them, and you keep
only what survives. You do not decide whether a change survived; the noise floor decides, and a
verifier with no stake in the answer confirms it. Everything below exists to keep those three roles
apart, because the moment one thing proposes, measures and judges, every change it likes is a win.

## Who owns what

Write this down at the top of the frontier file before the first round, and do not move the line.

- **The driver owns** the fixtures, the rubric, the safety set, and the gate. Changing any of them
  changes the meaning of every score ever quoted. If a fixture or a rubric line turns out to be
  wrong, that is a finding for the driver, in its own commit, with the reason — never a step inside
  a round.
- **The loop owns** the text the model reads: the system instructions, a skill's body, a tool's
  description and the descriptions of its arguments, the guidance strings a tool returns with its
  result, a context file. That is the whole search space, and it is larger than the prompt. The
  guidance a tool returns beside its data is text too, and it is where the reliable wins have come
  from.
- **The witness owns the verdict.** See "The verdict", below.

The ownership line is also an allow-list, so enforce it as one. The fixtures, the rubric and the
safety set live in paths the loop does not write to, and `git diff --name-only` before every commit
says whether that held. A loop that can edit its own scoreboard will eventually edit it, in good
faith, at four in the afternoon.

One component per round. A change that touches two of them cannot be attributed, and the next round
cannot build on it.

## Before the first round

**Fixtures.** Saved inputs standing for situations that matter, each with what a good answer looks
like. If the project keeps a fixture set and a runner, use them and cite them. If it does not, make
the smallest honest one: five real inputs (harvested from runs a person corrected, not invented),
a rubric with at least three criteria that two people would score the same way, and a note of
where each came from. Fewer than five fixtures and the loop is measuring the dice.

Split them: a **train** set the loop reads misses from, and a **validation** set it never sees until
admission. With five, that is three and two. The split is thin; say so in the log rather than
pretending otherwise.

**The judge.** If the project has a scorer, use it. If it has none and a model can score the rubric,
write the rubric as the judge's instruction and have it return, per criterion, a score and one
sentence saying why — the sentence is what the next round reads, and a score without one is
useless to you. If no model judge is trustworthy for this rubric, a person scores, and the loop
runs at the speed of that person.

**The baseline and its noise.** Run the unchanged system N times over the full set — N full passes,
not N goes at one fixture — and record, per fixture, the median, the minimum, and the spread. That
spread is the noise floor. Nothing below is a win until it clears it. Three runs is the least that
means anything; ten is honest. If a fixture's spread is bimodal — mostly fine, sometimes a
collapse — write that down; it changes what "better" means for it (see "Keep or discard").

**The budget.** Rounds, wall-clock, or cost, written in the frontier file before the first round.
Crossing it is a stop, not a warning.

**The frontier file.** One file in the repository, wherever the project keeps decision records,
holding: the ownership lines above; the budget; the baseline table; and, per candidate, its id,
its parent, the component it changed, the change itself (the full new text, not a description),
its screening scores, and its full-set medians if it was admitted. The frontier is the set of
candidates that hold the best median on at least one fixture. It is reviewed like a schema, and it
is what the next session resumes from.

## The round

1. **Pick a parent.** From the frontier, weighted by how many fixtures it leads on
   (`scripts/frontier.py`). Early on that is
   the baseline. Do not always take the best aggregate; a candidate that leads on one hard fixture
   is worth extending.
2. **Run a minibatch.** Three train fixtures, one run each, with the parent. Collect the score, the
   judge's sentence, and the transcript for each.
3. **Reflect.** Read the transcripts before the scores. Look at the tool results before the model's
   reply: a "wrong" answer is often the right answer to a lying tool, and no wording fixes that —
   report it and stop the round. Then find the recurring miss, not the one-off. Propose one change
   to one component that would have fixed it, and say in the log which miss it targets and what
   score you predict.
4. **Screen.** Run the child on the same minibatch. If it does not beat the parent there, record it
   and go back to step 1. This is cheap and noisy; it prunes, it does not admit.
5. **Admit.** Run the child N times over the full set. Compare medians per fixture. It enters the
   frontier only if it leads on at least one fixture and no fixture's median fell by more than that
   fixture's noise band.
6. **Gate.** Run the safety set — the behaviors that must never regress — its own N times. One
   failure in N is a fail, and it is a revert even when the score went up. The loop cannot win by
   weakening what it was told not to touch.
7. **Log.** One entry per round, whatever happened: parent, component, change, prediction, screen,
   admission, gate, verdict. A reverted round is a finding; write why.

Stop when the budget is spent, when two rounds in a row admit nothing, or when a round finds a
structural cause (a tool contract, a data contract, a transport bug) — that is not this loop's
work, and pretending a prompt can paper over it is how the next ten rounds get wasted.

## Keep or discard

The candidate that leaves the loop is the frontier's best aggregate, and it has not proved anything
yet. It has been screened by the same process that proposed it. So, before anyone acts on it:

- **Clear the floor.** Run baseline and winner N times each on the validation set and run a
  permutation test with the arm labels flipped within each fixture (`scripts/permutation.py`). Write the
  confidence level down before you run it. If it does not clear, the result is *unconfirmed* — not
  useless, not shown.
- **Read the tail.** Report the minimum beside the median. One catastrophic run in a system that
  talks to people is the finding, not noise to average away.
- **Variance collapse counts.** When the baseline was bimodal on a fixture, a change that removes
  the failure mode — spread goes from wide to narrow, worst run rises — is a keep on that ground
  even if the median barely moved. Medians measure level; spreads measure reliability; the person
  on the other end meets the worst run.
- **Measure what the change costs.** A candidate that scores better and runs ten times slower, or
  calls a tool ten times more often, is a regression wearing a win. Time it. Count the calls.

## The verdict

You proposed the change, so you do not grade it. Dispatch the project's read-only verifier — an
agent whose tool list has no edit tools; the `witness` definition shipped beside this skill is one
— with the frontier file, the log, the winner's diff, and the validation numbers, and ask for the
`verify-work` report: what holds, what does not, what it could not verify. Record its verdict as
given. The deliverable is the branch, the frontier file, the log, and that report. Nothing merges
from inside this loop.

## Never

- Never edit a fixture, a rubric line, or the safety set to make a score move. If one is wrong, stop
  and hand it back.
- Never decide on one run. Not for a keep, not for a revert, not "to save time".
- Never re-run only the fixture you were aiming at. The whole set, every admission.
- Never let the proposer grade. That is what the verifier is for.
- Never let a change teach the model a specific — a timing, a name, a number — that no tool
  confirms. If the prompt teaches it, the model will say it, including when it is false. Text
  supplies voice and next actions; tools supply facts.

## The two pieces of arithmetic

They live beside this file, in `scripts/frontier.py` and `scripts/permutation.py`, and they are run
rather than read. A script costs only its output, it gives the same answer twice, and neither of
these is arithmetic you want regenerated from a description on a Friday. If the project already has
a statistics module, cite that instead and delete these two.

- `python scripts/frontier.py frontier.json` prints the frontier weighted by fixtures led, and picks
  a parent.
- `python scripts/permutation.py baseline.json candidate.json --alpha 0.05` prints the observed
  difference, the p-value, and whether it cleared.

Never shuffle scores freely across fixtures; a hard fixture is hard in both arms, and pretending
otherwise makes chance look quieter than it is. `permutation.py` flips the arm label within each
fixture for that reason, and it is the line in it most worth reading before you trust a result.

## Where wins come from, and where they do not

Told by mechanism and date, from one storefront's loop, so the rules above survive a hurry.

- **25 May 2026.** A nudge to "offer to move it forward" dropped one fixture from 78 to 8: the
  model fabricated the answer in the same turn as its tool call, before the result arrived.
  Reverted. Proactivity instructions are the riskiest class of text change; the safe shape is
  propose-then-confirm, anchored to a result already returned.
- **26 May 2026.** A regression on two fixtures hid for five rounds because each round re-ran only
  its own target. The change blamed for it was neutral; the branch had already regressed. Hence:
  the whole set, every admission.
- **9 July 2026.** One fixture scored 78, then 5, then 12 on identical code. The two low runs
  called no tool and confidently invented a handoff. Decisions had been made on single samples
  before that; none of them were evidence.
- **9 July 2026.** Fabricated promises — "email you back today", a four-hour window — were traced
  to the prompt's own worked examples. The fix was not better wording: the tool now returns the
  promised window as data, and the text says to echo it verbatim. Ten of the loop's largest wins
  were of that kind, a tool or data contract, not a sentence.
- **10 July 2026.** A full sweep ran fixtures alphabetically while an orphaned process leaked
  once per run; the head of the sweep measured the agent and the tail measured a machine being
  killed. Scores of zero that looked exactly like agent failures. A low tail on a long sweep is
  environment first, agent second; verify a shocking number with one clean run before you
  hypothesize.
- **10 July 2026.** A change scored perfectly and ran ten times slower on the hot path. Two
  "obviously better" rewrites each measured worse than the original. Time the cost of every
  candidate; the score does not carry it.

## If nothing is set up

Every "if the project has" above has an otherwise, and here they are together. No runner: a shell
loop over five saved inputs is a runner. No judge: a person with the rubric and a spreadsheet, and
the loop slows to match. No statistics module: the two scripts beside this file. No
verifier: an agent definition with no edit tools, which is a five-line file. No frontier file: the
markdown described above, started now. The loop does not need a platform. It needs the ownership
line, the baseline, the budget, and the honesty to discard a change you liked.
