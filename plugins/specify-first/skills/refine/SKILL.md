---
name: refine
description: Turns a vague ask into work an independent agent can pick up cold: maps the journey, settles every open question, names the risks, then slices it into vertical tickets with the walking skeleton first. Use when starting anything bigger than a single edit, when a ticket is too thin to hand off, or when asked to refine, spec, or break down work.
# An orchestrator: the driver starts it by name. See README.md for the layering rule.
disable-model-invocation: true
---

# Refine

You take something half-formed and leave behind tickets that carry their own context — enough that
an agent opening one cold, with no memory of this conversation, can do the work.

## The test this skill is built around

**Could a stranger do this ticket?** Not "is it written down" — could someone who was not here read
it and start? Every phase below exists to close a gap that would otherwise be filled by a
conversation only you remember.

## The rule that governs everything you write

**You must not become the bottleneck you exist to remove.** The driver's scarce resource is
attention, not typing — and asking one question at a time costs a round trip each, so six of those
is most of an afternoon of the only thing this skill is spending. So:

- Questions come in **batches**, as a numbered list, each with two or three options where the answer is a choice — one word each to answer, not an essay.
- Never ask what you can look up. Read the code, the tickets, the transcript first, then ask about
  what genuinely cannot be determined.
- Never write a paragraph where a task would do.
- One phase at a time. Do not publish a document that asks about phase 3 while phase 1 is open.

## Where the output goes

Story mapping and example mapping are general practices — Patton's and Wynne's respectively — and
this skill runs them itself. What varies is where a project keeps the RESULT.

If it keeps scenarios in a pipeline of its own — a spec suite, feature files, an acceptance
framework with maturity stages — put the mapping's output there and cite it, rather than keeping a parallel account in a separate document. If it has no such home, the refinement document is the home. Either
way the mapping happens here; only its resting place moves.

## The four phases

Keep ONE document and revise it as you go — the phases are sections in it, not separate docs. A markdown file where the project keeps its plans or decisions is enough; if there is no such place, `docs/refinement/<slug>.md`.

### 1 — Map the story

Before requirements, the journey. Two techniques, and they answer different questions.

**Story mapping** (Patton) — for anything with a shape. Lay the user's activities left to right in
the order they happen: the backbone. Under each, the tasks that make it up, most important at the
top. Now you can see the whole path at once, and the horizontal cuts through it ARE the slices
phase 3 will pull — a release is a line across the map, not a column of it. This is why mapping
first makes slicing honest later: the slice already exists on the map.

Mark where the backbone breaks: steps that do not exist, steps that exist and are bad, steps
nobody has considered. Those are the candidates.

**Example mapping** (Wynne) — for one behavior, once the map says which. Take the story, and
under it write the *rules* that govern it. Under each rule, concrete *examples* — real values,
real cases, the awkward ones especially. And beside them, the *questions* nobody in the room can
answer. Timebox it; if a story is still generating questions after twenty-five minutes, it is not
ready and the questions are the finding.

The four things — story, rules, examples, questions — are the whole output. Rules with no example
are opinions. Examples with no rule are trivia. Questions are phase 2's input.

Ask about shape, never implementation. "Does this start from a notification, or from them opening the app?" is a requirement. "Should we use a websocket?" is not.

### 2 — Grill until nothing is open

Interrogate your own draft, starting with the questions example mapping produced — those are
already the ones that block. For every claim in it, ask: do I know this, or am I assuming it? An assumption becomes either something you verify (read the code, run the command, check the transcript) or a question for the driver. **Never carry an assumption into a ticket.**

Ask in batches of three to six, grouped by what they decide. Ask again after the answers — a
resolved question usually reveals the next one. Keep going until a round produces no new questions.

**Then name the risks.** For each one: what could make this fail or cost far more than expected,
how would you find out early, and what would you do about it. A risk with no early signal is a
`spike` — the ticket whose only job is to find out. Say so, and size it in hours, not story points.

Refinement is finished when the document has zero unanswered questions and every risk either has a
mitigation or a spike. If the driver chooses to proceed with questions still open, that is a decision they are entitled to make, and it is not your cue to stop asking: record each open question as an accepted unknown with a named owner, so it rides along with the ticket instead of vanishing into it.

### 3 — Slice vertically

Now break it down — and the shape of the break-down matters more than its size.

If phase 1 produced a story map, the slices are already drawn on it — a slice is a horizontal cut
across the backbone, thin but complete. Read them off rather than inventing a new decomposition.

**The first ticket is a walking skeleton**: the thinnest possible path that goes all the way
through, end to end, and is real. Not a schema, not a component library, not "the backend part".
Something a person can actually do, however badly it does it. If the first ticket cannot be
demonstrated to somebody, it is a layer and you have sliced the wrong way.

**Every ticket after it is a slice of the same elephant.** Each adds one capability along the whole
path, each is demonstrable on its own, and each leaves the system working. Prefer many thin slices
to few thick ones — a slice that cannot be finished in a sitting is two slices.

Say the blocking edges out loud: which tickets cannot start until which others land, and why.
Where two tickets touch the same files, say that too — it decides what can run in parallel.

### 4 — Make each ticket portable

A ticket is not a title. Write into each one, in the tracker itself, everything the stranger needs:

- **What and why** — the slice of journey this delivers, in one or two sentences.
- **The decisions already made**, with their reasons. This is where the answered questions go —
  every one of them, phrased as the decision it produced. This is the part that only exists because
  refinement happened, and the part that makes the ticket portable.
- **What is deliberately not in this ticket**, so the agent does not helpfully widen it.
- **Where to look** — the files, the conventions, the neighboring code.
- **How it will be verified** — the behavior to prove, not the implementation to write. Name the
  depth of verification this slice has to reach, so the person doing it knows before they start
  whether a passing test suite is the finish line or the first step.
- **Any risk this slice carries**, and its early signal.

Write it with `gh issue edit` (or the tracker's own command) so the context lives on the ticket, not in a planning document that an independent agent will never open. The document is where refinement
happened; the ticket is what survives it.

Those six headings are a template, and a template is checkable. Put them in the tracker's issue
template, and if the project has a ticket lint or a bot on new issues, teach it to reject a ticket
whose decisions section is empty. Then the rule stops depending on anybody remembering it, which
includes you.

## When to stop and hand back

- The driver's answers keep changing the shape → the journey map is wrong, go back to phase 1.
- You cannot find an early signal for a risk → that is a spike, and the spike is the next ticket.
- The work is one edit with no open questions → say so and skip this entirely. Refinement is a cost
  and it is not always worth paying.
